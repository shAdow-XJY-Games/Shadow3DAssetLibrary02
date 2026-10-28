import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='waterworks-fixed-planar-spiral-tube-and-open-spoked-pump-wheel-01'
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
PALETTE=[('WholeSpiralTubeWarmCopper',(.64,.30,.12,1),.63,.25),('WholeOpenRimAndFourSpokesTeal',(.07,.25,.27,1),.72,.24),('WholeBoredHubAndBearingDarkSteel',(.15,.18,.19,1),.54,.54),('WholeIntegralGroundedStandWarmGrey',(.48,.49,.44,1),.84,.08)]
G={};FM={};LINKS=[];CONTACTS=[];ROOTS=['WholeIntegralFootAndTaperedStand'];GAPS=[];ZC=1.8
# One complete stand, broad foot transitions into the narrower unbroken upright.
name=ROOTS[0];top=ZC-.31*math.cos(math.pi/32);v=[];f=[]
for z,wx,wy in[(0,.80,1.4),(.16,.80,1.4),(.28,.32,.44),(top,.32,.44)]:
 v +=[(.90+sx*wx/2,sy*wy/2,z)for sx,sy in[(-1,-1),(1,-1),(1,1),(-1,1)]]
f.extend([(0,2,1),(0,3,2),(12,13,14),(12,14,15)])
for k in range(3):
 for j in range(4):a=4*k+j;b=4*k+(j+1)%4;c=b+4;d=a+4;f.extend([(a,b,c),(a,c,d)])
record(name,v,f,3)
def ring(name,x0,x1,ri,ro,m,n=32):
 phase=math.pi/n;v=[]
 for x,r in[(x0,ri),(x0,ro),(x1,ro),(x1,ri)]:
  v +=[(x,r*math.sin(phase+math.tau*i/n),ZC+r*math.cos(phase+math.tau*i/n))for i in range(n)]
 f=[]
 for k in range(4):
  kk=(k+1)%4
  for i in range(n):j=(i+1)%n;a=k*n+i;b=k*n+j;c=kk*n+j;d=kk*n+i;f.extend([(a,b,c),(a,c,d)])
 record(name,v,f,m)
ring('WholeOpenOuterWheelRim',-.06,.15,1.43,1.53,1,64)
ring('WholeBoredWheelHub',.38,.62,.12,.42,2)
ring('WholeAnnularSupportBearing',.74,1.06,.13,.31,2)
CONTACTS.append((ROOTS[0],'WholeAnnularSupportBearing',(.90,0,top),.019))
def witness(a,b,p,e=.002):
 pts=[p]+[tuple(p[k]+(sg*e if k==ax else 0)for k in range(3))for ax in range(3)for sg in[-1,1]];LINKS.append((a,b,pts))
