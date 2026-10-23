'One newly authored complete fixed open-truss reflector-style telescope display. A closed-back square mirror box opens into eight long exposed diagonal truss rods and a short hollow front cage carrying four thin spider members, a small diagonal secondary-style disc and a side eyepiece tube. Two large side bearing discs seat into matching concave rocker cheeks on a broad circular ground base. The main body has a genuinely open long span, not the old closed-cylinder tripod telescope recolored or resized; the complete ground-rocker support differs from the counterweighted equatorial stand. All parts form one fixed whole prop. Intentional finite overlaps fix static joints; no rotation range, balancing, optical prescription, focus, tracking, alignment, telescope compatibility, historical accuracy, engineering or safety claim.'
import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='astronomy-fixed-truss-reflector-rocker-01'
TITLE='Fixed Open-Truss Reflector and Rocker'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('DarkTealMirrorBox', [0.06, 0.19, 0.2, 1], 0.67), ('PaleBirchRocker', [0.59, 0.43, 0.25, 1], 0.76), ('GraphiteTrussAndBearings', [0.1, 0.13, 0.15, 1], 0.54), ('BlueGreyOpticalDisplayDiscs', [0.26, 0.39, 0.44, 1], 0.37)]
G={}
def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def rect(x,y0,y1,r):return[(-x+r,y0),(x-r,y0),(x,y0+r),(x,y1-r),(x-r,y1),(-x+r,y1),(-x,y1-r),(-x,y0+r)]
def prism(name,p,z0,z1,m,transform=None):
 v=[(x,y,z)for z in[z0,z1]for x,y in p];n=len(p);f=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)]
 if transform:v=[transform(q)for q in v]
 record(name,v,f,m)
def box(name,lo,hi,m,transform=None):prism(name,[(lo[0],lo[1]),(hi[0],lo[1]),(hi[0],hi[1]),(lo[0],hi[1])],lo[2],hi[2],m,transform)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(sum(x*x for x in a)))
def radial_profile(name,c,axis,u,profile,m,n=48,closed=False):
 v=cross(axis,u);vs=[add(c,add(mul(axis,t),add(mul(u,r*math.cos(math.tau*i/n)),mul(v,r*math.sin(math.tau*i/n)))))for t,r in profile for i in range(n)]
 fs=[]
 for j in range(len(profile)if closed else len(profile)-1):
  k=(j+1)%len(profile)
  for i in range(n):q=(i+1)%n;fs.append((j*n+i,j*n+q,k*n+q,k*n+i))
 if not closed:fs +=[tuple(reversed(range(n))),tuple((len(profile)-1)*n+i for i in range(n))]
 record(name,vs,fs,m)
def band(name,c,u,v,ri,ro,half,m):
 normal=cross(u,v);radial_profile(name,c,normal,u,[(-half,ri),(-half,ro),(half,ro),(half,ri)],m,64,True)
def rod(name,a,b,r,m):
 ax=unit(tuple(y-x for x,y in zip(a,b)));u=unit(cross(ax,(0,0,1)if abs(ax[2])<.9 else(0,1,0)));length=math.sqrt(sum((y-x)**2 for x,y in zip(a,b)));radial_profile(name,a,ax,u,[(0,r),(length,r)],m,16)
