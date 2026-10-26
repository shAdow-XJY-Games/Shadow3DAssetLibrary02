import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='timekeeping-static-open-bird-hatch-and-hanging-weight-clock-01'
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

def cell_union(name,cells,mat):
 faces={}
 for v in cells:
  v=[tuple(round(c,12)for c in p)for p in v]
  for f in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:
   q=tuple(v[i]for i in f);key=tuple(sorted(q))
   if key in faces:del faces[key]
   else:faces[key]=q
 v=[];ix={};f=[]
 for q in faces.values():
  ids=[]
  for p in q:
   if p not in ix:ix[p]=len(v);v.append(p)
   ids.append(ix[p])
  f.extend([(ids[0],ids[1],ids[2]),(ids[0],ids[2],ids[3])])
 record(name,v,f,mat)
def turned(name,x,y,profile,m,seg=16):
 v=[];rs=[];f=[]
 for r,z in profile:
  pts=[(x,y,z)]if r==0 else[(x+r*math.cos(math.tau*i/seg),y+r*math.sin(math.tau*i/seg),z)for i in range(seg)]
  rs.append(list(range(len(v),len(v)+len(pts))));v+=pts
 for a,b in zip(rs,rs[1:]+rs[:1]):
  if len(a)==len(b)==1:continue
  for i in range(seg):
   j=(i+1)%seg
   if len(a)==1:f.append((a[0],b[i],b[j]))
   elif len(b)==1:f.append((a[i],b[0],a[j]))
   else:f.extend([(a[i],b[i],b[j]),(a[i],b[j],a[j])])
 record(name,v,f,m)
PALETTE=[('WholeClockDarkTimber',(.27,.15,.075,1),.87,0),('WholeDialAndBirdIvory',(.78,.70,.48,1),.81,0),('WholePointersWeightsDarkBronze',(.12,.22,.20,1),.62,.30)]
FM={}
def shaped(name,rows,axis,mat,n=12,bands=None):
 v=[];f=[];mats=[]
 for x,y,z,rx,ry in rows:
  for j in range(n):
   a=math.tau*j/n
   v.append((x+rx*math.cos(a),y+ry*math.sin(a),z)if axis=='Z'else((x,y+rx*math.cos(a),z+ry*math.sin(a))if axis=='X'else(x+rx*math.cos(a),y,z+ry*math.sin(a))))
 for k in range(len(rows)-1):
  for j in range(n):
   a=k*n+j;b=k*n+(j+1)%n;c=b+n;d=a+n;f.extend([(a,b,c),(a,c,d)]);mats.extend([bands[k]if bands else mat]*2)
 for k in [0,len(rows)-1]:
  center=len(v);v.append(rows[k][:3])
  for j in range(n):f.append((center,k*n+(j+1)%n,k*n+j)if k==0 else(center,k*n+j,k*n+(j+1)%n));mats.append(bands[0 if k==0 else-1]if bands else mat)
 record(name,v,f,mat);FM[name]=mats

def cub(lo,hi):return[(x,y,z)for z in[lo[2],hi[2]]for y in[lo[1],hi[1]]for x in[lo[0],hi[0]]]
# Whole deep wall case with a real upper bird chamber, not a painted dark opening.
xs=[-.30,-.16,.16,.30];ys=[-.14,.08,.14];zs=[.60,1.13,1.18,1.40,1.44];cells=[]
for i in range(3):
 for j in range(2):
  for k in range(4):
   if i==1 and j==0 and k==2:continue
   cells.append(cub((xs[i],ys[j],zs[k]),(xs[i+1],ys[j+1],zs[k+1])))
