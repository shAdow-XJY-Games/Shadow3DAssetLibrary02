"""Original static cross-pole domed camping tent; game-art geometry only.
One compound-curved rounded-four-corner enclosure with full 12 mm faceted
wall/roof, integral 24 mm floor, real chamfer-curved entrance and 105 mm sill.
Two entire continuous bent diagonal rectangular-section poles meet in a finite
raised crown seat. The lower pole directly follows the fabric; the upper pole
has two full lower shell seats and a true crown-over-pole seat, never passes
through its partner. All three are complete editable closed material meshes.
No folding, pitching, fabric simulation, weatherproofing, occupancy, human fit,
load, manufacture, installation, fire, camping performance or safety claim.
All coordinates newly authored. No A-frame/tunnel/observatory/parasol geometry
is imported, rescaled, recoloured, extracted or reassembled into this asset.
"""
import math,json,hashlib,sys,time,itertools
from pathlib import Path
import numpy as np
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='camping-cross-pole-domed-tent-01';VERSION='1.0.0';TITLE='Cross-Pole Domed Camping Tent'
DESCRIPTION=('One original static low-poly domed camping tent appearance with a newly authored rounded-four-corner double-curved enclosure, integral thick floor and raised threshold, genuinely open chamfer-curved front entry, closed back and sides. Two whole continuous faceted diagonal pole paths meet at one finite opposed raised crown seat rather than crossing through each other. The lower pole seats along the complete convex fabric profile; the upper pole seats on both lower corners and on the lower pole at the crown. Three closed editable meshes, four constant opaque untextured PBR materials. Metres, native Z up, front -Y, horizontal bounds centred, entire floor underside at Z=0. One prop and zero scenes; not a family-completion claim or an old A-frame, play tunnel, climbing dome, parasol or observatory conversion. Empty fixed game-art appearance only: no flap operation, deployment, fabric simulation, moving mechanism, occupancy, human fit, practical entry, weatherproofing, thermal/fire behaviour, pitching, manufacture, installation, load, stability or camping safety/performance claim. No people, sleeping equipment, guy ropes, stakes, signs, lettering, brand, texture or animation.')
BODY='WholeCompoundEnclosureAndFloor';POLE_A='WholeFirstDiagonalBentPole';POLE_B='WholeRaisedCrownDiagonalBentPole'
PALETTE=[('Canvas_QuietOchre',(.52,.31,.095,1),.85,0.),('InnerCanvas_WarmLinen',(.63,.57,.42,1),.88,0.),('BathtubFloor_DeepTeal',(.035,.115,.12,1),.84,0.),('Poles_Graphite',(.055,.065,.072,1),.45,.30)]
G={};SOLID_VOLUMES={};VOID_VOLUMES={};AIR_CELLS={};CONTACTS=[];LINKS=[];GAPS=[];BORES=[];FEET=[BODY];INSIDE_TESTS=[]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
BASE=[(-1.,-.91),(-.77,-1.17),(.77,-1.17),(1.,-.91),(1.,.91),(.77,1.17),(-.77,1.17),(-1.,.91)]
LEVELS=[(0.,1.),(.10,1.),(.65,.86),(1.08,.48),(1.24,.15)]
def norm(x):return np.linalg.norm(x)

def normalized(x):return x/norm(x)

def clean(p):
 out=[]
 for q in p:
  if not out or norm(q-out[-1])>1e-9:out.append(q)
 if len(out)>1 and norm(out[0]-out[-1])<1e-9:out.pop()
 return out

def clip(p,n,d,inside=True):
 if not p:return []
 q=[]
 for a,b in zip(p,p[1:]+p[:1]):
  da=float(a@n-d);db=float(b@n-d)
  if not inside:da=-da;db=-db
  ia=da<=1e-10;ib=db<=1e-10
  if ia:q.append(a)
  if ia!=ib:q.append(a+(b-a)*(da/(da-db)))
 return clean(q)

def intersect_polygon(p,planes):
 for n,d in planes:p=clip(p,n,d)
 return p

def subtract_polygon(p,planes):
 out=[]
 for n,d in planes:
  outside=clip(p,n,d,False)
  if len(outside)>=3:out.append(outside)
  p=clip(p,n,d)
  if len(p)<3:break
 return out

