'One newly authored complete fixed tall treadle and suspended flexible-shaft tool stand appearance. A low open ground frame joins two low axle supports, a large open spoked wheel and an entire hinged footboard with side connecting rod and eccentric pin. An independent tall rear standard carries a small high pulley and one complete closed belt appearance rising from the large wheel. A single continuous gently arched thick flexible conduit reaches from the high axle housing to one hanging blunt handpiece, retained at a small side rest on the standard. All belong to one full apparatus, not loose tools counted separately. There is no scrollsaw worktable, pair of horizontal saw arms or vertical strip, and no drill-press worktable, rigid quill, enclosed head or motor. No old source geometry is imported. One model, zero scenes, four opaque constant PBR materials, metres, Z up, horizontally bounds-centred ground origin. Fixed illustrative overlaps only, not an engineered moving assembly. No drill bit, patient, medical use, power transmission, belt tracking, flexible drive internals, rotation, cutting, operating instructions, manufacture, stability or safety claim. Rigging, animation and interaction are not made and are outside this static delivery.'
import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='professional-fixed-treadle-wheel-and-suspended-shaft-stand-01'
TITLE='Fixed Treadle Wheel and Suspended Shaft Stand'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('MutedDarkStand',(.12,.18,.16,1),.67),('DarkBeltAndConduit',(.055,.050,.045,1),.72),('OpaqueAxlesAndHandpiece',(.46,.48,.45,1),.48),('WarmFootboard',(.31,.18,.075,1),.73)]
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
def earclip(poly):
 ids=list(range(len(poly)));out=[]
 def cross2(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 while len(ids)>3:
  done=False
  for k,i in enumerate(ids):
   a,b,c=ids[k-1],i,ids[(k+1)%len(ids)]
   if cross2(poly[a],poly[b],poly[c])<=1e-13:continue
   if any(j not in [a,b,c] and min(cross2(poly[a],poly[b],poly[j]),cross2(poly[b],poly[c],poly[j]),cross2(poly[c],poly[a],poly[j]))>=-1e-13 for j in ids):continue
   out.append((a,b,c));ids.pop(k);done=True;break
  assert done,'Cannot triangulate complete outer shell'
 out.append(tuple(ids));return out
def annular_x(name,x,z,ri,ro,th,m,n=32):
 vs=[(xx,r*math.cos(i*math.tau/n),z+r*math.sin(i*math.tau/n))for xx,r in[(x-th/2,ri),(x-th/2,ro),(x+th/2,ro),(x+th/2,ri)]for i in range(n)]
 fs=[(j*n+i,j*n+(i+1)%n,((j+1)%4)*n+(i+1)%n,((j+1)%4)*n+i)for j in range(4)for i in range(n)];record(name,vs,fs,m)
def axial_profile(name,profile,center,axis,m,n=32):
 axes=[i for i in range(3)if i!=axis];vs=[];rings=[]
 for r,z in profile:
  row=[]
  for j in range(1 if r==0 else n):
   p=list(center);p[axis]+=z;p[axes[0]]+=r*math.cos(j*math.tau/n);p[axes[1]]+=r*math.sin(j*math.tau/n);row.append(len(vs));vs.append(tuple(p))
  rings.append(row)
 fs=[]
 for k,row in enumerate(rings):
  nex=rings[(k+1)%len(rings)]
  if len(row)==len(nex)==1:continue
  for j in range(n):
   jj=(j+1)%n
   if len(row)==1:fs.append((row[0],nex[j],nex[jj]))
   elif len(nex)==1:fs.append((row[j],nex[0],row[jj]))
   else:fs.append((row[j],nex[j],nex[jj],row[jj]))
 record(name,vs,fs,m)
def whole_belt(name,x,width,m):
 # Shared convex-support envelope of two disks, with matching inset inner envelope.
 loops=[];n=64
 for inset in[0,.012]:
  pts=[]
  for i in range(n):
   t=math.tau*i/n;c=math.cos(t);s=math.sin(t)
   cy,cz,r=max([(0,.390,.283-inset),(.115,1.170,.080-inset)],key=lambda q:q[0]*c+q[1]*s+q[2])
   pts.append((cy+r*c,cz+r*s))
  loops.append(pts)
 v=[(xx,y,z)for xx,p in[(x-width/2,loops[0]),(x-width/2,loops[1]),(x+width/2,loops[0]),(x+width/2,loops[1])]for y,z in p];f=[]
 for i in range(n):
  j=(i+1)%n;f.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 record(name,v,f,m)
def make_geometry():
 G.clear()
 union_boxes('WholeLowOpenGroundFrame',[((-.240,-.370,0),(-.165,.300,.055)),((.165,-.370,0),(.240,.300,.055)),((-.240,.215,.020),(.240,.290,.075)),((-.240,-.290,.020),(.240,-.220,.075))],0)
 box('WholeLowCentralBed',(-.120,-.035,.040),(.120,.270,.085),0)
 for name,x in [('Left',-.090),('Right',.090)]:
  box('Whole'+name+'LowAxleStandard',(x-.023,-.035,.045),(x+.023,.035,.420),0)
  rod('Whole'+name+'RearBrace',(x,.0,.300),(x,.250,.055),.018,0,12)
 cyl('WholeLowWheelAxle',(0,0,.390),.018,.350,0,2,24)
 cyl('WholeLargeWheelHub',(.150,0,.390),.039,.070,0,2,24)
 axial_profile('WholeLargeOpenWheelRim',[(.240,-.022),(.279,-.022),(.279,.022),(.240,.022)],(.150,0,.390),0,0,40)
 for i in range(4):
  a=.35+i*math.tau/4;rod('WholeLargeWheelSpoke'+str(i),(.150,.025*math.cos(a),.390+.025*math.sin(a)),(.150,.258*math.cos(a),.390+.258*math.sin(a)),.017,0,12)
 box('WholeTallRearStandard',(-.043,.090,.050),(.013,.140,1.210),0)
 rod('WholeTallStandardBrace',(-.020,.115,.480),(-.020,.255,.055),.022,0,12)
 cyl('WholeHighCrossAxle',(.085,.115,1.170),.017,.235,0,2,24)
 cyl('WholeHighPulley',(.150,.115,1.170),.078,.045,0,2,32)
 whole_belt('WholeContinuousRisingBelt',.150,.026,1)
 cyl('WholeRearFootboardHinge',(0,.235,.095),.014,.370,0,2,24)
 box('WholeFootboardRearMount',(-.070,.215,.052),(.070,.255,.108),0)
 # Full inclined footboard prism, not two separate pedal fragments.
 prism('WholeInclinedFootboard',[(-.340,.130),(.255,.080),(.255,.113),(-.340,.163)],-.100,.100,3,lambda p:(p[2],p[0],p[1]))
 cyl('WholeFootboardDrivePin',(.100,-.240,.139),.012,.250,0,2,20)
 cyl('WholeEccentricWheelPin',(.202,-.100,.420),.012,.100,0,2,20)
 rod('WholeTreadleConnectingRod',(.224,-.240,.139),(.224,-.100,.420),.012,2,12)
 rod('WholeEccentricSpokeTab',(.150,0,.390),(.150,-.100,.420),.022,0,12)
 cyl('WholeHighConduitSocket',(.235,.115,1.170),.027,.100,0,1,24)
 sweep('WholeContinuousSuspendedConduit',[(.275,.115,1.170),(.275,.170,1.270),(.275,.170,1.350),(.275,.100,1.390),(.275,-.020,1.390),(.275,-.150,1.330),(.275,-.245,1.200),(.275,-.275,1.050),(.275,-.275,.940)],.012,1,16)
 axial_profile('WholeHangingBluntHandpiece',[(0,.770),(.009,.770),(.020,.820),(.020,.930),(.014,.960),(0,.960)],(.275,-.275,0),2,2,20)
 rod('WholeSideHandpieceRestArm',(-.015,.115,.880),(.275,-.275,.880),.012,0,12)
 axial_profile('WholeHandpieceRestRing',[(.018,.862),(.029,.862),(.029,.895),(.018,.895)],(.275,-.275,0),2,0,20)
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
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==30
 triangle_count=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons);assert triangle_count==proof['triangles']
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 lo=[min(v[k]for v in points)for k in range(3)];hi=[max(v[k]for v in points)for k in range(3)]
 assert abs(lo[2])<=TOL
 assert len({m for o in parts for m in o.data.materials})==4
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
 for layer in scene.view_layers:layer.cycles.use_denoising=False
 scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
 scene.render.resolution_x=scene.render.resolution_y=640;scene.render.resolution_percentage=100
 scene.world=scene.world or bpy.data.worlds.new('Neutral instrument preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.695))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(7,-9,5));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'),compress=False)
 def config():return dict(engine=scene.render.engine,samples=scene.cycles.samples,adaptive=scene.cycles.use_adaptive_sampling,cycles_denoise=scene.cycles.use_denoising,view_layer_denoise=[x.cycles.use_denoising for x in scene.view_layers],compositor_nodes=scene.use_nodes,compositing=scene.render.use_compositing,threads_mode=scene.render.threads_mode,threads=scene.render.threads)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'asset':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':30,'mesh_objects':30,'triangles':triangle_count,'materials':4,'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
 qa['native_saved_render_config']=config();qa['render_configs']={}
 if '--geometry-only' not in sys.argv:
  view=sys.argv[sys.argv.index('--tier-single-view')+1]if '--tier-single-view'in sys.argv else 'thumbnail';assert view in ['qa-front','thumbnail']
  scene.cycles.samples=16 if view=='qa-front' else 128;qa['render_configs'][view]=config();scene.render.filepath=str(OUT/(view+'.png'));start=time.monotonic();bpy.ops.render.render(write_still=True);qa['render']={'view':view,'samples':scene.cycles.samples,'seconds':time.monotonic()-start,'original_pixels_reviewed':False}
 (OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if p.exists():files[role]={'path':f'assets/professional/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'professional','style':'source-preserved-low-poly','title':TITLE,'description':'One newly authored complete fixed tall treadle and suspended flexible-shaft tool stand appearance. A low open ground frame joins two low axle supports, a large open spoked wheel and an entire hinged footboard with side connecting rod and eccentric pin. An independent tall rear standard carries a small high pulley and one complete closed belt appearance rising from the large wheel. A single continuous gently arched thick flexible conduit reaches from the high axle housing to one hanging blunt handpiece, retained at a small side rest on the standard. All belong to one full apparatus, not loose tools counted separately. There is no scrollsaw worktable, pair of horizontal saw arms or vertical strip, and no drill-press worktable, rigid quill, enclosed head or motor. No old source geometry is imported. One model, zero scenes, four opaque constant PBR materials, metres, Z up, horizontally bounds-centred ground origin. Fixed illustrative overlaps only, not an engineered moving assembly. No drill bit, patient, medical use, power transmission, belt tracking, flexible drive internals, rotation, cutting, operating instructions, manufacture, stability or safety claim. Rigging, animation and interaction are not made and are outside this static delivery.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
