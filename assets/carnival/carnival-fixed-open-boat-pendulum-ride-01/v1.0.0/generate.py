import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='carnival-fixed-open-boat-pendulum-ride-01'
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



# Original full boat pendulum exterior; no old swing seat or wheel geometry.
for side,y in [('Front',-.86),('Back',.86)]:
 for end,x in [('Left',-1.02),('Right',1.02)]:
  box(side+end+'WholeGroundShoe',(x,y,.055),(.36,.34,.11),0)
  beam(side+end+'WholeAFrameLeg',(x,y,.09),(0,y,2.24),.15,0)
 box(side+'WholeLowFrameTie',(0,y,.20),(2.12,.13,.14),0)
 ringy(side+'WholeBoredUpperBearing',y-.10,y+.10,0,2.24,.08,.19,2,32)
for end,x in [('Left',-1.02),('Right',1.02)]:box(end+'WholeGroundCrossTie',(x,0,.13),(.13,1.82,.12),0)
cyly('WholeContinuousUpperAxle',-1.00,1.00,0,2.24,.08,2,32)
for side,y in [('Front',-1.02),('Back',1.02)]:cyly(side+'WholeAxleCap',y-.035,y+.035,0,2.24,.115,2,24)
# Long rising bow/stern open U-shell with a real thick bottom, independent of its supports.
stations=[(-1.25,.09,.86,1.17),(-.90,.34,.53,.97),(-.45,.49,.38,.82),(.45,.49,.38,.82),(.90,.34,.53,.97),(1.25,.09,.86,1.17)]
vs=[];profiles=[]
for x,w,b,t in stations:
 p=[(-w,b),(w,b),(w,t),(w-.055,t),(w-.055,b+.055),(-w+.055,b+.055),(-w+.055,t),(-w,t)];profiles.append(p);vs.extend((x,y,z)for y,z in p)
f=[]
for a,b,c in triangulate(profiles[0]):f.append((c,b,a))
k=8*(len(stations)-1)
for a,b,c in triangulate(profiles[-1]):f.append((k+a,k+b,k+c))
for j in range(len(stations)-1):
 for i in range(8):n=(i+1)%8;f.append((j*8+i,j*8+n,(j+1)*8+n,(j+1)*8+i))
mesh('WholeRisingBowAndSternThickBoatShell',vs,f,1)
for side,x in [('Bow',-1.24),('Stern',1.24)]:box(side+'WholeEndClosure',(x,0,1.015),(.075,.175,.31),1)
# Four finite transverse benches, not separate model instances.
def hullwidth(x):
 for a,b in zip(stations,stations[1:]):
  if a[0]<=x<=b[0]:return a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0])
 raise AssertionError(x)
for i,(x,z)in enumerate([(-.66,.71),(-.23,.64),(.23,.64),(.66,.71)],1):
 x0=x-.10;x1=x+.10;w0=hullwidth(x0)-.02;w1=hullwidth(x1)-.02
 p=[(x0,-w0),(x1,-w1),(x1,w1),(x0,w0)];v=[(xx,yy,zz)for zz in[z-.0375,z+.0375]for xx,yy in p]
 mesh('WholeTransverseBench_'+str(i),v,[(3,2,1,0),(4,5,6,7)]+[(j,(j+1)%4,(j+1)%4+4,j+4)for j in range(4)],2)
# Each whole rigid side bridle joins the upper axle to two real cross-boat bearings.
for side,y in [('Front',-.46),('Back',.46)]:
 ringy(side+'WholePendulumHub',y-.07,y+.07,0,2.24,.08,.17,1,24)
 for end,x in [('Bow',-.90),('Stern',.90)]:beam(side+end+'WholeRigidSuspensionArm',(0,y,2.24),(x,y,.91),.075,1)
for end,x in [('Bow',-.90),('Stern',.90)]:cyly(end+'WholeThroughBoatSuspensionCrossmember',-.51,.51,x,.91,.046,2,24)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeGroundedFrame_MutedTeal',(.07,.25,.27,1),.72,.15),('WholeBoatAndPendulum_Russet',(.61,.19,.08,1),.74,.06),('WholeBenchesAndAxles_WarmIvory',(.71,.65,.46,1),.65,.20)]
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
focus=Vector((0,0,1.16))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.32;aim(cam,(4,-6,3.6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/carnival/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'carnival','style':'S01-clean-geometric','title':'Fixed Open Boat Pendulum Ride','description':'One newly authored complete static boat-shaped pendulum ride exterior. Four broad grounded shoes, two outside A-frames and low cross ties carry two truly bored top bearings and one continuous horizontal axle. Two rigid side suspension bridles connect that axle to complete bow and stern crossmembers on a newly shaped long open boat shell. The shell has rising narrow ends, a broad lower middle, full thick bottom and walls, separate closed end bulkheads and four transverse benches. All whole numerical shapes are new; no existing swing seat, boat asset, carousel horse or Ferris-wheel rim/cabin is imported, extracted, recoloured or counted again. It has one suspended boat rather than a wheel and multiple level cabins, or a rope-hung narrow plank. Three opaque constant untextured PBR materials. Metres, native Z up, horizontal bounds-centred ground datum. One complete prop, zero scenes. Fixed display only: no rotation or swing envelope, drive, latch, brake, restraint, passenger fit, load capacity, assembly instructions, stability or amusement-ride safety claim; no people, surrounding fairground, animation or operational mechanism.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
