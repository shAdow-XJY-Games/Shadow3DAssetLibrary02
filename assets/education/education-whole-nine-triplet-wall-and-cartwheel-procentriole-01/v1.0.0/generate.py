"""One wholly new nine-triplet procentriole scaffold. Static art only."""
import math,collections,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
G={}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.fm=[];self.index={}
 def vertex(self,p):
  p=tuple(round(float(x),9)for x in p)
  if p not in self.index:self.index[p]=len(self.v);self.v.append(p)
  return self.index[p]
 def tri(self,p,mat):self.f.append(tuple(self.vertex(v)for v in p));self.fm.append(mat)
 def quad(self,a,b,c,d,mat):self.tri([a,b,c],mat);self.tri([a,c,d],mat)
 def result(self,role):
  edges={}
  for i,f in enumerate(self.f):
   for a,b in zip(f,f[1:]+f[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((i,a,b))
  assert all(len(v)==2 for v in edges.values()),[(e,v)for e,v in edges.items()if len(v)!=2][:5]
  signs={0:1};todo=[0]
  while todo:
   i=todo.pop()
   for a,b in zip(self.f[i],self.f[i][1:]+self.f[i][:1]):
    for j,c,d in edges[tuple(sorted((a,b)))]:
     if i==j:continue
     want=signs[i]*(-1 if(a,b)==(c,d)else 1)
     if j in signs:assert signs[j]==want
     else:signs[j]=want;todo.append(j)
  assert len(signs)==len(self.f)
  ff=[f if signs[i]>0 else tuple(reversed(f))for i,f in enumerate(self.f)];vol=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]]))for f in ff)/6
  if vol<0:ff=[tuple(reversed(f))for f in ff]
  assert all(dot(cross(sub(self.v[f[1]],self.v[f[0]]),sub(self.v[f[2]],self.v[f[0]])),cross(sub(self.v[f[1]],self.v[f[0]]),sub(self.v[f[2]],self.v[f[0]])))>1e-18 for f in ff)
  return dict(vertices=self.v,faces=ff,face_materials=self.fm,material=0,role=role)

