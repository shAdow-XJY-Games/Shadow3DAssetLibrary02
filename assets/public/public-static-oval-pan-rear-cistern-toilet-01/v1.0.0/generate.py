from pathlib import Path
import json,hashlib,sys
OUT=Path(__file__).resolve().parent
ASSET='public-static-oval-pan-rear-cistern-toilet-01'
import math,collections
N=32
# (rx, ry, centreY, z, maximumY): full rings with a broad flat rear shelf.
PROFILE=[(0,0,.04,0,None),(.15,.235,.04,0,None),(.17,.25,.04,.045,None),(.135,.19,.02,.10,None),(.095,.13,.015,.22,None),(.16,.23,-.035,.28,None),(.23,.35,-.07,.35,.23),(.27,.40,-.07,.445,.23),(.27,.40,-.07,.46,.23),(.23,.34,-.07,.46,.14),(.205,.29,-.07,.39,.14),(.135,.19,-.055,.315,None),(.065,.09,-.025,.285,None),(0,0,-.025,.285,None)]
def ring(rx,ry,cy,z,clip=None):
 return [(rx*math.cos(2*math.pi*i/N),min(cy+ry*math.sin(2*math.pi*i/N),clip)if clip is not None else cy+ry*math.sin(2*math.pi*i/N),z)for i in range(N)]
def surface(profile,closed=False):
 v=[];rs=[]
 for rx,ry,cy,z,clip in profile:
  pts=[(0,cy,z)]if rx==0 else ring(rx,ry,cy,z,clip);rs.append(list(range(len(v),len(v)+len(pts))));v.extend(pts)
 f=[]
 pairs=list(zip(rs,rs[1:]))+([(rs[-1],rs[0])]if closed else [])
 for a,b in pairs:
  for i in range(N):
   j=(i+1)%N
   if len(a)==1:f.append((a[0],b[j],b[i]))
   elif len(b)==1:f.append((a[i],a[j],b[0]))
   else:f.extend([(a[i],a[j],b[j]),(a[i],b[j],b[i])])
 return v,f
G={}
v,f=surface(PROFILE);G['IntegralGroundedCeramicPan']=(v,f,0)
seat=[(.27,.40,-.07,.46,.15),(.27,.40,-.07,.488,.15),(.225,.335,-.07,.488,.105),(.225,.335,-.07,.46,.105)]
v,f=surface(seat,True);G['WholeOpenSeatRing']=(v,f,1)
# A single stepped cistern: broad upper tank and a narrower foot on the full rear ceramic shelf.
def tank():
 rings=[(-.115,.115,.16,.22,.46),(-.115,.115,.16,.22,.49),(-.19,.19,.16,.34,.51),(-.19,.19,.16,.34,.82)]
 v=[]
 for x0,x1,y0,y1,z in rings:v.extend([(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z)])
 f=[(0,2,1),(0,3,2)]
 for k in range(len(rings)-1):
  for i in range(4):
   j=(i+1)%4;a=k*4+i;b=k*4+j;c=(k+1)*4+j;d=(k+1)*4+i;f.extend([(a,b,c),(a,c,d)])
 k=12;f.extend([(k,k+1,k+2),(k,k+2,k+3)]);return v,f
v,f=tank();G['RearCisternWithIntegralFoot']=(v,f,0)
v,f=surface([(0,0,.25,.82,None),(.025,.025,.25,.82,None),(.025,.025,.25,.829,None),(0,0,.25,.829,None)]);G['FixedTopFlushButton']=(v,f,2)
# Whole occupied horizontal bounds, not nominal rings, determine the common origin.
vv=[p for v,f,m in G.values()for p in v];shift=tuple(-(min(p[k]for p in vv)+max(p[k]for p in vv))/2 if k<2 else 0 for k in range(3))
G={n:([(p[0]+shift[0],p[1]+shift[1],p[2])for p in v],f,m)for n,(v,f,m)in G.items()}

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
for name,color,rough in [('Ceramic_WarmWhite',(.74,.72,.66,1),.34),('Seat_OffWhite',(.62,.61,.57,1),.44),('Button_SatinSteel',(.32,.35,.36,1),.32)]:
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
parts=[x for x in scene.objects if x.type=='MESH'];assert len(parts)==4
view='thumbnail'
if '--view' in sys.argv:view=sys.argv[sys.argv.index('--view')+1]
assert view in ['qa-front','thumbnail']
scene.cycles.samples=16 if view=='qa-front' else 128
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.28,.28,.28,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
focus=Vector((0,0,.42))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.3;aim(cam,(3,-4,2.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/public/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'public','style':'S01-clean-geometric','title':'Static Pedestal Bowl and Rear Cistern Toilet','description':'Original static public-restroom toilet appearance: a continuous grounded ceramic foot and curved neck rise into a genuinely recessed D-shaped oval pan, with a thick open seat ring, supported rear cistern and fixed top button. No water, waste, plumbing, flushing, drainage, hygiene, accessibility, human-fit, installation or safety-performance claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
