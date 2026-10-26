"""One newly authored complete open scoop wheel and opposed conveyor boom excavator exterior. Static art only."""
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
# Whole new crawler, two opposed conveyor booms and open scoop-wheel excavator exterior.
G={};ROOT_WITNESSES=[];AIR_POINTS=[];GROUND=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
def xf(g,fn):
 g['vertices']=[fn(p)for p in g['vertices']]
 v=g['vertices'];volume=sum(dot(v[a],cross(v[b],v[c]))for a,b,c in g['faces'])/6
 if volume<0:g['faces']=[tuple(reversed(f))for f in g['faces']]
 return g

def loop(a,b,r):
 return[(y+r*math.cos(t),r*math.sin(t))for y,start in[(b,-math.pi/2),(a,math.pi/2)]for t in[start+j*math.pi/10 for j in range(11)]]
def ringprism(out,inn,x0,x1,mat,role):
 m=Mesh()
 for i in range(len(out)):
  j=(i+1)%len(out)
  for x in[x0,x1]:m.quad((x,*out[i]),(x,*out[j]),(x,*inn[j]),(x,*inn[i]),mat)
  for p in[out,inn]:m.quad((x0,*p[i]),(x0,*p[j]),(x1,*p[j]),(x1,*p[i]),mat)
 return m.result(role)
for lab,s in[('Left',-1),('Right',1)]:
 a,b=sorted([s*.73,s*1.18]);n='WholeClosedCrawler'+lab;G[n]=xf(ringprism(loop(-.91,.91,.36),loop(-.91,.91,.26),a,b,2,'One complete closed thick crawler band with whole flat sole and true long inner opening; no articulated track shoes.'),lambda p:(p[0],p[1],p[2]+.36));GROUND.append(n)
 for i,y in enumerate([-.91,-.31,.31,.91]):
  k='WholeCrawlerRoller'+lab+str(i);cyl(k,(a+.027,y,.36),(b-.027,y,.36),.27,1,'One complete broad fixed crawler roller with its circular end faces deliberately inset.',20);join(k,n,((a+b)/2,y,.095))
 for i,y in enumerate([-.91,.91]):
  k='WholeCrossAxle'+lab+str(i);aa,bb=sorted([s*.37,s*1.20]);cyl(k,(aa,y,.36),(bb,y,.36),.065,1,'Whole transverse fixed end axle connecting the complete roller to the inner track carrier.',16);join(k,'WholeCrawlerRoller'+lab+str(0 if i==0 else 3),(s*.96,y,.36));join(k,'WholeLowCrawlerCarrier',(s*.52,y,.36))
G['WholeLowCrawlerCarrier']=solid_union([((-.84,-1.04,.29),(-.43,1.04,.49)),((.43,-1.04,.29),(.84,1.04,.49)),((-.80,-.70,.42),(.80,-.46,.79)),((-.80,.46,.42),(.80,.70,.79)),((-.56,-.56,.60),(.56,.56,.91))],2,'One complete connected undercarriage with two inner longitudinal beams, broad transverse ties and an integral high round-pedestal seat.')
for lab,s in[('Left',-1),('Right',1)]:
 for i,y in enumerate([-.31,.31]):join('WholeCrawlerRoller'+lab+str(i+1),'WholeLowCrawlerCarrier',(s*.79,y,.39))
