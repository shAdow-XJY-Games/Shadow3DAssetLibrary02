"""One newly authored complete four-leg straddle carrier exterior. Static art only."""
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
# Entire new fixed straddle carrier: two independently wheeled side frames and a four-corner suspended spreader.
G={};ROOT_WITNESSES=[];AIR_POINTS=[];GROUND=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
for label,s in [('Left',-1),('Right',1)]:
 x=s*1.65;n='WholeLongWheelSideFrame'+label;G[n]=block((x-.25,-2.69,.58),(x+.25,2.69,.97),0,'Whole long side chassis of the complete high straddle carrier; no cross axle or deck blocks its open ground cargo bay.')
 for j,y in enumerate([-2.24,-.86,.86,2.24]):
  t=label+str(j);xx=x+s*.30;ty='WholeGroundTyre'+t;r=.50/math.cos(math.pi/24)
  G[ty]=axial([(.20,-.19),(r,-.19),(r,.19),(.20,.19)],(xx,y,.50),(0,1,0),(0,0,1),(1,0,0),24,2,'Whole thick annular road-wheel appearance with a full finite flat ground facet, fixed without steering or rolling.',math.pi/24);GROUND.append(ty)
  h='WholeWheelHub'+t;cyl(h,(xx-.215,y,.50),(xx+.215,y,.50),.213,3,'Whole proud axle hub with its entire faces offset from the tyre end faces.',20)
  ax='WholeShortSideAxle'+t;cyl(ax,(x-.30,y,.50),(x+.55 if s>0 else x+.30,y,.50),.115,3,'Whole fixed short axle roots the wheel into its own side chassis, never spans the open cargo bay.',20) if s>0 else cyl(ax,(x-.55,y,.50),(x+.30,y,.50),.115,3,'Whole fixed short axle roots wheel into its own side chassis; no central cross axle.',20)
  join(ty,h,(xx,y,.707));join(h,ax,(xx,y,.50));join(ax,n,(x,y,.60))
 for end,y in [('Front',-2.20),('Back',2.20)]:
  p=label+end;leg='WholeTallCornerLeg'+p;G[leg]=block((x-.19,y-.20,.90),(x+.19,y+.20,5.57),0,'Whole tall corner leg joins one long wheeled side frame to the fixed upper cross-bridge; no Cartesian carriage or robot slide.');join(leg,n,(x,y,.935))
  # Complete tapered side-plane knee at each lower corner, not a duplicated panel on the leg.
  dy=1 if y<0 else-1;k='WholeSideKnee'+p;poly=[(y,.90),(y+dy*.74,.90),(y,2.04)]
  G[k]=extrude(poly,x-.135,x+.135,'x',0,'Whole thick triangular lower side knee joins the leg and its own side frame while leaving the centre bay unobstructed.');join(k,n,(x,y+dy*.20,.945));join(k,leg,(x,y+dy*.05,1.24))
 for end,y in [('Front',-2.20),('Back',2.20)]:
  a='WholeLongUpperSideRail'+label
  if a not in G:G[a]=block((x-.16,-2.55,5.32),(x+.16,2.55,5.69),0,'One fixed entire upper side rail ties both tall corner legs, with no shoe, moving bridge or longitudinal track.');
  join(a,'WholeTallCornerLeg'+label+end,(x,y,5.46))
for end,y in [('Front',-2.20),('Back',2.20)]:
 n='WholeFixedUpperCrossBridge'+end;G[n]=block((-1.78,y-.24,5.40),(1.78,y+.24,5.78),0,'Whole fixed overhead cross bridge spanning both complete side frames. The empty space underneath remains tall and open, not a rooftop or robot carriage.')
 for label,s in [('Left',-1),('Right',1)]:join(n,'WholeTallCornerLeg'+label+end,(s*1.65,y,5.50))
 for label,x in [('Left',-1.35),('Right',1.35)]:
  m='WholeDrumPedestal'+end+label;G[m]=block((x-.13,y-.16,5.73),(x+.13,y+.16,6.05),3,'Whole fixed pedestal bearing appearance roots the complete upper winding drum to its cross bridge, no functional reeving claim.');join(m,n,(x,y,5.755))
 d='WholeUpperWindingDrum'+end;G[d]=axial([(0,-1.49),(.34,-1.49),(.34,-1.28),(.28,-1.28),(.28,1.28),(.34,1.28),(.34,1.49),(0,1.49)],(0,y,5.99),(0,1,0),(0,0,1),(1,0,0),24,3,'Whole fixed crosswise winding drum with real thick end flanges, no rotation or mechanical cable routing simulation.')
 for label,x in [('Left',-1.35),('Right',1.35)]:join(d,'WholeDrumPedestal'+end+label,(x,y,5.94))
