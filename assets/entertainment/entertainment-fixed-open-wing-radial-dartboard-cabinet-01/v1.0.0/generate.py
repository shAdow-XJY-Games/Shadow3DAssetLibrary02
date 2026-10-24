import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='entertainment-fixed-open-wing-radial-dartboard-cabinet-01'
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



# Complete newly authored shallow cabinet with two fixed open door wings and a real subdivided radial target surface.
box('WholeGroundCabinetSill',(0,0,.018),(.63,.13,.036),0)
box('WholeBackboard',(0,.035,.365),(.58,.045,.66),0)
for x in[-.294,.294]:box('WholeCabinetSide_'+str(x),(x,-.010,.365),(.035,.13,.66),0)
box('WholeTopCabinetCornice',(0,-.005,.710),(.65,.15,.048),0)
# Ground-centred illustration of a wall cabinet; no wall/fasteners or support safety implied.
for label,x,ang in[('Left',-.292,-110),('Right',.292,110)]:
 sign=1 if x<0 else -1
 n=label+'WholeFixedOpenDoor';box(n,(sign*.142,0,.365),(.284,.025,.64),0)
 v,f,m=G[n];a=math.radians(ang);G[n]=([(x+px*math.cos(a)-py*math.sin(a),-.070+px*math.sin(a)+py*math.cos(a),pz)for px,py,pz in v],f,m)
 # Actual flat inset dark writing panel, intentionally blank not a textured score sheet.
 n=label+'WholeBlankInnerPanel';box(n,(sign*.142,.017,.380),(.236,.012,.49),1)
 v,f,m=G[n];G[n]=([(x+px*math.cos(a)-py*math.sin(a),-.070+px*math.sin(a)+py*math.cos(a),pz)for px,py,pz in v],f,m)
 for z in[.16,.56]:lathe_z(label+'WholeFixedHinge_'+str(z),x,-.055,[(0,z-.030),(.012,z-.030),(.012,z+.030),(0,z+.030)],1,12)
cyly('WholeHiddenTargetMount',-.050,.025,0,.375,.095,1,24)
# One closed disc; target colours are assignments on complete connected front triangles, no overlay z-fighting.
N=80;rs=[.018,.035,.125,.140,.205,.220];zc=.375;yf=-.087;yb=-.042
v=[(0,yf,zc)]+[(r*math.cos(math.tau*i/N),yf,zc+r*math.sin(math.tau*i/N))for r in rs for i in range(N)];f=[];mats=[]
for i in range(N):f.append((0,1+i,1+(i+1)%N));mats.append(3)
for k in range(len(rs)-1):
 for i in range(N):
  j=(i+1)%N;a=1+k*N+i;b=1+(k+1)*N+i;c=1+(k+1)*N+j;d=1+k*N+j
  f.extend([(a,b,c),(a,c,d)]);sector=i//4;mat=(4 if k==0 else ((3 if sector%2==0 else 4)if k in[2,4]else(2 if sector%2==0 else 1)));mats.extend([mat,mat])
back=len(v);v.extend((rs[-1]*math.cos(math.tau*i/N),yb,zc+rs[-1]*math.sin(math.tau*i/N))for i in range(N));center=len(v);v.append((0,yb,zc));front=1+(len(rs)-1)*N
for i in range(N):
 j=(i+1)%N;f.extend([(front+i,back+i,back+j),(front+i,back+j,front+j),(center,back+j,back+i)]);mats.extend([1,1,1])
mesh('WholeConnectedRadiallyPartitionedTarget',v,f,1);FM['WholeConnectedRadiallyPartitionedTarget']=mats
# Genuine thin raised annular/spoke boundaries, deliberately proud of the face.
for r in rs: ringy('WholeRaisedTargetRing_'+str(r),-.090,-.085,0,zc,r-.0008,r+.0008,1,80)
for i in range(20):
 a=math.tau*i/20;beam('WholeRaisedTargetSpoke_'+str(i),(.035*math.cos(a),-.089,zc+.035*math.sin(a)),(.220*math.cos(a),-.089,zc+.220*math.sin(a)),.0014,1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeCabinet_WarmWood',(.28,.13,.055,1),.76,0),('TargetDarkAndRaisedBoundary',(.045,.050,.045,1),.79,0),('TargetPaleSectors',(.76,.69,.53,1),.85,0),('TargetMutedRedRings',(.49,.07,.06,1),.81,0),('TargetMutedGreenRings',(.07,.26,.15,1),.81,0)]
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
focus=Vector((0,0,.37))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.09;aim(cam,(1,-6,2.0));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/entertainment/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'entertainment','style':'S01-clean-geometric','title':'Fixed Open Wing Radial Dartboard Cabinet','description':'One newly authored complete fixed-open dartboard cabinet exterior. A full shallow wooden back-and-side enclosure with a grounded bottom sill and wider top cornice carries a separate thick radial target disc. Two whole door wings are fixed outward on four visible hinge barrels; each has one blank inset inner panel. The continuous closed target disc has real connected radial face subdivision with alternating pale and dark sectors, red and green ring zones, a central face and separate thin proud annular and radial boundaries. All colours are opaque constant face-material assignments, never an image texture or overlapping flat decal. No old cabinet or target mesh is imported. One whole model and zero scenes, five opaque untextured PBR materials, metres, Z up and whole ground-centred origin. Door pose is fixed; no arrows, darts, numbers, scoring apparatus, wall, working wall fasteners, characters, throwing simulation, impact response, load or safety performance are supplied. Static illustrative game art only; the ground-centred presentation does not claim a freestanding use configuration.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':5,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
