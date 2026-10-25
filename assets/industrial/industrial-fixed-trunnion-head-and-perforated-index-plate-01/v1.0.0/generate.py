'One newly authored complete fixed tilting dividing-head-style tabletop apparatus. A broad low plinth and two complete bored trunnion cheeks support a whole angled spindle housing on a transverse axis. The long housing, its true through spindle bore, a complete bevelled annular front chuck and three fixed stepped open jaws are all constructed for this apparatus. A separate circular side index plate has a central opening and twelve genuine through holes, an outward hub, a whole crank and a fixed small pin entering one hole. A separate fork-side locking handle and two trunnion caps complete the arrangement. This is one complete instrument, not the headstock extracted from the old bench lathe: no bed, ways, sliding saddle or tailstock is used, and the body is carried between two transverse bored cheeks above its own base. It is not the earlier open-slot Geneva wheel with driver peg and locking sector. All numeric geometry is newly written, no old component mesh imported; four opaque constant PBR appearances, metres Z up, one model zero scenes. The fixed illustrated tilt and sparse decorative hole circle do not define working indexing or angular calibration. No worm mechanism is represented or claimed. No rotation, accurate indexing, crank ratio, spindle function, jaw motion, clamping, travel, bearing fit, cutting, manufacturing dimensions, machine installation, load or safety capability. No workpiece, animation, rigging or interactive operation.'
import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='industrial-fixed-trunnion-head-and-perforated-index-plate-01'
TITLE='Fixed Trunnion Head And Perforated Index Plate'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('CastBaseAndForkDeepBlue',(.075,.19,.23,1),.68),('WholeHousingOchre',(.50,.29,.095,1),.62),('ChuckIndexAndPinsSteel',(.43,.49,.49,1),.46),('ControlsGraphite',(.05,.065,.075,1),.63)]
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





def closed_outline(name,p,z0,z1,m,tr=None):
 if sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1]for i in range(len(p)))<0:p=list(reversed(p))
 n=len(p);cap=earclip(p);v=[(x,y,z)for z in[z0,z1]for x,y in p]
 if tr:v=[tr(q)for q in v]
 record(name,v,[tuple(reversed(t))for t in cap]+[tuple(j+n for j in t)for t in cap]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],m)







ROOTS=[];AIR=[]
def tilt(q):
 x,y,z=q;a=math.radians(-22);return(x,y*math.cos(a)-(z-.35)*math.sin(a),.35+y*math.sin(a)+(z-.35)*math.cos(a))
def turn_component(name):
 v,f,m=G[name];G[name]=([tilt(q)for q in v],f,m)
def root(a,b,q,turned=False):ROOTS.append((a,b,tilt(q)if turned else q))
def holeplate():
 # A shared continuous annular plate, not disconnected washers around painted dots.
 vs=[];ix={};fs=[];walls={}
 def vertex(q):
  q=tuple(round(t,12)for t in q)
  if q not in ix:ix[q]=len(vs);vs.append(q)
  return ix[q]
 def face(q,wall=False):
  f=tuple(vertex(t)for t in q)
  if wall:
   key=tuple(sorted(f))
   if key in walls:del walls[key]
   else:walls[key]=f
  else:fs.append(f)
 for k in range(12):
  a=k*math.tau/12;lo=a-math.pi/12;hi=a+math.pi/12
  polar=lambda ang,r:(r*math.cos(ang),.35+r*math.sin(ang))
  edge=[polar(lo+(hi-lo)*i/3,.038)for i in range(4)]+[polar(hi,r)for r in [.075,.115,.158]]+[polar(hi-(hi-lo)*i/6,.158)for i in range(1,7)]+[polar(lo,r)for r in [.115,.075]]
  cy,cz=polar(a,.116);hole=[]
  for y,z in edge:
   t=math.atan2(z-cz,y-cy);hole.append((cy+.012*math.cos(t),cz+.012*math.sin(t)))
  def pt(q,x):return(x,q[0],q[1])
  for i in range(len(edge)):
   j=(i+1)%len(edge);b,c,h,kq=edge[i],edge[j],hole[i],hole[j]
   face([pt(b,.251),pt(c,.251),pt(kq,.251),pt(h,.251)])
   face([pt(h,.279),pt(kq,.279),pt(c,.279),pt(b,.279)])
   face([pt(b,.251),pt(b,.279),pt(c,.279),pt(c,.251)],True)
   face([pt(h,.251),pt(kq,.251),pt(kq,.279),pt(h,.279)])
 fs+=list(walls.values());record('WholePerforatedIndexPlate',vs,fs,2)
