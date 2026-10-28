import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='waterworks-whole-overcrest-hood-and-open-sided-siphon-cutaway-01'
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
PALETTE=[('WholeHoodAndRearWallMatteConcrete',(.47,.49,.45,1),.90,0),('WholeContinuousPassagePaleLining',(.67,.68,.59,1),.86,0),('WholeExposedLongitudinalSectionWarmStone',(.52,.35,.19,1),.88,0),('WholeIntegralOpenSummitVentMutedTeal',(.13,.32,.33,1),.75,.12)]
FM={};ROOTS=['WholeGroundedOvercrestHoodRearWallAndOpenSummitVent'];CONTACTS=[]
# A newly authored complete grounded longitudinal half-section of one over-crest hood.
# Each whole material boundary is derived directly from a conforming graded cell grid;
# no existing chute, pipe, crest, roof, vent or model is imported or trimmed.
def crest_height(x):
 if x<=-3.2:return .7
 if x<-.6:
  t=(x+3.2)/2.6;return .7+2.3*(3*t*t-2*t*t*t)
 if x<=.6:return 3.
 if x<3.3:
  t=(x-.6)/2.7;return 3.-2.6*(3*t*t-2*t*t*t)
 return .4
XS=sorted(set([-3.8,-3.2,-.6,-.3,-.18,.18,.3,.6,3.3,4.]+[-3.2+2.6*i/16 for i in range(1,16)]+[.6+2.7*i/18 for i in range(1,18)]))
YS=[0,.30,.45,.80,.95,1.35,1.55]
def level(x,k):return [0,crest_height(x),crest_height(x)+1,crest_height(x)+1.22,crest_height(x)+1.90][k]
faces={}
for i,(x0,x1)in enumerate(zip(XS,XS[1:])):
 for j,(y0,y1)in enumerate(zip(YS,YS[1:])):
  x=(x0+x1)/2;y=(y0+y1)/2;vent_outer=abs(x)<.30 and .30<y<.95;vent_inner=abs(x)<.18 and .45<y<.80
  for k in range(4):
   occupied=(k==0)or(k==1 and y>1.35)or(k==2 and not vent_inner)or(k==3 and vent_outer and not vent_inner)
   if not occupied:continue
   v=[(xx,yy,level(xx,zz))for zz in[k,k+1]for yy in[y0,y1]for xx in[x0,x1]];v=[tuple(round(c,12)for c in p)for p in v]
   for side,ix in enumerate([(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]):
    q=tuple(v[n]for n in ix);key=tuple(sorted(q))
    mat=0
    if (k==0 and side==1 and y<1.35)or(k==2 and side==0 and y<1.35)or(k==1 and side==2):mat=1
    if all(abs(p[1])<1e-10 for p in q)or all(abs(p[0]-XS[0])<1e-10 for p in q)or all(abs(p[0]-XS[-1])<1e-10 for p in q):mat=2
    if k==3 or(k==2 and vent_outer):mat=3
    if key in faces:del faces[key]
    else:faces[key]=(q,mat)
v=[];ix={};f=[];fm=[]
for q,mat in faces.values():
 ids=[]
 for p in q:
  if p not in ix:ix[p]=len(v);v.append(p)
  ids.append(ix[p])
 f.extend([(ids[0],ids[1],ids[2]),(ids[0],ids[2],ids[3])]);fm.extend([mat,mat])
record(ROOTS[0],v,f,0);FM[ROOTS[0]]=fm
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
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
focus=Vector((0,0,2.45))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,12),2000,6),('Fill',(7,-1,8),1500,5),('Rim',(1,7,11),2000,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=10.0;aim(cam,(10,-14,8) if view=='qa-front' else (-10,-15,9));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/waterworks/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'prop','theme':'waterworks','style':'S01-clean-geometric','title':'Whole Overcrest Hood and Open Sided Siphon Cutaway','description':'One wholly newly authored complete dry longitudinal half-section of an over-crest siphon-spillway-inspired architectural body. A single connected closed material solid includes the entire broad flat ground sole, shaped mass beneath the passage, complete far side wall, continuous thick overhead hood and one integral open summit breather. The real rectangular passage rises from a lower upstream mouth to a flat high summit and then descends to a lower downstream terminal; its complete floor, underside of roof and rear lining remain exposed along one deliberate full-length near-side section. Both entire end mouths are open through the passage, not capped by presentation faces. One genuinely hollow rectangular vent at the summit passes through the finite roof thickness into the main passage and has complete inner walls, outer walls and a finite top rim. No surrounding reservoir, whole dam, flowing water or terrain is supplied. Unlike the old rounded overflow crest and low basin, this body has a roofed rising-and-falling passage and a true open summit branch rather than an unroofed descending apron and basin. Unlike the old bellmouth shaft cutaway, there is no radial funnel or deep vertical shaft turning into a horizontal pipe: this new rectangular route climbs over a longitudinal summit before descending. Unlike the marine returning-pipe apparatus, there is no separate circular pipe, annular pedestal, side pivot, counterarm or weight. Every coordinate and graded closed boundary newly authored together, no old crest, pipe, shaft, vent or model imported, scaled or cut. The material body is one whole connected editable closed mesh with four opaque untextured constant PBR roles, metre-style Z up and the whole horizontal envelope centred over its complete flat ground sole; one model zero scenes. The absent near wall is intentional explanatory sectioning of the complete route, not damage and not a claim of a complete enclosed pressure conduit. Broad siphon-spillway vocabulary only; generic static civil-geometry art, not a named dam replica or engineering design. No hydraulic priming, air-control operation, flow, pressure, capacity, watertightness, water retention, cavitation, flood safety, structural stability, material properties, fabrication, installation or maintenance capability made or verified. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
