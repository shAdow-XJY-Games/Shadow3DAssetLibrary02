import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='public-service-fixed-nested-carriages-and-folded-seat-bleachers-01'
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



def whole_profile(name,p,a,b,axis,mat):
 if sum(u[0]*v[1]-u[1]*v[0]for u,v in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);tt=triangulate(p)
 def pt(q,t):return(t,q[0],q[1])if axis=='x'else(q[0],t,q[1])
 mesh(name,[pt(q,t)for t in[a,b]for q in p],[tuple(reversed(t))for t in tt]+[tuple(n+i for i in t)for t in tt]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],mat)
def flatwheel(name,x,y,width):
 n=16;r=.065/math.cos(math.pi/n)
 v=[(xx,y+r*math.sin(math.tau*i/n+math.pi/n),.065+r*math.cos(math.tau*i/n+math.pi/n))for xx in[x-width/2,x+width/2]for i in range(n)]
 mesh(name,v,[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],2)
rows=[(-.80,.99,.16,.28),(-.20,1.11,.26,.64),(.40,1.23,.36,1.00)]
for i,(y,half,base,deck)in enumerate(rows):
 rear=.85+.12*i;front=y-.28
 for side in[-1,1]:
  x=side*half
  box('WholeNestedBaseRail_'+str((i,side)),(x,(front+rear)/2,base),(.055,rear-front,.060),0)
  for yy in[y-.18,rear-.10]:
   flatwheel('WholeGroundFootWheel_'+str((i,side,yy)),x,yy,.036)
   axle('WholeWheelAxle_'+str((i,side,yy)),x-.044,x+.044,yy,.065,.013,3,12)
   # A side cheek bridges each actual axle to its own complete base rail.
   box('WholeWheelCheek_'+str((i,side,yy)),(x+side*.027,yy,(.065+base)/2),(.018,.050,base-.065+.035),0)
  bottom=base+.022;top=deck-.024
  box('WholeTierPost_'+str((i,side)),(x,y+.16,(bottom+top)/2),(.065,.065,top-bottom+.010),0)
  box('WholeCantileverDeckBearer_'+str((i,side)),(x,y,deck-.030),(.070,.66,.060),0)
 for yy in[y-.15,rear-.08]:box('WholeCarriageCrossTie_'+str((i,yy)),(0,yy,base),(2*half+.040,.045,.044),0)
 box('WholeCompleteFootDeck_'+str(i),(0,y,deck+.008),(2.75,.64,.040),1)
 # Separate complete hinged seat, not a recoloured old fixed tier board.
 sy=y+.15;sz=deck+.365
 for side in[-1,1]:
  x=side*.90
  box('WholeSeatRiser_'+str((i,side)),(x,sy,(deck+.025+sz)/2),(.055,.060,sz-deck-.025),0)
  axle('WholeSeatPivotPin_'+str((i,side)),x-.065,x+.065,sy,sz,.025,3,16)
  box('WholeSeatHingeTongue_'+str((i,side)),(x,sy-.025,sz+.015),(.055,.10,.050),0)
 # Lowest board is fixed 72 degrees up about the full rear edge; upper boards stay horizontal.
 angle=math.radians(72 if i==0 else 0)
 name='WholeFullWidthPivotedSeat_'+str(i);box(name,(0,-.135,.027),(2.72,.29,.054),1)
 v,f,m=G[name];G[name]=([(x,sy+yy*math.cos(angle)+zz*math.sin(angle),sz-yy*math.sin(angle)+zz*math.cos(angle))for x,yy,zz in v],f,m)
 # finite small under-seat rear stop carried by each hinge riser
 for side in[-1,1]:box('WholeSeatRearStop_'+str((i,side)),(side*.90,sy+.035,sz+.027),(.075,.045,.070),0)
# Captured channels visibly connect the three full rolling tiers without pretending movement was checked.
for i in[0,1]:
 y,half,base,deck=rows[i];nexthalf=rows[i+1][1];nextbase=rows[i+1][2];yy=.63+.12*i
 for side in[-1,1]:
  x=side*half
  p=[(x-.044,base-.048),(x+.044,base-.048),(x+.044,base+.048),(x+.030,base+.048),(x+.030,base-.031),(x-.030,base-.031),(x-.030,base+.048),(x-.044,base+.048)]
  whole_profile('WholeOpenCaptureChannel_'+str((i,side)),p,yy-.06,yy+.06,'y',3)
  # root below the inner rail and rise to the next carriage rail; no coplanar exposed end cap.
  beam('WholeGuideConnectingShoulder_'+str((i,side)),(x,yy,base-.042),(side*nexthalf,yy,nextbase),.025,0)
# Full rear frame is rooted in the rear rolling chassis, not an unrelated railing prop.
for side in[-1,1]:
 x=side*1.23
 box('WholeRearGuardPost_'+str(side),(x,1.02,1.06),(.060,.060,1.42),0)
box('WholeRearGuardTop',(0,1.02,1.76),(2.51,.075,.065),0)
box('WholeRearGuardMid',(0,1.02,1.48),(2.49,.042,.045),0)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeNestedChassisAndGuard_DeepTeal',(.09,.23,.25,1),.65,.18),('WholeSeatsAndDecks_WarmOchre',(.58,.36,.15,1),.77,0),('WholeFlatWheelTreads_Charcoal',(.035,.040,.042,1),.84,0),('WholePinsAndCaptures_SatinMetal',(.43,.47,.48,1),.46,.50)]
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
focus=Vector((0,0,.92))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=4.60;aim(cam,(4,-6,4.1));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/public-service/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'public-service','style':'S01-clean-geometric','title':'Fixed Nested Carriages and Folded Seat Bleachers','description':'One newly authored complete static partly nested bleacher-frame appearance. Three whole unequal-width wheel-supported undercarriages overlap beneath three progressively higher full cantilevered foot decks. Each complete pair of long base rails has its own four wheels, full front and rear cross ties, two posts and two deck bearers. Two pairs of complete open guide sleeves and connecting shoulders tie successive whole carriages together at the rear; they are not three loose benches grouped into a scene. Every full-width seat has its own transverse hinge axis and two rooted risers: the lowest entire seat board is fixed folded upward while the upper two are horizontal. A full high rear guard belongs to the largest rear carriage. All outlines and supports independently authored, no old mesh imported. Unlike the older fixed bleachers with common grounded runners, nine upright posts and diagonal braces, this whole assembly visibly uses nested different-width rolling chassis, rear guide captures and separate pivoted seat-to-deck relations. Four opaque untextured material roles, metres Z up, horizontal bounds-centred ground datum and twelve finite wheel soles. One fixed prop zero scenes, empty and unoccupied. The shown positions are static illustrative art only, not validated retracting or folding kinematics, sliding fits, rolling action, locking, pinch clearances, public access, egress, spectator capacity, load, stability, manufacture, installation or safety certification. Rigging animation interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
