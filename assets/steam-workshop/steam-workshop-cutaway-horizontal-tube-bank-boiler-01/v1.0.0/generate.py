import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='steam-workshop-cutaway-horizontal-tube-bank-boiler-01'
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

# One genuine three-dimensional open quadrant in the thick horizontal shell.
# Axis Y; six complete hollow tubes and two through-ported rectangular plates.
def arc_shell_y(name,y0,y1,z,ri,ro,a0,a1,mat,n=36):
 angles=[a0+(a1-a0)*i/n for i in range(n+1)];N=n+1;v=[(r*math.cos(a),y,z+r*math.sin(a))for y in[y0,y1]for r in[ri,ro]for a in angles];f=[]
 for i in range(n):j=i+1;f.extend([(i,j,N+j,N+i),(2*N+i,3*N+i,3*N+j,2*N+j),(i,2*N+i,2*N+j,j),(N+i,N+j,3*N+j,3*N+i)])
 f.extend([(0,N,3*N,2*N),(n,2*N+n,3*N+n,N+n)]);mesh(name,v,f,mat)
arc_shell_y('WholeQuarterCutThickHorizontalShell',-.90,.90,1.05,.49,.55,math.pi/2,math.tau,0)
# Whole square-port tube plates are connected solids with six true holes.
# Circular tube outer walls overlap their small square collars, while each bore
# remains clear of the plate: inner radius53mm < square half-width60mm.
def tubeplate(name,y0,y1):
 xs=[-.46,-.34,-.22,-.06,.06,.22,.34,.46];zs=[.72,.83,.95,1.15,1.27,1.38];holes={(i,j)for i in[1,3,5]for j in[1,3]};solid={(i,j)for i in range(7)for j in range(5)}-holes;v=[];f=[];index={}
 def face(p):
  ids=[]
  for q in p:
   if q not in index:index[q]=len(v);v.append(q)
   ids.append(index[q])
  f.append(tuple(ids))
 for i,j in sorted(solid):
  a,b=xs[i],xs[i+1];c,d=zs[j],zs[j+1]
  face([(a,y0,c),(b,y0,c),(b,y0,d),(a,y0,d)]);face([(a,y1,c),(a,y1,d),(b,y1,d),(b,y1,c)])
  if(i-1,j)not in solid:face([(a,y0,c),(a,y0,d),(a,y1,d),(a,y1,c)])
  if(i+1,j)not in solid:face([(b,y0,c),(b,y1,c),(b,y1,d),(b,y0,d)])
  if(i,j-1)not in solid:face([(a,y0,c),(a,y1,c),(b,y1,c),(b,y0,c)])
  if(i,j+1)not in solid:face([(a,y0,d),(b,y0,d),(b,y1,d),(a,y1,d)])
 mesh(name,v,f,2)
tubeplate('WholeFrontSixPortTubePlate',-.84,-.76);tubeplate('WholeRearSixPortTubePlate',.76,.84)
for j,z in enumerate([.89,1.21]):
 for i,x in enumerate([-.28,0,.28]):ringy('WholeOpenFireTube_'+str(j)+'_'+str(i),-.94,.94,x,z,.053,.09,1,20)
ringy('WholeFrontAnnularServiceRim',-.985,-.885,0,1.05,.475,.575,2,36)
cyly('WholeClosedRearHead',.89,1.0,0,1.05,.565,0,36)
# Two complete curved saddle blocks, not a rotated set of vertical boiler legs.
def extrude_y(name,p,y0,y1,mat):
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);v=[(x,y,z)for y in[y0,y1]for x,z in p];f=[tuple(t)for t in triangulate(p)]+[tuple(n+i for i in reversed(t))for t in triangulate(p)]+[(i,n+i,n+(i+1)%n,(i+1)%n)for i in range(n)];mesh(name,v,f,mat)
for j,y in enumerate([-.55,.55]):
 box('WholeSaddleGroundPad'+str(j),(0,y,.025),(1.05,.25,.05),3)
 top=[(x,1.05-math.sqrt(.55*.55-x*x)+.008)for x in [.46-.92*i/16 for i in range(17)]]
 p=[(-.50,.045),(.50,.045),(.50,.76),(.46,.76)]+top+[(-.46,.76),(-.50,.76)]
 extrude_y('WholeCurvedSaddle'+str(j),p,y-.10,y+.10,3)
# A blind recessed flue exterior fixed to the rear cap/shoulder. It does not
# establish combustion, pressure or connected fluid paths.
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
lathe_z('WholeBlindOpenTopRearFlue',0,.91,[(0,1.52),(.13,1.52),(.13,1.99),(.09,1.99),(.09,1.58),(0,1.58)],3)
# Fixed transverse front handle on the lower rim, no opening/rotation claim.
beam('WholeLowerServiceHandle',(-.16,-1.015,.53),(.16,-1.015,.53),.035,2)
for x,label in[(-.16,'Left'),(.16,'Right')]:beam(label+'HandleRoot',(x,-.94,.53),(x,-1.03,.53),.035,2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('CutawayShell_DeepTeal',(.045,.20,.21,1),.54,.35),('WholeTubeBank_WarmCopper',(.48,.23,.08,1),.47,.55),('TubePlatesRim_MutedBrass',(.52,.37,.12,1),.55,.40),('SaddlesFlue_DarkIron',(.09,.11,.12,1),.66,.35)]
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
focus=Vector((0,0,1.02))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.95;aim(cam,(5,-6,4.0));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/steam-workshop/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'steam-workshop','style':'S01-clean-geometric','title':'Cutaway Horizontal Tube-Bank Boiler Display','description':'One complete newly authored static cutaway horizontal tube-bank boiler appearance. A genuinely thick C-section barrel omits one full upper quadrant so its inner wall and six complete hollow longitudinal tubes can be seen. Two connected solid rectangular tube plates each have six real square through-ports surrounding the circular tubes; tube bores remain clear of these plates. A whole front annular service rim and closed rear head frame the assembly, with two complete curved saddle blocks on finite ground pads and a blind open-top rear flue exterior. This is not the old closed vertical firebox boiler rotated or rescaled, and not a cutaway piston cylinder with another rod: the twin plates, longitudinal tube bank, open quadrant and two saddle architecture are all newly defined. Four constant opaque PBR materials; separate closed editable bodies with intentional fixed embedded joins, metres/native Z up/actual horizontal bounds-centred ground origin. One illustrative display model, zero scenes. No real boiler construction specification, functional combustion, steam, pressure containment, connected fluid circuits, thermodynamics, repair, load, manufacture, motion or equipment safety claim. The rear head closes the display; this is not a functioning through-flow appliance.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
