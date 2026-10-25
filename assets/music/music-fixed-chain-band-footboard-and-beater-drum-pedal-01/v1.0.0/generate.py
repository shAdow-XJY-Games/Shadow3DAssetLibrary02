import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='music-fixed-chain-band-footboard-and-beater-drum-pedal-01'
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



# Whole compact pedal device; no drum-kit mesh extracted.
box('WholeGroundFootLongBase',(0,0,.009),(.18,.43,.018),0)
for j,x in enumerate([-.041,.041]):box('WholeHeelHingeRoot_%d'%j,(x,-.174,.034),(.022,.033,.045),0)
axle('WholeHeelHinge',-.058,.058,-.174,.048,.009,1,16)
outline=[(-.035,-.18),(.035,-.18),(.045,-.13),(.047,.040),(.035,.082),(-.035,.082),(-.047,.040),(-.045,-.13)]
def zboard(y):return .048+(y+.174)*.245
n=len(outline);v=[(x,y,zboard(y)+h)for h in[-.006,.006]for x,y in outline];fs=[]
for a,b,c in triangulate(outline):fs.extend([(c,b,a),(a+n,b+n,c+n)])
fs +=[(j,(j+1)%n,(j+1)%n+n,j+n)for j in range(n)];mesh('WholeLongSlopingFootboard',v,fs,1)
for j,y in enumerate([-.11,-.07,-.03,.01]):box('WholeFootboardRaisedGrip_%d'%j,(0,y,zboard(y)+.0075),(.071,.009,.004),3)
for j,x in enumerate([-.058,.058]):
 box('WholeFrontBearingTower_%d'%j,(x,.132,.119),(.027,.044,.204),0)
 ringx('WholeOpenTopShaftBearing_%d'%j,x-.017,x+.017,.132,.230,.009,.022,1,24)
axle('WholeTransverseCamAndBeaterShaft',-.082,.104,.132,.230,.009,1,20)
axle('WholeDriveCam',-.014,.014,.132,.230,.035,0,32)
# Continuous thick band follows the actual visible route from the board to cam crown.
path=[(.075,zboard(.075)+.004),(.097,.230)]+[(.132+.035*math.cos(a),.230+.035*math.sin(a))for a in[math.pi-j*math.pi/2/10 for j in range(1,11)]]
v=[];fs=[]
for k,(y,z)in enumerate(path):
 a=path[max(0,k-1)];b=path[min(len(path)-1,k+1)];dy=b[0]-a[0];dz=b[1]-a[1];L=math.hypot(dy,dz);ny,nz=-dz/L,dy/L
 for x,h in[(-.009,-.0018),(.009,-.0018),(.009,.0018),(-.009,.0018)]:v.append((x,y+h*ny,z+h*nz))
fs=[(3,2,1,0),tuple((len(path)-1)*4+j for j in range(4))]
for k in range(len(path)-1):
 for j in range(4):q=(j+1)%4;fs.append((4*k+j,4*k+q,4*(k+1)+q,4*(k+1)+j))
mesh('WholeContinuousFixedCamDriveBand',v,fs,2)
for j in range(7):
 t=(j+1)/8;y=.075+(.097-.075)*t;z=zboard(.075)+.004+(.230-zboard(.075)-.004)*t
 axle('WholeBandTransverseRib_%d'%j,-.011,.011,y-.002,z,.0025,1,8)
beam('WholeRaisedBeaterStem',(.027,.132,.224),(.027,.202,.430),.009,1)
cyly('WholeThickBeaterHead',.178,.226,.027,.430,.027,3,24)
beam('WholeOutboardReturnCrank',(.092,.132,.230),(.092,.102,.208),.010,1)
axle('WholeLowerSpringAnchor',.068,.111,.130,.057,.007,1,12)
box('WholeLowerSpringRoot',(.071,.130,.038),(.024,.030,.044),0)
def tube(name,pts,r,mat,n=8,closed=False):
 v=[];L=len(pts)
 for k,P in enumerate(pts):
  prev=pts[(k-1)%L]if closed else pts[max(k-1,0)];nex=pts[(k+1)%L]if closed else pts[min(k+1,L-1)];T=unit(sub(nex,prev));u=unit(cross(T,(0,1,0)if abs(T[1])<.9 else(1,0,0)));w=cross(T,u)
  for i in range(n):v.append(tuple(P[q]+r*(u[q]*math.cos(math.tau*i/n)+w[q]*math.sin(math.tau*i/n))for q in range(3)))
 fs=[]
 for k in range(L if closed else L-1):
  kk=(k+1)%L
  for i in range(n):fs.append((k*n+i,k*n+(i+1)%n,kk*n+(i+1)%n,kk*n+i))
 if not closed:fs +=[tuple(reversed(range(n))),tuple((L-1)*n+i for i in range(n))]
 mesh(name,v,fs,mat)

pts=[(.092,.130,.057),(.092,.118,.075)]+[(.092+.008*math.cos(math.tau*7*j/112),.126+.008*math.sin(math.tau*7*j/112),.077+.114*j/112)for j in range(113)]+[(.092,.116,.201),(.092,.102,.208)]
tube('WholeContinuousReturnSpringAndEndTails',pts,.002,1,8)
box('WholeFrontClampLowerSeat',(0,.194,.027),(.074,.055,.018),1)
for j,x in enumerate([-.032,.032]):box('WholeFrontClampSide_%d'%j,(x,.183,.050),(.012,.032,.038),0)
box('WholeFrontClampUpperBridge',(0,.183,.071),(.074,.032,.014),0)
lathe_z('WholeFixedClampScrew',0,.182,[(0,.051),(.004,.051),(.004,.086),(.013,.086),(.013,.095),(0,.095)],1,16)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeBaseTowersAndClamp_DarkBlue',(.055,.095,.12,1),.64,.3),('WholeBoardShaftSpringAndFasteners_SatinAlloy',(.44,.49,.51,1),.47,.65),('WholeDriveBand_DarkSteel',(.07,.09,.10,1),.57,.45),('WholeBeaterAndGrip_RubberFelt',(.69,.66,.55,1),.91,0)]
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
focus=Vector((0,0,.22))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.72;aim(cam,(4,-5,4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/music/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':'Fixed Chain Band Footboard and Beater Drum Pedal','description':'One newly authored complete empty bass-drum-pedal-style static mechanism exterior. One long ground plate carries a rear heel hinge, full sloping footboard, two front bearing towers and a transverse shaft with a fixed circular cam. A continuous narrow thick drive band rises from the footboard front and wraps over the cam, with separated small transverse raised link-like ribs. An independent long beater stem and thick cylindrical head rise from the shaft; an outboard crank and continuous helical return-spring appearance connect to a lower rooted anchor. A front fixed open clamp-like seat finishes the whole empty unit. The existing complete drum kit explicitly contains no pedal and no component is extracted from it; this is not the large grindstone frame reduced in scale, since it has no stone or long rigid crank rod and uses a compact shaft/beater/band/spring organization. All numeric geometry newly authored. One model zero scenes, four opaque PBR roles, metres Z up and horizontal-envelope-centred ground datum. Fixed empty appearance only: no drum supplied, mounting fit, pedal travel, working chain, elastic spring response, striking, force, sound, tuning, ergonomics, load, manufacture or safety capability. Rigging animation and interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
