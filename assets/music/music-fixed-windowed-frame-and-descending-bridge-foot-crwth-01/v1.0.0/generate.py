import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='music-fixed-windowed-frame-and-descending-bridge-foot-crwth-01'
TITLE='Fixed Windowed Frame and Descending Bridge Foot Crwth'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeHollowWindowFrameWarmWood',(.33,.17,.075,1),.77),('WholeSoundboardAndAsymmetricBridgePaleWood',(.67,.46,.23,1),.75),('WholeFretlessBoardNutAndPegsDarkWood',(.13,.073,.036,1),.72),('WholeContinuousUncalibratedStringsPaleAlloy',(.64,.65,.55,1),.53)]
G={}

def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def full_string(name,path):
 N=8;v=[]
 for k,p in enumerate(path):
  a=path[max(0,k-1)];b=path[min(len(path)-1,k+1)];dy,dz=b[1]-a[1],b[2]-a[2];le=math.hypot(dy,dz);u=(0,dz/le,-dy/le)
  for i in range(N):
   q=math.tau*i/N;v.append((p[0]+.0008*math.cos(q),p[1]+.0008*u[1]*math.sin(q),p[2]+.0008*u[2]*math.sin(q)))
 f=[tuple(reversed(range(N))),tuple((len(path)-1)*N+i for i in range(N))]+[(k*N+i,k*N+(i+1)%N,(k+1)*N+(i+1)%N,(k+1)*N+i)for k in range(len(path)-1)for i in range(N)];record(name,v,f,3)
def triangulate(poly):
 def cross(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 ids=list(range(len(poly)));out=[]
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(poly,poly[1:]+poly[:1]))<0:ids.reverse()
 while len(ids)>3:
  for k,b in enumerate(ids):
   a,c=ids[k-1],ids[(k+1)%len(ids)]
   if cross(poly[a],poly[b],poly[c])<=1e-14:continue
   if any(min(cross(poly[a],poly[b],poly[j]),cross(poly[b],poly[c],poly[j]),cross(poly[c],poly[a],poly[j]))>=-1e-14 for j in ids if j not in[a,b,c]):continue
   out.append((a,b,c));ids.pop(k);break
  else:raise AssertionError('Untriangulable authored polygon')
 return out+[tuple(ids)]
def prism(name,poly,a,b,mat,axis='Z'):
 n=len(poly);v=[(x,y,z)if axis=='Z'else(x,z,y)for z in[a,b]for x,y in poly];top=triangulate(poly);fs=[tuple(reversed(q))for q in top]+[tuple(i+n for i in q)for q in top]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];record(name,v,fs,mat)
def whole_frame():
 xs=[-.14,-.128,-.032,.032,.128,.14];ys=[-.32,-.308,.014,.026,.27,.29];zs=[0,.008,.043,.052];cells=set()
 for i in range(5):
  for j in range(3):cells.add((i,j,0))
 for i in range(5):
  for j in range(5):
   if j<3 and(i in[0,4]or j in[0,2]):cells.add((i,j,1))
   if j>=3 and(i in[0,2,4]or j==4):
    for k in[1,2]:cells.add((i,j,k))
 verts=[];look={};faces=[]
 def ix(p):
  if p not in look:look[p]=len(verts);verts.append(p)
  return look[p]
 # Every grid cell has consistent faces; internal facets are removed before triangulation.
 sides=[((-1,0,0),[(0,0,0),(0,0,1),(0,1,1),(0,1,0)]),((1,0,0),[(1,0,0),(1,1,0),(1,1,1),(1,0,1)]),((0,-1,0),[(0,0,0),(1,0,0),(1,0,1),(0,0,1)]),((0,1,0),[(0,1,0),(0,1,1),(1,1,1),(1,1,0)]),((0,0,-1),[(0,0,0),(0,1,0),(1,1,0),(1,0,0)]),((0,0,1),[(0,0,1),(1,0,1),(1,1,1),(0,1,1)])]
 for i,j,k in sorted(cells):
  for (di,dj,dk),face in sides:
   if(i+di,j+dj,k+dk)not in cells:faces.append(tuple(ix((xs[i+a],ys[j+b],zs[k+c]))for a,b,c in face))
 record('WholeFlatBackCavitySidesAndWindowNeckFrame',verts,faces,0)
