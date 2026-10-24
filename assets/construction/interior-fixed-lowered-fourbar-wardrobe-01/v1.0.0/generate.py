import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='interior-fixed-lowered-fourbar-wardrobe-01'
import math
N=24
G={}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def record(name,v,f,m):
 if sum(dot(v[a],cross(v[b],v[c]))for a,b,c in f)<0:f=[(a,c,b)for a,b,c in f]
 G[name]=(v,f,m)
def box(name,lo,hi,m):
 v=[(x,y,z)for z in[lo[2],hi[2]]for y in[lo[1],hi[1]]for x in[lo[0],hi[0]]];f=[]
 for a,b,c,d in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:f.extend([(a,b,c),(a,c,d)])
 record(name,v,f,m)
def pipe(name,points,r,m,segments=8):
 v=[]
 for k,p in enumerate(points):
  tangent=unit(sub(points[min(k+1,len(points)-1)],points[max(k-1,0)]));u=(1,0,0)if abs(tangent[0])<.9 else(0,1,0);u=unit(cross(tangent,u));w=cross(tangent,u)
  for i in range(segments):v.append(add(p,add(mul(u,r*math.cos(math.tau*i/segments)),mul(w,r*math.sin(math.tau*i/segments)))))
 f=[]
 for k in range(len(points)-1):
  for i in range(segments):
   j=(i+1)%segments;a=k*segments+i;b=k*segments+j;c=(k+1)*segments+j;d=(k+1)*segments+i;f.extend([(a,b,c),(a,c,d)])
 for k in [0,len(points)-1]:
  c=len(v);v.append(points[k]);base=k*segments
  for i in range(segments):f.append((c,base+(i+1)%segments,base+i)if k==0 else(c,base+i,base+(i+1)%segments))
 record(name,v,f,m)
def wheel(name,x,y,z,ro,ri,width,m):
 # Complete closed annular tire (or capped disc when ri=0), axis X.
 profile=[(ri,x-width/2),(ro,x-width/2),(ro,x+width/2),(ri,x+width/2)]
 v=[];rs=[]
 for r,xx in profile:
  ring=[(xx,y,z)]if r==0 else[(xx,y+r*math.sin(math.tau*i/N),z+r*math.cos(math.tau*i/N))for i in range(N)];rs.append(list(range(len(v),len(v)+len(ring))));v+=ring
 f=[]
 for a,b in zip(rs,rs[1:]+rs[:1]):
  if len(a)==len(b)==1:continue
  for i in range(N):
   j=(i+1)%N
   if len(a)==1:f.append((a[0],b[i],b[j]))
   elif len(b)==1:f.append((a[i],b[0],a[j]))
   else:f.extend([(a[i],b[i],b[j]),(a[i],b[j],a[j])])
 record(name,v,f,m)

def earclip(p):
 cr=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 ids=list(range(len(p)));out=[]
 while len(ids)>3:
  for j,b in enumerate(ids):
   a,c=ids[j-1],ids[(j+1)%len(ids)]
   if cr(p[a],p[b],p[c])<=1e-14:continue
   if any(all(cr(p[u],p[v],p[k])>=-1e-14 for u,v in [(a,b),(b,c),(c,a)])for k in ids if k not in [a,b,c]):continue
   out.append((a,b,c));ids.pop(j);break
  else:raise ValueError('Non-simple padding section')
 out.append(tuple(ids));return out
def pad(name,p,y0,y1,m):
 if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);v=[(x,y,z)for y in[y0,y1]for x,z in p];f=[]
 for a,b,c in earclip(p):f.extend([(a,b,c),(c+n,b+n,a+n)])
 for i in range(n):
  j=(i+1)%n;f.extend([(i,j+n,j),(i,i+n,j+n)])
 record(name,v,f,m)

