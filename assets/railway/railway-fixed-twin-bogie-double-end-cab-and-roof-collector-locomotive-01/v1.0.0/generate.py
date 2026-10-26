"""One newly authored complete twin-bogie double-ended rail locomotive exterior. Static art only."""
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
# One entire new twin-bogie, double-ended rail locomotive exterior.
G={};ROOT_WITNESSES=[];AIR_POINTS=[];GROUND=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
def box(n,lo,hi,mat,role):G[n]=block(lo,hi,mat,role)
# Two distinct wheelset frames sit beneath a bridge-like long body, not axles bored through a toy slab.
WZ=.36*math.cos(math.pi/24)
for k,cy in enumerate([-2.22,2.22]):
 bn='WholeIndependentBogieFrame'+str(k)
 G[bn]=solid_union([((-.85,cy-.93,.40),(-.68,cy+.93,.66)),((.68,cy-.93,.40),(.85,cy+.93,.66)),((-.80,cy-.22,.50),(.80,cy+.22,.78))],2,'One complete independent low H-shaped wheelset carrier, with two long outer frame sills and an integral central crossbody. It belongs to this newly authored full locomotive; no old spring-bolster bogie asset or wheel mesh is imported.')
 for j,dy in enumerate([-.65,.65]):
  y=cy+dy;an='WholeBogieCrossAxle'+str(k)+str(j);cyl(an,(-.94,y,WZ),(.94,y,WZ),.095,3,'One entire fixed transverse axle spanning the two whole profiled wheels and reaching both outside frame sills. No rolling, driven axle, bearing fit or track compatibility.',20)
  for lab,s in [('Left',-1),('Right',1)]:
   wn='WholeRailFlangeWheel'+str(k)+str(j)+lab
   G[wn]=axial([(.085,-.125),(.36,-.125),(.36,-.075),(.305,-.075),(.305,.095),(.18,.095),(.18,.135),(.085,.135)],(s*.56,y,WZ),(0,1,0),(0,0,1),(s,0,0),24,[3,3,3,2,3,3,3,3],'One entire profiled wheel with real annular bore, inner flange and outer hub; finite flange ground facet is only a static display datum, not a specified rail interface.',math.pi/24);GROUND.append(wn);join(wn,an,(s*.56,y+.090,WZ))
   xn='WholeAxleEndCarrier'+str(k)+str(j)+lab;lo,hi=sorted([s*.73,s*.93]);box(xn,(lo,y-.14,WZ-.075),(hi,y+.14,.55),2,'One full external axle end carrier, its upper part rooted in the bogie sill and its centre joined to the full fixed axle. Closed exterior, no functional bearing interior.');join(xn,an,(s*.82,y,WZ));join(xn,bn,(s*.79,y,.49))
 pn='WholeBogieBodySeat'+str(k);G[pn]=axial([(0,.72),(.30,.72),(.30,.91),(.22,.91),(.22,1.02),(0,1.02)],(0,cy,0),(1,0,0),(0,1,0),(0,0,1),24,3,'One complete stepped body-seat exterior linking this independent wheelset frame to the long locomotive underbody. Deliberately fixed positive embedding, not a turning bearing or suspension.');join(pn,bn,(0,cy,.75));join(pn,'WholeLongBridgeUnderframe',(0,cy,.97))
