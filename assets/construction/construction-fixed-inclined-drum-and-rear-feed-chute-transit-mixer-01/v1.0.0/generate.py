"""One wholly new complete inclined drum transport vehicle exterior. Static art only."""
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
# One wholly new inclined mixing-drum transport vehicle, no imported components.
G={};ROOT_WITNESSES=[];AIR_POINTS=[];GROUND=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
def box(n,lo,hi,m,role):G[n]=block(lo,hi,m,role)
G['WholeLongOpenLadderChassis']=solid_union([((-.78,-3.55,.68),(-.56,3.22,.96)),((.56,-3.55,.68),(.78,3.22,.96)),((-.70,-2.77,.71),(.70,-2.51,.92)),((-.70,-1.10,.71),(.70,-.80,.92)),((-.70,.78,.71),(.70,1.06,.92)),((-.70,2.55,.71),(.70,2.85,.92))],2,'One complete newly drawn long ladder chassis, with real open middle regions and full cross ties, connects the cab and the separate drum supports. Not an imported pump-truck chassis or flatbed carrying a portable mixer.')
for k,y in enumerate([-2.64,1.15,2.32]):
 ax='WholeRoadAxle'+str(k);cyl(ax,(-1.09,y,.48),(1.09,y,.48),.085,3,'One complete fixed transverse road axle, no steering or driven-wheel mechanism.',16)
 for lab,sign in [('Left',-1),('Right',1)]:
  x=sign*.96;n='Whole'+lab+'Tyre'+str(k);rr=.48/math.cos(math.pi/20)
  G[n]=axial([(.205,-.17),(rr,-.17),(rr,.17),(.205,.17)],(x,y,.48),(0,1,0),(0,0,1),(1,0,0),20,2,'One full annular road tyre has a finite lower ground facet in this fixed pose. No traction, rolling or safety claim.',math.pi/20);GROUND.append(n)
  hn='Whole'+lab+'Hub'+str(k);cyl(hn,(x-.185,y,.48),(x+.185,y,.48),.22,3,'One full wheel hub with distinct proud cap planes and a buried outer band joining the tyre.',20);join(hn,n,(x,y,.693));join(hn,ax,(x,y,.48))
  cn='Whole'+lab+'AxleSeat'+str(k);box(cn,(sign*.66-.10,y-.16,.43),(sign*.66+.10,y+.16,.76),2,'One complete low axle-seat exterior joins each axle to a longitudinal chassis rail.');join(cn,ax,(sign*.66,y,.48));join(cn,'WholeLongOpenLadderChassis',(sign*.66,y,.73))
G['WholeForwardCabShell']=extrude([(-3.65,.91),(-1.55,.91),(-1.55,2.56),(-3.31,2.56),(-3.65,2.18)],-.98,.98,'x',0,'One whole forward cab exterior with a short raked nose, thick roof and opaque divided windows. Solid stylized body, no driver, cabin interior or human-fit assertion.');join('WholeForwardCabShell','WholeLongOpenLadderChassis',(.65,-2.3,.94))
for lab,sg in [('Left',-1),('Right',1)]:
 x=sg*.977;n='Whole'+lab+'OpaqueSideWindow';G[n]=extrude([(-3.44,1.80),(-1.72,1.80),(-1.72,2.42),(-3.20,2.42),(-3.44,2.14)],x-.019,x+.019,'x',2,'One complete thick blank opaque side-window insert with buried rear and proud visible face, not a texture or true glass.');join(n,'WholeForwardCabShell',(sg*.970,-2.1,2.1))
 n='Whole'+lab+'FrontScreen';xa,xb=sorted([sg*.06,sg*.82]);G[n]=extrude([(-3.665,1.82),(-3.665,2.16),(-3.43,2.42),(-3.40,2.42),(-3.634,2.15),(-3.634,1.82)],xa,xb,'x',2,'One full thick opaque front screen follows the cab front/rake; the two screens leave a solid central divider. No transparent cabin or controls.');join(n,'WholeForwardCabShell',(sg*.40,-3.642,2.0))
