'One newly authored complete static floor-standing H-frame press appearance. Two whole deep pierced uprights and a broad upper crosshead stand on long flat feet with a full low tie. Two independent thick bed rails span the upright openings and rest on complete cross pins at one fixed height, leaving an actual open centre. A short central upper cylinder, exposed blunt ram and finite flat pressing pad face that bed across a real empty work interval. A separate rooted side pump case, long fixed lever and one continuous external hose complete the whole exterior. Unlike the earlier open C-casting rack press, this has a bilateral tall portal load-frame and a full spanning pinned bed, with no rack or pinion. It is not the old bottle jack placed in a borrowed frame; all coordinates are newly authored. Three opaque PBR roles, one model zero scenes. No workpiece, hydraulic circuit, pressure, force, travel, lifting, load, stability, manufacture, installation or safety capability. Rigging animation interaction not made.'
import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='industrial-fixed-pierced-h-frame-and-pinned-bed-press-01'
TITLE='Fixed Pierced H Frame and Pinned Bed Press'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeOxideFrame',[.32,.19,.12,1],.70),('WholeSatinPinsAndRam',[.53,.57,.54,1],.52),('WholeDarkBedAndControls',[.10,.14,.13,1],.76)]
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
 for label,x in [('Left',-.43),('Right',.43)]:
  box('Whole'+label+'LongGroundFoot',(x-.115,-.38,0),(x+.115,.38,.075),0)
  # Entire pierced upright plate, with five genuine rectangular through holes.
  cells=[((x-.068,-.055,.060),(x-.027,.065,1.66)),((x+.027,-.055,.060),(x+.068,.065,1.66))]
  z0=.060
  for z in [.52,.68,.84,1.00,1.16]:
   cells.append(((x-.027,-.055,z0),(x+.027,.065,z-.028)));z0=z+.028
  cells.append(((x-.027,-.055,z0),(x+.027,.065,1.66)))
  union_boxes('Whole'+label+'FivePortUpright',cells,0)
  # Rear flange makes the frame visibly deep, with deliberate hidden root overlap.
  box('Whole'+label+'DeepRearFlange',(x+.052,.051,.064),(x+.066,.145,1.65),0)
  rod('Whole'+label+'FixedBedCrossPin',(x,-.205,.840),(x,.205,.840),.022,1)
  radial_profile('Whole'+label+'FrontPinCap',(x,0,.840),(0,1,0),(1,0,0),[(-.222,.037),(-.198,.037)],1,20)
 box('WholeUpperCrosshead',(-.55,-.135,1.590),(.55,.160,1.780),0)
 box('WholeLowCrossTie',(-.450,-.065,.195),(.450,.085,.285),0)
 # Full finite open bed: two spanning rails bear into each fixed cross pin.
 box('WholeFrontBedRail',(-.53,-.181,.825),(.53,-.079,.915),2)
 box('WholeRearBedRail',(-.53,.079,.825),(.53,.181,.915),2)
 radial_profile('WholeUpperCylinderCase',(0,0,0),(0,0,1),(1,0,0),[(1.345,.096),(1.375,.113),(1.635,.113)],0,32)
 radial_profile('WholeLowerRamCollar',(0,0,0),(0,0,1),(1,0,0),[(1.325,.073),(1.370,.073)],1,28)
 radial_profile('WholeExposedBluntRam',(0,0,0),(0,0,1),(1,0,0),[(1.085,.035),(1.345,.035)],1,24)
 radial_profile('WholeFlatPressingPad',(0,0,0),(0,0,1),(1,0,0),[(1.055,.065),(1.105,.065)],2,24)
 box('WholeSidePumpMount',(.470,.045,1.080),(.620,.135,1.300),0)
 prism('WholeSidePumpCase',[(.570,-.050),(.690,-.050),(.715,-.025),(.715,.105),(.570,.105)],1.025,1.355,0)
 rod('WholePumpLeverPivot',(.624,-.087,1.160),(.624,-.028,1.160),.023,1)
 rod('WholeLongFixedPumpLever',(.624,-.064,1.155),(.805,-.064,1.480),.016,1)
 rod('WholePumpLeverGrip',(.771,-.064,1.418),(.820,-.064,1.507),.026,2)
 whole_curved_hose('WholeContinuousExternalHose',[(.665,.095,1.30),(.700,.200,1.39),(.650,.245,1.56),(.435,.225,1.69),(.160,.185,1.69),(.072,.078,1.57)],.014,2)
 pts=[p for v,f,m in G.values()for p in v];sx=(min(p[0]for p in pts)+max(p[0]for p in pts))/2;sy=(min(p[1]for p in pts)+max(p[1]for p in pts))/2
 for n,(v,f,m)in list(G.items()):G[n]=([(x-sx,y-sy,z)for x,y,z in v],f,m)
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
 assert len({m for o in parts for m in o.data.materials})==len(PALETTE)
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
 for layer in scene.view_layers:layer.cycles.use_denoising=False
 scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
 scene.render.resolution_x=scene.render.resolution_y=640;scene.render.resolution_percentage=100
 scene.world=scene.world or bpy.data.worlds.new('Neutral fixed disc and caliper display');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.89))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(10,-18,10));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'),compress=False)
 def config():return dict(engine=scene.render.engine,samples=scene.cycles.samples,adaptive=scene.cycles.use_adaptive_sampling,cycles_denoise=scene.cycles.use_denoising,view_layer_denoise=[x.cycles.use_denoising for x in scene.view_layers],compositor_nodes=scene.use_nodes,compositing=scene.render.use_compositing,threads_mode=scene.render.threads_mode,threads=scene.render.threads)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'asset':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':24,'mesh_objects':24,'triangles':triangle_count,'materials':len(PALETTE),'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
 qa['native_saved_render_config']=config();qa['render_configs']={}
 if '--geometry-only' not in sys.argv:
  view=sys.argv[sys.argv.index('--tier-single-view')+1]if '--tier-single-view'in sys.argv else 'thumbnail';assert view in ['qa-front','thumbnail']
  scene.cycles.samples=16 if view=='qa-front' else 128;qa['render_configs'][view]=config();scene.render.filepath=str(OUT/(view+'.png'));start=time.monotonic();bpy.ops.render.render(write_still=True);qa['render']={'view':view,'samples':scene.cycles.samples,'seconds':time.monotonic()-start,'original_pixels_reviewed':False}
 (OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if p.exists():files[role]={'path':f'assets/industrial/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'industrial','style':'source-preserved-low-poly','title':TITLE,'description':'One newly authored complete static floor-standing H-frame press appearance. Two whole deep pierced uprights and a broad upper crosshead stand on long flat feet with a full low tie. Two independent thick bed rails span the upright openings and rest on complete cross pins at one fixed height, leaving an actual open centre. A short central upper cylinder, exposed blunt ram and finite flat pressing pad face that bed across a real empty work interval. A separate rooted side pump case, long fixed lever and one continuous external hose complete the whole exterior. Unlike the earlier open C-casting rack press, this has a bilateral tall portal load-frame and a full spanning pinned bed, with no rack or pinion. It is not the old bottle jack placed in a borrowed frame; all coordinates are newly authored. Three opaque PBR roles, one model zero scenes. No workpiece, hydraulic circuit, pressure, force, travel, lifting, load, stability, manufacture, installation or safety capability. Rigging animation interaction not made.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
