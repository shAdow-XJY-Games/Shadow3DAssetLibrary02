"""SELF_REVIEW draft: unchanged old GLB payloads plus one scene floor. No product claim."""
import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='spacebase-offset-landing-and-access-court-scene-01'
TITLE='Offset Landing and Access-Tower Court'
TOL=2e-7
OFFSETS={'landing': (-1.5, 0, 0.12), 'tower': (3.2, 2.5, 0.12)}
ROTATIONS={'landing': (1, 0), 'tower': (1, 0)}
def f32(x):return struct.unpack('<f',struct.pack('<f',x))[0]
def wrapper_matrix(key):
 # Exact determinant +1 signed permutation in glTF Y-up, column-major.
 # No quaternion, data baking, normal setter or simultaneous node TRS.
 c,s=ROTATIONS[key];x,y,z=OFFSETS[key]
 return [c,0,-s,0,0,1,0,0,s,0,c,0,f32(x),f32(z),f32(-y),1]
def unpack_glb(raw):
 magic,version,size=struct.unpack_from('<4sII',raw);assert magic==b'glTF' and version==2 and size==len(raw)
 n,kind=struct.unpack_from('<II',raw,12);assert kind==0x4e4f534a
 doc=json.loads(raw[20:20+n]);p=20+n;length,kind=struct.unpack_from('<II',raw,p);assert kind==0x004e4942
 blob=raw[p+8:p+8+length];assert len(blob)==length and len(doc['buffers'])==1
 assert doc['buffers'][0]['byteLength']<=len(blob)
 return doc,blob

def pack_glb(doc,blob):
 j=json.dumps(doc,separators=(',',':'),allow_nan=False).encode();j+=b' '*((-len(j))%4)
 b=bytes(blob)+b'\0'*((-len(blob))%4)
 return struct.pack('<4sII',b'glTF',2,12+8+len(j)+8+len(b))+struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(b),0x004e4942)+b

