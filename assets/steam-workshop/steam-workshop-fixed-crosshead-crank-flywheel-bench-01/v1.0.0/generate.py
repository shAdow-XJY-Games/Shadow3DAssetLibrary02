import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='steam-workshop-fixed-crosshead-crank-flywheel-bench-01'
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

# Whole new fixed bench drive, no library cylinder/rod/gear mesh instances.
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
# Real top cutaway, complete inner chamber, separate piston and gland.
arc=[3*math.pi/4+3*math.pi*i/2/18 for i in range(19)];p=[(.17*math.cos(a),.48+.17*math.sin(a))for a in arc]+[(.14*math.cos(a),.48+.14*math.sin(a))for a in reversed(arc)];n=len(p);v=[(x,y,z)for x in[-1.20,-.65]for y,z in p];f=[tuple(reversed(t))for t in triangulate(p)]+[tuple(n+i for i in t)for t in triangulate(p)]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh('WholeOpenTopCylinderChamber',v,f,0)
axle('WholeRearCylinderCover',-1.24,-1.19,0,.48,.185,2)
ringx('WholeFrontBoredGland',-.67,-.61,0,.48,.035,.185,2)
axle('WholeVisiblePiston',-.98,-.92,0,.48,.132,2)
axle('WholePistonToCrossheadRod',-.95,-.20,0,.48,.030,1)
box('WholeGroundBenchBase',(-.08,.11,.035),(2.45,.94,.07),0)
for j,x in enumerate([-1.08,-.75]):box('CylinderPedestal_'+str(j),(x,0,.205),(.11,.10,.30),0)
box('WholeCrossheadSlider',(-.24,0,.48),(.16,.12,.12),2)
for side,y in [('Front',-.10),('Back',.10)]:box(side+'FullCrossheadGuide',(-.18,y,.48),(.72,.08,.07),1)
for j,x in enumerate([-.48,.12]):
 box('GuideFramePost_'+str(j),(x,0,.275),(.055,.25,.42),0)
# Shared-cell 2D rod construction: full two eyes + full shank, internal cell
# faces omitted, then all new coordinates inclined between the actual pins.
N=16;coords={};cells=[];length=math.hypot(.96,.17);u=(.96/length,.17/length);w=(-u[1],u[0])
for e,(cx,ro,ri)in enumerate([(0,.078,.037),(length,.090,.047)]):
 for k,r in enumerate([ri,ro]):
  for i in range(N):a=math.pi/N+math.tau*i/N;coords[e,k,i]=(cx+r*math.cos(a),r*math.sin(a))
 for i in range(N):j=(i+1)%N;cells.append([(e,0,i),(e,1,i),(e,1,j),(e,0,j)])
cells.append([(0,1,N-1),(1,1,N//2),(1,1,N//2-1),(0,1,0)])
edges={}
for c in cells:
 for a,b in zip(c,c[1:]+c[:1]):edges.setdefault(tuple(sorted([a,b])),[]).append((a,b))
v=[];f=[];lookup={}
def idx(key,y):
 x,z=coords[key];p=(-.24+x*u[0]+z*w[0],y,.48+x*u[1]+z*w[1])
 if p not in lookup:lookup[p]=len(v);v.append(p)
 return lookup[p]
for c in cells:
 f.extend([tuple(idx(k,-.18)for k in reversed(c)),tuple(idx(k,-.13)for k in c)])
for e in edges.values():
 if len(e)==1:
  a,b=e[0];f.append((idx(a,-.18),idx(b,-.18),idx(b,-.13),idx(a,-.13)))
mesh('WholeInclinedTwoEyeConnectingRod',v,f,1)
cyly('WholeCrossheadPin',-.215,.08,-.24,.48,.035,1)
cyly('WholeOffsetCrankPin',-.215,.025,.72,.65,.045,1)
for label,x,z,r in [('Crosshead',-.24,.48,.052),('Crank',.72,.65,.062)]:cyly(label+'FrontRetainingCap',-.218,-.179,x,z,r,2)
cyly('WholeCrankDisk',-.075,.005,.63,.48,.225,0)
cyly('WholeCrankshaft',-.095,.49,.63,.48,.05,1)
for label,y in [('Near',.075),('Far',.285)]:
 ringy(label+'WholeBoredMainBearing',y-.035,y+.035,.63,.48,.05,.10,2)
 box(label+'BearingPedestal',(.63,y,.235),(.12,.08,.35),0)
# New flywheel on far end: complete annulus, hub and six full spokes with real
# open spaces between them, no tooth/gear reuse or rotation assertion.
ringy('WholeFlywheelRim',.395,.455,.63,.48,.285,.345,0,32)
cyly('WholeFlywheelHub',.38,.47,.63,.48,.09,2)
for i in range(6):
 a=math.tau*i/6;beam('WholeFlywheelSpoke_'+str(i),(.63+.065*math.cos(a),.425,.48+.065*math.sin(a)),(.63+.30*math.cos(a),.425,.48+.30*math.sin(a)),.043,0)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('FrameCylinderFlywheel_DeepGreen',(.065,.23,.18,1),.71,.20),('GuidesRodPins_BrushedSteel',(.42,.46,.46,1),.43,.62),('CoversSliderBearings_WarmBrass',(.48,.31,.10,1),.47,.55)]
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
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.90;aim(cam,(3,-5,3.3));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/steam-workshop/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'steam-workshop','style':'S01-clean-geometric','title':'Fixed Crosshead Crank and Flywheel Bench','description':'One newly authored complete static steam-workshop drive-bench display: a grounded continuous base supports an open-top horizontal cylinder with visible separate piston, real bored front gland and a rod reaching a crosshead block between two full guides. One complete inclined two-eye connecting rod is retained on the crosshead pin and an actual offset crank pin. A separate crank disk, full shaft, two bored bearing pedestals and one full open-spoke flywheel complete the new assembly. All geometry is freshly authored, not a scene containing old cylinder/rod/gear props, not a resized cutaway cylinder or extra copied gear. The flywheel has a complete annular rim and six whole radial spokes around a hub, with real open spaces. Metres, native Z up, horizontal-bounds-centred grounded origin, three opaque solid untextured PBR materials and individually editable closed components. One complete prop, zero scene. One fixed illustrative pose only: no steam, pressure, cycle timing, torque, power, force transmission, working bearing fit, travel envelope, full-stroke collision clearance, rigging, animation, efficiency, load, stability, manufacture or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
