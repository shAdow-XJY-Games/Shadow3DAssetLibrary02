"""New fixed tape-dispenser pure numeric draft. No Blender or SOURCE approval.
Generic finite line arrangement idea reused from own reviewed bay prototype;
all tape/base/axle/linear cutter dimensions and material constructions new.
"""
import math,collections,json,time,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
CY=.04;CZ=.055+.017*math.cos(math.pi/8);AZ=.055+.010*math.cos(math.pi/8)
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(v,s):return tuple(x*s for x in v)
def unit(v):
 n=math.sqrt(dot(v,v));assert math.isfinite(n) and n>0
 return tuple(x/n for x in v)
def area(p):return sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))/2
def clean(p):
 out=[]
 for q in p:
  q=tuple(round(x,12)for x in q)
  if not out or q!=out[-1]:out.append(q)
 if len(out)>1 and out[0]==out[-1]:out.pop()
 return out

def clip(p,l):
 if not p:return []
 a,b,c=l;out=[];u=p[-1];du=a*u[0]+b*u[1]-c
 for v in p:
  dv=a*v[0]+b*v[1]-c
  if(du<=1e-13)!=(dv<=1e-13):
   t=du/(du-dv);out.append(tuple(u[k]+t*(v[k]-u[k])for k in range(2)))
  if dv<=1e-13:out.append(v)
  u=v;du=dv
 out=clean(out);return out if len(out)>2 and area(out)>1e-14 else []
def planes(p):
 out=[]
 for a,b in zip(p,p[1:]+p[:1]):
  u,v=b[0]-a[0],b[1]-a[1];n=math.hypot(u,v);out.append((v/n,-u/n,(v*a[0]-u*a[1])/n))
 return out

def contains(p,poly):
 # All classified cells already split at every edge's entire supporting line.
 x,y=p;inside=False
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if(a[1]>y)!=(b[1]>y)and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:inside=not inside
 return inside

def rect(y0,z0,y1,z1):return[(y0,z0),(y1,z0),(y1,z1),(y0,z1)]
def poly(radius,n=16,cy=CY,cz=CZ,phase=math.pi/16):return[(cy+radius*math.cos(phase+math.tau*i/n),cz+radius*math.sin(phase+math.tau*i/n))for i in range(n)]
def build(parts,holes=[],mat=0):
 # Each part: x0,x1,CCW yz polygon. Union boundary only, no internal faces.
 polygons=[r[2]for r in parts+holes];allp=[q for p in polygons for q in p];lo=[min(q[k]for q in allp)for k in[0,1]];hi=[max(q[k]for q in allp)for k in[0,1]]
 cells=[rect(lo[0],lo[1],hi[0],hi[1])];seen=set();lines=[]
 for p in polygons:
  for l in planes(p):
   key=tuple(round(x,10)for x in l)
   if key not in seen:seen.add(key);lines.append(l)
 for l in lines:
  nxt=[]
  for p in cells:
   ds=[l[0]*q[0]+l[1]*q[1]-l[2]for q in p]
   if min(ds)<-1e-10 and max(ds)>1e-10:
    a=clip(p,l);b=clip(p,tuple(-v for v in l));assert a and b,(l,p);nxt +=[a,b]
   else:nxt.append(p)
  cells=nxt
 ec=collections.defaultdict(list)
 for i,p in enumerate(cells):
  for a,b in zip(p,p[1:]+p[:1]):ec[tuple(sorted((a,b)))].append(i)
 assert all(len(v)<=2 for v in ec.values())
 xx=sorted(set(v for a,b,p in parts+holes for v in[a,b]));occ=[]
 for x0,x1 in zip(xx,xx[1:]):
  x=(x0+x1)/2;ss=set()
  for i,p in enumerate(cells):
   c=tuple(sum(q[k]for q in p)/len(p)for k in[0,1])
   if any(a<x<b and contains(c,q)for a,b,q in parts)and not any(a<x<b and contains(c,q)for a,b,q in holes):ss.add(i)
  occ.append(ss)
 vv=[];ff=[];lookup={}
 def vertex(p):
  p=tuple(round(x,12)for x in p)
  if p not in lookup:lookup[p]=len(vv);vv.append(p)
  return lookup[p]
 def tri(p):
  assert dot(cross(sub(p[1],p[0]),sub(p[2],p[0])),cross(sub(p[1],p[0]),sub(p[2],p[0])))>1e-28,p
  ids=tuple(vertex(q)for q in p);assert len(set(ids))==3;ff.append(ids)
 for k,ss in enumerate(occ):
  x0,x1=xx[k:k+2]
  for i in sorted(ss):
   p=cells[i];c=tuple(sum(q[h]for q in p)/len(p)for h in[0,1])
   for x,sign,j in[(x0,-1,k-1),(x1,1,k+1)]:
    if not 0<=j<len(occ)or i not in occ[j]:
     for a,b in zip(p,p[1:]+p[:1]):
      q=[(x,*c),(x,*a),(x,*b)];tri(q if sign>0 else q[::-1])
   for a,b in zip(p,p[1:]+p[:1]):
    other=next((j for j in ec[tuple(sorted((a,b)))]if j!=i),None)
    if other is None or other not in ss:
     aa=(x0,*a);bb=(x0,*b);cc=(x1,*b);dd=(x1,*a);tri([aa,bb,cc]);tri([aa,cc,dd])
 return dict(vertices=vv,faces=ff,face_materials=[mat]*len(ff),material=mat,yz_cells=len(cells),x_levels=xx)

