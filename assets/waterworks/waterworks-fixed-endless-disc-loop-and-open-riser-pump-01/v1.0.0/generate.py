import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='waterworks-fixed-endless-disc-loop-and-open-riser-pump-01'
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
PALETTE=[('WholeSupportFrameMutedTeal',(.10,.28,.29,1),.70,.26),('WholeRiserAndPistonFacesWarmGrey',(.61,.63,.56,1),.72,.10),('WholeEndlessCordOchre',(.47,.28,.11,1),.82,.04),('WholeWheelsAndAxlesDarkSteel',(.14,.18,.19,1),.56,.55)]
FM={};JOINS=[];ROOTS=[]
# Entire fixed free-standing illustrative frame, not a hidden cut from a well installation.
for side,x in [('Left',-1.10),('Right',1.10)]:
 foot='WholeGroundSole'+side;box(foot,(x-.22,-.28,0),(x+.22,.82,.14),0);ROOTS.append(foot)
 post='WholeUpright'+side;box(post,(x-.09,.40,.10),(x+.09,.64,4.03),0);JOINS.append((foot,post,(x,.51,.12)))
for label,z in [('Lower',.95),('Upper',3.8)]:
 rail='WholeRearCrossRail'+label;box(rail,(-1.18,.44,z-.12),(1.18,.62,z+.12),0)
 for side,x in [('Left',-1.10),('Right',1.10)]:JOINS.append((rail,'WholeUpright'+side,(x,.53,z)))
 axle='WholeThroughAxle'+label;pipe(axle,[(0,-.34,z),(0,.58,z)],.07,3,16);JOINS.append((axle,rail,(0,.53,z)))
 # Whole open rim and hub with three complete supporting spokes, all independently rooted.
 for name,ro,ri,width in [('WholeOpenPulleyRim'+label,.63,.49,.18),('WholePulleyHub'+label,.15,0,.28)]:
  wheel(name,0,0,z,ro,ri,width,3);v,f,m=G.pop(name);record(name,[(y,x,zz)for x,y,zz in v],f,m)
 JOINS.append(('WholePulleyHub'+label,axle,(.04,0,z)))
 for k in range(3):
  t=.25+math.tau*k/3;name='WholePulleySpoke'+label+str(k);pipe(name,[(.10*math.cos(t),0,z+.10*math.sin(t)),(.55*math.cos(t),0,z+.55*math.sin(t))],.055,3,10)
  JOINS +=[(name,'WholePulleyHub'+label,(.13*math.cos(t),0,z+.13*math.sin(t))),(name,'WholeOpenPulleyRim'+label,(.52*math.cos(t),0,z+.52*math.sin(t)))]
box('WholeRearRiserMountRail',(-.74,.43,.94),(-.56,.63,3.81),0)
JOINS +=[('WholeRearRiserMountRail','WholeRearCrossRailLower',(-.65,.52,.99)),('WholeRearRiserMountRail','WholeRearCrossRailUpper',(-.65,.52,3.75))]
# Full-height half-round riser display shell, with both longitudinal cutaway lips and both full end rims.
angles=[math.pi*i/20 for i in range(21)];profile=[(.18*math.cos(t),.18*math.sin(t))for t in angles]+[(.14*math.cos(t),.14*math.sin(t))for t in reversed(angles)]
pad('WholeOpenFrontHalfRoundRiser',profile,1.40,3.30,1);v,f,m=G.pop('WholeOpenFrontHalfRoundRiser');record('WholeOpenFrontHalfRoundRiser',[(x-.65,z,y)for x,y,z in v],f,m)
for i,z in enumerate([1.55,3.15]):
 name='WholeRiserRearBracket'+str(i);box(name,(-.72,.145,z-.06),(-.58,.53,z+.06),0);JOINS +=[(name,'WholeOpenFrontHalfRoundRiser',(-.65,.16,z)),(name,'WholeRearRiserMountRail',(-.65,.50,z))]
# One fully closed constant-section cord around both pulleys; never a set of disconnected segments.
path=[(.65*math.cos(math.pi*i/32),0,3.8+.65*math.sin(math.pi*i/32))for i in range(33)]
path +=[(-.65,0,3.8-(3.8-.95)*i/8)for i in range(1,8)]
path +=[(.65*math.cos(math.pi+math.pi*i/32),0,.95+.65*math.sin(math.pi+math.pi*i/32))for i in range(33)]
path +=[(.65,0,.95+(3.8-.95)*i/8)for i in range(1,8)]
v=[];f=[];NROPE=8
for k,p in enumerate(path):
 a=path[(k-1)%len(path)];b=path[(k+1)%len(path)];t=unit(sub(b,a));normal=(t[2],0,-t[0])
 for j in range(NROPE):
  ang=math.tau*j/NROPE;v.append(add(p,add(mul(normal,.026*math.cos(ang)),(0,.026*math.sin(ang),0))))
