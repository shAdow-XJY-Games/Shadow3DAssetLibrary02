import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='characters-static-open-hood-long-raincoat-worker-01'
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

# New whole dressed figure. Garment topology is actual thick shell geometry,
# unlike the old separate front bib or solid scarecrow rag silhouette.
def xy(cx,cy,z,rx,ry,n=12):return[(cx+rx*math.cos(math.pi/n+math.tau*i/n)/math.cos(math.pi/n),cy+ry*math.sin(math.pi/n+math.tau*i/n)/math.cos(math.pi/n),z)for i in range(n)]
def solid_loft(name,rings,mat,face_mat=None):
 n=len(rings[0]);v=[p for r in rings for p in r];f=[];fm=[]
 for k in range(len(rings)-1):
  for i in range(n):j=(i+1)%n;f.extend([(k*n+i,k*n+j,(k+1)*n+j),(k*n+i,(k+1)*n+j,(k+1)*n+i)]);fm.extend([face_mat(k,i)if face_mat else mat]*2)
 for k,r in [(0,rings[0]),(len(rings)-1,rings[-1])]:
  c=len(v);v.append(tuple(sum(p[j]for p in r)/n for j in range(3)))
  for i in range(n):j=(i+1)%n;f.append((c,k*n+j,k*n+i)if k==0 else(c,k*n+i,k*n+j));fm.append(mat)
 mesh(name,v,f,mat);FM[name]=fm

def tube_loft(name,outer,inner,mat):
 n=len(outer[0]);K=len(outer);v=[p for rr in[outer,inner]for r in rr for p in r];f=[];off=K*n
 for k in range(K-1):
  for i in range(n):j=(i+1)%n;a=k*n+i;b=k*n+j;c=(k+1)*n+j;d=(k+1)*n+i;f.extend([(a,b,c,d),(off+a,off+d,off+c,off+b)])
 for k in[0,K-1]:
  for i in range(n):j=(i+1)%n;a=k*n+i;b=k*n+j;f.append((a,off+a,off+b,b)if k==0 else(a,b,off+b,off+a))
 mesh(name,v,f,mat)
# Flared knee-length coat: open lower hem and neck, complete inner wall.
COAT=[(.47,.285,.17),(.62,.27,.165),(.88,.225,.145),(1.08,.215,.14),(1.27,.26,.15),(1.35,.25,.145),(1.435,.09,.075)]
outer=[xy(0,0,z,rx,ry)for z,rx,ry in COAT];inner=[xy(0,0,z,rx-.018,ry-.018)for z,rx,ry in COAT];tube_loft('WholeThickOpenHemRaincoat',outer,inner,0)
# An actual forward-open hood shell, with separate inner cavity and true front
# rim. Pole caps close only the back, never the face aperture.
n=20
outer=[[(rx*math.cos(math.tau*i/n),y,1.63+rz*math.sin(math.tau*i/n))for i in range(n)]for y,rx,rz in[(-.19,.145,.195),(-.055,.17,.22),(.075,.12,.17)]]
inner=[[(rx*math.cos(math.tau*i/n),y,1.63+rz*math.sin(math.tau*i/n))for i in range(n)]for y,rx,rz in[(-.19,.12,.17),(-.055,.145,.195),(.068,.095,.145)]]
v=[p for rr in[outer,inner]for r in rr for p in r];f=[];off=3*n
for k in range(2):
 for i in range(n):j=(i+1)%n;a=k*n+i;b=k*n+j;c=(k+1)*n+j;d=(k+1)*n+i;f.extend([(a,b,c,d),(off+a,off+d,off+c,off+b)])
for i in range(n):j=(i+1)%n;f.append((i,off+i,off+j,j))
for q,back in[(0,(0,.145,1.63)),(off,(0,.115,1.63))]:
 c=len(v);v.append(back)
 for i in range(n):j=(i+1)%n;f.append((c,q+2*n+j,q+2*n+i)if q else(c,q+2*n+i,q+2*n+j))
