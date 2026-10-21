"""Original interlaced double-diamond Chinese-festival-inspired knot ornament.
Static low-poly game art in a laid-flat pose; no knot-tying, hanging or load claim.
"""
DESCRIPTION=('One original complete static Chinese-festival-inspired double-diamond knot ornament displayed laid flat. Two continuous thick chamfer-cornered red cord loops interlace in real three-dimensional space: the left loop passes above the upper crossing with a genuine finite air gap, then below the lower crossing on a complete finite bearing patch. Three complete assembled through windows remain open between the bands. A separate warm-gold-fronted upper loop has its own true hanging aperture and full butt joint; a continuous lower red tassel silhouette has three genuine open-ended deep clefts and a full finite root joint. Four editable closed connected meshes and three opaque constant untextured PBR tones. Metres, native Z up, decorative face +Z, presentation front -Y and horizontally bounds-centred ground origin. The entire lower-left cord back and complete tassel back meet ground Z=0. One prop and zero scenes. All numerical geometry newly authored; no mooring coil, rope barrier, cloth bolt, wreath, firecracker, lantern, stacking ring or other model is imported, recoloured, resized or combined. The two linked loops are components of this one ornament, never counted as separate models. No wall, stand, scene, writing, texture, logo, animation, other festival object or extra knot variant. Stylized fixed decorative game geometry only: no precise historical knot type, knot-tying instruction, cultural authenticity, fabric deformation, flexibility, real cord construction, mechanical link performance, suspension or wall-mount suitability, attachment strength, loading, physical balance, manufacture, installation or safety certification. Dimensions describe game-space geometry only.')
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
LINKS=[];GAPS=[];BORES=[];FOOT_CONTACTS=[]
VERSION='1.0.0';TITLE='Interlaced Double-Diamond Festival Knot'
G={};SOLID_VOLUMES={};VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};CONTACTS=[];FEET=[]
ASSET='festival-interlaced-double-diamond-knot-01'
PALETTE=[('Cord_Cinnabar',(.58,.035,.025,1),.74,0),('Cord_DeepCrimson',(.25,.012,.016,1),.79,0),('Tie_MatteGold',(.65,.36,.075,1),.68,0)]
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




def area2(p):return sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(p,p[1:]+p[:1]))/2
def ccw(p):return list(p) if area2(p)>0 else list(reversed(p))
def intersect_lines(p,u,q,v):
 cross2=lambda a,b:a[0]*b[1]-a[1]*b[0]
 t=cross2(sub(q,p),v)/cross2(u,v);return add(p,mul(u,t))
def offset(poly,amount):
 poly=ccw(poly);out=[]
 for i,b in enumerate(poly):
  a,c=poly[i-1],poly[(i+1)%len(poly)];u=sub(b,a);v=sub(c,b);nu=(-u[1]/norm(u),u[0]/norm(u));nv=(-v[1]/norm(v),v[0]/norm(v))
  out.append(intersect_lines(add(b,mul(nu,amount)),u,add(b,mul(nv,amount)),v))
 return out

def clip_half(poly,axis,value,sign):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  da=(a[axis]-value)*sign;db=(b[axis]-value)*sign
  if (da>=-1e-12)!=(db>=-1e-12):out.append(add(a,mul(sub(b,a),da/(da-db))))
  if db>=-1e-12:out.append(b)
 clean=[]
 for p in out:
  if not clean or norm(sub(clean[-1],p))>1e-10:clean.append(p)
 if len(clean)>1 and norm(sub(clean[0],clean[-1]))<1e-10:clean.pop()
 return clean

