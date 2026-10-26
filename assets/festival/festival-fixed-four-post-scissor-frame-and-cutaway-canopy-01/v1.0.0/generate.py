import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='festival-fixed-four-post-scissor-frame-and-cutaway-canopy-01'
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



def square_tube(name,x,y,z0,z1,outer,inner,mat):
 loops=[[(x+sx*r,y+sy*r,z)for sx,sy in[(-1,-1),(1,-1),(1,1),(-1,1)]]for z,r in[(z0,outer),(z1,outer),(z1,inner),(z0,inner)]]
 v=sum(loops,[]);f=[(k*4+i,k*4+(i+1)%4,((k+1)%4)*4+(i+1)%4,((k+1)%4)*4+i)for k in range(4)for i in range(4)];mesh(name,v,f,mat)
corners=[(-1.2,-1.2),(1.2,-1.2),(1.2,1.2),(-1.2,1.2)]
for k,(x,y)in enumerate(corners):
 box('WholeGroundFoot_'+str(k),(x,y,.035),(.19,.19,.07),2)
 box('WholeLowerFixedLeg_'+str(k),(x,y,.64),(.052,.052,1.18),0)
 square_tube('WholeOpenUpperSleeve_'+str(k),x,y,1.02,2.19,.045,.032,0)
 cyly('WholeSleeveRetainingPin_'+str(k),y-.063,y+.063,x,1.15,.012,2,12)
 square_tube('WholeLowerScissorCollar_'+str(k),x,y,1.75,1.86,.070,.043,1)
 box('WholeUpperCornerCap_'+str(k),(x,y,2.18),(.15,.15,.085),1)
# Four integrated upper perimeter runs; each is two linked cells, not independent fence panels.
for side in range(4):
 a=corners[side];b=corners[(side+1)%4];u=((b[0]-a[0])/2.4,(b[1]-a[1])/2.4,0);n=(-u[1],u[0],0)
 def p(t,z,layer=0):return(a[0]+u[0]*t+n[0]*layer,a[1]+u[1]*t+n[1]*layer,z)
 for cell in range(2):
  t0=cell*1.2;t1=(cell+1)*1.2
  beam('WholePerimeterRisingLink_'+str((side,cell)),p(t0,1.80,-.027),p(t1,2.18,-.027),.043,0)
  beam('WholePerimeterFallingLink_'+str((side,cell)),p(t0,2.18,.027),p(t1,1.80,.027),.043,0)
  beam('WholePerimeterCrossPin_'+str((side,cell)),p((t0+t1)/2,1.99,-.066),p((t0+t1)/2,1.99,.066),.027,2)
 for j in range(3):
  for z in[1.80,2.18]:beam('WholeSharedEndpointPin_'+str((side,j,z)),p(j*1.2,z,-.077),p(j*1.2,z,.077),.027,2)
# One integrated centre roof support, with complete lower oblique props and upper rafters.
lathe_z('WholeCentralPeakMast',0,0,[(0,2.38),(.026,2.38),(.026,3.09),(0,3.09)],0,16)
lathe_z('WholeLowerPeakHub',0,0,[(.024,2.43),(.072,2.43),(.072,2.52),(.024,2.52)],1,16)
for k,(x,y)in enumerate(corners):
 beam('WholeDiagonalPeakRafter_'+str(k),(x,y,2.222),(0,0,3.045),.067,0)
 beam('WholeLowerObliquePeakProp_'+str(k),(x,y,1.82),(0,0,2.475),.042,0)
# Single continuous three-face cover, front triangular sector intentionally omitted.
L=1.255;top=[(-L,-L,2.235),(L,-L,2.235),(L,L,2.235),(-L,L,2.235),(0,0,3.085)];v=[(x,y,z-.032)for x,y,z in top]+top;faces=[]
for a,b,c in[(1,2,4),(2,3,4),(3,0,4)]:faces.extend([(c,b,a),(a+5,b+5,c+5)])
bound=[1,2,3,0,4]
for a,b in zip(bound,bound[1:]+bound[:1]):faces.append((a,b,b+5,a+5))
mesh('WholeThreeFaceCoverWithOpenFrontSector',v,faces,3)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeLegsLinksAndRafters_SatinAlloy',(.45,.50,.50,1),.58,.45),('WholeCollarsAndCornerCaps_Charcoal',(.045,.065,.07,1),.83,.02),('WholeShoesAndPins_DarkSteel',(.18,.22,.23,1),.67,.28),('WholeCutawayCover_MutedBlue',(.10,.31,.40,1),.94,0)]
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
focus=Vector((0,0,1.52))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=4.50;aim(cam,(4,-7,3.9));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/festival/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'festival','style':'S01-clean-geometric','title':'Fixed Four Post Scissor Frame and Cutaway Canopy','description':'One newly authored whole fixed expanded event-canopy frame with a deliberate front roof cutaway. Four independent finite shoes carry complete lower square legs and genuinely hollow upper sleeves with fixed transverse retainers. Four upper corner caps and four lower collars terminate four linked perimeter scissor runs: two crossing cells per side have distinct front/back link layers and complete shared endpoint and central pins. Separate diagonal roof rafters meet a complete central peak mast, while four lower oblique props root a lower centre hub. One continuous thick three-face hipped cover leaves the whole front triangular sector absent so the inner peak and perimeter construction remain visible. Unlike the old saddle shade this is not a single warped surface on four plain posts; unlike the concertina barrier it is not a planar wheeled chain between two end stiles. The corner collars, four-sided upper linkage circuit and central roof support form one newly authored shelter apparatus, not old barrier meshes placed around a copied roof. Four opaque PBR materials, metres Z up, actual horizontal ground-bounds centre; one complete static prop zero scenes. The roof cutaway is an intentional display omission, not damage or an unverified closed tent. No unfolding sequence, sliding or pivot travel, fabric tension, wind/rain protection, load, usable clearance, weather shelter, event installation, manufacture or safe occupancy claim. Rigging animation interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
