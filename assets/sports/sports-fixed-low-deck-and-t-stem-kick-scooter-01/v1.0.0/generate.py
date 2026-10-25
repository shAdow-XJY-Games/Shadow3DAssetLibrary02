import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='sports-fixed-low-deck-and-t-stem-kick-scooter-01'
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



# Closed complete deck, paired rear prongs and rising forward neck.
def union_boxes(name,boxes,mat):
 xs=sorted(set(v[0]for b in boxes for v in b));ys=sorted(set(v[1]for b in boxes for v in b));zs=sorted(set(v[2]for b in boxes for v in b));faces={}
 for i in range(len(xs)-1):
  for j in range(len(ys)-1):
   for k in range(len(zs)-1):
    c=((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)
    if not any(all(lo[t]<c[t]<hi[t]for t in range(3))for lo,hi in boxes):continue
    v=[(x,y,z)for z in[zs[k],zs[k+1]]for y in[ys[j],ys[j+1]]for x in[xs[i],xs[i+1]]]
    for f in BOX:
     q=tuple(v[t]for t in f);key=tuple(sorted(q))
     if key in faces:del faces[key]
     else:faces[key]=q
 v=[];ix={};f=[]
 for q in faces.values():
  ids=[]
  for p in q:
   if p not in ix:ix[p]=len(v);v.append(p)
   ids.append(ix[p])
  f.append(ids)
 mesh(name,v,f,mat)
union_boxes('WholeNarrowDeckAndRearForkProngs',[( (-.065,-.32,.072),(.065,.29,.105)),((-.062,.265,.073),(-.025,.42,.105)),((.025,.265,.073),(.062,.42,.105))],0)
box('WholeGripSurface',(0,-.015,.107),(.112,.53,.008),2)
p=[(-.32,.072),(-.32,.105),(-.392,.240),(-.447,.240),(-.447,.205),(-.417,.205)]
if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(p,p[1:]+p[:1]))<0:p.reverse()
n=len(p);v=[(x,y,z)for x in[-.038,.038]for y,z in p];f=[]
for a,b,c in triangulate(p):f.extend([(c,b,a),(a+n,b+n,c+n)])
f +=[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh('WholeRisingFrontDeckNeck',v,f,0)
lathe_z('WholeAnnularSteeringHead',0,-.43,[(.018,.195),(.031,.195),(.031,.292),(.018,.292)],0,24)
lathe_z('WholeFixedLongSteeringStem',0,-.43,[(0,.155),(.016,.155),(.016,.932),(0,.932)],1,16)
lathe_z('WholeAnnularHeadClamp',0,-.43,[(.016,.283),(.034,.283),(.034,.308),(.016,.308)],1,24)
box('WholeFrontForkCrown',(0,-.43,.175),(.085,.044,.030),1)
for x,label in[(-.034,'Left'),(.034,'Right')]:box(label+'WholeFrontForkLeg',(x,-.43,.128),(.020,.030,.095),1)
# Original new small wheel geometry, flat true tread facets at Z=0.
Z=.088*math.cos(math.pi/24)
for label,y in [('Front',-.43),('Rear',.40)]:
 name=label+'WholeGroundFootAnnularTire';lathe_z(name,0,0,[(.027,-.014),(.078,-.014),(.088,-.010),(.088,.010),(.078,.014),(.027,.014)],2,24)
 vv,ff,mm=G[name];a=math.pi/24;G[name]=([(w,y+x*math.cos(a)-z*math.sin(a),Z+x*math.sin(a)+z*math.cos(a))for x,z,w in vv],ff,mm)
 axle(label+'WholeHub',-.019,.019,y,Z,.030,1,20);axle(label+'WholeAxle',-.065,.065,y,Z,.007,1,12)
axle('WholeTBar',-.25,.25,-.43,.932,.014,1,16)
for side,x0,x1 in [('Left',-.264,-.155),('Right',.155,.264)]:axle(side+'WholeHandleGrip',x0,x1,-.43,.932,.021,2,16)
# Complete raised curved brake plate over rear wheel, finite gap not a wheel intersection.
p=[(.40+.105*math.cos(a),Z+.105*math.sin(a))for a in[.25+i*(2.65-.25)/12 for i in range(13)]]
p +=[(.40+.114*math.cos(a),Z+.114*math.sin(a))for a in reversed([.25+i*(2.65-.25)/12 for i in range(13)])]
if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(p,p[1:]+p[:1]))<0:p.reverse()
n=len(p);v=[(x,y,z)for x in[-.025,.025]for y,z in p];f=[]
for a,b,c in triangulate(p):f.extend([(c,b,a),(a+n,b+n,c+n)])
f +=[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh('WholeCurvedRearFenderBrakePlate',v,f,0)
union_boxes('WholeForkedBrakeRootSeat',[((-.045,.275,.095),(.045,.305,.150)),((-.045,.300,.095),(-.020,.332,.155)),((.020,.300,.095),(.045,.332,.155))],1)
beam('WholeDeployedStand',(-.035,.12,.078),(-.125,.16,.011),.014,1)
box('WholeGroundFootStandPad',(-.125,.16,.006),(.045,.038,.012),2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeDeckAndNeck_MutedBlue',(.075,.23,.31,1),.65,.20),('WholeStemsAndHubs_SatinMetal',(.38,.43,.45,1),.47,.60),('WholeTiresGripsPad_Charcoal',(.055,.062,.065,1),.87,0)]
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
focus=Vector((0,0,.48))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.40;aim(cam,(4,-6,3.4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/sports/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'sports','style':'S01-clean-geometric','title':'Fixed Low Deck and T Stem Kick Scooter','description':'One newly authored complete static unpowered kick-scooter exterior. A low long narrow foot deck continues into two integral rear axle prongs around a small rear wheel and a rising front neck that seats a real open cylindrical steering head. A long thin T mast, separate front fork crown and paired legs, two full annular small tires with hubs/axles, two thick handle grips, a complete curved rear fender-brake appearance, and a deployed narrow stand form one integrated whole vehicle. The head tube retains a real annular opening around its narrower fixed stem. No old electric step-through body is stripped: all geometry is new, with no saddle, broad leg shield or motor housing. Unlike the old skateboard there are no transverse paired-wheel trucks or double-kick concave deck. Three opaque untextured PBR roles, metres, ground-centred envelope, one prop and zero scenes. Fixed display only; no steering, braking, folding, riding suitability, load, road compliance, material or safety performance claim. Rigging, animation and interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
