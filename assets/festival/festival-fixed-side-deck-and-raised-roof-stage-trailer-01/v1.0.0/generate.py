import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='festival-fixed-side-deck-and-raised-roof-stage-trailer-01'
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



# Full chassis, independently grounded stabilizers, tandem wheels and tow yoke.
for y in[-.65,.65]:box('WholeLongChassisRail_'+str(y),(0,y,.48),(3.65,.12,.20),0)
for x in[-1.62,-.55,.55,1.62]:box('WholeChassisCrossRail_'+str(x),(x,0,.48),(.12,1.4,.19),0)
for x in[-.62,.62]:
 cyly('WholeTandemAxle_'+str(x),-.98,.98,x,.37,.055,0,16)
 for side in[-1,1]:
  y=side*.88;ringy('WholeTandemTyre_'+str((x,side)),y-.10,y+.10,x,.37,.15,.32,2,24)
  cyly('WholeTandemHub_'+str((x,side)),y-.105,y+.105,x,.37,.153,0,24)
for y in[-.63,.63]:beam('WholeConvergingTowRail_'+str(y),(1.77,y,.48),(2.70,0,.48),.11,0)
box('WholeTowNose',(2.70,0,.48),(.34,.18,.14),0)
# Main floor and the horizontal full side wing have a deliberate small hinge seam.
box('WholeMainStageDeck',(0,0,.67),(3.65,1.62,.18),1)
box('WholeExpandedSideDeck',(0,-1.47,.67),(3.65,1.28,.18),1)
for x in[-1.45,0,1.45]:axle('WholeSideDeckHinge_'+str(x),x-.12,x+.12,-.82,.67,.055,0,16)
for x in[-1.63,1.63]:
 for y in[-.65,.65]:
  box('WholeGroundFootMain_'+str((x,y)),(x,y,.035),(.32,.28,.07),0)
  box('WholeMainStabilizer_'+str((x,y)),(x,y,.32),(.11,.11,.58),0)
 for y in[-1.94]:
  box('WholeGroundFootWing_'+str(x),(x,y,.035),(.32,.28,.07),0)
  box('WholeOuterWingLeg_'+str(x),(x,y,.32),(.10,.10,.58),0)
# Four complete square sleeves and projecting inner posts root the raised roof.
def square_tube(name,x,y,z0,z1,outer,inner,mat):
 loops=[[(x+sx*r,y+sy*r,z)for sx,sy in[(-1,-1),(1,-1),(1,1),(-1,1)]]for z,r in[(z0,outer),(z1,outer),(z1,inner),(z0,inner)]]
 v=sum(loops,[]);f=[(k*4+i,k*4+(i+1)%4,((k+1)%4)*4+(i+1)%4,((k+1)%4)*4+i)for k in range(4)for i in range(4)];mesh(name,v,f,mat)
for x in[-1.65,1.65]:
 for y in[-.68,.68]:
  square_tube('WholeCornerOuterSleeve_'+str((x,y)),x,y,.74,1.78,.069,.049,0)
  box('WholeRaisedInnerPost_'+str((x,y)),(x,y,2.055),(.084,.084,1.05),0)
  cyly('WholeFixedPostRetainer_'+str((x,y)),y-.087,y+.087,x,1.64,.016,2,12)
  box('WholeRoofSeatCap_'+str((x,y)),(x,y,2.565),(.18,.18,.09),0)
# Roof has its own longitudinal beams and a single thick, shallow gabled shell.
for y in[-.68,.68]:box('WholeRoofLongBeam_'+str(y),(0,y,2.64),(3.52,.12,.12),0)
profile=[(-.92,2.635),(0,2.83),(.92,2.635),(.92,2.705),(0,2.90),(-.92,2.705)]
v=[(x,y,z)for x in[-1.88,1.88]for y,z in profile];n=len(profile);f=[]
for a,b,c in triangulate(profile):f.extend([(c,b,a),(a+n,b+n,c+n)])
for i in range(n):j=(i+1)%n;f.append((i,j,j+n,i+n))
mesh('WholeRaisedShallowGabledRoof',v,f,3)
box('WholeLowRearStageBackboard',(0,.775,1.02),(3.50,.07,.52),3)
# Side access stair: finite complete thick treads supported by full sloping stringers.
for y in[-1.78,-1.12]:beam('WholeStairStringer_'+str(y),(-2.53,y,.10),(-1.79,y,.66),.10,0)
for k in range(3):
 x=-2.45+k*.25;z=.18+k*.19
 box('WholeAccessTread_'+str(k),(x,-1.45,z),(.28,.82,.085),1)
for y in[-1.78,-1.12]:box('WholeGroundFootStair_'+str(y),(-2.53,y,.035),(.22,.19,.07),0)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeFrameAndColumns_SatinAlloy',(.37,.42,.43,1),.57,.42),('WholeStageAndTreads_WarmBoard',(.49,.29,.14,1),.91,0),('WholeTyresAndRetainers_Charcoal',(.035,.045,.047,1),.89,0),('WholeRoofAndBackboard_MutedTeal',(.09,.28,.30,1),.79,.04)]
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
focus=Vector((0,0,1.40))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=7.0;aim(cam,(6,8,4.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/festival/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'festival','style':'S01-clean-geometric','title':'Fixed Side Deck and Raised Roof Stage Trailer','description':'One wholly newly authored complete fixed expanded performance-stage trailer exterior. A tandem-wheel longitudinal chassis and converging tow yoke carry a raised main deck and continuous low rear backboard. An entire hinged side-deck wing is fixed horizontal, with three complete hinge barrels at its inner edge and two full-height outer support legs on finite ground shoes. Four main stabilizer feet and telescopic-looking square corner columns join the chassis to a raised whole shallow pitched roof body, with separate inner posts, transverse retainers and underside roof beams. A complete short side stair runs to the open stage floor. The low rear side panel and raised overhead roof remain separated by an open performance bay. Unlike the complete arched stock trailer, there is no enclosing stock vault, internal divided pen or rear loading ramp; unlike the field-kitchen trailer, there are no cooking wells or furnace. The outboard horizontal floor wing with its own legs and the lifted corner-supported canopy form an integrated newly authored spatial apparatus, not a copied vehicle carrying old stage objects. Four opaque PBR materials, metres Z up, whole horizontal bounds centred. One static complete model zero scenes. No roof raising sequence, hinge or telescopic travel, towing/road compatibility, wheel motion, weather enclosure, usable clearance, load, occupancy, performance installation or safety ability made or verified. No people, audience, sound equipment, lighting system, rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
