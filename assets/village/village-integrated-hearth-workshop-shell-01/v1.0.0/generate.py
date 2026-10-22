"""Original integral roofed hearth-workshop visual shell. Draft, not SOURCE approved."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='village-integrated-hearth-workshop-shell-01';VERSION='1.0.0';TITLE='Integrated Hearth Workshop Space Shell'
DESCRIPTION='One original static roofed workshop-space shell: broad open front leads into a complete floor, three thick enclosing walls and flat thick roof; an integral raised rear hearth supports a genuinely open contracting hood and a continuous empty flue through its own roof. One continuous closed shared-vertex material boundary, not a house plus overlapping stove or decorative chimney. Complete parallel-face inset material and the entire connected front-room-hood-flue air are represented as finite domains. One modular visual shell, zero scenes, no loose equipment, tools, fuel or imported earlier asset geometry. Native metres, Z up, front -Y, XY bounds-centred origin and full rectangular flat ground sole. Two opaque constant untextured face-role PBR materials. This is an unoccupied game-art workspace shell, not a fully equipped or functioning workshop. No fire, heat, combustion, smoke or ventilation simulation, real access, ergonomics, installation fit, weather exclusion, structural load, fire resistance, manufacture, building-code or safety certification. No texture, logo, text, moving parts, animation or performance claim.'
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};ISOLATED_VOID_VOLUMES={};FEET=[];FOOT_CONTACTS=[]
BODY='WholeIntegralHearthWorkshopSpace'
PALETTE=[('Workshop_BaseStone',(.30,.34,.35,1),.88,0.),('Workshop_WarmMasonry',(.60,.46,.31,1),.86,0.)]
def norm(a):return math.sqrt(sum(x*x for x in a))
def unit(a):return tuple(x/norm(a)for x in a)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
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
 poly=[(-5.,-1.),(5.,-1.),(5.,5.),(-5.,5.)]
 for line in lines:poly=clip(poly,line)
 assert poly
 return poly


def rect(x0,z0,x1,z1):return [(x0,z0),(x1,z0),(x1,z1),(x0,z1)]
# Full original nominal boundaries, in metres. Counterclockwise XZ regions.
MAIN=rect(-2.,0.,2.,2.85)
ROOM=rect(-1.8,.15,1.8,2.65)
DOOR=rect(-1.6,.15,1.6,2.30)
HEARTH=rect(-1.1,0.,1.1,.85)
HOOD=[(-1.1,1.7),(1.1,1.7),(.55,2.55),(.55,3.8),(-.55,3.8),(-.55,2.55)]
THROAT=[(-.9,1.7),(.9,1.7),(.35,2.55),(.35,3.9),(-.35,3.9),(-.35,2.55)]
# HOOD is concave at shoulders; partition into lower convex trap + upper rectangle.
HOOD_LO=[(-1.1,1.7),(1.1,1.7),(.55,2.55),(-.55,2.55)]
HOOD_HI=rect(-.55,2.45,.55,3.8)
THROAT_LO=[(-.9,1.69),(.9,1.69),(.35,2.55),(-.35,2.55)]
THROAT_HI=rect(-.35,2.45,.35,3.9)

def make(e=0, mode="material"):
 assert mode in ["material","air"]
 if mode=="air":assert e<0
 specs={
  'main':(MAIN,(-1.7,1.7)), 'room':(ROOM,(-1.5,1.5)),
  'door':(DOOR,(-1.8,-1.49)), 'hearth':(HEARTH,(.65,1.7)),
  'hoodlo':(HOOD_LO,(.65,1.7)), 'hoodhi':(HOOD_HI,(.65,1.7)),
  'throatlo':(THROAT_LO,(.85,1.5)), 'throathi':(THROAT_HI,(.85,1.5))}
 nominal={k:(planes(p),ys)for k,(p,ys)in specs.items()}
 specs={k:(planes(p,(-e if k in ['room','door','throatlo','throathi'] else e)),(ys[0]+(-e if k in ['room','door','throatlo','throathi'] else e),ys[1]-(-e if k in ['room','door','throatlo','throathi'] else e)))for k,(p,ys)in specs.items()}
 # Global line arrangement ensures adjoining finite faces have identical subdivisions.
 lines=[]
 for ls,ys in list(specs.values())+(list(nominal.values())if mode=="air"else[]):
  for q in ls:
   if not any(max(abs(a-b)for a,b in zip(q,r))<1e-10 for r in lines):lines.append(q)
 cells=[rect(-2.1,-.1,2.1,4.)]
 for line in lines:
  after=[]
  for poly in cells:
   ds=[line[0]*x+line[1]*z-line[2]for x,z in poly]
   if min(ds)<-1e-9 and max(ds)>1e-9:
    p=clip(poly,line);q=clip(poly,tuple(-v for v in line));assert p and q;after +=[p,q]
   else:after.append(poly)
  cells=after
 edgecells=collections.defaultdict(list)
 for i,poly in enumerate(cells):
  for a,b in zip(poly,poly[1:]+poly[:1]):edgecells[tuple(sorted((a,b)))].append(i)
 assert all(len(v)<=2 for v in edgecells.values())
 levels=sorted({y for ls,ys in list(specs.values())+(list(nominal.values())if mode=="air"else[])for y in ys});occupied=[]
 for y0,y1 in zip(levels,levels[1:]):
  y=(y0+y1)/2;s=set()
  for i,poly in enumerate(cells):
   p=tuple(sum(v[k]for v in poly)/len(poly)for k in[0,1])
   inside={k:ys[0]<y<ys[1]and all(a*p[0]+b*p[1]<=c+1e-9 for a,b,c in ls)for k,(ls,ys)in specs.items()}
   solid=((inside['main'] and not(inside['room']or inside['door']))or inside['hearth']or inside['hoodlo']or inside['hoodhi'])and not(inside['throatlo']or inside['throathi'])
   if mode=='air':
    interior=any(nominal[key][1][0]<y<nominal[key][1][1]and all(a*p[0]+b*p[1]<=c+1e-9 for a,b,c in nominal[key][0])for key in ['room','door','throatlo','throathi'])
    solid=interior and not solid
   if solid:s.add(i)
  occupied.append(s)
 vertices=[];faces=[];lookup={};mats=[]
 def vid(p):
  p=tuple(round(x,10)for x in p)
  if p not in lookup:lookup[p]=len(vertices);vertices.append(p)
  return lookup[p]
 def tri(points,mat):
  f=tuple(vid(p)for p in points);assert len(set(f))==3;faces.append(f);mats.append(mat)
 # Mapping (X,Z,Y) to (X,Y,Z) reverses orientation; emit opposite original bay winding.
 for k,s in enumerate(occupied):
  y0,y1=levels[k:k+2]
  for i in sorted(s):
   poly=cells[i];cen=tuple(sum(p[a]for p in poly)/len(poly)for a in[0,1]);mat=1 if cen[1]>.84 else 0
   for y,sgn,adj in[(y0,-1,k-1),(y1,1,k+1)]:
    if not 0<=adj<len(occupied)or i not in occupied[adj]:
     for a,b in zip(poly,poly[1:]+poly[:1]):
      pts=[(cen[0],y,cen[1]),(a[0],y,a[1]),(b[0],y,b[1])];tri(pts[::-1]if sgn>0 else pts,mat)
   for a,b in zip(poly,poly[1:]+poly[:1]):
    neighbor=next((j for j in edgecells[tuple(sorted((a,b)))]if j!=i),None)
    if neighbor is None or neighbor not in s:
     aa=(a[0],y0,a[1]);bb=(b[0],y0,b[1]);cc=(b[0],y1,b[1]);dd=(a[0],y1,a[1]);tri([cc,bb,aa],mat);tri([dd,cc,aa],mat)
 return dict(vertices=vertices,faces=faces,face_materials=mats,arrangement_cells=len(cells),y_levels=levels)

def payload(e=0,mode='material'):
 g=make(e,mode);g.update(material=0,role='Whole literal CSG workshop boundary; full parallel-face domain, not sampled boxes or Euclidean rounded erosion.');return g
G[BODY]=payload();SOLID_VOLUMES['WholeInsetWorkshopMaterial']=dict(payload(.004),targets=[BODY]);VOID_VOLUMES['WholeFrontRoomHoodFlueAir']=dict(payload(-.004,'air'),targets=None)
EXPECTED_EULER={BODY:0};FEET=[BODY]
INSIDE_TESTS=[(BODY,(-1.9,0,1),(0,0,1))]
GAPS=[dict(name='SupplementalFrontToRoom',origin_m=(0,-1.8,1.1),direction=(0,1,0),length_m=3.2),dict(name='SupplementalHearthAboveToFlue',origin_m=(0,1.1,.9),direction=(0,0,1),length_m=3.)]
CONTRACT=dict(single_modular_count=1,single_prop_count=0,new_scene_count=0,kind='modular',native_axis_up='Z',front_direction='-Y',origin='XY bounds centred; full sole on Z0',closed_meshes=1,materials=2,material_euler=0,whole_material_domains=1,whole_connected_air_domains=1,complete_internal_contacts=0,full_front_port=1,full_upper_flue_port=1,whole_flat_sole_area_m2=13.6,old_geometry_imports=0,fixed_visual_only=True,fully_equipped_or_functioning_workshop=False)
def measure_workshop_geometry(vertices):
 assert set(vertices)=={BODY};v=vertices[BODY];lo=[min(p[i]for p in v)for i in range(3)];hi=[max(p[i]for p in v)for i in range(3)]
 assert max(abs(a-b)for a,b in zip(lo,[-2,-1.7,0]))<2e-7 and max(abs(a-b)for a,b in zip(hi,[2,1.7,3.8]))<2e-7
 return dict(CONTRACT,bounds_m=[hi[i]-lo[i]for i in range(3)])
def check_complete_ground_sole(triangles):
 total=0
 for t in triangles:
  n=cross(sub(t[1],t[0]),sub(t[2],t[0]))
  assert all(p[2]>=-2e-7 for p in t)
  if max(abs(p[2])for p in t)<2e-7 and n[2]<0:
   assert all(-2-2e-7<=p[0]<=2+2e-7 and -1.7-2e-7<=p[1]<=1.7+2e-7 for p in t);total+=norm(n)/2
 assert abs(total-13.6)<2e-6
 return dict(complete_flat_sole_area_m2=total,finite_footprint_rectangle=[-2,-1.7,2,1.7],scope='Whole sole boundary only; no real ground/structural or stability claim')
FOCUS=(0,0,1.8);ORTHO=6.5
CAMERAS={'gray-front3q':(4.5,-10,3.5),'gray-back3q':(-7,10,6),'thumbnail':(4.5,-10,3.5),'qa-front':(0,-10,3.5),'qa-side':(10,0,4.5),'qa-top':(0,0,12),'qa-back':(0,10,4.5),'qa-wireframe':(4.5,-10,3.5),'silhouette-128-front':(0,-10,3.5),'silhouette-128-side':(10,0,4.5)}
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
root=bpy.data.objects.new('OneIntegralHearthWorkshopShell',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='full rectangular ground sole; continuous room-hood-through-roof-flue; static unoccupied space shell, no real building performance';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
complete_sole=check_complete_ground_sole(actual_triangles[id(trees[BODY])]);assert FEET==[BODY]
seen={BODY};todo=list(seen)
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
mount_evidence=measure_workshop_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'components':component_checks,'connection_interior_points':joints,'all_meshes_connected_to_whole_ground_sole':sorted(seen),'complete_ground_sole':complete_sole,
 'single_modular_count':1,'single_prop_count':0,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'workshop_space_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; maker product gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/village/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'architecture','assetKind':'modular','theme':'village','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-6,-8,10),1800,7),('Fill',(7,-5,7),1200,6),('Rim',(4,7,9),1600,5)]:
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
