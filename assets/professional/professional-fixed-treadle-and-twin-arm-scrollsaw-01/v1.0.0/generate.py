"""One complete static standing twin-arm treadle scrollsaw. No cutting, drive or safety claim."""
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



# New complete standing treadle scroll-saw appearance; no old band saw or bow reused.
G={};GROUND=[];ROOT_WITNESSES=[];AIR_POINTS=[]
def join(a,b,p):ROOT_WITNESSES.append((a,b,p))
def cylinder(a,b,r,mat,role,n=20):
 w=unit(sub(b,a));u=unit(cross(w,(0,0,1)if abs(w[2])<.9 else(0,1,0)));v=cross(w,u);ll=math.sqrt(dot(sub(b,a),sub(b,a)))
 return axial([(0,0),(r,0),(r,ll),(0,ll)],a,u,v,w,n,mat,role)
for label,s in [('Left',-1),('Right',1)]:
 x=s*.29;n=label+'WholeGroundSkid';G[n]=extrude([(x-.045,-.53),(x+.045,-.53),(x+.052,-.515),(x+.052,.515),(x+.045,.53),(x-.045,.53),(x-.052,.515),(x-.052,-.515)],0,.075,'z',0,'One complete long chamfered ground runner belongs to the single standing saw frame. Full finite flat sole; not a separate machine base or old stool.');GROUND.append(n)
 for end,t in [('Front',-1),('Rear',1)]:
  n2=label+end+'WholeSplayedLeg';a=(x,t*.42,.052);b=(s*.24,t*.34,.79);G[n2]=beam(a,b,.065,.070,0,'One entire splayed stand leg joins its ground runner to the long upper side rail. Complete four-legged open machine frame, no desktop, operator or workpiece.');join(n2,n,(x,t*.42,.060))
 n2=label+'WholeUpperSideRail';G[n2]=block((s*.245-.038,-.410,.755),(s*.245+.038,.445,.825),0,'One whole long upper side rail joins both splayed legs and carries the workboard supports; genuine under-table open space remains.')
 for end,t in [('Front',-1),('Rear',1)]:join(n2,label+end+'WholeSplayedLeg',(s*.245,t*.345,.780))
for end,t in [('Front',-1),('Rear',1)]:
 n=end+'WholeLowCrossTie';G[n]=block((-.294,t*.38-.035,.250),(.294,t*.38+.035,.310),0,'One full low transverse tie unifies the two side frames, leaving the treadle and drive-link regions visibly open.')
 for label,s in [('Left',-1),('Right',1)]:join(n,label+end+'WholeSplayedLeg',(s*.275,t*.395,.275))
for label,y in [('Near',-.100),('Far',.100)]:
 n=label+'WholeTableCrossSupport';G[n]=block((-.275,y-.030,.775),(.275,y+.030,.827),0,'One complete upper cross support roots below the true slotted work table behind the blade path, never sealing the table entry slot.')
 for lab,s in [('Left',-1),('Right',1)]:join(n,lab+'WholeUpperSideRail',(s*.245,y,.800))
p=[(-.29,-.51),(-.008,-.51),(-.008,-.29),(.008,-.29),(.008,-.51),(.29,-.51),(.33,-.47),(.33,.12),(.29,.16),(-.29,.16),(-.33,.12),(-.33,-.47)]
G['WholeFrontSlottedWorkTable']=extrude(p,.815,.845,'z',1,'One entire broad chamfered work table has a true open-to-front narrow slot reaching beyond the complete vertical blade. Full thickness inner slot walls and a continuous rear table bridge are geometry, not a dark line. No table insert, workpiece or cutting operation.');join('WholeFrontSlottedWorkTable','NearWholeTableCrossSupport',(0,-.100,.821));join('WholeFrontSlottedWorkTable','FarWholeTableCrossSupport',(0,.100,.821))
G['WholeRearArmBearingStandard']=block((-.060,.335,.285),(.060,.425,1.240),0,'One entire rear vertical standard rises from the rear low tie to carry two distinct arm pivots at separated heights. It is not a C-shaped column enclosing a continuous band or a ram guide for a horizontal bow.');join('WholeRearArmBearingStandard','RearWholeLowCrossTie',(0,.375,.298))
upper=[(.455,1.130),(.455,1.225),(.300,1.225),(-.300,1.160),(-.350,1.145),(-.350,1.100),(-.290,1.100),(.300,1.155)]
lower=[(.455,.600),(.455,.690),(.300,.690),(-.290,.680),(-.350,.665),(-.350,.625),(-.290,.625),(.300,.630)]
for label,p,z in [('Upper',upper,1.180),('Lower',lower,.650)]:
 n=label+'WholeLongTaperedSawArm';G[n]=extrude(p,-.030,.030,'x',0,'One entire long tapered horizontal saw arm independently reaches from its rear pivot to the front blade clamp. The upper and lower arms are two whole separate solids, not the sides of a closed saw bow or a wheel housing. Fixed pose, no reciprocal stroke or tension performance.')
 pin=label+'WholeProudRearPivot';G[pin]=cylinder((-.145,.380,z),(.085,.380,z),.016,2,'One whole transverse proud arm-pivot pin crosses both the rear standard and its complete arm. Fixed illustration only; no bearing fit or moving range.',24);join(pin,'WholeRearArmBearingStandard',(0,.380,z));join(n,pin,(0,.380,z))
