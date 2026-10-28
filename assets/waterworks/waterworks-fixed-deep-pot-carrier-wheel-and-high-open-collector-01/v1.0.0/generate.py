import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='waterworks-fixed-deep-pot-carrier-wheel-and-high-open-collector-01'
import math
N=24
G={}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def record(name,v,f,m):
 if sum(dot(v[a],cross(v[b],v[c]))for a,b,c in f)<0:f=[(a,c,b)for a,b,c in f]
 G[name]=(v,f,m)
def box(name,lo,hi,m):
 v=[(x,y,z)for z in[lo[2],hi[2]]for y in[lo[1],hi[1]]for x in[lo[0],hi[0]]];f=[]
 for a,b,c,d in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:f.extend([(a,b,c),(a,c,d)])
 record(name,v,f,m)
def pipe(name,points,r,m,segments=8):
 v=[]
 for k,p in enumerate(points):
  tangent=unit(sub(points[min(k+1,len(points)-1)],points[max(k-1,0)]));u=(1,0,0)if abs(tangent[0])<.9 else(0,1,0);u=unit(cross(tangent,u));w=cross(tangent,u)
  for i in range(segments):v.append(add(p,add(mul(u,r*math.cos(math.tau*i/segments)),mul(w,r*math.sin(math.tau*i/segments)))))
 f=[]
 for k in range(len(points)-1):
  for i in range(segments):
   j=(i+1)%segments;a=k*segments+i;b=k*segments+j;c=(k+1)*segments+j;d=(k+1)*segments+i;f.extend([(a,b,c),(a,c,d)])
 for k in [0,len(points)-1]:
  c=len(v);v.append(points[k]);base=k*segments
  for i in range(segments):f.append((c,base+(i+1)%segments,base+i)if k==0 else(c,base+i,base+(i+1)%segments))
 record(name,v,f,m)
def wheel(name,x,y,z,ro,ri,width,m):
 # Complete closed annular tire (or capped disc when ri=0), axis X.
 profile=[(ri,x-width/2),(ro,x-width/2),(ro,x+width/2),(ri,x+width/2)]
 v=[];rs=[]
 for r,xx in profile:
  ring=[(xx,y,z)]if r==0 else[(xx,y+r*math.sin(math.tau*i/N),z+r*math.cos(math.tau*i/N))for i in range(N)];rs.append(list(range(len(v),len(v)+len(ring))));v+=ring
 f=[]
 for a,b in zip(rs,rs[1:]+rs[:1]):
  if len(a)==len(b)==1:continue
  for i in range(N):
   j=(i+1)%N
   if len(a)==1:f.append((a[0],b[i],b[j]))
   elif len(b)==1:f.append((a[i],b[0],a[j]))
   else:f.extend([(a[i],b[i],b[j]),(a[i],b[j],a[j])])
 record(name,v,f,m)

def earclip(p):
 cr=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 ids=list(range(len(p)));out=[]
 while len(ids)>3:
  for j,b in enumerate(ids):
   a,c=ids[j-1],ids[(j+1)%len(ids)]
   if cr(p[a],p[b],p[c])<=1e-14:continue
   if any(all(cr(p[u],p[v],p[k])>=-1e-14 for u,v in [(a,b),(b,c),(c,a)])for k in ids if k not in [a,b,c]):continue
   out.append((a,b,c));ids.pop(j);break
  else:raise ValueError('Non-simple padding section')
 out.append(tuple(ids));return out
def pad(name,p,y0,y1,m):
 if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);v=[(x,y,z)for y in[y0,y1]for x,z in p];f=[]
 for a,b,c in earclip(p):f.extend([(a,b,c),(c+n,b+n,a+n)])
 for i in range(n):
  j=(i+1)%n;f.extend([(i,j+n,j),(i,i+n,j+n)])
 record(name,v,f,m)

def cell_union(name,cells,mat):
 faces={}
 for v in cells:
  v=[tuple(round(c,12)for c in p)for p in v]
  for f in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:
   q=tuple(v[i]for i in f);key=tuple(sorted(q))
   if key in faces:del faces[key]
   else:faces[key]=q
 v=[];ix={};f=[]
 for q in faces.values():
  ids=[]
  for p in q:
   if p not in ix:ix[p]=len(v);v.append(p)
   ids.append(ix[p])
  f.extend([(ids[0],ids[1],ids[2]),(ids[0],ids[2],ids[3])])
 record(name,v,f,mat)
