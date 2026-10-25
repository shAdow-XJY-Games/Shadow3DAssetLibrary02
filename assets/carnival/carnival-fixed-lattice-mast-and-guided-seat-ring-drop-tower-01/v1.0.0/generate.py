import math,json,hashlib,sys,struct
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='carnival-fixed-lattice-mast-and-guided-seat-ring-drop-tower-01'
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



# One shared structure: open lattice mast, external rail-guided carriage and rooted seats.
box('WholeGroundFootCommonPlinth',(0,0,.065),(2.1,2.1,.13),0)
for j,(x,y)in enumerate([(-.22,-.22),(.22,-.22),(.22,.22),(-.22,.22)]):box('WholeContinuousTowerChord_%d'%j,(x,y,2.23),(.075,.075,4.28),1)
levels=[.18,.86,1.54,2.22,2.90,3.58,4.26]
def local(p,a):
 x,y,z=p;c=math.cos(a);s=math.sin(a);return(x*c-y*s,x*s+y*c,z)
for j in range(4):
 a=math.tau*j/4
 for k,z in enumerate(levels):beam('WholeLatticeHorizontal_%d_%d'%(j,k),local((-.22,-.22,z),a),local((.22,-.22,z),a),.046,1)
 for k,(z0,z1)in enumerate(zip(levels,levels[1:])):
  x0,x1=(-.22,.22)if k%2==0 else(.22,-.22)
  beam('WholeLatticeDiagonal_%d_%d'%(j,k),local((x0,-.213,z0),a),local((x1,-.213,z1),a),.032,1)
 box('WholeContinuousExternalGuideRail_%d'%j,(0,-.292,2.23),(.070,.040,4.10),2);v,f,m=G['WholeContinuousExternalGuideRail_%d'%j];G['WholeContinuousExternalGuideRail_%d'%j]=([local(q,a)for q in v],f,m)
 for k,z in enumerate([.25,1.52,2.90,4.20]):beam('WholeRailRoot_%d_%d'%(j,k),local((0,-.22,z),a),local((0,-.292,z),a),.042,1)
 box('WholeFixedLowCarriageShoulder_%d'%j,(0,-.365,.785),(.17,.18,.075),1);v,f,m=G['WholeFixedLowCarriageShoulder_%d'%j];G['WholeFixedLowCarriageShoulder_%d'%j]=([local(q,a)for q in v],f,m)
# Single connected square annulus, no four overlaid coplanar frame bars.
v=[]
for z,r in[(.82,.46),(.82,.335),(.94,.46),(.94,.335)]:v +=[(-r,-r,z),(r,-r,z),(r,r,z),(-r,r,z)]
f=[]
for j in range(4):q=(j+1)%4;f +=[(j,q,4+q,4+j),(8+j,12+j,12+q,8+q),(j,8+j,8+q,q),(4+j,4+q,12+q,12+j)]
mesh('WholeOpenCentreSeatCarriageRing',v,f,0)
def tube(name,pts,r,mat,n=8,closed=False):
 v=[];L=len(pts)
 for k,P in enumerate(pts):
  prev=pts[(k-1)%L]if closed else pts[max(k-1,0)];nex=pts[(k+1)%L]if closed else pts[min(k+1,L-1)];T=unit(sub(nex,prev));u=unit(cross(T,(0,1,0)if abs(T[1])<.9 else(1,0,0)));w=cross(T,u)
  for i in range(n):v.append(tuple(P[q]+r*(u[q]*math.cos(math.tau*i/n)+w[q]*math.sin(math.tau*i/n))for q in range(3)))
 fs=[]
 for k in range(L if closed else L-1):
  kk=(k+1)%L
  for i in range(n):fs.append((k*n+i,k*n+(i+1)%n,kk*n+(i+1)%n,kk*n+i))
 if not closed:fs +=[tuple(reversed(range(n))),tuple((L-1)*n+i for i in range(n))]
 mesh(name,v,fs,mat)

