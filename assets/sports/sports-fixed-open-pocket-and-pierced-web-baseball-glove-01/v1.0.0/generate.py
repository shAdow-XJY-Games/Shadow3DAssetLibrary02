import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='sports-fixed-open-pocket-and-pierced-web-baseball-glove-01'
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



# Asymmetric open receiving shell. All radial loops share their full boundary.
P=[(-.055,-.115,.042),(.050,-.115,.042),(.085,-.075,.070),(.111,-.015,.096),(.118,.065,.125),(.108,.110,.146),(.091,.130,.152),(.073,.121,.142),(.067,.153,.164),(.047,.163,.170),(.028,.147,.155),(.015,.170,.174),(-.008,.170,.174),(-.026,.148,.154),(-.044,.150,.150),(-.062,.126,.135),(-.057,.090,.106),(-.071,.063,.081),(-.097,.084,.107),(-.125,.070,.114),(-.142,.037,.104),(-.136,-.006,.090),(-.104,-.052,.065)]
N=len(P);CY=.015;V=[];rr=[]
# Inner pocket centre -> rim -> thick exterior wall -> full flat back sole.
for rad,zmode in [(0,'inner'),(.25,'inner'),(.57,'inner'),(.82,'inner'),(1,'inner'),(1.075,'outer'),(.90,'back'),(.48,'sole'),(0,'sole')]:
 ids=[]
 if rad==0:ids=[len(V)];V.append((0,CY,.025 if zmode=='inner'else 0))
 else:
  for x,y,h in P:
   z=.025+(h-.025)*rad*rad if zmode=='inner'else h-.008 if zmode=='outer'else .018 if zmode=='back'else 0
   ids.append(len(V));V.append((x*rad,CY+(y-CY)*rad,z))
 rr.append(ids)
F=[]
for a,b in zip(rr,rr[1:]):
 for i in range(N):
  j=(i+1)%N
  if len(a)==1:F.append((a[0],b[i],b[j]))
  elif len(b)==1:F.append((a[i],b[0],a[j]))
  else:F.append((a[i],b[i],b[j],a[j]))
mesh('WholeGroundFootAsymmetricOpenPalmAndFingerThumbLobes',V,F,0)
# One full open wrist cuff, horizontal oval opening, entering the lower palm root.
def cuff(name,y0,y1,rx,rz,thick,mat):
 n=24;V=[(r*math.cos(math.tau*i/n),y,.044+z*math.sin(math.tau*i/n))for y,r,z in[(y0,rx,rz),(y1,rx,rz),(y1,rx-thick,rz-thick),(y0,rx-thick,rz-thick)]for i in range(n)];F=[]
 for k in range(4):
  for i in range(n):j=(i+1)%n;F.append((k*n+i,k*n+j,((k+1)%4)*n+j,((k+1)%4)*n+i))
 mesh(name,V,F,mat)
cuff('WholeOpenOvalWristCuff',-.152,-.085,.062,.038,.009,0)
cuff('WholeWristBindingRetainingOpenAperture',-.150,-.137,.064,.040,.003,2)
# Connected finite thick web with four true apertures, not crossing disconnected rods.
xs=[0,.009,.045,.054,.090,.100];ys=[0,.009,.039,.048,.081,.090];faces={}
O=(-.125,.060,.105);U=(.81,.90,.45);W=(.05,-.70,-.30)
for i in range(5):
 for j in range(5):
  if i%2 and j%2:continue
  vv=[(x,y,z)for z in[-.003,.003]for y in[ys[j],ys[j+1]]for x in[xs[i],xs[i+1]]]
  for f in BOX:
   q=tuple(vv[k]for k in f);key=tuple(sorted(q))
   if key in faces:del faces[key]
   else:faces[key]=q
v=[];ix={};f=[]
normal=unit(cross(U,W))
for q in faces.values():
 ids=[]
 for p in q:
  if p not in ix:ix[p]=len(v);v.append(tuple(O[k]+p[0]*U[k]+p[1]*W[k]+p[2]*normal[k]for k in range(3)))
  ids.append(ix[p])
 f.append(tuple(ids))
mesh('WholePiercedThumbToFingerWeb',v,f,1)
# Rounded welt follows the real upper rim; fixed leather seam appearance.
for i in [3,6,9,12,15,19]:
 x,y,z=P[i];axle('WholeEdgeLaceRivet_'+str(i),x-.003,x+.003,y,z,.0035,2,8)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholePalmAndCuff_OchreLeather',(.43,.22,.085,1),.86,0),('WholePiercedWeb_DeepBrown',(.16,.070,.025,1),.90,0),('WholeBindings_WarmTan',(.61,.36,.14,1),.88,0)]
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
focus=Vector((0,0,.07))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.43;aim(cam,(2,-4,5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/sports/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'sports','style':'S01-clean-geometric','title':'Fixed Open Pocket and Pierced Web Baseball Glove','description':'One newly authored complete static baseball-style receiving glove appearance. An asymmetric thick open concave palm rises into a broad rounded finger side and opposed shorter thumb lobe, with a complete genuinely pierced grid web joining their upper edges. A full separate open annular wrist cuff and its binding join the lower palm root. The palm has an actual recessed receiving bowl rather than a black decal; the thin web has through apertures rather than alpha texture. This is not the old closed padded boxing fist or five-finger plate gauntlet recoloured: no geometry is reused. Fixed display lying on a finite back patch, not an actual hand or wearable finger-channel model. Three opaque untextured PBR roles, metres, Z up and horizontal envelope-centred ground origin. One glove, no ball or partner glove, zero scenes. No catch performance, articulated fit, grip, padding response, fastening, protective capability, sport compliance, manufacture or safe-use claim. Rigging, animation and interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
