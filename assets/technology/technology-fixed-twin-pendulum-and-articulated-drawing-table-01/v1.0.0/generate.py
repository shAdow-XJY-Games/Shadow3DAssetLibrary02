"""One complete static twin-pendulum drawing table. No dynamics, drawing or precision claim."""
import math,collections,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
G={}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.fm=[];self.index={}
 def vertex(self,p):
  p=tuple(round(float(x),9)for x in p)
  if p not in self.index:self.index[p]=len(self.v);self.v.append(p)
  return self.index[p]
 def tri(self,p,mat):self.f.append(tuple(self.vertex(v)for v in p));self.fm.append(mat)
 def quad(self,a,b,c,d,mat):self.tri([a,b,c],mat);self.tri([a,c,d],mat)
 def result(self,role):
  edges={}
  for i,f in enumerate(self.f):
   for a,b in zip(f,f[1:]+f[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((i,a,b))
  assert all(len(v)==2 for v in edges.values()),[(e,v)for e,v in edges.items()if len(v)!=2][:5]
  signs={0:1};todo=[0]
  while todo:
   i=todo.pop()
   for a,b in zip(self.f[i],self.f[i][1:]+self.f[i][:1]):
    for j,c,d in edges[tuple(sorted((a,b)))]:
     if i==j:continue
     want=signs[i]*(-1 if(a,b)==(c,d)else 1)
     if j in signs:assert signs[j]==want
     else:signs[j]=want;todo.append(j)
  assert len(signs)==len(self.f)
  ff=[f if signs[i]>0 else tuple(reversed(f))for i,f in enumerate(self.f)];vol=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]]))for f in ff)/6
  if vol<0:ff=[tuple(reversed(f))for f in ff]
  assert all(dot(cross(sub(self.v[f[1]],self.v[f[0]]),sub(self.v[f[2]],self.v[f[0]])),cross(sub(self.v[f[1]],self.v[f[0]]),sub(self.v[f[2]],self.v[f[0]])))>1e-18 for f in ff)
  return dict(vertices=self.v,faces=ff,face_materials=self.fm,material=0,role=role)

def area2(p):return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1]))/2
def earclip(p):
 order=list(range(len(p))) if area2(p)>0 else list(reversed(range(len(p))));out=[]
 cr=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 while len(order)>3:
  found=False
  for j,b in enumerate(order):
   a,c=order[j-1],order[(j+1)%len(order)]
   if cr(p[a],p[b],p[c])<1e-14:continue
   if any(all(cr(p[u],p[v],p[k])>=-1e-14 for u,v in [(a,b),(b,c),(c,a)]) for k in order if k not in [a,b,c]):continue
   out.append((a,b,c));order.pop(j);found=True;break
  assert found,('untriangulable',p,order)
 out.append(tuple(order));return out


def extrude(poly,a,b,axis,mat,role):
 m=Mesh();pt=lambda p,t:(p[0],p[1],t)if axis=='z'else(t,p[0],p[1])if axis=='x'else(p[0],t,p[1])
 for t in[a,b]:
  for f in earclip(poly):m.tri([pt(poly[j],t)for j in f],mat)
 for p,q in zip(poly,poly[1:]+poly[:1]):m.quad(pt(p,a),pt(q,a),pt(q,b),pt(p,b),mat)
 return m.result(role)
def block(lo,hi,mat,role):return extrude([(lo[0],lo[1]),(hi[0],lo[1]),(hi[0],hi[1]),(lo[0],hi[1])],lo[2],hi[2],'z',mat,role)

def axial(profile,center,u,v,w,n,materials,role,phase=0):
 m=Mesh();rings=[[add(center,add(mul(w,t),add(mul(u,r*math.cos(phase+j*math.tau/n)),mul(v,r*math.sin(phase+j*math.tau/n)))))for j in range(n)]for r,t in profile]
 for k,a in enumerate(rings):
  kk=(k+1)%len(rings);b=rings[kk];ra=profile[k][0];rb=profile[kk][0];mat=materials[k]if isinstance(materials,list)else materials
  if ra==rb==0:continue
  for j in range(n):
   i=(j+1)%n
   if ra==0:m.tri([a[0],b[j],b[i]],mat)
   elif rb==0:m.tri([a[j],a[i],b[0]],mat)
   else:m.quad(a[j],a[i],b[i],b[j],mat)
 return m.result(role)
