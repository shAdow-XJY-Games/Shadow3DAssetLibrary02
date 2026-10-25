import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='sports-fixed-curved-sail-wishbone-and-footstrap-windsurf-rig-01'
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



# Whole new board, intentionally inclined fixed display, not old surfboard geometry.
rows=[(-1.13,.035,.018),(-1.08,.105,.004),(-1.04,.180,0),(-.95,.255,0),(-.82,.310,.032),(-.60,.350,.072),(-.25,.365,.126),(.15,.360,.185),(.50,.335,.230),(.80,.300,.255),(1.02,.265,.270),(1.10,.230,.275)]
ring=[(-.70,0),(.70,0),(.92,.12),(1,.40),(.96,.70),(.78,.93),(.55,1),(-.55,1),(-.78,.93),(-.96,.70),(-1,.40),(-.92,.12)]
v=[(x*w,y,z+t*.085)for y,w,z in rows for x,t in ring];n=len(ring);f=[tuple(reversed(range(n))),tuple((len(rows)-1)*n+i for i in range(n))]+[(k*n+i,k*n+(i+1)%n,(k+1)*n+(i+1)%n,(k+1)*n+i)for k in range(len(rows)-1)for i in range(n)]
mesh('WholeGroundFootWideTailRockerBoard',v,f,0)
def yz_prism(name,p,x0,x1,mat):
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);v=[(x,y,z)for x in[x0,x1]for y,z in p];f=[]
 for a,b,c in triangulate(p):f.extend([(c,b,a),(a+n,b+n,c+n)])
 f +=[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh(name,v,f,mat)
yz_prism('WholeGroundFootSweptRearFin',[(.57,.252),(.96,.287),(.95,.170),(.88,0),(.70,0),(.68,.160)],-.012,.012,2)
def tube(name,path,r,mat,n=10):
 v=[];f=[]
 for k,p in enumerate(path):
  t=unit(sub(path[min(k+1,len(path)-1)],path[max(0,k-1)]));u=unit(cross(t,(1,0,0)if abs(t[0])<.9 else(0,1,0)));w=cross(t,u)
  for j in range(n):v.append(tuple(p[a]+r*(u[a]*math.cos(math.tau*j/n)+w[a]*math.sin(math.tau*j/n))for a in range(3)))
 for k in range(len(path)-1):
  for i in range(n):j=(i+1)%n;f.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i))
 f +=[tuple(reversed(range(n))),tuple((len(path)-1)*n+i for i in range(n))];mesh(name,v,f,mat)
lathe_z('WholeDeckMastRoot',0,-.25,[(0,.199),(.055,.199),(.055,.235),(.030,.265),(0,.265)],2,20)
mast=[(0,-.25,.23),(0,-.32,1.15),(0,-.40,1.8),(0,-.45,2.4),(0,-.40,2.96)]
tube('WholeCurvedMast',mast,.024,2,12)
outline=[(-.25,.252),(.50,.62),(.95,1.02),(.86,1.75),(.55,2.45),(-.40,2.96),(-.45,2.40),(-.40,1.80),(-.32,1.15)]
yz_prism('WholeClosedCurvedTriangularSail',outline,-.005,.005,1)
vs,fs,mi=G['WholeClosedCurvedTriangularSail'];FM['WholeClosedCurvedTriangularSail']=[1 if sum(vs[i][2]for i in face)/3>1.5 else 3 for face in fs]
# Continuous bowed sides enclose the sail rather than crossing it midway.
for tag,sg in [('Left',-1),('Right',1)]:tube('WholeWishboneArm_'+tag,[(0,-.32,1.15),(sg*.18,-.14,1.15),(sg*.235,.22,1.15),(sg*.205,.55,1.15),(sg*.10,.79,1.15),(0,.93,1.15)],.014,2,10)
lathe_z('WholeMastBoomClamp',0,-.32,[(.023,1.115),(.037,1.115),(.037,1.185),(.023,1.185)],2,20)
box('WholeTrailingBoomClamp',(0,.924,1.15),(.054,.045,.050),2)
def deck(y):
 for (a,w,z),(b,ww,zz)in zip(rows,rows[1:]):
  if a<=y<=b:return z+(zz-z)*(y-a)/(b-a)+.085
 raise AssertionError(y)
# Full arched straps have thick walls and an actual empty under-arch span.
for k,y in enumerate([.25,.53,.80]):
 z=deck(y);p=[(-.145,z-.005),(-.102,z-.005),(-.095,z+.054),(-.065,z+.082),(.065,z+.082),(.095,z+.054),(.102,z-.005),(.145,z-.005),(.133,z+.069),(.090,z+.112),(-.090,z+.112),(-.133,z+.069)]
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:p.reverse()
 n=len(p);v=[(x,yy,zz)for yy in[y-.020,y+.020]for x,zz in p];f=[]
 for a,b,c in triangulate(p):f.extend([(a,b,c),(c+n,b+n,a+n)])
 f +=[(i,i+n,(i+1)%n+n,(i+1)%n)for i in range(n)];mesh('WholeOpenArchedFootStrap_%d'%k,v,f,2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeWideBoard_MutedCoral',(.61,.19,.105,1),.66,.04),('WholeUpperSail_OpaqueIvory',(.78,.75,.62,1),.84,0),('WholeMastBoomFinAndStraps_Charcoal',(.045,.061,.068,1),.65,.08),('WholeLowerSail_OpaqueTeal',(.055,.29,.31,1),.80,0)]
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
focus=Vector((0,0,1.35))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.55;aim(cam,(5,-6,3.3));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/sports/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'sports','style':'S01-clean-geometric','title':'Fixed Curved Sail Wishbone and Footstrap Windsurf Rig','description':'One newly authored whole static windsurf-rig appearance. A wide-tailed continuous low faceted board has an entirely new rocker and section profile, a real thick swept underside fin and three full arched foot straps with empty openings. One long curved mast rises from a modeled deck root and follows the leading edge of a single finite-thickness curved triangular sail. Two continuous bowed tubular arms form the complete wishbone grip around both sides of the sail and meet at the mast and trailing clamp. The sail is an actual closed polygonal solid with face-assigned opaque panels, not a texture or transparent sheet. The fixed inclined storage pose rests on finite nose-bottom and fin-tip patches; it is not a floating simulation or stability guarantee. No old surfboard, kite or other mesh was imported. This integrated mast/sail/wishbone/strap/board arrangement is not the old single-fin surfboard with changed paint, and has no kite cross spar, paper diamond or ribbon tail. Four opaque constant untextured PBR roles, metres, Z up and whole horizontally centred ground datum. One prop, zero scenes. Static illustrative exterior only: sail tension, aerodynamic or hydrodynamic performance, rigging adjustment, steering, user fit, buoyancy, wind or water use, manufacture and safety are not verified; no animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
