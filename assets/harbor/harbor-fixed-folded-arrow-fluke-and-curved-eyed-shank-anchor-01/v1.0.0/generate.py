import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='harbor-fixed-folded-arrow-fluke-and-curved-eyed-shank-anchor-01'
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
PALETTE=[('WholeFoldedArrowFlukeMutedSteel',(.37,.43,.43,1),.68,.49),('WholeCurvedShankAndEyeDeepSteel',(.10,.19,.21,1),.58,.59)]
G={};FM={};LINKS=[];ROOTS=['WholeFoldedArrowFlukeWithIntegralFlatKeel'];GAPS=[]
# Entire arrow fluke: a blunt narrow nose, two broad complete wings, a rear
# chevron indentation, a raised central top fold and one integral flat keel sole.
rows=[]
for y,w in[(-1.15,.06),(-.80,.22),(-.30,.45),(.15,.64)]:
 c=min(.08,w/2);rows.append([(x,y)for x in[-w,-c,0,c,w]])
rows.append([(x,.30+.30*abs(x)/.82)for x in[-.82,-.08,0,.08,.82]])
plan=sum(rows,[]);v=[]
for top in[False,True]:
 for x,y in plan:z=.12+.30*(y+1.15)/1.75-.18*abs(x)if top else max(0,.25*abs(x)-.02);v.append((x,y,z))
f=[]
for k in range(4):
 for j in range(4):a=k*5+j;b=a+1;c=b+5;d=a+5;f.extend([(a,c,b),(a,d,c),(a+25,b+25,c+25),(a+25,c+25,d+25)])
edge=list(range(5))+[i*5+4 for i in range(1,5)]+list(range(23,19,-1))+[i*5 for i in range(3,0,-1)]
for a,b in zip(edge,edge[1:]+edge[:1]):f.extend([(a,b,b+25),(a,b+25,a+25)])
record(ROOTS[0],v,f,0)
# One complete rectangular-section curved shank; every ring belongs to a single
# closed material mesh rather than disconnected straight stick fragments.
path=[(.20,.30),(.42,.62),(.35,.98),(-.20,1.28),(-1.05,1.43),(-1.40,1.43)]
v=[];f=[]
for k,(y,z)in enumerate(path):
 a=path[max(k-1,0)];b=path[min(k+1,len(path)-1)];dy,dz=b[0]-a[0],b[1]-a[1];ll=math.hypot(dy,dz);ny,nz=-dz/ll,dy/ll;ww=.11-.035*k/(len(path)-1)
 for x,h in[(-.07,-ww*.65),(-.045,-ww),(.045,-ww),(.07,-ww*.65),(.07,ww*.65),(.045,ww),(-.045,ww),(-.07,ww*.65)]:v.append((x,y+h*ny,z+h*nz))
for k in range(5):
 for i in range(8):j=(i+1)%8;a=k*8+i;b=k*8+j;c=(k+1)*8+j;d=(k+1)*8+i;f.extend([(a,b,c),(a,c,d)])
for i in range(1,7):f.extend([(0,i+1,i),(40,40+i,40+i+1)])
record('WholeContinuousCurvedForwardShank',v,f,1)
N=32;wheel('WholeOpenForwardAttachmentEye',0,-1.53,1.43,.19,.095,.10,1)
def root(a,b,p,e):LINKS.append((a,b,[p]+[tuple(p[k]+(sg*e if k==ax else 0)for k in range(3))for ax in range(3)for sg in[-1,1]]))
root(ROOTS[0],'WholeContinuousCurvedForwardShank',(0,.214,.320),.003)
root('WholeContinuousCurvedForwardShank','WholeOpenForwardAttachmentEye',(0,-1.385,1.43),.003)
for y,z in[(-1.53,1.43),(-1.57,1.43),(-1.49,1.43),(-1.53,1.39),(-1.53,1.47)]:GAPS.append(dict(label='SelectedFullAttachmentEyeBore',origin_m=[-.3,y,z],direction=[1,0,0],length_m=.6))
for y,z in[(-.70,.70),(-.40,.70),(.15,.80)]:GAPS.append(dict(label='SelectedFlukeToCurvedShankOpenGap',origin_m=[-.3,y,z],direction=[1,0,0],length_m=.6))
GAPS.append(dict(label='OpenRearFlukeChevronNotch',origin_m=[0,.55,-.05],direction=[0,0,1],length_m=.50))
for y,z in[(-.50,.10),(.35,.98),(-1.53,1.59)]:GAPS.append(dict(label='FlukeShankOrEyeMaterialControl',origin_m=[-.9,y,z],direction=[1,0,0],length_m=1.8,blocked=True))
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([sub(p,SHIFT)for p in v],f,m)for n,(v,f,m)in G.items()};FM={n:[m]*len(f)for n,(v,f,m)in G.items()};LINKS=[(a,b,[sub(p,SHIFT)for p in pts])for a,b,pts in LINKS]
for g in GAPS:g['origin_m']=sub(g['origin_m'],SHIFT)
assert max(len(n.encode())for n in G)<=63
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
focus=Vector((0,0,.78))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.25;aim(cam,(5,-9,5) if view=='qa-front' else (-6,-10,6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/harbor/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'prop','theme':'harbor','style':'S01-clean-geometric','title':'Fixed Folded Arrow Fluke and Curved Eyed Shank Anchor','description':'One newly authored complete fixed plough-anchor-inspired exterior. One full thick arrow-shaped fluke has a narrow blunt nose, two broad uninterrupted wings, a real rear chevron indentation, one raised longitudinal top fold and an integral finite flat keel sole beneath its otherwise rising lower wing faces. A separate complete curved solid shank roots into the rear centre, rises and returns forward over the open space above the fluke, ending in one whole open attachment eye with a genuine transverse bore. All three complete closed meshes are newly authored together; the fluke is not two detached palms or a cropped agricultural share, and the shank is not an extracted handle or old anchor arm. No timber stock, round cupped mushroom crown, central straight mast, separate handles, landside runner, chains or plinth. Unlike the stocked twin-fluke anchor, there is no opposed pair of upturned arms and perpendicular stock; unlike the circular cupped anchor, the broad folded arrow and low forward-returning shank form a lengthwise asymmetrical profile. Unlike the agricultural plough, there is no curling longitudinal mouldboard, wood drawbeam or two rear handles. Three whole editable material meshes, two opaque constant PBR roles, metres native Z up and whole horizontal bounds-centred origin on the integral keel. One independent static model zero scenes. Generic plough-anchor vocabulary only, original artistic profile, proportions and blunt surfaces, not a branded product, replica of a museum object or maritime standard. Selected finite static roots, ground sole, bore and under-shank gaps do not establish seabed embedment, holding force, pull direction, mooring, articulation, vessel compatibility, stability, strength, casting, manufacture, salvage, anchoring procedure or maritime/public safety capability. No fluid, rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