cyl('WholeFixedRoundPedestal',(0,0,.84),(0,0,1.10),.62,1,'Whole broad fixed turntable-style pedestal, static only without bearing or motion claim.',32);join('WholeFixedRoundPedestal','WholeLowCrawlerCarrier',(0,0,.87))
G['WholeUpperMachineDeck']=extrude([(-1.02,-.85),(1.02,-.85),(1.13,-.65),(1.13,.97),(.91,1.17),(-.91,1.17),(-1.02,.95)],1.04,1.25,'z',0,'One whole newly drawn broad upper deck supporting the two oppositely directed conveyor booms and separate side cabin, not a dragline rear winch house.');join('WholeUpperMachineDeck','WholeFixedRoundPedestal',(0,0,1.075))
G['WholeIndependentSideCab']=solid_union([((.52,-.61,1.22),(1.28,.47,1.53)),((.52,-.61,2.20),(1.28,.47,2.29)),((.52,-.61,1.50),(.60,-.53,2.23)),((1.20,-.61,1.50),(1.28,-.53,2.23)),((.52,.39,1.50),(.60,.47,2.23)),((1.20,.39,1.50),(1.28,.47,2.23))],3,'One whole enclosed lower cabin and roof joined by four full window posts, with genuine empty window bays. Static empty exterior, no glass or operator fit.');join('WholeIndependentSideCab','WholeUpperMachineDeck',(.78,0,1.235))
G['WholeLowAuxiliaryCover']=extrude([(.30,1.22),(1.05,1.22),(1.05,1.67),(.85,1.85),(.45,1.85),(.30,1.68)],-.93,-.39,'x',0,'Whole compact sloping auxiliary machinery cover at the opposite rear side of the deck, leaving a central through-boom route. No engine internals.');join('WholeLowAuxiliaryCover','WholeUpperMachineDeck',(-.65,.7,1.235))

def framepanel(length,height,mat,role):
 # Whole side rail with full rectangular cell openings, built as one shared-boundary solid.
 boxes=[((0,-.035,-height/2),(length,.035,-height/2+.075)),((0,-.035,height/2-.075),(length,.035,height/2))]
 for j in range(5):
  t=length*j/4;boxes.append(((max(0,t-.04),-.035,-height/2),(min(length,t+.04),.035,height/2)))
 return solid_union(boxes,mat,role)
BOOMS={}
for lab,p0,p1,width,height in [('Digging',(0,-.26,1.35),(0,-3.15,1.78),.68,.43),('Outfeed',(0,.42,1.37),(0,3.20,2.10),.56,.38)]:
 vec=sub(p1,p0);length=math.sqrt(dot(vec,vec));w=unit(vec);up=(0,-w[2],w[1]);up=mul(up,1 if up[2]>0 else-1)
 def pose(t,x,q,p0=p0,w=w,up=up):return add(p0,add(mul(w,t),add((x,0,0),mul(up,q))))
 BOOMS[lab]=(p0,p1,length,pose,width,height)
 axle='Whole'+lab+'RootPin';cyl(axle,add(p0,(-width/2-.10,0,0)),add(p0,(width/2+.10,0,0)),.11,1,'Whole transverse conveyor-arm root pin crossing two complete heel cheeks.',20)
 for side,s in[('Left',-1),('Right',1)]:
  n='Whole'+lab+'HeelCheek'+side;lo=(s*width/2-.07,p0[1]-.16,1.20);hi=(s*width/2+.07,p0[1]+.16,p0[2]+.17);G[n]=block(lo,hi,0,'One entire short thick arm heel cheek integral by hidden root overlap with the full upper deck.');join(n,'WholeUpperMachineDeck',(s*width/2,p0[1],1.23));join(n,axle,(s*width/2,p0[1],p0[2]))
  n='Whole'+lab+'PerforatedSideFrame'+side;G[n]=xf(framepanel(length,height,0,'One complete long open side truss web of this entire conveyor arm, with shared-boundary rails and four actual windows, not loose beams or an old crane mesh.'),lambda p,s=s,pose=pose,width=width:pose(p[0],s*width/2+p[1],p[2]));join(n,axle,pose(.02,s*width/2,0))
 for j,t in enumerate([.025,length-.025]):
  n='Whole'+lab+'ConveyorEndRoller'+str(j);c=pose(t,0,height/2+.045);cyl(n,add(c,(-width/2-.055,0,0)),add(c,(width/2+.055,0,0)),.103,1,'Whole transverse conveyor roller reaching both arm frames beneath the entire continuous fixed belt, not a moving or carrying component.',20)
  for side,s in[('Left',-1),('Right',1)]:join(n,'Whole'+lab+'PerforatedSideFrame'+side,pose(t,s*width/2,height/2-.022))
 belt='Whole'+lab+'ContinuousFixedBelt';G[belt]=xf(ringprism(loop(.025,length-.025,.118),loop(.025,length-.025,.098),-width/2+.065,width/2-.065,2,'One whole closed fixed conveyor-belt appearance with full upper and lower surfaces and continuous rounded end returns. No transport or working belt path is asserted.'),lambda p,pose=pose,height=height:pose(p[1],p[0],p[2]+height/2+.045))
 for j,t in enumerate([.025,length-.025]):join(belt,'Whole'+lab+'ConveyorEndRoller'+str(j),pose(t,0,height/2+.145))
 AIR_POINTS.append(pose(length*.125,width/2,0))
