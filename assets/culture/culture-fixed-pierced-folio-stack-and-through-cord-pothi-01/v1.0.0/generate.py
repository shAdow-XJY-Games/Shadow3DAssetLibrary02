import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='culture-fixed-pierced-folio-stack-and-through-cord-pothi-01'
TITLE='Fixed Pierced Folio Stack and Through Cord Pothi'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholePlainCoverBoardsWarmWood',(.28,.12,.041,1),.67),('WholeBlankPalmLookFolioFaces',(.64,.47,.23,1),.90),('WholeThinFolioEdgesWarmOchre',(.46,.31,.13,1),.93),('WholeReturningThroughCordMutedRed',(.29,.055,.035,1),.86)]
G={}

def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
HOLES=[-.09,.09]
HOLE_RADIUS=.0048
BOTTOM=.0037
LEAF_BASE=BOTTOM+.006
LEAF_THICKNESS=.0016
TOP_BASE=LEAF_BASE+8*LEAF_THICKNESS
TOP=TOP_BASE+.006
def pierced_sheet(name,hx,hy,z0,z1,face_mat,edge_mat,bevel=False):
 v=[];ix={};f=[];m=[]
 def V(p):
  p=tuple(round(q,10)for q in p)
  if p not in ix:ix[p]=len(v);v.append(p)
  return ix[p]
 def face(points,mat):f.append(tuple(V(p)for p in points));m.append(mat)
 for k,cx in enumerate(HOLES):
  x0=-hx if k==0 else 0.;x1=0. if k==0 else hx
  angles=sorted(set([round(math.tau*j/16,12)for j in range(16)]+[round(math.atan2(y,x-cx)%math.tau,12)for x in[x0,x1]for y in[-hy,hy]]));outer=[];inner=[]
  for a in angles:
   co,si=math.cos(a),math.sin(a);rx=(x1-cx)/co if co>1e-9 else(x0-cx)/co if co<-1e-9 else 1e9;ry=hy/abs(si)if abs(si)>1e-9 else 1e9;r=min(rx,ry);outer.append((cx+r*co,r*si));inner.append((cx+HOLE_RADIUS*co,HOLE_RADIUS*si))
  inset=[]
  for x,y in outer:inset.append((x-math.copysign(.00035,x)if bevel and abs(abs(x)-hx)<1e-8 else x,y-math.copysign(.00035,y)if bevel and abs(abs(y)-hy)<1e-8 else y))
  for i in range(len(angles)):
   j=(i+1)%len(angles);face([(*inset[i],z1),(*inset[j],z1),(*inner[j],z1),(*inner[i],z1)],face_mat);face([(*inset[j],z0),(*inset[i],z0),(*inner[i],z0),(*inner[j],z0)],face_mat);face([(*inner[j],z0),(*inner[i],z0),(*inner[i],z1),(*inner[j],z1)],edge_mat)
   if not(abs(outer[i][0])<1e-8 and abs(outer[j][0])<1e-8):
    if bevel:
     face([(*inset[i],z0),(*inset[j],z0),(*outer[j],z0+.00028),(*outer[i],z0+.00028)],face_mat)
     face([(*outer[i],z0+.00028),(*outer[j],z0+.00028),(*outer[j],z1-.00028),(*outer[i],z1-.00028)],edge_mat)
     face([(*outer[i],z1-.00028),(*outer[j],z1-.00028),(*inset[j],z1),(*inset[i],z1)],face_mat)
    else:face([(*outer[i],z0),(*outer[j],z0),(*outer[j],z1),(*outer[i],z1)],edge_mat)
 record(name,v,f,m)
