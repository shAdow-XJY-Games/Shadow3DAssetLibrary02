"""One newly authored whole contraction, observation-channel and rear-fan tunnel display. Static art only."""
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
# Whole newly drawn longitudinal observation-tunnel display, no operational flow model.
ROOT_WITNESSES=[];AIR_POINTS=[];GROUND=['WholeConnectedLowStand']
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
def rectduct(rows,mat,role):
 m=Mesh();out=[];inn=[]
 for x,wy,hz,wi,hi in rows:
  out.append([(x,sy*wy,1.25+sz*hz)for sy,sz in[(-1,-1),(1,-1),(1,1),(-1,1)]])
  inn.append([(x,sy*wi,1.25+sz*hi)for sy,sz in[(-1,-1),(1,-1),(1,1),(-1,1)]])
 for loops in[out,inn]:
  for a,b in zip(loops,loops[1:]):
   for j in range(4):k=(j+1)%4;m.quad(a[j],a[k],b[k],b[j],mat)
 for a,b in[(out[0],inn[0]),(out[-1],inn[-1])]:
  for j in range(4):k=(j+1)%4;m.quad(a[j],a[k],b[k],b[j],mat)
 return m.result(role)
def roundtransition(rows,mat,role):
 m=Mesh();out=[];inn=[];N=32
 for x,ro,ri,square in rows:
  def loop(r):
   q=[]
   for j in range(N):
    a=math.tau*j/N;c=math.cos(a);s=math.sin(a);scale=r/max(abs(c),abs(s))if square else r;q.append((x,scale*c,1.25+scale*s))
   return q
  out.append(loop(ro));inn.append(loop(ri))
 for loops in[out,inn]:
  for a,b in zip(loops,loops[1:]):
   for j in range(N):k=(j+1)%N;m.quad(a[j],a[k],b[k],b[j],mat)
 for a,b in[(out[0],inn[0]),(out[-1],inn[-1])]:
  for j in range(N):k=(j+1)%N;m.quad(a[j],a[k],b[k],b[j],mat)
 return m.result(role)
# One connected low apparatus frame, not a separately counted table or scene.
boxes=[((-2.15,-.66,0),(2.13,-.50,.10)),((-2.15,.50,0),(2.13,.66,.10)),((-1.74,-.58,.035),(-1.57,.58,.17)),((1.54,-.58,.035),(1.71,.58,.17)),((-2.06,-.46,.72),(2.03,-.34,.79)),((-2.06,.34,.72),(2.03,.46,.79))]
for x in[-1.66,1.63]:
 for y in[-.40,.40]:boxes.append(((x-.065,y-.065,.08),(x+.065,y+.065,.77)))
 boxes.append(((x-.10,-.44,.71),(x+.10,.44,.80)))
G['WholeConnectedLowStand']=solid_union(boxes,1,'One complete connected low apparatus stand: two long finite ground rails, two crossfeet, four posts and full longitudinal bearing rails. No table imported, no structural capacity statement.')
G['WholeBroadInletSettlingBox']=rectduct([(-2.0,.53,.49,.48,.44),(-1.22,.53,.49,.48,.44)],0,'One entire thick-walled broad rectangular inlet box, true empty interior and two actual open ends. No opaque panel substituted for its internal cavity.')
join('WholeBroadInletSettlingBox','WholeConnectedLowStand',(-1.66,.40,.78))
G['WholeInletLip']=rectduct([(-2.035,.555,.515,.478,.438),(-1.985,.555,.515,.478,.438)],2,'One complete slightly proud inlet rim with a genuine aperture, covering the wall junction without a duplicate exposed face.')
join('WholeInletLip','WholeBroadInletSettlingBox',(-1.995,0,.785))
# A coarse fixed grille is only a visible inlet feature, not a flow conditioner specification.
for j,y in enumerate([-.30,-.10,.10,.30]):
 n='WholeInletVerticalBar'+str(j);G[n]=block((-1.93,y-.008,.795),(-1.905,y+.008,1.705),2,'One complete thin blunt fixed inlet grille bar, both ends embedded in the full box walls. No working screen or airflow performance.')
 join(n,'WholeBroadInletSettlingBox',(-1.918,y,.802))
