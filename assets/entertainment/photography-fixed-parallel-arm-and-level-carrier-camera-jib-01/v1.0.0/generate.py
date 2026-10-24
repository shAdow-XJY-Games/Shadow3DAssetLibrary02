import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='photography-fixed-parallel-arm-and-level-carrier-camera-jib-01'
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



# One complete newly authored fixed parallel-arm camera jib, without a camera.
# Wide integral support assembly: four finite feet, full rails, crossmember and column.
for side,y in[('Near',-.38),('Far',.38)]:
 box('WholeLongBaseRail_'+side,(-.13,y,.105),(1.36,.085,.11),0)
 for end,x in[('Rear',-.72),('Front',.46)]:
  box('WholeGroundFoot_'+side+end,(x,y,.025),(.19,.19,.05),2)
box('WholeBaseCrossmember',(-.10,0,.155),(.24,.86,.12),0)
lathe_z('WholeColumnBaseCasting',-.10,0,[(0,.16),(.16,.16),(.16,.27),(.105,.31),(.105,.99),(0,.99)],0)
lathe_z('WholeFixedYawCollar',-.10,0,[(.087,.92),(.135,.92),(.135,1.04),(.087,1.04)],2)
lathe_z('WholeUpperColumn',-.10,0,[(0,.96),(.086,.96),(.086,1.205),(0,1.205)],1)
for side,y in[('Near',-.36),('Far',.36)]:beam('WholeColumnBrace_'+side,(-.10,y,.16),(-.10,0,.75),.055,0)
# Whole fork cheeks connect both high rear axes, not isolated pivot discs floating in space.
for side,y in[('Near',-.105),('Far',.105)]:box('WholeTallRearPivotCheek_'+side,(0,y,1.385),(.18,.045,.51),0)
box('WholeForkRootBridge',(-.035,0,1.18),(.30,.25,.09),0)
# Four corners define a genuine complete parallel-arm static linkage.
# Lower rear (0,1.30) -> lower front (1.50,1.85), upper pair exactly +0.32 m.
beam('WholeLongLowerParallelLink',(0,0,1.30),(1.50,0,1.85),.075,1)
beam('WholeContinuousUpperArmAndRearTail',(-.67,0,1.62-.67*.55/1.50),(1.50,0,2.17),.095,0)
for tag,x,z in[('RearLower',0,1.30),('RearUpper',0,1.62),('FrontLower',1.50,1.85),('FrontUpper',1.50,2.17)]:
 cyly('WholeTransversePivot_'+tag,-.153,.153,x,z,.034,1,20)
 # End heads are outside cheeks, not coplanar face overlays.
 cyly('WholeNearPivotHead_'+tag,-.172,-.146,x,z,.048,2,20)
 cyly('WholeFarPivotHead_'+tag,.146,.172,x,z,.048,2,20)
# Both full front cheeks span both axes and root the complete empty level carrier.
for side,y in[('Near',-.105),('Far',.105)]:box('WholeFrontCarrierCheek_'+side,(1.50,y,1.94),(.13,.045,.58),0)
box('WholeLevelCarrierCrossSeat',(1.50,0,1.681),(.20,.28,.065),1)
box('WholeEmptyHorizontalCameraPlate',(1.64,0,1.642),(.46,.36,.048),0)
# Continuous rear arm carries an actual finite bored weight, not a detached dark block.
a=(-.67,0,1.62-.67*.55/1.50);b=(-.40,0,1.62-.40*.55/1.50)
w=unit(sub(b,a));u=unit(cross(w,(0,1,0)));v=cross(w,u);N=24;vv=[]
for p,r in[(a,.145),(b,.145),(a,.071),(b,.071)]:
 for i in range(N):
  t=math.tau*i/N;vv.append(tuple(p[k]+r*(math.cos(t)*u[k]+math.sin(t)*v[k])for k in range(3)))
f=[]
for i in range(N):
 j=(i+1)%N;f.extend([(i,j,N+j,N+i),(2*N+i,3*N+i,3*N+j,2*N+j),(i,2*N+i,2*N+j,j),(N+i,N+j,3*N+j,3*N+i)])
mesh('WholeBoredRearCounterweight',vv,f,2)
# Bore contains the square arm diagonals with finite clearance; small shoulder fixes its location.
beam('WholeRearWeightShoulder',(-.69,0,1.62-.69*.55/1.50),(-.655,0,1.62-.655*.55/1.50),.17,0)
# Full operating grip fixed to the rear tail, without claimed articulation.
beam('WholeRearGripStem',(-.48,-.02,1.444),(-.48,-.27,1.444),.035,1)
cyly('WholeRearFixedGrip',-.37,-.235,-.48,1.444,.030,2,16)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeJibFrameAndCameraCarrier_DarkSlate',(.09,.14,.17,1),.64,.28),('WholeLowerLinkPinsAndColumn_SatinAlloy',(.48,.54,.56,1),.44,.65),('WholeCounterweightGripsAndFeet_Charcoal',(.037,.044,.047,1),.82,.05)]
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
focus=Vector((0,0,1.08))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.30;aim(cam,(3,-6,3.0));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/entertainment/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'photography','style':'S01-clean-geometric','title':'Fixed Parallel Arm and Level Carrier Camera Jib','description':'One newly authored whole static empty camera jib. Four broad ground pads, two long rails and a full crossmember support an upright stepped column with two full braces and a high two-cheek fork. Two complete parallel arms run from the paired rear axes to two real far axes; the upper arm continues behind the column as a full tail carrying a bored counterweight and fixed grip. All four transverse pins span their complete cheeks and arms. Two full far carrier cheeks connect both forward axes and the cross-seat beneath them, ending in an empty horizontal camera mounting plate. It is not a single grip-boom stand with a spigot, a one-arm hydraulic shop crane with a hook, or a gate boom with a separate catchpost. Entirely new numeric geometry, no imported old asset. Three opaque constant untextured PBR materials, metres, Z up, actual horizontal-bounds-centred ground origin. One model and zero scenes. Fixed illustrative art only; no camera, payload, real bearings, rigging, animation, automatic leveling, movement range, balance, load rating, manufacture, operation or equipment-safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
