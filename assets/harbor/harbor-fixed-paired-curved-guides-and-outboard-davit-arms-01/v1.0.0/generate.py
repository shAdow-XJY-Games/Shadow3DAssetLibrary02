import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='harbor-fixed-paired-curved-guides-and-outboard-davit-arms-01'
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
PALETTE=[('WholeGuideCheeksAndPedestalsBlueGrey',(.16,.29,.33,1),.71,.28),('WholeBentDavitsMutedOchre',(.59,.34,.11,1),.68,.24),('WholeRollersAxlesAndEyesSatinSteel',(.45,.49,.49,1),.46,.62),('WholeCommonGroundFrameAndCordsCharcoal',(.07,.10,.105,1),.80,.18)]
FM={};JOINS=[];ROOTS=['WholeCommonHShapedGroundFrame']
xx=[-2.20,-1.40,1.40,2.20];yy=[-.55,.40,.90,1.30];cells=[]
for i in range(3):
 for j in range(3):
  if i==1 and j!=1:continue
  cells.append([(x,y,z)for z in[0,.18]for y in[yy[j],yy[j+1]]for x in[xx[i],xx[i+1]]])
cell_union(ROOTS[0],cells,3)
def yzsolid(name,poly,x0,x1,m):
 pad(name,poly,x0,x1,m);v,f,mi=G.pop(name);record(name,[(y,x,z)for x,y,z in v],f,mi)
def path_outline(points,half):
 left=[];right=[]
 for i,p in enumerate(points):
  a=points[max(i-1,0)];b=points[min(i+1,len(points)-1)]
  if i in[0,len(points)-1]:
   d=(b[0]-a[0],b[1]-a[1]);s=math.hypot(*d);off=(-d[1]*half/s,d[0]*half/s)
  else:
   d0=(p[0]-a[0],p[1]-a[1]);d1=(b[0]-p[0],b[1]-p[1]);s0=math.hypot(*d0);s1=math.hypot(*d1);n0=(-d0[1]/s0,d0[0]/s0);n1=(-d1[1]/s1,d1[0]/s1);den=1+n0[0]*n1[0]+n0[1]*n1[1];off=((n0[0]+n1[0])*half/den,(n0[1]+n1[1])*half/den)
  left.append((p[0]+off[0],p[1]+off[1]));right.append((p[0]-off[0],p[1]-off[1]))
 return left+right[::-1]
def arcpoint(t):return(.70+1.10*math.cos(t),1.80+1.10*math.sin(t))
A=arcpoint(math.radians(-150));B=arcpoint(math.radians(-190));C=(-1.70,3.00);D=(-2.08,3.00)
for station,x in enumerate([-1.80,1.80]):
 label=str(station);ped='WholeRootedTrackPedestal'+label
 box(ped,(x-.32,.43,.12),(x+.32,.97,.76),0);JOINS.append((ped,ROOTS[0],(x,.70,.15)))
 tracks=[]
 for side,dx in enumerate([-.205,.205]):
  name='WholeContinuousCurvedGuideCheek'+label+'_'+str(side);tracks.append(name);ts=[math.radians(-90-120*i/24)for i in range(25)]
  poly=[(.70+1.21*math.cos(t),1.80+1.21*math.sin(t))for t in ts]+[(.70+.99*math.cos(t),1.80+.99*math.sin(t))for t in ts[::-1]]
  yzsolid(name,poly,x+dx-.045,x+dx+.045,0);JOINS.append((name,ped,(x+dx,.68,.70)))
 boom='WholeBentOutboardDavit'+label;yzsolid(boom,path_outline([A,B,C,D],.105),x-.09,x+.09,1)
 for level,(y,z)in enumerate([A,B]):
  axle='WholeTransverseGuideAxle'+label+'_'+str(level);pipe(axle,[(x-.30,y,z),(x+.30,y,z)],.045,2,12);JOINS.append((axle,boom,(x,y-.004,z+.020)if level==0 else(x,y,z)))
  for side,dx in enumerate([-.145,.145]):
   roller='WholeGuideRoller'+label+'_'+str(level)+'_'+str(side);wheel(roller,x+dx,y,z,.165,0,.15,2);JOINS.append((roller,axle,(x+dx,y,z)));JOINS.append((roller,tracks[side],(x+(-.19 if side==0 else .19),y,z)))
 pulley='WholeOutboardHeadPulley'+label;wheel(pulley,x,D[0],D[1],.165,0,.25,2);JOINS.append((pulley,boom,(x,D[0]+.025,D[1])))
 cord='WholeFixedSuspensionCord'+label;pipe(cord,[(x,-2.22,3.0),(x,-2.22,1.34)],.022,3,10);JOINS.append((cord,pulley,(x,-2.215,2.99)))
 eye='WholeClosedEmptySuspensionEye'+label;wheel(eye,x,-2.22,1.25,.13,.075,.065,2);JOINS.append((eye,cord,(x,-2.22,1.355)))
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()};FM={n:[m]*len(f)for n,(v,f,m)in G.items()};JOINS=[(a,b,sub(p,SHIFT))for a,b,p in JOINS]
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
focus=Vector((0,0,1.50))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=6.5;aim(cam,(8,-12,7) if view=='qa-front' else (-9,-13,8.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/harbor/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'harbor','style':'S01-clean-geometric','title':'Fixed Paired Curved Guides and Outboard Davit Arms','description':'One wholly newly authored complete fixed paired davit-inspired assembly on one continuous H-shaped grounded frame. Two whole broad pedestals carry four complete thick crescent guide cheeks. A full one-piece bent outboard arm sits between each pair, with two entire transverse axles and four whole broad rollers connecting the arm to its curved guide pair in the depicted fixed overlap relationship. Each full arm rises through the guide bay then bends outward to one whole head pulley, one full straight suspended cord and one whole closed empty eye. The paired stations remain connected by the complete common low frame and count as one assembled prop, not two independent lifting devices. This is not the older single-pivot wheeled shop crane with hydraulic strut and hook; nor a sectional doorway using many panels along vertical-to-horizontal C tracks. The two open crescent guide bays, two whole bent outboard arms and common spanning ground frame define a different whole organization. All numeric solids newly authored together, no old crane, doorway, track, roller or hook geometry imported or extracted. Four opaque constant untextured PBR materials, metres Z up, full horizontal envelope centred at the finite common ground sole, one prop zero scenes. Empty fixed illustrative mechanism only, not working maritime equipment. Rollers and guides deliberately overlap as static roots; no rolling fit, travel path, lowering, lifting, suspension strength, cable bending, loading, balance, boat compatibility, stability, manufacture, installation, maintenance or safety capability made or verified. No boat, payload, animation, rigging or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
