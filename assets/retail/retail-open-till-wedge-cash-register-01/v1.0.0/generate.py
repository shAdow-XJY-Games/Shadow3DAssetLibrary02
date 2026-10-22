"""New original static open-till register. Pure numerical SOURCE prefix.
Generic vector/mesh/offset/ear-clipping/contact utilities derived from the independently
reviewed current transport source; NO old asset geometry/coordinates imported.
"""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='retail-open-till-wedge-cash-register-01';VERSION='1.0.0';TITLE='Open-Till Wedge Cash Register'
DESCRIPTION=('One original fixed-open low-poly cash-register appearance, counted as one prop. One connected thick chassis integrates a ground base, a genuinely open-front drawer bay, a broad sloping keyboard deck and a raised rear display surround with a real blind recess. One independently editable continuous shallow till has three empty upward wells, integral partitions and a full floor. Its rear underside seats over a complete finite chassis-floor patch while the front extends beyond the opening; the rear part is obscured by the chassis roof in this fixed pose. Twelve separate solid chamfer-ended keycaps seat over complete sloping bases in a three-column four-row arrangement. A thick opaque unlit display plate seats against the blind recess back wall, with real remaining front and border gaps. Fifteen closed connected named meshes, three constant opaque untextured PBR materials, metres, native Z up, front -Y, complete assembly horizontal-bounds-centred ground origin. Every component profile and position is newly authored. No old cabinet, scale, caddy, chart-console or dispenser geometry is imported. No numbers, words, logo, currency, receipt, loose cash, cables, animation, counter or surrounding scene. The whole register counts once; keys, till and display are not separate assets. Static visual geometry only: no payment, accounting, scanning, networking, money storage or security, key or display operation, drawer motion, insertion or assembly path, stability, load or capacity, ergonomics, manufacture or safety certification. Complete finite contacts and air clearances do not establish practical performance. No compatibility with earlier scanner, cafe appliance, counter or scene is asserted.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};ISOLATED_VOID_VOLUMES={};FEET=[];FOOT_CONTACTS=[]
BODY='IntegralBayDeckDisplayChassis';TILL='ContinuousThreeWellExtendedTill';SCREEN='OpaqueRecessedUnlitDisplay';KEYS=[]
PALETTE=[('Chassis_MutedPetrol',(.07,.19,.20,1),.64,.12),('KeysTill_WarmIvory',(.71,.66,.52,1),.72,.0),('Screen_UnlitGraphite',(.025,.045,.05,1),.48,.0)]
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
  assert all(len(v)==2 for v in edges.values()),'not closed'
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

def cross2(a,b):return a[0]*b[1]-a[1]*b[0]

def polygon_area2(poly):return sum(cross2(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly)))

def inset_polygon(poly,d):
 """Parallel-offset every complete edge; intersection of adjacent inward lines."""
 assert polygon_area2(poly)>0
 if d==0:return list(poly)
 lines=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  e=sub(b,a);l=norm(e);n=(-e[1]/l,e[0]/l);lines.append((add(a,mul(n,d)),e))
 out=[]
 for i,(p,e) in enumerate(lines):
  q,f=lines[i-1];den=cross2(e,f);assert abs(den)>1e-10
  out.append(add(p,mul(e,cross2(sub(q,p),f)/den)))
 return out

def planar_ears(poly):
 assert polygon_area2(poly)>0
 order=list(range(len(poly)));out=[]
 while len(order)>3:
  found=False
  for i,b in enumerate(order):
   a=order[i-1];c=order[(i+1)%len(order)];pa,pb,pc=[poly[k] for k in (a,b,c)]
   if cross2(sub(pb,pa),sub(pc,pb))<=1e-13:continue
   def inside2(p):return all(cross2(sub(y,x),sub(p,x))>=-1e-13 for x,y in [(pa,pb),(pb,pc),(pc,pa)])
   if any(inside2(poly[j]) for j in order if j not in (a,b,c)):continue
   out.append((a,b,c));order.pop(i);found=True;break
  assert found,'non-simple or degenerate full polygon'
 out.append(tuple(order));return out

