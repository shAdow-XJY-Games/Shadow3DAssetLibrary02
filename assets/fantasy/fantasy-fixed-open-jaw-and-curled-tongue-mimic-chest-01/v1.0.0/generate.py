import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='fantasy-fixed-open-jaw-and-curled-tongue-mimic-chest-01'
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

# One complete stylized fantasy mimic: hollow lower jaw, raised barrel-vault upper jaw,
# real projecting teeth, one continuous curled tongue and four short creature feet.
PALETTE=[('MimicWarmTimber',(.31,.16,.075,1),.80,0),('MimicIvoryTeeth',(.78,.73,.54,1),.70,0),('MimicDarkMouthAndTongue',(.24,.075,.095,1),.73,0)]
def rect(w,y0,y1,r):return[(-w+r,y0),(w-r,y0),(w,y0+r),(w,y1-r),(w-r,y1),(-w+r,y1),(-w,y1-r),(-w,y0+r)]
outer=rect(.60,-.36,.36,.065);inner=rect(.535,-.295,.295,.055)
v=[(x,y,z)for p,z in[(outer,.14),(outer,.60),(inner,.60),(inner,.245)]for x,y in p];f=[];bodym=[]
for k in range(3):
 for i in range(8):
  j=(i+1)%8;f.extend([(k*8+i,k*8+j,(k+1)*8+j),(k*8+i,(k+1)*8+j,(k+1)*8+i)]);bodym.extend([2 if k==2 else 0]*2)
for ring,z,reverse in[(0,.14,True),(24,.245,False)]:
 c=len(v);v.append((0,0,z))
 for i in range(8):
  a=ring+i;b=ring+(i+1)%8;f.append((c,b,a)if reverse else(c,a,b));bodym.append(0 if reverse else 2)
record('WholeThickHollowLowerJaw',v,f,0)
# Upper jaw is a thick continuous curved shell, not a rectangular freezer lid.
profile=[]
for i in range(13):
 a=math.pi*i/12;profile.append((.36*math.cos(a),.60+.28*math.sin(a)))
for i in range(12,-1,-1):
 a=math.pi*i/12;profile.append((.305*math.cos(a),.60+.225*math.sin(a)))
pad('WholeCurvedUpperJawShell',profile,-.60,.60,0)
v,f,m=G['WholeCurvedUpperJawShell'];record('WholeCurvedUpperJawShell',[(y,x,z)for x,y,z in v],f,m)
# Fixed open pose about the entire rear joint, all upper teeth and eyebrow ridges follow it.
ANGLE=math.radians(-39)
def raisejaw(name):
 v,f,m=G[name];record(name,[(x,.36+(y-.36)*math.cos(ANGLE)-(z-.60)*math.sin(ANGLE),.60+(y-.36)*math.sin(ANGLE)+(z-.60)*math.cos(ANGLE))for x,y,z in v],f,m)
upper=['WholeCurvedUpperJawShell']
def tooth(name,c,tip,rx,ry,m=1):
 x,y,z=c;v=[(x-rx,y-ry,z),(x+rx,y-ry,z),(x+rx,y+ry,z),(x-rx,y+ry,z),tip];f=[(0,2,1),(0,3,2),(0,1,4),(1,2,4),(2,3,4),(3,0,4)];record(name,v,f,m)
for i,x in enumerate([-.45,-.27,-.09,.09,.27,.45]):
 h=.17 if i in[0,5]else .125
 tooth('UpperFrontFang_'+str(i),(x,-.33,.61),(x*.96,-.29,.61-h),.053,.045);upper.append('UpperFrontFang_'+str(i))
 tooth('LowerFrontFang_'+str(i),(x,-.33,.585),(x*.96,-.28,.585+h*.85),.047,.042)
for side in[-1,1]:
 for j,y in enumerate([-.12,.12]):
  n='UpperSideFang_'+str(side)+'_'+str(j);tooth(n,(side*.56,y,.61),(side*.51,y,.47),.04,.045);upper.append(n)
  tooth('LowerSideFang_'+str(side)+'_'+str(j),(side*.565,y,.585),(side*.51,y,.72),.039,.043)
 # Raised wood brow ridges make a monster jaw rather than a stored-box decoration.
 n='WholeUpperBrowRidge_'+str(side);pipe(n,[(side*.14,-.337,.685),(side*.36,-.323,.745),(side*.49,-.28,.77)],.037,0,6);upper.append(n)
for n in upper:raisejaw(n)
pipe('WholeRearJawJoint',[(-.59,.36,.60),(.59,.36,.60)],.045,2,12)
# One thick non-circular tongue swept through seven nonuniform elliptical sections.
path=[((0,.10,.26),.16,.035),((0,-.16,.34),.18,.040),((0,-.34,.62),.17,.037),((0,-.58,.48),.145,.033),((0,-.76,.21),.11,.030),((0,-.83,.07),.085,.027),((0,-.94,.12),.045,.022)]
v=[];seg=8
for k,(p,rx,rn)in enumerate(path):
 tangent=unit(sub(path[min(k+1,len(path)-1)][0],path[max(k-1,0)][0]));side=(1,0,0);normal=unit(cross(side,tangent))
 for i in range(seg):a=math.tau*i/seg;v.append(add(p,add(mul(side,rx*math.cos(a)),mul(normal,rn*math.sin(a)))))
f=[]
for k in range(len(path)-1):
 for i in range(seg):j=(i+1)%seg;a=k*seg+i;b=k*seg+j;c=(k+1)*seg+j;d=(k+1)*seg+i;f.extend([(a,b,c),(a,c,d)])
for k in [0,len(path)-1]:
 c=len(v);v.append(path[k][0])
 for i in range(seg):f.append((c,k*seg+(i+1)%seg,k*seg+i)if k==0 else(c,k*seg+i,k*seg+(i+1)%seg))
record('WholeContinuousCurledTongue',v,f,2)
# Four short closed wedge feet actually reach the floor and lower jaw; no loose props.
for side in[-1,1]:
 for y in[-.23,.23]:
  x=side*.46
  pad('WholeShortCreatureFoot_'+str(side)+'_'+str(y),[(x-.11,0),(x+.11,0),(x+.09,.18),(x-.08,.22)],y-.085,y+.085,0)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
FM={n:[m]*len(f)for n,(v,f,m)in G.items()}
FM['WholeThickHollowLowerJaw']=bodym
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
focus=Vector((0,0,.57))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.92;aim(cam,(5,-8,4.0));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/fantasy/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'fantasy','style':'S01-clean-geometric','title':'Fixed Open Jaw and Curled Tongue Mimic Chest','description':'One original complete stylized fantasy mimic-chest creature in a fixed open-mouth pose: a continuous thick hollow eight-corner lower jaw, a separately raised continuous barrel-vault upper-jaw shell, two rows of actual projecting ivory fangs with lateral teeth, one broad continuously swept curled tongue emerging from the mouth and four short grounded creature feet. Whole rear jaw joint and shaped upper brow ridges belong to the creature. No old freezer, toy box or closed book meshes imported. The arched upper shell, inward fangs and curved organic tongue form one readable monster silhouette rather than an empty cabinet recolour or scattered loot. Three opaque constant PBR materials, metre scale, centred ground datum, one complete model and zero scenes. Stylized nonhuman fantasy art only, no animation, biting simulation, real anatomy, rigging, game mechanics, collision, manufacture or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
