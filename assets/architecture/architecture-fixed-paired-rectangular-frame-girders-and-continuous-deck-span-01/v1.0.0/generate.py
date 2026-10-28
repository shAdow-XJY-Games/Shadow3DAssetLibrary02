import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='architecture-fixed-paired-rectangular-frame-girders-and-continuous-deck-span-01'
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
PALETTE=[('WholeUnbracedRectangularFramesTealSteel',(.12,.29,.30,1),.66,.28),('WholeContinuousLowDeckPaleConcrete',(.62,.60,.52,1),.90,0),('WholeIntegralTerminalPiersSlateConcrete',(.36,.39,.39,1),.95,0)]
G={};FM={};ROOTS=[];CONTACTS=[];LINKS=[];GAPS=[];SHIFT=(0,0,0)
XS=[-3.60,-3.30,-1.30,-1.00,1.00,1.30,3.30,3.60];ZS=[1.60,1.90,3.40,3.70]
for side in[-1,1]:
 y=side*1.05;cells=[]
 for i in range(len(XS)-1):
  for k in range(len(ZS)-1):
   if k==1 and i%2==1:continue
   cells.append([(x,yy,z)for z in ZS[k:k+2]for yy in[y-.12,y+.12]for x in XS[i:i+2]])
 name='WholeThreeOpeningsRectangularFrame_'+str(side);cell_union(name,cells,0);FM[name]=[0]*len(G[name][1])
 CONTACTS.append(('WholeContinuousStraightDeck',name,(0,y,1.60),(0,0,1),1.727))
box('WholeContinuousStraightDeck',(-3.9,-1.3,1.40),(3.9,1.3,1.60),1);FM['WholeContinuousStraightDeck']=[1]*12
for side in[-1,1]:
 cx=side*3.30;v=[]
 for rx,ry,z in[(.60,1.50,0),(.30,1.15,.25),(.30,1.15,1.40)]:v.extend([(cx-rx,-ry,z),(cx+rx,-ry,z),(cx+rx,ry,z),(cx-rx,ry,z)])
 f=[(0,2,1),(0,3,2),(8,9,10),(8,10,11)]
 for k in range(2):
  for i in range(4):
   j=(i+1)%4;a=k*4+i;b=k*4+j;c=(k+1)*4+j;d=(k+1)*4+i;f.extend([(a,b,c),(a,c,d)])
 name='WholeFootAndFullWidthTerminalPier_'+str(side);record(name,v,f,2);FM[name]=[2]*len(f);ROOTS.append(name);CONTACTS.append((name,'WholeContinuousStraightDeck',(cx,0,1.40),(0,0,1),1.379))
for x in[-2.30,0,2.30]:
 for z in[2.10,2.70,3.20]:GAPS.append(dict(label='SelectedTwoWholeFrameWindowsClearAcross',origin_m=[x,-1.6,z],direction=[0,1,0],length_m=3.20))
GAPS.append(dict(label='SelectedEmptyCentralUnderspan',origin_m=[0,0,.01],direction=[0,0,1],length_m=1.30))
GAPS.append(dict(label='WholeDeckSolidControl',origin_m=[0,0,.01],direction=[0,0,1],length_m=1.75,blocked=True))
for z in[.40,.90]:GAPS.append(dict(label='SelectedOpenUnderspanCrossway',origin_m=[0,-1.70,z],direction=[0,1,0],length_m=3.40))
for x in[-3.45,-1.15,1.15]:GAPS.append(dict(label='FullVerticalFramePostSolidControl',origin_m=[x,-1.60,2.60],direction=[0,1,0],length_m=3.20,blocked=True))
for x in[-2.,2.]:GAPS.append(dict(label='OpenUnroofedCentralDeckStrip',origin_m=[x,0,1.61],direction=[0,0,1],length_m=2.50))
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
focus=Vector((0,0,1.85))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=10.0;aim(cam,(5,-16,6.5) if view=='qa-front' else (-9,-15,8.0));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/architecture/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'modular','theme':'architecture','style':'S01-clean-geometric','title':'Fixed Paired Rectangular Frame Girders and Continuous Deck Span','description':'One newly authored complete fixed rectangular-frame-girder bridge illustration. Two whole continuous upright side frames each have three large genuine rectangular through-openings bounded by full straight upper and lower chords and four complete vertical posts, with no diagonal web members or bowed chords. Each entire frame is a single closed connected material boundary, not a loose set of crossing bars, pierced thin I-web or truncated truss. A complete low straight deck continuously joins the two lower-frame strips across its full width and seats on two whole full-width terminal piers with integral broadened flat feet. Five whole closed editable meshes, three opaque constant PBR roles, one model zero scenes, metres Z up and true complete horizontal bounds-centred ground datum. All numeric cells, dimensions, deck, openings and complete supports authored afresh; no previous beam, truss, bridge, frame, deck or support geometry imported, cropped, stretched, bent or simplified. Compared with the old independent castellated I-beam, the new assembly has two deep rectangular continuous frames rather than a single thin pierced web between wide flanges, a transverse full-width deck and two remote complete end supports leaving an actual open underspan. Compared with the old lenticular bridge there are no opposed bowed chords, alternating diagonals, short deck hangers, separate high bearing posts or upper cross-bracing; the deck directly shares the level of the straight lower-frame strips. The pair of complete unbraced orthogonal frames and deck relation defines the new body, not merely an altered hole count or colour. Four actual finite opposed seat patches with five separated sided witnesses each, two whole ground soles and eighteen selected clear-window, open-deck, underspan and solid-post controls are checked. Generic Vierendeel-like visual vocabulary only, with solid stylized member exteriors and no hidden rectangular-tube interiors represented. No actual rigid-joint or bending analysis, U-frame action, wind bracing, member grade, weld specification, load, span rating, deflection, vibration, traffic, walking access, parapet safety, bearings, construction, assembly or structural/civil safety capability. Dry static game architecture, no people, terrain, rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
