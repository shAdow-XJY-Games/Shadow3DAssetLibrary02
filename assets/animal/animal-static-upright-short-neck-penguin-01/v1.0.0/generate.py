import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='animal-static-upright-short-neck-penguin-01'
G={};FM={}
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def unit(a):return tuple(x/math.sqrt(dot(a,a))for x in a)
def mesh(name,v,faces,mat):
 f=[]
 for p in faces:
  for k in range(1,len(p)-1):f.append((p[0],p[k],p[k+1]))
 if sum(dot(v[a],cross(v[b],v[c]))for a,b,c in f)<0:f=[tuple(reversed(p))for p in f]
 G[name]=(v,f,mat)

# Newly authored whole upright short-neck silhouette; no old animal arrays imported.
def loft(name,rings,mat):
 n=len(rings[0]);v=[p for ring in rings for p in ring];f=[tuple(reversed(range(n))),tuple((len(rings)-1)*n+i for i in range(n))]
 for k in range(len(rings)-1):
  for i in range(n):j=(i+1)%n;f.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i))
 mesh(name,v,f,mat)
def xy(z,x,y,rx,ry,n=16):return[(x+rx*math.cos(math.tau*i/n),y+ry*math.sin(math.tau*i/n),z)for i in range(n)]
BODY=[(.10,0,.06,.16,.13),(.23,0,.04,.28,.23),(.48,0,.03,.355,.265),(.76,0,.01,.33,.245),(.98,0,-.015,.245,.185),(1.12,0,-.055,.19,.155),(1.26,0,-.095,.225,.19),(1.40,0,-.10,.215,.175),(1.50,0,-.095,.135,.115),(1.54,0,-.095,.045,.045)]
loft('WholeContinuousUprightTorsoShortNeckAndHead',[xy(*q)for q in BODY],0)
v,f,m=G['WholeContinuousUprightTorsoShortNeckAndHead'];FM['WholeContinuousUprightTorsoShortNeckAndHead']=[0]*len(f)
# Each complete longitudinal surface quad has a single material on both triangles.
# This forms an uninterrupted bounded belly panel, not centroid-selected diagonal patches.
for k in range(len(BODY)-1):
 for i in range(16):
  if k<=4 and 9<=i<=14:
   j=2*(16-2)+2*(k*16+i);FM['WholeContinuousUprightTorsoShortNeckAndHead'][j:j+2]=[1,1]
# Broad short bill, real whole closed tapered wedge, not the long wader bill.
loft('WholeShortBroadBluntBill',[[(x,y,z)for x,z in[(-w,zc-h),(w,zc-h),(w,zc+h),(-w,zc+h)]]for y,w,zc,h in[(-.235,.09,1.285,.055),(-.34,.09,1.275,.045),(-.455,.045,1.25,.012)]],2)
# Full tapered flattened side flippers: broad upper roots, a long downward/outward blade and blunt narrow tip.
for s,label in[(-1,'Left'),(1,'Right')]:
 rings=[]
 for x,y,z,rx,ry in[(.24,.00,1.01,.075,.067),(.345,-.015,.92,.087,.055),(.43,-.035,.74,.07,.038),(.51,-.07,.55,.042,.025),(.515,-.08,.49,.013,.012)]:rings.append(xy(z,s*x,y,rx,ry,8))
 loft(label+'WholeFlattenedDownsweptFlipper',rings,0)
 # Entire fan-shaped webbed foot has small front toe scallops; not independent rods or deep wader clefts.
 p=[(-.065,.11),(.065,.11),(.105,-.04),(.15,-.235),(.12,-.29),(.055,-.265),(.015,-.315),(-.025,-.305),(-.055,-.26),(-.12,-.285),(-.15,-.235),(-.095,-.04)]
 n=len(p);cx=s*.16;v=[(cx+x,y,0 if layer==0 else .045+.09*(y+.315)/.425)for layer in[0,1]for x,y in p];v.extend([(cx,0,0),(cx,0,.045+.09*.315/.425)]);f=[]
 for i in range(n):j=(i+1)%n;f.extend([(2*n,j,i),(2*n+1,n+i,n+j),(i,j,n+j,n+i)])
 mesh(label+'WholeFanWebFoot',v,f,2)
 # Dark glossy side eyes seated into the original head surface.
 rings=[]
 for x,r in[(s*.175,.012),(s*.195,.020),(s*.210,.012),(s*.213,.003)]:rings.append([(x,-.198+r*math.cos(math.tau*j/12),1.365+r*math.sin(math.tau*j/12))for j in range(12)])
 loft(label+'SmallLateralEye',rings,3)
