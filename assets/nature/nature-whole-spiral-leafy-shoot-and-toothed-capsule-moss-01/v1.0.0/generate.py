"""One newly authored complete leafy moss shoot and mature open sporophyte. Static enlarged botanical art."""
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

# New whole moss domain. Nothing below is a scaled old horsetail or liverwort.
G={};JOINTS=[];BODY='WholeLeafyMossStem';GROUND=[BODY]
def unit(v):return mul(v,1/math.sqrt(dot(v,v)))
def tube(name,centres,radii,mat,role,n=10):
 m=Mesh();rows=[]
 for i,(c,r)in enumerate(zip(centres,radii)):
  w=unit(sub(centres[min(i+1,len(centres)-1)],centres[max(i-1,0)]));ref=(0,1,0)if abs(w[1])<.8 else(1,0,0);u=unit(cross(w,ref));v=cross(w,u)
  rows.append([add(c,add(mul(u,r*math.cos(math.tau*j/n)),mul(v,r*math.sin(math.tau*j/n))))for j in range(n)])
 for j in range(n):
  k=(j+1)%n;m.tri([centres[0],rows[0][k],rows[0][j]],mat);m.tri([centres[-1],rows[-1][j],rows[-1][k]],mat)
 for a,b in zip(rows,rows[1:]):
  for j in range(n):k=(j+1)%n;m.quad(a[j],a[k],b[k],b[j],mat)
 G[name]=m.result(role)
def axis(z):return(0,0,z)if z<=.004 else(.0015*math.sin((z-.004)*42),.0007*math.sin((z-.004)*55),z)
# Finite basal cut is a display datum, not a claim that the specimen stands unaided.
centres=[axis(z)for z in[0,.004,.012,.022,.032,.043,.052]];tube(BODY,centres,[.0028,.0023,.0021,.00195,.0018,.00165,.0014],0,'One complete softly bent gametophyte axis; unjointed, no nodal sheaths or branch whorls.',12)
# Direct sessile, spirally inserted lanceolate leaves with actual curved laminae.
for i in range(27):
 z=.0055+i*.00165;angle=i*2.3999632297+.2;u=(math.cos(angle),math.sin(angle),0);v=(-u[1],u[0],0);c=axis(z);length=.019+.006*math.sin(math.pi*i/26);width=.0046*(.82+.18*math.sin(math.pi*i/26));rise=.008+.010*(i/26)**2
 def point(t,w,side):
  span=.00009+.0008*(1-t)+width*math.sin(math.pi*t)**.82
  radial=.00035+length*t;h=rise*t-.0048*t*t+.00070*math.sin(math.pi*t)*(1-abs(w))
  return add(c,add(mul(u,radial),add(mul(v,span*w),(0,0,h+side*.00020))))
 ts=[k/8 for k in range(9)];ws=[-1,-.66,-.33,0,.33,.66,1];m=Mesh()
 for k in range(8):
  for j in range(6):
   for side,mat in[(1,1),(-1,2)]:m.quad(point(ts[k],ws[j],side),point(ts[k+1],ws[j],side),point(ts[k+1],ws[j+1],side),point(ts[k],ws[j+1],side),mat)
 for k in range(8):
  for w in[-1,1]:m.quad(point(ts[k],w,-1),point(ts[k+1],w,-1),point(ts[k+1],w,1),point(ts[k],w,1),1)
 for t in[0,1]:
  for j in range(6):m.quad(point(t,ws[j],-1),point(t,ws[j+1],-1),point(t,ws[j+1],1),point(t,ws[j],1),1)
 name='WholeSessileSpiralLeaf_%02d'%(i+1);G[name]=m.result('One whole tapered directly attached leaf with continuous upper and lower surfaces, finite thin edge and folded costa-like midregion. No petiole, hairs, stomata, cell pattern or separate counted leaf asset.');JOINTS.append((BODY,name,point(.025,0,0)))
