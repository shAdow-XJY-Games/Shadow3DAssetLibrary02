import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='ceramics-twin-track-clay-storage-chest-01'
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

def earclip(p):
 cr=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 ids=list(range(len(p)));out=[]
 while len(ids)>3:
  for j,b in enumerate(ids):
   a,c=ids[j-1],ids[(j+1)%len(ids)]
   if cr(p[a],p[b],p[c])<=1e-14:continue
   if any(all(cr(p[u],p[v],p[k])>=-1e-14 for u,v in [(a,b),(b,c),(c,a)])for k in ids if k not in [a,b,c]):continue
   out.append((a,b,c));ids.pop(j);break
  else:raise ValueError('Non-simple padding section')
 out.append(tuple(ids));return out

def pad(name,p,y0,y1,m):
 if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);v=[(x,y,z)for y in[y0,y1]for x,z in p];f=[]
 for a,b,c in earclip(p):f.extend([(a,b,c),(c+n,b+n,a+n)])
 for i in range(n):
  j=(i+1)%n;f.extend([(i,j+n,j),(i,i+n,j+n)])
 record(name,v,f,m)

def quads(q):return [(a,b,c)for a,b,c,d in q]+[(a,c,d)for a,b,c,d in q]
outer=[(-.32,-.43),(.32,-.43),(.32,.43),(-.32,.43)]
inner=[(-.285,-.395),(.285,-.395),(.285,.395),(-.285,.395)]
v=[(x,y,z)for ring,z in [(outer,0),(outer,.65),(inner,.65),(inner,.04)]for x,y in ring]
q=[(0,3,2,1),(12,13,14,15)]
for i in range(4):
 j=(i+1)%4;q.extend([(i,j,j+4,i+4),(i+4,j+4,j+8,i+8),(i+8,j+8,j+12,i+12)])
record('WholeDeepClayChestShell',v,quads(q),0)
# Each rail is one continuous concave prism with two inward-facing real channels.
# Rail ends are 5 mm inset from body ends, avoiding exposed coplanar patches.
profile=[(-.335,.6497),(-.265,.6497),(-.265,.67),(-.305,.67),(-.305,.69),(-.265,.69),(-.265,.71),(-.305,.71),(-.305,.73),(-.265,.73),(-.265,.75),(-.335,.75)]
pad('LeftWholeTwinChannelRail',profile,-.425,.425,1)
pad('RightWholeTwinChannelRail',[(-x,z)for x,z in profile],-.425,.425,1)
def pierced_cover(name,y0,y1,z0,z1,hole_y):
 outer=[(-.302,y0),(.302,y0),(.302,y1),(-.302,y1)]
 inner=[(-.035,hole_y-.015),(.035,hole_y-.015),(.035,hole_y+.015),(-.035,hole_y+.015)]
 v=[(x,y,z)for ring,z in [(outer,z0),(outer,z1),(inner,z1),(inner,z0)]for x,y in ring];q=[]
 for i in range(4):
  j=(i+1)%4;q.extend([(i,j,j+4,i+4),(i+4,j+4,j+8,i+8),(i+8,j+8,j+12,i+12),(i+12,j+12,j,i)])
 record(name,v,quads(q),2)
# Deliberate 0.3 mm fixed bearing overlap; not a moving fit or tested sliding path.
pierced_cover('LowerPartlyRetractedPiercedCover',-.145,.285,.6697,.688,-.10)
pierced_cover('UpperRearPiercedCover',0,.395,.7097,.728,.35)
LINKS=[('WholeDeepClayChestShell','LeftWholeTwinChannelRail',(-.30,0,.64985)),('WholeDeepClayChestShell','RightWholeTwinChannelRail',(.30,0,.64985))]
for label,x in [('Left',-.295),('Right',.295)]:
 LINKS.append((label+'WholeTwinChannelRail','LowerPartlyRetractedPiercedCover',(x,-.10,.66985)))
 LINKS.append((label+'WholeTwinChannelRail','UpperRearPiercedCover',(x,.20,.70985)))

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
for name,color,rough in [('Chest_MutedClayGreen',(.19,.30,.27,1),.67),('Tracks_DarkSlate',(.085,.11,.12,1),.61),('Covers_WarmWood',(.53,.34,.17,1),.72)]:
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
focus=Vector((0,0,.375))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.30;aim(cam,(3,-5,3.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/ceramics/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'ceramics','style':'S01-clean-geometric','title':'Twin-Track Clay Storage Chest','description':'One original static empty clay-storage chest from the ceramics storage-box plan. A single thick deep rectangular shell has a complete bottom and unpartitioned open cavity. Two continuous side rails each contain two genuine full-length recessed channels; two separate thick cover panels sit at different fixed heights and overlap toward the rear, leaving a clear front access opening. Each cover has a true rectangular finger aperture. Five closed pieces, three constant opaque PBR materials, metres, Z up, front -Y, grounded centred origin. Newly authored shell, dual-channel cross-sections and pierced covers, not a resized round jar, six-compartment bait box, cushioned seatbox or low-front picking bin. No contents, hinge, animation, tested sliding travel, sealing, moisture retention, material suitability, capacity, load, manufacture or safety certification.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
