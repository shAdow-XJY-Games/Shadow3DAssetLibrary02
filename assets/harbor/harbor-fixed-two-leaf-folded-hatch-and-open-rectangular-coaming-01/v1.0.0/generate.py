import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='harbor-fixed-two-leaf-folded-hatch-and-open-rectangular-coaming-01'
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
PALETTE=[('WholeCoamingMutedMarineBlue',(.14,.27,.29,1),.71,.25),('WholeFoldedPanelsWarmLightGrey',(.54,.57,.55,1),.76,.15),('WholeRailsAndFixedBearings',(.23,.29,.30,1),.56,.55),('WholeRollersAndHingeAxles',(.07,.11,.13,1),.51,.64)]
FM={};ROOTS=['WholeOpenRectangularCoaming'];CONTACTS=[];LINKS=[];GAPS=[];SHIFT=(0,0,0)
def points7(p,e=.003):return[p]+[tuple(p[j]+(e*sign if j==axis else 0)for j in range(3))for axis in range(3)for sign in[-1,1]]
def link(a,b,p):LINKS.append((a,b,points7(p)))
# One whole closed rectangular coaming ring with real through opening, not four loose walls.
v=[]
for z in[0,.60]:
 for xx,yy in[(1.80,1.40),(1.55,1.10)]:v.extend([(-xx,-yy,z),(xx,-yy,z),(xx,yy,z),(-xx,yy,z)])
f=[]
for i in range(4):
 j=(i+1)%4
 for a,b,c,d in[(i,j,j+4,i+4),(i+8,i+12,j+12,j+8),(i,i+8,j+8,j),(i+4,j+4,j+12,i+12)]:f.extend([(a,b,c),(a,c,d)])
record(ROOTS[0],v,f,0)
for sy in[-1,1]:
 y=sy*1.25;rail='WholeLongitudinalRollerRail_'+str(sy);stool='WholeFixedEndHingeStool_'+str(sy);box(rail,(-1.72,y-.10,.60),(1.72,y+.10,.68),2);box(stool,(-1.72,y-.08,.68),(-1.48,y+.08,1.06),2)
 CONTACTS.extend([(ROOTS[0],rail,(0,y,.60),(0,0,1),.68),(rail,stool,(-1.60,y,.68),(0,0,1),.038)])
# Three full transverse retained-looking fixed axes join two complete folded panels.
A=(-1.60,0,.94);B=(-.95,0,2.34);C=(-.30,0,.94)
for name,p,r in[('WholeFixedEndHingeAxle',A,.14),('WholeRaisedPanelPairHingeAxle',B,.18),('WholeMovingEndRollerAxle',C,.14)]:pipe(name,[(p[0],-1.44,p[2]),(p[0],1.44,p[2])],r,3,16)
def panel(name,p,q,cutstart,cutend):
 d=unit(sub(q,p));n=(-d[2],0,d[0]);v=[]
 for t in[cutstart,math.sqrt(dot(sub(q,p),sub(q,p)))-cutend]:
  for y,norm in[(-1.16,-.055),(1.16,-.055),(1.16,.055),(-1.16,.055)]:v.append(add(add(p,mul(d,t)),add((0,y,0),mul(n,norm))))
 f=[(0,2,1),(0,3,2),(4,5,6),(4,6,7)]
 for i in range(4):j=(i+1)%4;f.extend([(i,j,j+4),(i,j+4,i+4)])
 record(name,v,f,1);return d
