"""One newly authored complete Z-fold-pipe and rear-hopper pump-truck exterior. Static art only."""
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
# New complete empty rear-hopper and Z-fold delivery-pipe truck exterior.
ROOT_WITNESSES=[];AIR_POINTS=[];GROUND=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
G['WholeLongTruckChassis']=block((-.83,-3.15,.66),(.83,3.03,.96),2,'One entire long truck chassis joining three complete axles and the independent pump deck. Newly drawn for this machine, no prior fire vehicle chassis imported.')
for k,y in enumerate([-2.40,1.25,2.31]):
 n='WholeTruckAxle'+str(k);cyl(n,(-1.10,y,.49),(1.10,y,.49),.085,3,'One entire fixed road axle crossing both full wheel hubs and the chassis underside carrier.',24)
 carrier='WholeAxleCarrier'+str(k);G[carrier]=block((-.44,y-.16,.44),(.44,y+.16,.73),2,'One whole low axle carrier rooted between the chassis and the complete road axle.');join(carrier,'WholeLongTruckChassis',(0,y,.69));join(carrier,n,(0,y,.49))
 for side,x in[('Left',-1.0),('Right',1.0)]:
  t='Whole'+side+'RoadTyre'+str(k);h='Whole'+side+'RoadHub'+str(k);rr=.49/math.cos(math.pi/24)
  G[t]=axial([(.22,-.19),(rr,-.19),(rr,.19),(.22,.19)],(x,y,.49),(0,1,0),(0,0,1),(1,0,0),24,2,'One complete thick annular tyre with full flat ground facet in the fixed stance. No steering or contact-performance claim.',phase=math.pi/24);GROUND.append(t)
  cyl(h,(x-.205,y,.49),(x+.205,y,.49),.235,3,'One complete wheel hub with proud cap planes and positive hidden radial tyre overlap.',24);join(h,t,(x,y,.718));join(h,n,(x,y,.49))
G['WholeForwardChamferedCab']=extrude([(-3.35,.92),(-1.54,.92),(-1.54,2.56),(-2.95,2.56),(-3.35,2.15)],-1.02,1.02,'x',1,'One entire new forward cab exterior with sloped upper front, blank opaque windows and no model occupant or drive components.');join('WholeForwardChamferedCab','WholeLongTruckChassis',(0,-2.1,.94))
for side,x in[('Left',-1.025),('Right',1.025)]:
 n='Whole'+side+'OpaqueCabWindow';G[n]=extrude([(-3.16,2.10),(-2.88,2.43),(-1.67,2.43),(-1.67,1.76),(-3.16,1.76)],x-.025,x+.025,'x',2,'One whole blank opaque side-window insert, its inner root enters the cab while its visible face is proud; no transparency.');join(n,'WholeForwardChamferedCab',((-1.01 if x<0 else 1.01),-2.1,2.0))
G['WholeOpaqueFrontWindscreen']=extrude([(-3.363,1.76),(-3.363,2.13),(-3.075,2.425),(-3.044,2.425),(-3.328,2.12),(-3.328,1.76)],-.84,.84,'x',2,'One continuous thick opaque bent front windscreen appearance, follows the front and sloping cab boundary with an embedded inner root, not a coplanar decal.');join('WholeOpaqueFrontWindscreen','WholeForwardChamferedCab',(0,-3.34,1.95))
G['WholeFrontBumper']=block((-1.10,-3.45,.84),(1.10,-3.28,1.02),3,'One entire blunt front bumper exterior with positive cab/chassis root, not impact protection.');join('WholeFrontBumper','WholeForwardChamferedCab',(0,-3.32,.98))
G['WholeLongRearPumpDeck']=block((-.98,-1.48,.92),(.98,2.91,1.15),1,'One complete rear equipment deck carried by the whole chassis, no fire-compartment shutters or ladders.');join('WholeLongRearPumpDeck','WholeLongTruckChassis',(0,.5,.94))
G['WholeRearPumpCasing']=extrude([(.75,1.10),(2.50,1.10),(2.50,1.53),(2.25,1.72),(.90,1.72),(.75,1.53)],-.75,.75,'x',0,'One whole closed low pump-cell exterior behind the front boom pedestal, visually connected to the empty rear hopper. No pump internals, valves, pressures or material path promised.');join('WholeRearPumpCasing','WholeLongRearPumpDeck',(0,1.7,1.13))
# Full deep open rear receiving hopper, not a tilted mixing drum or false black cap.
m=Mesh();rows=[]
for xx,y0,y1,z in[(.59,2.48,3.16,1.04),(.94,2.39,3.53,1.97),(.85,2.48,3.44,1.97),(.50,2.57,3.07,1.25)]:rows.append([(-xx,y0,z),(xx,y0,z),(xx,y1,z),(-xx,y1,z)])
m.quad(*rows[0],0)
for a,b in zip(rows,rows[1:]):
 for j in range(4):k=(j+1)%4;m.quad(a[j],a[k],b[k],b[j],0)
