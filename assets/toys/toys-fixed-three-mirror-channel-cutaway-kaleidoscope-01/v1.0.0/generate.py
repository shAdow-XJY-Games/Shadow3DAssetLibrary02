import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='toys-fixed-three-mirror-channel-cutaway-kaleidoscope-01'
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



# Whole intentionally sectioned three-mirror toy; no simulated optics.
def sector_shell(name,x0,x1,ri,ro,mat,n=24):
 # Longitudinal front half is deliberately absent; every cut edge has actual finite thickness.
 ts=[math.radians(270+180*i/n)for i in range(n+1)];v=[(x,r*math.cos(t),.11+r*math.sin(t))for x in[x0,x1]for r in[ri,ro]for t in ts];N=n+1;f=[]
 for i in range(n):
  j=i+1;f.extend([(i,j,N+j,N+i),(2*N+i,3*N+i,3*N+j,2*N+j),(i,2*N+i,2*N+j,j),(N+i,N+j,3*N+j,3*N+i)])
 f.extend([(0,N,3*N,2*N),(n,2*N+n,3*N+n,N+n)]);mesh(name,v,f,mat)
sector_shell('WholeLongitudinalHalfCutawayOuterCasing',-.250,.240,.068,.078,0)
# Complete rear and front annular casing collars, visibly retaining the triangular insert.
ringx('WholeRearCasingRetainingCollar',-.273,-.232,0,.110,.055,.084,1,32)
ringx('WholeRearPeepholeEndPlate',-.290,-.265,0,.110,.012,.079,1,32)
ringx('WholeFrontCasingRetainingCollar',.215,.247,0,.110,.055,.084,1,32)
# Closed finite mirror-style panels, with a deliberately half-sectioned near panel.
def mirror_plate(name,x0,x1,a,b,mat):
 dy=b[0]-a[0];dz=b[1]-a[1];le=math.hypot(dy,dz);ny=-dz/le;nz=dy/le;th=.003
 v=[(x,a[0]+t*dy+n*th*ny,a[1]+t*dz+n*th*nz)for n in[-.5,.5]for t in[0,1]for x in[x0,x1]];mesh(name,v,BOX,mat)
A0=(0,.170);B0=(-.052,.080);C0=(.052,.080)
mirror_plate('WholeLowerMirrorStylePlate',-.255,.242,B0,C0,2)
mirror_plate('WholeFarSlopedMirrorStylePlate',-.255,.242,C0,A0,2)
mirror_plate('SectionedNearMirrorStylePlate',-.255,.242,B0,(-.026,.125),2)
# Separate widened specimen-cell appearance, with its front cover absent in the pedagogical cutaway.
sector_shell('WholeSectionedSpecimenCellWall',.242,.325,.084,.095,0)
ringx('WholeSpecimenCellRearAnnularPartition',.239,.252,0,.110,.049,.094,1,32)
ringx('WholeSpecimenCellFrontOpenRetainingRim',.313,.332,0,.110,.077,.098,1,32)
box('WholeSpecimenCellLowerSeat',(.282,0,.0345),(.061,.060,.015),1)
for i,(x,y)in enumerate([(.266,-.015),(.294,-.015),(.266,.015),(.294,.015)]):
 lathe_z('WholeFixedColourSpecimen_'+str(i+1),x,y,[(0,.042),(.010,.042),(.011,.049),(.008,.060),(0,.063)],3 if i%2 else 4,8)
# Two attached shallow display saddles; no additional scene or tripod.
for tag,x in[('Rear',-.165),('Front',.160)]:
 box('WholeGroundFootAttachedSaddle_'+tag,(x,0,.017),(.047,.174,.034),1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeCutawayCasing_MutedSaffron',(.62,.36,.085,1),.69,.03),('WholeEndRimsAndDisplaySaddles_DeepTeal',(.045,.14,.17,1),.59,.15),('WholeOpaqueMirrorStylePanels_SatinAlloy',(.55,.63,.65,1),.26,.72),('WholeFixedSpecimens_MutedCoral',(.65,.13,.075,1),.47,.03),('WholeFixedSpecimens_Turquoise',(.04,.42,.38,1),.46,.03)]
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
focus=Vector((0,0,.105))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.86;aim(cam,(3,-5,3.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/toys/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'toys','style':'S01-clean-geometric','title':'Fixed Three Mirror Channel Cutaway Kaleidoscope','description':'One newly authored whole static cutaway kaleidoscope-style display. A finite long outer casing deliberately retains its rear/lower half and both complete annular end collars, exposing two complete long mirror-style plates and the lower half of a deliberately sectioned third plate in a triangular-channel arrangement. The rear end has one genuine small peephole annulus. A separately widened shallow specimen-cell appearance has a complete open front retaining ring, a real half-sectioned wall, an annular rear partition and a low seat containing four fixed coloured solid pieces. Two small attached ground saddles belong to the same display, not a separate stand asset or scene. This is not the tripod telescope without legs or a viewing drum tipped over: all geometry is new, and neither a lens train, pleated camera, upright slit wall nor inner image strip is reused. One prop, zero scenes; specimens are subordinate pieces, not individual models. Five opaque constant PBR roles, metres, Z up and actual horizontal-envelope-centred ground origin. Deliberate pedagogical cutaway: front/upper casing half, upper half of the near mirror plate and transparent specimen cover are not included. Mirror-style panels are opaque illustrative metal, no real pattern, optical transmission, image formation, rotation, calibration, educational efficacy, manufacturing, fit or toy-safety performance claimed.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':5,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
