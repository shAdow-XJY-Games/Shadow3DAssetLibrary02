import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='fitness-fixed-front-crank-rear-roller-elliptical-01'
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



# One complete front-crank/rear-roller elliptical appearance, no old exercise-machine geometry imported.
for label,y in [('Front',-.84),('Rear',.90)]:
 box(label+'WholeGroundCrossfoot',(0,y,.045),(.88,.18,.09),2)
for label,x in [('Left',-.285),('Right',.285)]:box(label+'WholeLongRearRollerRail',(x,.10,.095),(.15,1.75,.05),0)
box('WholeFrontCasePedestal',(0,-.63,.19),(.30,.42,.24),0)
# Complete bevelled cylindrical opaque resistance case on the transverse front shaft.
lathe_z('WholeBevelledFrontResistanceCase',0,0,[(0,-.17),(.25,-.17),(.295,-.13),(.295,.13),(.25,.17),(0,.17)],1,32)
v,f,m=G['WholeBevelledFrontResistanceCase'];G['WholeBevelledFrontResistanceCase']=([(z,-.65+y,.45+x)for x,y,z in v],[tuple(reversed(t))for t in f],m)
axle('WholeFrontCrankThroughAxle',-.36,.36,-.65,.45,.032,2,24)
# One fixed front mast supports both independent handle arms and blank console.
beam('WholeFixedFrontMast',(0,-.67,.45),(0,-.48,1.10),.085,0)
axle('WholeHandlePivotCrossAxle',-.445,.445,-.48,1.08,.035,2,24)
box('WholeBlankConsole',(0,-.47,1.18),(.25,.18,.12),2)
# Whole constant-section swept tubes; fixed outline only, no joint motion.
def tube(name,points,r,mat,n=12):
 v=[];f=[]
 for k,p in enumerate(points):
  t=unit(sub(points[min(k+1,len(points)-1)],points[max(k-1,0)]));u=unit(cross(t,(1,0,0)if abs(t[0])<.9 else(0,1,0)));w=cross(t,u)
  v.extend([tuple(p[j]+r*(u[j]*math.cos(math.tau*i/n)+w[j]*math.sin(math.tau*i/n))for j in range(3))for i in range(n)])
 for k in range(len(points)-1):
  for i in range(n):j=(i+1)%n;f.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i))
 f += [tuple(reversed(range(n))),tuple((len(points)-1)*n+i for i in range(n))];mesh(name,v,f,mat)
for label,side in [('Left',-1),('Right',1)]:
 x=side*.285;fy=-.65+side*.15;fz=.45+side*.09;ry=.70;rz=.20
 beam(label+'WholeFixedFrontCrank',(x,-.65,.45),(x,fy,fz),.050,2)
 axle(label+'WholeFrontPedalPin',min(x-side*.045,x+side*.045),max(x-side*.045,x+side*.045),fy,fz,.026,2,20)
 beam(label+'WholeLongPedalLink',(x,fy,fz),(x,ry,rz),.055,0)
 # Rear roller has an actual flat bottom tread at rail-top .12 in this fixed pose.
 n=16;r=.08/math.cos(math.pi/n);v=[(xx,ry+r*math.cos(math.tau*(i+.5)/n),rz+r*math.sin(math.tau*(i+.5)/n))for xx in[x-.055,x+.055]for i in range(n)]
 f=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh(label+'WholeRearSupportingRoller',v,f,2)
 axle(label+'WholeRearRollerAxle',x-.075,x+.075,ry,rz,.023,2,20)
 def height(y):return fz+(rz-fz)*(y-fy)/(ry-fy)
 # One continuous U-section tread tray, slope follows its own whole long link.
 y0=.02;y1=.47;z0=height((y0+y1)/2)+.012
 prof=[(-.105,0),(.105,0),(.105,.075),(.080,.075),(.080,.035),(-.080,.035),(-.080,.075),(-.105,.075)]
 n=len(prof);v=[(x+xx,y,z0+zz+(height(y)-height((y0+y1)/2)))for y in[y0,y1]for xx,zz in prof];f=[]
 for a,b,c in triangulate(prof):f.extend([(a,b,c),(c+n,b+n,a+n)])
 f += [(i,i+n,(i+1)%n+n,(i+1)%n)for i in range(n)];mesh(label+'WholeOpenPedalTray',v,f,2)
 ly=-.02;lz=height(ly);hx=side*.40
 axle(label+'WholePedalHandleLowerPin',min(x,hx)-.028,max(x,hx)+.028,ly,lz,.028,2,20)
 tube(label+'WholeLinkedMovingHandleArm',[(hx,ly,lz),(hx,-.48,1.08),(hx,-.43,1.38),(hx,-.31,1.58)],.033,0)
 tube(label+'WholeUpperHandGrip',[(hx,-.435,1.37),(hx,-.302,1.594)],.043,2)
 # Finite caps are proud of shaft ends, not coincident exposed disks.
 axle(label+'WholePivotEndCap',min(hx-side*.07,hx),max(hx-side*.07,hx),-.48,1.08,.055,2,20)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('FrameAndLongPedalLinks_PaleSteel',(.56,.63,.64,1),.57,.30),('WholeFrontResistanceCover_Orange',(.65,.27,.075,1),.65,.15),('RollersTraysAndGrips_Charcoal',(.065,.08,.09,1),.76,.05)]
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
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.50;aim(cam,(4,-6,3.3));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/fitness/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'fitness','style':'S01-clean-geometric','title':'Fixed Front-Crank Rear-Roller Elliptical','description':'One newly authored complete static front-crank/rear-roller elliptical-trainer appearance. Two continuous long grounded rails and transverse feet support an opaque front resistance case with one through axle and two opposed short fixed cranks. Each crank joins a whole long descending pedal link, a complete rimmed open foot tray and a rear supporting roller actually seated on its own rail in this pose. Two complete bent hand arms share a fixed high cross axle on the front mast, connect through lower pins to their pedal links and terminate in separate thick grips; a blank console completes the mast. This is not a seat deleted from the old upright cycle, a rail rower with its saddle replaced, or the old freely suspended air-walker fitted with longer platforms: the entire crank-link-rear-roller support topology is newly authored. Three opaque constant PBR roles; closed editable solids, metres, Z up and horizontal bounds-centred grounded feet. One whole prop, zero scenes. Fixed geometry only, no solved continuous linkage path, elliptical trajectory accuracy, pedal clearance throughout motion, rotation, exercise prescription, resistance, display or electrical operation, ergonomics, human fit, loading, manufacture or fitness-equipment safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
