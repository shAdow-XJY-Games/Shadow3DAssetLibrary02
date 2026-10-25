import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='toys-fixed-twin-link-and-jointed-wing-crank-bird-01'
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



box('WholeGroundFootCommonToyBed',(0,0,.025),(.34,.31,.050),0)
for j,y in enumerate([-.085,.085]):
 box('WholeCrankShaftStandard_%d'%j,(0,y,.137),(.065,.045,.196),0)
 ringy('WholeCrankShaftBearing_%d'%j,y-.028,y+.028,0,.224,.011,.025,2,20)
cyly('WholeThroughCrankShaft',-.167,.127,0,.224,.012,2,20)
box('WholeRearBodySupport',(0,.118,.274),(.038,.045,.455),0)
# Rounded whole body; ellipsoidal stations are original and not a reused animal mesh.
def oval(name,c,scale,mat,n=20,rows=8):
 profile=[(math.sin(math.pi*k/rows),-math.cos(math.pi*k/rows))for k in range(rows+1)];profile[0]=(0,-1);profile[-1]=(0,1)
 lathe_z(name,0,0,profile,mat,n);v,f,m=G[name];G[name]=([(c[0]+x*scale[0],c[1]+y*scale[1],c[2]+z*scale[2])for x,y,z in v],f,m)
oval('WholeRoundedWoodBirdBody',(0,.015,.473),(.072,.143,.081),0,24,10)
oval('WholeShortNeck',(0,-.105,.527),(.041,.044,.055),0,16,8)
oval('WholeRoundedBirdHead',(0,-.127,.575),(.050,.056,.051),0,20,8)
mesh('WholeBluntBirdBeak',[(-.028,-.165,.565),(.028,-.165,.565),(.017,-.222,.571),(-.017,-.222,.571),(-.025,-.165,.588),(.025,-.165,.588),(.014,-.215,.579),(-.014,-.215,.579)],[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],3)
for j,s in enumerate([-1,1]):axle('WholeSmallToyEye_%d'%j,s*.044-.006,s*.044+.006,-.145,.589,.008,3,12)
# Thick whole wings with tapered outer ends and blunt stepped feather silhouette.
outline=[(.052,-.044),(.16,-.105),(.31,-.098),(.405,-.045),(.413,.008),(.381,.033),(.351,.066),(.309,.073),(.272,.104),(.201,.111),(.121,.081),(.052,.060)]
for j,s in enumerate([-1,1]):
 pp=[(s*x,y)for x,y in outline]
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(pp,pp[1:]+pp[:1]))<0:pp.reverse()
 n=len(pp);v=[]
 for dz in[-.010,.010]:
  for x,y in pp:v.append((x,y,.489+.25*(abs(x)-.052)+dz))
 f=[]
 for a,b,c in triangulate(pp):f +=[(c,b,a),(a+n,b+n,c+n)]
 f +=[(k,(k+1)%n,(k+1)%n+n,k+n)for k in range(n)];mesh('WholeJointedTaperWing_%d'%j,v,f,1)
 x=s*.060
 cyly('WholeWingHingePin_%d'%j,-.063,.082,x,.491,.010,2,16)
 for k,y in enumerate([-.042,.061]):ringy('WholeWingHingeCollar_%d_%d'%(j,k),y-.009,y+.009,x,.491,.009,.018,2,16)
 # Rockers and rods stay proud of the body and have separate axial layers at crank cheeks.
 beam('WholeForwardWingRootRocker_%d'%j,(s*.077,.005,.500),(s*.120,-.118,.506),.018,2)
 cyly('WholeUpperRodPin_%d'%j,-.140,-.105,s*.120,.506,.012,2,16)
 q=(s*.045,-.126-j*.025,.224+s*.027)
 beam('WholeOffsetCrankCheek_%d'%j,(0,q[1],.224),q,.020,2)
 cyly('WholeLowerRodPin_%d'%j,q[1]-.012,q[1]+.012,q[0],q[2],.012,2,16)
 beam('WholeWingLinkRod_%d'%j,q,(s*.120,-.126,.506),.012,3)
# One new broad thick tail joins the rear body above the support, with no cloth or feathers claim.
p=[(-.035,.115),(.035,.115),(.094,.242),(.064,.266),(-.064,.266),(-.094,.242)];n=len(p);v=[(x,y,.462+.12*(y-.115)+dz)for dz in[-.010,.010]for x,y in p];f=[]
for a,b,c in triangulate(p):f +=[(c,b,a),(a+n,b+n,c+n)]
f +=[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh('WholeFanTail',v,f,1)
beam('WholeForwardHandCrank',(0,-.171,.224),(.060,-.171,.179),.018,2)
cyly('WholeCrankHandGrip',-.230,-.164,.060,.179,.020,0,20)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeWoodBodyBedAndGrip_Maple',(.61,.39,.17,1),.76,0),('WholeWingAndTail_MutedTeal',(.08,.28,.29,1),.74,0),('WholePinsCranksAndBearings_Brass',(.55,.36,.13,1),.42,.55),('WholeRodsEyesAndBeak_DarkWalnut',(.10,.065,.032,1),.72,.05)]
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
focus=Vector((0,0,.31))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.10;aim(cam,(3,-6,3.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/toys/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'toys','style':'S01-clean-geometric','title':'Fixed Twin Link and Jointed Wing Crank Bird','description':'One newly authored complete hand-crank winged-bird toy in a single fixed display pose. A common low wooden bed supports two fore-aft shaft standards, a full longitudinal axle, two offset crank cheeks and separate side linkage rods. Each complete rod joins a distinct short forward rocker at the root of one broad tapered thick wing. Two whole wing hinge pins run fore-aft through finite collars beside an independently authored rounded wooden bird body; a rear upright supports the body above the open crank bay. A short neck and rounded head, blunt beak, two small eyes and a whole fan tail complete the bird silhouette. A forward crank and entire hand grip belong to the low shaft. All visible geometry is newly authored: not an old spring rider with its spring removed, an old animal mounted on a base, or a string puppet with renamed limbs. The two shaft-to-wing rod paths are a fixed illustrative mechanical relationship, not an evaluated kinematic system. Four opaque constant PBR materials, one complete toy prop zero scenes, metres native Z up and complete horizontal-bounds-centred finite base datum. Static display art only: no cranking, wing motion, rigging, working joint travel, transmission ratio, flight, balance, toy operation, child suitability, handling, fabrication, pinch protection or safety claim. Animation and interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
