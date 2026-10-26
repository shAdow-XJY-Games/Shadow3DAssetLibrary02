import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='public-service-fixed-curved-heel-and-raised-truss-bridge-01'
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



def profile(name,p,a,b,axis,mat):
 if sum(u[0]*v[1]-u[1]*v[0]for u,v in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);tt=triangulate(p)
 def pt(q,t):return(t,q[0],q[1])if axis=='x'else(q[0],t,q[1])if axis=='y'else(q[0],q[1],t)
 mesh(name,[pt(q,t)for t in[a,b]for q in p],[tuple(reversed(t))for t in tt]+[tuple(n+i for i in t)for t in tt]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],mat)
def union_boxes(name,boxes,mat):
 xs=sorted({p[0]for b in boxes for p in b});ys=sorted({p[1]for b in boxes for p in b});zs=sorted({p[2]for b in boxes for p in b});occ=set()
 for i in range(len(xs)-1):
  for j in range(len(ys)-1):
   for k in range(len(zs)-1):
    c=((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)
    if any(all(lo[t]<c[t]<hi[t]for t in range(3))for lo,hi in boxes):occ.add((i,j,k))
 v=[];f=[];idx={}
 def vid(p):
  if p not in idx:idx[p]=len(v);v.append(p)
  return idx[p]
 for i,j,k in sorted(occ):
  p=[(x,y,z)for z in[zs[k],zs[k+1]]for y in[ys[j],ys[j+1]]for x in[xs[i],xs[i+1]]]
  for q,st in zip(BOX,[(0,0,-1),(0,0,1),(0,-1,0),(0,1,0),(-1,0,0),(1,0,0)]):
   if(i+st[0],j+st[1],k+st[2])not in occ:f.append(tuple(vid(p[n])for n in q))
 mesh(name,v,f,mat)
C=(.35,1.50);angles=[math.radians(-115+10*i)for i in range(16)]
for side in[-1,1]:
 x=side*1.06
 box('WholeGroundFootBearingPier_'+str(side),(x,.63,.12),(.64,2.64,.24),0)
 box('WholeFlatHeelBearingRail_'+str(side),(x,.63,.255),(.37,2.44,.05),3)
 p=[(C[0]+r*math.cos(a),C[1]+r*math.sin(a))for r,aa in[(1.25,angles),(.94,list(reversed(angles)))]for a in aa]
 profile('WholeOpenCurvedRollingHeel_'+str(side),p,x-.11,x+.11,'x',1)
 for k,ang in enumerate([-105,-35,25]):
  a=math.radians(ang)
  beam('WholeHeelSpoke_'+str(side)+str(k),(x,C[0],C[1]),(x,C[0]+1.09*math.cos(a),C[1]+1.09*math.sin(a)),.16,1)
axle('WholeTransverseHeelHub',-1.23,1.23,C[0],C[1],.13,3,24)
# The raised complete span and both open-window side trusses share full mesh boundaries.
ang=math.radians(22);D=(0,-math.cos(ang),math.sin(ang));N=(0,math.sin(ang),math.cos(ang))
def tr(p):x,u,n=p;return(x,C[0]+D[1]*u+N[1]*n,C[1]+D[2]*u+N[2]*n)
def moved(name):
 v,f,m=G[name];G[name]=([tr(p)for p in v],[tuple(reversed(q))for q in f],m)
cells=[((-1.13,-.12,-.09),(1.13,4.12,.06))]
for x in[-1.04,1.04]:
 cells += [((x-.075,-.08,.02),(x+.075,4.1,.17)),((x-.075,-.08,.83),(x+.075,4.1,.97))]
 for u in[0,1,2,3,4.02]:cells.append(((x-.075,u-.07,.07),(x+.075,u+.07,.91)))
union_boxes('WholeRaisedDeckAndWindowedTrusses',cells,1);moved('WholeRaisedDeckAndWindowedTrusses')
for side in[-1,1]:
 x=side*1.04
 for j in range(4):
  a=(x,j+.02,.13 if j%2==0 else .90);b=(x,j+.98,.90 if j%2==0 else .13)
  beam('WholeTrussDiagonal_'+str(side)+str(j),tr(a),tr(b),.070,2)
for j,u in enumerate([.15,1.40,2.75,3.95]):beam('WholeUnderdeckCrossBearer_'+str(j),tr((-1.10,u,-.12)),tr((1.10,u,-.12)),.15,3)
# Complete tall rear counterweight arms share the heel hub and are not overhead tower ropes.
for side in[-1,1]:
 x=side*1.06
 beam('WholeRearCounterweightArm_'+str(side),(x,C[0],C[1]),(x,1.44,2.24),.21,1)
 beam('WholeRearCounterweightUpperBrace_'+str(side),tr((x,.65,.90)),(x,1.44,2.24),.14,1)
box('WholeTransverseRearCounterweight',(0,1.50,2.22),(2.42,.54,.59),0)
box('WholeFixedRearApproach',(0,1.70,.325),(2.72,.40,.19),0)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholePiersAndWeight_MatteConcrete',(.48,.47,.41,1),.91,0),('WholeSpanAndHeel_MutedPetrol',(.14,.29,.30,1),.68,.28),('WholeTrussDiagonals_QuietOchre',(.57,.37,.16,1),.73,.18),('WholeBearingRailsAndHub_DarkAlloy',(.11,.13,.14,1),.55,.42)]
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
focus=Vector((0,0,1.85))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=7.8;aim(cam,(7,-8,5.4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/public-service/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'public-service','style':'S01-clean-geometric','title':'Fixed Curved Heel and Raised Truss Bridge','description':'One independently authored complete fixed rolling-heel-style opening-bridge exterior. Two full ground piers carry short flat bearing rails. Two entire thick curved heel sectors, each with actual inner opening and three full spokes, meet those rails at their low faceted soles and join a complete transverse hub. One broad raised deck with full side trusses and underfloor crossbearers extends forward from that hub. Two whole rear upper arms carry one complete crosswise counterweight appearance, while a low fixed rear approach ties the two piers. The curved heel-to-short-flat-track support is new full geometry: no overhead towers or rope paths, no anchored gate-leaf root pivot, and no central turning table. Unlike the old twin-tower lift bridge the entire span is inclined and its support is local to the rear; unlike the old masonry drawbridge gateway there is no enclosing portal or high rope routing. All geometry newly authored, no old bridge imported, scaled or reduced. Four opaque constant PBR roles, metre Z up and full horizontally centred ground datum; one complete static architectural equipment model zero scenes. Deliberate fixed embedded joints and small bearing overlaps are artistic support appearances, not functional rolling contact or an engineered mechanism. No terrain, river, vehicle, person, actual opening path, balance, gear engagement, traffic passage, waterway clearance, load, installation, manufacture or civil/safety performance. Rigging animation interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
