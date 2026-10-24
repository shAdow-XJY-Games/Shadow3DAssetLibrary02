"""One complete fixed three-strand rope-forming bench exterior. No working transmission, actual rope making or safety claim."""
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



# Complete new static rope-forming bench: separate strands through a guide to a common twisted bundle.
G={};GROUND=[];ROOT_WITNESSES=[];AIR_POINTS=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
def box(n,lo,hi,mat,role):G[n]=block(lo,hi,mat,role)
def cyl(n,a,b,r,mat,role,N=16):
 w=unit(sub(b,a));ref=(0,0,1)if abs(w[2])<.9 else(0,1,0);u=unit(cross(w,ref));v=cross(w,u);length=math.sqrt(dot(sub(b,a),sub(b,a)))
 G[n]=axial([(0,0),(r,0),(r,length),(0,length)],a,u,v,w,N,mat,role)
def sweep(points,r,N,mat,role):
 m=Mesh();rows=[]
 for i,p in enumerate(points):
  w=unit(sub(points[min(len(points)-1,i+1)],points[max(0,i-1)]));ref=(0,0,1)if abs(w[2])<.92 else(0,1,0);u=unit(cross(w,ref));v=cross(w,u)
  rows.append([add(p,add(mul(u,r*math.cos(j*math.tau/N)),mul(v,r*math.sin(j*math.tau/N))))for j in range(N)])
 for a,b in zip(rows,rows[1:]):
  for j in range(N):k=(j+1)%N;m.quad(a[j],a[k],b[k],b[j],mat)
 for p,row in[(points[0],rows[0]),(points[-1],rows[-1])]:
  for j in range(N):m.tri([p,row[j],row[(j+1)%N]],mat)
 return m.result(role)
# Full standing double bed, with no invisible supports.
for k,x in enumerate([-.63,.63]):
 n='WholeGroundRunner'+str(k+1);box(n,(x-.10,-.29,0),(x+.10,.29,.075),0,'One whole broad ground runner of the long rope-craft bench.');GROUND.append(n)
 u='WholeStandUpright'+str(k+1);box(u,(x-.065,-.065,.065),(x+.065,.065,.445),0,'One full upright rises from a complete runner to the transverse bed crosshead.');join(u,n,(x,0,.070))
 h='WholeStandCrosshead'+str(k+1);box(h,(x-.085,-.195,.410),(x+.085,.195,.465),0,'One complete transverse crosshead joins the two longitudinal bed rails.');join(h,u,(x,0,.432))
 for side,y in[('Front',-.14),('Back',.14)]:join(h,'WholeLongBedRail'+side,(x,y,.448))
for side,y in[('Front',-.14),('Back',.14)]:box('WholeLongBedRail'+side,(-.81,y-.037,.438),(.83,y+.037,.507),0,'One continuous full-length rail of the open long machine bed. The real interval between the two rails is not filled by a solid tabletop.')
# One broad shaped head plate, not a winding drum or wing cage.
head=[(-.193,.470),(.193,.470),(.193,.960),(.115,1.080),(-.115,1.080),(-.193,.960)]
G['WholeThreeAxisHeadPlate']=extrude(head,-.726,-.672,'x',0,'One complete high head plate carries three separate longitudinal hook axes and a lower central fixed crank axis. No copied lathe headstock or winch pedestal.')
for side,y in[('Front',-.14),('Back',.14)]:join('WholeThreeAxisHeadPlate','WholeLongBedRail'+side,(-.700,y,.490))
HEAD=[(0,.970),(-.104,.790),(.104,.790)]
def gear(n,x0,x1,y,z,rr,teeth,mat):
 p=[]
 for i in range(teeth):
  for t,r in[(0,rr*.88),(.18,rr),(.63,rr),(.86,rr*.88)]:
   a=math.tau*(i+t)/teeth;p.append((y+r*math.cos(a),z+r*math.sin(a)))
 G[n]=extrude(p,x0,x1,'x',mat,'One whole closed toothed-wheel appearance, independently supported by a complete shaft. Deliberate axial offsets avoid a false working tooth-engagement claim; no transmission ratio or drive operation.')
for i,(y,z)in enumerate(HEAD):
 n='WholeHookAxle'+str(i+1);cyl(n,(-.768,y,z),(-.576,y,z),.012,1,'One whole longitudinal hook axle passes through the head plate to the distinct front open hook.',16);join(n,'WholeThreeAxisHeadPlate',(-.700,y,z))
 k='WholeFixedHeadWheel'+str(i+1);gear(k,-.758,-.737,y,z,.050,12,1);join(k,n,(-.747,y,z))
 pts=[(-.562+.022*math.cos(a),y+.022*math.sin(a),z)for a in[math.pi+j*math.pi/20 for j in range(31)]];h='WholeOpenHookBar'+str(i+1);G[h]=sweep(pts,.007,10,1,'One entire finite round-bar C-shaped hook with both ends capped and a real open throat. It joins the shaft at its back curve and holds one continuous strand at its forward curve. No actual rotation, rope fastening or load claim.');join(h,n,(-.582,y-.001,z))
 AIR_POINTS.append((-.562,y,z))
