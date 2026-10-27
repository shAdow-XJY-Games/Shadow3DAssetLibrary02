'One static sports-equipment preparation bay, zero new models and one scene. Two complete accepted original models retain their entire geometry, metre scale and opaque PBR values: a tilted mesh rebounder stands at the left on its original four pads, while a whole lacrosse-inspired stick lies along the separate right-hand braced bench. Two small finite bench-top supports seat the original shaft without altering it. One new finite floor and complete subordinate braced bench leave an open front approach and a positive interval between the whole props. Embedded complete original source and whole-GLB hashes are checked before translation-only composition. No extracted fragments, scaled replacements, changed original materials or repeated model count. Empty illustrative static layout only, no training sequence, interaction, ball return, stick use, loading, fit, regulation, manufacture or safety claim.'
import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='sports-whole-rebounder-and-lacrosse-side-bench-preparation-bay-scene-01'
TITLE='Rebounder And Lacrosse Side Bench Preparation Bay'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
COMPONENTS=[{'label': 'CompleteRebounder', 'asset_id': 'sports-fixed-tilted-mesh-and-rear-u-stand-rebounder-01', 'source_sha256': 'a12febb3e32a47a3295616e3dc783407dec8080e3f9438bd3ede6038ac37f480', 'model_sha256': '3b297fa6cfa5c0f2e7e5b36c24f6467aec5ed80390f446c9eafbdd7a1181f180', 'source_compressed': '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', 'offset': [-0.65, 0.25, 0.06], 'verified_backup': 'libfile_583a9cd9172c8191999553a6031aa71c'}, {'label': 'CompleteLacrosse', 'asset_id': 'sports-fixed-tapered-pocket-and-open-throat-lacrosse-stick-01', 'source_sha256': '8e7c2fc92350bfc7da579de41190532c1b67b279f6d99b43b25ce8932b32c6c8', 'model_sha256': '686372260813ae9802ee5db092478050d63e4ead2b8470d1c714def2939f6579', 'source_compressed': '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', 'offset': [0.75, 0, 0.68], 'verified_backup': 'libfile_e8211c3809b8819189b4bf59f8db9da0'}]
PALETTE=[]
G={}
def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def rect(x,y0,y1,r):return[(-x+r,y0),(x-r,y0),(x,y0+r),(x,y1-r),(x-r,y1),(-x+r,y1),(-x,y1-r),(-x,y0+r)]
def prism(name,p,z0,z1,m,transform=None):
 v=[(x,y,z)for z in[z0,z1]for x,y in p];n=len(p);f=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)]
 if transform:v=[transform(q)for q in v]
 record(name,v,f,m)
def box(name,lo,hi,m,transform=None):prism(name,[(lo[0],lo[1]),(hi[0],lo[1]),(hi[0],hi[1]),(lo[0],hi[1])],lo[2],hi[2],m,transform)
def union_boxes(name,boxes,m):
 xs=sorted(set(p[0]for b in boxes for p in b));ys=sorted(set(p[1]for b in boxes for p in b));zs=sorted(set(p[2]for b in boxes for p in b));faces={}
 for i in range(len(xs)-1):
  for j in range(len(ys)-1):
   for k in range(len(zs)-1):
    c=((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)
    if not any(all(lo[t]<c[t]<hi[t]for t in range(3))for lo,hi in boxes):continue
    v=[(x,y,z)for z in[zs[k],zs[k+1]]for y in[ys[j],ys[j+1]]for x in[xs[i],xs[i+1]]]
    for f in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:
     q=tuple(v[t]for t in f);key=tuple(sorted(q))
     if key in faces:del faces[key]
     else:faces[key]=q
 verts=[];ix={};fs=[]
 for q in faces.values():
  f=[]
  for p in q:
   if p not in ix:ix[p]=len(verts);verts.append(p)
   f.append(ix[p])
  fs.append(f)
 record(name,verts,fs,m)
def cyl(name,center,r,length,axis,m,n=12):
 axes=[i for i in range(3)if i!=axis];v=[]
 for end in[-.5,.5]:
  for i in range(n):
   p=list(center);p[axis]+=end*length;p[axes[0]]+=r*math.cos(i*math.tau/n);p[axes[1]]+=r*math.sin(i*math.tau/n);v.append(tuple(p))
 record(name,v,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],m)
