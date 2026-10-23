import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='carpentry-fixed-spring-pole-lathe-display-01'
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



# Whole new open-bed spring-pole lathe; all coordinates authored here.
for label,y in [('Front',-.25),('Rear',.25)]:
 box(label+'WholeLatheBedRail',(0,y,.80),(1.84,.12,.16),0)
for label,x in [('Left',-.73),('Right',.73)]:
 box(label+'WholeGroundFoot',(x,.025,.045),(.18,.93,.09),0)
 for side,y in [('Front',-.25),('Rear',.25)]:box(label+side+'WholeBedLeg',(x,y,.43),(.10,.11,.74),0)
 box(label+'WholeLowCrossTie',(x,.025,.22),(.105,.65,.10),0)
# Full headstock and tailstock each span both rails; fixed centres hold the authored blank.
for label,x in [('Head',-.68),('Tail',.68)]:
 box(label+'WholeCentreStock',(x,0,1.03),(.16,.64,.36),0)
 axle(label+'WholeCentreBearing',x-.09,x+.09,0,1.12,.072,2,20)
axle('WholeLeftFixedCentre',-.72,-.475,0,1.12,.028,2,16)
axle('WholeRightFixedCentre',.475,.72,0,1.12,.028,2,16)
# Complete solid fixed demonstration billet, not a separately counted loose prop.
profile=[(-.50,.026),(-.45,.065),(-.30,.085),(.28,.085),(.43,.060),(.50,.026)];N=24
v=[(x,r*math.cos(math.tau*i/N),1.12+r*math.sin(math.tau*i/N))for x,r in profile for i in range(N)];f=[tuple(reversed(range(N))),tuple((len(profile)-1)*N+i for i in range(N))]
for k in range(len(profile)-1):
 for i in range(N):j=(i+1)%N;f.append((k*N+i,k*N+j,(k+1)*N+j,(k+1)*N+i))
mesh('WholeFixedWoodTurningBlank',v,f,1)
for label,x in [('Left',-.38),('Right',.38)]:box(label+'WholeToolRestPost',(x,-.25,.96),(.07,.07,.23),2)
box('WholeLongFrontToolRest',(0,-.25,1.065),(.96,.065,.045),2)
# Independent grounded high return pole, continuous tapered bent timber, not a loose overhead string.
path=[(-.85,.32,.075),(-.85,.32,.9),(-.80,.31,1.65),(-.61,.26,2.03),(-.32,.18,2.15),(-.15,.11,2.10)]
v=[]
for i,(x,y,z)in enumerate(path):
 a=path[max(0,i-1)];b=path[min(len(path)-1,i+1)];w=unit(sub(b,a));u=unit(cross(w,(0,1,0)));vv=cross(w,u);wid=.092-i*.010
 for su,sv in[(-1,-1),(1,-1),(1,1),(-1,1)]:v.append(tuple((x,y,z)[j]+wid/2*(su*u[j]+sv*vv[j])for j in range(3)))
f=[(3,2,1,0),tuple((len(path)-1)*4+i for i in range(4))]
for k in range(len(path)-1):
 for i in range(4):j=(i+1)%4;f.append((4*k+i,4*k+j,4*(k+1)+j,4*(k+1)+i))
mesh('WholeTaperedBentReturnPole',v,f,0)
box('WholeReturnPoleFootBlock',(-.85,.32,.055),(.20,.24,.11),0)
# Broad foot treadle, hinged to its own rear low cross support.
box('WholeTreadleRearHingeCrossmember',(0,.32,.18),(1.60,.12,.12),0)
zs=lambda y:.145+(y+.58)*(.080/.90)
p=[(-.26,-.58),(.26,-.58),(.26,.32),(-.26,.32)]
v=[(x,y,zs(y)+d)for d in[-.022,.022]for x,y in p];mesh('WholeLongFootTreadle',v,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],0)
axle('WholeTreadleHingeSpindle',-.38,.38,.30,zs(.30),.027,2,20)
# One continuous closed tubular rope: pole tip, one full visible wrap around blank, then treadle.
rope=[(-.15,.11,2.10),(-.15,.11,1.40)]
for i in range(49):
 t=-math.tau*i/48;rope.append((-.15+.30*i/48,.11*math.cos(t),1.12+.11*math.sin(t)))
rope +=[(.15,.11,.50),(.15,.11,zs(.11))]
N=8;v=[]
for i,p in enumerate(rope):
 a=rope[max(0,i-1)];b=rope[min(len(rope)-1,i+1)];w=unit(sub(b,a));ref=(1,0,0)if abs(w[0])<.9 else(0,1,0);u=unit(cross(w,ref));vv=cross(w,u)
 for j in range(N):t=math.tau*j/N;v.append(tuple(p[k]+.007*(math.cos(t)*u[k]+math.sin(t)*vv[k])for k in range(3)))
f=[tuple(reversed(range(N))),tuple((len(rope)-1)*N+i for i in range(N))]
for i in range(len(rope)-1):
 for j in range(N):k=(j+1)%N;f.append((i*N+j,i*N+k,(i+1)*N+k,(i+1)*N+j))
mesh('WholeContinuousPoleBlankTreadleCord',v,f,1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeBedStocksPoleTreadle_Walnut',(.30,.17,.075,1),.82,0),('BlankAndCord_PaleWoodFiber',(.65,.48,.25,1),.82,0),('CentresAndRest_DarkIron',(.12,.15,.15,1),.58,.40)]
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
focus=Vector((0,0,1.08))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.78;aim(cam,(3,-6,3.1));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/carpentry/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'carpentry','style':'S01-clean-geometric','title':'Fixed Spring Pole Lathe Display','description':'One new complete fixed spring-pole wood-lathe appearance. Two long open bed rails on four full legs carry two opposed complete centre stocks and fixed metal centres holding one authored spindle-shaped wood blank. A long front tool rest has two rooted posts. A separate continuous tapered high bent timber return pole reaches over the blank; one continuous thick cord descends from its tip, wraps once around the blank envelope and continues to a complete low rear-hinged foot treadle. Ground feet and cross ties connect the whole apparatus. No flat worktable top, large wheel, motor, yarn bobbin, belt-drive pulley, tool or worker is present. The fixed blank belongs to this one display model and is not a second reusable prop. All whole geometry is newly authored, not extracted from the old open worktable, spinning wheel, pottery kick wheel or piston machinery. Closed editable solids and three opaque PBR roles, metres, native Z up and actual whole horizontal bounds-centred ground origin. One model, zero scenes. This is illustrative static geometry only: the cord has deliberate nonfunctional envelope clearance around the blank, no frictional drive, spring elasticity, tension, pedal travel, rotating or cutting operation, wood-processing result, ergonomic fit, manufacture, load, stability or equipment-safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
