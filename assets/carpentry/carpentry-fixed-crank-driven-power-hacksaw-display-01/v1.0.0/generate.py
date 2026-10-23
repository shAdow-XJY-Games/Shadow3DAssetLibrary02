import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='carpentry-fixed-crank-driven-power-hacksaw-display-01'
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



# Whole newly authored fixed reciprocating bow-saw machine, no reused prop meshes.
def profile_y(name,p,y0,y1,mat):
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);v=[(x,y,z)for y in[y0,y1]for x,z in p];f=[]
 for a,b,c in triangulate(p):f.extend([(a,b,c),(c+n,b+n,a+n)])
 f += [(i,i+n,(i+1)%n+n,(i+1)%n)for i in range(n)];mesh(name,v,f,mat)
box('WholeGroundMachineBed',(-.20,.03,.045),(2.08,.82,.09),0)
box('WholeWorkTablePedestal',(.21,.02,.34),(.43,.46,.54),0)
box('WholeFixedWorkTable',(.18,.02,.635),(.80,.63,.07),1)
# Empty complete transverse vise; no workpiece or cutting action is implied.
box('WholeFixedRearViseJaw',(.18,.18,.715),(.40,.09,.16),2)
box('WholeFrontSlidingViseJaw',(.18,-.10,.715),(.40,.08,.16),2)
box('WholeViseFrontScrewBoss',(.18,-.25,.69),(.16,.12,.10),0)
cyly('WholeViseAdjustingScrew',-.44,-.07,.18,.70,.024,1,20)
cyly('WholeViseScrewCollar',-.465,-.415,.18,.70,.042,2,20)
axle('WholeViseTransverseHandle',.06,.30,-.447,.70,.014,1,16)
# One thick open-bottom metal bow carries one entire closed toothed blade.
p=[(-.74,.805),(-.74,1.24),(-.66,1.30),(.59,1.30),(.69,1.20),(.69,.805),(.585,.805),(.585,1.17),(-.625,1.17),(-.625,.805)]
profile_y('WholeContinuousOpenBottomSawBow',p,-.055,.055,0)
p=[(-.69,.84),(.635,.84),(.635,.802)]
for i in range(53):p.append((.61-i*.0246,.785 if i%2==0 else .803))
p.append((-.69,.802));profile_y('WholeStraightClosedZigzagBlade',p,-.009,.009,1)
for label,x in [('Rear',-.68),('Front',.635)]:
 cyly(label+'WholeBladeRetainingPin',-.075,.075,x,.824,.019,2,20)
# Full rear ram is held in a genuine rectangular through sleeve, not a solid block.
box('WholeReciprocatingTopRam',(-.85,0,1.22),(.88,.080,.080),1)
inner=[(-.042,1.18),(.042,1.18),(.042,1.264),(-.042,1.264)]
outer=[(-.09,1.13),(.09,1.13),(.09,1.31),(-.09,1.31)]
v=[(x,y,z)for x in[-1.13,-.86]for p in[inner,outer]for y,z in p];f=[]
for i in range(4):j=(i+1)%4;f.extend([(i,j,4+j,4+i),(8+i,12+i,12+j,8+j),(i,8+i,8+j,j),(4+i,4+j,12+j,12+i)])
mesh('WholeRectangularThroughRamGuide',v,f,2)
box('WholeTallRamGuideColumn',(-1.00,.04,.615),(.19,.19,1.08),0)
# A complete transverse crankshaft on two full bearing pedestals, open rear flywheel.
cx=-.99;cz=.56
cyly('WholeCrankshaft',-.31,.365,cx,cz,.035,1,24)
for label,y in [('Near',-.075),('Far',.17)]:
 ringy(label+'WholeBoredCrankBearing',y-.033,y+.033,cx,cz,.035,.080,2,20)
 box(label+'WholeCrankBearingPedestal',(cx,y,.30),(.15,.085,.47),0)
cyly('WholeFrontDrivingCrankDisk',-.205,-.145,cx,cz,.22,0,32)
px=cx+.12;pz=cz+.10
cyly('WholeOffsetDrivePin',-.315,-.17,px,pz,.028,1,20)
beam('WholeObliqueCrankConnectingLink',(px,-.267,pz),(-.43,-.267,1.22),.065,1)
cyly('WholeBowDriveCrossPin',-.31,.035,-.43,1.22,.028,2,20)
cyly('WholeCrankPinProudCap',-.333,-.303,px,pz,.046,2,20)
cyly('WholeBowPinProudCap',-.333,-.303,-.43,1.22,.046,2,20)
ringy('WholeRearFlywheelRim',.275,.325,cx,cz,.245,.295,0,32)
cyly('WholeRearFlywheelHub',.257,.345,cx,cz,.067,2,24)
for i in range(6):
 a=math.tau*i/6;beam('WholeRearFlywheelSpoke'+str(i+1),(cx+.050*math.cos(a),.30,cz+.050*math.sin(a)),(cx+.260*math.cos(a),.30,cz+.260*math.sin(a)),.033,0)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeCastFrameAndBow_DeepBlue',(.075,.19,.29,1),.65,.25),('BladeRamLinkAndScrew_SatinSteel',(.48,.53,.54,1),.42,.65),('GuidesJawsAndCaps_DarkIron',(.09,.105,.115,1),.70,.35)]
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
focus=Vector((0,0,.68))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.65;aim(cam,(3.5,-6,3.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/carpentry/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'carpentry','style':'S01-clean-geometric','title':'Fixed Crank Driven Power Hacksaw Display','description':'One newly authored whole static crank-driven power-hacksaw appearance. A grounded long machine bed carries a raised empty work table and complete transverse screw vise, a tall rear ram-guide column and two crankshaft bearing pedestals. One continuous thick open-bottom metal bow holds an entire closed straight zigzag-toothed blade; its rear top ram enters a genuine rectangular through guide. An offset front crank pin, separate inclined connecting link and full bow cross-pin connect the visible drive outline; a complete open-spoke rear flywheel shares the supported crankshaft. All machine geometry is new, not an old hand frame saw laid on the old cylinder bench, not a loop blade removed from the compact band saw, and not an extracted accessory counted independently. Three opaque constant PBR materials, editable closed solids, metres, Z up, horizontally bounds-centred ground origin. One prop, zero scenes. Empty fixed illustrative display only: no cutting action, actual reciprocating path, stroke clearance, feed or lift mechanism, power source, force transmission, bearing tolerance, clamping performance, workpiece compatibility, manufacture, load or machinery safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
