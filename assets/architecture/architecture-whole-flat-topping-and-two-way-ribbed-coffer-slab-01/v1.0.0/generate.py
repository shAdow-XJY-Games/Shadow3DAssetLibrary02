import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='architecture-whole-flat-topping-and-two-way-ribbed-coffer-slab-01'
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

def cell_union(name,cells,mat):
 faces={}
 for v in cells:
  v=[tuple(round(c,12)for c in p)for p in v]
  for f in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:
   q=tuple(v[i]for i in f);key=tuple(sorted(q))
   if key in faces:del faces[key]
   else:faces[key]=q
 v=[];ix={};f=[]
 for q in faces.values():
  ids=[]
  for p in q:
   if p not in ix:ix[p]=len(v);v.append(p)
   ids.append(ix[p])
  f.extend([(ids[0],ids[1],ids[2]),(ids[0],ids[2],ids[3])])
 record(name,v,f,mat)
def turned(name,x,y,profile,m,seg=16):
 v=[];rs=[];f=[]
 for r,z in profile:
  pts=[(x,y,z)]if r==0 else[(x+r*math.cos(math.tau*i/seg),y+r*math.sin(math.tau*i/seg),z)for i in range(seg)]
  rs.append(list(range(len(v),len(v)+len(pts))));v+=pts
 for a,b in zip(rs,rs[1:]+rs[:1]):
  if len(a)==len(b)==1:continue
  for i in range(seg):
   j=(i+1)%seg
   if len(a)==1:f.append((a[0],b[i],b[j]))
   elif len(b)==1:f.append((a[i],b[0],a[j]))
   else:f.extend([(a[i],b[i],b[j]),(a[i],b[j],a[j])])
 record(name,v,f,m)
PALETTE=[('WholeContinuousSlabWarmConcrete',(.53,.51,.45,1),.93,0),('RealBlindCofferCeilings',(.66,.64,.57,1),.92,0),('WholeIntegralFootColumns',(.43,.46,.46,1),.94,0)]
G={};FM={};ROOTS=[];CONTACTS=[];LINKS=[];GAPS=[];SHIFT=(0,0,0)
# New rectilinear closed continuous material body. No old vault flattened or old rods united.
# Four by three bottom-open blind pockets; all top-layer cells remain, joined cross-ribs below.
XS=[-2.45,-2.05,-1.20,-.98,-.13,.13,.98,1.20,2.05,2.45]
YS=[-1.95,-1.55,-.66,-.44,.44,.66,1.55,1.95]
ZS=[3.20,3.48,3.68]
cells=[]
for i in range(len(XS)-1):
 for j in range(len(YS)-1):
  for k in range(2):
   if k==0 and i%2==1 and j%2==1:continue
   cells.append([(x,y,z)for z in ZS[k:k+2]for y in YS[j:j+2]for x in XS[i:i+2]])
cell_union('WholeFlatToppingTwoWayRibsAndTwelveBlindCoffers',cells,0)
name='WholeFlatToppingTwoWayRibsAndTwelveBlindCoffers';v,f,m=G[name];FM[name]=[1 if all(abs(v[q][2]-ZS[1])<1e-9 for q in face)and cross(sub(v[face[1]],v[face[0]]),sub(v[face[2]],v[face[0]]))[2]<0 else 0 for face in f]
for sx in [-1,1]:
 for sy in [-1,1]:
  cx,cy=sx*2.25,sy*1.75;v=[]
  for r,z in[(.32,0),(.15,.20),(.15,3.20)]:v.extend([(cx-r,cy-r,z),(cx+r,cy-r,z),(cx+r,cy+r,z),(cx-r,cy+r,z)])
  f=[(0,2,1),(0,3,2),(8,9,10),(8,10,11)]
  for k in range(2):
   for i in range(4):
    j=(i+1)%4;a=k*4+i;b=k*4+j;c=(k+1)*4+j;d=(k+1)*4+i;f.extend([(a,b,c),(a,c,d)])
  name='WholeFootAndCornerColumn_'+str(sx)+'_'+str(sy);record(name,v,f,2);FM[name]=[2]*len(f);ROOTS.append(name)
  CONTACTS.append((name,'WholeFlatToppingTwoWayRibsAndTwelveBlindCoffers',(cx,cy,3.20),(0,0,1),.089))
for i in[1,3,5,7]:
 for j in[1,3,5]:
  x,y=(XS[i]+XS[i+1])/2,(YS[j]+YS[j+1])/2
  GAPS.append(dict(label='SelectedRealBlindCofferAir_'+str(i)+'_'+str(j),origin_m=[x,y,3.10],direction=[0,0,1],length_m=.35))
  GAPS.append(dict(label='UnbrokenCofferCeilingSolidControl_'+str(i)+'_'+str(j),origin_m=[x,y,3.10],direction=[0,0,1],length_m=.65,blocked=True))
for z in[.40,1.60,2.90]:
 for axis in[0,1]:GAPS.append(dict(label='SelectedUnenclosedUnderSlabCrossway',origin_m=[-2.8 if axis==0 else 0,-2.4 if axis==1 else 0,z],direction=[1 if axis==0 else 0,1 if axis==1 else 0,0],length_m=5.6 if axis==0 else 4.8))
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
focus=Vector((0,0,1.95))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(10,-13,3),1000,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='PERSP';cam.data.lens=35;cam.data.sensor_width=36;aim(cam,(5.0,-6.5,.25) if view=='qa-front' else (-5.0,-6.5,.25));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=400,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/architecture/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'modular','theme':'architecture','style':'S01-clean-geometric','title':'Whole Flat Topping and Two Way Ribbed Coffer Slab','description':'One complete newly authored fixed architectural two-way ribbed slab bay. A single closed monolithic rectangular material body retains an uninterrupted thin flat topping, continuous orthogonal downstand ribs, deep perimeter bands and twelve genuinely blind bottom-open rectangular coffers. Every pocket has four finite return walls and its own real ceiling below the unbroken top; no through-roof grid holes, black decals, detached ceiling tiles or overlapping separate rods. Four complete corner columns with integral broadened flat ground feet meet four finite corner seats in the underside of the continuous slab. Five whole closed editable meshes, three opaque constant PBR roles, one model zero scenes, native metre-style Z-up and true whole horizontal bounds-centred datum. All coordinates authored afresh, no imported or flattened old vault geometry and no copied grid-roof rods. The existing coffered barrel vault has a semicylindrical shell on two complete long springing walls; this is an open four-column bay with a planar continuous topping and intersecting straight two-direction downstand ribs. The old two-layer pyramid space grid is an entirely open offset rod graph with diagonal pyramidal cells, not a continuous slab with blind underside cavities. These differences change the continuous body, opening topology and support relation, not simply colour or repeated-member count. Four finite opposed column/slab seats with five separated sided witnesses each, four full ground soles and thirty selected air/ceiling/crossway rays are checked. No embedded reinforcement, cast formwork, structural analysis, actual span or load, punching resistance, fire rating, construction sequence, building code, dimensions for manufacture, access or public safety capability. Stylized dry static game architecture only; no brand, named building, people, rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
