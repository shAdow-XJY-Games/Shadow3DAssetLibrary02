import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='regional-fixed-cutaway-conical-vault-and-deep-storage-pit-01'
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
PALETTE=[('WholeBelowGradePitAndCutSectionEarth',(.43,.31,.20,1),.96,0),('WholeThickConicalVaultWarmPlaster',(.66,.52,.34,1),.94,0),('WholeEntranceAndDescendingStairPaleStone',(.65,.61,.48,1),.92,0)]
FM={}
# A full-thickness 270-degree architectural section, not an intact building disguised as a functioning one.
def section_sweep(name,profile,mat,entry=False):
 v=[];f=[];ix={};N=54;loops=[]
 def vv(p):
  p=tuple(round(x,11)for x in p)
  if p not in ix:ix[p]=len(v);v.append(p)
  return ix[p]
 for k in range(N+1):
  a=-math.pi/4+1.5*math.pi*k/N;dh=1.22*max(0,min(1,(.27-abs(a-math.pi))/.06)) if entry else 0
  row=[]
  for r,z in profile:
   zz=z+dh*max(0,(3.4-z)/(3.4-2.05)) if entry else z
   row.append(vv((r*math.cos(a),r*math.sin(a),zz)))
  loops.append(row)
 def face(ids):
  q=[]
  for i in ids:
   if i not in q:q.append(i)
  for j in range(1,len(q)-1):f.append((q[0],q[j],q[j+1]))
 for k in range(N):
  for j in range(len(profile)):
   jj=(j+1)%len(profile);face([loops[k][j],loops[k+1][j],loops[k+1][jj],loops[k][jj]])
 pp=profile
 if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(pp,pp[1:]+pp[:1]))<0:pp=list(reversed(pp));rev=True
 else:rev=False
 tris=earclip(pp)
 for row in[loops[0],loops[-1]]:
  rr=list(reversed(row))if rev else row
  for a,b,c in tris:f.append((rr[a],rr[b],rr[c]))
 # Orient whole connected surface consistently; cap directions must agree with the side sweep.
 from collections import defaultdict
 ed=defaultdict(list)
 for k,t in enumerate(f):
  for a,b in zip(t,t[1:]+t[:1]):ed[tuple(sorted((a,b)))].append((k,a,b))
 signs={0:1};todo=[0]
 while todo:
  i=todo.pop()
  for a,b in zip(f[i],f[i][1:]+f[i][:1]):
   for j,c,d in ed[tuple(sorted((a,b)))]:
    if j==i:continue
    wanted=signs[i]*(-1 if(a,b)==(c,d)else 1)
    if j in signs:assert signs[j]==wanted
    else:signs[j]=wanted;todo.append(j)
 assert len(signs)==len(f)
 f=[t if signs[k]>0 else(t[0],t[2],t[1])for k,t in enumerate(f)];record(name,v,f,mat)
# Deep circular blind pit is inside the below-grade retaining mass, with a full upper access ledge.
section_sweep('WholeCutawayRetainingMassLedgeAndDeepPit',[(0,0),(3.60,0),(3.60,2.10),(2.18,2.10),(2.18,.25),(0,.25)],0)
# New tapering thick vault with a real narrow top throat and a low side entry cut in its lower wall.
profile=[(3.20,2.05),(3.16,2.65),(2.94,3.30),(2.56,4.00),(2.04,4.65),(1.42,5.25),(.66,5.85),(.25,6.12),(.18,6.12),(.18,5.93),(.48,5.65),(1.18,5.05),(1.77,4.47),(2.26,3.85),(2.61,3.20),(2.84,2.60),(2.86,2.05)]
section_sweep('WholeThickTaperedVaultAndTopThroat',profile,1,True)
# The short low vaulted entrance meets the real side opening at the upper ledge, not the pit floor.
p=[(-.62,2.04),(-.62,2.56)]+[(.62*math.cos(math.pi-j*math.pi/16),2.56+.62*math.sin(math.pi-j*math.pi/16))for j in range(1,17)]+[(.62,2.04),(.46,2.04),(.46,2.56)]+[(.46*math.cos(j*math.pi/16),2.56+.46*math.sin(j*math.pi/16))for j in range(1,17)]+[(-.46,2.04)]
pad('WholeLowArchedEntranceVestibule',p,-4.65,-2.70,2);v,f,m=G.pop('WholeLowArchedEntranceVestibule');record('WholeLowArchedEntranceVestibule',[(y,x,z)for x,y,z in v],f,m)
box('WholeEntranceFoundationAndLevelThreshold',(-4.72,-.72,0),(-2.70,.72,2.07),0)
# One complete descending stair solid joins the high ledge to the dry pit base, not a ladder on the dome.
p=[(-2.24,.24),(-.35,.24)]
for k in reversed(range(7)):
 x=-2.24+.27*k;z=2.08-.235*k;p.extend([(x+.27,z),(x,z)])
pad('WholeDescendingInteriorStorageStair',p,-.40,.40,2)
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
focus=Vector((0,0,2.80))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=10.8;aim(cam,(7,-12,9.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/regional/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'modular','theme':'regional','style':'S01-clean-geometric','title':'Fixed Cutaway Conical Vault and Deep Storage Pit','description':'One newly authored complete static regional icehouse-inspired architectural section. A deliberately removed front quarter exposes a deep blind circular storage pit within a thick retaining mass, an upper perimeter access ledge, and one whole stair descending from that ledge into the dry pit. Above it, a full-thickness tapering vault rises to a genuinely open narrow top throat. A low arched side vestibule passes through a real raised opening in the vault base and meets the upper ledge rather than the pit floor. The retained vault and retaining mass each close their visible finite section faces; the cut is a presentation choice, not an unfinished hole. Unlike the old hollow straw skep there is a below-grade pit with a separate high entry datum, and unlike the open sunken stepwell the pit is enclosed by a thick tapering overhead vault and side-entry throat. All geometry newly authored together, no old cover, stair, well or building meshes imported. Three opaque constant PBR roles, metres Z up with the lowest foundation on the origin ground, one architectural module zero scenes. Dry stylized game exhibit only, not a historically exact building. No ice, water, external terrain, real cooling, thermal insulation, airflow, storage performance, drainage, human access, structural thrust, load, construction or engineering safety capability. Rigging animation interaction not made or verified.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
