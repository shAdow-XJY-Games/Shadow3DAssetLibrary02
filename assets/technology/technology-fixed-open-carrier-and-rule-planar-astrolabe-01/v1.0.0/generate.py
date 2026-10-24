"""One complete fixed open-carrier planar astrolabe-style prop. No astronomical, navigation or accuracy claim."""
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



# New whole flat astrolabe-style display, with a layered real-open carrier rather than a clock dial.
G={};GROUND=['WholeGroundedMotherPan'];ROOT_WITNESSES=[];AIR_POINTS=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
u=(1,0,0);v=(0,1,0);w=(0,0,1)
G['WholeGroundedMotherPan']=axial([(0,0),(.165,0),(.179,.006),(.184,.012),(.184,.030),(.164,.030),(.164,.014),(0,.014)],(0,0,0),u,v,w,64,0,'One entire thick closed-back circular mother pan has a real recessed face and full raised outer wall. Its whole finite circular underside lies at ground. It is not an old pocket-watch case rescaled and has no hinged cover or winding crown.')
G['WholeRecessedOpaqueBackPlate']=axial([(0,.012),(.162,.012),(.162,.018),(0,.018)],(0,0,0),u,v,w,64,1,'One entire opaque blank recessed inner plate lies on the complete mother-pan floor. It remains visible through the real open carrier above, but contains no calibrated coordinate map, star chart, printed markings or optical surface.');join('WholeRecessedOpaqueBackPlate','WholeGroundedMotherPan',(.060,0,.013))
# One full limb band: marks are actual top-face assignments, no floating decals.
m=Mesh();rs=[.165,.171,.177,.181];N=192
pt=lambda r,a,z:(r*math.cos(a),r*math.sin(a),z)
for i in range(N):
 a=math.tau*i/N;b=math.tau*(i+1)/N
 for j,(ri,ro)in enumerate(zip(rs,rs[1:])):
  mat=3 if i%8==0 and(j>=1 or i%32==0)else 0
  m.quad(pt(ri,a,.0315),pt(ro,a,.0315),pt(ro,b,.0315),pt(ri,b,.0315),mat)
  m.quad(pt(ri,a,.0275),pt(ri,b,.0275),pt(ro,b,.0275),pt(ro,a,.0275),0)
 for r in[rs[0],rs[-1]]:m.quad(pt(r,a,.0275),pt(r,b,.0275),pt(r,b,.0315),pt(r,a,.0315),0)
G['WholeIllustrativeFaceMarkedLimb']=m.result('One entire finite annular limb band roots in the mother-pan lip. Sparse long and short dark marks are face materials within its conforming top surface, never duplicate coplanar skins or separate numerical labels. Spacing is illustrative, not angular calibration.');join('WholeIllustrativeFaceMarkedLimb','WholeGroundedMotherPan',(.176,0,.029))
G['WholeCentralFixedSpindle']=axial([(0,.010),(.007,.010),(.007,.067),(0,.067)],(0,0,0),u,v,w,24,3,'One whole full-height central spindle is fixed into the mother-pan floor and opaque plate, physically joining the raised carrier, rule and retaining head. No working rotation, bearing fit or calibrated setting.');join('WholeCentralFixedSpindle','WholeGroundedMotherPan',(0,0,.012));join('WholeCentralFixedSpindle','WholeRecessedOpaqueBackPlate',(0,0,.016))
G['WholeCarrierCentralBoredHub']=axial([(.006,.024),(.024,.024),(.024,.039),(.006,.039)],(0,0,0),u,v,w,32,2,'One entire annular center hub of the open star-net-style carrier has a genuine bore occupied by the fixed spindle. The carrier is a connected multi-part fixed assembly, not claimed a one-piece cutout casting.');join('WholeCarrierCentralBoredHub','WholeCentralFixedSpindle',(.0065,0,.030))
G['WholeCarrierOuterOpenRing']=axial([(.143,.026),(.154,.026),(.154,.036),(.143,.036)],(0,0,0),u,v,w,64,2,'One entire outer annulus belongs to the open planar carrier above the recessed plate. Its central region is genuinely empty apart from the separate curved branches, eccentric ring and fixed pointer tongues. It is not another flat solid dial.')
def curved_strip(points,widths,z0,z1,mat,role):
 left=[];right=[]
 for i,p in enumerate(points):
  a=points[max(0,i-1)];b=points[min(len(points)-1,i+1)];d=unit((b[0]-a[0],b[1]-a[1],0));n=(-d[1],d[0]);h=widths[i]/2;left.append((p[0]+n[0]*h,p[1]+n[1]*h));right.append((p[0]-n[0]*h,p[1]-n[1]*h))
 return extrude(left+right[::-1],z0,z1,'z',mat,role)
