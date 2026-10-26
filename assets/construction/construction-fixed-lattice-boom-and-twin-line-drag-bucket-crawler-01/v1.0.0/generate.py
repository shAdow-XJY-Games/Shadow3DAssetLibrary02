"""One newly authored complete lattice-boom twin-line drag-bucket crawler exterior. Static art only."""
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
# Whole new crawler-mounted lattice-boom and suspended-bucket dragline exterior.
G={};ROOT_WITNESSES=[];AIR_POINTS=[];GROUND=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
def box(n,lo,hi,mat,role):G[n]=block(lo,hi,mat,role)
def path_tube(n,points,r,mat,role,N=10):
 m=Mesh();rows=[]
 for j,p in enumerate(points):
  d=sub(points[min(j+1,len(points)-1)],points[max(0,j-1)]);w=unit(d);u=unit(cross(w,(1,0,0)if abs(w[0])<.9 else(0,0,1)));v=cross(w,u)
  rows.append([add(p,add(mul(u,r*math.cos(i*math.tau/N)),mul(v,r*math.sin(i*math.tau/N))))for i in range(N)])
 for a,b in zip(rows,rows[1:]):
  for i in range(N):j=(i+1)%N;m.quad(a[i],a[j],b[j],b[i],mat)
 for row,p in[(rows[0],points[0]),(rows[-1],points[-1])]:
  for i in range(N):m.tri([p,row[i],row[(i+1)%N]],mat)
 G[n]=m.result(role)
def annular_prism(outer,inner,x0,x1,mat,role):
 m=Mesh();N=len(outer)
 for i in range(N):
  j=(i+1)%N
  for x in[x0,x1]:m.quad((x,*outer[i]),(x,*outer[j]),(x,*inner[j]),(x,*inner[i]),mat)
  for row in[outer,inner]:m.quad((x0,*row[i]),(x0,*row[j]),(x1,*row[j]),(x1,*row[i]),mat)
 return m.result(role)
def track_loop(r):
 return[(y+r*math.cos(t),.33+r*math.sin(t))for y,start in[(.82,-math.pi/2),(-.82,math.pi/2)]for t in[start+j*math.pi/12 for j in range(13)]]
for lab,s in[('Left',-1),('Right',1)]:
 x0,x1=sorted([s*.69,s*1.06]);n='WholeClosedCrawlerBelt'+lab;G[n]=annular_prism(track_loop(.33),track_loop(.245),x0,x1,2,'One complete continuous thick racetrack crawler belt, real central open region and whole straight lower ground facet. Fixed shape with no individual articulated shoes.');GROUND.append(n)
 for i,y in enumerate([-.82,-.28,.28,.82]):
  k='WholeCrawlerRoller'+lab+str(i);cyl(k,(x0+.028,y,.33),(x1-.028,y,.33),.254,3,'Whole fixed transverse crawler roller held in a closed belt, with its end faces inset from the belt outer faces.',20);join(k,n,((x0+x1)/2,y,.080))
 for i,y in enumerate([-.82,.82]):
  k='WholeCrawlerAxle'+lab+str(i);a,b=sorted([s*.32,s*1.083]);cyl(k,(a,y,.33),(b,y,.33),.052,1,'Whole fixed axle connecting an end crawler roller to the inner track carrier; proud small end cap, not coplanar with outer roller face.',16);join(k,'WholeCrawlerRoller'+lab+str(0 if i==0 else 3),(s*.83,y,.33));join(k,'WholeLowCrawlerCrossFrame',(s*.43,y,.33))
G['WholeLowCrawlerCrossFrame']=solid_union([((-.76,-.95,.275),(-.39,.95,.43)),((.39,-.95,.275),(.76,.95,.43)),((-.70,-.67,.34),(.70,-.43,.58)),((-.70,.43,.34),(.70,.67,.58)),((-.48,-.50,.39),(.48,.50,.61))],2,'One whole connected low track carrier with full side rails, separated transverse ties and central pedestal seat. Its underside remains visibly open between the two belts.')
for lab,s in[('Left',-1),('Right',1)]:
 for i,y in enumerate([-.28,.28]):join('WholeCrawlerRoller'+lab+str(i+1),'WholeLowCrawlerCrossFrame',(s*.72,y,.35))
