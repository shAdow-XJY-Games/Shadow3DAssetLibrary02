import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='interior-fixed-part-raised-auditorium-seat-01'
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

# A complete fixed floor-mounted tip-up auditorium seat, not a scissor folding chair.
PALETTE=[('CastStandardDarkSteel',(.16,.20,.21,1),.59,.42),('UpholsteryMutedBurgundy',(.40,.13,.12,1),.85,0),('ArmAndShellWarmGrey',(.40,.43,.40,1),.65,.12)]
def xprofile(name,p,x0,x1,m):
 pad(name,p,x0,x1,m);v,f,mi=G[name];record(name,[(y,x,z)for x,y,z in v],f,mi)
# Each full standard includes a broad fixed sole, seat pivot support and rear back upright.
profile=[(-.28,0),(.33,0),(.33,.045),(.25,.06),(.31,.94),(.24,.96),(.18,.54),(-.045,.49),(-.08,.12),(-.25,.06),(-.28,.045)]
for side in[-1,1]:
 x=side*.31;xprofile('WholeFloorStandard_'+str(side),profile,x-.026,x+.026,0)
 box('WholeArmSupport_'+str(side),(x-.025,-.16,.46),(x+.025,-.09,.68),0)
 arm=[(-.29,.665),(-.29,.695),(-.255,.72),(.29,.72),(.315,.695),(.315,.665)]
 xprofile('WholeArmrest_'+str(side),arm,x-.045,x+.045,2)
 for y in[-.20,.26]:
  pipe('WholeFloorFixingCap_'+str((side,y)),[(x,y,.043),(x,y,.052)],.024,2,12)
pipe('WholeSeatPivotAxle',[(-.355,.075,.46),(.355,.075,.46)],.025,0,16)
for side in[-1,1]:wheel('WholeSeatPivotBoss_'+str(side),side*.286,.075,.46,.060,0,.045,2)
# One thick whole pan, distinct from the back, in a clearly raised fixed position.
ang=math.radians(56);SD=(0,-math.cos(ang),math.sin(ang));SN=(0,math.sin(ang),math.cos(ang));P=(0,.075,.46)
def st(q):x,t,n=q;return add(add(P,(x,0,0)),add(mul(SD,t),mul(SN,n)))
seat=[(-.255,0),(.255,0),(.265,.35),(.225,.43),(-.225,.43),(-.265,.35)]
# pad XY-shaped pan via local coordinates; convert its extrusion to normal direction.
pad('WholeRaisedSeatPan',seat,-.035,.015,2);v,f,m=G['WholeRaisedSeatPan'];record('WholeRaisedSeatPan',[st((x,z,y))for x,y,z in v],f,m)
pad('WholeRaisedSeatCushion',[(-.225,.018),(.225,.018),(.235,.34),(.205,.397),(-.205,.397),(-.235,.34)],.012,.062,1);v,f,m=G['WholeRaisedSeatCushion'];record('WholeRaisedSeatCushion',[st((x,z,y))for x,y,z in v],f,m)
# One rear shell and one broad back cushion, both supported by the full rear standards.
back=[(-.28,.50),(.28,.50),(.285,.95),(.23,1.025),(-.23,1.025),(-.285,.95)]
pad('WholeSeparateBackShell',back,.22,.275,2)
pad('WholeBackCushion',[(-.248,.53),(.248,.53),(.253,.938),(.21,.985),(-.21,.985),(-.253,.938)],.175,.225,1)
box('WholeRearBackCrossTie',(-.31,.25,.58),(.31,.30,.625),0)
# Fixed pan underside counterbalance exterior, no spring or return behaviour claim.
box('WholeSeatUndersideCounterbalance',(-.20,.02,-.090),(.20,.12,-.030),0);v,f,m=G['WholeSeatUndersideCounterbalance'];record('WholeSeatUndersideCounterbalance',[st(q)for q in v],f,m)
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
focus=Vector((0,0,.50))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.43;aim(cam,(5,-7,3.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/interior/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'interior','style':'S01-clean-geometric','title':'Fixed Part Raised Auditorium Seat','description':'One original complete fixed floor-mounted auditorium seat with two whole cast-style floor standards, broad fixing soles and rear back supports, two armrests, a separate broad back shell/cushion and one distinct thick seat pan/cushion held at 56 degrees on a full transverse pivot axle and end bosses. A fixed pan underside counterbalance exterior is visible; no actuation is provided. This is not a crossed-frame canvas camp chair or a continuous cantilever dining shell tilted as a whole: only the separate seat rises between fixed standards and back. All whole geometry is newly authored, three opaque PBR materials, metre scale and true XY-centred ground origin; one static model, no scene or occupant. No automatic return, spring force, human fit, seating comfort, load, installation, aisle clearance, fire or safety compliance claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
