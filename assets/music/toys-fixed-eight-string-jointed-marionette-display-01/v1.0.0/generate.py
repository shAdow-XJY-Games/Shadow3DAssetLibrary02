import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='toys-fixed-eight-string-jointed-marionette-display-01'
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



# One complete hanging jointed wooden puppet, fixed to a cross-control display stand.
box('WholeDisplayGroundFoot',(0,.045,.025),(.66,.46,.05),0)
box('WholeRearDisplayPost',(0,.225,.81),(.040,.040,1.55),0)
beam('WholeUpperControlSupport',(0,.225,1.56),(0,0,1.56),.040,0)
box('WholeTransverseWoodControlBar',(0,0,1.55),(.62,.034,.026),0)
box('WholeForeAftWoodControlBar',(0,-.040,1.572),(.035,.50,.026),0)
# New full wood torso/hip/neck/head; no imported spring-puppet half body.
lathe_z('WholeTaperedWoodTorso',0,-.045,[(0,.62),(.072,.62),(.085,.69),(.082,.77),(.107,.86),(.102,.90),(.070,.918),(0,.918)],1,24)
v,f,m=G['WholeTaperedWoodTorso'];G['WholeTaperedWoodTorso']=([(x,(y+.045)*.62-.045,z)for x,y,z in v],f,m)
lathe_z('WholeWoodPelvis',0,-.045,[(0,.565),(.083,.565),(.089,.59),(.082,.62),(0,.62)],0,24)
lathe_z('WholeNarrowNeck',0,-.045,[(0,.90),(.027,.90),(.027,.972),(0,.972)],0,16)
lathe_z('WholeRoundedToyHead',0,-.045,[(0,.95),(.045,.96),(.068,.985),(.079,1.025),(.078,1.075),(.064,1.115),(.034,1.140),(0,1.148)],0,24)
for side,x in [('Left',-.027),('Right',.027)]:cyly(side+'WholeBlankEye',-.123,-.114,x,1.073,.006,2,12)
cyly('WholeSmallBluntNose',-.141,-.114,0,1.043,.012,0,12)
# Rounded tapered limb segments are new, with real end sockets carried by pin/ear appearances.
def limb(name,a,b,r0,r1,mat):
 w=unit(sub(b,a));u=unit(cross(w,(0,1,0)));vv=cross(w,u);N=12;v=[]
 for t,r in[(0,r0*.70),(.12,r0),(.82,r1),(1,r1*.70)]:
  p=tuple(a[k]+t*(b[k]-a[k])for k in range(3))
  for j in range(N):q=math.tau*(j+.5)/N;v.append(tuple(p[k]+r*(u[k]*math.cos(q)+vv[k]*math.sin(q))for k in range(3)))
 f=[tuple(reversed(range(N))),tuple(3*N+i for i in range(N))]+[(k*N+i,k*N+(i+1)%N,(k+1)*N+(i+1)%N,(k+1)*N+i)for k in range(3)for i in range(N)];mesh(name,v,f,mat)
def clevis(label,p,rad=.027,depth=.060):
 x,y,z=p
 # Two complete parallel cheeks and a full visible through pin; no moving tolerance claim.
 for s in[-1,1]:cyly(label+'WholeClevisEar_'+str(s),y+s*depth/2-.007,y+s*depth/2+.007,x,z,rad,0,16)
 cyly(label+'WholeTransversePin',y-depth/2-.013,y+depth/2+.013,x,z,.009,2,12)
control=[]
for side,sgn in [('Left',-1),('Right',1)]:
 shoulder=(sgn*.112,-.045,.866);elbow=(sgn*.186,-.065,.715);wrist=(sgn*.238,-.100,.620)
 limb(side+'WholeUpperArm',shoulder,elbow,.031,.025,1);limb(side+'WholeForearm',elbow,wrist,.023,.019,0)
 clevis(side+'Shoulder',shoulder,.029,.072);clevis(side+'Elbow',elbow,.023,.060)
 limb(side+'WholeRoundedHand',(sgn*.238,-.100,.632),(sgn*.248,-.106,.575),.026,.024,0)
 hip=(sgn*.061,-.045,.586);knee=(sgn*.083,-.067,.375);ankle=(sgn*.092,-.045,.163)
 limb(side+'WholeUpperLeg',hip,knee,.038,.031,1);limb(side+'WholeLowerLeg',knee,ankle,.029,.022,0)
 clevis(side+'Hip',hip,.032,.080);clevis(side+'Knee',knee,.027,.070)
 # One whole closed long wooden shoe, suspended above ground rather than false ground contact.
 p=[(-.092,.105),(.035,.105),(.042,.123),(.020,.162),(-.032,.180),(-.085,.154)];n=len(p);x=sgn*.092;v=[(xx,y,z)for xx in[x-.032,x+.032]for y,z in p];f=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh(side+'WholeWoodShoe',v,f,2)
 control.extend([(side+'Head', (sgn*.035,-.045,1.126),(sgn*.070,0,1.548)),(side+'Shoulder',shoulder,(sgn*.155,0,1.548)),(side+'Hand',wrist,(sgn*.285,0,1.548)),(side+'Knee',knee,(sgn*.010,-.260,1.570))])
# Eight whole straight solid cords each root inside its original part and control wood.
for label,a,b in control:beam(label+'WholeSuspensionCord',a,b,.0025,2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeWoodHeadLimbsStandAndControls_WarmMaple',(.62,.40,.19,1),.76,0),('WholeWoodTorsoUpperLimbs_MutedTeal',(.065,.24,.25,1),.79,0),('WholePinsCordsEyesAndShoes_Charcoal',(.055,.065,.065,1),.70,0)]
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
focus=Vector((0,0,.79))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.96;aim(cam,(2.6,-6,2.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/music/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'toys','style':'S01-clean-geometric','title':'Fixed Eight String Jointed Marionette Display','description':'One newly authored complete fixed wooden marionette display. A rounded head, narrow neck, full shaped torso and separate pelvis lead to two-section arms and legs, blunt hands and long wooden shoes. Eight paired-cheek joint appearances contain actual transverse pins. Eight whole solid suspension cords connect the head, shoulders, hands and knees to complete crossed wooden control bars, themselves supported by an entire rear stand and finite low base. The puppet remains visibly above the base. Unlike the existing raised spring-box half figure, there is no case or spring and the entire four-limbed body is independently suspended. Unlike the fixed open-waist inspection robot, there is no sensor visor, claw, machine chest or grounded foot support: the new rounded wood parts, hanging cord routes and control assembly form one different complete toy. No old body meshes imported or scaled. Three opaque constant untextured PBR roles, metres, Z up and whole horizontally bounds-centred ground origin. One whole prop, zero scenes. Fixed static illustration only: no string rigging, animation, joint travel, realistic tension or balance, control operation, child fit, load, manufacture or toy-safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