# The whole front scoop wheel is fixed on a true transverse nose shaft, not a chain loop.
p0,p1,length,pose,width,height=BOOMS['Digging'];C=p1
cyl('WholeScoopWheelNoseShaft',add(C,(-.63,0,0)),add(C,(.63,0,0)),.115,1,'Whole transverse shaft through the front arm nose and the complete scoop-wheel hub, fixed orientation only.',24)
for side,s in[('Left',-1),('Right',1)]:join('WholeScoopWheelNoseShaft','WholeDiggingPerforatedSideFrame'+side,pose(length-.018,s*width/2,0))
cyl('WholeScoopWheelHub',add(C,(-.27,0,0)),add(C,(.27,0,0)),.25,1,'Whole thick central hub on the nose shaft; an actual open spoke-wheel surrounds it.',28);join('WholeScoopWheelHub','WholeScoopWheelNoseShaft',C)
for side,s in[('Left',-1),('Right',1)]:
 n='WholeScoopWheelRim'+side;G[n]=axial([(1.00,s*.36-.07),(1.13,s*.36-.07),(1.13,s*.36+.07),(1.00,s*.36+.07)],C,(0,1,0),(0,0,1),(1,0,0),40,1,'One complete thick open annular scoop-wheel rim; no filled disc, water housing, nozzle or divided impulse cups.')
 for j in range(6):
  a=math.tau*j/6+.10;d=(0,math.cos(a),math.sin(a));k='WholeWheelSpoke'+side+str(j);aa=add(C,add((s*.20,0,0),mul(d,.18)));bb=add(C,add((s*.36,0,0),mul(d,1.075)));G[k]=beam(aa,bb,.095,.10,0,'One full slightly dished radial spoke joining hub to whole annular wheel rim, fixed art not wheel dynamics.');join(k,'WholeScoopWheelHub',add(aa,mul(sub(bb,aa),.045)));join(k,n,add(aa,mul(sub(bb,aa),.965)))
# Eight whole single-cavity scoops, each has its own continuous floor/back/two side walls.
for j in range(8):
 a=math.tau*j/8+.17;rr=(0,math.cos(a),math.sin(a));tt=(0,-math.sin(a),math.cos(a));base=add(C,mul(rr,1.075))
 def wp(p,base=base,rr=rr,tt=tt):return add(base,add((p[0],0,0),add(mul(tt,p[1]),mul(rr,p[2]))))
 n='WholeSingleOpenScoop'+str(j);g=solid_union([((-.50,-.26,-.085),(.50,.23,-.012)),((-.50,-.26,-.085),(.50,-.19,.24)),((-.50,-.26,-.085),(-.425,.23,.24)),((.425,-.26,-.085),(.50,.23,.24))],1,'One complete newly authored single open scoop, with integral full floor, bent back and two finite side walls. Tangential mouth and outward cavity stay genuinely open; not an old split water bucket, cutter tooth, suspended drag bucket or copied mesh.');G[n]=xf(g,wp)
 for side,s in[('Left',-1),('Right',1)]:join(n,'WholeScoopWheelRim'+side,wp((s*.36,0,-.045)))
 if j in [0,2,4,6]:AIR_POINTS.append(wp((0,.02,.11)))
