import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='art-fixed-crosshatched-roller-and-bent-neck-texturing-tool-01'
TITLE='Fixed Crosshatched Roller and Bent Neck Texturing Tool'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholePearGripWarmWood',(.36,.17,.060,1),.68),('WholeGripEndWood',(.23,.09,.025,1),.76),('WholeIntegralReliefRollerSilver',(.44,.49,.48,1),.42),('WholeBentNeckCollarAndAxleCap',(.17,.21,.21,1),.46)]
G={}

def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def make_geometry():
 G.clear();N=24;phase=-math.pi/2+math.pi/N;cz=.014*math.cos(math.pi/N)
 stations=[(.013,.0068),(.027,.0075),(.045,.0100),(.072,.014),(.100,.014),(.124,.011),(.139,.006)]
 v=[(r*math.cos(phase+math.tau*i/N),y,cz+r*math.sin(phase+math.tau*i/N))for y,r in stations for i in range(N)];f=[tuple(reversed(range(N))),tuple((len(stations)-1)*N+i for i in range(N))]+[(k*N+i,k*N+(i+1)%N,(k+1)*N+(i+1)%N,(k+1)*N+i)for k in range(len(stations)-1)for i in range(N)];record('WholeCompletePearWoodGrip',v,f,[1,1]+[0]*(len(f)-2))
 v=[(r*math.cos(phase+math.tau*i/N),y,cz+r*math.sin(phase+math.tau*i/N))for y,r in[(.007,.0063),(.007,.0084),(.027,.0084),(.027,.0063)]for i in range(N)];f=[(k*N+i,k*N+(i+1)%N,((k+1)%4)*N+(i+1)%N,((k+1)%4)*N+i)for k in range(4)for i in range(N)];record('WholeAnnularNeckCollar',v,f,3)
 path=[(0,.038),(0,.005),(-.002,-.010),(-.007,-.023),(-.014,-.036),(-.016,-.043),(-.015,-.049),(-.010,-.052),(-.004,-.052),(.014,-.052)];N=20;v=[]
 for k,(x,y)in enumerate(path):
  a=path[max(k-1,0)];b=path[min(len(path)-1,k+1)];dx,dy=b[0]-a[0],b[1]-a[1];le=math.hypot(dx,dy);u=(-dy/le,dx/le)
  for i in range(N):t=math.tau*i/N;v.append((x+.0023*u[0]*math.cos(t),y+.0023*u[1]*math.cos(t),cz+.0023*math.sin(t)))
 f=[tuple(reversed(range(N))),tuple((len(path)-1)*N+i for i in range(N))]+[(k*N+i,k*N+(i+1)%N,(k+1)*N+(i+1)%N,(k+1)*N+i)for k in range(len(path)-1)for i in range(N)];record('WholeContinuousBentNeckAndTransverseAxle',v,f,3)
 # Integral radial relief: two crossing families of true recessed diagonal grooves, no texture map and no detached teeth.
 N=64;K=24;v=[]
 for j in range(K+1):
  u=j/K;x=-.009+.018*u
  for i in range(N):
   t=i/N;relief=min(abs(math.sin(math.pi*(6*u+16*t))),abs(math.sin(math.pi*(6*u-16*t))));r=.0097+.0015*relief;a=math.tau*t+math.pi/N;v.append((x,-.052+r*math.cos(a),cz+r*math.sin(a)))
 f=[]
 for j in range(K):
  for i in range(N):q=(i+1)%N;f.append((j*N+i,j*N+q,(j+1)*N+q,(j+1)*N+i))
 off=len(v)
 for x in[-.009,.009]:
  for i in range(N):a=math.tau*i/N+math.pi/N;v.append((x,-.052+.0021*math.cos(a),cz+.0021*math.sin(a)))
 for i in range(N):
  q=(i+1)%N;f.extend([(i,off+i,off+q,q),(K*N+i,K*N+q,off+N+q,off+N+i),(off+i,off+N+i,off+N+q,off+q)])
 record('WholeThroughBoredCrosshatchedReliefDrum',v,f,2)
 N=24;v=[(x,-.052+r*math.cos(math.tau*i/N),cz+r*math.sin(math.tau*i/N))for x,r in[(.0105,.0040),(.0145,.0040),(.0155,.0028)]for i in range(N)];f=[tuple(reversed(range(N))),tuple(2*N+i for i in range(N))]+[(k*N+i,k*N+(i+1)%N,(k+1)*N+(i+1)%N,(k+1)*N+i)for k in range(2)for i in range(N)];record('WholeRetainingEndCap',v,f,3)
 pts=[p for v,f,m in G.values()for p in v];lo=[min(p[k]for p in pts)for k in range(3)];hi=[max(p[k]for p in pts)for k in range(3)]
 global SHIFT,CZ
 CZ=cz;SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2])
 for name,(v,f,m)in list(G.items()):G[name]=([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)
 return G

def pack_glb(doc,blob):
 j=json.dumps(doc,separators=(',',':'),allow_nan=False).encode();j+=b' '*((-len(j))%4)
 b=bytes(blob)+b'\0'*((-len(blob))%4)
 return struct.pack('<4sII',b'glTF',2,12+8+len(j)+8+len(b))+struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(b),0x004e4942)+b
def compose(inputs):
 make_geometry();d=dict(asset={'version':'2.0','generator':'Original static mesh construction'},scene=0,scenes=[{'name':TITLE,'nodes':[0]}],nodes=[{'name':'AssetRoot__'+ASSET,'children':[]}],meshes=[],materials=[{'name':n,'doubleSided':True,'pbrMetallicRoughness':{'baseColorFactor':c,'metallicFactor':(.55 if n in ['WholeIntegralReliefRollerSilver','WholeBentNeckCollarAndAxleCap'] else 0.),'roughnessFactor':r}}for n,c,r in PALETTE],accessors=[],bufferViews=[],buffers=[]);blob=bytearray()
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole roulette texturing-tool preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.014))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(3.2,-4.2,6.0));bpy.context.view_layer.update()
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'art','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete static printmaking-roulette-inspired tool. One small broad cylindrical drum has real integral coarse diamond-like relief formed by two crossing families of recessed diagonal grooves around its whole circumference, full annular end walls and a genuine through axle bore. A single continuous bent metal-look neck becomes the transverse axle, enters a whole pear-shaped long wooden grip and carries a complete retaining end cap; one full annular collar covers the grip root. The entire grip rests on its original finite lower facet while the textured head remains slightly raised. Every profile, groove field, neck bend and coordinate is new, not an old paint-roller sleeve reduced in size or a brayer fork removed. Unlike those plain long coating rollers, the characteristic component here is an integral deeply relieved short cylindrical texturing drum; it is not a thin toothed tracing/pounce disc or a broad serrated rocker plate. Five closed editable bodies, four constant opaque PBR roles, metres native Z up, one model zero scenes. Generic category appearance only, no maker marks or copied dimensions. Coarse relief is a visual convention, not a usable tooth grade; static small shaft/bore overlaps are intentional attachment, not rotating bearing clearance. No paper, ink, metal plate, actual rolling, engraving, scoring, pressure, print result, tooling sharpness, manufacturing, ergonomic or safety capability made or verified. No rig, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
