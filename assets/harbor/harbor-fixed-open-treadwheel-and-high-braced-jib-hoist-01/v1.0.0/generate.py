import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='harbor-fixed-open-treadwheel-and-high-braced-jib-hoist-01'
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

def cell_union(name,cells,mat):
 faces={}
 for v in cells:
  v=[tuple(round(c,12)for c in p)for p in v]
  for f in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:
   q=tuple(v[i]for i in f);key=tuple(sorted(q))
   if key in faces:del faces[key]
   else:faces[key]=q
 v=[];ix={};f=[]
 for q in faces.values():
  ids=[]
  for p in q:
   if p not in ix:ix[p]=len(v);v.append(p)
   ids.append(ix[p])
  f.extend([(ids[0],ids[1],ids[2]),(ids[0],ids[2],ids[3])])
 record(name,v,f,mat)
def turned(name,x,y,profile,m,seg=16):
 v=[];rs=[];f=[]
 for r,z in profile:
  pts=[(x,y,z)]if r==0 else[(x+r*math.cos(math.tau*i/seg),y+r*math.sin(math.tau*i/seg),z)for i in range(seg)]
  rs.append(list(range(len(v),len(v)+len(pts))));v+=pts
 for a,b in zip(rs,rs[1:]+rs[:1]):
  if len(a)==len(b)==1:continue
  for i in range(seg):
   j=(i+1)%seg
   if len(a)==1:f.append((a[0],b[i],b[j]))
   elif len(b)==1:f.append((a[i],b[0],a[j]))
   else:f.extend([(a[i],b[i],b[j]),(a[i],b[j],a[j])])
 record(name,v,f,m)
PALETTE=[('WholeTimberCradleAndMast',(.22,.13,.065,1),.80,.02),('WholeBroadTreadDrumWarmTimber',(.50,.34,.17,1),.75,.01),('WholeAxlesAndHoistFittings',(.26,.34,.33,1),.50,.55),('WholeCordDarkFibre',(.10,.085,.06,1),.92,.01)]
FM={};JOINS=[];ROOTS=[]
def link(a,b,p):JOINS.append((a,b,p))
def beam(name,a,b,w,y,d,m):
 dx,dz=b[0]-a[0],b[1]-a[1];le=math.hypot(dx,dz);nx,nz=-dz/le*w/2,dx/le*w/2
 pad(name,[(a[0]+nx,a[1]+nz),(a[0]-nx,a[1]-nz),(b[0]-nx,b[1]-nz),(b[0]+nx,b[1]+nz)],y-d/2,y+d/2,m)
def axial_y(name,x,z,profile,m,seg=32):
 turned(name,0,0,profile,m,seg);v,f,mi=G[name];record(name,[(x+xx,zz,z+yy)for xx,yy,zz in v],f,mi)
CX=-.60;CZ=1.65
for side,y in [('Front',-.86),('Rear',.86)]:
 foot='Whole'+side+'LongGroundFoot';box(foot,(-2.06,y-.23,0),(.86,y+.23,.16),0);ROOTS.append(foot)
 head='Whole'+side+'AxleBearingHead';box(head,(CX-.19,y-.16,1.49),(CX+.19,y+.16,1.85),2)
 for side2,x in [('Left',-1.88),('Right',.68)]:
  n='Whole'+side+side2+'InclinedCradleLeg';endx=CX+(-.11 if side2=='Left'else .11);beam(n,(x,.105),(endx,1.63),.18,y,.19,0);link(n,foot,(x,y,.13));link(n,head,(endx,y,1.615))
for side,x in [('Left',-1.90),('Right',.70)]:
 n='Whole'+side+'TransverseBaseTie';box(n,(x-.095,-.93,.095),(x+.095,1.17,.25),0)
 for s,y in [('Front',-.86),('Rear',.86)]:link(n,'Whole'+s+'LongGroundFoot',(x,y,.13))
axial_y('WholeContinuousHorizontalAxle',CX,CZ,[(0,-1.12),(.095,-1.12),(.095,1.22),(0,1.22)],2,24)
for side,y in [('Front',-.86),('Rear',.86)]:link('WholeContinuousHorizontalAxle','Whole'+side+'AxleBearingHead',(CX,y,CZ))
# One uninterrupted thick broad annulus is the empty tread drum, not a narrow pulley.
axial_y('WholeBroadOpenTreadDrum',CX,CZ,[(1.16,-.58),(1.30,-.58),(1.30,.58),(1.16,.58)],1,40)
axial_y('WholeRearSpokeHub',CX,CZ,[(0,.31),(.18,.31),(.18,.54),(0,.54)],2,24);link('WholeRearSpokeHub','WholeContinuousHorizontalAxle',(CX,.42,CZ))
for i in range(6):
 a=.17+i*math.tau/6;n='WholeRearRadialSpoke%02d'%i
 beam(n,(CX+.10*math.cos(a),CZ+.10*math.sin(a)),(CX+1.235*math.cos(a),CZ+1.235*math.sin(a)),.11,.43,.14,0)
 link(n,'WholeRearSpokeHub',(CX+.13*math.cos(a),.43,CZ+.13*math.sin(a)));link(n,'WholeBroadOpenTreadDrum',(CX+1.205*math.cos(a),.43,CZ+1.205*math.sin(a)))
