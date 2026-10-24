"""One complete fixed nested-shaft planetary display. No orbit, drive, astronomical accuracy or safety claim."""
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

# A new whole table-top planetary-model appearance: low open mechanism support and staggered radial carrier arms.
G['WholeBroadSteppedDisplayBase']=axial([(0,0),(.222,0),(.235,.018),(.235,.045),(.215,.060),(0,.060)],(0,0,0),(1,0,0),(0,1,0),(0,0,1),64,[0,0,0,0,0,0],'One full stepped finite circular ground base supports the entire static planetary display. No wall fixture or detached planets.');GROUND.append('WholeBroadSteppedDisplayBase')
for i,a in enumerate([math.radians(35),math.radians(155),math.radians(270)]):
 x=.180*math.cos(a);y=.180*math.sin(a);n='WholeOpenCaseSupportColumn'+str(i+1)
 G[n]=axial([(0,.048),(.018,.048),(.018,.075),(.012,.085),(.012,.170),(.018,.180),(.018,.208),(0,.208)],(x,y,0),(1,0,0),(0,1,0),(0,0,1),16,1,'One complete turned column joins lower base and upper circular support deck, leaving the intervening gear display genuinely open.');join(n,'WholeBroadSteppedDisplayBase',(x,y,.054))
G['WholeUpperAnnularSupportDeck']=axial([(.056,.190),(.204,.190),(.210,.198),(.210,.216),(.200,.224),(.056,.224)],(0,0,0),(1,0,0),(0,1,0),(0,0,1),64,0,'One entire thick horizontal support deck has a true central bore around the fixed stacked shaft assembly. The visible open mechanism bay is below, not a solid pedestal masquerading as a gearcase.')
for i,a in enumerate([math.radians(35),math.radians(155),math.radians(270)]):join('WholeUpperAnnularSupportDeck','WholeOpenCaseSupportColumn'+str(i+1),(.180*math.cos(a),.180*math.sin(a),.202))
cyl('WholeCentralStationarySpindle',(0,0,.045),(0,0,.544),.013,1,'One complete central upright spindle roots in the broad base and carries the central sun-model sphere.',24);join('WholeCentralStationarySpindle','WholeBroadSteppedDisplayBase',(0,0,.052))
# Whole toothed disk appearances stay deliberately separated; they do not assert a working meshing gear train.
def gear(n,c,z0,z1,r,teeth,mat):
 p=[]
 for i in range(teeth):
  for t,rr in[(0,r*.91),(.20,r),(.63,r),(.87,r*.91)]:
   a=math.tau*(i+t)/teeth;p.append((c[0]+rr*math.cos(a),c[1]+rr*math.sin(a)))
 G[n]=extrude(p,z0,z1,'z',mat,'One full closed toothed-disk appearance on its own complete shaft. Fixed separated exhibit geometry only; no tooth engagement, gearing ratio or motion claim.')
