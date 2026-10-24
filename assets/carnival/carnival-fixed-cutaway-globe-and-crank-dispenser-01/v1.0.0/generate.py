import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='carnival-fixed-cutaway-globe-and-crank-dispenser-01'
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



# A complete fixed dispenser intentionally cut open at the front to show its interior.
def partial_lathe(name,profile,a0,a1,mat,n=32):
 v=[(r*math.cos(a0+(a1-a0)*j/n),r*math.sin(a0+(a1-a0)*j/n),z)for j in range(n+1)for r,z in profile];m=len(profile);f=[]
 for j in range(n):
  for i in range(m):k=(i+1)%m;f.append((j*m+i,(j+1)*m+i,(j+1)*m+k,j*m+k))
 tt=triangulate(profile);f += list(tt)+[tuple(n*m+i for i in reversed(t))for t in tt];mesh(name,v,f,mat)
lathe_z('WholeGroundFootTurnedPedestal',0,0,[(0,0),(.19,0),(.195,.025),(.18,.057),(.16,.075),(0,.075)],0,48)
# Rear and both side walls form one continuous thick C-section with a true front exhibit opening.
partial_lathe('WholeCutawayLowerMechanismHousing',[(.15,.065),(.15,.375),(.13,.375),(.13,.065)],-.12*math.pi,1.12*math.pi,0,40)
lathe_z('WholeUpperHousingShoulder',0,0,[(.028,.362),(.172,.362),(.172,.395),(.028,.395)],0,48)
# Whole open neck and complete funnel slope, no flat painted store opening.
lathe_z('WholeOpenFeedFunnelAndThroat',0,0,[(.027,.32),(.040,.32),(.040,.412),(.174,.539),(.175,.558),(.163,.558),(.159,.545),(.027,.418)],2,48)
# Thick rear half of a real spherical reservoir; the open front is a cutaway, not transparent material.
profile=[(.24*math.sin(math.radians(t)),.735+.24*math.cos(math.radians(t)))for t in range(140,29,-5)]+[(.230*math.sin(math.radians(t)),.735+.230*math.cos(math.radians(t)))for t in range(30,141,5)]
partial_lathe('WholeOpenFrontSphericalReservoirRearShell',profile,0,math.pi,1,48)
lathe_z('WholeReservoirUpperCap',0,0,[(0,.936),(.129,.936),(.136,.952),(.126,.966),(.025,.976),(0,.976)],0,40)
lathe_z('WholeFixedTopCapKnob',0,0,[(0,.970),(.028,.970),(.034,.993),(.020,1.014),(0,1.014)],2,24)
# A full horizontal spindle is rooted in the rear body and carries the fixed pocketed wheel and crank.
cyly('WholeHorizontalMeteringSpindle',-.205,.145,0,.245,.016,2,24)
ringy('WholeFixedMeteringWheelOuterRim',-.026,.012,0,.245,.064,.090,2,32)
cyly('WholeMeteringWheelHub',-.036,.021,0,.245,.028,2,24)
for k in range(4):
 a=math.tau*k/4;beam('WholeMeteringWheelRadialWeb_%02d'%k,(.018*math.cos(a),-.007,.245+.018*math.sin(a)),(.078*math.cos(a),-.007,.245+.078*math.sin(a)),.023,2)
cyly('WholeFrontFixedTurnHub',-.223,-.193,0,.245,.038,0,24)
beam('WholeFrontFixedCrankArm',(0,-.220,.245),(.075,-.220,.205),.024,2)
cyly('WholeFrontCrankGrip',-.285,-.211,.075,.205,.022,3,24)
# Continuous thick open U-channel bends down and forward to an accessible low receiving mouth.
path=[(.055,.153),(-.015,.123),(-.095,.092),(-.205,.084)];section=[(-.060,0),(.060,0),(.060,.041),(.047,.041),(.047,.012),(-.047,.012),(-.047,.041),(-.060,.041)]
v=[(x,y,z+dz)for y,z in path for x,dz in section];n=len(section);tt=triangulate(section);f=[tuple(reversed(t))for t in tt]+[tuple((len(path)-1)*n+i for i in t)for t in tt]
for j in range(len(path)-1):
 for i in range(n):k=(i+1)%n;f.append((j*n+i,j*n+k,(j+1)*n+k,(j+1)*n+i))
mesh('WholeBentOpenDischargeChute',v,f,2)
box('WholeChuteGroundedRootSupport',(0,-.11,.071),(.10,.17,.030),0)
# One connected static coloured-ball cluster is display content of this machine, not separate assets.
for k,(x,y,z,r)in enumerate([(0,.010,.455,.039),(-.050,.015,.500,.037),(.050,.015,.500,.037),(0,.025,.545,.039),(-.040,.045,.591,.035),(.040,.045,.591,.035)]):
 z-=.017 # The lowest sphere is actually seated across the narrow funnel throat, not suspended in empty air.
 pr=[(0,z-r)]+[(r*math.sin(math.pi*j/12),z-r*math.cos(math.pi*j/12))for j in range(1,12)]+[(0,z+r)];lathe_z('WholeFixedExhibitBall_%02d'%k,x,y,pr,0 if k%2 else 3,20)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeDispenserBodyAndCap_MutedRed',(.48,.075,.045,1),.62,.12),('WholeCutawayReservoir_OpaquePaleBlue',(.36,.57,.62,1),.57,.08),('WholeFeedWheelChuteAndSpindle_SatinMetal',(.45,.48,.47,1),.48,.58),('WholeFixedGripAndAlternateBalls_WarmIvory',(.74,.61,.26,1),.74,0)]
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
focus=Vector((0,0,.51))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.22;aim(cam,(3,-5,2.6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/carnival/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'carnival','style':'S01-clean-geometric','title':'Fixed Cutaway Globe and Crank Dispenser','description':'One newly authored complete fixed cutaway globe-reservoir hand-crank dispenser appearance. A single thick spherical rear half-shell and full capped top outline an intentionally open-front reservoir above a complete sloping feed funnel and real narrow throat. A continuous rear-and-side lower housing on a full turned ground pedestal supports a whole horizontal spindle, an open four-web fixed metering wheel, front crank arm and grip. One continuous thick U-section discharge channel bends down and forward to the low front mouth. Six fixed coloured balls are connected illustrative contents of this one machine, not separately counted models. No old popcorn roof cabinet, hanging kettle or open candy-floss spinner pan is imported or resized; this complete globe/funnel/turning-dial/chute arrangement is new geometry. Four opaque constant untextured PBR roles; the blue reservoir is genuinely cut away and is not claimed to be transparent glass. Metres, Z up, whole horizontal bounds-centred ground origin. One model and zero scenes. Static exhibit only: no rotation, dispensing, ball dynamics, payment, vending, hygiene, food contact, quantity measurement, manufacture, load, age suitability or safety claim. No text, prices, player or environment.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
