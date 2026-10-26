import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='festival-fixed-open-jaw-and-hooped-cloth-dragon-display-01'
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



# Complete thick lofted open-under cloth, with all section edges closed through wall thickness.
def open_shell(name,sections,span,thick,mat,n=24):
 v=[];K=len(sections)
 for inner in[False,True]:
  for x,y,z,ry,rz in sections:
   for i in range(n+1):
    t=math.radians(-span+2*span*i/n);v.append((x,y+(ry-(thick if inner else 0))*math.sin(t),z+(rz-(thick if inner else 0))*math.cos(t)))
 N=K*(n+1);out=[]
 for k in range(K-1):
  for i in range(n):a=k*(n+1)+i;out.append((a,a+1,a+n+2,a+n+1))
 f=[];edges={}
 for q in out:
  f.extend([q,tuple(i+N for i in reversed(q))])
  for a,b in zip(q,q[1:]+q[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((a,b))
 for es in edges.values():
  if len(es)==1:a,b=es[0];f.append((b,a,a+N,b+N))
 mesh(name,v,f,mat)
sections=[(-1.02,0,1.38,.16,.17),(-.72,.02,1.25,.19,.20),(-.40,.10,1.17,.20,.20),(-.08,.17,1.22,.19,.19),(.25,.19,1.36,.18,.18),(.58,.12,1.43,.17,.17),(.90,0,1.38,.15,.15),(1.18,-.12,1.25,.13,.13),(1.43,-.16,1.16,.105,.105),(1.65,-.12,1.19,.067,.070),(1.84,-.04,1.29,.027,.034)]
open_shell('WholeUndulatingOpenUnderClothAndTail',sections,137,.016,0)
# Whole transverse inner rings are geometric structure, not painted band decals.
for j in[0,2,4,6,8]:
 x,y,z,ry,rz=sections[j];ringx('WholeInnerHoop_'+str(j),x-.014,x+.014,y,z,ry-.026,ry+.004,1,24)
# Three poles attach to the actual low arcs of the corresponding full hoops.
for j in[0,4,8]:
 x,y,z,ry,rz=sections[j]
 box('WholeGroundFoot_'+str(j),(x,y,.025),(.14,.46,.050),2)
 lathe_z('WholeDisplayPole_'+str(j),x,y,[(0,.040),(.022,.040),(.022,z-ry+.025),(0,z-ry+.025)],1,12)
# New long roofed muzzle with a broad real open mouth underneath, not an old lion head.
head=[(-1.67,0,1.43,.13,.095),(-1.53,0,1.46,.20,.13),(-1.31,0,1.48,.23,.20),(-1.10,0,1.44,.21,.23),(-.96,0,1.38,.16,.18)]
open_shell('WholeLongMuzzleAndHeadRoof',head,105,.025,0)
# One full thick tapered jaw profile, and two complete rear cheek roots.
p=[(-1.67,-.12),(-1.53,-.19),(-1.14,-.18),(-1.02,-.12),(-1.02,.12),(-1.14,.18),(-1.53,.19),(-1.67,.12)];n=len(p);tt=triangulate(p);mesh('WholeFixedLowerJaw',[(x,y,z)for z in[1.19,1.235]for x,y in p],[tuple(reversed(t))for t in tt]+[tuple(n+i for i in t)for t in tt]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],1)
for side in[-1,1]:
 box('WholeJawRearCheek_'+str(side),(-1.08,side*.18,1.38),(.075,.065,.32),1)
 cyly('WholeJawPivot_'+str(side),side*.155-.037,side*.155+.037,-1.08,1.32,.040,2,20)
def ellipsoid(name,c,r,mat,n=16,m=8):
 v=[(c[0],c[1],c[2]-r[2])];rows=[]
 for k in range(1,m):
  t=-math.pi/2+math.pi*k/m;rows.append(list(range(len(v),len(v)+n)));v.extend((c[0]+r[0]*math.cos(t)*math.cos(math.tau*i/n),c[1]+r[1]*math.cos(t)*math.sin(math.tau*i/n),c[2]+r[2]*math.sin(t))for i in range(n))
 top=len(v);v.append((c[0],c[1],c[2]+r[2]));f=[]
 for i in range(n):f.extend([(0,rows[0][(i+1)%n],rows[0][i]),(top,rows[-1][i],rows[-1][(i+1)%n])])
 for a,b in zip(rows,rows[1:]):
  for i in range(n):j=(i+1)%n;f.append((a[i],a[j],b[j],b[i]))
 mesh(name,v,f,mat)
def tapered_path(name,points,radii,mat,n=10):
 v=[]
 for k,p in enumerate(points):
  w=unit(sub(points[min(k+1,len(points)-1)],points[max(k-1,0)]));u=unit(cross(w,(0,1,0)));b=cross(w,u)
  v.extend(tuple(p[j]+radii[k]*(u[j]*math.cos(math.tau*i/n)+b[j]*math.sin(math.tau*i/n))for j in range(3))for i in range(n))
 f=[tuple(reversed(range(n))),tuple((len(points)-1)*n+i for i in range(n))]
 for k in range(len(points)-1):
  for i in range(n):j=(i+1)%n;f.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i))
 mesh(name,v,f,mat)
