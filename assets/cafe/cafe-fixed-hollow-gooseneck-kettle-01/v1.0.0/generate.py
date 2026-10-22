"""Original fixed hollow gooseneck kettle; maker SELF_REVIEW workflow."""
import math,collections,json,time,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

def dot(a,b):return sum(x*y for x,y in zip(a,b))

def sub(a,b):return tuple(x-y for x,y in zip(a,b))

def add(a,b):return tuple(x+y for x,y in zip(a,b))

def mul(v,s):return tuple(x*s for x in v)

def unit(v):
 n=math.sqrt(dot(v,v));assert math.isfinite(n) and n>0
 return tuple(x/n for x in v)

def area(p):return sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))/2

def clean(p):
 out=[]
 for q in p:
  q=tuple(round(x,12)for x in q)
  if not out or q!=out[-1]:out.append(q)
 if len(out)>1 and out[0]==out[-1]:out.pop()
 return out

def clip(p,l):
 if not p:return []
 a,b,c=l;out=[];u=p[-1];du=a*u[0]+b*u[1]-c
 for v in p:
  dv=a*v[0]+b*v[1]-c
  if(du<=1e-13)!=(dv<=1e-13):
   t=du/(du-dv);out.append(tuple(u[k]+t*(v[k]-u[k])for k in range(2)))
  if dv<=1e-13:out.append(v)
  u=v;du=dv
 out=clean(out);return out if len(out)>2 and area(out)>1e-14 else []

def planes(p):
 out=[]
 for a,b in zip(p,p[1:]+p[:1]):
  u,v=b[0]-a[0],b[1]-a[1];n=math.hypot(u,v);out.append((v/n,-u/n,(v*a[0]-u*a[1])/n))
 return out

def contains(p,poly):
 # All classified cells already split at every edge's entire supporting line.
 x,y=p;inside=False
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if(a[1]>y)!=(b[1]>y)and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:inside=not inside
 return inside

def rect(y0,z0,y1,z1):return[(y0,z0),(y1,z0),(y1,z1),(y0,z1)]

def build(parts,holes=[],mat=0):
 # Each part: x0,x1,CCW yz polygon. Union boundary only, no internal faces.
 polygons=[r[2]for r in parts+holes];allp=[q for p in polygons for q in p];lo=[min(q[k]for q in allp)for k in[0,1]];hi=[max(q[k]for q in allp)for k in[0,1]]
 cells=[rect(lo[0],lo[1],hi[0],hi[1])];seen=set();lines=[]
 for p in polygons:
  for l in planes(p):
   key=tuple(round(x,10)for x in l)
   if key not in seen:seen.add(key);lines.append(l)
 for l in lines:
  nxt=[]
  for p in cells:
   ds=[l[0]*q[0]+l[1]*q[1]-l[2]for q in p]
   if min(ds)<-1e-10 and max(ds)>1e-10:
    a=clip(p,l);b=clip(p,tuple(-v for v in l));assert a and b,(l,p);nxt +=[a,b]
   else:nxt.append(p)
  cells=nxt
 ec=collections.defaultdict(list)
 for i,p in enumerate(cells):
  for a,b in zip(p,p[1:]+p[:1]):ec[tuple(sorted((a,b)))].append(i)
 assert all(len(v)<=2 for v in ec.values())
 xx=sorted(set(v for a,b,p in parts+holes for v in[a,b]));occ=[]
 for x0,x1 in zip(xx,xx[1:]):
  x=(x0+x1)/2;ss=set()
  for i,p in enumerate(cells):
   c=tuple(sum(q[k]for q in p)/len(p)for k in[0,1])
   if any(a<x<b and contains(c,q)for a,b,q in parts)and not any(a<x<b and contains(c,q)for a,b,q in holes):ss.add(i)
  occ.append(ss)
 vv=[];ff=[];lookup={}
 def vertex(p):
  p=tuple(round(x,12)for x in p)
  if p not in lookup:lookup[p]=len(vv);vv.append(p)
  return lookup[p]
 def tri(p):
  assert dot(cross(sub(p[1],p[0]),sub(p[2],p[0])),cross(sub(p[1],p[0]),sub(p[2],p[0])))>1e-28,p
  ids=tuple(vertex(q)for q in p);assert len(set(ids))==3;ff.append(ids)
 for k,ss in enumerate(occ):
  x0,x1=xx[k:k+2]
  for i in sorted(ss):
   p=cells[i];c=tuple(sum(q[h]for q in p)/len(p)for h in[0,1])
   for x,sign,j in[(x0,-1,k-1),(x1,1,k+1)]:
    if not 0<=j<len(occ)or i not in occ[j]:
     for a,b in zip(p,p[1:]+p[:1]):
      q=[(x,*c),(x,*a),(x,*b)];tri(q if sign>0 else q[::-1])
   for a,b in zip(p,p[1:]+p[:1]):
    other=next((j for j in ec[tuple(sorted((a,b)))]if j!=i),None)
    if other is None or other not in ss:
     aa=(x0,*a);bb=(x0,*b);cc=(x1,*b);dd=(x1,*a);tri([aa,bb,cc]);tri([aa,cc,dd])
 return dict(vertices=vv,faces=ff,face_materials=[mat]*len(ff),material=mat,yz_cells=len(cells),x_levels=xx)

