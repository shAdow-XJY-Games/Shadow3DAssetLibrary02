import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='museum-fictional-quadruped-skeleton-mount-01'
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



def sweep(name,path,radii,mat,n=8):
 vs=[]
 for j,p in enumerate(path):
  w=unit(sub(path[min(j+1,len(path)-1)],path[max(j-1,0)]));ref=(0,1,0)if abs(w[1])<.85 else(1,0,0);u=unit(cross(w,ref));v=cross(w,u)
  for i in range(n):vs.append(tuple(p[k]+radii[j]*(math.cos(math.tau*i/n)*u[k]+math.sin(math.tau*i/n)*v[k])for k in range(3)))
 fs=[tuple(reversed(range(n))),tuple((len(path)-1)*n+i for i in range(n))]+[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i)for j in range(len(path)-1)for i in range(n)];mesh(name,vs,fs,mat)
def bone(name,a,b,r):
 ts=[0,.06,.18,.38,.62,.82,.94,1];scale=[1.1,1.35,1.0,.72,.72,1.0,1.35,1.1];sweep(name,[tuple(a[k]+t*(b[k]-a[k])for k in range(3))for t in ts],[r*q for q in scale],0)
def ring_y(name,y0,y1,outer,inner,mat):
 n=len(outer);v=[(x,y,z)for y in[y0,y1]for p in[outer,inner]for x,z in p];f=[]
 for i in range(n):j=(i+1)%n;f.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 mesh(name,v,f,mat)
# One original dedicated low base and two slender fixed exhibit posts; not an
# old exhibit plinth or a separately counted room or specimen collection.
box('WholeDedicatedGroundBase',(0,0,.055),(.96,2.75,.11),1)
for j,y in enumerate([-.38,.53]):
 beam('WholeFixedMountPost'+str(j),(0,y,.08),(0,y,1.27),.035,2)
 box('WholeSpinalSaddle'+str(j),(0,y,1.29),(.17,.075,.18 if j==0 else .075),2)
# New axial backbone with integrated joint-like swells, upper neck and tapered
# rear caudal chain. Four limbs and girdles create a true terrestrial whole.
path=[];rad=[]
for j in range(7):
 y=-.58+j*.20;z=1.43-.09*(j/6)
 for dy,r in [(-.07,.040),(-.035,.064),(.035,.064),(.07,.040)]:path.append((0,y+dy,z));rad.append(r)
sweep('WholeContinuousSwelledSpine',path,rad,0)
sweep('WholeAscendingNeck',[(0,-.64,1.42),(0,-.82,1.48),(0,-.98,1.63),(0,-1.12,1.65)],[.055,.060,.056,.055],0)
sweep('WholeTaperedCaudalChain',[(0,.66,1.34),(0,.88,1.29),(0,1.13,1.18),(0,1.35,1.02)],[.058,.045,.029,.012],0)
# Whole thick skull ring, long low muzzle and real transverse eye aperture.
outer=[(-1.10,1.50),(-1.10,1.76),(-1.23,1.83),(-1.40,1.80),(-1.68,1.65),(-1.72,1.51),(-1.47,1.49),(-1.25,1.49)];inner=[(-1.24+.085*math.cos(math.tau*i/8),1.68+.080*math.sin(math.tau*i/8))for i in range(8)]
# Match the radial order of aperture to each outer vertex, rather than twist it.
inner=[(-1.27+.085*(y+1.27)/math.hypot(y+1.27,z-1.67),1.67+.085*(z-1.67)/math.hypot(y+1.27,z-1.67))for y,z in outer]
n=8;v=[(x,y,z)for x in[-.11,.11]for p in[outer,inner]for y,z in p];f=[]
for i in range(n):j=(i+1)%n;f.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
mesh('WholeThickLongMuzzleOrbitalSkull',v,f,0)
# Two complete lower jaw branches meet in the front chin, leaving a real open
# mouth gap under the upper muzzle. Frozen geometry, not an operating jaw.
for side,x in [('Left',-.083),('Right',.083)]:sweep(side+'WholeLowerJawBranch',[(x,-1.15,1.53),(x,-1.24,1.39),(x,-1.55,1.38),(0,-1.69,1.43)],[.030,.025,.021,.025],0)
# Paired tapered arched ribs enclose a real open three-dimensional thorax.
for j,y in enumerate([-.48,-.27,-.06,.15,.36]):
 scale=[.82,1.,1.04,.94,.75][j]
 for side,sgn in [('Left',-1),('Right',1)]:
  pts=[(sgn*x*scale,y,1.40+(z-1.40)*scale)for x,z in[(.025,1.43),(.18,1.40),(.30,1.29),(.32,1.12),(.23,.98),(.03,.96)]]
  sweep(side+'WholeArchedRib'+str(j),pts,[.024,.024,.022,.020,.018,.018],0)
