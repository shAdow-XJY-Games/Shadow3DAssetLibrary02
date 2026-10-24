import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='arcade-fixed-pierced-deck-pop-target-cabinet-01'
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



# Complete new low cabinet with genuinely pierced target deck, not a vertical peg field.
box('WholeGroundFootCabinetPlinth',(0,0,.055),(.97,1.12,.11),0)
box('WholeLowCabinetBody',(0,0,.345),(.90,1.05,.56),0)
# Low solid body top is below every through-hole and anchors the fixed target stems.
for x in[-.431,.431]:box('WholeDeckSideSupport_'+str(x),(x,0,.736),(.050,1.04,.262),0)
for y in[-.497,.497]:box('WholeDeckEndSupport_'+str(y),(0,y,.736),(.90,.050,.278),0)
for y in[-.16,.16]:box('WholeUnderDeckCrossSupport_'+str(y),(0,y,.80),(.86,.035,.075),0)
# Six separate thick square deck panels each have an actual continuous round through opening.
angles=sorted(set([math.tau*i/24 for i in range(24)]+[math.atan2(y,x)%math.tau for x in[-.205,.205]for y in[-.16,.16]]));N=len(angles)
for row,yc in enumerate([-.32,0,.32]):
 for col,xc in enumerate([-.205,.205]):
  v=[];f=[]
  for z,inside in[(.82,False),(.82,True),(.86,False),(.86,True)]:
   for a in angles:
    c=math.cos(a);ss=math.sin(a);r=.100 if inside else min(.205/max(abs(c),1e-12),.16/max(abs(ss),1e-12));v.append((xc+r*c,yc+r*ss,z))
  for i in range(N):
   j=(i+1)%N;f.extend([(i,j,N+j,N+i),(2*N+i,3*N+i,3*N+j,2*N+j),(i,2*N+i,2*N+j,j),(N+i,N+j,3*N+j,3*N+i)])
  mesh('WholePiercedTargetDeckPanel_%d_%d'%(row,col),v,f,1)
  lathe_z('WholeOpenTargetRim_%d_%d'%(row,col),xc,yc,[(.102,.850),(.116,.850),(.116,.878),(.102,.878)],0,24)
  top=[.96,.89,1.02,.92,.985,.87][row*2+col]
  lathe_z('WholeFixedDomedTargetOnStem_%d_%d'%(row,col),xc,yc,[(0,.61),(.035,.61),(.035,top-.105),(.078,top-.100),(.082,top-.055),(.068,top-.020),(0,top)],2,24)
# Rear blank score/header panel is only a fixed exterior, not a functional display.
box('WholeRearHeaderUpright',(0,.522,.995),(.90,.055,.43),0)
box('WholeBlankHeaderInset',(0,.488,1.025),(.75,.022,.24),1)
box('WholeHeaderTopCap',(0,.525,1.220),(.95,.085,.055),0)
box('WholeBlankFrontInset',(0,-.534,.40),(.47,.028,.23),1)
# One mallet rests in a real attached side holder and has one continuous thick cord.
box('WholeSideMalletHolderArm',(.493,-.35,.725),(.14,.10,.065),0)
box('WholeSideMalletHandleSeat',(.56,-.35,.750),(.09,.095,.07),0)
lathe_z('WholeRestingMalletHandle',.56,-.35,[(0,.73),(.016,.73),(.016,1.025),(0,1.025)],1,12)
axle('WholeSoftLookingMalletHead',.485,.635,-.35,1.020,.055,2,20)
path=[(.44,-.43,.70),(.58,-.49,.62),(.68,-.46,.69),(.66,-.38,.84),(.56,-.35,.83)];v=[];f=[];N=8
for k,p in enumerate(path):
 t=unit(sub(path[min(k+1,len(path)-1)],path[max(k-1,0)]));u=unit(cross(t,(0,0,1)if abs(t[2])<.9 else(1,0,0)));w=cross(t,u)
 for j in range(N):v.append(tuple(p[i]+.006*(u[i]*math.cos(math.tau*j/N)+w[i]*math.sin(math.tau*j/N))for i in range(3)))
f=[tuple(reversed(range(N))),tuple((len(path)-1)*N+j for j in range(N))]
for k in range(len(path)-1):
 for j in range(N):f.append((k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j))
mesh('WholeContinuousMalletTetherCord',v,f,2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeCabinetRimsAndHolder_MutedTeal',(.055,.23,.26,1),.76,0),('WholePiercedDeckAndBlankPanels_WarmIvory',(.64,.55,.36,1),.78,0),('WholeFixedTargetsMalletHeadAndCord_MutedCoral',(.52,.15,.08,1),.82,0)]
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
focus=Vector((0,0,.64))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.05;aim(cam,(3,-5,4.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/arcade/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'arcade','style':'S01-clean-geometric','title':'Fixed Pierced Deck Pop Target Cabinet','description':'One newly authored complete static pop-target amusement cabinet. A whole low grounded cabinet supports six thick deck panels with genuine round through openings and raised annular rims. Six complete round-topped targets have continuous stems seated on the lower cabinet top and are fixed at different visible heights within the real holes. A blank rear header and blank front inset complete the case. One separately modelled mallet is parked in its attached side holder and joined to the cabinet by a continuous solid tether cord. Numeric geometry is new, not a vertical peg-drop field, inclined roll lane, ring-toss table or rearranged old game props. The six targets and deck pieces count only as parts of this one whole model, zero scenes. Three opaque untextured PBR materials, metres, native Z up and full horizontally centred ground datum. Static simplified game-art exterior only, no animal faces or licensed characters. No popping motion, scoring, sensors, electronics, playable rules, impact response, operating amusement machine, manufacture or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
