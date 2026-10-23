import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='animal-static-long-foot-tail-resting-kangaroo-01'
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

def xy(cx,cy,z,rx,ry,n=12):return[(cx+rx*math.cos(math.pi/n+math.tau*i/n)/math.cos(math.pi/n),cy+ry*math.sin(math.pi/n+math.tau*i/n)/math.cos(math.pi/n),z)for i in range(n)]
def solid_loft(name,rings,mat,face_mat=None):
 n=len(rings[0]);v=[p for r in rings for p in r];f=[];fm=[]
 for k in range(len(rings)-1):
  for i in range(n):j=(i+1)%n;f.extend([(k*n+i,k*n+j,(k+1)*n+j),(k*n+i,(k+1)*n+j,(k+1)*n+i)]);fm.extend([face_mat(k,i)if face_mat else mat]*2)
 for k,r in [(0,rings[0]),(len(rings)-1,rings[-1])]:
  c=len(v);v.append(tuple(sum(p[j]for p in r)/n for j in range(3)))
  for i in range(n):j=(i+1)%n;f.append((c,k*n+j,k*n+i)if k==0 else(c,k*n+i,k*n+j));fm.append(mat)
 mesh(name,v,f,mat);FM[name]=fm

# New tall asymmetric-limb whole animal architecture: two long integral hind
# feet and a long flat-bottom rear tail contact ground; small forearms stay up.
def front_belly(k,i):return 1 if i in[7,8,9]else 0
solid_loft('WholeAscendingTorsoAndLongNeck',[xy(0,.06,.36,.15,.17),xy(0,.08,.55,.24,.23),xy(0,.03,.83,.235,.21),xy(0,-.065,1.05,.18,.17),xy(0,-.16,1.23,.135,.12),xy(0,-.25,1.43,.095,.09),xy(0,-.29,1.51,.085,.08)],0,front_belly)
def xz(x,y,lo,hi,w,n=12):
 c=math.cos(math.pi/n);return[(x+w*math.cos(math.pi/n+math.tau*i/n)/c,y,lo+(hi-lo)*(math.sin(math.pi/n+math.tau*i/n)+c)/(2*c))for i in range(n)]
solid_loft('WholeLongTaperedGroundRestingTail',[xz(0,.19,.49,.86,.14),xz(0,.37,.30,.57,.13),xz(.01,.60,.09,.31,.10),xz(.025,.85,0,.145,.065),xz(.05,1.10,0,.075,.036),xz(.065,1.30,0,.030,.012),xz(.068,1.34,0,.018,.006)],0)
for side,sx in [('Left',-1),('Right',1)]:
 # Full foot, ankle, slender lower segment, forward knee and huge upper thigh
 # are a single varying-section body per side, not a rabbit paw/haunch copy.
 solid_loft(side+'WholeLongFootHockAndStrongHindLeg',[xy(sx*.245,-.18,0,.095,.34),xy(sx*.245,-.18,.06,.095,.34),xy(sx*.245,.07,.135,.061,.10),xy(sx*.24,.12,.28,.055,.075),xy(sx*.235,.025,.42,.105,.14),xy(sx*.20,-.015,.60,.155,.19),xy(sx*.16,.06,.78,.145,.16)],0)
 solid_loft(side+'WholeRaisedShortForearm',[xy(sx*.16,-.16,1.19,.045,.05),xy(sx*.235,-.20,1.065,.038,.045),xy(sx*.21,-.29,.97,.033,.04),xy(sx*.16,-.39,.94,.040,.055)],0)
# Small elongated head above the long ascending neck, unlike the low seated
# rabbit head directly on shoulders or deer quadruped trunk.
solid_loft('WholeElongatedSmallHead',[xy(0,-.32,1.46,.065,.09),xy(0,-.39,1.54,.105,.145),xy(0,-.38,1.65,.105,.13),xy(0,-.33,1.71,.065,.075)],0)
solid_loft('WholeTaperedForwardMuzzle',[xz(0,-.65,1.525,1.60,.045),xz(0,-.59,1.515,1.62,.066),xz(0,-.49,1.51,1.645,.075)],0)
# Muzzle front end material is part of the same closed cap, not a floating nose.
n=12;fm=FM['WholeTaperedForwardMuzzle'];start=2*(3-1)*n
for i in range(start,start+n):fm[i]=2
for side,sx in [('Left',-1),('Right',1)]:
 solid_loft(side+'WholePointedUprightEar',[xy(sx*.067,-.31,1.685,.028,.034),xy(sx*.095,-.30,1.78,.045,.034),xy(sx*.13,-.285,1.91,.033,.025),xy(sx*.15,-.28,1.985,.008,.008)],0,lambda k,i:1 if i in[7,8,9]else 0)
# Small dark eye meshes seat into lateral head skin; fixed artistic eyes only.
def eye(name,c):
 n=12;rr=[]
 for k in range(1,6):
  a=math.pi*k/6;rr.append([(c[0]+.016*math.sin(a)*math.cos(math.tau*i/n),c[1]+.022*math.sin(a)*math.sin(math.tau*i/n),c[2]+.017*math.cos(a))for i in range(n)])
 solid_loft(name,rr,2)
for side,sx in [('Left',-1),('Right',1)]:eye(side+'SeatedSmallEye',(sx*.098,-.428,1.62))
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('Body_MutedRustBrown',(.42,.235,.115,1),.89,0),('BellyInnerEars_WarmSand',(.64,.49,.31,1),.91,0),('EyesNose_DeepBrown',(.026,.017,.009,1),.66,0)]
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
focus=Vector((0,0,1.0))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.70;aim(cam,(4.5,-6,3.1));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/animal/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'animal','style':'S01-clean-geometric','title':'Static Long-Foot Tail-Resting Kangaroo','description':'One original stylised fixed kangaroo-like animal with an ascending continuous torso and long neck, small elongated head and tapered muzzle, two upright pointed thick ears, two short raised forearms and two strongly developed hind limbs. Each hind limb is one closed continuous long ground foot, narrow hock, forward knee and broad thigh, not a separate enlarged rabbit paw. One long thick tapering rear tail has genuine finite ground-contact facets and completes the three-part resting support silhouette. New whole proportions and coordinates, no old seated rabbit, antlered deer, frog or robot mesh reused. Pale belly and ear regions belong to the full surfaces; small dark eyes are seated separate bodies and the nose is an integral muzzle cap. Three opaque constant matte PBR materials, metres, native Z up, head/front -Y and whole horizontal bounds-centred ground origin. Separate closed components use intentionally embedded fixed joins. One whole prop, zero scenes, no extra pose or juvenile. Artistic exterior only: no precise species or anatomy, sex/pouch/offspring, gait, jumping, balance, locomotion, biological behaviour, rig, physical simulation, welfare, manufacture or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
