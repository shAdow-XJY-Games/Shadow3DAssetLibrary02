import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='coral-reef-fixed-twin-frame-and-nose-pocket-diving-mask-01'
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



# Whole new shallow twin-lens mask exterior; all lenses are intentionally opaque.
def loopmesh(name,loops,mat):
 n=len(loops[0]);v=[p for q in loops for p in q];f=[]
 for k in range(len(loops)):
  h=(k+1)%len(loops)
  for i in range(n):j=(i+1)%n;f.append((k*n+i,k*n+j,h*n+j,h*n+i))
 mesh(name,v,f,mat)
def solid_profile(name,p,y0,y1,mat):
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);v=[(x,y,z)for y in[y0,y1]for x,z in p];f=[]
 for a,b,c in triangulate(p):f.extend([(c,b,a),(a+n,b+n,c+n)])
 f +=[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh(name,v,f,mat)
# One continuous flared soft perimeter, including a true low nose contour, with an open rear.
outer=[(-.145,.070),(-.151,.125),(-.126,.158),(-.045,.163),(0,.151),(.045,.163),(.126,.158),(.151,.125),(.145,.070),(.113,.045),(.048,.042),(.025,.016),(-.025,.016),(-.048,.042),(-.113,.045)]
inner=[(x*.92,.095+(z-.095)*.83)for x,z in outer]
front=[(x*.94,.095+(z-.095)*.94)for x,z in outer];fronti=[(x*.89,.095+(z-.095)*.77)for x,z in outer]
loopmesh('WholeContinuousFlaredOpenRearFaceSkirt',[[(x,.024,z)for x,z in outer],[(x,-.030,z)for x,z in front],[(x,-.026,z)for x,z in fronti],[(x,.024,z)for x,z in inner]],0)
# Two independently complete angled polygonal lens frames; not a solid electronics visor.
left=[(-.132,.079),(-.132,.128),(-.114,.145),(-.035,.145),(-.020,.126),(-.029,.082),(-.052,.059),(-.112,.059)]
for sign,tag in[(1,'Left'),(-1,'Right')]:
 p=[(sign*x,z)for x,z in left];cx=sign*(-.077);cz=.103
 q=[(cx+(x-cx)*.82,cz+(z-cz)*.78)for x,z in p]
 loopmesh('WholeIndependentLensFrame_'+tag,[[(x,-.046,z)for x,z in p],[(x,-.046,z)for x,z in q],[(x,-.023,z)for x,z in q],[(x,-.023,z)for x,z in p]],1)
 # Complete finite lens edge sits inside the corresponding full frame.
 ins=[(cx+(x-cx)*1.025,cz+(z-cz)*1.025)for x,z in q]
 solid_profile('WholeOpaqueIllustrativeLens_'+tag,ins,-.042,-.029,2)
box('WholeUpperNoseBridge',(0,-.032,.137),(.053,.024,.019),1)
# A closed thick open-back nose pocket, projecting from the lower middle, no mouth enclosure.
p=[(-.026,0),(.026,0),(.039,.025),(.029,.065),(0,.090),(-.029,.065),(-.039,.025)]
q=[(x*.75,.043+(z-.043)*.72)for x,z in p];n=len(p)
# Back outer, projecting front outer, projecting front inner, back inner. Front surfaces close the pocket wall, not its rear aperture.
loops=[[(x,.018,z)for x,z in p],[(x*.78,-.084,0 if z==0 else .037+(z-.037)*.84)for x,z in p],[(x*.78,-.078,.037+(z-.037)*.84)for x,z in q],[(x,.018,z)for x,z in q]]
v=[t for l in loops for t in l];f=[]
for a,b in[(0,1),(2,3),(3,0)]:
 for i in range(n):j=(i+1)%n;f.append((a*n+i,a*n+j,b*n+j,b*n+i))
for a,b,c in triangulate([(x,z)for x,y,z in loops[1]]):f.append((n+a,n+b,n+c))
for a,b,c in triangulate([(x,z)for x,y,z in loops[2]]):f.append((2*n+c,2*n+b,2*n+a))
mesh('WholeOpenBackProjectingNosePocket',v,f,0)
# Closed strap root ears and actual open rectangular buckles at both lateral sides.
for sign,tag in[(-1,'Left'),(1,'Right')]:
 box('WholeStrapRootEar_'+tag,(sign*.145,.008,.107),(.026,.044,.030),1)
 # Buckle is a complete rectangular annulus in YZ, not a painted slot.
 p=[(-.006,.087),(.051,.087),(.051,.128),(-.006,.128)];q=[(.004,.096),(.041,.096),(.041,.119),(.004,.119)]
 loopmesh('WholeOpenSideBuckle_'+tag,[[(sign*.152,y,z)for y,z in p],[(sign*.152,y,z)for y,z in q],[(sign*.161,y,z)for y,z in q],[(sign*.161,y,z)for y,z in p]],1)
# One continuous flat flexible-style rear band with genuine open head space.
v=[];N=32
for i in range(N+1):
 a=math.pi*i/N
 v +=[(rx*math.cos(a),.026+ry*math.sin(a),z)for rx,ry,z in[(.153,.167,.097),(.159,.173,.097),(.159,.173,.117),(.153,.167,.117)]]
f=[(3,2,1,0),tuple(N*4+i for i in range(4))]+[(k*4+i,k*4+(i+1)%4,(k+1)*4+(i+1)%4,(k+1)*4+i)for k in range(N)for i in range(4)];mesh('WholeContinuousRearRetentionBand',v,f,0)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeSoftSkirtNoseAndBand_Charcoal',(.045,.065,.068,1),.84,.0),('WholeLensFramesAndBuckles_MutedTeal',(.075,.34,.34,1),.55,.1),('WholeOpaqueIllustrativeLens_SmokeBlue',(.16,.29,.37,1),.25,.28)]
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
focus=Vector((0,0,.080))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.48;aim(cam,(3,-5,3.4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/coral-reef/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'coral-reef','style':'S01-clean-geometric','title':'Fixed Twin Frame and Nose Pocket Diving Mask','description':'One newly authored complete static twin-lens diving-mask exterior. Two broad polygonal front frames hold separate finite opaque illustrative lens inserts, joined by a short upper nose bridge. A continuous flared soft-style perimeter has an actual open rear and surrounds both eyes; a distinct thick hollow projecting nose pocket has a real rear opening without any mouth enclosure or breathing connector. Two whole open side buckles and root ears attach one complete fixed rear retention band around empty head space. New full geometry rather than a shortened old breathing facepiece or recoloured electronic headset: no visor casing, rear eyecup cylinders, top strap, pressure helmet or mannequin. Three opaque untextured PBR roles, metres, Z up, horizontal-envelope-centred ground origin. One static prop and zero scenes. Opaque lens surfaces deliberately do not transmit light. No optical visibility, sealing, breathing, head fit, wearability, protection, pressure performance, buckling or diving safety capability; no manufacturing or actual-use guidance. Fixed display pose only, not an articulated or functional apparatus.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