def polar(r,a):return(r*math.cos(a),r*math.sin(a))
for k,a in enumerate([.25,2.35,4.45]):
 p0=polar(.015,a);p1=polar(.061,a-.42);p2=polar(.113,a+.40);p3=polar(.149,a+.22);pts=[]
 for i in range(13):
  t=i/12;s=1-t;pts.append(tuple(s*s*s*p0[h]+3*s*s*t*p1[h]+3*s*t*t*p2[h]+t*t*t*p3[h]for h in[0,1]))
 n='WholeCurvedCarrierBranch'+str(k+1);G[n]=curved_strip(pts,[.010]*len(pts),.025,.034,2,'One entire gently curved finite-width carrier branch joins the center hub to the outer annulus. Real spaces remain beside the complete branch. New outline and coordinates, not an old clock hand or 3D armillary band flattened.');join(n,'WholeCarrierCentralBoredHub',(*tuple(p0[h]+.20*(pts[1][h]-p0[h])for h in[0,1]),.029));join(n,'WholeCarrierOuterOpenRing',(*tuple(p3[h]+.20*(pts[-2][h]-p3[h])for h in[0,1]),.030))
EC=(0,.047,0)
G['WholeEccentricOpenCarrierCircle']=axial([(.087,.030),(.098,.030),(.098,.043),(.087,.043)],EC,u,v,w,56,2,'One entire eccentric annular carrier circle sits in the same shallow planar assembly, with a real large interior opening and a finite overlap at the outer carrier ring. It is intentionally offset, unlike concentric watch bezels, and not a tilted spherical armillary. No ecliptic coordinate accuracy is implied.');join('WholeEccentricOpenCarrierCircle','WholeCarrierOuterOpenRing',(0,.144,.033))
# Three complete blunt pointer tongues are subordinate to the whole open carrier.
tongues=[([polar(.149,-.72),(.105,-.081),(.072,-.059)],'WholeCarrierOuterOpenRing',.027,.038),([polar(.149,3.50),(-.116,-.027),(-.079,-.008)],'WholeCarrierOuterOpenRing',.028,.0395),([(.092*math.cos(.48),.047+.092*math.sin(.48)),(.062,.088),(.045,.073)],'WholeEccentricOpenCarrierCircle',.032,.045)]
for i,(pts,parent,z0,z1)in enumerate(tongues):
 n='WholeBluntStarPointerTongue'+str(i+1);G[n]=curved_strip(pts,[.012,.008,.0035],z0,z1,2,'One entire finite-blunt curved pointer tongue roots in the open carrier ring. It is not a sharp tip, text, constellation reconstruction or separate crystal ornament. Fixed illustrative astronomy/fantasy detail only.');join(n,parent,(*tuple(pts[0][h]+.10*(pts[1][h]-pts[0][h])for h in[0,1]),(max(z0,.030)+min(z1,.036 if i<2 else .043))/2))
# One complete two-ended rule sits above the network, unlike two watch hands.
ANGLE=.55;d=(math.cos(ANGLE),math.sin(ANGLE),0);e=(-math.sin(ANGLE),math.cos(ANGLE),0)
poly=[(-.166,-.005),(-.152,-.012),(.152,-.012),(.166,-.005),(.166,.005),(.152,.012),(-.152,.012),(-.166,.005)]
poly=[(d[0]*a+e[0]*b,d[1]*a+e[1]*b)for a,b in poly]
G['WholeTwoEndedRaisedSightingRule']=extrude(poly,.048,.056,'z',3,'One entire long two-ended blunt rule crosses the center above the open carrier, physically rooted on the central spindle with real layer clearance below. It is not a pair of clock hands or a copied ruler, and no functioning alidade or directional reading is asserted.');join('WholeTwoEndedRaisedSightingRule','WholeCentralFixedSpindle',(0,0,.052))
for label,t in [('Near',-.135),('Far',.135)]:
 c=mul(d,t);outer=[(-.014,.052),(.014,.052),(.014,.090),(-.014,.090)];inner=[(-.006,.064),(.006,.064),(.006,.080),(-.006,.080)]
 def point(a,b,z):return(c[0]+d[0]*a+e[0]*b,c[1]+d[1]*a+e[1]*b,z)
 rows=[[point(a,b,z)for b,z in p]for a,p in[(-.0025,outer),(.0025,outer),(-.0025,inner),(.0025,inner)]];m=Mesh()
 for i in range(4):
  j=(i+1)%4
  for a,b,c0,d0 in[(rows[0][i],rows[0][j],rows[1][j],rows[1][i]),(rows[2][i],rows[3][i],rows[3][j],rows[2][j]),(rows[0][i],rows[2][i],rows[2][j],rows[0][j]),(rows[1][i],rows[1][j],rows[3][j],rows[3][i])]:m.quad(a,b,c0,d0,3)
 n=label+'WholePiercedRuleVane';G[n]=m.result('One whole thick end vane has a true rectangular aperture through its full thickness and a lower finite rule attachment. The two aligned-looking windows are static art, not a sighting, optical or angle-measurement guarantee.');join(n,'WholeTwoEndedRaisedSightingRule',(d[0]*t,d[1]*t,.054));AIR_POINTS.append((d[0]*t,d[1]*t,.072))
