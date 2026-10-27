"""Static complete penguin on complete fractured ice shelf: two whole originals, zero new models."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='winter-whole-penguin-on-fractured-ice-shelf-scene-01';VERSION='1.0.0';TITLE='Whole Penguin on Fractured Ice Shelf'
DESCRIPTION='One static cold-region wildlife display scene, one scene and zero new independent models. One entire qualified upright short-neck penguin stands with both complete original webbed foot soles on the real planar top of one entire qualified fractured ice-edge module. The complete head, bill, both flippers, belly, feet, tail and eyes remain unchanged. The full thick ice shelf retains its original through-thickness V fracture, recessed lower body and projecting upper lip; it is neither recoloured nor reshaped around the animal. A single opaque blue scene-only datum surrounds the whole shelf. Unlike the original opposed frozen riverbanks scene, no second bank, snowbank or central river passage is composed; this establishes one actual animal-on-shelf contact with the notch and front undercut left visible. Both entire source GLBs retain all oriented triangles and full constant opaque per-face PBR at unit scale under whole translations only; hierarchy is explicitly baked and faceted normals recomputed. No new penguin or terrain model, no animals multiplied for count. Artistic fixed ecological vignette only, without exact species, geographic locality, habitat suitability, animal care, buoyancy, water or ice simulation, ice strength, safe standing, load, navigation or safety capability. Rigging animation and interaction not made.'
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
LOCK={'winter-fractured-undercut-ice-edge-01': {'bytes': 8792, 'sha256': '46560a28933ed6a9b85e816d0a264412d84a720df0312bbe6443704f501757e7'}, 'animal-static-upright-short-neck-penguin-01': {'bytes': 57476, 'sha256': '53876497748be033034004efb03b989c0dae5d75c0625da92b5da8fc1e83e811'}}
ENCODED={'winter-fractured-undercut-ice-edge-01': 'c-qxiYitzP6~15t2F%mOkPu)p32*N*@0m4twzh*C6R;CZ5EPT`cz4#Gu%0n9V-we*ib$y1DlH`{sw!HcG$g8&$UjoGim2?V5{do^QmaTsty;BF5~L_;McXuLQ-1W^yF2z>+p~|-{ODS9=i4*)oO{l9&zy6;1Gyue3lT!cScGn`Lg+wmPxm-$c%JFAE#vHfX`8O$J1*P8J~HS!w&O7apu)80Ogm$`OxK<sW>kucaY<#H*-_K=EXRh)LY!mIHnUzD46rR+0eNi8iE-98hCs&ll4s4V?PSOU{^Z${GvCHp^C{moJnTi<85(wM)Am!Ylf$Y#w#l3s1k9v!j%Q|=0oNG;e=>}fHW_cw%w?G~mOscCjB6S>#s}9&1_opPpp`xaZg|X5ChHn$f5bHz!_L4w@`xFBohQw-Z`lJ3w&$ite3<CiK9jSC<2a%r(;FlK6`}xFIt!LEj~7(B(q=FA0p^4AgH|r%nn2144&s}MijbVLGGOG4W&5TZ3th^@!o_0{Pt42=m@$qAs)#G8jOAh<3D2?PAohI2x6-Lm%NsFrDaX!@u`RwkVm7mmYYkX-Dr5K~LogdiWH6aI(>Ix{Wm|9~jA1GbpZQWNx0lIVo92gbN_=39;bGHo4Lgmu%_RwtN`psuCRiWuV~vb4>|3K|AKSuYjhtsTGky8(^DNBjymH4)kzFr-IF`<tUMgeSj^!2GGi`{8i2B%$;~fY0_x7<^?in~TVulwqEP;JDjSP`U)c4d7ESJ~s>^ippp}hL2Wu8gpj4=p`TJ;23_T*W-_ocUdKTyQt6dp2QGc8afX`FFJ`g3Nl1=$(yO2H23q#iYL=Ho!C3yco;yN68Q$mOi`VVtfwQE{U58=l$W<Q%sX7R9gP2`;V(9QjD9qKPW6G;?uHNZ^kqiae(z5;7L4M3j&PkyivwYUZ(fg*8HJkjrkk+_Wq%@p)^CrYQ+k<K?qBnM()Lo*S8FrpkB(IqxYaDWV`N;3^lFmAnibS0zcnF%~46#;FNT<*SHCl=6g$vZ@HGrdANnL#8<#?r)Xh@Io>1Li1b?KqM)7ktRx#B6EUT%?2g%x(QiSR0)=;Afis!@q9A_M$Bp>QuE6Ryaev60uSCN@;S&Wik1*L4kuhf%*U-NysYsMcIELXQjsQqmb^+(ZHv1`$$ASRxz><{D^Om^@O{_nAMs5R*P}hXT}Qflx`_+jJ%<mq9b{X0c(E-z14Rzz2s3XlOu~dlSrBI|NVEl+w!oLNpv+iMX$u-{K`3P*K}EsQCU~B<A)Y0j)kwoL&vEn2^p9k-rh61>9${m;#U2?O2AX9aUN;bq*ihJ2Z0srAq2qi$=LAuccum%D3X6G>%FBW*tN6WD)Z)Cr`)J|*7purXY|d*A27KZcdvt$?NV+QRK3~@TQrg0N+Tye}FHEcVcC;OAJ3PmLSbBL$s+PVv!Ixl9C~(cGf~JWIr&Ld$RNntm>T+rR6r~)0O6m1wd4@l((3H4@pvb(4ODM0+syOphMw-I8CJ1A*iccBJ)bcKuQrAjTmJrKPmMFcxqJ5qzH;3`+Us$fZ|0VVL(gbS!90I|k84Gj;B-O8f%r_6hvC@a5JsdsA_nvH){1XI^eZw8VP?QpiFyl;FRs6kDU163kPe`DY#S+Rg9CwSg6GG)n&(T(eDuU)kVb<D$RE6t`!p%|_wJKJhqb_h#HO_0wEOn@-l{>HTv(+_Ct0G@!tBWdEMasa*vRGY`g*nboCw?L6DSZi!*>E&q4z5M0y{jADc>DR_(;dIp-`Kn;7;lUdyyg7v<j%eeQy8}{TaWQ1#uwiFM=Q)vVtnK6`rzhE!vu?>2)cF<VnjaAB+>Nee}NYu{F}u>R0CrzS_FTK0nz@?hr!Pzjp-Om#5-^7H2(N8O~-g=->M{yv8@6RML6UQboKc#<}-@hD4vUPJUHF@&FQ#8jAO?*<RQd3MvTLFDLjdB7;lJij2MUUh8VAbaTsriaV!O0eLft<8)6(|LAMCw80W)bEa6^<_=8O?B>!U9_rU#`Ak3oYUU_~B-zT<>CTaPLHy+mU{d-Hslk^-~{?5-Wl7lb&_E$QMU%m7Mv15O9N2hgZxsdpf*jaEZU1Xn@)A|0brac7jcniltzX#LrLr^?tMoz~b6;~xZ{6EGUweK6ydZ-i|;97{9(7jMIn&7HM8_|8J4#qmP1Z_fF&~g};qorswx*x58aRpk27{sELFs?-P=mE49t$}e3T7@1&+ff6I4QMsmhIXJv7#q=Av=i-u6?ek54(&$wK&9FZ*8<dc;T-V?@_(uv9&en`qi{C6jo>ZkKZ?Z5ZoWh~Z=CpLB*yPG#vq%F!duRtBKswZKhdKwtV{Og;deia#Na={V7n~F?{5^&X0rt2SflW=o9Un&##i5kc0J@R#F%G{L(W5tdBZs5FvOTEj6>c+jQPPh<SN9N6O2QCLX2a?IOJhA4tWSMju+!F_7LM3=fhzvVUC43e24IO_2eVu?tOJ*(Yr&>dF7KI5}gCjdda9cQ%@fux$*4KSCYl^=btlC+fSYyuy5=199sVR-yS0}_UW}nc3yk`MPmQrAKYZroUgrchuGbG^@$`sKWfh0`jem2yKx_pU%DELtWnYP=buA!9>rS}=TRI+@fO8Z6hBd%RKi14>~y?Q`L>vx?Us^rT|L|p)YMgg*1;W*^`xG!gYiDNlZpqZ7HT*PBMa4e2~_Q^Fm8n^z8q@!b{MxqbzTW|dl!tmpjxknTHOp|GgRsZ=ms$uV^FErLwDd{<WL-H_a-F3D4;#iBQ_%uMiKGQ3l<<5Mj1)aPZmKBSO}LAaSok*-i$gwmOCfn^HEgYs-%WhQqL->ZI#ryN^0KS)W5r_g_YFBsB`pPo~g^8uPZrgS90#I<_!MdoX79xY)<3P=YPZ*{EZElTHkzqD7b#=ntols-1@*_JNVc8KhuA6>)pu}O-}Ifx(R)J-{j=?8%_sxKYF=H{z<JI;0xQKbw6yVNxuB|-heywq<-w%Ym@SO?ZNR|my7T-6W6A$beq8++s^5ySJnsHKJ5(t8oQ!j{O((mgNufPAIq=mpVj_zGBK75ZmzyoH2<9zPJdy^P|&yMHT|;3>tFn-6MU!p2SxK~Irx|i{rvi0?&x1$!3WNJi-Ql&H6#<i+Z<fnT^G=E@TX>CNswzgUNnc6xBa;;xYF4goH2hr^{1O_f`2dG65Rg9(jqy{56yEFpR_zmH;U&d&ZD@E;-BU=YA>SrkK#Fs+o-*u=R|Q!%W1Cizkk$_Up{IIzkSq@aWV9}dgyyQNUz%oeRC!BwmRr&+n~#>fey9`I$8{RXcP3a2IylP^w4{tYc)b2<Drw@i!|taD)cnm>-NI97bTzrGDwI1+KO7B&)$!cFecGH=(7)^Ht4nO=nK$iS3pnQ3Rees@*l4V!Se', 'animal-static-upright-short-neck-penguin-01': 'c-rl~2Xs`$7e9XAqleym2nn44*^=E&$j;CSy#<gGNFjkh3WOv;AQS<q5~<Rqget^{G$lI^0TmGt3-Cp3AU0G~6zuSy_t=Mb<4&^d{{H8G&j0*4Co>-=ckayG`<c6w-TP+8Cr9;=0bs%B0F(UzdJh@Ue`a9p)Ts#>f#EX)$0wvFq{n8Yr3Z!w_L-2LmYOy-U_9><&?Pw`bzDMvK(7u10<z5QP3_Irz~I2Fg!HLNX{lV;*ghmMCpd6wJXa7H9^yn(1H(tn3`~tp;cbCKwBH2>rlyV4ei0IE2sQ?rg3ZC9!Iofauq`?#`rqHq3`|LwIzdzA>_2=$T5>|ywA75G)XcQZsY55HCyk$w5tWucHEqa*wDgSr3GtIUr;dwEh#kkLqW3qr_SYo4q^HG>>yn(An$aaGIT;BX9}D+QNX*bW^hl1)$lwzn*DY;Y>eOiolQViGCrzH5kdC^U+;odg9i9-^BP}fh$(dc`hNQ$MC-;rb;090bJ|h9ig+7)WtS-^xd05=_b2kyItDtx$HaFHAoDiEH70X9X7#9_r#LdUOmZEk}icNmxxp8Tkaa=fQT*A1(@Qn1#gvVM2CTFI^j!zidEg@ktcR)hd39;$%X|c(i7L()B`z2)Xi6q4jPRkrWfwO0-O3Ap`sod+yY3V&;<27QA3TYo=3JuZz8O&iJ27|>A%-cf4w0|~BsLd7@Y7SG|tj;#0!C<q5SS-N?b+XQ3bcLK^>H3I|+uGYqT34&dYBhz0T1+{rRm3anl8~G{W9;zQ^psv%Y3Vbba6#5EZ8=7RIn-*g8rAi<X|mWJEyrpxgxU;d<CCn$X^Bvy$zU<s%q6Xc?+d<{ROTckWQ^^XnUOGVK>URCgeP5>@zEk|7DI^97#7MGVX{7Qo!M%!nXCp2Z!&~Dnp~JUgqzwF8v6g9n>4C(j!)Gn=q>$1ERWU@5^6MrnnNsRm1`kR?^q1RP)nFCL?fWV=p<^0*%V?k7;R6mG_%FYUK{6eh}Dpz?KHkGUE}H##KnH<rsiu+PfAJ3NXl~R;ejPRDUQ2XTkyaELwZH^8qi;xRsR8l`*rTiqbQH<NvY$K;#C>rzx$mFsrD9WF#W5+j5UN}4ThX(RYwU?`pKql`FCI|9@vHlHo6R4a>ReKDTE>Gh2S|D46gQbKZ(a-`^iQ%7}2mMmtoDtuf52Nz!MG|iiWkg3~R;1np}qU;MMI3r(r|W2y@|Vh}h`vUM!z%Tppbtk83n~YIS$7y-zqU+F(YP9cBy_n_c)){)B_0O=fi2Wky?3WAnfj8_$0?l}9B_X<TMvVnX_`q=ac&oQY3MnVgoIkeU%SV=|v&s6ka8pT_q--@yDef~%XZg<cbXVOK+9n9<5#_f28uU_<**lQZtxLQNq?tBJ>5qt&RL5Nsy1*%Hbd)ySE|52~ZuxznM(1i2n4jKQj4h&2?yRB<I4+WZ2Cb?<7@j!AeO1`pOzTz{jx{-%HXTWpW}59!*uZ|A}P(O@cm1_oOQvZT=(X0;m4+(@C85WaH^?e!Nc^wMlJ8Z~2C%tjMGgqU3HSX6_+jQo|~8fxG#lqRb!B-9dWEXj~&50+6}|Ip$MiTeu-X(@gNW@N{ZN9QztB(++MR+}Y^8`5Nc)MVl-=9b}xF`FORQ9plSJG#?gG(EB-f895kZ5ESzR}^OiYspI}uDh*x8(K;<VOa6w8$)cm4Y>&nmPZGAODN|DKMtC>2|}Ew!Vt5?#7|Tzy+Uk{wl!xSN1<j5He+b0;nDfuU^Q5|tyHT!Ez1v;7OR<CUZbNmOtYia5N6}YXlqHkI>dv86sy2cyeW;w68E*iSVCwqBU|cr<9pL$=4P@P)s5-=i-{Y;Y~~w4B@_>qp)S^O+1$>pY&6-pd?>fRYCD7RQ5R>cHLN7#nM$5`vHi^@Y-O{#MB9ay5KXK`Ohl{sk?r`_<9~KpE$VKznTrz97!s=4!D6w7^1pG625dT`!RY$OmKG60i~b?RIseEf21A&UQ@$iqT0B@su?nmu@X%^0(UvxkH?^Dn_=H>9T~zo#w57v*+|tGnpSQHp;OUljw-=vqKf4bK-fU>2(YFn4G<m!m1smx}Hltua`@9#8W*_&WG1TY1XncY*ioxJ?zR6&<hH)xrM`S01!YtgD=1`3d)<;K-$8W^ou;xyQA>>h`EhNmyx2VagYH@ScDb^M~o>YuaepKNz`d0(~gGBpdByL7VLf?ec@fqqHprK*LM=b*q6SX(VRc*29<5g%fhgppOPRE1Jk6JwKZ{Qo*wLcG~HnXb&Q!xsR21`g01vabk30Cl51w1y|o<M==KmAQ1<`B<UV7C3IKR;W0KE9j&Pc(mnv1os@wj_@|z<*y<f%!=$;6{NZOp6YlS|GG&|1h)F==ln4He1pDVcN@^r<<T?fAxLPCz!wSKm85XkSEy#>f5tL6ofs=E_9>791{8jD+moO5(P{agV84rnfObc(H9Px!VDIh4;(TZEEcm595NdXPZEay+n@h=Z1cs1W|J+<;*$dPb<+n9@E~9``w$1s{IF*6ArA6$^pkM-KXK3;roA}1&j0c2s`E7!Paw<^YRQSt2?z-I{dIsYz50XS)gW@={CWG0>@^Ng@SrhuHM}wUPml1#!(ZD~TsWo`^8{~uCtJfc!n=Efuf1vxQgQ3i13bdKuLJ2R5%ak@&^$}TeC-U`p+wAW%aEN*#CqTDF|QS3tk2=H{|gcN{NMPyi#>i>xjYp&SvbkA+f8lPZLZ4e{&MPci(8M*C0qxw`we&af)}MP(6Hl+s>~PsiKDlMBl?c^2?wWNS8YRT99-lR-Ws?yNX1uoKIaqWIvq&A*O;%7q4j!=xy>1}zt@;^fFVA3jdh(fva8#R!K5Udd+G?uJ#~-FtkvG(3*Pbl9u22O*JQrnn$OJD@S?;?KH*;)Rn+kQMyq|o?Pi}1QgPnoEk0qclOg?HW4=a)*6TIqHfPBGUSrMyhWOw$)^)zscZ$6jOiIG1@9ia{bGy**2OTf;1$V8#S;KMl?l^qGRqm#0c<kgz<_mr}P}1<e_h<Wr_l|unNX4h`E%pg>oeb&s8uK+Wv|g_<w>d-h_Zo8!FvJJ1v92@u$CdVCFewQ~-pD5Whw`&eM_+LA+3^~N&z3oS!GVbe4gWl@6!QgtUFxK|Hu`dAuur)6n597~j=T}>6XrS{NWa&ZuaTkkdX2fw8M43EnAZ&P!E3DRoYH8Wy%<bN!kpKHpJOPG`95JdY0~h@*OwIff}5<apy8#-OB}x7ufJJiSMi*Pi$38)n}-FdI5F`npD@?yK>EGLe2omP*K5pe&XE1R#+(BT@xg1X>-=oNr6<Pvx}HASkchBu!<<$`h!@@q$W!qYdv77ux#8^V7VA88&cQ9#IqzIci8wJak>vN>&R^^I`h<6U9Hrswi2)J5;On;oHT-)_l*1R?Zg_!R#bhb-36E$#J4nU%TYc;k<~kinzt@<rk)ic^jk(PkvcK1ubATZ}c#U<PLx1!qzF>WgQk5}2Vcq6a8ZYn(m)cD7RNQ3YGM}){NvD3VvA#!~>-8Gzd)8@xukrm>qlwA%3gtg`U$7&wkA}x|*c;&swjFG!;jS6A9KPU7bNAX+?El^KKH<V^=|Rpl`h>Yo2h#5~=4)hVy<TH(bB65iHRc>(h!0+4U1!gB{=^roud&;}r+mV?%}=$O;}h-|WXV%;V&XGCVV#ps{a#~zk2u%sHP-j6)BaxLDRw^sa8i2>@&&g}duUg2n|+Oa!r^mIYj|FnP2s-acQ*~uaL+}j3Vp(}>IJFzxPKXkPk7T12h#5~=4*7I^?HrD%^k@8USrMyhWOw$)^$!_CJ|q-zQ*H9OP{cA^A~$`_6b{0+}f#P^=}+su+B-Rey_2<N1W^R8tZ%3X@9Tr_k(Qq<Nj}G9Pk7;?A=Dg0WUA~2+tZSYq-L?0UqI{HJ*)7@x<*dJ;JpH^$Aq*#trp7!n|)G(o-Vlb9111mWcV<9mozPVs2XpvU7=8@0$>Q-XpBfZC=1_kFdV>OAQ`)gn5kJsp8SOGVuiKzH{m+5$oJ=&a*_UbI)mq5;181<|=A=;%q4W-~RT>v>Ha@h>oBZ|CY*(WE-ozB7(Lm+foU6*}|~=pJn~&$&czQ{ePE~E7$z#=iBNl?K?^e?u+FY)ILuN4^>i5{Mu33_U8q{CRS3cyE`ga50;NRP?1F3F0E|;d$<y9sZ4gBF0DkDeoDc5MDqU}tjOLfD6M?a<SAuRqsnaWt<p-PpNG51W0`Z4&$F|wDk(p9iBNuf^8&m5Y9*!O3|IYFrruNj$}>aiD}zF1C9l9=Ir2k&WmpZ@`D2+jSrJP6pq9#wRTgGk6rmjWu7&b&hpT<g?hI9?e%M}#{@g&Uw?dU_2ihxFJBAQX<Z-(%7;|9N#ZWr-Onc=>lMo_m$K043o=SiEd<h$JH-`=Glu8SpUCnx3NF*aGO{NR>Ji~&QPhglQpJs*AyUK7@`<oVuh;JMBb)k)x_h#!y`zu%v=FhddH_5q#+HCsvIOS}+U&*U$%CVhO#wa3wVx5>*r#96lhf=OMc6>NfIX0>p@oVz7V^qpaMZ{Y?mWZoZ59Z<GS8B5n^WSzPKA5Sz+Oiqj+wYoVL)c6qZ?O#KXWWXLY_zQm^KTxnRGIw?o3^tdoBeLIkk42K^R`w{M`hKB9&Ga5mdaa~IxE(+u`DmIv5@DO&shEgN2*fQ?-}-D=4@6sGfhdVvW$(rGoE2Si}pg<ACi?%jH_ATf>|W>(^SRQIhT!{G@f8RqCJA;F+Yc7rcj!h%cOuDf;oxXMZDd8CzEzbxNQIP?0mLN&Z5EAEB2%Q^I6pkS+v@&rS|Ye^9kng2PY%wTWJzGdb71M*kGrbqh(TYWNQWM#~j8w7pLAJeY;j9uNmWA`22D7O)|t#iB!51=dxe0e$3~zwzbGJcdL-YZ)7WXZq*`nyH+LlPh`7rTcjWJS=1NvIk#Oc7RF_iQ`yQpH*2v3KJND{+lAYrcFbpM><!khS0!?<ZM+gc@g^(Ry&@_7Yn%(WMeUf+n8Uqai%?oVCzIfhTPqP(yYlH!iIj_J?IMHQMI63<J5#xka>br;Za(|4OqO!PblIL2FyDo%BF<y^8Ar2}1L;fcD@+SW`nfD6_24pl)ROr`#Ca@(xjO7{7Tq#!nLWw4fM6cR%}$`D_c7A?*GzV1cLMz*SRudPpTc%rOQMt0cayR!vt9Ts(o@hbguavdI=TFuzw%;t1C{QdBKe;-a^W@}OSDINpZ<Wf9e#rJNExd1i@8E}y;(@!%7{`h&+%BIz4Of*70Ih_9VN@3OIF&JuR^{Zaf}=rlkCECJQmiExsCOR_Q)+BdslTjMyg~dD+K{n*p%0flKr!iU3iXVMEp0d_<;E>C?vtQp-R}!D~$CyK?;sVx$qpzi1<J3K?mi^;ZtN=tiRG@sX@6M`8xTqc4HTAV;K?WJH;j_)(C}M`6QE7eLF#MWHItEINgQYSmwmtB&F1~U8MTU*`%-EL?!Z*-DLaPEF#(qnA^Coi1V0}W!p`p{mSnq);F?Txc!YWj($_-5{ZjTWqu#W(e)p{N5=Pz7IGWwvF=Kys|T+m=Z4Q9KW=YJgIeDroj<LseAY6A?)dv#vMjQi3%BuDqJ2~lb&+hkc#HJP>g&SimWQs9=?%UkD-QHj@K~aKbhmeTl63nf`R%7T7e4pOt3h&?d`Y4|k5%wkqJ4z*i1x^<f0bj@`XzaPY@7?9>-p7W$2Qy~$2P>d$cXr#_V7Fldj2+fzGWX5K10rRW;*c&sX4Hhi;Rf>Z%u5Yq_4kC!p_!l;q&K549d=bZjd)uRCkdP@xT2uu}bHl4@mOf6t*}&UYStyBH8ya+J)O#M#O*2ZD^OGe3-wA1pdM~(<?<;nXrL0OBqi@djZRfxHsU(6uO}PT5_l21cEt?WzH{5p|?MNo~7*=?;`*Fg$(-6hi10o?NnBIXePbb-^30z8P70>2W{w17fxR4=yj#3Qhh`uy%#>uaeJx1BHBAxC+6+ZO83Z?!a5xT-i%SUum6jTs!=MU%`amV(cZ!1V%`S+6hv+XSF<l&GD|r;tu;APxskn6<SZ9Hi^j!#7U{&i{pW5FTe;BR{^8tNir@6s%-pV;y}^K4E_@crW8T)OaF5-xnj_Aiict=3{EMxfXAS@J*D)@97Rh7YmO0X0*%+7VIR0}}<wB=O<&)5r4wCNg!e@~@=J18TGL*T6A*|l5RMs;jQ#r!V$Va5{OvL$C_7o-M@CG)Ga~1RU{aUHYb9J9*HAcq}tTXd|sN(2wj#V#Rn?gjG(tFGsEMrX#iuo+k+0uTU)jNHQ?X1&_e)01S7TN9wt4AU!)_LneH71Yxk?o8fOLLmkVVOa9Si$VE6!-nkT%A<o?d;H4y1Y~!a=pcmY<2ipm%dmgved`q>!ml?-)DQ#tRXkZ#hYKSk-K}kw7<B<LO)1+lYO<QHf?pnMlEyCvWqQhxU}QF*8N%vowRK|Yt%BvW#5Tp@E#m;XBz$fyRCLxOgdXXVmjUHzsG+6?<CgY*mQd3rEL4KeiMoLi*EG&R`1v!>}aaAUEPzu9`}iT)Ax;C_Ni!(W1Wdt?vfpr-|flaW0l05Kgh+yrAgD8(JuQG??=&CW$Oi!t)nZFx}&p|bw9TxXFjSzE<c#zvQP1T6pe-VqexGmdVws8pM@M9vlY8vD;6}SBI(&U+hw2P{V0-|vG^`)pHhZA`^Ok%;i*4Z+NIy@y#__Q>{GlSMKV<jx+w=He`XKPYN||mqo)$G<eWXMhQG@`#rshtgZJatSEnfhf8Jw1)+?QrPo1tTd3CG(o4OO3Xy4(!<!#fIlNDyzrxv6W-1o;_)0MF&7TQyLO(b}4{%=)xWz+aE_6Ej4I{2wbW$R1x?QhKYr+A;@aj_n}Pq%jXl~tLOZr?U1hUS<3i-p%(ZeNr-hKgbW9t-c~SB3_$%uS2!wVThPvB9m`z`t_sWv|YpqWFNv!u!2ucn~@9N3Q*R?O8OZYish#g~j&jU(FQ85ImMBhG0E7R_v+%E1BPGxqZT@7<xVMFVeP2hP}edF~Zn_WpF&1n9-e9E|_n>P(P5)OXoKIG{$~^i@z}bU>O`wSc~bj{E~(C73<RpjvFV#yV6T5{pr@v2}xqz>6x1iX&Hx&?fbDiz4d1UN>e+##2=BK=4G1ES?#ORfW2jvtc}g-{le;W)GbNDaY>{T$DeV^`{dpq65XbBR%{3UN9r#sP5X=@3XV&7EK%Gm_`E8)6ZtDSQD=<Oy>uP&O56J+U|_UMT*70C;vUu`ifP%as<LTY?~z?6q80y?I;>BPUrC?Oqg~<>mJ!9PGoQT2maQm7hke&cDbxBRcBP_B*Y2b)aS6+a;?=vhAZ6dtYV^$CWt7)GZlRQmuS)-SOLmD%SO&Lu%jvG9u4zbbl<&;)C-qR~aesY2ER5k8g=5k1HC>fE4u3lSpoKiUud5O$`O_PblwdtBu}ct(s+*c9LFMbw1NkzY`CfnmK@I4)1O9f=iQ^L1gX2%w@^dV3X;oU<8cu)eaf!9xSDmiBXK{%|cq~z@JAa}A`<(dE1usWYWq(!HplU_B<@OMlScJzC#k!=070AvH{3sh7MeEnBMhXJ`=*GEGF0lxYC5m-ek0_39+x9m3;BGZqWo#II@AP}5aaL8D-Oc6_i?EC+MtwETpH4}sPeaPd^vzm<bjgFdbX@lb1jiyQgJXzHyV0SaHKuoaTZt%k;TV!Cze~p4nm`W@d)>aV+q<M)yCmB8vpk2X=_OKe`ve*_>XbvIAIGZ}m0lrph9uCgQ<k&w{~RUnG#gJxEY4t94~|QsSa<fFbn@DZ+#dZdGt;^GB<s^SIyCGJ7yURciQ?WnTVJ$S%!#IkrvI>SuDoIYGJXurJMlZiu?UYPihEd(D5lk4zu(c}%V?Uz{$i$pw;fB2(X`FEzZs52SVk1Dnr};E3zx;xk8<8;AHTbpDN|zT`>&s8I2K`<b_E5@R4tLNTfdZT-soU!LlfxlBXXE1j^S8@`*IF2CkGtctnagbW=){|2kvo*;uwxgxG(1qbMnW|{mz_zx8oQkif`P%%;{gk`NN$2Ay^NNOQN{Peaf6ZC7eIZ$sdCC<G3V>d))61r{4+ZkHg6yf@2XLOBDCG-|bGn6V460lN$ubB0QET?qNNmn8vw5oZKLsKg7u&f@2Yu;T#}N4iL^C;^Yqz#W5U<a9<olIDd$fKXy?Z!!gA9StM0UQ7pnbu{@45qS%GyMezjd!SXn6h~g5K7sVVL6R^A}Zs5I-<wfxU?|m#UiVt{?7qP$Fy)2T)`&6{|i`d`oe#Cl;*#Ggq6YXmk{b+xQ_HPmUyWN|3?-a4W+x><2P7(XN-(QH&ZJ`achPM2t6)#&sOJ25w7QAc$&3M@i0(cn!jd<Az>hZE3)Z%3=sK(1`P>Gk7pgb?jLup=?=Ho7xpOe?f%lXfGUaprn^K!GijhEZxJYMF>dwIE6KETTZase+3<ior?EFb6Pak-F}h4M*Wo|Mn<@{D{|mZ2P2pcGgk1j;}~utQlOV1^1%6}o~Sbc1lH4Ar3rRDqt*32H!X=nFNWAM}DcP#*?ET^IrbpaC?7r=TH>fT7R?f*=O`VJwV<rqCS5K_Dc+7zhRl+Cw|&0OP>~VUPg^m<p4?1{7vOD9nJ#5CPp`9(05`Fb%puBrJf=Fdt?^ALtKDp*JjnMKB1W;5irwx$rCuhf%N&hQS(G3DFP_n_)C;g6AO)5@9>U!Zz3lNnnIzm;e)DC!|6qybLK&0Q(>vvf&s^fuoQQ(_t<+APWlNFyz3~a1v&L0<Xa{uo&Kih42QPhUKsV&ciZz2i}I&uom8jRq!6X3maeyd<5&^8eE1KU<Z5(Tj3M94!a-?UW7c@4>w>pyaeCF9{2%n!2vh|ci|xX0=MB1oPgiq75D>wgyX>AFL)LHhI{ZjoB>HX1+w%2-hy*bPC5(arP9&`xCE7@i%>=KlRkheP*eI4YDv|ltMD<@ll}+wrP|VGuou3B&*3X*DBXnbpr!N$w37U#Z{TNWCw&X;rDoC{_zg_bPhghXNWa3LV3F>FRSJ>*0gxi3hhUe&q*78@sf$!b>MBvGf>cS0lqyQSr0!BxsfN^FswNGP`bc%82GTI8uJn{NNNOZ~4NauRQd4P?6ezWpGNm9XOG=fROC6+{QVS_Z%8=Shq0&4lSeh?oO9sg%Es%`TGtyisTq4p^siU-9S|W9lx=GJTouyS$uGB;7Ev=J!O6#SyQeSC^v_<MCZIw1i1Et~8E@`l|TiPr|Nu#6}rJ>RRX@@jI8Y8_djg$^ad!^A*taMC@mX1sL(pV`@dQFOvPDqEPcqu_TDUFj}mmE@}G(mb(8ZW&iotBcM04Z6TD5XemOOvH((p4!<x+1+RO_gRzpGfJ_$I^$=4C!g<3u(G^Q~F4nBQ2D^l4eU^N}o%MrDf9h(jw_Q>04=qv{Je&JuCez{V1)Go|pcVR!hH0_oPkIHc65<N)M&Kr0vokshs?RR8|H#PdX@7mUl{(<TCPp=@qG_yickj`^g2;t5SXWC8?fVO+G3WN{!?rQbW0ptVpM%K$%HR<tFkQ(pjmEd`4<5H<#a$rbzEe=cG$gTlu1NS+dF(B#Ug2-<PgS5%LF;T@IE1C*6>`$k(K<a!2`7>6X-8{!Hp2cap!BZcBaSZ=}9*FZl=QCuxX$M~adM$iGPUr4jP4(nxuz{JZo(ijn`2V&zftKT>IVy!^M6D36t8xuTpbmy%QD1i8FiT~3!P$W!G>auvC*JYB9T&yXj}wd4l!Ou4o^OU{xT%K`Fy*<W5D&yj=V7V;9gnY>h9D7Tc)OC97^a)`W4ZZDhV)p9#|mApbW%Hi@l*(5(Nuas?aXL+L>CU270%0%uaZ;`3IRo)=?lzYqD<w$vl{DRz19w_gU`^&rKo$?@gn7mIOEbo{1$iwB)@<I72`6c;9d5k<xenpO!56Ss*oIFuJD#y#m<d@|M@)Y?sIY~YtACXh#X)=@3WJP{e&XBX^*X2z4l<bgm<hk-2@@)A{`LsMwenx&<ep)^!za=k{gXL%C#d5Cvj_k>OJ0gtl;SphcKaU9GdwWC}-{&L3_&y&`?orY2feBx6!zZlYOH<}@5b*{7U`okTaqg*5pRj&!k5j+bSieWexn8faC->EOa!-hU&q=S*wTLfRzjvi>hXFp}9b?wzso3voyiZuam&U2zYpmas<6N)T*pvHMJh=x$zsKX&s0PFrtlulrferKtv$vMzsaUnSFIc~K#i`$GtltCUT(8&Illw+Ix#vN@r(*y7^28Uc-<vUUjln0J_UwQ>?Y;}><P+BK6>;kK8teC*IM?en_T)Z||G(Z#Fnn26<w%tfWoq5;N%gpD%84@_l=QD}lPwiqVL8F=mEAX*(YSMmS?bsAl)44YD3;%q^|PbLq+n&*#c=vy(65em1A>)B*TO08`~2RY?S+xS%77oj>DVT}+8d7xRyw^EPH|r>^W}(F_}}*JlnaLD6xJRlbDFkSM$BvG(*D#3RcYS?9h4r=eosEJRil&s>7abH<2J$Vcr6nQHf8N^3)t^pG^6jX=%nOjWwYqKMlS0rXa9^PHyg$Fy*ZXn8viq^9^aSE`f3yv*$3;vYoGFQP1bc+7@JjY2JO2!kiApS#HznOor>&<$HMkWt67Vzm~Uc3`^}&)4G1L3Uxc%i3Dc>_=6EcT&9NSA+wXq;jC?es539d0hQ1W@6S-G7maT$OLSJARZ2!X2Vf3epGuXGAo6|FkDNP%+h_yf8Q0Ol#gMDNTA<C)Fvfa_9Exo&wD5F=Gv+v#2#>Gd`i@spP#?*^wI5>gseEJsKm(V8S{Tc}_dT?LtFYKdw8*8&!N8Wq&gHAcL!K6Cc`(^dRa$Ls3`mw*TkLqu%t-aTCnd_-PsScTU_`O%_ay@t~tRMT!MGxwW{e^w>&NE+-W+z)kEFP3VThG5ms_khQ@l?$O7a81+{e^urvpu13s;s?z>$ddeU4%BTS;`)^r;UpYZpZ$L9cokdRhUicf8Cr;nH{D?#Lgqvnz{P!;_}bfxwi-@Hz=0=IN>JCJ=294;$vKVhxLg3e(g+6_D4h$(lt2S#b3`^>#&x&0VJthw#!%|ZseV+NeVj!kUyJdyZ9@^R);ib+Js1TvV~(|--+~K-(5=kj66u~OiGz!X;|(}5*JBH&JtJOVHuH6e=^wUgrvFT{kNOb()nTZ)}OP<fqu<ge1~O3KE*yNHI^u`z3<wuWwfH(FLqU$udh$e#ss+d$h7q<);hmkVbrp5G@{}?);4ikgq6hz{f>2FzYIBDmtBf~&M{)qEZX!$5Sz1Rjw91FOUMm8F7`{}$+~1k{(J}7Ig7^S1rh15Tt{~GSuXw(jf?#y(usXEY13Dv`hkNT19HdFYL)Jh=l%DbSo}te(5F})`{>rscA9X_k3`jOMJFb7qd(m&MMiuQAoMAg$9}=~7x@m`R^&TuH<4dNcE)xP*$1ytw03~fP!A-i4>dr257{3|K@+GAWxx-bL0M=H4WT?#gqBbNT0v8&1XZ9NREGA@2C71JFhMmiLkQG@20)-DM1TeALI8AwI?x5epfR+7-p~jlfkF_phJFwTeV{u8LkAcFZDA1f2P1^S2r$5KhyokfAr7n%3!|YUbcG2J4&z}gbcSA#3Y{PY#z9Z$3say6OooXt5C+3E7ywz20mI-a$bq3S3$kG(#J~a=1q)#|L_;Dhg)y)U=0Q9p!*h@TD`62NK^m-vNw5Z<g>=Y-4KNip!aA4^GvNi80o!0R%z<Yh59Y!y*a1(&a@Yg&VK3~2#jpzY!xDHAcEbu-3kM(<4#GZo9yY;CupSB^AGW}DI0Rea6?hrGA9UQ2H+hTp_fav}?g?(P@Wqm_!xOCPtd+mVQ*3`yeEQzrC&7*<!#2m;SzGC7zVC~{c2BT%$@Y@4qa^&_XE=-2_}_nIs7Pi*_DtGn10^2HxQz8r>>Q;-(-khy6faFk)#^oSUh`C*B6*iNe6xBSU9|iwg6H6cyl_6)Hu~IL<%Kd-B%{y4Lz%~8Rp7C(6pw+W`2QR62pP!BKpq_>9zUz|vO156Wq72l%geev4wmEbvpz5D^H^GuN7kymtjc3)B_1yWcp1PWV+|f7oAI(4kE^wK6mG%G7CcHe;4#*pm;OBJp1#+L<@cONFP!gN=n3wTK{fnJr%Z<@IQLYhhQGYD!y}wre%<4~p5XkR+aJ%(6Rh{``%x9UCs?1`xQ=5z!us0PzMkOK^|bfHwYxxl!3&zL)bNHXwH?0Tt2+xctlow03vLs1>9I~<aKjFtJYJ(OSl5}oq_y1_tgli1+{72G+g#P@3+As`EN`-1y&E~g7aacHDGk43%st@?zTfI&4Ilj_r_dMt^4xomb^3yNI92pD`hs<xU2MJWzF>Wg*Dg-;3F|gjb^3x2ZTXR1IA2NQq%XMk?Ry$_Gz#(wkIt196(9F6;}gzr?WgEEeZij%sI2H~^ablWPu}0)6V}(L-i_l6)@`op^aa<L4@%^XKgksPQjhTFS(1h)y*kAs?02=4hJPOt?-8D1DEqjtCs=M<?(y6_!Fu1|t(!c;`rP>0#v`n+UG3`$#^=iN7aPz%pM@x0ub*Q#)-|RXl_Qk9{;Sy5DIMrHg)Nm4$9K5or=2~QKt>$=fn9xSl+tq6DsudP)s&6Dbysj-ERSXKUz*2e>_6D?i(S){muKcP`cr3e!!gO_?+x63WkEy5-jvW|;m@%<5&p{M>A^HF`dt_O-!Ae~R#>{yW($sxtE=iLoxklu<*myI?u+Gj9GJqYU3!(|pGl+#uJ2%bUph}())-B3Uo2nqMmG6i<kRfLtTa0QpM4~z(pvUIL4r$P*ZjtRWwx&fq&v5@P#XAMCfJ_X<|3Joj+p7gY2UGkZz?F?z21>tXm_7wm%Y#KecPRmo_U&;-!IWqyN8q4C*-m=XVMhxml5r!k)d&$Sef4^DI))3oua<jcR%hJ%eHTO!?A4rbmdCSJhtlCvyL~bOmp$6s2%$h`|;g}J(TWw!$|toy2`Aa0m^~E9P-zX<rM5w5eMEWMU|R|3rN_>>U1^frF{5RKB@6(DT?(NUme3X(Xu3A(=>|x{?F5MS<lxhkUfc+RKy>wv;XU3$)FC092?%7PB9<0G?_=1e##slt;!PW$2<}B6>;XmM-g<&2aJ8ypc=(~e{a8m{&n~dHg8Qi1@q+BBn!PC^nj(_{D<MbsV{Y+UtG^)ZA;g5(KGa&D3aJekM(>uS;1UtZW&L4KG?_pnl(`ojfMFm(u28V{4$!whBsm5U(0gglHZ1OHgj?fb`-LNGMHDGGkX$xD-|=Y+8<78puCzfP`MZ;kt-FeE0`On%XU_t>c4|T^{h#8-(R2Ysl+60Bf;1GDAt4d)1vBVw)BU7#Jn$qVlLe&H<?BD8c1%Bno31uiTIQBTnzdA__Gl&yf%Xl4a_9FE0T!smrSRku`riJdN7wnexK*xgHGGMpY^z2fnuH%E)Szm5B-V#QD0K9e8(Ey>C*i#v+B(%xb&U6rWXwyASn-T9cFQK9Qo~s*Vy!g@h+TcePlOT6!kvaERS^Ik7!)XACb;-`3WrJr9*7Uoe3_S8FB0&t6lH{8)t}j;g3lE^O>EMD+k|VZ|*7U!kLiBQOYwt3fRz#XBd_d@#LM)`Y9b6_G4!{SEX3b>Tky?9rmtdJ%2e%Fi)0M%4EOwxm{?;m`+!8KgvG1w8JrdbgBzy@K{*?vhWPD;Ob#V?X}ZfIMX-kD5+I#v*XyLR2Tk;#>Jcw=@j|>yVfJ=oy$jA)pMs^?vcatm>VK_%ni%|+}Gv4KEwyy7yBK{W4~h=>|ZR8eT`+XAF(|49rlq(9{Whd0W6RGg8O27s_)A+f@)BUm+E_Wji5ZQ8$oGaHv;w3lSXhH4nqMH^11*{^11-d@VWrb^11-d^SS`qKsk^h09tFg^Xj{aEg=}nfEg-7MKFK~{2&Z!LKO&waHtAhpf1z^8+3;1&<h$u9iY%t%h_)X4WK*phWZeweOA*Cnu0%!(w;>a1S25`#y~r01;Zg4TEI9kLI}h_Jam8*u!9v6U?NyxDs+Vim;h6tBg}wE=mcpn9SF>VKF|X)ARD^DP-qSVAP0s(e^>$|U?9wer7#$l!)O==i(myj1*;$q#=>*324Z0&Bts&sgUv7=wnI83!3Nj?lVA@_gH+fGdtox{hnbKGyWjw1!P5{0vmqZAz#KTLeL8apj=@5B6`qA>;0U}1i@^b_As0>ngO%_)tcSIrz$thh-h`d72~NXXum#S+K6nA%fOlXUT+lN0--e5@8(xO_a1h>wSKuX3zgt1|IX{;>M0j-Wqvw%|!}&d9HJsn`MuZ6aT@5N!vHCenF<6tIS!;z5^FKVCI_C-TjqF;^`EL~ByvcSA=bl<C#OmGeD$bjnBgE?WFsfMn{sj>pe0(d@*C@iHbDw6qtwdP$i+Z29?jv_t^-D=u^-H;w5A3>+++o!(<&Wmrbsq_^!z}f;>ppUaRlnpE#M^Zrxx=bo)X$c5AGyP-U(z0Qvg<x_hgH8QWhdBmAGyP-U$TY|w(CA}hgHAmYZPJCFS@NnSpAM#)pzQ9_$sdQ<}JI5MW1;+Uv8#WZ@&=9L^4Sur)lxJ#@+c$)ZTK+3=OyFljtHdzc5B?KNND0cp@|B(lPCKU*2(jjo9~fPwoG<@0w6gWa<r_uF32gHQhx9w|AC@YHfobR(6r$`iZXJ6PbMrMrmyikCbwq4{Glam!;w8Qp;S{j@yg##n~y@v~6${@kFMmzudJK^@T1|oWI=36!nEJQ=Grt$rSaME>oPpbeZD(<xZxkzaG!07=P(9#rx~u&rNlC^>fKcehO&LPY*4%Pc57AT0O6n<?U_wZ+h_)Lpgo|QJ-!s!&@ux_ICU?z4%F?B0t@z85-qzYbD+u!hh3?pHeFGQ%ZYY`|;MQyxqiq(~F;2s`GP;n#ECtx7Oh87XF)F{H#$^%MP*fQhnYqlAmxaygi(sW@_=XO*k)W^Yc|CKZ%6#cEV3Kb@_RO@Uk91^Qbu^5xl(<KV#MBXO~XAY{<_#k^FQ-d3#rW`f1EhNL_j9&rd;-{9M$9xA)*DBQ*o12QQoQ^HwCcLU-QYf}g;G_$f;LjMZc^vBAgl>EHVdq&R$M)=M;XfT>t~y;1?acF|faUedXM9{t5$ELP=L*Xvd+R>yttd}Og$oxhr^TpT|7%fZL;BK&sz!N=o@aKjD<AJ1QeRe9YGBCL+9+tVGcmETjF|K;heJ;ne9lv;zm!Z&^_pgoS7JjVGwU)I*^DOUToG(>ug)w#7V7~nBh?XW&|u*W!W^1;V_J;A5v9(X)APw@R#2Oh886Rh^tZR-hE=cfCvBy9H^{&<gjiuL{ODc1MCH&~Aeo?<;dc#8E{;SJVfh^JVOC!S(Gws?y5IO8eSV~(d-k3XK^1C2&%YmdAUUM!yRZ9dKG-LY7lQTZi0XJSOLcw2*)v~?ASRrx!!Xt7uw_w43Q#bR~-&C7Q77`I*YZ(k7(iO+vL2N5nkEdTLZL|B#AZ6d<zxVmlKVcVkP<b-h=DYq|Cabl)ooWr(u;c;^9qgIsvC|JHY8UA~!>cTRporq+R9*X6QlX1?679C4(N9&?)^e9MAi8AWCi_QnPBg_PP6i;Q``9kEcBeQO^DqALzo$rm(F;lU~cax^xW)Hs)p!~<B@7bK&tkHJ?l>aCqpBC-Q`%!f~k$;g4!SW(sV|g?mD)Kv;KgIGQ4q$m?D=OjxmT~G=(0u;G4d?t7G=D{(k2{`Vd4!pWGgt=cS48~5e8BP|&eVE1MY(+Kfc<#XcILzm6^nRM;lUJTUdLp@e;Dp7;z@CRc|W3#C*ll}v5Vv}2atY(`-(VIRNlE3Qcg-&!ml5&e;c`-i1>r$k==-hKhCij8tbvVJN^`vS8c4X#T|dJ48jf(e~^AwRNftbipuLe5%CBAy)NQRaWcBEv5bfh0zEDq5XoR)7ahx;e?{^l{}v~s`^(K5|Kmr29_FcxJHIrB04)={F)!=#ItXg<ItZ%sItZ%pItVKAI!JpuCP>Tu4g#6iL68f}VF|3_^%7Xi>m}Of7E53=ub03Jyj}u3c)dh>s$>c5<+b`G$zEQz)^3Pu#%q9fTF!YZUY7zR_(3^n&ujIbr^-+P47{!YVNew+K`5^)fgNf<H3;W*HRu9$pe7Jr*M#m+4{AeaUf0$>OR5h&cwHa*LlbBOy?NaT25Fxn_2ad_men2zgLxeYBea{YhVr@vL_-H?10!K91Vg;`)Xx}Rhd?4&!KB^PWP(W$0X7(~-3FBg6gt90UU$?!Z|Ve-dEE)7LnL&A3|@DGna~G%!Zcp@ggGz(`ob(;_k{%zrG4JCfS1FdB@BW2ydDC}U^EPeMZ6vk&q550f~CA31uG!|VqpcZV_^*>!8q+Rsd2DQyD@4tuP49;m;x!<6FTarQCW}<8+n}$+h7J{!WLd<!cNG6Y}n50Y}f-&!)(ao^=#M&3t=AY=Jh;S3{Sx`u%Fk@Kz`5d1m&@ph?C2&BPdV4M4Wpnlb}5O5^;|VN>HAEiTL!rRs=mqP$Jg*I`ia9#QNNvdH5w_eeKRX{}OS-4xbQ|Pwq8t6Lg87{C2PL)tv<d<=cCW7c^T*Q2xKycy+x61U--7HP&@H^V_|~`Wl`2_FiM%=Fa?ouQ3m^6y=k9jbEO7kD&Z^ukrm>9}|>s?==p8?-W7#|6XIhHiDi<@EYqno%!uvV||Uze0#64ZgXe;zt{M)0hKArC-)lXxAvnbzujv*I#;GB-`;Cn`}RG8^8dZYhqnAk(DMjhV_l~+zujxBuhE%r?={wK?#%!98q00VQIyACBA#I=OHrPDiP-OIDT?y&OT?RJNfhPzmxyc32a28}C=u&@oq6&lVtsDTJp2-|zIJDxe~B39lfTfkIz9ABPx|GGXGqkMx^(S6GY!7<CVM`uDSg_{M&amMm;CmDY4gaLi;L}d>rPYVMir3bwf?gI(KA&M$zz$6kH)gE<0NHe!B8cKJkRWjWtH{A`nu%j<M!1PYANLx+mvz(PO&Q+gOqxQLzTI&Jny0(x2MUim6z9bP#niMlM54DEBBvkq-=ipiA%mcbeYZ8PU+32o=&HWGIq1R=2zIsuVN_fi{<A`%Oc%pzCg}LO`;1|ZY9Hh`-%+fG0deemd7$nCs(5_|Bj#+dOHZVv#1^0|E#44O&vCY47b-+7LSdj%hw(zhMuLU6f}^AE}u+h$COvzyE2ye<sER8{d~HzxyL**@$K!7&p*#nu#ZGO#d<`2vF}d&G>lDou!hzC)zy!6znaDd|Fw?o+>tD77x{GCQzj+2)LmBpqw-4AOA*SF**~*SQ-5P3zhj?bc}r!YoC!L{HkPSQx7_QdT>k1TTU=41Wh=+9f{+c4n^k8}?DzC?^Vn$ReMi{PEGps**0Z_XSn}u5U+k0rnMN@m{720twiPwW_-dI#{g@}Bz9P=FY2Jx0JHMBFu(1Zk9Kh}C`gNvfTWljE=GCMk&V16VH+^d64SV452Fkvj1L??HckN%Asw;0kh$i)ZX~^n+l;y&uF|q07=JmR4`Ma44)`|6C{)qHoUiDfV#ab2aVzUP(yKw1?o#WY_)IH38YobsFb7^OPgYw<Dzu2Pg<rK`H%Vn*~7f=7i4i!FNA{h~95`XKY^gFVHRi!oQ-`lz?EB-jhVis0#;ZMq{7*^)=-iQH5XV7uYGug(QZ*?s5>~t#9gZWd?W;AJVsyBi6GhDbd<yacoG<PU@y53abSeQ#9J(x=(Zd9q$lYV-3CuzUT&!v6Y)UGrK3R${bUcoY%d41{PDHGW56RJ?mnOcK}(Pi`BVO>U^WNoeENpkJ|?Ayr`T{v^9_kOZx`fJSZ&=>{l_k@Qcon5xXu_5hFv)gYcxNv6Wto^J^(^px`pT@ZGM<kDV^3ouy(zxrNEHdCBs~I&wxqaq4W~lO-3x7oNm?zmE_fSU0>|$5P`O(((hAN+Kevid>RLF&e8SI76mO1AAIn9ML=jtC}-&rcN8JClV+`~FCPyYTegAAPB)6u-^beeGGDCwWRwD7}PX)c@*jf?ps(kbFV#>RL$`>h1lEAqTc{yCPx+z`o&xPkj(dCUjg7yBK{W4~h=>|ZP|;sEv|mdCym`5nt+A7Q^>Jy>4kUu@6+lll3jAP`!E?99(s-*?sX^Fy@vU&Ej}RE1EmK^5q%<>!ZM@2`sT^VQrlH9tSVnV;Vr2Ezy~KR*~+KF-fKfx(%dKM^{D6%rxInV)ZmNiYQ>ocZ~wFzs=EekRO>ZZHIzY5DmBwLA4kLKG~3WiV8jpT8a^Kmx3V4bJ@hWY`2dAO-fobV!32V4s$spA8w12QNYv%!NTP8xF$LT7Lc#5AyTX+mrsy&)@twKYuT5eVm_v0Cu7L{CsDA{^;CC-$mif-*$@=6B9{ExK{omqUVr{@ZjTH3Cc@%i(8M*C3+sd2;Xltn&^4>B5X35h@OWp!fLL%o`)~O{Er;Fo`)~OepiF+dLDi;I08L`;1(bEUuf5DCBmv-P`<retoo%StolXIAs1oQFDNhFEmr-a=i!U6>K8o^UxZb^=y~`etj=A}!xv%IFM1xn2&;b4^YDwo5$G8Nw^;RyZYvSy@&x7QlmDBa|9|uI|8IW&|9AQMYCJ)C=0c3}%!L@`nF}$>GZ$i%XD-Aj&s>O6p1BaCJaZvNdFDcl^2~)8<(UgH$~kw7YvuPOD7V}rjPl8!7^B>Bk1)zD_Xwlha*r^|E%ykc+;WdF$}RT@qug?jFv>0W2&3F`k1)zJFA>}Qh7*)q?h!`0<sM;_PyWOh<(7MdQEs_M80C{cF-E!N9$}PQ?h!`0<sM;_Tka7?x#b>VlxJQdKG0|+L3!pvjPlHd80DD@G0HO+Vw7ht#3;{Ph*562M;PUq3o*(w7h;rWF2pF$T!>N5xm#>obey4lW`=T}6_gjvP#!Wv`R76zlv}Q#+-ZjLlikW7Jrv6qCxi0OUB*JW#|-6`7uBO6JtfMZ{PUvgQqZ~-!MYS=pAu!<`Qpf|+XUqd6Fo0f<i|-<ZxfUQOi=zXL3!qG{adsz${Tm<Ya~OkyvXlZ9?ge}IDqC)i<3ur=>+8o>$ajIZeSUweg*0O4^N!)SJ3?3%A>q=g7SoQ%tZXbGDyE7;u7XVaq=iH-7S}DJ)A;O{xC)P=Wh8^;lUJ&@`NeMKX=QY;`*X|a<^PUGIo(X<_6MFa9<IZiprz>bBglM-SP^{BfAk1ubg8sG}dEzcf2YpkMhsm@(Rl!>=5w^>1Rdd-SMiZJjy?J%OCt4jfgYF$)MbFigL5v@<E`-g##iP?CYXqx%00`UgY26WKjNj(KY_Zj{-f+QyF)D3DRx|57ItO2-2R5SM$(oX?f_?wLJ7HS{`~uEf2lCmWN(O%R`r82`txg&vUih^Ho~z`C2Xae7%-?zFEsXe?iMV-=XE6@6vM5_ri<XCnmwX42Bj^3d%wUUUtxK3h)CnFV(E?3Q!qrytIKyy9b~nFFQJ)@~6C1pW3epb)XwByFn-I8GrS&k)F_1dxF0YFZ)2Gc8~f%UJiu5+VlHEc&UB|aUe+0l9w$ZO3Q>F!Ate~h}BPIqM?oUeZ*=ed^|7XVGI}`6cTxv2ytM6aG1o)NiZJ5zz%7=OoNF)pfgP6<y4pqU7!a{=jC+B(C!78$;+8A4SGXAn8V9CFbn#_U|7J*1=^<|&0!cXhrxUp4x_c)^JTCIMnR00d;Tmeg;?!7C1Ux{3K$1TTJHH8cn&5&vX*<k4pu`7Oo0uMs(r6<I%H|N=UZVTWNP0vk;#9yKsMxPx#v4!JIscswcPVPkO%W%p_Y5T4|c;d@RXK&z8LmH?x}m~T|ngO&Jb1%wtIpvoL^oNc9ewGyLZ(0xNl@1_7vNn6l?EIc#a)Uf-jsuUl{Y{CHv^yo5kS>PjFg|Qltc2SQ0M!-2@ZTW-I&a-L&s`E=N0yuKTJ|aWYgS6a7;XE&SnK=An$sSh{`{@3}rlX*0gOJ+pRiO~$WPW5q*xisW79Kt}YVyFRI>;5m39FPsm4PuAW1i;<xs8GQ~O$~+#cly>t9Xx}Xns6CI<T>EZ`YCH~0+9%o)kNawDuc>{vM1Ac!pxWAZOH}2tz9NsO>UT>7Xx~7gKDAVtN6R`q5;xVpTcU;bee^-vcT4#5*NX-`s;b{D@&5oh%eUS'}
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
ICE_TOP=GROUND+.4300000071525574
placements=[('i','winter-fractured-undercut-ice-edge-01',(0,0,GROUND)),('p','animal-static-upright-short-neck-penguin-01',(0,.40,ICE_TOP))]
def rigid_point(instance,p):return tuple(p)
def stored_point(p):return tuple(struct.unpack('<f',struct.pack('<f',float(x)))[0]for x in p)
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[stored_point(add(p,t))for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,rotation_z_degrees=0,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values()),coordinate_storage='Exact IEEE754 float32 after translation, not hidden deformation; native versus final GLB bound unchanged2e-7'))
base_mat=len(PALETTE);PALETTE.append(('SceneOnly_OpaqueColdWaterDatum',(.11,.28,.36,1),.55,0))
v=[(x,y,z)for z in[0,GROUND]for y in[-1.2,1.2]for x in[-1.6,1.6]];f=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];emit('SceneOnly_ContinuousFloor',v,f,base_mat,'Single scene-only finite equipment bay floor, no extra counted model');FEET=['SceneOnly_ContinuousFloor']
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
  assert abs(bb[i][2][0]-(GROUND if i=='i'else ICE_TOP))<=tol
  assert -1.6<bb[i][0][0]<bb[i][0][1]<1.6 and -1.2<bb[i][1][0]<bb[i][1][1]<1.2
 contacts={};floor=triangles_of(FEET,vertices);ice=triangles_of(names['i'],vertices)
 for k in names:
  z=GROUND if k=='i'else ICE_TOP;tri=triangles_of(names[k],vertices);mask=READER['np'].max(abs(tri[:,:,2]-z),axis=1)<=tol;bottom=tri[mask];norms,areas=READER['normals_and_areas'](bottom);expected=float(areas[norms[:,2]<-.99].sum());report=READER['actual_opposed_face_contact'](bottom,floor if k=='i'else ice,plane_tolerance=tol);assert expected>1e-5 and abs(report['actual_contact_area_m2']-expected)<2e-7;contacts[k]=dict(complete_sole_contact_area_m2=expected,actual=report)
 tris=triangles_of([n for nn in names.values()for n in nn],vertices);rays=[]
 for p,d,length in[((-.07,-1.05,GROUND+.35),(0,1,0),.8)]:
  assert not ray_hits(tris,p,d,length);rays.append(dict(origin_m=p,direction=d,length_m=length))
 return dict(instance_bounds_m=bb,complete_instance_count=2,distinct_old_models=2,new_reusable_model_count=0,whole_oriented_triangles_and_pbr_retained_before_float32_translation=True,actual_complete_sole_contacts=contacts,selected_fracture_clearance_rays=rays,not_navigation_or_full_space_proof=True)

LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate(vertices);result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,.85);ORTHO=4.4;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(6,-9,6),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
root=bpy.data.objects.new('OneWholePenguinIceVignette',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole scene horizontal centre; continuous bed bottom at Z0; two entire unit-scale qualified instances';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 # Preserve the already consistent outward oriented triangles of complete source meshes.
 # Reuse the winding-preserving whole-instance scene path validated on the loaded-sled scene.
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
  files[role]={'path':f'assets/winter/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'scenes','assetKind':'scene','theme':'winter','style':'source-preserved-faceted-natural-ecology','title':TITLE,'description':DESCRIPTION,
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
