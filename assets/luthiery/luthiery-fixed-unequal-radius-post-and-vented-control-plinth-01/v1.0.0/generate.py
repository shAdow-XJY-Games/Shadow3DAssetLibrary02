import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='luthiery-fixed-unequal-radius-post-and-vented-control-plinth-01'
TITLE='Fixed Unequal Radius Post and Vented Control Plinth'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeMutedGreenControlCase',(.18,.29,.25,1),.68),('WholeUnequalRadiusPostAlloy',(.62,.65,.60,1),.40),('WholeBaseAndPlainControlDark',(.075,.09,.08,1),.76),('WholeFlangeAndFastenersSteel',(.29,.33,.30,1),.49)]
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
def cells_boundary(name,xs,ys,zs,predicate,mat):
 cells={(i,j,k)for i in range(len(xs)-1)for j in range(len(ys)-1)for k in range(len(zs)-1)if predicate((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)};v=[];fs=[];ix={}
 for i,j,k in sorted(cells):
  for(di,dj,dk),corners in DIRECTIONS:
   if(i+di,j+dj,k+dk)in cells:continue
   face=[]
   for a,b,c in corners:
    q=(xs[i+a],ys[j+b],zs[k+c])
    if q not in ix:ix[q]=len(v);v.append(q)
    face.append(ix[q])
   fs.append(face)
 record(name,v,fs,mat)
DIRECTIONS=[((-1,0,0),[(0,0,0),(0,0,1),(0,1,1),(0,1,0)]),((1,0,0),[(1,0,0),(1,1,0),(1,1,1),(1,0,1)]),((0,-1,0),[(0,0,0),(1,0,0),(1,0,1),(0,0,1)]),((0,1,0),[(0,1,0),(0,1,1),(1,1,1),(1,1,0)]),((0,0,-1),[(0,0,0),(0,1,0),(1,1,0),(1,0,0)]),((0,0,1),[(0,0,1),(1,0,1),(1,1,1),(0,1,1)])]
VENTS=[(-.052,-.032),(-.010,.010),(.032,.052)]
BOLTS=[(x,y)for x in[-.072,.072]for y in[-.050,.050]]
def chamfer_rect(a,b,r):return[(-a+r,-b),(a-r,-b),(a,-b+r),(a,b-r),(a-r,b),(-a+r,b),(-a,b-r),(-a,-b+r)]
def prism(name,p,z0,z1,mat):
 n=len(p);v=[(x,y,z)for z in[z0,z1]for x,y in p];f=[tuple(reversed(range(n))),tuple(n+j for j in range(n))]+[(j,(j+1)%n,n+(j+1)%n,n+j)for j in range(n)];record(name,v,f,mat)
def vented_case():
 xs=[-.115,-.107,.107,.115];ys=sorted(set([-.085,-.077,.077,.085]+[a for p in VENTS for a in p]));zs=[.009,.017,.030,.039,.050,.058]
 def solid(x,y,z):return(abs(x)>.107 or abs(y)>.077 or z<.017 or z>.050)and not(abs(x)>.107 and .030<z<.039 and any(a<y<b for a,b in VENTS))
 cells_boundary('WholeHollowCaseAndSixTrueSideVents',xs,ys,zs,solid,0)
def post_xy(a):return(.060*math.cos(a),.035*math.sin(a)*(1-.25*math.cos(a)))
def full_post():
 N=64;v=[]
 for scale,z in[(1.,.065),(1.,.239),(.955,.245)]:
  for j in range(N):x,y=post_xy(math.tau*j/N);v.append((scale*x,scale*y,z))
 fs=[tuple(reversed(range(N))),tuple(2*N+j for j in range(N))]+[(k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j)for k in range(2)for j in range(N)];record('WholeContinuousUnequalRadiusVerticalPost',v,fs,1)
def make_geometry():
 G.clear();prism('WholeBroadChamferedGroundSole',chamfer_rect(.140,.108,.014),0,.012,2);vented_case();prism('WholeFourCornerPostFlange',chamfer_rect(.086,.064,.009),.056,.068,3);full_post()
 for k,(x,y)in enumerate(BOLTS):
  lathe('WholeFixedFlangeBolt_'+str(k),x,[(0,.052),(.0038,.052),(.0038,.070),(.007,.070),(.007,.076),(.005,.078),(0,.078)],3,12);v,f,m=G['WholeFixedFlangeBolt_'+str(k)];G['WholeFixedFlangeBolt_'+str(k)]=([(a,b+y,c)for a,b,c in v],f,m)
 axis_lathe('WholeBlankFrontControl',(0,0,.033),'Y',[(-.107,0),(-.107,.012),(-.104,.016),(-.091,.016),(-.088,.009),(-.080,.009),(-.080,0)],2,32)
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
 for i,material in enumerate(d['materials']):material['pbrMetallicRoughness']['metallicFactor']=[.12,.72,0.,.65][i]
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole luthier tool preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.125))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(5.5,-8.0,5.3));bpy.context.view_layer.update()
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
  if p.exists():files[role]={'path':f'assets/luthiery/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'luthiery','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete fixed luthier-bending-iron-inspired exterior. A whole upright metal-look post has one continuous convex unequal-radius egg-like section, long vertical sides and a shallow full upper-edge chamfer with closed top. The broad noncircular forming post roots through one complete four-corner flange with four full fixed headed fasteners into a low hollow control plinth. That entire plinth has three genuine rectangular through-wall vents on each side, an empty interior, complete top and bottom walls and one whole unmarked front control. A separate full chamfered ground sole supports the case. All section functions, solids, cavities, vent layout, flange, bolt profiles and whole arrangement are newly numerically authored. This is not the earlier inclined hand iron in a separate helical rest with attached looped cord and side-by-side control case, nor a horizontal hollow goffering barrel around an inserted rod on a cranked stem. Here the full upright broad varying-radius post itself is the central body above a ventilated low base; no earlier mesh, pole, barrel, coil, case or hand grip is imported, extracted or resized. Nine closed editable complete meshes, four opaque constant untextured PBR roles, metres native Z up and whole horizontal-bounds-centred ground sole. One original model zero scenes. Broad craft-tool category art only, not a branded product, replica, measured device or construction plan. The post is a closed solid appearance with no heating element or internal electrical system; the case vents are real visual empty paths, not a cooling-performance claim. Fasteners deliberately overlap fixed roots and have no threaded travel. No cable, electrical supply, operating temperatures, heat, wet wood, forming strap, actual bending, material suitability, thermal simulation, electrical design, calibration, load, stability, handling, ergonomics, manufacture or equipment safety is provided or verified. No rig, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
