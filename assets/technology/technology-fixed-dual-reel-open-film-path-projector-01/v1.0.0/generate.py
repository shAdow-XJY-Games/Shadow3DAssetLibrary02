"""Original complete fixed dual-reel film projector exterior. Static art; no optical, film transport or safety claim."""
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


# Complete newly authored film-projector appearance; no old model data loaded.
G={};GROUND=[];ROOT_WITNESSES=[];AIR_POINTS=[]
def box(name,lo,hi,mat,role):G[name]=block(lo,hi,mat,role)
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
def cylinder(name,a,b,r,mat,role,n=16):
 w=unit(sub(b,a));ref=(0,0,1)if abs(w[2])<.9 else(0,1,0);u=unit(cross(w,ref));v=cross(w,u);length=math.sqrt(dot(sub(b,a),sub(b,a)))
 G[name]=axial([(0,0),(r,0),(r,length),(0,length)],a,u,v,w,n,mat,role)
for k,y in enumerate([-.137,.137]):
 name='WholeFiniteGroundShoe'+str(k);box(name,(-.345,y-.022,0),(.315,y+.022,.041),2,'One entire long flat underside shoe of this complete projector, not a stand counted separately.');GROUND.append(name);join(name,'WholeLowProjectorBase',(.05,y,.035))
base=[(-.355,-.166),(.325,-.166),(.35,-.14),(.35,.14),(.325,.166),(-.355,.166),(-.38,.14),(-.38,-.14)]
G['WholeLowProjectorBase']=extrude(base,.031,.081,'z',0,'One whole chamfered low base carrying the complete side-case and separate reel arms. Not an old cable-reel carry stand.')
case=[(-.045,.073),(.30,.073),(.30,.452),(.262,.492),(.016,.492),(-.045,.434)]
G['WholeProjectorMachineCase']=extrude(case,-.060,.12,'y',0,'One complete high bevel-topped projector machine-case exterior. It is a closed visual shell/solid exterior, not a claimed inner lamp or transmission chamber.');join('WholeProjectorMachineCase','WholeLowProjectorBase',(.12,0,.077))
REELS={}
for label,cx,cz,ro,windr,start in [('UpperFeed',-.220,.680,.180,.105,(-.025,.024,.432)),('LowerTakeup',-.235,.245,.155,.060,(-.025,.024,.135))]:
 arm='WholeReelSupportArm'+label;end=(cx,.024,cz);G[arm]=beam(start,end,.055,.045,0,'One complete inclined fixed reel arm reaches from the body to its own reel axis. Upper/lower topology is original, not duplicated old reels.');join(arm,'WholeProjectorMachineCase',add(start,mul(sub(end,start),.025)))
 shaft='WholeReelAxle'+label;cylinder(shaft,(cx,.047,cz),(cx,-.188,cz),.018,1,'One full supported horizontal reel axle crosses the arm and complete reel hub.',16);join(shaft,arm,add(end,mul(sub(start,end),.02)))
 hub='WholeReelHub'+label;cylinder(hub,(cx,-.166,cz),(cx,-.080,cz),.036,1,'One complete reel hub joins the two open flanges and fixed axle.',16);join(hub,shaft,(cx,-.125,cz))
 for face,y in [('Front',-.158),('Rear',-.088)]:
  rim='WholeOpenReelRim'+label+face;G[rim]=axial([(ro-.027,y-.005),(ro,y-.005),(ro,y+.005),(ro-.027,y+.005)],(cx,0,cz),(1,0,0),(0,0,1),(0,1,0),24,1,'One full thick open annular reel flange rim; large between-spoke windows remain real geometry.')
  for k in range(6):
   a=math.tau*k/6;d=(math.cos(a),0,math.sin(a));p0=add((cx,y,cz),mul(d,.027));p1=add((cx,y,cz),mul(d,ro-.006));name='WholeReelSpoke'+label+face+str(k)
   G[name]=beam(p0,p1,.014,.014,1,'One entire radial flange spoke, with full hub and rim roots. Six-spoke stylization, no rotation or reel capacity claim.');join(name,hub,add((cx,y,cz),mul(d,.032)));join(name,rim,add((cx,y,cz),mul(d,ro-.015)))
 wind='WholeStoredFilmMass'+label;G[wind]=axial([(.032,-.150),(windr,-.150),(windr,-.098),(.032,-.098)],(cx,0,cz),(1,0,0),(0,0,1),(0,1,0),32,2,'One annular stored-film exterior volume, not separately resolved windings. The continuous exposed ribbon has a small fixed root in this mass.');join(wind,hub,(cx+.034,-.125,cz))
 cap='WholeReelRetentionCap'+label;cylinder(cap,(cx,-.194,cz),(cx,-.174,cz),.025,3,'One complete small fixed retaining cap at the outboard end of the reel axle.',12);join(cap,shaft,(cx,-.180,cz))
 REELS[label]=(cx,cz,ro,windr)
