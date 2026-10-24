"""One complete fixed drawplate, open gripping carriage and transverse windlass bench. Static art only, no metal processing, motion or load performance."""
import math,collections,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
G={}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.fm=[];self.index={}
 def vertex(self,p):
  p=tuple(round(float(x),9)for x in p)
  if p not in self.index:self.index[p]=len(self.v);self.v.append(p)
  return self.index[p]
 def tri(self,p,mat):self.f.append(tuple(self.vertex(v)for v in p));self.fm.append(mat)
 def quad(self,a,b,c,d,mat):self.tri([a,b,c],mat);self.tri([a,c,d],mat)
 def result(self,role):
  edges={}
  for i,f in enumerate(self.f):
   for a,b in zip(f,f[1:]+f[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((i,a,b))
  assert all(len(v)==2 for v in edges.values()),[(e,v)for e,v in edges.items()if len(v)!=2][:5]
  signs={0:1};todo=[0]
  while todo:
   i=todo.pop()
   for a,b in zip(self.f[i],self.f[i][1:]+self.f[i][:1]):
    for j,c,d in edges[tuple(sorted((a,b)))]:
     if i==j:continue
     want=signs[i]*(-1 if(a,b)==(c,d)else 1)
     if j in signs:assert signs[j]==want
     else:signs[j]=want;todo.append(j)
  assert len(signs)==len(self.f)
  ff=[f if signs[i]>0 else tuple(reversed(f))for i,f in enumerate(self.f)];vol=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]]))for f in ff)/6
  if vol<0:ff=[tuple(reversed(f))for f in ff]
  assert all(dot(cross(sub(self.v[f[1]],self.v[f[0]]),sub(self.v[f[2]],self.v[f[0]])),cross(sub(self.v[f[1]],self.v[f[0]]),sub(self.v[f[2]],self.v[f[0]])))>1e-18 for f in ff)
  return dict(vertices=self.v,faces=ff,face_materials=self.fm,material=0,role=role)

def area2(p):return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1]))/2
def earclip(p):
 order=list(range(len(p))) if area2(p)>0 else list(reversed(range(len(p))));out=[]
 cr=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 while len(order)>3:
  found=False
  for j,b in enumerate(order):
   a,c=order[j-1],order[(j+1)%len(order)]
   if cr(p[a],p[b],p[c])<1e-14:continue
   if any(all(cr(p[u],p[v],p[k])>=-1e-14 for u,v in [(a,b),(b,c),(c,a)]) for k in order if k not in [a,b,c]):continue
   out.append((a,b,c));order.pop(j);found=True;break
  assert found,('untriangulable',p,order)
 out.append(tuple(order));return out


def extrude(poly,a,b,axis,mat,role):
 m=Mesh();pt=lambda p,t:(p[0],p[1],t)if axis=='z'else(t,p[0],p[1])if axis=='x'else(p[0],t,p[1])
 for t in[a,b]:
  for f in earclip(poly):m.tri([pt(poly[j],t)for j in f],mat)
 for p,q in zip(poly,poly[1:]+poly[:1]):m.quad(pt(p,a),pt(q,a),pt(q,b),pt(p,b),mat)
 return m.result(role)
def block(lo,hi,mat,role):return extrude([(lo[0],lo[1]),(hi[0],lo[1]),(hi[0],hi[1]),(lo[0],hi[1])],lo[2],hi[2],'z',mat,role)

def axial(profile,center,u,v,w,n,materials,role,phase=0):
 m=Mesh();rings=[[add(center,add(mul(w,t),add(mul(u,r*math.cos(phase+j*math.tau/n)),mul(v,r*math.sin(phase+j*math.tau/n)))))for j in range(n)]for r,t in profile]
 for k,a in enumerate(rings):
  kk=(k+1)%len(rings);b=rings[kk];ra=profile[k][0];rb=profile[kk][0];mat=materials[k]if isinstance(materials,list)else materials
  if ra==rb==0:continue
  for j in range(n):
   i=(j+1)%n
   if ra==0:m.tri([a[0],b[j],b[i]],mat)
   elif rb==0:m.tri([a[j],a[i],b[0]],mat)
   else:m.quad(a[j],a[i],b[i],b[j],mat)
 return m.result(role)
