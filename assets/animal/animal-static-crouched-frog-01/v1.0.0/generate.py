"""One original low crouched frog. New anatomical geometry, one fixed static prop.
Generic closed-mesh arithmetic and reviewed export/render infrastructure only are reused.
No living-animal, exact-species, biological, locomotion or safety performance claim.
"""
import math,json,hashlib,sys,time,collections,itertools,copy
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='animal-static-crouched-frog-01';VERSION='1.0.0';TITLE='Static Broad-Head Crouched Frog'
DESCRIPTION=('One original complete static stylized crouched frog with a broad low head flowing continuously into a short tapering torso, two raised dorsal eye domes with integral amber iris and dark pupil faces, two large outward-splayed muscular thighs, two narrow shanks folded backward from lateral knees to rear ankles, two short bent forearms and four thick splayed four-toed feet. The broad flattened snout and pale underside belong to the continuous body surface, not floating overlays. Thirteen closed editable meshes meet only at twelve complete finite opposed planar joints. Four entire ground soles, whole inset material, all toe clefts, complete bounded rear-thigh fold domains and supplementary belly air domains and all noncontact pairs are checked. Five ordinary opaque matte constant PBR colours. Metres, native Z up, front -Y and horizontal envelope-centred ground origin. One prop, zero scenes or variants. Newly authored whole amphibian silhouette, not a modified tortoise, shortened rabbit, plush bear, bird-foot extraction or carousel component. No tail, shell, ears, fur, texture, floating eyes, pedestal, habitat, water, vegetation, rig or animation. Artistic fixed appearance only; no exact species, biological or anatomical precision, ecology, animal behaviour, jumping, locomotion, physical stability, manufacturing, safety or old-asset compatibility claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};ISOLATED_VOID_VOLUMES={};FEET=[];FOOT_CONTACTS=[];RINGS={};POLYGONS={}
BODY='ContinuousBroadHeadAndLowTorso';EYES=[];THIGHS=[];SHANKS=[];ARMS=[];HINDFEET=[];FOREFEET=[]
PALETTE=[('Skin_MutedMoss',(.22,.36,.13,1),.86,0),('Belly_SoftReed',(.64,.66,.39,1),.93,0),('Limbs_DeepFern',(.115,.25,.09,1),.90,0),('Iris_OldGold',(.67,.44,.085,1),.72,0),('Pupil_Charcoal',(.015,.024,.012,1),.68,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm(a):return math.sqrt(dot(a,a))
def unit(a):return mul(a,1/norm(a))
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.fm=[];self.tags=[];self.index={}
 def vertex(self,p):
  p=tuple(round(float(x),9) for x in p)
  if p not in self.index:self.index[p]=len(self.v);self.v.append(p)
  return self.index[p]
 def tri(self,p,mat,tag):self.f.append(tuple(self.vertex(x) for x in p));self.fm.append(mat);self.tags.append(tag)
 def quad(self,a,b,c,d,mat,tag):self.tri([a,b,c],mat,tag);self.tri([a,c,d],mat,tag)
 def result(self,role):
  edges={}
  for i,f in enumerate(self.f):
   for a,b in zip(f,f[1:]+f[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((i,a,b))
  assert all(len(v)==2 for v in edges.values()),('not closed',[(k,v) for k,v in edges.items() if len(v)!=2][:8])
  signs={0:1};todo=[0]
  while todo:
   i=todo.pop()
   for a,b in zip(self.f[i],self.f[i][1:]+self.f[i][:1]):
    for j,c,d in edges[tuple(sorted((a,b)))]:
     if i==j:continue
     want=signs[i]*(-1 if (a,b)==(c,d) else 1)
     if j in signs:assert signs[j]==want,'nonorientable'
     else:signs[j]=want;todo.append(j)
  assert len(signs)==len(self.f),'disconnected'
  self.f=[f if signs[i]>0 else tuple(reversed(f)) for i,f in enumerate(self.f)]
  volume=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]])) for f in self.f)/6
  if volume<0:self.f=[tuple(reversed(f)) for f in self.f]
  return {'vertices':self.v,'faces':self.f,'face_materials':self.fm,'face_tags':self.tags,'material':0,'role':role}
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(lo,hi,mat=0,role='complete finite closed prism'):
 m=Mesh();v=[(x,y,z) for z in[lo[2],hi[2]] for y in[lo[1],hi[1]] for x in[lo[0],hi[0]]]
 for f in BOX_FACES:m.quad(*[v[i] for i in f],mat,'CompleteFiniteFace')
 return m.result(role)
