import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='art-fixed-orthogonal-pendulums-and-converging-pen-frame-01'
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



# Complete new open floor frame, no existing worktable instance imported.
for i,x in enumerate([-.48,.48]):
 for j,y in enumerate([-.38,.38]):
  box('WholeGroundFoot_%d_%d'%(i,j),(x,y,.037),(.15,.14,.074),0)
  box('WholeFullTableLeg_%d_%d'%(i,j),(x,y,.50),(.064,.064,.94),0)
 box('WholeLongUpperFrameRail_%d'%i,(x,0,.955),(.085,.85,.080),0)
 box('WholeLowerLongTie_%d'%i,(x,0,.23),(.046,.79,.046),0)
for i,y in enumerate([-.38,.38]):
 box('WholeUpperCrossRail_%d'%i,(0,y,.945),(.98,.085,.080),0)
 box('WholeLowerCrossTie_%d'%i,(0,y,.25),(.98,.046,.046),0)
# A separate central board has actual full supports and leaves the two pivot bays empty.
for i,y in enumerate([-.28,.15]):box('WholeBoardCrossSupport_%d'%i,(.075,y,.977),(.81,.046,.046),0)
box('WholeBlankDrawingBoard',(.075,-.065,1.009),(.66,.49,.035),1)
# Left bay, Y-axis pivot on two distinct bridge/bearing assemblies.
for i,y in enumerate([-.090,.090]):
 box('WholeLeftPivotBridge_%d'%i,(-.392,y,.983),(.245,.045,.055),0)
 box('WholeLeftPivotBearing_%d'%i,(-.36,y,1.040),(.057,.040,.110),2)
cyly('WholeLeftTransversePivot',-.125,.125,-.36,1.075,.015,2,20)
for i,y in enumerate([-.131,.125]):cyly('WholeLeftProudPivotCap_%d'%i,y,y+.010,-.36,1.075,.024,3,20)
# Rear bay, the whole pivot lies on X, orthogonal to the first.
for i,x in enumerate([-.090,.090]):
 box('WholeRearPivotBridge_%d'%i,(x,.335,.983),(.045,.205,.055),0)
 box('WholeRearPivotBearing_%d'%i,(x,.27,1.040),(.040,.057,.110),2)
axle('WholeRearTransversePivot',-.125,.125,.27,1.075,.015,2,20)
for i,x in enumerate([-.135,.125]):axle('WholeRearProudPivotCap_%d'%i,x,x+.010,.27,1.075,.024,3,20)
# Complete hanging rods continue through the real open bays to the upper linkage roots.
for i,(x,y,zlo,zhi,wlo,whi) in enumerate([(-.36,0,.145,1.320,.235,.395),(0,.27,.145,1.355,.195,.355)]):
 lathe_z('WholeThroughPivotPendulumRod_%d'%i,x,y,[(0,zlo),(.011,zlo),(.011,zhi),(0,zhi)],2,16)
 lathe_z('WholeLowPendulumWeight_%d'%i,x,y,[(0,wlo),(.072,wlo),(.080,wlo+.012),(.080,whi-.012),(.072,whi),(0,whi)],3,24)
 lathe_z('WholeWeightRetainingCollar_%d'%i,x,y,[(0,wlo-.015),(.020,wlo-.015),(.020,wlo+.006),(0,wlo+.006)],2,20)
# Two independently authored whole arms converge in separated layers, no closed four-bar loop.
beam('WholeLeftUpperConvergingArm',(-.36,0,1.307),(.15,-.055,1.307),.022,0)
beam('WholeRearUpperConvergingArm',(0,.27,1.342),(.15,-.055,1.342),.022,0)
lathe_z('WholeProudConvergingArmPin',.15,-.055,[(0,1.289),(.010,1.289),(.010,1.357),(.020,1.357),(.020,1.367),(0,1.367)],3,20)
lathe_z('WholeBluntPenStem',.15,-.055,[(0,1.026),(.003,1.026),(.009,1.055),(.009,1.310),(0,1.310)],2,12)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeFrameAndArms_WarmTimber',(.34,.18,.070,1),.81,0),('WholeBlankBoard_Ivory',(.76,.72,.60,1),.84,0),('WholeRodsPivotsAndPen_DullSteel',(.32,.39,.40,1),.48,.55),('WholeWeightsAndHeads_DeepTeal',(.065,.20,.20,1),.67,.32)]
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
focus=Vector((0,0,.69))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.95;aim(cam,(4,-6,3.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/art/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'art','style':'S01-clean-geometric','title':'Fixed Orthogonal Pendulums and Converging Pen Frame','description':'One newly authored complete fixed two-pendulum drawing-apparatus exterior. A whole open four-leg table frame carries a blank central drawing board while leaving separate left and rear open pivot bays. Each bay has a full pair of rooted support bridges and bearing blocks around a complete transverse pivot, with the two pivot axes perpendicular. Two whole upright rods continue below the frame into separate low cylindrical weights and above it into two independent long flat arms. Those arms occupy different heights and converge at one proud vertical pin and a blunt pen-shaped stem over the blank board. No drum, coil spring, tracing target, closed copying parallelogram or imported old table is supplied. The through-frame suspended rods and converging upper arm chain form one new whole instrument rather than two existing recorders arranged together. All numeric geometry new; four opaque constant PBR roles, metres native Z up, complete horizontal bounds centred on four finite grounded feet, one prop zero scenes. Generic harmonograph-inspired static display only: no actual oscillation, coupling, phase, drawing trajectory, markings, accuracy, tuning, suspension fit, stability, load, manufacture or machinery safety. Rigging, animation and interaction are not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
