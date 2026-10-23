import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='steam-workshop-static-open-cage-differential-display-01'
G={};FM={}
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def unit(a):return tuple(x/math.sqrt(dot(a,a))for x in a)
def mesh(name,v,faces,mat):
 f=[]
 for p in faces:
  for k in range(1,len(p)-1):f.append((p[0],p[k],p[k+1]))
 if sum(dot(v[a],cross(v[b],v[c]))for a,b,c in f)<0:f=[tuple(reversed(p))for p in f]
 G[name]=(v,f,mat)
BOX=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(name,c,size,mat):mesh(name,[tuple(c[i]+s[i]*size[i]/2 for i in range(3))for s in[(x,y,z)for z in[-1,1]for y in[-1,1]for x in[-1,1]]],BOX,mat)
def beam(name,a,b,width,mat):
 w=unit(sub(b,a));u=unit(cross(w,(1,0,0)if abs(w[0])<.9 else(0,1,0)));v=cross(w,u)
 mesh(name,[tuple(p[i]+width/2*(sx*u[i]+sy*v[i])for i in range(3))for p in[a,b]for sy in[-1,1]for sx in[-1,1]],BOX,mat)
def axle(name,x0,x1,y,z,r,mat,n=16):
 v=[(x,y+r*math.cos(math.tau*i/n),z+r*math.sin(math.tau*i/n))for x in[x0,x1]for i in range(n)]
 mesh(name,v,[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],mat)

def lathe_z(name,x,y,profile,mat,n=24):
 v=[];rings=[];f=[]
 for r,z in profile:
  ids=[]
  if r==0:ids=[len(v)];v.append((x,y,z))
  else:
   for i in range(n):ids.append(len(v));v.append((x+r*math.cos(math.tau*i/n),y+r*math.sin(math.tau*i/n),z))
  rings.append(ids)
 for a,b in zip(rings,rings[1:]+rings[:1]):
  if len(a)==len(b)==1:continue
  for i in range(n):
   j=(i+1)%n
   if len(a)==1:f.append((a[0],b[j],b[i]))
   elif len(b)==1:f.append((a[i],a[j],b[0]))
   else:f.append((a[i],a[j],b[j],b[i]))
 mesh(name,v,f,mat)

# A single connected two-window carrier around axis X, not separate floating hoops.
# The two wide side apertures reveal four non-meshing bevel-gear display forms.
def carrier():
 xs=[-.42,-.36,.36,.42];rs=[.095,.40,.46];n=48;occ=set()
 for i in range(3):
  for j in range(2):
   for k in range(n):
    t=math.tau*(k+.5)/n
    if i!=1 or(j==1 and abs(math.cos(t))<.26):occ.add((i,j,k))
 v=[];f=[];idx={}
 for i,j,k in sorted(occ):
  c=[(x,r*math.cos(t),1+r*math.sin(t))for t in[math.tau*k/n,math.tau*(k+1)/n]for r in[rs[j],rs[j+1]]for x in[xs[i],xs[i+1]]]
  neighbors=[(i,j,(k-1)%n),(i,j,(k+1)%n),(i,j-1,k),(i,j+1,k),(i-1,j,k),(i+1,j,k)]
  for face,nb in zip(BOX,neighbors):
   if nb in occ:continue
   ids=[]
   for p in [c[h]for h in face]:
    p=tuple(round(q,12)for q in p)
    if p not in idx:idx[p]=len(v);v.append(p)
    ids.append(idx[p])
   f.append(ids)
 mesh('WholeTwoWindowIntegralCarrier',v,f,0)
carrier()
# Complete X-axis annuli; through bores are occupied or deliberately clear as named.
def annulus_x(name,x0,x1,ri,ro,mat,n=48):
 loops=[[(x,r*math.cos(math.tau*i/n),1+r*math.sin(math.tau*i/n))for i in range(n)]for x,r in[(x0,ri),(x0,ro),(x1,ro),(x1,ri)]]
 v=sum(loops,[]);f=[]
 for j in range(4):
  for i in range(n):k=(i+1)%n;f.append((j*n+i,j*n+k,((j+1)%4)*n+k,((j+1)%4)*n+i))
 mesh(name,v,f,mat)
for sign,label in[(-1,'Left'),(1,'Right')]:
 a,b=sorted([sign*.405,sign*.67]);annulus_x(label+'CarrierJournal',a,b,.095,.14,2)
 a,b=sorted([sign*.14,sign*.88]);axle(label+'WholeOutputStubShaft',a,b,0,1,.06,2,24)
 a,b=sorted([sign*.77,sign*.805]);annulus_x(label+'FixedShaftStop',a,b,.058,.09,2,24)
