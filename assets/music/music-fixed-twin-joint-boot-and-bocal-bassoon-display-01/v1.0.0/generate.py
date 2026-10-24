import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='music-fixed-twin-joint-boot-and-bocal-bassoon-display-01'
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



# Complete two-bore boot and unequal long wooden joints; no borrowed U-horn mesh.
# The boot has two genuine blind insertion bores. Hidden acoustic return is not claimed.
v=[];f=[];ids={};N=24;outeredges=[]
def V(p):
 key=tuple(round(c,9)for c in p)
 if key not in ids:ids[key]=len(v);v.append(key)
 return ids[key]
for x in[-.060,.060]:
 outer=[];inner=[];lower=[]
 for j in range(N):
  a=math.tau*j/N;co,si=math.cos(a),math.sin(a);r=min(.060/max(abs(co),1e-15),.065/max(abs(si),1e-15));outer.append(V((x+r*co,r*si,.30)));inner.append(V((x+.042*co,.042*si,.30)));lower.append(V((x+.042*co,.042*si,.14)))
 c=V((x,0,.14))
 for i in range(N):
  j=(i+1)%N;f.extend([(outer[i],outer[j],inner[j],inner[i]),(inner[i],inner[j],lower[j],lower[i]),(c,lower[i],lower[j])]);outeredges.append((outer[i],outer[j]))
edgecounts={}
for a,b in outeredges:edgecounts.setdefault(tuple(sorted((a,b))),[]).append((a,b))
c=V((0,0,.10))
for e in edgecounts.values():
 if len(e)!=1:continue
 a,b=e[0];aa=V((v[a][0],v[a][1],.10));bb=V((v[b][0],v[b][1],.10));f.extend([(b,a,aa,bb),(c,bb,aa)])
mesh('WholeTwinBlindBoreBootJoint',v,f,0)
# Each full long joint is hollow with distinct changing outer and bore profiles.
lathe_z('WholeLongBassJointAndSmallOpenBell',.060,0,[(.039,.135),(.039,.33),(.037,.63),(.035,1.05),(.038,1.25),(.047,1.34),(.048,1.38),(.040,1.38),(.039,1.34),(.030,1.25),(.027,1.05),(.029,.63),(.031,.33),(.031,.135)],0,32)
lathe_z('WholeShortWingJoint',-.060,0,[(.039,.135),(.039,.33),(.033,.58),(.026,.84),(.021,1.04),(.014,1.04),(.019,.84),(.026,.58),(.031,.33),(.031,.135)],0,32)
for i,(x,z,r)in enumerate([(-.06,.34,.040),(.06,.34,.040),(.06,1.24,.039)]):lathe_z('WholeJointFerrule_'+str(i),x,0,[(r-.003,z-.018),(r+.004,z-.018),(r+.004,z+.018),(r-.003,z+.018)],1,24)
lathe_z('WholeBocalRootCollar',-.060,0,[(.0085,1.027),(.024,1.027),(.024,1.052),(.0085,1.052)],1,24)
# Entire narrow rising then forward-curving bocal has real bore and open end.
st=[(-.06,0,1.00),(-.06,0,1.09),(-.06,-.015,1.15),(-.06,-.045,1.19),(-.06,-.085,1.215),(-.06,-.135,1.22),(-.06,-.19,1.21),(-.06,-.23,1.19)];v=[];f=[];N=16
for i,p in enumerate(st):
 t=unit(sub(st[min(i+1,len(st)-1)],st[max(i-1,0)]));u=(1,0,0);w=cross(t,u)
 for r in[.009,.005]:
  for j in range(N):a=math.tau*j/N;v.append(tuple(p[k]+r*(u[k]*math.cos(a)+w[k]*math.sin(a))for k in range(3)))
for k in range(len(st)-1):
 for i in range(N):j=(i+1)%N;a=2*N*k+i;b=2*N*k+j;c=2*N*(k+1)+i;d=2*N*(k+1)+j;f.extend([(a,b,d,c),(a+N,c+N,d+N,b+N)])
for i in range(N):j=(i+1)%N;k=2*N*(len(st)-1);f.extend([(j,i,i+N,j+N),(k+i,k+j,k+j+N,k+i+N)])
mesh('WholeOpenCurvedBocal',v,f,1)
# Two complete long front key rods, fixed cups/levers and actual bearing roots.
for label,x,z0,z1,r0,r1,count in [('Bass',.06,.40,1.16,.038,.036,6),('Wing',-.06,.40,.93,.037,.024,5)]:
 beam(label+'WholeKeyRod',(x+.042,-.040,z0),(x+.042,-.040,z1),.006,1)
 for k,z in enumerate([z0,z1]):beam(label+'WholeRodBearing_'+str(k),(x+.01,-.022,z),(x+.045,-.040,z),.010,1)
 for k in range(count):
  u=(k+.5)/count;z=z0+u*(z1-z0);rr=r0+(r1-r0)*u
  cyly(label+'WholeClosedKeyCup_'+str(k),-rr-.015,-rr+.004,x,z,.018,1,16)
  cyly(label+'WholeKeyTouch_'+str(k),-rr-.020,-rr-.010,x,z,.010,2,16)
  beam(label+'WholeKeyLever_'+str(k),(x,-rr-.006,z),(x+.044,-.040,z),.006,1)
# A fixed display cradle supports boot and rear joint, not a player or instrument function.
box('WholeDisplayGroundFoot',(0,.025,.025),(.39,.32,.05),2)
box('WholeBootSupportBlock',(0,0,.075),(.21,.12,.055),2)
box('WholeRearDisplayPost',(0,.080,.43),(.028,.028,.77),2)
beam('WholeRearJointCradle',(0,.080,.79),(.06,.032,.79),.018,2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeWoodBootAndUnequalJoints_RedBrown',(.30,.095,.040,1),.62,0),('WholeBocalFerrulesAndKeys_SatinSilver',(.51,.54,.52,1),.37,.65),('KeyTouchesAndDisplaySupport_Charcoal',(.055,.065,.068,1),.77,0)]
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
focus=Vector((0,0,.70))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.66;aim(cam,(2.0,-6,2.4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/music/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':'Fixed Twin Joint Boot and Bocal Bassoon Display','description':'One newly authored complete fixed bassoon-style display. A single broad wooden boot has two real blind insertion bores receiving independently hollow unequal-height long tapered joints. The tall bass joint ends in a small genuinely open flared bell; the shorter wing joint receives a complete thin hollow curved bocal. Separate long key rods, actual bearing roots, fixed closed key cups and small touches run along both front joints, with full ferrules at joints. An entire low stand supports the boot and rear of the instrument. Unlike the old single continuous saxophone neck/body/bow/wide bell and the low looped valveless brass horn, this has a separate full double-bored boot, parallel unequal wooden joints, narrow upper bocal and two rooted exterior key assemblies. No old instrument mesh imported or scaled. Three opaque constant untextured PBR roles, metres, Z up and full horizontally bounds-centred ground origin. One complete prop, zero scenes. Static illustrative exterior only: hidden acoustic return passage, tone holes and reed internals are not modeled or claimed. No sound, tuning, playability, breath-flow continuity, key travel, actual instrument fit, manufacture, historical accuracy or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
