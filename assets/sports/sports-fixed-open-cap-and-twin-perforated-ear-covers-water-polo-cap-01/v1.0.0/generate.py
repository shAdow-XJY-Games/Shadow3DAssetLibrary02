'One newly authored complete fixed water-polo-cap-inspired empty display: a thin continuous blue domed cap shell with a completely open underside and two bounded side apertures, two whole curved pale ear-cover shells each with seven genuine bounded perforations, and two complete narrow forward-laid chin ties. Each ear cover follows the cap curvature and has real thickness, a closed outer rim and fourteen total actual open bores; the fabric-like dome is not a thick helmet, face cage or chin cup. All five complete component meshes and numeric geometry are newly authored, not removed helmet parts or copied pads. Intentional small positive-volume rim and tie seats keep the fixed empty assembly rooted to the finite flat lower shell hem and tie facets. Five closed whole meshes, three opaque constant untextured PBR roles, metres native Z up and full horizontal bounds-centred grounded origin. One original static model zero scenes. No person, wearer, fit, softness simulation, protection, safe use, impact resistance, breathing or hearing capability, regulation, certification, manufacturing specification, animation or interaction. Simplified faceted static game prop only.'
import base64,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ASSET='sports-fixed-open-cap-and-twin-perforated-ear-covers-water-polo-cap-01'
TITLE='Open Cap And Twin Perforated Ear Covers Water Polo Cap'
TOL=2e-7
INPUTS={}
SOURCE_INPUTS={}
PALETTE=[('WholeThinCapShell_MutedBlue',(.075,.22,.38,1),.89),('WholePerforatedEarCovers_WarmPale',(.70,.73,.69,1),.69),('WholeChinTies_PaleGrey',(.48,.53,.55,1),.9)]
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
def runner_prism(name,p,z0,z1,m,transform):
 if sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1]for i in range(len(p)))<0:p=list(reversed(p))
 n=len(p);cap=earclip(p);v=[transform((x,y,z))for z in[z0,z1]for x,y in p]
 f=[tuple(reversed(t))for t in cap]+[tuple(i+n for i in t)for t in cap]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)]
 record(name,v,f,m)
def tube3(name,path,r,m,n=6):
 vs=[]
 for j,p in enumerate(path):
  a=path[max(0,j-1)];b=path[min(len(path)-1,j+1)];w=[b[k]-a[k]for k in range(3)];le=math.sqrt(sum(x*x for x in w));w=[x/le for x in w];seed=(0,0,1)if abs(w[2])<.9 else(1,0,0);u=[w[1]*seed[2]-w[2]*seed[1],w[2]*seed[0]-w[0]*seed[2],w[0]*seed[1]-w[1]*seed[0]];le=math.sqrt(sum(x*x for x in u));u=[x/le for x in u];v=[w[1]*u[2]-w[2]*u[1],w[2]*u[0]-w[0]*u[2],w[0]*u[1]-w[1]*u[0]]
  for i in range(n):vs.append(tuple(p[k]+r*(u[k]*math.cos(i*math.tau/n)+v[k]*math.sin(i*math.tau/n))for k in range(3)))
 fs=[tuple(reversed(range(n))),tuple((len(path)-1)*n+i for i in range(n))]+[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i)for j in range(len(path)-1)for i in range(n)];record(name,vs,fs,m)
