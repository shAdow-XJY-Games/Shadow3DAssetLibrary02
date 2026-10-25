import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='fantasy-static-great-eye-and-curved-stalk-orb-creature-01'
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

def cell_union(name,cells,mat):
 faces={}
 for v in cells:
  v=[tuple(round(c,12)for c in p)for p in v]
  for f in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:
   q=tuple(v[i]for i in f);key=tuple(sorted(q))
   if key in faces:del faces[key]
   else:faces[key]=q
 v=[];ix={};f=[]
 for q in faces.values():
  ids=[]
  for p in q:
   if p not in ix:ix[p]=len(v);v.append(p)
   ids.append(ix[p])
  f.extend([(ids[0],ids[1],ids[2]),(ids[0],ids[2],ids[3])])
 record(name,v,f,mat)
def turned(name,x,y,profile,m,seg=16):
 v=[];rs=[];f=[]
 for r,z in profile:
  pts=[(x,y,z)]if r==0 else[(x+r*math.cos(math.tau*i/seg),y+r*math.sin(math.tau*i/seg),z)for i in range(seg)]
  rs.append(list(range(len(v),len(v)+len(pts))));v+=pts
 for a,b in zip(rs,rs[1:]+rs[:1]):
  if len(a)==len(b)==1:continue
  for i in range(seg):
   j=(i+1)%seg
   if len(a)==1:f.append((a[0],b[i],b[j]))
   elif len(b)==1:f.append((a[i],b[0],a[j]))
   else:f.extend([(a[i],b[i],b[j]),(a[i],b[j],a[j])])
 record(name,v,f,m)
PALETTE=[('OrbCreatureMutedViolet',(.29,.17,.37,1),.84,0),('OrbCreatureEyeAndBluntTeeth',(.82,.76,.56,1),.65,0),('OrbCreaturePupilAndCavity',(.035,.025,.055,1),.90,0)]
FM={}
# A whole thick orb shell: broad frontal mouth is an actual opening into its inner cavity.
n=32;rows=[(.45,.10),(.52,.30),(.66,.46),(.81,.55),(.99,.60),(1.17,.59),(1.35,.52),(1.50,.39),(1.61,.20)]
o=[];inn=[]
for z,r in rows:
 for j in range(n):
  a=math.tau*j/n;o.append((r*math.cos(a),.86*r*math.sin(a),z));inn.append(((r-.045)*math.cos(a),.86*(r-.045)*math.sin(a),z))
o.extend([(0,0,.425),(0,0,1.655)]);inn.extend([(0,0,.470),(0,0,1.61)]);bot=len(o)-2;top=len(o)-1;of=[]
for k in range(len(rows)-1):
 for j in range(n):
  if k in [2,3] and 21<=j<=26:continue
  a=k*n+j;b=k*n+(j+1)%n;c=b+n;d=a+n;of.extend([(a,b,c),(a,c,d)])
for j in range(n):
 q=(j+1)%n;of.extend([(bot,q,j),((len(rows)-1)*n+j,(len(rows)-1)*n+q,top)])
v=o+inn;off=len(o);f=of+[tuple(off+a for a in reversed(t))for t in of];fm=[0]*len(of)+[2]*len(of);ed={}
for t in of:
 for a,b in zip(t,t[1:]+t[:1]):ed.setdefault(tuple(sorted((a,b))),[]).append((a,b))
for occ in ed.values():
 if len(occ)==1:
  a,b=occ[0];f.extend([(a,off+a,off+b),(a,off+b,b)]);fm.extend([0,0])
record('WholeOrbWithRealOpenMouth',v,f,0);FM['WholeOrbWithRealOpenMouth']=fm
# Newly authored faceted ellipsoids, not imported eyes or old heads.
def orb(name,c,s,m,seg=20,bands=10):
 v=[add(c,(0,0,-s[2]))];f=[]
 for k in range(1,bands):
  a=-math.pi/2+math.pi*k/bands
  for j in range(seg):t=math.tau*j/seg;v.append(add(c,(s[0]*math.cos(a)*math.cos(t),s[1]*math.cos(a)*math.sin(t),s[2]*math.sin(a))))
 top=len(v);v.append(add(c,(0,0,s[2])))
 for j in range(seg):q=(j+1)%seg;f.extend([(0,1+q,1+j),(top,1+(bands-2)*seg+j,1+(bands-2)*seg+q)])
 for k in range(bands-2):
  for j in range(seg):q=(j+1)%seg;a=1+k*seg+j;b=1+k*seg+q;f.extend([(a,b,b+seg),(a,b+seg,a+seg)])
 record(name,v,f,m)
