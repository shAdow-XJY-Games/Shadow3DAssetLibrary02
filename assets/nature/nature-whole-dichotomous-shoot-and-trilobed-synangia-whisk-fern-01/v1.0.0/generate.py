"""One newly authored whole dichotomous whisk-fern aerial shoot with complete trilobed synangia. Static exterior plant art."""
import math,collections,json,hashlib,sys,time,itertools
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

# Entire new branching shoot graph; generic convex open-port joining only.
# No old coral coordinates, three-main/six-tip graph or horsetail whorls reused.
G={};JOINTS=[];AIR=[];CORE='WholeContinuousDichotomousAerialShoot';GROUND=[CORE];N=12
def norm(a):return math.sqrt(dot(a,a))
def unit(a):return mul(a,1/norm(a))
def ring(c,axis,r):
 axis=unit(axis);ref=(0,1,0)if abs(axis[1])<.9 else(1,0,0);u=unit(cross(axis,ref));v=cross(axis,u)
 return[add(c,mul(add(mul(u,math.cos(math.tau*i/N)),mul(v,math.sin(math.tau*i/N))),r*(1+.045*math.cos(3*math.tau*i/N))))for i in range(N)]
def poly(m,pts,mat=0):
 for i in range(1,len(pts)-1):m.tri([pts[0],pts[i],pts[i+1]],mat)
def hub(m,ports):
 pts=[p for q in ports.values()for p in q];groups=[set(range(i*N,(i+1)*N))for i in range(len(ports))];found=set();port_found=set()
 for ia,ib,ic in itertools.combinations(range(len(pts)),3):
  a,b,c=pts[ia],pts[ib],pts[ic];nn=cross(sub(b,a),sub(c,a));ll=norm(nn)
  if ll<1e-11:continue
  nn=mul(nn,1/ll);dd=[dot(sub(p,a),nn)for p in pts]
  if max(dd)>1e-8 and min(dd)<-1e-8:continue
  ids=frozenset(i for i,x in enumerate(dd)if abs(x)<1e-8)
  if len(ids)<3 or ids in found:continue
  found.add(ids)
  if any(ids==g for g in groups):port_found.add(ids);continue
  if max(dd)>1e-8:nn=mul(nn,-1)
  c=mul(tuple(sum(pts[i][k]for i in ids)for k in range(3)),1/len(ids));u=unit(sub(pts[min(ids)],c));v=cross(nn,u);order=sorted(ids,key=lambda i:math.atan2(dot(sub(pts[i],c),v),dot(sub(pts[i],c),u)));poly(m,[pts[i]for i in order])
 assert len(port_found)==len(ports),('Not all true open ports exposed',len(port_found),len(ports))
def connect(m,a,b,mat=0):
 candidates=[q[k:]+q[:k]for q in[b,list(reversed(b))]for k in range(N)];b=min(candidates,key=lambda q:sum(dot(sub(x,y),sub(x,y))for x,y in zip(a,q)))
 for i in range(N):j=(i+1)%N;m.quad(a[i],a[j],b[j],b[i],mat)
 return b
C=[(0,0,.155),(-.058,.004,.282),(.061,-.005,.276),(-.102,-.012,.389),(-.024,.020,.402),(.027,-.023,.386),(.109,.015,.390)]
PARENT={1:0,2:0,3:1,4:1,5:2,6:2};CHILDREN={0:[1,2],1:[3,4],2:[5,6]};TIPS={3:[(-.135,-.018,.484),(-.080,.006,.501)],4:[(-.045,.031,.513),(.000,.043,.493)],5:[(.007,-.047,.486),(.046,-.017,.503)],6:[(.090,.006,.491),(.143,.032,.478)]}
ports={};centres={};radii={};m=Mesh();SEGMENTS=[]
for i,c in enumerate(C):
 level=0 if i==0 else 1 if i<3 else 2;rad=[.0045,.0035,.00265][level];offset=[.018,.016,.013][level];p={};cc={};rr={};back=(0,0,0)if i==0 else C[PARENT[i]];axis=unit(sub(back,c));cc['In']=add(c,mul(axis,offset));rr['In']=rad;p['In']=ring(cc['In'],axis,rad)
 ends=[C[k]for k in CHILDREN[i]]if i in CHILDREN else TIPS[i]
 for j,end in enumerate(ends):
  k='Out'+str(j);axis=unit(sub(end,c));cc[k]=add(c,mul(axis,offset));rr[k]=rad*.88;p[k]=ring(cc[k],axis,rr[k])
 hub(m,p);ports[i]=p;centres[i]=cc;radii[i]=rr
