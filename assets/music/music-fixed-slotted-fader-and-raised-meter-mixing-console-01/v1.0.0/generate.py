import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='music-fixed-slotted-fader-and-raised-meter-mixing-console-01'
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



# New complete inclined case with genuinely slotted independent fader faceplate.
def top(y):return .105+.22*(y+.32)
poly=[(-.34,-.32),(.34,-.32),(.34,.32),(-.34,.32)]
v=[(x,y,.035)for x,y in poly]+[(x,y,top(y))for x,y in poly];mesh('WholeInclinedConsoleCase',v,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],0)
for sx in[-1,1]:
 for sy in[-1,1]:box('WholeGroundFoot_%s_%s'%(sx,sy),(sx*.28,sy*.24,.022),(.080,.066,.044),0)
# One full plate has true long holes, with shared mesh vertices and no overlapping bars.
centres=[-.24,-.08,.08,.24];xs=sorted(set([-.32,.32]+[x+d for x in centres for d in[-.009,.009]]));ys=[-.278,-.242,-.012,.025];cells=set()
for i in range(len(xs)-1):
 for j in range(len(ys)-1):
  x=(xs[i]+xs[i+1])/2;y=(ys[j]+ys[j+1])/2
  if -.242<y<-.012 and any(abs(x-c)<.009 for c in centres):continue
  cells.add((i,j))
vs=[];ix={};faces=[]
def vi(p):
 p=tuple(p)
 if p not in ix:ix[p]=len(vs);vs.append(p)
 return ix[p]
def quad(points):faces.append(tuple(vi(p)for p in points))
for i,j in sorted(cells):
 x0,x1=xs[i:i+2];y0,y1=ys[j:j+2];low=[(x0,y0,top(y0)-.002),(x1,y0,top(y0)-.002),(x1,y1,top(y1)-.002),(x0,y1,top(y1)-.002)];hi=[(x,y,z+.024)for x,y,z in low];quad(list(reversed(low)));quad(hi)
 for k,neighbor in enumerate([(i,j-1),(i+1,j),(i,j+1),(i-1,j)]):
  if neighbor not in cells:kk=(k+1)%4;quad([low[k],low[kk],hi[kk],hi[k]])
mesh('WholeFourSlotFaderFaceplate',vs,faces,1)
for k,(x,y)in enumerate(zip(centres,[-.195,-.095,-.145,-.052])):
 box('WholeFaderStem_%d'%k,(x,y,top(y)+.020),(.012,.014,.050),0)
 box('WholeFixedFaderCap_%d'%k,(x,y,top(y)+.052),(.061,.025,.019),3)
for row,y in enumerate([.070,.140,.210]):
 for col,x in enumerate(centres):lathe_z('WholeRotaryKnob_%d_%d'%(row,col),x,y,[(0,top(y)-.009),(.016,top(y)-.009),(.019,top(y)+.017),(.015,top(y)+.030),(0,top(y)+.030)],0,12)
# Full rear bridge and two real recessed framed blank displays.
box('WholeRaisedRearMeterBridge',(0,.310,.310),(.635,.110,.164),0)
def frame_y(name,x,z,hx,hz,y0,y1):
 outer=[(-hx,-hz),(hx,-hz),(hx,hz),(-hx,hz)];inner=[(-hx+.012,-hz+.012),(hx-.012,-hz+.012),(hx-.012,hz-.012),(-hx+.012,hz-.012)]
 vv=[(x+u,y,z+w)for y in[y0,y1]for loop in[outer,inner]for u,w in loop];ff=[]
 for i in range(4):j=(i+1)%4;ff.extend([(i,j,8+j,8+i),(4+i,12+i,12+j,4+j),(i,4+i,4+j,j),(8+i,8+j,12+j,12+i)])
 mesh(name,vv,ff,1)
for sx in[-1,1]:
 frame_y('WholeRecessedMeterFrame_'+str(sx),sx*.155,.315,.135,.048,.222,.270)
 box('WholeBlankOpaqueMeter_'+str(sx),(sx*.155,.258,.315),(.250,.025,.077),3)
# Whole side cheeks follow the case rise; their outer faces do not coincide with the body.
for sx in[-1,1]:
 pp=[(-.335,.030),(.375,.030),(.375,.397),(.265,.397),(.245,top(.245)+.015),(-.335,top(-.335)+.015)];n=len(pp);vv=[(xx,y,z)for xx in[sx*.34,sx*.385]for y,z in pp];tt=triangulate(pp);ff=list(tt)+[tuple(n+i for i in reversed(t))for t in tt]+[(i,n+i,n+(i+1)%n,(i+1)%n)for i in range(n)];mesh('WholeTimberSideCheek_'+str(sx),vv,ff,2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeConsoleKnobsAndFeet_Charcoal',(.048,.060,.064,1),.72,.06),('WholeSlottedFaceplateAndFrames_SatinGrey',(.32,.38,.39,1),.49,.34),('WholeSideCheeks_WarmTimber',(.38,.19,.085,1),.70,0),('WholeFaderCapsAndBlankMeters_Ivory',(.72,.69,.57,1),.68,0)]
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
focus=Vector((0,0,.17))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.12;aim(cam,(3,-5,4));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/music/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':'Fixed Slotted Fader and Raised Meter Mixing Console','description':'One newly authored complete static audio-mixing-console exterior. A continuous low inclined wedge case on four finite feet carries one complete thick faceplate with four genuine long through-slots backed by the real case surface. Four separate short stems rise through the slots into broad fixed fader caps at different positions. A rear rotary-control field and one full raised meter bridge with two genuinely recessed blank opaque meter panels complete the same desk unit; two whole shaped timber side cheeks bound its sides. New complete geometry, no old joystick controller, keyboard or tape-deck components imported. The slotted fader field and raised paired meter bridge are a different whole interface arrangement from the old flat ball-joystick/four-button deck and the twin-reel/continuous-tape recorder. Channel count is subordinate detail, not a series of counted variants. One prop, zero scenes; four opaque constant PBR roles, metres, Z up and horizontally bounds-centred ground origin. Empty blank display only: no printed scales, signal, audio mixing, electrical circuit, metering, fader or knob operation, calibration, compatibility, ergonomic or safety claim. No cables, instrument, rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
