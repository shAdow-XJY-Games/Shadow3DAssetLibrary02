import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='festival-fixed-hollow-bulging-eye-and-open-jaw-lion-head-01'
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



# Entire thick rounded head shell, real mouth cut and open lower access.
def ellipsoid(name,c,r,mat,n=24,m=12):
 v=[(c[0],c[1],c[2]-r[2])];rings=[]
 for j in range(1,m):
  a=-math.pi/2+math.pi*j/m;ids=[]
  for i in range(n):
   t=math.tau*i/n;ids.append(len(v));v.append((c[0]+r[0]*math.cos(a)*math.cos(t),c[1]+r[1]*math.cos(a)*math.sin(t),c[2]+r[2]*math.sin(a)))
  rings.append(ids)
 top=len(v);v.append((c[0],c[1],c[2]+r[2]));f=[]
 for i in range(n):f.extend([(0,rings[0][(i+1)%n],rings[0][i]),(top,rings[-1][i],rings[-1][(i+1)%n])])
 for a,b in zip(rings,rings[1:]):
  for i in range(n):j=(i+1)%n;f.append((a[i],a[j],b[j],b[i]))
 mesh(name,v,f,mat)
profile=[(0,.235,.205),(.10,.285,.245),(.18,.335,.285),(.32,.390,.325),(.46,.410,.330),(.61,.365,.295),(.75,.275,.225),(.845,.135,.120)]
n=32;v=[]
for inner in[False,True]:
 for z,rx,ry in profile:
  for i in range(n):
   a=math.tau*i/n;v.append(((rx-(.035 if inner else 0))*math.cos(a),(ry-(.035 if inner else 0))*math.sin(a),z))
N=n*len(profile);out=[]
for j in range(len(profile)-1):
 for i in range(n):
  # Broad frontal mouth through two complete ring bands, true finite reveal loop.
  if j in[2,3] and 19<=i<29:continue
  k=(i+1)%n;out.append((j*n+i,j*n+k,(j+1)*n+k,(j+1)*n+i))
top=len(v);v.append((0,0,.890));innertop=len(v);v.append((0,0,.855))
for i in range(n):out.append(((len(profile)-1)*n+i,(len(profile)-1)*n+(i+1)%n,top))
f=[]
for q in out:
 f.append(q);f.append(tuple((innertop if i==top else i+N)for i in reversed(q)))
edges={}
for q in out:
 for a,b in zip(q,q[1:]+q[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((a,b))
for pairs in edges.values():
 if len(pairs)==1:
  a,b=pairs[0];f.append((b,a,a+N,b+N))
mesh('WholeGroundFootHollowHeadShell',v,f,0)
# A full lower jaw crescent, with actual interior and finite end walls.
pp=[(.350*math.cos(math.pi+math.pi*i/24),-.035+.420*math.sin(math.pi+math.pi*i/24))for i in range(25)]
pp +=[(.285*math.cos(math.tau-math.pi*i/24),-.035+.335*math.sin(math.tau-math.pi*i/24))for i in range(25)]
vv=[(x,y,z)for z in[0,.095]for x,y in pp];nn=len(pp);ff=[]
for a,b,c in triangulate(pp):ff.extend([(c,b,a),(nn+a,nn+b,nn+c)])
ff +=[(i,(i+1)%nn,(i+1)%nn+nn,i+nn)for i in range(nn)]
mesh('WholeGroundFootOpenLowerJaw',vv,ff,2)
for side in[-1,1]:
 axle('WholeSideJawPivot_'+str(side),side*.302,side*.370,-.035,.104,.048,2,20)
 ellipsoid('WholeBulgingEyeShell_'+str(side),(side*.230,-.245,.630),(.155,.115,.150),3)
 cyly('WholeDarkForwardPupil_'+str(side),-.367,-.346,side*.230,.630,.070,1,24)
 ellipsoid('WholeRaisedEar_'+str(side),(side*.350,.045,.685),(.135,.066,.160),2,20,10)
 ellipsoid('WholeInsetEarFace_'+str(side),(side*.362,-.011,.690),(.085,.020,.106),0,20,10)
ellipsoid('WholeBroadMuzzleNose',(0,-.340,.478),(.160,.104,.077),1,24,10)
vv=[];nn=20
for y,z,r in[(.045,.790,.055),(.045,.900,.055),(-.015,.990,.035),(-.070,1.020,.010)]:
 for i in range(nn):a=math.tau*i/nn;vv.append((r*math.cos(a),y+r*math.sin(a),z))
ff=[tuple(reversed(range(nn))),tuple(3*nn+i for i in range(nn))]
for k in range(3):
 for i in range(nn):j=(i+1)%nn;ff.append((k*nn+i,k*nn+j,(k+1)*nn+j,(k+1)*nn+i))
mesh('WholeBentBluntCrownHorn',vv,ff,2)
axle('WholeInteriorTransverseGrip',-.375,.375,.035,.320,.020,2,20)
for i,x in enumerate([-.21,-.07,.07,.21]):
 y=-.035-.394*math.sqrt(1-(x/.35)**2)
 box('WholeBluntLowerTooth_%d'%i,(x,y,.113),(.065,.045,.060),3)
# First real visual revision: broad brows, shaped muzzle trim and lower beard.
def face_prism(name,pp,y0,y1,mat):
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(pp,pp[1:]+pp[:1]))<0:pp=list(reversed(pp))
 n=len(pp);vv=[(x,y,z)for y in[y0,y1]for x,z in pp];ff=[]
 for a,b,c in triangulate(pp):ff.extend([(c,b,a),(n+a,n+b,n+c)])
 ff +=[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)]
 mesh(name,vv,ff,mat)
