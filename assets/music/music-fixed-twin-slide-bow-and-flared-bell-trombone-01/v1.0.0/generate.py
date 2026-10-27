import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='music-fixed-twin-slide-bow-and-flared-bell-trombone-01'
TITLE='Fixed Twin Slide Bow and Flared Bell Trombone'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeSlideBowAndBellWarmBrass',(.52,.35,.12,1),.43),('WholeInnerSlideAndMouthpieceNickel',(.53,.57,.57,1),.38),('WholeTrueTubeAndBellInteriorDarkBrass',(.28,.15,.050,1),.61),('WholeFixedThreeSeatDisplayCarrierCharcoal',(.070,.10,.11,1),.81)]
G={}
def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)

def rod(name,a,b,r,m,n=8):
 d=[b[i]-a[i]for i in range(3)];le=math.sqrt(sum(t*t for t in d));w=[t/le for t in d];seed=[0,0,1]if abs(w[2])<.9 else[0,1,0]
 u=[w[1]*seed[2]-w[2]*seed[1],w[2]*seed[0]-w[0]*seed[2],w[0]*seed[1]-w[1]*seed[0]];le=math.sqrt(sum(t*t for t in u));u=[t/le for t in u];v=[w[1]*u[2]-w[2]*u[1],w[2]*u[0]-w[0]*u[2],w[0]*u[1]-w[1]*u[0]]
 vs=[tuple(p[k]+r*(u[k]*math.cos(math.tau*i/n)+v[k]*math.sin(math.tau*i/n))for k in range(3))for p in[a,b]for i in range(n)]
 record(name,vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],m)