def cross2(a,b):return a[0]*b[1]-a[1]*b[0]
def area2(p):return sum(cross2(a,b) for a,b in zip(p,p[1:]+p[:1]))
def triangulate_polygon(poly):
 order=list(range(len(poly)))
 if area2(poly)<0:order.reverse()
 out=[]
 while len(order)>3:
  found=False
  for j,b in enumerate(order):
   a=order[j-1];c=order[(j+1)%len(order)]
   if cross2(sub(poly[b],poly[a]),sub(poly[c],poly[b]))<1e-12:continue
   def within(q):return all(cross2(sub(y,x),sub(q,x))>=-1e-12 for x,y in[(poly[a],poly[b]),(poly[b],poly[c]),(poly[c],poly[a])])
   if any(within(poly[q]) for q in order if q not in[a,b,c]):continue
   out.append((a,b,c));order.pop(j);found=True;break
  assert found,'Non-simple or degenerate polygon'
 out.append(tuple(order));return out

def prism(poly,axis,lo,hi,mat,role):
 # Explicit whole concave polygon end surfaces, no fan across toe clefts.
 m=Mesh();axes=[i for i in range(3) if i!=axis]
 def point(p,k):
  a=[0.,0.,0.];a[axis]=k;a[axes[0]]=p[0];a[axes[1]]=p[1];return tuple(a)
 for i,j,k in triangulate_polygon(poly):
  for z in[lo,hi]:m.tri([point(poly[t],z) for t in[i,j,k]],mat,'CompleteConcaveEnd')
 for a,b in zip(poly,poly[1:]+poly[:1]):m.quad(point(a,lo),point(b,lo),point(b,hi),point(a,hi),mat,'WholeOutlineThickness')
 return m.result(role)
def inset_polygon(p,d):
 sign=1 if area2(p)>0 else -1;out=[]
 for i,q in enumerate(p):
  a=unit(sub(q,p[i-1]));b=unit(sub(p[(i+1)%len(p)],q));na=(-a[1]*sign,a[0]*sign);nb=(-b[1]*sign,b[0]*sign);v=add(q,mul(na,d));w=add(q,mul(nb,d));den=cross2(a,b)
  assert abs(den)>1e-10;out.append(add(v,mul(a,cross2(sub(w,v),b)/den)))
 return out

def cap(m,p,mat,tag):
 c=tuple(sum(x[k] for x in p)/len(p) for k in range(3))
 for a,b in zip(p,p[1:]+p[:1]):m.tri([c,a,b],mat,tag)
def inset_patch(m,p,mat,inner,tag,scale=.5):
 c=tuple(sum(x[d] for x in p)/4 for d in range(3));q=[add(c,mul(sub(x,c),scale)) for x in p]
 for h in range(4):v=(h+1)%4;m.quad(p[h],p[v],q[v],q[h],mat,tag+'Border')
 m.quad(*q,inner,tag+'Inset')
def loft(rings,mat,role,eye=False,body=False):
 m=Mesh();cap(m,rings[0],mat,'CompleteFirstEnd');cap(m,rings[-1],mat,'CompleteLastEnd')
 for k,(a,b) in enumerate(zip(rings,rings[1:])):
  for i in range(len(a)):
   j=(i+1)%len(a);p=[a[i],a[j],b[j],b[i]]
   if eye and i==5 and k==1:inset_patch(m,p,3,4,'IntegralDorsalPupil',.5)
   else:m.quad(*p,1 if body and i in[4,5,6] else mat,'WholePaleBellyFacet' if body and i in[4,5,6] else 'WholeContinuousFacet')
 return m.result(role)
