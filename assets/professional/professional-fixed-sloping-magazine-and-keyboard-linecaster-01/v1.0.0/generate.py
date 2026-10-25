"""One newly authored complete sloping magazine and keyboard linecaster exterior. Static art, no casting capability."""
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
# Whole newly authored early linecasting-machine-style exterior; generic static art, no real machine reproduction.
ROOT_WITNESSES=[];AIR_POINTS=[];GROUND=['WholeLinecasterGroundBed']
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
bed=[((-.53,-.44,.06),(-.32,.70,.16)),((.32,-.44,.06),(.53,.70,.16)),((-.50,.27,.11),(.50,.48,.22))]
for x in[-.43,.43]:
 for y in[-.33,.57]:bed.append(((x-.125,y-.13,0),(x+.125,y+.13,.10)))
bed=[tuple(tuple(round(c,9)for c in p)for p in b)for b in bed]
G['WholeLinecasterGroundBed']=solid_union(bed,0,'One entire connected cast-like standing-machine base with full side runners, cross-tie and four finite widened ground shoes. It belongs to this one linecaster-style machine, not a separate table or imported typewriter stand.')
sidepoly=[(-.34,.14),(.65,.14),(.65,1.35),(.30,1.35),(.10,1.12),(-.34,1.05)]
for side,x in [('Left',-.40),('Right',.40)]:
 name='WholeRisingSideCasting'+side;G[name]=extrude(sidepoly,x-.04,x+.04,'x',0,'One whole rising standing-machine side casting connects the finite base, low cantilevered keyboard level and high rear magazine supports. The broad central knee and mechanism space remain open between both side castings.')
 join(name,'WholeLinecasterGroundBed',(x,.34,.18))
G['WholeMainCastingCrossTie']=block((-.42,.30,.70),(.42,.48,.82),0,'One full rear cross-tie joins both entire main castings, leaving the lower front knee opening unfilled.')
for x,side in[(-.40,'Left'),(.40,'Right')]:join('WholeMainCastingCrossTie','WholeRisingSideCasting'+side,(x,.38,.76))
G['WholeLowInclinedKeyDeck']=extrude([(-.78,.82),(-.24,.98),(-.24,1.04),(-.78,.88)],-.43,.43,'x',0,'One complete thick forward-inclined cantilevered keyboard deck integrated into the full standing machine. No paper platen, typebar fan or paper carriage is present.')
for x,side in[(-.40,'Left'),(.40,'Right')]:join('WholeLowInclinedKeyDeck','WholeRisingSideCasting'+side,(x,-.28,1.025))
def keytop(y):return .88+(y+.78)*(.16/.54)
for r,y in enumerate([-.72,-.60,-.48,-.36]):
 for k in range(9):
  x=(k-4)*.085;z=keytop(y);name='WholeBlankKey_R%d_C%d'%(r,k)
  G[name]=axial([(0,z-.006),(.010,z-.006),(.010,z+.012),(.027,z+.012),(.027,z+.031),(0,z+.031)],(x,y,0),(1,0,0),(0,1,0),(0,0,1),12,[1,1,1,3,3,3],'One whole fixed blank stemmed key belonging to the shared low machine keyboard. Deliberately simplified count, no letters, character mapping, action or matrix-selection logic.')
  join(name,'WholeLowInclinedKeyDeck',(x,y,z-.003))
# Lower cross-mount and complete inclined matrix-store appearance.
mount=[((-.44,-.035,1.205),(.44,.085,1.285))]
for x in[-.40,.40]:mount.append(((x-.035,.010,1.06),(x+.035,.070,1.25)))
mount=[tuple(tuple(round(c,9)for c in p)for p in b)for b in mount]
G['WholeMagazineLowerMount']=solid_union(mount,0,'One entire low magazine cross-mount on two short integral necks, joining the full side castings and supporting the sloping store. No unsupported high panel.')
for x,side in[(-.40,'Left'),(.40,'Right')]:join('WholeMagazineLowerMount','WholeRisingSideCasting'+side,(x,.04,1.08))
P=(0,.02,1.25);T=unit((0,.53,.80));N=(0,-T[2],T[1]);D=math.hypot(.53,.80)
def pose(x,t,n):return add(P,add((x,0,0),add(mul(T,t),mul(N,n))))
def posed_box(x0,x1,t0,t1,n0,n1,mat,role):
 g=block((x0,t0,n0),(x1,t1,n1),mat,role);g['vertices']=[pose(*v)for v in g['vertices']];return g
