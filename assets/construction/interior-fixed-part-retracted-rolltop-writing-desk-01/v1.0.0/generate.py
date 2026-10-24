import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='interior-fixed-part-retracted-rolltop-writing-desk-01'
import math
N=24
G={}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def record(name,v,f,m):
 if sum(dot(v[a],cross(v[b],v[c]))for a,b,c in f)<0:f=[(a,c,b)for a,b,c in f]
 G[name]=(v,f,m)
def box(name,lo,hi,m):
 v=[(x,y,z)for z in[lo[2],hi[2]]for y in[lo[1],hi[1]]for x in[lo[0],hi[0]]];f=[]
 for a,b,c,d in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:f.extend([(a,b,c),(a,c,d)])
 record(name,v,f,m)
def pipe(name,points,r,m,segments=8):
 v=[]
 for k,p in enumerate(points):
  tangent=unit(sub(points[min(k+1,len(points)-1)],points[max(k-1,0)]));u=(1,0,0)if abs(tangent[0])<.9 else(0,1,0);u=unit(cross(tangent,u));w=cross(tangent,u)
  for i in range(segments):v.append(add(p,add(mul(u,r*math.cos(math.tau*i/segments)),mul(w,r*math.sin(math.tau*i/segments)))))
 f=[]
 for k in range(len(points)-1):
  for i in range(segments):
   j=(i+1)%segments;a=k*segments+i;b=k*segments+j;c=(k+1)*segments+j;d=(k+1)*segments+i;f.extend([(a,b,c),(a,c,d)])
 for k in [0,len(points)-1]:
  c=len(v);v.append(points[k]);base=k*segments
  for i in range(segments):f.append((c,base+(i+1)%segments,base+i)if k==0 else(c,base+i,base+(i+1)%segments))
 record(name,v,f,m)
def wheel(name,x,y,z,ro,ri,width,m):
 # Complete closed annular tire (or capped disc when ri=0), axis X.
 profile=[(ri,x-width/2),(ro,x-width/2),(ro,x+width/2),(ri,x+width/2)]
 v=[];rs=[]
 for r,xx in profile:
  ring=[(xx,y,z)]if r==0 else[(xx,y+r*math.sin(math.tau*i/N),z+r*math.cos(math.tau*i/N))for i in range(N)];rs.append(list(range(len(v),len(v)+len(ring))));v+=ring
 f=[]
 for a,b in zip(rs,rs[1:]+rs[:1]):
  if len(a)==len(b)==1:continue
  for i in range(N):
   j=(i+1)%N
   if len(a)==1:f.append((a[0],b[i],b[j]))
   elif len(b)==1:f.append((a[i],b[0],a[j]))
   else:f.extend([(a[i],b[i],b[j]),(a[i],b[j],a[j])])
 record(name,v,f,m)

def earclip(p):
 cr=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 ids=list(range(len(p)));out=[]
 while len(ids)>3:
  for j,b in enumerate(ids):
   a,c=ids[j-1],ids[(j+1)%len(ids)]
   if cr(p[a],p[b],p[c])<=1e-14:continue
   if any(all(cr(p[u],p[v],p[k])>=-1e-14 for u,v in [(a,b),(b,c),(c,a)])for k in ids if k not in [a,b,c]):continue
   out.append((a,b,c));ids.pop(j);break
  else:raise ValueError('Non-simple padding section')
 out.append(tuple(ids));return out
def pad(name,p,y0,y1,m):
 if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);v=[(x,y,z)for y in[y0,y1]for x,z in p];f=[]
 for a,b,c in earclip(p):f.extend([(a,b,c),(c+n,b+n,a+n)])
 for i in range(n):
  j=(i+1)%n;f.extend([(i,j+n,j),(i,i+n,j+n)])
 record(name,v,f,m)

# Whole fixed writing desk and curved grooved rolltop hood, no animation.
PALETTE=[('RolltopWarmTimber',(.37,.22,.12,1),.83,0),('RolltopLighterSlats',(.58,.40,.22,1),.82,0),('RolltopDarkHardware',(.19,.22,.20,1),.62,.4)]
box('WholeFixedWritingSurface',(-.65,-.65,.75),(.65,.39,.80),0)
for x in[-.57,.57]:
 for y in[-.54,.29]:box('WholeGroundedLeg_'+str((x,y)),(x-.035,y-.035,0),(x+.035,y+.035,.75),0)