def xy(x,y,z,rx,ry):return [(x+rx*math.cos((i+.5)*math.tau/8)/math.cos(math.pi/8),y+ry*math.sin((i+.5)*math.tau/8)/math.cos(math.pi/8),z) for i in range(8)]
def xz(x,y,z,rx,rz):return [(x+rx*a,y,z+rz*b) for a,b in[(1,.45),(.7,1),(-.7,1),(-1,.45),(-1,-.45),(-.7,-1),(.7,-1),(1,-.45)]]
def yz(x,y,z,ry,rz):return [(x,y+ry*a,z+rz*b) for a,b in[(1,.45),(.7,1),(-.7,1),(-1,.45),(-1,-.45),(-.7,-1),(.7,-1),(1,-.45)]]
def part(name,rr,mat,role,**kw):G[name]=loft(rr,mat,role,**kw);RINGS[name]=rr

def contact(name,a,b,axis,polygon):
 axis=unit(axis);u=unit(cross((0,1,0),axis)) if abs(axis[1])<.9 else(1,0,0);v=cross(axis,u);p=tuple(sum(q[i] for q in polygon)/len(polygon) for i in range(3));area=abs(sum(dot(cross(x,y),axis) for x,y in zip(polygon,polygon[1:]+polygon[:1])))/2
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'u':u,'v':v,'axis':axis,'plane_m':dot(axis,p),'minimum_patch_area_m2':area-2e-7,'complete_interface_area_m2':area,'complete_interface_polygons_m':[polygon],'finite_patch_count':1,'points':[p],'interior_probe_offset_m':.0004})

# One neckless body; broad anterior section tapers directly into the low torso.
rr=[xz(0,-.58,.36,.29,.08),xz(0,-.44,.36,.36,.14),xz(0,-.28,.36,.36,.14),xz(0,-.14,.34,.27,.12),xz(0,.30,.34,.27,.12),xz(0,.48,.32,.12,.075)]
part(BODY,rr,0,'One continuous broad head and low torso: no separate neck, shell or intersecting head sphere.',body=True)
# Pale lower face is integral to the closed front cap; no open mouth is claimed.
g=G[BODY]
for i,tag in enumerate(g['face_tags']):
 if tag=='CompleteFirstEnd':
  z=sum(g['vertices'][j][2] for j in g['faces'][i])/3
  if z<.36:g['face_materials'][i]=1
