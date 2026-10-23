import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='aviation-stepped-hull-pylon-engine-flyingboat-01'
G={};FM={};LINKS=[]
PALETTE=[('Flyingboat_Ivory',(.67,.70,.65,1),.65,.08),('Flyingboat_DeepTeal',(.07,.22,.24,1),.55,.15),('Flyingboat_Canopy',(.035,.095,.12,1),.22,.12),('Flyingboat_Metal',(.24,.27,.28,1),.43,.62)]
def emit(name,v,polys,mat=0,pm=None):
 fs=[];ms=[]
 for k,p in enumerate(polys):
  for j in range(1,len(p)-1):fs.append((p[0],p[j],p[j+1]));ms.append(pm[k] if pm else mat)
 volume=sum(sum(v[a][k]*(v[b][(k+1)%3]*v[c][(k+2)%3]-v[b][(k+2)%3]*v[c][(k+1)%3])for k in range(3))for a,b,c in fs)/6
 if volume<0:fs=[(a,c,b)for a,b,c in fs]
 G[name]=(v,fs,mat);FM[name]=ms;return name
# New closed boat-bottom fuselage: asymmetric section, real chines, flat narrow
# keel sole and a discrete aft step, opaque cockpit region in the same shell.
ST=[(-3.2,.07,.37,.50),(-2.8,.34,.15,.78),(-2.05,.56,.00,1.12),(-1.2,.61,.00,1.27),(-.25,.58,.00,1.20),(.22,.53,.00,1.12),(.28,.52,.24,1.11),(1.2,.40,.32,.94),(2.15,.23,.51,.78),(3.1,.055,.62,.71)]
v=[]
for y,w,b,t in ST:
 v.extend([(-w*.16,y,b),(w*.16,y,b),(w,y,b+(t-b)*.24),(w,y,b+(t-b)*.72),(w*.52,y,t),(-w*.52,y,t),(-w,y,b+(t-b)*.72),(-w,y,b+(t-b)*.24)])
n=8;f=[tuple(reversed(range(n))),tuple((len(ST)-1)*n+i for i in range(n))];m=[1,1]
for k in range(len(ST)-1):
 for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));m.append(2 if k in [1,2,3]and j in [3,4,5]else 1 if j in [0,1,7]else 0)
emit('ContinuousSteppedBoatHull',v,f,0,m)
def box(name,c,s,mat=0):
 x,y,z=c;a,b,d=[q/2 for q in s];v=[(x+i*a,y+j*b,z+k*d)for k in [-1,1]for j in [-1,1]for i in [-1,1]]
 return emit(name,v,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],mat)
def rod(name,a,b,r,mat=3,n=8):
 d=[b[i]-a[i]for i in range(3)];l=math.sqrt(sum(x*x for x in d));d=[x/l for x in d];ref=[0,0,1] if abs(d[2])<.9 else [0,1,0]
 u=[d[1]*ref[2]-d[2]*ref[1],d[2]*ref[0]-d[0]*ref[2],d[0]*ref[1]-d[1]*ref[0]];l=math.sqrt(sum(x*x for x in u));u=[x/l for x in u];w=[d[1]*u[2]-d[2]*u[1],d[2]*u[0]-d[0]*u[2],d[0]*u[1]-d[1]*u[0]]
 v=[tuple(p[k]+r*(u[k]*math.cos(i*math.tau/n)+w[k]*math.sin(i*math.tau/n))for k in range(3))for p in [a,b]for i in range(n)]
 return emit(name,v,[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],mat)
# Full thick high wing, central support from actual boat hull, not repositioned
# previous aircraft mesh. Finite leading and trailing edges remain editable.
FOIL=[(0,0),(.15,.075),(.45,.10),(1,.025),(1,-.025),(.45,-.055),(.15,-.045)]
def wing(name,stations,mat=0):
 v=[(x,lead+q*chord,z+h)for x,lead,chord,z in stations for q,h in FOIL];n=len(FOIL)
 return emit(name,v,[tuple(reversed(range(n))),tuple((len(stations)-1)*n+i for i in range(n))]+[(k*n+i,k*n+(i+1)%n,(k+1)*n+(i+1)%n,(k+1)*n+i)for k in range(len(stations)-1)for i in range(n)],mat)
