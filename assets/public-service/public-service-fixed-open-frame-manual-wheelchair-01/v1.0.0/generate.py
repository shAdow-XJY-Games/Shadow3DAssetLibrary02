"""Original complete fixed open-frame manual wheelchair appearance. Static art only; no medical, mobility or safety claim."""
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
# Newly authored complete fixed open-frame manual wheelchair appearance.
def unit(v):return mul(v,1/math.sqrt(dot(v,v)))
def rod(a,b,r,mat,role,n=12):
 w=unit(sub(b,a));ref=(0,0,1)if abs(w[2])<.9 else(0,1,0);u=unit(cross(w,ref));v=cross(w,u);return axial([(0,0),(r,0),(r,math.dist(a,b)),(0,math.dist(a,b))],a,u,v,w,n,mat,role)
def bent_side(points,x,r,mat,role,n=12):
 rows=[];m=Mesh()
 for i,(y,z)in enumerate(points):
  a=points[max(0,i-1)];b=points[min(len(points)-1,i+1)];dy=b[0]-a[0];dz=b[1]-a[1];ln=math.hypot(dy,dz);normal=(0,-dz/ln,dy/ln)
  rows.append([add((x,y,z),add((r*math.cos(math.tau*j/n),0,0),mul(normal,r*math.sin(math.tau*j/n))))for j in range(n)])
 for a,b in zip(rows,rows[1:]):
  for j in range(n):k=(j+1)%n;m.quad(a[j],a[k],b[k],b[j],mat)
 for row in[rows[0],rows[-1]]:
  c=tuple(sum(p[k]for p in row)/n for k in range(3))
  for j in range(n):m.tri([c,row[j],row[(j+1)%n]],mat)
 return m.result(role)
