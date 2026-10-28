'One independently authored complete empty weighted-training-vest-inspired static exterior. One continuous finite-thickness hollow garment shell joins the lower torso to an integral shoulder yoke, with a true top neck opening, two bounded full side arm openings and an open lower waist. This is a single genus-three material shell, not separate armour plates and connecting strips. Sixteen complete closed curved packet exteriors in two rows on the front and back follow the shell contour and have embedded finite root regions; their seam-coloured top faces are actual facets, not texture. No inner weights, removable inserts, open pockets, buckles or fastening mechanism are claimed. Four constant opaque PBR roles, metre-style native Z up and full annular lower-hem ground datum. All numerical surface domains, aperture topology and pouch geometry are new; no camera-harness fragments, old cuirass plate grids, support arm or fasteners are imported, removed or recoloured. One original model zero scenes, all repeated packet exteriors belong to the one complete vest. No person, mannequin, body fill or external stand. Static illustrative appearance only: no real weight, wearable fit, fastening, fabric behaviour, exercise instructions, training effect, ergonomics, movement, load, impact protection, manufacturing or safety capability. No text, logos, textures, rigging, animation or interaction.'
import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='fitness-fixed-continuous-open-shell-and-sixteen-packet-weighted-vest-01'
TITLE='Continuous Open Shell And Sixteen Packet Weighted Vest'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeGarmentShell_DeepSlate',(.075,.13,.15,1),.91),('WholePacketExteriors_MutedBlue',(.16,.25,.29,1),.88),('WholeBoundEdgesAndPacketSeams_LightSlate',(.30,.36,.35,1),.88),('WholeGarmentInner_DarkSlate',(.04,.065,.075,1),.94)]
G={}
def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
VEST_ROWS=[(0,.21,.115),(.04,.21,.115),(.13,.21,.115),(.17,.21,.115),(.235,.21,.115),(.30,.215,.118),(.37,.205,.115),(.395,.18,.095),(.445,.085,.075)]
def shell_radius(z):
 for j in range(len(VEST_ROWS)-1):
  a,b=VEST_ROWS[j:j+2]
  if a[0]<=z<=b[0]:
   t=(z-a[0])/(b[0]-a[0]);return tuple(a[k]*(1-t)+b[k]*t for k in[1,2])
 raise AssertionError('Outside whole vest')
def continuous_vest():
 n=96;vs=[];fs=[];ms=[];ix={};edges={}
 def vert(j,i,side):
  i%=n;key=(j,i,side)
  if key not in ix:
   z,rx,ry=VEST_ROWS[j];a=math.tau*i/n;ix[key]=len(vs);vs.append(((rx-.008*side)*math.cos(a),(ry-.008*side)*math.sin(a),z))
  return ix[key]
 for j in range(len(VEST_ROWS)-1):
  z=(VEST_ROWS[j][0]+VEST_ROWS[j+1][0])/2
  for i in range(n):
   a=math.tau*(i+.5)/n
   if .17<z<.395 and abs(math.cos(a))>math.cos(math.pi/6):continue
   q=[(j,i),(j,(i+1)%n),(j+1,(i+1)%n),(j+1,i)]
   fs +=[tuple(vert(*p,0)for p in q),tuple(vert(*p,1)for p in reversed(q))];ms +=[0,3]
   for a,b in zip(q,q[1:]+q[:1]):
    if (b,a)in edges:del edges[(b,a)]
    else:edges[(a,b)]=1
 for a,b in edges:fs.append((vert(*b,0),vert(*a,0),vert(*a,1),vert(*b,1)));ms.append(2)
 record('WholeContinuousNeckArmholeAndWaistShell',vs,fs,ms)
