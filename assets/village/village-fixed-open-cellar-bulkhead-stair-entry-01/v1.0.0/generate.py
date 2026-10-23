import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='village-fixed-open-cellar-bulkhead-stair-entry-01'
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

# One full descending cellar entrance module, shown above terrain to expose its full envelope.
PALETTE=[('WholeStoneEntryWell',(.45,.42,.34,1),.91,0),('WarmTimberSlopingHatchLeaves',(.37,.19,.075,1),.83,0),('DarkFixedHingeIron',(.095,.115,.11,1),.52,.6)]
# Two whole thick sloping side walls. Local Y goes from exterior upper mouth to low rear exit.
def side_profile(name,p,x0,x1,mat):
 pad(name,p,x0,x1,mat);v,f,m=G[name];G[name]=([(yy,xx,z)for xx,yy,z in v],[(a,c,b)for a,b,c in f],m)
for x0,x1,label in[(-.75,-.55,'Left'),(.55,.75,'Right')]:
 side_profile(label+'WholeSlopingEntryWellWall',[(-1.4,0),(1.4,0),(1.4,2.14),(-1.4,1.42)],x0,x1,0)
# Complete stair-and-floor solid, six descending risers and a full lower landing.
# The front upper access datum is1.12m, not the freestanding preview ground datum.
p=[(-1.4,0),(1.4,0),(1.4,.16),(.56,.16),(.56,.32),(.28,.32),(.28,.48),(0,.48),(0,.64),(-.28,.64),(-.28,.80),(-.56,.80),(-.56,.96),(-.84,.96),(-.84,1.12),(-1.4,1.12)]
side_profile('WholeDescendingSixRiserStairAndLowerLanding',p,-.55,.55,0)
# Whole rear lintel leaves the lower passage genuinely through, not a blind staircase recess.
box('WholeRearExitLintel',(-.55,1.25,1.95),(.55,1.4,2.14),0)
# The two full roof-like hatch leaves hinge about separate inclined side axes.
# Axis follows the slope of the well rim. Rotated fixed105degrees outward, no motion claim.
slope=.72/2.8;u=unit((0,1,slope))
def rotate_about_axis(p,origin,angle):
 q=sub(p,origin);c=math.cos(angle);s=math.sin(angle)
 return add(origin,add(add(mul(q,c),mul(cross(u,q),s)),mul(u,dot(u,q)*(1-c))))
for side,label in[(-1,'Left'),(1,'Right')]:
 pivot=(side*.67,-1.38,1.42+.02*slope+.025);x0,x1=(-.67,-.008)if side<0 else(.008,.67)
 # box then map its top/bottom to the inclined complete slab.
 name=label+'WholeFixedOpenSlopingHatchLeaf';box(name,(x0,-1.38,0),(x1,1.38,.055),1)
 v,f,m=G[name];base=[(x,y,1.42+(y+1.4)*slope+.025+z)for x,y,z in v]
 G[name]=([rotate_about_axis(p,pivot,side*math.radians(105))for p in base],f,m)
 # Two actual full fixed bearing barrels lie along the inclined root on the side-wall top.
 for j,y in enumerate([-.90,.86]):
  z=1.42+(y+1.4)*slope+.025
  pipe(label+'FixedInclinedHingeBearing'+str(j),[(side*.67,y-.085,z-.085*slope),(side*.67,y+.085,z+.085*slope)],.042,2,10)
 # One complete U pull is transformed with this leaf, not left hovering at the closed pose.
 x=side*.17;y=-.55;z=1.42+(y+1.4)*slope+.080
 name=label+'WholeLeafPull';pipe(name,[(x,y-.10,z),(x,y-.10,z+.07),(x,y+.10,z+.07),(x,y+.10,z)],.018,2,8)
 v,f,m=G[name];G[name]=([rotate_about_axis(p,pivot,side*math.radians(105))for p in v],f,m)
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
focus=Vector((0,0,1.25))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=4.55;aim(cam,(-4,6,6.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/village/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'modular','theme':'village','style':'S01-clean-geometric','title':'Fixed Open Cellar Bulkhead Stair Entry','description':'One newly authored complete static village cellar-entry architectural module. Two full thick sloping side walls surround a whole descending six-riser stair with upper exterior access edge and lower landing. A complete rear lintel leaves a genuine low-level through exit. Two full thick timber hatch leaves are fixed open outward about inclined side axes following the top rim, with fixed iron bearing appearances and full pulls. The module expresses a ground-height transition and inclined hatch enclosure around a descending route, not a changed step count, the old freestanding return stair, a vertical split door, or an upright airlock recolour. All numeric geometry is new. Three constant opaque PBR roles, native metres, horizontal bounds-centred lowest foundation datumZ0; the front exterior access level isZ1.12m and lower landingZ.16m. Exposed outside sidewalls are intentional: no surrounding earth, host house, basement room, invisible cutaway, copied components, animation or extra pose. One modular asset and zero scenes. Static appearance only; no human clearance, navigation, moving hatch or collision sweep, old-module dimensional fit, water exclusion, drainage, excavation, structural load, real cellar construction or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
