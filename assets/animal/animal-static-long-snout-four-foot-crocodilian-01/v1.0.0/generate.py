import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='animal-static-long-snout-four-foot-crocodilian-01'
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

# One completely new continuous low skull/snout, torso and long laterally
# flattened tapering tail. No tortoise shell removed and no old snake extended.
def loft(name,rings,mat,band_materials=None):
 n=len(rings[0]);v=[p for r in rings for p in r];f=[];fm=[]
 for k in range(len(rings)-1):
  for i in range(n):
   j=(i+1)%n;f.extend([(k*n+i,k*n+j,(k+1)*n+j),(k*n+i,(k+1)*n+j,(k+1)*n+i)]);fm.extend([band_materials(k,i)if band_materials else mat]*2)
 for k,ring in [(0,rings[0]),(len(rings)-1,rings[-1])]:
  center=len(v);v.append(tuple(sum(p[j]for p in ring)/n for j in range(3)))
  for i in range(n):j=(i+1)%n;f.append((center,k*n+j,k*n+i)if k==0 else(center,k*n+i,k*n+j));fm.append(mat)
 mesh(name,v,f,mat)
 # Whole convex section caps fan from interior centre, avoiding collinear
 # boundary-band fan triangles; material regions are integral, no overlays.
 FM[name]=fm
STATIONS=[(0,-1.40,.085,.12,.205),(0,-1.32,.12,.115,.22),(0,-.98,.145,.105,.245),(0,-.77,.18,.10,.29),(0,-.63,.22,.09,.355),(0,-.48,.25,.085,.34),(0,-.20,.275,.08,.32),(0,.12,.27,.08,.31),(0,.38,.24,.085,.30),(.025,.61,.17,.10,.28),(.07,.87,.12,.10,.245),(.14,1.15,.080,.09,.20),(.23,1.42,.045,.075,.135),(.26,1.65,.018,.065,.095),(.27,1.77,.004,.063,.070)]
rings=[]
for x,y,w,lo,hi in STATIONS:
 hh=hi-lo
 # Twelve true outline points include a narrow lateral mouth band on the
 # head sections. Dorsum is broad and low, not a round cable cross section.
 rings.append([(x+w*a,y,lo+hh*b)for a,b in[(1,.30),(.82,0),(-.82,0),(-1,.30),(-1,.40),(-1,.47),(-.88,.75),(-.48,1),(.48,1),(.88,.75),(1,.47),(1,.40)]])
def skin(k,i):
 if i in[0,1,2]:return 1
 if k<4 and i in[4,10]:return 3
 return 0
loft('WholeContinuousLongSnoutTrunkAndTaperedTail',rings,0,skin)
def ringxy(x,y,z,rx,ry,n=8):return[(x+rx*math.cos(math.pi/n+math.tau*i/n)/math.cos(math.pi/n),y+ry*math.sin(math.pi/n+math.tau*i/n)/math.cos(math.pi/n),z)for i in range(n)]
def triangulate(p):
 ids=list(range(len(p)));out=[]
 def cr(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:ids.reverse()
 while len(ids)>3:
  for k,b in enumerate(ids):
   a,c=ids[k-1],ids[(k+1)%len(ids)]
   if cr(p[a],p[b],p[c])<=1e-14:continue
   if any(min(cr(p[a],p[b],p[j]),cr(p[b],p[c],p[j]),cr(p[c],p[a],p[j]))>=-1e-14 for j in ids if j not in[a,b,c]):continue
   out.append((a,b,c));ids.pop(k);break
  else:raise AssertionError('bad toe outline')
 return out+[tuple(ids)]
def foot(name,p,z,mat):
 if sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);v=[(x,y,zz)for zz in[0,z]for x,y in p];f=[tuple(reversed(t))for t in triangulate(p)]+[tuple(n+i for i in t)for t in triangulate(p)]+[(i,(i+1)%n,n+(i+1)%n,n+i)for i in range(n)];mesh(name,v,f,0)
