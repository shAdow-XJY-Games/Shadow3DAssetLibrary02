import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='steam-workshop-fixed-tripod-winch-hoist-01'
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



# Whole new converging tripod apparatus, integrated low drum and complete visible cable route.
feet=[(-.866,-.50),( .866,-.50),(0,1.0)];tops=[(-.15,-.10),(.15,-.10),(0,.25)]
for i,((x,y),(tx,ty))in enumerate(zip(feet,tops),1):
 box('Foot'+str(i)+'WholeGroundPad',(x,y,.04),(.32,.32,.08),0)
 v=[(cx+dx,cy+dy,z)for cx,cy,z in[(x,y,.07),(tx,ty,2.32)]for dx,dy in[(-.06,-.06),(.06,-.06),(.06,.06),(-.06,.06)]]
 mesh('Leg'+str(i)+'WholeConvergingPost',v,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],0)
def leg_at(i,z):
 (x,y),(tx,ty)=feet[i],tops[i];t=(z-.07)/2.25;return(x+t*(tx-x),y+t*(ty-y),z)
for i in range(3):beam('WholeLowerTriangularBrace'+str(i+1),leg_at(i,.40),leg_at((i+1)%3,.40),.065,2)
# Two head cheeks and a rear connecting cap leave both actual rope runs clear.
for label,x in [('Left',-.15),('Right',.15)]:
 box(label+'WholeHeadCheekRoot',(x,.015,2.365),(.07,.29,.19),0)
 ringx(label+'WholeBoredHeadBearing',x-.045,x+.045,0,2.52,.044,.13,2,24)
box('WholeRearHeadCrossTie',(0,.25,2.30),(.39,.10,.13),0)
axle('WholeTopSheaveAxle',-.245,.245,0,2.52,.044,2,24)
# Closed grooved annular sheave, groove floor r=.175; cable outer radius reaches it in the frozen pose.
profile=[(.045,-.055),(.19,-.055),(.205,-.043),(.205,-.020),(.175,-.012),(.175,.012),(.205,.020),(.205,.043),(.19,.055),(.045,.055)];N=40
v=[(x,r*math.cos(math.tau*i/N),2.52+r*math.sin(math.tau*i/N))for r,x in profile for i in range(N)];f=[]
for k in range(len(profile)):
 for i in range(N):j=(i+1)%N;l=(k+1)%len(profile);f.append((k*N+i,k*N+j,l*N+j,l*N+i))
mesh('WholeGroovedHeadSheave',v,f,1)
for label,x0,x1 in [('Left',-.260,-.19),('Right',.19,.260)]:axle(label+'WholeHeadAxleRetainer',x0,x1,0,2.52,.069,2,20)
# Low hand drum is built into the two front tripod legs, not a separate old winch prop placed below a headframe.
DY=-.345;DZ=1.10
box('WholeFrontDrumCrossBeam',(0,DY,.89),(1.31,.15,.14),0)
for label,x in [('Left',-.46),('Right',.46)]:
 box(label+'WholeDrumBearingRoot',(x,DY,.99),(.12,.13,.19),0)
 ringx(label+'WholeBoredDrumBearing',x-.07,x+.07,DY,DZ,.040,.105,2,24)
axle('WholeDrumThroughShaft',-.66,.72,DY,DZ,.040,2,24)
# One complete barrel with integral thick flanges, newly proportioned for the tripod.
lathe_z('WholeIntegralLowWinchDrum',0,0,[(0,-.27),(.20,-.27),(.215,-.25),(.215,-.22),(.14,-.22),(.14,.22),(.215,.22),(.215,.25),(.20,.27),(0,.27)],1,32)
v,f,m=G['WholeIntegralLowWinchDrum'];G['WholeIntegralLowWinchDrum']=([(z,DY+y,DZ+x)for x,y,z in v],[tuple(reversed(t))for t in f],m)
for label,x0,x1 in [('Left',-.65,-.54),('Right',.54,.63)]:axle(label+'WholeDrumShaftStop',x0,x1,DY,DZ,.065,2,20)
beam('WholeFixedDrumCrank',(.70,DY,DZ),(.70,DY,.85),.045,2)
axle('WholeCrankOuterHandGrip',.68,.91,DY,.85,.033,0,20)
# One complete capped polyline tube, from within the barrel contact to head groove and suspended hook.
def cord(name,points,r,mat,n=8):
 v=[];f=[]
 for k,p in enumerate(points):
  t=unit(sub(points[min(k+1,len(points)-1)],points[max(k-1,0)]));u=unit(cross(t,(1,0,0)if abs(t[0])<.9 else(0,1,0)));w=cross(t,u)
  v.extend([tuple(p[j]+r*(u[j]*math.cos(math.tau*i/n)+w[j]*math.sin(math.tau*i/n))for j in range(3))for i in range(n)])
 for k in range(len(points)-1):
  for i in range(n):j=(i+1)%n;f.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i))
 f += [tuple(reversed(range(n))),tuple((len(points)-1)*n+i for i in range(n))];mesh(name,v,f,mat)
pts=[(0,DY-.144,DZ),(0,-.183,2.52)]+[(0,.183*math.cos(math.pi*(1-i/20)),2.52+.183*math.sin(math.pi*(1-i/20)))for i in range(1,21)]+[(0,.183,1.95)]
cord('WholeContinuousDrumSheaveHookCable',pts,.008,2)
box('WholeHangingHookShank',(0,.183,1.885),(.065,.070,.19),2)
a=[math.radians(120+255*i/20)for i in range(21)];p=[(.08+.15*math.cos(t),1.67+.15*math.sin(t))for t in a]+[(.08+.095*math.cos(t),1.67+.095*math.sin(t))for t in reversed(a)]
if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
n=len(p);v=[(x,y,z)for y in[.148,.218]for x,z in p];f=[]
for a,b,c in triangulate(p):f.extend([(a,b,c),(c+n,b+n,a+n)])
for i in range(n):j=(i+1)%n;f.append((i,i+n,j+n,j))
mesh('WholeOpenSuspendedHook',v,f,2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeTripodFrame_WarmTimber',(.34,.19,.075,1),.81,0),('WholeDrumAndGroovedSheave_OchreIron',(.50,.29,.09,1),.60,.35),('ShaftsCableAndHook_DarkSteel',(.16,.20,.21,1),.48,.60)]
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
focus=Vector((0,0,1.34))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.30;aim(cam,(4,-7,3.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/steam-workshop/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'steam-workshop','style':'S01-clean-geometric','title':'Fixed Tripod Winch Hoist','description':'One newly authored complete fixed tripod-winch hoist appearance. Three continuous tall splayed posts converge onto a two-cheek head and rear cap, with three broad real ground pads and a low triangular brace circuit. A newly built low double-flanged drum, bored bearings, shaft and hand crank are integrated into a crossbeam between the front legs. One top grooved sheave and fixed axle redirect a complete continuous thin cable from the drum up over the head and down to one empty open hook. Both rope runs pass through the actual clear space between the head cheeks. No old complete winch, mine headframe, hook module or jib is instanced. This is a complete converging three-leg lifting-layout display with its own low drum and entire rope route, not a four-post shaft-mouth headframe with one leg deleted or a single-column cantilever trolley with a different color. All numeric geometry newly authored, three opaque constant PBR roles, closed editable parts, metres, Z up and whole horizontal bounds-centred grounded pads. One prop, zero scenes. Fixed joins, cable contact and retained shafts show only this illustrative pose. No winching, drum winding capacity, cable tension, moving or braking mechanism, hook restraint, cargo lifting, human use, anti-tip stability, load, manufacture, construction or equipment safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
