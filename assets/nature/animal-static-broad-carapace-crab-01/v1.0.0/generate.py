"""Original static broad-carapace crab. New whole source, no product or visual PASS yet."""
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
def unit(v):return mul(v,1/math.sqrt(dot(v,v)))
def loft(points,radii,mat,role):
 m=Mesh();rings=[]
 for k,p in enumerate(points):
  tangent=unit(sub(points[min(k+1,len(points)-1)],points[max(k-1,0)]));u=unit(cross(tangent,(1,0,0)));v=cross(tangent,u)
  rings.append([add(p,add(mul(u,radii[k][0]*math.cos(math.tau*j/12)),mul(v,radii[k][1]*math.sin(math.tau*j/12))))for j in range(12)])
 for a,b in zip(rings,rings[1:]):
  for j in range(12):i=(j+1)%12;m.quad(a[j],a[i],b[i],b[j],mat)
 for ring,p in[(rings[0],points[0]),(rings[-1],points[-1])]:
  for j in range(12):m.tri([p,ring[j],ring[(j+1)%12]],mat)
 return m.result(role)
def profile(poly,a0,a1,mat,role,plane='xz'):
 m=Mesh()
 def pt(p,a):return(p[0],a,p[1])if plane=='xz'else(*p,a)
 for a in[a0,a1]:
  for f in earclip(poly):m.tri([pt(poly[i],a)for i in f],mat)
 for p,q in zip(poly,poly[1:]+poly[:1]):m.quad(pt(p,a0),pt(q,a0),pt(q,a1),pt(p,a1),mat)
 return m.result(role)
def ellipsoid(center,scale,mat):
 m=Mesh();rings=[]
 for k in range(1,6):
  a=math.pi*k/6;rings.append([add(center,(scale[0]*math.sin(a)*math.cos(math.tau*j/12),scale[1]*math.sin(a)*math.sin(math.tau*j/12),scale[2]*math.cos(a)))for j in range(12)])
 for j in range(12):i=(j+1)%12;m.tri([add(center,(0,0,scale[2])),rings[0][j],rings[0][i]],mat);m.tri([add(center,(0,0,-scale[2])),rings[-1][i],rings[-1][j]],mat)
 for a,b in zip(rings,rings[1:]):
  for j in range(12):i=(j+1)%12;m.quad(a[j],b[j],b[i],a[i],mat)
 return m.result('Small new crab eye, seated on its own stalk; not separately counted')

# New crab geometry below; no old body, elytron, turtle shell or serving tongs.
CROSS=[(-1,-.4),(-.4,-1),(.4,-1),(1,-.4),(1,.4),(.4,1),(-.4,1),(-1,.4)]
def flat_sweep(points,radii,mat,role):
 m=Mesh();rings=[]
 for k,p in enumerate(points):
  tangent=sub(points[min(k+1,len(points)-1)],points[max(k-1,0)]);length=math.hypot(tangent[0],tangent[1]);assert length>1e-9;u=(-tangent[1]/length,tangent[0]/length,0)
  rings.append([add(p,add(mul(u,x*radii[k][0]),(0,0,y*radii[k][1])))for x,y in CROSS])
 for a,b in zip(rings,rings[1:]):
  for i in range(8):j=(i+1)%8;m.quad(a[i],a[j],b[j],b[i],mat)
 for p,ring in[(points[0],rings[0]),(points[-1],rings[-1])]:
  for i in range(8):m.tri([p,ring[i],ring[(i+1)%8]],mat)
 return m.result(role)
def carapace():
 outline=[(0,-.32),(.18,-.31),(.38,-.25),(.53,-.13),(.57,0),(.51,.18),(.34,.28),(0,.32),(-.34,.28),(-.51,.18),(-.57,0),(-.53,-.13),(-.38,-.25),(-.18,-.31)];m=Mesh();rings=[[(x*s,y*s,z)for x,y in outline]for z,s in[(.13,.83),(.20,1),(.28,.97),(.36,.76)]]
 for k,(a,b)in enumerate(zip(rings,rings[1:])):
  for i in range(len(outline)):j=(i+1)%len(outline);m.quad(a[i],a[j],b[j],b[i],1 if k==0 else 0)
 for i in range(len(outline)):
  j=(i+1)%len(outline);m.tri([(0,0,.13),rings[0][j],rings[0][i]],1);m.tri([(0,0,.395),rings[-1][i],rings[-1][j]],0)
 return m.result('One new wide short flattened carapace with continuous lower sternum, angular broad shoulders and low dorsal crown; no separate long head, elytral seam, tall scuted turtle dome or copied old body.')
def pincer(sign):
 # Two unequal fingers and a real broad open V mouth belong to one closed claw.
 p=[(-.08,.10),(.08,.10),(.17,-.03),(.19,-.20),(.11,-.39),(.03,-.46),(-.015,-.42),(.03,-.28),(.055,-.20),(-.03,-.16),(-.07,-.22),(-.13,-.40),(-.19,-.38),(-.20,-.22),(-.19,-.04)];m=Mesh();rr=[]
 for z,s in[(.19,.88),(.25,1.),(.31,.84)]:rr.append([(sign*(.62+x*s),-.67+(-.07+(y+.07)*s),z)for x,y in p])
 for a,b in zip(rr,rr[1:]):
  for i in range(len(p)):j=(i+1)%len(p);m.quad(a[i],a[j],b[j],b[i],0)
 for ring in[rr[0],rr[-1]]:
  for f in earclip(p):m.tri([ring[i]for i in f],0)
 return m.result('Complete thick bevelled crab claw with broad palm and two unequal integral fingers enclosing a true front-open notch; not a scaled serving tongs, tool jaw or detachable fingers. Fixed artistic pose, no gripping simulation.')
