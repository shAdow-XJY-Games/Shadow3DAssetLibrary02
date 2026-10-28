import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='textile-fixed-open-three-plate-frame-and-opaque-optic-linen-tester-01'
TITLE='Fixed Open Three Plate Frame and Opaque Optic Linen Tester'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeThreePlateSatinFrame',(.33,.38,.37,1),.48),('WholeFixedHingePinsWarmMetal',(.49,.34,.15,1),.48),('WholeOpaqueOpticalAppearance',(.055,.11,.13,1),.30),('WholeBlankLowerFieldFace',(.55,.48,.31,1),.61)]
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
DIRECTIONS=[((-1,0,0),[(0,0,0),(0,0,1),(0,1,1),(0,1,0)]),((1,0,0),[(1,0,0),(1,1,0),(1,1,1),(1,0,1)]),((0,-1,0),[(0,0,0),(1,0,0),(1,0,1),(0,0,1)]),((0,1,0),[(0,1,0),(0,1,1),(1,1,1),(1,1,0)]),((0,0,-1),[(0,0,0),(0,1,0),(1,1,0),(1,0,0)]),((0,0,1),[(0,0,1),(1,0,1),(1,1,1),(0,1,1)])]
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
def upper_plate():
 cy=-.001;angles=sorted(set([math.tau*j/64 for j in range(64)]+[math.atan2(y-cy,x)%math.tau for x in[-.032,.032]for y in[-.031,.032]]));outer=[];inner=[]
 for a in angles:
  x,y=math.cos(a),math.sin(a);tx=.032/abs(x)if abs(x)>1e-12 else 1e9;ty=((.032-cy)if y>0 else(-.031-cy))/y if abs(y)>1e-12 else 1e9;t=min(tx,ty);outer.append((x*t,cy+y*t));inner.append((.023*x,cy+.023*y))
 n=len(angles);v=[(x,y,z)for p,z in[(outer,.062),(outer,.066),(inner,.066),(inner,.062)]for x,y in p];fs=[]
 for k in range(4):
  for i in range(n):j=(i+1)%n;fs.append((k*n+i,k*n+j,((k+1)%4)*n+j,((k+1)%4)*n+i))
 record('WholeUpperPlateWithCircularOpticSeat',v,fs,0)
def make_geometry():
 G.clear()
 cells_boundary('WholeLowerPlateWithSquareCountingOpening',[-.032,-.019,.019,.032],[-.031,-.018,.018,.032],[0,.004],lambda x,y,z:not(abs(x)<.019 and abs(y)<.018),0)
 v,f,m=G['WholeLowerPlateWithSquareCountingOpening'];m=[3 if all(abs(v[j][2]-.004)<1e-10 for j in tri)else 0 for tri in f];G['WholeLowerPlateWithSquareCountingOpening']=(v,f,m)
 cells_boundary('WholeRearPlateWithOpenRectangle',[-.032,-.019,.019,.032],[.028,.032],[.003,.018,.048,.065],lambda x,y,z:not(abs(x)<.019 and .018<z<.048),0)
 upper_plate()
 lathe('WholeOpaqueBiconvexOpticAppearance',0,[(0,.0608),(.016,.0618),(.0236,.063),(.0236,.065),(.016,.067),(0,.068)],2,48);v,f,m=G['WholeOpaqueBiconvexOpticAppearance'];G['WholeOpaqueBiconvexOpticAppearance']=([(x,y-.001,z)for x,y,z in v],f,m)
 for z,level in[(.005,'Lower'),(.063,'Upper')]:
  for x,side in[(-.021,'Left'),(.021,'Right')]:axis_lathe('Whole'+level+side+'HingeBarrel',(x,.030,z),'X',[(-.006,0),(-.006,.0035),(.006,.0035),(.006,0)],1,24)
  axis_lathe('Whole'+level+'AcrossFrameHeadedPin',(0,.030,z),'X',[(-.038,0),(-.038,.003),(-.034,.003),(-.034,.0018),(.034,.0018),(.034,.003),(.038,.003),(.038,0)],1,24)
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
 for i,material in enumerate(d['materials']):material['pbrMetallicRoughness']['metallicFactor']=[.56,.61,0.,.35][i]
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole folding linen tester preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.034))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(5.0,-8.0,4.2));bpy.context.view_layer.update()
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
  if p.exists():files[role]={'path':f'assets/textile/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'textile','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete fixed linen-tester-inspired textile and print-inspection frame exterior. Three whole thick plates form an open-front C arrangement: a flat lower plate has a genuinely full-through rectangular counting-field opening; the upright rear plate has its own large true rectangular window; and the upper plate surrounds an actual circular optic seat. One full softly biconvex opaque dark optical-appearance body occupies that upper seat. Four complete hinge-barrel exteriors and two whole headed transverse pins define both plate joints. All numeric plate openings, full convex optic profile, hinge barrels and pin profiles are independently authored. Unlike the older column microscope, there is no heavy base, upright focus column, long optical tube, objective, specimen platform or focus wheel; this is a compact three-plate folding-frame organization, not a reduced microscope. Unlike the two-leaf cord dial, it has no upright dial face, blind compass cup, needle or diagonal cord, but an upper optic aligned over an open lower measuring field. No old lenses, plates, boxes, book leaves, clocks or mesh fragments imported or extracted. Ten closed whole editable meshes, four opaque constant untextured PBR roles, metre-style native Z up and full horizontal-bounds-centred ground datum. One independent model zero scenes. Generic unbranded inspection-tool appearance with invented dimensions and blank surfaces; not a product replica or verified folding design. The lens is deliberately opaque, not optical glass, a transparent viewport or a view of magnified fabric. No magnification, focusing, measuring scale, calibrated field size, thread counting, image formation, cloth or print quality evaluation, authentication, folding movement, hinge fit, human suitability, manufacture or safety capability made or verified. No labels, ticks, fabric, rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
