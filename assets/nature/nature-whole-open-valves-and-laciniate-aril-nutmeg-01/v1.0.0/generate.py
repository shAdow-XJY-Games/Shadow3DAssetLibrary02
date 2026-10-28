"""One newly authored whole opened two-valve nutmeg fruit with a full single seed and connected laciniate aril."""
import math,collections,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
G={}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.fm=[];self.index={}
 def vertex(self,p):
  p=tuple(round(float(x),9)for x in p)
  if p not in self.index:self.index[p]=len(self.v);self.v.append(p)
  return self.index[p]
 def tri(self,p,mat):self.f.append(tuple(self.vertex(v)for v in p));self.fm.append(mat)
 def quad(self,a,b,c,d,mat):self.tri([a,b,c],mat);self.tri([a,c,d],mat)
 def result(self,role):
  edges={}
  for i,f in enumerate(self.f):
   for a,b in zip(f,f[1:]+f[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((i,a,b))
  assert all(len(v)==2 for v in edges.values()),[(e,v)for e,v in edges.items()if len(v)!=2][:5]
  signs={0:1};todo=[0]
  while todo:
   i=todo.pop()
   for a,b in zip(self.f[i],self.f[i][1:]+self.f[i][:1]):
    for j,c,d in edges[tuple(sorted((a,b)))]:
     if i==j:continue
     want=signs[i]*(-1 if(a,b)==(c,d)else 1)
     if j in signs:assert signs[j]==want
     else:signs[j]=want;todo.append(j)
  assert len(signs)==len(self.f)
  ff=[f if signs[i]>0 else tuple(reversed(f))for i,f in enumerate(self.f)];vol=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]]))for f in ff)/6
  if vol<0:ff=[tuple(reversed(f))for f in ff]
  assert all(dot(cross(sub(self.v[f[1]],self.v[f[0]]),sub(self.v[f[2]],self.v[f[0]])),cross(sub(self.v[f[1]],self.v[f[0]]),sub(self.v[f[2]],self.v[f[0]])))>1e-18 for f in ff)
  return dict(vertices=self.v,faces=ff,face_materials=self.fm,material=0,role=role)

# Entirely new complete opened fruit: both pericarp valves retained, no cut-away quadrant.
G={};JOINTS=[];AIR=[];GROUND=[]
def opening(z):return .028*(max(0,z-.010)/.066)**1.10
VALVES=[];N=36;L=30
for sign,label in[(-1,'Left'),(1,'Right')]:
 name='WholeSplayedPericarpValve_'+label;VALVES.append(name);m=Mesh();surfaces=[]
 for inner in[False,True]:
  rows=[]
  for i in range(L+1):
   t=-math.pi/2+math.pi*i/L;c=max(0,math.cos(t));z=.038+(.032 if inner else .038)*math.sin(t);row=[]
   for j in range(N+1):
    a=-math.pi/2+math.pi*j/N;rx=.025 if inner else .032;ry=.021 if inner else .027;shape=1+.025*math.cos(3*a+.4)*c*c
    row.append((sign*(rx*c*math.cos(a)*shape+opening(z)),ry*c*math.sin(a)*shape,z))
   rows.append(row)
  surfaces.append(rows)
  for i,(aa,bb)in enumerate(zip(rows,rows[1:])):
   for j in range(N):
    if i==0:m.tri([aa[0],bb[j],bb[j+1]],1 if inner else 0)
    elif i==L-1:m.tri([aa[j],aa[j+1],bb[0]],1 if inner else 0)
    else:m.quad(aa[j],aa[j+1],bb[j+1],bb[j],1 if inner else 0)
 outer,inside=surfaces
 for j in[0,N]:
  for i in range(L):m.quad(outer[i][j],outer[i+1][j],inside[i+1][j],inside[i][j],1)
 G[name]=m.result('One entire naturally divided fleshy pericarp valve, with full outer and inner surfaces, rounded polar ends and finite longitudinal dehiscence margins. Both valves remain joined in the common basal tissue; the open position is an artistic regularization, not a hinge or force simulation. No front peel is discarded and no old nut shell is reused.')
