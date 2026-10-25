import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='music-fixed-perforated-windchest-and-cluster-pipe-mouth-organ-01'
G={};FM={}
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def unit(a):return tuple(x/math.sqrt(dot(a,a))for x in a)
def mesh(name,v,faces,mat):
 f=[]
 for p in faces:
  for k in range(1,len(p)-1):f.append((p[0],p[k],p[k+1]))
 if sum(dot(v[a],cross(v[b],v[c]))for a,b,c in f)<0:f=[tuple(reversed(p))for p in f]
 G[name]=(v,f,mat)
BOX=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(name,c,size,mat):mesh(name,[tuple(c[i]+s[i]*size[i]/2 for i in range(3))for s in[(x,y,z)for z in[-1,1]for y in[-1,1]for x in[-1,1]]],BOX,mat)
def beam(name,a,b,width,mat):
 w=unit(sub(b,a));u=unit(cross(w,(1,0,0)if abs(w[0])<.9 else(0,1,0)));v=cross(w,u)
 mesh(name,[tuple(p[i]+width/2*(sx*u[i]+sy*v[i])for i in range(3))for p in[a,b]for sy in[-1,1]for sx in[-1,1]],BOX,mat)
def axle(name,x0,x1,y,z,r,mat,n=16):
 v=[(x,y+r*math.cos(math.tau*i/n),z+r*math.sin(math.tau*i/n))for x in[x0,x1]for i in range(n)]
 mesh(name,v,[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],mat)

def ringx(name,x0,x1,y,z,ri,ro,mat,n=24):
 v=[(x,y+r*math.cos(math.tau*i/n),z+r*math.sin(math.tau*i/n))for x in[x0,x1]for r in[ri,ro]for i in range(n)];f=[]
 for i in range(n):j=(i+1)%n;f.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 mesh(name,v,f,mat)
def cyly(name,y0,y1,x,z,r,mat,n=24):
 axle(name,y0,y1,x,z,r,mat,n);v,f,m=G[name];G[name]=([(b,a,c)for a,b,c in v],[tuple(reversed(p))for p in f],m)
def ringy(name,y0,y1,x,z,ri,ro,mat,n=24):
 ringx(name,y0,y1,x,z,ri,ro,mat,n);v,f,m=G[name];G[name]=([(b,a,c)for a,b,c in v],[tuple(reversed(p))for p in f],m)
