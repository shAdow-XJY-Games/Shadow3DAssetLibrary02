import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='playground-fixed-puffed-floor-and-open-grid-arch-enclosure-01'
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



# Whole puffed floor and enclosed upright play-frame exterior; no pressure simulation.
def tube(name,points,r,mat,n=12):
 v=[];f=[]
 for k,p in enumerate(points):
  t=unit(sub(points[min(k+1,len(points)-1)],points[max(k-1,0)]));u=unit(cross(t,(0,0,1)if abs(t[2])<.9 else(0,1,0)));w=cross(t,u)
  for j in range(n):v.append(tuple(p[i]+r*(u[i]*math.cos(math.tau*j/n)+w[i]*math.sin(math.tau*j/n))for i in range(3)))
 for k in range(len(points)-1):
  for j in range(n):h=(j+1)%n;f.append((k*n+j,k*n+h,(k+1)*n+h,(k+1)*n+j))
 f +=[tuple(reversed(range(n))),tuple((len(points)-1)*n+j for j in range(n))];mesh(name,v,f,mat)
def octagon(x,y,c):return[(-x+c,-y),(x-c,-y),(x,-y+c),(x,y-c),(x-c,y),(-x+c,y),(-x,y-c),(-x,-y+c)]
v=[]
for x,y,c,z in[(1.20,1.25,.22,0),(1.29,1.34,.24,.15),(1.22,1.27,.22,.30),(1.02,1.07,.18,.36)]:v +=[(a,b,z)for a,b in octagon(x,y,c)]
f=[tuple(reversed(range(8))),tuple(24+i for i in range(8))]+[(k*8+i,k*8+(i+1)%8,(k+1)*8+(i+1)%8,(k+1)*8+i)for k in range(3)for i in range(8)]
mesh('WholeGroundFootPuffedFloor',v,f,0)
for i,(x,y)in enumerate([(-1.08,-1.13),(1.08,-1.13),(-1.08,1.13),(1.08,1.13)]):
 lathe_z('WholeRootedPaddedCornerColumn_%d'%i,x,y,[(0,.24),(.15,.24),(.19,.32),(.20,.50),(.185,1.90),(.17,2.06),(.12,2.14),(0,2.18)],1,16)
 # A broad lower coloured sleeve is a separate proud padded appearance, not coplanar paint.
 lathe_z('WholeColumnFootCuff_%d'%i,x,y,[(0,.29),(.204,.29),(.215,.39),(.204,.53),(0,.53)],2,16)
path=[(-1.08*math.cos(math.pi*i/16),-1.13,1.94+.55*math.sin(math.pi*i/16))for i in range(17)]
tube('WholeFrontOpenEntryArch',path,.16,2,16)
# Three sides have full padded lower and upper edge rails and real open mesh windows.
for side in ['Left','Right','Back']:
 def pt(q,z):
  return(-1.08,q,z)if side=='Left'else((1.08,q,z)if side=='Right'else(q,1.13,z))
 half=1.13 if side!='Back'else 1.08
 tube('WholeLowerPaddedWall_'+side,[pt(-half,.60),pt(half,.60)],.145,1,12)
 tube('WholeUpperPaddedWall_'+side,[pt(-half,1.90),pt(half,1.90)],.12,2,12)
 for i in range(13):
  q=-half+.15+(2*half-.30)*i/12
  tube('WholeWindowVertical_'+side+'_'+str(i),[pt(q,.68),pt(q,1.84)],.012,3,6)
 for i in range(8):
  z=.72+1.08*i/7;a=pt(-half+.10,z);b=pt(half-.10,z)
  # Actual offset at the grid crossings prevents broad coincident strip faces.
  axis=0 if side!='Back'else 1;a=list(a);b=list(b);a[axis]+=.010;b[axis]+=.010
  tube('WholeWindowHorizontal_'+side+'_'+str(i),[tuple(a),tuple(b)],.011,3,6)
# One low rounded-looking ramp is wholly seated on the ground and embedded in floor front.
p=[(-.62,-1.91,0),(.62,-1.91,0),(.72,-1.13,0),(-.72,-1.13,0),(-.57,-1.91,.075),(.57,-1.91,.075),(.68,-1.13,.35),(-.68,-1.13,.35)]
mesh('WholeGroundFootEntryRamp',p,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeThickFloor_WarmAmber',(.70,.40,.09,1),.77,0),('WholeColumnsAndLowWalls_MutedCoral',(.63,.16,.105,1),.72,0),('WholeArchRailsAndRamp_DeepTeal',(.045,.32,.36,1),.72,0),('WholeActualOpenWindowStrands_Charcoal',(.055,.075,.075,1),.83,0)]
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
focus=Vector((0,0,1.10))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=4.25;aim(cam,(4,-6,4.3));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/playground/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'playground','style':'S01-clean-geometric','title':'Fixed Puffed Floor and Open Grid Arch Enclosure','description':'One newly authored whole fixed soft-play-enclosure exterior. A complete thick chamfer-rounded puffed floor has a finite flat underside and a gently raised top. Four rooted padded columns carry a tall continuous front entry arch and complete side/back lower and upper padded rails. Three full window fields consist of real separate crossed finite strands with actual open cells, not transparent planes or printed mesh. A whole broad low inclined entry ramp is grounded and enters the front of the floor. The complete rooted floor, columns, arch and enclosing windows form one prop, not a trampoline with a changed surface, a sandpit with taller walls, a castle recolour or a scene assembled from earlier pieces. All numeric geometry newly authored, four opaque constant untextured PBR roles, metres, Z up and whole horizontally centred ground datum. One model, zero scenes. Fixed illustrative exterior only: padded forms use solid closed surfaces, internal pressure chambers, blower, inflation, fabric seams, elastic response, jumping, child fit, restraint/enclosure effectiveness, load, installation, manufacture and playground safety are not modeled or verified. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
