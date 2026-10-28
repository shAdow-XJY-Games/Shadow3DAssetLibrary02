import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='waterworks-fixed-through-bore-headwall-and-top-hinged-round-flap-01'
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
PALETTE=[('WholeHeadwallWarmMineral',(.47,.44,.37,1),.86,0),('WholeOutletSleeveDeepTeal',(.08,.22,.24,1),.64,.44),('WholeFlapSlateSteel',(.23,.34,.36,1),.59,.52),('WholeTopPivotSatinSteel',(.43,.46,.45,1),.42,.70)]
G={};FM={};LINKS=[];ROOTS=['WholeRectangularHeadwallWithCircularThroughBore'];GAPS=[]
# One complete closed rectangular headwall with a genuine full depth circular
# aperture; sampled radial outer rays include all exact rectangle corners.
a0=[math.tau*i/48 for i in range(48)];a0 += [math.atan2(z-1.4,x)%math.tau for x,z in[(-1.5,0),(1.5,0),(1.5,3.0),(-1.5,3.0)]];aa=sorted(set(a0));nn=len(aa)
inner=[(.90*math.cos(a),1.4+.90*math.sin(a))for a in aa];outer=[]
for a in aa:
 c,s=math.cos(a),math.sin(a);rx=1.5/abs(c)if abs(c)>1e-12 else 1e99;rz=(1.6/s if s>0 else -1.4/s)if abs(s)>1e-12 else 1e99;r=min(rx,rz);outer.append((r*c,1.4+r*s))
v=[(x,y,z)for y in[-.55,-.20]for loop in[outer,inner]for x,z in loop];f=[]
for i in range(nn):
 j=(i+1)%nn
 for a,b,c,d in[(i,j,nn+j,nn+i),(2*nn+i,3*nn+i,3*nn+j,2*nn+j),(i,2*nn+i,2*nn+j,j),(nn+i,nn+j,3*nn+j,3*nn+i)]:f.extend([(a,b,c),(a,c,d)])
record(ROOTS[0],v,f,0)
# Whole open sleeve and proud integral flange, with uninterrupted bore through
# both the sleeve and the headwall. No capped cylinder or black painted opening.
profile=[(-.58,.80),(-.58,.92),(.12,.92),(.12,1.02),(.26,1.02),(.26,.80)]
v=[(r*math.cos(a),y,1.4+r*math.sin(a))for y,r in profile for a in aa];f=[]
for k in range(len(profile)):
 for i in range(nn):j=(i+1)%nn;a=k*nn+i;b=k*nn+j;c=((k+1)%len(profile))*nn+j;d=((k+1)%len(profile))*nn+i;f.extend([(a,b,c),(a,c,d)])
record('WholeOpenSleeveAndIntegralOutletFlange',v,f,1)
# Two complete top cheeks anchor the transverse fixed pivot above the round bore.
for x,name in[(-.65,'Left'),(.65,'Right')]:
 pad('WholeTopPivotCheek'+name,[(-.34,2.42),(.48,2.42),(.62,2.54),(.62,2.77),(.50,2.83),(-.34,2.83)],x-.10,x+.10,2)
 v,f,m=G['WholeTopPivotCheek'+name];record('WholeTopPivotCheek'+name,[(y,x,z)for x,y,z in v],f,m)
pipe('WholeTransverseTopPivotAxle',[(-.88,.46,2.65),(.88,.46,2.65)],.09,3,24)
ANGLE=math.radians(40);PV=(0,.46,2.65)
def flap(p):
 x,y,z=sub(p,PV);return add(PV,(x,y*math.cos(ANGLE)-z*math.sin(ANGLE),y*math.sin(ANGLE)+z*math.cos(ANGLE)))
