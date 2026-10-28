"""Whole spiral-separator and raised complete sample-divider inspection court; two unchanged full originals, zero new models."""
import math,json,hashlib,sys,time,collections,itertools,base64,zlib
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='agriculture-whole-spiral-separator-and-raised-sample-divider-inspection-court-scene-01';VERSION='1.0.0';TITLE='Whole Spiral Separator and Raised Sample Divider Inspection Court'
DESCRIPTION='One new complete empty seed-equipment inspection court, zero new standalone models and one scene. The entire accepted corrected nested two-channel spiral separator occupies the low left-rear station, preserving both full continuous helical troughs, complete top hopper, central mast, corrected under-channel supports, twin low outlets and all six original ground pads. The entire accepted six alternating-chute sample divider with its two full open receiver pans and low original plinth stands separately on one broad right raised platform. A full wide front step belongs to that platform; one common chamfered floor and a short low left-rear boundary leave a visibly open front and central interval. Every original mesh and opaque PBR value is retained at original metre scale under whole translation only. All seven original ground pads/plinths sit on actual opposed full support faces without sinking or extracting any component. Embedded full sources are hash-pinned; original oriented triangles are compared to accepted actual GLBs after inverse translation, while normals and hierarchy are explicitly recomputed/baked rather than claimed byte-identical. This is not the older flat trier/divider/sack intake corner or lower expeller plus tall suspended-riddle side-step deck: the newly completed tall double-helical apparatus and the whole raised low opposed-chute divider form two independent inspection stations with a broad front step. No trier, sack, seed, crop, material path, connecting chute, shared drive or operator is added. No sorting flow, sampling accuracy, processing train, machine compatibility, working access, platform capacity, load, stability, food suitability, engineering or safety capability is made or verified. No rigging animation physics or interaction.'
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];INSIDE_TESTS=[]
PALETTE=[('MatteCommonSeedInspectionFloor',(.25,.28,.26,1),.97,0),('MutedRearBoundaryAndFrontStep',(.31,.33,.27,1),.94,0),('WarmWholeRaisedDividerPlatform',(.43,.36,.24,1),.95,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm(a):return math.sqrt(dot(a,a))
def unit(a):return mul(a,1/norm(a))
def emit(name,v,f,mat,role):
 v=[tuple(round(float(x),9)for x in p)for p in v];f=[tuple(q)for q in f]
 volume=sum(dot(v[q[0]],cross(v[q[i]],v[q[i+1]]))/6 for q in f for i in range(1,len(q)-1))
 if volume<0:f=[tuple(reversed(q))for q in f];volume=-volume
 edges=collections.Counter((a,b)for q in f for a,b in zip(q,q[1:]+q[:1]));assert all(n==1 and edges[(b,a)]==1 for (a,b),n in edges.items()),name
 assert volume>1e-9 and 0<=mat<len(PALETTE) and all(math.isfinite(x)for p in v for x in p),(name,volume)
 G[name]=dict(vertices=v,faces=f,material=mat,role=role)
def rings_mesh(loops):
 n=len(loops[0]);v=sum(loops,[]);f=[tuple(reversed(range(n))),tuple((len(loops)-1)*n+i for i in range(n))]
 for k in range(len(loops)-1):
  for i in range(n):j=(i+1)%n;f.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i))
 return v,f







def earclip(poly):
 cr=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 ids=list(range(len(poly)));out=[]
 if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(poly,poly[1:]+poly[:1]))<0:ids.reverse()
 while len(ids)>3:
  for j,b in enumerate(ids):
   a,c=ids[j-1],ids[(j+1)%len(ids)]
   if cr(poly[a],poly[b],poly[c])<=1e-12:continue
   if any(all(cr(poly[u],poly[v],poly[k])>=-1e-12 for u,v in[(a,b),(b,c),(c,a)])for k in ids if k not in[a,b,c]):continue
   out.append((a,b,c));ids.pop(j);break
  else:raise AssertionError('Non-simple arch profile')
 out.append(tuple(ids));return out
def extrude_y(name,p,y0,y1,mat,role):
 if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);v=[(x,y,z)for y in[y0,y1]for x,z in p];f=[]
 for a,b,c in earclip(p):f.extend([(a,b,c),(c+n,b+n,a+n)])
 for i in range(n):j=(i+1)%n;f.append((i,i+n,j+n,j))
 emit(name,v,f,mat,role)

def box(name,lo,hi,mat,role):
 v=[(x,y,z)for z in[lo[2],hi[2]]for y in[lo[1],hi[1]]for x in[lo[0],hi[0]]]
 emit(name,v,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],mat,role)
def rod(name,a,b,r,mat,role,n=12):
 w=unit(sub(b,a));ref=(0,0,1)if abs(w[2])<.9 else(0,1,0);u=unit(cross(w,ref));vv=cross(w,u)
 loops=[[add(p,add(mul(u,r*math.cos(math.tau*i/n)),mul(vv,r*math.sin(math.tau*i/n))))for i in range(n)]for p in[a,b]]
 v,f=rings_mesh(loops);emit(name,v,f,mat,role)



def plate(name,p,lo,hi,axis,mat,role):
 if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);v=[((t,a,b)if axis=='x'else(a,b,t))for t in[lo,hi]for a,b in p];f=[]
 for a,b,c in earclip(p):f.extend([(c,b,a),(a+n,b+n,c+n)])
 for i in range(n):j=(i+1)%n;f.append((i,j,j+n,i+n))
 emit(name,v,f,mat,role)
def vertical(name,rows,mat,role,n=12):
 v,f=rings_mesh([[(x+r*math.cos(math.tau*j/n),y+r*math.sin(math.tau*j/n),z)for j in range(n)]for x,y,z,r in rows]);emit(name,v,f,mat,role)


def cylinder_x(name,x0,x1,y,z,r,mat,role,N=24,ground=False):
 phase=-math.pi/2+math.pi/N;rr=r/math.cos(math.pi/N)if ground else r
 loops=[[(x,y+rr*math.cos(phase+math.tau*i/N),z+rr*math.sin(phase+math.tau*i/N))for i in range(N)]for x in[x0,x1]];v,f=rings_mesh(loops);emit(name,v,f,mat,role)