axial_y('WholeExteriorDoubleShoulderDrum',CX,CZ,[(0,1.015),(.24,1.015),(.24,1.055),(.18,1.055),(.18,1.17),(.24,1.17),(.24,1.21),(0,1.21)],2,32);link('WholeExteriorDoubleShoulderDrum','WholeContinuousHorizontalAxle',(CX,1.1,CZ))
box('WholeMastLowerSeat',(-1.00,.83,.11),(-.20,1.43,.26),2);link('WholeMastLowerSeat','WholeRearLongGroundFoot',(-.60,.94,.13))
box('WholeFullHeightRearMast',(-.73,.99,.19),(-.47,1.25,3.04),0);link('WholeFullHeightRearMast','WholeMastLowerSeat',(CX,1.12,.22));link('WholeFullHeightRearMast','WholeContinuousHorizontalAxle',(CX,1.16,CZ))
beam('WholeHighJib',(CX,2.90),(2.02,3.04),.18,1.12,.21,0);link('WholeHighJib','WholeFullHeightRearMast',(CX+.03,1.12,2.90))
beam('WholeDiagonalJibBrace',(CX,1.97),(1.98,3.04),.16,1.12,.19,0);link('WholeDiagonalJibBrace','WholeFullHeightRearMast',(CX+.03,1.12,1.982));link('WholeDiagonalJibBrace','WholeHighJib',(1.91,1.12,3.015))
for label,x,z in [('Rear',CX,3.05),('Outer',2.02,3.17)]:
 axle='Whole'+label+'HighPulleyAxle';axial_y(axle,x,z,[(0,.91),(.065,.91),(.065,1.32),(0,1.32)],2,20)
 if label=='Rear':link(axle,'WholeFullHeightRearMast',(x,1.12,3.015))
 else:link(axle,'WholeHighJib',(x-.005,1.12,3.12))
 n='Whole'+label+'HighPulley';axial_y(n,x,z,[(0,1.27),(.155,1.27),(.155,1.34),(0,1.34)],2,32);link(n,axle,(x,1.30,z))
# Continuous external cord: complete rise, broad upper turn, long span, outer turn and empty end eye.
# Its plane is outside the full mast/jib faces, joined through complete pulley axles.
path=[(CX-.175,1.305,CZ),(CX-.175,1.305,3.05)]
for i in range(1,9):
 a=math.pi-(math.pi/2)*i/8;path.append((CX+.151*math.cos(a),1.305,3.05+.151*math.sin(a)))
# The upper route rises parallel to the whole jib; actual visual cord, not solved tangent kinematics.
path.append((2.02,1.305,3.17+.151))
for i in range(1,9):
 a=math.pi/2-(math.pi/2)*i/8;path.append((2.02+.151*math.cos(a),1.305,3.17+.151*math.sin(a)))
path.append((2.171,1.305,.97));pipe('WholeContinuousRoutedHoistCord',path,.017,3,10)
link('WholeContinuousRoutedHoistCord','WholeRearHighPulley',(CX-.106,1.305,3.156));link('WholeContinuousRoutedHoistCord','WholeOuterHighPulley',(2.171,1.305,3.17))
# Real small tab bridges the exterior drum to the cord start without a phantom unsupported rope root.
beam('WholeCordStartRetainingTab',(CX-.15,CZ),(CX-.18,CZ),.06,1.24,.16,2);link('WholeCordStartRetainingTab','WholeExteriorDoubleShoulderDrum',(CX-.16,1.18,CZ));link('WholeCordStartRetainingTab','WholeContinuousRoutedHoistCord',(CX-.175,1.305,CZ+.01))
axial_y('WholeEmptySuspendedEye',2.171,.85,[(.075,1.265),(.14,1.265),(.14,1.345),(.075,1.345)],2,28);link('WholeEmptySuspendedEye','WholeContinuousRoutedHoistCord',(2.171,1.305,.975))
V=[p for v,f,m in G.values()for p in v];SHIFT=((min(p[0]for p in V)+max(p[0]for p in V))/2,(min(p[1]for p in V)+max(p[1]for p in V))/2,min(p[2]for p in V))
for name,(v,f,m)in list(G.items()):G[name]=([sub(p,SHIFT)for p in v],f,m)
JOINS=[(a,b,sub(p,SHIFT))for a,b,p in JOINS]
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
focus=Vector((0,0,1.66))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=6.0;aim(cam,(7,-11,6) if view=='qa-front' else (7,11,7));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/harbor/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'harbor','style':'S01-clean-geometric','title':'Fixed Open Treadwheel and High Braced Jib Hoist','description':'One wholly newly authored complete static treadwheel-hoist-inspired display. A broad deep open annular tread drum has six whole rear radial spokes and a complete horizontal axle carried by two grounded A-shaped timber cradles. A separate full-height rear mast supports one whole high jib and complete diagonal jib brace, two high pulleys on full axles, an external double-shoulder winding drum and one continuous routed cord terminating in a complete empty open eye. The drum interior remains real empty space and the near side has no disc cap; all thick rear spokes and supports remain present. Unlike the small low treadle-wheel and suspended tool stand, this has a wide walk-in-scale drum, high load-cord route and long jib, with no footboard, belt, flexible handpiece or tool. Unlike the ratchet winch, it is not a compact bare spool between cheek plates and has no crank, pawl or sawtooth wheel. All complete numeric drum, support, mast, jib, cord and fitting geometry authored together; no mesh imported or extracted. Four opaque untextured constant PBR materials, native metres Z up and horizontal bounds-centred ground origin; one complete prop zero scenes. Broad historic equipment category only, not any surviving crane building or manufacturer replica. Deliberate small fixed overlaps establish static visual roots rather than a solved mechanism. No working hoist, power transmission, rope winding, tangency, rotation, travel, loading, human use, stability, dimensions for fabrication, installation or equipment safety capability made or verified. No cargo, person, building, rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
