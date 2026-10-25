'One newly authored complete fixed dental-unit-style equipment exterior, counted as one prop and zero scenes. A low broad grounded pedestal supports one continuous leg-seat-inclined-back shell and thick pad with a separate fixed headrest and open-side arm supports. A physically connected side column carries a true open rinse bowl and curved fixed spout. On the opposite side, two complete fixed support arms carry an empty tray and three short attached hoses with blunt parked handpiece exteriors. A tall mast with two whole angled arms supports an opaque examination-light head and two grip loops over the empty chair. No old chair geometry imported, recoloured or merely reclined. Three constant opaque untextured materials, all parts newly authored and editable. Static unoccupied artistic equipment appearance only: no patient, clinical procedure, diagnosis/treatment, medical suitability, water/plumbing, powered light, electrical function, real mechanism motion, ergonomics, hygiene, load, manufacture or safety certification. Rigging, animation and interaction are not made.'
import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='professional-fixed-reclined-chair-and-connected-dental-unit-01'
TITLE='Fixed Reclined Chair and Connected Dental Unit'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WarmOpaqueUnitShell', [0.63, 0.65, 0.6, 1], 0.68), ('MutedTealChairPads', [0.1, 0.29, 0.3, 1], 0.84), ('DarkFixedHardware', [0.09, 0.12, 0.13, 1], 0.57)]
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
 prism('WholeLowGroundPedestal',rect(.47,-.52,.54,.10),0,.095,2)
 # Broad offset tapered lift housing; frozen appearance, no mechanism claim.
 profile=[(-.28,.087),(.32,.087),(.26,.33),(.09,.55),(-.17,.55),(-.31,.28)]
 v=[(x,y,z)for x in[-.185,.185]for y,z in profile];n=len(profile);f=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];record('WholeOffsetPedestalHousing',v,f,0)
 def bed(name,rows,thick,mat):
  v=[]
  for y,z,w in rows:v +=[(-w,y,z-thick),(w,y,z-thick),(w,y,z),(-w,y,z)]
  f=[(3,2,1,0),tuple(4*(len(rows)-1)+i for i in range(4))]
  for k in range(len(rows)-1):
   for i in range(4):j=(i+1)%4;f.append((k*4+i,k*4+j,(k+1)*4+j,(k+1)*4+i))
  record(name,v,f,mat)
 rows=[(-.86,.515,.205),(-.78,.54,.245),(-.30,.655,.282),(-.12,.665,.300),(.15,.665,.300),(.54,.952,.263),(.68,1.035,.215)]
 bed('WholeContinuousInclinedChairShell',[(y,z-.045,w+.025)for y,z,w in rows],.065,0)
 bed('WholeContinuousLegSeatAndBackPad',[(y+(.004 if i==0 else -.004 if i==len(rows)-1 else 0),z,w)for i,(y,z,w)in enumerate(rows)],.062,1)
 rod('WholeFixedHeadrestStem',(0,.62,.975),(0,.80,1.13),.027,2)
 bed('WholeSeparatePaddedHeadrest',[(.70,1.085,.135),(.78,1.15,.150),(.86,1.165,.132)],.060,1)
 for side in[-1,1]:
  x=side*.355
  whole_curved_hose('WholeOpenSideArmSupport_'+str(side),[(side*.27,-.18,.60),(x,-.18,.70),(x,-.11,.80),(x,.20,.80),(side*.28,.26,.72)],.022,0)
  prism('WholeArmPad_'+str(side),[(x-.043,-.15),(x+.043,-.15),(x+.043,.22),(x-.043,.22)],.790,.835,1)
 # Side unit is physically connected to the pedestal by complete fixed carriers.
 box('WholeLeftUnitGroundCarrier',(-.66,.11,.070),(-.32,.34,.135),0)
 prism('WholeLeftServiceColumn',[(x-.62,y+.23)for x,y in rect(.105,-.115,.115,.025)],.12,.82,0)
 radial_profile('WholeOpenSideRinseBowl',(-.62,.16,.78),(0,0,1),(1,0,0),[(0,.105),(.105,.185),(.150,.185),(.150,.158),(.055,.075)],0,n=32)
 whole_curved_hose('WholeFixedCurvedBowlSpout',[(-.65,.29,.80),(-.65,.29,1.01),(-.65,.24,1.065),(-.65,.14,1.065),(-.65,.10,1.02)],.014,2)
 # Full two-arm delivery table and finite hoses; no instrument tips/sharpness.
 box('WholeRightArmPedestalMount',(.31,.13,.15),(.51,.31,.28),0)
 rod('WholeDeliveryVerticalPivot',(.45,.22,.20),(.45,.22,.78),.045,0)
 rod('WholeDeliveryFirstArm',(.45,.22,.76),(.78,.02,.88),.032,0)
 rod('WholeDeliverySecondArm',(.78,.02,.88),(.73,-.43,.96),.029,0)
 for i,p in enumerate([(.45,.22,.76),(.78,.02,.88),(.73,-.43,.96)]):radial_profile('WholeFixedDeliveryJoint_'+str(i),p,(0,0,1),(1,0,0),[(-.032,.055),(.032,.055)],2,n=20)
 prism('WholeInstrumentTrayBody',[(x+.73,y-.42)for x,y in rect(.225,-.15,.15,.04)],.950,1.000,0)
 prism('WholeBlankTraySurface',[(x+.73,y-.42)for x,y in rect(.195,-.12,.12,.03)],.998,1.011,2)
 for i,x in enumerate([.58,.73,.88]):
  whole_curved_hose('WholeAttachedShortInstrumentHose_'+str(i),[(x,-.55,.968),(x,-.59,.80),(x,-.61,.64),(x+.025,-.65,.59),(x+.050,-.67,.64),(x+.050,-.66,.88)],.009,2)
  rod('WholeBluntParkedHandpiece_'+str(i),(x+.050,-.66,.86),(x+.050,-.66,.99),.016,0)
  box('WholeHandpieceHolder_'+str(i),(x+.024,-.68,.947),(x+.075,-.535,.970),0)
 # High connected articulated light appearance; opaque insert, no emission.
 rod('WholeLightMast',(-.62,.29,.73),(-.62,.29,1.62),.035,0)
 rod('WholeLightUpperArm',(-.62,.29,1.60),(-.20,.34,1.84),.027,0)
 rod('WholeLightForwardArm',(-.20,.34,1.84),(.12,-.18,1.64),.025,0)
 for i,p in enumerate([(-.62,.29,1.60),(-.20,.34,1.84),(.12,-.18,1.64)]):rod('WholeLightFixedAxle_'+str(i),(p[0]-.040,p[1],p[2]),(p[0]+.040,p[1],p[2]),.046,2)
 # Rounded octagonal lamp housing oriented obliquely toward the empty seat.
 u=(1,0,0);v=(0,.60,.80);axis=(0,-.80,.60);c=(.12,-.20,1.60)
 outline=[(-.145,-.080),(.145,-.080),(.185,-.040),(.185,.040),(.145,.080),(-.145,.080),(-.185,.040),(-.185,-.040)]
 def lightplate(name,poly,t0,t1,mat):
  vs=[add(c,add(mul(u,x),add(mul(v,y),mul(axis,t))))for t in[t0,t1]for x,y in poly];n=len(poly);fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];record(name,vs,fs,mat)
 lightplate('WholeOpaqueExamLightHead',outline,-.045,.025,0)
 lightplate('WholeRecessedNonemittingLightFace',[(x*.84,y*.73)for x,y in outline],.023,.029,2)
 for side in[-1,1]:
  p=add(c,mul(u,side*.185));whole_curved_hose('WholeLightSideGrip_'+str(side),[add(p,mul(v,-.035)),add(p,add(mul(u,side*.070),mul(v,-.035))),add(p,add(mul(u,side*.070),mul(v,.035))),add(p,mul(v,.035))],.010,0)
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
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==42
 triangle_count=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons);assert triangle_count==proof['triangles']
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 lo=[min(v[k]for v in points)for k in range(3)];hi=[max(v[k]for v in points)for k in range(3)]
 assert abs(lo[2])<=TOL
 assert len({m for o in parts for m in o.data.materials})==len(PALETTE)
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
 for layer in scene.view_layers:layer.cycles.use_denoising=False
 scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
 scene.render.resolution_x=scene.render.resolution_y=640;scene.render.resolution_percentage=100
 scene.world=scene.world or bpy.data.worlds.new('Neutral fixed dental unit preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.90))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(8,-13,8));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'),compress=False)
 def config():return dict(engine=scene.render.engine,samples=scene.cycles.samples,adaptive=scene.cycles.use_adaptive_sampling,cycles_denoise=scene.cycles.use_denoising,view_layer_denoise=[x.cycles.use_denoising for x in scene.view_layers],compositor_nodes=scene.use_nodes,compositing=scene.render.use_compositing,threads_mode=scene.render.threads_mode,threads=scene.render.threads)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'asset':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':42,'mesh_objects':42,'triangles':triangle_count,'materials':len(PALETTE),'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'professional','style':'source-preserved-low-poly','title':TITLE,'description':'One newly authored complete fixed dental-unit-style equipment exterior, counted as one prop and zero scenes. A low broad grounded pedestal supports one continuous leg-seat-inclined-back shell and thick pad with a separate fixed headrest and open-side arm supports. A physically connected side column carries a true open rinse bowl and curved fixed spout. On the opposite side, two complete fixed support arms carry an empty tray and three short attached hoses with blunt parked handpiece exteriors. A tall mast with two whole angled arms supports an opaque examination-light head and two grip loops over the empty chair. No old chair geometry imported, recoloured or merely reclined. Three constant opaque untextured materials, all parts newly authored and editable. Static unoccupied artistic equipment appearance only: no patient, clinical procedure, diagnosis/treatment, medical suitability, water/plumbing, powered light, electrical function, real mechanism motion, ergonomics, hygiene, load, manufacture or safety certification. Rigging, animation and interaction are not made.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
