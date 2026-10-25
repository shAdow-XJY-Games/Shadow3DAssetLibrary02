'One newly authored complete fixed coffee-roaster-style machine exterior. A long four-foot common base carries a thick horizontal barrel with a genuinely open front chamber, separate full rear end and fixed side-open circular front door. A deep opaque top feed hopper has a real empty blind chamber, without a claimed hidden feed connection. A short open-topped discharge chute leads visually toward a separately supported low circular front pan with its complete floor/rim, central spindle and three full blunt radial sweep pieces. A true open-ended rear elbow and one blank side control complete the whole apparatus. No old winnower, grinder or drum geometry imported or rescaled; the open barrel and front pan are distinct connected stages of one static object. One prop zero scenes, three opaque constant PBR materials. No beans, combustion/heating, roasting or cooling performance, airflow, rotation, continuous processing passage, electrical operation, food handling/hygiene procedure, manufacture or safety certification. Rigging, animation and interaction are not made.'
import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='cafe-fixed-open-drum-and-front-pan-coffee-roaster-01'
TITLE='Fixed Open Drum and Front Pan Coffee Roaster'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('MutedOxideMachineHousing', [0.34, 0.16, 0.1, 1], 0.79), ('OpaqueSteelRimAndPan', [0.4, 0.43, 0.4, 1], 0.63), ('DarkFixedHardware', [0.055, 0.069, 0.066, 1], 0.77)]
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
def whole_curved_hose(name,path,r,m):
 frames=[];last=None
 for k,c in enumerate(path):
  a=path[max(k-1,0)];b=path[min(k+1,len(path)-1)];t=unit(tuple(b[j]-a[j]for j in range(3)))
  if last is None:u=unit(cross(t,(0,0,1) if abs(t[2])<.9 else (1,0,0)))
  else:
   proj=sum(last[j]*t[j]for j in range(3));u=unit(tuple(last[j]-proj*t[j]for j in range(3)))
  v=cross(t,u);last=u;frames.append((u,v))
 verts=[];n=16
 for c,(u,v)in zip(path,frames):verts +=[add(c,add(mul(u,r*math.cos(math.tau*i/n)),mul(v,r*math.sin(math.tau*i/n))))for i in range(n)]
 fs=[tuple(reversed(range(n))),tuple((len(path)-1)*n+i for i in range(n))]
 for k in range(len(path)-1):
  for i in range(n):j=(i+1)%n;fs.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i))
 record(name,verts,fs,m)