def plane_from_face(p,interior):
 n=normalized(np.cross(p[1]-p[0],p[2]-p[0]));d=float(n@p[0])
 if float(n@interior)>d:n=-n;d=-d;p=list(reversed(p))
 return p,(n,d)

def outer_planes():
 rings=[[np.array([x*s,y*s,z])for x,y in BASE]for z,s in LEVELS];faces=[]
 for a,b in zip(rings,rings[1:]):
  for i in range(8):j=(i+1)%8;faces.append([a[i],a[j],b[j],b[i]])
 faces.extend([rings[0],rings[-1]])
 return [plane_from_face(p,np.array([0,0,.5]))[1]for p in faces]

def polyhedron(planes):
 # This feasibility stage is small:34face hull. Enumerate3plane vertices only.
 vertices=[]
 for a,b,c in itertools.combinations(planes,3):
  N=np.array([a[0],b[0],c[0]])
  if abs(np.linalg.det(N))<1e-10:continue
  v=np.linalg.solve(N,np.array([a[1],b[1],c[1]]))
  if all(float(v@n)<=d+2e-9 for n,d in planes)and not any(norm(v-w)<1e-8 for w in vertices):vertices.append(v)
 faces=[]
 for n,d in planes:
  vs=[v for v in vertices if abs(float(v@n)-d)<1e-8]
  if len(vs)<3:continue
  centre=sum(vs)/len(vs);u=normalized(vs[0]-centre);v=np.cross(n,u)
  vs.sort(key=lambda p:math.atan2(float((p-centre)@v),float((p-centre)@u)))
  faces.append(vs)
 return faces

def door_planes():
 # Full-height finite curved/chamfered front entrance, not a dark applied polygon.
 profile=[(-.40,.105),(.40,.105),(.40,.64),(.32,.82),(.14,.965),(-.14,.965),(-.32,.82),(-.40,.64)]
 rings=[[np.array([x,y,z])for x,z in profile]for y in [-1.38,.05]];faces=[rings[0],rings[1]]
 for i in range(8):j=(i+1)%8;faces.append([rings[0][i],rings[0][j],rings[1][j],rings[1][i]])
 return [plane_from_face(p,np.array([0,-.6,.5]))[1]for p in faces]

def triangulate(faces):
 # All boundary polygons are convex; insert EVERY boundary vertex on an edge
 # before fan tessellation so independently clipped surfaces have no T junction.
 vv=[]
 def vertex(v):
  for i,w in enumerate(vv):
   if norm(v-w)<1e-8:return i
  vv.append(v);return len(vv)-1
 for poly,_ in faces:
  for v in poly:vertex(v)
 allv=list(vv);ff=[];tags=[]
 for poly,tag in faces:
  ring=[]
  for a,b in zip(poly,poly[1:]+poly[:1]):
   ab=b-a;length=float(ab@ab);edge=[]
   for v in allv:
    t=float((v-a)@ab)/length
    if -1e-9<=t<1-1e-9 and norm(v-(a+t*ab))<1e-8:edge.append((max(0,t),v))
   ring.extend(v for _,v in sorted(edge,key=lambda x:x[0]))
  centre=sum(ring)/len(ring);ci=vertex(centre)
  for a,b in zip(ring,ring[1:]+ring[:1]):
   f=(ci,vertex(a),vertex(b))
   if norm(np.cross(vv[f[1]]-vv[f[0]],vv[f[2]]-vv[f[0]]))>1e-12:ff.append(f);tags.append(tag)
 return np.array(vv),ff,tags

def topology(v,f):
 edges={}
 for i,t in enumerate(f):
  for a,b in zip(t,t[1:]+t[:1]):edges.setdefault(tuple(sorted([a,b])),[]).append((i,a,b))
 bad=[(e,x)for e,x in edges.items()if len(x)!=2 or x[0][1:]!=x[1][1:][::-1]]
 volume=sum(np.dot(v[a],np.cross(v[b],v[c]))for a,b,c in f)/6
 return dict(vertices=len(v),triangles=len(f),edges=len(edges),euler=len(v)-len(edges)+len(f),volume_m3=float(volume),bad_edges=len(bad),bad_examples=bad[:5])