def ellipsoid(name,c,rx,ry,rz,mat,role,n=48,l=24):
 m=Mesh();rows=[]
 for i in range(l+1):
  t=-math.pi/2+math.pi*i/l;cc=max(0,math.cos(t));rows.append([(c[0]+rx*cc*math.cos(math.tau*j/n),c[1]+ry*cc*math.sin(math.tau*j/n),c[2]+rz*math.sin(t))for j in range(n)])
 for i,(aa,bb)in enumerate(zip(rows,rows[1:])):
  for j in range(n):
   jj=(j+1)%n
   if i==0:m.tri([aa[0],bb[j],bb[jj]],mat)
   elif i==l-1:m.tri([aa[j],aa[jj],bb[0]],mat)
   else:m.quad(aa[j],aa[jj],bb[jj],bb[j],mat)
 G[name]=m.result(role)
BASE='WholeCommonBasalFruitTissue';ellipsoid(BASE,(0,0,.009),.006,.006,.008,1,'One complete small solid basal tissue connection retained between both whole valves and the single seed. Broad schematic fruit attachment, not a hinge, artificial stand, full vascular anatomy or attached tree stem.')
for sign,name in zip([-1,1],VALVES):JOINTS.append((name,BASE,(sign*.002,0,.004)))
SEED='WholeOvoidHardSeed';SC=(0,-.001,.036);RX=.014;RY=.0125;RZ=.020
def seedpoint(a,t,scale=1.):
 c=max(0,math.cos(t));q=1+.018*math.sin(5*a+2*t)*c*c+.010*math.sin(11*a-1.2*t)*c*c
 return(SC[0]+RX*scale*c*math.cos(a)*q,SC[1]+RY*scale*c*math.sin(a)*q,SC[2]+RZ*scale*math.sin(t))
m=Mesh();N=64;L=32;rows=[[seedpoint(math.tau*j/N,-math.pi/2+math.pi*i/L)for j in range(N)]for i in range(L+1)]
for i,(aa,bb)in enumerate(zip(rows,rows[1:])):
 for j in range(N):
  jj=(j+1)%N
  if i==0:m.tri([aa[0],bb[j],bb[jj]],2)
  elif i==L-1:m.tri([aa[j],aa[jj],bb[0]],2)
  else:m.quad(aa[j],aa[jj],bb[jj],bb[j],2)
G[SEED]=m.result('One entire ovoid hard dark seed coat form with shallow integral irregular longitudinal relief. No exposed cotyledons, kernel halves, embryo or internal endosperm is modelled. The whole seed remains seated at the common fruit base and inside its red aril.');JOINTS.append((BASE,SEED,(0,-.001,.0165)))
# One connected laciniate aril, not eight independent red ribbons or a texture.
# A sparse angular/latitudinal field defines real open windows. Every retained
# patch has outer/inner surfaces; every missing-cell boundary gets finite walls.
ARIL='WholeConnectedLaciniateAril';NA=180;NT=60
angles=[math.tau*j/NA for j in range(NA)];lat=[-math.pi/2+math.pi*i/NT for i in range(NT+1)]
def occupied(i,j):
 t=(lat[i]+lat[i+1])/2;a=math.tau*(j+.5)/NA
 if t<-1.10:return True
 if t>1.20:return False
 warped=a+.055*math.sin(3*t+2*a)+.025*math.sin(7*a)
 stripes=abs(math.sin(4*warped))<(.29+.07*math.cos(3*a+t))
 top=1.06+.12*math.sin(3*a+.5)
 # Limited irregular branch bridges join neighbouring long lobes at different heights.
 bridge1=abs(t-(-.27+.15*math.sin(2*a+.5)))<.095 and math.sin(a+.25)<.82
 bridge2=abs(t-(.36+.13*math.cos(3*a-.25)))<.085 and math.sin(a-.2)<.35
 return (stripes and t<top)or bridge1 or bridge2
cells={(i,j)for i in range(NT)for j in range(NA)if occupied(i,j)}
# Fill only diagonal-contact grid ambiguities before constructing a single
# orientable skin, avoiding nonmanifold vertex pinch points in a sparse mask.
changed=True
while changed:
 changed=False
 for i in range(NT-1):
  for j in range(NA):
   jj=(j+1)%NA;a=(i,j);b=(i,jj);c=(i+1,j);d=(i+1,jj);bits=[q in cells for q in[a,b,c,d]]
   if bits in[[True,False,False,True],[False,True,True,False]]:cells.add(b if bits[0]else a);changed=True
