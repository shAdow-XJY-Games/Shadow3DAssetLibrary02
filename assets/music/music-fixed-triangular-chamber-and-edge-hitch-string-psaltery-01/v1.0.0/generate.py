import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='music-fixed-triangular-chamber-and-edge-hitch-string-psaltery-01'
TITLE='Fixed Triangular Chamber and Edge Hitch String Psaltery'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeTriangularSoundboardHoneyWood',(.51,.29,.105,1),.76),('WholeChamberWallsAndBaseBridgeDarkWood',(.17,.080,.029,1),.77),('WholePerimeterAndBasePinsSatinSteel',(.37,.42,.41,1),.48),('WholeUnequalLengthStringsWarmPaleAlloy',(.69,.67,.55,1),.50)]
G={}

def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def body_shell():
 outer=[(-.160,-.250),(.160,-.250),(0,.350)];c=(0,.020);normals=[]
 for a,b in zip(outer,outer[1:]+outer[:1]):
  nx,ny=-(b[1]-a[1]),b[0]-a[0];q=math.hypot(nx,ny);nx/=q;ny/=q;normals.append((nx,ny,nx*a[0]+ny*a[1]))
 inner=[]
 for k,(a,b,q)in enumerate(normals):
  d,e,r=normals[k-1];q+=.006;r+=.006;det=a*e-b*d;inner.append(((q*e-b*r)/det,(a*r-q*d)/det))
 angles=sorted(set([round(math.tau*j/72,12)for j in range(72)]+[round(math.atan2(y-c[1],x-c[0])%math.tau,12)for x,y in outer+inner]));N=len(angles)
 def radius(a,margin):
  dx,dy=math.cos(a),math.sin(a);hits=[]
  for nx,ny,q in normals:
   den=nx*dx+ny*dy
   if den< -1e-12:hits.append((nx*c[0]+ny*c[1]-q-margin)/(-den))
  return min(hits)
 v=[];rows=[]
 for role,z in [('outer',0),('outer',.050),('hole',.050),('hole',.045),('inner',.045),('inner',.006),('point',.006),('point',0)]:
  ids=[]
  if role=='point':ids=[len(v)];v.append((c[0],c[1],z))
  else:
   for a in angles:
    r=.026 if role=='hole'else radius(a,.006 if role=='inner'else 0);ids.append(len(v));v.append((c[0]+r*math.cos(a),c[1]+r*math.sin(a),z))
  rows.append(ids)
 f=[];m=[]
 for k,(a,b)in enumerate(zip(rows,rows[1:]+rows[:1])):
  if len(a)==len(b)==1:continue
  mat=0 if k in[1,3,5,7]else 1
  for i in range(N):
   j=(i+1)%N
   if len(a)==1:f.append((a[0],b[j],b[i]))
   elif len(b)==1:f.append((a[i],a[j],b[0]))
   else:f.append((a[i],a[j],b[j],b[i]))
   m.append(mat)
 record('WholeTriangularHollowChamberAndRealSoundHole',v,f,m)
def cylinder(name,x,y,z0,z1,r,mat,N=12):
 v=[(x+r*math.cos(math.tau*i/N),y+r*math.sin(math.tau*i/N),z)for z in[z0,z1]for i in range(N)];f=[tuple(reversed(range(N))),tuple(N+i for i in range(N))]+[(i,(i+1)%N,(i+1)%N+N,i+N)for i in range(N)];record(name,v,f,mat)
def full_string(name,path):
 N=8;v=[]
 for k,p in enumerate(path):
  a=path[max(0,k-1)];b=path[min(len(path)-1,k+1)];dy,dz=b[1]-a[1],b[2]-a[2];le=math.hypot(dy,dz);u=(0,dz/le,-dy/le)
  for i in range(N):
   q=math.tau*i/N;v.append((p[0]+.0008*math.cos(q),p[1]+.0008*u[1]*math.sin(q),p[2]+.0008*u[2]*math.sin(q)))
 f=[tuple(reversed(range(N))),tuple((len(path)-1)*N+i for i in range(N))]+[(k*N+i,k*N+(i+1)%N,(k+1)*N+(i+1)%N,(k+1)*N+i)for k in range(len(path)-1)for i in range(N)];record(name,v,f,3)
def make_geometry():
 G.clear();body_shell()
 v=[(x,y,z)for z in[.048,.067]for y in[-.211,-.199]for x in[-.137,.137]];record('WholeSingleBaseStringBridge',v,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],1)
 for j in range(14):
  x=-.117+j*.018;end=.350-3.75*abs(x)-.020
  cylinder('WholeBaseTuningPin_%02d'%j,x,-.233,.044,.066,.0022,2)
  cylinder('WholeSlopingPerimeterHitchPin_%02d'%j,x,end,.044,.079,.0022,2)
  full_string('WholeUnequalLengthParallelString_%02d'%j,[(x,-.233,.062),(x,-.205,.0668),(x,end,.073)])
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
 d['materials'][2]['pbrMetallicRoughness']['metallicFactor']=.55
 d['materials'][3]['pbrMetallicRoughness']['metallicFactor']=.30
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole triangular psaltery preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.035))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(3.8,-5.5,6.3));bpy.context.view_layer.update()
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete static bowed-psaltery-inspired instrument. One full low triangular hollow chamber includes its entire flat bottom, thick perimeter walls, thin upper soundboard and genuine round sound hole. Fourteen whole parallel unequal-length strings begin at a single base pin row, rise across one whole short base bridge, and end separately on tall hitch posts distributed along both converging perimeter edges. The successive exposed string endpoints form the characteristic stepped edge field; no central bank of bridges or cross-string buttons is present. Each complete pin and continuous string is original closed geometry. Unlike the paired transverse courses across two internal dulcimer bridges, the full-length arched zither with individual middle bridges, or a rectangular chord-bar instrument, this support relation terminates the strings at the sloping edge posts rather than carrying them across the entire body between two opposed end banks. Every visible numeric coordinate and complete shell topology is newly authored; no prior instrument mesh imported, cropped, resized or recoloured. Forty-four whole closed component meshes, four opaque constant PBR roles, metres native Z up and whole horizontal-bounds-centred flat ground datum. One complete model zero scenes; strings and pins are not separately counted. Plain generic category art, not a measured instrument or historical replica. Symmetric sparse string layout and thick wires are deliberately uncalibrated visual simplifications, not a chromatic keyboard or tuned scale. Strings cross above parts of the actual sound hole, leaving real visible spaces; the chamber is not a solid box or black decal. No bow, player, string windings, note markings, sound, tuning, vibration, tension, bow access performance, acoustics, playability, physical strength, manufacture or safety capability made or verified. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