def geometry():
 base=(-.043,.043,rect(-.122,0,.09,.012))
 # Whole U-shaped side towers; flat notch floor at exactly z=.055.
 support=[(CY-.025,.0),(CY+.025,.0),(CY+.025,.090),(CY+.012,.090),(CY+.012,.055),(CY-.012,.055),(CY-.012,.090),(CY-.025,.090)]
 body=build([base,(-.034,-.023,support),(.023,.034,support),(-.018,.018,rect(-.112,0,-.094,.058))],mat=0)
 # Convex strip overlaps a finite part of ring then terminates at flat cutter ledge.
 tail=[(-.110,.062),(-.098,.062),(.014,.101),(.014,.1025),(-.098,.0635),(-.110,.0635)]
 band=build([(-.014,.014,poly(.043)),(-.014,.014,tail)],[(-.014,.014,poly(.017,8,phase=math.pi/8))],mat=1)
 shaft=build([(-.034,.034,poly(.010,8,cz=AZ,phase=math.pi/8))],mat=2)
 # Blade plan in XY becomes an extruded profile then axis-permuted. Four full teeth.
 plan=[(-.018,-.112),(-.018,-.117)]
 for i in range(4):
  x=-.018+i*.009;plan.extend([(x+.0045,-.122),(x+.009,-.117)])
 plan.extend([(.018,-.092),(-.018,-.092)])
 cutter=build([(.058,.062,plan)],mat=2)
 # old coordinates (height, X, Y) -> (X,Y,height), cyclic permutation.
 cutter['vertices']=[(p[1],p[2],p[0])for p in cutter['vertices']]
 return dict(IntegralGroundBaseTwinSideCradleAndCutterNeck=body,AnnularTapeMassWithContinuousFreeTail=band,FixedLowerSeatedOctagonalAxle=shaft,WholeLinearToothCutterWithLandingLedge=cutter)

def topology(g):
 v=g['vertices'];f=g['faces'];e=collections.defaultdict(list);stars=collections.defaultdict(list)
 for t in f:
  for a,b in zip(t,t[1:]+t[:1]):e[tuple(sorted((a,b)))].append((a,b))
  for j,a in enumerate(t):stars[a].append(tuple(t[k]for k in range(3)if k!=j))
 bad=[(k,q)for k,q in e.items()if len(q)!=2 or q[0]!=q[1][::-1]];assert not bad,bad[:10]
 for i,links in stars.items():
  a=collections.defaultdict(set)
  for x,y in links:a[x].add(y);a[y].add(x)
  seen=set();todo=[next(iter(a))]
  while todo:
   x=todo.pop()
   if x not in seen:seen.add(x);todo.extend(a[x]-seen)
  assert seen==set(a)and all(len(q)==2 for q in a.values()),('fan',i)
 volume=sum(dot(v[a],cross(v[b],v[c]))for a,b,c in f)/6;assert volume>0
 return dict(vertices=len(v),triangles=len(f),euler=len(v)-len(e)+len(f),signed_volume=volume,single_vertex_fans=True)
"""Complete declared finite domains draft. Not SOURCE, not Blender acceptance."""

E=.0004
NAMES=list(geometry())
def offset(p,e):
    """Parallel-edge polygon inset; used only for these simple unchanged-edge profiles."""
    p=[b for a,b,c in zip(p[-1:]+p[:-1],p,p[1:]+p[:1]) if abs((b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0]))>1e-14]
    pp=planes(p);out=[]
    for i,(a,b,c) in enumerate(pp):
        d,f,g=pp[i-1];det=d*b-f*a;assert abs(det)>1e-10
        out.append((( (g-e)*b-f*(c-e))/det,(d*(c-e)-(g-e)*a)/det))
    assert area(out)>0
    return clean(out)