base=ring((0,0,0),(0,0,-1),.0065);mid=ring((-.002,0,.07),(0,0,1),.0049);poly(m,base);q=connect(m,base,mid);connect(m,q,ports[0]['In'])
for child,parent in PARENT.items():
 j=CHILDREN[parent].index(child);k='Out'+str(j);connect(m,ports[parent][k],ports[child]['In']);SEGMENTS.append(dict(a=centres[parent][k],b=centres[child]['In'],r0=radii[parent][k],r1=radii[child]['In']))
for i,ends in TIPS.items():
 for j,end in enumerate(ends):
  k='Out'+str(j);a=centres[i][k];axis=unit(sub(end,a));mid=add(a,mul(sub(end,a),.66));r=radii[i][k];first=ring(mid,axis,r*.66);last=ring(end,axis,.00065);q=connect(m,ports[i][k],first);q=connect(m,q,last,1);poly(m,q,1);SEGMENTS.append(dict(a=a,b=mid,r0=r,r1=r*.66))
G[CORE]=m.result('One entire shared-vertex closed aerial axis with seven true open-port dichotomous forks, eight tapered terminal twigs, gently angular ridged sections and a finite basal stem datum. No capped overlapping limb cylinders, radial whorls, borrowed coral graph or old fern frond.')
# Ten complete trilobed synangia, each a single fused boundary, with bifid scales.
SYNANGIA=[];SCALES=[]
def earclip(p):
 cr=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]);ids=list(range(len(p)));out=[]
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:ids.reverse()
 while len(ids)>3:
  for j,b in enumerate(ids):
   a,c=ids[j-1],ids[(j+1)%len(ids)]
   if cr(p[a],p[b],p[c])<=1e-13:continue
   if any(min(cr(p[a],p[b],p[k]),cr(p[b],p[c],p[k]),cr(p[c],p[a],p[k]))>=-1e-13 for k in ids if k not in[a,b,c]):continue
   out.append((a,b,c));ids.pop(j);break
  else:raise AssertionError('Scale outline not simple')
 out.append(tuple(ids));return out
