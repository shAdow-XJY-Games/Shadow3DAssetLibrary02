import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='architecture-fixed-stepped-loop-escalator-module-01'
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

# Complete fixed escalator module: stepped material loop and two closed handrail loops.
PALETTE=[('StepAndEndDeckMetal',(.47,.51,.51,1),.63,.48),('OpaqueBalustradeBlue',(.24,.36,.39,1),.67,.25),('WholeLoopHandrailDark',(.075,.105,.11,1),.72,.12)]
def xprofile(name,p,x0,x1,m):
 pad(name,p,x0,x1,m);v,f,mi=G[name];record(name,[(y,x,z)for x,y,z in v],f,mi)
def ringx(name,outer,inner,x0,x1,m):
 assert len(outer)==len(inner);n=len(outer);v=[(x,y,z)for x,p in[(x0,outer),(x1,outer),(x0,inner),(x1,inner)]for y,z in p];f=[]
 for i in range(n):
  j=(i+1)%n
  for a,b,c,d in[(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)]:f.extend([(a,b,c),(a,c,d)])
 record(name,v,f,m)
outer=[(-1.75,.45),(-1.12,.45)]
for i in range(8):
 y=-1.12+(i+1)*.28;z=.45+i*.15;outer.append((y,z));outer.append((y,z+.15))
outer +=[(1.75,1.65),(1.86,1.57),(1.90,1.42),(1.83,1.30),(1.70,1.24),(-1.70,.04),(-1.83,.10),(-1.90,.22),(-1.86,.37)]
# Finite parallel-line inset of the simple full stepped outline; no centre scaling.
def inset_poly(p,d):
 sign=1 if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(p,p[1:]+p[:1]))>0 else -1
 lines=[]
 for a,b in zip(p,p[1:]+p[:1]):
  dx=b[0]-a[0];dz=b[1]-a[1];le=math.hypot(dx,dz);nx=-sign*dz/le;nz=sign*dx/le;lines.append(((a[0]+nx*d,a[1]+nz*d),(dx,dz)))
 out=[]
 for i,(a,u)in enumerate(lines):
  b,v=lines[i-1];det=u[0]*v[1]-u[1]*v[0]
  if abs(det)<1e-12:out.append(a);continue
  t=((b[0]-a[0])*v[1]-(b[1]-a[1])*v[0])/det;out.append((a[0]+t*u[0],a[1]+t*u[1]))
 return out
inner=inset_poly(outer,.035)
def inpoly(p,poly):
 x,z=p;inside=False
 for (a,b),(c,d)in zip(poly,poly[1:]+poly[:1]):
  if (b>z)!=(d>z)and x<(c-a)*(z-b)/(d-b)+a:inside=not inside
 return inside
assert all(inpoly(p,outer)for p in inner),'Inner return outside belt silhouette'
ringx('WholeContinuousSteppedFlightAndReturnBelt',outer,inner,-.48,.48,0)
for name,y0,y1,z in [('LowerLanding',-2.22,-1.75,.45),('UpperLanding',1.75,2.22,1.65)]:
 box('WholeStationary'+name,(-.60,y0,z-.075),(.60,y1,z),0)
 for side in[-1,1]:box(name+'MountingFlange_'+str(side),(side*.66-.08,y0+.035,z-.09),(side*.66+.08,y1-.035,z-.045),1)
sidepoly=[(-1.84,.30),(-1.84,.86),(-1.56,1.10),(1.56,2.30),(1.84,2.06),(1.84,1.48),(1.68,1.32),(-1.68,.12)]
for side in[-1,1]:
 x=side*.56;xprofile('WholeOpaqueBalustrade_'+str(side),sidepoly,x-.035,x+.035,1)
 A=(-1.52,.92);B=(1.52,2.12);phi=math.atan2(B[1]-A[1],B[0]-A[0])
 def capsule(r):
  return [(A[0]+r*math.cos(phi+math.pi/2+math.pi*i/12),A[1]+r*math.sin(phi+math.pi/2+math.pi*i/12))for i in range(13)]+[(B[0]+r*math.cos(phi-math.pi/2+math.pi*i/12),B[1]+r*math.sin(phi-math.pi/2+math.pi*i/12))for i in range(13)]
 ringx('WholeClosedReturnHandrail_'+str(side),capsule(.205),capsule(.165),x-.055,x+.055,2)
 for suffix,y,z in [('Lower',-1.75,.54),('Upper',1.75,1.74)]:box('WholeHandrailEntryHousing_'+str(side)+suffix,(x-.07,y-.12,z-.12),(x+.07,y+.12,z+.09),1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
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
focus=Vector((0,0,1.10))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=5.20;aim(cam,(7,-8,5.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/architecture/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'architecture','style':'S01-clean-geometric','title':'Fixed Stepped Loop Escalator Module','description':'One original complete fixed escalator-module appearance: one continuous thick stepped annular flight with real open interior and lower return, separate stationary low/high landing plates with mounting flanges, two full opaque sloped balustrades, and two separate closed thick handrail return loops with end-entry housings. Unlike a flat running belt or a rigid stair cart, the stepped top and both terminal returns belong to one material loop, while handrails form their own continuous loops alongside two different-level landings. No old meshes imported. Three opaque PBR materials, metres and actual XY-envelope centring. One uninstalled static module, no building floors, passenger or motor/drive internals; lowest return edge is export datum, not a certified ground sole. No animation, physical chain articulation, step synchronisation, handrail movement, comb clearance, human accessibility, capacity, loading, installation or safety performance claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