def pouch(name,a0,z0):
 # Entire closed radial packet exterior follows the parent shell; its inner
 # attachment face sits inside the whole shell thickness, not through the cavity.
 n=6;vs=[];fs=[];mats=[];rows=[(z0,.80),(z0+.009,1),(z0+.085,1),(z0+.094,.85)];half=.105
 for radial in[-.003,.030]:
  for z,fac in rows:
   rx,ry=shell_radius(z)
   for j in range(n+1):
    a=a0+half*fac*(2*j/n-1);vs.append(((rx+radial)*math.cos(a),(ry+radial)*math.sin(a),z))
 row=n+1;layer=row*len(rows)
 for k in range(len(rows)-1):
  for j in range(n):
   a=k*row+j;b=a+1;c=a+row+1;d=a+row;fs +=[(a,d,c,b),(layer+a,layer+b,layer+c,layer+d)];mats +=[1,1]
 outline=list(range(row))+[k*row+n for k in range(1,len(rows))]+list(range(layer-2,layer-row-1,-1))+[k*row for k in range(len(rows)-2,0,-1)]
 for a,b in zip(outline,outline[1:]+outline[:1]):fs.append((a,b,layer+b,layer+a));mats.append(2 if a//row==len(rows)-1 and b//row==len(rows)-1 else 1)
 record(name,vs,fs,mats)
def make_geometry():
 G.clear();continuous_vest()
 for side,center in [('Front',-math.pi/2),('Back',math.pi/2)]:
  for col,k in enumerate([-6,-2,2,6]):
   for row,z in enumerate([.030,.145]):pouch('Whole%sPacket_%d_%d'%(side,col,row),center+k*math.tau/96,z)
 global SHIFT
 SHIFT=(0,0,0)
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
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==proof['mesh_count']
 triangle_count=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons);assert triangle_count==proof['triangles']
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 lo=[min(v[k]for v in points)for k in range(3)];hi=[max(v[k]for v in points)for k in range(3)]
 assert abs(lo[2])<=TOL
 assert len({m for o in parts for m in o.data.materials})==len(PALETTE)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'),compress=False)
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
 for layer in scene.view_layers:layer.cycles.use_denoising=False
 scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
 scene.render.resolution_x=scene.render.resolution_y=640;scene.render.resolution_percentage=100
 scene.world=scene.world or bpy.data.worlds.new('Neutral instrument preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.22))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,22),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(4,-7,3.8) if '--tier-single-view' in sys.argv and sys.argv[sys.argv.index('--tier-single-view')+1]=='qa-front' else (-4,7,4.1));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 def config():return dict(engine=scene.render.engine,samples=scene.cycles.samples,adaptive=scene.cycles.use_adaptive_sampling,cycles_denoise=scene.cycles.use_denoising,view_layer_denoise=[x.cycles.use_denoising for x in scene.view_layers],compositor_nodes=scene.use_nodes,compositing=scene.render.use_compositing,threads_mode=scene.render.threads_mode,threads=scene.render.threads)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'asset':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':len(parts),'mesh_objects':len(parts),'triangles':triangle_count,'materials':len(PALETTE),'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
 qa['native_saved_render_config']=config();qa['render_configs']={}
 if '--geometry-only' not in sys.argv:
  view=sys.argv[sys.argv.index('--tier-single-view')+1]if '--tier-single-view'in sys.argv else 'thumbnail';assert view in ['qa-front','thumbnail']
  scene.cycles.samples=16 if view=='qa-front' else 128;qa['render_configs'][view]=config();scene.render.filepath=str(OUT/(view+'.png'));start=time.monotonic();bpy.ops.render.render(write_still=True);qa['render']={'view':view,'samples':scene.cycles.samples,'seconds':time.monotonic()-start,'original_pixels_reviewed':False}
 (OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if p.exists():files[role]={'path':f'assets/sports/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'sports','style':'source-preserved-low-poly','title':TITLE,'description':'One independently authored complete empty weighted-training-vest-inspired static exterior. One continuous finite-thickness hollow garment shell joins the lower torso to an integral shoulder yoke, with a true top neck opening, two bounded full side arm openings and an open lower waist. This is a single genus-three material shell, not separate armour plates and connecting strips. Sixteen complete closed curved packet exteriors in two rows on the front and back follow the shell contour and have embedded finite root regions; their seam-coloured top faces are actual facets, not texture. No inner weights, removable inserts, open pockets, buckles or fastening mechanism are claimed. Four constant opaque PBR roles, metre-style native Z up and full annular lower-hem ground datum. All numerical surface domains, aperture topology and pouch geometry are new; no camera-harness fragments, old cuirass plate grids, support arm or fasteners are imported, removed or recoloured. One original model zero scenes, all repeated packet exteriors belong to the one complete vest. No person, mannequin, body fill or external stand. Static illustrative appearance only: no real weight, wearable fit, fastening, fabric behaviour, exercise instructions, training effect, ergonomics, movement, load, impact protection, manufacturing or safety capability. No text, logos, textures, rigging, animation or interaction.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
