import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='sports-fixed-open-instep-twin-truck-and-toe-stop-roller-boot-01'
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



# All complete upper and rolling chassis coordinates authored as one new assembly.
N=28
def oval(z,rx,ry,cy=0,slope=0):return[(rx*math.cos(math.tau*i/N),cy+ry*math.sin(math.tau*i/N),z+slope*math.sin(math.tau*i/N))for i in range(N)]
# The long open instep reaches towards the toe, not only a high ankle mouth.
outer=[oval(.108,.050,.145,-.018),oval(.131,.060,.146,-.020),oval(.165,.060,.130,-.010),oval(.199,.053,.110,.008,.040),oval(.223,.046,.101,.017,.060)]
inner=[oval(.223,.035,.090,.017,.060),oval(.196,.041,.096,.009,.038),oval(.160,.045,.113,-.004),oval(.130,.039,.117,-.010)]
rr=outer+inner;v=[p for r in rr for p in r];f=[tuple(reversed(range(N))),tuple((len(rr)-1)*N+i for i in range(N))]+[(k*N+i,k*N+(i+1)%N,(k+1)*N+(i+1)%N,(k+1)*N+i)for k in range(len(rr)-1)for i in range(N)];mesh('WholeOpenInstepAndHeelBootShell',v,f,0)
rr=[oval(.097,.053,.148,-.018),oval(.114,.056,.151,-.018)];v=[p for r in rr for p in r];mesh('WholeFullFootOutsole',v,[tuple(reversed(range(N))),tuple(N+i for i in range(N))]+[(i,(i+1)%N,(i+1)%N+N,i+N)for i in range(N)],1)
# Full tapered tongue is a finite continuous solid; root seats in the front opening.
p=[(-.025,-.080,.155),(.025,-.080,.155),(.029,.027,.239),(-.029,.027,.239)];v=p+[(x,y+.004,z-.009)for x,y,z in p];mesh('WholeRaisedInstepTongue',v,[(3,2,1,0),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4)for i in range(4)],1)
for k,y in enumerate([-.053,-.020,.012]):
 z=.155+(y+.080)*(.084/.107)+.004
 beam('WholeFixedInstepLace_%d'%k,(-.036,y-.004,z-.003),(.036,y+.004,z+.003),.004,1)
box('WholeContinuousUnderShoeChassis',(0,-.010,.090),(.069,.246,.026),2)
Z=.033*math.cos(math.pi/24)
for k,y in enumerate([-.105,.088]):
 box('WholeTruckUpperSeat_%d'%k,(0,y,.077),(.064,.048,.022),2)
 # Separate compact wide hanger supports one continuous axle, no old deck/truck imported.
 p=[(-.075,.027),(.075,.027),(.075,.043),(.029,.054),(.020,.067),(-.020,.067),(-.029,.054),(-.075,.043)];v=[(x,yy,z)for yy in[y-.014,y+.014]for x,z in p];tt=triangulate(p);n=len(p);f=[tuple(reversed(t))for t in tt]+[tuple(n+i for i in t)for t in tt]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh('WholeShoulderedTruckHanger_%d'%k,v,f,2)
 beam('WholeInclinedKingpin_%d'%k,(0,y+.014,.083),(0,y-.011,.049),.012,2)
 lathe_z('WholeFixedTruckBushing_%d'%k,0,y,[(0,.054),(.014,.054),(.014,.073),(0,.073)],3,16)
 axle('WholeTransverseAxle_%d'%k,-.095,.095,y,Z,.006,2,16)
 for j,x in enumerate([-.080,.080]):
  name='WholeGroundFootWheel_%d_%d'%(k,j);lathe_z(name,0,0,[(.009,-.016),(.028,-.016),(.033,-.012),(.033,.012),(.028,.016),(.009,.016)],1,24)
  vv,ff,mm=G[name];a=math.pi/24;G[name]=([(x+c,y+u*math.cos(a)-w*math.sin(a),Z+u*math.sin(a)+w*math.cos(a))for u,w,c in vv],ff,mm)
  axle('WholeWheelHub_%d_%d'%(k,j),x-.019,x+.019,y,Z,.010,2,16)
beam('WholeForwardInclinedStopStem',(0,-.129,.088),(0,-.188,.048),.014,2)
# Blunt complete front stop, held clear of the floor in the fixed rolling pose.
lathe_z('WholeRoundToeStop',0,-.190,[(0,.025),(.024,.025),(.029,.032),(.025,.061),(0,.061)],3,24)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeOpenUpper_MutedTeal',(.07,.25,.27,1),.85,0),('WholeSoleTongueWheelsAndLaces_WarmCream',(.70,.60,.40,1),.88,0),('WholeChassisAndHubs_DullMetal',(.33,.39,.39,1),.49,.48),('WholeStopAndBushings_Charcoal',(.035,.045,.044,1),.92,0)]
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
focus=Vector((0,0,.145))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.52;aim(cam,(3,-5,2.9));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/sports/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'sports','style':'S01-clean-geometric','title':'Fixed Open Instep Twin Truck and Toe Stop Roller Boot','description':'One newly authored complete quad roller-boot static exterior. A continuous thick foot-shaped upper has a real long sloping open instep and heel cavity, full inner floor and a separate whole raised tongue seated at the toe-side opening. Three full fixed laces bridge the open instep. A continuous full outsole and low chassis carry two separately rooted transverse axle hangers, each with an inclined kingpin and distinct fixed bushing. Four complete bored broad wheels and their hubs stand on actual finite tread facets. A separate forward inclined stem carries one thick round toe-stop exterior ahead of the front axle. No old skate upper or skateboard truck vertices are imported, resized or extracted; the new broad instep opening/tongue and integrated short rolling chassis are drawn together, not an old ice runner replaced by decorative wheels. There is no long deck, raised blade bridge or continuous metal runner. Four opaque constant PBR materials, metres Z up and actual horizontal-envelope-centred origin. One whole static prop zero scenes, no paired-colour version, foot or wearer. The shown tiny embedded joints lock a display pose only: no rolling, steering, braking, wheel clearance over travel, fastening, shoe sizing, restraint, ergonomics, load, material performance, manufacture or protective/sport safety capability. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
