import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='farming-static-twin-wheel-chain-bucket-lift-01'
import math
N=24
G={}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def record(name,v,f,m):
 if sum(dot(v[a],cross(v[b],v[c]))for a,b,c in f)<0:f=[(a,c,b)for a,b,c in f]
 G[name]=(v,f,m)
def box(name,lo,hi,m):
 v=[(x,y,z)for z in[lo[2],hi[2]]for y in[lo[1],hi[1]]for x in[lo[0],hi[0]]];f=[]
 for a,b,c,d in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:f.extend([(a,b,c),(a,c,d)])
 record(name,v,f,m)
def pipe(name,points,r,m,segments=8):
 v=[]
 for k,p in enumerate(points):
  tangent=unit(sub(points[min(k+1,len(points)-1)],points[max(k-1,0)]));u=(1,0,0)if abs(tangent[0])<.9 else(0,1,0);u=unit(cross(tangent,u));w=cross(tangent,u)
  for i in range(segments):v.append(add(p,add(mul(u,r*math.cos(math.tau*i/segments)),mul(w,r*math.sin(math.tau*i/segments)))))
 f=[]
 for k in range(len(points)-1):
  for i in range(segments):
   j=(i+1)%segments;a=k*segments+i;b=k*segments+j;c=(k+1)*segments+j;d=(k+1)*segments+i;f.extend([(a,b,c),(a,c,d)])
 for k in [0,len(points)-1]:
  c=len(v);v.append(points[k]);base=k*segments
  for i in range(segments):f.append((c,base+(i+1)%segments,base+i)if k==0 else(c,base+i,base+(i+1)%segments))
 record(name,v,f,m)
def wheel(name,x,y,z,ro,ri,width,m):
 # Complete closed annular tire (or capped disc when ri=0), axis X.
 profile=[(ri,x-width/2),(ro,x-width/2),(ro,x+width/2),(ri,x+width/2)]
 v=[];rs=[]
 for r,xx in profile:
  ring=[(xx,y,z)]if r==0 else[(xx,y+r*math.sin(math.tau*i/N),z+r*math.cos(math.tau*i/N))for i in range(N)];rs.append(list(range(len(v),len(v)+len(ring))));v+=ring
 f=[]
 for a,b in zip(rs,rs[1:]+rs[:1]):
  if len(a)==len(b)==1:continue
  for i in range(N):
   j=(i+1)%N
   if len(a)==1:f.append((a[0],b[i],b[j]))
   elif len(b)==1:f.append((a[i],b[0],a[j]))
   else:f.extend([(a[i],b[i],b[j]),(a[i],b[j],a[j])])
 record(name,v,f,m)

def earclip(p):
 cr=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 ids=list(range(len(p)));out=[]
 while len(ids)>3:
  for j,b in enumerate(ids):
   a,c=ids[j-1],ids[(j+1)%len(ids)]
   if cr(p[a],p[b],p[c])<=1e-14:continue
   if any(all(cr(p[u],p[v],p[k])>=-1e-14 for u,v in [(a,b),(b,c),(c,a)])for k in ids if k not in [a,b,c]):continue
   out.append((a,b,c));ids.pop(j);break
  else:raise ValueError('Non-simple padding section')
 out.append(tuple(ids));return out
def pad(name,p,y0,y1,m):
 if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);v=[(x,y,z)for y in[y0,y1]for x,z in p];f=[]
 for a,b,c in earclip(p):f.extend([(a,b,c),(c+n,b+n,a+n)])
 for i in range(n):
  j=(i+1)%n;f.extend([(i,j+n,j),(i,i+n,j+n)])
 record(name,v,f,m)

# New whole dry fixed chain-bucket lifting frame; no working mechanism claim.
PALETTE=[('FrameWarmTimber',(.32,.18,.075,1),.8,0),('WheelAndChainIron',(.075,.095,.10,1),.54,.6),('BucketsAndTroughMutedTeal',(.13,.30,.27,1),.68,.25)]
LOW=.60;HIGH=2.20;RAD=.32
for x,label in[(-.55,'Left'),(.55,'Right')]:
 box(label+'WholeGroundSkid',(x-.075,-.80,0),(x+.075,1.47,.12),0)
 for y,side in[(-.63,'Front'),(.63,'Rear')]:pipe(label+side+'WholeSlopingFrameLeg',[(x,y,.10),(x,0,2.20)],.065,0,4)
 box(label+'UpperBearingBridge',(x-.09,-.17,2.10),(x+.09,.17,2.26),0)
 box(label+'LowerBearingPost',(x-.07,-.07,.10),(x+.07,.07,.68),0)