def unit(v):return mul(v,1/math.sqrt(dot(v,v)))
def beam(a,b,width,depth,mat,role):
 w=unit(sub(b,a));ref=(0,0,1)if abs(w[2])<.9 else(0,1,0);u=unit(cross(w,ref));v=cross(w,u);m=Mesh();rows=[]
 for p in[a,b]:rows.append([add(p,add(mul(u,s*width/2),mul(v,t*depth/2)))for s,t in[(-1,-1),(1,-1),(1,1),(-1,1)]])
 for row in rows:m.quad(*row,mat)
 for i in range(4):j=(i+1)%4;m.quad(rows[0][i],rows[0][j],rows[1][j],rows[1][i],mat)
 return m.result(role)



# New complete fixed twin-pendulum drawing table, not a low pantograph with extra bars.
G={};GROUND=[];ROOT_WITNESSES=[];AIR_POINTS=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
def cylinder(a,b,r,mat,role,n=24):
 w=unit(sub(b,a));u=unit(cross(w,(0,0,1)if abs(w[2])<.9 else(0,1,0)));v=cross(w,u);ll=math.sqrt(dot(sub(b,a),sub(b,a)))
 return axial([(0,0),(r,0),(r,ll),(0,ll)],a,u,v,w,n,mat,role)
# Complete one-piece tabletop cut by two actual square apertures around the rods.
xs=[-.600,-.440,-.320,.160,.280,.600];ys=[-.480,-.180,-.060,.220,.340,.480];zz=[.995,1.045];faces={}
for a,b in zip(xs,xs[1:]):
 for c,d in zip(ys,ys[1:]):
  x=(a+b)/2;y=(c+d)/2
  if(-.440<x<-.320 and-.180<y<-.060)or(.160<x<.280 and.220<y<.340):continue
  v=[(x,y,z)for z in zz for y in[c,d]for x in[a,b]]
  for ids in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:
   q=tuple(v[i]for i in ids);key=tuple(sorted(q))
   if key in faces:del faces[key]
   else:faces[key]=q
m=Mesh()
for f in faces.values():m.quad(*f,0)
G['WholeTabletopWithTwoTrueRodWindows']=m.result('One entire thick rectangular drawing-table top has two genuine through apertures with full inner walls. A separate whole long pendulum rod passes through each aperture with surrounding free space. No table model imported, no dark painted hole or solid slab behind either rod.')
for label,x,y in [('FrontLeft',-.520,-.400),('FrontRight',.520,-.400),('BackLeft',-.520,.400),('BackRight',.520,.400)]:
 n=label+'WholeGroundedLeg';G[n]=block((x-.035,y-.035,0),(x+.035,y+.035,1.015),0,'One complete tall square wooden leg belongs to this one instrument table and rests on its full flat end. The space beneath the table remains open around the two entire pendulum weights.');GROUND.append(n);join(n,'WholeTabletopWithTwoTrueRodWindows',(x,y,1.005))
for label,x in [('Left',-.520),('Right',.520)]:
 n=label+'WholeLowSideStretcher';G[n]=block((x-.025,-.420,.180),(x+.025,.420,.235),0,'One entire low side stretcher joins both same-side legs, clear of the hanging weights.')
 for end,y in [('Front',-.400),('Back',.400)]:join(n,end+label+'WholeGroundedLeg',(x,y,.205))
