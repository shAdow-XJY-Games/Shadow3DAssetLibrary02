import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='photography-fixed-open-slot-case-and-tripod-roll-screen-01'
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



def full_prism(name,p,a,b,axis,mat):
 if sum(u[0]*v[1]-u[1]*v[0]for u,v in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 def pt(q,t):return(q[0],q[1],t)if axis=='z'else(t,q[0],q[1])if axis=='x'else(q[0],t,q[1])
 n=len(p);tt=triangulate(p);mesh(name,[pt(q,t)for t in[a,b]for q in p],[tuple(reversed(t))for t in tt]+[tuple(n+i for i in t)for t in tt]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],mat)
for j,a in enumerate([-math.pi/2,math.pi/6,5*math.pi/6]):
 x=.46*math.cos(a);y=.095+.46*math.sin(a)
 box('WholeGroundFootShoe_%d'%j,(x,y,.019),(.100,.110,.038),2)
 beam('WholeSplayedTripodLeg_%d'%j,(x,y,.031),(0,.095,.335),.037,0)
 beam('WholeFixedLowerStay_%d'%j,(x*.66,.095+(y-.095)*.66,.135),(0,.095,.210),.018,0)
lathe_z('WholeLowerMastCollar',0,.095,[(0,.188),(.047,.188),(.047,.362),(0,.362)],2,24)
lathe_z('WholeRearOuterMast',0,.095,[(0,.315),(.026,.315),(.026,1.34),(.018,1.34),(.018,.315)],0,24)
lathe_z('WholeFixedRaisedInnerMast',0,.095,[(0,1.20),(.017,1.20),(.017,1.956),(0,1.956)],0,24)
lathe_z('WholeMastClampingCollar',0,.095,[(0,1.296),(.032,1.296),(.032,1.345),(0,1.345)],2,24)
axle('WholeBlankClampKnob',.024,.062,.095,1.322,.018,3,20)
box('WholeCaseToMastBracket',(0,.056,.835),(.105,.110,.072),0)
# Single continuous thick C-section shell, extruded whole width; the opening is real.
n=40;a0=math.pi/2+.22;a1=math.pi/2+math.tau-.22
p=[(.057*math.cos(a0+(a1-a0)*i/n),.835+.057*math.sin(a0+(a1-a0)*i/n))for i in range(n+1)]+[(.047*math.cos(a0+(a1-a0)*i/n),.835+.047*math.sin(a0+(a1-a0)*i/n))for i in reversed(range(n+1))]
full_prism('WholeContinuousSlottedRollCase',p,-.780,.780,'x',2)
for j,x in enumerate([-.793,.777]):axle('WholeProudCaseEndCap_%d'%j,x,x+.016,0,.835,.060,0,32)
# One closed thin sheet with shared-edge border regions, no surface overlays.
xs=[-.720,-.690,.690,.720];zs=[.870,.907,1.898,1.932];v=[(x,y,z)for y in[-.004,.004]for z in zs for x in xs];f=[];fm=[]
for k in range(2):
 for iz in range(3):
  for ix in range(3):
   q=[k*16+iz*4+ix,k*16+iz*4+ix+1,k*16+(iz+1)*4+ix+1,k*16+(iz+1)*4+ix]
   f.append(q if k==0 else list(reversed(q)));fm.append(1 if iz==ix==1 else 2)
for ix in range(3):f.extend([(ix,16+ix,17+ix,ix+1),(12+ix,13+ix,29+ix,28+ix)]);fm.extend([2,2])
for iz in range(3):f.extend([(iz*4,(iz+1)*4,16+(iz+1)*4,16+iz*4),(iz*4+3,16+iz*4+3,16+(iz+1)*4+3,(iz+1)*4+3)]);fm.extend([2,2])
mesh('WholeBlankScreenWithIntegralBorder',v,f,1);FM['WholeBlankScreenWithIntegralBorder']=[m for m in fm for _ in range(2)]
box('WholeTopRetainingRail',(0,0,1.937),(1.50,.025,.026),2)
full_prism('WholeForwardTopSupportHook',[(.109,1.947),(-.018,1.947),(-.018,1.923),(-.031,1.923),(-.031,1.962),(.109,1.962)],-.015,.015,'x',0)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeMastAndFeet_SatinGrey',(.41,.46,.44,1),.57,.40),('WholeBlankSheet_WarmIvory',(.79,.77,.67,1),.92,0),('WholeCaseBorderAndCaps_Charcoal',(.035,.042,.042,1),.82,.05),('WholeBlankKnob_MutedBlue',(.10,.23,.27,1),.72,.10)]
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
focus=Vector((0,0,1.0))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.65;aim(cam,(3,-6,3.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/photography/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'photography','style':'S01-clean-geometric','title':'Fixed Open Slot Case and Tripod Roll Screen','description':'One newly authored complete fixed-expanded portable roll-screen exterior. Three whole splayed legs and separate finite shoes meet one central collar and a tall rear tubular mast, with three lower fixed stays. A narrow inner upper mast reaches a short forward hook supporting a whole top rail. A complete wide horizontal cylindrical case is rooted on the lower mast; its single thick C-section shell has a true continuous long upward slot and independent proud end caps. One uninterrupted thin opaque blank screen rises from inside that slot to the top rail. Its dark border and cream centre are face materials on one shared-vertex closed sheet, not duplicate coplanar overlays. No blackboard slab, panel-lift, easel, projector or old frame meshes reused. Unlike two-legged thick teaching boards this has a thin deployed sheet between lower slot case and upper rail on a rear tripod mast; unlike a wheeled lifting cradle it has no winch, wheels or tilting H carrier. Three finite ground shoes; four solid opaque PBR roles, metres Z up, complete bounds-centred horizontal origin; one prop zero scenes. Fixed appearance only: no retracting, winding, spring or tension mechanism, telescoping travel, projection optics, reflective performance, load, installation, stability or safety claim. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
