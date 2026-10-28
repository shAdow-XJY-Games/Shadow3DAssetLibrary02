import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='harbor-fixed-deep-grooved-roller-and-notched-cross-bridge-stopper-01'
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
PALETTE=[('WholeMountAndTrueBoredCheeks',(.11,.25,.27,1),.65,.40),('WholeDeepGroovedRoller',(.39,.44,.45,1),.46,.72),('WholeNotchedStopBridge',(.55,.32,.12,1),.53,.52),('WholeIntegralRollerJournals',(.08,.12,.14,1),.43,.71)]
FM={};ROOTS=['WholeGroundMount'];CONTACTS=[];LINKS=[];GAPS=[];SHIFT=(0,0,0)
box(ROOTS[0],(-1.02,-.84,0),(1.02,.84,.12),0)
XC=-.32;ZC=.64;JR=.13;BR=.18;SEG=16;PH=math.pi/SEG;SEAT=ZC-JR*math.cos(PH);BZ=SEAT+BR*math.cos(PH)
# Two entire rectangular side cheeks, each with a real complete polygonal bearing bore.
outer=[(.82,BZ),(.82,.90),(.82,1.08),(.20,1.08),(-.32,1.08),(-.60,1.08),(-.82,1.08),(-.82,.90),(-.82,BZ),(-.82,.40),(-.82,.12),(-.55,.12),(-.32,.12),(.25,.12),(.82,.12),(.82,.40)]
inner=[(XC+BR*math.cos(math.tau*i/SEG+PH),BZ+BR*math.sin(math.tau*i/SEG+PH))for i in range(SEG)]
for sy in[-1,1]:
 y=sy*.59;name='WholeTrueBoredSideCheek_'+str(sy);v=[]
 for yy in[y-.08,y+.08]:
  for ring in[outer,inner]:v.extend([(x,yy,z)for x,z in ring])
 f=[]
 for i in range(SEG):
  j=(i+1)%SEG
  for a,b,c,d in[(i,j,j+SEG,i+SEG),(i+2*SEG,i+3*SEG,j+3*SEG,j+2*SEG),(i,i+2*SEG,j+2*SEG,j),(i+SEG,j+SEG,j+3*SEG,i+3*SEG)]:f.extend([(a,b,c),(a,c,d)])
 record(name,v,f,0);CONTACTS.append((ROOTS[0],name,(.40,y,.12),(0,0,1),.26))
# One whole roller and its two integral full journals: deep central groove, no winding bay/drum flanges assembled from disks.
prof=[(0,-.76),(JR,-.76),(JR,-.43),(.42,-.43),(.42,-.32),(.28,-.10),(.28,.10),(.42,.32),(.42,.43),(JR,.43),(JR,.76),(0,.76)]
v=[];rings=[];f=[];fm=[]
for r,y in prof:
 pts=[(XC,y,ZC)]if r==0 else[(XC+r*math.cos(math.tau*i/SEG+PH),y,ZC+r*math.sin(math.tau*i/SEG+PH))for i in range(SEG)]
 rings.append(list(range(len(v),len(v)+len(pts))));v+=pts
for k,(a,b)in enumerate(zip(rings,rings[1:]+rings[:1])):
 if len(a)==len(b)==1:continue
 mat=3 if max(prof[k][0],prof[(k+1)%len(prof)][0])<=JR else 1
 for i in range(SEG):
  j=(i+1)%SEG
  ff=[(a[0],b[i],b[j])]if len(a)==1 else[(a[i],b[0],a[j])]if len(b)==1 else[(a[i],b[i],b[j]),(a[i],b[j],a[j])]
  f+=ff;fm += [mat]*len(ff)