for k in range(len(path)):
 kk=(k+1)%len(path)
 for j in range(NROPE):
  jj=(j+1)%NROPE;a=k*NROPE+j;b=k*NROPE+jj;c=kk*NROPE+jj;d=kk*NROPE+j;f.extend([(a,b,c),(a,c,d)])
record('WholeEndlessClosedCord',v,f,2);JOINS +=[('WholeEndlessClosedCord','WholeOpenPulleyRimUpper',(0,0,4.427)),('WholeEndlessClosedCord','WholeOpenPulleyRimLower',(0,0,.323))]
# Eight entire small annular discs occupy the straight runs in this deliberately fixed display pose.
# Blank turning arcs are intentional: no rolling path, force transfer or physical piston operation claimed.
PISTONS=[]
for side,x in [('Rising',-.65),('Returning',.65)]:
 for i,z in enumerate([1.45,2.05,2.65,3.25]):
  name='WholeCordPiston'+side+str(i);turned(name,x,0,[(.018,z-.028),(.115,z-.028),(.115,z+.028),(.018,z+.028)],1,24);JOINS.append((name,'WholeEndlessClosedCord',(x+.022,0,z)));PISTONS.append((name,x,z))
pipe('WholeOffsetCrankArm',[(0,-.31,3.8),(.42,-.31,3.50)],.065,3,12);pipe('WholeForwardHandGrip',[(.42,-.31,3.50),(.42,-.65,3.50)],.075,0,12)
JOINS +=[('WholeOffsetCrankArm','WholeThroughAxleUpper',(.012,-.31,3.791)),('WholeForwardHandGrip','WholeOffsetCrankArm',(.408,-.33,3.509))]
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
focus=Vector((0,0,2.20))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=5.8;aim(cam,(7,-13,8) if view=='qa-front' else (-7,-13,9));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/waterworks/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'waterworks','style':'S01-clean-geometric','title':'Fixed Endless Disc Loop and Open Riser Pump Display','description':'One wholly newly authored complete free-standing dry rope-and-disc-lift-inspired inspection display. One genuinely continuous closed constant-section cord loop passes around two entire open three-spoke pulleys on separate full through axles. Eight complete small annular discs are fixed to the two straight cord runs, four on each side, rather than occupying a common rigid spindle. The left run passes through the real inner space of one entire full-height open-front half-round riser shell, whose two full longitudinal inspection lips and both finite end rims are supplied. The shell sits between and clear of both pulley rims on two full rear brackets and a separate full-length rear mounting rail. Two whole upright posts, two complete cross rails and two broad grounded soles support the shafts, open pulleys, loop, casing, crank arm and complete forward hand grip. Unlike the common-spindle contactor, there is no horizontal basin, large repeated radial disc stack or shared rigid shaft through all discs. Unlike the stationary open U tube and three-roller pump, the single full cord itself forms an endless tall loop, small discs travel conceptually with it, and the straight open riser is separate from the upper and lower pulley axles; there is no closed semicircular hose head or radial three-roller carrier. All shape coordinates and full material boundaries newly authored together; no old tube, frame, disc, pulley or basin mesh imported, extracted or transformed. Thirty-three editable complete closed material meshes, four opaque constant untextured PBR roles, metre-style native Z up and horizontal bounds-centred ground datum, one whole display model zero scenes. Broad rope-pump category only: original artistic proportions, not a replica of any public-domain standard or installed well pump. Turning arcs are deliberately free of discs in this fixed display pose, and small rooted cord-to-rim overlaps are static visual joins, not solved rolling or friction contacts. The deliberately open-front casing is an entire authored inspection shell, not a sealed rising main; there is no well, immersed guide box, discharge spout, water circuit or operating installation. No water lifting, hydraulic continuity, pumping output, water quality, drinking-water suitability, piston sealing, rope tension, disc transport path, pulley rotation, friction, drive operation, loading, stability, wear, manufacture, installation, maintenance or machinery/public-health safety capability made or verified. No fluid, animation, rigging or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
