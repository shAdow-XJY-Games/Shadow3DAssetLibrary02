"""One newly authored complete high-body centre-drum rising-belt road-milling-machine exterior. Static art only."""
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
# Complete new high-body centre-drum / forward-belt road machine; static art only.
ROOT_WITNESSES=[];AIR_POINTS=[];GROUND=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
def track(x,y):
 o=[(-.61,.16),(-.46,0),(.46,0),(.61,.16),(.61,.43),(.46,.59),(-.46,.59),(-.61,.43)];i=[(-.48,.20),(-.40,.12),(.40,.12),(.48,.20),(.48,.39),(.40,.47),(-.40,.47),(-.48,.39)];m=Mesh()
 for xx in[x-.20,x+.20]:
  for j in range(8):k=(j+1)%8;m.quad((xx,o[j][0]+y,o[j][1]),(xx,o[k][0]+y,o[k][1]),(xx,i[k][0]+y,i[k][1]),(xx,i[j][0]+y,i[j][1]),2)
 for pp in[o,i]:
  for j in range(8):k=(j+1)%8;m.quad((x-.20,pp[j][0]+y,pp[j][1]),(x+.20,pp[j][0]+y,pp[j][1]),(x+.20,pp[k][0]+y,pp[k][1]),(x-.20,pp[k][0]+y,pp[k][1]),2)
 return m.result('One full independent short crawler unit with genuine central aperture and a full flat ground sole, belonging to the new high four-station machine; no moving links, suspension or capacity claim.')
for side,x in[('Left',-1.08),('Right',1.08)]:
 for end,y in[('Front',-1.38),('Rear',1.61)]:
  tag=side+end;n='Whole'+tag+'Track';G[n]=track(x,y);GROUND.append(n)
  for k,dy in enumerate([-.34,.34]):
   name='Whole'+tag+'Roller'+str(k);cyl(name,(x-.18,y+dy,.295),(x+.18,y+dy,.295),.20,1,'One complete crawler end roller with hidden positive belt overlap and a proud axial span.',20);join(name,n,(x,y+dy,.105))
  n='Whole'+tag+'InnerBeam';G[n]=block((x-.10,y-.39,.26),(x+.10,y+.39,.49),1,'One complete internal track-carrier beam crossing the two whole roller cores.')
  for k,dy in enumerate([-.34,.34]):join(n,'Whole'+tag+'Roller'+str(k),(x,y+dy,.34))
  n='Whole'+tag+'VerticalSupport';cyl(n,(x,y,.40),(x,y,1.45),.115,3,'One whole fixed upright track-carrier support joins the separate lower crawler station to the high vehicle body. No actual lift/steering system or hydraulics.',20);join(n,'Whole'+tag+'InnerBeam',(x,y,.44))
G['WholeHighLongChassis']=extrude([(-1.29,-1.73),(1.29,-1.73),(1.29,1.94),(1.05,2.20),(-1.05,2.20),(-1.29,1.94)],1.18,1.58,'z',0,'One entire long high chassis spanning four separated crawler supports, leaving a genuine central-underbody drum space. It is not the low two-track front-hopper paver chassis.')
for side,x in[('Left',-1.08),('Right',1.08)]:
 for end,y in[('Front',-1.38),('Rear',1.61)]:join('WholeHighLongChassis','Whole'+side+end+'VerticalSupport',(x,y,1.35))
G['WholeRearPowerHousing']=extrude([(.30,1.52),(2.12,1.52),(2.12,2.30),(1.88,2.48),(.55,2.48),(.30,2.25)],-.94,.94,'x',0,'One whole high rear power-cover exterior with sloped shoulders and a clear forward operator station. No engine, exhaust or drive internals.');join('WholeRearPowerHousing','WholeHighLongChassis',(0,1.1,1.55))
# Entire transverse bottom-open drum canopy, not a closed painted black underside.
p=[(-.69,.15),(-.69,.82),(-.46,1.08),(.46,1.08),(.69,.82),(.69,.15),(.56,.15),(.56,.77),(.40,.94),(-.40,.94),(-.56,.77),(-.56,.15)]
G['WholeBottomOpenDrumCanopy']=extrude(p,-1.00,1.00,'x',0,'One continuous thick inverted-U drum canopy with an actual open lower space and sloped upper corners. The complete transverse blunt drum sits inside, not an extra front bucket or rear screed.')
for side,x in[('Left',-.91),('Right',.91)]:
 n='Whole'+side+'DrumSuspension';G[n]=block((x-.08,-.34,.91),(x+.08,.34,1.29),1,'One complete short suspension plate roots the central canopy to the underside of the long chassis. Fixed static attachment only.');join(n,'WholeHighLongChassis',(x,0,1.23));join(n,'WholeBottomOpenDrumCanopy',(x,0,1.00))
