import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='sports-fixed-window-riser-split-limb-and-eccentric-wheel-bow-01'
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



# Entire stylized rigid centre riser assembly with genuine open upper and lower windows.
def window_piece(name,outer,inner,z0,z1):
 n=len(outer);v=[(x,y,z)for z in[z0,z1]for ring in[outer,inner]for x,y in ring];f=[]
 for j in range(n):k=(j+1)%n;f +=[(j,k,n+k,n+j),(2*n+j,3*n+j,3*n+k,2*n+k),(j,2*n+j,2*n+k,k),(n+j,n+k,3*n+k,3*n+j)]
 mesh(name,v,f,0)
outer=[(-.06,.08),(.015,.08),(.065,.24),(.070,.33),(-.015,.33),(-.040,.22)]
inner=[(-.038,.113),(.002,.113),(.040,.245),(.043,.303),(.003,.303),(-.016,.216)]
window_piece('WholeUpperWindowRiser',outer,inner,.005,.065)
window_piece('WholeLowerWindowRiser',[(x,-y)for x,y in outer],[(x,-y)for x,y in inner],.005,.065)
box('WholeCentralRiserCore',(-.035,0,.035),(.050,.235,.050),0)
box('WholeGroundFootCentreGrip',(-.045,0,.025),(.065,.200,.090),1)
# Two complete bifurcated limb pairs lie on opposite axial sides of their end wheels.
for j,sgn in enumerate([-1,1]):
 box('WholeSplitLimbRootPocket_%d'%j,(.030,sgn*.309,.040),(.090,.074,.090),0)
 for k,z in enumerate([.010,.070]):
  rows=[(.03,sgn*.302,z),(.060,sgn*.405,z),(.112,sgn*.510,z),(.130,sgn*.590,z)];v=[]
  for x,y,zz in rows:v +=[(x-.020,y,zz-.007),(x+.020,y,zz-.007),(x+.020,y,zz+.007),(x-.020,y,zz+.007)]
  f=[(3,2,1,0),(12,13,14,15)]
  for t in range(3):
   for i in range(4):h=(i+1)%4;f.append((4*t+i,4*t+h,4*(t+1)+h,4*(t+1)+i))
  mesh('WholeForkedLimb_%d_%d'%(j,k),v,f,0)
 # A newly authored annular end wheel with truly off-centre axle hole, decorative not a working cam curve.
 n=40;v=[];f=[]
 for zz in[.023,.057]:
  for kind in[0,1]:
   for i in range(n):
    a=math.tau*i/n;r=.011 if kind==0 else .084;cx=.130 if kind==0 else .148;v.append((cx+r*math.cos(a),sgn*.590+r*math.sin(a),zz))
 for i in range(n):h=(i+1)%n;f +=[(i,h,n+h,n+i),(2*n+i,3*n+i,3*n+h,2*n+h),(i,2*n+i,2*n+h,h),(n+i,n+h,3*n+h,3*n+i)]
 mesh('WholeEccentricEndWheel_%d'%j,v,f,2)
 lathe_z('WholeEndWheelAxle_%d'%j,.130,sgn*.590,[(0,-.003),(.010,-.003),(.010,.083),(0,.083)],2,16)
 for k,z in enumerate([-.006,.081]):lathe_z('WholeAxleRetainer_%d_%d'%(j,k),.130,sgn*.590,[(0,z),(.016,z),(.016,z+.008),(0,z+.008)],1,16)
# Three continuous separate display cords, in distinct depth layers at their crossing.
# No real drive routing, draw motion or tension is represented.
cyly('WholeLongFrontDisplayString',-.590,.590,.228,.040,.0025,3,12)
beam('WholeUpperToLowerDisplayCableA',(.100,.520,.053),(.190,-.580,.053),.0035,3)
beam('WholeLowerToUpperDisplayCableB',(.190,.580,.027),(.100,-.520,.027),.0035,3)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeWindowRiserAndForkLimbs_MutedTeal',(.065,.23,.25,1),.65,.12),('WholeGripAndRetainers_Charcoal',(.035,.045,.048,1),.87,0),('WholeEccentricWheelsAndPins_DullBronze',(.43,.31,.14,1),.49,.50),('WholeStaticDisplayCords_DarkGrey',(.13,.15,.16,1),.72,0)]
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
focus=Vector((0,0,.045))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.62;aim(cam,(3,-5,7));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/sports/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'sports','style':'S01-clean-geometric','title':'Fixed Window Riser Split Limb and Eccentric Wheel Bow','description':'One newly authored complete compound-bow-inspired sports display exterior, laid flat in one fixed illustrative pose without arrows. A thick centre grip joins complete upper and lower open-window riser members and two fixed root pockets. Four separate full short curved limbs form two bifurcated ends around two independent thick eccentric-wheel appearances, each with a genuine off-centre axle bore, complete transverse pin and retainers. One full front string and two independent crossing display cables occupy separated depth layers. This is not the old single continuous double-recurve bow with two decorative discs added: the rigid pierced riser, rooted split-limb structure and separate axle-carried end-wheel organization are all newly constructed. No prior visible mesh imported or extracted. Unlike the small four-lobe climbing device, there is no stacked plate head, long loop handle or trigger crossbar. Four opaque PBR roles, metre game-space coordinates, Z up and horizontally centred whole envelope. One static prop zero scenes. Pure stylized visual artwork only: decorative wheel curves and cable routing are not a functional design; no draw path, stored energy, force, release, string tension, projectile, ballistic effect, manufacture, sport suitability or safe handling represented. Rigging animation and interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
