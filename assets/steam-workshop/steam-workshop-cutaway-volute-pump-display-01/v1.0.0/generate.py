import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='steam-workshop-cutaway-volute-pump-display-01'
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

def ringx(name,x0,x1,y,z,ri,ro,mat,n=24):
 v=[(x,y+r*math.cos(math.tau*i/n),z+r*math.sin(math.tau*i/n))for x in[x0,x1]for r in[ri,ro]for i in range(n)];f=[]
 for i in range(n):j=(i+1)%n;f.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 mesh(name,v,f,mat)
def cyly(name,y0,y1,x,z,r,mat,n=24):
 axle(name,y0,y1,x,z,r,mat,n);v,f,m=G[name];G[name]=([(b,a,c)for a,b,c in v],[tuple(reversed(p))for p in f],m)
def ringy(name,y0,y1,x,z,ri,ro,mat,n=24):
 ringx(name,y0,y1,x,z,ri,ro,mat,n);v,f,m=G[name];G[name]=([(b,a,c)for a,b,c in v],[tuple(reversed(p))for p in f],m)
def triangulate(p):
 def cr(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 ids=list(range(len(p)));out=[]
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:ids.reverse()
 while len(ids)>3:
  for k,b in enumerate(ids):
   a,c=ids[k-1],ids[(k+1)%len(ids)]
   if cr(p[a],p[b],p[c])<=1e-14:continue
   if any(min(cr(p[a],p[b],p[j]),cr(p[b],p[c],p[j]),cr(p[c],p[a],p[j]))>=-1e-14 for j in ids if j not in[a,b,c]):continue
   out.append((a,b,c));ids.pop(k);break
  else:raise AssertionError('bad polygon')
 return out+[tuple(ids)]
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



# One entire expanding spiral casing, not a resized straight axial fan duct.
ZC=.84;N=48
rads=[.465+.205*i/(N-1)for i in range(N)]
# Radial step at the cutoff closes the spiral perimeter. Front is intentionally removed.
profiles=[]
for i,r in enumerate(rads):
 a=math.tau*i/N
 profiles.append([(rr*math.cos(a),y,ZC+rr*math.sin(a))for rr,y in[(.085,.155),(r+.060,.155),(r+.060,-.18),(r,-.18),(r,.095),(.085,.095)]])
v=[profiles[i][k]for k in range(6)for i in range(N)];f=[]
for k in range(6):
 for i in range(N):j=(i+1)%N;l=(k+1)%6;f.append((k*N+i,k*N+j,l*N+j,l*N+i))
mesh('WholeOpenFrontExpandingVoluteCasing',v,f,0)
box('WholeGroundBed',(0,.22,.055),(1.44,1.48,.11),2)
for label,x in [('Left',-.36),('Right',.36)]:
 box(label+'WholeCasingFoot',(x,.015,.20),(.19,.27,.23),0)
 # Root intersects the lower spiral shell with finite volume, not a floating pedestal.
 beam(label+'WholeSlopingCasingRoot',(x,.015,.28),(x,.015,.40),.14,0)
# Whole back impeller disk, fixed hub and six continuously curved thick blades.
ringy('WholeImpellerBackplate',.025,.085,0,ZC,.070,.405,1,40)
cyly('WholeFixedImpellerHub',-.22,.11,0,ZC,.105,1,24)
for k in range(6):
 ang=math.tau*k/6;p=[]
 for sign,seq in [(1,range(9)),(-1,reversed(range(9)))]:
  for i in seq:
   t=i/8;r=.095+.295*t;a=ang+.70*t;p.append((r*math.cos(a)+sign*.012*math.sin(a),ZC+r*math.sin(a)-sign*.012*math.cos(a)))
 n=len(p);v=[(x,y,z)for y in[-.105,.045]for x,z in p];f=[]
 for a,b,c in triangulate(p):f.extend([(a,b,c),(c+n,b+n,a+n)])
 f += [(i,i+n,(i+1)%n+n,(i+1)%n)for i in range(n)];mesh('WholeCurvedImpellerBlade'+str(k+1),v,f,1)
# Cut-away intake collar remains on three short complete radial bridges. No sealed front cover claimed.
ringy('WholeAxialIntakeCollar',-.43,-.165,0,ZC,.135,.185,0,32)
for k in range(3):
 a=math.tau*(k+.5)/3;r=.465+.205*((a%math.tau)/math.tau)
 beam('WholeRemainingFrontBridge'+str(k+1),(.17*math.cos(a),-.17,ZC+.17*math.sin(a)),((r+.025)*math.cos(a),-.17,ZC+(r+.025)*math.sin(a)),.045,0)
# Tangential upward hollow outlet, rooted into the broad cutoff region; interior connection not validated.
lathe_z('WholeTangentialOutletNeck',.595,0,[(.070,.78),(.105,.78),(.105,1.50),(.145,1.50),(.145,1.56),(.070,1.56)],0,24)
# Entire shaft, two bored bearing pedestals and separate fixed drive pulley on the common bed.
cyly('WholeRearDriveShaft',.06,.94,0,ZC,.047,2,24)
for label,y in [('Near',.39),('Rear',.70)]:
 box(label+'WholeBearingPedestal',(0,y,.42),(.22,.15,.64),2)
 ringy(label+'WholeBoredShaftBearing',y-.065,y+.065,0,ZC,.047,.125,2,24)
# Profile is around Y via the established Y-axis transform, with bore around fixed shaft.
lathe_z('WholeDoubleFlangedDrivePulley',0,0,[(.047,.80),(.225,.80),(.225,.835),(.19,.85),(.19,.89),(.225,.905),(.225,.94),(.047,.94)],1,32)
v,f,m=G['WholeDoubleFlangedDrivePulley'];G['WholeDoubleFlangedDrivePulley']=([(x,z,ZC+y)for x,y,z in v],[tuple(reversed(t))for t in f],m)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('CutawayVolute_DeepTeal',(.095,.24,.25,1),.65,.25),('ImpellerAndPulley_OchreMetal',(.55,.34,.12,1),.52,.55),('BedShaftAndPedestals_DarkIron',(.17,.19,.20,1),.65,.40)]
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
focus=Vector((0,0,.78))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.45;aim(cam,(4,-7,3.6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/steam-workshop/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'steam-workshop','style':'S01-clean-geometric','title':'Cutaway Volute Pump Display','description':'One new whole static cutaway volute-pump display. An entire spiral-expanding thick casing has a real front opening and annular rear wall, around a separate backplate, central hub and six continuously curved impeller blades. A front axial annular intake collar remains supported by three fixed narrow bridges where the front cover is deliberately removed; a tall tangential annular outlet neck rises beside the cutoff. One grounded bed supports the casing feet, rear common shaft, two bored bearing pedestals and a double-flanged drive pulley. The new radial impeller/expanding collection casing/tangential branch topology differs from the old straight open axial-fan duct and from old vertical lever or twin-treadle piston-style pumps. All geometry newly authored rather than extracted or rearranged old objects. Three opaque constant PBR roles; closed editable solids, metres, Z up and whole horizontal ground-centred datum. One prop, zero scenes. Simplified fixed illustrative joins only; the exposed cutaway is not a sealed hydraulic chamber. Outlet neck root is a static overlap, not a validated continuous fluid passage. No rotation, pumping, pressure, flow, sealing, efficiency, belt engagement, manufacture, structural performance or equipment safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
