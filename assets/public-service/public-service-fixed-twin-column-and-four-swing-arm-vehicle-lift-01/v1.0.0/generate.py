import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='public-service-fixed-twin-column-and-four-swing-arm-vehicle-lift-01'
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



def prismz(name,p,z0,z1,mat):
 N=len(p);v=[(x,y,z)for z in[z0,z1]for x,y in p];f=[]
 for a,b,c in triangulate(p):f +=[(c,b,a),(a+N,b+N,c+N)]
 f +=[(i,(i+1)%N,(i+1)%N+N,i+N)for i in range(N)];mesh(name,v,f,mat)
def sleevesquare(name,a,b,outer,inner,mat):
 w=unit(sub(b,a));u=(-w[1],w[0],0);v=(0,0,1);vs=[]
 for p in[a,b]:
  for rr in[outer/2,inner/2]:
   for x,y in[(-rr,-rr),(rr,-rr),(rr,rr),(-rr,rr)]:vs.append(tuple(p[k]+x*u[k]+y*v[k]for k in range(3)))
 fs=[]
 for i in range(4):j=(i+1)%4;fs +=[(i,j,4+j,4+i),(8+i,12+i,12+j,8+j),(i,8+i,8+j,j),(4+i,4+j,12+j,12+i)]
 mesh(name,vs,fs,mat)
for side in[-1,1]:
 x=side*1.70
 box('WholeGroundFootColumnPlate_'+str(side),(x,0,.05),(.61,.76,.10),3)
 p=[(1.54,-.23),(1.86,-.23),(1.86,.23),(1.54,.23),(1.54,.16),(1.77,.16),(1.77,-.16),(1.54,-.16)]
 if side<0:p=[(-a,b)for a,b in reversed(p)]
 prismz('WholeInwardOpenColumn_'+str(side),p,.085,3.30,0)
 box('WholeFixedSideGuideCarriage_'+str(side),(side*1.60,0,1.14),(.17,.285,.56),1)
 for k,z in enumerate([.97,1.32]):
  box('WholeGuideRollerRoot_'+str((side,k)),(side*1.69,0,z),(.16,.10,.075),3)
  cyly('WholeColumnGuideRoller_'+str((side,k)),-.11,.11,side*1.72,z,.057,3,20)
 box('WholeArmBearingSaddle_'+str(side),(side*1.48,0,.91),(.28,.66,.14),1)
 for end in[-1,1]:
  a=(side*1.44,end*.23,.995);target=(side*.51,end*(1.10 if end<0 else .88),.995)
  d=sub(target,a);b=tuple(a[k]+d[k]*.67 for k in range(3));c=tuple(a[k]+d[k]*.59 for k in range(3))
  lathe_z('WholeArmVerticalPivot_'+str((side,end)),a[0],a[1],[(0,.84),(.052,.84),(.052,1.09),(0,1.09)],3,20)
  lathe_z('WholeArmPivotCollar_'+str((side,end)),a[0],a[1],[(.051,.945),(.095,.945),(.095,1.045),(.051,1.045)],1,24)
  sleevesquare('WholeOpenOuterArmSleeve_'+str((side,end)),a,b,.16,.105,1)
  beam('WholeInnerArmExtension_'+str((side,end)),c,target,.108,3)
  lathe_z('WholeEndPadStem_'+str((side,end)),target[0],target[1],[(0,.97),(.035,.97),(.035,1.14),(0,1.14)],3,20)
  lathe_z('WholeBluntRoundEndPad_'+str((side,end)),target[0],target[1],[(0,1.125),(.105,1.125),(.105,1.175),(0,1.175)],2,24)
 # Small opaque stop faces on the column are distinct insets, not coplanar strips.
 box('WholeColumnLowerStop_'+str(side),(side*1.70,0,.19),(.20,.28,.08),3)
box('WholeHighCrosshead',(0,0,3.34),(3.78,.29,.16),0)
box('WholeHighInsetCrossheadFace',(0,-.155,3.34),(2.95,.035,.085),1)
box('WholeSideServiceCase',(1.99,.05,1.48),(.30,.30,.52),0)
box('WholeBlankControlPlaque',(1.99,-.115,1.54),(.19,.035,.20),2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeColumnsAndCrosshead_MutedBlue',(.12,.28,.36,1),.66,.11),('WholeCarriagesAndArms_DullOchre',(.64,.39,.13,1),.68,.08),('WholePadsAndControls_Charcoal',(.04,.047,.05,1),.86,.01),('WholeGuidesExtensionsBases_SatinGrey',(.36,.40,.40,1),.52,.35)]
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
focus=Vector((0,0,1.65))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=5.70;aim(cam,(5,-8,5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/public-service/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'public-service','style':'S01-clean-geometric','title':'Fixed Twin Column and Four Swing Arm Vehicle Lift','description':'One wholly newly authored complete empty twin-column vehicle-lift-style static exterior. Two wide independent ground sole plates support complete inward-open tall C-channel columns joined only by a high crosshead. Each column contains a fixed guide-carriage appearance and separate finite rollers, with a lower outward saddle carrying two independent vertical pivot appearances. Four full arms open diagonally into the empty central bay; each has a genuinely hollow rectangular outer sleeve, smaller continuous inner extension and raised blunt round end pad. A rooted side service case and blank control complete the entire stationary machine. Unlike the manual stacker, there is no wheeled straddle chassis, shared rear carriage, pair of straight elevated forks or winch cable. Unlike the scissor platform, no crossed supporting links or continuous upper deck fill the centre: two separate side carriages and four independently directed pad-ended arms organize the whole object. New geometry only, not duplicating old stacker masts or placing old jack parts in a frame. Four opaque PBR roles, metre coordinates, Z up and whole centred ground datum, one model zero scenes. Empty fixed artistic exterior only; channel contacts and partly nested sleeves are illustrative embedded joins. No vehicle, load, drive internals, synchronized lift, arm sweep, extension travel, pad fit, hydraulics, anchoring design, structural rating, operation, manufacture, installation or safe-use capability. Rigging animation interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
