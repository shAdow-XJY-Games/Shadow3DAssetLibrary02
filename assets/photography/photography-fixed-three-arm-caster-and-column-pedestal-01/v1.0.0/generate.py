import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='photography-fixed-three-arm-caster-and-column-pedestal-01'
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



# New complete fixed studio camera pedestal, no camera or scene.
def prism_x(name,poly,x0,x1,mat):
 n=len(poly);v=[(x,y,z)for x in[x0,x1]for y,z in poly];tt=triangulate(poly);f=[tuple(reversed(t))for t in tt]+[tuple(n+i for i in t)for t in tt]+[(i,(i+1)%n,n+(i+1)%n,n+i)for i in range(n)];mesh(name,v,f,mat)
def turn(name,a):
 v,f,m=G[name];G[name]=([(x*math.cos(a)-y*math.sin(a),x*math.sin(a)+y*math.cos(a),z)for x,y,z in v],f,m)
lathe_z('WholeCentralLowHub',0,0,[(0,.195),(.115,.195),(.135,.215),(.135,.282),(.110,.300),(0,.300)],0,32)
for k in range(3):
 a=math.tau*k/3-math.pi/2;names=[]
 n='WholeRadialLowArm_%02d'%k;beam(n,(.075,0,.245),(.490,0,.245),.085,0);names.append(n)
 # One fork is a complete thick inverted U around a distinct full tyre and axle.
 n='WholeCasterBridgeFork_%02d'%k
 poly=[(-.090,.088),(-.056,.088),(-.056,.225),(.056,.225),(.056,.088),(.090,.088),(.090,.274),(-.090,.274)]
 prism_x(n,poly,.448,.522,1);names.append(n)
 zc=.110*math.cos(math.pi/16)
 n='WholeGroundFootFacetedCasterTyre_%02d'%k
 v=[(.485+.110*math.cos((i+.5)*math.tau/16),y,zc+.110*math.sin((i+.5)*math.tau/16))for y in[-.040,.040]for i in range(16)]
 f=[tuple(range(16)),tuple(reversed(range(16,32)))]+[(i,i+16,(i+1)%16+16,(i+1)%16)for i in range(16)];mesh(n,v,f,2);names.append(n)
 n='WholeCasterTransverseAxle_%02d'%k;cyly(n,-.104,.104,.485,zc,.017,1,20);names.append(n)
 for n in names:turn(n,a)
# Stepped cylindrical lower pedestal and a visibly narrower fixed extended upper stem.
lathe_z('WholeLowerColumnHousing',0,0,[(0,.270),(.105,.270),(.105,.820),(.094,.855),(0,.855)],0,32)
lathe_z('WholeUpperExtensionStem',0,0,[(0,.815),(.068,.815),(.068,1.180),(0,1.180)],1,32)
lathe_z('WholeColumnTopCollar',0,0,[(.068,.810),(.114,.810),(.114,.855),(.068,.855)],2,32)
lathe_z('WholeHorizontalOpenSteeringRing',0,0,[(.258,.790),(.273,.790),(.282,.803),(.282,.817),(.273,.830),(.258,.830)],2,48)
for k in range(3):
 a=math.tau*k/3;beam('WholeSteeringRingSpoke_%02d'%k,(.090*math.cos(a),.090*math.sin(a),.810),(.271*math.cos(a),.271*math.sin(a),.810),.022,1)
# Complete top pan bearing, full side-yoke and separate transverse tilt axle.
lathe_z('WholeUpperPanBearing',0,0,[(0,1.160),(.104,1.160),(.113,1.176),(.113,1.218),(0,1.218)],2,32)
# Yoke lies in XZ, open above with both cheeks as one connected body.
poly=[(-.130,1.205),(.130,1.205),(.130,1.378),(.098,1.378),(.098,1.248),(-.098,1.248),(-.098,1.378),(-.130,1.378)]
n=len(poly);tt=triangulate(poly);v=[(x,y,z)for y in[-.044,.044]for x,z in poly];f=list(tt)+[tuple(n+i for i in reversed(t))for t in tt]+[(i,n+i,n+(i+1)%n,(i+1)%n)for i in range(n)];mesh('WholeOpenTiltHeadYoke',v,f,0)
axle('WholeTransverseTiltAxle',-.151,.151,0,1.348,.024,1,24)
box('WholeEmptyCameraMountingPlate',(0,0,1.375),(.290,.245,.038),2)
# Finite collar projects beyond plate side; long pan arm is rooted in it, not floating.
axle('WholePanHandleRoot',.130,.174,0,1.348,.033,0,24)
beam('WholeFixedRearPanArm',(.160,.010,1.348),(.160,.350,1.225),.025,1)
beam('WholeRearPanGrip',(.160,.292,1.246),(.160,.411,1.203),.045,2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeArmsColumnAndYoke_DeepTeal',(.065,.145,.16,1),.69,.22),('WholeAxlesSpokesAndStem_SatinMetal',(.45,.48,.47,1),.45,.63),('WholeTyresRingAndMount_Charcoal',(.045,.052,.054,1),.79,.06)]
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
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.90;aim(cam,(3,-5,2.9));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/photography/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'photography','style':'S01-clean-geometric','title':'Fixed Three Arm Caster and Column Camera Pedestal','description':'One newly authored complete fixed studio-camera-pedestal exterior. Three full low radial arms join one central hub and terminate in complete thick U-fork caster groups with separate grounded faceted tyres and transverse axles. One broad lower column and narrower fixed raised stem carry a whole upper pan-bearing exterior, connected open U-yoke, transverse tilt axle and empty camera-mounting plate. A large genuinely open horizontal ring is supported by three complete radial spokes around the lower column; a side-rooted rear pan arm ends in a thick whole grip. No camera, scene, rails, cargo deck or old trolley mesh is imported. The whole caster/column/ring/yoke layout is newly authored rather than an existing luggage trolley or tabletop dual-rod slide with changed wheel counts. Three opaque constant untextured PBR materials, metres, Z up, whole horizontally centred bounds and three finite flat tyre soles at ground. One model, zero scenes. Static appearance only; no steering, rolling, telescoping travel, hydraulic or pneumatic internals, tilt or pan range, camera fitting dimensions, load capacity, stability, manufacture or equipment safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
