import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='education-fixed-open-case-c-tube-and-pointer-link-display-01'
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
PALETTE=[('WholeInstrumentDarkCase',(.10,.16,.16,1),.70,.30),('WholeInstrumentMutedBrassTubeAndLink',(.48,.31,.12,1),.62,.60),('WholeInstrumentBlankPlateAndPointer',(.62,.63,.53,1),.80,.10)]
# Whole shallow cup is open towards -Y. There is no transparent glass or printed dial.
turned('WholeOpenRoundInstrumentCase',0,0,[(0,.085),(.46,.085),(.46,-.07),(.425,-.07),(.425,.055),(0,.055)],0,48)
v,f,m=G['WholeOpenRoundInstrumentCase'];G['WholeOpenRoundInstrumentCase']=([(x,z,.65+y)for x,y,z in v],[(a,c,b)for a,b,c in f],m)
box('WholeGroundFoot',(-.32,-.20,0),(.32,.20,.075),0)
box('WholeLowerCaseSupport',(-.12,-.025,.06),(.12,.085,.25),0)
box('WholeFixedTubeRootBlock',(.10,-.067,.25),(.20,.06,.40),1)
# One complete flattened C-curved closed metal-like exterior; internal fluid bore not modelled.
v=[];n=12;steps=44
for k in range(steps+1):
 a=math.radians(-65+295*k/steps);x=.335*math.cos(a);z=.65+.335*math.sin(a)
 for j in range(n):
  b=math.tau*j/n;v.append((x+.023*math.cos(a)*math.cos(b),-.015+.047*math.sin(b),z+.023*math.sin(a)*math.cos(b)))
f=[]
for k in range(steps):
 for j in range(n):a=k*n+j;b=k*n+(j+1)%n;f.extend([(a,b,b+n),(a,b+n,a+n)])
for k in [0,steps]:
 a=math.radians(-65+295*k/steps);c=len(v);v.append((.335*math.cos(a),-.015,.65+.335*math.sin(a)))
 for j in range(n):f.append((c,k*n+(j+1)%n,k*n+j)if k==0 else(c,k*n+j,k*n+(j+1)%n))
record('WholeFlattenedCCurvedTubeExterior',v,f,1)
# Full short pinned link from free tube tip to sector tail; fixed art, not a motion solution.
pipe('WholeTubeTipLink',[(-.215,-.075,.393),(-.11,-.075,.50)],.012,1,8)
for j,(x,z)in enumerate([(-.215,.393),(-.11,.50)]):pipe('WholeTipLinkPin'+str(j),[(x,-.095,z),(x,.005,z)],.018,2,12)
box('WholeSectorRearBearingMount',(-.155,.01,.43),(-.065,.065,.53),0)
pipe('WholeSectorFixedAxle',[(-.11,-.065,.49),(-.11,.045,.49)],.022,1,16)
# Whole tooth-edged sector silhouette and its integral inward tail, no tooth meshing promised.
cx,cz=-.11,.49;p=[(cx,cz)]
for j in range(25):
 a=math.radians(0+95*j/24);r=.155 if j%3==1 else .139;p.append((cx+r*math.cos(a),cz+r*math.sin(a)))
pad('WholeFixedToothedSector',p,-.065,-.025,1)
# Small independently supported pinion appearance and complete long blank pointer.
box('WholePointerRearBearingMount',(-.035,.012,.645),(.035,.065,.715),0)
pipe('WholePointerFixedAxle',[(0,-.14,.68),(0,.045,.68)],.018,1,16)
p=[]
for j in range(48):
 a=math.tau*j/48;r=.044 if j%4 in[1,2]else .036;p.append((r*math.cos(a),.68+r*math.sin(a)))
pad('WholeSmallToothEdgedPinion',p,-.074,-.035,1)
p=[(-.023,.655),(.022,.659),(.018,.715),(-.142,.948),(-.156,.946),(-.126,.886),(-.017,.704)]
pad('WholeFixedBlankPointer',p,-.125,-.108,2)
pipe('WholeProudPointerHub',[(0,-.147,.68),(0,-.115,.68)],.033,0,20)
# A short blank arc reference strip stays separate from the tube and contains no calibration marks.
p=[(.384*math.cos(math.radians(a)),.65+.384*math.sin(math.radians(a)))for a in range(30,151,5)]+[(.358*math.cos(math.radians(a)),.65+.358*math.sin(math.radians(a)))for a in range(150,29,-5)]
pad('WholeBlankArcReferenceStrip',p,-.079,-.064,2)
for j,a in enumerate([30,150]):
 x=.373*math.cos(math.radians(a));z=.65+.373*math.sin(math.radians(a));pipe('WholeBlankArcRearSeat'+str(j),[(x,-.07,z),(x,.065,z)],.013,0,12)
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
focus=Vector((0,0,.56))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.50;aim(cam,(1.5,-7,2.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/education/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'education','style':'S01-clean-geometric','title':'Fixed Open Case C Tube and Pointer Link Display','description':'One newly authored complete static open-case C-tube instrument-style exhibit. A continuous shallow round backed cup on a complete foot and lower support exposes one whole flattened C-curved metal-like tube exterior. Its lower end is fixed in a full block, while its other end joins a complete short pinned link to a separate tooth-edged sector. An independently supported small tooth-edged pinion, fixed shaft and whole long blank pointer sit before the open mechanism; a narrow blank reference arc has two real rear seats. Unlike a closed cuff-gauge face or a capsule-stack pen drum, the visible curved tube-tip/link/sector/pointer relationship defines this complete newly authored object. No old gauge or mechanism vertices imported. Three opaque PBR roles, metres Z up, one model zero scenes. The tube is a closed exterior solid, not a modelled fluid bore; no transparent cover or calibrated marks. Static illustrative appearance only, not a functional pressure instrument. No pressure containment, fluid path, deformation, gearing accuracy, motion solution, readings, calibration, manufacture, operation or safety performance. Rigging animation interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
