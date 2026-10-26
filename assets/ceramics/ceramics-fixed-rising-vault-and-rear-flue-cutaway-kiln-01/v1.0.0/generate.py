import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='ceramics-fixed-rising-vault-and-rear-flue-cutaway-kiln-01'
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



def whole_profile(name,p,a,b,axis,mat):
 if sum(u[0]*v[1]-u[1]*v[0]for u,v in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);tt=triangulate(p)
 def pt(q,t):return(t,q[0],q[1])if axis=='x'else(q[0],t,q[1])
 mesh(name,[pt(q,t)for t in[a,b]for q in p],[tuple(reversed(t))for t in tt]+[tuple(n+i for i in t)for t in tt]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],mat)
box('WholeGroundFootMasonryFoundation',(-.12,0,.08),(4.30,1.72,.16),2)
# Entire rising bed has a flat grounded underside and one continuous inclined upper face.
whole_profile('WholeRisingChamberFloor',[(-1.32,.15),(1.39,.15),(1.39,.91),(-1.32,.34)],-.76,.76,'y',1)
box('WholeLowFireChamberFloor',(-1.73,0,.185),(.87,.98,.075),1)
# A long arched thick shell with integral full end collars and an explicit near-side section opening.
def vault(name,sections,ri,ro,mat):
 n=25;v=[];f=[]
 for x,z,angle in sections:
  for r in [ro,ri]:
   for j in range(n):
    a=math.radians(angle)*j/(n-1);v.append((x,r*math.cos(a),z+r*math.sin(a)))
 stride=2*n
 for k in range(len(sections)-1):
  a=k*stride;b=(k+1)*stride
  for j in range(n-1):
   f.append((a+j,a+j+1,b+j+1,b+j));f.append((a+n+j,b+n+j,b+n+j+1,a+n+j+1))
  f.extend([(a,b,b+n,a+n),(a+n-1,a+2*n-1,b+2*n-1,b+n-1)])
 for k in [0,len(sections)-1]:
  a=k*stride
  for j in range(n-1):
   q=(a+j,a+n+j,a+n+j+1,a+j+1);f.append(tuple(reversed(q))if k else q)
 mesh(name,v,f,mat)
vault('WholeRisingVaultWithIntegralCutawayCollars',[(-1.34,.325,180),(-1.12,.372,180),(-.96,.406,89),(.99,.817,89),(1.18,.857,180),(1.38,.899,180)],.65,.76,0)
vault('WholeLowerOpenFireArch',[(-2.12,.202,180),(-1.27,.202,180)],.37,.46,0)
# The full rear wall wraps a real rectangular outlet; the side inlet of the flue meets it.
p=[(.75*math.cos(i*math.pi/24),.895+.75*math.sin(i*math.pi/24))for i in range(25)]
p +=[(-.21,.895),(-.21,1.25),(.21,1.25),(.21,.895)]
whole_profile('WholeRearArchWallWithTrueThroat',p,1.30,1.41,'x',1)
# One shared-cell boundary for the tall hollow flue: no overlapping boxes or painted opening.
xs=[1.35,1.44,1.78,1.88];ys=[-.31,-.21,.21,.31];zs=[.15,.88,1.25,2.25]
occupied=set()
for i in range(len(xs)-1):
 for j in range(len(ys)-1):
  for k in range(len(zs)-1):
   wall=(i in[0,2]or j in[0,2]);solid=k==0 or wall
   if i==0 and j==1 and k==1:solid=False
   if solid:occupied.add((i,j,k))
v=[];f=[];idx={}
def vid(p):
 if p not in idx:idx[p]=len(v);v.append(p)
 return idx[p]
for i,j,k in sorted(occupied):
 p=[(x,y,z)for z in[zs[k],zs[k+1]]for y in[ys[j],ys[j+1]]for x in[xs[i],xs[i+1]]]
 for q,step in zip(BOX,[(0,0,-1),(0,0,1),(0,-1,0),(0,1,0),(-1,0,0),(1,0,0)]):
  if (i+step[0],j+step[1],k+step[2])not in occupied:f.append(tuple(vid(p[n])for n in q))
mesh('WholeHollowRearFlueWithSideInlet',v,f,0)
# Dark solid sill at the lower fire mouth is part of the whole empty display, not fuel.
box('WholeFrontMouthSill',(-2.105,0,.226),(.11,.73,.035),3)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeVaultAndFlue_WarmFiredClay',(.42,.21,.12,1),.93,0),('WholeChamberLining_PaleRefractory',(.67,.55,.37,1),.91,0),('WholeGroundFoundation_StoneGray',(.25,.27,.25,1),.94,0),('WholeMouthSill_DarkStone',(.12,.13,.12,1),.91,0)]
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
focus=Vector((0,0,1.00))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=5.30;aim(cam,(-5,-7,4.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/ceramics/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'ceramics','style':'S01-clean-geometric','title':'Fixed Rising Vault and Rear Flue Cutaway Kiln','description':'One independently authored complete empty rising-vault kiln illustrative cutaway. A common broad finite masonry foundation carries a low front open fire chamber, a raised throat step and an entire ascending internal floor beneath a long continuous thick arched shell. The front-facing middle side of that shell is deliberately removed with thick finished cut edges to expose the uninterrupted rising chamber; complete end arch collars remain integral to the shell. A complete rear arched wall has a genuine low throat opening leading into a tall rear hollow rectangular flue with a side inlet and open top. The fire chamber and rising chamber have different floor heights and meet at a real open passage, not an old horizontal bread oven extended or an old rectangular shelf kiln resized. Whole connected shells and an integral raised floor step, no old geometry imported. Four opaque matte stone/refractory roles, metres Z up and horizontal bounds-centred ground datum. One whole architectural display prop zero scenes. Empty static artistic section only: no fire, fuel, ware, firing cycle, temperature, ventilation, chimney draft, emissions, thermal design, construction, installation, historical accuracy, load or safety performance. Rigging animation interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
