'One newly authored whole fixed horizontal hand-mincer appearance: table-edge C-casting and raised pressure pad with spindle/crossbar, horizontal deep barrel with complete nine-bore front plate and lugged retaining collar, open flared top feed hopper and rear offset crank with whole wood grip. New complete original numeric geometry, no old coffee grinder, vise or mixer imported. Hopper has a real blind floor embedded into barrel top; no continuous internal processing circuit or auger is claimed. Static game-art only, one model zero scenes, no food cutting, grinding, rotation, mounting force, food-contact suitability, hygiene or safety claim. Lower C-casting is a preview datum, not a certified self-standing installation; no table host included.'
import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='kitchen-fixed-clamp-on-horizontal-mincer-01'
TITLE='Fixed Clamp-On Horizontal Mincer'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('CastBodyMutedTeal',(.10,.25,.23,1),.61),('PlainMetal',(.44,.48,.45,1),.46),('WoodGrip',(.29,.14,.055,1),.63),('PerforatedPlate',(.26,.29,.27,1),.53)]
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
def cyl(name,center,r,length,axis,m,n=12):
 axes=[i for i in range(3)if i!=axis];v=[]
 for end in[-.5,.5]:
  for i in range(n):
   p=list(center);p[axis]+=end*length;p[axes[0]]+=r*math.cos(i*math.tau/n);p[axes[1]]+=r*math.sin(i*math.tau/n);v.append(tuple(p))
 record(name,v,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],m)
def sweep(name,path,r,m,n=12):
 # Constant out-of-plane axis prevents local frame flips along this planar neck.
 v=[]
 for j,p in enumerate(path):
  a=path[max(0,j-1)];b=path[min(len(path)-1,j+1)];dy=b[1]-a[1];dz=b[2]-a[2];q=math.hypot(dy,dz);u=(0,dz/q,-dy/q)
  for i in range(n):
   t=math.tau*i/n;v.append((p[0]+r*math.cos(t),p[1]+u[1]*r*math.sin(t),p[2]+u[2]*r*math.sin(t)))
 fs=[tuple(reversed(range(n))),tuple((len(path)-1)*n+i for i in range(n))]
 fs +=[(k*n+i,k*n+(i+1)%n,(k+1)*n+(i+1)%n,(k+1)*n+i)for k in range(len(path)-1)for i in range(n)]
 record(name,v,fs,m)
def ring(name,x0,x1,y,th,z0,z1,m,tr=None):
 outer=[(x0,-y),(x1,-y),(x1,y),(x0,y)];inner=[(x0+th,-y+th),(x1-th,-y+th),(x1-th,y-th),(x0+th,y-th)]
 v=[(x,y,z)for z,p in[(z0,outer),(z0,inner),(z1,outer),(z1,inner)]for x,y in p];fs=[]
 for i in range(4):
  j=(i+1)%4;fs +=[(i,j,4+j,4+i),(8+i,12+i,12+j,8+j),(i,8+i,8+j,j),(4+i,4+j,12+j,12+i)]
 if tr:v=[tr(p)for p in v]
 record(name,v,fs,m)
def rod(name,a,b,r,m,n=8):
 d=[b[i]-a[i]for i in range(3)];le=math.sqrt(sum(t*t for t in d));w=[t/le for t in d];seed=[0,0,1]if abs(w[2])<.9 else[0,1,0]
 u=[w[1]*seed[2]-w[2]*seed[1],w[2]*seed[0]-w[0]*seed[2],w[0]*seed[1]-w[1]*seed[0]];le=math.sqrt(sum(t*t for t in u));u=[t/le for t in u];v=[w[1]*u[2]-w[2]*u[1],w[2]*u[0]-w[0]*u[2],w[0]*u[1]-w[1]*u[0]]
 vs=[tuple(p[k]+r*(u[k]*math.cos(math.tau*i/n)+v[k]*math.sin(math.tau*i/n))for k in range(3))for p in[a,b]for i in range(n)]
 record(name,vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],m)
