'One independently authored complete static clothed merfolk fantasy character. A continuous fully covered tunic waist, upright chest, neck and human-like head rises directly from a newly drawn single broad fish lower body. The whole lower body curves down and sideways into a tapered raised tailstock and a thick complete bifurcated fan fin, with a finite low tail-underside resting patch. Two complete long-sleeved bent arms and blunt hands frame the waist; integral dark hair regions, small embedded eyes, ears and a blunt nose define a simple adult-like stylized face. All body sections, curve paths, fin outline and limb placements are new numeric geometry, not a catalog fish with a human head, the existing centaur upper body pasted onto a fish, or a horse with its legs removed. No old mesh or character coordinates are imported. Four opaque untextured PBR materials, one character model zero scenes, metres Z up and full horizontal bounds-centred ground origin. Entire torso and arms clothed; no weapon, equipment, extra costume asset or realistic anatomy claim. Static fictional art only, no biology, swimming, balance, skin deformation, articulation, rig, animation, interaction, collision or safety validation.'
import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='fantasy-static-clothed-upright-torso-and-curled-fan-tail-merfolk-01'
TITLE='Static Clothed Upright Torso And Curled Fan Tail Merfolk'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('MutedSeaGreenTail',(.09,.32,.29,1),.76),('WarmTanFaceAndHands',(.60,.38,.25,1),.81),('OpaqueLongSleevedBlueTunic',(.065,.15,.26,1),.83),('DarkBrownHairAndEyes',(.045,.027,.020,1),.80)]
G={}
def record(name,v,fs,m):
 ts=[];mats=[]
 for i,f in enumerate(fs):
  for k in range(1,len(f)-1):ts.append((f[0],f[k],f[k+1]));mats.append(m[i] if isinstance(m,list)else m)
 vol=sum(sum(v[a][i]*([v[b][1]*v[c][2]-v[b][2]*v[c][1],v[b][2]*v[c][0]-v[b][0]*v[c][2],v[b][0]*v[c][1]-v[b][1]*v[c][0]][i])for i in range(3))for a,b,c in ts)/6
 if vol<0:ts=[(a,c,b)for a,b,c in ts]
 assert abs(vol)>1e-12;G[name]=(v,ts,mats)
def rect(x,y0,y1,r):return[(-x+r,y0),(x-r,y0),(x,y0+r),(x,y1-r),(x-r,y1),(-x+r,y1),(-x,y1-r),(-x,y0+r)]
def prism(name,p,z0,z1,m,transform=None):
 v=[(x,y,z)for z in[z0,z1]for x,y in p];n=len(p);f=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)]
 if transform:v=[transform(q)for q in v]
 record(name,v,f,m)
def box(name,lo,hi,m,transform=None):prism(name,[(lo[0],lo[1]),(hi[0],lo[1]),(hi[0],hi[1]),(lo[0],hi[1])],lo[2],hi[2],m,transform)
def union_boxes(name,boxes,m):
 xs=sorted(set(p[0]for b in boxes for p in b));ys=sorted(set(p[1]for b in boxes for p in b));zs=sorted(set(p[2]for b in boxes for p in b));faces={}
 for i in range(len(xs)-1):
  for j in range(len(ys)-1):
   for k in range(len(zs)-1):
    c=((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)
    if not any(all(lo[t]<c[t]<hi[t]for t in range(3))for lo,hi in boxes):continue
    v=[(x,y,z)for z in[zs[k],zs[k+1]]for y in[ys[j],ys[j+1]]for x in[xs[i],xs[i+1]]]
    for f in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:
     q=tuple(v[t]for t in f);key=tuple(sorted(q))
     if key in faces:del faces[key]
     else:faces[key]=q
 verts=[];ix={};fs=[]
 for q in faces.values():
  f=[]
  for p in q:
   if p not in ix:ix[p]=len(verts);verts.append(p)
   f.append(ix[p])
  fs.append(f)
 record(name,verts,fs,m)
def cyl(name,center,r,length,axis,m,n=12):
 axes=[i for i in range(3)if i!=axis];v=[]
 for end in[-.5,.5]:
  for i in range(n):
   p=list(center);p[axis]+=end*length;p[axes[0]]+=r*math.cos(i*math.tau/n);p[axes[1]]+=r*math.sin(i*math.tau/n);v.append(tuple(p))
 record(name,v,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],m)
