import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='sports-fixed-open-vent-round-canopy-and-empty-suspension-rig-01'
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



# One thick annular dome shell: top vent stays genuinely empty through both skins.
N=64;profile=[(.13,3.20),(.32,3.19),(.66,3.08),(.95,2.85),(1.16,2.50),(1.20,2.28)];v=[];f=[];mats=[]
for side in[0,1]:
 for k,(r,z)in enumerate(profile):
  for j in range(N):
   a=math.tau*j/N;bulge=math.sin(math.pi*(j%4)/4);rr=r*(1-.025*bulge*(r/1.2)**2);zz=z+(.065*bulge if k==len(profile)-1 else .018*bulge*(r/1.2))-.014*side
   v.append((rr*math.cos(a),rr*math.sin(a),zz))
L=len(profile)*N
for side in[0,1]:
 for k in range(len(profile)-1):
  for j in range(N):q=(j+1)%N;a=side*L+k*N+j;b=side*L+k*N+q;c=side*L+(k+1)*N+q;d=side*L+(k+1)*N+j;f.append((a,b,c,d)if side==0 else(d,c,b,a));mats.append((j//4)%2)
for k in[0,len(profile)-1]:
 for j in range(N):q=(j+1)%N;a=k*N+j;b=k*N+q;f.append((a,L+a,L+b,b)if k==0 else(b,L+b,L+a,a));mats.append((j//4)%2)
mesh('WholeOpenVentAndScallopedHemCanopyShell',v,f,0);FM['WholeOpenVentAndScallopedHemCanopyShell']=[m for m in mats for _ in range(2)]
# Newly authored complete empty lower webbing loops and real connecting straps.
def ovalband(name,cx,cy,rx,ry,z0,z1,w):
 n=32;v=[(cx+(rx-d)*math.cos(math.tau*j/n),cy+(ry-d)*math.sin(math.tau*j/n),z)for z,d in[(z0,0),(z1,0),(z0,w),(z1,w)]for j in range(n)];f=[]
 for j in range(n):q=(j+1)%n;f +=[(j,q,n+q,n+j),(2*n+j,3*n+j,3*n+q,2*n+q),(j,2*n+j,2*n+q,q),(n+j,n+q,3*n+q,3*n+j)]
 mesh(name,v,f,3)
ovalband('WholeEmptyWaistWebbingLoop',0,0,.19,.13,.255,.310,.025)
for j,x in enumerate([-.092,.092]):
 ovalband('WholeGroundFootEmptyLegLoop_%d'%j,x,0,.079,.102,0,.046,.022)
 for k,s in enumerate([-1,1]):beam('WholeLegToWaistWebbing_%d_%d'%(j,k),(x,s*.086,.031),(x*1.55,s*.076,.275),.029,3)
# Four whole risers; suspension lines are complete solid appearances, not simulated cables.
for j,(sx,sy)in enumerate([(-1,-1),(1,-1),(1,1),(-1,1)]):
 beam('WholeLowerRiserStrap_%d'%j,(sx*.147,sy*.077,.280),(sx*.165,sy*.105,.620),.033,3)
for j in range(16):
 a=math.tau*j/16;sx=1 if math.cos(a)>=0 else -1;sy=1 if math.sin(a)>=0 else -1
 start=(sx*.165,sy*.105,.605);end=(1.20*math.cos(a),1.20*math.sin(a),2.274)
 beam('WholeContinuousSuspensionLine_%02d'%j,start,end,.010,2)
PALETTE=[('WholeCanopyGores_WarmIvory',(.87,.83,.70,1),.87,0),('WholeCanopyGores_MutedCoral',(.66,.22,.10,1),.85,0),('WholeCompleteSuspensionLines_PaleCord',(.62,.65,.61,1),.89,0),('WholeEmptyLowerRig_CharcoalWebbing',(.055,.075,.072,1),.92,0)]
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
focus=Vector((0,0,1.55))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=4.05;aim(cam,(6,-9,5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/sports/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'sports','style':'S01-clean-geometric','title':'Fixed Open Vent Round Canopy and Empty Suspension Rig','description':'One newly authored complete round-parachute-style fixed expanded art pose. A single continuous finite-thickness domed fabric shell has a true circular crown vent, sixteen integral softly scalloped radial gores and a wholly open underside. Sixteen complete suspension-line appearances run from the lower hem to four full lower riser straps, which join a newly authored empty waist and two leg-loop rig. There is no central mast, ribs, spreaders, basket, burner or copied harness. The open-bottom broad canopy and converging many-line-to-small-empty-rig relation differs from both the old shallow pole-supported parasol and the old narrow-neck pear envelope over a basket. All visible numeric geometry is new, one whole prop zero scenes, four opaque constant PBR roles, metres Z up and whole horizontal-envelope-centred ground datum on the two lower loop edges. The unsupported-looking expanded pose is a fixed illustrative arrangement, not a physical equilibrium or deployment result. No pressure, airflow, descent rate, lift, inflation, packing, attachment, load, user fit, harness adequacy, flight or parachuting safety capability is represented. No rigging for motion, simulation, animation or interaction is delivered.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
