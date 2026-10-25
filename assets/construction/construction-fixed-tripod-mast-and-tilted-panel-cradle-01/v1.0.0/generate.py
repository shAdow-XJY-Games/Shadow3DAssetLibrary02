'One newly authored complete empty panel-lift-style static exterior. Three low radial outriggers end in complete caster forks, wheels and pivots around one central base. A genuinely bored tall square outer mast surrounds one separate fixed raised inner section with a transverse retaining pin. A complete side bracket carries a flanged drum, through shaft and large three-spoke handwheel with a distinct offset grip. The upper open clevis and full pivot carry one broad tilted H-shaped cradle: an entire cross spine, two whole transverse rails, four small pads and two continuous front stop hooks. No panel, load, cable routing, duplicated old hoist or engine-stand payload. All geometry newly authored; three opaque PBR roles, metres Z up and whole ground-centred bounds. One prop zero scenes. Fixed visual display only: no wheel motion, telescoping travel, winch transmission, brake, board fit, lifting, load capacity, stability, construction use, installation, manufacture or safety claim. Rigging animation interaction not made.'
import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='construction-fixed-tripod-mast-and-tilted-panel-cradle-01'
TITLE='Fixed Tripod Mast and Tilted Panel Cradle'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeMutedTealHousing', [0.15, 0.31, 0.29, 1], 0.69), ('WholeSatinShaftAndBell', [0.54, 0.59, 0.56, 1], 0.53), ('WholeDarkCapsAndControl', [0.08, 0.12, 0.11, 1], 0.76)]
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

