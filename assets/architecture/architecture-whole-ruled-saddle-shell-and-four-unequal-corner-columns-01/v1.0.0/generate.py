import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='architecture-whole-ruled-saddle-shell-and-four-unequal-corner-columns-01'
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
PALETTE=[('WholeRuledSaddlePatinaTop',(.17,.35,.32,1),.73,.14),('WholeSaddlePaleSoffitAndEdge',(.61,.59,.49,1),.89,0),('WholeUnequalCornerColumns',(.42,.40,.34,1),.91,0)]
FM={};ROOTS=[];CONTACTS=[];GAPS=[];SHIFT=(0,0,0);NGRID=16;SPAN=5.0;STEP=SPAN/NGRID;THICK=.12
height=lambda x,y:3.3+.12*x*y+.06*x+.03*y
# Entire closed saddle shell, a triangulated doubly ruled negative-curvature field, not intersecting roofs.
xs=[-2.5+i*STEP for i in range(NGRID+1)];ys=list(xs);v=[(x,y,height(x,y)+dz)for dz in[0,THICK]for y in ys for x in xs];stride=NGRID+1;offset=stride*stride;f=[];fm=[]
for j in range(NGRID):
 for i in range(NGRID):
  a=j*stride+i;b=a+1;c=a+stride+1;d=a+stride
  f += [(a,c,b),(a,d,c),(a+offset,b+offset,c+offset),(a+offset,c+offset,d+offset)];fm += [1,1,0,0]
boundary=list(range(stride))+[j*stride+NGRID for j in range(1,stride)]+[NGRID*stride+i for i in range(NGRID-1,-1,-1)]+[j*stride for j in range(NGRID-1,0,-1)]
for a,b in zip(boundary,boundary[1:]+boundary[:1]):f += [(a,b,b+offset),(a,b+offset,a+offset)];fm += [1,1]
record('WholeDoublyRuledSaddleShell',v,f,0);FM['WholeDoublyRuledSaddleShell']=fm
# Each whole column has a broad flat sole, an integral sloping foot shoulder and a top
# that exactly retains the two actual underside triangles of one complete corner cell.
for ix in[0,NGRID-1]:
 for iy in[0,NGRID-1]:
  x0,x1=xs[ix:ix+2];y0,y1=ys[iy:iy+2];cx=(x0+x1)/2;cy=(y0+y1)/2;top=[(x0,y0,height(x0,y0)),(x1,y0,height(x1,y0)),(x1,y1,height(x1,y1)),(x0,y1,height(x0,y1))];v=[(cx+dx,cy+dy,0)for dx,dy in[(-.30,-.30),(.30,-.30),(.30,.30),(-.30,.30)]]+[(x,y,.18)for x,y,z in top]+top;f=[(0,2,1),(0,3,2),(8,9,10),(8,10,11)]
  for k in range(2):
   for i in range(4):
    j=(i+1)%4;a=k*4+i;b=k*4+j;c=(k+1)*4+j;d=(k+1)*4+i;f.extend([(a,b,c),(a,c,d)])
  name='WholeUnequalCornerColumn_'+str(ix)+'_'+str(iy);record(name,v,f,2);FM[name]=[2]*len(f);ROOTS.append(name);point=tuple(sum(top[i][k]for i in[0,1,2])/3 for k in range(3));CONTACTS.append((name,'WholeDoublyRuledSaddleShell',point,.098))
for z in[.4,1.4,2.2]:
 for axis in[0,1]:GAPS.append(dict(label='FullCentralOpenBayCrossway',origin_m=[-3 if axis==0 else 0,-3 if axis==1 else 0,z],direction=[1 if axis==0 else 0,1 if axis==1 else 0,0],length_m=6))
GAPS += [dict(label='FullCentralUnderSaddleVoid',origin_m=[0,0,.01],direction=[0,0,1],length_m=3.20),dict(label='CentralWholeSaddleSolidControl',origin_m=[0,0,.01],direction=[0,0,1],length_m=3.6,blocked=True)]
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
focus=Vector((0,0,2.15))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=8.2;aim(cam,(11,-15,9) if view=='qa-front' else (-15,-6,8.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/architecture/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'prop','theme':'architecture','style':'S01-clean-geometric','title':'Whole Ruled Saddle Shell and Four Unequal Corner Columns','description':'One wholly newly authored complete fixed anticlastic saddle-shell architectural bay. One uninterrupted thick shell follows a bilinear doubly ruled height field across a square footprint: diagonally opposed directions bend with opposite signs, while both families of constant-coordinate rulings and all four outer edges remain straight in the mathematical design. The low-poly realization uses explicit consistently wound triangular facets with a finite vertical top-to-soffit separation and closed full perimeter walls. Four whole vertical corner columns have four distinct top height ranges; each integral broadened flat foot narrows into a straight shaft and ends in two actual sloped triangular bearing faces exactly matching one complete corner cell of the saddle soffit. Broad real open side bays and a completely empty central under-roof volume remain visible. This is not the old positive-curvature spherical sail vault, crossed cylindrical groin, nested barrel shell, planar folded chevron or cable-net skeleton: the entire saddle geometry and all matching whole columns are newly authored together, with no old shell, ribs, supports or other asset imported or cropped. Five closed separately editable whole material meshes and three opaque untextured PBR roles distinguish the full exterior surface, soffit/perimeter and complete columns. Four finite actual opposed triangular bearing patches and four broad planar ground soles, metre-style Z-up; one new model zero scenes. The regular fine facets are intentional low-poly approximation, not a mathematically smooth rendered surface or a real constant-normal-thickness concrete shell. Generic form vocabulary only; no historic building replica, material thickness standard or real project dimensions used. No membrane stress, thrust balance, concrete reinforcement, foundation, load or wind rating, roof drainage, building-code compliance, human access, construction or structural safety capability claimed. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