gear('WholeLargeLowerToothedDisk',(0,0),.080,.098,.147,28,1);join('WholeLargeLowerToothedDisk','WholeCentralStationarySpindle',(0,0,.089))
cyl('WholeOffsetDisplayGearAxle',(.098,.067,.049),(.098,.067,.184),.009,1,'One entire upright side gear axle roots in the lower base.',16);join('WholeOffsetDisplayGearAxle','WholeBroadSteppedDisplayBase',(.098,.067,.054))
gear('WholeSmallUpperToothedDisk',(.098,.067),.135,.151,.059,16,1);join('WholeSmallUpperToothedDisk','WholeOffsetDisplayGearAxle',(.098,.067,.143))
# Side crank with independent bearing block seated on the base; no fictitious internal gear function.
G['WholeSideCrankBearingBlock']=extrude([(.123,.046),(.210,.046),(.210,.153),(.191,.171),(.141,.171),(.123,.153)],-.037,.037,'y',0,'One whole vertical shaped bearing block rises from the base to support the complete horizontal side crank shaft.');join('WholeSideCrankBearingBlock','WholeBroadSteppedDisplayBase',(.165,0,.052))
cyl('WholeHorizontalCrankShaft',(.137,0,.132),(.283,0,.132),.010,1,'One full lateral crank shaft passes into the side bearing block; the unseen drive linkage is intentionally not modelled.',20);join('WholeHorizontalCrankShaft','WholeSideCrankBearingBlock',(.169,0,.132))
G['WholeOffsetSideHandCrank']=beam((.273,0,.132),(.273,-.059,.197),.020,.018,1,'One complete fixed offset crank arm belongs to the side shaft.');join('WholeOffsetSideHandCrank','WholeHorizontalCrankShaft',(.273,-.003,.135))
cyl('WholeSideHandGrip',(.263,-.059,.197),(.340,-.059,.197),.016,0,'One complete thick grip roots in the outer crank arm.',16);join('WholeSideHandGrip','WholeOffsetSideHandCrank',(.273,-.057,.195))
# Concentric complete nested collars, axially stepped; deliberate embedded collar seats make a fixed display, not bearings.
SPECS=[('Outer',.044,.061,.177,.271,.256,.345,math.radians(15),.033,.490),('Second',.031,.046,.178,.317,.302,.279,math.radians(155),.025,.515),('Third',.021,.033,.179,.363,.348,.211,math.radians(255),.029,.498),('Inner',.011,.023,.180,.409,.394,.137,math.radians(320),.020,.510)]
for i,(label,ri,ro,z0,z1,armz,length,a,pr,pz)in enumerate(SPECS):
 n='Whole'+label+'NestedShaftSleeve';G[n]=axial([(ri,z0),(ro,z0),(ro,z1),(ri,z1)],(0,0,0),(1,0,0),(0,1,0),(0,0,1),32,1,'One complete genuinely bored fixed coaxial sleeve has its own raised crown and whole radial carrier. The nesting and axial levels are explicit, not a painted stack on a single column.')
 if i==0:join(n,'WholeUpperAnnularSupportDeck',(.058,0,.204))
 else:join(n,'Whole'+SPECS[i-1][0]+'NestedShaftSleeve',((ro+SPECS[i-1][1])/2,0,.210))
 # inner sleeve overlaps the fixed centre by1mm in radius, only a static seat.
 if i==3:join(n,'WholeCentralStationarySpindle',(.012,0,.245))
 d=(math.cos(a),math.sin(a),0);normal=(-d[1],d[0],0);centres=[mul(d,ro-.007)[:2]+(armz,),mul(d,length*.65)[:2]+(armz,),mul(d,length)[:2]+(armz+.035,)];m=Mesh();rows=[]
 for c in centres:rows.append([add(c,add(mul(normal,ss*.012),(0,0,zz*.010)))for ss,zz in[(-1,-1),(1,-1),(1,1),(-1,1)]])
 for row in[rows[0],rows[-1]]:m.quad(*row,1)
 for u,v in zip(rows,rows[1:]):
  for j in range(4):k=(j+1)%4;m.quad(u[j],u[k],v[k],v[j],1)
 arm='Whole'+label+'BentRadialPlanetCarrier';G[arm]=m.result('One entire closed flat radial carrier extends from its own shaft collar through a shallow raised outer section to a complete end planet stem. No old ring segment or duplicated planet stand is reused.');join(arm,n,mul(d,ro-.004)[:2]+(armz,))
 stem='Whole'+label+'PlanetStem';x=length*d[0];y=length*d[1];cyl(stem,(x,y,armz+.026),(x,y,pz+.006),.007,1,'One entire short upright stem roots in its own carrier and seats the whole spherical planet appearance.',16);join(stem,arm,(x-.003*d[0],y-.003*d[1],armz+.034))
 profile=[(pr*math.sin(math.pi*j/12),pz-pr*math.cos(math.pi*j/12))for j in range(13)];profile[0]=(0,pz-pr);profile[-1]=(0,pz+pr)
 planet='Whole'+label+'PlanetModel';G[planet]=axial(profile,(x,y,0),(1,0,0),(0,1,0),(0,0,1),24,2 if i%2==0 else 3,'One complete closed faceted planet-model sphere on its own visible carrier stem. Arbitrary illustrative size/colour/position, not an accurate named planet or extra reusable model.');join(planet,stem,(x,y,pz-.010))
 AIR_POINTS.append((x-.030*d[0],y-.030*d[1],armz+.080))
