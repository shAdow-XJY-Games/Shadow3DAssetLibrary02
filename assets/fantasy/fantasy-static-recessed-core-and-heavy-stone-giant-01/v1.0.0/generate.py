import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='fantasy-static-recessed-core-and-heavy-stone-giant-01'
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
PALETTE=[('WholeGiantWeatheredBlueStone',(.24,.29,.30,1),.96,0),('WholeGiantWarmStoneEdges',(.38,.34,.26,1),.95,0),('WholeGiantDarkTealCoreAndRecess',(.045,.15,.14,1),.80,.08)]
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

# Broad continuous angular torso; chest recess is part of its front boundary, not an overlay.
rows=[(.77,.29,.23),(1.02,.42,.28),(1.18,.56,.33),(1.22,.61,.35),(1.53,.65,.35),(1.57,.64,.34),(1.76,.57,.31),(1.88,.42,.25)]
v=[];f=[];n=12
for k,(z,rx,ry)in enumerate(rows):
 for j in range(n):
  t=math.tau*j/n;x=rx*math.cos(t);y=ry*math.sin(t)
  if k in[3,4] and j in[8,9,10]:y+=.18
  v.append((x+.025*math.sin(z*5),y,z))
for k in range(len(rows)-1):
 for j in range(n):a=k*n+j;b=k*n+(j+1)%n;f.extend([(a,b,b+n),(a,b+n,a+n)])
for k in[0,len(rows)-1]:
 c=len(v);v.append((.025*math.sin(rows[k][0]*5),0,rows[k][0]))
 for j in range(n):f.append((c,k*n+(j+1)%n,k*n+j)if k==0 else(c,k*n+j,k*n+(j+1)%n))
record('WholeAngularShoulderTorsoAndRecessedChest',v,f,0)
# Small opaque faceted stone core is rooted into the recessed chest floor, not glowing or floating.
shaped('WholeEmbeddedFacetedStoneCore',[(0,-.12,1.25,.035,.025),(0,-.15,1.34,.12,.10),(0,-.15,1.44,.11,.10),(0,-.12,1.51,.025,.025)],'Z',2,6)
# Full blunt block-like head with two true shallow eye recesses and an actual narrow mouth recess.
xs=[-.26,-.19,-.13,-.06,.06,.13,.19,.26];ys=[-.28,-.22,.20];zs=[1.83,1.99,2.025,2.11,2.16,2.29];cells=[]
for i in range(len(xs)-1):
 for j in range(2):
  for k in range(len(zs)-1):
   midx=(xs[i]+xs[i+1])/2
   if j==0 and ((k==3 and .06<abs(midx)<.19)or(k==1 and abs(midx)<.13)):continue
   cells.append([(x,y,z)for z in[zs[k],zs[k+1]]for y in[ys[j],ys[j+1]]for x in[xs[i],xs[i+1]]])
cell_union('WholeHeavyRecessedFaceStoneHead',cells,0)
v,f,m=G.pop('WholeHeavyRecessedFaceStoneHead');v=[(x*(.88+.12*math.sin(math.pi*(z-1.83)/.46)),y+.015*abs(x)/.26,z)for x,y,z in v];record('WholeHeavyRecessedFaceStoneHead',v,f,m)
FM['WholeHeavyRecessedFaceStoneHead']=[2 if sum(v[j][1]for j in t)/3<-.19 and ((2.11<sum(v[j][2]for j in t)/3<2.16)or(1.99<sum(v[j][2]for j in t)/3<2.025)) else 0 for t in f]
for sg,side in[(-1,'Left'),(1,'Right')]:
 shaped(side+'WholeAngularHipAndThigh',[(sg*.31,.025,.30,.19,.18),(sg*.34,.015,.46,.23,.21),(sg*.28,0,.76,.22,.22),(sg*.24,.015,.91,.16,.16)],'Z',0,7)
 shaped(side+'WholeLowerStoneLeg',[(sg*.35,-.045,.12,.15,.15),(sg*.37,-.02,.29,.19,.18),(sg*.34,.015,.44,.18,.17)],'Z',1,7)
 shaped(side+'WholeBroadFlatStoneFoot',[(sg*.35,-.16,0,.24,.34),(sg*.35,-.16,.13,.27,.36),(sg*.35,-.10,.23,.18,.25)],'Z',0,8)
 dz=.055 if sg>0 else 0
 shaped(side+'WholeShoulderBoulder',[(sg*.54,0,1.40+dz,.19,.20),(sg*.64,0,1.60+dz,.29,.28),(sg*.59,.01,1.79+dz,.22,.22),(sg*.52,.02,1.84+dz,.08,.09)],'Z',1,7)
 shaped(side+'WholeMassiveUpperArm',[(sg*.82,-.025,1.03+dz,.17,.19),(sg*.79,.01,1.24+dz,.22,.21),(sg*.67,.02,1.55+dz,.20,.21)],'Z',0,7)
 shaped(side+'WholeMassiveLowerArm',[(sg*.94,-.16,.69+dz,.17,.18),(sg*.96,-.12,.83+dz,.24,.23),(sg*.86,-.015,1.12+dz,.19,.19)],'Z',1,7)
 shaped(side+'WholeBroadStonePalm',[(sg*.96,-.19,.45+dz,.19,.17),(sg*.98,-.20,.62+dz,.25,.20),(sg*.94,-.16,.81+dz,.19,.16)],'Z',0,7)
 for j in[-1,0,1]:
  x=sg*.98+j*.13
  shaped(side+'WholeBluntStoneFinger'+str(j),[(x,-.27,.37+dz,.052,.055),(x,-.29,.44+dz,.063,.075),(x,-.23,.62+dz,.06,.075)],'Z',0,6)
 shaped(side+'WholeBentStoneThumb',[(sg*.79,-.18,.52+dz,.075,.07),(sg*.74,-.22,.62+dz,.08,.08),(sg*.82,-.16,.72+dz,.08,.075)],'Z',0,6)
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
focus=Vector((0,0,1.14))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.0;aim(cam,(3,-8,3.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/fantasy/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'characters','assetKind':'character','theme':'fantasy','style':'S01-clean-geometric','title':'Static Recessed Core and Heavy Stone Giant','description':'One complete newly authored fictional stone-giant character in a fixed grounded pose. A broad continuous faceted shoulder torso has an actual front chest recess containing one rooted opaque angular stone core. Its heavy blunt head has two genuinely recessed eye bands and a small recessed mouth. Two squat separated hip/leg stacks terminate in broad full flat stone feet; asymmetrically raised shoulder boulders join massive angular upper and lower arms, broad palms, three separated blunt fingers and one bent thumb per hand. These are whole newly shaped irregular stone masses, not a human worker recoloured, a narrow open-waist plate robot with a rock texture, or a treefolk trunk with its branches shortened. No external pins, steel axles, claw-only hands, control strings, bark crown or imported body meshes. Three opaque constant PBR roles, metres Z-up and full horizontal-bounds-centred ground origin. One static fantasy character zero scenes. The core is an opaque stone accent, not a light or power system. No anatomy accuracy, sentience, walking, joint operation, balance, structural/load strength, rigging, animation, combat, physics or interaction is supplied or validated.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
