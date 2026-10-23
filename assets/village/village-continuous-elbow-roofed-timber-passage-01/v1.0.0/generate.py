import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='village-continuous-elbow-roofed-timber-passage-01'
G={};FM={}
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sheet_solid(name,xs,ys,occupied,low,high,mat):
 v=[];f=[];ids={}
 def vertex(x,y,upper):
  p=(round(x,9),round(y,9),round((high if upper else low)(x,y),9))
  if p not in ids:ids[p]=len(v);v.append(p)
  return ids[p]
 def quad(q):a,b,c,d=q;f.extend([(a,b,c),(a,c,d)])
 for i,j in sorted(occupied):
  x0,x1=xs[i:i+2];y0,y1=ys[j:j+2];q=[vertex(x,y,k)for k in [0,1]for y in [y0,y1]for x in [x0,x1]]
  quad([q[k]for k in [0,2,3,1]]);quad([q[k]for k in [4,5,7,6]])
  for delta,face in [((-1,0),[0,4,6,2]),((1,0),[1,3,7,5]),((0,-1),[0,1,5,4]),((0,1),[2,6,7,3])]:
   if (i+delta[0],j+delta[1])not in occupied:quad([q[k]for k in face])
 assert sum(dot(v[a],cross(v[b],v[c]))for a,b,c in f)>0
 G[name]=(v,f,mat)
def roof_top(x,y):return 2.55+.35*(1-min(abs(x+1),abs(y-1))/.95)
def roof_under(x,y):return 2.43
cells={(i,j)for i in range(4)for j in range(3)if i<2 or j>0}
sheet_solid('WholeLShapedGroundedPassageFloor',[-1.8,-1,-.2,1,1.8],[-1.8,.2,1,1.8],cells,lambda x,y:0,lambda x,y:.12,0)
sheet_solid('ContinuousValleyAndTurningRidgeRoof',[-1.95,-1,-.05,1,1.95],[-1.95,.05,1,1.95],cells,roof_under,roof_top,2)
POSTS=[(-1.65,-1.65),(-.35,-1.65),(-.35,.35),(1.65,.35),(1.65,1.65),(-1.65,1.65)]
for k,(x,y)in enumerate(POSTS):sheet_solid('FullFlatHeadTimberPost_'+str(k+1),[x-.085,x+.085],[y-.085,y+.085],{(0,0)},lambda x,y:.12,roof_under,1)
# Six complete edge headers, including the two open-end portal headers.
for k,((x0,y0),(x1,y1))in enumerate(zip(POSTS,POSTS[1:]+POSTS[:1])):
 if x0==x1:xs=[x0-.075,x0+.075];ys=sorted(set([min(y0,y1),max(y0,y1)]+[c for c in [.05,1]if min(y0,y1)<c<max(y0,y1)]))
 else:ys=[y0-.075,y0+.075];xs=sorted(set([min(x0,x1),max(x0,x1)]+[c for c in [-1,-.05]if min(x0,x1)<c<max(x0,x1)]))
 sheet_solid('CompleteFlatBearingHeader_'+str(k+1),xs,ys,{(i,j)for i in range(len(xs)-1)for j in range(len(ys)-1)},lambda x,y:2.31,roof_under,1)
PALETTE=[('GroundedWarmStone',(.45,.42,.34,1),.94,0),('DeepTimberPostsAndHeaders',(.30,.18,.085,1),.86,0),('MatteClayTurningRoof',(.47,.22,.12,1),.93,0)]
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
focus=Vector((0,0,1.35))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=6.10;aim(cam,(6,-8,5.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/village/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'modular','assetKind':'modular','theme':'village','style':'S01-clean-geometric','title':'Continuous Elbow Roofed Timber Passage','description':'One newly authored complete static village covered-passage module. A grounded full L-shaped stone floor turns between two perpendicular open end portals. Six complete timber posts with complete flat bearing heads and six whole edge headers support a single continuous solid clay-coloured elbow roof with a full flat soffit, two pitched upper ridge directions and an inner valley. The entire route and both mouths remain open, with no wall filling the elbow. Roof, ground slab and each post/header are closed editable meshes; no old canopy/house/wall mesh is imported, cropped or duplicated. This is an entire dogleg passage, not a short single-slope entrance canopy or a cantilever bus shelter, and not a new scene made by repeating those assets. Three constant opaque PBR materials; no texture, ornaments, extra furniture or copied building shell. Static illustrative architecture only, no structural load, weatherproofing, drainage, canonical construction, navigability, accessibility, installation or safety claim. One modular model and zero scenes.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
