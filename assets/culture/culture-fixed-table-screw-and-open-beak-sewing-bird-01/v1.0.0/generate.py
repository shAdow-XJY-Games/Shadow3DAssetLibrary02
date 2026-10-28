import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='culture-fixed-table-screw-and-open-beak-sewing-bird-01'
TITLE='Fixed Table Screw and Open Beak Sewing Bird'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeCFrameAndBirdMountDeepBronze',(.26,.18,.075,1),.55),('WholeOpposedBirdJawsMutedBrass',(.48,.33,.13,1),.47),('WholeFixedScrewAxleAndTailSpringSteel',(.20,.23,.22,1),.50),('WholePlainEyeStudsDarkMetal',(.045,.045,.038,1),.55)]
G={}

def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def lathe(name,cx,profile,materials,N=48):
 v=[];rows=[];f=[];m=[]
 for r,z in profile:
  ids=[]
  for j in range(1 if r==0 else N):ids.append(len(v));a=math.tau*j/N;v.append((cx+r*math.cos(a),r*math.sin(a),z))
  rows.append(ids)
 for k,(a,b)in enumerate(zip(rows,rows[1:]+rows[:1])):
  if len(a)==len(b)==1:continue
  for j in range(N):
   q=(j+1)%N;f.append((a[0],b[q],b[j])if len(a)==1 else(a[j],a[q],b[0])if len(b)==1 else(a[j],a[q],b[q],b[j]));m.append(materials[k]if isinstance(materials,list)else materials)
 record(name,v,f,m)
def smooth_path(control):
 out=[]
 for j,p1 in enumerate(control[:-1]):
  p0=control[max(j-1,0)];p2=control[j+1];p3=control[min(j+2,len(control)-1)]
  for k in range(4):
   t=k/4;out.append(tuple(.5*(2*p1[a]+(-p0[a]+p2[a])*t+(2*p0[a]-5*p1[a]+4*p2[a]-p3[a])*t*t+(-p0[a]+3*p1[a]-3*p2[a]+p3[a])*t*t*t)for a in range(2)))
 return out+[control[-1]]
def triangles2(poly):
 def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 assert sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(poly,poly[1:]+poly[:1]))>0
 live=list(range(len(poly)));result=[]
 while len(live)>3:
  for k,b in enumerate(live):
   a,c=live[k-1],live[(k+1)%len(live)]
   if cross(poly[a],poly[b],poly[c])<=1e-12:continue
   if any(all(cross(poly[u],poly[v],poly[q])>=-1e-12 for u,v in[(a,b),(b,c),(c,a)])for q in live if q not in[a,b,c]):continue
   result.append((a,b,c));live.pop(k);break
  else:raise AssertionError('Non-simple polygon')
 return result+[tuple(live)]
LOWER=[(-.044,.110),(-.015,.104),(.010,.107),(.032,.115),(.054,.115),(.079,.120),(.079,.125),(.053,.125),(.031,.131),(.011,.133),(-.010,.132),(-.025,.125),(-.044,.123)]
UPPER=[(-.060,.132),(-.023,.124),(-.006,.122),(.013,.130),(.028,.142),(.048,.136),(.077,.136),(.080,.141),(.053,.150),(.047,.158),(.030,.160),(.016,.155),(.004,.143),(-.018,.136),(-.060,.143)]
SPRING=[(-.041,.117),(-.053,.117),(-.059,.121),(-.059,.129),(-.052,.135),(-.042,.136)]
def axis_lathe(name,c,axis,profile,mat,N=32):
 lathe(name,0,[(r,t)for t,r in profile],mat,N);v,f,m=G[name]
 if axis=='X':v=[(c[0]+z,c[1]+x,c[2]+y)for x,y,z in v]
 elif axis=='Y':v=[(c[0]+y,c[1]+z,c[2]+x)for x,y,z in v]
 else:v=[(c[0]+x,c[1]+y,c[2]+z)for x,y,z in v]
 G[name]=(v,f,m)
def extrude(name,p,y0,y1,mat):
 n=len(p);v=[(x,y,z)for y in[y0,y1]for x,z in p];ts=triangles2(p);fs=ts+[tuple(n+i for i in reversed(f))for f in ts]+[(i,n+i,n+(i+1)%n,(i+1)%n)for i in range(n)];record(name,v,fs,mat)
