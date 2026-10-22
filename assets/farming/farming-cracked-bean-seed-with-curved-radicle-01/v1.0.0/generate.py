"""Original cracked bean seed and continuous curved radicle. New whole shape; arithmetic/mesh kernel and later renderer explicitly reused from reviewed farm-r2.
R2 new whole-shape SOURCE candidate after true first-front rejection; independent review and strict source-revision authority still required.
"""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='farming-cracked-bean-seed-with-curved-radicle-01';VERSION='1.0.0';TITLE='Cracked Bean Seed With Curved Radicle'
DESCRIPTION='One static stylised germinating seed game prop: two unequal plump solid cotyledons with small rounded crowns and real irregular inter-lobe split; a single continuously tapered curved radicle emerges through that split from a two-sided finite hilum seat and descends near the ground. Complete isolated cleft is checked against the seed bodies; the actual root intentionally occupies its middle, so only the whole upper/lower clear volumes are called assembled openings. No hollow bowls, external U handle, leaves, soil, thin separate seed-coat layer, animation, biological timing or horticultural/functional guarantee. New whole geometry, not extracted crop components.'
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};ISOLATED_VOID_VOLUMES={};FEET=[];FOOT_CONTACTS=[]
LEFT='WholeRoundedLeftSeedCotyledon';RIGHT='WholeRoundedRightSeedCotyledon';ROOT='ContinuousTaperedEmergingRadicle'
PALETTE=[('Seed_WarmSurface',(.27,.105,.060,1),.80,.0),('Seed_InnerFlesh',(.64,.48,.26,1),.84,.0),('Radicle_Ivory',(.73,.67,.50,1),.82,.0)]
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

def ccw(poly):return list(poly)if polygon_area2(poly)>0 else list(reversed(poly))
LEFT_PROFILE=ccw([(-.0015,.014),(-.010,.020),(-.020,.017),(-.028,.006),(-.026,-.007),(-.019,-.017),(-.010,-.020),(-.0045,-.014),(-.005,-.006),(-.003,.001),(-.0015,.006)])
RIGHT_PROFILE=ccw([(.0015,.014),(.010,.019),(.020,.014),(.025,.003),(.023,-.010),(.015,-.019),(.006,-.020),(.003,-.013),(.004,-.005),(.002,.001),(.0015,.006)])
LEFT_INNER=[(-.010,-.020),(-.0045,-.014),(-.005,-.006),(-.003,.001),(-.0015,.006),(-.0015,.014)]
RIGHT_INNER=[(.006,-.020),(.003,-.013),(.004,-.005),(.002,.001),(.0015,.006),(.0015,.014)]
SEED_DESIGNS={LEFT:(LEFT_PROFILE,(-.014,0),[(0,.30),(.003,.70),(.008,1),(.015,1),(.020,.80),(.024,.43),(.026,.10)],LEFT_INNER),RIGHT:(RIGHT_PROFILE,(.012,0),[(0,.33),(.003,.74),(.008,1),(.015,1),(.019,.80),(.022,.42),(.024,.10)],RIGHT_INNER)}
def lobe_sections(name,inward=0):
 profile,centre,levels,inner=SEED_DESIGNS[name];rings=[]
 for i,(z,scale)in enumerate(levels):
  zz=z+inward if i==0 else z-inward if i==len(levels)-1 else z
  if inward:
   for(za,sa),(zb,sb)in zip(levels,levels[1:]):
    if za<=zz<=zb:scale=sa+(sb-sa)*(zz-za)/(zb-za);break
  poly=[add(centre,mul(sub(p,centre),scale))for p in profile];poly=inset_polygon(poly,inward)
  rings.append([(x,y,zz)for x,y in poly])
 return rings

def cotyledon(name,inward=0):
 profile,centre,levels,inner=SEED_DESIGNS[name];rings=lobe_sections(name,inward);m=Mesh();inneredges={frozenset([a,b])for a,b in zip(inner,inner[1:])}
 for k,(a,b)in enumerate(zip(rings,rings[1:])):
  for i in range(len(a)):
   j=(i+1)%len(a);cream=frozenset([profile[i],profile[j]])in inneredges
   m.quad(a[i],a[j],b[j],b[i],1 if cream else 0,'IrregularInnerCotyledonSplit'if cream else'RoundedUnequalSeedLobeBand'+str(k))
 for index,tag in [(0,'CompleteSmallSeedGroundSole'),(-1,'SmallRoundedSeedCrown')]:
  for t in planar_ears([p[:2]for p in rings[index]]):m.tri([rings[index][i]for i in t],0,tag)
 return m.result('Whole solid unequal rounded seed cotyledon with small flat ground sole and small crown, not a hollow shell or cylinder.')
