import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='culture-static-palm-supported-and-split-leg-acrobat-statue-01'
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



box('WholeGroundFootPlinth',(0,0,.06),(1.32,.76,.12),2)
# New inverted head-to-hip continuous body, with full clothed silhouette.
rows=[(0,-.035,.39,.035,.035,1),(0,-.035,.43,.09,.082,1),(0,-.025,.52,.125,.113,1),(0,-.015,.60,.115,.102,1),(0,0,.65,.068,.064,1),(0,0,.70,.065,.063,0),(0,.005,.77,.205,.115,0),(0,.012,.85,.21,.13,0),(0,.025,.96,.165,.12,0),(0,.035,1.08,.125,.10,0),(0,.04,1.15,.155,.12,3),(0,.04,1.23,.185,.13,0),(0,.04,1.28,.165,.12,0)]
n=24;v=[];f=[];fm=[]
for x,y,z,rx,ry,m in rows:
 for j in range(n):a=math.tau*j/n;v.append((x+rx*math.cos(a),y+ry*math.sin(a),z))
for k in range(len(rows)-1):
 for j in range(n):q=(j+1)%n;f.append((k*n+j,k*n+q,(k+1)*n+q,(k+1)*n+j));fm.extend([rows[k][5]]*2)
for k in[0,len(rows)-1]:
 c=len(v);v.append(rows[k][:3])
 for j in range(n):f.append((c,k*n+(j+1)%n,k*n+j)if k==0 else(c,k*n+j,k*n+(j+1)%n));fm.append(rows[k][5])
mesh('WholeInvertedHeadNeckAndClothedTorso',v,f,0);FM['WholeInvertedHeadNeckAndClothedTorso']=fm
def organic_path(name,points,radii,mat,n=12):
 v=[];f=[]
 for k,p in enumerate(points):
  tangent=unit(sub(points[min(k+1,len(points)-1)],points[max(k-1,0)]));seed=(0,1,0)if abs(tangent[1])<.88 else(1,0,0);u=unit(cross(tangent,seed));w=cross(tangent,u)
  for j in range(n):v.append(tuple(p[i]+radii[k]*(u[i]*math.cos(math.tau*j/n)+w[i]*math.sin(math.tau*j/n))for i in range(3)))
 for k in range(len(points)-1):
  for j in range(n):q=(j+1)%n;f.append((k*n+j,k*n+q,(k+1)*n+q,(k+1)*n+j))
 f.extend([tuple(reversed(range(n))),tuple((len(points)-1)*n+j for j in range(n))]);mesh(name,v,f,mat)
for sg in[-1,1]:
 # Complete thin closed palms with truly flat undersides on the same plinth plane.
 vv=[(sg*.26+.067*math.cos(math.tau*j/16),-.035+.115*math.sin(math.tau*j/16),z)for z in[.12,.18]for j in range(16)];ff=[tuple(reversed(range(16))),tuple(16+j for j in range(16))]+[(j,(j+1)%16,(j+1)%16+16,j+16)for j in range(16)]
 mesh('WholePalmOnPlinth_'+str(sg),vv,ff,1)
 organic_path('WholePalmRootedBentArm_'+str(sg),[(sg*.26,0,.165),(sg*.265,.005,.29),(sg*.30,.025,.47),(sg*.265,.02,.63),(sg*.18,.005,.79)],[.047,.053,.062,.073,.085],0,16)
 # Metal relief rather than painted eyes; inverted brow position follows the downward head.
 box('WholeClosedEyelidRelief_'+str(sg),(sg*.052,-.125,.492),(.043,.022,.012),1)
organic_path('WholeHighExtendedLegAndPointedFoot',[(-.105,.04,1.23),(-.17,.035,1.42),(-.235,.02,1.63),(-.29,.005,1.84),(-.33,-.005,2.01),(-.36,-.06,2.12)],[.105,.104,.085,.07,.045,.027],0,16)
organic_path('WholeSideBentLegAndPointedFoot',[(.105,.04,1.23),(.255,.04,1.39),(.40,.03,1.51),(.51,.015,1.44),(.58,-.005,1.30),(.67,-.07,1.24)],[.105,.102,.085,.072,.047,.025],0,16)
# Short blunt inverted nose seated wholly through the front head surface.
mesh('WholeBluntSculptedNose',[(-.018,-.121,.475),(.018,-.121,.475),(.012,-.178,.502),(-.012,-.178,.502),(-.017,-.122,.55),(.017,-.122,.55),(.01,-.165,.524),(-.01,-.165,.524)],BOX,1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeClothedBody_PatinatedBronze',(.23,.34,.30,1),.67,.42),('WholeFaceAndPalms_WarmBronze',(.43,.39,.28,1),.72,.35),('WholeIntegralPlinth_CharcoalStone',(.21,.24,.24,1),.91,0),('WholeIntegralWaistBand_DeepPatina',(.13,.23,.20,1),.75,.32)]
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
focus=Vector((0,0,1.08))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.65;aim(cam,(3,-7,2.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/culture/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'culture','style':'S01-clean-geometric','title':'Static Palm Supported and Split Leg Acrobat Statue','description':'One wholly newly authored complete fixed anonymous adult-like acrobat sculpture on one integral low stone plinth. Two complete flattened palms actually meet the plinth; full bent arms rise to a connected inverted shoulder line. One continuously lofted head, short neck, shoulders, narrow waist and clothed hip mass establishes an upside-down human silhouette, not a standing figure rotated onto an invisible support. Two entire independently drawn clothed legs root in the hip: one reaches upward with a gently pointed foot, the other opens sideways through a bent knee into a distinct lower pointed foot. Closed limb lofts have deliberate finite roots into torso and palms. A small blunt nose and same-metal closed eyelid reliefs suggest an anonymous face, not a likeness or medical anatomy. All numeric surfaces newly authored; no old caryatid, seated reader, limbs, head, book or capital mesh is imported or rigidly reposed. Four opaque constant untextured patina and stone PBR roles. Metres Z up, horizontal bounds centred. One complete cultural sculpture zero scenes; pose plinth belongs to the composition, not a separate new asset. Static artistic depiction only: no human performance instruction, balance, strength, anatomical fidelity, body fit, physical equilibrium, installation or safety claim. Rigging, binding, animation and interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
