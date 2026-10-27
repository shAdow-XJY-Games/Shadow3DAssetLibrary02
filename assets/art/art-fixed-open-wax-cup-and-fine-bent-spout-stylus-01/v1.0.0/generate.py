import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='art-fixed-open-wax-cup-and-fine-bent-spout-stylus-01'
TITLE='Fixed Open Wax Cup and Fine Bent Spout Stylus'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeWarmCopperCupAndSpout',(.56,.26,.115,1),.48),('WholeDarkCopperInterior',(.24,.10,.041,1),.63),('WholeCopperLipAndNeckBand',(.66,.37,.17,1),.45),('WholeWarmWoodenHandle',(.47,.29,.11,1),.82)]
G={}

def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def consistent_record(name,v,fs,m):
 ts=[];ms=[]
 for j,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));ms.append(m[j]if isinstance(m,list)else m)
 edges={}
 for i,t in enumerate(ts):
  for a,b in zip(t,t[1:]+t[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((i,a,b))
 assert all(len(e)==2 for e in edges.values()),'closed topology'
 signs={0:1};todo=[0]
 while todo:
  i=todo.pop()
  for a,b in zip(ts[i],ts[i][1:]+ts[i][:1]):
   for j,c,d in edges[tuple(sorted((a,b)))]:
    if j==i:continue
    sign=signs[i]*(-1 if(a,b)==(c,d)else 1)
    if j in signs:assert signs[j]==sign
    else:signs[j]=sign;todo.append(j)
 assert len(signs)==len(ts),'one connected shell'
 record(name,v,[t if signs[i]>0 else tuple(reversed(t))for i,t in enumerate(ts)],ms)
def make_geometry():
 G.clear()
 # Whole oval cup and long narrowing down-curved outlet form one material shell.
 zs=[0,.003,.006,.010,.014,.019,.022];rs=[.45,.73,.91,1.,1.,.96,.96]
 angles=[math.pi-.28+.28*i for i in range(3)]+[math.pi+.28+(math.tau-.56)*i/30 for i in range(1,30)];N=len(angles);K=len(zs);v=[];fs=[];ms=[]
 for inner in[False,True]:
  for k,(z,r)in enumerate(zip(zs,rs)):
   r=r-(.10 if inner else 0);zz=.002 if inner and k==0 else z
   v.extend((.018*r*math.cos(a),.013*r*math.sin(a),zz)for a in angles)
 def ix(inner,k,i):return int(inner)*K*N+k*N+i%N
 def face(f,m):fs.append(f);ms.append(m)
 for inner in[False,True]:
  for k in range(K-1):
   for i in range(N):
    if 2<=k<4 and 0<=i<2:continue
    face([ix(inner,k,i),ix(inner,k,i+1),ix(inner,k+1,i+1),ix(inner,k+1,i)],1 if inner else 0)
 boundary=[(2,i)for i in range(3)]+[(k,2)for k in range(3,5)]+[(4,i)for i in range(1,-1,-1)]+[(3,0)]
 # Conforming continuous branch: no opaque wall or capped tube crosses its entrance.
 roots=[[ix(inner,k,i)for k,i in boundary]for inner in[False,True]]
 dirs=[math.atan2(zs[k]-.010,(angles[i]-math.pi)*.013)for k,i in boundary]
 final=[]
 path=[(-.024,.010, .0032,.0021),(-.031,.008, .0024,.0014),(-.037,.0045,.0018,.0010),(-.041,.003,.00165,.0009)]
 for inner in[False,True]:
  prev=roots[int(inner)]
  for q,(x,z,ro,ri)in enumerate(path):
   # Rings are in YZ planes; end channel is intentionally narrow but truly open.
   r=ri if inner else ro;row=[]
   for a in dirs:row.append(len(v));v.append((x,-r*math.cos(a),z+r*math.sin(a)))
   for j in range(8):face([prev[j],prev[(j+1)%8],row[(j+1)%8],row[j]],1 if inner else 0)
   prev=row
  final.append(prev)
 for j in range(8):face([final[0][j],final[0][(j+1)%8],final[1][(j+1)%8],final[1][j]],2)
 cb=len(v);v.append((0,0,0));ci=len(v);v.append((0,0,.002))
 for i in range(N):
  j=(i+1)%N;face([cb,ix(False,0,j),ix(False,0,i)],0);face([ci,ix(True,0,i),ix(True,0,j)],1);face([ix(False,K-1,i),ix(False,K-1,j),ix(True,K-1,j),ix(True,K-1,i)],2)
 # Drop unused patch-centre vertices before bounds computation.
 used=sorted(set(j for f in fs for j in f));mp={j:i for i,j in enumerate(used)}
 consistent_record('WholeContinuousOpenOvalCupAndNarrowDownwardSpout',[v[j]for j in used],[[mp[j]for j in f]for f in fs],ms)
 # Complete long polygonal wooden grip, pointed root fitted into rear cup shoulder.
 profile=[(.014,.0020,.012),(.025,.0053,.010),(.039,.0075,.007244443697),(.125,.0075,.007244443697),(.133,.0065,.007244443697),(.137,.0045,.007244443697)]
 v=[(x,r*math.cos(math.tau*i/12+math.pi/12),z+r*math.sin(math.tau*i/12+math.pi/12))for x,r,z in profile for i in range(12)];fs=[tuple(reversed(range(12))),tuple((len(profile)-1)*12+i for i in range(12))]
 for k in range(len(profile)-1):
  for i in range(12):j=(i+1)%12;fs.append((k*12+i,k*12+j,(k+1)*12+j,(k+1)*12+i))
 record('WholeTaperRootLongWoodenGrip',v,fs,3)
 # A genuine hollow neck ferrule encloses the root, rather than a floating dark decal.
 profile=[(.024,.0057),(.032,.0072),(.032,.0061),(.024,.0046)];v=[(x,r*math.cos(math.tau*i/24),(.010-(x-.025)*.09)+r*math.sin(math.tau*i/24))for x,r in profile for i in range(24)];fs=[]
 for k in range(4):
  for i in range(24):j=(i+1)%24;kk=(k+1)%4;fs.append((k*24+i,k*24+j,kk*24+j,kk*24+i))
 record('WholeHollowCopperRootFerrule',v,fs,2)
 pts=[p for v,f,m in G.values()for p in v];lo=[min(p[k]for p in pts)for k in range(3)];hi=[max(p[k]for p in pts)for k in range(3)]
 global SHIFT
 SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2])
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral complete craft tool preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.010))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(-2.4,-6.,4.7));bpy.context.view_layer.update()
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
  if p.exists():files[role]={'path':f'assets/art/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'art','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete canting-inspired static wax-drawing tool appearance. A small empty oval copper cup and its fine downward-curving spout are one continuous finite-thickness hollow material shell, with a genuine open filling mouth and communicating small outlet, not an opaque cup with a capped rod. A complete tapered-root long wooden grip extends from the rear shoulder and carries a full hollow copper ferrule. The shallow cup base and flat lower grip facets give finite resting contacts. All numerical geometry newly authored: not a resized watering can, fountain pen, soldering iron or extracted copper-stamp part. One model zero scenes, four opaque PBR materials, metre scale and native Z up. Broad traditional craft-tool category inspiration only; no copied museum object, cultural motif or exact historical reconstruction. Empty static visual only: no wax, heat, fluid simulation, actual flow, precision line, thermal insulation, grip, manufacture, operating or safety capability. No animation, rig or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
