"""Original cold-frame seedling preparation scene, four complete existing props and zero new reusable models. Lightweight maker SELF_REVIEW; no growth simulation."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='farming-cold-frame-seedling-preparation-scene-01';VERSION='1.0.0';TITLE='Cold-Frame Seedling Preparation Corner'
DESCRIPTION='One static outdoor cold-frame nursery preparation scene with four whole unchanged published assets at unit scale: a fixed-open cold frame, one complete six-seedling tray resting on the scene ground inside its empty footprint, one separate empty open-spout watering can at the left and one complete laid-flat D-grip dibber at the front. A half-metre-deep bounded clear front work strip separates the tray access edge from the loose tool. One simple new scene-only dry-ground support, zero new reusable models. All original source GLB bytes are embedded and hash-pinned; every original triangle and per-face opaque constant PBR is retained under translation. Normals are recomputed, not original NORMAL-byte preservation. This is not the old two-tier nursery rack scene with more trays or the firewood farmyard; no greenhouse glass is dropped or converted. Cold-frame panes remain their original explicitly opaque glass-look material. Static illustrative staging only, no actual greenhouse climate, moving lid, plant growth, watering/planting operation, human navigation/accessibility, agricultural performance or safety certification.'
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
LOCK={'farming-fixed-open-single-sash-cold-frame-01': {'bytes': 21632, 'sha256': '4fc942cc4d59d745c2da7ae425baeb5287a6e2bc82afa6926a21ce99ab198225'}, 'village-seedling-tray-01': {'bytes': 135324, 'sha256': '52657255c61c2f396952cc09a712a38ff8332fa4b144ef31aa40c30e18b4434b'}, 'farming-angular-open-spout-watering-can-01': {'bytes': 16100, 'sha256': '6c38dadc9a600130cee0a2c9821394aebe6effc0999b2353f93895b41080870c'}, 'farming-d-loop-handled-planting-dibber-01': {'bytes': 14452, 'sha256': '3ec691b80fb2d7a20f3de838585a5daf053a28db56567aafd45e77ca03938cbf'}}
ENCODED={'farming-fixed-open-single-sash-cold-frame-01': 'c-rk+eXJbSb-&mc{E@^TJYz5hh9w5u?6c?l!}go0ZEWMj@W6H;fSsrD?!5Ol?C!kI?0dGctkRS!sj4QC@=qn25EM1EBmqhqsY=a0_2Z99<&O#lMQuqd)Y7Jbrlm@xsA)xi=kC{CznR%tuSxocceQtaJ9F+m=bm%!x#!&3nd*r{%NS!%onUP5HpV`7eDZ<w1wW31Mq&5)!c0&PBEJzvh24dZ&qiTAjHMZLk@i=EdO3)sBfBQ01%0QsQ@0Am!a@+mm9P$Cb*EgoP%OkH3{coDw^3Z!{rLGp-LK(V;W)onEY!m?zoDq7E}ZK9JYNXTHX=VJF-l==F02Rj##9tmsqZ7R_?D(C^-3d<&iK`8QK~dz2|a?S5=Ih)i`809s?;$NX*vpPQd}tqQpul-rA8?E3t^=U^0_b$%2FwutNL|6l0r<N>d%qnwIH75g14nTgvmEJ+eg3-6glLZ4Wr7F=;l|Y(|!~M)$w@Np98}v05iYQ@Jq8b^eRgAP^yIsmHLb{ize7rs)E9=mmqP~uhe=1DP4h%2GcEh4pq(u<^6p8{gGdK0+t&f-DDj~6Evuhs=_({SLXw1&aVdJr>j6SRk*=;H4LA?#d=WPLsDYQdR(i-WM&D9=D+9sD5#gtNpsM11q$tnt1cCHlJhxCgCE7%4`S#%^5SPDf>1$yz5-#+NoRucOfcRE=SZPs+@e$s&p@kW?s`M=>t!f&W|ppyzI#GxONDxb20M;H@)`DncRal-<1xto%lA8@Cl7S`|KIV<1bKh?o@XUUmD}|MS*A(zQrz&*6(wI<sKoOybv!>e7e);z3nEC3AZ~!B8v12YmtX$$Jm^nD^|hch>(?u>U|qW_SI@A={do2`IOGwFE>;7qh;S~bk0Y)(NXRg3z^V4YR50rFe6=dgVUg587fJK9d+?PJLC}~~^_X02%RXJHRv~-25@UIsgAd0+PgbX2)=6+Yz!@HnLX3K-#dRpDBcGf{iZNrD5Q9rTAFE^Y&U&xZNir!8{6<`C8v%l2VAy;HstxPab3&|^(?mVS8Ipz%5xab=x~<k46iI6!3Q9ptV)Gyq&XZR83{FR6^JyQqdl9D_X%L_=yG8}~8?hj((l0B?){^!97C$ayX|_@=W65EAmWxVJEow!*XcWz&RkVvv5ffGvY~j7B@I+#&QpT{;epG{D#<|+Yxue7t(%LvlJzff{<#De3aaloDz?afg8QxxMv{H)kM{yZG+^CeMS}s4u^}U<?t5`tHo2k^N%6?<M25RnfXO@IRGHcvc<(~Ha1gDi^y78F2N9u_y&G=CnUp+}BA0eO}FS#hiLd4UesS?;BBqE0@oIhFc%l=%WvJjjs?1o*cF#^WPmX+fQaZ9`&MpHZ$>c4po5jviN7$H2U?^aO9^!cTeg#(WsIC}8-$pT%Eee!ZXjH23fr7?@BROVN7;rCPx>{|T~9r@(Jdt2QXD#4j4tU^pm;QBacd+Gu?P}^;=qIldOFF(!=%Y6vSYWp}Gqvq2#iLN}qD~I!lM-=+X9V2#=Eqp%$hdEKHoem=Cb?$U@e*g<sE2U%M{LCzJN$y}28^9xs4nf<Lramqs6?N!kJF2B9rsn8Hd8a1xm!deT?5MV5;+mqjF3N^u%DSl=MRML+n@wjxEaIrcv3qT&ZSbC|X6uS=Sk47n9vKtjTV-pLJOa-iaz<)fP}Q-)QdMb2s>WyO=%!{Ew&GZc*Ai#6(@31t61@$WRBJzd5c_s_PaW1$W=me%mMurN6imUiT81)B+kw#xx@5PgEK|Xxbae<bsYa_S%&Vz}X=6&KS|P8$7P%z5$1Jc>RcOt&$dEHdmD7l^d@2u49zSy8$m9c@>jRU=?%#J55fn?IQZH9ZM5Fe69YhySks@>C?Ya4CJ-)ig*AV$C$$XR2pxlhj9%D;nY>SN5WX8QrCpSAs(621=qx~vP!~Gd^ZeEHiFw=5cGcy~`&srB)8#xV{o!I8*EtpivYty9kH9tpN;OOMFYC>k3o1-eMQ?-Ags_6>O%rEov7S^iTw^&tUz--eK#{Ap`>#BX$RqX-Xm!^RExeDu6lT&?)m?9keCCX&Os5R#4`RVB(dKhU353k*1_{6z6h-N4>qY^C9Aa&AcXIooIYe!aeO*Rxow`k)~?AEqvDTZnomPT8oraPLcsJd*M8r?Q%Kd4YfJDxm<tQqaxL3fZpn6yc0ib8{^nr=9%uGtu)!Nn^)eDHwAQ)O`)%HU~abyt(RYu)ae+3kM(z`mpVjx8BL%jR#X9W_D)s@|HeZke_Q#o0yLrdyc-6oMRqx{i|$RA|sb?xbikC`CPLhQ1^N)0K7>(;m4sh)HI!Y|V5u4LTj5NPX}`vbr1Dic~apkS5K%4vD$Roe3*4{K=-|TY)zza2Zp!bjMaqhx`j^jjYQm(i7E?HM>uda5?^R49&E3O`)_^Hw>hCvS#WS#gZ+qM@@x8>Z;?Yj-_eZ06kixIix+RLpnpKQ8!yEur*yb4Oz9gFSXJ})3!~=vK3mVn!(qkLJQY$w7zwnypBn4I`=<Ibxd8i;NF8)vOJpR6lGM^De7o3ajEJ^4RUK4VkKjFTlVlVk?Yc=L6EKU=x7a6r8c4}^}JCnB_0hG)KUWD6^LnyF<MYl%pn|NNjMoUA|(d3D-w~E5krz<=huQUYy?RTLRTiBI3wl;L!?NCVx!V_Ow-X7ThnODHgX_G<L4lhBRTw3M8_;)cvVs0=2o8;OiWZ(EW?BgL38}b0q*1&_@&9JNwJK!KFhWos8J<eSZ9N*ua24_jhrH>1EP^`i+XJNj*Mjkm*Kw94i1WCBZxwy<W5#ANi=L7`g8<Mjwg+A8KFbf2Me9qe?UUy3|5;tgxb{BDUPDqj%CRP#U89YRkaOW)v)VOD50eXM}ofKKv0d^r?g8)fJ@4@tUIQq+PW&MhSiF|37XH;gEgWa?UD89<X^_L{@Qg7yw0%YRup%j2L+q8f%(cB`6QOH1$QzLiZm={T~uYlAW)``$Y5EDtjRid1hthL=$c_`P&!sOkCX$HsSTSVVZ2^{u?FPz-|2IW;Al{vY0%STxCp;6IX%t)pn&@gKbj$ky3SO4vJCFaFXZh_o3PlK9IdajmeJWZ_5R+bJ_PF}y|F*3L(Kcq?y5G7>`T>#O@0)uJL(8(hZ~O~yEc@~mv&!b^`T_vhP-^)9nBm;c3oBV5qwS`%IB7JH#BP$;Z1cUpTjOPirGzD8AW)6Q+<@~nxl@=-L&P)_gTv^?fgE=mxtILTk{aimv%RYQM}?@BD|wqs=1+rcQjicL3qb8<q?EeWJ4Pz)G4wxlG9U~zeM@now~hCixWV-tY0{FVOx>0{YM^P?>_Xi=Ju0oC!YMrSKJKj=D?i()lWa0h20#u`R+ru+Zi(jyE!nY7spJ%?jX#%ucy5B_hSFI_*z2aCD1J97-uoZI9@W(Oqwityd3f@8Rr^yJzI@-HM^F5n5|<sqP>ybfIG|CTC{7~huC#&1KWspBU{Cmv5&AZv}0@~Tfx?_O=vf<_3R6O{+;HFhu?CY=EY_femVM~`?=S@n~9gb^6#$orSD|oSHAoot}**!CMJ4q;`vNWeBb)t=Q1(LFK_s2CjRD@zw6Sc;m3aPy)NH0{K9*$cjZsRMBmXv8YaFSeJ0`i-g>fYmn__|OBU|fB@1`#l7%~V$-*7GWZ{lovT(;PS-4}DEZnh67Vg+33yXG1!n9VS&phqkdicy@8#i0Hf4z$|Ke^WM@L59ByUrMBJsRs$n)Y=!i>5t}*H51)kJnG1PSc)O5=~PWXEAA<-gPd|Vv;<)>s{PT8D}wzrl)_AKHV0Ay}TUu@^aYA%V94shrPTU_VRMr%gbReFNeLn9QN{Z*vrdduP)6pb|;hYzLjmpdlUAzG3;s|!FvsMI@;@&;VtpIWBmF`{N9Z3W$ZA!i*3id$adkaG6Qd$?ZMk+`|!RO6o+x2?i&31KK$N=@56kby&LV_?4#I$uVXvV?qJ*auDlcNPIeD=-48Pbt-{8!8?R$JTAj(*n>R2Mt;sa(*c+LH)?pU*@0-|Ow0qfZb~C$$d1yU0!M3p5*#Wc%*srkLSb-fvdx-64cVPeDigqhI$nJaVznklJ{G0oO!tXcJ@YkQY_u?Q-^e=D!4X^g*GZSf;=m%k<w_kqOJ$%m#%`{B(gD}zWUh}l~m*4&DL>eagL705y>>C>v5B%{%+;{N3NWU*#`zbViK1ug+-Rr0CA18&zyM&iVJO;><M3Xg6n{Vbg9h&Yq%i*`zqrD!OvPSYz${{JYqzv;~_}VI-VXngGI;^5GzLsbmt;f1sgLVy88(xc4Q+(y^Z@Yu=Up@6oGYe0w{=Pd1Q@zj`GYQ}Ro9{F`d<S6~GYfb4W?_+U5+1Uy$z8L&v_0~^_o1)5S@lRBnjvc_FNZu{4tcsXYufe63SP0S=Uz4j|GEYqxDM?)_~LS2*(~QCO7Zqav@OqM@Yq%OZ0y$8|GMHU%?#}3z?}YTPySIBc5`6vC!H}<u$u#OdU4DI><+?L>+9_L8accx)KjTgsHak~P*0^|p`J>`LOqp=g?cI#3-weg7V4=~EYwq}Sg5B`u~1K?VxhK5#Hf*7;k+Uh3+EN7SU9gp#lm?-Di+QwQn7Gek&1=$ic~C|SEOR$ydo6~=M||~IIl>>qFs{k)w=j<U3|4J{^06j)INKK`YsWphH?jCq8IABL`?L9FwqP3T_Ps>L73=;`YsU@{UCg`9?Y%>QM0&0eUypYwNEM*>Z4RF)JlmMB6&jnn2Fo9VJa5t$5brxO~F^|xQseZdiQ_azx`6ftxt}*S=fH|3HRQu|22_@-~ZhoyKj8E>V7JGFB32P!MuC^CpWlhc;U@!y*uxF*!$+xiC44m&sU%D!aw|KDt;~axm$Sfg!hT5=Q8ofe&=ED>|cK(6_bv(zWuDbTaCR>z4mL~Yfo%`^_m?Y-#hW;!mIDRA1$7Et@R8PG)>Sf=AjX<gMJb86QI8+^2$jw0U8f9O_A><yoRO8!>da}r%@|V+tWD!ok87z_6Ah>bPli{EuHa-=Kw4DGtHI!1Xw%=_><dKa6evqXVcBVUS3RfL<U~WgAqd}Ix?hSFE8%Mkb)Nn;lKFl59w@b!vFi<b2G4;7ytIcGtCU#%!5f+9T`%vn-_OvNWslP_!n?aa=B+IAJjR?6+cTEa-1tYuPdeJ%d~s%{}>d<wxHd@Ze};JTiD%b>G{!Cwhd8jD?ejj!B5s#@TXW5^=?OdJ9^y8BvwRQWZOY~527PIYoaGltJ?qZ*udjs0c`<2Zew?_akS%X2dH-<lHS8l_}B1r)iwBR;{O@B8STyJaVOi%?m~MP+Xd>akYp$Scgfg`*DwClJAdPT^5nOg8Q9B%3+q1Xz47@UO=RH3Jb3IIZ@P$q%?#}2!9RZgx4fUl&rf9F#X*?PUC({(J$HTMrDg_p^WZoB>}hZL+@lj2xS0pv_s?&;kA16kR-A&}Jb2~nzwZ6R>n}}Y;N~Fw3#hY(uEjp!I_rwpVwXA2WzXvh>Um_li_ae^X0Am`vGk*eoLkURETtH`4ed6>t@ZpLZtM9|q+1aGHlU^ake>2OXz8B<^ptZ4T6$hjF>@7vc61$&nH$kkETx!PKufWdo-vK1rC7R&Kk?jz&l*tQ1WE4TdFC!e&dq2yBZjV~{1)w2^w@s#3m3;W|BL&l&p+49z<YDxi=TVyGu}6T`ocs8-kSqoRBrrFcj8AcH8b$u9QfiF-+$UW`2EsE2HraeUp<G(Ui<$Ck~Y1z', 'village-seedling-tray-01': 'c-rlq2bdH^(6FmI3<w5tj;Ere<8lCQmYgJm1eI{W9XTBbl7or~6c9u}MF9~op$G=#b`cDqprT^V5d~3H%;?{}w|y4p?%oc=_xx#?XS?2+o$jfwuIa9txz&;5`gULda9247`zio*>C>b8thnqcQ*!d-n$L<GnKL0LFFSu?UR?9I%SPo*oG@`py^*R)y*A@=CXC3*tJk?%k9yNm;*;Z3(&L)MP0PufGJ4_!b#hXCLfo7taZ`q?2I870glI}!^DAe?O~@Xvj>Yu}e%B;!!o(55FA@gL8T9Yothn(xQ$_`=hR&Zhdfd3|kvUDL<m8MPH+sUzruli<GnytO#_4L~v-5NEMrV&JtU6-i)M4Xt`ivftGa{~ee%{oaqDDqdoRBj^U3Aj0yly%9+2h8I9^QN6)RCi<Zc}uJhh<O6X*+S;#JmpK!-L(vG9f-WEkXZFOi4~iO-xKlPi>MApO}#u{Fk1Vn3|E8lB5nLWTXbqOUTGfNl42~OK*~>6$@R(w5R%$XD(QDEIuPC*jh$%a-yo5nL1}qlW4t|l09LB!%n0Xb|NV)DJd->B{^LwtojrDm!6oKl$x5Jq7Ee`7IrHmBOyIgeeplog^8obIqX7WYN2vzDM`ucNr}nY=9wv{>#Gi>6b?gTdPYWKa%OVM|6Cu&<z(kN>_bv&(D46pp2UpP#v(cWe^%?J<3^7hmG4mZltL8~QZtnYrKRYeq^1@2Bq<{$JtZY6tx2$lZd4Ceoigh5siN)FVL9>2I9lPn(c?$wkDeAfAv-@mZ}hOK`8h$Yd-mwlxo_tl-Gi6w-lKQ7)?MS8CpL-e+kQaX9zA-u8<G&$JV{MUqbH0QJzQ5w{&(h3b+p|gHJI{mgQ=%Cm_{2+rwt}XYcS*A1~X4@Ffk#bib>I0OiU!5PAb-BGHo+4g*KWTwb4}4Xj-vG(@$$OgEpEnCpevF4_Dt!nV45NTEnL1=H}$}8=Z4?aD;|W96w3T#}o4V&X}ZzIW<u^kUBVZf?9hr({yXo3n$>hi7GKUF)=wIDKSHPUP9;|%1l)Ln4FNTXM?2BgqD(+o|K%FnwYGeX|!67u522%ktR*U*U1m66W6bO+vGTH8>)6<$!bTdp5&x@(toNahpV1kR6Q{{si=ORwynFi?){$@Qlcx6oRLE8o>aJIB&DUOxhlBqC55b&o|ciU=BkV^YsP6t|4$1Ep|evnlG4-CQ!>)hf}`-?HlkTEHHJ<^tDokm{(pxdJ^C=DCS{Z~3>mR|e^O{^NKDL3O2|yg3@&?x|5DUlkeZyD8eBor6HZ_E=s1LHBPp~9rKF{0BqXI~rt5(S*Ge=?X1co_5)<6r4~Zq*j(S=B*OG~P;Zk?G^01`L)TAUG1SKV<o))wPO_@-*)FmaRq$(#(I?bh%)OWg(jEv-z)Z}0wm5^T8MpC9SWO7ncO3;#F8i{I(q*%HVwS{D7Erc;=N_59gO2{bDvlC0WITKS-$dDwZq^GNyAwkV1si`TM$%U~{VXT^xl9-TQ7^<r1Ab2P(QB4sU$q8w6L=rQDZK!!&MNS!ssX7WtObx9MiD{{+$tfY{4%13hgQmsOm8dPGJ8L1#kYtoF<<l0-kf?tB+Xh{FgUjx)8TmO~b0&<;AEj>~HF*S&^vKN(CVjfK?7Wd0mEF>k{#7W3%7sT_t*;i5)2pk+I3@P#YEe18da}B&Pp_UFrFx3;x?=T{lhb0q{D14GXQnt%zfjxLte2GP#C$69Nh{VsYFbiC>=p<!etIo%<pAj!$!<JA<<%KZTp%$mA)#0cndwf97^a03HIX<O26YD(YavZ9FAh8@F}>J8rl<c$g{T9Wo|I8c1vL)_qmWoT@!uA7FqYxW7m5#svTcTgCe)f*yoIFnwBkx6|2w^frZ%dDnn5x$RPIr)UcIMIA++h-9r}L0(GTiho1r;&tbG5S&$Xz#aBNJx_vB{(eTsG6SXkG+y=~bn(@rd0=Isl!Ox==LUrX1Gl}X?Iv9PXte_>x@VqJH0p{-)(P+wx^kgZ~3t=r1NzQ@F>u1$QSL{@d}`~MyH5?R;X{I6fd#AMuKV&Y3Bves?ozkX68lfL_7<@^5~>k?UC>%M>eszfGzkBN2N+y5Q+5}DX4Cf5D_S)>Nk#|OcG^8>mp^K!+2{;WP!(HHtY0H^(%@1u2#pC9@z;_=hloL{W%)7tluc6`O#q36(g#m_h2M`|aW4a~oAx{iLeVnBc1-&Zj}zb}5A)-R#Ir=1(A9jb4H{svC(%YWJr)-8U%X+P5O80_OKW*=Wje;?Ji_;EUZ#rqV^-y*dW#UFfR+<jr}Q{3N9JD>P-*yG`@8O?t}?F2%0_Jz5>PP2XS^T~LHJs!=T5&XwT#@$Emm(z|HYu^`Tyo&o<*mm~!VfLs87ub<xO7a^v{8*{Qi)vrBX&V_lUU*%5j5;q-?RRZ7??3ywxmA3+esMWc%V7O_!Ts~c4)N*hnSCvb>Z^aFl+^phrPgz0-@olhQtPuy$t0!E_QS1w#rL&5f2_~9FW4_AlIFP9Lrbk+VS9!9TI%{*KfNDK0<`kwD5=jcE^EH!5864B1lS$4r`9KuZ28a}yOug%kBgD!xYjd6$)8r#E3z-$*ZS%GXi~SQ_0`uaF7@@aT_Q>CCqJ$LU+th?|4MUQ_fL<9_Lp!{>#NWEQR!>!uaBF3?FZ4M)?e2*ve57T-Oqqla4ux1kAOaKC3I9}M@Wau;bJJS%JPr}WuYoGQ)M%#3-#bqxJs2*L04d4L1{Q2DnKQu0kt3w8bBjx0!fep&B2B?&<?slcjyWIU;qq;n!urqD$76}C<PZlWmQ&&bD$zz0`aPhhbqt*E`-{utPM?}6I6rxs;m#);3DV?gH$;P8p1&61wB;R1BO5{Tn4>W*&EWJzcObBRd#?Ype?k3R8^)zd)3_p$W&z}NN5S=;5=2H2d$wxbcRG#CIZ4;&)utH<_#@>*wn#}m480<X3K*Iy2iw1-`)^pT{jlibq`PfCd;%F3oqSsGRxF0iS@N~-B_9Q-5(2+zQn}DRxxv^FEMk-RxvT@drZ7)!fi#q5eqlGYDv*p$HKa<@ugVVjCHJRd?^;zx*6Yyg-PH2v9cNKSeV!<CMJE4iAi5#Vq&XU*(QDx6O*wnk(F*X@v9P9*Cpc~6BA!5k@dBRpOna?@BUbr^d%-Hwu+gFpTxv;tV?3j_n27CT{c;pN@O*6*<{@*k#$|NuEoS;-HD0GT2>-!-N-ssB9p%RV`Z||l*q(ZF)`_TOicO`6BAp-#CfBZ`Ae(5ABwxuj+K8@eR-r~c1--~%oRb_bz@;&SJ^7dv=a+I((%(QQ@146*V1)kWz+Zl)9jeo^d(j{wmQ};BWBipF?C~M-4|20BsP6FdX~hhu1$QSL{@ceGVUd^u1owXCMM$^6BA!5k+p8bPfBFdcWSGWn2dFaY-|-8mlE0ZJyte-iIt75jGi&Dxp(}ra;WbyF}c@bVsbCU%pqIF#N^(IiOJj>6O*|#CMI)r%pAIRV&>4j6BCoUHzp?cPE1Vhg_xM!YcVq!_n4UYQi)9NwV0U9y)iQx>k^sF)iE)ddt+iUm&U|ou8xVl_fTi{9*Xqqw0BI!kDuv#s7USn-|`-cydOF39aHh+XZjv0Qaj#zsQ<g(LwWO$H~)C^k2nAPpEm#KzyApREl5oBPx153wIdyOI{$>)@fB|;lD`!{-+Ujb9jEgT>DOs<OY!4pI{!p!CzAh=e#JEZ6hGgzAL+Q$`A7eK3>kMHvCnD8&vgEY)J_zC@R4yZasDZOKJn+U$DPhUME{uPpW^3}@d|s~>HI_bb=urg{P>y9Katw;<{xkV@#Y_I{`ucE|BTFSU|)B1fgMR!e&j`a>FVlPdSCxNn30v#ar1Y8*Q@iYsQs)m^Zv8{%cZq^x_&rm{tob7wV#{Y&!?|v_O&$iwXRy4eJXR6KC>(7zxN6+wLUYI)cx3VvheQ!>Ase^xoN?63jaQ=P@3af4=r<)eueE7?rXVM)z^CH{b*AE9iWzbPX1ROJn&G^&XJ`4J2^8Bk>sk?1B2)5aWT>y5B}Ypl518sEV3`%*LvvvXi~SQr8%F<1L}I(E|H|xW6kPwe1&>Jku=A3|MYlhe+ehGzWO|^ud%;AZuYevGfR-VK9&0VX5aIF&;S2__WzR`nVpin+>Rt~x^bTkvm3V1``Qjh-l&g<{9m7Uv)a$io%WyoUC-3?!JLLI!b<aZ;A;QcenWh^p4l(-vrv8Y?-?caesQVwdF{Y4JCfA;98gm0vwC%BU-5n2ziayWe1-jjB596mJ+!<=>Gw*oy~6#%ap@e?Pwz*Q+W)n_`uyTjKI{+LE0Waykrc9LLKvy_EPchC;Q4x7j5No!o?6b?Qm@FqbYJVI_oGSOp4M0EQCtdjJ#CjrQtL5i3-}84`d6CcsQPEdBb?Ow>hoqReP0Xh>*Ho$>v158)cWiCRO;)Seb4_r|NsBl|GnQq6#fok72FHsR5=btz~k@?Y*OVWxC3^;LYS<|$#6G}g{xtSDwn`Km=8C?E>-S=hhP}w!YG&kd5{k?VK!U?*Tc=Q7;b|Vum;w`dbkfBfJfj_cmkdRKg@#RFh-SQU@nY=i7-`_Q(-hrfg9jfRo)8IU=dskb5uD8Zh_4(9Tuo^0Xz)X!FDK6WdYm-Ps3xdRh3&I0L$S)*rv*Duo9kxd*FUm-VZxr1KbI>tMYc(2t#2htXAb}$bq|H5{y^ncvuHBU<)i$<ub^I-vID{Di6SOP!VflDXgeIzd~jF5)P^I5S)US;cfU{mEXh1@Ch7&TKI|joQr$l1=t6#!0YfPyayk^XYdt#3&-F`_!<6yzk#8^GI&0g!zx$}>)`va7hZz*)#oF45nhGEsyqz);SKm2j;r!Gyah+$bNEn|AHsJ~8sC9WRrx8LhhIP?tgXu0_zhIY@^}GOSD(806O_dYs;q#&Kvnz)EUbza)<BMb!b#wG5+v@1AK-V`tv=7gU+@|nROLZHd>78a6YwsafM;O<4#g%oKz%O4DL4y9s&XXu$EnyJ6IGdrgRn8CV-HpKKp(ckPB>eYvvC~8VFSDr<1q<SusOEGHrN5XU{~yoeent$jKgpQj=>2y38&$7oQo~+LTseUMrh+D*bGxunTicD89QQkRd&ZTybRl7mMXKb8;-&ZY^}=HI3C+!KF(3)9PErUa57F*<wTr^eQ+%1sWK1y;ng?<b5)s(GjTXxiI=PLa?HVc*b@h;av)xeS78D+Rb^Am#!MWIy;Ru?>*LPOi~YCmIoWdU_m|kQ@~-@fS+gp|$He-#1DbW+SXkGsaP97*c4FZJ2M!d~Es6EDblq5)^xYo|lfJ~n#8xqLs4p>d$W}2i>3dA9>e|FNN@V@F{bbxrWL=l|RZL9AJtii;R3dBLh@X_mr0@P%nT&ObOl%bslfK8qq%Scsu~kg${e6h{_aWZjhj@P<^1tivLz?=T-Kxzsb|m@8Z!g(!OS2YD{Dsd2jC@od4?Q1fqt4r^_CNk;?tk_-Ut7Zmi<-3vE6wu(wLh)r5TCxD*+(Ud>Z^ZRntdv@p1TT8*^#8y$FHQ;r+)p`zT*43f75#Ue1-jjB596meWofoRq0pQUg5r$y8afWhu)7Q3-xaml=}SQ^60((pq(R0{d}NZ$e!V(*7JkbbAspp_0PN_X^v|>-&At()_O(urTbb>y&p-2#wjTE^@>Y<J#CjrQtPpJEBL;>xA3`uk><GWpBayEQtP`&ou~EH?P<Tz$IZUh!(W2b^{Ld?H~ac;?$@kdt=8^MS<!f8Zmu1TeG8I<=Wi+ZU{u!UN8`~qBm~cYt@YzkS)X4L>+?$wD~QVa{Ag_SZ?^pTsI1SA#>Sq_x9^L}`uu3TIxef|y3yENHxf^*)vCx2(b(7_8k=#6#%5e1vC&`qKr}Xf5{aw6+uc8JOiTM%ucsXIb*YK|QZw4ydq=$Jn434g!fz>la>r|q`OR5V{ACqu9h|ahr~dJK9JA5CvTuuH{`va0{uTB52K9H!56m9tU#?i&?Mzwg;FOIHy6;Z;inK=lC5pApowD|^n#~5C5igm4x&NyVZ2Rj?FSz11<FkTXG5%Rs{6wX8{%y_L+10Ll)fMMr6aRL_x{q$y==S{7t*-dF>=FKN6zewKaL04T26g*Z+1w4Au{-hS7FTTAJnoXs*zK;n&J|z(#U+0I-#MtFeCcfP9yNAuSl?@!_3!1}@DtCc1-ZWVa~Hh%;MAf%y5Z@^a*NtL8~mgiJ2z}}(>8a*##XvbH*Ci4i;Z`>;;%O+`M(-{dGMZf!_)5`=s%)Z&y8+)-=mX*ZR)wm4VyOgJ?n-|AN3sKhVM!2<lnyQir`x2hR5{G^gpIp_t6a>Yd195rd|`z2J1D*4VylmAhtRaCizG~G!Eq>5t-yiQ8|>4L}Ze$MdeUF5|u;wNK_8xBN3V8vr##ek3?jWUq|IoejSlXeiW6>bt5s!*P^nqLo_zy5{=EcL}HT9MrGqCk(lInj+x{;j+x|Hj+x|lj+x|@j+x}Mj+x|2j+x|WXUtj$r%ZBE$4v4&$4v4&$4p{-S4?srS4?7iS4?s`S4?tMS4?s`S4?s!S4?twS4?tDS4?twS4?uTv%)I(am6IIcf};vaK$9|am6GTJ1eYmLsv|4RaZ=MXID&ec~?ww7FSGiC|68!I#*0`Ojk^DURO+V7FSGiI#*0`v9rQ@4RXUI=XJ&U-LrWQ7>&()z(~BN@|qUrJx(+>?{Ok=-=4p>Fz=P3v3ai)jm>+mXl&kdMPj4Bey0|V&3m^<Z0xDu@kL|v9xxKCHlHEajmSiYu&ny{46#E*CN_!4WLzRL8JDnZ^bh$%L?%8HmIq{R-(}wSIprS~f8N5p?{mt{b4nEyz58>>_ih?jVBYsRWz$aZ-Je4?`s;URPI*Sp<Xz@{pHu$jfu05Ceczd~*1;(o9dzHFa=oXsTblQMPFeeydEe)hYfSxSmwCtMhMya=;TiLe&ke6_(sGx1$LEFzly2YByyJ7jMz`QQJ{LUHmr!8d@wwsgA9g7)@A%xX89V*V)(x9BkGo_ucKVsW8*Vc8+Lq=W*4beF&d3exd(FJ#bHhK>c%iv@r{;!_AD>!a`sjue#xyT5ZJrI*@6_C|(M{Xj4I5kOHr=opJN=H&4R5ZuqlJ0L=Y|vFWr2Ce=Y}WD$|*4K_}s8*Q{S_0*z{4)A#S+wpL2GZcYJR6lR0yDns<C|7!K4eFz@)z2J1D*4VylmAhtRaCizG~G&b)6BQeR3qOy696NyQ_7M0C=rD$y4b46qGo+}cQd^ReZ_imAx<kwNzya$ZLBtMGEM2E0U^0lZ;Y!Z>lxI|<!E@7GEvr(D&OjsuQont2Xj$<ZymSZOQont0>rDG=ftYap*l4B-0+8MLf!6}oR)G?F%&M}kx&M}kN-W8MF#}$*<-W8La&J~kf)fJPR&J~j!$`zAb-W8J^(-o6k-W8Kv?5wbUXXJ)SZ10LmuHlMF?&FF{E_PN}zf*I=Bv*CCBzJbjB$s!^BxiBOB!_avB&T!5B*%2cB<FR-BxiBOB&T!5Bo{j?tk)nnOmbdVtp6WZ<adG*nfzujEU%8svdQnfA~N~SS6H4{tCdZDcNUS!Z_pw#`5jzDCclFV%SQju@9!cq`Hfy!Huent9xx)4-wcLj--2YD{BAKKlix6g<<U1J*yMMV5t;m^G9r`Tbw*_JyUws|^bh@>G$NDVoQCCRU#f4L_kB*e?*yN1-uF4>wbQHE=6#=2F5UBwEc3q4DVuimJ1nPc^w;msobng7n%d@lpHq&%MA+ti-<h)3!6_RZbl;uw-0>Z3^S;k1YacW3`<!y;3v1fu9iJOsnU-vucYJO*Zb=i{yyJ7jdF$KR<{h6KHoEC&q;9xUn{#dRj?WD*TO)1rj?WF7vD43N-LPr%xJx!;r=R(|;ogBxwt0tjHdwzia>M#wGw=A^aNI|kwt1)KhO-|!nPvLuhKD|RPEng@gY`Q#H*9p%Hh06uR=Q0$Y{pK%<8#9&{>ZY;J3co&)T(NmcYJQR{#U26%sW0eY}(ZKtQ$6c)N_a%&dj^iHt+b{@Pt0;wt2_rhK~&{XBYhj@GNlf_kb?g^zj6-)tNBKM+%}b`ORQhCiziRCcpU#%Oqcm%H%g_5t;lBE+UiP!G&d#&qihP8@;eh^6RKfelr-BNq!WS$!{3LGRfDXGWktqL?*xMjL777one{evr(D+<}@sm{LV3xe8(}9Jj*eY{LV3xywWj~eAY3OT*)z$9PNx*>)@10PU@IRe&?7;e&?7;Z10Lm?&FF{Z10LmPUnhAuIh?OPUnhA4&{nTF7Jv-j_Ha?F7Jv-E_PN}zcX^fB(`_OB-e1oB=>Q}Bo{j?tlz1*VUnx5Vv;+%Vv@_dVv@7CVv<9-Vv^IjVv=LJVv_T^Vv@7CVv^IjVv>uU6%PI$&;^s6*A>(M7VrM#wRZ5o={sXeK(XI2{cre|aL#|)`LafjV7)dot3+%k%sD}M`tkW;|9i|OoKw6VUkvT|BDF(w_MLuy*nWjO=RfTb8%As=%sHkVKe<*Qf<DpCG4>(H=LaI#C)zp1+X=+bP9Rb{)UQrIKWx8FJEy|u7iZ1>eL~>DaZlKU{Zl5MZy&j4PVl^!DtuZXH(edr|Ilcguz&Lno$VLjO$dBjBgywye6~I5&xifns*drkSo5U4>-_<NyI<L7UsU;hd)k=B{@Fu^`?mG3=iAb+LLlkUQoi4smTOt%*W3N|_U8LeZ639&;__O7JLh-tt=<1+!G?uL3sycf+qa`pLw}1ZjRS`t&h))~c)Gvwm)rckHjniEn(&-|Yn`EiZZEF13H$p!UM29(mt_ML=2r6&4)iFOAIQ6IO|bvux&d<C0J&~}TsJ_j8zB7+kp2cpfBmGt0n%T6t(NLqzEB^t)U~ogeYDlJe4#$t>RPt$qtbJi($m)VQP=gW>-s`=_N(jKAv^okb$uZ_`_*;rkevhSx;|}ZQa3>A21s2$sT&}5sm=kSbAad^AUX$#&H*(pwi*{-Xp9W&G4iQ#@rB07upT3y8Y4U8Z&}L6d?9}`>{tF-p#0Mp@>RpySN+OYgMLo^**|+lmOZImpmfa(PxCSA&(z1>KY68p+2p~2q20f*Beg^C3+n&<?!Mi==8gQ|aq9on&uKgN{qT8K*Ln&5Uzg4FMY@lu&XL-uzDMsb>U$6Ik-l%&e&8==A3xD25TRdz2-o#TniHrE3Hu}6vyto{>3(0@`fY#z@^k&|#|@$PxGz$_=siyLr1v=0GtzN74^aJyJ^?!C(0PXHL&iPgd_r|r?c1t-TlbgFrSv|c<4(t#-czKV0G*@gJs8PnXgk!OsSndRjm}-_oC0-@9Xh9IZjV%#`ahiyBiVua1Dyk@Z_xQr^(&zIWrzAzv@S%_lg_u)CnH^#v~${;Lg!xUOVoepJRIpb^)WhEN9k9QztK6I`Wv0YBl!vS=SXeR`9G2!=z6E_FI(MTzR>+%G}d(OpyN(`p020V-_*TUpzbwaXpSu!(@1Nmn&13te)EOqx1#lwu8-7zBH5g-mDCPIpVMp-X<epkE3uECjuBl?>3Gq5nc9c0r;+SW*H&u7NNX{zOZAMj?ni2$uHAHuB8>}O_o;0ov=fNXj-QSf?N=oGN4l<;4|@5amk)aRpqCGN`Jk5%dikK24|@5amk)aRpqCGN`Jk5%dikK24|@5amk)aRpqCGN`Jk5%dikK24|@5amk)aRpqCGN`Jk5%dikK24|@5amk)aRpqCGN`Jk5%dikK24|@5amk)aRpqCGN`Jk5%dikK24|@5amk)aRpqCGN`Jk5%dikK24|@5amk)aRpqCGN`Jk5%dikK24|@5amk)aRpqCH+zmgBO@?EurnH)%c?tQ#a&bP^N2pxxVwMY2cUUt4OH#awUzLE8s@3YBqF!Id_Gkv%7roICQx(3fPa?^)D+vGSHsm~w#S8rcZa&quIBlY>@I2ft*DcC;Qw`z6u;CV)BeaLYzQup`1NppOs{`p7yeUa4tCC9<YA3m!YZ2zSL2ZHArIlt=1S>!kv*<_gv>VL=T)xq<OTzc`gmgG1Xsn6GT*mt07@H`{+`Q$hlsrAuz-h1FcmOjr&tq(a4MKZp*t;g_(^<{%&xh{TZa6e(^sNnw6_~t>08y49c9_?SEw3_YA3MX|NR1VGW6_eb3BrYb|dgl>47ODH&FS}WZQrm_~ZI5tL+b0&O?Hh~K_K!tsd;ea(RIp!KYCCJG?V+W%pOzPHC~Nn6XY7AuwL$s5aB|qrQ8tx_j;s&6Z{!|jFKyRYrPkkxEUkQ3U&qMF`G@Rq`$l%EIw*L2`l0r|SoZZe>g&WR-)UbpSg*L;yeK}b)Z?$~#VWNQIFWiB{<^Vk%u?IQiPZk$L~1{ABK3GUkyf+jS>dGi-*8fogA=L!!im&==tOFNaU%77ZtnM3<lgw5Sx%&$C!9z<zc`Vt)coW`YCqbXSu^M#;iUQANbT2JYJZJoU;7J{+ONXx8>#(*N<Hr3_KnozrllV5aMFBlq!(X#@s$@}dGVDOUwQGB7hietl^0)m@s$@}dGVDOUwQGB7hietl^0)m@s$@}dGVDOUwQGB7hietl^0)m@s$@}dGVDOUwQGB7hietl^0)m@s$@}dGVDOUwQGB7hietl^0)m@s$@}dGVDOUwQG>{|WIGf`BrB>Qf3zLs=-N%5rcXoDb!psw%5OC8!8hptdS&Lk*}7wIEKFaZnfP!G&<CDldhLp#e06cvZ$jV`u`+AXSyAkOUXNIl$GH3CU_}3YVy@KGalOW%b<!>KlFh61AVKJ{LeDq(BQ*wtx&shvpzvDS<(nS_dt)oeLGzRt@T??ILKTwgmNEn)*f`ucP)Ws81TSgt;&s+QPN4NCi)`U?sGIJ76PZ!FpH<?co-95<0+jup7F;I(P;8!UOO=^n-2i6|{pL@G^9Q=iv?L0f*po=ne0}_b>pyfoI?<_yNk{5cmUXV=nv+7vpGP*Z?O&S*(tg@e<63s(21I#L_qxF2zPz52rz66j&cE903<%9M;0C;UfGC>fkBJhPqe-E8tY9iN8Tb`~|Ln^YH?#gj1kAo`5R&6HI_=xC_q1$*>cSz`6J}jDs@x9dH~E$Kf52_#WgyDf|=wN5N<C8X&$3!{Hxz6aIvu@H#vPzr$V_48OvD_z?!dORyb&h9_VWoP;mo7>t20;88dVk3diO7CwZJVI+J255Y(9Fm#7c;2^vW!{7ki3va<%=mLjf54;Fh!n1HayZ|>s8`uX=LjdyNDOdu2xD^IM0W62d;Br_78(=Hk2fg5NxF0q{AJ_z|VGG;|UEx7k1NXpXunOkD-7p(E!(Ff#ZioJGGh72JU_RJz8_a~8pd-wHd9V-`Kx?=GnqmT`VN>-<#uQA)ma1%tnb;h&u&pZFVk`7v8|<vg&e#FlV<+sc%I<g>cEujpSCxIS7xu=>@d{O5f&Fm+UWwVN%*Mgk0#mV>+H!D++6H1DwROXeYHO{&YoWf;$NQ-LA?nit2jNg0smhT!0*7NRCaN+K<8c@^!6db1psluc*hOtUv7g$mQr`_z-{|9A)V{4g!*CQnfcN1<+=@@)Slonra2)Q%LpT~=!Cg2RpT^HI4<E&2I0FyjA2=W1!cy!S{0J+sN%$%Liurf~|G`;!3NK)DQL>usI;_mT#v8E~YsnU21J;?{hK*P+c00zi-t10HXYE;Q)`#7TZCNV2oTackurKS!y0Z1ypCzzvEQu|}9;`d-#5Q10b}8$^8nRpPGS-3FY#nxF7cn1;W7lJI)`GQS_h1&Q&DyZKYz?+!M=+D!jbC9Umcc5rRhY)Avu12H)?k7qGK($4WOg2F!dBq<>@RG}{=_BNm;t+lEylm`2fUblk2m9m>?GD<H{mb%3D#qu;aymtm1ou1N-W1dz^d#$oQ+l3Ijk&Oj-}Z<ScbieGx1#ZJ92g_{)PvTv6pZfB0G*h;SKm5Zo?mOJ5Io#@k>04Yw-(w2EWCfxDda=0Dg!IumE4h_whBHgCFDT_$JQ7H}H8pj4$GJd>dcDm+@+R4!7Wb+>BFkA3lZ8;<fk$K7zaPAsmB#ydQVq6x@gp;$!$Qj>pGwAiIhUV*}M^2ph_Vvr(!X#d26K8_g!Fav~eY#<B@)sw$_lJT{r-vze-#$*yM8*(^3+mGjvgHkU16*Q@e+b}hS(-N0^9<t^-HHj-ttE7i7)EmGS;HcxFc*c7#mSKp0P-{|A>)czv%8Od&9i`jBjE@w;G5_TIKq{>0;3U(_Szy_;r1RJBaNo<<hX0vP5cBA_4R`rcOK27b9QJ-7c3icLzjor!KXP>h>*c<FPTgAR-r`YZ64|asz&Awz8@U`p%R*i3Dzq1DXA;x$ze}t9cHouFV$1mjfvf8{c-^3d77W@I0$UE{!S!-UAZ)ctODE=ht&8Kod>&NHtXW12eE`N~?=acz(K93(@6L~gYz=!g^Y(Bq+Pv@_&Yxz}t1|Q6Ku~~d3&*!hQ*}N~G#xLhjv#WU?AHxr_DZD2i%e(V!ESHbu<M_*LH1EtO@XPoMY!a`;bNGH%fw$r#xQ{=_hVl0NO8z|Sz!Uf&p2Q2-5T3~g@ZGFAzmyN;m+)s;f8K=m;ZLzfycX}pYw{;p4_=>l;X7CyKbLpq=ktB68_(kH_#W1hm*#D`#W%AyJe8;O088P5r*X;eXBqrr-i+^L7xCX%JpYBQXH9txUY9@4s`HOn9sUVh!|L(!yefZ*mE&KtD*P+<7^}>WvUB*u>>KtcE5-j}TUc5CHv|44`-h!i$bVw@G0uNvzp@SN2X>g9WN)%{>}U1``;Kj8pRxDYG4>8y$-ZT;vrpMQ>=1jKeaPNrtJ%kFA-|E|$``87BEFa};VV?Rf-mE@@!R>Gs=Sl0;&<>he4Q%S@wNPJelNdYmG|=v{64;kKcvcs_!j;Ef0%Dm<u<;RKgu8HPpk52{sdpnZ{atnt$;tNw#WE`YTL-~QQK<u-E#GfKK`KEe^Pyx^Bw#t9#Ca~@8ZvJKfg(pH}UKFPJSJ~S#3-CO10g^*Q;$ae?)ED)ptA9H~RQ`wZBq*cJkeviNE-Zyp*^=?B)OP8sa%#Q#2IM@&=-k*w4$07UCsdTC@{~_{E~Pc!$S}A>uurCdP<;JX7=#2Y6@EU%bID7bC@6e2|zTKH%epPkh4j#R~B`pDWghZ}~N1i};RTFCGv-@g?GJv06MRe&ctFTg1a+vG|@pBpwm>i9h&OaiiEMZWc%QCUL*GSNzF0i}_-`SRlUS8^l_%QvA;E5wpb|Vy5_r-zJueRpM8EyO=80h^xhq{4UW-EE6ZWEyjtZVyyUq-zp}H8^j5oC$17ViNWF<zDVSV>%=jhEBcCsqL28RUn>TPdEyJ+PjnJ<L`U%%pC!79Y2s7fU1W&qqPh5)&k&=<BypUN5-DP$ND^=I2_jnz7f1O}ksyYNMDaQwA$o}`#aFzixJX<f;>0U_py(hj6Cd;TqKxPw&J{24t|Cjc6~FM7qM~RcDu@qxYf)9Cig$TsafwJ4mx{wYT{IF+#M`{Fs4bd`y5cq7Ow<t<idT6pfug<uagf&&<wSMyK0jYrqM8t553eHr=I4o*`6<rDIYNr(d0Fw8*e-Uea;JDwJSCnHyH&Yc6bQd~R=lXn7sYd8uXsTmROLbOlGrZ}h}Tv5x_DK*Cf*S5sPY|gSiB|P6(6bcBk{iYKzuB|ROOfAGZ7F^i^tXWjrd$`ABwltc1XOew&&G%0ribO{<hlxTzvxKQ}Km3s>-9{i1=E3D|V=Ihu9{*5|4@})V53PQQJQ8irU^3@2Tw*_1#zM8-4s0wZBJwz7oeoyu4KYB$8zd`Mqc?JIEhIM|rvYPV|<o<VlewN6KGBiku`*iC%K96!HqWNLq53Tq%DRIdYc#O-z;7%74THxm+@Nle|ZkmaFAhd9J)y?v@wG2joFnMLr@A%j$BQd`s4q&&d7qdHJ@yNWLhamhZ}^WKH>wd{4e68_4(Nc6mrXAuGu@<m>W)yhOe!ACj-ghh=&Bs(eZAkr&IC<z~58-Y?5YzYNId<c0ECxlX<yH^@42pByI(WPLeCu9Cat9kQ0(Desn#%i40Syix9uH_OWMNx4iuDyzxc<b3&<oF^;Ft@1kgpe!e^k@<3qoFdPco8%0+UY;js$`SHDnJeqbjq-MRm#iUI$f5F1Iaq>RBX5yQWL3FXUL|jpgXG_0shlHkkQL-?*;8IGyURbsLYXJ8mSyE+nI@;n4Edv&E=S9WGER<?J~=_!@*Fu{ww2jZ%GR=v93uNll*45|IY4sRUv`!Q<z@0Oai#1cd&oaUC)reXlTGCBqN{8v+sjh2xlEGnWP&^{+Q>#SQ~oL%%4RZECdv~cU4AG(kzc9uEBU$nLVhiesq&coMt&>5lRv5QC;5Z?Uj8V5SLN^W7kN_tCjVCD-||oSm;6Tx>o4^|i&@etqslT?DXX+q)+(>c^49s*QTe6(SZ$T93)FUwr4}OVl>Aj~C*)DJeJu5HZvCp{uWJ81tDIHUI!}EnSrx4+)~B+f`g|lSSRcsG)OJK3SKH6>54C}%|D9`9P}^t0<9|rYI<7tytZLR3R$r^GHN+Ze)wKFsc~&iJinYM1Zq2pES@o^a)^aP(8fx8THMHhf4_FD-_12SCl69-K$Es&7vo={5S?jE=R%7d7D`3T2JFJ(j6zh5G4lBbtU>&nsSZ`UsTWzfOEG*UD`p9CXF0;P2PFg1{UaF_{ll7$~OMPK=v_vVZ)L&L_t5m5^tW(x!Rx9ft>u>8ftB(bx-m(6$-nFu<KdoP^<5n;0SL;pdd+T*8&HC0lYW-mKu)ebnT0dH^T3xK4tyR`HRyS*<^_+FY+G};PzOwdPA6uQRm#pp9r`8izYwL5X!1};yXZfv%tPiaREuZzi^{Dl>)zW&zy4N~v-D5Sk-mo@WuUMJZ{nk?JHS0F3t98hF*4k%vuy$LEtrxAEttQqB*3;HAR$J>S>qcv*b(7V|+GTCA9=B|3vo+h=X3ex3SdUq2tqoSXb+<LlT5pZ8>R9(#w_A5w-K`bYSZj?n#!9tTTNABYtVC<PHP2dP&9|CbORQ_G>#SzhwboQ?p>?%&sda-j&6;IhV&z){tr^w;>tbuVHOiW7C0n`HU~7_fl~u!<VD+<dtP8Entt+i;Ymimj8gBJ|s*b<uw%YcwUQcB?<u$wiDA=*Pfo(0`@0fSyH}-E=yfyJn$2{`;j{c_=YaN`jX{TY{U5?r4|9aI;j``a^%lq4mN)77ol>3)!<!`N6+wDwQ>)@1)4!ZA7c_uqrkfm7L+$n1x+ds`dBYrxifq%tC_3VW0`&==rTQ<nm^Y*ynoI5M{hhBZLJ@U=hU2(s%-xmy1to!JOjc$R&M_h5`AJhDIDAsMd;TtE|eyv-wvbh^JW4HPHO|ICqxzQz?v77wr-L81>OJ5eusuXY6QoeLHc$XSGH>~e9%{Nwg*A*{Z&x4$&eA^9AUDU;I`sjx1zLHtg=Gov}HFj>;=%#J%hK;Rsn{L>QUC&$YaK-83?}8PNr3LR<H|#sy$iGsto*Uip@87of>o)aV<c3X~`kr;erjL3Kal=PjRP_%NErV;B8(uQk@()q0`{;((_eu)3sn^7_!FmmH!={g$iLK6rNjzNOlu3N(m`Pmfm`ObBm`NP&m`VKam`QBum`O}~#;kR4$|Qz&%p@Lm%p@Lm%p?|a#UxgA#UvJT#UuuH#U!?O#UuuH#U$o*#U%G}#Uv(o#U%G}#Uyq;E39HgS4?6dS4?6vS4?6>S4?8pv%)HtcEu#Ncf};vaK$9|am6IYbHya)bj2hFcEuzncf}+}aK$9XbHyYEcEu!iJu9r&AU8~M1Xq0Uz=4+Ld9qWU`NG&N^E}xp*LtH{OY=P0DQ|mw#xC<b*(sZL^fOYYZ1mU9W}UJ%pn8^hp6ryz9sKnf^E~-XS?l1GjSjl+PI=I}g<0l#vQySRW}YWI<=ehl+R{8jcEk6*oRVdpA-myP?^Ve%&yd~lf>jH$%rj&+Y;@B(xEmgNbZc|-4A~9ewS4b0<{7dZHe;us3Aka?=0=xn#!f#|a>Fy;y*bM~BRw0epGmr5eXp5k$Zq(~g5Fu?nXMb{d|=rw(?>VFySjg;Y4dEberD^2jc(fJZrIpLx9Nt>*y(4;Zn%{%C(ArTcEiuV)W4;9hU|u4UpjD?d4}wUO`H0jb;G8QdJb{JVt~jp&yd}4Ubl`}<{7dZZg<Y^7Umi9*<if}xna}C&BRt`!XzFpaLOb;bj&0!b<89lcFZIWcg!UIcg!TVbj&2CJ!957IAs#UJ7y9OJ7y9OJ7y9KxndG4x?&OwxndFnyJ8aCyJ8XpyJ8Y^x?+<1xMC8MyJC|2xMC8!o)y;5B;7EHg<LU-&0H~w6<sljUC#>ZXSQyb#P+V3<QlG+<UX#L#CWcl#GI~}#K5kY#N@7+<Or^q#CWcl#K5kY#I9$B^%~@cNsi!(7ar|po9D?+`R2A$Z1X(XDc5e+-ZsyZo${pZm)hoevQswg=x3x(+32sI%{t}pHVwAT^JJ$ye|ds!o+qCvYaN`j(Lwj!DX)o}Wt->8PFeeyd7kW)>rCuon`g*w_|5BbZ1W7+4d;~}Y@27uZn#OE8Mb+b?1qhQItO>ddmhWQ%`;>-+&wkPHqVgVuo*l3Ou!ABHaEItGj{r!k{jOapJSV6q-TTmGf6kB@3o@8VRpg2alCDw*}CCj)fyD_(G5R!IIXD7v%&hAts6GFX`8!YW2@lbFuPzgcKR8z8{V~UvTdFryWv%@w71POWH<cLQ;lr%4A~8vHuXL0hD{&!9O8zLjT~s3XUJ~2)5T+K^9<Pyr}egN^9=cHuwH}Qu<7GwVyiP@5)T(RWfC7cW)hb=W)crOW)g=xW)lB9W)fREW)jn$F>4*1GKt|GGl_>CGl_>CGl_*<F^LsjF^Pp-F^Pd)F^TP6F^Pd)F^M@{G0A;gF^S1tG0A;gF^OHz3hQT*ZkWVEu9(DTu9(D%u9(EGXNC1MTQ^K%dsj?y4OdKZA6HCbJXcI&PFGA~U{_3Ha#u`p1XoOAJXcI&U{_3H*R#TU4RXUIM{vd2-&D@pvpFviD7)S!>_6c@l~uab+<^Y?NpD}czo7cO8G*P`-EG4D9Zh|<*w!*ozkLH=`U6Al?H%^|FaA8om$GWJy`#*~K&5#*>{`EmU}r3D<G*!xwy)gS8oq+1bpq=)fNyh?axFhf-QqvIX0mVb)S<g7%xf5U{*cdiq}(?JYkijg!&<X_$&Ks#clSsStgIIAD-YBCJ#OCTADlJZ_rf`k`_HeO8~Az54K`u_?w894-fLeiu&hOSAK^f&hLZz*_C4s=eIeHkkn0A>bpzzO0dm~{>2HAaH$eL9C;bhO{_1PBRM+x_`k1AzWrzA`t84i}eYDlJY~4qt=PsqEt?i?(>sQzHh3xEC*R?}-_N(jqLU#76>)IhZ2h??a+RmhIfYc3;x_(kOK<ZMR14QQl(K$eL4iKFKYFunJF22wh8P;RuQ{&<bjgetJMm{x0cF5ndl#lsB{$|*({Ifv$r!VBIhPAI2C|?c!x6i3RpV)YFR{i_B2aeUQa+;4(f2KaRDXp_V<J5@2`*$C-Beg^C3+n%UlCQUSo_lrhIQ4((=d_)la=*%Y_p(m@=W}NGBHc$+=Sb~S-=p^z^}XZQXZsGd`_W&_K7OK4AVR+a5w7cxG$&9S681;BXCv7^(*1s*+&lhF)0X&`J$)6u$9<9dMelK{C%wn1o{^5zd4TFq^a;>8ht4xpA2RL{=M$>4YTs7v+q%DWE~WPo9d|m`^qwN^1n3+^@4-kuL))SLOnsQnX>{&V=M<=O?9e$yb9<z^)c@&x7|9OQALtxNeS^-2s$T)sFFVw)qIDsXo^-yYJ{jq{q@B~&6gu}(U!wj)=ix}lsgKdQI!eEa{Eg1x)ZgeF9?4IrKSyel&i|3@K-W8Uf7$B(@`djAqOqoH2OW3n^K?C>{-*A=0(GzXLUU}<m_}Md)%@mH^P4X;zZI>gbbX}$6UpXut)zA!`kZEyNb53PTZw)Abd2bFO2>=d%hWz}J&k04y0%gqMp}z$U8-lKbw5)3bnT{N6lq*eTla}=BeWBU(2k#u7wuOh`$xL27e9OPvll;m@v|2{d-1auKYQ`B7e9OPvll;m@v|2{d-1auKYQ`B7e9OPvll;m@v|2{d-1auKYQ`B7e9OPvll;m@v|2{d-1auKYQ`B7e9OPvll;m@v|2{d-1auKYQ`B7e9OPvll;m@v|2{d-1auKYQ`B7e9OPvll;m@v|2{d-1auKmWfMKktoiuEu}9?}zneeOj)I-x=Ib*f}b=zcjviP~wI~_J&9Mmnf}fJF~(`-3FCI^Lxc4cOQw1Nw(g3#EwPk{`SjmR-)AQrc&D@oYeM-MQZ!TBDMWvk=owBmoF9UmzLVjT55Y}sqLrbg&WG+z1|u7A6acszAu~{wsVwC<)I_%!|ofoN7+l;HCCzhcOpvz1obj<a{eJZ+`f^WstyVspMI#lFP42hj`}*W%6HmV4c03zH!q40EA{y6da+9F2Tr6Ohre!Y8?)4Qaw4_AIFZ^<oJc($PNdbWc~&^7{WqM{<KRSUzi=Y8A3BlRUz|vNpPTzV7P&WmXO<JG=LsiL&o547D>Xkkk=l<oXVwh*M>uJ|H&XkxmfBxq+1LI;rS_|E`$lTNpi+-}xP2q_xM``!JDfD%8|kgT-ummUzux-mt-s#->#e`u`s=N~-ummUzux-mt-s#->#e`u`s=N~-ummUzux-mt-s#->#e`u`s=N~-ummUzux-mt-s#->#e`u`s=N~-ummUzux-mt-ois{sOdtmQV^hLJ#2JgDXJ5l`t9*a-lDr1HE7tlz~og9h8S0xDBeo1h@xkz%+OOO2Z6T0_Va_a0gU`+hG$_fxF>xs09zhJg5iT;Z3*@{O~C>f<5pJG=&%7TS$gi;X`;AjzR{!4+r5pH~`Jy7#xQ$pgDXG``}A>2`+`N;VbwATEG$54WGfYa4~!iAHiFY2_M5QcpG*?9e5qyfOjAr4#N(351xc1_yFd^AxMR}@DRKP4?+UG0*}FqkO<r0F4zxip&`5s8{s)<0{6oTcpjF+C9oG(K>#j-m2e{zzzq-w&%iD41k{IHVLChoGa&_@hAr?Y#KUIDhpmtYmEaLr2OFR<+zXRnJxqoQa33s#JD~wAg%Pj@hQax;8m@;$P!|?L7q}U^f(46V4qOXqFdO>7HP9Ps!vg3JQ=vLs4kKX-jDpH=HH?9AP!-0)AQ%rrpd3tu!7v;yfUBT2WJ4=B4~9Zd7zj0?J9K~n&<+^%0~@+QS;&I6&>7l;gv;OuNWv!gE2N_je}ZP%1%HOia3G$5e%KCwht@b2|9}k4N5sqV8Z3>2aS4{eTwH^{!DyU^f58mA0XZ(jJJ7;ga08x;cjH7Xhxg%gSP>t=Ls$d1;k#HHpTPI<LJZ(R+>h_$rT8)y;D@*i>*5Fa5x$9y@MC-m593a(hHv9r_!>6Gckoes9UsHW_y)d$FJMD_6(7PE@c}#^_uyXKhnL{<xDj8%O&Es<a1uU?7vluH3wPt4SP%WU4xhyOxE>ed(|9XZ$7k?%+>W(yC0>U+@LH^jkK>KF6)WNOI2|9xtFZz;h;#6MERS<>6mG^bcoA;F)p#$~!Bsc{@4;axa4jyw<yaG!;!wN|vytHnT!4$P3eLyAcr*6Kzu_jFhO_VjoQlnHCbq<1U^b4&DcAtVVOz|@Hh3OR#*UbS=U{v6kHc{QN*sw-;8j=(uf%RR2zwyl5bTb9@E_=kiP#Gh@D%jKR@fQKqK#?T2~+S#=z#H<g?~a*OvX%1#gotiKfyRwi+zokux9LYtjn6SFR%sc%s#~qEQNi8iR?=DEndn-uoKvx<+0zeJDbP;z<%szb_55qiR>7TW>>SHa4Nfj{epAYa`qSA!iF$lE7*3%*;@82E5p{a{p>t;KYNK)WLsGQdz!t>s<CI-!|Wh?h+V)Auvge~tOk3PZD!B22UuzLB71@DW;NM9b}!q*)-lQUGCzBQRc8Tq7kiSeVSnQ`_BeZrRb@Na?QAEzgH>R=*iiNutIP(o#q3eGh?QfHuw`r$E6;9Yv)L9lmz~2NWDD7S>|Ay|%V!(e6jq9DVAI(>Ot5Ke6uX;^WQ^U(#<P_S*#tI#tzuWON^CW|i7jR4vm04owuJR&KjW=z0lSu!W%F52b`9&re#Gn8WHyUgY!Yk7X0kTyIL=_XY%Kc+b66ubhBaYd;W##k4QEx@RV<keV@d23X0vp5Ir|+`Sx44~bz&#6KkLG}vS0Bsmc_a;ANv7&Fq^ey-(yQwpS5Q7*mu~9C9q8PC&se|EQ4LdKEpIthc#tKu{OJqHDnjFFR?LujaA_1^0!%4UYEbYF5r#$o2)U<<cC-qzlguf>hsI^d#oDo%RgnQd>B8%Y(9~H%R2Cx{2kVr58)rMfqW$YoaOMV`B!W_zm^|kb9fK_1G|pj$A4nC^2hie>^A;1KgCw^ot*P~_``e)e}<Rl5AwTt0l$m?!*+2$-_FbM0AIy-@HPB5_9TCTKg!GUr}$F7jW6RT+2i~Xem_5lZ{>^mCVn$N&ern{d^0b_H}Zx20e%B#{2|_xuj7(;=d<~}d=>}3mM`FUaOBtUaeOtOz<+0V@~M0U|BFrIBlzunIRBL`=cD)%{xi$v1NbexKmU;};)D40`~(}!JMkNN7cTfsd<LJ-|7O#9J3f!M;a{-1d@`TH|74SRE1t(&^Uqj5&*o$KFKj4J;bV9b|A>v|{rHvqdv-am!LQ)8_*?8M-i`O+7VpY0<h^+u|Bm(Im+<!d8+I{I=WTfg|B`j&&3Q}yHEY3}@+{trf5Ln`o+tB<SrcBKC-QRqLzckn@rL{;tHZ1COL-;!I%~ks=e7C!>^xqPSLc=aVOEpx=1ly>U*x641!6D%hu09#@tUHcc$PO1mBfBtUbGM|@zSE5IK(d&y~R5`UJMcM@iZ|;?BkiDhd97Hi~iybez_Pa-r|GA6!8HcFMQ$?o-bC2&-q-jPJGL+5nIG}{Ce?#_=ztOcZ=2HLGc^EQ`{mR7K_FA{2}p(xKI4Sw~8CZMsc$^!Z(Tg#l7NBzFEu{>%{``CEp;{ik0Gbevg<f?hrG@NBlOiT&xnm^4rB!u|`}ie&lzFR$`er$!#%CEEQwL5Byd!S==B_@H}yqxJe8a-|$5uM_eb4@m$eYEEIjj*Zf*BK+F?g@P49`m?Juh&-g6SO-vJ?^6nx-Oc%|?&wPd$EhdTMe3VEL6Gf7ElTQ%YVz@ZUhl&I-OeBie`3TWVTq(ZdJ;g=h3K1t>;R8hnahdp-w-;qZ7jdq5fp-;IqOJIaw-gmc8&N@g$Xko5B2~Q0D~n4+vba<n=INr5Xd>R`jYVzIRMZu(@n)iqxKO;xYY7zf1&D*Zo+u}(i}(5Y!V=Yl5PNtP@i#wDyv$E=F3u5BJkQIDN5zlgn0QkBD*h3Vi|<7lxm}c%)#YQNiWKr`fwHmODSi_v@>x+?wvqcp9oa*^BpS#o<Wr)d^vPW!Q+AYlMSIy_z972E;qrhOB%8_C#0Ytvd_zo-%jA0^Pp+09ifM9<{9MeFx5%61o$`oSB<IMx<!t$}xJ#~;E9AH09ywj!E@#Sj#2s>_Tq=)>RdSNNO-`1F#d3M8yk34ImdJ7P202E)BCe6w${Xd^Vxi2DH_MUoGqG4E$OZCC5ihTj^W~ND6ERn2%d6$5VwmhIXUOjIT`@~uF7xFFqMvLhr^>eSZ81f5k`v{dqJzwk<7K*hU5u4kGFKiFw!Bo1l8xjSVzeA6hsuw{0C|xdBID$9VzBHb`^fi2Pgzg)mi6Tx(O0&Xm&vz8D_Kc)krkw0be3tdg?v?{%0EPN`ImS?w3JO{viwRkkz6K8CJ%~4SxR0k_X{bj$_r&R`MkJ9){wR2i=w7HPu7+f$lao@JYQCn0dcN8A<D}iM1d$LL7pRD7JrLhL}~f6*d{D_T$~cmi0{Nt;&*XU>=1v7{{<z<uF?', 'farming-angular-open-spout-watering-can-01': 'c-rk+TW}P|x&C9Dt1)1}7;znziv+C1%<Sy!u2`*%1OkDO0CB)JV0pAVk|tj5$g{fwLWpI@PMnhqb}q-pxtm;G^OCAmDh_r0oIJZKZ>Q?Ko%3*Ba-PrEJ=?oItDU{bxK33n+M18Ad;b3W|Ns7{r@M#Q{FRX>i0D5vL@#V1IyX5nem7zji*_l}e>XB~7i`Zexn86{a(>Qp3vN-FMH6KxZx?d5r;Hw-P!^58Sf7!IL?er~S9IJ0g!Mi(axWSwW}zU`uU1$w(trJKq+rdXE;7mQMI!|_$8W@L-n&^V-Hq6{OP*C^R%G4z1-D=qN>iSjXH6#xwsLC@T*<qIS;cdT4*n^=UbZ~Dw`gZeFhVKKIoa2g;(}W)olr`*T&3idZN*)%3kqy6Dpnzf3%ulbHdvvYw>-sj-I7wYtx{AexJu3`X5B&o8tt4?Do>+ZE1xg+G2iCx;v9Fa;?Ff^&}bo>cM5iHlG`%mdiEqU0P-yzVwHKj<eS)Aau*a2{aS@tZr7rXG08`jnQ}g_%;a6y;|{>Ol2a(V<)Tt_auxHGTTW?CvC!UvtW$8HblS5D**Rsw^-740=ay&Z@UN}RU{FiEndFofbZP<y4Y{|kaucpW_awTy2u<y|RkhGXe$3fc4#qgSSzDR)oCU=}#L77~e$y_jE-!e_>|9C7+q3=<@!D!^D&Ba`eD91HDS0^bI?F3P4)G4pLLcm6MrY@oe9p6xs@K)17S)k?H9vUzPdPbgnX$Zi*w$MahF(54Jg0hZStZ+J_p(-@SJjZoJeE^A$MZ7~&3j)$b+KfXob1%1Q!HEgDYuZn6X|EU7>&5_)hSHntWtR%(tb+&BaJb(;2x{Mzb_A{C;ZeEd4Pz_mkUl7s#)r@v1em@oZD7OjY`Za(dMCoIUav<r`Wi7Ru+$W<nE1#m9rK~&Z2!I(yz=|`Jx?FZusL_bXX4!>s@b(Kd!->cd~iAIF+*tu2T%^vkUN+SKWvVzcf5{dh$ku)fX*hDOaQENmhdl#i;QbLn=?rqdUL-$molwPx;Lk9sAZ)-ns*)q+YM{Zg1XWxlu_8q~l3{99c&52lHBG5QnWogiSy5yo{E73d*_V>AcOdJtu}tOkS+<)HP(s5R!(4bz$1OV3+V5IoZqX>B4NslWE#2+QV+%^+phEHj!Re`wTP1|B^{Hkx~;{RPBqY{7=(Tx|-6HDHC;?YH%?#p=$}lh#OIjnONyX=u`VlUo2s2@uX(xczQiyK}{&G`hBW~8Pnrt@*aB(!W~3FrY@8*?Onkn(xH2B!Z#?UCE#Bw#r!jU|BRR#*EAy$XLW|}bS$1Q^+Yle;$F;mFJ-8)R6G`sH+0X`eWAD>(@Z^SwBg<<%X@7Ule^cUduqI5P(sxZ^hAP>Rot&L4Lye8it#Gny?Dw*&<!IQ;-B8wqlC^|>q%2nbv+et;gLVZ@szyc%ujdhRfC+=*&wN@z#y5a#$GgbAzq(zH~on^xDsgk=7blR?Hx8b`Hien$#bTWn%tF(6O*G?MkmI(3F8x&FPt31`wP#!Q^+}4CZpG$Y6#uC$->y)+pX=cW3{dgx$C&xwZ=LQ(_q##BxDUqS%cod_(m_dw(U+yAyegUHBIg}c8@R3tSs&oUC-A!U7ne-y{njedFZR}{wsGDU|n3(O;%Yh;02RZnYP>h!&7-qQ!zbd7>R^ohD{EM-~-Jv$6@d5-Vi0rXB{S4$-tx;PbO1%aG|EeEsR_}Jsjg}0ofC+wI|J*>y4Vns?9OESKChxpBy`Rd6|Y-a|1LpS&OAsH|Od8GaKS|HF^!2u{I3?-po~_4MUr?k2epM8B<$@%4{)Kh7_sFT&$~@O-((XXfsj`nyHmEOU2`Q%8YBK!GmY|l6XOx2?GIa5xqof+nY5{HV>X2Gg<{N)!YC>N;5o{{wu(U;l&33_~TjcaLZseRO1gqhpDHjt&MNmUTYq{<nrjjqM8PI0_2n5^qrDDhShBeI}p6={fdd18NQ2Vd2D&JjAA8Y>NRUxx8)V>wvI8o<<@L18EhVF(p*<Dh=KNcOf}l?etCNgbO+{R1nayvktOZhuc>M>*dEIdvxEMZwNILz_-~lW`oYum_RYugs&4dPPY2;^(B6!9;(opP8Xk#d_E(>S$}=D<V9z&J3d*}tqM^}oy8r3l|Mby=2bml9Kg~4bxCZWjTK*)A|Mf3_3FSghJ^$aHpETu6e;6mCjIcp)*0vpf|I^=B`)b5}zZ&ycELQDTaMrdJXY&7j=?_&sjX0AJ=gF#0!Tq+)IpovQSOmB<76C4eMJSiz8Oo(NgmNkVp<IeX9k2N)`JR^YGn7lY9m=JA3vem-0$j?I0GDzgz@;2$!jqExa!%F1r9p;&|DXJ$kN@`X8I&K<vOmABGnp{`%jySF|7TII(>WO4S5q5W=nVMsIQwm(Gho}J)-qv!h5GwNj7vLlUTMw@b|BMfOxhWXRyi;jk^_%PzGbe4=JS{6DOv+uL+emlOY4E_=^1*GHqo=dXK6J(K^ti^a5JsKo%OU0xQ(8NL>KJ>?t;`t+Ce*kJ0Z1!w$dKp9@<X(C_)E;2k9_cY@_|a{j?V?577bO0kqyh3Uvd!(Rv*$IRZRF$LMM5B^9XB7Fc$aqQEHnUyc5b1CLV=Jx9AK28@x3o>FuIcmlm`qc|mjN%Xc0z4Qb7Nr%=WGyoi+7oc&FhJZuR+5>H;fTt);Cn-axfv0I0cZO&LI0Ajg(f%y(ETsA<K?cwu4N|9R6gWy}V8MAB2adyvI9i<po`V%SdcOd?fYxUqIRTuYG5W*aRXpd|T-u7`-4NjW-ubUj>N%6I=j%Uvm==1PaY;``>Nk`NdGStR_04$A{v}Dza_-v@&SgD~Idb^3hXF2PBI=pHl1xT$W@k-)DN~aP<3wlw<Bxxqx#&yOv%VymjNq)Vn*36xCKJYq@Lmq(qThNhY^diVHzYlodM@%o)H9pwxyXT<{L(Tmd}+oj>tvqKf=lb?Di?WMzpj?oy&`8CaalhbN5NT~1()p+T*ONBE4c7o=&$Kn3e;D4TJkY1`4!-jkD+T?$**Nx)?e{4E%}(1{0eZ%$F$^QTJkY1`Irv+RUP*MX<izT=Ar->K33|*Gd>`E^y`;GxvanP%nnG;;DGcj1h|y{15%z3NI5(pd=y-+ujFk;nv<9D%A6L;rMY(*m-J+$wgE0=q&apOujyHm+J<vkUiPIj*9EvVe`cilGb83tp{JgU7|J>;^IL#Rb7n@GGc#h&6gnI8>bw`qrFk#FrMWJ^rFk#FgZZ$W*RRuRYt#BQYODG%J@xgC_8sBt;V)i3%-%*aVZ75=h1u3BX8+%PHPYLTOndvv$1hXwSEKsJmCsG%7<Rwec(n1nt;FAd`uLCMWB9(iwM>{#UxZ9pESuIp>U^A9>Ky!H^*5X+J2^91L49L;zC=&bD&Q(wgVJhR%TH0((G#?uo(4WmPocDyHUKy9)02&~3AhP&o<YrK;AVb)vW2z+x8lxow1c{UU9=N-Hq-M!c6PFbw$m=)E=WB|yJ;_QFM56oy7mG0(H^i(qyQC^HbHJba6d{rp)CT8&;iu$qJzMLxU-uMQ8%y~n)aYg53q+0gDG?bcmyQ{az}wjQ91w($AHHuirRzJ3+%<6L;Q5)5Uy_OqZq}3anhivhYX-WDnFx10+YDY16>IqJ4G@1xs8b{iQ1#o5A4UCC_kr(;u?fRhSI<^q>iFTc6##yq}IUylfaWSjOY*1Dc~u@doA!Z@HAq)0XPC2K`eLBSsDe7A|9Jja|U<@(Om`q&jHUt(_Z*+9(W$5ZhmIdjq5zTiPJc6oW}U+(gbh<r6g>+2)u~WF}g&Pz)4tr0@hvzUdEka=)D5GLRVqsztA<{HQ0Cx_#*H{*m#z%(+%JaST{m1(aXS>VckjCaT9nGt<S-ZSAegebRJf{3Vao%G1y@NEt&$GplRSVN)zZi3(TT)iE=apoPl*0VU-QEapx-Z&H`u2fn{^_W#E@#*EQg4z}H~ii@-cE54)~Yfn1;qOJ73GJa8VCUV%*uzy)Z!37cLAzK+r>u&@X$qBI4YO286%VAE6vmQk999gDz4lyY>7?f~z=(kv{z4ZMvz4)lHn_!YVbE5Ax_0N;R(U!%M9Ch$#KLg@{93-}i7T|&*<z_;n^D7{7R0N;VVUq{V1f#0NWz>{y$w}Ib=H+kHB7x*r``3CNO2lyTOSM<6--vxdbJ>RA8(S6{3=zbIU9`HTrdmH#Z@O`v%q3!#?@6!)adY^s(`~fsA!2cfse*{h6qkp3hfFD4|ec*?{5252d-~-?TwEH16d<6Um@pvCKKL-97nqEgFe+v95G<k^K&w)RupFrc!=oi3WKwk-Q{3Y<0xbp#OJ_dda-DSk_A@CvYe2AJ~0e=PEx6sRPfWJZ17ZL4W1Ah&v2e|uN;BV2heEwF?<@3X4T%4`RT<jkOm(L;PGe#jJ_O|t0+GBnq_K(fD*jLtb`CP8i8J)~qee;#hni_HupL*Wxd#)_gh|6bOBF=&fn`JJ17kcFLE9tx_^n0sx*3^(oeg(K>b5kC6_9g2SXIzqB0WSHNmV8VH&v{5bQ>t<)heNrPhXEcur&<c=6z3uJT-X!FrCbegDOUr${wzywEBck5uj={C=UErEx2_M<zhareHr9=UpTEAXb!i7O?W|+lmRZRfeXzrGn@63?w0pkM*15-H^0A$>j#fUlTi?k!SeVS`sc+4n!rFNa{~o-Ke}`QUT+i3f>-k>g8SHabW4*iuxCQsu0Jj0R;XeB+ydAh5Qcqyr-39EzzG5xki>$@fg;n=1>>hUD+J{=gF5+oi3U)Dju#<Qa*DCzjm*Q2pHeol!_9h!~J&RvAb_>tq+KM0BJ#5AG99HgZH}E{Jo#?F#yM^7jj$`${A1n90xD51g0J{qXmxi8H>@4=+I*4BaJBow24x^_eb`ytib>r8MReLwC9{kuUz6aM4Xk~km<9t67g{~p~b(nokj$>DI3|Aj&O|0fMTtn#T1+3szTnYR}u&PhsN};E-ShXi{_2b7@@$B313H&Z#rG5gJ{|)*Q@DkSl8SEP_123b*zBNw*Cs8_s@)&Ro`+-X+j|17><Z@+we-WjjSM5JxzUS}FW?Xy=XvNw4s~P|7;qThw>>bpMi}zG3&d%7Iapq$So|fVe%B46o<rN=8xfF+{yy9ahm*UWr3m?OHeH`lf3eWR9IJ;i4%-~~^dDQuPr>!}BrDukZ9+S-AW0G0H+M_137IQf}1zXGi7ZE!V+s043*m>4Ql%D7RXJ`*Up<?s&PF#oaJA%3OFrUc}<J!sJO8yzwZoGZgVRm25{~r;1GaUjR!dqnn-WlD%Zp`VM@qRc4JchY@3*HmGKz2^G9q+I%U>D|U!aHXdko^y&{{#041)%', 'farming-d-loop-handled-planting-dibber-01': 'c-qZcYmgjQbv~A?m*vOm;kV^9V-ODBT}^k-qeoh)EomiLu+j?eVq2EPxOb*^x1-tVaZisP5$h+$0-Tt)0h<u8F|QyS%)`LWPKd3<!Eu0KVhlK`N-9+;{<-iUQ&5%f-kILLGkd$IS3gpyYR~!h&Uel|=iGDe?VZ*{X>|7zBJvHQ)9Z=eIWoNeRKluOZ9lR3RARy|+n(jSUSf0NU6Y<$cB{$+Oq3lZyIizAW$&h8<yfj;?@whDy@_MCS9RPn$Xb6gG2NS}7T_SUIoU$h#O6b%5@l-&V~G*|S#P537WoJIk?AAzznx0hCw$MUvM37fRK+dZWk2t^C1yHYwv|H3t=dJ!b|xnMzN%9Mo^+>Nf714yg5rC%a>4R3IA!}*N%5VEa@_GJ6-ya+%8qX<W2IWzSA5%>a>^i#TLpWI!e%Pj__S83AiJt<`HEXss*~2Z->Z~erBL&Ir#zw9#R*$+Jw#zSQ<%lAusR|4ewOx>U7h4vw^H4~<{B>e)`W|>MlF!-;yxDGs8fMK_hj8NrmeZPYAgIcf6^%&MMbO1U?0M(Aco^EYFAb~#Mi4h<wB`eWT9G0)h#(irQ{w*N@JeGLbu9Ae1PSxIc2+aQt`34wTa0-<WYt#R$UoXSe$;%LtT)0)wc>qF-y^@BAT*YV8tD?ysD6~I+yXzxqye^ad60WE4L!NJzl(gOD?N1Us|>>ez4lD6#05I*K=;g#!FZ$WZKNlKkm+d<W?%pUcm><U6m&^=@hvy7isxyEnT#4$*KtXXmj}tA)vVhWSNYx5O^wuNvBlwY;^shWUtz*p^4|S<2xzu6yajrVy!mOSL`dH8hw)pvt$?hDkY1R3ggb$nC<l?RqTmzY&Ab$bUc)~xuN<FVi;?H=FT5;sx_;Wcgv-diOuMAyEox_&V*CW7cIXw1@>I(gUSR-&PyVevspk^t*U~u-M%%sMH#P^O5nFTVQ%pkmJ?;<Zus`7A}o)e1$ow_o>joXkvMfYVHK^4?;NuaCpM$#rK;Vl9BwXl)nWNc$6YVa4}kU$PZkho9*gBV)pmb&8Cmn8!-<^-cMk0uIh<hQRg1;S-Kd(uMv#_m75PX?_&q;`>6-St_ujT^uxWnGv5)6V)=4BK%zB7Vdt{pRN2@K+tGu^wYA)u1)>;norA)B%Yzl{v=fIGkX+^g-R<cLfX%(zo%M%WQ{Jt9Y)QE4}B^0$X=J6Av<P>gZ3&Qp~>!>lSYVUMQuD2VdW(V`3WWTN_**{fRRXwSxM!GlIpGxNVzf4Ngvzn^2A-y@2&8TTZO=-O<3$Qgw;4ayp)wnm!$f!w8%cZfvK>+ilRF=Cka#~hZGkPvH&Gtfger)IG_qZk0lWm_xCYaWmfvdWa%Vv`-Kg~#W=9kPhhYTZ`%_Xy{JU?kV*;WN%rl*XI-X$BBLVj1dIN@1Nd6Btfn&nNVvKd3qsu={XXIVySw)ugYH4IhH>8VA;Z>UXMO*c|lf1^wM{PfBX+IHm}7DLu;YC7E<RC8J~r{&mcq??JV$*g7=dM24!%zC7!`R>6n-2T)MeU%~+&zW-Axzn_=eBX1%u&;PF2Zl%Xj_w`a&u85~eDl8TL%6iCot<*gDKL&Uzhgm~KElcv<4TJ?uRcF-N}M+>&a1Ln!#rf>J!C}>hUh_Si#+7=iXC)LC{|LOQ&q)D^{B8_O>m;OIZ1U!j)k`h_^j%B&A`TL<Kwn>3r=Oea&wOiqbDoKFRf}BHi*W+FG=R@1aDNdXlqww3=M6WR9RbUMsv`>$&tzG{47apDe+)ro#(I%y-)6hpEX)qY<QUXJetHUyLRgQ!9a{!?H+ZMxh6B$=gf1NIrEX7+lRK_yug7TJ-?=<gtBE)ZP$dnYAB7WH_L{jIGe(--d4ATUYL!f)KQ72V#FO~pN=kEN+^6t<ucI`{D0L=W)qcowrki?)<$&My0%*`dUjnqhfONkanYOf9IB=!y9XX=uXgD-qg&-vEjj|#_){&N-aYV0`_!UKhlu7qh&KhlCB{zr_7MI+@bQOSCfOPo9v|mlZLn=`c@qrksa!^zkEXjVABby>inm*<TBo@lVU9&HI_!1kG4AvW?Ndo(5#i?+B#)=o_~EBICeLO%t+mBiv!~_wmDf70GpYEI<2kz1JiCa=7nmDrW-(>YbXccTi-=uQJIynxMNGcX+(>86J$C#_rFF(Ww{u&&Ry0>L2A%;GMfvG<L_7BGr~X@B{=s9H4Gf&wbMLkYytx~m@z)Iy{ykBtZ;ik+-SAVlU%BPJ|JuWShT%8<I6C02y?+bihhfGi_ue^M8D{(^AANoxu$5t!<L^cvoXb~+S&lpI_@99wUm0fg6l|rK)j_b8V#NPLAr~n|{4+u>Qq1^5ZKas;h1yCnTelr|*qk5WV7&S79+Sx*-+Fgr_Y)u6`gAeXU_Y<-eJzS(N;r*k;7I2ZZC@|n&F6k9dAiL{3{K$3jNvDW6Xb3Rd6^-3MR7X)G-CLXaZGU>F*ic;>c%m}`gidY#W6+x3Ob+8qYG#SWDi|L%V;I^GP<1B)5Wv~`eNEZSJ67U40;_U=+Ed%x(516x}M%f3S9@S&?f4ojr8Zx8)-Eyp&O_l`UXm3mZgwO=|ad0X)WYhx&rbFx)$<UdMo5x=^c>o0Czd9B9$(IR_Rh`m9B<X=`GMIy&YPmK4=xZKFDXUeW1=VS$}55YzN*d!)KKw$7cH4C|vJ`*<9=l3FZ~>RvBjg84l(O!S!x9$c5;}P#okEg@f3la1dJ*{@;i1<36*07z)MXv%MT&@yJb~nDLp<z*dGCpW(n(h6mrQai3>S91O*eJez3ZR}X|@#%DeQTN!42j$5`e{K|WeaGxLfeK8cje&<?_?>=^0C}w=-Gq9Cm#%DONmElKr3~--M_PC*V<E3x%XN)f;@}ZdVna{vhh8dsXz*dIM->&2He)rbnq4<qwp5ybr@3CSiW_;!|u$5uPXE?BxVejmV+~>RRnhwR)mp;Jp#xs+lnDLp<z*dGCpW(n(hRe?lbDzI|{GL#J`p#7xe|FQ+P|WzuXJ9MCjL&djE5pIff#;L1SY26)#C(sm_)%EocVfgpBh*BS5&w)(6DekVp(awy_(Dyj80$MD^o$f^eP@K8kz&RddPa&FU+5VrM*r7^Jtf8H{~2LVNipLKdrFEKU)WPpjPs!`oH<gA^I=9fbEKH@g)>Kr8DBVaq!{OCT{x4a80TkQIFqHA@r5&4iWy%xlcgB<OI^6Lq!{;0UAVKPnDK=>ONtp^xU-}f_itUe)1?^qZ(X?4rI_)BJ6(zyU%1nyIC#cuJ*!A@@SGNfgJ-rV96WbLVe#*PdENf^LHjfJg3m&1rJN2w!S4&^HDk<c#+Wz6PxJGKp1+HapMK_rdIYD@;%p6zvx^@yh9Ca>hu-u#_uj`pG28C5jnimxwzd15pR0=>Gln1jyLQ&%+=;`l&x$@fIE@x(o9I)VtBW5qh9Ca>1OL5?bM?tYL-g6fX|y<|=u@1liyt$FpSjNhuIRIaGZ(w)Q=F@dA2WuZw)j}QqR$S_Y_KMxPjRj;e#{tt+SZS)r|7eTGaK}*=u@1liyt$FpSJ#H{Vw|K;M9XXE&3Ga>f*<Y;b%cS0>2T$F-4zY@ksobG5mDq-VkCAjYr7c49Q*Q$Bf~pvo{*Tnl?gu%oKXV4CxJ-A2WuZ&b`wRdcF~|2Tft`m?3*d=EscTr}J!S2xmeg<cu<fv&9TKTV#IB7=Aj>-iB~y&W4=frf~Ld3psmbe#{ttI`5`g;ZB(ix#PA8chk0zyGiE9jNzyA?w%Fy+<M3}z&7FT-Wqau%lw!z{B%Cs)We=h+HJc&+tgz`BenTiM(lsYuY@MLfG(s<ATOb{bTOSzD`*Y$3jSU068@d;5-_f!4UikaT1uDEHIUcPMf_Xc<<tYcoUS7U7MDY>2b+DXdlh~*(4~~1>mjeFtLX-M8~+CP21xeZFZ&*N6XZtHC=Hp0#apPKQjjTnJ7r1b-|}W5w~zsgP0+nyZ=>yy+hNg1o9RZ#8%d{~w3U*SflksM8id6bXanqb(mu$2u*lJF8iE`mlZI(84bTqg0UDtLu-F4V2=*;>5b_`_cG1mr8{}>DE;>Z-p_^zw^i7nf!>|~EJ^=O@*^o9Y-c9eNB4m+nr3tcVlx~L}rK2<ni#+sUu*-BO<ejiMLVrOO$O;vxN>g+PjYHo-$H|AqQRqpq|B|L5r(xkxjZQ(HBA4!_lT;!Px<vQWJ+L?q?SuUR`XJ;7VR4M^r3WD&r1#N>=>2qp?t(r+57R@ixF7l+us=qhg#08d?xVk=k3)W(PSdC8BlG}$82SNvls*lMhoK(=`)}wAkY9ksU(;vk^N^pXPtX_XG5RPy0{v0?GCcu{N1;Cr_Sfhekl%pCXX#7yb;z&N-_jZS3Vn_qhyENrLr=rv%g|4N{ayM#<o99mBz=><2l+kvJNf~Ao4!g<L4TDRGy{ugpq~c&ALuOPSy+6F>hv7sbM!3zBmF&nhkgkC9eR;ofJFm(2JC;OpF#c%7PIuv^b^RR(DU?f^e^-y`X}fg(JS;aEMA0u0qkGVYml$O;>Yw0`ZeUQ>8JD`^h<h)eh&Q-b`!zk73i12z5u)FSNM62{+-UF)sU;{H?)pc(W~^I(63U&dk5)zfsl7G5%@gpQuZEY2}Qi~jeK9s=Iy{UGTiN5u*eB;)H`316T}epZdc?4u|>VZ6*;ZBBHz`DoB&6?lNCAhYu7xZ-#9<rU_YH_KE}*Nj?ejN=gjv(mvJ-hxcGZJC)RkQ+ju)?{x0h>-iSMXKELmlL$mvCCHBNJ=%u*LF2asn4ZR9`at&^{i=i*X4YwY*+FIxy++tVY_PQMUQrvSJaN}Lg?>+YJ^BUY`D<He=sW|&3Y+r=+e^{S~^>bL?2K_1ip8<wro;i&WZ2l>a_Ym<n*XN-ldho-ZVV3iE*elT&J^Y!dhj&8{ehA&O6y3p|n$}>wmqD)L&q=GH*Pw@1L$Y34!+UBC{U01f_Bs'}
PALETTE=[];MATERIAL_LOOKUP={};ORIGINAL={};PLACEMENT_RECORDS=[]
def decode_asset(asset_key):
 raw=zlib.decompress(base64.b85decode(ENCODED[asset_key]));assert len(raw)==LOCK[asset_key]['bytes']and hashlib.sha256(raw).hexdigest()==LOCK[asset_key]['sha256'];assert raw[:4]==b'glTF';offset=12;chunks={}
 while offset<len(raw):n,k=struct.unpack_from('<II',raw,offset);chunks[k]=raw[offset+8:offset+8+n];offset+=8+n
 d=json.loads(chunks[0x4e4f534a]);binary=chunks[0x004e4942];assert d['asset']['version']=='2.0'and not d.get('skins')and not d.get('animations')and not d.get('textures');mapping=[]
 for m in d['materials']:
  assert set(m)<={'name','doubleSided','pbrMetallicRoughness'}and m.get('doubleSided',False)is True;p=m['pbrMetallicRoughness'];assert set(p)<={'baseColorFactor','metallicFactor','roughnessFactor'}and len(p['baseColorFactor'])==4 and p['baseColorFactor'][3]==1
  value=(m['name'],tuple(p['baseColorFactor']),p.get('roughnessFactor',1),p.get('metallicFactor',1));key=json.dumps(value)
  if key not in MATERIAL_LOOKUP:MATERIAL_LOOKUP[key]=len(PALETTE);PALETTE.append(value)
  mapping.append(MATERIAL_LOOKUP[key])
 def accessor(i):
  a=d['accessors'][i];assert not a.get('sparse')and not a.get('normalized');v=d['bufferViews'][a['bufferView']];assert v.get('buffer',0)==0;fmt={5121:'B',5123:'H',5125:'I',5126:'f'}[a['componentType']];count={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']];size=struct.calcsize('<'+fmt*count);stride=v.get('byteStride',size);start=v.get('byteOffset',0)+a.get('byteOffset',0);assert start+(a['count']-1)*stride+size<=len(binary)
  return[struct.unpack_from('<'+fmt*count,binary,start+j*stride)for j in range(a['count'])]
 used=[];parts={}
 for node in d['nodes']:
  assert not any(k in node for k in['matrix','translation','rotation','scale']),('Nonidentity source requires an explicit different decoder',asset_key,node.get('name'))
  if'mesh'not in node:continue
  mi=node['mesh'];used.append(mi);m=Mesh()
  for pr in d['meshes'][mi]['primitives']:
   assert pr.get('mode',4)==4;vv=accessor(pr['attributes']['POSITION']);ii=[x[0]for x in accessor(pr['indices'])];assert len(ii)%3==0
   for k in range(0,len(ii),3):m.tri([(vv[i][0],-vv[i][2],vv[i][1])for i in ii[k:k+3]],mapping[pr['material']])
  parts[node['name']]=dict(vertices=m.v,faces=m.f,face_materials=m.fm,material=m.fm[0],role='Complete retained source mesh, including every actual GLB triangle and per-face constant PBR.')
 assert sorted(used)==list(range(len(d['meshes']))),('All source meshes must be used once',asset_key);return parts
for asset_key in LOCK:ORIGINAL[asset_key]=decode_asset(asset_key)

COLD='farming-fixed-open-single-sash-cold-frame-01';TRAY='village-seedling-tray-01';CAN='farming-angular-open-spout-watering-can-01';DIBBER='farming-d-loop-handled-planting-dibber-01'
GROUND=.08
fv=ORIGINAL[COLD]['WholeOpenCentreGroundFooting']['vertices'];FCY=(min(p[1]for p in fv)+max(p[1]for p in fv))/2
placements=[('open_cold_frame',COLD,(.28,.45,GROUND)),('whole_seedling_tray',TRAY,(.28,.45+FCY,GROUND)),('empty_watering_can',CAN,(-.67,.05,GROUND)),('laid_flat_dibber',DIBBER,(.30,-.80,GROUND))]
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[add(p,t)for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values())))
mi=len(PALETTE);PALETTE.append(('SceneOnly_DryPreparedGround',(.30,.32,.245,1),.95,0))
v=[(x,y,z)for z in[0,GROUND]for y in[-1.10,1.10]for x in[-1.10,1.10]];f=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];emit('SceneOnly_ContinuousGround',v,f,mi,'One new scene-only support slab, not a separately counted reusable model.');FEET=['SceneOnly_ContinuousGround']
def layout_bounds(v):return[[min(p[i]for p in v),max(p[i]for p in v)]for i in range(3)]
def layout_validate(vertices):
 assert set(vertices)==set(G)
 bb={instance:layout_bounds([p for n,g in G.items()if g.get('instance_id')==instance for p in vertices[n]])for instance,_,_ in placements}
 for box in bb.values():
  assert abs(box[2][0]-GROUND)<2e-7
  assert all(-1.10<box[i][0]<box[i][1]<1.10 for i in[0,1])
 tray=bb['whole_seedling_tray'];assert .28-.455<tray[0][0]<tray[0][1]<.28+.455 and .45+FCY-.305<tray[1][0]<tray[1][1]<.45+FCY+.305 and tray[2][1]<GROUND+.25
 # Clear of the full imported instance bounds, not just sampled centre points.
 strip=[[-.43,.90],[-.50,0],[GROUND+.0001,1.50]]
 assert all(any(b[i][1]<strip[i][0]or b[i][0]>strip[i][1]for i in range(3))for b in bb.values())
 return dict(instance_bounds_m=bb,all_four_whole_instances_grounded=True,complete_seedling_tray_inside_true_cold_frame_footing_hole=True,front_empty_work_strip_m=strip,strip_clear_of_all_complete_instance_bounds=True,scope='Simple full bounds checks of fixed current arrangement, no navigation/human fit or continuous accessible-use guarantee.')
LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate(vertices);result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,.40);ORTHO=3.50;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(4,-6,4.6),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
root=bpy.data.objects.new('OneTwoStoneHandQuern',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole horizontal bounds centre; whole lower stone ground face at Z0; static quern display only';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert abs(lo[2])<1e-7 and triangles<=4000
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
  files[role]={'path':f'assets/farming/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'scenes','assetKind':'scene','theme':'farming','style':'warm-handcrafted-village','title':TITLE,'description':DESCRIPTION,
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
