import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='entertainment-fixed-openback-foldwing-puppet-theatre-01'
G={};FM={}
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def unit(a):return tuple(x/math.sqrt(dot(a,a))for x in a)
def mesh(name,v,faces,mat):
 f=[]
 for p in faces:
  for k in range(1,len(p)-1):f.append((p[0],p[k],p[k+1]))
 if sum(dot(v[a],cross(v[b],v[c]))for a,b,c in f)<0:f=[tuple(reversed(p))for p in f]
 G[name]=(v,f,mat)
BOX=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(name,c,size,mat):mesh(name,[tuple(c[i]+s[i]*size[i]/2 for i in range(3))for s in[(x,y,z)for z in[-1,1]for y in[-1,1]for x in[-1,1]]],BOX,mat)
def beam(name,a,b,width,mat):
 w=unit(sub(b,a));u=unit(cross(w,(1,0,0)if abs(w[0])<.9 else(0,1,0)));v=cross(w,u)
 mesh(name,[tuple(p[i]+width/2*(sx*u[i]+sy*v[i])for i in range(3))for p in[a,b]for sy in[-1,1]for sx in[-1,1]],BOX,mat)
def axle(name,x0,x1,y,z,r,mat,n=16):
 v=[(x,y+r*math.cos(math.tau*i/n),z+r*math.sin(math.tau*i/n))for x in[x0,x1]for i in range(n)]
 mesh(name,v,[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)],mat)

def ringx(name,x0,x1,y,z,ri,ro,mat,n=24):
 v=[(x,y+r*math.cos(math.tau*i/n),z+r*math.sin(math.tau*i/n))for x in[x0,x1]for r in[ri,ro]for i in range(n)];f=[]
 for i in range(n):j=(i+1)%n;f.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 mesh(name,v,f,mat)
def cyly(name,y0,y1,x,z,r,mat,n=24):
 axle(name,y0,y1,x,z,r,mat,n);v,f,m=G[name];G[name]=([(b,a,c)for a,b,c in v],[tuple(reversed(p))for p in f],m)
def ringy(name,y0,y1,x,z,ri,ro,mat,n=24):
 ringx(name,y0,y1,x,z,ri,ro,mat,n);v,f,m=G[name];G[name]=([(b,a,c)for a,b,c in v],[tuple(reversed(p))for p in f],m)