# Whole open wardrobe with fixed lowered parallel-link hanging rail.
PALETTE=[('WardrobeWarmIvory',(.64,.61,.52,1),.83,0),('WardrobeTimberPlinth',(.35,.24,.14,1),.86,0),('PulldownMechanismMetal',(.22,.26,.27,1),.58,.5)]
box('WholeRecessedGroundPlinth',(-.51,.035,0),(.51,.535,.11),1)
def cells(name,axes,keep,mat):
 v=[];idx={};faces={}
 def vi(p):
  if p not in idx:idx[p]=len(v);v.append(p)
  return idx[p]
 for i in range(len(axes[0])-1):
  for j in range(len(axes[1])-1):
   for k in range(len(axes[2])-1):
    mid=[(axes[n][t]+axes[n][t+1])/2 for n,t in enumerate([i,j,k])]
    if not keep(*mid):continue
    ids=[vi((x,y,z))for z in[axes[2][k],axes[2][k+1]]for y in[axes[1][j],axes[1][j+1]]for x in[axes[0][i],axes[0][i+1]]]
    for f in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:
     q=tuple(ids[t]for t in f);key=tuple(sorted(q))
     if key in faces:del faces[key]
     else:faces[key]=q
 ff=[]
 for a,b,c,d in faces.values():ff.extend([(a,b,c),(a,c,d)])
 record(name,v,ff,mat)

cells('WholeOpenWardrobeShell',[[-.57,-.53,.53,.57],[0,.53,.57],[.11,.15,1.98,2.03]],lambda x,y,z:abs(x)>.53 or y>.53 or z<.15 or z>1.98,0)
# Each side has two equal, parallel long links between two vertical pivot stations.
# The two moving stations are joined by a whole carrier, so the lowered rail is not a dangling single bar.
Ay=.14;By=-.54
for side in[-1,1]:
 x=side*.485
 box('WholeFixedMechanismWallPlate_'+str(side),(min(x,side*.535),.08,1.27),(max(x,side*.535),.20,1.79),2)
 for j,za in enumerate([1.36,1.70]):
  zb=za-.54
  pipe('WholeFixedPivot_'+str((side,j)),[(x-.034,Ay,za),(x+.034,Ay,za)],.032,2,12)
  pipe('WholeMovingPivot_'+str((side,j)),[(x-.034,By,zb),(x+.034,By,zb)],.032,2,12)
  dy,dz=By-Ay,zb-za;ln=math.hypot(dy,dz);ny,nz=-dz/ln*.025,dy/ln*.025
  poly=[(Ay+ny,za+nz),(Ay-ny,za-nz),(By-ny,zb-nz),(By+ny,zb+nz)]
  pad('WholeParallelSwingLink_'+str((side,j)),poly,x-.013,x+.013,2);v,f,m=G['WholeParallelSwingLink_'+str((side,j))];record('WholeParallelSwingLink_'+str((side,j)),[(y,x,z)for x,y,z in v],f,m)
 box('WholeLoweredVerticalCarrier_'+str(side),(x-.020,By-.026,.79),(x+.020,By+.026,1.19),2)
# Full transverse rail is one part, carried on both moving top stations.
pipe('WholeLoweredHangingRail',[(-.505,By,1.16),(.505,By,1.16)],.022,2,16)
# A complete centrally rooted U pull descends in front; it is not a loose floating handle.
pipe('WholeLongLoweringPull',[(-.13,By,1.16),(-.13,By-.055,.65),(.13,By-.055,.65),(.13,By,1.16)],.012,2,12)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
FM={n:[m]*len(f)for n,(v,f,m)in G.items()}
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
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
triangles=sum(len(f)for v,f,m in G.values())
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
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
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.1;aim(cam,(5,-7,3.9));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/construction/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'interior','style':'S01-clean-geometric','title':'Fixed Lowered Fourbar Wardrobe','description':'One newly authored whole static open wardrobe with a lowered hanging-rail mechanism. A complete five-sided tall cabinet and grounded recessed plinth enclose a real unpartitioned chamber. Each inner side has a full mounting plate, two separated fixed pivots, two equal parallel links and a full lowered vertical carrier with two moving pivots. One complete transverse hanging rail joins the two carriers, with a long centrally attached U pull below. The lowered rail stands outside and below its upper storage location in one fixed visual pose. Unlike a locker rod resting on fixed end pads or a linear pullout tray tower, support follows two paired four-bar link arrangements. No old cabinet or clothing model reused, no clothes or room. Three opaque constant PBR materials, metres, Z-up, horizontal bounds-centred ground origin. One complete prop, zero scenes. No mechanism movement, synchronized travel, counterbalance, storage rating, reach suitability, anti-tip, load capacity, assembly, installation or safety certification is claimed.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
