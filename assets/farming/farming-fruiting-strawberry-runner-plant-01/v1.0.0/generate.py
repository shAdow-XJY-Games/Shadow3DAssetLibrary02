"""Original whole fruiting strawberry runner plant. Lightweight maker SELF_REVIEW; no growth simulation."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='farming-fruiting-strawberry-runner-plant-01';VERSION='1.0.0';TITLE='Fruiting Strawberry Runner Plant'
DESCRIPTION='One newly authored whole low fruiting strawberry-like plant: compact upright crown with three complete trifoliate serrated-leaf petioles, a hanging downward-tapered seeded fruit and five true calyx blades, one small attached flower, and one continuous thin runner to a rooted daughter crown with its own trifoliate rosette. Complete new plant architecture and coordinates, not a removed seedling-tray plant, scaled pumpkin vine or recoloured fruit kit. No old visible mesh imported. Three opaque constant PBR roles; metres, Z up and true complete horizontal bounds-centred. Static stylised crop-form game-art only, not exact cultivar/species, growth/reproduction animation, botanical maturity, yield, edible/food-use, horticultural/irrigation or physical stability performance.'
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];INSIDE_TESTS=[]
PALETTE=[('WholePlantMutedLeafGreen',(.14,.32,.07,1),.76,0),('HangingBerryMutedRed',(.56,.036,.022,1),.56,0),('PetalsAndAchenesWarmCream',(.86,.77,.48,1),.72,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm(a):return math.sqrt(dot(a,a))
def unit(a):return mul(a,1/norm(a))
def emit(name,v,f,mat,role):
 v=[tuple(round(float(x),9)for x in p)for p in v];f=[tuple(q)for q in f]
 volume=sum(dot(v[q[0]],cross(v[q[i]],v[q[i+1]]))/6 for q in f for i in range(1,len(q)-1))
 if volume<0:f=[tuple(reversed(q))for q in f];volume=-volume
 edges=collections.Counter((a,b)for q in f for a,b in zip(q,q[1:]+q[:1]));assert all(n==1 and edges[(b,a)]==1 for (a,b),n in edges.items()),name
 assert volume>1e-9 and 0<=mat<len(PALETTE) and all(math.isfinite(x)for p in v for x in p),(name,volume)
 G[name]=dict(vertices=v,faces=f,material=mat,role=role)
def rings_mesh(loops):
 n=len(loops[0]);v=sum(loops,[]);f=[tuple(reversed(range(n))),tuple((len(loops)-1)*n+i for i in range(n))]
 for k in range(len(loops)-1):
  for i in range(n):j=(i+1)%n;f.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i))
 return v,f

"""Small standalone-source fragment: continuous transported section frames.
Requires the caller's existing pure unit/sub/dot/cross/norm/add/mul helpers.
No Blender, file IO, policy or review bypass. Centreline/radii are untouched.
"""
def continuous_sweep_frames(path):
 frames=[]
 for i in range(len(path)):
  d=unit(sub(path[min(i+1,len(path)-1)],path[max(i-1,0)]))
  if not frames:
   ref=(1,0,0)if abs(d[2])>.9 else(0,0,1);u=unit(cross(d,ref))
  else:
   previous,pu,_=frames[-1];axis=cross(previous,d);sn=norm(axis);cs=max(-1.,min(1.,dot(previous,d)))
   if sn<1e-12:
    assert cs>0,'Antiparallel tangent requires a genuine path redesign';u=pu
   else:
    k=mul(axis,1/sn);u=add(add(mul(pu,cs),mul(cross(k,pu),sn)),mul(k,dot(k,pu)*(1-cs)))
   u=unit(sub(u,mul(d,dot(u,d))))
  w=cross(d,u);assert abs(dot(d,u))<1e-10 and abs(norm(u)-1)<1e-10
  frames.append((d,u,w))
 return frames

# Entire newly authored low runner-linked strawberry-like plant; standalone-source fragment.
def swept(name,path,radii,n,mat,role):
 loops=[]
 for c,r,(_,u,w)in zip(path,radii,continuous_sweep_frames(path)):
  loops.append([add(c,add(mul(u,r*math.cos(math.tau*(i+.5)/n)),mul(w,r*math.sin(math.tau*(i+.5)/n))))for i in range(n)])
 v,f=rings_mesh(loops);emit(name,v,f,mat,role)
def connect(a,b,p):LINKS.append((a,b,[p]))
def radial_body(name,xy,profile,n,mat,role):
 v,f=rings_mesh([[(xy[0]+r*math.cos(math.tau*i/n),xy[1]+r*math.sin(math.tau*i/n),z)for i in range(n)]for z,r in profile]);emit(name,v,f,mat,role)
def serrated_leaf(name,base,bearing,L,W):
 E=(math.cos(bearing),math.sin(bearing),0);S=(-E[1],E[0],0)
 ts=[0,.08,.18,.25,.31,.38,.45,.52,.59,.66,.73,.80,.87,.94,1.];ws=[.04,.33,.52,.76,.62,.92,.76,1.,.80,.92,.72,.76,.52,.42,.02]
 contour=list(zip(ts,[-x*W for x in ws]))+list(reversed(list(zip(ts,[x*W for x in ws]))));v=[]
 def point(t,y,z):return add(base,add(mul(E,t*L),add(mul(S,y),(0,0,.008*math.sin(math.pi*t)-.018*t*t-.006*abs(y)/W+z))))
 for dz in[-.0015,.0015]:v.extend(point(t,y,dz)for t,y in contour)
 n=len(contour);v.extend([point(.5,0,-.0015),point(.5,0,.0015)]);f=[]
 for i in range(n):j=(i+1)%n;f.extend([(2*n,j,i),(2*n+1,n+i,n+j),(i,j,n+j,n+i)])
 emit(name,v,f,0,'One entire thick narrowed-base obovate serrated leaflet with a shallow folded midrib, not old heart-leaf geometry')
 return add(base,mul(E,.006))
def folded_strip(name,C,E,S,N,stations,mat,role):
 loops=[]
 for r,w,h,t in stations:loops.append([add(C,add(mul(E,r),add(mul(S,y),mul(N,h+z))))for y,z in[(-w,-t),(0,-t*1.2),(w,-t),(w,t),(0,t*1.5),(-w,t)]])
 v,f=rings_mesh(loops);emit(name,v,f,mat,role)
main='WholeMainBasalRootCrown';radial_body(main,(0,0),[(0,.014),(.025,.018),(.06,.012)],12,0,'Entire short upright root crown with true bottom cut sole; no simulated roots or soil');FEET=[main]
for k,bearing in enumerate([math.radians(-160),math.radians(80),math.radians(25)]):
 E=(math.cos(bearing),math.sin(bearing),0);J=add(mul(E,.13),(0,0,.18+.012*k));P=[(E[0]*.003,E[1]*.003,.035),add(mul(E,.07),(0,0,.12+.01*k)),add(J,mul(E,.008))];name=f'WholeMainTrifoliatePetiole{k:02d}';swept(name,P,[.007,.006,.0055],8,0,'Whole curved petiole bearing three complete joined leaflets');connect(name,main,add(P[0],mul(unit(sub(P[1],P[0])),.004)))
 for j,turn in enumerate([-1.,0,1.]):
  a=bearing+turn;D=(math.cos(a),math.sin(a),0);base=sub(J,mul(D,.003));leaf=f'Main{k:02d}WholeSerratedLeaflet{j:02d}';p=serrated_leaf(leaf,base,a,.115 if j==1 else .09,.038 if j==1 else .032);connect(leaf,name,p)
daughter='WholeDaughterBasalRootCrown';radial_body(daughter,(.34,.03),[(0,.010),(.014,.013),(.028,.009)],10,0,'Entire smaller daughter crown with its own actual flat cut sole');FEET.append(daughter)
runner='WholeContinuousInterCrownRunner';P=[(.008,.008,.025),(.10,.025,.035),(.23,.055,.025),(.34,.03,.015)];swept(runner,P,[.0035,.0033,.003,.0028],8,0,'One continuous thin curved stolon joining the two distinct upright crowns, not separated rods');connect(runner,main,add(P[0],mul(unit(sub(P[1],P[0])),.002)));connect(runner,daughter,sub(P[-1],mul(unit(sub(P[-1],P[-2])),.003)))
small='WholeDaughterTrifoliatePetiole';P=[(.34,.03,.02),(.35,.025,.05),(.364,.02,.071),(.364,.02,.088)];swept(small,P,[.0048,.0048,.005,.005],8,0,'Whole short daughter petiole');connect(small,daughter,add(P[0],mul(unit(sub(P[1],P[0])),.003)));J=(.364,.02,.080)
for j,a in enumerate([-.9,.05,1.]):
 D=(math.cos(a),math.sin(a),0);leaf=f'DaughterWholeSerratedLeaflet{j:02d}';p=serrated_leaf(leaf,sub(J,mul(D,.003)),a,.08 if j==1 else .065,.025 if j==1 else .021);connect(leaf,small,p)
fruitstem='WholeCurvedHangingFruitPeduncle';P=[(.005,-.005,.04),(-.04,-.05,.14),(-.10,-.10,.19),(-.15,-.14,.15),(-.17,-.16,.14)];swept(fruitstem,P,[.0055,.005,.0047,.0045,.004],8,0,'Whole continuous arching peduncle ending inside the fruit crown');connect(fruitstem,main,add(P[0],mul(unit(sub(P[1],P[0])),.003)))
fruit='WholeTaperedHangingStrawberryBody';C=(-.17,-.16,0);profile=[(.035,.002),(.045,.016),(.065,.029),(.09,.042),(.115,.045),(.135,.035),(.145,.020)];radial_body(fruit,C[:2],profile,20,1,'Whole fleshy downward-tapered shouldered fruit body; raised achenes are real joined exterior meshes');connect(fruit,fruitstem,sub(P[-1],mul(unit(sub(P[-1],P[-2])),.003)))
for j in range(5):
 a=math.tau*j/5;E=(math.cos(a),math.sin(a),0);S=(-E[1],E[0],0);name=f'WholePointedFruitCalyx{j:02d}';folded_strip(name,add(C,(0,0,.141)),E,S,(0,0,1),[(.006,.006,0,.0015),(.022,.012,.004,.0015),(.038,.009,.002,.0015),(.052,.001,-.006,.0015)],0,'Whole thick pointed calyx blade attached to actual fruit crown');connect(name,fruit,add(C,add(mul(E,.010),(0,0,.142))))
for row,z in enumerate([.06,.08,.10,.125]):
 for z0,r0 in profile:
  if z0<=z:lo=(z0,r0)
  else:hi=(z0,r0);break
 slope=(hi[1]-lo[1])/(hi[0]-lo[0]);rad=lo[1]+slope*(z-lo[0]);rpoly=rad*math.cos(math.pi/20)
 for k in range(8):
  a=(int(20*k/8)+(row%2)+.5)*math.tau/20;N=unit((math.cos(a),math.sin(a),-slope*math.cos(math.pi/20)));S=(-math.sin(a),math.cos(a),0);T=cross(S,N);O=add(C,(rpoly*math.cos(a),rpoly*math.sin(a),z));loops=[]
  for h,scale in[(-.0012,.45),(0,1),(.0015,.45)]:loops.append([add(O,add(mul(N,h),add(mul(S,.0014*scale*math.cos(math.tau*(i+.5)/6)),mul(T,.0032*scale*math.sin(math.tau*(i+.5)/6)))))for i in range(6)])
  name=f'WholeRaisedFruitAchene{row:02d}{k:02d}';v,f=rings_mesh(loops);emit(name,v,f,2,'One complete small pale raised achene exterior, joined through actual tapered fruit surface; not texture dots');connect(name,fruit,sub(O,mul(N,.0006)))
flowerstem='WholeShortFlowerPeduncle';FC=(-.13,.01,.24);FN=unit((0,-.5,.866));P=[(-.10,-.10,.19),(-.11,-.03,.22),(-.125,.019,.222),sub(FC,mul(FN,.016)),sub(FC,mul(FN,.002))];swept(flowerstem,P,[.0038,.0035,.0034,.0032,.0032],8,0,'Whole attached flower side-peduncle');connect(flowerstem,fruitstem,add(P[0],mul(unit(sub(P[1],P[0])),.0015)))
FU=(1,0,0);FV=cross(FN,FU)
def floral_body(name,profile,mat,role):
 v,f=rings_mesh([[add(FC,add(mul(FN,h),add(mul(FU,r*math.cos(math.tau*i/12)),mul(FV,r*math.sin(math.tau*i/12)))))for i in range(12)]for h,r in profile]);emit(name,v,f,mat,role)
base='WholeFlowerReceptacle';floral_body(base,[(-.008,.004),(0,.012),(.006,.009)],0,'Whole green flower base');connect(base,flowerstem,sub(FC,mul(FN,.006)))
disc='WholeSmallFlowerCentre';floral_body(disc,[(.002,.009),(.006,.010),(.010,.004)],2,'One small raised pale central disc, not a separate flower asset');connect(disc,base,add(FC,mul(FN,.004)))
for k in range(5):
 a=math.tau*k/5;E=add(mul(FU,math.cos(a)),mul(FV,math.sin(a)));S=cross(FN,E);name=f'WholeSmallFlowerPetal{k:02d}';folded_strip(name,FC,E,S,FN,[(.006,.003,.003,.0015),(.017,.011,.002,.0015),(.030,.011,0,.0015),(.040,.004,-.002,.0015),(.042,.0015,-.002,.0015)],2,'Whole rounded broad short petal, subordinate to complete runner-linked plant');connect(name,base,add(FC,add(mul(E,.008),mul(FN,.003))))
# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 assert set(vertices)==set(G)
 allv=[p for points in vertices.values()for p in points];assert abs(min(p[2]for p in allv))<2e-7
 assert all(abs(max(p[i]for p in allv)+min(p[i]for p in allv))<=4e-7 for i in [0,1])
 return dict(review_scope='basic complete-mesh count, finite bounds and true whole-centre only; no complete-air or finite-seat mathematical proof claimed',mesh_count=len(vertices),static_fruiting_runner_plant_visual_only=True)
FOCUS=(0,0,.12);ORTHO=.83;WIRE_THICKNESS=.0004
CAMERAS={'thumbnail':(3,-6,4.3),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
root=bpy.data.objects.new('OneFruitingStrawberryRunnerPlant',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole horizontal bounds centre; whole main and daughter basal crown soles Z0; static plant appearance only';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
# and whole-surface nonpenetration proofs are not claimed by this lightweight asset.
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
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.000025,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
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
mount_evidence=measure_basic_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],9) for i in range(3)]
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'basic_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; maker product gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/farming/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'farming','style':'warm-handcrafted-village','title':TITLE,'description':DESCRIPTION,
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
  wire_objects=[];wire_meshes=[];wm=None
  try:
   if name=='qa-wireframe':
    wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
    for o in parts:
     dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;wire_objects.append(dup);wire_meshes.append(dup.data);dup.data.materials.clear();dup.data.materials.append(wm)
     for f in dup.data.polygons:f.material_index=0
     w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=WIRE_THICKNESS;w.use_replace=True;w.use_even_offset=False;w.offset=1
   render(name,pos)
  finally:
   # A caller may request any valid view order. Diagnostic overlays never leak
   # into the following actual-material view or an exception recovery state.
   for dup in wire_objects:bpy.data.objects.remove(dup,do_unlink=True)
   for mesh in wire_meshes:
    if mesh.users==0:bpy.data.meshes.remove(mesh)
   if wm is not None and wm.users==0:bpy.data.materials.remove(wm)
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
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; maker actual pixel and file self-check pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
