import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='architecture-fixed-open-core-helical-ramp-and-peripheral-bents-01'
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
PALETTE=[('WholeContinuousRampWarmConcrete',(.59,.55,.44,1),.92,0),('WholePeripheralSupportsDeepBlue',(.18,.29,.31,1),.78,.12),('WholeOpenRailsPaleMetal',(.65,.67,.63,1),.6,.3)]
FM={}
# Full-turn thin slab with tangential lower and upper landings in one closed mesh. No central mast or ground-filled mass.
RI=1.25;RO=2.40;Z0=.24;RISE=3.35;THICK=.18;STEPS=64
stations=[]
for y in[-1.05,-.52]:stations.append((0,y,Z0,1,0))
for k in range(STEPS+1):
 t=math.tau*k/STEPS;stations.append((0,0,Z0+RISE*k/STEPS,math.cos(t),math.sin(t)))
for y in[.52,1.05]:stations.append((0,y,Z0+RISE,1,0))
v=[];f=[];profile=[(RI,-THICK),(RO,-THICK),(RO,0),(RI,0)]
for cx,cy,z,ux,uy in stations:
 for r,h in profile:v.append((cx+r*ux,cy+r*uy,z+h))
for k in range(len(stations)-1):
 for j in range(4):
  a=k*4+j;b=k*4+(j+1)%4;c=(k+1)*4+(j+1)%4;d=(k+1)*4+j;f.extend([(a,b,c),(a,c,d)])
f.extend([(0,2,1),(0,3,2)]);o=(len(stations)-1)*4;f.extend([(o,o+1,o+2),(o,o+2,o+3)])
record('WholeThinFullTurnRampAndTwoTangentialTerminals',v,f,0)
# Rails follow the same continuous profile, with an explicit radial frame rather than twist-prone tube frames.
for side,r in [('Inner',RI+.035),('Outer',RO-.035)]:
 v=[];f=[]
 for cx,cy,z,ux,uy in stations:
  for dr,h in[(-.025,.87),(.025,.87),(.025,.92),(-.025,.92)]:v.append((cx+(r+dr)*ux,cy+(r+dr)*uy,z+h))
 for k in range(len(stations)-1):
  for j in range(4):
   a=k*4+j;b=k*4+(j+1)%4;c=(k+1)*4+(j+1)%4;d=(k+1)*4+j;f.extend([(a,b,c),(a,c,d)])
 f.extend([(0,2,1),(0,3,2)]);o=(len(stations)-1)*4;f.extend([(o,o+1,o+2),(o,o+2,o+3)])
 record(side+'WholeContinuousOpenTopRail',v,f,2)
 for j,k in enumerate([0,2,10,18,26,34,42,50,58,66,68]):
  cx,cy,z,ux,uy=stations[k];x=cx+r*ux;y=cy+r*uy
  box(side+'WholeRailPost'+str(j),(x-.019,y-.019,z-.015),(x+.019,y+.019,z+.89),2)
# Independent outer bents support the rising slab from below without closing its central well.
for j,t in enumerate([math.pi*.25,math.pi*.75,math.pi*1.25,math.pi*1.75]):
 z=Z0+RISE*t/math.tau;ux=math.cos(t);uy=math.sin(t);x=2.55*ux;y=2.55*uy
 box('WholePeripheralColumnFoot'+str(j),(x-.19,y-.19,0),(x+.19,y+.19,.09),1)
 box('WholePeripheralColumn'+str(j),(x-.085,y-.085,.065),(x+.085,y+.085,z-.12),1)
 # Radial cantilever header crosses under outer slab band, stopping short of the open eye.
 name='WholeRadialUnderslabHeader'+str(j);box(name,(1.40,-.075,z-.27),(2.63,.075,z-.14),1)
 v,f,m=G.pop(name);record(name,[(x*ux-y*uy,x*uy+y*ux,z)for x,y,z in v],f,m)
for label,y,z in [('Lower',-.83,Z0),('Upper',.83,Z0+RISE)]:
 for r in[1.38,2.27]:
  box(label+'WholeTerminalFoot'+str(r),(r-.14,y-.14,0),(r+.14,y+.14,.075),1)
  box(label+'WholeTerminalColumn'+str(r),(r-.06,y-.06,.055),(r+.06,y+.06,z-.12),1)
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
focus=Vector((0,0,2.10))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=7.7;aim(cam,(7,-9,7.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/architecture/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'modular','theme':'architecture','style':'S01-clean-geometric','title':'Fixed Open Core Helical Ramp and Peripheral Bents','description':'One complete newly authored static architectural full-turn helical ramp module. One continuously sloping thin annular slab includes its full lower and upper tangential terminal platforms, separated vertically at the same azimuth. The whole central eye remains open and the rising underside is exposed between independent peripheral columns and radial underside headers; there is no central mast, ground-filled wedge mass, separate climbing ladder or U-section slide trough. Two continuous open top rails and individual posts follow the complete ramp and its level ends. The new whole peripheral support and two-level circulation organization is not an old winding stone stair with its treads removed, nor an enlarged mast-supported playground slide. No old visible geometry imported. Three opaque PBR roles, metres Z up, whole horizontal envelope centred over finite ground feet. One architectural module zero scenes. Fixed game-art appearance only. No host floors or building, actual walkability, accessible slope, headroom certification, ramp or rail performance, structural calculation, load rating, building-code or safety capability. Rig animation and interaction not made or verified.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