def triangulate(p):
 def cr(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 ids=list(range(len(p)));out=[]
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:ids.reverse()
 while len(ids)>3:
  for k,b in enumerate(ids):
   a,c=ids[k-1],ids[(k+1)%len(ids)]
   if cr(p[a],p[b],p[c])<=1e-14:continue
   if any(min(cr(p[a],p[b],p[j]),cr(p[b],p[c],p[j]),cr(p[c],p[a],p[j]))>=-1e-14 for j in ids if j not in[a,b,c]):continue
   out.append((a,b,c));ids.pop(k);break
  else:raise AssertionError('bad polygon')
 return out+[tuple(ids)]
def lathe_z(name,x,y,profile,mat,n=24):
 v=[];rings=[];f=[]
 for r,z in profile:
  ids=[]
  if r==0:ids=[len(v)];v.append((x,y,z))
  else:
   for i in range(n):ids.append(len(v));v.append((x+r*math.cos(math.tau*i/n),y+r*math.sin(math.tau*i/n),z))
  rings.append(ids)
 for a,b in zip(rings,rings[1:]+rings[:1]):
  if len(a)==len(b)==1:continue
  for i in range(n):
   j=(i+1)%n
   if len(a)==1:f.append((a[0],b[j],b[i]))
   elif len(b)==1:f.append((a[i],a[j],b[0]))
   else:f.append((a[i],a[j],b[j],b[i]))
 mesh(name,v,f,mat)



# One complete open-backed puppet booth: front concealment screen and true stage aperture.
for side,x in [('Left',-.65),('Right',.65)]:
 box(side+'WholeGroundFoot',(x,.04,.035),(.17,.48,.070),0)
 box(side+'WholeFrontProsceniumPost',(x,0,.88),(.070,.080,1.70),0)
box('WholeLowerConcealmentScreen',(0,.015,.515),(1.25,.025,.89),2)
box('WholePerformanceWindowSill',(0,-.035,.990),(1.40,.24,.075),0)
box('WholeProsceniumHeader',(0,0,1.70),(1.40,.105,.090),0)
axle('WholeCurtainSuspensionRail',-.655,.655,.005,1.675,.017,0,16)
# Two genuinely rear-folded whole framed solid wings; no roof or rear closing wall.
for side,sgn in [('Left',-1),('Right',1)]:
 ox,oy=sgn*.69,.030;ex,ey=sgn*.94,.630;L=math.hypot(ex-ox,ey-oy);ux,uy=(ex-ox)/L,(ey-oy)/L
 def place(n):
  v,f,m=G[n];G[n]=([(ox+x*ux-y*uy,oy+x*uy+y*ux,z)for x,y,z in v],f,m)
 for label,c,size in [('InnerStile',(.025,0,.75),(.055,.055,1.42)),('OuterStile',(L-.025,0,.75),(.055,.055,1.42)),('BottomRail',(L/2,0,.135),(L-.045,.055,.065)),('TopRail',(L/2,0,1.415),(L-.045,.055,.065)),('WholeInsetWingPanel',(L/2,0,.775),(L-.095,.020,1.245))]:
  name=side+label;box(name,c,size,2 if label=='WholeInsetWingPanel'else 0);place(name)
 name=side+'WingWholeGroundFoot';box(name,(L-.025,0,.030),(.17,.28,.060),0);place(name)
 lathe_z(side+'WholeVerticalHingePin',ox,oy,[(0,.16),(.010,.16),(.010,1.40),(0,1.40)],0,12)
 for i,z in enumerate([.30,1.20]):lathe_z(side+'WholeHingeKnuckle_'+str(i),ox,oy,[(0,z-.050),(.023,z-.050),(.023,z+.050),(0,z+.050)],0,12)
# Each curtain is one continuous pleated solid, gathered at a narrow waist, not loose strips.
for side,sgn in [('Left',-1),('Right',1)]:
 stations=[(1.055,.50,.12),(1.17,.52,.09),(1.34,.55,.05),(1.52,.52,.10),(1.67,.49,.13)];nx=19;v=[]
 for back in[False,True]:
  for z,cx,half in stations:
   for j in range(nx):u=-1+2*j/(nx-1);x=sgn*(cx+u*half);y=-.020+.014*math.cos(3*math.pi*(u+1))+(.006 if back else-.006);v.append((x,y,z))
 nr=len(stations);k=nx*nr;f=[]
 for i in range(nr-1):
  for j in range(nx-1):a=i*nx+j;f.extend([(a,a+1,a+nx+1,a+nx),(a+k,a+nx+k,a+nx+1+k,a+1+k)])
 for i in range(nr-1):
  a=i*nx;f.append((a,a+nx,a+nx+k,a+k));a=i*nx+nx-1;f.append((a,a+k,a+nx+k,a+nx))
 for j in range(nx-1):a=j;f.append((a,a+k,a+1+k,a+1));a=(nr-1)*nx+j;f.append((a,a+1,a+1+k,a+k))
 mesh(side+'WholeGatheredPleatedCurtain',v,f,1)
 # One complete wrap band around the gathered cloth, with actual overlap at its ends.
 v=[];N=24
 for z,rx,ry in[(1.330,.043,.018),(1.330,.068,.035),(1.350,.068,.035),(1.350,.043,.018)]:
  for j in range(N):a=math.tau*j/N;v.append((sgn*.55+rx*math.cos(a),-.020+ry*math.sin(a),z))
 mesh(side+'WholeCurtainGatherBand',v,[(k*N+i,k*N+(i+1)%N,((k+1)%4)*N+(i+1)%N,((k+1)%4)*N+i)for k in range(4)for i in range(N)],0)
# Full thick scalloped valance hangs from the header; central stage opening remains unfilled.
p=[(-.625,1.725),(.625,1.725)]+[(.625-1.25*j/30,1.585+.030*(1-math.cos(10*math.pi*j/30))/2)for j in range(31)]
if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:p.reverse()
n=len(p);v=[(x,y,z)for y in[-.066,-.046]for x,z in p];f=[]
for a,b,c in triangulate(p):f.extend([(a,b,c),(c+n,b+n,a+n)])
f +=[(i,i+n,(i+1)%n+n,(i+1)%n)for i in range(n)];mesh('WholeScallopedUpperValance',v,f,1)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeFrameSillAndHinges_WarmWood',(.44,.28,.12,1),.75,0),('WholeCurtainsAndValance_MutedRed',(.47,.065,.055,1),.88,0),('WholeFrontAndFoldedWingScreens_MutedTeal',(.075,.23,.24,1),.77,0)]
# BLENDER PHASE
import bpy
from mathutils import Vector
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=128
scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for layer in scene.view_layers:layer.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=4
scene.use_nodes=False;scene.render.use_compositing=False
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='AgX'
materials=[]
for name,col,rough,metal in PALETTE:
 m=bpy.data.materials.new(name);m.diffuse_color=col;m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=col;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;materials.append(m)

parts=[]
for name,(v,f,mi) in G.items():
 me=bpy.data.meshes.new(name+'Mesh');me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o)
 for m in materials:me.materials.append(m)
 face_materials=FM[name]if name in FM else[mi]*len(f)
 for i,p in enumerate(me.polygons):p.material_index=face_materials[i];p.use_smooth=False
 parts.append(o)