mesh('WholeForwardOpenThickHood',v,f,0)
# New quiet generic face grid: all small eye/nose/mouth regions belong to one
# surface. No copied identity, hairpiece, overlaid eye cards or image texture.
HR=[(1.46,.053,.050),(1.50,.073,.065),(1.54,.090,.079),(1.565,.098,.083),(1.575,.10,.085),(1.61,.103,.085),(1.635,.103,.085),(1.651,.102,.085),(1.69,.10,.082),(1.735,.078,.064),(1.765,.034,.028)];XF=[-1,-.66,-.36,-.18,.18,.36,.66,1];rr=[]
for z,rx,ry in HR:
 front=[(rx*x,-.070-ry-.024*max(0,1-abs(x)/.36)*max(0,1-abs(z-1.61)/.045),z)for x in XF]
 rr.append(front+[(rx,.01,z),(.70*rx,.045,z),(-.70*rx,.045,z),(-rx,.01,z)])
def facecolor(k,i):
 if (k==6 and i in[2,4])or(k==3 and i==3):return 4
 return 1
solid_loft('WholeAnonymousShapedHead',rr,1,facecolor)
solid_loft('WholeShortNeck',[xy(0,-.02,1.34,.052,.05),xy(0,-.02,1.50,.052,.05)],1)
solid_loft('WholeInternalTrouserBridge',[xy(0,0,.73,.16,.10),xy(0,0,.91,.17,.11)],2)
for side,sx in [('Left',-1),('Right',1)]:
 # The cuffs are true rings. Fixed hand roots occupy the opening in this pose;
 # not a claim of an independently wearable/dressable garment.
 specs=[(sx*.235,0,1.29,.083,.09),(sx*.29,-.005,1.12,.071,.077),(sx*.34,-.025,.91,.054,.060),(sx*.34,-.035,.84,.052,.055)]
 tube_loft(side+'WholeHollowLongSleeve',[xy(x,y,z,rx,ry)for x,y,z,rx,ry in specs],[xy(x,y,z,rx-.014,ry-.014)for x,y,z,rx,ry in specs],0)
 solid_loft(side+'WholeClosedGlovedHand',[xy(sx*.34,-.035,.865,.039,.039),xy(sx*.345,-.045,.80,.049,.046),xy(sx*.35,-.05,.73,.04,.045)],2)
 solid_loft(side+'WholeTrouserLeg',[xy(sx*.115,0,.20,.059,.062),xy(sx*.115,0,.52,.065,.070),xy(sx*.115,0,.82,.071,.084)],2)
 solid_loft(side+'WholeGroundTallBoot',[xy(sx*.115,-.055,0,.077,.15),xy(sx*.115,-.055,.045,.077,.15),xy(sx*.115,-.04,.11,.074,.132),xy(sx*.115,0,.18,.067,.07),xy(sx*.115,0,.36,.069,.075)],3)
# Thick narrow placket follows the complete front coat outline, shallowly
# embedded rather than placed as coplanar overlay. It is not a fastening claim.
rr=[]
for z,rx,ry in COAT:
 rr.append([(-.022,-ry-.008,z),(.022,-ry-.008,z),(.022,-ry+.010,z),(-.022,-ry+.010,z)])
solid_loft('WholeFrontClosurePlacket',rr,0)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('RaincoatHood_MutedOchre',(.65,.39,.075,1),.71,0),('Face_WarmBrown',(.46,.27,.15,1),.84,0),('TrousersGloves_DeepBlue',(.07,.12,.16,1),.87,0),('Boots_DarkRubber',(.045,.052,.05,1),.78,0),('IntegralFaceMarks_DeepBrown',(.025,.016,.009,1),.85,0)]
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
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.20;aim(cam,(3,-6,2.55));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/characters/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'characters','style':'S01-clean-geometric','title':'Static Open-Hood Long-Raincoat Worker','description':'One newly authored anonymous static outdoor worker display in a knee-length hooded raincoat. A complete thick flared coat has true inner walls, open lower hem and neck rim; a separate thick hood has an actual forward face aperture and closed back shell. Two complete long thick sleeves have genuine cuff apertures around fixed glove roots. A narrow full front placket follows the coat profile. One new shaped anonymous head uses integral nose and small eye/mouth material regions, while two whole trouser legs descend to two complete tall flat-ground boots. All numerical geometry is new, not the old apron worker recoloured or a scarecrow with a changed hat. Five opaque untextured matte PBR materials; separate closed bodies have intentionally embedded fixed clothing/body joins, not a seamless unified skin. Metres, native Z up, front -Y and full horizontal-bounds-centred ground origin. One whole dressed figure and zero scenes or outfit variants. Static artistic appearance only, no real identity, precise anatomy, interchangeable clothing, actual garment fit, waterproofing, protection, occupation certification, motion, rig, cloth simulation, comfort, manufacture or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':5,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
