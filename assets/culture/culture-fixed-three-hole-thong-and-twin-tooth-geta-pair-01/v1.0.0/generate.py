import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='culture-fixed-three-hole-thong-and-twin-tooth-geta-pair-01'
TITLE='Fixed Three Hole Thong and Twin Tooth Geta Pair'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeWoodenSoleWarmTop',(.49,.28,.115,1),.73),('WholeWoodenTeethAndSoleSides',(.32,.15,.055,1),.77),('WholePaddedThongsMutedVermilion',(.44,.070,.037,1),.84),('WholeThongBuriedRootsDarkCloth',(.13,.035,.024,1),.88)]
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
HOLES=[(-.006,.006,-.090,-.076),(-.045,-.033,.038,.052),(.033,.045,.038,.052)]
def clip(poly,a,b,c):
 out=[]
 for p,q in zip(poly,poly[1:]+poly[:1]):
  fp=a*p[0]+b*p[1]-c;fq=a*q[0]+b*q[1]-c
  if fp<=1e-12:out.append(p)
  if (fp<0 and fq>0)or(fp>0 and fq<0):
   t=fp/(fp-fq);out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
 clean=[]
 for p in out:
  p=tuple(round(x,10)for x in p)
  if not clean or p!=clean[-1]:clean.append(p)
 if len(clean)>1 and clean[0]==clean[-1]:clean.pop()
 return clean

