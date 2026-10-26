"""One newly authored complete double-cradle tank-over-engine motorcycle exterior. Static art only."""
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
# Wholly new complete tank-over-engine double-cradle motorcycle-style exterior.
G={};ROOT_WITNESSES=[];AIR_POINTS=[];GROUND=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
def box(n,lo,hi,m,role):G[n]=block(lo,hi,m,role)
def cyl(n,a,b,r,m,role,N=16):
 w=unit(sub(b,a));ref=(0,0,1)if abs(w[2])<.9 else(0,1,0);u=unit(cross(w,ref));v=cross(w,u);h=math.sqrt(dot(sub(b,a),sub(b,a)))
 G[n]=axial([(0,0),(r,0),(r,h),(0,h)],a,u,v,w,N,m,role)
def path(points,r,m,role,n=10,closed=False):
 mesh=Mesh();rows=[];K=len(points)
 for i,p in enumerate(points):
  w=unit(sub(points[(i+1)%K]if closed else points[min(i+1,K-1)],points[(i-1)%K]if closed else points[max(i-1,0)]));ref=(0,0,1)if abs(w[2])<.90 else(0,1,0);u=unit(cross(w,ref));v=cross(w,u)
  rows.append([add(p,add(mul(u,r*math.cos(j*math.tau/n)),mul(v,r*math.sin(j*math.tau/n))))for j in range(n)])
 for i in range(K if closed else K-1):
  a,b=rows[i],rows[(i+1)%K]
  for j in range(n):k=(j+1)%n;mesh.quad(a[j],a[k],b[k],b[j],m)
 if not closed:
  for j in range(n):k=(j+1)%n;mesh.tri([points[0],rows[0][k],rows[0][j]],m);mesh.tri([points[-1],rows[-1][j],rows[-1][k]],m)
 return mesh.result(role)
def loft(sections,m,role):
 mesh=Mesh();rows=[]
 for y,w,z0,z1 in sections:
  c=min(.035,w*.3,(z1-z0)*.25);rows.append([(-w+c,y,z0),(w-c,y,z0),(w,y,z0+c),(w,y,z1-c),(w-c,y,z1),(-w+c,y,z1),(-w,y,z1-c),(-w,y,z0+c)])
 for a,b in zip(rows,rows[1:]):
  for j in range(8):k=(j+1)%8;mesh.quad(a[j],a[k],b[k],b[j],m)
 for row in[rows[0],rows[-1]]:
  c=tuple(sum(p[k]for p in row)/8 for k in range(3))
  for j in range(8):mesh.tri([c,row[j],row[(j+1)%8]],m)
 return mesh.result(role)
# Two whole annular tires, open rims, integral separate spoke/hub/axle appearances.
for tag,y,width in[('Front',-.92,.13),('Rear',.78,.16)]:
 C=(0,y,.36);n='Whole'+tag+'Tire';ro=.36/math.cos(math.pi/32)
 G[n]=axial([(.273,-width/2),(.335,-width/2),(ro,-width*.30),(ro,width*.30),(.335,width/2),(.273,width/2)],C,(0,1,0),(0,0,1),(1,0,0),32,2,'One complete thick open annular motorcycle tire, with two bevel shoulders and a full true flat tread contact facet. Fixed no rotation or riding claim.',phase=math.pi/32);GROUND.append(n)
 q='Whole'+tag+'OpenRim';G[q]=axial([(.235,-.047),(.280,-.047),(.280,.047),(.235,.047)],C,(0,1,0),(0,0,1),(1,0,0),32,1,'One complete open annular wheel rim; no solid wheel disk substitutes for the open spoke bay.');join(n,q,(0,y,.36+.277))
 hub='Whole'+tag+'Hub';cyl(hub,(-.085,y,.36),(.085,y,.36),.075,1,'One complete fixed central hub separate from the open rim.');ax='Whole'+tag+'Axle';cyl(ax,(-.205,y,.36),(.205,y,.36),.023,1,'One whole transverse fixed axle crossing the complete hub.');join(hub,ax,(0,y,.36))
 for k in range(6):
  a=math.tau*k/6;nn='Whole'+tag+'BroadSpoke'+str(k);p=(0,y+.055*math.cos(a),.36+.055*math.sin(a));e=(0,y+.257*math.cos(a),.36+.257*math.sin(a));cyl(nn,p,e,.015,1,'One whole thick spoke with finite hub and rim roots; six spokes form one complete visible wheel organization, no spoke-count asset variants.',8);join(nn,hub,(0,y+.065*math.cos(a),.36+.065*math.sin(a)));join(nn,q,(0,y+.246*math.cos(a),.36+.246*math.sin(a)))
