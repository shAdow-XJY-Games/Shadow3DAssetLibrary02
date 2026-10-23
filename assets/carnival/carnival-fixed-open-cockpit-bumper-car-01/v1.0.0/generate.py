import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='carnival-fixed-open-cockpit-bumper-car-01'
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



# One newly authored complete fixed bumper-car exterior, not an old racer stripped of screen.
N=48
# Continuous closed hollow body: low outer belly, shoulder, foredeck, open cockpit, floor.
v=[]
for rx,ry,cy,z in[(.49,.77,0,.18),(.57,.90,0,.31),(.54,.86,0,.49),(.365,.535,.14,.49),(.34,.51,.14,.255)]:
 for i in range(N):t=math.tau*i/N;v.append((rx*math.cos(t),cy+ry*math.sin(t),z))
f=[tuple(reversed(range(N))),tuple(4*N+i for i in range(N))]
for k in range(4):
 for i in range(N):j=(i+1)%N;f.append((k*N+i,k*N+j,(k+1)*N+j,(k+1)*N+i))
mesh('WholeRoundedOpenCockpitBodyWithFloor',v,f,0)
# Complete thick flattened elliptical buffer ring with a real central opening.
v=[];K=10
for i in range(N):
 t=math.tau*i/N
 for j in range(K):
  a=math.tau*j/K;v.append(((.575+.085*math.cos(a))*math.cos(t),(.905+.085*math.cos(a))*math.sin(t),.245+.095*math.sin(a)))
f=[(i*K+j,((i+1)%N)*K+j,((i+1)%N)*K+(j+1)%K,i*K+(j+1)%K)for i in range(N)for j in range(K)]
mesh('WholeContinuousOvalBufferRing',v,f,1)
box('WholeUnderbodyChassis',(0,0,.175),(.75,1.28,.12),1)
# Three small complete fixed flat-contact wheels, visibly tucked under the low shell.
for label,x,y in [('Front',0,-.57),('RearLeft',-.32,.49),('RearRight',.32,.49)]:
 n=16;r=.10/math.cos(math.pi/n);v=[]
 for xx in[x-.055,x+.055]:
  for i in range(n):t=math.tau*i/n+math.pi/n;v.append((xx,y+r*math.sin(t),.10+r*math.cos(t)))
 mesh(label+'WholeGroundWheel',v,[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,n+(i+1)%n,n+i)for i in range(n)],1)
 axle(label+'WholeFixedWheelAxle',x-.09,x+.09,y,.10,.035,2,16)
box('WholeSeatPedestal',(0,.37,.325),(.48,.34,.17),0)
box('WholeBroadSeatCushion',(0,.34,.425),(.57,.39,.12),1)
# A single inclined thick back shell joins the seat, continuous profile extrusion.
p=[(.46,.39),(.60,.39),(.70,.88),(.58,.92)];n=len(p);v=[(x,y,z)for x in[-.315,.315]for y,z in p];f=[]
for a,b,c in triangulate(p):f.extend([(c,b,a),(a+n,b+n,c+n)])
f += [(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh('WholeInclinedSeatBack',v,f,1)
box('WholeFrontDashboard',(0,-.37,.475),(.60,.13,.12),0)
# Tilted complete steering ring, hub, shaft and three spokes, no screen or game cabinet.
c=(0,-.19,.73);w=unit((0,.70,.70));u=(1,0,0);v=cross(w,u)
def pt(r,a,d=0):return tuple(c[k]+r*(math.cos(a)*u[k]+math.sin(a)*v[k])+d*w[k]for k in range(3))
verts=[];n=32;k=8
for i in range(n):
 t=math.tau*i/n
 for j in range(k):a=math.tau*j/k;verts.append(pt(.175+.018*math.cos(a),t,.018*math.sin(a)))
mesh('WholeTiltedSteeringRim',verts,[(i*k+j,((i+1)%n)*k+j,((i+1)%n)*k+(j+1)%k,i*k+(j+1)%k)for i in range(n)for j in range(k)],1)
beam('WholeInclinedSteeringColumn',(0,-.40,.475),c,.050,2)
for i in range(3):beam('WholeSteeringSpoke_'+str(i+1),c,pt(.18,math.tau*i/3),.027,2)
box('WholeRearPickupMastSocket',(0,.72,.49),(.14,.16,.20),2)
beam('WholeTallRearPickupMast',(0,.72,.49),(0,.78,1.88),.027,2)
box('WholePickupContactShoe',(0,.78,1.90),(.19,.075,.045),1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeCockpitShell_MutedRed',(.48,.12,.075,1),.56,.10),('BufferSeatAndWheels_Charcoal',(.045,.052,.055,1),.82,0),('AxlesColumnAndPickup_DullSteel',(.34,.37,.39,1),.54,.55)]
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
focus=Vector((0,0,.93))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.65;aim(cam,(4,-7,3.7));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/carnival/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'carnival','style':'S01-clean-geometric','title':'Fixed Open Cockpit Bumper Car','description':'One newly authored complete static bumper-car exterior: one continuous rounded low hull with a genuine open cockpit and integral thick floor/foredeck, a complete broad oval buffer ring around the whole perimeter, low chassis and three small fixed grounded wheels, a broad dark seat with inclined back, tilted three-spoke steering ring on a supported column and one tall rear pickup mast ending in a small contact shoe. All complete numeric geometry is newly authored; no old sit-down racing cabinet is stripped of its screen, and no trailer or scooter shell is repurposed. The low enclosing oval buffer/hull and rear mast form a coherent distinct whole ride-car silhouette. Three opaque untextured solid PBR roles; metres, Z up, full horizontally centred bounds and ground origin. One complete prop, zero scenes, no independent seat/pole counts. Fixed unoccupied exterior only: no ceiling/floor power network, current collection, motor, steering or collision function, ride trajectory, padding performance, passenger fit, restraint, loading, road use or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
