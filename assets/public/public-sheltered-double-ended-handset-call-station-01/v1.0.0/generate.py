"""Unfrozen original telephone SOURCE draft. No production approval, Blender execution or product acceptance."""

import math,collections,json,hashlib

from pathlib import Path

G={}

def add(a,b):return tuple(x+y for x,y in zip(a,b))

def sub(a,b):return tuple(x-y for x,y in zip(a,b))

def mul(a,s):return tuple(x*s for x in a)

def dot(a,b):return sum(x*y for x,y in zip(a,b))

def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

def unit(a):return mul(a,1/math.sqrt(dot(a,a)))

class Mesh:
 def __init__(self):self.v=[];self.f=[];self.fm=[];self.index={}
 def vert(self,p):
  p=tuple(round(float(x),10)for x in p)
  if p not in self.index:self.index[p]=len(self.v);self.v.append(p)
  return self.index[p]
 def tri(self,p,mat=0):self.f.append(tuple(self.vert(v)for v in p));self.fm.append(mat)
 def quad(self,p,mat=0):self.tri([p[0],p[1],p[2]],mat);self.tri([p[0],p[2],p[3]],mat)
 def result(self,role):
  t=[[self.v[i]for i in f]for f in self.f];vol=sum(dot(a,cross(b,c))for a,b,c in t)/6
  if vol<0:self.f=[f[::-1]for f in self.f]
  return dict(vertices=self.v,faces=self.f,face_materials=self.fm,material=0,role=role)

F=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]

DELTA=[(0,0,-1),(0,0,1),(0,-1,0),(0,1,0),(-1,0,0),(1,0,0)]

def union_boxes(specs,e=0):
 # Closed whole boundary of overlapping authored rectangular cells; no duplicated interior faces.
 boxes=[(tuple(x+e for x in a),tuple(x-e for x in b),mat)for a,b,mat in specs]
 axes=[sorted({p[k]for a,b,mat in boxes for p in[a,b]})for k in range(3)];occupied={}
 for i in range(len(axes[0])-1):
  for j in range(len(axes[1])-1):
   for k in range(len(axes[2])-1):
    p=[(axes[q][r]+axes[q][r+1])/2 for q,r in enumerate([i,j,k])];owners=[mat for a,b,mat in boxes if all(a[q]<p[q]<b[q]for q in range(3))]
    if owners:occupied[i,j,k]=owners[-1]
 m=Mesh()
 for (i,j,k),mat in occupied.items():
  pts=[(x,y,z)for z in axes[2][k:k+2]for y in axes[1][j:j+2]for x in axes[0][i:i+2]]
  for d,f in zip(DELTA,F):
   if tuple(a+b for a,b in zip([i,j,k],d))not in occupied:m.quad([pts[n]for n in f],mat)
 return m.result('Complete integral foot/pedestal/back/side-hood/top and raised fixed keypad union, newly authored')

BODY='IntegralFootedOpenHoodCallStation'

HANDSET='WholeDoubleEndedBowedReceiver'

LOWER='WholeLowerHorizontalReceiverSeat'

UPPER='WholeUpperReceiverBackRest'

LEAD='OneContinuousFixedHangingLead'

BOXES=[((-.22,-.20,0),(.22,.20,.06),0),((-.10,.005,.035),(.10,.135,1.02),0),((-.28,.075,.99),(.28,.135,1.70),0),((-.31,-.26,.99),(-.27,.135,1.70),0),((.27,-.26,.99),(.31,.135,1.70),0),((-.31,-.28,1.665),(.31,.135,1.72),0)]

for z in[1.10,1.15,1.20,1.25]:
 for x in[.035,.095,.155]:BOXES.append(((x-.018,.045,z-.014),(x+.018,.09,z+.014),2))

G[BODY]=union_boxes(BOXES)

