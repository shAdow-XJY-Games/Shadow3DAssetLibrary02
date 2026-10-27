import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='culture-fixed-domed-drum-and-chain-weight-handwheel-01'
TITLE='Fixed Domed Drum and Chain Weight Handwheel'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeLongGripWarmWood',(.28,.12,.037,1),.72),('WholeUninscribedDrumBronze',(.35,.19,.08,1),.50),('WholePlainRimSpindleAndWeightBrass',(.47,.34,.14,1),.43),('WholeClosedLinksDarkMetal',(.16,.19,.18,1),.49)]
G={}

def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def radial(name,profile,mat,N=40,origin=(0,0,0),axis=(0,0,1),u=(1,0,0)):
 v=(axis[1]*u[2]-axis[2]*u[1],axis[2]*u[0]-axis[0]*u[2],axis[0]*u[1]-axis[1]*u[0]);points=[];rows=[];fs=[];ms=[]
 for t,r in profile:
  ids=[]
  if r==0:ids=[len(points)];points.append(tuple(origin[k]+axis[k]*t for k in range(3)))
  else:
   for i in range(N):
    a=math.tau*i/N;ids.append(len(points));points.append(tuple(origin[k]+axis[k]*t+r*(u[k]*math.cos(a)+v[k]*math.sin(a))for k in range(3)))
  rows.append(ids)
 for j,(a,b)in enumerate(zip(rows,rows[1:]+rows[:1])):
  if len(a)==len(b)==1:continue
  for i in range(N):
   q=(i+1)%N;fs.append((a[0],b[q],b[i])if len(a)==1 else(a[i],a[q],b[0])if len(b)==1 else(a[i],a[q],b[q],b[i]));ms.append(mat[j]if isinstance(mat,list)else mat)
 record(name,points,fs,ms)
def make_geometry():
 G.clear();radial('WholeLongTurnedWoodHandle',[(0,0),(0,.013),(.008,.016),(.028,.016),(.135,.012),(.172,.010),(.190,.010),(.190,0)],0,32)
 radial('WholeFixedAxialSpindleAndLowerCollar',[(.173,0),(.173,.005),(.194,.005),(.194,.020),(.201,.020),(.201,.005),(.277,.005),(.277,0)],2,32)
 profile=[(.205,0),(.205,.044),(.210,.049),(.217,.049),(.220,.047),(.292,.047),(.296,.051),(.303,.051),(.307,.047),(.318,.038),(.330,.020),(.338,.006),(.344,.006),(.344,0)];m=[2,2,2,2,1,1,2,2,1,1,1,2,2,2];radial('WholePlainCylindricalCaseAndDomedLidExterior',profile,m,48)
 global CHAIN_CENTRES,CHAIN_AXIS,WEIGHT_ROOT
 axis=(.8,0,-.6);v0=(0,1,0);v1=(.6,0,.8);centres=[(.051+j*.0145*axis[0],0,.260+j*.0145*axis[2])for j in range(6)]
 for j,c in enumerate(centres):
  side=v0 if j%2==0 else v1;normal=(axis[1]*side[2]-axis[2]*side[1],axis[2]*side[0]-axis[0]*side[2],axis[0]*side[1]-axis[1]*side[0]);N=32;Q=10;v=[]
  for i in range(N):
   a=math.tau*i/N;curve=tuple(c[k]+.008*math.cos(a)*axis[k]+.0042*math.sin(a)*side[k]for k in range(3));tangent=tuple(-.008*math.sin(a)*axis[k]+.0042*math.cos(a)*side[k]for k in range(3));le=math.sqrt(sum(x*x for x in tangent));tangent=tuple(x/le for x in tangent);outward=(tangent[1]*normal[2]-tangent[2]*normal[1],tangent[2]*normal[0]-tangent[0]*normal[2],tangent[0]*normal[1]-tangent[1]*normal[0])
   for q in range(Q):b=math.tau*q/Q;v.append(tuple(curve[k]+.0012*(outward[k]*math.cos(b)+normal[k]*math.sin(b))for k in range(3)))
  f=[(i*Q+q,((i+1)%N)*Q+q,((i+1)%N)*Q+(q+1)%Q,i*Q+(q+1)%Q)for i in range(N)for q in range(Q)];record('WholeClosedTetherLink_'+str(j),v,f,3)
 root=tuple(centres[-1][k]+.008*axis[k]for k in range(3));radial_fn=globals()['radial'];radial_fn('WholeTerminalNeckAndRoundedWeight',[(-.001,0),(-.001,.0022),(.003,.0022),(.008,.0065),(.017,.008),(.025,.005),(.029,.002),(.029,0)],2,24,root,axis,(0,1,0))
 CHAIN_CENTRES=centres;CHAIN_AXIS=axis;WEIGHT_ROOT=root
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
 make_geometry();d=dict(asset={'version':'2.0','generator':'Original static mesh construction'},scene=0,scenes=[{'name':TITLE,'nodes':[0]}],nodes=[{'name':'AssetRoot__'+ASSET,'children':[]}],meshes=[],materials=[{'name':n,'doubleSided':True,'pbrMetallicRoughness':{'baseColorFactor':c,'metallicFactor':(.5 if n!='WholeLongGripWarmWood' else 0.),'roughnessFactor':r}}for n,c,r in PALETTE],accessors=[],bufferViews=[],buffers=[]);blob=bytearray()
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral uninscribed whole handwheel display');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.172))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(2.7,-7.0,3.8));bpy.context.view_layer.update()
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
  if p.exists():files[role]={'path':f'assets/culture/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'culture','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete static uninscribed prayer-wheel-inspired exterior. A whole long turned wooden-look handle carries a single axial spindle and broad lower collar beneath one full cylindrical case with an integrated domed-lid exterior and plain narrow rim bands. Six separate complete closed oval links form one short alternating-plane side tether ending in one full neck-and-rounded-weight body. All link holes are genuine open space; small intentional overlaps root neighboring links in this fixed pose. Every numeric profile, loop path, placement and weight shape is new, not a cabasa cylinder with bead loops removed, a shallow pellet rattle case, a spinning top or an extracted chain accessory. The complete handle butt is the finite ground datum; ten closed editable components and four opaque PBR roles, metres native Z up, one model zero scenes. Broad category inspiration acknowledges Tibetan Buddhist prayer wheels, but this plain decorative exterior omits sacred inscriptions, icons, scrolls and internal drum cavity, and does not reproduce a particular museum object, regional ornament, historical form, material identity or ritual authenticity. The cylinder is an opaque closed display solid, not an accessible vessel. No prayer efficacy, ceremonial instruction, spinning, bearing clearance, chain articulation, dynamic suspension, balance, manufacture, hand fit, strength or safety capability made or verified. No rig, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
