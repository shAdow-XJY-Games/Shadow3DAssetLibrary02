"""One newly authored complete fixed balanced lattice tower crane. Static art only; no lifting, load or construction performance."""
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



def solid_union(boxes,mat,role):
 xs=sorted({p[0]for b in boxes for p in b});ys=sorted({p[1]for b in boxes for p in b});zs=sorted({p[2]for b in boxes for p in b});faces={};m=Mesh()
 for i in range(len(xs)-1):
  for j in range(len(ys)-1):
   for k in range(len(zs)-1):
    c=((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)
    if not any(all(lo[t]<c[t]<hi[t]for t in range(3))for lo,hi in boxes):continue
    vv=[(x,y,z)for z in[zs[k],zs[k+1]]for y in[ys[j],ys[j+1]]for x in[xs[i],xs[i+1]]]
    for f in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:
     q=tuple(vv[t]for t in f);key=tuple(sorted(q))
     if key in faces:del faces[key]
     else:faces[key]=q
 for q in faces.values():m.quad(*q,mat)
 return m.result(role)
def cyl(n,a,b,r,mat,role,N=24):
 w=unit(sub(b,a));ref=(0,0,1)if abs(w[2])<.9 else(0,1,0);u=unit(cross(w,ref));v=cross(w,u);h=math.sqrt(dot(sub(b,a),sub(b,a)))
 G[n]=axial([(0,0),(r,0),(r,h),(0,h)],a,u,v,w,N,mat,role)
# Newly authored complete balanced tower crane illustration; no old crane meshes imported.
ROOT_WITNESSES=[];AIR_POINTS=[];GROUND=['WholeBroadTowerFoot']
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
def lattice_panel(x0,x1,z0,z1,bays,thick,mat,transform,role):
 # Each bay is a complete four-cell ring around one true diamond opening.
 # Adjacent bays share a whole boundary face, cancelled before surface emission.
 faces={};m=Mesh()
 for k in range(bays):
  a=x0+(x1-x0)*k/bays;b=x0+(x1-x0)*(k+1)/bays;cx=(a+b)/2;cz=(z0+z1)/2
  margin=min((b-a)*.17,(z1-z0)*.20)
  outer=[(a,z0),(b,z0),(b,z1),(a,z1)];inner=[(cx,z0+margin),(b-margin,cz),(cx,z1-margin),(a+margin,cz)]
  for j in range(4):
   q=(j+1)%4;poly=[outer[j],outer[q],inner[q],inner[j]];rows=[[(x,t,z)for x,z in poly]for t in[-thick/2,thick/2]]
   fs=[rows[0],rows[1]]+[[rows[0][i],rows[0][(i+1)%4],rows[1][(i+1)%4],rows[1][i]]for i in range(4)]
   for f in fs:
    key=tuple(sorted(tuple(round(c,10)for c in p)for p in f))
    if key in faces:del faces[key]
    else:faces[key]=f
 for f in faces.values():
  if max(p[1]for p in f)-min(p[1]for p in f)<1e-12:
   for tri in earclip([(p[0],p[2])for p in f]):m.tri([transform(f[j])for j in tri],mat)
  else:m.quad(*[transform(p)for p in f],mat)
 return m.result(role)
G['WholeBroadTowerFoot']=block((-.76,-.76,0),(.76,.76,.16),2,'One complete broad finite tower ground foot, illustrative only and not an engineered foundation.')
for ix,x in enumerate([-.32,.32]):
 for iy,y in enumerate([-.32,.32]):
  n='WholeTowerCornerPost'+str(ix)+str(iy);G[n]=block((x-.055,y-.055,.13),(x+.055,y+.055,3.34),0,'One full vertical corner member of the four-sided tower.');join(n,'WholeBroadTowerFoot',(x,y,.145))
for label,y,iy in [('Front',-.32,0),('Back',.32,1)]:
 n=label+'WholeTowerDiamondWeb';G[n]=lattice_panel(.18,3.30,-.32,.32,4,.055,0,lambda p,y=y:(p[2],y+p[1],p[0]),'One entire connected tower face web with four actual diamond apertures, not separate floating braces.')
 join(n,'WholeTowerCornerPost0'+str(iy),(-.31,y,.22));join(n,'WholeTowerCornerPost1'+str(iy),(.31,y,.22))
for label,x,ix in [('Left',-.32,0),('Right',.32,1)]:
 n=label+'WholeTowerDiamondWeb';G[n]=lattice_panel(.18,3.30,-.32,.32,4,.055,0,lambda p,x=x:(x+p[1],p[2],p[0]),'One complete side tower web with real repeated open cells; parts remain a single crane, never counted separately.')
 join(n,'WholeTowerCornerPost'+str(ix)+'0',(x,-.31,.22))
G['WholeTowerUpperPlatform']=block((-.49,-.49,3.27),(.49,.49,3.44),0,'Whole upper mast platform, fixed with small buried corner connections.');join('WholeTowerUpperPlatform','WholeTowerCornerPost00',(-.32,-.32,3.31))
cyl('WholeFixedSlewingStyleDrum',(0,0,3.41),(0,0,3.61),.37,1,'One complete fixed broad drum above mast; no rotating bearing or drive is made.',32);join('WholeFixedSlewingStyleDrum','WholeTowerUpperPlatform',(0,0,3.425))
G['WholeUpperHeadCrossBody']=block((-.43,-.30,3.57),(.43,.30,3.81),0,'Whole central head joining the two unequal arms, side cabin and upper pylon.');join('WholeUpperHeadCrossBody','WholeFixedSlewingStyleDrum',(0,0,3.59))
# Whole three-sided main jib has a real triangular section and longitudinal lattice apertures.
for label,sgn in [('Near',-1),('Far',1)]:
 n=label+'WholeMainJibLatticeSide';G[n]=lattice_panel(.24,3.75,3.74,4.20,5,.052,0,lambda p,sgn=sgn:(p[0],sgn*(.24-(p[2]-3.74)*.24/.46)+p[1],p[2]),'One complete sloped side of the triangular main jib with five true diamond windows. No old I-beam is stretched or imported.')
 join(n,'WholeUpperHeadCrossBody',(.30,sgn*.225,3.77))
G['WholeMainJibLowerLattice']=lattice_panel(.24,3.75,-.24,.24,5,.052,0,lambda p:(p[0],p[2],3.74+p[1]),'One whole open lower web completing the triangular-section main jib.')
join('WholeMainJibLowerLattice','WholeUpperHeadCrossBody',(.30,-.22,3.75))
G['WholeShortCounterJibFrame']=solid_union([(( -1.65,-.29,3.64),(.00,-.20,3.85)),((-1.65,.20,3.64),(.00,.29,3.85)),((-1.65,-.20,3.64),(-1.50,.20,3.85)),((-.10,-.20,3.64),(.00,.20,3.85)),((-1.52,-.20,3.64),(-1.20,.20,3.71))],0,'One entire short counter-jib open frame opposite the long triangular working jib. Actual interior window retained.')
join('WholeShortCounterJibFrame','WholeUpperHeadCrossBody',(-.05,-.24,3.75))
G['WholeCounterweightExterior']=block((-1.61,-.34,3.68),(-1.22,.34,4.15),2,'One complete fixed counterweight-style mass occupying the short rear frame, without calculated balance or load claim.');join('WholeCounterweightExterior','WholeShortCounterJibFrame',(-1.42,0,3.695))
G['WholeOpenAFrameTowerHead']=extrude([(-.36,3.76),(-.08,4.77),(.08,4.77),(.36,3.76),(.245,3.76),(0,4.55),(-.245,3.76)],-.055,.055,'y',0,'One complete open A-shaped upper pylon, rooted at two distinct lower legs.');join('WholeOpenAFrameTowerHead','WholeUpperHeadCrossBody',(-.30,0,3.79))
G['WholeForwardFixedJibTie']=beam((0,0,4.71),(3.30,0,4.17),.034,.034,1,'One entire taut-looking fixed tie between head pylon and main-jib apex. No cable tension or movement simulated.');join('WholeForwardFixedJibTie','WholeOpenAFrameTowerHead',(.02,0,4.706));join('WholeForwardFixedJibTie','NearWholeMainJibLatticeSide',(3.28,0,4.173))
G['WholeRearFixedCounterTie']=beam((-.01,0,4.70),(-1.43,0,4.11),.034,.034,1,'One complete rear head tie into the short counterweight assembly.');join('WholeRearFixedCounterTie','WholeOpenAFrameTowerHead',(-.03,0,4.692));join('WholeRearFixedCounterTie','WholeCounterweightExterior',(-1.42,0,4.115))
# Whole side cab has real window voids and a full floor/roof, not a reused vehicle cabin.
G['WholeOpenWindowSideCab']=solid_union([((.05,-.91,3.18),(.64,-.28,3.29)),((.05,-.91,3.79),(.64,-.28,3.88)),((.05,-.91,3.28),(.64,-.28,3.45)),((.05,-.91,3.45),(.12,-.84,3.80)),((.57,-.91,3.45),(.64,-.84,3.80)),((.05,-.35,3.45),(.12,-.28,3.80)),((.57,-.35,3.45),(.64,-.28,3.80))],3,'One whole compact side operator-cab exterior with genuine window openings, opaque full floor and roof. No occupant, glazing, access or visibility guarantee.')
# Above list lower cabin body is solid exterior, not claimed occupiable volume; window zone is genuinely empty.
G['WholeCabSupportCantilever']=block((.08,-.70,3.27),(.40,-.19,3.39),0,'One full side support ledge connecting cab floor to mast platform.');join('WholeCabSupportCantilever','WholeTowerUpperPlatform',(.2,-.30,3.33));join('WholeOpenWindowSideCab','WholeCabSupportCantilever',(.2,-.6,3.28))
G['WholeFixedUnderJibTrolley']=solid_union([((2.46,-.30,3.60),(2.78,-.20,3.77)),((2.46,.20,3.60),(2.78,.30,3.77)),((2.46,-.20,3.60),(2.78,.20,3.66))],1,'One whole fixed open-top trolley cradle around the main jib lower edge, not a validated running assembly.');join('WholeFixedUnderJibTrolley','NearWholeMainJibLatticeSide',(2.48,-.225,3.75))
cyl('WholeFixedVerticalHookSuspension',(2.62,0,1.77),(2.62,0,3.64),.014,1,'One complete vertical fixed suspension segment; no reeving, rope physics or lifting performance.',12);join('WholeFixedVerticalHookSuspension','WholeFixedUnderJibTrolley',(2.62,0,3.62))
G['WholeLowerHookBlock']=block((2.53,-.085,1.60),(2.71,.085,1.84),2,'One whole lower hook-block exterior at a fixed empty height.');join('WholeLowerHookBlock','WholeFixedVerticalHookSuspension',(2.62,0,1.80))
angles=[math.radians(118+255*i/18)for i in range(19)];poly=[(2.69+.145*math.cos(a),1.53+.145*math.sin(a))for a in angles]+[(2.69+.080*math.cos(a),1.53+.080*math.sin(a))for a in reversed(angles)]
G['WholeOpenEmptyHook']=extrude(poly,-.043,.043,'y',1,'One complete thick open empty hook; no latch, cargo, load rating or lifting suitability.');join('WholeOpenEmptyHook','WholeLowerHookBlock',(2.63,0,1.63))
AIR_POINTS=[(0,-.32,.57),(0,.32,1.35),(-.32,0,2.13),(.32,0,2.91),(.591,-.12,3.97),(1.293,.12,3.97),(-.7,0,3.77),(.3,-.875,3.60),(2.69,0,1.53),(0,0,4.2)]
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='construction-fixed-lattice-mast-and-balanced-truss-tower-crane-01';VERSION='1.0.0';TITLE='Fixed Lattice Mast and Balanced Truss Tower Crane'
DESCRIPTION='One newly authored whole fixed tower-crane illustration. Four complete corner posts and four continuous open diamond-web faces form a three-dimensional mast on a broad full ground foot. An upper platform and fixed broad slewing-style drum carry a separate head, one long triangular-section three-web main jib and an opposite shorter open counter-jib with one whole counterweight exterior. A complete open A-pylon and two fixed ties link the unequal arms; one separately supported window-open side cab and a fixed under-jib trolley, continuous suspension and complete empty open hook finish the whole. No old column I-beam, tripod, timber walking drum, cabin or hook mesh is extracted or rearranged. Main-jib triangular section, two unequal arms and open four-sided lattice tower are real geometry, not a scaled old single-column cantilever. Four opaque constant PBR materials, metres, native Z up, actual whole horizontal bounds-centred grounded origin. One prop zero scenes. A stylized reduced-proportion static construction-machine exterior only. No motor, winch internals, reeving, rotation, trolley travel, lifting, cable tension, load balance, operator access, assembly, construction procedure, foundation design, manufacture or engineering/safety performance. Cab lower body is opaque exterior, not an occupiable interior; upper window voids are real, no glass or person. Rigging, animation and interaction are not made.'
PALETTE=[('WholeMastJibsAndPylon_Ochre',(.61,.36,.09,1),.66,.20),('WholeDrumTrolleyAndSuspension_DarkSteel',(.075,.095,.11,1),.58,.56),('WholeFootAndCounterweight_Concrete',(.40,.43,.42,1),.88,.01),('WholeWindowCab_SlateBlue',(.12,.29,.36,1),.64,.20)]
FOCUS=(0,0,2.45);ORTHO=6.70
CAMERAS={'thumbnail':(8,-13,7.5),'qa-front':(8,-13,7.5),'qa-side':(8,-2,5),'qa-top':(0,0,10),'qa-back':(-8,12,7),'qa-wireframe':(8,-13,7.5)}
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
root=bpy.data.objects.new('OneWholeFixedLatticeBalancedTowerCrane',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole broad tower foot at datum; horizontally centred; one complete fixed tower crane';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==1780 and len(parts)==26
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
  files[role]={'path':f'assets/construction/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'construction','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