def sweep(name,path,r,m,n=12):
 # Constant out-of-plane axis prevents local frame flips along this planar neck.
 v=[]
 for j,p in enumerate(path):
  a=path[max(0,j-1)];b=path[min(len(path)-1,j+1)];dy=b[1]-a[1];dz=b[2]-a[2];q=math.hypot(dy,dz);u=(0,dz/q,-dy/q)
  for i in range(n):
   t=math.tau*i/n;v.append((p[0]+r*math.cos(t),p[1]+u[1]*r*math.sin(t),p[2]+u[2]*r*math.sin(t)))
 fs=[tuple(reversed(range(n))),tuple((len(path)-1)*n+i for i in range(n))]
 fs +=[(k*n+i,k*n+(i+1)%n,(k+1)*n+(i+1)%n,(k+1)*n+i)for k in range(len(path)-1)for i in range(n)]
 record(name,v,fs,m)
def ring(name,x0,x1,y,th,z0,z1,m,tr=None):
 outer=[(x0,-y),(x1,-y),(x1,y),(x0,y)];inner=[(x0+th,-y+th),(x1-th,-y+th),(x1-th,y-th),(x0+th,y-th)]
 v=[(x,y,z)for z,p in[(z0,outer),(z0,inner),(z1,outer),(z1,inner)]for x,y in p];fs=[]
 for i in range(4):
  j=(i+1)%4;fs +=[(i,j,4+j,4+i),(8+i,12+i,12+j,8+j),(i,8+i,8+j,j),(4+i,4+j,12+j,12+i)]
 if tr:v=[tr(p)for p in v]
 record(name,v,fs,m)
def rod(name,a,b,r,m,n=8):
 d=[b[i]-a[i]for i in range(3)];le=math.sqrt(sum(t*t for t in d));w=[t/le for t in d];seed=[0,0,1]if abs(w[2])<.9 else[0,1,0]
 u=[w[1]*seed[2]-w[2]*seed[1],w[2]*seed[0]-w[0]*seed[2],w[0]*seed[1]-w[1]*seed[0]];le=math.sqrt(sum(t*t for t in u));u=[t/le for t in u];v=[w[1]*u[2]-w[2]*u[1],w[2]*u[0]-w[0]*u[2],w[0]*u[1]-w[1]*u[0]]
 vs=[tuple(p[k]+r*(u[k]*math.cos(math.tau*i/n)+v[k]*math.sin(math.tau*i/n))for k in range(3))for p in[a,b]for i in range(n)]
 record(name,vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],m)
