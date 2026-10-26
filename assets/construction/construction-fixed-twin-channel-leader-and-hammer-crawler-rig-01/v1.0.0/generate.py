"""One newly authored complete twin channel leader and hammer crawler rig exterior. Static art only."""
import math,collections,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
G={}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.fm=[];self.index={}
 def vertex(self,p):
  p=tuple(round(float(x),9)for x in p)
  if p not in self.index:self.index[p]=len(self.v);self.v.append(p)
  return self.index[p]
 def tri(self,p,mat):self.f.append(tuple(self.vertex(v)for v in p));self.fm.append(mat)
 def quad(self,a,b,c,d,mat):self.tri([a,b,c],mat);self.tri([a,c,d],mat)
 def result(self,role):
  edges={}
  for i,f in enumerate(self.f):
   for a,b in zip(f,f[1:]+f[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((i,a,b))
  assert all(len(v)==2 for v in edges.values()),[(e,v)for e,v in edges.items()if len(v)!=2][:5]
  signs={0:1};todo=[0]
  while todo:
   i=todo.pop()
   for a,b in zip(self.f[i],self.f[i][1:]+self.f[i][:1]):
    for j,c,d in edges[tuple(sorted((a,b)))]:
     if i==j:continue
     want=signs[i]*(-1 if(a,b)==(c,d)else 1)
     if j in signs:assert signs[j]==want
     else:signs[j]=want;todo.append(j)
  assert len(signs)==len(self.f)
  ff=[f if signs[i]>0 else tuple(reversed(f))for i,f in enumerate(self.f)];vol=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]]))for f in ff)/6
  if vol<0:ff=[tuple(reversed(f))for f in ff]
  assert all(dot(cross(sub(self.v[f[1]],self.v[f[0]]),sub(self.v[f[2]],self.v[f[0]])),cross(sub(self.v[f[1]],self.v[f[0]]),sub(self.v[f[2]],self.v[f[0]])))>1e-18 for f in ff)
  return dict(vertices=self.v,faces=ff,face_materials=self.fm,material=0,role=role)

def area2(p):return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1]))/2
def earclip(p):
 order=list(range(len(p))) if area2(p)>0 else list(reversed(range(len(p))));out=[]
 cr=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 while len(order)>3:
  found=False
  for j,b in enumerate(order):
   a,c=order[j-1],order[(j+1)%len(order)]
   if cr(p[a],p[b],p[c])<1e-14:continue
   if any(all(cr(p[u],p[v],p[k])>=-1e-14 for u,v in [(a,b),(b,c),(c,a)]) for k in order if k not in [a,b,c]):continue
   out.append((a,b,c));order.pop(j);found=True;break
  assert found,('untriangulable',p,order)
 out.append(tuple(order));return out


def extrude(poly,a,b,axis,mat,role):
 m=Mesh();pt=lambda p,t:(p[0],p[1],t)if axis=='z'else(t,p[0],p[1])if axis=='x'else(p[0],t,p[1])
 for t in[a,b]:
  for f in earclip(poly):m.tri([pt(poly[j],t)for j in f],mat)
 for p,q in zip(poly,poly[1:]+poly[:1]):m.quad(pt(p,a),pt(q,a),pt(q,b),pt(p,b),mat)
 return m.result(role)
def block(lo,hi,mat,role):return extrude([(lo[0],lo[1]),(hi[0],lo[1]),(hi[0],hi[1]),(lo[0],hi[1])],lo[2],hi[2],'z',mat,role)

def axial(profile,center,u,v,w,n,materials,role,phase=0):
 m=Mesh();rings=[[add(center,add(mul(w,t),add(mul(u,r*math.cos(phase+j*math.tau/n)),mul(v,r*math.sin(phase+j*math.tau/n)))))for j in range(n)]for r,t in profile]
 for k,a in enumerate(rings):
  kk=(k+1)%len(rings);b=rings[kk];ra=profile[k][0];rb=profile[kk][0];mat=materials[k]if isinstance(materials,list)else materials
  if ra==rb==0:continue
  for j in range(n):
   i=(j+1)%n
   if ra==0:m.tri([a[0],b[j],b[i]],mat)
   elif rb==0:m.tri([a[j],a[i],b[0]],mat)
   else:m.quad(a[j],a[i],b[i],b[j],mat)
 return m.result(role)
def unit(v):return mul(v,1/math.sqrt(dot(v,v)))
def beam(a,b,width,depth,mat,role):
 w=unit(sub(b,a));ref=(0,0,1)if abs(w[2])<.9 else(0,1,0);u=unit(cross(w,ref));v=cross(w,u);m=Mesh();rows=[]
 for p in[a,b]:rows.append([add(p,add(mul(u,s*width/2),mul(v,t*depth/2)))for s,t in[(-1,-1),(1,-1),(1,1),(-1,1)]])
 for row in rows:m.quad(*row,mat)
 for i in range(4):j=(i+1)%4;m.quad(rows[0][i],rows[0][j],rows[1][j],rows[1][i],mat)
 return m.result(role)



