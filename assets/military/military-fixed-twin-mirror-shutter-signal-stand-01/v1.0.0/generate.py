import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='military-fixed-twin-mirror-shutter-signal-stand-01'
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

# A complete fixed twin-mirror and shutter optical-signal stand exterior.
PALETTE=[('CampStandMutedOlive',(.29,.33,.23,1),.72,.25),('MirrorFaceSatinSilver',(.58,.64,.65,1),.24,.88),('BearingsAndShutterDark',(.10,.14,.15,1),.57,.56)]
for j,a in enumerate([math.radians(-90),math.radians(30),math.radians(150)]):
 x=.40*math.cos(a);y=.40*math.sin(a);tx=.08*math.cos(a);ty=.08*math.sin(a)
 box('WholeTripodFoot_'+str(j),(x-.045,y-.045,0),(x+.045,y+.045,.035),2)
 pipe('WholeSplayedLeg_'+str(j),[(x,y,.025),(tx,ty,.76)],.026,0,12)
 pipe('WholeSpreader_'+str(j),[(0,0,.30),(.282*math.cos(a),.282*math.sin(a),.30)],.011,2,10)
pipe('WholeTripodCrown',[(0,0,.72),(0,0,.81)],.105,2,20)
box('WholeTransverseInstrumentBeam',(-.56,-.055,.79),(.56,.055,.855),0)
def discy(name,cx,cy,cz,ro,ri,th,m):
 wheel(name,0,0,0,ro,ri,th,m);v,f,mi=G[name];record(name,[(cx+y,cy+x,cz+z)for x,y,z in v],f,mi)
for label,cx,r,ang in [('Primary',-.27,.19,0),('Secondary',.31,.135,math.radians(-23))]:
 before=set(G);cz=1.095;half=r+.055
 p=[(cx-half,.835),(cx+half,.835),(cx+half,cz+.075),(cx+r+.018,cz+.075),(cx+r+.018,.88),(cx-r-.018,.88),(cx-r-.018,cz+.075),(cx-half,cz+.075)]
 pad(label+'WholeUFork',p,-.03,.03,0)
 discy(label+'WholeRoundMirrorRim',cx,0,cz,r+.012,r-.014,.040,2)
 discy(label+'WholeOpaqueMirrorFace',cx,-.015,cz,r-.008,0,.012,1)
 pipe(label+'WholeHorizontalMirrorAxle',[(cx-half-.015,0,cz),(cx+half+.015,0,cz)],.018,2,12)
 for side in[-1,1]:wheel(label+'WholePitchThumbwheel_'+str(side),cx+side*(half+.019),0,cz,.034,0,.018,2)
 # Secondary fork and full mirror group rotate together about their own fixed base, not detached pieces.
 if ang:
  for n in set(G)-before:
   v,f,m=G[n];record(n,[(cx+(x-cx)*math.cos(ang)-y*math.sin(ang),(x-cx)*math.sin(ang)+y*math.cos(ang),z)for x,y,z in v],f,m)
# One full finite open rectangular shutter frame, in front of the primary mirror, on two brackets.
cx=-.27;out=[(cx-.235,.86),(cx+.235,.86),(cx+.235,1.33),(cx-.235,1.33)];inn=[(cx-.205,.89),(cx+.205,.89),(cx+.205,1.30),(cx-.205,1.30)];v=[(x,y,z)for y,p in[(-.215,out),(-.185,out),(-.215,inn),(-.185,inn)]for x,z in p];f=[]
for i in range(4):
 j=(i+1)%4
 for a,b,c,d in[(i,j,4+j,4+i),(8+i,12+i,12+j,8+j),(i,8+i,8+j,j),(4+i,4+j,12+j,12+i)]:f.extend([(a,b,c),(a,c,d)])
record('WholeOpenShutterFrame',v,f,2)
for side in[-1,1]:pipe('WholeForwardShutterBracket_'+str(side),[(cx+side*.22,0,.84),(cx+side*.22,-.20,.875)],.016,0,12)
for j,z in enumerate([.94,1.045,1.15,1.255]):
 n='WholeFixedTiltedShutterLeaf_'+str(j);box(n,(cx-.209,-.052,-.009),(cx+.209,.052,.009),0);v,f,m=G[n];a=math.radians(42);record(n,[(x,-.20+y*math.cos(a)-zz*math.sin(a),z+y*math.sin(a)+zz*math.cos(a))for x,y,zz in v],f,m)
 pipe('WholeShutterLeafAxle_'+str(j),[(cx-.242,-.20,z),(cx+.242,-.20,z)],.009,2,8)
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
focus=Vector((0,0,.66))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.82;aim(cam,(5,-7,3.4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/military/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'military','style':'S01-clean-geometric','title':'Fixed Twin Mirror Shutter Signal Stand','description':'One original complete fixed non-weapon camp optical-signal-stand exterior: grounded three-foot splayed tripod and spreaders, one transverse instrument beam, two separate U-fork mirror supports with full round opaque metal discs/rims and transverse axle/thumbwheel exteriors, and a complete open shutter frame held in front of the larger disc by two finite forward brackets. Four fixed tilted shutter leaves and full thin axles preserve actual openings. The smaller entire fork/mirror is held at a different fixed yaw on the same beam; no optical alignment is implied. Not an imported shop wall mirror or a surveying telescope with its barrel removed: full new common-frame geometry, secondary mirror and shutter mounting relationship. Three opaque PBR materials, metres and XY-centred ground soles, one model and zero scenes. Static display only, no usable optics, signalling procedure, targeting, transmission, mirror tracking, reflection accuracy, motion, load or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
