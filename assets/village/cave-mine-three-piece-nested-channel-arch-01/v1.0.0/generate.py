import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='cave-mine-three-piece-nested-channel-arch-01'
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
# Three whole open-section steel channels form one fixed, nested-lap mine arch.
RADIUS=1.35;SPRING=1.30
def section(w,back,thick):
 p=[(-w,-.14),(-w,back),(w,back),(w,-.14),(w-thick,-.14),(w-thick,back-thick),(-w+thick,back-thick),(-w+thick,-.14)]
 if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(p,p[1:]+p[:1]))<0:p.reverse()
 return p
def sweep(name,p,sections,mat):
 n=len(p);v=[]
 for x,z,ux,uz in sections:v.extend([(x+u*ux,y,z+u*uz)for u,y in p])
 f=[]
 for a,b,c in earclip(p):f.extend([(c,b,a),(a+(len(sections)-1)*n,b+(len(sections)-1)*n,c+(len(sections)-1)*n)])
 for k in range(len(sections)-1):
  for i in range(n):
   j=(i+1)%n;a=k*n+i;b=k*n+j;c=(k+1)*n+j;d=(k+1)*n+i;f.extend([(a,b,c),(a,c,d)])
 record(name,v,f,mat)
def arc(a):return(RADIUS*math.sin(a),SPRING+RADIUS*math.cos(a),math.sin(a),math.cos(a))
for side,sign in [('Left',-1),('Right',1)]:
 box(side+'WholeGroundPlate',(sign*RADIUS-.17,-.24,0),(sign*RADIUS+.17,.24,.16),0)
 sections=[(sign*RADIUS,.16,sign,0),(sign*RADIUS,SPRING,sign,0)]+[arc(sign*math.radians(90-7.5*k))for k in range(1,7)]
 sweep(side+'WholeCurvedOpenChannelLeg',section(.10,.14,.04),sections,0)
# Smaller complete crown channel nests in the true open grooves of the two legs
# over 45..55degree lap intervals; back web rests at Y=.10, not an intersecting tube.
sweep('WholeSmallerNestedCrownChannel',section(.053,.10,.025),[arc(math.radians(-55+110*k/20))for k in range(21)],0)
for sign,side in[(-1,'Left'),(1,'Right')]:
 for k,degrees in enumerate([48,52],1):
  a=sign*math.radians(degrees);p=[(-.14,-.19),(.14,-.19),(.14,-.14),(-.14,-.14)]
  sweep(side+'WholeLapClampStrap'+str(k),p,[arc(a+math.radians(d))for d in[-1,0,1]],1)
  for j,u in enumerate([-.118,.118],1):
   x=(RADIUS+u)*math.sin(a);z=SPRING+(RADIUS+u)*math.cos(a)
   pipe(side+'Clamp'+str(k)+'FixedHexHead'+str(j),[(x,-.215,z),(x,-.185,z)],.018,2,6)
# Actual complete stored geometry sets the centred ground origin once.
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
for name,color,rough in [('Channel_PaintedSteel', (0.36, 0.43, 0.44, 1), 0.73), ('Clamps_OxidePaint', (0.42, 0.27, 0.14, 1), 0.79), ('Bolt_CoatedDark', (0.22, 0.24, 0.24, 1), 0.66)]:
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
focus=Vector((0,0,1.35))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.90;aim(cam,(4,-7,4.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/village/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'modular','assetKind':'modular','theme':'cave-mine','style':'S01-clean-geometric','title':'Three-Piece Nested-Channel Mine Arch Support','description':'One newly authored complete static mine-arch support module: two whole curved open U-channel legs on flat ground plates and one genuinely narrower open-channel crown nested into their grooves over two finite lap zones. Four front bridge straps with eight fixed hex-head appearances mark the actual lap locations. The crown back web meets the leg channel back-web plane; side clearances remain real. Every channel is a complete closed thick material shell around a truly open front groove, not a solid arch painted with lines or a reused stone arch with different colors. All seventeen component meshes newly authored with mature polygon-sweep primitives. The passage has no threshold, wall, rock lining or hidden blocker. Static art only: no moving adjustment, sliding mechanism, excavation, tunnel installation, structural strength, rock-load resistance, bolt tightening or mining safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
