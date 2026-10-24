import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='interior-fixed-one-piece-upover-door-01'
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

# One complete rigid-panel up-and-over door in a single fixed partly raised pose.
PALETTE=[('FrameWarmGrey',(.51,.55,.53,1),.62,.22),('WholeDoorMutedBlue',(.22,.36,.39,1),.64,.15),('RollersAndLinksDarkMetal',(.15,.19,.20,1),.45,.56)]
for side in[-1,1]:
 x=side*1.38;box('WholeGroundedJamb_'+str(side),(x-.065,-.10,0),(x+.065,.13,2.46),0)
box('WholeHeader',(-1.318,-.095,2.32),(1.318,.125,2.46),0)
# Complete straight inward-open overhead channels, not the curved tracks of segmented doors.
profile=[(-.05,-.07),(.05,-.07),(.05,.07),(-.05,.07),(-.05,.045),(.02,.045),(.02,-.045),(-.05,-.045)]
for side in[-1,1]:
 n='WholeStraightSlottedOverheadTrack_'+str(side);pad(n,profile,.035,1.78,2);vv,ff,m=G[n];record(n,[(side*(1.29+x),y,2.20+z)for x,y,z in vv],ff,m)
 for y in[.09,1.66]:box('WholeOverheadTrackBracket_'+str((side,y)),(min(side*1.29,side*1.38),y-.035,2.245),(max(side*1.29,side*1.38),y+.035,2.33),0)
box('WholeRearCrossTie',(-1.40,1.63,2.29),(1.40,1.71,2.37),0)
# Single rigid whole panel, no division into hinged sections.
B=(0,-.55,1.28);D=(0,math.sqrt(1-(.92/2.24)**2),.92/2.24);PN=(0,-D[2],D[1])
def paneltr(q):x,t,n=q;return add(add(B,(x,0,0)),add(mul(D,t),mul(PN,n)))
box('WholeRigidDoorPanel',(-1.22,0,-.030),(1.22,2.24,.030),1);vv,ff,m=G['WholeRigidDoorPanel'];record('WholeRigidDoorPanel',[paneltr(q)for q in vv],ff,m)
# Integral-looking full back braces and perimeter stiffeners remain on this one rigid leaf.
for x in[-1.16,1.16]:
 n='WholeLeafEdgeStiffener_'+str(x);box(n,(x-.025,.035,.024),(x+.025,2.205,.067),0);vv,ff,m=G[n];record(n,[paneltr(q)for q in vv],ff,m)
for t in[.065,1.12,2.175]:
 n='WholeLeafCrossStiffener_'+str(t);box(n,(-1.135,t-.025,.026),(1.135,t+.025,.063),0);vv,ff,m=G[n];record(n,[paneltr(q)for q in vv],ff,m)
# Top-end captive rollers guide the rigid leaf; middle side swing links carry its distinct pivot route.
T=paneltr((0,2.24,0));M=paneltr((0,.92,0))
for side in[-1,1]:
 pipe('WholeUpperRollerAxle_'+str(side),[(side*1.19,T[1],T[2]),(side*1.305,T[1],T[2])],.014,2,12)
 wheel('WholeUpperTrackRoller_'+str(side),side*1.29,T[1],T[2],.045,0,.035,2)
 x=side*1.275;aa=(x,.035,1.04);bb=(x,M[1],M[2]);
 # One complete flat finite swing arm between two fixed side pivots.
 dy=bb[1]-aa[1];dz=bb[2]-aa[2];le=math.hypot(dy,dz);uy=-dz/le*.033;uz=dy/le*.033
 poly=[(aa[1]+uy,aa[2]+uz),(aa[1]-uy,aa[2]-uz),(bb[1]-uy,bb[2]-uz),(bb[1]+uy,bb[2]+uz)]
 n='WholeSideSwingArm_'+str(side);pad(n,poly,x-.018,x+.018,2);vv,ff,m=G[n];record(n,[(yy,u,z)for u,yy,z in vv],ff,m)
 pipe('WholeJambSwingPin_'+str(side),[(side*1.24,.035,1.04),(side*1.39,.035,1.04)],.032,2,16)
 pipe('WholeLeafSwingPin_'+str(side),[(side*1.20,M[1],M[2]),(side*1.30,M[1],M[2])],.029,2,16)
 # Fixed visible closed counterbalance-link exterior; no spring rate or actuation claim.
 pipe('WholeFixedCounterbalanceCase_'+str(side),[(side*1.335,.04,.24),(side*1.335,.04,.79)],.040,2,16)
 pipe('WholeCounterbalanceLink_'+str(side),[(side*1.335,.04,.77),(side*1.335,.035,1.04)],.015,2,12)
pipe('WholeLowerLeafPull',[paneltr((-.14,.12,-.024)),paneltr((-.14,.12,-.090)),paneltr((.14,.12,-.090)),paneltr((.14,.12,-.024))],.014,2,12)
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
focus=Vector((0,0,1.20))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.85;aim(cam,(6,-8,4.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/interior/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'interior','style':'S01-clean-geometric','title':'Fixed One Piece Up And Over Door','description':'One original complete rigid one-piece up-and-over doorway appearance held in a partly raised pose. Two full grounded jambs and header support straight inward-open overhead channels and a rear tie. A single whole thick rigid door panel, with full rear stiffeners and one lower pull, is guided by two top-end rollers and separately connected at middle side points to two whole swing arms on finite jamb pivots. Fixed counterbalance-case and short link exteriors flank the opening. The rigid leaf projects forward at its lower end while its upper rollers sit back in straight tracks. This is not the old chain of ten hinged door sections in curved return tracks, nor two leaves folding around vertical hinges; no old door meshes are imported. Three constant opaque PBR materials, metres Z up, true XY envelope-centred and grounded jamb soles at Z0; one complete static module, zero scenes, no host building. No opening animation, full motion clearance, spring behaviour, motor, roller-load fit, support load, weather, accessibility, anti-pinch, installation or safety certification claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
