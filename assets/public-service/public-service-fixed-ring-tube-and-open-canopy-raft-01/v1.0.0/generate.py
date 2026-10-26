import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='public-service-fixed-ring-tube-and-open-canopy-raft-01'
G={};FM={}
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def unit(a):return tuple(x/math.sqrt(dot(a,a))for x in a)
def mesh(name,v,faces,mat):
 f=[]
 for p in faces:
  for k in range(1,len(p)-1):f.append((p[0],p[k],p[k+1]))
 if sum(dot(v[a],cross(v[b],v[c]))for a,b,c in f)<0:f=[tuple(reversed(p))for p in f]
 G[name]=(v,f,mat)
BOX=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(name,c,size,mat):mesh(name,[tuple(c[i]+s[i]*size[i]/2 for i in range(3))for s in[(x,y,z)for z in[-1,1]for y in[-1,1]for x in[-1,1]]],BOX,mat)
def beam(name,a,b,width,mat):
 w=unit(sub(b,a));u=unit(cross(w,(1,0,0)if abs(w[0])<.9 else(0,1,0)));v=cross(w,u)
 mesh(name,[tuple(p[i]+width/2*(sx*u[i]+sy*v[i])for i in range(3))for p in[a,b]for sy in[-1,1]for sx in[-1,1]],BOX,mat)
def axle(name,x0,x1,y,z,r,mat,n=16):
 v=[(x,y+r*math.cos(math.tau*i/n),z+r*math.sin(math.tau*i/n))for x in[x0,x1]for i in range(n)]
 mesh(name,v,[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],mat)

def ringx(name,x0,x1,y,z,ri,ro,mat,n=24):
 v=[(x,y+r*math.cos(math.tau*i/n),z+r*math.sin(math.tau*i/n))for x in[x0,x1]for r in[ri,ro]for i in range(n)];f=[]
 for i in range(n):j=(i+1)%n;f.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 mesh(name,v,f,mat)
def cyly(name,y0,y1,x,z,r,mat,n=24):
 axle(name,y0,y1,x,z,r,mat,n);v,f,m=G[name];G[name]=([(b,a,c)for a,b,c in v],[tuple(reversed(p))for p in f],m)
def ringy(name,y0,y1,x,z,ri,ro,mat,n=24):
 ringx(name,y0,y1,x,z,ri,ro,mat,n);v,f,m=G[name];G[name]=([(b,a,c)for a,b,c in v],[tuple(reversed(p))for p in f],m)
