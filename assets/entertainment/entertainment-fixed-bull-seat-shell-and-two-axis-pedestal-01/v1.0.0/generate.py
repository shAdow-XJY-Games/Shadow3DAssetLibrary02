import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='entertainment-fixed-bull-seat-shell-and-two-axis-pedestal-01'
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



# New complete bull-shaped riding shell on a visible separated-axis cradle.
lathe_z('WholeGroundFootBroadPedestal',0,0,[(0,0),(.64,0),(.68,.045),(.65,.125),(.53,.160),(0,.160)],3,12)
for k,x in enumerate([-.235,.235]):
 box('WholeLowerTrunnionCheek_%d'%k,(x,0,.33),(.105,.30,.40),3)
 ringx('WholeBoredLowerSideBearing_%d'%k,x-.065,x+.065,0,.515,.053,.105,1,20)
 # Independent side stubs leave the central interval free of the perpendicular upper shaft.
 axle('WholeSeparateSideTrunnion_%d'%k,x-.075,x+.075,0,.515,.054,1,16)
for side,x in enumerate([-.168,.168]):box('WholeIntermediateSideRail_%d'%side,(x,0,.515),(.070,.58,.095),1)
for k,y in enumerate([-.245,.245]):
 box('WholeIntermediateEndRail_%d'%k,(0,y,.527),(.39,.070,.095),1)
 ringy('WholeBoredUpperEndBearing_%d'%k,y-.055,y+.055,0,.585,.045,.105,1,20)
cyly('WholeLongitudinalUpperPivot',-.323,.323,0,.585,.046,1,20)
box('WholeSeatShellMountingStem',(0,0,.755),(.17,.27,.38),3)
def loft_body(name,rows,mat,n=16):
 c=math.cos(math.pi/n);v=[];f=[]
 for y,w,lo,hi in rows:
  for j in range(n):t=(j+.5)*math.tau/n;v.append((w*math.cos(t)/c,y,lo+(hi-lo)*(math.sin(t)+c)/(2*c)))
 f=[tuple(reversed(range(n))),tuple((len(rows)-1)*n+j for j in range(n))]
 for k in range(len(rows)-1):
  for j in range(n):q=(j+1)%n;f.append((k*n+j,k*n+q,(k+1)*n+q,(k+1)*n+j))
 mesh(name,v,f,mat)
loft_body('WholeContinuousBullSeatShoulderAndMuzzleShell',[(.70,.16,1.08,1.35),(.48,.32,.93,1.43),(.10,.35,.90,1.37),(-.25,.33,.92,1.43),(-.50,.27,1.02,1.58),(-.70,.23,1.10,1.64),(-.88,.24,1.06,1.48),(-.98,.20,1.10,1.37)],0)
loft_body('WholeBroadBluntNosePad',[(-.945,.19,1.105,1.38),(-.998,.215,1.115,1.37),(-1.035,.18,1.15,1.34)],1)
def tube(name,path,mat,n=10):
 v=[];f=[]
 for k,(p,r)in enumerate(path):
  a=path[max(k-1,0)][0];b=path[min(k+1,len(path)-1)][0];w=unit(sub(b,a));u=unit(cross(w,(0,1,0)if abs(w[1])<.9 else(1,0,0)));vv=cross(w,u)
  for j in range(n):v.append(tuple(p[i]+r*(u[i]*math.cos(math.tau*j/n)+vv[i]*math.sin(math.tau*j/n))for i in range(3)))
 f=[tuple(reversed(range(n))),tuple((len(path)-1)*n+j for j in range(n))]
 for k in range(len(path)-1):
  for j in range(n):q=(j+1)%n;f.append((k*n+j,k*n+q,(k+1)*n+q,(k+1)*n+j))
 mesh(name,v,f,mat)