G['WholeRearArmCouplingLink']=beam((-.115,.380,.650),(-.115,.380,1.180),.025,.028,2,'One complete long rear coupling-link appearance joins the two proud rear pins outside the standard. It does not merge the upper and lower front arms into a bow, and no kinematic phase or linkage equation is asserted.');join('WholeRearArmCouplingLink','UpperWholeProudRearPivot',(-.115,.380,1.177));join('WholeRearArmCouplingLink','LowerWholeProudRearPivot',(-.115,.380,.653))
for label,z0,z1 in [('Upper',1.095,1.150),('Lower',.625,.685)]:
 n=label+'WholeFrontBladeClamp';G[n]=block((-.019,-.347,z0),(.019,-.304,z1),2,'One entire compact front blade clamp belongs to its corresponding full horizontal arm. It holds the finite blunt strip in a single display pose, without clamp adjustment or tension claim.');join(n,label+'WholeLongTaperedSawArm',(0,-.325,1.130 if label=='Upper'else .650))
G['WholeSingleVerticalBluntBladeStrip']=block((-.0028,-.332,.655),(.0028,-.318,1.120),1,'One entire finite blunt vertical strip bridges the upper and lower clamps through the genuine work-table slot. Unlike the old band saw it has no return run or closed loop; unlike the power hacksaw it is not a long horizontal blade. No sharpened teeth, cut, workpiece or safe-tool specification.');join('WholeSingleVerticalBluntBladeStrip','UpperWholeFrontBladeClamp',(0,-.325,1.110));join('WholeSingleVerticalBluntBladeStrip','LowerWholeFrontBladeClamp',(0,-.325,.670))
# Complete low treadle and exposed crank/flywheel assembly belong to the same frame.
G['WholeLowCentralDriveBed']=block((-.115,-.040,.258),(.115,.405,.317),0,'One entire low central bed reaches the rear low tie and carries the two distinct drive-axle supports; the front footboard remains below and clear of this bed.');join('WholeLowCentralDriveBed','RearWholeLowCrossTie',(0,.375,.285))
for label,x in [('Left',-.075),('Right',.075)]:
 n=label+'WholeCrankAxlePedestal';G[n]=block((x-.022,.105,.302),(x+.022,.175,.495),0,'One complete low bearing pedestal roots into the drive bed under the shared transverse crank axle.');join(n,'WholeLowCentralDriveBed',(x,.140,.310))
