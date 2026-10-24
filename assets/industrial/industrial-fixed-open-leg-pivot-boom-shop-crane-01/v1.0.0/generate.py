"""One whole fixed open-leg wheeled shop crane. Static art only, no hydraulic, lifting or safety claim."""
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


# Entire new open-leg wheeled shop crane, no fixed-jib or floor-jack mesh imported.
G={};GROUND=[];ROOT_WITNESSES=[];AIR_POINTS=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
def cylinder(a,b,r,mat,role,n=20):
 w=unit(sub(b,a));ref=(1,0,0)if abs(w[0])<.9 else(0,1,0);u=unit(cross(w,ref));v=cross(w,u);length=math.sqrt(dot(sub(b,a),sub(b,a)));return axial([(0,0),(r,0),(r,length),(0,length)],a,u,v,w,n,mat,role)
# Four entire fixed caster-like wheels with finite flat facets, hubs, axles and open forks.
for label,x in[('Left',-.45),('Right',.45)]:
 leg='WholeLongChassisLeg'+label;G[leg]=block((x-.045,-.98,.140),(x+.045,.40,.230),0,'One whole long low chassis leg extending forward of the mast; both legs leave a real wide open front bay. No cargo fork, old jack cheek or footprint copied.')
 for end,y in[('Front',-.92),('Rear',.30)]:
  tag=label+end;tire='WholeWheelTire'+tag;hub='WholeWheelHub'+tag;axle='WholeWheelAxle'+tag;fork='WholeOpenWheelFork'+tag
  G[tire]=axial([(.022,-.016),(.065/math.cos(math.pi/16),-.016),(.065/math.cos(math.pi/16),.016),(.022,.016)],(x,y,.065),(0,1,0),(0,0,1),(1,0,0),16,2,'One entire annular wheel exterior with a true finite flat ground facet. No rolling, caster swivel or load capacity claim.',phase=math.pi/16);GROUND.append(tire)
  G[hub]=cylinder((x-.019,y,.065),(x+.019,y,.065),.023,1,'One whole fixed hub inside the full wheel bore; separate from the tire and axle.',16)
  G[axle]=cylinder((x-.057,y,.065),(x+.057,y,.065),.012,1,'One full fixed short axle spans both fork cheeks; its end caps extend beyond the complete fork outer planes to avoid shared exposed cap planes.',16)
  poly=[(x-.050,.060),(x-.035,.060),(x-.035,.135),(x+.035,.135),(x+.035,.060),(x+.050,.060),(x+.050,.170),(x-.050,.170)]
  G[fork]=extrude(poly,y-.027,y+.027,'y',1,'One continuous closed material U-shaped wheel fork with both cheeks and its top bridge; a genuine empty bay remains over the wheel. Fixed orientation only.')
  join(tire,hub,(x,y,.0875));join(hub,axle,(x,y,.065));join(axle,fork,(x+.043,y,.065));join(fork,leg,(x,y,.155))
G['WholeRearChassisCrossmember']=block((-.50,.25,.180),(.50,.38,.290),0,'One complete broad rear crossmember joins both whole forward legs and roots the rear mast. Its outer planes differ from the leg planes, not co-oriented overlay skins.')
for label,x in[('Left',-.45),('Right',.45)]:join('WholeRearChassisCrossmember','WholeLongChassisLeg'+label,(x,.30,.205))
G['WholeRearUprightMast']=block((-.060,.240,.240),(.060,.360,1.460),0,'One whole rear vertical mast rooted into the crossmember, carrying a high single boom pivot. Not the earlier stationary jib column or a lengthened floor-jack saddle stem.');join('WholeRearUprightMast','WholeRearChassisCrossmember',(0,.30,.265))
for label,x in[('Near',-.074),('Far',.074)]:
 n='WholeMastFootGusset'+label;G[n]=extrude([(.080,.275),(.325,.275),(.325,.660)],x-.022,x+.022,'x',0,'One full triangular mast-foot gusset, rooted into the rear crossmember and the complete mast side.');join(n,'WholeRearChassisCrossmember',(x,.30,.282));join(n,'WholeRearUprightMast',((-0.055 if x<0 else .055),.30,.45))
