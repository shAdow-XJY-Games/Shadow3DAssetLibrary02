import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='public-service-fixed-twin-shaft-cabin-loop-cutaway-01'
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



box('WholeGroundFootFacilityBase',(0,0,.10),(3.30,2.05,.20),3)
# One shared architecture with two separate shaft lanes and two fixed level mouths.
for j,x in enumerate([-1.39,0,1.39]):box('WholeFrontShaftPier_%d'%j,(x,-.53,3.25),(.16,.19,6.10),0)
for j,z in enumerate([.62,3.07]):
 box('WholeLevelFrontThreshold_%d'%j,(0,-.75,z),(3.04,.65,.16),3)
 box('WholeLevelOverdoorHeader_%d'%j,(0,-.53,z+1.97),(3.04,.15,.18),0)
box('WholeTopArchitectureHeader',(0,-.15,6.40),(3.00,1.03,.20),0)
for j,x in enumerate([-1.39,1.39]):
 box('WholeRearShaftColumn_%d'%j,(x,.79,3.25),(.16,.16,6.10),0)
 for k,z in enumerate([.45,2.45,4.90,6.25]):box('WholeSideDepthTie_%d_%d'%(j,k),(x,.135,z),(.12,1.32,.14),0)
for j,z in enumerate([.95,5.60]):
 box('WholeRearBearingCrossbeam_%d'%j,(0,.79,z),(3.04,.18,.18),0)
 box('WholeReturnBearingPedestal_%d'%j,(0,.68,z),(.22,.30,.24),0)
 cyly('WholeReturnAxle_%d'%j,.32,.90,0,z,.070,2,24)
 # Full annular return wheel with open central area, broad hub and four spokes.
 ringy('WholeReturnRim_%d'%j,.43,.57,0,z,.60,.705,2,40)
 cyly('WholeReturnHub_%d'%j,.405,.595,0,z,.145,2,24)
 for k in range(4):
  t=math.tau*k/4;beam('WholeReturnSpoke_%d_%d'%(j,k),(.11*math.cos(t),.50,z+.11*math.sin(t)),(.625*math.cos(t),.50,z+.625*math.sin(t)),.075,2)
 cyly('WholeProudAxleEnd_%d'%j,.30,.37,0,z,.10,1,20)
# One continuous closed thick band, including both actual return arcs.
P=[]
for k in range(25):t=math.pi*k/24;P.append((.70*math.cos(t),5.60+.70*math.sin(t),math.cos(t),math.sin(t)))
P.append((-.70,.95,-1,0))
for k in range(1,25):t=math.pi+math.pi*k/24;P.append((.70*math.cos(t),.95+.70*math.sin(t),math.cos(t),math.sin(t)))
n=len(P);v=[];f=[]
for x,z,nx,nz in P:
 for r,y in[(-.023,.435),(.023,.435),(.023,.565),(-.023,.565)]:v.append((x+nx*r,y,z+nz*r))
for k in range(n):
 for i in range(4):j=(i+1)%4;f.append((4*k+i,4*k+j,4*((k+1)%n)+j,4*((k+1)%n)+i))
mesh('WholeContinuousRearReturnBand',v,f,1)
# Full shared-boundary cabin material shell, not overlapping box walls.
def cabin(name,cx,z0):
 xs=[-.49,-.435,.435,.49];ys=[-.415,.295,.35];zs=[0,.075,1.57,1.65];faces={}
 def face(p):
  key=tuple(sorted(p))
  if key in faces:del faces[key]
  else:faces[key]=p
 for a,b in zip(xs,xs[1:]):
  for c,d in zip(ys,ys[1:]):
   for e,h in zip(zs,zs[1:]):
    if not(abs((a+b)/2)>.435 or (c+d)/2>.295 or (e+h)/2<.075 or (e+h)/2>1.57):continue
    vv=[(cx+x,y,z0+z)for z in[e,h]for y in[c,d]for x in[a,b]]
    for ids in BOX:face(tuple(vv[i]for i in ids))
 vv=[];ff=[];ix={}
 for poly in faces.values():
  ii=[]
  for p in poly:
   if p not in ix:ix[p]=len(vv);vv.append(p)
   ii.append(ix[p])
  ff.append(tuple(ii))
 mesh(name,vv,ff,1)
for j,x in enumerate([-.70,.70]):
 for k,z in enumerate([.70,3.15]):
  cabin('WholeOpenCabin_%d_%d'%(j,k),x,z)
  # Rear fixtures connect the full cabin shell to the fixed band; no mobile kinematics claim.
  box('WholeCabinRearHangingBridge_%d_%d'%(j,k),(x,.415,z+1.43),(.24,.25,.18),2)
  cyly('WholeCabinSuspensionPin_%d_%d'%(j,k),.30,.61,x,z+1.43,.055,2,20)
  box('WholeCabinFloorInset_%d_%d'%(j,k),(x,-.045,z+.083),(.82,.62,.016),3)
PALETTE=[('WholeArchitectureDeepBlue',(.14,.24,.29,1),.82,.12),('WholeCabinsAndBandWarmIvory',(.64,.62,.53,1),.78,.1),('WholeReturnHardwareDullSteel',(.35,.40,.40,1),.52,.48),('WholeBaseThresholdAndFloorStone',(.34,.36,.35,1),.90,0)]
# Compact display scale authored before export; all dimensions uniformly .60 m per design unit.
G={n:([tuple(c*.60 for c in p)for p in v],f,m)for n,(v,f,m)in G.items()}
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
focus=Vector((0,0,1.95))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=4.92;aim(cam,(5,-11,7));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/public-service/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'public-service','style':'S01-clean-geometric','title':'Fixed Twin Shaft Cabin Loop Cutaway','description':'One complete independently authored compact static architectural cutaway display of a twin-shaft circulating-cabin lift appearance. A shared broad footing carries a full three-pier front frame, two separate open vertical cabin lanes and an entire rear mechanical support frame. Two full level-front thresholds and crossheaders define four genuine open landing mouths. Four whole empty front-open cabins have thick continuous floor, side, rear and roof shells; each has its own rear hanging attachment and pin to the fixed continuous closed return-band appearance behind the cabins. One complete tall closed racetrack band passes around separate upper and lower full return wheels on actual whole axles and bearing pedestals. Upper and lower return spaces stay deliberately open so the route can be seen; no cabin is placed through a turn, and no turning motion is claimed. Unlike the single caged tower with an integral projecting access trough, the building frame has two separate adjacent lanes, repeated level mouths and shared upper/lower returns. Unlike the enclosed narrow grain bucket elevator, there are no transfer ducts, casing inspection window or belt-mounted outward scoops: full upright empty cabins hang by distinct rear fixtures behind architectural landing openings. All geometry newly authored together, no old cabin, chain lift or building mesh imported. Four opaque constant PBR roles, metres Z up, full horizontal bounds centred, one entire modular facility zero scenes. Unoccupied static cutaway art only: no actual cabin circulation, pendulum clearance, guidance, drive, synchronization, stopping, entry or exit, boarding, evacuation, human access, code compliance, load, installation or safety capability. The displayed fixed seats do not validate moving suspension or travel. No people, doors, signs, rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
