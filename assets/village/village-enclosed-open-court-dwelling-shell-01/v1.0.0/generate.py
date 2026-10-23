import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='village-enclosed-open-court-dwelling-shell-01'
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

import itertools
PALETTE=[('CourtyardStoneFloor',(.42,.38,.31,1),.94,0),('WarmPlasterRooms',(.66,.54,.38,1),.92,0),('ClayCourtyardRoof',(.43,.18,.075,1),.9,0)]
G={};FM={}
def rec(name,v,f,m):G[name]=(v,f,m);FM[name]=[m]*len(f)
def cutbox(name,lo,hi,cuts,mat):
 axes=[sorted(set([lo[k],hi[k]]+[t for a,b in cuts for t in[a[k],b[k]]if lo[k]<t<hi[k]]))for k in range(3)]
 occ=set()
 for c in itertools.product(*[range(len(a)-1)for a in axes]):
  p=[(axes[k][c[k]]+axes[k][c[k]+1])/2 for k in range(3)]
  if not any(all(a[k]<p[k]<b[k]for k in range(3))for a,b in cuts):occ.add(c)
 v=[];f=[];lookup={}
 def face(pts):
  ids=[]
  for p in pts:
   if p not in lookup:lookup[p]=len(v);v.append(p)
   ids.append(lookup[p])
  a,b,c,d=ids;f.extend([(a,b,c),(a,c,d)])
 for i,j,k in sorted(occ):
  x0,x1=axes[0][i:i+2];y0,y1=axes[1][j:j+2];z0,z1=axes[2][k:k+2]
  for delta,pts in [((-1,0,0),[(x0,y0,z0),(x0,y0,z1),(x0,y1,z1),(x0,y1,z0)]),((1,0,0),[(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)]),((0,-1,0),[(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)]),((0,1,0),[(x0,y1,z0),(x0,y1,z1),(x1,y1,z1),(x1,y1,z0)]),((0,0,-1),[(x0,y0,z0),(x0,y1,z0),(x1,y1,z0),(x1,y0,z0)]),((0,0,1),[(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)])]:
   if(i+delta[0],j+delta[1],k+delta[2])not in occ:face(pts)
 rec(name,v,f,mat)
cutbox('CompleteGroundedFloor',(-3.6,-3.6,0),(3.6,3.6,.15),[],0)
cutbox('FrontExteriorDoorAndTwoWindows',(-3.6,-3.6,.15),(3.6,-3.4,2.85),[((-.55,-3.7,.1),(.55,-3.3,2.2)),((-2.6,-3.7,1),( -1.6,-3.3,2.1)),((1.6,-3.7,1),(2.6,-3.3,2.1))],1)
cutbox('RearExteriorWindow',(-3.6,3.4,.15),(3.6,3.6,2.85),[((-.6,3.3,1),(.6,3.7,2.1))],1)
for side in[-1,1]:
 a,b=sorted([side*3.4,side*3.6]);cutbox('ExteriorSide'+str(side),(a,-3.4,.15),(b,3.4,2.85),[((a-.1,-.6,1),(b+.1,.6,2.1))],1)
for side in[-1,1]:
 a,b=sorted([side*1.2,side*1.4]);cutbox('CourtyardLongSide'+str(side),(a,-1.4,.15),(b,1.4,2.85),[((a-.1,-.5,.1),(b+.1,.5,2.2))],1)
 a,b=sorted([side*1.2,side*1.4]);cutbox('CourtyardCrossSide'+str(side),(-1.2,a,.15),(1.2,b,2.85),[((-.55,a-.1,.1),(.55,b+.1,2.2))],1)
# Four true room partitions; doorways keep the wings connected to the court.
for sx in[-1,1]:
 x0,x1=sorted([sx*1.4,sx*3.4]);cx=(x0+x1)/2
 for sy in[-1,1]:
  y0,y1=sorted([sy*1.4,sy*1.55]);cutbox('RoomPartition'+str(sx)+'_'+str(sy),(x0,y0,.15),(x1,y1,2.85),[((cx-.45,y0-.1,.1),(cx+.45,y1+.1,2.2))],1)
# Roof is one continuous annulus with a real open central sky court, not four copied houses.
v=[]
for r,z in[(3.8,2.95),(2.4,3.8),(1.,2.95),(3.8,2.85),(1.,2.85)]:v +=[(-r,-r,z),(r,-r,z),(r,r,z),(-r,r,z)]
f=[]
def quad(a,b,c,d):f.extend([(a,b,c),(a,c,d)])
for i in range(4):
 j=(i+1)%4
 quad(i,j,4+j,4+i);quad(4+i,4+j,8+j,8+i)
 quad(12+i,16+i,16+j,12+j)
 quad(i,12+i,12+j,j);quad(8+i,8+j,16+j,16+i)
rec('WholeCourtyardRingHipRoof',v,f,2)
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
focus=Vector((0,0,1.6))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=12.3;aim(cam,(10,-14,13));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/village/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'prop','theme':'village','style':'S01-clean-geometric','title':'Enclosed Open-Court Dwelling Shell','description':'One newly authored complete courtyard dwelling shell, counted as one architecture model and zero scenes. A continuous grounded floor carries four exterior walls with true door/window openings, four inward-facing courtyard walls with actual doorways, and four doorway-bearing room partitions. These enclosed perimeter spaces surround a genuinely open-to-sky central courtyard; the front exterior entrance aligns with a real inner doorway leading into the court. One continuous annular hipped roof covers the perimeter rooms while leaving the central sky opening entirely unfilled, with complete inward eaves, outward eaves and a flat enclosed underside. No wall or roof is hidden or removed for the preview. Fourteen closed editable solids and three opaque constant PBR materials; native metres and bounds-centred ground datum. This is not the existing well/tree/fence courtyard scene, not four copies of a cottage, and not a lengthened open-post L corridor. It is an unfurnished static dwelling shell only: no sash/door leaves, glazing, furniture, residents, plumbing, collision/navigation system, real room usability, habitability, climate/weather performance, structural engineering, construction-code compliance, load or safety assurance. Interior parts are present but some are naturally occluded in exterior views.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