def baseparts(e=0):
    support=[(CY-.025,0),(CY+.025,0),(CY+.025,.090),(CY+.012,.090),(CY+.012,.055),(CY-.012,.055),(CY-.012,.090),(CY-.025,.090)]
    return [(-.043+e,.043-e,offset(rect(-.122,0,.09,.012),e)),(-.034+e,-.023-e,offset(support,e)),(.023+e,.034-e,offset(support,e)),(-.018+e,.018-e,offset(rect(-.112,0,-.094,.058),e))]
def tail():return [(-.110,.062),(-.098,.062),(.014,.101),(.014,.1025),(-.098,.0635),(-.110,.0635)]
def bandparts(e=0):return [(-.014+e,.014-e,offset(poly(.043),e)),(-.014+e,.014-e,offset(tail(),e))]
def bore(e=0):return offset(poly(.017,8,phase=math.pi/8),e)
def axle(e=0):return offset(poly(.010,8,cz=AZ,phase=math.pi/8),e)
def cutterplan():
    p=[(-.018,-.112),(-.018,-.117)]
    for i in range(4):
        x=-.018+i*.009;p.extend([(x+.0045,-.122),(x+.009,-.117)])
    return p+[(.018,-.092),(-.018,-.092)]
def rotate(g):
    g['vertices']=[(p[1],p[2],p[0])for p in g['vertices']];return g

def insets():
    return {NAMES[0]:build(baseparts(E)),NAMES[1]:build(bandparts(E),[(-.014+E,.014-E,bore(-E))]),NAMES[2]:build([(-.034+E,.034-E,axle(E))]),NAMES[3]:rotate(build([(.058+E,.062-E,offset(cutterplan(),E))]))}

def air():
    r={}
    # Isolated core intentionally targets only tape mass. No assembled-through claim.
    r['isolated_whole_tape_core']=(build([(-.014-E,.014+E,bore(E))]),[NAMES[1]])
    # Both complete ring mouths to before side posts. Whole offset core-minus-shaft.
    r['entire_installed_core_residual_before_side_posts']=(build([(-.023+E,.023-E,bore(E))],[(-.023+E,.023-E,axle(-E))]),NAMES)
    for sign,label in [(-1,'left'),(1,'right')]:
        a,b=sorted([sign*(.023-E),sign*(.034+E)])
        # Exact full support notch rectangle, expanded mouth above support crown.
        r[label+'_whole_side_notch_egress']=(build([(a,b,rect(CY-.012+E,.055+E,CY+.012-E,.095))],[(a,b,axle(-E))]),NAMES)
    # Entire lower outer-roll envelope, from base top. Supporting-line offset,
    # complete lower hemisphere chain: leftmost -> bottom -> rightmost.
    p=offset(poly(.043),-E);start=min(range(len(p)),key=lambda i:(p[i][0],p[i][1]));chain=[];i=start
    while True:
        chain.append(p[i]);i=(i+1)%len(p)
        if p[i][0] < chain[-1][0]-1e-10:break
    # CCW lower chain increases Y; air sits below it, hence reverse on upper edge.
    lower=[(chain[0][0]+E,.012+E),(chain[-1][0]-E,.012+E)]+list(reversed(chain))
    # Trim the two finite Y endpoints by E to avoid a zero-width tangent edge.
    lower=clip(lower,(-1,0,-(chain[0][0]+E)));lower=clip(lower,(1,0,chain[-1][0]-E))
    r['entire_under_roll_envelope']=(build([(-.014+E,.014-E,lower)]),NAMES)
    # Full tail lower profile to base, with actual occupied ring/neck/cutter removed.
    # Polygon first goes right along floor then left along the entire lower profile.
    tailgap=[(-.110+E,.012+E),(.014-E,.012+E),(.014-E,.101),(-.098,.062),(-.110+E,.062)]
    # Offset upper profile by actual perpendicular clearance, not only vertical delta.
    upper=planes(tail())[1] # sloped lower edge from(-.098,.062)to(.014,.101)
    # air is on opposite side of band supporting line, keep outward with E separation.
    # Tail lower mask is union flat left and sloped right, two complete subprofiles.
    slope=lambda y:.062+(y+.098)*(.039/.112)-E*math.hypot(1,.039/.112)
    underparts=[(-.014+E,.014-E,rect(-.110+E,.012+E,-.098,.062-E)),(-.014+E,.014-E,[(-.098,.012+E),(.014-E,.012+E),(.014-E,slope(.014-E)),(-.098,slope(-.098))])]
    # Full protrusions as expanded profiles, X ranges cover whole target domain.
    underholes=[(-.1,.1,offset(poly(.043),-E)),(-.018-E,.018+E,offset(rect(-.112,0,-.094,.058),-E)),(-.018-E,.018+E,rect(-.122-E,.058-E,-.092+E,.062+E))]
    r['entire_free_tail_underside_minus_true_occupied_supports']=(build(underparts,underholes),NAMES)
    # Full lateral silhouette (including the whole bore projection) minus actual
    # front occupied supports. Restrict to inboard ring-to-post clearances.
    for sign,label in [(-1,'left'),(1,'right')]:
        a,b=sorted([sign*(.014+E),sign*(.023-E)])
        parts=[(a,b,offset(poly(.043),E)),(a,b,offset(tail(),E))]
        holes=[(-.018-E,.018+E,offset(rect(-.112,0,-.094,.058),-E)),(-.018-E,.018+E,rect(-.122-E,.058-E,-.092+E,.062+E)),(-.034-E,.034+E,axle(-E))]
        r[label+'_entire_side_clearance_minus_actual_forward_supports']=(build(parts,holes),NAMES)
    # Three internal finite V openings. Closed inner domain covers their complete
    # notch polygon at uniform wall margins and extends forward beyond tooth tips.
    for i in range(3):
        x=-.009+i*.009
        p=[(x-.0045,-.126),(x+.0045,-.126),(x+.0045,-.122),(x,-.117),(x-.0045,-.122)]
        r['whole_linear_tooth_notch_'+str(i+1)]=(rotate(build([(.058+E,.062-E,offset(p,E))])),NAMES)
    return r

