import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='military-fixed-convex-kite-shield-with-rear-loops-01'
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

# Whole convex pointed shield shell with complete rear arm loops.
PALETTE=[('ShieldMutedBlueFace',(.075,.15,.22,1),.74,.12),('ShieldSteelRimAndBoss',(.38,.40,.39,1),.48,.68),('ShieldBrownRearStraps',(.17,.085,.035,1),.88,0)]
outline=[(-.012,0),(.012,0),(.20,.25),(.32,.80),(.30,1.05),(.15,1.14),(-.15,1.14),(-.30,1.05),(-.32,.80),(-.20,.25)]
S=len(outline)
# Two corresponding fan surfaces and a finite perimeter wall form one complete body.
v=[(0,-.145,.62)]+[(x*.985,-.025,.62+(z-.62)*.985)for x,z in outline]+[(0,-.120,.62)]+[(x*.985,.000,.62+(z-.62)*.985)for x,z in outline];f=[]
for i in range(S):
 j=(i+1)%S;f +=[(0,1+i,1+j),(S+1,S+2+j,S+2+i),(1+i,S+2+i,S+2+j),(1+i,S+2+j,1+j)]
record('WholeConvexPointedShieldBody',v,f,0)
# A complete raised metal perimeter follows the actual whole pointed outline.
inside=[(x*.94,.62+(z-.62)*.94)for x,z in outline]
v=[(x,y,z)for poly,y in[(outline,-.031),(outline,.007),(inside,.007),(inside,-.039)]for x,z in poly];f=[]
for k in range(4):
 for i in range(S):j=(i+1)%S;a=k*S+i;b=k*S+j;c=((k+1)%4)*S+j;d=((k+1)%4)*S+i;f.extend([(a,b,c),(a,c,d)])
record('WholeFinitePointedPerimeterRim',v,f,1)
# Solid faceted centre boss, wholly seated into the body; decorative nonweapon form.
SEG=20;profile=[(-.126,.105),(-.165,.105),(-.205,.077),(-.225,.034),(-.231,0)]
v=[];ix=[]
for y,r in profile:
 rr=[(0,y,.62)]if r==0 else[(r*math.cos(math.tau*i/SEG),y,.62+r*math.sin(math.tau*i/SEG))for i in range(SEG)];ix.append(list(range(len(v),len(v)+len(rr))));v+=rr
f=[]
# Back disk lies inside the finite body volume at the centre.
c=len(v);v.append((0,-.126,.62))
for i in range(SEG):f.append((c,ix[0][(i+1)%SEG],ix[0][i]))
for a,b in zip(ix,ix[1:]):
 for i in range(SEG):
  j=(i+1)%SEG
  if len(b)==1:f.append((a[i],a[j],b[0]))
  else:f.extend([(a[i],a[j],b[j]),(a[i],b[j],b[i])])
record('WholeLowFacetedCentreBoss',v,f,1)
def rear_y(x,z):
 c=(0,.62);poly=[(a*.985,.62+(b-.62)*.985)for a,b in outline]
 for i,a in enumerate(poly):
  b=poly[(i+1)%len(poly)];den=(a[0]-c[0])*(b[1]-c[1])-(a[1]-c[1])*(b[0]-c[0])
  u=((x-c[0])*(b[1]-c[1])-(z-c[1])*(b[0]-c[0]))/den
  v=((a[0]-c[0])*(z-c[1])-(a[1]-c[1])*(x-c[0]))/den
  if u>=-1e-10 and v>=-1e-10 and u+v<=1+1e-10:return -.120*(1-u-v)
 raise AssertionError(('Rear mounting point outside full body',x,z))
def rearfoot(name,x,z):
 corners=[(x-.018,z-.035),(x+.018,z-.035),(x+.018,z+.035),(x-.018,z+.035)]
 v=[(xx,rear_y(xx,zz)+d,zz)for d in[-.003,.012]for xx,zz in corners]
 f=[]
 for a,b,c,d in[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:f.extend([(a,b,c),(a,c,d)])
 record(name,v,f,1)

# Two continuous closed thick rear arches with finite embedded end feet.
for name,z,width in[('UpperRearArmLoop',.78,.13),('LowerRearGripLoop',.43,.115)]:
 pts=[(-width,rear_y(-width,z)+.004,z),(-width,.025,z),(-width*.70,.100,z),(width*.70,.100,z),(width,.025,z),(width,rear_y(width,z)+.004,z)]
 # Closed rectangular strip swept with one nonzero width along Z.
 vv=[]
 for i,p in enumerate(pts):
  d=unit(sub(pts[min(i+1,len(pts)-1)],pts[max(0,i-1)]));w=(-d[1],d[0],0)
  for a,b in[(-1,-1),(1,-1),(1,1),(-1,1)]:vv.append(add(p,add(mul(w,.006*a),(0,0,.022*b))))
 ff=[(0,2,1),(0,3,2)];e=4*(len(pts)-1);ff +=[(e,e+1,e+2),(e,e+2,e+3)]
 for k in range(len(pts)-1):
  for i in range(4):j=(i+1)%4;a=4*k+i;b=4*k+j;c=4*(k+1)+j;d=4*(k+1)+i;ff.extend([(a,b,c),(a,c,d)])
 record(name,vv,ff,2)
 for sign in[-1,1]:rearfoot(name+'FiniteFoot'+str(sign),sign*width,z)
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
focus=Vector((0,0,.56))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.45;aim(cam,(4,7,4) if view=="qa-front" else (4,-7,4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/military/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'military','style':'S01-clean-geometric','title':'Fixed Convex Kite Shield with Rear Loops','description':'One complete original fixed convex kite-shield display with a pointed flat-ended lower silhouette, broad shouldered crown, one shared-vertex thick outward-bowed body, a complete finite perimeter rim and a seated low faceted centre boss. Two entire thick arched rear straps have four embedded finite mounting feet and real empty space between each arch and the body. One shield, no wearer, weapon, emblem, lettering or stand. Newly drawn defensive-costume art, not the old narrow surfboard with its fin removed or a welding hood with a viewing insert. Three opaque constant PBR materials, metres, horizontal bounds centred and lowest edge at ground. Static invented appearance only, no arm fit, protective or impact performance, balance, working fastening, historical precision, manufacturing or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
