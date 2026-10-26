"""Static empty trailer and independently grounded headgate preparation display; two whole originals, zero new models."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='agriculture-whole-trailer-ramp-and-separated-headgate-staging-scene-01';VERSION='1.0.0';TITLE='Whole Trailer Ramp and Separated Headgate Staging'
DESCRIPTION='One static empty livestock-equipment staging scene, zero new reusable models. One entire qualified high-arched tandem-wheel trailer with four real side apertures, two empty longitudinal bays and its complete lowered rear ramp stands on a single finite common ground. A separate entire qualified open longitudinal headgate frame is aligned beyond the ramp low end, retaining both portal ends, waist-shaped front gate, all side rails, kickboards and skids. A visible unoccupied ground interval separates the ramp and gate: they are not attached, inserted into one another or scaled to imply compatibility. Unlike the earlier side-by-side gate and milker bay, this shows a longitudinal ramp-to-ground-to-independent-frame sequence, with open side margins and no trolley, animal, person or filler objects. All complete original oriented triangles and constant opaque per-face PBR retained with float32 whole translation; hierarchy baked and normals recomputed explicitly. Static exterior display only: no animal fit, loading, towing, restraint, husbandry operation, accessibility, navigation, load or safety claim. No rig or interaction.'
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
LOCK={'agriculture-fixed-arched-two-bay-and-lowered-ramp-stock-trailer-01': {'bytes': 81324, 'sha256': '5dd9df67d41fb0bab2f2bad62a4cdf9b731b1ae45dd8095fcbc0cf1da8a56531'}, 'agriculture-fixed-open-headgate-handling-frame-01': {'bytes': 47248, 'sha256': '1e47b029067d195cd861686e750b99581db4e1cea896b4b7d08bce6ec5178eb5'}}
ENCODED={'agriculture-fixed-arched-two-bay-and-lowered-ramp-stock-trailer-01': 'c-rlq34ByVwuetOvKSOaLBs`O+%;hD3zEJF3aALOi3`XyNe429bnGM`BBPGtHg4mL`!;SkzEMV<MaO|$M-)fJaUF3T#a(gVbsT;Fy4{tozNxCdZS&^6dA}I%;p>}otLoG_RduR5NzZSdG2TZ+x7IN_;V_~@rcar?v?kTomTs>ZwX|k_x+R@WwP&(5qiPOakj=DY+N$T{k?OI{>6V6cw))`xrc^Hqj|`0r$7*V87NxUoO_>%b2S@sAmetm@)uVu#QT{x&)r>l3X-!LNA@0>ocfMC!(~@a$z7dShSvIHea%oNag!XKzjW?q{v#>SOl5T0Ao6R)yXJ;+IztwFEGTHX(`UPliQ(N_dRLlHyme;y4-L}A~G+&dWeZUFL=^2^vS=^fFX!_^!CRSWcpky_HO;Js-L^Xj;V@;@JH6^W?(vq%T>{PX&Y5s!h_61G#$5p4Y^$XGs)!9s@aYU-6VMJR~18+*Yxw(3AQ~QGI#!N@Hx;@*GuFj_G+fh|Vb1GZyXk}W{Eln-++p6(gbz=vf;CG;x%I;s?lBsS@HMO*(?8Qwj4VlGl1zW<!wv5ZPv^TYMWIEaoa2j(&s-wC6fR={o&6##QKfQ^^ooCzXGcAbr`Dhs0o?V>EHdHrcQ;Vw?rWek`xPYO&O-(JLrwh%BbZb_=pab#zVb0_Je@8o_rQ6{#a_h61wzhfMRK3%j7C4YMXI=(=mD-YXVEckJJeEC<YqYhe7Z%zRD{c>O#o;-{ab4wm=@%zN8k<_0+NGNKx4UYJ7uPi2(aqO29v$Yr_Zyp2?IU1lduCyE`;u(BI@Q{WxJ<R6D>5yPu}*Uk(GBT^BT^Vn)g64|Y~(|#(4vH@MbkmE7Npb79%iad-=u)QM4JNt3vCJ*+Z6a;>8D_cHhJnNylg@n=4CUfhWwP-oLQXC@;NiLuvLuXlrz+vxeo?pGTG{M!~FFA2=^24-M02rdsBUNYo;w-%V)-pw$wa6<2Pf%tcGqg3g@GtzB$z-4ZJ|eZ2=0Kl&gIjYMO=yc$*03XEVHu8j41EuGgFnb!LNlc{GbAgcVK5kI3n{S;9m0xn5{Qn$li9FSP_$miI$DCLa9Xv@q2?qOqx+_e3_`hO)43R5zp-H5IkQH9e2dO{z|V#-^5xO=bQ6#>PZTH74MFMs&gjYea5hPA_b2UxJ8encvjjfv89|^H#Ryn%KTL;{*!~s7LyjmR5~`Ynq;f62@aFp*iDu4PM&AZ#JhfJr`Avc&~0~TGYgYr6J8Ha0C!<Nv^59bxy93>1apiHa9!pUXaf+czz)@GTyzB2<UNWM>f@rrXsZ3o7#D*TB5n*luZ@cQ+|<c>u7C7Qsu0{PA~I?&Y3WB>6P4liS8|%*)^+7OEoq7|J_Xr`b#ybjF~<+bvX%IduH*7^b&bq%?B64-AUIFg{hV$)r-=2MqZwSu33HxN}G{ce9)4#_jd4j7}2&M)!H=%7pE`?>YFodB5pG1p*Ef*U?)?XYYv}G+p6bvWSg9v$w@!C>LQ*h=4`_zM(#V;<Uif1aU5z%H;m`i&O)so^YTn{6Q*#u=eX*5=#qS{<a8yv(V5T}WZICrXF6J);K%eKwZt`v=Q?Z}mW}DW$TAWqK5ap-rH$|A(oWDgmA7@Yp)GuWC)N`8LK1Y%;xoER;rj^xzo!imQyX%TT)&{HxgndzKJ^%XZJ;(-8>$W0MrxzAvD$cTq86DC5)G{DSQxP|VMV|^jCl{U3WhI+3j!35M~}ncU<7;Cf>F-Sd2Uk!s!z?&Hq|3;I<n~zjzuGKo1hVx(?(!6bM`^`MScWd<VUo%XX=j|!PkQ3basS4fX%TJyK@_w_^v3ovmS92Zs%6|xr>_GI#SJZGcC<aYDV$hQ*BKq+k_l`ZbPcQV<EJiEmeLuhHssS()dizm+7|ZdOjcW?168-@>x+XZ(ht(7bk1ZW$j`;Z$vyHI$P4I_61IO=H}-7?#^j{b-w**W!5<(n2S9D?$x)WIZJ2Pq#9DK?M;i)vuj3GH>R3-sxmtl3mA;3LwP@wo$H(n6n}FGrj53_4e6FlQ(JL)Y0Qi*&aK%s<Bl3P>7ePeYxw=P6rVetVgkW9ztg?|$y9@LCoH|5yAajoo*#ekkp~@^dwfw-dhy)m)Djpa)q0Fm?VM#i2=k$bP|oe2osOB#`(;MHTlg8rLaeFTCOqYwb2MZ+kf!ndXM^x!zL*0s8l25Hwy9l9RvUV@bzb(cG(6edR6i}#F@J$GD<S;mrP{EOYtCfHqrds7%`yIw!BE2aFB}a;BJn^XR*QS_+`T|F5($M9u@Ju($=&lqF&K%)5&68S`D#Rg{*eKH?!Q1d;SU6&Jpav#HWai_k@H_L9*%{>!RRtR@bs3>N@W)wp2BeDbL@0}E>NbGk(g6mJQND}qlrWW21Rm4#zL`JC=rQr8_{IvzeFSyjfF#eT&rwUTNKMZ8;(Wep;(}lMF(QY<YpjjF3R<pKN8M$U(64OMPsoj8t;$hZpNYk_%V!GNU7-EqD0Q)v3MjL3<YC}5*8iSfpvRqHnX_J$@CDD&d#7b%R=E?FNPwqXfPIcf{{BbkdMA7ni320nb*4+p<I!%KqMH6#KOy*A%@kU_`Fen3J43bO$(d&tdx5q)!v?Mn%BV-Uzl<Dl<5c0IC#orr~b)PrX6;`BqVYe>{z3buD3adb7DwCY1tg!k0lQUJ=Yp4)Ecg+)<8M7Mhdk?E3CB)TVsV<<K@)q>2S|;D-x2Q{c<z-0Ysr40cATBr+J<$=96hx&7q>2!=-ybaen8$X35`yB8T%GpRs23NuBqa<5JCua-81%;LdZUL1`!l1Lap*bT;R`R>{4=BKHQ1+#B>zZ5h4|O1=$7E2*}u86+qT=3u<CYRj=!8oeQZnbj&zzP!)V0jc7kTyZEQR~*t*ET4CIuQV)G8YwG~6(?KXtBp$4#)@o>mtAi;YoX-aaFKJvffDt0JE`(qX;>Pz;gGhEL+Uy;2T$H>mpmLU%fqU}CGXWr9uCJUtF{aWho#jZT-ItJ9TRy^a-?M-QnU<2N>!&m>hWH)l+{Iw(z-~bM2_J;+VNhe<kCo4E_I*ec&}1&XQarTQGZ!=mJvcxX&#OS&2?g@kgCV`+A`T(q4PQ#8`Ie%u+ewY{jNi*8B1EzJVt_1ezT*cT`VUj;IR?dS^8c37u?Eif#cD5Jc><LfNyic(cE4o9tww}5q~how<=97`7*lgPV<|ikZbFShuWR?)EsfpxR7(ECAT|Jy4|M7gQ~|vU61prKmYjjaR*E~U|P2VLSFk#ZE|`2rtJD3(re+$dM&c4gN5tmk8Z?{-$StAJCR`Sp+G2}h{gPo5_U%`vpcq_oo%vP=j`&Wj#p-N!u)t7950yN?bs$bGFTj$wSkfRIF0v1B$^1v<B^c;YQ?z^Ob(0;gu+E9cBQ5TzlTN}3kaBJhCtXKE;Tm<g62lVf`yLrhZ2!sC>V-{BcVtr6o@$!LC(+oJAr7BpHhyDCjyBOdJa7qh(wD9Njz6VAQ2A*;;@g;3b|<^?2m*3=+H3k#r<)AG!TyaBf(%G5-Hh{q0%-OpAVPl$560jH%7d7qoNba>qV6xHbpl^E9}Nt<=q(fK6?d15yxUoUg2;c?ssPG+yIQn{jr2U7Vz_aEM9e-Ug+vcRT-h&F|`=^n9Tws-R>#XlZgsfe193;;A&b>a|%5&7S+#aibC*2B<l1|Bo++%!;wS@ql1;EIVEPIKv-U~W4ZZRelsDG&q;!zID8r5;|iu0z3U;{9M4%NRzGgCA|Of`9rDm<V*w@Ro?xtGdKZj%?l_gzW%Zk?<9|rEMJw&L*rpB^s3FR8Lq8Y@#H0Rbsc_*XcOO*7X2&bFJF$s<Z8Tfy?eeV-`75+K6!1PDqD@7iTiZPq<+++a7SXN>-HWIl5gh4{J5Pj=@*y*Jc09&52P>NnL!pYdePQpt=FcwxiBK>R4##3)XD{G-BabhHiQJM93`c_gcr09$mZ-|`2P6467-K>B0V^yDDKAeBMJnvcsOQ`ajSKp7fe}muBG}yWK@%^|2#WUt-M0>b-0E8hH<S=6e(SrG#j(mVu~59?Oe~b}p3o}#pqyUxZ<0O>`z!0SaG>Ho3kSUqxNZr*Vwx(k3+-M)_w={?U1>N}*=P%wHS2Vr9P&Sq5DJB2Sd94II+2Twt{){So^#wKpdbCkKRClztVC|Q&o6tiQn_rn!YL;lE$j3tXG0*62>KIP;c+Yf(=&-+ED(r>65$fD5YA1@g%OBtOf>&fK_P!65D3S9$O%O_R$({9%Q=kdW<puLpzOy@(g_uA<|3swb8+cxs{0Rf@ljozjMpl2k-}b1QA8-$xdDF+wV_k^6djM3)eVt=2Q!QXlsLzZl-}t?O3Y0OzhO}djtu0E0%Djs5lj(2+xYXjue7n(FYWx84^v6F+uq1%cDQt#jn79)tV_{&$!?35F(v1ZdJ_SEBoV?i%mXlzi=I#*5b_5xf1=|Oxk)w}jRpgF#C1H?t%#5-*qnozSlD%_Z0v^$=b}i7xhN5pHcqi_OKT_)%Pp<31a?wU=g=;a%a0Q<GvP1ZEOsv-=ssCj9om)ZgG6Z?jBhRYOT<##Un-WOflb?ueDMnB_FK^eHWuiFSlK=4yxov<MgWOVC>$>}Dx<+NdlKapo|oU6bl#Snx1>EiDcv%^eL;RA<Ts`?Hafqy&HFT!ozD>~4}S;L`?I-O)#KAV#g!k<&8X7Dp>nE@hT|19JQ0dk@N^*P4Cf#Gc!a;L@xvdF`z!L9zZ|DU9WNC<ABsgQd7i($P)_sx-Fhz)jC&89cr@(pzEC;N@BTc}w{rU5{XCwIhAU`)&>srMD`<a^C!m$IADib&25vAI3RV=q!Kgo8(ev>{C4)c6-xc%zd>|I=RzNrwtf+uUSrHhCxF+6UG*Qk7QZyhIj{7UJ0Ana#NdX~$Su?nzfM7IQkrzYZP@*C)hOqakWE_NI@rsr}?9R&RLig&8lsOo#U>e{lceJAB$I2Oo-KN11GO=Jq&zF}&xStREyDj5oEd$|zKU#_X$WqH$M!L5@7<0#eS^no|9+mh%914ZQ6+Isf1uJ?!QPJ?l-n^n^j32vH)PLc!#!vU>BV~=BP&g8G7Z8g2D=Hu!50tY81l;RjBp8g95yAm~-0vzN6fS2YpeO*nSVjR(;#%}P-;h=?2qTfof;bW_ZyoRMf@oP$tSBH>)<)0?xuWOeWlh711|$OIgmL!*qW)0#?O@k_KEIcjcT|CJG`wuivh6=28hh|$nz-ScPNGwi!<TPN>UjCaCrYx=zp-_-mW95Fxqe;M`mQon%=JsL(3i_}v(Ps&b^UjWmH*c+{#X95n~tT>u|1Sydnm_J*J;!-wa4<%o^ItZ>PuCSRkRsxNn6u)klWF=_)ag{3UVvjg8I-lG#GL)ZB9NKK!YF$Q9tTU{b>l~5E@A6^Q074N`~)Bve3`_QOQEz#9UvBD<yONQY`f4GTkinP23ZQ<~S7d%*qKHI(01O850ZrK`Z;(Iu`mS7W0fKQ^jJQF|p8>%XG8QH*rt=nBzyx5BdIAvX~!CEcEmJuVkTbVlh96GF2?*2NMf@xlA_;eG~V@k2!uC8~5PfvzBi>)iQA?)TZRd#uXY~YvecXskW;=e8I?*cHA0m_{hkkr*G`M@@g7mVzjHX&#1me-szy)&i7LNjm-P&(REuG8Tv`-StX<1q|^o_qy0(A7A2z}EU8bFjQ+HwzEv{(Vo5$S@CqeM@leE4{OH(;vAU{QH|FJ(V%~<*ytW&Q7<03TD>sW+a<hmZH;b5YvxpNni`a0phzB=|7;v-jyPJit-7Ng8<`pGb@`aWqpIUBTf3er>q?`G(rI@#&G_UQ(!q;vVzIL<lwVQ>n-7I|VX5ni$3tzig_}b0F*KQWRcC+xcn}x5{yrLvazR<GdQ_Jn^<r{zA>E_(LVdmVNQ;OGi<HDL!%!PHNm<wx1F&Ea0VlJ!^#avhyin*{B6mwzzFXqCWU(AJhzL*PhdodU0a}}>B$&xR$Ecw)O`+Cji6Kyy1XG<|}Lup>yjfJn>EPU-|;cGVwU%OfO+Reh(ZWg|Fv+%W>g|FQ#eC=l8Yc~sDt9eC9mVBXQ$)}dv*DELd+{nBf74tTzd99I!uT3ocZekGwCKmBvVi6lA7I9)?5i=$h@nd2UOC}a^WnvLyCKmBlnpY@UiiaYW;z!AKRYSV=FD4fGs+&cA+nv`M`R>;T+9N-C&d8rU>a)Mt>pde+yW;Pi|6KP^BiB`3+Ijn%y~Y^%*qu64xArwMkFhnM_cJo|lhU(luDUcSwL!^fe^RnV$>;}5>JufSKP{<ml?=aFl8+3$LdjA*6tNUPI_}!bxLM@JCKfrinb&q>5o2x^aph(aOKukN(~a{n<7N>jZWgi8jq~x~W)TB!7JhfL@U@$Tf7QIABul=~vgA|C?Q5Rvx>@ALCKfrinb&q>;cGVwU%OfO+Reh(-8k=SHw$08S@^me=Y8#F;cGVwU%OfO+Reh(YF<&2C0}S+@~P$aHP3b3EOKKLiyYg`YrAn_O)2KWI#SGqwWF8|>xGNE)`(&*tP90lSPNX-HUAfLVa_k+!aQHhg}J?$3-h^(SCnMQ7h0BlYPo&Qb6q!!+}Ok-$2RlYZY+H5X5ni$3tzig__`bCeeGu9Yc~sDcjLUT-7I|VX5ni$3tzig_*%^?O0wh&ElWPN+`g9cOcjfK)y*Qm?aphBEPQQZ;dc{@7%;Jj2P5ZW!^9#^Oe|u?$ocp&v4|xTi?}keh%pn3cq`2-lq|(V5liu-<nrIoD)0WOk1ew^H}p=L${cxGv;FOdYaE?o{esT$p@-UUuiw#WqpUCM;QKc8935F-*1>a~c;2}$>&rT*zZ30n?#ucvoutr_^>sSDy{dBL`@FrX_Q?17zbd=r`@B3=|H$`wyHx#Ld|&rIW4ZTD?_GL&-_t7Nz0ocmUF_-NO&4RjxYEUvE`D?|ql*(=Z0O=a7Xv!Kd+@bg#{1V+3ICSk_j2CL?(zGk_q+82e%@eH_`PSm_l)<R@&5m6yqEJcPUYSAkXzawa!cDoZfSeSEo~3ErR^cNv_0gOwuju(_K;iJ9&$_DLvCq%$SrMe^G~_=J;$xRDRbJqEuE$^^L^4O^+~5DZ?~ns?bPJ|w&WvQvyZSPU)!4fh%Lp8Q70dJwq}21OEGL~_F1+x7HrLa&6dWLt=ae4(%9_O>>oR&G2W@!hjwnty{&mpt7Hu|$F?r^bn&K(F<o5gVo4W2x|q?$i7qyD@t}(Vo!>q9x}2Z6wMzK69KU<{`CF^U@Bd?dFXv~rH>KZu#(U3r?-}p^uf}^h`{nZPd&n(q54ol7A-A+W<d(LF+|u@tTiPCSOWQ+kX?w^mZ4bGn?IE|cJ>-_QxA~{s`|8;9(Por@Oi&cmhekt=#;ZQGIVB;Jc-4=#pfQkRsE+#6Rx}oJELk*wwxI(d52OQVAPuJRkmG3_4WjL7BIHCmh=$OPbO_`jG=X-Yo#{}>L+M}|M%8o}<Y6?4cA;Hq3gi@;OuNw@G!=3x9Zq}F-ZUL@I!&W}sFr3z&ZHSMg7%}MAdjLWKmnQ!IUBD66sBV#kHxDfY^aB<rys$BBrSkkK#j0q4E-4L$21=njHPDCW@>^32T}`U3mpdw##1X~D=mZt6DbRsr3@@MgxVq7>3CRhD0M(~P#Y{bj21&KrbVz|3N3+LLMOn2sk9VwDV+!lrqeRWWpolOm`Nu?o=iW11xL|okf+fpX!Wsl7UWrU23lQD=RuxF=YSgNLdXm8su5OP1bGo&&4(4gg#0D_92PXwC6JfUFJM6nT?Tm>T?`9a=?cgz=u%jarK=#XqRU}HJ6!{L4P6NfI_O%+Yw2oOu$ZocypDba3zpCgkT=lvuwW_O1bGwP2n&|c&5$?K3RrM5-2!<F{TddWMz=xUM*jsmgKmes9k0%SMR!8piC5>qhPxo|qTj=Ui)a<(D!K<2{E|8$JL%7`;1aqQ@?KgE3ofJkAnzj^7F<F1L*7q+fdyC5TFAAu1{PdHe}()jJpc=?rH3FNq6cBYb@T}2BlIvVxPcype3aI~f}7|u$j9h!u;6BT0`duZ92VR{PeDFKPr`!RXg%b5dK#_1lU{^;k)B7Z@1hNm8|Y=wJ@gvnYj|}JtauahO}zRutau0V9eM*6+)M94zDIAvg8S%0$PZ~FEV!ROf&7F%fCX#mbI8x>V_5K4`U>(Z`V1C4MBhMuLtnyzN9bRW|Du1wf=7wiI$Ynug2$*A`x`FC9)}fuAp5Y**pskgbI8qEU-mSt*aC73R>juCh5?WR*cR-0STqoFARE9YvP0Q+klV3Apvi1|$nEiJGCQ2@2)QF(O<~j6FvwwS2R4<>V7ox>!gglU*%53v$lX{qo5_x3dqVEXc4f2J(QF^ceb^rCD0U31g{)<Jv)OD8+YfR-Hi8|?=CUAUkonn<Sc*j;BP_(`v3eGVjI$_fU}?5L<o+zd8rgi7giNy0Yymrt9RPU%vp_9u9OO8>YGJKxJmh%1%CZhvlEpQVoxo0nH7DSj%$Bf|V9gR-Q`l1W6Iinp*HpHQodRo?;hN4)W<P~BC*zvQPGzUVnp1JjVyCg?u;w&eN3k>5nXu*zT(j9(>}*(b7OrF2IqYY!<{Vr<V&}5+V9mL>=CSkH1+eCPTn+3(_H$TsA+APt5xW?zzX;a?b{V?@7F>p_g<Zw2g#}mP%7U&(>#xPt0lE>^T#xGnb^}`hYi_``gx$n`4Qp<~wUph={tMRJjB6RYh208kZozdj`wd$OYkq_4RCXKtEv&f>*J<o_b_cAv9oHG`PWC%kb0@B|*zegNV9oDwox}df?t(Rc#C0yaoBava+>Pseb`SeAthoo*g=`hGVa+OB7lH1BB{r^$LHEP5`*2;x*0P6S$y!`jv32Zkux1^u>)E61aai*xt{d26>`7Sj7_OVx6YObN^8~J&*;DKpSo0LFTiD;(v#{pxxPHUdv*%#VdR(`$=h+Le=6PJVvlrP*u;xWvcd~!5mtoC6aQ&XW!ZyH~S8)B2y~<vLHLv2jo4wB7fHkk<x`(~V-a+f%#I=gO$3B1s@8P<Seat?E1s~&D3;G<b{}k6lps!%f=eX9fFWEm~&6l_yW#6#xV9htU9%KJv%=a|p)3AqpoB5uBd<ORP^7ZvS3;8VU>Eqkn_Z;MNu&2tmh3^H(7hunpzO8&OLB0fgw)Sn~dl~X&*t4x~ux|t82H3NmZ+qWskgvg>p}rk`Z$Q2Qdv@{-^SuN44(u7`tM<JI`5x@6_U-EX0P+La)(bhoHjvw}!HiLaCO}SL+p^x&iv~juW<ywvM$sh5N$g<Om;ap!$RTVftD?Td<xsX0+mfn?%bnP8wl!@@Tn=Y7Y+KrzxU6BjGyeB1xZIuX#fH*$#N}RWU$zqsB`)`6BiV4;iMSle0<4CH6PE!NX1h}jaT#VYwioSAT*lZawlD2PT#jOOY$WYVT-LEM%ugeU%Q0*$n?*-cGh{PsVnOoLSje&LKsJX$bP(i0EW_qeoDP9JgtfB>&86cZk7pCu{*<Q0kc-)2?5A`j{TTAc?3e6JnnM}L47;2iL(Az>$V=HmHkZz(D<Q9B$Fl}XQ5$3%Tf}}w=hLqsf5on5r_-tQ3&>xvOW1E{CEW{oFI&y-pfl-m$jjLp_D4FGu7SLU{gs_fzoQ2rA7EFq3+PYu2;?K|I`$0RN}Z6M>}~b}-9c+0*Rc25Z|OPO2)U8{g}p?t&?k_eun*bq=pXbE<VWlQb~pWj9)x_5J<MLASLrjz&)6sIReGJifc%1e#$Knl=xfNY*%$0BdY8V1{FZ&q-lg~Hd&uwEx9olTh<v{HaedD|qED%}?;~73->38i^@Hr^>+So3zNY?={eAs>U(>fV0CIq@zwcZ6o(4h=^bPQRPd+vXa*%JJ&&PVRA&^6SgM7VNKehwp4!$A2eyl&+8FFXe4!&pU@AMXX7T3GDyCoa$>yK+^-`41Z_u1Cyg&N<MY%8`4<SxG9zK5^R{hfz{&z@!J_}=%v><si<m%QM!BeZ<k=^u60eZ3}`Ja(p*8yny3+`Z3VlA+LaEk`E4=;-g=Z>pBJeC27U-u1^%(Q>bSo^;wj?4`+C=K6<h@oLwzD(3YjcYL?24JzjCKVrc9UACy0_XF1#eWGICpS)htw<;d?+Agbk`}^<viIyJ;Zn2v8!^&4a*7C5|u3N?XbNOIB^9>UB3;#VL9YcRK*I)YX2U<qGb-dnb!}W~z*YWm${`C7==K8!J#Iq{q_457{ZBQ}a?{UB6ZBa7s2d*#rM8&*6dA*`<mHgX>oc-&N!;Z6$n^<qp`swM({hz!qndeT<vd+n=J?u$+BKDV;onNFAxw@^he*9v4_M4B_>GYwK%<HVy>B~BJ*2+KI=_<49KH6aA+tBH<#md{F)ybD*N#!KnI{EfkQhO|Sdt{xwU6#Tw<^6pB@G_IS`?6o4lg#T_27h(w==>$?$iC3|OQ)~XarsVp-{lwCE}ie(<#h9%><gW~PRHdV<$agG-2L3mUqrhg8yZeK(+>C=LWA%%kOttZKeDjC)XO>D8SZ>{kaNE;UhjZ^i4LOOXit3YgPdq21(5ZGob!@|b2>7H#zNyDe4l?e<lG;F*CX-oLF7Zew>RY8v<GcQ{iqhQ7CBcR<a_%;?uVRfbJ_w~)#kWHAoJUb!jNGKBJ<l8S=H9KBD4+iz5OBgrx*=JzL$hdBCp(@b|eeZqS46whS504adZGxBi|bjIi3!rU5O#%+ZERY!n&4});J|&T}w)9rIN9(C8af2$ynEt(%P+LtZPXr2T(HBwWO3wC>eQ3Qp!n`%=M+UQpvntY0XtKZ@;v5E1CC$lmjT4_otLgC|Ru6`87_-V!h6<aY`2Jb$*RgayjdGevMPISg-SIoRY<QozF>>EY@rBtct~YE!v>sa@KLtCn^@}wdh+V7v>^)9q*Lpe0lzq*JZ7aG|#V=^`$w#PN%Qak>>xT?!GkVCtY?~(t4-Vk>>fNtS`;^bvk{Wjx_(T*4>xpe^ozQQa`(M49noJPQ^N2q$BsaPG9zgPG8n>`KVK|cDwt(Q?Yhyb#y*bw8xU#<Ia(abX-2_RIJ^q{&DAWmd;;%9Uq1-e&#V0Yv4Bc+6wC>KR@Y%uiQF5%=zv%&iy`kJrw^I*71F@>h6d2HG;1=R@D8mk{*Dsart$ee>dXXKLD@y!@v4<yf5;Hk&q*i9mwnW0Ib^~$Pn^{fygLgkTI<4+amWE1vv^C#CFIp>LBZoDah;i&d5W?LXJfqp<Bm~udC`DwDQ5^6_-C}893>I9sTt;JZ|Eo2kzwSpD0tqNe}Gk%VjD!S&Do9PN4bcUhW>2d%tw~#toK%lOEX7e{bqvO`P<=ohv7#>O`3uPI_QRUoKO@$x_@CKj!$kv2~8~z37#HNt*c8!><~>$L?1f`Jvs@b#K3Yf{{Nw;-$LR&KPIp7q;*x&wFrZBY*qV2}wRrnE2`auP@1O+_AQ+OdVe`@2#Y0n~v9Q&MaZ0j;~)*Wr@Dh@!qqyvP7So_}ru4GBPi7^4q;F6Z5v+JZ3v1a~t=*d{-m$zWT1;2qW`8U%oM5WbV6C%ws^5sbd~XqHQ|nF)3`+F^_H0S32fnMD)3e>#Aa1<H*Ef9GO^*BNK~pWMVOnOf1HciN!cFu^2}t7URgoVjP)Rj3X0^aa4+h?{qB2k%`4PGO-v(CKlt!#9|zoSd1eRi*aOPF^)_u#*vA|I5M$&9J!hQyYqy_b{6|0)4IIycXRAN5!uE1#X6sD7P0wNtY56d@A2;y>lf?rvUwfF`ucUbpl{Sks&oqXow_VlU4{Ejn=MtF3-=w{EtTzs`%WKPsy-~-*XJa8ouo-8Uzb&^uWYkbtgp1)D%Mx_p;fG}&&LY-Mx9QTPT_u6Y*?BYv!ocaG_h()v1(~z-jZTIsqlp@`NG!tOEtbM597=7Fup7g<ID0ezAO*p%knV3EDz($@-V(E597=7Fup7g<ID0ezAO*p%knV3EDz($@-V(E597=7Fup7g<ID0ezAO*p%knV3EDz($D*PPs1Uk_9N#Z2F_NTb>E>RF)`%x{v_&L=cv@2EPOZA>tKj(9AeE2%hDIxAWTkAYkExilY&(TRb-`&HxKLD?T_}51l&>?gfz7D79_~JjAdlb#4x%iq#X?!i9<D8$ZJ>L20*~R!ek(S|$|J*D8dDpY?buLP|0A=tJj&hz&J5L?&=r40L&vtaCJKsIdxqlj7&&9tNpeHt?NsyChBK4xaGzD@B9qPQlHVtwbO{UFhOPUEelcv%Zv^5<Gc_huCt!NuM8uDnGMcdL~ngcn9j-l;nd-@UNkLXw$N;^_LWId&v_tzRB8>xYY(=OBm*+lcHhIXfgkPGR@v>WY3t&pwM?3^^VLAFuGdGBx$<RZ$_2nx^=$R*T4ehSk`kSEaz&bx{~f&2+Ar5GjXRLE25WEw@I>2%1`>8DhOusIX*Oj_=|^LP&AIdqnDc6lD;dGs?HPmB(RJebZW@i!dvIjWYW{eqUI{eqUI{eqUI{eqUI{eqUI{eqUI{eqUI{eqUI{eqUI{eqUI{eqG6`Kp$s{eqUI{eqUI{eqUI{eqUI{eqUI{eqUI{eqUI{eqUI{eqUI{eqUIy@QgmXSbyDE-g#vU0RmTyR<BwcWGHV@6xh#-lb*fyi3c{d6$-@^DZq*=UrNs&bzcMop%{o_)f>td6$-@^DZq*=UrNs&bzcMop)(jI`7i5bl#<9>AXwJ(s`GbrSmQ=yT_56d-mx)`}CfDde1(+XP@4)PybKcr;GP=9=WWyZDPJAKK;}XBlESjwstQg^EG<q=@BFIwf?lvl1An^L)H3mM&`LkDdsthC{xEg7ZPpLG0&-ljXLJJndmDW^Bhm~xrq<RzR_u7UZ(%sdyUN7_LD<@Wn^ySNmnd4GViPFI?_hY<$+U;oXZ2v%ws^5sbd~XqHQ|nF)3`+F^_H0S32fnMD)3e#d|v3cP19&$i!kCnOKY?6N_<VVlj?PEXI+E#W*st7)K@+<H*Ef9GO^*qf#t<r(-dWOf1HciN!cFu^2}t7URgoVjP)Rj3X0^ab#jKj!Z1Zk%`^o$jv?bub%x^&;F}t|JAeq>e+w&C+@$*S$#hD(6W>VYFWwywJha<T9)!aElYWzmZdyU%TgYwWhoETvXlpES;_;oEaibl&gUUomhwO?OL?G{r94o}QXZ&fDG$`Llm}{A$^*45<$+q3@<1(1d7zf1oKVT)tUkYY*0OYtp=IeDL(9@RhL)vs3@uCN7+RLjF|;h5V`y1A$I!BLj-h4g97D^}Ifjvi?{qAkV`y1A$I!BLj-h4g97D^}Ifj;{a||s@=NMX+&M~wsonvTOI>*qmdmOpBXaCi+|LWO)_3XcT_Fp~wum8mT*Yb@6?LjO1T31|twrya`1KU;WcdfgzwfDUSwmh&sal<!BQKp714{Yb&-^-P$VXG9o{r=^&Mr+SyFL#>eUP(tg-b<8YdniZLWkV-fqCG;#)E-kgwyqpTn^6@c|67S$(zdi6<aV?*zOw~w1-TXVa{l)6U`YPg0DRPs20`+lUhYi;X$b#&i`1VkxbO2-kFHxcdd=t0S_U5NfgSyo6P_^fXb-&Vi@jb<iZV4k+5<cKa+wMqU5a~t-`V{8&bhOsORc)9S(b@!Y`xg(e8bF-9QaG?_`0KwT($leT|XbEW3Ipch94Q3*L(Iq=NXx|ziNHGk=NgFS(m<!Z-4Cau6lKReBBjY?bk8a7yY1PUa#m+6;Hc+m@WKbV&NAP3%{6H_{GG+FD4d#F|qKAiG^QGEc{|(;TIDNznEC|i;CU3s4l0Kb7NipEa&06TwTsvO62p#{725mbh(zC9~$zyq*RWj$=NKaJ(eaPvn0DLja`=1KS~|h7rLBZ<1gETzibcwvOW0A_TVqugTHJK{<1yz%l6<e+k?Ms5B{<}_)GfS3NOD4=KjsE+;4kLpgm}BeAR0HZqk9!n1Juge>Z7@^LLXbAam<QdqVC>yE~tku@B@v&fiU{%KzP@eVyOW3P1*Eg!B7ZVaPD~k=t!cF~}H&kl78U1Z2YbyGh&AXvont%K7~)3(}%G+KGne|Nh|^8s_}nq+z(m(k`%nH^|-SAo9B2d098TtiN8@@lyGKm%PGDeo|`P^t%3fUB^r11Eul`tPz&9u4!3XAGIv4vs#wcYb{IbzLur@LCaDeqGf5V)UveBYFS#ZwJfdsT9*By;xgvXlJl^a`MivE!MMJ7S*JX%cgA_x>wI3ux?o&iysT3m^OKT!j+cC?jJ(U3zj?_6J?4`o^BgbvQW<%dF@GzS2maq%$2Z5S-51xsSkd`9UWIGq4_L={!m2&g`OK^xoppRiT$XknUpZkHoByr9<r`163~YH|M}OsnpW6nuJg{?~DazEa<$)c2xl9FHrMTxj$9$gi=(=^QW?$g5Hk{aQ8F;h@cJ!~fe2Hz~(H?l!@a4bhDpSLwJ+PxMm#N^<rMM@4%<*$$>%ThRn|il1hv<0k*^iZEq0h&xj)lI7x&8(Becn~3in)F%7W#6TZWj6`?uj3B{GhLrQamUbeO{7<e!l;eEc8vx^`&@FGS@G~LSHV^%|hSAJ@Hd&{hCyFeBHyzrGvh+bUgFPgB)&Y{#MJk&JH*{al<!SUi0|Y4u5{$*IMRl2j@%9{z}US_nG1F+i!fS<=h#<!^uG_^$h)0(z8nD>z&jFC8PbTC0mq?epoH_iIUNutEIkGGW@by@{y8-{+X-3*RrU0{S7om$D;kG9LBUP`r-D+^ep=G%w2q1=0VB%_&Plc|K^`nvWSy>8<Z^KEpLmGMcn55M9Cul^L?vi)GLiCHP3wV0f*<^|BaS!oqb20h+7@6dHh0$GkrhTvKZI5fA@)&59#x?(^p5_^|6-4I9fSD&(L2bJ*#99xA`_G8SP&!*`j3h!)mEdl#KpdE%mLE;TLI4safbBawm@gHH&(A-0E1g|NaYmX<78ct`~2nWznCH$9rp8jH4S{^(_3Ge^$vNPV#L~vWU05ElL(~o9`1Pi}=s?t&(}YRqJ2tTC-Hl$0KL4W~rEuYtCZLQZb(&IEyt)#eAOOEY>U)^ZAOiShG}|JKKM)Yt2$IpFgE%mCWa1sSQfz^SNY;lKHwI^@)=C`XcqMl6l-pK2oyK7i*S^MZIFpQn6^iShG|t`a!H&Di-}I)+`nCal~1ySt=I(6>FA?MVyE=OT{AI#G0jI5w~K^Qn84Cv1X~5uTupdshN*Q&SK3{F(20=ZgtG(2hL*6Qn47<V$D)9pRYKJHA}@}9Emkc#eDvho>j7lTd`)Tn9t{uElTF=g48EU=Ie{pw@T*gl;k5N3w^O>saVu2)+`l^_KP)3#iAd?nx$gVpJL5Yu^2~U%~G-OuUNBGEaF70St=IsCe|z!i?|hQmWoCEi#1Ed^8W19$Cf$&W^U-6l(^{U$w!{n?EL%fhihb=qMw@`KJ-xM-?!KAXvzAr4!$RJEm>dI!84utIxSgW))DPPTP#`MrIQpovc677wAEdXd|$NH-5&YA_@3J?`M#*b-9Peu(N=dq%l9Sj)Rfby(~;U^%laC-Y*}B^Kenu|>1SKk*Xc<9vNe9UCBNI6__3w<u{CjMOL1sx;@OtsSvM{^bz`T;U;lCb>X{G!Gv-6fgTE{f{<1vy%ktna%Y(lx5B{<|_{;L(FUy0!ED!#&Jow8h!(XQP(DE=JS{~*@%fozVd6*9^5A&hrVLr4x%!ihT`Oxw(A6g#fL(9W_*yFGNOn>#vhyUm2!(MbK_)wZi7t*uz0^|$y3u5$hx)}0e>g{|w#Y>Pc(euu4iA{!_j3<5p&3{1tgD#=X=$CXE<Ym;4Ceh*a3gj#FqVqdtQz56~iA$il0dfOfPJQW8x)SnA>Q7T>I=u$@8olg%_UjDD8F=DyXub~lI$cFobOl`lc?}JqX><g=3Hc_y>iqWFEXY}S;wosq1^E_TOIy;_bRFb%G>~S}QS=VvJM>1;XH{Ga&37T+rR!;H`W4*>c_R&?Bk3602)U8oc7D!k4&)p>aXmEOhkT!IqHXC0S^>F&wxii}EPVj^0lf!p{+Snpam|6&`}7gyNAznNLO0VbkhjoKnoBAA81iHK(D}UDddPY_@oQ*)3i&DhhIXL;qFW(vrJZOVHPB~}pV24K=AWIhBd&UAeM(<IenBf~XS$7k3;A0bPHCD?UqXIKpF^8}zQ!<IjnMjnzJ~mo?x1SAo$iFZlWJ%I{g}Ri{D!`Aek!aPvKdd@0nKkAzop;PuJk+l1LPlQcjvQ6zJvUZ{^@)Ya0W7iCw>pj?;*dZyJ!#kBmD{TPqa5Jq~nRPg}D9&?R_W<nZ*-#LDR?X!gUYrMR(IG$W>HJt<+ANu~uBf_Ms8ffoD4K#68gL4c*>sHSJ4(CL7YG{iux=Q(xAGs}~zVemViqoPZ}*L$e=r`>}gzBz4k#koQrL7SV}R#TMb}!~7JYrFdp3p12p9{h`~Rt)T$@g&u%>fFiVnmeH1M39ikV{MjOFpg91#1K3&$)BW@y<bxEWljs!Mnw^Ae3l?=ge<X_QC$tut1ED*RJw$Q(D?JSPFpZ*<>8G>}I~mtjEa7}cNdniY^bj-$L3a>aNBh$w^eE(`R7a=LavID|!?i6N?R<{OXk4e$I%p1o?hy7ECFyVUIOO9rhR&d~XnS@BuI-rReAbDD>r8qKnma&u2lgZ#Ku^$9kWbM#I-7n*JF>HJ4P|4U&qEoD>l}I#nma>xXZCkGke;SzAfKV}bS|Aw!`QjFc4GWD1192`iFo4g(0ms1S<ERDXgys7d6DyZHwV*mkk8R@#(#GSk67z(IK?us<%Js?*Bbe;DMPKRK6>8B*S2qNEgkfMksn<2N^<+tzccc*yRS(eb7Ai>Ccbs*Zpl5*+}y}~o}Rd&%E-{~l%7>G>g|-;pk%baQ?f<L=m%Ts6D6ZRZK-dS%>66*NXy*6%QqfxV#^EjGEFREz{Da3Oe|u+#3BYvEMmaKA_hz>V!*^A223nsz{Da3Oe|u+#3BYv{6Fw>O;$diOPX|e9wl<CV*P>+&&NcLChN;O{QDwrll5gC{+!6$WPMpj-V4e4Ivt*`7IM`holdEoPE|SbeV#w7+9TiRdAQ0h`99C*RsAF1&+m(p3V+$|v#$T4pH;Ix#D?u5Hf#^EVS9)T+e2*F9%94x5F56K*swjshV3CXY!9(vdx#BN7aRK!-|_g7A<hEx-Ao9tIP;xK6t6h*T?qfp3eJ3oF&eKp^WB4mSDg9IU@Ts7=2`zic*U7#^gILN%(HdAv*OG%alUKf%(HC1Bbw#p&-*yLm#NrojYP)DaBYTN7yrGI-njZ<mlQ^(*cVrS?0{m(0;_Nh!0u)gGQ2Hu4aCl+4%yq*xCUWYG6tF1wz!61cQOtc+IF~xVmC1Xnb!`ucEV2K5bV%)#x)$ffWxr+s>W4=4F7QKtain<JF@rb*fs5eYcFK+M_@;^H?Dn=p&#XZI^urF<*L^2y87;64<t97_?czkIuGpVheEHJxXuHwUi10eU1e&x&I3F8a+wOQE5$uOe{25v+m#bi_TIBENM7^dTS*h|{O*~_rR{GT*}CG?<RhbBHS+KWPE5Z4-U~*4?r)0`15X>7>p#=)Q6uwuzq)&^k$L+ko_e2=c|Yvl=PyQ%{Oyu1eI0Kz?CP$1b-ZTgbzSY(@f(j{-_;K~=K7*Pb<FD(e$g>+zwobyEh$d4EX9eIr8v>D6en7i;zY|*oM>5!6D><|qGc&gv@FGmmZdn+vJ@v;mf}RqQk-a6iW4o%aiU^A2X#C+A^Gb;ORYS2=D2tsE8NH4YSaMxo#$tC(<$61!oN0Nchf1{Cqj8PuiLFtxZlN{nsRKDPQE>MvA)tSyI8-QPEzO;^z}O2K2<q|`%Zf-ReK8e9lI=*UHSV-lTN-It5{#z9;;YiX_r;3uh)^{$MO(AmWTMUJj9RXA$}|m@nd<2AIn4hSRUfX@(@3khxoBP#E<16ek>31V|j=l%R~G~zlUD#=Zxz<TfFe8;&ZjXldk)m@xpJZPbm5f@%^1U{1e0Z@2!U*L(cA`5B5fz;R-vyx1NAZU|&*&z0zn%{(I<KVlOfVlK&n$|Go8bko@=1w{i9&+c>|6J{WtFgCP&bZi(-j4u#~qCI0!~lOZQNyOUk8Ga8O-iu3v4Ga+YUcfvm({76Xt`Q!Za!H<DF#@Snqq+=nErK7ROBWI`Qr#W4D=6)}|-f3dKZcaP$O(XO5*LUH&M&|4ID=&X!WS$SaH}xwcbNw&Zd~al4@5ar0*(T=gU$c8}BlCWk@tT?Wx+(N^%-3I0ua5aTF50hSo)3tA&@tB+{i$PKukeeGdHaQbHEc<7qGc&gv@FGmmZdn+vJ@v;mf}RqQk-a6iW4nMaiV1@PP8n=iI$}}(XtdLT9)EO%Tk<ZS&kDG_vD#9d1g<Z*^_7fZ{?Z)4b7Wq&j', 'agriculture-fixed-open-headgate-handling-frame-01': 'c-rlpeUKbSb->$_EL*aXjVyoRukjjVZ10|Cx_iDP-wu*231itZ76B71uJ&&C?l#`rJ$Cmbgb)}T9KuH`{DHwA2^EtfRe^$h5XVKKTS#FbHY6bxuoL2nse(V8G6Zl^6;qW|UiWP8_3cgf%v>Lb|5$I`=y$Vkx?jKd`n~Sn_02Tia$o~O=ntMiXww}Cz3Ir|+fNoMoldP=*mbfnQ)|}Rm2RtD*j2c7w%uyBI@Sz4V(o3zn$=p{x@G5K>lhs)W7IDc3&(2hPQBFxVLWCRP8AECDQKXu%kERBu<IQs3(d+L+$$X6?-dKpR+YbjgQKU8F8zA4P<wZ`UFk42rdo6Jt!Ay+ooKfj?Af=?!oL>0-R!VFYZho@O}C+8YqD0E+ig{*x(k(t)taw0>&+RfU7M@an;ok%**aFU8m;42ceY*YKr2<I<{Ti`vacF%et)xiN2}efH1@Syoepc(nXtzk4<1;5-JEpYoH397Ms&kzy5ZlP-AKA_S?qS8{_a}U>eQ<>tJ7VWv{)xhhwg06s@6O6jminDQ3JJ?dZx>J<}JLj(yTUWchrxyy4kET&HI&X0xGvz$Mf~3^*gOPH$<aWnYOwuuvM$swdPx$?vfU6k`}c}b*9p-?Ty=l$XO?4ye!J#byCJpR|c<}Wr8fqq*~^1Q>fCe)H@<zXL-;8H)dN4wQjdow3;oLJ)jS0+G@kpnYxE5I9Hnj*?MQrnrc+)b4%KV3EJJsd$==hC64PX>am-RTDNA+v|9^ML8{PubEe*1fawHtyK_&yYPA-+TyZwJU`n?ZW@bzCP?9P$H7OwuW$Q!G%t7Af5op6%UtJuXE;yGiERXRX@2OASGuf)NtGg}8FZHff=~_@Rp_PWUFyF4v%yyY0yVi801x}o5v^pXqtyB;XD|o!tz7;yy%R0!A0M<c8qF3>iU`47^5x*j==;~F>m|XkaLanQGVLfNHrg?YGO1lkOH|ob~oh~GeIJGckc$t>e7|Qf<&AkIsUglzBtb(srVZE#ns8t~Aq(Z1t0k4-Mu&q{Mog9H3wF)FtQC(;>O0eUZ>CVP;7V2xmnupb9t$mDj$kwEw<~;0(DpOOn4(yUD^O6EX`S-V&<Pm5Hs%V4lDgtj^)F4_loH63BiyBm;23|jFxLP%`TI0C10<1TWLz*oehqY0cEeK~J^IFZ?)IFuiN}DeLceAzETr1WO^lH}UDvi<<tO#LuV}SzGt@d1{IaM28gW;i+`nI@_+oAEjmG&WM+Ib~u>!)cOPyMOcdZXH|HDSMR7o8$5k|Hg-MX%@=gJM{OMINlJVD$p41E{`G-Jr5SW{1oQnGG@v%xsuj5Z4e>;7>3T_Ky}NBk+@qiFy?jsm!$NQwxpmLc3Pt1}L!rDb4nm*(H%ZN<4d%Y^P8x@U{9xwcf5xb>oAL(%a!SPefA_$Lbx}kWRFkjT41k-S$GQSZG0}sy8R9mF~hENVA)Lo6o{q?_ri}Sd(mN*oljLZMW4u-r~W$v<_uU&rXr=XKQ??AW|RP<e|>j3$XR&J7l(<5TjsjgLG&eufwc}-3)t>4(QzG2R0MTd2R3>D0lMiLZw=n??V2(yRgfet~5HZH@G_voKC$9wn)6+YESS(n&oevm}=BI6V+O?1sj89Z^0C;H~Fo*3;W)_@6i4ucNf_GPK7Oncry+T*c~?DN|oQC((e;<&|Uoefm`m{e{=l!v3l+J1Z=!vP*Sh&;N2cQ#bU7^fe`mg`<BDtbFs5J5SIxEm^t{ZU56+6!Be%hFxjZFR8SRu?KgEZxap2cy$P`#KU^%#PquHXfma*#sXN*Bpb3eFMcyRri}tk|t@Z)1HakFjhdt&5A^*?!95-+%F4|)_u=#(E6Jk5WA-iSAQiM`MgV2U}XDaqP5zT>|6UzmG?Sm8)xwcSXNyzu(9vu>dzHhsy*tAm*klU!g<K)B2IYLb0;ZVoN1iLVA;hxJbBvzJs#D%ekszK3sP=OZ&Ug!sGL7OltuWvQqak1<AG-Xt`Er7$=8+;ku$vGzC_s8UW0r4RNF|Wm=aXi;0H1ydpo#i?a#RwC}6U6NWt{2iEaLFkil#oi7ADQaUC1F(U`dppO=lH2gx7)5y!r1xH?l^qpmbct;_;#+t?T7EYZO<WCAi^}MH>>q2CWDtI0tlTt%8Z)n)G>3<WT|Ir)-%pIW_PJ)&$Q=!WA>MN4)XN8;>0j>kD=sWTket_R4n!BsQO%aKA5>{cG58Dn=I>_uBvaGqi@N_j%VCA&NXhy%T8cybDV43lE3jP{GD`^m$`Gcw;FVgm&G?p>3sOeE_<I;>eJ0Lr-o1FvUll8UHbXD96oEy-f19p8Y(-*>7C{nDUqrJaaP}HuIWRhv_XhTr+G#yg%NS{bh`XJD|?4h5RqI#wEXlcdxug0k#MyglI$H)DR`)}x(;&%4wV9jlGS#Y!=zLS8tSgL!#pOHf`;Y_nxs>v?A=PCLqmgZ`8i7VWttQ~uCwZHan8}YQW&|!pxd0Im4eC56--ITKiRvLLdsnhQf`pD-yCztl@==AvW1H04EGEBpZL(O)s7pTT$rA&wciSxe!hVjoNm44#C(m#3aijlP}#fj`e3f|ZoYY=u1EQ1I)E*<1KTUMQw!rwaS&o3?$M$%W(O|YyAjxx!?u$jBF)v=u~f+(b1`9WVi&`nw%-EA@va^AhM^7HLbw-(?y_wnG|}a{72djkUwq6gkHJYFgYI#h^f(zj&Pq-H@gw{89NKf|iUx>@4PgfqA1wF;hhW3d$!kMs!R~MM?GSseL-U)EnwijD<0vX64j^9`l@iUU8--_P1b>agAg>V;;vl~b0y7(g`p12|WCNFQ8~89-Cx}xA#x7Ieb%=*OI}F)O@c6BO`qaUWGcbTXM#9*J4g~`ehn;ATIX-2B#nca7mtf2qaQH1ZfcG3iNLntj(?_6v-qB|hhv2ky;^3@CgeV}CP=0VpV0=NyPt<&V%I2`i;088fMu=}=CnVIhLn6l!^?4kDZ6IQ(P5C)v|L~Cpfe%dtK5L_Y&k1dx&>%G_6GKB%b3?i&hIGc<AT}f>5T%~y<TfNU0kfI?haoL_w(G9Kj-H_%{p?ec!ffLQ=w5(b$EG=hiAnQ08F(HITsL(6HHxLc&<3G_4f4f7k`2}(46tEd!cLyd%xi{Yhn|mJ%BF%BgaHXW>IW24+vkbZg|~gk)Rbb|@jS@{G^DW&vF&<L(0FDB83z(Gb_oT4vX4`2$j~0P0}oy}OfvvBGypNqCzxif@GPGMap8rF=Z7}`ti$%>a*m-wV;DTIdCNW#af4+ge%KK<tLO<&Xb0{ZE|0w&>l)C9=@!BW38uNn3}(Y|3s9;30M;|B8?tXW<RFKmDe>8-a>Jjau^AG7Q0F;;OKj{fFBU-<X9>r5d}fuTPrbl;#O;5mNkf*CoV1aLW+Nx|8jQS@tarY#mlEx#)!lF(NN|oohoveX9kE@<p}8Y~e-z4>uK^*B?ZKjVjUs>$Lo3iVwt_Yqvf5!4(O{VNh?i$3V28$=H>ilA>#=20ym1LV&%+Lh_c8&`V-WSQhyclDsUB7Z?7aZ0Dy$#a_ZjTI(QF^8DXg44zOCn`!C=@B!%8L12!@G}1Z!*r7*+pk2_c0H@50i`&25H~q805(3=<=@*Vq!JL}%tSL}E;7hhdl_X`UQO0-ol52iAPBg2_24AT_v@o6+^{fO@XCHgkd+CP+%x)&$xqk<kdNnGw`5K~isR?Vy_wS<R4tJ{TrQnlC}dCsyoi%Z6<fD|JB_mo;$`$oH16dPl%F6tIvcuuFxl6Kf$pH1l0-Q|kEvx5COMw4*Rgj;?KF1qU|W{E!a9#DfJw;N`V~Ge!uv0z?LEO4-gMzZG1=-00@YjU+z21poW-haPz%fz1cLh7RozEXPm4*B}mD!_??f0}JGff|V9nn;0-mimsRA$kCxeoYSb!G-T&Qp}lPL3;Hj=BhP}Q6NVLEWQ7*`-+{HMN3iRqTEI6uXK@4La~3zpaovjZf;>iq8WO~hLtTO?=eu-GZ0H#t)_JS=5CK$LYC`^;mw(1Pd7@i8#Qz5mcDfP7Hx5rv^FK}i?{_Qh8HO+?J-nn&`m_8-)~DIH<%eD0TmCS~)3rwf1I0t)89eP^o(Wd{xXV7|S^eX%OfvDAoyTc`M~5CKzGv__!8DKZ!;e#TCZ9QIR`gDZXEJsd6KtS7EO|Tw<vrrr2Fm-nf_BB@fmzrDp^FV34+F;}>Kxk(Ol;>kE;TWp15qCsL=L2U9~&e~hqz`5j|65Jk2+>4k5Z$Y=TI*QjGhmDBm24Br3TNtu95xRfEwA)WB+5B$@A1PvY+SMM)vby$7%Asj{_t7`L1VVKR<Ad>=!uH$bJDOW=j?y8`%$*@J99vacE?}5GIh(^MQ|z)@+Vvw&tTo%Vli)M)d<bwo(1S4l$}97|ds6KPND%9~e7E^#hh}p2_+HW8Y}`g^8Cdf3J8R!p}BX`eN!Et-oN`ZnXY_8!OjegFSbDzrCyhm@lV}p0cd@S%mi9ayz<o)8^haKYV%ojX(NGq~dpe<%Mz@3;8>rc%PDmypEat{a<@iS+tqNOg@c;yxit63wa%*!GHJm`QG00f93yH$V3S;y$tR2GPDyV_o<c9=@VtpXGJ?_ptI0cxNb$8(5uk-=pwjYgf4)0Hlp+3dLB9#ZARPCg>bzPZ9yB*Hnan-JJ8waOmq&q7_JwiSMxZ0>$dMk!goo`{F25(UidnRg}jcL{FlG|gF%}~%;eKp$jfaGvyj*EC=T^;DCL=+ilscGWGU|{S;~7#mhy~}r97i#Deoy+%6m#4#ZP+t^yhw0#ZrDyvXrlsEafXDOZh>`Qhrdfl&_R5<trtR;zu7p=Wckq{P05$MStG@aHQiu`p-{AA47Wn=HEORefirDX!)`I4@OU1`5`Sc`LA~G*D~w(CpX=vWv2hvpZb87AKdrIKwiajCm$X3tKv`m^wEL-DrWM+4k~8-3VSB;`FCxJgkN+l{Gwyw7aa?~=veqg$HFf<7JkvO@QaRxUvw<|qGRC~9m{@6Vm8Ox_kFN@#lho(7h_&NPnYf^^k19Y9{jA3S-Ou9$o5#f!!k?v2fV0gr>B$Y>(g5<ze1)gWR~RBGEDcRc9!mQeWE0N`uEE^nSMLba`{AkqUG{x8OdK!27g5v{1s*JSCqkDQ3iiS8T=Jx@K=<<Ur`2sMH&1RW$@QPW&^qgS@607y#`(v!~Sds?8>&m>m1mrvAx;`cv<}29sK^;@cV1v-wo&>dL6nRUPZJMUKqLX3eawNmC+t}-3$^3;eGb5%kS@j-*>{l2Vv*95nTt@>(I5ZgWQa6fa?wD^{}hlf=X~Lp&Mau`6}eV)j?yhn>-&;xKd=p-tq$E!_`NG?=VBShRB2c=OySSxZZ?zp-a)_=nZgv0~$w{p{vk7xb8y{x)K%80k|GOd(qV}{@23wwP-)u{qJ95_AUR}FYb$UysgwO<JtSQJh5%IeD)VUsO2kuyIP)}en87i{z>b@T4wz|QvE$GGySjmp`K5?@W4P`#ozm%j}H1(@h|`B;{*Lw%;bd~RLuGn_DteWH-9<si;jg~bS(U$W8oJa3%}@C_(jLUFFF=}(XsH0j)h-zEc~Kl*)K_)BY&pm;Vk()M_tg?mn?NEW4+Vn;jH;QM_tg?mn?NE<N73Zos(s~lw;kcUB6{n2WDJPrml0cte0}EyR_@Kv~}Psua0kps(lvx+z1t&)$uLxQ(8qGzYMDOrSLNj6`j@b%i-q@+B&}Di{FYwy;kw#FFhHFnxf+8zx0hr)FTz&6@DWUbxp-gUerewvwlULRWZ|F)N2)YX8&#=ui{(2@YJAR6@Rbr^gw?VGkIYL6|;VYJ(HN#2;mnU3%}@C_(jLUFFF=}(XsH0j)h-zEc~Kl;TIhXzvx)_MaQyVl6X|dM|FHu$A5iweD)I`FN<})j>UdK$70{1W3hkHvDgRcSnQ{CEcRtO7W)Mqi+zWV#r{RdVjrYqv7b`$lh!{D{Gwyw7aa?~=veqg$HFf<7JkvO@QaRxUvw<|qGRC~9SgtcSoTX2kIs`v=gFh<<X_);GRuu(eXC=!PS&wlZ|hjB+jT6~|2h`?2px<4h>pcNS;u0%tz)rn*Rfdt>sag~RLpXt@QaRxUvw<|qGRC~9SgtcSolT9!Y?`&e$lb;i;jg~bS(U$W7#iBJgQ%#`ZcOwzrOl)%@4Ok<6A$)zr&#7moMECol}1>I`VJ#D|vkDS<%*)J{i6F=l3c3u5eTI?6*D{{p=w%cV^ER$g8;d7ynll{i^t~o&Q@F`m319&wu_?(G`^kl+5~l*VUhntlNH9$xQ#p4t+Yh@3U%Vb`bI^X7&{QsyOz`Gts-o-=yT&FF%O>^ofH?j{Wle=&|SbD>?Sd_oL^Cnq$Aj@+yw~68Ed(*e|jEDvtf~OtkxN4=FkJ%d=7R@a;;D{qk&d=E1{Cj{OqLt2p*c+^>q+92<MN+8cZM$K~xX4}bFCFOFY+{+!^`z>BiX4>r2dJAeGgi!c7i)jgHW<1nYko#z(6bi>h}EU%IQUKBhevnaLGOKL~H5Bl_y^y%Lh<LW8K#o8%DJCQ6e%Y6I&A6&ev_+0s};?YQ!ACf5x8ChN>)3?uxcI5lAU-~i;$SkJ#i_4_=i_4_=YlTdLzl4m=UqT<9zr?t7{*v2K`HRb>_)Ey>{Ix<R!C$hS6Z~~Gx)NTOp-bR(A=(Zv_Wxp>i?*Q6@Y=|$+?D*@?fm{``27<27oq*=wdgu{-GEB)vJruoheCMWgd%wD1&RIeK6{t&`w{$Jf`9j;4d_gCJzTFxuS1*A*{BHD;?U=S=kU(~&w-zvXdC|=a2xz!^lG#N1#k_Ji!MMHqup@bjeK+wdJQVWwah;UyaMfk>z<*{0WJPHpanlSqifI^=vug5iw?3n&f|c6_ff?sUiju>8cXs$6-)9;X7cdwxM(wpnS2^c@;wzx@=6|kuUr4U?$15)CuI=>D(=kwB9$fio{A-TB{O*u11e_nX)MY2R4mCWc@#hT_*wkSuNGf?b5LgMY84~&d@2k1>+e2qT*X3O$4vg@j<HCznZ!&!jfK42<}eF+J&)oiOZ<SXPODh*uac#B>#10ZHziB{J*{HNze<+kt*2rs-ZVUlA6@*E{_=EL<Pa6V_~vI*S;(_Ft70LqV<s<hh>Dqf8Vh;3&0!YuIv&MOw)kOlR>hKkl`O?uPsLKaDOvLGX%$QURk9RsJrzswrsPrl=;Nm|dq(fO-#Ik?tM`2*Qt`k1{WFVcEaZRo-uEk6$m^KN|L8sc9EmoQn8~NHkeAyWW+AWRQT$|!ALs1ixQc~;bu7uBR<R_nWZ_@YW)chk>R6ILtzt=D$)otm7C$i8dMcLkgOa6urDQ2zDOt)7N|y42lBIm5WGP=Mc@#hT_}Tn{zb=a!q~h)OKcC7%p5=TM3wa$gc~OH@%;eKp$jfaGvyj*ED1NfV56k%~7XH<-B!61PlDv|Ie?^-~Ec~luN&d8oC3z)};wM}Du$-@ADL*J#%2!I3@|BXM{GenhKPXwsS4x)hm6AvCqmQ2_E!6vJ_ek{cL+txw$?U%KUl-F@lJBWll2<a5-}zj1&}I@d`81Z~dn%UXl{|`{^!Pb<!{-M!Phw`zG?wIhDwgDx%;XO|{#S!GlbFe;u_WJ9u_UkLQT*uRXY%|f$|8rT`0<yXOJzyEr(#K7$xL445EV1|G?wIhDwgDxJc^(6_z^io#mt^*EXns&EXgaG$%`DKVkV!)l6+6alDv{f@uQEQ$6xxx#V;PLl&|{GM<W%twtsf<na}=Q%ai9{vbgn`sVI%V`<;(znf3d|AAKd2ulmr_TK@V|U(dv%O%)$soEYe)V=+b*v+ooMTdA1!D{QV};g>HS{D6{$Uvw<|lE!R|Iu?FOV`g(53%{hXXj8?)FKH~ssAAz49SgtcSe09T|LONfXFYSx`0#vx>eji)zx->9S!GnY<>=4r(N}-^4`oxC4EZNh9)rGm(AT1=42-=8V=rfw0UP$fhNpFTULn)V;ICc=fAuo>tCztSnPk?gUS#k^CYcQW>Sgd(PvtN6H*MHo)?t6sW+U3n|0>=M@cX&wJhUBoh#(v8oy*yV_qO!^f{w@eLjD(YLe7`)zo2sy@J9HJaS7VF8h&GZ9khQLx)OfhkM_dv8~EP>V&CIE6Kz7TM>oRtMsybcM(<9z?nLMCZ}i50m+w_*8~=Mj+u-Nb{2RSKTzzx_|3>d_xb8+5ql?fkG!EBsbSeKv?;g1BL09m<&=-G?_bO!ZzcOU8Z|?GM^j-_sYtb3#XYc(?S=0y>v+pj7TBG9c6)r1_nx$h=`&7*O6*W}Hq86+8Telw1#G*|VpLpSO<3cwbFV*X0e)Jpn4s4}j)~~R+iiKZTjZm@hi;jg~(pc0!6$`(lv8cr=7Jf-%(WZ)pU($G~UMI8gi;jg~bevMhPb+G4Ijc-cjb1dBS>rlhHkIk;{Kc#?{hU9Zp^lGdsN<&<HM*QtCZ$F%n#!zk9WR^8WbjungTHzzf5~-x3$NaU*X#2J^_sx_^Ei{C+P#@q@0)n#-#n<}H}LfUW40dH$gB5WUdcBO>iBi9xH|s-;k^lZ'}
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
placements=[('t','agriculture-fixed-arched-two-bay-and-lowered-ramp-stock-trailer-01',(0,-1.6,GROUND)),('g','agriculture-fixed-open-headgate-handling-frame-01',(0,2.1,GROUND))]
def rigid_point(instance,p):return tuple(p)
def stored_point(p):return tuple(struct.unpack('<f',struct.pack('<f',float(x)))[0]for x in p)
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[stored_point(add(p,t))for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,rotation_z_degrees=0,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values()),coordinate_storage='Exact IEEE754 float32 after translation, not hidden deformation; native versus final GLB bound unchanged2e-7'))
base_mat=len(PALETTE);PALETTE.append(('SceneOnly_EquipmentBayFloor',(.30,.31,.28,1),.97,0))
v=[(x,y,z)for z in[0,GROUND]for y in[-4,4]for x in[-1.4,1.4]];f=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];emit('SceneOnly_ContinuousFloor',v,f,base_mat,'Single scene-only finite equipment bay floor, no extra counted model');FEET=['SceneOnly_ContinuousFloor']
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
  assert -1.4<bb[i][0][0]<bb[i][0][1]<1.4 and -4<bb[i][1][0]<bb[i][1][1]<4
 for a,b in itertools.combinations(names,2):assert any(bb[a][j][1]<bb[b][j][0]or bb[b][j][1]<bb[a][j][0]for j in[0,1]),('Whole instances intersect',a,b)
 contacts={};floor=triangles_of(FEET,vertices)
 for k in names:
  tri=triangles_of(names[k],vertices);mask=READER['np'].max(abs(tri[:,:,2]-GROUND),axis=1)<=tol;bottom=tri[mask];norms,areas=READER['normals_and_areas'](bottom);expected=float(areas[norms[:,2]<-.99].sum());report=READER['actual_opposed_face_contact'](bottom,floor,plane_tolerance=tol);assert expected>1e-5 and abs(report['actual_contact_area_m2']-expected)<2e-7;contacts[k]=dict(complete_ground_contact_area_m2=expected,actual=report)
 tris=triangles_of([n for nn in names.values()for n in nn],vertices);rays=[]
 for p,d,length in[((1.15,-3.8,GROUND+.50),(0,1,0),7.6),((-1.2,.70,GROUND+.30),(1,0,0),2.4)]:
  assert not ray_hits(tris,p,d,length);rays.append(dict(origin_m=p,direction=d,length_m=length))
 return dict(instance_bounds_m=bb,complete_instance_count=2,distinct_old_models=2,new_reusable_model_count=0,whole_oriented_triangles_and_pbr_retained_before_float32_translation=True,actual_full_base_contacts=contacts,selected_visual_clearance_rays=rays,not_navigation_or_full_space_proof=True)
LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate(vertices);result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,.95);ORTHO=8.6;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(8,12,8),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
root=bpy.data.objects.new('OneWholeTrailerGateStaging',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole scene horizontal centre; continuous bed bottom at Z0; two entire unit-scale qualified instances';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
