import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='aviation-static-canard-wingtip-fin-pusher-01'
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

# Entire new compact canard airframe, no source aircraft mesh reuse.
ST=[(-1.48,.025,.035,.59),(-1.32,.075,.065,.60),(-.98,.15,.13,.64),(-.62,.20,.205,.68),(-.20,.225,.23,.68),(.25,.22,.19,.66),(.60,.18,.145,.65),(.92,.115,.095,.65),(1.06,.065,.055,.65)]
n=16;v=[(rx*math.cos(math.tau*j/n),y,z+rz*math.sin(math.tau*j/n))for y,rx,rz,z in ST for j in range(n)];f=[tuple(reversed(range(n))),tuple((len(ST)-1)*n+j for j in range(n))];fm=[0,0]
for k in range(len(ST)-1):
 for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));fm.append(2 if 2<=k<=4 and 1<=j<=6 else 0)
mesh('WholeCompactCockpitAndAftEngineBody',v,f,0)
FM['WholeCompactCockpitAndAftEngineBody']=[m for poly,m in zip(f,fm)for _ in range(len(poly)-2)]
FOIL=[(0,0),(.22,.034),(.6,.030),(1,0),(1,-.012),(.3,-.020)]
def wing(name,stations,mat):
 n=len(FOIL);v=[(x,lead+q*chord,z+h*scale)for x,lead,chord,z,scale in stations for q,h in FOIL];f=[tuple(reversed(range(n))),tuple((len(stations)-1)*n+j for j in range(n))]
 for k in range(len(stations)-1):
  for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
 mesh(name,v,f,mat)
wing('WholeSweptRearMainWing',[(-1.68,.69,.28,.62,.55),(-1.35,.48,.40,.60,.8),(-.22,.03,.66,.56,1),(0,.02,.68,.56,1),(.22,.03,.66,.56,1),(1.35,.48,.40,.60,.8),(1.68,.69,.28,.62,.55)],0)
wing('WholeForwardCanard',[(-.76,-.96,.17,.58,.55),(-.55,-1.04,.22,.58,.7),(0,-1.10,.26,.58,.8),(.55,-1.04,.22,.58,.7),(.76,-.96,.17,.58,.55)],1)
for side,sign in [('Left',-1),('Right',1)]:
 p=[(.68,.60),(.98,.60),(.94,1.06),(.82,1.03)];v=[(sign*1.63+dx,y,z)for dx in[-.018,.018]for y,z in p];mesh(side+'WholeWingtipVerticalFin',v,[(3,2,1,0),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4)for i in range(4)],1)
# Complete fixed rear propeller, not animated and not a flight-safety assertion.
beam('WholeAftPropellerHub',(0,1.02,.65),(0,1.19,.65),.075,3)
box('WholeFixedAftTwoBladePropeller',(0,1.16,.65),(.065,.032,.60),3)
def wheel(name,x,y,r,w):
 n=16;rr=r/math.cos(math.pi/n);v=[(x+dx,y+rr*math.sin(math.tau*j/n+math.pi/n),r+rr*math.cos(math.tau*j/n+math.pi/n))for dx in[-w/2,w/2]for j in range(n)];mesh(name,v,[tuple(reversed(range(n))),tuple(n+j for j in range(n))]+[(j,(j+1)%n,(j+1)%n+n,j+n)for j in range(n)],3)
for side,x in [('Left',-.50),('Right',.50)]:
 wheel(side+'WholeMainGroundTyre',x,.40,.12,.075)
 axle(side+'WholeMainAxle',x-.055,x+.055,.40,.12,.022,3)
 beam(side+'WholeSplayedGearLeg',(x,.40,.13),(x*.32,.31,.55),.040,3)
wheel('WholeNoseGroundTyre',0,-1.08,.095,.055)
axle('WholeNoseAxle',-.075,.075,-1.08,.095,.019,3)
beam('WholeNoseGearLeg',(.047,-1.08,.095),(.047,-1.01,.57),.031,3)
# Centre the complete actual envelope; soles remain at Z0.
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('Airframe_WarmIvory',(.72,.73,.64,1),.68,.05),('CanardAndFins_Ochre',(.53,.29,.065,1),.66,.05),('IntegralCanopy_OpaqueBlue',(.045,.12,.16,1),.28,.12),('GearAndPropeller_Charcoal',(.045,.052,.057,1),.55,.24)]
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
focus=Vector((0,0,.48))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=4.20;aim(cam,(3,-4,3.0));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/aviation/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'vehicles','assetKind':'prop','theme':'aviation','style':'S01-clean-geometric','title':'Static Canard Wingtip-Fin Pusher Airplane','description':'One newly authored complete static canard-layout land airplane exterior. The short pointed forebody broadens into a high cockpit crown and tapers directly into the rear engine body, with opaque canopy facets integral to that one surface. A full narrow forward canard precedes a separate broad swept rear main wing; two tall wingtip fins replace the conventional central aft tail and horizontal tailplane. A fixed rear two-blade propeller and complete hub sit behind the fuselage. Two splayed main gear legs and one forward leg join three flat-ground faceted tyres and complete axles. Entire new profiles, not moved old wing meshes, wheel-count change, recolour or scaled conventional plane, T-tail sailplane or stepped-hull flying boat. Sixteen closed named editable components, four constant opaque untextured PBR materials, metres, native Z up, front minus Y and whole horizontal-bounds-centred ground origin. One vehicle prop, zero scene. No internal cockpit, moving controls, flight, thrust, aerodynamic stability, centre of gravity, gear actuation, braking, compatible ground equipment, manufacture or airworthiness/safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
