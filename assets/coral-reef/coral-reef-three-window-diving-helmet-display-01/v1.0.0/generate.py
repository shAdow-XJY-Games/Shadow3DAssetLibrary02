import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='coral-reef-three-window-diving-helmet-display-01'
import math
N=24
G={}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def record(name,v,f,m):
 if sum(dot(v[a],cross(v[b],v[c]))for a,b,c in f)<0:f=[(a,c,b)for a,b,c in f]
 G[name]=(v,f,m)
def box(name,lo,hi,m):
 v=[(x,y,z)for z in[lo[2],hi[2]]for y in[lo[1],hi[1]]for x in[lo[0],hi[0]]];f=[]
 for a,b,c,d in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:f.extend([(a,b,c),(a,c,d)])
 record(name,v,f,m)
def pipe(name,points,r,m,segments=8):
 v=[]
 for k,p in enumerate(points):
  tangent=unit(sub(points[min(k+1,len(points)-1)],points[max(k-1,0)]));u=(1,0,0)if abs(tangent[0])<.9 else(0,1,0);u=unit(cross(tangent,u));w=cross(tangent,u)
  for i in range(segments):v.append(add(p,add(mul(u,r*math.cos(math.tau*i/segments)),mul(w,r*math.sin(math.tau*i/segments)))))
 f=[]
 for k in range(len(points)-1):
  for i in range(segments):
   j=(i+1)%segments;a=k*segments+i;b=k*segments+j;c=(k+1)*segments+j;d=(k+1)*segments+i;f.extend([(a,b,c),(a,c,d)])
 for k in [0,len(points)-1]:
  c=len(v);v.append(points[k]);base=k*segments
  for i in range(segments):f.append((c,base+(i+1)%segments,base+i)if k==0 else(c,base+i,base+(i+1)%segments))
 record(name,v,f,m)
def wheel(name,x,y,z,ro,ri,width,m):
 # Complete closed annular tire (or capped disc when ri=0), axis X.
 profile=[(ri,x-width/2),(ro,x-width/2),(ro,x+width/2),(ri,x+width/2)]
 v=[];rs=[]
 for r,xx in profile:
  ring=[(xx,y,z)]if r==0 else[(xx,y+r*math.sin(math.tau*i/N),z+r*math.cos(math.tau*i/N))for i in range(N)];rs.append(list(range(len(v),len(v)+len(ring))));v+=ring
 f=[]
 for a,b in zip(rs,rs[1:]+rs[:1]):
  if len(a)==len(b)==1:continue
  for i in range(N):
   j=(i+1)%N
   if len(a)==1:f.append((a[0],b[i],b[j]))
   elif len(b)==1:f.append((a[i],b[0],a[j]))
   else:f.extend([(a[i],b[i],b[j]),(a[i],b[j],a[j])])
 record(name,v,f,m)

def earclip(p):
 cr=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 ids=list(range(len(p)));out=[]
 while len(ids)>3:
  for j,b in enumerate(ids):
   a,c=ids[j-1],ids[(j+1)%len(ids)]
   if cr(p[a],p[b],p[c])<=1e-14:continue
   if any(all(cr(p[u],p[v],p[k])>=-1e-14 for u,v in [(a,b),(b,c),(c,a)])for k in ids if k not in [a,b,c]):continue
   out.append((a,b,c));ids.pop(j);break
  else:raise ValueError('Non-simple padding section')
 out.append(tuple(ids));return out
def pad(name,p,y0,y1,m):
 if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);v=[(x,y,z)for y in[y0,y1]for x,z in p];f=[]
 for a,b,c in earclip(p):f.extend([(a,b,c),(c+n,b+n,a+n)])
 for i in range(n):
  j=(i+1)%n;f.extend([(i,j+n,j),(i,i+n,j+n)])
 record(name,v,f,m)

