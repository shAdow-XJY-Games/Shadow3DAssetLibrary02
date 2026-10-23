import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='arcade-fixed-open-inspection-claw-cabinet-01'
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
# One integral lower cabinet with an actual top drop and front receiving mouth.
box('WholeGroundPlinth',(0,0,.045),(1.14,.94,.09),3)
def lower_body():
 xs=[-.53,-.43,-.13,.53];ys=[-.42,-.32,.05,.42];zs=[.075,.22,.78,.84];cells=set()
 for i in range(3):
  for j in range(3):
   for k in range(3):
    # One connected vertical receiver recess, open at front and prize-floor top.
    if not(i==1 and j<2 and k>0):cells.add((i,j,k))
 v=[];f=[];idx={}
 for i,j,k in sorted(cells):
  c=[(xs[i+x],ys[j+y],zs[k+z])for z in[0,1]for y in[0,1]for x in[0,1]]
  for face,nb in zip(BOX,[(i,j,k-1),(i,j,k+1),(i,j-1,k),(i,j+1,k),(i-1,j,k),(i+1,j,k)]):
   if nb in cells:continue
   ids=[]
   for n in face:
    p=c[n]
    if p not in idx:idx[p]=len(v);v.append(p)
    ids.append(idx[p])
   f.append(tuple(ids))
 mesh('WholeLowerCabinetWithOpenReceiver',v,f,0)
lower_body()
# Open inspection presentation deliberately omits transparent glazing.
for x,label in[(-.50,'Left'),(.50,'Right')]:
 for y,side in[(-.39,'Front'),(.39,'Rear')]:box(label+side+'WholeFramePost',(x,y,1.40),(.075,.075,1.26),0)
box('WholeBackPanel',(0,.405,1.39),(.95,.045,1.10),2)
box('WholeRoof',(0,0,2.02),(1.10,.91,.10),0)
box('WholeFrontHeader',(0,-.415,1.93),(1.04,.11,.12),2)
# Two full Y rails, one full X bridge, fixed carriage and suspended three-prong claw.
for x,label in[(-.47,'Left'),(.47,'Right')]:box(label+'GantryLongRail',(x,0,1.85),(.05,.78,.065),1)
box('WholeGantryCrossBridge',(0,.065,1.82),(1.0,.09,.09),1)
box('WholeFixedCarriage',(.10,.065,1.755),(.16,.16,.10),0)
lathe_z('WholeFixedHoistCable',.10,.065,[(0,1.52),(.014,1.52),(.014,1.77),(0,1.77)],1,12)
lathe_z('WholeClawCrown',.10,.065,[(0,1.43),(.075,1.43),(.085,1.52),(.045,1.57),(0,1.57)],1,16)
def prong(name,angle):
 path=[(.045,1.465),(.12,1.40),(.21,1.28),(.215,1.17),(.16,1.09),(.10,1.075)];v=[];f=[];er=(math.cos(angle),math.sin(angle));et=(-math.sin(angle),math.cos(angle))
 for j,(r,z) in enumerate(path):
  a=path[max(0,j-1)];b=path[min(len(path)-1,j+1)];dr,dz=b[0]-a[0],b[1]-a[1];l=math.hypot(dr,dz);nr,nz=-dz/l,dr/l
  for normal,tangent in[(-1,-1),(1,-1),(1,1),(-1,1)]:
   rr=r+normal*.016*nr;zz=z+normal*.016*nz;v.append((.10+rr*er[0]+tangent*.022*et[0],.065+rr*er[1]+tangent*.022*et[1],zz))
 f=[(3,2,1,0),tuple((len(path)-1)*4+i for i in range(4))]
 for j in range(len(path)-1):
  for i in range(4):k=(i+1)%4;f.append((j*4+i,j*4+k,(j+1)*4+k,(j+1)*4+i))
 mesh(name,v,f,1)
for j in range(3):prong('WholeFixedCurvedClawFinger_'+str(j+1),math.tau*j/3)
# Fixed control ledge, no screen/payment or successful-play promise.
box('WholeControlLedge',(.08,-.465,.84),(.76,.20,.08),2)
lathe_z('WholeJoystick',-.10,-.475,[(0,.87),(.018,.87),(.018,.95),(.045,.97),(.045,1.005),(.025,1.025),(0,1.025)],3,12)
for x,label in[(.21,'Left'),(.33,'Right')]:lathe_z(label+'WholeControlButton',x,-.475,[(0,.87),(.035,.87),(.035,.905),(0,.905)],4,16)
# Front upper play opening and right open side are intentional inspection openings.
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('Cabinet_MutedCyan',(.055,.30,.34,1),.62,.10),('GantryClaw_SatinMetal',(.37,.43,.44,1),.42,.65),('HeaderControls_WarmCream',(.73,.69,.54,1),.67,.05),('BaseJoystick_DarkGraphite',(.055,.07,.075,1),.74,.10),('Buttons_MutedCoral',(.63,.18,.09,1),.60,0)]
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
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.85;aim(cam,(5,-7,3.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/arcade/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'arcade','style':'S01-clean-geometric','title':'Fixed Open-Inspection Claw Game Cabinet','description':'One newly authored complete fixed claw-game cabinet shown in an open inspection presentation without glass. The integral lower cabinet contains a true connected top drop opening and deep front receiving mouth. Four full corner posts, a back panel and a roof support two longitudinal gantry rails, a full cross bridge, a fixed carriage, a short hoist cable and one crown with three complete thick inward-curved claw fingers. A projecting fixed control ledge has a joystick and two buttons. The upper play chamber is empty, no prizes or old toy models are instances. This differs from a screen arcade cabinet and a blind-neck token receiver: the complete elevated two-axis bridge, suspended claw and connected drop/receiver architecture are visible geometry rather than painted panels. Closed editable solids with intentionally embedded fixed joins, five constant opaque PBR materials, metres/native Z up/horizontal bounds-centred ground origin. One whole display prop, zero scenes. No actual control, payment, game or prize rules, prize capture, motion, continuous swept clearance, transparent glazing, human fit, load, manufacture or safety claim. Not an operating or fully enclosed commercial game appliance.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':5,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
