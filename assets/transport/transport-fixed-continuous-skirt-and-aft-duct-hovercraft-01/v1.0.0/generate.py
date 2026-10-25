"""One whole fixed skirted hovercraft exterior. Static art only, no hovering, navigation or vehicle safety claim."""
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
# Newly authored complete skirted single-duct hovercraft exterior.
ROOT_WITNESSES=[];AIR_POINTS=[];GROUND=['WholeContinuousAnnularSkirt']
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
N=64
def plan(a):
 c=math.cos(a);s=math.sin(a)
 return(.75*math.copysign(abs(c)**.60,c),1.45*math.copysign(abs(s)**.60,s))
# A continuous closed thick skirt material surrounds a real downward-open void.
profile=[(.88,0),(1.00,.085),(1.03,.22),(.98,.38),(.90,.43),(.78,.43),(.73,.18),(.72,0)]
m=Mesh();rings=[[(plan(math.tau*i/N)[0]*scale,plan(math.tau*i/N)[1]*scale,z)for i in range(N)]for scale,z in profile]
for k,a in enumerate(rings):
 b=rings[(k+1)%len(rings)]
 for i in range(N):j=(i+1)%N;m.quad(a[i],a[j],b[j],b[i],0)
G['WholeContinuousAnnularSkirt']=m.result('One complete broad rounded-rectangle annular skirt exterior with a true downward-open central void and full finite annular ground sole. Its flattened lower edge and swollen middle are newly authored, not two old boat floats, a tire or a scaled skiff hull. No inflation, pressure or lift behavior.')
outline=[(plan(math.tau*i/N)[0]*.91,plan(math.tau*i/N)[1]*.91)for i in range(N)]
G['WholeBroadUpperDeck']=extrude(outline,.405,.485,'z',1,'One whole low finite deck spans the open underside of the skirt and supports the cockpit and rear duct assembly. No water, terrain, cushion simulation or detached stage.')
join('WholeBroadUpperDeck','WholeContinuousAnnularSkirt',(.64,0,.420))
# Solid fixed cowl exterior with dark windscreen face as actual surface material,
# not transparent glass, a separately floating overlay or a claimed cabin interior.
p=[(-1.07,.455),(-1.07,.61),(-.64,.975),(-.38,.975),(-.38,.455)]
m=Mesh();xa,xb=-.43,.43
for x in[xa,xb]:
 for f in earclip(p):m.tri([(x,p[i][0],p[i][1])for i in f],1)
for i,(a,b)in enumerate(zip(p,p[1:]+p[:1])):m.quad((xa,*a),(xb,*a),(xb,*b),(xa,*b),0 if i==1 else 1)
G['WholeFrontCowlAndOpaqueWindshield']=m.result('One complete shaped forward cowl with a broad sloping opaque windscreen-style surface and full rear face. Dark glazing appearance is integral material on actual faces, not a transparency or optical claim. The seated cockpit is open behind this solid exterior.')
join('WholeFrontCowlAndOpaqueWindshield','WholeBroadUpperDeck',(0,-.72,.470))
for lab,x in[('Left',-.50),('Right',.50)]:
 poly=[(-.92,.46),(.42,.46),(.42,.60),(.12,.67),(-.60,.67),(-.92,.57)]
 G[lab+'WholeCockpitCoaming']=extrude(poly,x-.045,x+.045,'x',1,'One whole tapered low cockpit side coaming joins the deck, with a genuine open seating interval between the pair.')
 join(lab+'WholeCockpitCoaming','WholeBroadUpperDeck',(x,-.30,.475))
