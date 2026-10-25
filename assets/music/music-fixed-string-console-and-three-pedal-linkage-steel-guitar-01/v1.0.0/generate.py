import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='music-fixed-string-console-and-three-pedal-linkage-steel-guitar-01'
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



# One new full fixed string console with its own four legs and pedal train.
box('WholeLongConsoleBody',(0,0,.757),(.98,.34,.065),0)
for tag,y in [('Front',-.162),('Rear',.162)]:box('WholeDeepApron_'+tag,(0,y,.715),(.960,.026,.104),0)
box('WholeRaisedLongStringDeck',(.015,0,.803),(.72,.205,.030),2)
# Four complete sloping members with broad finite ground feet.
for side,x in [('Left',-.43),('Right',.43)]:
 for end,y in [('Front',-.13),('Rear',.13)]:
  xx=x*1.13;yy=y*1.50
  beam('WholeSlopingLeg_'+side+end,(xx,yy,.022),(x,y,.738),.028,1)
  box('WholeGroundFoot_'+side+end,(xx,yy,.014),(.065,.064,.028),2)
# Tuner housing: five entire slabs form an open central pocket, not a painted depression.
box('WholeTunerHeadFloor',(-.410,0,.801),(.145,.280,.023),1)
for tag,y in [('Front',-.130),('Rear',.130)]:box('WholeTunerHeadCheek_'+tag,(-.410,y,.828),(.145,.020,.060),1)
for tag,x in [('Outer',-.477),('Inner',-.343)]:box('WholeTunerHeadEnd_'+tag,(x,0,.825),(.013,.250,.055),1)
# A single real transverse axle carries ten distinct fixed bridge fingers.
cyly('WholeBridgeFingerAxle',-.135,.135,.385,.834,.010,1,16)
for tag,y in [('Front',-.127),('Rear',.127)]:box('WholeBridgeAxleBearing_'+tag,(.385,y,.820),(.045,.022,.065),1)
box('WholeStringNut',(-.315,0,.832),(.015,.227,.026),3)
box('WholePickupBlock',(.292,0,.826),(.052,.230,.021),2)
# True strings and tuning shafts are separate from the solid deck.
for i in range(10):
 y=-.0945+i*.021
 box('WholeFixedBridgeFinger_%02d'%i,(.385,y,.8415),(.055,.015,.029),1)
 # Staggered actual posts lie inside the tuner pocket; shafts reach a side cheek.
 x=-.452+(i%5)*.023;sg=-1 if i<5 else 1
 lathe_z('WholeTunerPost_%02d'%i,x,y,[(0,.804),(.004,.804),(.004,.850),(0,.850)],1,10)
 cyly('WholeTunerSideShaft_%02d'%i,min(y,sg*.149),max(y,sg*.149),x,.828,.0035,1,8)
 box('WholeTunerButton_%02d'%i,(x,sg*.153,.828),(.016,.020,.012),3)
 # Continuous narrow beam strings, finite contacts at nut and bridge; no acoustic assertion.
 beam('WholePlayingString_%02d'%i,(-.317,y,.844),(.407,y,.855),.0018,3)
 beam('WholePegToNutString_%02d'%i,(x,y,.849),(-.317,y,.844),.0018,3)
for i,x in enumerate([-.250,-.180,-.115,-.055,0,.050,.097,.141,.182,.221]):
 box('WholeFixedPositionMarker_%02d'%i,(x,0,.819),(.002,.183,.002),3)
for tag,x in [('One',.43),('Two',.465)]:lathe_z('WholeControlKnob_'+tag,x,-.07,[(0,.785),(.011,.785),(.011,.807),(0,.807)],2,12)
# Complete front bar and three pedal/rod/crank routes, all in one fixed display pose.
box('WholeLowFrontPedalCrossbar',(0,-.190,.108),(.990,.035,.045),1)
for i,x in enumerate([-.250,-.120,.010]):
 axle('WholePedalPivot_%d'%i,x-.026,x+.026,-.190,.111,.010,1,12)
 beam('WholeProjectingFootPedal_%d'%i,(x,-.190,.111),(x,-.375,.067),.034,1)
 box('WholeFootPedalTread_%d'%i,(x,-.352,.081),(.056,.086,.012),2)
 beam('WholeFullPedalVerticalRod_%d'%i,(x,-.221,.117),(x,-.174,.653),.007,1)
 axle('WholeUnderframeCrossShaft_%d'%i,x-.032,x+.032,-.137,.677,.009,1,12)
 beam('WholePedalUpperCrank_%d'%i,(x,-.174,.653),(x,-.137,.680),.017,1)
 box('WholeCrankBearingBracket_%d'%i,(x,-.137,.700),(.065,.026,.065),1)
for tag,x in [('Left',-.130),('Right',.160)]:
 box('WholeFixedKneeLeverRoot_'+tag,(x,.030,.701),(.035,.055,.048),1)
 beam('WholeFixedKneeLever_'+tag,(x,.030,.693),(x+.035,.030,.515),.021,1)
 box('WholeKneeLeverPad_'+tag,(x+.035,.030,.520),(.030,.063,.055),2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeConsoleAprons_DeepBurgundy',(.27,.055,.065,1),.53,.10),('WholeLegsTunerAndPedalHardware_SatinMetal',(.42,.47,.49,1),.40,.72),('WholeDeckFeetAndPedalPads_Charcoal',(.035,.044,.048,1),.72,0),('WholeStringsMarkersAndNut_WarmIvory',(.77,.74,.63,1),.43,.20)]
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
focus=Vector((0,0,.42))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.52;aim(cam,(4,-6,4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/music/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':'Fixed String Console and Three Pedal Linkage Steel Guitar','description':'One newly authored whole static pedal-steel-style string-console instrument. A long narrow solid console with deep front and rear aprons has a full raised string deck, a genuinely open central tuner-head pocket at one end and ten separate fixed bridge fingers on a common transverse axle at the other. Ten continuous strings span individual tuner posts, a full nut and bridge; a separate pickup and fixed controls complete the top. Four outward-sloping legs terminate in finite ground feet. A complete low front pedal bar joins the front legs, carries three thick projecting foot pedals and three full vertical rods ending in separately modeled under-console crank arms. Two additional fixed knee-lever appearances hang below the console. All geometry is new: not an electric guitar laid on a stand or a zither with more strings; the legged console, end hardware and entire pedal-to-underframe layout define the complete object. Four opaque untextured PBR roles, metres, Z up and horizontal-envelope-centred ground origin. One prop and zero scenes. Static illustrative exterior only; string tension, sound, tuning, pitch-change mechanism, pedal or knee movement, electrical internals, playing ergonomics and manufacture are not verified. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
