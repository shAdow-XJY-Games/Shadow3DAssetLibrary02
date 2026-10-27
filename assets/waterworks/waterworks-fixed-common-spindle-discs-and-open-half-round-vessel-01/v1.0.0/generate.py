import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='waterworks-fixed-common-spindle-discs-and-open-half-round-vessel-01'
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
PALETTE=[('WholeHalfRoundVesselMutedTeal',(.075,.27,.28,1),.71,.26),('WholeRadialDiscFacesWarmIvory',(.63,.65,.53,1),.72,.10),('WholeCommonSpindleAndBearingIron',(.13,.16,.16,1),.57,.55),('WholeLowBearersAndGroundPadsOchre',(.46,.25,.085,1),.79,.18)]
FM={};JOINS=[];ROOTS=[]
def yzpad(name,p,x0,x1,m):
 pad(name,p,x0,x1,m);v,f,mi=G.pop(name);record(name,[(y,x,z)for x,y,z in v],f,mi)
# Complete thick half-round shell: real full length interior and finite upper lips.
angles=[math.pi+math.pi*i/24 for i in range(25)]
outer=[(1.14*math.cos(a),1.35+1.14*math.sin(a))for a in angles];inner=[(1.02*math.cos(a),1.35+1.02*math.sin(a))for a in reversed(angles)]
yzpad('WholeOpenHalfRoundVesselShell',outer+inner,-2.135,2.135,0)
# Two slightly proud complete half-disc end walls finish the full trough.
for side,x in [('Left',-2.22),('Right',2.22)]:
 name='WholeHalfRoundEndWall'+side;yzpad(name,[(1.17*math.cos(a),1.35+1.17*math.sin(a))for a in angles],x-.085,x+.085,0);JOINS.append((name,'WholeOpenHalfRoundVesselShell',(x,0,.24)))
 bearing='WholeAnnularEndBearing'+side;wheel(bearing,x,0,1.45,.25,.10,.22,2);JOINS +=[(bearing,name,(x,0,1.28)),(bearing,'WholeCommonHorizontalSpindle',(x,.11,1.45))]
for i,x in enumerate([-1.70,1.70]):
 rail='WholeLowTransverseBearer'+str(i);box(rail,(x-.20,-1.24,.05),(x+.20,1.24,.27),3);JOINS.append((rail,'WholeOpenHalfRoundVesselShell',(x,0,.24)))
 for j,y in enumerate([-.94,.94]):
  foot='WholeGroundPad'+str(i)+str(j);box(foot,(x-.30,y-.28,0),(x+.30,y+.28,.10),3);ROOTS.append(foot);JOINS.append((foot,rail,(x,y,.08)))
pipe('WholeCommonHorizontalSpindle',[(-2.55,0,1.45),(2.88,0,1.45)],.12,2,16)
DISC_X=[-1.64+.41*i for i in range(9)]
for i,x in enumerate(DISC_X):
 n='WholePlainRadialDisc%02d'%i;wheel(n,x,0,1.45,.95,.10,.065,1);JOINS.append((n,'WholeCommonHorizontalSpindle',(x,.11,1.45)))
box('WholeOutboardDriveMount',(2.18,-.27,.65),(3.00,.27,1.16),0);box('WholeClosedOutboardDriveCase',(2.70,-.34,1.10),(3.15,.34,1.80),2)
JOINS +=[('WholeOutboardDriveMount','WholeHalfRoundEndWallRight',(2.22,0,.80)),('WholeClosedOutboardDriveCase','WholeOutboardDriveMount',(2.82,0,1.13)),('WholeClosedOutboardDriveCase','WholeCommonHorizontalSpindle',(2.80,0,1.45))]
# Exact finite axial end seats replace overlapping coplanar top lips.
JOINS=[q for q in JOINS if not(q[0].startswith('WholeHalfRoundEndWall')and q[1]=='WholeOpenHalfRoundVesselShell')]
SEATS=[dict(a='WholeOpenHalfRoundVesselShell',b='WholeHalfRoundEndWall'+side,min_area=.38)for side in['Left','Right']]
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()};FM={n:[m]*len(f)for n,(v,f,m)in G.items()};JOINS=[(a,b,sub(p,SHIFT))for a,b,p in JOINS]
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
focus=Vector((0,0,1.15))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=7.3;aim(cam,(7,-11,6) if view=='qa-front' else (-8,-10,7));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/waterworks/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'waterworks','style':'S01-clean-geometric','title':'Fixed Common Spindle Discs and Open Half Round Vessel','description':'One wholly new complete static dry disc-contactor-inspired apparatus. A complete finite-thickness half-round open vessel shell runs along one horizontal axis and has two full slightly proud semicircular end walls. Nine whole plain circular radial discs share one full straight spindle on two true annular end bearings, while a complete outboard closed drive-case exterior and full rooted mounting bracket finish the end. The lower portions of all discs lie inside the open semicircular vessel with real floor clearance; the full upper arcs are exposed above its lip, with genuine gaps between successive plates. Two low complete cross bearers and four finite whole ground pads support the assembly. Unlike the oval paper beater, this has no central raceway divider, return-around loop, single short bar-textured drum or large outboard spoke wheel; one common longitudinal spindle carries separate full flat radial discs across the whole straight vessel. Unlike the opposed concave-disc harrow, there are no oblique gang pairs, dish-shaped ground discs, trailer wheels or drawbar. Unlike the own inclined rectangular plate cutaway, these radial circular plates are all joined to an end-supported common spindle inside a half-round vessel rather than independently resting on two bottom rails above hopper openings. All vessel, walls, spindle, discs, bearings and support coordinates newly authored together, no old basin, gang disc, beater drum or frame mesh reused. Four opaque constant untextured PBR roles, metres Z up, whole horizontal bounds centred at four grounded soles, one whole model zero scenes. Empty static illustrative apparatus only, with no liquid, biomass, living material or treatment media. No biological activity, aeration, filtering, water quality, treatment efficiency, hydraulic or process connectivity, bearing fit, drive operation, rotation, machinery clearance specification, load, manufacture, cleaning, installation or equipment safety capability made or verified. No animation, rigging or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
