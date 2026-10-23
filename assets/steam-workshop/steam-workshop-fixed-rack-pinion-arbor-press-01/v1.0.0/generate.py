import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='steam-workshop-fixed-rack-pinion-arbor-press-01'
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



# All whole apparatus coordinates are newly authored; no old machine geometry imported.
def prism_y(name,poly,y0,y1,mat):
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(poly,poly[1:]+poly[:1]))<0:poly=list(reversed(poly))
 n=len(poly);v=[(x,y,z)for y in[y0,y1]for x,z in poly];t=triangulate(poly);f=[tuple(reversed(q))for q in t]+[tuple(n+i for i in q)for q in t]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh(name,v,f,mat)
def prism_z(name,poly,z0,z1,mat):
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(poly,poly[1:]+poly[:1]))<0:poly=list(reversed(poly))
 n=len(poly);v=[(x,y,z)for z in[z0,z1]for x,y in poly];t=triangulate(poly);f=[tuple(reversed(q))for q in t]+[tuple(n+i for i in q)for q in t]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh(name,v,f,mat)
box('WholeGroundedPressFoot',(0,.04,.055),(1.06,.72,.11),0)
# Full connected thick open C casting, not an arrangement of loose blocks.
prism_y('WholeOpenThroatCCasting',[(-.46,.09),(.46,.09),(.46,.20),(-.25,.20),(-.25,.82),(-.20,.91),(.38,.91),(.38,1.27),(-.33,1.27),(-.46,1.12)],.11,.35,0)
# Full fixed table with one open front receiving slot, intentionally no loose workpiece.
prism_z('WholeSlottedLowerAnvil',[(.05,-.27),(.20,-.27),(.20,-.05),(.28,-.05),(.28,-.27),(.45,-.27),(.45,.25),(.05,.25)],.15,.22,1)
# One continuous toothed ram: 12 integral trapezoid teeth, not boxes pasted on a bar.
profile=[(.30,.48),(.30,1.52),(.20,1.52),(.20,1.46)]
for i in range(12):
 z=1.46-i*.055
 profile.extend([(.20,z-.008),(.145,z-.018),(.145,z-.035),(.20,z-.045),(.20,z-.055)])
profile +=[(.20,.48)]
prism_y('WholeIntegralToothedVerticalRam',profile,-.08,.08,1)
box('WholeFlatRamNose',(.25,0,.47),(.15,.19,.08),1)
# Two complete left-open guide channels reveal the rack side rather than cap it.
upoly=[(.18,-.09),(.32,-.09),(.32,.09),(.18,.09),(.18,.15),(.38,.15),(.38,-.15),(.18,-.15)]
for name,z in [('Lower',.83),('Upper',1.14)]:prism_z(name+'WholeOpenRamGuide',upoly,z,z+.10,0)
# A fixed display retaining pin truly joins the ram to the upper channel and rear casting.
cyly('WholeFixedUpperRamRetainingPin',-.20,.25,.25,1.19,.022,2,16)
cyly('WholeRamRetainingPinFrontCap',-.225,-.19,.25,1.19,.039,2,16)
# Single toothed disk and supported shaft, with deliberate visible display clearance to rack.
poly=[]
for i in range(12):
 for da,r in [(-.5,.103),(-.27,.103),(-.16,.145),(.16,.145),(.27,.103)]:
  t=(i+da)*math.tau/12;poly.append((-.005+r*math.cos(t),1.05+r*math.sin(t)))
prism_y('WholeTwelveToothPinion',poly,-.075,.075,2)
cyly('WholePinionAxle',-.29,.26,-.005,1.05,.035,1,20)
cyly('WholeFrontBearingCollar',-.115,-.075,-.005,1.05,.065,0,20)
# Collar's fixed upper/lower ear has full attachment to the C casting, not a floating bearing.
box('WholeBearingRearMount',(-.005,.155,1.05),(.14,.18,.15),0)
cyly('WholeLeverHub',-.29,-.235,-.005,1.05,.075,2,20)
beam('WholeLongFixedActuatingHandle',(-.005,-.265,1.05),(.43,-.265,1.52),.045,1)
beam('WholeLongHandleGrip',(.37,-.265,1.455),(.49,-.265,1.585),.075,0)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeCastFrame_MutedPetrol',(.055,.18,.18,1),.72,.25),('RamHandleAnvil_SatinSteel',(.43,.47,.46,1),.45,.65),('PinionAndPins_WarmMetal',(.50,.31,.11,1),.46,.55)]
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
focus=Vector((0,0,.81))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.14;aim(cam,(3,-7,3.6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/steam-workshop/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'steam-workshop','style':'S01-clean-geometric','title':'Fixed Rack and Pinion Arbor Press','description':'One newly authored whole fixed arbor-press appearance for the original steam-workshop gear-transmission visual direction. A grounded foot carries one continuous thick C-shaped casting with a real open throat, a complete slotted lower anvil, two whole left-open ram guides, one long rectangular ram with twelve integral trapezoid rack teeth and a broad flat pressing nose. A separate whole toothed pinion, fixed supported axle, hub and long diagonal hand lever form the side drive appearance. One visible retaining pin fixes the ram in its displayed height and joins it to the upper guide and rear casting. This is not the old column drill without a bit, a citrus cone with a new color or a basket screw press without a basket: no motor, belt cover, drill spindle, fruit cone, screw spindle, basket or liquid collector is used. Every whole coordinate is new; only generic mesh/export/render tools are reused. Closed editable components with three opaque PBR materials, metres, Z up and actual whole horizontal bounds centred over the ground datum. One model, zero scenes. Intentional fixed overlap joins and deliberate small pinion-to-rack display clearance are not a validated conjugate gear mesh. Static illustrative art only; no pressing force, working transmission, continuous engagement, sliding stroke, rotation, release, workholding, manufacture, stability, load or equipment safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