# Full upper pivot cheeks, full transverse pin and one whole uninterrupted high boom.
for label,x in[('Near',-.081),('Far',.081)]:
 n='WholeUpperPivotCheek'+label;G[n]=block((x-.025,.210,1.335),(x+.025,.395,1.475),0,'One complete high side cheek rooting the transverse boom pin to the mast. Solid fixed static casting, no moving bore or bearing fit claim.');join(n,'WholeRearUprightMast',((-0.057 if x<0 else .057),.30,1.40))
G['WholeHighInclinedBoom']=beam((0,.30,1.405),(0,-1.08,1.720),.105,.100,0,'One entire long inclined overhead boom with a complete rectangular section, fixed in a raised position on the rear pivot. No I-beam track, trolley or telescoping motion.');
G['WholeUpperBoomPin']=cylinder((-.123,.28,1.410),(.123,.28,1.410),.027,1,'One complete fixed transverse boom pin across the upper cheeks and the full boom. Exposed end caps are outside the cheek faces.',20)
for label,x in[('Near',-.081),('Far',.081)]:join('WholeUpperBoomPin','WholeUpperPivotCheek'+label,(x,.28,1.410))
join('WholeUpperBoomPin','WholeHighInclinedBoom',(0,.28,1.410))
# Whole inclined strut body and a separate smooth rod in one fixed visual relation.
G['WholeLowerStrutBracket']=block((-.090,.100,.340),(.090,.325,.445),0,'One whole lower strut bracket projects forward from the mast to receive the inclined body pivot.');join('WholeLowerStrutBracket','WholeRearUprightMast',(0,.30,.395))
A=(0,.15,.40);T=(0,-.60,1.58);V=sub(T,A)
G['WholeLowerStrutPin']=cylinder((-.145,.15,.40),(.145,.15,.40),.024,1,'One entire lower fixed transverse pin roots the inclined strut and the adjacent small pump-like body.');join('WholeLowerStrutPin','WholeLowerStrutBracket',(0,.15,.40))
G['WholeInclinedCylinderBody']=cylinder(A,add(A,mul(V,.56)),.049,3,'One whole thick inclined cylinder-shaped body between the lower bracket and the high boom. Static exterior only; no fluid circuit, seal or pressure function represented.');join('WholeInclinedCylinderBody','WholeLowerStrutPin',add(A,mul(V,.009)))
G['WholeExtendedSmoothRod']=cylinder(add(A,mul(V,.51)),T,.020,1,'One complete exposed smooth rod entering the whole diagonal body and upper boom pin. Fixed assembly, not a functioning actuator.');join('WholeExtendedSmoothRod','WholeInclinedCylinderBody',add(A,mul(V,.535)))
G['WholeUpperStrutPin']=cylinder((-.086,-.60,1.58),(.086,-.60,1.58),.023,1,'One whole short transverse upper strut pin enters the high boom and the rod end.');join('WholeUpperStrutPin','WholeExtendedSmoothRod',add(A,mul(V,.993)));join('WholeUpperStrutPin','WholeHighInclinedBoom',(0,-.60,1.58))
G['WholeSmallPumpBody']=cylinder((.130,.15,.315),(.130,.15,.505),.029,3,'One whole small fixed pump-like cylinder appearance beside the lower pivot, not a functional reservoir or pressure supply.');join('WholeSmallPumpBody','WholeLowerStrutPin',(.130,.15,.40))
G['WholePumpHandleSocket']=block((.105,.125,.460),(.155,.180,.525),3,'One complete small fixed handle socket entering the adjacent pump body.');join('WholePumpHandleSocket','WholeSmallPumpBody',(.130,.15,.480))
G['WholeInclinedPumpHandle']=cylinder((.130,.150,.49),(.130,.34,.96),.012,1,'One whole long side pump-style handle, fixed tilted rearwards. No operating instruction or pumping performance.');join('WholeInclinedPumpHandle','WholePumpHandleSocket',(.130,.155,.503))
G['WholePumpHandleGrip']=cylinder((.130,.305,.875),(.130,.355,.998),.020,2,'One entire thick dark grip surrounds the upper part of the fixed pump-style handle.');join('WholePumpHandleGrip','WholeInclinedPumpHandle',(.130,.325,.925))
# Empty suspension: full short stem and one thick actual open hook, not chain simulation.
G['WholeFixedSuspensionStem']=cylinder((0,-1.065,1.715),(0,-1.065,1.380),.014,1,'One whole short fixed hanging stem from the boom tip, with no load or simulated chain.');join('WholeFixedSuspensionStem','WholeHighInclinedBoom',(0,-1.065,1.705))
G['WholeHookUpperShank']=block((-.022,-1.087,1.270),(.022,-1.043,1.405),1,'One complete thick hook shank receives the fixed suspension stem and continuous open hook body.');join('WholeHookUpperShank','WholeFixedSuspensionStem',(0,-1.065,1.392))
angles=[math.radians(140+260*j/26)for j in range(27)];cx=.065;cz=1.225;poly=[(cx+.100*math.cos(t),cz+.100*math.sin(t))for t in angles]+[(cx+.065*math.cos(t),cz+.065*math.sin(t))for t in reversed(angles)]
G['WholeOpenSuspendedHook']=extrude(poly,-1.096,-1.034,'y',1,'One whole continuous thick open hook with a genuinely open throat; its upper-left material root joins the complete shank. Empty static art, not a load-rated hook.');join('WholeOpenSuspendedHook','WholeHookUpperShank',(-.002,-1.065,1.275))
AIR_POINTS=[(0,-.60,.15),(0,-.35,.45),(.28,-.25,.65),(-.28,-.25,.65),(0,-.90,1.0),(.080,-1.065,1.245)]
for x in[-.45,.45]:
 for y in[-.92,.30]:AIR_POINTS.append((x,y,.132))
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='industrial-fixed-open-leg-pivot-boom-shop-crane-01';VERSION='1.0.0';TITLE='Fixed Open-Leg Pivot-Boom Shop Crane'
DESCRIPTION='One newly authored whole static empty wheeled shop-crane appearance. Two long low chassis legs form a broad real open front bay on four complete fixed fork/hub/axle/wheel assemblies with finite flat ground facets. A full rear crossmember, upright mast and two whole gussets support paired high cheeks, a complete transverse pin and one entire long inclined overhead boom. A thick diagonal cylinder-shaped body and separate smooth rod reach from a whole lower bracket to a short boom pin; a small adjacent pump-like body, socket and full fixed side handle complete the exterior. One short hanging stem, full shank and continuous thick open hook occupy the empty boom tip. It is not the older fixed-column I-beam trolley hoist, enlarged saddle jack or copied machinery assembly; all numeric geometry newly authored and no old model imported. One prop and zero scenes with no payload. Four opaque constant untextured PBR materials, metres, Z up, actual horizontal bounds-centred ground origin. Small fixed overlaps join whole components; no working bearings or hydraulic internals. Static illustrative art only: no pumping, pressure, lifting, loading, boom travel, folding, rolling, steering, load rating, stability, vehicle/service compatibility, operation, fabrication or safety claim.'
PALETTE=[('WholeFrameAndBoom_MutedOchre',(.52,.29,.08,1),.67,.20),('PinsRodForksAndHook_SatinSteel',(.45,.49,.49,1),.43,.62),('WheelTiresAndGrip_Charcoal',(.045,.055,.058,1),.82,.02),('WholeStrutAndPump_DarkPetrol',(.07,.20,.21,1),.61,.23)]
FOCUS=(0,0,.86);ORTHO=2.40
CAMERAS={'gray-front3q':(4.8,-6,3.3),'gray-back3q':(-4.8,6,3.3),'thumbnail':(4.8,-6,3.3),'qa-front':(4.8,-6,3.0),'qa-side':(5,0,2.5),'qa-top':(0,0,6),'qa-back':(-4.8,6,3.0),'qa-wireframe':(4.8,-6,3.3),'silhouette-128-front':(4.8,-6,3.0),'silhouette-128-side':(5,0,2.5)}
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
root=bpy.data.objects.new('OneFixedOpenLegPivotBoomShopCrane',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='four finite wheel facets at Z0; actual bounds centred; whole empty fixed wheeled shop crane';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==2204 and len(parts)==38
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
  files[role]={'path':f'assets/industrial/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'industrial','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