def earclip(poly):
 ids=list(range(len(poly)));out=[]
 def cross2(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 while len(ids)>3:
  done=False
  for k,i in enumerate(ids):
   a,b,c=ids[k-1],i,ids[(k+1)%len(ids)]
   if cross2(poly[a],poly[b],poly[c])<=1e-13:continue
   if any(j not in [a,b,c] and min(cross2(poly[a],poly[b],poly[j]),cross2(poly[b],poly[c],poly[j]),cross2(poly[c],poly[a],poly[j]))>=-1e-13 for j in ids):continue
   out.append((a,b,c));ids.pop(k);done=True;break
  assert done,'Cannot triangulate complete outer shell'
 out.append(tuple(ids));return out
def annular_x(name,x,z,ri,ro,th,m,n=32):
 vs=[(xx,r*math.cos(i*math.tau/n),z+r*math.sin(i*math.tau/n))for xx,r in[(x-th/2,ri),(x-th/2,ro),(x+th/2,ro),(x+th/2,ri)]for i in range(n)]
 fs=[(j*n+i,j*n+(i+1)%n,((j+1)%4)*n+(i+1)%n,((j+1)%4)*n+i)for j in range(4)for i in range(n)];record(name,vs,fs,m)
def axial_profile(name,profile,center,axis,m,n=32):
 axes=[i for i in range(3)if i!=axis];vs=[];rings=[]
 for r,z in profile:
  row=[]
  for j in range(1 if r==0 else n):
   p=list(center);p[axis]+=z;p[axes[0]]+=r*math.cos(j*math.tau/n);p[axes[1]]+=r*math.sin(j*math.tau/n);row.append(len(vs));vs.append(tuple(p))
  rings.append(row)
 fs=[]
 for k,row in enumerate(rings):
  nex=rings[(k+1)%len(rings)]
  if len(row)==len(nex)==1:continue
  for j in range(n):
   jj=(j+1)%n
   if len(row)==1:fs.append((row[0],nex[j],nex[jj]))
   elif len(nex)==1:fs.append((row[j],nex[0],row[jj]))
   else:fs.append((row[j],nex[j],nex[jj],row[jj]))
 record(name,vs,fs,m)
def runner_prism(name,p,z0,z1,m,transform):
 if sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1]for i in range(len(p)))<0:p=list(reversed(p))
 n=len(p);cap=earclip(p);v=[transform((x,y,z))for z in[z0,z1]for x,y in p]
 f=[tuple(reversed(t))for t in cap]+[tuple(i+n for i in t)for t in cap]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)]
 record(name,v,f,m)
def tube3(name,path,r,m,n=6):
 vs=[]
 for j,p in enumerate(path):
  a=path[max(0,j-1)];b=path[min(len(path)-1,j+1)];w=[b[k]-a[k]for k in range(3)];le=math.sqrt(sum(x*x for x in w));w=[x/le for x in w];seed=(0,0,1)if abs(w[2])<.9 else(1,0,0);u=[w[1]*seed[2]-w[2]*seed[1],w[2]*seed[0]-w[0]*seed[2],w[0]*seed[1]-w[1]*seed[0]];le=math.sqrt(sum(x*x for x in u));u=[x/le for x in u];v=[w[1]*u[2]-w[2]*u[1],w[2]*u[0]-w[0]*u[2],w[0]*u[1]-w[1]*u[0]]
  for i in range(n):vs.append(tuple(p[k]+r*(u[k]*math.cos(i*math.tau/n)+v[k]*math.sin(i*math.tau/n))for k in range(3)))
 fs=[tuple(reversed(range(n))),tuple((len(path)-1)*n+i for i in range(n))]+[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i)for j in range(len(path)-1)for i in range(n)];record(name,vs,fs,m)