box('WholeFrontBumper',(-1.06,-3.77,.83),(1.06,-3.58,1.05),3,'One complete blunt front beam positively roots into the cab nose, no crash or road-safety capability.');join('WholeFrontBumper','WholeForwardCabShell',(0,-3.62,1.0))
# Complete inclined hollow drum, front closed and rear narrowed/open. Its axis rises towards the feed assembly.
AX=unit((0,1,.26));U=(1,0,0);V=cross(U,AX);C=(0,-1.04,1.70)
def dp(x,r,t):return add(C,add(mul(AX,x),add(mul(U,r*math.cos(t)),mul(V,r*math.sin(t)))))
profile=[(0,-.10),(.40,-.10),(.65,.03),(1.01,.58),(1.08,1.50),(.99,2.20),(.71,2.92),(.47,3.30),(.41,3.30),(.65,2.90),(.93,2.18),(1.02,1.50),(.95,.60),(.58,.08),(.34,-.025),(0,-.025)]
G['WholeInclinedClosedFrontOpenRearDrum']=axial(profile,C,U,V,AX,32,1,'One complete large inclined thick pear-shaped drum with a closed front, widening middle and actual narrowed rear mouth. Both inner and outer walls and the full rim are real surfaces. It is not a portable trunnion cradle scaled onto a vehicle: this whole barrel is held by an axial front mount and a separate rear rolling-band support, while a fixed feed hopper and long open trough belong to the complete transport body. No internal paddles, mixing, rotation or material path performance.')
front=add(C,mul(AX,-.18));cyl('WholeFrontAxialDrumStub',add(C,mul(AX,-.36)),add(C,mul(AX,.01)),.17,3,'One whole short coaxial front stub is hidden partly in the drum closed face and front support. Fixed overlap, no rotating drive or bearing fit.',20);join('WholeFrontAxialDrumStub','WholeInclinedClosedFrontOpenRearDrum',add(C,mul(AX,-.06)))
G['WholeFrontRaisedDrivePedestal']=extrude([(-1.42,.90),(-.81,.90),(-.81,1.71),(-1.08,1.84),(-1.42,1.68)],-.39,.39,'x',0,'One full high front drive-pedestal exterior rises directly from the cross-tied chassis to the inclined axial drum stub. No motor interior or operational attachment.');join('WholeFrontRaisedDrivePedestal','WholeLongOpenLadderChassis',(0,-.94,.91));join('WholeFrontRaisedDrivePedestal','WholeFrontAxialDrumStub',add(C,mul(AX,-.20)))
# Full rolling-band annulus over the rear conical shoulder; two supports are visually separate from the axial front mount.
t=2.30;rad=.9511
G['WholeRearDrumRunningBand']=axial([(rad-.045,t-.075),(rad+.035,t-.075),(rad+.035,t+.075),(rad-.045,t+.075)],C,U,V,AX,32,3,'One complete thick ring around the rear shoulder of the inclined drum. This static metal band is not an independent copied handwheel or a validated running track.');join('WholeRearDrumRunningBand','WholeInclinedClosedFrontOpenRearDrum',dp(t,rad-.02,0))
for lab,sg in [('Left',-1),('Right',1)]:
 # Support roller axis follows the drum axis, positioned against its lower side.
 theta=-math.pi/2+sg*.57;pc=dp(t,rad+.16,theta);n='Whole'+lab+'RearSupportRoller'
 G[n]=axial([(0,-.14),(.20,-.14),(.20,.14),(0,.14)],pc,U,V,AX,16,3,'One whole short rear support roller exterior is fixed against the complete drum running band. Simplified positive static overlap, not an operational roller contact.',math.pi/16);join(n,'WholeRearDrumRunningBand',dp(t,rad+.015,theta))
 stand='Whole'+lab+'RearDrumSupport';box(stand,(pc[0]-.14,pc[1]-.21,.90),(pc[0]+.14,pc[1]+.21,pc[2]+.04),0,'One entire rear support upright rises from a full transverse mounting beam to the roller axis, independent of the front axial pedestal.');join(stand,n,(pc[0],pc[1],pc[2]-.05))