def topology(g):
 v=g['vertices'];f=g['faces'];e=collections.defaultdict(list);stars=collections.defaultdict(list)
 for t in f:
  for a,b in zip(t,t[1:]+t[:1]):e[tuple(sorted((a,b)))].append((a,b))
  for j,a in enumerate(t):stars[a].append(tuple(t[k]for k in range(3)if k!=j))
 bad=[(k,q)for k,q in e.items()if len(q)!=2 or q[0]!=q[1][::-1]];assert not bad,bad[:10]
 for i,links in stars.items():
  a=collections.defaultdict(set)
  for x,y in links:a[x].add(y);a[y].add(x)
  seen=set();todo=[next(iter(a))]
  while todo:
   x=todo.pop()
   if x not in seen:seen.add(x);todo.extend(a[x]-seen)
  assert seen==set(a)and all(len(q)==2 for q in a.values()),('fan',i)
 volume=sum(dot(v[a],cross(v[b],v[c]))for a,b,c in f)/6;assert volume>0
 return dict(vertices=len(v),triangles=len(f),euler=len(v)-len(e)+len(f),signed_volume=volume,single_vertex_fans=True)


def finish(vv,ff,mi):
    if sum(dot(vv[a],cross(vv[b],vv[c]))for a,b,c in ff)<0:ff=[q[::-1]for q in ff]
    return dict(vertices=vv,faces=ff,face_materials=mi,material=mi[0])
def revolved(profile,closed,material,n=8):
    vv=[];ff=[]
    for r,z in profile:
        vv.extend([(r*math.cos(2*math.pi*i/n+math.pi/8),r*math.sin(2*math.pi*i/n+math.pi/8),z)for i in range(n)])
    for j in range(len(profile)if closed else len(profile)-1):
        k=(j+1)%len(profile)
        for i in range(n):
            a=j*n+i;b=j*n+(i+1)%n;c=k*n+(i+1)%n;d=k*n+i;ff.extend([(a,b,c),(a,c,d)])
    if not closed:
        for j,reverse in [(0,True),(len(profile)-1,False)]:
            k=len(vv);vv.append((0,0,profile[j][1]))
            for i in range(n):
                q=(k,j*n+i,j*n+(i+1)%n);ff.append(q[::-1]if reverse else q)
    return finish(vv,ff,[material]*len(ff))
def ported_body():
    n=16;profile=[(.050,0),(.060,.005),(.060,.100),(.052,.120),(.048,.120),(.054,.100),(.054,.012)];vv=[];ff=[];lookup={}
    def vertex(p):
        p=tuple(round(x,12)for x in p)
        if p not in lookup:lookup[p]=len(vv);vv.append(p)
        return lookup[p]
    rings=[[vertex((r*math.cos(math.pi/16+2*math.pi*i/n),r*math.sin(math.pi/16+2*math.pi*i/n),z))for i in range(n)]for r,z in profile]
    def quad(a,b,c,d):ff.extend([(a,b,c),(a,c,d)])
    yo=-.060*math.cos(math.pi/16);yi=-.054*math.cos(math.pi/16)
    for j in range(len(rings)-1):
        for i in range(n):
            q=[rings[j][i],rings[j][(i+1)%n],rings[j+1][(i+1)%n],rings[j+1][i]]
            if i==11 and j in[1,5]:
                angles=[(225+45*k if j==1 else 135-45*k)*math.pi/180 for k in range(8)];y=yo if j==1 else yi
                h=[vertex((.006*math.cos(a),y,.035+.006*math.sin(a)))for a in angles]
                for k in range(4):
                    a=q[k];b=q[(k+1)%4];u=h[2*k];v=h[(2*k+1)%8];w=h[(2*k+2)%8];ff.extend([(a,b,w),(a,w,v),(a,v,u)])
            else:quad(*q)
    for j,reverse in[(0,True),(len(rings)-1,False)]:
        c=vertex((0,0,profile[j][1]))
        for i in range(n):
            t=(c,rings[j][i],rings[j][(i+1)%n]);ff.append(t[::-1]if reverse else t)
    h=[[vertex((.006*math.cos((225+45*k)*math.pi/180),y,.035+.006*math.sin((225+45*k)*math.pi/180)))for k in range(8)]for y in[yo,yi]]
    for i in range(8):k=(i+1)%8;quad(h[0][i],h[0][k],h[1][k],h[1][i])
    return finish(vv,ff,[0]*len(ff))
