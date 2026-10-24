'One newly authored whole static adjustable-wrench appearance. A continuous long tapered handle and broad fixed-jaw head include a real end hanging hole and an actual through-window below the jaw. A separate whole sliding-jaw appearance has a long transverse stem captured within the fixed head channel and a tall opposed flat jaw in one fixed open pose. A supported transverse axle carries one whole annular-ridged thumbwheel visible through the head window. A short dark inset handle pad leaves the end hole unobstructed. All finite geometry newly authored, no old fixed open-jaw wrench isolated from a wall kit. One prop, zero scenes, three opaque materials. No moving adjustment, helical gear engagement, calibrated jaw opening, torque, gripping capacity, operating guidance or safety claim.'
import base64,copy,hashlib,json,math,struct,zlib,collections
from pathlib import Path
ASSET='industrial-fixed-sliding-jaw-and-thumbwheel-adjustable-wrench-01'
TITLE='Fixed Sliding Jaw and Thumbwheel Adjustable Wrench'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('OpaqueWholeForgedBody', [0.56, 0.61, 0.57, 1], 0.5), ('DarkInsetHandlePad', [0.15, 0.21, 0.18, 1], 0.78), ('MutedAdjusterAndJaw', [0.33, 0.41, 0.36, 1], 0.56)]
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
CY=.04;CZ=.071;AZ=.064
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(v,s):return tuple(x*s for x in v)
def unit(v):
 n=math.sqrt(dot(v,v));assert math.isfinite(n) and n>0
 return tuple(x/n for x in v)
def area(p):return sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))/2
def clean(p):
 out=[]
 for q in p:
  q=tuple(round(x,12)for x in q)
  if not out or q!=out[-1]:out.append(q)
 if len(out)>1 and out[0]==out[-1]:out.pop()
 return out

def clip(p,l):
 if not p:return []
 a,b,c=l;out=[];u=p[-1];du=a*u[0]+b*u[1]-c
 for v in p:
  dv=a*v[0]+b*v[1]-c
  if(du<=1e-13)!=(dv<=1e-13):
   t=du/(du-dv);out.append(tuple(u[k]+t*(v[k]-u[k])for k in range(2)))
  if dv<=1e-13:out.append(v)
  u=v;du=dv
 out=clean(out);return out if len(out)>2 and area(out)>1e-14 else []
def planes(p):
 out=[]
 for a,b in zip(p,p[1:]+p[:1]):
  u,v=b[0]-a[0],b[1]-a[1];n=math.hypot(u,v);out.append((v/n,-u/n,(v*a[0]-u*a[1])/n))
 return out

def contains(p,poly):
 # All classified cells already split at every edge's entire supporting line.
 x,y=p;inside=False
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if(a[1]>y)!=(b[1]>y)and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:inside=not inside
 return inside

def rect(y0,z0,y1,z1):return[(y0,z0),(y1,z0),(y1,z1),(y0,z1)]
def poly(radius,n=16,cy=CY,cz=CZ,phase=math.pi/16):return[(cy+radius*math.cos(phase+math.tau*i/n),cz+radius*math.sin(phase+math.tau*i/n))for i in range(n)]
def build(parts,holes=[],mat=0):
 # Each part: x0,x1,CCW yz polygon. Union boundary only, no internal faces.
 polygons=[r[2]for r in parts+holes];allp=[q for p in polygons for q in p];lo=[min(q[k]for q in allp)for k in[0,1]];hi=[max(q[k]for q in allp)for k in[0,1]]
 cells=[rect(lo[0],lo[1],hi[0],hi[1])];seen=set();lines=[]
 for p in polygons:
  for l in planes(p):
   key=tuple(round(x,10)for x in l)
   if key not in seen:seen.add(key);lines.append(l)
 for l in lines:
  nxt=[]
  for p in cells:
   ds=[l[0]*q[0]+l[1]*q[1]-l[2]for q in p]
   if min(ds)<-1e-10 and max(ds)>1e-10:
    a=clip(p,l);b=clip(p,tuple(-v for v in l));assert a and b,(l,p);nxt +=[a,b]
   else:nxt.append(p)
  cells=nxt
 ec=collections.defaultdict(list)
 for i,p in enumerate(cells):
  for a,b in zip(p,p[1:]+p[:1]):ec[tuple(sorted((a,b)))].append(i)
 assert all(len(v)<=2 for v in ec.values())
 xx=sorted(set(v for a,b,p in parts+holes for v in[a,b]));occ=[]
 for x0,x1 in zip(xx,xx[1:]):
  x=(x0+x1)/2;ss=set()
  for i,p in enumerate(cells):
   c=tuple(sum(q[k]for q in p)/len(p)for k in[0,1])
   if any(a<x<b and contains(c,q)for a,b,q in parts)and not any(a<x<b and contains(c,q)for a,b,q in holes):ss.add(i)
  occ.append(ss)
 vv=[];ff=[];lookup={}
 def vertex(p):
  p=tuple(round(x,12)for x in p)
  if p not in lookup:lookup[p]=len(vv);vv.append(p)
  return lookup[p]
 def tri(p):
  assert dot(cross(sub(p[1],p[0]),sub(p[2],p[0])),cross(sub(p[1],p[0]),sub(p[2],p[0])))>1e-28,p
  ids=tuple(vertex(q)for q in p);assert len(set(ids))==3;ff.append(ids)
 for k,ss in enumerate(occ):
  x0,x1=xx[k:k+2]
  for i in sorted(ss):
   p=cells[i];c=tuple(sum(q[h]for q in p)/len(p)for h in[0,1])
   for x,sign,j in[(x0,-1,k-1),(x1,1,k+1)]:
    if not 0<=j<len(occ)or i not in occ[j]:
     for a,b in zip(p,p[1:]+p[:1]):
      q=[(x,*c),(x,*a),(x,*b)];tri(q if sign>0 else q[::-1])
   for a,b in zip(p,p[1:]+p[:1]):
    other=next((j for j in ec[tuple(sorted((a,b)))]if j!=i),None)
    if other is None or other not in ss:
     aa=(x0,*a);bb=(x0,*b);cc=(x1,*b);dd=(x1,*a);tri([aa,bb,cc]);tri([aa,cc,dd])
 return dict(vertices=vv,faces=ff,face_materials=[mat]*len(ff),material=mat,yz_cells=len(cells),x_levels=xx)