cyl('WholeCentralCrankShaft',(-.850,0,.850),(-.690,0,.850),.015,1,'One full central shaft joins the broad head plate to the fixed rear drive-wheel and crank appearance.',20);join('WholeCentralCrankShaft','WholeThreeAxisHeadPlate',(-.700,0,.850))
gear('WholeRearCentralDriveWheel',-.794,-.770,0,.850,.079,20,1);join('WholeRearCentralDriveWheel','WholeCentralCrankShaft',(-.782,0,.850))
G['WholeRearCrankArm']=beam((-.830,0,.850),(-.830,-.092,.937),.027,.023,1,'One entire offset rear hand-crank arm belongs to the complete head, distinct from the front rope hooks.');join('WholeRearCrankArm','WholeCentralCrankShaft',(-.830,-.005,.855))
cyl('WholeCrankHandGrip',(-.925,-.092,.937),(-.817,-.092,.937),.023,3,'One full axial hand grip on the outer crank end, rooted in its finite arm.',16);join('WholeCrankHandGrip','WholeRearCrankArm',(-.830,-.088,.933))
# A separate whole sliding-looking separator support, fixed in this exhibit.
box('WholeSeparatorSliderCrossbar',(.105,-.185,.480),(.215,.185,.540),1,'One complete low crossbar spans both long rails and supports the separate strand-separator pedestal. Static pose, no actual sliding fit.')
for side,y in[('Front',-.14),('Back',.14)]:join('WholeSeparatorSliderCrossbar','WholeLongBedRail'+side,(.16,y,.495))
box('WholeSeparatorShortPedestal',(.128,-.040,.527),(.193,.040,.756),0,'One full short pedestal carries the complete three-aperture separator above the open bed.');join('WholeSeparatorShortPedestal','WholeSeparatorSliderCrossbar',(.16,0,.534))
# Single connected thick rectangular guide block, with three actual bores through X.
GUIDES=[(0,.895),(-.065,.790),(.065,.790)];holes=[((y-.017,z-.017),(y+.017,z+.017))for y,z in GUIDES];Y=sorted(set([-.108,.108]+[q for a,b in holes for q in[a[0],b[0]]]));Z=sorted(set([.738,.936]+[q for a,b in holes for q in[a[1],b[1]]]));cells={(i,j)for i in range(len(Y)-1)for j in range(len(Z)-1)if not any(a[0]<(Y[i]+Y[i+1])/2<b[0]and a[1]<(Z[j]+Z[j+1])/2<b[1]for a,b in holes)};m=Mesh();xa=.130;xb=.195
for i,j in cells:
 y0,y1=Y[i:i+2];z0,z1=Z[j:j+2]
 for x in[xa,xb]:m.quad((x,y0,z0),(x,y1,z0),(x,y1,z1),(x,y0,z1),0)
 for k,y in[(i-1,y0),(i+1,y1)]:
  if(k,j)not in cells:m.quad((xa,y,z0),(xb,y,z0),(xb,y,z1),(xa,y,z1),0)
 for k,z in[(j-1,z0),(j+1,z1)]:
  if(i,k)not in cells:m.quad((xa,y0,z),(xb,y0,z),(xb,y1,z),(xa,y1,z),0)
