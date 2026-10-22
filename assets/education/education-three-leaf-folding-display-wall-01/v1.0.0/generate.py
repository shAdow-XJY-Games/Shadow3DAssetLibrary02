import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='education-three-leaf-folding-display-wall-01'
G={}
def add(a,b):return tuple(x+y for x,y in zip(a,b))

def sub(a,b):return tuple(x-y for x,y in zip(a,b))

def mul(a,s):return tuple(x*s for x in a)

def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

def dot(a,b):return sum(x*y for x,y in zip(a,b))

def record(name,v,f,m):
 if sum(dot(v[a],cross(v[b],v[c]))for a,b,c in f)<0:f=[(a,c,b)for a,b,c in f]
 G[name]=(v,f,m)

LINKS=[]
def quads(q):return [t for a,b,c,d in q for t in [(a,b,c),(a,c,d)]]
def turn(p,center,angle):
 c,s=math.cos(angle),math.sin(angle);x,y,z=p
 return (center[0]+c*x-s*y,center[1]+s*x+c*y,z)
def frame(name,center,angle):
 outer=[(-.36,0),(.36,0),(.36,1.65),(-.36,1.65)]
 inner=[(-.31,.05),(.31,.05),(.31,1.60),(-.31,1.60)]
 v=[turn((x,y,z),center,angle)for shape,y in [(outer,-.025),(outer,.025),(inner,.025),(inner,-.025)]for x,z in shape]
 q=[(4*k+i,4*k+(i+1)%4,4*((k+1)%4)+(i+1)%4,4*((k+1)%4)+i)for k in range(4)for i in range(4)]
 record(name+'WholeThroughFrame',v,quads(q),0)
 v=[turn((x,y,z),center,angle)for z in [.045,1.605]for y in [-.014,.014]for x in [-.315,.315]]
 q=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
 record(name+'WholeInsetBoard',v,quads(q),1)
 LINKS.append((name+'WholeThroughFrame',name+'WholeInsetBoard',turn((.3125,0,.8),center,angle)))
a=math.pi/6
centers={'Center':((0,0),0),'Left':((-.38-.38*math.cos(a),-.38*math.sin(a)),a),'Right':((.38+.38*math.cos(a),-.38*math.sin(a)),-a)}
for name,(center,angle)in centers.items():frame(name,center,angle)
def knuckle(name,x,z):
 n=12;v=[(x+r*math.cos(2*math.pi*i/n),r*math.sin(2*math.pi*i/n),h)for r,h in[(.025,z),(.025,z+.12),(.009,z+.12),(.009,z)]for i in range(n)]
 q=[(k*n+i,k*n+(i+1)%n,((k+1)%4)*n+(i+1)%n,((k+1)%4)*n+i)for k in range(4)for i in range(n)]
 record(name,v,quads(q),2)
def pinrod(name,x):
 n=12;v=[(x+.010*math.cos(2*math.pi*i/n),.010*math.sin(2*math.pi*i/n),z)for z in[.22,1.44]for i in range(n)]
 f=quads([(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)])+[(0,i+1,i)for i in range(1,n-1)]+[(n,n+i,n+i+1)for i in range(1,n-1)]
 record(name,v,f,2)
for side,x in [('Left',-.38),('Right',.38)]:
 rod=side+'CompleteVerticalPin';pinrod(rod,x)
 for j,z in enumerate([.24,.77,1.30]):
  k=side+'BoredKnuckle'+str(j);knuckle(k,x,z);h=z+.06
  LINKS.append((rod,k,(x+.0095,0,h)))
  owner='Center'if j==1 else side;center,angle=centers[owner]
  xx=(-.358 if side=='Left' else .358)if owner=='Center'else(.358 if side=='Left'else-.358)
  LINKS.append((owner+'WholeThroughFrame',k,turn((xx,0,h),center,angle)))
# Exact common bottom/bounds-centred origin, applied to every full component and witness.
bounds=[(min(p[k]for v,f,m in G.values()for p in v),max(p[k]for v,f,m in G.values()for p in v))for k in range(3)]
shift=((bounds[0][0]+bounds[0][1])/2,(bounds[1][0]+bounds[1][1])/2,bounds[2][0])
G={name:([sub(p,shift)for p in v],f,m)for name,(v,f,m)in G.items()}
LINKS=[(a,b,sub(p,shift))for a,b,p in LINKS]

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
for name,color,rough in [('Maple_Frame',(.48,.30,.14,1),.72),('Blank_TealBoard',(.12,.32,.28,1),.82),('Satin_Hinge',(.43,.45,.40,1),.46)]:
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
focus=Vector((0,0,.83))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.8;aim(cam,(3,-7,3.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/education/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'education','style':'S01-clean-geometric','title':'Three-Leaf Folding Display Wall','description':'One complete original three-leaf teaching display wall from the original education display-wall candidate. Three separately closed thick rectangular through-frames contain three inset blank board panels. Two complete vertical pins pass through six actual bored knuckles between the frames. Side leaves stand at fixed 30 degree inward folds; all three full lower frame rails meet the ground. Fourteen closed editable meshes and three constant opaque PBR materials. One complete prop, not three assets or three rotated copies of an old blackboard. The entire new frame, insert and joint construction is authored here; no previous geometry is extracted or rescaled. Fixed presentation only: the pin/knuckle geometry has deliberate static bearing overlap, not kinematic clearance. No folding simulation, writing, paper pinning, human fit, stability, hinge loading, manufacturing or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
