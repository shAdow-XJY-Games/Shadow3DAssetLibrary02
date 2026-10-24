import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='fantasy-fixed-twin-rope-raised-drawbridge-gateway-01'
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

# Complete masonry portal and one fixed raised timber deck with two upper rope routes.
PALETTE=[('PortalWarmStone',(.52,.49,.40,1),.88,0),('DeckDarkTimber',(.32,.20,.10,1),.80,0),('AxlesRopesIron',(.16,.19,.18,1),.56,.44)]
# Two complete grounded jambs and one real annular arch crown; open gate passage retained.
for side in [-1,1]:
 x=side*1.20
 box('WholeJamb_'+str(side),(x-.24,-.27,0),(x+.24,.43,2.20),0)
 box('WholeJambFoot_'+str(side),(x-.32,-.34,0),(x+.32,.50,.16),0)
# Semicircular arch extruded through the same finite wall thickness; no filled gate face.
p=[]
for i in range(17):
 a=math.pi*i/16;p.append((1.44*math.cos(a),2.20+1.44*math.sin(a)))
for i in range(16,-1,-1):
 a=math.pi*i/16;p.append((.96*math.cos(a),2.20+.96*math.sin(a)))
pad('WholeOpenArchCrown',p,-.27,.43,0)
box('WholeRearThreshold',(-.96,.13,.08),(.96,.62,.24),0)
# Single full-width raised deck, transverse root axle and underside cross bracing.
ANG=math.radians(31);P=(0,-.11,.29);D=(0,-math.cos(ANG),math.sin(ANG));PN=(0,math.sin(ANG),math.cos(ANG))
def tr(q):x,t,n=q;return add(P,add((x,0,0),add(mul(D,t),mul(PN,n))))
def transform(name):
 v,f,m=G[name];record(name,[tr(q)for q in v],f,m)
box('WholeRaisedBridgeDeck',(-.90,0,-.07),(.90,2.65,.035),1);transform('WholeRaisedBridgeDeck')
for x in [-.68,.68]:
 n='WholeLongUnderStringer_'+str(x);box(n,(x-.075,.05,-.19),(x+.075,2.55,-.062),1);transform(n)
for t in [.25,2.38]:
 n='WholeUndersideEndTie_'+str(t);box(n,(-.88,t-.065,-.25),(.88,t+.065,-.16),2);transform(n)
pipe('WholeRootPivotAxle',[(-1.14,-.11,.29),(1.14,-.11,.29)],.075,2,16)
for side in [-1,1]:
 x=side*.80
 # Finite deck eye at each outer forward corner, not a floating rope endpoint.
 A=tr((x,2.40,.08));n='WholeDeckRopeLug_'+str(side)
 box(n,(x-.075,2.32,.015),(x+.075,2.49,.13),2);transform(n)
 # Rope crosses a real exposed overhead wheel, then ends in a visible rear weight.
 C=(side*1.08,-.55,2.82);radius=.16
 wheel('WholeHighRopeWheel_'+str(side),*C,.18,.055,.11,2)
 pipe('WholeHighWheelAxle_'+str(side),[(side*.90,-.55,2.82),(side*1.25,-.55,2.82)],.045,2,12)
 # Front run to upper semicircle, then vertical back run, complete one opaque rope mesh.
 pts=[A,(C[0],C[1]-.16,C[2])]
 for i in range(1,9):
  a=math.pi-math.pi*i/8;pts.append((C[0],C[1]+radius*math.cos(a),C[2]+radius*math.sin(a)))
 pts.append((C[0],C[1]+.16,1.12))
 pipe('WholeContinuousUpperRope_'+str(side),pts,.018,2,8)
 # Rear weight is an exterior fixed display, not a calculated counterweight.
 box('WholeRearHangingWeight_'+str(side),(C[0]-.095,C[1]+.075,.73),(C[0]+.095,C[1]+.245,1.13),2)

for side in [-1,1]:
 box('WholeWheelWallBracket_'+str(side),(side*1.08-.10,-.59,2.74),(side*1.08+.10,-.23,2.87),2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
FM={n:[m]*len(f)for n,(v,f,m)in G.items()}
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
focus=Vector((0,0,1.62))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=5.15;aim(cam,(6,-9,6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/fantasy/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'fantasy','style':'S01-clean-geometric','title':'Fixed Twin Rope Raised Drawbridge Gateway','description':'One complete original static fantasy gateway exterior: full grounded stone-look jambs and continuous open semicircular arch, finite rear threshold, one raised thick timber bridge deck with underside stringers and transverse root pivot, two full upper rope paths routed over exposed wheels on finite wall brackets, deck corner lugs and hanging fixed weights. Different from a narrow counterweighted boom or a hydraulic loading deck with independently hinged lip: this complete gate passage is paired with one full-width raised bridge leaf and overhead support routes. No old model geometry imported. Three opaque untextured PBR materials, metre scale, XY-centred ground datum; one complete model and zero scenes. Fixed artistic display only, no moat, host fortification, working lift, rigging, balancing, movement, load, installation, access control or engineering/safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