TRIPLET_PLAN={'points': [[0.0031, 0.0025278449], [0.0027480579, 0.0029065749], [0.0023502062, 0.003236747], [0.0019130914, 0.0035128452], [0.001444016, 0.0037302571], [0.0009508166, 0.0038853504], [0.0004417326, 0.0039755342], [-7.47311e-05, 0.0039993018], [-0.0005899462, 0.0039562562], [-0.0010953056, 0.0038471165], [-0.0015823666, 0.003673706], [-0.0020429922, 0.0034389217], [-0.0024694872, 0.0031466861], [-0.0028547263, 0.0028018811], [-0.0031922737, 0.0024102674], [-0.0034764903, 0.0019783871], [-0.0037026278, 0.0015134555], [-0.0038669084, 0.0010232397], [-0.0039665875, 0.0005159295], [-0.004, 0.0], [-0.0039665875, -0.0005159295], [-0.0038669084, -0.0010232397], [-0.0037026278, -0.0015134555], [-0.0034764903, -0.0019783871], [-0.0031922737, -0.0024102674], [-0.0028547263, -0.0028018811], [-0.0024694872, -0.0031466861], [-0.0020429922, -0.0034389217], [-0.0015823666, -0.003673706], [-0.0010953056, -0.0038471165], [-0.0005899462, -0.0039562562], [-7.47311e-05, -0.0039993018], [0.0004417326, -0.0039755342], [0.0009508166, -0.0038853504], [0.001444016, -0.0037302571], [0.0019130914, -0.0035128452], [0.0023502062, -0.003236747], [0.0027480579, -0.0029065749], [0.0031, -0.0025278449], [0.0034441939, -0.0028992297], [0.0038325488, -0.0032241549], [0.0042588416, -0.0034974139], [0.004716241, -0.0037146277], [0.0051974173, -0.0038723156], [0.0056946597, -0.0039679505], [0.0062, -0.004], [0.0067053403, -0.0039679505], [0.0072025827, -0.0038723156], [0.007683759, -0.0037146277], [0.0081411584, -0.0034974139], [0.0085674512, -0.0032241549], [0.0089558061, -0.0028992297], [0.0093, -0.0025278449], [0.0096519421, -0.0029065749], [0.0100497938, -0.003236747], [0.0104869086, -0.0035128452], [0.010955984, -0.0037302571], [0.0114491834, -0.0038853504], [0.0119582674, -0.0039755342], [0.0124747311, -0.0039993018], [0.0129899462, -0.0039562562], [0.0134953056, -0.0038471165], [0.0139823666, -0.003673706], [0.0144429922, -0.0034389217], [0.0148694872, -0.0031466861], [0.0152547263, -0.0028018811], [0.0155922737, -0.0024102674], [0.0158764903, -0.0019783871], [0.0161026278, -0.0015134555], [0.0162669084, -0.0010232397], [0.0163665875, -0.0005159295], [0.0164, -0.0], [0.0163665875, 0.0005159295], [0.0162669084, 0.0010232397], [0.0161026278, 0.0015134555], [0.0158764903, 0.0019783871], [0.0155922737, 0.0024102674], [0.0152547263, 0.0028018811], [0.0148694872, 0.0031466861], [0.0144429922, 0.0034389217], [0.0139823666, 0.003673706], [0.0134953056, 0.0038471165], [0.0129899462, 0.0039562562], [0.0124747311, 0.0039993018], [0.0119582674, 0.0039755342], [0.0114491834, 0.0038853504], [0.010955984, 0.0037302571], [0.0104869086, 0.0035128452], [0.0100497938, 0.003236747], [0.0096519421, 0.0029065749], [0.0093, 0.0025278449], [0.0089558061, 0.0028992297], [0.0085674512, 0.0032241549], [0.0081411584, 0.0034974139], [0.007683759, 0.0037146277], [0.0072025827, 0.0038723156], [0.0067053403, 0.0039679505], [0.0062, 0.004], [0.0056946597, 0.0039679505], [0.0051974173, 0.0038723156], [0.004716241, 0.0037146277], [0.0042588416, 0.0034974139], [0.0038325488, 0.0032241549], [0.0034441939, 0.0028992297], [0.0025, -0.0], [0.0024692209, -0.0003910862], [0.0023776413, -0.0007725425], [0.0022275163, -0.0011349762], [0.0020225425, -0.0014694631], [0.001767767, -0.001767767], [0.0014694631, -0.0020225425], [0.0011349762, -0.0022275163], [0.0007725425, -0.0023776413], [0.0003910862, -0.0024692209], [0.0, -0.0025], [-0.0003910862, -0.0024692209], [-0.0007725425, -0.0023776413], [-0.0011349762, -0.0022275163], [-0.0014694631, -0.0020225425], [-0.001767767, -0.001767767], [-0.0020225425, -0.0014694631], [-0.0022275163, -0.0011349762], [-0.0023776413, -0.0007725425], [-0.0024692209, -0.0003910862], [-0.0025, -0.0], [-0.0024692209, 0.0003910862], [-0.0023776413, 0.0007725425], [-0.0022275163, 0.0011349762], [-0.0020225425, 0.0014694631], [-0.001767767, 0.001767767], [-0.0014694631, 0.0020225425], [-0.0011349762, 0.0022275163], [-0.0007725425, 0.0023776413], [-0.0003910862, 0.0024692209], [-0.0, 0.0025], [0.0003910862, 0.0024692209], [0.0007725425, 0.0023776413], [0.0011349762, 0.0022275163], [0.0014694631, 0.0020225425], [0.001767767, 0.001767767], [0.0020225425, 0.0014694631], [0.0022275163, 0.0011349762], [0.0023776413, 0.0007725425], [0.0024692209, 0.0003910862], [0.0087, -0.0], [0.0086692209, -0.0003910862], [0.0085776413, -0.0007725425], [0.0084275163, -0.0011349762], [0.0082225425, -0.0014694631], [0.007967767, -0.001767767], [0.0076694631, -0.0020225425], [0.0073349762, -0.0022275163], [0.0069725425, -0.0023776413], [0.0065910862, -0.0024692209], [0.0062, -0.0025], [0.0058089138, -0.0024692209], [0.0054274575, -0.0023776413], [0.0050650238, -0.0022275163], [0.0047305369, -0.0020225425], [0.004432233, -0.001767767], [0.0041774575, -0.0014694631], [0.0039724837, -0.0011349762], [0.0038223587, -0.0007725425], [0.0037307791, -0.0003910862], [0.0037, -0.0], [0.0037307791, 0.0003910862], [0.0038223587, 0.0007725425], [0.0039724837, 0.0011349762], [0.0041774575, 0.0014694631], [0.004432233, 0.001767767], [0.0047305369, 0.0020225425], [0.0050650238, 0.0022275163], [0.0054274575, 0.0023776413], [0.0058089138, 0.0024692209], [0.0062, 0.0025], [0.0065910862, 0.0024692209], [0.0069725425, 0.0023776413], [0.0073349762, 0.0022275163], [0.0076694631, 0.0020225425], [0.007967767, 0.001767767], [0.0082225425, 0.0014694631], [0.0084275163, 0.0011349762], [0.0085776413, 0.0007725425], [0.0086692209, 0.0003910862], [0.0149, -0.0], [0.0148692209, -0.0003910862], [0.0147776413, -0.0007725425], [0.0146275163, -0.0011349762], [0.0144225425, -0.0014694631], [0.014167767, -0.001767767], [0.0138694631, -0.0020225425], [0.0135349762, -0.0022275163], [0.0131725425, -0.0023776413], [0.0127910862, -0.0024692209], [0.0124, -0.0025], [0.0120089138, -0.0024692209], [0.0116274575, -0.0023776413], [0.0112650238, -0.0022275163], [0.0109305369, -0.0020225425], [0.010632233, -0.001767767], [0.0103774575, -0.0014694631], [0.0101724837, -0.0011349762], [0.0100223587, -0.0007725425], [0.0099307791, -0.0003910862], [0.0099, -0.0], [0.0099307791, 0.0003910862], [0.0100223587, 0.0007725425], [0.0101724837, 0.0011349762], [0.0103774575, 0.0014694631], [0.010632233, 0.001767767], [0.0109305369, 0.0020225425], [0.0112650238, 0.0022275163], [0.0116274575, 0.0023776413], [0.0120089138, 0.0024692209], [0.0124, 0.0025], [0.0127910862, 0.0024692209], [0.0131725425, 0.0023776413], [0.0135349762, 0.0022275163], [0.0138694631, 0.0020225425], [0.014167767, 0.001767767], [0.0144225425, 0.0014694631], [0.0146275163, 0.0011349762], [0.0147776413, 0.0007725425], [0.0148692209, 0.0003910862]], 'faces': [[154, 44, 45], [46, 154, 45], [27, 118, 26], [130, 11, 12], [46, 153, 154], [153, 46, 47], [171, 101, 170], [141, 167, 0], [94, 95, 176], [95, 175, 176], [33, 34, 112], [115, 30, 31], [30, 115, 29], [70, 185, 69], [4, 5, 136], [8, 133, 7], [133, 8, 9], [110, 111, 35], [111, 34, 35], [34, 111, 112], [109, 37, 38], [37, 109, 110], [152, 153, 47], [48, 152, 47], [152, 48, 151], [195, 58, 194], [195, 57, 58], [57, 195, 196], [103, 169, 170], [169, 103, 0], [42, 157, 41], [137, 138, 3], [4, 137, 3], [137, 4, 136], [1, 139, 0], [139, 1, 138], [101, 102, 170], [102, 103, 170], [96, 175, 95], [174, 96, 97], [96, 174, 175], [65, 189, 64], [189, 65, 66], [58, 59, 194], [59, 193, 194], [113, 33, 112], [113, 32, 33], [219, 77, 78], [77, 219, 76], [83, 84, 214], [215, 83, 214], [88, 210, 87], [84, 213, 214], [85, 213, 84], [213, 85, 212], [171, 100, 101], [5, 135, 136], [6, 135, 5], [117, 27, 28], [117, 118, 27], [36, 110, 35], [36, 37, 110], [107, 108, 38], [108, 109, 38], [48, 49, 151], [49, 150, 151], [150, 49, 50], [201, 52, 200], [52, 199, 200], [172, 100, 171], [56, 57, 196], [56, 197, 55], [197, 56, 196], [167, 168, 0], [168, 169, 0], [161, 107, 38], [158, 40, 41], [157, 158, 41], [155, 44, 154], [11, 131, 10], [130, 131, 11], [138, 2, 3], [1, 2, 138], [140, 141, 0], [139, 140, 0], [177, 94, 176], [177, 93, 94], [93, 177, 178], [178, 179, 91], [179, 90, 91], [90, 179, 180], [190, 63, 64], [189, 190, 64], [67, 188, 66], [188, 189, 66], [60, 61, 193], [59, 60, 193], [20, 21, 123], [25, 119, 24], [118, 119, 26], [119, 25, 26], [23, 121, 22], [79, 218, 78], [218, 219, 78], [220, 75, 76], [219, 220, 76], [81, 82, 215], [82, 83, 215], [210, 211, 87], [85, 86, 212], [211, 86, 87], [86, 211, 212], [89, 90, 209], [210, 89, 209], [89, 210, 88], [98, 174, 97], [174, 98, 173], [172, 99, 100], [99, 172, 173], [98, 99, 173], [129, 13, 14], [129, 130, 12], [13, 129, 12], [126, 127, 16], [17, 126, 16], [125, 17, 18], [17, 125, 126], [114, 115, 31], [32, 114, 31], [113, 114, 32], [197, 198, 55], [198, 54, 55], [51, 52, 149], [51, 150, 50], [150, 51, 149], [52, 148, 149], [158, 39, 40], [39, 159, 38], [159, 39, 158], [156, 157, 42], [133, 134, 7], [134, 6, 7], [134, 135, 6], [181, 90, 180], [181, 207, 90], [92, 178, 91], [92, 93, 178], [63, 191, 62], [190, 191, 63], [187, 67, 68], [187, 188, 67], [21, 122, 123], [121, 122, 22], [122, 21, 22], [119, 120, 24], [120, 23, 24], [23, 120, 121], [217, 79, 80], [217, 218, 79], [75, 221, 74], [220, 221, 75], [90, 208, 209], [207, 208, 90], [127, 15, 16], [128, 129, 14], [15, 128, 14], [128, 15, 127], [115, 116, 29], [29, 116, 28], [116, 117, 28], [52, 53, 199], [198, 53, 54], [53, 198, 199], [160, 161, 38], [159, 160, 38], [155, 43, 44], [156, 43, 155], [43, 156, 42], [132, 133, 9], [132, 9, 10], [131, 132, 10], [147, 148, 52], [147, 52, 201], [192, 61, 62], [191, 192, 62], [61, 192, 193], [69, 186, 68], [186, 187, 68], [185, 186, 69], [20, 124, 19], [124, 20, 123], [124, 18, 19], [124, 125, 18], [81, 216, 80], [216, 217, 80], [216, 81, 215], [222, 73, 74], [221, 222, 74], [223, 72, 73], [222, 223, 73], [184, 70, 71], [184, 185, 70], [72, 184, 71], [223, 184, 72], [106, 163, 105], [163, 106, 162], [163, 164, 104], [105, 163, 104], [106, 161, 162], [161, 106, 107], [203, 145, 202], [202, 145, 146], [144, 145, 204], [145, 203, 204], [205, 144, 204], [205, 183, 144], [205, 206, 182], [183, 205, 182], [164, 165, 104], [165, 143, 104], [206, 181, 182], [207, 181, 206], [142, 166, 141], [141, 166, 167], [165, 166, 143], [166, 142, 143], [147, 202, 146], [147, 201, 202]], 'loop_lengths': [104, 40, 40, 40], 'outer_radius': 0.004, 'lumen_radius': 0.0025, 'centre_spacing': 0.0062, 'cap_triangles': 228}
# New complete short procentriole scaffold: nine shared-wall three-lumen blades.
G={};JOINTS=[];LUMEN_CENTRES=[];BLADES=[];CENTRES=[]
def transform(u,v,a,z):
 t=a+math.radians(70);return(.046*math.cos(a)+u*math.cos(t)-v*math.sin(t),.046*math.sin(a)+u*math.sin(t)+v*math.cos(t),z)
