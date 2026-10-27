import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='waterworks-fixed-inclined-plate-pack-and-three-hopper-cutaway-01'
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
PALETTE=[('WholeCutawayVesselMutedTeal',(.07,.25,.27,1),.69,.31),('WholeInclinedPlatesSatinSteel',(.49,.55,.55,1),.54,.54),('WholeHollowHoppersWarmGrey',(.44,.45,.40,1),.76,.18),('WholeDeliberateCutEndsAndFootPadsOchre',(.56,.32,.10,1),.71,.20)]
FM={}
# One continuous floor with three genuine openings and full retained side/back walls.
# The front wall is deliberately absent for this complete cutaway asset; ends are closed.
xs=[-1.65,-1.50,-1.40,-.60,-.50,-.40,.40,.50,.60,1.40,1.50,1.65];ys=[-1.10,-.92,-.82,.82,.92,1.10];zs=[1.45,1.57,2.95];cells=[]
for i in range(len(xs)-1):
 for j in range(len(ys)-1):
  x=(xs[i]+xs[i+1])/2;y=(ys[j]+ys[j+1])/2
  for k in range(2):
   floor=k==0 and not(any(abs(x-c)<.40 for c in[-1.,0.,1.])and abs(y)<.82)
   wall=abs(x)>1.50 or y>.92
   if floor or wall:cells.append([(x,y,z)for z in zs[k:k+2]for y in ys[j:j+2]for x in xs[i:i+2]])
cell_union('WholeFrontCutawayVesselAndThreeOpenings',cells,0)
v,f,m=G['WholeFrontCutawayVesselAndThreeOpenings'];FM['WholeFrontCutawayVesselAndThreeOpenings']=[3 if all(abs(v[i][1]+1.10)<1e-9 for i in face) else 0 for face in f]
# Each whole rectangular hopper has its own real upper cavity, taper and open lower neck.
def hopper(name,cx):
 prof=[(.20,.24,.30),(.20,.24,.52),(.48,.90,1.45),(.40,.82,1.45),(.12,.16,.52),(.12,.16,.30)];v=[];f=[]
 for hx,hy,z in prof:v.extend([(cx+x,y,z)for x,y in[(-hx,-hy),(hx,-hy),(hx,hy),(-hx,hy)]])
 for k in range(len(prof)):
  kk=(k+1)%len(prof)
  for i in range(4):j=(i+1)%4;a=k*4+i;b=k*4+j;c=kk*4+j;d=kk*4+i;f.extend([(a,b,c),(a,c,d)])
 record(name,v,f,2)
for i,c in enumerate([-1.,0.,1.]):hopper('WholeOpenTaperedHopper'+str(i),c)
# Full four-leg stand holds the complete three-hopper body above the ground.
for x in[-1.59,1.59]:
 for y in[-1.02,1.02]:
  key=str(x)+'_'+str(y);box('WholeStandLeg'+key,(x-.075,y-.075,.10),(x+.075,y+.075,1.58),0);box('WholeStandGroundPad'+key,(x-.19,y-.20,0),(x+.19,y+.20,.13),3)
# Two entire internal rails support every complete inclined plate bottom edge.
for y in[-.80,.80]:box('WholePlatePackSupportRail'+str(y),(-1.53,y-.065,1.67),(1.53,y+.065,1.77),0)
PLATE_X=[-1.35+.28*i for i in range(9)]
for i,x in enumerate(PLATE_X):pad('WholeInclinedPlainPlate%02d'%i,[(x-.02,1.73),(x+.02,1.73),(x+.52,2.82),(x+.48,2.82)],-.85,.85,1)
# One full open collection trough lies on the retained high rear wall; both axial ends open.
profile=[(.86,2.95),(1.18,2.95),(1.18,3.22),(1.12,3.22),(1.12,3.02),(.92,3.02),(.92,3.22),(.86,3.22)]
pad('WholeHighRearOpenCollectionTrough',profile,-1.50,1.50,0);v,f,m=G.pop('WholeHighRearOpenCollectionTrough');record('WholeHighRearOpenCollectionTrough',[(y,x,z)for x,y,z in v],f,m)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()};FM={n:FM.get(n,[m]*len(f))for n,(v,f,m)in G.items()}
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
focus=Vector((0,0,1.60))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=5.5;aim(cam,(4,-9,5) if view=='qa-front' else (-6,-8,7));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/waterworks/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'waterworks','style':'S01-clean-geometric','title':'Fixed Inclined Plate Pack and Three Hopper Cutaway','description':'One wholly newly authored complete dry inclined-plate-settler-inspired cutaway apparatus. One continuous thick rectangular floor contains three genuine rectangular through openings and joins full retained back and side walls; the front wall is deliberately omitted, with complete finite exposed ends marked in a warm material role, so this is honestly an open-front cutaway rather than a sealed tank. Three complete hollow rectangular hoppers taper from those floor openings into real open lower necks. Nine full plain finite-thickness plates stand at one inclined angle with genuine parallel air gaps on two complete internal support rails. One full elevated open rear collection trough and four whole rooted stand legs with separate finite ground pads complete the assembly. Unlike the circular basin with diameter bridge, central feedwell and low radial rakes, there is no circular bowl or suspended rotating-looking centre apparatus. Unlike the horizontal plate filter press, there are no through-bored recessed square filter faces, pressure head, plunger or compression rails; these are broad plain inclined plates over three lower hoppers inside a rectangular cutaway body. All numeric vessel boundaries, plates, hoppers, supports and trough authored together, no old vessel, press plate, rack or frame mesh imported or extracted. Four opaque constant PBR roles, metres Z up, whole horizontal bounds centred over four ground soles, one complete model zero scenes. Empty fixed illustrative waterworks cutaway only, with no fluid, sediment or biological contents. No filtering medium, separation, settling, treatment, water quality, flow distribution, hydraulic connectivity, collection efficiency, cleanability, maintenance access, pressure, structural load, manufacture, installation, operation or equipment safety capability made or verified. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