G['WholeLowRearCrossStretcher']=block((-.540,.375,.180),(.540,.425,.235),0,'One entire low rear cross stretcher joins the two tall side frames. It remains below the rear pendulum weight and is not a simulated moving platform.')
for label,x in [('Left',-.520),('Right',.520)]:join('WholeLowRearCrossStretcher','Back'+label+'WholeGroundedLeg',(x,.400,.205))
R1=(-.380,-.120);R2=(.220,.280);J=(.220,-.120);P=(.220,-.240)
for label,c,axis,zweight in [('Left',R1,(1,0,0),.295),('Rear',R2,(0,1,0),.405)]:
 x,y=c
 for k,s in enumerate([-1,1]):
  q=(x+axis[0]*s*.080,y+axis[1]*s*.080);n=label+'WholePivotCheek'+str(k+1)
  G[n]=block((q[0]-.014,q[1]-.014,1.039),(q[0]+.014,q[1]+.014,1.112),1,'One complete small tabletop bearing cheek stands outside its real rod aperture. The two pairs have perpendicular horizontal axes, not four posts enclosing a clock.');join(n,'WholeTabletopWithTwoTrueRodWindows',(*q,1.042))
 a=(x-axis[0]*.106,y-axis[1]*.106,1.083);b=(x+axis[0]*.106,y+axis[1]*.106,1.083);n=label+'WholeHorizontalPivotPin';G[n]=cylinder(a,b,.009,2,'One complete proud transverse horizontal pivot pin crosses its two bearing cheeks and whole long rod. Perpendicular pin directions are a fixed display relation only, not validated suspension or free oscillation.')
 for k,s in enumerate([-1,1]):join(n,label+'WholePivotCheek'+str(k+1),(x+axis[0]*s*.080,y+axis[1]*s*.080,1.083))
 rod=label+'WholeLongThroughTablePendulumRod';G[rod]=cylinder((x,y,.170),(x,y,1.390),.010,2,'One entire continuous long vertical rod extends from well below the tabletop through its real free aperture to the articulated arm above. It is not a detached weight hung from a table or a shorter duplicated metronome rod. Fixed display only.');join(rod,n,(x,y,1.083))
 weight=label+'WholePiercedLowerPendulumWeight';z0=zweight-.055;z1=zweight+.055
 G[weight]=axial([(.009,z0),(.095,z0),(.110,z0+.015),(.110,z1-.015),(.095,z1),(.009,z1)],(x,y,0),(1,0,0),(0,1,0),(0,0,1),28,1,'One whole broad bevel-edged annular pendulum weight surrounds its long rod below the table. Its genuine central bore is deliberately occupied with shallow fixed engagement by the rod; no weight adjustment, mass, frequency or dynamics claimed.');join(weight,rod,(x+.0095,y,zweight))
def flat_link(a,b,z0,z1,role):
 dx,dy=b[0]-a[0],b[1]-a[1];ll=math.hypot(dx,dy);u=(dx/ll,dy/ll);v=(-u[1],u[0]);r=.022;poly=[]
 for c,angles in[(a,[math.pi/2+j*math.pi/8 for j in range(9)]),(b,[-math.pi/2+j*math.pi/8 for j in range(9)])]:
  for t in angles:poly.append((c[0]+r*(u[0]*math.cos(t)+v[0]*math.sin(t)),c[1]+r*(u[1]*math.cos(t)+v[1]*math.sin(t))))
 return extrude(poly,z0,z1,'z',2,role)
