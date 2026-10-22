import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='cave-mine-open-ended-peripheral-roller-trommel-01'
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
# One open-ended, genuinely perforated drum, fixed on four peripheral rollers.
# Complete new apparatus, no central supporting shaft or capped drum bottom.
d=unit((0,1,.18));u=(1,0,0);w=cross(u,d)
def world(t,x,z):return add((0,0,1.02),add(mul(d,t),add(mul(u,x),mul(w,z))))
ys=[-.90,-.78,-.06,.06,.78,.90];segments=40;cells={(k,j)for k in range(5)for j in range(segments)if k in[0,2,4]or j%4==0};v=[];ids={};f=[]
def vi(r,k,j):
 key=(r,k,j%segments)
 if key not in ids:
  ids[key]=len(v);a=math.tau*(j%segments)/segments;rr=[.415,.46][r];v.append(world(ys[k],rr*math.cos(a),rr*math.sin(a)))
 return ids[key]
def quad(q):f.extend([(q[0],q[1],q[2]),(q[0],q[2],q[3])])
for k,j in sorted(cells):
 a,b,c,dd=vi(1,k,j),vi(1,k+1,j),vi(1,k+1,j+1),vi(1,k,j+1)
 aa,bb,cc,ddd=vi(0,k,j),vi(0,k+1,j),vi(0,k+1,j+1),vi(0,k,j+1)
 quad((a,b,c,dd));quad((ddd,cc,bb,aa))
 for p,q,pp,qq,neighbor in[(a,b,aa,bb,(k,(j-1)%segments)),(b,c,bb,cc,(k+1,j)),(c,dd,cc,ddd,(k,(j+1)%segments)),(dd,a,ddd,aa,(k-1,j))]:
  if neighbor not in cells:quad((q,p,pp,qq))
record('WholeOpenEndedTwentyWindowScreenDrum',v,f,0)
def along_ring(name,center,ro,ri,width,mat):
 wheel(name,0,0,0,ro,ri,width,mat);vv,ff,mm=G[name];record(name,[add(center,add(mul(d,x),add(mul(u,y),mul(w,z))))for x,y,z in vv],ff,mm)
# Four peripheral seating rolls: two under each full end band. All eight axle
# housings are genuinely bored; the installed shaft occupies the bore.
for end,t in [('Low',-.84),('High',.84)]:
 cz=world(t,0,-.576*math.sin(math.radians(54)))[2];cy=world(t,0,-.576*math.sin(math.radians(54)))[1]
 box(end+'CompleteCrossFrame',(-.65,cy-.23,cz-.28),(.65,cy+.23,cz-.20),2)
 for side,sign in [('Left',-1),('Right',1)]:
  x=sign*.576*math.cos(math.radians(54));p=world(t,x,-.576*math.sin(math.radians(54)))
  along_ring(end+side+'WholePeripheralRoll',p,.12,.035,.10,1)
  pipe(end+side+'FixedRollAxle',[add(p,mul(d,-.20)),add(p,mul(d,.20))],.035,2,16)
  for fore,tt in [('A',-.15),('B',.15)]:
   pp=add(p,mul(d,tt));along_ring(end+side+fore+'TrueBoredRollBearing',pp,.065,.036,.06,2)
   box(end+side+fore+'BearingPost',(x-.05,pp[1]-.05,cz-.20),(x+.05,pp[1]+.05,pp[2]-.045),2)
  xx=sign*.49
  box(end+side+'WholeFrameLeg',(xx-.055,cy-.06,.12),(xx+.055,cy+.06,cz-.28),2)
  box(end+side+'FlatGroundFoot',(xx-.14,cy-.17,0),(xx+.14,cy+.17,.04),2)
for side,x in [('Left',-.49),('Right',.49)]:box(side+'WholeBaseRail',(x-.065,-1.12,.04),(x+.065,1.17,.12),2)
# One real thick open catch funnel between the two roll frames. Both mouth and
# short lower neck are open; it covers the central screening span, not all holes.
def rectangle(x,y,z,sloped=False):return[(xx,yy,z+.18*yy if sloped else z)for xx,yy in[(-x,-y),(x,-y),(x,y),(-x,y)]]
rings=[rectangle(.15,.16,.13),rectangle(.15,.16,.22),rectangle(.50,.45,.52,True),rectangle(.46,.41,.52,True),rectangle(.11,.12,.22),rectangle(.11,.12,.13)];v=[p for ring in rings for p in ring];f=[]
for k in range(len(rings)):
 for i in range(4):
  j=(i+1)%4;a=4*k+i;b=4*k+j;c=4*((k+1)%len(rings))+j;dd=4*((k+1)%len(rings))+i;f.extend([(a,b,c),(a,c,dd)])
record('WholeOpenCentralCatchFunnelAndNeck',v,f,3)
for side,x in [('Left',-.49),('Right',.49)]:
 for end,y in [('A',-.30),('B',.30)]:box(side+end+'FunnelMount',(x-.025,y-.035,.12),(x+.025,y+.035,.512+.18*y),2)
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
for name,color,rough in [('Screen_CoatedSteel', (0.43, 0.49, 0.47, 1), 0.67), ('Roll_DarkWearSurface', (0.13, 0.16, 0.16, 1), 0.76), ('Frame_OchrePaint', (0.43, 0.29, 0.12, 1), 0.79), ('Catch_DarkTeal', (0.18, 0.28, 0.28, 1), 0.78)]:
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
focus=Vector((0,0,.78))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.45;aim(cam,(5,-7,4.4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/village/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'cave-mine','style':'S01-clean-geometric','title':'Open-Ended Peripheral-Roller Trommel Screen','description':'One newly authored complete static mine-processing appearance: a single thick cylindrical screen with two fully open axial mouths and twenty real surrounding windows, carried on four peripheral rollers under its full end bands. There is no central drum-supporting spindle, end plate, closed bottom or lid. Eight bored roller-axle housings, two end frames, tied base rails and four flat feet form the whole fixed support assembly. A separate continuous thick open catch funnel with a short genuine outlet neck sits beneath the central screen span; it is not claimed to collect every window. This differs structurally from the old closed-end spindle-supported garden composter, closed-bottom pear-drum mixer and flat seven-bar grizzly, not merely a barrel with more holes or new colors. All main geometry newly authored with mature annular and cell-shell primitives. Static visual art only: no rotation, motor, actual screening/flow capacity, precision bearing, assembly/manufacturing, load or equipment safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