for side in[-1,1]:
 ellipsoid('WholeBulgingEye_'+str(side),(-1.30,side*.195,1.62),(.078,.067,.080),3)
 ellipsoid('WholeInsetPupil_'+str(side),(-1.342,side*.232,1.63),(.041,.033,.043),2)
 tapered_path('WholeSweptHorn_'+str(side),[(-1.08,side*.12,1.62),(-1.04,side*.18,1.81),(-.90,side*.20,1.93),(-.80,side*.18,1.97)],[.044,.033,.021,.008],1)
 tapered_path('WholeContinuousWhisker_'+str(side),[(-1.58,side*.13,1.43),(-1.76,side*.20,1.38),(-1.83,side*.30,1.42),(-1.81,side*.35,1.48)],[.017,.015,.012,.008],1)
 # Short blunt lower teeth have full roots within the jaw top, not floating points.
 for i,x in enumerate([-1.53,-1.32]):beam('WholeBluntLowerTooth_'+str((side,i)),(x,side*.13,1.228),(x-.012,side*.13,1.282),.025,3)
ellipsoid('WholeBroadNose',(-1.64,0,1.515),(.052,.12,.035),2)
# A full connected dorsal cloth fringe follows the whole body, rather than floating fins.
def profile_xz(name,p,y0,y1,mat):
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);tt=triangulate(p);mesh(name,[(x,y,z)for y in[y0,y1]for x,z in p],[tuple(reversed(t))for t in tt]+[tuple(n+i for i in t)for t in tt]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],mat)
base=[(x,z+rz-.010)for x,y,z,ry,rz in sections];upper=[]
for j,(x,y,z,ry,rz)in enumerate(sections):
 upper.append((x,z+rz+(.11 if j%2==0 else .035)*(1-j/(len(sections)+1))))
p=base+list(reversed(upper));profile_xz('WholeContinuousSerratedDorsalCloth',p,-.013,.013,1)
v,f,m=G['WholeContinuousSerratedDorsalCloth']
def body_y(x):
 for a,b in zip(sections,sections[1:]):
  if a[0]<=x<=b[0]:return a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0])
 return sections[-1][1]
G['WholeContinuousSerratedDorsalCloth']=([(x,y+body_y(x),z)for x,y,z in v],f,m)
# Entire side cheek fans root into the head roof, not duplicated animal wings.
for side in[-1,1]:
 p=[(-1.24,1.39),(-1.25,1.56),(-1.16,1.70),(-1.10,1.64),(-.98,1.75),(-.98,1.61),(-.87,1.66),(-.94,1.51),(-.88,1.47),(-1.07,1.39)]
 profile_xz('WholeCheekClothFrill_'+str(side),p,side*.18-.017,side*.18+.017,1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeClothAndHead_Vermilion',(.61,.07,.035,1),.82,0),('WholeInnerHoopsJawAndHorns_Ochre',(.69,.40,.08,1),.74,0),('WholeGroundShoesNoseAndPupils_Charcoal',(.025,.035,.035,1),.79,0),('WholeEyesAndBluntTeeth_Ivory',(.81,.76,.58,1),.76,0)]
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
focus=Vector((0,0,.99))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=4.35;aim(cam,(-4,-7,3.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/festival/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'festival','style':'S01-clean-geometric','title':'Fixed Open Jaw and Hooped Cloth Dragon Display','description':'One newly authored complete processional-dragon-inspired static display prop. A full long-snouted thick upper head shell, genuine mouth opening, separate complete fixed lower jaw, two side eyes, two swept horns, two continuous whiskers and whole cheek frills lead into an entire undulating cloth-like body shell and tapering tail. A continuous serrated dorsal cloth fringe follows the whole body. The continuous thick body has an intentionally open underside exposing complete inner circular hoops; three complete upright display poles meet three whole internal hoops and stand on finite transverse ground shoes. It has no quadruped torso, legs or wings. All visible numerical geometry is new, no old lion head, dragon character, dragonboat crest or cloth model imported or cropped. The whole head-to-hooped-fabric-to-pole organisation is one supported performance-object appearance, not independent toys positioned as a scene. Four opaque PBR roles, metres Z up and horizontal-bounds-centred ground origin, one whole prop zero scenes. Anonymous simplified festival art only, no exact tradition, historical authenticity, performer, carried balance, human fit, fabric simulation, pole control, jaw movement, assembly suitability, structural load or performance safety. Static display supports are part of this one asset. Rigging animation interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
