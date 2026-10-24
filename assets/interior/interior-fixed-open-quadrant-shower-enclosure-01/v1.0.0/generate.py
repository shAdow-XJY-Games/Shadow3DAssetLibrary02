import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='interior-fixed-open-quadrant-shower-enclosure-01'
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

# One whole quadrant shower enclosure, fixed partly-open sliding pose.
PALETTE=[('IvoryTrayAndBackPanels',(.66,.68,.65,1),.58,.05),('MutedMetalRailsAndControls',(.23,.29,.30,1),.43,.55),('OpaquePaleBlueScreens',(.31,.48,.51,1),.38,.05)]
O=(-.56,.56)
def P(r,a,z):a=math.radians(a);return(O[0]+r*math.cos(a),O[1]-r*math.sin(a),z)
def arcsolid(name,ri,ro,a0,a1,z0,z1,m,n=24):
 v=[P(r,a0+(a1-a0)*i/n,z)for z in[z0,z1]for i in range(n+1)for r in[ri,ro]];f=[];stride=2*(n+1)
 for i in range(n):
  a=2*i;b=a+2
  for q in[(a,b,b+1,a+1),(a+stride,a+1+stride,b+1+stride,b+stride),(a,a+stride,b+stride,b),(a+1,b+1,b+1+stride,a+1+stride)]:f.extend([(q[0],q[1],q[2]),(q[0],q[2],q[3])])
 for q in[(0,1,1+stride,stride),(2*n,2*n+stride,2*n+1+stride,2*n+1)]:f.extend([(q[0],q[1],q[2]),(q[0],q[2],q[3])])
 record(name,v,f,m)
# Full deep-low tray: full bottom, inner floor and continuous raised perimeter with genuine recess.
n=32;R=1.10;t=.045;ri=R-t;aa=math.degrees(math.asin(t/ri))
outer=[(O[0],O[1])]+[(P(R,90*i/n,0)[0],P(R,90*i/n,0)[1])for i in range(n+1)]
inner=[(O[0]+t,O[1]-t)]+[(P(ri,aa+(90-2*aa)*i/n,0)[0],P(ri,aa+(90-2*aa)*i/n,0)[1])for i in range(n+1)]
outer.reverse();inner.reverse()
v=[(x,y,z)for ring,z in[(outer,0),(outer,.13),(inner,.13),(inner,.055)]for x,y in ring];nn=len(outer);f=[]
for j in range(3):
 for i in range(nn):
  k=(i+1)%nn;a=j*nn+i;b=j*nn+k;c=(j+1)*nn+k;d=(j+1)*nn+i;f.extend([(a,b,c),(a,c,d)])
for a,b,c in earclip(outer):f.append((c,b,a))
for a,b,c in earclip(inner):f.append((3*nn+a,3*nn+b,3*nn+c))
record('WholeRecessedQuadrantTray',v,f,0)
# Two full rear infills form the corner, not a room or imported host walls.
box('WholeLeftRearPanel',(O[0]+.014,O[1]-1.03,.115),(O[0]+.039,O[1]-.025,2.02),0)
box('WholeRightRearPanel',(O[0]+.030,O[1]-.039,.115),(O[0]+1.03,O[1]-.014,2.02),0)
for x,y,label in[(O[0]+.025,O[1]-.025,'RearCorner'),(*P(1.025,0,0)[:2],'SideJamb0'),(*P(1.025,90,0)[:2],'SideJamb90')]:
 box('WholeUpright_'+label,(x-.027,y-.027,.116),(x+.027,y+.027,2.08),1)
# Two actual separated track radii at top and bottom; no central revolving shaft or radial leaves.
for label,z0,z1 in[('Lower',.115,.160),('Upper',2.035,2.09)]:
 arcsolid('WholeOuter'+label+'ArcRail',1.000,1.045,0,90,z0,z1,1)
 arcsolid('WholeInner'+label+'ArcRail',.926,.966,0,90,z0+.003,z1-.003,1)
# Complete static outer curved screen and one offset inner curved sliding leaf.
for label,r,a0,a1 in[('Fixed',1.022,45,90),('Sliding',.947,30,75)]:
 arcsolid(label+'WholeOpaqueCurvedInfill',r-.006,r+.006,a0,a1,.205,1.985,2,20)
 for zz in[.174,2.000]:arcsolid(label+'WholeCurvedSashRail_'+str(zz),r-.020,r+.020,a0-.4,a1+.4,zz-.022,zz+.022,1,20)
 for a in[a0,a1]:
  x,y,_=P(r,a,0);box(label+'WholeEndStile_'+str(a),(x-.020,y-.020,.154),(x+.020,y+.020,2.026),1)
# Lower and upper short captive slider blocks connect the displayed inner sash to its dedicated track.
for a in[34,71]:
 for z in[.156,2.028]:
  x,y,_=P(.947,a,0);box('WholeFiniteGuideBlock_'+str((a,z)),(x-.020,y-.020,z-.018),(x+.020,y+.020,z+.018),1)
# Pull mounted at the leading edge, outside the opaque sash.
x,y,_=P(.974,31,0)
pipe('WholeLeadingPullHandle',[(x,y,.90),(x+.035,y-.025,.90),(x+.035,y-.025,1.12),(x,y,1.12)],.011,1,12)
# Own complete fixed shower fittings on the back panel, no water or live plumbing.
pipe('WholeBackRiser',[(O[0]+.095,O[1]-.25,.88),(O[0]+.095,O[1]-.25,1.79),(O[0]+.27,O[1]-.25,1.91),(O[0]+.36,O[1]-.25,1.91)],.018,1,16)
pipe('WholeDownwardHead',[(O[0]+.36,O[1]-.25,1.88),(O[0]+.36,O[1]-.25,1.91)],.075,1,24)
box('WholeFixedMixer',(O[0]+.028,O[1]-.30,.85),(O[0]+.12,O[1]-.20,.94),1)
pipe('WholeShallowDrainCap',[(O[0]+.26,O[1]-.26,.054),(O[0]+.26,O[1]-.26,.059)],.038,1,20)
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
focus=Vector((0,0,1.02))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.65;aim(cam,(7,-3,3.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/interior/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'interior','style':'S01-clean-geometric','title':'Fixed Open Quadrant Shower Enclosure','description':'One original complete fixed partly-open quarter-round shower enclosure appearance. A single thick quadrant tray has a full inner floor, outer sole and continuously raised recessed rim. Two complete back infills meet at a corner, three full upright posts carry separated inner and outer curved guide rails at top and bottom, and one whole fixed curved opaque screen overlaps a second complete inner-radius framed sliding leaf. The leading leaf is held away from the side jamb, leaving a real broad arc entry; short finite guide blocks and an external grip complete its shown support route. Newly authored fixed rear riser, shower head and mixer are included. Not an old standalone beach shower, resized bath, or cylindrical four-wing central revolving entrance; no prior mesh imported. Three opaque PBR materials, metres Z up, whole XY bounds centred and tray sole at Z0; one complete prop, zero scenes. No transparency, water, working drain, plumbing, slider animation, weather or water seal, hygiene, user fit, installation, support load or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