EAR_POINTS=[(0.034, 0.0), (0.03370912528670956, 0.0044378905354817534), (0.03284147809382833, 0.008799847533485707), (0.031411904105383755, 0.013011236700413053), (0.029444863728670917, 0.016999999999999998), (0.026974013569902, 0.020697888586296505), (0.02404163056034262, 0.024041630560342614), (0.020697888586296505, 0.026974013569902), (0.017000000000000005, 0.029444863728670913), (0.013011236700413055, 0.031411904105383755), (0.008799847533485707, 0.03284147809382833), (0.004437890535481759, 0.03370912528670956), (2.0818995585505005e-18, 0.034), (-0.004437890535481755, 0.03370912528670956), (-0.008799847533485701, 0.03284147809382833), (-0.013011236700413044, 0.031411904105383755), (-0.016999999999999994, 0.029444863728670917), (-0.020697888586296505, 0.026974013569902), (-0.024041630560342614, 0.02404163056034262), (-0.026974013569901995, 0.020697888586296512), (-0.029444863728670917, 0.016999999999999998), (-0.031411904105383755, 0.013011236700413058), (-0.03284147809382832, 0.008799847533485715), (-0.03370912528670956, 0.004437890535481768), (-0.034, 4.163799117101001e-18), (-0.03370912528670956, -0.00443789053548176), (-0.03284147809382833, -0.008799847533485708), (-0.031411904105383755, -0.01301123670041305), (-0.02944486372867092, -0.01699999999999999), (-0.026974013569902, -0.020697888586296505), (-0.02404163056034263, -0.024041630560342604), (-0.020697888586296512, -0.02697401356990199), (-0.017000000000000015, -0.029444863728670907), (-0.013011236700413044, -0.031411904105383755), (-0.008799847533485701, -0.03284147809382833), (-0.004437890535481756, -0.03370912528670956), (-6.2456986756515014e-18, -0.034), (0.004437890535481743, -0.03370912528670956), (0.008799847533485691, -0.03284147809382833), (0.013011236700413032, -0.03141190410538376), (0.017000000000000005, -0.029444863728670913), (0.020697888586296478, -0.026974013569902016), (0.02404163056034261, -0.024041630560342624), (0.02697401356990199, -0.020697888586296512), (0.029444863728670907, -0.017000000000000015), (0.031411904105383755, -0.013011236700413046), (0.03284147809382832, -0.008799847533485734), (0.03370912528670956, -0.004437890535481758), (0.0036, 0.0), (0.0031176914536239792, 0.0017999999999999997), (0.0018000000000000004, 0.003117691453623979), (2.2043642384652355e-19, 0.0036), (-0.001799999999999999, 0.0031176914536239792), (-0.0031176914536239792, 0.0017999999999999997), (-0.0036, 4.408728476930471e-19), (-0.0031176914536239797, -0.0017999999999999989), (-0.0018000000000000015, -0.003117691453623978), (-6.613092715395707e-19, -0.0036), (0.0018000000000000004, -0.003117691453623979), (0.003117691453623978, -0.0018000000000000015), (0.0176, 0.0), (0.01711769145362398, 0.0017999999999999997), (0.0158, 0.003117691453623979), (0.014, 0.0036), (0.0122, 0.0031176914536239792), (0.010882308546376021, 0.0017999999999999997), (0.0104, 4.408728476930471e-19), (0.010882308546376021, -0.0017999999999999989), (0.012199999999999999, -0.003117691453623978), (0.014, -0.0036), (0.0158, -0.003117691453623979), (0.01711769145362398, -0.0018000000000000015), (0.010600000000000002, 0.01212435565298214), (0.01011769145362398, 0.01392435565298214), (0.008800000000000002, 0.01524204710660612), (0.007000000000000002, 0.01572435565298214), (0.005200000000000003, 0.01524204710660612), (0.0038823085463760227, 0.01392435565298214), (0.003400000000000002, 0.01212435565298214), (0.0038823085463760222, 0.010324355652982141), (0.005200000000000001, 0.009006664199358163), (0.007000000000000001, 0.008524355652982141), (0.008800000000000002, 0.009006664199358161), (0.01011769145362398, 0.01032435565298214), (-0.0033999999999999968, 0.012124355652982142), (-0.0038823085463760175, 0.013924355652982142), (-0.005199999999999996, 0.015242047106606121), (-0.006999999999999997, 0.015724355652982143), (-0.008799999999999995, 0.015242047106606121), (-0.010117691453623977, 0.013924355652982142), (-0.010599999999999997, 0.012124355652982142), (-0.010117691453623977, 0.010324355652982143), (-0.008799999999999999, 0.009006664199358165), (-0.0069999999999999975, 0.008524355652982141), (-0.005199999999999996, 0.009006664199358163), (-0.0038823085463760188, 0.010324355652982141), (-0.0104, 1.7145055188062945e-18), (-0.010882308546376021, 0.0018000000000000015), (-0.012199999999999999, 0.0031176914536239805), (-0.014, 0.0036000000000000016), (-0.015799999999999998, 0.003117691453623981), (-0.01711769145362398, 0.0018000000000000015), (-0.0176, 2.1553783664993416e-18), (-0.01711769145362398, -0.0017999999999999971), (-0.0158, -0.003117691453623976), (-0.014, -0.003599999999999998), (-0.012199999999999999, -0.003117691453623977), (-0.010882308546376023, -0.0017999999999999997), (-0.0034000000000000063, -0.012124355652982137), (-0.003882308546376027, -0.010324355652982137), (-0.005200000000000006, -0.009006664199358158), (-0.007000000000000006, -0.008524355652982138), (-0.008800000000000006, -0.009006664199358158), (-0.010117691453623985, -0.010324355652982137), (-0.010600000000000005, -0.012124355652982137), (-0.010117691453623985, -0.013924355652982136), (-0.008800000000000007, -0.015242047106606114), (-0.007000000000000007, -0.015724355652982136), (-0.005200000000000006, -0.015242047106606116), (-0.0038823085463760283, -0.013924355652982138), (0.010600000000000002, -0.01212435565298214), (0.01011769145362398, -0.010324355652982141), (0.008800000000000002, -0.009006664199358161), (0.007000000000000002, -0.008524355652982141), (0.005200000000000003, -0.009006664199358161), (0.0038823085463760227, -0.010324355652982141), (0.003400000000000002, -0.01212435565298214), (0.0038823085463760222, -0.01392435565298214), (0.005200000000000001, -0.015242047106606118), (0.007000000000000001, -0.01572435565298214), (0.008800000000000002, -0.01524204710660612), (0.01011769145362398, -0.013924355652982142)]
EAR_TRIANGLES=[[128, 118, 36], [28, 104, 27], [40, 130, 39], [6, 7, 73], [60, 47, 0], [1, 60, 0], [30, 31, 115], [116, 32, 33], [116, 31, 32], [31, 116, 115], [118, 35, 36], [111, 55, 107], [102, 23, 24], [89, 17, 18], [19, 89, 18], [100, 20, 21], [16, 88, 15], [88, 87, 15], [17, 88, 16], [88, 17, 89], [25, 102, 24], [103, 25, 26], [25, 103, 102], [103, 26, 27], [104, 103, 27], [29, 30, 115], [41, 42, 131], [130, 41, 131], [41, 130, 40], [37, 128, 36], [129, 38, 39], [130, 129, 39], [129, 37, 38], [37, 129, 128], [42, 43, 131], [70, 44, 45], [5, 6, 73], [4, 62, 3], [34, 117, 33], [117, 116, 33], [35, 117, 34], [117, 35, 118], [90, 19, 20], [19, 90, 89], [100, 90, 20], [22, 101, 21], [101, 100, 21], [23, 101, 22], [101, 23, 102], [87, 14, 15], [13, 14, 87], [86, 76, 12], [13, 86, 12], [86, 13, 87], [76, 11, 12], [10, 75, 9], [11, 75, 10], [75, 11, 76], [29, 114, 28], [114, 29, 115], [28, 114, 104], [120, 43, 44], [43, 120, 131], [70, 120, 44], [46, 71, 45], [71, 70, 45], [71, 46, 47], [71, 47, 60], [5, 72, 4], [72, 5, 73], [72, 62, 4], [61, 2, 3], [62, 61, 3], [2, 61, 1], [1, 61, 60], [59, 123, 67], [97, 53, 93], [74, 8, 9], [75, 74, 9], [7, 74, 73], [8, 74, 7], [57, 109, 125], [65, 81, 49], [95, 51, 79], [55, 96, 107], [96, 55, 54], [122, 68, 67], [123, 122, 67], [92, 97, 93], [97, 92, 98], [110, 56, 111], [56, 55, 111], [106, 112, 107], [112, 111, 107], [105, 114, 113], [114, 105, 104], [112, 105, 113], [105, 112, 106], [78, 95, 79], [95, 78, 84], [53, 96, 54], [53, 97, 96], [127, 119, 128], [128, 119, 118], [65, 48, 66], [48, 65, 49], [66, 48, 67], [48, 59, 67], [94, 53, 52], [53, 94, 93], [92, 91, 98], [91, 99, 98], [99, 91, 100], [91, 90, 100], [122, 69, 68], [121, 69, 122], [69, 121, 120], [69, 120, 70], [63, 83, 64], [83, 82, 64], [83, 63, 62], [72, 83, 62], [57, 56, 110], [109, 57, 110], [81, 50, 49], [50, 81, 80], [81, 65, 64], [82, 81, 64], [51, 94, 52], [94, 51, 95], [51, 80, 79], [51, 50, 80], [85, 77, 86], [86, 77, 76], [78, 77, 84], [77, 85, 84], [126, 119, 127], [126, 108, 119], [108, 126, 109], [109, 126, 125], [58, 124, 123], [59, 58, 123], [124, 58, 125], [58, 57, 125]]
def cap_shell():
 N=48;heights=[.01*i for i in range(12)]+[.118];v=[]
 for inner in[False,True]:
  rx,ry,h=(.089,.109,.117)if inner else(.092,.112,.12)
  for z in heights:
   phi=math.asin(z/.12)
   for j in range(N):v.append((rx*math.cos(phi)*math.cos(math.tau*j/N),ry*math.cos(phi)*math.sin(math.tau*j/N),h*math.sin(phi)))
  v.append((0,0,h))
 L=len(heights)*N+1;surf=[]
 for i in range(len(heights)-1):
  for j in range(N):
   if (3<=i<5 and j in[0,1,46,47,22,23,24,25])or(i in[1,2,5,6]and j in[0,47,23,24]):continue
   surf.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
 for j in range(N):surf.append(((len(heights)-1)*N+j,(len(heights)-1)*N+(j+1)%N,L-1))
 edges={}
 for f in surf:
  for x,y in zip(f,f[1:]+f[:1]):
   k=tuple(sorted((x,y)))
   if k in edges:del edges[k]
   else:edges[k]=(x,y)
 fs=surf+[tuple(i+L for i in reversed(f))for f in surf]+[(y,x,x+L,y+L)for x,y in edges.values()]
 record('WholeThinOpenDomeWithTwoSideApertures',v,fs,0)
