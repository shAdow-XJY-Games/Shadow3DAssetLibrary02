import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='music-fixed-cranked-pin-barrel-and-pipe-chest-street-organ-01'
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



# Entire newly drawn compact street-organ cabinet with barrel, followers and pipe chest.
box('WholeUnderframeBase',(0,0,.255),(.94,.64,.060),0)
for k,s in enumerate([-1,1]):
 box('WholeGroundFootFront_%d'%k,(s*.36,-.23,.045),(.13,.14,.09),3)
 box('WholeFrontShortLeg_%d'%k,(s*.36,-.23,.15),(.075,.075,.17),0)
 box('WholeRearAxleCarrier_%d'%k,(s*.37,.21,.18),(.07,.09,.15),0)
# Rear full wheels have flat lower polygon facets, no point-ground promise.
axle('WholeRearWheelAxle',-.53,.53,.21,.128*math.cos(math.pi/16),.018,2,16)
for k,s in enumerate([-1,1]):
 cx=s*.49;cz=.128*math.cos(math.pi/16)
 ringx('WholeGroundFootRearWheel_%d'%k,cx-.027,cx+.027,.21,cz,.095,.128,3,16)
 v,f,m=G['WholeGroundFootRearWheel_%d'%k];co=math.cos(math.pi/16);si=math.sin(math.pi/16);G['WholeGroundFootRearWheel_%d'%k]=([(x,.21+(y-.21)*co-(z-cz)*si,cz+(y-.21)*si+(z-cz)*co)for x,y,z in v],f,m)
 axle('WholeWheelHub_%d'%k,cx-.033,cx+.033,.21,cz,.037,2,16)
 for j in range(6):
  t=math.tau*j/6;beam('WholeWheelSpoke_%d_%d'%(k,j),(cx,.21,cz),(cx,.21+.102*math.cos(t),cz+.102*math.sin(t)),.018,0)
# Cabinet cheeks and back are separate whole boards, outer corners deliberately staggered.
for k,s in enumerate([-1,1]):box('WholeCabinetCheek_%d'%k,(s*.423,0,.760),(.054,.55,.98),0)
box('WholeRearCabinetWall',(0,.267,.755),(.80,.035,.96),0)
box('WholeTopCornice',(0,0,1.270),(.94,.62,.06),0)
box('WholePipeChest',(0,0,.855),(.82,.50,.075),0)
# Whole lower pleated bellows shell appearance, fixed compressed pose.
vv=[];fs=[]
for k in range(7):
 z=.295+k*.022;rx=.30+(.023 if k%2 else 0);ry=.18+(.018 if k%2 else 0)
 for x,y in[(-rx,-ry),(rx,-ry),(rx,ry),(-rx,ry)]:vv.append((x,y,z))
fs=[(3,2,1,0),(24,25,26,27)]
for k in range(6):
 for j in range(4):q=(j+1)%4;fs.append((4*k+j,4*k+q,4*(k+1)+q,4*(k+1)+j))
mesh('WholeFixedPleatedLowerBellows',vv,fs,3)
box('WholeBellowsUpperPlate',(0,0,.438),(.68,.43,.035),0)
for k,s in enumerate([-1,1]):box('WholeBarrelBearing_%d'%k,(s*.342,-.025,.555),(.055,.10,.23),2)
axle('WholePinnedBarrelAxle',-.39,.53,-.025,.620,.017,2,20)
axle('WholeWoodenPinBarrel',-.29,.29,-.025,.620,.118,0,32)
for i in range(7):
 x=(i-3)*.075
 for j in range(3):
  t=.35+i*.41+j*1.42;beam('WholeBluntBarrelPeg_%d_%d'%(i,j),(x,-.025+.114*math.cos(t),.620+.114*math.sin(t)),(x,-.025+.131*math.cos(t),.620+.131*math.sin(t)),.009,2)
# Complete independent follower rods share a visible supported rear shaft, not a comb block.
axle('WholeFollowerSupportShaft',-.36,.36,.135,.765,.013,2,20)
for k,s in enumerate([-1,1]):box('WholeFollowerShaftRoot_%d'%k,(s*.342,.135,.790),(.05,.05,.09),0)
for i in range(7):beam('WholeFixedFollowerRod_%d'%i,((i-3)*.075,-.075,.751),((i-3)*.075,.17,.765),.014,2)
beam('WholeSideCrank',(.518,-.025,.620),(.518,-.025,.770),.026,2)
axle('WholeCrankGrip',.51,.63,-.025,.770,.023,0,16)
# Complete new open-top pipes with real short front mouth slots above the chest.
N=16
for k,h in enumerate([1.08,1.14,1.19,1.235,1.19,1.14,1.08]):
 x=(k-3)*.105;y=-.105;ro=.040;ri=.033;zs=[.882,.925,.956,h];v=[]
 for rr in[ro,ri]:
  for z in zs:
   for j in range(N):v.append((x+rr*math.cos(math.tau*j/N),y+rr*math.sin(math.tau*j/N),z))
 f=[];off=4*N
 cells={(a,j)for a in range(3)for j in range(N)}-{(1,11),(1,12)}
 for a,j in cells:
  q=(j+1)%N;ids=[a*N+j,a*N+q,(a+1)*N+q,(a+1)*N+j];f.append(ids);f.append([u+off for u in reversed(ids)])
  for ne,(u,w)in zip([(a-1,j),(a,q),(a+1,j),(a,(j-1)%N)],zip(ids,ids[1:]+ids[:1])):
   if ne not in cells:f.append((u,u+off,w+off,w))
 mesh('WholeOpenMouthPipe_%d'%k,v,f,1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeCabinetBarrelAndCrankGrip_Walnut',(.32,.15,.055,1),.79,0),('WholePipeRank_DullBrass',(.61,.48,.23,1),.47,.58),('WholeAxlesPinsAndFollowers_DarkSteel',(.18,.21,.22,1),.52,.5),('WholeBellowsAndWheelTires_Charcoal',(.065,.065,.058,1),.93,0)]
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
focus=Vector((0,0,.66))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.90;aim(cam,(3,-5,3));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/music/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':'Fixed Cranked Pin Barrel and Pipe Chest Street Organ','description':'One newly authored complete fixed hand-cranked street-organ exterior on its integral two-wheel and two-foot underframe. A tall compact timber cabinet contains an exposed transverse pinned barrel, independent row of full follower rods on a shared support shaft, a lower pleated bellows appearance and an upper chest carrying seven whole open-mouthed pipes. A continuous axle reaches a right-hand crank and offset grip. The pipes, barrel and bellows are independently newly drawn parts of one integrated cabinet, not an old keyboard organ and music box positioned together or extracted into a scene. There is no manual keyboard, pedal board or plucked comb. Real pipe bores, mouth openings, open cabinet inspection space and lower pleat valleys remain geometry. Four opaque solid PBR appearances, metres Z up and grounded whole horizontal envelope. One model zero scenes. Fixed illustrative silent exterior only: no supplied internal air channels, valves, functional pin sequence, tune, gearing, motor, sound, wheel/crank action, bellows motion, transport ergonomics, capacity, manufacture or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