def compose(inputs):
 d=dict(asset={'version':'2.0','generator':'Source-preserving static scene composition'},scene=0,scenes=[{'name':TITLE,'nodes':[0]}],nodes=[{'name':'AssetRoot__'+ASSET,'children':[]}],meshes=[],materials=[],accessors=[],bufferViews=[],buffers=[])
 blob=bytearray();proof={}
 for key in ['landing', 'tower']:
  raw=inputs[key];src,b=unpack_glb(raw)
  assert not any(src.get(x) for x in ['textures','images','skins','animations','cameras','extensionsUsed','extensionsRequired'])
  assert not any(any(k in n for k in ['skin','camera']) for n in src['nodes'])
  start=len(blob);blob.extend(b);blob.extend(b'\0'*((-len(blob))%4))
  vi,ai,mi,ni,pi=(len(d[k]) for k in ['bufferViews','accessors','meshes','nodes','materials'])
  for old in src['bufferViews']:
   v=copy.deepcopy(old);assert v['buffer']==0;v['byteOffset']=v.get('byteOffset',0)+start;d['bufferViews'].append(v)
  for old in src['accessors']:
   a=copy.deepcopy(old);assert 'sparse' not in a;a['bufferView']+=vi;d['accessors'].append(a)
  d['materials'].extend(copy.deepcopy(src['materials']))
  for old in src['meshes']:
   m=copy.deepcopy(old)
   for p in m['primitives']:
    assert p.get('mode',4)==4 and not p.get('targets');p['indices']+=ai;p['material']+=pi
    p['attributes']={k:v+ai for k,v in p['attributes'].items()}
   d['meshes'].append(m)
  for old in src['nodes']:
   n=copy.deepcopy(old);n['name']=key+'__'+n.get('name','node')
   if 'mesh'in n:n['mesh']+=mi
   if 'children'in n:n['children']=[x+ni for x in n['children']]
   d['nodes'].append(n)
  wrapper=len(d['nodes']);d['nodes'].append({'name':'INSTANCE__'+key,'matrix':wrapper_matrix(key),'children':[x+ni for x in src['scenes'][src.get('scene',0)]['nodes']]});d['nodes'][0]['children'].append(wrapper)
  proof[key]={'source_glb_sha256':hashlib.sha256(raw).hexdigest(),'original_meshes':len(src['meshes']),'original_payload_bytes_unchanged':True,'original_internal_TRS_and_matrix_unchanged':True,'unit_scale':True,'rotation_degrees':0,'translation_zup_m':[f32(x)for x in OFFSETS[key]],'buffer_range':[start,start+len(b)]}
  assert bytes(blob[start:start+len(b)])==b
 floor,materials=make_floor();material_base=len(d['materials']);d['materials'].extend(materials)
 def array(values,component,kind):
  flat=[v for row in values for v in row] if kind=='VEC3' else values;fmt='f' if component==5126 else 'I'
  raw=struct.pack('<'+fmt*len(flat),*flat);offset=len(blob);blob.extend(raw);blob.extend(b'\0'*((-len(blob))%4));view=len(d['bufferViews']);d['bufferViews'].append({'buffer':0,'byteOffset':offset,'byteLength':len(raw)})
  a={'bufferView':view,'componentType':component,'count':len(values),'type':kind}
  if kind=='VEC3':a.update(min=[min(p[k]for p in values)for k in range(3)],max=[max(p[k]for p in values)for k in range(3)])
  index=len(d['accessors']);d['accessors'].append(a);return index
 primitives=[]
 for material in range(len(materials)):
  positions=[];normals=[]
  for tri,mat in floor:
   if mat!=material:continue
   a,b,c=tri;u=[b[k]-a[k]for k in range(3)];v=[c[k]-a[k]for k in range(3)];n=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]);length=math.sqrt(sum(x*x for x in n));assert length>0;n=[x/length for x in n]
   positions.extend((x,z,-y)for x,y,z in tri);normals.extend([(n[0],n[2],-n[1])]*3)
  primitives.append({'attributes':{'POSITION':array(positions,5126,'VEC3'),'NORMAL':array(normals,5126,'VEC3')},'indices':array(list(range(len(positions))),5125,'SCALAR'),'material':material_base+material,'mode':4})
 mesh=len(d['meshes']);d['meshes'].append({'name':'SceneOnlyOffsetLandingCourtGround','primitives':primitives});node=len(d['nodes']);d['nodes'].append({'name':'SCENE_ONLY__OffsetLandingCourtGround','mesh':mesh,'extras':{'new_independent_model':False}});d['nodes'][0]['children'].append(node);d['buffers']=[{'byteLength':len(blob)}]
 assert len(d['meshes'])==12 and len(d['materials'])==10
 proof['floor_triangles']=len(floor);proof['triangles']=948+len(floor);proof['single_scene_count']=1;proof['new_independent_model_count']=0
 return d,bytes(blob),proof

def make_floor():
 # Single scene-only connected slab with a dogleg ground band from the landing side-ramp toe toward the offset tower front; lower outlet side remains unoccupied; no new buildings or reused model edits.
 xs=[-5.4,1.85,2.7,3.7,4.8,5.4];ys=[-4.2,-.45,.45,1.025,4.2];zs=[0,.12]
 boundary={};fs=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
 for i in range(len(xs)-1):
  for j in range(len(ys)-1):
   for k in range(len(zs)-1):
    x0,x1=xs[i:i+2];y0,y1=ys[j:j+2];z0,z1=zs[k:k+2]
    v=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    for f in fs:
     q=tuple(v[t]for t in f);key=tuple(sorted(q))
     if key in boundary:del boundary[key]
     else:boundary[key]=q
 ts=[]
 for q in boundary.values():
  cx=sum(p[0]for p in q)/4;cy=sum(p[1]for p in q)/4
  mat=0 if all(p[2]==.12 for p in q) and ((1.85<cx<4.8 and abs(cy)<.45)or(2.7<cx<3.7 and .45<cy<1.025))else 1
  for f in [(0,1,2),(0,2,3)]:ts.append((tuple(q[i]for i in f),mat))
 mats=[{'name':n,'doubleSided':True,'pbrMetallicRoughness':{'baseColorFactor':color,'metallicFactor':0.,'roughnessFactor':.88}}for n,color in [('SceneOffsetLandingCourtFloor',[.53,.42,.22,1]),('SceneOffsetLandingCourtWallAndEdge',[.20,.235,.24,1])]]
 return ts,mats

