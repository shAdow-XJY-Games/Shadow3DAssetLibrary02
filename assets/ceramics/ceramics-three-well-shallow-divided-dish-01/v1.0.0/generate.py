import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='ceramics-three-well-shallow-divided-dish-01'
G={}
def add(a,b):return tuple(x+y for x,y in zip(a,b))

def sub(a,b):return tuple(x-y for x,y in zip(a,b))

def mul(a,s):return tuple(x*s for x in a)

def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

def dot(a,b):return sum(x*y for x,y in zip(a,b))

def unit(a):return mul(a,1/math.sqrt(dot(a,a)))

def record(name,v,f,m):
 if sum(dot(v[a],cross(v[b],v[c]))for a,b,c in f)<0:f=[(a,c,b)for a,b,c in f]
 G[name]=(v,f,m)

# Exact exterior of occupied polar prisms; every shared face cancels once.
# Lower slab is complete. Upper material is only the outer ring, central hub,
# and three real radial dividers. Three intervening annular sectors are empty.
N=36;RADII=[0,.025,.165,.19];LEVELS=[0,.009,.035]
v=[];lookup={};boundary={}
def idx(p):
 k=tuple(round(x,12)for x in p)
 if k not in lookup:lookup[k]=len(v);v.append(k)
 return lookup[k]
def xy(r,i):return(r*math.cos(2*math.pi*(i%N)/N),r*math.sin(2*math.pi*(i%N)/N))
for layer in range(2):
 for band in range(3):
  for i in range(N):
   if layer==1 and band==1 and i not in [0,12,24]:continue
   r0,r1=RADII[band:band+2];p=([xy(0,0),xy(r1,i),xy(r1,i+1)]if r0==0 else[xy(r0,i),xy(r1,i),xy(r1,i+1),xy(r0,i+1)])
   low=[idx((x,y,LEVELS[layer]))for x,y in p];up=[idx((x,y,LEVELS[layer+1]))for x,y in p];faces=[tuple(reversed(low)),tuple(up)]+[(low[j],low[(j+1)%len(p)],up[(j+1)%len(p)],up[j])for j in range(len(p))]
   for face in faces:
    key=tuple(sorted(face))
    if key in boundary:del boundary[key]
    else:boundary[key]=face
f=[(face[0],face[i],face[i+1])for face in boundary.values()for i in range(1,len(face)-1)]
used=sorted({x for face in f for x in face});remap={old:i for i,old in enumerate(used)}
v=[v[i]for i in used];f=[tuple(remap[x]for x in face)for face in f]
record('WholeThreeWellDividedDish',v,f,0)

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
for name,color,rough in [('Dish_CeladonGlaze',(.44,.59,.54,1),.32)]:
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=0;materials.append(m)
parts=[]
for name,(v,f,mi) in G.items():
 me=bpy.data.meshes.new(name+'Mesh');me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o)
 for m in materials:me.materials.append(m)
 for p in me.polygons:p.material_index=mi;p.use_smooth=False
 parts.append(o)
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
triangles=sum(len(f)for v,f,m in G.values())
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
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
focus=Vector((0,0,.0175))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.53;aim(cam,(2.4,-3.2,4.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/ceramics/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'ceramics','style':'S01-clean-geometric','title':'Three-Well Shallow Ceramic Dish','description':'One original static shallow ceramic serving dish from the ceramics shallow-plate plan, not a rescaled single-cavity mixing bowl. One connected closed solid includes a full planar bottom, continuous outer wall and annular rim, central hub and three full-depth radial material dividers. These form three genuine separate 110-degree shallow blind wells with their own integral floors and inner walls; no independent bowls, pasted dark patches, overlapping surfaces or loose divider bars. 0.38 m diameter, 0.035 m height, 0.009 m bottom, three 10-degree solid divider sectors. One editable mesh, one constant opaque celadon PBR, metres and ground-centred origin. Static game exterior only; no food-contact, thermal, liquid, load, manufacture or safety certification.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':1,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