def make_geometry():
 G.clear();C=(0,.20,.60);angle=math.radians(35);A=(0,-math.sin(angle),math.cos(angle));U=(1,0,0);V=cross(A,U)
 def w(x,y,t):return add(C,add(mul(U,x),add(mul(V,y),mul(A,t))))
 radial_profile('WholeGroundCircularBase',(0,.15,0),(0,0,1),(1,0,0),[(0,.47),(.025,.49),(.08,.49)],1,48)
 # A complete closed-back square vessel: continuous walls, finite rim, genuine front cavity.
 vs=[]
 for t,r in[(-.12,.255),(.28,.255),(-.06,.224),(.28,.224)]:vs +=[w(x*r,y*r,t)for x,y in[(-1,-1),(1,-1),(1,1),(-1,1)]]
 fs=[(0,3,2,1),(8,9,10,11)]
 for i in range(4):q=(i+1)%4;fs +=[(i,q,4+q,4+i),(4+i,4+q,12+q,12+i),(8+q,8+i,12+i,12+q)]
 record('WholeOpenFrontClosedBackMirrorBox',vs,fs,0)
 radial_profile('PrimaryStyleInsetDisplayDisc',w(0,0,-.063),A,U,[(0,.199),(.018,.199)],3,48)
 # Side altitude discs, with exact lower polygon stations reused by each rocker cheek.
 B=w(0,0,.05);radius=.25
 for sign in[-1,1]:
  center=add(B,(sign*.285,0,0));radial_profile('WholeSideAltitudeDisc_'+str(sign),center,U,(0,1,0),[(-.045,radius),(.045,radius)],2,64)
  stations=[(B[1]-.40,B[2]),(B[1]-.25,B[2])]+[(B[1]+radius*math.cos(math.pi+math.pi*j/32),B[2]+radius*math.sin(math.pi+math.pi*j/32))for j in range(1,32)]+[(B[1]+.25,B[2]),(B[1]+.40,B[2])]
  x0,x1=(.305,.355)if sign>0 else(-.355,-.305);v=[]
  for y,z in stations:v +=[(x0,y,.075),(x1,y,.075),(x1,y,z),(x0,y,z)]
  faces=[(3,2,1,0),tuple(range(4*(len(stations)-1),4*len(stations)))]+[(4*j+i,4*j+(i+1)%4,4*(j+1)+(i+1)%4,4*(j+1)+i)for j in range(len(stations)-1)for i in range(4)]
  record('WholeConcaveRockerCheek_'+str(sign),v,faces,1)
 box('RockerRearCrossTie',(-.35,B[1]+.27,.075),(.35,B[1]+.35,.25),1)
 # The long tube span is deliberately open: eight complete rods, no hidden wall sheet.
 for k in range(4):
  a=math.pi/4+math.tau*k/4
  for sign in[-1,1]:
   lower=a+sign*.12;upper=a-sign*.25
   p=w(.32*math.cos(lower),.32*math.sin(lower),.265);q=w(.241*math.cos(upper),.241*math.sin(upper),1.035)
   rod('FullExposedDiagonalTruss_%d_%d'%(k,sign),p,q,.012,2)
 radial_profile('WholeHollowUpperCage',C,A,U,[(1.0,.249),(1.15,.249),(1.15,.218),(1.0,.218)],0,48,True)
 for k in range(4):
  a=math.tau*k/4;p=w(.012*math.cos(a),.012*math.sin(a),1.085);q=w(.235*math.cos(a),.235*math.sin(a),1.085);rod('ThinUpperSpider_'+str(k),p,q,.005,2)
 N=unit(add(A,U));P=w(0,0,1.085);UU=V
 radial_profile('FixedDiagonalSecondaryStyleDisc',P,N,UU,[(-.006,.041),(.006,.041)],3,24)
 F=w(.235,0,1.085);radial_profile('WholeSideEyepieceBarrel',F,U,V,[(0,.035),(.14,.035),(.14,.022),(0,.022)],2,24,True)
 radial_profile('SideEyepieceInsetDisc',add(F,(.125,0,0)),U,V,[(0,.021),(.007,.021)],3,24)
 # Centre the complete ground footprint, not individual moving parts.
 pts=[p for v,f,m in G.values()for p in v];cy=(max(p[1]for p in pts)+min(p[1]for p in pts))/2
 for n,(v,f,m)in list(G.items()):G[n]=([(x,y-cy,z)for x,y,z in v],f,m)
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
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==24
 triangle_count=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons);assert triangle_count==proof['triangles']
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 lo=[min(v[k]for v in points)for k in range(3)];hi=[max(v[k]for v in points)for k in range(3)]
 assert abs(lo[2])<=TOL
 assert len({m for o in parts for m in o.data.materials})==4
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
 for layer in scene.view_layers:layer.cycles.use_denoising=False
 scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
 scene.render.resolution_x=scene.render.resolution_y=640;scene.render.resolution_percentage=100
 scene.world=scene.world or bpy.data.worlds.new('Neutral open truss telescope preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.78))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(6,-9,6));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'),compress=False)
 def config():return dict(engine=scene.render.engine,samples=scene.cycles.samples,adaptive=scene.cycles.use_adaptive_sampling,cycles_denoise=scene.cycles.use_denoising,view_layer_denoise=[x.cycles.use_denoising for x in scene.view_layers],compositor_nodes=scene.use_nodes,compositing=scene.render.use_compositing,threads_mode=scene.render.threads_mode,threads=scene.render.threads)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'asset':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':24,'mesh_objects':24,'triangles':triangle_count,'materials':4,'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
 qa['native_saved_render_config']=config();qa['render_configs']={}
 if '--geometry-only' not in sys.argv:
  view=sys.argv[sys.argv.index('--tier-single-view')+1]if '--tier-single-view'in sys.argv else 'thumbnail';assert view in ['qa-front','thumbnail']
  scene.cycles.samples=16 if view=='qa-front' else 128;qa['render_configs'][view]=config();scene.render.filepath=str(OUT/(view+'.png'));start=time.monotonic();bpy.ops.render.render(write_still=True);qa['render']={'view':view,'samples':scene.cycles.samples,'seconds':time.monotonic()-start,'original_pixels_reviewed':False}
 (OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if p.exists():files[role]={'path':f'assets/astronomy/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'astronomy','style':'source-preserved-low-poly','title':TITLE,'description':'One newly authored complete fixed open-truss reflector-style telescope display. A closed-back square mirror box opens into eight long exposed diagonal truss rods and a short hollow front cage carrying four thin spider members, a small diagonal secondary-style disc and a side eyepiece tube. Two large side bearing discs seat into matching concave rocker cheeks on a broad circular ground base. The main body has a genuinely open long span, not the old closed-cylinder tripod telescope recolored or resized; the complete ground-rocker support differs from the counterweighted equatorial stand. All parts form one fixed whole prop. Intentional finite overlaps fix static joints; no rotation range, balancing, optical prescription, focus, tracking, alignment, telescope compatibility, historical accuracy, engineering or safety claim.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