COMPONENT_SOURCES=[{'label': 'Spiral', 'sha256': 'dd8944316c7b43a643525f509ef0bc296aceb5904fa8db32212375871c6f9510', 'encoded': 'c-p;vdvn@Iv-kge3Z30LB`F>-;7bySwvIP(vZ*JVq-^hV<E1D8!YCFJmIO9Q<-5PX?w--j*x9Y~yl<*v!(4lMx_kOI<DY)|=~EhBhp``7vt+f7f;_O|Aj^Y!dl^LG%#Yf6nryC@Ru-Tv3)X(>=SkWQ<7^$K!Q9GnKM!YCaGwWhn53Pbe)_2uuGUGKTPr_bsxMg*tEHbUqj0LSU8eGI6{uMfMZqi&lQ>f$dge(IWvxY;tgJP9p{=C{`HZiv%d4}CE0211=!fGDKmBp#QI#{9EW#+5Ox#WyWJ$C|Wd}e8ao#$+yga}1Z2vk9XPYSBq(OTT-eVb!70#BMJjmL9Ja6ZBVcbqOIS|oqthn2=hkrl6xP1TVqi6Rz-A>mYUcJBiaPHY}X;kYYk81rUqgt<dR12e8R~Xg$#G_i57!^PCsCMhk`Q_`2_n)tL*iSK`|1R2D{w7~0gx_LY7<6l%?(|jw{eXSXj`(XX+GHK;%vvOyw7p1@+=`MrYnCQih9*-#3#^%+rXfLSEjCeP<vxDQfHw?_t;_Nb;7+VCo(JmyKjPfFTP6|uC2=0cn`Dz|Qn555Eg_Z6ng<yMnp?o;EU<i((wAkx!w#$jtGo;60mhDl)XJ8a8Ne-~@Op_!!h8vss073K>!6)c+bCQ!E~#@2$dfyC#ZKX;CZ;4ceU}(WYPstj#_w3?{%l!dGhc?Y8!N%eh)hAc1^8xtzzhwCK``Pp4g4Fxn*$+vW+itq1DF9>40P_t*T4{sG7q!a(oe4gWn~GiIwcffMj#V)7<$H=K>*V9LT#CaEhC`wr5|I$ER3&#>mUlYe$HeNZ-X6{7{)|Jgo)rj#2%gV{4_V_Aed5rPGDr4HSv!SV8D&CB{3A^tW7wv)=7p27&->}c!Qb<o%+C1o)nv>csN=L(+tfQ1=ktV(vDjd%LhzzkRXwCfpuPRjy)whO@mnwZm~{lnXFM{b`OZ$gy;og<MA0)`7%xX+**M2GoB|;)|!5VZibpV^}4ZR06oy_2R>J{VBsMqiUr1PUjw&==&BM&Q01blrG|X%GlOA$m^hN584reSqQsxG0OK7`jA)HFE6gy%%92%(r#ofEU`P>g74|WEtgJkYs3M!C0hl)Ovn*VM0V<}+UBpPBFIhwj0pOWWfVbzsCMo~`_Pt~M5l7*TEC!@Pgm-Poihyo|1p(+hzz#F!u?688B*>6Nn^i0e<dvHR&UO(A1cn4%AghcFD3OAde@Vb9B*oH{7-Mc^05PxLAcCeUZG^CbbOns%BpNI&+Jve#mlUh=No*|g_6p;cs0xX7G#d-&g%DDSl_qpbVa7C^PH`Tg;S38ANr+CsA*i)I4g8ehS`x;yp|vSdC^)tZj!VAA@IH1cjb(;HBoqk2;LQ6$4hdAyJ?~T8WRP_Vvi=&RiA54L$dp9{15reyZv*S!)@H3(sAFIJ+f877{`I1eU>Hq~qF}YocUBlh8v=)Wf}XKDKZZa~;%GM@xalAPy8JK9>^l-zyfMnUPW^3|@7fDKHAEodyRw4CBAkUmJlhc%2@vlu0;*UAv|y&=MF=?o$?ea$i$9wM8CGIA6CefgHB<w@9d8!?j810R0<cRE&=wrZutfXes$+c=SP30TP7H#Xu;`Gs5=?eYh-cXdJov0ubnMnU@7wp`hxZ@<cIl1A!`GiaUY)(Z;?M8SKJ)KiKV6*jhqvcY6!81~$IJI`&L>yrm)x-R`Rv2_)z!H-a_oQj>FRe#$NAgTUj=9J{C5zot(?wrS9Okhs?$4BJy&&J9H~zCg{vI<4VdgQ4}$1Di77hw-?F6QPA95!f{w?}xzp(hjX|AwieIBm@QEbxYa@s;-)}4=sdMjGb^7Shm(I^$U~-w!Pj8q2-hm*{<t@(r&;C54PTl9|(ZiJ8mm1LL4CuHu4;Gd`pF6&qx`Q;pZa_wFK#$J-!48|8TK8&4to1cqb0e3#WSi-}F6}3}tTqw8Wz8<nGU>wXD=p_qUK>2ytkCX>p;@!3c5(bsZ~SaJ>W|w#e&ADYtn{ZYm35_7=}$c>>q)H)87Jw=@e2@0o9$$`Y3>MczMgp#hk3Obud#QidrO;Og*GwhMs3wXVI-B}ta1k}YwL{!3oIZV@SC4I_pW;B7ARTsM>_4S?RdB_9d5b!mWmf+3`8P3@CZ=^-*$A1g^ZQpg}#OO#=j4G<FV@=o?2yp{ut6nme)>CML~=i+C4153Kx3xSKUD|eHuW7L6=0UDj-7*M_YcktYCf}WL`zz@4RM_ojSZ*4H!^l_V!lYj(UUf!R=_!1H40sWY`IiwUHBhUQhHI8hqqTu^D43qak=$71J<W-GP0v${ZJEJ^`f15%_-T1?`tSRQHvKeR)Oe)?Dw3>VWxp>%(jjVyi)~mHn_PyQK6E^T0scyAgdKd-HIH{lJ`1hBFTY;L~p=1D4vJp$CtNf(eFXU^ZC=+0u!UWStSI#2x|1Ux`MCTi$H`u15I&aBE~UV;5_e8mAb6w)R<k5H@!njX_LQcvBYEdI6G$od#b#2ZZJRcRXBl=%@iLJ2y0eqMu)sb92BGmY+f*EzLAQN=yG^cJWgj&ueF$L_3;qmU@xDn$CTq4>cP&1q-{+oS9)=x9t>c%;lyHD0rTE5mX?jTn~>8vVvkklAeg1&{;|Yn&TOb)u2o2sOSe%Cx2i91#@7Ujz+$NS?`vxOf8xW749!b26JCzuz=M<5CK<HC8n8q_%iy^hOnX!&KE+e8DdOrLK1ci#mFBEAXEK&Hg;cmpy*zIV2l{u!;g0kQL^c|(LJ{M_s!V-#cOj{263ad0C6O|1pb=g=Zv__El2|Z(a1NV%f=(#nz37(8OSZDf$M>ALee@}J73%(TUBTWEh!j4ZGusH#@q=xaSjtNb?lEx4Ev8&FA&9&6eP0uZJ@U@xKKBt$Q^2uLaor!eV%US!DJ`gxmLTb+VyHO_|I>>TFa&vJHFOrWjJn4L@kWECJr4rIIYxI#u}YkBc6RM$Jkev8!XZ_&oPdeHVg;2gGGl76fAP2QHY&5h}9JT{e##g^8Rz|7^)C`zR-Vy@{u!1IB=TWOI?(xW!OBiDvP2ujG}}N(q)LB<6@;K>~UdF3h#AcmkV(=jq5OsoUZDtBhpQrV|AjQt5baHsvbTc<5ORqqU?yvj`6vVPd&7Mu1?%>1%4Kv$y|mdjHN}TioIT+)^O+XsZA;jogG9p3lHOBHkY_%nmKn^jQgtdl8KYS=(@v=^pivNPN5h2ZnvH(*Z{9AD812$RI0V2pQI9ORQimMky(<-d6N5^XW=2_t)lwv)--@U(r6$DY;A+b<_IFTBTQlsy$6TJ@X<Y%U0z2deKcRlPW!MF|Nk+ElhY0{$}z9!+4nZ1o3<^NW#>XRfUP>=U*VdWqCHlQueoOS7rEvO^9*?BDXt-O${FuRQlBPw*+a@}?9&Lmbg+*yzF_0k?qDBHaFuZ1mj^V#oT*YS2LR)zXn^%*ZO~6Nzu$M&eNV<Hf&b|BkJUA6sNP$cnM@dK7|GD{7_4=8*gr6zJ`U5=OAqU7qH@}28HJh3N=s%TiE@xu5W%A#RQTW{)?Bn8eC%n_<dctXDS3EdW9X-Ukx^<$`YLT^>T6eh?KM%fe}732d1Q;RCemIW+2xOWc3H28r7puTesYH^Iu*NQn6bbeY!%l|=Fu8F+xpphOYW@FY0QGn_(Q~P<&%pKl4ECOkv}D~+mG2v)Se}<<4Z46Tf9hxTdULJ?NPMXZe0NyIqlBTDI_cmRsFlGsE9w%?=c~lK=SN=ke}}z(-DkY`yk6xCxkMABa0ef{5Bi8JNZR}-5*Ga{OWX%Ph6ZFGLj`~y`jvtPj0HxBa`K@0&JIE1O{U?jcZoJvgyHku%P4a3D(d(p$Yr65-yQ~UiSoopIXt^wyu#@+<*(X6|a2ir+VQZlDpTmDZhgHe-BpEAgy5l4Yefin)N+!{7(aaWxEwE-x=Y28-qJT&+9U8j&Kt5#3WF>Ke0W~AcsO?1i{`tx^a2yvCbnbt3^&fy{0Rurmw{pcqvXIcCHL7e8<jbI-y<iT0m0(hPr~xVxg75M9s5UxWd_IS?p}#cGZqLTY-gJ4G{vNEz4p6ezXM)A-P!k%uK)5=1XA!W6VwDr|nFPVe5|~W<svS>@Ha67DvIzy`3inagJ~78(oTDQwM7}-cYzjTUj1JkUsAZ(b4O7di~)%#iw59q&v))LGE`eqPoRFJJ{lMgf?tF9_WD0Jl~U^?LsK^pWPgCgP|Fr5F)g2%-yDGO)FIhJ)FOVh=ac677$nmo<-!<dqIdhdGQ>-+N1&!PjJ!ki?Zlcih6x165o|zP^&Rw9@I1#t#L?=R>~oAH+<wg+u*D_Si0reiSi9Qm<kZ7E>%m`J7g52ea!r|S128Nf`(3lCi|2Twn5Dd+8FoMzS8O5(pjOxH0<<hyTahCX*su^Sd~pv{R^Aww}pXTetObg;2?}<<ktlUiqBIbdzT!lJd5WN0=0*F$G9i-ev-!|DcOnH>A&dKzZ9QOU(`N#MOZ#BKj4RaK0cApW2o&MRF&8ehcfCxM~<adBadYe=q|CylGG8jGQd{nJvtOQ=#@dFa`@~4F6yq_$FRYD2^&Yf3O0_Pck5sHP+$-8aqY7R=l=8Z1I`oq+&huaW7t;}Y|MjTUBpn!V4Q%X%J2)zqiU#)5n_S@=)qx8NVLR+!^(h-O=6Iz4D&dEDv_8C;CL=+6KSA>rl~$|Sulnf+DV{}Ml2#k{LM&i4(zsWyqCkLMAcWXDVOv~CG;mJ3&^GStSYX`0+Cse5{yJzP%Y-#jJGDU*=D`tAd3#0>hSW0jxt)(kji(~JYjumMgitR&!Uq^;uv9)W}-5IF&pZ|sluK@CqFt;$9;9uQxJ@&FULO;+Iuju@tjA5GzbZ@6a22}`GVK^hgpO^sO9AQ0t>n@xeJRI2Ypu`iC-b%kAb{u?eXbRS=)U{wZQOkU2)Oa_0tv97AmNp;X2m0fEu4>Lyl?bC=+9p>3L}q4K#Xf^#Uss5@3j#0;*siSHV7dN#_;E$~7h~DUQxe{SOde6A`nSS1hpaR&^K}LOC-s2-J)ef0rldb(yx9OMBgN`47VNW@$7|5h|r6lHdws$>4a95`jWd+#eu9&}J)GrUoAjVsjg59hHshk=wM=Tm;wt_E=Z<h09Ds$s~nL(GsZ06`&-7!$lAj%33K%^g<&m-Nc!(A$ARh02)tOC4JdtE`S!VH%p}Kesck>SgSbcva#@-)k_qdU>nF*AaT3bRww{(Q<@8z0}TrSBa<sAxUNBQS%khn1lKi4&{FgpF<Za|`0-qT!NEqrP}xZjz!U^hP0cAquEC&fHi^d8D?Pz+Y83EFtx!c({}(c<bUEq16wxO_ua?Lm=^IMUPZsAobwiRi3bWBqZ>%hd!a2DYJ1uSdiw62tE$`Km9fwYz&NZb^@l!hC`knq!w^4FJf!7`zQ!Hjo$uY%Zd#9CN6rF`M=Mov&l#B=31!4A$RMBq#<ltU0MI9J7r^Fml3n<&m9fqoY;NNZe0E4`>Co=Ou&ps7{wq|S`moBK|;mwW5`qzJ-*7USv4yhcIwpRH?!4%mBLvUz+Va{|39dits_T`GV#TLJT-aOLj`VVxa{V6({35pyF5;2uz7;UJud4y{Ajw*5vIIRE*bF#1trvnHlEwgr3Bnvptr$%Jbilw1MSJGhR100I~>ufK|&zf=ef)N&98^Qu~0Yd7-ZaraPvD|q?RR_-3Hj|8d2%V|>jLL>PPY7YTYZ>4)h6Sk?fTwl>7&~0rDz@<Z%+%fIEI)f<<ahhbha&n<D_qSh)T=eZ5SXGQmoP3Bp(Z{Gb~iJNUc=<f>K`b%*+lQXZp1L2QZsDHyIN*cNI88`IAsJvuaTrr&GFj(V^XxB#`%(36W~w+(0Qjtc~%;2oS$%sjd}|jpjoc`sm&;(Mhwe~BXD28*TWX|o{L28o>Ez_`vPUCsYzr`crlQ2Mpy1njnG*oOuiYU5}HwMfheA@f`ZfM!t^vPX(KJ1lJm&GO`sCkm-z<plC~q&-1T|AE0y)wuTv?*Husxg%Ms5o%V-5~dhh}#&tEox``Nk-=!g&IHSA-jbp9N+X%oXD#kz-b(jSsjWLHV&q1M|l+dyKIy4q<`VvLbB9JUtyPe}a_`f*N~MX#B?Y$XY9la;3_$Ut~<iuKOJRGb_VSRo5O;=CWU?;LfzDyIW9#|a>NK>o)fN<Lb%Y$V&lde_<d(I&{8GVXpovQ1NaJRV;D_WtdaCqclrvm)p4C>)njdfn7LSo!ylRJn)!LK?F-%sl|u;tpy+F{sV%=|B&|@EC+GorWZ?*1a9pc_zVCcG2c!{#e{gPL6AzThRs$@Ofk#+yep{uTiE)m#mw>&o*f=p;Wio#N;3r83`(fbwXKznfEb?*<+$pB(k8)TW~#(zP^K217Wi@8?+{3&8nDuxLML>TqJNzGrdLqavx|+*L~Fw+RuyWDPGNuo14as4<2l@9>Y7vAdS5&5)GKB(_kA0cav-e#_?=Mi$3(oXCGwdfSZ!en5jy3p5%W@>UBL0)HobVYn3=^sHG5PWQMayk~Q;mLn&|MolNFrj?k==8D+(=r>a1?5-~er*d}yvPGssyk@Y>HS-h)s6S%FnpI-lQsiT;kK1`2K7gxW1@{S-jhyQqgaXz{F?fvV&eLTOs#Bm2n-+F!a`}xJ$rT5Lwmz&iz_QS{?IAG)F>bL_X%f9v7F#h8lrC{J=3b|4l9kVDROHG%+tmHObiquj8<qdO5(diDTTTtp;eTwVU-^nCLw|i=69Ij|nKv*iWFj^*?AkQgV;l)D;8}&74zYk^6lgrm<AI`D#@8qWaaQ^Yl`GxiQx3kN0ikIlC2h;UVO=)xFVglL5n>@sZ>-xX5h1IC+Ot;HC4Fc2X*T4UEg|96P)*(eRnNqf8Cu89~VHy`HX<wdyIDdVG6QI!)Gy>vtHd!#aj*_V#=@=Z#1@g>T9A>3nb3gYxMK-8Acv#kf!jx<SXXUmy!_=cDbRysc?QqGEe|9L)4LZxoTFE-uF3W?JXa9bFb@BeSy}!*2XY52|yw{WAF&!Dd9ZBu<?AQN#4YZs7vmJN>9XYi&^RQcu3Xr_ld)}%Q5+3}yzox9#33tWpf|B8bhOmv2Fe@4`%C-@EceyDGg2>+mX*SqKPxaI*MokQ^&1w_sMN%cniX;p3CQP~sPU*m(XA|Ol&wl&<pXYDvy)C@sIs(I$e;t&#<~uJ~4EEKtKYx7J7^Km9mP8O0GUvs+U(Xt?G1zJX=@n;kaYnEB{GXpekLPb7A7uONf!RMWne3T8z@{nN?1w$zuF4ifY9yA$CA!P15!a2;N23m)GK$N=N}LvDRYU?V!DLZv501Y}<Til{bnVcgrcZ!!F?$HKvaWp;T3zUmY4RZ!9w*O7P_y0Jm=Cw@ULxL$#s=v&5c(7eH}U)^EmttVuZ?WR^~O)<*o&EGw#DcKGtV>Bre-FCYt{mF7Y+gmyb~cSaZp2x@tKo#x+b=G<?Ru8ad5|KtUFwF=HX%?OT;)H|3qoY)O3&z*WRi_UneBS`BT<`qUzY6Q<%Krnhc3wFW<a{q+WNzcn!OAWK%5AdQAh`V@T|Uzlrh*t3rC3vgrkZPtNcMEqP&;mcP>yqj2`1A+NpC@GM#{{Rgdjol27{;_p?MW#nD|2VV$!(4kxHaBdo3>U{lu&1r{>!GI&BdYG(n-otW_Nhc(6Mb~18lfWUA4@5^^w?&3+xoL9X$(E5Tf=wm4Rwq#tN}@0C&MDScjnFSLjEiBwgf|Y&K;G#jAK650`6Qe}XXd+sx|lVHNnx*`)^7jH)|FZZ6Elg`Ez~oeNWIp%0sn?{aa$Bg*mdDoj0y@BEm9OjGR4Zw0%{18O%e~xe8M;r!XjN|z>su<vNPYT)|sO@NYOow$xX1!wCcw<e&_<jbjKDO)S7~4wDqF1povR@3Y)OPTji0UL;B2Qy`y@kX2z(|SfPOPm+djP-K^*2QgMgL{#_LR`VTiL!2tT!rblRKSyS*b0mq|2C0YqsoK!>ONhN7X*fl?zO$e$9CEbJPo#{$vS&L?b&ORG?G)|sWN5QZG!7skJmAF{)Y=E_uBBUg6u`AS~?omQx%A&odu<Kw^bexcb_TIY|>A?UNW7=v2RGP0a5ucIjUmeJWZPT)nkx1(psF_f}6$F8f@@XhHy)<}0qHMp;J5K~!hP5&<03?Bzt$^pHKI*G{Tb?H6?v^HEcUXcmTL!ZmCOeXp8C|!b%RE?k*<Mp(!iFG0J9v6;6Q&^)`g3-olKm8PLYy*w94?Y*&THcPVd%#R{x01)z=$2D14+MkvhX^F^2qE_*=8ADT9SXZgcOzY;F{;mJD^1WRhbP<If$0-TJPl+)+zz)b=ejK2<5#38r175ER1;p&FF@JLU9GH2W<E~HbWERX2ZYPG22smXuIfR4;~+m>?1;rM$}|=WDf`+J5FMQ;|b%{9uTlLAO-6Zolhzgp!7RH<BcB)0Ao+vI-R%J&d-|M9Mpo$)9`+Bm!#4Bf1uMOr3RycG(rY4M%*}gQRMz$3&sj(WQF2HB3eyK9EEeI2CX~xMtU;2bu*KhIBUac0Nnr+tcg{)Zt1`;;T``7UY)ceUnj6~C(AI;oT7nRt2w)+L(zWf`6NX%O6~}Hp2=Yz27UfaS^C4J&PblCpigw2dvqr#=&2<zW9bZM6uYk;+!hGqt=Bt5-7w2|z%>oH;Q_J?13W{E;jNwkB|(pJYN&dyZlzXF*Vo@=%8kBYpn0VBZF8`F<@FBA0(^S@Du31Q4hRcHnt$oYp<+pFlr#a}Tg9#>!rjl-8Sg(wcS@Xz!}{|sUqY|pT|YfWSv)7L`t0Ky@}dSo8+$^+ibDt(>J5k_oRO0@TS79-+r%CWfn4*AwX4V{=c*1n(?!)8D8lCype&&K-O%Yftr8gTF%oql*uBRnQ<gYPR>8Fo4XpbVd2p#G7xmWA8kkh{hZ#N$Bj4L|t!)@h8^u$)XE%&yjp7+y=)gR%OuWc{7EPZ;vjcN=&wQpU3(q3|KsxyNJVh6V|G?`@iUqhN?rQ*qu=uVBq-0F@XgnfU?s4cGKhtS!0EqV}3`#C3bT~rA$myxh(R2Jb>A#eup(BNFr#=35+<U1y{Uf??Kw&^(x2M^XlmCl3DgYP)<peAo_HvmoS1&5Ui$-(Z|L)6$I=*7i?lA+NFv%B-@kTv>*&CZ1g(T3p&)wd}<aO&7jpaPI_FkrO?2;x8(Nk)hziSJ%Q(W7>1_iEg*x2e$nQ1g*QL+~?+XTA(oH=5W1<@jhhF-VR)~blc#a8uFZRuRDux%y^3kZ_eCijUR)anrleUAcBo{XYi+5<Tmbq@|cPjo7hJs`xw@J`CIiJnASN(&rwEsn_)OJomy;rM1JJ^2@syOI#Ox^#XMeXTw57do1QVb{xjY>zzIvQmExQz@QLVpL&0&e|Ovjg{0*_tg~^bPZvCfy-L)v?wm-{)IfjJ>}T%W7u@zT+%>nRV+~zO^MNIjU|rxXq<4f$qG70$WSR8>j_tz)x@MRO^Pw7S@Gq&$vUYF>DvQe*;A+<v}w9~f}=I^*D@3KjiC6>DJ9D=vwn@(VzRQ}n#k4?9SKWJGLEnXQIx4hk~f<JiX&kV!X(B0OkqIXif}eBvan3<ntseBxR?ACa8Hn~Q-&Xwzc%XR=KVC8gKID#bzqCIoo!N@71SMLtpQ)lPhtszXZj(5T<*J5?38lHusF`QyOZZT*m~{onOB;Z6$O?_{j1un=>UX1R<Q+&TaHhwCPb#&tvC8J%FkZaXE;keXS=0qLipJoyB&T1cuV)NrAV{^3hIyyTz9^<zlxNUfZP@$u>(1GDukMLzCPQmf9Vb?xBb2qHYw55i0N+YmOABjJ61OB>15Rhy`>%TNgwvVm-+);5B%ABEBhVX6BQ)uwI-Ql6A4B6`iQ?y{q<6=6RYwO7k2z>;>=`YC=+->Q_EHKmL+%7Yj@fATsUv(Tb+DD)3rIig)Rp+U9ID<bfs$AxKcHh)U;?P<-WF1*Xq_>%fivk*RrO3EsJ&-3cg2OhTM;+f@UY`L(Rb4$)sVR+?ioerSPAJqTgmPYo2);@LQu=;J9!}>wHiVa77k+^UT~f9R~Oom~Z;FY8L*N7lZ?X&+IwHI5WN}Cj-HdnP-R2JZs}f-~>JH+2|FN8&1SV#+|tV8|s^{l5SJn2p+r5q@2oSVG0sslA`37z9dU^TWs8GaZ;QUd<)CGJE3VIO6Y<Zv#52e_3N}6xiuG9SsS{gx(y0d@oiiCM%U(Sik$P{M6gYPK-QjYJBxr}T`=g4ep(~|(2>9`O6mW?HqzTva6gF!EMpz{alorDCBbb&5U{yH)I|JoTkyv%@dtl(>2U{IZe3d3^1)Sdz2*B}15t!XdkjTzIGygPo1zY?T8qyK_7Ie8K3b0k{c#C3j^1X`RIkeCdY?b@CC2HrbRW=Qzj&C;9G+`GpDiawij9?%D*9p=oaqyYlOvH8*m-gnYl<R1DX4?!q&Q1)-b{l@vRIHOln@TvZtY1%!e8k{*2NypLohj31j`-`M36bAGitx8XZk<YU|LMjvTA%+%Ul7v#JtjCz1ULI+~C$@v_i@A=U=>U;v5)|5-+<}dalHi#dj%0Z8@mTK0yD`7lFS+2>rsKLPL}CX{8)(+*TIAY@&%Manv2=$vhD$P8DuT^4q9XCknDrLxWKnU!ix$^hjMipdUPREW;Q?V3Z=219S0Y!u|AG%pb8%FT<H9eqdWwTC@cWlh<C=?+FkBniFk7rrzWF2q*pw3&tTQydmjQ^6((#3m?P^q?b}kk<KZnEgBk7n*J}*@rwhWKGd9HJUq_+X_5w|)3OxN{0xvdT)cwH2qUy(WC+55&mFD3*M+qzODpjMmzc*SJK-yz@OpKagwn1kbU|u23=QApaPiYqw6?jeQV@3q-u<K<>fRIGo2^#Xuf+@IwyvQz?^!XY5n%#I^&2P>9v=o)VZP<!NeIfvQ&>aLJD-X_Tc>Z?Vx9=Q=Km>l$-7-Sqp8Fll^B?TJniD4%GETgAW_;77L{oZbe6c-k4;M5ndrfGlL9xz2yTlX8=D050vOwE`xC2-4Ebx0&!(`UEaFE;DBC?g;4n(Okx7!ODA*4aoFjKUT!v_?^Q?Z<RsveyNSqwY5MA0)LJHN(eeGM7yf1zzf_)y(g<cGkzVc4M@A4?YG<8;-!~f^wuzHGhm27HML+_u&oqV?rI$2J5BS)ZPU!DJRV!NeueJ~-c*^dbsX|rI?DO<EWO0KXdR<dEM4bAA*^D4~2iuQwPGa{dyLKqb43M7Cbg}jS8;3_leCY2RRZEXU{uq*62!<V%nv?_zgsuFQlI#jIe_n$8C^Ku=`=t8Q6uhs`x6%h*eg^HE^n$k<_->TzYE^%Cx^+oj9fU_r@%;qLXl8dM_E2Z@?vuRXbH5D1P@71hRw|tO^JF(ze`k9~Sslz48o=}d`g!WxtA*c)?eJ~6uIE`8Dd9s;O9v(RdY(?8EsRNXwCYk^Q2*gkM293Zd<LHM;f?1NzGe<{1-KO7&8CzGf(*9JuYMXg~O~(9bZT}&1X9aTE&AcTw|8W(+>L=o4PyJ-sD3k}i!towS;VNSNq>;Zd${X?2v0HgKDr5D<q4}VyB%2i5pmFROT(g{n_8_&3wWnVr?qo~9e{$+n;_LMhRFP(xc@9We*#p~kJCOb0c?X}C!TmhECTASZhI$gGp7h6Ae{arB-d`h7dN86$_;`?*UZk5zaO;t9tqG~q(Az))=>`DtT1_Mje;wru$K+&qbZg<$A6JJqr=y~BYP(9eHz{WCKKyDc4jTtLfX^C+X|{t6QT>jsk9HDUE{e>Hjaj{%-e>Yn)K2F&6ll9!Ny3Ov@!ycL*@HcB%dT~%<OswDwQhayo8)@f1J3hM_EemNHfKZvx{gjknP3pfb1K!v(&KNJ;d+j!Qf2`8H)*Rivh6{+@tB5>M)FGO+~J~x6`(<slqLQ>l`KQmvdR!Y#%o4<DP4;n=p}GVi%k1M#S($`3*AMO_=#>#CQmZa$t45LD6G@djPejH8Fp&{-X8P{KY8g{*Q!zBV7CX4JKvQp?$g5Js+mXjp!QYSb*%|_tSMJmkul#2)fQuvI$Y79P=ZNarl57HHPb>hOo9iosyQc4+Y(B9v7w{}ab7hOSsj#!0p!v|gasi|ixC=Jg8-H(>Knr40cUk6A#O6=<s`yuB1GBp$m@hiem*G^ffnI4R<2WjXzy}*ml(nbyEos=g0y&8SSOvY{2O{+mTTpD2`La9@UbNokEXcw9d{t`-TLh`AbfO47y`(<l#oUOrYat9eHHR`L$B{1*#8F&^#z06=WHRq(iZBp4|z6$-##)5ienQBR87!0!kd&*T4Q5W=)40~A50EHXT9S(!47A9>eThl8mp5~-rA#8$#aj!x4G`{Bgm8jC1(d6h6L+~U>rkYkWc}YisZ-+E6>Iseq%B6{c!tDzX1RJ@EZ;Poxl#i!UkQFUWrY_uL+f)d_O^~A146dYz{am@TA3-mQwaWPYYQ999$>FFN8%>-2ehZ{I`(!oM>XrXbH$Pu0DQGu;#mnO7Hx1)ut;(v(#VEQ~293ilEg}$1tZR{IWeIe`K>XT(g}vs616qWGI5n9<UWfKH`ymj{$c0|J5EVsdhPN>e(yo+Fuf~yf@g6klPd_FLyUE1vJ|rrX*Qtv=Kc5yrehO1E}6$9#FZZIZxB((}X>LK-WK8=RiI`IJ@$rLzvXj&Jv;{BO_VJBjI9!%27tDJ-KX(cfI*t1V84OP{?mo)8YI7;wFG;CsY6FQ{Elw#KDSHDSh?nM$D72+2m2~|K)FXVa}CGj^~v}AX{~H#mn;=T9y44+qATxQdmanmICZhZqUdzVSd{>%vL0{Z5->As!3B-#4d|Po7lII;ASkS9P_3Wm!Wjzw**@#PvHGNG{Uik)!XfMoV2yHVf^f%V5QevvIJ3SCTnwMXte=nS{lJP<UpZgzdQd#S1A59xi~+2^DkQopO?&_nPy0X(EI*Qm){XOfA{{Qb@s>AZ=WvS|NH!nb@l%I0>3Wg-pb#5L-Rg3gpK7#Bw=>elngRHODsR{^<PMY3Y3^m03Y;v|5|BFtGM}v6;rwPyOwJ)*Qca8+Igm`!%8`iRtBRFdi;>CX;T<Prhp$IZqX_xpD#YWegEOyE8qfB1>NoPtxs-w_Tj^)fADn#c@VU{?b!pTcdADCf7Dl}$75G=+oRxKDp5MpHQ!~B%l9AOHD;sFZPAC?EL`+_AKqVHN%Ac{>z_Ff`cUIGd2At$Mq|=Ex!)%U>x=ggmQQxpZ}wC8Fbye9U)kTj7h_yroqc?BcJam=Rqke0E@YMWu!{Rv<-M!MeXB9iaTV8P5=OO@_PdH_W@Vyq$`29hZcs(N#WV_UVdw5|TBdyf(e$L+EO6?`Qgn=%Cyn^^S*zZl$Y9nZ@m+d-g^eM(`7f`6Eb%Wva#3iQUy~8xv~8|)R7Jvg)EhqvD-ndE{T62@QFu`fF=vv0%CaJcQI^TygDEM|tzCDF3*Za^P{372sV=v0Se0`z?^XsLRJT})nh2{_>HQkjFXYv4;XQKoZvTxtppgVN(R!iGvYggjJ>mSC3hJT8@ZY=%zp|M)DXtITh`*$_cH$tKEc%Pt?DVwPI|*LA=)LT{n0NcrSugOPzv#X^IU;9Qp+r|NDDmG0+K3u6Iz8?}By`8JI+%c@`3&qt9Bfd{CI%9GGeW4i8btN%0<;I;zJD)esy@d_C}a-*)B=@ITVp@-=ry%@ux;j=QngHP+Ne@C{$BQ^{V)2(MeBIHhfcoNZ}&2oue^e64cS$m=4L31RZfEi*;iC5HwK<uW6P@C?K3e1ug0eAgKKa)d3o8%_XMAECW%>!p5zC!=w^RH0PMY<sDHOCb5&_n+!h;`m3xSO^pJGM?CCtP*=Q+yL+kwb=Bb0eekrh|>dCzaiXJ{zyL+;B9i((S1#o%2ZdXsiW^wasRJE$%DJSpq>_)pA#>Fk7{a2!#4n54G|M%S1Umy3;OGzDbhg9x(n=6p~jqf;;M(^2Y*Z;Izi)6OROj;gapB5D+pYYAIZ>xR5mQ}@jT9_^(2mEm5Bx;?2^OFu`Ot3nS@57`ce}V?s4mMGcdJfOsE}OY@F@>)D+)Qpauq5sFzaew}Wpg?AaokFRWkNZbcR{Mi*wn`L-vZcPPWy;1LZ7<ow9D7A9s4beJDVQWZuhC+=(MYj=q9yeUxX{0Ue-QV_<H;T<!nGV%nnXMn^1h2Edl!s%B!ua>ofO%j8jrN4kZxg*`M`|d;5UCn@bpE(O>U8UWO@ykxVnZd4KsgyC}m7J^C>$@!K?_W<FiTVHn*ZzU+er#SM5~b1$1~cq&;R-<z+L!lYUz6TaT;ah<u%#N9poD!}1uEztFGl+Yn0c`cl~M2qNSM+&sbs~8mLK7t{pUsv7(w$wBr*X}Hc-HA9lTi1`>eJuK9k-UC#-M9wnboyY#zWh;{o&lvfl=kLd>%Y$u`qy!i(apFl_Se}GI!^VH?P@S`LS;f<WLnD~u+k;d2*-aVjH8QdoLmdt>}&8KlCyslxv^CS+$z_${$zO3MCcv@L=KY5WVSmlMMNn`zPHR@0-IDq88oD~7msE0EJ{cYB?E^OLz+^@Riox@v+~N9Zfvf7jUT47NI)vf=|HalQVj2yC#qITM<Mx7W$j-|<$~c~h}@dLB|@O92XrzaepHNF{)-blk^G?ylY4}IY-(1*sBem;lwnrF3?;YoAHm`vs--K-*rP<3Dx*IjU(YK)vj*KHXYzHFfbWBZ`{%nuYQQguT-Ts!9A-KI${VK~rUvp<$+f8JW^h$?3o2fk1|eum#SBw}k~5UWkyC-KNp>AhF>%c1F|{)QgX9sZu`+EJO7_BJmDWKk*7oocCI76fYcD$h{R9SY&0pXQ&(rf33guq5^t{Jtzm7xkU(s&1dE&#8Xn5NXg`kD=BnzAba*$?a^1zQ=XqEY@<LFJR{K3VhgYB^4UZZ?TpS{DPx>i=sS<#cq@NB-3V{Ji5fR(TPXxhidgwHFUlq+UV5NfVF-#B1p(8${+{yGX0>Fua@;92%N`N*@UQB&>ny+!t&SNCD;apCQ8UsPQem_>{nYB;D8eJSDxfAK7N^1%Ry|1_NbPkE<ogL&U>3e)apTz$O#DVu$40GA{3KjBVt#q<Q`)}mSL@qKEDs}BotQFZ=tF%HLo*`1c{8HQ6Gt8lZk(qQE=+q<P-B<5?$5=7&VMC3ZOrkSeZO%~!Adr!HVCDmGnaEvm}GIzg$jEcuKNs?$#YSDm48UElRHebOJJA%~ChEYM50@)5h8lwz~Fh@l^)98P+q2u)E#+W4jKB$vFbmI=!`o`1$Dg*8Q-WzQ@l&sE>xJ66zB-n0e8f?}NYBl1F!hGQIAkQSB<o;e>bHi`<u-~pWtW4-0Y}UHNZYLe^dvAvgT}{}#QPfLM)z(uhJyKhb>^|#tdM5z5`L0eq_Tp5Gewt0FQeW3MxetHp1Ta3AlC#-9xANK_$u?F=Ve&K0N(c-hK8p1Hc+Dvq5Pf;E9H*VbE-Z7+h*CKRh?%pZbC8TMc@cEgfWJ#p0)Jh3l9y+RM71ien)(A_RA=3-erVB97Z@~ms|OYhy|qZMrYn9|xyRQ-tOpMf(7!pjAOTgcck}|lX3Z0NChtm$pMJaooup^oMB~-l2Vw&ctGFrBPpM-CNtJT_3WE9cQ1{wbrMus)WVxlnQ?#wT0nyN}y3*y&qqeJL&WCpc-C7pP;{eL0H|5@5;6$P==<pxZrd&X;{?;6-Xk*d<w(u+vH<A<uTNrP0r$9fIb=T2fdz?hp5V0JvXT^iJ?q}-^@&Q|d!`P?TEFIsRa%ss`MuHhfJW;+?(U;`H){g#oIsFmdNUl3!I1blRRCmFz<WeHBthik~;jV||pzi%F;J7$*D#wZ`NKH4q1@l0p#TRYMjUPOCBSpW)hPG;+Oz6)I$2aB$1FdLKtkjGnbRv{X*J#Mw092-#=XD3oM_tTIZ}?`eN8PQe8M1OaakX!R=5ujOQ$~~c^I;!?bc%hy`LT1N2q93|o4Pc8k8$ovd7)^bNb6dLDd>(<QOM(8E`1QdM-+V8<j}l+H!rTxpG|tStw~npRzLD(@&#;ioWwZ`1Q`we5}uL%SSMXxE?t*$6Vx6Xqo^U19y7Owk6BlYmV#jRnK=9TT|0V~l+Pv1_8<20@;!FK%zx0o+bd4lryabP^mm&`VH-Z~GA|z-+~+b!t=^#OsW%dVR0LW0DUn7V_FoB;(arsaoGYc=)83iZt#35LZ-q`PN4Y)FACz6oBjfx+{-ErDuC3CWqNdBkga7jC?Ba_4=3+Ae$K;sl1ekSrA4Kv3IAy?4N?@B)@XE9^&ZaOb%b?7RXqjvalOn+>5tG-Se*gU8{ObJC6p7aV1%um5Wd', 'offset': (-0.75, 0.375, 0.0625), 'rotation_quarter_turns': 0, 'seat': 'WholeChamferedInspectionCourtFloor'}, {'label': 'Divider', 'sha256': '79e798c00e0db97cb424b465c5dd05da0353c7be670f1cb0a66947b50ce36714', 'encoded': 'c-p;veRG@0((nKJ6g<0i3WyPw{FX!tTh~dPtn1{&Dciey_R&>QNWu~^0vV8OC6({~{JMJv5R#qb-gEEP#)f(A>FMt2x52;s^2<dQO`{};jr&;|hei+=VU`3%luX;>*|G?Y;yy~+iy$%bV7@?$NwkV4VdfeiqUo%-59y~d4{pQExH|jr&c8hS^Ze|uzL6IgWo!hCMHpm3G7gP2iP!Egzx>jQ=8H6=PQ}dmoTrI13-VbUjhuX)J4G}PopBn+;kby>BzGb}RHSK~w{Eg@ZY<CXZ4EWZC%m?<u1_zoJ?iPw56kXf{BiA3mF4?4Q5^cd?Pg(~#w%31iy#Y=qIG(8b$0EU!8D7;%eYu(Vf!X}2q*0=B(yaW+Jc0(LPERKHT!>_U0$7EeDut&+i^Q)|N8v;!<lEkqoIt`+E8y8pVu_hC*bo+@cCATGFxxYuHIapf4b(eE|Snl!uxn_1j}NUW*BOmQhSV`F<Zio-P?q#hIQ9CHAX>lYos?u9z7UEw#1&!qA^MqVPgEz&IQrNcorl{80SV7j>Bjb<_6<CFp?n4(tCscVUQ(;&Ww2quyP|vCdMSp$6+$bOWFwmb&=i&*#uK8(i|H|LnQ?_&j1)8K`$4$NR23&gaBlM9Wic}aV%gd7&2^klB0QHjKUZI6thqU1wsG<@R5VAxET1E<B?h|;wUL*GX5A7N69i>VwgBxU?Yrimgado$4Wp!vWS~>naT8VIL(bQmb{ix1uKk0;1UgV$xWQ5S?<VM908l~;8ehmgH=?ljr$;u^Zij;6zN<|mj(0Cn1}OGn4u&C<Bf|Y_Hi8Z(r%)Jur>|Td01p?tYo&qn<Zk~G&{Ct$)z;(B8Z4ufCd1dA<4nEH#aEYElojO`7EGjpe#f9{5~pX*lcWNfwC-`OtEWWIH7S1;4zqd4yckyO-;MPy25qdH<GlVu0YHbV@ls~x=ad(a9$KBoMu6k7>g_&VFL*;5Ga*{n3G8m6G*gEXas0o<AUEe2_Bsn#+NWl4I((gxy+k~VCY~3Ub>A6*Z7zcjm33&l@omj<1tueymn~k?j0I#9OgOJhmtg%$oyl#JWp4&YK&T7l5wyI#@I%*3PxbLfVjm0f&)Syrnw2R$KyDN=C0X#?|uE&|8V~CpI6>s*ne~J@%r@5H9x;U{lvdtUtFH?!@DzxAN)T5cy<2v%)dUn;)bnHrytI)ug|=JWh&wD7KHh)un6KeibqYyau1(7?ok*2I!@Pi+~+5b+da0Os#B2NegZy=cSLN|qkDiRFY)g=_jvKbaXT++JuVfsKsxaZ$7p{{GaO3$4!R!H+J8vz{{rGZF}E>DXmLQT1f-Y8PRAa$CgBaJXJQ4;$nIq!1Qr-}iM_EN_SQgsW;{4+$N}R^wBSZIcgdHdU0vEwbeS(>yyeX<&vNNP9Rg`NNsEoa^W_}vo*0^CM!ky_47$T-qrt(j9pDF^x<f}jb*QW(wT^n~Qdw7OWymDW=2lRGK*yn*-(`g*zy)gNB}75J8LzRsuX;<HaE>+!w%J)ZHx5Q}GMwgiuVt*ffnWhLBAHkq{h+WOZ0Dt2qGZ933wm4)`!~A79T(qG@y!qerSWnedW0x~Z#B5XLWYjuh2A2(@$bFvaA@26Cq~tuA0v9qNJdy)Ck_+L(C%UZMs%Y_f7R)g(`O;ct#E=?bwK(Gj<)=686kvC?$s0q_YFy&Ftd2K8Ze+p@9mv)H|X|;dv}9g7x4CjJcptIDH~gf=XF__^56q&gv}UI84bb1ItdNK)h@*FJhyC=1q6^9N8tOd8@6BaP@PvE_T?3=TQRuJ<uo5}eUyvT$L>`7VbpfXQ9H~718wgI^gi?^(HQ%IIU~q34+Id<Zzh8<i-OqG^x!d3Fu`OHaJfGZ^O=QXY>^YGBpw0BuSBE$6>m1bI|ICLZ;fnbVq@)6W0fP&);>%2qUO${F^Gu@Z>z$MUVvn~Q}459fw1g<B>fwgv>VW}bxRXC^z*Z0-R|*()l)>IrI-dtX{rC1U4m>Jg9H|7yr%ianHLB1(Ig=HaK=5WWMTW6HP)<ax2=+mxm>pa1y6D>j`G5)*280itZ+1wP$wcMbXL-U=6FV9HRzH$I`o67lOLEs!5o;zRmit6>-`L>twEEa!v5`0WA3vI7AByR3`D@yREcTE9$p5Y+YnatV0|W}>LG^ICL&?SPz-{h05Vd)$3y#-2a4_<^psi^svbeIwuq8-&!y_IQonD9_HSOByE2GNX9W-k!b{+<F@BDT%j}Xg01%CQ%cnfr^41LPjhTVmk{Y-k2qz>h(uMWe?vJ1d+@c*$%&-RqBoB>K=1$0oGbpv0WqwSd)JLo-fGB396_CMT0=>1tg}Mnvc3+VcYK4{_pi)mle=Xd(aMm4X-QAGEKfd+OLN>kJ@r5EQ&2bANYGKp`ap=IpY2|!jtkJ18;Ms?AjD2Cb!6IGp9OH;-Lvw)LyK%7uTI4{X5IeD#I3xTE_7a=O`^VTZaw7EkO#cYVN6sYSz)|`jb#dy<qUMQJTNJHf5T|sI&LaFAmMcYJmkYa6_@D|qT!^!2xCz6+>Np1ut1{M+bL>2KPVfXx1<yx#I&e-<cF1K%cqUD!i}uf*V|!SGpT%c7kzomASy|~M9uy?3;ojp@n^YJ&JBVm*Jd8_v5pl~Xx9+hR`<45WiIc(T*!`vSlSB31K`-=Otvp?@1YTKCdV>L}R11fGl1i|2vS)mZjMH4slOk9?i}oRJ9jafgbOUI-jRtbSZfx*SA3?-+gh}k7w{>XrAKhcw<wZ==NAZR1bnp=6|Nof7Drkoo<(Sv=%m<UvP1{z;vI`*_z*e8|XSinU&>lNhptxrIlU(zec?P`m6xWP`JoL=J$VmgWTYLvf4OjYipLmLzIab>}K6cvfbJD*_k3V+k+3h^HLC@wDwlS`mSK8QQ4N=+73_KZSrAGl(5sYOr1xu^awAqN!YoW>Q7WE|a(8;IC<}oyAcO7h9Po4kHL$lgFf)R6c!c7c9f?Ba!=#^OPAHu1*mlv5uv)Fs4FK@SYzmzI46Wq=rLGTPV5<SC|=@6Gc?A0pvq~aK?-gRUu7{=sQQqBSL1{h?ePbRQcftXa|hw!oCPcTMdFb6`|_A7Unq2Wy-p{Aw<D94Z~wB0mB=(&e4_pwVYgP4Z>3RY1n{O-%6HaB}_6?-tP&`TXsAaM5(`+7u1oO|@V_9TPg$;KLK-?^nKJv>&W!;)QOKz*VRoLT_0SOq}=O(J{Mu_8U5W)n5)k21^WO=bbNd~R|Jc!mC#bA}K|SXWeXCEIbqZXrc0uW3^%ViAEweVDzl>F>zrb01BxrFze)TDe2SDWmsUTwi$@P@4q5W=1i~!jMe2@r>OvJhyTUnf4D5`X;$BWIsjon{;*D5wiN#ID?Xug{3pC09KcA!2UEx7B>Yz5jdQ<IcKL6K@I#DGpw?h1u&MO=77)RAetDHAiFh+bm6wh6POe2b+Cv-82N5j2&}XHN@9n-5^m>Z^*Ze9LrepI+}$e)j?M3Z)y^KAcD6>}`UC%N%Y&TzUmSj8+5up&5O*F`Sh%8-3*h8Je26uV#}<_krie%m9P^D9l{Lp{-9x!SE$m8+k_1)k_+wF_{Cb<X-jWtHr4kk$jTZ=u6BZU5exi*o8;zeI+ZzQ39h~p2hQW10686DsyN3tIkST}HZu{r}1)VkSe;jyThxHPp+b4|RjgIMQ@~SLefB@P=0er&Le!JZhej;&Hd+hLYd&i4@mafD8rgppcpv930ueH5b({|hBYI2W6GClksXuSVvaa23BYOa5xI3=Bw2d_M`HqZNx!=8VM#R#!g4*Dp;0uqV@C=WE#AtX?`oX+@gRum|5ipWm9z~YsjM41|>bkw8AG>DSCU{`nP;f;eN+<lV$u%NAprA~Pmb@<phVq#`5s2-d>7{sg|&ysRX%Ab2`3{VI89c37P-eX;+T#;zaLiLUumQZ^^M$=-3Vch2j*qfc~Bl;34=1>KMbD)a52gEbK8rKvok<G{p3c|DrNCO%|^o5+oF}usdjD5&trY7l}gK3K_!oEU0fPN-X<hDxp%wWN^H6_}5@2-M)8Rk~y@R<%w-P9Zo`&Yl8zq|It`fOVm+gc2wVdWlDP3^sT@bE~Ly?;<?qJs`8V0&1lh=c|hy^ZNTWnwT8kAc`yzHU~jcXwD6xtR6T1TR#^y@st#*S9jMYGd%roqFLhlrh0By?XB<uV+N@4Ad}n_2_M2YHGrQXtZXb8eGs3Fu>%g@8Nl?Z=+0iW!G~U<jXAdK~T}y*MXbTE$0+j6p-4Tdmo`zllWDB!aS^;cedxz>w5?ioE$4nEQ=H>XI|gcZNiZ@!_tch3scDDprQ#H6Nb}4*nVD4Pfi<d+$11wythSiY7FlPgEZ-?bhj}-!z_!!dp{qOhHEljN}EIYNQH=${V^i*Lr%-0<h!<tM^WsU;!M>DL6lMWMLM@xDI=>koKvibSujm+BrFq7Oot})c|ty3N{l-aT=ID~zZPQiIV|QY`^R5JIYg^ZaCjsZ?AE)BH-B7-QBM{`|Kjrc_Y3a;+I9c0^GlHB@8@s+`SI-P%7f7BoV4DY{_E`W^ve5c7PIAilmt<1_N-&~xzj#zkDOx{;>WxT+8ioHO~+{;IS1~Ml#*0M;USBs=TZi3jN5g{Ye5C0V0_CZwT|}?k{oX2-tA-OkSCgE!CIy|yxUPjBXLFh(9son6wlISSQO;Nd$9}7MvDf_-}-_A|LV=@hch7JTMIJw^@p>MZ_h4`PrsjDosr`}1@=dawKJk!ldwPS?XrlVPO17oA^Ov-QR$9Wvw}2o)#&w~zhC3Eg~42Cfo?kbjBaioQn0{h+Lr^wygK`E_U0O=UZd$GBx<vkdFW5$bQHwiyCBwP?wn|!eGt@Z5)^@}o$k5a+b(mna1Mpqn%gZ7VS3br{F%^4TrTPJPnXU!AEJN=F?aKIUWBl6{&jYJdH%-S-3Bxt`f}uXT^SzJC6uaxLg)>i`R4C8z`O20UXLM;TnUrr9yY8|5rz}5`@FSLNO%Y)!Gg{<pSxmqK}mnB;UrAbC@&i@%2qMqOq#NMh=X;Q<-Jw>R8O^H)FkNyz}6>Ji=;{t4ipw|!laszu@+2V7GMm|e0Touv$y8X7T(b&0;72_4J%x8MhO;!ef7*wAKy0yX|x`vahj<)FW<jDZM4Q<bH9L^nM+!VTJhPxKY<?4-a=f+_L)7sf8aCOGqZ<Hb4<M-W{<l%rXW%wu_~_6T~!UZZiqe#bpVx7Tn$#?v@EM55^xD7%VM*4^i5)>X>t=yEjsMf!B8z`2Z7eswTnXQ3;jM#Ze!tb@_Ym}tDTMc&|B>!;+<%0kZuE^PmypF&yUh_4fDI&$YxBJK{ml&j6J<AT2~l*o~AZutiv1Q7N|QXGpf|On2;T|HgKGh_6sDaSSGf3?(GnGNqEm%o!y_il!78l#5f-RL}|s;bgaUzoV)bulNjfx+?_%vGCx7f9!DUAiShdC?K?>7g&QS{Wswie*U;jPH#DF*gv7oHmT}>;ilnBgnqCt435@Wqmb|c9OHR0mqw!WlUVE+KX}p*PTdlfot;sd<_dLou5#=w=ncM2nsdqTjjjw<QlIgpe(++7%21iQ$Fj?Tx57Co!MG{w(HAkET4k5=a9eJG=G^C>1G&%5O%g73C8nK+dw&8d-9oA*F;4ee)<xpV6TZ?9~`}A{Q62%pMG=V<N*>|d#RSCZ|=TK|5|29>nQqXD&80wi;q+aRcSi_R^bhA<(>xP=rE=8T}tNJQe%*Z+WF{!25sWh{;wzeB7cH~0HB2b(HLwL@o4alHW01`@VbSKOCBDWOtIXRRP|2ACbN{8eWBgz39t=V$`m8fJlWt*w&0%EYR#$iy5!VUHcT~dYo#hU7^4I|AN3>_43UVu5|w#&tYJdt)k-Aw=t!Th^>n_>W!PU#UETE+-sfPmvspiRvMEcV3Fcv49U7B)MG$38*jQ!)$0g*BS1>;+M(&^cfmmc}X4`Y0GSB>2Tu!-^QOLl0}Kq)){gVyZYdn~qpCrs(uEO>*)I>5e|-BtCdk5j+fFIi~3hfJ*%e1Na%46ZL^?m`g1q9f+V$fEu4dI3Nggl&3!Ly9N(Pl<imf9H~Idu+|0!fFvvPIq*DFT0))WtAnW8-OB3h^eb@2vv7RNWJf|ar;Ii69QjpyMTsffmIQ6@>Ag*vhENzxIBkTyA)y=LfC`f6CXFY&CN|E|j}vEX%H_d`F4KXewODyHO`vx&d(^gBhL@J)(5)av<s_W)oP`TY3|>`P1{B*fRM*X3c4+_;z+Q)0A0SluIy9))aj-BI!<kU#jf3JETKCwPd~Aj$#`T7OH50bS)X-+x$Lu{m99dU{8igo-erWaxATvo5jboqjYW4_N6Oe*+iO&7n1StIm(0Jnq0>IEyW|I33+xbb6n}u4Cc@{nR_h}YS{uk7tv{HT)kXpz<#)y}yD2wdxY{AgM@mixek%&f<5(m-5+JM#`dIL3?WV4NBCie1L4WJuff;F)U+patp6}-dm!OLote)VA``?ILXt+Ii$a3&<DsdU@_TsEWFX4v&~Za_ag;AhHy>CaT8f8vA(MAwB!xpraKnE^9~${awk{c0-<CrVaccOP~AJm&!yG~kj4$a4(v3@!S1Y66smU2?Hg^~AZ8S~cB)dY37eDse~g$i~}pZ}rOS?o|bNdj6_-b<pV%7RvOQ$~8pAk{l2v<R9R@b=Z4Fxck*O6(2U?zQUOVSU#<b8B`+P^^+r%C7hjn`thyA;o8^}5>`>Mc4?@$AQH;g)!EK%Vh@IZQ?4nz&1ylAttEzw(OlyXC`}n9A{%3<mAS!rLvE`A#(RuJZ3uSnG0K!B_S1Pd4WPVro+1w}^&|my0j+^aMLmr1(2oOeN4jV~9yN+bl)u`K$Bp7KB}!o)7&TrTJc~!q;_;qNiPg`P3iK=v_M}6A=MlOv{CnPk<dT3(k^=>R5EkcPK}sf+pXL#{a*uuMNO~+Hn__X;qbRJnq>4?DGtuf&sF1>$2QMjrbZ~O$;O(T#Z%35Ed~isKJVQbjv)j{b$>D)=jv4@(KuPS9=T(wq3+F{mc+qIK{f`4lROQs2c9$9OSS8%6#dw3RLkSK#a8Ck_``qtrOn$pg*;vkVV`q|@WmYt)iJl|1>$Xrk@RtWuP~aSgjp^JwdK$%8c1xJehgmRTj_~s^zA3`IVd5>E6y^uz_BY(?mA|^iwz()QAV^-D<mqkIsu2l&j{;GhjG|teJvkXw4=Cr+#D@%E!>vb%h0UH;Wxkq3T1pEXbFI(p71vAT_(SPS=MY3sN3#_na&_fTC;D1=;%c-M2ajWQwZ<doxU4i7!pce}eu65j$6DBf!=WQ}qg{2S@x6htpv2`y@u(~==l+d+%3a4Y&l8w~(Zt}DnohYyr))}$PHU`i%txco&HOoZj)<XhOsprGFXvEy#kBFuF{oMjLi&Rswi+@pdx2w)pnA}zsqT_Hu#lOsZv@3Rj;qb0+;|<c#bo5+l*rZ)9Z5&ZVcx`X?lh8<*c@>5O%0ObLGEBc)rxS&X*xW=p@<`tphEb-E@3pChS?%x_>D5MAI=xxqft5m*I+>EAOVPcnbEAE?gVQMVcfBt;_!l;BSiNq&R~q_)({pK*DlAg(d+V=R~e)=1(r$ui?dwN0SJ4nW($<r!%wRwM5e2iH~10dXQ%4ZA7`GmT2cBPes+eotMd9+biYB0L>r(u5y`-X`=$Lwq@=_fR}hIV<lKo6YUX}<wp{$y>D97mzm_&B(bItGZe>?G<!Uu_Oxja_egJyQTybabAAGCy2THsB)p#fS9X=2h==)&#EM3MEm7ybBGtGj<Ow#lz0G>lxLI=47CB&J_#!za2PgBbk56Q$DXB&4!c3k9WscdOJp(!1eZ+FOnO)0DVN~wyYMyeuRD>2Bjlkz}Ws4B2Y>5e$MIo)x@>5jC+Q1CtK(&v6e6*N0hA8L9!*O}AroKO#gDhK~~DEh4jGbXvG0Ke0!1&#}ww9c)HkSp@Yo8&r+yC32$)Nd*aJdgg%3!@&vr}vz~ra5Pz%0Mt=Ci%WK$=f&*Y}P`kXQNkGZ8#Ad8FxCfJW?6ul1W)++7In!zGW>5pJL#cq%8UEK+;$`EjI3zI4REwO5ZW`)h$H}aSGehViq;-lzyGngTXp6oVB4ls#~JaDc@EbZ<LN|a;g?zbppXQ1p--nvh6Ga`kR75ZS>P30e}t!Zc$4AFKi>VO(pk}SimwClq$ljuOz`;LlCgJLDWS2aaZ!k9q|Xh+H`4(mb)n}?)c!UxZVf?uYo8+q&b8l*dL8{)QwOFRjtM61bYZ7HXkeoy@O!|HICk9(MYW-;QD}{IXQSVs@w-O*l!*t(}(ARashoU#fFZRIrO3#oaqyYlOvH8*hzYyD2gIJDXD|#q&!Rc=A@tA+>is65DwdJ;YqH<&-5beVu$7-m>fC;%MJ}hkU69?YPYJV`#;rSR8G(`Hu!EM4G8EG^Gb>Ja!Yk{ja!e=3MDU?eD=PIbD&2`yzE-#xe`wnXLE_#vbQmN5B&$91%8(h`k6t6h9>2sS~=R-tvrO;L=#c&v)wP!Nh(sDD(sfr%Arz~=*&h94Mt^rHN_sbscnyb@X(12qY;5o%Ipx##ghs5)9uSY5|ycnGf(`$rc-Ot7BKYn=DL1QfDq6CjLFn{Tp#HW=k!a)A>X|w=}PkOAl1z|Vg=GmI|s+=t{QJqUxU*0e~FG?9{BXI;SA&9arRTnPUW<$M6_i2u*1bGsf;i}J4S{e4EVxQ+WV%kcB;}^*uf^|(P?9N<r7}54wD#A>?q<vYBvlGzQ0U4c$@=HYnzx(Mmfn9yt_#|QoViEo2^#Xuf+>yx28~=cdVE*lQ03K`YjX*j}HT*G~WvGB!tzaMAi`0&S&D!E`kidK{MP?*tPgip^H#NyiaJVa7QH?W*|?wc&Ktdifc%eHiSh-HwQW^T<pdsUEBB7U~9j`O*w+ynp577A5!3k?Y7;yT3Uwuoa3`8Z0y#yB3_PAwR?QPew=y(op)7Ju(uSPLwnetMQE#1x4zd_LSWuNoE)<VUD|O<3f0S9?OU}}GQNPtK9A=rK}#{|EAI&WE|+~qnKdVk<tIY8YKldjY&NKd?iD6(v0j93UJ%~M5onp$XaDw1yOOS36T+JPn93FZ34b7imPdIR2E|I2Y_*}8u?VwyL?0+Hx2DaBd<qI-P^c@E0EQIuE~;3q%%qysRw%U_6G+ltY0qiC+=yR0RovOB1*;tuWp>Q-i%a~xT7+ZH=f|t@0aitf!d+2jN?s3&##?>ds~L`qs=f?7YjAc%qS@T!Aaoh9W~Fp9LaiI+n<>OQZ=;{s)kSCS#DZ%U<Uvtn7MD1tPw7oQ?K>;)^&zAWh9L!~F{?RAmyj|(I|odMwpX$aD924S0SFL?pXzR>z$oLW3xDA_%_g~}qMvrtZ^VqPDp_fNDqgk9y`PgYKdkL<BX?XPm)*=OQu7~I@#}sf&L35u0vJScQ9c^(kQBB<te-YgKL$l3o;tK^7qW9!Uo4srs!F=dunh{wp2juHNoWsJd$aJ=XM)^(791R(She{2<_L~_5d;TT?pYvV$LyK5?Lzj0=Pf+V!iPyTC1)JYhRwuKHR<;g2H&3Pl)*-zbZ<bB@L@02y+}8c;MODIS{+iSp;w^<(lr3$welqlKaGnUOQ&;qlx%<T$MwERIY2QgN2cwl_BuQ5{fF14!(ro41@KwJ(9PDcA?okg`gkp|<+2E74ZFPZ&2qZ;9O$T>%5Nyqc0ZR~lYrvCQ9>Z^fLnIW9g!mt8`QcByswfXV)i&a#4$(WBs4jh641FSd&S2fk|I^9i<QUUtitsiQKifP@^8{sD`cC!YU42tAC2UdlBcSK6`)?6Rwcm$mCPciWmF-4jMt3zQl?ju2+}K;s`iD7B?9dix{E0BzG_Y;PwI=q)9fimVV$04%=z*r8FmW+-t2WtKY8U@SE^CzU^jb@JKr5s+^40*wP7Bay^UAL+|-(Y#|`BQE7Im$soG+UN{1^Olu9tE%M`S(v}RhUf=TcoRyC*7DO<u(UTi3-bOobkCbBvx5d+92UxWoAQi%~7T!8?VDeD`;Ws9?1%BAy1>w-l1h6r&?N|55*!xaFj5`k`_DORphe`xQDpjcuJCU$SK9EVx?fhU#UE}v18+5&oS!5Rt&d`!vWqbcqJ%kBw$cR@P~2_G&ALjZZ75z<J&)Wzdn;6(g|E$_hIGygXlsyhosz}Z54B{x!OA1vVIHoI0(ER#^+YzP`lc$2bGH`o{zD(`^R2c3i9F4kNp*x_VRl?3lDusR9lEj(J4d`3n4HWv_qFs>;DO3n^C3<=f&!8nA(AfW;(70HqB*S_br|CPnaxBb;u^_8}7`(J7JZv=Mq1vcn{^h#_Ze)&{_^4$cnc$@%$vkBm!z>^YNN=lhMH7#TTa4=1YUkHn&x&Z`+_@5E+Inl&|(GrqrT>mN^!CI_iD!mV~d3y#8e4GVf-bs5E#WA#6>KGN&gugyV$shSRixzCB^=e<1BQg|0X7<>MA|LU<e82!}{QF`K9jUfCXzH1B?AlKWS>79LN5pMPl9$^cm;#z@m{5MLNgq?oNbRIg&O!AC^MJ|?#d(T0pC;_d7G3{poB{d#A*Xo|@57{y*M<-s85!w~Ty+x*RE{$K-de2h4Cs5_LBcVihyn|I`2N4RM4;Qr)IWU6+kKTdShFgnuR7g`c~Ul;Ji0b;^}AV`bCr_gdDRi9KFwEGygaX=RhjQHy0rt9!q8H;5@7rC^*oll#;4bp2FwP&7H#5KrwmV;swQ?>ESki=r3BYwLFJe<rML{GBEJ>bLU{u3x4ssREv(*bx0AH3qz&U|4FxNkuE-KZrJk(K38nQ0oN1{AW1j<smihkdf^J{@?O&dqzWv*DgwHExP)yUOK_IURt3#yt`t1GrN8|L5>)$Uf&;R@Et#N&Rc8On?a^>aEZr_ljgG?PGh)Ke%jS(4Se3lqN(LHz}5h_q(<^w+H^}*CpmR5P0ETZoQ1XJaAt=6J1WJz<h^K_NVN;!{K1*7-6{DCUnrZk9j0e{@9MXT^XU0%F9|8VA&Z~>`;?soMJ9d3F0;lssWe3L;ww9{U7&7RdgaR&Hzc;K8I4Q)w_kHZJ4MCm})e3L=0&Og3y%tp^`(TCbBT-1CY&abW|`If%Xms?wXsBxP-wh%{yA!(l6?*hX5@*KkQ$<8Vbn8Jq{efbe%eEn9AadmzA@$Kp5TW?Ui<yE`ZRo&$(Z*WyNw;K1ghD678TvtgL^-|jJI-Z%8iNYyAM5wz#6`L(aadZbecX!h&?IWjq!W90uHj(AfF;af%U{yj>HYhWg)ku5|U0sG_NN)ejt07DLOORX?8jdJaLxj_+xz0fy3By5m_$aJI5Dx9PI6H~L%W{Z0o%~akl`)K}j7w^iXm8x0OiJK10Z_nIMyW5ibXZk$G4Iv}?$x(gikb+kSE>CPY+mTwyv6s()xF*K^?*ha*hK54GRtyWakbC+H8s>jjp0w!Mqk)W^vjzEIO4BD%1;bq|K{LkJU%(;c8|jsFS;+gFD9LX(YPB1&tG(29v_mkt5l-vcboX5y-QJJ1}8@yh=k5iRtFQ1G@qWCih~WRnXe(in-)Ults<&t7ogeu`t4gKQ`I?6LLs;KrxK`y+70&8ACsdtTid2@IMvJ4rVVOk!*5kj+W)d&QnpTpJLu%w=7nJf^OaYUttPwLC+`@_a+Ra-hU_aUl^X+3uCZm*t_A8Cg15n@?1O7?I(d27$@c`Gawdshikjp*v#4f2AOLpWY*fEnhQ8%AC@-1~tI8cjKiDRnA$vOaOg37o-q1QfzJ2PT-@H#)QMLczfuj45)vlkcU4$9kX8~MZx6@Hmuvy%^RaLKQc*@E9Jib-#hGBUDY4>d^^;H-7*R@+eKklRVnOuGSRBnyy+mrmp*CR=z_srAjzs=T7I$q{FEsyVEiwaZtd};0Ld{?k#Uh|%ori;jdAevjLvq-`DsY@9Xtj^=TpSoFEh+GSoahQ1)&)u$?*>o|5uKe8kcS~53X8XS(bN)8DocmaIEx|ISoXq<$bI90K#`Ql#*j{wgx_w07q&w+!_=9xjI~aE+eXOp1Km~^<9l42ZnU~Srq%YPTIe0yKK^MTufNq!_oP_36e3>l)^AyUf>D1S!@Be70q;%{{Aj~sAsXP4U9=+>J7-Z2;*B&oJm%&J;8Qz{>{nISVutJZ1^eg-}ji_-zS8*6dyN{P$(4e>h&l~P#at%)<>*E{vwNjW=v()FC(H__7+f3Zu!><w?zSdHHwZoUZ7S3IwMI2y9O0@BX`!>b74`GN2f$suaY8sF$cNWC1FOJUE^s#G`WuKhfWH2hHjT@8}e{1>R2>*^L2S!cU7)p8br|P@MQ7}!?oG#SmNwCOg&~fVbbLYK*6*)TeMW%Ih6A`sa$tcG0Ukl@?;tfvT2;J;zuocPKJ&N4esse7cYg<1UUepn~ZGgx@Qk%@Qhn0w^1j)Bns{T5HUkhc>kls!_R?X?F=a55b&*H?8rqr>WLG!j*b>&Mn*4Ms<+vzM4km4`W_%%Sv;Vu1%y}6^JkTmQgOQ~Hj{E5h|{zfl>?rhPCPyFaGYWYj9Jdu2WR_7j}ADf!BFzVZKDOH%2Fhj}h{Pzqvh-#?HD)uPRrP}CQ<m-9WvwXR)LC)msr~uyu3HLA7`_w>x>AnU{<1kYJP~JGlVrn2ym0XLeZw6P@x1i>wX%K?4RP-<#P;!Q{IC5&RHObE96cbBt9#cC5&`TeY8gt$D#*w|yS*4qxm22C+M9DvE>)Oc<KtF-OTk{i~;dyG_QlZ?*mY(+*?Qh~x{8zM_ZJv0)A{yTIeIaP!Jjnu=zp9W|$phbWq1EQAkE8!|LUsAL>0sM$xYsCOGGOnpsIIk@b5^up8=lQKa;)7D5@6*kKbrEfG2!!y{c6R`2|~@A&NmKNX*BY-iNB75L~1)WJMb*KoqXikQ>dx;`PL%)&fD~1>~P`ja9`A27nnti9BSCB6MZG(dp~)WJo&8w%RQ!V0m(ngJ7pWp`+8fNcDKXo)92QcHv3QmE=S~l!kuJ`=?Tm&M6=l8`&1CuKT*U*_4$Y8I2;3JcUrz<7*2Jp!_Cf0jg`l2Zy0f)2uf7?`mHZPG=3x^SD`h<R5fq15YNzi%GE5X)-r^pm2sB2yA5PiJg!NSM1xX`20Y5vCtWsu_g2klgwCi|rLKGH*!d4h5N)$pl)?6$QEdG6BdyhzCL^y|LMRXsajfoFD@-du)aAEooOS`bqRLgGm2wUVZ*J|(A{x_ibxKv|cL{3q>)eyPE<-rdsG0hkAE=@_<9_~KjhMPXA-<n)X~Z4+8z-GE{biHxG4r5d7+V+F>A%Tx;ib^o7i+pfzFhExp3d8m;-^1;fKJkLQ^n`in|oqI_3OAP(-)~@4N0|fb&Fm<ZJ*t{s#N#;xh%IjFw3^JZwNHb=Z<u__o(eWov`q4pj+{hTrPJ^`nuV>OGq@@0++v1Nx5X+=2y>9MH`cau%*VKxFMt{TtWGloOJb-rh8Ytb~y>D!J-`S<%5g2?pNa!jEOCQFb^oUN8+DT_6)fSM=;}v;6GAUJ8$K}&pI~}x`YD_i?7RII1cwwRPY8Ho!;{wQsNc2HLmoK929&Qha6XBPUTo51v%-4uwWjDH29)sweh{JZ)~U!fuXH4N&RI)1f_4ltAmPSZF(G`6QNwXhC$XUP?_bP*XcDs3Zg$UhBtk^=6+t!u$0?v^Ian}zf{IFrB9+C4;v7qBkcR__l?`q1x;a7>eBRGC50#D<w1=ibyjPppgS^UA&-AG3qSxLQE;&=aB}}kf3br;x%y~Zo$Sc1zUK?$3%q1_Cj|=x84dkXo{|2D3SEA!TwijN&>U)|x*?MuQ`h^CY3GcVl3;eJ$h-MnISOW!4<yX?ANCURJ!rzrf6zZjqTxpzgjf6r#c<&FA9uM{-@4o7az(A$p!%t&zD`;?>G@L>jXd6;3A516?}nVKq}<cied{jJpLqFN>O^vsn?3d5m>YRWoS()Ijv3OmN2uaum+ga}|DYm&RkD%5p>vc}0>vVF2xIw+c9cOuDP?U=;i}S>I2x~2mR=QEZ|P{g4zY7c-G6iOuTLM&uFoC~vA6yQa>-Ll', 'offset': (0.9375, 0, 0.4375), 'rotation_quarter_turns': 0, 'seat': 'WholeRaisedDividerPlatform'}]