def unit(v):return mul(v,1/math.sqrt(dot(v,v)))
def beam(a,b,width,depth,mat,role):
 w=unit(sub(b,a));ref=(0,0,1)if abs(w[2])<.9 else(0,1,0);u=unit(cross(w,ref));v=cross(w,u);m=Mesh();rows=[]
 for p in[a,b]:rows.append([add(p,add(mul(u,s*width/2),mul(v,t*depth/2)))for s,t in[(-1,-1),(1,-1),(1,1),(-1,1)]])
 for row in rows:m.quad(*row,mat)
 for i in range(4):j=(i+1)%4;m.quad(rows[0][i],rows[0][j],rows[1][j],rows[1][i],mat)
 return m.result(role)



# One full newly authored fixed drawplate/carriage/windlass bench, no old mesh payloads.
G={};GROUND=[];ROOT_WITNESSES=[];AIR_POINTS=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
def box(n,lo,hi,m,role):G[n]=block(lo,hi,m,role)
def cyl(n,a,b,r,m,role,N=20):
 w=unit(sub(b,a));ref=(0,0,1)if abs(w[2])<.9 else(0,1,0);u=unit(cross(w,ref));v=cross(w,u);h=math.sqrt(dot(sub(b,a),sub(b,a)))
 G[n]=axial([(0,0),(r,0),(r,h),(0,h)],a,u,v,w,N,m,role)
for i,x in enumerate([-.90,.90]):
 for j,y in enumerate([-.22,.22]):
  f='WholeGroundPad'+str(i)+str(j);box(f,(x-.075,y-.085,0),(x+.075,y+.085,.055),0,'One whole finite grounded pad belonging to the four-legged long drawbench.');GROUND.append(f)
  n='WholeStandLeg'+str(i)+str(j);box(n,(x-.045,y-.045,.045),(x+.045,y+.045,.744),0,'One entire upright leg from its sole pad to the top crosshead.');join(n,f,(x,y,.050))
 n='WholeBedCrosshead'+str(i);box(n,(x-.085,-.285,.705),(x+.085,.285,.785),0,'One complete transverse head carries both separated long bed rails.')
 for j,y in enumerate([-.22,.22]):join(n,'WholeStandLeg'+str(i)+str(j),(x,y,.735))
 for side,y in[('Front',-.17),('Back',.17)]:join(n,'WholeLongGuideRail'+side,(x,y,.778))
for side,y in[('Front',-.17),('Back',.17)]:box('WholeLongGuideRail'+side,(-1.15,y-.040,.770),(1.15,y+.040,.860),0,'One entire long horizontal guide rail, with a genuine empty interval between the two rails. Not a solid lathe bed with a high headstock and tail quill.')
# One rigid square plate with a genuine single circular through-aperture, no rope separator.
box('WholeDrawplateFoot',(-1.10,-.245,.845),(-.88,.245,.912),1,'One whole transverse fixed-end foot spans both rails and carries the separate vertical drawplate.')
for side,y in[('Front',-.17),('Back',.17)]:join('WholeDrawplateFoot','WholeLongGuideRail'+side,(-1.00,y,.853))
m=Mesh();rows=[]
for x,inner in[(-1.035,False),(-.985,False),(-.985,True),(-1.035,True)]:
 row=[]
 for j in range(32):
  a=math.tau*j/32;c=math.cos(a);s=math.sin(a);r=.025 if inner else .18/max(abs(c),abs(s));row.append((x,r*c,1.075+r*s))
 rows.append(row)
for a,b in zip(rows,rows[1:]+rows[:1]):
 for j in range(32):k=(j+1)%32;m.quad(a[j],a[k],b[k],b[j],1)
