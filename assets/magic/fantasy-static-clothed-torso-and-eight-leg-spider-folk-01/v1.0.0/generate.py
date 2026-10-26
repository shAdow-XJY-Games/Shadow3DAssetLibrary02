import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='fantasy-static-clothed-torso-and-eight-leg-spider-folk-01'
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
PALETTE=[('WholeSpiderFolkCoveredTunic',(.12,.25,.24,1),.88,0),('WholeSpiderFolkFaceHands',(.52,.34,.22,1),.88,0),('WholeSpiderFolkCarapaceHairEyes',(.065,.075,.095,1),.87,0)]
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

# Entirely new arachnid lower body, narrow waist and broad high rear abdomen share one skin.
shaped('WholeLowFrontBodyWaistAndBroadAbdomen',[(0,-.64,.64,.07,.09),(0,-.52,.67,.22,.18),(0,-.30,.68,.29,.24),(0,-.06,.67,.26,.21),(0,.15,.66,.13,.13),(0,.32,.71,.24,.24),(0,.57,.79,.43,.36),(0,.80,.80,.47,.39),(0,1.02,.78,.31,.28),(0,1.15,.75,.07,.09)],'Y',2,16)
# Whole covered upright torso, narrow neck and adult-like head; no imported centaur torso.
shaped('WholeCoveredUprightTorsoNeckAndHead',[(0,-.37,.72,.20,.17),(0,-.37,.95,.21,.16),(0,-.38,1.13,.16,.13),(0,-.37,1.35,.23,.15),(0,-.36,1.52,.27,.15),(0,-.36,1.59,.095,.085),(0,-.36,1.67,.08,.075),(0,-.38,1.72,.12,.11),(0,-.37,1.83,.145,.13),(0,-.34,1.92,.12,.105),(0,-.33,1.98,.025,.028)],'Z',0,16,[0,0,0,0,0,1,1,1,2,2])
def arched_limb(name,points,radii):
 v=[];f=[];n=8
 for k,c in enumerate(points):
  t=unit(sub(points[min(k+1,len(points)-1)],points[max(0,k-1)]));u=unit((-t[1],t[0],0));w=cross(t,u)
  if k==len(points)-1:w=(u[1],-u[0],0)
  for i in range(n):
   a=math.tau*i/n;v.append(add(c,add(mul(u,radii[k][0]*math.cos(a)),mul(w,radii[k][1]*math.sin(a)))))
 for k in range(len(points)-1):
  for i in range(n):
   j=(i+1)%n;a=k*n+i;b=k*n+j;cc=(k+1)*n+j;d=(k+1)*n+i;f.extend([(a,b,cc),(a,cc,d)])
 for k in[0,len(points)-1]:
  c=len(v);v.append(points[k])
  for i in range(n):f.append((c,k*n+(i+1)%n,k*n+i)if k==0 else(c,k*n+i,k*n+(i+1)%n))
 record(name,v,f,2)
for sg,label in[(-1,'Left'),(1,'Right')]:
 paths=[[(.19,-.49,.67),(.58,-.80,.94),(.94,-1.18,.22),(1.02,-1.30,0)],[(.25,-.34,.69),(.74,-.43,1.00),(1.12,-.60,.20),(1.20,-.65,0)],[(.25,-.15,.67),(.76,.17,.98),(1.13,.40,.20),(1.20,.48,0)],[(.20,.015,.66),(.59,.52,.90),(.95,.94,.20),(1.03,1.04,0)]]
 for j,pts in enumerate(paths):arched_limb(label+'WholeArchedGroundLeg'+str(j),[(sg*x,y,z)for x,y,z in pts],[(.065,.075),(.070,.065),(.030,.035),(.024,.042)])
 shaped(label+'WholeCoveredBentArmAndHand',[(sg*.23,-.36,1.49,.075,.085),(sg*.37,-.38,1.36,.072,.075),(sg*.45,-.48,1.22,.055,.060),(sg*.46,-.62,1.10,.043,.047),(sg*.46,-.65,1.03,.060,.052),(sg*.46,-.65,.98,.036,.035)],'Z',0,12,[0,0,0,1,1])
 shaped(label+'WholeEmbeddedEye',[(sg*.063,-.481,1.817,.018,.015),(sg*.063,-.499,1.817,.012,.010),(sg*.063,-.503,1.817,.004,.005)],'Y',2,8)
shaped('WholeFiniteBluntNose',[(0,-.48,1.79,.028,.04),(0,-.535,1.77,.024,.026),(0,-.553,1.76,.009,.013)],'Y',1,8)
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
focus=Vector((0,0,.99))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.4;aim(cam,(5,-8,4.1));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/magic/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'magic','style':'S01-clean-geometric','title':'Static Clothed Torso and Eight Leg Spider Folk','description':'One wholly newly authored static spider-folk fantasy character. A complete low front arachnid body narrows through a continuous waist into a broad high rounded abdomen, while eight whole high-arched tapering jointed legs fan into separate finite ground tips. A newly drawn continuous fully covered upright torso, neck and human-like head rises from the front body; two complete bent sleeved arms end in blunt stylized hands. Hair and tunic roles are integral face regions; small embedded eyes and a finite blunt nose define the adult-like face. The complete radial arachnid leg/waist/abdomen and upright covered body organization is not a horse with more legs, a catalogue spider with a head attached, or an extracted centaur torso. Every body station, limb path and facial placement is new numeric geometry with no imported old meshes. Three opaque matte PBR roles, metres Z up, whole horizontal envelope centred on actual ground tips, one character prop zero scenes. No weapons, exposed intimate anatomy or extra costume props. Fictional fixed art only: no biological species, anatomical fidelity, gait, balance, poison, strength, rigging, animation, deformation, interaction, collision or safety capability.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
