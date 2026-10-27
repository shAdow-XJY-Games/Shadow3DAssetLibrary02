import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='architecture-fixed-opposed-bow-lens-frames-and-hung-deck-bridge-01'
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
PALETTE=[('WholeLensChordFramesDeepTeal',(.10,.25,.28,1),.70,.26),('WholeWebMembersAndDeckHangersPaleSteel',(.53,.59,.57,1),.59,.38),('WholeDeckAndTerminalAbutmentsWarmConcrete',(.55,.51,.43,1),.91,0),('WholeBearingPostsAndDeckEdgeBeamsSlate',(.30,.35,.34,1),.80,.15)]
FM={};JOINS=[];ROOTS=[];SPAN=3.45;INNER=3.27
for s in[-1,1]:
 name='WholeTerminalAbutment'+str(s);ROOTS.append(name);box(name,(s*3.45-.43,-1.42,0),(s*3.45+.43,1.42,.60),2)
 for side in[-1,1]:
  n='WholeEndBearingPost'+str(s)+'_'+str(side);box(n,(s*3.45-.16,side*1.12-.145,.54),(s*3.45+.16,side*1.12+.145,1.78),3);JOINS.append((n,name,(s*3.45,side*1.12,.57)))
box('WholeStraightHungDeck',(-3.60,-1.02,.56),(3.60,1.02,.68),2)
for s in[-1,1]:JOINS.append(('WholeStraightHungDeck','WholeTerminalAbutment'+str(s),(s*3.45,0,.58)))
for side in[-1,1]:
 n='WholeStraightDeckEdgeBeam'+str(side);box(n,(-3.55,side*1.08-.12,.53),(3.55,side*1.08+.12,.70),3)
 for s in[-1,1]:JOINS.append((n,'WholeTerminalAbutment'+str(s),(s*3.45,side*1.08,.57)))
 for x in[-2,0,2]:JOINS.append((n,'WholeStraightHungDeck',(x,side*.99,.62)))
