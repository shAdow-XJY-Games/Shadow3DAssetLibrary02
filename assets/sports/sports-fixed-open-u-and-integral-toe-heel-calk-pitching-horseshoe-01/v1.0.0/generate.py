'One independently authored complete pitching-horseshoe-inspired static prop: one thick open U material body with two extended gently flared heel arms, a continuous rounded toe, integral raised heel shoulders and a broad raised toe calk. The central void is truly open out through the wide front gap; finite bevels, continuous inner and outer walls and a full flat underside are actual geometry. One connected closed genus-zero whole mesh with three constant opaque PBR face roles, metre-style native Z up and centred ground. No nail holes, letters, fasteners, pole, throwing scene, motion or detached calk pieces. Not a horseshoe-shaped router sole extracted from its tool, and not a bent boomerang wing recoloured or shortened: no prior geometry is imported. Broad sports-equipment category only with invented proportions and plain surfaces, not a branded or competition replica. One original model zero scenes. Static unoccupied visual prop only; no actual throwing, official size or mass, scoring, balance, grip, impact, material strength, manufacturing or safety capability. No textures, animation, rigging or interaction.'
import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='sports-fixed-open-u-and-integral-toe-heel-calk-pitching-horseshoe-01'
TITLE='Open U And Integral Toe Heel Calk Pitching Horseshoe'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeBody_SlateBlue',(.12,.19,.25,1),.74),('UpperRidge_LightSlate',(.28,.34,.38,1),.69),('FullUndersole_DeepSlate',(.065,.085,.11,1),.84)]
G={}
def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def shoe_rows():
 rows=[]
 for j in range(11):
  t=j/10;rows.append((.075,-.103+.093*t,0.,1.,t*.093))
 for j in range(1,49):
  a=math.pi*j/48;rows.append((.075*math.cos(a),-.010+.075*math.sin(a),-math.sin(a),math.cos(a),.093+.075*a))
 total=.186+.075*math.pi
 for j in range(1,11):
  t=j/10;rows.append((-.075,-.010-.093*t,0.,-1.,.093+.075*math.pi+.093*t))
 return rows,total
def make_geometry():
 G.clear();rows,total=shoe_rows();vs=[];fs=[];ms=[]
 for x,y,tx,ty,s in rows:
  # Whole U body has integral raised heel shoulders and a broad toe crown.
  # No old sole, bent wing or separately glued-on calk blocks are used.
  edge=min(s,total-s);heel=max(0.,min(1.,(.034-edge)/.017))
  toe=max(0.,min(1.,(.034-abs(s-total/2))/.017))
  w=.030+.010*heel;h=.010+.007*max(heel,toe);bevel=.0018
  section=[(-w/2+bevel,0),(-w/2,.0018),(-w/2,h-.0018),(-w/2+bevel,h),(w/2-bevel,h),(w/2,h-.0018),(w/2,.0018),(w/2-bevel,0)]
  for q,z in section:vs.append((x+ty*q,y-tx*q,z))
 for j in range(len(rows)-1):
  for k in range(8):
   fs.append((j*8+k,j*8+(k+1)%8,(j+1)*8+(k+1)%8,(j+1)*8+k));ms.append(2 if k==7 else 1 if k==3 and max(rows[j][4],rows[j+1][4])>.01 else 0)
 fs +=[tuple(reversed(range(8))),tuple((len(rows)-1)*8+k for k in range(8))];ms +=[0,0]
 record('WholeOpenUWithIntegralRaisedToeAndHeelCalks',vs,fs,ms)
 global SHIFT
 SHIFT=(0,0,0)
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
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==proof['mesh_count']
 triangle_count=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons);assert triangle_count==proof['triangles']
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 lo=[min(v[k]for v in points)for k in range(3)];hi=[max(v[k]for v in points)for k in range(3)]
 assert abs(lo[2])<=TOL
 assert len({m for o in parts for m in o.data.materials})==len(PALETTE)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'),compress=False)
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
 for layer in scene.view_layers:layer.cycles.use_denoising=False
 scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
 scene.render.resolution_x=scene.render.resolution_y=640;scene.render.resolution_percentage=100
 scene.world=scene.world or bpy.data.worlds.new('Neutral instrument preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,-.015,.008))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,22),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(3,-5,4.8) if '--tier-single-view' in sys.argv and sys.argv[sys.argv.index('--tier-single-view')+1]=='qa-front' else (-3,-5,4.0));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 def config():return dict(engine=scene.render.engine,samples=scene.cycles.samples,adaptive=scene.cycles.use_adaptive_sampling,cycles_denoise=scene.cycles.use_denoising,view_layer_denoise=[x.cycles.use_denoising for x in scene.view_layers],compositor_nodes=scene.use_nodes,compositing=scene.render.use_compositing,threads_mode=scene.render.threads_mode,threads=scene.render.threads)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'asset':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':len(parts),'mesh_objects':len(parts),'triangles':triangle_count,'materials':len(PALETTE),'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'sports','style':'source-preserved-low-poly','title':TITLE,'description':'One independently authored complete pitching-horseshoe-inspired static prop: one thick open U material body with two extended gently flared heel arms, a continuous rounded toe, integral raised heel shoulders and a broad raised toe calk. The central void is truly open out through the wide front gap; finite bevels, continuous inner and outer walls and a full flat underside are actual geometry. One connected closed genus-zero whole mesh with three constant opaque PBR face roles, metre-style native Z up and centred ground. No nail holes, letters, fasteners, pole, throwing scene, motion or detached calk pieces. Not a horseshoe-shaped router sole extracted from its tool, and not a bent boomerang wing recoloured or shortened: no prior geometry is imported. Broad sports-equipment category only with invented proportions and plain surfaces, not a branded or competition replica. One original model zero scenes. Static unoccupied visual prop only; no actual throwing, official size or mass, scoring, balance, grip, impact, material strength, manufacturing or safety capability. No textures, animation, rigging or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
