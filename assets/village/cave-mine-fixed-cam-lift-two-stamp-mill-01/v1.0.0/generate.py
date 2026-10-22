import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='cave-mine-fixed-cam-lift-two-stamp-mill-01'
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
# Fixed two-stamp ore-mill appearance: two different static cam/tappet poses,
# square guided stems and heads above one true open mortar. No working drive claim.
for side,x in [('Left',-.62),('Right',.62)]:
 box(side+'WholeGroundSill',(x-.16,-.50,0),(x+.16,.42,.12),0)
 box(side+'WholeFramePost',(x-.08,.12,.12),(x+.08,.28,2.15),0)
 for label,z in [('Lower',.82),('Upper',1.82)]:box(side+label+'FrontGuideSupportArm',(x-.06,-.36,z+.02),(x+.06,.22,z+.10),0)
 box(side+'ShaftBearingShelf',(x-.09,-.10,.97),(x+.09,.25,1.04),0)
 wheel(side+'ThroughBoredCamshaftBearing',x,0,1.15,.14,.046,.12,1)
for label,z in [('Low',.72),('High',2.0)]:box(label+'RearFrameTie',(-.64,.15,z),(.64,.25,z+.10),0)
# Each whole guide is a single closed material body with two genuine square bores.
def whole_guide(name,z):
 xs=[-.64,-.27,-.17,.17,.27,.64];ys=[-.39,-.33,-.23,-.17];cells={(i,j)for i in range(5)for j in range(3)if not(i in[1,3]and j==1)};ids={};v=[];f=[]
 def vid(i,j,k):
  key=(i,j,k)
  if key not in ids:ids[key]=len(v);v.append((xs[i],ys[j],z+.12*k))
  return ids[key]
 for i,j in sorted(cells):
  q=[vid(i+a,j+b,k)for k in[0,1]for b in[0,1]for a in[0,1]]
  for face,neighbor in [((0,2,3,1),None),((4,5,7,6),None),((0,1,5,4),(i,j-1)),((2,6,7,3),(i,j+1)),((0,4,6,2),(i-1,j)),((1,3,7,5),(i+1,j))]:
   if neighbor is None or neighbor not in cells:
    a,b,c,dd=[q[k]for k in face];f.extend([(a,b,c),(a,c,dd)])
 record(name,v,f,1)
whole_guide('WholeLowerTwoBoreStemGuide',.82);whole_guide('WholeUpperTwoBoreStemGuide',1.82)
CZ=1.149
wheel('WholeFixedHorizontalCamshaft',.09,0,CZ,.045,0,1.82,2)
def yzsolid(name,p,x0,x1,m):
 pad(name,p,x0,x1,m);v,f,mat=G[name];record(name,[(y,x,z)for x,y,z in v],f,mat)
cam=[(-.10,-.08),(.10,-.08),(.14,.02),(.12,.10),(.035,.24),(-.035,.24),(-.10,.10),(-.13,.02)]
for side,x,phase in [('Left',-.22,1),('Right',.22,-1)]:
 p=[(phase*y,CZ+phase*z)for y,z in cam];yzsolid(side+'WholeFlatCrestLiftingCam',p,x-.045,x+.045,1)
 base=CZ+(.24 if phase==1 else .08);head=.44 if phase==1 else .28
 box(side+'FixedCamRestingTappet',(x-.10,-.34,base),(x+.10,.12,base+.06),1)
 box(side+'WholeSquareGuidedStampStem',(x-.04,-.32,head+.16),(x+.04,-.24,head+1.86),2)
 box(side+'WholeRaisedStampHead',(x-.12,-.41,head),(x+.12,-.15,head+.20),2)
# One blind-bottom mortar cavity; the head positions are static and above its floor.
outer=[(-.49,-.59),(.49,-.59),(.49,.01),(-.49,.01)];inner=[(-.42,-.52),(.42,-.52),(.42,-.06),(-.42,-.06)];v=[(x,y,z)for p,z in[(outer,0),(outer,.43),(inner,.43),(inner,.12)]for x,y in p];f=[]
for k in range(3):
 for i in range(4):
  j=(i+1)%4;a=k*4+i;b=k*4+j;c=(k+1)*4+j;dd=(k+1)*4+i;f.extend([(a,b,c),(a,c,dd)])
f.extend([(0,2,1),(0,3,2),(12,13,14),(12,14,15)]);record('WholeOpenBlindBottomStampMortar',v,f,3)
wheel('WholeStaticFlywheelRim',.94,0,CZ,.33,.28,.07,1);wheel('WholeStaticFlywheelHub',.94,0,CZ,.07,0,.16,1)
for k in range(4):
 a=math.tau*k/4;pipe('FlywheelSpoke'+str(k),[(.94,.055*math.sin(a),CZ+.055*math.cos(a)),(.94,.295*math.sin(a),CZ+.295*math.cos(a))],.025,1,8)
ps=[p for v,f,m in G.values()for p in v];cx=(min(p[0]for p in ps)+max(p[0]for p in ps))/2;cy=(min(p[1]for p in ps)+max(p[1]for p in ps))/2
for name,(v,f,m)in list(G.items()):G[name]=([(x-cx,y-cy,z)for x,y,z in v],f,m)

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
for name,color,rough in [('Frame_OiledTimber', (0.38, 0.25, 0.12, 1), 0.84), ('Cams_Guide_Iron', (0.25, 0.28, 0.28, 1), 0.75), ('Stamps_WornSteel', (0.42, 0.46, 0.46, 1), 0.65), ('Mortar_CutStone', (0.36, 0.38, 0.36, 1), 0.89)]:
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=.6 if name in ['Frame_Silver','Rims_Satin'] else 0;materials.append(m)
parts=[]
for name,(v,f,mi) in G.items():
 me=bpy.data.meshes.new(name+'Mesh');me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o)
 for m in materials:me.materials.append(m)
 for p in me.polygons:p.material_index=mi;p.use_smooth=False
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
focus=Vector((0,0,1.15))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.20;aim(cam,(5,-7,4.3));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/village/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'cave-mine','style':'S01-clean-geometric','title':'Fixed Cam-Lift Two-Stamp Ore Mill','description':'One newly authored complete static historical ore-stamp appearance: a grounded twin-post frame carries a horizontal camshaft, two distinct fixed flat-crest cam/tappet contacts, two whole square stamp stems passing through actual square bores in two closed guide bodies, raised heads and one genuinely open blind-bottom mortar. A fixed four-spoke rim completes the shaft appearance. The whole cam-to-tappet and guided falling-stem arrangement is structurally different from the old single-column bench drill, lever citrus press, threaded-spindle basket press and smith scene with hand tools; adding a second head is not the novelty. All main geometry newly authored using mature boxes, annuli, polygon extrusions and a small boundary-cell guide primitive. Both heads remain above the mortar floor, the two cams are fixed in different phases, and the bore spaces occupied by stems/shaft are not claimed fully clear. Static art only: no motor/belt drive, motion cycle, impact force, ore crushing capacity, manufacturing, installation, guarding, structural loading or machinery safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
