import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='firefighting-static-raised-ladder-truck-01'
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
# New complete fixed raised ladder vehicle; no original asset mesh imported.
def prismx(name,p,x0,x1,m):
 pad(name,p,x0,x1,m)
 v,f,mi=G[name];G[name]=([(y,x,z)for x,y,z in v],[(a,c,b)for a,b,c in f],mi)
def beam(name,a,b,w,h,m):
 d=unit(sub(b,a));u=(1,0,0);v=cross(d,u);verts=[add(p,add(mul(u,s*w/2),mul(v,t*h/2)))for p in[a,b]for t in[-1,1]for s in[-1,1]]
 fs=[]
 for a,b,c,d in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:fs.extend([(a,b,c),(a,c,d)])
 record(name,verts,fs,m)
for x in[-.56,.56]:box('ChassisRail'+str(x),(x-.09,-2.35,.53),(x+.09,2.65,.72),2)
for i,y in enumerate([-1.74,.85,1.97]):
 pipe('FixedAxle'+str(i),[(-1.02,y,.42),(1.02,y,.42)],.065,2,12)
 for s in[-1,1]:
  wheel('RoadTire%d_%d'%(i,s),s*.88,y,.42,.42,0,.28,2)
  wheel('ClosedHub%d_%d'%(i,s),s*1.027,y,.42,.20,0,.022,3)
for x in[-.56,.56]:
 box('CabMount'+str(x),(x-.09,-1.9,.67),(x+.09,-1.0,.90),2)
 for y in[.3,2.3]:box('DeckMount'+str(x)+str(y),(x-.09,y-.12,.68),(x+.09,y+.12,.88),2)
box('RearCompartmentBody',(-.92,-.74,.86),(.92,2.62,1.35),0)
box('RearDeck',(-.97,-.77,1.35),(.97,2.68,1.43),3)
prismx('NewCabExterior',[(-2.43,.88),(-.80,.88),(-.80,2.08),(-2.03,2.08),(-2.43,1.60)],-.91,.91,0)
for s in[-1,1]:
 prismx('CabOpaqueSideWindow'+str(s),[(-2.28,1.61),(-1.98,1.97),(-.97,1.97),(-.97,1.40),(-2.28,1.40)],s*.912-.012,s*.912+.012,4)
 box('CabDoorHandle'+str(s),(s*.938-.016,-1.22,1.24),(s*.938+.016,-1.00,1.28),3)
 for i,(a,b)in enumerate([(-.64,.30),(.39,1.32),(1.41,2.51)]):
  box('SideShutter%d_%d'%(s,i),(s*.932-.016,a,.94),(s*.932+.016,b,1.27),3)
  for j in range(3):box('ShutterGroove%d_%d_%d'%(s,i,j),(s*.952-.008,a+.03,1.00+j*.075),(s*.952+.008,b-.03,1.011+j*.075),2)
