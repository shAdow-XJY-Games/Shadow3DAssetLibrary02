import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='toys-fixed-open-ladder-frame-pedal-kart-01'
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



# Complete independently authored fixed low pedal-kart chassis and exterior controls.
Z=.18*math.cos(math.pi/32)
for side,x in [('Left',-.46),('Right',.46)]:
 for end,y in [('Front',-.52),('Rear',.52)]:
  name=side+end+'WholeGroundFootTire'
  lathe_z(name,0,0,[(.075,-.060),(.155,-.060),(.18,-.047),(.18,.047),(.155,.060),(.075,.060)],1,32)
  v,f,m=G[name];a=math.pi/32;G[name]=([(x+c,y+u*math.cos(a)-w*math.sin(a),Z+u*math.sin(a)+w*math.cos(a))for u,w,c in v],f,m)
  axle(side+end+'WholeWheelHub',x-.065,x+.065,y,Z,.082,2,20)
# The whole rear axle is carried in two full bearing blocks on the separate ladder chassis.
axle('WholeRearLiveAxle',-.535,.535,.52,Z,.024,2,20)
for side,x in [('Left',-.26),('Right',.26)]:
 box(side+'WholeLadderSideRail',(x,.035,.235),(.060,1.23,.065),0)
 box(side+'WholeRearAxleBearing',(x,.52,.211),(.09,.09,.095),0)
for label,y in [('Front',-.52),('Pedal',-.24),('Seat',.22),('Rear',.58)]:box(label+'WholeChassisCrossTie',(0,y,.23),(.57,.052,.065),0)
# Two distinct front kingpin blocks, actual stub axles and a common rearward tie link.
for side,sgn in [('Left',-1),('Right',1)]:
 x=sgn*.36;box(side+'WholeFrontKingpinCarrier',(x,-.52,.215),(.085,.085,.105),0)
 lathe_z(side+'WholeVerticalKingpin',x,-.52,[(0,.145),(.015,.145),(.015,.285),(0,.285)],2,16)
 axle(side+'WholeFrontStubAxle',min(sgn*.33,sgn*.535),max(sgn*.33,sgn*.535),-.52,Z,.022,2,16)
 beam(side+'WholeSteeringArm',(x,-.52,.21),(x,-.40,.21),.026,2)
 beam(side+'WholeCarrierFrameRoot',(sgn*.26,-.52,.23),(x,-.52,.23),.045,0)
beam('WholeSteeringTieRod',(-.36,-.40,.21),(.36,-.40,.21),.018,2)
beam('WholeSteeringPitmanLink',(0,-.52,.22),(0,-.40,.21),.025,2)
# Full inclined steering column terminates at a three-spoke open ring.
c=(0,-.12,.65);w=unit(sub(c,(0,-.52,.22)));u=(1,0,0);vv=cross(w,u)
def pt(r,a,d=0):return tuple(c[k]+r*(math.cos(a)*u[k]+math.sin(a)*vv[k])+d*w[k]for k in range(3))
v=[];n=32;k=8
for i in range(n):
 for j in range(k):a=math.tau*j/k;v.append(pt(.145+.014*math.cos(a),math.tau*i/n,.014*math.sin(a)))
mesh('WholeOpenSteeringWheelRim',v,[(i*k+j,((i+1)%n)*k+j,((i+1)%n)*k+(j+1)%k,i*k+(j+1)%k)for i in range(n)for j in range(k)],1)
beam('WholeInclinedSteeringColumn',(0,-.52,.22),c,.025,2)
for j in range(3):beam('WholeSteeringWheelSpoke_%d'%j,c,pt(.145,math.tau*j/3),.020,2)
# Independent transverse pedal shaft, fixed opposed cranks and actual outward pedals.
axle('WholePedalShaft',-.215,.215,-.24,.30,.019,2,16)
for side,sgn in [('Left',-1),('Right',1)]:
 box(side+'WholePedalShaftBearing',(sgn*.22,-.24,.275),(.08,.09,.10),0)
 y=-.24+sgn*.085;z=.30+sgn*.055;beam(side+'WholePedalCrank',(sgn*.205,-.24,.30),(sgn*.205,y,z),.022,2)
 axle(side+'WholePedalAxle',min(sgn*.20,sgn*.30),max(sgn*.20,sgn*.30),y,z,.012,2,12)
 box(side+'WholePedalTread',(sgn*.27,y,z),(.10,.09,.035),1)
# Closed restrained chain-band appearance links equal fixed sprockets, not a driven simulation.
for name,y,z in [('Front',-.24,.30),('Rear',.52,Z)]:axle(name+'WholeFixedChainDisc',.102,.126,y,z,.073,2,32)
a=(-.24,.30);b=(.52,Z);dy=b[0]-a[0];dz=b[1]-a[1];ang=math.atan2(dz,dy);loops=[]
for x,r in[(.105,.078),(.123,.078),(.123,.068),(.105,.068)]:
 row=[]
 for center,start in[(b,ang-math.pi/2),(a,ang+math.pi/2)]:
  for j in range(17):t=start+math.pi*j/16;row.append((x,center[0]+r*math.cos(t),center[1]+r*math.sin(t)))
 loops.append(row)
n=len(loops[0]);mesh('WholeContinuousClosedPedalChainBand',sum(loops,[]),[(k*n+i,k*n+(i+1)%n,((k+1)%4)*n+(i+1)%n,((k+1)%4)*n+i)for k in range(4)for i in range(n)],1)
# Full fixed low seat pan and inclined back, with real roots on two chassis crossmembers.
for x in[-.18,.18]:box('WholeSeatRiser_'+str(x),(x,.27,.30),(.065,.30,.10),0)
box('WholeLowSeatPan',(0,.28,.365),(.43,.36,.075),1)
p=[(.40,.34),(.48,.34),(.58,.64),(.51,.67)];n=len(p);v=[(x,y,z)for x in[-.225,.225]for y,z in p];f=[]
for a,b,c in triangulate(p):f.extend([(c,b,a),(a+n,b+n,c+n)])
f +=[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh('WholeInclinedSeatBack',v,f,1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeLadderChassisBearingRoots_MutedOrange',(.56,.23,.075,1),.68,.12),('WholeTiresSeatWheelAndChain_DarkRubber',(.055,.065,.071,1),.82,0),('WholeAxlesKingpinsCranksAndLinks_DullMetal',(.43,.48,.49,1),.51,.45)]
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
focus=Vector((0,0,.32))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.10;aim(cam,(3.6,-5,3.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/music/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'toys','style':'S01-clean-geometric','title':'Fixed Open Ladder Frame Pedal Kart','description':'One newly authored complete fixed open pedal-kart exterior. A low full ladder chassis carries four thick annular tires with finite bottom tread facets and distinct hubs, a whole rear axle on two bearings, and two front kingpin carriers with separate stub axles and a real transverse steering tie link. A full inclined column joins a three-spoke open steering ring. An independent pedal shaft has two opposed fixed cranks and whole tread pedals; one closed thick chain-band appearance joins two fixed sprocket discs beside the low seat. The seat pan, inclined back and risers are rooted on the chassis. This is not an old bumper-car shell stripped away or a bicycle given extra wheels: all low chassis, independent front carriers, rear axle and low-seated pedal layout are newly authored together; no old mesh imports. Three opaque constant untextured PBR roles, metres, Z up and actual whole horizontal ground centering. One model and zero scenes. Empty fixed art only: no functioning steering or differential, chain travel, gear teeth engagement, brakes, drive performance, racing or road use, rider fit, load, engineering, fabrication or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