box('WholeRearSupportCrossBeam',(-.84,.92,.86),(.84,1.62,1.03),0,'One whole transverse support beam joins both rear drum uprights to the ladder chassis.');join('WholeRearSupportCrossBeam','WholeLongOpenLadderChassis',(.65,1.05,.93))
for lab,sg in [('Left',-1),('Right',1)]:
 theta=-math.pi/2+sg*.57;pc=dp(t,rad+.16,theta);join('Whole'+lab+'RearDrumSupport','WholeRearSupportCrossBeam',(pc[0],pc[1],.96))
# Complete rear high support frame carries an independent actual open feed hopper and open downward trough.
for lab,x in [('Left',-.68),('Right',.68)]:
 box('Whole'+lab+'RearUpright',(x-.075,2.63,.90),(x+.075,2.83,3.15),0,'One full rear feed-frame upright roots into the complete chassis, beside the drum mouth rather than through its open centre.');join('Whole'+lab+'RearUpright','WholeLongOpenLadderChassis',(x,2.72,.93))
box('WholeRearHighCrossBeam',(-.75,2.64,3.04),(.75,2.82,3.19),0,'One complete high crossmember connects both rear uprights and the empty feed hopper outer wall.');
for lab,x in [('Left',-.68),('Right',.68)]:join('WholeRearHighCrossBeam','Whole'+lab+'RearUpright',(x,2.72,3.10))
# Through hopper, four outer/inner stations; no fake dark cap at either end.
m=Mesh();rows=[]
for hx,hy,z,cy in[(.19,.16,2.64,2.16),(.58,.45,3.38,2.55),(.51,.38,3.38,2.55),(.125,.095,2.64,2.16)]:rows.append([(-hx,cy-hy,z),(hx,cy-hy,z),(hx,cy+hy,z),(-hx,cy+hy,z)])
for k,a in enumerate(rows):
 b=rows[(k+1)%4]
 for j in range(4):h=(j+1)%4;m.quad(a[j],a[h],b[h],b[j],1)
G['WholeOpenUpperFeedHopper']=m.result('One complete thick flared upper hopper has an actual open top, continuous sloping walls and a separate small real bottom opening fixed just inside the upper drum mouth region. No liquid or aggregate, no feed-flow or collision-free material trajectory assertion.')
# Two lateral brackets hold the hopper exterior without filling either opening.
for lab,sg in [('Left',-1),('Right',1)]:
 n='Whole'+lab+'HopperBracket';G[n]=beam((sg*.66,2.72,3.12),(sg*.43,2.70,3.18),.11,.12,3,'One complete short lateral bracket joins the fixed hopper wall to the high rear frame, without bridging its open centre.');join(n,'WholeRearHighCrossBeam',(sg*.62,2.72,3.12));join(n,'WholeOpenUpperFeedHopper',(sg*.46,2.70,3.17))
# Entire open U-section trough follows a new curved path from below the drum lip to the lower rear discharge end.
path=[(0,2.22,2.10),(0,2.63,1.94),(.25,3.15,1.64),(.63,3.75,1.24),(.75,4.10,1.08)];m=Mesh();prof=[(-.30,.24),(-.30,0),(.30,0),(.30,.24),(.245,.24),(.245,.055),(-.245,.055),(-.245,.24)]
# cross sections remain horizontal in width, with continuous rising walls and finite bottom thickness.
def tp(p,q):return(p[0]+q[0],p[1],p[2]+q[1])
for a,b in zip(path,path[1:]):
 for j,p in enumerate(prof):q=prof[(j+1)%len(prof)];m.quad(tp(a,p),tp(a,q),tp(b,q),tp(b,p),1)
for p in[path[0],path[-1]]:
 for f in earclip(prof):m.tri([tp(p,prof[j])for j in f],1)
