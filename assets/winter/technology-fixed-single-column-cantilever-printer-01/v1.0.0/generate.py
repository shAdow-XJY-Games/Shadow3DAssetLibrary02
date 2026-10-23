'One newly authored complete single-column cantilever 3D-printer-style exterior: four feet and low base, one front-open vertical guide tower and fixed carriage, a true front-slotted one-sided crossrail, suspended fan-hood head and tapered nozzle above an independent lower Y-rail build bed, a side-supported complete bored double-flange material spool with a continuous fixed feed line, plus blank control wedge. All numeric geometry newly authored without old gantry, paper printer or cable-reel payload. Static opaque low-poly game-art only, one complete model zero scenes; no kinematics, printing, thermal or electrical operation, nozzle flow, calibration, fabrication, strength or safety claim.'
import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='technology-fixed-single-column-cantilever-printer-01'
TITLE='Fixed Single-Column Cantilever Printer'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('FrameGraphite',(.10,.14,.15,1),.64),('GuideSatin',(.43,.48,.47,1),.44),('CarrierMutedTeal',(.055,.34,.33,1),.60),('DarkBedAndControls',(.035,.045,.045,1),.70)]
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
 for x in[-.185,.185]:
  for y in[-.175,.175]:box('WholeGroundFoot_%s_%s'%(x,y),(x-.025,y-.025,0),(x+.025,y+.025,.024),3)
 prism('WholeLowPrinterBase',rect(.23,-.22,.22,.025),.018,.075,0)
 # Single front-open vertical guide column, not a two-sided overhead gantry.
 union_boxes('WholeOpenGuideColumn',[((-.185,.115,.065),(-.125,.135,.620)),((-.185,.080,.065),(-.172,.135,.620)),((-.138,.080,.065),(-.125,.135,.620)),((-.185,.080,.065),(-.125,.135,.095)),((-.185,.080,.590),(-.125,.135,.620))],0)
 box('WholeVerticalGuideRail',(-.160,.084,.090),(-.150,.121,.601),1)
 union_boxes('WholeFixedVerticalCarriage',[((-.193,.063,.352),(-.117,.083,.430)),((-.193,.063,.352),(-.174,.117,.430)),((-.136,.063,.352),(-.117,.117,.430))],2)
 # Full horizontal front-slotted cantilever rail extends to only one side.
 union_boxes('WholeSlottedCantileverRail',[((-.184,.056,.370),(.200,.075,.405)),((-.184,.025,.370),(.200,.075,.381)),((-.184,.025,.394),(.200,.075,.405))],1)
 box('WholeHeadCarriageBack',(.022,.003,.346),(.098,.042,.430),2)
 def lathe(name,profile,mat,N=24,tr=None):
  v=[];rings=[];f=[]
  for r,z in profile:
   ring=[]
   for i in range(N if r else 1):ring.append(len(v));p=(r*math.cos(math.tau*i/N),r*math.sin(math.tau*i/N),z);v.append(tr(p)if tr else p)
   rings.append(ring)
  for aa,bb in zip(rings,rings[1:]+rings[:1]):
   if len(aa)==len(bb)==1:continue
   for i in range(N):
    j=(i+1)%N;f.append((aa[0],bb[j],bb[i])if len(aa)==1 else((aa[i],aa[j],bb[0])if len(bb)==1 else(aa[i],aa[j],bb[j],bb[i])))
  record(name,v,f,mat)
 F=lambda p:(.060+p[0],-p[2],.382+p[1])
 lathe('WholeOpenFrontFanHood',[(.023,-.009),(.037,-.009),(.037,.043),(.023,.043)],0,24,F)
 cyl('WholeFixedFanHub',(.060,-.013,.382),.008,.051,1,3,16)
 for k in range(5):
  a=math.tau*k/5
  def Q(p,a=a):x,z,y=p;return(.060+x*math.cos(a)-z*math.sin(a),y,.382+x*math.sin(a)+z*math.cos(a))
  box('WholeFixedFanBlade%d'%k,(.006,-.003,-.029),(.027,.003,-.022),3,Q)
 box('WholeNozzleBlock',(.044,-.018,.322),(.076,.016,.354),1)
 lathe('WholeFixedTaperedNozzle',[(0,.299),(.003,.299),(.012,.316),(.012,.328),(0,.328)],2,16,lambda p:(.060+p[0],-.002+p[1],p[2]))
 # Lower Y rails and an independent flat build-bed carriage, no printed object.
 for k,x in enumerate([-.075,.075]):box('WholeBedYRail%d'%k,(x-.009,-.200,.070),(x+.009,.157,.097),1)
 box('WholeBedCarriage',(-.110,-.172,.091),(.110,.105,.114),0)
 for k,(x,y)in enumerate([(-.105,-.150),(.105,-.150),(-.105,.075),(.105,.075)]):cyl('WholeBedStandoff%d'%k,(x,y,.122),.009,.032,2,2,12)
 box('WholeBuildPlate',(-.142,-.202,.132),(.142,.112,.145),1)
 box('WholeBlankBuildSurface',(-.137,-.197,.143),(.137,.107,.149),3)
 # One fixed low angled control housing, blank display and one knob.
 p=rect(.040,-.067,.067,.009);v=[(.180+x,-.115+y,.072)for x,y in p]+[(.180+x,-.115+y,.124+.24*y)for x,y in p];n=len(p);record('WholeAngledControlHousing',v,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],0)
 C=1/math.sqrt(1+.24**2);S=.24*C
 def T(p):x,y,z=p;return(.180+x,-.102+C*y-S*z,.128+S*y+C*z)
 box('WholeBlankControlInset',(-.029,-.030,-.003),(.029,.030,.003),3,T)
 cyl('WholeControlKnob',(.180,-.164,.118),.012,.015,2,2,16)
 # Side-offset complete spool, actually supported by its bore on the holder axle.
 rod('WholeSpoolHolderAxle',(-.315,.105,.500),(-.165,.105,.500),.012,1,16)
 X=lambda p:(p[2],.105+p[0],.500+p[1])
 lathe('WholeBoredDoubleFlangeSpool',[(.010,-.320),(.105,-.320),(.105,-.309),(.055,-.309),(.055,-.251),(.105,-.251),(.105,-.240),(.010,-.240)],0,32,X)
 lathe('WholeWoundMaterialBand',[(.054,-.307),(.089,-.307),(.089,-.253),(.054,-.253)],2,32,X)
 # One continuous fixed feed line, no filament transport or thermal operation.
 path=[(-.280,.105,.587),(-.279,.105,.612),(-.260,.103,.650),(-.218,.094,.673),(-.160,.080,.674),(-.090,.061,.650),(-.020,.040,.600),(.035,.022,.540),(.060,.020,.485),(.060,.020,.421)]
 v=[];N=8
 for j,p in enumerate(path):
  a=path[max(0,j-1)];b=path[min(len(path)-1,j+1)];w=[b[i]-a[i]for i in range(3)];q=math.sqrt(sum(t*t for t in w));w=[t/q for t in w];ref=(1,0,0)if abs(w[0])<.9 else(0,1,0);u=[w[1]*ref[2]-w[2]*ref[1],w[2]*ref[0]-w[0]*ref[2],w[0]*ref[1]-w[1]*ref[0]];q=math.sqrt(sum(t*t for t in u));u=[t/q for t in u];vv=[w[1]*u[2]-w[2]*u[1],w[2]*u[0]-w[0]*u[2],w[0]*u[1]-w[1]*u[0]]
  v.extend(tuple(p[k]+.0025*(u[k]*math.cos(math.tau*i/N)+vv[k]*math.sin(math.tau*i/N))for k in range(3))for i in range(N))
 f=[tuple(reversed(range(N))),tuple((len(path)-1)*N+i for i in range(N))]+[(k*N+i,k*N+(i+1)%N,(k+1)*N+(i+1)%N,(k+1)*N+i)for k in range(len(path)-1)for i in range(N)];record('WholeFixedFeedLine',v,f,2)
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
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==35
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
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'asset':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':35,'mesh_objects':35,'triangles':triangle_count,'materials':4,'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'technology','style':'source-preserved-low-poly','title':TITLE,'description':'One newly authored complete single-column cantilever 3D-printer-style exterior: four feet and low base, one front-open vertical guide tower and fixed carriage, a true front-slotted one-sided crossrail, suspended fan-hood head and tapered nozzle above an independent lower Y-rail build bed, a side-supported complete bored double-flange material spool with a continuous fixed feed line, plus blank control wedge. All numeric geometry newly authored without old gantry, paper printer or cable-reel payload. Static opaque low-poly game-art only, one complete model zero scenes; no kinematics, printing, thermal or electrical operation, nozzle flow, calibration, fabrication, strength or safety claim.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
