import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='music-fixed-front-stop-panel-and-rear-wedge-bellows-drone-box-01'
TITLE='Fixed Front Stop Panel and Rear Wedge Bellows Drone Box'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeUprightCabinetWarmWood',(.36,.19,.075,1),.78),('WholeWedgeBellowsDeepWine',(.20,.055,.050,1),.88),('WholeBlankStopTabsIvory',(.72,.64,.46,1),.72),('WholeStopPivotBrass',(.50,.33,.11,1),.48)]
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
def axis_lathe(name,c,axis,profile,mat,N=32):
 lathe(name,0,[(r,t)for t,r in profile],mat,N);v,f,m=G[name]
 if axis=='X':v=[(c[0]+z,c[1]+x,c[2]+y)for x,y,z in v]
 elif axis=='Y':v=[(c[0]+y,c[1]+z,c[2]+x)for x,y,z in v]
 else:v=[(c[0]+x,c[1]+y,c[2]+z)for x,y,z in v]
 G[name]=(v,f,m)
def extrude(name,p,y0,y1,mat):
 n=len(p);v=[(x,y,z)for y in[y0,y1]for x,z in p];ts=triangles2(p);fs=ts+[tuple(n+i for i in reversed(f))for f in ts]+[(i,n+i,n+(i+1)%n,(i+1)%n)for i in range(n)];record(name,v,fs,mat)
DIRECTIONS=[((-1,0,0),[(0,0,0),(0,0,1),(0,1,1),(0,1,0)]),((1,0,0),[(1,0,0),(1,1,0),(1,1,1),(1,0,1)]),((0,-1,0),[(0,0,0),(1,0,0),(1,0,1),(0,0,1)]),((0,1,0),[(0,1,0),(0,1,1),(1,1,1),(1,1,0)]),((0,0,-1),[(0,0,0),(0,1,0),(1,1,0),(1,0,0)]),((0,0,1),[(0,0,1),(1,0,1),(1,1,1),(0,1,1)])]
PORTS=[(x,z)for z in[.125,.205]for x in[-.120,-.040,.040,.120]]
OPEN={1:75,6:-75}
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
def case():
 xs=sorted(set([-.180,-.166,.166,.180]+[x+d for x,z in PORTS for d in[-.014,.014]]));ys=[-.045,-.033,.025];zs=sorted(set([.018,.032,.264,.278]+[z+d for x,z in PORTS for d in[-.009,.009]]))
 def solid(x,y,z):return(abs(x)>.166 or z<.032 or z>.264 or y<-.033)and not(y<-.033 and any(abs(x-cx)<.014 and abs(z-cz)<.009 for cx,cz in PORTS))
 cells_boundary('WholeHollowUprightCabinetAndEightPortFront',xs,ys,zs,solid,0)
def board_y(z):return .035+.115*(z-.032)/.232
def bellows():
 v=[];count=11
 for k in range(count):
  t=k/(count-1);w,h=(.174,.124)if k in[0,count-1]else(.178,.124)if k%2 else(.164,.114)
  for x,z in[(-w,.148-h),(w,.148-h),(w,.148+h),(-w,.148+h)]:v.append((x,.023+t*(board_y(z)-.023),z))
 fs=[(3,2,1,0),tuple((count-1)*4+j for j in range(4))]+[(k*4+j,k*4+(j+1)%4,(k+1)*4+(j+1)%4,(k+1)*4+j)for k in range(count-1)for j in range(4)];record('WholeContinuousFiveFoldRearWedgeBellowsExterior',v,fs,1)
 v=[(x,board_y(z)+d,z)for d in[-.002,.010]for x,z in[(-.180,.020),(.180,.020),(.180,.276),(-.180,.276)]];record('WholeFixedInclinedRearPumpBoard',v,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],0)
def box(name,lo,hi,mat):
 v=[(x,y,z)for z in[lo[2],hi[2]]for y in[lo[1],hi[1]]for x in[lo[0],hi[0]]];record(name,v,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],mat)
def stop(k,cx,cz):
 p=[(-.014,-.016),(.014,-.016),(.018,-.012),(.018,.028),(.014,.032),(-.014,.032),(-.018,.028),(-.018,-.012)];a=math.radians(OPEN.get(k,0));co,sn=math.cos(a),math.sin(a);q=[(cx+x*co+(z-.024)*sn,cz+.024-x*sn+(z-.024)*co)for x,z in p];extrude('WholeFixedSwivelStopTab_'+str(k),q,-.053,-.049,2)
 axis_lathe('WholeStopPivot_'+str(k),(cx,0,cz+.024),'Y',[(-.057,0),(-.057,.005),(-.054,.005),(-.053,.0035),(-.038,.0035),(-.038,0)],3,24)
def make_geometry():
 G.clear();case();bellows()
 for k,(x,z)in enumerate(PORTS):stop(k,x,z)
 for x,label in[(-.132,'Left'),(.132,'Right')]:box('Whole'+label+'GroundShoe',(x-.025,-.055,0),(x+.025,.060,.022),0)
 cells_boundary('WholeOpenTopCarryLoop',[-.060,-.042,.042,.060],[-.020,.010],[.274,.290,.312,.326],lambda x,y,z:abs(x)>.042 or z>.312,0)
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
 for i,material in enumerate(d['materials']):material['pbrMetallicRoughness']['metallicFactor']=[0.,0.,0.,.65][i]
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole upright drone box preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.165))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(6.0,-8.0,5.2));bpy.context.view_layer.update()
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete shruti-box-inspired fixed drone-instrument exterior. A whole upright wooden-look cabinet has a real shallow inner cavity, eight genuine front rectangular ports in two rows and a complete open top carry loop. Eight whole unmarked swivel-tab appearances have complete fixed pivot heads; six cover their ports and two are turned aside so the real openings remain visible. A single continuous five-fold wedge-shaped bellows exterior expands behind the cabinet toward one complete inclined rear pump board, narrow at the lower hinge-like region and broader at the top. Two full low shoes support the complete instrument. The original cabinet, front stop organization, rear fan-shaped pump arrangement and whole supports are designed together, not an accordion with keyboard parts deleted. Unlike the earlier two-ended keyboard accordion, there is no central expanding bridge between two deep end cases, keyboard backing or separate button case. Unlike the pear-shaped workshop hand bellows, there are no extended paired grasp handles or projecting nozzle, and the fixed wedge forms the rear of a front-port upright instrument body rather than a hand-held pear bag. Every numerical body boundary, port, tab outline, bellows station, board and support is original; no old instrument or bellows mesh imported. Twenty-two closed editable complete meshes, four opaque constant untextured PBR roles, metres native Z up and full horizontal-bounds-centred ground datum. One original model zero scenes; tabs are components, not extra assets. Unmarked broad category art, not a particular regional specimen, brand, authentic note layout, museum reconstruction or exact construction plan. Front cavity and ports are real visual negative spaces, but the folded rear bag is a closed stylized exterior, not an internally resolved pneumatic chamber. No internal reeds or valve system, wax, airflow, tuning, pitch, sound, bellows motion, hinge travel, airtightness, carrying strength, ergonomics, stability, manufacture or safety capability is supplied or tested. No rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