def sweep(name,path,r,m,n=12):
 # Constant out-of-plane axis prevents local frame flips along this planar neck.
 v=[]
 for j,p in enumerate(path):
  a=path[max(0,j-1)];b=path[min(len(path)-1,j+1)];dy=b[1]-a[1];dz=b[2]-a[2];q=math.hypot(dy,dz);u=(0,dz/q,-dy/q)
  for i in range(n):
   t=math.tau*i/n;v.append((p[0]+r*math.cos(t),p[1]+u[1]*r*math.sin(t),p[2]+u[2]*r*math.sin(t)))
 fs=[tuple(reversed(range(n))),tuple((len(path)-1)*n+i for i in range(n))]
 fs +=[(k*n+i,k*n+(i+1)%n,(k+1)*n+(i+1)%n,(k+1)*n+i)for k in range(len(path)-1)for i in range(n)]
 record(name,v,fs,m)
def ring(name,x0,x1,y,th,z0,z1,m,tr=None):
 outer=[(x0,-y),(x1,-y),(x1,y),(x0,y)];inner=[(x0+th,-y+th),(x1-th,-y+th),(x1-th,y-th),(x0+th,y-th)]
 v=[(x,y,z)for z,p in[(z0,outer),(z0,inner),(z1,outer),(z1,inner)]for x,y in p];fs=[]
 for i in range(4):
  j=(i+1)%4;fs +=[(i,j,4+j,4+i),(8+i,12+i,12+j,8+j),(i,8+i,8+j,j),(4+i,4+j,12+j,12+i)]
 if tr:v=[tr(p)for p in v]
 record(name,v,fs,m)
def rod(name,a,b,r,m,n=8):
 d=[b[i]-a[i]for i in range(3)];le=math.sqrt(sum(t*t for t in d));w=[t/le for t in d];seed=[0,0,1]if abs(w[2])<.9 else[0,1,0]
 u=[w[1]*seed[2]-w[2]*seed[1],w[2]*seed[0]-w[0]*seed[2],w[0]*seed[1]-w[1]*seed[0]];le=math.sqrt(sum(t*t for t in u));u=[t/le for t in u];v=[w[1]*u[2]-w[2]*u[1],w[2]*u[0]-w[0]*u[2],w[0]*u[1]-w[1]*u[0]]
 vs=[tuple(p[k]+r*(u[k]*math.cos(math.tau*i/n)+v[k]*math.sin(math.tau*i/n))for k in range(3))for p in[a,b]for i in range(n)]
 record(name,vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],m)
def earclip(poly):
 ids=list(range(len(poly)));out=[]
 def cross2(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 while len(ids)>3:
  done=False
  for k,i in enumerate(ids):
   a,b,c=ids[k-1],i,ids[(k+1)%len(ids)]
   if cross2(poly[a],poly[b],poly[c])<=1e-13:continue
   if any(j not in [a,b,c] and min(cross2(poly[a],poly[b],poly[j]),cross2(poly[b],poly[c],poly[j]),cross2(poly[c],poly[a],poly[j]))>=-1e-13 for j in ids):continue
   out.append((a,b,c));ids.pop(k);done=True;break
  assert done,'Cannot triangulate complete outer shell'
 out.append(tuple(ids));return out
def annular_x(name,x,z,ri,ro,th,m,n=32):
 vs=[(xx,r*math.cos(i*math.tau/n),z+r*math.sin(i*math.tau/n))for xx,r in[(x-th/2,ri),(x-th/2,ro),(x+th/2,ro),(x+th/2,ri)]for i in range(n)]
 fs=[(j*n+i,j*n+(i+1)%n,((j+1)%4)*n+(i+1)%n,((j+1)%4)*n+i)for j in range(4)for i in range(n)];record(name,vs,fs,m)
def axial_profile(name,profile,center,axis,m,n=32):
 axes=[i for i in range(3)if i!=axis];vs=[];rings=[]
 for r,z in profile:
  row=[]
  for j in range(1 if r==0 else n):
   p=list(center);p[axis]+=z;p[axes[0]]+=r*math.cos(j*math.tau/n);p[axes[1]]+=r*math.sin(j*math.tau/n);row.append(len(vs));vs.append(tuple(p))
  rings.append(row)
 fs=[]
 for k,row in enumerate(rings):
  nex=rings[(k+1)%len(rings)]
  if len(row)==len(nex)==1:continue
  for j in range(n):
   jj=(j+1)%n
   if len(row)==1:fs.append((row[0],nex[j],nex[jj]))
   elif len(nex)==1:fs.append((row[j],nex[0],row[jj]))
   else:fs.append((row[j],nex[j],nex[jj],row[jj]))
 record(name,vs,fs,m)
def zbody(name,rows,mat,n=16,band=None):
 v=[(x+rx*math.cos(math.tau*j/n),y+ry*math.sin(math.tau*j/n),z)for x,y,z,rx,ry in rows for j in range(n)];f=[];mi=[]
 for k in range(len(rows)-1):
  for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));mi.append(band(k,j)if band else mat)
 for k in [0,len(rows)-1]:f.append(tuple(k*n+j for j in (reversed(range(n))if k==0 else range(n))));mi.append(mat if not band else band(k,0))
 record(name,v,f,mi)