def sole(name,cx,cy):
 xs=sorted(set([-.055,.055]+[h[i]for h in HOLES for i in[0,1]]));ys=sorted(set([-.132,.132]+[h[i]for h in HOLES for i in[2,3]]));v=[];index={};f=[];m=[];edges={}
 def ix(p,z):
  q=(round(p[0]+cx,10),round(p[1]+cy,10),z)
  if q not in index:index[q]=len(v);v.append(q)
  return index[q]
 for x0,x1 in zip(xs,xs[1:]):
  for y0,y1 in zip(ys,ys[1:]):
   x,y=(x0+x1)/2,(y0+y1)/2
   if any(a<x<b and c<y<d for a,b,c,d in HOLES):continue
   p=[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
   for a,b in[(1,1),(1,-1),(-1,1),(-1,-1)]:p=clip(p,a,b,.175)
   if len(p)<3:continue
   for t in triangulate(p):f.append(tuple(ix(p[i],.065)for i in t));m.append(0);f.append(tuple(ix(p[i],.045)for i in reversed(t)));m.append(1)
   for a,b in zip(p,p[1:]+p[:1]):
    key=tuple(sorted([a,b]))
    if key in edges:del edges[key]
    else:edges[key]=(a,b)
 for a,b in edges.values():f.append((ix(a,.045),ix(b,.045),ix(b,.065),ix(a,.065)));m.append(1)
 record(name,v,f,m)
def tooth(name,cx,cy,y):
 # Each full cross tooth has a broad flat sole and chamfered lower long edges.
 p=[(y-.010,0),(y+.010,0),(y+.014,.006),(y+.014,.048),(y-.014,.048),(y-.014,.006)];v=[(cx+x,cy+yy,z)for x in[-.049,.049]for yy,z in p];N=len(p);f=[tuple(reversed(range(N))),tuple(N+i for i in range(N))]+[(i,(i+1)%N,(i+1)%N+N,i+N)for i in range(N)];record(name,v,f,1)
def tube(name,path,cx,cy):
 # Whole closed padded strap, parallel-transport frame, varying width/depth only along this original path.
 N=12;v=[];last=None
 for j,(x,y,z,ru,rv)in enumerate(path):
  a=path[max(j-1,0)];b=path[min(j+1,len(path)-1)];w=[b[k]-a[k]for k in range(3)];le=math.sqrt(sum(q*q for q in w));w=[q/le for q in w]
  if last is None:u=[1.,0.,0.]
  else:u=last[:]
  dot=sum(u[k]*w[k]for k in range(3));u=[u[k]-dot*w[k]for k in range(3)];le=math.sqrt(sum(q*q for q in u));assert le>1e-8;u=[q/le for q in u];last=u;vv=[w[1]*u[2]-w[2]*u[1],w[2]*u[0]-w[0]*u[2],w[0]*u[1]-w[1]*u[0]]
  for i in range(N):
   t=math.tau*i/N;q=[p+ru*u[k]*math.cos(t)+rv*vv[k]*math.sin(t)for k,p in enumerate((x,y,z))];v.append((q[0]+cx,q[1]+cy,q[2]))
 f=[tuple(reversed(range(N))),tuple((len(path)-1)*N+i for i in range(N))];m=[3,3]
 for j in range(len(path)-1):
  for i in range(N):f.append((j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i));m.append(3 if path[j][2]<.052 and path[j+1][2]<.052 else 2)
 record(name,v,f,m)
def one_geta(label,cx,cy):
 sole(label+'WholeThreeThroughHoleSoleBoard',cx,cy)
 for n,y in[('Front',-.054),('Rear',.083)]:tooth(label+'Whole'+n+'TransverseTooth',cx,cy,y)
 path=[(-.039,.045,.039,.008,.008),(-.039,.045,.047,.008,.008),(-.039,.045,.053,.0038,.0038),(-.039,.045,.069,.0038,.0038),(-.037,.037,.082,.008,.0045),(-.029,.014,.098,.010,.0045),(-.018,-.023,.109,.010,.0045),(-.007,-.060,.108,.009,.0045),(0,-.075,.104,.008,.0045),(.007,-.060,.108,.009,.0045),(.018,-.023,.109,.010,.0045),(.029,.014,.098,.010,.0045),(.037,.037,.082,.008,.0045),(.039,.045,.069,.0038,.0038),(.039,.045,.053,.0038,.0038),(.039,.045,.047,.008,.008),(.039,.045,.039,.008,.008)]
 tube(label+'WholePaddedVThongAndTwoFlaredRoots',path,cx,cy)
 tube(label+'WholeForwardToePostAndFlaredRoot',[(0,-.083,.039,.008,.008),(0,-.083,.047,.008,.008),(0,-.083,.053,.0034,.0034),(0,-.083,.077,.0034,.0034),(0,-.075,.105,.0034,.0034)],cx,cy)
def make_geometry():
 G.clear();one_geta('Left_',-.074,-.010);one_geta('Right_',.074,.010);pts=[p for v,f,m in G.values()for p in v];lo=[min(p[k]for p in pts)for k in range(3)];hi=[max(p[k]for p in pts)for k in range(3)]
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole wooden geta pair preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.058))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(4.2,-6.5,5.6));bpy.context.view_layer.update()
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
  if p.exists():files[role]={'path':f'assets/culture/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'culture','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete matched pair of geta-inspired wooden sandal exteriors, counted together as one independent prop rather than two assets. Each whole thick chamfer-corner sole board has three real bounded through holes and rests on two full transverse wooden teeth with finite flat lower faces. One entire padded V-shaped thong rises clear of the board and returns through both rear holes; its two flared buried roots meet the board internally. A whole separate front toe post passes through the third hole and meets the V apex, also with a flared fixed lower root. Space remains under the straps and around the narrow stems inside the upper holes. Both complete sandals are set apart by a genuine empty gap in a slightly staggered but unchanged-size pose. All board boundaries, three-hole topology, full teeth, padded paths and roots are new numerical geometry, not the inclined heel-fork boot jack with a strap added and not a snowshoe stripped of its web. The boot jack has an open front fork, sloping board, liner and rear standing pad; the snowshoe has an oval tube, two open web fields, heel cup and traction teeth. Neither supplies this whole closed-perimeter sole and three-point thong organization. Ten closed editable whole meshes, four opaque constant PBR roles, metres native Z up and complete pair horizontal bounds centred. One model zero scenes, no separate stand or surroundings. Generic unmarked cultural footwear appearance only; not a particular museum pair, child or adult size, branded product, regional costume specification or historical replica. No person, foot, fit, wearable flexibility, fastening operation, gait, sound, comfort, grip, strength, stability, manufacturing or safety capability. Static hidden root overlaps are visual connections, not functional joinery or knot construction. No rig, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
