import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='music-fixed-bound-drone-and-two-five-port-reed-pipes-display-01'
TITLE='Fixed Bound Drone and Two Five Port Reed Pipes Display'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeCaneLookPipeWalls',(.56,.36,.15,1),.78),('WholePlainFixedReedTongues',(.28,.14,.045,1),.83),('WholePairBindingBands',(.16,.075,.027,1),.88),('WholeLowCompleteDisplayCarrier',(.17,.23,.22,1),.86)]
G={}

def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def mesh_boundary(name,vertices,faces,m):
 # Orient a closed connected manifold coherently before exporting flat faces.
 edges={}
 for i,f in enumerate(faces):
  for a,b in zip(f,f[1:]+f[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((i,a,b))
 assert all(len(v)==2 for v in edges.values()),name
 signs={0:1};todo=[0]
 while todo:
  i=todo.pop()
  for a,b in zip(faces[i],faces[i][1:]+faces[i][:1]):
   for j,c,d in edges[tuple(sorted((a,b)))]:
    if i==j:continue
    want=signs[i]*(-1 if(a,b)==(c,d)else 1)
    if j in signs:assert signs[j]==want
    else:signs[j]=want;todo.append(j)
 assert len(signs)==len(faces);faces=[f if signs[i]>0 else tuple(reversed(f))for i,f in enumerate(faces)];record(name,vertices,faces,m)
def pipe(name,x,y0,r,holes):
 N=32;ends=[y0,.290,.300,.309,.312,.329,.335]+[v for c in holes for v in[c-.005,c+.005]];ys=sorted(set(ends));v=[]
 for outer in[True,False]:
  for y in ys:
   ro=r if y<=.290 else r*(1-(1-.65)*min(1,(y-.290)/.010));rr=ro if outer else ro-.0025
   for i in range(N):a=math.tau*i/N;v.append((x+rr*math.cos(a),y,.035+rr*math.sin(a)))
 def vid(side,j,i):return(side*len(ys)+j)*N+i%N
 present={(j,i)for j in range(len(ys)-1)for i in range(N)if not(6<=i<10 and any(abs((ys[j]+ys[j+1])/2-c)<.005-1e-9 for c in holes))and not(7<=i<9 and .312<(ys[j]+ys[j+1])/2<.329)};f=[]
 for j,i in sorted(present):
  k=(i+1)%N;f.extend([(vid(0,j,i),vid(0,j,k),vid(0,j+1,k),vid(0,j+1,i)),(vid(1,j,k),vid(1,j,i),vid(1,j+1,i),vid(1,j+1,k))])
  if(j-1,i)not in present:f.append((vid(0,j,k),vid(0,j,i),vid(1,j,i),vid(1,j,k)))
  if(j+1,i)not in present:f.append((vid(0,j+1,i),vid(0,j+1,k),vid(1,j+1,k),vid(1,j+1,i)))
  if(j,(i-1)%N)not in present:f.append((vid(0,j,i),vid(0,j+1,i),vid(1,j+1,i),vid(1,j,i)))
  if(j,k)not in present:f.append((vid(0,j+1,k),vid(0,j,k),vid(1,j,k),vid(1,j+1,k)))
 mesh_boundary(name,v,f,0)
 # A separate plain fixed tongue roots at the short top socket wall and lifts above its window.
 z=.035+r*.65;vv=[(x+dx,y,z+dz)for y,dz in[(.310,-.0006),(.327,.0007),(.310,.0002),(.327,.0015)]for dx in[-.0018,.0018]];ff=[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)];record(name+'__WholeFixedTongue',vv,ff,1)
def band(name,y):
 a=[(-.039,.0255),(.000,.0255),(.000,.0445),(-.039,.0445)];b=[(-.0365,.0275),(-.0055,.0275),(-.0055,.0425),(-.0365,.0425)];v=[(x,t,z)for t in[y-.003,y+.003]for p in[a,b]for x,z in p];f=[]
 for i in range(4):k=(i+1)%4;f.extend([(i,k,8+k,8+i),(4+k,4+i,12+i,12+k),(k,i,4+i,4+k),(8+i,8+k,12+k,12+i)])
 mesh_boundary(name,v,f,2)
def carrier():
 xs=[-.075,.075];ys=[-.325,.032,.048,.232,.248,.350];zs=[0,.008,.030];occupied={(0,j,0)for j in range(5)}|{(0,1,1),(0,3,1)};v=[];f=[];lookup={}
 def vert(i,j,k):
  key=(i,j,k)
  if key not in lookup:lookup[key]=len(v);v.append((xs[i],ys[j],zs[k]))
  return lookup[key]
 directions=[((-1,0,0),[(0,0,0),(0,0,1),(0,1,1),(0,1,0)]),((1,0,0),[(1,0,0),(1,1,0),(1,1,1),(1,0,1)]),((0,-1,0),[(0,0,0),(1,0,0),(1,0,1),(0,0,1)]),((0,1,0),[(0,1,0),(0,1,1),(1,1,1),(1,1,0)]),((0,0,-1),[(0,0,0),(0,1,0),(1,1,0),(1,0,0)]),((0,0,1),[(0,0,1),(1,0,1),(1,1,1),(0,1,1)])]
 for i,j,k in sorted(occupied):
  for (di,dj,dk),corners in directions:
   if(i+di,j+dj,k+dk)not in occupied:f.append(tuple(vert(i+a,j+b,k+c)for a,b,c in corners))
 mesh_boundary('WholeLowTwinRailDisplayCarrier',v,f,3)
def make_geometry():
 G.clear();global PIPE_SPECS,SHIFT
 PIPE_SPECS=[('WholeLongUnperforatedDrone',-.030,-.300,.008,[]),('WholeBoundFivePortChanter',-.012,-.150,.0075,[-.025,.015,.075,.115,.155]),('WholeSeparateFivePortChanter',.045,-.080,.007,[.005,.045,.085,.125,.165])]
 for name,x,y,r,h in PIPE_SPECS:pipe(name,x,y,r,h)
 band('WholeUpperPairedPipeBinding',.275);band('WholeLowerPairedPipeBinding',.185);carrier();SHIFT=(0.,.0125,0.)
 for name,(v,f,m)in list(G.items()):G[name]=([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)
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
 d['buffers']=[{'byteLength':len(blob)}];return d,bytes(blob),{'new_original_geometry':True,'triangles':sum(len(f)for v,f,m in G.values()),'mesh_count':len(G),'whole_original_model_count':1,'static_pose_only':True}
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
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==len(G)
 triangle_count=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons);assert triangle_count==proof['triangles']
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 lo=[min(v[k]for v in points)for k in range(3)];hi=[max(v[k]for v in points)for k in range(3)]
 assert abs(lo[2])<=TOL
 assert len({m for o in parts for m in o.data.materials})==4
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
 for layer in scene.view_layers:layer.cycles.use_denoising=False
 scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
 scene.render.resolution_x=scene.render.resolution_y=640;scene.render.resolution_percentage=100
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole triple reed-pipe inspection display');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.024))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(3.0,-4.8,6.2));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'),compress=False)
 def config():return dict(engine=scene.render.engine,samples=scene.cycles.samples,adaptive=scene.cycles.use_adaptive_sampling,cycles_denoise=scene.cycles.use_denoising,view_layer_denoise=[x.cycles.use_denoising for x in scene.view_layers],compositor_nodes=scene.use_nodes,compositing=scene.render.use_compositing,threads_mode=scene.render.threads_mode,threads=scene.render.threads)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'asset':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':len(G),'mesh_objects':len(G),'triangles':triangle_count,'materials':4,'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
 qa['native_saved_render_config']=config();qa['render_configs']={}
 if '--geometry-only' not in sys.argv:
  view=sys.argv[sys.argv.index('--tier-single-view')+1]if '--tier-single-view'in sys.argv else 'thumbnail';assert view in ['qa-front','thumbnail']
  scene.cycles.samples=16 if view=='qa-front' else 128;qa['render_configs'][view]=config();scene.render.filepath=str(OUT/(view+'.png'));start=time.monotonic();bpy.ops.render.render(write_still=True);qa['render']={'view':view,'samples':scene.cycles.samples,'seconds':time.monotonic()-start,'original_pixels_reviewed':False}
 (OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if p.exists():files[role]={'path':f'assets/music/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete launeddas-inspired three-reed-pipe display. One full long unperforated drone and one shorter five-port chanter are joined by two complete finite binding bands; a third shorter five-port chanter remains laterally separate on the same whole low two-rail display carrier. All three whole cane-looking tubes have continuous open bores, open terminal mouths and narrowed short sockets. Each socket has a genuine upper window and one complete fixed lifted tongue exterior rooted at its rear edge. The ten main finger apertures are real quadrangular openings through full finite wall thickness, not painted discs. All numeric tube surfaces, hole locations, sockets, tongue shapes, bindings and carrier are new. The bound pair plus independent five-port pipe organization differs from seven stopped panpipes, a central bag with five attached pipes and a cluster over a socketed windchest; it is not a pipe-count alteration of those models. Nine whole closed editable meshes, four constant opaque PBR roles, metres native Z up and finite complete display-carrier ground sole. One whole instrument-display prop zero scenes; the carrier is not a separate counted asset. Broad Sardinian instrument inspiration only, deliberately horizontal inspection display rather than playing pose or historically exact cuntzertu. No sound, tuning, calibrated fingering, actual vibrating reeds, wax, continuous playable air path, breath technique, bodily contact, articulation, pipe tying performance, stability, material identity, manufacture or safety capability. No rig, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