# R2 smooth only the boundary in its angular/latitudinal parameter domain.
# The complete closed skin remains on the same seed surface, with finite wall thickness.
boundary={}
for i,j in cells:
 for neighbor,(a,b)in[((i,j-1),((i,j),(i+1,j))),((i,j+1),((i,j+1),(i+1,j+1))),((i-1,j),((i,j),(i,j+1))),((i+1,j),((i+1,j),(i+1,j+1)))]:
  if(neighbor[0],neighbor[1]%NA)in cells or(a[0]==b[0]and a[0]in[0,NT]):continue
  a=(a[0],a[1]%NA);b=(b[0],b[1]%NA);boundary.setdefault(a,set()).add(b);boundary.setdefault(b,set()).add(a)
assert all(len(v)==2 for v in boundary.values())
uv={p:(math.tau*p[1]/NA,lat[p[0]])for p in boundary}
for iteration in range(3):
 nextuv={}
 for p,ns in boundary.items():
  a,t=uv[p];others=[uv[q]for q in ns];da=sum((x-a+math.pi)%math.tau-math.pi for x,y in others)/len(others);dt=sum(y-t for x,y in others)/len(others);nextuv[p]=(a+.45*da,t+.45*dt)
 uv=nextuv
def ap(i,j,outer):
 a,t=uv.get((i,j%NA),(math.tau*(j%NA)/NA,lat[i]));return seedpoint(a,t,1.047 if outer else .987)
m=Mesh()
for i,j in sorted(cells):
 for outer in[False,True]:
  pp=[ap(i,j,outer),ap(i,j+1,outer),ap(i+1,j+1,outer),ap(i+1,j,outer)]
  if i==0:m.tri([pp[0],pp[2],pp[3]],3)
  elif i==NT-1:m.tri(pp[:3],3)
  else:m.quad(*pp,3)
 edges=[((i,j-1),((i,j),(i+1,j))),((i,j+1),((i,j+1),(i+1,j+1))),((i-1,j),((i,j),(i,j+1))),((i+1,j),((i+1,j),(i+1,j+1)))]
 for neighbor,(a,b)in edges:
  if(neighbor[0],neighbor[1]%NA)in cells:continue
  if a[0]==b[0]and a[0]in[0,NT]:continue
  m.quad(ap(*a,False),ap(*b,False),ap(*b,True),ap(*a,True),3)
