"""New complete open-hood binnacle. Static art only, no navigation, magnetism, motion or safety claim."""
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


# One newly authored whole open-hood binnacle, not an old compass on a post.
G={};GROUND=['WholeOctagonalGroundPlinth'];ROOT_WITNESSES=[];AIR_POINTS=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
def cylinder(a,b,r,mat,role,n=20):
 w=unit(sub(b,a));ref=(0,0,1)if abs(w[2])<.9 else(0,1,0);u=unit(cross(w,ref));v=cross(w,u);ll=math.sqrt(dot(sub(b,a),sub(b,a)))
 return axial([(0,0),(r,0),(r,ll),(0,ll)],a,u,v,w,n,mat,role)
def upright(profile,n,mat,role,center=(0,0,0),phase=0):return axial(profile,center,(1,0,0),(0,1,0),(0,0,1),n,mat,role,phase)
G['WholeOctagonalGroundPlinth']=upright([(0,0),(.265,0),(.265,.045),(.235,.065),(0,.065)],8,0,'One entire broad eight-sided wooden plinth with a true finite ground bottom. It is part of this complete housed navigation-instrument exterior, not a separate stand asset.',phase=math.pi/8)
G['WholeTaperedOctagonalWoodPedestal']=upright([(0,.047),(.185,.047),(.181,.105),(.144,.760),(.172,.840),(.206,.900),(0,.900)],8,0,'One whole tall tapered octagonal wooden pedestal and flared upper shoulder, newly constructed together for the compass housing. Solid illustrative body; no claimed storage interior or access panel.',phase=math.pi/8);join('WholeTaperedOctagonalWoodPedestal','WholeOctagonalGroundPlinth',(0,0,.055))
G['WholeUpperHousingDeck']=upright([(0,.885),(.240,.885),(.255,.905),(.255,.935),(.245,.950),(0,.950)],32,0,'One complete broad upper wooden deck joins the pedestal to the partial brass hood and two independent ring-support standards. It is not the old planning table or armillary pedestal.');join('WholeUpperHousingDeck','WholeTaperedOctagonalWoodPedestal',(0,0,.892))
# A true finite-thickness HALF dome/cowl: the entire front sector is absent.
# Both actual spherical skins and both radial cut edges are closed material geometry.
p=[(.235,.935),(.235,1.030)]
p +=[(.235*math.cos(math.pi*i/16),1.030+.235*math.sin(math.pi*i/16))for i in range(1,9)]
p +=[(0,1.245)]
p +=[(.215*math.cos(math.pi*i/16),1.030+.215*math.sin(math.pi*i/16))for i in range(7,-1,-1)]
p +=[(.215,.935)]
m=Mesh();n=24;rows=[[(r*math.cos(math.pi*j/n),r*math.sin(math.pi*j/n),z)for j in range(n+1)]for r,z in p]
for k,a in enumerate(rows):
 kk=(k+1)%len(rows);b=rows[kk];ra=p[k][0];rb=p[kk][0]
 if abs(ra)<1e-10 and abs(rb)<1e-10:continue
 for j in range(n):
  if abs(ra)<1e-10:m.tri([a[0],b[j],b[j+1]],1)
  elif abs(rb)<1e-10:m.tri([a[j],a[j+1],b[0]],1)
  else:m.quad(a[j],a[j+1],b[j+1],b[j],1)
for j in[0,n]:
 for f in earclip(p):m.tri([rows[k][j]for k in f],1)
G['WholeRearHalfDomeOpenFrontHood']=m.result('One whole finite-thickness brass rear half-dome cowl with a short integral cylindrical skirt. The front half is genuinely open, exposing the suspended instrument instead of a dark painted window. Outer and inner curved skins and both complete cut edges are material geometry. This is an intentionally open static housing, not a watertight enclosure, removable cover or pressure vessel.');join('WholeRearHalfDomeOpenFrontHood','WholeUpperHousingDeck',(0,.225,.942))
for side in[-1,1]:
 lab='Left'if side<0 else'Right';x=side*.198
 G[lab+'WholeGimbalSupport']=block((x-.018,-.037,.937),(x+.018,.037,1.102),1,'One whole finite upright brass support at the deck side, carrying the transverse outer-ring trunnion. Its outer faces are separated from the half-dome cut edge.');join(lab+'WholeGimbalSupport','WholeUpperHousingDeck',(x,-.015,.943))
 G[lab+'WholeOuterRingTrunnion']=cylinder((side*.155,0,1.078),(side*.222,0,1.078),.012,2,'One whole proud horizontal outer-ring stub passing through its own finite support. Endcaps do not coincide with support or ring faces. Fixed artistic junction, not a moving bearing.');join(lab+'WholeOuterRingTrunnion',lab+'WholeGimbalSupport',(x,0,1.078))