G['WholeSeatPedestal']=block((-.20,-.02,.47),(.20,.30,.60),2,'One complete seat root fixed into the deck.')
G['WholePilotSeatPan']=extrude([(-.29,-.10),(.29,-.10),(.31,-.06),(.31,.32),(.27,.36),(-.27,.36),(-.31,.32),(-.31,-.06)],.575,.655,'z',0,'One entire padded-looking finite seat pan, not a person or loose cushion.')
G['WholePilotSeatBack']=extrude([(.27,.60),(.36,.60),(.47,1.035),(.38,1.055)],-.29,.29,'x',0,'One complete thick inclined seat back fixed to the pan; no human fit or ergonomic claim.')
join('WholeSeatPedestal','WholeBroadUpperDeck',(0,.15,.478));join('WholePilotSeatPan','WholeSeatPedestal',(0,.15,.59));join('WholePilotSeatBack','WholePilotSeatPan',(0,.32,.63))
a=(0,-.405,.685);b=(0,-.125,.90);cyl('WholeFixedSteeringColumn',a,b,.022,2,'One whole fixed steering-column exterior rooted in the rear cowl; no working control.')
join('WholeFixedSteeringColumn','WholeFrontCowlAndOpaqueWindshield',(0,-.397,.691))
w=unit(sub(b,a));u=(1,0,0);v=cross(w,u)
G['WholeOpenSteeringRim']=axial([(.133,-.012),(.153,-.012),(.153,.012),(.133,.012)],b,u,v,w,24,0,'One complete open steering rim with a true central opening; fixed visual only.')
G['WholeSteeringHub']=axial([(0,-.02),(.036,-.02),(.036,.025),(0,.025)],b,u,v,w,20,2,'Whole hub rooted in the column.')
join('WholeSteeringHub','WholeFixedSteeringColumn',add(b,mul(w,-.010)))
for i in range(3):
 d=add(mul(u,math.cos(math.tau*i/3)),mul(v,math.sin(math.tau*i/3)));n='WholeSteeringSpoke_%d'%i
 G[n]=beam(add(b,mul(d,.025)),add(b,mul(d,.143)),.018,.020,2,'One full finite radial steering spoke, part of the single wheel.')
 join(n,'WholeSteeringHub',add(b,mul(d,.030)));join(n,'WholeOpenSteeringRim',add(b,mul(d,.140)))
# New high aft propulsion-duct exterior, not an imported standalone ventilation fan.
C=(0,.86,1.13);U=(1,0,0);V=(0,0,1);W=(0,1,0)
G['WholeAftOpenDuct']=axial([(.55,.18),(.55,-.14),(.60,-.21),(.60,-.24),(.51,-.24),(.49,-.14),(.49,.18)],C,U,V,W,48,3,'One complete thick high rear annular duct with a wide forward lip and real interior. The hub, blades and supports occupy parts of the aperture; not a claimed wholly empty bore or certified guard.')
for lab,x in[('Left',-.32),('Right',.32)]:
 top=(x,.87,.718);base=(x,.87,.47);n=lab+'WholeAftDuctSaddle'
 G[n]=beam(base,top,.080,.085,2,'One entire deck-to-duct saddle; its upper end roots into the lower outside ring material, away from the blade envelope.')
 join(n,'WholeBroadUpperDeck',(x,.87,.478));join(n,'WholeAftOpenDuct',(x,.87,.704))
G['WholeAftMotorAndHub']=axial([(0,-.155),(.145,-.155),(.145,-.08),(.115,-.08),(.115,.235),(0,.235)],C,U,V,W,32,2,'One whole supported central motor-and-hub exterior, without internal motor, drive or operating claims.')
for i in range(3):
 angle=math.tau*(i+.25)/3;d=(math.cos(angle),0,math.sin(angle));n='WholeRearMotorStay_%d'%i
 G[n]=beam(add(add(C,mul(d,.10)),(0,.13,0)),add(add(C,mul(d,.525)),(0,.13,0)),.030,.032,2,'One complete radial rear stator-style support connecting the hub and ring in the same full craft.')
 join(n,'WholeAftMotorAndHub',add(add(C,mul(d,.108)),(0,.13,0)));join(n,'WholeAftOpenDuct',add(add(C,mul(d,.52)),(0,.13,0)))
for i in range(4):
 angle=math.tau*(i+.5)/4;c=math.cos(angle);s=math.sin(angle);m=Mesh()
 # Radial/tangential outline and finite pitched thickness. New whole blades.
 poly=[(.12,-.045),(.26,-.085),(.445,-.075),(.46,.035),(.30,.070),(.12,.055)]
 def pt(p,t):r,q=p;return(C[0]+r*c-q*s,C[1]-.11+.38*q+t,C[2]+r*s+q*c)
 for t in[-.014,.014]:
  for f in earclip(poly):m.tri([pt(poly[j],t)for j in f],2)
 for a,b in zip(poly,poly[1:]+poly[:1]):m.quad(pt(a,-.014),pt(b,-.014),pt(b,.014),pt(a,.014),2)
 n='WholeFixedPitchedBlade_%d'%i;G[n]=m.result('One complete finite-thickness tapered pitched blade, fixed into the whole hub. No thrust, airflow, rotation or protected operating clearance claim.')
 join(n,'WholeAftMotorAndHub',pt((.13,0),0))
