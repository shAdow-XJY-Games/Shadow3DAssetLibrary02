import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='harbor-fixed-battered-hollow-piles-and-through-hatch-cap-01'
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
PALETTE=[('WholeBatteredPileOuter',(.13,.23,.25,1),.72,.38),('WholePileInnerAndEndRing',(.075,.11,.12,1),.82,.22),('WholePiercedCapWarmConcrete',(.49,.46,.39,1),.89,0)]
FM={};ROOTS=[];CONTACTS=[];GAPS=[];SHIFT=(0,0,0);HEIGHT=3.4
# Four entire true constant-normal-thickness cylindrical tubes, capped only at their material end rings.
# Their end planes are horizontal ellipses, not slanted uncut tips on a ground plane.
for sx in[-1,1]:
 for sy in[-1,1]:
  name='WholeBatteredHollowPile_'+str(sx)+'_'+str(sy);ROOTS.append(name);a=(sx*1.7,sy*1.7,0);b=(sx*1.05,sy*1.05,HEIGHT);d=unit(sub(b,a));u=unit(cross(d,(0,0,1)));w=cross(d,u);uu=sub(u,mul(d,u[2]/d[2]));ww=sub(w,mul(d,w[2]/d[2]));seg=32
  profile=[(.30,0),(.30,HEIGHT),(.22,HEIGHT),(.22,0)];v=[];f=[];fm=[]
  for r,z in profile:
   c=add(a,mul(sub(b,a),z/HEIGHT))
   v += [add(c,add(mul(uu,r*math.cos(math.tau*i/seg)),mul(ww,r*math.sin(math.tau*i/seg))))for i in range(seg)]
  for k in range(4):
   for i in range(seg):
    j=(i+1)%seg;aa=k*seg+i;bb=k*seg+j;cc=((k+1)%4)*seg+j;dd=((k+1)%4)*seg+i;f.extend([(aa,bb,cc),(aa,cc,dd)]);fm += [0 if k==0 else 1]*2
  record(name,v,f,0);FM[name]=fm
  p=add(b,mul(uu,.26));CONTACTS.append((name,'WholeBevelledCapWithThroughHatch',p,.13))
  GAPS.append(dict(label=name+'_full_oblique_lumen_until_cap',origin_m=add(a,mul(d,.015)),direction=d,length_m=math.sqrt(dot(sub(b,a),sub(b,a)))-.030))
  GAPS.append(dict(label=name+'_cap_closes_pipe_mouth_control',origin_m=add(a,mul(d,.015)),direction=d,length_m=math.sqrt(dot(sub(b,a),sub(b,a)))+.1,blocked=True))
def clipped(rx,ry,c,z):return[(x,y,z)for x,y in[(-rx+c,-ry),(rx-c,-ry),(rx,-ry+c),(rx,ry-c),(rx-c,ry),(-rx+c,ry),(-rx,ry-c),(-rx,-ry+c)]]
loops=[clipped(1.80,1.80,.22,3.4),clipped(1.90,1.90,.24,3.50),clipped(1.90,1.90,.24,3.78),clipped(1.82,1.82,.22,3.86),clipped(.55,.45,.06,3.86),clipped(.55,.45,.06,3.4)];v=[p for ring in loops for p in ring];f=[]
for k in range(len(loops)):
 for i in range(8):
  j=(i+1)%8;a=k*8+i;b=k*8+j;c=((k+1)%len(loops))*8+j;d=((k+1)%len(loops))*8+i;f.extend([(a,b,c),(a,c,d)])
record('WholeBevelledCapWithThroughHatch',v,f,2);FM['WholeBevelledCapWithThroughHatch']=[2]*len(f)
for x,y in[(0,0),(.4,0),(-.4,0),(0,.3),(0,-.3)]:GAPS.append(dict(label='FullVerticalInspectionHatch',origin_m=[x,y,.01],direction=[0,0,1],length_m=4.1))
for z in[.2,1.5,3.2]:GAPS.append(dict(label='FullUnderCapCrosswayGap',origin_m=[-2.2,0,z],direction=[1,0,0],length_m=4.4))
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
focus=Vector((0,0,1.93))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=6.8;aim(cam,(9,-13,9) if view=='qa-front' else (-10,-14,8.5));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/harbor/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'prop','theme':'harbor','style':'S01-clean-geometric','title':'Fixed Battered Hollow Piles and Through Hatch Cap','description':'One wholly newly authored complete fixed dry pile-cap foundation display inspired only by broad marine dolphin foundation vocabulary. Four entire thick-walled round tubular piles incline inward in two plan directions from four widely separated flat annular soles to four distinct full annular seats beneath one whole thick cap. Each pile is a true constant-radius tube about its inclined axis; both finished end planes are horizontal ellipses rather than uncropped oblique tube ends making edge-only support. Every pile retains its complete outer wall, continuous inner bore and both finite end rings as one closed material mesh. The complete upper cap has a broad bevelled eight-sided outer perimeter and one genuine central through-hatch; the central empty vertical shaft and full crosswise under-cap gaps remain open. The cap rests on four actual opposed finite annular patches; its solid material intentionally closes the top of each pile bore, while the four inspection-display lower bores remain open. Unlike the old two-metre timber pier tile, there is no plank deck, under-deck stringer, short vertical timber piling, collar or snapped shore module. All four hollow inclined tubes and the continuous ported cap were newly authored together as one whole structural appearance, not clipped from a dock, stool, roof, hull, old pile or old model. Five closed separately editable material meshes and three untextured opaque PBR roles, metre-style Z-up and four actual bottom annular contact patches. One model zero scenes. Deliberately bare dry foundation appearance: no bollard, fender, catwalk, railing, vessel, water, soil volume, reinforcement or operating berth. The exposed bottom cuts are an inspection datum, not piles supported safely on a seabed or claims of embedment. No dimensions or specification of any real project copied. No anchorage, soil resistance, pile driving, concrete/steel behaviour, buoyancy, impact, mooring, load rating, marine suitability, installation, human access or structural safety capability claimed or tested. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