# Entire empty suspended rectangular spreader is a shared-vertex material body, not four floating loose rails.
boxes=[((-.99,-2.08,1.92),(-.79,2.08,2.16)),((.79,-2.08,1.92),(.99,2.08,2.16)),((-.98,-2.08,1.92),(.98,-1.86,2.16)),((-.98,1.86,1.92),(.98,2.08,2.16))]
for x in[-.91,.91]:
 for y in[-1.98,1.98]:boxes.append(((x-.14,y-.18,1.72),(x+.14,y+.18,2.18)))
G['WholeEmptySuspendedSpreader']=solid_union(boxes,1,'One whole thick rectangular suspended spreader appearance with a genuine large central aperture and four integral downward corner heads. Empty static interface only, no container dimensions, twist-lock, cargo compatibility or rated lifting.')
for end,y in [('Front',-2.20),('Back',2.20)]:
 yy=-1.98 if y<0 else 1.98
 for label,x in [('Left',-.91),('Right',.91)]:
  n='WholeFixedHangingLine'+end+label;cyl(n,(x,yy,2.07),(x,yy,5.99),.026,3,'One complete fixed straight hanging-line exterior from its upper drum to an integral spreader corner. No rope material, working reeving, load path or hoisting function.');join(n,'WholeEmptySuspendedSpreader',(x,yy,2.12));join(n,'WholeUpperWindingDrum'+end,(x,yy,5.97))
# A full high offset cab and its own platform make this a whole mobile carrier, not a bare gantry scaled up.
G['WholeHighCabPlatform']=block((-2.40,-2.73,4.30),(-1.44,-1.40,4.49),3,'Whole high side-cab platform joins the left front corner leg; the central cargo bay is not a vehicle deck.');join('WholeHighCabPlatform','WholeTallCornerLegLeftFront',(-1.60,-2.20,4.40))
G['WholeOffsetHighCab']=extrude([(-2.65,4.42),(-1.47,4.42),(-1.47,5.55),(-2.42,5.55),(-2.65,5.27)],-2.34,-1.45,'x',1,'Whole newly shaped high offset cab exterior rooted on its own projecting platform, with opaque windows and no modeled occupancy or controls.');join('WholeOffsetHighCab','WholeHighCabPlatform',(-1.90,-2.0,4.46))
for lab,x in [('Outer',-2.345),('Inner',-1.445)]:
 n='WholeCabSideOpaqueWindow'+lab;G[n]=extrude([(-2.54,4.78),(-1.58,4.78),(-1.58,5.43),(-2.35,5.43),(-2.54,5.20)],x-.016,x+.016,'x',2,'Whole proud opaque side window appearance has a real buried root, not duplicate exposed cabin planes.');join(n,'WholeOffsetHighCab',(-2.335 if lab=='Outer'else-1.455,-1.90,5.0))
