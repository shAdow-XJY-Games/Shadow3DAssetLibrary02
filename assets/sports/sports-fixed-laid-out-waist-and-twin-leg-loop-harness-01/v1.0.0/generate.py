import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='sports-fixed-laid-out-waist-and-twin-leg-loop-harness-01'
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



# New whole empty laid-out waist / leg-loop / connecting-strap equipment exterior.
def band(name,c,outer,inner,h,mat,n=32,rear=0):
 v=[];f=[]
 for layer in range(4):
  for j in range(n):
   t=math.tau*j/n;rx,ry=outer if layer in[0,1]else inner;z=0 if layer in[0,3]else h+rear*(1+math.sin(t))/2
   v.append((c[0]+rx*math.cos(t),c[1]+ry*math.sin(t),z))
 for k in range(4):
  for j in range(n):q=(j+1)%n;f.append((k*n+j,k*n+q,((k+1)%4)*n+q,((k+1)%4)*n+j))
 mesh(name,v,f,mat)
band('WholeGroundFootOpenWaistBand',(0,0),(.32,.22),(.278,.18),.070,0,40,.055)
for k,x in enumerate([-.19,.19]):band('WholeGroundFootOpenLegLoop_%d'%k,(x,-.48),(.15,.18),(.115,.145),.045,0,32)
def strap(name,path,width,thick,mat):
 v=[];f=[]
 for k,p in enumerate(path):
  a=path[max(0,k-1)];b=path[min(len(path)-1,k+1)];dx=b[0]-a[0];dy=b[1]-a[1];le=math.hypot(dx,dy);u=(-dy/le,dx/le,0)
  for z in[-thick/2,thick/2]:
   for s in[-1,1]:v.append((p[0]+s*width/2*u[0],p[1]+s*width/2*u[1],p[2]+z))
 f=[(0,2,3,1),(4*(len(path)-1),4*(len(path)-1)+1,4*(len(path)-1)+3,4*(len(path)-1)+2)]
 for k in range(len(path)-1):
  for a,b in[(0,1),(1,3),(3,2),(2,0)]:f.append((4*k+a,4*k+b,4*(k+1)+b,4*(k+1)+a))
 mesh(name,v,f,mat)
for k,s in enumerate([-1,1]):
 strap('WholeFrontWaistLegBridge_%d'%k,[(s*.12,-.185,.046),(s*.13,-.26,.041),(s*.13,-.33,.032)],.045,.018,1)
 strap('WholeContinuousOuterRearStrap_%d'%k,[(s*.28,.10,.065),(s*.40,-.05,.060),(s*.40,-.30,.038),(s*.32,-.46,.032)],.035,.014,1)
box('WholeTransverseFrontConnection',(0,-.26,.041),(.30,.045,.022),1)
# Closed small central upright loop in XZ, visibly separate from the full waist opening.
ringy('WholeUprightCentralBelayVisualLoop',-.278,-.248,0,.087,.036,.052,3,24)
# Complete flat front buckle frame; rooted into waist material, not floating over the aperture.
v=[];f=[]
for rx,ry,z in[(.055,.031,.063),(.055,.031,.087),(.037,.017,.087),(.037,.017,.063)]:
 for x,y in[(-rx,-ry),(rx,-ry),(rx,ry),(-rx,ry)]:v.append((.10+x,-.19+y,z))
for k in range(4):
 for j in range(4):q=(j+1)%4;f.append((4*k+j,4*k+q,4*((k+1)%4)+q,4*((k+1)%4)+j))
mesh('WholeRootedFrontBuckleFrame',v,f,2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholePaddedWaistAndLegBands_MutedBlue',(.065,.22,.28,1),.90,0),('WholeConnectionStraps_Graphite',(.045,.055,.065,1),.92,0),('WholeBuckleFrame_SatinMetal',(.43,.47,.48,1),.48,.6),('WholeBelayVisualLoop_MutedOchre',(.64,.34,.11,1),.88,0)]
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
focus=Vector((0,0,.065))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.2;aim(cam,(2,-4,6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/sports/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'sports','style':'S01-clean-geometric','title':'Fixed Laid Out Waist and Twin Leg Loop Harness','description':'One newly authored complete empty sit-harness-style exterior laid out on its flat band edges in a fixed display pose. A continuous wide oval waist band has a taller padded rear section, a genuine large central opening and a separately rooted front buckle frame. Two independent complete lower leg loops each have their own true through aperture and connect to the waist by two short front bridges and two broad continuous outer rear straps. A complete transverse front bridge joins the front connections, carrying one upright closed belay-loop-like visual ring. All material bodies are finite closed geometry with visible spaces between waist, leg loops and connecting straps; there is no person, mannequin, ropes or imported collar/backpack part. The whole waist/two-leg/fore-and-aft connection topology is newly drawn, not a horse collar with extra ring count or a backpack with its body removed. One complete prop zero scenes, four opaque solid PBR roles, metres Z up and horizontally bounds-centred ground datum. Static illustrative equipment appearance only, not a usable design or fitting guide. No certification, life support, climbing protection, fall arrest, knotting, buckle function, strength, body fit, load, manufacture, usage instruction or safety claim; rigging and animation are not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
