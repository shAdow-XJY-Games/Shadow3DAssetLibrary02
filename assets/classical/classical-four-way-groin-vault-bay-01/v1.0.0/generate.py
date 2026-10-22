import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='classical-four-way-groin-vault-bay-01'
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
# A new single connected vault and four full corner piers, not crossed old arches.
V=[];F=[];index={}
def vertex(p):
 p=tuple(round(float(a),9)for a in p)
 if p not in index:index[p]=len(V);V.append(p)
 return index[p]
def tri(a,b,c):F.append(tuple(vertex(p)for p in[a,b,c]))
def quad(a,b,c,d):tri(a,b,c);tri(a,c,d)
RADIUS=1.4;SPRING=1.1;THICK=.18
XS=sorted(set([round(RADIUS*math.sin(math.pi*k/12),9)for k in range(-6,7)]+[-1.1,1.1]))
def zroof(x,y):return SPRING+math.sqrt(max(0,RADIUS*RADIUS-min(x*x,y*y)))
def pt(i,j,kind):
 x,y=XS[i],XS[j];h=zroof(x,y)
 return(x,y,0 if kind=='ground' else h+THICK if kind=='top' else h)
def pier(i,j):return abs((XS[i]+XS[i+1])/2)>1.1 and abs((XS[j]+XS[j+1])/2)>1.1
edges={};P=[]
for i in range(len(XS)-1):
 for j in range(len(XS)-1):
  a,b,c,d=(i,j),(i+1,j),(i+1,j+1),(i,j+1)
  ts=[(a,b,c),(a,c,d)]if (XS[i]+XS[i+1])*(XS[j]+XS[j+1])>=0 else[(a,b,d),(b,c,d)]
  for t in ts:
   tri(*(pt(*p,'top')for p in t));tri(*(pt(*p,'ground'if pier(i,j)else'ceiling')for p in reversed(t)))
  for u,v in[(a,b),(b,c),(c,d),(d,a)]:edges.setdefault(tuple(sorted([u,v])),[]).append((u,v,pier(i,j)))
for e,uses in edges.items():
 if len(uses)==1:
  a,b,p=uses[0];quad(pt(*a,'ceiling'),pt(*b,'ceiling'),pt(*b,'top'),pt(*a,'top'))
 if sum(p for a,b,p in uses)==1:
  a,b,p=next(x for x in uses if x[2]);quad(pt(*a,'ground'),pt(*b,'ground'),pt(*b,'ceiling'),pt(*a,'ceiling'))
record('WholeFourWayGroinVaultAndCornerPiers',V,F,0)

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
for name,color,rough in [('WarmLimestone',(.58,.51,.40,1),.86)]:
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=.6 if name in ['Frame_Silver','Rims_Satin'] else 0;materials.append(m)
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
focus=Vector((0,0,1.30))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=4.45;aim(cam,(5,-7,2.0));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/classical/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'modular','theme':'classical','style':'S01-clean-geometric','title':'Four-Way Groin Vault Bay','description':'One original complete static classical four-way groin-vault bay. Two perpendicular faceted cylindrical vault directions meet along four diagonal groins in one continuous thick roof, with four integral solid corner piers and four fully open sides leading into a shared central space. The whole roof and four broad ground soles belong to one closed connected editable mesh, not two overlapping old arch meshes, an oven with its rear removed, a straight corridor or a reskinned room. No floor, hidden crossing partition, detached capital, old asset mesh, rubble, texture or animation. Geometry is an illustrative static game module only: no structural thrust, load bearing, engineering, historical reconstruction, building-code, navigation, accessibility, installation, modular-host fit or safety certification.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':1,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