G[ARIL]=m.result('One whole connected red laciniate aril skin with a shared basal cap, irregular long lobes and sparse branching bridges. All exposed windows are real absent areas with finite edge walls, not painted lace or opacity. The inner skin intentionally overlaps the intact seed coat by a small finite amount for continuous seating. Pattern and lobe count are artistic, not a measured specimen or universal taxonomic rule.')
JOINTS.append((SEED,ARIL,seedpoint(-math.pi/2,-1.28,.994)))
# Finite radial window probes stop just outside the seed and below the aril outer
# surface; they demonstrate several actual lace openings rather than all visibility.
# Choose only well-inside absent patches, not boundary-edge numerical coincidences.
missing=[(i,j)for i in range(14,NT-12)for j in range(NA)if all((i+di,(j+dj)%NA)not in cells for di,dj in[(0,0),(-1,0),(1,0),(0,-1),(0,1)])]
selected=[]
for targett,targeta in[(-.55,-1.9),(.02,-1.5),(.65,-1.05)]:
 i,j=min(missing,key=lambda q:(lat[q[0]]-targett)**2+(((math.tau*(q[1]+.5)/NA-targeta+math.pi)%math.tau)-math.pi)**2)
 if(i,j)in selected:continue
 selected.append((i,j));a=math.tau*(j+.5)/NA;t=(lat[i]+lat[i+1])/2;p=seedpoint(a,t,1.060);end=seedpoint(a,t,1.015);d=sub(end,p);ll=math.sqrt(dot(d,d));AIR.append(dict(point=p,direction=mul(d,1/ll),length_m=ll,scope='Short radial opening across an absent aril patch, terminating outside the intact seed coat'))
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[k]for p in vv)+max(p[k]for p in vv))/2 if k<2 else-min(p[2]for p in vv)for k in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
JOINTS=[(a,b,add(p,SHIFT))for a,b,p in JOINTS]
for r in AIR:r['point']=add(r['point'],SHIFT)
EXPECTED_TRIANGLES=sum(len(g['faces'])for g in G.values());EXPECTED_MESHES=len(G)
ASSET='nature-whole-open-valves-and-laciniate-aril-nutmeg-01';VERSION='1.0.0';TITLE='Whole Open Valves and Laciniate Aril Nutmeg'
DESCRIPTION='One wholly newly authored complete opened nutmeg fruit schematic, approximately eight centimetres tall. Both entire fleshy pericarp valves retain complete outer surfaces, inner walls, polar ends and finite natural dehiscence margins, splaying around their shared basal tissue rather than removing a front quadrant. One complete dark ovoid seed remains seated inside a single connected red laciniate aril with a basal cap, irregular elongated lobes, branching bridges and real open lace windows. The source has independent fruit wall cross-sections, a whole seed surface and a newly drawn connected aril mask. No old walnut posterior shell, cotyledon, partition, pomegranate rind, calyx or aril bead cluster is copied, recoloured, reduced or relabelled. One whole fruit prop, zero scenes and no separately counted valves or seeds. Open position, aril pattern and scale are regularized artistic choices, not a measured cultivar or a universal biological arrangement. The seed kernel, ruminate endosperm, embryo, microscopic tissue layers, tree stem and leaves are omitted; no false hinge, fruit-opening mechanism or natural standing stability is claimed. Quiet opaque PBR materials; no reference image textures, rig, animation, interaction, nutritional, food-safety, medicinal or diagnostic claims.'
PALETTE=[('FleshyPericarp_GoldenOchre',(.61,.43,.17,1),.85,0.),('InnerPericarp_WarmIvory',(.78,.67,.43,1),.90,0.),('WholeSeed_DeepBrown',(.105,.045,.024,1),.44,0.),('LaciniateAril_MutedScarlet',(.57,.045,.025,1),.68,0.)]
FOCUS=(0,0,.037);CAMERAS={'thumbnail':(.42,-1.6,1.05),'qa-front':(.42,-1.6,1.05),'qa-side':(1.5,.4,.65),'qa-top':(0,0,2),'qa-back':(-.42,1.6,1.05),'qa-wireframe':(.42,-1.6,1.05)}
ORTHO=.135;WIRE_THICKNESS=.000045

# BLENDER PHASE: mature export/render only.
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.seed=17
scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
EXPECTED={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False],'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4}
def config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def guard():c=config();assert c==EXPECTED,c;return c
mats=[]
for name,color,rough,metal in PALETTE:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;p.inputs['Alpha'].default_value=1.;p.inputs['Transmission Weight'].default_value=0.;p.inputs['Emission Strength'].default_value=0.;mats.append(m)
bpy.context.preferences.filepaths.save_version=0
root=bpy.data.objects.new('OneWholeOpenedNutmegFruit',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='lowest whole fruit pole as art origin; both opened valves retained, no physical standing claim';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();
 for m in mats:me.materials.append(m)
 for i,f in enumerate(me.polygons):f.material_index=g.get('face_materials',[g['material']]*len(me.polygons))[i]
 o['component_role']=g['role'];parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={};actual_triangles={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg);triangles+=len(o.data.loop_triangles)
 component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i]for p in v)for i in range(3)];hi=[max(p[i]for p in v)for i in range(3)];bounds=[round(hi[i]-lo[i],6)for i in range(3)]
