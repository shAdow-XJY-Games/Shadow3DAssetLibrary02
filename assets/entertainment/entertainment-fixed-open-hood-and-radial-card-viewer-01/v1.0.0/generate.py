import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='entertainment-fixed-open-hood-and-radial-card-viewer-01'
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



# Complete pedestal and lower enclosure; side carriers rise to a full transverse drum axle.
box('WholeGroundFootWidePedestal',(0,0,.040),(.54,.48,.080),0)
box('WholeLowerCabinet',(0,.015,.300),(.35,.30,.470),0)
box('WholeUpperCarrierDeck',(0,0,.540),(.49,.39,.065),0)
for j,x in enumerate([-.205,.205]):
 box('WholeBearingSideUpright_%d'%j,(x,.025,.675),(.052,.115,.265),0)
 axle('WholeCircularBearingBoss_%d'%j,x-.033,x+.033,.025,.840,.058,1,24)
axle('WholeContinuousCardDrumAxle',-.256,.315,.025,.840,.020,1,20)
axle('WholeCardRootCylinder',-.158,.158,.025,.840,.072,1,36)
for j,x in enumerate([-.163,.163]):ringx('WholeCardPackEndShoulder_%d'%j,x-.006,x+.006,.025,.840,.018,.083,1,32)
# Each whole thick blank card spans axially and projects radially from the complete root cylinder.
# No illustrated sequence or functional flip travel is provided.
for j in range(24):
 a=math.tau*j/24;u=(math.cos(a),math.sin(a));t=(-math.sin(a),math.cos(a));v=[]
 for q in[-.003,.003]:
  for r,x in[(.067,-.148),(.067,.148),(.244,.148),(.244,-.148)]:v.append((x,.025+r*u[0]+q*t[0],.840+r*u[1]+q*t[1]))
 mesh('WholeBlankRadialCard_%02d'%j,v,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],2)
# Intentional open front-left cutaway: rear arched housing is a full thick curved solid, not missing polygons.
v=[];f=[];N=20
for x in[-.223,.223]:
 for r in[.264,.284]:
  for j in range(N+1):
   a=math.radians(-48+155*j/N);v.append((x,.025+r*math.cos(a),.840+r*math.sin(a)))
w=N+1
for j in range(N):
 k=j+1;f +=[(j,k,w+k,w+j),(2*w+j,3*w+j,3*w+k,2*w+k),(j,2*w+j,2*w+k,k),(w+j,w+k,3*w+k,3*w+j)]
f +=[(0,w,3*w,2*w),(N,2*w+N,3*w+N,w+N)]
mesh('WholeThickRearArchedCutawayHousing',v,f,0)
# Rear housing lower ends meet a whole independent rear cross carrier rooted on the deck.
for j,x in enumerate([-.205,.205]):box('WholeRearHousingRoot_%d'%j,(x,.184,.619),(.055,.075,.145),0)
box('WholeRearHousingCrossTie',(0,.184,.665),(.455,.072,.045),0)
# Whole rectangular open viewing hood at the upper front; no opaque lens pretending a real aperture.
def hood(name,y0,y1,z0,z1,wo,ho,wi,hi):
 v=[]
 for y,z in[(y0,z0),(y1,z1)]:
  for w,h in[(wo,ho),(wi,hi)]:v +=[(-w,y,z-h),(w,y,z-h),(w,y,z+h),(-w,y,z+h)]
 f=[]
 for j in range(4):k=(j+1)%4;f +=[(j,k,4+k,4+j),(8+j,12+j,12+k,8+k),(j,8+j,8+k,k),(4+j,4+k,12+k,12+j)]
 mesh(name,v,f,3)
hood('WholeOpenFrontViewingHood',-.393,-.241,1.107,1.055,.108,.058,.088,.038)
for j,x in enumerate([-.205,.205]):
 beam('WholeFrontHoodSideStay_%d'%j,(x,.025,.844),(x,-.280,1.078),.025,1)
 beam('WholeFrontHoodCrossSeat_%d'%j,(x,-.280,1.078),(x*.46,-.280,1.078),.025,1)
beam('WholeOutboardCrank',(.306,.025,.840),(.306,-.075,.840),.020,1)
axle('WholeOutboardCrankGrip',.298,.398,-.075,.840,.025,0,16)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeCasePedestalAndHousing_DarkRed',(.23,.07,.045,1),.75,0),('WholeBearingsAxleAndCrank_DullBrass',(.47,.32,.12,1),.49,.55),('WholeBlankCards_WarmIvory',(.78,.73,.60,1),.88,0),('WholeOpenViewingHood_Charcoal',(.055,.065,.072,1),.69,.12)]
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
focus=Vector((0,0,.57))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.52;aim(cam,(4,-7,3.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/entertainment/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'entertainment','style':'S01-clean-geometric','title':'Fixed Open Hood and Radial Card Viewer','description':'One newly authored complete hand-cranked radial-card viewing-device appearance in a deliberately open-front cutaway pose. A full broad ground pedestal and lower cabinet carry two side bearing uprights, one continuous horizontal axle and a complete root cylinder with twenty-four independently thick blank radial cards. A thick curved rear housing has fully modeled cut edges rather than invisible missing polygons. Separate rooted side stays carry one true rectangular through-open viewing hood above the front of the card pack. A complete side crank and grip belong to the same axis. Unlike the old slotted vertical-axis viewing drum, there is no enclosing open-top cylinder, ring picture strip or circumferential slit field. Unlike the old pinned-cylinder music box, there is no comb, pin array or hinged case lid: the broad radial card pack and front viewing hood define this whole apparatus. All numeric geometry newly authored, no old model imported. Four opaque constant PBR roles, metre Z up and horizontal full-bounds-centred ground origin. One complete static prop zero scenes. Generic mutoscope-inspired exhibition exterior, not a historical replica: cards are intentionally blank, no film frames, verified sight line, lens optics, card-release mechanism, timed flip, motion, projected imagery, animation effect, coin operation, manufacture, load or equipment safety. Rigging animation and interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
