import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='timekeeping-fixed-open-twin-leaves-and-cord-gnomon-dial-01'
TITLE='Fixed Open Twin Leaves and Cord Gnomon Dial'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeLeafCutWallsWarmWood',(.29,.16,.065,1),.78),('WholeBlankLeafFacesAndCupFloor',(.69,.60,.41,1),.78),('WholeFixedHingesAndPivotBrass',(.49,.32,.11,1),.48),('WholeCordAndNeedleDark',(.075,.09,.085,1),.80)]
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
def axis_lathe(name,c,axis,profile,mat,N=32):
 lathe(name,0,[(r,t)for t,r in profile],mat,N);v,f,m=G[name]
 if axis=='X':v=[(c[0]+z,c[1]+x,c[2]+y)for x,y,z in v]
 elif axis=='Y':v=[(c[0]+y,c[1]+z,c[2]+x)for x,y,z in v]
 else:v=[(c[0]+x,c[1]+y,c[2]+z)for x,y,z in v]
 G[name]=(v,f,m)
CUP_Y=-.020
CORD=[(0,-.068,.013),(0,.081,.148)]
def lower_leaf():
 angles=sorted(set([math.tau*j/64 for j in range(64)]+[math.atan2(y-CUP_Y,x)%math.tau for x in[-.075,.075]for y in[-.085,.085]]));outer=[];inner=[]
 for a in angles:
  x,y=math.cos(a),math.sin(a);tx=.075/abs(x)if abs(x)>1e-12 else 1e9;ty=((.085-CUP_Y)if y>0 else(-.085-CUP_Y))/y if abs(y)>1e-12 else 1e9;t=min(tx,ty);outer.append((x*t,CUP_Y+y*t));inner.append((.030*x,CUP_Y+.030*y))
 n=len(angles);v=[(x,y,z)for p,z in[(outer,0),(outer,.014),(inner,.014),(inner,.004)]for x,y in p];cb=len(v);v.append((0,CUP_Y,0));cf=len(v);v.append((0,CUP_Y,.004));fs=[];m=[]
 for i in range(n):
  j=(i+1)%n;fs.extend([(cb,j,i),(i,j,n+j,n+i),(n+i,n+j,2*n+j,2*n+i),(2*n+i,2*n+j,3*n+j,3*n+i),(cf,3*n+i,3*n+j)]);m.extend([0,0,1,0,1])
 record('WholeLowerLeafWithTrueBlindCompassCup',v,fs,m)
def upper_leaf():
 v=[(x,y,z)for z in[.010,.170]for y in[.080,.094]for x in[-.075,.075]];fs=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];record('WholeFixedUprightBlankUpperLeaf',v,fs,[0,0,1,0,0,0])
def cord():
 a,b=CORD;dx,dy,dz=[b[k]-a[k]for k in range(3)];le=math.sqrt(dx*dx+dy*dy+dz*dz);u=(1,0,0);w=(0,dz/le,-dy/le);N=12;v=[]
 for c in[a,b]:
  for j in range(N):q=math.tau*j/N;v.append(tuple(c[k]+.0012*(u[k]*math.cos(q)+w[k]*math.sin(q))for k in range(3)))
 fs=[tuple(reversed(range(N))),tuple(N+j for j in range(N))]+[(j,(j+1)%N,N+(j+1)%N,N+j)for j in range(N)];record('WholeContinuousFixedDiagonalCordGnomon',v,fs,3)
def make_geometry():
 G.clear();lower_leaf();upper_leaf();cord()
 for x,label in[(-.047,'Left'),(.047,'Right')]:axis_lathe('Whole'+label+'FixedHingeBarrel',(x,.085,.016),'X',[(-.011,0),(-.011,.006),(.011,.006),(.011,0)],2,24)
 axis_lathe('WholeAcrossLeafHingePin',(0,.085,.016),'X',[(-.083,0),(-.083,.004),(-.078,.004),(-.078,.0025),(.078,.0025),(.078,.004),(.083,.004),(.083,0)],2,24)
 p=[(0,CUP_Y-.023),(.005,CUP_Y),(0,CUP_Y+.023),(-.005,CUP_Y)];v=[(x,y,z)for z in[.008,.011]for x,y in p];fs=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)];record('WholeFixedSingleCompassNeedle',v,fs,3)
 lathe('WholeCompassPivotAndHead',0,[(0,.003),(.002,.003),(.002,.012),(.004,.012),(.004,.015),(0,.015)],2,24);v,f,m=G['WholeCompassPivotAndHead'];G['WholeCompassPivotAndHead']=([(x,y+CUP_Y,z)for x,y,z in v],f,m)
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
 for i,material in enumerate(d['materials']):material['pbrMetallicRoughness']['metallicFactor']=[0.,0.,.66,0.][i]
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole twin leaf cord dial preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.085))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(5.0,-8.0,5.4));bpy.context.view_layer.update()
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
  if p.exists():files[role]={'path':f'assets/timekeeping/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'timekeeping','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete diptych-dial-inspired fixed portable instrument exterior. A whole low rectangular wooden-look lower leaf has a genuinely recessed circular blind compass cup with a full bottom and continuous inner wall. One complete dark diamond needle and full headed pivot occupy that cup. A separate whole blank upper leaf stands upright at the rear, joined by two entire short hinge-barrel exteriors and one full through-span pin. A single continuous thin diagonal cord reaches from the lower leaf near the front to the upper inner face, making the characteristic open two-leaf and string-gnomon organization visible. All leaf boundaries, cavity construction, full needle, hinge profiles, complete pin and cord coordinates are original numerical geometry. Unlike the earlier pedestal sundial, there is no round elevated disk, heavy column, triangular solid gnomon or dial-marker ring. Unlike the independent round pocket-compass prop, this is not that circular case reused or reduced and fitted with a lid; the compass cup belongs to the entire new rectangular lower leaf and the upper leaf/diagonal cord jointly define a different whole device. No existing dial, compass, book, case, marker or hinge mesh is imported or extracted. Eight closed editable whole meshes, four constant opaque untextured PBR roles, metres native Z up and whole horizontal-bounds-centred ground datum. One original model zero scenes. Uninscribed broad historical-instrument category art, not ivory, a named makers product, a museum replica or a historical calibrated layout. The fixed joined pose and slightly buried cord ends are visual attachments, not tension equilibrium or an operable hinge. No scales, printed text, geographical tables, winding, magnetism, time reading, true-north alignment, solar or lunar computation, shadow calibration, latitude accuracy, navigation reliability, manufacture, material performance, handling or safety capability made or verified. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
