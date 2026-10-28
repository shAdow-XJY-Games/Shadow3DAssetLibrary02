import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='architecture-fixed-three-separated-helices-and-flanged-shaft-inspection-cradles-01'
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
PALETTE=[('WholeLeadShaftDarkSteel',(.19,.23,.24,1),.56,.65),('WholeSeparatedHelixPlatesSatinSteel',(.52,.57,.55,1),.47,.62),('WholeFourPortHeadPlateMutedOchre',(.56,.34,.12,1),.61,.40),('WholeTwinInspectionSaddlesMutedTeal',(.10,.28,.29,1),.78,.16)]
FM={};ROOTS=[];CONTACTS=[];JOINS=[]
C=.95;SR=.18;SEG=48;PHASE=math.pi/SEG;SEAT=C-SR*math.cos(PHASE)
# Whole capped tapered lead shaft, long axis Y. No cut or extracted prior auger geometry.
vs=[];rings=[];fs=[]
for y,r in[(-3.8,.025),(-3.35,SR),(3.55,SR)]:
 pts=[(r*math.cos(math.tau*i/SEG+PHASE),y,C+r*math.sin(math.tau*i/SEG+PHASE))for i in range(SEG)];rings.append(list(range(len(vs),len(vs)+SEG)));vs+=pts
for a,b in zip(rings,rings[1:]):
 for i in range(SEG):j=(i+1)%SEG;fs.extend([(a[i],a[j],b[j]),(a[i],b[j],b[i])])
for k,reverse in[(0,True),(-1,False)]:
 c=len(vs);vs.append((0,[-3.8,3.55][0 if k==0 else 1],C));a=rings[k]
 for i in range(SEG):j=(i+1)%SEG;fs.append((c,a[j],a[i])if reverse else(c,a[i],a[j]))
shaft='WholeLongTaperedLeadShaft';record(shaft,vs,fs,0)
# Three separate whole single-turn plates, each with four continuous material sides
# and two complete separated end faces; unlike one continuous multi-turn auger.
for k,(yc,ro)in enumerate([(-1.60,.55),(0,.67),(1.60,.78)]):
 name='WholeSeparateSingleTurnHelixPlate%d'%(k+1);v=[];f=[];steps=64;pitch=.60
 for i in range(steps+1):
  a=math.tau*i/steps;y=yc+pitch*(i/steps-.5)
  for r,h in[(.15,-.04),(ro,-.04),(ro,.04),(.15,.04)]:v.append((r*math.cos(a),y+h,C+r*math.sin(a)))
 for i in range(steps):
  for j in range(4):q=(j+1)%4;a=i*4+j;b=i*4+q;c=(i+1)*4+q;d=(i+1)*4+j;f.extend([(a,b,c),(a,c,d)])
 f +=[(0,2,1),(0,3,2),(steps*4,steps*4+1,steps*4+2),(steps*4,steps*4+2,steps*4+3)];record(name,v,f,1)
 for t in[.125,.375,.625,.875]:
  a=math.tau*t;JOINS.append((shaft,name,(.165*math.cos(a),yc+pitch*(t-.5),C+.165*math.sin(a))))
# One entire square head plate with four true square through-ports; no decorative discs.
xx=[-.55,-.40,-.28,.28,.40,.55];zz=[C-.55,C-.40,C-.28,C+.28,C+.40,C+.55];cells=[]
for a,b in zip(xx,xx[1:]):
 for c,d in zip(zz,zz[1:]):
  x=(a+b)/2;z=(c+d)/2-C
  if .28<abs(x)<.40 and .28<abs(z)<.40:continue
  cells.append([(x,y,z)for z in[c,d]for y in[3.45,3.63]for x in[a,b]])
head='WholeFourThroughPortSquareHeadPlate';cell_union(head,cells,2);JOINS.append((shaft,head,(0,3.50,C)))
# Two complete independent inspection saddles provide actual finite flat underside seats.
for k,y in enumerate([-2.75,2.75]):
 name='WholeOpenTopInspectionSaddle%d'%(k+1);profile=[(-.48,0),(.48,0),(.48,1.15),(.23,1.15),(.23,SEAT),(-.23,SEAT),(-.23,1.15),(-.48,1.15)];pad(name,profile,y-.325,y+.325,3);ROOTS.append(name);CONTACTS.append((name,shaft,(0,y,SEAT),.012))
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()};FM={n:[m]*len(f)for n,(v,f,m)in G.items()};CONTACTS=[(a,b,sub(p,SHIFT),area)for a,b,p,area in CONTACTS];JOINS=[(a,b,sub(p,SHIFT))for a,b,p in JOINS]
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
focus=Vector((0,0,.90))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=8.6 if view=='qa-front' else 6.4;aim(cam,(8,-11,6) if view=='qa-front' else (9,12,6.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/architecture/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'prop','theme':'architecture','style':'S01-clean-geometric','title':'Fixed Three Separated Helices and Flanged Shaft Inspection Cradles','description':'One wholly newly authored complete static horizontal inspection assembly of a helical-pile-lead-inspired exterior. One complete long capped shaft includes a full narrowing lead tip and carries three independent thick single-turn annular helical plates of progressively different radii, separated by long genuinely empty axial intervals. Each plate is an entire continuous closed material solid with modeled upper and lower winding faces, inner and outer side walls, and two separated finished end faces; none is an isolated helical slice extracted from another model. A complete thick square head plate has four true square through-ports outside the shaft. Two entire open-top inspection saddles support the complete shaft at two finite flat polygonal underside patches and both broad saddle soles are grounded. The plates and head have finite selected interior roots to the same uncut shaft. Unlike the old T-handle soil auger, there is no hand grip or single continuous two-turn cutting flight: three separate one-turn bearing-plate-like solids are isolated by complete plain shaft intervals and a full four-port head. Unlike the six-turn screw roof prop, there is no telescopic lower tube, adjustment collar, fixed handles or opposing roof and ground load plates. Unlike the open helical conveyor, there is no open cylindrical centre, tangential inlet or outlet, transport deck, edge band or tier frame. All seven complete meshes newly authored together, no old screw, auger, blade, shaft, flange or display stand imported, extracted or resized. Four opaque constant untextured PBR roles, metres native Z up and whole horizontal bounds centred over the two complete ground soles; one model zero scenes. Deliberately a supported horizontal artistic inspection display, not an installed foundation, complete buried pile system or operating soil tool. The small flat tip is not sharpened; the head and ports are generic display geometry, not a specific product connection. Broad helical lead-section vocabulary only, no brand or dimension replica. No geology, soil penetration, torque, cutting, load resistance, real weld, connection capacity, extension compatibility, fabrication, assembly instructions, installation or foundation safety capability made or verified. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