def ring_mesh(outer,inner,height,thickness,inset=0):
 outer=offset(outer,inset);inner=offset(inner,-inset);m=Mesh();levels=[-10,-.04,.04,10]
 def point(p,upper):return (p[0],p[1],height(p[1])+inset+(thickness-2*inset if upper else 0))
 for i in range(len(outer)):
  j=(i+1)%len(outer);quad=[outer[i],outer[j],inner[j],inner[i]]
  for y0,y1 in zip(levels,levels[1:]):
   poly=clip_half(clip_half(quad,1,y0,1),1,y1,-1)
   if len(poly)<3 or abs(area2(poly))<1e-12:continue
   center=tuple(sum(p[k] for p in poly)/len(poly) for k in range(2))
   for upper in [False,True]:
    for a,b in zip(poly,poly[1:]+poly[:1]):m.tri([point(center,upper),point(a,upper),point(b,upper)],0 if upper else 1,'WholeCordTop' if upper else 'WholeCordBack')
  for loop,tag in [(outer,'WholeOuterCordWall'),(inner,'WholeInnerApertureWall')]:
   a,b=loop[i],loop[j];ts=[0,1]
   if abs(b[1]-a[1])>1e-12:ts += [(y-a[1])/(b[1]-a[1]) for y in[-.04,.04] if 1e-9<(y-a[1])/(b[1]-a[1])<1-1e-9]
   path=[add(a,mul(sub(b,a),t)) for t in sorted(ts)]
   for a,b in zip(path,path[1:]):m.quad(point(a,False),point(b,False),point(b,True),point(a,True),1,tag)
 return m.result('One continuous thick closed cord annulus, with genuine aperture and fully joined rising or falling band segments.')

def earclip(poly):
 poly=ccw(poly);order=list(range(len(poly)));tris=[]
 def cross2(a,b):return a[0]*b[1]-a[1]*b[0]
 while len(order)>3:
  for k,b in enumerate(order):
   a=order[k-1];c=order[(k+1)%len(order)];A,B,C=poly[a],poly[b],poly[c]
   if cross2(sub(B,A),sub(C,B))<1e-12:continue
   def inside(p):return min(cross2(sub(B,A),sub(p,A)),cross2(sub(C,B),sub(p,B)),cross2(sub(A,C),sub(p,C)))>=-1e-12
   if any(inside(poly[q]) for q in order if q not in[a,b,c]):continue
   tris.append((a,b,c));order.pop(k);break
  else:raise AssertionError('earclip could not find a positive ear')
 tris.append(tuple(order));return poly,tris

def prism(poly,z0,z1,inset=0,mat=0):
 poly,tri=earclip(offset(poly,inset));m=Mesh();z0+=inset;z1-=inset
 for f in tri:
  for z in[z0,z1]:m.tri([(poly[i][0],poly[i][1],z) for i in f],mat if z==z1 else 1,'CompleteFrontOrBack')
 for a,b in zip(poly,poly[1:]+poly[:1]):m.quad((a[0],a[1],z0),(b[0],b[1],z0),(b[0],b[1],z1),(a[0],a[1],z1),1,'WholeExteriorWall')
 return m.result('One thick closed editable decorative silhouette with all finite front, back and edge surfaces.')