for sx,side in[(-1,'Left'),(1,'Right')]:
 eye=side+'RaisedDorsalEyeDome';EYES.append(eye)
 rr=[xy(sx*.17,-.36,.5,.075,.07),xy(sx*.17,-.36,.53,.075,.07),xy(sx*.17,-.36,.625,.055,.052),xy(sx*.17,-.36,.655,.025,.025)]
 part(eye,rr,0,'Complete raised dorsal eye dome with integral amber front iris and dark pupil, whole head-crown attachment.',eye=True)
 contact(side+'WholeEyeCrownSeat',BODY,eye,(0,0,1),rr[0])
 thigh=side+'SplayedMuscularThigh';THIGHS.append(thigh)
 rr=[yz(sx*.27,.12,.34,.09,.048),yz(sx*.37,.12,.27,.21,.14),yz(sx*.47,.10,.25,.23,.14),yz(sx*.58,.04,.235,.035,.04)]
 part(thigh,rr,0,'Whole broad outward thigh ending at a low lateral knee; newly authored amphibian proportions, not a rabbit haunch.')
 contact(side+'WholeHipSeat',BODY,thigh,(sx,0,0),rr[0])
 shank=side+'BackwardFoldedNarrowShank';SHANKS.append(shank)
 poly=[(-.04,.18),(-.04,.28),(.03,.33),(.13,.29),(.52,.09),(.52,.055),(.43,.055),(.34,.11),(.05,.19)]
 lo,hi=sorted([sx*.58,sx*.65]);G[shank]=prism(poly,0,lo,hi,2,'Complete long narrow shank folded backward from lateral knee to low rear ankle; continuous closed concave outline.');POLYGONS[shank]=(poly,0,lo,hi)
 contact(side+'WholeKneeSeat',thigh,shank,(sx,0,0),rr[-1])
 arm=side+'ShortBentForearm';ARMS.append(arm)
 rr=[xy(sx*.27,-.43,.045,.045,.04),xy(sx*.30,-.39,.12,.040,.045),xy(sx*.19,-.27,.22,.05,.04)]
 part(arm,rr,2,'Complete short bent forearm from low shoulder to grounded palm; three whole finite cross-sections.')
 contact(side+'WholeForearmShoulderSeat',arm,BODY,(0,0,1),rr[-1])
 # Four true thick digits per foot, three open concave clefts; each entire foot
 # remains one closed connected mesh. Internal symmetry is one animal, not variants.
 frontpoly=[(-.065,.08),(-.14,-.055),(-.14,-.09),(-.115,-.10),(-.045,-.025),(-.065,-.18),(-.045,-.205),(-.020,-.205),(.005,-.055),(.035,-.19),(.065,-.20),(.08,-.175),(.055,-.025),(.135,-.11),(.16,-.10),(.165,-.075),(.07,.08)]
 hindpoly=[(-.06,.12),(-.15,-.10),(-.14,-.15),(-.105,-.16),(-.03,-.02),(-.04,-.24),(-.02,-.27),(.01,-.27),(.025,-.04),(.07,-.23),(.10,-.25),(.125,-.23),(.07,.015),(.16,-.11),(.19,-.11),(.205,-.08),(.095,.13),(.04,.16),(-.03,.16)]
 for label,poly,cx,cy,z,limb in[('Fore',frontpoly,.27,-.43,.045,arm),('Hind',hindpoly,.615,.42,.055,shank)]:
  foot=side+label+'WholeFourToedFoot';FEET.append(foot);(FOREFEET if label=='Fore' else HINDFEET).append(foot)
  pp=[(sx*(cx+x),cy+y) for x,y in poly];G[foot]=prism(pp,2,0,z,2,'One complete four-toed thick splayed foot; every toe cleft is real open outline and full flat sole.');POLYGONS[foot]=(pp,2,0,z)
  if label=='Fore':patch=RINGS[arm][0]
  else:patch=[(sx*x,y,.055) for x,y in[(.58,.43),(.65,.43),(.65,.52),(.58,.52)]]
  contact(side+label+'WholeAnklePalmSeat',foot,limb,(0,0,1),patch)

# Whole inset material domains preserve every complete section and concave digit.
for name,rings in RINGS.items():
 inset=[]
 for ring in rings:
  c=tuple(sum(p[k] for p in ring)/len(ring) for k in range(3));inset.append([add(c,mul(sub(p,c),.85)) for p in ring])
 inset[0]=[add(a,mul(sub(b,a),.06)) for a,b in zip(inset[0],inset[1])];inset[-1]=[add(a,mul(sub(b,a),.06)) for a,b in zip(inset[-1],inset[-2])]
 SOLID_VOLUMES[name+'_WholeInsetMaterial']=dict(loft(inset,0,'Complete inward cross-section material domain'),targets=[name])
for name,(poly,axis,lo,hi) in POLYGONS.items():
 SOLID_VOLUMES[name+'_WholeInsetMaterial']=dict(prism(inset_polygon(poly,.0015),axis,lo+.0015,hi-.0015,0,'Entire inward edge-offset domain including all toe branches and folded shank'),targets=[name])
VOID_VOLUMES['WholeLowBellyAir']=dict(box((-.10,-.53,.004),(.10,.40,.20)),targets=None)
VOID_VOLUMES['WholeBetweenForearmsAir']=dict(box((-.10,-.62,.004),(.10,-.32,.21)),targets=None)
VOID_VOLUMES['WholeBetweenDorsalEyesAir']=dict(box((-.085,-.425,.505),(.085,-.295,.64)),targets=None)
def clip_axis_polygon(poly,axis,value,keep_greater):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  da=(a[axis]-value)*(1 if keep_greater else -1);db=(b[axis]-value)*(1 if keep_greater else -1)
  if da>=-1e-12:out.append(a)
  if (da<0<db) or (db<0<da):out.append(add(a,mul(sub(b,a),da/(da-db))))
 return out