# Two complete finite closed lens frames, each containing oppositely bowed upper/lower chord bands and whole joined end noses.
SEG=64
outer=[(SPAN*math.cos(math.tau*i/SEG),1.70+(1.50 if math.sin(math.tau*i/SEG)>=0 else -.85)*math.sin(math.tau*i/SEG)**2)for i in range(SEG)]
inner=[(INNER*math.cos(math.tau*i/SEG),1.70+(1.33 if math.sin(math.tau*i/SEG)>=0 else -.68)*math.sin(math.tau*i/SEG)**2)for i in range(SEG)]
def outline_z(poly,x,upper):
 seq=poly[:SEG//2+1]if upper else poly[SEG//2:]+poly[:1]
 for (a,b),(c,d)in zip(seq,seq[1:]):
  if min(a,c)-1e-10<=x<=max(a,c)+1e-10 and abs(c-a)>1e-10:return b+(d-b)*(x-a)/(c-a)
 raise ValueError((x,upper))
def upper(x):return(outline_z(outer,x,True)+outline_z(inner,x,True))/2
def lower(x):return(outline_z(outer,x,False)+outline_z(inner,x,False))/2
for side in[-1,1]:
 y=side*1.12;n='WholeOpposedBowLensFrame'+str(side);v=[(x,yy,z)for yy in[y-.08,y+.08]for poly in[outer,inner]for x,z in poly];f=[]
 def q(a,b,c,d):f.extend([(a,b,c),(a,c,d)])
 for i in range(SEG):
  j=(i+1)%SEG
  q(i,j,SEG+j,SEG+i);q(2*SEG+i,3*SEG+i,3*SEG+j,2*SEG+j)
  q(i,2*SEG+i,2*SEG+j,j);q(SEG+i,SEG+j,3*SEG+j,3*SEG+i)
 record(n,v,f,0)
 for s in[-1,1]:JOINS.append((n,'WholeEndBearingPost'+str(s)+'_'+str(side),(s*3.36,y,1.70)))
def member(name,a,b,r,m,host_a,host_b):
 t=unit(sub(b,a));pipe(name,[sub(a,mul(t,.025)),add(b,mul(t,.025))],r,m,8);JOINS.extend([(name,host_a,a),(name,host_b,b)])
NODES=[-3.36,-2.52,-1.68,-.84,0,.84,1.68,2.52,3.36]
for side in[-1,1]:
 y=side*1.12;frame='WholeOpposedBowLensFrame'+str(side)
 for k,x in enumerate(NODES[1:-1]):
  member('WholeLensVerticalWeb'+str(side)+'_'+str(k),(x,y,lower(x)),(x,y,upper(x)),.036,1,frame,frame)
  member('WholeLowerChordDeckHanger'+str(side)+'_'+str(k),(x,y,.64),(x,y,lower(x)),.024,1,'WholeStraightDeckEdgeBeam'+str(side),frame)
 for k,(a,b)in enumerate(zip(NODES,NODES[1:])):
  za=1.70 if k==0 else(lower(a)if k%2==0 else upper(a));zb=1.70 if k==7 else(upper(b)if k%2==0 else lower(b))
  member('WholeAlternatingLensDiagonal'+str(side)+'_'+str(k),(a,y,za),(b,y,zb),.028,1,frame,frame)
for k,x in enumerate([-1.68,0,1.68]):member('WholeUpperLensCrossSpreader'+str(k),(x,-1.12,upper(x)),(x,1.12,upper(x)),.042,0,'WholeOpposedBowLensFrame-1','WholeOpposedBowLensFrame1')
for k,(a,b)in enumerate([(-1.68,0),(0,1.68)]):member('WholeUpperLateralDiagonal'+str(k),(a,-1.12,upper(a)),(b,1.12,upper(b)),.028,1,'WholeOpposedBowLensFrame-1','WholeOpposedBowLensFrame1')
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
for n,(v,f,m)in G.items():FM.setdefault(n,[m]*len(f))
JOINS=[(a,b,sub(p,SHIFT))for a,b,p in JOINS]
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
focus=Vector((0,0,1.55))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=9.4;aim(cam,(5,-16,7.8) if view=='qa-front' else (-6,-17,8.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/architecture/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'modular','theme':'architecture','style':'S01-clean-geometric','title':'Fixed Opposed Bow Lens Frames and Hung Deck Bridge','description':'One wholly newly authored complete dry lenticular-truss-inspired bridge module. Two full finite lens-shaped side frames each combine an upward-bowed upper chord and downward-bowed lower chord into joined common end noses; the curved lower chord is not the straight deck edge or a low horizontal tie. Seven full vertical web members and eight alternating diagonals fill each lens with a real open lattice. A complete straight low deck and two edge beams hang below the two curved lower chords on fourteen whole short rods. Two terminal abutments carry four complete separate outboard bearing posts at the lens ends, leaving the central deck clear between those posts. Three full upper cross-spreaders and two lateral diagonals link the opposing frames. Unlike the earlier tied-arch bridge, both principal chords curve in opposite directions, the lower chord stays independently above the straight deck, and there is a braced web between both curved chords rather than only long vertical hangers from an upper bow to a straight tie beam. Unlike the sagging-ribbon bridge, the deck remains level and is not the principal sagging tension member; there are no towers, main overhead cables or outer cable anchors. All frame contours, deck, web members, hangers and supports newly authored together; no earlier arch, cable, truss or deck mesh imported, bent or extracted. Four opaque constant untextured PBR roles, metres native Z up and full horizontal bounds-centred terminal soles, one architectural model zero scenes. Generic fixed architectural art only, not a named historic bridge reconstruction or an engineering design. No force equilibrium, pin-joint design, buckling resistance, tension, arch thrust, fatigue, dynamic response, load, traffic, pedestrian access, navigation clearance, construction, installation or civil safety capability made or verified. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