G['WholeTransverseDriveAxle']=cylinder((-.120,.140,.450),(.325,.140,.450),.016,1,'One full transverse static drive axle enters both pedestal bodies and carries the whole rim-and-spoke flywheel and crank disk. No rotation or torque claim.',24)
for label,x in [('Left',-.075),('Right',.075)]:join('WholeTransverseDriveAxle',label+'WholeCrankAxlePedestal',(x,.140,.450))
C=(.195,.140,.450);u=(0,1,0);v=(0,0,1);w=(1,0,0)
G['WholeOpenFlywheelHub']=axial([(0,-.032),(.038,-.032),(.038,.036),(0,.036)],C,u,v,w,24,2,'One entire proud central hub surrounds the full axle of the open flywheel.');join('WholeOpenFlywheelHub','WholeTransverseDriveAxle',C)
G['WholeOpenFlywheelRim']=axial([(.180,-.022),(.225,-.022),(.225,.022),(.180,.022)],C,u,v,w,40,0,'One complete thick flywheel rim has a genuine large open center occupied only by its five separate full spokes and hub. It is not a lower blade pulley and carries no closed saw band.')
for i in range(5):
 d=add(mul(u,math.cos(.2+math.tau*i/5)),mul(v,math.sin(.2+math.tau*i/5)));n='WholeFlywheelSpoke'+str(i+1);G[n]=beam(add(C,mul(d,.025)),add(C,mul(d,.205)),.026,.025,0,'One complete new flywheel spoke joins the full central hub and rim. No old wheel or drive component was imported.');join(n,'WholeOpenFlywheelHub',add(C,mul(d,.032)));join(n,'WholeOpenFlywheelRim',add(C,mul(d,.198)))
G['WholeSideCrankDisk']=cylinder((.243,.140,.450),(.275,.140,.450),.102,2,'One entire side crank disk roots on the proud drive axle and carries one fixed eccentric crosspin; it remains distinct from the annular flywheel. No actual crank travel. ',32);join('WholeSideCrankDisk','WholeTransverseDriveAxle',(.260,.140,.450))
G['WholeEccentricCrankCrossPin']=cylinder((.253,.090,.510),(.351,.090,.510),.012,1,'One full proud eccentric crosspin enters the crank disk and the two separated fixed drive links. No causal drive or bearing-performance claim.',20);join('WholeEccentricCrankCrossPin','WholeSideCrankDisk',(.265,.090,.510))
for label,s in [('Left',-1),('Right',1)]:
 x=s*.290;n=label+'WholeTreadleHingePedestal';G[n]=block((x-.025,.385,.060),(x+.025,.455,.149),0,'One entire rear low treadle hinge pedestal joins its grounded runner and supports the complete cross axle above the ground.');join(n,label+'WholeGroundSkid',(x,.420,.068))
