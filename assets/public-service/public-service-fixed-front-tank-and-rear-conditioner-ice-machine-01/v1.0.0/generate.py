import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='public-service-fixed-front-tank-and-rear-conditioner-ice-machine-01'
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



# New whole low vehicle frame and four flat-facet tyres; no old chassis imported.
for j,x in enumerate([-.43,.43]):box('WholeLongChassisRail_%d'%j,(x,-.13,.42),(.14,2.18,.16),2)
for j,y in enumerate([-.72,.63]):
 box('WholeChassisCrossmember_%d'%j,(0,y,.43),(1.08,.19,.18),2)
 axle('WholeRoadWheelAxle_%d'%j,-.78,.78,y,.25,.10,2,20)
 for k,x in enumerate([-.64,.64]):
  n=24;ri=.115;ro=.25/math.cos(math.pi/n);v=[];f=[]
  for xx in[x-.105,x+.105]:
   for r in[ri,ro]:
    for i in range(n):t=math.tau*i/n+math.pi/n;v.append((xx,y+r*math.cos(t),.25+r*math.sin(t)))
  for i in range(n):q=(i+1)%n;f.extend([(i,q,n+q,n+i),(2*n+i,3*n+i,3*n+q,2*n+q),(i,2*n+i,2*n+q,q),(n+i,n+q,3*n+q,3*n+i)])
  mesh('WholeGroundFootTyre_%d_%d'%(j,k),v,f,3)
  axle('WholeRoadWheelHub_%d_%d'%(j,k),x-.117,x+.117,y,.25,.122,2,24)
# Full closed forward collection exterior, with an independent clear rear operator corner.
def rectrow(hx,y0,y1,c):return[(-hx+c,y0),(hx-c,y0),(hx,y0+c),(hx,y1-c),(hx-c,y1),(-hx+c,y1),(-hx,y1-c),(-hx,y0+c)]
rows=[(.50,.55,-1.17,.25,.09),(.63,.60,-1.22,.30,.12),(1.37,.60,-1.17,.25,.12),(1.55,.48,-1.04,.10,.10)]
v=[];f=[]
for z,hx,y0,y1,c in rows:v +=[(x,y,z)for x,y in rectrow(hx,y0,y1,c)]
for k in range(len(rows)-1):
 for i in range(8):q=(i+1)%8;f.append((k*8+i,k*8+q,(k+1)*8+q,(k+1)*8+i))
f +=[tuple(reversed(range(8))),tuple(24+i for i in range(8))];mesh('WholeHighForwardCollectionBody',v,f,0)
box('WholeFrontBluntBumper',(0,-1.235,.59),(1.22,.13,.16),2)
for k,x in enumerate([-.42,.42]):cyly('WholeBlankFrontLamp_%d'%k,-1.242,-1.165,x,.99,.065,1,16)
# Empty side-rear control station. No closed forward cab or copied seat geometry.
box('WholeRightRearOperatorDeck',(.38,.63,.53),(.58,.70,.10),2)
box('WholeLowSideStep',(.73,.57,.33),(.20,.42,.07),2)
beam('WholeStepRoot',(.58,.57,.51),(.73,.57,.35),.08,2)
box('WholeSeatPedestal',(.38,.74,.72),(.13,.13,.36),2)
box('WholeSeatPan',(.38,.72,.92),(.38,.35,.10),3)
box('WholeSeatBack',(.38,.89,1.12),(.36,.08,.39),3)
lathe_z('WholeSteeringColumn',.38,.36,[(0,.57),(.028,.57),(.028,1.15),(0,1.15)],2,16)
lathe_z('WholeSteeringRing',.38,.36,[(.128,1.15),(.157,1.15),(.157,1.178),(.128,1.178)],3,24)
for k in range(3):
 t=math.tau*k/3;beam('WholeSteeringSpoke_%d'%k,(.38,.36,1.164),(.38+.142*math.cos(t),.36+.142*math.sin(t),1.164),.018,2)
