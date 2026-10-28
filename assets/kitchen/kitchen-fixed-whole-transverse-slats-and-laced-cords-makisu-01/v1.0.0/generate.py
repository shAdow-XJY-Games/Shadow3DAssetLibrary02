import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='kitchen-fixed-whole-transverse-slats-and-laced-cords-makisu-01'
TITLE='Fixed Whole Transverse Slats and Laced Cords Makisu'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeBambooSlatUpperHoney',(.53,.35,.14,1),.73),('WholeSlatCutEndsPaleBamboo',(.65,.49,.27,1),.84),('WholeContinuousLacingFlax',(.72,.63,.45,1),.90),('WholeBambooSlatUnderside',(.36,.23,.095,1),.79)]
G={}

def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
SLAT_S=[.009*j for j in range(24)]
LACING_X=[-.081,-.027,.027,.081]
def mat_frame(s):
 if s<=.117:return(s-.105,.003,0.)
 a=(s-.117)/.045;return(.012+.045*math.sin(a),.003+.045*(1-math.cos(a)),a)
def mapped(x,s,h):
 y,z,a=mat_frame(s);return(x,y-math.sin(a)*h,z+math.cos(a)*h)
def slat(name,s):
 y,z,a=mat_frame(s);section=[(-.0036,-.0014),(.0036,-.0014),(.0040,-.0008),(.0033,.0010),(.0020,.0018),(-.0020,.0018),(-.0033,.0010),(-.0040,-.0008)];v=[]
 for x,scale in[(-.112,.83),(-.110,1),(.110,1),(.112,.83)]:
  for u,h in section:v.append((x,y+scale*(math.cos(a)*u-math.sin(a)*h),z+scale*(math.sin(a)*u+math.cos(a)*h)))
 f=[tuple(reversed(range(8))),tuple(24+i for i in range(8))];m=[1,1]
 for j in range(3):
  for i in range(8):f.append((j*8+i,j*8+(i+1)%8,(j+1)*8+(i+1)%8,(j+1)*8+i));m.append(3 if i==0 else 0)
 record(name,v,f,m)
def lacing_path(x):
 routes=[]
 for side in[-1,1]:
  p=[]
  for j,s in enumerate(SLAT_S):
   h=.0023 if (j+(side==1))%2==0 else-.0019
   if j==0:p.append(mapped(x+side*.001,-.006,h))
   p.extend(mapped(x+side*.001,s+u,h)for u in[-.0024,0,.0024])
   if j<23:p.append(mapped(x+side*.001,s+.0045,.0002))
   else:p.append(mapped(x+side*.001,s+.006,h))
  routes.append(p)
 return routes[0]+list(reversed(routes[1]))
def closed_cord(name,path):
 N=8;r=.00065;v=[]
 for j,p in enumerate(path):
  a=path[j-1];b=path[(j+1)%len(path)];w=[b[k]-a[k]for k in range(3)];le=math.sqrt(sum(q*q for q in w));w=[q/le for q in w];u=[1-w[0]*w[0],-w[0]*w[1],-w[0]*w[2]];le=math.sqrt(sum(q*q for q in u));assert le>1e-8;u=[q/le for q in u];vv=[w[1]*u[2]-w[2]*u[1],w[2]*u[0]-w[0]*u[2],w[0]*u[1]-w[1]*u[0]]
  for i in range(N):
   a=math.tau*i/N;v.append(tuple(p[k]+r*(u[k]*math.cos(a)+vv[k]*math.sin(a))for k in range(3)))
 # The low fixed cord skin has a deliberately finite flattened resting facet.
 v=[(x,y,max(z,.00075))for x,y,z in v]
 f=[(j*N+i,j*N+(i+1)%N,((j+1)%len(path))*N+(i+1)%N,((j+1)%len(path))*N+i)for j in range(len(path))for i in range(N)];record(name,v,f,2)
def make_geometry():
 G.clear()
 for j,s in enumerate(SLAT_S):slat('WholeBevelEndedTransverseBambooSlat_%02d'%j,s)
 for j,x in enumerate(LACING_X):closed_cord('WholeReturningOverUnderLacingCircuit_%02d'%j,lacing_path(x))
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole laced bamboo mat preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.030))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(4.2,-6.4,6.5));bpy.context.view_layer.update()
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
  if p.exists():files[role]={'path':f'assets/kitchen/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'kitchen','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete empty makisu-inspired bamboo rolling-mat appearance in one fixed partly curled pose. Twenty-four whole long transverse slats have finite flattened lower faces, curved bevelled upper sections and complete bevelled cut ends. Four entire closed lacing circuits each form two uninterrupted narrow opposite-phase over-under routes along all slats, returning at both ends. The broad front portion lies low while the rear slat sequence rises into an open inward curl; real narrow air intervals remain between the slats and no filled sheet replaces the bamboo field. All slat cross-sections, stations, curled centre route and complete lacing paths are original numerical geometry. Unlike the long agility ladder with widely spaced slotted rungs and two broad straps passing inside the rung holes, these unperforated close-set full-width rods are externally encircled by returning alternating narrow cords. Unlike the elevated one-sided warp loom there is no supporting side frame, cantilever pegs, winding polygon, heddle or separate working thread span. Twenty-eight complete closed editable meshes, four opaque constant untextured PBR roles, metres native Z up and horizontal whole-bounds-centred ground datum. One whole independent model zero scenes; the slats and laces are not separately counted. Ground contact is through finite lower cord facets; all slats have explicit small static lacing contacts. Category-level artistic exterior only, not a measured museum or branded product, and not a claim of exact traditional knot or weaving topology. The compact fixed return circuits are a simplified visual binding, not a manufactured textile fastening specification. No sushi, other food, hand, film, water or cookware included. No rolling range, flexibility, cord tension, food preparation, food-contact suitability, hygiene, material species, fibre construction, grasp, load, stability, manufacture or safety capability made or verified. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