def fold_cell(poly):
 # Entire clipped rear-facing thigh triangle swept to the bounded ankle plane.
 # Actual thigh front is translated outward 1.5mm; no hand-picked core box.
 a=[(x,y+.0015,z) for x,y,z in poly];b=[(x,.5185,z) for x,y,z in poly];m=Mesh()
 for row in[a,b]:
  for i in range(1,len(row)-1):m.tri([row[0],row[i],row[i+1]],0,'CompleteFoldBoundary')
 for i in range(len(a)):j=(i+1)%len(a);m.quad(a[i],a[j],b[j],b[i],0,'CompleteFoldLateralBoundary')
 return m.result('Whole convex fold cell from complete rear-facing thigh facet to rear ankle envelope; exact adjacent-cell union coverage is independently checked')
FOLD_DOMAIN_CELLS={};TOE_DOMAIN_BOUNDARIES={}
for sx,side in[(-1,'Left'),(1,'Right')]:
 thigh=side+'SplayedMuscularThigh';g=G[thigh];index=0
 for face in g['faces']:
  tri=[g['vertices'][i] for i in face];n=cross(sub(tri[1],tri[0]),sub(tri[2],tri[0]))
  if n[1]<=1e-10:continue
  lo,hi=sorted([sx*.2715,sx*.5785]);poly=clip_axis_polygon(clip_axis_polygon(tri,0,lo,True),0,hi,False)
  if len(poly)<3:continue
  index+=1;name=side+'CompleteRearThighFoldCell%02d'%index;VOID_VOLUMES[name]=dict(fold_cell(poly),targets=None);FOLD_DOMAIN_CELLS[name]={'thigh':thigh,'complete_boundary_polygon':poly,'outward_y_margin_m':.0015,'rear_ankle_envelope_y_m':.5185,'x_trim_m':.0015}
 assert index==18,index
 lo,hi=sorted([sx*.34,sx*.51]);VOID_VOLUMES[side+'BoundedBelowThighAir']=dict(prism([(-.055,.004),(.14,.004),(.14,.061),(.26,.061),(.26,.085),(-.055,.085)],0,lo,hi,0,'Complete bounded supplementary under-thigh inspection region, excluding intentional rear toe occupancy; not a full exterior-air partition'),targets=None)
 for label,cx,cy,z,outline in[('Fore',.27,-.43,.045,frontpoly),('Hind',.615,.42,.055,hindpoly)]:
  for j,ids in enumerate([[3,4,5],[7,8,9],[11,12,13]]):
   # Actual whole digit-boundary chain from inner tip through cleft root to
   # adjacent inner tip, closed only by the actual inner-tip mouth chord.
   complete=[outline[i] for i in ids];inset=inset_polygon(complete,.0015);pp=[(sx*(cx+x),cy+y) for x,y in inset]
   name=side+label+'WholeToeCleft'+str(j+1);VOID_VOLUMES[name]=dict(prism(pp,2,-.002,z+.002,0,'Complete actual-outline toe cleft through thickness, full boundary offset1.5mm including true root and tip-mouth chord'),targets=None)
   TOE_DOMAIN_BOUNDARIES[name]={'actual_outline_indices':ids,'complete_uninset_polygon':[(sx*(cx+x),cy+y) for x,y in complete],'inward_boundary_margin_m':.0015,'complete_through_z_range_m':[-.002,z+.002]}
# Bounds-centred horizontal datum; all domains and complete contact patches translate.
vv=[p for g in G.values() for p in g['vertices']];SHIFT_Y=-(min(p[1] for p in vv)+max(p[1] for p in vv))/2
for group in[G,SOLID_VOLUMES,VOID_VOLUMES]:
 for g in group.values():g['vertices']=[(p[0],p[1]+SHIFT_Y,p[2]) for p in g['vertices']]
for r in CONTACTS:
 r['plane_m']+=r['axis'][1]*SHIFT_Y;r['points']=[(p[0],p[1]+SHIFT_Y,p[2]) for p in r['points']];r['complete_interface_polygons_m']=[[(p[0],p[1]+SHIFT_Y,p[2]) for p in poly] for poly in r['complete_interface_polygons_m']]
