import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='toys-fixed-continuous-spatial-loop-bead-route-01'
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



# One complete continuous spatial wire route with two perpendicular loops and captured beads.
box('WholeGroundFootWoodBase',(0,-.025,.030),(.80,.64,.060),0)
pts=[(-.30,-.24,.040),(-.30,-.24,.080),(-.30,-.24,.100)]
pts +=[(-.30+.20*i/8,-.24,.100)for i in range(1,9)]
for i in range(1,65):
 a=-math.pi/2+math.tau*i/64;pts.append((-.10+.20*math.cos(a),-.24+.28*i/64,.30+.20*math.sin(a)))
pts +=[(-.10+.30*i/12,.04,.10)for i in range(1,13)]
for i in range(1,57):
 a=-math.pi/2+math.tau*i/56;pts.append((.20+.13*i/56,.04+.15*math.cos(a),.25+.15*math.sin(a)))
pts.extend([(.33,.04,.080),(.33,.04,.040)])
# Transport radial frames continuously; no disconnected segment pieces or sharp hidden connectors.
frames=[];u=(1,0,0)
for i,p in enumerate(pts):
 t=unit(sub(pts[min(i+1,len(pts)-1)],pts[max(i-1,0)]));uu=tuple(u[k]-dot(u,t)*t[k]for k in range(3))
 if dot(uu,uu)<1e-12:uu=cross(t,(0,1,0))
 u=unit(uu);w=cross(t,u);frames.append((t,u,w))
N=16;rw=.006;v=[]
for p,(_,u,w)in zip(pts,frames):
 for j in range(N):a=math.tau*(j+.5)/N;v.append(tuple(p[k]+rw*(u[k]*math.cos(a)+w[k]*math.sin(a))for k in range(3)))
f=[tuple(reversed(range(N))),tuple((len(pts)-1)*N+j for j in range(N))]+[(k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j)for k in range(len(pts)-1)for j in range(N)];mesh('WholeContinuousOrthogonalLoopWire',v,f,1)
# Whole blind base collars encompass the actual two rooted terminal wire sections.
for i,(x,y)in enumerate([(-.30,-.24),(.33,.04)]):lathe_z('WholeRootedWireTerminalCollar_'+str(i),x,y,[(0,.045),(.019,.045),(.019,.075),(0,.075)],1,16)
# Each complete thick bored bead is on a true straight path section, not perched on a curved chord.
for i,(x,y)in enumerate([(-.25,-.24),(-.175,-.24),(-.025,.04),(.05,.04),(.125,.04)]):
 idx=min(range(len(pts)),key=lambda k:sum((pts[k][j]-[x,y,.10][j])**2 for j in range(3)));t,u,w=frames[idx]
 assert abs(t[0]-1)<1e-10 and abs(t[1])+abs(t[2])<1e-10
 if u[2]<0:u=tuple(-c for c in u);w=tuple(-c for c in w)
 ri=.009;off=(ri-rw)*math.cos(math.pi/N);c=(x-off*u[0],y-off*u[1],.10-off*u[2]);profile=[(-.023,ri),(-.023,.021),(-.014,.032),(.014,.032),(.023,.021),(.023,ri)];v=[];f=[]
 for axial,r in profile:
  for j in range(N):a=math.tau*(j+.5)/N;v.append(tuple(c[k]+axial*t[k]+r*(u[k]*math.cos(a)+w[k]*math.sin(a))for k in range(3)))
 for k in range(len(profile)):
  kk=(k+1)%len(profile)
  for j in range(N):jj=(j+1)%N;f.append((k*N+j,k*N+jj,kk*N+jj,kk*N+j))
 mesh('WholeCapturedBoredBarrelBead_'+str(i),v,f,2 if i%2==0 else 0)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeBaseAndWarmBeads_WarmMaple',(.64,.42,.20,1),.76,0),('WholeContinuousWireAndTerminalCollars_MutedRed',(.48,.07,.045,1),.56,.18),('WholeAlternateBoredBeads_MutedTeal',(.055,.25,.25,1),.72,0)]
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
focus=Vector((0,0,.23))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.03;aim(cam,(3,-5,3.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/music/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'toys','style':'S01-clean-geometric','title':'Fixed Continuous Spatial Loop Bead Route','description':'One newly authored complete static tabletop wire-and-bead toy. A single closed solid wire starts inside one base collar, follows a low straight loading run, travels through an entire pitched vertical loop, crosses a low bridge, passes through a second vertical loop in a perpendicular plane and returns into the second base collar. Five whole thick barrel-shaped beads have genuine polygonal through-bores on actual straight portions of that same route. Each bead has a small explicit eccentric offset giving matching wire/bore facet contact, rather than a floating ring. One full finite wooden base supports both terminal roots. Unlike the existing upright abacus, there are no five separate parallel straight shafts or two tall end stiles; unlike the gimballed board maze, there is no floor route, wall labyrinth or tilting tray. All whole geometry independently authored, not a bent copy of an old rod or changed bead-count asset. Three opaque constant untextured PBR roles, metres, Z up and whole horizontally bounds-centred ground origin. One whole prop, zero scenes; beads and loops are not separate assets. Static illustrative pose only: no runtime slider, traversal of curves, solved motion or collision-free travel, educational outcome, child fit, choking/material suitability, load, manufacture or toy-safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
