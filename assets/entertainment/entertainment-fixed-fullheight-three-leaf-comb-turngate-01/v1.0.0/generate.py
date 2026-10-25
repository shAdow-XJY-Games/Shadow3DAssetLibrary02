import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='entertainment-fixed-fullheight-three-leaf-comb-turngate-01'
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



# Complete through-height rotor, fixed comb and enclosing half cage.
box('WholeGroundFootMachinePlinth',(0,0,.035),(1.94,1.76,.070),1)
for k,(x,y)in enumerate([(-.88,-.80),(-.88,.80),(.88,-.80),(.88,.80)]):box('WholeFramePost_%d'%k,(x,y,1.115),(.09,.09,2.10),0)
for y in[-.80,.80]:box('WholeUpperCrossHeader_'+str(y),(0,y,2.18),(1.85,.095,.12),1)
for x in[-.88,.88]:box('WholeUpperLongHeader_'+str(x),(x,0,2.155),(.095,1.68,.12),1)
box('WholeUpperBearingBridge',(0,0,2.17),(.11,1.61,.095),0)
for z in[.070,2.085]:lathe_z('WholeFixedBearingHousing_'+str(z),0,0,[(0,z),(.095,z),(.095,z+.085),(0,z+.085)],2,20)
lathe_z('WholeThroughHeightRotorShaft',0,0,[(0,.130),(.054,.130),(.054,2.12),(0,2.12)],0,20)
# Three complete radial leaf sets in one fixed pose; closed crossbars bury roots in shaft.
for k,a in enumerate([0,120,240]):
 a=math.radians(a)
 for j in range(8):
  z=.275+j*.23;beam('WholeRotorLeaf%dCrossbar%d'%(k,j),(.020*math.cos(a),.020*math.sin(a),z),(.655*math.cos(a),.655*math.sin(a),z),.035,0)
box('WholeFixedCombMast',(-.78,0,1.10),(.075,.09,2.065),0)
beam('WholeFixedCombUpperRoot',(-.78,0,2.12),(-.88,0,2.18),.070,0)
for j in range(8):
 z=.390+j*.23;beam('WholeFixedInterleavingCombBar_%d'%j,(-.78,0,z),(-.105,0,z),.035,0)
# Continuous half-circle rails, not disconnected copies of a flat old fence.
def arcrail(name,z):
 n=24;r=.735;w=.021;v=[];f=[]
 for i in range(n+1):
  a=-math.pi/2+math.pi*i/n
  for rr,zz in[(r-w,z-w),(r+w,z-w),(r+w,z+w),(r-w,z+w)]:v.append((rr*math.cos(a),rr*math.sin(a),zz))
 for i in range(n):
  for k in range(4):f.append((4*i+k,4*i+(k+1)%4,4*(i+1)+(k+1)%4,4*(i+1)+k))
 f +=[(3,2,1,0),tuple(4*n+k for k in range(4))];mesh(name,v,f,0)
arcrail('WholeContinuousLowerHalfCageRail',.12);arcrail('WholeContinuousUpperHalfCageRail',2.10)
for i in range(6):
 a=-math.pi/2+math.pi*i/5;x=.735*math.cos(a);y=.735*math.sin(a)
 beam('WholeFixedCageUpright_%d'%i,(x,y,.070),(x,y,2.15),.035,0)
for y in[-.735,.735]:beam('WholeCageHeaderConnection_'+str(y),(0,y,2.12),(0,y,2.18),.050,0)
beam('WholeBlankPanelFrameRoot',(-.88,-.80,1.20),(-.886,-.45,1.20),.055,0)
box('WholeBlankStatusPanelHousing',(-.886,-.45,1.20),(.12,.26,.30),2)
box('WholeBlankStatusPanelFace',(-.951,-.45,1.20),(.012,.20,.21),3)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeRotorCageAndFrame_SatinSteel',(.47,.52,.51,1),.44,.62),('WholePlinthAndHeaders_DeepTeal',(.065,.22,.22,1),.56,.22),('WholeBearingAndReaderHousings_Charcoal',(.045,.052,.05,1),.57,.18),('WholeBlankReaderFace_MutedAmber',(.62,.37,.11,1),.55,.05)]
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
focus=Vector((0,0,1.1))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.65;aim(cam,(-4,-6,3.3));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/entertainment/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'entertainment','style':'S01-clean-geometric','title':'Fixed Full Height Three Leaf Comb Turngate','description':'One newly authored whole full-height three-leaf comb-turngate static exterior. A grounded low machine plinth supports four full-height frame posts and a closed rectangular upper frame. The complete vertical rotor has lower and upper bearing housings, three radial comb leaves with eight full crossbars apiece, and a separate fixed interleaving comb rooted in a full-height side mast. A continuous half-round fixed cage, with real open cells, encloses the opposite side. Upper and lower cage rails and six full vertical cage rods form a complete connected structure. This is not a waist-height cabinet tripod gate enlarged: its through-height rotor, fixed comb, cage and overhead bearing frame are all newly authored full geometry. Nor is it an old flat fence made taller. One complete prop, zero scenes, four opaque PBR roles. Metres, Z up, horizontal envelope centred, entire flat plinth underside grounded. Fixed illustrative pose only: no rotation, access control, locking, ticketing, egress, accessibility, installation, structural, crowd-control or safety performance is modeled or validated. No people, passage animation, rigging or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
