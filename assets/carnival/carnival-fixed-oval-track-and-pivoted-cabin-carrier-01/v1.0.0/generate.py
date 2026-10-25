import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='carnival-fixed-oval-track-and-pivoted-cabin-carrier-01'
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



# Entire new long-carrier/end-wheel/straight-run amusement structure.
Z=2.70;LOW=1.30;HIGH=4.10
for side,y in [('Front',-1.10),('Rear',1.10)]:
 for k,x in enumerate([-1.02,1.02]):
  box(side+'WholeGroundFoot_'+str(k),(x,y,.065),(.42,.42,.13),0)
  beam(side+'WholeRakingCarrierSupport_'+str(k),(x,y,.11),(0,y,Z),.18,0)
 box(side+'WholeLowFrameTie',(0,y,.22),(2.10,.13,.15),0)
 ringy(side+'WholeCentralAxleBearing',y-.115,y+.115,0,Z,.092,.23,3,24)
for x in[-1.02,1.02]:box('WholeFootCrossTie_'+str(x),(x,0,.18),(.14,2.31,.14),0)
cyly('WholeContinuousCentralAxle',-1.27,1.27,0,Z,.094,3,24)
box('WholeLongRigidCarrierSpine',(0,0,Z),(.19,.29,2.93),1)
for j,z in enumerate([LOW,HIGH]):
 cyly('WholeSeparateEndWheelShaft_'+str(j),-.31,.31,0,z,.075,3,20)
 ringy('WholeOpenEndWheelRim_'+str(j),-.135,.135,0,z,.51,.585,1,48)
 ringy('WholeEndWheelHub_'+str(j),-.145,.145,0,z,.074,.15,3,20)
 for k in range(4):
  a=math.pi/4+math.tau*k/4;beam('WholeEndWheelSpoke_%d_%d'%(j,k),(.13*math.cos(a),0,z+.13*math.sin(a)),(.55*math.cos(a),0,z+.55*math.sin(a)),.075,1)
# Complete annular stadium guide bands; long straight sides are not ellipse segments.
def stadium(r):
 return [(r*math.cos(math.pi*i/24),HIGH+r*math.sin(math.pi*i/24))for i in range(25)]+[(r*math.cos(math.pi+math.pi*i/24),LOW+r*math.sin(math.pi+math.pi*i/24))for i in range(25)]
for j,y in enumerate([-.225,.225]):
 o=stadium(.64);a=stadium(.58);n=len(o);v=[(x,yy,z)for yy,p in[(y-.035,o),(y+.035,o),(y-.035,a),(y+.035,a)]for x,z in p];f=[]
 for i in range(n):
  q=(i+1)%n;f.extend([(i,q,n+q,n+i),(2*n+i,3*n+i,3*n+q,2*n+q),(i,2*n+i,2*n+q,q),(n+i,n+q,3*n+q,3*n+i)])
 mesh('WholeClosedStraightRunGuideBand_'+str(j),v,f,1)
# Eight full level framed cages pivot independently off the track positions in this static pose.
positions=[(0,4.70),(.61,3.65),(.61,2.70),(.61,1.75),(0,.70),(-.61,1.75),(-.61,2.70),(-.61,3.65)]
for k,(x,z)in enumerate(positions):
 cyly('Cabin%02d_WholeTrackPivot'%k,-.355,.94,x,z,.028,3,16)
 b=z-.37;v=[]
 for hx,hy,zz in[(.235,.315,b),(.235,.315,b+.13),(.205,.285,b+.13),(.205,.285,b+.035)]:v.extend([(x-hx,-hy,zz),(x+hx,-hy,zz),(x+hx,hy,zz),(x-hx,hy,zz)])
 f=[(3,2,1,0),(12,13,14,15)]
 for a,c in[(0,4),(4,8),(8,12)]:
  for i in range(4):q=(i+1)%4;f.append((a+i,a+q,c+q,c+i))
 mesh('Cabin%02d_WholeOpenLowPan'%k,v,f,2)
 for corner,(dx,y)in enumerate([(-.217,-.297),(.217,-.297),(-.217,.297),(.217,.297)]):beam('Cabin%02d_WholeCornerPost_%d'%(k,corner),(x+dx,y,b+.085),(x+dx,y,b+.57),.033,0)
 box('Cabin%02d_WholeRoof'%k,(x,0,b+.58),(.49,.66,.045),2)
 box('Cabin%02d_WholeFrontFixedCrossbar'%k,(x,-.296,b+.29),(.45,.028,.035),0)
 # Full short pivot cheeks connect each side pivot directly to the rear/front cage frame.
 for sy in[-1,1]:
  box('Cabin%02d_WholePivotCheek_%d'%(k,sy),(x,sy*.299,z),(.45,.040,.065),0)
 box('Cabin%02d_WholeSeatPad'%k,(x,.13,b+.082),(.37,.24,.105),3)
# All complete cages are forward of both track planes; only their long pivot shafts return to the tracks.
for name,(vv,ff,mm) in list(G.items()):
 if name.startswith('Cabin'):G[name]=([(x,y-.65,z)for x,y,z in vv],ff,mm)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(.75*(p[k]-SHIFT[k])for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeFramesAndCagePosts_DeepTeal',(.055,.20,.22,1),.68,.12),('WholeSpineGuideBandsAndEndWheels_WarmIvory',(.72,.65,.45,1),.61,.20),('WholeCabinPansAndRoofs_MutedOrange',(.60,.21,.075,1),.72,.05),('WholeShaftsCheeksAndPads_DarkAlloy',(.13,.17,.18,1),.57,.35)]
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
focus=Vector((0,0,1.80))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=4.575;aim(cam,(5,-9,5.0));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/carnival/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'carnival','style':'S01-clean-geometric','title':'Fixed Oval Track and Pivoted Cabin Carrier','description':'One newly authored complete static oval-track amusement-carrier exterior. Two grounded whole A-frames and low cross-ties support a full central horizontal axle. The axle enters a long rigid vertical spine carrying separate upper and lower end-wheel shafts. Two whole stadium-shaped guide bands consist of actual straight long sides joined to semicircular ends; two independent open end wheels with complete spokes and hubs lie inside those return ends. Eight whole empty framed cabins have their own transverse track pivots, low thick open pans, four posts, roofs and front crossbars. This is not a circular Ferris wheel scaled into an ellipse: there is no central radial-spoke wheel or single circular rim; two separate end-wheel centres, a continuous long carrier spine and straight guide runs establish a different complete structure. Nor is it a twin-arm ride with one transverse passenger tray. All new numeric geometry, no old frame, wheel or cabin extracted or transformed. One complete compact display model at explicit 0.75 design scale, zero scenes, four opaque PBR appearances, metres Z up, horizontal bounds-centred and four finite full feet on ground. Empty fixed exhibition pose only. Guide bands are solid visual track members, not an articulated or validated chain. No movement, rolling engagement, passenger restraint, capacity, fit, loading, manufacture, ride operation or safety is built or certified; no rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
