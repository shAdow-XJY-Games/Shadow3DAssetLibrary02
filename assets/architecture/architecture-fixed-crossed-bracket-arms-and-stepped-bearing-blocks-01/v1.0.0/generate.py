import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='architecture-fixed-crossed-bracket-arms-and-stepped-bearing-blocks-01'
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
PALETTE=[('ColumnWarmReddishTimber',(.38,.19,.085,1),.84,0),('WholeCurvedArmsAndTerminalRailsDarkTimber',(.30,.13,.055,1),.86,0),('WholeSteppedBearingBlocksGoldenTimber',(.53,.32,.14,1),.87,0),('WholeStoneGroundPlinth',(.46,.47,.42,1),.94,0)]
FM={};CONTACTS=[];ROOTS=['WholeSquareGroundPlinth']
box(ROOTS[0],(-.65,-.65,0),(.65,.65,.20),3)
turned('WholeTaperedSixteenSidedColumn',0,0,[(0,.20),(.26,.20),(.23,2.45),(0,2.45)],0,16)
CONTACTS.append((ROOTS[0],'WholeTaperedSixteenSidedColumn',(0,0,.20),.18))
def flared_block(name,x,y,z0,zneck,z1,bx,by,tx,ty):
 rings=[(z0,bx,by),(zneck,bx,by),(z1,tx,ty)];v=[(x+xx,y+yy,z)for z,hx,hy in rings for xx,yy in[(-hx,-hy),(hx,-hy),(hx,hy),(-hx,hy)]];f=[(0,2,1),(0,3,2),(8,9,10),(8,10,11)]
 for k in range(2):
  for i in range(4):
   j=(i+1)%4;a=k*4+i;b=k*4+j;c=(k+1)*4+j;d=(k+1)*4+i;f.extend([(a,b,c),(a,c,d)])
 record(name,v,f,2)
flared_block('WholeFlaredColumnHeadBlock',0,0,2.45,2.53,2.72,.30,.30,.55,.55)
CONTACTS.append(('WholeTaperedSixteenSidedColumn','WholeFlaredColumnHeadBlock',(0,0,2.45),.14))
def bracket_arm(name,along,centre,lower,top,seat,centres,half_notch,half_width):
 # Full continuous curved underside with complete rectangular shallow top seats, one closed whole arm.
 L=lower[-1][0];poly=list(lower)+[(L,top)]
 for c in sorted(centres,reverse=True):poly.extend([(c+half_notch,top),(c+half_notch,seat),(c-half_notch,seat),(c-half_notch,top)])
 poly.append((-L,top));pad(name,poly,-half_width,half_width,1);v,f,m=G.pop(name)
 record(name,[(x,y+centre,z)if along==0 else(y+centre,x,z)for x,y,z in v],f,m)
primary='WholeLongitudinalCurvedThreeSeatBracketArm'
bracket_arm(primary,1,0,[(-2,3.00),(-1.6,2.96),(-1.2,2.88),(-.8,2.78),(-.45,2.72),(.45,2.72),(.8,2.78),(1.2,2.88),(1.6,2.96),(2,3.00)],3.18,3.12,[-1.55,0,1.55],.22,.20)
CONTACTS.append(('WholeFlaredColumnHeadBlock',primary,(0,0,2.72),.30))
for k,y in enumerate([-1.55,0,1.55]):
 n='WholePrimarySteppedBearingBlock'+str(k);flared_block(n,0,y,3.12,3.22,3.40,.21,.17,.34,.26);CONTACTS.append((primary,n,(0,y,3.12),.12))
 arm='WholeTransverseCurvedTwoSeatBracketArm'+str(k)
 bracket_arm(arm,0,y,[(-1.4,3.64),(-1.1,3.59),(-.75,3.50),(-.35,3.40),(.35,3.40),(.75,3.50),(1.1,3.59),(1.4,3.64)],3.85,3.80,[-1.05,1.05],.18,.18)
 CONTACTS.append((n,arm,(0,y,3.40),.23))
 for side,x in enumerate([-1.05,1.05]):
  b='WholeTerminalSteppedBearingBlock'+str(k)+str(side);flared_block(b,x,y,3.80,3.90,4.08,.13,.18,.21,.25);CONTACTS.append((arm,b,(x,y,3.80),.09))
  CONTACTS.append((b,'WholeLongitudinalTerminalRail'+str(side),(x,y,4.08),.17))
for side,x in enumerate([-1.05,1.05]):box('WholeLongitudinalTerminalRail'+str(side),(x-.18,-2.05,4.08),(x+.18,2.05,4.32),1)
for n,(v,f,m)in G.items():FM[n]=[m]*len(f)
SHIFT=(0,0,0)
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
focus=Vector((0,0,2.20))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=6.4;aim(cam,(7,-11,6.5) if view=='qa-front' else (-8,-11,7.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/architecture/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'prop','theme':'architecture','style':'S01-clean-geometric','title':'Fixed Crossed Bracket Arms and Stepped Bearing Blocks','description':'One wholly newly authored complete stepped cross-bracket column-head display from grounded stone plinth to two finished full-length upper bearing rails. A whole tapered timber column supports a separate complete flared head block. One entire long curved-underface longitudinal bracket arm has three genuinely shallow bounded top seats, each carrying a whole necked-and-flared bearing block. Three complete transverse curved-underface arms rest on those blocks and contain two upper seats apiece. Six separate whole stepped terminal blocks support two complete longitudinal upper rails. All four arms are entire continuous closed timbers with real underside profiles, finite end faces and full notch floors and walls; the nine bearing blocks each have complete lower necks and upper flared shoulders. Twenty-one actual opposed horizontal contact patches and sided interior witnesses form a connected static seating graph to the complete bottom sole. Unlike the old diagonal two-tier branching column, support spreads by perpendicular flat-seated bracket arms and intermediary stepped blocks, not sloping rods or fork collars. Unlike the nine alternating crossed courses of a timber crib, this is one complete column-head hierarchy of curved cantilever-like arms, localized notch seats and flared blocks, not repeated full-length rectangular wall courses. Every numerical surface newly authored together; no old column, timber, bracket, joint or bearing mesh imported, cropped or transformed. Eighteen editable complete closed material solids, four opaque constant untextured PBR roles, metre-style native Z up and whole horizontal bounds-centred ground datum, one model zero scenes. Broad timber bracket-set category inspired by Chinese timber-framed architectural craftsmanship only; not a replica of a named historic building, historic measured drawing, particular traditional order or standardized joint. The finished upper rails are display terminals with no roof or host building supplied. Shallow seats and static contacts are artistic assembly evidence, not complete tenon joints, restraints, structural connections or manufacturing instructions. No historic authenticity, seismic resistance, real load distribution, stiffness, strength, stability, roof compatibility, timber properties, preservation advice, assembly procedure, manufacture, installation or building safety capability made or verified. No textures, animation, rigging or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
