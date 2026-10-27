import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='music-fixed-perforated-ovoid-slat-and-coiled-cord-01'
TITLE='Fixed Perforated Ovoid Slat and Coiled Cord'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholePlainSlatWarmWood',(.37,.18,.075,1),.70),('WholeSlatBevelEndGrain',(.27,.12,.044,1),.76),('WholeLongCordFlax',(.59,.48,.29,1),.84),('WholeFixedEyeTieFlax',(.46,.35,.19,1),.83)]
G={}

def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def add(a,b):return tuple(a[i]+b[i]for i in range(3))
def mul(a,s):return tuple(x*s for x in a)
def sub(a,b):return tuple(a[i]-b[i]for i in range(3))
def unit(a):
 l=math.sqrt(sum(x*x for x in a));assert l>1e-12;return mul(a,1/l)
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def sweep(name,path,radius,mat,closed=False):
 N=12;phase=math.pi/N;v=[]
 for k,p in enumerate(path):
  a=path[k-1]if k or closed else path[0];b=path[(k+1)%len(path)]if k+1<len(path)or closed else path[-1];t=unit(sub(b,a));n=unit((-t[1],t[0],0))if math.hypot(t[0],t[1])>1e-8 else(1,0,0);w=cross(t,n)
  v.extend(add(p,add(mul(n,radius*math.cos(math.tau*j/N+phase)),mul(w,radius*math.sin(math.tau*j/N+phase))))for j in range(N))
 fs=[]
 if not closed:fs=[tuple(reversed(range(N))),tuple((len(path)-1)*N+i for i in range(N))]
 for k in range(len(path)if closed else len(path)-1):
  q=(k+1)%len(path)
  fs.extend((k*N+i,k*N+(i+1)%N,q*N+(i+1)%N,q*N+i)for i in range(N))
 record(name,v,fs,mat)
def make_geometry():
 G.clear();N=128;cx,cy=0.,.111;rx,ry=.032,.145
 # Matching radial annuli around a genuinely empty end eye, with one whole bevelled slat.
 outer=[]
 for i in range(N):
  a=math.tau*i/N;ux,uy=math.cos(a),math.sin(a);A=(ux/rx)**2+(uy/ry)**2;B=2*cy*uy/ry**2;C=(cy/ry)**2-1;t=(-B+math.sqrt(B*B-4*A*C))/(2*A);outer.append((ux*t,cy+uy*t))
 rings=[]
 for kind,z in [('inner',0),('bottom',0),('outer',.0015),('outer',.0065),('bottom',.008),('inner',.008)]:
  row=[]
  for i,p in enumerate(outer):
   a=math.tau*i/N;u=(math.cos(a),math.sin(a));rr=.006 if kind=='inner'else math.hypot(p[0],p[1]-cy)-(.0013 if kind=='bottom'else 0)
   row.append((rr*u[0],cy+rr*u[1],z))
  rings.append(row)
 v=[p for row in rings for p in row];fs=[];m=[]
 for k in range(6):
  q=(k+1)%6
  for i in range(N):j=(i+1)%N;fs.append((k*N+i,k*N+j,q*N+j,q*N+i));m.append(0 if k in[0,4]else 1)
 record('WholeBevelledOvoidSlatAndTrueEndBore',v,fs,m)
 # One complete small fixed knot-like collar: it seats into the bore rim, not a painted knot.
 path=[(.0062*math.cos(math.tau*i/48),cy+.0062*math.sin(math.tau*i/48),.0087+.0005*math.sin(2*math.tau*i/48))for i in range(48)]
 sweep('WholeFixedEndEyeCordTie',path,.0015,3,True)
 # Capped cord end is deliberately seated inside the actual bore wall. Its whole long tail
 # rises through the eye, crosses the tie, descends beyond the slat, and lies in an open spiral.
 R=.0012;floor=R*math.cos(math.pi/12)
 ctrl=[(.0053,cy,.004),(.0053,cy,.007),(.005,cy+.003,.0105),(.003,cy+.006,.010),(.001,cy+.013,.0105),(0,.143,.011),(0,.162,.003),(0,.18,floor),(.009,.202,floor),(.026,.216,floor)]
 path=[]
 for k in range(len(ctrl)-1):
  a=ctrl[max(0,k-1)];b=ctrl[k];c=ctrl[k+1];d=ctrl[min(len(ctrl)-1,k+2)]
  for j in range(8):
   t=j/8;path.append(tuple(.5*((2*b[i])+(-a[i]+c[i])*t+(2*a[i]-5*b[i]+4*c[i]-d[i])*t*t+(-a[i]+3*b[i]-3*c[i]+d[i])*t*t*t)for i in range(3)))
 # Keep the grounded part exactly planar; interpolation cannot produce a hidden floor undershoot.
 path=[(x,y,max(floor,z))for x,y,z in path]
 # Tangent-compatible outside lead into 1.75 laid-out spiral turns; no detached coil pieces.
 path.append(ctrl[-1]);center=(.026,.273);start=-math.pi/2
 for j in range(1,177):
  u=j/176;theta=start+u*math.tau*1.75;r=.057-.024*u;path.append((center[0]+r*math.cos(theta),center[1]+r*math.sin(theta),floor))
 global CORD_PATH
 CORD_PATH=path
 sweep('WholeEndBoreToOpenCoilCord',path,R,2)
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole slat and cord preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.005))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(3.0,-4.3,9.0));bpy.context.view_layer.update()
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored plain complete static bullroarer-inspired visual unit. A long ovoid wooden-look slat is a single closed bevelled solid with a genuine end bore. One complete narrow flax-look cord has a fixed end seated inside the bore, passes through a compact knot-like eye tie, and extends beyond the slat into a continuous open ground coil. Broad flat slat underside and finite cord facets share the ground datum. All outlines, eye, tie and winding coordinates are original numerical construction; no castanet shells, whistle body, yo-yo or recovered cord meshes reused. Four opaque PBR roles, metres, native Z up, one whole model and zero scenes. Plain generic appearance only, not a replica of a named culture, sacred object or museum object; no copied motifs. Fixed small assembly overlaps. No cord dynamics, whirling, sound, playability, strength, manufacturing, authenticity or safety capability; no rig or animation.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