G['WholeLongBridgeUnderframe']=solid_union([((-.78,-3.63,.91),(-.54,3.63,1.12)),((.54,-3.63,.91),(.78,3.63,1.12)),((-.76,-2.52,.93),(.76,-1.92,1.14)),((-.76,1.92,.93),(.76,2.52,1.14)),((-.82,-3.62,.95),(.82,-3.32,1.14)),((-.82,3.32,.95),(.82,3.62,1.14))],2,'One entire long bridge underframe with two continuous longitudinal rails, two full bogie-seat crossmembers and complete end ties. This full body is carried across two separated truck frames rather than resting directly on three axles through one low toy chassis.')
box('WholeLongBodyFloor',(-.92,-3.62,1.09),(.92,3.62,1.23),0,'One full continuous locomotive floor and narrow exterior ledge above the bridge frame; no freight deck boards, loaded cargo or old wagon instance.');join('WholeLongBodyFloor','WholeLongBridgeUnderframe',(.65,0,1.105))
G['WholeCentralEquipmentBody']=extrude([(-.80,1.19),(.80,1.19),(.80,2.32),(.64,2.49),(-.64,2.49),(-.80,2.32)],-2.18,2.18,'y',0,'One complete new long equipment-body exterior with upper chamfered shoulders, connecting the two end cab forms. Opaque solid art body, not a fabricated machine interior or a stretched boiler.');join('WholeCentralEquipmentBody','WholeLongBodyFloor',(0,0,1.21))
for lab,s in [('Front',-1),('Rear',1)]:
 cn='WholeSlopingEndCab'+lab;poly=[(s*y,z)for y,z in[(2.08,1.19),(3.60,1.19),(3.60,1.92),(3.28,2.50),(2.08,2.50)]]
 G[cn]=extrude(poly,-.86,.86,'x',0,'One entire sloping-ended cab exterior, structurally continuous through hidden roots with the long central equipment body and whole floor. Two opposite integral cab forms are authored as one complete double-ended locomotive, not separate toy cabins copied onto a wagon. No operator or interior supplied.');join(cn,'WholeCentralEquipmentBody',(0,s*2.13,1.8));join(cn,'WholeLongBodyFloor',(0,s*3.0,1.21))
 for side,t in [('Left',-1),('Right',1)]:
  x0,x1=sorted([t*.845,t*.877]);nn='WholeOpaqueCabSideWindow'+lab+side
  G[nn]=extrude([(s*2.29,1.86),(s*3.13,1.86),(s*3.00,2.34),(s*2.29,2.34)],x0,x1,'x',1,'One entire opaque side glazing appearance with a finite hidden root and proud outer plane. Not transparent glass or a window opening; no cab visibility or human-fit assertion.');join(nn,cn,(t*.85,s*2.6,2.05))
  xa,xb=sorted([t*.055,t*.73]);nn='WholeOpaqueSlantedWindscreen'+lab+side
  yf=lambda z:3.60-(z-1.92)*(.32/.58)
  poly=[(s*(yf(2.01)-.014),2.01),(s*(yf(2.39)-.014),2.39),(s*(yf(2.39)+.017),2.39),(s*(yf(2.01)+.017),2.01)]
  G[nn]=extrude(poly,xa,xb,'x',1,'One entire thick blank windscreen insert following this cab sloped end, with a proud exterior surface and finite buried heel. Two divided panels leave the central body mullion visible; no functioning cab or glass.');join(nn,cn,(t*.40,s*(yf(2.20)-.007),2.20))
 # Two complete end steps and one small blank coupling boss are subordinate fixed exterior pieces.
 en='WholeEndBufferBeam'+lab;box(en,(-.94,s*3.69-.085,1.00),(.94,s*3.69+.085,1.17),2,'One full blunt end beam overlapping the end floor and underframe. Static exterior with no impact, coupling or railway service claim.');join(en,'WholeLongBodyFloor',(0,s*3.615,1.13))
 cou='WholeFixedCouplingBoss'+lab;ya,yb=sorted([s*3.70,s*3.99]);box(cou,(-.13,ya,1.045),(.13,yb,1.15),3,'One whole blunt end coupling-style boss, not an operative knuckle mechanism or compatible coupler.');join(cou,en,(0,s*3.74,1.10))
# New blank side radiator panels add depth without thin coplanar stickers or decals.
for lab,s in [('Left',-1),('Right',1)]:
 xa,xb=sorted([s*.789,s*.825]);nn='WholeLongSideEquipmentPanel'+lab
 G[nn]=extrude([(-1.64,1.50),(1.64,1.50),(1.64,2.15),(-1.64,2.15)],xa,xb,'x',2,'One complete deeply contrasting blank side equipment panel with its rear rooted in the central body and its outer plane proud. No operating grille, heat exchange, louvers or branding.');join(nn,'WholeCentralEquipmentBody',(s*.795,0,1.8))
box('WholeRoofCollectorBase',(-.54,-.92,2.455),(.54,.92,2.61),2,'One full raised roof base for the complete fixed diamond collector-style frame, sunk into the central body roof. No electrical insulation or current collection.');join('WholeRoofCollectorBase','WholeCentralEquipmentBody',(0,0,2.47))
# Complete paired side diamonds and transverse pins; retained fixed pose only.
cyl('WholeLowerCollectorAxis',(-.48,0,2.70),(.48,0,2.70),.064,3,'One full lower transverse axis belongs to the roof frame; fixed and not a moving pivot.',20)
for lab,s in [('Left',-1),('Right',1)]:
 nn='WholeLowerCollectorBearing'+lab;box(nn,(s*.32-.095,-.13,2.58),(s*.32+.095,.13,2.76),2,'Whole low collector bearing cheek embedded in the roof base.');join(nn,'WholeRoofCollectorBase',(s*.32,0,2.60));join(nn,'WholeLowerCollectorAxis',(s*.32,0,2.70))
for e,y in [('Front',-.62),('Rear',.62)]:
 n='WholeOuterCollectorBendAxis'+e;cyl(n,(-.40,y,3.17),(.40,y,3.17),.051,3,'Whole transverse retained bend pin connecting the two sides of the fixed diamond frame, proud beyond arm ends.',16)
