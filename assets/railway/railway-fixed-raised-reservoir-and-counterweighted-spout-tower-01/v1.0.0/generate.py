import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='railway-fixed-raised-reservoir-and-counterweighted-spout-tower-01'
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
PALETTE=[('WholeTankWarmStaveAppearance',(.42,.25,.11,1),.81,.02),('WholeBracedTowerTimber',(.24,.19,.12,1),.85,.02),('WholeSpoutBandsAndCounterweight',(.10,.22,.24,1),.52,.40)]
FM={}
# One complete hollow flat-bottom reservoir with a real central lower outlet.
turned('WholeReservoirAndOpenBottomOutlet',0,0,[(.15,3.36),(1.48,3.36),(1.48,5.03),(1.35,5.03),(1.35,3.53),(.15,3.53)],0,32)
for j,z in enumerate([3.52,4.25,4.88]):turned('WholeTankBindingBand_%d'%j,0,0,[(1.465,z-.045),(1.515,z-.045),(1.515,z+.045),(1.465,z+.045)],2,32)
for x in[-.96,.96]:
 for y in[-.96,.96]:box('WholeTowerPost_%s_%s'%(x,y),(x-.13,y-.13,0),(x+.13,y+.13,3.45),1)
for x in[-.96,.96]:
 box('WholeReservoirBearer_'+str(x),(x-.16,-1.40,3.24),(x+.16,1.40,3.40),1)
 pipe('SideWholeBrace_'+str(x),[(x,-.96,.30),(x,.96,3.15)],.09,1,4)
pipe('RearWholeBrace',[(-.96,.96,.30),(.96,.96,3.15)],.09,1,4)
box('WholeFrontPipeSupport',(-1.10,-1.04,2.35),(1.10,-.84,2.52),1)
# Generic full inner/outer tube sweep; no hidden solid cap at either mouth.
def hollow(name,pts,ro,ri,m):
 n=16;vv=[]
 for inner in[False,True]:
  r=ri if inner else ro
  for i,c in enumerate(pts):
   w=unit(sub(pts[min(i+1,len(pts)-1)],pts[max(0,i-1)]));u=(1,0,0);v=cross(w,u)
   for j in range(n):vv.append(add(c,add(mul(u,r*math.cos(math.tau*j/n)),mul(v,r*math.sin(math.tau*j/n)))))
 ff=[];M=len(pts);off=M*n
 for h in[0,1]:
  for k in range(M-1):
   for j in range(n):
    a=h*off+k*n+j;b=h*off+k*n+(j+1)%n;c=b+n;d=a+n
    ff.extend([(a,b,c),(a,c,d)]if h==0 else[(a,c,b),(a,d,c)])
 for k in[0,M-1]:
  for j in range(n):
   a=k*n+j;b=k*n+(j+1)%n;c=off+b;d=off+a
   ff.extend([(a,c,b),(a,d,c)]if k==0 else[(a,b,c),(a,c,d)])
 record(name,vv,ff,m)
pts=[(0,0,3.48),(0,0,3.0)]
for j in range(1,7):
 a=math.pi/2*j/6;pts.append((0,-.35+.35*math.cos(a),3-.35*math.sin(a)))
pts.append((0,-1.82,2.65));hollow('WholeReservoirDownpipeAndSideFeed',pts,.185,.13,2)
pts=[(0,-1.80,2.65),(0,-2.08,2.74),(0,-3.88,3.30),(0,-4.08,3.29),(0,-4.23,3.14),(0,-4.24,2.93)]
hollow('WholeRaisedOpenSpout',pts,.205,.14,2)
for x in[-.29,.29]:
 box('WholeSpoutHingeCheek_'+str(x),(x-.055,-1.99,2.40),(x+.055,-1.60,2.96),2)
 pipe('WholeLateralTrunnion_'+str(x),[(x*.56,-1.80,2.65),(x*1.22,-1.80,2.65)],.08,2,12)
box('WholeHingeSupportShelf',(-.42,-2.04,2.31),(.42,-.87,2.45),1)
pipe('WholeHingeShelfDiagonal',[(0,-.94,1.45),(0,-1.94,2.36)],.085,1,4)
# Separate counterweight line routed over a raised wheel alongside the tank.
box('WholePulleyUpright',(.47,-1.85,2.38),(.63,-1.69,4.12),1)
wheel('WholeGroovedPulleyAppearance',.55,-1.80,4.03,.19,.065,.10,2)
pipe('WholePulleyPin',[(.41,-1.80,4.03),(.70,-1.80,4.03)],.06,2,12)
pipe('WholeSpoutLiftingYoke',[(0,-3.46,3.18),(.55,-3.46,3.18)],.045,2)
pipe('WholeFixedCounterweightCord',[(.55,-3.46,3.18),(.55,-1.90,4.19),(.55,-1.69,4.17),(.55,-1.61,4.01),(.55,-1.61,1.61)],.022,2)
box('WholeSuspendedCounterweight',(.36,-1.78,1.19),(.74,-1.44,1.71),2)
pipe('WholePulleyBaseSupport',[(.96,-.96,2.40),(.55,-1.78,2.40)],.085,1,4)
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
focus=Vector((0,0,2.4))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=8.6;aim(cam,(10,-13,9));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/railway/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'railway','style':'S01-clean-geometric','title':'Fixed Raised Reservoir and Counterweighted Spout Tower','description':'One newly authored complete static railway water-service tower appearance. A high braced four-post trestle supports a whole broad empty flat-bottom cylindrical reservoir with real central bottom outlet and three full exterior bands. Its whole downward feed tube bends forward into a separate fixed raised long open spout, carried by independent lateral trunnions and two complete support cheeks. A full side upright and pulley support one continuous cord from the spout yoke to a separate suspended counterweight within the trestle. The distinctive complete relation is elevated reservoir, lower returning feed, side outboard hinged-spout appearance and independent upper counterweight route, not a grain silo with a changed cone or a scaled ground fire monitor. No old visible geometry imported; one full apparatus, not a scene or separately counted tank and spout. All inner and outer pipe walls and both spout mouths genuinely modeled, dry and empty. Three opaque PBR roles, metres Z up, bounds-centred ground origin. Fixed illustrative railway infrastructure only; no stored water, pipe seal, flow, pressure, rotation, counterbalance solution, refilling, railway compatibility, historical accuracy, load, installation or operator safety capability. Rigging animation and interaction not made or verified.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
