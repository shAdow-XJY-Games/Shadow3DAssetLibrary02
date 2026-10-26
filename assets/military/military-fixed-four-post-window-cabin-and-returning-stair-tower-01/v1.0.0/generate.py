import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='military-fixed-four-post-window-cabin-and-returning-stair-tower-01'
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
PALETTE=[('WholeWarmTimberTower',(.31,.23,.14,1),.78,.02),('WholeMutedOliveCabin',(.32,.38,.25,1),.78,.01),('WholeSlateRoofAndRails',(.12,.18,.19,1),.65,.13)]
FM={}
for x in [-.91,.91]:
 for y in [-.91,.91]:box('MainFootPost_%s_%s'%(x,y),(x-.11,y-.11,0),(x+.11,y+.11,3.64),0)
for side in [-1,1]:
 pipe('SideWholeDiagonal_'+str(side),[(side*.92,-.91,.35),(side*.92,.91,3.40)],.075,0,4)
pipe('RearWholeDiagonal',[(-.91,.92,.35),(.91,.92,3.40)],.075,0,4)
box('WholeCabinPlatform',(-1.16,-1.16,3.45),(1.16,1.16,3.62),0)
# One welded wall shell; real front doorway and three broad unglazed window openings.
xx=[-1,-.84,-.52,.52,.84,1];yy=xx;zz=[3.62,4.30,5.03,5.34];cc=[]
for i in range(5):
 for j in range(5):
  for k in range(3):
   if not(i in [0,4]or j in [0,4]):continue
   if j==0 and i==2 and k<2:continue
   if k==1 and((j==4 and i in [1,2,3])or(i in[0,4]and j in[1,2,3])):continue
   cc.append([(x,y,z)for z in[zz[k],zz[k+1]]for y in[yy[j],yy[j+1]]for x in[xx[i],xx[i+1]]])
cell_union('WholeWindowedCabinWithFrontEntry',cc,1)
pad('WholeThickPitchedRoof',[(-1.23,5.30),(0,5.92),(1.23,5.30),(1.23,5.44),(0,6.06),(-1.23,5.44)],-1.26,1.26,2)
# Returning two-flight external stair stays outside all tower braces.
for row,(x0,x1,reverse) in enumerate([(1.38,2.18,False),(2.34,3.14,True)]):
 for i in range(9):
  y=-1.80+i*.30 if not reverse else .60-i*.30
  z=(i+1)*.20+row*1.80
  box('WholeTread_%d_%02d'%(row,i),(x0,y,z-.09),(x1,y+.30,z),0)
 for x in [x0+.04,x1-.04]:
  p0=(x,-1.80,.08)if not reverse else(x,.90,1.75)
  p1=(x,.90,1.77)if not reverse else(x,-1.80,3.57)
  pipe('WholeStringer_%d_%s'%(row,x),[p0,p1],.075,0,4)
  pipe('WholeStairHandrail_%d_%s'%(row,x),[(p0[0],p0[1],p0[2]+.88),(p1[0],p1[1],p1[2]+.88)],.035,2)
  for t in [0,.5,1]:
   q=tuple(p0[k]*(1-t)+p1[k]*t for k in range(3));pipe('StairRailUpright_%d_%s_%s'%(row,x,t),[q,(q[0],q[1],q[2]+.88)],.028,2)
box('WholeMidTurnLanding',(1.30,.88,1.65),(3.22,1.55,1.81),0)
box('WholeTopEntryLanding',(-1.16,-2.36,3.45),(3.22,-1.16,3.62),0)
for x,y,h in [(1.38,1.43,1.7),(3.14,1.43,1.7),(3.14,-2.23,3.5),(-1.02,-2.23,3.5)]:
 box('LandingWholeSupport_%s_%s'%(x,y),(x-.07,y-.07,0),(x+.07,y+.07,h),0)
for name,a,b in [('Front',(-1.08,-2.27,4.42),(3.14,-2.27,4.42)),('Left',(-1.08,-2.27,4.42),(-1.08,-1.04,4.42)),('MidBack',(1.38,1.46,2.64),(3.14,1.46,2.64))]:
 pipe('LandingWholeRail_'+name,[a,b],.035,2)
 for t in [0,.5,1]:
  q=tuple(a[k]*(1-t)+b[k]*t for k in range(3));pipe('LandingUpright_'+name+str(t),[(q[0],q[1],q[2]-.86),q],.028,2)
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
focus=Vector((0,0,2.8))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=9.4;aim(cam,(10,-15,10));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/military/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'military','style':'S01-clean-geometric','title':'Fixed Four Post Window Cabin and Returning Stair Tower','description':'One independently authored complete fixed nonweapon camp observation tower visual model. Four complete ground posts and three diagonal braces carry a thick high floor and one continuous cabin wall shell with actual broad side and rear window voids and a front entry. A whole pitched thick roof caps the cabin. Outside the braced central tower, two independent opposite-running stair flights meet a full intermediate turning landing and reach a full upper entry landing beside the cabin front doorway. Complete stair stringers, rails, and landing supports remain part of this single whole structure. This is not the old elevated open lifeguard seat or the solid tapered lighthouse shaft and lantern gallery. All geometry newly authored, no old meshes imported. Three opaque PBR roles, metres Z up, bounds-centred ground origin. Fixed artistic architectural appearance only: no weapon, occupant, observation coverage, climbability, accessibility, load, stability, wind, military protection, building compliance or safety claim. Rigging animation and interaction not made or verified.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
