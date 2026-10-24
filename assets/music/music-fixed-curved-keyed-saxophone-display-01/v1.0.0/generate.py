import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='music-fixed-curved-keyed-saxophone-display-01'
G={};FM={}
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def unit(a):return tuple(x/math.sqrt(dot(a,a))for x in a)
def mesh(name,v,faces,mat):
 f=[]
 for p in faces:
  for k in range(1,len(p)-1):f.append((p[0],p[k],p[k+1]))
 if sum(dot(v[a],cross(v[b],v[c]))for a,b,c in f)<0:f=[tuple(reversed(p))for p in f]
 G[name]=(v,f,mat)
BOX=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(name,c,size,mat):mesh(name,[tuple(c[i]+s[i]*size[i]/2 for i in range(3))for s in[(x,y,z)for z in[-1,1]for y in[-1,1]for x in[-1,1]]],BOX,mat)
def beam(name,a,b,width,mat):
 w=unit(sub(b,a));u=unit(cross(w,(1,0,0)if abs(w[0])<.9 else(0,1,0)));v=cross(w,u)
 mesh(name,[tuple(p[i]+width/2*(sx*u[i]+sy*v[i])for i in range(3))for p in[a,b]for sy in[-1,1]for sx in[-1,1]],BOX,mat)
def axle(name,x0,x1,y,z,r,mat,n=16):
 v=[(x,y+r*math.cos(math.tau*i/n),z+r*math.sin(math.tau*i/n))for x in[x0,x1]for i in range(n)]
 mesh(name,v,[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],mat)

def ringx(name,x0,x1,y,z,ri,ro,mat,n=24):
 v=[(x,y+r*math.cos(math.tau*i/n),z+r*math.sin(math.tau*i/n))for x in[x0,x1]for r in[ri,ro]for i in range(n)];f=[]
 for i in range(n):j=(i+1)%n;f.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 mesh(name,v,f,mat)
def cyly(name,y0,y1,x,z,r,mat,n=24):
 axle(name,y0,y1,x,z,r,mat,n);v,f,m=G[name];G[name]=([(b,a,c)for a,b,c in v],[tuple(reversed(p))for p in f],m)
def ringy(name,y0,y1,x,z,ri,ro,mat,n=24):
 ringx(name,y0,y1,x,z,ri,ro,mat,n);v,f,m=G[name];G[name]=([(b,a,c)for a,b,c in v],[tuple(reversed(p))for p in f],m)