G['WholeSuspensionGimbalRing']=upright([(.146,1.065),(.174,1.065),(.174,1.091),(.146,1.091)],40,1,'One complete thick horizontal open suspension ring, carried by its opposite X-axis stubs. The compass bowl sits inside a true radial gap and has independent perpendicular Y-axis stubs. This is a single compass support, not an astronomical display of multiple crossing spheres.')
for side in[-1,1]:join(('Left'if side<0 else'Right')+'WholeOuterRingTrunnion','WholeSuspensionGimbalRing',(side*.165,0,1.078))
G['WholeHollowSuspendedCompassBowl']=upright([(0,.986),(.050,.989),(.112,1.016),(.137,1.065),(.139,1.089),(.130,1.089),(.122,1.068),(.100,1.030),(.043,1.005),(0,1.004)],40,2,'One whole genuinely hollow compass bowl with curved lower exterior, finite bottom, real inner walls and a thick upper rim. It hangs inside the entire brass gimbal ring, not a scaled old flat compass case. The blank card is independently mounted above its inner floor; hidden interior surfaces are not claimed visible in every image.')
for side in[-1,1]:
 lab='Front'if side<0 else'Rear';G[lab+'WholeBowlTrunnion']=cylinder((0,side*.116,1.078),(0,side*.164,1.078),.0085,1,'One complete short perpendicular Y-axis bowl trunnion joins the bowl wall to the outer ring across their real gap, without filling that whole gap. Static, no gimbal movement or sea-stability performance.');join(lab+'WholeBowlTrunnion','WholeHollowSuspendedCompassBowl',(0,side*.133,1.078));join(lab+'WholeBowlTrunnion','WholeSuspensionGimbalRing',(0,side*.155,1.078))
G['WholeCardCentralStem']=upright([(0,.997),(.012,.997),(.012,1.083),(0,1.083)],20,1,'One whole central fixed stem rooted in the inner bowl bottom supports a separate plain compass card. No hidden magnetic assembly or working instrument.');join('WholeCardCentralStem','WholeHollowSuspendedCompassBowl',(0,0,1.001))
G['WholePlainCompassCard']=upright([(0,1.066),(.116,1.066),(.116,1.075),(0,1.075)],40,3,'One complete plain ivory compass card on the central stem with a visible peripheral interval to the inside bowl wall. No text, calibrated scale, magnetic direction or numerical reading.');join('WholePlainCompassCard','WholeCardCentralStem',(0,0,1.070))
rose=[]
for i in range(16):
 a=math.tau*i/16;rr=(.092 if i%4==0 else .061)if i%2==0 else .018;rose.append((rr*math.cos(a),rr*math.sin(a)))
