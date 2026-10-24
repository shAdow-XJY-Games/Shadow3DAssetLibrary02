import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='military-fixed-splayed-five-finger-plate-gauntlet-01'
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

# Complete static five-finger plate gauntlet, dorsal side upward.
PALETTE=[('GauntletBrushedSteel',(.31,.36,.39,1),.46,.70),('GauntletDarkUnderlayer',(.065,.055,.045,1),.88,0),('GauntletWarmRivets',(.46,.31,.12,1),.52,.60)]
SEG=16
# One cuff/palm material shell, genuine wrist cavity, closed forward palm.
prof=[(-.24,.088,.060),(-.205,.082,.055),(-.13,.055,.034),(-.045,.072,.031),(.075,.073,.027)]
def ell(y,rx,rz):return[(rx*math.cos(math.tau*i/SEG),y,.072+rz*math.sin(math.tau*i/SEG))for i in range(SEG)]
rings=[ell(y,rx,rz)for y,rx,rz in prof]+[[(0,.075,.072)],[(0,.056,.072)]]+[ell(y,rx-.006,rz-.006)for y,rx,rz in reversed(prof[:-1]+[(.056,.068,.027)])]
v=[];ix=[]
for rr in rings:ix.append(list(range(len(v),len(v)+len(rr))));v+=rr
f=[]
for a,b in zip(ix,ix[1:]+ix[:1]):
 if len(a)==len(b)==1:continue
 for i in range(SEG):
  j=(i+1)%SEG
  if len(a)==1:f.append((a[0],b[i],b[j]))
  elif len(b)==1:f.append((a[i],b[0],a[j]))
  else:f.extend([(a[i],b[i],b[j]),(a[i],b[j],a[j])])
record('WholeFlaredOpenCuffAndPalmShell',v,f,0)
# Each finger is an independently closed continuous underlayer, with separate rigid dorsal plates.
def finger(label,pts,r):
 pipe(label+'WholeUnderFinger',pts,r,1,8)
 for k,(a,b)in enumerate(zip(pts,pts[1:])):
  d=unit(sub(b,a));u=unit(cross(d,(0,0,1)));w=cross(u,d)
  if w[2]<0:w=mul(w,-1)
  # Closed solid curved-width dorsal plate, each spans one phalanx only.
  corners=[(-1,0),(-.7,.70),(0,1),(.7,.70),(1,0)]
  vv=[]
  for p in[a,b]:
   for layer in[0,1]:
    for x,z in corners:vv.append(add(p,add(mul(u,x*r*1.04),mul(w,z*r+(.003 if layer else 0)))))
  ff=[];n=5
  # Cross-section around outer arch then reversed inner arch; prism along finger.
  poly=list(range(5))+list(reversed(range(5,10)))
  # End caps use a guaranteed strip pairing, avoiding concave fan.
  for end in[0,10]:
   for i in range(4):
    q=(end+i,end+i+1,end+5+i+1,end+5+i)
    if end==0:q=tuple(reversed(q))
    ff.extend([(q[0],q[1],q[2]),(q[0],q[2],q[3])])
  for i,j in zip(poly,poly[1:]+poly[:1]):ff.extend([(i,j,j+10),(i,j+10,i+10)])
  record(label+'DorsalPlate'+str(k+1),vv,ff,0)
 # Small closed dorsal knuckle fastener embedded in the palm end.
 p=pts[0];pipe(label+'KnuckleRivet',[(p[0],p[1],p[2]+r-.001),(p[0],p[1],p[2]+r+.004)],.004,2,8)
for label,x,L,spread in[('Index',-.052,.155,-.016),('Middle',-.017,.180,-.003),('Ring',.020,.165,.010),('Little',.054,.130,.028)]:
 pts=[(x,.068,.070),(x+spread*.35,.068+L*.38,.067),(x+spread*.70,.068+L*.73,.047),(x+spread,.068+L,.031)]
 finger(label,pts,.013 if label!='Little' else .011)
finger('Thumb',[(-.065,-.025,.065),(-.106,.006,.057),(-.136,.044,.041),(-.142,.082,.028)],.016)
# Two closed cuff borders retain the true open wrist, not a capped cylinder.
for name,y,rx,rz in[('WideCuffRim',-.236,.089,.061),('NarrowWristBinding',-.139,.059,.038)]:
 rr=[ell(y-.003,rx,rz),ell(y+.003,rx,rz),ell(y+.003,rx-.004,rz-.004),ell(y-.003,rx-.004,rz-.004)];vv=[p for ring in rr for p in ring];ff=[]
 for k in range(4):
  for i in range(SEG):j=(i+1)%SEG;a=k*SEG+i;b=k*SEG+j;c=((k+1)%4)*SEG+j;d=((k+1)%4)*SEG+i;ff.extend([(a,b,c),(a,c,d)])
 record(name,vv,ff,2)
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
focus=Vector((0,0,.065))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.63;aim(cam,(4,-7,6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/military/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'military','style':'S01-clean-geometric','title':'Fixed Splayed Five Finger Plate Gauntlet','description':'One complete original static five-finger metal gauntlet display: a single changing-width flared cuff and palm shell retains an explicit open wrist cavity, four separately splayed and gently curved continuous finger forms plus one lateral thumb carry fifteen solid dorsal plate segments and five small knuckle fasteners. Two complete annular cuff borders retain the wrist opening. The under-finger forms are solid display volumes, not claimed to provide wearable finger channels or functioning articulation. This is not the old closed padded boxing fist or a robot arm with two stepped jaws. All geometry newly authored, three opaque constant PBR materials, metres, ground datum and horizontal bounds centred. One model, no wearer or second glove. Nonweapon costume and military-fantasy art only: no hand fit, precise anatomy, working joints, protective or impact performance, manufacturing or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
