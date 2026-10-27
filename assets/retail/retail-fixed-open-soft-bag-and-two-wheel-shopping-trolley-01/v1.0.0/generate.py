'One newly authored complete empty static personal shopping trolley. A tall softly faceted rounded rectangular bag has a finite thick wall, closed bottom, genuinely open mouth and one complete raised rear flap. Its full upright tubular frame rises above the flap to a rounded hand grip, carries the bag on a short support tray and attaches behind with two small rooted mounts. Two complete broad wheels flank a full transverse axle and an integral bent forward parking foot reaches the ground. The body has gently varying lower belly and upper sections, unlike a flat paper bag with two loop handles, a large four-wheel lattice retail cart or a bare parcel handtruck with a projecting loading toe. No old source geometry or imported mesh is reused. Three constant opaque PBR materials, metres Z up, horizontal bounds-centred ground origin. One original model, zero scenes. Fixed empty artistic exhibit: no textiles simulation, bag contents, brands, person, wheel rotation, folding motion, load capacity, ergonomic fit, stability, manufacture or safety capability; rigging, animation and interaction not made.'
import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='retail-fixed-open-soft-bag-and-two-wheel-shopping-trolley-01'
TITLE='Fixed Open Soft Bag and Two Wheel Shopping Trolley'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeMutedWineBagAndFlap',[.34,.12,.16,1],.90),('WholeLightTubularFrameAndHubs',[.52,.57,.57,1],.52),('WholeGraphiteTyresAndGrip',[.055,.070,.075,1],.86)]
G={}
def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def rect(x,y0,y1,r):return[(-x+r,y0),(x-r,y0),(x,y0+r),(x,y1-r),(x-r,y1),(-x+r,y1),(-x,y1-r),(-x,y0+r)]
def triangulate_polygon(p):
 cross2=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 order=list(range(len(p)));out=[]
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:order.reverse()
 while len(order)>3:
  for k,b in enumerate(order):
   a,c=order[k-1],order[(k+1)%len(order)]
   if cross2(p[a],p[b],p[c])<=1e-14:continue
   if any(min(cross2(p[a],p[b],p[j]),cross2(p[b],p[c],p[j]),cross2(p[c],p[a],p[j]))>=-1e-14 for j in order if j not in[a,b,c]):continue
   out.append((a,b,c));order.pop(k);break
  else:raise AssertionError('Untriangulable original polygon')
 return out+[tuple(order)]
def prism(name,p,z0,z1,m,transform=None):
 v=[(x,y,z)for z in[z0,z1]for x,y in p];n=len(p);tri=triangulate_polygon(p)
 f=[tuple(reversed(t))for t in tri]+[tuple(n+i for i in t)for t in tri]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)]
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
def whole_soft_bag():
 n=32;stations=[(.205,.165,.117),(.28,.183,.137),(.52,.188,.145),(.75,.177,.132)];vertices=[]
 def ring(z,rx,ry):
  q=[]
  for j in range(n):
   a=math.tau*j/n;co,si=math.cos(a),math.sin(a);w=1-.014*math.cos(8*a)
   q.append((rx*math.copysign(abs(co)**.48,co)*w,ry*math.copysign(abs(si)**.48,si)*w,z))
  return q
 for z,x,y in stations:vertices+=ring(z,x,y)
 for z,x,y in stations:vertices+=ring(max(z,.217),x-.008,y-.008)
 caps=triangulate_polygon([(x,y)for x,y,z in vertices[:n]]);innercaps=triangulate_polygon([(x,y)for x,y,z in vertices[4*n:5*n]]);faces=[tuple(reversed(t))for t in caps]+[tuple(4*n+j for j in t)for t in innercaps]
 for k in range(3):
  for j in range(n):
   q=(j+1)%n;faces +=[(k*n+j,k*n+q,(k+1)*n+q,(k+1)*n+j),(4*n+k*n+j,4*n+(k+1)*n+j,4*n+(k+1)*n+q,4*n+k*n+q)]
 for j in range(n):q=(j+1)%n;faces.append((3*n+j,3*n+q,7*n+q,7*n+j))
 record('WholeClosedBottomOpenMouthSoftBag',vertices,faces,0)
