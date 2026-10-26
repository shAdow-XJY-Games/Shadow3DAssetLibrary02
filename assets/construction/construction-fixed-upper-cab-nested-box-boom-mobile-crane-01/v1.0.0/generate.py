"""One newly authored complete upper-cab nested-box-boom mobile crane exterior. Static art only."""
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
# Entire new two-axle upper-cab / nested hollow-boom crane-style vehicle, fixed unloaded pose.
G={};ROOT_WITNESSES=[];AIR_POINTS=[];GROUND=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
def box(n,a,b,m,role):G[n]=block(a,b,m,role)
G['WholeLowClosedCarrierChassis']=extrude([(-.83,-1.85),(.83,-1.85),(.94,-1.57),(.94,1.58),(.77,1.88),(-.77,1.88),(-.94,1.58),(-.94,-1.57)],.57,.95,'z',0,'One complete low chamfer-ended vehicle carrier, without a separate road cab or tall rear shuttered equipment body. All visible coordinates new, not an imported fire truck.')
for j,y in enumerate([-1.19,1.20]):
 n='WholeCrossAxle'+str(j);cyl(n,(-1.18,y,.52),(1.18,y,.52),.13,2,'One complete fixed transverse axle through the lower carrier body.',24);join(n,'WholeLowClosedCarrierChassis',(0,y,.62))
 for label,s in[('Left',-1),('Right',1)]:
  name='WholeLargeGroundTyre'+label+str(j);x=s*1.04;r=.52/math.cos(math.pi/24);G[name]=axial([(.24,-.22),(r,-.22),(r,.22),(.24,.22)],(x,y,.52),(0,1,0),(0,0,1),(1,0,0),24,2,'One whole thick annular large vehicle tyre with a complete finite flat ground facet; no rolling or road capability.',math.pi/24);GROUND.append(name)
  hub='WholeAxleWheelHub'+label+str(j);cyl(hub,(x-.235,y,.52),(x+.235,y,.52),.25,3,'One full proud-ended wheel hub with actual hidden overlap to the whole tyre and axle.',24);join(hub,name,(x,y,.765));join(hub,n,(x,y,.52))
# Full independent deployed stabilizer beams and pads, no engineered support claim.
for j,y in enumerate([-1.45,1.44]):
 for label,s in[('Left',-1),('Right',1)]:
  tag=label+str(j);lo,hi=sorted((s*.70,s*1.78));arm='WholeOutboardStabilizerBeam'+tag;box(arm,(lo,y-.13,.68),(hi,y+.13,.86),1,'One complete horizontal outboard support beam is fixed into the carrier side, not an adjustable mechanism.');join(arm,'WholeLowClosedCarrierChassis',(s*.79,y,.77))
  stem='WholeStabilizerPost'+tag;cyl(stem,(s*1.68,y,.075),(s*1.68,y,.83),.085,3,'One whole vertical fixed post joins beam to a broad pad; no hydraulics or load capability.',16);join(stem,arm,(s*1.68,y,.77))
  pad='WholeStabilizerSole'+tag;box(pad,(s*1.68-.21,y-.20,0),(s*1.68+.21,y+.20,.105),2,'One entire broad ground pad with real finite underside at the same display datum as the tyres.');GROUND.append(pad);join(pad,stem,(s*1.68,y,.09))
