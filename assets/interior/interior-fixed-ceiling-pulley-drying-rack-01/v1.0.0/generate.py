import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='interior-fixed-ceiling-pulley-drying-rack-01'
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

# Whole isolated ceiling-mounted drying apparatus in one fixed lowered pose.
PALETTE=[('SuspendedTimberDryingRods',(.48,.32,.18,1),.8,0),('PulleyBracketsAndCrossheads',(.20,.29,.29,1),.58,.40),('ContinuousLiftCords',(.69,.66,.53,1),.9,0)]
for i,y in enumerate([-.28,-.14,0,.14,.28]):pipe('WholeLongDryingRod_'+str(i),[(-.98,y,.62),(.86,y,.62)],.017,0,12)
for i,x in enumerate([-.82,.62]):
 box('WholeEndCrosshead_'+str(i),(x-.035,-.325,.58),(x+.035,.325,.62),1)
 yy=0 if i==0 else .14
 pipe('WholeTwoLegSuspensionBridle_'+str(i),[(x,-.29,.605),(x,yy,.90),(x,.29,.605)],.012,1,12)
# Grooved complete sheaves, axis Y; 2 nearby sheaves route both cords independently.
def sheave(name,x,y,z):
 profile=[(.012,-.027),(.098,-.027),(.112,-.019),(.112,-.011),(.095,-.005),(.095,.005),(.112,.011),(.112,.019),(.098,.027),(.012,.027)]
 nn=24;v=[(x+r*math.cos(i*math.tau/nn),y+t,z+r*math.sin(i*math.tau/nn))for r,t in profile for i in range(nn)];f=[]
 for k in range(len(profile)):
  kk=(k+1)%len(profile)
  for i in range(nn):j=(i+1)%nn;f.extend([(k*nn+i,k*nn+j,kk*nn+j),(k*nn+i,kk*nn+j,kk*nn+i)])
 record(name,v,f,1)
for i,(x,y) in enumerate([(-.72,0),(.72,0),(.72,.14)]):
 sheave('WholeGroovedCeilingSheave_'+str(i),x,y,1.72)
 pipe('WholeSheaveAxle_'+str(i),[(x,y-.05,1.72),(x,y+.05,1.72)],.012,1,12)
 for side in[-1,1]:box('WholeHangerCheek_'+str((i,side)),(x-.035,y+side*.04-.008,1.70),(x+.035,y+side*.04+.008,1.90),1)
# One remote single mounting plate, one near double mounting plate; exposed host interfaces intentionally retained.
box('WholeSingleCeilingMountPlate',(-.84,-.075,1.895),(-.60,.075,1.93),1)
box('WholeDoubleCeilingMountPlate',(.60,-.075,1.895),(.84,.215,1.93),1)
# Tangent rope paths rest in groove radius .095 with 5mm rope radius; both full paths continuous.
p=[(-.82,0,.895),(-.82,0,1.72)]+[(-.72+.10*math.cos(a),0,1.72+.10*math.sin(a))for a in[math.pi-j*math.pi/16 for j in range(1,9)]]
p +=[(.72,0,1.82)]+[(.72+.10*math.cos(a),0,1.72+.10*math.sin(a))for a in[math.pi/2-j*math.pi/16 for j in range(1,9)]]+[(.82,0,.30),(.845,.055,.29)]
pipe('WholeFarLiftCordOverBothPulleys',p,.005,2,8)
p=[(.62,.14,.895),(.62,.14,1.72)]+[(.72+.10*math.cos(a),.14,1.72+.10*math.sin(a))for a in[math.pi-j*math.pi/16 for j in range(1,17)]]+[(.82,.14,.30),(.845,.085,.29)]
pipe('WholeNearLiftCordOverOwnPulley',p,.005,2,8)
box('WholeWallCleatMountPlate',(.89,-.035,.12),(.925,.175,.47),1)
pipe('WholeCleatStandoff',[(.90,.07,.29),(.845,.07,.29)],.019,1,12)
pipe('WholeDoubleHornTieCleat',[(.845,-.025,.38),(.845,.07,.29),(.845,.165,.20)],.018,1,12)
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
focus=Vector((0,0,.90))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.9;aim(cam,(4,-7,3.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/interior/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'interior','style':'S01-clean-geometric','title':'Fixed Ceiling Pulley Drying Rack','description':'One newly authored complete static ceiling pulley drying-rack apparatus in a lowered fixed pose. Five full long timber rods cross two complete end crossheads; two real two-leg bridles lead to independent continuous lift cords. One remote single grooved sheave and two near grooved sheaves with complete axles, cheek hangers and exposed ceiling mounting plates route the far and near cords down to one whole two-horn wall cleat and plate. No X floor stands, raised wings, winch drum, cargo hook or old model instances. This is one isolated installation fixture kit with no host wall or ceiling included; the mounting plates are intentional exposed attachment interfaces, not ground feet. All geometry new, three opaque constant PBR materials, metres, Z up and horizontal bounds centred; lowest mount edge is datum zero only. One prop and zero scenes, no clothes. Static appearance only: no lifting, rope tension, usable travel, knot security, drying rate, installation suitability, load, accessibility or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
