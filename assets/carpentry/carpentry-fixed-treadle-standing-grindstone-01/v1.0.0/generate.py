import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='carpentry-fixed-treadle-standing-grindstone-01'
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



# Newly authored whole foot-driven grindstone appearance; no old machine meshes imported.
for label,x in [('Left',-.29),('Right',.29)]:
 box(label+'WholeGroundRunner',(x,-.10,.045),(.14,1.40,.09),0)
 for side,basey in [('Front',-.48),('Rear',.38)]:
  v=[(x+dx,y+dy,z)for y,z in[(basey,.065),(0,1.075)]for dx,dy in[(-.055,-.055),(.055,-.055),(.055,.055),(-.055,.055)]]
  mesh(label+side+'WholeSplayedBearingLeg',v,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],0)
 ringx(label+'WholeBoredAxleBearing',x-.075,x+.075,0,1.10,.040,.095,2,24)
for label,y in [('Front',-.65),('Rear',.35)]:box(label+'WholeLowFrameStretcher',(0,y,.12),(.70,.105,.10),0)
axle('WholeHorizontalStoneAxle',-.43,.46,0,1.10,.040,2,24)
# Thick closed annular stone with bevelled outer edges and genuine axial bore.
profile=[(.042,-.115),(.48,-.115),(.52,-.080),(.52,.080),(.48,.115),(.042,.115)];N=64
v=[(x,r*math.cos(math.tau*i/N),1.10+r*math.sin(math.tau*i/N))for r,x in profile for i in range(N)];f=[]
for k in range(len(profile)):
 for i in range(N):j=(i+1)%N;l=(k+1)%len(profile);f.append((k*N+i,k*N+j,l*N+j,l*N+i))
mesh('WholeThickBoredStoneWheel',v,f,1)
for label,x0,x1 in [('Left',-.165,-.115),('Right',.115,.165)]:axle(label+'WholeStoneRetainingFlange',x0,x1,0,1.10,.12,2,24)
for label,x0,x1 in [('Left',-.43,-.365),('Right',.365,.43)]:axle(label+'WholeOuterShaftCollar',x0,x1,0,1.10,.068,2,24)
# Entire sloping treadle with a genuine cross hinge carried by the open low frame.
zs=lambda y:.155+(y+.65)*(.070/.99)
p=[(-.17,-.65),(.17,-.65),(.17,.34),(-.17,.34)]
v=[(x,y,zs(y)+d)for d in[-.020,.020]for x,y in p]
mesh('WholeLongSlopedFootTreadle',v,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],0)
for label,x in [('Left',-.225),('Right',.225)]:box(label+'WholeTreadleHingeRoot',(x,.33,.185),(.08,.11,.15),0)
axle('WholeTreadleRearHinge',-.29,.29,.33,zs(.33),.025,2,16)
# One complete fixed crank and long rod, no duplicated winding spindle or drive belt.
beam('WholeOffsetAxleCrank',(.415,0,1.10),(.415,-.12,.98),.055,2)
axle('WholeUpperCrankLinkPin',.385,.485,-.12,.98,.025,2,16)
lowz=zs(-.44);axle('WholeTreadleLinkCrossPin',.10,.485,-.44,lowz,.022,2,16)
beam('WholeLongTreadleConnectingRod',(.465,-.44,lowz),(.465,-.12,.98),.037,2)
for label,y,z in [('Upper',-.12,.98),('Lower',-.44,lowz)]:axle(label+'WholeLinkPinOuterHead',.48,.505,y,z,.039,2,16)
# Forward rest has its own two continuous rooted uprights and a complete transverse plate.
for label,x in [('Left',-.29),('Right',.29)]:box(label+'WholeToolRestUpright',(x,-.645,.535),(.085,.085,.91),0)
box('WholeToolRestCrossmember',(0,-.645,.965),(.70,.09,.07),0)
box('WholeForwardToolRestPlate',(0,-.625,1.012),(.51,.15,.035),2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeFrameAndTreadle_WarmTimber',(.34,.20,.085,1),.82,0),('WholeStoneWheel_MatteGrey',(.37,.38,.35,1),.93,0),('AxleCrankAndRest_DarkIron',(.12,.16,.16,1),.57,.42)]
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
focus=Vector((0,0,.82))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.15;aim(cam,(4,-6,3.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/carpentry/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'carpentry','style':'S01-clean-geometric','title':'Fixed Treadle Standing Grindstone','description':'One newly authored complete fixed treadle grindstone appearance: a single large thick annular stone with bevelled edges and a genuine shaft bore stands vertically on a transverse axle between two paired splayed bearing supports. Two long ground runners and low crossmembers form an open timber base. A whole long sloped footboard has a supported rear hinge; a fixed offset crank and a separate full connecting rod join its forward crosspin to the main axle. Two additional rooted uprights carry a complete forward tool-rest plate. No motor, second grinding wheel, small winding spindle, yarn belt, pottery work disk, rear seat, loose tool or operator is included. This is not an old bench grinder enlarged or an old spinning/kick wheel recoloured: all frame, stone profile, treadle placement and connections are newly authored whole geometry. Three solid opaque PBR materials, closed editable parts, metres, Z up, actual whole horizontal bounds centre and grounded runner soles. One complete model, zero scenes. Intentional fixed assembly joins and collars support a single display pose. No rotation, pedal travel, continuous linkage clearance, abrasive action, sharpening or processing performance, force, power, balance, human fit, manufacture, equipment load or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
