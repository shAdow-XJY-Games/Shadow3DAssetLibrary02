import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='fantasy-static-open-ribcage-and-two-leg-skeleton-01'
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
PALETTE=[('WholeFictionalBonesWarmIvory',(.71,.66,.52,1),.86,0),('WholeOrbitalInnerShadow',(.24,.23,.19,1),.95,0),('WholeDedicatedLowBaseBronze',(.12,.18,.18,1),.74,.24)]
FM={}
def bone(name,a,b,r):
 w=unit(sub(b,a));u=unit(cross(w,(0,1,0)));v0=cross(w,u);v=[];f=[];nn=10
 ts=[0,.08,.24,.76,.92,1];rs=[1.05,1.35,.75,.75,1.35,1.05]
 for t,sc in zip(ts,rs):
  p=add(a,mul(sub(b,a),t))
  for j in range(nn):v.append(add(p,add(mul(u,r*sc*math.cos(math.tau*j/nn)),mul(v0,r*sc*math.sin(math.tau*j/nn)))))
 for k in range(len(ts)-1):
  for j in range(nn):q=(j+1)%nn;aa=k*nn+j;bb=k*nn+q;f.extend([(aa,bb,bb+nn),(aa,bb+nn,aa+nn)])
 for k,p in[(0,a),(len(ts)-1,b)]:
  c=len(v);v.append(p)
  for j in range(nn):q=(j+1)%nn;f.append((c,k*nn+q,k*nn+j)if k==0 else(c,k*nn+j,k*nn+q))
 record(name,v,f,0)
# Whole hollow cranium has two actual front orbits, one nose opening and an open lower jaw gap.
rows=[(1.54,.105,.105),(1.575,.14,.12),(1.615,.165,.135),(1.635,.17,.14),(1.725,.18,.145),(1.80,.16,.132),(1.855,.10,.085),(1.88,.025,.024)]
n=32;outer=[];inner=[]
for z,rx,ry in rows:
 for j in range(n):
  a=math.tau*j/n;outer.append((rx*math.cos(a),ry*math.sin(a),z));inner.append(((rx-.016)*math.cos(a),(ry-.016)*math.sin(a),z-.006))
outer.append((0,0,1.891));inner.append((0,0,1.872));top=len(outer)-1;holes={(3,j)for j in[20,21,22,25,26,27]}|{(1,j)for j in[23,24]};outerf=[]
for k in range(len(rows)-1):
 for j in range(n):
  if(k,j)in holes:continue
  a=k*n+j;b=k*n+(j+1)%n;c=b+n;d=a+n;outerf.extend([(a,b,c),(a,c,d)])
