"""One complete fixed rotary duplicator exterior. No printing, motion or machinery safety claims."""
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



# One entire newly authored fixed hand-crank rotary duplicator exterior.
G={};GROUND=[];ROOT_WITNESSES=[];AIR_POINTS=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
def cylinder(a,b,r,mat,role,n=24):
 w=unit(sub(b,a));ref=(0,0,1)if abs(w[2])<.9 else(0,1,0);u=unit(cross(w,ref));v=cross(w,u);ll=math.sqrt(dot(sub(b,a),sub(b,a)))
 return axial([(0,0),(r,0),(r,ll),(0,ll)],a,u,v,w,n,mat,role)
def sideframe(x):
 outer=[(-.250,.035),(.250,.035),(.250,.345),(.205,.440),(.130,.490),(-.130,.490),(-.205,.440),(-.250,.345)]
 inner=[(-.175,.105),(.175,.105),(.175,.230),(.145,.285),(.095,.310),(-.095,.310),(-.145,.285),(-.175,.230)]
 m=Mesh();loops=[[(xx,y,z)for y,z in p]for xx,p in[(x-.018,outer),(x+.018,outer),(x-.018,inner),(x+.018,inner)]]
 for i in range(8):
  j=(i+1)%8
  for a,b,c,d in[(loops[0][i],loops[0][j],loops[1][j],loops[1][i]),(loops[2][i],loops[3][i],loops[3][j],loops[2][j]),(loops[0][i],loops[2][i],loops[2][j],loops[0][j]),(loops[1][i],loops[1][j],loops[3][j],loops[3][i])]:m.quad(a,b,c,d,0)
 return m.result('One complete thick arched side casting with a genuine broad lower through-window, whole bottom rail and solid upper bearing bridge. Not a note-counter opaque casing or the rear-rising side of an open-platen press.')
for lab,x in[('Left',-.245),('Right',.245)]:
 foot='WholeLongGroundShoe'+lab;G[foot]=block((x-.045,-.300,0),(x+.045,.300,.050),0,'One full long grounded shoe carries the entire corresponding windowed side casting.');GROUND.append(foot)
 n='WholeWindowedSideCasting'+lab;G[n]=sideframe(x);join(n,foot,(x,0,.043))
G['WholeRearLowerCrossTie']=block((-.258,.205,.080),(.258,.245,.135),0,'One whole rear cross-tie joins both complete side castings; no worktable or imported machine support.')
for lab,x in[('Left',-.245),('Right',.245)]:join('WholeRearLowerCrossTie','WholeWindowedSideCasting'+lab,(x,.225,.115))
G['WholeMainDrumCrossAxle']=cylinder((-.289,0,.385),(.335,0,.385),.025,1,'One entire horizontal main axle passes through both upper bearing bridges and the whole large drum.',24)
for lab,x in[('Left',-.245),('Right',.245)]:join('WholeMainDrumCrossAxle','WholeWindowedSideCasting'+lab,(x,0,.385))
# A single complete drum with closed beveled end caps; no separate repeated print cylinders.
G['WholeBroadPlainRotaryDrum']=axial([(0,-.215),(.143,-.215),(.155,-.205),(.155,.205),(.143,.215),(0,.215)],(0,0,.385),(0,1,0),(0,0,1),(1,0,0),48,[2,1,3,1,2,2],'One whole broad closed transverse drum dominates the open machine. Its blank slightly bevelled cylindrical skin and complete dark end faces are real solid faces, not a paper texture, a narrow feed roller or a flattened platen. No stencil perforations, printed matter, ink or cylinder rotation.');join('WholeBroadPlainRotaryDrum','WholeMainDrumCrossAxle',(0,0,.385))
G['WholeRaisedLongDrumClampStrip']=beam((-.207,-.080,.515),(.207,-.080,.515),.024,.016,1,'One entire narrow raised longitudinal strip is rooted in the upper-front drum skin, visually suggesting a fixed sheet-retaining seam. It is not a working clamp or a separate wrapped paper sheet.');join('WholeRaisedLongDrumClampStrip','WholeBroadPlainRotaryDrum',(0,-.080,.512))
# The complete lower pressure-roller appearance has its own whole supporting brackets and through shaft.
for lab,x in[('Left',-.245),('Right',.245)]:
 n='WholeLowerRollerBearingBracket'+lab;G[n]=block((x-.021,-.223,.166),(x+.021,-.105,.214),1,'One full bearing bracket extends from the front solid side of the windowed casting to the lower roller axle, rather than allowing the axle to float within an open window.');join(n,'WholeWindowedSideCasting'+lab,(x,-.202,.190))
