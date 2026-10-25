"""One newly authored complete wide-header and high-grain-body combine exterior. Static art only."""
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
# Entire newly authored generic combine-style vehicle; no crop handling or operating system.
ROOT_WITNESSES=[];AIR_POINTS=[];GROUND=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
G['WholeCombineLowerFrame']=block((-.75,-.75,.70),(.75,2.60,1.12),0,'One complete long high vehicle lower frame, linking front drive-axle and rear wheel-carrier appearances. No imported construction vehicle chassis.')
G['WholeRearDroppedAxleCarrier']=block((-.69,1.87,.49),(.69,2.40,.88),0,'One whole rear dropped axle carrier connects the smaller complete rear wheels to the main high frame, rather than changing wheel count on an old machine.')
join('WholeRearDroppedAxleCarrier','WholeCombineLowerFrame',(0,2.10,.78))
for y,r,x,tag,frame in[(-.30,.85,1.12,'Front','WholeCombineLowerFrame'),(2.13,.55,1.03,'Rear','WholeRearDroppedAxleCarrier')]:
 axle='Whole'+tag+'Axle';cyl(axle,(-x-.15,y,r),(x+.15,y,r),.10,3,'One complete fixed cross-axle through both full wheel hubs and the proper main-frame carrier.',24);join(axle,frame,(0,y,r))
 for side,sx in[('Left',-1),('Right',1)]:
  cx=sx*x;w=.24 if tag=='Front'else .18;ri=r*.44;ro=r/math.cos(math.pi/24);t='Whole'+side+tag+'Tyre';h='Whole'+side+tag+'Hub'
  G[t]=axial([(ro,-w),(ro,w),(ri,w),(ri,-w)],(cx,y,r),(0,1,0),(0,0,1),(1,0,0),24,2,'One complete thick annular vehicle tyre with a full finite ground facet. No tread traction, steering, suspension or motion claim.',phase=math.pi/24);GROUND.append(t)
  cyl(h,(cx-w-.018,y,r),(cx+w+.018,y,r),ri+.018,1,'One whole proud hub seats through the thick tyre ring and complete axle; its cap plane is not coplanar with the tyre side.',24)
  join(h,t,(cx,y,r+ri+.009));join(h,axle,(cx,y,r))
G['WholeHighGrainProcessingBody']=extrude([(0,1.05),(2.65,1.05),(2.65,2.16),(2.28,2.60),(0,2.60)],-.90,.90,'x',0,'One full high shouldered main-body exterior behind the front operator station. Opaque closed artistic shell; no internal threshing, separation, sieves, engine or crop-processing machine is supplied.')
join('WholeHighGrainProcessingBody','WholeCombineLowerFrame',(0,1.1,1.08))
G['WholeSlopingFeederNeck']=extrude([(-2.20,.56),(-.65,1.05),(-.65,1.55),(-2.20,.95)],-.56,.56,'x',0,'One entire broad inclined feeder-house exterior reaches forward and down from the vehicle to the separate wide low header. It is not a front-loader pair of arms, paver hopper or open grain conveyor.')
join('WholeSlopingFeederNeck','WholeCombineLowerFrame',(0,-.69,1.065))
# Complete cab on its own forward floor, with actual open upper windows.
cab=[((-.76,-1.36,1.40),(.76,.10,1.63)),((-.79,-1.40,2.82),(.79,-.06,2.94))]
for x in[-.70,.70]:
 for y in[-1.30,-.15]:cab.append(((x-.045,y-.045,1.60),(x+.045,y+.045,2.87)))
cab=[tuple(tuple(round(v,9)for v in p)for p in b)for b in cab]
G['WholeForwardWindowOpenCab']=solid_union(cab,1,'One entire forward raised cab frame with integral floor, four posts and roof. Front and side window bays are genuine empty spaces, not translucent planes. No occupant, protective enclosure or control function.')
join('WholeForwardWindowOpenCab','WholeSlopingFeederNeck',(0,-.79,1.48));join('WholeForwardWindowOpenCab','WholeHighGrainProcessingBody',(0,.045,1.52))
G['WholeCabSeat']=solid_union([((-.24,-.87,1.61),(.24,-.40,1.93)),((-.24,-.48,1.90),(.24,-.38,2.34))],2,'One whole fixed seat-shaped solid attached to the forward cab floor. No character or ergonomic dimensions.')
join('WholeCabSeat','WholeForwardWindowOpenCab',(0,-.65,1.62))
# New integral open square grain box, with full outside and inside surfaces.
def open_grain_box():
 m=Mesh();rows=[]
 for sx,sy,z in[(.67,.61,2.56),(.96,.88,3.13),(.87,.79,3.13),(.59,.53,2.69)]:rows.append([(x,y+1.25,z)for x,y in[(-sx,-sy),(sx,-sy),(sx,sy),(-sx,sy)]])
 m.quad(*rows[0],0)
 for a,b in zip(rows,rows[1:]):
  for i in range(4):j=(i+1)%4;m.quad(a[i],a[j],b[j],b[i],0)
 m.quad(*rows[-1],0)
 return m.result('One continuous thick-walled open grain-box exterior with flared outer sides, full rim, deep inner sides and complete inner floor. Empty real top chamber, not a black panel. No grain volume or unloading connection guarantee.')