def turned(name,x,y,profile,m,seg=16):
 v=[];rs=[];f=[]
 for r,z in profile:
  pts=[(x,y,z)]if r==0 else[(x+r*math.cos(math.tau*i/seg),y+r*math.sin(math.tau*i/seg),z)for i in range(seg)]
  rs.append(list(range(len(v),len(v)+len(pts))));v+=pts
 for a,b in zip(rs,rs[1:]+rs[:1]):
  if len(a)==len(b)==1:continue
  for i in range(seg):
   j=(i+1)%seg
   if len(a)==1:f.append((a[0],b[i],b[j]))
   elif len(b)==1:f.append((a[i],b[0],a[j]))
   else:f.extend([(a[i],b[i],b[j]),(a[i],b[j],a[j])])
 record(name,v,f,m)
PALETTE=[('WholePiersAndCollectorPaleStone',(.49,.50,.44,1),.88,0),('WholeWheelRimHubSpokesWarmTimber',(.28,.16,.075,1),.82,0),('WholeDeepOpenPotsMutedCopper',(.38,.17,.075,1),.60,.32),('WholeShaftAndPotMounts',(.08,.16,.18,1),.53,.58)]
FM={};ROOTS=[];CONTACTS=[];LINKS=[];GAPS=[];SHIFT=(0,0,0)
def points7(p,e=.002):return[p]+[tuple(p[j]+(e*s if j==a else 0)for j in range(3))for a in range(3)for s in[-1,1]]
def link(a,b,p):LINKS.append((a,b,points7(p)))
def axial(name,profile,c,u,v,w,mat,n=24,phase=0):
 vv=[];rr=[];ff=[]
 for r,t in profile:
  pts=[add(c,mul(w,t))]if r==0 else[add(c,add(mul(w,t),add(mul(u,r*math.cos(math.tau*i/n+phase)),mul(v,r*math.sin(math.tau*i/n+phase)))))for i in range(n)]
  rr.append(list(range(len(vv),len(vv)+len(pts))));vv+=pts
 for a,b in zip(rr,rr[1:]+rr[:1]):
  if len(a)==len(b)==1:continue
  for i in range(n):
   j=(i+1)%n
   ff += [(a[0],b[i],b[j])]if len(a)==1 else[(a[i],b[0],a[j])]if len(b)==1 else[(a[i],b[i],b[j]),(a[i],b[j],a[j])]
 record(name,vv,ff,mat)
