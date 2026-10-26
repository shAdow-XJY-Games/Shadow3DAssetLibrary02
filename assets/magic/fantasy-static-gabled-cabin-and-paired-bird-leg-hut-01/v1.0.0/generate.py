import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='fantasy-static-gabled-cabin-and-paired-bird-leg-hut-01'
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

def cell_union(name,cells,mat):
 faces={}
 for v in cells:
  v=[tuple(round(c,12)for c in p)for p in v]
  for f in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:
   q=tuple(v[i]for i in f);key=tuple(sorted(q))
   if key in faces:del faces[key]
   else:faces[key]=q
 v=[];ix={};f=[]
 for q in faces.values():
  ids=[]
  for p in q:
   if p not in ix:ix[p]=len(v);v.append(p)
   ids.append(ix[p])
  f.extend([(ids[0],ids[1],ids[2]),(ids[0],ids[2],ids[3])])
 record(name,v,f,mat)
def turned(name,x,y,profile,m,seg=16):
 v=[];rs=[];f=[]
 for r,z in profile:
  pts=[(x,y,z)]if r==0 else[(x+r*math.cos(math.tau*i/seg),y+r*math.sin(math.tau*i/seg),z)for i in range(seg)]
  rs.append(list(range(len(v),len(v)+len(pts))));v+=pts
 for a,b in zip(rs,rs[1:]+rs[:1]):
  if len(a)==len(b)==1:continue
  for i in range(seg):
   j=(i+1)%seg
   if len(a)==1:f.append((a[0],b[i],b[j]))
   elif len(b)==1:f.append((a[i],b[0],a[j]))
   else:f.extend([(a[i],b[i],b[j]),(a[i],b[j],a[j])])
 record(name,v,f,m)
PALETTE=[('WholeHutWarmTimber',(.35,.20,.085,1),.87,0),('WholeHutMutedRoof',(.13,.20,.16,1),.88,0),('WholeHutBirdLegOchre',(.49,.31,.13,1),.86,0)]
FM={}
def shaped(name,rows,axis,mat,n=12,bands=None):
 v=[];f=[];mats=[]
 for x,y,z,rx,ry in rows:
  for j in range(n):
   a=math.tau*j/n
   v.append((x+rx*math.cos(a),y+ry*math.sin(a),z)if axis=='Z'else((x,y+rx*math.cos(a),z+ry*math.sin(a))if axis=='X'else(x+rx*math.cos(a),y,z+ry*math.sin(a))))
 for k in range(len(rows)-1):
  for j in range(n):
   a=k*n+j;b=k*n+(j+1)%n;c=b+n;d=a+n;f.extend([(a,b,c),(a,c,d)]);mats.extend([bands[k]if bands else mat]*2)
 for k in [0,len(rows)-1]:
  center=len(v);v.append(rows[k][:3])
  for j in range(n):f.append((center,k*n+(j+1)%n,k*n+j)if k==0 else(center,k*n+j,k*n+(j+1)%n));mats.append(bands[0 if k==0 else-1]if bands else mat)
 record(name,v,f,mat);FM[name]=mats

# Continuous closed cabin material boundary has floor, walls, a real front doorway and side window.
xs=[-.65,-.56,-.19,.19,.56,.65];ys=[-.48,-.39,.39,.48];zs=[1.15,1.27,1.95,2.34];cc=[]
for i in range(5):
 for j in range(3):
  for k in range(3):
   solid=k==0 or i in[0,4] or j in[0,2]
   if j==0 and i==2 and k==1:solid=False
   if i==4 and j==1 and k==2:solid=False
   if solid:cc.append([(x,y,z)for z in[zs[k],zs[k+1]]for y in[ys[j],ys[j+1]]for x in[xs[i],xs[i+1]]])
cell_union('WholeCabinFloorWallsDoorAndSideWindow',cc,0)
for lab,y0,y1 in [('Front',-.50,-.40),('Back',.40,.50)]:
 pad('Whole'+lab+'ClosedGable',[(-.65,2.23),(.65,2.23),(.65,2.31),(0,2.87),(-.65,2.31)],y0,y1,0)
pad('WholeThickOverhangingGableRoof',[(-.80,2.20),(0,2.87),(.80,2.20),(.80,2.31),(0,2.98),(-.80,2.31)],-.60,.60,1)
box('WholeRightWindowMullion',(.555,-.025,1.91),(.665,.025,2.41),1)
for side,sg in [('Left',-1),('Right',1)]:
 # One new continuous large thigh, rear hock and tapering lower bird leg, no old character mesh.
 shaped(side+'WholeBentBirdLeg',[(sg*.34,.035,1.22,.18,.16),(sg*.37,.07,1.04,.16,.145),(sg*.39,.22,.77,.085,.095),(sg*.38,.24,.64,.066,.075),(sg*.37,-.005,.27,.047,.055),(sg*.37,-.055,.065,.044,.048)],'Z',2,12)
 p=[(-.075,.10),(-.13,.24),(-.105,.28),(-.035,.17),(.035,.17),(.105,.28),(.13,.24),(.075,.10),(.082,-.035),(.235,-.24),(.215,-.29),(.09,-.19),(.048,-.39),(.0,-.445),(-.048,-.39),(-.09,-.19),(-.215,-.29),(-.235,-.24),(-.082,-.035)]
 name=side+'WholeSplayedToeFoot';pad(name,p,0,.085,2);v,f,m=G[name];G[name]=([(sg*.37+x,-.055+z,y)for x,y,z in v],[(a,c,b)for a,b,c in f],m)
 # Dark finite claw tips follow actual foot ends, not detached teeth.
 for j,(xx,yy)in enumerate([(-.215,-.27),(0,-.42),(.215,-.27)]):
  shaped(side+'WholeToeClaw'+str(j),[(sg*.37+xx,-.055+yy+.055,.045,.035,.033),(sg*.37+xx,-.055+yy-.02,.037,.023,.023),(sg*.37+xx,-.055+yy-.055,.022,.006,.009)],'Y',1,8)
# Real doorway remains empty, with no dark false door decal or claimed access route.
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
for n,(v,f,m)in G.items():FM.setdefault(n,[m]*len(f))
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
focus=Vector((0,0,1.5))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.65;aim(cam,(4.4,-8,3.9));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/magic/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'magic','style':'S01-clean-geometric','title':'Static Gabled Cabin and Paired Bird Leg Hut','description':'One wholly newly authored fictional bird-legged hut in a fixed standing art pose. A complete finite cabin floor and thick walls contain a true front doorway and a true side window beneath full gables and one continuous thick overhanging pitched roof. Two whole large jointed bird legs merge into the floor underside, bend backward at separate hocks and descend to two whole spread-toe feet with rooted blunt claw appearances. The complete raised dwelling-body and organic two-leg/toe support silhouette is the subject, not a familiar hut given more posts, a recoloured animal enclosure or an extracted bird character. No old cabin, roof, bird or foot mesh is imported. Three opaque matte PBR roles, metres Z up, whole horizontal bounds centred and both feet at ground; one static fantasy prop zero scenes. Interior is empty and partly occluded, not a furnished living space. No walking, balance, load capacity, structural stability, real construction, inhabitation, access, creature anatomy or safety capability. Rigging animation interaction are not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