def curved_hollow_spout():
    yy=-.060*math.cos(math.pi/16);centres=[(0,yy,.035),(0,-.075,.035),(0,-.095,.045),(0,-.108,.070),(0,-.111,.100),(0,-.125,.125),(0,-.145,.135)];radii=[.008,.008,.0075,.007,.0065,.006,.0055];vv=[];ff=[];rings=[]
    for inner in[False,True]:
        row=[]
        for j,(c,r)in enumerate(zip(centres,radii)):
            t=unit(sub(centres[min(j+1,len(centres)-1)],centres[max(0,j-1)]));u=(1,0,0);v=cross(t,u);rr=r-.002 if inner else r;ids=[]
            for k in range(8):
                a=(225+45*k)*math.pi/180;ids.append(len(vv));vv.append(add(c,add(mul(u,rr*math.cos(a)),mul(v,rr*math.sin(a)))))
            row.append(ids)
        rings.append(row)
    def quad(a,b,c,d,reverse=False):
        q=[a,b,c,d];q=q[::-1]if reverse else q;ff.extend([(q[0],q[1],q[2]),(q[0],q[2],q[3])])
    for inside in[0,1]:
        for j in range(len(centres)-1):
            for i in range(8):k=(i+1)%8;quad(rings[inside][j][i],rings[inside][j][k],rings[inside][j+1][k],rings[inside][j+1][i],bool(inside))
    for i in range(8):
        k=(i+1)%8;quad(rings[0][0][i],rings[1][0][i],rings[1][0][k],rings[0][0][k]);quad(rings[0][-1][i],rings[0][-1][k],rings[1][-1][k],rings[1][-1][i])
    return finish(vv,ff,[1]*len(ff))
def c_handle():
    b=.060*math.cos(math.pi/16);outer=[(b,.095),(.105,.115),(.128,.095),(.128,.035),(.105,.015),(b,.020)];inner=[(b,.083),(.098,.098),(.112,.085),(.112,.045),(.095,.030),(b,.032)];vv=[];ff=[];lookup={}
    def vertex(p):
        p=tuple(p)
        if p not in lookup:lookup[p]=len(vv);vv.append(p)
        return lookup[p]
    def quad(points):
        q=[vertex(p)for p in points];ff.extend([(q[0],q[1],q[2]),(q[0],q[2],q[3])])
    for j in range(5):
        p=[outer[j],outer[j+1],inner[j+1],inner[j]]
        if area(p)<0:p.reverse()
        for x in[-.007,.007]:quad([(x,*q)for q in(p[::-1]if x<0 else p)])
    boundary=outer+inner[::-1]
    if area(boundary)<0:boundary.reverse()
    for a,b in zip(boundary,boundary[1:]+boundary[:1]):quad([(-.007,*a),(-.007,*b),(.007,*b),(.007,*a)])
    return finish(vv,ff,[2]*len(ff))
def geometry():
    g={'HollowKettleBodyWithTrueSidePort':ported_body(),'ContinuousOpenEndedRisingGooseneckSpout':curved_hollow_spout(),'FixedConicalKettleLid':revolved([(.054,.120),(.016,.134)],False,0,n=16),'SmallFacetedLidKnob':revolved([(.009,.134),(.012,.144),(.009,.149)],False,2,n=12),'RearOpenCHandleWithTwoFullWallSeats':c_handle()}
    pts=[v for q in g.values()for v in q['vertices']];cy=(min(v[1]for v in pts)+max(v[1]for v in pts))/2
    for q in g.values():q['vertices']=[(x,y-cy,z)for x,y,z in q['vertices']];q['role']='Original fixed hollow gooseneck-kettle component'
    return g