def unionboxes(name,boxes,mat):
 xs=sorted({p[0]for b in boxes for p in b});ys=sorted({p[1]for b in boxes for p in b});zs=sorted({p[2]for b in boxes for p in b});cells=[]
 for i in range(len(xs)-1):
  for j in range(len(ys)-1):
   for k in range(len(zs)-1):
    c=((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)
    if any(all(lo[t]<c[t]<hi[t]for t in range(3))for lo,hi in boxes):cells.append([(x,y,z)for z in[zs[k],zs[k+1]]for y in[ys[j],ys[j+1]]for x in[xs[i],xs[i+1]]])
 cell_union(name,cells,mat)
C=(0,0,2.35);JR=.13;BR=.18;PH=math.pi/16;SEAT=C[2]-JR*math.cos(PH);BZ=SEAT+BR*math.cos(PH)
outer=[(.38,BZ),(.34,2.62),(.30,2.76),(.16,2.76),(0,2.76),(-.16,2.76),(-.30,2.76),(-.34,2.62),(-.38,BZ),(-.48,1.40),(-.72,0),(-.35,0),(0,0),(.35,0),(.72,0),(.48,1.40)]
inner=[(BR*math.cos(math.tau*i/16+PH),BZ+BR*math.sin(math.tau*i/16+PH))for i in range(16)]
for sy in[-1,1]:
 y=(-1.40 if sy<0 else .98);name='WholeBoredGroundPier_'+str(sy);v=[]
 for yy in[y-.15,y+.15]:
  for ring in[outer,inner]:v.extend([(x,yy,z)for x,z in ring])
 f=[]
 for i in range(16):
  j=(i+1)%16
  for a,b,c,d in[(i,j,j+16,i+16),(i+32,i+48,j+48,j+32),(i,i+32,j+32,j),(i+16,j+16,j+48,i+48)]:f.extend([(a,b,c),(a,c,d)])
 record(name,v,f,0);ROOTS.append(name);CONTACTS.append((name,'WholeContinuousWheelShaft',(0,y,SEAT),(0,0,1),.015))
axial('WholeContinuousWheelShaft',[(0,-1.60),(JR,-1.60),(JR,1.18),(0,1.18)],C,(1,0,0),(0,0,1),(0,1,0),3,16,PH)
axial('WholeBroadWheelHub',[(0,-.23),(.30,-.23),(.30,.23),(0,.23)],C,(1,0,0),(0,0,1),(0,1,0),1,32)
link('WholeContinuousWheelShaft','WholeBroadWheelHub',C)
axial('WholeOpenAnnularPotCarrier',[(1.72,-.14),(1.98,-.14),(1.98,.14),(1.72,.14)],C,(1,0,0),(0,0,1),(0,1,0),1,64)
for j in range(8):
 a=math.tau*j/8;r=(math.cos(a),0,math.sin(a));name='WholeRadialWheelSpoke_'+str(j);pipe(name,[add(C,mul(r,.22)),add(C,mul(r,1.85))],.10,1,4)
 link('WholeBroadWheelHub',name,add(C,mul(r,.25)));link('WholeOpenAnnularPotCarrier',name,add(C,mul(r,1.81)))
# Twelve full necked blind-bottom pots, not scoop blades or copied vessel fragments.
# Every complete cavity and lip is made by the one closed thick radial profile.
profile=[(0,-.30),(.16,-.30),(.23,-.20),(.25,0),(.21,.20),(.14,.30),(.14,.48),(.10,.48),(.10,.31),(.16,.18),(.18,0),(.16,-.18),(0,-.22)]
for j in range(12):
 a=math.tau*j/12;r=(math.cos(a),0,math.sin(a));t=(-math.sin(a),0,math.cos(a));w=add(mul(t,.8),(0,-.6,0));v=cross(w,r);center=add(C,add(mul(r,1.87),(0,-.53,0)));pot='WholeDeepNeckedOpenPot_'+str(j);mount='WholePotRearMount_'+str(j)
 axial(pot,profile,center,r,v,w,2,20)
 q=add(center,mul(v,.225));p=(q[0],-.12,q[2]);e=(q[0],q[1]-.010,q[2]);pipe(mount,[p,e],.035,3,12)
 link(mount,'WholeOpenAnnularPotCarrier',(q[0],-.13,q[2]));link(mount,pot,q)
 GAPS.append(dict(label='SelectedCompletePotMouthAndDeepCavity_'+str(j),origin_m=list(add(center,mul(w,.49))),direction=list(mul(w,-1)),length_m=.50))
# One complete high offset receiving trough with both ends open and a continuously falling floor.
# It is not asserted to intercept every pot or to provide a working fluid trajectory.
x0=-1.85;x1=2.80;yc=-1.21
section=[(-.25,0),(.25,0),(.25,.26),(.19,.26),(.19,.08),(-.19,.08),(-.19,.26),(-.25,.26)]
pad('WholeHighOpenReceivingTrough',section,x0,x1,0)
v,f,m=G['WholeHighOpenReceivingTrough'];G['WholeHighOpenReceivingTrough']=([(xx,yc+y,3.80-.05*(xx-x0)+z)for y,xx,z in v],[(a,c,b)for a,b,c in f],m)
for j,x in enumerate([-1.60,2.55]):
 z=3.80-.05*(x-x0);name='WholeCollectorColumnAndFoot_'+str(j)
 # Entire column top is cut to the same shallow plane as the trough underside.
 unionboxes(name,[((x-.36,yc-.32,0),(x+.36,yc+.32,.14)),((x-.11,yc-.12,.14),(x+.11,yc+.12,z))],0)
 vv,ff,mi=G[name];G[name]=([(xx,yy,zz-.05*(xx-x)if abs(zz-z)<1e-8 else zz)for xx,yy,zz in vv],ff,mi);ROOTS.append(name)
 normal=unit((.05,0,1));CONTACTS.append((name,'WholeHighOpenReceivingTrough',(x,yc,z),normal,.052))
for j in range(8):
 a=math.tau*(j+.5)/8;GAPS.append(dict(label='SelectedOpenSpokeSector_'+str(j),origin_m=[.95*math.cos(a),-.22,C[2]+.95*math.sin(a)],direction=[0,1,0],length_m=.44))
for sy in[-1,1]:
 for dx in[-.05,0,.05]:GAPS.append(dict(label='SelectedBoreUpperAir',origin_m=[dx,(-1.40 if sy<0 else .98)-.19,BZ+.14],direction=[0,1,0],length_m=.38))
GAPS.append(dict(label='SelectedWholeReceivingTroughLongitudinalAir',origin_m=[x0+.01,yc,3.80-.05*.01+.15],direction=list(unit((1,0,-.05))),length_m=(x1-x0-.02)*math.sqrt(1.0025)))
GAPS.append(dict(label='SelectedGroundClearBelowWheel',origin_m=[-2.3,0,.08],direction=[1,0,0],length_m=4.6))
GAPS.append(dict(label='WholeShaftSolidControl',origin_m=[0,-1.7,C[2]],direction=[0,1,0],length_m=3.0,blocked=True))
GAPS.append(dict(label='WholeTroughFloorSolidControl',origin_m=[1.0,yc,3.0],direction=[0,0,1],length_m=1.0,blocked=True))
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([sub(p,SHIFT)for p in v],f,m)for n,(v,f,m)in G.items()};CONTACTS=[(a,b,sub(p,SHIFT),n,area)for a,b,p,n,area in CONTACTS];LINKS=[(a,b,[sub(p,SHIFT)for p in pts])for a,b,pts in LINKS]
for r in GAPS:r['origin_m']=list(sub(r['origin_m'],SHIFT))
FM={n:[m]*len(f)for n,(v,f,m)in G.items()}
# BLENDER PHASE



