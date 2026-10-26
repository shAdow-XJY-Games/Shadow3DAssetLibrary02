import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='theatre-fixed-four-screw-platform-and-cutaway-stage-pit-01'
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



# A shared material boundary for the floor and fixed sectioned retaining enclosure.
xs=[-2.20,-2.04,2.04,2.20];ys=[-1.30,-1.14,0,1.14,1.30];zs=[0,.18,.32,2.00]
occupied=set()
for i in range(len(xs)-1):
 for j in range(len(ys)-1):
  for k in range(len(zs)-1):
   solid=k==0 or i==0 or j==3 or (i==2 and j>=2) or (j==0 and k==1)
   if solid:occupied.add((i,j,k))
v=[];f=[];idx={}
def vid(p):
 if p not in idx:idx[p]=len(v);v.append(p)
 return idx[p]
for i,j,k in sorted(occupied):
 p=[(x,y,z)for z in[zs[k],zs[k+1]]for y in[ys[j],ys[j+1]]for x in[xs[i],xs[i+1]]]
 for q,step in zip(BOX,[(0,0,-1),(0,0,1),(0,-1,0),(0,1,0),(-1,0,0),(1,0,0)]):
  if(i+step[0],j+step[1],k+step[2])not in occupied:f.append(tuple(vid(p[n])for n in q))
mesh('WholeGroundFootSectionedPitFloorAndWalls',v,f,0)
# Fixed stage edge follows only the retained wall crowns, not the cutaway side.
box('WholeFixedRearStageEdge',(0,1.22,2.025),(4.44,.28,.060),3)
box('WholeFixedLeftStageEdge',(-2.12,-.10,2.025),(.28,2.36,.060),3)
box('WholeFixedRightRearStageEdge',(2.12,.57,2.025),(.28,1.02,.060),3)
# One complete helical ridge, not independent rings or a claimed functional thread.
def helix(name,x,y,z0,z1,r,mat):
 turns=9;steps=216;v=[];f=[]
 for k in range(steps+1):
  a=math.tau*turns*k/steps;z=z0+(z1-z0)*k/steps
  for rr,dz in[(r-.006,-.009),(r+.012,-.004),(r+.012,.004),(r-.006,.009)]:v.append((x+rr*math.cos(a),y+rr*math.sin(a),z+dz))
 for k in range(steps):
  for j in range(4):h=(j+1)%4;f.append((4*k+j,4*k+h,4*(k+1)+h,4*(k+1)+j))
 f +=[(3,2,1,0),tuple(4*steps+j for j in range(4))]
 mesh(name,v,f,mat)
for x in[-1.75,1.75]:
 for y in[-.85,.85]:
  tag=str((x,y))
  box('WholeCornerDriveCase_'+tag,(x,y,.30),(.24,.23,.25),1)
  box('WholeCornerUpperHead_'+tag,(x,y,1.82),(.25,.20,.10),1)
  for dx in[-.10,.10]:box('WholeVerticalGuideBar_'+tag+str(dx),(x+dx,y,1.06),(.027,.034,1.53),1)
  lathe_z('WholeVerticalScrewCore_'+tag,x,y,[(0,.28),(.035,.28),(.035,1.87),(0,1.87)],2,20)
  helix('WholeContinuousThreadRidge_'+tag,x,y,.40,1.75,.035,2)
  lathe_z('WholeBoredIntermediateCarrier_'+tag,x,y,[(.043,.92),(.076,.92),(.076,1.12),(.043,1.12)],2,20)
  # Full carrier shoulder connects to both the frame sleeve and the platform underframe.
  side=1 if x>0 else-1
  box('WholePlatformCarrierShoulder_'+tag,(side*1.62,y,1.01),(.32,.12,.10),1)
# Full common underframe and blank timber platform, an integral apparatus not a separate old stage.
for y in[-.85,.85]:box('WholePlatformLongBearer_'+str(y),(0,y,1.01),(3.30,.13,.12),1)
for x in[-1.56,0,1.56]:box('WholePlatformCrossBearer_'+str(x),(x,0,1.01),(.105,1.70,.105),1)
box('WholeIntermediateTimberPlatform',(0,0,1.105),(3.28,1.82,.080),3)
# Complete low connecting shaft appearances meet all four whole corner cases.
for y in[-.85,.85]:axle('WholeLowTransverseShaft_'+str(y),-1.76,1.76,y,.30,.024,2,16)
cyly('WholeLowSideReturnShaft',-.86,.86,1.75,.30,.024,2,16)
box('WholeBlankDriveHousing',(1.75,0,.31),(.30,.38,.27),1)
box('WholeDriveHousingFoot',(1.75,0,.205),(.36,.45,.060),1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeSectionedPit_MatteConcrete',(.42,.43,.40,1),.94,0),('WholeFramesAndCases_DeepTeal',(.08,.18,.20,1),.66,.24),('WholeShaftsThreadsAndCarriers_SatinAlloy',(.43,.47,.48,1),.43,.55),('WholeFixedAndIntermediateDecks_WarmTimber',(.48,.30,.14,1),.78,0)]
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
focus=Vector((0,0,.95))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=6.25;aim(cam,(5,-7,5.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/theatre/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'theatre','style':'S01-clean-geometric','title':'Fixed Four Screw Platform and Cutaway Stage Pit','description':'One newly authored complete empty stage-pit platform apparatus in a fixed intermediate-height cutaway. A shared thick grounded pit floor and rear/side retaining walls form one continuous material shell, with the front and near-right wall deliberately cut low to expose the interior. Complete fixed stage-edge boards remain over the uncut wall crowns. Four corner steel frames each enclose one entire continuous vertical shaft, a rooted full helical-ridge exterior and a genuine bored carrier sleeve; the four carriers connect by full shoulders to one common open underframe and broad blank intermediate platform. Whole low corner cases, two transverse shafts, a side return shaft and one blank motor-like case share the bottom support structure. No old lift, stage deck or railway turntable mesh imported. Unlike the old crossed-arm platform or centrally pivoted rail bridge, the new apparatus combines four vertical threaded/guide frames around an otherwise open central volume and one shared lowering-well architectural boundary. Four opaque matte concrete, dark frame, satin metal and timber PBR roles, metres Z up, whole horizontal-bounds-centred pit underside datum. One entire static architectural equipment prop zero scenes. The displayed positions and deliberate static material joins do not establish screw engagement, synchronous driving, power transmission, lifting, platform travel, load, human access, orchestra use, egress, structural or construction safety. No people, instruments, active machinery, rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