BASE=ccw([(-.02,.22),(.02,.22),(.18,.025),(.18,-.025),(.02,-.22),(-.02,-.22),(-.18,-.025),(-.18,.025)])
LEFT_OUT=[(x-.095,y) for x,y in BASE];RIGHT_OUT=[(x+.095,y) for x,y in BASE]
LEFT_IN=[(x*.78-.095,y*.78) for x,y in BASE];RIGHT_IN=[(x*.78+.095,y*.78) for x,y in BASE]
LEFT='ContinuousOverUnderLeftDiamondCord';RIGHT='ContinuousFlatRightDiamondCord';HANGER='CompleteThroughOpeningUpperHangingLoop';TASSEL='ContinuousNotchedLowerTassel'
def bent_height(y):return .045*max(0,min(1,(y+.04)/.08))
G[LEFT]=ring_mesh(LEFT_OUT,LEFT_IN,bent_height,.020)
G[RIGHT]=ring_mesh(RIGHT_OUT,RIGHT_IN,lambda y:.020,.020)
SOLID_VOLUMES[LEFT+'_WholeInset']=dict(ring_mesh(LEFT_OUT,LEFT_IN,bent_height,.020,.001),targets=[LEFT])
SOLID_VOLUMES[RIGHT+'_WholeInset']=dict(ring_mesh(RIGHT_OUT,RIGHT_IN,lambda y:.020,.020,.001),targets=[RIGHT])
# Top loop is an independent narrow open octagon joined by a complete bottom face.
HANG_OUT=ccw([(.075,.22),(.115,.22),(.145,.25),(.145,.34),(.115,.37),(.075,.37),(.045,.34),(.045,.25)])
HANG_IN=offset(HANG_OUT,.012)
G[HANGER]=ring_mesh(HANG_OUT,HANG_IN,lambda y:.020,.020)
SOLID_VOLUMES[HANGER+'_WholeInset']=dict(ring_mesh(HANG_OUT,HANG_IN,lambda y:.020,.020,.001),targets=[HANGER])
# Newly drawn full connected fan/tassel silhouette; three true open-bottom clefts.
TASSEL_POLY=ccw([(-.115,-.22),(-.075,-.22),(-.075,-.27),(-.035,-.32),(-.025,-.45),(-.058,-.43),(-.062,-.35),(-.071,-.445),(-.087,-.445),(-.095,-.35),(-.103,-.445),(-.119,-.445),(-.128,-.35),(-.132,-.43),(-.165,-.45),(-.155,-.32),(-.115,-.27)])
G[TASSEL]=prism(TASSEL_POLY,0,.020)
SOLID_VOLUMES[TASSEL+'_WholeInset']=dict(prism(TASSEL_POLY,0,.020,.001),targets=[TASSEL])
FEET=[LEFT,TASSEL]
# Three finite contacts; right loop rests on left lower crossing, while upper crossing keeps a genuine 5 mm air gap.
CONTACTS=[{'name':'LowerDiamondCrossingSeat','a':LEFT,'b':RIGHT,'axis':(0,0,1),'plane_m':.020}, {'name':'WholeUpperLoopBottomEnd','a':RIGHT,'b':HANGER,'axis':(0,1,0),'plane_m':.22}, {'name':'WholeLowerTasselRootEnd','a':TASSEL,'b':LEFT,'axis':(0,1,0),'plane_m':-.22}]

# Warm gold belongs only to the complete upper-loop front surface.
G[HANGER]['face_materials']=[2 if tag=='WholeCordTop' else mat for mat,tag in zip(G[HANGER]['face_materials'],G[HANGER]['face_tags'])]

def point_inside(poly,p):
 return all((b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])>=-1e-10 for a,b in zip(poly,poly[1:]+poly[:1]))
def clip_convex(subject,clip):
 poly=list(subject)
 for a,b in zip(clip,clip[1:]+clip[:1]):
  out=[]
  def side(p):return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
  for p,q in zip(poly,poly[1:]+poly[:1]):
   dp,dq=side(p),side(q)
   if (dp>=-1e-12)!=(dq>=-1e-12):out.append(add(p,mul(sub(q,p),dp/(dp-dq))))
   if dq>=-1e-12:out.append(q)
  poly=out
  if not poly:break
 return poly

def convex_difference(A,B):
 """Boundary assembly for this connected convex-minus-convex notch; no buried partition faces."""
 A,B=ccw(A),ccw(B);edges=[]
 def cross2(u,v):return u[0]*v[1]-u[1]*v[0]
 def split(poly,other,reverse):
  for a,b in zip(poly,poly[1:]+poly[:1]):
   u=sub(b,a);ts=[0,1]
   for c,d in zip(other,other[1:]+other[:1]):
    v=sub(d,c);den=cross2(u,v)
    if abs(den)<1e-12:continue
    t=cross2(sub(c,a),v)/den;q=cross2(sub(c,a),u)/den
    if -1e-9<=t<=1+1e-9 and -1e-9<=q<=1+1e-9:ts.append(max(0,min(1,t)))
   ts=sorted(set(round(t,12) for t in ts))
   for t0,t1 in zip(ts,ts[1:]):
    p=add(a,mul(u,t0));q=add(a,mul(u,t1));mid=mul(add(p,q),.5)
    if point_inside(other,mid)==reverse:
     p=tuple(round(x,9) for x in p);q=tuple(round(x,9) for x in q)
     if p!=q:edges.append((q,p) if reverse else (p,q))
 split(A,B,False);split(B,A,True);graph={}
 for p,q in edges:assert p not in graph,('branched difference',p);graph[p]=q
 start=min(graph);poly=[start];current=graph[start]
 while current!=start:assert current not in poly;poly.append(current);current=graph[current]
 assert len(poly)==len(edges),'difference has disconnected components';return ccw(poly)