for y,label in[(-.66,'Front'),(.65,'Rear')]:box(label+'LowCrossTie',(-.58,y-.045,.09),(.58,y+.045,.18),0)
for z,label in[(LOW,'Lower'),(HIGH,'Upper')]:
 pipe(label+'WholeAxle',[(-.67,0,z),(.67,0,z)],.045,1,16)
 wheel(label+'WholeOpenRim',0,0,z,.302,.235,.38,1)
 pipe(label+'WholeHub',[(-.19,0,z),(.19,0,z)],.085,1,16)
 for k in range(4):
  a=math.tau*k/4;pipe(label+'Spoke'+str(k),[(0,.06*math.cos(a),z+.06*math.sin(a)),(0,.26*math.cos(a),z+.26*math.sin(a))],.035,1,4)
def capsule(r):
 return [(r*math.cos(a),HIGH+r*math.sin(a))for a in[math.pi*i/16 for i in range(17)]]+[(r*math.cos(a),LOW+r*math.sin(a))for a in[math.pi+math.pi*i/16 for i in range(17)]]
for x,label in[(-.21,'Left'),(.21,'Right')]:
 outer=capsule(.337);inner=capsule(.307);n=len(outer);v=[(xx,y,z)for xx in[x-.018,x+.018]for ring in[outer,inner]for y,z in ring];f=[]
 for i in range(n):
  j=(i+1)%n
  for a,b,c,d in[(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)]:f.extend([(a,b,c),(a,c,d)])
 record(label+'WholeContinuousStylizedChainLoop',v,f,1)
def cup(name,cy,cz,ny,nz):
 # Full thick open scoop: outer bottom/top, inner lip/floor. Its mouth follows local tangent.
 ty,tz=nz,-ny
 rings=[(-.08,.23,0,.18),(.08,.23,0,.18),(.08,.205,.022,.158),(-.056,.205,.022,.158)];v=[]
 for t,w,u0,u1 in rings:
  for x,u in[(-w,u0),(w,u0),(w,u1),(-w,u1)]:v.append((x,cy+ny*u+ty*t,cz+nz*u+tz*t))
 f=[]
 for k in range(3):
  for i in range(4):
   j=(i+1)%4;a=k*4+i;b=k*4+j;c=(k+1)*4+j;d=(k+1)*4+i;f.extend([(a,b,c),(a,c,d)])
 f.extend([(0,2,1),(0,3,2),(12,13,14),(12,14,15)]);record(name,v,f,2)
for k,z in enumerate([.80,1.20,1.60,2.00]):
 cup('AscendingWholeOpenBucket'+str(k),-.32,z,-1,0);cup('DescendingWholeInvertedBucket'+str(k),.32,z,1,0)
cup('UpperTurningWholeBucket',0,HIGH+.32,0,1);cup('LowerTurningWholeBucket',0,LOW-.32,0,-1)
# Full separate fixed outlet gutter, open at both ends, outside chain route.
profile=[(-.28,0),(.28,0),(.28,.20),(.235,.20),(.235,.035),(-.235,.035),(-.235,.20),(-.28,.20)]
pad('WholeSlopingOpenOutletGutter',profile,.56,1.40,2);v,f,m=G['WholeSlopingOpenOutletGutter'];G['WholeSlopingOpenOutletGutter']=([(x,y,z+2.14-.20*(y-.56))for x,y,z in v],f,m)
for x,label in[(-.55,'Left'),(.55,'Right')]:box(label+'OutletSupportPost',(x-.045,1.135,.10),(x+.045,1.225,1.95),0)
box('WholeOutletSupportCrossbar',(-.60,1.135,1.95),(.60,1.225,2.016),0)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
FM={n:[m]*len(f)for n,(v,f,m)in G.items()}
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
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
triangles=sum(len(f)for v,f,m in G.values())
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
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
focus=Vector((0,0,1.33))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.65;aim(cam,(4,-6,3.6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/farming/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'farming','style':'S01-clean-geometric','title':'Static Twin Wheel Chain Bucket Lift','description':'One new whole static dry chain-bucket irrigation-lift appearance: two vertically separated open-rim wheels on full axles and a grounded braced timber frame carry two continuous closed capsule-shaped chain-route bands and a fixed row of ten whole thick open buckets. The ascending buckets face upward, return-side buckets downward and the two turning buckets sideways. A separate elevated sloping U-section outlet gutter on its full support stands beside the upper route. This is not the previous single paddle waterwheel, single-rope well, piston/treadle pump or an extra row of buckets on an old model. All visible geometry new, three opaque PBR roles, metres and whole XY-centred ground origin. Stylized continuous bands indicate chain routing; individual articulated chain links, sprocket engagement, empty-cycle trajectories, liquid pickup/discharge, drive input, motion, pressure/lift/flow efficiency, bearings, load/stability/manufacture and safety are not modeled or certified. Dry visual game prop, not operating instructions.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
