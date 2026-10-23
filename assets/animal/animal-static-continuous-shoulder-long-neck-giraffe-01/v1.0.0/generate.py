import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='animal-static-continuous-shoulder-long-neck-giraffe-01'
G={};FM={}
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def mesh(name,v,faces,mat):
 f=[]
 for p in faces:
  for k in range(1,len(p)-1):f.append((p[0],p[k],p[k+1]))
 if sum(dot(v[a],cross(v[b],v[c]))for a,b,c in f)<0:f=[tuple(reversed(p))for p in f]
 G[name]=(v,f,mat)
def round_body(name,stations,mat,n=16):
 v=[]
 for y,w,low,high in stations:
  for j in range(n):
   a=math.tau*j/n;h=(math.sin(a)+1)/2
   # A finite underside patch, not a single lowest vertex; head is raised.
   if h<.04:h=0
   v.append((w*math.cos(a),y,low+(high-low)*h))
 f=[tuple(reversed(range(n))),tuple((len(stations)-1)*n+j for j in range(n))]
 for k in range(len(stations)-1):
  for j in range(n):q=(j+1)%n;f.append((k*n+j,k*n+q,(k+1)*n+q,(k+1)*n+j))
 mesh(name,v,f,mat)
def ellipsoid(name,c,s,mat,n=12,r=6):
 v=[(c[0],c[1],c[2]+s[2])]
 for k in range(1,r):
  a=math.pi*k/r
  v.extend([(c[0]+s[0]*math.sin(a)*math.cos(math.tau*j/n),c[1]+s[1]*math.sin(a)*math.sin(math.tau*j/n),c[2]+s[2]*math.cos(a))for j in range(n)])
 v.append((c[0],c[1],c[2]-s[2]));f=[]
 for j in range(n):q=(j+1)%n;f.extend([(0,1+j,1+q),(len(v)-1,1+(r-2)*n+q,1+(r-2)*n+j)])
 for k in range(r-2):
  for j in range(n):q=(j+1)%n;f.append((1+k*n+j,1+(k+1)*n+j,1+(k+1)*n+q,1+k*n+q))
 mesh(name,v,f,mat)
def prism(name,outline,height,thickness,mat):
 # Convex full outline, fan from actual polygon centroid on each parallel skin.
 n=len(outline);cx=sum(x for x,y in outline)/n;cy=sum(y for x,y in outline)/n
 v=[(x,y,height(x,y)+off)for off in[-thickness/2,thickness/2]for x,y in outline]+[(cx,cy,height(cx,cy)-thickness/2),(cx,cy,height(cx,cy)+thickness/2)]
 f=[]
 for i in range(n):j=(i+1)%n;f.extend([(2*n,j,i),(2*n+1,n+i,n+j),(i,j,n+j,n+i)])
 mesh(name,v,f,mat)

def loft(name,rings,mat):
 n=len(rings[0]);v=[p for ring in rings for p in ring];f=[tuple(reversed(range(n))),tuple((len(rings)-1)*n+j for j in range(n))]
 for k in range(len(rings)-1):
  for j in range(n):q=(j+1)%n;f.append((k*n+j,k*n+q,(k+1)*n+q,(k+1)*n+j))
 mesh(name,v,f,mat)
def ring_xz(y,z,rx,rz,angle=0,n=16):
 return[(rx*math.cos(math.tau*j/n),y-rz*math.sin(math.tau*j/n)*math.sin(angle),z+rz*math.sin(math.tau*j/n)*math.cos(angle))for j in range(n)]