def make_geometry():
 G.clear()
 def lathe(name,profile,cx,cy,mat,N=24,tr=None):
  v=[];rings=[];f=[]
  for r,z in profile:
   ring=[]
   for i in range(N if r else 1):ring.append(len(v));p=(cx+r*math.cos(math.tau*i/N),cy+r*math.sin(math.tau*i/N),z);v.append(tr(p)if tr else p)
   rings.append(ring)
  for aa,bb in zip(rings,rings[1:]+rings[:1]):
   if len(aa)==len(bb)==1:continue
   for i in range(N):
    j=(i+1)%N;f.append((aa[0],bb[j],bb[i])if len(aa)==1 else((aa[i],aa[j],bb[0])if len(bb)==1 else(aa[i],aa[j],bb[j],bb[i])))
  record(name,v,f,mat)
 # Full C-casting carries the horizontal barrel above an open fixed table-clamp gap.
 union_boxes('WholeTableEdgeCCasting',[((-.040,.043,0),(.040,.085,.275)),((-.040,-.072,0),(.040,.085,.035)),((-.050,-.072,.230),(.050,.085,.272))],0)
 H=lambda p:(p[0],-p[2],.320+p[1])
 lathe('WholeHorizontalOpenBarrel',[(0,-.085),(.050,-.085),(.063,-.060),(.063,.097),(.068,.104),(.051,.104),(.048,.089),(.048,-.059),(0,-.059)],0,0,0,32,H)
 # Genuine open flared hopper with a blind floor embedded into the barrel top; no continuous processing circuit claim.
 lathe('WholeOpenFlaredFeedHopper',[(0,.366),(.026,.366),(.029,.398),(.083,.464),(.086,.476),(.073,.476),(.071,.465),(.019,.398),(0,.386)],0,.015,1,24)
 cyl('WholeClampVerticalSpindle',(0,-.038,.092),.008,.158,2,1,16)
 cyl('WholeRaisedTablePressurePad',(0,-.038,.167),.023,.018,2,1,20)
 cyl('WholeClampCrossBar',(0,-.038,.049),.005,.145,0,1,12)
 for s in[-1,1]:cyl('WholeCrossBarEnd'+str(s),(s*.074,-.038,.049),.008,.012,0,1,12)
 cyl('WholeRearDriveStub',(0,.104,.320),.013,.068,1,1,16)
 # One offset crank with a complete end grip, fixed and non-operative.
 rod('WholeOffsetCrankArm',(0,.127,.320),(.108,.127,.232),.010,1,12)
 cyl('WholeCrankGripAxle',(.108,.161,.232),.007,.083,1,1,12)
 lathe('WholeWoodCrankGrip',[(0,-.142),(.014,-.142),(.018,-.151),(.018,-.195),(.013,-.204),(0,-.204)],0,0,2,16,lambda p:(.108+p[0],-p[2],.232+p[1]))
 lathe('WholeFrontRetainingCollar',[(.051,.095),(.072,.095),(.072,.130),(.054,.130),(.051,.123)],0,0,1,32,H)
 for s in[-1,1]:box('WholeCollarGripLug'+str(s),(s*.076-.012,-.124,.312),(s*.076+.012,-.102,.328),1)
 # Whole perforated front plate: nine independent real bores, not painted dots.
 outline=[(.053*math.cos(math.tau*i/40),.053*math.sin(math.tau*i/40))for i in range(40)]
 holes=[[(.007*math.cos(math.tau*j/10),.007*math.sin(math.tau*j/10))for j in range(10)]]
 holes +=[[(.031*math.cos(a)+.0068*math.cos(math.tau*j/10),.031*math.sin(a)+.0068*math.sin(math.tau*j/10))for j in range(10)]for a in[math.tau*k/8+.12 for k in range(8)]]
 outline=[tuple(round(t,9)for t in p)for p in outline];holes=[[tuple(round(t,9)for t in p)for p in h]for h in holes]
 def cross2(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 def ears(p):
  ids=list(range(len(p)));out=[]
  if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:ids.reverse()
  while len(ids)>3:
   for j,b in enumerate(ids):
    a,c=ids[j-1],ids[(j+1)%len(ids)]
    if cross2(p[a],p[b],p[c])<=1e-14:continue
    if any(all(cross2(p[u],p[v],p[k])>=-1e-14 for u,v in[(a,b),(b,c),(c,a)])for k in ids if k not in[a,b,c]):continue
    out.append((a,b,c));ids.pop(j);break
   else:raise AssertionError('strip triangulation')
  out.append(tuple(ids));return out
 def interval(poly,x):
  if x<min(a for a,b in poly)-1e-10 or x>max(a for a,b in poly)+1e-10:return None
  ys=[]
  for (a,u),(b,v)in zip(poly,poly[1:]+poly[:1]):
   if abs(b-a)<1e-12:
    if abs(x-a)<1e-9:ys.extend([u,v])
   elif min(a,b)-1e-10<=x<=max(a,b)+1e-10:ys.append(u+(v-u)*(x-a)/(b-a))
  return min(ys),max(ys)
 stations=sorted(set(round(x,9)for poly in[outline]+holes for x,y in poly));pp=[];tt=[];ix={}
 def vertex(p):
  p=tuple(round(c,9)for c in p)
  if p not in ix:ix[p]=len(pp);pp.append(p)
  return ix[p]
 def cell(a,b,al,bl,ah,bh):
  right=sorted(set(y for poly in holes for q in[interval(poly,b)]if q for y in q if bl+1e-9<y<bh-1e-9));left=sorted(set(y for poly in holes for q in[interval(poly,a)]if q for y in q if al+1e-9<y<ah-1e-9),reverse=True)
  p=[(a,al),(b,bl)]+[(b,y)for y in right]+[(b,bh),(a,ah)]+[(a,y)for y in left];q=[]
  for point in p:
   point=tuple(round(c,9)for c in point)
   if not q or q[-1]!=point:q.append(point)
  if q[0]==q[-1]:q.pop()
  if len(q)<3:return
  ids=[vertex(v)for v in q];tt.extend(tuple(ids[k]for k in tri)for tri in ears(q))
 for a,b in zip(stations,stations[1:]):
  aa=interval(outline,a);bb=interval(outline,b);active=sorted((p for p in holes if min(x for x,y in p)<(a+b)/2<max(x for x,y in p)),key=lambda p:interval(p,(a+b)/2)[0]);al,bl=aa[0],bb[0]
  for p in active:lo,hi=interval(p,a);ll,hh=interval(p,b);cell(a,b,al,bl,lo,ll);al,bl=hi,hh
  cell(a,b,al,bl,aa[1],bb[1])
 n=len(pp);v=[H((x,y,z))for z in[.117,.126]for x,y in pp];f=[tuple(reversed(t))for t in tt]+[tuple(n+i for i in t)for t in tt];edges={}
 for t in tt:
  for a,b in zip(t,t[1:]+t[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((a,b))
 for key,es in edges.items():
  if len(es)==1:a,b=es[0];f.append((a,b,b+n,a+n))
 record('WholeNineBoreMincerFacePlate',v,f,3)
 pts=[p for v,f,m in G.values()for p in v];sx=(min(p[0]for p in pts)+max(p[0]for p in pts))/2;sy=(min(p[1]for p in pts)+max(p[1]for p in pts))/2
 for name,(v,f,m)in list(G.items()):G[name]=([(x-sx,y-sy,z)for x,y,z in v],f,m)
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
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==16
 triangle_count=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons);assert triangle_count==proof['triangles']
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 lo=[min(v[k]for v in points)for k in range(3)];hi=[max(v[k]for v in points)for k in range(3)]
 assert abs(lo[2])<=TOL
 assert len({m for o in parts for m in o.data.materials})==4
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
 for layer in scene.view_layers:layer.cycles.use_denoising=False
 scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
 scene.render.resolution_x=scene.render.resolution_y=640;scene.render.resolution_percentage=100
 scene.world=scene.world or bpy.data.worlds.new('Neutral exercise cycle preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.42))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(4,-6,3.4));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'),compress=False)
 def config():return dict(engine=scene.render.engine,samples=scene.cycles.samples,adaptive=scene.cycles.use_adaptive_sampling,cycles_denoise=scene.cycles.use_denoising,view_layer_denoise=[x.cycles.use_denoising for x in scene.view_layers],compositor_nodes=scene.use_nodes,compositing=scene.render.use_compositing,threads_mode=scene.render.threads_mode,threads=scene.render.threads)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'asset':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':16,'mesh_objects':16,'triangles':triangle_count,'materials':4,'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
 qa['native_saved_render_config']=config();qa['render_configs']={}
 if '--geometry-only' not in sys.argv:
  view=sys.argv[sys.argv.index('--tier-single-view')+1]if '--tier-single-view'in sys.argv else 'thumbnail';assert view in ['qa-front','thumbnail']
  scene.cycles.samples=16 if view=='qa-front' else 128;qa['render_configs'][view]=config();scene.render.filepath=str(OUT/(view+'.png'));start=time.monotonic();bpy.ops.render.render(write_still=True);qa['render']={'view':view,'samples':scene.cycles.samples,'seconds':time.monotonic()-start,'original_pixels_reviewed':False}
 (OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if p.exists():files[role]={'path':f'assets/winter/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'kitchen','style':'source-preserved-low-poly','title':TITLE,'description':'One newly authored whole fixed horizontal hand-mincer appearance: table-edge C-casting and raised pressure pad with spindle/crossbar, horizontal deep barrel with complete nine-bore front plate and lugged retaining collar, open flared top feed hopper and rear offset crank with whole wood grip. New complete original numeric geometry, no old coffee grinder, vise or mixer imported. Hopper has a real blind floor embedded into barrel top; no continuous internal processing circuit or auger is claimed. Static game-art only, one model zero scenes, no food cutting, grinding, rotation, mounting force, food-contact suitability, hygiene or safety claim. Lower C-casting is a preview datum, not a certified self-standing installation; no table host included.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
