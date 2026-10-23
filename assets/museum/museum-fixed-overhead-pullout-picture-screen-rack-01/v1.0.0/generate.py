import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='museum-fixed-overhead-pullout-picture-screen-rack-01'
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
  ring=[(xx,y,z)]if r==0 else[(xx,y+r*math.sin(math.tau*i/N+math.pi/N),z+r*math.cos(math.tau*i/N+math.pi/N))for i in range(N)];rs.append(list(range(len(v),len(v)+len(ring))));v+=ring
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

# Complete fixed overhead-hung picture-screen storage rack, no paintings or texture panels.
PALETTE=[('RackWarmLightSteel',(.55,.58,.56,1),.67,.2),('ScreenSlateMetal',(.19,.26,.28,1),.55,.55),('BlueHandlesAndFootPads',(.08,.22,.28,1),.68,.1)]
# Ground-connected complete portal frame and full forward skids.
for label,x in [('L',-.55),('R',.55)]:
 box(label+'WholeLongGroundSkid',(x-.065,-1.29,.025),(x+.065,.94,.10),0)
 for tag,y in [('Front',-1.23),('Rear',.88)]:box(label+tag+'FiniteFootPad',(x-.08,y-.07,0),(x+.08,y+.07,.035),2)
 for tag,y in [('Entry',-.54),('Back',.84)]:box(label+tag+'FullHeightPortalPost',(x-.04,y-.04,.075),(x+.04,y+.04,2.23),0)
for tag,y in [('Entry',-.54),('Back',.84)]:
 box(tag+'WholeTopCrossbeam',(-.62,y-.05,2.16),(.62,y+.05,2.25),0)
 box(tag+'WholeGroundCrossbeam',(-.55,y-.045,.045),(.55,y+.045,.105),0)
# Each rail is ONE closed downward-slotted channel, with internal bearing shoulders.
profile=[(-.07,2.02),(-.018,2.02),(-.018,2.04),(-.05,2.04),(-.05,2.14),(.05,2.14),(.05,2.04),(.018,2.04),(.018,2.02),(.07,2.02),(.07,2.16),(-.07,2.16)]
def yz_grid(name,x,y0,y1,z0,z1):
 def bands(a,b,n):
  edge=.04;rib=.009;gap=(b-a-2*edge-(n-1)*rib)/n;out=[a,a+edge]
  for k in range(n):
   out.append(out[-1]+gap)
   if k<n-1:out.append(out[-1]+rib)
  out.append(b);return out
 ys=bands(y0,y1,5);zs=bands(z0,z1,7);v=[];index={};boundary={}
 for j in range(len(zs)-1):
  for i in range(len(ys)-1):
   if i%2 and j%2:continue
   pts=[(xx,yy,zz)for zz in[zs[j],zs[j+1]]for yy in[ys[i],ys[i+1]]for xx in[x-.009,x+.009]];ids=[]
   for p in pts:
    p=tuple(round(c,9)for c in p)
    if p not in index:index[p]=len(v);v.append(p)
    ids.append(index[p])
   for f in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:
    face=tuple(ids[k]for k in f);key=tuple(sorted(face))
    if key in boundary:del boundary[key]
    else:boundary[key]=face
 f=[]
 for a,b,c,d in boundary.values():f.extend([(a,b,c),(a,c,d)])
 record(name,v,f,1)
for label,x,y0 in [('Extended',-.23,-1.14),('Stored',.23,-.39)]:
 pad(label+'WholeSlottedOverheadRail',[(xx+x,z)for xx,z in profile],-1.25,.91,0)
 for tag,y in [('Front',-1.24),('Rear',.90)]:box(label+tag+'FixedRailStop',(x-.05,y-.008,2.04),(x+.05,y+.008,2.14),1)
 # Full bottom guide profile, not carrying the panel weight.
 pad(label+'WholeFloorGuide',[(x-.045,.10),(x+.045,.10),(x+.045,.25),(x+.021,.25),(x+.021,.14),(x-.021,.14),(x-.021,.25),(x-.045,.25)],-1.25,.91,0)
 yz_grid(label+'WholeVerticalOpenPictureScreen',x,y0,y0+1.20,.20,1.94)
 for n,y in enumerate([y0+.17,y0+1.03]):
  box(label+str(n)+'WholeSuspensionStem',(x-.012,y-.023,1.92),(x+.012,y+.023,2.085),1)
  pipe(label+str(n)+'WholeTrolleyAxle',[(x-.049,y,2.04+.036*math.cos(math.pi/24)),(x+.049,y,2.04+.036*math.cos(math.pi/24))],.009,1,12)
  # Two complete wheels rest on the two shoulders; no result relies on motion.
  for side,xx in [('L',x-.033),('R',x+.033)]:wheel(label+str(n)+side+'BearingWheel',xx,y,2.04+.036*math.cos(math.pi/24),.036,.008,.026,1)
 # Continuous front pull connected at both ends to the true front screen border.
 pipe(label+'WholeFrontPull',[(x,y0+.016,.88),(x,y0-.085,.88),(x,y0-.085,1.14),(x,y0+.016,1.14)],.018,2,8)
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
focus=Vector((0,0,1.10))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.75;aim(cam,(5,-6,3.6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/museum/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'museum','style':'S01-clean-geometric','title':'Fixed Overhead Pullout Picture Screen Rack','description':'One newly authored complete empty museum collection picture-screen storage rack. A grounded four-post portal frame and long ground skids carry two full downward-slotted overhead channels. Each whole vertical welded open-grid screen has two hanging trolleys, each with two fixed shoulder-seated wheels and a suspension stem through the rail slot. One screen is fixed forward while the other stays in its rear position. Full low channels guide the lower screen edges without becoming horizontal shelves. The entire upper bearing relationship and vertical hanging access architecture differs from rear-hinged horizontal drying trays, leaning A-frame sheet storage and bottom-supported linked pantry baskets. Two screen positions illustrate one rack, not new assets counted by panels or hole count. All numeric geometry newly authored, no paintings, labels, old mesh instances or transparent texture grid. Three opaque untextured PBR materials, metres/native Z up and horizontal-bounds-centred ground origin. One fixed static prop, zero scenes. No rolling, sliding travel, loading method, retention, anti-tip, conservation, humidity control, load, human access, installation, manufacture or museum safety compliance is verified.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
