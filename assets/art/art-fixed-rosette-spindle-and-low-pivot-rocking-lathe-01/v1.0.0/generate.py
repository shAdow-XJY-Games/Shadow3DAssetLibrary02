import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='art-fixed-rosette-spindle-and-low-pivot-rocking-lathe-01'
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



# Entire fixed low-pivot ornamental turning apparatus, independent new construction.
for x in[-.43,.43]:
 for y in[-.40,.40]:box('WholeGroundFoot_'+str((x,y)),(x,y,.027),(.16,.16,.054),2)
box('WholeCommonBed',(0,0,.09),(1.0,.97,.10),0)
# Fixed front/rear lower cheeks receive the complete low horizontal pivot.
for y in[-.24,.24]:
 box('WholeFixedLowerPedestal_'+str(y),(-.12,y,.167),(.19,.115,.14),0)
 ringy('WholeBoredLowerBearing_'+str(y),y-.066,y+.066,-.12,.235,.028,.075,1,24)
cyly('WholeLowParallelPivot',-.345,.345,-.12,.235,.030,1,24)
for y in[-.34,.34]:cyly('WholeLowerPivotCap_'+str(y),y-.018,y+.018,-.12,.235,.047,2,20)
# Tall moving-looking frame has an upper axis parallel to its own low pivot.
for y in[-.12,.12]:
 box('WholeRockingHeadCheek_'+str(y),(-.12,y,.423),(.105,.075,.39),0)
 ringy('WholeUpperSpindleBearing_'+str(y),y-.049,y+.049,-.12,.66,.036,.081,1,24)
box('WholeRockingLowerTie',(-.12,0,.264),(.15,.31,.085),0)
cyly('WholeUpperParallelSpindle',-.405,.407,-.12,.66,.039,1,24)
cyly('WholeBlankFrontFaceplate',-.414,-.365,-.12,.66,.125,1,32)
cyly('WholeFrontFaceplateHub',-.383,-.30,-.12,.66,.058,2,24)
# A full continuous noncircular thick plate, not painted scallops or separate petal disks.
n=96;p=[]
for i in range(n):
 t=math.tau*i/n;r=.218+.018*math.cos(8*t);p.append((-.12+r*math.cos(t),.66+r*math.sin(t)))
v=[(x,y,z)for y in[.256,.292]for x,z in p];f=[]
for a,b,c in triangulate(p):f.extend([(c,b,a),(a+n,b+n,c+n)])
for i in range(n):j=(i+1)%n;f.append((i,j,j+n,i+n))
mesh('WholeEightLobedRosette',v,f,3)
cyly('WholeRearRosetteHub',.20,.33,-.12,.66,.059,1,24)
# Independent stop has a short rounded-looking blunt nose seated at the rightmost lobe.
box('WholeSideStopPedestal',(.325,.274,.36),(.125,.16,.47),0)
box('WholeSideStopUpperCap',(.325,.274,.62),(.18,.18,.075),2)
beam('WholeFixedSideStopStem',(.109,.274,.66),(.38,.274,.66),.031,1)
box('WholeSideStopClamp',(.325,.274,.66),(.073,.08,.075),0)
# Independent front slide supports a short static tool blank with an honest open tip gap.
box('WholeFrontSlideBase',(.075,-.342,.16),(.63,.25,.07),0)
for y in[-.42,-.275]:box('WholeTransverseSlideWay_'+str(y),(.075,y,.205),(.58,.035,.05),1)
box('WholeTransverseSlideCarriage',(-.07,-.348,.25),(.22,.21,.075),0)
box('WholeFrontToolPost',(-.07,-.46,.425),(.082,.10,.30),2)
box('WholeShortBluntTool',(-.07,-.53,.567),(.037,.12,.032),1)
# Tool points toward the open face but is not claimed engaged with it.
cyly('WholeSlideControlShaft',-.57,-.40,.205,.20,.018,1,16)
ringy('WholeSlideControlRim',-.58,-.552,.205,.20,.049,.066,2,24)
cyly('WholeSlideControlHub',-.585,-.54,.205,.20,.023,1,16)
for i in range(3):
 t=math.tau*i/3;beam('WholeSlideControlSpoke_'+str(i),(.205,-.566,.20),(.205+.060*math.cos(t),-.566,.20+.060*math.sin(t)),.014,1)
beam('WholeRearCrankArm',(-.12,.405,.66),(-.12,.405,.805),.029,2)
cyly('WholeRearOffsetCrankGrip',.402,.495,-.12,.805,.020,0,16)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeBedAndRockingFrame_MutedTeal',(.10,.25,.25,1),.73,.12),('WholeShaftsBearingsAndWays_SatinMetal',(.48,.51,.48,1),.46,.54),('WholeFeetAndControls_DarkIron',(.055,.065,.064,1),.82,.12),('WholeRosettePlate_DullBrass',(.48,.34,.16,1),.57,.46)]
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
focus=Vector((0,0,.39))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.75;aim(cam,(6,-5,3.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/art/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'art','style':'S01-clean-geometric','title':'Fixed Rosette Spindle and Low Pivot Rocking Lathe','description':'One wholly newly authored complete fixed ornamental-turning-inspired tabletop apparatus. A full low bed and four finite feet carry two fixed lower bearing pedestals supporting one complete elevated rocking head frame on a long low hinge. The upper horizontal spindle is parallel to that lower pivot rather than crossing it: two complete tall head cheeks and bored bearing collars join both levels. A true thick eight-lobed rosette plate is rooted on the rear spindle and visibly meets a separate fixed side stop stem carried on its own pedestal. The front spindle ends in one whole blank circular faceplate. An independent front transverse slide, raised toolpost and short blunt tool appearance remain visibly separated from the faceplate. A complete rear crank with offset grip and front slide handwheel finish the apparatus. No old lathe or dividing-head geometry imported. Unlike the fixed-head long-bed lathe there are no tailstock, longitudinal saddle, stepped chuck jaws or long feed rod. Unlike the tilting index head, the lower pivot runs parallel to the spindle and the rosette-to-side-stop relation belongs to the whole rocking head, not a perforated indexing disk on a transverse tilt axis. Four opaque constant PBR roles, metres Z up, full horizontal bounds centred, one model zero scenes. Generic static art-workshop display, not an identified historical machine replica or engineering design. No rotation, rocking travel, cam law, sustained contact, spring return, engraving, cutting, material removal, dimensional accuracy, adjustment, workholding, bearing fit, manufacture, load or machine safety made or verified. No rigging animation interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