COMPONENT_PAIRS=list(itertools.combinations(sorted(G),2));cp={frozenset([r['a'],r['b']]) for r in CONTACTS};NONCONTACT_PAIRS=[p for p in COMPONENT_PAIRS if frozenset(p) not in cp]
CONTRACT={'single_prop_count':1,'new_scene_count':0,'kind':'prop','closed_meshes':len(G),'materials':5,'continuous_broad_head_low_torso':1,'raised_dorsal_eye_domes':2,'splayed_thighs':2,'backward_folded_shanks':2,'short_bent_forearms':2,'four_toed_feet':4,'finite_opposed_contacts':len(CONTACTS),'whole_material_volumes':len(SOLID_VOLUMES),'whole_air_volumes':len(VOID_VOLUMES),'full_ground_soles':len(FEET),'all_component_pairs':len(COMPONENT_PAIRS),'noncontact_pairs':len(NONCONTACT_PAIRS),'old_geometry_imports':0,'rig_animation_or_species_claim':False,'ordinary_opaque_PBR':True,'static_visual_only':True}
def measure_frog_geometry(vertices):
 assert set(vertices)==set(G);vv=[p for v in vertices.values() for p in v];assert abs(min(p[2] for p in vv))<2e-7
 return dict(CONTRACT,bounds_m=[max(p[i] for p in vv)-min(p[i] for p in vv) for i in range(3)],scope='Producer geometry only; independently decoded actual GLB full finite predicates govern acceptance')
INSIDE_TESTS=[(BODY,(0,.02+SHIFT_Y,.34),(3,3,3)),(EYES[0],(-.17,-.36+SHIFT_Y,.57),(3,3,3)),(THIGHS[1],(.43,.1+SHIFT_Y,.25),(3,3,3))]
FOCUS=(0,0,.29);ORTHO=2.10
CAMERAS={'gray-front3q':(2.5,-4,2.05),'gray-back3q':(-2.5,4,2.05),'thumbnail':(2.5,-4,2.05),'qa-front':(0,-5,1.35),'qa-side':(5,0,1.30),'qa-top':(0,0,5),'qa-back':(0,5,1.30),'qa-wireframe':(-2.5,4,2.05),'silhouette-128-front':(0,-5,1.35),'silhouette-128-side':(5,0,1.30)}
WIRE_THICKNESS=ORTHO/1800
# BLENDER PHASE


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
root=bpy.data.objects.new('OneStaticBroadHeadCrouchedFrog',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='four entire frog toe soles at Z0; horizontal bounds centred';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
 trees[o.name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
 actual_triangles[id(trees[o.name])]=[[tuple(float(c) for c in (o.matrix_world@o.data.vertices[i].co)) for i in t.vertices] for t in o.data.loop_triangles]
def triangle_ray_hits(triangles,p,d):
 hits=[]
 for a,b,c in triangles:
  e1=sub(b,a);e2=sub(c,a);h=cross(d,e2);det=dot(e1,h)
  if abs(det)<1e-12:continue
  inv=1/det;ss=sub(p,a);u=dot(ss,h)*inv;q=cross(ss,e1);v=dot(d,q)*inv;t=dot(e2,q)*inv
  if u>=-1e-10 and v>=-1e-10 and u+v<=1+1e-10 and 1e-7<t<20:hits.append(t)
 return hits

def inside(tree,point):
 # Actual loop triangles with Python float64 winding AND three-ray parity.
 # Duplicate shared-edge hits are one boundary crossing. Uncertain cases raise.
 triangles=actual_triangles[id(tree)];p=tuple(float(c) for c in point);omega=0.0
 for a,b,c in triangles:
  a,b,c=sub(a,p),sub(b,p),sub(c,p);la=math.sqrt(dot(a,a));lb=math.sqrt(dot(b,b));lc=math.sqrt(dot(c,c))
  den=la*lb*lc+dot(a,b)*lc+dot(b,c)*la+dot(c,a)*lb
  omega+=2*math.atan2(dot(a,cross(b,c)),den)
 w=abs(omega/(4*math.pi));parities=[]
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  hits=triangle_ray_hits(triangles,p,unit(direction));parities.append(len(set(round(t,8) for t in hits))%2)
 if abs(w-1)<1e-5 and parities==[1,1,1]:return True
 if w<1e-5 and parities==[0,0,0]:return False
 raise AssertionError(('Uncertain winding or ray-parity disagreement',w,parities,point))
inside_predicate_selftests=[]
for name,p,outside in INSIDE_TESTS:
 assert inside(trees[name],p) and not inside(trees[name],outside)
 inside_predicate_selftests.append({'object':name,'inside_solid_witness':True,'void_witness_outside_solid':True})

joints=[]
for a,b,points in LINKS:
 rows=[]
 for point in points:
  p=Vector(point);clearance=min(trees[a].find_nearest(p)[3],trees[b].find_nearest(p)[3]);assert inside(trees[a],p) and inside(trees[b],p) and clearance>.0001,('Invalid joint',a,b,point,clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
# This Blender segment checks closed shells, finite ground faces, contact areas,
# finite sided interior witnesses and export fingerprints. Complete empty bodies
# and whole-surface nonpenetration remain separate maker-self-reviewed actual-GLB gates.
def horizontal_triangles(name,z,up):
 o=byname[name];out=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z-z) for p in vv)<1.1e-6 and cr.z*up>0:out.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 return out
# Finite exact opposed shoulder seats are graph edges, distinct from overlaps.
def clip_area(a,b):
 def cr(a,b):return a[0]*b[1]-a[1]*b[0]
 if cr(sub(b[1],b[0]),sub(b[2],b[0]))<0:b=list(reversed(b))
 poly=list(a)
 for p,q in zip(b,b[1:]+b[:1]):
  old=poly;poly=[]
  if not old:break
  for s,e in zip(old,old[1:]+old[:1]):
   ds=cr(sub(q,p),sub(s,p));de=cr(sub(q,p),sub(e,p));si=ds>=-1e-12;ei=de>=-1e-12
   if si!=ei:poly.append(add(s,mul(sub(e,s),ds/(ds-de))))
   if ei:poly.append(e)
 return abs(sum(cr(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly))))/2 if len(poly)>2 else 0