G['WholeSquareBoredDrawplate']=m.result('One complete thick square metal drawplate with a true circular open bore through its entire thickness. The opening is empty; no drawn wire, die tolerance, reduction or metal processing is demonstrated.');join('WholeSquareBoredDrawplate','WholeDrawplateFoot',(-1.010,0,.903))
# Full single carriage across the two rails; independent open gripping halves point toward the fixed plate.
box('WholeBridgeCarriage',(-.20,-.235,.845),(.24,.235,.910),1,'One complete low bridge carriage spans both long rails, separate from the fixed bored plate and tail windlass. Fixed pose only, no verified sliding fit.')
for side,y in[('Front',-.17),('Back',.17)]:join('WholeBridgeCarriage','WholeLongGuideRail'+side,(0,y,.852))
box('WholeCarriageGripPedestal',(-.055,-.060,.898),(.145,.060,1.100),0,'One whole short carriage pedestal roots the open gripping pair and their upright common pivot.');join('WholeCarriageGripPedestal','WholeBridgeCarriage',(.045,0,.905))
poly=[(.080,-.035),(-.120,-.100),(-.530,-.065),(-.560,-.015),(-.500,-.010),(-.460,-.030),(-.100,-.050),(.050,.020)]
for side,sign in[('Near',1),('Far',-1)]:
 n='WholeOpenGrippingHalf'+side;G[n]=extrude([(x,y*sign)for x,y in poly],1.035,1.090,'z',1,'One full long tapered gripping half, continuous from the supported rear pivot heel to a blunt open front nose. No workpiece, tooth action or clamping force.');join(n,'WholeCarriageGripPedestal',(.050,0,1.065))
cyl('WholeGripperPivotPin',(.065,0,1.015),(.065,0,1.130),.020,2,'One complete fixed upright pin is rooted in the carriage pedestal and both rear gripping heels.',20);join('WholeGripperPivotPin','WholeCarriageGripPedestal',(.065,0,1.060))
box('WholeRearDrawLug',(.100,-.045,.930),(.235,.045,1.025),1,'One full carriage draw lug joins the fixed metal strap to the gripping pedestal, not an independent cable end.');join('WholeRearDrawLug','WholeCarriageGripPedestal',(.125,0,1.000))
# Complete transverse windlass on two finite bearing towers, not three rotating hook axes.
for side,y in[('Front',-.210),('Rear',.210)]:
 n='WholeWindlassBearing'+side;box(n,(.925,y-.045,.842),(1.075,y+.045,.990),0,'One whole bearing tower rises from its own long rail to the transverse windlass axle.')
 join(n,'WholeLongGuideRail'+('Front'if y<0 else'Back'),(1.0,y*.84,.852));join(n,'WholeFullWindlassAxle',(1.0,y,.900))
cyl('WholeFullWindlassAxle',(1.0,-.500,.900),(1.0,.285,.900),.027,1,'One complete fixed transverse axle passes through both windlass bearing towers, the barrel and the outer handwheel hub.',24)
cyl('WholeWindlassBarrel',(1.0,-.160,.900),(1.0,.160,.900),.100,2,'One whole broad windlass barrel carries the fixed draw-strap wrap. No rotation, torque or transmission function.',32);join('WholeWindlassBarrel','WholeFullWindlassAxle',(1.0,0,.900))
for side,y0,y1 in[('Front',-.184,-.151),('Rear',.151,.184)]:
 n='WholeWindlassFlange'+side;cyl(n,(1.0,y0,.900),(1.0,y1,.900),.140,1,'One complete finite barrel flange, with a continuous rooted central web rather than a floating ring.',32);join(n,'WholeWindlassBarrel',(1.0,-.155 if side=='Front'else .155,.950))
# Single continuous flat strap: carriage tail to upper tangent and one fixed quarter wrap.
p=[(.180,1.007),(1.000,1.007)]
p +=[(1+.107*math.cos(a),.900+.107*math.sin(a))for a in[math.pi/2-j*math.pi/24 for j in range(1,13)]]
p +=[(1+.093*math.cos(a),.900+.093*math.sin(a))for a in[j*math.pi/24 for j in range(13)]]
p +=[(.180,.993)]
G['WholeContinuousFixedDrawStrap']=extrude(p,-.014,.014,'y',2,'One whole finite-thickness straight-to-curved flat metal draw-strap appearance links the full carriage rear lug to one windlass quarter wrap. It is not a loose straight wire, three-strand rope or a claimed working chain. No motion or tension.');join('WholeContinuousFixedDrawStrap','WholeRearDrawLug',(.205,0,1.000));join('WholeContinuousFixedDrawStrap','WholeWindlassBarrel',(1+.097/math.sqrt(2),0,.900+.097/math.sqrt(2)))
# Complete outboard open handwheel, all spokes rooted; no meshing gears declared.
C=(1.0,-.410,.900);U=(1,0,0);V=(0,0,1);W=(0,-1,0)
G['WholeOpenWindlassHandwheel']=axial([(.195,-.014),(.235,-.014),(.235,.014),(.195,.014)],C,U,V,W,40,0,'One complete thick open handwheel rim outboard of the front bearing. Not an ornamental disk or an old lathe feed wheel scaled into a new machine.')
cyl('WholeHandwheelHub',(1.0,-.454,.900),(1.0,-.325,.900),.045,1,'One complete wheel hub is rooted on the full windlass axle.',24);join('WholeHandwheelHub','WholeFullWindlassAxle',(1.0,-.390,.900))
for j,a in enumerate([0,math.tau/3,2*math.tau/3]):
 d=add(mul(U,math.cos(a)),mul(V,math.sin(a)));n='WholeWheelSpoke'+str(j);G[n]=beam(add(C,mul(d,.025)),add(C,mul(d,.225)),.027,.025,1,'One full radial spoke joins the complete hub to the actual open wheel rim.');join(n,'WholeHandwheelHub',add(C,mul(d,.035)));join(n,'WholeOpenWindlassHandwheel',add(C,mul(d,.215)))
