import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='art-fixed-raised-mesh-frame-and-cantilever-platen-screen-press-01'
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



# New complete single-station raised screen-frame and cantilever platen press.
for k,x in enumerate([-.23,.23]):box('WholeGroundFootRunner_%d'%k,(x,-.10,.025),(.08,.82,.05),0)
box('WholeRearCrossTie',(0,.24,.065),(.54,.13,.08),0)
box('WholeRearSupportColumn',(0,.24,.167),(.13,.13,.23),0)
box('WholeForwardCantileverArm',(0,-.07,.147),(.075,.66,.065),0)
box('WholePlatenUndersideSeat',(0,-.16,.183),(.24,.38,.035),0)
# Full clipped-corner garment platen; front is free, no borrowed table top.
p=[(-.18,-.44),(.18,-.44),(.21,-.40),(.21,.11),(.15,.16),(-.15,.16),(-.21,.11),(-.21,-.40)];n=len(p);v=[(x,y,z)for z in[.195,.220]for x,y in p];fs=[]
for a,b,c in triangulate(p):fs.extend([(c,b,a),(a+n,b+n,c+n)])
fs +=[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh('WholeBlankCantileverPlaten',v,fs,1)
for k,x in enumerate([-.16,.16]):box('WholeHingeBearingRoot_%d'%k,(x,.24,.269),(.065,.10,.11),0)
axle('WholeRearScreenCrossPivot',-.235,.235,.22,.300,.016,2,20)
a=math.radians(40);co=math.cos(a);si=math.sin(a)
def pose(x,t,h):return(x,.22-t*co+h*si,.300+t*si+h*co)
def transform(name):
 v,f,m=G[name];G[name]=([pose(*q)for q in v],[tuple(reversed(q))for q in f],m)
# One whole thick raised rectangular frame, shared ring vertices at the four corners.
v=[];fs=[]
for x0,x1,t0,t1,h in[(-.255,.255,-.016,.685,-.016),(-.255,.255,-.016,.685,.019),(-.220,.220,.022,.649,.019),(-.220,.220,.022,.649,-.016)]:v.extend([(x0,t0,h),(x1,t0,h),(x1,t1,h),(x0,t1,h)])
for k in range(4):
 for j in range(4):q=(j+1)%4;fs.append((4*k+j,4*k+q,4*((k+1)%4)+q,4*((k+1)%4)+j))
mesh('WholeRaisedScreenFrame',v,fs,2);transform('WholeRaisedScreenFrame')
# Single connected open lattice. Adjacent cell faces are removed, no crossing coplanar sheets.
xv=[-.222];yv=[.020]
for k in range(11):xv +=[-.220+k*.044,-.218+k*.044]
for k in range(15):yv +=[.022+k*.0447,.024+k*.0447]
xv=sorted(set(xv));yv=sorted(set(yv));faces={}
for i in range(len(xv)-1):
 for j in range(len(yv)-1):
  if xv[i+1]-xv[i]>.003 and yv[j+1]-yv[j]>.003:continue
  vv=[(x,y,z)for z in[-.003,.001]for y in[yv[j],yv[j+1]]for x in[xv[i],xv[i+1]]]
  for ff in BOX:
   q=tuple(vv[k]for k in ff);key=tuple(sorted(q))
   if key in faces:del faces[key]
   else:faces[key]=q
v=[];ind={};fs=[]
for q in faces.values():
 row=[]
 for z in q:
  if z not in ind:ind[z]=len(v);v.append(z)
  row.append(ind[z])
 fs.append(row)
mesh('WholeConnectedOpenScreenLattice',v,fs,3);transform('WholeConnectedOpenScreenLattice')
for k,x in enumerate([-.16,.16]):
 box('WholeScreenClampLower_%d'%k,(x,.013,-.022),(.075,.075,.023),0);transform('WholeScreenClampLower_%d'%k)
 box('WholeScreenClampUpper_%d'%k,(x,.013,.031),(.075,.075,.024),0);transform('WholeScreenClampUpper_%d'%k)
 box('WholeScreenClampBack_%d'%k,(x,-.024,.005),(.075,.018,.076),0);transform('WholeScreenClampBack_%d'%k)
 lathe_z('WholeFixedClampKnob_%d'%k,x,.013,[(0,.039),(.009,.039),(.009,.064),(.021,.064),(.021,.077),(0,.077)],3,16);transform('WholeFixedClampKnob_%d'%k)
 # Actual fixed side stays join the lower frame base to the raised screen edge.
 beam('WholeFixedAngleStay_%d'%k,(x,.240,.250),pose((-.24 if x<0 else .24),.18,-.008),.013,2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholePressUnderframeAndClamps_DeepBlue',(.055,.18,.25,1),.67,.26),('WholeBlankPlaten_WarmBoard',(.66,.48,.27,1),.85,0),('WholeScreenFramePivotAndStays_SatinAlloy',(.48,.53,.54,1),.46,.65),('WholeOpenLatticeAndKnobs_Charcoal',(.055,.062,.060,1),.83,0)]
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
focus=Vector((0,0,.34))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.16;aim(cam,(3,-5,4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/art/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'art','style':'S01-clean-geometric','title':'Fixed Raised Mesh Frame and Cantilever Platen Screen Press','description':'One newly authored complete single-station screen-printing-press appearance in a fixed raised-frame pose. Two whole grounded rails and a rear crossmember carry a short rear column and long forward cantilever arm beneath one complete blank garment-shaped platen. Two rear hinge roots and a common axle carry two real clamp-body appearances and one continuous rectangular raised screen frame. A single connected thin open lattice spans the complete frame opening with genuine through-cells, not transparent texture or a solid gray sheet. Two whole side stays fix the display angle. The rear hinge/forward empty platen/raised open-mesh relationship is new, not the old vertical chase and lever platen press or rotary duplicator repurposed. No prior press mesh imported; no squeegee, ink, garment or artwork included. One complete prop, zero scenes, four opaque constant PBR materials, metres Z up and whole horizontal ground datum. Static workshop appearance only: no stencil, ink transfer, mesh tension, hinge sweep, clamping, registration, manufacturing, installation, capacity or machinery safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