# Whole assembled apertures, every outer/inner boundary, and both full-depth mouths.
WINDOW_LEFT=convex_difference(offset(LEFT_IN,.001),offset(RIGHT_OUT,-.001))
WINDOW_CENTRE=clip_convex(offset(LEFT_IN,.001),offset(RIGHT_IN,.001))
WINDOW_RIGHT=convex_difference(offset(RIGHT_IN,.001),offset(LEFT_OUT,-.001))
for name,poly in [('EntireLeftLobedOpening',WINDOW_LEFT),('EntireCentralOverlapOpening',WINDOW_CENTRE),('EntireRightLobedOpening',WINDOW_RIGHT),('EntireUpperHangingLoopOpening',offset(HANG_IN,.001))]:
 VOID_VOLUMES[name]=dict(prism(poly,-.020,.090),targets=None)
# Full isolated annular holes are checked additionally, without pretending the
# other ring is absent in the complete assembled aperture tests above.
for name,poly,target in [('EntireIsolatedLeftDiamondHole',LEFT_IN,LEFT),('EntireIsolatedRightDiamondHole',RIGHT_IN,RIGHT)]:
 ISOLATED_VOID_VOLUMES[name]=dict(prism(offset(poly,.001),-.020,.090),targets=[target])
# Analytic band intersections: complete finite lower seat and upper crossing air.
# Derive exact band overlap from all original annular quadrilaterals rather than
# estimate by a ray or one overlap witness. In this symmetric construction each
# upper/lower crossing is one convex polygon after adjacent collinear vertices.
def band_crossings():
 out=[]
 for i in range(8):
  j=(i+1)%8;A=ccw([LEFT_OUT[i],LEFT_OUT[j],LEFT_IN[j],LEFT_IN[i]])
  for k in range(8):
   l=(k+1)%8;B=ccw([RIGHT_OUT[k],RIGHT_OUT[l],RIGHT_IN[l],RIGHT_IN[k]])
   p=clip_convex(A,B)
   if len(p)>=3 and abs(area2(p))>1e-10:out.append(p)
 assert len(out)==2,('expected two full crossings',out)
 return sorted(out,key=lambda p:sum(y for x,y in p)/len(p))
LOWER_CROSS,UPPER_CROSS=band_crossings()
VOID_VOLUMES['EntireUpperWeaveCrossingAir']=dict(prism(offset(UPPER_CROSS,.001),.041,.044),targets=None)
for i,(x,dx_left,dy_left,dx_right,dy_right) in enumerate([(-.062,-.009,-.095,.004,-.080),(-.095,-.008,-.095,.008,-.095),(-.128,-.004,-.080,.009,-.095)]):
 y=-.470;left=(x+(y+.35)*dx_left/dy_left,y);right=(x+(y+.35)*dx_right/dy_right,y)
 poly=offset(ccw([(x,-.35),left,right]),.001)
 VOID_VOLUMES['EntireTasselCleft%02dAndOpenMouth'%(i+1)]=dict(prism(poly,-.020,.090),targets=None)