for i,idx in enumerate([0,1,2,3,4,5,6,8,10,12]):
 seg=SEGMENTS[idx];t=.62 if i<6 else .43;axis=unit(sub(seg['b'],seg['a']));p=add(seg['a'],mul(sub(seg['b'],seg['a']),t));r=seg['r0']*(1-t)+seg['r1']*t;front=(0,-1,0);out=unit(sub(front,mul(axis,dot(front,axis))));side=unit(cross(axis,out));c=add(p,mul(out,r+.0035));m=Mesh();K=14;J=36;rows=[]
 for k in range(K+1):
  tt=math.pi*k/K;row=[]
  for j in range(J):
   a=math.tau*j/J;rr=.0066*(1+.32*math.cos(3*a))*math.sin(tt);row.append(add(c,add(mul(out,.0048*math.cos(tt)),add(mul(side,rr*math.cos(a)),mul(axis,rr*math.sin(a))))))
  rows.append(row)
 for k,(aa,bb)in enumerate(zip(rows,rows[1:])):
  for j in range(J):
   jj=(j+1)%J
   if k==0:m.tri([aa[0],bb[j],bb[jj]],2)
   elif k==K-1:m.tri([aa[j],aa[jj],bb[0]],2)
   else:m.quad(aa[j],aa[jj],bb[jj],bb[j],2)
 name='WholeFusedTrilobedSynangium_%02d'%(i+1);G[name]=m.result('One whole closed three-lobed synangium formed as a single continuous solid boundary, sessile on the branch. Three-lobed shape is real geometry, not three loose beads or painted cell borders; no internal chambers, microscopic spores or opening process claimed.');SYNANGIA.append(name);JOINTS.append((CORE,name,add(p,mul(out,r*.80))))
 # Newly authored short bifid fertile scale, below the full synangium.
 root=add(p,mul(axis,-.0080));outline=[(0,-.0013),(.0061,-.0030),(.0102,-.0018),(.0074,0),(.0102,.0018),(.0061,.0030),(0,.0013)];m=Mesh()
 def point(q,h):return add(root,add(mul(out,q[0]+r*.35),add(mul(axis,q[1]),mul(side,h))))
 for h in[-.00045,.00045]:
  for f in earclip(outline):m.tri([point(outline[k],h)for k in f],1)
 for a,b in zip(outline,outline[1:]+outline[:1]):m.quad(point(a,-.00045),point(b,-.00045),point(b,.00045),point(a,.00045),1)
 leaf='WholeBifidFertileScale_%02d'%(i+1);G[leaf]=m.result('One complete tiny thick bifid scale at a synangium-bearing branch site. A newly authored simple fertile enation, not a copied full leaf/frond or separate counted model.');SCALES.append(leaf);JOINTS.append((CORE,leaf,add(root,mul(out,r*.55))))
vv=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[k]for p in vv)+max(p[k]for p in vv))/2 if k<2 else-min(p[2]for p in vv)for k in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
JOINTS=[(a,b,add(p,SHIFT))for a,b,p in JOINTS]
EXPECTED_TRIANGLES=sum(len(g['faces'])for g in G.values());EXPECTED_MESHES=len(G)
ASSET='nature-whole-dichotomous-shoot-and-trilobed-synangia-whisk-fern-01';VERSION='1.0.0';TITLE='Whole Dichotomous Shoot and Trilobed Synangia Whisk Fern'
DESCRIPTION='One newly authored complete visible aerial whisk-fern-like shoot: a gently angular green axis repeatedly forks into a slender eight-tip branching system, with seven genuine shared-surface junctions rather than capped intersecting cylinders. Ten complete small three-lobed synangia and ten whole bifid fertile scales attach at branch sites. The fused three-lobed yellow capsule shapes, entire branching graph, coordinates, tapers and scale outlines are new; this is not a recoloured coral, a horsetail with whorls removed, or an old fern frond/count variation. One whole aerial-shoot model and zero scenes, not separately counted branches or reproductive bodies. The short finite basal stem datum stands for the continuation into the unmodelled subterranean rhizome, not a pot, pedestal, true root system or physical-standing claim. Three quiet opaque constant PBR roles and real geometric angular relief, no texture leaves or transparency. Generic Psilotum-like visible morphology with stylized enlarged reproductive details; not an exact specimen, complete subterranean plant, anatomical cross-section, measured natural scale, exact branch/capsule count, spores, mycorrhiza, germination, growth, toxicity, cultivation or treatment depiction. No animation, rig or interaction.'
PALETTE=[('AngularAerialStem_QuietGreen',(.16,.28,.075,1),.91,0.),('YoungTwigsAndBifidScales_LightGreen',(.29,.41,.12,1),.88,0.),('TrilobedSynangia_QuietYellowOchre',(.52,.39,.09,1),.89,0.)]
FOCUS=(0,0,.255);CAMERAS={'thumbnail':(.33,-1.8,.85),'qa-front':(.33,-1.8,.85),'qa-side':(-.6,1.7,.9),'qa-top':(0,0,2),'qa-back':(-.33,1.8,.85),'qa-wireframe':(.33,-1.8,.85)}
ORTHO=.66;WIRE_THICKNESS=.00013

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
root=bpy.data.objects.new('OneWholeDichotomousWhiskFernAerialShoot',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='finite basal aerial-stem continuation datum; subterranean rhizome not modelled, no physical standing claim';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