G['WholeThreeThroughGuideSeparator']=m.result('One entire connected thick strand-separator block has three separate true square bores through its full length. The three finite rope strands pass through different apertures with real surrounding air. No guide geometry is painted or copied from a peg rack.');join('WholeThreeThroughGuideSeparator','WholeSeparatorShortPedestal',(.160,0,.747))
# Distant tailstock, end shaft and a whole small fixed capture eye.
box('WholeTailstockFoot',(.660,-.180,.480),(.810,.180,.545),1,'One full tailstock bed foot bridges both complete rails, separate from the front head and central separator.')
for side,y in[('Front',-.14),('Back',.14)]:join('WholeTailstockFoot','WholeLongBedRail'+side,(.73,y,.495))
G['WholeTaperedTailstock']=extrude([(-.093,.530),(.093,.530),(.062,.865),(-.062,.865)],.704,.778,'x',0,'One complete broad tapered tailstock rises to the longitudinal end shaft and fixed eye, not a bare unrelated hook or invisible rope support.');join('WholeTaperedTailstock','WholeTailstockFoot',(.740,0,.537))
cyl('WholeTailEyeShaft',(.691,0,.835),(.830,0,.835),.015,1,'One full fixed longitudinal tail-eye shaft passes into the distant tailstock.',20);join('WholeTailEyeShaft','WholeTaperedTailstock',(.735,0,.835))
G['WholeFixedTailCaptureEye']=axial([(.0105,.678),(.029,.678),(.029,.702),(.0105,.702)],(0,0,.835),(0,1,0),(0,0,1),(1,0,0),24,1,'One full thick annular capture eye attaches to the end shaft. The three strand ends are visibly captured around its real inner opening; no tensioning, fastening or bearing performance.');join('WholeFixedTailCaptureEye','WholeTailEyeShaft',(.697,.013,.835))
# Three newly authored full-length strands. Never separate straight ropes plus a detached coil.
for i,((hy,hz),(gy,gz))in enumerate(zip(HEAD,GUIDES)):
 phase=[math.pi/2,math.pi*7/6,math.pi*11/6][i]
 points=[(-.540,hy,hz),(-.500,hy,hz),(-.300,hy*.80+gy*.20,hz*.80+gz*.20),(.090,gy,gz),(.130,gy,gz),(.195,gy,gz),(.235,gy*.68,gz*.68+.835*.32),(.285,.014*math.cos(phase),.835+.014*math.sin(phase))]
 for j in range(1,65):
  t=j/64;a=phase+t*math.tau*2.5;r=.014 if t<.90 else .014+(t-.90)*.05;points.append((.285+t*.403,r*math.cos(a),.835+r*math.sin(a)))
 n='WholeContinuousFormingStrand'+str(i+1);G[n]=sweep(points,.006,8,2,'One whole continuous finite-thickness rope-appearance strand runs from its head hook, through its own separate guide bore, then into the three-strand helical bundle and the far eye. The separate head region and joined bundle are one mesh per strand, not disconnected straight segments or a pasted rope coil. Fixed visual geometry only, no rope making, fiber twist, tension or strength simulation.');join(n,'WholeOpenHookBar'+str(i+1),(-.538,hy,hz))
 p=points[-2];q=points[-1];join(n,'WholeFixedTailCaptureEye',add(p,mul(sub(q,p),.7)))
 AIR_POINTS.append((.162,gy+.012,gz))
AIR_POINTS +=[(0,0,.470),(-.250,0,.610),(.450,0,.650),(-.600,.165,.850),(.162,0,.905),(.500,.050,.835)]
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='professional-fixed-three-strand-and-guide-rope-twisting-bench-01';VERSION='1.0.0';TITLE='Fixed Three Strand and Guide Rope Twisting Bench'
DESCRIPTION='One newly authored complete fixed rope-craft twisting-bench exterior. Two broad ground stands and full crossheads support a long open two-rail bed. A complete shaped head plate carries three independent longitudinal axles and open C-shaped hook bars, with distinct rear wheel/crank appearances supported on their own shafts. A separate low slider crossbar and pedestal carry one whole thick separator block with three true through guides. A distant complete tapered tailstock carries a full end shaft and capture eye. Three independently editable continuous finite-thickness strands run from the three hooks, pass separately through their respective guides, converge and form a fixed helical bundle ending at the far eye. No old winch drum, ratchet/pawl, four-wing winding cage, spool frame or existing rope-coil geometry is reused. The entire new longitudinal strand-forming relation, rather than hook count or wood colour, defines this whole object. Four opaque constant untextured PBR roles, metres, native Z up and actual horizontal-bounds-centred ground datum. One model, zero scenes, no operator or surroundings. Fixed illustrative craft-device exterior only: axially offset wheel appearances do not establish actual meshing gears or a transmission; no rotation, carriage movement, strand tension, fiber twist, rope formation, production rate, rope length or strength, mechanical advantage, working fastener, manufacture, ergonomics, stability, bearing load or safety claim.'
PALETTE=[('WholeTimberBedHeadAndSupports_WarmAsh',(.43,.28,.14,1),.82,0.),('FixedShaftsWheelsHookBarsAndSliders_DarkIron',(.12,.15,.15,1),.48,.60),('WholeContinuousStrands_NaturalHemp',(.68,.56,.34,1),.94,0.),('WholeCrankGrip_DarkTimber',(.16,.085,.035,1),.82,0.)]
FOCUS=(0,0,.570);ORTHO=2.25
CAMERAS={'gray-front3q':(3.8,-6,3.6),'gray-back3q':(-3.8,6,3.6),'thumbnail':(-3.8,-6,3.6),'qa-front':(-3.3,-6,3.4),'qa-side':(6,0,3.2),'qa-top':(0,0,6),'qa-back':(3.8,6,3.6),'qa-wireframe':(-3.8,-6,3.6),'silhouette-128-front':(-3.3,-6,3.4),'silhouette-128-side':(6,0,3.2)}
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
root=bpy.data.objects.new('OneFixedThreeStrandGuideRopeBench',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='two whole runners at Z0; actual bounds centred; fixed whole rope-craft bench';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==7180 and len(parts)==32
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
  files[role]={'path':f'assets/professional/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'professional','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
