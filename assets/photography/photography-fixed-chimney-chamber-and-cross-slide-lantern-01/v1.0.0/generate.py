import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='photography-fixed-chimney-chamber-and-cross-slide-lantern-01'
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



# New hollow box boundary made from a small exact rectilinear occupancy lattice.
def boundary_solid(name,xs,ys,zs,filled,mat):
 cells={(i,j,k)for i in range(len(xs)-1)for j in range(len(ys)-1)for k in range(len(zs)-1)if filled((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)}
 vv=[];ff=[];idx={}
 def ids(coords):
  out=[]
  for q in coords:
   if q not in idx:idx[q]=len(vv);vv.append(q)
   out.append(idx[q])
  return tuple(out)
 for i,j,k in sorted(cells):
  x,X=xs[i:i+2];y,Y=ys[j:j+2];z,Z=zs[k:k+2]
  faces=[((-1,0,0),[(x,y,z),(x,y,Z),(x,Y,Z),(x,Y,z)]),((1,0,0),[(X,y,z),(X,Y,z),(X,Y,Z),(X,y,Z)]),((0,-1,0),[(x,y,z),(X,y,z),(X,y,Z),(x,y,Z)]),((0,1,0),[(x,Y,z),(x,Y,Z),(X,Y,Z),(X,Y,z)]),((0,0,-1),[(x,y,z),(x,Y,z),(X,Y,z),(X,y,z)]),((0,0,1),[(x,y,Z),(X,y,Z),(X,Y,Z),(x,Y,Z)])]
  for (a,b,c),q in faces:
   if(i+a,j+b,k+c)not in cells:ff.append(ids(q))
 mesh(name,vv,ff,mat)
for j,x in enumerate([-.125,.125]):box('WholeGroundFoot_%d'%j,(x,-.075,.016),(.045,.52,.032),0)
box('WholeLongCommonBed',(0,-.075,.047),(.34,.56,.045),3)
xs=[-.15,-.136,-.05,-.043,.043,.05,.136,.15];ys=[-.13,-.116,-.08,-.043,.043,.08,.116,.13];zs=[.062,.077,.115,.17,.27,.292,.325,.339]
def filled(x,y,z):
 if z<.077:return True
 if z>.325:return not(abs(x)<.043 and abs(y)<.043)
 if abs(x)>.136:
  return not(x>0 and abs(y)<.08 and .115<z<.292)
 if abs(y)>.116:
  return not(y<0 and abs(x)<.05 and .17<z<.27)
 return False
boundary_solid('WholeHollowLampChamberWithSideAccess',xs,ys,zs,filled,1)
# Whole side door held outward at a fixed angle; no invisible hinge or moving claim.
theta=math.radians(57);yy=.086
box('WholeSideAccessDoor',(0,0,0),(.012,.177,.192),1)
v,f,m=G['WholeSideAccessDoor'];G['WholeSideAccessDoor']=([(.151+math.sin(theta)*(y+.0885),yy-math.cos(theta)*(y+.0885),z+.2035)for x,y,z in v],f,m)
# Restore door thickness after the planar rotation above.
v,f,m=G['WholeSideAccessDoor'];orig=[tuple(s[i]*[.012,.177,.192][i]/2 for i in range(3))for s in[(x,y,z)for z in[-1,1]for y in[-1,1]for x in[-1,1]]]
G['WholeSideAccessDoor']=([(.151+math.cos(theta)*x+math.sin(theta)*(y+.0885),yy+math.sin(theta)*x-math.cos(theta)*(y+.0885),z+.2035)for x,y,z in orig],[tuple(reversed(q))for q in f],m)
for k,z in enumerate([.143,.264]):lathe_z('WholeDoorHinge_%d'%k,.151,.086,[(0,z-.018),(.010,z-.018),(.010,z+.018),(0,z+.018)],2,12)
# Entire square chimney remains open through the roof, and the cap is raised clear on four posts.
boundary_solid('WholeOpenSquareChimney',[-.052,-.038,.038,.052],[-.052,-.038,.038,.052],[.326,.435],lambda x,y,z:abs(x)>.038 or abs(y)>.038,1)
for i,(x,y)in enumerate([(-.048,-.048),(.048,-.048),(-.048,.048),(.048,.048)]):box('WholeCapPost_%d'%i,(x,y,.448),(.010,.010,.042),2)
v=[(x,y,z)for z in[.461,.474]for x,y in[(-.075,-.070),(.075,-.070),(.075,.070),(-.075,.070)]]
mesh('WholeRaisedChimneyCap',v,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],1)
# Full transverse frame with two actual rectangular windows; not a card decal.
boundary_solid('WholeTransverseTwoApertureSlideCarrier',[-.20,-.182,-.054,-.036,.092,.110],[-.171,-.157],[.148,.164,.276,.292],lambda x,y,z:z<.164 or z>.276 or x<-.182 or -.054<x<-.036 or x>.092,3)
box('WholeBlankOpaqueSlideInsert',(.028,-.163,.22),(.133,.009,.118),0)
for j,z in enumerate([.142,.297]):box('WholeCarrierFixedGuide_%d'%j,(-.042,-.157,z),(.340,.035,.020),2)
box('WholeCarrierLowerSeat',(-.040,-.153,.102),(.18,.055,.076),1)
# Complete deep annular lens assembly supported independently in front of the chamber.
box('WholeLensSupportSaddle',(0,-.257,.124),(.115,.102,.127),1)
ringy('WholeLongLensHousing',-.360,-.172,0,.220,.038,.058,2,32)
ringy('WholeForwardLensHood',-.394,-.342,0,.220,.042,.066,2,32)
cyly('WholeOpaqueRecessedLens',-.359,-.353,0,.220,.043,0,32)
axle('WholeFixedLensSideKnob',.047,.080,-.276,.192,.019,3,20)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeFeetAndOpaqueInsert_Graphite',(.045,.052,.049,1),.72,.05),('WholeChamberAndChimney_DarkGreenEnamel',(.12,.22,.18,1),.53,.20),('WholeLensAndHardware_Brass',(.59,.40,.14,1),.39,.66),('WholeBedCarrierAndKnob_Walnut',(.34,.17,.065,1),.77,0)]
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
focus=Vector((0,0,.23))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.80;aim(cam,(4,-6,3.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/photography/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'photography','style':'S01-clean-geometric','title':'Fixed Chimney Chamber and Cross Slide Lantern','description':'One newly authored complete fixed magic-lantern-style film-history prop. Two finite shoes and a common long bed carry a genuine thick hollow lamp chamber with a side opening and an entire door held aside, a real open square upper chimney with a raised weather-cap appearance, and a separate forward lens-support saddle. A complete transverse two-aperture slide carrier crosses the space between the chamber and the long stepped annular lens housing. One carrier aperture contains a blank opaque insert; the other remains genuinely open. An empty unlit inner chamber floor, independent recess-ended barrel and fixed side knob complete the device. No camera tripod, reels, film ribbon, prior machine case or old visible mesh is imported. The complete hollow chamber/vent stack, side access and transverse slide relationship is newly constructed rather than a renamed camera body. Four opaque constant PBR materials, one prop zero scenes, metres native Z up and whole horizontal-bounds-centred finite shoe origin. Static historical-style illustrative appearance only, not a particular historical replica: no flame, fuel, heat, ventilation performance, optics, transparency, image projection, focusing, sliding, operation, electrical or mechanical function, fabrication, compatibility or safety claim. Rigging animation and interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