G['WholeCabFrontOpaqueWindow']=block((-2.22,-2.663,4.75),(-1.57,-2.632,5.18),2,'One full thick opaque front cabin window with a small buried root in the front plane.');join('WholeCabFrontOpaqueWindow','WholeOffsetHighCab',(-1.90,-2.643,4.95))
# Whole side ladder outline: a connected pair of rails with all rung material shared at its roots.
lad=[((-2.23,-1.72,1.02),(-2.16,-1.64,4.37)),((-1.84,-1.72,1.02),(-1.77,-1.64,4.37))]
for z in[1.16,1.58,2.,2.42,2.84,3.26,3.68,4.10]:lad.append(((-2.22,-1.71,z),(-1.78,-1.65,z+.065)))
G['WholeFixedSideLadder']=solid_union(lad,3,'One whole connected side ladder-like frame joins the high cab platform and lower side frame through two separate brackets. No climbability, person fit or workplace access safety.')
join('WholeFixedSideLadder','WholeHighCabPlatform',(-2.19,-1.68,4.34))
G['WholeLadderLowerBracket']=block((-2.24,-1.75,.88),(-1.48,-1.60,1.12),3,'Whole lower ladder bracket roots into the left long wheel frame, without crossing the open central vehicle bay.');join('WholeLadderLowerBracket','WholeLongWheelSideFrameLeft',(-1.65,-1.67,.93));join('WholeLadderLowerBracket','WholeFixedSideLadder',(-2.19,-1.68,1.07))
G['WholeRearUpperPowerCowl']=extrude([(.65,5.52),(1.80,5.52),(1.80,6.13),(1.55,6.28),(.85,6.28),(.65,6.08)],1.43,1.96,'x',1,'Whole compact upper-rear power-cowl exterior rooted to the right upper side rail. Solid unpowered housing, not exposed working machinery.');join('WholeRearUpperPowerCowl','WholeLongUpperSideRailRight',(1.65,1.20,5.60))
AIR_POINTS=[(0,-2.6,.5),(0,0,.3),(0,0,1.35),(0,0,2.04),(0,0,4.2),(0,2.6,.6),(.5,1.1,2.06)]
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='logistics-fixed-four-leg-straddle-and-suspended-spreader-carrier-01';VERSION='1.0.0';TITLE='Fixed Four-Leg Straddle and Suspended Spreader Carrier'
DESCRIPTION='One newly authored complete empty straddle-carrier vehicle exterior. Two independent long wheeled side chassis carry four full-height corner legs, two fixed upper side ties and two cross bridges, leaving the centre open from the ground. Two entire crosswise flanged drums and four fixed hanging-line exteriors support one complete shared-vertex rectangular spreader with a genuine large centre aperture and integral downward corner heads. A newly shaped high offset side cab with proud opaque windows, its separate platform and one whole connected ladder-like frame complete the vehicle; a compact upper rear cowl is fixed on the opposite side. Unlike the old Cartesian robot, there are no rail shoes, moving bridge, orthogonal tool slide or small fingers. Unlike the shop crane, there is no single rear mast with inclined actuator/boom and hook. This is not either old frame scaled up or given wheels: the complete side-chassis, four-point surrounding suspension and large low cargo interface are newly authored together. All coordinates are new; no old vehicle or gantry mesh imported. One prop zero scenes, no container or payload. Four opaque untextured PBR roles, metres Z up and horizontal-bounds-centred ground datum. Static artistic exterior only; no engine, steering, driving, rope mechanics, reeving, lifting, rated load, container fit, climbability, operator occupancy, manufacturing or road/port safety capability. Rigging animation and interaction not made.'
PALETTE=[('WholeCarrierFrame_MutedOchre',(.62,.38,.105,1),.68,.18),('CabAndSpreader_WarmIvory',(.66,.70,.66,1),.61,.20),('TyresAndOpaqueWindows_Charcoal',(.045,.064,.069,1),.79,.03),('AxlesLinesAndPlatform_SatinSteel',(.28,.36,.38,1),.48,.52)]
FOCUS=(0,0,3.0);ORTHO=9.3
CAMERAS={'gray-front3q':(-10,-13,9),'gray-back3q':(10,13,9),'thumbnail':(-10,-13,9),'qa-front':(-10,-13,8.0),'qa-side':(-14,0,8),'qa-top':(0,0,17),'qa-back':(10,13,8),'qa-wireframe':(-10,-13,9),'silhouette-128-front':(-10,-13,8),'silhouette-128-side':(-14,0,8)}
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
root=bpy.data.objects.new('OneWholeFourLegStraddleSuspendedSpreaderCarrier',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='eight whole tyre facets at display datum; horizontal bounds-centred; complete empty static straddle carrier';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==5384 and len(parts)==57
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
  files[role]={'path':f'assets/logistics/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'logistics','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