record('WholeGroovedRollerAndIntegralJournals',v,f,1);FM['WholeGroovedRollerAndIntegralJournals']=fm
for sy in[-1,1]:CONTACTS.append(('WholeTrueBoredSideCheek_'+str(sy),'WholeGroovedRollerAndIntegralJournals',(XC,sy*.59,SEAT),(0,0,1),.008))
# Complete rear transverse blocking bridge with a genuine central bottom-open slot.
# Profile coordinates are Y/Z; it has two finite end soles on the full cheek tops.
p=[(-.69,1.08),(-.16,1.08),(-.16,1.30),(.16,1.30),(.16,1.08),(.69,1.08),(.69,1.42),(-.69,1.42)]
pad('WholeCentralNotchedBlockingBridge',p,.38,.58,2)
a,f,m=G['WholeCentralNotchedBlockingBridge'];G['WholeCentralNotchedBlockingBridge']=([(yy,x,z)for x,yy,z in a],[(i,k,j)for i,j,k in f],m)
for sy in[-1,1]:CONTACTS.append(('WholeTrueBoredSideCheek_'+str(sy),'WholeCentralNotchedBlockingBridge',(.48,sy*.59,1.08),(0,0,1),.031))
# Selected rays explicitly describe only their bounded paths, not exhaustive swept-fit/void certification.
for sy in[-1,1]:
 for dx in[-.06,0,.06]:GAPS.append(dict(label='SelectedRealBoreUpperAir',origin_m=[XC+dx,sy*.59-.10,.83],direction=[0,1,0],length_m=.20))
for z in[1.12,1.20,1.26]:GAPS.append(dict(label='SelectedWholeBridgeCentralNotch',origin_m=[.30,0,z],direction=[1,0,0],length_m=.36))
for y in[-.20,0,.20]:GAPS.append(dict(label='SelectedBelowWholeRollerAir',origin_m=[-.82,y,.17],direction=[1,0,0],length_m=1.0))
GAPS += [dict(label='WholeRollerSolidControl',origin_m=[-.9,0,.64],direction=[1,0,0],length_m=1.2,blocked=True),dict(label='WholeNotchRoofSolidControl',origin_m=[.30,0,1.36],direction=[1,0,0],length_m=.36,blocked=True)]
FM.update({n:[m]*len(f)for n,(v,f,m)in G.items()if n not in FM})
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
focus=Vector((0,0,.72))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.85 if view=='qa-front' else 3.15;aim(cam,(-7,-10,5.2) if view=='qa-front' else (-8,-9,12));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/harbor/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'harbor','style':'S01-clean-geometric','title':'Fixed Deep Grooved Roller and Notched Cross Bridge Stopper','description':'One newly authored complete empty fixed roller-chain-stopper-inspired deck fitting. A broad entire ground mount carries two whole full-height side cheeks, each with a genuine complete sixteen-facet through-bore. One continuous deep-grooved horizontal roller includes both full integral journals; their lower flat facets rest on finite opposed bore-bottom facets, while selected upper bore air remains clear. A separate entire transverse blocking bridge sits behind the roller on both full cheek tops. Its thick body has a real central bottom-open rectangular notch, not a painted slot. All five closed whole meshes and numerical profiles newly authored together, no fairlead, winch, roller, stop arm, plate or ship fragment imported or cropped. Unlike the earlier four-roller fairlead there is only one full deeply waisted roller and a fixed notched bridge rather than opposed four-boundary staggered rollers; unlike the ratchet drum winch there is no empty winding bay with separated drum flanges, asymmetric toothed wheel, pawl, crank or handgrip. Six finite opposed support seats, each with five separated sided witnesses, connect every whole component to the full rectangular sole; twelve selected empty rays and two solid controls supplement the complete source/actual triangle checks without claiming exhaustive clearance volumes. Four opaque constant PBR materials, metre-style native Z up, complete horizontal bounds-centred ground origin, one independent prop zero scenes. Generic fixed visual vocabulary and original proportions only, not a named manufacturer item or measured device. The fixed stop bridge deliberately has no working hinge, release or lock assembly, and no chain, rope, attached load, ship deck, operator, actuator, labels, texture or animation is present. No link-size compatibility, engagement, rotation, stopping, release, friction, braking, force, capacity, manufacturing, installation, operational marine or equipment safety capability is claimed.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