def make_geometry():
 G.clear()
 def beam(n,a,b,w,d,m):
  ax=unit(tuple(b[i]-a[i]for i in range(3)));u=unit(cross(ax,(0,0,1)if abs(ax[2])<.9 else(0,1,0)));v=cross(ax,u);le=math.sqrt(sum((b[i]-a[i])**2 for i in range(3)))
  box(n,(-w/2,-d/2,0),(w/2,d/2,le),m,lambda p:add(a,add(mul(u,p[0]),add(mul(v,p[1]),mul(ax,p[2])))))
 h=.075*math.cos(math.pi/16)
 for i,a in enumerate([-math.pi/2,math.pi/6,5*math.pi/6]):
  x=.68*math.cos(a);y=.68*math.sin(a);tag=str(i)
  radial_profile('WholeCasterTire'+tag,(x-.023,y,h),(1,0,0),(0,math.cos(math.pi/16),math.sin(math.pi/16)),[(0,.024),(0,.075),(.046,.075),(.046,.024)],2,16,True)
  rod('WholeCasterAxle'+tag,(x-.054,y,h),(x+.054,y,h),.025,1)
  union_boxes('WholeCasterFork'+tag,[((x-.049,y-.030,h-.012),(x-.034,y+.030,.192)),((x+.034,y-.030,h-.012),(x+.049,y+.030,.192)),((x-.049,y-.030,.174),(x+.049,y+.030,.204))],1)
  radial_profile('WholeCasterPivot'+tag,(x,y,.192),(0,0,1),(1,0,0),[(0,.035),(.055,.035)],1,20)
  beam('WholeLowOutrigger'+tag,(.06*math.cos(a),.06*math.sin(a),.251),(x,y,.231),.077,.076,0)
 prism('WholeCentralBaseBlock',rect(.140,-.140,.140,.030),.213,.345,0)
 # Thick square outer mast with an actual complete through bore at its top.
 union_boxes('WholeOuterBoredMast',[((-.075,-.070,.292),(-.050,.070,1.655)),((.050,-.070,.292),(.075,.070,1.655)),((-.050,-.070,.292),(.050,-.047,1.655)),((-.050,.047,.292),(.050,.070,1.655))],0)
 box('WholeInsetRaisedInnerMast',(-.042,-.039,1.365),(.042,.039,2.245),1)
 # Full transverse retaining pin links the static nested sections; no adjustment claimed.
 rod('WholeFixedMastRetainingPin',(-.102,0,1.473),(.115,0,1.473),.014,1)
 radial_profile('WholeRetainingPinHead',(.102,0,1.473),(1,0,0),(0,1,0),[(0,.027),(.035,.027)],2,20)
 union_boxes('WholeSideWinchBracket',[((.063,-.102,.963),(.130,.102,1.229)),((.100,-.102,.960),(.238,.102,1.012)),((.205,-.092,1.002),(.237,.092,1.228))],0)
 radial_profile('WholeWinchDrum',(.123,0,1.134),(1,0,0),(0,1,0),[(0,.095),(.018,.095),(.018,.055),(.070,.055),(.070,.095),(.088,.095)],1,32)
 rod('WholeWinchThroughShaft',(.085,0,1.134),(.302,0,1.134),.022,1)
 radial_profile('WholeLargeHandwheelRim',(.294,0,1.134),(1,0,0),(0,1,0),[(-.015,.211),(-.015,.239),(.015,.239),(.015,.211)],0,48,True)
 radial_profile('WholeHandwheelHub',(.273,0,1.134),(1,0,0),(0,1,0),[(0,.046),(.044,.046)],1,24)
 for i in range(3):
  a=i*math.tau/3;beam('WholeHandwheelSpoke'+str(i),(.294,.025*math.cos(a),1.134+.025*math.sin(a)),(.294,.224*math.cos(a),1.134+.224*math.sin(a)),.024,.022,1)
 rod('WholeHandwheelOffsetGrip',(.295,-.192,1.134),(.410,-.192,1.134),.024,2)
 # Open clevis and fixed transverse pivot carry the full tilted H cradle.
 union_boxes('WholeTopOpenClevis',[((-.102,-.075,2.208),(-.067,.075,2.350)),((.067,-.075,2.208),(.102,.075,2.350)),((-.102,-.075,2.208),(.102,.075,2.245))],0)
 rod('WholeCradlePivot',(-.137,0,2.306),(.137,0,2.306),.027,1)
 a=math.radians(18)
 def tilt(p):x,y,z=p;return(x,y*math.cos(a)-z*math.sin(a),2.306+y*math.sin(a)+z*math.cos(a))
 box('WholeCradlePivotRoot',(-.062,-.071,-.020),(.062,.071,.104),1,tilt)
 box('WholeFullTransverseCradleSpine',(-1.080,-.036,.085),(1.080,.036,.150),0,tilt)
 for side in[-1,1]:
  x=side*.755
  box('WholeCradleCrossRail'+str(side),(x-.037,-.650,.124),(x+.037,.650,.188),0,tilt)
  for y in[-.63,.63]:box('WholeCradleProtectivePad'+str((side,y)),(x-.047,y-.035,.181),(x+.047,y+.035,.205),2,tilt)
  # Continuous hook-shaped finite front stop, not a floating peg.
  union_boxes('WholeCradleFrontStop'+str(side),[((x-.050,-.684,.128),(x+.050,-.604,.157)),((x-.050,-.684,.128),(x+.050,-.654,.276))],1)
  n='WholeCradleFrontStop'+str(side);v,f,m=G[n];G[n]=([tilt(p)for p in v],f,m)
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
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==41
 triangle_count=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons);assert triangle_count==proof['triangles']
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 lo=[min(v[k]for v in points)for k in range(3)];hi=[max(v[k]for v in points)for k in range(3)]
 assert abs(lo[2])<=TOL
 assert len({m for o in parts for m in o.data.materials})==len(PALETTE)
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
 for layer in scene.view_layers:layer.cycles.use_denoising=False
 scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
 scene.render.resolution_x=scene.render.resolution_y=640;scene.render.resolution_percentage=100
 scene.world=scene.world or bpy.data.worlds.new('Neutral fixed empty tilted panel cradle preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,1.35))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(10,-15,9));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'),compress=False)
 def config():return dict(engine=scene.render.engine,samples=scene.cycles.samples,adaptive=scene.cycles.use_adaptive_sampling,cycles_denoise=scene.cycles.use_denoising,view_layer_denoise=[x.cycles.use_denoising for x in scene.view_layers],compositor_nodes=scene.use_nodes,compositing=scene.render.use_compositing,threads_mode=scene.render.threads_mode,threads=scene.render.threads)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'asset':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':41,'mesh_objects':41,'triangles':triangle_count,'materials':len(PALETTE),'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
 qa['native_saved_render_config']=config();qa['render_configs']={}
 if '--geometry-only' not in sys.argv:
  view=sys.argv[sys.argv.index('--tier-single-view')+1]if '--tier-single-view'in sys.argv else 'thumbnail';assert view in ['qa-front','thumbnail']
  scene.cycles.samples=16 if view=='qa-front' else 128;qa['render_configs'][view]=config();scene.render.filepath=str(OUT/(view+'.png'));start=time.monotonic();bpy.ops.render.render(write_still=True);qa['render']={'view':view,'samples':scene.cycles.samples,'seconds':time.monotonic()-start,'original_pixels_reviewed':False}
 (OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if p.exists():files[role]={'path':f'assets/construction/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'construction','style':'source-preserved-low-poly','title':TITLE,'description':'One newly authored complete empty panel-lift-style static exterior. Three low radial outriggers end in complete caster forks, wheels and pivots around one central base. A genuinely bored tall square outer mast surrounds one separate fixed raised inner section with a transverse retaining pin. A complete side bracket carries a flanged drum, through shaft and large three-spoke handwheel with a distinct offset grip. The upper open clevis and full pivot carry one broad tilted H-shaped cradle: an entire cross spine, two whole transverse rails, four small pads and two continuous front stop hooks. No panel, load, cable routing, duplicated old hoist or engine-stand payload. All geometry newly authored; three opaque PBR roles, metres Z up and whole ground-centred bounds. One prop zero scenes. Fixed visual display only: no wheel motion, telescoping travel, winch transmission, brake, board fit, lifting, load capacity, stability, construction use, installation, manufacture or safety claim. Rigging animation interaction not made.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