START=time.time()
ASSET='cafe-fixed-hollow-gooseneck-kettle-01';VERSION='1.0.0';TITLE='Fixed Hollow Gooseneck Kettle'
DESCRIPTION='One original static gooseneck kettle. A genuinely hollow faceted pot body has a complete front side port through its material wall. A continuous rising hollow spout is seated by its annular inlet around that port and ends in a small open upward-tilted mouth. A fixed conical lid and knob cover the main chamber; a separate rear open C handle has two full flat wall seats. Five closed editable material meshes, three opaque untextured PBR materials. Metres, Z up, front -Y, horizontal-bounds-centred grounded sole. No fluid simulation, controlled pour rate, heat source, pressure, food-contact fitness, working lid hinge or safe use is claimed. Newly authored complete vessel, not the moka pot resized, a stockpot with colour changes or a spout extracted from a serving pitcher.'
PALETTE=[('KettleBodyAndLid_MutedBlue',(.12,.23,.31,1),.50,.12),('HollowSpout_SatinMetal',(.55,.59,.61,1),.40,.65),('HandleAndKnob_Charcoal',(.035,.044,.050,1),.74,0)]
G=geometry()
if '--source-check' in sys.argv:
    print(json.dumps({'status':'PASS_SOURCE_SELF_REVIEW','review_mode':'SELF_REVIEW','asset_id':ASSET,'components':{k:topology(g)for k,g in G.items()}},indent=2));sys.exit(0)
FOCUS=(0,0,.075);ORTHO=.38;CAMERAS={'thumbnail':(.45,-.43,.33),'qa-front':(.46,-.39,.25)}
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.seed=17
scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
EXPECTED={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False],'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4}
def config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def guard():c=config();assert c==EXPECTED,c;return c
mats=[]
for name,color,rough,metal in PALETTE:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;p.inputs['Alpha'].default_value=1.;p.inputs['Transmission Weight'].default_value=0.;p.inputs['Emission Strength'].default_value=0.;mats.append(m)
bpy.context.preferences.filepaths.save_version=0
root=bpy.data.objects.new('OneFixedHollowGooseneckKettle',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='kettle body sole Z=0; true side port and rising hollow spout, fixed lid and two-seat rear C handle';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();
 for m in mats:me.materials.append(m)
 for i,f in enumerate(me.polygons):f.material_index=g.get('face_materials',[g['material']]*len(me.polygons))[i]
 o['component_role']=g['role'];parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
bpy.context.view_layer.update();triangles=0;component_checks=[]
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-14 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-10 and deg==0,(o.name,bad,vol,deg);triangles+=len(o.data.loop_triangles)
 component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
allv=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(v[k]for v in allv)for k in range(3)];hi=[max(v[k]for v in allv)for k in range(3)];bounds=[hi[k]-lo[k]for k in range(3)]
def pbr(m):
 p=m.node_tree.nodes.get('Principled BSDF');assert p is not None
 assert not any(n.type.startswith('TEX_') for n in m.node_tree.nodes),'No procedural or image texture nodes permitted'
 assert not any(socket.is_linked for socket in p.inputs),'No linked Principled inputs permitted'
 values=[]
 for name in ['Base Color','Metallic','Roughness','Alpha','IOR','Specular IOR Level','Transmission Weight','Coat Weight','Coat Roughness','Sheen Weight','Emission Color','Emission Strength']:
  value=p.inputs[name].default_value
  values.append((name,tuple(round(float(x),6) for x in value) if hasattr(value,'__len__') else round(float(value),6)))
 values.append(('double_sided',not m.use_backface_culling));return tuple(values)
def records(objects):
 rows=[]
 for o in objects:
  o.data.calc_loop_triangles();vs=[o.matrix_world@v.co for v in o.data.vertices]
  for t in o.data.loop_triangles:
   q=[tuple(round(float(c),6) for c in vs[i]) for i in t.vertices]
   rows.append((min(tuple(q[i:]+q[:i]) for i in range(3)),pbr(o.data.materials[t.material_index])))
 return sorted(rows)
