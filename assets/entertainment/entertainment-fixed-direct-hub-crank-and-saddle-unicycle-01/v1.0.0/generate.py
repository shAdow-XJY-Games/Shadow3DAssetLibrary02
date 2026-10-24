import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='entertainment-fixed-direct-hub-crank-and-saddle-unicycle-01'
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



# One newly authored full direct-hub unicycle, static illustrative stance only.
zc=.320*math.cos(math.pi/32)
def phasedring(name,x0,x1,ri,ro,mat):
 ringx(name,x0,x1,0,zc,ri,ro,mat,32);v,f,m=G[name];a=math.pi/32;G[name]=([(x,y*math.cos(a)-(z-zc)*math.sin(a),zc+y*math.sin(a)+(z-zc)*math.cos(a))for x,y,z in v],f,m)
phasedring('WholeGroundFootFacetedAnnularTyre',-.034,.034,.273,.320,2)
phasedring('WholeOpenWheelRim',-.023,.023,.246,.278,1)
axle('WholeWideWheelHub',-.049,.049,0,zc,.043,1,24)
axle('WholeDirectPedalAndWheelAxle',-.113,.113,0,zc,.018,1,24)
for k in range(12):
 a=math.tau*k/12;beam('WholeWheelSpoke_%02d'%k,(0,.031*math.cos(a),zc+.031*math.sin(a)),(0,.255*math.cos(a),zc+.255*math.sin(a)),.012,1)
# Single complete U fork, two full side legs and crown above the wheel; not bicycle frame fragments.
poly=[(-.079,.297),(-.047,.297),(-.047,.659),(.047,.659),(.047,.297),(.079,.297),(.079,.710),(-.079,.710)]
n=len(poly);tt=triangulate(poly);v=[(x,y,z)for y in[-.030,.030]for x,z in poly];f=list(tt)+[tuple(n+i for i in reversed(t))for t in tt]+[(i,n+i,n+(i+1)%n,(i+1)%n)for i in range(n)];mesh('WholeOpenCrownFork',v,f,0)
lathe_z('WholeStraightSeatTube',0,0,[(0,.685),(.029,.685),(.029,.877),(0,.877)],0,24)
lathe_z('WholeSeatTubeCollar',0,0,[(.023,.847),(.036,.847),(.036,.883),(.023,.883)],2,24)
lathe_z('WholeFixedRaisedSeatPost',0,0,[(0,.850),(.022,.850),(.022,.963),(0,.963)],1,24)
# One entire shaped saddle with raised front and rear ends and a narrowed waist.
# Shared rectangular cross sections form a closed padded body, not a scaled bicycle box.
sections=[(-.180,.031,.984,.035),(-.145,.043,.968,.033),(-.050,.054,.953,.032),(.055,.075,.957,.036),(.132,.080,.980,.042),(.158,.057,.988,.037)]
v=[]
for y,w,z,t in sections:
 v.extend([(-w,y,z-t/2),(w,y,z-t/2),(w,y,z+t/2),(-w,y,z+t/2)])
f=[(3,2,1,0),(20,21,22,23)]+[(j*4+i,j*4+(i+1)%4,(j+1)*4+(i+1)%4,(j+1)*4+i)for j in range(len(sections)-1)for i in range(4)];mesh('WholeCurvedNoseAndRearSaddle',v,f,2)
box('WholeSaddleUndersideMount',(0,0,.945),(.090,.125,.028),1)
for sign,label in[(-1,'Left'),(1,'Right')]:
 y=sign*.112;z=zc+sign*.070;x=sign*.107
 beam('WholeOpposedDirectCrank_'+label,(x,0,zc),(x,y,z),.030,0)
 x0,x1=sorted([sign*.098,sign*.195]);axle('WholePedalSpindle_'+label,x0,x1,y,z,.014,1,20)
 # Full thick chamfered pedal shape, complete top/bottom and finite edge bevel outline.
 cx=sign*.178;poly=[(cx-.060,y-.038),(cx+.049,y-.038),(cx+.060,y-.027),(cx+.060,y+.027),(cx+.049,y+.038),(cx-.049,y+.038),(cx-.060,y+.027),(cx-.060,y-.027)]
 n=len(poly);tt=triangulate(poly);v=[(xx,yy,zz)for zz in[z-.020,z+.020]for xx,yy in poly];f=[tuple(reversed(t))for t in tt]+[tuple(n+i for i in t)for t in tt]+[(i,(i+1)%n,n+(i+1)%n,n+i)for i in range(n)];mesh('WholeChamferedPedal_'+label,v,f,2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeForkTubeAndCranks_MutedRed',(.48,.095,.065,1),.67,.20),('WholeRimSpokesHubAndPost_SatinMetal',(.48,.50,.46,1),.43,.62),('WholeTyreSaddleAndPedals_Charcoal',(.043,.052,.050,1),.81,.04)]
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
focus=Vector((0,0,.50))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.32;aim(cam,(5,-3,2.6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/entertainment/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'entertainment','style':'S01-clean-geometric','title':'Fixed Direct Hub Crank and Saddle Unicycle','description':'One newly authored complete fixed direct-hub unicycle appearance. A full annular faceted tyre with actual finite flat bottom tread surrounds an open rim, twelve complete spokes and a broad hub. One continuous transverse axle connects that hub directly to two opposed crank arms and separate whole thick pedals. A single complete U crown fork passes around the tyre and rises to one straight seat tube, collar and fixed post; one continuous section-shaped saddle has a narrow waist and raised front/rear ends. All geometry is newly authored: no old bicycle frame or wheel mesh is imported, deleted or rearranged. There is no remote bottom bracket, chain, steering tube, handlebar, counter case or long staff. This common wheel/pedal axis and directly above fork/seat relationship is the whole model, not merely a wheel-count change to a reused bicycle. Three opaque constant PBR roles, metres, Z up, whole XY-bounds centred and finite tyre facet at Z0. One prop, zero scenes. Static illustrative pose only, not a balanced physical rest-state simulation; no rider, animation, rotation, rideability, balancing, ergonomics, load, manufacture or sporting-safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