DA=panel('WholeRisingFixedEndCoverPanel',A,B,.11,.14);DB=panel('WholeReturningMovingEndCoverPanel',B,C,.14,.11)
for sy in[-1,1]:link('WholeFixedEndHingeStool_'+str(sy),'WholeFixedEndHingeAxle',(-1.60,sy*1.25,.94))
link('WholeFixedEndHingeAxle','WholeRisingFixedEndCoverPanel',add(A,mul(DA,.12)))
link('WholeRisingFixedEndCoverPanel','WholeRaisedPanelPairHingeAxle',sub(B,mul(DA,.15)))
link('WholeRaisedPanelPairHingeAxle','WholeReturningMovingEndCoverPanel',add(B,mul(DB,.15)))
link('WholeReturningMovingEndCoverPanel','WholeMovingEndRollerAxle',sub(C,mul(DB,.12)))
# Whole16-facet fixed rollers have exact finite flat undersides on their complete rails.
for sy in[-1,1]:
 y=sy*1.25;name='WholeFlatFacetRailRoller_'+str(sy);v=[];NROLL=16;RROLL=.26/math.cos(math.pi/NROLL)
 for yy in[y-.08,y+.08]:
  for i in range(NROLL):a=math.tau*(i+.5)/NROLL;v.append((C[0]+RROLL*math.sin(a),yy,C[2]+RROLL*math.cos(a)))
 f=[]
 for i in range(NROLL):j=(i+1)%NROLL;f.extend([(i,j,j+NROLL),(i,j+NROLL,i+NROLL)])
 for k in[0,1]:
  c=len(v);v.append((C[0],y+(-.08 if k==0 else .08),C[2]));base=k*NROLL
  for i in range(NROLL):j=(i+1)%NROLL;f.append((c,base+j,base+i)if k==0 else(c,base+i,base+j))
 record(name,v,f,3);link('WholeMovingEndRollerAxle',name,(C[0],y,C[2]));CONTACTS.append(('WholeLongitudinalRollerRail_'+str(sy),name,(C[0],y,.68),(0,0,1),.016))
for x in[.15,.70,1.30]:
 for y in[-.8,0,.8]:GAPS.append(dict(label='OpenRectangularHatchExposedVerticalBay',origin_m=[x,y,.01],direction=[0,0,1],length_m=2.7))
for z in[1.25,1.65]:GAPS.append(dict(label='SelectedFoldedPanelTriangleCrossway',origin_m=[-.95,-1.6,z],direction=[0,1,0],length_m=3.2))
GAPS += [dict(label='WholeCoamingWallSolidControl',origin_m=[1.70,0,.01],direction=[0,0,1],length_m=.8,blocked=True),dict(label='WholeRisingPanelSolidControl',origin_m=[-1.20,0,.01],direction=[0,0,1],length_m=2.7,blocked=True)]
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
focus=Vector((0,0,1.2))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=5.4;aim(cam,(-7,-11,5.2) if view=='qa-front' else (8,-10,7.8));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/harbor/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'modular','theme':'harbor','style':'S01-clean-geometric','title':'Fixed Two Leaf Folded Hatch and Open Rectangular Coaming','description':'One newly authored complete static folded marine-hatch module. A whole continuous thick low rectangular coaming surrounds an actual full-depth open hatch void, with no floor or inserted dark plane. Two complete longitudinal rails sit on the side rims. Two whole thick full-width cover panels form one raised folding pair near one end: the first rises from a fixed end axis to a full high transverse inter-panel axis; the second returns downward to a third full axle carrying two complete flat-facet rollers seated on the rails. Two whole fixed end stools carry the first axle. The long remaining rectangular hatch area is genuinely uncovered, while a real open triangular space remains between the folded panels below the raised hinge. All twelve whole closed meshes and every visible coordinate are newly authored together; no old door, lid, panel, folding table, roof, rail, roller or ship fragment imported or cropped. Unlike the upright single-leaf fixed-open airlock, this is a horizontal whole coaming with a coupled pitched two-leaf cover, high transverse fold axis and rail-supported moving end; unlike the four-panel flat garment table there is no central workboard, hand slot, connector web or table legs. Six finite opposed coaming-to-rail, rail-to-stool and rail-to-roller seats and eight selected sevenpoint embedded static joint groups root all parts to the complete coaming sole. Four opaque constant PBR materials, native metre-style Z up and full horizontal bounds-centred ground origin, one independent architectural/marine module zero scenes. Generic folding-pair hatch vocabulary only, original proportions not a named product, ship, measured hardware or build specification. Simplified thick panel exteriors and deliberately embedded axes represent one fixed display pose, not complete bearing or hinge construction. No hydraulic actuator, drive, locks, seals, cleats, full ship, deck cargo, cargo hold, occupants or water included. No continuous opening/closing trajectory, closed-cover fit, roller motion, hinge articulation, pressure or weather seal, flooding protection, cargo capacity, mechanical balance, structural loading, manufacture, installation, deck access or marine/public safety capability made or verified. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
