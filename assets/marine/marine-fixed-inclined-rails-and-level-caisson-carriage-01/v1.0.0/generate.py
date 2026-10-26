import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='marine-fixed-inclined-rails-and-level-caisson-carriage-01'
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
PALETTE=[('WholeInclineRailsAndFrameMutedBlue',(.15,.28,.31,1),.67,.30),('WholeLevelCaissonWarmPaleGrey',(.59,.59,.52,1),.86,.08),('WholeWheelsGatesAndHaulDarkSteel',(.18,.20,.18,1),.60,.45)]
FM={}
slope=.40
rz=lambda x:.34+slope*(x+4.2)
# A single rising twin-track infrastructure with its own complete ground supports.
for side,y in [('Near',-1.02),('Far',1.02)]:
 pad(side+'WholeInclinedRail',[(-4.25,rz(-4.25)-.08),(4.25,rz(4.25)-.08),(4.25,rz(4.25)+.08),(-4.25,rz(-4.25)+.08)],y-.085,y+.085,0)
 for k,x in enumerate([-4.0,-2,0,2,4.0]):
  box(side+'WholeRailSupport'+str(k),(x-.12,y-.15,.10),(x+.12,y+.15,rz(x)-.03),1)
  box(side+'WholeGroundFoot'+str(k),(x-.32,y-.30,0),(x+.32,y+.30,.14),1)
for k,x in enumerate([-4,-2,0,2,4]):
 pipe('WholeUnderRailCrossTie'+str(k),[(x,-1.07,rz(x)-.12),(x,1.07,rz(x)-.12)],.065,0,8)
# Four independent complete rolling discs remain in one fixed pose. Axles are transverse Y.
wheelz=lambda x:rz(x)+.08+.23*math.sqrt(1+slope*slope)
for k,x in enumerate([-1.78,1.78]):
 z=wheelz(x)
 pipe('WholeCarriageTransverseAxle'+str(k),[(x,-1.20,z),(x,1.20,z)],.065,2,12)
 for side,y in [('Near',-1.02),('Far',1.02)]:
  name=side+'WholeRailWheel'+str(k);wheel(name,0,0,0,.23,0,.15,2);v,f,m=G.pop(name);record(name,[(x+yy,y+xx,z+zz)for xx,yy,zz in v],f,m)
# Whole open wedge underframes hold the long vessel floor horizontal above the sloping wheel centres.
for side,y in [('Near',-.93),('Far',.93)]:
 pad(side+'WholeInclinedCarriageSill',[(-2.10,wheelz(-2.10)-.035),(2.10,wheelz(2.10)-.035),(2.10,wheelz(2.10)+.13),(-2.10,wheelz(-2.10)+.13)],y-.07,y+.07,0)
 box(side+'WholeHorizontalVesselBearer',(-2.48,y-.10,3.40),(2.48,y+.10,3.56),0)
 for k,x in enumerate([-1.78,1.78]):
  box(side+'WholeVaryingHeightCarriagePost'+str(k),(x-.08,y-.085,wheelz(x)-.03),(x+.08,y+.085,3.49),0)
 pipe(side+'WholeUnderbodyDiagonal',[(-1.78,y,wheelz(-1.78)+.06),(1.78,y,3.48)],.052,0,8)
# One whole horizontal U-section caisson floor plus thin side walls; empty and dry, not a reused floating dock.
profile=[(-1.22,3.48),(1.22,3.48),(1.22,4.32),(1.06,4.32),(1.06,3.65),(-1.06,3.65),(-1.06,4.32),(-1.22,4.32)]
pad('WholeLevelCaissonFloorAndSideWalls',profile,-2.55,2.55,1);v,f,m=G.pop('WholeLevelCaissonFloorAndSideWalls');record('WholeLevelCaissonFloorAndSideWalls',[(y,x,z)for x,y,z in v],f,m)
# Both full end gate leaves and their distinct open-head portals are part of the empty caisson.
for side,x in [('LowEnd',-2.48),('HighEnd',2.48)]:
 box(side+'WholeEndGateLeaf',(x-.065-(.08 if x>0 else-.08),-1.075,3.60),(x+.065-(.08 if x>0 else-.08),1.075,4.25),2)
 for k,y in enumerate([-1.15,1.15]):box(side+'WholeGateGuidePost'+str(k),(x-.13,y-.11,3.46),(x+.13,y+.11,4.70),0)
 box(side+'WholeGatePortalCrosshead',(x-.12,-1.25,4.57),(x+.12,1.25,4.72),0)
 pipe(side+'WholeGateUprightStem',[(x-(.08 if x>0 else-.08),0,4.18),(x-(.08 if x>0 else-.08),0,4.63)],.035,2,10)
# Upper anchored haul station, two real strands and the whole transverse drum, all fixed.
box('WholeUpperHaulFoundation',(4.04,-1.30,0),(4.74,1.30,3.64),1)
for k,y in enumerate([-.92,.92]):box('WholeHaulBearingSeat'+str(k),(4.18,y-.13,3.60),(4.61,y+.13,4.03),0)
pipe('WholeHaulCrossShaft',[(4.39,-1.13,3.92),(4.39,1.13,3.92)],.07,2,12)
# Drum axis Y, broad middle with two integral raised flanges.
turned('WholeHaulDrum',0,0,[(0,-.77),(.30,-.77),(.30,-.66),(.23,-.66),(.23,.66),(.30,.66),(.30,.77),(0,.77)],2,24)
v,f,m=G.pop('WholeHaulDrum');record('WholeHaulDrum',[(4.39+x,z,3.92+y)for x,y,z in v],f,m)
for k,y in enumerate([-.55,.55]):pipe('WholeFixedHaulStrand'+str(k),[(2.43,y,3.48),(4.25,y,3.74)],.017,2,8)
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
focus=Vector((0,0,2.35))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=10.5;aim(cam,(-10,-14,10.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/marine/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'marine','style':'S01-clean-geometric','title':'Fixed Inclined Rails and Level Caisson Carriage','description':'One complete newly authored fixed inclined-caisson boat-lift-style exterior. A full horizontal thick U-section vessel has a dry blind floor, thin high side walls and two entire closed end gates in separate open-head guide portals. Beneath it, two complete open wedge carriage frames connect the level vessel bearers to two transverse axles and four rail wheels at different heights on a single continuous inclined twin track. The rails have their own grounded supports and ties. A separate high-end anchored haul station carries a complete flanged drum, cross-shaft and two full fixed strands into the carriage end. The long level gated chamber over unequal-height open carriage frames, long rising guide infrastructure and end haul station are authored together; no old boat, dock, ramp, hopper or carriage mesh is reused. Unlike the floating dock the chamber is lifted on rail wheels rather than resting on broad hull wings, and unlike the mixing skip there is no hopper mouth feeding a stationary processing pan. Three opaque untextured PBR roles, metres Z up and full horizontal bounds centred, one prop zero scenes. Static dry artistic exterior only, no ship, water or host canals. No actual travel, gate opening, level control, cable reeving or winding, wheel contact tolerances, watertightness, lift capacity, buoyancy, docking, rail compatibility, structural load, manufacture, operation or engineering safety. Rigging animation and interaction not made or verified.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