def contact(a,b,p,z):
 CONTACTS.append(dict(a=a,b=b,origin_m=(0,0,0),u=(1,0,0),v=(0,1,0),axis=(0,0,1),plane_m=z,points=[p],minimum_patch_area_m2=.000025,interior_probe_offset_m=.002))
floor='WholeChamferedInspectionCourtFloor';plate(floor,[(-1.600,-1.400),(1.600,-1.400),(1.750,-1.250),(1.750,1.250),(1.600,1.400),(-1.600,1.400),(-1.750,1.250),(-1.750,-1.250)],0,.0625,'z',0,'Whole common court floor under both whole stations, no navigation proof');FEET=[floor]
deck='WholeRaisedDividerPlatform';box(deck,(.300,-.950,.0625),(1.600,.950,.4375),2,'Whole full rectangular raised platform supporting entire unchanged divider plinth');contact(floor,deck,(.95,0,.0625),.0625)
step='WholeWideFrontPlatformStep';box(step,(.350,-1.300,.0625),(1.550,-.950,.250),1,'Whole broad front step, side face meets platform without overlapping skins; not rated access');contact(floor,step,(.95,-1.10,.0625),.0625)
rear='WholeLowLeftRearCourtBoundary';box(rear,(-1.500,1.120,.050),(-.050,1.195,.225),1,'Whole short low left-rear boundary outside separator footprint');LINKS.append((rear,floor,[(-.75,1.15,.056)]))
REUSED_ASSETS=[]
for row in COMPONENT_SOURCES:
 raw=zlib.decompress(base64.b85decode(row['encoded']));assert hashlib.sha256(raw).hexdigest()==row['sha256'];E={'__file__':str(OUT/(row['label']+'-embedded-original.py'))};exec(raw.decode().split('# BLENDER'+' PHASE')[0],E)
 prefix=row['label']+'__';off=row['offset'];rot=lambda p:(-p[1],p[0],p[2])if row['rotation_quarter_turns']==1 else tuple(p);trans=lambda p:add(rot(p),off);mi=len(PALETTE)
 for name,color,rough,metal in E['PALETTE']:PALETTE.append((prefix+name,color,rough,metal))
 for name,g in E['G'].items():
  name2=prefix+name;emit(name2,[trans(p)for p in g['vertices']],g['faces'],g['material']+mi,'Reused complete '+E['ASSET']+'; '+g['role'])
  if 'face_materials'in g:G[name2]['face_materials']=[i+mi for i in g['face_materials']]
 joints=E['LINKS']if 'LINKS'in E else[(a,b,[p])for a,b,p in E['ROOT_WITNESSES']]
 for a,b,points in joints:LINKS.append((prefix+a,prefix+b,[trans(p)for p in points]))
 assert not E.get('CONTACTS',[]),'No untransformed contact records'
 for name,p,q in E.get('INSIDE_TESTS',[]):INSIDE_TESTS.append((prefix+name,trans(p),trans(q)))
 for q in E.get('GAPS',[]):
  r=dict(q);r['origin_m']=trans(q['origin_m']);r['direction']=rot(q['direction']);r['name']=prefix+q['name'];r['targets']=[prefix+n for n in q.get('targets',E['G'])];GAPS.append(r)
 for q in E.get('BORES',[]):
  r=dict(q);r['origin_m']=trans(q['origin_m']);r['direction']=rot(q['direction']);r['mesh']=prefix+q['mesh'];BORES.append(r)
 for j,p in enumerate(E.get('AIR_POINTS',[])):GAPS.append(dict(name=prefix+'OriginalSelectedAirPoint'+str(j),origin_m=trans(p),direction=rot((0,1,0)),length_m=.0001,targets=[prefix+n for n in E['G']]))
 for name in E.get('FEET',E.get('GROUND',[])):
  g=E['G'][name];polys=[f for f in g['faces']if all(abs(g['vertices'][i][2])<1e-8 for i in f)];assert polys;f=max(polys,key=lambda f:len(f));p=tuple(sum(g['vertices'][i][k]for i in f)/len(f)for k in range(3));contact(row['seat'],prefix+name,trans(p),row['offset'][2])
 REUSED_ASSETS.append(dict(id=E['ASSET'],source_sha256=row['sha256'],unchanged_scale=True,unchanged_material_parameters=True,offset_m=off,rotation_quarter_turns=row['rotation_quarter_turns'],new_model_count=0))



