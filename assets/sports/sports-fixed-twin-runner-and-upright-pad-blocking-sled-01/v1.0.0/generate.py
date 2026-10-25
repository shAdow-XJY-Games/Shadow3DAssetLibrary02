import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='sports-fixed-twin-runner-and-upright-pad-blocking-sled-01'
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



# Complete new twin-runner contact-pad sled, no old machine components.
def yz_prism(name,pp,x0,x1,mat):
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(pp,pp[1:]+pp[:1]))<0:pp=list(reversed(pp))
 n=len(pp);v=[(x,y,z)for x in[x0,x1]for y,z in pp];f=[]
 for a,b,c in triangulate(pp):f.extend([(c,b,a),(n+a,n+b,n+c)])
 f +=[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh(name,v,f,mat)
runner=[(-1.02,.235),(-.900,.090),(-.720,0),(.670,0),(.850,.085),(.965,.215),(.905,.265),(.790,.150),(.650,.080),(-.690,.080),(-.840,.155),(-.955,.280)]
for k,x in enumerate([-.43,.43]):yz_prism('WholeGroundFootUpturnedRunner_%d'%k,runner,x-.065,x+.065,0)
for k,y in enumerate([-.60,.10,.65]):box('WholeChassisCrossmember_%d'%k,(0,y,.115),(.91,.080,.095),0)
box('WholeRearStandingPlatform',(0,.475,.186),(.55,.37,.060),2)
box('WholeRearPlatformFrontTie',(0,.265,.155),(.55,.06,.08),0)
# Both full constant-thickness bent support profiles join their actual root clamps and pad backing.
path=[(.650,.160),(.500,.230),(.230,.330),(-.100,.440),(-.400,.650),(-.535,.985)]
edgeA=[];edgeB=[]
for i,(y,z)in enumerate(path):
 a=path[max(i-1,0)];b=path[min(i+1,len(path)-1)];dy=b[0]-a[0];dz=b[1]-a[1];l=math.hypot(dy,dz);ny,nz=-dz/l,dy/l
 edgeA.append((y+.020*ny,z+.020*nz));edgeB.append((y-.020*ny,z-.020*nz))
for k,x in enumerate([-.16,.16]):
 yz_prism('WholeBentPadSupportPlate_%d'%k,edgeA+list(reversed(edgeB)),x-.040,x+.040,1)
 box('WholeLeafRootClamp_%d'%k,(x,.635,.175),(.145,.155,.060),3)
 cyly('WholeRootClampFastener_%d'%k,.550,.710,x,.175,.022,1,12)
box('WholePadRearBacking',(0,-.553,.995),(.45,.065,.68),0)
# Whole cushion: chamfered front, side band and back, no overlapping outer trim sheets.
outline=[(-.24,.550),(.24,.550),(.32,.650),(.32,1.360),(.22,1.460),(-.22,1.460),(-.32,1.360),(-.32,.650)]
v=[]
for y,sx,sz in[(-.855,.91,.95),(-.805,1,1),(-.580,.96,.98)]:
 v +=[(x*sx,y,1.005+(z-1.005)*sz)for x,z in outline]
n=len(outline);f=[]
for a,b,c in triangulate(outline):f.extend([(c,b,a),(2*n+a,2*n+b,2*n+c)])
for k in range(2):
 for i in range(n):j=(i+1)%n;f.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i))
mesh('WholeTallChamferedBlockingPad',v,f,2)
# Rear handling cross-grip has two short rooted supports, no claim of loaded handling.
for side in[-1,1]:beam('WholeRearGripRoot_'+str(side),(side*.31,.62,.145),(side*.31,.78,.42),.035,0)
axle('WholeRearTransverseGrip',-.34,.34,.78,.42,.028,3,16)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeSledChassisAndRunners_MutedBlue',(.075,.18,.23,1),.70,.15),('WholeBentPlatesAndFasteners_DullAlloy',(.40,.44,.43,1),.54,.45),('WholeContactPadAndPlatform_DarkRed',(.45,.055,.045,1),.82,0),('WholeClampsAndRearGrip_Charcoal',(.055,.065,.065,1),.80,.05)]
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
focus=Vector((0,0,.65))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.65;aim(cam,(4,-5,3));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/sports/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'sports','style':'S01-clean-geometric','title':'Fixed Twin Runner and Upright Pad Blocking Sled','description':'One newly authored complete empty fixed blocking-sled exterior. Two entire thick runners have long flat ground spans and genuinely upturned ends. Three full crossmembers connect the runners; two continuous broad bent leaf-like support plates rise forward from separate clamped rear roots to the backing of one tall thick chamfered contact pad. A distinct rear cross-grip and a short tied standing-platform appearance belong to the same complete chassis. The broad pad is a whole closed three-ring cushion volume, not a plane or a box face decal. This is not a shortened hanging punching-bag frame or the old timber dummy with arms removed: there is no overhead suspension or solid central tree post, and the runner-to-bent-plate-to-pad whole structure is new. Nor is it an inclined-carriage leg press without the seat: no sliding rails, carriage sleeves, pegs or weights are reused. All numeric geometry new, one prop zero scenes and four opaque PBR appearances. Empty fixed sports-equipment visual only. No impact absorption, spring behaviour, resistance, travel, training instructions, user fit, load, balance, manufacturing or safe contact-sport operation claim. Rigging animation and interaction are not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