def solid_union(boxes,mat,role):
 xs=sorted({p[0]for b in boxes for p in b});ys=sorted({p[1]for b in boxes for p in b});zs=sorted({p[2]for b in boxes for p in b});faces={};m=Mesh()
 for i in range(len(xs)-1):
  for j in range(len(ys)-1):
   for k in range(len(zs)-1):
    c=((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)
    if not any(all(lo[t]<c[t]<hi[t]for t in range(3))for lo,hi in boxes):continue
    vv=[(x,y,z)for z in[zs[k],zs[k+1]]for y in[ys[j],ys[j+1]]for x in[xs[i],xs[i+1]]]
    for f in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:
     q=tuple(vv[t]for t in f);key=tuple(sorted(q))
     if key in faces:del faces[key]
     else:faces[key]=q
 for q in faces.values():m.quad(*q,mat)
 return m.result(role)
def cyl(n,a,b,r,mat,role,N=24):
 w=unit(sub(b,a));ref=(0,0,1)if abs(w[2])<.9 else(0,1,0);u=unit(cross(w,ref));v=cross(w,u);h=math.sqrt(dot(sub(b,a),sub(b,a)))
 G[n]=axial([(0,0),(r,0),(r,h),(0,h)],a,u,v,w,N,mat,role)
# One whole newly authored crawler carrier, paired channel leader and fixed guided hammer exterior.
G={};ROOT_WITNESSES=[];AIR_POINTS=[];GROUND=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
def box(n,a,b,m,role):G[n]=block(a,b,m,role)
def annular_prism(outer,inner,x0,x1,mat,role):
 m=Mesh();N=len(outer)
 for i in range(N):
  j=(i+1)%N
  for x in[x0,x1]:m.quad((x,*outer[i]),(x,*outer[j]),(x,*inner[j]),(x,*inner[i]),mat)
  for row in[outer,inner]:m.quad((x0,*row[i]),(x0,*row[j]),(x1,*row[j]),(x1,*row[i]),mat)
 return m.result(role)
def track_loop(r):return[(y+r*math.cos(t),.31+r*math.sin(t))for y,start in[(.94,-math.pi/2),(-.94,math.pi/2)]for t in[start+j*math.pi/12 for j in range(13)]]
for lab,s in[('Left',-1),('Right',1)]:
 x0,x1=sorted([s*.76,s*1.16]);n='WholeContinuousTrack'+lab;G[n]=annular_prism(track_loop(.31),track_loop(.225),x0,x1,2,'One complete thick fixed crawler loop with genuine central opening and full straight lower facet; no articulated shoes, traction or driving capability.');GROUND.append(n)
 for i,y in enumerate([-.94,-.31,.31,.94]):
  q='WholeTrackRoller'+lab+str(i);cyl(q,(x0+.024,y,.31),(x1-.024,y,.31),.237,3,'One entire fixed transverse roller, visible end planes inset within the complete belt.',20);join(q,n,(s*.96,y,.079));join(q,'WholeLowCarrierFrame',(s*.81,y,.31))
G['WholeLowCarrierFrame']=solid_union([((-.85,-1.06,.245),(-.64,1.06,.43)),((.64,-1.06,.245),(.85,1.06,.43)),((-.78,-.76,.35),(.78,-.50,.55)),((-.78,.51,.35),(.78,.77,.55))],2,'One complete low connected ladder carrier roots both closed tracks and the entire long upper deck. Not an old slewing dragline body instance.')
G['WholeLongCarrierDeck']=extrude([(-.84,-1.37),(.84,-1.37),(.91,-1.22),(.91,1.39),(.75,1.52),(-.75,1.52),(-.91,1.39),(-.91,-1.22)],.49,.69,'z',0,'One complete newly drawn long rigid machinery deck reaches forward under the vertical leader feet and back below the power-house exterior. No slew mechanism or working machinery claim.');join('WholeLongCarrierDeck','WholeLowCarrierFrame',(0,.63,.53))
G['WholeRearMachineryExterior']=extrude([(.25,.66),(1.39,.66),(1.39,1.40),(1.16,1.58),(.42,1.58),(.25,1.43)],-.72,.71,'x',0,'One whole rear machinery-case exterior with chamfered upper shoulders, independent from the forward leader and small left cab; no engine, fuel or hydraulic internals.');join('WholeRearMachineryExterior','WholeLongCarrierDeck',(0,.8,.675))
G['WholeSideCabShell']=solid_union([((-.91,-1.03,.66),(-.23,.29,1.04)),((-.91,-1.03,1.76),(-.23,.29,1.85)),((-.91,-1.03,1.0),(-.83,-.95,1.80)),((-.31,-1.03,1.0),(-.23,-.95,1.80)),((-.91,.21,1.0),(-.83,.29,1.80)),((-.31,.21,1.0),(-.23,.29,1.80))],0,'One complete forward side cabin shell has genuine broad window openings, integral low body and roof. Empty static shell, no occupant or ergonomic fit.');join('WholeSideCabShell','WholeLongCarrierDeck',(-.57,-.45,.675))
box('WholeLowRearCounterbody',(-.76,1.20,.68),(.76,1.57,.99),1,'One whole low broad counterbody appearance extends behind the machinery case with its visible upper and end planes intentionally offset, without balance or stability claim.');join('WholeLowRearCounterbody','WholeLongCarrierDeck',(0,1.40,.685))
# Full front leader posts have actual inward-facing C channels throughout their height.
left=[(-.44,-1.45),(-.25,-1.45),(-.25,-1.39),(-.38,-1.39),(-.38,-1.16),(-.25,-1.16),(-.25,-1.10),(-.44,-1.10)]
for lab,s in[('Left',-1),('Right',1)]:
 poly=left if s<0 else[(-x,y)for x,y in reversed(left)];n='WholeChannelLeader'+lab;G[n]=extrude(poly,.65,4.38,'z',0,'One entire tall inward-facing C-section leader post, with real channel space rather than a painted groove. Whole vertical guidance appearance is new, not the inclined triangular lattice boom of a dragline.');join(n,'WholeLongCarrierDeck',(s*.41,-1.24,.675))
 q='WholeRearLeaderBrace'+lab;G[q]=beam((s*.66,.94,.665),(s*.405,-1.235,3.62),.10,.11,1,'One full long inclined rear brace joins the deck rear to the tall guide post. Fixed static brace only, no load certification.');join(q,'WholeLongCarrierDeck',(s*.659,.929,.68));join(q,n,(s*.407,-1.22,3.60))
# A fixed full hammer enclosure with two whole cross-carriages physically seated into both channel posts.
for k,z in enumerate([2.08,3.07]):
 n='WholeFixedHammerCrossCarriage'+str(k);box(n,(-.422,-1.31,z-.07),(.422,-1.205,z+.07),3,'One entire transverse fixed carriage roots the hammer enclosure between the two channel leaders. Display pose uses finite embedded roots; no sliding fit or movement claim.')
 for lab,s in[('Left',-1),('Right',1)]:join(n,'WholeChannelLeader'+lab,(s*.405,-1.25,z))
 join(n,'WholeLongGuidedHammerExterior',(0,-1.25,z))
G['WholeLongGuidedHammerExterior']=axial([(0,1.37),(.125,1.37),(.19,1.55),(.19,3.18),(.155,3.35),(0,3.35)],(0,-1.26,0),(1,0,0),(0,1,0),(0,0,1),24,1,'One complete long closed guided hammer-like housing is fixed between two full channel leaders, with distinct tapered ends. No internal ram, impact, pile, lifting stroke or pile-driving function.')
cyl('WholeLowerBluntHammerEnd',(0,-1.26,1.12),(0,-1.26,1.55),.105,3,'One complete blunt lower end is fixed into the hammer enclosure and stops above the empty lower guide; no tool, impact surface or working pile.',24);join('WholeLowerBluntHammerEnd','WholeLongGuidedHammerExterior',(0,-1.26,1.48))
G['WholeOpenLowerGuideCollar']=axial([(.15,.79),(.255,.79),(.255,.96),(.15,.96)],(0,-1.26,0),(1,0,0),(0,1,0),(0,0,1),32,3,'One entire thick lower guide collar has a real unobstructed vertical bore below the separated blunt hammer end. It contains no pile and implies no pile size, alignment or driving capability.')
for lab,s in[('Left',-1),('Right',1)]:
 n='WholeLowerGuideBracket'+lab;a,b=sorted([s*.22,s*.425]);box(n,(a,-1.33,.83),(b,-1.19,.93),0,'One whole short side bracket roots the lower ring to its channel post while leaving the central bore genuinely open.');join(n,'WholeChannelLeader'+lab,(s*.405,-1.25,.88));join(n,'WholeOpenLowerGuideCollar',(s*.24,-1.26,.88))
G['WholeLeaderCrownFork']=solid_union([((-.445,-1.445,4.26),(.445,-1.10,4.34)),((-.445,-1.445,4.30),(-.30,-1.10,4.66)),((.30,-1.445,4.30),(.445,-1.10,4.66))],0,'One whole open crown fork spans both guide-post tops and surrounds the complete top sheave. Fixed illustrative head, no hoisting system or working reeving.')
for lab,s in[('Left',-1),('Right',1)]:join('WholeLeaderCrownFork','WholeChannelLeader'+lab,(s*.405,-1.25,4.31))
cyl('WholeCrownCrossAxle',(-.48,-1.27,4.48),(.48,-1.27,4.48),.045,3,'One full crown axle is rooted in both cheeks with proud ends, never a coplanar overlaid cap.',20);join('WholeCrownCrossAxle','WholeLeaderCrownFork',(.37,-1.27,4.48))
G['WholeGroovedCrownSheave']=axial([(0,-.10),(.175,-.10),(.175,-.065),(.145,-.035),(.145,.035),(.175,.065),(.175,.10),(0,.10)],(0,-1.27,4.48),(0,1,0),(0,0,1),(1,0,0),28,3,'One complete thick grooved top sheave with a real recessed centre band around the rim. No bearing fit, rotation or cable performance.');join('WholeGroovedCrownSheave','WholeCrownCrossAxle',(0,-1.27,4.48))
cyl('WholeFixedFrontHoistStrand',(0,-1.42,3.23),(0,-1.42,4.48),.016,2,'One complete fixed front hoist-style strand joins the whole hammer top shoulder to the crown sheave rim. No hidden reeving or powered lifting function is claimed.',12);join('WholeFixedFrontHoistStrand','WholeLongGuidedHammerExterior',(0,-1.42,3.255));join('WholeFixedFrontHoistStrand','WholeGroovedCrownSheave',(0,-1.412,4.475))
AIR_POINTS=[(0,-1.26,.87),(0,-1.26,1.03),(0,-1.26,3.8),(-.33,-1.27,2.65),(-.57,-.43,1.40),(0,0,.20)]
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='construction-fixed-twin-channel-leader-and-hammer-crawler-rig-01';VERSION='1.0.0';TITLE='Fixed Twin Channel Leader and Hammer Crawler Rig'
DESCRIPTION='One wholly newly authored complete dedicated crawler piling-rig-style static exterior. Two full closed tracks and inset rollers support one low connected carrier and long deck, rear machinery case, low rear counterbody and empty forward side cab with real windows. The front holds two entire tall inward-facing C-channel leader posts: two independent cross-carriages physically seat one full long hammer enclosure between them, with a blunt lower end stopping above a genuinely open guide collar. A full open crown fork, transverse axle, grooved sheave and one complete fixed front strand complete the leader head, while two entire long rear braces join that leader to the deck. All visible geometry is newly drawn, not the old inclined triangular lattice-boom dragline with its bucket replaced, and not the two-stamp camshaft, bored guide beams and mortar placed on a vehicle. No old mesh imported or extracted. One prop zero scenes, four constant opaque untextured PBR roles, metres native Z up and centred whole horizontal envelope; both full track bottom facets define the display ground. Empty fixed art exterior only: no pile, engine or hammer internals, impact, pile-driving, lifting cycle, hydraulic system, travel, bearing or guide fit, soil behaviour, construction method, load, stability, manufacturing or safety claim. Rigging animation interaction not made or verified.'
PALETTE=[('WholeCarrierCabAndLeader_MutedPetrol',(.075,.28,.31,1),.65,.22),('WholeHammerBracesAndCounterbody_WarmOchre',(.65,.36,.10,1),.65,.22),('WholeTracksCarrierAndStrand_Graphite',(.035,.05,.055,1),.76,.12),('WholeRollersGuidesAndPins_SatinAlloy',(.43,.49,.48,1),.43,.62)]
FOCUS=(0,0,2.30);ORTHO=5.8
CAMERAS={'thumbnail':(-8,-12,6.3),'qa-front':(-8,-12,6.3),'qa-side':(9,0,4),'qa-top':(0,0,12),'qa-back':(8,12,6.5),'qa-wireframe':(-8,-12,6.3)}
WIRE_THICKNESS=ORTHO/1800

# BLENDER PHASE: mature export/render only.
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
root=bpy.data.objects.new('OneWholeTwinChannelLeaderAndHammerCrawlerRig',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole two track soles; horizontal bounds-centred; complete fixed twin channel leader crawler rig';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i]for p in v)for i in range(3)];hi=[max(p[i]for p in v)for i in range(3)];bounds=[round(hi[i]-lo[i],6)for i in range(3)]
assert abs(lo[2])<1e-7 and triangles==2728 and len(parts)==30
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
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'mesh_objects':mesh_count,'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,'components':component_checks,'single_prop_count':1,'review_mode':'SELF_REVIEW','static_visual_only':True,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),'status':'producer geometry; maker actual-image acceptance pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/construction/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'construction','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; maker necessary-view self-review pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