# Sparse fixed front grille: its bars intentionally obscure narrow portions only.
G['WholeFrontGrilleCentre']=axial([(0,-.242),(.08,-.242),(.08,-.218),(0,-.218)],C,U,V,W,24,2,'One whole finite front centre carried by four real bars; not a working protective certification.')
for i in range(4):
 angle=math.tau*i/4;d=(math.cos(angle),0,math.sin(angle));n='WholeFrontGrilleBar_%d'%i
 G[n]=beam(add(add(C,mul(d,.068)),(0,-.230,0)),add(add(C,mul(d,.555)),(0,-.230,0)),.017,.019,2,'One entire sparse front grille bar connected to full centre and duct lip.')
 join(n,'WholeFrontGrilleCentre',add(add(C,mul(d,.073)),(0,-.230,0)));join(n,'WholeAftOpenDuct',add(add(C,mul(d,.545)),(0,-.230,0)))
# Complete twin vertical rear vanes and their full carrier, not fins floating behind fan.
G['WholeRearRudderBridge']=block((-.46,1.15,.70),(.46,1.23,.775),2,'One entire low rear crosscarrier for both full upright tail vanes.')
for lab,x in[('Left',-.41),('Right',.41)]:
 n=lab+'WholeRearBridgeRoot';G[n]=block((x-.030,1.15,.47),(x+.030,1.23,.735),2,'One whole deck root for the rear vane crosscarrier.')
 join(n,'WholeBroadUpperDeck',(x,1.18,.478));join(n,'WholeRearRudderBridge',(x,1.19,.723))
for lab,x in[('Left',-.19),('Right',.19)]:
 n=lab+'WholeRearRudderVane';G[n]=extrude([(1.18,.745),(1.38,.80),(1.37,1.51),(1.22,1.57)],x-.018,x+.018,'x',3,'One full thick upright rear rudder-style vane, rooted in the common carrier. Static exterior only, no steering or aerodynamic claim.')
 join(n,'WholeRearRudderBridge',(x,1.205,.764))
AIR_POINTS=[(0,0,.12),(0,-.7,.12),(.30,.55,.15),(0,-.22,.55),(.37,.08,.75),(-.37,.08,.75)]
for a in[math.radians(22.5),math.radians(112.5),math.radians(202.5),math.radians(292.5)]:AIR_POINTS.append(add(C,(.32*math.cos(a),-.23,.32*math.sin(a))))
AIR_POINTS +=[(0,1.32,1.20),(.35,.66,1.13),(-.35,.66,1.13)]
vv=[v for g in G.values()for v in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='transport-fixed-continuous-skirt-and-aft-duct-hovercraft-01';VERSION='1.0.0';TITLE='Fixed Continuous Skirt and Aft Duct Hovercraft'
DESCRIPTION='One newly authored whole static small hovercraft-style exterior. A broad continuous rounded-rectangle annular skirt has a swollen outer profile, finite lower annular sole and true downward-open centre under one complete deck. A shaped forward cowl with integral opaque windscreen-style face, two full side coamings, one complete seated pilot station and open steering wheel define the cockpit. At the rear, two deck saddles carry one whole flared thick duct, a supported central motor-and-hub exterior, four complete fixed pitched blades and a sparse four-bar front grille. Two full vertical rear vane exteriors join a complete lower carrier and deck roots. All geometry is independently authored, not a work skiff with an imported mine fan, twin old floats with wheels removed, a count or color variant, or an existing boat scene. The thick skirt and deck enclose an open underside rather than a sealed flotation hull. One model, zero scenes; four opaque constant untextured PBR roles, metres, Z up and whole horizontally bounds-centred ground origin on the skirt sole. Opaque windscreen appearance does not supply cabin glazing, light transmission or a hidden enclosed cabin. No occupant, water, cushion field, external hose, motor internals, rigging, animation or interaction. Fixed illustrative game art only: no buoyancy, hovering, inflation, thrust, airflow, propulsion, steering, control response, blade-guard safety, occupancy fit, stability, load, manufacture or real vehicle operation and safety claim.'
PALETTE=[('WholeSkirtSeatAndOpaqueScreen_Charcoal',(.045,.060,.065,1),.72,.08),('WholeDeckAndCowl_WarmOchre',(.60,.33,.10,1),.63,.12),('WholeSupportsAndRotor_SatinSteel',(.38,.45,.46,1),.43,.60),('WholeDuctAndTail_DeepPetrol',(.055,.25,.27,1),.56,.32)]
FOCUS=(0,0,.72);ORTHO=3.65
CAMERAS={'thumbnail':(4.5,-6,4.4),'qa-front':(4.2,-6,3.6),'qa-side':(5,0,3),'qa-top':(0,0,6),'qa-back':(-3,5,3),'qa-wireframe':(4.5,-6,4.4)}
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
root=bpy.data.objects.new('OneWholeFixedSkirtAndAftDuctHovercraft',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole annular skirt sole at datum; full horizontal bounds centred; complete fixed skirted hovercraft exterior';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==3060 and len(parts)==35
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