# Two new closed lower cradle loops, not the old bicycle diamond frame.
for tag,s in[('Left',-1),('Right',1)]:
 n='WholeDoubleCradleLoop'+tag;pts=[(s*.045,-.59,1.02),(s*.15,-.49,.72),(s*.16,-.45,.28),(s*.16,.27,.28),(s*.16,.50,.85),(s*.13,-.10,.98)]
 G[n]=path(pts,.033,0,'One complete continuous closed double-cradle side loop surrounding the whole central engine exterior; the two loops are separately editable but both meet the full steering head and rear frame.',closed=True)
cyl('WholeSteeringHead',(0,-.63,.90),(0,-.575,1.11),.058,0,'One entire inclined steering-head exterior connecting both cradle loops to the fixed twin front fork; no steering articulation.');
for tag,s in[('Left',-1),('Right',1)]:join('WholeDoubleCradleLoop'+tag,'WholeSteeringHead',(s*.04,-.591,1.021))
# Large central crankcase, real layered cylinder silhouette and entire top head.
G['WholeCentralCrankcase']=axial([(0,-.18),(.17,-.18),(.205,-.13),(.205,.13),(.17,.18),(0,.18)],(0,-.02,.46),(0,1,0),(0,0,1),(1,0,0),24,1,'One complete central rounded crankcase exterior occupying the lower cradle, not a pedal crank ring. Solid static shape without internal engine parts.')
for tag,s in[('Left',-1),('Right',1)]:join('WholeCentralCrankcase','WholeDoubleCradleLoop'+tag,(s*.155,.04,.30))
prof=[(0,.59),(.132,.59)]
for z in[.60,.65,.70,.75]:prof.extend([(.14,z),(.169,z+.009),(.169,z+.024),(.14,z+.035)])
prof.extend([(.14,.82),(0,.82)])
G['WholeIntegralFinnedCylinderExterior']=axial(prof,(0,-.12,0),(1,0,0),(0,1,0),(0,0,1),20,1,'One entire integral-rib cylinder exterior rises from the crankcase under a separate full head. Solid appearance only, no combustion, cooling or engine design.');join('WholeIntegralFinnedCylinderExterior','WholeCentralCrankcase',(0,-.12,.62))
G['WholeCylinderHead']=loft([(-.28,.14,.805,.91),(-.23,.19,.805,.94),(.015,.19,.805,.94),(.07,.14,.805,.91)],1,'One complete wide chamfered cylinder-head exterior, finitely rooted into the whole central cylinder.');join('WholeCylinderHead','WholeIntegralFinnedCylinderExterior',(0,-.12,.815))
# Whole upper tank and rear saddle are distinct volumes over the new central cradle.
G['WholeSculptedLongFuelTankExterior']=loft([(-.55,.10,1.00,1.09),(-.43,.20,.97,1.21),(-.05,.22,.955,1.20),(.18,.13,.955,1.08)],0,'One complete longitudinal sculpted tank-like exterior above the central engine, independently shaped to the new double cradle. Closed opaque solid, no fuel storage or filler function.');join('WholeSculptedLongFuelTankExterior','WholeDoubleCradleLoopRight',(.13,-.10,.98))
cyl('WholeTankBlankCap',(0,-.16,1.185),(0,-.16,1.225),.043,1,'One full small capped top detail with buried lower root, no access, fuel or pressure claim.');join('WholeTankBlankCap','WholeSculptedLongFuelTankExterior',(0,-.16,1.19))
for tag,s in[('Left',-1),('Right',1)]:
 n='WholeRearSaddleRail'+tag;G[n]=path([(s*.13,.10,.92),(s*.16,.50,.89),(s*.14,.77,.91)],.028,0,'One entire rear saddle-support rail tied into the upper cradle, without a broad enclosing scooter body.');join(n,'WholeDoubleCradleLoop'+tag,(s*.16,.50,.868))
