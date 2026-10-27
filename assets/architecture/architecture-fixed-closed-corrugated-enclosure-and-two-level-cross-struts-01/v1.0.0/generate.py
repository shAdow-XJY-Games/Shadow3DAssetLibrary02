import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='architecture-fixed-closed-corrugated-enclosure-and-two-level-cross-struts-01'
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
PALETTE=[('WholeClosedFoldedCurtainMutedBlueSteel',(.15,.30,.32,1),.70,.30),('WholeInternalWalerFramesDeepSteel',(.13,.18,.18,1),.59,.48),('WholeCrossStrutsAndCornerKneesWarmSteel',(.48,.32,.15,1),.66,.36),('WholeDryBaseSlabWarmConcrete',(.49,.48,.42,1),.94,0)]
FM={};JOINS=[];ROOTS=['WholeDryEnclosureFloorAndGroundSole']
box(ROOTS[0],(-3.10,-2.20,0),(3.10,2.20,.16),3)
# One continuous corrugated rectangular closed perimeter, with genuine wall thickness.
corners=[(-2.8,-1.9),(2.8,-1.9),(2.8,1.9),(-2.8,1.9)];path=[]
for edge,(a,b)in enumerate(zip(corners,corners[1:]+corners[:1])):
 dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy);n=(-dy/length,dx/length);count=6 if edge%2==0 else 4
 for j in range(count):
  for f,o in[(0,0),(.20,0),(.36,.10),(.66,.10),(.82,0)]:
   t=(j+f)/count;path.append((a[0]+dx*t+n[0]*o,a[1]+dy*t+n[1]*o))
def offset(poly,d):
 out=[]
 for i,b in enumerate(poly):
  a,c=poly[i-1],poly[(i+1)%len(poly)];v=(b[0]-a[0],b[1]-a[1]);w=(c[0]-b[0],c[1]-b[1]);lv=math.hypot(*v);lw=math.hypot(*w);nv=(-v[1]/lv,v[0]/lv);nw=(-w[1]/lw,w[0]/lw);den=1+nv[0]*nw[0]+nv[1]*nw[1];assert den>.1
  out.append((b[0]+d*(nv[0]+nw[0])/den,b[1]+d*(nv[1]+nw[1])/den))
 return out
inner=offset(path,.045);outer=offset(path,-.045);N=len(path);v=[(x,y,z)for p,z in[(outer,.10),(outer,2.94),(inner,2.94),(inner,.10)]for x,y in p];f=[]
for a,b in[(0,N),(N,2*N),(2*N,3*N),(3*N,0)]:
 for i in range(N):
  j=(i+1)%N;f.extend([(a+i,a+j,b+j),(a+i,b+j,b+i)])
wall='WholeContinuousClosedCorrugatedPerimeter';record(wall,v,f,0);JOINS.append((wall,ROOTS[0],(-2.8,-1.9,.13)))
# Each complete rectangular waler is a closed frame with a genuine large central opening.
for k,z in enumerate([1.16,2.34]):
 frame='WholeClosedInternalWalerFrame'+str(k);xs=[-2.735,-2.47,2.47,2.735];ys=[-1.835,-1.57,1.57,1.835];cells=[]
 for i in range(3):
  for j in range(3):
   if i==j==1:continue
   cells.append([(x,y,zz)for zz in[z-.09,z+.09]for y in[ys[j],ys[j+1]]for x in[xs[i],xs[i+1]]])
 cell_union(frame,cells,1)
 # Four finite overlaps into the inward folds, well away from coplanar faces.
 for edge,(a,b)in enumerate(zip(corners,corners[1:]+corners[:1])):
  count=6 if edge%2==0 else 4;dx,dy=b[0]-a[0],b[1]-a[1];le=math.hypot(dx,dy);t=.5/count;n=(-dy/le,dx/le);p=(a[0]+dx*t+n[0]*.10,a[1]+dy*t+n[1]*.10,z);JOINS.append((frame,wall,p))
 for j,x in enumerate([-1.60,0,1.60]):
  name='WholeFullWidthCrossStrut'+str(k)+'_'+str(j);box(name,(x-.085,-1.70,z-.07),(x+.085,1.70,z+.07),2)
  for y in[-1.64,1.64]:JOINS.append((name,frame,(x,y,z)))
 # Four full in-plane diagonal corner knees belong to the upper brace level.
 if k==1:
  for ix,sx in enumerate([-1,1]):
   for iy,sy in enumerate([-1,1]):
    name='WholeUpperCornerKnee'+str(ix)+'_'+str(iy);a=(sx*2.60,sy*.96,z);b=(sx*1.96,sy*1.70,z);pipe(name,[a,b],.065,2,4);JOINS.append((name,frame,(sx*2.56,sy*1.00625,z)));JOINS.append((name,frame,(sx*2.0,sy*1.65375,z)))
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()};FM={n:[m]*len(f)for n,(v,f,m)in G.items()};JOINS=[(a,b,sub(p,SHIFT))for a,b,p in JOINS]
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
focus=Vector((0,0,1.35))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=8.4;aim(cam,(8,-10,14) if view=='qa-front' else (-8,-10,16));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/architecture/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'modular','theme':'architecture','style':'S01-clean-geometric','title':'Fixed Closed Corrugated Enclosure and Two-Level Cross Struts','description':'One wholly newly authored complete dry internally-braced-cofferdam-inspired architectural display. One continuous thick corrugated rectangular perimeter closes around all four corners with a genuine open top and a full separate flat ground floor. Two complete rectangular inner waler frames run around the enclosure at separated heights, each with an actual large central opening. Three whole transverse struts at each level join the opposite long waler sides; four whole upper diagonal corner knees connect adjacent frame sides. Every wall fold, corner, waler and strut is newly authored together. The full interior remains open between the brace rows, with no soil, water or installed worksite. Unlike the prior one-sided retaining curtain with rear tie rods and separate anchors, this whole closed perimeter carries inward encircling frames and full cross-span bracing on both levels. Unlike the timber flying shore, there are no isolated wall-bearing plates, central raker/cheek joint or absent host walls. The entire finite-thickness corrugated curtain is one closed editable body, not repeated independent sheet assets or an asserted interlocking system. All numeric geometry new, no old wall, shore, tieback, basin or brace mesh imported or extracted. Four constant opaque untextured PBR appearances, metres native Z up, whole bounds-centred finite ground sole, one architectural model zero scenes. Empty static illustrative geometry only, not a construction detail or designed temporary work. No soil pressure, excavation sequence, water seal, dewatering, sheet interlock, weld, bolt, strut compression, buckling, anchoring, load, stability, access, installation, fabrication, structural or civil safety capability made or verified. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
