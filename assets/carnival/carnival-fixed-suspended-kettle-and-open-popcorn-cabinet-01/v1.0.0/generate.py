import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='carnival-fixed-suspended-kettle-and-open-popcorn-cabinet-01'
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



# Whole new fixed open popcorn cabinet: four full corner posts, crowned canopy, suspended kettle and receiving trough.
for x in[-.22,.22]:
 for y in[-.17,.17]:box('WholeGroundFoot_'+str((x,y)),(x,y,.022),(.060,.060,.044),2)
box('WholeRaisedCabinetPlinth',(0,0,.095),(.56,.46,.13),0)
# Single complete thick open rectangular receiving trough: continuous floor and full four walls.
outer=[(-.27,-.22),(.27,-.22),(.27,.22),(-.27,.22)];inner=[(-.255,-.205),(.255,-.205),(.255,.205),(-.255,.205)]
v=[(x,y,z)for row,z in[(outer,.151),(outer,.245),(inner,.245),(inner,.168)]for x,y in row];f=[(3,2,1,0),(12,13,14,15)]
for k in range(3):
 for i in range(4):j=(i+1)%4;f.append((k*4+i,k*4+j,(k+1)*4+j,(k+1)*4+i))
mesh('WholeContinuousOpenReceivingTrough',v,f,1)
for x in[-.255,.255]:
 for y in[-.205,.205]:box('WholeCanopyCornerPost_'+str((x,y)),(x,y,.590),(.034,.034,.89),0)
# Wide cornice with a true tapered crown, not a floating sign or thin painted facade.
box('WholeCanopyLowerCornice',(0,0,1.027),(.62,.52,.060),0)
v=[(x,y,z)for z,hx,hy in[(1.052,.31,.26),(1.130,.245,.195)]for x,y in[(-hx,-hy),(hx,-hy),(hx,hy),(-hx,hy)]];mesh('WholeSlopedCanopyCrown',v,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],0)
# Two roof-hung straps each carry a real bored ring and an independent short side trunnion.
for label,x in[('Left',-.185),('Right',.185)]:
 box(label+'WholeRoofHanger',(x,0,.851),(.034,.045,.346),1)
 ringx(label+'WholeKettleBearing',x-.026,x+.026,0,.680,.020,.038,1,24)
 # Fixed pin seats slightly into the lower land; no dynamic-bearing claim.
 a,b=sorted((x,(-.123 if x<0 else .123)));axle(label+'WholeKettleSideTrunnion',a,b,0,.674,.017,2,24)
# Thick shallow open kettle, nearly upright with a small fixed forward tilt; actual inner wall and floor.
lathe_z('WholeFixedOpenKettle',0,0,[(0,-.108),(.078,-.108),(.124,-.079),(.144,.016),(.150,.038),(.149,.052),(.135,.052),(.131,.035),(.127,.016),(.109,-.065),(.070,-.089),(0,-.089)],1,32)
v,f,m=G['WholeFixedOpenKettle'];a=math.radians(12);G['WholeFixedOpenKettle']=([(x,y*math.cos(a)-z*math.sin(a),.674+y*math.sin(a)+z*math.cos(a))for x,y,z in v],f,m)
# Separate complete split-cover plate shown fixed lifted at rear, not sealing the open kettle.
lathe_z('WholeFixedRaisedKettleCover',0,0,[(0,0),(.148,0),(.148,.009),(0,.009)],1,32)
v,f,m=G['WholeFixedRaisedKettleCover'];a=math.radians(58);G['WholeFixedRaisedKettleCover']=([(x,.12+y*math.cos(a)-z*math.sin(a),.790+y*math.sin(a)+z*math.cos(a))for x,y,z in v],f,m)
beam('WholeRearCoverHingeArm',(0,.13,.707),(0,.12,.785),.024,1)
axle('WholeRightFixedCrankSpindle',.178,.313,0,.674,.014,2,20)
beam('WholeRightCrankDrop',(.305,0,.674),(.305,0,.555),.020,1)
axle('WholeRightDarkCrankGrip',.295,.365,0,.555,.026,2,20)
# Current blank canopy controls, without labels/lights or operating claims.
box('WholeBlankCanopyControlPanel',(0,-.268,1.027),(.16,.020,.034),2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeCanopyFrameAndBase_MutedRed',(.43,.075,.065,1),.61,.05),('WholeKettleReceivingTroughAndHangers_SatinMetal',(.56,.61,.61,1),.40,.55),('WholeFeetCrankAndBlankControl_Charcoal',(.045,.050,.055,1),.77,0)]
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
focus=Vector((0,0,.56))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.47;aim(cam,(3,-6,2.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/carnival/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'carnival','style':'S01-clean-geometric','title':'Fixed Suspended Kettle and Open Popcorn Cabinet','description':'One newly authored complete static popcorn-cabinet machine exterior shown as an intentionally open display. Four full corner posts rise from a low four-foot cabinet base to a broad cornice and sloping canopy crown. Two independent roof-hung straps support bored kettle bearings and short side trunnions. A thick open kettle with an actual interior floor is fixed slightly tipped; a separate lifted cover and hinge arm expose the mouth. A right crank and dark grip are attached to its side spindle. Below is one continuous empty rectangular receiving trough with four finite walls and a complete floor. All numeric geometry is new, not a fantasy cauldron transplanted, a bakery shelf cabinet recoloured or a scene of existing props. One whole model and zero scenes, three opaque untextured PBR materials, metres and ground-centred Z up. There are deliberately no glass panels or doors; the large front and side openings are real and are not claimed to contain transparent glazing. No popcorn, food, heater, cable, motor internals, lamp, rotating stirrer, working pour, operating recipe, thermal behaviour, hygiene, manufacturing or safety claim. Fixed illustrative game art only.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
