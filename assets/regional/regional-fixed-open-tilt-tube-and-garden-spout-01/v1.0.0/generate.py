import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='regional-fixed-open-tilt-tube-and-garden-spout-01'
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



def prismz(name,p,z0,z1,mat):
 n=len(p);v=[(x,y,z)for z in[z0,z1]for x,y in p];f=[]
 for a,b,c in triangulate(p):f +=[(c,b,a),(a+n,b+n,c+n)]
 f +=[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh(name,v,f,mat)
prismz('WholeGroundFootIrregularStoneBase',[(-.61,-.72),(.16,-.78),(.48,-.56),(.45,.63),(.22,.78),(-.30,.73),(-.54,.38)],0,.10,3)
angle=math.radians(13);w=(0,-math.cos(angle),math.sin(angle));u=(1,0,0);v0=cross(w,u);origin=(0,0,.66)
def local(t,r,a):return tuple(origin[k]+w[k]*t+r*(u[k]*math.cos(a)+v0[k]*math.sin(a))for k in range(3))
# Continuous thick body, deeply blind inside, oblique open front with real end reveals.
N=32;rows=[];verts=[]
for kind,t,r in [('back',-.55,0),('outerrear',-.55,.088),('outermouth',.65,.088),('innermouth',.65,.064),('innerrear',-.32,.064),('blind',-.32,0)]:
 ids=[]
 for j in range(1 if r==0 else N):
  a=math.tau*j/N;tt=t-.9*r*math.sin(a)if 'mouth'in kind else t;ids.append(len(verts));verts.append(local(tt,r,a))
 rows.append(ids)
faces=[]
for aa,bb in zip(rows,rows[1:]+rows[:1]):
 if len(aa)==len(bb)==1:continue
 for j in range(N):
  k=(j+1)%N
  if len(aa)==1:faces.append((aa[0],bb[k],bb[j]))
  elif len(bb)==1:faces.append((aa[j],aa[k],bb[0]))
  else:faces.append((aa[j],aa[k],bb[k],bb[j]))
mesh('WholeClosedRearAndObliqueOpenTiltTube',verts,faces,0)
for k,t in enumerate([-.40,.27]):
 vs=[local(tt,r,math.tau*j/24)for tt,r in[(t-.016,.086),(t-.016,.096),(t+.016,.096),(t+.016,.086)]for j in range(24)]
 fs=[(q*24+j,q*24+(j+1)%24,((q+1)%4)*24+(j+1)%24,((q+1)%4)*24+j)for q in range(4)for j in range(24)];mesh('WholeTubeNodeCollar_'+str(k),vs,fs,1)
for side in[-1,1]:
 x=side*.185
 lathe_z('WholeForkPost_'+str(side),x,0,[(0,.085),(.050,.085),(.050,.72),(0,.72)],0,20)
 lathe_z('WholeForkPostFootCollar_'+str(side),x,0,[(.048,.105),(.060,.105),(.060,.145),(.048,.145)],1,20)
axle('WholeTransverseTiltBodyAxle',-.259,.259,0,.66,.018,2,20)
for side in[-1,1]:axle('WholeAxleRetainer_'+str(side),side*.251-.012,side*.251+.012,0,.66,.033,2,20)
# Blunt stop is an integral full stone volume, fixed at a visible small rear-end gap.
lathe_z('WholeLowRearStopStone',0,.51,[(0,.085),(.155,.085),(.18,.17),(.14,.37),(.085,.445),(0,.445)],3,12)
# Tall rooted side feed-post exterior and one angled independently blind open spout.
lathe_z('WholeTallSideFeedPost',-.40,-.47,[(0,.085),(.048,.085),(.048,1.14),(.038,1.18),(0,1.18)],0,20)
for k,z in enumerate([.34,.79,1.10]):lathe_z('WholeFeedPostNode_'+str(k),-.40,-.47,[(.046,z-.013),(.057,z-.013),(.057,z+.013),(.046,z+.013)],1,20)
# Full spout along a downward diagonal; the cavity is intentionally blind at its rear root.
a=(-.41,-.47,1.09);b=(.015,-.54,1.025);ww=unit(sub(b,a));uu=unit(cross(ww,(0,0,1)));vv=cross(ww,uu);length=math.sqrt(dot(sub(b,a),sub(b,a)));vs=[];rs=[]
for t,r in[(0,0),(0,.040),(length,.040),(length,.026),(.075,.026),(.075,0)]:
 ids=[]
 for j in range(1 if r==0 else 24):
  th=math.tau*j/24;ids.append(len(vs));vs.append(tuple(a[k]+ww[k]*t+r*(uu[k]*math.cos(th)+vv[k]*math.sin(th))for k in range(3)))
 rs.append(ids)
fs=[]
for aa,bb in zip(rs,rs[1:]+rs[:1]):
 if len(aa)==len(bb)==1:continue
 for j in range(24):
  k=(j+1)%24
  if len(aa)==1:fs.append((aa[0],bb[k],bb[j]))
  elif len(bb)==1:fs.append((aa[j],aa[k],bb[0]))
  else:fs.append((aa[j],aa[k],bb[k],bb[j]))
mesh('WholeAngledBlindOpenSpout',vs,fs,0)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeBambooLookingTubes_WarmOlive',(.43,.44,.20,1),.88,0),('WholeNodeCollars_DarkOlive',(.28,.30,.13,1),.93,0),('WholeAxleAndRetainers_DarkWood',(.13,.10,.065,1),.94,0),('WholeBaseAndStop_WarmStone',(.40,.39,.34,1),.98,0)]
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
focus=Vector((0,0,.55))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.90;aim(cam,(4,-6,4.6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/regional/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'regional','style':'S01-clean-geometric','title':'Fixed Open Tilt Tube and Garden Spout','description':'One wholly newly authored complete dry garden tipping-tube-inspired decorative apparatus in a single fixed pose. A full thick long bamboo-looking body has a closed rear end, genuine deep front cavity and obliquely cut full-thickness open mouth. Its transverse axle joins two independent short fork posts rooted in one irregular low stone base; the rear end is fixed just over a separate blunt low stop stone. A whole tall side post and independently angled deep-mouth spout are rooted beside the open tube, with small finite structural collars. Unlike the foot-beam mortar frame, there is no broad treadle, hanging pestle or fixed receiving mortar: the complete hollow tube itself occupies the pivoted upper body. Unlike the rain-gauge cutaway, there are no paired rectangular buckets, surrounding casing, circular collector funnel or measured receiving interval. All complete coordinates newly authored; no old well, lever, vessel or stone mesh imported. Four opaque solid PBR roles, metres Z up and whole horizontal centred ground datum, one prop zero scenes. Dry fixed regional-garden-inspired artistic appearance only, not a historical reconstruction. No water, connected fluid circuit, filling, tipping cycle, balancing, sound, animal deterrence, planting, outdoor durability, installation, load, manufacture or safety capability. Rigging animation interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
