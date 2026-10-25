"""One newly authored complete forewell hull and inclined bucket-ladder dredger. Dry static exterior only."""
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
# One entire newly authored fork-bow work hull and inclined bucket-ladder vessel. Dry static exterior only.
ROOT_WITNESSES=[];AIR_POINTS=[];GROUND=['WholeJoinedForewellWorkHull']
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
hull=[(-1.12,-2.60),(-.58,-2.60),(-.58,-.08),(.58,-.08),(.58,-2.60),(1.12,-2.60),(1.43,-2.22),(1.43,2.05),(1.17,2.43),(-1.17,2.43),(-1.43,2.05),(-1.43,-2.22)]
G['WholeJoinedForewellWorkHull']=extrude(hull,0,.64,'z',0,'One complete newly drawn closed flat-bottom work hull with a joined full aft body and two forward bow arms around a genuine long front-open ladder well. Chamfered outer bow and stern corners are part of the one hull; not two old pontoons under an old machine. Whole finite dry-display sole, no water or flotation claim.')
g=G['WholeJoinedForewellWorkHull']
for j,f in enumerate(g['faces']):
 if all(g['vertices'][i][2]==.64 for i in f):g['face_materials'][j]=2
LOW=(0,-3.15,.55);HIGH=(0,.18,1.95);T=unit(sub(HIGH,LOW));N=(0,-T[2],T[1]);D=math.sqrt(dot(sub(HIGH,LOW),sub(HIGH,LOW)))
def pos(x,t,n):return add(LOW,add((x,0,0),add(mul(T,t),mul(N,n))))
for side,x in [('Left',-.76),('Right',.76)]:
 for fore,y in [('Fore',-.37),('Aft',.95)]:
  name=side+fore+'WholeUpperAxleSupport';base=(x*1.33,y,.60);top=(x,.18,1.95)
  G[name]=beam(base,top,.14,.14,2,'One whole sloping steel bearing support, from the complete hull side deck to the upper bucket-ladder axle. It belongs to this dry fixed vessel, not a freestanding irrigation timber tower.')
  join(name,'WholeJoinedForewellWorkHull',add(base,mul(sub(top,base),.015)))
for name,p in [('Lower',LOW),('Upper',HIGH)]:
 axle='Whole'+name+'LadderAxle';drum='Whole'+name+'LadderDrum'
 cyl(axle,add(p,(-.90,0,0)),add(p,(.90,0,0)),.056,3,'One complete transverse ladder drum axle, held in the continuous side ladder rails; upper axle is carried by the vessel bearing supports.',24)
 G[drum]=axial([(.055,-.32),(.305,-.32),(.305,.32),(.055,.32)],p,T,N,(1,0,0),32,1,'One full thick bored ladder drum crossing the paired continuous route bands. Fixed exterior only; no sprocket engagement, power or chain articulation.')
 join(drum,axle,add(p,mul(T,.0555)))
 if name=='Upper':
  for side,x in [('Left',-.76),('Right',.76)]:
   for fore in['Fore','Aft']:join(axle,side+fore+'WholeUpperAxleSupport',(x,.18,1.92))
for side,x in [('Left',-.46),('Right',.46)]:
 name=side+'WholeInclinedLadderRail';G[name]=beam(add(LOW,(x,0,0)),add(HIGH,(x,0,0)),.12,.12,2,'One entire inclined ladder side rail connecting both full drum axles from the low forward rake to the high inboard pivot. Its diagonal route passes through the genuine forewell, not a tilted copy of the old vertical lift.')
 join(name,'WholeLowerLadderAxle',pos(x,.035,0));join(name,'WholeUpperLadderAxle',pos(x,D-.035,0))
def capsule(r):
 return [(D+r*math.sin(j*math.pi/24),r*math.cos(j*math.pi/24))for j in range(25)]+[(r*math.sin(math.pi+j*math.pi/24),r*math.cos(math.pi+j*math.pi/24))for j in range(25)]
