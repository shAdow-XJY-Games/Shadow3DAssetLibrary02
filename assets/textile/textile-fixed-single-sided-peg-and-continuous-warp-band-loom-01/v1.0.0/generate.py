import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='textile-fixed-single-sided-peg-and-continuous-warp-band-loom-01'
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



# Whole side-supported narrow-band frame: two broad ground crossfeet, long side rail and high back.
for j,x in enumerate([-.30,.27]):box('WholeGroundFoot_%d'%j,(x,0,.025),(.075,.34,.05),1)
box('WholeLowLongitudinalSideRail',(0,.105,.070),(.68,.065,.085),0)
box('WholeRearUpright',(.27,.107,.360),(.065,.075,.620),0)
beam('WholeInclinedSideArm',(-.30,.105,.290),(.27,.105,.640),.047,0)
box('WholeFrontShortPost',(-.30,.101,.185),(.058,.061,.255),0)
beam('WholeLowerDiagonalSideBrace',(-.03,.105,.180),(.27,.105,.380),.043,0)
box('WholeLowPegSupport',(-.03,.106,.120),(.055,.058,.145),0)
# Full cantilevered pegs belong to the one-sided frame; front free ends stay visible.
P=[(-.30,.30),(-.05,.55),(.27,.64),(.27,.38),(-.03,.18)]
# Middle upper peg needs a true independent short root rather than a floating cylinder.
beam('WholeMiddlePegRoot',(-.05,.105,.55),(-.05,.105,.4435),.039,0)
for j,(x,z)in enumerate(P):
 cyly('WholeCantileverWarpPeg_%d'%j,-.155,.139,x,z,.022,0,20)
 cyly('WholePegEndShoulder_%d'%j,-.161,-.149,x,z,.029,1,20)
# Closed CW polygon around the five whole pegs. Every corner is a real sampled round wrap.
# Parallel full loops are static warp exteriors, not functional interlacing.
path=[]
for k,(x,z)in enumerate(P):
 prev=P[k-1];nxt=P[(k+1)%len(P)]
 a=math.atan2(z-prev[1],x-prev[0])+math.pi/2
 b=math.atan2(nxt[1]-z,nxt[0]-x)+math.pi/2
 while b>a:b-=math.tau
 # The convex clockwise path rotates outward normals clockwise, under half turn.
 for j in range(7):
  t=a+(b-a)*j/6;path.append((x+.0232*math.cos(t),z+.0232*math.sin(t)))
def loop_thread(name,y):
 v=[];f=[];n=6
 for k,(x,z)in enumerate(path):
  a=path[k-1];b=path[(k+1)%len(path)];t=unit((b[0]-a[0],0,b[1]-a[1]));u=(0,1,0);w=cross(t,u)
  for j in range(n):v.append((x+.0022*w[0]*math.sin(math.tau*j/n),y+.0022*math.cos(math.tau*j/n),z+.0022*w[2]*math.sin(math.tau*j/n)))
 for k in range(len(path)):
  h=(k+1)%len(path)
  for j in range(n):q=(j+1)%n;f.append((k*n+j,k*n+q,h*n+q,h*n+j))
 mesh(name,v,f,2)
for j in range(8):loop_thread('WholeContinuousWarpCircuit_%d'%j,-.112+j*.017)
# Short complete lower heddle bar and open loops connect a subset of the upper sloping threads.
box('WholeHeddleBarRoot',(-.13,.108,.200),(.040,.052,.285),0)
cyly('WholeLowHeddleBar',-.150,.134,-.13,.330,.014,1,16)
for j in range(4):
 y=-.112+2*j*.017
 # Fixed elongated loop with actual open centre, rooted at lower bar and reaching upper warp.
 v=[];f=[];poly=[(-.141,.328),(-.139,.498),(-.121,.524),(-.111,.505),(-.119,.329)];inner=[(-.136,.332),(-.134,.496),(-.121,.516),(-.116,.503),(-.124,.333)]
 for yy in[y-.002,y+.002]:
  for ring in[poly,inner]:v +=[(x,yy,z)for x,z in ring]
 n=len(poly)
 for k in range(n):h=(k+1)%n;f +=[(k,h,n+h,n+k),(2*n+k,3*n+k,3*n+h,2*n+h),(k,2*n+k,2*n+h,h),(n+k,n+h,3*n+h,3*n+k)]
 mesh('WholeOpenHeddleLoop_%d'%j,v,f,3)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeSideFrameAndPegs_WarmWood',(.49,.28,.12,1),.80,0),('WholeFeetAndPegTips_DarkWood',(.23,.12,.05,1),.84,0),('WholeWarpLoops_Ivory',(.81,.74,.57,1),.92,0),('WholeHeddleLoops_MutedBlue',(.11,.28,.34,1),.86,0)]
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
focus=Vector((0,0,.34))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.02;aim(cam,(3,-7,3.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/textile/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'textile','style':'S01-clean-geometric','title':'Fixed Single Sided Peg and Continuous Warp Band Loom','description':'One newly authored complete one-sided narrow-band weaving-frame appearance. Two full crossfeet carry a low longitudinal side frame, a high rear upright, rising side arm and lower brace. Five complete cantilevered round pegs support eight continuous closed warp-appearance circuits around the entire changing-height route. Every route bends around the actual peg surface rather than ending in disconnected straight painted lines. A separate low transverse heddle bar and four whole genuinely open elongated loops occupy the front upper working span. Unlike the old horizontal four-wing warping cage, this is not an axial rotating framework with two end stands; all pegs project from one side and the thread path stays in a vertical plane. Unlike the full treadle floor loom, there are no two end drums, tall two-shaft castle, beater or treadles. No old mesh imported, extracted or scaled. Four opaque constant PBR roles, metres Z up and horizontal whole-bounds-centred ground origin. One whole static prop zero scenes. Generic inkle-inspired display only, not a validated weaving system: no interlacing sequence, shed change, thread movement, tension, textile result, ergonomic suitability, adjustment, manufacture or safe operation. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