assert abs(lo[2])<1e-7 and triangles==EXPECTED_TRIANGLES and len(parts)==EXPECTED_MESHES
def pbr(m):
 p=m.node_tree.nodes.get('Principled BSDF');assert p is not None
 assert not any(n.type.startswith('TEX_') for n in m.node_tree.nodes),'No procedural or image texture nodes permitted'
 assert not any(socket.is_linked for socket in p.inputs),'No linked Principled inputs permitted'
 values=[]
 for name in ['Base Color','Metallic','Roughness','Alpha','IOR','Specular IOR Level','Transmission Weight','Coat Weight','Coat Roughness','Sheen Weight','Emission Color','Emission Strength']:
  value=p.inputs[name].default_value
  values.append((name,tuple(round(float(x),6) for x in value) if hasattr(value,'__len__') else round(float(value),6)))
 values.append(('double_sided',not m.use_backface_culling));return tuple(values)
def records(objects):
 rows=[]
 for o in objects:
  o.data.calc_loop_triangles();vs=[o.matrix_world@v.co for v in o.data.vertices]
  for t in o.data.loop_triangles:
   q=[tuple(round(float(c),6) for c in vs[i]) for i in t.vertices]
   rows.append((min(tuple(q[i:]+q[:i]) for i in range(3)),pbr(o.data.materials[t.material_index])))
 return sorted(rows)
source_records=records(parts);source_fp=hashlib.sha256(json.dumps(source_records,separators=(',',':')).encode()).hexdigest()
mesh_count=len(parts);bpy.ops.object.select_all(action='DESELECT')
for o in parts+[root]:o.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
# Count the material list in the actual exported GLB, not a copied literal.
import struct
_glb=(OUT/'model.glb').read_bytes();_json_length,_json_kind=struct.unpack_from('<II',_glb,12);assert _json_kind==0x4e4f534a
actual_material_count=len(json.loads(_glb[20:20+_json_length])['materials'])
assert actual_material_count==len({f.material_index for o in parts for f in o.data.polygons})
guard();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':actual_material_count,'mesh_objects':mesh_count,'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,'components':component_checks,'single_prop_count':1,'review_mode':'SELF_REVIEW','static_visual_only':True,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),'status':'producer geometry; maker actual-image acceptance pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/nature/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'nature','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
 'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':actual_material_count,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
# Every formal/early render is of the actual exported file imported into an emptied scene.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));parts=[o for o in scene.objects if o.type=='MESH']
assert len(parts)==mesh_count and records(parts)==source_records,'Fresh GLB oriented geometry / full solid PBR mismatch'
qa['fresh_actual_glb_guard']={'oriented_geometry_and_full_solid_pbr_match':True,'mesh_count':len(parts)};saveqa()
if '--no-render' in sys.argv or '--geometry-only' in sys.argv:
 metadata();print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)

# BEGIN AUTHORIZED TIERED RENDER V1; native has already been saved at128.
def tier_arg(flag,default=None):
 if flag not in sys.argv:return default
 i=sys.argv.index(flag);assert i+1<len(sys.argv);return sys.argv[i+1]
TIER_PROFILE=tier_arg('--render-profile')
TIER_ALLOWED={'simple-v1':(16,[16,32,64]),'complex-v1':(32,[32,64])}
TIER_SINGLE=tier_arg('--tier-single-view')
TIER_LIST=json.loads(tier_arg('--tier-view-list','[]'))
TIER_OVERRIDES=json.loads(tier_arg('--tier-sample-overrides','{}'))
TIER_STANDARD=['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe']
if TIER_PROFILE:
 assert TIER_PROFILE in TIER_ALLOWED and '--gray-only' not in sys.argv and '--gray-obliques-only' not in sys.argv
 assert isinstance(TIER_OVERRIDES,dict)
 for k,v in TIER_OVERRIDES.items():assert k in CAMERAS and k!='thumbnail' and type(v) is int and v in TIER_ALLOWED[TIER_PROFILE][1]
 assert isinstance(TIER_LIST,list) and len(TIER_LIST)==len(set(TIER_LIST)) and not(TIER_LIST and TIER_SINGLE)
 assert all(n in TIER_STANDARD[1:] and n in CAMERAS for n in TIER_LIST)
 if TIER_SINGLE:assert TIER_SINGLE in CAMERAS and TIER_SINGLE not in ['gray-front3q','gray-back3q','silhouette-128-front','silhouette-128-side']
 qa['tiered_render']={'profile_id':TIER_PROFILE,'authorization_reference':'Sentinel_f2fcc66115e881918d02bc1ea780953c','native_samples':128,'resolution':[640,640],'gray_stage':'omitted_by_authorized_profile','samples_by_image':{}}