cyl('WholeFixedRoundSlewPedestal',(0,0,.57),(0,0,.79),.52,1,'One complete broad fixed round pedestal between track chassis and upper machinery deck, without moving bearing or slewing claim.',32);join('WholeFixedRoundSlewPedestal','WholeLowCrawlerCrossFrame',(0,0,.59))
G['WholeChamferedUpperDeck']=extrude([(-.90,-.78),(.90,-.78),(.98,-.70),(.98,1.40),(.86,1.56),(-.86,1.56),(-.98,1.40),(-.98,-.70)],.74,.92,'z',0,'One new complete long machinery deck with chamfered rear corners, broad enough for the enclosed rear machinery body and independent side-window cab.')
join('WholeChamferedUpperDeck','WholeFixedRoundSlewPedestal',(0,0,.77))
G['WholeRearSlopingMachineryHouse']=extrude([(-.08,.89),(1.45,.89),(1.45,1.58),(1.13,1.91),(.16,1.91),(-.08,1.68)],-.83,.43,'x',0,'One full rear machinery-house exterior with sloping shoulders and a long rear body, not the small engine cover of a hydraulic arm excavator; no interior engine or winch circuit.')
join('WholeRearSlopingMachineryHouse','WholeChamferedUpperDeck',(0,.5,.905))
G['WholeSideWindowCab']=solid_union([((.39,-.67,.88),(1.12,.48,1.20)),((.39,-.67,1.94),(1.12,.48,2.03)),((.39,-.67,1.18),(.46,-.59,1.97)),((1.04,-.67,1.18),(1.12,-.59,1.97)),((.39,.40,1.18),(.46,.48,1.97)),((1.04,.40,1.18),(1.12,.48,1.97))],3,'One complete side cabin shell with real large front/side/rear window voids and a full roof, lower body deliberately solid. No glass, occupant, entry or ergonomic fit is claimed.')
join('WholeSideWindowCab','WholeChamferedUpperDeck',(.65,0,.90))
# Whole boom heel and long inclined triangular lattice boom.
G['WholeFrontBoomHeelFork']=solid_union([((-.43,-.70,.88),(.43,-.31,1.05)),((-.43,-.70,1.0),(-.31,-.31,1.23)),((.31,-.70,1.0),(.43,-.31,1.23))],0,'One whole front heel fork with two thick cheeks and an integral bottom, mounted directly to the deck.')
join('WholeFrontBoomHeelFork','WholeChamferedUpperDeck',(0,-.50,.90))
cyl('WholeBoomHeelPin',(-.48,-.50,1.06),(.48,-.50,1.06),.066,1,'Whole transverse heel pin rooted into both fork cheeks; fixed pose, no rotation travel.',20);join('WholeBoomHeelPin','WholeFrontBoomHeelFork',(.37,-.50,1.06))
P0=(0,-.50,1.06);P1=(0,-3.13,3.28);w=unit(sub(P1,P0));up=(0,w[2],-w[1])
def local(t,q,side=0,depth=0):
 c=add(P0,mul(sub(P1,P0),t));width=.36-.19*t;height=.44-.18*t
 return add(c,add((side*width*(1-q)+depth,0,0),mul(up,q*height)))

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
for lab,s in[('Left',-1),('Right',1)]:
 n='WholeInclinedTriangularBoomSide'+lab
 G[n]=lattice_panel(0,1,0,1,6,.050,0,lambda p,s=s:local(p[0],p[2],s,p[1]),'One whole sloping tapered side web of the long triangular-section dragline boom, with six real diamond apertures. The entire spatial boom is newly parameterized, not a tower-crane jib instance.')
 join(n,'WholeBoomHeelPin',local(.004,.010,s))
