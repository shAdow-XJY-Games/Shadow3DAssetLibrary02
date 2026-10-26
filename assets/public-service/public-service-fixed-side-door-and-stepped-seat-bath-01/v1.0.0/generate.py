import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='public-service-fixed-side-door-and-stepped-seat-bath-01'
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



# Shared cell boundary, not overlapping thin box walls: the seat, footwell and portal are integral.
xs=[-.45,-.37,-.28,.28,.37,.45];ys=[-.65,-.57,.12,.57,.65];zs=[.10,.18,.60,1.00]
occupied=set()
for i in range(len(xs)-1):
 for j in range(len(ys)-1):
  for k in range(len(zs)-1):
   x=(xs[i]+xs[i+1])/2;y=(ys[j]+ys[j+1])/2;z=(zs[k]+zs[k+1])/2
   solid=z<.18 or abs(x)>.37 or y>.57 or (y>.12 and z<.60) or (y<-.57 and abs(x)>.28)
   if solid:occupied.add((i,j,k))
v=[];faces=[];index={}
def vi(p):
 if p not in index:index[p]=len(v);v.append((xs[p[0]],ys[p[1]],zs[p[2]]))
 return index[p]
for i,j,k in sorted(occupied):
 for delta,q in [((-1,0,0),[(i,j,k),(i,j,k+1),(i,j+1,k+1),(i,j+1,k)]),((1,0,0),[(i+1,j,k),(i+1,j+1,k),(i+1,j+1,k+1),(i+1,j,k+1)]),((0,-1,0),[(i,j,k),(i+1,j,k),(i+1,j,k+1),(i,j,k+1)]),((0,1,0),[(i,j+1,k),(i,j+1,k+1),(i+1,j+1,k+1),(i+1,j+1,k)]),((0,0,-1),[(i,j,k),(i,j+1,k),(i+1,j+1,k),(i+1,j,k)]),((0,0,1),[(i,j,k+1),(i+1,j,k+1),(i+1,j+1,k+1),(i,j+1,k+1)])]:
  if (i+delta[0],j+delta[1],k+delta[2])not in occupied:faces.append(tuple(vi(p)for p in q))
mesh('WholeSteppedSeatFootwellAndDoorwayShell',v,faces,0)

for x in[-.31,.31]:
 for y in[-.48,.48]:box('WholeGroundFoot_'+str((x,y)),(x,y,.06),(.12,.14,.12),2)
# One matching panel fixed away from the portal; no moving or sealing performance.
ang=math.radians(-110)
def doorpoint(p):
 x,y,z=p;return(-.28+math.cos(ang)*x-math.sin(ang)*y,-.61+math.sin(ang)*x+math.cos(ang)*y,z)
def place_door(n):
 v,f,m=G[n];G[n]=([doorpoint(p)for p in v],f,m)
box('WholeFixedOpenDoor',(.270,0,.590),(.540,.055,.800),1);place_door('WholeFixedOpenDoor')
for j,z in enumerate([.31,.86]):
 lathe_z('WholeVerticalHinge_'+str(j),-.28,-.61,[(0,z-.06),(.025,z-.06),(.025,z+.06),(0,z+.06)],3,16)
 box('WholeRootedHingeEar_'+str(j),(-.315,-.61,z),(.095,.085,.065),3)
# Door grip with full ends into the exterior panel, not a floating handle.
for j,z in enumerate([.57,.75]):
 box('WholeDoorGripRoot_'+str(j),(.43,-.047,z),(.024,.055,.024),3);place_door('WholeDoorGripRoot_'+str(j))
box('WholeDoorGripBridge',(.43,-.074,.66),(.030,.030,.21),3);place_door('WholeDoorGripBridge')
# Two continuous extruded profiles avoid exposed coplanar rod caps at their bends.
def whole_profile(name,p,a,b,axis,mat):
 if sum(u[0]*v[1]-u[1]*v[0]for u,v in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);tt=triangulate(p)
 def pos(q,t):return(t,q[0],q[1])if axis=='x'else(q[0],q[1],t)
 mesh(name,[pos(q,t)for t in[a,b]for q in p],[tuple(reversed(t))for t in tt]+[tuple(n+i for i in t)for t in tt]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],mat)
whole_profile('WholeRearOpenGrab',[(-.244,.60),(-.244,.466),(.244,.466),(.244,.60),(.216,.60),(.216,.494),(-.216,.494),(-.216,.60)],.836,.864,'z',3)
whole_profile('WholeContinuousReturnTap',[(.5925,.99),(.6275,.99),(.6275,1.1775),(.3925,1.1775),(.3925,1.10),(.4275,1.10),(.4275,1.1425),(.5925,1.1425)],.2525,.2875,'x',3)
for j,x in enumerate([.12,-.05]):lathe_z('WholeBlankControl_'+str(j),x,.61,[(0,.99),(.035,.99),(.035,1.035),(0,1.035)],2,16)
lathe_z('WholeBlindFootwellDrainCap',0,-.28,[(0,.179),(.035,.179),(.035,.185),(0,.185)],3,20)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeSteppedShell_WarmIvory',(.72,.73,.66,1),.54,.02),('WholeDoor_MutedTeal',(.18,.34,.35,1),.60,.03),('WholeFeetAndControls_Charcoal',(.055,.065,.065,1),.72,.05),('WholeHingesGripAndTap_SatinAlloy',(.39,.43,.43,1),.47,.45)]
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
focus=Vector((0,0,.49))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.25;aim(cam,(4,-6,4.7));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/public-service/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'public-service','style':'S01-clean-geometric','title':'Fixed Side Door and Stepped Seat Bath','description':'One newly authored complete empty short seated-bath appearance in a fixed open-door pose. One shared-vertex thick shell includes the full lower footwell, a genuinely raised rear seat step, rear and side walls, and a low front doorway through the full wall. A whole matching thick door is fixed outward on two rooted vertical hinges, with an open grip attached to its outside. Four full short grounded feet carry the shell, while a rear rim carries the whole fixed tap and two blank controls. A continuous interior grab bar is rooted into the rear wall. This is not the older elongated rolled-lip clawfoot tub resized or the neck-notched pedestal bowl enlarged: the stepped seat-to-footwell cavity and full low side-entry portal form a new connected boundary. No old model or mesh imported. Four opaque PBR roles, metres Z up, horizontally bounds-centred ground datum, one whole prop zero scenes. Empty static visual art only: no person, water, door sweep, seal or watertightness, usable plumbing, drainage, bathing or medical advice, human fit, accessibility certification, ergonomic suitability, load, installation or safety performance. Rigging animation interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