def prism_xy(poly,z0,z1,material,role):
 m=Mesh();bottom=[(x,y,z0) for x,y in poly];top=[(x,y,z1) for x,y in poly]
 for face in planar_ears(poly):
  m.tri([bottom[i] for i in reversed(face)],material,'WholeLowerFiniteFace');m.tri([top[i] for i in face],material,'WholeUpperFiniteFace')
 for i in range(len(poly)):
  j=(i+1)%len(poly);m.quad(bottom[i],bottom[j],top[j],top[i],material,'CompleteFiniteProfileSide')
 return m.result(role)

def box(lo,hi,mat=3,role='Complete closed rectangular solid'):
 x0,y0,z0=lo;x1,y1,z1=hi;return prism_xy([(x0,y0),(x1,y0),(x1,y1),(x0,y1)],z0,z1,mat,role)

def contact(n,a,b,axis,point,area):
 axis=unit(axis);e=tuple(1. if j==min(range(3),key=lambda k:abs(axis[k])) else 0. for j in range(3));u=unit(sub(e,mul(axis,dot(e,axis))));v=cross(axis,u);assert abs(dot(u,v))<1e-12 and norm(sub(cross(u,v),axis))<1e-12
 CONTACTS.append(dict(name=n,a=a,b=b,origin_m=(0,0,0),u=u,v=v,axis=axis,plane_m=dot(point,axis),points=[point],minimum_patch_area_m2=area-2e-7,complete_interface_area_m2=area,interior_probe_offset_m=.0004))

# New finite cell boundary algorithm. YZ grid cells are clipped by the exact
# piecewise-linear outer roof; X extrusion faces cancel before triangulation.
# All cut extents enter the grid. No overlapping hidden wall boxes or booleans.
def below_line(poly,m,c):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  fa=a[1]-m*a[0]-c;fb=b[1]-m*b[0]-c
  if fa<=1e-12:out.append(a)
  if (fa>1e-12)!=(fb>1e-12):
   t=fa/(fa-fb);out.append((a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])))
 result=[]
 for p in out:
  if not result or norm(sub(p,result[-1]))>1e-10:result.append(p)
 if len(result)>1 and norm(sub(result[0],result[-1]))<1e-10:result.pop()
 return result

def cell_boundary(xlo,xhi,ylo,yhi,zlo,zhi,cuts,material,role,roof=None):
 xs=sorted(set([xlo,xhi]+[v for a,b in cuts for v in[a[0],b[0]]if xlo<v<xhi]))
 ys=sorted(set([ylo,yhi]+[v for a,b in cuts for v in[a[1],b[1]]if ylo<v<yhi]+([roof[0]]if roof else [])))
 zs=sorted(set([zlo,zhi]+[v for a,b in cuts for v in[a[2],b[2]]if zlo<v<zhi]+([roof[1]*y+roof[2]for y in ys if y<=roof[0] and zlo<roof[1]*y+roof[2]<zhi]if roof else [])))
 faces={}
 def put(face):
  face=[tuple(round(c,9)for c in p)for p in face];key=tuple(sorted(face))
  if key in faces:del faces[key]
  else:faces[key]=face
 for i,j,k in itertools.product(range(len(xs)-1),range(len(ys)-1),range(len(zs)-1)):
  x0,x1=xs[i:i+2];y0,y1=ys[j:j+2];z0,z1=zs[k:k+2];mid=((x0+x1)/2,(y0+y1)/2,(z0+z1)/2)
  if any(all(a[d]<mid[d]<b[d]for d in range(3))for a,b in cuts):continue
  poly=[(y0,z0),(y1,z0),(y1,z1),(y0,z1)]
  if roof and (y0+y1)/2<roof[0]:poly=below_line(poly,roof[1],roof[2])
  if len(poly)<3 or abs(polygon_area2(poly))<1e-14:continue
  ends=[[(x,y,z)for y,z in poly]for x in[x0,x1]]
  put(list(reversed(ends[0])));put(ends[1])
  for q in range(len(poly)):
   r=(q+1)%len(poly);put([ends[0][q],ends[1][q],ends[1][r],ends[0][r]])
 mesh=Mesh()
 for face in faces.values():
  # Cell-face polygons are convex. Triangulate in their own plane, with a
  # deterministic fan, retaining every grid boundary vertex for manifold edges.
  for k in range(1,len(face)-1):mesh.tri([face[0],face[k],face[k+1]],material,'WholeFiniteCellBoundary')
 return mesh.result(role)

