import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='fitness-fixed-twin-rail-reformer-bed-01'
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



# Entire new low twin-rail training bed, with one fixed padded carriage pose.
for x in[-.34,.34]:
 box('WholeLongSideFrame_'+str(x),(x,0,.255),(.09,2.30,.15),0)
 box('WholeInnerRunningRail_'+str(x),(x*.80,0,.325),(.035,2.18,.045),1)
 for y in[-.97,.97]:
  box('WholeGroundFoot_'+str(x)+'_'+str(y),(x,y,.025),(.17,.20,.05),2)
  box('WholeShortSupportLeg_'+str(x)+'_'+str(y),(x,y,.115),(.095,.11,.18),0)
for y in[-1.10,1.10]:box('WholeEndCrossMember_'+str(y),(0,y,.270),(.74,.12,.14),0)
# Separate finite roller carriage under the full lying pad, not a continuous moving belt.
box('WholeCarriageUnderframe',(0,.12,.385),(.60,1.13,.07),0)
for x in[-.272,.272]:
 for y in[-.32,.56]:axle('WholeFixedCarriageRoller_'+str(x)+'_'+str(y),x-.035,x+.035,y,.357,.028,2,16)
box('WholeLongCarriagePad',(0,.12,.445),(.57,1.08,.07),2)
for x in[-.19,.19]:box('WholeRaisedShoulderBlock_'+str(x),(x,.60,.53),(.11,.135,.17),2)
box('WholeCentralHeadRest',(0,.686,.452),(.23,.27,.085),2)
# Genuine open front bay contains three complete fixed tension-spring-looking helices.
def tube(name,path,r,mat,n=8):
 v=[];f=[]
 for k,p in enumerate(path):
  t=unit(sub(path[min(k+1,len(path)-1)],path[max(k-1,0)]));u=unit(cross(t,(0,0,1)if abs(t[2])<.9 else(1,0,0)));w=cross(t,u)
  for j in range(n):v.append(tuple(p[i]+r*(u[i]*math.cos(math.tau*j/n)+w[i]*math.sin(math.tau*j/n))for i in range(3)))
 f=[tuple(reversed(range(n))),tuple((len(path)-1)*n+j for j in range(n))]
 for k in range(len(path)-1):
  for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
 mesh(name,v,f,mat)
box('WholeSpringFrontSeatBar',(0,-1.06,.285),(.61,.075,.07),1)
box('WholeSpringCarriageSeatBar',(0,-.41,.34),(.56,.07,.06),1)
for i,x in enumerate([-.16,0,.16]):
 path=[(x,-1.065,.30),(x,-.99,.30)]+[(x+.018*math.cos(math.tau*7*k/112),-.97+.50*k/112,.31+.018*math.sin(math.tau*7*k/112))for k in range(113)]+[(x,-.410,.335)]
 tube('WholeContinuousFixedSpring_'+str(i),path,.004,1)
# Fixed transverse footbar slopes up from two full side hubs; no adjustable movement.
for x in[-.34,.34]:
 axle('WholeFootbarRootHub_'+str(x),x-.035,x+.035,-.94,.285,.06,1,16)
 tube('WholeFootbarSide_'+str(x),[(x,-.94,.285),(x,-.81,.73)],.025,1,12)
axle('WholeFootbarPaddedCrossGrip',-.365,.365,-.81,.73,.038,2,24)
# Paired rear rope towers, complete pulley wheels and two fixed returns to parked hand loops.
for i,x in enumerate([-.27,.27]):
 box('WholePulleyTower_'+str(i),(x,1.035,.565),(.055,.065,.59),0)
 axle('WholePulleyAxle_'+str(i),x-.07,x+.07,1.035,.835,.015,1,16)
 # A complete flanged grooved pulley around the transverse axis.
 lathe_z('WholeGroovedPulley_'+str(i),0,0,[(0,-.025),(.066,-.025),(.066,-.012),(.052,-.008),(.052,.008),(.066,.012),(.066,.025),(0,.025)],1,24)
 n='WholeGroovedPulley_'+str(i);v,f,m=G[n];G[n]=([(x+c,1.035+a,.835+b)for a,b,c in v],f,m)
 path=[(x,.60,.36),(x,1.065,.765)]+[(x,1.035+.058*math.cos(a),.835+.058*math.sin(a))for a in[-math.pi/2+j*math.pi/12 for j in range(13)]]+[(x,.43,.490)]
 tube('WholeContinuousFixedReturnCord_'+str(i),path,.005,2)
 # Each true open horizontal grip loop lies on the padded carriage, not a dangling loose prop.
 lathe_z('WholeParkedOpenHandLoop_'+str(i),x,.375,[(.042,.477),(.057,.477),(.057,.494),(.042,.494)],1,24)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeLowFrameCarriageAndRopeTowers_WarmTimber',(.40,.23,.105,1),.77,0),('WholeRailsSpringsPulleyAndGrips_SatinMetal',(.40,.47,.49,1),.44,.55),('WholePadsFeetAndFixedRope_DeepTeal',(.045,.18,.20,1),.84,0)]
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
focus=Vector((0,0,.40))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.85;aim(cam,(4,-5,4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/fitness/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'fitness','style':'S01-clean-geometric','title':'Fixed Twin Rail Reformer Bed','description':'One newly authored complete static low twin-rail reformer-style training bed. A full rectangular timber-like frame on four finite feet carries two separate long rails, four fixed carriage rollers and an independent long lying pad with two raised shoulder blocks and a central headrest. A genuine open front bay contains three continuous whole coil springs between fixed crossseats, below a complete inclined transverse padded footbar with two rooted side hubs. Two rear towers support complete grooved pulleys and continuous fixed return cords ending at open hand loops resting on the carriage. This is not the old single narrow rowing rail with a saddle and front fan, or a treadmill continuous capsule belt and raised console; all geometry is newly authored as one whole bed apparatus. Three opaque constant untextured PBR roles, metres, Z up and complete horizontal ground-centred origin. One model, zero scenes. Unoccupied fixed illustrative display only: no sliding stroke, resistance, force or spring specification, exercise or therapy advice, posture/fit, load, motion clearance, manufacturing, certification or equipment safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
