import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='architecture-fixed-interleaved-opposed-return-stair-bay-01'
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
PALETTE=[('WholeRouteAOchreStone',(.53,.38,.21,1),.88,0),('WholeRouteBMutedBlueStone',(.24,.37,.39,1),.88,0),('WholeCommonFrameAndRails',(.40,.43,.40,1),.78,.12)]
FM={}
# Four independently closed thin stepped flights. The two routes do not share a mid-level landing.
def flight(name,x0,x1,z0,direction,mat):
 y0=-1.62;dy=.27;dz=.25;top=[(y0,z0)]
 for j in range(12):top.extend([(y0+j*dy,z0+(j+1)*dz),(y0+(j+1)*dy,z0+(j+1)*dz)])
 p=[(y0,z0-.18),(1.62,z0+3-.18)]+list(reversed(top))
 pad(name,p,x0,x1,mat);v,f,m=G.pop(name)
 # (localYdepth, profileX, Z) changes handedness; negative direction adds a second reversal.
 v=[(depth,direction*yy,z)for yy,depth,z in v];f=[(a,c,b)for a,b,c in f]if direction>0 else f;record(name,v,f,m)
 for k,x in enumerate([x0+.07,x1-.07]):
  for j in[0,4,8,11]:
   y=direction*(y0+(j+.5)*dy);z=z0+(j+1)*dz
   pipe(name+'WholeRailPost'+str(k)+str(j),[(x,y,z-.025),(x,y,z+.73)],.026,2,8)
  pipe(name+'WholeContinuousSlopeRail'+str(k),[(x,direction*(y0+.5*dy),z0+.25+.71),(x,direction*(y0+11.5*dy),z0+3+.71)],.025,2,8)
flight('RouteAWholeLowerRearRisingFlight',-1.24,-.16,.20,1,0)
flight('RouteAWholeUpperFrontReturningFlight',.16,1.24,3.20,-1,0)
flight('RouteBWholeLowerFrontRisingFlight',.16,1.24,.20,-1,1)
flight('RouteBWholeUpperRearReturningFlight',-1.24,-.16,3.20,1,1)
# The two reverse-direction intermediate landings sit at opposite ends, not a common branching platform.
for label,y0,y1,mat in[('RouteARear',1.62,2.52,0),('RouteBFront',-2.52,-1.62,1)]:
 box(label+'WholeIndependentIntermediateLanding',(-1.24,y0,3.02),(1.24,y1,3.20),mat)
 yy=(y1-.065)if y0>0 else(y0+.065)
 for j,x in enumerate([-1.16,0,1.16]):pipe(label+'WholeLandingRailPost'+str(j),[(x,yy,3.175),(x,yy,3.95)],.026,2,8)
 pipe(label+'WholeLandingOuterRail',[(-1.18,yy,3.93),(1.18,yy,3.93)],.025,2,8)
for label,y0,y1,mat in[('RouteATopFront',-2.52,-1.62,0),('RouteBTopRear',1.62,2.52,1)]:
 box(label+'WholeUpperExitLanding',(-1.24,y0,6.02),(1.24,y1,6.20),mat)
 yy=(y1-.065)if y0>0 else(y0+.065)
 for j,x in enumerate([-1.16,0,1.16]):pipe(label+'WholeTopRailPost'+str(j),[(x,yy,6.175),(x,yy,6.95)],.026,2,8)
 pipe(label+'WholeTopOuterRail',[(-1.18,yy,6.93),(1.18,yy,6.93)],.025,2,8)
for sg in[-1,1]:
 lo,hi=(1.62,2.52)if sg>0 else(-2.52,-1.62)
 box('WholeGroundedEntryBand'+str(sg),(-1.28,lo-.04,0),(1.28,hi+.04,.20),2)
 for x in[-1.13,1.13]:box('WholeCommonCornerColumn'+str(sg)+str(x),(x-.07,sg*2.31-.07,.10),(x+.07,sg*2.31+.07,6.12),2)
# Distinct same-lane upper flights have 3m separation, not intersecting copies of a grounded stone mass.
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
focus=Vector((0,0,3.45))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=8.8;aim(cam,(10,-9,8.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/architecture/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'modular','theme':'architecture','style':'S01-clean-geometric','title':'Fixed Interleaved Opposed Return Stair Bay','description':'One complete newly authored static interleaved-return stair bay. Four whole thin stepped flights occupy two side lanes at two vertical levels within the same four-column frame. An ochre route starts at the front-left, rises rearward to its own rear intermediate landing, then returns forward on the upper right. A blue route starts at the rear-right, rises forward to a separate front intermediate landing, then returns rearward on the upper left. The opposite-end mid-landings never form one common branching landing; same-lane upper and lower flights retain a real three-metre vertical offset and open air beneath their thin sloping undersides. Full upper terminal landings, ground entry bands and complete flight/outer landing rails belong to the same whole module. This is not two copies of the old grounded solid half-turn stair stacked, nor extra upper branches on a shared T landing. All step profiles, thin supports, fixed placements and coordinates newly authored; no old stair mesh imported. Three opaque PBR roles, metres Z-up and full horizontal-bounds-centred grounded entry bands. One architectural model zero scenes. Route colours are only visual guides, not wayfinding signage. No host floors or fire-separating enclosure, human occupancy, walkability, headroom certification, emergency-egress/fire design, building-code/accessibility compliance, load, installation, engineering or safety capability. Rigging, animation and interaction not made or verified.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
