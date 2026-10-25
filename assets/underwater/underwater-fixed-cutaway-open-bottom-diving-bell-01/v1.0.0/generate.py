import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='underwater-fixed-cutaway-open-bottom-diving-bell-01'
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
PALETTE=[('DivingBellOpaqueWeatheredShell',(.13,.26,.27,1),.69,.42),('DivingBellDarkSupportIron',(.10,.13,.14,1),.62,.54),('DivingBellSeatsAndRimOchre',(.47,.33,.13,1),.71,.24)]
# Sectioned vessel wall: back and both sides intact, explicit open front cutaway.
def sector(name,profile,a0,a1,m,n=32):
 v=[(r*math.sin(t),-r*math.cos(t),z)for r,z in profile for t in[a0+(a1-a0)*i/n for i in range(n+1)]];f=[];K=len(profile);W=n+1
 for k in range(K):
  q=(k+1)%K
  for i in range(n):a=k*W+i;b=k*W+i+1;c=q*W+i+1;d=q*W+i;f.extend([(a,b,c),(a,c,d)])
 # Planar profile caps at both actual cut edges.
 for edge in [0,n]:
  poly=[(r,z)for r,z in profile]
  if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(poly,poly[1:]+poly[:1]))<0:poly.reverse();ids=list(reversed(range(K)))
  else:ids=list(range(K))
  for a,b,c in earclip(poly):f.append((ids[a]*W+edge,ids[b]*W+edge,ids[c]*W+edge)if edge==0 else(ids[c]*W+edge,ids[b]*W+edge,ids[a]*W+edge))
 # Orient all boundary facets consistently before final positive-volume orientation.
 e={}
 for i,t in enumerate(f):
  for a,b in zip(t,t[1:]+t[:1]):e.setdefault(tuple(sorted((a,b))),[]).append((i,a,b))
 signs={0:1};todo=[0]
 while todo:
  i=todo.pop()
  for a,b in zip(f[i],f[i][1:]+f[i][:1]):
   for j,c,d in e[tuple(sorted((a,b)))]:
    if i==j:continue
    q=signs[i]*(-1 if(a,b)==(c,d)else 1)
    if j not in signs:signs[j]=q;todo.append(j)
    else:assert signs[j]==q
 f=[t if signs[i]>0 else tuple(reversed(t))for i,t in enumerate(f)];record(name,v,f,m)
sector('WholeFrontCutawayThickBellWall',[(.77,.18),(.77,1.25),(.61,1.80),(.55,1.80),(.71,1.24),(.71,.18)],math.radians(53),math.radians(307),0,36)
# Roof is whole, genuinely hollow beneath, with a central isolated through inlet.
turned('WholeDomedBellRoof',0,0,[(.55,1.76),(.63,1.76),(.58,1.91),(.43,2.02),(.10,2.08),(.065,2.08),(.065,2.01),(.40,1.95),(.52,1.85)],0,32)
turned('WholeThickOpenBottomBallastRing',0,0,[(.64,.08),(.84,.08),(.86,.13),(.84,.24),(.64,.24)],2,32)
# Two internal curved seats retain an unobstructed central bottom entry; no full floor.
for side,a0,a1 in [('Left',210,285),('Right',75,150)]:
 sector('WholeInternalCurvedSeat'+side,[(.46,.51),(.715,.51),(.715,.58),(.46,.58)],math.radians(a0),math.radians(a1),2,12)
 for j,a in enumerate([a0+15,a1-15]):
  t=math.radians(a);x,y=.66*math.sin(t),-.66*math.cos(t)
  pipe('WholeSeatRoot'+side+str(j),[(x,y,.20),(x,y,.53)],.025,1,8)
# Four complete external straps seat on the whole lower rim and roof shoulders.
for j,a in enumerate([55,125,235,305]):
 t=math.radians(a);pipe('WholeExternalSuspensionStrap'+str(j),[(.81*math.sin(t),-.81*math.cos(t),.18),(.79*math.sin(t),-.79*math.cos(t),1.23),(.62*math.sin(t),-.62*math.cos(t),1.80),(.37*math.sin(t),-.37*math.cos(t),2.02)],.028,1,4)
# Complete top hanging eye plus rooted roof bracket; not a detached handling hook.
box('WholeTopEyeRoot',(-.15,-.10,2.02),(.15,.10,2.13),1)
wheel('WholeTopLiftingEye',0,0,2.25,.19,.11,.075,1)
# The continuous inlet has a real opening, but no gas system or operational air supply claim.
turned('WholeTopInletCollar',.31,.02,[(.042,1.96),(.067,1.96),(.067,2.16),(.042,2.16)],2,16)
# Low static display feet keep the bottom mouth visibly open above the preview ground.
for i,a in enumerate([45,135,225,315]):
 t=math.radians(a);x,y=.75*math.sin(t),-.75*math.cos(t)
 box('WholeStaticDisplayFoot'+str(i),(x-.065,y-.065,0),(x+.065,y+.065,.13),1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()};FM={n:[m]*len(f)for n,(v,f,m)in G.items()}
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
focus=Vector((0,0,1.20))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.05;aim(cam,(3,-8,3.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/underwater/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'underwater','style':'S01-clean-geometric','title':'Fixed Cutaway Open Bottom Diving Bell','description':'One newly authored complete fixed cutaway open-bottom diving-bell display. A thick tapered cylindrical rear-and-side wall meets a full hollow domed roof above a wide genuinely open lower ballast ring. An intentional front sector is removed for display, exposing two curved internal side seats and their fixed roots while leaving the central bottom opening unfilled. Four full exterior straps meet the lower ring and roof shoulders; a rooted upper hanging eye and a short inlet collar complete the vessel silhouette. Small integral display feet raise the open mouth above the ground. This is a sectioned chamber with internal occupancy space and suspension, not an enlarged wearable three-window helmet or a lab torsion case with a different rod. No old meshes imported, three opaque constant PBR materials, metres and centred ground datum. One static exhibit model, zero scenes. The front cutaway is intentionally not sealed; no person, breathing system, air retention, pressure, diving, buoyancy, hoisting capacity, fabrication, historical reconstruction or safety claim. Rigging, animation and interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
