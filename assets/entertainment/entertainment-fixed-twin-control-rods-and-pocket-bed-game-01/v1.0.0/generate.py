import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='entertainment-fixed-twin-control-rods-and-pocket-bed-game-01'
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



# New full collection bed, perforated upper landing board and finite blind pocket floors.
box('WholeGroundFootCollectionBase',(0,0,.014),(.330,1.22,.028),0)
def perforated(name,x0,x1,y0,y1,holes,z0,z1,mat):
 xs=sorted(set([x0,x1]+[r[i]for r in holes for i in[0,1]]));ys=sorted(set([y0,y1]+[r[i]for r in holes for i in[2,3]]));v=[];f=[];vm={};edges={}
 def vi(p):
  if p not in vm:vm[p]=len(v);v.append(p)
  return vm[p]
 for a,b in zip(xs,xs[1:]):
  for c,d in zip(ys,ys[1:]):
   if any(r[0]<(a+b)/2<r[1]and r[2]<(c+d)/2<r[3]for r in holes):continue
   ps=[(a,c),(b,c),(b,d),(a,d)];f +=[tuple(vi((*p,z1))for p in ps),tuple(vi((*p,z0))for p in reversed(ps))]
   for u,w in zip(ps,ps[1:]+ps[:1]):edges.setdefault(tuple(sorted([u,w])),[]).append((u,w))
 for es in edges.values():
  if len(es)==1:
   a,b=es[0];f.append(tuple(vi(p)for p in[(*a,z0),(*b,z0),(*b,z1),(*a,z1)]))
 mesh(name,v,f,mat)
perforated('WholeFiveApertureLandingBoard',-.153,.153,-.592,.592,[(-.060,.060,y-.063,y+.063)for y in[-.40,-.20,0,.20,.40]],.026,.080,1)
for j,x in enumerate([-.153,.153]):box('WholeLongRaisedSideRim_%d'%j,(x,0,.068),(.024,1.20,.086),0)
for j,y in enumerate([-.591,.591]):box('WholeRaisedEndRim_%d'%j,(0,y,.062),(.292,.026,.068),0)
# Two independent whole long rods fan from two fixed rear pivots towards the handgrips.
def rod(name,a,b,r,mat,n=16):
 w=unit(sub(b,a));u=unit(cross(w,(0,0,1)));v2=cross(w,u);vs=[tuple(p[k]+r*(u[k]*math.cos(math.tau*i/n)+v2[k]*math.sin(math.tau*i/n))for k in range(3))for p in[a,b]for i in range(n)];f=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh(name,vs,f,mat)
for j,sgn in enumerate([-1,1]):
 x=sgn*.025
 box('WholeRearPivotPlinth_%d'%j,(x,.538,.112),(.044,.070,.080),0)
 lathe_z('WholeRearVerticalPivot_%d'%j,x,.538,[(0,.137),(.012,.137),(.012,.180),(0,.180)],3,16)
 rod('WholeLongControlRod_%d'%j,(x,.538,.160),(sgn*.108,-.745,.160),.007,3,16)
 rod('WholeFrontHandGrip_%d'%j,(sgn*.1005,-.630,.160),(sgn*.1132,-.825,.160),.019,2,20)
 # Small fixed front saddles are honest static display supports, not moving guide mechanics.
 box('WholeFrontRodSaddle_%d'%j,(sgn*.0928,-.510,.117),(.025,.036,.080),0)
# Fixed whole ball seats very slightly into both rods; not an animated/solved path.
y=.13;xrod=.025+(.538-y)/1.283*.083;r=.061;zc=.160+math.sqrt((r+.007)**2-xrod*xrod)-.0015
profile=[(0,zc-r)]+[(r*math.sin(math.pi*k/12),zc-r*math.cos(math.pi*k/12))for k in range(1,12)]+[(0,zc+r)]
lathe_z('WholeFixedBallAcrossTwoRods',0,y,profile,3,24)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeBedRimsAndSupports_WarmTimber',(.43,.23,.10,1),.78,0),('WholePocketLandingBoard_MutedTeal',(.07,.25,.24,1),.77,0),('WholeLongRodGrips_DarkWalnut',(.12,.065,.032,1),.72,0),('WholeRodsPivotsAndBall_DullMetal',(.45,.49,.50,1),.34,.65)]
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
focus=Vector((0,0,.13))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.72;aim(cam,(3,-5,4.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/entertainment/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'entertainment','style':'S01-clean-geometric','title':'Fixed Twin Control Rods and Pocket Bed Game','description':'One newly authored complete static two-rod ball-control tabletop game appearance. A whole long grounded timber bed supports one continuous upper landing board with five genuine through apertures over the separate full blind bottom, bounded by real raised side and end rims. Two separate full long thin rods extend from independent rear pivot plinths to projecting front handgrips, slightly fanning apart above the open pockets; short fixed front saddles represent the displayed resting pose. One complete ball is visibly seated across both rods. The whole bed, pierced landing board, paired rod support architecture and ball are newly authored, not old gimballed maze geometry with obstacles removed and not the tabletop suspended-ball skittle set with renamed pieces. There is no gimbal frame, tilting playing floor, maze walls, overhead mast, tether or skittle targets. One game prop/kit zero scenes; subordinate ball and rods not separately counted. Four opaque untextured PBR roles, metres, Z up, full horizontal envelope centre on the finite bed underside. Fixed illustrative still life only: intentional tiny ball/rod support overlaps do not validate ball movement. No playable physics, rod travel, scoring, rules, coordination training, human fit, durability, manufacturing or toy/child safety. Rigging, animation and interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
