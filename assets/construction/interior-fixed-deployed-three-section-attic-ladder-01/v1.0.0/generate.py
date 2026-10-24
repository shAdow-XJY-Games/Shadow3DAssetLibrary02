import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='interior-fixed-deployed-three-section-attic-ladder-01'
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

# One fixed deployed ceiling hatch and three-section attic ladder assembly.
PALETTE=[('AtticTimber',(.49,.34,.20,1),.82,0),('AtticHatchIvory',(.63,.64,.57,1),.85,0),('AtticSteel',(.25,.29,.28,1),.62,.55)]
# Closed rectangular hollow ceiling curb; actual horizontal passage, no host slab.
v=[];f=[]
for zz in[2.42,2.56]:
 for xx,yy in[(.43,1.25),(.36,1.18)]:v.extend([(-xx,-.07,zz),(xx,-.07,zz),(xx,yy,zz),(-xx,yy,zz)] if xx==.43 else[(-xx,0,zz),(xx,0,zz),(xx,yy,zz),(-xx,yy,zz)])
for i in range(4):
 j=(i+1)%4
 for q in[(i,j,j+8,i+8),(i+4,i+12,j+12,j+4),(i,i+4,j+4,j),(i+8,j+8,j+12,i+12)]:f.extend([(q[0],q[1],q[2]),(q[0],q[2],q[3])])
record('WholeHorizontalCeilingOpeningCurb',v,f,1)
# s descends from the upper fixed pivot toward grounded feet; n offsets from ladder plane.
D=(0,-.48,-.87726848798);T=(0,.87726848798,-.48);length=2.40/(-D[2])
def tr(p):
 x,n,s=p;return(x,D[1]*s+T[1]*n,2.42+D[2]*s+T[2]*n)
def obox(name,lo,hi,m):
 box(name,lo,hi,m);v,f,mm=G[name];record(name,[tr(p)for p in v],f,mm)
# Downfolded complete door panel lies behind the upper ladder, hinged on the curb front.
obox('WholeLoweredHatchDoor',(-.35,.045,0),(.35,.082,1.15),1)
for side in[-1,1]:
 x=side*.28
 for k in range(3):
  s0=k*length/3+.012;s1=(k+1)*length/3-.012
  obox('WholeSectionRail_'+str(side)+'_'+str(k),(x-.032,-.035,s0),(x+.032,.035,s1),0)
 for k in[1,2]:
  s=k*length/3
  obox('WholeSectionHingePlate_'+str(side)+'_'+str(k),(x+side*.038-.009,-.044,s-.075),(x+side*.038+.009,.044,s+.075),2)
  p=tr((x,0,s));pipe('WholeSectionPivot_'+str(side)+'_'+str(k),[(x-.05,p[1],p[2]),(x+.05,p[1],p[2])],.018,2,12)
 # Explicit fixed top transverse hinge, seating ladder and hatch to the curb front.
 pipe('WholeTopHinge_'+str(side),[(x-.07,0,2.42),(x+.07,0,2.42)],.032,2,16)
 # Two linked side limiter arms show the fold linkage, not a claim of operation.
 a=(side*.39,.64,2.46);c=(side*.39,.12,1.98);e=tr((side*.33,.07,.85))
 pipe('WholeUpperLimiter_'+str(side),[a,c],.016,2,8);pipe('WholeLowerLimiter_'+str(side),[c,e],.016,2,8)
 pipe('WholeLimiterKnee_'+str(side),[(side*.39-.025,c[1],c[2]),(side*.39+.025,c[1],c[2])],.025,2,12)
 p=tr((x,0,length-.02));box('WholeGroundShoe_'+str(side),(x-.047,p[1]-.065,0),(x+.047,p[1]+.065,.055),2)
for i in range(9):
 s=.20+i*(length-.38)/8;p=tr((0,0,s))
 # Horizontal complete tread, rather than tilting the walking surface with the rail.
 box('WholeHorizontalTread_'+str(i),(-.285,p[1]-.070,p[2]-.018),(.285,p[1]+.070,p[2]+.018),0)
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
focus=Vector((0,0,1.28))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=4.1;aim(cam,(5,-7,4.3));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/construction/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'military','style':'S01-clean-geometric','title':'Fixed Deployed Three Section Attic Ladder','description':'One original complete fixed-deployed attic access ladder appearance. A thick horizontal ceiling curb has a real through-opening. Its lowered whole hatch panel lies behind the first of three distinct ladder sections; explicit section hinge plates and cross pins join the six full rails, with nine whole horizontal treads, two grounded shoes, top hinge bearings and paired fixed two-link side limiters connected to the curb. All geometry newly authored, no old A-frame, wheeled library ladder or vertical airlock model reused. Three opaque constant PBR materials, metre game units, Z-up, horizontally centred ground origin. One static prop, zero scenes, no surrounding ceiling or host building. The ceiling curb is an intentionally unsupported mounting interface without a supplied host. No folding motion, mechanism clearance, locking, climbing, accessibility, load, fit, installation, manufacture or building safety capability is claimed.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
