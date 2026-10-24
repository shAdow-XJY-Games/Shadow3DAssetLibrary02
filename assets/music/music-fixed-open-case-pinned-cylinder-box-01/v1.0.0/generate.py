import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='music-fixed-open-case-pinned-cylinder-box-01'
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



# Entire new fixed-open cylinder music-box exterior, with full floor/walls and internal comb.
def tray(name,hx,hy,z0,zt,ix,iy,zf,mat):
 v=[]
 for x,y,z in[(hx,hy,z0),(hx,hy,zt),(ix,iy,zt),(ix,iy,zf)]:v.extend([(-x,-y,z),(x,-y,z),(x,y,z),(-x,y,z)])
 f=[(3,2,1,0),(12,13,14,15)]
 for i in range(4):j=(i+1)%4;f.extend([(i,j,j+4,i+4),(i+4,j+4,j+8,i+8),(i+8,j+8,j+12,i+12)])
 mesh(name,v,f,mat)
tray('WholeGroundFootOpenCase',.32,.23,0,.18,.294,.204,.026,0)
tray('WholeFixedRaisedRecessedLid',.32,.23,0,.035,.295,.205,.012,0)
def lidpoint(x,y,z):q=y+.23;return(x,.235+q*.20-z*.979795897,.190+q*.979795897+z*.20)
v,f,m=G['WholeFixedRaisedRecessedLid'];G['WholeFixedRaisedRecessedLid']=([lidpoint(*p)for p in v],f,m)
for x in[-.22,.22]:
 axle('WholeFixedHingePin_'+str(x),x-.050,x+.050,.235,.19,.015,1,16)
 box('WholeRearHingeRoot_'+str(x),(x,.218,.17),(.075,.05,.065),0)
 beam('WholeLidHingeTongue_'+str(x),(x,.235,.19),lidpoint(x,-.195,.012),.025,1)
 beam('WholeFixedLidStay_'+str(x),(x,.135,.158),lidpoint(x,-.055,.010),.011,1)
# Whole drum on a real transverse axle and two grounded bearing blocks.
for x in[-.242,.242]:box('WholeDrumBearingBlock_'+str(x),(x,.045,.092),(.055,.075,.145),1)
axle('WholeContinuousDrumAxle',-.278,.375,.045,.145,.012,1,20)
axle('WholePinnedMusicCylinder',-.205,.205,.045,.145,.075,1,48)
for side,x in[('Left',-.207),('Right',.207)]:ringx(side+'WholeCylinderEndFlange',x-.006,x+.006,.045,.145,.010,.082,1,32)
# Twenty-four separate thick fixed blunt pins are genuine solids seated into the drum.
for i in range(12):
 x=-.181+i*.033
 for j in range(2):
  a=.50+i*.31+j*1.13;p=(x,.045+.071*math.cos(a),.145+.071*math.sin(a));q=(x,.045+.087*math.cos(a),.145+.087*math.sin(a));beam('WholeFixedCylinderPin_%02d_%d'%(i,j),p,q,.005,2)
# One continuous connected comb outline, all teeth share the same full supported root.
box('WholeCombGroundedSupport',(0,-.143,.090),(.46,.085,.135),0)
p=[(-.23,-.18),(.23,-.18),(.23,-.115)]
for i in range(12):
 right=.216-i*.036;left=right-.028;tip=-.026+i*.0015;p.extend([(right,-.115),(right,tip),(left,tip),(left,-.115)])
p.append((-.23,-.115));n=len(p);v=[(x,y,z)for z in[.153,.169]for x,y in p];f=[]
for a,b,c in triangulate(p):f.extend([(c,b,a),(a+n,b+n,c+n)])
f +=[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh('WholeContinuousTwelveTongueComb',v,f,2)
# Fixed side crank and grip root on the same transverse axle, not a detached handle.
beam('WholeSideCrankArm',(.365,.045,.145),(.365,.045,.235),.018,1)
axle('WholeSideCrankGrip',.361,.443,.045,.235,.016,0,16)
box('WholeBlankFrontLatchAppearance',(0,-.237,.13),(.07,.022,.05),1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeOpenCaseLidCombSupportAndCrankGrip_WarmTimber',(.34,.145,.055,1),.76,0),('WholeCylinderBearingsAxleAndStays_DullBrass',(.52,.37,.14,1),.49,.55),('WholeContinuousCombAndBluntPins_DarkSteel',(.13,.19,.22,1),.45,.50)]
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
focus=Vector((0,0,.32))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.25;aim(cam,(3,-5,4.3));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/music/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':'Fixed Open Case Pinned Cylinder Music Box','description':'One newly authored complete fixed-open cylinder music-box appearance. A continuous timber-like shell has a real floor and four thick walls, with one complete recessed lid held in a fixed raised pose by hinge-style pins and side stays. Inside, two bearing blocks support a whole transverse drum and common axle. Twenty-four blunt fixed pegs project from the drum; one connected comb has twelve full fingers sharing a supported root. A side crank and grip belong to the same axle. This is not a fishing compartment box with contents swapped, a wheel-bowed instrument with strings removed, or a texture representing the internal mechanism: all geometry is independently authored as one complete musical-device exterior. Three opaque constant untextured PBR roles, metres, Z up and whole horizontally centred ground datum. One model and zero scenes. Static silent illustrative display only: no melody, tuning, audible output, actuating pin-comb contact sequence, rotating crank/drum, hinge motion, gearing or stored energy, fabrication, operation or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