for i in range(9):
 a=math.tau*i/9;name='WholeSharedWallTripletBlade_%02d'%(i+1);m=Mesh();ps=TRIPLET_PLAN['points'];lower=[transform(u,v,a,0)for u,v in ps];upper=[transform(u,v,a,.095)for u,v in ps]
 for face in TRIPLET_PLAN['faces']:
  u=sum(ps[j][0]for j in face)/3;mat=min(2,max(0,round(u/.0062)))
  m.tri([lower[j]for j in face],mat);m.tri([upper[j]for j in face],mat)
 start=0
 for li,length in enumerate(TRIPLET_PLAN['loop_lengths']):
  for j in range(length):
   k=start+j;n=start+(j+1)%length;mat=li-1 if li else min(2,max(0,round((ps[k][0]+ps[n][0])/2/.0062)))
   m.quad(lower[k],lower[n],upper[n],upper[k],mat)
  start+=length
 G[name]=m.result('One complete connected triplet blade with three true axial lumens and continuous shared solid septa. The outer three-lobed contour is fused, not three independent complete pipes. Uniform smooth channel walls stand for compound microtubules; individual protofilaments and molecular junctions are not represented.');BLADES.append(name);CENTRES.append([transform(k*.0062,0,a,0)for k in range(3)]);LUMEN_CENTRES.extend([transform(k*.0062,0,a,.070)for k in range(3)])