G['WholeContinuousBentOpenDischargeTrough']=m.result('One entire long thick U-section discharge trough begins below the rear drum mouth and bends downward and sideways to an open-ended rear channel. It has a real continuous floor, two side walls, full thickness and no top cap; newly drawn with the whole mixer body, not an old chute mesh. No flow continuity, pouring, positioning or discharge function.')
box('WholeLowRearChuteCrossbar',(-.75,2.65,1.78),(.75,2.81,1.92),0,'One full low rear crossbar links the uprights and supports the fixed trough heel without filling its channel.');
for lab,x in [('Left',-.68),('Right',.68)]:join('WholeLowRearChuteCrossbar','Whole'+lab+'RearUpright',(x,2.72,1.85))
join('WholeContinuousBentOpenDischargeTrough','WholeLowRearChuteCrossbar',(.10,2.72,1.915))
AIR_POINTS=[(0,2.55,3.25),(0,2.20,2.70),(0,1.30,2.35),(.25,3.15,1.78),(0,-.25,.82)]
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='construction-fixed-inclined-drum-and-rear-feed-chute-transit-mixer-01';VERSION='1.0.0';TITLE='Fixed Inclined Drum and Rear Feed Chute Transit Mixer'
DESCRIPTION='One wholly newly authored complete inclined-drum transport-vehicle static exterior. A full open ladder chassis on three complete axles and six whole road wheels carries a forward raked cab with opaque divided glazing and an independent inclined thick pear-shaped drum. The drum has a closed front, real hollow interior and narrowed open rear mouth. A separate front raised axial pedestal and a rear full running-band/two-roller support establish a longitudinal drum mounting unlike the old portable mixer U-cradle, transverse trunnions, control handwheel and two-wheel frame. Behind the drum, a complete high two-post frame supports an actual through feed hopper above the mouth and a separate long continuous thick U-section trough curving downward and to one side below it. This whole arrangement is not the old Z-fold pump truck with its delivery pipe removed: no deployed outriggers, boom, pump casing or receiving bin exists. Every visible coordinate is newly authored; no prior truck, mixer, shell or wheel mesh imported. One complete static prop zero scenes; four constant opaque untextured PBR materials, native metre-style Z up, all tyre facets on the ground datum and horizontal bounds centred. Empty stylized art only; no concrete, mixing paddles, motor interior, drum rotation, roller contact performance, material flow, feeding, pouring, loading, transport, steering, human fit, chassis strength, engineering compatibility, manufacture, operation or safety validation. Rigging animation and interaction not made or verified.'
PALETTE=[('WholeCabAndSupports_MutedOchre',(.53,.27,.085,1),.67,.20),('WholeDrumHopperAndTrough_WarmIvory',(.71,.69,.58,1),.62,.18),('WholeTyresChassisAndWindows_Graphite',(.045,.062,.07,1),.77,.12),('WholeHubsBandAndHardware_Steel',(.40,.46,.48,1),.43,.60)]
FOCUS=(0,0,1.55);CAMERAS={'thumbnail':(9,12,7),'qa-front':(9,12,7),'qa-side':(13,0,5),'qa-top':(0,0,15),'qa-back':(-9,-12,7),'qa-wireframe':(9,12,7)}
fwd=unit(sub(FOCUS,CAMERAS['thumbnail']));right=unit(cross(fwd,(0,0,1)));up=cross(right,fwd);pts=[p for g in G.values()for p in g['vertices']];ORTHO=round(max(max(dot(p,u)for p in pts)-min(dot(p,u)for p in pts)for u in[right,up])*1.20,3);WIRE_THICKNESS=ORTHO/1800
FRAME_OFFSET=add(mul(right,(min(dot(sub(p,FOCUS),right)for p in pts)+max(dot(sub(p,FOCUS),right)for p in pts))/2),mul(up,(min(dot(sub(p,FOCUS),up)for p in pts)+max(dot(sub(p,FOCUS),up)for p in pts))/2));FOCUS=add(FOCUS,FRAME_OFFSET);CAMERAS={k:add(v,FRAME_OFFSET)for k,v in CAMERAS.items()}

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
root=bpy.data.objects.new('OneWholeInclinedDrumTransitMixer',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='six whole tyre soles; horizontal envelope centred; fixed inclined drum transport vehicle';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==3820 and len(parts)==45
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
 d={'id':ASSET,'version':VERSION,'category':'vehicles','assetKind':'prop','theme':'construction','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