def ear_cover(side):
 v=[]
 for outer in[False,True]:
  for y,dz in EAR_POINTS:
   z=.04+dz;r=math.hypot(y,dz);x=.092*math.sqrt(1-(y/.112)**2-(z/.12)**2)
   x+=.0025+.005*(1-r/.034)**2 if outer else -.0017
   v.append((side*x,y,z))
 n=len(EAR_POINTS);fs=[tuple(reversed(t))for t in EAR_TRIANGLES]+[tuple(i+n for i in t)for t in EAR_TRIANGLES];edges={}
 for f in EAR_TRIANGLES:
  for x,y in zip(f,f[1:]+f[:1]):
   k=tuple(sorted((x,y)))
   if k in edges:del edges[k]
   else:edges[k]=(x,y)
 fs +=[(x,y,y+n,x+n)for x,y in edges.values()];record('Whole'+('Left'if side<0 else'Right')+'SevenHoleEarCover',v,fs,1)
def flat_tie(side):
 path=[(side*.0644,-.0784,.019),(side*.066,-.092,.006),(side*.060,-.13,.001),(side*.029,-.178,.001)];v=[]
 for i,p in enumerate(path):
  a=path[max(0,i-1)];b=path[min(len(path)-1,i+1)];d=(b[0]-a[0],b[1]-a[1]);le=math.hypot(*d);u=(-d[1]/le,d[0]/le)
  for q,z in[(-1,-.001),(1,-.001),(1,.001),(-1,.001)]:v.append((p[0]+q*.0035*u[0],p[1]+q*.0035*u[1],p[2]+z))
 fs=[(3,2,1,0),(12,13,14,15)]+[(i*4+j,i*4+(j+1)%4,(i+1)*4+(j+1)%4,(i+1)*4+j)for i in range(3)for j in range(4)];record('Whole'+('Left'if side<0 else'Right')+'ForwardLaidChinTie',v,fs,2)