def shifted(planes,d):return[(n,x+d)for n,x in planes]

def strip(direction,width=.018,z0=.10):
 u=normalized(np.array([*direction,0.]));v=np.array([-u[1],u[0],0.])
 return[(v,width),(-v,width),(np.array([0.,0.,-1.]),-z0)]
def inside_planes(p,planes,tolerance=0.):return all(float(p@n)<d+tolerance for n,d in planes)

def region_inside(p,outer,cuts):return inside_planes(p,outer)and not any(inside_planes(p,c)for c in cuts)

def finite_difference(p,cut):
 # A zero-area intersection has no finite polygon to subtract. This also avoids
 # artificial subdivisions when a face is wholly beyond one convex cut plane.
 overlap=intersect_polygon(p,cut)
 if len(overlap)<3 or norm(sum(np.cross(a,b)for a,b in zip(overlap,overlap[1:]+overlap[:1])))<1e-12:return[p]
 pieces=[]
 for n,d in cut:
  vals=[float(v@n-d)for v in p]
  outside=[] if max(abs(v)for v in vals)<1e-9 else clip(p,n,d,False)
  if len(outside)>=3:pieces.append(outside)
  p=clip(p,n,d)
  if len(p)<3:break
 return pieces
def difference_faces(outer,cuts):
 faces=[]
 for poly in polyhedron(outer):
  pieces=[poly]
  for cut in cuts:pieces=[q for p in pieces for q in finite_difference(p,cut)]
  faces.extend((p,'outer')for p in pieces)
 for i,cut in enumerate(cuts):
  for poly in polyhedron(cut):
   p=intersect_polygon(poly,outer)
   if len(p)<3:continue
   pieces=[p]
   for j,other in enumerate(cuts):
    if i!=j:pieces=[q for p in pieces for q in finite_difference(p,other)]
   faces.extend((list(reversed(p)),'cut_%d'%i)for p in pieces)
 keep=[]
 for p,tag in faces:
  n=sum(np.cross(a,b)for a,b in zip(p,p[1:]+p[:1]));area2=norm(n)
  if area2<1e-12:continue
  n=n/area2;centre=sum(p)/len(p)
  if region_inside(centre-n*1e-7,outer,cuts)and not region_inside(centre+n*1e-7,outer,cuts):keep.append((p,tag))
 return keep

def difference(outer,cuts):return triangulate(difference_faces(outer,cuts))
def clipped_solid(faces,n,d):
 values=[float(p@n-d)for f in faces for p in f]
 if not values or min(values)>1e-9:return []
 if max(values)<1e-9:return faces
 out=[];rim=[]
 for poly in faces:
  p=clip(poly,n,d)
  if len(p)>=3 and norm(sum(np.cross(a,b)for a,b in zip(p,p[1:]+p[:1])))>1e-12:out.append(p)
  for v in p:
   if abs(float(v@n-d))<1e-8 and not any(norm(v-w)<1e-8 for w in rim):rim.append(v)
 if len(rim)>=3:
  c=sum(rim)/len(rim);u=normalized(rim[0]-c);v=np.cross(n,u)
  rim.sort(key=lambda p:math.atan2(float((p-c)@v),float((p-c)@u)))
  out.append(rim)
 return out

def signed_volume(faces):
 return sum(float(np.dot(p[0],np.cross(p[i],p[i+1])))for p in faces for i in range(1,len(p)-1))/6

def partition(outer,cuts):
 cells=[(polyhedron(outer),list(outer),[])]
 for cut_index,cut in enumerate(cuts):
  next_cells=[]
  for faces,planes,path in cells:
   current=faces;current_planes=list(planes)
   for plane_index,(n,d)in enumerate(cut):
    if not current:break
    vals=[float(v@n-d)for p in current for v in p]
    if max(vals)<1e-9:current_planes.append((n,d));continue
    if min(vals)>-1e-9:
     next_cells.append((current,current_planes+[(-n,-d)],path+[(cut_index,plane_index)]));current=[];break
    outside=clipped_solid(current,-n,-d)
    if outside and signed_volume(outside)>1e-12:next_cells.append((outside,current_planes+[(-n,-d)],path+[(cut_index,plane_index)]))
    current=clipped_solid(current,n,d);current_planes.append((n,d))
  cells=next_cells
 return cells