def tailbody():
 rows=[((0,0,.60),.23,.21),((0,0,.40),.225,.20),((.12,0,.18),.19,.15),((.30,0,.18),.18,.18/math.cos(math.pi/16)),((.48,0,.18),.15,.18/math.cos(math.pi/16)),((.65,0,.18),.105,.11),((.82,0,.32),.070,.075),((.90,0,.47),.038,.042)]
 v=[];n=16
 for k,(p,ry,rr)in enumerate(rows):
  a=rows[max(0,k-1)][0];b=rows[min(len(rows)-1,k+1)][0];dx,dz=b[0]-a[0],b[2]-a[2];ll=math.hypot(dx,dz);w=(-dz/ll,0,dx/ll)
  for j in range(n):
   t=math.pi/16+math.tau*j/n;v.append((p[0]+w[0]*rr*math.sin(t),p[1]+ry*math.cos(t),p[2]+w[2]*rr*math.sin(t)))
 f=[tuple(reversed(range(n))),tuple((len(rows)-1)*n+j for j in range(n))]+[(k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j)for k in range(len(rows)-1)for j in range(n)]
 record('WholeContinuousCurledFishLowerBody',v,f,0)
def rounded(name,c,r,mat,n=12,k=6):
 rows=[(c[0],c[1],c[2]+r[2]*math.cos(math.pi*t/k),r[0]*math.sin(math.pi*t/k),r[1]*math.sin(math.pi*t/k))for t in range(1,k)]
 # Full small finite pole caps rather than zero-radius degenerate rows.
 zbody(name,list(reversed(rows)),mat,n)
def fanfin():
 p=[(.86,.44),(.99,.46),(1.18,.29),(1.28,.33),(1.22,.49),(1.12,.56),(1.24,.69),(1.24,.80),(1.10,.78),(.95,.62),(.86,.52)]
 if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(p,p[1:]+p[:1]))<0:p.reverse()
 n=len(p);v=[(x,y,z)for y in[-.038,.038]for x,z in p];f=[]
 for a,b,c in earclip(p):f.extend([(a,b,c),(c+n,b+n,a+n)])
 f +=[(i,i+n,(i+1)%n+n,(i+1)%n)for i in range(n)]
 record('WholeThickForkedTailFan',v,f,0)