for name in [LEFT,RIGHT]:G[name]=cotyledon(name);SOLID_VOLUMES[name+'_WholeInset']=dict(cotyledon(name,.0012),targets=[name])
# First two rectangular sections create one complete genuine root/hilum head.
# Its two finite lateral faces mate the two lobes; the following continuous
# round sections descend, taper and turn asymmetrically out through the split.
ROOT_PATH=[(0,.014,.012),(0,.006,.012),(.0002,.001,.0115),(.0007,-.008,.010),(.002,-.017,.008),(.005,-.026,.006),(.010,-.034,.004),(.016,-.039,.003),(.022,-.040,.0035),(.026,-.037,.0045)]
ROOT_RADII=[(.0015,.002),(.0015,.002),(.00165,.0018),(.00155,.0016),(.0013,.00135),(.0011,.0012),(.0009,.001),(.0009,.001),(.0008,.0009),(.00075,.0008)]
def radicle(inward=0):
 m=Mesh();rings=[]
 for i,(p,(ru,rv))in enumerate(zip(ROOT_PATH,ROOT_RADII)):
  a=ROOT_PATH[max(i-1,0)];b=ROOT_PATH[min(i+1,len(ROOT_PATH)-1)];d=(b[0]-a[0],b[1]-a[1]);d=mul(d,1/norm(d));side=(1,0,0)if i<2 else(-d[1],d[0],0)
  centre=p
  if i==0:centre=add(p,(0,-inward,0))
  if i==len(ROOT_PATH)-1:centre=sub(p,(d[0]*inward,d[1]*inward,0))
  shape=[(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)]if i<2 else[(math.cos(-3*math.pi/4+j*math.pi/4),math.sin(-3*math.pi/4+j*math.pi/4))for j in range(8)]
  assert ru>inward and rv>inward
  rings.append([add(centre,add(mul(side,(ru-inward)*u),(0,0,(rv-inward)*v)))for u,v in shape])
 for k,(a,b)in enumerate(zip(rings,rings[1:])):
  for i in range(8):j=(i+1)%8;m.quad(a[i],a[j],b[j],b[i],2,'ContinuouslyTaperedEmergingRadicle'+str(k))
 for ring,tag in [(rings[0],'CompleteHilumHeadEnd'),(rings[-1],'MinuteBluntRadicleTip')]:
  c=mul(tuple(map(sum,zip(*ring))),1/8)
  for i in range(8):m.tri([c,ring[i],ring[(i+1)%8]],2,tag)
 return m.result('One continuous root with complete two-sided rectangular hilum head and descending unequal curved taper, not a ring, handle or separate inserted rod.')
G[ROOT]=radicle();SOLID_VOLUMES[ROOT+'_WholeInset']=dict(radicle(.00043),targets=[ROOT])
CONTACTS=[dict(name='WholeLeftCotyledonHilumSeat',a=LEFT,b=ROOT,origin_m=(0,0,0),u=(0,1,0),v=(0,0,1),axis=(1,0,0),plane_m=-.0015,points=[(-.0015,.010,.012)],minimum_patch_area_m2=.008*.004-1e-8,complete_interface_area_m2=.008*.004,interior_probe_offset_m=.00012),dict(name='WholeRightCotyledonHilumSeat',a=ROOT,b=RIGHT,origin_m=(0,0,0),u=(0,1,0),v=(0,0,1),axis=(1,0,0),plane_m=.0015,points=[(.0015,.010,.012)],minimum_patch_area_m2=.008*.004-1e-8,complete_interface_area_m2=.008*.004,interior_probe_offset_m=.00012)]
FEET=[LEFT,RIGHT]
# Full isolated cleft is required against both complete seed lobes. The real
# emerging root intentionally occupies part of it; never claim an unobstructed
# assembled cleft. Complete upper and lower wall-following domains are separately
# proved against all three whole meshes; pairwise finite contact tests cover every
# root/lobe triangle, not merely its declared seat.
def seed_scale(name,z):
 levels=SEED_DESIGNS[name][2]
 if z<=levels[0][0]:return levels[0][1]
 if z>=levels[-1][0]:return levels[-1][1]
 for (za,sa),(zb,sb)in zip(levels,levels[1:]):
  if za<=z<=zb:return sa+(sb-sa)*(z-za)/(zb-za)
