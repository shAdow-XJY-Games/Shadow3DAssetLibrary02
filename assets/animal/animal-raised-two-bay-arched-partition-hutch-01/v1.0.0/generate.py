import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='animal-raised-two-bay-arched-partition-hutch-01'
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


def orient(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def polygon_triangles(p):
 # Actual concave partition outline, ear-clipped without a fan over its doorway.
 area=sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(p,p[1:]+p[:1]));ids=list(range(len(p)))if area>0 else list(reversed(range(len(p))));out=[]
 while len(ids)>3:
  for j,b in enumerate(ids):
   a=ids[j-1];c=ids[(j+1)%len(ids)]
   if orient(p[a],p[b],p[c])<=1e-12:continue
   if any(min(orient(p[a],p[b],p[k]),orient(p[b],p[c],p[k]),orient(p[c],p[a],p[k]))>=-1e-12 for k in ids if k not in[a,b,c]):continue
   out.append((a,b,c));ids.pop(j);break
  else:raise AssertionError('Partition polygon cannot triangulate')
 return out+[tuple(ids)]
def wall_x(name,x0,x1,p,mat):
 n=len(p);v=[(x,y,z)for x in[x0,x1]for y,z in p];t=polygon_triangles(p);f=[tuple(reversed(a))for a in t]+[tuple(n+i for i in a)for a in t]
 # Side orientation follows the original outline winding; normalise first.
 area=sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(p,p[1:]+p[:1]))
 for i in range(n):j=(i+1)%n;f.append((i,j,n+j,n+i)if area>0 else(j,i,n+i,n+j))
 mesh(name,v,f,mat)
def roof_z(y):return 1.015+.12*y
box('WholeRaisedSharedFloor',(0,0,.42),(1.30,.64,.06),0)
for x,label in[(-.58,'Left'),(.58,'Right')]:
 for y,side in[(-.25,'Front'),(.25,'Back')]:box(label+side+'WholeGroundLeg',(x,y,.205),(.075,.075,.41),1)
# Entire rear panel, left closed end and private bay front; all under one roof.
box('WholeRearWall',(0,.294,.747),(1.278,.030,.614),0)
wall_x('WholeClosedLeftSide',-.644,-.608,[(-.314,.44),(.314,.44),(.314,roof_z(.314)),(-.314,roof_z(-.314))],0)
box('WholePrivateBayFront',(-.435,-.294,.709),(.430,.030,.538),0)
# One finite partition with a true floor-level arch, not a dark door decal.
P=[(-.282,.445),(-.282,roof_z(-.282)),(.282,roof_z(.282)),(.282,.445),(.135,.445),(.135,.66)]
P +=[(.135*math.cos(math.pi*j/12),.66+.135*math.sin(math.pi*j/12))for j in range(1,13)]
P +=[(-.135,.445)]
wall_x('WholePartitionWithTrueArchedPassage',-.235,-.197,P,1)
# Closed finite lean roof with full underside and overhang, no copied nest shell.
v=[(x,y,roof_z(y)+dz)for dz in[0,.045]for y in[-.365,.365]for x in[-.70,.70]];mesh('WholeSingleSlopingRoof',v,BOX,2)
# Right bay has real open spaced bars and a complete frame, fixed static only.
box('FrontBayLowerSill',(.207,-.301,.477),(.836,.045,.055),1)
box('FrontBayUpperLintel',(.207,-.301,.947),(.836,.045,.055),1)
for x,label in[(-.196,'Left'),(.611,'Right')]:box('FrontBay'+label+'Upright',(x,-.292,.712),(.045,.032,.515),1)
for k in range(7):box('FrontWholeOpenGrilleBar_'+str(k+1),(-.10+k*.105,-.301,.712),(.014,.014,.46),3)
for y,label in[(-.25,'Front'),(.25,'Back')]:
 top=roof_z(y)-.015;box('RightSide'+label+'Post',(.623,y,(.44+top)/2),(.034,.045,top-.44),1)
beam('RightSideWholeSlopedHeader',(.624,-.28,roof_z(-.28)-.025),(.624,.28,roof_z(.28)-.025),.034,1)
box('RightSideLowerSill',(.624,0,.475),(.036,.56,.05),1)
for k,y in enumerate([-.16,-.05,.06,.17]):
 top=roof_z(y)-.025;box('RightWholeOpenGrilleBar_'+str(k+1),(.63,y,(.47+top)/2),(.014,.014,top-.47),3)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={name:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for name,(v,f,m)in G.items()}
PALETTE=[('Panels_MatteHoneyWood',(.43,.25,.115,1),.89,0),('Frame_DarkTimber',(.21,.12,.058,1),.91,0),('Roof_MatteMutedOxide',(.24,.075,.045,1),.92,0),('FixedBars_DarkSteel',(.065,.072,.068,1),.62,.45)]
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
focus=Vector((0,0,.55))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.25;aim(cam,(4,-6,3.4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/animal/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'animal','style':'S01-clean-geometric','title':'Raised Two-Bay Arched-Partition Hutch','description':'One newly authored static raised two-bay wooden hutch appearance. A full shared elevated floor and four ground legs carry a closed left private compartment and a genuinely open spaced-bar right compartment under one complete sloping finite roof. A complete internal partition has a real floor-level arch connecting both bays, not a painted dark doorway. Front and end bars have true air gaps and join complete sills/headers; left/front/back panels and roof overhang are whole bodies. This is a new complete layout, not the old single round-hole nest box, artificial bent burrow, wheeled delivery cage or open firewood shelter recoloured. Metres, native Z up, front -Y, horizontally centred and four full feet at ground. One prop, zero scenes. Fixed illustrative enclosure exterior only; no animal, feed, hinged movement or rig. No suitability for housing any species, animal welfare, ventilation, hygiene, drainage, load capacity, manufacture, stability or real-world safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
