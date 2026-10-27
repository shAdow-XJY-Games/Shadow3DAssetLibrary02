'One original static sports preparation bay scene. The complete accepted horseshoe throwing cage and complete accepted laid-wire throwing hammer are preserved with every original mesh, triangle, dimension and opaque PBR material, translated only. The empty cage opens onto a clear forward apron; the entire rested implement is separately displayed on an outside side preparation table rather than occupying the entry. New finite ground slab, table supports and modest approach strips organize the space. Both complete source generators and exact GLB hashes are embedded and verified before composition; nothing is extracted, rescaled, recoloured, deformed or counted as a new independent prop. Zero new models and one scene. Static illustrative unoccupied preparation layout only, no throwing action, user route certification, regulation dimensions, equipment compatibility, impact containment, loading, manufacture or safety claim.'
import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='sports-whole-open-sector-cage-and-separated-hammer-preparation-bay-scene-01'
TITLE='Open Sector Cage And Separated Hammer Preparation Bay'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
COMPONENTS=[{'label': 'CompleteCage', 'asset_id': 'sports-fixed-horseshoe-net-and-open-sector-throwing-cage-01', 'source_sha256': 'ec97fec55b7a84318fcd4fc236193164694e683a506e823cd33560d30293a4e8', 'model_sha256': 'd0729111a4738c1089f17789b294ca8a7b242b7c57dbe85ff88942b445f4fdb6', 'source_compressed': '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', 'offset': [-0.6, 0, 0.12], 'verified_backup': 'libfile_387823c8ed0c8191b6db87632fd13b8a'}, {'label': 'CompleteHammer', 'asset_id': 'sports-fixed-round-head-and-long-wire-throwing-hammer-01', 'source_sha256': 'cfca8d4a111e2a107cab9ec642eeb2b81d7164b0457f5fa60f0577b35f7327b7', 'model_sha256': '4cf484dc7f0a9fb23c364d11c1207153b0679aee5f8a23788f0a1ff549d49864', 'source_compressed': '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', 'offset': [3.35, -2.0, 0.96], 'verified_backup': 'libfile_9a735e9380588191af421a8f026c153e'}]
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
 site=len(PALETTE);PALETTE.extend([('SiteSlab_LightSlate',(.30,.36,.36,1),.88),('SitePrepTable_WarmBoard',(.49,.36,.20,1),.78),('SiteApproachMarkers_WarmWhite',(.72,.70,.58,1),.80)])
 box('SceneWholeFiniteSiteSlab',(-4,-3.8,0),(4,3.8,.12),site)
 box('SceneWholeSeparatePrepTableTop',(3.02,-3.05,.86),(3.68,-.95,.96),site+1)
 for i,x in enumerate([3.10,3.60]):
  for j,y in enumerate([-2.94,-1.06]):box('SceneWholeTableLeg%d%d'%(i,j),(x-.045,y-.045,.12),(x+.045,y+.045,.89),site)
 for i,y in enumerate([-2.94,-1.06]):box('SceneWholeTableCrossBrace%d'%i,(3.08,y-.025,.35),(3.62,y+.025,.41),site)
 for i,y in enumerate([-.75,.75]):box('SceneWholeApproachGuide%d'%i,(2.35,y-.045,.119),(3.90,y+.045,.128),site+2)
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
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==67
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
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,1.5))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,22),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(10,-11,9));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 def config():return dict(engine=scene.render.engine,samples=scene.cycles.samples,adaptive=scene.cycles.use_adaptive_sampling,cycles_denoise=scene.cycles.use_denoising,view_layer_denoise=[x.cycles.use_denoising for x in scene.view_layers],compositor_nodes=scene.use_nodes,compositing=scene.render.use_compositing,threads_mode=scene.render.threads_mode,threads=scene.render.threads)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'asset':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':67,'mesh_objects':67,'triangles':triangle_count,'materials':11,'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
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
  meta={'id':ASSET,'version':'1.0.0','category':'scenes','assetKind':'scene','theme':'sports','style':'source-preserved-low-poly','title':TITLE,'description':'One original static sports preparation bay scene. The complete accepted horseshoe throwing cage and complete accepted laid-wire throwing hammer are preserved with every original mesh, triangle, dimension and opaque PBR material, translated only. The empty cage opens onto a clear forward apron; the entire rested implement is separately displayed on an outside side preparation table rather than occupying the entry. New finite ground slab, table supports and modest approach strips organize the space. Both complete source generators and exact GLB hashes are embedded and verified before composition; nothing is extracted, rescaled, recoloured, deformed or counted as a new independent prop. Zero new models and one scene. Static illustrative unoccupied preparation layout only, no throwing action, user route certification, regulation dimensions, equipment compatibility, impact containment, loading, manufacture or safety claim.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':11,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