sweep('WholeLongSternum',[(0,-.50,1.02),(0,-.27,.96),(0,.02,.95),(0,.35,1.06)],[.030,.030,.028,.024],0)
# One thick open pelvis ring links the axial spine to both hind limb roots.
outer=[(.29*math.cos(math.tau*i/12),1.22+.21*math.sin(math.tau*i/12))for i in range(12)];inner=[(.20*math.cos(math.tau*i/12),1.22+.12*math.sin(math.tau*i/12))for i in range(12)];ring_y('WholeOpenPelvicGirdle',.52,.66,outer,inner,0)
for side,sgn in [('Left',-1),('Right',1)]:
 # Shoulder blade is a whole tapered solid plate, not an isolated detached disc.
 v=[(sgn*x,y,z)for x in[.24,.285]for y,z in[(-.58,1.44),(-.20,1.34),(-.43,1.12)]];mesh(side+'WholeTriangularScapula',v,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],0)
 bone(side+'WholeUpperForeLimb',(sgn*.265,-.43,1.17),(sgn*.31,-.35,.76),.046)
 bone(side+'WholeLowerForeLimb',(sgn*.31,-.35,.76),(sgn*.32,-.54,.26),.031)
 bone(side+'WholeForeFoot',(sgn*.32,-.54,.25),(sgn*.32,-.77,.19),.042)
 bone(side+'WholeHindThigh',(sgn*.25,.59,1.21),(sgn*.37,.36,.79),.050)
 bone(side+'WholeHindShank',(sgn*.37,.36,.79),(sgn*.34,.76,.31),.033)
 bone(side+'WholeHindFoot',(sgn*.34,.76,.29),(sgn*.34,.48,.19),.044)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('FictionalBone_WarmIvory',(.73,.66,.51,1),.83,0),('DedicatedBase_DeepTeal',(.035,.11,.13,1),.74,.05),('FixedExhibitPosts_DarkBronze',(.20,.18,.12,1),.58,.42)]
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
focus=Vector((0,0,.93))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.65;aim(cam,(6,-4,3.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/museum/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'museum','style':'S01-clean-geometric','title':'Fictional Quadruped Skeleton Display Mount','description':'One complete newly authored fictional four-limbed skeletal exhibit on its dedicated low base and two fixed posts. A continuous swelled spine connects an ascending neck, thick long-muzzle skull with a true orbital opening, paired fixed jaw branches and a tapered caudal chain. Five complete rib pairs form an open three-dimensional thorax, with a separate full sternum, shoulder plates and one real open pelvic girdle. Four complete segmented limbs include swollen-ended upper/lower bones and elongated foot bones. This is a whole terrestrial quadruped display architecture, not the earlier fish skeleton stretched or supplied with additional fins, and not a live deer mesh made thin. All numeric geometry is new; no old specimen, plinth, room, label or mesh instance. Separate closed editable solid parts with intentional fixed embedded joins, three constant opaque PBR materials, metres, native Z up and bounds-centred ground origin. One illustrative display model, zero scenes. Fictional anatomy only: no real species, accurate bone count, scientific, medical, paleontological, educational, restoration, motion, load or exhibit-safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