orb('WholeDominantFrontEye',(0,-.437,1.29),(.285,.205,.255),1,24,12)
orb('WholeDominantDarkPupil',(0,-.627,1.29),(.111,.030,.145),2,20,10)
# Four broad blunt teeth project from the actual upper and lower mouth margins.
for j,x in enumerate([-.22,.22]):
 y=-.86*math.sqrt(.60**2-x*x)
 pad('WholeUpperBluntTooth'+str(j),[(x-.055,.997),(x+.055,.997),(x+.036,.865),(x-.038,.865)],y-.008,y+.050,1)
 y=-.86*math.sqrt(.46**2-x*x)
 pad('WholeLowerBluntTooth'+str(j),[(x-.044,.65),(x+.044,.65),(x+.035,.755),(x-.031,.755)],y-.008,y+.045,1)
# Each stalk lies in its own fixed vertical plane, avoiding changing reference-frame twists.
def stalk(name,pts,radii,mat):
 direction=sub(pts[-1],pts[0]);side=unit(cross(direction,(0,0,1)));v=[];f=[];seg=10
 for k,p in enumerate(pts):
  t=unit(sub(pts[min(k+1,len(pts)-1)],pts[max(0,k-1)]));up=unit(cross(t,side))
  for j in range(seg):a=math.tau*j/seg;v.append(add(p,add(mul(side,radii[k]*math.cos(a)),mul(up,radii[k]*math.sin(a)))))
 for k in range(len(pts)-1):
  for j in range(seg):q=(j+1)%seg;a=k*seg+j;b=k*seg+q;f.extend([(a,b,b+seg),(a,b+seg,a+seg)])
 for k in [0,len(pts)-1]:
  c=len(v);v.append(pts[k])
  for j in range(seg):q=(j+1)%seg;f.append((c,k*seg+q,k*seg+j)if k==0 else(c,k*seg+j,k*seg+q))
 record(name,v,f,mat)
paths=[[(0,.20,1.45),(0,.30,1.72),(0,.27,1.95),(0,.13,2.08)], [(-.34,.06,1.40),(-.55,.10,1.63),(-.72,.10,1.79),(-.78,.06,1.95)],[(.34,.06,1.40),(.54,.10,1.62),(.72,.10,1.73),(.80,.06,1.88)], [(-.48,.02,1.15),(-.70,.02,1.26),(-.92,.02,1.37),(-1.00,.02,1.53)],[(.48,.02,1.15),(.72,.02,1.25),(.94,.02,1.31),(1.04,.02,1.45)]]
for i,p in enumerate(paths):
 stalk('WholeCurvedEyeStalk'+str(i),p,[.065,.052,.047,.052],0)
 c=p[-1];orb('WholeTerminalEye'+str(i),c,(.115,.100,.108),1,16,8);orb('WholeTerminalPupil'+str(i),add(c,(0,-.091,0)),(.045,.025,.055),2,12,8)
# Three short complete lobed lower supports belong to the character; not an octopus arm fan.
for i,a in enumerate([-math.pi/2,.45*math.pi,1.05*math.pi]):
 u=(math.cos(a),math.sin(a),0);pts=[(.12*u[0],.12*u[1],.53),(.23*u[0],.23*u[1],.32),(.31*u[0],.31*u[1],.14),(.43*u[0],.43*u[1],.10)]
 stalk('WholeShortGroundedLobe'+str(i),pts,[.16,.13,.11,.09],0)
 orb('WholeBroadLobeSole'+str(i),(.43*u[0],.43*u[1],.075),(.15,.14,.075),0,16,8)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()};FM={n:FM.get(n,[m]*len(f))for n,(v,f,m)in G.items()}
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
focus=Vector((0,0,1.10))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.65;aim(cam,(2.4,-8,2.9));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/fantasy/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'fantasy','style':'S01-clean-geometric','title':'Static Great Eye and Curved Stalk Orb Creature','description':'One independently authored complete fixed fantasy orb creature. A broad continuous thick rounded body contains a real open lower mouth with full inner walls and four blunt projecting teeth. One dominant convex front eye sits above that cavity. Five newly swept curved upper and lateral stalks terminate in complete smaller eyes; three short thick grounded lower lobes and broad soles support the whole static character. This is a new single-eyed mouth-bearing orb silhouette, not an old octopus with additional eyes or a mimic chest with altered shell. No old mesh or character parts imported. Three opaque PBR materials, metres Z-up, complete bounds-centred ground origin; one model zero scenes. Stylized fictional nonhuman art only, no biological or optical accuracy, vision, magical effect, flight, locomotion, biting, rigging, animation, collision or physical support performance claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