G['WholeUncalibratedRaisedCompassRose']=extrude(rose,1.073,1.079,'z',2,'One whole shallow eight-point compass-rose silhouette on the plain card, with all arms integral and finite. It supplies visual identification, not a true magnetic needle, calibrated dial or separate decorative variants.');join('WholeUncalibratedRaisedCompassRose','WholePlainCompassCard',(.025,0,1.074))
G['WholeCentralCardCap']=upright([(0,1.076),(.016,1.076),(.019,1.081),(.012,1.090),(0,1.090)],24,1,'One entire small upper central cap, visibly proud of the card and integral rose. It is fixed art, not a validated pivot.');join('WholeCentralCardCap','WholeCardCentralStem',(0,0,1.080))
# Complete lateral ball-and-arm fittings belong to the characteristic binnacle exterior.
for side in[-1,1]:
 lab='Left'if side<0 else'Right'
 G[lab+'WholeSideBallArm']=beam((side*.142,0,.812),(side*.364,0,.812),.046,.038,1,'One complete lateral side-fitting arm embedded in the pedestal shoulder. It supports a separate vertical post and full spherical exterior fitting, not a loose added ball or count variant.');join(lab+'WholeSideBallArm','WholeTaperedOctagonalWoodPedestal',(side*.148,0,.812))
 G[lab+'WholeSideBallPost']=cylinder((side*.355,0,.803),(side*.355,0,.900),.016,1,'One whole vertical fixed side-fitting post, rooted through the lateral arm into the complete sphere. No magnetic adjustment or compensation claimed.');join(lab+'WholeSideBallPost',lab+'WholeSideBallArm',(side*.355,0,.812))
 pp=[(0 if i in[0,12]else .062*math.sin(math.pi*i/12),-.062*math.cos(math.pi*i/12))for i in range(13)]
 G[lab+'WholeSideSphere']=upright(pp,24,2,'One entire dark finite spherical side fitting of the complete binnacle silhouette. Static external appearance only, without any actual magnetic compensation or validated orientation.',center=(side*.355,0,.930));join(lab+'WholeSideSphere',lab+'WholeSideBallPost',(side*.355,0,.887))
AIR_POINTS=[(0,-.190,1.150),(0,0,1.170),(0,.100,1.170),(-.080,-.080,1.200),(.080,-.080,1.200),(.100,.100,1.078),(-.100,-.100,1.078),(.060,-.040,1.040),(-.060,.040,1.040),(.210,-.100,1.070),(-.210,-.100,1.070),(.290,0,.860),(-.290,0,.860)]
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='navigation-fixed-open-hood-gimbal-binnacle-01';VERSION='1.0.0';TITLE='Fixed Open Hood Gimbal Binnacle'
DESCRIPTION='One newly authored complete static marine binnacle-style navigation instrument exterior. A tall tapered eight-sided wooden pedestal and full ground plinth flare into an upper deck. A thick brass rear half-dome hood with its own inner curved skin and complete cut edges leaves the entire front genuinely open. Two finite side standards carry one complete horizontal suspension ring on opposed X-axis trunnions; one whole hollow compass bowl is separately suspended inside that ring by perpendicular Y-axis trunnions across real radial gaps. A central stem supports a plain ivory card with an integral eight-point uncalibrated rose and proud cap. Two complete lateral arm/post/sphere fittings belong to the whole characteristic housed instrument. All numeric geometry is new, not the old flat compass placed on a stand, an armillary sphere with its globe changed, imported components or extra separately counted fittings. One prop, zero scenes. Four opaque constant untextured PBR materials, metres, Z up, true horizontal-bounds-centred grounded origin. Small deliberate fixed attachment overlaps only. Static illustrative appearance: no magnetic response, compensation, navigation, true bearings, calibration, historical accuracy, gimbal movement, stability at sea, weather seal, manufacture, structural or operational safety claim.'
PALETTE=[('WholeWoodPedestalAndDeck_WarmMahogany',(.245,.090,.033,1),.71,0.),('WholeOpenHoodGimbalAndArms_SatinBrass',(.50,.345,.120,1),.43,.64),('WholeBowlRoseAndSideFittings_DarkIron',(.040,.055,.060,1),.50,.36),('WholePlainCompassCard_WarmIvory',(.72,.68,.52,1),.76,0.)]
FOCUS=(0,0,.625);ORTHO=1.51
CAMERAS={'gray-front3q':(2.1,-6,3.5),'gray-back3q':(-3,5,3),'thumbnail':(2.1,-6,3.5),'qa-front':(1.7,-6,3.0),'qa-side':(5,0,3),'qa-top':(0,0,6),'qa-back':(-3,5,3),'qa-wireframe':(2.1,-6,3.5),'silhouette-128-front':(1.7,-6,3.0),'silhouette-128-side':(5,0,3)}
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
root=bpy.data.objects.new('OneFixedOpenHoodGimbalBinnacle',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole finite octagonal wood plinth at Z0; actual bounds centred; complete open-hood binnacle';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==4272 and len(parts)==22
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
  files[role]={'path':f'assets/navigation/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'navigation','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
