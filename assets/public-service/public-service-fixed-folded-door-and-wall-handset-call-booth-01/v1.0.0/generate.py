import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='public-service-fixed-folded-door-and-wall-handset-call-booth-01'
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



def union(name,boxes,mat,cuts=()):
 axes=[sorted({round(p[k],9)for b in list(boxes)+list(cuts)for p in b})for k in range(3)];used=set()
 for i in range(len(axes[0])-1):
  for j in range(len(axes[1])-1):
   for k in range(len(axes[2])-1):
    c=[(axes[a][n]+axes[a][n+1])/2 for a,n in enumerate((i,j,k))]
    inside=lambda b:all(b[0][a]<c[a]<b[1][a]for a in range(3))
    if any(inside(b)for b in boxes)and not any(inside(b)for b in cuts):used.add((i,j,k))
 v=[];f=[];ix={};corners=[(0,0,0),(1,0,0),(0,1,0),(1,1,0),(0,0,1),(1,0,1),(0,1,1),(1,1,1)]
 defs=[((0,0,-1),(0,2,3,1)),((0,0,1),(4,5,7,6)),((0,-1,0),(0,1,5,4)),((0,1,0),(2,6,7,3)),((-1,0,0),(0,4,6,2)),((1,0,0),(1,3,7,5))]
 for cell in sorted(used):
  for d,ids in defs:
   if tuple(cell[a]+d[a]for a in range(3))in used:continue
   ff=[]
   for i in ids:
    p=tuple(axes[a][cell[a]+corners[i][a]]for a in range(3))
    if p not in ix:ix[p]=len(v);v.append(p)
    ff.append(ix[p])
   f.append(tuple(ff))
 mesh(name,v,f,mat)
box('WholeGroundFootFloor',(0,0,.04),(1.18,1.18,.08),2)
# One connected shell: back wall plus genuinely open side-window frames.
w=[((-.52,.46,.06),(.52,.52,2.28))]
for sg in[-1,1]:
 x=sg*.49
 for y in[-.49,.49]:w.append(((x-.03,y-.03,.06),(x+.03,y+.03,2.28)))
 for z0,z1 in[(.06,.23),(.88,.94),(2.14,2.28)]:w.append(((x-.03,-.49,z0),(x+.03,.49,z1)))
w.append(((-.49,-.52,2.14),(.49,-.46,2.28)))
union('WholeOpenWindowAndRearWallShell',w,0)
box('WholeFlatOverhangingRoof',(0,0,2.305),(1.19,1.19,.11),0)
# Each entire folding leaf contains two actual rectangular window openings.
def door(name,a,b):
 le=math.dist(a,b);t=.048
 boxes=[((0,-t/2,.10),(.045,t/2,2.13)),((le-.045,-t/2,.10),(le,t/2,2.13))]
 for z0,z1 in[(.10,.24),(.89,.95),(2.06,2.13)]:boxes.append(((.025,-t/2,z0),(le-.025,t/2,z1)))
 union(name,boxes,0);v,f,m=G[name];dx=(b[0]-a[0])/le;dy=(b[1]-a[1])/le;G[name]=([(a[0]+dx*x-dy*y,a[1]+dy*x+dx*y,z)for x,y,z in v],f,m)
a=(-.49,-.49);b=(-.24,-.16);c=(.01,-.49)
door('WholeInwardFoldDoorLeafA',a,b);door('WholeInwardFoldDoorLeafB',b,c)
for j,p in enumerate([a,b]):lathe_z('WholeFoldHinge'+str(j),*p,[(0,.12),(.028,.12),(.028,2.11),(0,2.11)],3,12)
# Complete wall casing with actual blind slots cut from its front-facing material.
union('WholeWallPhoneBody',[((-.23,.30,.98),(.23,.49,1.68))],3,[((.055,.28,1.48),(.17,.39,1.505)),((.04,.28,1.045),(.18,.40,1.11))])
box('WholeBlankKeypadSeat',(.09,.293,1.295),(.20,.032,.25),1)
for z in range(4):
 for x in range(3):box('WholeBlankKey'+str((x,z)),(.035+.055*x,.272,1.215+.052*z),(.034,.018,.030),3)
box('WholeHandsetHook',(-.125,.29,1.38),(.13,.14,.04),2)
# One continuous vertical handset, not two detached cups.
prof=[(.022,1.155),(.047,1.17),(.05,1.21),(.031,1.25),(.024,1.30),(.024,1.43),(.032,1.47),(.05,1.51),(.047,1.55),(.022,1.565)]
lathe_z('WholeBridgedVerticalHandset',-.13,.205,[(0,1.155)]+prof+[(0,1.565)],3,20)
def cord(name,path,r):
 v=[];f=[];N=8
 for j,p in enumerate(path):
  w=unit(sub(path[min(j+1,len(path)-1)],path[max(0,j-1)]));u=unit(cross(w,(0,1,0)));q=cross(w,u)
  for i in range(N):v.append(tuple(p[k]+r*(u[k]*math.cos(math.tau*i/N)+q[k]*math.sin(math.tau*i/N))for k in range(3)))
 f=[tuple(reversed(range(N))),tuple((len(path)-1)*N+i for i in range(N))]+[(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i)for j in range(len(path)-1)for i in range(N)]
 mesh(name,v,f,3)
cord('WholeHandsetReturnCord',[(-.13,.205,1.17),(-.15,.205,1.10),(-.16,.205,.97),(-.13,.205,.90),(-.06,.205,.87),(.02,.215,.90),(.07,.23,.96),(.10,.27,1.02),(.12,.34,1.035)],.009)
# A handle roots in the free leaf, outside its real opening.
beam('WholeFoldDoorGrip',(.005,-.49,1.02),(.005,-.49,1.22),.045,1)
# Centre the full envelope once; all relationships remain unchanged.
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];shift=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-shift[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('Enclosure_MutedForest',(.10,.28,.23,1),.66,.12),('BlankPanel_WarmIvory',(.78,.75,.63,1),.62,.04),('FloorAndHook_DarkGrey',(.19,.21,.21,1),.78,.04),('PhoneAndHinges_Charcoal',(.045,.055,.06,1),.5,.12)]
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
focus=Vector((0,0,1.18))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.15;aim(cam,(3.5,-7,3.4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/public-service/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'public-service','style':'S01-clean-geometric','title':'Folded Door and Wall Handset Call Booth','description':'One newly authored complete fixed public call-booth exterior and open interior. A continuous four-corner framed shell has real open side windows and one solid rear mounting wall above an integral ground floor. A low flat roof closes the top. Two entire thick windowed entrance leaves form one fixed inward-folded pair around a continuous common hinge and left jamb, leaving the remaining front opening empty. A newly drawn wall-mounted phone body has real blind coin and return recesses, a blank keypad and one whole vertically bridged bulb-ended handset on a short bracket; one continuous curved cord returns to that same body. This is not the old table telephone placed into a service-window kiosk: no desktop base, rotary finger wheel, front counter, hipped striped roof or rear staff door is imported. Every visible surface is newly authored. Four opaque untextured PBR roles, metre Z-up ground-centred envelope; one model zero scenes. Side and door windows are deliberately unglazed real openings, no transparent glass promise. Static artistic depiction only: no calling, signal, circuit, payment, sound, door travel, privacy, weatherproofing, human fit, accessible passage, occupancy, manufacture, installation or safety capability. Rigging animation and interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