G={};GROUND=[];ROOT_WITNESSES=[];AIR_POINTS=[]
# Continuous side tubes integrate rear push posts, full seat rails and forward descending leg rests.
for side,sgn in[('L',-1),('R',1)]:
 x=sgn*.26;frame='WholeBentSeatBackLegFrame'+side;lower='WholeLowerSideRail'+side;rear='WholeRearAxleUpright'+side
 path=[(.40,.95),(.27,.95),(.22,.91),(.22,.51),(.18,.485),(-.24,.485),(-.29,.44),(-.32,.30),(-.38,.18),(-.48,.16)]
 G[frame]=bent_side(path,x,.018,0,'One whole new continuous bent side tube includes rear push handle/post, horizontal seat support and descending front leg-rest support; not a chair body on a cart.')
 G[lower]=rod((x,.22,.28),(x,-.32,.28),.018,0,'One complete low longitudinal side member forms the open lower chassis.')
 G[rear]=rod((x,.16,.28),(x,.16,.49),.023,0,'One full rear axle upright joins lower chassis, main transverse axle and the seat rail.')
 ROOT_WITNESSES +=[(lower,rear,(x,.16,.285)),(rear,frame,(x,.16,.485)),(lower,frame,(x,-.315,.287)),(rear,'WholeRearThroughAxle',(x,.16,.31))]
 grip='WholeRearPushGrip'+side;G[grip]=rod((x,.30,.95),(x,.425,.95),.026,2,'One complete short rear push grip with a continuous fixed root over its own side-frame handle.')
 ROOT_WITNESSES.append((grip,frame,(x,.35,.95)))
 for lab,y in[('Front',-.19),('Back',.16)]:
  post='WholeArmPost'+side+lab;G[post]=rod((x,y,.485),(x,y,.69),.013,0,'One complete arm support post from the side seat rail into its full arm pad.');ROOT_WITNESSES +=[(post,frame,(x,y,.49)),(post,'WholeArmPad'+side,(x,y,.685))]
 pad='WholeArmPad'+side;G[pad]=block((x-.038,-.235,.68),(x+.038,.20,.715),2,'One whole thin arm pad, not an enclosed upholstered recliner side. Open space below remains visible.')
 foot='WholeForwardFootPlate'+side;x0,x1=sorted([sgn*.035,sgn*.28]);G[foot]=block((x0,-.62,.145),(x1,-.40,.175),2,'One complete forward foot plate with a real central separation from the other plate; fixed only, no hinge travel or user fit claim.')
 ROOT_WITNESSES.append((foot,frame,(x,-.46,.164)))
 # One large spoked rear wheel plus a separate outboard push rim.
 xx=sgn*.345;cy=.16;cz=.31;ro=.31/math.cos(math.pi/32);tire='WholeRearAnnularTire'+side;rim='WholeRearMetalRim'+side;hub='WholeRearWheelHub'+side;hand='WholeSeparateHandrim'+side
 G[tire]=axial([(.282,xx-.027), (ro,xx-.027),(ro,xx+.027),(.282,xx+.027)],(0,cy,cz),(0,1,0),(0,0,1),(1,0,0),32,2,'One whole annular rear tire with a finite flat ground facet and genuine open spoke region.',phase=math.pi/32);GROUND.append(tire)
 G[rim]=axial([(.265,xx-.013),(.290,xx-.013),(.290,xx+.013),(.265,xx+.013)],(0,cy,cz),(0,1,0),(0,0,1),(1,0,0),32,1,'One whole narrow metal rim seated into its tire, no wheel geometry imported.',phase=math.pi/32)
 ROOT_WITNESSES.append((tire,rim,(xx,cy,cz+.285)))
 G[hub]=rod((xx-.032,cy,cz),(xx+.032,cy,cz),.034,1,'Whole rear wheel hub connected to its individual spokes and the common rear axle.');ROOT_WITNESSES.append((hub,'WholeRearThroughAxle',(xx,cy,cz)))
 hx=sgn*.404;G[hand]=axial([(.245,hx-.010),(.260,hx-.010),(.260,hx+.010),(.245,hx+.010)],(0,cy,cz),(0,1,0),(0,0,1),(1,0,0),32,1,'One complete separate outboard hand-propulsion rim with actual separation from the tire and four fixed spacing mounts; not another tire.',phase=math.pi/32)
 for k in range(8):
  a=math.pi/8+k*math.pi/4;dy=math.cos(a);dz=math.sin(a);n='WholeRearSpoke'+side+str(k);G[n]=rod((xx,cy,cz),(xx,cy+.280*dy,cz+.280*dz),.006,1,'One whole new radial rear wheel spoke with finite roots in hub and rim.',8);ROOT_WITNESSES +=[(n,hub,(xx,cy+.02*dy,cz+.02*dz)),(n,rim,(xx,cy+.275*dy,cz+.275*dz))]
 for k in range(4):
  a=math.pi/4+k*math.pi/2;dy=math.cos(a);dz=math.sin(a);n='WholeHandrimStandOff'+side+str(k);G[n]=rod((xx,cy+.274*dy,cz+.274*dz),(hx,cy+.253*dy,cz+.253*dz),.007,1,'One entire short outboard rim spacer; four fixed mounts leave an open handrim-to-wheel gap.',8);ROOT_WITNESSES +=[(n,rim,(xx+.001*sgn,cy+.2735*dy,cz+.2735*dz)),(n,hand,(hx-.001*sgn,cy+.2535*dy,cz+.2535*dz))]
 # Two small front caster appearances, distinct from rear drive wheels, on full open forks.
 fx=sgn*.26;fy=-.34;fz=.075;cw='WholeSmallFrontCasterTire'+side;ch='WholeFrontCasterHub'+side;ca='WholeFrontCasterAxle'+side;fork='WholeFrontCasterFork'+side;stem='WholeFrontCasterStem'+side
 G[cw]=axial([(.026,fx-.020),(.075/math.cos(math.pi/16),fx-.020),(.075/math.cos(math.pi/16),fx+.020),(.026,fx+.020)],(0,fy,fz),(0,1,0),(0,0,1),(1,0,0),16,2,'One complete small front tire with a true central opening and finite ground facet, held in a fixed caster fork.',phase=math.pi/16);GROUND.append(cw)
 G[ch]=rod((fx-.023,fy,fz),(fx+.023,fy,fz),.033,1,'One full small caster hub inside its tire.');G[ca]=rod((fx-.057,fy,fz),(fx+.057,fy,fz),.012,1,'One entire short caster axle spanning both fork cheeks.');ROOT_WITNESSES +=[(cw,ch,(fx,fy,fz+.03)),(ch,ca,(fx,fy,fz))]
 poly=[(fx-.055,.06),(fx-.035,.06),(fx-.035,.175),(fx+.035,.175),(fx+.035,.06),(fx+.055,.06),(fx+.055,.205),(fx-.055,.205)];G[fork]=extrude(poly,fy-.025,fy+.025,'y',0,'One whole continuous inverted-U caster fork with a true open space around the small front wheel, not four copied trolley casters.')
 ROOT_WITNESSES +=[(fork,ca,(fx-.045,fy,fz)),(fork,ca,(fx+.045,fy,fz))]
 G[stem]=rod((fx,fy,.19),(fx,-.32,.29),.017,0,'One whole slightly offset fixed caster stem joins the fork top and front lower chassis; no actual swivel or trail geometry claim.')
 ROOT_WITNESSES +=[(stem,fork,(fx,fy+.001,.195)),(stem,lower,(fx,-.315,.282))]
 AIR_POINTS +=[(hx,cy+.15,cz),(x,-.05,.60),(x,-.52,.25)]
