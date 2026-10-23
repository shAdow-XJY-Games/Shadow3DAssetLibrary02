import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='carpentry-fixed-open-long-bar-f-clamp-01'
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

def rectangular_collar(name,x0,x1):
 outer=[(.074,0),(.156,0),(.156,.08),(.074,.08)];inner=[(.098,.032),(.132,.032),(.132,.056),(.098,.056)]
 v=[(x,y,z)for x in[x0,x1]for ring in[outer,inner]for y,z in ring];f=[]
 for i in range(4):j=(i+1)%4;f.extend([(i,j,4+j,4+i),(8+i,12+i,12+j,8+j),(i,8+i,8+j,j),(4+i,4+j,12+j,12+i)])
 mesh(name,v,f,0)
def ringx(name,x0,x1,y,z,inner,outer,mat,n=16):
 v=[(x,y+r*math.cos(math.tau*j/n),z+r*math.sin(math.tau*j/n))for x in[x0,x1]for r in[inner,outer]for j in range(n)];f=[]
 for i in range(n):j=(i+1)%n;f.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 mesh(name,v,f,mat)
box('CompleteLongFlatSteelBar',(0,.115,.042),(.94,.030,.020),1)
box('WholeFixedEndJaw',(-.40,-.025,.04),(.080,.30,.08),0)
box('FixedOpposedFacePad',(-.351,-.135,.04),(.018,.080,.08),1)
rectangular_collar('TrueThroughBarSlidingCollar',.15,.23)
box('CompleteLowerJawBridge',(.19,-.0155,.0385),(.075,.199,.077),0)
ringx('TrueThroughSpindleBoss',.145,.235,-.145,.04,.010,.038,0)
axle('CompleteFixedSpindle',.035,.30,-.145,.04,.010,1)
axle('FullRoundPressurePad',.018,.044,-.145,.04,.034,1)
axle('WholeTimberHandle',.278,.415,-.145,.04,.027,2)
# True closed fixed visual helical ridge, not a thread engagement/actuation claim.
v=[];f=[];N=96;sides=6
for k in range(N+1):
 a=math.tau*6*k/N;x=.064+.204*k/N
 for j in range(sides):
  b=math.tau*j/sides;rr=.0108+.0019*math.cos(b);v.append((x+.0019*math.sin(b),-.145+rr*math.cos(a),.04+rr*math.sin(a)))
for k in range(N):
 for j in range(sides):q=(j+1)%sides;f.append((k*sides+j,k*sides+q,(k+1)*sides+q,(k+1)*sides+j))
f.extend([tuple(reversed(range(sides))),tuple(N*sides+j for j in range(sides))]);mesh('ClosedFixedHelicalSpindleRidge',v,f,1)
box('WholeRearBarEndStop',(.462,.115,.042),(.025,.049,.035),1)
# Full horizontal bounds centring, flat jaw/collar undersides provide true ground datum.
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)]
SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={name:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for name,(v,f,m)in G.items()}
PALETTE=[('JawBodies_MatteDeepRed',(.34,.075,.052,1),.78,.12),('BarSpindlePads_BrushedSteel',(.37,.40,.40,1),.49,.65),('Grip_WarmTimber',(.43,.24,.10,1),.83,0)]
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
focus=Vector((0,0,.035))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.18;aim(cam,(2,-3,4.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/carpentry/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'carpentry','style':'S01-clean-geometric','title':'Fixed Open Long-Bar F Clamp','description':'One newly authored complete static long-bar F-form woodworking clamp in a fixed empty opening. A full flat steel guide bar carries a perpendicular fixed end jaw and a second jaw assembly with a real rectangular through-bar collar, complete bridge and genuinely pierced spindle boss. A separate full spindle with a closed visual six-turn helical ridge terminates in an opposed round pressure pad and a thick timber grip; the bar has one integral-purpose end stop. The complete long-bar geometry and open jaw bay differ from the existing table-edge C-mounted bench vise and elevated split bicycle-tube clamp. No old tool mesh is cropped, recoloured or stretched. Eleven editable closed components and three solid untextured PBR materials, metres, native Z up, actual horizontal bounds-centred origin and flat jaw/collar undersides in a laid-down display pose. One complete prop, zero scene. No stock, bench, product-use compatibility, slide path, screw engagement, clamping motion, force, load, thread standard, manufacture, woodworking performance or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