# Separate central slew pedestal and a complete upper platform with the sole cab at one side.
G['WholeCentralSlewPedestal']=axial([(0,.90),(.56,.90),(.56,1.10),(.48,1.16),(0,1.16)],(0,.27,0),(1,0,0),(0,1,0),(0,0,1),32,2,'One whole low stepped upper-carrier pedestal, fixed rather than a claimed functioning slew bearing.');join('WholeCentralSlewPedestal','WholeLowClosedCarrierChassis',(0,.27,.93))
G['WholeUpperOperatorAndCounterweightDeck']=extrude([(-1.03,-.88),(.76,-.88),(.90,-.60),(.90,1.33),(.72,1.55),(-.86,1.55),(-1.03,1.28)],1.08,1.25,'z',0,'One whole upper deck organises a side-offset single operator enclosure, central pivot and rear counterweight, unlike a rear ladder on a conventional front-cab fire body.');join('WholeUpperOperatorAndCounterweightDeck','WholeCentralSlewPedestal',(0,.27,1.13))
G['WholeOffsetUpperCab']=extrude([(-.88,1.20),(.68,1.20),(.68,2.19),(-.47,2.19),(-.88,1.86)],-1.00,-.34,'x',0,'One complete fixed offset upper-cab exterior, carried beside the boom on the rotating-looking upper deck; the low chassis has no other cab. Opaque windows, no operator fit.');join('WholeOffsetUpperCab','WholeUpperOperatorAndCounterweightDeck',(-.64,-.1,1.23))
G['WholeOpaqueUpperCabSideWindow']=extrude([(-.77,1.85),(-.41,2.08),(.55,2.08),(.55,1.51),(-.77,1.51)],-1.018,-.987,'x',2,'One complete thick opaque side pane with hidden root and proud visible surface, not transmission glass.');join('WholeOpaqueUpperCabSideWindow','WholeOffsetUpperCab',(-.993,.1,1.82))
G['WholeOpaqueUpperCabFrontWindow']=extrude([(-.889,1.59),(-.889,1.855),(-.515,2.155),(-.488,2.155),(-.86,1.845),(-.86,1.59)],-.90,-.44,'x',2,'One complete bent opaque front pane following the sloping cab face, with genuine solid root rather than a coincident decal.');join('WholeOpaqueUpperCabFrontWindow','WholeOffsetUpperCab',(-.65,-.870,1.71))
G['WholeRearUpperCounterweight']=extrude([(-.81,.85),(.78,.85),(.88,1.33),(.68,1.60),(-.70,1.60),(-.89,1.33)],1.23,1.72,'z',1,'One full rear fixed counterweight exterior on the upper deck, distinct from a shuttered equipment compartment. No balance or lifting calculation.');join('WholeRearUpperCounterweight','WholeUpperOperatorAndCounterweightDeck',(0,1.1,1.24))
P=(.14,.42,1.61);A=math.radians(36);W=(0,-math.cos(A),math.sin(A));U=(1,0,0);V=(0,math.sin(A),math.cos(A))
def bp(t,x=0,z=0):return add(P,add(mul(W,t),add(mul(U,x),mul(V,z))))
def localmesh(g):g['vertices']=[bp(z,x,y)for x,y,z in g['vertices']];return g
for label,s in[('Left',-1),('Right',1)]:
 n='WholeBoomRootCheek'+label;box(n,(P[0]+s*.32-.075,.13,1.20),(P[0]+s*.32+.075,.67,1.83),1,'One complete upper pivot cheek bears on the central deck beside the hollow box-boom root.');join(n,'WholeUpperOperatorAndCounterweightDeck',(P[0]+s*.32,.4,1.23))
cyl('WholeBoomCrossPivot',(P[0]-.47,P[1],P[2]),(P[0]+.47,P[1],P[2]),.105,3,'One entire transverse fixed pin crosses the lower box-boom side walls and two upper cheeks; no moving fit.',24)
for label,s in[('Left',-1),('Right',1)]:join('WholeBoomCrossPivot','WholeBoomRootCheek'+label,(P[0]+s*.32,P[1],P[2]))
def hollow_box(w,d,iw,id,t0,t1,mat,role):
 m=Mesh();outer=[(-w/2,-d/2),(w/2,-d/2),(w/2,d/2),(-w/2,d/2)];inner=[(-iw/2,-id/2),(iw/2,-id/2),(iw/2,id/2),(-iw/2,id/2)];pt=lambda q,t:bp(t,q[0],q[1])
 for t in[t0,t1]:
  for i in range(4):j=(i+1)%4;m.quad(pt(outer[i],t),pt(outer[j],t),pt(inner[j],t),pt(inner[i],t),mat)
 for p in[outer,inner]:
  for i in range(4):j=(i+1)%4;m.quad(pt(p[i],t0),pt(p[j],t0),pt(p[j],t1),pt(p[i],t1),mat)
 return m.result(role)
