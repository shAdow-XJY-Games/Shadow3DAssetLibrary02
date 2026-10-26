import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='regional-fixed-three-aisle-and-apsidal-hall-section-01'
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
PALETTE=[('WholeMasonry_WarmStone',(.57,.50,.38,1),.9,0),('WholeRoof_DullClay',(.38,.18,.11,1),.91,0),('WholeFloor_QuietSlate',(.32,.34,.30,1),.93,0)]
FM={}
def xy_prism(name,poly,z0,z1,mat):
 pad(name,poly,z0,z1,mat)
 v,f,m=G[name];record(name,[(x,z,y)for x,y,z in v],[(a,c,b)for a,b,c in f],m)
def yz_prism(name,poly,x0,x1,mat):
 pad(name,poly,x0,x1,mat)
 v,f,m=G[name];record(name,[(y,x,z)for x,y,z in v],[(a,c,b)for a,b,c in f],m)
# Continuous footprint includes central semicircular rear chamber, no overlapping floor caps.
outline=[(-2.35,-2.65),(2.35,-2.65),(2.35,2.58),(1.18,2.58)]
outline += [(1.18*math.cos(t),2.58+1.18*math.sin(t))for t in [math.pi*i/20 for i in range(1,21)]]
outline += [(-2.35,2.58)]
xy_prism('WholeHallAndApseFloor',outline,0,.12,2)
# Two full longitudinal arcade assemblies, each with three true ground-to-arch openings.
for side in[-1,1]:
 x0,x1=sorted([side*.90,side*1.10])
 for k,(a,b)in enumerate([(-2.5,-2.25),(-.95,-.65),(.65,.95),(2.25,2.5)]):
  box('WholeArcadePier_'+str(side)+'_'+str(k),(x0,a,.10),(x1,b,3.24),0)
 for k,c in enumerate([-1.6,0,1.6]):
  lower=[(c-.65*math.cos(t),1.5+.65*math.sin(t))for t in[math.pi*i/16 for i in range(17)]]
  yz_prism('WholeHighArcadeSpandrel_'+str(side)+'_'+str(k),lower+[(c+.65,3.24),(c-.65,3.24)],x0,x1,0)
# Whole far exterior wall; foreground wall is intentionally sectioned low for interior reading.
box('WholeFarAisleOuterWall',(-2.25,-2.5,.10),(-2.06,2.5,1.84),0)
box('WholeNearAisleRetainedLowSection',(2.06,-2.5,.10),(2.25,.1,.48),0)
box('WholeNearAisleRetainedRearWall',(2.06,.1,.10),(2.25,2.5,1.84),0)
# Two independent rear side-aisle closures leave central apse mouth unobstructed.
box('WholeFarAisleRearEnd',(-2.06,2.31,.10),(-1.1,2.5,1.84),0)
box('WholeNearAisleRearEnd',(1.1,2.31,.10),(2.06,2.5,1.84),0)
# Roof sections: complete far lean-to, retained rear half near lean-to and high central gable.
pad('WholeFarLowAisleRoof',[(-2.30,1.80),(-.99,2.45),(-.99,2.59),(-2.30,1.94)],-2.55,2.55,1)
pad('WholeNearLowAisleRoofSection',[(.99,2.45),(2.30,1.80),(2.30,1.94),(.99,2.59)],.10,2.55,1)
pad('WholeHighNaveRoofSection',[(-1.16,3.18),(0,3.92),(1.16,3.18),(1.16,3.33),(0,4.07),(-1.16,3.33)],0,2.55,1)
# Rear high transom closes the space above the apsidal arch beneath the gable.
rear_arch=[(-.90*math.cos(t),2.25+.90*math.sin(t))for t in[math.pi*i/20 for i in range(21)]]
pad('WholeRearArchedGableTransom',rear_arch+[(.90,3.48),(0,4.00),(-.90,3.48)],2.30,2.50,0)
# Continuous thick half-cylindrical apse wall, genuinely open towards nave.
cells=[]
for i in range(20):
 a=math.pi*i/20;b=math.pi*(i+1)/20
 cells.append([(r*math.cos(t),2.5+r*math.sin(t),z)for z in[.10,2.25]for t in[a,b]for r in[.90,1.10]])
cell_union('WholeSemicircularRearChamberWall',cells,0)
# One closed thick spherical half-dome over the rear chamber, finite front cut face.
v=[];f=[];lookup={}
def vi(p):
 p=tuple(round(x,9)for x in p)
 if p not in lookup:lookup[p]=len(v);v.append(p)
 return lookup[p]
def tri(a,b,c):
 ids=[vi(p)for p in[a,b,c]]
 if len(set(ids))==3:f.append(tuple(ids))
def quad(a,b,c,d):tri(a,b,c);tri(a,c,d)
def dome(r,t,u):return(r*math.cos(u)*math.cos(t),2.5+r*math.cos(u)*math.sin(t),2.25+r*math.sin(u))
for i in range(20):
 a=math.pi*i/20;b=math.pi*(i+1)/20
 for j in range(8):
  c=math.pi*j/16;d=math.pi*(j+1)/16
  quad(dome(1.10,a,c),dome(1.10,b,c),dome(1.10,b,d),dome(1.10,a,d))
  quad(dome(.90,a,d),dome(.90,b,d),dome(.90,b,c),dome(.90,a,c))
 quad(dome(.90,a,0),dome(.90,b,0),dome(1.10,b,0),dome(1.10,a,0))
for t in[0,math.pi]:
 for j in range(8):
  c=math.pi*j/16;d=math.pi*(j+1)/16
  pts=[dome(.90,t,c),dome(1.10,t,c),dome(1.10,t,d),dome(.90,t,d)]
  if t==math.pi:pts.reverse()
  quad(*pts)
record('WholeRearHalfDomeAndFiniteMouthSection',v,f,1)
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
focus=Vector((0,0,1.70))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=8.6;aim(cam,(7,-10,7) if view=='qa-front' else (8,9,7));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/regional/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'modular','theme':'regional','style':'S01-clean-geometric','title':'Fixed Three Aisle And Apsidal Hall Section','description':'One newly authored complete static architectural section of a high central longitudinal hall, two lower side aisles and a semicircular rear chamber. Two complete parallel high arcade assemblies have three genuine ground-to-arch openings each, connecting the central floor to lower lateral passages. Whole side walls and inclined aisle roofs sit below the retained high central gabled roof. A single continuous floor expands into the rear semicircular chamber, whose thick half-cylinder wall and closed thick half-dome terminate only the central hall, not all three aisles. The front half of the high roof and the front-right low roof/wall are deliberately omitted as finite presentation sections to expose the interior hierarchy; all retained pieces have closed finite edges. Unlike the earlier monitor roof alone, this includes grounded rooms, arcades, lower aisles and an apsidal termination; unlike a square groin bay it is a longitudinal three-volume organization rather than crossed cylindrical roofs. All coordinates newly authored, no old columns, roof or church parts imported. Three opaque solid PBR appearances, metres Z-up and bounds-centred ground datum, one static architecture model zero scenes. A generic artistic sectional building, not a historically exact basilica or a religious-use proposal. No people, rituals, furnishing, hidden finished front facade, complete weather enclosure, occupancy, daylight, acoustics, load, construction, historical accuracy, building-code or safety capability. No rigging animation interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