for side in[-1,1]:
 pp=[(side*.230+r*math.cos(a),.635+.9*r*math.sin(a))for r,aa in[(.185,[math.radians(-10+200*i/24)for i in range(25)]),(.145,[math.radians(190-200*i/24)for i in range(25)])]for a in aa]
 face_prism('WholeBroadArchedEyebrow_'+str(side),pp,-.367,-.330,2)
 pp=[(side*x,z)for x,z in[(.010,.405),(.080,.375),(.155,.370),(.230,.390),(.305,.425),(.355,.480),(.350,.525),(.300,.485),(.220,.450),(.140,.430),(.070,.438),(.010,.460)]]
 face_prism('WholeSweptMuzzleWhisker_'+str(side),pp,-.385,-.337,3)
# One whole broad lower beard panel, rooted in the jaw lip, with a flat bottom fringe.
pp=[(-.265,0),(.265,0),(.290,.035),(.275,.075),(.240,.120),(.205,.155),(.135,.145),(.065,.160),(0,.148),(-.065,.160),(-.135,.145),(-.205,.155),(-.240,.120),(-.275,.075),(-.290,.035)]
face_prism('WholeGroundFootLowerBeard',pp,-.478,-.410,3)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeFestivalHeadAndEarFace_Vermilion',(.60,.065,.025,1),.78,0),('WholeNoseAndPupils_Charcoal',(.018,.024,.021,1),.72,0),('WholeJawEarsHornAndGrip_Ochre',(.76,.42,.055,1),.72,0),('WholeEyesAndBluntTeeth_Ivory',(.82,.76,.57,1),.74,0)]
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
focus=Vector((0,0,.51))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.40;aim(cam,(1.5,-5,1.6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/festival/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'festival','style':'S01-clean-geometric','title':'Fixed Hollow Bulging Eye and Open Jaw Lion Head','description':'One newly authored complete stylised lion-dance-inspired head puppet in one fixed open-jaw display pose. A whole deep rounded finite-thickness head shell has a genuine lower access opening and a separate broad open mouth into its cavity. Two large forward bulging eye shells and dark pupils, paired broad raised ears, a broad muzzle nose and short crown horn form its nonhuman festival silhouette. Broad arched brows, swept muzzle trim and a wide lower beard reinforce the lion-head silhouette. A complete U-shaped lower jaw joins the side hinge appearances, with short blunt teeth; one entire interior transverse grip meets the two side walls. This is not an extracted dragonboat bow ornament or a carved flat theatrical face with changed colours: the deep enclosing head volume, round projecting eyes, open lower access, wide jaw and internal grip are newly authored together. No imported old head, mannequin, cloth body or surrounding scene. One prop zero scenes, four opaque PBR appearances, metres and true horizontal bounds-centred ground origin. Anonymous simplified festival art only, not a historically exact regional tradition, wearable costume, fitted headgear or functioning puppet. Jaw motion, hand access, vision, ventilation, performance, human fit, load, manufacture and safety not made or verified. Rigging animation interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
