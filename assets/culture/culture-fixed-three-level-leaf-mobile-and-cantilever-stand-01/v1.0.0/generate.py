import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='culture-fixed-three-level-leaf-mobile-and-cantilever-stand-01'
TITLE='Fixed Three-Level Leaf Mobile and Cantilever Stand'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeStandCharcoal',(.11,.145,.15,1),.69),('WholeBranchWarmAlloy',(.39,.31,.19,1),.54),('WholeLeafMutedSage',(.25,.43,.36,1),.74),('WholeLeafWarmOchre',(.59,.36,.12,1),.73)]
G={}

def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def prism(name,p,z0,z1,m,transform=None):
 v=[(x,y,z)for z in[z0,z1]for x,y in p];n=len(p);f=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)]
 if transform:v=[transform(q)for q in v]
 record(name,v,f,m)
def rod(name,a,b,r,m,n=8):
 d=[b[i]-a[i]for i in range(3)];le=math.sqrt(sum(t*t for t in d));w=[t/le for t in d];seed=[0,0,1]if abs(w[2])<.9 else[0,1,0]
 u=[w[1]*seed[2]-w[2]*seed[1],w[2]*seed[0]-w[0]*seed[2],w[0]*seed[1]-w[1]*seed[0]];le=math.sqrt(sum(t*t for t in u));u=[t/le for t in u];v=[w[1]*u[2]-w[2]*u[1],w[2]*u[0]-w[0]*u[2],w[0]*u[1]-w[1]*u[0]]
 vs=[tuple(p[k]+r*(u[k]*math.cos(math.tau*i/n)+v[k]*math.sin(math.tau*i/n))for k in range(3))for p in[a,b]for i in range(n)]
 record(name,vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],m)
def lerp(a,b,t):return tuple(a[k]+(b[k]-a[k])*t for k in range(3))
def path_tube(name,path,r,m,n=12):
 v=[]
 for k,p in enumerate(path):
  a=path[max(0,k-1)];b=path[min(len(path)-1,k+1)];dx=b[0]-a[0];dz=b[2]-a[2];le=math.hypot(dx,dz);u=(-dz/le,0,dx/le)
  for j in range(n):v.append(tuple(p[i]+r*(u[i]*math.cos(math.tau*j/n)+(1 if i==1 else 0)*math.sin(math.tau*j/n))for i in range(3)))
 fs=[tuple(reversed(range(n))),tuple((len(path)-1)*n+i for i in range(n))]+[(k*n+i,k*n+(i+1)%n,(k+1)*n+(i+1)%n,(k+1)*n+i)for k in range(len(path)-1)for i in range(n)]
 record(name,v,fs,m)
def make_geometry():
 G.clear();global ATTACHMENTS,LEAF_NAMES;ATTACHMENTS=[];LEAF_NAMES=[]
 # A whole finite elliptical foot and one continuous rounded cantilever, no scene floor.
 p=[(-.12+.50*math.cos(math.tau*i/40),.22*math.sin(math.tau*i/40))for i in range(40)];prism('WholeEllipticalGroundedFoot',p,0,.040,0)
 path=[(-.51,0,.025),(-.51,0,1.26)]+[(-.35-.16*math.cos(math.pi*i/32),0,1.26+.16*math.sin(math.pi*i/32))for i in range(1,17)]+[(.030,0,1.42)]
 path_tube('WholeRoundedCantileverStand',path,.014,0,16);ATTACHMENTS.append(('WholeRoundedCantileverStand','WholeEllipticalGroundedFoot',(-.51,0,.025)))
 # Five full rods form three explicit branching levels, with six complete leaves.
 rods={'Top':((-.20,0,1.22),(.29,.015,1.24)), 'Left':((-.33,-.018,.99),(-.05,.018,.97)), 'Right':((.14,-.04,1.025),(.45,.07,1.015)), 'LowerLeft':((-.15,.030,.680),(.10,.010,.700)), 'LowerRight':((.33,.070,.800),(.55,.030,.760))}
 for key,(a,b)in rods.items():
  d=[b[i]-a[i]for i in range(3)];le=math.sqrt(sum(x*x for x in d));aa=tuple(a[i]-.007*d[i]/le for i in range(3));bb=tuple(b[i]+.007*d[i]/le for i in range(3));rod('WholeBranchRod'+key,aa,bb,.0045,1,12)
 def link(name,a,b,parent,child):
  rod(name,a,b,.0034,1,10);ATTACHMENTS.extend([(name,parent,a),(name,child,b)])
 link('WholeMainSuspension',(.02,0,1.42),lerp(*rods['Top'],.22/.49),'WholeRoundedCantileverStand','WholeBranchRodTop')
 link('WholeLeftSuspension',rods['Top'][0],lerp(*rods['Left'],.13/.28),'WholeBranchRodTop','WholeBranchRodLeft')
 link('WholeRightSuspension',rods['Top'][1],lerp(*rods['Right'],.15/.31),'WholeBranchRodTop','WholeBranchRodRight')
 link('WholeLowerLeftSuspension',rods['Left'][1],lerp(*rods['LowerLeft'],.10/.25),'WholeBranchRodLeft','WholeBranchRodLowerLeft')
 link('WholeLowerRightSuspension',rods['Right'][1],lerp(*rods['LowerRight'],.12/.22),'WholeBranchRodRight','WholeBranchRodLowerRight')
 leaves=[('A','Left',0,.880,.190,.110,-.12,2),('B','LowerLeft',0,.590,.160,.125,.16,3),('C','LowerLeft',1,.570,.220,.140,-.20,2),('D','Right',0,.860,.150,.125,.10,3),('E','LowerRight',0,.650,.170,.125,-.14,2),('F','LowerRight',1,.610,.210,.145,.18,3)]
 for label,key,end,top,height,width,angle,mat in leaves:
  anchor=rods[key][end];cx,cy=anchor[:2];name='WholeThickOrganicLeaf'+label;N=28;v=[]
  # Newly drawn asymmetric ovoid silhouette, broad lower shoulder and pointed top/bottom.
  for dep in[-.004,.004]:
   for j in range(N):
    t=math.tau*j/N;x=.5*width*math.sin(t)*(.85-.15*math.cos(t));z=top-.5*height+.5*height*math.cos(t);v.append((cx+x*math.cos(angle)-dep*math.sin(angle),cy+x*math.sin(angle)+dep*math.cos(angle),z))
  fs=[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(j,(j+1)%N,(j+1)%N+N,j+N)for j in range(N)];record(name,v,fs,mat);LEAF_NAMES.append(name)
  link('WholeLeafSuspension'+label,anchor,(cx,cy,top-.025),'WholeBranchRod'+key,name)
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole suspension sculpture preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.72))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(2.6,-8,3.2));bpy.context.view_layer.update()
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'culture','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored whole fixed leaf-suspension sculpture on its own complete grounded elliptical foot and rounded cantilever stand. Five warm-alloy-look complete rods form three explicit suspension levels and carry six new finite-thickness organic leaf plates in muted sage and ochre. Every suspension wire seats into both its whole parent and child, and the complete stand seats into the finite foot. Intentional fixed intersections, not articulation. Original numerical silhouettes, branching layout, palette and stand; no artist design, branded object, historical replica, reused balance pans or old pendulum mechanism. One model zero scenes, four opaque PBR roles, metre scale and native Z up. Static display appearance only: no dynamic balance, swinging, kinetic behaviour, wind response, structural strength, manufacture, installation, stability or safety capability; no rig, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