cyl('WholeTopCollectorAxis',(-.40,0,3.64),(.40,0,3.64),.052,3,'One full top transverse axis directly under the collector bow, belonging to the same diamond frame.',16)
for lab,s in [('Left',-1),('Right',1)]:
 for end,y in [('Front',-.62),('Rear',.62)]:
  pts=[(s*.30,0,2.70),(s*.30,y,3.17),(s*.30,0,3.64)]
  for j in range(2):
   n='WholeCollectorLink'+lab+end+str(j);G[n]=beam(pts[j],pts[j+1],.075,.055,3,'One full long flat side link of the complete two-sided roof diamond. All links and pins are new, in a single fixed raised pose, not a kinematic or conductive assembly.');join(n,'WholeOuterCollectorBendAxis'+end,add(pts[1],mul(unit(sub(pts[j],pts[1])) if j==0 else unit(sub(pts[2],pts[1])),.018)));join(n,'WholeLowerCollectorAxis'if j==0 else'WholeTopCollectorAxis',add(pts[j if j==0 else 2],mul(unit(sub(pts[1],pts[j if j==0 else 2])),.018)))
G['WholeRaisedCollectorBow']=extrude([(-.87,3.63),(-.72,3.72),(.72,3.72),(.87,3.63),(.80,3.60),(.68,3.655),(-.68,3.655),(-.80,3.60)],-.065,.065,'y',2,'One complete thick shallow transverse bow at the top of the diamond, with downward-blunt end horns and genuine long underside. No overhead wire, contact pressure, power collection or travel.');join('WholeRaisedCollectorBow','WholeTopCollectorAxis',(0,0,3.66))
AIR_POINTS=[(0,0,.43),(0,0,3.16),(.30,0,3.12),(0,-1.40,2.68),(0,1.40,2.68)]
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='railway-fixed-twin-bogie-double-end-cab-and-roof-collector-locomotive-01';VERSION='1.0.0';TITLE='Fixed Twin Bogie Double End Cab and Roof Collector Locomotive'
DESCRIPTION='One wholly newly authored complete double-ended rail-locomotive-style static exterior. Two independent complete low H-shaped wheelset frames each carry two transverse axles and whole profiled flanged wheels. Separate stepped body seats connect these frames beneath one long bridge underframe and a continuous body floor. One central chamfer-shoulder equipment body is joined to two opposing sloped cab exteriors with proud opaque divided windscreens and full side-window inserts. Complete blunt end beams and closed coupling-style bosses belong to both ends. A roof base supports a complete fixed raised two-sided diamond frame: lower bearings and full transverse axis, four whole links per side, two retained outer bend pins, top axis and one complete shallow collector bow. It is not the old short three-bore toy locomotive with extra wheels or a longer boiler, nor the old standalone spring-bolster bogie copied under a wagon. No old mesh or subassembly is imported. All visible coordinates and the long-body/two-frame/paired-cab/roof-frame relationship are new and authored together as one prop, zero scenes. Four opaque constant untextured PBR appearances, native metre game coordinates and Z up; whole horizontal envelope centred above real flange ground facets. Static stylized exterior only: cab and equipment volumes are solid artwork, side panels and glazing opaque, no passengers, driver, engine or electrical interior, rails or wires. No motor, propulsion, current collection, insulation, articulation, steering, suspension, rolling, rail gauge, track or coupling compatibility, human fit, load, manufacturing, installation, railway operation or safety validation. Rigging animation interaction not made or verified.'
PALETTE=[('WholeBodyAndCabs_MutedTerracotta',(.52,.18,.10,1),.58,.22),('WholeOpaqueGlazing_BlueBlack',(.045,.105,.135,1),.42,.22),('WholeFramesPanelsAndRoofBase_DeepGraphite',(.065,.075,.08,1),.59,.38),('WholeWheelsAxlesAndCollector_SatinSteel',(.40,.45,.46,1),.42,.68)]
FOCUS=(0,0,1.70);CAMERAS={'thumbnail':(8.6,-10.4,6.0),'qa-front':(8.6,-10.4,6.0),'qa-side':(12,0,5),'qa-top':(0,0,12),'qa-back':(-8.6,10.4,6),'qa-wireframe':(8.6,-10.4,6)}
fwd=unit(sub(FOCUS,CAMERAS['thumbnail']));right=unit(cross(fwd,(0,0,1)));up=cross(right,fwd);pts=[p for g in G.values()for p in g['vertices']];ORTHO=round(max(max(dot(p,u)for p in pts)-min(dot(p,u)for p in pts)for u in[right,up])*1.22,3)
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
root=bpy.data.objects.new('OneWholeTwinBogieDoubleEndedRailLocomotive',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='eight complete flange soles; horizontal bounds-centred; fixed whole double-ended rail locomotive exterior';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==5384 and len(parts)==59
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
  files[role]={'path':f'assets/railway/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'railway','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