def make_geometry():
 G.clear();cap_shell()
 for side in[-1,1]:ear_cover(side);flat_tie(side)
 global SHIFT
 pts=[p for v,f,m in G.values()for p in v];SHIFT=((min(p[0]for p in pts)+max(p[0]for p in pts))/2,(min(p[1]for p in pts)+max(p[1]for p in pts))/2,0)
 for n,(v,f,m)in list(G.items()):G[n]=([tuple(p[k]-SHIFT[k]for k in range(3))for p in v],f,m)
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
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==proof['mesh_count']
 triangle_count=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons);assert triangle_count==proof['triangles']
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 lo=[min(v[k]for v in points)for k in range(3)];hi=[max(v[k]for v in points)for k in range(3)]
 assert abs(lo[2])<=TOL
 assert len({m for o in parts for m in o.data.materials})==len(PALETTE)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'),compress=False)
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
 for layer in scene.view_layers:layer.cycles.use_denoising=False
 scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
 scene.render.resolution_x=scene.render.resolution_y=640;scene.render.resolution_percentage=100
 scene.world=scene.world or bpy.data.worlds.new('Neutral instrument preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.3,.3,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 scene.view_settings.view_transform='AgX';focus=Vector((0.,0.,.05))
 def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,power,size in [('Key',(-8,-10,22),2200,9),('Fill',(10,-6,10),1500,8),('Rim',(4,12,12),1800,8)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';scene.camera=cam;aim(cam,(4,-6,3.5) if '--tier-single-view' in sys.argv and sys.argv[sys.argv.index('--tier-single-view')+1]=='qa-front' else (-4,-6,4.1));bpy.context.view_layer.update()
 rot=cam.rotation_euler.to_quaternion();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
 cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.12
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';mat=bpy.data.materials.new('Preview_slate');mat.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(mat)
 def config():return dict(engine=scene.render.engine,samples=scene.cycles.samples,adaptive=scene.cycles.use_adaptive_sampling,cycles_denoise=scene.cycles.use_denoising,view_layer_denoise=[x.cycles.use_denoising for x in scene.view_layers],compositor_nodes=scene.use_nodes,compositing=scene.render.use_compositing,threads_mode=scene.render.threads_mode,threads=scene.render.threads)
 qa={'review_mode':'SELF_REVIEW','status':'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW','asset_id':ASSET,'asset':ASSET,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(model).hexdigest(),'mesh_count':len(parts),'mesh_objects':len(parts),'triangles':triangle_count,'materials':len(PALETTE),'bounds_min_m':lo,'bounds_max_m':hi,'composition':proof,'native_readback_claim':False,'normal_setter_or_vertex_bake_used':False,'render_configuration':{'samples':128,'threads':4,'engine':'CYCLES','denoising':False}}
 qa['native_saved_render_config']=config();qa['render_configs']={}
 if '--geometry-only' not in sys.argv:
  view=sys.argv[sys.argv.index('--tier-single-view')+1]if '--tier-single-view'in sys.argv else 'thumbnail';assert view in ['qa-front','thumbnail']
  scene.cycles.samples=16 if view=='qa-front' else 128;qa['render_configs'][view]=config();scene.render.filepath=str(OUT/(view+'.png'));start=time.monotonic();bpy.ops.render.render(write_still=True);qa['render']={'view':view,'samples':scene.cycles.samples,'seconds':time.monotonic()-start,'original_pixels_reviewed':False}
 (OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if p.exists():files[role]={'path':f'assets/sports/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if len(files)==4:
  meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'sports','style':'source-preserved-low-poly','title':TITLE,'description':'One newly authored complete fixed water-polo-cap-inspired empty display: a thin continuous blue domed cap shell with a completely open underside and two bounded side apertures, two whole curved pale ear-cover shells each with seven genuine bounded perforations, and two complete narrow forward-laid chin ties. Each ear cover follows the cap curvature and has real thickness, a closed outer rim and fourteen total actual open bores; the fabric-like dome is not a thick helmet, face cage or chin cup. All five complete component meshes and numeric geometry are newly authored, not removed helmet parts or copied pads. Intentional small positive-volume rim and tie seats keep the fixed empty assembly rooted to the finite flat lower shell hem and tie facets. Five closed whole meshes, three opaque constant untextured PBR roles, metres native Z up and full horizontal bounds-centred grounded origin. One original static model zero scenes. No person, wearer, fit, softness simulation, protection, safe use, impact resistance, breathing or hearing capability, regulation, certification, manufacturing specification, animation or interaction. Simplified faceted static game prop only.','bounds':dict(zip(['x','y','z'],[hi[k]-lo[k]for k in range(3)]),unit='m'),'triangles':triangle_count,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('SCENE_STAGE_COMPLETE',ASSET,triangle_count)
if __name__=='__main__':main()