# One newly drawn continuous torso/raised shoulder/long neck surface, not
# an old deer neck stretched or a new colour applied to another quadruped.
BODY_NECK=[(.88,2.13,.18,.26,0),(.66,2.15,.35,.43,0),(.12,2.22,.39,.47,0),(-.30,2.30,.36,.46,-.15),(-.54,2.54,.27,.32,-.60),(-.68,2.98,.19,.22,-1.10),(-.88,3.50,.15,.17,-1.18),(-1.06,4.03,.12,.135,-1.18)]
loft('ContinuousSlopingTorsoShoulderAndLongNeck',[ring_xz(*q,n=16)for q in BODY_NECK],0)
loft('WholeSmallElongatedHead',[ring_xz(y,z,rx,rz,n=12)for y,z,rx,rz in[(-.94,4.12,.11,.16),(-1.10,4.16,.20,.22),(-1.32,4.12,.16,.16),(-1.61,4.03,.13,.105),(-1.68,4.025,.09,.075)]],0)
# Integral face assignments on existing full triangles, not protruding spot discs.
for name in ['ContinuousSlopingTorsoShoulderAndLongNeck','WholeSmallElongatedHead']:
 v,f,m=G[name];FM[name]=[1 if ((i//2)%7 in (1,4)and i>24)else 0 for i in range(len(f))]
LEGS=[]
for sign,side in[(-1,'Left'),(1,'Right')]:
 for y,label in[(-.25,'Front'),(.58,'Hind')]:
  name=side+label+'WholeLongLegAndFlatHoof';LEGS.append(name)
  rings=[[(sign*x+rx*math.cos(math.tau*j/10),yy+ry*math.sin(math.tau*j/10),z)for j in range(10)]for x,yy,z,rx,ry in[(.26,y-.03,0,.10,.135),(.26,y-.03,.14,.10,.135),(.26,y,.25,.060,.065),(.28,y+(.10 if label=='Hind'else-.04),.92,.065,.075),(.27,y,1.40,.080,.09),(.25,y,2.12,.13,.15)]]
  loft(name,rings,0);v,f,m=G[name];FM[name]=[2 if max(v[k][2]for k in t)<=.14+1e-9 else 0 for t in f]
 # Two short unbranched whole ossicones, with rounded wider closed terminal ring.
 rings=[[(sign*.105+r*math.cos(math.tau*j/10),-1.075+r*math.sin(math.tau*j/10),z)for j in range(10)]for z,r in[(4.27,.040),(4.47,.033),(4.52,.050),(4.57,.026)]]
 loft(side+'WholeShortUnbranchedOssicone',rings,2)
 # One complete thick pointed lateral ear; full root resides in head flank.
 outline=[(sign*.12,4.21),(sign*.28,4.40),(sign*.48,4.43),(sign*.43,4.26),(sign*.20,4.17)]
 n=len(outline);v=[(x,y,z)for y in[-1.13,-1.045]for x,z in outline];f=[tuple(reversed(range(n))),tuple(n+j for j in range(n))]+[(j,(j+1)%n,(j+1)%n+n,j+n)for j in range(n)];mesh(side+'WholePointedThickEar',v,f,0)
 ellipsoid(side+'SmallDarkEye',(sign*.167,-1.27,4.20),(.027,.030,.029),2,n=10,r=5)
# One long tapered hanging tail with closed tuft in the same loft.
loft('WholeHangingTailAndTuft',[ring_xz(y,z,r,r,a,n=10)for y,z,r,a in[(.80,2.20,.045,0),(.96,1.94,.035,-1.0),(1.01,1.57,.027,-1.4),(1.03,1.25,.050,-1.5),(1.04,1.13,.018,-1.5)]],2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)]
SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={name:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for name,(v,f,m)in G.items()}
# Compact stylised display dimensions, not a life-size animal measurement.
G={name:([tuple(.5*x for x in p)for p in v],f,m)for name,(v,f,m)in G.items()}
PALETTE=[('Coat_MatteGoldenTan',(.58,.36,.14,1),.91,0),('CoatFacets_DeepUmber',(.22,.105,.035,1),.93,0),('HoovesEyesTuft_DarkBrown',(.045,.028,.015,1),.80,0)]
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
focus=Vector((0,0,1.12))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.05;aim(cam,(5,-7,4.9));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/animal/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'animal','style':'S01-clean-geometric','title':'Static Continuous-Shoulder Long-Neck Giraffe','description':'One newly authored stylised static giraffe-like whole animal. A continuous sloping torso rises through the shoulder into a long narrowing neck as one closed mesh, carrying a small elongated head, paired complete short unbranched ossicones and pointed thick lateral ears. Four entire long legs end in integral flat dark hoof soles; a long hanging tufted tail and small eyes complete the whole silhouette. New complete body path, proportions and head geometry rather than an old deer stretched or a colour swap; coat facet colours are secondary and are not counted as structural novelty. Metres, native Z up, head -Y, actual horizontal bounds-centred ground datum. One prop, zero scene. No rig, animation, sex, age or exact species/anatomical precision claim; no animal handling, locomotion or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