HUB='WholeProximalCartwheelHub';m=Mesh();N=36;profile=[(.013,.020),(.013,.040),(.007,.040),(.007,.020)]
rows=[[(r*math.cos(math.tau*j/N),r*math.sin(math.tau*j/N),z)for j in range(N)]for r,z in profile]
for i,a in enumerate(rows):
 b=rows[(i+1)%len(rows)]
 for j in range(N):k=(j+1)%N;m.quad(a[j],a[k],b[k],b[j],3)
G[HUB]=m.result('One full hollow proximal cartwheel hub representation connected through nine whole spokes to the A-side walls. One thick schematic hub stands for the short stacked proximal assembly, not literal molecular dimensions or protein count.')
def bar(name,a,b,width,z0,z1,role):
 dx=b[0]-a[0];dy=b[1]-a[1];ll=math.hypot(dx,dy);ux=-dy/ll*width/2;uy=dx/ll*width/2
 base=[(a[0]+ux,a[1]+uy,z0),(b[0]+ux,b[1]+uy,z0),(b[0]-ux,b[1]-uy,z0),(a[0]-ux,a[1]-uy,z0)];top=[(x,y,z1)for x,y,z in base];m=Mesh();m.quad(*base,3);m.quad(*top,3)
 for j in range(4):k=(j+1)%4;m.quad(base[j],base[k],top[k],top[j],3)
 G[name]=m.result(role+' Complete closed finite-thickness schematic connector, rooted at both ends; no molecular, mechanical or strength claim.')