G['WholeInclinedBoomLowerWeb']=lattice_panel(0,1,-1,1,6,.050,0,lambda p:add(add(P0,mul(sub(P1,P0),p[0])),add((p[2]*(.36-.19*p[0]),0,0),mul(up,p[1]))),'One entire open lower web completes the boom triangular section. Its matching longitudinal edges embed into the two full side webs, avoiding separate floating bracing.')
join('WholeInclinedBoomLowerWeb','WholeBoomHeelPin',add(add(P0,mul(sub(P1,P0),.004)),(.20,0,0)))
G['WholeBoomNoseBlock']=block((-.22,-3.23,3.22),(.22,-2.90,3.56),1,'One complete fixed boom nose/sheave-housing exterior, attached to the tapered end of the whole boom. It is a closed illustrative housing, no internal reeving.')
for lab,s in[('Left',-1),('Right',1)]:join('WholeBoomNoseBlock','WholeInclinedTriangularBoomSide'+lab,local(.985,.015,s))
join('WholeBoomNoseBlock','WholeInclinedBoomLowerWeb',add(add(P0,mul(sub(P1,P0),.985)),(.16,0,0)))
# New rear open A mast anchored on separate deck-side feet, complete top cross-shaft.
for lab,s in[('Left',-1),('Right',1)]:
 n='WholeRearAMastLeg'+lab;G[n]=beam((s*.70,.74,.89),(s*.10,.62,2.34),.095,.095,1,'One whole inclined rear mast leg from the side of the deck to the high transverse head, fixed solid appearance.');join(n,'WholeChamferedUpperDeck',(s*.69,.738,.912))
cyl('WholeRearMastTopShaft',(-.18,.62,2.31),(.18,.62,2.31),.095,1,'Whole rear high cross-shaft joins the two long mast legs; fixed support appearance.',20)
for lab,s in[('Left',-1),('Right',1)]:join('WholeRearMastTopShaft','WholeRearAMastLeg'+lab,(s*.11,.622,2.31))
for lab,s in[('Left',-1),('Right',1)]:
 n='WholeFixedBoomStay'+lab;path_tube(n,[(s*.13,.62,2.32),(s*.16,-1.3,2.82),(s*.17,-3.02,3.47)],.018,2,'One continuous fixed full-length stay between the rear mast and boom nose. No load tension, flexible cable physics or boom support certification.',10)
 join(n,'WholeRearMastTopShaft',(s*.13,.61,2.323));join(n,'WholeBoomNoseBlock',(s*.17,-3.01,3.466))
# Entire empty bucket: one bent back/floor, two whole sides, whole lip and a three-sided bail.
G['WholeDragBucketBackAndFloor']=extrude([(-3.59,.76),(-3.60,.25),(-3.44,.13),(-2.62,.13),(-2.55,.22),(-2.62,.27),(-3.40,.22),(-3.50,.29),(-3.50,.76)],-.48,.48,'x',1,'One newly drawn complete thick bent bucket back/floor, opening upward and toward the machine. Actual empty interior, no spoil, cutting specification or copied excavator scoop.')
for lab,s in[('Left',-1),('Right',1)]:
 a,b=sorted([s*.425,s*.49]);n='WholeDragBucketSide'+lab
 G[n]=extrude([(-3.56,.73),(-3.56,.28),(-3.43,.17),(-2.60,.19),(-2.57,.34),(-3.00,.62)],a,b,'x',1,'One whole tapered thick bucket side, lower perimeter embedded in its full bent floor while the large top and forward mouth stay open.')
 join(n,'WholeDragBucketBackAndFloor',(s*.45,-3.41,.20))