INSIDE_TESTS.append((floor,(0,0,.030),(0,0,-.1)))
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in[0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
INSIDE_TESTS=[(name,add(p,SHIFT),add(q,SHIFT))for name,p,q in INSIDE_TESTS]
for bore in BORES:bore['origin_m']=add(bore['origin_m'],SHIFT)
for gap in GAPS:gap['origin_m']=add(gap['origin_m'],SHIFT)
for c in CONTACTS:c['origin_m']=add(c['origin_m'],SHIFT);c['points']=[add(p,SHIFT)for p in c['points']]
def measure_basic_geometry(vertices,triangles=None):
 assert set(vertices)==set(G)
 allv=[p for points in vertices.values()for p in points];assert abs(min(p[2]for p in allv))<2e-7
 assert all(abs(max(p[i]for p in allv)+min(p[i]for p in allv))<=4e-7 for i in[0,1])
 bounds={}
 for row in COMPONENT_SOURCES:
  vv=[p for n,pts in vertices.items()if n.startswith(row['label']+'__')for p in pts];bounds[row['label']]=[(min(p[i]for p in vv),max(p[i]for p in vv))for i in range(3)]
 assert bounds['Spiral'][0][1]+.25<bounds['Divider'][0][0]
 return dict(review_scope='basic complete original bounds and opposed full-base supports only; no access, capacity or operating proof',mesh_count=len(vertices),whole_instance_bounds_m=bounds,static_two_reused_models_one_inspection_scene=True)
FOCUS=(0,0,1.28);ORTHO=4.65;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(5,-8,5.8),'qa-front':(0,-5,2),'qa-side':(5,0,2),'qa-top':(0,0,5),'qa-back':(0,5,2),'qa-wireframe':(5,-8,5.8),'gray-front3q':(5,-8,5.8),'gray-back3q':(-5,8,5.8),'silhouette-128-front':(0,-5,2),'silhouette-128-side':(5,0,2)};CAMERA_SCALES={}
# BLENDER PHASE



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
root=bpy.data.objects.new('OneWholeSpiralAndRaisedDividerInspectionCourt',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole horizontal bounds centre; full opposed contact seats for two entire accepted originals';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
 trees[o.name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
 actual_triangles[id(trees[o.name])]=[[tuple(float(c) for c in (o.matrix_world@o.data.vertices[i].co)) for i in t.vertices] for t in o.data.loop_triangles]
def triangle_ray_hits(triangles,p,d):
 hits=[]
 for a,b,c in triangles:
  e1=sub(b,a);e2=sub(c,a);h=cross(d,e2);det=dot(e1,h)
  if abs(det)<1e-12:continue
  inv=1/det;ss=sub(p,a);u=dot(ss,h)*inv;q=cross(ss,e1);v=dot(d,q)*inv;t=dot(e2,q)*inv
  if u>=-1e-10 and v>=-1e-10 and u+v<=1+1e-10 and 1e-7<t<20:hits.append(t)
 return hits

def inside(tree,point):
 # Actual loop triangles with Python float64 winding AND three-ray parity.
 # Duplicate shared-edge hits are one boundary crossing. Uncertain cases raise.
 triangles=actual_triangles[id(tree)];p=tuple(float(c) for c in point);omega=0.0
 for a,b,c in triangles:
  a,b,c=sub(a,p),sub(b,p),sub(c,p);la=math.sqrt(dot(a,a));lb=math.sqrt(dot(b,b));lc=math.sqrt(dot(c,c))
  den=la*lb*lc+dot(a,b)*lc+dot(b,c)*la+dot(c,a)*lb
  omega+=2*math.atan2(dot(a,cross(b,c)),den)
 w=abs(omega/(4*math.pi));parities=[]
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  hits=triangle_ray_hits(triangles,p,unit(direction));parities.append(len(set(round(t,8) for t in hits))%2)
 if abs(w-1)<1e-5 and parities==[1,1,1]:return True
 if w<1e-5 and parities==[0,0,0]:return False
 raise AssertionError(('Uncertain winding or ray-parity disagreement',w,parities,point))
inside_predicate_selftests=[]
for name,p,outside in INSIDE_TESTS:
 assert inside(trees[name],p) and not inside(trees[name],outside)
 inside_predicate_selftests.append({'object':name,'inside_solid_witness':True,'void_witness_outside_solid':True})

joints=[]
for a,b,points in LINKS:
 rows=[]
 for point in points:
  p=Vector(point);clearance=min(trees[a].find_nearest(p)[3],trees[b].find_nearest(p)[3]);assert inside(trees[a],p) and inside(trees[b],p) and clearance>.0001,('Invalid joint',a,b,point,clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
# This Blender segment checks closed shells, finite ground faces, contact areas,
# finite sided interior witnesses and export fingerprints. Complete empty bodies
# and whole-surface nonpenetration proofs are not claimed by this lightweight asset.
def horizontal_triangles(name,z,up):
 o=byname[name];out=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z-z) for p in vv)<1.1e-6 and cr.z*up>0:out.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 return out
# Finite exact opposed shoulder seats are graph edges, distinct from overlaps.
def clip_area(a,b):
 def cr(a,b):return a[0]*b[1]-a[1]*b[0]
 if cr(sub(b[1],b[0]),sub(b[2],b[0]))<0:b=list(reversed(b))
 poly=list(a)
 for p,q in zip(b,b[1:]+b[:1]):
  old=poly;poly=[]
  if not old:break
  for s,e in zip(old,old[1:]+old[:1]):
   ds=cr(sub(q,p),sub(s,p));de=cr(sub(q,p),sub(e,p));si=ds>=-1e-12;ei=de>=-1e-12
   if si!=ei:poly.append(add(s,mul(sub(e,s),ds/(ds-de))))
   if ei:poly.append(e)
 return abs(sum(cr(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly))))/2 if len(poly)>2 else 0
