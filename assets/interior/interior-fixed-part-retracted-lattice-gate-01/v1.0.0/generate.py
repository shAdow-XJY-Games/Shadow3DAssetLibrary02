import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='interior-fixed-part-retracted-lattice-gate-01'
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

# One full fixed partially retracted lattice gate, not working security equipment.
PALETTE=[('FrameAndTrackIvory',(.59,.62,.60,1),.75,.16),('CrossLinkLatticeMutedTeal',(.16,.29,.28,1),.61,.38),('RollersPinsAndLatchDarkAlloy',(.13,.16,.17,1),.51,.52)]
box('WholeLeftFramePost',(-1.13,-.10,0),(-1.03,.10,1.93),0)
box('WholeRightReceivingPost',(.98,-.10,0),(1.08,.10,1.93),0)
# Whole top C-channel: bottom stem slot, actual finite cavity contains upper carriers.
pad('WholeUpperOpenTrack',[(-.10,1.93),(-.02,1.93),(-.02,1.958),(-.07,1.958),(-.07,2.055),(.07,2.055),(.07,1.958),(.02,1.958),(.02,1.93),(.10,1.93),(.10,2.08),(-.10,2.08)],-1.13,1.08,0)
v,f,m=G['WholeUpperOpenTrack'];record('WholeUpperOpenTrack',[(y,x,z)for x,y,z in v],f,m)
box('WholeGroundGuide',(-1.10,-.025,0),(1.05,.025,.055),0)
# Slender whole stave bodies with vertically elongated slots for fixed endpoints.
def slot_stave(name,x):
 # paired complete flat strips joined by top/bottom bridges, real full central aperture.
 poly=[(x-.026,.12),(x+.026,.12),(x+.026,1.88),(x-.026,1.88)]
 # Each stile made as one annular rectangular boundary, no painted slot.
 outer=[(x-.026,.12),(x+.026,.12),(x+.026,1.88),(x-.026,1.88)];inner=[(x-.009,.21),(x+.009,.21),(x+.009,1.79),(x-.009,1.79)];v=[(xx,y,z)for y in[-.012,.012]for loop in[outer,inner]for xx,z in loop];f=[]
 for i in range(4):j=(i+1)%4;f.extend([(i,j,j+4),(i,j+4,i+4),(i+8,j+12,j+8),(i+8,i+12,j+12),(i,i+8,j+8),(i,j+8,j),(i+4,j+12,i+12),(i+4,j+4,j+12)])
 record(name,v,f,1)
xs=[-1.00,-.70,-.40,-.10,.20]
for i,x in enumerate(xs):
 slot_stave('WholeOpenSlotStave_'+str(i),x)
 pipe('WholeUpperCarrierStem_'+str(i),[(x,0,1.86),(x,0,1.99)],.014,2,12)
 
 for side in[-1,1]:
  name='WholeUpperTrackRoller_'+str((i,side));wheel(name,0,0,0,.034,.014,.026,2);v,f,m=G[name];record(name,[(x+yy,side*.043+xx,1.992+z)for xx,yy,z in v],f,m)
 pipe('WholeUpperRollerAxle_'+str(i),[(x,-.065,1.992),(x,.065,1.992)],.014,2,12)
 box('WholeLowerGuideShoe_'+str(i),(x-.035,-.04,.035),(x+.035,.04,.14),2)
 for j,z in enumerate([.25,.75,1.25,1.75]):pipe('WholeStaveEndpointPin_'+str((i,j)),[(x,-.058,z),(x,.058,z)],.017,2,10)
# Distinct front/back crossing layers with finite pins at every crossover.
def strip(name,a,b,y):
 dx=b[0]-a[0];dz=b[1]-a[1];le=math.hypot(dx,dz);ux,uz=dx/le,dz/le;nx,nz=-uz*.015,ux*.015
 # ends stop at pin centres; adjacent bays do not share coplanar broad faces.
 poly=[(a[0]+nx,a[1]+nz),(a[0]-nx,a[1]-nz),(b[0]-nx,b[1]-nz),(b[0]+nx,b[1]+nz)];pad(name,poly,y-.008,y+.008,1)
for i in range(4):
 for j in range(3):
  x0,x1=xs[i],xs[i+1];z0,z1=.25+j*.5,.75+j*.5
  strip('WholeRisingCrossLink_'+str((i,j)),(x0,z0),(x1,z1),-.031)
  strip('WholeFallingCrossLink_'+str((i,j)),(x0,z1),(x1,z0),.031)
  pipe('WholeCrossJointPin_'+str((i,j)),[((x0+x1)/2,-.055,(z0+z1)/2),((x0+x1)/2,.055,(z0+z1)/2)],.021,2,10)
box('WholeMovingLeadingStile',(.19,-.065,.10),(.28,.065,1.91),0)
pipe('WholeLeadingPullLoop',[(.245,-.065,.87),(.245,-.15,.87),(.245,-.15,1.15),(.245,-.065,1.15)],.014,2,12)
box('WholeLeadingLatchTongue',(.275,-.025,.97),(.34,.025,1.05),2)
# Receiver has a true open recess, even though the gate is shown away from it.
pad('WholeReceivingOpenStrike',[(.91,.93),(.985,.93),(.985,1.09),(.91,1.09),(.91,1.065),(.96,1.065),(.96,.955),(.91,.955)],-.055,.055,2)
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
focus=Vector((0,0,1.04))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.15;aim(cam,(3,-8,3.1));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/interior/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'interior','style':'S01-clean-geometric','title':'Fixed Part Retracted Lattice Gate','description':'One newly authored complete static partly retracted lattice entrance gate. Full opposed upright frame posts carry one continuous slotted overhead box track and a grounded lower guide. Five complete slotted vertical staves with independent upper rollers, carrier stems and lower shoes guide a connected three-height four-bay network of separate front/back diagonal links and real fixed crossover/end pins. One whole leading stile has a projecting pull loop and latch tongue; a separate receiver has a real strike recess across the remaining clear doorway. This is not a solid-panel folding screen, a scissor lifting platform turned upright or a repeated freestanding barrier. All geometry newly authored, three opaque constant PBR materials, metres, Z up and centred horizontal envelope. One complete isolated static opening fixture, zero scenes and no host building. Only the displayed fixed pose is represented: no extension kinematics, sliding or rolling operation, lock/security, pinch clearances, emergency egress, access, load, installation or safety certification.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