def triangulate(p):
 def cr(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 ids=list(range(len(p)));out=[]
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:ids.reverse()
 while len(ids)>3:
  for k,b in enumerate(ids):
   a,c=ids[k-1],ids[(k+1)%len(ids)]
   if cr(p[a],p[b],p[c])<=1e-14:continue
   if any(min(cr(p[a],p[b],p[j]),cr(p[b],p[c],p[j]),cr(p[c],p[a],p[j]))>=-1e-14 for j in ids if j not in[a,b,c]):continue
   out.append((a,b,c));ids.pop(k);break
  else:raise AssertionError('bad polygon')
 return out+[tuple(ids)]
def lathe_z(name,x,y,profile,mat,n=24):
 v=[];rings=[];f=[]
 for r,z in profile:
  ids=[]
  if r==0:ids=[len(v)];v.append((x,y,z))
  else:
   for i in range(n):ids.append(len(v));v.append((x+r*math.cos(math.tau*i/n),y+r*math.sin(math.tau*i/n),z))
  rings.append(ids)
 for a,b in zip(rings,rings[1:]+rings[:1]):
  if len(a)==len(b)==1:continue
  for i in range(n):
   j=(i+1)%n
   if len(a)==1:f.append((a[0],b[j],b[i]))
   elif len(b)==1:f.append((a[i],a[j],b[0]))
   else:f.append((a[i],a[j],b[j],b[i]))
 mesh(name,v,f,mat)



# Complete new windchest, perforated socket lid and full clustered pipes.
W=.094;D=.0705
outer=[(-W+.002,-D+.002),(W-.002,-D+.002),(W-.002,D-.002),(-W+.002,D-.002)];inner=[(-W+.007,-D+.007),(W-.007,-D+.007),(W-.007,D-.007),(-W+.007,D-.007)]
v=[(x,y,z)for p,z in[(outer,0),(outer,.127),(inner,.010),(inner,.127)]for x,y in p];f=[(3,2,1,0),(8,9,10,11)]
for i in range(4):j=(i+1)%4;f.extend([(i,j,4+j,4+i),(8+i,12+i,12+j,8+j),(4+i,4+j,12+j,12+i)])
mesh('WholeGroundFootHollowWindchest',v,f,0)
# One welded thick socket lid: cell annuli share their exact common edges.
v=[];f=[];index={}
def vp(p):
 p=tuple(round(x,10)for x in p)
 if p not in index:index[p]=len(v);v.append(p)
 return index[p]
def quad(points):f.append(tuple(vp(p)for p in points))
centres=[]
for row in range(3):
 for col in range(4):
  x=(col-1.5)*.047;y=(row-1)*.047;centres.append((x,y,row,col));h=.0235
  rect=[(-h,-h),(0,-h),(h,-h),(h,0),(h,h),(0,h),(-h,h),(-h,0)]
  out=[(x+a,y+b)for a,b in rect];ins=[(x+.016*math.cos(-3*math.pi/4+math.tau*i/8),y+.016*math.sin(-3*math.pi/4+math.tau*i/8))for i in range(8)]
  for i in range(8):
   j=(i+1)%8;a,b=out[i],out[j];c,d=ins[i],ins[j]
   quad([(a[0],a[1],.136),(b[0],b[1],.136),(d[0],d[1],.136),(c[0],c[1],.136)])
   quad([(b[0],b[1],.122),(a[0],a[1],.122),(c[0],c[1],.122),(d[0],d[1],.122)])
   quad([(c[0],c[1],.136),(d[0],d[1],.136),(d[0],d[1],.122),(c[0],c[1],.122)])
   if any(abs(a[k]-lim)<1e-9 and abs(b[k]-lim)<1e-9 for k,lim in[(0,-W),(0,W),(1,-D),(1,D)]):quad([(a[0],a[1],.122),(b[0],b[1],.122),(b[0],b[1],.136),(a[0],a[1],.136)])
mesh('WholeTwelveSocketThickLid',v,f,1)
heights=[[.47,.40,.43,.50],[.63,.55,.59,.66],[.79,.72,.74,.81]]
for x,y,row,col in centres:
 n=16;v=[];f=[]
 def pr(r,z):
  ids=[]
  for i in range(n):ids.append(len(v));v.append((x+r*math.cos(math.tau*i/n),y+r*math.sin(math.tau*i/n),z))
  return ids
 h=heights[row][col];o=[pr(.0167,z)for z in[.108,.163,.184,h]];a=[pr(.0128,z)for z in[.114,.163,.184,h]]
 f=[tuple(reversed(o[0])),tuple(a[0])]
 for k in range(3):
  for i in range(n):
   if k==1 and i in[11,12]:continue
   j=(i+1)%n;f.extend([(o[k][i],o[k][j],o[k+1][j],o[k+1][i]),(a[k][j],a[k][i],a[k+1][i],a[k+1][j])])
 for i in range(n):j=(i+1)%n;f.append((o[-1][i],o[-1][j],a[-1][j],a[-1][i]))
 for i in[11,12]:
  j=(i+1)%n;f.extend([(o[1][j],a[1][j],a[1][i],o[1][i]),(o[2][i],a[2][i],a[2][j],o[2][j])])
 f.extend([(a[1][11],a[2][11],o[2][11],o[1][11]),(o[1][13],o[2][13],a[2][13],a[1][13])])
 name='WholeOpenTopAndFingerPortPipe_%d_%d'%(row,col);mesh(name,v,f,2)
# One true open-ended mouth branch; buried root stops at the chest wall, no airflow assertion.
path=[(0,-.063,.070),(0,-.100,.070),(0,-.130,.082),(0,-.156,.111),(0,-.179,.156),(0,-.201,.192),(0,-.225,.205)]
v=[];f=[];n=16
for k,p in enumerate(path):
 a=path[max(0,k-1)];b=path[min(len(path)-1,k+1)];t=unit(sub(b,a));u=(1,0,0);w=cross(t,u)
 for r in[.0125,.008]:
  for j in range(n):v.append(tuple(p[i]+r*(u[i]*math.cos(math.tau*j/n)+w[i]*math.sin(math.tau*j/n))for i in range(3)))
for k in range(len(path)-1):
 for j in range(n):q=(j+1)%n;a=2*n*k+j;b=2*n*k+q;c=2*n*(k+1)+j;d=2*n*(k+1)+q;f.extend([(a,b,d,c),(a+n,c+n,d+n,b+n)])
for j in range(n):q=(j+1)%n;k=(len(path)-1)*2*n;f.extend([(q,j,j+n,q+n),(k+j,k+q,k+q+n,k+j+n)])
mesh('WholeCurvedOpenMouthBranch',v,f,3)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeWindchest_DarkRedWood',(.31,.065,.035,1),.72,0),('WholePiercedLid_DarkWood',(.18,.085,.030,1),.76,0),('WholePipes_MutedBamboo',(.61,.43,.21,1),.73,0),('WholeMouthBranch_DullBrass',(.38,.29,.14,1),.52,.45)]
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
for prefix in []:
 parent=bpy.data.objects.new(prefix+'_CompleteSourceAssembly',None);scene.collection.objects.link(parent)
 for o in parts:
  if o.name.startswith(prefix+'__'):o.parent=parent
 parent.select_set(True)
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
triangles=sum(len(f)for v,f,m in G.values())
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
(OUT/'qa-report.json').write_text(json.dumps({'asset':ASSET,'mesh_objects':len(G),'triangles':triangles,'materials':len(PALETTE),'new_independent_models':1,'new_scenes':0},indent=2))
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
focus=Vector((0,0,.39))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.02;aim(cam,(3,-5,3));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/music/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':'Fixed Pierced Windchest and Cluster Pipe Mouth Organ','description':'One newly authored complete static cluster-pipe mouth-organ appearance. A thick open-interior rectangular windchest with full flat bottom supports one separate thick lid with twelve actual through sockets. Twelve complete unequal-height thick-walled pipes penetrate those sockets in a three-dimensional four-by-three cluster; each pipe has a real open top, blind lower floor and real small forward side aperture. One continuous curved hollow mouth branch enters the chest front wall and ends in an open lip. The new whole windchest, pierced lid, clustered socketed pipes and curved mouth-branch topology is not a panflute pipe-count variant or a keyboard pipe-organ with its keyboard removed. No old component or full asset is extracted or transformed; ordinary mesh tools are reused. One whole model, zero scenes, four opaque PBR appearances, metre Z-up, horizontal bounds-centred ground origin. A generic sheng-inspired static art interpretation, not an exact historical or regional instrument. Interior branch and windchest communication, reeds, acoustic pitch, air supply, finger operation, performance, physical balance, manufacturing and safety are not built or validated. Fixed hidden socket/pipe and branch/wall overlaps represent display support, not airtight joints; no rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
