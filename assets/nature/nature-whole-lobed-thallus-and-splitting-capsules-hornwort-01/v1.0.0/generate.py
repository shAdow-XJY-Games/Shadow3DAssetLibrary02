"""One newly authored entire visible lobed hornwort thallus and attached whole horn capsules. Static botanical exterior art."""
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

# Entire new hornwort surface and complete capsules; no old liverwort geometry.
G={};JOINTS=[];AIR=[];BODY='WholeIrregularRosetteThallus';GROUND=[BODY]
def unit(v):return mul(v,1/math.sqrt(dot(v,v)))
def edge(a):return .052*(1+.13*math.sin(5*a+.3)+.06*math.cos(9*a-.4))
def height(x,y):
 a=math.atan2(y,x);r=math.hypot(x,y)/edge(a);return .0063+.0012*math.cos(x*65)*math.sin(y*53)+.0022*r**6*math.sin(6*a+.4)
N=96;NR=10;upper=[];lower=[];m=Mesh()
for i in range(1,NR+1):
 r=i/NR;xy=[(r*edge(math.tau*j/N)*math.cos(math.tau*j/N),r*edge(math.tau*j/N)*math.sin(math.tau*j/N))for j in range(N)];upper.append([(x,y,height(x,y))for x,y in xy]);lower.append([(x,y,0)for x,y in xy])
for j in range(N):k=(j+1)%N;m.tri([(0,0,height(0,0)),upper[0][j],upper[0][k]],0);m.tri([(0,0,0),lower[0][k],lower[0][j]],1)
for rows,mat in[(upper,0),(lower,1)]:
 for aa,bb in zip(rows,rows[1:]):
  for j in range(N):k=(j+1)%N;m.quad(aa[j],aa[k],bb[k],bb[j],mat)
for j in range(N):k=(j+1)%N;m.quad(upper[-1][j],upper[-1][k],lower[-1][k],lower[-1][j],0)
G[BODY]=m.result('One whole continuous irregular rosette-like thallus, with low gently corrugated lobed margins, a finite lower placement surface and no forked midrib, notched paired tips or gemma cups. It is a complete visible above-ground generic hornwort form, not a cropped leaf or old liverwort mesh. Microscopic rhizoids, internal cavities and cellular layers beneath the exterior are omitted.')
def axial(name,profile,c,lean,mat,role,N=24):
 rows=[];m=Mesh()
 for r,z in profile:rows.append([(c[0]+lean[0]*z+r*math.cos(math.tau*j/N),c[1]+lean[1]*z+r*math.sin(math.tau*j/N),c[2]+z)for j in range(N)])
 for i,(aa,bb)in enumerate(zip(rows,rows[1:])):
  ra,rb=profile[i][0],profile[i+1][0]
  if ra==rb==0:continue
  for j in range(N):
   k=(j+1)%N;mi=mat if isinstance(mat,int)else mat[i]
   if ra==0:m.tri([aa[0],bb[j],bb[k]],mi)
   elif rb==0:m.tri([aa[j],aa[k],bb[0]],mi)
   else:m.quad(aa[j],aa[k],bb[k],bb[j],mi)
 G[name]=m.result(role)