G['WholeSmoothContraction']=rectduct([(-1.25,.52,.48,.47,.43),(-1.07,.495,.455,.445,.405),(-.76,.395,.375,.35,.33),(-.36,.283,.283,.243,.243)],0,'One continuous thick hollow contraction from the wide inlet to the narrow observation channel. The whole outer and inner surfaces change section together; no inserted closed cone.')
join('WholeSmoothContraction','WholeBroadInletSettlingBox',(-1.235,0,.782))
# Full C section: deliberately removed near-side viewing wall, not glass or a sealed working test cell.
obs=[(-.288,.962),(.288,.962),(.288,1.538),(-.288,1.538),(-.288,1.498),(.248,1.498),(.248,1.002),(-.288,1.002)]
G['WholeOpenSideObservationChannel']=extrude(obs,-.39,.57,'x',0,'One whole thick connected floor/back/roof observation-channel shell with a genuinely open near-side wall. It is an intentional static cutaway, not a transparent material or sealed test enclosure.')
for label,x in[('Inlet',-.375),('Outlet',.55)]:
 n='WholeObservation'+label+'Rim';G[n]=rectduct([(x-.035,.315,.315,.242,.242),(x+.035,.315,.315,.242,.242)],1,'One full narrow observation end-frame with real rectangular aperture, proud of adjoining wall planes and embedded at the section junction.')
 join(n,'WholeOpenSideObservationChannel',(x,0,.982))
 if label=='Inlet':join(n,'WholeSmoothContraction',(-.37,0,.983))
 # A separate complete raised saddle joins the thin observation floor to the low stand.
 n2='WholeObservation'+label+'Saddle';G[n2]=solid_union([((x-.06,-.43,.75),(x+.06,.43,.84)),((x-.06,-.22,.79),(x+.06,.22,.98))],1,'One complete raised observation saddle from both full stand stringers to the shell floor; static fixed connection.')
 join(n2,'WholeConnectedLowStand',(x,.39,.77));join(n2,'WholeOpenSideObservationChannel',(x,0,.972))
G['WholeLongExpandingDiffuser']=rectduct([(.54,.283,.283,.243,.243),(.92,.34,.34,.30,.30),(1.35,.43,.43,.38,.38)],0,'One complete long hollow widening section after the observation channel, with true continuous inner floor and walls. No flow prediction or diffuser efficiency claim.')
join('WholeLongExpandingDiffuser','WholeObservationOutletRim',(.56,0,.983))
G['WholeSquareToRoundTail']=roundtransition([(1.32,.422,.375,True),(1.365,.422,.375,True),(1.62,.46,.405,False)],0,'One entire thick transition from a square diffuser mouth to a circular fan enclosure, including the full changing internal bore. Not two disconnected ducts intersecting at their edges.')
join('WholeSquareToRoundTail','WholeLongExpandingDiffuser',(1.335,0,.833))
G['WholeOpenFanCasing']=axial([(.402,1.59),(.464,1.59),(.464,2.04),(.402,2.04)],(0,0,1.25),(0,1,0),(0,0,1),(1,0,0),48,0,'One complete annular rear fan casing with two real open mouths and constant thick wall; inner rotor remains visible at the rear. No fan operation or guarding claim.')
join('WholeOpenFanCasing','WholeSquareToRoundTail',(1.605,0,.815))
G['WholeRearFanLip']=axial([(.398,2.005),(.485,2.005),(.485,2.065),(.398,2.065)],(0,0,1.25),(0,1,0),(0,0,1),(1,0,0),48,1,'One entire slightly proud circular rear lip embedded across the casing end, avoiding identical exposed annular caps.')
join('WholeRearFanLip','WholeOpenFanCasing',(2.025,0,.805))
G['WholeRearCasingSaddle']=block((1.63,-.24,.76),(1.87,.24,.84),1,'One full low rear saddle under the fan-casing lower arc, with broad embedded support to the stand cross-seat.')
join('WholeRearCasingSaddle','WholeConnectedLowStand',(1.65,0,.785));join('WholeRearCasingSaddle','WholeOpenFanCasing',(1.75,0,.81))
# A single connected stationary spider is behind the separate complete rotor.
spider=[]
for y in[-.205,.205]:spider.append(((1.735,y-.205,1.235),(1.77,y+.205,1.265)))
spider.append(((1.735,-.015,.84),(1.77,.015,1.66)))
G['WholeStationaryFanSpider']=solid_union(spider,2,'One whole crossed rear bearing spider, its four arm ends rooted into the real cylindrical wall. Separate from the static four-blade rotor; no drive model.')
join('WholeStationaryFanSpider','WholeOpenFanCasing',(1.75,0,.845))
cyl('WholeFanCentralShaft',(1.72,0,1.25),(2.005,0,1.25),.045,2,'One complete fixed rotor shaft crossing the full stationary bearing spider.',24)
join('WholeFanCentralShaft','WholeStationaryFanSpider',(1.75,0,1.25))
# Rotor is one connected hub-and-four-blade mesh through a grid union, deliberately blunt and fixed.
rotor=Mesh()
# Full blades are separate whole meshes seated into a solid complete hub; no coplanar outer hub cap.
cyl('WholeFanHub',(1.80,0,1.25),(1.975,0,1.25),.10,3,'One complete broad static hub on the fixed shaft, left proud of its blades and not a working bearing.',32)
join('WholeFanHub','WholeFanCentralShaft',(1.88,0,1.25))
for j in range(4):
 a=j*math.tau/4+.22;c=math.cos(a);s=math.sin(a)
 poly=[(.065,-.035),(.28,-.095),(.355,-.045),(.34,.035),(.12,.055)]
 yz=[(r*c-t*s,1.25+r*s+t*c)for r,t in poly]
 n='WholeFixedFanBlade'+str(j);G[n]=extrude(yz,1.855,1.925,'x',2,'One complete blunt thick slightly swept fan-blade exterior, independently authored and embedded at its root into the full hub. Fixed nonfunctional pose; no aerodynamic geometry or running clearance.')
 join(n,'WholeFanHub',(1.89,.083*c+.025*s,1.25+.083*s-.025*c))
