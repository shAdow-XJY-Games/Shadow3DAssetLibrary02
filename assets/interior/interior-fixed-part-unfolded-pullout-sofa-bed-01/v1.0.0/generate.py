import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='interior-fixed-part-unfolded-pullout-sofa-bed-01'
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

# Complete low sofa shell with its own partly unfolded three-section pullout bed.
PALETTE=[('MutedSageUpholsteredShell',(.30,.40,.34,1),.93,0),('WarmIvoryFoldingMattress',(.71,.69,.60,1),.96,0),('DarkFixedBedFrame',(.16,.19,.18,1),.58,.42)]
def softbox(name,lo,hi,b,mi):
 x0,y0,z0=lo;x1,y1,z1=hi;v=[];f=[]
 for z,ins in[(z0,b),(z0+b,0),(z1-b,0),(z1,b)]:
  l=x0+ins;r=x1-ins;t=y0+ins;u=y1-ins;c=b
  v +=[(l+c,t,z),(r-c,t,z),(r,t+c,z),(r,u-c,z),(r-c,u,z),(l+c,u,z),(l,u-c,z),(l,t+c,z)]
 for j in range(3):
  for i in range(8):k=(i+1)%8;a=j*8+i;bb=j*8+k;c=(j+1)*8+k;d=(j+1)*8+i;f.extend([(a,bb,c),(a,c,d)])
 for j in[0,3]:
  c=len(v);v.append(((x0+x1)/2,(y0+y1)/2,z0 if j==0 else z1))
  for i in range(8):k=(i+1)%8;f.append((c,j*8+k,j*8+i)if j==0 else(c,j*8+i,j*8+k))
 record(name,v,f,mi)
for x in[-.80,.80]:
 for y in[-.22,.39]:box('WholeSofaFoot_'+str((x,y)),(x-.055,y-.055,0),(x+.055,y+.055,.20),2)
for side in[-1,1]:
 softbox('WholeSofaArm_'+str(side),(side*.80-.105,-.36,.165),(side*.80+.105,.51,.73),.035,0)
 box('WholeInnerRearBedAnchor_'+str(side),(side*.70-.030,.16,.28),(side*.70+.030,.34,.47),2)
softbox('WholeRearSofaShell',(-.81,.30,.18),(.81,.55,.99),.035,0)
box('WholeRearUnderframe',(-.79,.18,.18),(.79,.44,.265),2)
for x in[-.35,.35]:softbox('WholeBackCushion_'+str(x),(x-.337,.20,.58),(x+.337,.36,.94),.026,0)
# Three whole connected open rectangular bed frames, not an imported separate bed beside a sofa.
def frame(name,half,length,mi):
 outer=[(-half,0),(half,0),(half,length),(-half,length)];inner=[(-half+.032,.032),(half-.032,.032),(half-.032,length-.032),(-half+.032,length-.032)]
 v=[(x,s,z)for r,z in[(outer,-.025),(outer,.025),(inner,.025),(inner,-.025)]for x,s in r];f=[]
 for i in range(4):
  k=(i+1)%4
  for q in[(i,k,k+4,i+4),(i+4,k+4,k+8,i+8),(i+8,k+8,k+12,i+12),(i+12,k+12,k,i)]:f.extend([(q[0],q[1],q[2]),(q[0],q[2],q[3])])
 record(name,v,f,mi)
sections=[('Rear',.25,.415,.72,0),('Middle',-.47,.415,.72,0),('FoldedFoot',-1.19,.415,.63,28)]
def tr(q,y,z,angle):x,s,n=q;a=math.radians(angle);return(x,y-s*math.cos(a)+n*math.sin(a),z+s*math.sin(a)+n*math.cos(a))
for label,y,z,length,angle in sections:
 length=.63 if label=='FoldedFoot'else.72
 name=label+'WholeBedFrame';frame(name,.70,length,2);vv,ff,m=G[name];record(name,[tr(p,y,z,angle)for p in vv],ff,m)
 for s in[.16,length/2,length-.16]:
  name=label+'WholeTransverseSupport_'+str(s);box(name,(-.677,s-.022,-.018),(.677,s+.022,.020),2);vv,ff,m=G[name];record(name,[tr(p,y,z,angle)for p in vv],ff,m)
 name=label+'WholeMattressSection';softbox(name,(-.665,.035,.024),(.665,length-.035,.145),.018,1);vv,ff,m=G[name];record(name,[tr(p,y,z,angle)for p in vv],ff,m)
# Finite hinge pins at both real fold joins and the rear anchors.
for y in[.25,-.47,-1.19]:
 for side in[-1,1]:
  pipe('WholeBedFrameHingePin_'+str((y,side)),[(side*.665,y,.415),(side*.737,y,.415)],.024,2,16)
# Two complete U support legs, their whole bottom transverse bars are grounded.
for y in[-.47,-1.19]:
 pad('WholeGroundedUFrame_'+str(y),[(-.69,0),(.69,0),(.69,.425),(.642,.425),(.642,.045),(-.642,.045),(-.642,.425),(-.69,.425)],y-.022,y+.022,2)
# Short rear pullout links connect the unfolded carrier to its own low sofa anchors.
for side in[-1,1]:pipe('WholeRearCarrierLink_'+str(side),[(side*.70,.25,.415),(side*.70,.08,.30),(side*.70,-.20,.35)],.018,2,12)
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
focus=Vector((0,0,.48))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.15;aim(cam,(7,-6,6.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/interior/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'interior','style':'S01-clean-geometric','title':'Fixed Part Unfolded Pullout Sofa Bed','description':'One original complete sofa with its own partly unfolded pullout bed carrier. A low upholstered back shell, two complete arms, rear underframe, anchor blocks and four feet surround the rear section of one continuous three-frame folding assembly. Two whole rectangular bed frames lie out in front on two complete grounded U supports, while the third whole foot frame remains angled upward about its real end-to-end hinge pins. Three separate thick mattress sections rest on their respective complete open frames and cross supports; rear carrier links join the assembly to the sofa anchors. No imported sofa or separate bed is placed as a scene. This low internally folding carrier differs from the ordinary fixed two-seat sofa and tall cabinet wall-bed with one full pivoting mattress. Three constant opaque PBR materials, metres Z up, true XY envelope centred, grounded soles, one complete prop and zero scenes. Fixed partly unfolded appearance only; no sleeping surface usability, full folding clearance, pullout travel, upholstery simulation, comfort, load, balance, installation or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