def cord_path():
 r=.005;xl,xr=-.09,.09;zb,zt=.0022,TOP+.0015;out=[]
 # Rounded rectangular loop runs through both entire aligned hole columns.
 centers=[(xr-r,zb+r,-math.pi/2,0),(xr-r,zt-r,0,math.pi/2),(xl+r,zt-r,math.pi/2,math.pi),(xl+r,zb+r,math.pi,3*math.pi/2)]
 for j,(x,z,a,b)in enumerate(centers):
  start=(x+r*math.cos(a),z+r*math.sin(a));prev=out[-1]if out else(xl+r,zb)
  for q in range(1,6):t=q/5;out.append((prev[0]+t*(start[0]-prev[0]),prev[1]+t*(start[1]-prev[1])))
  for q in range(1,13):w=a+(b-a)*q/12;out.append((x+r*math.cos(w),z+r*math.sin(w)))
 return out

def whole_cord():
 path=cord_path();N=12;r=.0016;v=[]
 for k,(x,z)in enumerate(path):
  a=path[(k-1)%len(path)];b=path[(k+1)%len(path)];dx,dz=b[0]-a[0],b[1]-a[1];le=math.hypot(dx,dz);normal=(-dz/le,0,dx/le)
  for j in range(N):w=math.tau*j/N+math.pi/N;v.append((x+normal[0]*r*math.sin(w),r*math.cos(w),max(.0009,z+normal[2]*r*math.sin(w))))
 f=[(k*N+j,k*N+(j+1)%N,((k+1)%len(path))*N+(j+1)%N,((k+1)%len(path))*N+j)for k in range(len(path))for j in range(N)];record('WholeClosedThroughHoleAndReturningCord',v,f,3)
def make_geometry():
 G.clear();pierced_sheet('WholeLowerTwinPiercedPlainBoard',.180,.034,BOTTOM,LEAF_BASE,0,0)
 for j in range(8):pierced_sheet('WholeBlankTwinPiercedFolio_%02d'%j,.174,.030,LEAF_BASE+j*LEAF_THICKNESS,LEAF_BASE+(j+1)*LEAF_THICKNESS,1,2,True)
 pierced_sheet('WholeUpperTwinPiercedPlainBoard',.180,.034,TOP_BASE,TOP,0,0);whole_cord()
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole blank pierced folio bundle preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.015))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(3.4,-7.2,6.0));bpy.context.view_layer.update()
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'culture','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete blank pothi-inspired folio bundle in a fixed horizontal display pose. Eight entire narrow landscape folios lie between two complete independent wooden-looking end boards. Every full folio has real shallow upper and lower outer-edge bevels, creating continuous visible layer grooves without changing or separating the central seated faces. Every folio and both boards have two genuine through apertures aligned through the full stack; complete finite hole walls and surrounding leaf material remain present on each separate closed sheet. One whole continuous returning cord passes down one hole column, beneath the lower board, back through the other column and over the upper board. Small finite top and bottom cord contacts locate the entire assembly, with a flattened cord underside as the display datum. No glued side spine, enclosing box, hollow compartment or hinged cover is present. All numerical pierced sheet domains, full cover outlines, folio thicknesses and closed cord route are new. The earlier closed book kit uses continuous U-wrap covers and solid page blocks, the concertina book uses one continuous alternately folded leaf with two end boards, and the nested inro uses hollow compartments with external side-channel bosses. None of those whole organizations or meshes is imported, flattened, extracted or rescaled here. Eleven editable whole closed meshes, four opaque constant paper-look, wood-look and cord-look PBR roles, metre-style native Z up and whole horizontal bounds-centred lower datum. One independent model zero scenes; individual folios and boards are not separately counted. Broad manuscript-form category artwork only: entirely uninscribed, without copied sacred text, floral decoration, specimen measurements, named regional attribution or historic authenticity claim. The fixed closed cord circuit is a simplified visual binding, not a historical knot topology, threading procedure or manufacturing specification. Hidden aligned holes and underside cord are numerically checked, not claimed visible in every image. No page turning, loosening, cord tension, paper/palm species, fibre construction, preservation or conservation advice, adhesive, portability, stability, manufacture or safety capability. No rig, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
