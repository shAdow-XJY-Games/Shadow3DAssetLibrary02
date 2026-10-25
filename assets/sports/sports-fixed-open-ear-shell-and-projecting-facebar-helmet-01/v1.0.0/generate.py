import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='sports-fixed-open-ear-shell-and-projecting-facebar-helmet-01'
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



# Newly drawn complete crown, ear apertures, coarse projecting faceguard and chin cup.
def cells_mesh(name,cells,mat):
 faces={}
 for vv in cells:
  vv=[tuple(round(x,12)for x in v)for v in vv]
  for ff in BOX:
   q=tuple(vv[i]for i in ff);key=tuple(sorted(q))
   if key in faces:del faces[key]
   else:faces[key]=q
 v=[];ids={};fs=[]
 for q in faces.values():
  z=[]
  for a in q:
   if a not in ids:ids[a]=len(v);v.append(a)
   z.append(ids[a])
  fs.append(z)
 mesh(name,v,fs,mat)
levels=[(0,.112),(.045,.132),(.095,.145),(.165,.148),(.225,.133),(.275,.101),(.305,.045)]
cells=[];S=32
for k,((z0,r0),(z1,r1))in enumerate(zip(levels,levels[1:])):
 for i in range(S):
  # Broad open face below the brow; independent actual lateral ear ports.
  if k<3 and i in list(range(0,6))+list(range(26,32)):continue
  if k==1 and i in[7,8,23,24]:continue
  cells.append([(r*math.sin(t),-r*math.cos(t)*1.12,z)for z,ro in[(z0,r0),(z1,r1)]for t in[i*math.tau/S,(i+1)*math.tau/S]for r in[ro-.009,ro]])
cells_mesh('WholeGroundFootOpenFaceAndEarPortShell',cells,0)
# Closed crown patch overlaps the upper shell only on its hidden inner seat.
lathe_z('WholeCrownTopPatch',0,0,[(0,.302),(.045,.302),(.045,.308),(0,.316)],0,32)
v,ff,m=G['WholeCrownTopPatch'];G['WholeCrownTopPatch']=([(x,y*1.12,z)for x,y,z in v],ff,m)
def tube(name,pts,r,mat,n=8,closed=False):
 v=[];L=len(pts)
 for k,P in enumerate(pts):
  prev=pts[(k-1)%L]if closed else pts[max(k-1,0)];nex=pts[(k+1)%L]if closed else pts[min(k+1,L-1)];T=unit(sub(nex,prev));u=unit(cross(T,(0,1,0)if abs(T[1])<.9 else(1,0,0)));w=cross(T,u)
  for i in range(n):v.append(tuple(P[q]+r*(u[q]*math.cos(math.tau*i/n)+w[q]*math.sin(math.tau*i/n))for q in range(3)))
 fs=[]
 for k in range(L if closed else L-1):
  kk=(k+1)%L
  for i in range(n):fs.append((k*n+i,k*n+(i+1)%n,kk*n+(i+1)%n,kk*n+i))
 if not closed:fs +=[tuple(reversed(range(n))),tuple((L-1)*n+i for i in range(n))]
 mesh(name,v,fs,mat)

for k,z in enumerate([.063,.128]):
 pts=[(-.133,-.040,z+.015),(-.144,-.115,z),(-.115,-.219,z),(-.055,-.242,z),(0,-.246,z),(.055,-.242,z),(.115,-.219,z),(.144,-.115,z),(.133,-.040,z+.015)]
 tube('WholeRootedProjectingFacebar_%d'%k,pts,.007,1,8)
for k,x in enumerate([-.052,.052]):tube('WholeFrontVerticalBar_%d'%k,[(x,-.242,.058),(x,-.245,.095),(x,-.242,.133)],.006,1,8)
# Shallow open-backed curved chin cup, no solid fake dark mouth aperture.
lathe_z('WholeConcaveChinCup',0,0,[(0,0),(.024,0),(.038,.012),(.040,.023),(.032,.023),(.030,.014),(.020,.008),(0,.008)],2,24)
v,ff,m=G['WholeConcaveChinCup'];G['WholeConcaveChinCup']=([(x,-.207+z,.053-y)for x,y,z in v],ff,m)
for k,sgn in enumerate([-1,1]):
 beam('WholeChinRetentionStrap_%d'%k,(sgn*.030,-.190,.053),(sgn*.119,-.030,.025),.016,3)
 axle('WholeFacebarSideRoot_%d'%k,sgn*.125,sgn*.145,-.040,.135,.018,1,12)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeHelmetShell_MutedBlue',(.065,.24,.34,1),.58,0),('WholeCoarseFacebars_OffWhite',(.76,.77,.71,1),.60,.08),('WholeChinCup_WarmGrey',(.45,.46,.42,1),.89,0),('WholeRetentionStraps_Graphite',(.06,.07,.075,1),.93,0)]
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
focus=Vector((0,0,.15))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.60;aim(cam,(3,-5,3));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/sports/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'sports','style':'S01-clean-geometric','title':'Fixed Open Ear Shell and Projecting Facebar Helmet','description':'One newly authored complete empty football-style helmet exterior. A continuous thick crowned shell has a large open face, open lower neck and two real side ear ports. A separate coarse projecting face-bar assembly is rooted at both shell sides, with two broad bent horizontal bars and two short front vertical bars, not a dense domed fencing grid or a raised visor plate. A shallow concave chin cup and two fixed straps complete the static empty appearance. All geometry is opaque solid low-poly art, no wearer or imported old helmet numeric geometry. One whole model zero scenes. No impact protection, certification, fitting, wearing, materials specification, sporting suitability, mechanism or safety capability is claimed; rigging and animation not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
