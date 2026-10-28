import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='music-fixed-cambered-stick-and-frog-held-hair-bow-01'
TITLE='Fixed Cambered Stick and Frog Held Hair Bow'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeCamberedStickAndHeadWarmWood',(.36,.15,.048,1),.64),('WholeHollowMouthFrogAndGripDarkTimber',(.067,.054,.042,1),.72),('WholeContinuousFiniteHairRibbonIvory',(.78,.74,.60,1),.80),('WholeFerruleAndButtonMutedSteel',(.42,.45,.43,1),.48)]
G={}

def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def triangulate(poly):
 def cross(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 ids=list(range(len(poly)));out=[]
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(poly,poly[1:]+poly[:1]))<0:ids.reverse()
 while len(ids)>3:
  for k,b in enumerate(ids):
   a,c=ids[k-1],ids[(k+1)%len(ids)]
   if cross(poly[a],poly[b],poly[c])<=1e-14:continue
   if any(min(cross(poly[a],poly[b],poly[j]),cross(poly[b],poly[c],poly[j]),cross(poly[c],poly[a],poly[j]))>=-1e-14 for j in ids if j not in[a,b,c]):continue
   out.append((a,b,c));ids.pop(k);break
  else:raise AssertionError('Untriangulable authored polygon')
 return out+[tuple(ids)]
def prism(name,poly,a,b,mat,axis='Z'):
 if sum(x[0]*y[1]-x[1]*y[0]for x,y in zip(poly,poly[1:]+poly[:1]))<0:poly=list(reversed(poly))
 n=len(poly);v=[(x,y,z)if axis=='Z'else(x,z,y)for z in[a,b]for x,y in poly];top=triangulate(poly);fs=[tuple(reversed(q))for q in top]+[tuple(i+n for i in q)for q in top]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];record(name,v,fs,mat)
def ystick(x):return .014-.017*(1-(x/.355)**2)
def rstick(x):return .0042-.0016*(x+.355)/.710
def cambered_stick():
 N=12;v=[];sections=37
 for k in range(sections):
  x=-.355+.710*k/(sections-1);y=ystick(x);r=rstick(x);dy=.034*x/(.355**2);le=math.hypot(1,dy);w=(dy/le,-1/le,0)
  for j in range(N):
   a=math.tau*j/N;v.append((x+r*w[0]*math.sin(a),y+r*w[1]*math.sin(a),.011+r*math.cos(a)))
 f=[tuple(reversed(range(N))),tuple((sections-1)*N+j for j in range(N))]+[(k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j)for k in range(sections-1)for j in range(N)];record('WholeTaperedCamberedStick',v,f,0)
def rect(y0,y1,z0,z1,r):return[(y0+r,z0),(y1-r,z0),(y1,z0+r),(y1,z1-r),(y1-r,z1),(y0+r,z1),(y0,z1-r),(y0,z0+r)]
def frog():
 outer=rect(-.024,.016,0,.022,.003);inner=rect(-.021,-.017,.003,.015,.0007);v=[];rows=[]
 for p,x in[(outer,-.325),(outer,-.245),(inner,-.245),(inner,-.295),([(-.019,.009)],-.295),([(-.019,.009)],-.325)]:
  ids=[]
  for y,z in p:ids.append(len(v));v.append((x,y,z))
  rows.append(ids)
 f=[]
 for a,b in zip(rows,rows[1:]+rows[:1]):
  if len(a)==len(b)==1:continue
  for i in range(8):
   j=(i+1)%8
   if len(a)==1:f.append((a[0],b[j],b[i]))
   elif len(b)==1:f.append((a[i],a[j],b[0]))
   else:f.append((a[i],a[j],b[j],b[i]))
 record('WholeChamferedFrogWithBlindHairMouth',v,f,1)
def ferrule():
 outer=rect(-.0255,-.0155,.0015,.0165,.001);inner=rect(-.0214,-.0166,.0026,.0154,.0006);v=[(x,y,z)for x in[-.258,-.242]for p in[outer,inner]for y,z in p];N=8;f=[]
 for i in range(N):
  j=(i+1)%N;f.extend([(i,j,N+j,N+i),(2*N+i,3*N+i,3*N+j,2*N+j),(i,2*N+i,2*N+j,j),(N+i,N+j,3*N+j,3*N+i)])
 record('WholeOpenHairMouthFerrule',v,f,3)
def button():
 N=12;v=[(x,.014+r*math.cos(math.tau*i/N),.011+r*math.sin(math.tau*i/N))for x,r in[(-.375,.0055),(-.371,.006),(-.357,.006),(-.357,.0027),(-.348,.0027)]for i in range(N)];f=[tuple(reversed(range(N))),tuple(4*N+i for i in range(N))]+[(k*N+i,k*N+(i+1)%N,(k+1)*N+(i+1)%N,(k+1)*N+i)for k in range(4)for i in range(N)];record('WholeEndButtonAndBuriedFixedStem',v,f,3)