box('HullToHighWingPedestal',(0,-.12,1.4),(.32,.65,.64),1)
wing('ContinuousHighMainWing',[(-4.05,-.38,.62,1.72),(-3.2,-.63,1.05,1.69),(0,-.82,1.40,1.65),(3.2,-.63,1.05,1.69),(4.05,-.38,.62,1.72)])
# Pylon-mounted forward-facing engine clear above cabin and wing.
box('AboveWingEnginePylon',(0,-.07,1.93),(.16,.35,.53),3)
rod('CompleteRaisedEngineNacelle',(0,-.86,2.20),(0,.57,2.20),.23,1,12)
rod('PropellerHub',(0,-1.02,2.20),(0,-.80,2.20),.085,3,12)
box('FixedVerticalTwoBladePropeller',(0,-.98,2.20),(.10,.055,1.20),3)
# Genuine underwing outrigger floats with tapered boat-shaped ends, each two
# whole struts. No landing wheels and no buoyancy/flight claim.
for sign,side in [(-1,'Left'),(1,'Right')]:
 x=sign*2.82;ss=[(-1.20,.025,.52),(-.85,.16,.42),(.55,.16,.42),(.95,.025,.55)];vv=[]
 for y,w,z in ss:vv.extend([(x-w,y,z),(x+w,y,z),(x+w,y,z+.20),(x-w,y,z+.20)])
 emit(side+'OutriggerFloat',vv,[(3,2,1,0),tuple(12+i for i in range(4))]+[(k*4+i,k*4+(i+1)%4,(k+1)*4+(i+1)%4,(k+1)*4+i)for k in range(3)for i in range(4)],1)
 for label,y in [('Fore',-.60),('Aft',.28)]:rod(side+label+'FloatStrut',(x,y,.56),(sign*2.60,y,1.73),.045)
 rod(side+'WingBrace',(sign*.40,-.12,.90),(sign*2.1,-.12,1.69),.045)
# Integral-style dorsal tail root and low rear stabilizer, separate complete
# connected pieces rather than the old sailplane's high T-tail.
v=[(x,y,z)for x in [-.065,.065]for y,z in [(2.02,.68),(3.13,.66),(2.93,1.98),(2.48,1.75)]]
emit('SweptDorsalTailFin',v,[(3,2,1,0),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4)for i in range(4)])
wing('RearLowHorizontalTail',[(-1.15,2.47,.50,1.04),(0,2.24,.83,1.04),(1.15,2.47,.50,1.04)])
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
focus=Vector((0,0,1.05))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=11.6;aim(cam,(8,-10,6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/aviation/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'vehicles','assetKind':'prop','theme':'aviation','style':'S01-clean-geometric','title':'Stepped-Hull Pylon-Engine Flying Boat','description':'One original static low-poly flying-boat exterior, newly authored as a continuous closed boat-bottom fuselage with narrow finite keel sole, real chines and a raised aft bottom step; opaque cockpit material belongs to the hull surface. One complete thick high main wing on a hull pedestal, a distinct above-wing engine pylon with nacelle and fixed two-blade propeller, two complete underwing outrigger floats with paired struts, wing braces, a swept dorsal fin and low horizontal tail. Seventeen complete closed connected-by-overlap components; no old aircraft or boat geometry imported, no scaled wing or wheel-count variant. One whole vehicle prop, source Z-up metres, ground datum at the hull keel. Pose is a dry static visual display, not a deployed landing-gear or flotation simulation. No moving controls, open cabin, wheel system, textures, pilots or fuel lines. No flight, buoyancy, propulsion, aerodynamics, functional sampling, production engineering or aviation safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
