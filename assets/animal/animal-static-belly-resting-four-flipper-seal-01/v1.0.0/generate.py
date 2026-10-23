import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='animal-static-belly-resting-four-flipper-seal-01'
G={};FM={}
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def mesh(name,v,faces,mat):
 f=[]
 for p in faces:
  for k in range(1,len(p)-1):f.append((p[0],p[k],p[k+1]))
 if sum(dot(v[a],cross(v[b],v[c]))for a,b,c in f)<0:f=[tuple(reversed(p))for p in f]
 G[name]=(v,f,mat)
def round_body(name,stations,mat,n=16):
 v=[]
 for y,w,low,high in stations:
  for j in range(n):
   a=math.tau*j/n;h=(math.sin(a)+1)/2
   # A finite underside patch, not a single lowest vertex; head is raised.
   if h<.04:h=0
   v.append((w*math.cos(a),y,low+(high-low)*h))
 f=[tuple(reversed(range(n))),tuple((len(stations)-1)*n+j for j in range(n))]
 for k in range(len(stations)-1):
  for j in range(n):q=(j+1)%n;f.append((k*n+j,k*n+q,(k+1)*n+q,(k+1)*n+j))
 mesh(name,v,f,mat)
def ellipsoid(name,c,s,mat,n=12,r=6):
 v=[(c[0],c[1],c[2]+s[2])]
 for k in range(1,r):
  a=math.pi*k/r
  v.extend([(c[0]+s[0]*math.sin(a)*math.cos(math.tau*j/n),c[1]+s[1]*math.sin(a)*math.sin(math.tau*j/n),c[2]+s[2]*math.cos(a))for j in range(n)])
 v.append((c[0],c[1],c[2]-s[2]));f=[]
 for j in range(n):q=(j+1)%n;f.extend([(0,1+j,1+q),(len(v)-1,1+(r-2)*n+q,1+(r-2)*n+j)])
 for k in range(r-2):
  for j in range(n):q=(j+1)%n;f.append((1+k*n+j,1+(k+1)*n+j,1+(k+1)*n+q,1+k*n+q))
 mesh(name,v,f,mat)
def prism(name,outline,height,thickness,mat):
 # Convex full outline, fan from actual polygon centroid on each parallel skin.
 n=len(outline);cx=sum(x for x,y in outline)/n;cy=sum(y for x,y in outline)/n
 v=[(x,y,height(x,y)+off)for off in[-thickness/2,thickness/2]for x,y in outline]+[(cx,cy,height(cx,cy)-thickness/2),(cx,cy,height(cx,cy)+thickness/2)]
 f=[]
 for i in range(n):j=(i+1)%n;f.extend([(2*n,j,i),(2*n+1,n+i,n+j),(i,j,n+j,n+i)])
 mesh(name,v,f,mat)
STATIONS=[(-.95,.065,.48,.60),(-.86,.18,.40,.68),(-.72,.22,.34,.78),(-.55,.23,.22,.71),(-.30,.34,.06,.63),(0,.38,0,.56),(.30,.32,0,.43),(.58,.21,.02,.28),(.78,.10,.035,.16),(.88,.055,.05,.12)]
round_body('WholeRaisedHeadNeckAndTaperedRestingTorso',STATIONS,0)
for sign,label in[(-1,'Left'),(1,'Right')]:
 fore=[(sign*x,y)for x,y in[(.22,-.32),(.38,-.35),(.69,-.10),(.76,.04),(.69,.13),(.42,.04),(.24,-.12)]]
 prism(label+'CompleteSweptFrontFlipper',fore,lambda x,y:.24-.27*(abs(x)-.22),.035,0)
 rear=[(sign*x,y)for x,y in[(.025,.75),(.09,.76),(.32,1.10),(.31,1.24),(.19,1.26),(.06,1.04)]]
 prism(label+'CompleteSplayedHindFlipper',rear,lambda x,y:.10-.12*(y-.75),.035,0)
 ellipsoid(label+'SmallLateralEye',(sign*.178,-.785,.634),(.035,.031,.036),2)
 ellipsoid(label+'BluntMuzzleLobe',(sign*.058,-.93,.535),(.075,.065,.050),1)
ellipsoid('SmallBluntDarkNose',(0,-.983,.565),(.044,.030,.029),2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)]
SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('SealBody_MatteBlueGrey',(.30,.38,.40,1),.89,0),('Muzzle_WarmPaleGrey',(.54,.56,.51,1),.90,0),('EyesAndNose_Charcoal',(.018,.023,.022,1),.67,0)]
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
focus=Vector((0,0,.34))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.90;aim(cam,(4,-5,3.1));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/animal/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'animal','style':'S01-clean-geometric','title':'Static Belly-Resting Four-Flipper Seal','description':'One newly authored stylised resting seal exterior. A continuous blunt raised head and short neck flow into a thick broad belly and tapering rear torso; four distinct thick flattened flippers comprise two swept lateral foreflippers and a paired splayed rear set. The torso has a real finite low belly patch. Two small side eyes, two blunt muzzle lobes and a small dark nose complete the face. All body station proportions and flipper outlines are newly authored, not a fish given legs, recoloured ray, cropped rabbit or a modified old animal. Ten closed editable meshes, three opaque matte PBR materials, no texture, fur simulation, gill slit, dorsal fin, tail fluke, teeth or scene. Metres, native Z up, head -Y and actual horizontal bounds-centred ground datum. One complete static prop and zero scenes. Illustrative seal-like shape only, not exact species identification, anatomical specimen, rig, breathing, locomotion, swimming, buoyancy, biological fidelity, handling or animal safety guidance.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
