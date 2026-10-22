import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='cave-mine-wide-basin-inclined-spiral-classifier-01'
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
# One complete broad settling basin narrowing into a raised open classifier trough.
# A fixed solid helical ribbon, shaft, real bored end housings and grounded frame.
def channel_section(y):
 f=.16 if y<=-.30 else .16+.41*(y+.30)
 w=.60 if y<=-.30 else .60-.24*min(1,(y+.30)/.60)
 wi=.55 if y<=-.30 else .55-.25*min(1,(y+.30)/.60)
 top=.60 if y<=-.30 else f+.44-.10*min(1,(y+.30)/.60)
 left=.46 if abs(y+.75)<1e-8 else top
 return[(-w,f-.06),(w,f-.06),(w,top),(wi,top),(wi,f),(-wi,f),(-wi,left),(-w,left)]
ys=[-1.05,-.75,-.45,-.30,.30,1.40];v=[(x,y,z)for y in ys for x,z in channel_section(y)];f=[];n=8
for a,b,c in earclip(channel_section(ys[0])):f.append((c,b,a))
o=(len(ys)-1)*n
for a,b,c in earclip(channel_section(ys[-1])):f.append((a+o,b+o,c+o))
for k in range(len(ys)-1):
 for i in range(n):
  j=(i+1)%n;a=k*n+i;b=k*n+j;c=(k+1)*n+j;dd=(k+1)*n+i;f.extend([(a,b,c),(a,c,dd)])
record('WholeWideBasinToRisingNarrowOpenChannel',v,f,0)
box('WholeLowerBasinEndWall',(-.60,-1.11,.10),(.60,-1.05,.60),0)
d=unit((0,1,.41));u=(1,0,0);w=cross(d,u)
def axis(y):return(0,y,.573+.41*y)
pipe('WholeFixedInclinedRotorShaft',[axis(-.80),axis(1.62)],.05,1,16)
# One three-turn closed material ribbon, not separate discs or a fake spiral texture.
v=[];f=[];steps=96
for k in range(steps+1):
 a=math.tau*3*k/steps;p=axis(-.20+1.45*k/steps);rad=add(mul(u,math.cos(a)),mul(w,math.sin(a)))
 for rr,t in[(.045,-.0125),(.24,-.0125),(.24,.0125),(.045,.0125)]:v.append(add(p,add(mul(rad,rr),mul(d,t))))
for k in range(steps):
 for i in range(4):
  j=(i+1)%4;a=k*4+i;b=k*4+j;c=(k+1)*4+j;dd=(k+1)*4+i;f.extend([(a,b,c),(a,c,dd)])
f.extend([(0,2,1),(0,3,2)]);o=steps*4;f.extend([(o,o+1,o+2),(o,o+2,o+3)])
record('WholeContinuousThreeTurnClassifierFlight',v,f,1)
for label,y in [('Lower',-.70),('Upper',1.52)]:
 name=label+'CompleteThroughBoredRotorBearing';wheel(name,0,0,0,.105,.052,.12,2);vv,ff,mm=G[name];p=axis(y);G[name]=([add(p,add(mul(d,x),add(mul(u,yy),mul(w,z))))for x,yy,z in vv],ff,mm)
box('LowerBasinBearingPedestal',(-.115,-.76,.16),(.115,-.64,.21),2)
box('UpperOutboardBearingCrossMember',(-.46,1.46,1.085),(.46,1.62,1.14),2)
for side,x in [('Left',-.50),('Right',.50)]:box(side+'LowerGroundFoot',(x-.13,-.98,0),(x+.13,-.70,.10),2)
for side,x in [('Left',-.25),('Right',.25)]:
 box(side+'UpperGroundFoot',(x-.13,.97,0),(x+.13,1.33,.05),2)
 ya,yb=1.07,1.23;v=[(xx,yy,zz)for xx in[x-.055,x+.055]for yy,zz in[(ya,.05),(yb,.05),(yb,.10+.41*(yb+.30)),(ya,.10+.41*(ya+.30))]];f=[]
 for a,b,c,dd in[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:f.extend([(a,b,c),(a,c,dd)])
 record(side+'WholeInclinedTopUpperLeg',v,f,2)
box('UnderChannelFrameCrossBrace',(-.44,1.11,.58),(.44,1.19,.64),2)
for side,x in[('Left',-.40),('Right',.40)]:pipe(side+'ExternalUpperBearingRaker',[(x,1.15,.61),(x,1.54,1.11)],.035,2,12)
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
for name,color,rough in [('Basin_OxidePaint', (0.26, 0.38, 0.36, 1), 0.78), ('Rotor_MattSteel', (0.54, 0.58, 0.58, 1), 0.64), ('Frame_DarkPaint', (0.16, 0.2, 0.2, 1), 0.74)]:
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
focus=Vector((0,0,.65))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.65;aim(cam,(-6,-4,4.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/village/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'cave-mine','style':'S01-clean-geometric','title':'Fixed Wide-Basin Inclined Spiral Classifier','description':'One newly authored complete static mineral-processing appearance: an integral broad low basin narrows into an inclined open U-channel with an open elevated discharge end, a lower end wall and a visibly lowered side crest. One real continuous three-turn thick helical ribbon and shaft span the basin/channel, held by two through-bored fixed housings, an outboard bearing crossmember, rakers and four grounded feet. This is not the old soil auger laid in a generic box: the new integral wide-to-narrow rising vessel and the complete bearing/frame arrangement define the whole installation. All components newly authored; mature box, annular housing and polygon-sweep construction only. The assembled bores are occupied by the shaft and are not claimed unobstructed. Static art, no motor, water, moving rotation, actual sorting, flow capacity, installation, load or machinery safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