SLOPE=4/11;INTERCEPT=.15+.14*SLOPE;CUTS=[((-.16,-.16,.022),(.16,.15,.105)),((-.14,.08,.25),(.14,.12,.315))]
def chassis(inset=0):
 cuts=[(sub(a,(inset,inset,inset)),add(b,(inset,inset,inset)))for a,b in CUTS]
 return cell_boundary(-.18+inset,.18-inset,-.14+inset,.18-inset,inset,.34-inset,cuts,0,'One whole connected chassis: full sole, front-open bay, inclined key deck, integral raised rear blind display surround.',roof=(.08+inset,SLOPE,INTERCEPT-inset*math.sqrt(1+SLOPE*SLOPE)))
G[BODY]=chassis();SOLID_VOLUMES[BODY+'_WholeInsetMaterial']=dict(chassis(.001),targets=[BODY]);FEET=[BODY]
WELLS=[(-.149,-.054),(-.048,.048),(.054,.149)]
def till(inset=0):
 cuts=[((a-inset,-.304-inset,.028-inset),(b+inset,-.056+inset,.12))for a,b in WELLS]
 return cell_boundary(-.155+inset,.155-inset,-.31+inset,-.05-inset,.022+inset,.088-inset,cuts,1,'Complete three shallow blind wells with integral floor, perimeter and two partitions; entire tray in one extended static pose.')
G[TILL]=till();SOLID_VOLUMES[TILL+'_WholeInsetMaterial']=dict(till(.001),targets=[TILL])
contact('TillFullRearUndersideSeat',BODY,TILL,(0,0,1),(0,-.095,.022),.31*.09)
G[SCREEN]=box((-.138,.112,.252),(.138,.12,.313),2,'Thick opaque unlit plate completely recessed inside the real chassis blind pocket, finite rear-wall seat.')
SOLID_VOLUMES[SCREEN+'_WholeInsetMaterial']=dict(box((-.137,.113,.253),(.137,.119,.312),2),targets=[SCREEN])
contact('ScreenFullBackWallSeat',BODY,SCREEN,(0,-1,0),(0,.12,.2825),.276*.061)

def keycap(cx,cy,inset=0):
 # Whole chamfer-ended prism in local X/Y, then exact affine sloping-deck map.
 hx=.029-inset;hy=.014-inset;c=.003
 poly=[(-hx+c,-hy),(hx-c,-hy),(hx,-hy+c),(hx,hy-c),(hx-c,hy),(-hx+c,hy),(-hx,hy-c),(-hx,-hy+c)]
 g=prism_xy(poly,inset,.012-inset,1,'One whole chamfer-ended solid key with complete sloping finite base and clear neighbouring gaps.')
 g['vertices']=[(x+cx,y+cy,z+SLOPE*(y+cy)+INTERCEPT)for x,y,z in g['vertices']]
 return g
for row,cy in enumerate([-.101,-.058,-.015,.028]):
 for col,cx in enumerate([-.09,0,.09]):
  name='SolidSlopedKey_R%dC%d'%(row+1,col+1);KEYS.append(name);G[name]=keycap(cx,cy);SOLID_VOLUMES[name+'_WholeInsetMaterial']=dict(keycap(cx,cy,.001),targets=[name])
  contact(name+'_CompleteBaseSeat',BODY,name,(0,-SLOPE,1),(cx,cy,SLOPE*cy+INTERCEPT),(.058*.028-2*.003*.003)*math.sqrt(1+SLOPE*SLOPE))
for i,(a,b)in enumerate(WELLS,1):
 VOID_VOLUMES['TillWell_%d_WholeInterior'%i]=dict(box((a+.001,-.303,.029),(b-.001,-.057,.087)),targets=None)
 VOID_VOLUMES['TillWell_%d_WholeExposedTopApproach'%i]=dict(box((a+.001,-.303,.087),(b-.001,-.141,.20)),targets=None)