for j in range(n):outerf.append(((len(rows)-1)*n+j,(len(rows)-1)*n+(j+1)%n,top))
v=outer+inner;off=len(outer);f=list(outerf)+[tuple(off+x for x in reversed(t))for t in outerf];mats=[0]*len(outerf)+[1]*len(outerf);edges={}
for t in outerf:
 for a,b in zip(t,t[1:]+t[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((a,b))
for occ in edges.values():
 if len(occ)==1:
  a,b=occ[0];f.extend([(a,off+a,off+b),(a,off+b,b)]);mats.extend([0,0])
record('WholeHollowSkullWithTwoOrbitsAndNose',v,f,0);FM['WholeHollowSkullWithTwoOrbitsAndNose']=mats
# A complete thick U-shaped lower jaw, distinct from the open mouth gap.
pad('WholeOpenLowerJaw',[(-.145,1.60),(-.12,1.60),(-.105,1.49),(.105,1.49),(.12,1.60),(.145,1.60),(.135,1.46),(-.135,1.46)],-.125,-.080,0)
for j in range(6):
 x=-.080+j*.032;box('WholeUpperBluntTooth'+str(j),(x-.011,-.119,1.532),(x+.011,-.086,1.574),0)
# Vertical joint-swollen spine and a genuinely open short pelvic ring.
for j in range(9):bone('WholeSpineSection'+str(j),(0,.075,.91+j*.071),(0,.075,.995+j*.071),.027)
N=24
wheel('WholeOpenPelvis',0,0,.94,.18,.108,.11,0)
v,f,m=G['WholeOpenPelvis'];G['WholeOpenPelvis']=([(y,x,z*.65+.94*.35)for x,y,z in v],[(a,c,b)for a,b,c in f],m)
# Five upright stacked left/right rib arches, full 3D open thorax.
for k,z in enumerate([1.14,1.20,1.26,1.32,1.38]):
 width=[.16,.19,.22,.23,.205][k]
 for sg in[-1,1]:
  pts=[(0,.075,z+.035),(sg*width*.70,.07,z+.035),(sg*width,.005,z+.006),(sg*width*.78,-.115,z-.015),(sg*.025,-.15,z-.028)];v=[];f=[];nn=8
  for i,p in enumerate(pts):
   aa=pts[max(0,i-1)];bb=pts[min(len(pts)-1,i+1)];dx=bb[0]-aa[0];dy=bb[1]-aa[1];le=math.hypot(dx,dy)
   for j in range(nn):a=math.tau*j/nn;v.append((p[0]+.014*dy/le*math.cos(a),p[1]-.014*dx/le*math.cos(a),p[2]+.014*math.sin(a)))
  for i in range(len(pts)-1):
   for j in range(nn):q=(j+1)%nn;a=i*nn+j;b=i*nn+q;f.extend([(a,b,b+nn),(a,b+nn,a+nn)])
  for i in[0,len(pts)-1]:
   c=len(v);v.append(pts[i])
   for j in range(nn):q=(j+1)%nn;f.append((c,i*nn+q,i*nn+j)if i==0 else(c,i*nn+j,i*nn+q))
  record('WholeRib'+str(k)+'_'+str(sg),v,f,0)
bone('WholeFrontSternum',(0,-.15,1.10),(0,-.15,1.40),.020)
for sg,side in[(-1,'Left'),(1,'Right')]:
 bone(side+'WholeClavicle',(0,.015,1.43),(sg*.245,.00,1.40),.025)
 bone(side+'WholeUpperArm',(sg*.245,0,1.40),(sg*.34,.015,1.13),.030)
 bone(side+'WholeForearm',(sg*.34,.015,1.13),(sg*.365,-.05,.88),.024)
 bone(side+'WholePalm',(sg*.365,-.05,.89),(sg*.375,-.065,.81),.032)
 for j in range(3):bone(side+'WholeBluntFinger'+str(j),(sg*(.348+j*.028),-.07,.825),(sg*(.35+j*.029),-.08,.735),.009)
 bone(side+'WholeFemur',(sg*.135,0,.94),(sg*.18,.015,.55),.038)
 bone(side+'WholeShin',(sg*.18,.015,.55),(sg*.19,-.015,.15),.028)
 pad(side+'WholeBroadForefoot',[(sg*.19-.055,.04),(sg*.19+.055,.04),(sg*.19+.055,.08),(sg*.19+.04,.16),(sg*.19-.04,.16)],-.19,.045,0)
box('WholeDedicatedLowPlinth',(-.31,-.27,0),(.31,.15,.042),2)
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
focus=Vector((0,0,.95))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.20;aim(cam,(2.6,-8,3.1));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/magic/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'magic','style':'S01-clean-geometric','title':'Static Open Ribcage and Two Leg Skeleton','description':'One complete newly authored fictional standing biped skeleton on a dedicated low plinth. A vertically joint-swollen spine connects a short open pelvic ring, stacked paired three-dimensional rib arches and front sternum, narrow neck and hollow cranium. Two actual forward eye orbits and a smaller nose opening pierce the thick skull shell; a complete U-shaped lower jaw leaves a real mouth gap below the blunt upper tooth silhouettes. Two full arm chains terminate in simplified hands, while two full long leg chains end in broad finite forefeet on the low base. All poses, sections, skull shell and rib paths newly authored, not the existing quadruped skeleton rotated upright, a centaur trimmed, or old fish ribs multiplied. Three opaque PBR materials, metres Z-up and horizontal complete-envelope centred ground origin, one whole static fantasy figure zero scenes. Fictional non-gory art only: no real human anatomical fidelity, actual bone count, medical, scientific or educational accuracy, balance, gait, articulation, rig, animation, collision or safety claim. No weapon, blood, injury or separately counted bones.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