# Complete elevated stay mast links the opposed long arms to the upper deck.
for side,s in[('Left',-1),('Right',1)]:
 n='WholeStayMastLeg'+side;aa=(s*.43,.59,1.22);bb=(s*.085,.60,2.67);G[n]=beam(aa,bb,.12,.12,0,'One whole tall inclined mast leg from the upper deck to a common top head; support appearance only, no load calculation.');join(n,'WholeUpperMachineDeck',add(aa,mul(sub(bb,aa),.01)))
cyl('WholeStayMastHead',(-.17,.60,2.65),(.17,.60,2.65),.11,1,'Whole horizontal mast-head member joining both complete legs.',20)
for side,s in[('Left',-1),('Right',1)]:join('WholeStayMastHead','WholeStayMastLeg'+side,(s*.09,.60,2.65))
for lab in ['Digging','Outfeed']:
 p0,p1,length,pose,width,height=BOOMS[lab]
 for side,s in[('Left',-1),('Right',1)]:
  aa=(s*.10,.60,2.65);bb=pose(length-.045,s*width/2,height/2-.03);n='Whole'+lab+'FixedStay'+side;cyl(n,aa,bb,.020,2,'One whole fixed straight stay between the complete mast and a whole conveyor-arm end web. No cable tension, flexible rigging or balance verification.',10);join(n,'WholeStayMastHead',add(aa,mul(sub(bb,aa),.007)));join(n,'Whole'+lab+'PerforatedSideFrame'+side,add(bb,mul(sub(aa,bb),.002)))
AIR_POINTS += [(0,0,.22),(.91,-.04,1.87),add(C,(0,-.48,.45))]
vv=[v for g in G.values()for v in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='construction-fixed-open-scoop-wheel-and-opposed-belt-boom-excavator-01';VERSION='1.0.0';TITLE='Fixed Open Scoop Wheel and Opposed Belt Boom Excavator'
DESCRIPTION='One newly authored complete reduced-proportion bucket-wheel excavator static exterior. Two whole closed crawler bands and complete rollers support a connected carrier, broad round fixed pedestal and full upper deck. A real-window side cabin and separate low auxiliary cover flank two complete oppositely directed long perforated conveyor-arm frames. Each arm includes full side webs, transverse end rollers and one continuous closed fixed belt exterior with genuine end returns. At the forward arm nose a full transverse shaft and hub carry two open annular rims with complete radial spokes and whole single-cavity scoop shells; every scoop has its own integral back, floor and two side walls, with an actual open tangential mouth and outward cavity. A common high stay mast and complete fixed stays link both arms back to the deck. All visible coordinates newly authored. No old crawler, impulse waterwheel, drag bucket, cabin or conveyor mesh is imported. It is neither a closed-chain trencher with a lateral screw, nor a dragline with a suspended single bucket and two independent ropes, nor a divided-cup waterwheel in a nozzle housing. One static prop zero scenes, metres, native Z up, complete horizontal bounds centred over whole crawler soles, four opaque constant untextured PBR roles. No terrain, load or people. No running tracks, digging, material transport, belt travel, slewing, wheel motion, drive, bearings, hydraulics, cable tension, structural sizing, equilibrium, access, operator fit, manufacture or engineering/safety performance. Rigging, animation and interaction are not made or verified.'
PALETTE=[('WholeDeckFramesMastAndSpokes_MutedOchre',(.58,.32,.085,1),.69,.18),('WholeRollersRimsAndScoops_SatinSteel',(.32,.39,.40,1),.49,.64),('WholeTracksBeltsAndStays_Graphite',(.045,.060,.064,1),.78,.08),('WholeSideCab_DeepPetrol',(.045,.21,.23,1),.64,.16)]
FOCUS=(0,0,1.45);ORTHO=8.4
CAMERAS={'thumbnail':(9,-11,7),'qa-front':(9,-11,7),'qa-side':(10,0,5),'qa-top':(0,0,12),'qa-back':(-8,11,6),'qa-wireframe':(9,-11,7)}
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
root=bpy.data.objects.new('OneWholeOpenScoopWheelOpposedBeltBoomExcavator',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole crawler soles at display datum; horizontal bounds-centred; complete opposed-boom scoop-wheel static exterior';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==5448 and len(parts)==66
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
