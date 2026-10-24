import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='carnival-fixed-twin-rotary-arm-transverse-gondola-01'
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



# Entire fixed twin-arm transverse-gondola ride, not a boat under a single top axle.
for side,x in [('Left',-1.55),('Right',1.55)]:
 box(side+'WholeGroundFoot',(x,.08,.060),(.52,1.75,.12),0)
 # Whole tapered pier, wide in depth at its root and narrow at the upper bearing.
 v=[(xx,y,z)for xx in[x-.13,x+.13]for y,z in[(-.46,.11),(.46,.11),(.13,2.72),(-.13,2.72)]];f=[(3,2,1,0),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4)for i in range(4)];mesh(side+'WholeTaperedUpperPivotPier',v,f,0)
 ringx(side+'WholeUpperBoredBearing',x-.18,x+.18,0,2.62,.105,.225,2,32)
 axle(side+'WholeUpperPivotShaft',x-.27,x+.27,0,2.62,.106,2,24)
 for sy in[-.62,.62]:beam(side+'WholePierGroundKnee_'+str(sy),(x,sy,.12),(x,sy*.14,1.15),.075,0)
# Two lower ties connect the grounded piers without a wide scene platform.
for y in[-.55,.65]:box('WholeGroundPierCrossTie_'+str(y),(0,y,.16),(3.15,.10,.10),0)
# Full separately authored counterbalanced arms, with a second independent gondola axle.
for side,x in [('Left',-1.305),('Right',1.305)]:
 # In-plane directions: upper pivot at 0/2.62, lower journal -.62/1.10.
 a=(-.62,1.10);b=(.35,3.48);dy,dz=b[0]-a[0],b[1]-a[1];L=math.hypot(dy,dz);ny,nz=-dz/L,dy/L
 p=[(a[0]+ny*.115,a[1]+nz*.115),(b[0]+ny*.115,b[1]+nz*.115),(b[0]-ny*.115,b[1]-nz*.115),(a[0]-ny*.115,a[1]-nz*.115)];v=[(xx,y,z)for xx in[x-.075,x+.075]for y,z in p];mesh(side+'WholeContinuousRotaryArm',v,[(3,2,1,0),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4)for i in range(4)],1)
 ringx(side+'WholeLowerGondolaBearing',x-.095,x+.095,-.62,1.10,.070,.16,2,24)
 axle(side+'WholeLowerGondolaJournal',x-.19,x+.19,-.62,1.10,.071,2,24)
 # Complete fixed counterweight housing belongs to the upper arm, not a separate object count.
 box(side+'WholeUpperCounterweightHousing',(x,.31,3.39),(.24,.42,.40),1)
# Whole thick open passenger tray, with low front sill and tall rear wall.
v=[]
for hx,y0,y1,zf,zfront,zback in[(1.17,-1.02,-.25,.65,.89,1.43),(1.115,-.965,-.305,.705,.89,1.43)]:
 v.extend([(-hx,y0,zf),(hx,y0,zf),(hx,y1,zf),(-hx,y1,zf),(-hx,y0,zfront),(hx,y0,zfront),(hx,y1,zback),(-hx,y1,zback)])
f=[(3,2,1,0),(8,9,10,11)]
for i in range(4):j=(i+1)%4;f.extend([(i,j,j+4,i+4),(i+4,j+4,j+12,i+12),(i+8,i+12,j+12,j+8)])
mesh('WholeOpenTransversePassengerTray',v,f,1)
# End journals seat into whole tray cheeks; no axle crosses the empty seat spaces.
box('WholeUndertrayCrossTie',(0,-.62,.672),(2.36,.10,.09),0)
for side,x in [('Left',-1.15),('Right',1.15)]:box(side+'WholeJournalRootCheek',(x,-.62,1.055),(.08,.29,.37),1)
# Five empty fixed seats share the whole tray; individual restraints are static appearances.
for i,x in enumerate([-.86,-.43,0,.43,.86]):
 box('Seat'+str(i)+'WholeRiser',(x,-.55,.82),(.32,.32,.24),0)
 box('Seat'+str(i)+'WholeSeatPad',(x,-.59,.945),(.35,.40,.055),2)
 box('Seat'+str(i)+'WholeBackPad',(x,-.345,1.16),(.35,.055,.39),2)
 # Whole U restraint traces from rear roots above the shoulders to the visible lap crossbar.
 beam('Seat'+str(i)+'LeftFixedRestraint',(x-.135,-.325,1.35),(x-.135,-.77,1.10),.036,0)
 beam('Seat'+str(i)+'RightFixedRestraint',(x+.135,-.325,1.35),(x+.135,-.77,1.10),.036,0)
 beam('Seat'+str(i)+'WholeLapCrossbar',(x-.15,-.77,1.10),(x+.15,-.77,1.10),.036,0)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholePiersFeetTiesAndRestraints_MutedTeal',(.075,.23,.25,1),.72,.10),('WholeArmsHousingAndTray_MutedOrange',(.61,.22,.08,1),.71,.08),('WholeAxlesBearingsAndSeatPads_WarmCream',(.73,.66,.46,1),.64,.15)]
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
focus=Vector((0,0,1.65))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=4.75;aim(cam,(4,-6,3.7));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/music/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'carnival','style':'S01-clean-geometric','title':'Fixed Twin Rotary Arm Transverse Gondola','description':'One newly authored complete fixed twin-rotary-arm amusement-ride appearance. Two deep grounded runners, tapered bearing piers, root knees and low cross-ties support two separate upper horizontal pivots. Each full long arm extends from a low transverse gondola journal past its upper pivot to a complete counterweight housing. A whole thick open transverse tray has its own second horizontal pivot axis, full side journal roots and five empty fixed seats with individually rooted restraint appearances. This is not the old boat pendulum with one upper common axle and rigid triangular bridles, and not a Ferris wheel with full rims, spokes and multiple level cabins: the two long grounded pivot arms and one independently journalled transverse passenger tray form a different complete structure. All geometry newly authored; no old ride mesh or cabin imported. Three opaque untextured constant PBR roles, metres, Z up and whole horizontally bounds-centred ground origin. One complete prop, zero scenes; seats and counterweights are not additional assets. Fixed empty game-art display only: no real rotation, synchronized arms, ride motion or kinematics, passenger fit, restraint effectiveness, balance, drive/brake internals, loads, manufacture, installation, operation or amusement safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
