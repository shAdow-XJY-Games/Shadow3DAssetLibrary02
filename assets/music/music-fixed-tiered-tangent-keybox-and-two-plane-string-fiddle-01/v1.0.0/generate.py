import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='music-fixed-tiered-tangent-keybox-and-two-plane-string-fiddle-01'
TITLE='Fixed Tiered Tangent Keybox and Two Plane String Fiddle'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeBodyNeckGuideWarmMaple',(.40,.20,.070,1),.75),('WholeWaistedSoundboardAndBridgePaleWood',(.70,.48,.23,1),.72),('WholeTangentKeysNutsAndPegsDarkTimber',(.12,.065,.028,1),.72),('WholeTwoLevelStringsMutedSilver',(.61,.65,.62,1),.50)]
G={}

def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
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
def full_string(name,path,radius):
 N=8;v=[]
 for k,p in enumerate(path):
  a=path[max(0,k-1)];b=path[min(len(path)-1,k+1)];dy,dz=b[1]-a[1],b[2]-a[2];le=math.hypot(dy,dz);u=(0,dz/le,-dy/le)
  for i in range(N):
   q=math.tau*i/N;v.append((p[0]+radius*math.cos(q),p[1]+radius*u[1]*math.sin(q),p[2]+radius*u[2]*math.sin(q)))
 f=[tuple(reversed(range(N))),tuple((len(path)-1)*N+i for i in range(N))]+[(k*N+i,k*N+(i+1)%N,(k+1)*N+(i+1)%N,(k+1)*N+i)for k in range(len(path)-1)for i in range(N)];record(name,v,f,3)
def grid(name,xs,ys,zs,cells,mat):
 verts=[];look={};faces=[]
 def ix(p):
  if p not in look:look[p]=len(verts);verts.append(p)
  return look[p]
 sides=[((-1,0,0),[(0,0,0),(0,0,1),(0,1,1),(0,1,0)]),((1,0,0),[(1,0,0),(1,1,0),(1,1,1),(1,0,1)]),((0,-1,0),[(0,0,0),(1,0,0),(1,0,1),(0,0,1)]),((0,1,0),[(0,1,0),(0,1,1),(1,1,1),(1,1,0)]),((0,0,-1),[(0,0,0),(0,1,0),(1,1,0),(1,0,0)]),((0,0,1),[(0,0,1),(1,0,1),(1,1,1),(0,1,1)])]
 for i,j,k in sorted(cells):
  for(di,dj,dk),face in sides:
   if(i+di,j+dj,k+dk)not in cells:faces.append(tuple(ix((xs[i+a],ys[j+b],zs[k+c]))for a,b,c in face))
 record(name,verts,faces,mat)
YS=[-.34,-.31,-.25,-.18,-.13,-.07,0,.08,.15,.20]
WS=[.045,.10,.14,.135,.13,.075,.08,.12,.10,.05]
ROWS=[(k,.08+.04*k,.132,-.030,-.027)for k in range(8)]+[(8+k,.10+.08*k,.106,-.014,-.011)for k in range(4)]
MAIN_X=[-.023,-.007,.009,.025];LOW_X=[.044,.053,.062,.071,.080,.089]
def body():
 p=[(w,y)for y,w in zip(YS,WS)]+[(-w,y)for y,w in reversed(list(zip(YS,WS)))];prism('WholeWaistedFlatBack',p,0,.009,0)
 outer=[(x*.985,-.07+(y+.07)*.99)for x,y in p];inner=[(x*.90,-.07+(y+.07)*.965)for x,y in p];N=len(p);v=[(x,y,z)for z in[.007,.070]for poly in[outer,inner]for x,y in poly];f=[]
 for i in range(N):
  j=(i+1)%N;f.extend([(i,j,N+j,N+i),(2*N+i,3*N+i,3*N+j,2*N+j),(i,2*N+i,2*N+j,j),(N+i,N+j,3*N+j,3*N+i)])
 record('WholeInsetWaistedCavityRibRing',v,f,0)
 # One continuous whole top board; missing cells are actual bounded apertures, not dark overlays.
 fr=[-1,-.75,-.42,.42,.75,1];v=[];look={};faces=[];edges={}
 def ix(p):
  p=tuple(round(q,12)for q in p)
  if p not in look:look[p]=len(v);v.append(p)
  return look[p]
 for j in range(len(YS)-1):
  for i in range(5):
   if j==2 and i in[1,3]:continue
   poly=[(WS[j]*fr[i],YS[j]),(WS[j]*fr[i+1],YS[j]),(WS[j+1]*fr[i+1],YS[j+1]),(WS[j+1]*fr[i],YS[j+1])]
   faces.append(tuple(ix((x,y,.074))for x,y in poly));faces.append(tuple(ix((x,y,.066))for x,y in reversed(poly)))
   for a,b in zip(poly,poly[1:]+poly[:1]):
    key=tuple(sorted((a,b)))
    if key in edges:del edges[key]
    else:edges[key]=(a,b)
 for a,b in edges.values():faces.append((ix((*a,.066)),ix((*b,.066)),ix((*b,.074)),ix((*a,.074))))
 record('WholeWaistedBoardWithTwinBoundedSoundSlots',v,faces,1)