G['WholeSlopingMatrixStoreBack']=posed_box(-.39,.39,0,D,-.060,0,2,'One full high sloping thick matrix-magazine-style back panel, rising above the separate lower keyboard. It is a new whole store silhouette, not the typewriter paper guard raised or a desk screen.')
join('WholeSlopingMatrixStoreBack','WholeMagazineLowerMount',pose(0,.015,-.035))
for j,x in enumerate([-.35,-.28,-.21,-.14,-.07,0,.07,.14,.21,.28,.35]):
 name='WholeMagazineChannelRail'+str(j);G[name]=posed_box(x-.007,x+.007,.03,D-.03,-.004,.045,1,'One entire straight finite rail attached through the sloping magazine back. Real shallow open channels separate neighbouring rails. Coarse static organizing appearance, not an exact matrix store, key count or working passage.')
 join(name,'WholeSlopingMatrixStoreBack',pose(x,D/2,-.002))
for side,x in [('Left',-.39),('Right',.39)]:
 name='WholeMagazineSideCheek'+side;G[name]=posed_box(x-.018,x+.018,-.015,D+.015,-.05,.065,0,'One full thick high magazine side cheek, enclosing the outer edge while leaving the channel face open.')
 join(name,'WholeSlopingMatrixStoreBack',pose(x*.98,D/2,-.025))
# A genuine tall open return frame and whole bent upper distribution rail; not a circular printing roller.
returnboxes=[((-.68,.16,1.08),(-.62,.24,2.22)),((-.52,.16,1.08),(-.46,.24,2.22)),((-.68,.16,1.08),(-.38,.24,1.18)),((-.68,.16,2.10),(-.46,.24,2.22))]
G['WholeOpenReturnElevatorFrame']=solid_union(returnboxes,0,'One complete narrow high return-elevator-style frame with a true long central through window, rooted into the left main casting. It is an exterior architectural cue only; no matrices, travel, gripper or return action is implemented.')
join('WholeOpenReturnElevatorFrame','WholeRisingSideCastingLeft',(-.40,.20,1.13))
G['WholeBentTopDistributionRail']=solid_union([((-.69,.45,2.15),(.45,.57,2.23)),((-.69,.18,2.15),(-.45,.57,2.23))],1,'One entire bent top distribution-rail exterior spanning from the high return frame across the upper magazine, with a genuine L-shaped plan, not separate floating bars.')
join('WholeBentTopDistributionRail','WholeOpenReturnElevatorFrame',(-.65,.21,2.18))
G['WholeRightDistributorStandard']=block((.37,.46,1.20),(.43,.56,2.21),0,'One complete right-hand standard supports the opposite end of the top distribution rail from the high rear main casting; fixed not adjustable.')
join('WholeRightDistributorStandard','WholeRisingSideCastingRight',(.40,.51,1.28));join('WholeRightDistributorStandard','WholeBentTopDistributionRail',(.40,.51,2.18))
G['WholeOpenFrontComposingChannel']=extrude([(-.28,1.07),(-.10,1.07),(-.10,1.17),(-.125,1.17),(-.125,1.10),(-.255,1.10),(-.255,1.17),(-.28,1.17)],-.425,.425,'x',1,'One whole shallow transverse open composing-channel-style tray above the key deck and below the magazine. Its interior is empty and genuinely open; no letters, line slug, molten metal or type output.')
for x,side in[(-.40,'Left'),(.40,'Right')]:join('WholeOpenFrontComposingChannel','WholeRisingSideCasting'+side,(x,-.12,1.078))
# Separate side casting-unit exterior and low supported flywheel belong to the same full machine.
G['WholeSideCastingHousing']=axial([(0,.80),(.18,.80),(.20,.86),(.20,1.11),(.16,1.18),(0,1.18)],(.62,.28,0),(1,0,0),(0,1,0),(0,0,1),24,0,'One full closed shouldered side casting-unit housing silhouette attached to the main frame. No pot interior, heater, melt, temperature, pressure, nozzle or hot-metal path is supplied.')
join('WholeSideCastingHousing','WholeRisingSideCastingRight',(.43,.28,.96))
G['WholeSideMoldCaseExterior']=block((.40,-.15,1.04),(.76,.16,1.14),2,'One entire blank low rectangular side mold-case exterior joining the composing station and closed side housing. This is nonfunctional external form, not a casting cavity or usable mould.')
join('WholeSideMoldCaseExterior','WholeSideCastingHousing',(.62,.12,1.10));join('WholeSideMoldCaseExterior','WholeRisingSideCastingRight',(.42,.10,1.08))
cyl('WholeLowDriveAxle',(.37,.45,.49),(.83,.45,.49),.035,1,'One full fixed low transverse shaft from the right main casting to the separate outboard drive wheel.',20)
join('WholeLowDriveAxle','WholeRisingSideCastingRight',(.40,.45,.49))
cyl('WholeDriveWheelHub',(.71,.45,.49),(.79,.45,.49),.075,1,'Whole low side drive-wheel hub seated on the complete shaft, distinct from the upper casting housing.',20)
join('WholeDriveWheelHub','WholeLowDriveAxle',(.75,.45,.49))
G['WholeDriveWheelRim']=axial([(.235,-.028),(.270,-.028),(.270,.028),(.235,.028)],(.75,.45,.49),(0,1,0),(0,0,1),(1,0,0),32,1,'One full open side flywheel rim with a true open annular centre, carried by complete radial spokes. No drive input, rotation, timing or mechanical performance.')
for k,a in enumerate([0,math.pi/2,math.pi,3*math.pi/2]):
 name='WholeDriveWheelSpoke'+str(k);u=(0,math.cos(a),math.sin(a));c=(.75,.45,.49);G[name]=beam(c,add(c,mul(u,.253)),.026,.030,1,'One complete fixed spoke joining the full flywheel hub and annular rim; not a detached radial mark.')
 join(name,'WholeDriveWheelHub',add(c,mul(u,.04)));join(name,'WholeDriveWheelRim',add(c,mul(u,.245)))