def cframe():
 boxes=[((-.040,-.016,0),(.047,.016,.014)),((-.040,-.016,.014),(-.027,.016,.085)),((-.040,-.016,.078),(.047,.016,.092)),((-.018,-.010,.092),(.005,.010,.110))]
 axes=[sorted(set(p[k]for b in boxes for p in b))for k in range(3)];xs,ys,zs=axes;occupied=set()
 for i in range(len(xs)-1):
  for j in range(len(ys)-1):
   for k in range(len(zs)-1):
    c=((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)
    if any(all(lo[t]<c[t]<hi[t]for t in range(3))for lo,hi in boxes):occupied.add((i,j,k))
 directions=[((-1,0,0),[(0,0,0),(0,0,1),(0,1,1),(0,1,0)]),((1,0,0),[(1,0,0),(1,1,0),(1,1,1),(1,0,1)]),((0,-1,0),[(0,0,0),(1,0,0),(1,0,1),(0,0,1)]),((0,1,0),[(0,1,0),(0,1,1),(1,1,1),(1,1,0)]),((0,0,-1),[(0,0,0),(0,1,0),(1,1,0),(1,0,0)]),((0,0,1),[(0,0,1),(1,0,1),(1,1,1),(0,1,1)])];v=[];fs=[];ix={}
 for i,j,k in sorted(occupied):
  for(di,dj,dk),corners in directions:
   if(i+di,j+dj,k+dk)not in occupied:
    f=[]
    for x,y,z in corners:
     p=(xs[i+x],ys[j+y],zs[k+z])
     if p not in ix:ix[p]=len(v);v.append(p)
     f.append(ix[p])
    fs.append(f)
 record('WholeContinuousCFrameAndUpperMount',v,fs,0)
def thread():
 path=[(.025+.0045*math.cos(a),.0045*math.sin(a),.016+.006*a/math.tau)for a in[math.tau*4*i/96 for i in range(97)]];N=8;v=[]
 for k,c in enumerate(path):
  a=math.tau*4*k/96;u=(math.cos(a),math.sin(a),0);t=(-.0045*math.sin(a),.0045*math.cos(a),.006/math.tau);le=math.sqrt(sum(q*q for q in t));t=tuple(q/le for q in t);w=(t[1]*u[2]-t[2]*u[1],t[2]*u[0]-t[0]*u[2],t[0]*u[1]-t[1]*u[0])
  for j in range(N):
   b=math.tau*j/N;v.append(tuple(c[d]+.0011*(u[d]*math.cos(b)+w[d]*math.sin(b))for d in range(3)))
 fs=[tuple(reversed(range(N))),tuple((len(path)-1)*N+j for j in range(N))]+[(k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j)for k in range(len(path)-1)for j in range(N)];record('WholeCappedFourTurnThreadRidge',v,fs,2)
def leaf_spring():
 path=smooth_path(SPRING);v=[]
 for k,(x,z)in enumerate(path):
  a=path[max(k-1,0)];b=path[min(k+1,len(path)-1)];dx,dz=b[0]-a[0],b[1]-a[1];le=math.hypot(dx,dz);normal=(dz/le,-dx/le)
  for sy,sn in[(-1,-1),(1,-1),(1,1),(-1,1)]:v.append((x+normal[0]*sn*.00085,sy*.0045,z+normal[1]*sn*.00085))
 fs=[(3,2,1,0),tuple((len(path)-1)*4+j for j in range(4))]+[(k*4+j,k*4+(j+1)%4,(k+1)*4+(j+1)%4,(k+1)*4+j)for k in range(len(path)-1)for j in range(4)];record('WholeCurvedTailLeafSpring',v,fs,2)
def make_geometry():
 G.clear();cframe()
 axis_lathe('WholeClampShaftAndPressurePad',(.025,0,0),'Z',[(.003,0),(.003,.004),(.042,.004),(.043,.011),(.049,.012),(.051,.009),(.051,0)],2,32)
 thread();axis_lathe('WholeFlaredCrossHandle',(.025,0,.007),'X',[(-.045,0),(-.045,.004),(-.040,.004),(-.038,.0025),(.038,.0025),(.040,.004),(.045,.004),(.045,0)],2,24)
 extrude('WholeFixedLowerBirdBodyAndBeak',LOWER,-.011,.011,1);extrude('WholeRaisedUpperBirdHeadAndTail',UPPER,-.009,.009,1)
 axis_lathe('WholeFixedTransverseJawAxle',(-.010,0,.128),'Y',[(-.018,0),(-.018,.005),(-.014,.005),(-.012,.0035),(.012,.0035),(.014,.005),(.018,.005),(.018,0)],2,24)
 leaf_spring()
 for side,label in[(-1,'Front'),(1,'Back')]:axis_lathe('Whole'+label+'PlainEyeStud',(.037,0,.151),'Y',[(side*.0085,0),(side*.0085,.002),(side*.0105,.0023),(side*.0115,0)],3,16)
 pts=[p for v,f,m in G.values()for p in v];lo=[min(p[k]for p in pts)for k in range(3)];hi=[max(p[k]for p in pts)for k in range(3)]
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
 for i,material in enumerate(d['materials']):material['pbrMetallicRoughness']['metallicFactor']=[.65,.70,.65,.35][i]
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole sewing bird clamp preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.080))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(3.0,-8.5,3.8));bpy.context.view_layer.update()
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'culture','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete sewing-bird-inspired craft clamp in a fixed open pose. A single continuous C-shaped table-edge frame includes its upper bird mount and a finite flat lower resting surface. A complete vertical shaft with integral pressure pad, one capped four-turn helical ridge and one flared transverse handle occupy the lower jaw; a real empty table gap remains beneath the upper arm. The complete stationary lower bird body and raised upper bird head/tail meet a whole transverse axle, with an actual open gap between their blunt beak tips. One entire curved flat tail spring joins the rear portions, and two plain small eye studs make the simple unornamented bird outline readable. Every full profile, curve, jaw outline, support and screw coordinate is newly authored. Unlike the clamp-on bench vise there is no sliding front flat jaw, rectangular slide guide or second long screw translating the work jaws; unlike the clothespin basket there is no basket or three repeated opposed wooden clips with central coil springs. This complete mount-and-pivoted-bird organization is not old clamp geometry with a bird ornament added or an extracted clothes clip. Ten closed editable whole meshes, four opaque untextured metal-look PBR roles, metres native Z up and whole horizontal-bounds-centred ground origin. One model zero scenes, no extra component count. Plain broad category inspiration only, not a museum-object replica, patented mechanism, historical proportion, branded sewing aid or copied feather ornament. The apparent hinge, helical ridge and flat spring are fixed visual geometry with explicit finite attachment overlaps, not a working fit, spring law or tested movement. No tabletop or cloth is supplied; the lower C-frame resting surface is only a neutral static display datum, not a claim of freestanding balance or actual clamping. No gripping force, thread pitch compatibility, opening travel, needlework performance, pinch protection, load, manufacture, handling or safety capability supplied. No rig, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