G['WholeRearThroughAxle']=rod((-.39,.16,.31),(.39,.16,.31),.014,1,'One whole rear transverse fixed axle below the seat joins both rear wheel hubs and the two chassis uprights.')
# Thin full seat and back panels, each new solid geometry, not reused chair cushions.
G['WholeSeatSling']=extrude([(-.24,.475),(.19,.475),(.225,.49),(-.24,.505)],-.265,.265,'x',3,'One complete thin fixed seat panel, with full underside and edge walls, carried by both long side rails. No cloth motion or loaded sag is claimed.')
G['WholeBackSling']=block((-.265,.202,.53),(.265,.235,.90),3,'One complete thin upright back panel rooted into both rear side posts; no recliner cushion or medical posture claim.')
for sgn in[-1,1]:
 side='L'if sgn<0 else'R';ROOT_WITNESSES +=[('WholeSeatSling','WholeBentSeatBackLegFrame'+side,(sgn*.255,-.10,.49)),('WholeBackSling','WholeBentSeatBackLegFrame'+side,(sgn*.255,.218,.70))]
for k,(a,b)in enumerate([((-.26,-.02,.285),(.26,-.02,.475)),((.26,.02,.285),(-.26,.02,.475))]):
 name='WholeUnderseatCrossBrace'+str(k);G[name]=rod(a,b,.012,0,'One complete diagonal under-seat brace in a fixed crossed pair, not a demonstrated folding mechanism.');left='L'if a[0]<0 else'R';right='R'if b[0]>0 else'L';ROOT_WITNESSES +=[(name,'WholeLowerSideRail'+left,(a[0]*.98,a[1],a[2]+.002)),(name,'WholeBentSeatBackLegFrame'+right,(b[0]*.98,b[1],b[2]-.002))]
G['WholeCrossBraceCentrePin']=rod((0,-.04,.38),(0,.04,.38),.015,1,'One entire short fixed central joining pin between the two offset crossing brace bars.')
for k,y in[(0,-.02),(1,.02)]:ROOT_WITNESSES.append(('WholeCrossBraceCentrePin','WholeUnderseatCrossBrace'+str(k),(0,y,.38)))
AIR_POINTS +=[(0,-.05,.65),(0,-.52,.20),(0,-.10,.20),(0,.35,.70)]
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='public-service-fixed-open-frame-manual-wheelchair-01';VERSION='1.0.0';TITLE='Fixed Open-Frame Manual Wheelchair Appearance'
DESCRIPTION='One newly authored whole fixed manual-wheelchair appearance under the public-service equipment direction. Two large open-spoked rear wheels have separate outboard hand rims with real gaps and individual spacing mounts; two much smaller front wheels sit in complete open caster forks. Full bent side frames integrate the rear push handles, seat rails and descending forward leg supports, with lower chassis rails, rear axle uprights and a fixed crossed under-seat brace pair. Complete thin seat/back panels, two independent open-underarm pads and two separated forward foot plates finish the one seated mobility silhouette. This is not an upholstered recliner placed on a trolley, a bicycle with a chair payload or wheel-count variation of a storage cart; no old model vertices are imported. Four opaque constant PBR materials, metres, Z up and true horizontal-bounds-centred ground origin. One static prop, zero scenes or separate wheel/seat assets. All joints are a fixed illustrative pose with small intentional embedded connections. No rolling, steering, braking, folding, propulsion, user dimensions, posture, disability fit, medical or rehabilitation suitability, transport performance, accessibility compliance, load, stability, manufacture or safety claim; not an operable or certified mobility-device design.'
PALETTE=[('WholeMetalFrame_MutedTeal',(.13,.28,.27,1),.57,.42),('RimsSpokesAndAxles_SatinAlloy',(.42,.48,.47,1),.42,.67),('TiresPadsAndGrips_Charcoal',(.055,.065,.065,1),.85,0.),('CompleteSeatBackPanels_DeepBlue',(.065,.115,.16,1),.87,0.)]
FOCUS=(0,0,.49);ORTHO=1.55
CAMERAS={'gray-front3q':(4,-6,3.0),'gray-back3q':(-4,6,3.0),'thumbnail':(4,-6,3.0),'qa-front':(4,-6,2.6),'qa-side':(5,0,2.7),'qa-top':(0,0,6),'qa-back':(-3.8,6,2.8),'qa-wireframe':(4,-6,3.0),'silhouette-128-front':(4,-6,2.6),'silhouette-128-side':(5,0,2.7)}
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
root=bpy.data.objects.new('OneFixedOpenFrameManualWheelchair',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='four finite wheel facets at Z0; actual bounds centred; whole fixed manual wheelchair appearance';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==4224 and len(parts)==64
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
  files[role]={'path':f'assets/public-service/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'public-service','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