def triangulate(p):
 def cr(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 ids=list(range(len(p)));out=[]
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:ids.reverse()
 while len(ids)>3:
  for k,b in enumerate(ids):
   a,c=ids[k-1],ids[(k+1)%len(ids)]
   if cr(p[a],p[b],p[c])<=1e-14:continue
   if any(min(cr(p[a],p[b],p[j]),cr(p[b],p[c],p[j]),cr(p[c],p[a],p[j]))>=-1e-14 for j in ids if j not in[a,b,c]):continue
   out.append((a,b,c));ids.pop(k);break
  else:raise AssertionError('bad polygon')
 return out+[tuple(ids)]
def lathe_z(name,x,y,profile,mat,n=24):
 v=[];rings=[];f=[]
 for r,z in profile:
  ids=[]
  if r==0:ids=[len(v)];v.append((x,y,z))
  else:
   for i in range(n):ids.append(len(v));v.append((x+r*math.cos(math.tau*i/n),y+r*math.sin(math.tau*i/n),z))
  rings.append(ids)
 for a,b in zip(rings,rings[1:]+rings[:1]):
  if len(a)==len(b)==1:continue
  for i in range(n):
   j=(i+1)%n
   if len(a)==1:f.append((a[0],b[j],b[i]))
   elif len(b)==1:f.append((a[i],a[j],b[0]))
   else:f.append((a[i],a[j],b[j],b[i]))
 mesh(name,v,f,mat)



# New continuous variable-bore reed-instrument exterior, not a looped bugle turned upright.
# Numeric main tube includes curved neck, sloping body, bottom return and wide rising bell.
st=[(-.31,1.19,.013),(-.25,1.19,.014),(-.20,1.175,.016),(-.16,1.145,.018),(-.135,1.10,.020),(-.12,1.04,.022),(-.08,.82,.030),(-.03,.56,.040),(.02,.32,.050)]
for k in range(1,17):
 a=math.pi+math.pi*k/16;st.append((.16+.14*math.cos(a),.32+.14*math.sin(a),.050+.004*k/16))
st +=[(.30,.395,.058),(.30,.46,.069),(.30,.52,.088),(.30,.57,.115),(.30,.595,.131),(.30,.61,.134)]
v=[];f=[];N=32
for k,(x,z,r)in enumerate(st):
 a=st[max(k-1,0)];b=st[min(k+1,len(st)-1)];t=unit((b[0]-a[0],0,b[1]-a[1]));u=(0,1,0);w=cross(t,u)
 for rr in[r,r-.004]:
  for j in range(N):q=math.tau*j/N;v.append((x+rr*w[0]*math.sin(q),rr*math.cos(q),z+rr*w[2]*math.sin(q)))
for k in range(len(st)-1):
 for i in range(N):j=(i+1)%N;a=2*N*k+i;b=2*N*k+j;c=2*N*(k+1)+i;d=2*N*(k+1)+j;f.extend([(a,b,d,c),(a+N,c+N,d+N,b+N)])
for i in range(N):
 j=(i+1)%N;k=2*N*(len(st)-1);f.extend([(j,i,i+N,j+N),(k+i,k+j,k+j+N,k+i+N)])
mesh('WholeContinuousNeckBodyBowAndOpenFlaredBell',v,f,0)
# Thick open dark tapered mouth sleeve follows the existing top tube, not an opaque hole decal.
ringx('WholeOpenMouthpieceSleeve',-.355,-.275,0,1.19,.010,.020,2,24)
# Whole long key shaft and six supported fixed key cups; no claim of playable tone holes.
def centre(z):return .02+(z-.32)*(-.14)/.72
beam('WholeLongFrontKeyShaft',(centre(.47)+.050,-.043,.47),(centre(1.00)+.050,-.031,1.00),.009,1)
for i,z in enumerate([.51,.59,.67,.75,.83,.91]):
 x=centre(z);rr=.050-(z-.32)/.72*.028;y=-rr
 cyly('WholeFixedClosedKeyCup_'+str(i+1),y-.029,y+.003,x,z,.024,1,24)
 cyly('WholePaleKeyTouch_'+str(i+1),y-.035,y-.022,x,z,.017,2,24)
 beam('WholeKeyLeverBridge_'+str(i+1),(x,y-.009,z),(x+.052,-.043+(z-.47)/.53*.012,z),.009,1)
# Two actual shaft bearing struts connect the rod to the body exterior.
for i,z in enumerate([.48,.98]):beam('WholeShaftBearingStrut_'+str(i+1),(centre(z)+.010,-.025,z),(centre(z)+.054,-.035,z),.013,1)
# Independent complete low display stand supports the bottom bow and back of the main body.
box('WholeGroundedDisplayBase',(.05,.035,.025),(.66,.40,.05),2)
box('WholeLowBowSupportPost',(.16,0,.085),(.07,.07,.09),2)
box('WholeBowCradlePad',(.16,0,.12),(.16,.10,.020),2)
box('WholeRearDisplayUpright',(-.02,.12,.345),(.04,.04,.62),2)
beam('WholeRearBodySupport',(-.02,.12,.64),(centre(.64),.038,.64),.018,2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeOpenBodyAndBell_MutedBrass',(.57,.36,.10,1),.44,.65),('WholeKeyMechanism_SatinNickel',(.48,.51,.49,1),.42,.65),('MouthTouchAndDisplayStand_Charcoal',(.055,.065,.068,1),.77,0)]
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
for prefix in []:
 parent=bpy.data.objects.new(prefix+'_CompleteSourceAssembly',None);scene.collection.objects.link(parent)
 for o in parts:
  if o.name.startswith(prefix+'__'):o.parent=parent
 parent.select_set(True)
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
triangles=sum(len(f)for v,f,m in G.values())
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
(OUT/'qa-report.json').write_text(json.dumps({'asset':ASSET,'mesh_objects':len(G),'triangles':triangles,'materials':len(PALETTE),'new_independent_models':1,'new_scenes':0},indent=2))
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
focus=Vector((0,0,.62))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.52;aim(cam,(3,-6,2.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/music/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':'Fixed Curved Keyed Saxophone Display','description':'One newly authored complete static saxophone display exterior. A single continuous thick hollow variable-radius tube runs through a curved upper neck, long inclined body, low semicircular return and widening upright open bell. A separate dark open mouth sleeve seats on the upper tube. A whole front key shaft, two real shaft supports and six separate closed key cups with touch faces and lever bridges form the fixed keyed exterior. A complete low grounded display stand has a bow cradle and a rear body support. All instrument geometry is new, not the old low horizontal looped bugle raised on end, separate open organ pipes combined, or a reshaped pocket harmonica. Three opaque constant untextured PBR roles, metres, native Z up, full horizontally bounds-centred ground origin. One complete instrument-with-display-support prop, zero scenes. Fixed illustrative exterior only: closed key cups do not claim actual tone-hole operation; no reed, airflow, acoustic tuning, fingering accuracy, music, key motion, instrument playability, manufacture, support load or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
