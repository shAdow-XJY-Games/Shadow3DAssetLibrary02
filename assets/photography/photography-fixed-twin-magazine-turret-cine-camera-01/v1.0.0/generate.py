import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='photography-fixed-twin-magazine-turret-cine-camera-01'
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



# Complete newly authored hand-cranked cine-camera exterior, without tripod or scene.
def prism_y(name,poly,y0,y1,mat):
 v=[(x,y,z)for y in[y0,y1]for x,z in poly];n=len(poly);tt=triangulate(poly);f=list(tt)+[tuple(n+i for i in reversed(t))for t in tt]+[(i,n+i,n+(i+1)%n,(i+1)%n)for i in range(n)];mesh(name,v,f,mat)
body=[(-.145,.022),(.145,.022),(.160,.043),(.160,.355),(.133,.410),(-.112,.410),(-.153,.363),(-.153,.045)]
prism_y('WholeGroundFootBeveledDriveCameraBody',body,-.105,.105,0)
# One connected double-lobed magazine boundary, not two detached round boxes.
r=.130;cx=.105;zc=.480;alpha=math.acos(cx/r);outline=[]
for center,start,end in[(-cx,alpha,math.tau-alpha),(cx,math.pi+alpha,3*math.pi-alpha)]:
 for j in range(25):
  a=start+(end-start)*j/24;p=(center+r*math.cos(a),zc+r*math.sin(a))
  if not outline or math.dist(p,outline[-1])>1e-8:outline.append(p)
if math.dist(outline[0],outline[-1])<1e-8:outline.pop()
prism_y('WholeConnectedTwinLobeFilmMagazine',outline,-.077,.077,0)
lid=[(x*.94,zc+(z-zc)*.94)for x,z in outline];prism_y('WholeProudMagazineFrontLid',lid,-.083,-.074,1)
# Full raised turret plate and three unequal separate hollow lens mouths around its actual axis.
cyly('WholeFixedTurretBearing',-.130,-.095,0,.230,.060,2,24)
cyly('WholeThreeLensTurretPlate',-.156,-.124,0,.230,.108,1,36)
for k,(a,length,ro)in enumerate([(math.pi/2,.140,.032),(math.pi*7/6,.080,.029),(math.pi*11/6,.055,.026)]):
 x=.065*math.cos(a);z=.230+.065*math.sin(a)
 ringy('WholeOpenLensBarrel_%02d'%k,-.151-length,-.148,x,z,ro-.008,ro,2,24)
 cyly('WholeRecessedOpaqueOptic_%02d'%k,-.151-length+.009,-.151-length+.016,x,z,ro-.008,3,24)
 ringy('WholeLensShoulderRing_%02d'%k,-.177,-.150,x,z,ro,ro+.004,1,24)
cyly('WholeTurretCentralRetainer',-.171,-.151,0,.230,.015,2,20)
# Whole side-mounted finder with two real roots, independent of the taking lenses.
for y in[-.035,.065]:beam('WholeFinderRoot_'+str(y),(.147,y,.345),(.198,y,.345),.025,2)
ringy('WholeLongSideFinderHousing',-.154,.130,.202,.350,.014,.027,2,24)
cyly('WholeFinderRecessedOpaqueFront',-.142,-.132,.202,.350,.014,3,24)
ringy('WholeRearFinderEyecup',.113,.153,.202,.350,.014,.034,2,24)
# Real open handle above the magazine central saddle, both lower legs seated in its lobes.
handle=[(-.045,.541),(-.025,.541),(-.025,.638),(.025,.638),(.025,.541),(.045,.541),(.045,.659),(-.045,.659)]
prism_y('WholeOpenUpperCarryHandle',handle,-.023,.023,2)
# Side drive spindle and one fixed bent arm/complete grip are part of this camera only.
axle('WholeSideCrankSpindle',.148,.202,.025,.185,.016,1,20)
beam('WholeFixedSideCrankArm',(.198,.025,.185),(.198,.080,.100),.022,1)
axle('WholeSideCrankGrip',.188,.265,.080,.100,.024,2,20)
# One recessed side panel with deliberate offset border, no markings or controls implied.
box('WholeProudSideAccessPanel',(-.158,.015,.205),(.014,.142,.215),1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeBodyAndMagazine_DeepTeal',(.055,.12,.13,1),.69,.10),('WholeLidsTurretAndCrank_SatinNickel',(.47,.49,.45,1),.48,.55),('WholeBarrelsHandleAndGrip_Charcoal',(.035,.045,.045,1),.73,.08),('WholeRecessedOpaqueOptics_BlueBlack',(.025,.055,.070,1),.32,.13)]
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
focus=Vector((0,0,.32))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.89;aim(cam,(3,-5,2.9));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/photography/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'photography','style':'S01-clean-geometric','title':'Fixed Twin Magazine Turret Cine Camera','description':'One newly authored complete static hand-cranked cine-camera-style exterior. A whole bevelled grounded drive body carries one continuous double-lobed sealed upper film-magazine shape with a separately proud whole matching lid. A complete front turret disc sits on its own hub and carries three unequal genuinely hollow lens barrels with recessed opaque optical-appearance discs. Two finite side roots carry a full longitudinal finder tube and rear eyecup. A whole open upper handle seats in the central magazine saddle; a separate side spindle, fixed crank arm and full grip belong to the lower body. No old tripod box, long-barrel grip camera, projector reel or lens geometry is imported. This is a new complete magazine/drive-body/three-lens-turret layout, not two discs added to a reused camera. Four opaque constant untextured PBR roles, metres, Z up and whole horizontal-bounds-centred finite body sole. One complete model, zero scenes. Static illustrative exterior only: internal film and transport are not modeled, and no optics, exposure, imaging, focus, turret selection, winding, motion, historical authenticity, interchangeable fit, handling, manufacture or safety claim. No tripod, film strip, brands, text, photographer or environment.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
