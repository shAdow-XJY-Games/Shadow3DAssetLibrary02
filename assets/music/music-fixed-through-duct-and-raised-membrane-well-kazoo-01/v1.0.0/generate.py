import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='music-fixed-through-duct-and-raised-membrane-well-kazoo-01'
TITLE='Fixed Through Duct and Raised Membrane Well Kazoo'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeTaperedThroughBodyMutedTeal',(.055,.26,.25,1),.61),('WholeRecessedMembraneOpaqueIvory',(.77,.69,.51,1),.86),('WholeOpenRetainerBrassLook',(.52,.34,.12,1),.48),('WholeOpenMouthCollarDark',(.045,.085,.08,1),.72)]
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
OUTLINE=[(-.075,-.012),(-.045,-.020),(.020,-.018),(.075,-.006),(.075,.006),(.020,.018),(-.045,.020),(-.075,.012)]
def outer_hit(a):
 dx,dy=math.cos(a),math.sin(a);hits=[]
 for p,q in zip(OUTLINE,OUTLINE[1:]+OUTLINE[:1]):
  ux,uy=q[0]-p[0],q[1]-p[1];det=dx*uy-dy*ux
  if abs(det)<1e-14:continue
  t=(p[0]*uy-p[1]*ux)/det;u=(p[0]*dy-p[1]*dx)/det
  if t>0 and -1e-8<=u<=1+1e-8:hits.append(t)
 assert hits;v=min(hits);return(v*dx,v*dy)
def through_body():
 angles=sorted(set([round(math.tau*j/48,12)for j in range(48)]+[round(math.atan2(y,x)%math.tau,12)for x,y in OUTLINE]));outer=[outer_hit(a)for a in angles];inner=[]
 for x,y in outer:
  if abs(abs(x)-.075)<1e-10:y*=((.012 if x<0 else .006)-.003)/(.012 if x<0 else .006)
  else:y-=math.copysign(.003,y)
  inner.append((x,y))
 n=len(angles);v=[]
 for ring,z in[(outer,0),(outer,.028),(inner,.004),(inner,.024)]:v.extend((x,y,z)for x,y in ring)
 for radius,z in[(.014,.028),(.014,.049),(.011,.024),(.011,.049)]:v.extend((radius*math.cos(a),radius*math.sin(a),z)for a in angles)
 OB=0;OT=n;IB=2*n;IT=3*n;C=4*n;D=5*n;IC=6*n;ID=7*n;fs=[]
 # Entire outer and inner bottom surfaces; end rims remain genuinely open.
 cb=len(v);v.append((0,0,0));ci=len(v);v.append((0,0,.004))
 for i in range(n):j=(i+1)%n;fs.extend([(cb,OB+j,OB+i),(ci,IB+i,IB+j)])
 ends=[abs(outer[i][0]-outer[(i+1)%n][0])<1e-9 and abs(abs(outer[i][0])-.075)<1e-9 for i in range(n)]
 for i in range(n):
  j=(i+1)%n
  fs.extend([(OT+i,OT+j,C+j,C+i),(IT+i,IC+i,IC+j,IT+j),(C+i,C+j,D+j,D+i),(IC+i,ID+i,ID+j,IC+j),(D+i,D+j,ID+j,ID+i)])
  if not ends[i]:fs.extend([(OB+i,OB+j,OT+j,OT+i),(IB+i,IT+i,IT+j,IB+j)])
  else:fs.extend([(OT+i,IT+i,IT+j,OT+j),(OB+i,OB+j,IB+j,IB+i)])
  if ends[i]!=ends[i-1]:
   f=(OB+i,OT+i,IT+i,IB+i);fs.append(tuple(reversed(f))if ends[i]else f)
 record('WholeTwoOpenEndDuctAndCommunicatingMembraneWell',v,fs,0)
def mouth_collar():
 outer=[(-.0145,0),(.0145,0),(.0145,.031),(-.0145,.031)];inner=[(-.0085,.004),(.0085,.004),(.0085,.024),(-.0085,.024)];v=[]
 for x,p in[(-.078,inner),(-.078,outer),(-.068,outer),(-.068,inner)]:v.extend((x,y,z)for y,z in p)
 fs=[(k*4+i,k*4+(i+1)%4,((k+1)%4)*4+(i+1)%4,((k+1)%4)*4+i)for k in range(4)for i in range(4)];record('WholeOpenRectangularMouthCollar',v,fs,3)
def make_geometry():
 G.clear();through_body();mouth_collar()
 lathe('WholeFixedOpaqueRecessedMembrane',0,[(0,.041),(.01125,.041),(.01125,.042),(0,.042)],1,64)
 lathe('WholeOpenAnnularMembraneRetainer',0,[(.0085,.047),(.017,.047),(.017,.051),(.0085,.051)],2,64)
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
 for i,material in enumerate(d['materials']):material['pbrMetallicRoughness']['metallicFactor']=[0.,0.,.65,0.][i]
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole duct and membrane well preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.025))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(-6.5,-8.0,6.3));bpy.context.view_layer.update()
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete kazoo-inspired static tube-membrane instrument appearance. A whole low elongated tapered body has two genuinely open end mouths connected by a continuous empty internal duct. Its upper wall transitions into one raised cylindrical well with actual continuous inner walls joining the same main duct; no hidden roof plate seals the branch. One complete finite-thickness opaque pale membrane sits recessed inside that well, under one full thick annular retaining cover with a real central opening. A separate whole dark rectangular mouth collar surrounds the broad end without filling its opening. All body outlines, two mouth rims, branch junction, membrane and retainer geometry are original numerical construction. Unlike the earlier wooden whistle, there is no narrow windway feeding a blind chamber, sloping labium, window edge or lanyard: this is a full end-to-end duct with a connected membrane branch. Unlike the closed-bottom side-port clay vessel, there is no bulbous belly or open neck and lateral drum port; the entire straight-through body and covered raised membrane organization is new rather than a vessel profile or hole-count variation. No old source vertices, whole objects or extracted parts are imported. Four closed editable whole meshes, four opaque constant untextured PBR roles, metres native Z up and whole horizontal-bounds-centred ground datum. One independent model zero scenes; membrane and collar do not count separately. Generic unmarked category-inspired art only, no copied brand, patent dimensions, inscription or museum reproduction. The membrane is a visibly thick static opaque disk, not a simulated film; its fixed edge seating and the cover overlaps do not imply a serviceable screw or acoustic seal. No sound, voice modification, pitch, breath or airflow response, hygiene, mouth contact, real membrane vibration, disassembly, fit, manufacture, material authenticity, durability or safety capability. No person, rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