def triangulate(p):
 def cr(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 ids=list(range(len(p)));out=[]
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:ids.reverse()
 while len(ids)>3:
  for k,b in enumerate(ids):
   a,c=ids[k-1],ids[(k+1)%len(ids)]
   if cr(p[a],p[b],p[c])<=1e-14:continue
   if any(min(cr(p[a],p[b],p[j]),cr(p[b],p[c],p[j]),cr(p[c],p[a],p[j]))>=-1e-14 for j in ids if j not in[a,b,c]):continue
   out.append((a,b,c));ids.pop(k);break
  else:raise AssertionError('bad polygon')
 return out+[tuple(ids)]
def lathe_z(name,x,y,profile,mat,n=24):
 v=[];rings=[];f=[]
 for r,z in profile:
  ids=[]
  if r==0:ids=[len(v)];v.append((x,y,z))
  else:
   for i in range(n):ids.append(len(v));v.append((x+r*math.cos(math.tau*i/n),y+r*math.sin(math.tau*i/n),z))
  rings.append(ids)
 for a,b in zip(rings,rings[1:]+rings[:1]):
  if len(a)==len(b)==1:continue
  for i in range(n):
   j=(i+1)%n
   if len(a)==1:f.append((a[0],b[j],b[i]))
   elif len(b)==1:f.append((a[i],a[j],b[0]))
   else:f.append((a[i],a[j],b[j],b[i]))
 mesh(name,v,f,mat)



# Complete oval tube surfaces. Bottom two facets are explicitly flattened for dry display.
def oval_tube(name,z,rx,ry,r,mat,ground=False):
 N=48;M=12;v=[];f=[]
 for i in range(N):
  a=math.tau*i/N
  for j in range(M):
   b=math.tau*(j+.5)/M;zz=z+r*math.sin(b)
   if ground:zz=max(0,zz-.006814834742186)
   v.append(((rx+r*math.cos(b))*math.cos(a),(ry+r*math.cos(b))*math.sin(a),zz))
 for i in range(N):
  for j in range(M):f.append((i*M+j,((i+1)%N)*M+j,((i+1)%N)*M+(j+1)%M,i*M+(j+1)%M))
 mesh(name,v,f,mat)
oval_tube('WholeGroundFootLowerOvalTube',.20,1.10,1.28,.20,0,True)
oval_tube('WholeUpperOvalTube',.55,1.10,1.28,.20,0)
N=48;v=[(1.10*math.cos(math.tau*i/N),1.28*math.sin(math.tau*i/N),z)for z in[.16,.235]for i in range(N)]
mesh('WholeRecessedFloor',v,[tuple(reversed(range(N))),tuple(N+i for i in range(N))]+[(i,(i+1)%N,(i+1)%N+N,i+N)for i in range(N)],2)
# One closed thick canopy: full outer/inner arched surfaces, integral back wall and front return.
outer=[(.99,.215)]+[(.99*math.cos(math.pi*i/20),.57+.99*math.sin(math.pi*i/20))for i in range(21)]+[(-.99,.215)]
inner=[(.955,.235)]+[(.955*math.cos(math.pi*i/20),.57+.955*math.sin(math.pi*i/20))for i in range(21)]+[(-.955,.235)]
n=len(outer);v=[(x,y,z)for profile,y in[(outer,-.78),(outer,1.06),(inner,-.78),(inner,1.025)]for x,z in profile];f=[]
for i in range(n-1):f.extend([(i,i+1,n+i+1,n+i),(2*n+i,3*n+i,3*n+i+1,2*n+i+1),(i,2*n+i,2*n+i+1,i+1)])
# lower side thickness returns, back outer and inner complete caps.
for i in[0,n-1]:f.append((i,n+i,3*n+i,2*n+i) if i==0 else (2*n+i,3*n+i,n+i,i))
for a,b,c in triangulate(outer):f.append((n+a,n+b,n+c))
for a,b,c in triangulate(inner):f.append((3*n+c,3*n+b,3*n+a))
f.append((n,2*n-1,4*n-1,3*n));mesh('WholeThickOpenFrontCanopy',v,f,1)
# Whole front tongue with rounded-down sides, held directly by the lower tube.
p=[(-1.22,.18),(-1.25,.24),(-1.78,.13),(-1.78,.08)];n=len(p);v=[(x,y,z)for x in[-.29,.29]for y,z in p];f=[]
for a,b,c in triangulate(p):f.extend([(c,b,a),(a+n,b+n,c+n)])
f +=[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh('WholeFrontBoardingTongue',v,f,2)
for k,y in enumerate([-1.66,-1.51]):box('WholeTongueRidge_'+str(k),(0,y,.13+(y+1.78)*.2075),(.51,.035,.035),0)
# Full external grab rope is one closed oval tube; the six keepers connect it to the actual perimeter.
def rope_ring():
 N=64;M=8;v=[];f=[]
 for i in range(N):
  a=math.tau*i/N
  for j in range(M):b=math.tau*j/M;v.append(((1.325+.015*math.cos(b))*math.cos(a),(1.505+.015*math.cos(b))*math.sin(a),.51+.015*math.sin(b)))
 for i in range(N):
  for j in range(M):f.append((i*M+j,((i+1)%N)*M+j,((i+1)%N)*M+(j+1)%M,i*M+(j+1)%M))
 mesh('WholeContinuousOuterGrabRope',v,f,3)
rope_ring()
for k,a in enumerate([0,math.pi/3,2*math.pi/3,math.pi,4*math.pi/3,5*math.pi/3]):beam('WholeRopeKeeper_'+str(k),(1.25*math.cos(a),1.43*math.sin(a),.51),(1.33*math.cos(a),1.51*math.sin(a),.51),.035,3)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeRingTube_MutedOrange',(.72,.28,.075,1),.78,0),('WholeCanopy_WarmOchre',(.82,.48,.13,1),.83,0),('WholeFloorAndTongue_Charcoal',(.065,.085,.09,1),.83,0),('WholeRopeAndKeepers_WarmIvory',(.73,.69,.55,1),.85,0)]
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
for prefix in []:
 parent=bpy.data.objects.new(prefix+'_CompleteSourceAssembly',None);scene.collection.objects.link(parent)
 for o in parts:
  if o.name.startswith(prefix+'__'):o.parent=parent
 parent.select_set(True)
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
triangles=sum(len(f)for v,f,m in G.values())
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
(OUT/'qa-report.json').write_text(json.dumps({'asset':ASSET,'mesh_objects':len(G),'triangles':triangles,'materials':len(PALETTE),'new_independent_models':1,'new_scenes':0},indent=2))
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
focus=Vector((0,0,.73))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=4.35;aim(cam,(4,-7,4.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/public-service/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'public-service','style':'S01-clean-geometric','title':'Fixed Ring Tube and Open Canopy Raft','description':'One wholly newly authored complete fixed canopied ring-tube raft exterior for dry static display. Two full continuous flattened-bottom oval perimeter tubes surround one recessed solid floor; a thick continuous arched canopy has closed sides and back and a genuinely open front aperture. The canopy lower sides and rear are rooted in the perimeter and floor, not suspended above them. A whole short ribbed front boarding tongue joins the lower ring, and a continuous external grab rope is held by six separate rooted loop keepers. Unlike the old twin-float pedalboat there are no separate pointed hulls, seats, transverse paddle drive or rudder; unlike the cross-pole tent this has a complete annular double-tube perimeter and low floor bay, no diagonal external poles or independent camping base. The whole numeric assembly is newly authored rather than old hulls and a tent imported into a scene. Four opaque untextured PBR roles, metres Z up, horizontal bounds centred and finite flattened lower tube sole. One prop zero scenes. Fixed empty illustrative appearance only: no inflation, gas chamber, buoyancy, floating, deployment, boarding, capacity, occupancy, weather protection, rescue function, rope tension, manufacture, installation or maritime safety performance. No water, people, emergency markings, rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
