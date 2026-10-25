import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='fishing-fixed-bail-rotor-front-spool-and-curved-foot-reel-01'
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



# Newly drawn whole front-spool/bail reel, resting on the complete mounting foot.
p=[(-.018,-.071),(.018,-.071),(.023,-.05),(.023,.05),(.017,.080),(-.017,.080),(-.023,.05),(-.023,-.05)];n=len(p);v=[(x,y,z)for z in[0,.014]for x,y in p];fs=[]
for a,b,c in triangulate(p):fs.extend([(c,b,a),(a+n,b+n,c+n)])
fs +=[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh('WholeGroundFootMountingShoe',v,fs,0)
# One continuous thick curved stem: full extruded side outline with no detached elbow.
p=[(-.012,.010),(.035,.010),(.072,.045),(.082,.083),(.065,.117),(.042,.121),(.052,.078),(.044,.055),(.018,.032),(-.012,.027)]
if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:p.reverse()
n=len(p);v=[(x,y,z)for x in[-.011,.011]for y,z in p];fs=[]
for a,b,c in triangulate(p):fs.extend([(c,b,a),(a+n,b+n,c+n)])
fs +=[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh('WholeCurvedMountingStem',v,fs,0)
# Rounded side gearbox shell appearance, one closed finite exterior solid.
pp=[(-.026,.119),(-.030,.155),(-.010,.188),(.042,.194),(.087,.173),(.098,.137),(.077,.105),(.025,.099)]
v=[];fs=[]
for x,scale in[(-.030,.82),(-.024,1),(.024,1),(.030,.82)]:
 for y,z in pp:v.append((x,.034+(y-.034)*scale,.147+(z-.147)*scale))
N=len(pp);fs=[tuple(reversed(range(N))),tuple(3*N+i for i in range(N))]
for k in range(3):
 for j in range(N):q=(j+1)%N;fs.append((k*N+j,k*N+q,(k+1)*N+q,(k+1)*N+j))
mesh('WholeRoundedGearHousing',v,fs,0)
def axial_profile(name,profile,mat,n=32):
 lathe_z(name,0,0,profile,mat,n);v,f,m=G[name];G[name]=([(x,-z,.162+y)for x,y,z in v],f,m)
axial_profile('WholeOpenFrontCupRotor',[(0,.025),(.044,.025),(.055,.043),(.055,.076),(.048,.076),(.048,.046),(.038,.035),(0,.035)],0,32)
cyly('WholeFrontContinuousSpoolShaft',-.147,-.019,0,.162,.008,2,16)
axial_profile('WholeSteppedRecessedFrontSpool',[(.008,.063),(.040,.063),(.046,.069),(.046,.077),(.035,.081),(.035,.112),(.048,.117),(.048,.127),(.042,.131),(.018,.131),(.018,.120),(.008,.120)],1,32)
cyly('WholeFrontKnob',-.143,-.122,0,.162,.017,3,20)
for k,s in enumerate([-1,1]):
 beam('WholeRotorBailArm_%d'%k,(s*.051,-.056,.162),(s*.061,-.112,.162),.014,0)
 axle('WholeBailPivotCap_%d'%k,s*.052,s*.069,-.108,.162,.012,2,16)
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

pts=[(.061*math.cos(math.pi*j/24),-.112-.040*math.sin(math.pi*j/24),.162+.061*math.sin(math.pi*j/24))for j in range(25)]
tube('WholeContinuousFrontBailArch',pts,.0035,2,8)
axle('WholeTransverseSideCrankAxis',.022,.062,.040,.147,.010,2,16)
beam('WholeOffsetSideCrankArm',(.056,.040,.147),(.083,.040,.062),.012,2)
axle('WholeSideCrankGrip',.079,.130,.040,.062,.015,3,16)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeHousingRotorStemAndFoot_DeepTeal',(.055,.22,.22,1),.49,.28),('WholeFrontSpool_DullBrass',(.58,.43,.19,1),.44,.60),('WholeBailAxlesAndCrank_SatinSteel',(.50,.54,.55,1),.37,.7),('WholeKnobAndGrip_Graphite',(.045,.052,.055,1),.86,0)]
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
focus=Vector((0,0,.12))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.39;aim(cam,(3,-5,3));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/fishing/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'fishing','style':'S01-clean-geometric','title':'Fixed Bail Rotor Front Spool and Curved Foot Reel','description':'One newly authored complete empty spinning-reel-style exterior in a fixed inverted display pose on its own flat mounting foot. A continuous curved stem connects the full foot to a thick rounded side gear-housing appearance. The front axis supports one open-front cup rotor, an independently stepped spool with a genuine annular winding recess and a front knob. Two full rotor arms carry one continuous semicircular bail-like wire around and ahead of the spool, with visible clearance from the spool lip. A separate transverse side crank and axial handgrip complete the whole reel. This is not the old fishing rod kit with the rod removed or the old bare double-flange winch rescaled: the curved stem, side housing and front cup/bail relation are new geometry. No old visible meshes imported. One model zero scenes, four opaque constant PBR roles, metres Z up and complete horizontal-envelope-centred ground datum. Static illustrative equipment exterior only: no internal gears, line, winding, drag, braking, bail motion, spool oscillation, mounting compatibility, manufacture, fishing or safety capability.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
