import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='culture-static-seated-draped-reader-and-open-book-statue-01'
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



box('WholeGroundFootPlinth',(0,0,.06),(.94,.90,.12),2)
box('WholeIntegralLowSeat',(0,.20,.425),(.62,.47,.63),2)
# New continuous seated drapery, torso and head silhouette; no old standing figure transformed.
rows=[(0,-.15,.23,.25,.13,.11,0),(0,-.14,.35,.27,.17,.13,0),(0,-.18,.54,.29,.20,.12,0),(0,-.12,.68,.30,.25,.09,0),(0,.02,.78,.28,.22,.05,0),(0,.08,.88,.23,.18,.04,0),(0,.07,1.00,.18,.14,.025,0),(0,.04,1.20,.23,.15,.015,0),(0,.01,1.32,.255,.16,0,0),(0,-.015,1.40,.12,.095,0,0),(0,-.025,1.46,.075,.07,0,1),(0,-.045,1.50,.105,.10,0,1),(0,-.065,1.62,.135,.115,0,1),(0,-.045,1.72,.13,.11,0,1),(0,-.02,1.80,.08,.07,0,1),(0,-.018,1.82,.025,.025,0,1)]
n=32;v=[];f=[];fm=[]
for x,y,z,rx,ry,fold,mat in rows:
 for j in range(n):
  a=math.tau*j/n;scale=1-fold*(.5+.5*math.cos(8*a));v.append((x+rx*scale*math.cos(a),y+ry*scale*math.sin(a),z))
for k in range(len(rows)-1):
 for j in range(n):
  q=(j+1)%n;f.append((k*n+j,k*n+q,(k+1)*n+q,(k+1)*n+j));fm.extend([rows[k][6]]*2)
for k in[0,len(rows)-1]:
 c=len(v);v.append(rows[k][:3])
 for j in range(n):f.append((c,k*n+(j+1)%n,k*n+j)if k==0 else(c,k*n+j,k*n+(j+1)%n));fm.append(rows[k][6])
mesh('WholeSeatedDraperyTorsoNeckAndHead',v,f,0);FM['WholeSeatedDraperyTorsoNeckAndHead']=fm
# Closed tapered bent sleeves and palms, rooted together rather than detached rods.
def organic_path(name,points,radii,mat,n=12):
 v=[];f=[]
 for k,p in enumerate(points):
  tangent=unit(sub(points[min(k+1,len(points)-1)],points[max(k-1,0)]));seed=(0,1,0)if abs(tangent[1])<.88 else(1,0,0);u=unit(cross(tangent,seed));w=cross(tangent,u)
  for j in range(n):v.append(tuple(p[i]+radii[k]*(u[i]*math.cos(math.tau*j/n)+w[i]*math.sin(math.tau*j/n))for i in range(3)))
 for k in range(len(points)-1):
  for j in range(n):q=(j+1)%n;f.append((k*n+j,k*n+q,(k+1)*n+q,(k+1)*n+j))
 f.extend([tuple(reversed(range(n))),tuple((len(points)-1)*n+j for j in range(n))]);mesh(name,v,f,mat)
for sg in[-1,1]:
 organic_path('WholeBentSleevedArm_'+str(sg),[(sg*.205,.015,1.30),(sg*.292,-.018,1.21),(sg*.325,-.08,1.11),(sg*.275,-.15,1.065),(sg*.235,-.21,1.035)],[.091,.09,.077,.060,.047],0)
 organic_path('WholeBookRestingPalm_'+str(sg),[(sg*.242,-.198,1.040),(sg*.225,-.235,1.024),(sg*.205,-.252,1.015)],[.047,.047,.032],1)
 # Whole projecting feet are low ellipsoidal lofts with finite seated bottoms.
 rr=[(.115,.063,.12),(.17,.080,.15),(.225,.065,.115),(.28,.05,.07)];vv=[];ff=[]
 for z,rx,ry in rr:
  for j in range(16):a=math.tau*j/16;vv.append((sg*.13+rx*math.cos(a),-.235+ry*math.sin(a),z))
 for k in range(3):
  for j in range(16):q=(j+1)%16;ff.append((k*16+j,k*16+q,(k+1)*16+q,(k+1)*16+j))
 ff.extend([tuple(reversed(range(16))),tuple(48+j for j in range(16))]);mesh('WholeForwardFoot_'+str(sg),vv,ff,1)
 # Same-stone short relief eyelids, intentionally no painted pupil disks.
 box('WholeClosedEyelidRelief_'+str(sg),(sg*.062,-.151,1.677),(.049,.027,.012),1)
# Full blunt facial nose rooted through the head front, not a texture.
mesh('WholeSculptedNose',[(-.021,-.151,1.60),(.021,-.151,1.60),(.014,-.222,1.605),(-.014,-.222,1.605),(-.018,-.151,1.675),(.018,-.151,1.675),(.011,-.210,1.632),(-.011,-.210,1.632)],[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],1)
# Thick blank book with an actual central valley; no text or loose sheets.
for sg in[-1,1]:
 p=[(0,.910),(sg*.29,.990),(sg*.29,1.025),(0,.945)]
 if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(p,p[1:]+p[:1]))<0:p.reverse()
 vv=[(x,y,z)for y in[-.36,-.08]for x,z in p];ff=[]
 for a,b,c in triangulate(p):ff.extend([(c,b,a),(a+4,b+4,c+4)])
 for i in range(4):j=(i+1)%4;ff.append((i,j,j+4,i+4))
 mesh('WholeBlankBookPageMass_'+str(sg),vv,ff,3)
cyly('WholeRoundedBookSpine',-.37,-.07,0,.925,.026,0,20)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeRobeAndSpine_CoolStone',(.46,.50,.48,1),.92,0),('WholeFaceHandsAndFeet_WarmStone',(.64,.60,.52,1),.91,0),('WholeSeatAndPlinth_DarkStone',(.28,.32,.32,1),.94,0),('WholeBlankBookPages_PaleStone',(.73,.69,.60,1),.93,0)]
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
focus=Vector((0,0,.91))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.45;aim(cam,(3,-7,3.0));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/culture/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'culture','style':'S01-clean-geometric','title':'Static Seated Draped Reader and Open Book Statue','description':'One wholly newly authored complete low-poly cultural sculpture of an anonymous adult-like seated reader. A full flat plinth carries a low solid seat and both forward feet. The continuous draped body rises from a folded lower hem over broad forward knees into a set-back seated hip, narrower waist, shoulders, short inclined neck and simplified head. Drapery folds are part of the actual closed surface rather than applied stripes. Two entire bent sleeve arms root at the shoulders, turn forward at the elbows and end in small complete palms seated on the two sides of one thick open book. Two sloping blank page masses and a full rounded centre spine make the book opening actual geometry. A blunt sculpted nose and small same-stone closed eyelid ridges suggest a downward-looking calm face, not a likeness of a real person. No original caryatid, wooden toy or book mesh is imported: this is a newly drawn full seated figure, not a removed capital on an old standing body or a mechanical puppet recoloured as stone. Four opaque constant untextured stone-toned PBR roles, metres Z up, full horizontal bounds centre, one complete sculpture zero scenes; seat, book and plinth are integral parts of this one composition, not separately counted assets. Generic contemporary game-art sculpture, not a named historical artifact, specific person, anatomical study, religious identity, readable text, tactile accessibility or public installation design. No pose change, binding, animation, interaction, structural or load/installation safety capability made or verified.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