cyl('WholeCentralDrumAxle',(-1.13,0,.50),(1.13,0,.50),.075,3,'One entire transverse drum axle crossing the complete wide blunt drum and both exterior side bearing plates.',24)
for side,x in[('Left',-1.025),('Right',1.025)]:
 n='Whole'+side+'DrumEndPlate';G[n]=extrude([(-.53,.29),(.53,.29),(.53,.78),(.34,.98),(-.34,.98),(-.53,.78)],x-.055,x+.055,'x',1,'One complete outer drum bearing plate, deliberately proud of the canopy end plane; neither exposed cap is coplanar with the canopy side.');join(n,'WholeBottomOpenDrumCanopy',((-0.985 if x<0 else .985),0,.96));join(n,'WholeCentralDrumAxle',(x,0,.50))
# Closed fully rooted faceted drum with modest integral broad longitudinal ridges.
m=Mesh();rings=[];N=40
for x in[-.96,.96]:rings.append([(x,r*math.cos(j*math.tau/N),.50+r*math.sin(j*math.tau/N))for j in range(N)for r in[.405 if j%5 in[1,2]else .37]])
for x,row in zip([-.96,.96],rings):
 for j in range(N):k=(j+1)%N;m.tri([(x,0,.50),row[j],row[k]],2)
for j in range(N):k=(j+1)%N;m.quad(rings[0][j],rings[0][k],rings[1][k],rings[1][j],2)
G['WholeBluntTransverseMillingDrum']=m.result('One entire wide transverse thick drum with integral broad blunt longitudinal ridge variations. It has no separate teeth, tool holders or sharp edges and makes no cutting claim. The lower drum remains above the ground datum.');join('WholeBluntTransverseMillingDrum','WholeCentralDrumAxle',(0,0,.50))
# New front operator deck and open canopy frame, no grain box or gathering reel.
G['WholeForwardOperatorDeck']=block((-1.00,-1.62,1.55),(1.00,.36,1.72),1,'One entire forward open operator-platform exterior joining the chassis and rear cover, with space on both sides of its single fixed seat.');join('WholeForwardOperatorDeck','WholeHighLongChassis',(0,-.6,1.565))
G['WholeFixedOperatorSeat']=solid_union([((-.31,-.37,1.70),(.31,.18,2.03)),((-.31,.10,2.00),(.31,.23,2.42))],2,'One full fixed seat-shaped exterior on the high front platform, no person or ergonomic standard.');join('WholeFixedOperatorSeat','WholeForwardOperatorDeck',(0,-.1,1.71))
G['WholeBlankForwardConsole']=extrude([(-1.31,1.69),(-1.05,1.69),(-1.05,2.26),(-1.31,2.37)],-.52,.52,'x',0,'One complete blank inclined control pedestal ahead of the seat, separated by a real empty foot space. No instruments or functioning controls.');join('WholeBlankForwardConsole','WholeForwardOperatorDeck',(0,-1.2,1.71))
for side,x in[('Left',-.92),('Right',.92)]:
 n='Whole'+side+'OpenStationRail';G[n]=extrude([(-1.49,1.69),(-1.49,2.48),(.16,2.48),(.16,1.69),(.09,1.69),(.09,2.41),(-1.42,2.41),(-1.42,1.69)],x-.035,x+.035,'x',3,'One full U-shaped station side rail with two complete rooted posts and a clear interior gap, not an engineering protective barrier.');join(n,'WholeForwardOperatorDeck',(x,-1.455,1.705))
# Two complete newly authored forward conveyors, fixed and empty.
def conveyor(tag,a,b,width,r):
 w=unit(sub(b,a));u=(1,0,0);v=cross(w,u);h=math.sqrt(dot(sub(b,a),sub(b,a)));outer=[];inner=[]
 for c,t0 in[(0,math.pi/2),(h,3*math.pi/2)]:
  for j in range(9):
   t=t0+j*math.pi/8;outer.append((c+r*math.cos(t),r*math.sin(t)));inner.append((c+(r-.045)*math.cos(t),(r-.045)*math.sin(t)))
 m=Mesh();p=lambda x,q:add(a,add(mul(u,x),add(mul(w,q[0]),mul(v,q[1]))))
 for j in range(len(outer)):
  k=(j+1)%len(outer)
  for x in[-width/2,width/2]:m.quad(p(x,outer[j]),p(x,outer[k]),p(x,inner[k]),p(x,inner[j]),2)
  m.quad(p(-width/2,outer[j]),p(width/2,outer[j]),p(width/2,outer[k]),p(-width/2,outer[k]),2)
  m.quad(p(-width/2,inner[j]),p(-width/2,inner[k]),p(width/2,inner[k]),p(width/2,inner[j]),2)
 n='Whole'+tag+'ClosedBelt';G[n]=m.result('One complete thick continuous empty conveyor-belt exterior, full upper/lower runs and rounded returns. It is not the previous open grain tube or broad receiving hopper; no conveying, drive or material-flow promise.')
 for k,p0 in enumerate([a,b]):
  nn='Whole'+tag+'EndRoller'+str(k);cyl(nn,add(p0,(-width/2-.035,0,0)),add(p0,(width/2+.035,0,0)),r-.035,1,'One whole belt return roller with hidden positive overlap at both complete end returns.',24);join(nn,n,add(p0,mul(v,r-.040)))
 for side,x in[('Left',-width/2-.055),('Right',width/2+.055)]:
  nn='Whole'+tag+side+'SideBeam';G[nn]=beam(add(a,(x,0,0)),add(b,(x,0,0)),.11,.13,0,'One full continuous side carrier beam between the two whole end rollers, supporting the empty belt appearance without floating bars.');join(nn,'Whole'+tag+'EndRoller0',add(a,add(mul(w,.03),((1 if x>0 else -1)*(width/2+.015),0,0))))
 return n