def pierced_soundboard():
 # Two mirror half-domains form ONE closed board with two true circular apertures.
 cx,cy=.082,-.09;angles=sorted(set([round(math.tau*k/40,12)for k in range(40)]+[round(math.atan2(y-cy,x-cx)%math.tau,12)for x,y in[(0,-.32),(.14,-.32),(.14,.026),(0,.026)]]))
 verts=[];look={};facemap={}
 def ix(p):
  p=tuple(round(q,11)for q in p)
  if p not in look:look[p]=len(verts);verts.append(p)
  return look[p]
 for sg in[-1,1]:
  rows=[]
  for hole,z in[(False,.041),(False,.052),(True,.052),(True,.041)]:
   row=[]
   for a in angles:
    dx,dy=math.cos(a),math.sin(a)
    hits=[((.14 if dx>0 else 0)-cx)/dx]if abs(dx)>1e-10 else[]
    if abs(dy)>1e-10:hits.append(((.026 if dy>0 else -.32)-cy)/dy)
    r=.022 if hole else min(hits);row.append(ix((sg*(cx+r*dx),cy+r*dy,z)))
   rows.append(row)
  for aa,bb in zip(rows,rows[1:]+rows[:1]):
   for i in range(len(angles)):
    j=(i+1)%len(angles);f=(aa[i],aa[j],bb[j],bb[i]);f=f if sg==1 else tuple(reversed(f));key=tuple(sorted(f))
    if key in facemap:del facemap[key]
    else:facemap[key]=f
 record('WholeTwoApertureSoundboard',verts,list(facemap.values()),1)
def peg(name,x):
 n=12;profile=[(.0035,.044),(.0035,.094),(.0065,.094),(.0065,.102)];v=[(x+r*math.cos(math.tau*i/n),.279+r*math.sin(math.tau*i/n),z)for r,z in profile for i in range(n)];f=[tuple(reversed(range(n))),tuple(3*n+i for i in range(n))]+[(k*n+i,k*n+(i+1)%n,(k+1)*n+(i+1)%n,(k+1)*n+i)for k in range(3)for i in range(n)];record(name,v,f,2)
def make_geometry():
 G.clear();whole_frame();pierced_soundboard()
 prism('WholeCentralFretlessFingerboard',[(-.028,-.02),(.028,-.02),(.028,.274),(-.028,.274)],.051,.065,2)
 prism('WholeShortUpperNut',[(-.033,.251),(.033,.251),(.033,.259),(-.033,.259)],.064,.078,2)
 prism('WholeLowerStringAnchor',[(-.107,-.272),(.035,-.272),(.035,-.246),(-.107,-.246)],.050,.073,2)
 # The right whole bridge leg passes through its true hole to the inner back, not a hidden separate post.
 shape=[(-.110,.076),(-.055,.076),(-.055,.050),(-.041,.050),(-.041,.076),(.074,.076),(.074,.006),(.090,.006),(.090,.085),(-.110,.085)]
 prism('WholeBridgeWithOneDescendingThroughHoleFoot',shape,-.096,-.084,1,axis='Y')
 for i,x in enumerate([-.095,-.075,-.021,-.007,.007,.021]):
  peg('WholeUpperTuningPeg_%d'%i,x)
  path=[(x,-.257,.072),(x,-.090,.0847)]
  if i>=2:path.append((x,.255,.0777))
  path.append((x,.279,.086));full_string('WholeContinuousDisplayString_%d'%i,path)
 points=[p for v,f,m in G.values()for p in v];lo=[min(p[k]for p in points)for k in range(3)];hi=[max(p[k]for p in points)for k in range(3)]
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole windowed frame instrument preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.045))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(3.6,-5.0,7.8));bpy.context.view_layer.update()
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete crwth-inspired static frame instrument lying on its whole flat back. One connected lower back, hollow chamber sides, outer upper frame and central neck create two large true upper windows. A whole thin soundboard closes the lower chamber except for two actual circular apertures. The central fretless fingerboard crosses the upper window region and extends over the chamber. A single complete asymmetric bridge has a short left foot seated on the top board and a long right foot passing with positive clearance through the right aperture to the inner back. Four whole strings cross the fingerboard nut and two whole lateral strings run alongside it; all six terminate in one lower anchor and their separate upper pegs. This whole support and cavity organization is new, not the bowl-back lyre with extra strings or a reshaped violin: there are no separate curved lyre arms, bowl shell, projecting violin neck, scroll, pegbox or f holes. Every numeric frame, aperture, bridge and fitting shape is independently authored, not imported or extracted. Eighteen closed editable whole component meshes, four opaque constant PBR roles, metres native Z up and whole horizontal-bounds-centred ground origin. One model zero scenes; subordinate strings and pegs are never extra assets. Generic uninscribed cultural instrument-category artwork, not an authentic measured historical specimen, regional tuning or reproduction. The whole central neck is solid; the historical hidden fingerboard cavity is deliberately not reconstructed. No bow, player, tuning markings, string windings, sound, pitch, tension, acoustic transmission, playing technique, operation, structural balance, manufacture or safety capability is made or verified. No rigging animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
