import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='public-service-fixed-tall-hoop-and-inclined-track-chair-01'
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



def prism_yz(name,p,x0,x1,mat):
 if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 ts=triangulate(p);n=len(p);v=[(x,y,z)for x in[x0,x1]for y,z in p];f=[tuple(reversed(t))for t in ts]+[tuple(n+i for i in t)for t in ts]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh(name,v,f,mat)
def tube(name,path,r,mat,n=12):
 v=[];f=[]
 for j,p in enumerate(path):
  w=unit(sub(path[min(j+1,len(path)-1)],path[max(0,j-1)]));u=unit(cross(w,(1,0,0)if abs(w[0])<.9 else(0,1,0)));q=cross(w,u)
  for i in range(n):v.append(tuple(p[k]+r*(u[k]*math.cos(math.tau*i/n)+q[k]*math.sin(math.tau*i/n))for k in range(3)))
 f=[tuple(reversed(range(n))),tuple((len(path)-1)*n+i for i in range(n))]+[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i)for j in range(len(path)-1)for i in range(n)];mesh(name,v,f,mat)
# One entire tall bent handle/back-support hoop, continuous across its top.
tube('WholeTallBackAndCarryHoop',[(-.255,.60,.13),(-.255,.26,.78),(-.255,.17,1.30),(-.255,.20,1.52),(-.19,.22,1.57),(.19,.22,1.57),(.255,.20,1.52),(.255,.17,1.30),(.255,.26,.78),(.255,.60,.13)],.023,0)
for sg in[-1,1]:
 x=sg*.255
 tube('WholeFrontSeatAndStandingSide'+str(sg),[(x,-.45,.135),(x,-.36,.50),(x,-.29,.57),(x,.27,.57),(x,.36,.40)],.024,0)
 beam('WholeRearTrackSeatStay'+str(sg),(x,.22,.57),(x,.42,.43),.055,0)
 axle('WholeSeatSidePivot'+str(sg),x-.045,x+.045,.26,.57,.035,3,16)
# A single closed thin bent sling joins seat and tall back, without separate upholstered cushions.
prism_yz('WholeContinuousSeatBackSling',[(-.32,.56),(.20,.56),(.255,.63),(.18,1.25),(.205,1.255),(.28,.62),(.22,.535),(-.32,.535)],-.245,.245,1)
# Whole wide foot platform and complete paired roots, not two wheelchair foot plates.
box('WholeFrontFootPlatform',(0,-.51,.19),(.56,.23,.035),2)
for sg in[-1,1]:beam('WholeFootPlatformRoot'+str(sg),(sg*.255,-.40,.36),(sg*.255,-.50,.185),.035,0)
axle('WholeFrontTransverseSupport',-.30,.30,-.43,.135,.024,3,16)
# Narrow parallel inclined tracks behind the sling; each complete ring retains a genuine centre opening.
a=(.61,.125);b=(.225,1.035);theta=math.atan2(b[1]-a[1],b[0]-a[0])
def outline(r):
 p=[]
 for c,start in[(b,theta-math.pi/2),(a,theta+math.pi/2)]:
  for j in range(13):
   t=start+math.pi*j/12;p.append((c[0]+r*math.cos(t),c[1]+r*math.sin(t)))
 return p
for sg in[-1,1]:
 x=sg*.255;x0=x-.047;x1=x+.047;outer=outline(.125);inner=outline(.088)
 # Finite parked contact facet at lower belt end, kept on the original straight rim rather than a separate ground pedestal.
 zmin=min(z for y,z in outer);outer=[(y,0 if z<zmin+.010 else z-zmin)for y,z in outer];inner=[(y,z-zmin)for y,z in inner];n=len(outer)
 v=[(xx,y,z)for xx in[x0,x1]for p in[outer,inner]for y,z in p];f=[]
 for i in range(n):j=(i+1)%n;f.extend([(i,j,2*n+j,2*n+i),(n+i,3*n+i,3*n+j,n+j),(i,n+i,n+j,j),(2*n+i,2*n+j,3*n+j,3*n+i)])
 mesh('WholeRearGroundFootTrack'+str(sg),v,f,2)
 beam('WholeInclinedTrackBearingRail'+str(sg),(x,a[0],a[1]-zmin),(x,b[0],b[1]-zmin),.055,3)
 for j,t in enumerate([0,.5,1]):
  yy=a[0]+t*(b[0]-a[0]);zz=a[1]+t*(b[1]-a[1])-zmin
  axle('WholeTrackRoller'+str((sg,j)),x0+.004,x1-.004,yy,zz,.092,3,20)
  axle('WholeTrackAxle'+str((sg,j)),x-.065,x+.065,yy,zz,.018,0,12)
 # A complete folded-side link meets the back hoop and the rear-bearing member.
 beam('WholeTrackUpperMount'+str(sg),(x,.23,.97),(x,b[0],b[1]-zmin),.055,0)
 # Fixed small front wheel and its full fork, with a real broad flat bottom facet.
 r=.075/math.cos(math.pi/16);poly=[(-.45+r*math.cos(math.pi/16+math.tau*j/16),.075+r*math.sin(math.pi/16+math.tau*j/16))for j in range(16)]
 prism_yz('WholeFrontGroundFootWheel'+str(sg),poly,x-.026,x+.026,2)
 axle('WholeFrontWheelAxle'+str(sg),x-.060,x+.060,-.45,.075,.018,3,16)
 for side in[-1,1]:beam('WholeFrontForkCheek'+str((sg,side)),(x+side*.045,-.45,.075),(x+side*.045,-.43,.15),.025,0)
 axle('WholeFrontForkBridge'+str(sg),x-.057,x+.057,-.43,.15,.025,0,12)
# Whole low rear cross tie connects the two bearing sides below the seat.
axle('WholeRearLowCrossTie',-.30,.30,.55,.25,.022,0,16)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];shift=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-shift[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('Frame_MutedAmber',(.70,.38,.10,1),.63,.24),('Sling_DeepBlue',(.08,.16,.20,1),.88,0),('TrackAndFoot_DarkGraphite',(.045,.055,.055,1),.83,.03),('AxleRail_SatinAlloy',(.40,.44,.44,1),.48,.52)]
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
focus=Vector((0,0,.80))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.35;aim(cam,(5,-7,3.4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/public-service/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'public-service','style':'S01-clean-geometric','title':'Tall Hoop and Inclined Track Chair','description':'One newly authored complete empty inclined-track chair appearance in a fixed parked pose. A continuous tall back-and-carry hoop supports a whole thin bent seat/back sling and connects to two long rear inclined closed-loop tracks. Each entire track retains its true open centre, full bearing rail, three rooted rollers and transverse axle exteriors. Separate fixed seat side rails join two low front forked wheels and a full single forward foot platform; short upper track mounts and rear stays connect the bearing rails to the chair frame. No large rear drive wheels or outboard hand rims, individual wheelchair arm pads or paired foot plates are used. Unlike a tracked excavator chassis carrying a seat, there is no horizontal crawler deck, pedestal, engine, cabin or boom; the inclined bearing assembly belongs to the tall chair frame itself. All geometry newly authored, no old seat or tracks imported. Four opaque PBR roles. One model zero scenes. Empty static art only: no rolling, stair travel, traction, braking, carrying, folding, transfer, evacuation or rescue function, occupant dimensions, disability or medical suitability, load, manufacture or human safety capability. Rigging animation interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
