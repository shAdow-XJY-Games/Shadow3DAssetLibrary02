import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='beach-fixed-offset-arched-arm-parasol-01'
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


# Whole new side-borne parasol. No geometry imported from the central-pole parasol.
CX=.55
box('WholeGroundedBallast',(-1.15,0,.09),(1.0,1.10,.18),3)
def sweep(name,path,width,depth,mat):
 v=[];f=[]
 for j,p in enumerate(path):
  a=path[max(0,j-1)];b=path[min(len(path)-1,j+1)];t=unit(sub(b,a));side=(0,1,0)if abs(t[1])<.8 else(1,0,0);side=unit(sub(side,tuple(dot(side,t)*q for q in t)));normal=cross(t,side)
  for sn,ss in[(-1,-1),(1,-1),(1,1),(-1,1)]:v.append(tuple(p[k]+sn*depth/2*normal[k]+ss*width/2*side[k]for k in range(3)))
 f=[(3,2,1,0),tuple((len(path)-1)*4+i for i in range(4))]
 for j in range(len(path)-1):
  for i in range(4):k=(i+1)%4;f.append((4*j+i,4*j+k,4*(j+1)+k,4*(j+1)+i))
 mesh(name,v,f,mat)
# A continuous heavy rectangular arch rises outside the canopy and reaches above its crown.
sweep('WholeOffsetContinuousArchedMast',[(-1.15,0,.12),(-1.15,0,1.50),(-1.12,0,2.25),(-.96,0,2.78),(-.60,0,3.12),(-.12,0,3.30),(.30,0,3.31),(.55,0,3.18)],.14,.14,2)
lathe_z('WholeCrownSuspensionStem',CX,0,[(0,2.54),(.026,2.54),(.026,3.22),(0,3.22)],2,16)
lathe_z('WholeUpperRibCrown',CX,0,[(0,2.90),(.095,2.90),(.095,2.96),(0,2.96)],2,24)
lathe_z('WholeFixedLowerStretcherHub',CX,0,[(0,2.54),(.075,2.54),(.075,2.63),(0,2.63)],2,24)
# Rectangular-plan shallow dome with complete finite thickness and scalloped edge.
EDGE=[(1.10,0),(1.10,.95),(0,.95),(-1.10,.95),(-1.10,0),(-1.10,-.95),(0,-.95),(1.10,-.95)]
PROFILE=[(.10,2.955),(.40,2.85),(.70,2.64),(1.0,2.40)];N=32;v=[];f=[];L=1+4*N
for top in[False,True]:
 v.append((CX,0,2.97+(.022 if top else 0)))
 for t,z in PROFILE:
  for i in range(N):
   k=i//4;u=(i%4)/4;a=EDGE[k];b=EDGE[(k+1)%8];sag=math.sin(math.pi*u);scale=t*(1-.025*sag*t*t)
   x=(a[0]*(1-u)+b[0]*u)*scale;y=(a[1]*(1-u)+b[1]*u)*scale
   v.append((CX+x,y,z-.025*sag*t*t+(.022 if top else 0)))
for level in[0,1]:
 off=level*L
 for i in range(N):
  j=(i+1)%N;q=(off,off+1+i,off+1+j);f.append(q if level else q[::-1])
 for k in range(3):
  for i in range(N):
   j=(i+1)%N;a=off+1+k*N+i;b=off+1+k*N+j;c=off+1+(k+1)*N+j;d=off+1+(k+1)*N+i
   for q in[(a,d,c),(a,c,b)]:f.append(q if level else q[::-1])
for i in range(N):j=(i+1)%N;a=1+3*N+i;b=1+3*N+j;f.append((a,b,L+b,L+a))
mesh('WholeRectangularDomeClosedCanopy',v,f,0)
# Integral alternating panel assignments are not separate shell overlays.
vv,ff,mi=G['WholeRectangularDomeClosedCanopy'];FM['WholeRectangularDomeClosedCanopy']=[]
for face in ff:
 c=tuple(sum(vv[j][k]for j in face)/3 for k in range(3));theta=math.atan2(c[1]/.95,(c[0]-CX)/1.10);FM['WholeRectangularDomeClosedCanopy'].append(int((theta+math.tau)%math.tau/(math.pi/2))%2)
for i,(x,y)in enumerate(EDGE):
 # Centers are tucked 11mm under the actual rib-line canopy underside; 18mm half-depth.
 path=[(CX+x*.055,y*.055,2.96175-.011)]+[(CX+x*t,y*t,z-.011)for t,z in PROFILE]
 sweep('WholeCurvedUnderCanopyRib_'+str(i+1),path,.028,.036,2)
 # The fixed stretcher ends inside the full rib at t=.55,z2.745.
 direction=unit((x,y,0));a=(CX+.055*direction[0],.055*direction[1],2.61);b=(CX+x*.55,y*.55,2.734)
 beam('WholeFixedDiagonalStretcher_'+str(i+1),a,b,.025,2)
# Full assembly origin is the horizontal bounds centre at the base sole.
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('Canopy_WarmSand',(.77,.67,.45,1),.82,0),('Canopy_MutedIvory',(.82,.79,.65,1),.82,0),('ArmAndRibs_DarkBronze',(.18,.20,.19,1),.48,.45),('Ballast_CharcoalStone',(.13,.15,.14,1),.90,0)]
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
focus=Vector((0,0,1.65))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=4.45;aim(cam,(4,-7,3.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/beach/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'beach','style':'S01-clean-geometric','title':'Fixed Offset Arched-Arm Parasol','description':'One newly authored complete static cantilever parasol. A broad side ballast carries one continuous curved rectangular mast that rises outside the shade footprint and arches above its crown. A short fixed suspension stem, upper rib crown and lower stretcher hub hang a full thick rectangular-plan domed canopy with eight complete curved ribs and eight fixed diagonal stretchers. There is no ground-reaching central pole below the canopy. This is a whole side-supported structure, not the old central-pole umbrella moved sideways, resized, recoloured or repeated; no old umbrella geometry is imported. The canopy is one closed finite-thickness shell with integral muted panel materials and a lightly scalloped edge, not independent overlapping sheets. Twenty-two closed editable parts, four opaque solid PBR materials, metres, Z up and horizontal-bounds-centred ground origin. One complete prop, zero scenes. One fixed open visual only: no folding, crank, latch or hinge motion, fabric physics, ballast sufficiency, stability, wind/rain/UV protection, person clearance, installation, manufacture, loading or public-space safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