G={'BroadLowCarapaceAndSternum':carapace()}
legs=[('Front',(.45,-.18),(.76,-.35),(1.02,-.54),(1.13,-.62)),('FrontMiddle',(.49,-.04),(.88,-.10),(1.15,-.15),(1.26,-.18)),('RearMiddle',(.47,.10),(.86,.20),(1.13,.38),(1.22,.50)),('Rear',(.40,.22),(.69,.43),(.91,.63),(1.0,.76))]
for side,s in[('Left',-1),('Right',1)]:
 for name,r,e,a,t in legs:
  direction=unit((t[0]-a[0],t[1]-a[1],0));end=(t[0]+direction[0]*.035,t[1]+direction[1]*.035)
  pts=[(s*r[0],r[1],.215),(s*e[0],e[1],.23),(s*a[0],a[1],.12),(s*t[0],t[1],.009),(s*end[0],end[1],.009)]
  G[side+name+'WalkingLeg']=flat_sweep(pts,[(.060,.044),(.057,.035),(.037,.023),(.018,.009),(.014,.009)],2,'One complete laterally splayed angular walking limb with flattened taper and two finite toe rings sharing a small actual Z0 sole; four pairs, not extra counted assets.')
 G[side+'ClawArm']=flat_sweep([(s*.36,-.23,.24),(s*.63,-.42,.20),(s*.62,-.60,.25)],[(.065,.045),(.078,.052),(.065,.045)],2,'One new bent stout claw-bearing forelimb, visibly seated into carapace and full pincer palm.')
 G[side+'WholeOpenPincer']=pincer(s)
 G[side+'EyeStalk']=flat_sweep([(s*.17,-.26,.31),(s*.195,-.29,.41),(s*.21,-.31,.49)],[(.029,.027),(.026,.022),(.024,.020)],2,'Short rising forward eye stalk joining dorsal-front carapace to a dark rounded eye.')
 G[side+'StalkEye']=ellipsoid((s*.21,-.31,.505),(.045,.043,.045),3)
vv=[p for g in G.values()for p in g['vertices']];SHIFT=(-(min(p[0]for p in vv)+max(p[0]for p in vv))/2,-(min(p[1]for p in vv)+max(p[1]for p in vv))/2,0)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]

ASSET='animal-static-broad-carapace-crab-01';VERSION='1.0.0';TITLE='Static Broad-Carapace Crab'
DESCRIPTION='One original stylised crab in a fixed grounded display: a broad short low carapace with continuous lower sternum, four pairs of laterally splayed flattened walking limbs, two stout bent forelimbs ending in complete thick bevelled pincers, and two rising stalked dark eyes. Each pincer has two unequal integral fingers around a genuinely open front notch. Each walking foot ends in a finite flat Z0 toe patch. New whole profiles and coordinates, not a beetle with extra old legs, a recoloured tortoise, an eight-arm octopus or paired serving tongs reused. Seventeen closed editable meshes and four opaque matte constant PBR materials, no textures. Metres, native Z up, front -Y, complete horizontal bounds-centred ground origin. One prop, zero scenes; claws, limbs and eyes are not separately counted models. Artistic external exoskeletal silhouette only, not species diagnosis, scientific anatomy, biological internal construction, locomotion, working pincers, rig, animation, collision or stability certification.'
PALETTE=[('CarapaceAndClaws_Russet',(.44,.115,.035,1),.72,0.),('Sternum_WarmOchre',(.40,.23,.095,1),.80,0.),('Limbs_RustOrange',(.47,.175,.055,1),.77,0.),('StalkEyes_Charcoal',(.012,.010,.008,1),.43,0.)]
FOCUS=(0.,0.,.23);ORTHO=3.12
CAMERAS={'gray-front3q':(3.,-4.,3.2),'gray-back3q':(-3.,4.,3.2),'thumbnail':(3.,-4.,3.2),'qa-front':(0,-4.,2.7),'qa-side':(4.,0.,2.7),'qa-top':(0,0,5.),'qa-back':(0,4.,2.7),'qa-wireframe':(-3.,4.,3.2),'silhouette-128-front':(0,-4.,2.7),'silhouette-128-side':(4.,0.,2.7)}
WIRE_THICKNESS=ORTHO/1800
# BLENDER PHASE: common render/export infrastructure only.
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
root=bpy.data.objects.new('OneStaticBroadCarapaceCrab',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='eight finite walking toe soles at Z0; entire horizontal bounds centred; fixed broad-carapace crustacean form';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==1356 and len(parts)==17
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
  files[role]={'path':f'assets/nature/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'nature','style':'S02-hard-edge-faceted','title':TITLE,'description':DESCRIPTION,
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