for i in range(9):
 a=math.tau*i/9;co,si=math.cos(a),math.sin(a);name='WholeCartwheelSpoke_%02d'%(i+1);bar(name,(.0105*co,.0105*si),(.0431*co,.0431*si),.0020,.028,.034,'One full proximal spoke from central hub to the A-side wall of one whole triplet blade.')
 JOINTS.extend([(HUB,name,(.0115*co,.0115*si,.031)),(BLADES[i],name,(.0428*co,.0428*si,.031))])
 c=CENTRES[i][2];b=CENTRES[(i+1)%9][0];dx=b[0]-c[0];dy=b[1]-c[1];ll=math.hypot(dx,dy);u=(dx/ll,dy/ll);p=(c[0]+.0032*u[0],c[1]+.0032*u[1]);q=(b[0]-.0032*u[0],b[1]-.0032*u[1]);name='WholeAdjacentBladeLink_%02d'%(i+1)
 bar(name,(p[0]-.0003*u[0],p[1]-.0003*u[1]),(q[0]+.0003*u[0],q[1]+.0003*u[1]),.0015,.012,.016,'One full low schematic A-to-C connector between adjacent whole blades, separated vertically from the cartwheel spokes.')
 JOINTS.extend([(BLADES[i],name,(p[0],p[1],.014)),(BLADES[(i+1)%9],name,(q[0],q[1],.014))])