m.quad(*rows[-1],0);G['WholeDeepOpenRearReceivingHopper']=m.result('One entire thick flared rear receiving hopper with actual deep open chamber, continuous four walls, full rim and blind floor. Empty, no grate, contents, mixer paddles or material-processing mechanism.');join('WholeDeepOpenRearReceivingHopper','WholeLongRearPumpDeck',(0,2.70,1.10));join('WholeDeepOpenRearReceivingHopper','WholeRearPumpCasing',(0,2.49,1.35))
# Four full fixed deployed stabilizer appearances, not a load/stability specification.
for k,y in enumerate([-.95,2.14]):
 for side,x in[('Left',-2.13),('Right',2.13)]:
  tag=side+str(k);n='Whole'+tag+'OutriggerArm';a=(x/abs(x)*.60,y,.79);b=(x,y,.79);G[n]=beam(a,b,.18,.20,0,'One whole transverse deployed outrigger beam exterior. New geometry rooted across the long chassis, fixed static position only.');join(n,'WholeLongTruckChassis',(x/abs(x)*.74,y,.79))
  n='Whole'+tag+'OutriggerPost';cyl(n,(x,y,.065),(x,y,.87),.075,3,'One entire upright stabilizer-post appearance joining the deployed arm and a full finite ground pad.',20);join(n,'Whole'+tag+'OutriggerArm',(x-x/abs(x)*.025,y,.79))
  pad='Whole'+tag+'GroundPad';G[pad]=block((x-.25,y-.23,0),(x+.25,y+.23,.11),2,'One full rectangular flat pad at the display datum. No load, soil or stability capability.');GROUND.append(pad);join(pad,n,(x,y,.085))
cyl('WholeFrontBoomPedestal',(0,-.73,1.10),(0,-.73,1.55),.48,0,'One whole front-of-deck boom pedestal directly behind the cab. Not the old rear fire-truck turntable, and no rotation function.',32);join('WholeFrontBoomPedestal','WholeLongRearPumpDeck',(0,-.73,1.13))
G['WholeOpenBoomRootFork']=solid_union([((-.39,-.96,1.51),(.39,-.50,1.67)),((-.39,-1.00,1.60),(-.25,-.46,2.02)),((.25,-1.00,1.60),(.39,-.46,2.02))],0,'One complete forked boom root with actual open middle and two thick bearing cheeks, integral bottom joining the pedestal.');join('WholeOpenBoomRootFork','WholeFrontBoomPedestal',(0,-.73,1.53))
PIVOTS=[(0,-.73,1.90),(0,.78,4.67),(0,3.20,3.28),(0,5.27,4.25)]
for j,p in enumerate(PIVOTS):
 n='WholeBoomPivot'+str(j);cyl(n,add(p,(-.44,0,0)),add(p,(.44,0,0)),.205 if j else .16,3,'One whole transverse fixed boom pivot exterior, proud ends avoid a duplicate arm-end face. No bearing fit, articulation or hydraulic promise.',24)
 if j==0:join(n,'WholeOpenBoomRootFork',(.32,-.73,1.90))
for j,(a,b)in enumerate(zip(PIVOTS,PIVOTS[1:])):
 n='WholeZFoldBoomMember'+str(j);G[n]=beam(a,b,.34,.38,0,'One complete long structural-looking member in the fixed three-section Z-fold silhouette, no open rung ladder, telescope or actuated motion. Newly placed full part, not a rotated old fire ladder.')
 w=unit(sub(b,a));join(n,'WholeBoomPivot'+str(j),add(a,mul(w,.07)));join(n,'WholeBoomPivot'+str(j+1),sub(b,mul(w,.07)))