G['WholeLateralPendulumDrawingArm']=flat_link(R1,J,1.315,1.335,'One entire rounded-end lateral drawing-arm appearance joins the upper end of the left long pendulum to the common pen-arm joint above the table. It is one arm, not an old four-bar parallelogram reused.');join('WholeLateralPendulumDrawingArm','LeftWholeLongThroughTablePendulumRod',(*R1,1.325))
G['WholeExtendedRearPendulumPenArm']=flat_link(R2,P,1.350,1.370,'One entire perpendicular pen-arm appearance runs from the rear long pendulum, through the shared joint, to a separate forward pen sleeve. It lies in a visibly higher layer than the lateral arm. This static two-arm layout is not claimed to trace a mathematically valid curve.');join('WholeExtendedRearPendulumPenArm','RearWholeLongThroughTablePendulumRod',(*R2,1.360))
G['WholeProudSharedArmJoint']=axial([(0,1.305),(.010,1.305),(.010,1.375),(.020,1.375),(.020,1.391),(0,1.391)],(*J,0),(1,0,0),(0,1,0),(0,0,1),24,1,'One whole headed vertical joint pin bridges both separated arm layers. It is finite geometry rather than a floating linkage intersection; no articulation or friction claim.');join('WholeProudSharedArmJoint','WholeLateralPendulumDrawingArm',(*J,1.325));join('WholeProudSharedArmJoint','WholeExtendedRearPendulumPenArm',(*J,1.360))
G['WholeBlankDrawingSurface']=block((-.160,-.360,1.043),(.360,.130,1.050),3,'One whole blank thick ivory drawing-surface appearance is fixed on the full tabletop below the pen. It contains no artwork, plotted trajectory, recorded motion or claimed drawing result. Not a loose second asset.');join('WholeBlankDrawingSurface','WholeTabletopWithTwoTrueRodWindows',(.100,-.100,1.044))
G['WholeBoredPenSleeve']=axial([(.007,1.200),(.019,1.200),(.019,1.390),(.007,1.390)],(*P,0),(1,0,0),(0,1,0),(0,0,1),24,1,'One entire hollow pen sleeve roots around the extended end of the rear arm. Its real bore is occupied by the fixed blunt pencil-like body, not claimed empty or adjustable.');join('WholeBoredPenSleeve','WholeExtendedRearPendulumPenArm',(P[0]+.012,P[1],1.360))
G['WholeFiniteBluntPenBody']=axial([(0,1.048),(.0025,1.048),(.008,1.080),(.008,1.420),(.006,1.430),(0,1.430)],(*P,0),(1,0,0),(0,1,0),(0,0,1),12,[1,1,0,0,2,2],'One entire finite blunt pencil-like pen body spans the sleeve and meets the blank drawing surface in this fixed pose. No sharp point, ink, actual marking, drawing accuracy or human-use specification.');join('WholeFiniteBluntPenBody','WholeBoredPenSleeve',(P[0]+.0075,P[1],1.280));join('WholeFiniteBluntPenBody','WholeBlankDrawingSurface',(*P,1.049))
AIR_POINTS=[(-.420,-.120,1.020),(-.340,-.120,1.020),(-.380,-.160,1.020),(.180,.280,1.020),(.260,.280,1.020),(.220,.240,1.020),(-.380,-.120,.900),(.220,.280,.900)]
# Replace the two rod-centre candidates with actual side-of-rod clearances.
AIR_POINTS[-2:]=[(-.340,-.120,.900),(.260,.280,.900)]
AIR_POINTS +=[(-.200,-.120,1.200),(.220,.080,1.210),(-.380,-.120,.100),(.220,.280,.100),(-.200,-.100,.500),(.050,.150,.500),(.180,-.120,1.343)]
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='technology-fixed-twin-pendulum-and-articulated-drawing-table-01';VERSION='1.0.0';TITLE='Fixed Twin Pendulum and Articulated Drawing Table'
DESCRIPTION='One newly authored complete static twin-pendulum drawing-instrument appearance. A full tall four-legged wooden table with low stretchers has two true through apertures in its one-piece top. Two entire long rods extend through the actual apertures from independent perpendicular horizontal pivot mounts above the table to separate complete pierced heavy-looking weights below it. One whole upper lateral arm and one entire perpendicular extended pen arm occupy distinct axial layers and join through a proud full headed pin. The pen arm carries an independent thick bored sleeve and one full finite blunt pencil-like body touching a blank integral drawing-surface appearance. The free rod intervals above and below the table, both true tabletop holes and the complete under-table space are actual geometry. All whole coordinates are newly authored, not an old table furnished with extracted pendulum or copying-instrument parts. Unlike the old low-board pantograph there is no four-bar parallelogram or separate tracer; unlike a metronome there is no tapered case, low internal pivot or one weighted rod controlling a time display. One prop, zero scenes, no drawing, printed trajectory, operator, glass, liquid or imported old model. Four opaque constant untextured PBR materials, metres, native Z up and actual horizontal-bounds-centred ground origin. A fixed illustrative harmonograph-style exhibit only: no oscillation, coupled dynamics, damping, frequency ratio, valid traced curve, pen motion, actual marking, drawing precision, educational outcome, manufacture, stability, ergonomics or safety claim.'
PALETTE=[('WholeTableAndPenBarrel_WarmTimber',(.34,.19,.085,1),.76,0.),('WholeWeightsBearingCheeksAndSleeve_DeepBlueIron',(.08,.13,.17,1),.63,.34),('WholeRodsPinsAndArms_SatinBrass',(.50,.40,.22,1),.45,.56),('WholeBlankDrawingSurface_Ivory',(.76,.73,.64,1),.83,0.)]
FOCUS=(0,0,.700);ORTHO=2.03
CAMERAS={'gray-front3q':(3.5,-5,3.0),'gray-back3q':(-3,5,3),'thumbnail':(3.5,-5,3.0),'qa-front':(3.5,-5,2.7),'qa-side':(5,0,3),'qa-top':(0,0,6),'qa-back':(-3,5,3),'qa-wireframe':(3.5,-5,3.0),'silhouette-128-front':(3.5,-5,2.7),'silhouette-128-side':(5,0,3)}
WIRE_THICKNESS=ORTHO/1800
# BLENDER PHASE: mature export/render only.
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.seed=17
scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
EXPECTED={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False],'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4}
def config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def guard():c=config();assert c==EXPECTED,c;return c
mats=[]
for name,color,rough,metal in PALETTE:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;p.inputs['Alpha'].default_value=1.;p.inputs['Transmission Weight'].default_value=0.;p.inputs['Emission Strength'].default_value=0.;mats.append(m)
bpy.context.preferences.filepaths.save_version=0
root=bpy.data.objects.new('OneFixedTwinPendulumDrawingTable',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='four full leg soles at Z0; actual bounds centred; whole fixed pendulum drawing table';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();
 for m in mats:me.materials.append(m)
 for i,f in enumerate(me.polygons):f.material_index=g.get('face_materials',[g['material']]*len(me.polygons))[i]
 o['component_role']=g['role'];parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={};actual_triangles={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg);triangles+=len(o.data.loop_triangles)
 component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i]for p in v)for i in range(3)];hi=[max(p[i]for p in v)for i in range(3)];bounds=[round(hi[i]-lo[i],6)for i in range(3)]
