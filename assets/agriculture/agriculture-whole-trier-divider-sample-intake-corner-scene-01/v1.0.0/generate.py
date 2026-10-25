"""Original complete agricultural sample intake corner display, three whole existing models and zero new reusable models. Lightweight maker SELF_REVIEW; static composition only."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='agriculture-whole-trier-divider-sample-intake-corner-scene-01';VERSION='1.0.0';TITLE='Whole Trier and Divider Sample Intake Corner'
DESCRIPTION='One static agricultural sample-intake preparation corner scene, zero new models. Three entire qualified originals retain unit scale, every oriented world triangle and opaque per-face constant PBR: the fixed six alternating opposed-chute divider with both complete receiver pans at right, the complete open slotted-sleeve grain trier in the left-front tool position, and the complete gathered sack in the separate rear-left intake position. One finite scene-only floor under all whole original bases and a clear front strip establish separate intake/tool/division stations without interpenetration, extracting a receiver or filling the sack. Unlike the older grain-silo service yard or winnower/riddle cleaning workbay, these are complete sampling-preparation objects, not duplicates or a replacement grain-cleaning machine. The dock sack retains its original small sewn markings and is not relabelled as newly authored grain packaging; contents are unspecified. Only whole translations and IEEE754 float32 storage are applied; original hierarchy and normals are baked/recomputed and not claimed byte-identical. Static illustrative arrangement only: no real sampling accuracy, grain flow, tool operation, food contact, workflow ergonomics, navigation, load or safety validation.'
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];INSIDE_TESTS=[]
PALETTE=[('LowerStoneGrey',(.28,.30,.27,1),.98,0),('UpperStoneGrey',(.41,.43,.38,1),.97,0),('OffsetWoodGrip',(.34,.17,.075,1),.84,0)]
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

import base64,zlib,struct
LOCK={'agriculture-fixed-alternating-chute-twin-pan-sample-divider-01': {'bytes': 26812, 'sha256': '4e077590684e086888259a2006f3a2aad6ec3dfd761a6c2cb3bc92150894f6c5'}, 'agriculture-fixed-open-slotted-sleeve-grain-trier-01': {'bytes': 84496, 'sha256': 'e869ee1e159b53bc817e46449824a140e7a8f9e235272df631299085cb6497a2'}, 'harbor-cargo-sack-01': {'bytes': 49652, 'sha256': 'c93a3bb3df9b4c4ad81d9fcdc2d2b3423a1cde4aaeec5227fd0ad69964251804'}}
ENCODED={'agriculture-fixed-alternating-chute-twin-pan-sample-divider-01': 'c-rloO>Er86@bUTwH4QK64{RPV>4?fc9LD0|36N>TU&`yw~pmnsnftV6l#}}n5;;Jq^!7xfTEY6KpPk6DZK{hsqm#219f)W6gi|wdTD{6Krbzjo_gpdIrP-`_+xP;4mlLpX$)uqk3Mqe=e;*?-n`+`v)xzDY$k-<nImM6NXU05C(hrfnZ9oYwG%gLvzB9dX5f0Y6SeQnd9LI7+$=QVPIoP*V|m=!;}hI9c}yCUwOYM)&GLNPb)d31#@CkXHNOoV)K2g*`Lz?5Z`2%f9`4m9!|&=f$L)k)2+Gyvt1Fi`YS!C<XZk2c+nrx<9m@%(JhzK&Cmf4gngiy7IlKKP_k)ISwF4NMvz>O=cB~H9o--ZC>T>Ra<v=aZU7Vfc?7-*DcCcu6xy6MAkl%DVT-RL!0)6~C*Rj30BeNS=o?`|Uw3sz*#}A+vi!(cKm>_t-bxn{SRGhc`xlqGctyfX3Q*mS4nVo>~C%f(f;CLhwTIT-JPAH+BaNlVsme5YT@3fOjXeZrw+Q}uflkYq2loHx0McRd3aQ>X@1)L9Z;@_?{%USc&R;L5H*-qec3!rB(7i!=~{c~;4^?h#IGUrz$QwJq`(Y|KGb}$)rd(N8Wr}(c_9<5Lw;VYF#FOWz0itS?*%2Q~cN$48{!uwq-u(%o9vEk1wtN|E2mSe{CIA{eP9}W=8h07yYayeK7mW?SwYGYZoZ=Q3PCQa-=7VtvYYmsE*iAd414cBHe7`I?L+>(tZidN{1yXb-GAg|$;%x>2YMQnFnA1sQEe1w^<3pvk<n5#BGTzwN@I;eUv9_NDT@c(}~MHV>=XZp-yw+pg#K$yhw(3=LtOPnnVc)n#~9S8o*VOX>*Zr%*qb6CS&3_$5f)b!M^+L+>KHWAj29rHAd%6~nimD!|?Yztj=JDvrJ@MXR()Wy0~m+MMht!s6?Zq&i+!J}ZZzy^X0Iq!;gVdgz$cVHZI*0bA--C)tP8Z-9WR;OXE#Q#QnZZWVL!IJGXz;haYxM~{lvTN`HB-S&KuLo0i_a5l7@fzIr1L&bWb<Os{GE=V8y<R&Jc#BrO=6d$5?M!vdU~wL5<IQ+Kgdk-92zmokPUCX-Ioz#0>xKAx*zA%B;Nx}ZtBJR}kq0)Cy>n1j4wSb%8{D{F^TI>LR2xR}VCF!E8&_&($6N@&b+6P;a5HAtx9Z%L$P0WMO_6!u^`^pu#Ne0L+g;0_>R66z`-A;i4rm_Ux>6f|ZT#FzlUHhZKaw@<Mi6zpgZ^T6!aH*6dTJhqi`t(#`@@%BjGAAwt);21c^#BWje0p8_UbaaSL{@fdaT~!$8m-SqG1isN8qVoF6baUBX!)xY4Aq)wv)_a++*D4MOYm#TQG5Pn&5+(7pA@NR@ZJ{!~_NoW})*<o4z&fc3tlb7$47km-#VC<HL`vsk)>IYMmdGc_aL&vM6aH_%PmzK8m68vMMWe0VR#cNP6SP1ZAL_47;S42(VI1Q=<N%iX<wkzKlz%SW(k^^8#d4!5I(lm(x-Zq9HX&&@=<|1DymtzNZR`F32L@ij5&?x-LkDBvbU{wWz5s3WBcks+y^%9@kPtNl-;yX44b4$X8vr6Yq>ACo>jbFht%EbpvNpjHgaCbY7H1QAR!EdxC60Wfdb;mY$hf8FHk$4o2WLflaB@?o`%6m1yd8P)Jn-Ndxf}e$au?L1Wc5K@k;2qfOjeKggW80W%uQ;j)BnV(|F}%Yy(=)wAbq3~y0eGYC9;8Ww)2?}drUv#*?;I3L>j{KUnVPo0CU2%?7VbnG_P5my2NR9e1@)-G{WXC7Z#8DCD1uT&XdWFKE$8DATk{u2B6`pWpm(Dawt#~0ELFgy=XN=P84B#_G3AoFm@KCYY^S4ocxn^9_Dfob3pE-z@Qf%R$w3#BwRRt6UNssoqMSQJtNi=_sp9NgH4P6ZfIrVlNy9h!C+V;@^djjax>EiFB^#5#5vlcxfUXp|b8eqdsc>ZzzA4MY`5ESPZm0f>F{)SOELb1o^XM~5BOY~!I9Pi5HY^y18n<z0gOI@}!Zo(f;Nz5p^Rf~exnMF$QMm}btKZ$q;Nq&sSupXiEe$hr>6KwU`E9Z}L{L07_bVK9l|@sKueJ5d)<Z6LkCj7d=jQi6ITBZ-1Of>65JrI*H|N3Cfsgkml7nu}S@rMt~R%B1<^_^ETJF0Sc7Dq%%Iiu6?^$l?W^molxGWr4d^6cu?O`^`3D)<oo4L9S**rK%Ct5=MkWReVg)bx{^XLn!Zy0yywcyicoUIGt7RNaS+fl4+`;xQkIuYk_B1dyT)Bo9nDKH=M9jG42Q=yA9Sx&a#fMHhd4o4+N>A5eniCoT^vW{hG6A<{?&=qm#Lys=5I!l=QL(%Y+{ToI#VN@UaXpMN7mGcm*0r=pT|6J!23AO-F%>%%Bvjk=tI)kDroS6h8%x)sWdnC}qgZsThVC^@?URhU`s^OchFcQzP4yxj6}6%@Cq6WN*kb1fw^s#|&acGf3=aSRD-UVdSbOe06-pnx6kPZBR+AP%F8jR!WJD!w5wbcumxGN#${JvmR!u`rr%>r0p4f@bRN&T~&15fE^n9jUQ%9il&O1t`(U<t(doKRdY^JAGRSInN}!i$wuaM<eH*lIwtWY)(Luxh|hR=RTjbPc`e*5RAV4>7+5CweH1)&L)0KOkqkL>n5c~m!9tOgqIDw))z*z9R^4PJsiK`4nMxNJs*!2kTum!R7)dE@DUfKThxC(%@F~Oe^}sr3IkN%2o1>}Gjft6=@NG%>J}|vmL@<sju1HhdHoU>wT2S@D)&eZA!RAt#!39aIBD;VQWBtO5vQ|ZSI1p43UJ?bhN^{K+D>RoSw8r|I8?s!*>6A+IuJT3|)2XUf!gR3F3^vz9S+CMukxB@Uk`A=iMVZ}a*A8B4#jI(r3%XpTxm?Ncx~B3Kn#0+@%DfqpRK;{qy^87J7*J)o3p|_~Dz(=t?h{hAjY6mvF$9sX<oK}nS8`oJG|Kqy>QxW><Z9n7wd@6{)JB`pUgh;F;;#ui(n`J)=Q?TkkqlK|zPil)LM7z%+4JP~!H;^My}!`<^pj6Mpz-LfcbNFoPkxrmTQ9xK#BbaQa{1$HJtj{2q%rEq#=BZGGyiJRIMT70Z+@ucGU~{}uYbNLmr+L+PWq%V>R80&?&rsSEJyx&q5qplM*GS2;Ac&pR!*H3)M+u+=?|&Sy_BcLV4oI)eOe6iv`WZRrq0mi*-5sOE#z@>kUT|p!4>jT<OuK<`1Vn_Izk?VE94{OC@>*=NdvBq!rzDC`Y3r0t~Zgb<OwLBAP2}cvV(9?a^y+!4KhM%P}ayH@&MUQo`Lcia+rLR>><aXJVu@-50Oz)hq6wdC6ADOWDLqN@;up3Hj~Goe2g3?S8o0!iFGGw{MN}4CXQnZl`s5!KNH8Xj>>=g^AZy$ebN|pWaBW_^=KUFSj=&3p)%^o!f~vlGU~{}NuM-E9gCQ<##v$o%bMyl*69za&b^eU&tRWEgMIo8^7Ko{Q>M<)<=FypawkN_gAft70PTWk_!KaHgZwx|L;{5I@Cfi;xI%suV&j7lCoyI|2iFH6LT-g}E5yntAwuqeatFl9Ll7ZHpd5i%c^D$(ZYXy{tb7_G<Q^#ZK&*TgBIGEPqYx{fhX}b3%6$+kk3)pq4CQ8smGHTn6ViC(v-f|;!buKB<2%7G@33%^6Vmwf>z{wX!bzVrMjhFBSCTtra-?H1Cpj36QAZX|azYxTjx3z?Nn_NJfj9EWjeK(5@__%pkmOo4hH6a~PI4O>gKwW?;Uw3hF|4(3v2fBSjZsH7j&dy;M>-aBD!0jG)RBdgT#Lr2BMT>e(in9t;*C6QBTuU$51dny81ey);atGPNzOoHID;^8lEcs#&O}U{^hsmXk&UAqhQ^VO#hl~}G)5g+ILTpXj5@M#(kG2k$0FXye>U=;D)NlpdgpEqL*v^AKVsq}XQ1)N*LqBx<S;bedg)yzPWq%V>d3}X4nyNe$6`)$1{$M|ES%&pG)5g+IO&tdsACat<UbqvPZfE-^N;^RK7IJ)Uta!alg3{j`+FfL^|hb=fyzn!JjVLB4{mEEeP%J%FXE(ry3f^|)X(G9KDJ^zx<9AtQ0JncpFTrBt?V&#>*UGPVvuJ|Kbyi|Y&OBat>JGp`=G>UjQE`M!SI>pF0ws*p1B?V?IfGYZZZnxX!sQK0kR*;{p2A6HgBf<DwARE3OT7C&toPh_463(r~E3Dv3?OJ_0xT>=A?ceZ}?%pAEx3=kH)DuL*-Q5qjD<lQ8^W7sGN#3R8GY`DyQNel{fq+-+xl^p-1CXe4uhFUQsy}uc(}g4^&RY2P&uH6_r!*ipm@QlkY!p&WOMJb}NTl44l;O=WvUG`_Epvc{1sf!Yu|)>i2WFRm2<qlkY!oo%~bp=7)<XZ;Xz$a=6LPx0*TJW8q)D_g*uRfx=C8j%1*4uZRixeaL_O;#ez(o2>lr@853baF2!I@5w|43O89fk%7X!V!r3=YrSjmUaha8ufdZ2eBJb_BoDqvvNb%#Z3^EZc^*o9XC!@&!}s(?p~Uw|@a>l9O!qLH;x>oxp6rH`9G(H6fD+&9+XLsoLr@-qD|}C{1|`1NhiAkCP#%CQd}Huv_;%ot@couLl=xmBzF*jY65oP3Odbp00eprWPsPbwy&P_`^H@KJdn_Ess9p{?**TJd!o4C+#i(8mH(42CR6mD%EF8zEUJf@|Igx?Fy<*;olN)iel05yJAAZr4q~A7+__O!_lgqU)M_NVv>mJui`lN6xHEu4)eNs6!E|t^cQg}T+Usz{YzjZR61q$n|_cv4AE4RV^xjTIFxg&f6iu)<<oA?A3_g{Sfb32syrakVPBT(Z0yf=KWesA~|e#+l^MGSM7%kli?ay-9z+)9m`%W<DnPK`_D^tco*<73Qc$zlEGHLN{ly}zAp13yIH+YP?=K=>>k|5wHS@c(7(ffC;z-V#2!-xB_>4SdSK4@!KtzcYMu8Q*E%Oa2GEk68E', 'agriculture-fixed-open-slotted-sleeve-grain-trier-01': 'c-rlq2Y6If^Z)0Zvo`FC4H06nQ%o;plNCf1rKqT=T*N>E1Ve&J00mJLv3J3Sz3XeQC?T<71FYEfwRf>&FaMdldoJG%_av9+_xy_Qf6X%|AMVaQGw00rPBwRU<M`Tx25KVOWM4(`t%>#>K5XcW?8?T*>Za_zGqT55*Ht%EHq|#|_s!mKLPLFBePh;mJ|(MvZFOB$bwk#m-G^mOE$EZqr=U2ySN7EEhQ^xuI(E+MlaoEOS9arAo*=t#PKp|{`;MHET~|4Yk7W<{AM2G}S6}5nP&8`hs8#=(kzIXEQ$uB=WHGjW(&YNO>bj=U4fVBh>ae=%EdFOrLv_~Jdj4KFrG83dR?~!<u}5V!O&L?2HLa#;0{^?Ax;l%OFr`NPYwPRAS2k5wWz|ovuFGnysjAMJT;I^tm{nO<l_eo+tDCB`YU+5!S<@<OYs<3g>a(h<n<~dn;FG4+)K%3_<A)oo`5al>r0T{A{?bzG88LyA>sMPdzOK6JAPGIfKV^_iIJ~yHdTKSF)#0*&L^$uJ+GDetDkoPraQv~g^^N?kwtgC?$9tb#;<%c+8ulGiJEg8EtE#4Pa&6_YS&ckfFHXKGt1_!`LS@6`th(yzs@m#RN#~{~-Cs`M(+@CM=HIKXs-sl>^Emu5oYR!aoT5ank$tSKt!&7eSkH;ojn8WI*WJk5X0v1e%H$sL?l;yniClub^3wAfDAOM-v+tXnZ%=>rDBC#A&#$3=3ahj#i(Ts)MV$OVJqs+zCTn~{&E!?_^V8!Wm^}TU;OxDV-Vurzh_Z14Ys_v@Q}v{*arF(XOq(HOHi31BMJh;7X1Gk`Z^m$*CQ26nN3M{<^mV|cF>Fdx+NCjeLQQQ|LpAr0kvY9`d*$`Y?^V#NkekA)h5DUobWIh{R>`#+JEgX1N<(#TUx>XW?cR;G^-a8n-bv~89^X(|Q`ftxp{BZ_cTO(1n{nL5nnqXg&WvqJ_Nv~8@!`g%%BGsJqo>w1PN}RNU0+vwY<AzKhAGv(vg;da#@E!1uBvRBGKszAV5)drk(%i|TV-w57?Db27PqvfhU&5`u0{H_8C<u$vYMvVui8x6U*5aab<!&(6npukt|r<3RK%o4dSy5G?RT`)wxMz?_v-8!UUp?w<>aQCsnuR~->h+!wT;{byreYbLaQ4edc3}2wBK{nA3Sz!ZFS>lzEbLI8q?>iuH)VC4|&;p9=7M;y@q?)a=fupmgG;9n^z)7L|v6t{*eOs_vlF+E_wdIL5J=&AbI-Kn(Aqzr9U)a)RBJJQ8PtNDG{-<S2c&>$zty<MLtMsoGm{?Cb5VcYWPh5=SWrklrenyu$rrENmEk|sBAb2+H=3Us#JsNl|6Y(!w?pBZEek1?gHZ{@Xsz^e`6{etJ$f(VIc3i{8${B(<d*t)c>!fB&WDEr#QD4A1ag~Kga*CAh$R#Kd&%1zgMm#mzvg2kkhBI(09wtEzQd*%`4^N+K8)sii(pyMMWj0JZ<4jxn9~?*_7H^yt>wGLHQ-g^%NGB7L=3}`im(@t|h0iv?!;bs6Y<oC)byopPQSXlb2gk=vZG-fj?bwQEp*LZb4pd=mHCqF^ltyi}Onhi}E{Ipf7<D+{^uzyoSpwPS&e1FF&^^ucW{)Rq{|lQGOvOSz64;a#Lk3&d)98x|WuPFE4a8CB>=I7Z;V}7v~nu^kvEIF#Rb|gr^L=w1%2VHF8-ePpxd?W;TXv>#uMBVZ#R<G-%jRKarus4jj^NF#mYxtA!`387n?{tF8xjnmJ1LwWA;Yk%Q*13R-|c3o&T!>OoyU*&_!oS{1k$1DABL+VCIgk;9h4Cg)(>+*}Ntw|d|<KfWVJ%*}(4`Dq~wI#{dYCvEi5g%G;PsVONhtGjY6Kh#*?keqYOlyT##8xG;7?kh8Resa*UlR3Y_+`J+=$jXzAEb^;%jDK<F<Ru$HX>L(rVSWK$eZ6w|U;%cJUSV!>fz`-Uhu)!+@b#SPV7UdQ+-r+?V|zR1Y4VfIK4h;w^Zn-~xR~51i)n9yys!!Kg9-AuBLx!--?QJ~eh02LMSlA^<mVT`ex|xzNpW#WF88An*@?Vldn(8&<lbHAcfi&B()M%pNqY4TKc~H=7evUrz4Hs(-@3x0f{u2ssDtVi6u{0Eq<$y_vST3@`a&!yE-WZ6l`})!(l&0jIdb}xmL_#rT9{u{T#%oXVaO!y?L={eb+mVWNe3b<F6w9}OWV&NFBdeJTe8|l<|VJjeEw%qX>ne$e@Q33O7rtd3kr&h3yN?jL*~d$e_oNioI~bl_j1mOu#R>o$ZdZs^9wq>oOAQq&!H4AXS)yl94&{Rz?8~9Bn4GioR^nVP*~b4#4AmcAyee!`+HebRFs#?O6=7;e2#WEBERERw0nL*`x}{ClGEWv7Ov4xn*7v-Si(<ei?}5gg#V;j%`Lq%t~QD5Cr#Kq?QTfX8vm%_8CT7KKZyMw!efqYsvgY0zBS1mpu7^9Uk(i$H_pG?C)-=uFuvLsZD~>7s(hlHojMeC2L7d@%>;aadturH`Rz<lkR#qWL4Hn2NlEk!LMABSU%=L26Xe(2^a)D%cZ%ps;9m>dOi&=|Sc42!pMbBDHQ0l~!Zuq_kYAWz6nzDGg{5sLD9BlpB7{u9zu~UI78I4XkrCIhcui`MyV@3T8!TB96||k8kcF`ZE66X(X>)$wnyp~<Yq2nIwM%IYujZn{f`ZjHA?Plt&H_^um*f={@b3Xx3vw0pA2gIEoWCNzZ0XW+BAVsmZIAuf=NG<TxzNS6i<bF3;rvO>E*}5KO+NE?C$pc=e4djzUYRh*cQWTq$+#<=EP2DZp)7er4xuc0!&*XF{9sQ)S>nOohO*=hH40_$FLN=(jk_4~cQWjQlVLxdEP1Eu;$*0=lR+m=2E92Mbn9f$f0>IV?@q7vsIb?RW$_WV*O6tJU)WwdmL(@)d%akeJcR8vVp(Df+v~!z=s!8<iZqtk;2*HWhWP`Q*pN@a@)+bFu*?PP4On8s{xrk>Sf4Uvm@|$HIYeSui<4m=oGiJf_Rz_&|4xS5IT`96i9tVU40<a=mR!F&U_qc&%i<$!wQ5=B6t-HmEU|^HRxL|xVXIZk5?k16)w1X_Ip>Nrme}AQu*8P>1D4p3Pr&jR<R7ri1?vr1V#EG4!~R&GGGv%Djtn_OVpxllVIQ0<xu*8e$*})UhT1t9>K=(fKWPklD?^rC=Y08MpjFG_BW$&5S>_bBTD2^(g{@XCOKf4QRm&1v*lN|X=rcLziZqtk;2*HWhWP`Q*pN@a@)+bFu*?PP4On8s{xrk>Sf4Uvm@|$HIYeSui<4m=oGiJf_Rz_&|4xS5IT`96i9tVU40<a=mRx_@rE9`!)w1{qTdi7_IfboOElX@+t5wSqTi9yVvcwj)TD2_tOwPF?jU_ht2Q0B+{(vPm<P)$w2KfgpbHRE8me{aA&9Fb#rwke9j3Yx1kr>wEWY`BMORlLsbTaI}lc9D_hPp>$&`%nJ-pY_A*T+}x5@^-3_y}9AT9!G5tyV2dY+<Wa%Mx4IYSpsD7PeZoEc#5&xgw1vHuwiDv0?szB{t*}usjC&2P|{JdIOf&us_YPKh~!V8Rm>5Lk^J`*5YK?2PaFesXcTu?7x$tc20)6M`F-V8iU@-kdwXCgTCrPU-h7`deB!r=&K&|RS){A2YuCpzUo0=^`NhM&{sX^s~+@K5BjPHebs}$>Oo)ips#w+S3T&f9`scY`l<(g)q}q3L0|QtuX@l|J?N_*^i>b~XZs9maWd?Klau|^gI>Bi!~Q!NYUgCAdn5+^q%r8N3|VrW(YY?rs%7yJwpz6;a|&CnT9(+tR;!jJwy@QzWr;0pwQ5=PnVfS)8cS^O4_IQu`~gdB$R}WV4Dt_H=7RMGEU{sKnqhyePZ=`I8Apa3(in11V_0JvOYGF1q%rJa8pEEaG1MrHp{8jJ8Yn}S*!lUh1O0@t_zPPtg|WmEwz>*q$xqm7EQ}>rVXL<=mb`_n_QF`SmyEl@$&xpm8_JS5<Pge|H>@R;#Siu*lqDYQZ756LP@_-=|1uXt+_;M&e<#B}I2rcS$&z=fE>4E}IvI50WYC+FLAOo@{g=7;go(|;>m4rs{;&IeUVD?r7rJ<Guj_n1VPd@5#ozXw<1>GEGW+?==Q)|<`S-m!zLV|i9lQ=FOWts9C`;auLnuq$u$E93KiHE{mUytYp)7erjY1jx%Uld`<1U8$oecZnWY|w9+t)ipcP@tdIvI50WYC+FLAOo@{g=5|^0xQ(k;O;YUPqQ?eqnp<SeBfG?e$_=@({Myh-HZ_Y_AK;_O%atEm)S=;2*HWhWP`Q*pN@a@)+bFu*?PP4On8s{xrk>Sf4Uvm@|$HIYeSui<4m=oNQn3uv!gc*ncNO?VJpCkHny#GzPtuAxp0I-afMU2wSaMmN|v3RxL|xVXIZk5?k16)w0AEwpz7pU;D6HwJfp0KVXRs^9L-kA)kQdF~~n)nG4n%u*8P_X@>o=K4r)-XB-)Fh{UiKC&NBC*}mRk^%=&n|4xS5IT`96i9tVU40<a=mR#+<ePr<wwpz6;a|&CnT9(+tR;!jJwy@QzWr;0pwQAYE_F=VZSz?2Kz!Dqg4_IPDJ^{;Pkbl537pym6i4FVH4Etk!%8+5sI5OlAiD4~HhJA3deZ9l#GmK&XoeZ^eGSod1gMQK&^j3x}x!QaC$l@bxwQ5=B6t-HmEU|^HRxL|xVXIZk5?k16)v|r<!)n#C#0LL>B{s|-u*8OZ0+z=h|A1vKSZ}}*8}_Fe_Q(2^A;X+;WXK^B!&;mS``~2zdWY3#7{mTM8EWTbsCy&^{iHGItqfUmwfFXs#Yfm`)w0YfY_)1xVhdZXT9(+tR;!jJwy@QzW&7HP)v9HQ4gLX3Y?wb_i4FM#ERR9{0n1#l-hd@G>`yc7kM$`-hB@QNkV7PfwKy5}!O8aZ4y(^FhW&Rk)XvFJ_ec!-Nn_Ak8FI3hdeB!r=&K&|RS){A2YuCpzUo0=^`NhM&{sX^s~+@K5BjPHebs}$>Oo)ips#w+S3T&f9`scY`l<(g)q}q3L0|QtuX@l|J?N_*^i>b~st0}5gTCrP|7@ROEl!4gaI$^9V^uF*onil-47GDI)IAb|e$p89R)#FO+I#!R;v;OeYFXwKwpz6;v4yQxElX@+t5wSqTi9yVvVHBtYSpsD2LFI1Hq0Ne#D;tVmd7CffMqUNZ@>~8_NN*4$NH2Z!<=zs$RUj(=QM^jrm=nP!|Kg4>|q+io~JR?D2<_}X$%@DLzdX~{<(|AU)X9Xj3t(^)m0cve!^B`VJx`{TfK#`<SlHq7smGW4y(g3mb~HIP?o$QhftQhVJ)F7ey}H@Eb(A(Ls{~M8ig|Wm$?|?#$62gI~n%D$*`YJwy$^C>mrPyzD@?6I2rWjWYDdXLH}hgCjY-#tumhY{7k72)nB((1#k=c^qF1jAOGW<$6H)J-M87#KmOTk+qR-V`tW0kly58gqYs}`k&4-h{^%pQrgCpZf0vKVRk)2$3(V6JHV+=Rxwg#*kK4!Et_zRb7;X0lkK0_^?lT;(aQVPI=u_dyCxQNsbtTZ>u|Em)ckFWl{T=m6pufup>Yi}uCjt6NICPi*9VQ%lPJo^(9M?sK<2p*ard-#N>)LT$FRp9EbzQiw1(*I^ns@2krEQm<T^e@jwgavD>;ExU7<}(Qw}}Y4O+?UbB7$xc5p<h~pxZ=yy5%*u+O@lMo6+k339YuSp;rIndTd6knZBCos~N3k`f8@HX8LNTuV%EG>8qK(n$hZiMXN4Nx^(E$o=a~ojk$E?($bph2YYD;_h}Om?$ahB+^0=MxKEpiaGy32;XZ95!hPCAg!{CK2={3d5$@9_BHX7<M7U3zh;W}a5#c^<BEo&zM1=da|8dVB9C{ABPn&4(K5gc{`akQwdggVjf7a_(nV;|fGtUoQKfCdH`+w@s@ix!TGtWi;8Cq>!L#_Tt^w^A6GkrDFS2J48^wmsX&1f~#S2J48^wmsX&1g0AI#K)j$=p}}N8VS@yl(XmdEH9WTC^W&wn21+uGHJ=BiOdmF<O^~P>gL~I#Q3--Sm-cUGzG%J`JOF*ap)WU9Gp*W7xLSooFLEfI6`ar7AsM@1U#Lvh;?uDGjF$+4iS#x<>D;$FcR$o6zQT5N*PCAWhIm>D}}Mww-im+L8{T&TI$ML|v<U>4|K+>aA!SI+V6z8$pwFo!(tfV(YEDP**yfy09Ha^?I_-)AejQdOPY)9&N`ql8)95x=<g@manrYn~tC?wo%lmn{<h8WGm7=XeX+q9&Dp&ik_;=^c1#Iy(8^PV`)dWBWapGRwwi{wz%GfdQmm)!ZwDE(KB>^eGFTL?n%2-4fSNJqUrhsy_cTO)=&4LJgTKWY!hgvK1uJRXR-~@xl~B?l*@J$ov7#N{q%`!d+P!!p#~~otD}?ksd|V$nQdQPOns?|irJ2))ASj7e|;L;P+dmlG>yvGrqG%CY&~3`$##IQpgm|hRj?gH=jikFA^IG)gLFUIlV(yswi$GRzEB^gFJK#?2hcz|fd;T0PjmG=?diE}hwHsb(LS^{+bp_BkJel3i`Yi#L9CpUSvx1wNp!Kkj1_b-+Yx$SR?aD`ol|HwU8*l<1zpN^q#n%5IgPb*8qJ~k`bt*Ne6}%qC@bd-*3KDpDqW$kW(8frR;Bl6<($RZIg3uGtMs+3psU!%=>u6gXR~(BrZedpeLXAa8ny}gU{=n#tetb|9J)^5zzVvKZK58*$~m94b3UC%H|m>MK{v8Z(uc8fE@bUoNEgt}`W9Bu&2060Br9hgYiAzKrCasCSV6b49j!;PaxP}=Tuc|yZTfar&~0pudNeENGS<#zbP3&|?_>qt!8S!7$;!E$wR1ULN_XjdSV4EOP19poIajiFuB7>Nx4w@RbT`{Ex{8%^Eo<jmx`OW23s^z-vQ5`BxKa;rtsbEJXo+6R6<fk~fj*uqwSa52fF7h}`Z=!HGPb#T7FX&-uGNY35IwIi;fg)ac9A}bE47GgwTKqd3;JcQ*b8hI>)BkXR<2bmHPcJ_6|UGzY?taeT&YL7R*zB(E!VGc#g?<p*Qau&9_Ly;PLI&5`VFqwt87>3)45WMxmJtmF?wCU#T9#<?J9jHSL#Ww)syrDy{X^fioMBpjXsAf^)%P&X?lv@*8k>;z0G!=K94K)EZ6E;dWPQB?{UT6WxG*dz?E9cwOUF`=zaYGSL}VZoAq3-)N@>`=V%#ys6XP0eaLpJzKARJ0@vyVdY(SkpK!%KX1h&a!j*cNYxOd{NT2G@xMH8O-Jvh#O1;9hdWBx1&-IsFvCrA=((}1euW_wjqviC4UcnXng6(d71y|}VuGL%gDt)ED<BEO7cCWsMZlHhDHEeIvH~L4tP=CYrfWDq?ruXT3ws+_U{j+Y-Kd?QlZ=!$EM|2b0d-Rk3RX?JCVq2tdrQ7Kfx|Qui`c40#AJ@OJJ*w}ZyXbSegY8rLQ~#}>)PJ%)q3@=9=_|UM?F%BK%`=+Vp3?WRa=u~hd_yZJX4W!Gb&PF^evp;(9c$-1`j*x<>zL>C+HA}8L#&*KSvwEY_q48gkrlMAxr8;ekd^ZjYv(8Wk=8RCn3wf>Y%l0$R?aW1onL4rt#39mujuvJUeYbBoZnbGztPXMq1nW|rZ;3;t{-9L{K4A!gMOur&1U8ey)oOX`Y~3{U#y+K=y%%GbT)74P1#=8Pq1?SX6^h<f70e=OY@H2ob65h6e~xmr`SksVYV{=)?2W>t)F4#81)RBR$H5G%zJukws-XsR?b>#30q8cG25CCbQiYw^)gn@I%*l)+N!JB&U~c1vVEwZXXUJ?o@ZNEbu-<~C%PNk$NEK9&Iam5woWR`Y;Qi(S!|!`msmL)sh8N+SJ`F<^QF#a`&=()<!qvsvu&t)n4QcD-Gl85{VFS`vwD?nW3{8%&3vbKWcy05;7aYHR<P})%1s4Vteh=ozU4~oroLs{RVB<GT(Jb(+U9$%)DK*%AE>A5XF74k`mwERe&kB+u6|_et@@k2xMKa;)-x-)Qn_j+TOT#R?9CM$z_z~mnJbmAerC&21I-|=*g&=o&97XkLiH<Kp4!Lk#}(U$ZDaF0SE^Y3&Q_rIHAA>!`?76n{^UxPs6W|?)L=7=D>j&IbHjyFeYsYBRjC?k_UDQXW!u7NWmKGN6<1~I0CON$>;Sf{O-!w&D!5h^s$2~>2XV!Qvvo0Rt98^KT&q1)LLF=l;ffv1*43=5)>HktR{d2!HNqUq6&u0U&2&;5sJ*yWd#OFuVdikI*kNp0W_`7h+M8>&w;G^Eno(S_k!;y!L$!$-#I+iv1}e{t=8Ac2J<P_cvl_y+8lv`5N0_l(u_M@aG@Glf)c$I7w!x~>j5EDWCEG4$OVvdUS6i|TQ`M%%<d|x<US=D$ojOEq!*-yWV2(0*W&+#prmO0%4pm**4pz0M&J>zjwtSPNveihH#desgH%FTiQ_ogpdZ-=M5vm89ry5L?DKiahrDi9!i>hSpRI1Txs+q<Ln#xvgc2&Env8<i3YK%I@9LowihAm-wsvoGA>Zy9EDmC5g$qJgz*3a}-yQ>MToe653nqiJ-1<hdVZ~CZQHIcP5QH@tK%`8^XOtt|gN9C(p)=sUeQ74#_SV1SS4K#VGP}Q+^>eNx{L~}AL=tQ=COo1v^lUX~H)g(3BoWcs4&9<*8QYGqW*3QwYUd=J5v4ZBX4K}5$oJQ78qiRs6n$uZ9r?L$-WvrYjteq*UNu6QNWCfkUc7Q2o<xFGkOjA?US>|k3&{=H5O@ftkENkajb&NX4oXZM2hwWg~kCiinwKGFaSLd1YSwZKqjWBz%a*k*19IuX37nloKK^L$cW(KfwX0di=shMi7xrh}smu;jO$jUj1wR4g>LCrIlu!82Xd1fD0&MB;&Q`Cv-Vskkw=wh}b%xJFEWn8Pv)FtXpa~D_aPPVCL3|H!MuGQsgzPj7o!xg)m?HE(Vm8#}iRjVu1z2-Qs*u8Ai%{Z>qHC(G})K%&}^B`C3KDHTVJXh*EuGMwwYW0A5h%5F0+e}l#mAZjzb%VNAEienYVhh+#Fh_BvZsJ<qq^?&Fn?+o)huKavlekj1aIJ1pH>zgS$`xy7n{Dd3QnzxgZdEs{7V{`qtc7ikY2ZrT#<jXl{YyP!9^;BV!gi`@;!54YwYo#yt{yi}aK#>HJHt%nO5Me^x=Y=u7MmxzVvE_%GRJVG?%`V9qwZEunWwp8PqCe2rgNq4<67OP?p4p2XSrg}u$^a)<4QfqwR%w9ua=mlT(Ko=7nqq`sfV~$52**#GV?rFY#G~Ja{^atA=hf5TA-dYFLK46W1DAA<Vr2#S}jr!s~616T(K9}E;e)2>8e%DVQW?|nODqJ<|Vev%xUT@^{6_Htwk+2ubFGja<(hYnd)5ixH^;V5%sEh-CS>8WxK|lqs~`PsB_pJQ*W3z%}wSFwj0a^YOZ=xUBI?jy=C4ux0<)uZZ`AO#p-D_kL@Y-j`_E_-Mqv0FLMbi=ULXyv+5c3u6d6Y^e)?-W<D!tDQjn`TB6=JAFzVnXS>^6!OFRkwR5Ffram<Hvw}WkyVqRB%6XZ!^RjwDeQZ8w1%1qRpShZq^D1lSRrQkk%zVWP`i$)Xb1f_94c5*Z>J{~+`GytrCEEgXJuByJ*3R4Nb@jFRo)z>p+r#EYR?fSuop;q+>N~TN74#ijv$>g-^FC|mef4kkqxppu^dnn~`4=naBi7DG>I3z&`HdCyGutEPc2>@(tesEQ$Le?UCoAZ8w#Ut#teh`cJ71{J)L({TPny42MT^bdteh3BofYa!rD7)bv{7tNnR{6|-?DbTRbQ)EZ0*>yCdT%Rxu2EuBWveJ^_^NLwq9(hS%+<jd4QGkGi&E(^@HjZ+c5UL>BP3oEMVpQ#@hK!{iHUCZ4!IYY{2%Md6<>+Cu`?V^{d)Awt4JjvoYHXrkRyPx|!_{wOMS-*ehl;wwFu`E63;-w!hUDv29|nnJw6sn@3nVYwJhYwB9<lZR~ZkHQTG^F;>pH`Z2b(bk|t7*qf#++Z$#vD`$PZm~B1XJ+^)9ZPT6YE%OvBXCwU-+Xgy2wnOaSCY$XY^9(CzQ~eCv#(Kxt&awB*j%@FmC9IszdI{TRdY9O4u@B5HZ10<8teodrJI|{vbkEo)te~E;`&mPVh_=**Z5zEd8Io}u-BqtgYm<y!b$7i1tw%C;*V%ew+JI!t);sFWXk(IbN4<;Qf;J-=chNod*0cr5*i-k>+tSt~V;`NXyV15JW3DdH+fz4^u|OB=9cX)!u~_%jJJSv%V_#jaccYz2#&W%f?oGRqjC<%kbq@6=8TZr!^*EYHvv{1PkJI^-Lj!pns0ZnZG>K;OI9t!sMU+p2cpRh$>q#`3PT}zsJzJMj5e?>XupXu-QzM<u<LUYo9j8(n#^W%3pl+n8bQX_i>C<(B;&dR72kL|MR63T<<?&p7mhMjpI+(|U^`Uw%>Q6Ersz+*~y-3E9dP{vZji=*zJYGMjkE8qPSstI&=j-d}D!QM?`}ITmb$Xk==ka^}wZ4(Aqlb8WNH^=Z>0MgM<4XO#zJ+e2W*(b$tA3Y0pkH|WMX%Ji(Jj=<W2=5le?TA8?>zplf6;f+ZS)wAkLktwWBQE#;_)y2yS|6+q{Tcg)=%rt=u1-OGq%6<X6g<4md9`PuI6jnS;cvb8)LRmo2s38+}ZRr`>LU;ipMH*q}f_+p?dPz)ATVz)d6ZekK;|1*;Z|>`taDt<eCH2L24q86U}(jO>L`kdCWBh<{&jfP2zEqnP|3G-BbaO1*X`HP=~9@JWe)~%noXMRm@|t>1z&Gqf{f0jb^erS?#CB@HocIH%F>V)g3(EVWyZ<)ogVskC&P&%o*xbCF2$5YIC+aL&<oxxz3!Y&Q>yBXKpkXs`HeLH=0|_Me0H&<1OYk^PGB7eahpf<|Ff>TCTp}@eA{*S*~7FD|lRCzA&$;H`TX1err~kH`P1p2OfVg-<o&Sd+H}1e=<Lq_tb~#R~~;gKba5JC+ZI#|1iIrPt@n?Zyx_Pf0)nJS4zh|XZzcHrM^*X#lB+Gv2WD(YF!@Jjja{?UaeH?^SFL&-PlU?i`t0CjbiJ^eo?=xO?lijwo&YN^_S|*W9QhWvA>kkTk*J6taFSf)?Ik)65A>k)9dK%c-$`5CAN<4q_cR;iftF`q&L((c<d3&ifyPj(L3?DQ>;g96TP|KmB(FUJH<BF&#8~h=K3SEYwX7PPo(}f4b5`#^`9;Bd8ad%JnZ5b18(*C#`yyly7<kt&h(kTJDL4_=JTA)@%jpLd?%-J=eSQeS@MQ+Ls{~M970+0hP8yU_`#lpvdufSx1kJcnB`*d@9ScSTjpZO-^s8KPKNz-vgDnri<6<gP6nMg8T964(5;g}|9xG|e)6~a<H;Iz%-4Tb?(=SE?zb=s&m6Fu&r<&={Ki`A`^?{)qp<9|FwYT*IVYbv$4H#||7CD)10u1k8RqGbWzCRhhb(J`edv(o9N6a$S#p9pcF3}3&`F03=axlb$So4X+T&3e_BIkj?ILmN|KB0nh{T}1NDSJJ#Bl9IVz@TTqA*<hk@&+Kwk@C0`40d8+Y*I)9lE8@vwCdb9EHzbvbN73-Y`EBU)t^MxG;Z@#C(p=JjbFa%sKhYIY#2--zJsZwvEKHW|*f#mNi439kQ$$_Mt<Tb6}r4WXTEY*dfcBK_?wDoEwkAkXs~%wMSyu+wv$3wTr~bzuoF<BNBu5A~9$?62r9<kHT<mMq;@3BeAS`-wkwy?K5F4{=&Amgt6oxZ2L(V%X)-u4+&#ggRt!zVJvwI+g=gI(i4(#w{^1Q4d;fk<PAB5vg8eG31#tvJqcxr2YVaJk~h>Sl)*plVu<Tx$luAZ59Ka~{dBVAovMqIp}tNAoj4iv7I!h|*2$oMC*%7_H~L~~;**UgwOq=N0jIs6_UtXkCAQjdQp>hiw6wT<j+?hvV(`Y3TGpGtRV(_V4?pJnux~5+qYs}`A?NZOt>}+FlB?vvxwN9c%SUpx+{UK`=4lC=2aijxVfo;3v9NXFahWS@fAF~E6t>TByu#%J^Po?KBcBBNJJyvzf5-kL(BHAo3G{c=D}nwlAE<l6p`QfkC*jax0(6*g=s5v;u5erzc<oeNpI?)>X6t8La?W2_4!p>9tsTDqVTn##Jlpc4xvvGU9mlyX7tQaRcz}<0&)GQbI&#g!e!f4Smv&9L=Hc@zWFDR`?fP=fBkPnrIp0>i?p*V@{AHbRyrrY#vQC&kxK3TiWu1_JaLu}o%fDfNg6r3HT;jq02iLOexU2{28(hn9yxifFcJ0Ib6?iS<Ja{hTpLSil=7If5yT)Df!2YLQ@2+{EzG>IKYaY-~0(*jM9+yApGp(Pvj)VTwdW-8gTwiH@#&sO7-wNz4uH)EeqVylvd%Ur4pug+=-q<(r{o6PXo{N10-^=Zq2m1!TuiG^b_7i-+w`(4kKlT}XPq^zi_8EMCxa&CfnY8zcJC0+Y!S{{3j$@y}_mJap>?f}GnY;Rr>oXnLH}G87=R2@(;O8}P9y}NO27Y$KH4pX;{2YgC9_$<VnGV-H*iZ1Y9<F&@{@7>m^B}I{*k{r{8{#;QeFi@#;yR9f20t@`$Fa9$K39_YduW-@ZT)Y2ZcE;2BJVtjle}N0h~!-^IVA6m*^T6#GdqyHucjNxyKc57c~8z}B=6YSfaLu=Ym>a&NB-;Y&rsx_yPJPjH{X9V-*au>C+<JGgMWMj{&x<4CmN#GRqHExNA9Nl)md%DUtQF8{FSA8@YhaiSN`gycIPj7KWU*VQDyv9q5AQcyc2V8wXYh&U+eobY~`QZ!#`_x-@nZF+}ror)PHnW|9C(C_jde!h?37k4I|CAAIWE+hVwX_hLC*jX#|fW{7*S;L?d||Ne7dBzG*a%qv<e`&oou?SV^NuKF3teV>OK>`Rq~+k2N%&<nv0Cc$`E>k$gt!XdaKIdXmp2P2q70HIjT5X$FroXd21qk51t61e#9rnWNb}&Ze0ppEEj@$5ZJ<lFt^M$>W(chvf4_=kj<iolf!@q6>Mvkj^Ig+|WE8=h68jpB1{4$4lvAlFtWS!Q&M)pX4(^*YJ1^T}ARapc{C+fvzL@?9aYD?n^h(AR0=y^LRVmLWAi*x`)Sm=r-D)4xtBle1PtvgXnO2n8%0dK01_+pcWomXaRY2Bt638Bh*Y|sEVH8@d<j2#?b_Nn#ZT<Nt#Htw3NrC^eolUWO{+e7w9=^pe9<*<8pe5<h@dF@c0J3LdVeY^bU{j(Cc&@okSn-_yN65v*;B1gvU?lJvy1rpf7m*f<B_t=p6c*$FJ!#I*Tr#?|J;5zM}JJF8#>kkMu2FM3>MnJpMvI(PeZw{lViO^c!7CR}-l#+5Vzy>3WK(YuU8Ak@lgR=|;A-)W7IX+K|T$RVQ@^-AkMBxQW_8-AxbD<~(k$Hdgo3LfVqYE!Ae~A!?;<c-%&9p%&4jv@MVFUZ=-tF?Hjyo9e2bqGxD(9=BKB)e>4pJMg%J%2v<Qi?lP3JF6Yl%k(Pk#^Y{k7xfywMSXbeqk5`0>0Qd@F<13g|E3SAfX4!rqu!@ashG!Nm9IXgFR3q&eN~bAoW7xQ9?Mm!T0uY19z5=$;_5qEN&R{3uM+BK`jz(LQQk}cJN-%f@VJi}sQxCU_TzCsHAoq?wi?RgP&HVsqi&`3cwA2nQ-_uoEV_QO-*;xYc#kdm`26wQzHt|C*SV|DhnC*w<c;6^t67-8JDL4_=JU#3%<+8Y_)hj;^Y-HwI9c+Bb3<A3h8#j!@`km9viQNCgtEkgy$xl_J5?8QG59yT7~(n^@^>=q!y*^MemdEIpH8waPKNqA8Fb=g&|9;MLAOo@{X1FmF7I?|a7~4=_zT->DvTwru)U_jSn?LO*Hjow-oo~p3S-Gz*j`g%EO{s67C2e*hI2z%@`fBjS@MRpgtGX-o`kZ*gS`!9$vagSaxwTfyBOj+8S-~B?871#!+tth@=n#o$xvS>gHD_bdTVwu=+?=ge<x@DZgA%B250_m@PGUN?=o}WAoKTLGWX^FTkgyK@89P+n}1*4kH6$^ejGpt(Fp!JoJR4N{I!g+G>&TctCs5dtAVEQ*D*AMzmBI9`RimlmE^BaoXubR`7@00&mHTZRqy-H@I6oUeGc#+t?`ea$p0S2-_IsRYtaxMhtMGZKF|I<?oWgL`#i&W98Sah`#gv6cnBTn-{(1u$HVAg+Jrij$D>Dw(&n@!9l_%fG}6D%Q^}+J4H>!5Q^jKyjq&gEjOTGYRr~jOCh|CuCQuLBktXpd_kwn!UFm2ZkES~RK2H;mO*GlR&ohn3Y1HW7=b6sqbeihl=b6dlOgfedsF+UR@dP@KN~kZL#N$ac%fHVvhsQZI+rQ6q8jq*ZDgJ$)GkH9dPWSKgoWtWebQbMRI(47tT=LHC-%{S`;zaJcw>7uNL&sc_Sn>PZcDeTvm$HAacKL{hFZF*nX^&I>@%A_sw_Q%<-!AvQXI|j%;-L@BT@}~C+Z{gFzaHD;lz(%3oQmt@8J+w1`S(Ba<H-Ei@=Fr&8=j2JFYRy{pIaT7Tduk+k$lf-G)|oxkIJdsB6Di(k$GlfUT|&{zU7+>gWRHUbJK;1<a@fKaq8UWsGQ0z5+{EzyEt*~V=E)`<0~&o%ztHhWS%?fGCp@oWZvifq&A{*>fCr#PURMvQ)`dR3%bn<&W*yKK5$`>TNKXEzc67xM;L`u=Qc;>RBn-&wNwGUB@#n#iNw%bA~E!qNDRFt5<_o^#L!zJG4z&5480{1LvM-1&|4xg^qCHsf0k9i^9m=!^9m=!^9m=!^9m=!^9m=!^9m=!^9m=!^9m=!^9m=!^9m=!^9m=!bBs{F>hJ4XuGwlvMLaRFHN`E$_V;_gcm94|%j+|GCfHihzdav*JRx(T4;-&>`M^90^l#56l~1B=EPEW*l?a)q73S&CN7mgoA3P4+;+Us3s!v!gsuuTcPRu&FLhU)NHN`E$t~%B}(YN_KRhVFF#dBRXZR^jz35nsVFZfiTzpK_Te*({S)xE8MD*uE_1Ly<$lW^%FHGeD2-vaZmrj54#vX_wmYC1t5;1-u=VE$J0cj>3Cztw|FOY9Q|{lu-mOIJL99P|*J>(W(Qf2#+VuE3`P{aw0(`4f1qOIL0Etu|b`LLb;4r>;`-x5E4_F#l@0YU^*c;nEfQ0Jpew1@pI}ze`tb{h{umx^n4<HC6%rrvmy<sD4<V70^#Ap#OyGr>#HqpHTgPPX+qB^aJxJ@LZRE+WJHP3Dpn!!2US(lbXL3<`4CU{*&ep{U=mE=mYH356s`%o<H=TG=HlHmrm^c&eYGrP;Ip51J5NA@N+p-1CDvp>fW9YJl{x*6;|Jnc~+}wdp_`dqwTs@tDR$>)~G&Vwb0aqviNH|>cU@JQD^?zls4k8^=V!HT8lk2KQ51U_K&a2|L(%yHN8d;&_nzse^a)V<S)W5rl)BMe?3Pp@|XNA)z|1D|Ix+%@fZ2ut^EBpjvS+&JocoW$k5u<hsQp&8?8f~D4)lC+MU*;4XK#NV#=cpXk+TjV_zzwO=vT!;IV?r{QJ6l^0+4@Xbak!2J$$N`qMVFE$z#r+$Zfy-Dwz)@?ODiv^^cj<AF4kvPsd-Jnl@xX$RVsM)Ek44)O2n9>L=gbU5{<TpG*cSQ<?^R7m4_98Y8X_v}sNaUzYQQi@X@k9Bkul~X@z<gt<JX%8AeQ+b?94YU{SL(_SjPSa=*4WScwJb`A=VA`Kf;_)Opo(`ZL{r4@7pxJZ~9Y&|~csiX-hmuEU@pu-UMx&^b&gb!bI-8E9YMRI6JUWl6XaZfr<0UlLzbAh=kMg&yC(+S#4UgB*6*QTe=z1Qnr>p&Y^*8f)Gu=SP(oDLYM|rQ{aWsqW;_)uJjZUP4X%3Hb=x#cN&ZGrAE};A93_6D%=J8>Akj|wGsfEWDT1Xer#q=nTkJ2K#h%TeYd6d69Eq{~wNgm~IN?%3S(X%{0OHa|YbR#Y0aVb4RH_@&1Jde-QGLrY^z0Bjw^a9;M_s}am%HMgumrkYodAy%qCHXw>`_oTOBtL5$&dZjb>+{k5zAkg|rQJNA`Fq^O?6**u&vUZG6PC~6x>(}DxuGoaAcs&EKUhmBOT5%Rkc+{8p^G7Ivx^~rCriB4J~$cn)5%a5CqsP~x>(|Ub-*QoX2Mwfg{@}7SmFs=&4jVU6SkTOV~HnhH50}X56%r`i3d4^viQMTLRsRa_JLds{tI0UahqKX`8!$SrS`$eu%Awbx;Po?yU@k>9*LVf&+xxbd1~(p;I#KqeE#M^{`Y<QZj?ZO^x?;>Zvy?%$Ii=hB+$Q&PlfeCf0vJq(RLm@ZXau#4<5HM+O7+a1GhNlX?6KPKCS5QSXV3hyL@1OS{?h`3j5sZs8=i0tJP8W)(~wZBIqX(K|hHI`bk94Pa=YT5)t&1h@hWD1pOo;=qC|DKZywXNkq_3B7%Mr5%iOYpr1th`dQQWfw<oLvFcqPqxiXPK7SSQb6I&#o8Yhh{G4?!=lekNeb0pNgYWSu^^eFqI^_Kug*+DW^JsbhMhTB4{JdG-zfs0x89%$1_it42Si#TkH{|E_d+@jiKZoAbe_p>STR;DEIs<te$j_<e{TqXL9K_G<yYO!=LwJ<`|4~=|J!O9$<^3Vu`S+UPJj(k+viW)S!8{(!&-!=b=k<s3cql*5-<5y+80kOnKa8L8_u=RJ^1R>U-#j$`#<4rwXqwj2y?oiyrT+VuUA)$iE<SHsxnr}7Zy3?Z=V>ihIr+rT-<Q9`R?gp@%zi%ed5c`k@qFg^PEP%eM2_3t$&xpm8_JS5<Pge|H>@R;#Siu*lqDYQZ756LP@_-=|G0}Gu9G2uC&NCJyBPM<$*I3dD0Oi%)Yr+N6DNb-;w}c=IvMouWXZeJYdtFLHDy_Rgza@?S>_kE*N$b$N!VU5mL(5idyQC@*uwU@uq^sd&e=VUB{uj6EU{t!fF(BM6R<o6`3Ed>!FmIh*swo~V1KMn92w?JW5^*A!&=H+4Ex|@$u+fyPKNz=GStq=Q1^Hg2K}Tl=q-&U*RKv(5NOr1_y}9AT9!G5tyV2dY+<Wa%Mx4IYSpsD7PeZooc!HqL7-L35*z#jme??Vz!Dqs30NM3`~#M`V7&oLY}lVgus_x(jtq0AG2{@5VJ+n@hJA2y@^|e8fj+|+_TR}+J10Zk<53v&lg6O8G?rZFeEDLaRm<WdY_)1x<`lMCwJfoPtyV2dY+<Wa%Mx4IYSpsnGdXAXG?v)lAF#xR`2&{NkWaw!7~~(Y%mwQWSYpHeEQ0;9K5=B2GmRmKNDON!cQNdPlO@;G9y%HJ-^oxrCqv!iQ5f`-#-O(}mRx_@rE9`!)w1{qTdi7_IfboOElX@+t5wSqTi9yVvcwj)TD2_tOwQRojU_ht2Q0B+{(vPm<P)$w2KfgpbHRE8me{aAi(r4OPaGNMOk>C)62n@`T@3r+WXUzPhfaq5cQVw@$x!!r6bAjIG3YIgCD+GS?h<I#viJyFty-2jg{@XCOKf4QRm&1v*lN|X#1^(%wVZtK>n?#-ElX_h4_IQu`~gdB$R}WV4Dt_H=7RMGEU{sK7Qy~lpExqinZ}SqB!;z=yBPMt$&zbo51kDA?_{W*lcDbMC=B{ZW6)a~Cwr*}ebs}$>Oo)ips#w+S3T&f9`scY`l<(g)q}q3L0|QtuX@l|J?N_*^i>b~st0}5gTCrPU-h7`deB!r=&K&|RS){A2YuCpzUo0=^`NhM&{sX^s~+^v_8Hbv?qb*nCnx)-2fcK4hW&Rk)XvFJ_jnWr{iHGIEsZ7D8J+6_ty&fzVXIZkGN-WBs%42SY_)1xVhdZXT9(+tR;!ki@1?E_v}##mgMYvh8|DvKVnaRw%VUs#z%m!CH(-ek`?Co4$NI#PVa_y$9MTwaE=Ptnrg8GU_;rEaEW;kAG3<F7Lyh9dP}4L94WzNe&d;A6=qHTDU)X9Xj3t(^)m0cve!^B`VJx`{TfK#`<SlHq7skoYhRhCh7{-z}oEyrLH{=k?k~gd+l*JGBB$Oo{>}@DZ-cX}Z2LHH=A+D1le<#B}l)D)A)5(%|sxD53`Z^hO;$+ZU+{K_<CxiZ-T)&wKUhi=6?nQt4_lLXOvre;%e_!iEpX)c9?d0rH5BbdBoy>kd^Lb9@cs_G{C)?LMcpZyeEP2DZp)7er4xuc0!&*XF{9sQ)S>nOohO*=hH40_$kGmM+IvMhJGVFtsVLzR0U+)mzxftpjcQNS1$)GnUgKnJ+`ggMAZSU<Pi;u9qjx5Xk!uHy+EIA3=>&3F<A#AS^%Mx4IUKf__YajMnuq?5`KVXRs^9L-kA)kQdF~~n)nG4n%u*8P_Sp@rIed5S4XBtBekr>wEWY`BM+t)j+R>K(fKkj0vos*&Nkr?!o#-O(}mR#+<ePr<wwpz6;a|&CnT9(+tR;!jJwy@QzWr;0pwQAYE_F=VZSz?2Kz!Dqg4_IPDJ^{;Pkbl537pym6i4FU+2=>SN#F1gnG=>}^F|5VOun$hQuXk8|hB54a+{I8kCqvyMG3Y0aL2qd+x!QaC$l@bxwQ5=B6t-HmEU|^HRxL|xVXIZk5?k16)v|r<!)n#C#0LL>B{s|-u*8OZ0+z=h|A1vKSZ}}*8}?@r?2q+{Bg33&3^_z%Sc{WkADnDo@38s|W7z+=i=lQ-hPp>$&`%nJ-qKidwfFXs#Yfm`)w0YfY_)1xVhdZXT9(+tR;!jJwy@QzW&7HP)v9HQ4gLX3Y?wb_i4FM#ERR9{0n1#l-hd@G?9U?DAL|oGhB?z1a)`vR7AM0#IN845Vf7itu>WxvL+zXlb&tfLpEL%&rLp8{@9iUtkFeFMWtmghYSpsD7PeZoEU|^HRxL|xVXIZk_O%bIRm&0^`~#NQFn_=j8}bQQ9)tV?mbqZP0ZVMypGB}g)+de(bEYxm5Q$+ePKJGOvVFb7>NAXC|Kl!(+Bq5O9*IFeX$*Qx<76-Ops#w+S3T&f9`scY`l<(g)q}q3L0|QtuX@l|J?N_*^i>b~st0}5gTCrPU-h7`deB!r=&K&|RS){A2YuCpzUo0=^`NhM&{sX^s~+@K5BjPHebs~h**?QsoDBQmWczx@s$RM}!~Vxz47GDI)IAb|e$p89md28+y|<4nKEhV3mSs+1t5wSqTi9yVvcwj)TD2^(g{@XC+t)s<RxL|x@DEsG!~6kDY{(~Ic?|LoSmuKD1}w2*e-^?1Sf4mD%$dfJLmETQX$)&jWBb~N)thD5!#FbRc^X5F(im!*#-M>Tme}_Gxr@bL*lH<^C6=(&RTxWt!d7EpEV&9>y@j#lEo`+H#`g6NtHUssyy4tXmb@W{P?o%5Euk!auqUA`@nCO5S@MP&g);cZT?}!Z4EZ}5_QA=ppH8-~ci8J9jG?}97lTfm40>}i=+?=ge<x@DPW3<X?^I|04*Wml@4&mRDc5!6x^`UGi|ZP3T^Fuv!KHtf=3P2>Y1^e|mxf)sjq*3ue~c9d-~WI6`|7;rR=akWZZlf_KcUsuHPq^VT#wCYHPcr!eKn)iOkd6P)l6T_^wo@3GkrDFS2J4uuV~e!NtX^?+H>j6r7@STTv}RF{bc@sXaBVS-&yAWC-@Ki{|RR9t7rcIs+rfV{u^Gm%KUu)pLu@h`q_=o+y7I4j<<P!o_Q|%&(Lb?8fx`FqQ_>mn(3>VzM9c$rmtrDYDTM>zM9c$rmtrDYDTM>*NNKKPv*Y*Kk~kM=5?!o$m>@B53o$KJO', 'harbor-cargo-sack-01': 'c-rlJ2Y6IP_xG7gFVd^D5I}m^mdysT_fn*HNKiTf0)&!45<*u%nt)V65J40{1*s~aWbZ`~6afLj7f?~LV#NZ2iuj$mdk1IB?2h^Wzwde8?}2^p@BC)=%(>^xIWu>5T{CiQaytb8uDt<Jv?M^M-rc)Ri%reWPRogHJ}q`+T1Hw{YEEWWZ1dR8qp~tHGP7ew;*gluW79H*r)9--Y}P#{*A?fCb0x$!iOo&R%1+PBKxIdqEp|qe*z93wAhx;9V%f3H`%jC_NF9fLvAxarn#5*g4maPh4V*FXpVqY4acSA3%%PV4sMM^XnORMTrDl!HY?_@qY)n&|J(dm`mztB7m7Y4*KWupB#Gzx;dZ!Oh8y?#{Cu?Hb9Rt~^8N=~@<A-K-P0L9gJ2rh-ugr-fN1<EUG}fW1*=cPu$7W`=OC4rL+}{@G_SnpS3HEqLe0+kdi7n3M4C!*%6U~1fk1Zh)-)Lf|URn2G)-aGPcDp-$aUO?%q|<4)xf2uPXUu34DTGm(8EI4gWelza|1A<733j{NnP_?(?=m~%9ZtL3;h|l2o4?DQ;IJpST=A~|dr{=1rH=iVLD(#Z6BBIq!~}Ojf}6VRvHINhc#qxXpn>_5V{;^WY!0Wx@jr{g9GX2UsBSYy<ire1&B#s7j-h23XTv(gXtL7BrRSvQTFR+8Ia%pLC+4J?A@%6qyJK?4?%m8=ckAA(YpX7?&FxKMliNPnrhE5Z_YbzkHh189NzWLbK8y}={!`XChEAu*pz9xl@qq^2yuk$Cpgod7&p!qe0}a}3yhXd6H|dyRF5lE)_+EBqmVXk4P8=~JEvrv@+9WgZVVUE`V*zL6Bu^QSGZ}ApxM}Ca4BTs+ZW}c>+03@n=5*Mc2~K-LLcGJ{^k8B=c5Jxam}_UeJKp9tmmShXSE9piv*SBXnyqx)eEK)V_gwCTM7P5o?{K+X9%o{F6I&DPwkNuA{l?o|SQ@r?2ad=wU5V|}wv98E&I<3cUBcx^;~oEMydz}1Gu(LRo$>K**PZdb+qCM^s#k~wS7Z;|xQy;hy4_~&Y<7F1!<Ohs#3@d2INZ37Yza7-t^|+M+$Wszel4fN<?%S;`DwR#{5D*UM0>o`WiHA1!~|zz0&Xep_;|N1(N6PVOZ4l}EI1SF9(R;X#7o2xX}tSijStO4LgY-??G8`0RCpr0;P80<Nreq3%ADf_hX<!I0cR1X(42OUlTM_~kzj6ii7x)Z6Of5e6Aq8V74VqyuLrZo<-`@_NsN+)M2Q$8E-2f-G7y>vyFGFuoQdv`JYY=!nBey%b59yNB`2**TE@s6JZs>tVD)q#F~U3n(FKa<4N9FZ+)w`TM`EzQM|M2M9yH$LcKwU-{u<=R+wp`FWWX800Pe7kAOjA!%OmeWr~!v9!Tm2nh<Dk7LcmE$aQurobi}&@4LDs6&%c-hrz^yOJKpJ*_aKY`Twnht1gFgvTt=>clZAxDpd`5B@gW*K1$P#OwIKLHcE`J1_%x3>{VG7~j@{t<o*ota|7MDKX;(v&zq??CPsG3Px!+59_wiSSJhrA*hw}2j5M9Jk-^Yy&%kjQC=R;VI{+s;N^fjAAykE&my8phjyduusSI7%(s{Ne*zU5RA=jOpH;&@+`^C2uxidmp~i$6!l%#`7kj^(K3oSVI?XC3m%@XrbsS8vZ*=1u>ynl8hyHkh2$Xuw2otJpXxetiFB->l-<Ug%#(ir+k(q9;3-n7+yI%CpmS8v8HHj&73S0}gt18hfkQ9bOqueWS6XZ>kJuv9F%hT8h)TrLp7OO7W>j2B<W4>YEIo>s_ZlcXlbQr<pSRO8R_t_nC$2Z@WM6$?#hbS5{}Vn5#a2v#Bn_&sCV0<b8gQTA^M?DZaj{qT645RQ+LtSBkIeHclU|Ej4|U;SKjs*J<ppuD-NMh8O?tL7m24q24jC45z-)*wHsthO^jz+ucu!)48Rw<J?MdZTwV~#!h{c;iD!lP*vkkvo>V-&RS{e8zp{IPxsFA$?%Jx{pNkA>2>wio=Un5KQsBh7Cj66p%&@klHx0u6x2`c{aYRPSOY2k&3A+KVVyvuzRB=r6*F}j``}-UO)~uN_I-33dyyWmcx5>CjmD0?sWP0!e!6#(6sL1bW5>Cb;zy_TS843jHyPe|MI-g&M`~-dHe`5@MMc&2KgDPTKcC~1;oE%kz1eN*Xod6(Qhd8@a9%>A`?PWW3h6Su^O$qKcYXJ1wMSg@$?y>q>gvyou50=x!;i1F>ooRRMHg<8;m_QxtJB!W^_%OJ;nX)8JNhQYS?mQrFR03JI=3`-oLjF9UtF%3N@J(K$?$!xXL!rCvYE9Z!w0>b<V~LD(9RquJ{dly_^PCd<Ki{nUwx%`+=$2WlIyv(jT06~@!Q)+`O1Cg)Y9+Emf}ZCZub3r(`Nc6!!Im<#YbbWd9L^-8Qy#MHXn_B<AkDK8BTqpv7>KNoW*|T_$(<-=a$Bfb1TIs-|Fb4u~Xk<`0FR$@ospzm024y{2TYv-prl%YxTBQ@yT%8SIxXl7q!)r^X5qL<aeJtaPOEl+Obnxr1<EU(|w&XTWY`kvQ&z{eEMbI;+2}|n+*Tt#JfHkdy%pYH_7nK*@t~J_G72+^U84Q8;u=(lj1D)dfV4XaXPm&cAQ%&zWK@yFO8l0Cc}@GIqjW#rkhzCB0g}+Ht*Wg-L-bMKl4O9v3RQY`{P};-B(k6B7W{*tE8B>J89iEFBbAiql);*v5wkA*BBx1Q7+fF{bXnJz9Rl@>KY&QKl}62n?(Gh9gBU`|8AR0dPSVxm->(Q6>{c(JKHoNr}IGl$9WL)vbB6(>OZ}&h+AJ_7!+5ut)nGA=`yOd+Mt$S+e~}?OP4YDQ@hUVe6jz6y7XujWAN-aL!?u;LrL{Uzfwktk9r!szDVb@^e25EtgUD?Io~Znhwr~t<a>Qilk!HhQcVMN`2IoF`x<qt6f|;I{^sL#JQq3}$8UeHKQ#I+Riv}-xmrfkK7Z>4Yuu~x`n=B6omu+ttx6e{Nf(XR=XEB1GeT{;EXJsGQPp^TkxsFv6s_6rIOF*Og#&c>em*av9GzU!Pix<~hCbuKZS~~k@!Cbbj(+sm8l9j2fp6YWH>dsR+h1%@K<;>bJ}>9mxz*Z5fAaOHIn@x^5$W@}yIp#_?|jvQ`mL+eh5dXU>nB$*QZEqwQnhZvem;*w4^A^G7r)}WQMIft%5~)mV+~uo0(!#P*HvDh&tsupZsV;V?$y21n+4PWKlZf^gY?g`3+vU^P0~d5z}w+-J$T;+^^rXneK$Xvpo#2=^!a*d_jOI}?U-vmdulsjKVK(&Z4{r-PrK2#yxOoEXng<3mLs(}<2>rw-fsoe!@5VmSARWGRn0y;I3VvLeZB@<{fDT#y;r;`l_nb^J0kr;8=mydpS9E5toK6!bt3BLYvWq!>Ucfno%B~nVLx93ZT3$$79E)D-BP)t&gZ)M&}^gl5xe(dv-PS-f9Wo#aW$rwcjKk_fV_+B*nY9;pEW+`t$c85Kn;lOTpzMp)yEc7OLxo)s0Wc9k$#={QreXRg;dhKS3sSJ`bBlJCsWmut`^b8zj;d6wzSnsZ!fI%S+O^uuK3#E^S<qqAJi=my`x?@+sWYV@cMiWY%RY;eX;)r)&0RJLu5y!&)3QOPd@AW`^HkW(YYL9KVKWizpG_D_QK0*w^a^dfBfQfqmu0%^$*v_KE58-%^YFOdw!pKq1tqn*Wqh`*S}q(kuk5?(`uRPO#^Cxx5JNpZFdd*i9u`BWM^Ovi0oWGJzHJgW}CVrVN^hEi0p{;9bf;YPM>^SJ^4c0fSM8Yi)!PmGS}3<4iDB!PB*;6n-tI*&ri`dID6`%y5e(vM*CSUT3*u@Jo}R_8q3$f{zGfk+?Q<HCrcU_B0C~|zBba!7tky8XsMkzTu<2FzuYywYvTtr&-q7mzE1f5JrzqBIp6frK6tfYlBkw=oxOFd8P`3Xwe=r%^NQ-~P>+&E|7%_?_t_&Vug}*5KbFt?&nIi>AFp<4i>ui+-VQ%@$hRZZ11(x=XTGW#P#YpUBK_R-lj^Wn`e^F%Je98*zMroRUWcy-QT>dW)=EpO_>NxjP$6UE_r0~RPX4XGuzt2Gs+mg%ifXgFZqYMOw>S8)d<`5cx<j45e4}3GkD&oI!;cl|^R?05Q%)bUYqXv*BUjkZ*Gc)91S7Lej9&4<IAQ(pIs@{uj6oag>mx@m(na;d>lEHI$(X(-LEqQLt%~Z$6<5>Hf2yNH*|r+5|3JgzzV`;Z^;e#rDy$!V?8D>gsAZ2X(*OJ@E1)(+c0~Goo&27BPOZM_h+g*BUc!F9PWXBd)k)!b1GG66<9rL35#z;G6SarmUgOIhvq<H0J^q*4TGkhjB;EA13#b`>>}~rzb>H5hD&&q2s0Wc9kv?A=m&PyD=bpKx-dx#R*q_j&s&VRZMSG%TO@pruQGc&xZH;EXe69ZW$QL?a8+`wuLxYSPpZ}@Ofv=N9^>g2v>v~)jqE$Ydpz(R<$MX8|L(*FG?)<iTV9l6-8W7px_4(T9^FnWR-u7Je{GqG>J0cyvHWqgIT`iC?(z_;hu&|%64Za>kb#iWC+JR1gJ*@57P%MehFR#z*@OkI;MLK*xpLbC|pLbq|@8@&P>xgQA*WvTU>+ty!>GL{#j(B~(pU(@g!}p7FVST37?#jFJuDmPn%DeKeyesd@yYjA#E)^&QjX=Sx9u$P45Qi8C4WI}V2OFXdnm`G-2V96Qa6l<210F;VxS=dm0575!nnQW046PAcLlRVid!Zd-J7@`2p$2qD><n$8I@E$Lh+Uuq#6T?cK<okCpbikIi&z(WL49Zp{So`a1JDqf!C=I}&=;D59flwdfdSxzct}G`gJF;Wi7*Or6pVltpg{&=28;$3+CUa!7L0{f&>kisPJ#(=KXig=h|^#qbcC)j191jSf$q=~W+BdkhoLvz2Pudt@CfvQey|8}5zL1NVGt}qTmlPVAf&=F#AUD;hQe@o9Px2j0V5$D)*!Bd)i4G!;c3LDVI7QvY}kaj2{yoZ$c5(-pND542d2U{#BHz{Cc|{tj<_9Ogoj`z>_*%TJ7G2?!#u=!@G{JSg>V4z0PKZFVJYZ{I_!tXU^yH_JP3KP5>~;Rh;PCncmmeKJBaVVTks^Thf|2B;5a-5&%#;6v+yo#ge`C$@jSc-&%svs0PzDj2QR=&a0&4eT!bC43qC{q3_gK9Fc<bA?t{<aRd^k~LHq{3gxA1;9}$0qE8v4S;3veN;Cna>N8lRbHTVUN!rO2Y@h1ER$KV9qLc9gP!$~*;gq+0dFE|bVfx_f8UO?W551|BN2~vn$fRErF#Cu3F@-ci0Wf04dQsgqc0$;#oyvmWU;5)b%@m^Aad<$2hCSpxeh5P_NLv6&`qz3sFu0vhKx+Ip|fIpxiVnb4&{0X-q4l#~2CVxW#;zV?kW<()HNCIL4v6F(NIB9{{g2a=eq$Ei~Od^S-G$~73BDN$dDNnwJiij0SYf_0+BOMSsko!qhQj2s(>`dB|>LiAAMeIsCkvgOv>515rbSL+b1|%6Vne-x!NE7k^;sYdwG$jtwAF)4qkl2Wu3_=`4`VklLkim$9$pF%vc*#)2p=1crNGp<tm_~+?Hl#9Xi`bToAON+YCcdgc6?|2Ma`-9@CGk}Z3gfGQxi8c--z{hM7shrKlmH`1JJJzfT}U^4^&q|R)ra)O*Fchrui<1QzB-!k_BQ)dvE2>jNV4_k_q^@)I?dmQ$nY)e-t>NW+8vQ^xcYol{^Z)VcWlaVI(GLuTSQKMh{jvyoG@*kh&z%e!#l3iO`m%{uvf?jeDkcy2fVOG$VZe}W!n7g^rKRoj-@^`JK;F>fpX?gIG#A}HGeF*s!xW0scbiWemlk{<Z9gGCO2}*3;B14=bJVU)GQ>$=~(JBvlEU}A1G)3gyV}EtTS!Cw0)iw&ndLr^tpb;DMG&Bp(*~@7xWPF2R&(~%{8r)q&OXG`fS+=$EgpLGk?PIg=0sWHv9haoD`o|sjumC;RS1i{GriFCeIu3u#iu!5NFz~xMGA9r(>zl%uYB?eW0BA6OK1}tb}QE@bCMict-7lrq82dwhH-|E5A*md|Jj5As?OhVG^}DchyWOPRCN8nVoQ)`an7JCmb(#zK&`0SgtO`%Oa;fABou|<Yg@G%ULPpr7fGU)toEE=~(JBvlEV&wK(%99A7YRL>|kX41fH5hdk<YI?k1dZ=G_F$*1F-i}=`8pB!Mhli_qM^_kfT$EgpLGk?NyWmZKWwb>8XrVNM1MSN_Xiul#P&Y5xPxTZw>>z@0~Ijn?hQ-;&A)MsWV9H&08bt>X((uSL{yoh_R3?EgihZ$Ea?sXzwbY*>$AI3dX#4mIyZ`ynu_g)!J$5Nk}op7A`Ksoa#9M7G!%(Qt5pRF>y&OLKXpO53SOvHa1-^b*K@R=y$J)ZKKHhuVPmEm+O^_kfT$EgpLGk?PIhaTEw+B}A5CmFtA^D5Kl?s!%aarf8RChv!59ue;l|Db8}Q#?D#a5|Ry%<P2Y)CbC$KjHY5KVLL$&fQ*Oj|~4}^E%V#DvgK~-~a0jlTT}RVYdw5)jrj{*E8B-DNe_l&m+rDG){e^ocS4zbGc5E;auK@oXfkAbGeq{T;7G8%e#<IvDWgDT-7VX>sjmijToDd-?G;A>pA6xJlR^ydutYw;<v1I&FqBZ^{jQx{0Yaoy;_QM`?ipC`?ipCd$knj_H7~O_H7~Op2bp}doBw(_gofo?pZ9wx#zNwbI)ZVf5kd$4f=hb6wkBHT_a<*3i%1^+%+|0iIBfwoweqynkmIkSm!QgCmheS&Rxu(aGX0!OL6X8E#%y}TFAMxv=ryg)k4mltA)Il^;u~M=1ztWwLUlD*;UBjvpzTB8Cb~sTA!8XVeVx3d)DVBW+xmUYJF~E{)FS)XJIMMeJ&Pq?sKt_bDxE!IQO|&$hptOLO$R6u45POy)t~f^}UA;_c{@uZGG=?3inJAPqx16cpCR!89v+k-h<f*$H!aWdoX{(aqhb;Db9VbCFI=qT0+i!mnFry@3n-S`(8`P*>{zP@a!bRJ6YdbcEGcWh!3>Bw@k(}kBGDHDnG!plMEkdeQ(L^gyWs8?=6`>;dqC`3-d}}t)f-j@s?MH|FnKx-uNN+YNu|TmEwOMJC^t4#j56589r=bw(ma&-R4*szW2s7UxLG9j+NoA9&>%9xm%jE*biTSL5j0jWI3CwVlO=<#aS$LtPE#!MaRl;7CRj)!^bNn^18p~&z%hKVr)DxcXu^up0}?_-mXT~%v{Ux9ew)xCf)MqT88)griZW6q6BlS3{O6r==;8`f2<5=vGa2kiL+Q}E@U{HD>_z&v)E-hi$#{RxuU+waEv{PtCOf4V^8Ap9+hM4Ex5Xh%F#D3m-na~=gP~~RaB01<>l%mDrd1<brO}cSY$byE32-eau$nKCs8?@D=Y6&Ig8z@tEe3J-X!ih6_w-Oo5VeLqH^4Olep(vRE~SEmwWC+<+%5Hx#wC`j(e|{drn2=EOvgbB5@Xr_1uZd*<4xAwWyrMF3VXgvYgG8^<0a}Uuic$tI+qhy1DQbp8G7WbN!V2_}>+Y#s=vaoQ}cSkJPVo{rr6m&So^7u>RZHbk(X1ysZu_wpF*dPPriVfLQpkqIglquyj;DM!w(Tdaw>37avO){ct+Lv6%j!X>HTS47#mu(TW%r*C`jx10M@Nme&u`F)SU8kCE@UxE`#-$Hm7IMn9ZRa4e?(bPT;OwPA6ca?w2SvG8Mg{U9B~($V-B`F@M*!8&|gd@Nz~!|4RaV){?#h0Z6PCyUd38lrjNW8ug0`awFnr4tY%-*0g}Sci{`k0p$LIGx~FO#f-!)Ad5vfyHUP3+I84g&)i72kH1Moq!nmev9kDI(%GwEMfG+=>*4O`Y(!?^T*)q3*+VW1v<eodV{zgM(0jkf>>m90{j=n#m%$9&7mlF0s5kNxf&40%j<A?5yl%qCpZ?JizOs3ZXFri8WF9{0DZw4*SIw<jEmRd)}3f=M$!q6MdxA(iHqAO4Q>w<?Y#l|f<0X0_HbcbybiaoiuT?}I>E8%Tr44RanC`Wd&Y^LtpWOiXSBvWqg7E{ybkx=6g^wD2s**B=v*uzaS6_NqO((gzTga|^5;)sTx|zvJJ8QJN(7uyMQ5h~eZd(_=l##;Io7J3=;!1J`r*&sf_S5xZw=1ApNHCss4t2)pXc6)XK9%;c|Oni5zo>xXYzcWdn2BuWzOXJJm*I|OUs<e^Lg%#c$StqljrlCAMq?Lb0*K{xi{ijTINii&vSmnv$V{aJfG*@h-Yb;GkHGG`4P|3GH3F9o_iynrDe|K`8?-GJWI=*$@6*cjd+%pIg{t}oFDNlEpsN%=ealHSz6{yp3ifB#Iv-_nLMB8-iT*unKOAl&-oG0(lTfAe4cwFo~32Z<oP`3M?6c*oXJITg*p4_5zbC(n6q)jGkHGG`4P|3qBA+~f6LyJ)$fWmGA0*_*G4VfseUzeys2M5d6ypdh}T$us=T)T`g#4U>Z7<bsy`lnEU!=d@I5`apSQ#7(0k&&^)U8z)YGUAuTSlvU6tD8b*K%rWzI9NL+^?AR)g;=(&7E#Vl)KvWAJf_`nmfWf_M%7Uc4QCEElgKh}Ym_39^4@EN_z^E9#e+pMd(ov1abAxixcd&4XDt*8GRnp)pZgk?Kukhx$v~R=ugzuH|RgI^pf}V|n}hSdo2RpZ8x>Kb+47AG@d?IQs@aR@5(=PtJcsFh2oxCDP~bE6A6@kLC6Gds*Dz@?voHtaEEqv_BZ!{-AQ}TIcqnkbd5#RnMY&)3|+13%1GYSozhseL&;(y@>t1P2L|aMnf<^1|JJ&#}MfV;^lK;i0p9j8iIHYKCUqJta1CB#_c(3aKB)F4BmgM#td#f8bR|GP*);-t3GvZ{py1K!Ql1>o!cLbNcCW?O_kg0BGwykpC2pg=WX)-b3Pk_`3b12FzeUg)~_D4W(|>jUZ3|zR6krS1|JJ=N2DXjS3tdq?4Y6+?b^E4JhO(#m$o(vD=h~&IaA|hN=iytxpix!5V>t@ag#@q)SqyY`V&r4r~GoJ7OqYG2`8C9yi7@{XvH9w)SqyY`V&r4fBbT$7OqYG2`8C9yab4`=3XrQ`3#l*e1=MYT4StyhPM6r43*3uUT(8;9ZCB087lqx43++THnQ>=+V<x&R5E{fnUWH3<xwpC`3#l*e1=MYKI5%?hPM6r43*3uUgC~o<xwpC`3#l*e1=MYK3iJ(3~l@K87i4Syxg|6la)uY^yf2F`tuno{rT)<<ukPH&u6G){_s+?7xB`c&rs>lXQ=e&GsVhhXj^nKe|QNn#LA;s`tuno{rL=){(KIx@)_Fp`x+{lKfK(wb+na7vGnINRQmH7D*gE!ZRInx?aybZWd86nC1s+ON3rzhGgSKX87lqxoM`2fm;Qc#K0_t*hnMuLr@&`qaC;_u-fjt$tbZnZ?r!nR(Dpx<`EScVawcD+TY_r#PMi4|C}*;L(rfM0LTT;SA=28fL!`A|d#(LCq;2ijA(HtMD7RXEh^613Q0ez4RQmndYWWk|_WKhmnLoV5q3p~glvdtDq?P9oY30|-eQ4XtZ-`|6@N%1Vri&!4e1=FXpCQu9r)uRhq;2IhL^6MPiSMb_J}s2iejOsM{W?Ti`?YGVg^;$jUx!HM4=-_yl}E9()^Uim)^CWk&i8C>hqSGA8zPxMyi7@1WzCaV`sXWD`sXWD`sZtvHD94^|9pi?<_|BoS)Vl`No&1^NNc@@NNc@X^%mN;)@z7l{_qmupp{3l^yf2F`tuno{rNm-<ukPH&u6G){_rv-<$WuUV(HIksPyMERQmJzzLn3=wm+YtlKI2SZCk&!@+g-6e1=MYK0~EHpWj;f3~l@K87i4SynMWFNA>LqPpKj~=*khbLB|!|71*Y0ib>kf_S>VV$K(*~um08qjmgs`YG`yklV?!UajZ>0C&i%rU~gCLZPSjwO(h*q^_evPyAIc;lKRtp$>*v_Qondf{rcR~O=FVA@zLI<nm;bMBUwN7<3p4mqJMrn{x+3#JoSU>MUqU9erDj?RPG(O&YWkFq<;G6_h3MqN$ThL58b9d%M0J8e$sZmj*dI?%eSc?v>i!OJ5(OE^m(}t??dNBB&k33I+oM?{`lvWZ__wDs7Ek9kCh)@Qh%wei~h3tuZ!bZoBH97AZeY^`&sp)u{M+cw*Fb&vo@=9(K-mO|KN2XQ~%-WUbg;Oor~5%aQz3j|2OJCT;0pozo_p2U)DdX_i*dre_H>dy65YkulL~fAY1>zlC1|~{#9avS79g!RiGMTH7Ei_p$5bt#z1i>3ALdvVqGW=r63mSA=ZPkP#)?-W%Dl_7k~=T2;vaqpekBv0?iPcp{43z2N$9XYC<iD2M?kL>Yx=jBqAoFrTd@-G)8O;6`=th<69%PhNftxCA2|ogO+U27CIny00%gsBXmLR0tslP6LdxFik6x~cP!ZEcr}D1=mmWc`#>wSk_-<ZK7f|)hrTcXaR9V~_An5JAP#}fXk`$jBBr9HZZHgbBlZR_^nejC8gVqFpp{WD25}5pdJx9Jc*OD05BkFd$U)43!DuB5CL&HmOG9B2j6@s>Jz+RZh8c)6ARVnthldd#MoVL17R*7M0~wGBb72AE0?0-y^Wag$N6}I)EQBeDQy>kd!eUsCxEvlrE6ZRd;!3nM6CQ`vh^t{XJOWR^I>dD_AFa^8ZafdKM`00cfX5IYgK4k?Ho|7a&9DNkJO|GsK5zbo<QHHo;#OD#YhfGgMBE8ap_Lu58*w*UdK&h?Gl<W?Qg{|#f!7dU!;jm~!G1V^cmOTE2zj6*>hKb52Llcx9)?|L<q#Y}Jc5>9hNJK*;;XO;_QKn667eLwj#f^<Da2D~$p@$5J;e9mAiM!*;XLAb^Dj962QDIBL`!eM2XGAW80>?0;3K$<cp2VBE1$yWh@YdSGw=m`h4>YmgZJTU_zv+qxPVr^g&z=qKuaIOk8la`5*&w*;b*vkcmqB|E7#yA;!U*lCHw(@A^rv5z!kU!3b}&U_h<!3LGmpWBtO7aC_;Wk{1rZdpP)D?MSg-(<TtnuB}r*=9ZHkm;ZG<_Dv&>+0=W%;Lq$@B{0&t|0YXS6QWdc(DMSjBYNP~W3GxdRB{fMbDT>!Uq$G(Ubr9>IwKAk0X@J;(lq2OyL(&AX38{=$8j+@mP0`Z5q#3D&Sc?=R)ro_+5#6LVT5*vC#00cdmn4!T#3XVbsZYG5C1Oj`7_F$J6=Ey26i3<+C!&+oAU4vDbVBSz;?YV6(iyQcTJn&tqz7UT(wwv)JxMZRGSSdVFOq_of|gp72S|Iw_QX!^C;iAE#6hGZS{XnFBMwGOUCh6m+y$?0q&rC?qYy`t-e_e6Nk>daOMS=~(jT!uX-gg?86*oaiws07<4HDRHd-1&a!4*>E*VOOkx674;xsZ6txP2|5NDvJ(d1#0iI_?HlCfkanTt4=Oh7Ah$b7{4XlWu@Ko%k{B$LS$vWP52TuP>+l_g|3;&Qa~5LrQHA<iP>$ZYaBS&O)q%tI?{$U4MzXz5Y%6xo2dfh;DEk*CQf#7$%wT6vaiM%;{+R+24b72+!L2w6>DAlnhQlPA&2OJpbFPPDY1>>_&*_mGX`8S*mOhq#YChgSBI*AQPrOV5+n$%}|Dk|)Skl1JV^e1q&jD+kG8#KUN5H+hpBMLbGgA+M6R$Z^EuWItMYhnz$_iIxtKcZm<tN4622oF?xhzE2LJm2>1g;(4@mgj^sWAbvpJCdbH!<P*eC$O*LaF}aL*87-Y6pOG_&XNW=GBLIcqJyHn%gH{US6XzT$0_Vv^QVdGKMN$GjBA3WLPzElMGVm!{DTPm*k4ag$Og<;&K!MMR0%u8erLOW5;!orXNl-MUv66sSHKm18Ou0^4;8jPtO8z9}5z8wDl!8i0r6poZ#io2kz9rw2U&(LecXFG6QdlXjlvc_rm6WPVEhR>&r!-LF6sHoec$6fimGU?Fn*2ci#)~N5kzdG7@*Q43k{hIiQck%+$|--4Qc4j;QA*)eMroqlB83nODR!l((p+hS*haZWQ5BcsKy)armC8yp#f|7z?o|?%+Db#jhKg6YPpPR?L9C)QQobM+lp2UNly69^a*h0q_%o@m{6(576%i{cUy|v{9Hoac9j^|`6Ux)dBE&_?G-a)luB0HQD6^FAN`ECAF<Tj?3|Gb~8xc1u%anFXXQivsOX;ILs0>n4m66J5B|{mn<S3Js8Om&BzVfKDSXr(-t~{x%S2ihwmG(+E#BRz^rIXTI>4(@)>7qQKj8P^aPEh(PnaT)d2;vYWOIe}}P|^_7l$FXTWsUL-;xo!P<tb&gvI231@~kpZc}!V_xJsF#tWzFQ79uWGHYoFyhm@&^Q<VkE{YtL#Fyg~XM`fmxtn@_esmxUdDod3~h?A7I%C*0eeH|`8sXmd>OO@p-et1f4Jim_=Z#^W<<aDeIr(=h=Fz(oq;XB&Dac68aPVYs>%5oO_C*8YBaTbd#XLHp#p`$dXv9Pf+oW{b&M&m4Y=4Uj%x=o2YwIRco9lD;!axKH@SXN82oaI`Uvs#kj)HhZeGMvTE&s8+eaxKHzT+y*IoW(B7SuC=g%@y-A8u#Ut&pW?qnK@T7JP&#8T`SC7$Z)J}lUr*!DyL)LpM30&ooHM~UTf}gbF2)f_o8EExo*Wy=T?TZSY$byE1C-#?z3W{V`Vs-D`qDeXR$Lsqj8KqiPeS-$FWIV-lKB#Es3kEs2pQYV!4*#bSzg_Q91REtCOhQXT@&iB`RmJSb2%c*<4w9iOO{=c3IA1k>zZzn4i%&?nPd;_!Dfemg4g(t!2-Js2umkB+9MlLR3!2W|ljA$Bqo&U-QVFvC%la7ac3hS?t!{9+k6LWI3BFmJ1n9V_{=uIE{skjmBB*%+F{XYwu2N$Z$M6d0DPyI33GsNtUx*%W_srGMxIxYD0#z*!j7N##ydqIGZc$TpE?L*kw73MV7O<Vtz*B^uJYHD;RI!74Y{S)}ASE6hCfWn)QCj|8K;P4c52b6ZQw%oEc<0z`n-W(Sq&pI{dg`efGY{PPjQ>|HApo#bxmC2lw;iqr@AaE3(7;D~Q(!j3var#@W|`?Th*)<|nv*G%oKNH$MUWeEx!Cic)W3?L?>tjmx_hW`2U}EkK{E=dk_Z?ir<iG%mkdnDrH04*~jIzQXoLnomLfXk6YkZoLHb2ieym<SV$|!rJ+7*?-bcl{Y?oyF8Ur`%kbwdtYSd?*8+?yZ_Mn#d$WYdA{RsaDRUHACaBA`_KO$`w!J)wJ5Xy1naYVi~9fD&p%vT0eeeue}4BLk)8jR{fFA%@~(076VRXE{YPZyzh(d7{FmB)g7w*ZqW=Gu{U>*5eKlw3^QuTbbM~nE>7zBgldw&H&&1?L>}S8{oQ!(UV*5z9u_0~S>gw8Q93L#3p=7^jqwQh!`)Ij1j<u<z<NbO7bR4tC%ZcdEg7p_vk)-}CL`nT^vAeex+@^A9eYfV13+_nPPyL{BDEhb1wC8VA*&N4HKWJMd{r<N!+bt}8ULNiCl1k$iN&0&>I-k^^T!CD?{y|g!*541`k*uHkN#%wM4YeF=e)%@_gSJJ|%9Gj7we)#;1n)=ZMI>qcY`9QNqis5`OtO9&AI%f3mvEB$yB_tZzpT9&C2LbZqDgumCarq9(~egEZ)Cq2w*C)cKVSc}&DTF`*E(85qvOL#nfmwZ0Z_@>yp*kf>JMN4tWDz!SO2U(TK!W$XgiXm^-pCBOP`mr^-ulH4I`<a3&PYt>yK9d)DNl`Nz!~%$@F;{t^TPW;p(6Dv-+p;EDR%~)xY1*$dcZNm-POu9j*TR?>eHM4paXFb{z?*f7<5jpS9nsU&E~DV0o^-T>YP|@2`J4j@jd-Z2i+X`1)sUD#O)3>yK9d)IZveBx(Iqf9d^#rEL9Ee{uyf-2Tt{qt!q4kG3O8ns4eay<f15R{zwGaP`mnS^d*`Sr|q}tAFap!YGp7he@lR?zBD75=w#xuY%AU`a^rf_K*N6<}a30@bW?ls0_^zn?Wszfd()DaR77y1qwq^C<W!90^AGLAr|g~M$iNt;DYAn?~?C_PS6c{Kp%Jz20=9_0L2lDLro|GrJ*8XMJQ(eE;<e|4k|%or~@?+Yd}-z09BwiVr}RObs-rBA`XOx&=-0_cf{^67@W`<dLi}#H#`6uv_otM{h$rBfOy1sXiHB|kcgNFg&+yaz&(ifKr5&U9l?%h2LfwgBaB5H3&Y`M^B1`<<Mjl*3Ugrs;sjU^V_*_2MO<qBes}@oA?CqLFce0>D9C^;$bqRa9cIHkSO|+@1w0N<!UlL2o`bEh19rh)*bh2PgJCclaWp&xBOwzeB2I*K$cFi_1aS%E!XkJCW+2Xh$KVB+46_ht!FHGfuYeEH2am#Qup4$F?gRr?!Zz50xCd6lK6o0oAZ~%zVH2!_Rfwx#GYo-cuoiJGq`^}#9>yV#gJ)n0ya>w?mqRMt1Ry66Pr#c{o>U`6NO`<&Kt=K;oIyMTf5CA$4_6Vd!YA-4T!HH3Q@l!&LvR${hIipTI0qlVNAMYZ1>eH=@C#gnKj1bfq#&Wc?kz(qkt(Dn`4A4nJMbZ1AH!R43f@P2ACAFU_!@ph{1N^G-@)f_3GovA07c0KxQuui?jc`51yTdC2Kff6lCq>Usft%E@+*`e<q*q}-=H%28w!)kq%gUc6d-@XbtpitLm_eyeuCfOAYMn{7MzBYh$n%Ni%^XG3>V>Ncmw_qRBvzp'}
READER_SHA='b06d26f9590c321f1088f3449b0558aa1c6fb86e58a6e8f18127f880c616f59d'
READER_ENCODED='c-pNRYjfMi@w<M-Rh<@q2+|}aD+z06;#V3^li0PDv?+#z0f8fV76`z2P^3Km@7>*d-~du~(kW+b0e5@5dwcuFou8k-<xw)sv-H6J{^K)Nmm<p6DQ6`N^O8kb!bFzvg2R7V&G<fw>)|SjIg9hGh8MQsX~D~Cbar;L5f$6!NdxPXoL4N%YnJ9w!k(qLzVu-|kDHpasH%9));!~7ROe;ovluAC#G2<@UY7^|tW-<#5~0O9V-fr3Q?}z}BI0_)-ZmK%H6zyZjMW>!+SHr86!$y<vT>BMc*En{A{SXbIy*l<KU<agmK9OGNyU<hZIPEXdjqd$>Uk4YIHh0TS9zwNw-#7cmrY#jx2)L~2jG!q#o5`5o8R8Ne8=YO<KxM6JY&uiF>!nbFB5!e)XS7+rt;;IX4K1LdbyG>*Z8u!az35?>(z^!9|*7W?)lRnpT2cwY~nNL*O$+y@Hmx^m+*KgAFtr?3LbxYdV`OX>rZFD{qiQfc^&@emp6bXD@IXSMh7<tCL^DX>EFU<!C1WwC+1ZGEEe9`*;&F@Ea7pU@Nk_jT@<D_J7e%GqdUNh;*_H!)S+;BsCngj1hI|QBKGkJE0JeD1Fcxs8(1U-I%={aif=<aCD(cK>eVZd0$`PkQDx{H00*1T*?50-{rKwo`Sn+%r3xv|Old$PpW~B@Xh0gTvR#ylgmisFD((>Sc++IJpoRHrg^CGc{sh~e(%juffI_R8CkC6`H2x~kIG^2uojkl1xf4ymGiw#v!JK_<#?(&r6yax2I{UaOn=A%<kvk#oo&I`a2u)CAW`E9$rbq>@Y!|ZnQ1EuO1PyTY0`>z01Ifuu{uv-UixV5baT-qYxY?q&n3DyK&;?Yk!VAat^6LA?msd|0QVL6vMdbltCBSISYj?aKj{)qPE70qu<8%}NrJyMgu(NDdD>!`+aj@__Jn;!>fYX%1(Gt*00t3DX#-QNN%YDIPlw_W9#<xqJB=DlRlCX|VAMthRS0Jm(@rdT}Y?KM`9iW;30_5J+@DeKr*koK$2PX#3hY>1rdF`q`@hCgExAvAK9lo!5h9*$`Qt?CzgRKA+!3NGhes~)uWfbS(mRFlF&bLL$D_r296#jif<9ShcrWVNab2R{RK^T^Co>btDD_%q;>XLK_ASZeL;3A?ph6Q=)V)WQs#uC9vw`ZZj@H7Z=(br<90vZ)J=NK6=M{?g;UT(pr!Rbr+68NKb)UZN}s-{4vjVFA7m;nK+wA=vxc7oq^c$7NuD-0u-kv-rnj`+ppwpxO4$E1^E1DT+~LBz|`W(%iHzL>^b89k5&o&hLiR^Om;F7Oy+2*Al&jv0jLV?*P*EDm7&H4RHH23lsliPn=r{7?81j(0Q+pv2`!)O<@m=|b<p>q|i)`gZ={60?Gn+qAbZU@l3Z$!cdYoOl-s+n|T+LQ7D9zL^D#rxmyH^?5^rPd+220nP+8`Xj{<z^S~i^a`kEPqk9<eN5IMPn)o|x>WMIDKk9ZERoUH+L_S+PYHIe6hoq#OJcr3cKnn3n_GMJmE^0rD<Ar2=6RzyFAflp2`?B6=vYMoj|R|TkRkeDE+BKTI1UL8rfIzAc5z-i-PXPlK@1TS^F~4;foTY6N%&c3Q|esgDrM%1F_84n$Oihx`YzYQPG`Lu3<v?nEZTr{n{h36sL&uAy=Qb!B8$@|;jY?hyop3MckO*BrU;;oq5y{e@DM`~WmOFMD_fUQv9W?LQ5;1{qFmo;$+Yf8ic!12FH1|aPB4n~f!c_twuq$4ydU_8UnJEFUpP#fzc@PBmb4~|XmvIR8U|J%mB)zoE-%yMGlCT>B~;)|qv-BXS&g22ATWIHWTZy)kA@U_{-Ee>4jm%CceE0B8I;9^l|v&)pw}$4Im7e{a-aJ83UlFV6M=_^l>7>78VEUa=X<Bs4)j`GDj>dt&+dJO;i$EwGOsByaI9QiCg}_Blvzc~%H3b=2ZxKp;Qr!%aCdPBsl5l8?1T>=lYwQ!CKI)k&xZyqz08n6_fQnsPU&#un}W%3df_Tk;Md?~e{mSzU)<@Jdtl_wTO7N!K*A0rEa5@64W7fr{c!)erT4>wCIhg8eHRb#)L+_@mvyTA04H@~Hkd(mHM^v|Sj*!(3g04HyX_fO0E;F?rPV|o&O`VJUAwj}qpV6#9I?f2&op4YE6q;3LOFiq9XiIReLuxZvuO`DM7*7S!5n4Xq|+4i0>PpiLXb#B$(Ad<qU8ntkS&7knEdb98nF=}vWA;M-Nb<Cu|;JTQ5uRwa_DO=HK#=>wt|90$5$dv;zyY_vanbLjsb_clTpk7$kW{BlsH{c3W)XiYwTB;HcN}H%}l#?2X$?&ysXKo%_>NsYrwT^YU0&-^ZMPZn^&)YhO~VYRg_X%PUsZ7FfFQ;0Q2XrCIxHL)b*5Wkdw@yeuz7y6o-Kx@ewtsM&)ASWKeqx&@U@Qc%vIHm`S7hj<p?%(M>PtC7%(3n#EmfKMQFi>5iTvg*Qj7RUWFBY|VQdo)Qy6C{!N%3%jI*o+=TSnq2lYDAhLFx9_rL(Bik+5JnF)n;qIlk4I5~4LE}%P~g^X!Hsx5e`f3ch^oWH4f^V-U>xlCc#8|y-pQj!mzFfZgd6Q2!Q`-qkYQ42xFms_x7Mv}iyHFYv5%dp4#HNn5;scbB|<||t%@|6FOl`N4GQCPv|K)R_D!xNB<*r$I+=B{Xv^WX^|LhKvy}w@NN}I1gp`iaU{HRNR!N=hh7qj1%c$xgS3^EzMu?FVK9u=EcxVcMwQZn>&&V*mCr~LJpE>P`Ds`E)vDiNCKEfpw90_3yx3DIV2z%Ny+6p*`y{P76VEF+M&}#+Ki=|Fp3Xl>{Ld|^$E2odIfu8EBj^qIPi4qxd^}fC~&dPbR`r7eEb*{RG-e|-3iCFUrviFwYC#gg#Fnx5e-3WA`;*p(45Y<D(v47S<${g+V0a!ow_9mlOC_~gtrT9iss#Zr}tkq5!ZeKpB)~W1ER3W&I5Y|MMWj`{W?0AeFab;*_URfaMDJP3z=N+3^oq_2QfE1T(h$_S>6qo6GgzUJAA{;s%?L<N=Mpbu0?4Xux0Tn954k3aA2YFLtzI)Gs;V>1q1{frKx8Wt9_t&s*b>~4>$&#YM{%ERXR_8^Y=IcX<Syq-;-~(MN#@}(UtvXMkM$KYAhphHmiL%PjK_qeyrO4`b*`w|%J6r;s4wgJw^ImamxonNU%>!=vfzph+DN>Mt?7!_0R4?l$9}yJ$ID0P&7uWiPA(+e-1A3TE`qdu{0|AL&<yHY=>8F>(`3S0B5Mb1#HKM1APW#LWbxj~REv2U(s&fxP4NxyBCw*8~I|gVdJ6)-gx9JYGmSx;rDElEZiUchM3o_yAOA!x`7U8MFp;gV+m3%*$V_`FydNu~~fKhn}^AgNB+eVpK<-iw-30(&)rzq{QKj8-ib8b?O5Um^XM;6Ko;s<DC32F|hdYI(R64*L{(0q~D1>*(2?SjeTcTo`Q3>@kXyF?&M{J2A@oZc@6SCQe9Bi{Ss{qS4i^n3w2hlkwAk=yV*@6oklK>MqZmQG#NG5wuKp1Ncuf<0X<VMD_R{)4Bn`AQT*DPEWZbE{_g9%KbI2@Ly;7nMl!Y%b4AVg@rmtf|BdOk69Z5fx-_5{0xO(K3e^kp=pTTc(Gp8NeKD+}aV2;`aueoXv(4t876kGAF$3wk$BqQ|xsOatTUz+vYTA&<eHCjJRSjp{#LX)l?N2Wm_}R?n}NCd4raxC<U4~dm41Es?n4HP77c;1i~6%7<GG2^!=0a-&6cQhz(cSsFWaFv*6n~8>&+zt8tGxv_WP^WxEuDc1U{lz?G!+yLWMn_|fsuP(OIy5znXi`64^WL>H5$>7P6cTHqU6?YSAHmISo&qIXbpsGpa!e!)E++2)3A95i)(NLocu%k;BWG#j=02xMutJ&Pu<!>mll!W_!b3fvBU<PX(He%)-8X%75Nql{ZIcglxQ+pf!KC+b7E<Pikh_57x6bjg2yetx3^C)z{-^DJL6B8JaZQzF6YZ|v#QXU{5(LGsgn1Oj+3eJs^}sk|{T!q53+%o$i&bTV2I)A9(544FR(CHLf6?eK6bGT%H$dpulvX;b8h=bJH|6HhdbI^OVJKO`1@Cv#|f>XONhuZg1|77G)|u%L8%vZZ(uX941!E=aEd_ABoTosl%Z!z&dHsCbEKgyP6f{fE7?^)0A2`yce6THgwci3B#LGRIXK)evwoFT{9-jRi}vz_(&aNs#@O^`JmlAPC~Po1lL2_gC;p*q$RXfjB`#14<5QCW8D^<p~B|W6312@@xnp7R;lg1iEQa?CiW<QU-Z@XPvfRD9hT;B@E26^V%(JqPUXc_lcREw`c>S$u4`IpRB$;k_SD%l6Fvt&Za#hy}m~!RRE9FI$aQFPbZE&?2$gU5>Xxd|DQ<O9rfGdVD%L2I@yVJE`EolqhLbomF^sGQCYv~Ovq0;h7Q(*qHQr)!<few0_#yE5N`2S4?g){RCWgrLu{LEDCMt@gpzNWq#d7@_dC!^&Y`foi^?RFjuZJOg@7786{>(%n>m6kG8Dgo>{sn7-lz~0w%f)qR|G~5okJz*N}}{gwKqNWYWAKok~EH7o6~cv0Mi@kVcqh2lP3V?sHSQg!Hj#?l{2~M9BD=+o4#lPOaR2|3>mn0z$q807%VT?Eu%_6Jj`+miBj)46u;Q%addtTmJ)76UD*Y3UWzqFFjJghAAD~VV~$tZpvql!lJIZZNc}5S?sRwJr#uB=4Iz?mmwAbytL9}Tu~zI()EnIwY@3xjGD|jWlQxX?Kaa_ehnih`iM59>tvdG0W=>V}6WH<8^6~#`KSjoQ+tb6tvdp6-jw-O~+-93kN7O^}@KN#1m8UyVz9Ex^1d~1DIi-HE1YN8;FquPUyH0lozcVFx1>m?BgR6BPhOkNk$b~$UlRIo4WD-+A?*bSgxDTCP6>dTC591#ogtSL=!Sos{_&gwosn0&NG`3N7i}zAUBoM!wZutQtyQ7h2u%jeuU=Oyn06RGh3v6TQ_^jZg)AQKmuuphgJp}2w_o+?5dkGP4%3CN)miK7Gil?iZT9eWq|IFSUvU<bu(wOleXu*^o`|3uRyiev^7hW-Ilvije)h;mGgd-TK8+vyc`s!}HwZAoXZ+@yTnQBf))TU54G&=f_g9Wv|W77K!{kaN5<M0()FL)?GEQX`U>hra_p{Ysy4)lX|zhl^p&qm`3UatBg(e?`0AE4$N(fkq2#-~fBK=>mt2K+anb0NNm_&oLcmjjR2!m@`~nqXXMCBv^28>5Ag1mU$m&}%H_FgZaz3-LxLjeZY-j^e1gwvGKYsdb^e&~1P)U}4K9#P2R)h?{moASSXfbX5C?TC{X!G-<X)<sO*?<m&$gCRccF'

PALETTE=[];MATERIAL_LOOKUP={};ORIGINAL={};PLACEMENT_RECORDS=[]
import tempfile
READER_BYTES=zlib.decompress(base64.b85decode(READER_ENCODED));assert hashlib.sha256(READER_BYTES).hexdigest()==READER_SHA
READER={'__name__':'pinned_established_readonly_glb_reader'};exec(compile(READER_BYTES,'embedded_read_actual_glb.py','exec'),READER)
def decode_asset(asset_key):
 raw=zlib.decompress(base64.b85decode(ENCODED[asset_key]));assert len(raw)==LOCK[asset_key]['bytes']and hashlib.sha256(raw).hexdigest()==LOCK[asset_key]['sha256']
 with tempfile.TemporaryDirectory(prefix='whole_reference_decode_')as tmp:
  p=Path(tmp)/'model.glb';p.write_bytes(raw);decoded=READER['decode_glb'](p)
 d=decoded['document'];assert not d.get('textures')and not d.get('skins')and not d.get('animations');mapping=[]
 for m in d['materials']:
  assert set(m)<={'name','doubleSided','pbrMetallicRoughness'}and m.get('doubleSided',False)is True;p=m['pbrMetallicRoughness'];assert set(p)<={'baseColorFactor','metallicFactor','roughnessFactor'}and len(p['baseColorFactor'])==4 and p['baseColorFactor'][3]==1
  value=(m['name'],tuple(p['baseColorFactor']),p.get('roughnessFactor',1),p.get('metallicFactor',1));key=json.dumps(value)
  if key not in MATERIAL_LOOKUP:MATERIAL_LOOKUP[key]=len(PALETTE);PALETTE.append(value)
  mapping.append(MATERIAL_LOOKUP[key])
 parts={};used=[]
 for c in decoded['components']:
  node=d['nodes'][c['node_index']];used.append(node['mesh']);m=Mesh()
  for tri,mi in zip(c['triangles_zup'],c['material_indices']):m.tri(tri,mapping[int(mi)])
  assert c['name']not in parts
  parts[c['name']]=dict(vertices=m.v,faces=m.f,face_materials=m.fm,material=m.fm[0],role='Complete existing evaluated world-space mesh and every oriented triangle/full constant PBR retained, original hierarchy baked explicitly.')
 assert sorted(used)==list(range(len(d['meshes']))),'Every old mesh must be used once';return parts
for asset_key in LOCK:ORIGINAL[asset_key]=decode_asset(asset_key)





GROUND=.125
placements=[('d', 'agriculture-fixed-alternating-chute-twin-pan-sample-divider-01', (0.65, 0.25, 0.125)), ('t', 'agriculture-fixed-open-slotted-sleeve-grain-trier-01', (-0.7, -0.15, 0.125)), ('s', 'harbor-cargo-sack-01', (-0.75, 0.6, 0.125))]
def rigid_point(instance,p):return tuple(p)
def stored_point(p):return tuple(struct.unpack('<f',struct.pack('<f',float(x)))[0]for x in p)
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[stored_point(add(p,t))for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,rotation_z_degrees=0,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values()),coordinate_storage='Exact IEEE754 float32 after translation, not hidden deformation; native versus final GLB bound unchanged2e-7'))
base_mat=len(PALETTE);PALETTE.append(('SceneOnly_SampleCornerFloor',(.32,.30,.23,1),.96,0))
v=[(x,y,z)for z in[0,GROUND]for y in[-1.2,1.2]for x in[-1.5,1.5]];f=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];emit('SceneOnly_ContinuousFloor',v,f,base_mat,'Single scene-only flat court support, no extra counted model');FEET=['SceneOnly_ContinuousFloor']
def layout_bounds(v):return[[min(p[i]for p in v),max(p[i]for p in v)]for i in range(3)]
def triangles_of(names,vertices):return READER['np'].array([[vertices[n][q[0]],vertices[n][q[i]],vertices[n][q[i+1]]]for n in names for q in G[n]['faces']for i in range(1,len(q)-1)],dtype=float)
def ray_hits(tris,p,d,length):
 hits=[]
 for a,b,c in tris:
  e1=sub(b,a);e2=sub(c,a);h=cross(d,e2);det=dot(e1,h)
  if abs(det)<1e-12:continue
  inv=1/det;ss=sub(p,a);u=dot(ss,h)*inv;q=cross(ss,e1);v=dot(d,q)*inv;t=dot(e2,q)*inv
  if u>=-1e-10 and v>=-1e-10 and u+v<=1+1e-10 and 1e-7<t<length:hits.append(t)
 return hits
def layout_validate(vertices):
 assert set(vertices)==set(G);tol=2e-7;names={i:[n for n,g in G.items()if g.get('instance_id')==i]for i,_,_ in placements};bb={k:layout_bounds([p for n in nn for p in vertices[n]])for k,nn in names.items()}
 for i,k,t in placements:
  for name,g in ORIGINAL[k].items():
   vv=vertices[i+'__'+name];expected=[stored_point(add(p,t))for p in g['vertices']];assert len(vv)==len(expected)and max(abs(x-y)for p,q in zip(vv,expected)for x,y in zip(p,q))<=tol
  assert abs(bb[i][2][0]-GROUND)<=tol
  assert -1.5<bb[i][0][0]<bb[i][0][1]<1.5 and -1.2<bb[i][1][0]<bb[i][1][1]<1.2
 for a,b in itertools.combinations(names,2):assert any(bb[a][j][1]<bb[b][j][0]or bb[b][j][1]<bb[a][j][0]for j in[0,1]),('Whole instances intersect',a,b)
 contacts={};floor=triangles_of(FEET,vertices)
 for k in names:
  tri=triangles_of(names[k],vertices);mask=READER['np'].max(abs(tri[:,:,2]-GROUND),axis=1)<=tol;bottom=tri[mask];norms,areas=READER['normals_and_areas'](bottom);expected=float(areas[norms[:,2]<-.99].sum());report=READER['actual_opposed_face_contact'](bottom,floor,plane_tolerance=tol);assert expected>1e-5 and abs(report['actual_contact_area_m2']-expected)<2e-7;contacts[k]=dict(complete_ground_contact_area_m2=expected,actual=report)
 tris=triangles_of([n for nn in names.values()for n in nn],vertices);rays=[]
 p=(-1.35,-.95,GROUND+.25);d=(1,0,0);length=2.7;assert not ray_hits(tris,p,d,length);rays.append(dict(origin_m=p,direction=d,length_m=length))
 return dict(instance_bounds_m=bb,complete_instance_count=3,distinct_old_models=3,new_reusable_model_count=0,whole_oriented_triangles_and_pbr_retained_before_float32_translation=True,actual_full_base_contacts=contacts,selected_visual_clearance_rays=rays,not_navigation_or_full_space_proof=True)
LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate(vertices);result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,.65);ORTHO=4.4;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(7,-12,7),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

assert all(len(name.encode('utf-8'))<=63 for name in G), 'Blender object name exceeds 63 bytes'
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
root=bpy.data.objects.new('OneWholeSampleIntakeCorner',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole scene horizontal centre; continuous bed bottom at Z0; three entire unit-scale legacy instances';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert seen==set(FEET),('Scene-only graph covers new ground; complete imported instances are separately grounded and retained by layout_validate.')
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
assert abs(lo[2])<1e-7 and triangles<=6000
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
 'components':component_checks,'connection_interior_points':joints,'complete_source_meshes_retained_on_supported_instances':sorted(G),
 'single_prop_count':0,'scene_count':1,'new_reusable_model_count':0,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'basic_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
 d={'id':ASSET,'version':VERSION,'category':'scenes','assetKind':'scene','theme':'agriculture','style':'source-preserved-faceted-natural-ecology','title':TITLE,'description':DESCRIPTION,
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
  aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
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