VOID_VOLUMES['WholeBayUpperGap']=dict(box((-.159,-.139,.089),(.159,.149,.104)),targets=None)
VOID_VOLUMES['WholeBayRearEmptySpace']=dict(box((-.159,-.049,.023),(.159,.149,.104)),targets=None)
VOID_VOLUMES['WholeBayLeftSideGap']=dict(box((-.159,-.139,.023),(-.156,-.051,.088)),targets=None)
VOID_VOLUMES['WholeBayRightSideGap']=dict(box((.156,-.139,.023),(.159,-.051,.088)),targets=None)
VOID_VOLUMES['WholeRemainingDisplayPocketAir']=dict(cell_boundary(-.1395,.1395,.0805,.1195,.2505,.3145,[((-.1385,.1115,.2515),(.1385,.1205,.3135))],2,'Entire remaining blind display pocket air: front space AND all four narrow finite border clearances around the seated screen; conservative 0.5 mm inset.'),targets=None)
# Centre the complete NEW assembly's horizontal bounds, preserving relationships.
SHIFT_Y=.065
for mapping in[G,SOLID_VOLUMES,VOID_VOLUMES]:
 for g in mapping.values():g['vertices']=[(x,y+SHIFT_Y,z)for x,y,z in g['vertices']]
for r in CONTACTS:
 r['origin_m']=(0,SHIFT_Y,0);r['points']=[(x,y+SHIFT_Y,z)for x,y,z in r['points']]
FOOT_CONTACTS=[dict(name='CompleteChassisGroundSole',mesh=BODY,x=0,y=.02+SHIFT_Y,half_x=.18,half_y=.16,minimum_area_m2=.36*.32-2e-7)]
EXPECTED_EULER={n:2 for n in G}
CONTRACT=dict(single_prop_count=1,new_scene_count=0,kind='prop',original_numeric_whole=True,native_axis_up='Z',front_direction='-Y',origin='complete assembly horizontal bounds centre; whole chassis sole Z=0',closed_connected_meshes=15,materials=3,true_till_wells=3,individual_keycaps=12,blind_screen_pockets=1,front_open_drawer_bays=1,whole_material_volumes=15,whole_air_volumes=11,finite_opposed_contacts=14,whole_ground_soles=1,all_unordered_pairs=105,contact_pairs=14,noncontact_pairs=91,old_geometry_imports=0,fixed_visual_only=True)
def measure_register_geometry(vertices):
 assert set(vertices)==set(G)
 vv=[p for vs in vertices.values()for p in vs];lo=[min(p[k]for p in vv)for k in range(3)];hi=[max(p[k]for p in vv)for k in range(3)]
 assert abs(lo[2])<2e-7 and all(abs(lo[k]+hi[k])<2e-7 for k in [0,1])
 return dict(CONTRACT,bounds_m=[hi[k]-lo[k]for k in range(3)],scope='Complete new source layout only; actual GLB all finite boundary gates remain required.')
FOCUS=(0,0,.17);ORTHO=.78
CAMERAS={'gray-front3q':(1.2,-1.6,1.15),'gray-back3q':(-1.2,1.6,1.15),'thumbnail':(1.2,-1.6,1.8),'qa-front':(0,-2,.95),'qa-side':(-2,0,.95),'qa-top':(0,0,2.2),'qa-back':(0,2,.95),'qa-wireframe':(-1.2,-1.6,1.8),'silhouette-128-front':(0,-2,.95),'silhouette-128-side':(-2,0,.95)}
WIRE_THICKNESS=ORTHO/1800

INSIDE_TESTS=[(BODY,(0,.02+SHIFT_Y,.011),(0,.02+SHIFT_Y,.06)),(TILL,(0,-.18+SHIFT_Y,.025),(0,-.18+SHIFT_Y,.05)),(SCREEN,(0,.116+SHIFT_Y,.28),(0,.095+SHIFT_Y,.28))]
for name in KEYS:
 vv=G[name]['vertices'];p=tuple((min(v[k]for v in vv)+max(v[k]for v in vv))/2 for k in range(3));INSIDE_TESTS.append((name,p,add(p,(0,0,.03))))

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
root=bpy.data.objects.new('OneOpenTillWedgeCashRegister',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole chassis ground sole at Z=0; one fixed extended three-well till and twelve individually seated keys; static geometry only';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_register_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_modular_count':0,'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'open_till_register_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; maker product gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/retail/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'retail','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