BODY=BLADES[0];v=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[k]for p in v)+max(p[k]for p in v))/2 if k<2 else-min(p[2]for p in v)for k in range(3))
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
JOINTS=[(a,b,add(p,SHIFT))for a,b,p in JOINTS];LUMEN_CENTRES=[add(p,SHIFT)for p in LUMEN_CENTRES];EXPECTED_TRIANGLES=sum(len(g['faces'])for g in G.values());EXPECTED_MESHES=len(G)
ASSET='education-whole-nine-triplet-wall-and-cartwheel-procentriole-01';VERSION='1.0.0';TITLE='Whole Nine Triplet Wall and Cartwheel Procentriole'
DESCRIPTION='One wholly newly authored enlarged schematic short procentriole scaffold. Nine complete longitudinal compound blades form a ninefold barrel around a hollow centre; every blade has a continuous three-lobed outer wall, three genuine open axial channels and shared solid septa rather than three detached full pipes. One whole hollow proximal hub connects through nine complete radial spokes to the A-side walls, while nine lower A-to-C link representations join adjacent blades. All numeric cross-sections, positions, wall topology and connectors are new; no chloroplast envelope, granum stack, fruit shell, wheel, pipe bundle or old cell geometry is reused. One complete teaching prop and zero scenes, twenty-eight closed editable components, four opaque diagram PBR roles, roughly twelve centimetres wide rather than biological life size. The short equal-length triplet walls depict an intentionally simplified developing scaffold, not a mature appendage-bearing centriole, a distal doublet transition, a whole centrosome or cell. Three smooth channels and thick shared septa are topology-level teaching approximations, not accurate protofilament geometry, protein identities, molecular counts, species, cell-cycle timing, living function, force, clinical or medical assertions. Flat blade ends are a display datum; no physical-stability claim. No labels, textures, rig, animation or interaction.'
PALETTE=[('ATubuleRole_MutedTeal',(.13,.37,.31,1),.80,0.),('BTubuleRole_QuietBlue',(.16,.31,.44,1),.82,0.),('CTubuleRole_DeepBlue',(.10,.22,.34,1),.84,0.),('CartwheelAndLinks_WarmOchre',(.55,.30,.11,1),.83,0.)]
FOCUS=(0,0,.047);CAMERAS={'thumbnail':(.60,-1.2,2.7),'qa-front':(.60,-1.2,2.7),'qa-side':(1.5,-.2,.7),'qa-top':(0,0,2),'qa-back':(-.60,1.2,2.7),'qa-wireframe':(.60,-1.2,2.7)}
ORTHO=.170;WIRE_THICKNESS=.00006

# BLENDER PHASE: mature export/render only.
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
root=bpy.data.objects.new('OneWholeShortProcentrioleScaffold',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='finite full blade ends; enlarged short procentriole scaffold';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();
 for m in mats:me.materials.append(m)
 for i,f in enumerate(me.polygons):f.material_index=g.get('face_materials',[g['material']]*len(me.polygons))[i]
 o['component_role']=g['role'];parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={};actual_triangles={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg);triangles+=len(o.data.loop_triangles)
 component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i]for p in v)for i in range(3)];hi=[max(p[i]for p in v)for i in range(3)];bounds=[round(hi[i]-lo[i],6)for i in range(3)]
