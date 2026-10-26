import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='regional-fixed-horizontal-runner-and-stone-millroom-cutaway-01'
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
PALETTE=[('WholeDryRaceWallsAndGrindingStones',(.47,.46,.39,1),.96,0),('WholeRunnerAxleAndMillTimber',(.29,.18,.085,1),.88,0),('WholeRearRoomWallsAndRoof',(.62,.43,.27,1),.92,0)]
FM={}
box('WholeDryRaceBed',(-2.25,-1.90,0),(2.25,1.90,.18),0)
for x,label in[(-1.91,'Left'),(1.91,'Right')]:box('Whole'+label+'UndercroftBearingWall',(x-.27,-1.65,.15),(x+.27,1.65,1.84),0)
# Whole transverse joists remain exposed where the front room floor is deliberately omitted.
for y,label in[(-.48,'Front'),(.48,'Rear')]:box('Whole'+label+'MillstoneBearingJoist',(-1.99,y-.13,1.65),(1.99,y+.13,1.90),1)
box('WholeRetainedRearRoomFloor',(-1.98,.72,1.80),(1.98,1.65,1.99),1)
# Rear full thick wall with a genuine square window, and short side returns, make a cutaway room.
xs=[-2.,-.43,.43,2.];zs=[1.91,2.63,3.26,3.76];cells=[]
for i in range(3):
 for j in range(3):
  if i==1 and j==1:continue
  cells.append([(x,y,z)for z in[zs[j],zs[j+1]]for y in[1.48,1.68]for x in[xs[i],xs[i+1]]])
cell_union('WholeRearWindowedMillroomWall',cells,2)
for x,label in[(-1.86,'Left'),(1.86,'Right')]:box('Whole'+label+'RetainedUpperSideWall',(x-.10,.78,1.91),(x+.10,1.60,3.76),2)
pad('WholeRearThickPitchedRoofSection',[(-2.20,3.70),(-2.20,3.87),(0,4.62),(2.20,3.87),(2.20,3.70),(0,4.44)],.66,1.84,2)
# One fixed horizontal runner below the millroom, directly joined by vertical shaft to upper stone pair.
turned('WholeLowerAxleBearingFoot',0,0,[(0,.17),(.22,.17),(.22,.43),(0,.43)],0,16)
pipe('WholeVerticalRunnerToStoneAxle',[(0,0,.36),(0,0,2.51)],.085,1,12)
turned('WholeHorizontalRunnerHub',0,0,[(0,.63),(.23,.63),(.23,.94),(0,.94)],1,16)
for i in range(10):
 a=math.tau*i/10;u=(math.cos(a),math.sin(a),0);w=(-u[1],u[0],0)
 # Whole broad shallow angled vane, no separate rim or imported vertical wheel.
 vv=[add(add(mul(u,r),mul(w,t)),(0,0,z))for z in[.65,.89]for t in[-.055,.055]for r in[.17,1.03]];ff=[]
 for a0,b0,c0,d0 in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:ff.extend([(a0,b0,c0),(a0,c0,d0)])
 record('WholeHorizontalRunnerPaddle'+str(i),vv,ff,1)
turned('WholeLowerStoneWithRealShaftPassage',0,0,[(.10,1.88),(.72,1.88),(.76,1.95),(.76,2.12),(.10,2.12)],0,32)
turned('WholeUpperStoneAndCentralFeedEye',0,0,[(.12,2.115),(.72,2.115),(.73,2.20),(.65,2.39),(.25,2.45),(.14,2.45),(.12,2.36)],0,32)
# Full open hopper wall with true bottom neck, independently held by two uprights and top ties.
turned('WholeOpenGrainHopperAndNarrowThroat',0,0,[(.13,2.50),(.13,2.70),(.60,3.24),(.60,3.39),(.53,3.39),(.53,3.27),(.075,2.73),(.075,2.50)],1,4)
for x,label in[(-.89,'Left'),(.89,'Right')]:box('Whole'+label+'HopperPost',(x-.065,.39,1.84),(x+.065,.52,3.43),1)
box('WholeHopperRearTie',(-.95,.41,3.22),(.95,.53,3.36),1)
for x,label in[(-.43,'Left'),(.43,'Right')]:box('Whole'+label+'HopperSeatArm',(x-.055,-.05,3.22),(x+.055,.49,3.34),1)
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
focus=Vector((0,0,2.2))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=7.5;aim(cam,(6,-12,6.4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/regional/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'regional','style':'S01-clean-geometric','title':'Fixed Horizontal Runner and Stone Millroom Cutaway','description':'One newly authored complete static regional millroom cutaway. A real open-ended dry race lies between two full supporting masonry walls beneath the room. A whole horizontal radial paddle runner sits on a low bearing foot and shares one continuous vertical shaft with the complete broad upper and lower millstones above. The lower stone has a genuine shaft passage and sits on two whole exposed transverse floor joists; the upper stone has a real central feed eye. A full open tapering hopper and narrow throat stand on independent complete rear posts, tie and side seats. The retained room has a true rear window, two short side returns, a rear floor patch and a thick pitched rear roof section; the front walls, floor boards and front roof are deliberately omitted to reveal the continuous lower-runner to upper-stone relationship. Finite section faces are closed, not unfinished surface holes. This is neither the old vertically oriented twin-rim waterwheel on an external A-frame nor a standalone hand quern relocated indoors, and no old wheel, building or stone mesh is imported. Three opaque PBR roles, metres Z up, whole horizontal envelope centred, one architectural cutaway zero scenes. Dry unoccupied regional-inspired artwork, not an exact historic reconstruction or operational plan. No water, grain, grinding process, shaft rotation, bearing fit, transmission, hydraulics, energy output, food hygiene, access, loading, structure or engineering safety capability. Rigging animation and interaction not made or verified.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
