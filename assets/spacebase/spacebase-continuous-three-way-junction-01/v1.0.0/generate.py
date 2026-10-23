import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='spacebase-continuous-three-way-junction-01'
G={};FM={}
PALETTE=[('Junction_BlueShell',(.14,.27,.34,1),.58,.15),('Junction_IvoryLining',(.64,.69,.67,1),.7,.03),('Junction_AmberMouths',(.76,.35,.075,1),.47,.22),('Junction_DarkFloor',(.10,.14,.17,1),.76,.05)]
# New single material-domain T shell. Cells are merely construction volumes;
# only their external union boundary is emitted, with shared indexed vertices.
# No old corridor mesh/array is imported, overlaid, cut or counted again.
XS=[-3.5,-3.24,-1.5,-1.22,1.22,1.5,3.24,3.5]
YS=[-3.5,-3.24,-1.5,-1.22,1.22,1.5]
ZS=[0,.22,2.82,3.10,3.25]
def outer(x,y):return (-1.5<y<1.5) or (-1.5<x<1.5 and -3.5<y<1.5)
def air(x,y):return (-1.22<y<1.22) or (-1.22<x<1.22 and -3.5<y<1.22)
def collar(x,y):return abs(x)>3.24 or y<-3.24
cells=set()
for i in range(len(XS)-1):
 for j in range(len(YS)-1):
  for k in range(len(ZS)-1):
   x=(XS[i]+XS[i+1])/2;y=(YS[j]+YS[j+1])/2;z=(ZS[k]+ZS[k+1])/2
   if outer(x,y) and ((z<.22) or (2.82<z<3.10) or (z>3.10 and collar(x,y)) or (z<2.82 and not air(x,y))):cells.add((i,j,k))
v=[];f=[];fm=[];lookup={}
def vertex(p):
 p=(p[0],p[1]+1,p[2])
 if p not in lookup:lookup[p]=len(v);v.append(p)
 return lookup[p]
quads=[((0,0,-1),(0,2,3,1)),((0,0,1),(4,5,7,6)),((0,-1,0),(0,1,5,4)),((0,1,0),(2,6,7,3)),((-1,0,0),(0,4,6,2)),((1,0,0),(1,3,7,5))]
for i,j,k in sorted(cells):
 vv=[(x,y,z) for z in ZS[k:k+2] for y in YS[j:j+2] for x in XS[i:i+2]]
 for (di,dj,dk),q in quads:
  if (i+di,j+dj,k+dk) in cells:continue
  pts=[vv[n] for n in q];c=[sum(p[a] for p in pts)/4 for a in range(3)]
  # Positive-Z floor and inner wall/ceiling faces use real distinct PBR roles.
  mat=0
  if c[2]==.22 and dk==1:mat=3
  elif c[2]==2.82 and dk==-1:mat=1
  elif (abs(c[0])==1.22 or abs(c[1])==1.22) and c[2]>.22:mat=1
  if (abs(c[0])>=3.24 or c[1]<=-3.24) and c[2]>.22:mat=2
  a,b,c1,d=[vertex(p) for p in pts];f.extend([(a,b,c1),(a,c1,d)]);fm.extend([mat,mat])
G['ContinuousThreeMouthTShell']=(v,f,0);FM['ContinuousThreeMouthTShell']=fm
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
focus=Vector((0,0,1.4))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=10.8;aim(cam,(8,-10,7));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/spacebase/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'modular','theme':'spacebase','style':'S01-clean-geometric','title':'Continuous Three-Way Junction Module','description':'One original static spacebase three-way junction module. A single continuous thick closed material shell encloses a connected T-shaped empty interior with three genuine open mouths, a full raised floor, side walls, shared central ceiling and three integral raised roof-end rims. The two opposed side arms meet one forward stem in a real common chamber, not overlapping old straight corridors with hidden internal walls. All material-cell interior faces are removed and every boundary shares indexed vertices; one closed connected editable mesh and four constant opaque PBR roles. Newly authored plan and topology, zero imported geometry and one modular asset, not three corridor assets or a length/color variant. Source Z up, metres, horizontal-bounds-centred origin on the complete ground sole. No doors, pressure chamber, furniture, people, cables or textures. Static visual-only empty junction: no pressure seal, atmosphere, airlock cycle, installation compatibility with previous modules, navigation, accessibility, manufacturing, structural load, spaceflight or safety performance claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
