import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='culture-fixed-nested-case-and-twin-cord-channel-inro-01'
TITLE='Fixed Nested Case and Twin Cord Channel Inro'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholePlainCaseMutedBurgundy',(.22,.032,.025,1),.40),('WholeNestedInteriorDarkRed',(.09,.024,.018,1),.69),('WholeContinuousCordWarmFlax',(.65,.44,.19,1),.86),('WholePiercedSliderPlainWood',(.25,.105,.036,1),.55)]
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
def cord():
 path=cord_path();N=12;radius=.0011;v=[];last=None
 for j,p in enumerate(path):
  a=path[max(j-1,0)];b=path[min(j+1,len(path)-1)];w=[b[k]-a[k]for k in range(3)];le=math.sqrt(sum(q*q for q in w));w=[q/le for q in w];u=[1.,0.,0.]if last is None else last[:];dot=sum(u[k]*w[k]for k in range(3));u=[u[k]-dot*w[k]for k in range(3)];le=math.sqrt(sum(q*q for q in u));assert le>1e-8;u=[q/le for q in u];last=u;vv=[w[1]*u[2]-w[2]*u[1],w[2]*u[0]-w[0]*u[2],w[0]*u[1]-w[1]*u[0]]
  for i in range(N):
   a=math.tau*i/N;v.append(tuple(p[k]+radius*(u[k]*math.cos(a)+vv[k]*math.sin(a))for k in range(3)))
 f=[tuple(reversed(range(N))),tuple((len(path)-1)*N+i for i in range(N))]+[(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i)for j in range(len(path)-1)for i in range(N)];record('WholeContinuousSideChannelAndUpperLoopCord',v,f,2)
def case_profile(name,profile,materials):
 N=48;v=[];rows=[];f=[];m=[]
 for scale,z in profile:
  ids=[]
  for j in range(1 if scale==0 else N):
   a=math.tau*j/N;co=math.cos(a);si=math.sin(a);ids.append(len(v));v.append((scale*.034*math.copysign(abs(co)**.65,co),scale*.014*math.copysign(abs(si)**.65,si),z))
  rows.append(ids)
 for k,(a,b)in enumerate(zip(rows,rows[1:]+rows[:1])):
  if len(a)==len(b)==1:continue
  for j in range(N):
   q=(j+1)%N;f.append((a[0],b[q],b[j])if len(a)==1 else(a[j],a[q],b[0])if len(b)==1 else(a[j],a[q],b[q],b[j]));m.append(materials[k]if isinstance(materials,list)else materials)
 record(name,v,f,m)
def cord_path():
 control=[(-.0367,0,.007),(-.0355,0,.014),(-.0355,0,.040),(-.0355,0,.067),(-.028,0,.077),(-.012,0,.084),(-.0014,0,.090),(-.0014,0,.098),(-.0014,0,.105),(-.0065,0,.111),(0,0,.117),(.0065,0,.111),(.0014,0,.105),(.0014,0,.098),(.0014,0,.090),(.012,0,.084),(.028,0,.077),(.0355,0,.067),(.0355,0,.040),(.0355,0,.014),(.0367,0,.007)];out=[]
 for j,p1 in enumerate(control[:-1]):
  p0=control[max(j-1,0)];p2=control[j+1];p3=control[min(j+2,len(control)-1)]
  for k in range(4):
   t=k/4;out.append(tuple(.5*(2*p1[a]+(-p0[a]+p2[a])*t+(2*p0[a]-5*p1[a]+4*p2[a]-p3[a])*t*t+(-p0[a]+3*p1[a]-3*p2[a]+p3[a])*t*t*t)for a in range(3)))
 return out+[control[-1]]
def make_geometry():
 G.clear()
 for j in range(3):
  z=.021*j
  profile=[(1,z+.0015 if j==0 else z),(1,z+.0215),(.94,z+.022),(.89,z+.022),(.89,z+.0245),(.80,z+.0245),(.80,z+.006),(0,z+.006),(0,z+.004 if j else z),(.90,z+.004 if j else z),(.90,z if j else z),(.96,z)]
  if j==0:profile=[(1,.0015),(1,.0215),(.94,.022),(.89,.022),(.89,.0245),(.80,.0245),(.80,.006),(0,.006),(0,0),(.96,0)]
  case_profile('WholeNestedCompartment_%02d'%j,profile,[0,0,1,1,1,1,1,1,1,1,0,0][:len(profile)])
  for sign,label in[(-1,'Left'),(1,'Right')]:lathe(label+'_WholeThroughCordChannel_%02d'%j,sign*.0355,[(.0038,z+.004),(.0045,z+.005),(.0045,z+.020),(.0038,z+.021),(.0019,z+.021),(.0019,z+.004)],0,24)
 case_profile('WholeReceiverRecessTopLid',[(1,.063),(1,.069),(.94,.071),(0,.071),(0,.067),(.90,.067),(.90,.063)],[0,0,0,0,1,1,1])
 for sign,label in[(-1,'Left'),(1,'Right')]:lathe(label+'_WholeThroughCordChannel_Lid',sign*.0355,[(.0038,.064),(.0045,.065),(.0045,.069),(.0038,.070),(.0019,.070),(.0019,.064)],0,24)
 cord();lathe('WholePiercedFixedCordSlider',0,[(.0023,.091),(.0045,.091),(.0065,.094),(.0065,.099),(.0045,.102),(.0023,.102)],3,32)
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole plain nested case preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.058))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(4.2,-8.5,4.8));bpy.context.view_layer.update()
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'culture','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete static plain inro-inspired nested case with its cord and pierced slider. Three whole flattened rounded-oblong compartments each have a real inner cavity, finite bottom and upper nesting lip; the upper two and the whole top lid have matching underside receiver recesses. Two columns of full through-bored side channel bosses remain seated to the four case sections. One continuous finite tube cord rises from a hidden fixed root through the left column, converges through a real bored slider, makes an open upper return loop and descends through the right column to its other fixed root. The slider and roots use explicit small hidden fixed contacts, not a working sliding or detachable mechanism. The entire shape, superellipse section, nesting cross-sections, side-channel sequence and cord route are original numeric geometry. Unlike a rectangular observation case with exterior stack feet, bearing rails, handle and latches, this is an internally nested flattened case with axial side cords; unlike a gift parcel it has genuine cavities, aligned passages and one returning cord rather than sealed box faces and two perpendicular ribbon wraps. Fourteen whole closed editable meshes, four opaque constant PBR roles, metres, native Z up, horizontal whole bounds-centred ground origin with a finite base sole. One new complete model and zero scenes; compartments, cord and slider are not counted as separate assets. Closed fixed display pose; hidden interiors and channels are numerically checked, not claimed visible from every view. Broad Japanese case category only, uninscribed and without copied museum motifs, provenance, lacquer technique or historic dimensions. No netsuke toggle or complete historical dressed ensemble is claimed. No actual opening, sliding, hanging/load support, medical storage, manufacture, period authenticity, cultural efficacy, material suitability or safety capability. No rig, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