for k in range(4):
 a=math.tau*k/4;name='WholeDeepRadialSpoke_'+str(k);v=[(x,r*math.cos(a)-t*math.sin(a),ZC+r*math.sin(a)+t*math.cos(a))for x in[-.04,.58]for r,t in[(.34,-.055),(1.48,-.055),(1.48,.055),(.34,.055)]];f=[]
 for q in[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:f.extend([(q[0],q[1],q[2]),(q[0],q[2],q[3])])
 record(name,v,f,1)
 witness(name,'WholeBoredWheelHub',(.50,.38*math.cos(a),ZC+.38*math.sin(a)))
 witness(name,'WholeOpenOuterWheelRim',(.04,1.465*math.cos(a),ZC+1.465*math.sin(a)))
# One annular-ended continuous tube: open outer tangential inlet, three planar
# spiral turns, smooth inward three-dimensional elbow, then straight axial outlet.
spiral=[]
for i in range(145):
 t=i/144;a=math.pi/2+math.tau*3*t;r=.30+1.10*t;spiral.append((-.10,r*math.cos(a),ZC+r*math.sin(a)))
end=spiral[-1];tan=unit(sub(spiral[-1],spiral[-2]));PATH=[add(end,mul(tan,.22)),add(end,mul(tan,.11))]+list(reversed(spiral))
p0=spiral[0];p1=add(p0,(0,.18,-.035));p2=(.40,0,ZC);p3=(.60,0,ZC)
for i in range(1,21):
 t=i/20;PATH.append(tuple((1-t)**3*p0[k]+3*(1-t)**2*t*p1[k]+3*(1-t)*t*t*p2[k]+t**3*p3[k]for k in range(3)))
PATH +=[(x,0,ZC)for x in[.72,.90,1.08,1.25,1.40]]
RO=[.075 if p[0]<=.28 else .075+.065*min(1,(p[0]-.28)/.27)for p in PATH];RO[0]=.11;RO[1]=.085
RI=[.050 for p in PATH];RI[0]=.082;RI[1]=.060
v=[];f=[];frames=[];u=(1,0,0);ns=12
for k,p in enumerate(PATH):
 tangent=unit(sub(PATH[min(k+1,len(PATH)-1)],PATH[max(k-1,0)]));u=unit(sub(u,mul(tangent,dot(u,tangent))));w=cross(tangent,u);frames.append((u,w,tangent))
 for r in[RO[k],RI[k]]:
  for j in range(ns):v.append(add(p,add(mul(u,r*math.cos(math.tau*j/ns)),mul(w,r*math.sin(math.tau*j/ns)))))
for k in range(len(PATH)-1):
 for side in[0,1]:
  for j in range(ns):jj=(j+1)%ns;a=k*2*ns+side*ns+j;b=k*2*ns+side*ns+jj;c=(k+1)*2*ns+side*ns+jj;d=(k+1)*2*ns+side*ns+j;faces=[(a,b,c),(a,c,d)];f +=faces if side==0 else[tuple(reversed(q))for q in faces]
for k in[0,len(PATH)-1]:
 for j in range(ns):jj=(j+1)%ns;a=k*2*ns+j;b=k*2*ns+jj;c=k*2*ns+ns+jj;d=k*2*ns+ns+j;ff=[(a,d,c),(a,c,b)];f+=ff if k==0 else[tuple(reversed(q))for q in ff]
record('WholeContinuousHollowPlanarSpiralTube',v,f,0)
for k in range(4):
 a=math.tau*k/4;i=next(i for i,p in enumerate(spiral)if i>=48 and abs(p[1]*math.sin(a)-(p[2]-ZC)*math.cos(a))<1e-7 and p[1]*math.cos(a)+(p[2]-ZC)*math.sin(a)>.3)
 p=spiral[i];witness('WholeContinuousHollowPlanarSpiralTube','WholeDeepRadialSpoke_'+str(k),(-.032,p[1],p[2]),.0015)
witness('WholeContinuousHollowPlanarSpiralTube','WholeBoredWheelHub',(.57,.13,ZC),.002)
witness('WholeContinuousHollowPlanarSpiralTube','WholeAnnularSupportBearing',(.90,.132,ZC),.001)
# Selected between-turn windows in the actual front-to-back throat.
for k in range(4):
 a=math.pi/4+math.tau*k/4
 phase=(a-math.pi/2)%math.tau;rfirst=.30+1.10*phase/(math.tau*3)
 for r in[rfirst+1.10/3*.5,rfirst+1.10/3*1.5]:GAPS.append(dict(label='SelectedBetweenTurnAndSpokeWindow',origin_m=[-.45,r*math.cos(a),ZC+r*math.sin(a)],direction=[1,0,0],length_m=1.10))
GAPS.append(dict(label='AxialOutletBore',origin_m=[.62,0,ZC],direction=[1,0,0],length_m=.9))
GAPS.append(dict(label='AxialOutletWallControl',origin_m=[.62,.10,ZC],direction=[1,0,0],length_m=.9,blocked=True))
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,0)
G={n:([sub(p,SHIFT)for p in v],f,m)for n,(v,f,m)in G.items()};FM={n:[m]*len(f)for n,(v,f,m)in G.items()}
CONTACTS=[(a,b,sub(p,SHIFT),area)for a,b,p,area in CONTACTS];LINKS=[(a,b,[sub(p,SHIFT)for p in pts])for a,b,pts in LINKS];PATH=[sub(p,SHIFT)for p in PATH]
for g in GAPS:g['origin_m']=sub(g['origin_m'],SHIFT)
assert max(len(n.encode())for n in G)<=63
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
focus=Vector((0,0,1.66))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=4.35;aim(cam,(-12,-8,6) if view=='qa-front' else (-14,-7,5.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/waterworks/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'waterworks','style':'S01-clean-geometric','title':'Fixed Planar Spiral Tube and Open Spoked Pump Wheel','description':'One newly authored complete static dry spiral-pump-inspired inspection model. One continuous thick hollow tube runs from a visibly flared open outer tangential inlet through three fully separated planar Archimedean spiral turns, curves inward as one smooth three-dimensional elbow, and ends in a thick straight hollow axial outlet. Both tube ends have real open lumens and finite annular rims; the entire material tube is a single closed editable mesh, not a rope or paired flat guide strips. A complete open outer wheel rim and four complete deep radial spokes carry the coiled tube and connect to a separate whole through-bored hub. The enlarged straight outlet wall is rooted into that hub and one whole annular bearing on a single integral tapered upright and broad flat foot, forming one fixed cantilevered inspection pose. All nine complete meshes are independently newly authored, no reel, waterwheel, disc pump or support mesh imported or extracted. Four opaque constant PBR roles, metre-style Z up, horizontal bounds-centred ground datum, one independent model zero scenes. The prior developing reel has paired solid spiral guide ribbons inside a tank rather than this single continuous hollow delivery tube. The prior paddle wheel has twin timber rims and water-receiving paddle boards, absent here. The prior disc pump has an endless cord and separate small pistons running through an open vertical riser, absent here. Only selected whole-lumen centreline segments, between-turn windows and static material-root witnesses are checked; they are not a full volumetric fluid or collision simulation. No water, paddle drive, rotary seal, supply circuit, operating installation, actual pumping, hydraulic head, flow rate, load or cantilever capacity, rotating/bearing function, seal, pressure integrity, manufacture, assembly, maintenance or public/machinery safety capability made or verified. Original artistic topology and proportions, not a replica or installation drawing. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