# New conical tooth flanks, continuous with their full bored gear bodies.
# All opposed cone envelopes retain a visible finite gap; no functional mesh claimed.
def bevel(name,axis,sign,mat):
 count=16 if axis=='X'else 12;n=count*4
 angles=[math.tau*(k+t)/count for k in range(count)for t in[-.5,-.22,.22,.38]]
 # Four samples/tooth: low/high/high/low with a finite valley between teeth.
 heights=[h for k in range(count)for h in[0,.018,.018,0]]
 end=.34 if axis=='X'else.30;bore=.058 if axis=='X'else.044
 profile=[(.17,'outer'),(end,'outer'),(end,'bore'),(.17,'bore')]
 def p(a,r,t):
  return(sign*a,r*math.cos(t),1+r*math.sin(t))if axis=='X'else(r*math.cos(t),r*math.sin(t),1+sign*a)
 loops=[]
 for a,kind in profile:loops.append([p(a,(a-.045+h if kind=='outer'else bore),t)for t,h in zip(angles,heights)])
 v=sum(loops,[]);f=[]
 for j in range(4):
  for i in range(n):k=(i+1)%n;f.append((j*n+i,j*n+k,((j+1)%4)*n+k,((j+1)%4)*n+i))
 mesh(name,v,f,mat)
for sign,label in[(-1,'Left'),(1,'Right')]:
 bevel(label+'WholeConicalSideGear','X',sign,1)
 a,b=sorted([sign*.333,sign*.375]);annulus_x(label+'SideGearFixedThrustCollar',a,b,.058,.125,1)
for sign,label in[(-1,'Lower'),(1,'Upper')]:bevel(label+'WholeConicalSpiderGear','Z',sign,3)
lathe_z('WholeCarrierCrossPin',0,0,[(0,.545),(.045,.545),(.045,1.455),(0,1.455)],2,24)
# Two bored pedestals hold the carrier journals; each is one complete closed solid.
def pedestal(name,x0,x1):
 angles=sorted(set([math.tau*i/32 for i in range(32)]+[math.atan2(z-1,y)%math.tau for y in[-.24,.24]for z in[.10,1.22]]));n=len(angles);rings=[]
 for x,inside in[(x0,False),(x1,False),(x1,True),(x0,True)]:
  ring=[]
  for t in angles:
   dy,dz=math.cos(t),math.sin(t);ts=[]
   if abs(dy)>1e-12:ts.append((.24 if dy>0 else-.24)/dy)
   if abs(dz)>1e-12:ts.append(((1.22 if dz>0 else.10)-1)/dz)
   rad=.139 if inside else min(q for q in ts if q>0)
   ring.append((x,rad*dy,1+rad*dz))
  rings.append(ring)
 v=sum(rings,[]);f=[]
 for j in range(4):
  for i in range(n):k=(i+1)%n;f.append((j*n+i,j*n+k,((j+1)%4)*n+k,((j+1)%4)*n+i))
 mesh(name,v,f,0)
for x,label in[(-.58,'Left'),(.58,'Right')]:pedestal(label+'WholeBoredPedestal',x-.07,x+.07)
box('WholeGroundedDisplayBase',(0,0,.06),(1.82,1.10,.12),0)
PALETTE=[('CarrierPedestals_MutedPetrol',(.07,.20,.21,1),.67,.25),('SideCones_WarmBrass',(.60,.34,.10,1),.47,.55),('JournalsShafts_DarkSteel',(.22,.26,.28,1),.40,.65),('SpiderCones_WarmSteel',(.55,.57,.55,1),.46,.60)]
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
for prefix in []:
 parent=bpy.data.objects.new(prefix+'_CompleteSourceAssembly',None);scene.collection.objects.link(parent)
 for o in parts:
  if o.name.startswith(prefix+'__'):o.parent=parent
 parent.select_set(True)
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
triangles=sum(len(f)for v,f,m in G.values())
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
(OUT/'qa-report.json').write_text(json.dumps({'asset':ASSET,'mesh_objects':len(G),'triangles':triangles,'materials':len(PALETTE),'new_independent_models':1,'new_scenes':0},indent=2))
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
focus=Vector((0,0,.79))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.35;aim(cam,(3,-7,3.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/steam-workshop/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'steam-workshop','style':'S01-clean-geometric','title':'Static Open-Cage Differential Display','description':'One newly authored whole static differential-layout display. A single connected carrier has two broad real side windows, two full annular end plates and two continuous longitudinal bridges. Two coaxial output stub shafts carry opposed hollow conical side gears; a perpendicular carrier crosspin carries upper and lower conical spider gears. Tooth flanks taper with the cones and belong to each whole gear, not attached blocks. Carrier journals, two complete bored pedestals and one finite grounded base complete the assembly. This differs structurally from a flat parallel-axis spur pair and a skew-axis screw/wheel: the crossed internal four-cone arrangement, coaxial outputs and enclosing open carrier are all new geometry. Deliberate visible gaps separate the opposing cone envelopes; it is an illustrative static apparatus, not a conjugately meshed or functioning differential. Closed editable components with fixed overlapping support joins, four constant opaque PBR materials, metres, Z up and ground-centred origin. One model, zero scenes. No rotation, differential action, torque, speed ratio, lubrication, bearing fit, working gear accuracy, engineering, manufacture, loading or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
