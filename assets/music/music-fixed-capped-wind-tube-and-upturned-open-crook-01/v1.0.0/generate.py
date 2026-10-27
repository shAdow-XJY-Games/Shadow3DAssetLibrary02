import base64,copy,hashlib,json,math,struct,zlib,collections
from pathlib import Path
ASSET='music-fixed-capped-wind-tube-and-upturned-open-crook-01'
TITLE='Fixed Capped Wind Tube and Upturned Open Crook'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeContinuousCrookHoneyWood',(.46,.25,.095,1),.69),('WholeBoreAndPortRevealsDarkWood',(.10,.045,.020,1),.81),('WholeWindCapDeepBrown',(.19,.075,.030,1),.64),('WholeBandsWarmAlloy',(.47,.37,.19,1),.51)]
G={}

def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def lathe_profile(name,profile,mat,n=48):
 v=[];rings=[];fs=[]
 for r,z in profile:
  if r==0:rings.append([len(v)]);v.append((0,0,z))
  else:
   row=[]
   for i in range(n):row.append(len(v));v.append((r*math.cos(math.tau*i/n+math.pi/n),r*math.sin(math.tau*i/n+math.pi/n),z))
   rings.append(row)
 for a,b in zip(rings,rings[1:]+rings[:1]):
  if len(a)==len(b)==1:continue
  for i in range(n):
   j=(i+1)%n
   if len(a)==1:fs.append((a[0],b[j],b[i]))
   elif len(b)==1:fs.append((a[i],a[j],b[0]))
   else:fs.append((a[i],a[j],b[j],b[i]))
 record(name,v,fs,mat)
def thick_grid_tube(name,outer,inner,removed,outermat=0):
 N=len(outer[0]);K=len(outer);off=N*K;v=[p for row in outer+inner for p in row];fs=[];ms=[];edges={}
 for k in range(K-1):
  for i in range(N):
   if(k,i)in removed:continue
   q=[k*N+i,k*N+(i+1)%N,(k+1)*N+(i+1)%N,(k+1)*N+i];fs.extend([q,[j+off for j in reversed(q)]]);ms.extend([outermat,1])
   for a,b in zip(q,q[1:]+q[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((a,b))
 # Every boundary of the actual surface domain, including each port and each end, is bridged through the finite wall.
 for pair in edges.values():
  if len(pair)==1:
   a,b=pair[0];fs.append([a,a+off,b+off,b]);ms.append(1)
  else:assert len(pair)==2
 record(name,v,fs,ms)
def make_geometry():
 G.clear();global PORT_Z;PORT_Z=[.255,.310,.365,.420,.475,.530,.585];N=48;phase=math.pi/N
 zs=sorted(set([.680,.650,.620,.210,.180]+[h+d for h in PORT_Z for d in[-.006,-.003,0,.003,.006]]),reverse=True)
 path=[(0.,0.,z)for z in zs]
 # A complete new J-shaped centreline. A short bottom tangent gives a finite polygonal resting facet without an added stand.
 path +=[(.09-.09*math.cos(math.pi*j/32),0.,.18-.09*math.sin(math.pi*j/32))for j in range(1,17)]
 path +=[(x,0.,.09)for x in[.105,.120,.135,.150]]
 path +=[(.15+.09*math.sin(math.pi*j/32),0.,.18-.09*math.cos(math.pi*j/32))for j in range(1,17)]
 path +=[(.24,0.,.215),(.24,0.,.240),(.24,0.,.260)]
 outer=[];inner=[]
 for k,c in enumerate(path):
  a=path[max(0,k-1)];b=path[min(len(path)-1,k+1)];dx=b[0]-a[0];dz=b[2]-a[2];le=math.hypot(dx,dz);w=(-dz/le,0,dx/le)
  ro=.0145 if k<len(path)-3 else .0145+.0025*(k-(len(path)-4))/3;ri=.009 if k<len(path)-3 else .009+.002*(k-(len(path)-4))/3
  for arr,r in[(outer,ro),(inner,ri)]:arr.append([tuple(c[q]+r*((1 if q==1 else 0)*math.cos(math.tau*i/N+phase)+w[q]*math.sin(math.tau*i/N+phase))for q in range(3))for i in range(N)])
 removed=set()
 for k,(za,zb)in enumerate(zip(zs,zs[1:])):
  mid=(za+zb)/2
  for h in PORT_Z:
   if abs(mid-h)<.006:
    columns=[22,23,24]if abs(mid-h)>.003 else[21,22,23,24,25]
    removed.update((k,i)for i in columns)
 thick_grid_tube('WholeContinuousSevenPortJBody',outer,inner,removed,0)
 # Whole hollow wind cap: broad socket at the root narrows to a genuine small oval top slot. Concealed reed is not modeled.
 rows=[(.655,.0185,.0185,.0130,.0130),(.673,.020,.020,.013,.013),(.708,.0188,.0188,.011,.011),(.728,.016,.015,.008,.006),(.742,.012,.009,.0048,.0024)]
 outer=[];inner=[]
 for z,rx,ry,ix,iy in rows:
  outer.append([(rx*math.sin(math.tau*i/N+phase),ry*math.cos(math.tau*i/N+phase),z)for i in range(N)]);inner.append([(ix*math.sin(math.tau*i/N+phase),iy*math.cos(math.tau*i/N+phase),z)for i in range(N)])
 thick_grid_tube('WholeHollowSocketAndSlottedWindCap',outer,inner,set(),2)
 lathe_profile('WholeWindCapRootBand',[(.018,.657),(.0208,.657),(.0208,.667),(.018,.667)],3,48)
 lathe_profile('WholeOpenCrookEndBand',[(.0152,.238),(.0185,.238),(.0185,.251),(.0152,.251)],3,48)
 v,f,m=G['WholeOpenCrookEndBand'];G['WholeOpenCrookEndBand']=([(x+.24,y,z)for x,y,z in v],f,m)
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole capped crook preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.33))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(2.6,-8.,3.4));bpy.context.view_layer.update()
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored whole crumhorn-inspired fixed wind-instrument appearance. A single continuous finite-wall J-shaped wooden-look tube has seven true polygonal front finger ports, a rounded lower return with a short finite bottom resting facet, and one open upturned mouth. Its entire hollow socketed wind cap narrows to a real small oval top slot; the cap seats around the upper body and two whole annular alloy-look bands finish the cap root and crook end. Every body coordinate and port layout is newly authored, not a bent old blockflute, reused bassoon boot or separate horn assembly. One model zero scenes, four opaque PBR roles, metres and native Z up. Broad capped-reed/J-shaped category inspiration only, not an exact historical or branded instrument; hidden reed not modeled. No sound, pitch, working airflow, fingering accuracy, tuning, breath pressure, flexible bending, manufacture, playability, handling, equilibrium or safety capability. No rig, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