source_records=records(parts);source_fp=hashlib.sha256(json.dumps(source_records,separators=(',',':')).encode()).hexdigest()
mesh_count=len(parts);bpy.ops.object.select_all(action='DESELECT')
for o in parts+[root]:o.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
guard();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'review_mode':'SELF_REVIEW','blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'mesh_objects':mesh_count,'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,'components':component_checks,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),'status':'geometry exported; actual image self-review pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/cafe/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'cafe','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
 'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len(mats),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
# Every formal/early render is of the actual exported file imported into an emptied scene.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));parts=[o for o in scene.objects if o.type=='MESH']
assert len(parts)==mesh_count and records(parts)==source_records,'Fresh GLB oriented geometry / full solid PBR mismatch'
qa['fresh_actual_glb_guard']={'oriented_geometry_and_full_solid_pbr_match':True,'mesh_count':len(parts)};saveqa()
if '--no-render' in sys.argv or '--geometry-only' in sys.argv:
 metadata();print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)
# BEGIN AUTHORIZED TIERED RENDER V1; native has already been saved at128.
def tier_arg(flag,default=None):
 if flag not in sys.argv:return default
 i=sys.argv.index(flag);assert i+1<len(sys.argv);return sys.argv[i+1]
TIER_PROFILE=tier_arg('--render-profile')
TIER_ALLOWED={'simple-v1':(16,[16,32,64]),'complex-v1':(32,[32,64])}
TIER_SINGLE=tier_arg('--tier-single-view')
TIER_LIST=json.loads(tier_arg('--tier-view-list','[]'))
TIER_OVERRIDES=json.loads(tier_arg('--tier-sample-overrides','{}'))
TIER_STANDARD=['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe']
if TIER_PROFILE:
 assert TIER_PROFILE in TIER_ALLOWED and '--gray-only' not in sys.argv and '--gray-obliques-only' not in sys.argv
 assert isinstance(TIER_OVERRIDES,dict)
 for k,v in TIER_OVERRIDES.items():assert k in CAMERAS and k!='thumbnail' and type(v) is int and v in TIER_ALLOWED[TIER_PROFILE][1]
 assert isinstance(TIER_LIST,list) and len(TIER_LIST)==len(set(TIER_LIST)) and not(TIER_LIST and TIER_SINGLE)
 assert all(n in TIER_STANDARD[1:] and n in CAMERAS for n in TIER_LIST)
 if TIER_SINGLE:assert TIER_SINGLE in CAMERAS and TIER_SINGLE not in ['gray-front3q','gray-back3q','silhouette-128-front','silhouette-128-side']
 qa['tiered_render']={'profile_id':TIER_PROFILE,'authorization_reference':'Current separately pinned R3 operation approval; historical sample contract retained, no old approval replay.','native_samples':128,'resolution':[640,640],'gray_stage':'omitted_by_authorized_profile','samples_by_image':{}}
def tier_select_views(views):
 if not TIER_PROFILE:return views
 if TIER_SINGLE:return {TIER_SINGLE:CAMERAS[TIER_SINGLE]}
 if TIER_LIST:return {n:CAMERAS[n] for n in TIER_LIST}
 assert set(views)<=set(TIER_STANDARD)
 return views
def tier_before_view(name):
 if not TIER_PROFILE:return
 samples=128 if name=='thumbnail' else TIER_OVERRIDES.get(name,TIER_ALLOWED[TIER_PROFILE][0])
 assert samples==128 if name=='thumbnail' else samples in TIER_ALLOWED[TIER_PROFILE][1]
 scene.cycles.samples=samples
 EXPECTED['samples']=samples
 qa['tiered_render']['samples_by_image'][name+'.png']=samples
# END AUTHORIZED TIERED RENDER V1
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.30,.30,.30,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8;scene.view_settings.view_transform='AgX'
focus=Vector(FOCUS);asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3,-4,6),600,4),('Fill',(4,-2,4),360,3.5),('Rim',(2,4,5),480,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
views=tier_select_views({'thumbnail':CAMERAS['thumbnail'],'qa-front':CAMERAS['qa-front']})
seconds={};configs={}
for name,pos in views.items():
 tier_before_view(name);aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
qa.update(render_seconds=seconds,render_configs=configs,status='images rendered; maker actual-pixel self-review pending');metadata();saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