G['WholeLongTwoLevelSaddle']=loft([(.13,.11,.93,.99),(.35,.16,.89,.99),(.68,.18,.88,1.035),(.82,.14,.89,1.015)],2,'One whole shaped long saddle exterior, front low and rear raised, supported on the full rear rails. No rider, fit, comfort or load claim.');
for tag,s in[('Left',-1),('Right',1)]:join('WholeLongTwoLevelSaddle','WholeRearSaddleRail'+tag,(s*.14,.73,.905))
# Independent fixed rear swing arms and complete outer suspension-looking struts.
for tag,s in[('Left',-1),('Right',1)]:
 n='WholeRearSwingArm'+tag;G[n]=path([(s*.16,.13,.40),(s*.175,.42,.35),(s*.175,.78,.36)],.035,0,'One complete rear swing-arm exterior from the lower engine/frame region to the rear axle, fixed pose not articulated.');join(n,'WholeCentralCrankcase',(s*.1605,.140,.398));join(n,'WholeRearAxle',(s*.175,.770,.36))
 n='WholeRearSuspensionStrut'+tag;a=(s*.175,.745,.37);b=(s*.165,.52,.90);c=add(a,mul(sub(b,a),.58));G[n]=path([a,c,b],.043,1,'One complete thick fixed rear suspension-strut silhouette, with no actual spring or damping claim.');join(n,'WholeRearSwingArm'+tag,(s*.175,.745,.37));join(n,'WholeRearSaddleRail'+tag,(s*.165,.524,.891))
# Full twin fork arms, transverse crowns, steering stem and complete handlebar.
for tag,s in[('Left',-1),('Right',1)]:
 n='WholeFrontForkLeg'+tag;a=(s*.13,-.92,.36);b=(s*.13,-.62,1.04);G[n]=path([a,add(a,mul(sub(b,a),.48)),b],.033,1,'One entire fixed long front fork arm outside the tire, connecting its axle to both transverse crowns.');join(n,'WholeFrontAxle',add(a,mul(sub(b,a),.008)))
for tag,y,z in[('Upper',-.62,1.04),('Lower',-.69,.88)]:
 n='WholeFrontForkCrown'+tag;box(n,(-.16,y-.046,z-.025),(.16,y+.046,z+.025),0,'One full transverse fork crown, with deliberate enclosed fork-arm overlaps and no duplicate end face.')
 if tag=='Upper':join(n,'WholeSteeringHead',(0,y+.018,z))
 for side,s in[('Left',-1),('Right',1)]:join(n,'WholeFrontForkLeg'+side,(s*.13,y-.003,z-.006))
cyl('WholeShortHandleStem',(0,-.61,1.035),(0,-.60,1.18),.026,1,'One complete short handlebar stem rooted into the upper fork crown.');join('WholeShortHandleStem','WholeFrontForkCrownUpper',(0,-.61,1.05))
G['WholeRaisedHandlebar']=path([(-.36,-.53,1.22),(-.21,-.60,1.22),(-.12,-.60,1.18),(.12,-.60,1.18),(.21,-.60,1.22),(.36,-.53,1.22)],.018,1,'One continuous broad raised handlebar, independent of the new tank and engine; fixed without steering control claim.');join('WholeRaisedHandlebar','WholeShortHandleStem',(0,-.60,1.175))
for tag,s in[('Left',-1),('Right',1)]:
 n='WholeHandleGrip'+tag;cyl(n,(s*.245,-.58,1.22),(s*.37,-.525,1.22),.027,2,'One full thick handgrip exterior over the handlebar end.');join(n,'WholeRaisedHandlebar',(s*.29,-.563,1.22))
