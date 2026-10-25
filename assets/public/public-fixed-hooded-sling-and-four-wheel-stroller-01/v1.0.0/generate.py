'One newly authored complete static hooded-stroller appearance in an empty fixed display pose. Two continuous front-to-rear push side tubes and separate trailing legs support four full annular wheels in actual open forks, a shared rear pushbar and a complete continuous calf-seat-back sling. Two raised side bolsters border the sling. A full thick curved canopy forms a genuine open front underside and is rooted by two complete curved side ribs and rear stays. One low empty basket with its floor and walls sits within dedicated lower rails and crosssupports. This is not the manual wheelchair with its large handrims removed or the rollator with a differently coloured seat; all numerical geometry is new and no old component is imported. Three opaque materials, one prop zero scenes. Fixed visual art only: no child or occupant, textile simulation, restraint system, steering, rolling, folding path, seating or age suitability, human fit, loading, stability, manufacture, transport or product safety certification. Rigging animation and interaction not made.'
import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='public-fixed-hooded-sling-and-four-wheel-stroller-01'
TITLE='Fixed Hooded Sling and Four Wheel Stroller'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeMutedMetalFrame', [0.15, 0.28, 0.28, 1], 0.69), ('WholeDeepFabricCanopyAndSling', [0.16, 0.26, 0.36, 1], 0.88), ('WholeDarkPadsAndGrips', [0.08, 0.12, 0.12, 1], 0.8)]
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
 for side in [-1,1]:
  x=side*.245
  whole_curved_hose('WholeFrontToPushSideFrame'+str(side),[(x,-.35,.17),(x,-.23,.43),(x,.04,.64),(x,.34,.95),(x,.43,1.01)],.018,0)
  rod('WholeRearTrailingLeg'+str(side),(x,.11,.70),(x,.34,.17),.019,0)
  rod('WholeSeatRail'+str(side),(x,-.27,.49),(x,.15,.49),.017,0)
  rod('WholeBackSupport'+str(side),(x,.13,.49),(x,.31,.91),.016,0)
  rod('WholeFootrestSupport'+str(side),(x,-.22,.48),(x,-.48,.30),.014,0)
  for j,y in enumerate([-.35,.34]):
   z=.10
   radial_profile('WholeAnnularWheel'+str((side,j)),(x-.027,y,z),(1,0,0),(0,1,0),[(0,.033),(0,.10),(.054,.10),(.054,.033)],2,n=24,closed=True)
   rod('WholeWheelHub'+str((side,j)),(x-.03,y,z),(x+.03,y,z),.039,0)
   rod('WholeWheelAxle'+str((side,j)),(x-.055,y,z),(x+.055,y,z),.011,0)
   union_boxes('WholeWheelFork'+str((side,j)),[((x-.049,y-.025,.085),(x-.035,y+.025,.218)),((x+.035,y-.025,.085),(x+.049,y+.025,.218)),((x-.049,y-.025,.20),(x+.049,y+.025,.232))],0)
  radial_profile('WholeSideFramePivot'+str(side),(x-.026,.10,.65),(1,0,0),(0,1,0),[(0,.03),(.052,.03)],2,24)
 rod('WholePushCrossbar',(-.245,.43,1.01),(.245,.43,1.01),.026,2)
 for y in [-.24,.13]:rod('WholeSeatCrossbearer'+str(y),(-.245,y,.49),(.245,y,.49),.015,0)
 rod('WholeLowRearTie',(-.245,.31,.25),(.245,.31,.25),.013,0)
 # One complete thick textile-look seat/calf/back ribbon, not a chair imported onto wheels.
 path=[(-.48,.305),(-.27,.505),(.13,.505),(.31,.91)]
 v=[]
 for y,z in path:v +=[(-.24,y,z-.012),(.24,y,z-.012),(.24,y,z+.012),(-.24,y,z+.012)]
 k=len(path)-1;fs=[(3,2,1,0),tuple(k*4+i for i in range(4))]+[(j*4+i,j*4+(i+1)%4,(j+1)*4+(i+1)%4,(j+1)*4+i)for j in range(k)for i in range(4)]
 record('WholeContinuousSeatCalfAndBackSling',v,fs,1)
 for side in [-1,1]:
  x=side*.225
  whole_curved_hose('WholeRaisedSlingSideBolster'+str(side),[(x,-.24,.525),(x,-.12,.56),(x,.12,.56),(x,.26,.82)],.030,1)
 # Entire curved thick canopy roof, closed boundary and genuinely open front underside.
 angles=[i*2.12/12 for i in range(13)];v=[]
 for x,r in [(-.255,.32),(.255,.32),(-.255,.307),(.255,.307)]:v +=[(x,.10+r*math.cos(a),.82+r*math.sin(a))for a in angles]
 n=len(angles);fs=[]
 for i in range(n-1):
  j=i+1;fs +=[(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)]
 fs +=[(0,n,3*n,2*n),(n-1,3*n-1,4*n-1,2*n-1)]
 record('WholeCurvedOpenFrontCanopy',v,fs,1)
 for side in [-1,1]:
  x=side*.247
  whole_curved_hose('WholeCanopySideRib'+str(side),[(x,.10+.313*math.cos(a),.82+.313*math.sin(a))for a in angles],.009,0)
  rod('WholeCanopyRearStay'+str(side),(x,.23,.72),(x,.412,.82),.012,0)
 # One whole open low basket stays within the chassis; no payload is present.
 union_boxes('WholeUnderseatOpenBasket', [((-.19,-.19,.25),(.19,.21,.268)),((-.19,-.19,.25),(-.177,.21,.365)),((.177,-.19,.25),(.19,.21,.365)),((-.19,-.19,.25),(.19,-.177,.365)),((-.19,.197,.25),(.19,.21,.365))],2)
 for y in [-.16,.18]:rod('WholeBasketCrossSupport'+str(y),(-.245,y,.26),(.245,y,.26),.012,0)
 for side in [-1,1]:rod('WholeLowBasketSideRail'+str(side),(side*.245,-.16,.26),(side*.245,.18,.26),.012,0)
 for side in [-1,1]:rod('WholeBasketSuspension'+str(side),(side*.24,.05,.49),(side*.24,.05,.26),.012,0)
 pts=[p for v,f,m in G.values()for p in v];sx=(min(p[0]for p in pts)+max(p[0]for p in pts))/2;sy=(min(p[1]for p in pts)+max(p[1]for p in pts))/2;sz=min(p[2]for p in pts)
 for n,(v,f,m)in list(G.items()):G[n]=([(x-sx,y-sy,z-sz)for x,y,z in v],f,m)
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
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==47
 triangle_count=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons);assert triangle_count==proof['triangles']
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 lo=[min(v[k]for v in points)for k in range(3)];hi=[max(v[k]for v in points)for k in range(3)]
 assert abs(lo[2])<=TOL
 assert len({m for o in parts for m in o.data.materials})==len(PALETTE)
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
 for layer in scene.view_layers:layer.cycles.use_denoising=False
 scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
 scene.render.resolution_x=scene.render.resolution_y=640;scene.render.resolution_percentage=100
 scene.world=scene.world or bpy.data.worlds.new('Neutral fixed hooded stroller preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.56))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(8,-12,7));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'),compress=False)
 def config():return dict(engine=scene.render.engine,samples=scene.cycles.samples,adaptive=scene.cycles.use_adaptive_sampling,cycles_denoise=scene.cycles.use_denoising,view_layer_denoise=[x.cycles.use_denoising for x in scene.view_layers],compositor_nodes=scene.use_nodes,compositing=scene.render.use_compositing,threads_mode=scene.render.threads_mode,threads=scene.render.threads)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'asset':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':47,'mesh_objects':47,'triangles':triangle_count,'materials':len(PALETTE),'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
 qa['native_saved_render_config']=config();qa['render_configs']={}
 if '--geometry-only' not in sys.argv:
  view=sys.argv[sys.argv.index('--tier-single-view')+1]if '--tier-single-view'in sys.argv else 'thumbnail';assert view in ['qa-front','thumbnail']
  scene.cycles.samples=16 if view=='qa-front' else 128;qa['render_configs'][view]=config();scene.render.filepath=str(OUT/(view+'.png'));start=time.monotonic();bpy.ops.render.render(write_still=True);qa['render']={'view':view,'samples':scene.cycles.samples,'seconds':time.monotonic()-start,'original_pixels_reviewed':False}
 (OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if p.exists():files[role]={'path':f'assets/public/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'public','style':'source-preserved-low-poly','title':TITLE,'description':'One newly authored complete static hooded-stroller appearance in an empty fixed display pose. Two continuous front-to-rear push side tubes and separate trailing legs support four full annular wheels in actual open forks, a shared rear pushbar and a complete continuous calf-seat-back sling. Two raised side bolsters border the sling. A full thick curved canopy forms a genuine open front underside and is rooted by two complete curved side ribs and rear stays. One low empty basket with its floor and walls sits within dedicated lower rails and crosssupports. This is not the manual wheelchair with its large handrims removed or the rollator with a differently coloured seat; all numerical geometry is new and no old component is imported. Three opaque materials, one prop zero scenes. Fixed visual art only: no child or occupant, textile simulation, restraint system, steering, rolling, folding path, seating or age suitability, human fit, loading, stability, manufacture, transport or product safety certification. Rigging animation and interaction not made.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
