"""New complete fixed twin-cylinder horizontal-tank compressor appearance. Static art only; no pressure, operation, engineering or safety claim."""
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


# One complete newly authored fixed receiver-trolley compressor appearance.
G={};GROUND=[];ROOT_WITNESSES=[];AIR_POINTS=[]
def box(name,lo,hi,mat,role):G[name]=block(lo,hi,mat,role)
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
def cylinder(name,a,b,r,mat,role,n=16):
 w=unit(sub(b,a));ref=(0,0,1)if abs(w[2])<.9 else(0,1,0);u=unit(cross(w,ref));v=cross(w,u);length=math.sqrt(dot(sub(b,a),sub(b,a)))
 G[name]=axial([(0,0),(r,0),(r,length),(0,length)],a,u,v,w,n,mat,role)
def solid_path(points,r,mat,role,n=12):
 m=Mesh();rows=[]
 for i,p in enumerate(points):
  w=unit(sub(points[min(i+1,len(points)-1)],points[max(0,i-1)]));ref=(0,0,1)if abs(w[2])<.90 else(0,1,0);u=unit(cross(w,ref));v=cross(w,u)
  rows.append([add(p,add(mul(u,r*math.cos(j*math.tau/n)),mul(v,r*math.sin(j*math.tau/n))))for j in range(n)])
 for j in range(n):
  k=(j+1)%n;m.tri([points[0],rows[0][k],rows[0][j]],mat);m.tri([points[-1],rows[-1][j],rows[-1][k]],mat)
  for a,b in zip(rows,rows[1:]):m.quad(a[j],a[k],b[k],b[j],mat)
 return m.result(role)
# Low whole trolley, two finite rear soles and two grounded front wheels.
for label,y in [('Near',-.13),('Far',.13)]:
 n='WholeLowChassisRail'+label;box(n,(-.44,y-.022,.05),(.45,y+.022,.085),2,'One entire low longitudinal trolley rail, independent of the tank exterior.')
 foot='WholeRearGroundFoot'+label;box(foot,(-.395,y-.047,0),(-.305,y+.047,.063),2,'One whole finite rear standing foot, no castor or unspecified support.');GROUND.append(foot);join(foot,n,(-.35,y,.058))
for k,x in enumerate([-.35,.35]):
 n='WholeChassisCrossmember'+str(k);box(n,(x-.025,-.145,.055),(x+.025,.145,.082),2,'One complete transverse chassis crossmember.')
 for label,y in [('Near',-.13),('Far',.13)]:join(n,'WholeLowChassisRail'+label,(x,y,.07))
cylinder('WholeFrontAxle',(.35,-.282,.12),(.35,.282,.12),.019,1,'One whole fixed front axle carried by two full chassis bearing blocks.')
for label,y in [('Near',-.13),('Far',.13)]:
 n='WholeAxleBearingBlock'+label;box(n,(.315,y-.030,.07),(.385,y+.030,.152),2,'One entire bearing-block appearance rooted onto the low rail and enclosing its fixed axle.');join(n,'WholeLowChassisRail'+label,(.35,y,.078));join(n,'WholeFrontAxle',(.35,y,.12))
for label,y in [('Near',-.24),('Far',.24)]:
 n='WholeFrontTire'+label;G[n]=axial([(.035,-.025),(.12/math.cos(math.pi/16),-.025),(.12/math.cos(math.pi/16),.025),(.035,.025)],(.35,y,.12),(1,0,0),(0,0,1),(0,-1,0),16,2,'One whole open-bore tire with a true finite flat ground facet, fixed no wheel physics.',phase=math.pi/16);GROUND.append(n)
 cylinder('WholeFrontHub'+label,(.35,y-.027,.12),(.35,y+.027,.12),.036,1,'One entire fixed wheel hub, its end faces offset from the tire faces to avoid coplanarity.');join('WholeFrontHub'+label,n,(.35,y,.1555));join('WholeFrontHub'+label,'WholeFrontAxle',(.35,y,.12))