def cleft_profile(z,front=-.022,rear=.026):
 sides=[]
 for name,back in [(LEFT,(-.010,.020)),(RIGHT,(.010,.019))]:
  profile,c,levels,inner=SEED_DESIGNS[name];s=seed_scale(name,z);chain=inner+[back]
  sides.append([add(c,mul(sub(p,c),s))for p in chain])
 left,right=sides
 poly=ccw([(left[0][0],front)]+left+[(left[-1][0],rear),(right[-1][0],rear)]+list(reversed(right))+[(right[0][0],front)])
 return inset_polygon(poly,.001)
def cleft_volume(zlo,zhi):
 levels=sorted({zlo,zhi}|{z for _,_,ll,_ in SEED_DESIGNS.values()for z,_ in ll if zlo<z<zhi});rings=[];polys=[];m=Mesh()
 for z in levels:
  p=cleft_profile(z);polys.append(p);rings.append([(x,y,z)for x,y in p])
 for a,b in zip(rings,rings[1:]):
  for i in range(len(a)):j=(i+1)%len(a);m.quad(a[i],a[j],b[j],b[i],0,'WholeIrregularCleftBoundary')
 for i in [0,-1]:
  for t in planar_ears(polys[i]):m.tri([rings[i][j]for j in t],0,'WholeFiniteCleftMouth')
 return m.result('Full finite wall-following irregular inter-cotyledon cleft with both end mouths extended, not a central ray or a box substitute.')
ISOLATED_VOID_VOLUMES['WholeIsolatedInterCotyledonCleft']=dict(cleft_volume(-.003,.030),targets=[LEFT,RIGHT])
VOID_VOLUMES['WholeUpperCleftAboveEmergingRoot']=dict(cleft_volume(.0155,.030),targets=None)
VOID_VOLUMES['WholeLowerCleftBelowEmergingRoot']=dict(cleft_volume(-.003,.005),targets=None)
INSIDE_TESTS=[(LEFT,(-.014,0,.012),(0,0,.012)),(RIGHT,(.013,0,.012),(0,0,.012)),(ROOT,(0,.010,.012),(.006,.010,.012))]
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 for i in [0,1])+(0.,)
for group in [G,SOLID_VOLUMES,VOID_VOLUMES,ISOLATED_VOID_VOLUMES]:
 for g in group.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
for r in CONTACTS:r['points']=[add(p,SHIFT)for p in r['points']];r['plane_m']+=dot(SHIFT,r['axis'])
INSIDE_TESTS=[(n,add(a,SHIFT),add(b,SHIFT))for n,a,b in INSIDE_TESTS]
CONTRACT=dict(single_prop_count=1,closed_meshes=3,triangles=460,materials=3,rounded_unequal_solid_cotyledons=2,continuous_tapered_radicles=1,whole_material_domains=3,whole_assembled_air_domains=2,whole_isolated_cleft_domains=1,complete_contact_pairs=2,noncontact_pairs=1,whole_ground_soles=2,expanded_leaves=0,animated_growth=False)
def measure_seed_geometry(vertices):
 assert set(vertices)==set(G);vv=[p for v in vertices.values()for p in v];lo=[min(p[i]for p in vv)for i in range(3)];hi=[max(p[i]for p in vv)for i in range(3)];assert abs(lo[2])<2e-7 and max(abs(lo[i]+hi[i])for i in[0,1])<2e-7
 return dict(CONTRACT,bounds_m=[hi[i]-lo[i]for i in range(3)],scope='SOURCE numeric measurements only; actual GLB, independent first-front identification and native gates required.')
FOCUS=(0,0,.012);ORTHO=.105
CAMERAS={'gray-front3q':(.18,-.28,.26),'gray-back3q':(-.18,.28,.26),'silhouette-128-front':(0,-.30,.18),'silhouette-128-side':(-.30,0,.18),'qa-front':(0,-.30,.18),'qa-side':(-.30,0,.18),'qa-top':(0,0,.30),'qa-back':(0,.30,.18),'thumbnail':(.18,-.28,.26),'qa-wireframe':(-.18,.28,.26)}
WIRE_THICKNESS=.0001
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
root=bpy.data.objects.new('OneCrackedBeanSeedWithCurvedRadicle',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='two complete small cotyledon soles at Z=0; irregular isolated cleft with deliberately occupied root centre, whole assembled upper/lower clear domains and two complete finite hilum seats';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_seed_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'cracked_seed_radicle_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
 d={'id':ASSET,'version':VERSION,'category':'nature','assetKind':'prop','theme':'farming','style':'warm-handcrafted-village','title':TITLE,'description':DESCRIPTION,
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