G['WholeLowerRollerAxle']=cylinder((-.269,-.130,.190),(.269,-.130,.190),.012,1,'One whole lower transverse axle enters both supported lower bearing brackets.',20)
for lab,x in[('Left',-.245),('Right',.245)]:join('WholeLowerRollerAxle','WholeLowerRollerBearingBracket'+lab,(x,-.130,.190))
G['WholeLowerPlainPressureRoller']=cylinder((-.213,-.130,.190),(.213,-.130,.190),.033,2,'One whole lower dark pressure-roller appearance surrounds its own complete axle. A deliberate static air interval separates it from the large drum, with no gripping, feeding, deformation or printing nip claimed.',32);join('WholeLowerPlainPressureRoller','WholeLowerRollerAxle',(0,-.130,.190))
# Complete rear feed table slopes toward the upper rear drum and is supported at its near end by both upper bridges.
G['WholeRearInclinedFeedTable']=extrude([(.205,.395),(.545,.475),(.545,.497),(.205,.417)],-.258,.258,'x',3,'One entire thick empty rear feed table slopes up away from the drum and enters both solid upper side bridges at its near edge. The whole open rear tray is part of this machine, not a loose sheet or copied note-counter hopper.')
for lab,x in[('Left',-.245),('Right',.245)]:join('WholeRearInclinedFeedTable','WholeWindowedSideCasting'+lab,(x,.210,.409))
for lab,x in[('Left',-.218),('Right',.218)]:
 n='WholeRearFeedSideGuide'+lab;G[n]=extrude([(.275,.423),(.535,.484),(.535,.525),(.275,.464)],x-.009,x+.009,'x',0,'One whole finite longitudinal feed-table side guide follows the complete sloping rear table. Empty between the two guides.');join(n,'WholeRearInclinedFeedTable',(x,.380,.455))
