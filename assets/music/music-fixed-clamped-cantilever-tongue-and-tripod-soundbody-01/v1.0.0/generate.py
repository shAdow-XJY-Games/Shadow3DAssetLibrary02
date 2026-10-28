import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='music-fixed-clamped-cantilever-tongue-and-tripod-soundbody-01'
TITLE='Fixed Clamped Cantilever Tongue and Tripod Soundbody'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeSingleWoodTongueHoney',(.58,.32,.115,1),.70),('WholeSoundbodyClampAndTripodWalnut',(.18,.085,.033,1),.75),('WholeFixedClampSpindlesSatinMetal',(.26,.29,.27,1),.46),('WholeThreeFiniteFeetDarkMatte',(.055,.065,.065,1),.87)]
G={}

def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def loc(p):
 x,y,z=p;c=math.cos(math.pi/6);s=math.sin(math.pi/6);return(x,y*c-z*s,.550+y*s+z*c)
def polytris(p):
 ids=list(range(len(p)));ts=[]
 def cr(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:ids.reverse()
 while len(ids)>3:
  for k,b in enumerate(ids):
   a,c=ids[k-1],ids[(k+1)%len(ids)]
   if cr(p[a],p[b],p[c])<=1e-13:continue
   if any(min(cr(p[a],p[b],p[j]),cr(p[b],p[c],p[j]),cr(p[c],p[a],p[j]))>=-1e-13 for j in ids if j not in[a,b,c]):continue
   ts.append((a,b,c));ids.pop(k);break
  else:raise AssertionError('invalid new polygon')
 return ts+[tuple(ids)]
def prism(name,p,z0,z1,mat,tilt=True):
 n=len(p);v=[(x,y,z)for z in[z0,z1]for x,y in p];f=[]
 for a,b,c in polytris(p):f.extend([(c,b,a),(a+n,b+n,c+n)])
 for i in range(n):j=(i+1)%n;f.append((i,j,n+j,n+i))
 record(name,[loc(p)for p in v]if tilt else v,f,mat)
def ringpoints(x0,x1,y0,y1,b):return[(x0+b,y0),(x1-b,y0),(x1,y0+b),(x1,y1-b),(x1-b,y1),(x0+b,y1),(x0,y1-b),(x0,y0+b)]
def soundbody():
 outer=ringpoints(-.065,.065,-.055,.100,.012);inner=ringpoints(-.055,.055,-.045,.090,.008);v=[];rows=[]
 for p,z in[(outer,-.045),(outer,0),([(0,.0225)],0),([(0,.0225)],-.007),(inner,-.007),(inner,-.045)]:
  row=[]
  for x,y in p:row.append(len(v));v.append(loc((x,y,z)))
  rows.append(row)
 f=[]
 for a,b in zip(rows,rows[1:]+rows[:1]):
  if len(a)==len(b)==1:continue
  for i in range(8):
   j=(i+1)%8
   if len(a)==1:f.append((a[0],b[j],b[i]))
   elif len(b)==1:f.append((a[i],a[j],b[0]))
   else:f.append((a[i],a[j],b[j],b[i]))
 record('WholeTiltedOpenUndersideSoundbody',v,f,1)
def bolt(name,x):
 profile=[(0,-.013),(.004,-.013),(.004,.025),(.009,.025),(.009,.036),(0,.036)];v=[];rows=[];f=[];N=8
 for r,z in profile:
  row=[]
  for j in range(N if r else 1):row.append(len(v));v.append(loc((x+r*math.cos(math.tau*j/N),.012+r*math.sin(math.tau*j/N),z)))
  rows.append(row)
 for a,b in zip(rows,rows[1:]+rows[:1]):
  if len(a)==len(b)==1:continue
  for i in range(N):
   j=(i+1)%N
   if len(a)==1:f.append((a[0],b[j],b[i]))
   elif len(b)==1:f.append((a[i],a[j],b[0]))
   else:f.append((a[i],a[j],b[j],b[i]))
 record(name,v,f,2)
def beam(name,a,b):
 d=[b[i]-a[i]for i in range(3)];le=math.sqrt(sum(x*x for x in d));w=[x/le for x in d];u=[-w[1],w[0],0];le=math.hypot(*u[:2]);u=[x/le for x in u];v=[w[1]*u[2]-w[2]*u[1],w[2]*u[0]-w[0]*u[2],w[0]*u[1]-w[1]*u[0]]
 pts=[tuple(p[i]+.012*(sx*u[i]+sy*v[i])for i in range(3))for p in[a,b]for sy in[-1,1]for sx in[-1,1]];record(name,pts,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],1)
def make_geometry():
 G.clear();soundbody()
 tongue=[(-.018,.035),(-.018,-.035),(-.012,-.115),(-.025,-.205),(-.027,-.265),(-.019,-.287),(.006,-.296),(.023,-.280),(.027,-.230),(.019,-.175),(.012,-.115),(.018,-.035),(.018,.035)]
 prism('WholeSingleWaistedCantileverWoodTongue',tongue,-.001,.004,0)
 prism('WholeTransverseTongueClampBar',ringpoints(-.042,.042,-.003,.027,.004),.003,.020,1)
 for x,n in[(-.030,'Left'),(.030,'Right')]:bolt('Whole'+n+'ClampSpindleAndOctagonalHead',x)
 for j,(x,y,root)in enumerate([(-.190,-.200,(-.060,-.030,-.025)),(.190,-.200,(.060,-.030,-.025)),(0,.230,(0,.095,-.025))]):
  beam('WholeSplayedTripodLeg_%d'%j,(x,y,.010),loc(root));prism('WholeFiniteGroundFoot_%d'%j,ringpoints(x-.030,x+.030,y-.035,y+.035,.005),0,.020,3,False)
 pts=[p for v,f,m in G.values()for p in v];lo=[min(p[k]for p in pts)for k in range(3)];hi=[max(p[k]for p in pts)for k in range(3)]
 global SHIFT
 SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2])
 for n,(v,f,m)in list(G.items()):G[n]=([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)
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
 d['materials'][2]['pbrMetallicRoughness']['metallicFactor']=.50
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole clamped tongue tripod preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.29))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(4.4,-6,3.8));bpy.context.view_layer.update()
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete fixed unbowed daxophone-inspired instrument-body display. A whole thick chamfered wooden soundbody has a genuinely open underside recess and a full thin upper board held at an inclined angle. One entire thin asymmetric waisted wooden tongue is rooted over that upper board under a full transverse clamp bar; two complete side spindles with integral plain octagonal heads flank the tongue. The long free tongue projects beyond the body into unobstructed space. Three separate full splayed timber legs meet the soundbody wall margins and three complete finite ground feet. Unlike the seven short metal keys laid over a hollow handheld kalimba roof, this wide single wooden tongue reaches far outside a narrow inclined soundbody above its own full tripod. Unlike the small metal jaw harp, there is no surrounding return frame or pair of guiding arms around the tongue. The entire clamp, inclined support body and free cantilever relation is newly authored together, not an extracted old tine or a changed tine-count variation. Eleven closed whole component meshes, four opaque constant untextured PBR roles, metres native Z up and whole horizontal-bounds-centred origin at the three ground feet. One model zero scenes; parts are not separately counted. Plain category-inspired static exterior, not any maker product, measured historical design, distinctive tongue alphabet or instrument plan. No bow, separate dax block, amplifier, cable or internal pickup is supplied or claimed. No playing, actual vibration, acoustic response, electrical output, pitch control, tuned shape, clamping motion, threaded fit, balance, load, manufacture, installation or use-safety capability made or verified. No rigging animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
