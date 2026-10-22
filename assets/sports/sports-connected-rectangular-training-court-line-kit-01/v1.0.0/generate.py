"""New complete connected rectangular training-court line kit. SELF_REVIEW, not regulation dimensions."""
import hashlib,json,math,struct
from pathlib import Path
ASSET='sports-connected-rectangular-training-court-line-kit-01'
TITLE='Connected Rectangular Training Court Line Kit'
TOL=2e-7
DESCRIPTION='One newly authored complete rectangular training-court line kit: an outer boundary, two continuous inner side lines, three transverse lines and a short central service divider form one connected closed raised ribbon mesh with genuinely open cells. One opaque ivory PBR material, one prop and zero scenes; metre units, Z up, bottom-centred origin. Every numeric vertex and face is new; no old semicircle, floor, net or scene geometry is copied. Deliberately stylised 25 mm thick game-art marking, not regulation tennis/badminton/volleyball dimensions, physical paint, safety-approved surfacing or functional sports equipment. No ground slab, net, player, texture, text or animation.'
def geometry():
 xs=[-3.4,-3.3,-2.5,-2.4,-.05,.05,2.4,2.5,3.3,3.4];ys=[-6.,-5.9,-2.5,-2.4,-.05,.05,2.4,2.5,5.9,6.];h=.025
 occupied={(i,j)for i in range(9)for j in range(9)if i in (0,8,2,6)or j in (0,8,4)or(j in(2,6)and 2<=i<=6)or(i==4 and 2<=j<=6)}
 triangles=[]
 def quad(q):triangles.extend([(q[0],q[1],q[2]),(q[0],q[2],q[3])])
 for i,j in sorted(occupied):
  a,b=xs[i:i+2];c,d=ys[j:j+2]
  quad([(a,c,h),(b,c,h),(b,d,h),(a,d,h)]);quad([(a,c,0),(a,d,0),(b,d,0),(b,c,0)])
  if(i-1,j)not in occupied:quad([(a,c,0),(a,c,h),(a,d,h),(a,d,0)])
  if(i+1,j)not in occupied:quad([(b,c,0),(b,d,0),(b,d,h),(b,c,h)])
  if(i,j-1)not in occupied:quad([(a,c,0),(b,c,0),(b,c,h),(a,c,h)])
  if(i,j+1)not in occupied:quad([(a,d,0),(a,d,h),(b,d,h),(b,d,0)])
 return triangles

def compose():
 tris=geometry();blob=bytearray();d={'asset':{'version':'2.0','generator':'New connected court-marking mesh'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'name':'AssetRoot__'+ASSET,'children':[1]},{'name':'ContinuousCourtLineNetwork','mesh':0}],'meshes':[],'materials':[{'name':'CourtMarking_Ivory','doubleSided':True,'pbrMetallicRoughness':{'baseColorFactor':[.86,.84,.77,1.],'metallicFactor':0.,'roughnessFactor':.82}}],'accessors':[],'bufferViews':[],'buffers':[]}
 def array(values,component,kind):
  flat=[x for v in values for x in v]if kind=='VEC3'else values;fmt='f'if component==5126 else'I';raw=struct.pack('<'+fmt*len(flat),*flat);offset=len(blob);blob.extend(raw);blob.extend(b'\0'*((-len(blob))%4));vi=len(d['bufferViews']);d['bufferViews'].append({'buffer':0,'byteOffset':offset,'byteLength':len(raw)});a={'bufferView':vi,'componentType':component,'count':len(values),'type':kind}
  if kind=='VEC3':a.update(min=[min(v[k]for v in values)for k in range(3)],max=[max(v[k]for v in values)for k in range(3)])
  ai=len(d['accessors']);d['accessors'].append(a);return ai
 pos=[];normal=[]
 for a,b,c in tris:
  u=[b[k]-a[k]for k in range(3)];v=[c[k]-a[k]for k in range(3)];n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];length=math.sqrt(sum(x*x for x in n));assert length>0;n=[x/length for x in n]
  pos.extend((x,z,-y)for x,y,z in(a,b,c));normal.extend([(n[0],n[2],-n[1])]*3)
 d['meshes']=[{'name':'ContinuousCourtLineNetwork','primitives':[{'attributes':{'POSITION':array(pos,5126,'VEC3'),'NORMAL':array(normal,5126,'VEC3')},'indices':array(list(range(len(pos))),5125,'SCALAR'),'material':0,'mode':4}]}];d['buffers']=[{'byteLength':len(blob)}]
 return d,bytes(blob),{'triangles':len(tris),'new_independent_model_count':1,'scene_count':0,'original_new_numeric_geometry':True,'regulation_dimensions_claim':False}

def pack_glb(doc,blob):
 j=json.dumps(doc,separators=(',',':'),allow_nan=False).encode();j+=b' '*((-len(j))%4)
 b=bytes(blob)+b'\0'*((-len(blob))%4)
 return struct.pack('<4sII',b'glTF',2,12+8+len(j)+8+len(b))+struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(b),0x004e4942)+b

def main():
 import bpy,sys,time
 from mathutils import Vector
 OUT=Path(__file__).resolve().parent
 document,blob,proof=compose();model=pack_glb(document,blob);(OUT/'model.glb').write_bytes(model)
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==1
 triangle_count=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons);assert triangle_count==proof['triangles']
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 lo=[min(v[k]for v in points)for k in range(3)];hi=[max(v[k]for v in points)for k in range(3)]
 assert abs(lo[2])<=TOL and abs(lo[0]+hi[0])<=TOL and abs(lo[1]+hi[1])<=TOL
 assert len({m for o in parts for m in o.data.materials})==1
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
 for layer in scene.view_layers:layer.cycles.use_denoising=False
 scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
 scene.render.resolution_x=scene.render.resolution_y=640;scene.render.resolution_percentage=100
 scene.world=scene.world or bpy.data.worlds.new('Neutral sports studio');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.02))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(11,-16,17));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'),compress=True)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':1,'triangles':triangle_count,'materials':1,'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_rotation_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
 if '--geometry-only' not in sys.argv:
  view=sys.argv[sys.argv.index('--tier-single-view')+1]if '--tier-single-view'in sys.argv else 'thumbnail';assert view in ['qa-front','thumbnail']
  scene.cycles.samples=16 if view=='qa-front' else 128;scene.render.filepath=str(OUT/(view+'.png'));start=time.monotonic();bpy.ops.render.render(write_still=True);qa['render']={'view':view,'samples':scene.cycles.samples,'seconds':time.monotonic()-start,'original_pixels_reviewed':False}
 (OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if p.exists():files[role]={'path':f'assets/sports/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'models','assetKind':'model','theme':'sports','style':'low-poly','title':TITLE,'description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':1,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('ASSET_STAGE_COMPLETE',ASSET,triangle_count)

if __name__=='__main__':main()
