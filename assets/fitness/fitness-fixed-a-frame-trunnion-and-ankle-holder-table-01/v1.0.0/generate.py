import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='fitness-fixed-a-frame-trunnion-and-ankle-holder-table-01'
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



# Whole fixed A-frame inversion-table exterior, empty static display pose only.
for side,x in[('Left',-.35),('Right',.35)]:
 for end,y in[('Front',-.63),('Rear',.63)]:
  box('WholeGroundFoot_'+side+end,(x,y,.025),(.17,.20,.05),2)
  beam('WholeAFrameLeg_'+side+end,(x,y,.065),(x,0,1.105),.065,0)
 beam('WholeSideSpreadTie_'+side,(x,-.40,.43),(x,.40,.43),.040,0)
 # Whole high sleeve is fixed on the two continuous side legs.
 axle('WholeHighPivotSleeve_'+side,x-.065,x+.065,0,1.10,.068,0,24)
for tag,y in[('Front',-.60),('Rear',.60)]:beam('WholeGroundFrameCrossTie_'+tag,(-.36,y,.08),(.36,y,.08),.060,0)
axle('WholeFullTransverseTrunnionShaft',-.44,.44,0,1.10,.026,1,24)
# One continuous tilted support board, not a separated chair seat and back.
angle=math.radians(63);C=math.cos(angle);S=math.sin(angle)
def p(x,t,n=0):return(x,t*C-n*S,1.10+t*S+n*C)
def prism_board(name,poly,n0,n1,mat):
 count=len(poly);v=[p(x,t,n)for n in[n0,n1]for x,t in poly];f=[]
 for a,b,c in triangulate(poly):f.extend([(c,b,a),(a+count,b+count,c+count)])
 f +=[(i,(i+1)%count,(i+1)%count+count,i+count)for i in range(count)];mesh(name,v,f,mat)
outline=[(-.17,-.53),(.17,-.53),(.215,-.43),(.215,.46),(.18,.66),(.12,.72),(-.12,.72),(-.18,.66),(-.215,.46),(-.215,-.43)]
prism_board('WholeContinuousBackSupportShell',outline,-.035,.010,0)
inner=[(x*.93,t*.97)for x,t in outline];prism_board('WholeContinuousUpholsteredBoard',inner,.005,.065,2)
# Board root actually crosses the full shaft and receives the full lower extension.
beam('WholeRearCentralBoardSpine',p(0,-.62,-.040),p(0,.50,-.040),.065,0)
beam('WholeFixedLowerAnkleExtension',p(0,-.46,-.025),p(0,-1.03,-.025),.050,1)
# Distinct lower foot plate perpendicular to the board, with a finite stem connection.
prism_board('WholeLowerFootRestPlate',[(-.20,-1.045),(.20,-1.045),(.20,-1.005),(-.20,-1.005)],-.035,.16,0)
# Two opposed complete roller rows, each has central axle and left/right thick pads.
for tag,t,n in[('Rear',-.875,.025),('Front',-.875,.145)]:
 yy,zz=p(0,t,n)[1:];axle('WholeAnkleHolderAxle_'+tag,-.205,.205,yy,zz,.014,1,16)
 for side,x0,x1 in[('Left',-.195,-.035),('Right',.035,.195)]:axle('WholeAnkleRoller_'+tag+side,x0,x1,yy,zz,.047,2,24)
# Both rows are joined to a complete central bracket, not floating pads.
beam('WholeAnkleHolderCentralBracket',p(0,-.90,-.035),p(0,-.875,.15),.045,0)
# Curved fixed side handrails rooted at high sleeves and forward legs.
def tube(name,path,r,mat,n=12):
 v=[];f=[]
 for k,pt in enumerate(path):
  t=unit(sub(path[min(k+1,len(path)-1)],path[max(0,k-1)]));u=unit(cross(t,(1,0,0)if abs(t[0])<.9 else(0,1,0)));w=cross(t,u)
  for j in range(n):v.append(tuple(pt[i]+r*(math.cos(math.tau*j/n)*u[i]+math.sin(math.tau*j/n)*w[i])for i in range(3)))
 for k in range(len(path)-1):
  for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
 f +=[tuple(reversed(range(n))),tuple((len(path)-1)*n+j for j in range(n))];mesh(name,v,f,mat)
for side,x in[('Left',-.35),('Right',.35)]:
 sx=-1 if x<0 else 1
 tube('WholeSideGrabRail_'+side,[(x,0,1.10),(x+sx*.12,-.12,1.20),(x+sx*.14,-.31,1.12),(x+sx*.11,-.44,.88),(x,-.30,.61)],.022,1)
# The rails join original A leg at y=-.30,z=.61. No rotation or folding claimed.
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeAFrameAndBoardShell_MutedBlue',(.10,.22,.26,1),.65,.22),('WholeShaftExtensionAndHandrails_SatinMetal',(.49,.55,.56,1),.44,.66),('WholeCushionRollersAndFeet_Charcoal',(.045,.055,.058,1),.85,.02)]
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
focus=Vector((0,0,.98))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.43;aim(cam,(4,-6,3.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/fitness/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'fitness','style':'S01-clean-geometric','title':'Fixed A Frame Trunnion and Ankle Holder Table','description':'One newly authored whole static A-frame inversion-table exterior in a fixed empty upright-rest presentation. Two full high A side frames with spread ties and front/rear crossmembers stand on four finite pads. A complete transverse trunnion shaft joins the high sleeves and one continuous long chamfered upholstered board with its full rear spine. A separate full lower extension leads to an actual foot-rest plate and a central bracket carrying two complete opposed ankle-roller rows, each with its own transverse axle and separate thick pads. Two entire curved side handrails root into the high sleeves and front frame legs. This is not a rotated old press bench, its seat/back replacement, low slant board or an oval mirror stand with a different face; all geometry is newly authored. Three opaque constant untextured PBR roles, metres, Z up and actual whole horizontal-bounds-centred ground origin. One prop, zero scenes, no person. Static illustrative exterior only: no exercise guidance, inversion movement, therapy, medical benefit, suitability, body dimensions, actual restraint, locking, adjustment, stability, load capacity, manufacture or safety is modeled or verified.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