# Sparse complete basal rhizoid strands. Not vascular roots or a soil puck.
for j in range(6):
 a=math.tau*j/6+.23;u=(math.cos(a),math.sin(a),0);v=(-u[1],u[0],0);origin=axis(.0023);length=.0105+.002*math.sin(j*1.4);centres=[add(origin,add(mul(u,length*t),add(mul(v,.002*math.sin(math.pi*t)),(0,0,-.0012*t))))for t in[0,.25,.5,.75,1]];name='WholeBasalRhizoidStrand_%02d'%(j+1);tube(name,centres,[.00065,.00055,.00042,.00030,.00015],3,'One tapered basal anchoring rhizoid strand, exposed for an enlarged display; not an absorptive vascular root.',8);JOINTS.append((BODY,name,add(origin,mul(u,.001))))
# Complete leafless seta arises at the leafy shoot apex and lifts the capsule.
SETA='WholeCurvedLeaflessSeta';CAP='WholeOpenOvoidCapsule';CAP_C=(.014,-.005,.102);CAP_AXIS=unit((.22,-.30,.928));U=unit(cross(CAP_AXIS,(0,1,0)));V=cross(CAP_AXIS,U)
centres=[axis(.047),(.002,-.0002,.057),(.003,-.001,.069),(.006,-.003,.083),(.010,-.0044,.096),add(CAP_C,mul(CAP_AXIS,.0011))];tube(SETA,centres,[.0010,.0011,.00105,.00095,.0009,.0009],3,'One entire slender, gently curved leafless sporophyte stalk attached within the leafy apex; no independent stem count.',12);JOINTS.append((BODY,SETA,axis(.048)))
def local(r,a,t):return add(CAP_C,add(mul(CAP_AXIS,t),add(mul(U,r*math.cos(a)),mul(V,r*math.sin(a)))))
profile=[(0,0),(.0016,0),(.004,.004),(.0068,.010),(.0082,.017),(.008,.023),(.0065,.030),(.0065,.033),(.0053,.033),(.0053,.030),(.0068,.023),(.0069,.017),(.0055,.010),(.0028,.004),(0,.0025)]
m=Mesh();N=48;rows=[[local(r,math.tau*j/N,t)for j in range(N)]for r,t in profile]
for i,a in enumerate(rows):
 k=(i+1)%len(rows);b=rows[k];ra,rb=profile[i][0],profile[k][0];mat=4 if i<8 else 5
 if ra==rb==0:continue
 for j in range(N):
  q=(j+1)%N
  if ra==0:m.tri([a[0],b[j],b[q]],mat)
  elif rb==0:m.tri([a[j],a[q],b[0]],mat)
  else:m.quad(a[j],a[q],b[q],b[j],mat)
G[CAP]=m.result('One complete elongated ovoid empty mature spore capsule with narrowing neck, actual finite wall, interior and open mouth. Operculum has been shed and is not shown. No columella, spores or cell-level wall reconstruction.');JOINTS.append((SETA,CAP,add(CAP_C,mul(CAP_AXIS,.0006))))
# Sixteen short rooted peristome teeth, actual separated solids around open mouth.
for i in range(16):
 a=math.tau*i/16;radial=add(mul(U,math.cos(a)),mul(V,math.sin(a)));side=add(mul(U,-math.sin(a)),mul(V,math.cos(a)));m=Mesh();rows=[]
 for t in[0,.25,.5,.75,1]:
  c=add(CAP_C,add(mul(CAP_AXIS,.0326+.0042*t),mul(radial,.0059-.0010*t*t)));w=.00065*(1-.86*t);th=.00030*(1-.5*t)
  rows.append([add(c,add(mul(side,ss*w),mul(radial,rr*th)))for ss,rr in[(-1,-1),(1,-1),(1,1),(-1,1)]])
 for a0,b0 in zip(rows,rows[1:]):
  for j in range(4):k=(j+1)%4;m.quad(a0[j],a0[k],b0[k],b0[j],6)
 for row in[rows[0],rows[-1]]:m.quad(*row,6)
 name='WholePeristomeTooth_%02d'%(i+1);G[name]=m.result('One entire short tapering peristome tooth rooted inside the capsule rim, with an open gap to the next tooth. Generic single series, not a species-specific cell-wall or humidity mechanism.');JOINTS.append((CAP,name,add(CAP_C,add(mul(CAP_AXIS,.0328),mul(radial,.0059)))))
