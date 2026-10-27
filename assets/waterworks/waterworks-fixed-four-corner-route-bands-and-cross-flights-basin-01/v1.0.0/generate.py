import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='waterworks-fixed-four-corner-route-bands-and-cross-flights-basin-01'
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
PALETTE=[('WholeBasinWarmConcrete',(.48,.47,.41,1),.92,.0),('WholeFourCornerBandsAndWheelsDarkSteel',(.10,.16,.17,1),.65,.47),('WholeCrossFlightsMutedOchre',(.57,.34,.12,1),.72,.25),('WholeAxlesPedestalsAndDriveGreyGreen',(.23,.34,.32,1),.70,.31)]
FM={};JOINS=[];ROOTS=['WholeContinuousRectangularDryBasin']
xs=[-3.0,-2.80,2.80,3.0];ys=[-1.60,-1.40,1.40,1.60];zs=[0,.16,1.45];cells=[]
for i in range(3):
 for j in range(3):
  for k in range(2):
   if k==1 and i==j==1:continue
   cells.append([(x,y,z)for z in[zs[k],zs[k+1]]for y in[ys[j],ys[j+1]]for x in[xs[i],xs[i+1]]])
cell_union(ROOTS[0],cells,0)
def wheel_y(name,x,y,z,r,w,m):
 wheel(name,y,x,z,r,0,w,m);v,f,mi=G.pop(name);record(name,[(y,x,z)for x,y,z in v],f,mi)
centres=[(2.25,1.90),(-2.25,1.90),(-2.25,.65),(2.25,.65)]
for j,(x,z)in enumerate(centres):
 axle='WholeTransverseCornerAxle'+str(j);pipe(axle,[(x,-1.55,z),(x,1.55,z)],.055,3,12)
 if z<1:
  for y in[-1.49,1.49]:JOINS.append((axle,ROOTS[0],(x,y,z)))
 else:
  for side,y in enumerate([-1.49,1.49]):
   ped='WholeUpperAxlePedestal'+str(j)+'_'+str(side);box(ped,(x-.16,y-.10,1.40),(x+.16,y+.10,2.0),3);JOINS.append((ped,ROOTS[0],(x,y,1.425)));JOINS.append((axle,ped,(x,y,z)))
 for side,y in enumerate([-1.10,1.10]):
  name='WholeCornerRouteWheel'+str(j)+'_'+str(side);wheel_y(name,x,y,z,.225,.17,1);JOINS.append((name,axle,(x,y,z)))
def roundedrect(r):
 return[(x+r*math.cos(math.pi/2*k+math.pi/2*i/8),z+r*math.sin(math.pi/2*k+math.pi/2*i/8))for k,(x,z)in enumerate(centres)for i in range(9)]
def route_band(name,y):
 inner=roundedrect(.207);outer=roundedrect(.253);v=[(x,yy,z)for yy in[y-.045,y+.045]for loop in[inner,outer]for x,z in loop];f=[];n=len(inner)
 def quad(a,b,c,d):f.extend([(a,b,c),(a,c,d)])
 for j in range(n):
  k=(j+1)%n
  quad(j,k,n+k,n+j);quad(2*n+j,3*n+j,3*n+k,2*n+k)
  quad(j,2*n+j,2*n+k,k);quad(n+j,n+k,3*n+k,3*n+j)
 record(name,v,f,1)
for side,y in enumerate([-1.10,1.10]):
 name='WholeContinuousFourCornerRouteBand'+str(side);route_band(name,y)
 for j,(x,z)in enumerate(centres):
  dx,dz=[(0,.216),(0,.216),(0,-.216),(0,-.216)][j];JOINS.append((name,'WholeCornerRouteWheel'+str(j)+'_'+str(side),(x+dx,y,z+dz)))
for label,z in[('UpperReturn',2.130),('LowerRun',.420)]:
 for j,x in enumerate([-1.60,0,1.60]):
  name='WholeBroadCrossFlight'+label+str(j);box(name,(x-.055,-1.20,z-.105),(x+.055,1.20,z+.105),2)
  for side,y in enumerate([-1.10,1.10]):JOINS.append((name,'WholeContinuousFourCornerRouteBand'+str(side),(x,y,z)))
# One closed outboard casing, directly carried by the complete upper rear pedestal.
box('WholeBlankOutboardDriveCase',(2.03,1.50,1.64),(2.47,1.95,2.10),3);JOINS.append(('WholeBlankOutboardDriveCase','WholeUpperAxlePedestal0_1',(2.25,1.55,1.85)))
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
focus=Vector((0,0,1.05))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=8.4;aim(cam,(8,-11,13) if view=='qa-front' else (-8,-12,17));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/waterworks/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'waterworks','style':'S01-clean-geometric','title':'Fixed Four Corner Route Bands and Cross Flights Basin','description':'One wholly newly authored complete dry rectangular chain-and-flight-basin-inspired apparatus. A single continuous thick shell joins a full flat floor and four complete tall sidewalls around a genuinely open top. Two complete closed rounded-rectangular route bands run through four distinct upper/lower corner stations, with eight whole wheels on four full transverse axles. The lower axles root into the full basin sidewalls; four complete upper pedestals lift the upper return above the rim. Six entire broad transverse flights span both route bands in two separated horizontal rows, while a single closed outboard drive-case exterior belongs to one upper pedestal. No articulated chain links are modeled: the paired dark bands are continuous fixed route illustrations. Unlike the older circular basin with diameter bridge, central feedwell, vertical shaft and radial rake, the whole path is rectangular with distributed sidewall axle supports and full transverse flights. Unlike the forewell dredger with a two-drum oblique capsule route and empty scoops on an inclined ladder, this has four corner levels around a horizontal dry basin, no buckets, inclined ladder, hull, cabin or vessel. All numeric shell, routes, wheels, supports and whole flights authored anew together; no old basin, scoop, conveyor, bucket-lift or machine mesh imported or extracted. Four opaque constant untextured PBR materials, metres Z up, complete horizontal envelope centred over the finite basin ground sole, one whole model zero scenes. Empty static illustrative exterior only; bottom flights remain above the floor, and fixed wheel/band overlaps are not meshing or fit specifications. No water, sediment, wastewater, biology, material transport, scraping, treatment, continuous motion, chain articulation, sprocket engagement, drive mechanism, torque, throughput, hydraulic circuit, load, access, fabrication, maintenance, structural or machinery safety capability made or verified. No animation, rigging or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
