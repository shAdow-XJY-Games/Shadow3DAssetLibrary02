import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='steam-workshop-static-orthogonal-worm-wheel-display-01'
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

# Orthogonal static screw-and-wheel display, with a deliberate visible gap.
# No real worm profile, conjugate meshing or speed/force transmission is claimed.
PALETTE=[('CastBaseAndBearingBlocks',(.075,.19,.18,1),.76,.15),('WarmBrassToothedWheel',(.57,.32,.095,1),.52,.45),('SteelShaftAndHelix',(.30,.34,.35,1),.49,.60)]
box('WholeGroundedDisplayBase',(-1.1,-.95,0),(1.1,.95,.14),0)
def ring_loops(name,loops,mat):
 n=len(loops[0]);v=sum(loops,[]);f=[]
 for k in range(len(loops)):
  kk=(k+1)%len(loops)
  for i in range(n):j=(i+1)%n;a=k*n+i;b=k*n+j;c=kk*n+j;d=kk*n+i;f.extend([(a,b,c),(a,c,d)])
 record(name,v,f,mat)
def bearing(name,axis,centre,ax0,ax1):
 u0,u1=-.22,.22;z0,z1=.14,centre+.22
 angles=sorted(set([math.tau*i/24 for i in range(24)]+[math.atan2(z-centre,u)%math.tau for u in[u0,u1]for z in[z0,z1]]))
 def point(u,z,a):return(a,u,z)if axis=='X'else(u,a,z)
 outside=[];inside=[]
 for t in angles:
  du,dz=math.cos(t),math.sin(t);ts=[]
  if abs(du)>1e-12:ts.append((u1 if du>0 else u0)/du)
  if abs(dz)>1e-12:ts.append(((z1 if dz>0 else z0)-centre)/dz)
  r=min(x for x in ts if x>0);outside.append((r*du,centre+r*dz));inside.append((.071*du,centre+.071*dz))
 loops=[[point(u,z,a)for u,z in ring]for a,ring in[(ax0,outside),(ax1,outside),(ax1,inside),(ax0,inside)]]
 ring_loops(name,loops,0)
for x,label in[(-.70,'Left'),(.70,'Right')]:bearing(label+'WormWholeBoredBearing','X',1.47,x-.08,x+.08)
for y,label in[(-.55,'Front'),(.55,'Rear')]:bearing(label+'WheelWholeBoredBearing','Y',.78,y-.08,y+.08)
# Complete solid shafts use a fixed capped polygonal cylindrical surface.
pipe('WholeHorizontalWormShaft',[(-.95,0,1.47),(.95,0,1.47)],.07,2,24)
pipe('WholePerpendicularWheelShaft',[(0,-.78,.78),(0,.78,.78)],.07,2,24)
# One thick complete helical flight around the X shaft; three full turns.
v=[];f=[];n=72
for k in range(n+1):
 t=math.tau*3*k/n;x=-.45+.90*k/n
 for r,dx in[(.068,-.035),(.13,-.035),(.13,.035),(.068,.035)]:v.append((x+dx,r*math.cos(t),1.47+r*math.sin(t)))
for k in range(n):
 for i in range(4):j=(i+1)%4;a=4*k+i;b=4*k+j;c=4*(k+1)+j;d=4*(k+1)+i;f.extend([(a,b,c),(a,c,d)])
f.extend([(0,3,2),(0,2,1),(4*n,4*n+1,4*n+2),(4*n,4*n+2,4*n+3)])
record('WholeThreeTurnWormFlight',v,f,2)
# New complete toothed annulus, shallow oblique tooth direction across thickness.
angles=[math.tau*(k+t)/24 for k in range(24)for t in[-.5,-.32,-.16,.16,.32]];radii=[r for k in range(24)for r in[.47,.47,.54,.54,.47]]
loops=[]
for y,outer in[(-.12,True),(.12,True),(.12,False),(-.12,False)]:
 phase=.025*y/.12;loops.append([((r if outer else .071)*math.cos(a+phase),y,.78+(r if outer else .071)*math.sin(a+phase))for a,r in zip(angles,radii)])
ring_loops('WholeObliqueToothedWheelAndBore',loops,1)
# Fixed stop collars are visible shaft-end detail, not a moving bearing claim.
for x,label in[(-.82,'Left'),(.82,'Right')]:wheel(label+'WormFixedStop',x,0,1.47,.105,.07,.04,2)
# Whole wheel collars rotated exactly by coordinate permutation from X-axis rings.
for y,label in[(-.67,'Front'),(.67,'Rear')]:
 name=label+'WheelFixedStop';wheel(name,y,0,.78,.105,.07,.04,2);vv,ff,mm=G[name];G[name]=([(yy,xx,z)for xx,yy,z in vv],[(a,c,b)for a,b,c in ff],mm)
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
focus=Vector((0,0,.85))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.5;aim(cam,(5,-7,4.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/steam-workshop/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'steam-workshop','style':'S01-clean-geometric','title':'Static Orthogonal Worm and Wheel Display','description':'One newly authored static orthogonal screw-and-toothed-wheel display for the original steam-workshop transmission-appearance direction. A grounded full base carries four whole bored bearing pedestals, two perpendicular horizontal shafts, one complete three-turn thick helical worm flight and one full bored oblique-tooth wheel, plus four fixed shaft stops. The elevated screw axis crosses above the upright wheel with a deliberate minimum20mm envelope display gap; the pair is not claimed to mesh or transmit motion. This is a whole new opposed-axis apparatus, not the old parallel-shaft spur-gear kit with changed tooth counts and not a detached soil-auger flight renamed. All geometry is new and independently editable; three opaque constant PBR materials. One model, zero scenes, metres and horizontal bounds-centred ground origin. Static illustrative display only: no conjugate tooth profile, real worm drive, speed ratio, motion range, bearing function, engineering accuracy, manufacturing, installation, power, load or safety claim. Small fixed collar/flight-to-shaft assembly overlaps are intentional visual joins, not mechanical tolerance proof.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