def make_geometry():
 G.clear()
 prism('WholeLongCommonMachineBase',rect(.535,-1.15,.715,.060),.035,.105,0)
 for x in[-.435,.435]:
  for y in[-1.04,.605]:radial_profile('WholeGroundFoot_'+str((x,y)),(x,y,0),(0,0,1),(1,0,0),[(0,.049),(.055,.049)],2,n=20)
 prism('WholeRearDrumPedestal',rect(.25,-.03,.44,.035),.095,.605,0)
 # Complete thick horizontal barrel, genuine front chamber, rear closed by its separate full plate.
 radial_profile('WholeThickHorizontalRoasterBarrel',(0,0,.925),(0,1,0),(1,0,0),[(-.215,.310),(-.190,.333),(.450,.333),(.480,.310),(.480,.285),(-.215,.285)],0,n=48,closed=True)
 radial_profile('WholeRearBarrelEnd',(0,.466,.925),(0,1,0),(1,0,0),[(0,.308),(.034,.308)],1,n=48)
 radial_profile('WholeFrontAnnularDrumRim',(0,-.232,.925),(0,1,0),(1,0,0),[(0,.286),(0,.327),(.025,.327),(.025,.286)],1,n=48,closed=True)
 # Separate full round door fixed to the left in an open side pose.
 radial_profile('WholeFixedOpenRoundFrontDoor',(-.325,-.523,.925),(1,0,0),(0,1,0),[(-.015,.292),(.015,.292)],0,n=40)
 for z in[.70,1.15]:
  box('WholeDoorHingeBridge_'+str(z),(-.345,-.370,z-.034),(-.258,-.185,z+.034),1)
  rod('WholeDoorVerticalHingePin_'+str(z),(-.323,-.216,z-.050),(-.323,-.216,z+.050),.018,2)
 whole_curved_hose('WholeDoorOuterGrip',[(-.343,-.66,.89),(-.405,-.66,.89),(-.405,-.66,.99),(-.343,-.66,.99)],.014,2)
 # Top hopper is a genuine empty blind chamber. No hidden connecting passage is asserted.
 radial_profile('WholeUpperHopperNeck',(0,.18,0),(0,0,1),(1,0,0),[(1.215,.085),(1.335,.085)],1,n=24)
 radial_profile('WholeDeepOpenTopFeedHopper',(0,.18,0),(0,0,1),(1,0,0),[(1.305,.083),(1.37,.10),(1.640,.245),(1.675,.245),(1.675,.222),(1.635,.222),(1.383,.078),(1.338,.066)],0,n=40)
 # Deep front receiving/cooling-pan appearance with actual full floor and finite raised rim.
 radial_profile('WholeFrontPanPedestal',(0,-.715,0),(0,0,1),(1,0,0),[(.095,.245),(.160,.230),(.405,.230)],0,n=32)
 radial_profile('WholeOpenCircularFrontPan',(0,-.715,0),(0,0,1),(1,0,0),[(.392,.390),(.423,.435),(.565,.435),(.565,.411),(.446,.411)],1,n=48)
 rod('WholeFixedPanCentreSpindle',(0,-.715,.437),(0,-.715,.585),.028,2)
 for i,a in enumerate([0,2*math.pi/3,4*math.pi/3]):
  u=(math.cos(a),math.sin(a),0);p=(.345*u[0],-.715+.345*u[1],.493);rod('WholeRadialPanSweepArm_'+str(i),(0,-.715,.493),p,.016,2)
  # A full blunt paddle with intentional material overlap, no sweeping animation.
  box('WholeBluntPanSweepPaddle_'+str(i),(.225,-.024,.458),(.373,.024,.505),2,lambda q:(q[0]*u[0]-q[1]*u[1],-.715+q[0]*u[1]+q[1]*u[0],q[2]))
 # Small chute is a whole open-topped thick channel between drum mouth and front pan.
 union_boxes('WholeShortOpenDischargeChute',[((-.145,-.485,.570),(.145,-.198,.598)),((-.145,-.485,.598),(-.123,-.198,.687)),((.123,-.485,.598),(.145,-.198,.687))],1)
 box('WholeBlankRightControlPanel',(.245,.145,.370),(.290,.385,.570),2)
 rod('WholeBlankControlKnob',(.278,.235,.472),(.325,.235,.472),.037,1)
 # True open-ended finite rear elbow tube; its inboard end overlaps the closed rear plate.
 def hollow_bent(name,path,ro,ri,mat):
  frames=[];last=None
  for k,c in enumerate(path):
   a=path[max(k-1,0)];b=path[min(k+1,len(path)-1)];t=unit(tuple(b[j]-a[j]for j in range(3)))
   u=unit(cross(t,(1,0,0)));v=cross(t,u);frames.append((u,v))
  n=20;vs=[]
  for r in[ro,ri]:
   for c,(u,v)in zip(path,frames):vs +=[add(c,add(mul(u,r*math.cos(math.tau*i/n)),mul(v,r*math.sin(math.tau*i/n))))for i in range(n)]
  off=len(path)*n;fs=[]
  for k in range(len(path)-1):
   for i in range(n):j=(i+1)%n;fs +=[(k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i),(off+k*n+i,off+(k+1)*n+i,off+(k+1)*n+j,off+k*n+j)]
  for i in range(n):j=(i+1)%n;fs +=[(i,off+i,off+j,j),((len(path)-1)*n+i,(len(path)-1)*n+j,off+(len(path)-1)*n+j,off+(len(path)-1)*n+i)]
  record(name,vs,fs,mat)
 hollow_bent('WholeOpenRearExhaustElbow',[(0,.473,1.04),(0,.615,1.04),(0,.685,1.10),(0,.685,1.285),(0,.685,1.480)],.063,.048,1)
 pts=[p for v,f,m in G.values()for p in v];sx=(min(p[0]for p in pts)+max(p[0]for p in pts))/2;sy=(min(p[1]for p in pts)+max(p[1]for p in pts))/2;sz=min(p[2]for p in pts)
 for name,(v,f,m)in list(G.items()):G[name]=([(x-sx,y-sy,z-sz)for x,y,z in v],f,m)
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
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==30
 triangle_count=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons);assert triangle_count==proof['triangles']
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 lo=[min(v[k]for v in points)for k in range(3)];hi=[max(v[k]for v in points)for k in range(3)]
 assert abs(lo[2])<=TOL
 assert len({m for o in parts for m in o.data.materials})==len(PALETTE)
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
 for layer in scene.view_layers:layer.cycles.use_denoising=False
 scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
 scene.render.resolution_x=scene.render.resolution_y=640;scene.render.resolution_percentage=100
 scene.world=scene.world or bpy.data.worlds.new('Neutral fixed coffee roaster preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.81))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(8,-13,8));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'),compress=False)
 def config():return dict(engine=scene.render.engine,samples=scene.cycles.samples,adaptive=scene.cycles.use_adaptive_sampling,cycles_denoise=scene.cycles.use_denoising,view_layer_denoise=[x.cycles.use_denoising for x in scene.view_layers],compositor_nodes=scene.use_nodes,compositing=scene.render.use_compositing,threads_mode=scene.render.threads_mode,threads=scene.render.threads)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'asset':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':30,'mesh_objects':30,'triangles':triangle_count,'materials':len(PALETTE),'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
 qa['native_saved_render_config']=config();qa['render_configs']={}
 if '--geometry-only' not in sys.argv:
  view=sys.argv[sys.argv.index('--tier-single-view')+1]if '--tier-single-view'in sys.argv else 'thumbnail';assert view in ['qa-front','thumbnail']
  scene.cycles.samples=16 if view=='qa-front' else 128;qa['render_configs'][view]=config();scene.render.filepath=str(OUT/(view+'.png'));start=time.monotonic();bpy.ops.render.render(write_still=True);qa['render']={'view':view,'samples':scene.cycles.samples,'seconds':time.monotonic()-start,'original_pixels_reviewed':False}
 (OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if p.exists():files[role]={'path':f'assets/cafe/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'cafe','style':'source-preserved-low-poly','title':TITLE,'description':'One newly authored complete fixed coffee-roaster-style machine exterior. A long four-foot common base carries a thick horizontal barrel with a genuinely open front chamber, separate full rear end and fixed side-open circular front door. A deep opaque top feed hopper has a real empty blind chamber, without a claimed hidden feed connection. A short open-topped discharge chute leads visually toward a separately supported low circular front pan with its complete floor/rim, central spindle and three full blunt radial sweep pieces. A true open-ended rear elbow and one blank side control complete the whole apparatus. No old winnower, grinder or drum geometry imported or rescaled; the open barrel and front pan are distinct connected stages of one static object. One prop zero scenes, three opaque constant PBR materials. No beans, combustion/heating, roasting or cooling performance, airflow, rotation, continuous processing passage, electrical operation, food handling/hygiene procedure, manufacture or safety certification. Rigging, animation and interaction are not made.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