# One genuine connected flat thick ribbon with rectangular cross sections.
# It is NOT an axial cable tube, separate strips or a complete winding simulation.
def cubic(a,b,c,d,steps):return[tuple((1-t)**3*a[j]+3*(1-t)**2*t*b[j]+3*(1-t)*t*t*c[j]+t**3*d[j]for j in range(2))for t in[i/steps for i in range(1,steps+1)]]
a=(-.220+.098*math.cos(-math.pi/5),.680+.098*math.sin(-math.pi/5));end=(-.235+.056*math.cos(math.pi/5),.245+.056*math.sin(math.pi/5));PATH=[a]
PATH+=cubic(a,(-.100,.574),(.015,.550),(.080,.550),16)
PATH+=cubic(PATH[-1],(.150,.550),(.225,.500),(.225,.440),16)
PATH +=[(.225,.440-i*.145/8)for i in range(1,9)]
PATH+=cubic(PATH[-1],(.225,.240),(.170,.205),(.100,.205),16)
PATH+=cubic(PATH[-1],(.020,.205),(-.130,.245),end,16)
def ribbon(path,width,thickness):
 m=Mesh();rows=[]
 for i,(x,z)in enumerate(path):
  aa=path[max(0,i-1)];bb=path[min(len(path)-1,i+1)];tx,tz=bb[0]-aa[0],bb[1]-aa[1];length=math.hypot(tx,tz);nx,nz=-tz/length,tx/length
  rows.append([(x+nx*h,-.125+w,z+nz*h)for w,h in[(-width/2,-thickness/2),(width/2,-thickness/2),(width/2,thickness/2),(-width/2,thickness/2)]])
 for row in[rows[0],rows[-1]]:m.quad(*row,3)
 for a,b in zip(rows,rows[1:]):
  for j in range(4):k=(j+1)%4;m.quad(a[j],a[k],b[k],b[j],3)
 return m.result('One entire continuous thin flat exposed film-like ribbon, rooted at both stored-film masses and following two broad curved feed loops and one straight gate segment. Real sides and finite thickness; no photographs, perforation mechanism or operational feed claim.')
G['WholeContinuousExposedFilmRibbon']=ribbon(PATH,.030,.0032)
for label,k,j in [('UpperFeed',0,1),('LowerTakeup',-1,-2)]:
 p=tuple(PATH[k][i]+.01*(PATH[j][i]-PATH[k][i])for i in range(2));join('WholeContinuousExposedFilmRibbon','WholeStoredFilmMass'+label,(p[0],-.125,p[1]))
# Fixed guide wheels have full stubs back to the case and actual exposed round rims.
for label,x,z in [('Upper',.080,.525),('Lower',.100,.230)]:
 stub='WholeGuideStub'+label;cylinder(stub,(x,-.038,z),(x,-.140,z),.009,1,'One complete horizontal guide-wheel stub, rooted into its supporting bracket.',12)
 bracket='WholeGuideBracket'+label;box(bracket,(x-.017,-.072,z-.068),(x+.017,-.037,z+.012),0,'One whole guide-wheel bracket runs back into the full machine case, including the raised upper guide.');join(bracket,'WholeProjectorMachineCase',(x,-.050,z-.045));join(stub,bracket,(x,-.050,z))
 wheel='WholeFilmGuideWheel'+label;cylinder(wheel,(x,-.144,z),(x,-.106,z),.025,1,'One complete small fixed film guide wheel near a broad ribbon-loop extremum. No tension, track or rolling performance.',20);join(wheel,stub,(x,-.125,z))
# Paired narrow fixed gate cheeks leave a real slot around the vertical ribbon.
for label,x in [('Left',.213),('Right',.237)]:
 n='WholeFixedGateCheek'+label;box(n,(x-.004,-.148,.300),(x+.004,-.052,.440),1,'One full narrow gate cheek, rooted directly into the machine face and separated from its opposite around the ribbon.');join(n,'WholeProjectorMachineCase',(x,-.056,.365))