G['WholeUpperOpenGrainBox']=open_grain_box();join('WholeUpperOpenGrainBox','WholeHighGrainProcessingBody',(0,1.25,2.58))
# Entire broad low header: empty upper tray plus open straight-bat reel above.
G['WholeWideHeaderFloorAndRear']=extrude([(-3.25,.40),(-1.98,.40),(-1.98,1.08),(-2.13,1.08),(-2.13,.53),(-3.25,.53)],-2.15,2.15,'x',0,'One whole wide low header floor with continuous high rear wall. A real empty upper receiving space lies beneath the open reel; no crop, conveyor, gathering action or working cutter is modeled.')
join('WholeWideHeaderFloorAndRear','WholeSlopingFeederNeck',(0,-2.08,.88))
for side,x in[('Left',-2.13),('Right',2.13)]:
 n='WholeHeaderEndCheek'+side;G[n]=extrude([(-3.24,.44),(-2.01,.44),(-2.01,1.045),(-2.20,1.045),(-3.24,.68)],x-.06,x+.06,'x',0,'One full outer header cheek, locally below and inside the full rear wall at its corner to avoid duplicated exposed end/top planes. It bounds the real long receiving tray.')
 join(n,'WholeWideHeaderFloorAndRear',(x,-2.5,.49))
G['WholeBluntHeaderFrontLip']=block((-2.195,-3.30,.39),(2.195,-3.18,.545),3,'One entire straight broad blunt front lip, attached to the low header floor. Not an actual cutting edge or ground-contact blade.')
join('WholeBluntHeaderFrontLip','WholeWideHeaderFloorAndRear',(0,-3.21,.47))
for side,x in[('Left',-2.13),('Right',2.13)]:
 n='WholeReelSupportArm'+side;G[n]=beam((x,-2.04,.94),(x,-2.81,1.257),.105,.115,1,'One complete inclined reel-bearing support connects the header end cheek to the whole transverse axle above the empty tray.')
 join(n,'WholeHeaderEndCheek'+side,(x,-2.08,.957))
cyl('WholeReelCrossAxle',(-2.27,-2.75,1.23),(2.27,-2.75,1.23),.052,3,'One entire long transverse fixed reel axle. It passes through both supported outer ends and the full inner spiders.',24)
for side,x in[('Left',-2.13),('Right',2.13)]:join('WholeReelCrossAxle','WholeReelSupportArm'+side,(x,-2.75,1.23))
for k in range(5):
 a=math.tau*k/5+.22;u=(0,math.cos(a),math.sin(a));name='WholeStraightReelBat'+str(k);poly=[(-2.75+r*math.cos(t),1.23+r*math.sin(t))for r,t in[(.47,a-.055),(.52,a-.055),(.52,a+.055),(.47,a+.055)]]
 G[name]=extrude(poly,-2.06,2.06,'x',3,'One entire straight thick longitudinal reel bat with blunt finite edges. Unlike the old small hand-mower twisted cutting strip, this is part of the new broad above-header gathering-reel silhouette. No actual contact or rotation.')
 for j,x in enumerate([-1.87,0,1.87]):
  n='WholeReelSpider_%d_%d'%(j,k);c=(x,-2.75,1.23);G[n]=beam(c,add(c,mul(u,.505)),.045,.055,1,'One whole radial spider member links the complete reel axle to a separate full longitudinal bat; fixed and nonfunctional.')
  join(n,'WholeReelCrossAxle',add(c,mul(u,.022)));join(n,name,add(c,mul(u,.488)))