def connected(g):
    adj=collections.defaultdict(set)
    for a,b,c in g['faces']:
        for u,v in[(a,b),(b,c),(c,a)]:adj[u].add(v);adj[v].add(u)
    remain=set(adj);sizes=[]
    while remain:
        todo=[next(iter(remain))];s=set()
        while todo:
            u=todo.pop()
            if u not in s:s.add(u);todo.extend(adj[u]-s)
        remain-=s;sizes.append(len(s))
    return sizes

START=time.time()
ASSET='florist-fixed-payout-desktop-tape-dispenser-01';VERSION='1.0.0';TITLE='Fixed-Payout Desktop Tape Dispenser'
DESCRIPTION=('One newly authored static florist wrapping-station tape-dispenser prop: one integral grounded base with two U-notched side supports and a front cutter neck; one lower-seated octagonal axle; one closed annular tape mass genuinely continuous with a flat oblique free tail; and one complete four-tooth linear cutter plate with a flat landing ledge. The free tail terminates on that elevated ledge ahead of the roll rather than as a floor sweep or separately retained cable end. All material is opaque untextured constant PBR; native metres, Z up, front -Y, horizontal-bound-centred ground origin. Counted once, not a scene or a family variant. The thick annular mass is only a fixed tape-roll appearance, NOT separate realistic windings, an unwinding simulation, adhesive or working feed. Installed bore clearance subtracts the real axle; side supports partially occlude the core mouths and are evaluated through separate complete notch egress volumes, never called an unobstructed full bore through the assembled stand. Mathematical contacts and empty domains do not certify cutting sharpness, tape adhesion, movement, dispensing, assembly route, stability, material strength, safe handling, fabrication or commercial operation. No old backdrop, reel, cradle, stapler or other asset geometry is imported.')
PALETTE=[('DispenserBase_MutedPetrol',(.055,.17,.18,1),.77,.0),('FixedTapeMass_WarmIvory',(.73,.66,.46,1),.8,.0),('AxleAndCutter_BrushedGrey',(.30,.34,.35,1),.55,.35)]
LINKS=[];GAPS=[];BORES=[];FOOT_CONTACTS=[]

Y_SHIFT=.016
G=geometry();SOLID_VOLUMES={};VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={}
def shifted(g):
 g['vertices']=[(x,y+Y_SHIFT,z)for x,y,z in g['vertices']];return g
for name,g in G.items():shifted(g);g['role']=name+'; whole original closed material, fixed visual state'
for name,g in insets().items():
 shifted(g);g['targets']=[name];g['role']='Entire declared conservative parallel-profile inset, not maximal Euclidean erosion';SOLID_VOLUMES['WholeInset_'+name]=g
for name,(g,targets)in air().items():
 shifted(g);g['targets']=list(targets);g['role']='Whole finite declared domain with occupied material subtracted; not sparse witnesses'
 (ISOLATED_VOID_VOLUMES if name.startswith('isolated_')else VOID_VOLUMES)[name]=g