cell_union('WholeDeepClockCaseAndBirdChamber',cells,0)
pad('WholeThickGabledClockRoof',[(-.37,1.42),(.37,1.42),(.37,1.48),(0,1.68),(-.37,1.48)],-.20,.20,0)
# Complete fixed-open hatch rotates only in the authored static pose.
box('WholeHatchBeforeRotation',(0,-.012,1.185),(.315,.012,1.395),0)
v,f,m=G.pop('WholeHatchBeforeRotation');t=-math.radians(100);record('WholeFixedOpenBirdHatch',[(-.16+x*math.cos(t)-y*math.sin(t),-.15+x*math.sin(t)+y*math.cos(t),z)for x,y,z in v],f,m)
pipe('WholeHatchFixedHinge',[(-.16,-.15,1.175),(-.16,-.15,1.41)],.015,2,12)
pipe('WholeShortBirdPerch',[(0,.10,1.22),(0,-.25,1.22)],.018,0,10)
shaped('WholeSmallFixedBirdBodyAndHead',[(0,.04,1.265,.022,.023),(0,-.035,1.28,.062,.046),(0,-.12,1.30,.052,.055),(0,-.18,1.335,.040,.042),(0,-.225,1.34,.028,.028)],'Y',1,12)
shaped('WholeSmallBluntBirdBeak',[(0,-.214,1.34,.022,.013),(0,-.28,1.335,.004,.004)],'Y',2,8)
for sg in[-1,1]:shaped('WholeBirdEye'+str(sg),[(sg*.032,-.192,1.351,.008,.008),(sg*.032,-.207,1.351,.004,.004)],'Y',2,8)
def axialY(name,x,z,prof,m,n=32):
 turned(name,0,0,prof,m,n);v,f,ma=G.pop(name);record(name,[(x+a,c,z+b)for a,b,c in v],[(a,c,b)for a,b,c in f],ma)
axialY('WholeRaisedRoundDialBezel',0,.90,[(.196,-.185),(.23,-.185),(.23,-.125),(.196,-.125)],2)
axialY('WholeIvoryDial',0,.90,[(0,-.162),(.202,-.162),(.202,-.135),(0,-.135)],1)
for k in range(12):
 t=math.tau*k/12;x=.171*math.sin(t);z=.90+.171*math.cos(t)
 box('WholeDialIndex'+str(k),(x-.006,-.171,z-.014),(x+.006,-.159,z+.014),2)
pipe('WholePointerSpindle',[(0,-.208,.90),(0,-.151,.90)],.017,2,12)
pad('WholeFixedMinutePointer',[(-.009,.89),(.009,.89),(.006,1.032),(0,1.047),(-.006,1.032)],-.193,-.181,2)
pad('WholeFixedHourPointer',[(-.012,.895),(.010,.887),(.103,.942),(.105,.954),(.09,.952)],-.210,-.198,2)
pipe('WholeFixedPendulumRod',[(0,0,.125),(0,0,.69)],.008,2,10)
axialY('WholeFixedPendulumBob',0,.15,[(0,-.027),(.065,-.027),(.065,.018),(0,.018)],2,24)
for sg in[-1,1]:
 x=sg*.195
 pipe('WholeFixedWeightCord'+str(sg),[(x,.015,.20),(x,.015,.66)],.006,2,8)
 turned('WholeShapedHangingWeight'+str(sg),x,.015,[(0,0),(.009,0),(.037,.035),(.052,.075),(.054,.15),(.036,.205),(.018,.226),(0,.226)],2,16)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
for n,(v,f,m)in G.items():FM.setdefault(n,[m]*len(f))
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
focus=Vector((0,0,.84))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.12;aim(cam,(1.5,-7,2.1));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/timekeeping/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'timekeeping','style':'S01-clean-geometric','title':'Static Open Bird Hatch and Hanging Weight Clock','description':'One wholly newly authored complete fixed bird-window wall-clock exterior. A full deep timber case has a true upper blind bird chamber and one thick hatch held open on its fixed hinge; one whole small stylized bird rests on a continuous short perch projecting from the chamber back. Below are a complete raised circular bezel, recessed ivory dial, twelve plain markers and two separately layered fixed hands. One full pendulum rod and bob plus two continuous suspension-appearance cords and two whole shaped weights hang below the case. A full thick gabled cap closes the top. Unlike the old open-frame table clock or four-faced through-arch tower, this whole shallow wall case organises an actual opening bird compartment above the dial and separate hanging pendulum/weight elements below it; no old clock, roof or bird mesh imported. Three opaque constant PBR roles, metres Z-up, full horizontal bounds-centred origin at the lowest weight bottoms. One static uninstalled wall prop zero scenes. No host wall or load-bearing mount is supplied; the hanging display pose is fixed geometry, not a demonstrated supported installation. No working internal escapement, bird linkage, bellows, chime, timekeeping, calibration, pendulum motion, cord winding, moving hatch, manufacture or safety capability. Small bird is a simplified ornament, not biological anatomy. Rigging animation interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
