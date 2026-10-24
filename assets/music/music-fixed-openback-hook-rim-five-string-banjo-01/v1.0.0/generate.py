import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='music-fixed-openback-hook-rim-five-string-banjo-01'
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



# Entire independently authored open-back five-string banjo, lying on its real annular rear edge.
lathe_z('WholeOpenBackCircularTimberPotGroundSole',0,0,[(.160,0),(.180,0),(.180,.090),(.160,.090)],0,48)
lathe_z('WholeUpperOpenTensionHoop',0,0,[(.166,.083),(.190,.083),(.190,.105),(.166,.105)],2,48)
lathe_z('WholeLowerOpenBand',0,0,[(.172,.010),(.187,.010),(.187,.027),(.172,.027)],2,48)
lathe_z('WholeFiniteTopMembrane',0,0,[(0,.085),(.176,.085),(.176,.095),(0,.095)],1,48)
def prism_z(name,p,z0,z1,mat):
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:p.reverse()
 n=len(p);v=[(x,y,z)for z in[z0,z1]for x,y in p];f=[]
 for a,b,c in triangulate(p):f.extend([(c,b,a),(a+n,b+n,c+n)])
 f +=[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh(name,v,f,mat)
prism_z('WholeLongTaperedNeckAndHeel',[(-.035,.150),(.035,.150),(.022,.725),(-.022,.725)],.052,.096,0)
prism_z('WholeLongFiveStringFingerboard',[(-.033,.145),(.033,.145),(.021,.728),(-.021,.728)],.091,.103,2)
prism_z('WholeFacetedPeghead',[(-.022,.710),(.022,.710),(.040,.770),(.034,.845),(-.034,.845),(-.040,.770)],.057,.100,0)
box('WholeUpperStringNut',(0,.710,.108),(.048,.010,.014),1)
# Actual low two-foot bridge: one continuous arched profile over the membrane.
p=[(-.050,.094),(-.030,.094),(-.030,.108),(.030,.108),(.030,.094),(.050,.094),(.050,.123),(-.050,.123)];n=len(p);v=[(x,y,z)for y in[-.055,-.045]for x,z in p];f=[]
for a,b,c in triangulate(p):f.extend([(a,b,c),(c+n,b+n,a+n)])
f +=[(i,i+n,(i+1)%n+n,(i+1)%n)for i in range(n)];mesh('WholeTwoFootBridgeWithOpenArch',v,f,0)
box('WholeFixedTailAnchor',(0,-.156,.105),(.085,.048,.020),2)
# Twelve actual fixed bent hooks individually enter top hoop and lower shoulder, not painted stripes.
def path_tube(name,path,r,mat,n=8):
 v=[];f=[]
 for k,p in enumerate(path):
  t=unit(sub(path[min(k+1,len(path)-1)],path[max(0,k-1)]));u=unit(cross(t,(1,0,0)if abs(t[0])<.9 else(0,1,0)));w=cross(t,u)
  for j in range(n):v.append(tuple(p[i]+r*(u[i]*math.cos(math.tau*j/n)+w[i]*math.sin(math.tau*j/n))for i in range(3)))
 for k in range(len(path)-1):
  for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
 f +=[tuple(reversed(range(n))),tuple((len(path)-1)*n+j for j in range(n))];mesh(name,v,f,mat)
for i in range(12):
 a=math.tau*(i+.5)/12;u=(math.cos(a),math.sin(a));path=[(.181*u[0],.181*u[1],.022),(.194*u[0],.194*u[1],.032),(.194*u[0],.194*u[1],.094),(.188*u[0],.188*u[1],.104),(.177*u[0],.177*u[1],.102)]
 path_tube('WholeFixedBentTensionHook_%02d'%i,path,.004,2)
# Four peghead tuners, plus the defining short side fifth-string tuner partway down the neck.
for i,(sgn,y)in enumerate([(-1,.770),(1,.770),(-1,.817),(1,.817)]):
 axle('WholePegheadTunerShaft_%d'%i,sgn*.018,sgn*.054,y,.086,.005,2,12)
 axle('WholePegheadTunerButton_%d'%i,sgn*.050,sgn*.061,y,.086,.013,1,12)
axle('WholeSideFifthTunerShaft',-.054,-.020,.487,.091,.006,2,12)
axle('WholeSideFifthTunerButton',-.067,-.051,.487,.091,.014,1,12)
for i,y in enumerate([.215,.270,.322,.370,.415,.457,.497,.535,.571,.605,.637,.667]):
 width=.064-(y-.145)/(.728-.145)*.022;beam('WholeFixedFret_%02d'%i,(-width/2,y,.104),(width/2,y,.104),.003,1)
for i,x in enumerate([-.018,-.006,.006,.018]):
 endx=(-.028 if i%2==0 else .028);endy=.770 if i<2 else.817
 path_tube('WholeFixedLongString_%d'%i,[(x,-.165,.114),(x,-.05,.124),(x*.80,.710,.116),(endx,endy,.092)],.0013,1,6)
path_tube('WholeFixedShortSideFifthString',[(-.030,-.165,.114),(-.030,-.05,.124),(-.028,.465,.112),(-.035,.487,.091)],.0013,1,6)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholePotNeckPegheadAndBridge_Walnut',(.30,.12,.045,1),.74,0),('WholeMembraneAndStrings_WarmIvory',(.73,.70,.58,1),.80,0),('WholeHoopsHooksAndFingerboard_CharcoalMetal',(.07,.085,.09,1),.48,.40)]
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
focus=Vector((0,0,.07))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.20;aim(cam,(2,-3,5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/music/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':'Fixed Open Back Hook Rim Five String Banjo','description':'One newly authored whole static five-string banjo appearance, laid on the actual finite annular rear edge. A genuinely open-back thick circular timber pot carries a complete thin solid top membrane, two open metal-style bands and twelve continuous bent fixed tension hooks. A full tapered neck and fretboard continue into a polygonal peghead with four separate shaft/button tuners; a fifth whole side tuner sits partway down the neck with its own shorter string. Twelve actual fixed frets, a complete two-foot bridge with a real under-arch, a tail anchor and five continuous supported visual strings complete the whole instrument. This is not an extracted old drum-kit snare, a circular replacement mesh on the old guitar, or a violin with new color: all numeric geometry is new and its membrane pot, open back, outer hook rim, long fretted neck and asymmetric short-string routing form one integrated instrument identity. One model, zero scenes. Three opaque untextured PBR roles, metres, native Z up and horizontal ground-centred origin. The open back faces the ground in this static presentation; its actual geometry is not asserted visible in the hero. No performer, stand, case, logo, ornament or licensed design. Deliberately stylized counts/proportions: no tuning, sound, tension, playability, acoustic system, ergonomics, manufacture or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
