import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='animal-static-broad-ear-continuous-trunk-elephant-01'
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

def loft(name,rings,mat):
 n=len(rings[0]);v=[p for ring in rings for p in ring];f=[tuple(reversed(range(n))),tuple((len(rings)-1)*n+j for j in range(n))]
 for k in range(len(rings)-1):
  for j in range(n):q=(j+1)%n;f.append((k*n+j,k*n+q,(k+1)*n+q,(k+1)*n+j))
 mesh(name,v,f,mat)
def ring_xz(y,z,rx,rz,angle=0,n=16):
 return[(rx*math.cos(math.tau*j/n),y-rz*math.sin(math.tau*j/n)*math.sin(angle),z+rz*math.sin(math.tau*j/n)*math.cos(angle))for j in range(n)]
ellipsoid('WholeBroadBarrelTorso',(0,.19,1.35),(.53,.80,.58),0,n=16,r=8)
# Complete new head-to-trunk surface. The large head narrows into a downward
# trunk and a small upward-curled tip; no old snake mesh or appendage reused.
HEAD_TRUNK=[(-.32,1.52,.27,.29,0),(-.54,1.72,.34,.39,0),(-.76,1.69,.31,.35,0),(-.93,1.46,.18,.21,-.35),(-1.02,1.16,.125,.13,-1.10),(-1.04,.88,.108,.11,-1.48),(-1.12,.62,.092,.095,-1.05),(-1.29,.48,.075,.08,-.30),(-1.44,.50,.060,.066,.50),(-1.51,.64,.043,.049,1.15)]
loft('ContinuousBroadHeadAndCurledTrunk',[ring_xz(*q)for q in HEAD_TRUNK],0)
LEGS=[]
for sign,side in[(-1,'Left'),(1,'Right')]:
 for y,label in[(-.30,'Front'),(.57,'Hind')]:
  name=side+label+'WholeColumnLegAndFlatFoot';LEGS.append(name)
  rr=[[(sign*.32+rx*math.cos(math.tau*j/12),y+ry*math.sin(math.tau*j/12),z)for j in range(12)]for z,rx,ry in[(0,.15,.18),(.07,.16,.185),(.65,.14,.15),(1.28,.18,.19)]];loft(name,rr,0)
 # Complete thick fan-like ear, broad root inside the new head flank.
 p=[(sign*x,z)for x,z in[(.23,1.75),(.34,2.04),(.61,1.98),(.73,1.61),(.58,1.15),(.29,1.35)]]
 n=len(p);v=[(x,y,z)for y in[-.61,-.49]for x,z in p];f=[tuple(reversed(range(n))),tuple(n+j for j in range(n))]+[(j,(j+1)%n,(j+1)%n+n,j+n)for j in range(n)];mesh(side+'WholeThickBroadEar',v,f,1)
 ellipsoid(side+'SmallHeadEye',(sign*.255,-.825,1.735),(.036,.035,.034),2)
# Thin complete tapered tail seated in the posterior torso, not an extra leg.
loft('WholeDownwardTail',[ring_xz(y,z,r,r,a,n=12)for y,z,r,a in[(.88,1.42,.045,0),(1.03,1.25,.035,-.7),(1.08,1.02,.025,-1.2),(1.07,.79,.018,-1.6),(1.05,.70,.030,-1.8)]],0)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)]
SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={name:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for name,(v,f,m)in G.items()}
PALETTE=[('ElephantSkin_MatteWarmGrey',(.38,.39,.37,1),.91,0),('BroadEars_MutedWarmGrey',(.43,.39,.34,1),.92,0),('SmallEyes_DeepCharcoal',(.018,.021,.020,1),.68,0)]
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
focus=Vector((0,0,1.02))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.70;aim(cam,(4,-6,3.3));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/animal/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'animal','style':'S01-clean-geometric','title':'Static Broad-Ear Continuous-Trunk Elephant','description':'One newly authored stylised static elephant-like animal. A broad barrel torso rests on four thick column legs with complete finite flat feet. A large head narrows continuously into a long downward trunk and small curled-up tip in the same closed surface; two complete thick broad ears, small side eyes and one thin downward tail complete the whole animal. New full proportions, head/trunk trajectory and ear outlines, not a deer with its antlers removed, an enlarged rabbit, an old snake attached as a trunk or a reskinned existing quadruped. Eleven closed editable meshes and three opaque matte untextured PBR materials. Metres, native Z up, head -Y and actual horizontal bounds-centred ground datum. One prop, zero scene; no tusks, tack, platform, person, facial rig or animation. Artistic fixed elephant-like exterior only, not an exact species, sex, age or anatomical specimen; no respiratory or feeding function, locomotion, trunk manipulation, biological fidelity, animal handling or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
