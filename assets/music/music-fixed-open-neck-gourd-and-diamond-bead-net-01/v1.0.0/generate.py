import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='music-fixed-open-neck-gourd-and-diamond-bead-net-01'
TITLE='Fixed Open Neck Gourd and Diamond Bead Net'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeOpenNeckGourdWarmOchre',(.49,.25,.085,1),.79),('WholeDiamondNetDarkCord',(.075,.055,.035,1),.86),('WholeKnotBeadsRedEarth',(.41,.115,.055,1),.68),('WholeKnotBeadsIvory',(.70,.60,.41,1),.74)]
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
OUTER=[(.045,0),(.065,.008),(.088,.035),(.108,.065),(.118,.095),(.118,.120),(.106,.150),(.083,.180),(.050,.205),(.032,.223),(.028,.246),(.027,.304),(.030,.326)]
def body_radius(z):
 for (a,x),(b,y)in zip(OUTER,OUTER[1:]):
  if x<=z<=y:return a+(b-a)*(z-x)/(y-x)
 raise AssertionError('outside gourd body')
def whole_cord(name,path,r):
 vs=[];n=6;last=None
 for j,p in enumerate(path):
  a=path[max(0,j-1)];b=path[min(len(path)-1,j+1)];t=[b[k]-a[k]for k in range(3)];le=math.sqrt(sum(q*q for q in t));t=[q/le for q in t]
  if last is None:u=[-t[1],t[0],0]
  else:
   q=sum(last[k]*t[k]for k in range(3));u=[last[k]-q*t[k]for k in range(3)]
  le=math.sqrt(sum(q*q for q in u));u=[q/le for q in u];v=[t[1]*u[2]-t[2]*u[1],t[2]*u[0]-t[0]*u[2],t[0]*u[1]-t[1]*u[0]];last=u
  for i in range(n):vs.append(tuple(p[k]+r*(math.cos(math.tau*i/n)*u[k]+math.sin(math.tau*i/n)*v[k])for k in range(3)))
 fs=[tuple(reversed(range(n))),tuple((len(path)-1)*n+i for i in range(n))]+[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i)for j in range(len(path)-1)for i in range(n)]
 record(name,vs,fs,1)
def collar(name,z):
 rr=body_radius(z)+.001;n=48;q=8;v=[((rr+.0025*math.cos(math.tau*j/q))*math.cos(math.tau*i/n),(rr+.0025*math.cos(math.tau*j/q))*math.sin(math.tau*i/n),z+.0025*math.sin(math.tau*j/q))for i in range(n)for j in range(q)]
 record(name,v,[(i*q+j,((i+1)%n)*q+j,((i+1)%n)*q+(j+1)%q,i*q+(j+1)%q)for i in range(n)for j in range(q)],1)
def make_geometry():
 G.clear()
 # One whole thick hollow bottle-gourd with a genuine open mouth and closed bottom.
 inner=[(.022,.326),(.019,.304),(.020,.246),(.024,.223),(.043,.205),(.075,.180),(.098,.150),(.110,.120),(.110,.095),(.100,.065),(.080,.035),(.058,.017),(0,.011)]
 lathe_profile('WholeHollowOpenMouthBottleGourd',[(0,0)]+OUTER+inner,0,48)
 levels=[.035,.065,.095,.120,.150,.180,.205,.223]
 for sign in[-1,1]:
  for i in range(12):
   path=[]
   # Subdivide each diamond edge along the original curved gourd surface.
   for j in range(len(levels)-1):
    for k in range(5):
     a=k/5;z=levels[j]*(1-a)+levels[j+1]*a;t=math.tau*i/12+sign*(j+a)*math.tau/24;rr=body_radius(z)+.003;path.append((rr*math.cos(t),rr*math.sin(t),z))
   z=levels[-1];t=math.tau*i/12+sign*(len(levels)-1)*math.tau/24;rr=body_radius(z)+.003;path.append((rr*math.cos(t),rr*math.sin(t),z))
   whole_cord('WholeDiamondNetCord_%s_%02d'%('A'if sign==1 else'B',i),path,.0016)
 collar('WholeLowerNetRetainingCord',levels[0]);collar('WholeUpperNeckNetRetainingCord',levels[-1])
 # Complete solid beads at the true crossings of the two diagonal cord families.
 for j,z in enumerate(levels[1:-1],1):
  for i in range(12):
   name='WholeNetKnotBead_%02d_%02d'%(j,i);t=math.tau*i/12+j*math.tau/24;rr=body_radius(z)+.003;p=(rr*math.cos(t),rr*math.sin(t),z)
   lathe_profile(name,[(0,-.0055),(.0041,-.0038),(.0055,0),(.0041,.0038),(0,.0055)],2 if(i+j)%3 else 3,8)
   v,f,m=G[name];G[name]=([(x+p[0],y+p[1],zz+p[2])for x,y,zz in v],f,m)
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral instrument preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.16))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(4.5,-6,3.6));bpy.context.view_layer.update()
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete static bead-net gourd rattle appearance. A single thick hollow bottle-gourd body has a finite flat belly foot, rounded broad chamber, narrowing shoulder and long genuinely open neck. Twenty-four complete curved diagonal cords form an attached diamond net around the belly between two whole retaining collars; seventy-two complete faceted beads sit at the cord crossings. The cords follow the original body surface and remain rooted in the collars; beads and cords have small intentional fixed intersections. This whole open-neck chamber and two-direction beaded net is neither the old sealed grooved guiro nor the cylindrical core and independent parallel beaded loops of the cabasa. All numeric geometry newly authored, one model zero scenes and four opaque PBR roles. Beads are subordinate parts, not separate models. Metres, native Z up and horizontal-envelope-centred ground datum. Static artistic illustration only; no moving net, cord tension, bead articulation, sound, playability, cultural or historical reconstruction, manufacturing, handling or toy-safety capability. No rig, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