# Two thick opaque windscreen plates lie on the actual sloping cab face.
for s in[-1,1]:
 xa,xb=sorted([s*.045,s*.77]);z0,z1=1.66,1.98
 p=[(xa,-2.43+(z0-1.6)*.4/.48,z0),(xb,-2.43+(z0-1.6)*.4/.48,z0),(xb,-2.43+(z1-1.6)*.4/.48,z1),(xa,-2.43+(z1-1.6)*.4/.48,z1)]
 n=unit((0,-.48,.4));vv=[add(q,mul(n,t))for t in[.002,.018]for q in p];ff=[]
 for a,b,c,d in[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:ff.extend([(a,b,c),(a,c,d)])
 record('OpaqueWindshield'+str(s),vv,ff,4)
box('FrontBumper',(-1.01,-2.51,.77),(1.01,-2.40,.93),3)
box('FrontDarkGrille',(-.42,-2.447,1.04),(.42,-2.432,1.30),2)
for s in[-1,1]:
 box('FrontHeadlight'+str(s),(s*.68-.17,-2.451,1.10),(s*.68+.17,-2.434,1.29),5)
 box('RoofBeacon'+str(s),(s*.62-.17,-1.63,2.08),(s*.62+.17,-1.38,2.21),5)
# Fixed deployed outriggers, separate from the road wheels.
for j,y in enumerate([-.32,2.32]):
 for s in[-1,1]:
  box('OutriggerBeam%d_%d'%(j,s),(min(s*.55,s*1.35),y-.09,.72),(max(s*.55,s*1.35),y+.09,.86),3)
  box('OutriggerStem%d_%d'%(j,s),(s*1.30-.055,y-.055,.07),(s*1.30+.055,y+.055,.79),3)
  box('OutriggerGroundPad%d_%d'%(j,s),(s*1.30-.17,y-.16,0),(s*1.30+.17,y+.16,.08),2)
pipe('FixedTurntable',[(0,1.25,1.41),(0,1.25,1.60)],.48,2,24)
for s in[-1,1]:box('LadderPivotCheek'+str(s),(s*.38-.075,1.04,1.57),(s*.38+.075,1.46,1.89),0)
pipe('CrossPivotPin',[(-.52,1.25,1.77),(.52,1.25,1.77)],.09,3,16)
P=(0,1.25,1.77);D=unit((0,-.84,.54));UP=(0,D[2],-D[1])
def lp(t,x=0,n=0):return add(add(add(P,mul(D,t)),(x,0,0)),mul(UP,n))
for label,t0,t1,width,off in [('Outer',0,3.7,.74,0),('Inner',2.4,5.35,.49,.15)]:
 for s in[-1,1]:beam(label+'ContinuousRail'+str(s),lp(t0,s*width/2,off),lp(t1,s*width/2,off),.075,.14,3)
 for j in range(int((t1-t0)/.31)+1):
  t=t0+.10+j*.31
  if t>t1-.05:continue
  pipe(label+'Rung'+str(j),[lp(t,-width/2,off),lp(t,width/2,off)],.033,3,8)
pipe('StaticElevationCylinder',[(0,.18,1.40),(0,.20,2.08)],.10,2,12)
pipe('StaticElevationRod',[(0,.20,1.98),lp(1.28,0,-.04)],.045,3,12)

G={n:(v,f,m-1 if m>0 else m)for n,(v,f,m)in G.items()}

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
for name,color,rough in [('FireRed',(.65,.028,.018,1),.54),('RubberGraphite',(.025,.03,.034,1),.8),('Frame_Silver',(.52,.56,.58,1),.36),('OpaqueNavyPane',(.035,.09,.13,1),.33),('LampIvory',(.93,.75,.34,1),.45)]:
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=.6 if name in ['Frame_Silver','Rims_Satin'] else 0;materials.append(m)
parts=[]
for name,(v,f,mi) in G.items():
 me=bpy.data.meshes.new(name+'Mesh');me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o)
 for m in materials:me.materials.append(m)
 for p in me.polygons:p.material_index=mi;p.use_smooth=False
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
focus=Vector((0,-.3,2.30))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-5,-7,10),1800,6),('Fill',(7,-3,7),1100,6),('Rim',(4,7,9),1500,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=7.3;aim(cam,(8,-10,6.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/firefighting/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'firefighting','style':'S01-clean-geometric','title':'Static Raised-Ladder Fire Truck','description':'Original complete static raised-ladder fire vehicle appearance: a new short cab and shuttered equipment body on a three-axle chassis, four deployed ground-pad outriggers, fixed rear turntable and twin nested open rung ladders on a cross pivot. All geometry is newly constructed, no old vehicle or ladder is imported. Opaque window and lamp surfaces. Fixed visual pose only, not a working vehicle: no driving, steering, rescue, telescoping, rotation, hydraulic operation, human fit, load capacity, stability or safety performance is claimed.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':5,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