cyl('WholeOutboardCrankGrip',(1.215,-.525,.900),(1.215,-.402,.900),.023,3,'One full outboard grip is rooted through the rim at the end of a spoke; no operating handle path verified.',20);join('WholeOutboardCrankGrip','WholeOpenWindlassHandwheel',(1.215,-.414,.900))
AIR_POINTS=[(-1.010,0,1.075),(-.780,0,1.075),(-.520,0,1.060),(.50,0,.810),(.55,0,.950),(0,0,.35),(1.05,-.410,.987)]
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='professional-fixed-drawplate-and-windlass-drawing-bench-01';VERSION='1.0.0';TITLE='Fixed Drawplate and Windlass Drawing Bench'
DESCRIPTION='One newly authored complete fixed traditional metalworking drawbench-style exterior. Four complete grounded legs and two crossheads carry long separated guide rails. A full square fixed drawplate has one genuine circular empty through-bore above its entire cross-bed foot. A separate whole bridge carriage supports two long blunt open gripping halves and their common upright pin; a full rear lug joins a single continuous finite flat strap which runs toward and wraps partway around a transverse windlass barrel. Two complete bearing towers support the whole axle, broad barrel, both flanges and an outboard open three-spoke handwheel with a fixed grip. Unlike the old rope-forming bench, there are no three independent hook axes, three-hole separator, forming strands or far capture eye; unlike the old metal lathe there is no chuck, tail quill, cutting tool or cross-feed slide. All geometry is newly authored, not old bench components rearranged. One prop, zero scenes, no wire or workpiece. Four opaque constant untextured PBR materials, metres, Z up, actual horizontally centred bounds and grounded soles. Static illustrative appearance only: no wire reduction, pulling action, clamping, carriage travel, drum rotation, strap tension, gear ratio, material processing, manufacture, operation, load, ergonomic fit or machinery safety guarantee. Rigging, animation and interaction are not made and outside this static asset.'
PALETTE=[('WholeStandRailsAndWheel_DeepGreen',(.075,.19,.16,1),.74,.20),('PlateCarriageAxleAndSpokes_SatinIron',(.44,.48,.47,1),.50,.65),('WholeStrapAndBarrel_DarkSteel',(.10,.12,.12,1),.63,.50),('WholeCrankGrip_DarkWood',(.24,.13,.055,1),.82,0.)]
FOCUS=(0,0,.62);ORTHO=3.00
CAMERAS={'gray-front3q':(-3.8,-6,4.0),'gray-back3q':(3.8,6,4),'thumbnail':(-3.8,-6,4.0),'qa-front':(-3.5,-6,3.7),'qa-side':(6,0,3),'qa-top':(0,0,6),'qa-back':(3.8,6,3.7),'qa-wireframe':(-3.8,-6,4),'silhouette-128-front':(-3.5,-6,3.7),'silhouette-128-side':(6,0,3)}
WIRE_THICKNESS=ORTHO/1800