for r in CONTACTS:
 area=abs(area2(LOWER_CROSS)) if r['name']=='LowerDiamondCrossingSeat' else .04*.020
 p=(sum(x for x,y in LOWER_CROSS)/len(LOWER_CROSS),sum(y for x,y in LOWER_CROSS)/len(LOWER_CROSS),.020) if r['name']=='LowerDiamondCrossingSeat' else ((.095,.22,.030) if r['name']=='WholeUpperLoopBottomEnd' else(-.095,-.22,.010))
 r.update(origin_m=(0,0,0),u=(1,0,0),v=(0,1,0) if r['axis']==(0,0,1) else(0,0,-1),points=[p],minimum_patch_area_m2=area-2e-7,complete_interface_area_m2=area,interior_probe_offset_m=.0004)

INSIDE_TESTS=[(LEFT,(-.095,.20,.055),(-.095,0,.03)),(RIGHT,(.25,0,.030),(.095,0,.03)),(HANGER,(.095,.364,.030),(.095,.30,.030)),(TASSEL,(-.095,-.25,.010),(-.095,-.39,.010))]
for name,p in [('LeftOpening',(-.17,0,-.02)),('CentralOpening',(0,0,-.02)),('RightOpening',(.17,0,-.02)),('HangingLoopOpening',(.095,.30,-.02))]:GAPS.append({'name':name,'origin_m':p,'direction':(0,0,1),'length_m':.11})
YSHIFT=.040
for group in [G,SOLID_VOLUMES,VOID_VOLUMES,ISOLATED_VOID_VOLUMES]:
 for shape in group.values():shape['vertices']=[(x,round(y+YSHIFT,9),z) for x,y,z in shape['vertices']]
for r in CONTACTS:
 r['plane_m']+=r['axis'][1]*YSHIFT;r['points']=[(x,y+YSHIFT,z) for x,y,z in r['points']]
for r in GAPS:
 x,y,z=r['origin_m'];r['origin_m']=(x,y+YSHIFT,z)
INSIDE_TESTS=[(n,(a[0],a[1]+YSHIFT,a[2]),(b[0],b[1]+YSHIFT,b[2])) for n,a,b in INSIDE_TESTS]
CONTRACT={'single_prop_count':1,'new_scene_count':0,'kind':'prop','original_numeric_whole':True,'native_axis_up':'Z','front_direction':'-Y','decorative_face':'+Z','origin':'horizontal bounds-centred grounded laid-flat pose','closed_meshes':4,'materials':3,'interlaced_continuous_diamond_cords':2,'assembled_diamond_windows':3,'true_hanging_loop_apertures':1,'open_ended_tassel_clefts':3,'whole_material_domains':4,'assembled_air_domains':8,'isolated_air_domains':2,'finite_opposed_contacts':3,'whole_ground_meshes':2,'old_geometry_imports':0,'fixed_visual_only':True}
def measure_knot_geometry(vertices):
 assert set(vertices)==set(G);vv=[p for vs in vertices.values() for p in vs];assert abs(min(p[2] for p in vv))<2e-7
 return dict(CONTRACT,bounds_m=[max(p[i] for p in vv)-min(p[i] for p in vv) for i in range(3)],upper_crossing_air_height_m=.005,cord_thickness_m=.020,complete_lower_crossing_area_m2=abs(area2(LOWER_CROSS)),scope='Producer geometry only; separately decoded actual GLB complete predicates govern acceptance')
FOCUS=(0,0,.025);ORTHO=1.05
CAMERAS={'gray-front3q':(1.4,-2,3),'gray-back3q':(-1.4,2,3),'thumbnail':(-1.3,-2,3.8),'qa-front':(0,-3,2.5),'qa-side':(-3,0,2.5),'qa-top':(0,0,4),'qa-back':(0,3,2.5),'qa-wireframe':(-1.3,-2,3.8),'silhouette-128-front':(0,-3,2.5),'silhouette-128-side':(-3,0,2.5)}
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
root=bpy.data.objects.new('OneInterlacedDoubleDiamondKnot',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='entire lower cord back and complete tassel back at Z=0; linked upper/lower crossings and full through apertures';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_knot_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'interlaced_knot_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
