import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='interior-fixed-suspended-ceiling-fan-light-01'
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

# Complete ceiling-suspended fan/light appearance; omitted host ceiling, no rotation.
PALETTE=[('MutedBrassMotorAndMounts',(.42,.35,.23,1),.46,.56),('WarmBladeTimber',(.42,.27,.15,1),.75,.02),('OpaqueIvoryDiffuser',(.73,.74,.66,1),.48,.03)]
def turned(name,profile,mi,n=32):
 v=[];rings=[];f=[]
 for r,z in profile:
  pts=[(0,0,z)]if r==0 else[(r*math.cos(math.tau*i/n),r*math.sin(math.tau*i/n),z)for i in range(n)]
  rings.append(list(range(len(v),len(v)+len(pts))));v+=pts
 for a,b in zip(rings,rings[1:]+rings[:1]):
  if len(a)==len(b)==1:continue
  for i in range(n):
   k=(i+1)%n
   if len(a)==1:f.append((a[0],b[i],b[k]))
   elif len(b)==1:f.append((a[i],b[0],a[k]))
   else:f.extend([(a[i],b[i],b[k]),(a[i],b[k],a[k])])
 record(name,v,f,mi)
turned('WholeCeilingCanopy',[(0,1.04),(.14,1.04),(.14,.99),(.10,.91),(.040,.89),(0,.89)],0)
pipe('WholeSuspensionDownrod',[(0,0,.515),(0,0,.945)],.023,0,20)
turned('WholeClosedMotorHousing',[(0,.31),(.16,.31),(.19,.37),(.19,.47),(.13,.53),(.04,.55),(0,.55)],0)
turned('WholeLowerDiffuserCollar',[(.125,.235),(.155,.235),(.155,.270),(.125,.270)],0)
turned('WholeOpaqueLampDiffuser',[(0,.080),(.07,.080),(.135,.13),(.149,.20),(.140,.253),(0,.253)],2)
pipe('WholeLampNeck',[(0,0,.252),(0,0,.335)],.065,0,24)
# Each broad horizontal paddle and its offset root bracket are whole bounded solids.
def flatpoly(name,poly,z0,z1,mi):
 nn=len(poly);v=[(x,y,z+.10*y)for z in[z0,z1]for x,y in poly];f=[]
 for a,b,c in earclip(poly):f.extend([(c,b,a),(a+nn,b+nn,c+nn)])
 for i in range(nn):k=(i+1)%nn;f.extend([(i,k,k+nn),(i,k+nn,i+nn)])
 record(name,v,f,mi)
def spin(name,a):
 vv,ff,m=G[name];record(name,[(x*math.cos(a)-y*math.sin(a),x*math.sin(a)+y*math.cos(a),z)for x,y,z in vv],ff,m)
for j in range(4):
 a=math.radians(22.5+90*j)
 n='WholePaddleBlade_'+str(j);flatpoly(n,[(.245,-.045),(.57,-.095),(.68,-.070),(.70,-.025),(.68,.070),(.56,.092),(.245,.045)],.383,.402,1);spin(n,a)
 n='WholeOffsetBladeBracket_'+str(j);flatpoly(n,[(.13,-.032),(.265,-.045),(.33,-.035),(.33,.035),(.265,.045),(.13,.032)],.352,.388,0);spin(n,a)
 for x in[.275,.31]:
  c=(x*math.cos(a),x*math.sin(a));pipe('WholeBladeMountCap_'+str((j,x)),[(c[0],c[1],.398),(c[0],c[1],.410)],.010,0,12)
# Two full hanging pull exteriors are independent of the opaque diffuser, not loose debris.
for x,zend in[(-.165,.035),(.165,.065)]:
 pipe('WholeHangingControlChain_'+str(x),[(x,0,.315),(x,0,zend+.025)],.0035,0,8)
 pipe('WholeControlPull_'+str(x),[(x,0,zend),(x,0,zend+.035)],.013,0,12)
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
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.80;aim(cam,(5,-7,3.0));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/interior/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'interior','style':'S01-clean-geometric','title':'Fixed Suspended Ceiling Fan Light','description':'One original complete suspended ceiling fan and light exterior. A full ceiling canopy and long downrod carry a closed rounded motor housing. Four broad whole horizontal paddles extend on their own bounded offset root brackets with finite mount caps; the lower neck, collar and opaque lamp diffuser form one central light appearance below the rotor plane. Two full pull-control chain exteriors end in finite small grips. No turbine, mine fan or chandelier mesh is imported or rescaled: the full suspended open horizontal-paddle mounting and lower diffuser differ from a grounded tall mast/nacelle vertical rotor and a skid-mounted bellmouth duct fan. Three constant opaque PBR materials, metres Z up, true whole XY centred. One isolated fixture, zero scenes; host ceiling is omitted, and minimum displayed Z is an export datum, not a ground-support claim. No animated rotation, blade sweep, airflow, cooling, illumination, electrical circuit, mounting load, installation or safety performance claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
