import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='music-fixed-tapered-fingerport-tube-and-beaked-blockflute-01'
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



def perforated_loft(name,outer,inner,holes,blind_tail=False):
 N=len(outer[0]);K=len(outer);v=[p for l in outer+inner for p in l];off=K*N;fs=[];mats=[]
 def face(f,m):fs.append(f);mats.append(m)
 def oi(k,i):return k*N+(i%N)
 cells={(k,i)for k in range(K-1)for i in range(N)}-set(holes)
 for k,i in sorted(cells):
  j=(i+1)%N;ids=[oi(k,i),oi(k,j),oi(k+1,j),oi(k+1,i)]
  face(tuple(ids),0);face(tuple(q+off for q in reversed(ids)),1)
  neighbors=[(k-1,i),(k,j),(k+1,i),(k,(i-1)%N)]
  for n,(a,b)in enumerate(zip(ids,ids[1:]+ids[:1])):
   neighbor=neighbors[n]
   if neighbor in cells:continue
   if blind_tail and n==2 and k==K-2:continue
   face((a,a+off,b+off,b),1)
 if blind_tail:
  # Complete finite rear closure, separate outer and cavity caps; no right through bore.
  cout=len(v);v.append((outer[-1][0][0]+.007,0,.046));cin=len(v);v.append((inner[-1][0][0]-.001,0,.046))
  for i in range(N):
   j=(i+1)%N;face((cout,oi(K-1,i),oi(K-1,j)),0);face((cin,off+oi(K-1,j),off+oi(K-1,i)),1)
 mesh(name,v,fs,0);FM[name]=[m for f,m in zip(fs,mats)for k in range(len(f)-2)]
# Entire new long body: one continuous profiled bore with finite wall apertures.
N=32
holes_z=[.072,.112,.152,.192,.232,.272,.310]
zs=sorted(set([0,.009,.025,.045,.335,.348,.358]+[z+d for z in holes_z for d in[-.005,.005]]+[.286,.296]))
profile=[(0,.024),(.009,.024),(.025,.017),(.045,.014),(.310,.016),(.335,.020),(.348,.020),(.358,.019)]
def radius(z):
 for (a,ra),(b,rb)in zip(profile,profile[1:]):
  if a<=z<=b:return ra+(rb-ra)*(z-a)/(b-a)
 raise AssertionError(z)
outer=[];inner=[]
for z in zs:
 r=radius(z);outer.append([(r*math.cos(math.tau*i/N),r*math.sin(math.tau*i/N),z)for i in range(N)])
 inner.append([(.009*math.cos(math.tau*i/N),.009*math.sin(math.tau*i/N),z)for i in range(N)])
holes=set()
for k,(a,b)in enumerate(zip(zs,zs[1:])):
 mid=(a+b)/2
 if any(abs(mid-z)<.005 for z in holes_z):holes.update((k,i)for i in [22,23,24,25])
 if .286<mid<.296:holes.update((k,i)for i in[6,7,8,9])
perforated_loft('WholeGroundFootTaperedFingerportBody',outer,inner,holes,False)
# Full head/socket and flattened beak, with front window and a narrow open mouth.
levels=[(.342,.021,.021,.009,.009),(.355,.022,.022,.010,.010),(.374,.021,.020,.010,.010),(.386,.019,.017,.010,.008),(.397,.018,.015,.010,.006),(.408,.018,.013,.010,.004),(.425,.017,.010,.010,.0028),(.455,.015,.0065,.010,.0028)]
outer=[];inner=[]
for z,rx,ry,ix,iy in levels:
 outer.append([(rx*math.cos(math.tau*i/N),ry*math.sin(math.tau*i/N),z)for i in range(N)])
 inner.append([(ix*math.cos(math.tau*i/N),iy*math.sin(math.tau*i/N),z)for i in range(N)])
perforated_loft('WholeOpenBeakHeadAndFrontWindow',outer,inner,{(4,i)for i in[22,23,24,25]},False)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeBlockfluteExterior_PaleTimber',(.58,.38,.18,1),.64,0),('WholeBoreAndReveals_DarkTimber',(.16,.070,.025,1),.79,0)]
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
focus=Vector((0,0,.23))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.57;aim(cam,(1.7,-5,2.0));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/music/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':'Fixed Tapered Fingerport Tube and Beaked Blockflute','description':'One newly authored complete static blockflute-style exterior. A whole long tapered thick-wall body has seven genuine front finger apertures and one separate rear thumb aperture, a modest flared open lower bell and continuous empty inner bore. A complete upper head transitions from a rounded socket to a flattened beak, with a genuinely open narrow mouth and separate front window through its wall. All aperture reveals close the finite wall thickness; they are not dark discs or printed marks. Newly authored complete axial profiles and opening layout, no old vessel-flute body, bagpipe pipe or panpipe imported, cut or resized. Unlike the old broad blind ovoid chamber with two finger rows and short side neck, this has a long through-bore and end-to-end head/body arrangement; unlike seven bound stopped panpipes it is one full single-body instrument. Two opaque constant PBR roles, metres, Z up, horizontal-envelope-centred ground datum on the full lower bell annulus. One model, zero scenes. Upright illustrative display only, not a physical balance guarantee. The external head window is shown, but a sound-producing internal block, ramp and calibrated windway are not modeled or validated. No pitch, acoustic response, playing, breath resistance, hygiene, manufacturing, ergonomic or safety claim. No person, stand, rig, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