def make_geometry():
 G.clear()
 handle=[(-.014,-.150),(.014,-.150),(.021,-.140),(.018,-.095),(.013,.040),(.022,.069),(-.022,.069),(-.013,.040),(-.018,-.095),(-.021,-.140)]
 head=[(-.022,.052),(.025,.060),(.037,.078),(.035,.116),(.018,.119),(-.012,.119),(-.012,.154),(-.029,.160),(-.042,.142),(-.043,.088),(-.033,.065)]
 g=build([(.003,.023,handle),(.003,.023,head)],[(-.001,.028,poly(.008,16,0,-.130)),(-.001,.028,rect(-.019,.075,.019,.093)),(.009,.017,rect(-.014,.103,.040,.116))])
 record('WholeIntegralHandleFixedJawAndOpenWindows',[(p[1],p[2],p[0])for p in g['vertices']],g['faces'],0)
 g=build([(.010,.016,rect(-.012,.104,.029,.114)),(.005,.021,[ (.020,.108),(.035,.111),(.039,.143),(.030,.156),(.020,.153)])])
 record('WholeFixedPoseSlidingJawAndCapturedStem',[(p[1],p[2],p[0])for p in g['vertices']],g['faces'],2)
 rod('WholeThumbwheelAxle',(-.026,.084,.013),(.026,.084,.013),.0025,0)
 pr=[(-.017,.005)]
 for i in range(6):
  x=-.016+i*.0055;pr.extend([(x,.005),(x+.0015,.008),(x+.0035,.008),(x+.005,.005)])
 pr.append((.017,.005));radial_profile('WholeAnnularRidgedThumbwheel',(0,.084,.013),(1,0,0),(0,1,0),pr,2,20)
 prism('WholeInsetHandlePad',[(-.009,-.109),(.009,-.109),(.008,.028),(-.008,.028)],.022,.025,1)
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
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==5
 triangle_count=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons);assert triangle_count==proof['triangles']
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 lo=[min(v[k]for v in points)for k in range(3)];hi=[max(v[k]for v in points)for k in range(3)]
 assert abs(lo[2])<=TOL
 assert len({m for o in parts for m in o.data.materials})==len(PALETTE)
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
 for layer in scene.view_layers:layer.cycles.use_denoising=False
 scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
 scene.render.resolution_x=scene.render.resolution_y=640;scene.render.resolution_percentage=100
 scene.world=scene.world or bpy.data.worlds.new('Neutral fixed sliding jaw adjustable wrench preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.011))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(7,-9,18));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'),compress=False)
 def config():return dict(engine=scene.render.engine,samples=scene.cycles.samples,adaptive=scene.cycles.use_adaptive_sampling,cycles_denoise=scene.cycles.use_denoising,view_layer_denoise=[x.cycles.use_denoising for x in scene.view_layers],compositor_nodes=scene.use_nodes,compositing=scene.render.use_compositing,threads_mode=scene.render.threads_mode,threads=scene.render.threads)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'asset':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':5,'mesh_objects':5,'triangles':triangle_count,'materials':len(PALETTE),'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'industrial','style':'source-preserved-low-poly','title':TITLE,'description':'One newly authored whole static adjustable-wrench appearance. A continuous long tapered handle and broad fixed-jaw head include a real end hanging hole and an actual through-window below the jaw. A separate whole sliding-jaw appearance has a long transverse stem captured within the fixed head channel and a tall opposed flat jaw in one fixed open pose. A supported transverse axle carries one whole annular-ridged thumbwheel visible through the head window. A short dark inset handle pad leaves the end hole unobstructed. All finite geometry newly authored, no old fixed open-jaw wrench isolated from a wall kit. One prop, zero scenes, three opaque materials. No moving adjustment, helical gear engagement, calibrated jaw opening, torque, gripping capacity, operating guidance or safety claim.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
