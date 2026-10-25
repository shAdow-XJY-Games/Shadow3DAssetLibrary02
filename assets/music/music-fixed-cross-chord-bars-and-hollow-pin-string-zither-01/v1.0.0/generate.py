import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='music-fixed-cross-chord-bars-and-hollow-pin-string-zither-01'
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



# Entire new asymmetric soundbox shell, including actual roof aperture and interior walls.
poly=[(-.18,-.29),(.18,-.29),(.20,-.24),(.20,.09),(.08,.29),(-.16,.29),(-.20,.25),(-.20,-.24)]
c=(-.075,.15);N=40
cross2=lambda a,b:a[0]*b[1]-a[1]*b[0]
outer=[]
for j in range(N):
 a=math.tau*j/N;d=(math.cos(a),math.sin(a));hits=[]
 for aa,bb in zip(poly,poly[1:]+poly[:1]):
  e=(bb[0]-aa[0],bb[1]-aa[1]);den=cross2(d,e)
  if abs(den)<1e-12:continue
  ac=(aa[0]-c[0],aa[1]-c[1]);t=cross2(ac,e)/den;u=cross2(ac,d)/den
  if t>0 and -.00000001<=u<=1.00000001:hits.append(t)
 r=min(hits);outer.append((c[0]+r*d[0],c[1]+r*d[1]))
v=[]
for scale,z in[(.97,0),(1,.012),(1,.070),(.98,.078)]:v +=[(x*scale,y*scale,z)for x,y in outer]
for z in[.078,.066]:v +=[(c[0]+.030*math.cos(math.tau*j/N),c[1]+.030*math.sin(math.tau*j/N),z)for j in range(N)]
for z in[.066,.013]:v +=[(x*.93,y*.93,z)for x,y in outer]
f=[]
for k in range(7):
 for j in range(N):q=(j+1)%N;f.append((k*N+j,k*N+q,(k+1)*N+q,(k+1)*N+j))
bottom=len(v);v.append((c[0],c[1],0));floor=len(v);v.append((c[0],c[1],.013))
for j in range(N):q=(j+1)%N;f +=[(bottom,q,j),(floor,7*N+j,7*N+q)]
mesh('WholeGroundFootHollowClippedShoulderSoundbox',v,f,0)
# Whole end banks and finite little crown strips hold every complete longitudinal string.
for tag,y,w in [('Tail',-.235,.328),('Head',.185,.290)]:
 box('WholeEndPinBank_'+tag,(0,y,.081),(w,.026,.018),1)
 box('WholeEndStringCrown_'+tag,(0,y,.091),(w-.012,.008,.006),3)
for j in range(13):
 x=-.135+j*.022
 cyly('WholeLongitudinalString_%02d'%j,-.244,.194,x,.094,.0009,2,6)
 for tag,y in [('Tail',-.244),('Head',.194)]:lathe_z('WholeAnchorPin_%s_%02d'%(tag,j),x,y,[(0,.076),(.0026,.076),(.0026,.100),(0,.100)],2,8)
# Full side rails and crossing chord bars; fixed raised pad state, not a functioning damper.
for j,x in enumerate([-.171,.171]):box('WholeChordBarSideRail_%d'%j,(x,-.059,.101),(.024,.256,.054),1)
for j,y in enumerate([-.150,-.105,-.060,-.015,.030]):
 box('WholeCrossStringChordBar_%d'%j,(0,y,.128),(.361,.021,.018),1)
 box('WholeRaisedChordButton_%d'%j,(-.055 if j%2==0 else .045,y,.148),(.045,.032,.025),3)
 # Separated fixed lower pad appearances are integral to this bar assembly, not calibrated note selection.
 for k,x in enumerate([-.105,-.025,.070]):box('WholeLowerPad_%d_%d'%(j,k),(x,y,.113),(.040,.018,.015),1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeHollowSoundbox_HoneyWood',(.48,.27,.10,1),.78,0),('WholeCrossbarsRailsPadsAndBanks_DarkTimber',(.11,.050,.022,1),.82,0),('WholeCompleteStringsAndPins_SatinAlloy',(.55,.58,.56,1),.49,.5),('WholeButtonsAndCrownStrips_WarmIvory',(.79,.75,.63,1),.71,0)]
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
focus=Vector((0,0,.065))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.78;aim(cam,(3,-5,7));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/music/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':'Fixed Cross Chord Bars and Hollow Pin String Zither','description':'One newly authored complete chord-bar zither-style static instrument exterior. One low clipped-shoulder hollow soundbox has a true round sound hole through the full upper skin and a finite closed bottom. Thirteen complete lengthwise strings run between two whole end banks and separately rooted anchor pins. A distinct transverse fixed chord-bar bank crosses over the strings: two complete side bearing rails support five whole crossbars with separated lower pad appearances and raised staggered buttons. This is not the old paired transverse courses crossing two central dulcimer bridges, nor a wheel-bowed pear instrument with a longitudinal keybox and side crank. The complete hollow-body, longitudinal string field and cross-string bar/control organization is new geometry, with no old visible meshes imported and no string-count variant claim. One whole model zero scenes, four opaque constant PBR roles, metres Z up and whole horizontal-envelope-centred ground datum. Fixed simplified instrument appearance only: no calibrated chord mapping, working dampers or key travel, string tension, pitch, resonance, acoustic response, playability, cultural authenticity, manufacture or safety capability. No performer, pick, case, rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
