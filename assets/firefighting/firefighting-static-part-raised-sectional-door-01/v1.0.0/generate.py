import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='firefighting-static-part-raised-sectional-door-01'
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
# Original static segmented door in an explicitly fixed partly raised pose.
PROFILE=[(-.10,-.08),(.04,-.08),(.04,-.05),(-.06,-.05),(-.06,.05),(.04,.05),(.04,.08),(-.10,.08)]
def path(t):
 if t<=2.8:return (0,.14,t),(0,0,1)
 if t<=2.8+math.pi*.25:
  a=(t-2.8)/.5;return (0,.14+.5*(1-math.cos(a)),2.8+.5*math.sin(a)),(0,math.sin(a),math.cos(a))
 return (0,.64+t-2.8-math.pi*.25,3.3),(0,1,0)
stations=[0,2.8]+[2.8+.5*math.pi/2*i/12 for i in range(1,13)]+[2.8+math.pi*.25+1.31]
for s in[-1,1]:
 vv=[]
 for t in stations:
  p,d=path(t);normal=cross(d,(1,0,0))
  for x,q in PROFILE:vv.append(add(add(p,(s*(1.60-x),0,0)),mul(normal,q)))
 n=len(PROFILE);ff=[]
 for k in range(len(stations)-1):
  for i in range(n):
   j=(i+1)%n;a=k*n+i;b=k*n+j;c=(k+1)*n+j;d=(k+1)*n+i;ff.extend([(a,b,c),(a,c,d)])
 for a,b,c in earclip(PROFILE):ff.extend([(c,b,a),(a+(len(stations)-1)*n,b+(len(stations)-1)*n,c+(len(stations)-1)*n)])
 record('WholeCurvedCTrack'+str(s),vv,ff,1)
 x=s*1.79;box('GroundedJamb'+str(s),(x-.09,-.10,0),(x+.09,.24,3.60),0)
 for i,z in enumerate([.45,1.65,2.67]):box('TrackBracket%d_%d'%(s,i),(min(s*1.66,s*1.79),-.015,z-.04),(max(s*1.66,s*1.79),.19,z+.04),1)
box('FullFrontHeader',(-1.70,-.10,3.44),(1.70,.24,3.60),0)
box('RearTrackCrossTie',(-1.72,1.82,3.37),(1.72,1.98,3.46),1)
def panel(name,center,d,width,height,depth,m):
 u=(1,0,0);n=cross(d,u);v=[add(add(add(center,mul(d,k*height/2)),mul(n,j*depth/2)),mul(u,i*width/2))for k in[-1,1]for j in[-1,1]for i in[-1,1]];f=[]
 for a,b,c,e in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:f.extend([(a,b,c),(a,c,e)])
 record(name,v,f,m)
for i in range(10):
 t=1.40+.37*i;p,d=path(t);panel('ClosedDoorSection%02d'%i,p,d,3.08,.33,.052,2)
 for s in[-1,1]:
  pipe('SectionAxle%d_%d'%(i,s),[add(p,(s*1.50,0,0)),add(p,(s*1.62,0,0))],.014,1,8)
  wheel('GuideRoller%d_%d'%(i,s),s*1.60,p[1],p[2],.032,0,.060,3)
# A pair of short dark fixed lift pulls on the lowest panel, not a rig.
for s in[-1,1]:pipe('FixedLowerPull'+str(s),[(s*.65-.10,.12,1.40),(s*.65-.10,.055,1.40),(s*.65+.10,.055,1.40),(s*.65+.10,.12,1.40)],.014,3,8)
# Centre the finite horizontal envelope; ground remains Z0.
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];Y=(lo[1]+hi[1])/2
G={name:([(x,y-Y,z)for x,y,z in v],f,m)for name,(v,f,m)in G.items()}

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
for name,color,rough in [('FrameIvory',(.72,.74,.70,1),.66),('Frame_Silver',(.40,.46,.49,1),.40),('DoorTerracotta',(.56,.09,.045,1),.62),('RollerGraphite',(.035,.04,.045,1),.74)]:
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=.6 if name in ['Frame_Silver','Rims_Satin'] else 0;materials.append(m)
parts=[]
for name,(v,f,mi) in G.items():
 me=bpy.data.meshes.new(name+'Mesh');me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o)
 for m in materials:me.materials.append(m)
 for p in me.polygons:p.material_index=mi;p.use_smooth=False
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
focus=Vector((0,0,1.78))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=5.25;aim(cam,(6,-8,6.4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/firefighting/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'modular','assetKind':'modular','theme':'firefighting','style':'S01-clean-geometric','title':'Static Part-Raised Sectional Overhead Door','description':'Original independent static fire-station doorway module: two whole inward-open C-section guide tracks bend through a quarter turn into overhead returns, carrying ten separate thick door sections and their visible fixed side rollers in one partly raised pose. Grounded jambs, a front header, track brackets and rear cross tie complete the displayed frame; a real lower passage is left open. No host building or roof is included. This is not a translated single sluice plate or hinged gate. No door motion, rigging, exact roller contact, continuous clearance, mounting compatibility, weather seal, fire resistance, human access, load or safety certification is claimed.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
