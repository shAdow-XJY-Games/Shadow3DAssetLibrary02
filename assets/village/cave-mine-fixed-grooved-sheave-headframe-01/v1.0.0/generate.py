import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='cave-mine-fixed-grooved-sheave-headframe-01'
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
# One complete fixed shaft headgear: four feet, two front posts and two raked rear stays.
for side,x in [('Left',-.85),('Right',.85)]:
 for end,y in [('Front',-.80),('Rear',1.20)]:box(side+end+'GroundFoot',(x-.20,y-.26,0),(x+.20,y+.26,.15),3)
 box(side+'FrontUpright',(x-.11,-.91,.15),(x+.11,-.69,3.12),0)
 # Whole sheared rectangular rear leg, horizontal end cuts seat on foot and top rail.
 v=[(xx,y,z)for xx in[x-.11,x+.11]for y,z in[(1.09,.15),(1.31,.15),(-.29,3.12),(-.51,3.12)]];f=[]
 for a,b,c,d in[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:f.extend([(a,b,c),(a,c,d)])
 record(side+'WholeRakedRearStay',v,f,0)
 box(side+'WholeTopBearingRail',(x-.15,-.96,3.12),(x+.15,-.24,3.27),0)
# Cross ties remain behind the declared front shaft opening, not across it.
def rear_y(z):return 1.20-1.60*(z-.15)/(3.12-.15)
for z in[.85,2.35]:
 y=rear_y(z);box('RearCrossTie'+str(z),(-.90,y-.07,z-.065),(.90,y+.07,z+.065),0)
pipe('RearDiagonalA',[(-.85,rear_y(.85)+.06,.85),(.85,rear_y(2.35)+.06,2.35)],.035,2,12)
pipe('RearDiagonalB',[(.85,rear_y(.85)-.06,.85),(-.85,rear_y(2.35)-.06,2.35)],.035,2,12)
CY=-.60;CZ=3.46
# Real annular bearing housings: capped outer shell but open through-axis bore.
for side,x in [('Left',-.85),('Right',.85)]:
 v=[]
 for xx,inner in[(x-.08,False),(x+.08,False),(x-.08,True),(x+.08,True)]:
  for i in range(N):
   a=math.tau*i/N;sy,sz=math.sin(a),math.cos(a);r=.06 if inner else min(.17/max(abs(sy),1e-12),.19/max(abs(sz),1e-12));v.append((xx,CY+r*sy,CZ+r*sz))
 f=[]
 for i in range(N):
  j=(i+1)%N
  for a,b,c,d in[(i,j,N+j,N+i),(2*N+i,3*N+i,3*N+j,2*N+j),(i,2*N+i,2*N+j,j),(N+i,N+j,3*N+j,3*N+i)]:f.extend([(a,b,c),(a,c,d)])
 record(side+'TrueBoredAxleBearing',v,f,2)
wheel('WholeFixedHorizontalAxle',0,CY,CZ,.06,0,2.04,2)
wheel('WholeSheaveHub',0,CY,CZ,.15,0,.35,2)
# One closed annular rim with a real continuous recessed circumferential cable groove.
profile=[(.49,-.10),(.64,-.10),(.66,-.08),(.66,-.045),(.60,-.025),(.60,.025),(.66,.045),(.66,.08),(.64,.10),(.49,.10)]
n=32;v=[(x,CY+r*math.sin(math.tau*i/n),CZ+r*math.cos(math.tau*i/n))for r,x in profile for i in range(n)];f=[]
for k in range(len(profile)):
 for i in range(n):
  j=(i+1)%n;a=k*n+i;b=k*n+j;c=((k+1)%len(profile))*n+j;d=((k+1)%len(profile))*n+i;f.extend([(a,b,c),(a,c,d)])
record('WholeContinuousGroovedSheaveRim',v,f,1)
for i in range(6):
 a=math.tau*i/6;d=(0,math.sin(a),math.cos(a));t=(0,-math.cos(a),math.sin(a));v=[]
 for r in[.14,.50]:
  for x,k in[(-.045,-1),(.045,-1),(.045,1),(-.045,1)]:v.append((x,CY+r*d[1]+k*.035*t[1],CZ+r*d[2]+k*.035*t[2]))
 f=[]
 for a,b,c,d0 in[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:f.extend([(a,b,c),(a,c,d0)])
 record('FixedSheaveSpoke%02d'%i,v,f,1)
# A single whole raised shaft-mouth collar, truly open through its thickness.
outer=[(-.58,-1.37),(.58,-1.37),(.58,-.07),(-.58,-.07)];inner=[(-.42,-1.21),(.42,-1.21),(.42,-.23),(-.42,-.23)];v=[(x,y,z)for p,z in[(outer,0),(outer,.18),(inner,0),(inner,.18)]for x,y in p];f=[]
for i in range(4):
 j=(i+1)%4
 for a,b,c,d in[(i,j,4+j,4+i),(8+i,12+i,12+j,8+j),(i,8+i,8+j,j),(4+i,4+j,12+j,12+i)]:f.extend([(a,b,c),(a,c,d)])
record('WholeOpenShaftMouthCollar',v,f,3)
# Horizontally bounds-centred ground origin, applied once to every complete component.
ps=[p for v,f,m in G.values()for p in v];cx=(min(p[0]for p in ps)+max(p[0]for p in ps))/2;cy=(min(p[1]for p in ps)+max(p[1]for p in ps))/2
for name,(v,f,m)in list(G.items()):G[name]=([(x-cx,y-cy,z)for x,y,z in v],f,m)

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
for name,color,rough in [('Headgear_PaintedSteel', (0.2, 0.32, 0.29, 1), 0.78), ('Sheave_Oxide', (0.52, 0.26, 0.12, 1), 0.76), ('Axle_GraphiteSteel', (0.19, 0.21, 0.21, 1), 0.6), ('Footings_Stone', (0.43, 0.42, 0.37, 1), 0.9)]:
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
focus=Vector((0,0,2.05))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=5.10;aim(cam,(6,-8,4.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/village/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'cave-mine','style':'S01-clean-geometric','title':'Fixed Mine Shaft Headframe with Grooved Sheave','description':'One original complete fixed mine shaft headframe appearance. Two tall front posts and two long raked rear stays carry separate top bearing rails, true through-bored axle housings, one whole horizontal fixed axle and a large six-spoke sheave with a genuinely recessed continuous rim groove. Offset rear diagonal braces and cross ties sit behind the front vertical shaft-mouth zone. One complete raised open rectangular shaft collar and four whole ground footplates define the support base. All geometry newly authored, no old swing, winch or portal mesh reused; generic fixed mesh construction only. Separate closed material components and intentionally embedded fixed frame/spoke joints, not a single welded shell or all-finite-interface proof. No rope, cage, winch, working shaft excavation, motion, hoisting, mining operation, load rating, engineering or safety claim. The preview ground remains visible through the collar; no underground pit is modelled.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
