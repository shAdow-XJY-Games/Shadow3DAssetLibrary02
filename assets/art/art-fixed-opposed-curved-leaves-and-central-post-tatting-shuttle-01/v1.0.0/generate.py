import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='art-fixed-opposed-curved-leaves-and-central-post-tatting-shuttle-01'
TITLE='Fixed Opposed Curved Leaves and Central Post Tatting Shuttle'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeHoneyWoodLeafExterior',(.44,.23,.080,1),.63),('WholeDarkInnerLeafFaces',(.22,.105,.032,1),.75),('WholeCentralWoodenPost',(.31,.16,.063,1),.78),('WholeContinuousWoundCreamThread',(.71,.62,.42,1),.91)]
G={}

def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def lathe_profile(name,profile,mat,n=48):
 v=[];rings=[];fs=[]
 for r,z in profile:
  if r==0:rings.append([len(v)]);v.append((0,0,z))
  else:
   row=[]
   for i in range(n):row.append(len(v));v.append((r*math.cos(math.tau*i/n+math.pi/n),r*math.sin(math.tau*i/n+math.pi/n),z))
   rings.append(row)
 for a,b in zip(rings,rings[1:]+rings[:1]):
  if len(a)==len(b)==1:continue
  for i in range(n):
   j=(i+1)%n
   if len(a)==1:fs.append((a[0],b[j],b[i]))
   elif len(b)==1:fs.append((a[i],a[j],b[0]))
   else:fs.append((a[i],a[j],b[j],b[i]))
 record(name,v,fs,mat)
def make_geometry():
 G.clear()
 # Two whole thick pointed-oval leaves bend toward one another at both blunt tips.
 xs=[-.038,-.035,-.029,-.020,-.010,0,.010,.020,.029,.035,.038];ws=[.0011,.004,.008,.011,.0125,.013,.0125,.011,.008,.004,.0011];us=[-1,-.5,0,.5,1];N=len(xs);M=len(us)
 for upper in[False,True]:
  v=[]
  for inner in[False,True]:
   for x,w in zip(xs,ws):
    for u in us:
     rise=.0068*(abs(x)/.038)**2.2+.0013*max(0,abs(u)-.5)*2*(1-(abs(x)/.038)**2)
     # Broad central lower face stays exactly planar instead of a point contact.
     if abs(x)<=.010 and abs(u)<=.5:rise=0
     z=rise+(.0016 if inner else 0)
     v.append((x,w*u,.018-z if upper else z))
  fs=[];ms=[]
  def ix(inner,i,j):return int(inner)*N*M+i*M+j
  for inner in[False,True]:
   for i in range(N-1):
    for j in range(M-1):
     f=[ix(inner,i,j),ix(inner,i+1,j),ix(inner,i+1,j+1),ix(inner,i,j+1)]
     if inner:f.reverse()
     fs.append(f);ms.append(1 if inner else 0)
  border=[(i,0)for i in range(N)]+[(N-1,j)for j in range(1,M)]+[(i,M-1)for i in range(N-2,-1,-1)]+[(0,j)for j in range(M-2,0,-1)]
  for k,(i,j)in enumerate(border):ii,jj=border[(k+1)%len(border)];fs.append([ix(False,i,j),ix(True,i,j),ix(True,ii,jj),ix(False,ii,jj)]);ms.append(0)
  record('WholeUpperCurvedPointedLeaf'if upper else'WholeLowerCurvedPointedLeaf',v,fs,ms)
 # Complete central post seats across both opposed leaves; its cross-section is oval.
 lathe_profile('WholeCentralJoiningPost',[(0,.0012),(.009,.0012),(.009,.0168),(0,.0168)],2,40)
 v,f,m=G['WholeCentralJoiningPost'];G['WholeCentralJoiningPost']=([(x,y*2/3,z)for x,y,z in v],f,m)
 # One continuous solid helical thread strip wraps and seats into the central post.
 path=[];turns=8;steps=turns*32
 for i in range(steps+1):
  t=i/steps;a=math.tau*turns*t;ramp=.87 if i in[0,steps]else 1
  path.append((.0094*ramp*math.cos(a),.0064*ramp*math.sin(a),.0032+.0116*t))
 v=[];F=8;last=None
 for k,c in enumerate(path):
  a=path[max(0,k-1)];b=path[min(len(path)-1,k+1)];t=[b[i]-a[i]for i in range(3)];le=math.sqrt(sum(x*x for x in t));t=[x/le for x in t]
  u=[-t[1],t[0],0];le=math.sqrt(sum(x*x for x in u));u=[x/le for x in u];w=[t[1]*u[2]-t[2]*u[1],t[2]*u[0]-t[0]*u[2],t[0]*u[1]-t[1]*u[0]]
  for j in range(F):v.append(tuple(c[i]+.00057*(u[i]*math.cos(math.tau*j/F)+w[i]*math.sin(math.tau*j/F))for i in range(3)))
 fs=[tuple(reversed(range(F))),tuple((len(path)-1)*F+j for j in range(F))]
 for k in range(len(path)-1):
  for j in range(F):q=(j+1)%F;fs.append((k*F+j,k*F+q,(k+1)*F+q,(k+1)*F+j))
 record('WholeContinuousEightTurnThreadWinding',v,fs,3)
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral complete handcraft shuttle preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.009))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(3.1,-7.,3.2));bpy.context.view_layer.update()
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
  if p.exists():files[role]={'path':f'assets/art/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'art','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete tatting-shuttle-inspired static handcraft tool. Two thick pointed-oval wooden leaves curve toward each other at both finite blunt tips; their real open side galleries expose one full central oval post joining them and a continuous eight-turn cream thread winding seated around that post. The lower leaf has a finite central flat resting patch. The leaves, centre post and winding together count as one whole tool, not separate assets. All numerical geometry newly authored: not the old floor-and-sidewall weaving boat with its horizontal spindle, and not an extracted bobbin from the roller lace apparatus. Four opaque PBR roles, metre scale and source Z up. Broad craft-tool category only, no copied historical or branded shuttle, bone or ivory claim, actual knot sequence, thread feed, flex, hand fit, lace output, manufacture or safety capability. No rig, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
