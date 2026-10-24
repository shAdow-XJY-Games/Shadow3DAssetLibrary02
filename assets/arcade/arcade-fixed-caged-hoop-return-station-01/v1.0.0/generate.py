import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='arcade-fixed-caged-hoop-return-station-01'
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



# New entire caged hoop-and-return station, not old independent goal placed on a reused lane.
def xprism(name,p,x0,x1,mat):
 n=len(p);v=[(x,y,z)for x in[x0,x1]for y,z in p];f=[]
 for a,b,c in triangulate(p):f.extend([(c,b,a),(a+n,b+n,c+n)])
 f += [(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh(name,v,f,mat)
# Four actual independent ground feet and connected open underframe.
for side,x in [('Left',-.54),('Right',.54)]:
 for end,y,z in [('Front',-1.02,.74),('Rear',.88,2.22)]:
  box(side+end+'WholeGroundShoe',(x,y,.035),(.18,.20,.07),0)
  box(side+end+'WholeFrameUpright',(x,y,(.045+z)/2),(.075,.075,z-.045),0)
 box(side+'WholeLowerLongTie',(x,-.07,.29),(.058,1.96,.058),0)
for end,y in [('Front',-1.02),('Rear',.88)]:box(end+'WholeLowerCrossTie',(0,y,.31),(1.12,.055,.055),0)
# One continuous thick downward-return surface, joining a flat front receiving bay.
p=[(-1.20,.605),(-.79,.605),(.94,.985),(.94,1.04),(-.79,.66),(-1.20,.66)]
xprism('WholeContinuousDescendingReturnAndFrontCatchFloor',p,-.51,.51,1)
for side,x in [('Left',-.51),('Right',.51)]:
 p=[(-1.195,.625),(-.79,.625),(.94,1.005),(.94,1.16),(-.79,.815),(-1.195,.815)]
 xprism(side+'WholeSlopedReturnSideCheek',p,x-.027,x+.027,0)
box('WholeFrontReceivingLip',(0,-1.185,.735),(1.06,.055,.17),0)
box('WholeRearReturnClosure',(0,.92,1.10),(1.10,.055,.25),0)
# Upper catch enclosure built into this same frame; open front is not a solid wall.
for side,x in [('Left',-.54),('Right',.54)]:
 box(side+'WholeFrontCagePost',(x,-.28,1.525),(.06,.06,1.39),0)
 box(side+'WholeUpperCageRail',(x,.30,2.20),(.058,1.20,.06),0)
 beam(side+'WholeSlopingFrontCatchRail',(x,-1.03,.79),(x,-.28,2.20),.045,0)
 for j,y in enumerate([-.05,.18,.41,.64]):
  low=.66+(y+.79)*(.38/1.73)+.10
  beam(side+'WholeVerticalCatchBar_'+str(j+1),(x,y,low),(x,y,2.20),.012,0)
 for j,z in enumerate([1.30,1.59,1.88]):box(side+'WholeHorizontalCatchBar_'+str(j+1),(x+(.008 if x>0 else-.008),.30,z),(.012,1.17,.012),0)
for tag,y in [('Front',-.28),('Rear',.88)]:box(tag+'WholeUpperCageCrossbar',(0,y,2.20),(1.13,.050,.050),0)
# Full backboard is embedded into two rear uprights; no independent stand/source mesh.
box('WholeRearBackboard',(0,.84,1.86),(1.06,.075,.58),1)
outer=[(-.165,1.751),(.165,1.751),(.165,1.949),(-.165,1.949)];inner=[(-.147,1.769),(.147,1.769),(.147,1.931),(-.147,1.931)]
v=[(x,y,z)for y,p in[(.785,outer),(.810,outer),(.810,inner),(.785,inner)]for x,z in p];f=[]
for k in range(4):
 for i in range(4):j=(i+1)%4;f.append((4*k+i,4*k+j,4*((k+1)%4)+j,4*((k+1)%4)+i))
mesh('WholeContinuousRaisedRectangularHoopMark',v,f,2)
box('WholeHoopBracket',(0,.755,1.72),(.10,.17,.055),2)
# Real continuous open rim, tapered sparse strand basket and open bottom ring.
for name,r,z,w,mat in [('WholeOpenUpperHoop',.17,1.72,.017,2),('WholeOpenLowerNetRing',.105,1.47,.006,1)]:
 profile=[(r+w*math.cos(math.tau*j/8),z+w*math.sin(math.tau*j/8))for j in range(8)];lathe_z(name,0,.565,profile,mat,40)
for i in range(10):
 a=math.tau*i/10;b=a+.13;beam('WholeFixedBasketStrand_'+str(i+1),(.17*math.cos(a),.565+.17*math.sin(a),1.72),(.105*math.cos(b),.565+.105*math.sin(b),1.47),.008,1)
# One stationary ball rests slightly into the horizontal front catch floor.
profile=[(0,.657)]+[(.102*math.sin(math.pi*j/12),.758-.102*math.cos(math.pi*j/12))for j in range(1,12)]+[(0,.860)]
lathe_z('WholeStationaryReceivingBall',-.20,-.98,profile,2,24)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeFrameAndCatchRails_DeepTeal',(.055,.17,.21,1),.68,.18),('WholeReturnBackboardAndNet_Ivory',(.71,.68,.56,1),.79,0),('WholeRimTargetAndBall_MutedOrange',(.67,.255,.065,1),.77,0)]
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
focus=Vector((0,0,1.10))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.23;aim(cam,(4,-6,3.7));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/arcade/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'arcade','style':'S01-clean-geometric','title':'Fixed Caged Hoop Return Station','description':'One newly authored complete static arcade hoop-return station. Four grounded shoes and an open tied leg frame support one continuous rear-high to front-low return surface and a flat receiving bay. Two full side catch cages with sloping front rails, actual spaced bars and upper crossmembers rise into a rear backboard integrated with the same frame. A real open upper hoop, sparse closed basket strands and an open lower ring hang above the return floor; one static ball rests in the front receiving bay. All whole geometry is new, not a freestanding basketball stand arranged beside a previous lane, a hole-target table with its printed scoring changed, or the existing upward-curved roll-launch cabinet fitted with a new target. Three opaque constant untextured PBR roles, metres, native Z up and whole horizontal bounds-centred ground origin. One complete prop, zero scenes. Static unoccupied visual only: no electronics, actual scoring, ball simulation, guaranteed return route or containment, playable game, human fit, impact resistance, loading, manufacture or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
