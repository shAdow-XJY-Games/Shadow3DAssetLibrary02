import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='farming-fixed-pivot-frame-trussed-pipe-and-wheeled-tower-01'
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
PALETTE=[('WholePivotAndWheelTowerMutedGreen',(.18,.32,.22,1),.78,.12),('WholePipeAndSpanBracingPaleSteel',(.55,.61,.59,1),.57,.44),('WholeTyresAndDropOutletsDarkRubber',(.095,.115,.105,1),.86,.03)]
FM={}
def tube(name,points,ro,ri,mat,n=12):
 v=[];f=[];frames=[]
 for k,p in enumerate(points):
  t=unit(sub(points[min(k+1,len(points)-1)],points[max(k-1,0)]));u=(0,1,0);w=unit(cross(t,u));frames.append((u,w))
 for r in[ro,ri]:
  for p,(u,w)in zip(points,frames):
   for j in range(n):v.append(add(p,add(mul(u,r*math.cos(math.tau*j/n)),mul(w,r*math.sin(math.tau*j/n)))))
 off=len(points)*n
 for k in range(len(points)-1):
  for j in range(n):
   q=(j+1)%n;a=k*n+j;b=k*n+q;c=(k+1)*n+q;d=(k+1)*n+j;f.extend([(a,b,c),(a,c,d),(a+off,c+off,b+off),(a+off,d+off,c+off)])
 for j in range(n):
  q=(j+1)%n;f.extend([(j,j+off,q+off),(j,q+off,q)]);o=(len(points)-1)*n;f.extend([(o+j,o+q,o+q+off),(o+j,o+q+off,o+j+off)])
 record(name,v,f,mat)
# Grounded four-legged pivot support with a genuine hollow upright returning into the high lateral pipe.
for ix,x in enumerate([-.42,.42]):
 for iy,y in enumerate([-.43,.43]):
  box('WholePivotFoot'+str(ix)+str(iy),(x-.17,y-.17,0),(x+.17,y+.17,.09),0)
  pipe('WholePivotSlopingLeg'+str(ix)+str(iy),[(x,y,.06),(0,y*.26,2.12)],.065,0,8)
for y in[-.43,.43]:pipe('WholePivotLowerCrossTie'+str(y),[(-.42,y,.50),(.42,y,.50)],.04,0,8)
turned('WholeFixedPivotCollar',0,0,[(.10,2.00),(.16,2.00),(.16,2.18),(.10,2.18)],1,16)
tube('WholeHollowUprightAndUpperElbow',[(0,0,.22),(0,0,1.96),(.025,0,2.10),(.12,0,2.21),(.30,0,2.25)],.10,.065,1)
box('WholeBlankPivotSideControlCase',(-.40,-.53,.88),(-.11,-.34,1.25),0)
# One complete long upper pipe span and short outer overhang; not a lifting jib.
points=[(.28+6.32*k/32,0,2.25+.30*math.sin(math.pi*k/32))for k in range(33)]
points.extend([(6.70,0,2.20),(6.76,0,2.09)])
tube('WholeArchedPipeSpanAndDownturnedOuterEnd',points,.095,.060,1)
xs=[.30,1.44,2.58,3.72,4.86,6.0]
zpipe=lambda x:2.25+.30*math.sin(math.pi*(x-.28)/6.32)
zlow=[2.20,1.85,1.66,1.66,1.85,2.20]
for side,y in [('Near',-.25),('Far',.25)]:
 pipe(side+'WholeLowerSpanChord',[(x,y,z)for x,z in zip(xs,zlow)],.028,1,8)
 for k,x in enumerate(xs):pipe(side+'WholeSpanStrut'+str(k),[(x,0,zpipe(x)),(x,y,zlow[k])],.026,1,8)
 for k in range(5):
  pipe(side+'WholeDiagonalTie'+str(k),[(xs[k],y,zlow[k]),(xs[k+1],0,zpipe(xs[k+1]))],.022,1,8)
# One terminal tower, with two complete tandem wheels rolling tangent to a hypothetical circle (no motion claimed).
for j,y in enumerate([-.74,.74]):
 wheel('WholeTowerTyre'+str(j),6,y,.36,.36,.17,.22,2)
 wheel('WholeTowerHub'+str(j),6,y,.36,.17,0,.24,0)
 pipe('WholeTowerWheelAxle'+str(j),[(5.80,y,.36),(6.20,y,.36)],.065,1,12)
 for side,x in [('Left',5.88),('Right',6.12)]:pipe(side+'WholeTowerDiagonalLeg'+str(j),[(x,y,.36),(6,0,2.22)],.055,0,8)
pipe('WholeTowerLowTandemTie',[(6,-.74,.53),(6,.74,.53)],.055,0,8)
box('WholeTowerUpperPipeSeat',(5.84,-.15,2.17),(6.16,.15,2.32),0)
# Separate complete hanging drop tubes terminate in real open annular outlet heads. Internal network intersections not asserted.
for k,x in enumerate([1.05,2.25,3.45,4.65,5.65]):
 z=zpipe(x);bottom=1.08
 tube('WholeVerticalDropTube'+str(k),[(x,0,z-.025),(x,0,bottom+.045)],.029,.015,2)
 turned('WholeOpenDropOutlet'+str(k),x,0,[(.014,bottom+.065),(.045,bottom+.065),(.060,bottom),(.014,bottom)],2,12)
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
focus=Vector((0,0,1.20))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=8.6;aim(cam,(5,-12,5.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/farming/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'farming','style':'S01-clean-geometric','title':'Fixed Pivot Frame Trussed Pipe and Wheeled Tower','description':'One complete newly authored static centre-pivot-irrigation-inspired apparatus. A fixed four-leg ground frame surrounds a thick hollow upright pipe and curved upper elbow. One whole gently arched long pipe span is supported by two lower chords and diagonal spatial ties, reaching a separate complete two-wheel tandem tower; the far pipe continues as a short downturned overhang. Five complete hanging drop tubes have real annular open outlet heads. The long span is a supported pipe assembly between a ground pivot and a wheeled outer tower, not an old garden sprinkler with longer arms, nor a crane jib stripped of its hook or placed on wheels. No old visible mesh imported. Three opaque PBR roles, metres Z up, full horizontal envelope centred over four pivot feet and the displayed tyre ground facets, one whole prop zero scenes. Fixed stylized empty exterior only; no water, hoses, fields or crops supplied. Internal intersections of the separate hollow parts are not a verified fluid network. No irrigation distribution, pressure, rotary joint, wheel travel, propulsion, motors, structural truss capacity, plumbing fit, installation or operating safety capability. Rig animation and interaction not made or verified.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