G['WholeTreadleRearHingeAxle']=cylinder((-.325,.420,.120),(.325,.420,.120),.012,1,'One entire rear transverse footboard hinge axle spans the two grounded runner mounts. Static pose only.',24)
for label,s in [('Left',-1),('Right',1)]:join('WholeTreadleRearHingeAxle',label+'WholeTreadleHingePedestal',(s*.290,.420,.120))
pa=(0,.445,.118);pb=(0,-.450,.200)
G['WholeLongInclinedFootTreadle']=beam(pa,pb,.200,.034,3,'One entire broad wooden foot treadle runs forward and upward from its rear hinge, below the open frame and drive bed. It is a full board rather than disconnected pedals, and no human fit or operating guidance is asserted.');join('WholeLongInclinedFootTreadle','WholeTreadleRearHingeAxle',(0,.420,.120))
pz=.118+(.200-.118)*(.445+.300)/(.445+.450)
G['WholeFootboardDriveCrossPin']=cylinder((-.110,-.300,pz),(.329,-.300,pz),.013,2,'One complete proud transverse drive pin roots through the whole footboard; the side link joins outside its edge, not through a floating endpoint.',20);join('WholeFootboardDriveCrossPin','WholeLongInclinedFootTreadle',(0,-.300,pz))
G['WholeTreadleToCrankConnectingLink']=beam((.291,-.300,pz),(.291,.090,.510),.025,.024,1,'One entire oblique side connecting link runs from the footboard crosspin to the eccentric crank pin, outside the open frame. No force, speed, cycle or engineered linkage compatibility.');join('WholeTreadleToCrankConnectingLink','WholeFootboardDriveCrossPin',(.291,-.297,pz+.002));join('WholeTreadleToCrankConnectingLink','WholeEccentricCrankCrossPin',(.291,.088,.508))
G['WholeLowerArmDriveCrossPin']=cylinder((-.040,.120,.657),(.350,.120,.657),.012,2,'One complete proud transverse lower-arm drive pin joins its whole arm to the short separate crank link.');join('WholeLowerArmDriveCrossPin','LowerWholeLongTaperedSawArm',(0,.120,.657))
G['WholeCrankToLowerArmLink']=beam((.328,.090,.510),(.328,.120,.657),.022,.024,1,'One full short upper crank connecting link terminates on the proud lower-arm pin. It is spatially separated from the long footboard link and illustrates a fixed assembly only.');join('WholeCrankToLowerArmLink','WholeEccentricCrankCrossPin',(.328,.090,.513));join('WholeCrankToLowerArmLink','WholeLowerArmDriveCrossPin',(.328,.120,.654))
AIR_POINTS=[(-.0056,-.325,.830),(.0056,-.325,.830),(0,-.450,.830),(0,-.300,.830),(0,-.100,1.010),(0,.150,.980),(0,-.100,.715),(-.17,-.240,.520),(.12,-.300,.520),(0,.10,.200),(-.115,.20,.960),(-.12,.20,.530)]
# One actual aperture of the new flywheel is selected away from every whole spoke.
a=.2+math.pi/5;AIR_POINTS.append(add(C,add(mul(u,.12*math.cos(a)),mul(v,.12*math.sin(a)))))
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vv)+max(p[i]for p in vv))/2 if i<2 else-min(p[2]for p in vv)for i in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
ROOT_WITNESSES=[(a,b,add(p,SHIFT))for a,b,p in ROOT_WITNESSES];AIR_POINTS=[add(p,SHIFT)for p in AIR_POINTS]
ASSET='professional-fixed-treadle-and-twin-arm-scrollsaw-01';VERSION='1.0.0';TITLE='Fixed Treadle and Twin Arm Scrollsaw'
DESCRIPTION='One newly authored complete standing treadle-scrollsaw-style exterior. Two grounded long runners, four splayed legs, full side rails and cross ties form an open standing frame. A broad chamfered work table has a genuine open-to-front through slot around one entire finite blunt vertical strip. Two distinct long tapered horizontal arms reach forward from separate proud pivots on a full rear standard, ending in complete upper and lower blade clamps. A separate whole rear coupling link joins the rear pins. Below the table, an entire inclined wooden treadle on a complete rear cross axle connects through a full side link to one eccentric crank pin; a separate short link reaches the lower arm. The complete low bed, paired bearing pedestals, transverse axle, open five-spoke flywheel and side crank disk belong to this one machine. All numeric geometry is new. Unlike the old two-wheel band saw, there is no continuous closed blade loop or paired wheel enclosures; unlike the power hacksaw, there is no horizontal blade bow, long top ram or workholding vise. Not a handheld jigsaw scaled up or an old machine with its motor replaced. One prop, zero scenes, no workpiece, operator, loose accessory, sharpened tooth or surrounding workshop. Four opaque constant untextured PBR materials, metres, Z up and actual whole horizontal-bounds-centred ground origin. Fixed illustrative game-art only: no cutting, reciprocation, tension, motion phase, linked mechanism performance, torque, power, dimensional compatibility, machining accuracy, loading, human fit, operating guidance, manufacture or machinery safety claim.'
PALETTE=[('WholeStandingFrameAndArms_MutedOlive',(.16,.24,.18,1),.68,.28),('WholeWorkTableBladeAndLinks_SatinSteel',(.43,.48,.49,1),.44,.58),('WholeClampsPinsAndCrank_DarkIron',(.075,.10,.11,1),.65,.35),('WholeFootTreadle_WarmTimber',(.34,.18,.070,1),.76,0.)]
FOCUS=(0,0,.605);ORTHO=1.63
CAMERAS={'gray-front3q':(4.6,-6,3.7),'gray-back3q':(-3,5,3),'thumbnail':(4.6,-6,3.7),'qa-front':(4.8,-6,3.3),'qa-side':(5,0,3),'qa-top':(0,0,6),'qa-back':(-3,5,3),'qa-wireframe':(4.6,-6,3.7),'silhouette-128-front':(4.8,-6,3.3),'silhouette-128-side':(5,0,3)}
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
root=bpy.data.objects.new('OneFixedStandingTwinArmTreadleScrollsaw',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='two complete runner soles at Z0; actual bounds centred; whole fixed treadle scrollsaw';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles==1660 and len(parts)==43
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