PROFILE=[(1.06,.045,-.10,-.03),(1.08,.05,-.12,-.015),(1.13,.05,-.14,-.015),(1.16,.025,-.18,-.12),(1.25,.022,-.20,-.14),(1.29,.027,-.18,-.11),(1.32,.05,-.14,-.015),(1.38,.05,-.12,-.015),(1.40,.043,-.10,-.03)]

def receiver(profile):
 m=Mesh();rings=[[(x-.16,y,z)for x,y in[(-w,y0),(w,y0),(w,y1),(-w,y1)]]for z,w,y0,y1 in profile]
 m.quad(rings[0][::-1],1);m.quad(rings[-1],1)
 for k,(a,b)in enumerate(zip(rings,rings[1:])):
  for i in range(4):j=(i+1)%4;m.quad([a[i],a[j],b[j],b[i]],1)
 return m.result('One original continuous two-ended expanded receiver with a genuinely bowed narrow connecting neck; not a stretched old microphone')

G[HANDSET]=receiver(PROFILE)

G[LOWER]=union_boxes([((-.215,-.105,1.035),(-.105,.075,1.060),2)])

G[UPPER]=union_boxes([((-.20,-.015,1.335),(-.12,.075,1.36),2)])

def bezier(a,b,c,d,n):return [add(add(mul(a,(1-t)**3),mul(b,3*(1-t)**2*t)),add(mul(c,3*(1-t)*t*t),mul(d,t**3)))for t in[i/n for i in range(n+1)]]

PATH=bezier((-.21,-.08,1.105),(-.25,-.08,1.105),(-.25,-.08,.98),(-.25,-.08,.90),12)

PATH+=bezier(PATH[-1],(-.25,-.08,.72),(-.23,.045,.70),(-.18,.045,.76),12)[1:]

PATH+=bezier(PATH[-1],(-.16,.045,.79),(-.13,.045,.80),(-.10,.045,.80),8)[1:]

def tube(path,r=.004):
 m=Mesh();rings=[];previous=(0,1,0)
 for i,p in enumerate(path):
  t=(-1,0,0)if i==0 else(1,0,0)if i==len(path)-1 else unit(sub(path[i+1],path[i-1]));u=unit(sub(previous,mul(t,dot(previous,t))));v=cross(t,u);previous=u
  rings.append([add(p,add(mul(u,r*math.cos(math.tau*j/8)),mul(v,r*math.sin(math.tau*j/8))))for j in range(8)])
 for k in[0,len(rings)-1]:
  rr=rings[k][::-1]if k==0 else rings[k]
  for j in range(1,7):m.tri([rr[0],rr[j],rr[j+1]],1)
 for a,b in zip(rings,rings[1:]):
  for j in range(8):k=(j+1)%8;m.quad([a[j],a[k],b[k],b[j]],1)
 return m.result('One continuous uncoiled fixed hanging lead with finite flat end caps, no elastic/circuit or connection performance claim')

G[LEAD]=tube(PATH)

vv=[p for g in G.values()for p in g['vertices']]

SHIFT=tuple(-(min(p[k]for p in vv)+max(p[k]for p in vv))/2 if k<2 else 0 for k in range(3))

for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
import sys,time,itertools,copy
import numpy as np
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='public-sheltered-double-ended-handset-call-station-01';VERSION='1.0.0';TITLE='Sheltered Double-ended Handset Call Station'
DESCRIPTION='One newly authored static public-service call-station appearance: integral footed open hood with a raised fixed twelve-key area, a genuinely two-ended bowed receiver, complete lower horizontal seat and upper backrest, and one continuous hanging lead. All bodies, full functional air regions and finite contact seats are explicit. No actual communication, electrical, payment, emergency, weather, acoustic, accessibility, human-fit, installation or safety claim. Not old drinking-station geometry with a swapped microphone.'
PALETTE=[('Housing_MutedTeal',(.10,.27,.29,1),.68,.12),('Receiver_DeepCharcoal',(.035,.045,.05,1),.72,.0),('SeatAndKeys_WarmMetal',(.60,.53,.39,1),.48,.35)]
def norm(a):return math.sqrt(dot(a,a))

