"""New original unglazed three-face bay display frame. Pure SOURCE prefix.
Generic guarded Blender export/render tail is adapted from the reviewed register;
no prior object geometry is imported. Shape is a new planar cell boundary.
"""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='retail-three-face-unglazed-bay-window-01';VERSION='1.0.0';TITLE='Three-Face Unglazed Bay Display Frame'
DESCRIPTION=('One original static unglazed commercial bay-display frame module, counted once. A complete outward-projecting six-sided platform, flat deep crown and continuous finite frame form three genuinely open display windows facing three distinct horizontal directions around one shared deep empty chamber. The rear has a complete broad open access/interface; the bottom is a closed display platform with a full six-sided ground sole, not an open underbody. One closed connected editable material mesh with three handles in its topological boundary, two opaque untextured constant PBR face-role colours. All outlines, apertures and volumes are newly authored; no old shop-house display window, flat wall frame, glass vitrine, counter cabinet or dormer component is imported or extracted. Native metres, Z up, front -Y, complete horizontal-bounds-centred ground origin. This is specifically an unglazed frame-and-platform module, not a complete enclosed glass showcase or shop. There is no glass, door, glazing material, host wall, merchandise, internal shelf, signage, texture, animation, scene, physical display capacity, practical access, insertion path, installation, old-family fit, weather protection, security, load, structural, manufacture or building-safety certification. The full rear plane is only this new asset’s mathematical datum, not proof of any external host connection.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};ISOLATED_VOID_VOLUMES={};FEET=[];FOOT_CONTACTS=[]
BODY='WholeThreeFaceUnglazedBayDisplayFrame'
PALETTE=[('BayFrame_MutedPetrol',(.09,.22,.23,1),.76,.08),('BayPlatformCrown_WarmIvory',(.69,.63,.49,1),.82,.0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def norm(a):return math.sqrt(sum(x*x for x in a))
def unit(a):return mul(a,1/norm(a))
def cross2(a,b):return a[0]*b[1]-a[1]*b[0]
P=[(-1.,.4),(-1.,0.),(-.6,-.4),(.6,-.4),(1.,0.),(1.,.4)]
WALL=.1;FLOOR=.3;CEILING=2.02;HEIGHT=2.14;LOW=.38;HIGH=1.90;MARGIN=.09

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def area(p):return sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(p,p[1:]+p[:1]))/2

def clean(poly):
 out=[]
 for p in poly:
  p=tuple(round(x,10)for x in p)
  if not out or p!=out[-1]:out.append(p)
 if len(out)>1 and out[-1]==out[0]:out.pop()
 return out

def clip(poly,line):
 a,b,c=line;out=[]
 if not poly:return []
 p=poly[-1];dp=a*p[0]+b*p[1]-c
 for q in poly:
  dq=a*q[0]+b*q[1]-c
  if (dp<=1e-11)!=(dq<=1e-11):
   t=dp/(dp-dq);out.append(tuple(p[k]+t*(q[k]-p[k])for k in range(2)))
  if dq<=1e-11:out.append(q)
  p=q;dp=dq
 out=clean(out)
 return out if len(out)>=3 and area(out)>1e-12 else []

def planes(poly,offset=0):
 out=[]
 for p,q in zip(poly,poly[1:]+poly[:1]):
  ux,uy=sub(q,p);n=math.hypot(ux,uy);a,b=uy/n,-ux/n;out.append((a,b,a*p[0]+b*p[1]-offset))
 return out

def intersection(lines):
 poly=[(-3.,-3.),(3.,-3.),(3.,3.),(-3.,3.)]
 for line in lines:poly=clip(poly,line)
 assert poly
 return poly

def window(index,e=0):
 p=P[index];q=P[(index+1)%6];v=sub(q,p);length=math.hypot(*v);u=tuple(x/length for x in v);n=(-u[1],u[0]);up=dot(u,p);np=dot(n,p)
 lines=[(u[0],u[1],up+length-MARGIN+e),(-u[0],-u[1],-up-MARGIN+e),(n[0],n[1],np+WALL+.04+e),(-n[0],-n[1],-np+.06+e)]
 return dict(index=index,u=u,n=n,p=p,length=length,lines=lines,z=(LOW-e,HIGH+e))

def make(e=0):
 outer=planes(P,e);inner=planes(P,WALL-e);cuts=[window(i,e)for i in[1,2,3]]
 rear=[(1.,0.,.9+e),(-1.,0.,.9+e),(0.,-1.,-.29+e),(0.,1.,.5+e)]
 cuts.append(dict(index='rear',lines=rear,z=(FLOOR-e,CEILING+e)))
 lines=inner+[l for c in cuts for l in c['lines']];cells=[intersection(outer)]
 for line in lines:
  nextcells=[]
  for poly in cells:
   ds=[line[0]*x+line[1]*y-line[2]for x,y in poly]
   if min(ds)<-1e-9 and max(ds)>1e-9:
    p=clip(poly,line);q=clip(poly,tuple(-v for v in line));assert p and q;nextcells +=[p,q]
   else:nextcells.append(poly)
  cells=nextcells
 edgecells=collections.defaultdict(list)
 for i,poly in enumerate(cells):
  for a,b in zip(poly,poly[1:]+poly[:1]):edgecells[tuple(sorted((a,b)))].append(i)
 assert all(len(v)<=2 for v in edgecells.values())
 levels=sorted({e,FLOOR-e,LOW-e,HIGH+e,CEILING+e,HEIGHT-e});occupied=[]
 def within(p,ls):return all(a*p[0]+b*p[1]<=c+1e-9 for a,b,c in ls)
 for z0,z1 in zip(levels,levels[1:]):
  z=(z0+z1)/2;s=set()
  for i,poly in enumerate(cells):
   p=tuple(sum(v[k]for v in poly)/len(poly)for k in[0,1]);empty=(FLOOR-e<z<CEILING+e and within(p,inner))or any(c['z'][0]<z<c['z'][1]and within(p,c['lines'])for c in cuts)
   if not empty:s.add(i)
  occupied.append(s)
 vertices=[];faces=[];lookup={};mats=[]
 def vid(p):
  p=tuple(round(x,10)for x in p)
  if p not in lookup:lookup[p]=len(vertices);vertices.append(p)
  return lookup[p]
 def tri(points,mat):
  f=tuple(vid(p)for p in points);assert len(set(f))==3;assert math.sqrt(dot(cross(sub(points[1],points[0]),sub(points[2],points[0])),cross(sub(points[1],points[0]),sub(points[2],points[0]))))>1e-12
  faces.append(f);mats.append(mat)
 for k,s in enumerate(occupied):
  z0,z1=levels[k:k+2]
  for i in sorted(s):
   poly=cells[i];cen=tuple(sum(p[a]for p in poly)/len(poly)for a in[0,1]);mat=int(k in[0,len(occupied)-1])
   for z,sgn,adj in[(z0,-1,k-1),(z1,1,k+1)]:
    if not 0<=adj<len(occupied)or i not in occupied[adj]:
     for a,b in zip(poly,poly[1:]+poly[:1]):
      points=[(*cen,z),(*a,z),(*b,z)];tri(points if sgn>0 else points[::-1],mat)
   for a,b in zip(poly,poly[1:]+poly[:1]):
    others=edgecells[tuple(sorted((a,b)))];neighbor=next((j for j in others if j!=i),None)
    if neighbor is None or neighbor not in s:
     aa=(*a,z0);bb=(*b,z0);cc=(*b,z1);dd=(*a,z1);tri([aa,bb,cc],mat);tri([aa,cc,dd],mat)
 return dict(vertices=vertices,triangles=faces,face_materials=mats,xy_cell_count=len(cells),z_levels=levels,scope='New pure boundary prototype only; no source or actual product approval.')

def whole_geometry(e=0):
 g=make(e);return dict(vertices=g['vertices'],faces=g['triangles'],face_materials=g['face_materials'],face_tags=['CompleteFiniteBayBoundary']*len(g['triangles']),material=0,role='Whole finite bay frame or parallel-face full material inset; no internal cell faces, rounded erosion claim or imported geometry.')
def convex_prism(poly,z0,z1,role):
 assert area(poly)>0;v=[(x,y,z)for z in[z0,z1]for x,y in poly];n=len(poly);f=[]
 for i in range(1,n-1):f.extend([(0,i+1,i),(n,n+i,n+i+1)])
 for i in range(n):j=(i+1)%n;f.extend([(i,j,j+n),(i,j+n,i+n)])
 return dict(vertices=v,faces=f,face_materials=[0]*len(f),material=0,role=role)
G[BODY]=whole_geometry();SOLID_VOLUMES['EntireParallelInsetBayMaterial']=dict(whole_geometry(.001),targets=[BODY]);FEET=[BODY];EXPECTED_EULER={BODY:-4}
AIR_CLEARANCE=.001
inner_poly=intersection(planes(P,WALL+AIR_CLEARANCE))
VOID_VOLUMES['WholeSharedDisplayChamber']=dict(convex_prism(inner_poly,FLOOR+AIR_CLEARANCE,CEILING-AIR_CLEARANCE,'Complete finite six-sided shared chamber, not a central box.'),targets=[BODY])
PORTS=[]
for i,label in[(1,'LeftOblique'),(2,'Front'),(3,'RightOblique')]:
 w=window(i);u,n,p,length=w['u'],w['n'],w['p'],w['length'];a=MARGIN+AIR_CLEARANCE;b=length-MARGIN-AIR_CLEARANCE
 # CCW in (tangent,inward) coordinates; complete opening including exterior and inner overlap.
 poly=[add(p,add(mul(u,s),mul(n,d)))for s,d in[(a,-.05),(b,-.05),(b,WALL+.002),(a,WALL+.002)]]
 key='Whole'+label+'WindowEgress';VOID_VOLUMES[key]=dict(convex_prism(poly,LOW+AIR_CLEARANCE,HIGH-AIR_CLEARANCE,'Entire window along its own tangent and normal, overlapping shared chamber with positive volume.'),targets=[BODY]);PORTS.append(dict(name=key,index=i,normal_inward=n,entire_tangent_interval=[a,b],inward_interval=[-.05,WALL+.002],height=[LOW+AIR_CLEARANCE,HIGH-AIR_CLEARANCE]))
poly=[(-.899,.298),(.899,.298),(.899,.46),(-.899,.46)]
VOID_VOLUMES['WholeRearOpeningEgress']=dict(convex_prism(poly,FLOOR+AIR_CLEARANCE,CEILING-AIR_CLEARANCE,'Complete rear opening with positive-volume overlap into the shared interior.'),targets=[BODY]);PORTS.append(dict(name='WholeRearOpeningEgress',normal_inward=(0,-1),entire_x=[-.899,.899],entire_y=[.298,.46],height=[FLOOR+AIR_CLEARANCE,CEILING-AIR_CLEARANCE]))
ATTACHMENT=dict(plane_equation='Y=0.4',normal=(0,1,0),outer_xz=[(-1.,0.),(1.,0.),(1.,HEIGHT),(-1.,HEIGHT)],open_xz=[(-.9,FLOOR),(.9,FLOOR),(.9,CEILING),(-.9,CEILING)],complete_area_m2=1.184,actual_host_included=False,old_family_compatibility=False)
CONTRACT=dict(single_modular_count=1,single_prop_count=0,new_scene_count=0,kind='modular',original_numeric_whole=True,native_axis_up='Z',front_direction='-Y',origin='complete horizontal bounds centre, whole six-sided sole at Z0',closed_connected_meshes=1,materials=2,noncoplanar_front_window_directions=3,whole_rear_ports=1,whole_material_volumes=1,whole_air_volumes=5,finite_opposed_contacts=0,all_unordered_pairs=0,contact_pairs=0,noncontact_pairs=0,whole_ground_soles=1,complete_ground_area_m2=1.44,whole_rear_attachment=ATTACHMENT,material_euler=-4,old_geometry_imports=0,fixed_visual_only=True,explicitly_unglazed=True)
def measure_bay_geometry(vertices):
 assert set(vertices)=={BODY};v=vertices[BODY];lo=[min(p[k]for p in v)for k in range(3)];hi=[max(p[k]for p in v)for k in range(3)];assert abs(lo[2])<2e-7 and max(abs(lo[k]+hi[k])for k in[0,1])<2e-7
 return dict(CONTRACT,bounds_m=[hi[k]-lo[k]for k in range(3)],scope='Producer geometry only. Full finite air/material/datum and actual source-GLB binding remain independent maker product predicates. No host fit.')
INSIDE_TESTS=[(BODY,(0,0,.15),(0,0,1.))]
FOCUS=(0,0,1.07);ORTHO=3.3
CAMERAS={'gray-front3q':(4,-6,4.2),'gray-back3q':(-4,6,4.2),'thumbnail':(4,-6,4.2),'qa-front':(0,-6,2.3),'qa-side':(6,0,2.3),'qa-top':(0,0,7),'qa-back':(0,6,2.3),'qa-wireframe':(4,-6,4.2),'silhouette-128-front':(0,-6,2.3),'silhouette-128-side':(6,0,2.3)}
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
root=bpy.data.objects.new('OneThreeFaceUnglazedBayDisplayFrame',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole six-sided platform sole at Z=0; three distinct-facing open windows and entire rear mathematical interface; no glass or host fit';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_bay_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_modular_count':1,'single_prop_count':0,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'three_face_bay_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; maker product gates pending'}
qa['modularity']={'own_rear_datum':ATTACHMENT,'placement':'Full own six-sided sole at Z0. Rear datum Y=.4; no host or old-family compatibility. No repeat grid asserted.'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/retail/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'modular','theme':'retail','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
 qa['tiered_render']={'profile_id':TIER_PROFILE,'authorization_reference':'Current separately pinned R3 operation approval; historical sample contract retained, no old approval replay.','native_samples':128,'resolution':[640,640],'gray_stage':'omitted_by_authorized_profile','samples_by_image':{}}
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