# Every complete material and finite air body below is derived from these
# explicit original halfspaces, not from a sampled bounding box or centre ray.
O=outer_planes();I=[(n,d-(.024 if n[2]<-.999 else .012))for n,d in O];D=door_planes()
S1=strip((.885,1.04));S2=strip((-.885,1.04));A=shifted(O,.036)+S1
H=[(n,d+(0. if i<16 or i==32 else .018 if i<24 else .036))for i,(n,d)in enumerate(O)]
B=shifted(H,.036)+S2
REGIONS={BODY:(O,[I,D]),POLE_A:(A,[O]),POLE_B:(B,[H])}
def material_mesh(outer,cuts,role,body=False):
 faces=difference_faces(outer,cuts);v,f,t=triangulate(faces);m=[]
 for ids,tag in zip(f,t):
  z=float(np.mean(v[list(ids),2]));m.append((2 if z<.106 else 0 if tag=='outer' else 1)if body else 3)
 return dict(vertices=v.tolist(),faces=f,face_materials=m,face_tags=t,material=0 if body else 3,role=role),faces
FACES={}
for name,(outer,cuts)in REGIONS.items():
 role='One complete compound-curved enclosing material shell, floor and true entry returns.'if name==BODY else 'One entire continuous bent diagonal pole; exact whole finite profile, cut ends and seats.'
 G[name],FACES[name]=material_mesh(outer,cuts,role,name==BODY)
 probe,_=material_mesh(shifted(outer,-.002),[shifted(c,.002)for c in cuts],'Entire material offset inward 2 mm from every physical planar boundary, including all returns and ends.',name==BODY)
 SOLID_VOLUMES[name+'_Whole2mmInset']=dict(probe,targets=[name])
 candidates=sorted(FACES[name],key=lambda r:-norm(sum(np.cross(a,b)for a,b in zip(r[0],r[0][1:]+r[0][:1]))))
 for p,tag in candidates:
  n=normalized(sum(np.cross(a,b)for a,b in zip(p,p[1:]+p[:1])));c=sum(p)/len(p)-n*.004
  if region_inside(c,outer,cuts):INSIDE_TESTS.append((name,c.tolist(),(4.,4.,4.)));break
 assert any(r[0]==name for r in INSIDE_TESTS)
def raw_probe(faces,role):
 v,f,t=triangulate([(p,'CompletePhysicalBoundary')for p in faces]);return dict(vertices=v.tolist(),faces=f,material=0,role=role)
def serialized_planes(planes):return[dict(normal=n.tolist(),offset_m=float(d))for n,d in planes]
for name,planes in [('EntireInnerTentAir',I),('EntireFrontEntranceAir',D)]:
 faces=polyhedron(planes);g=raw_probe(faces,'Whole nominal convex finite air domain up to all physical boundaries. Source/actual predicate uses 2e-7 numerical boundary band, not a central inset box.');VOID_VOLUMES[name]=dict(g,targets=None)
 AIR_CELLS[name]=[dict(g,planes=serialized_planes(planes),first_violated_halfspace_path=[])]
gap_faces=difference_faces(H+S2,[O,A]);gv,gf,gt=triangulate(gap_faces)
VOID_VOLUMES['EntireAirUnderRaisedPole']=dict(vertices=gv.tolist(),faces=gf,material=0,targets=None,role='Both complete connected peripheral air branches between raised second pole and shell, excluding only actual first-pole keepout; nominal physical boundaries.')
AIR_CELLS['EntireAirUnderRaisedPole']=[]
for faces,planes,path in partition(H+S2,[O,A]):
 g=raw_probe(faces,'Complete convex first-violated-halfspace partition cell, not a sample.');AIR_CELLS['EntireAirUnderRaisedPole'].append(dict(g,planes=serialized_planes(planes),first_violated_halfspace_path=path))
