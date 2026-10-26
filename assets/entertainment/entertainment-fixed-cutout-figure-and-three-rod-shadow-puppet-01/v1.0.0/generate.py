import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='entertainment-fixed-cutout-figure-and-three-rod-shadow-puppet-01'
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



def cutout_prism(name,loops,y0,y1,mat):
 # Exact horizontal decomposition of whole polygon loops; all contour segments retained.
 levels=sorted(set(z for loop in loops for x,z in loop));edges=[(a,b)for loop in loops for a,b in zip(loop,loop[1:]+loop[:1])];xy=[];ids={};tf=[]
 def key(p):return(round(p[0],12),round(p[1],12))
 def idx(p):
  p=key(p)
  if p not in ids:ids[p]=len(xy);xy.append(p)
  return ids[p]
 def at(e,z):a,b=e;return a[0]+(z-a[1])*(b[0]-a[0])/(b[1]-a[1])
 def cuts(z):
  q=[]
  for a,b in edges:
   if a[1]==b[1]:
    if z==a[1]:q.extend([a[0],b[0]])
   elif min(a[1],b[1])<=z<=max(a[1],b[1]):q.append(at((a,b),z))
  return sorted(set(round(x,12)for x in q))
 for za,zb in zip(levels,levels[1:]):
  zm=(za+zb)/2;active=sorted([e for e in edges if min(e[0][1],e[1][1])<zm<max(e[0][1],e[1][1])],key=lambda e:at(e,zm));assert len(active)%2==0
  for le,re in zip(active[::2],active[1::2]):
   la,ra,lb,rb=[round(x,12)for x in[at(le,za),at(re,za),at(le,zb),at(re,zb)]]
   bottom=sorted(set([la,ra]+[x for x in cuts(za)if la<x<ra]));top=sorted(set([lb,rb]+[x for x in cuts(zb)if lb<x<rb]),reverse=True)
   boundary=[]
   for p in [(x,za)for x in bottom]+[(x,zb)for x in top]:
    q=idx(p)
    if not boundary or boundary[-1]!=q:boundary.append(q)
   if boundary[-1]==boundary[0]:boundary.pop()
   c=idx(((at(le,zm)+at(re,zm))/2,zm))
   for a,b in zip(boundary,boundary[1:]+boundary[:1]):tf.append((c,a,b))
 n=len(xy);v=[(x,y,z)for y in[y0,y1]for x,z in xy];faces=[tuple(reversed(t))for t in tf]+[tuple(n+i for i in t)for t in tf];counts={}
 for t in tf:
  for a,b in zip(t,t[1:]+t[:1]):counts.setdefault(tuple(sorted((a,b))),[]).append((a,b))
 for es in counts.values():
  if len(es)==1:a,b=es[0];faces.append((a,b,b+n,a+n))
 mesh(name,v,faces,mat)
box('WholeDisplayGroundFoot',(0,.025,.014),(.47,.20,.028),0)
outline=[(-.060,.320),(-.045,.400),(-.040,.490),(-.055,.550),(-.042,.600),(-.020,.630),(-.025,.665),(-.050,.685),(-.052,.725),(-.040,.755),(-.045,.790),(-.010,.775),(.010,.795),(.026,.767),(.045,.753),(.046,.727),(.072,.715),(.048,.702),(.054,.683),(.026,.671),(.020,.640),(.050,.615),(.056,.575),(.040,.535),(.050,.490),(.043,.400),(.065,.375),(.070,.350),(.028,.350),(.010,.395),(-.005,.465),(-.018,.395),(-.020,.320)]
holes=[[(.008,.731),(.016,.741),(.026,.731),(.016,.721)],[(-.019,.574),(0,.601),(.026,.574),(0,.548)],[(-.014,.511),(.003,.530),(.020,.510),(.004,.491)]]
cutout_prism('WholePiercedProfileHeadTorsoAndLegs',[outline]+holes,-.003,.003,1)
beam('WholeCentralHoldingRod',(0,.018,.020),(0,.018,.620),.012,0)
beam('WholeCentralRodBodyMount',(0,.018,.620),(0,0,.620),.013,0)
def flat_arm(name,a,b,w,y0,y1,mat):
 dx,dz=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dz);nx,nz=-dz/l*w/2,dx/l*w/2
 p=[(a[0]+nx,a[1]+nz),(a[0]-nx,a[1]-nz),(b[0]-nx,b[1]-nz),(b[0]+nx,b[1]+nz)]
 cutout_prism(name,[p],y0,y1,mat)
for side,shoulder,elbow,hand,root in [('Left',(-.033,.599),(-.126,.553),(-.194,.618),(-.18,.025)),('Right',(.038,.603),(.127,.584),(.189,.672),(.18,.025))]:
 flat_arm(side+'WholeFlatUpperArm',shoulder,elbow,.022,-.009,-.003,2)
 flat_arm(side+'WholeFlatForearm',elbow,hand,.018,-.015,-.008,1)
 for j,(x,z)in enumerate([shoulder,elbow,hand]):cyly(side+'WholeProudJointPin_'+str(j),-.021,.007,x,z,.007,3,12)
 beam(side+'WholeHandControlRod',(root[0],.018,root[1]),(hand[0],.018,hand[1]),.006,0)
 beam(side+'WholeRodToHandLink',(hand[0],.018,hand[1]),(hand[0],-.010,hand[1]),.007,0)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeDisplayAndHoldingRods_DarkWalnut',(.14,.095,.055,1),.80,0),('WholePiercedFigure_OchreRed',(.44,.13,.055,1),.85,0),('WholeArmLayer_MutedGreen',(.15,.25,.18,1),.83,0),('WholeProudJointPins_DullBrass',(.47,.34,.14,1),.58,.35)]
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
focus=Vector((0,0,.42))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.99;aim(cam,(.9,-6,1.6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/entertainment/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'entertainment','style':'S01-clean-geometric','title':'Fixed Cutout Figure and Three Rod Shadow Puppet','description':'One newly authored complete fixed shadow-puppet-style display. A single continuous thin but thick-walled profile character has a side-facing crowned head, nose, torso, two legs and real pierced eye and costume openings. Two separate two-segment flat arms overlap at actual rooted transverse joint pins. One complete central holding rod and two full independent hand rods run to a common plain display foot, permanently fixing the portrayed pose. The pierced silhouette, flat arm layers and below-held rods are newly authored; no volumetric wooden marionette, suspension cords, cross-control or book facade imported. Four opaque constant PBR appearances; metres Z up, complete horizontal bounds centred, display sole at zero, one model zero scenes. Generic fictional theatrical art, no identified historical costume or cultural reconstruction. No shadow-projection test, puppeteering, movable linkage, rig, animation, interaction, load or child-safety capability claimed.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
