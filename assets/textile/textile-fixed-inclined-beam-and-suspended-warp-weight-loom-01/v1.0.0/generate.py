import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='textile-fixed-inclined-beam-and-suspended-warp-weight-loom-01'
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



# Whole inclined frame with an open lower hanging field, not a bounded rectangle.
for side,x in [('Left',-.72),('Right',.72)]:
 box(side+'WholeGroundFootRunner',(x,.12,.045),(.18,.95,.09),0)
 beam(side+'WholeInclinedStandard',(x,-.20,.07),(x,.22,1.96),.105,0)
 beam(side+'WholeRearBrace',(x,.55,.075),(x,.16,1.70),.085,0)
 box(side+'WholeBeamBearing',(x,.20,1.86),(.15,.19,.18),0)
 beam(side+'WholeHeddleBracket',(x,.02,1.05),(x,-.26,1.05),.052,0)
box('WholeRearLowCrossTie',(0,.48,.19),(1.50,.075,.085),0)
axle('WholeUpperWindingBeam',-.84,.84,.20,1.86,.076,0,24)
for side in[-1,1]:axle('WholeUpperBeamCollar'+str(side),side*.80-.018,side*.80+.018,.20,1.86,.095,0,20)
axle('WholeLowerShedBar',-.75,.75,-.12,.89,.025,0,16)
for side,x in [('Left',-.72),('Right',.72)]:beam(side+'WholeShedBracket',(x,-.02,.89),(x,-.12,.89),.05,0)
axle('WholeProjectingHeddleRod',-.78,.78,-.26,1.05,.022,0,16)
# Cloth is a continuous thick bent sheet rooted around the upper winding beam.
path=[(.25,1.88),(.20,1.94),(.13,1.89),(.12,1.76),(.035,1.30)];v=[]
for y,z in path:v.extend([(-.59,y-.009,z),(.59,y-.009,z),(.59,y+.009,z),(-.59,y+.009,z)])
f=[(3,2,1,0),(16,17,18,19)]+[(4*j+i,4*j+(i+1)%4,4*(j+1)+(i+1)%4,4*(j+1)+i)for j in range(4)for i in range(4)];mesh('WholeBentUpperClothDisplay',v,f,3)
def wire(name,path,r,mat):
 closed=path[0]==path[-1]
 if closed:path=path[:-1]
 N=8;v=[];f=[]
 for k,p in enumerate(path):
  w=unit(sub(path[(k+1)%len(path)] if closed else path[min(k+1,len(path)-1)],path[(k-1)%len(path)] if closed else path[max(0,k-1)]));u=unit(cross(w,(1,0,0) if abs(w[0])<.9 else (0,1,0)));q=cross(w,u)
  for j in range(N):v.append(tuple(p[i]+r*(u[i]*math.cos(math.tau*j/N)+q[i]*math.sin(math.tau*j/N))for i in range(3)))
 for k in range(len(path) if closed else len(path)-1):
  for j in range(N):f.append((k*N+j,k*N+(j+1)%N,((k+1)%len(path))*N+(j+1)%N,((k+1)%len(path))*N+j))
 if not closed:f +=[tuple(reversed(range(N))),tuple((len(path)-1)*N+j for j in range(N))]
 mesh(name,v,f,mat)
# Six full thick pierced weights with a true off-centre through hole.
for k in range(6):
 x=-.475+.19*k;y=-.13 if k%2==0 else .055;z=.34+(k%2)*.035;N=24
 outer=[(x+.073*math.cos(math.tau*j/N),z+.125*math.sin(math.tau*j/N))for j in range(N)]
 inner=[(x+.021*math.cos(math.tau*j/N),z+.063+.021*math.sin(math.tau*j/N))for j in range(N)]
 v=[(xx,yy,zz)for yy in[y-.035,y+.035]for loop in[outer,inner]for xx,zz in loop];f=[]
 for j in range(N):
  q=(j+1)%N;f +=[(j,q,N+q,N+j),(2*N+j,3*N+j,3*N+q,2*N+q),(j,2*N+j,2*N+q,q),(N+j,N+q,3*N+q,3*N+j)]
 mesh('WholePiercedHangingClayWeight_'+str(k),v,f,2)
 for h in[-1,1]:
  xx=x+h*.023
  wire('WholeContinuousWarp_'+str(k)+'_'+str(h),[(xx,.036,1.315),(xx,-.155 if k%2==0 else .04,.94),(xx,y,z+.112)],.0045,1)
 # Small closed loop encircles the top bridge and passes through the real hole.
 loop=[(x,y+.038,z+.065),(x,y+.038,z+.127),(x,y-.038,z+.127),(x,y-.038,z+.065),(x,y+.038,z+.065)]
 wire('WholeWeightBinding_'+str(k),loop,.004,1)
 if k%2==0:
  # Whole elongated closed heddle loop from projecting rod to the active warp pair.
  loop=[(x-.029,-.26,1.067),(x+.029,-.26,1.067),(x+.029,-.145,.985),(x-.029,-.145,.985),(x-.029,-.26,1.067)]
  wire('WholeHeddleLoop_'+str(k),loop,.004,1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeFrame_WarmTimber',(.40,.25,.13,1),.88,0),('WholeWarpAndBindings_Cream',(.76,.69,.52,1),.97,0),('WholePiercedWeights_Clay',(.43,.23,.13,1),.97,0),('WholeCloth_MutedTeal',(.13,.29,.27,1),.98,0)]
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
focus=Vector((0,0,.95))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.65;aim(cam,(3,-7,3.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/textile/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'textile','style':'S01-clean-geometric','title':'Fixed Inclined Beam and Suspended Warp Weight Loom','description':'One newly authored complete warp-weighted upright textile loom in a single fixed display pose. Two long finite feet carry inclined full standards and independent rear braces, with a complete upper transverse winding beam and a short folded woven-cloth appearance. Twelve continuous thick warp strands descend from that cloth edge; alternate paths pass in front of a distinct low shed bar, and six complete thick perforated clay-looking weights terminate the paired hanging strands. Each weight has a genuine open upper hole and continuous whole material rim, not a painted circle. Short side brackets hold a separate projecting heddle rod and individual closed elongated heddle loops around the alternate strand lanes. Unlike the old bounded flat loom, there is no lower beam fixing the warp ends: the open lower field and independently hanging weights define the full silhouette and support relation. Unlike the fore-aft treadle loom there are no rear warp drum, floor treadles, twin castle shafts or reed-beater assembly. All coordinates authored for this one complete inclined weighted apparatus, no old frame or cloth meshes copied. Four opaque solid PBR materials, metres Z up, horizontal bounds-centred ground origin. One static cultural-craft prop zero scenes. Generic illustrative construction, no historical reconstruction, working weave, tension equilibrium, weight suspension safety, shed movement, cloth simulation, ergonomics, manufacture or safe use; rigging animation interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
