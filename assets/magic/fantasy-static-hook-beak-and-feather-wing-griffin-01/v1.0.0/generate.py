import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='fantasy-static-hook-beak-and-feather-wing-griffin-01'
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
PALETTE=[('WholeLionBodyWarmOchre',(.47,.29,.105,1),.88,0),('WholeEagleHeadAndFeathersIvory',(.73,.69,.55,1),.93,0),('WholeHookBeakTalonsAndEyesBronze',(.14,.105,.045,1),.71,0)]
def ysections(name,sections,mat,n=16):
 v=[(x+rx*math.cos(math.tau*j/n),y,z+rz*math.sin(math.tau*j/n))for x,y,z,rx,rz in sections for j in range(n)];f=[]
 for k in range(len(sections)-1):
  for j in range(n):q=(j+1)%n;a=k*n+j;b=k*n+q;c=(k+1)*n+q;d=(k+1)*n+j;f.extend([(a,b,c),(a,c,d)])
 for k in[0,len(sections)-1]:
  q=len(v);v.append(sections[k][:3]);base=k*n
  for j in range(n):f.append((q,base+(j+1)%n,base+j)if k==0 else(q,base+j,base+(j+1)%n))
 record(name,v,f,mat)
def ovoid(name,c,r,mat):
 profile=[(0,-1)]+[(math.sin(math.pi*k/8),-math.cos(math.pi*k/8))for k in range(1,8)]+[(0,1)]
 turned(name,0,0,profile,mat,16);v,f,m=G[name];G[name]=([(c[0]+p[0]*r[0],c[1]+p[1]*r[1],c[2]+p[2]*r[2])for p in v],f,m)
def bent_limb(name,path,radii,mat,n=10):
 v=[]
 for k,p in enumerate(path):
  t=unit(sub(path[min(k+1,len(path)-1)],path[max(k-1,0)]));u=(1,0,0);w=unit(cross(t,u))
  for j in range(n):v.append(add(p,add(mul(u,radii[k][0]*math.cos(math.tau*j/n)),mul(w,radii[k][1]*math.sin(math.tau*j/n)))))
 f=[]
 for k in range(len(path)-1):
  for j in range(n):q=(j+1)%n;a=k*n+j;b=k*n+q;c=(k+1)*n+q;d=(k+1)*n+j;f.extend([(a,b,c),(a,c,d)])
 for k in[0,len(path)-1]:
  c=len(v);v.append(path[k]);base=k*n
  for j in range(n):f.append((c,base+(j+1)%n,base+j)if k==0 else(c,base+j,base+(j+1)%n))
 record(name,v,f,mat)
