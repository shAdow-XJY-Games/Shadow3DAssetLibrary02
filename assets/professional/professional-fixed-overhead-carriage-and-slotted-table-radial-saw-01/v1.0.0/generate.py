"""One whole fixed overhead-carriage radial saw table exterior. Static art only, no working saw motion or cutting performance."""
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
# New complete radial overhead-carriage saw table exterior. No old model geometry.
G={};GROUND=[];ROOT_WITNESSES=[];AIR_POINTS=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
for sx in[-1,1]:
 for sy in[-1,1]:
  x=sx*.52;y=sy*.36;n='WholeGroundShoe'+str(sx)+'_'+str(sy);leg='WholeSplayedTableLeg'+str(sx)+'_'+str(sy)
  G[n]=block((x-.055,y-.050,0),(x+.055,y+.050,.055),2,'One whole finite ground shoe, part of the complete freestanding machine.');GROUND.append(n)
  G[leg]=beam((x,y,.045),(sx*.46,sy*.30,.755),.065,.065,0,'One whole slightly splayed leg supporting the full worktable, not an imported separate table model.');join(n,leg,(x,y,.050));join(leg,'WholeFrontSlottedTabletop',(sx*.46,sy*.30,.748))
G['WholeFrontSlottedTabletop']=solid_union([((-.60,-.48,.74),(.11,.40,.80)),((.15,-.48,.74),(.60,.40,.80)),((.11,.26,.74),(.15,.40,.80))],3,'One complete thick broad wood-like work surface with an actual narrow front-open through slot beneath the suspended blunt disk. No workpiece, feed or cutting setup.')
for lab,x in [('Left',-.46),('Right',.46)]:
 n='Whole'+lab+'SideApron';G[n]=block((x-.035,-.33,.68),(x+.035,.33,.749),0,'One full long under-table side apron.');join(n,'WholeFrontSlottedTabletop',(x,0,.745))
 n='Whole'+lab+'LowerStretcher';G[n]=beam((x,-.325,.27),(x,.325,.27),.045,.045,0,'One entire lower side stretcher with ends seated into the complete splayed legs.');join(n,'WholeSplayedTableLeg'+str(-1 if x<0 else 1)+'_-1',(-.476 if x<0 else .476,-.318,.27));join(n,'WholeSplayedTableLeg'+str(-1 if x<0 else 1)+'_1',(-.476 if x<0 else .476,.318,.27))
for lab,y in [('Front',-.32),('Rear',.32)]:
 n='Whole'+lab+'LongApron';G[n]=block((-.48,y-.030,.682),(.48,y+.030,.746),0,'One complete long upper apron of the integrated machine table.');join(n,'WholeFrontSlottedTabletop',(0,y,.744))
G['WholeRearColumnFoot']=block((-.14,.19,.686),(.14,.40,.835),0,'One complete rear rectangular column-foot casting rooted in the rear apron and table.');join('WholeRearColumnFoot','WholeRearLongApron',(0,.32,.710));join('WholeRearColumnFoot','WholeFrontSlottedTabletop',(0,.32,.770))
G['WholeSteppedRearUpright']=axial([(0,.800),(.098,.800),(.098,.850),(.071,.885),(.071,1.48),(.086,1.48),(.086,1.52),(0,1.52)],(0,.31,0),(1,0,0),(0,1,0),(0,0,1),24,1,'One entire stepped high rear upright. It is fixed to the integrated table base, not a rotating or telescoping robot sleeve.');join('WholeSteppedRearUpright','WholeRearColumnFoot',(0,.31,.819))
G['WholeRearArmColumnHead']=block((-.100,.235,1.305),(.100,.390,1.463),0,'One full upper head casting grips the rear upright and the complete fixed overhead rail.');join('WholeRearArmColumnHead','WholeSteppedRearUpright',(0,.31,1.36))
G['WholeOverheadForeAftArm']=block((-.055,-.440,1.330),(.055,.370,1.430),0,'One full overhead fore-aft arm above the entire tabletop. A separate carriage surrounds this fixed rail; the beam does not slide through the column like the older radial work robot.');join('WholeOverheadForeAftArm','WholeRearArmColumnHead',(0,.28,1.37))
G['WholeArmFrontStop']=block((-.080,-.460,1.315),(.080,-.430,1.450),2,'One whole proud front stop at the overhead rail end.');join('WholeArmFrontStop','WholeOverheadForeAftArm',(0,-.435,1.37))
# Complete rectangular wraparound carriage, with genuine passage and side/bottom space.
outer=[(-.095,1.285),(.095,1.285),(.095,1.475),(-.095,1.475)];inner=[(-.066,1.317),(.066,1.317),(.066,1.428),(-.066,1.428)];m=Mesh()
for y in[-.140,.040]:
 for i in range(4):j=(i+1)%4;m.quad((outer[i][0],y,outer[i][1]),(outer[j][0],y,outer[j][1]),(inner[j][0],y,inner[j][1]),(inner[i][0],y,inner[i][1]),1)
