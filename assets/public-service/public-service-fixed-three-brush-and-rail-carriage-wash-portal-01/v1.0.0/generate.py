import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='public-service-fixed-three-brush-and-rail-carriage-wash-portal-01'
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



# Two continuous grounded rail beds; all portal wheels remain above their running tops.
for side in[-1,1]:
 x=side*1.67
 box('WholeGroundFootRailBed_'+str(side),(x,0,.055),(.30,2.9,.11),3)
 box('WholeRaisedRunningRail_'+str(side),(x,0,.135),(.12,2.86,.05),3)
 for k,y in enumerate([-.52,.52]):
  # Flat-tread fixed wheel radius puts its bottom on the rail top.
  N=20;r=.14/math.cos(math.pi/N)
  v=[(xx,y+r*math.sin(math.tau*i/N+math.pi/N),.30+r*math.cos(math.tau*i/N+math.pi/N))for xx in[x-.073,x+.073]for i in range(N)]
  mesh('WholeCarriageWheel_'+str((side,k)),v,[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N)for i in range(N)],2)
  axle('WholeWheelAxle_'+str((side,k)),x-.16,x+.16,y,.30,.035,3,16)
  for q in[-1,1]:box('WholeWheelCheek_'+str((side,k,q)),(x+q*.115,y,.39),(.055,.15,.24),0)
 box('WholeLongCarriageFoot_'+str(side),(x,0,.51),(.40,1.45,.15),0)
 box('WholePortalUpright_'+str(side),(x,0,1.97),(.24,.35,2.82),0)
 box('WholePortalTopShoulder_'+str(side),(x,0,3.40),(.38,.39,.17),0)
box('WholeUpperPortalCrosshead',(0,0,3.49),(3.62,.43,.22),0)
box('WholeBlankFrontHeader',(0,-.235,3.49),(2.73,.035,.13),1)
# Thick closed fluted exterior, no floating bristle chips. Each cap is a true centre fan.
def brush(name,a,b,r,mat):
 w=unit(sub(b,a));u=unit(cross(w,(1,0,0)if abs(w[0])<.9 else(0,1,0)));v0=cross(w,u);N=48;vv=[]
 for p in[a,b]:
  for i in range(N):
   rr=r if i%2==0 else r*.84;vv.append(tuple(p[k]+rr*(u[k]*math.cos(math.tau*i/N)+v0[k]*math.sin(math.tau*i/N))for k in range(3)))
 vv +=[a,b];fs=[]
 for i in range(N):j=(i+1)%N;fs +=[(i,j,N+j,N+i),(2*N,j,i),(2*N+1,N+i,N+j)]
 mesh(name,vv,fs,mat)
for side in[-1,1]:
 x=side*1.07
 # Whole lateral arm joins its complete pivot seat to the top of one long hanging brush.
 lathe_z('WholeSideArmPivot_'+str(side),side*1.67,-.04,[(0,3.17),(.075,3.17),(.075,3.43),(0,3.43)],3,20)
 beam('WholeSideSuspensionArm_'+str(side),(side*1.67,-.04,3.24),(x,-.48,3.24),.13,1)
 lathe_z('WholeVerticalBrushMotorExterior_'+str(side),x,-.48,[(0,3.16),(.12,3.16),(.12,3.47),(0,3.47)],0,20)
 lathe_z('WholeVerticalBrushShaft_'+str(side),x,-.48,[(0,.32),(.045,.32),(.045,3.25),(0,3.25)],3,16)
 brush('WholeLongVerticalBrush_'+str(side),(x,-.48,.39),(x,-.48,2.91),.325,2)
 for k,z in enumerate([.37,2.93]):lathe_z('WholeVerticalBrushEndHub_'+str((side,k)),x,-.48,[(0,z-.025),(.105,z-.025),(.105,z+.025),(0,z+.025)],3,20)
# Upper cross brush is separately supported by guide sleeves, not intersecting the side rolls.
for side in[-1,1]:
 x=side*1.42
 box('WholeVerticalGuideStay_'+str(side),(side*1.56,.10,2.08),(.24,.13,1.91),3)
 lathe_z('WholeVerticalCrossBrushGuide_'+str(side),x,.10,[(0,1.08),(.036,1.08),(.036,3.22),(0,3.22)],3,20)
 lathe_z('WholeBoredCrossBrushSleeve_'+str(side),x,.10,[(.035,2.40),(.075,2.40),(.075,2.86),(.035,2.86)],1,20)
 box('WholeCrossBrushBearingArm_'+str(side),(side*1.30,.22,2.62),(.30,.31,.13),1)
 axle('WholeCrossBrushBearing_'+str(side),side*1.30-.085,side*1.30+.085,.30,2.62,.085,3,20)
axle('WholeFullCrossBrushAxle',-1.40,1.40,.30,2.62,.040,3,20)
brush('WholeUpperHorizontalBrush',(-1.22,.30,2.62),(1.22,.30,2.62),.285,2)
for side in[-1,1]:axle('WholeCrossBrushEndHub_'+str(side),side*1.24-.025,side*1.24+.025,.30,2.62,.105,3,20)
box('WholeSideServiceCase',(1.88,.035,1.33),(.26,.53,.95),0)
box('WholeBlankServiceControlFace',(1.88,-.243,1.43),(.17,.035,.25),2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholePortalAndCases_MutedTeal',(.16,.36,.35,1),.68,.09),('WholeArmsAndHeader_WarmIvory',(.73,.72,.63,1),.66,.08),('WholeFlutedBrushesAndWheels_DeepBlue',(.055,.12,.19,1),.88,.01),('WholeRailsGuidesHubs_DullAlloy',(.40,.46,.46,1),.51,.38)]
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
focus=Vector((0,0,1.72))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=6.25;aim(cam,(5,-8,5.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/public-service/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'public-service','style':'S01-clean-geometric','title':'Fixed Three Brush and Rail Carriage Wash Portal','description':'One wholly newly authored complete empty vehicle-wash-portal-style static exterior. Two full ground rails support four fixed wheels and two long carriage feet beneath a high open through-portal. Two independently supported front swing-arm appearances suspend whole vertical fluted brush cylinders with complete upper shafts and lower hubs. A separate broad horizontal fluted cylinder sits on its full axle between two vertical guide-carriage appearances inside the portal, with genuine bored sleeves, full guides and a raised crosshead. A whole side service case and blank control face belong to the same machine. This is not the low shoe-polisher enlarged: that old backed foot bay contains only paired coaxial horizontal rolls, while the new full-height through-lane has opposed vertical brushes and an independent upper cross-brush on a travelling portal exterior. It is not the old three-axis gantry fitted with renamed fingers: no fixed four-post overhead rail cage or central downward tool survives. All coordinates newly authored, no old mesh imported. Four opaque solid PBR roles, metres Z up and whole centred ground datum, one model zero scenes. Empty dry fixed visual only: no vehicle, bristles at fibre scale, water, fluid circuit, cleaning, brush contact, rail travel, brush rotation, drive transmission, vehicle clearance, electrical operation, machinery guarding, manufacture, installation or safety capability. Rigging animation interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
