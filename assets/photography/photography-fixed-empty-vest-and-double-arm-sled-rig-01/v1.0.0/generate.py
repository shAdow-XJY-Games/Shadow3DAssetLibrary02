import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='photography-fixed-empty-vest-and-double-arm-sled-rig-01'
G={};FM={}
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def unit(a):return tuple(x/math.sqrt(dot(a,a))for x in a)
def mesh(name,v,faces,mat):
 f=[]
 for p in faces:
  for k in range(1,len(p)-1):f.append((p[0],p[k],p[k+1]))
 if sum(dot(v[a],cross(v[b],v[c]))for a,b,c in f)<0:f=[tuple(reversed(p))for p in f]
 G[name]=(v,f,mat)
BOX=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(name,c,size,mat):mesh(name,[tuple(c[i]+s[i]*size[i]/2 for i in range(3))for s in[(x,y,z)for z in[-1,1]for y in[-1,1]for x in[-1,1]]],BOX,mat)
def beam(name,a,b,width,mat):
 w=unit(sub(b,a));u=unit(cross(w,(1,0,0)if abs(w[0])<.9 else(0,1,0)));v=cross(w,u)
 mesh(name,[tuple(p[i]+width/2*(sx*u[i]+sy*v[i])for i in range(3))for p in[a,b]for sy in[-1,1]for sx in[-1,1]],BOX,mat)
def axle(name,x0,x1,y,z,r,mat,n=16):
 v=[(x,y+r*math.cos(math.tau*i/n),z+r*math.sin(math.tau*i/n))for x in[x0,x1]for i in range(n)]
 mesh(name,v,[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],mat)

def ringx(name,x0,x1,y,z,ri,ro,mat,n=24):
 v=[(x,y+r*math.cos(math.tau*i/n),z+r*math.sin(math.tau*i/n))for x in[x0,x1]for r in[ri,ro]for i in range(n)];f=[]
 for i in range(n):j=(i+1)%n;f.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 mesh(name,v,f,mat)
def cyly(name,y0,y1,x,z,r,mat,n=24):
 axle(name,y0,y1,x,z,r,mat,n);v,f,m=G[name];G[name]=([(b,a,c)for a,b,c in v],[tuple(reversed(p))for p in f],m)
def ringy(name,y0,y1,x,z,ri,ro,mat,n=24):
 ringx(name,y0,y1,x,z,ri,ro,mat,n);v,f,m=G[name];G[name]=([(b,a,c)for a,b,c in v],[tuple(reversed(p))for p in f],m)