ysections('WholeLionTorso',[(0,-.52,.70,.12,.18),(0,-.36,.70,.24,.27),(0,-.05,.67,.28,.27),(0,.25,.65,.27,.25),(0,.48,.63,.18,.19),(0,.56,.62,.07,.09)],0)
ysections('WholeRisingFeatherNeckAndEagleSkull',[(0,-.34,.77,.17,.20),(0,-.49,.91,.18,.24),(0,-.57,1.12,.15,.22),(0,-.67,1.34,.18,.17),(0,-.82,1.37,.18,.16),(0,-.94,1.34,.09,.08)],1)
ysections('WholeDownHookedBeak',[(0,-.89,1.34,.075,.070),(0,-1.02,1.33,.09,.075),(0,-1.10,1.25,.055,.075),(0,-1.085,1.17,.012,.014)],2,12)
for side,sg in[('Left',-1),('Right',1)]:
 ovoid(side+'EmbeddedEye',(sg*.164,-.79,1.425),(.034,.041,.034),2)
 # Long bird foreleg and true three-toe ground shape, not four identical lion paws.
 bent_limb(side+'WholeBirdForeleg',[(sg*.17,-.42,.72),(sg*.235,-.49,.39),(sg*.255,-.62,.075)],[(.075,.09),(.042,.05),(.035,.038)],2)
 p=[(-.065,.06),(.065,.06),(.075,-.015),(.13,-.14),(.105,-.18),(.055,-.09),(.038,-.21),(0,-.24),(-.038,-.21),(-.055,-.09),(-.105,-.18),(-.13,-.14),(-.075,-.015)]
 pad(side+'WholeCleftTalonFoot',p,0,.065,2);v,f,m=G[side+'WholeCleftTalonFoot'];G[side+'WholeCleftTalonFoot']=([(sg*.255+x,-.62+z,y)for x,y,z in v],[(a,c,b)for a,b,c in f],m)
 bent_limb(side+'WholeBentLionHindleg',[(sg*.19,.28,.68),(sg*.30,.48,.39),(sg*.30,.35,.075)],[(.13,.15),(.09,.10),(.065,.065)],0)
 # Rounded full rear paws have flat true soles, separate from long split foretoes.
 pp=[(-.09,-.10),(.09,-.10),(.12,-.065),(.12,.06),(.08,.09),(-.08,.09),(-.12,.06),(-.12,-.065)]
 pad(side+'WholeLionGroundPaw',pp,0,.115,0);v,f,m=G[side+'WholeLionGroundPaw'];G[side+'WholeLionGroundPaw']=([(sg*.30+x,.31+z,y)for x,y,z in v],[(a,c,b)for a,b,c in f],m)
 # Thick feather-fan wings: distinct long primary tips, not membrane scallops.
 wing=[(.17,.79),(.33,1.10),(.65,1.37),(1.21,1.65),(1.29,1.56),(1.17,1.25),(1.10,1.40),(1.06,1.09),(.98,1.29),(.91,.96),(.83,1.16),(.76,.86),(.69,1.04),(.60,.78),(.53,.91),(.38,.73)]
 name=side+'WholeFeatherFanWing';pad(name,wing,-.027,.027,1);v,f,m=G[name]
 def wp(x,y,z):return(sg*x,-.17+.28*x+y,z)
 G[name]=([wp(*p)for p in v],[(a,c,b)for a,b,c in f]if sg<0 else f,m)
 # Three distinct layered coverts root fully on the main feather fan.
 for j in range(3):
  x=.29+j*.15;z=.91+j*.12
  feather=[(x,z),(x+.08,z+.14),(x+.43,z+.30),(x+.36,z+.08),(x+.15,z-.04)]
  name=side+'WholeLayeredCovert'+str(j);pad(name,feather,-.045-j*.006,-.018-j*.006,1);v,f,m=G[name];G[name]=([wp(*p)for p in v],[(a,c,b)for a,b,c in f]if sg<0 else f,m)
bent_limb('WholeLongCurvedLionTail',[(0,.48,.65),(0,.77,.53),(0,1.03,.58),(0,1.14,.83),(0,1.12,1.02)],[(.050,.050),(.039,.039),(.028,.028),(.020,.020),(.015,.015)],0,12)
ovoid('WholeTailEndTuft',(0,1.12,1.025),(.055,.065,.09),0)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()};FM={n:[m]*len(f)for n,(v,f,m)in G.items()}
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
focus=Vector((0,0,.83))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.35;aim(cam,(5,-8,3.3));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/magic/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'magic','style':'S01-clean-geometric','title':'Static Hook Beak and Feather Wing Griffin','description':'One newly authored complete stylized griffin character in a fixed four-foot pose. A deep tawny lion torso and two bent rear legs with rounded whole paws combine with a tall ivory feathered neck/skull, a downward hooked beak and two long bird forelegs ending in real cleft three-toe feet. Two entire raised feather-fan wings have projecting primary tips and separate rooted overlapping coverts, not scalloped bat membranes. A long thin curved lion tail ends in a volumetric tuft. Dark lateral eyes are seated into the head. All body sections, head proportions, feather outlines and limbs are newly drawn, not a modified old dragon body with an owl head attached; no old mesh is imported. Three opaque PBR materials, metre Z-up and full horizontal-bounds-centred four-foot ground origin. One static character prop and zero scenes. Fictional game-art appearance only; no biological accuracy, flight, locomotion, physical balance, animal care, manufacture or safety. Rigging, animation, interactions, collision and living functions are not produced or verified.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
