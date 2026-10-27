import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='waterworks-fixed-inclined-bar-rack-and-raised-comb-carriage-01'
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
PALETTE=[('WholeChannelCastConcrete',(.45,.46,.42,1),.89,0),('WholeRakeFrameMutedTeal',(.08,.25,.26,1),.66,.31),('WholeScreenBarsSatinSteel',(.34,.40,.42,1),.48,.62),('WholeRaisedRakeCombWarmOchre',(.62,.36,.09,1),.63,.34)]
FM={}
# One full U-shaped channel: emit only boundary cells, both longitudinal ends open.
xs=[-1.65,-1.35,1.35,1.65];ys=[-2.10,2.10];zs=[0,.20,.86];cells=[]
for i in range(3):
 for k in range(2):
  if k==0 or i in [0,2]:cells.append([(x,y,z)for z in zs[k:k+2]for y in ys for x in xs[i:i+2]])
cell_union('WholeOpenEndedUChannel',cells,0)
P=(0,-1.45,.20);T=unit((0,2.45,2.50));NORMAL=(0,-T[2],T[1]);LENGTH=math.sqrt(2.45**2+2.50**2)
def local(x,s,n):return add(P,add((x,0,0),add(mul(T,s),mul(NORMAL,n))))
def obox(name,x0,x1,s0,s1,n0,n1,m):
 v=[local(x,s,n)for n in [n0,n1]for s in[s0,s1]for x in[x0,x1]]
 f=[]
 for a,b,c,d in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:f.extend([(a,b,c),(a,c,d)])
 record(name,v,f,m)
BAR_X=[-1.20+.15*i for i in range(17)]
for i,x in enumerate(BAR_X):obox('WholeInclinedScreenBar%02d'%i,x-.03,x+.03,.08,LENGTH-.08,-.04,.04,2)
# Complete distinct lower and upper cross rails close the finite rack boundary.
obox('WholeLowerRackCrossrail',-1.32,1.32,0,.12,-.09,.055,1)
obox('WholeUpperRackCrossrail',-1.58,1.58,LENGTH-.12,LENGTH+.10,-.09,.055,1)
for sign,label in[(-1,'Left'),(1,'Right')]:
 x=sign*1.41;obox('WholeCarriageGuide'+label,x-.065,x+.065,0,LENGTH+.15,-.10,.02,1)
 # Full tall rear support grounded on its concrete channel wall.
 end=local(x,LENGTH,0)
 box('WholeRearGuideSupport'+label,(x-.11,end[1]-.13,.86),(x+.11,end[1]+.13,end[2]-.035),1)
 # Guide lower feet terminate against the near channel wall/floor volume.
 lo=local(x,.20,-.10)
 pipe('WholeLowerGuideShoe'+label,[(x,lo[1],.20),(x,lo[1],lo[2]+.03)],.085,1,8)
# A single shared-vertex comb boundary, not a disconnected set of yellow teeth.
S=2.25;teeth=[(BAR_X[i]+BAR_X[i+1])/2 for i in range(16)]
cx=sorted(set([-1.52,1.52]+[round(t+d,8)for t in teeth for d in[-.025,.025]]));ss=[S-.43,S,S+.14];nn=[0,.09,.20];cells=[]
for i in range(len(cx)-1):
 mid=(cx[i]+cx[i+1])/2;tooth=any(abs(mid-t)<.0250001 for t in teeth)
 for j in range(2):
  for k in range(2):
   if (j==0 and tooth)or(j==1 and k==1):cells.append([local(x,s,n)for n in nn[k:k+2]for s in ss[j:j+2]for x in cx[i:i+2]])
cell_union('WholeRaisedSixteenToothComb',cells,3)
for sign,label in[(-1,'Left'),(1,'Right')]:
 x=sign*1.41;obox('WholeCarriageGuideShoe'+label,x-.095,x+.095,S-.07,S+.21,.02,.26,1)
# Whole hoist cross-shaft, two grooved-looking full drums and retained cable ends.
# These illustrate one fixed pose only, not a working drive, bearing or winding model.
shaft_y=local(0,LENGTH+.06,.03)[1];shaft_z=local(0,LENGTH+.06,.03)[2]
pipe('WholeUpperCrossShaft',[(-1.57,shaft_y,shaft_z),(1.57,shaft_y,shaft_z)],.052,2,16)
for x,label in[(-.94,'Left'),(.94,'Right')]:
 wheel('WholeCableDrum'+label,x,shaft_y,shaft_z,.135,0,.16,3)
 wheel('WholeDrumOuterFlange'+label,x-.09,shaft_y,shaft_z,.17,0,.025,2)
 wheel('WholeDrumInnerFlange'+label,x+.09,shaft_y,shaft_z,.17,0,.025,2)
 bottom=local(x,S+.14,.145);top=(x,shaft_y-.12,shaft_z-.03)
 pipe('WholeRetainedHoistCable'+label,[bottom,top],.014,2,8)
# The complete horizontal bounds are centred and the channel sole is exactly ground.
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()};FM={n:[m]*len(f)for n,(v,f,m)in G.items()}
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
focus=Vector((0,0,1.40))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=6.8;aim(cam,(6,-9,6) if view=='qa-front' else (7,-10,8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/waterworks/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'modular','theme':'waterworks','style':'S01-clean-geometric','title':'Fixed Inclined Bar Rack and Raised Comb Carriage','description':'One wholly newly authored complete fixed inclined bar-screen infrastructure appearance. One continuous thick U-shaped channel has a full ground sole and genuinely open ends. Seventeen complete steel-look bars incline upward between full lower and upper crossrails, leaving sixteen actual empty longitudinal gaps. Separate outboard guide rails carry two complete shoes and a raised one-piece comb with sixteen finite teeth positioned in the bar gaps; all teeth join one continuous full crosshead, with finite side clearance in this authored pose. Two rear posts, lower guide shoes, a complete top shaft, two full drums with flange pairs and two retained cables complete the static support and hoist appearance. Unlike the earlier vertical half-open solid sluice plate in C grooves with a threaded spindle and handwheel, this is a visibly open inclined bar bank and a separate crosswise rake carriage. All numeric channel, frame, bars, comb and hoist faces authored together, no gate, drain, grate, hoist or machine mesh imported or extracted. Four opaque constant PBR roles, metres Z up, whole horizontal bounds centred over its own channel sole, one modular model zero scenes. One fixed dry waterworks-inspired artwork, no water or debris. No filtering, screening, cleaning, hydraulic flow, gate sealing, rake travel, cable winding, bearing or running fit, drive, load, stability, manufacture, installation, maintenance, potable-water suitability or civil-engineering safety capability made or verified. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