# One entire circular plate held in a fixed raised attitude; its complete rim
# remains intact. Straps are complete new components, not a cropped old gate.
poly=[(1.02*math.cos(a),1.4+1.02*math.sin(a))for a in aa]
pad('WholeRaisedRoundFlapPlate',poly,.405,.495,2)
v,f,m=G['WholeRaisedRoundFlapPlate'];record('WholeRaisedRoundFlapPlate',[flap(p)for p in v],f,m)
for x,name in[(-.38,'Left'),(.38,'Right')]:
 box('WholeFlapPivotStrap'+name,(x-.085,.465,1.20),(x+.085,.565,2.70),3)
 v,f,m=G['WholeFlapPivotStrap'+name];record('WholeFlapPivotStrap'+name,[flap(p)for p in v],f,m)
def root(a,b,p,e=.002):LINKS.append((a,b,[p]+[tuple(p[k]+(sg*e if k==ax else 0)for k in range(3))for ax in range(3)for sg in[-1,1]]))
root(ROOTS[0],'WholeOpenSleeveAndIntegralOutletFlange',(.91,-.37,1.4),.001)
for x,name in[(-.65,'Left'),(.65,'Right')]:
 root(ROOTS[0],'WholeTopPivotCheek'+name,(x,-.28,2.60))
 root('WholeTopPivotCheek'+name,'WholeTransverseTopPivotAxle',(x,.46,2.65))
for x,name in[(-.38,'Left'),(.38,'Right')]:
 root('WholeTransverseTopPivotAxle','WholeFlapPivotStrap'+name,flap((x,.515,2.65)))
 root('WholeFlapPivotStrap'+name,'WholeRaisedRoundFlapPlate',flap((x,.480,1.50)))
# End-to-end sleeve rays remain below the raised plate, not just short mouth rays.
for x,z in[(0,.70),(-.20,.70),(.20,.70),(0,.80),(-.30,.80),(.30,.80)]:GAPS.append(dict(label='SelectedFullSleeveAndRaisedFlapClearance',origin_m=[x,-.85,z],direction=[0,1,0],length_m=2.9))
for x in[-.85,0,.85]:GAPS.append(dict(label='SelectedOpenBottomFlapGap',origin_m=[x,.45,.60],direction=[0,1,0],length_m=1.5))
for x,z in[(1.3,1.40),(.85,1.40),(0,2.65)]:GAPS.append(dict(label='WallSleeveOrTopPivotSolidControl',origin_m=[x,-.85,z],direction=[0,1,0],length_m=2.9,blocked=True))
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([sub(p,SHIFT)for p in v],f,m)for n,(v,f,m)in G.items()};FM={n:[m]*len(f)for n,(v,f,m)in G.items()};LINKS=[(a,b,[sub(p,SHIFT)for p in pts])for a,b,pts in LINKS]
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
focus=Vector((0,0,1.5))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=4.8;aim(cam,(6,9,4.4) if view=='qa-front' else (-7,10,5.4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/waterworks/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'prop','theme':'waterworks','style':'S01-clean-geometric','title':'Fixed Through Bore Headwall and Top Hinged Round Flap','description':'One wholly new fixed outfall flap-gate appearance. A complete rectangular mineral headwall has a genuine circular full-depth opening and uninterrupted flat ground sole. One whole open sleeve with an integral proud outlet flange passes through the wall. Two complete overhead cheeks carry a single transverse fixed axle, and two complete straps connect that axle to one intact thick circular plate held raised outward at forty degrees. The circular plate is not a cropped radial-gate leaf; the sleeve is not an extracted or relabelled valve body. The complete top-edge pivot, raised exterior round flap and open-ended outlet form a distinct relationship from side radial arms and a curved channel-spanning skin, and from a stem/bonnet/handwheel over an inline valve. All eight complete closed meshes newly authored together with four opaque PBR roles; none imported from existing assets. Whole horizontal bounds-centred origin on the headwall sole, metres native Z up, one model zero scenes. Selected nine static root joins each seven internal witnesses, a finite whole ground sole and selected through-bore/below-flap clearances are geometric evidence only. No operating clearance, sealing seat, running bearing, pressure or backflow performance, flood defence, installation compatibility, civil design, real manufacture, engineering certification or public safety claim. No water, rigging, animation, labels, brand or hardware replica. Generic top-hinged outfall vocabulary only; original proportions and geometry.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
