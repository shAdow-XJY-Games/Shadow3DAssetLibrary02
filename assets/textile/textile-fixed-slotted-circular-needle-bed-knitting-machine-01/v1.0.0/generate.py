"""One complete fixed circular needle-bed and hanging textile tube knitting-device appearance. No operation or safety claim."""
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



G={};GROUND=[];ROOT_WITNESSES=[];AIR_POINTS=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
def box(n,lo,hi,mat,role):G[n]=block(lo,hi,mat,role)
def cyl(n,a,b,r,mat,role,N=16):
 w=unit(sub(b,a));ref=(0,0,1)if abs(w[2])<.9 else(0,1,0);u=unit(cross(w,ref));v=cross(w,u);length=math.sqrt(dot(sub(b,a),sub(b,a)))
 G[n]=axial([(0,0),(r,0),(r,length),(0,length)],a,u,v,w,N,mat,role)
def sweep(points,r,N,mat,role):
 m=Mesh();rows=[]
 for i,p in enumerate(points):
  w=unit(sub(points[min(len(points)-1,i+1)],points[max(0,i-1)]));ref=(0,0,1)if abs(w[2])<.92 else(0,1,0);u=unit(cross(w,ref));v=cross(w,u)
  rows.append([add(p,add(mul(u,r*math.cos(j*math.tau/N)),mul(v,r*math.sin(j*math.tau/N))))for j in range(N)])
 for a,b in zip(rows,rows[1:]):
  for j in range(N):k=(j+1)%N;m.quad(a[j],a[k],b[k],b[j],mat)
 for p,row in[(points[0],rows[0]),(points[-1],rows[-1])]:
  for j in range(N):m.tri([p,row[j],row[(j+1)%N]],mat)
 return m.result(role)

# Complete newly authored clamp-mounted circular knitting-device exterior.
G['WholeRearCClampBody']=extrude([(.155,0),(.335,0),(.335,.430),(.123,.430),(.123,.370),(.280,.370),(.280,.080),(.155,.080)],-.040,.040,'x',0,'One entire thick C-profile rear clamp and fixed upper cantilever. Its lower jaw is the actual whole ground sole; the large front-facing jaw opening is real. No table, hidden support, real clamping fit, stability or load claim.');GROUND.append('WholeRearCClampBody')
cyl('WholeClampVerticalScrew',(0,.205,.030),(0,.205,.165),.010,1,'One whole vertical screw-appearance stem is embedded in the lower clamp jaw; no threaded motion.',20);join('WholeClampVerticalScrew','WholeRearCClampBody',(0,.205,.050))
G['WholeClampPressurePad']=axial([(0,.153),(.026,.153),(.026,.167),(0,.167)],(0,.205,0),(1,0,0),(0,1,0),(0,0,1),24,1,'One complete low pressure-pad appearance on the fixed clamp stem.');join('WholeClampPressurePad','WholeClampVerticalScrew',(0,.205,.158))
cyl('WholeClampCrossbar',(-.063,.205,.105),(.063,.205,.105),.007,1,'One full transverse thumb bar belongs to the clamp screw, not a detached tool.',16);join('WholeClampCrossbar','WholeClampVerticalScrew',(0,.205,.105))
# A continuous true annular case, not a solid cylinder with a dark painted cap.
G['WholeOpenAnnularMachineCase']=axial([(.101,.375),(.149,.375),(.164,.388),(.164,.445),(.152,.461),(.119,.461),(.101,.446)],(0,0,0),(1,0,0),(0,1,0),(0,0,1),64,[0,0,0,0,1,1,1],'One complete thick bevelled annular body has an actual through centre. It is rooted in the independent clamp cantilever and supports the entire slotted needle cylinder.');join('WholeOpenAnnularMachineCase','WholeRearCClampBody',(0,.143,.401))
# One connected annular wall with real 24 open top slots, created as boundary of occupied cells.
N=96;zs=[.435,.505,.557];occupied={(i,j)for i in range(N)for j in range(2)if j==0 or i%4 in[2,3]};m=Mesh()
def rp(i,r,z):
 a=math.tau*(i%N)/N;return(r*math.cos(a),r*math.sin(a),z)
for i,j in sorted(occupied):
 k=(i+1)%N;z0,z1=zs[j:j+2]
 for r in[.106,.132]:m.quad(rp(i,r,z0),rp(k,r,z0),rp(k,r,z1),rp(i,r,z1),1)
 for z,nb in[(z0,j-1),(z1,j+1)]:
  if(i,nb)not in occupied:m.quad(rp(i,.106,z),rp(k,.106,z),rp(k,.132,z),rp(i,.132,z),1)
 if((i-1)%N,j)not in occupied:m.quad(rp(i,.106,z0),rp(i,.132,z0),rp(i,.132,z1),rp(i,.106,z1),1)
 if(k,j)not in occupied:m.quad(rp(k,.106,z0),rp(k,.132,z0),rp(k,.132,z1),rp(k,.106,z1),1)
