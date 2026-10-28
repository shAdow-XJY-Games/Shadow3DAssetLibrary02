import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='waterworks-fixed-converging-throat-flume-and-twin-open-side-wells-01'
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
PALETTE=[('WholeShapedFlumeWallsWarmConcrete',(.50,.47,.39,1),.92,0),('WholeContinuousFlumeFloorPaleConcrete',(.68,.65,.54,1),.91,0),('WholeOpenSideWellsMutedTeal',(.18,.32,.33,1),.82,.05),('WholeHollowSideConnectionsSatinBronze',(.46,.34,.19,1),.62,.42)]
FM={};JOINS=[];ROOTS=['WholeConvergingDroppingAndExpandingFlume'];WELLS=[-1.85,.10]
STATIONS=[(-3.4,1.55,.56),(-.6,.50,.56),(.55,.50,.22),(3.1,1.25,.40)]
def section(y):
 for a,b in zip(STATIONS,STATIONS[1:]):
  if a[0]-1e-9<=y<=b[0]+1e-9:
   t=(y-a[0])/(b[0]-a[0]);return(a[1]+(b[1]-a[1])*t,a[2]+(b[2]-a[2])*t)
 raise ValueError(y)
def grid_skin(name,nx,ny,nz,point,occupied,material):
 v=[];f=[];fm=[];ix={}
 def vertex(key):
  if key not in ix:ix[key]=len(v);v.append(point(*key))
  return ix[key]
 sides=[((0,2,3,1),(0,0,-1)),((4,5,7,6),(0,0,1)),((0,1,5,4),(0,-1,0)),((2,6,7,3),(0,1,0)),((0,4,6,2),(-1,0,0)),((1,3,7,5),(1,0,0))]
 for i,j,k in sorted(occupied):
  verts=[(i+a,j+b,k+c)for c in[0,1]for b in[0,1]for a in[0,1]]
  for face,delta in sides:
   near=(i+delta[0],j+delta[1],k+delta[2])
   if near in occupied:continue
   ids=[vertex(verts[t])for t in face];f.extend([(ids[0],ids[1],ids[2]),(ids[0],ids[2],ids[3])]);fm.extend([material(i,j,k,delta)]*2)
 record(name,v,f,0);FM[name]=fm
YS=sorted(set([s[0]for s in STATIONS]+[y+d for y in WELLS for d in[-.12,.12]]))
def flume_point(i,j,k):
 y=YS[j];w,h=section(y);return([-w-.18,-w,w,w+.18][i],y,[0,h,.84,1.01,1.35][k])
ports={j for j in range(len(YS)-1)if any(abs((YS[j]+YS[j+1])/2-y)<1e-9 for y in WELLS)}
cells={(i,j,k)for i in range(3)for j in range(len(YS)-1)for k in range(4)if(k==0 or i in[0,2])and not(i==2 and j in ports and k==2)}
grid_skin(ROOTS[0],3,len(YS)-1,4,flume_point,cells,lambda i,j,k,d:1 if k==0 and i==1 and d==(0,0,1)else 0)
for index,yc in enumerate(WELLS):
 name='WholeOpenFloorAndPortSideWell%d'%(index+1);xs=[1.95,2.07,2.53,2.65];ys=[yc-.38,yc-.24,yc-.12,yc+.12,yc+.24,yc+.38];zs=[0,.20,.84,1.01,1.60]
 cells={(i,j,k)for i in range(3)for j in range(5)for k in range(4)if(k==0 or i in[0,2]or j in[0,4])and not(i==0 and j==2 and k==2)}
 grid_skin(name,3,5,4,lambda i,j,k:(xs[i],ys[j],zs[k]),cells,lambda i,j,k,d:2);ROOTS.append(name)
 # One whole continuous hollow duct with both true rectangular mouths and all four walls.
 loops=[]
 for end,inner in[(0,False),(1,False),(1,True),(0,True)]:
  half=.125 if inner else .16;z0,z1=(.835,1.015)if inner else(.80,1.05);ring=[]
  for dy,z in[(-half,z0),(half,z0),(half,z1),(-half,z1)]:
   y=yc+dy;x=2.03 if end else section(y)[0]+.09;ring.append((x,y,z))
  loops.append(ring)
 v=sum(loops,[]);f=[]
 for a in range(4):
  for j in range(4):
   b=(j+1)%4;aa=a*4+j;bb=a*4+b;cc=((a+1)%4)*4+b;dd=((a+1)%4)*4+j;f.extend([(aa,bb,cc),(aa,cc,dd)])
 duct='WholeHollowRectangularSideConnection%d'%(index+1);record(duct,v,f,3);FM[duct]=[3]*len(f);JOINS.extend([(duct,'WholeConvergingDroppingAndExpandingFlume',(section(yc)[0]+.12,yc,.82)),(duct,name,(2.01,yc,.82))])
V=[p for v,f,m in G.values()for p in v];SHIFT=((min(p[0]for p in V)+max(p[0]for p in V))/2,(min(p[1]for p in V)+max(p[1]for p in V))/2,min(p[2]for p in V))
for n,(v,f,m)in list(G.items()):G[n]=([sub(p,SHIFT)for p in v],f,m)
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
focus=Vector((0,0,.75))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=9.2;aim(cam,(9,-12,11) if view=='qa-front' else (8,11,13));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/waterworks/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'modular','theme':'waterworks','style':'S01-clean-geometric','title':'Fixed Converging Throat Flume and Twin Open Side Wells','description':'One wholly newly authored complete dry constricted-flume-inspired waterworks module. A single continuous closed material shell joins a broad level-floor converging inlet, a short parallel-sided throat with a descending floor, and a diverging outlet whose full floor rises again to a lower level than the inlet. Both complete axial mouths and the entire open top remain present, with continuous tall side walls and a finite grounded sole. Two genuine rectangular through-ports occupy the same full side wall at separated longitudinal stations. Each port meets one whole short hollow four-wall rectangular connection and one complete tall open-topped side well with a full floor, all four walls and a real inward-facing wall port. The separate wells are empty complete chambers, not solid boxes or dark top decals. All five whole material meshes authored together with shared indexed boundary grids, no old chute, dam, basin, well or pipe imported or extracted. Unlike the equal-width monotonically sloping U-baffle chute, the main route changes width and reverses its floor slope, with no baffles, piers or overlaid ground slab. Unlike a high rounded overflow body descending into a low basin with end sill, this retains two open axial mouths, a narrow finite throat and genuine lateral communicating chambers. Four opaque constant untextured PBR surface roles, metre-style native Z up and full horizontal bounds-centred three ground soles. One whole architectural model zero scenes. Broad measurement-flume and side-well category only; artistic proportions deliberately do not use standard Parshall dimensions, calibration tables or any named installation. Small fixed duct/wall overlaps and slightly wider duct bores create static rooted visual interfaces, not a fitted fabricated system. No water, float, gauge scale, actual flow, discharge measurement, calibration, water-level equivalence, flow regime, sediment handling, sealing, hydraulic design, loading, manufacture, access, installation or civil safety capability made or verified. No rigging animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
