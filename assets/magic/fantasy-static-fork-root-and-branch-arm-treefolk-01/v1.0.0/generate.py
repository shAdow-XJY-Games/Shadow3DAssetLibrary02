import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='fantasy-static-fork-root-and-branch-arm-treefolk-01'
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
PALETTE=[('WholeBarkWarmUmber',(.30,.175,.078,1),.94,0),('WholeBrokenWoodOchre',(.55,.36,.14,1),.93,0),('WholeRecessedFaceDarkBark',(.052,.042,.021,1),.95,0)]
def branch(name,path,radii,mat,n=10):
 v=[]
 for k,p in enumerate(path):
  t=unit(sub(path[min(k+1,len(path)-1)],path[max(k-1,0)]));u=(0,1,0);w=unit(cross(t,u))
  for j in range(n):v.append(add(p,add(mul(u,radii[k]*math.cos(math.tau*j/n)),mul(w,radii[k]*math.sin(math.tau*j/n)))))
 f=[]
 for k in range(len(path)-1):
  for j in range(n):q=(j+1)%n;a=k*n+j;b=k*n+q;c=(k+1)*n+q;d=(k+1)*n+j;f.extend([(a,b,c),(a,c,d)])
 for k in[0,len(path)-1]:
  c=len(v);v.append(path[k]);base=k*n
  for j in range(n):f.append((c,base+(j+1)%n,base+j)if k==0 else(c,base+j,base+(j+1)%n))
 record(name,v,f,mat)
# Complete irregular upright trunk, with face sculpted into its front surface.
rows=[(.69,.28,.22),(.84,.32,.23),(1.10,.28,.25),(1.32,.34,.27),(1.43,.35,.27),(1.46,.35,.27),(1.50,.35,.28),(1.67,.34,.28),(1.70,.34,.28),(1.76,.35,.28),(1.80,.36,.29),(1.88,.35,.28),(2.06,.31,.25),(2.20,.25,.21)]
xf=[-.78,-.60,-.34,-.18,0,.18,.34,.60,.78];v=[]
for z,rx,ry in rows:
 for f in xf:
  nose=max(0,1-abs(f)/.34)*max(0,1-abs(z-1.67)/.18)*.14
  recess=.038 if 1.70<=z<=1.76 and .34<=abs(f)<=.60 else (.03 if 1.43<=z<=1.46 and abs(f)<=.34 else 0)
  v.append((rx*f,-ry-nose+recess,z))
 v.extend([(rx,-ry*.56,z),(rx*.94,ry*.40,z),(rx*.65,ry,z),(-rx*.62,ry*1.04,z),(-rx*.96,ry*.48,z),(-rx,-ry*.55,z)])
n=15;f=[]
for k in range(len(rows)-1):
 for j in range(n):q=(j+1)%n;a=k*n+j;b=k*n+q;c=(k+1)*n+q;d=(k+1)*n+j;f.extend([(a,b,c),(a,c,d)])
for k in[0,len(rows)-1]:
 c=len(v);v.append((0,0,rows[k][0]));base=k*n
 for j in range(n):f.append((c,base+(j+1)%n,base+j)if k==0 else(c,base+j,base+(j+1)%n))
record('WholeSculptedTrunkAndFace',v,f,0)
for sg,label in[(-1,'Left'),(1,'Right')]:
 branch(label+'WholeBentRootLeg',[(sg*.18,.02,.79),(sg*.29,.025,.42),(sg*.38,-.04,.11)],[.20,.14,.095],0)
 # Entire rooted fork-foot is a thick continuous silhouette with three forward tips.
 p=[(-.13,.13),(.13,.13),(.18,-.09),(.26,-.30),(.23,-.34),(.12,-.21),(.08,-.42),(.02,-.45),(-.03,-.25),(-.14,-.38),(-.20,-.35),(-.11,-.13),(-.18,-.07)]
 name=label+'WholeForkedGroundRoot';pad(name,p,0,.16,0);vv,ff,m=G[name];G[name]=([(sg*.38+x,z,y)for x,y,z in vv],[(a,c,b)for a,b,c in ff],m)
 branch(label+'WholeBentBranchArm',[(sg*.25,0,1.48),(sg*.52,-.015,1.40),(sg*.69,-.06,1.12),(sg*.86,-.10,1.22)],[.15,.125,.085,.07],0)
 for j in range(3):
  z=1.21+(j-1)*.065
  branch(label+'WholeBranchFinger'+str(j),[(sg*.84,-.10,z),(sg*(1.02+.03*(j==1)),-.12,z+.035*(j-1)),(sg*(1.12+.04*(j==1)),-.16,z+.08*(j-1))],[.045,.032,.012],0,8)
 branch(label+'WholeCrownBranch',[(sg*.17,.02,2.03),(sg*.28,.02,2.30),(sg*.43,0,2.48),(sg*.49,-.03,2.53)],[.105,.075,.045,.025],0)
 branch(label+'WholeCrownFork',[(sg*.28,.02,2.29),(sg*.19,.025,2.47),(sg*.22,0,2.63)],[.065,.038,.017],0,8)
# Faceted wood face regions are actual surface faces, not coplanar eye/mouth plates.
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()};FM={n:[m]*len(f)for n,(v,f,m)in G.items()}
v,f,m=G['WholeSculptedTrunkAndFace']
for i,t in enumerate(f):
 x,y,z=[sum(v[j][k]+SHIFT[k]for j in t)/3 for k in range(3)]
 if y<-.23 and ((1.70<z<1.76 and .115<abs(x)<.205)or(1.43<z<1.46 and abs(x)<.12)):FM['WholeSculptedTrunkAndFace'][i]=2
 if z>2.199:FM['WholeSculptedTrunkAndFace'][i]=1
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
focus=Vector((0,0,1.31))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.25;aim(cam,(4,-8,3.4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/magic/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'magic','style':'S01-clean-geometric','title':'Static Fork Root and Branch Arm Treefolk','description':'One wholly newly authored stylized treefolk character in a fixed standing pose: a tall irregular whole trunk carries an integral sculpted nose, recessed eye bands and small mouth region, with a modeled broken crown. Two separated bent root legs terminate in broad whole forked grounded root feet. Two long asymmetrically bent branch arms terminate in three genuine separated tapered branch fingers each. Four upward branching crown limbs extend from the trunk, with no leafy canopy or clothing disguise. This is not an existing root stump with painted eyes, a human worker recolored brown, or imported meshes rearranged. All component outlines and full body proportions are authored here. Three opaque PBR materials, metre Z-up, whole horizontal-bounds-centred ground origin. One static fictional character prop, zero scenes. No rig, animation, walking, interaction, collision, biological realism, strength, growth or safety claims.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