assert abs(lo[2])<1e-7 and triangles==EXPECTED_TRIANGLES and len(parts)==EXPECTED_MESHES
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
# Count the material list in the actual exported GLB, not a copied literal.
import struct
_glb=(OUT/'model.glb').read_bytes();_json_length,_json_kind=struct.unpack_from('<II',_glb,12);assert _json_kind==0x4e4f534a
actual_material_count=len(json.loads(_glb[20:20+_json_length])['materials'])
assert actual_material_count==len({f.material_index for o in parts for f in o.data.polygons})
guard();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':actual_material_count,'mesh_objects':mesh_count,'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,'components':component_checks,'single_prop_count':1,'review_mode':'SELF_REVIEW','static_visual_only':True,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),'status':'producer geometry; maker actual-image acceptance pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/education/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'education','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
 'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':actual_material_count,'files':files,'status':'review','license':'All rights reserved'}
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
 qa['tiered_render']={'profile_id':TIER_PROFILE,'authorization_reference':'Sentinel_f2fcc66115e881918d02bc1ea780953c','native_samples':128,'resolution':[640,640],'gray_stage':'omitted_by_authorized_profile','samples_by_image':{}}
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
def diagnostic_snapshot():
 return {m:[(i,socket.identifier,socket.bl_idname,tuple(socket.default_value) if hasattr(socket.default_value,'__len__') else socket.default_value) for i,socket in enumerate(m.node_tree.nodes.get('Principled BSDF').inputs) if hasattr(socket,'default_value')] for m in asset_mats}
original_material_inputs=diagnostic_snapshot()
original_slots={o:(list(o.data.materials),[f.material_index for f in o.data.polygons]) for o in parts}
def restore_diagnostic_materials():
 for m,inputs in original_material_inputs.items():
  p=m.node_tree.nodes.get('Principled BSDF')
  for index,identifier,socket_type,value in inputs:
   assert index<len(p.inputs),'Diagnostic socket index disappeared'
   socket=p.inputs[index]
   assert socket.identifier==identifier and socket.bl_idname==socket_type,'Diagnostic socket identity/type changed'
   socket.default_value=value
 for o,(slots,indices) in original_slots.items():
  assert len(o.data.polygons)==len(indices),'Diagnostic face count changed'
  o.data.materials.clear()
  for m in slots:o.data.materials.append(m)
  for f,index in zip(o.data.polygons,indices):f.material_index=index
  assert list(o.data.materials)==slots and [f.material_index for f in o.data.polygons]==indices
 assert diagnostic_snapshot()==original_material_inputs,'Diagnostic full socket-index/identifier/type/value restoration differs'
 assert records(parts)==source_records,'Diagnostic restoration changed complete oriented geometry/full solid PBR signature'
 qa['diagnostic_exact_restoration']={'try_finally':True,'full_socket_index_identifier_type_value_match':True,'all_material_slots_and_face_indices_match':True,'full_oriented_geometry_and_pbr_records_match':True}
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
try:
 if gray:
  for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
 views={k:CAMERAS[k] for k in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
 if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
 if '--extra-views' in sys.argv:views.pop('thumbnail',None)
 views=tier_select_views(views)
 seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
 def render(name,pos):
  tier_before_view(name)
  ground.hide_render=(name=='qa-side')
  cam.data.ortho_scale=ORTHO
  aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
 for name,pos in views.items():
  if name=='qa-wireframe':
   wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
   for o in parts:
    dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
    for f in dup.data.polygons:f.material_index=0
    w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=WIRE_THICKNESS;w.use_replace=True;w.use_even_offset=False;w.offset=1
  render(name,pos)
 if gray and '--gray-obliques-only' not in sys.argv:
  black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
  for o in parts:
   o.data.materials.clear();o.data.materials.append(black)
   for f in o.data.polygons:f.material_index=0
  ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
  scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
  for name,pos in [(name,CAMERAS[name]) for name in ['silhouette-128-front','silhouette-128-side']]:render(name,pos)
finally:
 restore_diagnostic_materials()
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; maker necessary-view self-review pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