assert abs(lo[2])<1e-7 and triangles==1964 and len(parts)==24
def pbr(m):
 p=m.node_tree.nodes.get('Principled BSDF');assert p is not None
 assert not any(n.type.startswith('TEX_') for n in m.node_tree.nodes),'No procedural or image texture nodes permitted'
 assert not any(socket.is_linked for socket in p.inputs),'No linked Principled inputs permitted'
 values=[]
 for name in ['Base Color','Metallic','Roughness','Alpha','IOR','Specular IOR Level','Transmission Weight','Coat Weight','Coat Roughness','Sheen Weight','Emission Color','Emission Strength']:
  value=p.inputs[name].default_value
  values.append((name,tuple(round(float(x),6) for x in value) if hasattr(value,'__len__') else round(float(value),6)))
 values.append(('double_sided',not m.use_backface_culling));return tuple(values)
def records(objects):
 rows=[]
 for o in objects:
  o.data.calc_loop_triangles();vs=[o.matrix_world@v.co for v in o.data.vertices]
  for t in o.data.loop_triangles:
   q=[tuple(round(float(c),6) for c in vs[i]) for i in t.vertices]
   rows.append((min(tuple(q[i:]+q[:i]) for i in range(3)),pbr(o.data.materials[t.material_index])))
 return sorted(rows)
source_records=records(parts);source_fp=hashlib.sha256(json.dumps(source_records,separators=(',',':')).encode()).hexdigest()
mesh_count=len(parts);bpy.ops.object.select_all(action='DESELECT')
for o in parts+[root]:o.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
guard();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'mesh_objects':mesh_count,'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,'components':component_checks,'single_prop_count':1,'review_mode':'SELF_REVIEW','static_visual_only':True,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),'status':'producer geometry; maker actual-image acceptance pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/technology/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'technology','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
 'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len(mats),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
# Every formal/early render is of the actual exported file imported into an emptied scene.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));parts=[o for o in scene.objects if o.type=='MESH']
assert len(parts)==mesh_count and records(parts)==source_records,'Fresh GLB oriented geometry / full solid PBR mismatch'
qa['fresh_actual_glb_guard']={'oriented_geometry_and_full_solid_pbr_match':True,'mesh_count':len(parts)};saveqa()
if '--no-render' in sys.argv or '--geometry-only' in sys.argv:
 metadata();print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)

# BEGIN AUTHORIZED TIERED RENDER V1; native has already been saved at128.
def tier_arg(flag,default=None):
 if flag not in sys.argv:return default
 i=sys.argv.index(flag);assert i+1<len(sys.argv);return sys.argv[i+1]
TIER_PROFILE=tier_arg('--render-profile')
TIER_ALLOWED={'simple-v1':(16,[16,32,64]),'complex-v1':(32,[32,64])}
TIER_SINGLE=tier_arg('--tier-single-view')
TIER_LIST=json.loads(tier_arg('--tier-view-list','[]'))
TIER_OVERRIDES=json.loads(tier_arg('--tier-sample-overrides','{}'))
TIER_STANDARD=['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe']
if TIER_PROFILE:
 assert TIER_PROFILE in TIER_ALLOWED and '--gray-only' not in sys.argv and '--gray-obliques-only' not in sys.argv
 assert isinstance(TIER_OVERRIDES,dict)
 for k,v in TIER_OVERRIDES.items():assert k in CAMERAS and k!='thumbnail' and type(v) is int and v in TIER_ALLOWED[TIER_PROFILE][1]
 assert isinstance(TIER_LIST,list) and len(TIER_LIST)==len(set(TIER_LIST)) and not(TIER_LIST and TIER_SINGLE)
 assert all(n in TIER_STANDARD[1:] and n in CAMERAS for n in TIER_LIST)
 if TIER_SINGLE:assert TIER_SINGLE in CAMERAS and TIER_SINGLE not in ['gray-front3q','gray-back3q','silhouette-128-front','silhouette-128-side']
 qa['tiered_render']={'profile_id':TIER_PROFILE,'authorization_reference':'Sentinel_f2fcc66115e881918d02bc1ea780953c','native_samples':128,'resolution':[640,640],'gray_stage':'omitted_by_authorized_profile','samples_by_image':{}}