for p in[outer,inner]:
 for i in range(4):j=(i+1)%4;m.quad((p[i][0],-.140,p[i][1]),(p[j][0],-.140,p[j][1]),(p[j][0],.040,p[j][1]),(p[i][0],.040,p[i][1]),1)
G['WholeThroughPassageHeadCarriage']=m.result('One entire thick wraparound suspended-head carriage. Its inner ceiling has a small deliberate fixed engagement with the overhead rail; side and bottom passage gaps are real. This is not a moving-fit or travel demonstration.');join('WholeThroughPassageHeadCarriage','WholeOverheadForeAftArm',(0,-.060,1.429))
G['WholeDownturnedMotorYoke']=solid_union([((-.090,-.125,1.058),(-.040,.015,1.320)),((-.090,-.125,1.285),(.080,.015,1.320))],0,'One continuous downturned yoke descends from the overhead carriage to the horizontally oriented motor head.');join('WholeDownturnedMotorYoke','WholeThroughPassageHeadCarriage',(-.065,-.065,1.300))
G['WholeHorizontalMotorBody']=axial([(0,-.235),(.060,-.235),(.075,-.218),(.075,.065),(.055,.085),(0,.085)],(0,-.060,1.035),(0,1,0),(0,0,1),(1,0,0),24,0,'One complete broad horizontal motor-style body under the carriage, without internal mechanism.');join('WholeHorizontalMotorBody','WholeDownturnedMotorYoke',(-.065,-.060,1.080))
G['WholeRearMotorEndCap']=axial([(0,-.255),(.050,-.255),(.063,-.239),(.063,-.220),(0,-.220)],(0,-.060,1.035),(0,1,0),(0,0,1),(1,0,0),24,2,'One entire dark rear motor end cap, slightly overlapping the case shoulder.');join('WholeRearMotorEndCap','WholeHorizontalMotorBody',(-.228,-.060,1.035))
cyl('WholeSawHeadCrossSpindle',(.060,-.060,1.035),(.177,-.060,1.035),.020,1,'One full fixed transverse spindle connecting the head and blunt disk.',24);join('WholeSawHeadCrossSpindle','WholeHorizontalMotorBody',(.075,-.060,1.035))
G['WholeBluntSuspendedCircularDisk']=axial([(.018,.124),(.245,.124),(.250,.127),(.250,.133),(.245,.136),(.018,.136)],(0,-.060,1.035),(0,1,0),(0,0,1),(1,0,0),48,1,'One complete thick annular toothless disk, with its lower arc in the real narrow tabletop slot. No blade teeth, sharp cutting edge, material contact or cutting function.')
join('WholeBluntSuspendedCircularDisk','WholeSawHeadCrossSpindle',(.130,-.041,1.035))
def head_arc(name,x0,x1,ri,ro,t0,t1,mat,role):
 m=Mesh();N=32;aa=[math.radians(t0+(t1-t0)*i/N)for i in range(N+1)];pt=lambda x,r,t:(x,-.060+r*math.cos(t),1.035+r*math.sin(t))
 for i in range(N):
  a,b=aa[i:i+2]
  for x in[x0,x1]:m.quad(pt(x,ri,a),pt(x,ro,a),pt(x,ro,b),pt(x,ri,b),mat)
  for r in[ri,ro]:m.quad(pt(x0,r,a),pt(x1,r,a),pt(x1,r,b),pt(x0,r,b),mat)
 for a in[aa[0],aa[-1]]:m.quad(pt(x0,ri,a),pt(x1,ri,a),pt(x1,ro,a),pt(x0,ro,a),mat)
 G[name]=m.result(role)
