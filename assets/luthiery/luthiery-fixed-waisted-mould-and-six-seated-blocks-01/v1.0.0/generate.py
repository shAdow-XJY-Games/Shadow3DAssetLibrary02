import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='luthiery-fixed-waisted-mould-and-six-seated-blocks-01'
TITLE='Fixed Waisted Mould and Six Seated Blocks'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeMouldUpperWarmWood',(.35,.205,.082,1),.80),('WholeMouldCutWallDarkWood',(.22,.12,.045,1),.82),('WholeUnshapedBlockSidesPaleWood',(.60,.45,.24,1),.85),('WholeUnshapedBlockTopsLightWood',(.77,.63,.39,1),.84)]
G={}

def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def triangles2(poly):
 def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 assert sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(poly,poly[1:]+poly[:1]))>0
 live=list(range(len(poly)));result=[]
 while len(live)>3:
  for k,b in enumerate(live):
   a,c=live[k-1],live[(k+1)%len(live)]
   if cross(poly[a],poly[b],poly[c])<=1e-12:continue
   if any(all(cross(poly[u],poly[v],poly[q])>=-1e-12 for u,v in[(a,b),(b,c),(c,a)])for q in live if q not in[a,b,c]):continue
   result.append((a,b,c));live.pop(k);break
  else:raise AssertionError('Non-simple polygon')
 return result+[tuple(live)]
HALF=[(0,-.163),(.023,-.163),(.023,-.178),(.045,-.170),(.064,-.159),(.080,-.144),(.090,-.124),(.093,-.103),(.088,-.086),(.080,-.075),(.082,-.062),(.060,-.062),(.060,-.038),(.073,-.038),(.061,-.025),(.054,-.010),(.052,.004),(.057,.023),(.070,.039),(.056,.039),(.056,.061),(.078,.061),(.084,.081),(.082,.101),(.075,.121),(.062,.140),(.044,.155),(.021,.164),(.021,.151),(0,.151)]
BLOCKS=[('LowerEnd',(-.0235,-.183),(.0235,-.162)),('UpperEnd',(-.0215,.150),(.0215,.171)),('LowerRight',(.059,-.0625),(.086,-.0375)),('LowerLeft',(-.086,-.0625),(-.059,-.0375)),('UpperRight',(.055,.0385),(.082,.0615)),('UpperLeft',(-.082,.0385),(-.055,.0615))]
def whole_mould():
 outer=HALF+[(-x,y)for x,y in reversed(HALF[1:-1])];inner_right=[(.026*math.sin(math.pi*j/32),.095*math.cos(math.pi*j/32))for j in range(33)];inner_right[0]=(0,.095);inner_right[-1]=(0,-.095)
 right=HALF+inner_right;left=[(-x,y)for x,y in reversed(right)];verts=[];ix={};fs=[];mats=[]
 def vertex(p):
  p=tuple(p)
  if p not in ix:ix[p]=len(verts);verts.append(p)
  return ix[p]
 for poly in[right,left]:
  for t in triangles2(poly):
   fs.append(tuple(vertex((*poly[i],.026))for i in t));mats.append(0);fs.append(tuple(vertex((*poly[i],0))for i in reversed(t)));mats.append(1)
 inner=inner_right+[(-x,y)for x,y in reversed(inner_right[1:-1])]
 for boundary in[outer,inner]:
  for a,b in zip(boundary,boundary[1:]+boundary[:1]):fs.append((vertex((*a,0)),vertex((*b,0)),vertex((*b,.026)),vertex((*a,.026))));mats.append(1)
 record('WholeNotchedWaistedMouldWithLongThroughOpening',verts,fs,mats)
def whole_block(label,lo,hi):
 x0,y0=lo;x1,y1=hi;v=[(x,y,z)for z in[0,.041]for y in[y0,y1]for x in[x0,x1]];f=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];record('WholeSeated'+label+'Block',v,f,[2,3,2,2,2,2])
def make_geometry():
 G.clear();whole_mould()
 for label,lo,hi in BLOCKS:whole_block(label,lo,hi)
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole luthier mould preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.020))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(4.8,-7.0,10.0));bpy.context.view_layer.update()
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'luthiery','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete fixed luthier internal-mould-inspired workshop tool assembly. A full thick wooden-look waisted form has two broad unequal end lobes, four interrupted corner shoulders, six genuine perimeter notches and one long central through opening. Six entire unshaped pale block exteriors sit in the two end seats and four corner seats, rising above the form while retaining full flat ground faces. The form remains one closed continuous material body around the empty long opening; its outer notch walls and full upper/lower faces are actual geometry. Every contour point, notch boundary, elliptical through-opening, block and support coordinate is original. This is a complete fixed empty mould-with-blocks appearance, not an incomplete violin asset or a violin with its neck, strings and boards deleted. Unlike the old hollow waisted violin, it has no acoustic chamber, rib shell, top/back pair, f holes, neck or string fittings; its thick central tool plate, central access void and external block seats define a different complete object. No previous violin outline, mesh, rib ring, backplate or acoustic cavity is reused, extracted or resized. Seven closed editable whole meshes, four opaque constant untextured PBR roles, metres native Z up and full horizontal-bounds-centred ground datum. One original model zero scenes; the six blocks remain subordinate to the complete fixture. Generic maker-tool category art only, not a famous makers mould, instrument-size pattern, measured historical reconstruction or manufacturing plan. No wood ribs, lining, clamping workpiece, glue, authentic block grain, mounting screws or usable pattern measurements. Fixed overlaps deliberately join the blocks to their seats; no removable fit, instrument compatibility, rib-forming accuracy, pressure, stability, load, hand fit, material performance, manufacture or safety capability is provided or verified. No animation, rigging or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