def contact(name,a,b,poly):
 axis=normalized(sum(np.cross(x,y)for x,y in zip(poly,poly[1:]+poly[:1])));u=normalized(poly[1]-poly[0]);v=np.cross(axis,u);c=sum(poly)/len(poly);area=norm(sum(np.cross(x,y)for x,y in zip(poly,poly[1:]+poly[:1])))/2
 CONTACTS.append(dict(name=name,a=a,b=b,axis=axis.tolist(),u=u.tolist(),v=v.tolist(),origin_m=(0.,0.,0.),plane_m=float(c@axis),points=[c.tolist()],interior_probe_offset_m=.0004,minimum_patch_area_m2=area-2e-7,complete_interface_area_m2=area,complete_interface_polygons_m=[[p.tolist()for p in poly]],finite_patch_count=1))
for name in[POLE_A,POLE_B]:
 ix=0
 for poly,tag in FACES[name]:
  if tag!='cut_0':continue
  # Entire pole inner face is a shell seat iff it lies on a literal outer plane.
  if not any(max(abs(float(p@n-d))for p in poly)<1e-8 for n,d in O):continue
  patch=intersect_polygon(poly,O)
  if len(patch)<3 or norm(sum(np.cross(x,y)for x,y in zip(patch,patch[1:]+patch[:1])))<1e-12:continue
  ix+=1;contact(name+'_EntireShellSeat%02d'%ix,BODY,name,list(reversed(patch)))
 assert ix>0,'Each pole needs real finite shell seats, never proximity.'
for poly,tag in FACES[POLE_B]:
 if tag!='cut_0' or max(abs(float(p[2]-1.276))for p in poly)>1e-8:continue
 patch=intersect_polygon(poly,A)
 if len(patch)>=3:contact('EntireFiniteCrossedCrownSeat',POLE_A,POLE_B,list(reversed(patch)))
assert len([r for r in CONTACTS if r['a']==POLE_A and r['b']==POLE_B])==1
COMPONENT_PAIRS=list(itertools.combinations(sorted(G),2));CONTACT_PAIRS=sorted({tuple(sorted((r['a'],r['b'])))for r in CONTACTS});NONCONTACT_PAIRS=[p for p in COMPONENT_PAIRS if p not in CONTACT_PAIRS]
CONTRACT=dict(single_prop_count=1,new_scene_count=0,kind='prop',closed_meshes=3,materials=4,whole_compound_enclosure=1,whole_continuous_diagonal_poles=2,finite_contact_patches=len(CONTACTS),complete_contact_pairs=len(CONTACT_PAIRS),whole_material_domains=3,whole_air_domains=3,complete_air_cells=sum(map(len,AIR_CELLS.values())),entire_ground_soles=1,physical_boundary_tolerance_m=2e-7,material_domain_inset_m=.002,whole_region_maximum_top_m=1.312,old_geometry_imports=0,static_visual_only=True,real_weather_fit_load_safety_claim=False)
def measure_tent_geometry(vertices):
 assert set(vertices)==set(G);vv=[p for x in vertices.values()for p in x]
 assert abs(min(float(p[2])for p in vv))<=2e-7 and abs(max(float(p[2])for p in vv)-1.312)<=2e-7
 return dict(CONTRACT,scope='Producer geometry only; independent complete source, actual decoded GLB domains and first-front recognition still required.')
FOCUS=(0.,0.,.62);ORTHO=3.22
CAMERAS={'gray-front3q':(3.8,-5.5,3.1),'gray-back3q':(-3.8,5.5,3.1),'thumbnail':(3.8,-5.5,3.1),'qa-front':(0.,-7.,1.65),'qa-side':(7.,0.,1.65),'qa-top':(0.,0.,8.),'qa-back':(0.,7.,1.65),'qa-wireframe':(-3.8,5.5,3.1),'silhouette-128-front':(0.,-7.,1.65),'silhouette-128-side':(7.,0.,1.65)}
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
root=bpy.data.objects.new('OneStaticCrossPoleDomedTent',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='entire integral floor underside at Z0; horizontal bounds centred';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_tent_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'static_tent_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; maker product gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/camping/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'camping','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
