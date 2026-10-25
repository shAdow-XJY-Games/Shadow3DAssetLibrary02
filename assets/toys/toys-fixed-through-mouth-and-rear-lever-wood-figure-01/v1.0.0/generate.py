import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='toys-fixed-through-mouth-and-rear-lever-wood-figure-01'
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



def boundary_solid(name,xs,ys,zs,filled,mat):
 cells={(i,j,k)for i in range(len(xs)-1)for j in range(len(ys)-1)for k in range(len(zs)-1)if filled((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)}
 vv=[];ff=[];idx={}
 def ids(coords):
  out=[]
  for q in coords:
   if q not in idx:idx[q]=len(vv);vv.append(q)
   out.append(idx[q])
  return tuple(out)
 for i,j,k in sorted(cells):
  x,X=xs[i:i+2];y,Y=ys[j:j+2];z,Z=zs[k:k+2]
  faces=[((-1,0,0),[(x,y,z),(x,y,Z),(x,Y,Z),(x,Y,z)]),((1,0,0),[(X,y,z),(X,Y,z),(X,Y,Z),(X,y,Z)]),((0,-1,0),[(x,y,z),(X,y,z),(X,y,Z),(x,y,Z)]),((0,1,0),[(x,Y,z),(x,Y,Z),(X,Y,Z),(X,Y,z)]),((0,0,-1),[(x,y,z),(x,Y,z),(X,Y,z),(X,y,z)]),((0,0,1),[(x,y,Z),(X,y,Z),(X,Y,Z),(x,Y,Z)])]
  for (a,b,c),q in faces:
   if(i+a,j+b,k+c)not in cells:ff.append(ids(q))
 mesh(name,vv,ff,mat)
lathe_z('WholeGroundFootDisplayPlinth',0,0,[(0,0),(.142,0),(.155,.012),(.155,.032),(.140,.044),(0,.044)],0,32)
for j,s in enumerate([-1,1]):
 # Entire shoes and legs rooted into the same base; there is no floating character support.
 poly=[(-.112,.040),(.050,.040),(.061,.060),(.045,.089),(-.055,.089),(-.101,.075)]
 n=len(poly);v=[(x,y,z)for x in[s*.045-.030,s*.045+.030]for y,z in poly];f=[]
 for a,b,c in triangulate(poly):f +=[(c,b,a),(a+n,b+n,c+n)]
 f +=[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh('WholeLongWoodShoe_%d'%j,v,f,3)
 lathe_z('WholeWoodLeg_%d'%j,s*.045,.005,[(0,.075),(.025,.075),(.027,.105),(.026,.246),(0,.246)],1,16)
lathe_z('WholeShapedSolidTorso',0,.007,[(0,.223),(.063,.223),(.073,.251),(.068,.346),(.085,.389),(.073,.415),(0,.415)],2,20)
lathe_z('WholeShortNeck',0,.007,[(0,.397),(.035,.397),(.035,.454),(0,.454)],1,16)
for j,s in enumerate([-1,1]):
 lathe_z('WholeSimpleWoodArm_%d'%j,s*.096,.007,[(0,.278),(.022,.278),(.025,.301),(.027,.380),(.021,.400),(0,.400)],2,16)
 axle('WholeArmShoulderRoot_%d'%j,min(s*.067,s*.102),max(s*.067,s*.102),.007,.385,.023,2,16)
 lathe_z('WholeBluntWoodHand_%d'%j,s*.096,.007,[(0,.253),(.020,.257),(.024,.272),(.023,.289),(0,.292)],1,16)
# One shared-vertex head with a genuine rectangular tunnel through the mouth region.
boundary_solid('WholeThroughMouthWoodHead',[-.066,-.045,.045,.066],[-.055,.055],[.438,.461,.510,.603],lambda x,y,z:z<.461 or z>.510 or abs(x)>.045,1)
# One whole continuous L member: front lower jaw bends down into the long back lever.
poly=[(-.075,.468),(.070,.468),(.070,.324),(.093,.324),(.093,.490),(-.075,.490)]
n=len(poly);v=[(x,y,z)for x in[-.039,.039]for y,z in poly];f=[]
for a,b,c in triangulate(poly):f +=[(c,b,a),(a+n,b+n,c+n)]
f +=[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh('WholeLowerJawAndRearLever',v,f,0)
axle('WholeTransverseJawPin',-.074,.074,.031,.479,.009,3,16)
for j,s in enumerate([-1,1]):axle('WholePinCap_%d'%j,s*.070-.006,s*.070+.006,.031,.479,.014,3,16)
box('WholeUpperLipStrip',(0,-.060,.517),(.094,.015,.017),0)
box('WholeLowerJawLip',(0,-.078,.488),(.072,.014,.012),1)
lathe_z('WholeLowPlainCap',0,0,[(0,.594),(.074,.594),(.082,.606),(.078,.623),(.061,.637),(0,.637)],3,24)
for j,s in enumerate([-1,1]):
 cyly('WholeSmallEye_%d'%j,-.062,-.052,s*.027,.567,.008,3,12)
 box('WholeBrow_%d'%j,(s*.027,-.061,.581),(.027,.013,.006),0)
mesh('WholeBluntCarvedNose',[(-.012,-.054,.542),(.012,-.054,.542),(.009,-.083,.542),(-.009,-.083,.542),(-.011,-.054,.565),(.011,-.054,.565),(.008,-.078,.554),(-.008,-.078,.554)],[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholePlinthJawAndBrow_Walnut',(.31,.16,.060,1),.78,0),('WholeFaceHandsAndLegs_Maple',(.65,.44,.23,1),.76,0),('WholeTorsoAndArms_MutedRed',(.48,.105,.065,1),.76,0),('WholeShoesCapAndPins_Charcoal',(.045,.055,.052,1),.73,.05)]
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
focus=Vector((0,0,.315))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.84;aim(cam,(3,-7,3.0));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/toys/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'toys','style':'S01-clean-geometric','title':'Fixed Through Mouth and Rear Lever Wood Figure','description':'One independently authored whole wooden lever-jaw figure in a fixed standing display pose. A broad finite plinth holds two full long shoes, separate legs and one shaped solid torso with two simple complete arms and blunt hands. A thick continuous head has a real front-to-back rectangular mouth tunnel. One entire bent lower-jaw and long rear lever member passes through that mouth around a separately supported transverse pin, leaving a visibly open gap beneath the upper lip. A low plain cap, nose, two eyes and simple cheek details finish the new stylized wooden character. Unlike a suspended marionette it has no overhead strings, jointed elbows or knees, or control cross; unlike an empty dental articulator it has a full standing figure and an integral rear-handled jaw member instead of opposed mounting discs. All visible coordinates newly authored; no old puppet, clamp or human mesh imported. Four opaque constant PBR materials, one whole toy prop zero scenes, metres native Z up and full horizontal-bounds-centred ground datum. Static nutcracker-inspired exterior only, no food or nut present: no lever motion, bite force, joint range, crushing, food-contact suitability, child suitability, pinch protection, manufacture, toy operation or safety claim. No historical costume attribution, rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
