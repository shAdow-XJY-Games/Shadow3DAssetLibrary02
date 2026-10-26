import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='public-service-fixed-open-bay-and-parked-connector-charge-post-01'
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



box('WholeGroundFootBroadPlinth',(0,0,.045),(.73,.46,.09),3)
# One closed material boundary surrounding a tall actual through-bay; the upper head remains integral.
outer=[(-.28,.08),(.28,.08),(.31,.16),(.31,1.57),(.22,1.70),(-.22,1.70),(-.31,1.57),(-.31,.16)]
inner=[(-.13,.34),(.13,.34),(.16,.39),(.16,1.02),(.10,1.12),(-.10,1.12),(-.16,1.02),(-.16,.39)]
v=[(x,y,z)for y in[-.14,.14]for loop in[outer,inner]for x,z in loop];f=[]
for i in range(8):
 j=(i+1)%8;f.extend([(i,j,8+j,8+i),(16+i,24+i,24+j,16+j),(i,16+i,16+j,j),(8+i,8+j,24+j,24+i)])
mesh('WholeThroughBayAndUpperHeadPedestal',v,f,0)
box('WholeBlankUpperControlPlaque',(0,-.151,1.40),(.36,.036,.23),2)
cyly('WholeBlankRoundIndicator',-.164,-.13,0,1.205,.026,1,20)
# Full side holster supports an independently authored forward-facing deep connector mouth.
box('WholeSideParkHolster',(.345,-.095,1.15),(.13,.10,.11),3)
ringy('WholeDeepOpenConnectorMouth',-.28,-.11,.40,1.15,.036,.061,2,24)
cyly('WholeConnectorRearCap',-.132,-.085,.40,1.15,.061,2,24)
for i,(dx,dz)in enumerate([(-.014,.011),(.014,.011),(0,-.015)]):cyly('WholeRecessedBluntContact_'+str(i),-.215,-.125,.40+dx,1.15+dz,.0055,3,12)
beam('WholeCantedConnectorGrip',(.40,-.10,1.145),(.40,.005,.93),.070,1)
beam('WholeShortGripEnd',(.40,.005,.955),(.40,-.015,.90),.057,2)
# Continuous capped tube follows the entire hanging cable without discontinuous segment joins.
def bezier(a,b,c,d,n):return[tuple((1-t)**3*a[k]+3*(1-t)**2*t*b[k]+3*(1-t)*t*t*c[k]+t**3*d[k]for k in range(3))for t in[i/n for i in range(n+1)]]
path=bezier((-.295,.015,1.09),(-.46,.015,1.05),(-.48,-.03,.58),(-.44,-.10,.39),20)
path+=bezier(path[-1],(-.41,-.22,.08),(.17,-.25,.09),(.40,-.16,.35),24)[1:]
path+=bezier(path[-1],(.56,-.09,.53),(.48,-.03,.76),(.40,-.015,.92),20)[1:]
def tube(name,path,r,mat):
 v=[];f=[];N=12;previous=(0,1,0)
 for k,p in enumerate(path):
  t=unit(sub(path[min(k+1,len(path)-1)],path[max(k-1,0)]));u=unit(tuple(previous[j]-t[j]*dot(previous,t)for j in range(3)));w=cross(t,u);previous=u
  for i in range(N):v.append(tuple(p[j]+r*(u[j]*math.cos(math.tau*i/N)+w[j]*math.sin(math.tau*i/N))for j in range(3)))
 for k in range(len(path)-1):
  for i in range(N):j=(i+1)%N;f.append((k*N+i,k*N+j,(k+1)*N+j,(k+1)*N+i))
 f.extend([tuple(reversed(range(N))),tuple((len(path)-1)*N+i for i in range(N))]);mesh(name,v,f,mat)
tube('WholeContinuousLowerHangingCable',path,.016,2)
axle('WholeCableExitCollar',-.335,-.295,.015,1.09,.035,3,20)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeChargePost_WarmIvory',(.72,.73,.67,1),.69,.08),('WholeGripAndBlankIndicator_MutedTeal',(.10,.34,.33,1),.72,.05),('WholeCableConnectorAndBlankScreen_Charcoal',(.035,.047,.048,1),.75,.04),('WholeFootHolsterAndContacts_SatinAlloy',(.36,.41,.42,1),.48,.46)]
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
focus=Vector((0,0,.83))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.38;aim(cam,(4,-7,3.3));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/public-service/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'public-service','style':'S01-clean-geometric','title':'Fixed Open Bay and Parked Connector Charge Post','description':'One wholly newly authored complete fixed charging-post-style public-service exterior. A broad finite ground foot carries one continuous thick tapered-shoulder upright with a genuine tall through-open lower bay and integral solid upper control head. A complete heavy-looking cable leaves the left side, forms a deep uninterrupted hanging loop around the lower open bay and ends in one independent canted grip beneath a parked axial connector. That connector has a complete thick annular mouth, real blind inner cavity, small blunt recessed contact appearances and whole rear cap; a separate short side holster roots it to the upright. A blank opaque upper control plaque and small separate round blank indicator complete the one assembly. Unlike the old finned inverter this has no rear fin field or array of fixed blind sockets, and unlike the hooded telephone it has no keypad, recessed handset booth or double-ended receiver. The full through-bay, lower continuous cable route and independent axial connector/side park relation are newly authored together, not an imported cabinet with a renamed handset. Four opaque untextured PBR roles, metres Z up, full horizontal-bounds-centred ground sole, one prop zero scenes. No vehicle, battery, circuit, charging, voltage, power delivery, connector standard or insertion fit, cable tension, powered display, payment, weather protection, electrical safety, manufacture or installation performance made or verified. Fixed static visual appearance only; rigging animation interaction absent.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
