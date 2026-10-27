import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='music-fixed-open-neck-and-round-side-port-clay-vessel-01'
TITLE='Fixed Open Neck and Round Side Port Clay Vessel'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeClayVesselTerracotta',(.42,.16,.070,1),.82),('WholeClayVesselInnerAndPortWall',(.18,.070,.033,1),.89),('WholeClayVesselNeckGlaze',(.045,.19,.18,1),.38),('WholeClayVesselLowFootBand',(.18,.090,.045,1),.86)]
G={}

def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def make_geometry():
 G.clear()
 # New whole clay chamber with two connected air openings, not a sphere with decals.
 zs=[0,.015,.045,.085,.105,.135,.165,.195,.225,.255,.28,.30,.36,.38]
 rs=[.060,.075,.105,.132,.140,.142,.140,.128,.108,.075,.044,.035,.033,.040]
 theta=-math.pi/2;angles=[theta-.48+.24*i for i in range(5)]+[theta+.48+(math.tau-.96)*i/44 for i in range(1,44)];N=len(angles);K=len(zs);v=[];fs=[];mats=[]
 for inner in [False,True]:
  for k,(z,r)in enumerate(zip(zs,rs)):
   rr=r-(.009 if inner else 0);zz=.010 if inner and k==0 else z
   v.extend((rr*math.cos(a),rr*math.sin(a),zz)for a in angles)
 def idx(inner,k,i):return (K*N if inner else 0)+k*N+(i%N)
 def face(f,m):fs.append(f);mats.append(m)
 for inner in [False,True]:
  for k in range(K-1):
   for i in range(N):
    if 4<=k<8 and 0<=i<4:continue
    f=[idx(inner,k,i),idx(inner,k,i+1),idx(inner,k+1,i+1),idx(inner,k+1,i)]
    face(list(reversed(f))if inner else f,1 if inner else (3 if k<2 else 2 if k>=10 else 0))
 # A 4x4-cell patch is retopologized into a true sixteen-sided side aperture.
 boundary=[(4,i)for i in range(5)]+[(k,4)for k in range(5,9)]+[(8,i)for i in range(3,-1,-1)]+[(k,0)for k in range(7,4,-1)]
 def radius(z):
  for k in range(K-1):
   if zs[k]<=z<=zs[k+1]:return rs[k]+(rs[k+1]-rs[k])*(z-zs[k])/(zs[k+1]-zs[k])
  raise ValueError(z)
 holes=[]
 for inner in [False,True]:
  row=[]
  for k,i in boundary:
   a=math.atan2((zs[k]-.165)/.060,(angles[i]-theta)/.48);t=theta+.48*.62*math.cos(a);z=.165+.060*.70*math.sin(a);r=radius(z)-(.009 if inner else 0)
   row.append(len(v));v.append((r*math.cos(t),r*math.sin(t),z))
  holes.append(row)
  for q,(k,i)in enumerate(boundary):
   j=(q+1)%len(boundary);kk,ii=boundary[j];f=[idx(inner,k,i),idx(inner,kk,ii),row[j],row[q]]
   face(list(reversed(f))if inner else f,1 if inner else 0)
 for q in range(len(boundary)):
  j=(q+1)%len(boundary);face([holes[0][q],holes[0][j],holes[1][j],holes[1][q]],1)
 outerbottom=len(v);v.append((0,0,0));innerbottom=len(v);v.append((0,0,.010))
 for i in range(N):
  j=(i+1)%N
  face([outerbottom,idx(False,0,j),idx(False,0,i)],3)
  face([innerbottom,idx(True,0,i),idx(True,0,j)],1)
  face([idx(False,K-1,i),idx(False,K-1,j),idx(True,K-1,j),idx(True,K-1,i)],2)
 record('WholeContinuousOpenNeckSidePortClayChamber',v,fs,mats)
 pts=[v[i] for v,f,m in G.values()for face in f for i in face];lo=[min(p[k]for p in pts)for k in range(3)];hi=[max(p[k]for p in pts)for k in range(3)]
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral clay vessel preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.19))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(2.6,-7,3.5));bpy.context.view_layer.update()
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete static clay-vessel-drum-inspired appearance. A continuous finite-thickness terracotta chamber expands from its own flat basal footprint to a broad low belly and contracts through a long shoulder to a narrow open glazed neck. One true sixteen-sided round side port passes through the same wall into the same hollow interior; both apertures are actual geometry, not black discs. Interior and port walls are continuous with the outer ceramic skin through both rims. A dark low foot band and teal upper-neck glaze are material regions on that same closed connected shell, not floating ornaments. All numeric geometry is newly authored as a whole: no kettle spout, handle or lid, no six-fingerhole flute, and no beaded gourd net. One model zero scenes, four opaque PBR regions, metres and native Z up. Static stylized category inspiration only; no copied branded shape, labels, regional or historical reconstruction, actual acoustic response, playability, fabrication, leak-tightness, handling or safety capability. No rig, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
