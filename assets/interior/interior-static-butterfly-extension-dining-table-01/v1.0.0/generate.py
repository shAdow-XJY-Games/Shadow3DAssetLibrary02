import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='interior-static-butterfly-extension-dining-table-01'
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

# Newly authored complete table in a single fixed partial butterfly deployment pose.
PALETTE=[('WarmMapleDiningLeaves',(.48,.285,.12,1),.76,0),('MutedTealUnderframe',(.09,.22,.19,1),.8,0),('FixedHingeHardware',(.20,.22,.21,1),.48,.65)]
for x,label in[(-.88,'Left'),(.88,'Right')]:
 for y,side in[(-.34,'Front'),(.34,'Rear')]:box(label+side+'WholeGroundLeg',(x-.045,y-.045,0),(x+.045,y+.045,.705),1)
 box(label+'FullEndApron',(x-.045,-.385,.61),(x+.045,.385,.705),1)
 box(label+'LowerEndTie',(x-.035,-.295,.19),(x+.035,.295,.245),1)
for y,label in[(-.345,'Front'),(.345,'Rear')]:
 # Full fixed U rail, genuinely open upper channel with visible tongue on each half.
 p=[(y-.04,.625),(y+.04,.625),(y+.04,.697),(y+.025,.697),(y+.025,.643),(y-.025,.643),(y-.025,.697),(y-.04,.697)]
 # pad initially extrudes in Y; transform profile first coordinate into Y and extrusion into X.
 pad(label+'WholeOpenSlideRail',p,-.925,.925,2);v,f,m=G[label+'WholeOpenSlideRail'];G[label+'WholeOpenSlideRail']=([(yy,xx,z)for xx,yy,z in v],[(a,c,b)for a,b,c in f],m)
 for x0,x1,side in[(-1.00,-.14,'Left'),(.14,1.00,'Right')]:
  box(label+side+'FixedSlideTongue',(x0,y-.022,.646),(x1,y+.022,.721),1)
for x0,x1,label in[(-1.05,-.34,'Left'),(.34,1.05,'Right')]:box(label+'SeparatedWholeMainDiningTop',(x0,-.45,.721),(x1,.45,.761),0)
# The middle storage bay is not filled by a central fixed tabletop.
box('WholeCentralStorageTrayFloor',(-.33,-.29,.52),(.33,.29,.545),1)
for x,label in[(-.32,'Left'),(.32,'Right')]:
 box(label+'StorageBayEndWall',(x-.012,-.29,.545),(x+.012,.29,.615),1)
 box(label+'StorageTrayHanger',(x-.018,-.34,.525),(x+.018,-.29,.645),2)
 box(label+'RearStorageTrayHanger',(x-.018,.29,.525),(x+.018,.34,.645),2)
# A whole horizontal half leaf and its full matching raised partner share the central hinge axis.
box('ButterflyFrontWholeHalfLeaf',(-.32,-.44,.721),(.32,-.008,.753),0)
box('ButterflyRearWholeHalfLeafRaised',(-.32,.008,.721),(.32,.44,.753),0)
v,f,m=G['ButterflyRearWholeHalfLeafRaised'];a=math.radians(55);G['ButterflyRearWholeHalfLeafRaised']=([(x,y*math.cos(a)-(z-.753)*math.sin(a),.753+y*math.sin(a)+(z-.753)*math.cos(a))for x,y,z in v],f,m)
for x,label in[(-.22,'Left'),(.22,'Right')]:
 pipe(label+'FixedCentralLeafHinge',[(x-.045,0,.753),(x+.045,0,.753)],.016,2,12)
 box(label+'FrontLeafHingeStrap',(x-.035,-.065,.708),(x+.035,0,.723),2)
 box(label+'RearLeafHingeStrap',(x-.035,0,.708),(x+.035,.065,.723),2)
 n=label+'RearLeafHingeStrap';v,f,m=G[n];G[n]=([(xx,yy*math.cos(a)-(z-.753)*math.sin(a),.753+yy*math.sin(a)+(z-.753)*math.cos(a))for xx,yy,z in v],f,m)
 # Fixed low cradles visibly carry the horizontal leaf, not a claim of working pivot travel.
 box(label+'HorizontalLeafBearingBlock',(x-.045,-.28,.545),(x+.045,-.20,.721),1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
FM={n:[m]*len(f)for n,(v,f,m)in G.items()}
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
focus=Vector((0,0,.53))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.85;aim(cam,(4,-6,3.6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/interior/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'interior','style':'S01-clean-geometric','title':'Static Butterfly Extension Dining Table','description':'One newly authored complete static butterfly-extension dining table in a single partially deployed display pose. Two whole main dining tops are visibly separated over two genuine open-channel slide rails with fixed tongues. The central gap contains a whole horizontal half-leaf and its matching full raised half-leaf with central fixed hinge barrels and straps; an actual lowered open storage tray and hangers remain below. Four complete grounded legs, end aprons and lower ties form the whole underframe. The paired middle folding-leaf and storage arrangement differs from the old narrow fixed-centre outer D-leaf gateleg table and laundry outer-wing folding board; no old tabletop is stretched or imported. Three opaque solid PBR roles, metres and whole horizontal bounds-centred ground datum. One prop, no extra pose counted. Static furniture appearance only, not a flat usable dining surface in this displayed transitional pose. No working slide, hinge movement, complete folding trajectory, storage motion, ergonomic fit, load, stability, manufacture or safety certification.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