PALETTE=[('Helmet_BurnishedCopper',(.46,.235,.105,1),.58,.60),('Collar_AgedBrass',(.52,.37,.14,1),.63,.54),('Window_OpaqueDeepBlue',(.065,.16,.21,1),.28,.15)]
FM={}
# Closed finite wedge-cell union; missing wall cells create three real apertures.
def cells_mesh(name,cells,mat):
 faces={}
 for v in cells:
  v=[tuple(round(c,12) for c in p) for p in v]
  for f in [(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:
   q=tuple(v[i] for i in f);key=tuple(sorted(q))
   if key in faces:del faces[key]
   else:faces[key]=q
 vs=[];ix={};fs=[]
 for q in faces.values():
  ids=[]
  for p in q:
   if p not in ix:ix[p]=len(vs);vs.append(p)
   ids.append(ix[p])
  fs.extend([(ids[0],ids[1],ids[2]),(ids[0],ids[2],ids[3])])
 record(name,vs,fs,mat)
def cell(t0,t1,z0,z1,ri0,ro0,ri1,ro1):
 return [(r*math.sin(t),-r*math.cos(t),z) for z,ri,ro in [(z0,ri0,ro0),(z1,ri1,ro1)] for t in [t0,t1] for r in [ri,ro]]
levels=[(.025,.115),(.10,.16),(.16,.18),(.28,.18),(.34,.14),(.39,.07)]
windows={'Front':[-2,-1,0,1],'Right':[5,6],'Left':[17,18]}
missing={i%24 for a in windows.values() for i in a};cells=[]
for k,((z0,r0),(z1,r1)) in enumerate(zip(levels,levels[1:])):
 for i in range(24):
  if k==2 and i in missing:continue
  cells.append(cell(i*math.tau/24,(i+1)*math.tau/24,z0,z1,r0-.012,r0,r1-.012,r1))
cells_mesh('WholeHollowThreeApertureHelmetShell',cells,0)
# Opaque illustrative window inserts occupy the actual openings; not transparent optics.
for label,indices in windows.items():
 t0=min(indices)*math.tau/24-.008;t1=(max(indices)+1)*math.tau/24+.008;cells=[];n=len(indices)
 for i in range(n):cells.append(cell(t0+(t1-t0)*i/n,t0+(t1-t0)*(i+1)/n,.157,.283,.166,.183,.166,.183))
 cells_mesh(label+'WholeOpaqueWindowInsert',cells,2)
# True annular lower neck flange, open to the hollow interior; closed crown cap.
for name,z,ro,ri,w,m in [('WholeOpenNeckFlange',.0175,.195,.090,.035,1),('WholeCrownCap',.39,.074,0,.018,0)]:
 wheel(name,0,0,0,ro,ri,w,m);v,f,mm=G.pop(name);record(name,[(y,zz,x+z) for x,y,zz in v],f,mm)

# Whole raised reveal frames, curved consistently with each actual aperture.
for label,indices in windows.items():
 t0=min(indices)*math.tau/24;t1=(max(indices)+1)*math.tau/24
 ts=[t0-.045,t0-.008]+[t0+(t1-t0)*k/len(indices) for k in range(1,len(indices))]+[t1+.008,t1+.045];zs=[.144,.158,.282,.296];cc=[]
 for j in range(3):
  for i in range(len(ts)-1):
   if j==1 and 0<i<len(ts)-2:continue
   cc.append(cell(ts[i],ts[i+1],zs[j],zs[j+1],.172,.199,.172,.199))
 cells_mesh(label+'WholeRaisedWindowFrame',cc,1)
for angle,label in [(-.15,'Left'),(.15,'Right')]:
 cells_mesh('FrontFixedProtectionBar'+label,[cell(angle-.022,angle+.022,.153,.287,.183,.201,.183,.201)],1)
pipe('FixedSideCappedConnector',[(.14,.035,.115),(.235,.035,.115)],.026,1,12)

for n,(v,f,m) in G.items():FM[n]=[m]*len(f)
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
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
triangles=sum(len(f)for v,f,m in G.values())
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
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
focus=Vector((0,0,.19))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.58;aim(cam,(.75,-1.2,.65));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/coral-reef/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'coral-reef','style':'S01-clean-geometric','title':'Three-Window Diving Helmet Display','description':'One newly authored static stylized three-window diving-helmet display prop for the original underwater-ruins equipment direction. A complete thick faceted domed shell has three true wall apertures occupied by separate thick curved opaque illustrative window inserts, three whole raised reveal frames, two fixed front protection bars, a solid capped side connector, a closed crown cap and a broad annular neck flange open into the shell interior. Twelve closed editable solids with three opaque constant untextured PBR materials. Unlike the existing open-backed strapped firefighting facepiece, this is an enclosing bell-like head shell with frontal and lateral windows, no rear headbands, nose-mouth mask contour, cylinder or mannequin. One prop and zero scenes. Metres, native Z up and ground-centred collar datum. Windows intentionally opaque; no see-through or optical performance. Static appearance only: not real diving equipment, no breathing, oxygen supply, pressure containment, watertightness, wearer fit, protection, historical accuracy or diving/maritime safety claim. No suit, hose, wearer or scenery; preview floor excluded.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
