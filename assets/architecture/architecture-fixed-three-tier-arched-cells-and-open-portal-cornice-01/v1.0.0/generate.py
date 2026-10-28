import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='architecture-fixed-three-tier-arched-cells-and-open-portal-cornice-01'
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
PALETTE=[('WholeGroundPlinthMutedLimestone',(.40,.39,.34,1),.95,0),('WholePortalCarrierWarmStone',(.52,.45,.34,1),.94,0),('WholeProjectingHoodOuterPaleStone',(.66,.56,.39,1),.92,0),('WholeArchedSoffitsSoftIvory',(.75,.67,.51,1),.94,0)]
FM={};JOINS=[];ROOTS=['WholeGroundPortalPlinth'];CELLS=[]
box(ROOTS[0],(-3.30,-1.65,0),(3.30,.75,.14),0)
for side in[-1,1]:
 n='WholeFullHeightPortalPier'+str(side);box(n,(side*2.95-.14,-.10,.10),(side*2.95+.14,.50,2.30),1);JOINS.append((n,ROOTS[0],(side*2.95,.1,.12)))
box('WholePortalSpanningLintel',(-3.05,-.07,2.08),(3.05,.57,2.28),1)
for side in[-1,1]:JOINS.append(('WholePortalSpanningLintel','WholeFullHeightPortalPier'+str(side),(side*2.95,.15,2.18)))
box('WholeUpperRearCarrier',(-3.08,.32,2.12),(3.08,.64,4.07),1);JOINS.append(('WholeUpperRearCarrier','WholePortalSpanningLintel',(0,.44,2.20)))
# Complete finite hood solid, with a genuinely rising arched underside and no lower floor.
# Each independently defined grid has full front/side/back thickness faces and a closed top.
def hood(name,xc,front,base):
 nx,ny=12,6;w=.56;back=.42;top=base+.62;v=[];f=[];fm=[]
 for layer in[0,1]:
  for j in range(ny+1):
   t=j/ny;y=front+(back-front)*t
   for i in range(nx+1):
    u=i/nx;z=top if layer else base+.48*math.sin(math.pi*u)*(1-t)+.55*t
    v.append((xc-w+2*w*u,y,z))
 n=(nx+1)*(ny+1)
 def face(q,mat):f.extend([(q[0],q[1],q[2]),(q[0],q[2],q[3])]);fm.extend([mat,mat])
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;d=a+nx+1;c=d+1
   face((a,d,c,b),3);face((a+n,b+n,c+n,d+n),2)
 for i in range(nx):
  a=i;b=i+1;face((a,b,b+n,a+n),2)
  a=ny*(nx+1)+i;b=a+1;face((a,a+n,b+n,b),2)
 for j in range(ny):
  a=j*(nx+1);b=a+nx+1;face((a,a+n,b+n,b),2)
  a=j*(nx+1)+nx;b=a+nx+1;face((a,b,b+n,a+n),2)
 record(name,v,f,2);FM[name]=fm;CELLS.append((name,xc,front,base,back));JOINS.append((name,'WholeUpperRearCarrier',(xc,.37,top-.025)))
for tier,(centres,front,base)in enumerate([([-1.8,-.6,.6,1.8],-.32,2.15),([-2.4,-1.2,0,1.2,2.4],-.82,2.78),([-1.8,-.6,.6,1.8],-1.32,3.41)]):
 for j,x in enumerate(centres):hood('WholeArchedCellTier%dUnit%d'%(tier+1,j+1),x,front,base)
box('WholeContinuousProjectingCrown',(-3.16,-1.45,4.00),(3.16,.68,4.23),2);JOINS.append(('WholeContinuousProjectingCrown','WholeUpperRearCarrier',(0,.48,4.04)))
V=[p for v,f,m in G.values()for p in v];SHIFT=((min(p[0]for p in V)+max(p[0]for p in V))/2,(min(p[1]for p in V)+max(p[1]for p in V))/2,min(p[2]for p in V))
for n,(v,f,m)in list(G.items()):G[n]=([sub(p,SHIFT)for p in v],f,m);FM.setdefault(n,[m]*len(f))
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
focus=Vector((0,0,2.05))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=8.4;aim(cam,(1,-18,6.3) if view=='qa-front' else (8,-18,6.0));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/architecture/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'modular','theme':'architecture','style':'S01-clean-geometric','title':'Fixed Three Tier Arched Cells and Open Portal Cornice','description':'One wholly newly authored complete static cellular-cornice-inspired portal module. Two full grounded side piers and one whole spanning lintel leave a broad real open central portal. A complete upper rear carrier joins thirteen entire thick niche-hood solids in three staggered tiers that project progressively farther forward. Each independently authored hood has a genuine curved front arch and continuously rising concave soffit, complete side and back thickness faces, and a full unbroken top; there is no lower niche floor or dark painted recess. The central, side and upper fields are offset instead of stacking a uniform grid. A whole broad crown caps the full array. All complete hood and support geometry newly authored together, no tile, squinch, vault or wall mesh imported, extracted or stretched. Unlike four diagonal squinches carrying an open octagonal drum, this is one frontal tiered cornice with deep projecting cells and a whole rectangular portal. Unlike shallow blind coffers cut into a single continuous semicylindrical roof, the major relationship is three successively overhanging staggered rows of complete curved hood solids rooted in a full rear carrier. Generic muqarnas-like cellular ornament category only; not a reconstruction of any historical object, named building, religious fixture, traditional geometric grammar or museum tile. Four opaque constant untextured PBR surface roles, metre-style native Z up and full horizontal bounds-centred grounded plinth. One architectural module zero scenes; repeated hood components are not separate assets. Small static seat overlaps and separated tier margins are visual simplifications, not assembly or engineering details. No historical authenticity, masonry stability, thrust, bearing, ornament attachment, weathering, fabrication, host fit, usable doorway, navigation, accessible route, building-code, structural load or construction safety capability made or verified. No rigging animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