# BLENDER PHASE: mature export/render only.
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.seed=17
scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
EXPECTED={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False],'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4}
def config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def guard():c=config();assert c==EXPECTED,c;return c
mats=[]
for name,color,rough,metal in PALETTE:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;p.inputs['Alpha'].default_value=1.;p.inputs['Transmission Weight'].default_value=0.;p.inputs['Emission Strength'].default_value=0.;mats.append(m)
bpy.context.preferences.filepaths.save_version=0
root=bpy.data.objects.new('OneWholeFixedDrawplateWindlassBench',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='four grounded sole pads; actual whole bounds centred; fixed traditional drawbench exterior';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();
 for m in mats:me.materials.append(m)
 for i,f in enumerate(me.polygons):f.material_index=g.get('face_materials',[g['material']]*len(me.polygons))[i]
 o['component_role']=g['role'];parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={};actual_triangles={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg);triangles+=len(o.data.loop_triangles)
 component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i]for p in v)for i in range(3)];hi=[max(p[i]for p in v)for i in range(3)];bounds=[round(hi[i]-lo[i],6)for i in range(3)]
assert abs(lo[2])<1e-7 and triangles==1728 and len(parts)==33
def pbr(m):
 p=m.node_tree.nodes.get('Principled BSDF');assert p is not None
 assert not any(n.type.startswith('TEX_') for n in m.node_tree.nodes),'No procedural or image texture nodes permitted'
 assert not any(socket.is_linked for socket in p.inputs),'No linked Principled inputs permitted'
 values=[]
 for name in ['Base Color','Metallic','Roughness','Alpha','IOR','Specular IOR Level','Transmission Weight','Coat Weight','Coat Roughness','Sheen Weight','Emission Color','Emission Strength']:
  value=p.inputs[name].default_value
  values.append((name,tuple(round(float(x),6) for x in value) if hasattr(value,'__len__') else round(float(value),6)))
 values.append(('double_sided',not m.use_backface_culling));return tuple(values)
def records(objects):
 rows=[]
 for o in objects:
  o.data.calc_loop_triangles();vs=[o.matrix_world@v.co for v in o.data.vertices]
  for t in o.data.loop_triangles:
   q=[tuple(round(float(c),6) for c in vs[i]) for i in t.vertices]
   rows.append((min(tuple(q[i:]+q[:i]) for i in range(3)),pbr(o.data.materials[t.material_index])))
 return sorted(rows)
source_records=records(parts);source_fp=hashlib.sha256(json.dumps(source_records,separators=(',',':')).encode()).hexdigest()
mesh_count=len(parts);bpy.ops.object.select_all(action='DESELECT')
for o in parts+[root]:o.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
guard();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'mesh_objects':mesh_count,'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,'components':component_checks,'single_prop_count':1,'review_mode':'SELF_REVIEW','static_visual_only':True,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),'status':'producer geometry; maker actual-image acceptance pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/professional/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'professional','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
 'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len(mats),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
# Every formal/early render is of the actual exported file imported into an emptied scene.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));parts=[o for o in scene.objects if o.type=='MESH']
assert len(parts)==mesh_count and records(parts)==source_records,'Fresh GLB oriented geometry / full solid PBR mismatch'
qa['fresh_actual_glb_guard']={'oriented_geometry_and_full_solid_pbr_match':True,'mesh_count':len(parts)};saveqa()
if '--no-render' in sys.argv or '--geometry-only' in sys.argv:
 metadata();print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)

# BEGIN AUTHORIZED TIERED RENDER V1; native has already been saved at128.
def tier_arg(flag,default=None):
 if flag not in sys.argv:return default
 i=sys.argv.index(flag);assert i+1<len(sys.argv);return sys.argv[i+1]
TIER_PROFILE=tier_arg('--render-profile')
TIER_ALLOWED={'simple-v1':(16,[16,32,64]),'complex-v1':(32,[32,64])}
TIER_SINGLE=tier_arg('--tier-single-view')
TIER_LIST=json.loads(tier_arg('--tier-view-list','[]'))
TIER_OVERRIDES=json.loads(tier_arg('--tier-sample-overrides','{}'))
TIER_STANDARD=['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe']
if TIER_PROFILE:
 assert TIER_PROFILE in TIER_ALLOWED and '--gray-only' not in sys.argv and '--gray-obliques-only' not in sys.argv
 assert isinstance(TIER_OVERRIDES,dict)
 for k,v in TIER_OVERRIDES.items():assert k in CAMERAS and k!='thumbnail' and type(v) is int and v in TIER_ALLOWED[TIER_PROFILE][1]
 assert isinstance(TIER_LIST,list) and len(TIER_LIST)==len(set(TIER_LIST)) and not(TIER_LIST and TIER_SINGLE)
 assert all(n in TIER_STANDARD[1:] and n in CAMERAS for n in TIER_LIST)
 if TIER_SINGLE:assert TIER_SINGLE in CAMERAS and TIER_SINGLE not in ['gray-front3q','gray-back3q','silhouette-128-front','silhouette-128-side']
 qa['tiered_render']={'profile_id':TIER_PROFILE,'authorization_reference':'Sentinel_f2fcc66115e881918d02bc1ea780953c','native_samples':128,'resolution':[640,640],'gray_stage':'omitted_by_authorized_profile','samples_by_image':{}}