AIR_POINTS=[(0,-.47,.50),(-.57,.20,1.65),pose(.035,D/2,.025),(0,-.19,1.14),(.75,.57,.60)]
vv=[v for g in G.values()for v in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='professional-fixed-sloping-magazine-and-keyboard-linecaster-01';VERSION='1.0.0';TITLE='Fixed Sloping Magazine and Keyboard Linecaster'
DESCRIPTION='One newly authored complete generic early linecasting-machine-style exterior, not a reproduction of a particular maker or historical model. A joined four-shoe ground bed and two tall rising side castings carry a low inclined blank keyboard, a separate high sloping channelled matrix-store appearance, a full narrow open return-elevator frame and a bent upper distribution rail with its own opposite standard. One empty transverse open composing channel lies between the keyboard and magazine. A whole shouldered closed side casting-unit housing and rectangular mold-case exterior, plus a supported low outboard open-spoke drive wheel, belong to the same standing machine. All geometry and layout are new, not the existing tabletop typewriter raised on a stand or the old open-platen/ink-disc press with a new keyboard. There is no paper platen, fan of typebars, ink disc, impression bed, loose type or printed output. Four opaque constant PBR materials, metres, native Z up, horizontal bounds centred over the full finite ground shoes. One prop zero scenes. Simplified blank keys and channel counts do not represent a real character system. Static occupational game art only: no typing action, matrix selection, distribution, return, molten material, heater, casting, mould compatibility, pressure, temperature, drive, motion, power, historical precision, manufacture, operation, load or safety capability. Rigging, animation and interaction are not made or verified.'
PALETTE=[('WholeCastBodyAndHousing_DeepGreen',(.075,.20,.16,1),.72,.20),('WholeRailsChannelAndWheel_SatinAlloy',(.37,.43,.38,1),.44,.62),('WholeMagazineAndMoldCase_Charcoal',(.075,.09,.08,1),.76,.16),('WholeBlankKeyFaces_WarmIvory',(.73,.66,.48,1),.73,0.)]
FOCUS=(0,0,1.08);ORTHO=3.05
CAMERAS={'thumbnail':(4.0,-7.0,3.6),'qa-front':(4.0,-7.0,3.6),'qa-side':(8,0,3),'qa-top':(0,0,8),'qa-back':(-4,7,3.6),'qa-wireframe':(4.0,-7.0,3.6)}
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
root=bpy.data.objects.new('OneWholeSlopingMagazineKeyboardLinecaster',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole finite ground shoes at datum; horizontally centred; one complete static linecaster exterior';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==5156 and len(parts)==69
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
  files[role]={'path':f'assets/professional/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'professional','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
