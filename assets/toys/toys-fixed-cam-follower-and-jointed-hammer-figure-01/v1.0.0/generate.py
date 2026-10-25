import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='toys-fixed-cam-follower-and-jointed-hammer-figure-01'
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



def boundary_solid(name,xs,ys,zs,filled,mat):
 cells={(i,j,k)for i in range(len(xs)-1)for j in range(len(ys)-1)for k in range(len(zs)-1)if filled((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)}
 vv=[];ff=[];idx={}
 def ids(coords):
  out=[]
  for q in coords:
   if q not in idx:idx[q]=len(vv);vv.append(q)
   out.append(idx[q])
  return tuple(out)
 for i,j,k in sorted(cells):
  x,X=xs[i:i+2];y,Y=ys[j:j+2];z,Z=zs[k:k+2]
  faces=[((-1,0,0),[(x,y,z),(x,y,Z),(x,Y,Z),(x,Y,z)]),((1,0,0),[(X,y,z),(X,Y,z),(X,Y,Z),(X,y,Z)]),((0,-1,0),[(x,y,z),(X,y,z),(X,y,Z),(x,y,Z)]),((0,1,0),[(x,Y,z),(x,Y,Z),(X,Y,Z),(X,Y,z)]),((0,0,-1),[(x,y,z),(x,Y,z),(X,Y,z),(X,y,z)]),((0,0,1),[(x,y,Z),(X,y,Z),(X,Y,Z),(x,Y,Z)])]
  for (a,b,c),q in faces:
   if(i+a,j+b,k+c)not in cells:ff.append(ids(q))
 mesh(name,vv,ff,mat)
# Common open toy case; the follower has a genuine through opening in its roof.
box('WholeGroundFootToyBase',(0,0,.024),(.60,.34,.048),0)
for j,x in enumerate([-.265,.265]):
 for k,y in enumerate([-.125,.125]):box('WholeCaseCorner_%d_%d'%(j,k),(x,y,.145),(.045,.045,.21),0)
boundary_solid('WholeDeckWithFollowerWindow',[-.30,-.015,.075,.30],[-.17,-.090,-.020,.17],[.235,.265],lambda x,y,z:not(-.015<x<.075 and -.090<y<-.020),0)
for j,y in enumerate([-.125,.125]):
 box('WholeCamshaftBearingFoot_%d'%j,(.030,y,.088),(.065,.04,.080),2)
 ringy('WholeCamshaftBearing_%d'%j,y-.025,y+.025,.030,.132,.009,.022,2,20)
cyly('WholeTransverseCamshaft',-.20,.16,.030,.132,.010,2,20)
# One complete eccentric disc, not the old stamp mill's two flat-crest cams.
cyly('WholeEccentricRoundCam',-.074,-.036,.030,.151,.055,2,32)
box('WholeFollowerFoot',(.030,-.055,.211),(.074,.045,.014),2)
lathe_z('WholeFollowerRod',.030,-.055,[(0,.211),(.008,.211),(.008,.625),(0,.625)],2,16)
lathe_z('WholeBoredFollowerGuide',.030,-.055,[(.0095,.266),(.022,.266),(.022,.303),(.0095,.303)],2,24)
# Guide sits on an integral side bracket rooted beside the real roof aperture.
box('WholeGuideSideSeat',(.077,-.055,.278),(.070,.040,.024),0)
beam('WholeFrontHandCrank',(.030,-.194,.132),(.096,-.194,.088),.018,2)
cyly('WholeHandCrankGrip',-.26,-.188,.096,.088,.018,0,20)
# Newly authored wooden figure, not imported marionette or jaw-head mesh.
for j,y in enumerate([-.055,.055]):
 box('WholeWoodFigureShoe_%d'%j,(-.155,y,.283),(.120,.052,.042),3)
 lathe_z('WholeWoodFigureLeg_%d'%j,-.18,y,[(0,.295),(.021,.295),(.024,.335),(.024,.423),(0,.423)],1,16)
lathe_z('WholeFigureTorso',-.18,0,[(0,.404),(.052,.404),(.064,.450),(.059,.530),(.048,.555),(0,.555)],1,20)
lathe_z('WholeFigureNeck',-.18,0,[(0,.545),(.025,.545),(.025,.580),(0,.580)],0,16)
lathe_z('WholeWoodFigureHead',-.18,0,[(0,.563),(.030,.567),(.044,.589),(.045,.622),(.029,.643),(0,.648)],0,24)
lathe_z('WholePlainFigureCap',-.18,0,[(0,.635),(.048,.635),(.048,.651),(.034,.668),(0,.668)],3,24)
# Face points towards the anvil on the right, not a repurposed frontal nutcracker face.
axle('WholeBluntWoodNose',-.141,-.117,0,.612,.010,0,12)
for j,y in enumerate([-.026,.026]):axle('WholeSmallEye_%d'%j,-.145,-.137,y,.624,.0045,3,10)
cyly('WholeShoulderPivot',-.087,.081,-.18,.530,.013,2,20)
beam('WholeForwardUpperArm',(-.18,-.063,.530),(-.055,-.063,.601),.033,1)
cyly('WholeElbowPivot',-.086,-.042,-.055,.601,.017,2,16)
beam('WholeForwardForearm',(-.055,-.063,.601),(.142,-.063,.560),.030,0)
# The follower is connected through a separate sloping link, rather than becoming a falling stamp.
beam('WholeFollowerToElbowLink',(.030,-.055,.618),(-.055,-.055,.601),.012,2)
cyly('WholeUpperFollowerPin',-.080,-.035,.030,.618,.012,2,16)
beam('WholeFarRestingArm',(-.18,.063,.530),(-.09,.063,.452),.032,1)
box('WholeNearWoodHand',(.140,-.063,.555),(.041,.039,.038),0)
beam('WholeFixedHammerHandle',(.140,-.063,.573),(.177,-.063,.424),.014,0)
box('WholeRaisedWoodHammerHead',(.180,-.063,.425),(.085,.045,.035),3)
# Anvil is integral to this same toy's deck, no independent old tool reused.
box('WholeToyAnvilFoot',(.185,-.027,.280),(.133,.125,.035),3)
box('WholeToyAnvilWaist',(.185,-.027,.326),(.070,.080,.075),3)
box('WholeToyAnvilTop',(.185,-.027,.371),(.165,.105,.025),3)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeCaseHeadAndHands_WarmWood',(.57,.34,.14,1),.77,0),('WholeTorsoAndLimbs_MutedBlue',(.075,.23,.30,1),.76,0),('WholeCamPinsAndLinks_Brass',(.52,.34,.12,1),.44,.50),('WholeCapShoesHammerAndAnvil_DarkWood',(.10,.065,.034,1),.74,0)]
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
focus=Vector((0,0,.34))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.95;aim(cam,(3,-6,3.4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/toys/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'toys','style':'S01-clean-geometric','title':'Fixed Cam Follower and Jointed Hammer Figure','description':'One newly authored complete hand-cranked cam-and-hammer wooden automaton exterior in one fixed pose. A common open four-post case carries a transverse shaft, eccentric round cam and a separate footed follower passing through a genuine deck window and bored guide. Its upper sloping link joins the elbow of a newly authored wooden figure, whose shoulder and elbow are distinct transverse pivots and whose raised hand carries one full hammer above an integrated small anvil on the same deck. This is not the old ore stamp mill resized: the follower does not itself end in a falling stamp or mortar; the whole output is an articulated side-facing figure with a shoulder-elbow chain. Unlike the old crank bird, there are no paired direct crank-to-wing links or spread wings, and unlike the lever-jaw figure there is no mouth mechanism. No old figure, anvil or machine geometry imported. Four opaque constant PBR materials; metres, native Z up and horizontal-bounds-centred ground datum. One whole toy prop zero scenes. Static mechanism-inspired art only: no motion cycle, correct kinematic timing, gravity return, actual cam contact through travel, impact, playability, child suitability, manufacturing or safety claim. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