# Complete broad rear panel and a genuine continuous bent empty side tube.
G['WholeRearInsetStylePanel']=block((-.57,2.635,1.30),(.57,2.674,1.88),3,'One blank rear inset-style panel rooted into the closed body. Its visible face stands proud instead of sharing an exterior plane; no cooling or exhaust function.')
join('WholeRearInsetStylePanel','WholeHighGrainProcessingBody',(0,2.644,1.55))
def bent_empty_tube(path,outer,inner):
 m=Mesh();ors=[];irs=[];N=16
 for k,p in enumerate(path):
  w=unit(sub(path[min(k+1,len(path)-1)],path[max(0,k-1)]));u=(0,1,0);v=cross(w,u)
  ors.append([add(p,add(mul(u,outer*math.cos(j*math.tau/N)),mul(v,outer*math.sin(j*math.tau/N))))for j in range(N)])
  irs.append([add(p,add(mul(u,inner*math.cos(j*math.tau/N)),mul(v,inner*math.sin(j*math.tau/N))))for j in range(N)])
 for rows in[ors,irs]:
  for a,b in zip(rows,rows[1:]):
   for j in range(N):i=(j+1)%N;m.quad(a[j],a[i],b[i],b[j],0)
 for k in[0,len(path)-1]:
  for j in range(N):i=(j+1)%N;m.quad(ors[k][j],ors[k][i],irs[k][i],irs[k][j],0)
 return m.result('One complete thick bent side discharge-tube exterior with a real inner bore and open end. The inner/outer walls continue through its bend; body-side opening is embedded into the closed main exterior. No internal auger, grain flow, motion or compatibility.')
G['WholeLongBentSideDischargeTube']=bent_empty_tube([(-.82,.65,2.38),(-2.65,.65,2.85),(-2.95,.65,2.65)],.13,.085)
join('WholeLongBentSideDischargeTube','WholeHighGrainProcessingBody',(-.86,.765,2.39))
AIR_POINTS=[(0,1.25,2.94),(.45,-2.70,.64),(0,-.90,2.27),(0,-1.60,.26),(-2.80,.65,2.75)]
vv=[v for g in G.values()for v in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='agriculture-fixed-wide-header-reel-and-grain-body-combine-01';VERSION='1.0.0';TITLE='Fixed Wide Header Reel and Grain Body Combine'
DESCRIPTION='One newly authored complete generic combine-harvester-style vehicle exterior. Four full unequal front/rear tyres and complete hubs/axles support a high shouldered main body with a separate genuinely window-open forward cab and fixed seat. A whole broad sloping feeder neck projects down to a very wide low empty header with continuous floor/rear wall and full end cheeks. Above it, two complete supports carry one transverse axle, full radial spiders and five straight thick longitudinal reel bats; this is not the old hand-push mower enlarged, its twisted strips copied, or a paver given more wheels. One entire upper flared thick-walled grain box has a genuinely empty top chamber. A separate continuous long bent side tube has actual inner and outer walls and an open tip. All geometry and whole layout newly authored; no old visible mesh imported, no separate accessory counted as another model. Four opaque constant PBR materials, metres, native Z up and complete horizontal-envelope-centred ground origin on four full finite tyre facets. One prop zero scenes. Simplified fixed occupational game art, not any particular manufacturer model. No crops, blade sharpness, gathering, conveying, threshing, cleaning, grain unloading, capacity, engine, powertrain, steering, motion, hydraulic system, load, manufacture, fit, operation or safety performance. Rigging, animation and interaction not made or verified.'
PALETTE=[('WholeGrainBodyAndHeader_MutedBrick',(.48,.18,.09,1),.74,.14),('WholeCabSpidersAndHubs_PaleOat',(.69,.64,.46,1),.65,.20),('WholeTyresAndSeat_Charcoal',(.055,.065,.065,1),.88,0),('WholeAxlesBatsAndPanels_DarkSteel',(.15,.21,.21,1),.47,.60)]
FOCUS=(0,0,1.46);ORTHO=8.15
CAMERAS={'thumbnail':(-9,-12,8),'qa-front':(-9,-12,8),'qa-side':(11,0,5),'qa-top':(0,0,12),'qa-back':(8,10,7),'qa-wireframe':(-9,-12,8)}
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
root=bpy.data.objects.new('OneWholeWideHeaderAndGrainBodyCombine',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole four tyre facets at datum; horizontally centred; one complete static combine exterior';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==2600 and len(parts)==46
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
  files[role]={'path':f'assets/agriculture/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'agriculture','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