def make_geometry():
 G.clear();whole_soft_bag()
 # A complete shallow bowed flap rises behind the open mouth, with finite material thickness.
 p=[(-.168,0),(.168,0),(.170,.185),(.148,.245),(-.148,.245),(-.170,.185)];angle=math.radians(55)
 prism('WholeRaisedRearBagFlap',p,-.004,.004,0,lambda q:(q[0],.128+q[1]*math.cos(angle)-q[2]*math.sin(angle),.744+q[1]*math.sin(angle)+q[2]*math.cos(angle)))
 path=[(-.19,.185,.145),(-.19,.185,1.015)]
 for j in range(1,7):a=math.pi-j*(math.pi/2)/6;path.append((-.13+.06*math.cos(a),.185,1.015+.06*math.sin(a)))
 path.append((.13,.185,1.075))
 for j in range(1,7):a=math.pi/2-j*(math.pi/2)/6;path.append((.13+.06*math.cos(a),.185,1.015+.06*math.sin(a)))
 path.append((.19,.185,.145));whole_curved_hose('WholeRoundedUprightTrolleyFrame',path,.013,1)
 rod('WholeFixedTopHandGrip',(-.125,.185,1.075),(.125,.185,1.075),.022,2)
 for tag,z in [('Lower',.34),('Upper',.675)]:rod('Whole'+tag+'RearCrossRail',(-.19,.185,z),(.19,.185,z),.011,1)
 for tag,x in [('Left',-.12),('Right',.12)]:box('Whole'+tag+'RearBagMount',(x-.018,.125,.659),(x+.018,.194,.688),0)
 prism('WholeShortUnderBagSupport',rect(.186,-.135,.197,.018),.184,.209,1)
 whole_curved_hose('WholeBentForwardParkingFoot',[(-.165,.18,.185),(-.165,-.125,.027),(-.15,-.15,.015),(.15,-.15,.015),(.165,-.125,.027),(.165,.18,.185)],.015,1)
 rod('WholeTransverseWheelAxle',(-.258,.17,.115),(.258,.17,.115),.015,1)
 for tag,x in [('Left',-.238),('Right',.238)]:
  radial_profile('Whole'+tag+'BroadTyre',(x,.17,.115),(1,0,0),(0,1,0),[(-.024,.099),(-.018,.115),(.018,.115),(.024,.099)],2,32)
  radial_profile('Whole'+tag+'Hub',(x,.17,.115),(1,0,0),(0,1,0),[(-.027,.048),(.027,.048)],1,24)
 pts=[p for v,f,m in G.values()for p in v];lo=[min(p[k]for p in pts)for k in range(3)];hi=[max(p[k]for p in pts)for k in range(3)];shift=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2])
 for name,(v,f,m)in list(G.items()):G[name]=([tuple(p[k]-shift[k]for k in range(3))for p in v],f,m)
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
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
 for layer in scene.view_layers:layer.cycles.use_denoising=False
 scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
 scene.render.resolution_x=scene.render.resolution_y=640;scene.render.resolution_percentage=100
 scene.world=scene.world or bpy.data.worlds.new('Neutral empty soft bag trolley display');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.53))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(8,-15,10));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'),compress=False)
 def config():return dict(engine=scene.render.engine,samples=scene.cycles.samples,adaptive=scene.cycles.use_adaptive_sampling,cycles_denoise=scene.cycles.use_denoising,view_layer_denoise=[x.cycles.use_denoising for x in scene.view_layers],compositor_nodes=scene.use_nodes,compositing=scene.render.use_compositing,threads_mode=scene.render.threads_mode,threads=scene.render.threads)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'asset':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':proof['mesh_count'],'mesh_objects':proof['mesh_count'],'triangles':triangle_count,'materials':len(PALETTE),'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
 qa['native_saved_render_config']=config();qa['render_configs']={}
 if '--geometry-only' not in sys.argv:
  view=sys.argv[sys.argv.index('--tier-single-view')+1]if '--tier-single-view'in sys.argv else 'thumbnail';assert view in ['qa-front','thumbnail']
  scene.cycles.samples=16 if view=='qa-front' else 128;qa['render_configs'][view]=config();scene.render.filepath=str(OUT/(view+'.png'));start=time.monotonic();bpy.ops.render.render(write_still=True);qa['render']={'view':view,'samples':scene.cycles.samples,'seconds':time.monotonic()-start,'original_pixels_reviewed':False}
 (OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if p.exists():files[role]={'path':f'assets/retail/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'retail','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete empty static personal shopping trolley. A tall softly faceted rounded rectangular bag has a finite thick wall, closed bottom, genuinely open mouth and one complete raised rear flap. Its full upright tubular frame rises above the flap to a rounded hand grip, carries the bag on a short support tray and attaches behind with two small rooted mounts. Two complete broad wheels flank a full transverse axle and an integral bent forward parking foot reaches the ground. The body has gently varying lower belly and upper sections, unlike a flat paper bag with two loop handles, a large four-wheel lattice retail cart or a bare parcel handtruck with a projecting loading toe. No old source geometry or imported mesh is reused. Three constant opaque PBR materials, metres Z up, horizontal bounds-centred ground origin. One original model, zero scenes. Fixed empty artistic exhibit: no textiles simulation, bag contents, brands, person, wheel rotation, folding motion, load capacity, ergonomic fit, stability, manufacture or safety capability; rigging, animation and interaction not made.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