for side,x in [('Left',-.28),('Right',.28)]:
 m=Mesh();inside=capsule(.298);outside=capsule(.328)
 for j in range(len(inside)):
  k=(j+1)%len(inside)
  for xx in[x-.025,x+.025]:m.quad(pos(xx,*inside[j]),pos(xx,*inside[k]),pos(xx,*outside[k]),pos(xx,*outside[j]),1)
  m.quad(pos(x-.025,*inside[j]),pos(x-.025,*inside[k]),pos(x+.025,*inside[k]),pos(x+.025,*inside[j]),1)
  m.quad(pos(x-.025,*outside[j]),pos(x-.025,*outside[k]),pos(x+.025,*outside[k]),pos(x+.025,*outside[j]),1)
 name=side+'WholeContinuousLadderRoute';G[name]=m.result('One complete finite-thickness closed oblique capsule route band around both drums, supporting the complete scoop row. Stylized continuous route rather than actual articulated chain links or claimed engagement.')
 join(name,'WholeUpperLadderDrum',pos(x,D,.301));join(name,'WholeLowerLadderDrum',pos(x,0,.301))
def scoop(t,sign):
 # One whole thick blind-bottom box scoop, mouth along the selected tangent. All surfaces explicit, genuine inner cavity.
 m=Mesh();rows=[]
 for dt,w,n0,n1 in[(-.12,.36,.300,.540),(.12,.36,.300,.540),(.12,.322,.329,.507),(-.083,.322,.329,.507)]:
  rows.append([pos(x,t+sign*dt,sign*n)for x,n in[(-w,n0),(w,n0),(w,n1),(-w,n1)]])
 for a,b in zip(rows,rows[1:]):
  for j in range(4):k=(j+1)%4;m.quad(a[j],a[k],b[k],b[j],3)
 m.quad(*rows[0],3);m.quad(*rows[-1],3)
 return m.result('One complete thick open scoop attached to the paired oblique route bands, with a genuine blind bottom, full walls and finite open mouth. Empty static shape, no scraping edge, pickup or discharge guarantee.')
for sign,label in[(1,'ForwardRise'),(-1,'RearReturn')]:
 for j,t in enumerate([.55,1.30,2.05,2.80]):
  name=label+'WholeEmptyScoop'+str(j);G[name]=scoop(t,sign)
  join(name,'LeftWholeContinuousLadderRoute',pos(-.28,t-sign*.10,sign*.315))
# Entire aft station, with integral opaque face-material window region rather than decals or floating glass.
cabboxes=[((.35,.82,.60),(1.19,1.88,1.56)),((.48,.90,.96),(1.06,1.8,1.40))]
G['WholeAftClosedControlHouse']=solid_union(cabboxes,0,'One full compact closed aft control-house exterior attached to the common hull deck. The blank dark upper front material region is opaque static styling, not a transparent cabin or validated interior.')
g=G['WholeAftClosedControlHouse']
for j,f in enumerate(g['faces']):
 vv=[g['vertices'][i]for i in f]
 if all(abs(v[1]-.82)<1e-9 for v in vv) and all(.48-1e-9<=v[0]<=1.06+1e-9 and .96-1e-9<=v[2]<=1.40+1e-9 for v in vv):g['face_materials'][j]=1