# Whole rounded receiver-like solid exterior, not a rotated cutaway boiler or tanker instance.
tank_profile=[(0,-.58),(.085,-.55),(.145,-.49),(.18,-.42),(.19,-.35),(.19,.35),(.18,.42),(.145,.49),(.085,.55),(0,.58)]
G['WholeDomedHorizontalTankExterior']=axial(tank_profile,(0,0,.27),(0,1,0),(0,0,1),(1,0,0),32,0,'One continuous rounded horizontal solid tank exterior, without pressure interior, fluid capacity, joints or fabrication specification.')
for k,x in enumerate([-.25,.25]):
 top=[(y,.27-math.sqrt(.19*.19-y*y)+.009)for y in[.16-.32*i/16 for i in range(17)]];poly=[(-.17,.065),(.17,.065),(.17,.18),(.16,.18)]+top+[(-.16,.18),(-.17,.18)]
 n='WholeCurvedTankSaddle'+str(k);G[n]=extrude(poly,x-.045,x+.045,'x',2,'One continuous curved lower tank saddle, with small intentional fixed embedding into the tank and both rails.')
 for label,y in [('Near',-.13),('Far',.13)]:join(n,'WholeLowChassisRail'+label,(x,y,.075))
 join(n,'WholeDomedHorizontalTankExterior',(x,0,.085))
# Raised whole top bed roots two separate drive bodies into the receiver exterior.
box('WholeUpperMountingBed',(-.35,-.13,.455),(.38,.13,.485),2,'One complete top mounting bed carries separate motor and crankcase, rooted in the tank top rather than floating beside it.');join('WholeUpperMountingBed','WholeDomedHorizontalTankExterior',(0,0,.458))
box('WholeMotorFoot',(-.29,-.085,.475),(-.15,.085,.515),1,'One whole broad motor foot rooted to the upper bed.');join('WholeMotorFoot','WholeUpperMountingBed',(-.22,0,.48))
cylinder('WholeMotorCasing',(-.22,-.13,.56),(-.22,.13,.56),.075,2,'One complete separate horizontal motor exterior; closed and unpowered, no wiring or electrical capability.',24);join('WholeMotorCasing','WholeMotorFoot',(-.22,0,.505))
G['WholePumpCrankcase']=extrude([(.08,.475),(.32,.475),(.32,.61),(.285,.65),(.115,.65),(.08,.61)],-.09,.09,'y',1,'One complete shouldered crankcase exterior on the upper bed, distinct from the motor casing and from a volute casing.');join('WholePumpCrankcase','WholeUpperMountingBed',(.20,0,.48))
# Two inclined closed finned barrels: every rib is part of its whole barrel material shell.
for label,a,b in [('Left',(.16,0,.615),(.04,0,.795)),('Right',(.24,0,.615),(.36,0,.795))]:
 w=unit(sub(b,a));length=math.sqrt(dot(sub(b,a),sub(b,a)));u=(0,1,0);v=cross(w,u);profile=[(0,0),(.052,0)]
 for t in[.025,.057,.089,.121,.153]:profile +=[(.052,t),(.073,t),(.073,t+.009),(.052,t+.009)]
 profile +=[(.052,length), (0,length)]
 n='WholeFinnedCylinder'+label;G[n]=axial(profile,a,u,v,w,20,1,'One complete inclined cylinder-shaped solid with five integral thick cooling-fin appearances and real inter-fin spaces, no hidden piston, gas path or cooling claim.');join(n,'WholePumpCrankcase',add(a,mul(w,.010)))
 head='WholeCylinderHead'+label;G[head]=axial([(0,length-.014),(.080,length-.014),(.080,length+.021),(0,length+.021)],a,u,v,w,20,2,'One whole broad fixed inclined cylinder head cap, rooted onto the complete finned barrel.');join(head,n,add(a,mul(w,length-.007)))
# Whole fixed shafts and visibly separate unequal-size pulleys.
cylinder('WholeMotorShaft',(-.22,-.232,.56),(-.22,-.115,.56),.018,1,'One entire fixed motor shaft roots the small pulley into the motor.');join('WholeMotorShaft','WholeMotorCasing',(-.22,-.12,.56))
cylinder('WholePumpShaft',(.20,-.235,.595),(.20,-.07,.595),.023,1,'One entire fixed pump shaft roots the open-spoke large pulley into the crankcase.');join('WholePumpShaft','WholePumpCrankcase',(.20,-.08,.595))
G['WholeSmallMotorPulley']=axial([(.015,-.219),(.063,-.219),(.063,-.185),(.015,-.185)],(-.22,0,.56),(1,0,0),(0,0,-1),(0,1,0),24,1,'One full small annular motor pulley with a real centre bore occupied by its fixed shaft.')
join('WholeSmallMotorPulley','WholeMotorShaft',(-.204,-.202,.56))
G['WholeLargePulleyRim']=axial([(.105,-.219),(.140,-.219),(.140,-.185),(.105,-.185)],(.20,0,.595),(1,0,0),(0,0,-1),(0,1,0),32,1,'One full large open pulley rim with five real open sectors between its spokes.')
cylinder('WholeLargePulleyHub',(.20,-.225,.595),(.20,-.178,.595),.033,1,'Whole large pulley hub, rooted on the pump shaft.');join('WholeLargePulleyHub','WholePumpShaft',(.20,-.202,.595))
for k in range(5):
 a=k*math.tau/5;dr=(math.cos(a),0,math.sin(a));c=(.20,-.202,.595);n='WholePulleySpoke'+str(k);G[n]=beam(add(c,mul(dr,.020)),add(c,mul(dr,.133)),.040,.015,1,'One whole thick fixed spoke connects hub and rim; axial depth differs from the rim to prevent coplanar joints.');join(n,'WholeLargePulleyHub',add(c,mul(dr,.026)));join(n,'WholeLargePulleyRim',add(c,mul(dr,.124)))
