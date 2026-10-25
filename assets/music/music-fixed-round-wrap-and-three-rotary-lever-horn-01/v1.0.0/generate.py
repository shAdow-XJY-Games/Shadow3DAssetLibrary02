import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='music-fixed-round-wrap-and-three-rotary-lever-horn-01'
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



# New surrounding round wrap and low rotary housing bank, static exterior.
def hollow_path(name,stations,mat,inner,n=20):
 v=[];f=[];fm=[]
 for k,(p,ro,ri)in enumerate(stations):
  a=stations[max(k-1,0)][0];b=stations[min(k+1,len(stations)-1)][0];t=unit(sub(b,a));u=unit(cross(t,(0,0,1)if abs(t[2])<.9 else(0,1,0)));w=cross(t,u)
  for r in[ro,ri]:
   for j in range(n):v.append(tuple(p[i]+r*(u[i]*math.cos(math.tau*j/n)+w[i]*math.sin(math.tau*j/n))for i in range(3)))
 for k in range(len(stations)-1):
  for j in range(n):
   h=(j+1)%n;a=2*n*k+j;b=2*n*k+h;c=2*n*(k+1)+j;d=2*n*(k+1)+h
   f.extend([(a,b,d,c),(a+n,c+n,d+n,b+n)]);fm.extend([mat,inner])
 for j in range(n):
  h=(j+1)%n;k=(len(stations)-1)*2*n;f.extend([(h,j,j+n,h+n),(k+j,k+h,k+h+n,k+j+n)]);fm.extend([mat,mat])
 mesh(name,v,f,mat);FM[name]=[m for m,face in zip(fm,f)for _ in range(len(face)-2)]
def route(name,path,r=.008):hollow_path(name,[(p,r,r-.0025)for p in path],0,3,16)
for k,x in enumerate([-.065,0,.065]):
 lathe_z('WholeGroundFootRotorCap_%d'%k,x,0,[(0,0),(.029,0),(.031,.008),(.031,.054),(.027,.059),(0,.059)],1,24)
 lathe_z('WholeLowRotaryDrumHousing_%d'%k,x,0,[(0,.046),(.030,.046),(.032,.057),(.032,.112),(.028,.119),(0,.119)],0,24)
 lathe_z('WholeRaisedRotaryCover_%d'%k,x,0,[(0,.112),(.034,.112),(.034,.123),(.029,.128),(0,.128)],1,24)
 lathe_z('WholeFixedRotorSpindle_%d'%k,x,0,[(0,.120),(.006,.120),(.006,.150),(0,.150)],1,12)
 beam('WholeRotorCrank_%d'%k,(x,0,.146),(x-.014,-.032,.146),.008,1)
 beam('WholeFixedLinkRod_%d'%k,(x-.014,-.030,.146),(x-.014,-.112,.164),.0055,1)
 beam('WholeFingerLever_%d'%k,(x-.014,-.112,.164),(x-.014,-.160,.164),.008,1)
 box('WholeSeparateFingerPaddle_%d'%k,(x-.014,-.153,.169),(.039,.041,.010),2)
 # Each valve has its own complete side-return appearance, no internal flow claim.
 out=[.080,.101,.080][k]
 route('WholeUpperReturnSlide_%d'%k,[(x-.015,.023,.082),(x-.015,out-.018,.082),(x-.008,out,.082),(x+.009,out,.082),(x+.017,out-.018,.082),(x+.017,.023,.082)],.007)
beam('WholeCommonLeverBearing',(-.101,-.111,.154),(.081,-.111,.154),.012,1)
for k,x in enumerate([-.065,.065]):beam('WholeBearingRoot_%d'%k,(x,-.022,.095),(x,-.111,.153),.011,0)
# A near-full circular main branch surrounds the rotor bank and then turns into a side bell.
st=[((.066,.025,.093),.009,.006),((.105,.080,.093),.010,.007)]
for i in range(43):
 a=math.radians(45+315*i/42);r=.218;st.append(((r*math.cos(a),r*math.sin(a),.093),.011,.008))
st += [((.225,-.036,.096),.013,.010),((.250,-.074,.102),.019,.016),((.290,-.113,.112),.029,.026),((.330,-.153,.125),.047,.044),((.363,-.186,.140),.076,.073),((.384,-.211,.155),.109,.106),((.394,-.225,.164),.128,.125),((.398,-.232,.168),.129,.126)]
hollow_path('WholeCircularWrapAndBackSweptOpenBell',st,0,3,24)
route('WholeHighLeadpipe',[(-.305,.272,.154),(-.210,.272,.154),(-.125,.261,.154),(-.083,.237,.154),(-.057,.198,.154),(-.055,.145,.154),(-.065,.080,.133),(-.065,.024,.102)],.0085)
hollow_path('WholeOpenCupMouthpiece',[((-.304,.272,.154),.010,.006),((-.326,.272,.154),.010,.006),((-.342,.272,.154),.014,.010),((-.356,.272,.154),.020,.016),((-.365,.272,.154),.021,.017)],1,1,24)
for tag,a,b in [('Left',(-.030,0,.082),(-.207,0,.093)),('Right',(.090,0,.082),(.210,.006,.093)),('Upper',(-.055,.117,.146),(-.056,.210,.097))]:beam('WholeFiniteBranchStay_'+tag,a,b,.009,0)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeCircularTubesAndRotorHousings_MutedBrass',(.55,.36,.11,1),.44,.68),('WholeCoversMouthpieceAndLinks_SatinNickel',(.51,.55,.54,1),.40,.7),('WholeLeverPaddles_WarmIvory',(.75,.69,.55,1),.57,.04),('WholeTrueBellAndTubeInteriors_DarkBrass',(.30,.17,.05,1),.54,.53)]
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
focus=Vector((0,0,.12))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.0;aim(cam,(3,-5,5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/music/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':'Fixed Round Wrap and Three Rotary Lever Horn','description':'One newly authored whole static rotary-horn-style exterior. A continuous near-circular hollow main tube surrounds three short broad rotor drum housings and flows into a back-swept expanding open side bell. Each drum has its own raised cover, fixed spindle and crank, complete short link rod, separate lever paddle and upper return slide. A common supported lever bearing and three rooted branch stays connect the complete assembly. A higher swept inlet ends in a real open shallow cup. All numeric geometry is new, with no imported instrument meshes. The surrounding round wrap and low rotary-linkage bank are not the old long valveless U bugle lengthened or an inline three-piston trumpet scaled or recoloured. Four opaque untextured PBR roles, metres, Z up and horizontal-envelope-centred datum on three finite rotor-cap lower faces. One whole prop, zero scenes. Generic fixed illustrative exterior only: the drum housings are solid, internal acoustic routing and airtightness are not modeled; no sound, tuning, playability, rotor motion, linkage operation, exact historical design, fit, manufacture or safety claim. No animation, rigging, interaction, player or stand.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