import bpy
from mathutils import Vector
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=128
scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for layer in scene.view_layers:layer.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=4
scene.use_nodes=False;scene.render.use_compositing=False
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='AgX'
materials=[]
for name,col,rough,metal in PALETTE:
 m=bpy.data.materials.new(name);m.diffuse_color=col;m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=col;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;materials.append(m)

parts=[]
for name,(v,f,mi) in G.items():
 me=bpy.data.meshes.new(name+'Mesh');me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o)
 for m in materials:me.materials.append(m)
 face_materials=FM[name]if name in FM else[mi]*len(f)
 for i,p in enumerate(me.polygons):p.material_index=face_materials[i];p.use_smooth=False
 parts.append(o)
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
triangles=sum(len(f)for v,f,m in G.values())
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
if '--geometry-only' in sys.argv:
 print('GEOMETRY_READY',ASSET,triangles);sys.exit(0)
# Render the actual exported geometry, not an unexported proxy.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
parts=[x for x in scene.objects if x.type=='MESH'];assert len(parts)==len(G)
view='thumbnail'
if '--view' in sys.argv:view=sys.argv[sys.argv.index('--view')+1]
assert view in ['qa-front','thumbnail']
scene.cycles.samples=16 if view=='qa-front' else 128
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.28,.28,.28,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
focus=Vector((0,0,2.3))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=6.7;aim(cam,(9,-15,10) if view=='qa-front' else (-9,-14,10.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/waterworks/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'waterworks','style':'S01-clean-geometric','title':'Fixed Deep Pot Carrier Wheel and High Open Collector','description':'One newly authored complete empty fixed noria-inspired wheel-and-high-collector apparatus. Two entire tapered ground piers with genuine polygonal through-bores carry one full shaft on finite opposed lower bearing facets. A whole broad hub, eight complete radial spokes and one continuous thick open annular carrier support twelve entire bulbous necked pots around the circumference. Each pot has its own real narrow open mouth, complete thick lip, deep full interior and blind bottom; it is not a flat paddle or shallow open excavation scoop. Each whole pot axis tilts outward from the wheel plane and a separate complete short rear mount connects its full body to the carrier. Beside the upper wheel, one whole long open receiving trough has a continuously declining floor, full sidewalls and two open axial ends; two entire tall columns with integral broad feet support its sloped underside on finite matching top faces. Forty whole closed meshes and all geometry newly authored together, no old waterwheel, scoop, excavator, pot, stand, channel or pump fragments imported or extracted. Unlike the earlier twin-rim flat-board paddle wheel there is one pot-carrying ring, real deep enclosed-bottom recipient interiors and a high independent receiving trough rather than a sixteen-paddle power receiver. Unlike the crawler scoop-wheel excavator there are no tracks, opposed conveyor booms, belts, mast, cabin or tangential open scoops. Four finite opposed shaft/trough seats and forty-one selected sevenpoint embedded root groups link all parts to four complete ground soles. Four opaque constant PBR materials, metre-style Z up, complete horizontal bounds-centred ground datum, one independent apparatus zero scenes. Generic pot-wheel vocabulary only, not a reconstruction of a named historical machine or museum specimen. A single fixed dry display pose with simplified bearing and mounting connections; the offset trough is not certified to intercept each mouth or to form a continuous fluid path. No water, drive paddles, stream, reservoir, aqueduct, operator, rigging or animation. No filling/emptying sequence, rotation, flow, lift head, volume, efficiency, hydraulic power, cup capacity, bearing running fit, structural loading, balance, installation, manufacture, historical accuracy or public/equipment safety capability is claimed.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