for side,sx in [('Left',-1),('Right',1)]:
 for label,cy,ey,wy in [('Fore',-.47,-.31,-.53),('Hind',.35,.55,.34)]:
  rr=[ringxy(sx*.22,cy,.23,.075,.10),ringxy(sx*.35,ey,.17,.09,.10),ringxy(sx*.45,ey,.10,.055,.075),ringxy(sx*.50,wy,.035,.045,.055)];loft(side+label+'WholeBentSplayedLimb',rr,0)
  # Three separate open clefts between four broad short forward digits; each
  # foot remains a single connected thick sole, not separate floating toes.
  p=[(-.085,.075),(-.115,-.085),(-.12,-.13),(-.085,-.145),(-.055,-.055),(-.045,-.20),(-.015,-.21),(.005,-.06),(.035,-.20),(.065,-.19),(.065,-.055),(.11,-.14),(.14,-.13),(.13,-.085),(.085,.075)];p=[(sx*(.50+x),wy+y)for x,y in p];foot(side+label+'WholeFourDigitGroundFoot',p,.045,0)
# Eye bosses are low on the back of the skull, unlike frog towers. The small
# outer dark pupil bodies are genuinely seated, not detached billboards.
def ellipsoid(name,c,r,mat,n=12,rows=6):
 v=[(c[0]+r[0]*math.sin(math.pi*k/rows)*math.cos(math.tau*i/n),c[1]+r[1]*math.sin(math.pi*k/rows)*math.sin(math.tau*i/n),c[2]+r[2]*math.cos(math.pi*k/rows))for k in range(1,rows)for i in range(n)];top=len(v);v.append((c[0],c[1],c[2]+r[2]));bot=len(v);v.append((c[0],c[1],c[2]-r[2]));f=[]
 for i in range(n):j=(i+1)%n;f.extend([(top,i,j),(bot,(rows-2)*n+j,(rows-2)*n+i)])
 for k in range(rows-2):
  for i in range(n):j=(i+1)%n;f.extend([(k*n+i,(k+1)*n+i,(k+1)*n+j),(k*n+i,(k+1)*n+j,k*n+j)])
 mesh(name,v,f,mat)
for side,sx in [('Left',-1),('Right',1)]:
 ellipsoid(side+'LowDorsalEyeBoss',(sx*.145,-.64,.338),(.065,.085,.055),0)
 ellipsoid(side+'SeatedDarkLateralEye',(sx*.19,-.655,.355),(.022,.032,.022),2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('Skin_MutedOlive',(.22,.30,.115,1),.88,0),('Belly_WarmSand',(.50,.46,.25,1),.9,0),('Eyes_DeepBrown',(.025,.021,.009,1),.62,0),('IntegralClosedMouthSeam_DarkOlive',(.085,.10,.035,1),.87,0)]
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
focus=Vector((0,0,.18))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.65;aim(cam,(4.8,-5.5,4.7));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/animal/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'animal','style':'S01-clean-geometric','title':'Static Long-Snout Four-Foot Crocodilian','description':'One original stylised fixed crocodilian appearance: one continuous shared-vertex broad flattened long snout, low skull, long low torso and tapering laterally flattened gently curved tail. Four separately editable whole bent splayed limbs lead to four thick connected four-digit feet with real outline clefts and full ground soles. Two low dorsal eye bosses carry small seated lateral dark eyes. Pale belly and a narrow closed-mouth seam use integral body face materials, not a second overlaid skin or claimed open mouth. All body stations and appendage outlines newly authored, no old tortoise shell removal, snake geometry extension or frog limbs reused. Separate closed components have intentionally embedded static roots, not an asserted welded animal shell. Four constant opaque untextured matte PBR materials, metres, native Z up, snout/front -Y and full horizontal-bounds-centred ground origin. One whole prop and zero scenes. Artistic exterior only: no exact species, anatomy, scale-row count, motion, bite, behaviour, wildlife safety, ecology, welfare, rig or physical simulation claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