primary=conveyor('PrimaryTransfer',(0,-.30,.62),(0,-1.96,1.18),.63,.14);join(primary,'WholeBottomOpenDrumCanopy',(0,-.635,.865))
secondary=conveyor('RisingDischarge',(0,-1.93,1.48),(0,-5.08,3.08),.70,.17)
G['WholeFrontConveyorYoke']=solid_union([((-.52,-1.99,1.10),(.52,-1.57,1.29)),((-.52,-2.02,1.19),(-.39,-1.70,1.62)),((.39,-2.02,1.19),(.52,-1.70,1.62))],1,'One complete forward fork yoke rooted into the chassis, carrying the higher second belt stage above the first return with a genuine transfer gap.');join('WholeFrontConveyorYoke','WholeHighLongChassis',(0,-1.66,1.235))
cyl('WholeDischargeRootCrossPin',(-.55,-1.93,1.48),(.55,-1.93,1.48),.07,3,'One complete transverse static conveyor-root pin joins the two yoke cheeks and the whole lower return roller.',20);join('WholeDischargeRootCrossPin','WholeFrontConveyorYoke',(.46,-1.93,1.48));join('WholeDischargeRootCrossPin','WholeRisingDischargeEndRoller0',(0,-1.93,1.48))
for side,x in[('Left',-.42),('Right',.42)]:
 n='Whole'+side+'ConveyorDiagonalStay';a=(x,-1.52,1.35);b=(x,-3.02,2.034);G[n]=beam(a,b,.075,.085,3,'One entire diagonal static stay from the front chassis to the complete long side carrier of the rising conveyor, no hydraulic, load or motion capability.');join(n,'WholeHighLongChassis',(x,-1.57,1.373));join(n,'WholeRisingDischarge'+side+'SideBeam',(x,-3.0,2.027))
AIR_POINTS=[(0,-.72,1.96),(.6,-.55,2.15),(0,.42,.13),(0,-3.3,1.0),(0,-2.12,1.34)]
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='construction-fixed-underbody-drum-and-rising-belt-road-miller-01';VERSION='1.0.0';TITLE='Fixed Underbody Drum and Rising Belt Road Miller'
DESCRIPTION='One newly authored complete road-milling-machine-style static exterior. A high long body stands on four separated short crawler units and whole fixed upright carrier posts. A complete wide blunt transverse drum occupies a genuine bottom-open thick canopy under the middle of the chassis, visibly separate from the tracks. An entire low primary belt rises forward from this lower region to a second much longer elevated discharge belt; both have full continuous upper and lower runs, complete end rollers, side beams and proper root yoke/stays. A forward high open platform with a fixed seat, blank console and rooted side rails lies ahead of the shouldered power cover. Unlike the old paver, there is no wide front receiving hopper or rear screed; unlike the combine, no forward harvesting reel/header, upper grain box or bent discharge tube; unlike the compact trencher, no downward cutting-chain boom or rear standing control station. Every visible profile and machine layout newly authored, with no old product mesh imported or scaled. Four opaque constant PBR materials, metres, Z up, centred full horizontal envelope and four full finite track soles. One prop zero scenes. No sharp teeth, pavement or workpiece. Static game-art exterior only: no milling, conveyor flow, crawler motion, steering, hydraulics, engine, lift, capacity, ergonomics, manufacture, assembly, protective or safety performance. Rigging, animation and interaction are not made or verified.'
PALETTE=[('WholeHighBodyAndBeltRails_MutedTeal',(.075,.30,.32,1),.66,.21),('WholePlatformDrumEndsAndRollers_LightSteel',(.49,.56,.55,1),.48,.54),('WholeTracksBeltsAndDrum_DarkGraphite',(.05,.065,.07,1),.79,.12),('WholePostsPinsAndStays_WarmSteel',(.39,.31,.16,1),.50,.55)]
FOCUS=(0,0,1.43);ORTHO=8.9
CAMERAS={'thumbnail':(8,-10,6.6),'qa-front':(8,-10,6.3),'qa-side':(12,0,5),'qa-top':(0,0,13),'qa-back':(-8,11,6),'qa-wireframe':(8,-10,6.6)}
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
root=bpy.data.objects.new('OneWholeHighBodyCentreDrumRisingBeltRoadMiller',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole four crawler soles at datum; horizontally centred; one complete static road-milling-machine exterior';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==2728 and len(parts)==48
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
