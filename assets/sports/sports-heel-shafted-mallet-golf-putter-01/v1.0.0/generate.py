"""Original heel-shafted mallet golf putter visual prop, light SELF_REVIEW."""
import hashlib,json,math,struct
from pathlib import Path
ASSET='sports-heel-shafted-mallet-golf-putter-01'
TITLE='Heel-Shafted Mallet Golf Putter'
TOL=2e-7
DESCRIPTION='One original static golf-putter appearance: a broad bevelled flat-soled metal mallet head, a slim heel-offset leaning shaft and a thicker dark upper grip. Three closed connected component meshes and three opaque untextured PBR materials, one prop and zero scenes. The shaft lower flat cap is entirely seated on the head top; the grip lower cap covers the shaft top with a finite opposed seat. All numeric geometry is new, not a hockey toe blade, baseball bat or old handle transplant. Metres, Z up, horizontally bounds-centred ground origin. Static game-art display, not regulation golf dimensions, real playability, grip suitability, balance, material performance or safety certification. No ball, turf, golfer, text, logo, animation or physical operation.'
def geometry():
 def loft(rings):
  n=len(rings[0]);tris=[]
  for a,b in zip(rings,rings[1:]):
   for j in range(n):k=(j+1)%n;tris.extend([(a[j],a[k],b[k]),(a[j],b[k],b[j])])
  for ring,top in [(rings[0],False),(rings[-1],True)]:
   c=tuple(sum(v[k]for v in ring)/n for k in range(3))
   for j in range(n):k=(j+1)%n;tris.append((c,ring[j],ring[k])if top else(c,ring[k],ring[j]))
  return tris
 outline=[(-.074,-.025),(.074,-.025),(.08,-.019),(.08,.019),(.074,.025),(-.074,.025),(-.08,.019),(-.08,-.019)]
 head=loft([[(x*scale,y*scale,z)for x,y in outline]for z,scale in [(0,.94),(.005,1),(.03,1),(.035,.94)]])
 def centre(z):return -.052+.202*(z-.035)/1.005
 def ring(z,r):return[(centre(z)+r*math.cos(2*math.pi*j/12),r*math.sin(2*math.pi*j/12),z)for j in range(12)]
 shaft=loft([ring(.035,.0045),ring(.86,.0045)]);grip=loft([ring(.86,.008),ring(.87,.009),ring(1.03,.009),ring(1.04,.008)])
 meshes=[('MalletHead',head,0),('LeaningHeelShaft',shaft,1),('UpperGrip',grip,2)];points=[v for _,tris,_ in meshes for tri in tris for v in tri];shift=(min(v[0]for v in points)+max(v[0]for v in points))/2
 return[(name,[tuple((x-shift,y,z)for x,y,z in tri)for tri in tris],mat)for name,tris,mat in meshes]

def compose():
 meshes=geometry();blob=bytearray();palette=[('Putter_MetalHead',[.56,.6,.63,1],.28,.7),('Putter_SteelShaft',[.36,.40,.43,1],.22,.85),('Putter_DarkGrip',[.025,.055,.045,1],.8,0.)]
 d={'asset':{'version':'2.0','generator':'New numerical golf putter'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'name':'AssetRoot__'+ASSET,'children':[]}],'meshes':[],'materials':[{'name':n,'doubleSided':True,'pbrMetallicRoughness':{'baseColorFactor':c,'metallicFactor':m,'roughnessFactor':r}}for n,c,r,m in palette],'accessors':[],'bufferViews':[],'buffers':[]}
 def array(values,component,kind):
  flat=[x for v in values for x in v]if kind=='VEC3'else values;fmt='f'if component==5126 else'I';raw=struct.pack('<'+fmt*len(flat),*flat);offset=len(blob);blob.extend(raw);blob.extend(b'\0'*((-len(blob))%4));vi=len(d['bufferViews']);d['bufferViews'].append({'buffer':0,'byteOffset':offset,'byteLength':len(raw)});a={'bufferView':vi,'componentType':component,'count':len(values),'type':kind}
  if kind=='VEC3':a.update(min=[min(v[k]for v in values)for k in range(3)],max=[max(v[k]for v in values)for k in range(3)])
  ai=len(d['accessors']);d['accessors'].append(a);return ai
 for name,tris,material in meshes:
  pos=[];normal=[]
  for a,b,c in tris:
   u=[b[k]-a[k]for k in range(3)];v=[c[k]-a[k]for k in range(3)];n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];length=math.sqrt(sum(x*x for x in n));assert length>0;n=[x/length for x in n];pos.extend((x,z,-y)for x,y,z in(a,b,c));normal.extend([(n[0],n[2],-n[1])]*3)
  mi=len(d['meshes']);d['meshes'].append({'name':name,'primitives':[{'attributes':{'POSITION':array(pos,5126,'VEC3'),'NORMAL':array(normal,5126,'VEC3')},'indices':array(list(range(len(pos))),5125,'SCALAR'),'material':material,'mode':4}]});ni=len(d['nodes']);d['nodes'].append({'name':name,'mesh':mi});d['nodes'][0]['children'].append(ni)
 d['buffers']=[{'byteLength':len(blob)}];return d,bytes(blob),{'triangles':sum(len(t)for _,t,_ in meshes),'new_independent_model_count':1,'scene_count':0,'original_new_numeric_geometry':True,'static_visual_only':True}

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
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==3
 triangle_count=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons);assert triangle_count==proof['triangles']
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 lo=[min(v[k]for v in points)for k in range(3)];hi=[max(v[k]for v in points)for k in range(3)]
 assert abs(lo[2])<=TOL and abs(lo[0]+hi[0])<=TOL and abs(lo[1]+hi[1])<=TOL
 assert len({m for o in parts for m in o.data.materials})==3
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
 for layer in scene.view_layers:layer.cycles.use_denoising=False
 scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
 scene.render.resolution_x=scene.render.resolution_y=640;scene.render.resolution_percentage=100
 scene.world=scene.world or bpy.data.worlds.new('Neutral sports studio');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.5))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,14),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(3,-5,2.5));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'),compress=True)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':3,'triangles':triangle_count,'materials':3,'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_rotation_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
 if '--geometry-only' not in sys.argv:
  view=sys.argv[sys.argv.index('--tier-single-view')+1]if '--tier-single-view'in sys.argv else 'thumbnail';assert view in ['qa-front','thumbnail']
  scene.cycles.samples=16 if view=='qa-front' else 128;scene.render.filepath=str(OUT/(view+'.png'));start=time.monotonic();bpy.ops.render.render(write_still=True);qa['render']={'view':view,'samples':scene.cycles.samples,'seconds':time.monotonic()-start,'original_pixels_reviewed':False}
 (OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if p.exists():files[role]={'path':f'assets/sports/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'models','assetKind':'model','theme':'sports','style':'low-poly','title':TITLE,'description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('ASSET_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