G['WholeBucketBail']=solid_union([((-.47,-3.16,.55),(-.395,-3.04,1.09)),((.395,-3.16,.55),(.47,-3.04,1.09)),((-.47,-3.16,1.015),(.47,-3.04,1.09))],0,'One continuous three-sided bucket bail: two full long cheeks and integral upper cross-bar, visibly surrounding the open bucket without sealing it. Fixed display connection only.')
for lab,s in[('Left',-1),('Right',1)]:join('WholeBucketBail','WholeDragBucketSide'+lab,(s*.443,-3.10,.568))
path_tube('WholeFixedBucketHoist',[(0,-3.04,3.49),(0,-3.085,2.17),(0,-3.10,1.05)],.022,2,'One entire unbroken hoist-style suspension from the boom nose to the bucket bail, with full finite end overlaps. No working reeving, lifting or balancing.')
join('WholeFixedBucketHoist','WholeBoomNoseBlock',(0,-3.041,3.47));join('WholeFixedBucketHoist','WholeBucketBail',(0,-3.10,1.06))
G['WholeFrontDragFairlead']=solid_union([((-.16,-.87,.88),(.16,-.65,.99)),((-.16,-.87,.98),(-.095,-.65,1.14)),((.095,-.87,.98),(.16,-.65,1.14)),((-.16,-.87,1.12),(.16,-.65,1.18))],1,'One whole small forward fairlead frame with a real middle opening, seated on the machinery deck. It is not a working or separately counted guide accessory.')
join('WholeFrontDragFairlead','WholeChamferedUpperDeck',(0,-.70,.90))
cyl('WholeStaticDragAnchor',(-.15,-.77,1.065),(.15,-.77,1.065),.034,1,'Whole transverse fixed anchor through the fairlead cheeks, deliberately crossing the drawn drag line as one display joint.',16);join('WholeStaticDragAnchor','WholeFrontDragFairlead',(.13,-.77,1.065))
path_tube('WholeContinuousDragLine',[(0,-.77,1.065),(0,-1.65,.61),(0,-2.48,.40)],.020,2,'One continuous gently sagged fixed drag line, separate from the high hoist line and boom stays. No pull tension or movement.')
join('WholeContinuousDragLine','WholeStaticDragAnchor',(0,-.780,1.06))
for lab,s in[('Left',-1),('Right',1)]:
 n='WholeBucketDragBridle'+lab;path_tube(n,[(0,-2.48,.40),(s*.43,-2.64,.29)],.020,2,'One whole short fixed branch from the drag-line meeting point to a separate bucket-mouth side; real finite root, no chain articulation or digging performance.')
 join(n,'WholeContinuousDragLine',(s*.006,-2.482,.410));join(n,'WholeDragBucketSide'+lab,(s*.428,-2.64,.291))
AIR_POINTS=[(0,0,.16),(.75,-.15,1.60),(0,-3.20,.52),local(.083,.50,1),local(.25,.50,-1),(0,-2.0,1.5)]
vv=[v for g in G.values()for v in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='construction-fixed-lattice-boom-and-twin-line-drag-bucket-crawler-01';VERSION='1.0.0';TITLE='Fixed Lattice Boom and Twin Line Drag Bucket Crawler'
DESCRIPTION='One newly authored complete crawler-mounted dragline-style static exterior. Two whole continuous closed crawler belts and their full rollers support a connected low track frame, fixed round pedestal and long chamfered upper deck. A complete sloping rear machinery house and side cabin with true empty window openings sit behind the full heel fork. One new long tapered triangular-section lattice boom consists of three complete perforated web faces and a solid nose; an independent rear open A mast and two full stays join the deck to the nose. One whole hollow bucket has a bent back/floor, tapered side walls and continuous top bail. A complete high hoist line connects the nose to the bail, while a separate low sagged drag line and two short branches reach the bucket mouth through a fixed fairlead. All visible coordinates are new; no old hydraulic excavator, tower-crane, cabin or bucket meshes are imported or extracted. There is no hydraulic two-section dipper, no tall mast with balanced horizontal jibs, and no trolley or hook accessory swap. One whole prop zero scenes, four opaque constant untextured PBR roles, metres, native Z up and full horizontal bounds-centred crawler-sole origin. Empty reduced-proportion illustrative machine only: no running tracks, slewing, winch internals, reeving, cable tension or dynamics, boom lift, bucket travel, digging, material handling, operator fit, drive, manufacturing, stability, load or engineering/safety performance. No people or soil. Rigging, animation and interaction are not made or verified.'
PALETTE=[('WholeDeckHouseBoomAndBail_MutedOchre',(.63,.33,.08,1),.68,.18),('WholeAxlesMastAndBucket_SatinSteel',(.38,.43,.43,1),.49,.60),('WholeTracksFrameAndCables_Graphite',(.045,.06,.065,1),.76,.08),('WholeCabAndRollers_DeepPetrol',(.055,.20,.22,1),.66,.18)]
FOCUS=(0,0,1.6);ORTHO=6.60
CAMERAS={'thumbnail':(8,-10,6.8),'qa-front':(8,-10,6.8),'qa-side':(8,0,4),'qa-top':(0,0,10),'qa-back':(-7,10,6),'qa-wireframe':(8,-10,6.8)}
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
root=bpy.data.objects.new('OneWholeLatticeBoomTwinLineDragBucketCrawler',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole carrier soles at datum; horizontally centred; one complete static dragline crawler exterior';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==3516 and len(parts)==40
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