face_contacts=[]
for r in CONTACTS:
 def local(p):
  q=sub(p,r['origin_m']);return(dot(q,r['u']),dot(q,r['v']),dot(q,r['axis']))
 def seat_triangles(name,sign):
  out=[];o=byname[name]
  for t in o.data.loop_triangles:
   q=[local(tuple(o.matrix_world@o.data.vertices[i].co)) for i in t.vertices]
   if max(abs(p[2]-r['plane_m']) for p in q)<1.1e-6 and cross(sub(q[1],q[0]),sub(q[2],q[0]))[2]*sign>0:out.append(q)
  return out
 aa=seat_triangles(r['a'],1);bb=seat_triangles(r['b'],-1)
 area=sum(clip_area([p[:2] for p in a],[p[:2] for p in b]) for a in aa for b in bb)
 assert area>=r['minimum_patch_area_m2'],(r,area)
 for p in r['points']:
  down=sub(p,mul(r['axis'],r['interior_probe_offset_m']));up=add(p,mul(r['axis'],r['interior_probe_offset_m']))
  assert inside(trees[r['a']],down) and inside(trees[r['b']],up) and not inside(trees[r['a']],up) and not inside(trees[r['b']],down)
 face_contacts.append(dict(r,actual_opposed_triangle_contact_area_m2=area))