join('WholeAftClosedControlHouse','WholeJoinedForewellWorkHull',(.80,1.3,.62))
G['WholeAftDriveHousing']=extrude([(-1.18,.60),(-.40,.60),(-.40,1.02),(-.53,1.16),(-1.05,1.16),(-1.18,1.02)],.72,1.66,'y',2,'One complete chamfered aft drive-housing exterior on the opposite side of the deck. No engine internals, wiring, exhaust, transmission or power performance is supplied.')
join('WholeAftDriveHousing','WholeJoinedForewellWorkHull',(-.75,1.2,.62))
# Full open discharge trough across the rear deck, visibly part of the vessel rather than an extracted bucket accessory.
trough=[(-.30,0),(.30,0),(.30,.22),(.25,.22),(.25,.045),(-.25,.045),(-.25,.22),(-.30,.22)]
G['WholeAftOpenDischargeTrough']=extrude(trough,.47,1.85,'y',3,'One whole open-ended thick U-section trough carried above the rear deck, away from the upper drum. Empty static outlet appearance; not a connected liquid/material flow simulation.')
g=G['WholeAftOpenDischargeTrough'];g['vertices']=[(x,y,z+1.66-.16*(y-.47))for x,y,z in g['vertices']]
for j,y in enumerate([.65,1.60]):
 name='WholeDischargeTroughStand'+str(j);G[name]=solid_union([((-.33,y-.055,.60),(-.26,y+.055,1.73-.16*(y-.47))),((.26,y-.055,.60),(.33,y+.055,1.73-.16*(y-.47))),((-.33,y-.055,1.64-.16*(y-.47)),(.33,y+.055,1.70-.16*(y-.47)))],2,'One full portal stand under the complete aft outlet trough, rooted to the full hull deck; not load-rated structure.')
 join(name,'WholeJoinedForewellWorkHull',(-.295,y,.62));join(name,'WholeAftOpenDischargeTrough',(0,y,1.68-.16*(y-.47)))
AIR_POINTS=[(0,-1.5,.25),pos(0,D/2,0),(.80,.50,1.20),(0,1.20,1.82-.16*(1.20-.47))]
vv=[v for g in G.values()for v in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='marine-fixed-forewell-hull-and-inclined-bucket-ladder-dredger-01';VERSION='1.0.0';TITLE='Fixed Forewell Hull and Inclined Bucket Ladder Dredger'
DESCRIPTION='One newly authored complete dry-display chain-bucket dredger vessel exterior. One joined flat-bottom work hull has two chamfered forward bow arms around a genuine long front-open ladder well and a connected aft deck. A complete oblique twin-rail ladder descends through that well beyond the bow, with two full transverse drum axles, whole thick bored drums, paired continuous closed route bands and eight entire thick open empty scoops in fixed tangent-facing poses. Four whole inclined deck bearing supports carry the upper axle. A compact closed aft station, separate plain drive housing and elevated whole open U-section rear discharge trough on two full portal stands belong to the same vessel. All hull outlines, ladder, drums, scoop walls and layout coordinates are newly authored, not the old vertical irrigation chain lift placed on old pontoons, not a walkway with equipment substituted, and no component extraction. Four opaque constant PBR materials, metres, native Z up, complete horizontal bounds centred over the finite hull sole. One prop and zero scenes; no water, operator, stock, rigging, animation or interaction. Static artistic exterior only: no buoyancy, flotation, sailing, stability, dredging, scraping, chain articulation, sprocket engagement, motion, lifting, material flow, discharge, power, hydraulic design, structural load, access, manufacture, operation or safety capability is modeled or verified.'
PALETTE=[('WholeForewellHullAndHouse_MutedNavy',(.075,.19,.23,1),.72,.28),('WholeRouteAndDrums_DarkSteel',(.08,.10,.11,1),.48,.65),('WholeDeckAndLadder_GreyGreen',(.25,.32,.30,1),.76,.20),('WholeScoopsAndAxles_MutedOchre',(.47,.32,.10,1),.58,.32)]
FOCUS=(0,0,1.05);ORTHO=7.15
CAMERAS={'thumbnail':(7.5,-10,6.4),'qa-front':(7.5,-10,6.4),'qa-side':(10,0,4),'qa-top':(0,0,12),'qa-back':(-7,10,6),'qa-wireframe':(7.5,-10,6.4)}
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
root=bpy.data.objects.new('OneWholeForewellBucketLadderDredger',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole finite hull sole at datum; horizontally centred; one complete static bucket-ladder vessel';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==2120 and len(parts)==26
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
  files[role]={'path':f'assets/marine/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'marine','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