# One closed thick flat belt has two real external tangent runs and two unequal arcs.
c0=(-.22,.56);c1=(.20,.595);r0=.063;r1=.140;dx=c1[0]-c0[0];dz=c1[1]-c0[1];phi=math.atan2(dz,dx);alpha=math.acos((r0-r1)/math.hypot(dx,dz))
def belt_loop(offset):
 return[(c1[0]+(r1+offset)*math.cos(phi-alpha+2*alpha*i/24),c1[1]+(r1+offset)*math.sin(phi-alpha+2*alpha*i/24))for i in range(25)]+[(c0[0]+(r0+offset)*math.cos(phi+alpha+(math.tau-2*alpha)*i/18),c0[1]+(r0+offset)*math.sin(phi+alpha+(math.tau-2*alpha)*i/18))for i in range(19)]
outer=belt_loop(.003);inner=belt_loop(-.003);m=Mesh();N=len(outer)
for i in range(N):
 j=(i+1)%N;of=(outer[i][0],-.210,outer[i][1]);on=(outer[j][0],-.210,outer[j][1]);ob=(outer[i][0],-.194,outer[i][1]);obn=(outer[j][0],-.194,outer[j][1]);if0=(inner[i][0],-.210,inner[i][1]);ifn=(inner[j][0],-.210,inner[j][1]);ib=(inner[i][0],-.194,inner[i][1]);ibn=(inner[j][0],-.194,inner[j][1]);m.quad(of,on,obn,ob,2);m.quad(if0,ib,ibn,ifn,2);m.quad(of,if0,ifn,on,2);m.quad(ob,obn,ibn,ib,2)
G['WholeContinuousFlatDriveBelt']=m.result('One whole continuous thick flat belt exterior around unequal-size pulleys, with real two-run open middle. Fixed illustrative overlap only, not belt tension, speed, engagement or a safe operating arrangement.')
join('WholeContinuousFlatDriveBelt','WholeLargePulleyRim',(.338,-.202,.595));join('WholeContinuousFlatDriveBelt','WholeSmallMotorPulley',(-.281,-.202,.56))
# Whole fixed delivery-tube exterior, not a validated connected fluid circuit.
a=(.36,-.015,.795);b=(.48,-.10,.76);c=(.53,-.10,.52);d=(.48,0,.39);pts=[]
for i in range(15):
 t=i/14;pts.append(tuple((1-t)**3*a[k]+3*(1-t)**2*t*b[k]+3*(1-t)*t*t*c[k]+t**3*d[k]for k in range(3)))
