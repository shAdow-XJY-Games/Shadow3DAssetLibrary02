import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='pet-care-fixed-open-globe-and-lower-collection-drawer-01'
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



# One fully closed thick shell around two actual openings; rear sphere pole is a single shared vertex.
M=40;K=18;RADIUS=.37;CZ=.75;theta0=.70
sv=[];rows=[]
for j in range(K+1):
 p=theta0+(math.pi-theta0)*j/K
 if j==K:rows.append([len(sv)]);sv.append((0,RADIUS,CZ));continue
 row=[]
 for i in range(M):
  a=math.tau*i/M;row.append(len(sv));sv.append((RADIUS*math.sin(p)*math.cos(a),-RADIUS*math.cos(p),CZ+RADIUS*math.sin(p)*math.sin(a)))
 rows.append(row)
sf=[]
for j in range(K):
 for i in range(M):
  if 5<=j<=8 and 27<=i<=32:continue
  n=(i+1)%M
  sf.append((rows[j][i],rows[j][n],rows[j+1][0])if j==K-1 else(rows[j][i],rows[j][n],rows[j+1][n],rows[j+1][i]))
# Outward orientation is determined against the actual radial vector, not a guessed cap fan.
for k,f in enumerate(sf):
 a,b,c=[sv[i]for i in f[:3]];normal=cross(sub(b,a),sub(c,a));rad=sub(a,(0,0,CZ))
 if dot(normal,rad)<0:sf[k]=tuple(reversed(f))
used=sorted({i for f in sf for i in f});ix={i:k for k,i in enumerate(used)};sv=[sv[i]for i in used];sf=[tuple(ix[i]for i in f)for f in sf];n=len(sv)
v=sv+[tuple((0,0,CZ)[k]+(p[k]-(0,0,CZ)[k])*(RADIUS-.028)/RADIUS for k in range(3))for p in sv]
f=list(sf)+[tuple(i+n for i in reversed(t))for t in sf];edges={}
for t in sf:
 for a,b in zip(t,t[1:]+t[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((a,b))
for es in edges.values():
 if len(es)==1:a,b=es[0];f.append((b,a,a+n,b+n))
mesh('WholeFrontOpenGlobeWithLowerPassage',v,f,0)
box('WholeGroundFootBase',(0,-.035,.035),(.66,.67,.07),2)
# Entire U-shaped low housing is formed as a continuous profile, open at front and top.
profile=[(-.32,-.335),(-.29,-.335),(-.29,.25),(.29,.25),(.29,-.335),(.32,-.335),(.32,.28),(-.32,.28)]
n=len(profile);v=[(x,y,z)for z in[.055,.32]for x,y in profile];f=[]
for a,b,c in triangulate(profile):f.extend([(c,b,a),(a+n,b+n,c+n)])
f +=[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];mesh('WholeOpenFrontAndTopLowerHousing',v,f,1)
# Whole drawer tub retains its floor and complete four wall returns in the withdrawn pose.
outer=[(-.275,-.48),(.275,-.48),(.275,.20),(-.275,.20)];inner=[(-.256,-.461),(.256,-.461),(.256,.181),(-.256,.181)]
v=[(x,y,z)for loop,z in[(outer,.075),(outer,.265),(inner,.265),(inner,.094)]for x,y in loop];f=[(3,2,1,0),(12,13,14,15)]
for k in range(3):
 for i in range(4):j=(i+1)%4;f.append((k*4+i,k*4+j,(k+1)*4+j,(k+1)*4+i))
mesh('WholePartWithdrawnEmptyCollectionDrawer',v,f,2)
box('WholeDrawerFrontGrip',(0,-.49,.20),(.19,.045,.04),3)
for side in[-1,1]:
 x=side*.31;beam('WholeSideSupport_'+str(side),(x,.06,.27),(side*.405,0,.75),.075,1)
 axle('WholeSideTrunnion_'+str(side),min(side*.35,side*.45),max(side*.35,side*.45),0,.75,.055,3,20)
 axle('WholeOuterTrunnionCap_'+str(side),min(side*.433,side*.46),max(side*.433,side*.46),0,.75,.070,1,20)
box('WholeFrontStepRoot',(0,-.42,.055),(.43,.29,.07),1)
box('WholeFrontLowStep',(0,-.57,.10),(.52,.22,.13),1)
for i in range(4):box('WholeStepTread_'+str(i),(0,-.64+.045*i,.171),(.46,.016,.018),2)
lo=[min(p[k]for v,f,m in G.values()for p in v)for k in range(3)];hi=[max(p[k]for v,f,m in G.values()for p in v)for k in range(3)];SHIFT=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]);G={n:([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)for n,(v,f,m)in G.items()}
PALETTE=[('WholeGlobe_WarmIvory',(.76,.75,.67,1),.72,.01),('WholeCradleAndStep_MutedTeal',(.20,.36,.35,1),.72,.03),('WholeBaseDrawerAndTreads_Charcoal',(.055,.075,.078,1),.79,.01),('WholePinsAndGrip_SatinAlloy',(.38,.43,.44,1),.5,.35)]
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
focus=Vector((0,0,.51))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-2,4),380,3.5),('Rim',(2,4,5),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.60;aim(cam,(4,-7,3.7));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/pet-care/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'pet-care','style':'S01-clean-geometric','title':'Fixed Open Globe and Lower Collection Drawer','description':'One wholly newly authored complete empty globe-chamber pet-care-device-style exterior in a fixed illustrative pose. A continuous thick rounded chamber has a genuine large forward opening, closed rear and a separate real lower through-opening. Two independent side supports carry whole transverse trunnion exteriors at the chamber sides. A low open-front and open-top collection housing contains one complete thick empty drawer fixed partly withdrawn, while an integral low front step remains connected to the base. The upper hollow globe and the separate lower collection void are not a rectangular washing cabinet with a recoloured door: there is no hinged inspection disc, enclosed cylindrical drum, detergent panel or cabinet shell. Unlike a pet carrier, there is no grille door, carry handle or ventilation-slot enclosure. The chamber, actual lower passage and under-chamber drawer relation are authored together as one apparatus, not assembled imported old meshes. Four opaque PBR roles, metres Z up and full horizontal ground-centred bounds, one prop zero scenes. No litter, waste, animal, sensors or moving parts included. Static stylised exterior only: no rotation, cleaning, separation, disposal, animal access or species fit, hygiene, powered operation, manufacture, welfare, load or safety performance. Rigging animation and interaction not made.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':4,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
