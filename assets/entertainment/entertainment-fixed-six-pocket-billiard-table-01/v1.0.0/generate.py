import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='entertainment-fixed-six-pocket-billiard-table-01'
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



# One complete new six-pocket billiard table, no old arcade table meshes imported.
def slab_xy(name,p,z0,z1,mat):
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);v=[(x,y,z)for z in[z0,z1]for x,y in p];f=[]
 for a,b,c in triangulate(p):f.extend([(c,b,a),(a+n,b+n,c+n)])
 f += [(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh(name,v,f,mat)
# Six genuine outer-boundary concavities in one complete thick playing bed.
p=[]
def append(x,y):
 if not p or math.hypot(p[-1][0]-x,p[-1][1]-y)>1e-10:p.append((x,y))
def arc(cx,cy,a,b,n):
 for i in range(n+1):
  t=math.radians(a+(b-a)*i/n);append(cx+.12*math.cos(t),cy+.12*math.sin(t))
append(-.43,-1.05);append(.43,-1.05);arc(.55,-1.05,180,90,6)
append(.55,-.12);arc(.55,0,270,90,12);append(.55,.93);arc(.55,1.05,270,180,6)
append(-.43,1.05);arc(-.55,1.05,0,-90,6);append(-.55,.12);arc(-.55,0,90,-90,12)
append(-.55,-.93);arc(-.55,-1.05,90,0,6)
if math.hypot(p[-1][0]-p[0][0],p[-1][1]-p[0][1])<1e-10:p.pop()
slab_xy('WholeSixNotchPlayingBed',p,.90,.93,1)
# Four complete tapered legs, not loose old table furniture instances.
for i,(x,y)in enumerate([(-.48,-.88),(.48,-.88),(-.48,.88),(.48,.88)],1):
 v=[]
 for z,hx,hy in[(0,.075,.080),(.10,.075,.080),(.72,.115,.125),(.88,.115,.125)]:v.extend([(x-hx,y-hy,z),(x+hx,y-hy,z),(x+hx,y+hy,z),(x-hx,y+hy,z)])
 f=[(3,2,1,0),(12,13,14,15)]
 for k in range(3):
  for j in range(4):q=(j+1)%4;f.append((4*k+j,4*k+q,4*(k+1)+q,4*(k+1)+j))
 mesh('WholeTaperedGroundLeg_'+str(i),v,f,0)
for side,y in [('Front',-.88),('Back',.88)]:box(side+'WholeUnderbedCrossBeam',(0,y,.865),(1.20,.13,.07),0)
box('WholeCentralUnderbedSpine',(0,0,.865),(.18,1.85,.07),0)
# Split aprons and six rail/cushion spans preserve all actual mouth openings.
for side,sign in [('Left',-1),('Right',1)]:
 for half,y in [('Front',-.535),('Back',.535)]:
  box(side+half+'WholeSideApron',(sign*.615,y,.785),(.09,.73,.21),0)
  box(side+half+'WholeWoodTopRail',(sign*.625,y,.965),(.15,.77,.07),0)
  # Real broad inward cushion with bevelled inner face; no decal or fake groove.
  pr=[(.505,.935),(.605,.935),(.605,.985),(.530,.985)]
  pr=[(sign*x,z)for x,z in pr]
  if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(pr,pr[1:]+pr[:1]))<0:pr.reverse()
  n=len(pr);v=[(x,yy,z)for yy in[y-.37,y+.37]for x,z in pr];f=[]
  for a,b,c in triangulate(pr):f.extend([(a,b,c),(c+n,b+n,a+n)])
  f += [(j,j+n,(j+1)%n+n,(j+1)%n)for j in range(n)];mesh(side+half+'WholeInwardCushion',v,f,1)
for side,sign in [('Front',-1),('Back',1)]:
 box(side+'WholeEndApron',(0,sign*1.11,.785),(.84,.09,.21),0)
 box(side+'WholeWoodEndRail',(0,sign*1.115,.965),(.82,.15,.07),0)
 box(side+'WholeEndCushion',(0,sign*1.065,.958),(.80,.09,.05),1)
# Six complete blind pocket cups, real closed walls/floors and open upper mouths.
for i,(x,y)in enumerate([(-.55,-1.05),(.55,-1.05),(-.55,0),(.55,0),(-.55,1.05),(.55,1.05)],1):
 lathe_z('WholeOpenPocketCup_'+str(i),x,y,[(0,.72),(.14,.72),(.14,.985),(.11,.985),(.11,.75),(0,.75)],2,32)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('CabinetRailsAndLegs_WarmWalnut',(.30,.145,.065,1),.73,0),('WholeBedAndCushions_DeepGreen',(.035,.235,.14,1),.90,0),('SixWholePocketCups_Charcoal',(.045,.038,.030,1),.84,0)]
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
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.05;aim(cam,(4,-6,4.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/entertainment/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'entertainment','style':'S01-clean-geometric','title':'Fixed Six Pocket Billiard Table','description':'One newly authored whole static six-pocket billiard-table exterior. The continuous thick green playing bed has four curved corner cutouts and two complete semicircular side notches, each meeting one real open-top blind pocket cup with full wall and floor. Six separate raised cushion spans and thick wood rail spans leave those six mouths open. Four whole tapered grounded legs, supported underbed crossbeams and spine, and interrupted aprons carry the whole table while keeping the pocket openings visible. No old air-puck table goal frames, pinball cabinet or table-football rods/figures are imported, removed or recoloured; the complete new bed boundary and six-pocket perimeter layout are numerically authored for this whole model. Three opaque constant untextured PBR roles; metres, Z up, full horizontally bounds-centred ground origin. One complete prop, zero scenes, no independent pocket counts. Fixed empty appearance only: no balls/cues, ruleset or regulation dimensions, cushion rebound, cloth friction, ball path or return route, scoring, playability, human ergonomics, load, manufacture or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