G['WholeCurvedDeliveryTubeExterior']=solid_path(pts,.010,3,'One entire curved solid tube-like delivery exterior joins the right head to the tank shoulder. No bore, working seal, continuous fluid path or pressure claim.');join('WholeCurvedDeliveryTubeExterior','WholeCylinderHeadRight',tuple(.98**3*a[k]+3*.98**2*.02*b[k]+3*.98*.02**2*c[k]+.02**3*d[k]for k in range(3)));join('WholeCurvedDeliveryTubeExterior','WholeDomedHorizontalTankExterior',tuple(.02**3*a[k]+3*.02**2*.98*b[k]+3*.02*.98**2*c[k]+.98**3*d[k]for k in range(3)))
# One continuous open inclined push handle, rooted into both rear chassis rails.
pts=[(-.37,-.13,.075),(-.50,-.20,.24),(-.64,-.20,.63),(-.64,.20,.63),(-.50,.20,.24),(-.37,.13,.075)]
G['WholeOpenPushHandle']=solid_path(pts,.015,2,'One whole open rear push-handle frame on both chassis rails. Its large central aperture and rearward incline are true geometry, not an added icon.')
for label,y in [('Near',-.13),('Far',.13)]:join('WholeOpenPushHandle','WholeLowChassisRail'+label,(-.3705,y,.076))
# A small blank gauge face is subordinate to the full machine construction.
cylinder('WholeGaugeStem',(-.40,-.05,.39),(-.40,-.05,.49),.013,3,'One whole short fixed gauge-stem appearance rooted in the tank shoulder, no pressure connection.');join('WholeGaugeStem','WholeDomedHorizontalTankExterior',(-.40,-.05,.40))
G['WholeBlankGaugeRim']=axial([(.029,-.084),(.041,-.084),(.041,-.05),(.029,-.05)],(-.40,0,.49),(1,0,0),(0,0,-1),(0,1,0),20,1,'One complete small annular gauge bezel, with a real shallow recess and no measurement markings.');join('WholeBlankGaugeRim','WholeGaugeStem',(-.40,-.055,.458))
cylinder('WholeOpaqueBlankGaugeFace',(-.40,-.064,.49),(-.40,-.049,.49),.030,2,'One recessed opaque blank gauge face, no reading, units, lit screen or operation.');join('WholeOpaqueBlankGaugeFace','WholeBlankGaugeRim',(-.3705,-.056,.49))
# Bounded actual-coordinate sample checks, not exhaustive material/air proofs.
AIR_POINTS=[(-.60,0,.40),(0,-.202,.60),(.20+.070*math.cos(math.pi/5),-.202,.595+.070*math.sin(math.pi/5)),(.35,-.19,.18),(.35,.19,.18),(-.40,-.075,.49),(-.02,0,.72)]
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='industrial-fixed-twin-cylinder-horizontal-tank-compressor-01';VERSION='1.0.0';TITLE='Fixed Twin Cylinder Horizontal Tank Compressor'
DESCRIPTION='One newly authored complete portable compressor-style exterior. A whole domed horizontal solid receiver-like tank rests in two full curved saddles on its own low chassis, two flat-grounded front wheels, complete axle/bearing blocks and two finite rear feet. One entire open inclined rear push handle joins both rails. A full upper mounting bed supports a separate motor casing and shouldered crankcase; two inclined complete finned barrel solids with thick independent heads distinguish the pump silhouette. Full shafts carry one small annular pulley and one large five-spoke open pulley, linked by one continuous closed thick flat belt with real unequal curved ends and two tangent runs. One whole curved solid delivery-tube exterior connects a head to the tank shoulder; a small recessed blank gauge is subordinate. All coordinates newly authored, no old truck cab deletion, boiler rotation, volute impeller or imported meshes. One prop, zero scenes; no separately counted tank, motor or accessories. Four opaque constant PBR roles, metres, Z up and true horizontal bounds-centred ground datum. Small fixed material overlaps establish assembly roots. Static illustrative art only: no pressure vessel interior, seals, fluid circuit, capacity, pumping, belt tension or motion, cooling, wiring, electrical operation, structural performance, manufacture, repair or equipment safety claim. The exposed drive is a static display, not a safe operating arrangement.'
PALETTE=[('WholeReceiver_MutedPetrol',(.075,.25,.27,1),.66,.18),('PumpHeadsAndPulleys_SatinAlloy',(.47,.50,.49,1),.43,.58),('FrameMotorAndBelt_Charcoal',(.065,.075,.078,1),.76,.12),('TubeAndGaugeStem_DullCopper',(.48,.25,.11,1),.55,.45)]
FOCUS=(0,0,.42);ORTHO=1.62
CAMERAS={'gray-front3q':(3.5,-5,2.5),'gray-back3q':(-3,5,2.7),'thumbnail':(3.5,-5,2.5),'qa-front':(3.5,-5,2.4),'qa-side':(0,-5,2),'qa-top':(0,0,6),'qa-back':(-3,5,2.5),'qa-wireframe':(3.5,-5,2.5),'silhouette-128-front':(3.5,-5,2.4),'silhouette-128-side':(0,-5,2)}
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
root=bpy.data.objects.new('OneFixedTwinCylinderHorizontalTankCompressor',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='two finite rear feet and two whole wheel facets at Z0; actual bounds centred; whole fixed portable compressor';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==5136 and len(parts)==40
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
  files[role]={'path':f'assets/industrial/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'industrial','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