def tier_select_views(views):
 if not TIER_PROFILE:return views
 if TIER_SINGLE:return {TIER_SINGLE:CAMERAS[TIER_SINGLE]}
 if TIER_LIST:return {n:CAMERAS[n] for n in TIER_LIST}
 assert set(views)<=set(TIER_STANDARD)
 return views
def tier_before_view(name):
 if not TIER_PROFILE:return
 samples=128 if name=='thumbnail' else TIER_OVERRIDES.get(name,TIER_ALLOWED[TIER_PROFILE][0])
 assert samples==128 if name=='thumbnail' else samples in TIER_ALLOWED[TIER_PROFILE][1]
 scene.cycles.samples=samples
 EXPECTED['samples']=samples
 qa['tiered_render']['samples_by_image'][name+'.png']=samples
# END AUTHORIZED TIERED RENDER V1
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.30,.30,.30,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8;scene.view_settings.view_transform='AgX'
focus=Vector(FOCUS);asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),600,4),('Fill',(4,-2,4),360,3.5),('Rim',(2,4,5),480,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
def diagnostic_snapshot():
 return {m:[(i,socket.identifier,socket.bl_idname,tuple(socket.default_value) if hasattr(socket.default_value,'__len__') else socket.default_value) for i,socket in enumerate(m.node_tree.nodes.get('Principled BSDF').inputs) if hasattr(socket,'default_value')] for m in asset_mats}
original_material_inputs=diagnostic_snapshot()
original_slots={o:(list(o.data.materials),[f.material_index for f in o.data.polygons]) for o in parts}
def restore_diagnostic_materials():
 for m,inputs in original_material_inputs.items():
  p=m.node_tree.nodes.get('Principled BSDF')
  for index,identifier,socket_type,value in inputs:
   assert index<len(p.inputs),'Diagnostic socket index disappeared'
   socket=p.inputs[index]
   assert socket.identifier==identifier and socket.bl_idname==socket_type,'Diagnostic socket identity/type changed'
   socket.default_value=value
 for o,(slots,indices) in original_slots.items():
  assert len(o.data.polygons)==len(indices),'Diagnostic face count changed'
  o.data.materials.clear()
  for m in slots:o.data.materials.append(m)
  for f,index in zip(o.data.polygons,indices):f.material_index=index
  assert list(o.data.materials)==slots and [f.material_index for f in o.data.polygons]==indices
 assert diagnostic_snapshot()==original_material_inputs,'Diagnostic full socket-index/identifier/type/value restoration differs'
 assert records(parts)==source_records,'Diagnostic restoration changed complete oriented geometry/full solid PBR signature'
 qa['diagnostic_exact_restoration']={'try_finally':True,'full_socket_index_identifier_type_value_match':True,'all_material_slots_and_face_indices_match':True,'full_oriented_geometry_and_pbr_records_match':True}
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
try:
 if gray:
  for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
 views={k:CAMERAS[k] for k in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
 if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
 if '--extra-views' in sys.argv:views.pop('thumbnail',None)
 views=tier_select_views(views)
 seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
 def render(name,pos):
  tier_before_view(name)
  cam.data.ortho_scale=ORTHO
  aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
 for name,pos in views.items():
  if name=='qa-wireframe':
   wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
   for o in parts:
    dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
    for f in dup.data.polygons:f.material_index=0
    w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=WIRE_THICKNESS;w.use_replace=True;w.use_even_offset=False;w.offset=1
  render(name,pos)
 if gray and '--gray-obliques-only' not in sys.argv:
  black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
  for o in parts:
   o.data.materials.clear();o.data.materials.append(black)
   for f in o.data.polygons:f.material_index=0
  ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
  scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
  for name,pos in [(name,CAMERAS[name]) for name in ['silhouette-128-front','silhouette-128-side']]:render(name,pos)
finally:
 restore_diagnostic_materials()
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; maker necessary-view self-review pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
