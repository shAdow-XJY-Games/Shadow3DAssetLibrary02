import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='architecture-fixed-high-truss-and-low-suspended-transporter-bridge-01'
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
PALETTE=[('WholeBridgeWarmStone',(.43,.40,.32,1),.94,0),('WholeFixedFramePetrol',(.12,.26,.25,1),.70,.25),('WholeGondolaAndCarriageOchre',(.55,.31,.10,1),.76,.18)]
FM={}
def beam(name,a,b,width,depth,mat):
 w=unit(sub(b,a));u=unit(cross(w,(0,0,1)if abs(w[2])<.9 else(0,1,0)));v=cross(w,u);verts=[]
 for q in[a,b]:verts.extend([add(q,add(mul(u,s*width/2),mul(v,t*depth/2)))for s,t in[(-1,-1),(1,-1),(1,1),(-1,1)]])
 fs=[]
 for aa,bb,cc,dd in[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:fs.extend([(aa,bb,cc),(aa,cc,dd)])
 record(name,verts,fs,mat)
# Two complete high open portal towers at the two finite shore piers; fixed overhead span, no raised crossing deck.
for side,x in[('Left',-3.4),('Right',3.4)]:
 box(side+'WholeGroundedPier',(x-.55,-1.50,0),(x+.55,1.50,.38),0)
 poly=[(-1.28,.34),(1.28,.34),(1.28,4.65),(-1.28,4.65),(-1.28,.34),(-1.02,.34),(-1.02,4.32),(1.02,4.32),(1.02,.34)]
 # Simple U portal section with two full legs and one full top, without coincident duplicate polygon point.
 poly=[(-1.28,.34),(-1.02,.34),(-1.02,4.32),(1.02,4.32),(1.02,.34),(1.28,.34),(1.28,4.65),(-1.28,4.65)]
 name=side+'WholeHighPortalTower';pad(name,poly,x-.16,x+.16,1)
 vv,ff,mm=G.pop(name);record(name,[(y,xx,z)for xx,y,z in vv],[(a,c,b)for a,b,c in ff],mm)
 # Independent splayed struts seat inside pier and portal lower side, not coplanar caps.
 for j,y in enumerate([-1.13,1.13]):
  beam(side+'WholeTowerKnee'+str(j),(x+(.34 if x<0 else-.34),y,.30),(x,y,1.65),.13,.13,1)
 box(side+'WholeApproachLanding',(x-.58,-.93,.30),(x+.58,.93,.57),0)
# The bridge carries only upper fixed tracks; no full lower connecting deck exists.
for side,y in[('Front',-.91),('Back',.91)]:
 for j,z in enumerate([4.46,5.18]):box(side+'WholeFixedLongChord'+str(j),(-4.0,y-.09,z-.09),(4.0,y+.09,z+.09),1)
 for j,x in enumerate([-3.85,-2.57,-1.28,0,1.28,2.57,3.85]):box(side+'WholeUpperTrussPost'+str(j),(x-.065,y-.075,4.40),(x+.065,y+.075,5.22),1)
 for j,(x0,x1)in enumerate(zip([-3.85,-2.57,-1.28,0,1.28,2.57],[-2.57,-1.28,0,1.28,2.57,3.85])):
  beam(side+'WholeUpperTrussDiagonal'+str(j),(x0,y,4.46 if j%2==0 else 5.18),(x1,y,5.18 if j%2==0 else 4.46),.075,.085,1)
for j,x in enumerate([-3.4,-1.7,0,1.7,3.4]):box('WholeFixedOverheadCrossTie'+str(j),(x-.075,-.99,5.10),(x+.075,.99,5.23),1)
# One offset complete overhead carriage has four whole wheels resting on the two fixed lower chords.
cx=-.65
for j,x in enumerate([cx-.65,cx+.65]):
 box('WholeCarriageCrossbar'+str(j),(x-.09,-1.13,4.72),(x+.09,1.13,4.88),2)
 pipe('WholeCarriageWheelAxle'+str(j),[(x,-1.12,4.70),(x,1.12,4.70)],.045,2,12)
 for k,y in enumerate([-.91,.91]):
  n='WholeCarriageWheel'+str(j)+str(k);wheel(n,y,x,4.70,.15,.035,.13,2);vv,ff,mm=G.pop(n);record(n,[(yy,xx,z)for xx,yy,z in vv],[(a,c,b)for a,b,c in ff],mm)
for j,y in enumerate([-.65,.65]):box('WholeCarriageLongTie'+str(j),(cx-.73,y-.055,4.73),(cx+.73,y+.055,4.86),2)
# A short low suspended gondola is not the full bridge span. Four long load-route rods connect its corners to the upper carriage.
box('WholeShortSuspendedGondolaDeck',(cx-.92,-.88,.53),(cx+.92,.88,.70),2)
for j,x in enumerate([cx-.82,cx+.82]):
 for k,y in enumerate([-.77,.77]):pipe('WholeLongSuspensionRod'+str(j)+str(k),[(x,y,.60),(cx+(-.65 if j==0 else .65),y,4.80)],.033,1,8)
for side,y in[('Front',-.80),('Back',.80)]:
 for j,x in enumerate([cx-.80,cx,cx+.80]):pipe(side+'WholeGondolaRailPost'+str(j),[(x,y,.65),(x,y,1.12)],.024,1,8)
 for j,z in enumerate([.88,1.10]):pipe(side+'WholeGondolaRail'+str(j),[(cx-.85,y,z),(cx+.85,y,z)],.02,1,8)
# Both deck ends stay open; no vehicle, passenger, river, invisible foundation or animated travel supplied.
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
focus=Vector((0,0,2.65))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=10.2;aim(cam,(8,-12,7.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/architecture/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'architecture','style':'S01-clean-geometric','title':'Fixed High Truss and Low Suspended Transporter Bridge','description':'One newly authored whole fixed transporter-bridge-style exterior. Two complete high open portal towers on grounded end piers carry a permanently high, long twin-sided open truss and upper cross ties. One offset four-wheel overhead carriage rests on the two long lower chords; four entire long suspension rods connect it to a much shorter low gondola deck with two full side rails and open ends. The open air beneath the high fixed crossing remains distinct from the short hanging platform. Unlike the old vertical-lift bridge, no full-width crossing deck rises between guide towers, no top rope wheels or counterweights are supplied. Unlike the small orthogonal robot gantry, there is no transverse sliding bridge, downward tool guide or finger tool; only one fixed long travel direction and a low suspended crossing platform. No old visible meshes imported. Three opaque PBR materials, metres Z-up and complete horizontal-bounds-centred pier datum. One complete model zero scenes. Static architectural transport illustration only; no people, vehicles, water, terrain, drive or internal brake. No motion, path clearance, traffic access, engineering, cable tension, load, manufacture, navigation or safety capability is asserted. Rigging, animation and interaction are not made or verified.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