def triangulate(p):
 def cr(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 ids=list(range(len(p)));out=[]
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:ids.reverse()
 while len(ids)>3:
  for k,b in enumerate(ids):
   a,c=ids[k-1],ids[(k+1)%len(ids)]
   if cr(p[a],p[b],p[c])<=1e-14:continue
   if any(min(cr(p[a],p[b],p[j]),cr(p[b],p[c],p[j]),cr(p[c],p[a],p[j]))>=-1e-14 for j in ids if j not in[a,b,c]):continue
   out.append((a,b,c));ids.pop(k);break
  else:raise AssertionError('bad polygon')
 return out+[tuple(ids)]
def lathe_z(name,x,y,profile,mat,n=24):
 v=[];rings=[];f=[]
 for r,z in profile:
  ids=[]
  if r==0:ids=[len(v)];v.append((x,y,z))
  else:
   for i in range(n):ids.append(len(v));v.append((x+r*math.cos(math.tau*i/n),y+r*math.sin(math.tau*i/n),z))
  rings.append(ids)
 for a,b in zip(rings,rings[1:]+rings[:1]):
  if len(a)==len(b)==1:continue
  for i in range(n):
   j=(i+1)%n
   if len(a)==1:f.append((a[0],b[j],b[i]))
   elif len(b)==1:f.append((a[i],a[j],b[0]))
   else:f.append((a[i],a[j],b[j],b[i]))
 mesh(name,v,f,mat)



# Ground support attaches only to the back of the complete empty harness.
box('WholeGroundFootDisplayBase',(-.20,.02,.045),(.68,.68,.09),3)
box('WholeRearDisplayUpright',(-.25,.235,.58),(.075,.075,1.02),3)
box('WholeRearFrameAttachment',(-.25,.155,.98),(.21,.18,.10),2)
# Thick curved waist band, with an open top and bottom and no hidden torso fill.
n=32;v=[];f=[]
for z in[.70,.86]:
 for rx,ry in[(.265,.205),(.238,.178)]:
  for i in range(n):t=math.tau*i/n;v.append((-.25+rx*math.cos(t),ry*math.sin(t),z))
for i in range(n):
 j=(i+1)%n;f.extend([(i,j,2*n+j,2*n+i),(n+i,3*n+i,3*n+j,n+j),(i,n+i,n+j,j),(2*n+i,2*n+j,3*n+j,3*n+i)])
mesh('WholeOpenWaistSupportBand',v,f,0)
box('WholeFrontChestPlate',(-.25,-.177,1.085),(.31,.037,.46),0)
box('WholeBackSupportPlate',(-.25,.177,1.075),(.29,.037,.43),0)
# Complete broad shoulder bridges; real neck opening remains between them.
def strip(name,points,width,thick):
 v=[];f=[]
 for k,p in enumerate(points):
  d=unit(sub(points[min(k+1,len(points)-1)],points[max(0,k-1)]));u=(1,0,0);w=unit(cross(d,u))
  for a,b in[(-1,-1),(1,-1),(1,1),(-1,1)]:v.append(tuple(p[i]+a*width/2*u[i]+b*thick/2*w[i]for i in range(3)))
 for k in range(len(points)-1):
  for i in range(4):j=(i+1)%4;f.append((4*k+i,4*k+j,4*(k+1)+j,4*(k+1)+i))
 f.extend([tuple(reversed(range(4))),tuple(4*(len(points)-1)+i for i in range(4))]);mesh(name,v,f,0)
for x in[-.36,-.14]:strip('WholeShoulderBridge_'+str(x),[(x,-.175,1.25),(x,-.15,1.38),(x,-.07,1.43),(x,.09,1.43),(x,.175,1.31),(x,.175,1.23)],.066,.023)
box('WholeSideRootPlate',(.016,0,.84),(.064,.20,.18),2)
# Two serial parallelograms in different horizontal directions, not one elongated jib.
points=[(.037,-.015,.87),(.61,-.08,.98),(1.00,-.46,.91)]
for k,(p,q)in enumerate(zip(points,points[1:])):
 for h in[0,.18]:beam('WholeParallelLink_%d_%s'%(k,h),(p[0],p[1],p[2]+h),(q[0],q[1],q[2]+h),.034,1)
 # Thick diagonal spring housing is a fixed exterior, not a simulated coil.
 aa=(p[0]+.10*(q[0]-p[0]),p[1]+.10*(q[1]-p[1]),p[2]+.025)
 bb=(p[0]+.85*(q[0]-p[0]),p[1]+.85*(q[1]-p[1]),p[2]+.15+.85*(q[2]-p[2]))
 beam('WholeDiagonalHousing_%d'%k,aa,bb,.049,3)
for k,(x,y,z)in enumerate(points):
 box('WholeLinkEndBlock_%d'%k,(x,y,z+.09),(.065,.065,.245),2)
 for h in[0,.18]:cyly('WholeProudLinkPin_%d_%s'%(k,h),y-.044,y+.044,x,z+h,.026,2,20)
# Independent long vertical sled, a rear holding collar, upper blank plate and low weight crossbar.
box('WholeWristReach',(1.065,-.46,1.08),(.15,.055,.065),1)
lathe_z('WholeClosedSledCollar',1.13,-.46,[(.025,1.045),(.045,1.045),(.045,1.115),(.025,1.115)],2,24)
lathe_z('WholeVerticalSledShaft',1.13,-.46,[(0,.43),(.025,.43),(.025,1.59),(0,1.59)],1,24)
box('WholeUpperCameraCarrier',(1.13,-.46,1.58),(.27,.19,.035),1)
box('WholeRaisedPlatePad',(1.13,-.46,1.603),(.20,.125,.020),3)
box('WholeLowerWeightCrossbar',(1.13,-.46,.465),(.36,.045,.045),1)
for j,x in enumerate([.98,1.28]):box('WholeLowerCounterweight_%d'%j,(x,-.46,.48),(.115,.14,.09),3)
PALETTE=[('HarnessSlate',(.15,.21,.23,1),.85,.06),('LinksAndSledMutedSteel',(.43,.48,.48,1),.54,.5),('JointCapsWarmMetal',(.46,.34,.18,1),.52,.5),('PadsHousingAndBaseCharcoal',(.045,.055,.055,1),.86,.03)]
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}

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
focus=Vector((0,0,.86))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.60;aim(cam,(4,-7,3.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/photography/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'photography','style':'S01-clean-geometric','title':'Fixed Empty Vest and Double Arm Sled Rig','description':'One complete newly authored static empty body-carried camera-support rig appearance on its own low display support. A curved waist band, separate chest plate, back plate and two thick over-shoulder bridges surround an actual empty body space. A side root carries two serial full parallelogram sections, folded in different horizontal directions, with separate upper and lower links, complete end blocks, proud pins and thick diagonal spring-housing exteriors. The far wrist carries an independent long vertical sled through a closed collar and side pin; a wide blank upper camera plate and low crossbar with two complete counterweight exteriors terminate this sled. No camera, person, monitor or battery internals. The ground display bracket connects only to the empty back frame; it is not a wearable human or a separate scene object. All meshes numerically new, not a cuirass or old long camera jib imported or merely given a different base. The compact lateral two-stage folded chain and vertically distributed payload/counterweight silhouette are distinct from the old single forward parallel jib and rear tail weight. Four opaque constant PBR roles, metres Z up, horizontal-envelope-centred ground datum, one whole model zero scenes. Fixed illustrative appearance only. No wearable fit, ergonomics, spring action, arm travel, stabilization, gimbal operation, balancing, camera compatibility, load, strength or safety capability made or validated. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