face_contacts=[]
for r in CONTACTS:
 def local(p):
  q=sub(p,r['origin_m']);return(dot(q,r['u']),dot(q,r['v']),dot(q,r['axis']))
 def seat_triangles(name,sign):
  out=[];o=byname[name]
  for t in o.data.loop_triangles:
   q=[local(tuple(o.matrix_world@o.data.vertices[i].co)) for i in t.vertices]
   if max(abs(p[2]-r['plane_m']) for p in q)<1.1e-6 and cross(sub(q[1],q[0]),sub(q[2],q[0]))[2]*sign>0:out.append(q)
  return out
 aa=seat_triangles(r['a'],1);bb=seat_triangles(r['b'],-1)
 area=sum(clip_area([p[:2] for p in a],[p[:2] for p in b]) for a in aa for b in bb)
 assert area>=r['minimum_patch_area_m2'],(r,area)
 for p in r['points']:
  down=sub(p,mul(r['axis'],r['interior_probe_offset_m']));up=add(p,mul(r['axis'],r['interior_probe_offset_m']))
  assert inside(trees[r['a']],down) and inside(trees[r['b']],up) and not inside(trees[r['a']],up) and not inside(trees[r['b']],down)
 face_contacts.append(dict(r,actual_opposed_triangle_contact_area_m2=area))

adj={o.name:set() for o in parts}
for j in joints+face_contacts:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen=set(FEET);todo=list(seen)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)
supports=[]
for name in FEET:
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.0005,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
bore_checks=[]
for r in BORES:
 hit=trees[r['mesh']].ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0]
 assert hit is None,('Isolated opening capped',r)
 bore_checks.append(dict(r,actual_isolated_opening_ray_clear=True))
gap_checks=[]
for r in GAPS:
 blockers=[name for name,t in trees.items() if name in r.get('targets',trees) and t.ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0] is not None]
 assert not blockers,('Actual assembled opening blocked',r,blockers)
 gap_checks.append(dict(r,actual_full_assembly_blockers=blockers))
mount_evidence=measure_frog_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert abs(lo[2])<1e-7 and triangles<=4000
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
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'mesh_objects':mesh_count,'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,
 'components':component_checks,'connection_interior_points':joints,'all_meshes_connected_to_ground':sorted(seen),
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'static_frog_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; maker product gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/animal/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'animal','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; maker visual/native/clean gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