INSETS={}

AIR={}

margin=.001

INSETS[BODY]=union_boxes(BOXES,margin)

INSETS[LOWER]=union_boxes([((-.215,-.105,1.035),(-.105,.075,1.06),2)],margin)

INSETS[UPPER]=union_boxes([((-.20,-.015,1.335),(-.12,.075,1.36),2)],margin)

p=np.array(PROFILE)

slopes=np.diff(p[:,1:],axis=0)/np.diff(p[:,0,None],axis=0)

off=margin*np.sqrt(1+slopes**2)

rings=[]

for i,row in enumerate(p):
 z,w,y0,y1=row.copy()
 if i==0:z+=margin;w,y0,y1=p[0,1:]+slopes[0]*margin;d=off[0]
 elif i==len(p)-1:z-=margin;w,y0,y1=p[-1,1:]-slopes[-1]*margin;d=off[-1]
 else:d=np.maximum(off[i-1],off[i])
 rings.append((float(z),float(w-d[0]),float(y0+d[1]),float(y1-d[2])))

INSETS[HANDSET]=receiver(rings)

path=copy.deepcopy(PATH)

path[0]=add(path[0],(-margin,0,0))

path[-1]=add(path[-1],(-margin,0,0))

INSETS[LEAD]=tube(path,r=.0025)

def box_difference(lo,hi,holes):
 axes=[sorted({lo[k],hi[k]}|{min(hi[k],max(lo[k],p[k]))for a,b in holes for p in[a,b]})for k in range(3)];occupied=set()
 for i in range(len(axes[0])-1):
  for j in range(len(axes[1])-1):
   for k in range(len(axes[2])-1):
    idx=(i,j,k);c=[sum(axes[q][r:r+2])/2 for q,r in enumerate(idx)]
    if not any(all(a[q]<c[q]<b[q]for q in range(3))for a,b in holes):occupied.add(idx)
 mesh=Mesh()
 for i,j,k in sorted(occupied):
  pts=[(x,y,z)for z in axes[2][k:k+2]for y in axes[1][j:j+2]for x in axes[0][i:i+2]]
  for d,f in zip(DELTA,F):
   if tuple(a+b for a,b in zip((i,j,k),d))not in occupied:mesh.quad([pts[n]for n in f])
 return mesh.result('Complete right control bay with all expanded occupied body primitives including pedestal top and twelve keys removed; not sample boxes')

holes=[(tuple(x-margin for x in a),tuple(x+margin for x in b))for a,b,mat in BOXES]

AIR['CompleteAssembledRightControlBay']=box_difference((-.100,-.259,1.001),(.269,.074,1.664),holes)

neck=[]

for i in [3,4,5,6]:
 z,w,y0,y1=p[i];z=float(z);rear=float(y1)
 if i==3:z+=margin;rear=float(p[i,3]+slopes[i,2]*margin)
 if i==6:z-=margin;rear=float(p[i,3]-slopes[i-1,2]*margin)
 adjacent=[off[j,2]for j in [i-1,i]if 0<=j<len(off)];neck.append((z,.019,rear+max(adjacent),.074))

AIR['CompleteReceiverRearNeckOpening']=receiver(neck)

for table in [INSETS,AIR]:
 for g in table.values():g['vertices']=[add(v,SHIFT)for v in g['vertices']]
