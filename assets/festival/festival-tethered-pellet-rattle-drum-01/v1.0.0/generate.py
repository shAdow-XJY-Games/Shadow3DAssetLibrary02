"""One original static handheld pellet rattle-drum gift; complete blind drum cavity."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='festival-tethered-pellet-rattle-drum-01';VERSION='1.0.0';TITLE='Tethered Pellet Rattle Drum'
DESCRIPTION=('One original static low-poly handheld pellet rattle-drum gift. A single continuous shallow sixteen-sided drum case has a genuine complete blind chamber, thick back and integral flat-ended grip. A separate finite-thickness front head seals the chamber on its entire annular seat. Two opposed narrow tethers each expand continuously into one faceted end pellet and meet the case at complete finite side seats. Four editable closed connected meshes and four opaque constant untextured PBR materials, one prop and zero scenes. The complete interior chamber is real geometry even though its opaque head hides it in the assembled pose. Newly authored whole numeric shape and contact layout; no drum-kit part, kettle-drum bowl, clock case, paddle, dumbbell, top, cord or bead shape is imported, extracted, recoloured or scaled. Metres, native Z up, front-Y, horizontal bounds-centred origin with the entire grip butt on ground. Static extended-tether pose only: no sound, membrane response, flexible-cord dynamics, swinging, rotation, percussion performance, playability, historical authenticity, age suitability, child safety, physical stability, manufacture, material suitability or certification claim. No labels, ornament overlays, textures, rig, animation, extra scene or consumed asset.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};ISOLATED_VOID_VOLUMES={};FEET=[];FOOT_CONTACTS=[]
BODY='ContinuousBlindDrumCaseAndIntegralGrip';HEAD='CompleteThickFrontDrumHead';LEFT='LeftContinuousTetherAndPellet';RIGHT='RightContinuousTetherAndPellet'
PALETTE=[('Case_DeepFestivalRed',(.46,.035,.025,1),.70,0.),('Head_WarmIvory',(.83,.75,.56,1),.78,0.),('GripAndPellets_HoneyWood',(.49,.25,.075,1),.72,0.),('Tethers_DeepGold',(.39,.245,.045,1),.85,0.)]
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
# Exact Cartesian union boundary. Global cell cuts give identical edge splits;
# only exposed cell faces are emitted. There are no internal duplicate faces,
# Blender booleans, intersecting boxes, or separate component pieces per bar.

N=16;CENTRE_Z=.30;CASE_APOTHEM=.120;CAVITY_APOTHEM=.105;HEAD_APOTHEM=.115
GRIP_HALF=.014;FRONT_Y=-.023;BACK_Y=.027;CAVITY_FLOOR_Y=.021;HEAD_FRONT_Y=-.027;TETHER_Y=.002
TETHER_PROFILE=[(0.,.003),(.058,.003),(.061,.012),(.073,.018),(.085,.012),(.088,.003)]
INSET=.001;TETHER_INSET=.0006

def polygon_ring(apothem,cut_half=None):
 radius=apothem/math.cos(math.pi/N);p=[(radius*math.cos((2*i+1)*math.pi/N),CENTRE_Z+radius*math.sin((2*i+1)*math.pi/N)) for i in range(N)];out=[]
 for a,b in zip(p,p[1:]+p[:1]):
  out.append(a)
  if cut_half is not None and abs(a[1]-(CENTRE_Z-apothem))<1e-12 and abs(b[1]-a[1])<1e-12:
   assert a[0]<-cut_half<cut_half<b[0]
   out.extend([(-cut_half,CENTRE_Z-apothem),(cut_half,CENTRE_Z-apothem)])
 return out

def case_geometry(d=0):
 outer=polygon_ring(CASE_APOTHEM-d,GRIP_HALF-d)
 inner=polygon_ring(CAVITY_APOTHEM+d,(GRIP_HALF-d)*(CAVITY_APOTHEM+d)/(CASE_APOTHEM-d));assert len(outer)==len(inner)==18
 front=FRONT_Y+d;back=BACK_Y-d;floor=CAVITY_FLOOR_Y+d;m=Mesh();bottom=CENTRE_Z-(CASE_APOTHEM-d);h=GRIP_HALF-d;z0=d
 for i,(a,b) in enumerate(zip(outer,outer[1:]+outer[:1])):
  c,e=inner[i],inner[(i+1)%len(inner)]
  m.quad((a[0],front,a[1]),(b[0],front,b[1]),(e[0],front,e[1]),(c[0],front,c[1]),0,'WholeFiniteAnnularFrontRim')
  m.quad((c[0],front,c[1]),(e[0],front,e[1]),(e[0],floor,e[1]),(c[0],floor,c[1]),0,'WholeBlindChamberWall')
  m.tri([(0,floor,CENTRE_Z),(c[0],floor,c[1]),(e[0],floor,e[1])],0,'WholeBlindChamberFloor')
  m.tri([(0,back,CENTRE_Z),(a[0],back,a[1]),(b[0],back,b[1])],0,'WholeOuterBack')
  central=abs(a[1]-bottom)<1e-12 and abs(b[1]-bottom)<1e-12 and abs(a[0]+h)<1e-12 and abs(b[0]-h)<1e-12
  if not central:m.quad((a[0],front,a[1]),(b[0],front,b[1]),(b[0],back,b[1]),(a[0],back,a[1]),0,'WholeOuterCaseWall')
 # A single welded continuous grip replaces exactly the middle bottom sidewall;
 # no overlapping handle solid, hidden internal cap or duplicate seam exists.
 for y in [front,back]:m.quad((-h,y,z0),(h,y,z0),(h,y,bottom),(-h,y,bottom),2,'WholeIntegralGripCap')
 for a,b in [((-h,bottom),(-h,z0)),((-h,z0),(h,z0)),((h,z0),(h,bottom))]:m.quad((a[0],front,a[1]),(b[0],front,b[1]),(b[0],back,b[1]),(a[0],back,a[1]),2,'WholeIntegralGripSide')
 return m.result('One closed connected blind drum case with annular front mouth, complete chamber floor/back, outer walls and integral ground-ended grip; no intersecting primitives.')

def capped_ring_prism(apothem,y0,y1,mat,role,cut_half=None):
 ring=polygon_ring(apothem,cut_half);m=Mesh()
 for a,b in zip(ring,ring[1:]+ring[:1]):
  for y in [y0,y1]:m.tri([(0,y,CENTRE_Z),(a[0],y,a[1]),(b[0],y,b[1])],mat,'WholeFiniteCap')
  m.quad((a[0],y0,a[1]),(b[0],y0,b[1]),(b[0],y1,b[1]),(a[0],y1,a[1]),mat,'WholePrismSide')
 return m.result(role)

def inset_tether_profile(profile,d):
 # Offset every complete longitudinal facet plane inward. Ring radii are
 # apothems, so this2D support-line distance is the true3D facet-plane distance.
 lines=[]
 for (s,r),(t,R) in zip(profile,profile[1:]):
  slope=(R-r)/(t-s);lines.append((slope,r-slope*s-d*math.sqrt(1+slope*slope)))
 out=[(d,lines[0][0]*d+lines[0][1])]
 for (m,b),(n,c) in zip(lines,lines[1:]):
  assert abs(m-n)>1e-12;s=(c-b)/(m-n);out.append((s,m*s+b))
 s=profile[-1][0]-d;out.append((s,lines[-1][0]*s+lines[-1][1]));assert all(r>0 for s,r in out) and all(a[0]<b[0] for a,b in zip(out,out[1:]));return out

def tether_geometry(side,profile):
 m=Mesh();n=8
 def vertex(s,r,i):
  radius=r/math.cos(math.pi/n);angle=(2*i+1)*math.pi/n
  return(side*(CASE_APOTHEM+s),TETHER_Y+radius*math.cos(angle),CENTRE_Z+radius*math.sin(angle))
 for k,((s,r),(t,R)) in enumerate(zip(profile,profile[1:])):
  mat=3 if k==0 else 2
  for i in range(n):m.quad(vertex(s,r,i),vertex(s,r,(i+1)%n),vertex(t,R,(i+1)%n),vertex(t,R,i),mat,'WholeTetherFacet' if k==0 else 'WholePelletProfileFacet')
 for (s,r),mat in [(profile[0],3),(profile[-1],2)]:
  for i in range(n):m.tri([(side*(CASE_APOTHEM+s),TETHER_Y,CENTRE_Z),vertex(s,r,i),vertex(s,r,(i+1)%n)],mat,'WholeFiniteTetherEndCap')
 return m.result('One connected narrow finite tether transitioning into one faceted end pellet; fixed extended visual pose, no flexible-cord or swing simulation.')

G[BODY]=case_geometry();G[HEAD]=capped_ring_prism(HEAD_APOTHEM,HEAD_FRONT_Y,FRONT_Y,1,'Full finite-thickness opaque front head seals the true drum chamber.',GRIP_HALF*HEAD_APOTHEM/CASE_APOTHEM)
for side,name in [(-1,LEFT),(1,RIGHT)]:G[name]=tether_geometry(side,TETHER_PROFILE)
SOLID_VOLUMES[BODY+'_WholeInsetMaterial']=dict(case_geometry(INSET),targets=[BODY])
SOLID_VOLUMES[HEAD+'_WholeInsetMaterial']=dict(capped_ring_prism(HEAD_APOTHEM-INSET,HEAD_FRONT_Y+INSET,FRONT_Y-INSET,1,'Entire inward head material.'),targets=[HEAD])
for side,name in [(-1,LEFT),(1,RIGHT)]:SOLID_VOLUMES[name+'_WholeInsetMaterial']=dict(tether_geometry(side,inset_tether_profile(TETHER_PROFILE,TETHER_INSET)),targets=[name])
VOID_VOLUMES['WholeEnclosedDrumChamber']=dict(capped_ring_prism(CAVITY_APOTHEM-INSET,FRONT_Y+INSET,CAVITY_FLOOR_Y-INSET,0,'Entire finite inset polygonal sealed drum chamber; not a centre ray or cosmetic recess.'),targets=None)
def polygon_area(apothem,n=16):return n*apothem*apothem*math.tan(math.pi/n)
seat_outer=polygon_ring(HEAD_APOTHEM,GRIP_HALF*HEAD_APOTHEM/CASE_APOTHEM);seat_inner=polygon_ring(CAVITY_APOTHEM,GRIP_HALF*CAVITY_APOTHEM/CASE_APOTHEM)
annular_quads=[[(p[0],FRONT_Y,p[1]) for p in [a,b,seat_inner[(i+1)%18],seat_inner[i]]] for i,(a,b) in enumerate(zip(seat_outer,seat_outer[1:]+seat_outer[:1]))]
CONTACTS.append(dict(name='EntireAnnularCaseToHeadSeat',a=BODY,b=HEAD,origin_m=(0,0,0),u=(1,0,0),v=(0,0,1),axis=(0,-1,0),plane_m=-FRONT_Y,points=[(.110,FRONT_Y,CENTRE_Z)],complete_interface_area_m2=polygon_area(HEAD_APOTHEM)-polygon_area(CAVITY_APOTHEM),minimum_patch_area_m2=polygon_area(HEAD_APOTHEM)-polygon_area(CAVITY_APOTHEM)-2e-9,interior_probe_offset_m=.0004,finite_convex_contact_polygons_m=annular_quads))
for side,name in [(-1,LEFT),(1,RIGHT)]:
 r=.003/math.cos(math.pi/8);cap=[(side*CASE_APOTHEM,TETHER_Y+r*math.cos((2*i+1)*math.pi/8),CENTRE_Z+r*math.sin((2*i+1)*math.pi/8)) for i in range(8)]
 CONTACTS.append(dict(name=name+'_EntireSideAttachment',a=BODY,b=name,origin_m=(0,0,0),u=(0,1,0),v=(0,0,side),axis=(side,0,0),plane_m=CASE_APOTHEM,points=[(side*CASE_APOTHEM,TETHER_Y,CENTRE_Z)],complete_interface_area_m2=polygon_area(.003,8),minimum_patch_area_m2=polygon_area(.003,8)-2e-9,interior_probe_offset_m=.0004,finite_convex_contact_polygons_m=[cap]))
FEET=[BODY];INSIDE_TESTS=[(BODY,(0,TETHER_Y,.08),(0,TETHER_Y,CENTRE_Z)),(HEAD,(0,(HEAD_FRONT_Y+FRONT_Y)/2,CENTRE_Z),(0,.0,CENTRE_Z)),(LEFT,(-.15,TETHER_Y,CENTRE_Z),(-.15,TETHER_Y+.02,CENTRE_Z)),(RIGHT,(.15,TETHER_Y,CENTRE_Z),(.15,TETHER_Y+.02,CENTRE_Z))]
COMPONENT_PAIRS=list(itertools.combinations(sorted(G),2));NONCONTACT_PAIRS=[(a,b) for a,b in COMPONENT_PAIRS if not any({a,b}=={r['a'],r['b']} for r in CONTACTS)];assert len(COMPONENT_PAIRS)==6 and len(NONCONTACT_PAIRS)==3
CONTRACT={'single_prop_count':1,'new_scene_count':0,'kind':'prop','original_numeric_whole':True,'native_axis_up':'Z','front_direction':'-Y','origin':'horizontal bounds-centred; entire integral grip butt at groundZ0','closed_meshes':4,'materials':4,'true_blind_drum_chambers':1,'continuous_case_and_grip_bodies':1,'complete_thick_front_heads':1,'continuous_tether_pellets':2,'whole_material_volumes':4,'whole_air_volumes':1,'finite_opposed_contacts':3,'component_noncontact_pairs':3,'complete_component_pair_universe':6,'whole_ground_soles':1,'old_geometry_imports':0,'fixed_visual_only':True}
def measure_rattle_drum_geometry(vertices):
 assert set(vertices)==set(G);v=[p for vs in vertices.values() for p in vs];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];assert abs(lo[2])<2e-7 and max(abs(hi[i]+lo[i]) for i in [0,1])<2e-7
 return dict(CONTRACT,bounds_m=[hi[i]-lo[i] for i in range(3)],complete_grip_ground_area_m2=2*GRIP_HALF*(BACK_Y-FRONT_Y),scope='Producer geometry only; separately decoded actual complete finite predicates remain required. No acoustic or moving mechanism claims.')
FOCUS=(0,0,.21);ORTHO=.60
CAMERAS={'gray-front3q':(.6,-1.5,.8),'gray-back3q':(-.6,1.5,.8),'thumbnail':(.6,-1.5,.8),'qa-front':(0,-2,.65),'qa-side':(2,0,.65),'qa-top':(0,0,3),'qa-back':(0,2,.65),'qa-wireframe':(-.6,-1.5,.8),'silhouette-128-front':(0,-2,.65),'silhouette-128-side':(2,0,.65)}
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
root=bpy.data.objects.new('OneBlindChamberPelletRattleDrum',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole integral grip butt at Z=0; true blind drum chamber, sealed thick head and two continuous tether pellets';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
# and whole-surface nonpenetration remain separate maker actual-GLB gates.
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
mount_evidence=measure_rattle_drum_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'pellet_rattle_drum_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; maker product gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/festival/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'festival','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; maker visual/native/clean gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