adj={o.name:set() for o in parts}
for j in joints+face_contacts:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen=set(FEET);todo=list(seen)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)
supports=[]
for name in FEET:
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.000025,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
bore_checks=[]
for r in BORES:
 hit=trees[r['mesh']].ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0]
 assert hit is None,('Isolated opening capped',r)
 bore_checks.append(dict(r,actual_isolated_opening_ray_clear=True))
gap_checks=[]
for r in GAPS:
 blockers=[name for name,t in trees.items() if name in r.get('targets',trees) and t.ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0] is not None]
 assert not blockers,('Actual assembled opening blocked',r,blockers)
 gap_checks.append(dict(r,actual_full_assembly_blockers=blockers))
mount_evidence=measure_basic_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],9) for i in range(3)]
assert abs(lo[2])<1e-7 and triangles<=5000
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
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'mesh_objects':mesh_count,'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,
 'components':component_checks,'connection_interior_points':joints,'all_meshes_connected_to_ground':sorted(seen),
 'single_prop_count':0,'new_model_count':0,'new_scene_count':1,'reused_assets':REUSED_ASSETS,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'basic_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; maker product gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/agriculture/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'scenes','assetKind':'scene','theme':'agriculture','style':'warm-handcrafted-village','title':TITLE,'description':DESCRIPTION,
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
  cam.data.ortho_scale=ORTHO
  aim(cam,pos);bpy.context.view_layer.update()
  rotation=cam.rotation_euler.to_quaternion();right=rotation@Vector((1,0,0));up=rotation@Vector((0,1,0));points=[o.matrix_world@v.co for o in parts for v in o.data.vertices];xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
  cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.15
  scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
 for name,pos in views.items():
  wire_objects=[];wire_meshes=[];wm=None
  try:
   if name=='qa-wireframe':
    wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
    for o in parts:
     dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;wire_objects.append(dup);wire_meshes.append(dup.data);dup.data.materials.clear();dup.data.materials.append(wm)
     for f in dup.data.polygons:f.material_index=0
     w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=WIRE_THICKNESS;w.use_replace=True;w.use_even_offset=False;w.offset=1
   render(name,pos)
  finally:
   # A caller may request any valid view order. Diagnostic overlays never leak
   # into the following actual-material view or an exception recovery state.
   for dup in wire_objects:bpy.data.objects.remove(dup,do_unlink=True)
   for mesh in wire_meshes:
    if mesh.users==0:bpy.data.meshes.remove(mesh)
   if wm is not None and wm.users==0:bpy.data.materials.remove(wm)
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
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; maker actual pixel and file self-check pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