def grip():
 N=12;v=[]
 for x,r in[(-.239,.005),(-.190,.005),(-.190,.0035),(-.239,.0035)]:
  for i in range(N):a=math.tau*i/N;v.append((x,ystick(x)+r*math.cos(a),.011+r*math.sin(a)))
 f=[(k*N+i,k*N+(i+1)%N,((k+1)%4)*N+(i+1)%N,((k+1)%4)*N+i)for k in range(4)for i in range(N)];record('WholeShortFixedGripSleeve',v,f,1)
def make_geometry():
 G.clear();cambered_stick();frog();ferrule();button();grip()
 prism('WholeTaperedHeadWithHairSeat',[(.350,.016),(.360,.018),(.373,-.017),(.368,-.024),(.347,-.024),(.351,-.016),(.354,-.009)],0,.022,0)
 # A single whole thick ribbon, not textured alpha hair or simulated fibres; both ends are seated.
 prism('WholeContinuousFiniteHairRibbon',[(-.297,-.020),(.361,-.020),(.361,-.0186),(-.297,-.0186)],.004,.014,2)
 points=[p for v,f,m in G.values()for p in v];lo=[min(p[k]for p in points)for k in range(3)];hi=[max(p[k]for p in points)for k in range(3)]
 global SHIFT
 SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2])
 for n,(v,f,m)in list(G.items()):G[n]=([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)
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
 d['materials'][3]['pbrMetallicRoughness']['metallicFactor']=.45
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
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==len(G)
 triangle_count=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons);assert triangle_count==proof['triangles']
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 lo=[min(v[k]for v in points)for k in range(3)];hi=[max(v[k]for v in points)for k in range(3)]
 assert abs(lo[2])<=TOL
 assert len({m for o in parts for m in o.data.materials})==4
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
 for layer in scene.view_layers:layer.cycles.use_denoising=False
 scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
 scene.render.resolution_x=scene.render.resolution_y=640;scene.render.resolution_percentage=100
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole cambered instrument bow preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.011))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(4.0,-6.0,6.2));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'),compress=False)
 def config():return dict(engine=scene.render.engine,samples=scene.cycles.samples,adaptive=scene.cycles.use_adaptive_sampling,cycles_denoise=scene.cycles.use_denoising,view_layer_denoise=[x.cycles.use_denoising for x in scene.view_layers],compositor_nodes=scene.use_nodes,compositing=scene.render.use_compositing,threads_mode=scene.render.threads_mode,threads=scene.render.threads)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'asset':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':len(G),'mesh_objects':len(G),'triangles':triangle_count,'materials':4,'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
 qa['native_saved_render_config']=config();qa['render_configs']={}
 if '--geometry-only' not in sys.argv:
  view=sys.argv[sys.argv.index('--tier-single-view')+1]if '--tier-single-view'in sys.argv else 'thumbnail';assert view in ['qa-front','thumbnail']
  scene.cycles.samples=16 if view=='qa-front' else 128;qa['render_configs'][view]=config();scene.render.filepath=str(OUT/(view+'.png'));start=time.monotonic();bpy.ops.render.render(write_still=True);qa['render']={'view':view,'samples':scene.cycles.samples,'seconds':time.monotonic()-start,'original_pixels_reviewed':False}
 (OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if p.exists():files[role]={'path':f'assets/music/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete static string-instrument bow accessory, displayed lying on its side. A full tapered cambered stick reaches a separate whole shaped head; a complete dark frog has a genuine blind front hair passage and a whole open ferrule. One continuous finite-thickness pale ribbon runs from its buried frog root to the head seat, retaining clear space from the stick along its exposed span. A whole short grip sleeve and an entire end button with buried fixed stem complete the handle end. Both frog and head have actual finite planar side-rest soles. Unlike the broad central grip and two reflex limbs of the sports bow, this has an asymmetric frog-to-head hair-bearing organization; unlike the large single-string gourd bow, it has no resonator, stave bindings or tip-to-tip round string. All numeric stick route, head, frog cavity, ferrule and fittings are newly authored together. No bow is extracted from a violin or other instrument, and no old stave or cord mesh is reused. Seven closed editable whole meshes, four opaque constant PBR roles, metres native Z up and whole horizontal-bounds-centred ground origin. One independent complete accessory model zero scenes; individual components are not additional assets. Generic unmarked cultural instrument accessory artwork, not a measured historic or branded bow, rare material reconstruction or matched instrument specification. The pale ribbon deliberately stands for a grouped hair appearance, not individual strands or alpha texture. Its fixed seats and button do not establish a working screw, hair tension, flex, camber adjustment, bow friction, sound, balance, playing ergonomics, materials, manufacture or safe handling. No instrument, player, rosin, rigging, animation or interaction is supplied or verified.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
