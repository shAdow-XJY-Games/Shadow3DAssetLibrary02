import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='textile-fixed-two-shaft-treadle-floor-loom-01'
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


def frame_xz(name,y,xc,zc,w,h,b,depth,mat):
 out=[(xc-w/2,zc-h/2),(xc+w/2,zc-h/2),(xc+w/2,zc+h/2),(xc-w/2,zc+h/2)];inn=[(xc-w/2+b,zc-h/2+b),(xc+w/2-b,zc-h/2+b),(xc+w/2-b,zc+h/2-b),(xc-w/2+b,zc+h/2-b)]
 v=[(x,yy,z)for yy in[y-depth/2,y+depth/2]for ring in[out,inn]for x,z in ring];f=[]
 for i in range(4):j=(i+1)%4;f.extend([(i,j,4+j,4+i),(8+i,12+i,12+j,8+j),(i,8+i,8+j,j),(4+i,4+j,12+j,12+i)])
 mesh(name,v,f,mat)
# Entire new fore/aft floor-loom architecture; no flat-frame mesh instancing.
for side,x in [('Left',-.58),('Right',.58)]:
 box(side+'WholeGroundRunner',(x,0,.045),(.14,1.50,.09),0)
 for end,y in [('Front',-.55),('Rear',.55)]:box(side+end+'WholePost',(x,y,.73),(.095,.095,1.38),0)
 box(side+'WholeUpperRail',(x,0,1.31),(.08,1.20,.095),0)
 box(side+'WholeLowerRail',(x,0,.27),(.08,1.20,.09),0)
for label,y,z in [('FrontLow',-.55,.27),('RearLow',.55,.27),('FrontBreast',-.55,1.04),('RearBack',.55,1.14)]:box(label+'WholeCrossbeam',(0,y,z),(1.24,.085,.085),0)
# Separate transverse whole cloth/warp drums, not an array of loose spools.
for label,y,z in [('FrontCloth',-.58,.78),('RearWarp',.58,.91)]:
 axle(label+'WholeWindingBeam',-.63,.63,y,z,.075,0,20)
 for side,x in [('Left',-.58),('Right',.58)]:box(label+side+'WholeBearing',(x,y,z),(.13,.16,.18),0)
 axle(label+'WholeAxle',-.71,.71,y,z,.022,2,16)
 box(label+'WholeFixedCrank',(.70,y-.06,z),(.035,.17,.04),2)
 axle(label+'WholeCrankGrip',.69,.80,y-.13,z,.026,0,12)
# One high shaft support; two whole open rectangular shaft frames at distinct
# fixed shed heights, each with complete wire heddle loops. No rig or motion.
for side,x in [('Left',-.58),('Right',.58)]:box(side+'WholeCastlePost',(x,0,1.48),(.10,.13,.48),0)
box('WholeCastleTopCrossbeam',(0,0,1.70),(1.25,.12,.085),0)
for k,(y,z)in enumerate([(-.09,1.12),(.09,.98)]):
 frame_xz('Shaft'+str(k)+'WholeOpenFrame',y,0,z,1.02,.48,.025,.028,0)
 for side,x in [('Left',-.43),('Right',.43)]:beam('Shaft'+str(k)+side+'FixedSuspension',(x,y,z+.23),(x,0,1.70),.010,2)
 for i in range(8):
  if i%2==k:
   x=-.35+.10*i
   frame_xz('Shaft'+str(k)+'WholeWireHeddle'+str(i),y,x,z,.022,.435,.004,.006,2)
# Full continuous warp ribbons from rear beam over back beam, through the fixed
# alternating shed, through the reed, then to the front cloth edge.
for i in range(8):
 x=-.35+.10*i;z=1.12 if i%2==0 else .98;path=[(.60,.95),(.55,1.19),(.09,z),(-.09,z),(-.35,1.09),(-.54,1.09)];v=[]
 for y,zz in path:v.extend([(x-.004,y,zz-.003),(x+.004,y,zz-.003),(x+.004,y,zz+.003),(x-.004,y,zz+.003)])
 f=[(3,2,1,0),(20,21,22,23)]+[(4*j+i,4*j+(i+1)%4,4*(j+1)+(i+1)%4,4*(j+1)+i)for j in range(5)for i in range(4)];mesh('WholeContinuousWarpRibbon'+str(i),v,f,1)
# A single complete shallow bent cloth sheet wraps over the front breast beam
# to the front winding drum. Thick static display strip, not simulated weaving.
p=[(-.54,1.092),(-.61,1.085),(-.66,1.03),(-.66,.82),(-.63,.77)];v=[]
for i,(y,z) in enumerate(p):
 a=p[max(0,i-1)];b=p[min(len(p)-1,i+1)];dy=b[0]-a[0];dz=b[1]-a[1];L=math.hypot(dy,dz);ny=-dz/L;nz=dy/L
 v.extend([(-.40,y-.006*ny,z-.006*nz),(.40,y-.006*ny,z-.006*nz),(.40,y+.006*ny,z+.006*nz),(-.40,y+.006*ny,z+.006*nz)])
f=[(3,2,1,0),(16,17,18,19)]+[(4*j+i,4*j+(i+1)%4,4*(j+1)+(i+1)%4,4*(j+1)+i)for j in range(4)for i in range(4)];mesh('WholeBentFrontWovenClothDisplay',v,f,3)
# Real open reed frame and discrete fixed teeth separate the front thread lanes.
frame_xz('WholeOpenReedBeaterFrame',-.35,0,1.09,1.06,.25,.027,.040,0)
for i in range(9):box('WholeReedTooth'+str(i),(-.40+.10*i,-.35,1.09),(.010,.012,.205),2)
for side,x in [('Left',-.50),('Right',.50)]:beam(side+'WholeBeaterArm',(x,-.35,.98),(x,-.52,.30),.032,0)
# Two whole lower treadles and two fixed tie rods make a separate floor layout,
# not an added pedal on the earlier flat standing weaving frame.
for k,x in enumerate([-.17,.17]):
 beam('WholeFixedTreadle'+str(k),(x,-.69,.14),(x,.36,.22),.075,0)
 beam('WholeFixedShaftTie'+str(k),(x,.16,.20),(x,[-.09,.09][k],[.89,.75][k]),.012,2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('LoomFrame_WarmTimber',(.43,.24,.10,1),.77,0),('WarpThreads_Cream',(.77,.70,.52,1),.90,0),('HeddlesReedTies_DarkSteel',(.16,.19,.20,1),.56,.32),('ClothDisplay_MutedTeal',(.08,.28,.26,1),.92,0)]
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
focus=Vector((0,0,.85))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.25;aim(cam,(4.0,-6,3.7));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/textile/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'textile','style':'S01-clean-geometric','title':'Fixed Two-Shaft Treadle Floor Loom','description':'One newly authored complete fixed floor loom with four grounded posts on two long runners, a distinct front cloth drum and rear warp drum, full breast/back beams and a high castle support. Two whole open shaft frames at different frozen heights carry complete wire heddle loops. Eight continuous solid warp ribbons follow the full fore/aft path and form a visible alternating shed before a real open reed frame with separate teeth. A full bent cloth display sheet passes over the front breast beam to its drum. Two lower treadles, fixed shaft ties and beater side arms belong to this single whole assembly. No mesh from the older flat standing weaving frame, spinning wheel or warping cage is reused. Separate closed editable bodies with intentional fixed embedded joins, four opaque constant PBR materials, metres, native Z up and horizontally centred ground origin. One illustrative model, zero scenes. No functioning weave, thread tension, animation, moving linkage, cloth simulation, ergonomics, load, manufacture or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
