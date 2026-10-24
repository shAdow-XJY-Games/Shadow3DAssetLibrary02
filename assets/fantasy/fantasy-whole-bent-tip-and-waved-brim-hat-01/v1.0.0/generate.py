import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='fantasy-whole-bent-tip-and-waved-brim-hat-01'
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

# One continuous thick waved brim and bent pointed crown, with a genuine open underside.
PALETTE=[('HatMutedPlum',(.22,.16,.27,1),.89,0),('HatBrownBand',(.22,.12,.065,1),.84,0),('HatOldGoldBuckle',(.63,.43,.13,1),.53,.50)]
SEG=32
path=[((0,0,.055),.155),((0,0,.14),.137),((.010,0,.25),.108),((.035,0,.345),.077),((.085,0,.415),.051),((.15,0,.445),.031),((.215,0,.425),.016),((.255,0,.385),0)]
def crownrings(inner=False):
 out=[]
 for k,(p,r)in enumerate(path):
  if inner and k==len(path)-1:p=(.244,0,.391)
  if k==0:tangent=(0,0,1)
  else:tangent=unit(sub(path[min(k+1,len(path)-1)][0],path[max(k-1,0)][0]))
  u=(0,1,0);w=unit(cross(tangent,u));rr=max(0,r-(.007 if inner else 0));pp=add(p,(0,0,-.008))if inner and k==0 else p
  if rr==0:out.append([pp])
  else:out.append([add(pp,add(mul(u,rr*math.cos(math.tau*i/SEG)),mul(w,rr*math.sin(math.tau*i/SEG))))for i in range(SEG)])
 return out
# Ring angular orientation follows first crown ring: (x,y)=(-r sin(a),r cos(a)).
def brim(lower=False):
 out=[]
 for i in range(SEG):
  a=math.tau*i/SEG;r=.34*(1+.055*math.sin(3*a));z=.036+.017*math.cos(2*a)+.009*math.sin(3*a)-(.010 if lower else 0);out.append((-r*math.sin(a),r*math.cos(a),z))
 return out
rings=[brim()]+crownrings()+list(reversed(crownrings(True)))+[brim(True)]
v=[];ix=[]
for ring in rings:ix.append(list(range(len(v),len(v)+len(ring))));v+=ring
f=[]
for a,b in zip(ix,ix[1:]+ix[:1]):
 if len(a)==len(b)==1:continue
 for i in range(SEG):
  j=(i+1)%SEG
  if len(a)==1:f.append((a[0],b[i],b[j]))
  elif len(b)==1:f.append((a[i],b[0],a[j]))
  else:f.extend([(a[i],b[i],b[j]),(a[i],b[j],a[j])])
record('WholeThickWavedBrimAndBentCrown',v,f,0)
# A finite continuous band follows the actual lower tapered crown.
pr=[(.071,.158),(.115,.149),(.115,.140),(.071,.149)];v=[(-r*math.sin(math.tau*i/SEG),r*math.cos(math.tau*i/SEG),z)for z,r in pr for i in range(SEG)];f=[]
for k in range(4):
 for i in range(SEG):j=(i+1)%SEG;a=k*SEG+i;b=k*SEG+j;c=((k+1)%4)*SEG+j;d=((k+1)%4)*SEG+i;f.extend([(a,b,c),(a,c,d)])
record('WholeTaperedClothBand',v,f,1)
# Solid hollow buckle with four full side walls, not a filled black square decal.
o=[(-.047,.072),(.047,.072),(.047,.119),(-.047,.119)];inn=[(-.030,.083),(.030,.083),(.030,.108),(-.030,.108)];v=[(x,y,z)for p,y in[(o,-.166),(o,-.146),(inn,-.146),(inn,-.166)]for x,z in p];f=[]
for k in range(4):
 for i in range(4):j=(i+1)%4;a=k*4+i;b=k*4+j;c=((k+1)%4)*4+j;d=((k+1)%4)*4+i;f.extend([(a,b,c),(a,c,d)])
record('WholeOpenRectangularBandBuckle',v,f,2)
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
focus=Vector((0,0,.22))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.86;aim(cam,(5,-8,4.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/fantasy/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'fantasy','style':'S01-clean-geometric','title':'Whole Bent Tip and Waved Brim Fantasy Hat','description':'One complete original fixed fantasy pointed hat: one shared-vertex closed material shell joins a broad unevenly waved brim to a tall tapering crown whose final tip curves sideways and downward. Explicit outer and inner crown surfaces leave the full underside head cavity open; the brim has finite edge thickness rather than a double-sided card. A whole tapered brown band and one genuinely hollow rectangular buckle complete the object. No head, wearer, stand, veil, feather, lettering or texture. Newly drawn continuous curved shell, not an enlarged beekeeping dome with its veil deleted or a party crown with more points. Three opaque constant PBR materials, metres and lowest brim datum, one model and zero scenes. Invented decorative costume appearance only: no wearer fit, cloth deformation, protective capability, historical/religious accuracy or magical effect claimed.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
