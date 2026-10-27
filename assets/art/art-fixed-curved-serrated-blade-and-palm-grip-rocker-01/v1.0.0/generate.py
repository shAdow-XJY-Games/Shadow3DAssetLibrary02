import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='art-fixed-curved-serrated-blade-and-palm-grip-rocker-01'
TITLE='Fixed Curved Serrated Blade and Palm Grip Rocker'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeBroadBladeSatinSteel',(.44,.49,.50,1),.46),('WholeFiniteToothBevelSteel',(.30,.35,.37,1),.52),('WholePalmGripWarmWood',(.34,.17,.075,1),.70),('WholeFrontFerruleWarmAlloy',(.48,.38,.20,1),.50)]
G={}

def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def earclip(poly):
 ids=list(range(len(poly)));out=[]
 def cross2(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 while len(ids)>3:
  done=False
  for k,i in enumerate(ids):
   a,b,c=ids[k-1],i,ids[(k+1)%len(ids)]
   if cross2(poly[a],poly[b],poly[c])<=1e-13:continue
   if any(j not in [a,b,c] and min(cross2(poly[a],poly[b],poly[j]),cross2(poly[b],poly[c],poly[j]),cross2(poly[c],poly[a],poly[j]))>=-1e-13 for j in ids):continue
   out.append((a,b,c));ids.pop(k);done=True;break
  assert done,'Cannot triangulate complete outer shell'
 out.append(tuple(ids));return out
def edge_y(x):return -.029-math.sqrt(.060*.060-x*x)
def make_geometry():
 G.clear();global TEETH;TEETH=36;step=.078/TEETH;front=[]
 for k in range(TEETH):
  for u,depth in[(0,0),(.30,.0009),(.70,.0009),(1,0)]:
   x=-.039+(k+u)*step;p=(x,edge_y(x)-depth)
   if not front or abs(front[-1][0]-x)>1e-12:front.append(p)
 # One continuous complete steel plate, including shoulders, rising root and buried tang.
 left=[(-.006,.027),(-.006,.006),(-.007,.005),(-.029,-.017),(-.039,-.042)]
 right=[(.039,-.042),(.029,-.017),(.007,.005),(.006,.006),(.006,.027)]
 outline=left+front+right;innerfront=[(x,edge_y(x)+.007)for x,y in front];upper=left+innerfront+right
 def lift(y):return max(0.,min(.0088,(y-.005)*.4))
 v=[];ix={};fs=[];ms=[]
 def V(p):
  p=tuple(round(float(q),10)for q in p)
  if p not in ix:ix[p]=len(v);v.append(p)
  return ix[p]
 def face(points,mat):fs.append(tuple(V(p)for p in points));ms.append(mat)
 # Conforming cross-section at the exact root rise: lower blade remains genuinely planar,
 # rather than letting an ear-clipped diagonal lift the broad back toward the tang.
 def surface_regions(poly):
  cuts=[i for i,p in enumerate(poly)if abs(p[1]-.005)<1e-12];assert len(cuts)==2
  i,j=cuts;return [poly[i:j+1],poly[j:]+poly[:i+1]]
 for poly in surface_regions(outline):
  for tri in earclip(poly):face([(poly[i][0],poly[i][1],lift(poly[i][1]))for i in reversed(tri)],0)
 for poly in surface_regions(upper):
  for tri in earclip(poly):face([(poly[i][0],poly[i][1],lift(poly[i][1])+.005)for i in tri],0)
 # Complete bevel strip follows every actual tooth and valley, not painted teeth or detached tips.
 for (a,b),(c,d)in zip(zip(front,front[1:]),zip(innerfront,innerfront[1:])):face([(a[0],a[1],.0012),(b[0],b[1],.0012),(d[0],d[1],.005),(c[0],c[1],.005)],1)
 # Boundary side walls; transition shoulder faces close at both ends of the bevel strip.
 frontstart=len(left);frontend=frontstart+len(front)-1
 for i,a in enumerate(outline):
  j=(i+1)%len(outline);b=outline[j];za=.0012 if frontstart<=i<=frontend else lift(a[1])+.005;zb=.0012 if frontstart<=j<=frontend else lift(b[1])+.005
  face([(a[0],a[1],lift(a[1])),(b[0],b[1],lift(b[1])),(b[0],b[1],zb),(a[0],a[1],za)],0)
 for p,q in[(front[0],innerfront[0]),(front[-1],innerfront[-1])]:
  shoulder=left[-1]if p==front[0]else right[0];ps=[(p[0],p[1],.0012),(q[0],q[1],.005),(shoulder[0],shoulder[1],.005)];face(ps if p==front[0]else list(reversed(ps)),0)
 record('WholeCurvedSerratedPlateRootAndTang',v,fs,ms)
 # Whole plump short palm handle with a finite lower polygonal facet, not an old long pencil grip.
 N=24;phase=math.pi/N;cz=.014*math.cos(phase);rows=[(.014,.009,.009),(.028,.0102,.0102),(.043,.019,.014),(.075,.021,.014),(.095,.016,.012),(.108,.009,.007)]
 v=[(rx*math.cos(math.tau*i/N+phase),y,cz+rz*math.sin(math.tau*i/N+phase))for y,rx,rz in rows for i in range(N)]
 fs=[tuple(reversed(range(N))),tuple((len(rows)-1)*N+i for i in range(N))]+[(k*N+i,k*N+(i+1)%N,(k+1)*N+(i+1)%N,(k+1)*N+i)for k in range(len(rows)-1)for i in range(N)];record('WholeShortRoundedPalmGrip',v,fs,2)
 # Complete annular ferrule, deliberately fixed around the original new grip root.
 v=[(r*math.cos(math.tau*i/N+phase),y,cz+r*math.sin(math.tau*i/N+phase))for y,r in[(.012,.008),(.012,.0115),(.029,.0115),(.029,.008)]for i in range(N)];fs=[(k*N+i,k*N+(i+1)%N,((k+1)%4)*N+(i+1)%N,((k+1)%4)*N+i)for k in range(4)for i in range(N)];record('WholeThickFrontFerrule',v,fs,3)
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole printmaking rocker preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.012))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(3.8,-6.,8.5));bpy.context.view_layer.update()
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'art','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete static mezzotint-rocker-inspired hand tool. A single broad finite steel-look plate has a curved front edge with thirty-six actual finite-thickness serrations and a continuous bevel strip following every tooth and valley. Both shoulders narrow into one rising root and tang seated in a complete short rounded wooden-look palm grip; one whole thick annular alloy-look ferrule surrounds that root. Full blade back and a finite grip facet rest at the same ground datum. All numerical outlines, serrations, shoulder/root transitions and grip proportions are new, not an old U-flute gouge, bent hive scraper or long pen handle reused. Four opaque PBR roles, metre scale, native Z up, one whole model zero scenes. Broad printmaking-tool appearance only; coarse visual serrations are not a real working tooth specification. No sharpened edge, cutting, plate preparation, ink retention, printing performance, historical maker, manufacture, ergonomics, strength or safety capability. Fixed intentional assembly overlaps; no animation, rig or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
