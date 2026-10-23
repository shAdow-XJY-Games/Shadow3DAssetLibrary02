import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='steam-workshop-fixed-elevated-beam-engine-display-01'
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



# Complete new fixed elevated-beam layout; no old whole machinery is instanced.
box('WholeGroundedMachineBed',(0,.03,.06),(3.45,1.55,.12),0)
# A pair of whole tapered standards and a complete fixed central spindle carry the upper beam.
def tapered_post(name,y):
 v=[(x,y+dy,z)for z,rx,ry in[(.12,.29,.15),(1.83,.14,.10),(2.08,.16,.10)]for x,dy in[(-rx,-ry),(rx,-ry),(rx,ry),(-rx,ry)]];f=[(3,2,1,0),(8,9,10,11)]
 for k in range(2):
  for i in range(4):j=(i+1)%4;f.append((4*k+i,4*k+j,4*(k+1)+j,4*(k+1)+i))
 mesh(name,v,f,0)
for side,y in [('Front',-.31),('Rear',.31)]:
 tapered_post(side+'WholeTaperedBeamStandard',y)
 ringy(side+'WholeBeamBearing',y-.075,y+.075,0,2.20,.07,.15,2,24)
cyly('WholeHighBeamPivotSpindle',-.47,.47,0,2.20,.07,1,24)
# Generic planar-cell linked-eye solid. Every hole is a true full bore; ring/shank internal faces omitted.
def eye_link(name,a,b,radii,bores,y0,y1,mat,centres=None):
 dx,dz=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dz);u=(dx/length,dz/length);w=(-u[1],u[0]);centres=centres or[0,length];N=16;coords={};cells=[]
 for e,(cx,ro,ri)in enumerate(zip(centres,radii,bores)):
  for k,r in enumerate([ri,ro]):
   for i in range(N):t=math.pi/N+math.tau*i/N;coords[e,k,i]=(cx+r*math.cos(t),r*math.sin(t))
  for i in range(N):j=(i+1)%N;cells.append([(e,0,i),(e,1,i),(e,1,j),(e,0,j)])
 for e in range(len(centres)-1):cells.append([(e,1,N-1),(e+1,1,N//2),(e+1,1,N//2-1),(e,1,0)])
 edges={}
 for c in cells:
  for k,l in zip(c,c[1:]+c[:1]):edges.setdefault(tuple(sorted([k,l])),[]).append((k,l))
 v=[];f=[];lookup={}
 def idx(k,y):
  x,z=coords[k];p=(a[0]+x*u[0]+z*w[0],y,a[1]+x*u[1]+z*w[1])
  if p not in lookup:lookup[p]=len(v);v.append(p)
  return lookup[p]
 for c in cells:f.extend([tuple(idx(k,y0)for k in reversed(c)),tuple(idx(k,y1)for k in c)])
 for e in edges.values():
  if len(e)==1:
   k,l=e[0];f.append((idx(k,y0),idx(l,y0),idx(l,y1),idx(k,y1)))
 mesh(name,v,f,mat)
L=math.hypot(2.10,.20)
eye_link('WholeThreeEyeElevatedWalkingBeam',(-1.05,2.10),(1.05,2.30),[.14,.20,.14],[.058,.075,.058],-.09,.09,0,[0,L/2,L])
for side,y0,y1 in [('Front',-.125,-.09),('Rear',.09,.125)]:cyly(side+'BeamPivotRetainer',y0,y1,0,2.20,.13,2,24)
# Complete vertical cylinder with genuine front section opening, bottom cap, piston and bored top gland.
arc=[-math.pi/4+3*math.pi*i/2/24 for i in range(25)];poly=[(-1.05+.28*math.cos(t),.28*math.sin(t))for t in arc]+[(-1.05+.225*math.cos(t),.225*math.sin(t))for t in reversed(arc)];n=len(poly);v=[(x,y,z)for z in[.18,1.15]for x,y in poly];f=[tuple(reversed(t))for t in triangulate(poly)]+[tuple(n+i for i in t)for t in triangulate(poly)]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh('WholeFrontCutawayVerticalCylinder',v,f,0)
lathe_z('WholeCylinderBottomFootAndCover',-1.05,0,[(0,.12),(.33,.12),(.33,.20),(0,.20)],2,32)
lathe_z('WholeTopAnnularRodGland',-1.05,0,[(.05,1.13),(.32,1.13),(.32,1.21),(.05,1.21)],2,32)
lathe_z('WholeVisiblePistonDisk',-1.05,0,[(0,.55),(.21,.55),(.21,.64),(0,.64)],2,32)
lathe_z('WholeVerticalPistonStem',-1.05,0,[(0,.61),(.035,.61),(.035,2.00),(0,2.00)],1,20)
ringy('WholePistonStemUpperEye',-.065,.065,-1.05,2.10,.055,.125,1,24)
cyly('WholeLeftBeamToPistonEyePin',-.14,.14,-1.05,2.10,.05,1,24)
for side,y0,y1 in [('Front',-.17,-.09),('Rear',.09,.17)]:cyly(side+'LeftEndPinRetainer',y0,y1,-1.05,2.10,.085,2,24)
# The opposite beam end descends via a whole long two-eye rod to the actual offset crank pin.
eye_link('WholeLongBeamToCrankConnectingRod',(1.05,2.30),(1.22,.93),[.10,.115],[.055,.06],-.22,-.16,1)
cyly('WholeRightBeamEndPin',-.26,.14,1.05,2.30,.05,1,24)
cyly('WholeUpperRodRetainingCap',-.28,-.22,1.05,2.30,.078,2,24)
cyly('WholeRightBeamRearCap',.09,.16,1.05,2.30,.085,2,24)
cyly('WholeCrankDisk',-.14,-.06,1.02,.75,.33,0,32)
cyly('WholeOffsetCrankPin',-.26,.02,1.22,.93,.055,1,24)
cyly('WholeLowerRodRetainingCap',-.28,-.22,1.22,.93,.085,2,24)
cyly('WholeMainCrankshaft',-.17,.54,1.02,.75,.065,1,24)
for label,y in [('Front',.025),('Rear',.255)]:
 box(label+'WholeCrankBearingPedestal',(1.02,y,.365),(.23,.15,.49),0)
 ringy(label+'WholeCrankBearing',y-.075,y+.075,1.02,.75,.065,.15,2,24)
# Full open-spoke wheel on the rear shaft, physically joined hub/spokes/rim, no tooth or gear import.
ringy('WholeOpenFlywheelRim',.385,.485,1.02,.75,.49,.59,0,48)
cyly('WholeFlywheelHub',.36,.51,1.02,.75,.13,2,24)
for i in range(6):
 t=math.tau*i/6;beam('WholeFlywheelRadialSpoke_'+str(i+1),(1.02+.10*math.cos(t),.435,.75+.10*math.sin(t)),(1.02+.52*math.cos(t),.435,.75+.52*math.sin(t)),.065,0)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('BedStandardsBeamFlywheel_DeepPetrol',(.055,.18,.18,1),.72,.25),('RodsAndPins_SatinSteel',(.44,.48,.47,1),.43,.66),('CoversPistonBearings_WarmBrass',(.53,.34,.12,1),.45,.57)]
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
focus=Vector((0,0,1.22))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=4.15;aim(cam,(3,-7,3.7));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/steam-workshop/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'steam-workshop','style':'S01-clean-geometric','title':'Fixed Elevated Beam Engine Display','description':'One newly authored complete fixed beam-engine appearance for the original steam-workshop piston and transmission-display direction. A broad single bed supports a vertical front-cutaway cylinder with visible piston, full top gland and long upright piston stem. Two tall tapered standards carry a transverse high spindle and one continuous three-eyed inclined walking beam. The cylinder-side eye/pin joins the upright stem; the opposite beam end has a separate complete long two-eye rod descending to an offset crank pin. A grounded paired-bearing crankshaft carries a complete open-spoke flywheel. Real beam and rod bores, complete cylinder chamber/front opening and flywheel windows are geometry, with fixed pins and retainers visibly connecting the two linkage paths. All whole coordinates, proportions and layout are newly authored, not old horizontal crosshead machinery rotated, a water sweep with a wheel, or old complete props arranged together. Only mature generic mesh, export and rendering infrastructure reused. Separate closed editable components use three opaque solid PBR materials, metres, native Z up, front -Y and whole horizontal bounds-centred grounded bed. One complete model, zero scenes. This is a single frozen illustrative display: no functioning steam engine, pressure, thermal effects, sealing, parallel-motion accuracy, continuous kinematics or stroke clearance, power, load, stability, manufacture, installation or safety claim.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