CONTACTS=[{'name': 'lower-back-full-seat', 'a': 'WholeLowerHorizontalReceiverSeat', 'b': 'IntegralFootedOpenHoodCallStation', 'axis': [0.0, 1.0, 0.0], 'u': [0.0, 0.0, 1.0], 'v': [1.0, 0.0, 0.0], 'plane_m': 0.115, 'complete_interface_polygons_m': [[[-0.215, 0.115, 1.035], [-0.105, 0.115, 1.035], [-0.105, 0.115, 1.06], [-0.215, 0.115, 1.06]]], 'points': [[-0.16, 0.115, 1.0474999999999999]], 'interior_probe_offset_m': 0.0001, 'origin_m': [0, 0, 0], 'complete_interface_area_m2': 0.002750000000000044, 'minimum_patch_area_m2': 0.002749800000000044}, {'name': 'receiver-bottom-full-seat', 'a': 'WholeDoubleEndedBowedReceiver', 'b': 'WholeLowerHorizontalReceiverSeat', 'axis': [-0.0, -0.0, -1.0], 'u': [1.0, 0.0, 0.0], 'v': [0.0, -1.0, 0.0], 'plane_m': -1.06, 'complete_interface_polygons_m': [[[-0.205, -0.06, 1.06], [-0.115, -0.06, 1.06], [-0.115, 0.010000000000000009, 1.06], [-0.205, 0.010000000000000009, 1.06]]], 'points': [[-0.16, -0.024999999999999994, 1.06]], 'interior_probe_offset_m': 0.0001, 'origin_m': [0, 0, 0], 'complete_interface_area_m2': 0.006299999999999999, 'minimum_patch_area_m2': 0.0062997999999999995}, {'name': 'upper-back-full-seat', 'a': 'WholeUpperReceiverBackRest', 'b': 'IntegralFootedOpenHoodCallStation', 'axis': [0.0, 1.0, 0.0], 'u': [0.0, 0.0, 1.0], 'v': [1.0, 0.0, 0.0], 'plane_m': 0.115, 'complete_interface_polygons_m': [[[-0.2, 0.115, 1.335], [-0.12, 0.115, 1.335], [-0.12, 0.115, 1.36], [-0.2, 0.115, 1.36]]], 'points': [[-0.16, 0.115, 1.3475000000000001]], 'interior_probe_offset_m': 0.0001, 'origin_m': [0, 0, 0], 'complete_interface_area_m2': 0.001999999999999974, 'minimum_patch_area_m2': 0.001999799999999974}, {'name': 'receiver-upper-back-full-seat', 'a': 'WholeDoubleEndedBowedReceiver', 'b': 'WholeUpperReceiverBackRest', 'axis': [0.0, 1.0, 0.0], 'u': [0.0, 0.0, 1.0], 'v': [1.0, 0.0, 0.0], 'plane_m': 0.02500000000000001, 'complete_interface_polygons_m': [[[-0.2, 0.02500000000000001, 1.335], [-0.12, 0.02500000000000001, 1.335], [-0.12, 0.02500000000000001, 1.36], [-0.2, 0.02500000000000001, 1.36]]], 'points': [[-0.16, 0.02500000000000001, 1.3475000000000001]], 'interior_probe_offset_m': 0.0001, 'origin_m': [0, 0, 0], 'complete_interface_area_m2': 0.001999999999999974, 'minimum_patch_area_m2': 0.001999799999999974}, {'name': 'lead-start', 'a': 'OneContinuousFixedHangingLead', 'b': 'WholeDoubleEndedBowedReceiver', 'axis': [1.0, 0.0, 0.0], 'u': [0.0, 1.0, 0.0], 'v': [0.0, 0.0, 1.0], 'plane_m': -0.21, 'complete_interface_polygons_m': [[[-0.21, -0.0428284271, 1.1021715729], [-0.21, -0.039999999999999994, 1.101], [-0.21, -0.03717157289999999, 1.1021715729], [-0.21, -0.03599999999999999, 1.105], [-0.21, -0.03717157289999999, 1.1078284271], [-0.21, -0.039999999999999994, 1.109], [-0.21, -0.0428284271, 1.1078284271], [-0.21, -0.044, 1.105]]], 'points': [[-0.21, -0.039999999999999994, 1.105]], 'interior_probe_offset_m': 0.0001, 'origin_m': [0, 0, 0], 'complete_interface_area_m2': 4.525483359999957e-05, 'minimum_patch_area_m2': 4.5054833599999574e-05}, {'name': 'lead-end', 'a': 'OneContinuousFixedHangingLead', 'b': 'IntegralFootedOpenHoodCallStation', 'axis': [1.0, 0.0, 0.0], 'u': [0.0, 1.0, 0.0], 'v': [0.0, 0.0, 1.0], 'plane_m': -0.1, 'complete_interface_polygons_m': [[[-0.1, 0.08101009940000001, 0.7997159342], [-0.1, 0.08237957910000002, 0.7969778494], [-0.1, 0.0852840658, 0.7960100994], [-0.1, 0.08802215060000002, 0.7973795791], [-0.1, 0.0889899006, 0.8002840658], [-0.1, 0.08762042090000001, 0.8030221506], [-0.1, 0.08471593420000001, 0.8039899006], [-0.1, 0.08197784940000001, 0.8026204209]]], 'points': [[-0.09999999999999999, 0.085, 0.8]], 'interior_probe_offset_m': 0.0001, 'origin_m': [0, 0, 0], 'complete_interface_area_m2': 4.5254834164017155e-05, 'minimum_patch_area_m2': 4.505483416401716e-05}]
LINKS=[];GAPS=[];BORES=[];FOOT_CONTACTS=[];FEET=[BODY];ISOLATED_VOID_VOLUMES={}
SOLID_VOLUMES={n+'_WholeInset':dict(g,targets=[n])for n,g in INSETS.items()}
VOID_VOLUMES={n:dict(g,targets=list(G),isolated=False)for n,g in AIR.items()}
INSIDE_TESTS=[(BODY,add((0,.07,.5),SHIFT),(3,3,3)),(HANDSET,add((-.16,-.17,1.25),SHIFT),(3,3,3)),(LOWER,add((-.16,-.02,1.045),SHIFT),(3,3,3)),(UPPER,add((-.16,.03,1.35),SHIFT),(3,3,3)),(LEAD,add(PATH[16],SHIFT),(3,3,3))]
CONTRACT=dict(single_prop_count=1,new_scene_count=0,kind='prop',native_axis_up='Z',front_direction='-Y',origin='horizontal bounds-centred; complete integral foot on Z0',closed_meshes=5,materials=3,whole_finite_material_domains=5,complete_assembled_air_domains=2,full_opposed_contact_pairs=6,finite_contact_patch_count=6,all_noncontact_pairs=4,whole_ground_soles=1,old_geometry_imports=0,fixed_visual_only=True)
def measure_telephone_geometry(vertices):
 vv=[p for row in vertices.values()for p in row];lo=[min(p[i]for p in vv)for i in range(3)];hi=[max(p[i]for p in vv)for i in range(3)]
 return dict(CONTRACT,bounds_m=[hi[i]-lo[i]for i in range(3)],scope='Prepared full numeric phone; complete actual predicates and first original pixels still mandatory')
FOCUS=(0,0,.86);ORTHO=2.10;WIRE_THICKNESS=.0011
CAMERAS={'thumbnail':(3,-5,2.5),'qa-front':(0,-7,2),'qa-side':(7,0,2),'qa-top':(0,0,7),'qa-back':(0,7,2),'qa-wireframe':(3,-5,2.5),'gray-front3q':(3,-5,2.5),'gray-back3q':(-3,5,2.5),'silhouette-128-front':(0,-7,2),'silhouette-128-side':(7,0,2)}

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
root=bpy.data.objects.new('OneShelteredDoubleEndedHandsetCallStation',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='complete foot at Z0; fixed receiver in two finite seats, no communication claim';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_telephone_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'telephone_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; maker product gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/public/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'public','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