head_arc('WholeUpperDiskGuardBackWeb',.105,.115,.015,.265,-12,192,0,'One full thick upper guard back web, with a real open lower half and central seated root. It is not an opaque full disk covering the blade.');join('WholeUpperDiskGuardBackWeb','WholeSawHeadCrossSpindle',(.110,-.043,1.035))
head_arc('WholeCurvedUpperGuardRim',.110,.162,.255,.280,-10,190,0,'One complete curved upper guard rim, with positive internal separation from the disk. End planes are inset from the separate web ends.');join('WholeCurvedUpperGuardRim','WholeUpperDiskGuardBackWeb',(.113,-.060,1.295))
G['WholeSpindleProudBlankCap']=axial([(0,.132),(.032,.132),(.032,.165),(.026,.174),(0,.174)],(0,-.060,1.035),(0,1,0),(0,0,1),(1,0,0),24,2,'One whole blank spindle cap, with a proud face clear of the disk face.');join('WholeSpindleProudBlankCap','WholeSawHeadCrossSpindle',(.155,-.060,1.035));join('WholeSpindleProudBlankCap','WholeBluntSuspendedCircularDisk',(.134,-.036,1.035))
G['WholeForwardPullHandleStem']=beam((-.150,-.110,1.080),(-.150,-.365,1.125),.025,.025,1,'One full forward handle stem seated in the suspended motor body, not attached to the stationary table.');join('WholeForwardPullHandleStem','WholeHorizontalMotorBody',(-.150,-.115,1.080))
G['WholeTransversePullGrip']=axial([(0,-.235),(.024,-.235),(.028,-.223),(.028,-.077),(.024,-.065),(0,-.065)],(0,-.365,1.125),(0,1,0),(0,0,1),(1,0,0),20,2,'One full transverse dark pull grip on the hanging head. No travel, human fit or operating demonstration.');join('WholeTransversePullGrip','WholeForwardPullHandleStem',(-.150,-.360,1.124))
for lab,lo,hi in [('Left',-.570,.105),('Right',.155,.570)]:
 n='Whole'+lab+'SplitRearFence';G[n]=block((lo,.230,.795),(hi,.265,.880),3,'One complete thick rear-fence half, fixed to the table and separated from the genuine blade slot. The two halves are subordinate parts of this one machine.');join(n,'WholeFrontSlottedTabletop',((lo+hi)/2,.247,.798))
G['WholeBlankColumnControl']=block((-.123,.250,1.335),(-.094,.305,1.399),2,'One full blank side-control exterior rooted in the head casting. No switch wiring or electrical function.');join('WholeBlankColumnControl','WholeRearArmColumnHead',(-.098,.275,1.365))
AIR_POINTS=[(.130,-.420,.770),(.130,.150,.770),(.061,-.06,1.365),(0,-.06,1.323),(.14,-.06,1.287),(.13,-.35,1.020),(0,-.05,.50),(.30,0,1.0),(-.30,0,1.10)]
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='professional-fixed-overhead-carriage-and-slotted-table-radial-saw-01';VERSION='1.0.0';TITLE='Fixed Overhead Carriage and Slotted Table Radial Saw'
DESCRIPTION='One newly authored complete freestanding radial-arm-saw-style machine exterior. Four whole splayed legs and finite shoes, full aprons and lower stretchers support one broad thick wood-like tabletop with a genuine front-open narrow slot. A complete high rear column and fixed overhead fore-aft arm carry a separate truly through-bored wraparound carriage, continuous downturned yoke and full transverse motor-style body. One suspended thick toothless disk has its lower arc inside the tabletop slot, with a separate complete open-bottom upper guard web and curved rim, spindle and proud cap. A whole forward stem and transverse grip belong to the hanging head, while two complete split-fence halves remain on the table. All geometry is newly authored; no old radial robot, hand circular saw, table or power hacksaw components are imported. The entire table-plus-overhead-carriage-and-hanging-disk relation is the difference, not a swapped blade or changed size. Four opaque constant PBR roles, one complete prop and zero scenes. Metres, native Z up, full horizontal bounds-centred ground origin. Empty static occupational appearance only: no sharp teeth, cutting setup, blade rotation, carriage or column travel, moving guard, working drive, motor wiring, workholding, load, stability, human fit, manufacture or machinery-safety assurance. Rigging, animation and interaction are not made and outside this static delivery.'
PALETTE=[('WholeCastFrame_MutedPetrol',(.09,.25,.26,1),.67,.30),('WholeRailAndDisc_SatinMetal',(.48,.54,.55,1),.43,.68),('WholeFeetAndGrip_Charcoal',(.042,.053,.057,1),.78,.05),('WholeTableAndFence_WarmWood',(.43,.29,.15,1),.76,.0)]
FOCUS=(0,0,.76);ORTHO=2.15
CAMERAS={'gray-front3q':(4,-6,3.5),'gray-back3q':(-4,6,3.5),'thumbnail':(4,-6,3.5),'qa-front':(4,-6,3.5),'qa-side':(6,0,3),'qa-top':(0,0,6),'qa-back':(4,6,3.5),'qa-wireframe':(4,-6,3.5),'silhouette-128-front':(4,-6,3.5),'silhouette-128-side':(6,0,3)}
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
root=bpy.data.objects.new('OneWholeFixedOverheadCarriageRadialSawTable',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='four complete finite table shoes at datum; whole bounds centred; static suspended-carriage saw table';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==2488 and len(parts)==34
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
  files[role]={'path':f'assets/professional/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'professional','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
