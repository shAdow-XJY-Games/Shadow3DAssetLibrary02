import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='toys-fixed-two-axis-open-maze-table-01'
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



# New whole tabletop two-axis maze, with a real connected perforated floor.
def perforated(name,x0,x1,y0,y1,holes,z0,z1,mat):
 xs=sorted(set([x0,x1]+[r[i]for r in holes for i in[0,1]]));ys=sorted(set([y0,y1]+[r[i]for r in holes for i in[2,3]]));v=[];f=[];vm={};edges={}
 def vi(p):
  if p not in vm:vm[p]=len(v);v.append(p)
  return vm[p]
 for a,b in zip(xs,xs[1:]):
  for c,d in zip(ys,ys[1:]):
   if any(r[0]<(a+b)/2<r[1]and r[2]<(c+d)/2<r[3]for r in holes):continue
   p=[(a,c),(b,c),(b,d),(a,d)];f.extend([tuple(vi((*q,z1))for q in p),tuple(vi((*q,z0))for q in reversed(p))])
   for u,w in zip(p,p[1:]+p[:1]):edges.setdefault(tuple(sorted([u,w])),[]).append((u,w))
 for es in edges.values():
  if len(es)==1:
   a,b=es[0];f.append(tuple(vi(p)for p in[(*a,z0),(*b,z0),(*b,z1),(*a,z1)]))
 mesh(name,v,f,mat)
box('WholeGroundedCollectionBase',(0,0,.025),(.98,.90,.05),0)
perforated('WholeContinuousOuterSupportBoxRim',-.486,.486,-.446,.446,[(-.445,.445,-.405,.405)],.035,.23,0)
# Middle open frame and front/rear Y pivots. Full fixed pose, not solved animated gimbal.
start=set(G)
perforated('WholeOpenIntermediateGimbalFrame',-.405,.405,-.365,.365,[(-.36,.36,-.32,.32)],.225,.255,1)
for tag,lo,hi in [('Front',-.47,-.35),('Back',.35,.44)]:cyly(tag+'WholeIntermediatePivot',lo,hi,0,.24,.014,2,20)
cyly('WholeFrontOuterAxisControlKnob',-.505,-.465,0,.24,.049,2,24)
# All parts below this marker rotate together about the inner X axis, including real holes/walls.
inner=set(G)
perforated('WholeMazeFloorWithThreeThroughDropApertures',-.34,.34,-.30,.30,[(-.223,-.177,-.143,-.097),(.107,.153,.077,.123),(.197,.243,-.223,-.177)],.218,.24,1)
for tag,c,size in [('Front',(0,-.293,.263),(.68,.014,.055)),('Back',(0,.293,.263),(.68,.014,.055)),('Left',(-.333,0,.263),(.014,.58,.055)),('Right',(.333,0,.263),(.014,.58,.055))]:box(tag+'WholeInnerMazeRail',c,size,0)
# Thick independent maze obstacles rooted below the complete playing floor.
walls=[(-.12,-.20,.35,.012),(.05,-.11,.012,.17),(-.22,.025,.012,.19),(-.055,.105,.32,.012),(.215,.205,.012,.18),(.20,-.075,.17,.012),(-.085,.22,.012,.15),(.04,-.025,.25,.012)]
for i,(x,y,w,d)in enumerate(walls):box('WholeMazeObstacle_'+str(i+1),(x,y,.262),(w,d,.052),0)
lathe_z('WholeStationaryDisplayBall',-.29,-.235,[(0,.237),(.010,.239),(.015,.249),(.013,.260),(.006,.265),(0,.266)],2,20)
for n in set(G)-inner:
 v,f,m=G[n];a=math.radians(8);G[n]=([(x,y*math.cos(a)-(z-.24)*math.sin(a),.24+y*math.sin(a)+(z-.24)*math.cos(a))for x,y,z in v],f,m)
# Two real side pins meet the inner tray and intermediate ring at the inner-axis height.
for tag,lo,hi in [('Left',-.413,-.325),('Right',.325,.420)]:axle(tag+'WholeInnerAxisPin',lo,hi,0,.24,.012,2,20)
axle('WholeRightInnerAxisControlKnob',.410,.435,0,.24,.035,2,24)
# Middle assembly fixed 5 degrees about the perpendicular Y axis. No old flat board reused.
for n in set(G)-start:
 v,f,m=G[n];a=math.radians(-5);G[n]=([(x*math.cos(a)+(z-.24)*math.sin(a),y,.24-x*math.sin(a)+(z-.24)*math.cos(a))for x,y,z in v],f,m)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('OuterBoxAndMazeWalls_WarmTimber',(.43,.225,.085,1),.80,0),('WholeGimbalAndMazeFloor_Ivory',(.69,.64,.49,1),.75,0),('FixedPivotsKnobsAndBall_DeepTeal',(.055,.17,.19,1),.55,.28)]
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
focus=Vector((0,0,.16))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.52;aim(cam,(3.6,-5,4.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/toys/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'toys','style':'S01-clean-geometric','title':'Fixed Two Axis Open Maze Table','description':'One newly authored complete static tabletop maze-game exterior. A deep grounded collection base and continuous outer support rim carry a whole open intermediate frame on front/rear pins. A separate complete maze tray is held on perpendicular side pins in one gently tilted pose; two distinct control knobs terminate the two axes. The tray has a single shared-vertex thick floor with three genuine through-drop apertures, four perimeter rails, fixed raised maze walls and one stationary display ball. All whole geometry is new, not the fixed inclined pinball cabinet with its targets replaced, a quarter-turn modular grooved track, or an abacus given a horizontal board. Three constant opaque untextured PBR roles, metres, native Z up, full horizontally bounds-centred ground origin. One whole prop, zero scenes. Fixed illustrative pose only: no solved ball route, game rules, playable scoring, physics, axis motion through all angles, dynamic collision guarantees, controls or transfer mechanism, user fit, manufacture or toy-safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
