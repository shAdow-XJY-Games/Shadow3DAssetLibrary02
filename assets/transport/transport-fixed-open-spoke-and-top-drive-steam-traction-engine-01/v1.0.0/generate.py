"""One newly authored whole open-spoke top-drive steam traction engine. Static art only."""
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
# Entire new road-traction-engine exterior, one fixed illustrative machine.
ROOT_WITNESSES=[];AIR_POINTS=[];GROUND=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
# Whole open-spoke wheels: occupied radial cells share their original edges.
# The hub, spokes and full rim form one manifold solid, not stacked disks.
def road_wheel(x0,x1,y,z,R,N,spokes,mat):
 rh=.15*R;ri=.88*R;phase=math.pi/N;pts={};cells=[]
 for j in range(N):
  a=phase+math.tau*j/N
  for k,r in enumerate([rh,ri,R]):pts[k,j]=(y+r*math.cos(a),z+r*math.sin(a))
 pts['c']=(y,z)
 for j in range(N):
  k=(j+1)%N;cells.append(['c',(0,j),(0,k)])
  cells.append([(1,j),(2,j),(2,k),(1,k)])
  if j%(N//spokes)==0:cells.append([(0,j),(1,j),(1,k),(0,k)])
 edges={};m=Mesh()
 for c in cells:
  for x in[x0,x1]:
   for j in range(1,len(c)-1):m.tri([(x,*pts[c[k]])for k in[0,j,j+1]],mat)
  for a,b in zip(c,c[1:]+c[:1]):edges.setdefault(frozenset([a,b]),[]).append((a,b))
 for pair in edges.values():
  if len(pair)==1:
   a,b=pair[0];m.quad((x0,*pts[a]),(x0,*pts[b]),(x1,*pts[b]),(x1,*pts[a]),mat)
 return m.result('One entire thick open-spoke road wheel with shared hub, radial webs and complete outer rim, a true flat bottom facet and real clear wedge openings. Fixed art only, no rolling or bearing fit.')
for label,y,R,x,w,N,spokes in [('Front',-1.58,.52,.82,.15,24,6),('Rear',1.00,.94,1.00,.26,32,8)]:
 z=R*math.cos(math.pi/N)
 for side,sgn in [('Left',-1),('Right',1)]:
  n=side+label+'WholeOpenSpokeWheel';a,b=sorted([sgn*(x-w/2),sgn*(x+w/2)]);G[n]=road_wheel(a,b,y,z,R,N,spokes,0);GROUND.append(n)
 cyl(label+'WholeAxle',(-x-w*.6,y,z),(x+w*.6,y,z),.072 if label=='Rear' else .050,2,'One complete fixed transverse axle passing through both full wheel hubs; no rotation, steering or load claim.',16)
 for side,sgn in [('Left',-1),('Right',1)]:join(label+'WholeAxle',side+label+'WholeOpenSpokeWheel',(sgn*x,y,z))
FRONTZ=.52*math.cos(math.pi/24);REARZ=.94*math.cos(math.pi/32)
G['WholeFrontPivotedCrossFrame']=solid_union([((-.70,-1.67,FRONTZ-.055),(.70,-1.49,FRONTZ+.10)),((-.13,-1.72,FRONTZ+.05),(.13,-1.44,.90))],2,'One complete front crossframe and raised central pivot-block appearance carrying the small front axle beneath the boiler. Static straight pose, no actual steerable joint.')
join('WholeFrontPivotedCrossFrame','FrontWholeAxle',(0,-1.58,FRONTZ))
G['WholeLongChassisAndRearFootplate']=solid_union([((-.32,-1.85,.79),(.32,.97,.94)),((-.49,.64,.62),(.49,1.16,1.03)),((-.67,.94,.62),(.67,1.72,.76))],2,'One newly drawn continuous long narrow central chassis, rear-axle housing and broad open rear operator-footplate appearance. It is not a scaled low railway toy chassis or a stationary engine bench.')
join('WholeLongChassisAndRearFootplate','WholeFrontPivotedCrossFrame',(0,-1.58,.85));join('WholeLongChassisAndRearFootplate','RearWholeAxle',(0,1.00,REARZ))
G['WholeHorizontalBoilerExterior']=axial([(0,-2.00),(.40,-2.00),(.46,-1.91),(.46,-1.40),(.482,-1.40),(.482,-1.34),(.46,-1.34),(.46,-.12),(.482,-.12),(.482,-.06),(.46,-.06),(.46,.47),(0,.47)],(0,0,1.24),(1,0,0),(0,0,1),(0,1,0),24,1,'One entire closed horizontal boiler exterior with a blunt front cover and two integral raised bands in the same skin. No actual pressure chamber, tubes, fire or functional steam vessel.',math.pi/24)
join('WholeHorizontalBoilerExterior','WholeLongChassisAndRearFootplate',(0,-1.2,.88))
G['WholeRearUprightFirebox']=extrude([(-.43,.67),(.43,.67),(.43,1.58),(.31,1.81),(-.31,1.81),(-.43,1.58)],.32,.96,'y',1,'One full upright rear firebox exterior meets the boiler and rear chassis; upper shoulders rise above the open operator platform. It is closed static art, not a combustion or boiler system.')
join('WholeRearUprightFirebox','WholeHorizontalBoilerExterior',(0,.40,1.24));join('WholeRearUprightFirebox','WholeLongChassisAndRearFootplate',(0,.82,.85))
# Front blind hollow chimney and the separate rear inspection-cover appearance.
G['WholeTallFrontFlaredStack']=axial([(0,1.62),(.105,1.62),(.105,2.45),(.15,2.55),(.15,2.66),(.105,2.66),(.105,2.50),(.067,2.43),(.067,2.32),(0,2.32)],(0,-1.69,0),(1,0,0),(0,1,0),(0,0,1),20,2,'One whole tall front stack with a flared thick top and a real short blind cavity. Its base is embedded into the boiler crown; no connected exhaust or smoke.')
join('WholeTallFrontFlaredStack','WholeHorizontalBoilerExterior',(0,-1.69,1.65))
G['WholeRearFireboxDoor']=axial([(0,.93),(.19,.93),(.19,1.006),(.16,1.026),(0,1.026)],(0,0,1.17),(1,0,0),(0,0,1),(0,1,0),12,2,'One full thick closed rear inspection-cover appearance with its root hidden inside the firebox, not a movable opening.')
join('WholeRearFireboxDoor','WholeRearUprightFirebox',(0,.945,1.17))
# The top engine is newly positioned as part of the road vehicle, not an imported drive bench.
G['WholeUpperEngineSaddle']=block((-.25,-1.10,1.55),(.25,-.59,1.88),2,'One entire deep upper saddle rooted in the boiler crown and carrying the small complete cylinder.')
join('WholeUpperEngineSaddle','WholeHorizontalBoilerExterior',(0,-.84,1.62))
G['WholeTopCylinderAndCovers']=axial([(0,-1.18),(.16,-1.18),(.16,-1.12),(.135,-1.12),(.135,-.67),(.16,-.67),(.16,-.61),(0,-.61)],(0,0,1.96),(1,0,0),(0,0,1),(0,1,0),20,3,'One entire small top-mounted closed cylinder and stepped full cover ends. No piston interior or pressure system is claimed.')
join('WholeTopCylinderAndCovers','WholeUpperEngineSaddle',(0,-.85,1.85))
cyl('WholeTopPistonRod',(0,-.65,1.96),(0,-.18,1.96),.044,3,'One continuous fixed rod projecting from the top cylinder into the full crosshead block. No stroke or slide performance.',16)
join('WholeTopPistonRod','WholeTopCylinderAndCovers',(0,-.63,1.96))
G['WholeUpperCrossheadBlock']=block((-.115,-.30,1.89),(.115,-.16,2.03),3,'One complete fixed crosshead block, with upper and lower empty guide clearances; illustrative rather than a moving fit.')
join('WholeUpperCrossheadBlock','WholeTopPistonRod',(0,-.23,1.96))
G['WholeTopGuideSupport']=solid_union([((-.23,-.53,1.57),(.23,-.45,1.86)),((-.23,.03,1.57),(.23,.11,1.86)),((-.23,-.53,1.80),(-.14,.11,1.91)),((.14,-.53,1.80),(.23,.11,1.91))],2,'One complete two-end support with two longitudinal guide rails rooted into the boiler crown. The crosshead sits between real open rails without an enclosing toy cab.')
join('WholeTopGuideSupport','WholeHorizontalBoilerExterior',(.17,-.49,1.64))
# Rear transverse crank shaft and two entire support towers meet the firebox shoulders.
for side,sgn in [('Near',-1),('Far',1)]:
 n=side+'WholeCrankBearingTower';G[n]=block((sgn*.32-.06,.28,1.63),(sgn*.32+.06,.46,2.00),2,'One complete upper bearing-tower appearance, with its full root embedded in the rear boiler/firebox shoulder. No bearing clearance or rotation asserted.')
 join(n,'WholeRearUprightFirebox',(sgn*.32,.39,1.71))
cyl('WholeUpperTransverseCrankshaft',(-.86,.37,1.96),(.49,.37,1.96),.066,3,'One complete upper transverse shaft, held by both upper supports and ending in the side flywheel hub.',20)
for side,sgn in [('Near',-1),('Far',1)]:join('WholeUpperTransverseCrankshaft',side+'WholeCrankBearingTower',(sgn*.32,.37,1.96))
G['WholeSideCrankDisk']=axial([(0,-.18),(.23,-.18),(.23,-.10),(0,-.10)],(0,.37,1.96),(0,1,0),(0,0,1),(1,0,0),24,0,'One whole fixed crank disk on the upper shaft. A separate offset pin and long diagonal rod are visible; phase is an illustrative static arrangement.')
join('WholeSideCrankDisk','WholeUpperTransverseCrankshaft',(-.14,.37,1.96))
for lab,y,z,r in [('Crosshead',-.23,1.96,.040),('OffsetCrank',.30,2.125,.042)]:
 cyl(lab+'WholePin',(-.29,y,z),(.07,y,z),r,3,'One full fixed pin linking the visible long top connecting rod to its named complete endpoint. No moving joint or retention performance.',16)
 join(lab+'WholePin','WholeUpperCrossheadBlock'if lab=='Crosshead'else'WholeSideCrankDisk',(-.06 if lab=='Crosshead'else-.14,y,z))
G['WholeTopInclinedConnectingRod']=beam((-.245,-.23,1.96),(-.245,.30,2.125),.068,.075,3,'One whole inclined fixed connecting rod from the crosshead pin to the offset crank pin, with intentionally embedded closed ends. Not an imported bench rod or operating linkage.')
for lab,y,z in [('Crosshead',-.23,1.96),('OffsetCrank',.30,2.125)]:join('WholeTopInclinedConnectingRod',lab+'WholePin',(-.245,y+(.01 if lab=='Crosshead'else-.01),z+(.003 if lab=='Crosshead'else-.003)))
G['WholeSideOpenSpokeFlywheel']=road_wheel(-.84,-.74,.37,1.96,.52,24,6,0)
join('WholeSideOpenSpokeFlywheel','WholeUpperTransverseCrankshaft',(-.79,.37,1.96))
# Rear empty operator space: a low U rail and a full steering-column appearance.
G['WholeRearPlatformGuard']=solid_union([((-.65,1.02,.71),(-.58,1.72,1.27)),((.58,1.02,.71),(.65,1.72,1.27)),((-.65,1.63,1.18),(.65,1.72,1.31))],0,'One whole low three-sided guard around the rear footplate, with an open upper operator space. The sides are thick plain panels; no occupancy, fall protection or load claim.')
join('WholeRearPlatformGuard','WholeLongChassisAndRearFootplate',(-.61,1.30,.73))
cyl('WholeRearSteeringColumn',(.40,1.20,.70),(.40,1.20,1.68),.035,3,'One complete fixed upright steering-column appearance rooted into the rear footplate. It is not linked to an actual movable front axle.',16)
join('WholeRearSteeringColumn','WholeLongChassisAndRearFootplate',(.40,1.20,.73))
G['WholeOpenSteeringWheel']=axial([(.16,1.66),(.19,1.66),(.19,1.71),(.16,1.71)],(.40,1.20,0),(1,0,0),(0,1,0),(0,0,1),24,2,'One full small thick steering rim with a genuine central opening, fixed horizontally above the platform.')
for j in range(3):
 a=math.tau*j/3;u=(math.cos(a),math.sin(a),0);n='WholeSteeringSpoke'+str(j)
 G[n]=beam(add((.40,1.20,1.685),mul(u,.012)),add((.40,1.20,1.685),mul(u,.18)),.025,.026,2,'One entire fixed rim-to-column spoke, with both hidden ends embedded rather than coplanar caps.')
 join(n,'WholeRearSteeringColumn',add((.40,1.20,1.674),mul(u,.02)));join(n,'WholeOpenSteeringWheel',add((.40,1.20,1.685),mul(u,.17)))
AIR_POINTS=[(0,-1.69,2.57),(0,1.38,1.05),(-.79,.37+.29,1.96+.18),(.82,-1.58+.27,FRONTZ+.17),(-1.00,1+.43,REARZ+.35),(.10,-.37,1.96)]
vv=[v for g in G.values()for v in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='transport-fixed-open-spoke-and-top-drive-steam-traction-engine-01';VERSION='1.0.0';TITLE='Fixed Open Spoke and Top Drive Steam Traction Engine'
DESCRIPTION='One newly authored complete steam-road-traction-engine-style static exterior. A small-wheel front crossframe and large open-spoke rear driving-wheel pair support a long narrow chassis and an open rear footplate. A complete horizontal boiler exterior with integral bands joins a separate upright rear firebox; a tall blind hollow flared front stack rises from its crown. A complete top-mounted cylinder, fixed piston rod and crosshead, open two-rail guides, separate inclined connecting rod, offset crank pin and transverse shaft meet a full open-spoke side flywheel. Rear guard panels and one entire fixed steering-column/rim assembly complete the open operator area. Every road wheel has a connected shared hub, spokes and rim with genuine clear openings and a full finite ground facet. The whole front crossframe, rear firebox/footplate and elevated engine arrangement is newly authored together, not a toy railway locomotive resized or given fewer wheels, and not a pre-existing bench engine placed on a cart. No prior mesh or machine subassembly is imported. One prop zero scenes, four opaque constant PBR materials, metres/native Z up, front -Y and horizontally bounds-centred whole-wheel-ground datum. Closed boiler and cylinder exteriors only; no internal pressure or combustion system, working gear train, steering linkage, moving bearing fit, cylinder stroke, rolling, steam, towing, traction, output, load rating, fuel, fabrication, operation or safety performance is made or verified. No driver, brand, text or track. Rigging, animation and interaction are not produced.'
PALETTE=[('WholeOpenWheelsAndGuard_DeepOxide',(.32,.065,.042,1),.66,.28),('WholeBoilerAndFirebox_DeepGreen',(.060,.18,.115,1),.61,.32),('WholeChassisStackAndGuides_CharcoalSteel',(.040,.055,.060,1),.68,.35),('WholeTopDriveAndControls_WarmSteel',(.46,.38,.23,1),.41,.62)]
FOCUS=(0,0,1.30);ORTHO=5.25
CAMERAS={'thumbnail':(-7.5,-9,5.3),'qa-front':(-7.5,-9,5.3),'qa-side':(-9,0,4),'qa-top':(0,0,10),'qa-back':(7.5,9,5.3),'qa-wireframe':(-7.5,-9,5.3)}
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
root=bpy.data.objects.new('OneWholeOpenSpokeTopDriveSteamTractionEngine',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole four road wheel facets at datum; horizontally centred; one complete static steam road vehicle';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==4272 and len(parts)==31
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
