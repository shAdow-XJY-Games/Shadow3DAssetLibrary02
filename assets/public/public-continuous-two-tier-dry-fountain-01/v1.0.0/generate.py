from pathlib import Path
import json,hashlib,sys
OUT=Path(__file__).resolve().parent
ASSET='public-continuous-two-tier-dry-fountain-01'
"""Original dry two-basin courtyard fountain shell, numeric draft only."""
import math,collections
PROFILE=[(0,0),(.36,0),(.40,.055),(.40,.105),(.32,.15),(.21,.18),(.16,.27),(.12,.47),(.25,.49),(.49,.53),(.71,.61),(.84,.75),(.86,.81),(.84,.85),(.79,.85),(.77,.78),(.65,.66),(.44,.59),(.23,.56),(.12,.56),(.105,.89),(.15,1.00),(.28,1.04),(.39,1.12),(.45,1.23),(.46,1.28),(.44,1.31),(.40,1.31),(.385,1.25),(.33,1.16),(.24,1.10),(.13,1.075),(.085,1.075),(.07,1.40),(.105,1.45),(.07,1.52),(0,1.60)]
def build(n=32):
 v=[];rings=[]
 for r,z in PROFILE:
  ids=[]
  for i in range(1 if r==0 else n):
   ids.append(len(v));v.append((r*math.cos(math.tau*i/n),r*math.sin(math.tau*i/n),z))
  rings.append(ids)
 f=[];materials=[]
 for j,(a,b) in enumerate(zip(rings,rings[1:])):
  mat=1 if j in (1,2,11,12,13,24,25,26) else 0
  for i in range(n):
   k=(i+1)%n
   if len(a)==1:rows=[(a[0],b[k],b[i])]
   elif len(b)==1:rows=[(a[i],a[k],b[0])]
   else:rows=[(a[i],a[k],b[k]),(a[i],b[k],b[i])]
   f.extend(rows);materials.extend([mat]*len(rows))
 return v,f,materials

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
for name,color,rough in [('PaleLimestone',(.57,.53,.44,1),.78),('WarmCutStoneRims',(.39,.34,.26,1),.72)]:
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=0;materials.append(m)
v,f,mi=build();me=bpy.data.meshes.new('ContinuousFountainMesh');me.from_pydata(v,[],f);me.update()
o=bpy.data.objects.new('ContinuousTwoTierDryFountain',me);scene.collection.objects.link(o)
for m in materials:me.materials.append(m)
for p,m in zip(me.polygons,mi):p.material_index=m;p.use_smooth=False
bpy.context.view_layer.objects.active=o;o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
if '--geometry-only' in sys.argv:
 print('GEOMETRY_READY',ASSET,len(f));sys.exit(0)
# Render the actual exported geometry, not an unexported proxy.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
parts=[x for x in scene.objects if x.type=='MESH'];assert len(parts)==1
view='thumbnail'
if '--view' in sys.argv:view=sys.argv[sys.argv.index('--view')+1]
assert view in ['qa-front','thumbnail']
scene.cycles.samples=16 if view=='qa-front' else 128
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.28,.28,.28,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
focus=Vector((0,0,.78))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.65;aim(cam,(3,-4,3.6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/public/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'public','style':'S01-clean-geometric','title':'Continuous Two-tier Dry Courtyard Fountain','description':'Original continuous thick stone fountain shell: stepped ground foot, waisted central column, broad lower open basin, smaller upper open basin and integral stone finial. Both annular bowls are genuinely recessed around the continuous central column. Dry static courtyard appearance only; no water, jets, pump, pipes, drain holes, hydraulic, installation or safety performance claimed.','bounds':{'x':1.72,'y':1.72,'z':1.6,'unit':'m'},'triangles':len(f),'materials':2,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