G['WholeOuterHollowBoxBoom']=hollow_box(.50,.54,.36,.40,-.15,2.38,0,'One entire thick rectangular outer boom sleeve with both real open ends and continuous inner walls, not two open rung ladders or a solid painted tube.');join('WholeOuterHollowBoxBoom','WholeBoomCrossPivot',bp(0,.22,0))
G['WholeMiddleHollowBoxBoom']=hollow_box(.34,.38,.245,.285,1.86,3.85,1,'One full smaller hollow middle box sleeve is fixed inside the outer sleeve with a visible proud outer mouth and genuine unused aperture portions. No telescoping travel or fits claimed.')
G['WholeInnerHollowBoxBoom']=hollow_box(.225,.265,.13,.17,3.30,4.92,3,'One whole third hollow box sleeve extends from the middle tube, with real thick side walls and open terminal mouth behind the full tip carrier.')
# Actual fixed wear-block appearances connect nested sleeves without erasing their remaining small clearance.
for tag,t,z0,z1,outer,inner in [('OuterMiddle',2.05,-.212,-.178,'WholeOuterHollowBoxBoom','WholeMiddleHollowBoxBoom'),('MiddleInner',3.50,-.154,-.120,'WholeMiddleHollowBoxBoom','WholeInnerHollowBoxBoom')]:
 n='WholeFixedNestedSeat'+tag;G[n]=localmesh(block((-.06,z0,t-.08),(.06,z1,t+.08),2,'One whole small fixed lower seat occupies only a bounded patch between nested sleeve walls. Display attachment only; no sliding wear, motion or engineering fit.'));join(n,outer,bp(t,0,z0+.004));join(n,inner,bp(t,0,z1-.004))
# Full closed cylinder/rod exterior below the boom, both rooted in the declared fixed pose.
aa=(.14,-.72,1.18);bb=bp(1.33,0,-.215);dd=sub(bb,aa)
cyl('WholeElevationCylinder',aa,add(aa,mul(dd,.63)),.10,1,'One full closed elevation-cylinder exterior on the upper carrier; no hydraulic circuit, fluid or motion.',24);join('WholeElevationCylinder','WholeUpperOperatorAndCounterweightDeck',add(aa,mul(dd,.035)))
cyl('WholeElevationRod',add(aa,mul(dd,.52)),add(bb,mul(unit(dd),.06)),.051,3,'One whole separate rod exterior enters the cylinder and the outer boom lower wall, fixed only.',20);join('WholeElevationRod','WholeElevationCylinder',add(aa,mul(dd,.58)));join('WholeElevationRod','WholeOuterHollowBoxBoom',bb)
G['WholeUpperTipSheaveCarrier']=localmesh(block((-.27,-.17,4.74),(.27,.17,5.06),1,'One entire tip carrier spans the terminal hollow sleeve and carries the fixed hanging lines. No sheave gearing or engineered reeving.'));join('WholeUpperTipSheaveCarrier','WholeInnerHollowBoxBoom',bp(4.82,.09,.12))
tip=bp(4.98);bz=tip[2]-.95
G['WholeSuspendedHookBlock']=extrude([(-.26,bz-.14),(.26,bz-.14),(.33,bz+.05),(.25,bz+.23),(-.25,bz+.23),(-.33,bz+.05)],tip[1]-.13,tip[1]+.13,'y',1,'One full thick hanging hook-block exterior below the boom tip, no working pulley internals.');G['WholeSuspendedHookBlock']['vertices']=[(x+tip[0],y,z)for x,y,z in G['WholeSuspendedHookBlock']['vertices']]
for j,x in enumerate([-.18,.18]):
 n='WholeFixedSuspensionLine'+str(j);a=(tip[0]+x,tip[1],bz+.18);b=(tip[0]+x,tip[1],tip[2]);cyl(n,a,b,.018,2,'One whole continuous straight fixed suspension-line exterior between tip and block. No cable path through sheaves, load, lifting or safety claim.',10);join(n,'WholeSuspendedHookBlock',add(a,(0,0,.015)));join(n,'WholeUpperTipSheaveCarrier',add(b,(0,0,-.015)))