# Entire U-section low receiving pan, open at the rear toward the drum, including finite front stop.
m=Mesh();section=[(-.229,.065),(.229,.065),(.229,.130),(.211,.130),(.211,.081),(-.211,.081),(-.211,.130),(-.229,.130)]
G['WholeLowFrontUReceivingPan']=extrude(section,-.550,-.175,'y',3,'One entire thick U-section low front receiving pan has a real floor and both full side lips. Its rear rim enters the two side castings near their front shoes; the empty pan is not an output paper stack.')
for lab,x in[('Left',-.228),('Right',.228)]:join('WholeLowFrontUReceivingPan','WholeWindowedSideCasting'+lab,(x,-.215,.091))
G['WholePanFrontStop']=block((-.225,-.554,.072),(.225,-.535,.119),0,'One complete front stop joins the entire receiving pan at its floor and lips. No generated printed sheets.');join('WholePanFrontStop','WholeLowFrontUReceivingPan',(0,-.543,.077))
# Outboard whole crank makes the rotary drum machine distinct from a lever-operated flat press.
G['WholeOutboardCrankHub']=cylinder((.300,0,.385),(.373,0,.385),.047,1,'One complete outboard hand-crank hub overlaps the real main axle end.',24);join('WholeOutboardCrankHub','WholeMainDrumCrossAxle',(.321,0,.385))
G['WholeFixedCrankArm']=beam((.349,0,.385),(.349,-.148,.280),.028,.028,1,'One whole fixed radial crank arm descends in front of the right side casting with a clear outboard gap. No crank rotation, gearing or drive performance.');join('WholeFixedCrankArm','WholeOutboardCrankHub',(.349,-.012,.376))
G['WholeCrankGripStub']=cylinder((.338,-.148,.280),(.412,-.148,.280),.012,1,'One entire axial stub passes through the far crank arm end and carries the complete separate wooden grip.',20);join('WholeCrankGripStub','WholeFixedCrankArm',(.349,-.148,.280))
G['WholeLongWoodCrankGrip']=axial([(0,.387),(.022,.387),(.027,.404),(.027,.475),(.020,.488),(0,.488)],(0,-.148,.280),(0,1,0),(0,0,1),(1,0,0),24,3,'One complete finite rounded wooden crank grip around the outer stub, with a proud end outside the side frame. No ergonomics or operability claim.');join('WholeLongWoodCrankGrip','WholeCrankGripStub',(.400,-.148,.280))
AIR_POINTS=[(-.245,0,.170),(.245,0,.170),(0,-.360,.145),(0,.420,.500),(0,-.210,.315),(.310,-.148,.280),(0,.175,.385),(0,0,.130),(0,-.107,.224)]
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='professional-fixed-open-drum-hand-crank-duplicator-01';VERSION='1.0.0';TITLE='Fixed Open Drum Hand Crank Duplicator'
DESCRIPTION='One newly authored whole static tabletop rotary stencil-duplicator-style machine exterior. Two complete long ground shoes support thick arched side castings with genuine broad lower windows and a solid upper bearing bridge. A full common axle carries one large broad closed bevelled transverse drum with a blank cylindrical skin, dark end caps and one full raised retaining-strip appearance. A separate lower dark roller and full axle have their own supported side brackets, with a deliberate static air gap to the drum. One empty rear sloping feed table has two whole raised guides. A lower front U-section receiving pan has an actual floor, lips and end stop. An outboard hub, radial crank arm, complete axial stub and long wooden grip belong to the same machine. No old press, note-counter, copier, typewriter or rollers imported. Distinct from the upright chase and forward-opening flat platen/raised ink disc of the old press, and from small feed rollers/star stackers inside the note-counter casing. One prop, zero scenes; no papers, words, artwork, banknotes, ink or printed output. Four opaque constant untextured PBR materials, metres, Z up and actual bounds-centred ground origin. Fixed illustrative art only: no stencil processing, replication, printing, ink transfer, feeding, pressure, drive, mechanical travel, historical accuracy, manufacture, operation or machinery safety claim.'
PALETTE=[('WholeWindowedFrameAndGuides_DeepGreen',(.075,.205,.150,1),.65,.25),('WholeAxlesCrankAndStrip_SatinSteel',(.40,.45,.46,1),.43,.65),('WholeRollerAndDrumEnds_Charcoal',(.045,.055,.052,1),.73,.05),('WholeDrumTrayAndGrip_WarmIvory',(.60,.50,.33,1),.66,.05)]
FOCUS=(0,0,.285);ORTHO=1.30
CAMERAS={'gray-front3q':(3.3,-5,3.4),'gray-back3q':(-3,5,3),'thumbnail':(3.3,-5,3.4),'qa-front':(3.3,-5,3.1),'qa-side':(5,0,3),'qa-top':(0,0,6),'qa-back':(-3,5,3),'qa-wireframe':(3.3,-5,3.4),'silhouette-128-front':(3.3,-5,3.1),'silhouette-128-side':(5,0,3)}
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
root=bpy.data.objects.new('OneFixedOpenDrumHandCrankDuplicator',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='two whole long shoe soles at Z0; actual bounds centred; whole fixed rotary duplicator';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==1344 and len(parts)==21
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