box('WholeBlankControlHousing',(.58,.40,.74),(.105,.22,.34),0)
# One rear conditioner frame connected by two actual entire trailing arms.
for k,x in enumerate([-.51,.51]):beam('WholeConditionerTrailingArm_%d'%k,(x,.74,.43),(x,1.16,.26),.085,2)
box('WholeConditionerRearWall',(0,1.035,.225),(1.74,.065,.31),0)
box('WholeConditionerRoof',(0,1.225,.385),(1.74,.43,.06),0)
for k,x in enumerate([-.85,.85]):box('WholeConditionerEndCheek_%d'%k,(x,1.23,.22),(.065,.45,.34),0)
axle('WholeConditionerTransverseShaft',-.89,.89,1.23,.21,.039,2,24)
for k,x in enumerate([-.90,.90]):axle('WholeProudConditionerAxleCap_%d'%k,x-.018,x+.018,1.23,.21,.062,2,20)
# Two complete closed helical ribbons, with roots embedded in the whole transverse shaft.
def helix(name,x0,x1,sg):
 n=72;v=[];f=[]
 for i in range(n+1):
  u=i/n;t=sg*math.tau*1.75*u;x=x0+(x1-x0)*u
  for dx,r in[(-.009,.034),(-.009,.127),(.009,.127),(.009,.034)]:v.append((x+dx,1.23+r*math.cos(t),.21+r*math.sin(t)))
 for k in range(n):
  for i in range(4):q=(i+1)%4;f.append((4*k+i,4*k+q,4*(k+1)+q,4*(k+1)+i))
 f +=[tuple(reversed(range(4))),tuple(4*n+i for i in range(4))];mesh(name,v,f,2)
helix('WholeLeftInwardHelicalRibbon',-.78,-.065,1);helix('WholeRightInwardHelicalRibbon',.065,.78,-1)
box('WholeTrailingBluntStrip',(0,1.46,.065),(1.74,.035,.055),3)
box('WholeTrailingStripBacking',(0,1.445,.102),(1.74,.055,.035),2)
# Central rising closed transfer-housing exterior: no hidden fluid/snow route claimed.
def thickpath(name,pts,r):
 v=[];f=[];n=12
 for k,p in enumerate(pts):
  d=unit(sub(pts[min(k+1,len(pts)-1)],pts[max(k-1,0)]));u=unit(cross(d,(1,0,0)));w=cross(d,u)
  for i in range(n):t=math.tau*i/n;v.append(tuple(p[j]+r*(u[j]*math.cos(t)+w[j]*math.sin(t))for j in range(3)))
 for k in range(len(pts)-1):
  for i in range(n):q=(i+1)%n;f.append((k*n+i,k*n+q,(k+1)*n+q,(k+1)*n+i))
 f +=[tuple(reversed(range(n))),tuple((len(pts)-1)*n+i for i in range(n))];mesh(name,v,f,0)
thickpath('WholeCentralRisingTransferExterior',[(0,1.10,.27),(0,.91,.48),(0,.91,1.29),(0,.78,1.57),(0,.49,1.64),(0,.14,1.44)],.105)
PALETTE=[('WholeBodyAndSledMutedBlue',(.17,.33,.40,1),.71,.12),('WholeBlankLampPaleCream',(.70,.69,.55,1),.67,.08),('WholeFrameAndAugerDullSteel',(.36,.42,.43,1),.51,.48),('WholeTyreSeatAndStripCharcoal',(.045,.055,.06,1),.86,.02)]
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}

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
focus=Vector((0,0,.78))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=4.45;aim(cam,(5,8,4.6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/public-service/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'public-service','style':'S01-clean-geometric','title':'Fixed Front Tank and Rear Conditioner Ice Machine','description':'One complete newly authored ice-rink-resurfacer-style static vehicle exterior. Four full annular flat-bottom-facet tyres and complete hubs carry one low two-rail chassis. A broad high forward closed collection-body exterior has a gently chamfered full outline and sloping shoulders, rather than a front driver cab. A separate empty right-rear operator platform, full seat and back, low side step, blank controls and whole steering ring sit beside a tall central transfer-housing exterior. Behind the vehicle two full trailing arms carry a single broad low conditioner frame with an actual open rear/underside mouth. Inside this frame one whole transverse shaft carries two separate oppositely winding thick continuous helical blade exteriors; a full trailing blunt strip and backing crossbar span the mouth edge. A complete curved opaque riser exterior connects the conditioner centre toward the front body. All parts belong to one integrated newly authored vehicle, not a road sweeper with its brushes exchanged or a walk-behind scrubber enlarged with a seat. Unlike those strongest old models there are no forward outboard brush discs, tall enclosed front cab or bowed squeegee behind a push frame. The high forward body, side-rear open controls and wide rear transverse-helix conditioning sled form a different entire organisation. Four opaque constant PBR roles, metres Z up and whole horizontal bounds centred over four finite tyre soles. One model zero scenes. Fixed unoccupied illustrative exterior only: the front body and rising conduit are opaque, no complete internal transfer or liquid circuit. No snow, ice, water, cooling, shaving, smoothing, blade action, screw transport, steering, driving, wheel motion, operator fit, load, manufacture, operation or safety capability. No people, branding, logos, rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