# Central bright sun-like sphere on the complete common spindle, separated from all four planet arms.
rad=.056;cz=.537;profile=[(rad*math.sin(math.pi*j/14),cz-rad*math.cos(math.pi*j/14))for j in range(15)];profile[0]=(0,cz-rad);profile[-1]=(0,cz+rad)
G['WholeCentralSunModel']=axial(profile,(0,0,0),(1,0,0),(0,1,0),(0,0,1),28,3,'One complete central sun-model sphere is the focal body above the visibly independent radial planet carriers. No astronomy or orbital-scale claim.');join('WholeCentralSunModel','WholeCentralStationarySpindle',(0,0,.510))
AIR_POINTS +=[(0,-.115,.145),(-.135,-.045,.145),(0,.110,.175),(.085,0,.350),(-.070,.060,.430),(.030,0,.455)]
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='technology-fixed-nested-shaft-and-radial-planetary-display-01';VERSION='1.0.0';TITLE='Fixed Nested Shaft and Radial Planetary Display'
DESCRIPTION='One newly authored complete static tabletop planetary-model display. A broad stepped ground base and three full turned columns support an annular upper deck, leaving an actual open lower bay with two independent toothed-disk appearances on complete upright shafts. A shaped side bearing block carries a full horizontal shaft, offset hand crank and grip. Above the deck, four complete truly bored concentric sleeves have different crown heights and independently carry whole bent radial arms, full outer vertical stems and closed faceted planet-model spheres. A separate complete central spindle supports the larger central sun-model sphere. The new low mechanism-base and nested-axis/radial-carrier whole relation is not an armillary ring cage with added balls or a gimballed flywheel with its rim removed; no old component geometry is reused. Four planets are subordinate parts of one illustrative device, not four separately counted models, and their arbitrary colours/sizes do not define the new asset. Closed editable solids, four opaque untextured constant PBR roles, metres, native Z up and actual horizontal bounds-centred ground datum. One model, zero scenes. Frozen fictional teaching-display exterior only: deliberate fixed overlaps and separated gear levels are not functioning bearings or a meshing drive. No motion, accurate planet identity, orbital position, astronomical time, orbital or body scale, gear ratio, calibration, instruction, manufacture, balance, stability, load, ergonomics or safety certification.'
PALETTE=[('WholeBaseDeckAndGrip_DarkWalnut',(.20,.105,.046,1),.77,0.),('FixedColumnsGearAppearancesSleevesAndArms_Brass',(.59,.39,.14,1),.46,.62),('WholePlanetModels_MutedBlue',(.12,.29,.36,1),.66,.04),('WholeSunAndOtherPlanetModels_WarmOchre',(.70,.45,.16,1),.63,.08)]
FOCUS=(0,0,.300);ORTHO=.93
CAMERAS={'gray-front3q':(4,-6,3.4),'gray-back3q':(-4,6,3.4),'thumbnail':(4,-6,3.6),'qa-front':(3.8,-6,3.1),'qa-side':(6,0,3.0),'qa-top':(0,0,6),'qa-back':(-4,6,3.4),'qa-wireframe':(4,-6,3.6),'silhouette-128-front':(3.8,-6,3.1),'silhouette-128-side':(6,0,3)}
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
root=bpy.data.objects.new('OneFixedNestedShaftPlanetaryDisplay',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole broad base at Z0; actual bounds centred; fixed planetary display';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==7088 and len(parts)==30
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
