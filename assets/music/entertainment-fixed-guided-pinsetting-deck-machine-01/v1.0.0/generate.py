import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='entertainment-fixed-guided-pinsetting-deck-machine-01'
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



# Entire fixed pinsetting-machine appearance, no loose pin or lane imported.
for side,x in [('Left',-.74),('Right',.74)]:
 box(side+'GroundFootRunner',(x,.10,.065),(.16,1.70,.13),0)
 box(side+'WholeLongCarriageRail',(x,0,.98),(.11,1.48,.12),0)
 for end,y in [('Front',-.59),('Rear',.69)]:
  box(side+end+'WholeFrameColumn',(x,y,.86),(.09,.10,1.60),0)
  gx=x-(.10 if x>0 else -.10)
  lathe_z(side+end+'WholeGuideShaft',gx,y,[(0,.16),(.018,.16),(.018,1.72),(0,1.72)],1,16)
  lathe_z(side+end+'WholeBoredCarriageSleeve',gx,y,[(.019,.87),(.036,.87),(.036,1.10),(.019,1.10)],1,20)
  for iz in [.20,1.63]:beam(side+end+'WholeGuideEndRoot_'+str(iz),(x,y,iz),(gx,y,iz),.055,0)
  beam(side+end+'WholeCarriageSleeveRoot',(x,y,.99),(gx,y,.99),.06,0)
 box(side+'WholeTopRail',(x,.05,1.68),(.13,1.50,.12),0)
 beam(side+'RearDiagonalBrace',(x,.83,.12),(x,.69,.77),.055,0)
for end,y in [('Front',-.59),('Rear',.69)]:box(end+'WholeUpperCrossbeam',(0,y,1.72),(1.58,.14,.12),0)
box('WholeRearLowerTie',(0,.72,.27),(1.48,.09,.10),0)
# Four connected row plates together form the complete triangular ten-aperture setting deck.
# Each plate is a whole closed shared-boundary mesh, not separate rings on solid backing.
def rowplate(name,count,y,z):
 vs=[];fs=[];lookup={}
 def V(p):
  p=tuple(round(v,10)for v in p)
  if p not in lookup:lookup[p]=len(vs);vs.append(p)
  return lookup[p]
 N=24;angles=sorted(set(round(a,12)for a in [math.tau*i/N for i in range(N)]+[math.pi/4,3*math.pi/4,5*math.pi/4,7*math.pi/4]));N=len(angles)
 for c in range(count):
  x=(c-(count-1)/2)*.32;loops=[]
  for zz in[z-.035,z+.035]:
   loops.append([[V((x+math.cos(a)*r(a),y+math.sin(a)*r(a),zz))for a in angles]for r in[lambda a:.16/max(abs(math.cos(a)),abs(math.sin(a))),lambda a:.105]])
  for i in range(N):
   j=(i+1)%N;lo,hi=loops
   fs.extend([(lo[0][j],lo[0][i],lo[1][i],lo[1][j]),(hi[0][i],hi[0][j],hi[1][j],hi[1][i]),(lo[1][i],hi[1][i],hi[1][j],lo[1][j])])
 edge={}
 for f in fs:
  for a,b in zip(f,f[1:]+f[:1]):edge.setdefault(tuple(sorted((a,b))),[]).append((a,b))
 for e in list(edge.values()):
  if len(e)==1:
   a,b=e[0]
   if abs(vs[a][2]-(z+.035))<1e-8 and abs(vs[b][2]-(z+.035))<1e-8:
    aa=V((vs[a][0],vs[a][1],z-.035));bb=V((vs[b][0],vs[b][1],z-.035));fs.append((b,a,aa,bb))
 mesh(name,vs,fs,1)
for row in range(4):
 y=-.46+row*.32;rowplate('WholePerforatedSettingRow_%d'%(row+1),row+1,y,.98)
 box('WholeSettingRowSupport_%d'%row,(0,y+.145,.93),(1.48,.035,.07),0)
# Lower sweeping-style bar and opposed swing links are connected to side journals.
for side,x in [('Left',-.68),('Right',.68)]:
 axle(side+'WholeSweepJournal',x-.08,x+.08,-.57,.71,.035,1,20)
 beam(side+'WholeSweepArm',(x,-.57,.71),(x,-.76,.29),.045,0)
box('WholeLowSweepBar',(0,-.76,.28),(1.43,.065,.12),2)
# Upper fixed lift appearance: paired side chains represented as continuous thick links.
for side,x in [('Left',-.61),('Right',.61)]:
 beam(side+'WholeFixedDeckLiftLink',(x,.05,1.68),(x,.05,1.015),.025,2)
 beam(side+'WholeDeckLiftCrossRoot',(x,.05,.995),(x,.18,.995),.035,0)
box('WholeRearDriveHousing',(0,.75,1.39),(.54,.22,.36),0)
axle('WholeTransverseDriveShaft',-.74,.74,.75,1.43,.025,1,20)
for x in[-.63,.63]:ringx('WholeFixedDriveDisc_'+str(x),x-.022,x+.022,.75,1.43,.024,.13,1,24)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeChassisAndLiftRoots_MutedBlue',(.12,.28,.34,1),.66,.10),('WholeSettingDeckGuidesAndDiscs_DullAlloy',(.52,.56,.54,1),.52,.35),('WholeSweepFaceAndFixedLiftLinks_Dark',(.055,.065,.073,1),.75,.08)]
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
focus=Vector((0,0,.88))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.15;aim(cam,(3.6,-5,3.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/music/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'entertainment','style':'S01-clean-geometric','title':'Fixed Guided Pinsetting Deck Machine','description':'One newly authored complete fixed pinsetting-machine visual display. A grounded braced double-side chassis has four whole guide shafts and bored setting-deck carriage sleeves. Four connected full perforated row plates have one, two, three and four real through-apertures in a triangular ten-position layout, supported on full crossrails. A distinct low sweep bar belongs to two side journal arms. Upper fixed lift links, a rear housing and transverse shaft with end discs complete the machinery exterior. No old bowling pins, lane or loose balls imported or counted; not a scaled desk plunger or inclined carnival target table with extra holes. Three opaque untextured constant PBR roles; metres, Z up and whole horizontal ground centering. One whole machine prop and zero scenes. Static empty illustrative machinery appearance only: no pin compatibility, feeding or gripping internals, ball return, regulation geometry, lifting or sweep motion, complete drive transmission, operating instructions, power, load, fabrication or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
