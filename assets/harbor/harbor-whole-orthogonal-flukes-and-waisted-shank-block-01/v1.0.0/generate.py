import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='harbor-whole-orthogonal-flukes-and-waisted-shank-block-01'
G={};FM={}
PALETTE=[('WholeCastBlockWarmMineral',(.50,.49,.43,1),.94,0)]
# Every perimeter is one complete chamfered convex section; shared ring vertices
# continue through both full orthogonal flukes and the integral waisted shank.
PROFILES=[(0,1.15,.32,.08),(.36,1.08,.32,.08),(.58,.30,.30,.06),(.95,.22,.22,.05),(1.42,.30,.30,.06),(1.64,.32,1.08,.08),(2.0,.32,1.15,.08)]
v=[];f=[]
for z,a,b,c in PROFILES:
 v +=[(x,y,z)for x,y in[(-a+c,-b),(a-c,-b),(a,-b+c),(a,b-c),(a-c,b),(-a+c,b),(-a,b-c),(-a,-b+c)]]
for k in range(len(PROFILES)-1):
 for i in range(8):j=(i+1)%8;a=8*k+i;b=8*k+j;c=8*(k+1)+j;d=8*(k+1)+i;f.extend([(a,b,c),(a,c,d)])
for i in range(1,7):f.extend([(0,i+1,i),(48,48+i,48+i+1)])
G['WholeOrthogonalEndFlukesAndIntegralWaistedShank']=(v,f,0);FM={n:[m]*len(f)for n,(v,f,m)in G.items()};ROOTS=list(G);SHIFT=(0,0,0)
GAPS=[]
for x in[-.80,-.55,.55,.80]:GAPS.append(dict(label='OpenSideAboveLowerFullFluke',origin_m=[x,-1.3,1.0],direction=[0,1,0],length_m=2.6))
for y in[-.80,-.55,.55,.80]:GAPS.append(dict(label='OpenSideBelowUpperFullFluke',origin_m=[-1.3,y,1.1],direction=[1,0,0],length_m=2.6))
for z in[.18,.95,1.82]:GAPS.append(dict(label='WholeSolidFlukeOrShankControl',origin_m=[-1.3,0,z],direction=[1,0,0],length_m=2.6,blocked=True))
CORE_POINTS=[(0,0,z)for z in[.18,.50,.70,.95,1.20,1.50,1.82]]
assert len(G)==1 and len(f)==108 and len(v)==56
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
focus=Vector((0,0,1.0))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.7;aim(cam,(6,-8,6) if view=='qa-front' else (-7,-10,6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/harbor/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'prop','theme':'harbor','style':'S01-clean-geometric','title':'Whole Orthogonal Flukes and Waisted Shank Block','description':'One newly authored complete fixed coastal-armour-block-inspired exterior. One broad lower transverse fluke, one visibly waisted central shank and one full upper transverse fluke oriented at right angles form a single continuous closed material mesh. Both complete flukes retain their full opposed ends and chamfered perimeter; their tapered shoulders flow through shared vertices into the complete middle shank. The lower fluke itself has one broad finite horizontal ground sole; there are no added feet or plinth. The upper fluke extends in the orthogonal plan direction, leaving true open exterior spaces around the narrower shank rather than four limbs radiating tetrahedrally from one small core. One continuous section-to-section manifold, not overlapping detached bars or a renamed old four-limb block. All 56 vertices and 108 triangles newly authored together, one opaque matte mineral PBR role, metre-style native Z up and horizontal whole-envelope centred ground datum. One independent original model zero scenes. Generic dolos-like visual vocabulary only with original artistic proportions and simplified integral shoulders, not a standard or engineered coastal protection unit. No wave dissipation, block interlock, coastal performance, strength, reinforcement, mass, load, lifting, casting, manufacture, placement, stability, maritime construction or public safety capability made or verified. No water, repeated blockfield, rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
