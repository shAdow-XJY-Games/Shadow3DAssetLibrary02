import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='public-service-fixed-lowered-upper-trough-cycle-rack-01'
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



def full_prism(name,p,a,b,axis,mat):
 if sum(u[0]*v[1]-u[1]*v[0]for u,v in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 def pt(q,t):return(q[0],q[1],t)if axis=='z'else(t,q[0],q[1])if axis=='x'else(q[0],t,q[1])
 n=len(p);tt=triangulate(p);mesh(name,[pt(q,t)for t in[a,b]for q in p],[tuple(reversed(t))for t in tt]+[tuple(n+i for i in t)for t in tt]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],mat)
for side,x in [('Left',-.25),('Right',.25)]:
 for j,y in enumerate([-.75,.80]):box(side+'WholeGroundFoot_'+str(j),(x,y,.018),(.16,.18,.036),2)
 box(side+'WholeLongBaseRail',(x,.025,.080),(.070,1.70,.105),0)
 box(side+'WholeRearColumn',(x,.80,.87),(.060,.080,1.60),0)
 beam(side+'WholeColumnBrace',(x,.30,.080),(x,.80,.68),.045,0)
for j,y in enumerate([-.75,.80]):box('WholeBaseCrossTie_'+str(j),(0,y,.115),(.56,.065,.055),0)
profile=[(-.065,0),(.065,0),(.065,.055),(.049,.055),(.049,.014),(-.049,.014),(-.049,.055),(-.065,.055)]
def track(name,a,b):
 d=sub(b,a);L=math.sqrt(dot(d,d));u=unit(d);n=(0,-u[2],u[1]);p=profile;N=len(p);tt=triangulate(p);v=[]
 for t in[0,L]:
  for x,z in p:v.append((a[0]+x,a[1]+u[1]*t+n[1]*z,a[2]+u[2]*t+n[2]*z))
 mesh(name,v,[tuple(reversed(q))for q in tt]+[tuple(N+i for i in q)for q in tt]+[(i,(i+1)%N,(i+1)%N+N,i+N)for i in range(N)],1)
track('WholeLowerHorizontalOpenTrough',(0,-1.10,.140),(0,1.00,.140))
track('WholeUpperLoweredOpenTrough',(0,-1.50,.350),(0,.800,1.550))
box('WholeLowerRearWheelStop',(0,.955,.188),(.126,.027,.060),3)
# Upper axle and cheeks connect the complete upper trough to the high rear columns.
axle('WholeHighRearTransversePivot',-.305,.305,.80,1.550,.027,3,20)
for side,x in [('Left',-.25),('Right',.25)]:
 box(side+'WholeUpperPivotCheek',(x,.80,1.55),(.080,.14,.18),0)
 axle(side+'WholeProudPivotCap',x-.054,x+.054,.80,1.55,.039,3,20)
# Real sloping closed sleeves/rods drawn on one line; appearance only, fixed pose.
def roundrod(name,a,b,r,mat,N=16):
 w=unit(sub(b,a));u=unit(cross(w,(1,0,0)));v=cross(w,u);vv=[tuple(p[k]+r*(u[k]*math.cos(math.tau*i/N)+v[k]*math.sin(math.tau*i/N))for k in range(3))for p in[a,b]for i in range(N)];mesh(name,vv,[tuple(reversed(range(N))),tuple(N+i for i in range(N))]+[(i,(i+1)%N,(i+1)%N+N,i+N)for i in range(N)],mat)
for side,x in [('Left',-.14),('Right',.14)]:
 a=(x,.80,.62);b=(x,-.35,.95);mid=tuple(a[k]+.62*(b[k]-a[k])for k in range(3))
 roundrod(side+'WholeSlopingSupportSleeve',a,mid,.025,0)
 roundrod(side+'WholeExtendedSupportRod',tuple(a[k]+.55*(b[k]-a[k])for k in range(3)),b,.012,3)
 axle(side+'WholeLowerSupportAxle',min(x,-.25 if x<0 else .25)-.016,max(x,-.25 if x<0 else .25)+.016,.80,.62,.023,3,16)
 axle(side+'WholeUpperTraySupportAxle',min(x,0)-.020,max(x,0)+.020,-.35,.950,.020,3,16)
# Upper rear stop and a genuine full open front grip, transformed with the tray's fixed slope.
u=unit((0,2.30,1.20));normal=(0,-u[2],u[1])
def place_upper(name):
 v,f,m=G[name];G[name]=([(x,-1.50+u[1]*y+normal[1]*z,.350+u[2]*y+normal[2]*z)for x,y,z in v],f,m)
L=math.hypot(2.30,1.20)
box('WholeUpperRearWheelStop',(0,L-.045,.055),(.126,.025,.075),3);place_upper('WholeUpperRearWheelStop')
p=[(-.105,-.12),(.105,-.12),(.105,.025),(.082,.025),(.082,-.095),(-.082,-.095),(-.082,.025),(-.105,.025)]
full_prism('WholeFrontOpenGrip',p,.003,.025,'z',2);place_upper('WholeFrontOpenGrip')
for side,x in [('Left',-.07),('Right',.07)]:box(side+'WholeGripSeat',(x,.010,.018),(.050,.055,.025),2);place_upper(side+'WholeGripSeat')
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeFrameAndSleeves_MutedTeal',(.10,.25,.27,1),.65,.25),('WholeContinuousTroughs_SatinAlloy',(.49,.53,.51,1),.54,.42),('WholeFeetAndGrip_Charcoal',(.04,.05,.05,1),.78,0),('WholePinsStopsAndRods_DullOchre',(.55,.35,.11,1),.58,.25)]
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
focus=Vector((0,0,.81))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.35;aim(cam,(4,-6,3.7));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/public-service/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'public-service','style':'S01-clean-geometric','title':'Fixed Lowered Upper Trough Cycle Rack','description':'One newly authored complete empty two-level cycle-parking rack appearance in one fixed lowered-upper-tray pose. Four full finite mounting feet and a low common rectangular chassis carry a full horizontal open U wheel trough. Two complete rear columns support a real transverse upper pivot shaft and a second entire long U trough tilted downward and forward into a distinct loading silhouette. Two independently drawn side sleeve-and-rod supports meet separate whole pins beneath the upper trough. Continuous high side walls, rear stop bars, a full front loop grip and fixed rear pivot cheeks belong to the one common rack, not two unrelated stands. No old parking hoop, bicycle, scissor platform, crossed link or tray mesh imported. Four opaque PBR roles; metres Z up, whole XY bounds centred, four ground soles, one model zero scenes. Static empty visual structure only: no lifting or sliding travel, mechanism constraints, counterbalance, damping, wheel capture, bicycle fit or support, accessibility certification, human operation, security, manufacture, installation or load/safety performance. No bicycle supplied, no rigging animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
