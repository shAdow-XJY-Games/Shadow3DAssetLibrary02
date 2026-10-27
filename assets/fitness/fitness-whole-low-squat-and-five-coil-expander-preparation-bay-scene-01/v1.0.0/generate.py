'One static fitness-equipment preparation bay, zero new models and one scene. Two complete accepted originals retain all geometry, metre scale and opaque PBR: the whole low footplate and upright calf-pad station stands on the left floor using its four original ground pads, and the whole five-coil expander rests flat on a separate right low braced bench by its original grip soles. The finite shared floor keeps a clear front access strip and separated full source bounds. Complete embedded original source and whole-GLB hashes are checked before translation-only composition; no extraction, scaling, recolouring or repeated model count. Empty illustrative layout only, no exercise sequence, physical use, belt or spring force, training advice, therapeutic benefit, body fit, loading, manufacture or safety claim.'
import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='fitness-whole-low-squat-and-five-coil-expander-preparation-bay-scene-01'
TITLE='Low Squat And Five Coil Expander Preparation Bay'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
COMPONENTS=[{'label': 'CompleteSquatStation', 'asset_id': 'fitness-fixed-low-footplate-and-upright-calf-pad-squat-station-01', 'source_sha256': 'a918e828a03fb29bc12432a64d71db0ac576d8e349480192d227da89a30155cc', 'model_sha256': '3c9ff1ffe009266f9c2e6ac0db2420b6d0c765cf96ca76ad739a3a1f88b23bc1', 'source_compressed': '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', 'offset': [-0.38, 0, 0.04], 'verified_backup': 'libfile_16127de7e85c8191bf1908a2e398c99c'}, {'label': 'CompleteExpander', 'asset_id': 'fitness-fixed-five-extension-coils-and-opposed-loop-grips-01', 'source_sha256': 'ef294cf24508b9df90ba89f75204e9e3a87b5e99698737d66bb6df7f5351e0b6', 'model_sha256': '8a0cab4c35dc54a17fed327a3410733be274eb04f6d3e5cd786e24d82eb2be51', 'source_compressed': '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', 'offset': [0.37, 0.05, 0.46], 'verified_backup': 'libfile_4c011a3f22c881918f8363d38f9badce'}]
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
 site=len(PALETTE);PALETTE.extend([('SiteWholeFloor_PaleSlate',(.31,.38,.39,1),.89),('SiteWholeBenchTop_WarmNeutral',(.42,.33,.22,1),.82),('SiteWholeBenchFrame_DeepTeal',(.07,.18,.20,1),.76)])
 box('SceneWholeFinitePreparationFloor',(-.78,-.75,0),(.68,.75,.04),site)
 box('SceneWholeLowBenchTop',(.18,-.40,.42),(.56,.50,.46),site+1)
 for side,x in[('Outer',.515),('Inner',.225)]:
  for end,y in[('Front',-.34),('Rear',.44)]:box('SceneWhole'+side+end+'BenchLeg',(x-.025,y-.025,.04),(x+.025,y+.025,.429),site+2)
 for end,y in[('Front',-.34),('Rear',.44)]:box('SceneWhole'+end+'BenchCrossBrace',(.207,y-.019,.19),(.533,y+.019,.225),site+2)
 box('SceneWholeOuterLongBrace',(.496,-.355,.13),(.534,.455,.164),site+2)
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
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==46
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
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.26))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,22),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(3,-5,4.5));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 def config():return dict(engine=scene.render.engine,samples=scene.cycles.samples,adaptive=scene.cycles.use_adaptive_sampling,cycles_denoise=scene.cycles.use_denoising,view_layer_denoise=[x.cycles.use_denoising for x in scene.view_layers],compositor_nodes=scene.use_nodes,compositing=scene.render.use_compositing,threads_mode=scene.render.threads_mode,threads=scene.render.threads)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'asset':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':46,'mesh_objects':46,'triangles':triangle_count,'materials':11,'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
 qa['native_saved_render_config']=config();qa['render_configs']={}
 if '--geometry-only' not in sys.argv:
  view=sys.argv[sys.argv.index('--tier-single-view')+1]if '--tier-single-view'in sys.argv else 'thumbnail';assert view in ['qa-front','thumbnail']
  scene.cycles.samples=16 if view=='qa-front' else 128;qa['render_configs'][view]=config();scene.render.filepath=str(OUT/(view+'.png'));start=time.monotonic();bpy.ops.render.render(write_still=True);qa['render']={'view':view,'samples':scene.cycles.samples,'seconds':time.monotonic()-start,'original_pixels_reviewed':False}
 (OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if p.exists():files[role]={'path':f'assets/fitness/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'scenes','assetKind':'scene','theme':'fitness','style':'source-preserved-low-poly','title':TITLE,'description':'One static fitness-equipment preparation bay, zero new models and one scene. Two complete accepted originals retain all geometry, metre scale and opaque PBR: the whole low footplate and upright calf-pad station stands on the left floor using its four original ground pads, and the whole five-coil expander rests flat on a separate right low braced bench by its original grip soles. The finite shared floor keeps a clear front access strip and separated full source bounds. Complete embedded original source and whole-GLB hashes are checked before translation-only composition; no extraction, scaling, recolouring or repeated model count. Empty illustrative layout only, no exercise sequence, physical use, belt or spring force, training advice, therapeutic benefit, body fit, loading, manufacture or safety claim.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':11,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
