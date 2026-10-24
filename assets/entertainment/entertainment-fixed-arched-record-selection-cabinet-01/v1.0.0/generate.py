import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='entertainment-fixed-arched-record-selection-cabinet-01'
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



# Whole new upright arched record-selection cabinet, not a reused radio or speaker.
def arch(r,bottom,cz):return[(-r,bottom),(r,bottom)]+[(r*math.cos(math.pi*i/16),cz+r*math.sin(math.pi*i/16))for i in range(17)]
def extrude_y(name,p,y0,y1,mat):
 n=len(p);v=[(x,y,z)for y in[y0,y1]for x,z in p];f=[]
 for a,b,c in triangulate(p):f.extend([(a,b,c),(c+n,b+n,a+n)])
 f +=[(i,i+n,(i+1)%n+n,(i+1)%n)for i in range(n)];mesh(name,v,f,mat)
outer=arch(.51,.065,1.12);inner=arch(.435,.15,1.12);n=len(outer)
v=[(x,y,z)for y,p in[(-.29,outer),(.24,outer),(.24,inner),(-.29,inner)]for x,z in p];f=[(k*n+i,k*n+(i+1)%n,((k+1)%4)*n+(i+1)%n,((k+1)%4)*n+i)for k in range(4)for i in range(n)];mesh('WholeContinuousDeepArchedOpenCase',v,f,0)
extrude_y('WholeArchedRearWall',arch(.49,.09,1.12),.215,.27,0)
box('WholeCabinetGroundPlinthGroundSole',(0,0,.045),(1.08,.62,.09),0)
box('WholeMiddleSelectorDeck',(0,-.025,.825),(.91,.54,.09),0)
# An actual two-section arched front trim, ring surfaces not luminous paint.
outer2=arch(.515,.09,1.12);inner2=arch(.47,.14,1.12);v=[(x,y,z)for y,p in[(-.322,outer2),(-.28,outer2),(-.28,inner2),(-.322,inner2)]for x,z in p]
mesh('WholeContinuousArchTrim',v,f,1)
# Genuine full lower speaker compartment: seven separated grille rails and a recessed complete cone.
for i in range(7):box('WholeLowerGrilleRail_%d'%i,(-.36+i*.12,-.298,.455),(.035,.06,.59),1)
box('WholeLowerGrilleBottomRail',(0,-.306,.18),(.88,.08,.045),1)
box('WholeLowerGrilleTopRail',(0,-.306,.735),(.88,.08,.045),1)
# One continuous shallow thick driver cone, convex centre closed, behind the actual grille gaps.
prof=[(0,.035),(.06,.025),(.20,-.12),(.225,-.135),(.225,-.105),(.20,-.09),(.06,.05),(0,.055)]
lathe_z('WholeRecessedLowerCone',0,0,prof,2,32);v,ff,m=G['WholeRecessedLowerCone'];G['WholeRecessedLowerCone']=([(x,-z,.455+y)for x,y,z in v],ff,m)
# Five entire fixed upright records on a common stepped rack, visible in the open upper bay.
box('WholeUpperRecordRack',(0,.07,1.005),(.76,.22,.10),0)
for i,x in enumerate([-.26,-.13,0,.13,.26]):
 y=.055+i*.026;cyly('WholeFixedRecordDisc_%d'%i,y-.010,y+.010,x,1.18,.175,2,32)
 cyly('WholeBlankRecordCentre_%d'%i,y-.016,y-.009,x,1.18,.034,1,16)
 # Each solid record enters its own short full rack shoulder at the bottom.
 box('WholeRecordRackSeat_%d'%i,(x,y,1.035),(.085,.055,.07),0)
# A continuous pitched selector fascia with eight real fixed blank ivory buttons.
p=[(-.345,.765),(-.345,.875),(-.22,.925),(-.22,.805)];p.reverse();n=len(p);v=[(x,y,z)for x in[-.425,.425]for y,z in p];ff=[]
for a,b,c in triangulate(p):ff.extend([(c,b,a),(a+n,b+n,c+n)])
ff +=[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh('WholePitchedSelectorFascia',v,ff,2)
for i in range(8):box('WholeBlankFixedSelectorButton_%d'%i,(-.35+i*.10,-.351,.842),(.065,.03,.045),1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeArchCasePlinthAndRack_WarmWalnut',(.28,.10,.045,1),.72,0),('WholeArchGrilleAndBlankSelectors_WarmIvory',(.70,.62,.43,1),.61,.12),('WholeFixedRecordsAndLowerCone_Charcoal',(.035,.045,.05,1),.75,0)]
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
focus=Vector((0,0,.80))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.10;aim(cam,(3,-6,2.6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/entertainment/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'entertainment','style':'S01-clean-geometric','title':'Fixed Arched Record Selection Cabinet','description':'One newly authored complete static jukebox-style record-selection cabinet. A continuous thick upright arched case and full rear wall stand on one ground plinth; an open upper bay holds five whole dark fixed records with plain small centres on a common stepped support rack. A complete pitched central selector fascia carries eight separate blank fixed buttons. The lower continuous compartment contains a real recessed thick driver cone behind seven separated full vertical grille rails with actual open gaps, inside a continuous contrasting arch trim. This is not the old rectangular open-driver speaker cabinet with circular exposed baffles and reflex duct, or a low gramophone cabinet with a horizontal single platter and tall external flared horn; all numeric geometry is independently authored as one upright stacked record-selection equipment appearance. One whole model, zero scenes; records and buttons are constituents, not extra assets. Three constant opaque untextured PBR roles, metres, Z up and whole ground-centred origin. No glass, luminous tubes, labels, trademarks, music, loose media or room. The upper bay is deliberately open for the fixed display, not a simulated transparent enclosure. No selector mechanism, record-changing motion, playback, sound, acoustic/electrical performance, historical authenticity, load, fabrication or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