# Simple fixed opaque specimen reinforces the open viewing region without a promised test object.
cyl('WholeObservationSpecimenStem',(.06,0,.982),(.06,0,1.255),.017,2,'One entire short specimen-support stem rooted into the observation floor, fixed in this empty cutaway display.',16)
join('WholeObservationSpecimenStem','WholeOpenSideObservationChannel',(.06,0,.99))
G['WholeBluntObservationSpecimen']=extrude([(-.12,1.24),(-.08,1.285),(.14,1.265),(.23,1.24),(.10,1.225),(-.08,1.215)],-.18,.18,'y',3,'One complete blunt opaque wedge-like display specimen spanning the observation channel. Generic static insert only, not a tested airfoil or measurement model.')
join('WholeBluntObservationSpecimen','WholeObservationSpecimenStem',(.06,0,1.24))
AIR_POINTS=[(-1.70,0,1.25),(-.82,0,1.25),(.05,-.22,1.36),(.9,0,1.25),(1.50,0,1.25),(2.035,.20,1.45)]
vv=[v for g in G.values()for v in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='technology-fixed-contraction-window-and-fan-wind-tunnel-01';VERSION='1.0.0';TITLE='Fixed Contraction, Observation Window and Fan Tunnel'
DESCRIPTION='One independently authored complete open-circuit wind-tunnel-style static cutaway display on a connected low four-post stand. A broad empty inlet box with a thin coarse grille narrows through a fully hollow changing-section contraction into a distinct floor/back/roof observation channel whose near-side wall is intentionally open. Full proud end frames and raised saddles hold this channel and a short fixed specimen stem with one opaque blunt wedge. A long hollow expanding diffuser leads into a whole square-to-round transition, annular rear fan enclosure and open circular lip; a separate crossed stationary spider, full shaft/hub and four thick swept blades complete the fixed visible rotor. All outer and inner duct walls, section changes, openings, stand and rotor are newly drawn together. No existing hood, collector, blower, duct or furniture mesh is copied, extracted or resized. Unlike the old sash fume hood, this is not one front-open work cabinet with a roof exhaust; unlike the old dust collector it is not a tall filter/bag beside a transverse blower. One prop, zero scenes; four opaque constant PBR materials, metres, Z up, centred horizontal bounds, full base-rail ground soles. This is solely generic low-poly art, not an operational apparatus or engineering drawing. No airflow, aerodynamic test, pressure, flow conditioning, measurement, fan rotation, specimen performance, guarding, structural rating, capacity, manufacture, operation or safety claim. Rigging, animation and interaction are not made or verified.'
PALETTE=[('WholeDuctShells_WarmIvory',(.66,.68,.62,1),.67,.12),('WholeStandAndMouthFrames_MutedBlue',(.08,.22,.28,1),.68,.28),('WholeGrilleRotorAndStem_DarkSteel',(.075,.09,.10,1),.48,.50),('WholeSpecimenAndHub_Ochre',(.58,.32,.10,1),.54,.30)]
FOCUS=(0,0,.96);ORTHO=5.15
CAMERAS={'thumbnail':(5.8,-8.8,4.1),'qa-front':(5.8,-8.8,4.1),'qa-side':(0,-8,3),'qa-top':(0,0,8),'qa-back':(-5.8,8.8,4.1),'qa-wireframe':(5.8,-8.8,4.1)}
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
root=bpy.data.objects.new('OneWholeContractionObservationAndFanTunnel',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole connected base rail soles at datum; horizontally centred; one complete static observation tunnel';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();
 for m in mats:me.materials.append(m)
 for i,f in enumerate(me.polygons):f.material_index=g.get('face_materials',[g['material']]*len(me.polygons))[i]
 o['component_role']=g['role'];parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=(name=='WholeSquareToRoundTail')
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={};actual_triangles={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg);triangles+=len(o.data.loop_triangles)
 component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i]for p in v)for i in range(3)];hi=[max(p[i]for p in v)for i in range(3)];bounds=[round(hi[i]-lo[i],6)for i in range(3)]
assert abs(lo[2])<1e-7 and triangles==3960 and len(parts)==27
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