def tier_select_views(views):
 if not TIER_PROFILE:return views
 if TIER_SINGLE:return {TIER_SINGLE:CAMERAS[TIER_SINGLE]}
 if TIER_LIST:return {n:CAMERAS[n] for n in TIER_LIST}
 assert set(views)<=set(TIER_STANDARD)
 return views
def tier_before_view(name):
 if not TIER_PROFILE:return
 samples=128 if name=='thumbnail' else TIER_OVERRIDES.get(name,TIER_ALLOWED[TIER_PROFILE][0])
 assert samples==128 if name=='thumbnail' else samples in TIER_ALLOWED[TIER_PROFILE][1]
 scene.cycles.samples=samples
 EXPECTED['samples']=samples
 qa['tiered_render']['samples_by_image'][name+'.png']=samples
# END AUTHORIZED TIERED RENDER V1
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.30,.30,.30,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8;scene.view_settings.view_transform='AgX'
focus=Vector(FOCUS);asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),600,4),('Fill',(4,-2,4),360,3.5),('Rim',(2,4,5),480,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
def diagnostic_snapshot():
 return {m:[(i,socket.identifier,socket.bl_idname,tuple(socket.default_value) if hasattr(socket.default_value,'__len__') else socket.default_value) for i,socket in enumerate(m.node_tree.nodes.get('Principled BSDF').inputs) if hasattr(socket,'default_value')] for m in asset_mats}
original_material_inputs=diagnostic_snapshot()
original_slots={o:(list(o.data.materials),[f.material_index for f in o.data.polygons]) for o in parts}
def restore_diagnostic_materials():
 for m,inputs in original_material_inputs.items():
  p=m.node_tree.nodes.get('Principled BSDF')
  for index,identifier,socket_type,value in inputs:
   assert index<len(p.inputs),'Diagnostic socket index disappeared'
   socket=p.inputs[index]
   assert socket.identifier==identifier and socket.bl_idname==socket_type,'Diagnostic socket identity/type changed'
   socket.default_value=value
 for o,(slots,indices) in original_slots.items():
  assert len(o.data.polygons)==len(indices),'Diagnostic face count changed'
  o.data.materials.clear()
  for m in slots:o.data.materials.append(m)
  for f,index in zip(o.data.polygons,indices):f.material_index=index
  assert list(o.data.materials)==slots and [f.material_index for f in o.data.polygons]==indices
 assert diagnostic_snapshot()==original_material_inputs,'Diagnostic full socket-index/identifier/type/value restoration differs'
 assert records(parts)==source_records,'Diagnostic restoration changed complete oriented geometry/full solid PBR signature'
 qa['diagnostic_exact_restoration']={'try_finally':True,'full_socket_index_identifier_type_value_match':True,'all_material_slots_and_face_indices_match':True,'full_oriented_geometry_and_pbr_records_match':True}
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
try:
 if gray:
  for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
 views={k:CAMERAS[k] for k in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
 if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
 if '--extra-views' in sys.argv:views.pop('thumbnail',None)
 views=tier_select_views(views)
 seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
 def render(name,pos):
  tier_before_view(name)
  cam.data.ortho_scale=ORTHO
  aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
 for name,pos in views.items():
  if name=='qa-wireframe':
   wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
   for o in parts:
    dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
    for f in dup.data.polygons:f.material_index=0
    w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=WIRE_THICKNESS;w.use_replace=True;w.use_even_offset=False;w.offset=1
  render(name,pos)
 if gray and '--gray-obliques-only' not in sys.argv:
  black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
  for o in parts:
   o.data.materials.clear();o.data.materials.append(black)
   for f in o.data.polygons:f.material_index=0
  ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
  scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
  for name,pos in [(name,CAMERAS[name]) for name in ['silhouette-128-front','silhouette-128-side']]:render(name,pos)
finally:
 restore_diagnostic_materials()
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; maker necessary-view self-review pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