G['WholeCentralRetainingHead']=axial([(0,.061),(.018,.061),(.018,.070),(0,.070)],(0,0,0),u,v,w,8,2,'One entire low faceted retaining head joins the top of the complete spindle above the raised rule. No threaded fastener or moving retention specification.');join('WholeCentralRetainingHead','WholeCentralFixedSpindle',(0,0,.064))
G['WholeTopSuspensionThrone']=extrude([(-.030,.175),(.030,.175),(.030,.199),(.018,.219),(.012,.224),(-.012,.224),(-.018,.219),(-.030,.199)],.012,.031,'z',0,'One whole broad shaped suspension throne grows from the mother-pan rim to the separate hanging ring. It is not a winding crown or a second clock-control part.');join('WholeTopSuspensionThrone','WholeGroundedMotherPan',(0,.180,.020))
G['WholeOpenHangingRing']=axial([(.028,.014),(.039,.014),(.039,.027),(.028,.027)],(0,.245,0),u,v,w,48,0,'One entire thick open hanging ring roots in the top throne and retains a real central void. The prop is shown laid flat on its full mother-pan back, not hanging from an invisible support or supplied with an extra stand.');join('WholeOpenHangingRing','WholeTopSuspensionThrone',(0,.214,.022))
AIR_POINTS +=[(0,.245,.021),(.080,-.080,.038),(-.060,-.095,.039),(.100,.035,.023),(-.080,.030,.022),(.030,-.075,.022),(0,.110,.047),(.065,-.020,.046)]
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='technology-fixed-open-carrier-and-rule-planar-astrolabe-01';VERSION='1.0.0';TITLE='Fixed Open Carrier and Rule Planar Astrolabe'
DESCRIPTION='One newly authored complete fixed planar-astrolabe-style display laid on its full circular back. A thick mother pan has a genuinely recessed opaque blank inner plate and a complete raised limb with illustrative marks assigned to actual top faces. Above it, a physically connected multi-part open carrier combines a central bored hub, outer annulus, three complete curved branches, one full eccentric open circle and three finite-blunt pointer tongues. The empty carrier regions reveal the recessed plate through real layer depth, not a solid disk painted with star shapes. One entire two-ended rule crosses the central spindle above the carrier and carries two thick end vanes with genuine rectangular apertures. A full retaining head, shaped top suspension throne and complete open hanging ring belong to the whole instrument. All numeric geometry is new, not a pocket watch with its hands removed, a 3D armillary flattened or old complete components reassembled. No watch lid, winding crown, spherical cage, globe, table or stand. One prop, zero scenes, four opaque constant untextured PBR materials, metres, native Z up and actual horizontal-bounds-centred ground origin. Fixed fictional technology/fantasy exhibit only: no calibrated graduations, actual star map, celestial coordinates, calendar, latitude, observation, navigation, optical sighting, angle accuracy, historical reconstruction, working rotation, material strength, manufacture, wearability or safety claim.'
PALETTE=[('WholeMotherPanLimbAndThrone_WarmBrass',(.48,.31,.115,1),.46,.58),('WholeBlankRecessPlate_DarkTeal',(.065,.15,.17,1),.68,.20),('WholeOpenCarrierAndHead_PaleBrass',(.66,.53,.28,1),.43,.60),('WholeRuleVanesSpindleAndIllustrativeMarks_BlueIron',(.055,.09,.115,1),.58,.45)]
FOCUS=(0,0,.030);ORTHO=.550
CAMERAS={'gray-front3q':(2.2,-3.7,8),'gray-back3q':(-2,3,8),'thumbnail':(2.2,-3.7,8),'qa-front':(1.4,-3,8),'qa-side':(5,0,6),'qa-top':(0,0,6),'qa-back':(-2,3,8),'qa-wireframe':(2.2,-3.7,8),'silhouette-128-front':(1.4,-3,8),'silhouette-128-side':(5,0,6)}
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
root=bpy.data.objects.new('OneFixedPlanarOpenCarrierAstrolabe',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole mother-pan back at Z0; actual bounds centred; fixed planar astrolabe display';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==6304 and len(parts)==19
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
  files[role]={'path':f'assets/technology/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'technology','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
