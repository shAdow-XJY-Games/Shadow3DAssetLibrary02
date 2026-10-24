import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='architecture-fixed-raised-hinged-lip-dock-leveler-01'
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

# Complete fixed dock leveller: rear pivot deck and a separately hinged nose lip.
PALETTE=[('ReceiverDarkSteel',(.18,.23,.24,1),.61,.52),('DeckMutedOchre',(.57,.40,.16,1),.66,.32),('PinsCylinderSteel',(.42,.47,.48,1),.36,.68)]
# Low receiving pit frame; no host building or truck is supplied.
for side in [-1,1]:
 x=side*.86
 box('WholePitSideRail_'+str(side),(x-.055,-.95,0),(x+.055,.95,.14),0)
 box('WholeRearPivotTower_'+str(side),(x-.050,.73,.10),(x+.050,.91,.55),0)
for y in[-.89,.84]:box('WholePitCrossRail_'+str(y),(-.815,y-.055,0),(.815,y+.055,.13),0)
box('WholeCentralCylinderBase',(-.18,.27,.09),(.18,.45,.21),0)
ang=math.radians(13);D=(0,-math.cos(ang),math.sin(ang));PN=(0,math.sin(ang),math.cos(ang));P=(0,.82,.52)
def decktr(q):x,t,n=q;return add(add(P,(x,0,0)),add(mul(D,t),mul(PN,n)))
box('WholeInclinedDeck',(-.79,0,-.055),(.79,1.73,.025),1)
v,f,m=G['WholeInclinedDeck'];record('WholeInclinedDeck',[decktr(q)for q in v],f,m)
for x in[-.58,.58]:
 n='WholeDeckUndersideBeam_'+str(x);box(n,(x-.045,.07,-.135),(x+.045,1.64,-.047),0);v,f,m=G[n];record(n,[decktr(q)for q in v],f,m)
pipe('WholeRearPivotAxle',[(-.92,.82,.52),(.92,.82,.52)],.035,2,16)
for side in[-1,1]:wheel('RearPivotEndCap_'+str(side),side*.929,.82,.52,.052,0,.028,2)
T=decktr((0,1.73,-.015));lipang=math.radians(-8);LD=(0,-math.cos(lipang),math.sin(lipang));LN=(0,math.sin(lipang),math.cos(lipang))
def liptr(q):x,t,n=q;return add(add(T,(x,0,0)),add(mul(LD,t),mul(LN,n)))
box('WholeIndependentFrontLip',(-.765,.012,-.025),(.765,.39,.025),1);v,f,m=G['WholeIndependentFrontLip'];record('WholeIndependentFrontLip',[liptr(q)for q in v],f,m)
pipe('WholeLipHingeAxle',[(-.81,T[1],T[2]),(.81,T[1],T[2])],.032,2,16)
for x in[-.65,0,.65]:
 wheel('WholeLipHingeKnuckle_'+str(x),x,T[1],T[2],.043,0,.16,0)
 # Each knuckle has finite material reaching into both adjoining thick plates.
 box('LipKnuckleDeckBracket_'+str(x),(x-.065,T[1]-.005,T[2]-.015),(x+.065,T[1]+.055,T[2]+.038),0)
A=(0,.36,.19);B=decktr((0,1.05,-.126));V=sub(B,A);C=add(A,mul(V,.63))
pipe('WholeAngledCylinderBarrel',[A,C],.069,0,16)
pipe('WholeCylinderExposedRod',[add(A,mul(V,.57)),B],.030,2,16)
for tag,p in [('Lower',A),('Upper',B)]:
 pipe('WholeCylinderMountPin_'+tag,[add(p,(-.17,0,0)),add(p,(.17,0,0))],.031,2,16)
 for side in[-1,1]:
  x=side*.13;box('WholeCylinderMountEar_'+tag+str(side),(x-.025,p[1]-.055,p[2]-.065),(x+.025,p[1]+.055,p[2]+.035),0)
# Short fixed support strut beneath the elevated deck; no rated hydraulic function.
pipe('WholeFixedSafetyProp',[(.57,-.89,.12),decktr((.57,1.45,-.13))],.029,0,12)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
FM={n:[m]*len(f)for n,(v,f,m)in G.items()}
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
focus=Vector((0,0,.40))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.95;aim(cam,(6,-7,4.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/construction/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'interior','style':'S01-clean-geometric','title':'Fixed One Piece Up And Over Door','description':'One original complete fixed raised hinged-lip dock leveller exterior: low open receiving frame, rear pivot towers and continuous axle, one thick inclined deck with two underside beams, separate front hinged full-width lip, finite hinge knuckles, sloping cylinder/rod and mounting ears plus a fixed support prop. Unlike a solid ramp on wedges or a vertically translating scissor platform, the whole deck rises from its rear hinge and terminates in an independently tilted front lip. No old model meshes imported. Three opaque PBR materials, metre scale, true XY centred and frame soles on Z0. One static model, zero scenes; host dock and vehicle omitted. No hydraulic, movement, docking fit, load, installation, traffic or safety performance claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