def guide(name,x0,x1):
 ys=sorted(set([.052,.402]+[round(y+d,12)for k,y,z,pl,pr in ROWS for d in[-.007,.007]]));zs=[.088,.100,.114,.126,.140,.148];cells=set()
 for j in range(len(ys)-1):
  for k in range(len(zs)-1):
   yc=(ys[j]+ys[j+1])/2;zc=(zs[k]+zs[k+1])/2
   hole=any(abs(yc-y)<.007-1e-9 and z-.006<zc<z+.008 for _,y,z,pl,pr in ROWS)
   if not hole:cells.add((0,j,k))
 grid(name,[x0,x1],ys,zs,cells,0)
def whole_key(k,y,z,pl,pr):
 xs=sorted(set([-.198,-.180,-.172,pl,pr,.044]));ys=[y-.011,y-.005,y+.005,y+.011];zs=[z-.0065,z+.004,z+.010,.169];cells=set()
 for i in range(len(xs)-1):
  for j in range(3):
   for kk in range(3):
    x=(xs[i]+xs[i+1])/2;yy=(ys[j]+ys[j+1])/2;zz=(zs[kk]+zs[kk+1])/2
    stem=-.180<x<.044 and abs(yy-y)<.005 and zz<z+.004
    button=-.198<x<-.172 and zz<z+.010
    tangent=pl<x<pr and abs(yy-y)<.005
    if stem or button or tangent:cells.add((i,j,kk))
 grid('WholeKeyStemButtonAndUprightTangent_%02d'%k,xs,ys,zs,cells,2)
def peg(name,x,y,top):
 N=12;v=[(x+r*math.cos(math.tau*i/N),y+r*math.sin(math.tau*i/N),z)for r,z in[(.0026,.110),(.0026,top-.006),(.004,top-.006),(.004,top)]for i in range(N)];f=[tuple(reversed(range(N))),tuple(3*N+i for i in range(N))]+[(k*N+i,k*N+(i+1)%N,(k+1)*N+(i+1)%N,(k+1)*N+i)for k in range(3)for i in range(N)];record(name,v,f,2)
def make_geometry():
 G.clear();body();prism('WholeProjectingKeyNeck',[(-.048,.035),(.050,.035),(.050,.53),(-.048,.53)],.043,.092,0)
 prism('WholeWideTwoBankPegHead',[(-.070,.44),(.110,.44),(.110,.54),(.098,.55),(-.058,.55),(-.070,.54)],.078,.118,0)
 guide('WholeLeftTwoTierSlottedGuideRail',-.055,-.043);guide('WholeRightTwoTierSlottedGuideRail',.030,.042)
 for args in ROWS:whole_key(*args)
 shape=[(-.055,.072),(-.035,.072),(-.035,.103),(.075,.103),(.075,.072),(.098,.072),(.098,.123),(.037,.123),(.037,.176),(-.055,.176)]
 prism('WholeSteppedTwoPlaneStringBridge',shape,-.116,-.104,1,axis='Y')
 prism('WholeWideTailStringAnchor',[(-.055,-.300),(.10,-.300),(.10,-.270),(-.055,-.270)],.072,.108,2)
 prism('WholeHighMelodyNut',[(-.031,.451),(.033,.451),(.033,.461),(-.031,.461)],.116,.171,2)
 prism('WholeLowResonanceNut',[(.037,.451),(.100,.451),(.100,.461),(.037,.461)],.116,.125,2)
 for i,x in enumerate(MAIN_X):
  peg('WholeMelodyPeg_%d'%i,x,.51,.182);full_string('WholeUpperMelodyString_%d'%i,[(x,-.281,.107),(x,-.11,.1757),(x,.456,.1707),(x,.51,.175)],.0008)
 for i,x in enumerate(LOW_X):
  peg('WholeResonancePeg_%d'%i,x,.535,.134);full_string('WholeLowerResonanceString_%d'%i,[(x,-.281,.107),(x,-.11,.1227),(x,.456,.1247),(x,.535,.128)],.00055)
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole tiered key fiddle preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.045))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(-4.1,-5.5,7.0));bpy.context.view_layer.update()
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete keyed-fiddle-inspired fixed instrument. A full waisted flat-back chamber has separate inset ribs and one complete top board with two genuine bounded sound slots. One long projecting neck carries two entire slotted guide rails and twelve whole keys, each with an integral side button, transverse stem and upright tangent; the two staggered levels have actual open guide apertures and are held in one resting display position. A whole stepped bridge and separate high and low nuts carry four upper melody strings and six lower resonance strings to independent complete peg banks on a wide head. The twin string planes stay separate along the long neck and bridge, with small clear space between the unpressed visual tangents and the upper strings. This complete keyed-neck and stepped-string support organization is original, not the old hurdy-gurdy with its wheel removed: there is no wheel slot, axle, crank or end handle, and the fully hollow waisted body, projecting two-tier slotted neck and lower string plane are new throughout. Unlike the carved violin there is no fingerboard, volute, side-peg box or paired f holes. No prior visible mesh or numerical instrument part imported or extracted. All whole keys, strings and pegs are subordinate components of one model, zero scenes. Four constant opaque PBR roles, metres native Z up and whole horizontal-bounds-centred flat back datum. Generic unbranded nyckelharpa-category art only, not a measured museum instrument, authentic chromatic layout, tuning, model or reconstruction. Deliberate fixed small seating overlaps establish visual support rather than solved sliding clearances. No bow, player, note markings, sounding sympathetic response, key action, pitch, tension, playing, friction, acoustics, ergonomics, structural load, manufacture or safety capability is made or verified. No rigging animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