def make_geometry():
 G.clear();PALETTE.clear()
 for c in COMPONENTS:
  raw=zlib.decompress(base64.b64decode(c['source_compressed']));assert hashlib.sha256(raw).hexdigest()==c['source_sha256']
  ns={'__name__':'preserved_whole_component'};exec(compile(raw,c['asset_id']+'/generate.py','exec'),ns);d,blob,proof=ns['compose']({});assert hashlib.sha256(ns['pack_glb'](d,blob)).hexdigest()==c['model_sha256']
  mi=len(PALETTE);PALETTE.extend(ns['PALETTE']);off=c['offset']
  for name,(v,f,mats)in ns['G'].items():G[c['label']+'__'+name]=([tuple(p[k]+off[k]for k in range(3))for p in v],list(f),[mi+i for i in mats])
 site=len(PALETTE);PALETTE.extend([('SiteWholeFloor_PaleSlate',(.30,.37,.38,1),.89),('SiteWholeBenchTop_WarmNeutral',(.43,.34,.23,1),.82),('SiteWholeBenchFrameAndPads_DeepTeal',(.07,.18,.20,1),.76)])
 box('SceneWholeFinitePreparationFloor',(-1.40,-1.24,0),(1.30,1.10,.06),site)
 box('SceneWholeSideBenchTop',(.44,-1.06,.64),(1.06,1.06,.68),site+1)
 for side,x in[('Inner',.52),('Outer',.98)]:
  for end,y in[('Front',-.94),('Rear',.94)]:box('SceneWhole'+side+end+'BenchLeg',(x-.035,y-.035,.06),(x+.035,y+.035,.652),site+2)
 for end,y in[('Front',-.94),('Rear',.94)]:box('SceneWhole'+end+'BenchCrossBrace',(.501,y-.025,.29),(.999,y+.025,.34),site+2)
 box('SceneWholeOuterLongBrace',(.959,-.955,.21),(1.001,.955,.255),site+2)
 # Two shallow full-width shaft supports have real 2-5 mm finite interior seating,
 # not an unsupported shaft hovering above a table or a coplanar contact claim.
 for i,y in enumerate([.20,.65]):
  minz=.046495398547026084-(y+.13597339080400614)*(.04/1.08)
  box('SceneWholeShaftSupport%d'%i,(.708,y-.045,.678),(.792,y+.045,.68+minz+.004),site+2)
 return G

def pack_glb(doc,blob):
 j=json.dumps(doc,separators=(',',':'),allow_nan=False).encode();j+=b' '*((-len(j))%4)
 b=bytes(blob)+b'\0'*((-len(blob))%4)
 return struct.pack('<4sII',b'glTF',2,12+8+len(j)+8+len(b))+struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(b),0x004e4942)+b
def compose(inputs):
 make_geometry();d=dict(asset={'version':'2.0','generator':'Original static mesh construction'},scene=0,scenes=[{'name':TITLE,'nodes':[0]}],nodes=[{'name':'AssetRoot__'+ASSET,'children':[]}],meshes=[],materials=[{'name':n,'doubleSided':True,'pbrMetallicRoughness':{'baseColorFactor':c,'metallicFactor':0.,'roughnessFactor':r}}for n,c,r in PALETTE],accessors=[],bufferViews=[],buffers=[]);blob=bytearray()
 def array(values,component,kind):
  flat=[v for row in values for v in row]if kind=='VEC3'else values;fmt='f'if component==5126 else'I';raw=struct.pack('<'+fmt*len(flat),*flat);offset=len(blob);blob.extend(raw);blob.extend(b'\0'*((-len(blob))%4));view=len(d['bufferViews']);d['bufferViews'].append({'buffer':0,'byteOffset':offset,'byteLength':len(raw)});a={'bufferView':view,'componentType':component,'count':len(values),'type':kind}
  if kind=='VEC3':a.update(min=[min(p[k]for p in values)for k in range(3)],max=[max(p[k]for p in values)for k in range(3)])
  index=len(d['accessors']);d['accessors'].append(a);return index
 for name,(v,fs,mats)in G.items():
  prim=[]
  for mat in sorted(set(mats)):
   positions=[];normals=[]
   for ids,mi in zip(fs,mats):
    if mi!=mat:continue
    a,b,c=[v[i]for i in ids];u=[b[k]-a[k]for k in range(3)];w=[c[k]-a[k]for k in range(3)];n=(u[1]*w[2]-u[2]*w[1],u[2]*w[0]-u[0]*w[2],u[0]*w[1]-u[1]*w[0]);le=math.sqrt(sum(x*x for x in n));assert le>1e-12;n=[x/le for x in n];positions.extend((x,z,-y)for x,y,z in[a,b,c]);normals.extend([(n[0],n[2],-n[1])]*3)
   prim.append({'attributes':{'POSITION':array(positions,5126,'VEC3'),'NORMAL':array(normals,5126,'VEC3')},'indices':array(list(range(len(positions))),5125,'SCALAR'),'material':mat,'mode':4})
  mesh=len(d['meshes']);d['meshes'].append({'name':name,'primitives':prim});node=len(d['nodes']);d['nodes'].append({'name':name,'mesh':mesh});d['nodes'][0]['children'].append(node)
 d['buffers']=[{'byteLength':len(blob)}];return d,bytes(blob),{'new_original_geometry':True,'triangles':sum(len(f)for v,f,m in G.values()),'mesh_count':len(G),'whole_original_model_count':0,'preserved_complete_source_models':2,'new_scene_count':1,'static_pose_only':True}