def make_geometry():
 G.clear();tailbody();fanfin()
 rows=[(0,0,.52,.18,.14),(0,-.015,.72,.17,.13),(0,-.015,.92,.22,.14),(0,-.02,1.08,.245,.14),(0,-.02,1.16,.10,.085),(0,-.02,1.24,.085,.08),(0,-.035,1.29,.125,.115),(0,-.03,1.41,.145,.135),(0,-.01,1.53,.125,.12),(0,0,1.60,.055,.06)]
 def mat(k,j):return 2 if k<4 else 3 if k>=8 or(k>=6 and j<8)else 1
 zbody('WholeClothedTorsoNeckAndHead',rows,2,16,mat)
 for i,sg in enumerate([-1,1]):
  sweep('WholeLongSleevedBentArm%d'%i,[(sg*.21,-.02,1.07),(sg*.33,-.03,.88),(sg*.28,-.22,.73)],.069,2,12)
  rounded('WholeBluntHand%d'%i,(sg*.275,-.245,.68),(.052,.062,.083),1)
  rounded('WholeDarkEye%d'%i,(sg*.060,-.149,1.429),(.015,.017,.016),3)
  rounded('WholeEar%d'%i,(sg*.137,-.015,1.408),(.035,.027,.055),1)
 # A compact wedge nose, deeply rooted behind the true face surface.
 p=[(-.154,1.42),(-.205,1.375),(-.143,1.35)];n=len(p);v=[(x,y,z)for x in[-.022,.022]for y,z in p];f=[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)];record('WholeBluntNose',v,f,1)
 pts=[p for v,f,m in G.values()for p in v];lo=[min(p[k]for p in pts)for k in range(3)];hi=[max(p[k]for p in pts)for k in range(3)]
 global SHIFT
 SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2])
 for name,(v,f,m)in list(G.items()):G[name]=([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)
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
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==12
 triangle_count=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons);assert triangle_count==proof['triangles']
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 lo=[min(v[k]for v in points)for k in range(3)];hi=[max(v[k]for v in points)for k in range(3)]
 assert abs(lo[2])<=TOL
 assert len({m for o in parts for m in o.data.materials})==4
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
 for layer in scene.view_layers:layer.cycles.use_denoising=False
 scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
 scene.render.resolution_x=scene.render.resolution_y=640;scene.render.resolution_percentage=100
 scene.world=scene.world or bpy.data.worlds.new('Neutral instrument preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.78))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,22),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(3,-8,3.6));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'),compress=False)
 def config():return dict(engine=scene.render.engine,samples=scene.cycles.samples,adaptive=scene.cycles.use_adaptive_sampling,cycles_denoise=scene.cycles.use_denoising,view_layer_denoise=[x.cycles.use_denoising for x in scene.view_layers],compositor_nodes=scene.use_nodes,compositing=scene.render.use_compositing,threads_mode=scene.render.threads_mode,threads=scene.render.threads)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'asset':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':12,'mesh_objects':12,'triangles':triangle_count,'materials':4,'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
 qa['native_saved_render_config']=config();qa['render_configs']={}
 if '--geometry-only' not in sys.argv:
  view=sys.argv[sys.argv.index('--tier-single-view')+1]if '--tier-single-view'in sys.argv else 'thumbnail';assert view in ['qa-front','thumbnail']
  scene.cycles.samples=16 if view=='qa-front' else 128;qa['render_configs'][view]=config();scene.render.filepath=str(OUT/(view+'.png'));start=time.monotonic();bpy.ops.render.render(write_still=True);qa['render']={'view':view,'samples':scene.cycles.samples,'seconds':time.monotonic()-start,'original_pixels_reviewed':False}
 (OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if p.exists():files[role]={'path':f'assets/magic/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'magic','style':'source-preserved-low-poly','title':TITLE,'description':'One independently authored complete static clothed merfolk fantasy character. A continuous fully covered tunic waist, upright chest, neck and human-like head rises directly from a newly drawn single broad fish lower body. The whole lower body curves down and sideways into a tapered raised tailstock and a thick complete bifurcated fan fin, with a finite low tail-underside resting patch. Two complete long-sleeved bent arms and blunt hands frame the waist; integral dark hair regions, small embedded eyes, ears and a blunt nose define a simple adult-like stylized face. All body sections, curve paths, fin outline and limb placements are new numeric geometry, not a catalog fish with a human head, the existing centaur upper body pasted onto a fish, or a horse with its legs removed. No old mesh or character coordinates are imported. Four opaque untextured PBR materials, one character model zero scenes, metres Z up and full horizontal bounds-centred ground origin. Entire torso and arms clothed; no weapon, equipment, extra costume asset or realistic anatomy claim. Static fictional art only, no biology, swimming, balance, skin deformation, articulation, rig, animation, interaction, collision or safety validation.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
