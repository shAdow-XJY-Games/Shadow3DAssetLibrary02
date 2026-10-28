import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='art-fixed-v-trough-and-pierced-register-bookbinding-cradle-01'
TITLE='Fixed V Trough and Pierced Register Bookbinding Cradle'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeCheekBoardsAndEndStopHoneyWood',(.43,.26,.11,1),.78),('WholeVWorkingFacesPaleWood',(.66,.47,.25,1),.82),('WholeGroundedVEndFeetDarkWood',(.19,.105,.045,1),.84),('WholePiercedRegisterWarmAlloy',(.42,.35,.20,1),.49)]
G={}

def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def triangulate(poly):
 ids=list(range(len(poly)));out=[]
 def cr(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 while len(ids)>3:
  for j,b in enumerate(ids):
   a,c=ids[j-1],ids[(j+1)%len(ids)]
   if cr(poly[a],poly[b],poly[c])<=1e-13:continue
   if any(min(cr(poly[a],poly[b],poly[k]),cr(poly[b],poly[c],poly[k]),cr(poly[c],poly[a],poly[k]))>=-1e-13 for k in ids if k not in[a,b,c]):continue
   out.append((a,b,c));ids.pop(j);break
  else:raise AssertionError('non-simple original section')
 return out+[tuple(ids)]
def section(name,poly,y0,y1,mat,working=False):
 if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(poly,poly[1:]+poly[:1]))<0:poly=list(reversed(poly))
 N=len(poly);v=[(x,y,z)for y in[y0,y1]for x,z in poly];caps=triangulate(poly);f=caps+[tuple(i+N for i in reversed(t))for t in caps];m=[mat]*len(f)
 for i in range(N):
  j=(i+1)%N
  f.append((i,i+N,j+N,j));a,b=poly[i],poly[j];m.append(1 if working and abs((a[1]-abs(a[0]))-.024)<1e-8 and abs((b[1]-abs(b[0]))-.024)<1e-8 else mat)
 record(name,v,f,m)
HOLE_Y=[-.120+.040*j for j in range(7)]
def register():
 v=[];ix={};f=[]
 def V(p):
  p=tuple(round(q,10)for q in p)
  if p not in ix:ix[p]=len(v);v.append(p)
  return ix[p]
 def face(points):f.append(tuple(V(p)for p in points))
 for k,cy in enumerate(HOLE_Y):
  lo=-.145 if k==0 else(HOLE_Y[k-1]+cy)/2;hi=.145 if k==6 else(HOLE_Y[k+1]+cy)/2;w=.013;outer=[(-w,lo),(0,lo),(w,lo),(w,cy),(w,hi),(0,hi),(-w,hi),(-w,cy)];inner=[(.0028*math.cos(-3*math.pi/4+i*math.pi/4),cy+.0028*math.sin(-3*math.pi/4+i*math.pi/4))for i in range(8)]
  for i in range(8):
   j=(i+1)%8
   face([(*outer[i],.035),(*outer[j],.035),(*inner[j],.035),(*inner[i],.035)]);face([(*outer[j],.030),(*outer[i],.030),(*inner[i],.030),(*inner[j],.030)])
   face([(*inner[j],.030),(*inner[i],.030),(*inner[i],.035),(*inner[j],.035)])
   if i not in[0,1,4,5]or(k==0 and i in[0,1])or(k==6 and i in[4,5]):face([(*outer[i],.030),(*outer[j],.030),(*outer[j],.035),(*outer[i],.035)])
 record('WholeSevenThroughHoleRegisterStrip',v,f,3)
def make_geometry():
 G.clear()
 for sign,label in[(-1,'Left'),(1,'Right')]:section(label+'_WholeInclinedVWorkingCheek',[(sign*x,z)for x,z in[(.008,.032),(.084,.108),(.092,.100),(.016,.024)]],-.160,.160,0,True)
 foot=[(-.10,0),(.10,0),(.10,.104),(.09,.104),(.015,.029),(-.015,.029),(-.09,.104),(-.10,.104)]
 for label,y in[('Front',-.150),('Rear',.150)]:section(label+'_WholeVNotchedGroundFoot',foot,y-.012,y+.012,2)
 section('WholeRaisedRearRegistrationStop',[(-.095,.100),(-.013,.026),(.013,.026),(.095,.100),(.095,.116),(-.095,.116)],.156,.168,0)
 register()
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
 d['materials'][3]['pbrMetallicRoughness']['metallicFactor']=.4
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole empty bookbinding cradle preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.050))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(4.2,-6.4,5.8));bpy.context.view_layer.update()
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'art','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete empty static bookbinding-punching-cradle-inspired tool. Two whole thick sloping cheek boards form an open V bed with a real full-length central separation below the register. Two complete broad V-notched end feet support both boards and leave the middle underside open. One full raised rear stop closes only the far end. A single continuous narrow register strip bridges the lower inner cheek shoulders and contains seven genuine octagonal through apertures, with complete hole walls and material bridges between openings. The central empty under-bed route is clear beneath every register hole, not a black line painted on a filled support. Every section, end-stop contour, shoulder and perforated-strip coordinate is new. Unlike the V book scanner there is no broad ground slab, blank book, imaging arch, camera head or optical system; the low empty split bed and piercing-clearance/register relation is original together, not a stripped scanner. Unlike a sewing frame there are no tall shoulder posts, bored overhead crosshead, vertical support cords or blank text block. Six complete closed editable meshes, four opaque constant PBR roles, metres native Z up and whole horizontal bounds-centred ground origin. One whole independent model zero scenes; boards and guide are not separate counted assets. Generic unmarked fixed craft-tool appearance, not a copied product, template or construction plan. No book, paper, needle, awl or sharp working tool included. The register is fixed and the small shoulder/support overlaps are static visual contacts, not removable joints or fitted manufacture. No actual puncturing, hole-spacing standard, paper alignment accuracy, binding result, tool fit, user handling, material strength, load, stability, manufacture or safety capability made or verified. No rig, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
