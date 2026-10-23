import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='carpentry-static-twin-screw-wooden-hand-clamp-01'
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

# Two newly authored whole bored timber jaws and opposed handled fixed screws.
# A static display, no real thread engagement or clamping force.
PALETTE=[('Jaws_WarmHardwood',(.48,.28,.12,1),.84,0),('ShaftsAndBushes_Steel',(.32,.36,.37,1),.50,.65),('Grips_DarkTimber',(.22,.105,.040,1),.82,0)]
# Orthogonal cell boundary: remove two complete square bushing pockets through
# each full wooden jaw; all internal cell faces are omitted, no split jaw parts.
XS=[-.35,-.228,-.172,.022,.078,.35];ZS=[0,.012,.068,.08]
def jaw(name,y0,y1):
 occupied={(i,k)for i in range(5)for k in range(3)if not(i in[1,3]and k==1)};verts=[];faces=[];lookup={}
 def index(p):
  if p not in lookup:lookup[p]=len(verts);verts.append(p)
  return lookup[p]
 def quad(p):
  aa,bb,cc,dd=map(index,p);faces.extend([(aa,bb,cc),(aa,cc,dd)])
 for i,k in sorted(occupied):
  x0,x1=XS[i:i+2];z0,z1=ZS[k:k+2]
  quad([(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)]);quad([(x0,y1,z0),(x0,y1,z1),(x1,y1,z1),(x1,y1,z0)])
  if(i-1,k)not in occupied:quad([(x0,y0,z0),(x0,y0,z1),(x0,y1,z1),(x0,y1,z0)])
  if(i+1,k)not in occupied:quad([(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)])
  if(i,k-1)not in occupied:quad([(x0,y0,z0),(x0,y1,z0),(x1,y1,z0),(x1,y0,z0)])
  if(i,k+1)not in occupied:quad([(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)])
 record(name,verts,faces,0)
for y,label in[(-.12,'Near'),(.12,'Far')]:
 jaw(label+'WholeTwoPocketTimberJaw',y-.035,y+.035)
 for x,which in[(-.20,'Rear'),(.05,'Front')]:
  # Full closed square-to-round through-bushing, fixed in real wooden pocket.
  n=16;loops=[]
  for yy,outer in[(y-.035,True),(y+.035,True),(y+.035,False),(y-.035,False)]:
   ring=[]
   for j in range(n):
    t=math.tau*j/n+math.pi/4;rr=.028/max(abs(math.cos(t)),abs(math.sin(t)))if outer else .012;ring.append((x+rr*math.cos(t),yy,.04+rr*math.sin(t)))
   loops.append(ring)
  v=sum(loops,[]);f=[]
  for k in range(4):
   for j in range(n):jj=(j+1)%n;aa=k*n+j;bb=k*n+jj;cc=((k+1)%4)*n+jj;dd=((k+1)%4)*n+j;f.extend([(aa,bb,cc),(aa,cc,dd)])
  record(label+which+'WholeCapturedBoredBush',v,f,1)
for x,label,direction in[(-.20,'Rear',1),(.05,'Front',-1)]:
 pipe(label+'WholeFixedSpindle',[(x,-.21,.04),(x,.21,.04)],.0115,1,16)
 # Distinct opposite-side hand grips, no transverse sliding bar.
 pipe(label+'WholeTimberHandGrip',[(x,direction*.19,.04),(x,direction*.34,.04)],.027,2,12)
 # One complete four-turn closed ridge across the empty inter-jaw span.
 v=[];f=[];N=64
 for k in range(N+1):
  t=math.tau*4*k/N;y=-.078+.156*k/N
  for j in range(4):
   b=math.tau*j/4;rr=.012+.002*math.cos(b);v.append((x+rr*math.cos(t),y+.002*math.sin(b),.04+rr*math.sin(t)))
 for k in range(N):
  for j in range(4):jj=(j+1)%4;aa=4*k+j;bb=4*k+jj;cc=4*(k+1)+jj;dd=4*(k+1)+j;f.extend([(aa,bb,cc),(aa,cc,dd)])
 f.extend([(0,3,2),(0,2,1),(4*N,4*N+1,4*N+2),(4*N,4*N+2,4*N+3)])
 record(label+'WholeFixedHelicalRidge',v,f,1)
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
focus=Vector((0,0,.04))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.05;aim(cam,(2,-3,4.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/carpentry/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'carpentry','style':'S01-clean-geometric','title':'Static Twin Screw Wooden Hand Clamp','description':'One newly authored complete static wooden handscrew clamp in a fixed laid-down open pose. Two full elongated timber jaws each have two actual through pockets with complete captured square-to-round bushings. Two parallel steel spindles have separate opposite-side timber grips and continuous fixed visual helical ridges; an empty front gripping bay extends beyond the front spindle. This whole double-spindle wood-jaw apparatus has no long steel guide bar, sliding F-jaw or table-edge C mount, and does not reuse or recolour the old F clamp or bench vise. Twelve separately editable closed meshes, three opaque solid PBR materials, metres, native Z-up and full horizontal bounds-centred ground origin. One prop, zero scenes. Fixed visual only: no stock, bench interface, working threads, jaw adjustment, clamping force, machining, fit standard, durability, load or safety claim. Bushes and shaft ridges intentionally fixed, not a real bearing/thread tolerance proof.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