def tier_select_views(views):
 if not TIER_PROFILE:return views
 if TIER_SINGLE:return {TIER_SINGLE:CAMERAS[TIER_SINGLE]}
 if TIER_LIST:return {n:CAMERAS[n] for n in TIER_LIST}
 assert set(views)<=set(TIER_STANDARD)
 return views
def tier_before_view(name):
 if not TIER_PROFILE:return
 samples=128 if name=='thumbnail' else TIER_OVERRIDES.get(name,TIER_ALLOWED[TIER_PROFILE][0])
 assert samples==128 if name=='thumbnail' else samples in TIER_ALLOWED[TIER_PROFILE][1]
 scene.cycles.samples=samples
 EXPECTED['samples']=samples
 qa['tiered_render']['samples_by_image'][name+'.png']=samples
# END AUTHORIZED TIERED RENDER V1
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.30,.30,.30,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8;scene.view_settings.view_transform='AgX'
focus=Vector(FOCUS);asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),600,4),('Fill',(4,-2,4),360,3.5),('Rim',(2,4,5),480,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
def diagnostic_snapshot():
 return {m:[(i,socket.identifier,socket.bl_idname,tuple(socket.default_value) if hasattr(socket.default_value,'__len__') else socket.default_value) for i,socket in enumerate(m.node_tree.nodes.get('Principled BSDF').inputs) if hasattr(socket,'default_value')] for m in asset_mats}
original_material_inputs=diagnostic_snapshot()
original_slots={o:(list(o.data.materials),[f.material_index for f in o.data.polygons]) for o in parts}
def restore_diagnostic_materials():
 for m,inputs in original_material_inputs.items():
  p=m.node_tree.nodes.get('Principled BSDF')
  for index,identifier,socket_type,value in inputs:
   assert index<len(p.inputs),'Diagnostic socket index disappeared'
   socket=p.inputs[index]
   assert socket.identifier==identifier and socket.bl_idname==socket_type,'Diagnostic socket identity/type changed'
   socket.default_value=value
 for o,(slots,indices) in original_slots.items():
  assert len(o.data.polygons)==len(indices),'Diagnostic face count changed'
  o.data.materials.clear()
  for m in slots:o.data.materials.append(m)
  for f,index in zip(o.data.polygons,indices):f.material_index=index
  assert list(o.data.materials)==slots and [f.material_index for f in o.data.polygons]==indices
 assert diagnostic_snapshot()==original_material_inputs,'Diagnostic full socket-index/identifier/type/value restoration differs'
 assert records(parts)==source_records,'Diagnostic restoration changed complete oriented geometry/full solid PBR signature'
 qa['diagnostic_exact_restoration']={'try_finally':True,'full_socket_index_identifier_type_value_match':True,'all_material_slots_and_face_indices_match':True,'full_oriented_geometry_and_pbr_records_match':True}
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
try:
 if gray:
  for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
 views={k:CAMERAS[k] for k in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
 if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
 if '--extra-views' in sys.argv:views.pop('thumbnail',None)
 views=tier_select_views(views)
 seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
 def render(name,pos):
  tier_before_view(name)
  ground.hide_render=(name=='qa-side')
  cam.data.ortho_scale=ORTHO
  aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
 for name,pos in views.items():
  if name=='qa-wireframe':
   wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
   for o in parts:
    dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
    for f in dup.data.polygons:f.material_index=0
    w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=WIRE_THICKNESS;w.use_replace=True;w.use_even_offset=False;w.offset=1
  render(name,pos)
 if gray and '--gray-obliques-only' not in sys.argv:
  black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
  for o in parts:
   o.data.materials.clear();o.data.materials.append(black)
   for f in o.data.polygons:f.material_index=0
  ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
  scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
  for name,pos in [(name,CAMERAS[name]) for name in ['silhouette-128-front','silhouette-128-side']]:render(name,pos)
finally:
 restore_diagnostic_materials()
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; maker necessary-view self-review pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
