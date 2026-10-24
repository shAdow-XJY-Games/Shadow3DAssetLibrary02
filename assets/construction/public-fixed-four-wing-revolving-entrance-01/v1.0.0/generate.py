import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='public-fixed-four-wing-revolving-entrance-01'
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

# Complete static cylindrical entrance assembly, no host building or operating mechanism.
PALETTE=[('EntranceWarmMetalFrame',(.50,.53,.50,1),.65,.25),('EntranceOpaqueBlueInfill',(.20,.32,.35,1),.65,0),('EntranceDarkBaseHardware',(.22,.25,.24,1),.78,.2)]
def cells(name,axes,keep,mat):
 v=[];idx={};faces={}
 def vi(p):
  if p not in idx:idx[p]=len(v);v.append(p)
  return idx[p]
 for i in range(len(axes[0])-1):
  for j in range(len(axes[1])-1):
   for k in range(len(axes[2])-1):
    mid=[(axes[n][t]+axes[n][t+1])/2 for n,t in enumerate([i,j,k])]
    if not keep(*mid):continue
    ids=[vi((x,y,z))for z in[axes[2][k],axes[2][k+1]]for y in[axes[1][j],axes[1][j+1]]for x in[axes[0][i],axes[0][i+1]]]
    for f in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:
     q=tuple(ids[t]for t in f);key=tuple(sorted(q))
     if key in faces:del faces[key]
     else:faces[key]=q
 ff=[]
 for a,b,c,d in faces.values():ff.extend([(a,b,c),(a,c,d)])
 record(name,v,ff,mat)

# Full circular threshold and canopy; closed disc geometry mapped from the mature annulus helper.
for label,z,r,t,m in [('Threshold',.035,1.18,.07,2),('Canopy',2.36,1.20,.13,0)]:
 wheel('WholeCircular'+label,z,0,0,r,0,t,m);v,f,mi=G['WholeCircular'+label];record('WholeCircular'+label,[(y,z,x)for x,y,z in v],f,mi)
pipe('WholeCentralVerticalPivot',[(0,0,.07),(0,0,2.295)],.055,2,16)
for z,label in[(.07,'Lower'),(2.245,'Upper')]:pipe(label+'WholePivotBearing',[(0,0,z),(0,0,z+.05)],.095,2,16)
# Two whole curved side frames leave opposed front/back entrance mouths.
# Polar grid only emits exposed material boundaries, so each is one connected closed solid.
def arcframe(name,start):
 angles=[math.radians(start+i*7.5)for i in range(13)];rs=[1.075,1.13];zs=[.07,.15,.43,2.20,2.295];v=[];lookup={};faces={}
 def vi(p):
  p=tuple(round(x,12)for x in p)
  if p not in lookup:lookup[p]=len(v);v.append(p)
  return lookup[p]
 for i in range(12):
  for k in range(4):
   if not(k in[0,1,3]or i in[0,5,6,11]):continue
   ids=[vi((r*math.cos(a),r*math.sin(a),z))for z in[zs[k],zs[k+1]]for a in[angles[i],angles[i+1]]for r in rs]
   for f in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:
    q=tuple(ids[t]for t in f);key=tuple(sorted(q))
    if key in faces:del faces[key]
    else:faces[key]=q
 ff=[]
 for a,b,c,d in faces.values():ff.extend([(a,b,c),(a,c,d)])
 record(name,v,ff,0)
arcframe('WholeRightCurvedEntranceFrame',-45);arcframe('WholeLeftCurvedEntranceFrame',135)
# Four full radial framed leaves share a single central pivot; all are internal parts of one entrance.
for j in range(4):
 a=math.radians(22.5+90*j)
 def tr(p):u,v,z=p;return(u*math.cos(a)-v*math.sin(a),u*math.sin(a)+v*math.cos(a),z)
 name='WholeRadialLeafFrame_'+str(j)
 cells(name,[[.04,.10,1.005,1.045],[-.022,.022],[.09,.15,.88,.94,2.21,2.27]],lambda u,v,z:u<.10 or u>1.005 or z<.15 or .88<z<.94 or z>2.21,0)
 vv,ff,m=G[name];record(name,[tr(p)for p in vv],ff,m)
 # Opaque infill is explicit, not real transparent glass.
 for label,z0,z1 in[('Lower',.15,.88),('Upper',.94,2.21)]:
  n=label+'WholeOpaqueLeafInfill_'+str(j);box(n,(.10,-.012,z0),(1.005,.012,z1),1);vv,ff,m=G[n];record(n,[tr(p)for p in vv],ff,m)
 pipe('WholeLeafPushBar_'+str(j),[tr((.18,-.02,1.04)),tr((.18,-.075,1.04)),tr((.91,-.075,1.04)),tr((.91,-.02,1.04))],.014,2,10)
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
focus=Vector((0,0,1.20))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.8;aim(cam,(5,-8,4.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/construction/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'public','style':'S01-clean-geometric','title':'Fixed Four Wing Revolving Entrance','description':'One newly authored complete static revolving-entrance assembly. A full circular threshold and upper canopy bound a central full-height vertical pivot with end bearings. Two complete curved side frames form a cylindrical perimeter with genuine open windows and opposed front/back entry mouths. Four whole framed radial leaves, each with opaque inset panels and a full push bar, divide the central volume around that one shared axis. These are components of one entrance, not four separately counted doors. This is not a waist-height tripod bar gate with more arms or a duplicated bifold door: the new organization is a full-height cylindrical passage enclosure and radial leaf chambers between opposed mouths. All numeric geometry is new. Three opaque constant PBR materials, metres, Z-up, horizontal bounds-centred threshold datum. One fixed architectural prop, zero scenes, no host building, people or transparent glass claim. No rotation, closing envelope, crowd throughput, accessibility, emergency egress, weather sealing, security, fire compliance, installation, structural load, manufacture or safety certification is claimed.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
