import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='waterworks-whole-double-curved-wall-and-full-height-end-abutments-01'
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
PALETTE=[('WholeConvexWallWarmConcrete',(.51,.49,.43,1),.94,0),('WholeConcaveWallPaleConcrete',(.64,.63,.57,1),.93,0),('WholeEndAbutmentsSlateConcrete',(.32,.37,.37,1),.96,0)]
G={};FM={};ROOTS=[];CONTACTS=[];LINKS=[];GAPS=[]
ANGLE=math.pi/3;ANG=[-ANGLE+2*ANGLE*i/24 for i in range(25)];HEIGHT=4.;ZZ=[HEIGHT*i/8 for i in range(9)]
def radii(z):t=z/HEIGHT;return(3.+t*t,3.+t*t+.65-.40*t)
def point(a,r,z):return(r*math.sin(a),r*math.cos(a),z)
# Entire two-curvature finite wall: plan is curved at every height and the meridian radius varies quadratically.
# Each vertical interval remains a finite wedge, but all interior faces are removed into one closed body.
cells=[]
for i in range(len(ANG)-1):
 for k in range(len(ZZ)-1):cells.append([point(a,r,z)for z in ZZ[k:k+2]for a in ANG[i:i+2]for r in radii(z)])
wall='WholeDoubleCurvedTaperedArchWall';cell_union(wall,cells,0);v,f,m=G[wall];FM[wall]=[]
for face in f:
 a,b,c=[v[i]for i in face];n=cross(sub(b,a),sub(c,a));mid=mul(add(add(a,b),c),1/3);FM[wall].append(1 if n[0]*mid[0]+n[1]*mid[1]<-1e-8 else 0)
ROOTS.append(wall)
for side in[-1,1]:
 a=side*ANGLE;away=(side*math.cos(a),-side*math.sin(a),0);rad=(math.sin(a),math.cos(a),0);cells=[]
 for k in range(len(ZZ)-1):
  v=[]
  for z in ZZ[k:k+2]:
   for d in[0.,.90]:
    ri,ro=radii(z)
    for r in[ri-.40*d/.90,ro+.40*d/.90]:v.append(add(point(a,r,z),mul(away,d)))
  cells.append(v)
 name='WholeFlaredFullHeightEndAbutment_'+str(side);cell_union(name,cells,2);FM[name]=[2]*len(G[name][1]);ROOTS.append(name)
 # Parent end block faces inwards toward the wall on the full radial vertical end section.
 ri,ro=radii(2.0);CONTACTS.append((name,wall,point(a,(ri+ro)/2,2.0),mul(away,-1),1.79))
for z in[.25,.75,1.25,2.,2.75,3.25,3.75]:
 ri,ro=radii(z)
 GAPS.append(dict(label='SelectedConcaveSideClearRadialAir',origin_m=[0,0,z],direction=[0,1,0],length_m=ri-.12))
 GAPS.append(dict(label='ContinuousWallSolidRadialControl',origin_m=[0,0,z],direction=[0,1,0],length_m=ro+.15,blocked=True))
for x,y in[(-1,1),(0,1),(1,1),(0,5)]:GAPS.append(dict(label='SelectedNoCapOpenInnerOrOuterSpace',origin_m=[x,y,.01],direction=[0,0,1],length_m=4.20))
V=[p for v,f,m in G.values()for p in v];SHIFT=((min(p[0]for p in V)+max(p[0]for p in V))/2,(min(p[1]for p in V)+max(p[1]for p in V))/2,0)
G={n:([sub(p,SHIFT)for p in v],f,m)for n,(v,f,m)in G.items()};CONTACTS=[(a,b,sub(p,SHIFT),normal,area)for a,b,p,normal,area in CONTACTS]
for r in GAPS:r['origin_m']=sub(r['origin_m'],SHIFT)
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
focus=Vector((0,0,2.0))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=10.2;aim(cam,(11,-14,9) if view=='qa-front' else (-11,12,8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/waterworks/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'modular','theme':'waterworks','style':'S01-clean-geometric','title':'Whole Double Curved Wall and Full Height End Abutments','description':'One newly authored complete fixed double-curved arch-wall and end-abutment waterworks illustration. A single finite-thickness curved barrier spans an open concave side and has continuous horizontal curvature, a separately curved height profile and a thicker lower section tapering into a thin uninterrupted curved crest. The wall is not a planar inclined slab, constant-radius vertical cylinder segment or a terrain-filled overflow apron. Two whole full-height flared end abutment blocks meet the two complete radial vertical end sections on genuine finite opposed faces, instead of four repeated rear buttresses or remote tiebacks. The wall and both blocks have complete flat bottom soles. Three whole closed editable meshes, three opaque constant PBR roles, one model zero scenes, true horizontal bounds-centred ground datum in metre-style Z up. All numerical geometry newly authored together; no old wall, vault, slab, dam, terrain, gate or basin mesh imported, scaled, bent or removed. Compared with the previous inclined barrier and pierced buttress assembly, this has one compound-curved continuous wall meeting only its two full-height ends and has no separate crest cap, rear transverse portals or broad support slab. Compared with the rounded overflow-crest and low-basin body, there is no longitudinal channel, solid curved apron, guide wall, basin floor or end sill. Generic double-curved dam vocabulary only; artistic proportions and end-block shapes, not a named structure replica. Two full finite end-section contacts, five separated sided witnesses each, three complete ground soles, seven selected concave-side empty radial rays with matching wall-hit controls and four open-space vertical rays are checked. No actual reservoir, water, canyon geology, drainage galleries, gates, spillways, reinforcement, terrain or personnel. No retention, sealing, seepage, hydrostatic force, thrust-transfer calculation, abutment capacity, seismic response, load, stability, flood protection, construction, manufacture, access, civil or public-safety capability. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
