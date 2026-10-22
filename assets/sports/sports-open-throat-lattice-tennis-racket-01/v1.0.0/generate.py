"""New fixed open-throat lattice tennis-racket appearance, SOURCE draft only.
No string tension, regulation, impact, ergonomics or safety claim.
"""
import math,json,hashlib,sys,time,collections,itertools
from collections import defaultdict
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='sports-open-throat-lattice-tennis-racket-01';VERSION='1.0.0';TITLE='Open-Throat Lattice Tennis Racket'
DESCRIPTION='One original static low-poly tennis-racket appearance: one continuous thick faceted oval frame, real triangular open throat, two integrated neck branches and long flared-butt handle, plus one separately editable thin connected flat lattice with48 actual through-holes. The lattice seats on all eight full finite inner frame walls without positive penetration. The complete frame has two true holes and the lattice has48; no opaque head sheet or transparent net texture. Two closed connected meshes and two constant opaque untextured PBR materials, one prop and zero scenes. Metres, Z up, front-Y, horizontally centred origin at the complete butt sole. All numeric contours and grid geometry are new; no old paddle, landing-net bag, strainer bowl, field net or carabiner is imported, flattened, rescaled or extracted. Generic planar clipping, triangulation, welded boundary and guarded export utilities are reused. Coarse flat lattice is a stylized visual representation, not simulated round woven strings. No ball, player, stand, logo, text, skin, wrap, tension adjustment, joints, animation or scene. No regulation dimensions, string material, tension, elasticity, strength, swing, impact, bounce, grip fit, balance, standing stability, sports affiliation, manufacturing, usability or safety certification.'
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};ISOLATED_VOID_VOLUMES={};FEET=[];FOOT_CONTACTS=[]
BODY='WholeOpenThroatFrameAndLongHandle';HANDLE='WholeConnectedFortyEightHoleLattice'
PALETTE=[('Frame_DeepBlue',(.035,.15,.22,1),.52,.08),('Lattice_WarmIvory',(.78,.72,.54,1),.86,0.)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm(a):return math.sqrt(dot(a,a))
def unit(a):return mul(a,1/norm(a))
def cross2(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def area(p):return sum(cross2(a,b)for a,b in zip(p,p[1:]+p[:1]))/2
def tidy(p):
 out=[]
 for q in p:
  q=tuple(round(x,12)for x in q)
  if not out or q!=out[-1]:out.append(q)
 if len(out)>1 and out[0]==out[-1]:out.pop()
 return out if len(out)>=3 and abs(area(out))>1e-13 else []
def cut(poly,a,b,inside=True):
 out=[];e=sub(b,a)
 for p,q in zip(poly,poly[1:]+poly[:1]):
  dp=cross2(e,sub(p,a))*(1 if inside else -1);dq=cross2(e,sub(q,a))*(1 if inside else -1);ip=dp>=-1e-13;iq=dq>=-1e-13
  if ip:out.append(p)
  if ip!=iq:out.append(tuple(p[i]+(q[i]-p[i])*dp/(dp-dq)for i in range(2)))
 return tidy(out)
def intersect(p,c):
 for a,b in zip(c,c[1:]+c[:1]):
  if not p:return []
  p=cut(p,a,b)
 return p
def difference(p,h):
 if not intersect(p,h):return [p]
 out=[]
 for a,b in zip(h,h[1:]+h[:1]):
  if not p:break
  q=cut(p,a,b,False)
  if q:out.append(q)
  p=cut(p,a,b)
 return out
def offset(p,d):
 lines=[]
 for a,b in zip(p,p[1:]+p[:1]):
  v=sub(b,a);l=math.hypot(*v);lines.append(((a[0]-v[1]*d/l,a[1]+v[0]*d/l),v))
 out=[]
 for i,(p,v)in enumerate(lines):
  q,w=lines[i-1];t=cross2(sub(q,p),w)/cross2(v,w);out.append((p[0]+t*v[0],p[1]+t*v[1]))
 return tidy(out)
def ears(p):
 ids=list(range(len(p)));out=[]
 while len(ids)>3:
  for j,b in enumerate(ids):
   a=ids[j-1];c=ids[(j+1)%len(ids)];tri=[p[a],p[b],p[c]]
   if area(tri)<=1e-13:continue
   if any(all(cross2(sub(v,u),sub(p[k],u))>=-1e-13 for u,v in zip(tri,tri[1:]+tri[:1]))for k in ids if k not in [a,b,c]):continue
   out.append(tri);ids.pop(j);break
  else:raise AssertionError('ear failure')
 return out+[[p[k]for k in ids]]
def region(outer,holes,grid=False):
 if grid:
  xs=sorted(set(x for p in [outer]+holes for x,z in p));zs=sorted(set(z for p in [outer]+holes for x,z in p));cells=[]
  for a,b in zip(xs,xs[1:]):
   for c,d in zip(zs,zs[1:]):
    p=intersect([(a,c),(b,c),(b,d),(a,d)],outer)
    if p:cells.append(p)
 else:cells=ears(outer)
 for hole in holes:cells=[q for p in cells for q in difference(p,hole)]
 return cells
def extrude(cells,y0,y1):
 pts=sorted(set(q for p in cells for q in p));split=[]
 for p in cells:
  out=[]
  for a,b in zip(p,p[1:]+p[:1]):
   e=sub(b,a);l=sum(x*x for x in e);qs=[]
   for q in pts:
    t=sum(x*y for x,y in zip(sub(q,a),e))/l
    if -1e-9<=t<1-1e-9 and abs(cross2(e,sub(q,a)))<=1e-11:qs.append((t,q))
   out += [q for t,q in sorted(qs)]
  split.append(out)
 vv=[];ff=[];lookup={};boundary={}
 def vi(q):
  q=tuple(round(x,11)for x in q)
  if q not in lookup:lookup[q]=len(vv);vv.append(q)
  return lookup[q]
 def face(q):ff.append(tuple(vi(x)for x in q))
 for p in split:
  for tri in ears(p):
   face([(x,y0,z)for x,z in tri]);face([(x,y1,z)for x,z in reversed(tri)])
  for a,b in zip(p,p[1:]+p[:1]):
   key=tuple(sorted((a,b)))
   if key in boundary:assert boundary[key]==(b,a);del boundary[key]
   else:boundary[key]=(a,b)
 for a,b in boundary.values():
  A=(a[0],y0,a[1]);B=(b[0],y0,b[1]);C=(b[0],y1,b[1]);D=(a[0],y1,a[1]);face([A,D,C]);face([A,C,B])
 edges=defaultdict(list)
 for i,f in enumerate(ff):
  for a,b in zip(f,f[1:]+f[:1]):edges[tuple(sorted((a,b)))].append((i,a,b))
 assert all(len(v)==2 for v in edges.values()),[(e,v)for e,v in edges.items()if len(v)!=2][:4]
 assert all(v[0][1:]==v[1][1:][::-1]for v in edges.values())
 vol=sum(vv[a][0]*(vv[b][1]*vv[c][2]-vv[b][2]*vv[c][1])+vv[a][1]*(vv[b][2]*vv[c][0]-vv[b][0]*vv[c][2])+vv[a][2]*(vv[b][0]*vv[c][1]-vv[b][1]*vv[c][0])for a,b,c in ff)/6
 assert vol>0,vol
 return dict(vertices=vv,faces=ff,euler=len(vv)-len(edges)+len(ff),volume=vol,boundary2d=list(boundary.values()))
OUTER=[(-.024,0),(.024,0),(.024,.018),(.018,.033),(.018,.185),(.076,.278),(.122,.334),(.122,.526),(.076,.582),(-.076,.582),(-.122,.526),(-.122,.334),(-.076,.278),(-.018,.185),(-.018,.033),(-.024,.018)]
INNER=[(-.070,.290),(.070,.290),(.110,.340),(.110,.520),(.070,.570),(-.070,.570),(-.110,.520),(-.110,.340)]
THROAT=[(-.043,.274),(0,.205),(.043,.274)]
assert all(area(p)>0 for p in [OUTER,INNER,THROAT])
HBOUND=offset(INNER,.004)
HOLES=[]
for i in range(6):
 for j in range(8):
  x=-.104+i*.208/6;z=.296+j*.268/8;h=intersect([(x+.0015,z+.0015),(x+.208/6-.0015,z+.0015),(x+.208/6-.0015,z+.268/8-.0015),(x+.0015,z+.268/8-.0015)],HBOUND)
  if h:HOLES.append(h)

INSET=.0004
assert len(HOLES)==48

def model(outer,holes,depth,grid,mat,role):
 q=extrude(region(outer,holes,grid),-depth,depth)
 return dict(vertices=q['vertices'],faces=q['faces'],face_materials=[mat]*len(q['faces']),face_tags=['CompleteFinitePlanarRegionBoundary']*len(q['faces']),material=mat,role=role)
G[BODY]=model(OUTER,[INNER,THROAT],.012,False,0,'Whole genus2 frame, triangular throat, two neck branches and long flared-butt handle, with no hidden internal faces.')
G[HANDLE]=model(INNER,HOLES,.0015,True,1,'Whole connected thin planar48-hole lattice; all node crossings are one union boundary, not overlapping bars or transparent sheets.')
for name,p,hs,d,grid in [(BODY,OUTER,[INNER,THROAT],.012,False),(HANDLE,INNER,HOLES,.0015,True)]:
 SOLID_VOLUMES[name+'_WholeParallelInset']=dict(model(offset(p,INSET),[offset(h,-INSET)for h in hs],d-INSET,grid,0,'Complete inward parallel profile-and-thickness counterpart; entire nonconvex material including every grid node. Mitered plane offset, not claimed exact spherical erosion.'),targets=[name])
def inset_convex(poly,d):
 # Entire intersection of inward shifted half-planes. Vanished corner edges
 # are intentionally removed; adjacent-line offsets are unsafe for tiny clips.
 margin=1.;p=[(-margin,-margin),(margin,-margin),(margin,margin),(-margin,margin)]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  e=sub(b,a);length=norm(e);delta=(-e[1]*d/length,e[0]*d/length)
  p=cut(p,add(a,delta),add(b,delta))
 assert len(p)>=3 and area(p)>1e-10
 return p
def air(poly,role,targets=None):return dict(model(inset_convex(poly,INSET),[],.020,False,0,role),targets=targets)
for i,p in enumerate(HOLES):VOID_VOLUMES['WholeLatticeThroughHole%02d'%i]=air(p,'Entire inward-offset hole, extended20mm both sides beyond all frame/lattice faces.')
VOID_VOLUMES['WholeTriangularOpenThroat']=air(THROAT,'Entire triangular throat extended beyond both frame faces.')
ISOLATED_VOID_VOLUMES['WholeFrameHeadApertureOnly']=air(INNER,'Complete isolated frame aperture. Targets frame ONLY; assembled head deliberately contains lattice material.',targets=[BODY])
for i,(a,b)in enumerate(zip(INNER,INNER[1:]+INNER[:1])):
 u=unit((b[0]-a[0],0,b[1]-a[1]));v=(0,1,0);axis=cross(u,v);p=(a[0],0,a[1]);plane=dot(axis,p);A=norm(sub(b,a))*.003
 patch=[(a[0],-.0015,a[1]),(b[0],-.0015,b[1]),(b[0],.0015,b[1]),(a[0],.0015,a[1])]
 CONTACTS.append(dict(name='WholeInnerWallSeat%02d'%i,a=BODY,b=HANDLE,origin_m=(0,0,0),axis=axis,u=u,v=v,plane_m=plane,points=[((a[0]+b[0])/2,0,(a[1]+b[1])/2)],complete_interface_polygons_m=[patch],complete_interface_area_m2=A,minimum_patch_area_m2=A-2e-7,interior_probe_offset_m=.0003,finite_patch_count=1))
FEET=[BODY];SOLE_AREAS={BODY:.048*.024};EXPECTED_EULER={BODY:-2,HANDLE:-94};COMPONENT_PAIRS=list(itertools.combinations(sorted(G),2));CONTACT_PAIR_SET={frozenset((BODY,HANDLE))};NONCONTACT_PAIRS=[]
INSIDE_TESTS=[(BODY,(0,0,.100),(.05,0,.100)),(HANDLE,(0,0,.430),(0,.002,.430))]
for i,p in enumerate(HOLES+[THROAT]):
 x,z=(sum(q[k]for q in p)/len(p)for k in range(2));GAPS.append(dict(name='SupplementaryThroughRay%02d'%i,origin_m=(x,-.05,z),direction=(0,1,0),length_m=.1))
BORES=[dict(mesh=BODY,origin_m=(0,-.05,.43),direction=(0,1,0),length_m=.1)]
CONTRACT=dict(single_prop_count=1,new_scene_count=0,kind='prop',original_numeric_whole=True,native_axis_up='Z',front_direction='-Y',origin='horizontal bounds-centred ground',closed_meshes=2,materials=2,open_frame_genus=2,lattice_genus=48,complete_lattice_holes=48,complete_throat_holes=1,whole_material_volumes=2,whole_assembled_air_volumes=49,whole_isolated_through_bores=1,finite_opposed_contacts=8,complete_disjoint_contact_patches=8,component_noncontact_pairs=0,complete_component_pair_universe=1,whole_ground_soles=1,old_geometry_imports=0,fixed_visual_only=True)
def measure_racket_geometry(vertices):
 assert set(vertices)==set(G);vv=[p for vs in vertices.values()for p in vs];lo=[min(p[i]for p in vv)for i in range(3)];hi=[max(p[i]for p in vv)for i in range(3)];assert abs(lo[2])<2e-7 and max(abs(hi[i]+lo[i])for i in range(2))<2e-7
 return dict(CONTRACT,bounds_m=[hi[i]-lo[i]for i in range(3)],whole_ground_bottom_areas_m2=SOLE_AREAS,complete_inner_seating_area_m2=sum(r['complete_interface_area_m2']for r in CONTACTS),scope='Producer geometry only. Whole material,49 assembled air,1 isolated frame air and8 full seats require independent SOURCE and actual predicates. No sporting or safety claim.')
FOCUS=(0,0,.291);ORTHO=.76
CAMERAS={'gray-front3q':(.62,-1.55,.78),'gray-back3q':(-.62,1.55,.78),'thumbnail':(.62,-1.55,.78),'qa-front':(0,-1.55,.70),'qa-side':(1.55,0,.70),'qa-top':(0,0,1.85),'qa-back':(0,1.55,.70),'qa-wireframe':(-.62,1.55,.78),'silhouette-128-front':(0,-1.55,.70),'silhouette-128-side':(1.55,0,.70)}
WIRE_THICKNESS=ORTHO/2500
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
root=bpy.data.objects.new('OneOpenThroatLatticeTennisRacket',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='one full handle butt sole at Z=0; full inner-rim lattice seating,49 real assembled through-holes';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert abs(area-SOLE_AREAS[name])<2e-9,(name,area,SOLE_AREAS[name]);supports.append({'name':name,'area_m2':area,'triangles':patch})
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
mount_evidence=measure_racket_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'racket_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; maker product gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/sports/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'sports','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
