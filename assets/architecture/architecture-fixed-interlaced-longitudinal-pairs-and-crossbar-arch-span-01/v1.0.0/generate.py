import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='architecture-fixed-interlaced-longitudinal-pairs-and-crossbar-arch-span-01'
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
PALETTE=[('WholeInclinedTimbersWarmWood',(.36,.23,.105,1),.84,0),('WholeCrossbarsLightWood',(.58,.39,.19,1),.86,0),('WholeCutEndGrain',(.27,.17,.075,1),.91,0)]
G={};FM={};ROOTS=[];CONTACTS=[];GAPS=[]
# Original finite-facet reciprocal-inspired arch, not a replica or functioning
# friction assembly. Every long timber and every transverse bar is whole.
RADIUS=.08;HALF=.06;D=RADIUS+HALF
MB=4*D/(1-4*D*D);QB=math.hypot(1,MB);Z2=1.60;Z3=Z2+2*D;Z1=Z3-2*MB
DELTA=Z2-Z1
MA=(DELTA+math.sqrt(DELTA*DELTA-(1-4*D*D)*(DELTA*DELTA-4*D*D)))/(1-4*D*D);QA=math.hypot(1,MA)
BA=Z2+D*QA+MA;BB=Z3+D*QB
PINS=[(-2,Z1),(-1,Z2),(0,Z3),(1,Z2),(2,Z1)]
# Each sign describes the timber lying above/below that crossbar in elevation.
SPECS=[('OuterLeft',MA,BA,None,-.84,.94,[(0,-1),(1,1)]),('InnerLeft',MB,BB,-2.18,-.015,.64,[(0,1),(1,-1),(2,1)]),('Crown',0,Z2+D,-1.18,1.18,.34,[(1,1),(2,-1),(3,1)]),('InnerRight',-MB,BB,.015,2.18,.64,[(2,1),(3,-1),(4,1)]),('OuterRight',-MA,BA,.84,None,.94,[(3,1),(4,-1)])]
NORMALS={i:[]for i in range(5)}
for label,m,b,x0,x1,y,joins in SPECS:
 q=math.hypot(1,m)
 for idx,sg in joins:NORMALS[idx].append((-sg*m/q,sg/q))
# Crossbar facets are analytic tangent planes of one nominal small radius.
# Extra planes match every supporting timber's own flat side exactly, creating
# actual finite opposing patches instead of zero-area cylinder tangencies.
for i,(x,z)in enumerate(PINS):
 angles=[math.tau*k/16 for k in range(16)]+[math.atan2(nz,nx)%math.tau for nx,nz in NORMALS[i]];angles=sorted(set(round(a,12)for a in angles));poly=[]
 for a,b in zip(angles,angles[1:]+[angles[0]+math.tau]):
  mid=(a+b)/2;rr=RADIUS/math.cos((b-a)/2);poly.append((x+rr*math.cos(mid),z+rr*math.sin(mid)))
 name='WholeTransverseFacetBar'+str(i+1);pad(name,poly,-1.20,1.20,1)
 v,f,mi=G[name];FM[name]=[2 if max(v[k][1]for k in face)-min(v[k][1]for k in face)<1e-9 else 1 for face in f]
def clipground(poly):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if a[1]>=0:out.append(a)
  if (a[1]<0)!=(b[1]<0):t=-a[1]/(b[1]-a[1]);out.append((a[0]+t*(b[0]-a[0]),0))
 return out
for label,m,b,x0,x1,y,joins in SPECS:
 q=math.hypot(1,m)
 if x0 is None:x0=(-.08-b-HALF*q)/m
 if x1 is None:x1=(-.08-b-HALF*q)/m
 poly=clipground([(x0,m*x0+b-HALF*q),(x1,m*x1+b-HALF*q),(x1,m*x1+b+HALF*q),(x0,m*x0+b+HALF*q)])
 for sg,side in[(-1,'Near'),(1,'Far')]:
  yy=sg*y;name='Whole'+label+side+'LongitudinalTimber';pad(name,poly,yy-.08,yy+.08,0)
  v,f,mi=G[name];FM[name]=[2 if max(v[k][0]for k in face)-min(v[k][0]for k in face)<1e-9 else 0 for face in f]
  if label.startswith('Outer'):ROOTS.append(name)
  for idx,up in joins:
   nx,nz=-up*m/q,up/q;x,z=PINS[idx];p=(x+RADIUS*nx,yy,z+RADIUS*nz)
   CONTACTS.append(('WholeTransverseFacetBar'+str(idx+1),name,p,(nx,0,nz),.00035))
for x in[-.75,0,.75]:
 for z in[.4,.8,1.1]:GAPS.append(dict(label='SelectedOpenArchUnderpass',origin_m=[x,-1.35,z],direction=[0,1,0],length_m=2.70))
for x in[-1.5,-.5,.5,1.5]:GAPS.append(dict(label='SelectedBetweenWholeCrossbarOpenSlot',origin_m=[x,0,.1],direction=[0,0,1],length_m=2.25))
for x,y in[(0,0),(-1,.94),(1,-.94)]:GAPS.append(dict(label='WholeCrossbarAndTimberSolidControl',origin_m=[x,y,.1],direction=[0,0,1],length_m=2.3,blocked=True))
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([sub(p,SHIFT)for p in v],f,m)for n,(v,f,m)in G.items()};CONTACTS=[(a,b,sub(p,SHIFT),n,minimum)for a,b,p,n,minimum in CONTACTS]
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
focus=Vector((0,0,1.08))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=6.6;aim(cam,(7,-12,5.4) if view=='qa-front' else (-8,-11,6.4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/architecture/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'modular','theme':'architecture','style':'S01-clean-geometric','title':'Fixed Interlaced Longitudinal Pairs and Crossbar Arch Span','description':'One newly authored complete static reciprocal-inspired timber arch span. Five laterally separated longitudinal pairs comprise two steeper outer grounded pairs, two shallower inner rising pairs and one whole horizontal crown pair. Five full transverse faceted bars weave above and below those complete timbers in a three-dimensional sequence, leaving the arch underside, middle longitudinal spacing and intervals between crossbars open. The outer four timbers have integral finite flat ground soles; there is no hidden plinth, wall or intermediate pier. Every transverse crossbar is one full closed solid with deliberately aligned narrow tangent facets matching the actual flat sides of its contacting timbers. Twenty-six true finite opposed contact patches, each with three separated sided interior witness pairs, replace penetrating cylinders or zero-area line contacts. All fifteen complete closed meshes and three opaque PBR wood roles are newly authored together; no old bars imported, trimmed, recoloured or rearranged. Unlike the existing opposed cantilever bridge, there are no stacked horizontal projecting courses, masonry abutments, short separate suspended centre span or flat deck; unlike the tall open crib, the elements make one rising open arch and change over-under order rather than nine horizontal courses; unlike the six-member crown roof, this is a bilateral longitudinal and transverse interlacing graph, not a cyclic radial rafter ring on tall columns. Native Z up, metre-style coordinates and full horizontal bounds-centred ground datum, one independent architectural module zero scenes. Generic historical reciprocal-bridge vocabulary only, original numerical proportions and facet contacts, not an exact historical reconstruction or build kit. No deck, guardrail, people or public crossing included. Checked contact geometry does not certify friction, self-support, reciprocal-force balance, strength, mechanical locking, assembly sequence, dynamic stability, loading, pedestrian access, real timber fabrication, construction or structural safety. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