G['WholeOpenSlottedNeedleCylinder']=m.result('One complete connected cylindrical needle bed with a continuous lower annulus and 24 genuine open top slots. The selected count is subordinate to this new radial whole-device architecture, never counted as extra assets.');join('WholeOpenSlottedNeedleCylinder','WholeOpenAnnularMachineCase',(.123,0,.448))
for i in range(24):
 a=math.tau*(4*i+1)/N;u=(math.cos(a),math.sin(a),0);pts=[mul(u,.119)[:2]+(.469,),mul(u,.119)[:2]+(.562,),mul(u,.116)[:2]+(.574,),mul(u,.109)[:2]+(.577,),mul(u,.105)[:2]+(.571,)]
 n='WholeFixedBentNeedle'+str(i+1);G[n]=sweep(pts,.0027,8,2,'One entire finite blunt bent needle appearance roots in the lower annulus and rises through its own true top slot. No stitch-making, latch, movement or pointed-needle safety claim.');join(n,'WholeOpenSlottedNeedleCylinder',mul(u,.119)[:2]+(.480,));AIR_POINTS.append(mul(u,.128)[:2]+(.538,))
# Hollow ribbed textile tube: full outer/inner walls and top/bottom edge thickness, not a filled sock or detached bands.
NZ=12;NT=96;m=Mesh();layers=[]
for j in range(NZ+1):
 t=j/NZ;z=.135+.352*t;rr=.078+.031*t+.004*math.sin(t*math.pi)
 layer=[]
 for inner in[False,True]:
  ring=[]
  for i in range(NT):
   a=math.tau*i/NT;r=rr+(.0022 if i%4 in[0,1]else-.0012)-( .006 if inner else 0);ring.append((r*math.cos(a),r*math.sin(a),z))
  layer.append(ring)
 layers.append(layer)
for j in range(NZ):
 for inner in[0,1]:
  for i in range(NT):k=(i+1)%NT;m.quad(layers[j][inner][i],layers[j][inner][k],layers[j+1][inner][k],layers[j+1][inner][i],3)
for layer in[layers[0],layers[-1]]:
 for i in range(NT):k=(i+1)%NT;m.quad(layer[0][i],layer[0][k],layer[1][k],layer[1][i],3)