SITES=[(-.025,-.011,.150,.30,True),(.022,.017,.128,1.0,True),(.026,-.025,.102,.10,False),(-.019,.028,.087,2.3,False),(.001,.004,.115,2.0,False)]
for i,(x,y,h,angle,opened)in enumerate(SITES):
 z=height(x,y);c=(x,y,z);lean=(.045*math.cos(angle+.5),.045*math.sin(angle+.5));axisx=(math.cos(angle),math.sin(angle),0);axisy=(-math.sin(angle),math.cos(angle),0)
 sheath='WholeBasalInvolucre_%d'%(i+1);profile=[(0,-.0013),(.0045,-.0013),(.0058,.003),(.0053,.012),(.00435,.012),(.0039,.004),(0,.0010)];axial(sheath,profile,c,(0,0),3,'One entire short cylindrical involucral remnant around the capsule base, with real open rim and closed attached floor. This is a natural basal sheath, not a gemma cup, vase or added stand.');JOINTS.append((BODY,sheath,(x,y,z-.0006)))
 cap='WholeHornCapsule_%d'%(i+1)
 if not opened:
  profile=[(0,-.0008),(.0036,-.0008),(.0038,.008),(.0035,h*.25),(.0028,h*.55),(.0018,h*.82),(.0007,h*.97),(0,h)];axial(cap,profile,c,lean,2,'One entire closed tapering horn capsule emerging directly from the thallus. Its full visible horn is capsule, not a moss stalk carrying an apical head. No separate seta, flower, spore release or internal spore anatomy is claimed.')
 else:
  profile=[(0,-.0008),(.0036,-.0008),(.0038,.008),(.0036,h*.25),(.0035,h*.45),(0,h*.45)];axial(cap,profile,c,lean,2,'Complete still-closed basal region of a mature capsule, joined by finite overlap to both whole separating upper valves and the complete central columella. The whole capsule assembly remains present; this is not an isolated harvested segment.')
  for side in[-1,1]:
   K=18;STEPS=18;rows=[];m=Mesh()
   for j in range(STEPS+1):
    t=j/STEPS;zz=h*(.40+.60*t);spread=.014*t*t;radius=.0036*(1-.72*t);inner=radius*.62;row=[]
    # A full curved half-shell valve with real wall thickness and closed cut margins.
    section=[(r,-math.pi/2+.10+k*(math.pi-.20)/K)for r in[radius,inner]for k in(range(K+1)if r==radius else range(K,-1,-1))]
    for r,a in section:
     xx=side*(spread+r*math.cos(a));yy=r*math.sin(a);p=add((x+lean[0]*zz,y+lean[1]*zz,z+zz),add(mul(axisx,xx),mul(axisy,yy)));row.append(p)
    rows.append(row)
   for aa,bb in zip(rows,rows[1:]):
    for j in range(len(aa)):k=(j+1)%len(aa);m.quad(aa[j],aa[k],bb[k],bb[j],4)
   # Cap each curved annular half-section by radial-strip quads, no concave fan.
   for row in[rows[0],rows[-1]]:
    for j in range(K):m.quad(row[j],row[j+1],row[2*K+2-2-j],row[2*K+2-1-j],4)
   name='WholeSeparatedCapsuleValve_%d_%s'%(i+1,'A'if side<0 else'B');G[name]=m.result('One whole upper capsule valve with complete curved half-shell width, real thickness and closed margins. It remains rooted in the complete lower capsule; its partner and the central columella are also present. Mature open schematic, no detached ribbon, exact species or dehiscence animation.');t=.025;zz=h*(.40+.60*t);p=add((x+lean[0]*zz,y+lean[1]*zz,z+zz),mul(axisx,side*(.014*t*t+.0030)));JOINTS.append((cap,name,p))
  col='WholeCentralColumella_%d'%(i+1);profile=[(0,h*.31),(.00078,h*.31),(.00072,h*.60),(.00048,h*.90),(.00025,h*.99),(0,h)];axial(col,profile,c,lean,5,'One complete exposed central sterile-column schematic through the open capsule region, rooted inside the still-closed lower capsule. No inferred flow, microscopic tissue, spore mass or pseudo-elater detail.');JOINTS.append((cap,col,(x+lean[0]*h*.34,y+lean[1]*h*.34,z+h*.34)))
  zz=h*.78;centre=(x+lean[0]*zz,y+lean[1]*zz,z+zz);p=add(centre,add(mul(axisx,.003),mul(axisy,-.013)));AIR.append(dict(point=p,direction=axisy,length_m=.026,scope='Finite assembled transverse corridor between separated complete valves, beside the central columella; not a through-thallus pore'))
 JOINTS.append((BODY,cap,(x,y,z-.0004)));JOINTS.append((sheath,cap,(x,y,z+.0005)))
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[k]for p in vv)+max(p[k]for p in vv))/2 if k<2 else-min(p[2]for p in vv)for k in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
JOINTS=[(a,b,add(p,SHIFT))for a,b,p in JOINTS]
for ray in AIR:ray['point']=add(ray['point'],SHIFT)
EXPECTED_TRIANGLES=sum(len(g['faces'])for g in G.values());EXPECTED_MESHES=len(G)
ASSET='nature-whole-lobed-thallus-and-splitting-capsules-hornwort-01';VERSION='1.0.0';TITLE='Whole Lobed Thallus and Splitting Capsules Hornwort'
DESCRIPTION='One newly authored whole visible generic hornwort form: a continuous low irregular rosette-like thallus bears five complete horn-capsule assemblies directly, without moss-like supporting setae. Three capsules remain closed and tapered. Two mature capsules retain their complete green lower regions, both whole spreading upper half-shell valves and slender complete central columellae. Each capsule base sits within an entire short open-rimmed involucral sheath rooted to the thallus. New thallus outline, surface sampling, horn profiles, complete valve shell geometry, column paths and all attachment positions; no old liverwort forked thallus, gemma cups, old moss leaves/setae/capsule, held plant or cropped biological part is reused. One above-ground botanical exterior model, zero scenes; naturally attached capsules and valves are not separate asset counts. Quiet opaque schematic, not a measured Anthoceros or Phaeoceros species, natural exact capsule count or developmental sequence. Rhizoids, internal thallus cavities, Nostoc, cell walls, stomata, spores and pseudo-elaters are omitted rather than falsely simulated. Open valves portray one static mature arrangement, not a claim that all hornwort taxa open identically. Finite thallus underside defines the art placement plane, with no added ground, pot or base. No growth, dispersal, photosynthesis, nutrient transport, physical stability, rig, animation, textures or labels.'
PALETTE=[('WholeThallus_DeepGreen',(.15,.31,.075,1),.87,0.),('ThallusLower_EarthyOlive',(.12,.17,.055,1),.93,0.),('CompleteCapsule_QuietGreen',(.23,.38,.10,1),.84,0.),('WholeInvolucre_LeafGreen',(.20,.35,.075,1),.87,0.),('WholeMatureValves_WarmBrown',(.40,.26,.12,1),.89,0.),('WholeColumella_PaleOchre',(.62,.52,.27,1),.89,0.)]
FOCUS=(0,0,.074);CAMERAS={'thumbnail':(.45,-1.3,1.12),'qa-front':(.45,-1.3,1.12),'qa-side':(-1.4,.3,.3),'qa-top':(0,0,2),'qa-back':(-.45,1.3,1.1),'qa-wireframe':(.45,-1.3,1.12)}
ORTHO=.220;WIRE_THICKNESS=.000035

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
root=bpy.data.objects.new('OneWholeLobedThallusHornwort',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='finite complete thallus underside as art placement datum, no physical stability claim';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
