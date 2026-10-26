import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='textile-fixed-cross-carriage-and-twin-roll-longarm-quilting-frame-01'
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



def whole_profile(name,p,a,b,axis,mat):
 if sum(u[0]*v[1]-u[1]*v[0]for u,v in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);tt=triangulate(p)
 def pt(q,t):return(t,q[0],q[1])if axis=='x'else(q[0],t,q[1])
 mesh(name,[pt(q,t)for t in[a,b]for q in p],[tuple(reversed(t))for t in tt]+[tuple(n+i for i in t)for t in tt]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],mat)
for x in[-1.,1.]:
 for y in[-.50,.50]:
  box('WholeGroundFoot_'+str((x,y)),(x,y,.025),(.15,.16,.050),2)
  box('WholeStandLeg_'+str((x,y)),(x,y,.39),(.060,.060,.72),0)
 box('WholeEndUpperTie_'+str(x),(x,0,.70),(.075,1.05,.060),0)
 box('WholeEndLowTie_'+str(x),(x,0,.18),(.070,1.04,.060),0)
for y in[-.50,.50]:box('WholeLongMainRail_'+str(y),(0,y,.73),(2.18,.065,.080),0)
box('WholeLowerLongTie',(0,.50,.18),(2.05,.045,.045),0)
# Complete rollers on true bored ring heads and independent posts.
for y in[-.36,.36]:
 for x in[-1.,1.]:
  box('WholeRollBearingPost_'+str((x,y)),(x,y,.85),(.070,.055,.27),0)
  ringx('WholeBoredRollBearing_'+str((x,y)),x-.032,x+.032,y,1.03,.022,.047,3,20)
 axle('WholeRollAxle_'+str(y),-1.09,1.09,y,1.03,.022,3,20)
 axle('WholeFullWidthClothRoll_'+str(y),-.94,.94,y,1.03,.060,1,32)
# One entire blank cloth thick boundary passes over both whole rollers.
path=[(-.420,1.01),(-.414,1.06),(-.397,1.085),(-.36,1.095),(.36,1.095),(.397,1.085),(.414,1.06),(.420,1.01)]
p=path+[(y,z-.008)for y,z in reversed(path)];whole_profile('WholeContinuousBlankRollHeldCloth',p,-.90,.90,'x',1)
c=-.18
# First X-travelling carriage, fixed on complete lower wheels at both main rails.
for x in[c-.15,c+.15]:
 box('WholeCrossCarriageRail_'+str(x),(x,.06,.845),(.042,1.44,.035),3)
 for y in[-.50,.50]:
  cyly('WholeLowerCarriageWheel_'+str((x,y)),y-.019,y+.019,x,.803,.033,2,16)
  cyly('WholeLowerWheelAxle_'+str((x,y)),y-.035,y+.035,x,.803,.010,3,12)
  box('WholeLowerWheelCheek_'+str((x,y)),(x,y+.027,.824),(.045,.012,.064),3)
for y in[-.60,.72]:box('WholeCrossCarriageTie_'+str(y),(c,y,.845),(.34,.032,.028),3)
# Second Y-travelling saddle; separate four wheels ride the two crossing rails.
for x in[c-.15,c+.15]:
 for y in[-.18,.58]:
  axle('WholeUpperSaddleWheel_'+str((x,y)),x-.019,x+.019,y,.8975,.035,2,16)
  axle('WholeUpperSaddleAxle_'+str((x,y)),x-.040,x+.040,y,.8975,.011,3,12)
  box('WholeUpperSaddleCheek_'+str((x,y)),(x+.029,y,.922),(.014,.045,.065),3)
box('WholeMachineSaddlePlate',(c,.19,.938),(.39,1.13,.035),0)
# One continuously extruded long C casing includes the lower bed, rear column and head.
p=[(-.35,.950),(.75,.950),(.75,1.40),(.69,1.52),(.53,1.56),(-.25,1.56),(-.34,1.48),(-.34,1.32),(-.20,1.32),(-.20,1.41),(.50,1.41),(.55,1.36),(.55,1.01),(-.35,1.01)]
whole_profile('WholeContinuousLongThroatMachine',p,c-.105,c+.105,'x',0)
# Fixed blunt sewing-head appearances, with a real gap below the long upper arm.
lathe_z('WholeBluntNeedleBar',c,-.272,[(0,1.102),(.0045,1.102),(.0045,1.345),(0,1.345)],3,12)
lathe_z('WholePresserRod',c+.035,-.255,[(0,1.106),(.006,1.106),(.006,1.345),(0,1.345)],3,12)
box('WholeSmallPresserSole',(c+.020,-.268,1.104),(.065,.060,.012),3)
# One side wheel and central hub root into the rear column, no drive function.
axle('WholeSideHandwheel',c+.10,c+.145,.64,1.30,.10,2,24)
axle('WholeProudHandwheelHub',c+.14,c+.16,.64,1.30,.028,3,16)
lathe_z('WholeSpoolPin',c,.36,[(0,1.54),(.008,1.54),(.008,1.74),(0,1.74)],3,12)
lathe_z('WholeBlankThreadSpool',c,.36,[(0,1.60),(.050,1.60),(.050,1.612),(.034,1.612),(.034,1.70),(.050,1.70),(.050,1.714),(0,1.714)],1,20)
box('WholeBlankHeadControl',(c+.110,.02,1.49),(.024,.135,.070),2)
for side in[-1,1]:
 beam('WholeFrontGuideArm_'+str(side),(c+side*.095,-.26,1.43),(c+side*.20,-.47,1.33),.023,3)
 beam('WholeFrontGrip_'+str(side),(c+side*.20,-.47,1.33),(c+side*.20,-.47,1.22),.036,2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeMachineAndFrame_MutedTeal',(.14,.29,.29,1),.66,.10),('WholeBlankClothAndSpool_WarmIvory',(.76,.70,.55,1),.88,0),('WholeFeetWheelsAndControls_Charcoal',(.035,.045,.045,1),.78,0),('WholeRailsAndShafts_SatinAlloy',(.43,.47,.46,1),.48,.45)]
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
focus=Vector((0,0,.83))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.30;aim(cam,(4,-6,4.3));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/textile/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'textile','style':'S01-clean-geometric','title':'Fixed Cross Carriage and Twin Roll Longarm Quilting Frame','description':'One newly authored complete fixed longarm-quilting-frame appearance. Four whole grounded legs and a common open chassis carry two full long rails. A complete cross carriage rests on four lower wheels; two transverse rails carry a second whole four-wheel saddle and one continuous long-throat machine casing with an integral lower bed, raised rear column and forward overhanging head. Two separately supported full-width cloth rollers and axles flank a single continuous blank thick cloth sheet crossing the open working field and curling over both rollers. A full side handwheel, plain top spool, blank control, two forward guide grips and finite blunt needle/presser appearances belong to the one whole assembly. All geometry independently authored, not an old sewing workstation placed on a generic table or an extracted shoe-patcher head. Unlike the old fixed tabletop bed or upturned narrow horn, the broad roll-held field surrounds a two-stage rail carriage with a full long-clearance head. Four opaque PBR roles, metres Z up and whole horizontal bounds-centred ground origin; one model zero scenes. Static artistic machine exterior with one blank display cloth only: no sewing, cutting, needle motion, stitch formation, thread path, carriage travel, roller rotation, tension, workpiece compatibility, ergonomics, load, manufacture or operating safety. Rigging animation interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