# Complete blank headlamp, not transparent optics, attached to the fork crown.
cyl('WholeRoundHeadlampCase',(0,-.76,.98),(0,-.95,.98),.105,0,'One complete round blank headlamp case, a fixed opaque exterior.');box('WholeLampCrownBracket',(-.055,-.80,.96),(.055,-.61,1.02),1,'One complete bracket links the lamp case to the top fork crown.');join('WholeLampCrownBracket','WholeFrontForkCrownUpper',(0,-.63,1.018));join('WholeLampCrownBracket','WholeRoundHeadlampCase',(0,-.78,.985))
cyl('WholeOpaqueLampFace',(0,-.938,.98),(0,-.965,.98),.092,3,'One entire opaque nonemissive pale lamp-face insert with buried rear root.');join('WholeOpaqueLampFace','WholeRoundHeadlampCase',(0,-.945,.98))
# Two complete upper arch mudguards, away from actual tire surfaces.
def fender(y,width):
 m=Mesh();tt=[math.radians(20+140*i/20)for i in range(21)];prof=[(-width,.395),(width,.395),(width,.419),(-width,.419)];pt=lambda p,t:(p[0],y+p[1]*math.cos(t),.36+p[1]*math.sin(t))
 for i in range(20):
  for j,p in enumerate(prof):q=prof[(j+1)%4];m.quad(pt(p,tt[i]),pt(q,tt[i]),pt(q,tt[i+1]),pt(p,tt[i+1]),0)
 for t in[tt[0],tt[-1]]:m.quad(*(pt(p,t)for p in prof),0)
 return m.result('One full thick upper-arc mudguard with real front/back cut faces and inner surface positively apart from the whole tire; no coverage or road-safety claim.')
G['WholeFrontArchMudguard']=fender(-.92,.092);G['WholeRearArchMudguard']=fender(.78,.105)
for tag,s in[('Left',-1),('Right',1)]:
 n='WholeFrontMudguardStrut'+tag;cyl(n,(s*.13,-.76,.72),(s*.075,-.76,.735),.020,1,'One complete short front-mudguard side support.');join(n,'WholeFrontForkLeg'+tag,(s*.124,-.76,.722));join(n,'WholeFrontArchMudguard',(s*.080,-.76,.735))
 n='WholeRearMudguardStrut'+tag;cyl(n,(s*.15,.55,.90),(s*.090,.55,.695),.022,1,'One whole short rear-mudguard support rooted into saddle rail and guard.');join(n,'WholeRearSaddleRail'+tag,(s*.147,.55,.890));join(n,'WholeRearArchMudguard',(s*.09,.55,.695))
# One new continuous bent exhaust exterior and an independent long low muffler.
G['WholeBentExhaustHeader']=path([(.17,-.23,.85),(.24,-.34,.78),(.27,-.40,.48),(.28,-.30,.32),(.28,.30,.32)],.031,1,'One complete bent side exhaust-like exterior from the head toward the low rear silencer; closed solid tube, no gas path or heat/emissions function.');join('WholeBentExhaustHeader','WholeCylinderHead',(.175,-.237,.845))
G['WholeLowLongMuffler']=axial([(0,0),(.060,0),(.072,.065),(.072,.65),(.052,.72),(0,.72)],(.28,.10,.32),(1,0,0),(0,0,1),(0,1,0),24,1,'One whole closed long low muffler-like exterior, independently rooted over the full bent header and rear bracket.');join('WholeLowLongMuffler','WholeBentExhaustHeader',(.28,.22,.32))
# Two broad finite stand feet support the deliberately upright empty display.
for tag,s in[('Left',-1),('Right',1)]:
 n='WholeParkingStandLeg'+tag;cyl(n,(s*.16,.18,.29),(s*.27,.25,.028),.019,1,'One complete deployed fixed stand leg, not a balance or stability simulation.');join(n,'WholeDoubleCradleLoop'+tag,(s*.162,.182,.285));q='WholeParkingStandFoot'+tag;box(q,(s*.27-.045,.205,0),(s*.27+.045,.295,.04),2,'One complete broad ground sole at the end of the fixed display stand.');GROUND.append(q);join(q,n,(s*.27,.25,.028))