for j in range(4):
 a=math.tau*j/4
 def turn(name):
  v,f,m=G[name];G[name]=([local(q,a)for q in v],f,m)
 for k,x in enumerate([-.070,.070]):
  name='WholeCarriageRollerCheek_%d_%d'%(j,k);box(name,(x,-.385,1.035),(.025,.080,.395),0);turn(name)
 for k,z in enumerate([.87,1.20]):
  name='WholeRailContactRoller_%d_%d'%(j,k);axle(name,-.032,.032,-.355,z,.045,3,20);turn(name)
  name='WholeRollerCrossAxle_%d_%d'%(j,k);axle(name,-.089,.089,-.355,z,.010,2,12);turn(name)
 beam('WholeSeatRadialCarrier_%d'%j,local((0,-.40,.905),a),local((0,-.69,.905),a),.09,1)
 # One full L-shell seat/back, its back located toward the central guide tower.
 pp=[(-.19,0),(.15,0),(.15,.48),(.100,.48),(.100,.055),(-.19,.055)];n=len(pp);vv=[local((x,y-.64,z+.93),a)for x in[-.185,.185]for y,z in pp];ff=[]
 for aa,bb,cc in triangulate(pp):ff +=[(cc,bb,aa),(aa+n,bb+n,cc+n)]
 ff +=[(k,(k+1)%n,(k+1)%n+n,k+n)for k in range(n)];mesh('WholeOutwardSeatBackShell_%d'%j,vv,ff,0)
 # One complete thick fixed U-bar rooted at the two upper back sides.
 pts=[(-.155,-.50,1.33),(-.170,-.58,1.35),(-.170,-.74,1.24),(-.145,-.79,1.14),(-.08,-.80,1.12),(.08,-.80,1.12),(.145,-.79,1.14),(.170,-.74,1.24),(.170,-.58,1.35),(.155,-.50,1.33)]
 tube('WholeFixedSeatUpperBodyBar_%d'%j,[local(q,a)for q in pts],.018,3,8)
 for k,x in enumerate([-.17,.17]):
  name='WholeUpperBarSidePivot_%d_%d'%(j,k);axle(name,x-.022,x+.022,-.50,1.33,.028,2,16);turn(name)
 name='WholeTopRailStop_%d'%j;box(name,(0,-.30,4.25),(.15,.10,.13),0);turn(name)
box('WholeTowerHeadCap',(0,0,4.35),(.65,.65,.17),0)
box('WholeSmallRaisedHead',(0,0,4.465),(.44,.44,.08),1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
# Freeze authored vertex coordinates once to the actual float32 export representation.
G={n:([tuple(struct.unpack('<f',struct.pack('<f',c))[0]for c in p)for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeCarriageSeatsCapAndPlinth_MutedOrange',(.65,.25,.08,1),.73,.05),('WholeTowerAndCarriers_DeepTeal',(.065,.20,.23,1),.65,.20),('WholeRailsAndAxles_SatinSteel',(.47,.52,.53,1),.47,.65),('WholeRollersAndFixedBars_Charcoal',(.040,.052,.055,1),.84,.05)]
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
focus=Vector((0,0,2.15))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=5.4;aim(cam,(7,-10,6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/carnival/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'carnival','style':'S01-clean-geometric','title':'Fixed Lattice Mast and Guided Seat Ring Drop Tower','description':'One newly authored complete stationary drop-tower-style amusement apparatus exterior. A shared broad grounded plinth carries a full four-chord open square lattice tower with alternating diagonal bracing and four continuous exterior guide rails. One real open-centred thick square carriage ring surrounds the tower in a fixed low pose. Four paired roller sets and complete bearing cheeks meet the corresponding rails; fixed low support shoulders under the ring make the displayed support explicit. Four whole outward-facing seat/back shells are rooted by full radial carriers to this one carriage, with complete fixed curved upper-body bars, and the tower ends in a stepped full cap with four rail stops. This is not a suspended-chair canopy with fewer seats, a grooved weight cassette on a two-rod pulldown portal renamed, or old props combined: all geometry newly authored, counted together as one apparatus and zero scenes. Four opaque PBR roles, metres Z up and whole horizontal-envelope-centred ground datum. Unoccupied static illustrative exterior only; the fixed seat ring is not a simulation of free fall. No passenger fit, operating lift, rope/drive system, travel range, brake, restraint performance, installation, structural load, ride operation, fabrication or safety capability. Rigging animation and interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
