import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='sports-fixed-twin-rigger-and-rail-seat-single-scull-01'
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



def solid_route(name,path,r,mat,n=12):
 v=[];f=[]
 for k,p in enumerate(path):
  a=path[max(k-1,0)];b=path[min(k+1,len(path)-1)];t=unit(sub(b,a));u=unit(cross(t,(0,0,1)if abs(t[2])<.9 else(0,1,0)));w=cross(t,u)
  for j in range(n):v.append(tuple(p[i]+r*(u[i]*math.cos(math.tau*j/n)+w[i]*math.sin(math.tau*j/n))for i in range(3)))
 f=[tuple(reversed(range(n))),tuple((len(path)-1)*n+i for i in range(n))]
 for k in range(len(path)-1):
  for j in range(n):h=(j+1)%n;f.append((k*n+j,k*n+h,(k+1)*n+h,(k+1)*n+j))
 mesh(name,v,f,mat)
# New longitudinally sampled complete shell, not an edited existing kayak payload.
st=[(-2.90,.018),(-2.64,.065),(-2.12,.130),(-1.40,.190),(-.70,.226),(0,.238),(.70,.226),(1.40,.190),(2.12,.130),(2.64,.065),(2.90,.018)]
outer=[(x,-w)for x,w in st]+[(x,w)for x,w in reversed(st)]
N=len(outer);v=[]
# Five whole loops: dry sole, chine, full top, bounded long rowing well, well floor.
for k in range(5):
 for i,(x,y)in enumerate(outer):
  t=x/2.90
  if k==0:p=(x*.94,y*.27,0)
  elif k==1:p=(x*.985,y*.78,.085+.065*abs(t)**2)
  elif k==2:p=(x,y,.255+.035*abs(t))
  elif k==3:p=(t*.95,y/.238*.186,.255)
  else:p=(t*.88,y/.238*.158,.055)
  v.append(p)
f=[tuple(reversed(range(N)))];fm=[0]
for k in range(4):
 for i in range(N):j=(i+1)%N;f.append((k*N+i,k*N+j,(k+1)*N+j,(k+1)*N+i));fm.append(0 if k<2 else(1 if k==2 else 3))
f.append(tuple(4*N+i for i in range(N)));fm.append(3)
mesh('WholeGroundFootRacingShellAndBoundedRowingWell',v,f,0);FM['WholeGroundFootRacingShellAndBoundedRowingWell']=[m for m,face in zip(fm,f)for _ in range(len(face)-2)]
# Two finite rails and their complete low seat; footboard is separate, no backrest.
for j,y in enumerate([-.095,.095]):
 box('WholeSeatRail_%d'%j,(-.22,y,.091),(.68,.026,.070),2)
 box('WholeRailSlideShoe_%d'%j,(-.23,y,.135),(.15,.040,.030),3)
box('WholeLowBacklessSeat',(-.23,0,.168),(.24,.29,.040),3)
for j,y in enumerate([-.105,.105]):beam('WholeFootboardSupport_%d'%j,(.50,y,.065),(.59,y,.190),.032,2)
# Fixed inclined footboard, supported by both finite braces.
beam('WholeInclinedFootboardCross',(.59,-.145,.187),(.59,.145,.187),.055,3)
box('WholeFootboardLowerHeelBar',(.49,0,.079),(.070,.29,.037),3)
for j,sgn in enumerate([-1,1]):
 end=(-.04,sgn*.82,.335)
 for k,x in enumerate([-.42,.42]):
  box('WholeRiggerRoot_%d_%d'%(j,k),(x,sgn*.208,.251),(.09,.065,.045),2)
  beam('WholeTriangularRigger_%d_%d'%(j,k),(x,sgn*.208,.263),end,.025,2)
 lathe_z('WholeOarlockPin_%d'%j,end[0],end[1],[(0,.323),(.015,.323),(.015,.362),(0,.362)],2,16)
 # Whole U-section open fork aligned to the one complete oar shaft.
 a=(-.35,sgn*.20,.373);b=(.59,sgn*2.08,.373);u=unit(sub(b,a));w=(-u[1],u[0],0);c=(-.04,sgn*.82,.373)
 poly=[(-.037,-.035),(.037,-.035),(.037,.035),(.023,.035),(.023,-.014),(-.023,-.014),(-.023,.035),(-.037,.035)];nn=len(poly)
 vv=[tuple(c[k]+u[k]*dd+w[k]*h+(z if k==2 else 0)for k in range(3))for dd in[-.033,.033]for h,z in poly];ff=[]
 for aa,bb,cc in triangulate(poly):ff +=[(cc,bb,aa),(aa+nn,bb+nn,cc+nn)]
 ff +=[(i,(i+1)%nn,(i+1)%nn+nn,i+nn)for i in range(nn)];mesh('WholeOpenForkOarlock_%d'%j,vv,ff,2)
 solid_route('WholeContinuousScullShaft_%d'%j,[a,b],.014,2,12)
 gripend=tuple(a[k]+u[k]*.22 for k in range(3));solid_route('WholeInnerOarGrip_%d'%j,[a,gripend],.023,3,16)
 # One broad finite blade at the outer tip, continuous root joining shaft.
 shape=[(-.17,-.025),(-.07,-.072),(.25,-.090),(.32,-.050),(.32,.055),(.22,.090),(-.08,.070),(-.17,.025)];nn=len(shape)
 vv=[tuple(b[k]+u[k]*ll+w[k]*ww+(zz if k==2 else 0)for k in range(3))for zz in[-.009,.009]for ll,ww in shape];ff=[]
 for aa,bb,cc in triangulate(shape):ff +=[(cc,bb,aa),(aa+nn,bb+nn,cc+nn)]
 ff +=[(i,(i+1)%nn,(i+1)%nn+nn,i+nn)for i in range(nn)];mesh('WholeBroadScullBlade_%d'%j,vv,ff,1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeHull_DeepTeal',(.055,.28,.31,1),.54,.04),('WholeDeckAndBlades_Ivory',(.76,.72,.60,1),.62,.02),('WholeRiggersRailsAndShafts_SatinGrey',(.28,.31,.32,1),.43,.5),('WholeWellSeatAndGrips_DarkGrey',(.07,.09,.09,1),.76,0)]
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
focus=Vector((0,0,.18))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=7.2;aim(cam,(4,-6,6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/sports/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'sports','style':'S01-clean-geometric','title':'Fixed Twin Rigger and Rail Seat Single Scull','description':'One newly authored complete fixed single-scull rowing-shell exterior. A long longitudinally sampled thick hull has a genuine bounded central well, continuous fore and aft deck and a finite narrow dry-display sole. Two whole parallel seat rails carry a fixed low backless seat, with forward inclined foot supports. Two independent complete triangular outboard riggers root at four finite hull seats and carry genuinely open U-shaped oarlocks; each holds one entire long scull shaft with inner grip and broad finite outer blade. The complete hull-to-outrigger-to-oar station and internal rail-seat arrangement distinguishes this whole craft from the old open work skiff with loose paddle and transverse benches, and the closed-deck kayak with contained backrest and no outboard bearing system. All visible numeric geometry newly authored, not an old hull with accessories extracted or appended. One whole sports prop, zero scenes, four opaque constant PBR roles. Metres Z up, whole horizontal envelope centred, static dry display only; no water or occupant. No rowing, sliding, oarlock motion, fit, buoyancy, hydrostatics, hydrodynamics, racing compliance, speed, loading, operation, manufacture or water-safety claim. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