# Front horizontal annular lens body, intentionally backed by a recessed opaque optic.
G['WholeHorizontalLensHousing']=axial([(.035,.285),(.055,.285),(.055,.405),(.048,.432),(.035,.432)],(0,.025,.350),(0,1,0),(0,0,1),(1,0,0),24,0,'One complete thick horizontal lens-barrel housing with a real front recess. It is not a demonstrated through optical path.');join('WholeHorizontalLensHousing','WholeProjectorMachineCase',(.292,.070,.350))
cylinder('WholeRecessedOpaqueOptic',(.395,.025,.350),(.403,.025,.350),.036,2,'One full opaque recessed circular optic visual; no transparency, projection or physical lens simulation.',24);join('WholeRecessedOpaqueOptic','WholeHorizontalLensHousing',(.399,.0605,.350))
handle=[(.045,.465),(.075,.465),(.075,.545),(.215,.545),(.215,.465),(.245,.465),(.245,.575),(.045,.575)]
G['WholeOpenCarryHandle']=extrude(handle,.005,.052,'y',2,'One complete raised carry-handle with a real central open aperture, fixed by its two full lower legs to the case. No carrying strength or ergonomic claim.')
for x in[.060,.230]:join('WholeOpenCarryHandle','WholeProjectorMachineCase',(x,.025,.478))
cylinder('WholeFixedFrontControl',(.145,-.040,.135),(.145,-.096,.135),.026,3,'One subordinate fixed front control appearance rooted in the case; no switch or electrical function.',16);join('WholeFixedFrontControl','WholeProjectorMachineCase',(.145,-.052,.135))
AIR_POINTS=[(.145,.025,.525),(.225,-.125,.365),(.220,-.125,.365),(.230,-.125,.365),(.420,.025,.350),(-.06,-.125,.40)]
# The ribbon itself occupies the gate centre, therefore only left/right clear strips are empty tests.
AIR_POINTS.remove((.225,-.125,.365))
for label,(cx,cz,ro,windr)in REELS.items():
 a=math.pi/6;r=(max(windr,ro-.027)+windr)/2
 # Outboard annular wedge between stored mass and flange rim, avoiding spokes.
 r=(windr+ro-.027)/2;AIR_POINTS.append((cx+r*math.cos(a),-.125,cz+r*math.sin(a)));AIR_POINTS.append((cx+r*math.cos(a),-.158,cz+r*math.sin(a)))
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='technology-fixed-dual-reel-open-film-path-projector-01';VERSION='1.0.0';TITLE='Fixed Dual Reel Open Film Path Projector'
DESCRIPTION='One newly authored complete static film-projector-style device. A low chamfered base on two long finite shoes carries a high machine-case exterior, two independent inclined reel arms and separate upper feed and lower take-up axes. Both whole reels have open-spoke front and rear flanges, supported hubs and retaining caps, with shallow annular stored-film exterior masses. One genuine connected thick flat exposed ribbon runs from the upper mass through a broad guide loop, a straight slot between two rooted gate cheeks and a lower guide loop into the lower mass. A horizontal thick annular lens housing contains a visibly recessed opaque optic; a full open carry handle and fixed front control complete the machine. All numerical geometry new, no old overhead projector, camera, cable reel, hose winding or component instances imported. One complete prop, zero scenes. Four opaque constant PBR materials, metres, Z up and actual horizontal-bounds-centred bottom-shoe origin. Stored-film masses are exterior annuli, not resolved continuous windings; only the exposed ribbon is a single continuous piece. Deliberately stylized fixed relationships and small assembly overlaps, no sprocket holes or actual film frames. No rotation, transport, tension, sprocket engagement, focus, exposure, optical imaging, illumination, projection, electric drive, heat management, historical reproduction, manufacture, compatibility, ergonomics, load or machinery safety claim.'
PALETTE=[('WholeCaseAndArms_MutedBlueGrey',(.22,.32,.34,1),.68,.15),('ReelFlangesAndGuides_SatinMetal',(.52,.54,.50,1),.44,.60),('FilmMassFeetAndOptic_Graphite',(.045,.055,.050,1),.80,.05),('ExposedRibbonAndControls_WarmBrown',(.34,.20,.09,1),.72,.08)]
FOCUS=(0,0,.420);ORTHO=1.14
CAMERAS={'gray-front3q':(3.8,-6,3.2),'gray-back3q':(-3.8,6,3.2),'thumbnail':(3.8,-6,3.2),'qa-front':(3.8,-6,2.9),'qa-side':(6,0,2.7),'qa-top':(0,0,6),'qa-back':(-3.8,6,2.9),'qa-wireframe':(3.8,-6,3.2),'silhouette-128-front':(3.8,-6,2.9),'silhouette-128-side':(6,0,2.7)}
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
root=bpy.data.objects.new('OneFixedDualReelOpenFilmPathProjector',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='two finite whole shoes at Z0; actual bounds centred; whole fixed dual-reel projector';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==3328 and len(parts)==55
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
  files[role]={'path':f'assets/technology/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'technology','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