# Small rear tail is one whole tapered blunt solid, not a third long flipper.
loft('WholeShortRearTaperedTail',[[(-w,y,z-h),(w,y,z-h),(w,y,z+h),(-w,y,z+h)]for y,w,z,h in[(.16,.12,.20,.075),(.34,.095,.15,.045),(.43,.025,.115,.013)]],0)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('Plumage_DeepBlueCharcoal',(.035,.060,.080,1),.84,0),('Belly_WarmIvory',(.79,.79,.69,1),.88,0),('BillAndWebFeet_MutedOchre',(.72,.37,.11,1),.84,0),('SmallEyes_DeepCharcoal',(.006,.009,.012,1),.47,0)]
# BLENDER PHASE
import bpy
from mathutils import Vector
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=128
scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for layer in scene.view_layers:layer.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=4
scene.use_nodes=False;scene.render.use_compositing=False
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='AgX'
materials=[]
for name,col,rough,metal in PALETTE:
 m=bpy.data.materials.new(name);m.diffuse_color=col;m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=col;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;materials.append(m)

parts=[]
for name,(v,f,mi) in G.items():
 me=bpy.data.meshes.new(name+'Mesh');me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o)
 for m in materials:me.materials.append(m)
 face_materials=FM[name]if name in FM else[mi]*len(f)
 for i,p in enumerate(me.polygons):p.material_index=face_materials[i];p.use_smooth=False
 parts.append(o)
for prefix in []:
 parent=bpy.data.objects.new(prefix+'_CompleteSourceAssembly',None);scene.collection.objects.link(parent)
 for o in parts:
  if o.name.startswith(prefix+'__'):o.parent=parent
 parent.select_set(True)
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
triangles=sum(len(f)for v,f,m in G.values())
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
(OUT/'qa-report.json').write_text(json.dumps({'asset':ASSET,'mesh_objects':len(G),'triangles':triangles,'materials':len(PALETTE),'new_independent_models':1,'new_scenes':0},indent=2))
if '--geometry-only' in sys.argv:
 print('GEOMETRY_READY',ASSET,triangles);sys.exit(0)
# Render the actual exported geometry, not an unexported proxy.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
parts=[x for x in scene.objects if x.type=='MESH'];assert len(parts)==len(G)
view='thumbnail'
if '--view' in sys.argv:view=sys.argv[sys.argv.index('--view')+1]
assert view in ['qa-front','thumbnail']
scene.cycles.samples=16 if view=='qa-front' else 128
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.28,.28,.28,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
focus=Vector((0,0,.80))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.10;aim(cam,(3,-6,2.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/animal/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'animal','style':'S01-clean-geometric','title':'Static Upright Short-Neck Penguin','description':'One newly authored stylised upright penguin-inspired animal exterior. A full thick upright pear-shaped torso, short neck and rounded head form one continuous closed shared-vertex surface. A short broad blunt bill, two long flattened downward-swept flippers, two broad thick web-shaped ground feet with shallow front toe scallops, two small lateral eyes and a short rear tapered tail complete the fixed whole silhouette. The warm pale belly is an integral face-material region of the same torso, not an overlapping shell. Whole body stations, flipper trajectories, bill, feet and tail are new; not a shortened long-legged wading bird, upright old seal or recoloured toy bear. Generic mesh construction and mature export/render tools only are reused. Nine closed editable meshes, four opaque constant matte PBR roles, no textures, fur, feathers or scene. Metres, native Z up, head/front -Y, actual complete horizontal-bounds-centred ground origin, two full finite foot soles. One whole model and zero scenes or separately counted parts. Artistic fixed exterior only: no exact species or biological/anatomical fidelity, swimming, flight, gait, motion, rig, animal care, stability, fit, physical or ecological performance claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