BASE,BAND,SHAFT,CUTTER=NAMES;FEET=[BASE];EXPECTED_EULER={BASE:2,BAND:0,SHAFT:2,CUTTER:2}
SEAT_WIDTH=2*.010*math.sin(math.pi/8)
FINITE_CONTACTS={(BASE,SHAFT):(.055,[(-.034,CY-SEAT_WIDTH/2+Y_SHIFT,-.023,CY+SEAT_WIDTH/2+Y_SHIFT),(.023,CY-SEAT_WIDTH/2+Y_SHIFT,.034,CY+SEAT_WIDTH/2+Y_SHIFT)]),(BAND,SHAFT):(.055,[(-.014,CY-SEAT_WIDTH/2+Y_SHIFT,.014,CY+SEAT_WIDTH/2+Y_SHIFT)]),(BASE,CUTTER):(.058,[(-.018,-.112+Y_SHIFT,.018,-.094+Y_SHIFT)]),(BAND,CUTTER):(.062,[(-.014,-.110+Y_SHIFT,.014,-.098+Y_SHIFT)])}
CONTACTS=[]
for(a,b),(z,patches)in FINITE_CONTACTS.items():
 if(a,b)==(BAND,CUTTER):a,b=b,a
 area_=sum((x1-x0)*(y1-y0)for x0,y0,x1,y1 in patches)
 CONTACTS.append(dict(a=a,b=b,origin_m=(0,0,0),axis=(0,0,1),u=(1,0,0),v=(0,1,0),plane_m=z,points=[((x0+x1)/2,(y0+y1)/2,z)for x0,y0,x1,y1 in patches],interior_probe_offset_m=.0002,minimum_patch_area_m2=area_*.98,complete_interface_area_m2=area_,finite_xy_rectangles=patches))
CONTRACT=dict(single_modular_count=0,single_prop_count=1,new_scene_count=0,kind='prop',native_axis_up='Z',front_direction='-Y',origin='horizontal bounds centre and complete base sole at Z0',closed_connected_meshes=4,materials=3,whole_material_volumes=4,whole_assembled_air_volumes=10,whole_isolated_air_volumes=1,air_target_matrix_pairs=41,finite_opposed_contacts=4,contact_patches=5,all_unordered_pairs=6,contact_pairs=4,noncontact_pairs=2,whole_ground_soles=1,complete_ground_area_m2=.086*.212,old_geometry_imports=0,fixed_visual_only=True,realistic_windings=False,assembled_full_core_unobstructed=False)
def measure_tape_geometry(vertices):
 assert set(vertices)==set(G);vv=[p for v in vertices.values()for p in v];lo=[min(p[k]for p in vv)for k in range(3)];hi=[max(p[k]for p in vv)for k in range(3)]
 assert abs(lo[2])<2e-7 and max(abs(lo[k]+hi[k])for k in[0,1])<2e-7
 assert abs(hi[0]-lo[0]-.086)<2e-7 and abs(hi[1]-lo[1]-.212)<2e-7
 return dict(CONTRACT,bounds_m=[hi[k]-lo[k]for k in range(3)],scope='Producer measurements only. Complete finite domains, all surfaces, exact finite contact boundaries and actual GLB binding remain separate maker gates.')
INSIDE_TESTS=[(BASE,(0,Y_SHIFT,.006),(0,Y_SHIFT,.020)),(BAND,(0,CY+Y_SHIFT,CZ+.035),(0,CY+Y_SHIFT,CZ)),(SHAFT,(0,CY+Y_SHIFT,AZ),(0,CY+Y_SHIFT,AZ+.02)),(CUTTER,(0,-.103+Y_SHIFT,.060),(0,-.103+Y_SHIFT,.070))]
FOCUS=(0,0,.055);ORTHO=.30
CAMERAS={'gray-front3q':(.34,-.42,.28),'gray-back3q':(-.34,.42,.28),'thumbnail':(.34,-.42,.28),'qa-front':(0,-.55,.15),'qa-side':(.55,0,.15),'qa-top':(0,0,.65),'qa-back':(0,.55,.15),'qa-wireframe':(.34,-.42,.28),'silhouette-128-front':(0,-.55,.15),'silhouette-128-side':(.55,0,.15)}
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
root=bpy.data.objects.new('OneFixedPayoutDesktopTapeDispenser',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole base sole at Z=0; actual seated axle and fixed band tail on elevated cutter; no working dispensing claim';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_tape_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_modular_count':0,'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'fixed_payout_tape_dispenser_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
