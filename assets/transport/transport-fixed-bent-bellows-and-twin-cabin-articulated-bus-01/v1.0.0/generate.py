import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='transport-fixed-bent-bellows-and-twin-cabin-articulated-bus-01'
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



YAW=math.radians(18)
def yaw(p):x,y,z=p;return(math.cos(YAW)*x-math.sin(YAW)*y,math.sin(YAW)*x+math.cos(YAW)*y,z)
def xyprism(name,p,z0,z1,mat):
 n=len(p);v=[(x,y,z)for z in[z0,z1]for x,y in p];f=[]
 for a,b,c in triangulate(p):f.extend([(c,b,a),(a+n,b+n,c+n)])
 f +=[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh(name,v,f,mat)
def tyre(name,x,y):
 N=20;r=.30/math.cos(math.pi/N);v=[]
 for xx,rr in[(x-.09,r),(x+.09,r),(x+.09,.13),(x-.09,.13)]:
  v.extend((xx,y+rr*math.sin(math.tau*i/N+math.pi/N),.30+rr*math.cos(math.tau*i/N+math.pi/N))for i in range(N))
 f=[(k*N+i,k*N+(i+1)%N,((k+1)%4)*N+(i+1)%N,((k+1)%4)*N+i)for k in range(4)for i in range(N)];mesh(name,v,f,2)
def cabin(label,ya,yb,axles,rear=False):
 before=set(G)
 p=[(-.70,ya),(.70,ya),(.70,yb),(-.70,yb)]
 if not rear:p=[(-.70,ya),(.70,ya),(.70,-3.15),(.34,-3.15),(.34,-2.45),(.70,-2.45),(.70,yb),(-.70,yb)]
 xyprism(label+'WholeNotchedCabinFloor'if not rear else label+'WholeCabinFloor',p,.65,.735,3)
 for side in[-1,1]:
  box(label+'WholeLongitudinalUnderframe_'+str(side),(side*.48,(ya+yb)/2,.56),(.11,yb-ya-.08,.16),3)
  spans=[(ya,yb)]if rear or side==-1 else[(ya,-3.15),(-2.45,yb)]
  for k,(a,b)in enumerate(spans):box(label+'WholeLowerSide_'+str((side,k)),(side*.72,(a+b)/2,.95),(.08,b-a,.44),0)
  ys=[ya+.04,ya+.74,ya+1.55,yb-.04]if rear else[ya+.04,-3.15,-2.45,-1.70,-.98,yb-.04]
  for k,y in enumerate(ys):box(label+'WholeWindowPillar_'+str((side,k)),(side*.72,y,1.57),(.075,.065,.86),1)
  box(label+'WholeWindowHeader_'+str(side),(side*.72,(ya+yb)/2,1.98),(.08,yb-ya,.07),1)
 box(label+'WholeRoofCap',(0,(ya+yb)/2,2.05),(1.53,yb-ya+.035,.12),1)
 for k,y in enumerate(axles):
  axle(label+'WholeAxle_'+str(k),-.87,.87,y,.30,.042,3,16)
  box(label+'WholeAxleCrossBearer_'+str(k),(0,y,.60),(1.40,.13,.12),3)
  for side in[-1,1]:
   box(label+'WholeAxleHanger_'+str((k,side)),(side*.48,y,.43),(.13,.12,.30),3)
   tyre(label+'WholeGroundFootTyre_'+str((k,side)),side*.79,y)
   axle(label+'WholeWheelHub_'+str((k,side)),side*.79-.105,side*.79+.105,y,.30,.14,3,20)
 seatys=[.9,1.78,2.36]if rear else[-1.96,-1.24,-.52]
 for k,y in enumerate(seatys):
  for side in[-1,1]:
   x=side*.43
   box(label+'WholeSeatRoot_'+str((k,side)),(x,y,.86),(.12,.23,.28),3)
   box(label+'WholeSeatPan_'+str((k,side)),(x,y,1.015),(.43,.40,.10),0)
   box(label+'WholeSeatBack_'+str((k,side)),(x,y+.16,1.22),(.43,.075,.47),0)
 end=yb if rear else ya
 box(label+'WholeEndApron',(0,end,.95),(1.48,.08,.44),0)
 box(label+'WholeEndWindowHeader',(0,end,1.97),(1.47,.085,.08),1)
 box(label+'WholeEndBumper',(0,end+(.065 if rear else-.065),.75),(1.55,.12,.13),2)
 for side in[-1,1]:box(label+'WholeBlankEndMarker_'+str(side),(side*.53,end+(.048 if rear else-.048),1.03),(.20,.025,.12),1 if not rear else 0)
 if rear:
  for name in set(G)-before:
   v,f,m=G[name];G[name]=([yaw(p)for p in v],f,m)
cabin('Forward',-3.90,-.27,[-3.2,-.88])
cabin('Rear',.27,2.70,[1.88],True)
# Real through passage, thick pleated side/ceiling/floor connector; never an opaque box across the cabins.
outer=[(-.68,.70),(.68,.70),(.74,.77),(.74,1.96),(.67,2.02),(-.67,2.02),(-.74,1.96),(-.74,.77)]
inner=[(-.645,.745),(.645,.745),(.695,.79),(.695,1.925),(.65,1.975),(-.65,1.975),(-.695,1.925),(-.695,.79)]
rings=[]
for k in range(13):
 t=k/12;ang=YAW*t;cx=-math.sin(YAW)*.27*t;cy=-.285*(1-t)+math.cos(YAW)*.285*t;expand=.055 if k%2 else 0
 for loop in[outer,inner]:
  ring=[]
  for x,z in loop:
   xx=x+(expand if x>0 else-expand);zz=z+expand*(1 if z>1.3 else-1)
   ring.append((cx+xx*math.cos(ang),cy+xx*math.sin(ang),zz))
  rings.append(ring)
v=sum(rings,[]);f=[];n=8
for k in range(12):
 for i in range(n):j=(i+1)%n;f.extend([(k*16+i,k*16+j,(k+1)*16+j,(k+1)*16+i),(k*16+8+i,(k+1)*16+8+i,(k+1)*16+8+j,k*16+8+j)])
for i in range(n):
 j=(i+1)%n;f.extend([(i,8+i,8+j,j),(192+i,192+j,200+j,200+i)])
mesh('WholeBentFourWallPleatedPassage',v,f,2)
# Low broad pivot connection and separate fixed passage-floor saddle.
xyprism('WholeLowerJointBridge',[(-.28,-.45),(.28,-.45),(.28,.05),(.18,.25),(-.18,.25),(-.28,.05)],.49,.54,3)
lathe_z('WholeCapturedJointPin',0,0,[(0,.46),(.12,.46),(.12,.49),(.075,.49),(.075,.63),(.12,.63),(.12,.66),(0,.66)],3,24)
xyprism('WholeFixedPassageFloor',[(-.65,-.34),(.65,-.34),yaw((.65,.34,0))[:2],yaw((-.65,.34,0))[:2]],.67,.75,3)
# Right entry treads root in the front floor notch and its low cross supports.
box('WholeUpperEntryTread',(.52,-2.80,.57),(.38,.68,.12),3)
box('WholeLowerEntryTread',(.82,-2.80,.39),(.35,.68,.12),3)
for y in[-3.07,-2.53]:beam('WholeEntryTreadBracket_'+str(y),(.42,y,.64),(.87,y,.36),.09,3)
box('WholeDriverSeatPedestal',(-.39,-3.24,.86),(.14,.25,.28),3)
box('WholeDriverSeatPan',(-.39,-3.24,1.015),(.42,.39,.10),0)
box('WholeDriverSeatBack',(-.39,-3.08,1.25),(.42,.08,.48),0)
box('WholeDriverDashboard',(0,-3.76,1.19),(1.30,.23,.12),2)
beam('WholeFixedSteeringColumn',(-.39,-3.55,.73),(-.39,-3.58,1.29),.045,3)
lathe_z('WholeOpenSteeringRim',-.39,-3.58,[(.13,1.275),(.16,1.275),(.16,1.31),(.13,1.31)],2,24)
box('WholeSteeringCrossbar',(-.39,-3.58,1.29),(.29,.035,.025),2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeBodyAndSeats_MutedTeal',(.17,.38,.36,1),.72,.03),('WholeRoofsPillarsAndFrontMarkers_WarmIvory',(.76,.75,.66,1),.70,.03),('WholeBellowsTyresControls_Charcoal',(.04,.052,.055,1),.83,.01),('WholeUnderframesFloorsPins_SatinGrey',(.33,.38,.39,1),.60,.30)]
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
focus=Vector((0,0,.92))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=8.15;aim(cam,(6,-8,5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/transport/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'transport','style':'S01-clean-geometric','title':'Fixed Bent Bellows and Twin Cabin Articulated Bus','description':'One wholly newly authored complete fixed articulated passenger-bus exterior and open-cabin display. Two separate full cabin floors, lower side walls, actual open window bays and complete roof caps carry their own fixed seat rows and underframes. The longer forward section rests on two axles; the shorter rear section and its own axle are baked at an eighteen-degree horizontal angle. One continuous thick four-sided pleated connector surrounds a real open passage between the two cabin ends; a separate fixed joining floor and low captured-pivot exterior join the independent chassis below. A right-front entry and two rooted treads, whole driver controls, six full flat-tread tyres and fixed front/rear marker faces complete one vehicle. Unlike the short single-cabin minibus, this has an entire bent enclosed passage and independently supported rear cabin, not only added wheels, stretched body or changed paint. Unlike the old low split-bin robot, this has two hollow roofed passenger sections and the surrounding pleated connection, no cargo tub or transplanted old clevis mesh. All numeric geometry is new. Four opaque PBR roles; window apertures intentionally unglazed. Metres Z up, whole XY-centred ground datum, one prop zero scenes. Proportions are stylised display dimensions, not road-vehicle design. No doors, people, powered drivetrain, driving, steering, articulation path, passage accessibility, passenger fit/capacity, crashworthiness, roadworthiness, loading, manufacturing or safety capability. Rigging animation and interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