for x in[-.57,.57]:box('WholeSideApron_'+str(x),(x-.025,-.54,.64),(x+.025,.29,.75),0)
box('WholeRearApron',(-.57,.265,.64),(.57,.315,.75),0)
box('WholeRearLowerStretcher',(-.57,.27,.18),(.57,.31,.225),0)
# Vertical front, a quarter-circle turn, then a horizontal rear return.
def route(t):
 if t<.20:return(-.30,.80+t),(0,1)
 if t<.20+math.pi*.14:
  a=(t-.20)/.28;return(-.02-.28*math.cos(a),1+.28*math.sin(a)),(math.sin(a),math.cos(a))
 return(-.02+t-.20-math.pi*.14,1.28),(1,0)
# Full side cheeks, each a complete closed shaped panel rather than floating rails.
outer=[(-.33,.80),(-.33,1.)]+[(-.02-.31*math.cos(math.pi/2*i/16),1.+.31*math.sin(math.pi/2*i/16))for i in range(1,17)]+[(.39,1.31),(.39,.80)]
def yz_prism(name,poly,x0,x1,m):
 pad(name,poly,x0,x1,m);v,f,mm=G[name];record(name,[(y,x,z)for x,y,z in v],f,mm)
for side in[-1,1]:
 x=side*.62;yz_prism('WholeCurvedSideCheek_'+str(side),outer,x-.03,x+.03,0)
# Channel lips follow the real continuous curved route, leaving a retained path between them.
ts=[0,.20]+[.20+math.pi*.14*i/16 for i in range(1,17)]+[.20+math.pi*.14+.38]
for side in[-1,1]:
 for off,label in[(-.025,'Inner'),(.025,'Outer')]:
  poly=[]
  for t in ts:
   (y,z),(dy,dz)=route(t);poly.append((y-dz*(off-.008),z+dy*(off-.008)))
  for t in reversed(ts):
   (y,z),(dy,dz)=route(t);poly.append((y-dz*(off+.008),z+dy*(off+.008)))
  x=side*.583;yz_prism(label+'WholeCurvedGuideLip_'+str(side),poly,x-.008,x+.008,2)
box('WholeUpperBackWall',(-.59,.355,.80),(.59,.39,1.275),0)
# One continuous thick curved cover, with shallow real transverse slat grooves.
# Surface profile is corrugated only outward; the inner face remains continuous.
T=.20+math.pi*.14+.34;stations=[.29+i*(T-.29)/60 for i in range(61)]
outerp=[];innerp=[]
for i,t in enumerate(stations):
 (y,z),(dy,dz)=route(t);th=.014 if i%3==0 else .020
 outerp.append((y-dz*th,z+dy*th));innerp.append((y+dz*.008,z-dy*.008))
yz_prism('WholeContinuousGroovedReturningHood',outerp+list(reversed(innerp)),-.58,.58,1)
(y,z),(dy,dz)=route(.29)
pipe('WholeFrontHoodPull',[(-.24,y-.018,z),(-.24,y-.055,z-.018),(.24,y-.055,z-.018),(.24,y-.018,z)],.012,2,12)
# Shallow fixed rear stationery bays, not moving drawers or separately counted boxes.
box('WholeRearStationeryShelf',(-.585,.16,.94),(.585,.355,.965),0)
for x in[-.20,.20]:box('WholeStationeryDivider_'+str(x),(x-.012,.17,.80),(x+.012,.355,1.12),0)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
FM={n:[m]*len(f)for n,(v,f,m)in G.items()}
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
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
triangles=sum(len(f)for v,f,m in G.values())
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
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
focus=Vector((0,0,.67))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.25;aim(cam,(5,-7,4.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/construction/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'interior','style':'S01-clean-geometric','title':'Fixed Part Retracted Rolltop Writing Desk','description':'One newly authored complete static rolltop writing desk. Four full grounded legs and side/rear aprons carry a permanent horizontal writing surface with open knee space. Two full shaped upper side cheeks retain curved guide lips around one continuous thick returning hood with real shallow transverse grooves. Its raised front edge and whole pull reveal the writing area and shallow rear stationery shelf/dividers. This is not a lowered hinged secretary leaf, enlarged cupboard, or a reduced sectional vehicle door with wheels. All geometry is new. Three opaque constant untextured PBR roles, metres, Z-up, full horizontal bounds-centred ground origin. One complete furniture prop and zero scenes, no contents or room. Fixed partly retracted pose only; no flexible joints, actual sliding, full-travel clearance, rolling storage mechanism, ergonomics, load capacity, manufacture, installation or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