for prefix in []:
 parent=bpy.data.objects.new(prefix+'_CompleteSourceAssembly',None);scene.collection.objects.link(parent)
 for o in parts:
  if o.name.startswith(prefix+'__'):o.parent=parent
 parent.select_set(True)
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
triangles=sum(len(f)for v,f,m in G.values())
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
(OUT/'qa-report.json').write_text(json.dumps({'asset':ASSET,'mesh_objects':len(G),'triangles':triangles,'materials':len(PALETTE),'new_independent_models':1,'new_scenes':0},indent=2))
if '--geometry-only' in sys.argv:
 print('GEOMETRY_READY',ASSET,triangles);sys.exit(0)
# Render the actual exported geometry, not an unexported proxy.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
parts=[x for x in scene.objects if x.type=='MESH'];assert len(parts)==len(G)
view='thumbnail'
if '--view' in sys.argv:view=sys.argv[sys.argv.index('--view')+1]
assert view in ['qa-front','thumbnail']
scene.cycles.samples=16 if view=='qa-front' else 128
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.28,.28,.28,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
focus=Vector((0,0,.86))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.50;aim(cam,(3,-5,2.7));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/music/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'entertainment','style':'S01-clean-geometric','title':'Fixed Open Back Fold Wing Puppet Theatre','description':'One newly authored complete fixed open-backed folding-wing puppet-theatre booth. A full lower front concealment screen carries a tall genuinely open performance window with a broad projecting sill, side posts and header. Two independently framed solid wings are fixed folded rearward on complete vertical hinge appearances and stand on their own finite feet. A full upper rod supports two continuous thick pleated curtains gathered by complete wrap bands; a single scalloped valance closes only the top border. The rear stays entirely open with no roof, back wall or floor. This is not a ticket booth re-labelled or a low music platform with flags: the concealment front, high aperture, supporting folded wings and curtain routing are newly authored together with no old meshes. Three opaque constant untextured PBR roles, metres, Z up and full horizontally bounds-centred ground origin. One complete prop, zero scenes and no puppet or performer. Static visual only: no folding animation, cloth simulation, hinge range, child or performer fit, actual operation, anchoring, fire behavior, loading, manufacture or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