allv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[k]for p in allv)+max(p[k]for p in allv))/2 if k<2 else-min(p[2]for p in allv)for k in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
JOINTS=[(a,b,add(p,SHIFT))for a,b,p in JOINTS];AP_CENTRE=add(CAP_C,SHIFT);AP_AXIS=CAP_AXIS
EXPECTED_TRIANGLES=sum(len(g['faces'])for g in G.values());EXPECTED_MESHES=len(G)
ASSET='nature-whole-spiral-leafy-shoot-and-toothed-capsule-moss-01';VERSION='1.0.0';TITLE='Whole Spiral Leafy Shoot and Toothed Capsule Moss'
DESCRIPTION='One wholly newly authored enlarged moss specimen with a complete softly bent leafy gametophyte, 27 directly attached spiral lanceolate leaves, six exposed basal rhizoid strands, a long leafless curved seta and a mature open ovoid capsule. The capsule has an actual interior wall and sixteen separate rooted tapering peristome teeth around its open mouth, not a painted hole, attached flower or separate crown prop. Leaves are thin continuous folded blades rather than horsetail branches; there are no old jointed axes, nodal whorls, forked liverwort thalli or gemma cups reused. One complete nature model, zero scenes. Seven opaque restrained botanical material roles, arbitrary enlarged display scale. Generic moss form only, not a measured species, natural colony, cellular anatomy, precise generation ratio, planted root system or physical stability claim. Fine rhizoid branching, spores, columella, membrane endostome, leaf cells and shed operculum are not reconstructed; this is not a whole life-cycle demonstration. No textures, transparency, labels, rig, wind, humidity response, animation or biological simulation.'
PALETTE=[('LeafyAxis_DarkGreen',(.15,.22,.045,1),.91,0.),('LeafUpper_QuietGreen',(.25,.39,.075,1),.84,0.),('LeafLower_Olive',(.16,.27,.055,1),.91,0.),('SetaRhizoids_Russet',(.27,.105,.045,1),.86,0.),('CapsuleOuter_AmberBrown',(.46,.24,.065,1),.84,0.),('CapsuleInside_ShadedUmber',(.23,.12,.035,1),.94,0.),('Peristome_PaleOchre',(.64,.43,.16,1),.88,0.)]
FOCUS=(0,0,.068);CAMERAS={'thumbnail':(.8,-1.5,1.0),'qa-front':(.8,-1.5,1.0),'qa-side':(-1.2,-.4,.9),'qa-top':(0,0,2),'qa-back':(-.8,1.5,.9),'qa-wireframe':(.8,-1.5,1.0)}
ORTHO=.165;WIRE_THICKNESS=.00004

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
root=bpy.data.objects.new('OneWholeLeafyMossAndOpenSporophyte',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='finite basal stem display datum, enlarged complete moss specimen';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==EXPECTED_TRIANGLES and len(parts)==EXPECTED_MESHES
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
# Count the material list in the actual exported GLB, not a copied literal.
import struct
_glb=(OUT/'model.glb').read_bytes();_json_length,_json_kind=struct.unpack_from('<II',_glb,12);assert _json_kind==0x4e4f534a
actual_material_count=len(json.loads(_glb[20:20+_json_length])['materials'])
assert actual_material_count==len({f.material_index for o in parts for f in o.data.polygons})
guard();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':actual_material_count,'mesh_objects':mesh_count,'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,'components':component_checks,'single_prop_count':1,'review_mode':'SELF_REVIEW','static_visual_only':True,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),'status':'producer geometry; maker actual-image acceptance pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/nature/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'nature','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
 'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':actual_material_count,'files':files,'status':'review','license':'All rights reserved'}
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
  ground.hide_render=(name=='qa-side')
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