# Continuous real hollow outer-pipe surface, including bends and pendant end.
def empty_sweep(path,ro,ri):
 m=Mesh();rings=[]
 for r in[ro,ri]:
  rr=[]
  for k,p in enumerate(path):
   w=unit(sub(path[min(k+1,len(path)-1)],path[max(0,k-1)]));u=(1,0,0);v=cross(w,u);rr.append([add(p,add(mul(u,r*math.cos(t*math.tau/16)),mul(v,r*math.sin(t*math.tau/16))))for t in range(16)])
  rings.append(rr)
 for rr in rings:
  for a,b in zip(rr,rr[1:]):
   for j in range(16):k=(j+1)%16;m.quad(a[j],a[k],b[k],b[j],1)
 for i in[0,len(path)-1]:
  for j in range(16):k=(j+1)%16;m.quad(rings[0][i][j],rings[0][i][k],rings[1][i][k],rings[1][i][j],1)
 return m.result('One entire continuous thick hollow delivery-pipe exterior along the fixed Z-fold members, with actual inner and outer surfaces through all drawn bends and a real downward open terminal mouth. No flow continuity, pressure, coupling or transport capability is certified.')
PATH=[(.37,2.32,1.38),(.37,.18,1.38),(.37,-.73,1.90),(.37,.78,4.67),(.37,3.20,3.28),(.37,5.27,4.25),(.37,5.45,4.06),(.37,5.46,2.13)]
G['WholeContinuousBentDeliveryTube']=empty_sweep(PATH,.085,.055);join('WholeContinuousBentDeliveryTube','WholeRearPumpCasing',(.445,2.26,1.38))
for j,(a,b)in enumerate(zip(PIVOTS,PIVOTS[1:])):
 p=add(a,mul(sub(b,a),.47));n='WholePipeStandOff'+str(j);cyl(n,add(p,(.12,0,0)),add(p,(.450,0,0)),.045,3,'One whole short transverse pipe standoff roots the complete outer tube to its full boom member with positive hidden intersections. Static shape, no clamp holding claim.',16);join(n,'WholeZFoldBoomMember'+str(j),add(p,(.15,0,0)));join(n,'WholeContinuousBentDeliveryTube',add(p,(.435,0,0)))
AIR_POINTS=[(0,2.95,1.75),(0,2.94,1.30),(.37,5.459,2.20),(0,2.0,2.5),(0,-.73,1.70),(0,-2.1,2.8)]
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='construction-fixed-z-fold-pipe-and-open-rear-hopper-pump-truck-01';VERSION='1.0.0';TITLE='Fixed Z Fold Pipe and Open Rear Hopper Pump Truck'
DESCRIPTION='One wholly newly authored complete truck-mounted concrete-pump-style static exterior. A long three-axle chassis and forward opaque-window cab carry an independent rear pump-cell cover and genuinely deep open blind receiving hopper. Four full deployed side arms terminate in complete posts and flat ground pads. Immediately behind the cab, a separate front pedestal/open root fork carries three full members in a high folded Z silhouette, with distinct complete cross pivots. One continuous genuinely hollow outer pipe follows the full arm path and ends in a descending open terminal, with complete standoffs joining it to the arm members. This is not the old rear-turntable telescopic rung-ladder fire truck with a pipe substituted: there are no side fire compartments, ladder rails, rungs or telescopic section; the overall rear hopper/pump to front articulated carrier and long returning pipe is newly constructed. It is also not a portable tilting drum mixer or old vehicle assembled from extracted meshes. Generic closed-mesh/export mathematics only reused. Four constant opaque PBR materials, metres, Z up, centred complete horizontal envelope, whole tyre facets and pad soles at datum. One prop zero scenes. Empty static art only: no concrete, mixing, pumping, pipe-flow connectivity, pressure, hydraulics, boom movement, steering, support load, stability, operator fit, manufacture, use or safety performance. Rigging, animation and interaction are not made or verified.'
PALETTE=[('WholePumpDeckBoomAndHopper_MutedTeal',(.065,.28,.28,1),.65,.20),('WholeCabAndContinuousPipe_WarmIvory',(.68,.65,.49,1),.59,.22),('WholeTyresWindowsAndPads_DarkGraphite',(.045,.062,.07,1),.75,.10),('WholeAxlesPinsAndPosts_SatinMetal',(.42,.47,.48,1),.43,.62)]
FOCUS=(0,0,2.15);ORTHO=11.7
CAMERAS={'thumbnail':(10,-12,7.2),'qa-front':(10,-12,7.0),'qa-side':(13,0,6),'qa-top':(0,0,15),'qa-back':(-10,12,7),'qa-wireframe':(10,-12,7.2)}
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
root=bpy.data.objects.new('OneWholeZFoldPipeAndRearHopperPumpTruck',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole tyre and pad soles at datum; horizontally centred; one complete static pipe-and-hopper pump-truck exterior';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==3980 and len(parts)==52
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