def main():
 import bpy,sys,time
 from mathutils import Vector
 OUT=Path(__file__).resolve().parent
 view=sys.argv[sys.argv.index('--tier-single-view')+1]if '--tier-single-view'in sys.argv else 'thumbnail';assert view in ['qa-front','thumbnail']
 inputs={k:zlib.decompress(base64.b64decode(v['compressed']))for k,v in INPUTS.items()}
 for k,raw in inputs.items():assert hashlib.sha256(raw).hexdigest()==INPUTS[k]['sha256']
 document,blob,proof=compose(inputs);model=pack_glb(document,blob);(OUT/'model.glb').write_bytes(model)
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==12
 triangle_count=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons);assert triangle_count==proof['triangles']
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 lo=[min(v[k]for v in points)for k in range(3)];hi=[max(v[k]for v in points)for k in range(3)]
 assert abs(lo[2])<=TOL and abs(lo[0]+hi[0])<=TOL and abs(lo[1]+hi[1])<=TOL
 assert len({m for o in parts for m in o.data.materials})==10
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
 for layer in scene.view_layers:layer.cycles.use_denoising=False
 scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
 scene.render.resolution_x=scene.render.resolution_y=640;scene.render.resolution_percentage=100
 scene.world=scene.world or bpy.data.worlds.new('Neutral static spacebase display');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,1.0))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(9,-13,11) if view=='qa-front' else (10,-14,13));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'),compress=True)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':12,'triangles':triangle_count,'materials':10,'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
 if '--geometry-only' not in sys.argv:
  view=sys.argv[sys.argv.index('--tier-single-view')+1]if '--tier-single-view'in sys.argv else 'thumbnail';assert view in ['qa-front','thumbnail']
  scene.cycles.samples=16 if view=='qa-front' else 128;scene.render.filepath=str(OUT/(view+'.png'));start=time.monotonic();bpy.ops.render.render(write_still=True);qa['render']={'view':view,'samples':scene.cycles.samples,'seconds':time.monotonic()-start,'original_pixels_reviewed':False}
 (OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if p.exists():files[role]={'path':f'assets/spacebase/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'scenes','assetKind':'scene','theme':'spacebase','style':'source-preserved-low-poly','title':TITLE,'description':'One static spacebase landing-service court assembled from two complete qualified original facilities: a broad octagonal well-and-outlet landing platform on the left and a separate fixed caged access-lift tower offset to the rear-right. The landing ramp reaches a ground-level dogleg band aimed toward the tower front, while the front low outlet faces a separate empty apron. The tower keeps its original fixed elevated car and forward trough, at a different height from the landing field: these are deliberately not claimed to be a connected upper bridge or a compatible docking system. All original meshes, directed triangles, normal buffers, internal node transforms and material dictionaries remain intact at unit scale and unchanged pose. A low scene-only connected floor with same-surface path materials is the only new geometry. This landing-field / lower-outlet clearance / offset service-access relation differs from the earlier junction with solar array and sampling rover forecourt. One scene, zero new independent models, two complete instances of two accepted models. No new leg, ramp, tower, vehicle, solar array or repeated prop is counted. Static art only: no real landing, exhaust clearance, evacuation, boarding accessibility, docking compatibility, elevator function, loading, thermal behaviour, navigation, operational workflow, engineering or safety claim.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':10,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)

INPUTS={'landing': {'sha256': '7d0436cf851747ac477455e947eed1bbaaef64d20cf6e1574d73f7cc836bd199', 'compressed': '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'}, 'tower': {'sha256': 'ea0ceaa61d98f6ebb9bd59ff5e85e428a6b145f2e98418e74d04020c2240ce3d', 'compressed': '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'}}
if __name__=='__main__':main()