def blob(name,c,r,mat):
 lathe_z(name,0,0,[(0,-1),(.65,-.75),(.94,-.35),(1,0),(.94,.35),(.65,.75),(0,1)],mat,12);v,f,m=G[name];G[name]=([(c[0]+x*r[0],c[1]+y*r[1],c[2]+z*r[2])for x,y,z in v],f,m)
for k,sgn in enumerate([-1,1]):
 tube('WholeBluntOutwardUpturnedHorn_%d'%k,[((sgn*.15,-.68,1.56),.040),((sgn*.28,-.67,1.60),.035),((sgn*.43,-.64,1.73),.022),((sgn*.48,-.60,1.84),.006)],2)
 blob('WholeLateralEar_%d'%k,(sgn*.265,-.60,1.49),(.14,.075,.05),0)
 blob('WholeSeatedDarkEye_%d'%k,(sgn*.225,-.85,1.385),(.026,.037,.034),1)
tube('WholeShortHangingTail',[((0,.65,1.22),.045),((0,.83,1.12),.028),((0,.91,.97),.023),((0,.88,.84),.052),((0,.84,.78),.020)],0)
# Thick concave saddle surface, with hidden underside overlap rather than coplanar exterior.
xx=[-.25,0,.25];ys=[-.25,-.12,.10,.30,.45];zz=[1.43,1.40,1.37,1.42,1.49];v=[];f=[]
for down in[True,False]:
 for y,z in zip(ys,zz):
  for x in xx:v.append((x,y,z+.025+(.025 if x else 0)-(.10 if down else 0)))
n=15
for j in range(4):
 for i in range(2):a=j*3+i;b=a+1;c=a+4;d=a+3;f.extend([(a,d,c,b),(n+a,n+b,n+c,n+d)])
edge=[0,1,2,5,8,11,14,13,12,9,6,3]
for a,b in zip(edge,edge[1:]+edge[:1]):f.append((a,b,n+b,n+a))
mesh('WholeConcaveRidingSaddlePad',v,f,2)
tube('WholeRootedFixedLoopGrip',[((-.09,-.18,1.445),.015),((-.085,-.18,1.535),.015),((-.05,-.18,1.575),.015),((.05,-.18,1.575),.015),((.085,-.18,1.535),.015),((.09,-.18,1.445),.015)],1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeBullShellAndTail_WarmBrown',(.30,.12,.055,1),.85,0),('WholeMechanismGripAndFaceDetails_Charcoal',(.065,.08,.085,1),.63,.25),('WholeSaddleAndBluntHorns_WarmTan',(.67,.46,.23,1),.78,0),('WholePedestalAndMount_MutedBlue',(.06,.17,.22,1),.71,.15)]
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
focus=Vector((0,0,.90))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.7;aim(cam,(4,-6,3.3));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/entertainment/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'entertainment','style':'S01-clean-geometric','title':'Fixed Bull Seat Shell and Two Axis Pedestal','description':'One newly authored complete static mechanical-bull-style amusement-seat exterior. A continuous wide short-neck bull-shaped riding shell has a broad blunt muzzle, two outward-upturned blunt horns, seated eyes, lateral ears and one short hanging tail. Its low concave saddle and rooted loop grip belong to the same complete ride, not a separate animal count. Instead of standing on hooves, the shell mounts directly through an underside stem into a visible two-axis cradle: paired side trunnions support an open rectangular intermediate frame, separate front and rear bearings carry a longitudinal upper shaft, and the whole assembly stands on two rooted lower cheeks and one broad finite base. All new numeric geometry: no old cow moved onto a stand and no spring-rider body or helix reused. The new shell has no udder, weight-bearing legs or biological anatomy claim, and the pedestal has no coil spring. One complete prop zero scenes, four opaque PBR roles, metres Z up and horizontally bounds-centred ground origin. Empty fixed art display only: the separated shafts and support members do not establish a validated motion mechanism, motor, control system, balance, rider fit, load, restraint, operation, fabrication or safety. No person, arena, rigging, animation or interaction is made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