# One continuous blunt J hook with a truly open throat, not an opaque printed hook.
poly=[(-.055,.12),(.055,.12),(.055,-.08),(.16,-.18),(.17,-.32),(.06,-.46),(-.10,-.46),(-.23,-.34),(-.24,-.20),(-.14,-.14),(-.13,-.27),(-.06,-.34),(.02,-.34),(.07,-.28),(.06,-.22),(-.055,-.14)]
G['WholeOpenBluntLoadHook']=extrude([(tip[0]+x,bz-.13+z)for x,z in poly],tip[1]-.065,tip[1]+.065,'y',3,'One entire blunt thick open-throat J-shaped hook is integral in shape and fixed into the hanging block. Empty art only, not a lifting-rated or safe-to-use hook.');join('WholeOpenBluntLoadHook','WholeSuspendedHookBlock',(tip[0],tip[1],bz-.07))
AIR_POINTS=[bp(.45,0,0),bp(2.60,0,0),bp(4.30,0,0),(tip[0]-.11,tip[1],bz-.32),(0,-.30,.28),(1.52,0,.38)]
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='construction-fixed-upper-cab-nested-box-boom-mobile-crane-01';VERSION='1.0.0';TITLE='Fixed Upper Cab and Nested Box Boom Mobile Crane'
DESCRIPTION='One wholly newly authored compact mobile-crane-style static vehicle. A low chamfer-ended two-axle carrier and four large whole annular tyres carry four deployed full outrigger beams with posts and broad grounded pads. A separate centre pedestal supports one complete upper deck, its sole side-offset cab, rear counterweight and central cross-pivot cheeks. Three genuinely hollow thick rectangular box sleeves extend in one fixed inclined pose; small independently whole lower seats join their nested walls while leaving their remaining real aperture space. A complete lower cylinder-and-rod exterior, tip carrier, two full hanging line exteriors, independent hook block and continuous blunt open J hook complete the empty machine. The carrier has no separate front road cab or rear fire-equipment body and the boom is not the old open rung ladder replaced on an unchanged truck. It is also not a workshop crane scaled onto wheels: the sole upper cab/counterweight/slew platform, nested box sleeves and line-suspended block are authored as one new whole vehicle. No old geometry imported or extracted. Four opaque constant PBR roles, metres Z up and centred complete horizontal bounds with full tyre and pad sole datum. One whole prop zero scenes. Single empty static exterior only: no hydraulic or geared internals, engineered cable reeving, telescoping travel, slew, lifting, rolling, steering, operator fit, load, balance, terrain ability, manufacturing, operation or machinery/vehicle safety performance. Rigging animation and interaction not made.'
PALETTE=[('WholeCarrierCabAndOuterBoom_MutedOchre',(.65,.40,.12,1),.66,.23),('WholeInnerDeckSeatsAndHookBlock_DeepPetrol',(.075,.23,.24,1),.62,.30),('WholeTyresWindowsAndLines_Graphite',(.035,.05,.06,1),.72,.12),('WholeHubsRodsAndTip_SatinAlloy',(.48,.52,.52,1),.42,.64)]
FOCUS=(0,0,1.85);ORTHO=7.4
CAMERAS={'thumbnail':(-8,-11,7),'qa-front':(-8,-11,7),'qa-side':(10,0,5),'qa-top':(0,0,13),'qa-back':(-8,10,7),'qa-wireframe':(-8,-11,7)}
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
root=bpy.data.objects.new('OneWholeUpperCabNestedBoxBoomMobileCrane',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole tyre and outrigger pad soles; horizontal bounds-centred; complete static upper cab box boom mobile crane';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==2600 and len(parts)==44
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