AIR_POINTS=[(0,-.92,.56),(0,.78,.56),(0,-.92,.742),(0,.78,.742),(0,-.60,.54),(.36,.45,.64)]
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='transport-fixed-double-cradle-and-tank-over-engine-motorcycle-01';VERSION='1.0.0';TITLE='Fixed Double Cradle and Tank Over Engine Motorcycle'
DESCRIPTION='One wholly newly authored complete empty motorcycle-style static exterior. Two broad annular tires with open rims, complete spokes, hubs and fixed transverse axles carry a new twin-fork and rear-swing-arm organization. Two continuous closed lower cradle loops surround an independent round crankcase, integral-rib cylinder and complete head. A full sculpted longitudinal tank occupies the upper frame, while two whole rear rails support a separate long stepped saddle over the rear wheel. Full fixed suspension-strut appearances, fork crowns, raised handlebar/grips, blank round headlamp, two genuinely thick raised mudguard arches and a complete bent side exhaust with long low muffler finish the whole vehicle. A deployed two-foot stand accompanies the actual finite tire tread facets. This is not the existing thin diamond-frame pedal bicycle with a motor pasted on: no old frame, pedal crank, chainring or mesh is reused. It is not the existing step-through scooter with different wheels: there is no low foot deck, leg shield, enclosing rear seat body or open step-through bay. Every visible coordinate is newly authored to the complete engine-in-cradle/tank/saddle/fork/swing-arm organization. One prop zero scenes, four opaque constant untextured PBR roles, metres native Z up and whole horizontal-envelope-centered ground datum. Simplified invented fixed illustrative exterior only: no rider, internal engine, fuel path, exhaust fluid, real brakes, suspension spring, drivetrain, steering, wheel rotation, speed, balance, rider fit, load, roadworthiness, manufacture or operating safety is made or verified. Rigging animation and interaction not made.'
PALETTE=[('WholeFrameTankAndMudguards_DeepMaroon',(.32,.075,.055,1),.51,.22),('WholeEngineRimsForkAndExhaust_SatinSteel',(.39,.44,.44,1),.47,.58),('WholeTiresSaddleGripsAndSoles_Charcoal',(.035,.045,.047,1),.78,.03),('WholeOpaqueBlankLamp_WarmCream',(.72,.70,.57,1),.60,.08)]
FOCUS=(0,0,.63);CAMERAS={'thumbnail':(7,-8,4.3),'qa-front':(7,-8,4.3),'qa-side':(9,0,3.3),'qa-top':(0,0,10),'qa-back':(7,8,4.3),'qa-wireframe':(7,-8,4.3)}
fwd=unit(sub(FOCUS,CAMERAS['thumbnail']));right=unit(cross(fwd,(0,0,1)));up=cross(right,fwd);pts=[p for g in G.values()for p in g['vertices']];ORTHO=round(max(max(dot(p,u)for p in pts)-min(dot(p,u)for p in pts)for u in[right,up])*1.23,3)
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
root=bpy.data.objects.new('OneWholeDoubleCradleTankOverEngineMotorcycle',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='two whole tire treads and stand soles; horizontal bounds-centred; fixed motorcycle';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==5376 and len(parts)==58
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
  files[role]={'path':f'assets/transport/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'transport','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