G['WholeOpenEndedHangingRibbedTextileTube']=m.result('One continuous thick hollow textile-appearance tube hangs through the complete annular machine. Twenty-four shallow integrated longitudinal rib waves belong to its surface, not stacked separate rings or simulated stitches. Both top and bottom remain open.');join('WholeOpenEndedHangingRibbedTextileTube','WholeOpenSlottedNeedleCylinder',(.108,0,.480))
# Distinct entire side crank and housing, with finite embedded shaft roots.
box('WholeSideDriveHousing',(.140,-.035,.382),(.206,.035,.452),0,'One complete small side drive housing roots in the annular body; the enclosed transmission is not represented or claimed.');join('WholeSideDriveHousing','WholeOpenAnnularMachineCase',(.154,0,.414))
cyl('WholeSideCrankShaft',(.180,0,.419),(.243,0,.419),.012,1,'One complete lateral shaft belongs to the side drive housing and full crank.',20);join('WholeSideCrankShaft','WholeSideDriveHousing',(.195,0,.419))
G['WholeSideCrankArm']=beam((.234,0,.419),(.234,-.067,.492),.021,.018,1,'One complete side crank arm, held at one fixed pose.');join('WholeSideCrankArm','WholeSideCrankShaft',(.234,-.004,.423))
cyl('WholeSideCrankGrip',(.225,-.067,.492),(.310,-.067,.492),.018,0,'One whole thick handle roots in the outer side crank end.',16);join('WholeSideCrankGrip','WholeSideCrankArm',(.234,-.065,.490))
# One integrated high guide and its own supply spool, with a single continuous display yarn path.
cyl('WholeRearGuideMast',(-.085,.125,.407),(-.085,.125,.745),.009,1,'One complete tall rear yarn-guide mast joins the machine outer rim; it is not an unrelated needle or detached ornament.',16);join('WholeRearGuideMast','WholeOpenAnnularMachineCase',(-.085,.125,.421))
G['WholeRearSpoolSupportArm']=beam((-.085,.125,.503),(-.213,.125,.503),.022,.024,1,'One full side arm carries a complete upright supply spool.');join('WholeRearSpoolSupportArm','WholeRearGuideMast',(-.088,.125,.503))
cyl('WholeSupplySpoolPin',(-.205,.125,.492),(-.205,.125,.630),.006,1,'One complete vertical spindle attaches the integrated supply spool to its arm.',16);join('WholeSupplySpoolPin','WholeRearSpoolSupportArm',(-.205,.125,.503))
G['WholeSupplyYarnSpool']=axial([(0,.514),(.034,.514),(.034,.524),(.027,.524),(.027,.610),(.034,.610),(.034,.620),(0,.620)],(-.205,.125,0),(1,0,0),(0,1,0),(0,0,1),32,[0,0,0,3,0,0,0,0],'One whole supply bobbin exterior with full flanges and an opaque yarn-colour middle belongs to the integrated guide assembly.');join('WholeSupplyYarnSpool','WholeSupplySpoolPin',(-.205,.125,.550))
feed=math.tau*69/N;fx=.119*math.cos(feed);fy=.119*math.sin(feed)
G['WholeHighGuideArm']=beam((-.085,.125,.738),(fx,fy,.738),.014,.014,1,'One entire high guide arm reaches above a particular front needle slot, not across and filling the central through aperture.');join('WholeHighGuideArm','WholeRearGuideMast',(-.084,.121,.738))
G['WholeOpenYarnGuideEye']=axial([(.006,-.008),(.013,-.008),(.013,.008),(.006,.008)],(fx,fy,.721),(1,0,0),(0,0,1),(0,1,0),24,2,'One complete finite annular guide eye with a real through opening at the end of the high guide arm.');join('WholeOpenYarnGuideEye','WholeHighGuideArm',(fx,fy,.733))
pts=[(-.231,.125,.588),(-.230,.125,.652),(-.10,.11,.720),(fx,fy+.035,.721),(fx,fy,.721),(fx,fy-.020,.690),(fx,fy-.020,.600),(.109*math.cos(feed),.109*math.sin(feed),.576)]
G['WholeContinuousFeedYarn']=sweep(pts,.0017,8,3,'One continuous finite-thickness yarn-appearance path runs from the supply spool through the real guide eye to one fixed bent needle. Only a frozen visual route, not a threading, tension or stitch instruction.');join('WholeContinuousFeedYarn','WholeSupplyYarnSpool',(-.2305,.125,.590));join('WholeContinuousFeedYarn','WholeFixedBentNeedle18',(.109*math.cos(feed),.109*math.sin(feed)-.0004,.5767))
AIR_POINTS +=[(0,0,.420),(0,0,.540),(0,0,.200),(0,.212,.260),(.190,-.060,.405),(.01,-.02,.640),(fx+.004,fy,.721)]
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='textile-fixed-slotted-circular-needle-bed-knitting-machine-01';VERSION='1.0.0';TITLE='Fixed Slotted Circular Needle Bed Knitting Machine'
DESCRIPTION='One newly authored complete fixed circular-knitting-device exterior. A thick whole rear C-clamp and upper cantilever support a fully open annular machine case. One connected needle cylinder has a continuous lower band and genuine open top slots; separate full blunt bent needle appearances rise through those slots. One continuous finite-thickness ribbed textile tube passes inside the annulus and hangs down with both ends truly open. A complete side drive housing, shaft, crank arm and thick grip, plus a tall mast, integrated full supply bobbin, high guide arm, real open eye and one continuous feed-yarn appearance, belong to this single device. The whole circular needle-bed and through-tube relation is newly authored, not the old C-arm sewing workstation, floor loom, current overlock edge-bed case, spool rack or yarn swift resized or recoloured. Needle count and fabric ribs are subordinate details, never separate new assets. Closed editable solids, four opaque untextured constant PBR roles, metres, native Z up and actual horizontal bounds-centred ground datum at the lower clamp jaw. One model, zero scenes, no table, operator, real stitches or cloth simulation. Fixed illustrative craft-device appearance only: no rotation, moving needles, actual knitting, yarn feed, tension, transmission, fastening fit, production rate, material performance, manufacture, load, stability, ergonomics or equipment-safety claim.'
PALETTE=[('WholeCaseClampSpoolAndGrip_DeepTeal',(.08,.25,.23,1),.61,.08),('NeedleBedShaftsAndGuideFrame_DarkMetal',(.14,.17,.18,1),.49,.58),('BluntNeedlesAndOpenGuide_PaleSteel',(.53,.58,.56,1),.42,.72),('WholeHollowTextileAndYarn_WarmOchre',(.66,.40,.16,1),.93,0.)]
FOCUS=(0,0,.385);ORTHO=.94
CAMERAS={'gray-front3q':(3.8,-6,3.7),'gray-back3q':(-3.8,6,3.7),'thumbnail':(4.4,-6,3.9),'qa-front':(3.4,-6,3.5),'qa-side':(6,0,3.4),'qa-top':(0,0,6),'qa-back':(-3.8,6,3.7),'qa-wireframe':(4.4,-6,3.9),'silhouette-128-front':(3.4,-6,3.5),'silhouette-128-side':(6,0,3.4)}
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
root=bpy.data.objects.new('OneFixedSlottedCircularNeedleBedKnitter',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole lower clamp jaw at Z0; actual bounds centred; fixed whole circular needle-bed device';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==10156 and len(parts)==42
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
  files[role]={'path':f'assets/textile/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'textile','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
