import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='culture-fixed-seat-board-and-bound-paddle-distaff-01'
TITLE='Fixed Seat Board and Bound Paddle Distaff'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeUprightPaddleHoneyWood',(.40,.23,.085,1),.76),('WholeLongSeatBoardDarkWood',(.25,.13,.045,1),.81),('WholePreparedTowAppearancePaleFibre',(.68,.57,.35,1),.92),('WholeContinuousBindingBrownCord',(.19,.105,.037,1),.90)]
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
PADDLE=[(-.022,.014),(.022,.014),(.022,.29),(.046,.32),(.082,.36),(.095,.40),(.095,.68),(.085,.72),(.055,.75),(0,.765),(-.055,.75),(-.085,.72),(-.095,.68),(-.095,.40),(-.082,.36),(-.046,.32),(-.022,.29)]
BASE=[(-.065,.035),(.065,.035),(.078,-.02),(.078,-.32),(.061,-.375),(.035,-.395),(-.035,-.395),(-.061,-.375),(-.078,-.32),(-.078,-.02)]
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
def seat_board():
 p=list(reversed(BASE));n=len(p);v=[]
 for z,sx,sy in[(0,.97,.99),(.003,1,1),(.017,1,1),(.020,.97,.99)]:v +=[(x*sx,-.18+(y+.18)*sy,z)for x,y in p]
 fs=[tuple(reversed(f))for f in triangles2(p)]+[tuple(3*n+i for i in f)for f in triangles2(p)]
 for k in range(3):fs.extend((k*n+i,k*n+(i+1)%n,(k+1)*n+(i+1)%n,(k+1)*n+i)for i in range(n))
 record('WholeLongRoundedSeatBoard',v,fs,1)
def upright_paddle():
 n=len(PADDLE);v=[(x,y,z)for y in[-.010,.010]for x,z in PADDLE];ts=triangles2(PADDLE);fs=ts+[tuple(n+i for i in reversed(f))for f in ts]+[(i,n+i,n+(i+1)%n,(i+1)%n)for i in range(n)];record('WholeNarrowNeckBroadPaddle',v,fs,0)
def fibre_bundle():
 lathe('WholeClosedPreparedTowAppearance',0,[(0,.330),(.025,.340),(.050,.390),(.063,.470),(.066,.540),(.060,.610),(.035,.660),(0,.688)],2,64)
 v,f,m=G['WholeClosedPreparedTowAppearance'];w=[]
 for x,y,z in v:
  angle=math.atan2(y,x);scale=1+.025*math.cos(16*angle);w.append((x*scale,-.031+.40*y*scale,z))
 G['WholeClosedPreparedTowAppearance']=(w,f,m)
def complete_binding():
 points=[];r=.010
 for cx,cy,a0 in[(.082,.0005,0),(-.082,.0005,90),(-.082,-.048,180),(.082,-.048,270)]:
  for k in range(9):
   a=math.radians(a0+90*k/8);points.append((cx+r*math.cos(a),cy+r*math.sin(a),.520))
 v=[];N=8
 for k,c in enumerate(points):
  a=points[k-1];b=points[(k+1)%len(points)];dx,dy=b[0]-a[0],b[1]-a[1];le=math.hypot(dx,dy);normal=(dy/le,-dx/le,0)
  for j in range(N):
   a=math.tau*j/N;v.append((c[0]+.003*normal[0]*math.cos(a),c[1]+.003*normal[1]*math.cos(a),c[2]+.003*math.sin(a)))
 fs=[(k*N+j,k*N+(j+1)%N,((k+1)%len(points))*N+(j+1)%N,((k+1)%len(points))*N+j)for k in range(len(points))for j in range(N)];record('WholeSingleClosedBindingLoop',v,fs,3)
def make_geometry():
 G.clear();seat_board();upright_paddle();fibre_bundle();complete_binding()
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
 scene.world=scene.world or bpy.data.worlds.new('Neutral whole bound paddle distaff preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.38))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(4.8,-7.5,3.8));bpy.context.view_layer.update()
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
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'culture','style':'S01-clean-geometric','title':TITLE,'description':'One newly authored complete fixed seat-board distaff-inspired textile preparation appearance. A long horizontal rounded board rests on its whole finite underside and joins one complete upright paddle through a narrow lower stem. The upper paddle widens into a plain uninscribed rounded head. One closed tapered pale tow-appearance mass sits against its front, with shallow integral longitudinal surface flutes; a single whole finite-thickness cord loop surrounds both the complete mass and paddle at one level. All outlines, thicknesses, bundle profiles, loop coordinates and fixed contacts are original numeric construction. This is a full fibre-holding paddle and seat-board organization, not the earlier spinning wheel with its drive wheel or spindle removed: there is no chassis, wheel, axle, treadle, crank, belt, bobbin or bearing. It is also not a map stand with its surface turned upward: there are no four elevated legs, inclined tabletop, map sheet, islands or pins. Four closed editable whole meshes and four opaque untextured PBR roles, metres native Z up and whole horizontal-bounds-centred ground origin. One model zero scenes; constituent board, mass and cord are not counted separately. Broad traditional textile-tool category inspiration only, not a copy of a museum distaff, authentic regional form, historical carving, measured antique or artisan construction. The pale mass is one simplified closed exterior, not individual flax or wool strands, real fibre structure, prepared material stock or fibre simulation. Cord and concealed attachment overlaps are a static illustrative binding, not a tied knot, tension calculation or assembly specification. No person, seating suitability, spinning, fibre drawing, cloth production, material identity, ergonomics, load capacity, stability, manufacture, handling or safety capability supplied. No spindle accessory, rig, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