def union_boxes(name,boxes,m):
 xs=sorted(set(p[0]for b in boxes for p in b));ys=sorted(set(p[1]for b in boxes for p in b));zs=sorted(set(p[2]for b in boxes for p in b));faces={}
 for i in range(len(xs)-1):
  for j in range(len(ys)-1):
   for k in range(len(zs)-1):
    c=((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)
    if not any(all(lo[t]<c[t]<hi[t]for t in range(3))for lo,hi in boxes):continue
    v=[(x,y,z)for z in[zs[k],zs[k+1]]for y in[ys[j],ys[j+1]]for x in[xs[i],xs[i+1]]]
    for f in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:
     q=tuple(v[t]for t in f);key=tuple(sorted(q))
     if key in faces:del faces[key]
     else:faces[key]=q
 verts=[];ix={};fs=[]
 for q in faces.values():
  f=[]
  for p in q:
   if p not in ix:ix[p]=len(verts);verts.append(p)
   f.append(ix[p])
  fs.append(f)
 record(name,verts,fs,m)
def hollow_xy_path(name,stations,outermat,innermat,n=24):
 # One closed finite tube wall; a constant Z frame avoids twist at planar returns.
 v=[];fs=[];mats=[];K=len(stations)
 for k,(p,ro,ri)in enumerate(stations):
  a=stations[max(0,k-1)][0];b=stations[min(K-1,k+1)][0];dx=b[0]-a[0];dy=b[1]-a[1];le=math.hypot(dx,dy);u=(0,0,1);w=(dy/le,-dx/le,0)
  for r in[ro,ri]:
   for j in range(n):
    t=math.tau*j/n;v.append(tuple(p[i]+r*(u[i]*math.cos(t)+w[i]*math.sin(t))for i in range(3)))
 for k in range(K-1):
  for j in range(n):
   q=(j+1)%n;a=k*2*n+j;b=k*2*n+q;c=(k+1)*2*n+j;d=(k+1)*2*n+q
   fs.extend([(a,b,d,c),(a+n,c+n,d+n,b+n)]);mats.extend([outermat,innermat])
 for j in range(n):
  q=(j+1)%n;k=(K-1)*2*n;fs.extend([(q,j,j+n,q+n),(k+j,k+q,k+q+n,k+j+n)]);mats.extend([outermat,outermat])
 record(name,v,fs,mats)
def make_geometry():
 G.clear()
 z=.240
 # Whole long outer slide: two parallel legs joined by an actual hollow U bow.
 path=[(-.140,-.045,z),(.250,-.045,z),(.480,-.045,z)]
 for i in range(1,17):
  a=-math.pi/2+math.pi*i/16;path.append((.480+.045*math.cos(a),.045*math.sin(a),z))
 path +=[(.250,.045,z),(-.140,.045,z)]
 hollow_xy_path('WholeLongOuterTwinSlideAndReturnBow',[(p,.0105,.0085)for p in path],0,2,24)
 for i,(y,start)in enumerate([(-.045,-.380),(.045,-.300)]):hollow_xy_path('WholeExposedInnerSlideTube%d'%i,[((start,y,z),.008,.0055),((.230,y,z),.008,.0055)],1,2,24)
 # Separate whole back return and expanding bell branch, no piston or rotary bank.
 path=[(-.300,.045,z),(-.450,.045,z),(-.550,.045,z)]
 for i in range(1,17):
  a=-math.pi/2-math.pi*i/16;path.append((-.550+.070*math.cos(a),.115+.070*math.sin(a),z))
 stations=[(p,.012,.0095)for p in path]
 stations +=[((x,.185,z),ro,ro-.0035)for x,ro in[(-.480,.012),(-.300,.015),(-.100,.018),(0,.024),(.080,.038),(.130,.058),(.170,.085),(.190,.103),(.198,.105)]]
 hollow_xy_path('WholeRearReturnAndOpenExpandingBell',stations,0,2,40)
 hollow_xy_path('WholeOpenCupAndThroatMouthpiece',[((-.380,-.045,z),.009,.0055),((-.405,-.045,z),.010,.006),((-.425,-.045,z),.017,.012),((-.440,-.045,z),.022,.017),((-.447,-.045,z),.022,.017)],1,1,32)
 for tag,x,r,end in[('Inner',-.270,.0045,.0385),('Outer',-.090,.004,.036)]:rod('Whole'+tag+'SlideHandBrace',(x,-end,z),(x,end,z),r,1,12)
 rod('WholeBellBranchCrossBrace',(-.250,.0515,z),(-.250,.171,z),.005,0,12)
 # Genuine short sleeve collars visibly mark the nested static slide interface.
 for i,y in enumerate([-.045,.045]):hollow_xy_path('WholeOuterSlideMouthCollar%d'%i,[((-.146,y,z),.012,.0103),((-.126,y,z),.012,.0103)],1,1,24)
 # Complete grounded carrier is subordinate, with three finite raised seats.
 boxes=[((-.320,-.100,0),(-.080,.240,.025))]
 for y,top in[(-.045,.233),(.045,.233),(.185,.225)]:boxes.append(((-.214,y-.013,.020),(-.186,y+.013,top)))
 union_boxes('WholeGroundedThreeSeatDisplayCarrier',boxes,3)
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
 make_geometry();d=dict(asset={'version':'2.0','generator':'Original static mesh construction'},scene=0,scenes=[{'name':TITLE,'nodes':[0]}],nodes=[{'name':'AssetRoot__'+ASSET,'children':[]}],meshes=[],materials=[{'name':n,'doubleSided':True,'pbrMetallicRoughness':{'baseColorFactor':c,'metallicFactor':0. if 'Carrier'in n else .67,'roughnessFactor':r}}for n,c,r in PALETTE],accessors=[],bufferViews=[],buffers=[]);blob=bytearray()
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral fixed slide instrument preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.18))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(3.8,-6.2,4.0));bpy.context.view_layer.update()
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete trombone-inspired instrument appearance with its own subordinate three-seat resting carrier. Two long parallel hollow outer slide legs join through one continuous hollow U return bow, surrounding the ends of two thinner visible nickel inner-slide tubes in a fixed partly extended pose. A separate whole rear return branch curves back and expands along a long shoulder into a genuine open flared bell; a whole open cup-and-throat mouthpiece terminates the opposite lead tube. Complete inner and outer slide braces, one bell branch crossbrace and two finite sleeve collars visually connect the instrument. One newly authored grounded carrier supports three tube seats without becoming an additional model. Every numeric route and component shape is new, not old trumpet piston or horn rotary housings removed and rescaled. One model zero scenes, four opaque PBR roles, metres and native Z up. Static stylized exterior category only, not a branded or historical instrument reconstruction, complete acoustic circuit, working slide or tuning system, bore or pitch accuracy, playability, manufacture, handling or safety certification. No valves, rig, animation, sound or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