def make_geometry():
 G.clear();ROOTS.clear();AIR.clear()
 prism('WholeChamferedTableBase',rect(.30,-.30,.28,.035),0,.045,0)
 for side,x in [('Left',-.18),('Right',.18)]:
  name=side+'WholeBoredTrunnionCheek'
  # Full upper ring intersects a broad integral lower leg, fused as one profile extrusion.
  # Explicit annular head and whole rising foot are separate complete structural members.
  box(side+'WholeRisingForkFoot',(x-.037,-.080,.035),(x+.037,.080,.325),0)
  axial_profile(name,[(.033,x-.041),(.092,x-.041),(.092,x+.041),(.033,x+.041)],(0,0,.35),0,0,32)
  root(side+'WholeRisingForkFoot','WholeChamferedTableBase',(x,0,.04))
  root(side+'WholeRisingForkFoot',name,(x,.055,.30))
 cyl('WholeTransverseTrunnionShaft',(0,0,.35),.035,.51,0,2,24)
 for side,x in [('Left',-.18),('Right',.18)]:root('WholeTransverseTrunnionShaft',side+'WholeBoredTrunnionCheek',(x,.034,.35))
 axial_profile('WholeTiltedThroughSpindleHousing',[(.048,-.20),(.105,-.20),(.120,-.17),(.120,.15),(.100,.19),(.048,.19)],(0,0,.35),1,1,32);turn_component('WholeTiltedThroughSpindleHousing')
 root('WholeTiltedThroughSpindleHousing','WholeTransverseTrunnionShaft',(.09,0,.35))
 axial_profile('WholeOpenSpindleSleeve',[(.034,-.265),(.051,-.265),(.051,.215),(.034,.215)],(0,0,.35),1,2,28);turn_component('WholeOpenSpindleSleeve')
 root('WholeOpenSpindleSleeve','WholeTiltedThroughSpindleHousing',(.049,-.13,.35),True)
 axial_profile('WholeBevelledOpenChuck',[(.039,-.285),(.128,-.285),(.14,-.27),(.14,-.215),(.128,-.20),(.039,-.20)],(0,0,.35),1,2,36);turn_component('WholeBevelledOpenChuck')
 root('WholeBevelledOpenChuck','WholeOpenSpindleSleeve',(.045,-.25,.35),True)
 for i in range(3):
  a=math.pi/2+i*math.tau/3;name='WholeSteppedOpenJaw'+str(i)
  def tr(q):
   r,y,t=q;return tilt((r*math.cos(a)-t*math.sin(a),y,.35+r*math.sin(a)+t*math.cos(a)))
  # Concave stepped radial jaw is a single closed extrusion.
  poly=[(.043,-.322),(.085,-.322),(.085,-.303),(.124,-.303),(.124,-.263),(.043,-.263)]
  closed_outline(name,poly,-.016,.016,2,tr)
  root(name,'WholeBevelledOpenChuck',(.10*math.cos(a),-.275,.35+.10*math.sin(a)),True)
 cyl('LeftWholeTrunnionCap',(-.242,0,.35),.055,.030,0,3,24);root('LeftWholeTrunnionCap','WholeTransverseTrunnionShaft',(-.24,.02,.35))
 holeplate()
 cyl('WholeIndexCentralHub',(.265,0,.35),.040,.085,0,2,24)
 root('WholeIndexCentralHub','WholeTransverseTrunnionShaft',(.24,.02,.35))
 root('WholeIndexCentralHub','WholePerforatedIndexPlate',(.26,.039,.35))
 rod('WholeSideIndexCrank',(.317,0,.35),(.317,.116,.35),.015,3,10)
 root('WholeSideIndexCrank','WholeIndexCentralHub',(.305,.012,.35))
 cyl('WholeFixedHolePin',(.286,.116,.35),.008,.085,0,2,16)
 root('WholeFixedHolePin','WholeSideIndexCrank',(.317,.109,.35))
 cyl('WholeOutwardCrankGrip',(.355,.116,.35),.018,.075,0,3,20)
 root('WholeOutwardCrankGrip','WholeFixedHolePin',(.325,.116,.35))
 rod('WholeForkLockLever',(-.265,0,.35),(-.265,-.09,.24),.012,2,12)
 root('WholeForkLockLever','LeftWholeTrunnionCap',(-.255,-.006,.343))
 cyl('WholeLockLeverGrip',(-.265,-.09,.225),.020,.065,2,3,16)
 root('WholeLockLeverGrip','WholeForkLockLever',(-.265,-.087,.243))
 AIR.extend([tilt((0,-.31,.35)),tilt((0,.16,.35)),(0,-.20,.10),(.265,-.116,.35),(.265,0,.466)])
 pts=[p for v,f,m in G.values()for p in v];lo=[min(p[k]for p in pts)for k in range(3)];hi=[max(p[k]for p in pts)for k in range(3)]
 global SHIFT;SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2])
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
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==20
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
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.26))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,22),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(5,-7,4));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'),compress=False)
 def config():return dict(engine=scene.render.engine,samples=scene.cycles.samples,adaptive=scene.cycles.use_adaptive_sampling,cycles_denoise=scene.cycles.use_denoising,view_layer_denoise=[x.cycles.use_denoising for x in scene.view_layers],compositor_nodes=scene.use_nodes,compositing=scene.render.use_compositing,threads_mode=scene.render.threads_mode,threads=scene.render.threads)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'asset':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':20,'mesh_objects':20,'triangles':triangle_count,'materials':4,'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
 qa['native_saved_render_config']=config();qa['render_configs']={}
 if '--geometry-only' not in sys.argv:
  view=sys.argv[sys.argv.index('--tier-single-view')+1]if '--tier-single-view'in sys.argv else 'thumbnail';assert view in ['qa-front','thumbnail']
  scene.cycles.samples=16 if view=='qa-front' else 128;qa['render_configs'][view]=config();scene.render.filepath=str(OUT/(view+'.png'));start=time.monotonic();bpy.ops.render.render(write_still=True);qa['render']={'view':view,'samples':scene.cycles.samples,'seconds':time.monotonic()-start,'original_pixels_reviewed':False}
 (OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if p.exists():files[role]={'path':f'assets/industrial/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'industrial','style':'source-preserved-low-poly','title':TITLE,'description':__doc__,'bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