def main():
 import bpy,sys,time
 from mathutils import Vector
 OUT=Path(__file__).resolve().parent
 inputs={k:zlib.decompress(base64.b64decode(v['compressed']))for k,v in INPUTS.items()}
 for k,raw in inputs.items():assert hashlib.sha256(raw).hexdigest()==INPUTS[k]['sha256']
 for v in SOURCE_INPUTS.values():assert hashlib.sha256(zlib.decompress(base64.b64decode(v['compressed']))).hexdigest()==v['sha256']
 document,blob,proof=compose(inputs);model=pack_glb(document,blob);(OUT/'model.glb').write_bytes(model)
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==104
 triangle_count=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons);assert triangle_count==proof['triangles']
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 lo=[min(v[k]for v in points)for k in range(3)];hi=[max(v[k]for v in points)for k in range(3)]
 assert abs(lo[2])<=TOL
 assert len({m for o in parts for m in o.data.materials})==11
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'),compress=False)
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
 for layer in scene.view_layers:layer.cycles.use_denoising=False
 scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
 scene.render.resolution_x=scene.render.resolution_y=640;scene.render.resolution_percentage=100
 scene.world=scene.world or bpy.data.worlds.new('Neutral instrument preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.58))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,22),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(4,-6,4.8));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 def config():return dict(engine=scene.render.engine,samples=scene.cycles.samples,adaptive=scene.cycles.use_adaptive_sampling,cycles_denoise=scene.cycles.use_denoising,view_layer_denoise=[x.cycles.use_denoising for x in scene.view_layers],compositor_nodes=scene.use_nodes,compositing=scene.render.use_compositing,threads_mode=scene.render.threads_mode,threads=scene.render.threads)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'asset':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':104,'mesh_objects':104,'triangles':triangle_count,'materials':11,'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
 qa['native_saved_render_config']=config();qa['render_configs']={}
 if '--geometry-only' not in sys.argv:
  view=sys.argv[sys.argv.index('--tier-single-view')+1]if '--tier-single-view'in sys.argv else 'thumbnail';assert view in ['qa-front','thumbnail']
  scene.cycles.samples=16 if view=='qa-front' else 128;qa['render_configs'][view]=config();scene.render.filepath=str(OUT/(view+'.png'));start=time.monotonic();bpy.ops.render.render(write_still=True);qa['render']={'view':view,'samples':scene.cycles.samples,'seconds':time.monotonic()-start,'original_pixels_reviewed':False}
 (OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if p.exists():files[role]={'path':f'assets/sports/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'scenes','assetKind':'scene','theme':'sports','style':'source-preserved-low-poly','title':TITLE,'description':'One static sports-equipment preparation bay, zero new models and one scene. Two complete accepted original models retain their entire geometry, metre scale and opaque PBR values: a tilted mesh rebounder stands at the left on its original four pads, while a whole lacrosse-inspired stick lies along the separate right-hand braced bench. Two small finite bench-top supports seat the original shaft without altering it. One new finite floor and complete subordinate braced bench leave an open front approach and a positive interval between the whole props. Embedded complete original source and whole-GLB hashes are checked before translation-only composition. No extracted fragments, scaled replacements, changed original materials or repeated model count. Empty illustrative static layout only, no training sequence, interaction, ball return, stick use, loading, fit, regulation, manufacture or safety claim.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':11,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
