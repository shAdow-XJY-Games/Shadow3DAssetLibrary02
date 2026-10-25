import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='fantasy-static-bull-head-and-two-hoof-minotaur-01'
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
PALETTE=[('WholeWarmBovineHide',(.30,.135,.055,1),.90,0),('WholeHornsWarmIvory',(.64,.54,.34,1),.86,0),('WholeHoofNoseEyesAndWrap',(.055,.040,.027,1),.85,0)]
# Newly drawn full figure sections, not imported animal or human parts.
FM={}
def shaped(name,rows,axis,mat,n=12,bands=None):
 v=[];f=[];mats=[]
 for x,y,z,rx,ry in rows:
  for j in range(n):
   a=math.tau*j/n
   v.append((x+rx*math.cos(a),y+ry*math.sin(a),z)if axis=='Z'else((x,y+rx*math.cos(a),z+ry*math.sin(a))if axis=='X'else(x+rx*math.cos(a),y,z+ry*math.sin(a))))
 for k in range(len(rows)-1):
  for j in range(n):
   a=k*n+j;b=k*n+(j+1)%n;c=b+n;d=a+n;f.extend([(a,b,c),(a,c,d)]);mats.extend([bands[k]if bands else mat]*2)
 for k in [0,len(rows)-1]:
  center=len(v);v.append(rows[k][:3])
  for j in range(n):f.append((center,k*n+(j+1)%n,k*n+j)if k==0 else(center,k*n+j,k*n+(j+1)%n));mats.append(bands[0 if k==0 else-1]if bands else mat)
 record(name,v,f,mat);FM[name]=mats
shaped('WholeUprightBroadChestAndCoveredHip',[(0,.02,.79,.22,.17),(0,.02,1.00,.25,.19),(0,.015,1.13,.22,.16),(0,0,1.35,.34,.23),(0,.005,1.56,.42,.24),(0,.02,1.67,.34,.21),(0,0,1.74,.16,.14)],'Z',0,16,[2,2,0,0,0,0])
shaped('WholeThickForwardNeck',[(0,.01,1.62,.18,.14),(0,-.015,1.81,.19,.17),(0,-.025,1.98,.18,.16)],'Z',0)
shaped('WholeBroadBullHeadAndDescendingMuzzle',[(0,.12,2.04,.12,.15),(0,-.02,2.08,.23,.22),(0,-.18,2.04,.25,.22),(0,-.35,1.98,.20,.17),(0,-.49,1.91,.22,.115),(0,-.56,1.91,.17,.085)],'Y',0,16,[0,0,0,0,2])
for sg,side in[(-1,'Left'),(1,'Right')]:
 shaped(side+'WholeBentLeg',[(sg*.15,.01,.97,.15,.15),(sg*.20,-.02,.72,.12,.12),(sg*.22,.10,.43,.082,.09),(sg*.23,.02,.18,.070,.075),(sg*.23,.00,.10,.075,.075)],'Z',0,12)
 # A complete hoof with real front cleft, not a painted line or two floating toes.
 p=[(-.13,-.16),(-.025,-.16),(-.015,-.05),(.015,-.05),(.025,-.16),(.13,-.16),(.13,.08),(-.13,.08)]
 pad(side+'WholeCleftHoof',p,0,.145,2);v,f,m=G[side+'WholeCleftHoof'];G[side+'WholeCleftHoof']=([(sg*.23+x,z,y)for x,y,z in v],[(a,c,b)for a,b,c in f],m)
 shaped(side+'WholeLongBentArm',[(sg*.36,0,1.57,.15,.16),(sg*.51,.02,1.39,.135,.14),(sg*.58,.035,1.18,.105,.11),(sg*.59,-.12,.99,.075,.085),(sg*.59,-.15,.94,.068,.074)],'Z',0,12)
 shaped(side+'WholeBluntHand',[(sg*.59,-.15,1.00,.069,.073),(sg*.60,-.18,.90,.09,.08),(sg*.60,-.19,.81,.077,.065),(sg*.59,-.19,.775,.045,.045)],'Z',0,10)
 # Whole tapered side ear on a horizontal long axis.
 shaped(side+'WholeEar',[(sg*.18,.005,2.075,.05,.06),(sg*.34,.035,2.07,.11,.055),(sg*.44,.045,2.08,.015,.018)],'X',0,10)
 # Fixed Y section frame on this near-XZ curved horn avoids frame flips.
 pts=[(sg*.18,-.03,2.18,.066),(sg*.34,-.015,2.25,.062),(sg*.49,-.035,2.35,.046),(sg*.56,-.10,2.47,.026),(sg*.55,-.19,2.54,.005)];v=[];f=[];nn=10
 for k,(x,y,z,r)in enumerate(pts):
  aa=pts[max(0,k-1)];bb=pts[min(len(pts)-1,k+1)];dx=bb[0]-aa[0];dz=bb[2]-aa[2];le=math.hypot(dx,dz);u=(0,1,0);w=(-dz/le,0,dx/le)
  for j in range(nn):a=math.tau*j/nn;v.append((x+r*w[0]*math.sin(a),y+r*math.cos(a),z+r*w[2]*math.sin(a)))
 for k in range(len(pts)-1):
  for j in range(nn):a=k*nn+j;b=k*nn+(j+1)%nn;c=b+nn;d=a+nn;f.extend([(a,b,c),(a,c,d)])
 for k in[0,len(pts)-1]:
  center=len(v);v.append(pts[k][:3])
  for j in range(nn):f.append((center,k*nn+(j+1)%nn,k*nn+j)if k==0 else(center,k*nn+j,k*nn+(j+1)%nn))
 record(side+'WholeOutwardUpturnedHorn',v,f,1)
 shaped(side+'WholeSeatedDarkEye',[(sg*.195,-.25,2.105,.027,.024),(sg*.195,-.275,2.105,.022,.019),(sg*.195,-.285,2.105,.010,.010)],'Y',2,10)
shaped('WholeShortHangingTail',[(0,.16,1.02,.045,.045),(0,.29,.87,.035,.04),(.035,.36,.67,.028,.035),(.07,.34,.52,.055,.06),(.09,.30,.45,.02,.025)],'Z',0,10,[0,0,2,2])
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
for n,(v,f,m)in G.items():FM.setdefault(n,[m]*len(f))
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
focus=Vector((0,0,1.27))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.25;aim(cam,(4.5,-8,3.7));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/fantasy/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'fantasy','style':'S01-clean-geometric','title':'Static Bull Head and Two Hoof Minotaur','description':'One independently authored whole static minotaur-inspired fantasy character: a broad upright chest and covered hip stand above two bent legs ending in whole actually cleft hooves. Two long relaxed arms end in blunt stylized hands. A thick neck carries a complete broad bull-like head with descending blunt dark muzzle, lateral ears, two full curved outward-upturned horns and seated dark eyes. A short hanging tail has a widened dark tip. All proportions, sections and limb paths are newly drawn as one coherent bipedal fantasy figure, not an extracted cow head pasted onto an old person or a recoloured centaur with two legs removed. Three opaque PBR materials, metres, Z up, full horizontal envelope centred at the two finite hoof soles. Integral dark lower-torso wrap covers the hips; no weapons or extra costume props. Static fictional art only, not anatomical realism, gait, strength, behavioral or safety functionality. Fine articulated fingers, rigging, animation, interaction and collision are not produced or verified and are outside delivery.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
