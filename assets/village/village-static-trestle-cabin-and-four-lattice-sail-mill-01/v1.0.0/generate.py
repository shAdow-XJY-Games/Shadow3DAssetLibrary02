import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='village-static-trestle-cabin-and-four-lattice-sail-mill-01'
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
PALETTE=[('WholeMillWarmTimber',(.43,.24,.105,1),.88,0),('WholeMillDarkCapAndFrame',(.16,.20,.18,1),.84,0),('WholeSailPaleLattice',(.72,.66,.48,1),.88,0)]
FM={}
def bar(name,a,b,width,depth,mat):
 t=unit(sub(b,a));u=unit(cross(t,(0,0,1)if abs(t[2])<.95 else(0,1,0)));w=cross(t,u);v=[]
 for p in[a,b]:
  for j,k in[(-1,-1),(1,-1),(1,1),(-1,1)]:v.append(add(p,add(mul(u,j*width/2),mul(w,k*depth/2))))
 f=[]
 for a,b,c,d in[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:f.extend([(a,b,c),(a,c,d)])
 record(name,v,f,mat)
def cub(lo,hi):return[(x,y,z)for z in[lo[2],hi[2]]for y in[lo[1],hi[1]]for x in[lo[0],hi[0]]]
box('WholeCrossGroundShoeX',(-.95,-.13,0),(.95,.13,.16),1)
box('WholeCrossGroundShoeY',(-.12,-.87,.018),(.12,.87,.18),1)
box('WholeCentralFixedMainPost',(-.17,-.17,.10),(.17,.17,1.57),0)
for i,(x,y)in enumerate([(-.79,0),(.79,0),(0,-.73),(0,.73)]):bar('WholeTrestleBrace'+str(i),(x,y,.13),(x*.11,y*.11,1.27),.12,.12,0)
box('WholeRaisedCabinFloor',(-.74,-.57,1.32),(.74,.57,1.46),1)
# Complete thick front/back/side walls with real open windows and rear doorway.
for side in['Front','Rear']:
 cells=[];xs=[-.70,-.23,.23,.70];zs=[1.43,1.91,2.26,2.74];lo,hi=(-.52,-.42)if side=='Front'else(.42,.52)
 for i in range(3):
  for j in range(3):
   if i==1 and ((side=='Front'and j==1)or(side=='Rear'and j<2)):continue
   cells.append(cub((xs[i],lo,zs[j]),(xs[i+1],hi,zs[j+1])))
 cell_union('Whole'+side+'CabinWall',cells,0)
for sg,label in[(-1,'Left'),(1,'Right')]:
 cells=[];ys=[-.48,-.19,.19,.48];zs=[1.43,1.91,2.26,2.74];xs=sorted([sg*.585,sg*.685])
 for i in range(3):
  for j in range(3):
   if i==1 and j==1:continue
   cells.append(cub((xs[0],ys[i],zs[j]),(xs[1],ys[i+1],zs[j+1])))
 cell_union('Whole'+label+'WindowedCabinWall',cells,0)
pad('WholeThickGabledMillCap',[(-.81,2.69),(.81,2.69),(.81,2.81),(0,3.23),(-.81,2.81)],-.62,.62,1)
# Full horizontal fixed windshaft rooted into the complete enclosed mill cabin.
pipe('WholeFixedWindshaft',[(0,.22,2.39),(0,-1.035,2.39)],.095,1,16)
turned('WholeSailHubUntransformed',0,0,[(0,-1.09),(.18,-1.09),(.18,-.93),(0,-.93)],0,16)
v,f,m=G.pop('WholeSailHubUntransformed');record('WholeFrontSailHub',[(x,z,2.39+y)for x,y,z in v],[(a,c,b)for a,b,c in f],m)
# Each whole sail has two long side rails and seven real cross rungs: all grid apertures remain empty.
for k in range(4):
 t=math.pi/8+k*math.pi/2;u=(math.sin(t),0,math.cos(t));w=(math.cos(t),0,-math.sin(t));center=(0,-1.01,2.39)
 def at(r,q,dy=0):return add(center,add(mul(u,r),add(mul(w,q),(0,dy,0))))
 bar('WholeSailMainSpine'+str(k),at(.04,0),at(1.88,0),.065,.075,0)
 bar('WholeSailOuterRail'+str(k),at(.49,.37),at(1.88,.37),.045,.055,2)
 for j in range(7):
  r=.50+1.37*j/6;bar('WholeSailCrossRung'+str(k)+'_'+str(j),at(r,-.025,-.009),at(r,.39,-.009),.044,.045,2)
# Rear empty entry platform with full short fixed steps and one long tail beam.
box('WholeRearEntryLanding',(-.32,.49,1.31),(.32,.94,1.43),1)
for i in range(6):
 y=.87+.16*i;z=1.25-.20*i
 box('WholeRearEntryTread'+str(i),(-.29,y,z-.055),(.29,y+.21,z+.055),0)
for sg in[-1,1]:bar('WholeRearStairStringer'+str(sg),(sg*.245,.90,1.33),(sg*.245,1.83,.055),.075,.085,1)
bar('WholeLongFixedRearTailBeam',(.39,.32,1.52),(.59,2.20,.14),.105,.115,0)
box('WholeTailGroundFoot',(.44,2.10,0),(.73,2.34,.18),1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
for n,(v,f,m)in G.items():FM.setdefault(n,[m]*len(f))
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
focus=Vector((0,0,2.03))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=5.45;aim(cam,(6,-10,5.4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/village/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'prop','theme':'village','style':'S01-clean-geometric','title':'Static Trestle Cabin and Four Lattice Sail Mill','description':'One wholly newly authored complete fixed timber sail-mill exterior. Two crossed ground shoes and four diagonal braces surround a thick central fixed post supporting a whole raised wooden cabin, real open wall windows and rear entry, full floor and thick gabled cap. A full horizontal windshaft projects from the cabin into a distinct front hub with four long complete lattice sails, each with real empty rung apertures. Behind are one full small entry platform, six fixed treads with complete side stringers and a separate long tail beam ending on a ground foot. Unlike the old small tubular wind-turbine mast with three solid propeller blades or a tapered lighthouse with a lantern gallery, this is a raised post-and-trestle millhouse with an open-grid sail assembly and rear access/tail relation. Every numeric body, aperture and sail frame newly drawn; no old lighthouse, rotor, cabin or stairs mesh imported. Three opaque constant PBR materials, metres Z-up and full horizontal bounds-centred ground origin. One complete static building prop zero scenes. Stylized post-mill-inspired exterior only, no internal milling machinery, exact historic reconstruction, wind capture, rotation, grinding, transmission, human access, structural load, construction or equipment safety capability. Rigging animation interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
