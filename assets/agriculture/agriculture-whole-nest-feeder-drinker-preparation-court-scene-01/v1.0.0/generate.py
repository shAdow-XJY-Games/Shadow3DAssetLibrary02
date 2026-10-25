"""Original complete horse feeding/watering court display, three whole existing models and zero new reusable models. Lightweight maker SELF_REVIEW; static composition only."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='agriculture-whole-nest-feeder-drinker-preparation-court-scene-01';VERSION='1.0.0';TITLE='Whole Nest Feeder and Drinker Preparation Court'
DESCRIPTION='One static poultry-equipment preparation court scene, zero new reusable models. Three entire qualified unit-scale originals stand on a single finite scene-only ground floor: the raised sloped laying-nest chamber and external collection trough at rear left, the complete high storage hopper and low treadle-feed channel at rear right, and the complete bell-reservoir drinking tray in a distinct left-front bay. Both high apparatus fronts face an empty common approach strip, while the low drinker remains visually separate. Every original oriented world triangle and per-face constant opaque PBR is retained, with only whole translations and explicit float32 storage. Node hierarchy and normals are baked/recomputed, not original GLB bytes. No parts extracted, no recoloring or rescaling, no extra animal or duplicate equipment. One scene zero new models. Static illustrative equipment arrangement only; no actual feeding, egg movement, water supply, linkage travel, animal accommodation, hygiene, access, structural safety or husbandry suitability claim.'
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
LOCK={'agriculture-fixed-sloped-nest-and-front-collection-trough-01': {'bytes': 30304, 'sha256': '491c10316ac8f5db291656e1911eb7869f06c1030b7e971f1be56d2f91414854'}, 'agriculture-fixed-high-hopper-treadle-and-open-trough-feeder-01': {'bytes': 49280, 'sha256': '9630b35363cc614f632b51041d03f562077e57a758a29baf68894d5417271c7b'}, 'farming-fixed-bell-reservoir-poultry-drinker-01': {'bytes': 63744, 'sha256': 'd2a085fa82664760e0b198a0b65a9554e5e25633a3370590e3cf0229a58f8dee'}}
ENCODED={'agriculture-fixed-sloped-nest-and-front-collection-trough-01': 'c-rk-dw^S2ng24hrEmHe+R_&x1zJjGn)|+K>AkemCl-cI!Gg4u%;e5YAd?J9rVnc6q1A;|K+$zAK41Y+SL({Dpl*{Dl$Eu(tD<#R(M5EX<>7;ZD2v_ioSU1Ro5{I3X{!5Ad&$RdPQLTK&pF?@oercgTh|5v*X#s%x)b1{E!~&wjU@7Urx01bH!|R4oLr)i%|(_+-ZGfWX0rM408R<7PCJ>TlM8QL)*ardb}F5!5s5~2I=Or*n?Yu|GZxtwjpX}KKxBEWjPjA?SM7~t5<@r^*+RdIMl#tX{X){V@7rGeac{)gUC1T!#Eib|&~P^6WC}ZS*)*BEbrAm_?oaJ@lHtK@E_FjTQ%I!4gQ?7b6Yfpqa!xuL&KDAeRA2boY${U-qcA6z%I3n^OnMJ7ZOF+FQp?KbP?25PblT}df4j2i%LXEDHI;@l1Pm$+ruwc6V`Rd+66tifFP+Uh`EbtZb5bZS+&7rWWSn$(SE?|W9Vwvw=`^YcrwaLSB9*IJC2_1;n@M&hhGTzOW8^?%Br#*C_GCEeIK!A9w2RnO)uH%xtU<OOCz0FgG6l--&N%2~A(eB&sZ1ZbfNJ_vnN$JmBb~*BV>w}^C5dnSx$KZ@1A0Hyi%}?KcO`Pka5}pSf1ovz!8+>me5_ii)>`NZy~N2E))7TwfyfV{PuX3lf+WGM;6x#u9d<I|L}mav62179m!1{jOg21}-I?gcZ_t_kkxX9!ml*NJt@gfjA~jUCQ}f%ojwt9!q%ipY+HR(XXmrrd${M=7qikLj{lM5~MzSOMaBsFy!1yMx;xN#e!ZMoZbZR&sC0-;Gx$DBi30#aQDxc04sz&QIMw8h+v{2E-E>~3(b<jV8^*)fxj-VxJXCT~%OLz~77-}6x<zDjp%V{fHVfd}sv>MG{Po->f2AYYNCqJJ`I&^)7bE!PhUoNvGrfn!u=o_RpNsKKUR%4J^V-Q&uTTo_`%i=i05wFosvmzW1qJLL;m!^x6C?iU9*=)ZX6j~%?L12_fNn)M{m_4v&Ywj*{po~pUBGZFn{`@hJYIfqD|M!}ZYPRE^zid%RH9K`r^Ho6x(@ufp9JktJDnFb~><K#qsM<-8y&;vsm^qb`if)04zQPD{59hMUkv?}P%x06do1av(OK(Y$9d%<mJ(5S03Mg&ufNLYhIi1Wo*s5F=i%L;BszlYO7S*Fh)QrZXSbUgzj5Yczso0fNeWJb5j#LtLBnEP+zL9icB<FO{oxH;hUI%tMg$~>YJ7|e_l#dhKwmS+Kse!?cn1qcF{c=YVvq8T@fgM-ku-mrm*qO?s$2(}dvb>NRaiS4ybg=w)Bol>^A><~5<u%6iK)oat`7oYNg`Bej!!(lfmLSP<9@+DBk9KGJ)4go;5m?#v(X<?G`gV{#KZhAX8}@FCB$A0?654H%<>CHBI`2fo+uY3OQ+PBC)E&>}cF;!8|K*-OG;T-I$z<`s@_pryg-?gJMY^u++O&4dwg?%|CrB|-F_LVOk-}ikNhIlr%KW@z2-Ugs*KNFF?HYIb&Xluj2bLc?#b~{Xs@=Yi6jr&MuyEaqqTwQEepj_e!1}<Yi$TI^v~x{nM|w&1C7q;~yRsZIa}6GZ>vH7hXk@rIcd>(MOQ-sJNM&H<&?@Uq<VmNM&8<sN9ayHFk{P3a3`vtU%}|Uej>XhC`J)@MWT>j9;#f@8D4%4QrliCbH7XGc%W6D<xV`2)jg_&^xJJbprl!h@Y{d7G#S-k!23+BLw&H4R(jC?HCZ@&pn5wH9S}rS8dtB8OO*5r<eGi-PrYz6UB^0O10^VFaf?Lq~oa1ENHmS)Jx#5fJ7(KLC;rUd{Chn4H(wU~F$5qqR6aklN_rK;`(p^(cGiJoG^w4@;a?49qVwxnW#38jN&`ssYSJmo1x}0!3_um#9T+h&_TxuvqTy&=;3WZ#%7n4aHyR>`D#>+N#UqX$zq`T+hRh#g%z~!C79=?z8$kjEBO#8Nzum;}2gf%KvjVh~AYfhsiu2HXQG@8-qyLJg{GppL-Ty0W4ZKJPH!b&AJkG@1oas$2mE0MT%Ca01wsgloYxsLX_cN=ldOl~D#awW4tc5Ci4;ws}+m2#|^dh%abgcZsXqfl-tx3!lPah*&?<))Tty?cqcT8&Yw^Ife|NIl1yPT62on$39HbDZg9>PLw+mCl~yO{c<?kRmtZWc@3HxMHS`6ki=FKF!KL`m!_8hu`J1Iag@!NPoYRdn@*&^qi{Po-W%njP_}gtdqf!3^v{d4c%_Hkuuy9IxZWMq$_dK1L}r*NGo_6>v4lNBITw7n=M7wbdy|bhEn7P)WMM<$LOGB#uY<1sSI}ndrDPNP3#9yMuA!vdF$FPg<h>#FQmp^1WlLgO;;+@C8aulOV_GRt9nLBP=XDRRWFPr2BzlgYe+|`Ycd_f{}j!PDKxZh`=je7>0LB7jGC;nZ4l{}G)eU}Y_uhGTOL(1u*udWr9l+c#!duH*Mg&{=#7G?iw3c70GbJ5{Un@#5E`w8&=ik=8h0&=Yl?2D3Le-}r{XRfRW^*crb<y#DdoOeHdVaU$hvPajuH{;G-wcGvWeZdEXOq>qqY%m5QBJYF_2<SlmW5W(5c0;iPun5Ax<deJD;K%x@?$+Z|RUk>#F}6(Y%wA)S{PitE)v)S}B&%7b1GS@((pC7F}~!p`@5`!-&zVwdB9YH40;kdydrdrXw}jbySlnH`h5c7MFG03&@RBSK_sMhHmnsSVw{u^PiW;5k#Z03xV^^;2@f6!yv|+IsZl%o<a8++@ak4E2dzTX<BgL+}+K;kQ)R_j<r^8veb;5s=M{-xNtNLw_n_#WjC*yjOzz?WSQjJebEw^bWKxKY@vK!$7rmu9WrC4LbtAR1EnZZ4CNos{w&KaMnP#U*)=&MXSXc-GcPwteXJADc=xTIqN}Qe$9*HGTij@5t%*~q=FBB0v*xxNxSFw{)yX!Y80FT2^t^`TJDKZ9kbT^mNfSSMrwQ~yZ!rc&6EPUQ(KT4)^=jpK*0|ZClkp~;tXZB-F7SGL#0gp9N{joPBDIw0rWSbJv^T%Ll@>QOrO~ElGJSxo`z{JHZA0C^Kd7b+;}A34(5Px$H*~htrSd8;a7!?BY+*^_%f%4GD8=Z_SdF_^8obY-vUsBqr~)no3TV(wsk%9;5kQ-&BG}gp^wmP|o`SQ<$qW?8ZyD&SJJ8+VPk-$Tzb_<m0|er_(B-N*jpxz<(b;nCY`n~w{^?54bP_k;bljMm&|W(oZz@f=PTpPkW@~yYwqq<}t=Jx~ja*aH6`8c#$3I<*sjW;mTFRRmYb9^0(o)`3wWYkNMl*S<wOxzVrY*>JymZ%2H=9sCdb-}sVwdz9*LArza!myu*GnrEuj}zvDqfG9tyH`r8?98lq3Nv@onfl2gwB+dRzio}S1X}24XKsTk+&tSOqb18LKmlt==i5Mcf5`|A7j|biO*M5O|KQu)NWTtfMPbY?BYu8d_$@AK&iGm<u-@ibW9AwzU}+M!|MT7Z@dKVc<j~U>TAxiS5Dk&1>upqme{Lzzbz0ieqpIS@kn1F{?rra+ehvj4#b52{^5OrnCSh|z&ismvH#J9`vdXRj!1={hqrzI%!*zf{?Q*6R_y0t!tcd_hlyS<o*Zm3dEsIvFI>#zg^QWIa50k?E@tw=#Y|qfn8^zlGkM`+CNEsf<b{jbywt;he{#3H%UZC0SE-DPF20HW?EPVRj*ii6{EXtMjsqaCO=Q*bl*g?gp0XU<&tKOb+t1JEDf?BAr^v`D)ss^lr}mWU*;5^_;37v(DTt>Uf0m!03npK-K)!5&eAxo|vIX*G3*^fd$d@gUFIymAwm`mYfqdBl`Ks`=!6FFbvjFDeGaK6RnGRF&nFQnU8H*fk_&xcyosN&kpXcKL+h9GM3+Lezg=P52py6Y}3VbYBh0hw~SdZV6Z#6o;3V&XP|Hs1<PJzWp7sJ^w2FAfsq)TB5oC*`66KN-$4-;StNJu5<fXOfoRHQ1z;53*4I#L}Jm<gvt9BCX3m<4m-0;CtfaySF#fsNFLl`tR9gf66Aa3L&&2&_Z84pzfi5Q1}%o&#&4zkgh5;*nGAGxwiw^YDwCUoSSoRsQQN9<K89G2!3y{J9mG^)TUYgsc3lOh2yj^KrGJyxQ^BynpR;c<eenB>_1l0XcSkoq;?-_SgdUjFJ<gl^ep(7_8c9ScOyYGn3Z&X-H4Q+8u{=dpgq7v8LN_1+^n>r)z8yuDr4MnGP6pi>a%+7;|Sg!c~5n$GW)6&&PzHsjIq}@HfI$epaR*SNZw)WE}?A;f81bSbTA_Y43kwdMN-~0+{l@wq$+~wghmo{osQYnH+2hV9L+Rtb?sa_+<SA*AM<F9l39sy|?|K6@+iR_5v@ST>P5{*EPf&o}F8f$-y?Gmx~#_T+Ha@VpcB)`*QKy-|a0uk<*GnaTesUk;e+kyC9FJ%NDT57O=+_u&2U9`bBb@O~tcp5<T0d;~6&_PsTBLDu(bg1y4kB5}tye)99%=3n@7(C*b_aNGIb7N!ImKhoknv^$9Bo?`_Z6PaQrSh#!A-5cB)vK-_+CG3nETu*K-*Vn#0)GkUq0)msmfSg*Qwrv2vGn`yo*xV&^_+tg8aF_vdl+vRr8u_>eOkJWL?UqXJnj-2wim@bCL7O=+_u*Vj#r(qqk{n!{<hhy+F4J&X0R^6%inMwP&DM(2N_vpg0rEPb#;o9%C8(~rdL3rYkMM8Mn9k&GHrw&gR!jCRI#}2~x4=)hHo{t=CGjRySWgoeii9;YR`^d#i90GCKM=oaK5Qse=>)|H*jb?g@X8MHV<td#Yo@VT6rq{BY>}{IqqmHN7I^p)Xd)ER8!y@`lhTuhTF5<EDJ<I~c)9Krox%6$!bVRdZ8UA!0eVa4A{C<X<zw?pKhcoE;yAbI@m`Bgw2+|0gNl)Ihk)91_(L3xCq)Xr&`o3i;(xtE%cgI=KiIlvbIUVhrgLDpb(0!8Ft0=D&c^J>OVk7MFV{cdDVUIruyZjg0Rhgr)%O8wAepY5J_V|PF$$LleTKMSKq4ewx?e?=be9#KQUwUOF?bU;DfBz>N;tkIpsK~5`mp$|IqNg_qdwPSgr#A?*dh6jo*S+Jhue`&)`<vfd8I*Sso)dNNV0766_EdPh{h`0V-{N6!e+a@J|Me>;a<RuBgb9Ct|GBm&vmPe=jj+eh%B;m6e-J*o{{-(p<Q>z2k9-9CwnJ7BUODkW($|%O@cqLNHN*h-RAh3n&FJM~MlTmLdbya@TMyS+gC$&phZ^iHB0MK#|6z350`{En{fFG!nSQ1&Cij9y*yAtv4|TD}AB0{0N<UK<yZph}<7Z{oVvj!vpWJ_f_a8j#EvB#FVy3U)Vy3U)Vy4Hai?J87nZApQnZApQnZApQS-th}$^J)d|0(wmb+NZU1YwWA+&|RC9)A!f{7gSn7Zd(Q*yCqq)?$x82%p@4g7=?4J-yqK#!sg2zj%1!#9b86**$@aC;$3-inRyEaq+Q>uBBLdYz!BZ_k9H4HHVM4ueqYa&%>AAb7@5{5BKbUOT~U3zWOU0D{<gqkN@Vgrg5>SH+ggh7kl=nj<j>J7l&~-pU%ZzJPAJ!dwC&xdDzP@v7d*@?-!E4k8|IjHpchf@lJ||Ql|>x71lc_p8Uf$Av}0=nBwGzj#(m@#Eszlhu;*!M-ObS%oV|BZC+EcO$5&!UQzK~1i!f1ti)CXdviNtGlZ~b+xxyYO9*?u|LWUk2w^X_<nLKUu$MbBR|I>tL2MJjUhNUzMR5DU_gKU(5?c{G_oe+5#}=L{gx~Y>O%#v2xJ?Kjdp<|;yrqA#M6mn!mvil*U%nxPw?EKbnJa?3AHJ|+n+RU~MZMy?2v!uO5?c}M&AoQ-3?b~<cGsraLfG^Dz3-YUguU24_rN?M?B$Nk6~SI@5ZgqsS9`>F5p3Lgv-S9^OK5CG@bB%LD86{#cp?0`=pKp>e}9Y+?$k3BKay+{!X&l?8@GmpaOahmRpkiahk7?wY!kslr>(B|E`ncvyIqN`2(HYXKV1lWwmtQDyAbw#|Cu^l2z#;Zoi;}Zd%2@>1h7{d#5NIJsXg>v1P{J{2=D1CjV%u!y*Ewq)e|Oh@#NQ26o2Nn30!>R8xF;<+%}$zNvsH7Eb;L(cWtZi^YG>mUs2J^!-FqfUa_BtkG^?XH4Yr?@vpdZDi?cte=~I&7kl<UICVM~dvVAQ^060B!q3BAUWi^E_VP>Y=VA7K)^U5>UVU9>=?n9|vy#DwSe_rRJJ&uiMK0~V=wn45&s2EDD!yix?)f~FSbml#d%&>1`x(15E3v4=^7D8Q7d>3VQ)J{6>&aoq(VkL0d)RUGt5nY~W_%@&hmm8k{2Y61mY?I7&GK{NW3&7`9wyE<Cto&`FN>3Ri&H1Qn)$#Ld+kS}uN^84&9WF=<kipNYx?Z2@BZXa*X=(qvi!VS`gr$w_O-Wt`OxckTP1cbTQfJ^a*MU|=>vz(e{!d<#@M+$ezvY~yx3@*tud5e^5pYskL5x8OP>9_I%Ih;J|!<cyqaWqES8^FpNxE#-{RFOW53PLW$TcMkFSQ=xomwh@wa($c>HV)Gx@c7waxM{^<(ksoaJF_yC=8HzH`D>>*06%aFJL4T_3pGh8wqAd$P|J*}CP-E&le{BKylvrY!s53SZsw<iu9pU|n!@#Jc9DVP8G-<nZ`$yvU3f8;zs<5+lD-+q`kKzr@&Iscqgk#;3%@r&7<%xW(b|)juQOV(XTb!_H;w_th;=4ig_=-SXrx@%Pm;PY#ct$*-^edE-p|SZr<c#@RY&Yx~>Le!Fk%53D&ajA3z+w=QOVw%cBC<1^Ol=_h?_fit%#{pt++bKiTxI=XbRuZDSYI#;BviBtb*ee?RQzS`!=;ql{mkr^*G8b|phMt-H{dE;n*iLt*@^Sp74Pl<_7rOuggi^Jnv7mR$1tzlLUJD0KFSHnCxOniJb%#*{!-&fl_IXr$QzrLF1jWhM*t9jlyTjy+Tvwxq#TMH}?TemzOwpLkwmWQodmY>JN)@=<>k&#oXCx;zp>$AqM6605?o?pCL<;d~XB*z|K9di8g)gC84zIx;Fu(ia=m#?lkdH2;4-YQ@z{SDW%>F>WTq`w_IhyH%+4EirsCeweLG7g_psJx|=b0OuKLBAbG$IqrClgYoy4*dpR!RIyj13v!?$M9(jjm2ktXc9hCL(}nT56#ABZfF5MuTaioKzJt6Z)el-KhTlsh}vK*XwZfq3C6&9h$D@I3a7#(u#j3{(to*dA<_%s0=!d9gEdIkz-pKdGhqYL4X_T{VHRvcx(PPIY?uq1k#2^I;S5*+mm|F#E`|9JhAWX?375f{un4Y3dNo`D5jYomk@mtiI0u$M5@`~yf%D*e7(_Y<{SbvtNFz-{ivIR-3~3C8Kmh}GA>9Re&|wAaMY<P8U^!leZbW(`?17cA3T{SvGwg#dSPT1+?uU26dbkK~MS3f|2i^jg!26KC5B?guVGG=a^e(sqdSEMj80m-M1MpV33hqXFH+%@*20P#rNIwA|f$h)-_aVIxJ_ZSJ-~pr$z`Za4*TScfei|Nx>mUOUA$<t`9<m@q4rvZP2iL<+cm(Mq@Q+Y{8{n%*zY1T3-S7^)?C!?Tm*MSj6MPNn*WeJ`0`G!vApHhB4)2D)f+vwa3I77O!F%B;q))-O;C6UFd=KgO;NRd*_!~Ha^ay+xJ_rZkM@WAJ--o}2kHb%q{uKTLJ_>&a&mnydo`HMde)t8_U%<2QN%#~zkMw!?C42@x3ojvk30{DMFboePeHeZXpNB8Ot4Lpk-@zB)EATqf*WoBU3PpGW=^OBS_$T;hcoXTH@JDzIz77z23_pK@C*YfKO6UpvghKxchhZGjaiKAxZ^L(BBGQSWQ$zm_KY%Gnr-UYio`(N~X-KDqCWn3qKY^J@XNFD-{TO}*vyjdT%?SM${2b;WofA4e^xyC+n1^&;=#0?+z>BaD>B7+b(97@-@LPBpKWB#i4~b{+00', 'agriculture-fixed-high-hopper-treadle-and-open-trough-feeder-01': 'c-rk;eUKbiaUXs7OO`Ev$ltcKtYu+|z0-WptmK`wBulbEwrok*0ZFL#Zujoi-rGIz?n#z~f^k`u5Nrfgs#10Zl3*wj0xqZ&pipQRj41-KaaGERpn!miO2Dx~Fu_g;0n+_u-rn2U_ukBCPLMxVTRZo=*?zD4b@%J;*R!X|+U~6j6-9aEON#Q?TNUNayLQ}lI9qD9D(&q0!`aD7z0xeT8_n$c>|3Uqje4V%nS>#kO|?qBTxn+RShpi{z#KJ3O(&bn9;h^1)kYnN^-(o@B$sWC!vxv&YJghV^?MFy>!oS9m)%7^%Vq10GWozz_Z`_c_v_(o<)L=7)Iu@F8`Cq5dZpgp-)z)y?0r-4Gc#VAnW>aBEs(D?S;;gTjfq^Q-pI5YGnvLrrCzO1W*W`RbfXPIWyWiz>NE;9U1?1bnF2w`WSeV^R;7G<17>XQZp>^h%>Zc}85*$YOr_M!j5Vv}$x18Jm~FSJ<w~Yjtv`TbwHujcrBs98%bDp?yV9(dYI9;}Au({eT`+uSqr9cmRDU}{=u#oHctT8px+_G8QoCImp90I2+L>D8AaEY9R8c|@p*hFZ=;yk%`VbfZC)qVSGt+3c<F7w4Ycra4<f?bnQSs9=wMrZG+ic8EP6dXT!09s0QniJGjKMu3%LMG7c4nedDWhYKPnGKR3S$I|BhwD>;;sIG-Gl=%O+2McRO?lcY!b%R%bAHrqdmvV?&r0Q&}?nOt*t<(?pM>Za3WY}=~=i^7TSEQA|Jsb<|<|}tOO1)Qv$PRAbhq0->BBdVVi=hOw<|>u4<Li0d$bkczYIiEO-v=X7IAiBne71aD)PwAG)?8i;Xz#PT1}{$hdeSwtUY=A*cPVQ>xZ5ZuG>PA{-bAG@b+)H-cSsccax-&l-0<2KSiesn#JP)<M}mlgwD7-3B=z5sec&fgB}f3%4N?mfDzV+HilO2C-(WTKCPz2pEcQcLXch<)^E_Ucs37kp}2|S^fB4Ip90ibmk!b9ta50u8dOqk!S+_H8WE^z<Rb8ih<i3^-0v;ZX650;>7CjMlvf}vRKjiATci3t<uCYVX9O^8@`o>-pm*jAf@&c2sK-wrl+<=mzZqAVtij%=ZjyfvOCZY%XyG&znvuK^g?zbNqxVcCAAgMRGU<=b!|Es<?ak{XPkd0OrxGH&TbUvnA@(GoMDqedDdvn0@H(4ut>R5tBzsiS*ab$G$tmX91UV<1<D&z<c&9GYNa})d{XVfEVa@hM#fO!4%uW&y{!JuWz^Lu8Dn|*#B8mWX;xd9Gn$QZ=Ke;NRKCnE?CrOpCh^M@$SVH27?DCDeJ7a~txF0Is0Y>Gx=4DINHM+b01O<%RD(j0kV7^*mTffqkS$OGLlYSp8A72Pxsxz-H%_CTeg3A5f6VpMW71e@{DI6th=t7jp@_R1KK1j{CLoSCeS4}3^AgKbPPo#XAAiZ7fZ7Tpa4S^tFml*~as=rTm#qF4C2^#Z#4cVR>bbUmMkzg1Z82Ozk(8<N$!TO$so5k)gqUG`402bQ*0X-9g#ZMYZa_$8Q_L=GZ2%3G+STz)qh4bpQz&}g2O~&oBPsZ9oRSDNK2@!in-w_l?@@DFPR|)RGiT-OoRf2N`5cs}P$NR22Bi>`8<5u_WkTM91Oo9H!XJbi*xs<az`?->!Tg|iP>P=4mt$5;+7bJ!We}${*{qJw*4hw-M~HSurmB-uBYvhDY5Ntz2yCGdYygb-scQt!T=21~Wpi1Q$oH2azm2#3Ud71U;I^-a{jf=)=-yA%u^#J!T(;4yPFCyt%cb`0G*FXb!B_VbeDpBPMyiBaEEJ(!1Q|Afd(Aef9sC-n1p``SZwF&RY?@#(`}&fu3s&IQQdRKCT((I%E&IoTQ4`JtAj09j*;2VQ(}ujXH@iMFQL44TyZ8E@(W<t=(%k!v=6=#$>HqN1I7qg?T&Xu85chplsl&p_t-aaJZ`-_m%dWjyyx%He#Yd*mz*=wz0vX6n?wHK)`=^1OKYr^SzqjQ!fB1oF<=}qEgs>=v>mI^(-x2h}!1uthgKa^S5>(8@mRW2S(ME>fE-E)>$NbP(rlt$#@rP_{Rx0(KB-{9>=v;PYta)bz%vY<9??m<2D=p%1W2F{kms+E_6%>xmuRZFhX64C0+tdw52ai@qb;G}9+J<GhTHeWV$TSo*U_z&Z#NVX+diO?M#~*6xhGy%oc?7pu)T(YPH6I}7(d~YxC*i78$5Qd1o_AH<&|x3Ky*#<48kS@0j%(+0JUZ^WMm2w^s+oCJ(`-DX@m3m4X1J#2T24OJO7Dc)piCCFsZl<ZaGj<`RO{L<tjBR76u~{)*SG7cPF{61yk+>}JDR0imLpuH+ec<N+*LZhJsr((^Nyohu~vCssX0yjeb;PrqBNe=o`&N~W;(WOI1p~ZOL485-tSv_0>8`$ZtmC`c)6(`A$t!JMSnk6)JBB`G^^89j8;B<soic?$H1Co6?gC0b;s^IcHBj{-?d}sog249`3^y#S}#|}kw%}}=|FU3AF5H>GmXvBnB!;)Ickv{wfG#ZIgWM`j{N3mY_`rETQ@D+1gp(67F84T6*NC%bI1NvkG;;a$JUJ0r8o`I_-svvt(9ceoE~X>t~SHfNx@Z1v{sklnoq?w!CG}DQs`O|u97BceC|5K-4JruMcfA(r13d3o~2vK*FDf2jnA3!E<KTVNxGi#xiem-_j#G2MyQ<M)r_AYm=I$0g%HDtSUA6H8J{y_Yr{&&ncs(u&zrHf(PwSLjnwyG7cxFyCSRC|@&&I28Jn%i7}?a5u;q0X<FjR}4>L&|;WY~5vt>#U(@w;e(+rHymMKBZz8b{LM`@YU@rz$@F}cFh67dap`Qr0rGKAHaAuKZy&m`+)%xd+S)p8<uhPr+6Su$bS$|v!pfxcdBo;G7nTT7G*23mOWnKJgYjbu#u9liLhnKWQqiOkAt+QsL~qySr-@QownJ3FOu_^8!r`g4xWPE1sq_f{(h$(gR#uiSlTrh=Ogi-~cl{@Q*;GhKSfKca_@nK^A#^KZG9oi|<AGIAs8s2Y&vHPy-+s$t+^w2Cdr5$+s8H^VRt$F)@rr*MKEjcVG4ZrLu(&?d5F@7=Q5Ae~Ki4O;XXWW#mdaHBUIlWj13*XE7eH|`vmz=*3uR6x*wvGO*o&cvg?qg#E=mK>*l!Ripl*skh#wsgnITPC(fG}H7u2(Iqfj_EoPS~JsW&5G|hi5JOL(>yHMPPb$yft?M9bg<0629|1)4H9nO^>2{A)|-p{AuZGf8^M)_6cn*?H{HtfNutES0upM0DsMj4t*Pl2u4zeD9_mek*Bf@wZ8cO&BTY>`SU|5)+i(4WDU3YPr=~i(>%w$4QG@Qc5lz)HU|QFVQiGmS4My4+shLSOPsn3(9K)k3gPu3z3zB_AB2NF!D6Ls3wPw%vnlbwO{-C?Irs{e=YSAMYIFqf~Nx5n_Rj^28Xr9{6z|Q%U1%x`!E0&p=yX53n*3%YEdi*tmM1AF)Nvgj7^^ueieul;R_TVIN&-Mr8Ed$cOq4}{fNE?o!L7@OOLzE_rl$uBs*(}$O=DG!9x_RDHF0{U_hK)J5$%DM8=D~0BCV8aU=Rc-P{6X)3&=jSGl(9~?6YPP36(rIDSBvwagOrg^PZIeCqa05O@>-D-DT4yS)EwABmPSrwj$b%Cu4TeaCvroi42OoA`al&CoE)7!QCUQ9F4S6vt6BKmA2&W6A>lxPPm*=hAqNo6upml6tT3U9>Qkhp61C|n1RmEwJ*u_?#g%HpnKlp8T6&IzATospXIJn|%Z>6ULyumDbbLhBr5SppCe65-<Y^(19=Vp7A3a(r^%xPGOjlaO2emd+fnyF1zFDF|eQsD*L=n%8PT_B&L}|f^UWIhLEB7YXjC7`aqD)6r<mPop(`>^}R0Chj0J<Pu>#pgTrf&DAI{)mW<-sX+H;<av)O^3{{f1Fgvm@m>&`fd;<Vl@m<pSlM*}_wv{LCcHEhF!{zHK{}qpLb@9@o#o5Irnib^Rl)*_YIu{>|g>HXDGUYPP?7{OuEHH1BVo(2k1IL&|oSX(g%g2iK5D4_r;oixyILz)UAeV)n}~h%tG`v28rjI#BRKA!3<OlED&5cgukfP1gkiAX57yY2N>amX$Yc7pg$AlQc`iq7e3soj2g9Ku%Cl?O2)ysYb^z9n}so-E;}X%%@JwmKr}X^VE<;lU!5GhaN30ogOVcfjbQz_OL+l<EjC%(KI#x0fZ48v0XSQ!x+84d9Ip$-?JlMz4Irrq3pIHG&?!oaWhI4MoLwf>0Qc7QtJ(>A(<`(2ALOK+9`GEq}OGFqugMJR)b{i--C0UVY)WarR}hFLEiyna0*TtiRs=?B5YSks)&>)Ia^JV{B1Y<-CX)@<6g5X@<glYgI|vg*V<=rq_tCayX*wruE8}V)B{hI^Q4B9tu8ykY0?bZH@(O~9t3Ir(-6xvEW_|07rUCI*TtE{$om6yTi2oLF-VBfj6f5*<!Z3sqC$+F@<?eXXm?q`SKDFJ+m=R3e=R87pc1qp{#xW<J^0XjE^7@=0o7&SlXT4KVX`PCB<**>d~@U3?-G#j5sV#bSGHH`lWp>cQ?7qw2l=~8@_D<|oJ0tYZ0mEfM2{sm;*Lhkv4dfI^$#|Zu(nM%h2VL^PBB{3i2=@dxP?#s&U`q8pfom9-87oh4JVE2blXm&I>@YPRA=a>dgcymSh}0SWATY|8rj`cb~Ck9c7rIN#%`vQ%5G2;r%|0{=xJ1E*;*RaS&%qV47Z^wO*7nd)2PmdQYpo7N43(Z4odVis&i~3jq04do+4Vf5NP8^3m3On|L`Ps8yKF~5@{|x91FQL(!(Lh(Nl=8X<CvDO-hOW46P;!ww&=+l5nZn;T&yf;eeMYS7?Tzr`fikJ=IM$9=qcy#>0UjRf%MpPO2ISj(Dl`2N@@o{@@U0r}2NwPEukHj>mRmn*Hw>N&I(^zmq6u4vu%tRN+s{C(0ZH<8@V6)98;hX;bJ=*V6fquIq`4&4KZT8m{+@WT%95C6{ibtGRR|UD2hR>8dW>Ojma4W}>=l(Ee7U!izILpDO?8wv#IU>yA1Y|9ef2puxdTfZyjmvhPSHllj5@in8gByOd|Po$9PS`rhJ_lQ*7_U@rzH^m~tO>PoN|19y(T@`2u*0_?@Wgr1#~gS{xM^!`0k41RX|f3p7uXo?(~Zj5=lG3F`qc}i(y@)TppGceBr<ve8xT$d<|m5Y>1lq=zSrE)oZvPfA5*Ja95<y_@5<qEi7p<JLWR4!JQ!*#iGzH*Lop>h>muTn0>sk)2r9W9=|$Mr<`h3B8|L}5yQ>fz-=OzCA9>7RNs-<y+%kv<AjdUnn*rt~sA^h3EHg04KqAGjFEicy%-2m0q?N-x7m&-eouBYhO6^z58rOz9)=(0?TUv-9{rcb?f+@=o7#{DcTA%9kQBrC+mmSx1B^y$mD$#Kgb$=Hy|dkHVCmoimIny&MnyN9I4EE06I9E(V=PVoD$ApNlEI3?n_`4_u7&QJB)RbA~acm*JuR$o=Q_o4?z+`-zj@o0l%^$nd-Fzoq!{YR!}3W6xT}7oOiP#Sa#~fjQ)a1bYl$A!hgrF~e7gS-w1sIy(3LYO(!}JkjCPlWw>B0j(R>bBLx0G{rE@+<ijd1^Oaqp5T6LUX-R7L!M#`d5SUQ>Cv16H8ob#7eg(5A*rn|g&O;+zB+s{sl*q<`x2<yFMxXdJa}JD>i3J_ij_O&1;3tp+!NuGPk%ZRQ~Hn26oi=4%P`VI{P5_UJdE^Fn9{RzhB2j=;b9z$uA}hh>3gp3iZHdW3{(0wd)EmurI%r9UpglbQ~Sy=rDx|1V@fZ>L;sQc59rEc;t3aHT@i&TeXxJIn9|EI(lhadi;+GGQ+jsJFsAe}JoKM<{uAt9E~fUCVM-tDUoNKfGED7D=j35(Um2$K?3`gt>1BB6KXU&$zT&H$+fRMLd+Nz2Pe`yA0~7jV&%P$ZUJML%_Txo5rvQ5~FrjDX<X|rf5B*2(KVz4CtMk;8*WiBZityLo^7%+i>31GqA;gqkhLQf{(?9La$-_t=g(*EdXBbm@86NtN+<!n<9^(&O3_6d*ls?cu7gKr}Mta5{xESf9Fr{bb3}Z?!!$bdxd=AoCdGrC&yOZId|I(FV)Oi$su<%E{IR)5b_zE$@SBM$DLd^2z;jk@6pKf&zt@}_%rstS6MWFFyc8^Izc@<;GQ;Z=`F@`*meWV4-V&xLJUZPy2EFyiRMetrmp8j45SA6Ds0gPV?*QLr8%8!2eatHKXIDL;>6yd)=_Dbiv7yrC);3hHN@csYjod4vp!Yhl#80wPFTeiQau;3St5dZLFzwFVA@b1@s)8i|`fBKx#rSgj~(tq)#7Yn7|7h~l6;*wK^(;pUNl>hPjepL9UPlz$<fzpdG>XY&nVYCaxS8wmJXFDQ{^#AtyW!}~wi!t*3!JZ}FzBOMFVwC?;>pV~0D8{G<N-x5wPs&$>(JoYe5k~qi99ru&Z81i^&n-8+J+FOPh*AFR2HX3??};($fzpdG>XY&nVce_ZAAj(~x1M-capTs5#rNI$nD;NAdia(AcL0BprTN(+t9aLE&F<ANtUV#3`SqiZd7uB*f$kq4uAX4&MKpjr6o+U!%sgG*JnVgtr^}NkxKG#B6|4*ADZ)GjmYyR|5#%Yb^qh4O8kSx}6X<7P9`-(Kmw=`KG~Eb$5t;~l5t;~l4bX7xMQLRAqVmY>Mb{;>7dwy0UaUMKd$H>h*=vA?V=q?E9DBV%Spl!>l&j%&1?0NR$TJkoZ|A~m5y_S-$fuW)`{%;%SHn+5*`lmc-UzR?$_Ttv#ekQs<l%LTQiRtgpx6SR<EI9>UxeRB;O7>|zUL@w;JQXx4H@@*B?s4>ax=-Zqi`Kn-UNC1B1MC%rmTZJeTibi)l_tnsa?3biUryDDrEy)Hz*F|=4%xXuAZ`9xkkA`*$CH-N<q0^S*dJ>>t^LvC8K1Ot#I9{+@{<JdHyE2-lS|(AWjyU9LL2FCp{)taxuh7kIA`Q3~|z9ayJ)4ob;F)fQuncdQ2_B#gNxLrY7NHq-Sy^7b9OL=W;R1&*W|{Mm;b!02iY^nOcI2(JoAm<6@*|awQidUnb{rG0M;6ZZ1YWFf{-dqdu8hf{W2EOijYYNYCU-E=Img&gEj1pUK@^jCx>d04_#-GPML35A*mij}P<s*~{bjofhn68OGmuQFzJ88#^)#=j2!z#FFB@$2P^n&use(PlmCl5eL&X3b4oML5hPl3NfPxDGt^s#Ec%KI9Q_)GkTC>x<(#O*l$eIOH9%yJX4zPJkcbPCrPihn54Ivu#b8sz1De`$M2!t0G0KPP^Di;@QqO0Urah}*TQeBp<=(7;MGv|Ukd0dsOzr<d==F5m%`5+{Eq#%>*0Dm)b7}STLD)*o#4433)d{v^4NJ>1=m$@cEP{JxEZcDLlwUaPAF^Px)#nHm%}+=6s~xVxPqKmu7LN5^3;>x?mV;YRAI@<r#%rq_UvaPF{M|OTe~7m>17z{@%!&|P98@3C`{?uIm4LJ%kc2IgM2T5t~|ycxEOREi79=ce=er<GK}<$KX5V9M`23O&Kbs(UWSMMBln+!o$r%A^Wo*scp|*r`FbR#^iY>{M3~acFw);O_Ws_SJdE^Fn9{RzhB2j=;i3P?{RedAG5)~Cpz}yf=>z?9F{PJbq-Xqri;+GGQ+jsJFsAe}JoF#A|9s~czwZ3+U%gs5zT&7S!e2e{tIn#A{Jik`C*C8();s>E^Pz9PUhsbNxDey>pzTlnSHW=JC&VwWeziw0!f*fDzxVix@NMrs-IHI0k^ZI6{G@RBgO3O?^4)XvbfNOjhlLpB|K#7kQaHTyAt6RRP<jzYeNw(6jCL^$qxhBAZWdyscRy$p3m5A`jC{X#(kOoObFL7h{DoJI;_=lRgc$We=|vdzN%@K}+J(w5!bm^*l3u+1dn<()`Tp7a^y25uYlIl(Uo)#0UwH0HAx1q=dJ#r_QobULd+g<pzq9+R|6b))w;k+eUtC-G*>jIld;)NXrTOk6tNX#tFBg9LmwJ(<XKDWP-H&zF-@DR#U}?L^(uZg~O2g8NXkeZqZyxqO$W!FW!`=@tZ(TUg37DrVq6y^bfIMB6UPKeDi(rm^=saECJnVgrEs8+XiLe);iLe);iLe)?k=bj2hGQ=(kIY_lT{3&I^N8%l$|JJZ01d}ptbRoHV)e|i*YD<e<pT1&asj+=3O%p9P+14pb;_H_UzTZb)s)fD^UBK=2d<7{k?$C7fa?au4Lz^CUbz*nw<-nY2J*b}26%4_J+EA-tR`KRZ3@ImkI8Xd3~|z9awQi-ob;HS%f<LSh{@et3~|z9Y5*>VIO#F91Q$bI^O%~1i;<qmm0XN`nVieTC_j_Cxfu1p)Bs$J`ebSeE=IdBIgX2wp2?M5jC`4#%f%=^le@VX^}y5sT#Wi;Y6&hzyD&8g7b88BE4di?GC7xvQGO<Ob1~|HsR6hc^~ux{Ts+L<!#qCB<7Y3A-+t-~o%26=y%+qQkPvV9{xa`#lV6eI)+6V7JCApyxN+Gc{Jx76BmL1=J|o4*_YJpvN{Uhbl}G<tivRJUH9dL}{_sh?$5(_uvc>MnFTzMq^&rB?m+F&;pV_vcOYI`V)Gjhi?IOd}E;3B*BE!@!GED6v!_+P^Ozk4W)Gjhi?IOdhU3eJxVDr((yc=N81-Rqm{+`m@eMR~CVylbqFwNY3ML}8|6Q&97dor3}o?<^eSDs=&{Q!+eY3As~G&l!up1J!(o+3}4x%)lb5zNz-(Xh6dqZiXK_Ugv4S2u>ex-sn4jbX2D410BB*sB}EUfme>>c+5FH-^2sG3?c&SqSH_47_fDGu*Z03HEaGeEVYZB>a5x)O#U(j-M_k_s=KKzVQk8Hu41Af8M<g&W9GfTsRSKfRo@xc-;mR+u(Ej)FSsc!td+g=QcQjE`k&40(jp<{-2Yza9tbv-s}bB9C`t~N8sFx=g_6_R^gnC=g?*FHpu@}n1^c~PQX{f`S=#N-a^iy*TJdx8hH1AZ*~PahpvG4COCmB<k|ZwI2YsJ?=pE!h?)E-#7v$QVkTb;F_ZU&n5iFxn5jdAn8}qw%;Z@iX7aTVGkIT#nfif?Ax9LMye7m<eiULR&k8Y<uZ5V&`$Ejr4?@h;AwtaLN+D+QtPnH#T8NpvFT|`}csN1)jEuu^;(3C+Ak8mv@>I-xCym2#<9UL-Ak8mv@>I<FB(lzlQ!gc`yQKA7oH{UOJsDZ&#Hp7O)Lqj0EvgRu|Ch%vfUJEUy!-pf$@BPJKlwV6$FGBTQJBXcEPR7}-}Hs&b6pAcVqijl`W{z?y%@Oj(U~WTbWQ>GVqikg&dI@E6dr!BK>odgPrUjMos&<`kiR{bVf;UO@Nd{<_=V^3|6qy6bWR?A*Zp7Y@s(l9SB5FyC`{+%;j{Jk`1AFB=K1=2{4@RjFzCu->>|XBU4)piixks2c^G`jWBgW#8NU@`#&4yV&dI|=|B?I8%A>Dze*UYMyxl+i*a;ba;!nQm?d^V2ir4)3>)ub^*_GlqYJcbb!Ij^ZVx)h=r++5J$oJcyTiB6dl>d9H&XwY~m%r1a7vaw3Kj`rl;V*yVR8M{pMtZ6T5k|gLp91VLb`fI6E<()MMTi-@2r*+9A!h6%#Ee~pn6ZlxGj<VT#x6q4*hPq0yYTSv96CIQ4$q-y?;Lu3#W~&MD~=ZS9@|uu;9?9+=>2;_T#SLcu>X5=3UDz7CiLu_99)dT!}FKCM*2VZcs2Y', 'farming-fixed-bell-reservoir-poultry-drinker-01': 'c-rlKcYIV;^ZuMU3n(HGz=Ej6*fn6X>5|=5nqor*D<FmtAP^Ev0tkqLioJ^{Vg)O9u|sz4y`V4lE_Qtpd)MEbn{0S)-aG8&_4m*F`F!!S&wX+-XU@!=InT|;``L`I89tav{{2eycu%7Jh7CPvR!&7jLsetWp0jesSJhV4S2Whu=j@rY|AhLw+Pa49@iHa5e@#{G*sA*MA$ttXo>thmpl@MGPHxV$s``fNx>_-g_RY(gotx88DGqY>%xhr{IeU(nl~Y?WS;lgPdEd*;sjVC9eWQ5P>{08!nw3*^d}Dn@gNvfFZt|46+N#>d(e-sTZt9@g#_Ia2?8XVzm6Nh3)Ya6~P0y~bmDL-o#%9-7HB{A4tE;Zho?hKJA-l4su0cjC>+7c1W>?gX&6b>|R@YW#JFhiWjaAt)TQZqkH??s>Zgy>5cEyyc<FgwkRE%qMw7zkwELB&ZJ)wH+*s9uWiCW^S$(~Zz(AdwJ*Hj-jwR)_xm?BFzIO}m!YbzUFA*2M8s~RSF6=+HO2#L39fEUyN7t_!wRki)=8XM~-_php{IW!%-OkHmYhDrw0ovU<$lPeml>Z>KNF?G{xnp00_D!F(is*|O%r^_n25@AhE_W1g`sZx*z=fzb<Dj<cZuc&tZYO1HW^rQya<7z4zv&YE1>?t+XwT%<jrIqhbYah>H)mWF)u;xVv)>qd~s;(VByuM;arkp$<+2g8ftDAQvTdH3@WkQuJcf*v5N(pYv)cR@(Zc0UcW6ccN^K5Z8LjtUm^1Bq)ZGQ8vPM0A1Wmi--P8A<s{w~1!KHhGN_2i1`+6Kw3ae9?}uX&M%b@@g8`5jO<y>)|zdA6hT^8WX-D#)Bw{{LQ9g_*O8hCfx~s*iW7QBhw%BfFx$azggxs;Wlm;}#)lJ#Fq})Jb?EhYh(c=f%?jNnZ|it<wd`MMTt1o>oyat!iD!MgEZ8vGFuvfLnHNS=EcTazb^@*!n7w)e(8Q`MJ^Dg51K~BGJlqiFkrNx_Yd58dp(2S(fVKCD6y6+CHs??lYxsYE5JPj6P%Csg%;nKIi6)6J2i{JysO8S+w@d>2s6}H#ADjm7}LsH^_dBuB)w?k+WxG{nV=5oVxnz@zu4X$5u2>oh;UFu%&7f<Xbbvn<qoEdkxKUS=F!Q`)MWeI>FoBhU&3Z%?fmMUcc<-HM84<DKb2zs-nK4wo-)H#gUs+@7;bzSJpW(u9SOK&a9C+6=N%=G*(Zm8kw_a_PC0ghN|4`k<EMDQ0>YeI9^vj+PmlYzd56_rmA7I=zX1tq3>H&wUWCxG%{zvQ3DPbG;Cy!8*iv^w-e7zezeq$G)}0msu=5y6vEe|C(Clp^9K((a?rr$>C>vKrjM?vm?25Qsw2E*N6mIE)6yx@qJ!Pm`tBA7Hy3PRbG>rhjWpe%%{SArbyLUGR1K42k4^7li@#PMM@ZugnO0Zt$~$FD{ee}oi#64iht^FUKS6HYUZ0JrXs8-cS5sF%Sc>j`Dj1R1w<Mb9{zXfR^Yfz7vZCC;p`y|<_phX&q@<v%sJI|E-^JLnM%tU)CF|46wT|@_C+=T<VL@I|etu!eY<DR1gxsCxK)I8R9bQ#0y&<>OiVe(27V`d;<QGMYib@J4{QM#>{IcT0XhBIdzd(laN{gD!O3MoKipz>iHXx;v7I%4t#Rbu#;?fK$wd%pZiuy@j8XK5VK={pDB%4%LninmIM!hVXH>s?oIKQYgzc3n{QQx9`&#E-9ELvQYUr-X5Vo`H-^7G50VplfX>q${P{||v-e;Sf>>#HYMyVKn~zoN0RzFH)<%FFrSp~Hp@A2ReHuigg@J@ml650D>D<j_>tj;*eAHqmt_LX2jQas}UzA6-HRP_Qn5LJXh?1IYi+0D^zE2)%6ax@Ajn+0y@F+5GU!mO;7maNYd;|6<{2_=WSMuyTQK<-!ar2i#`EFIxo57W<Yh!DXYfy>~MemGZrYy833PW2TN9S5<$wD81LGtv`JXpD{&(E6R@+yTPfojjotQ-p(E0a(tW5YEfCSC`MsnX|5ttZOq(}t9Cy(^a=KnS6t{j@A<iXg1t0)5#}5|Xh4DYBMD}bA10IaIfw>1C|Kv9B)ZPQumO7?u=k<=;i6#uF_e_#tt)1<rErDfSj4wk%S%d|)v7qJOvVcHa|7(KngLF7`vlKfU+RS+;$GkUq70=gC@joWy5jYR5G{l@EN;1J6qXd17L?={dzEXxJ4?ES(nI;~UN5)m7P|tu*Ax_&6t$L4oJ5;TU7S}U_e}Y5z?;x=<0&XD%PWc&l(||4dRbpFN-}4%zUigwuVq1Trb?EDt)xq?D8IC%sJO7eC0CeNP!w27cN+5wO2v(|k~CFeS+TDRrCIZ%g$1r+MMVXLMNzGm@>5f^tXN#int26<rI|{ZpZCvdnV<hpi<uw&|6a}DGHhTmgLh=TwJ7+9wJiL{wJgdY(WP*&$t%s1#0m<cc_k%9c?GTtMFph=lBuLERf&2BHqRT8A1e!@CGJ~gzDoY53#n9oS#h)|S{jX(mK1yEJIKd+3sD>*jrBSx$xzAYf2yU#w9W<I#=Tqkm>G>#2gp0ZM)$k0sJsbi9vV7soc9Y<r`{Fy;~g!KPKmAyD9r4Zp|BpLW!pH278R65{SFG&<De{BnAgTZX=!0;_z3>fK|yI==>|B67CUQnP*_qBEe)SSwC(&NcTeAd0RD5nbaMFlCDFFii#B8j0+uf>F8oK~mlZ|-LHPOJj{f)I=NIHh|4I1r^H|<L3BR;-Lz*Yr_5jHn-Qo>cKfr<fOuYf^S6tY(0L6tR|It6KlGGwc;Gn1^KkDAxW@o=o)PKl9bos)b@dvh@7bBuM8h?0H50Bp;>D{F9x$W9{{PKkhRlY;nn=!}bs&cXOxXepxT-NirtgmwSzpR?q?WuAXH_Q#>E^de+kh{1cmq709peBLbtp~LY<SuU5qd*S!F^$8zDu?)04t0oY9O|iZ7kA6Ps2uiJ<<KW8hklD`9Qsz}(EloTaf@v{eWo(;mK@^g^OcFW<Q7k#wM@Ka&*JHGmx;SP9Z#RZOuRYgh4J)x%*5S!Y>usGDBgSqTK#0?E@y}{BX7w$U5AXkWq!KO8F@=g>3z(|UCz)a89B_2h2aoeC=R)Y;!xXo7!G?EiZ|!)^+qTTy%&l@Z-?S=c4A>ToXt=i&VDHV;mjWKf`VmU4Z`rdCUx=nqxbi03d1WGkjFoqIX@Ji^ZUy&$K@J|%N&o3k7O7wF?n2K48@(cG{@E>6n8m;pN!n)3~^@UE@!AiM(*Z7oilP56YOI~?sA4c$;e@DEDVR(LUG7F6o=Zz!*JNUP~7F*(i@>T^j;_qy&a0f*@=bWa5h76IQyZv<R0&F`%_*G!tgH#{~U9C%_)(lF#Ppp@5Y+v&I!f8kKF5VxrX90$K&E76qlGhE-{AUPFq@XPln+xXYiAeyPP4;jNIi6b;!uw9H?_f?qY&{%*b8N&?gx=%#DTN5L+k?xrgFV+fW?#E);h;x8xoV!=d+LVL0@5C=O>Q6o<1Jio@9t#XG*fBqre1APj$R@2fn%_^O*%gyBuA&-Hl6*SBv9!zbP|-s5r&#bu7i#YZSEF_k+mF^1w!Tbg5A5{kQ=!B0l+a)vlFa+fpIAtQHlpw1b&iwX8IBX>DNpJe1Pw>%7o*kWNg<Q|GcZ9{R`yHMQa+|nDNIP_j94!s?U!`TVN;cSNDaQ4f?aLKv+r(NDj_emfZdyk9#a*az29+wzaXnfK=<2^1{m5ZInWuD4qy?&0%`YLyt(7f&vmAklMZXkDYLkxl3#SOUxa%TrM3FK})sBIv3al;-3a<K2Gaagxp;}E~fp$;mCdaB&T-Lfw#hy7JK^oh!$-&78Lt8(c7ei~2rTg%UZ)HCv$$5%97T%L)~sy)x+$J}(;a*aPU?j(<|Xzad1<4>M(u*c=9a<TKc%u~6n*UxcTU*+i>B@dOmxM6M}cX2}uf!xInxdd`&2Q>-gZat`NAa`-Y9tCo+@27ECw_M{8zsjKwDu;Ti+{N9pFDi%qRXOyD%Awy>4t=X~=>L8icfX4~Xw1s=?^ZMNheyr#`2CTqSA^kn+s*U%<qLZ@h2cAt9p!PkhT<~E<KiO}mzc^Oml#8FcOIK#TNsMFoWV~<?sA4WGjf+R)FC5xbD+){xr+(*F(Y?5L!V^iFt<DmhuC6aIOHCRLv2HG*t<~N<=oO6p*ZwjC=R_Hio@9n#o=s*;&ArM!|>kozKWHc`H0sWVfY;<uJ-swtG-_mh9CR$a~|(KZ&Fhje%qNhcwDZbxXkgm_z1-%rgFz6#!%d8OLJ^rh2kz}@RO0doFUGP+~o{)$jIFssB=c{VuF3l$X(9RCmA`+Ef2#XwpbVrxrgFV+fW?#E);h;xAaCR4!swOLvM%TaCSm*IGdq3oc;1JoOkaKpVi}buQ$T*wdb?PZ~bPIrZ9Z>ZNH2;&byx;if^(@%Hwhk#bu7i#YZSEF?n2KOori3Tbg6*5Q@8;!B0l+a)vlFa+fpIAtQHlpw1b&iwX8IBX>DNpJe1PHx`CNY@s;h9*RS4Lvh%<co^=z-)ruTP#k(M6o=l9h2d~^LUA~op*WoVQ2e1Go#In3zRasZ82<O%4j#X@JgX@TAOFX9F~=Voa!x3Id)1R3muo04b386SLUD=7;}T;s40qbn99ySQ+~o{@GIEzQ#F>%1oS_aGxtjxZ&d6O%u#XwJ%NhD4BZs-MFdSkF#Ub}l9BLbi!`{WiaF=sSZ-nB|d!ab=b}S5svlEKL*$l<u?1$nm=k)W&8h7@Nr?n-ByBHi#>q!uI`8b}|kRa}Ia6GLWLEOddcv>rhc>4M9v_1rJ7dOle<SuTAA&|ScA(uez?4Txr+^q+-4dgCv*rPxW_A!max+;hGRStDfIn*<*@$~cI>GK%GVSiN)eG=0+^qb0|Z&eQcuX6JK%}F_&`_k-$yVfmf7YCk1o4%*ic;kP3^H@@|>D_aGZ~XJud!^7GZRC527TXlsqm9gox2%~$d$e(}w#1%7d(9>ttK)5KlHey9<Oj#ov9^r|$J5_yn-`9!*JxWG98bsEw$3mf*KEKK+QgN35@@gFl|Xx?J_)o}>YPA(Wxo<=ui3!9CzSq4K>s9^K1@I#CX{|oKtIQobAe|k{>z0YB#z$x+1P@Jk0-UWRyA@`qJ7S@u`WM9n#8lC%uSxyYrjM%v462gFW))R{D_@rFY|n7O7kQ0<Ia!x^PMlvkIU1=De<Q8+-ZI^dzUASCo_$^Ji&kKIn~Bpo)CZQInc)4*HE9<Gog*U^`QQ(=R+HJ`N00Ro)s96D>lBf5B}qLmeCK+h4_8vTJr<-@ttwa57ggx-Zek4zrM4t`GNjPpeAU3G<)bzpPp#r(EmPd(Z=C?`E*7bhw~dpZPCV2XHZ)%nNXSNFlKdp(8O<Iz?(E(+U|>CiOSKd<NKX|M-uH(Ptg9kUy2gLD_6%Kyk--hhM*suD|Vi}%=2l8=11noogeY%(-6&%%hSayvHP?|^P}0joMAkfY24)r{#!Li8+Um^{H>a!jk~X*KCPOgjl1=r{;isW<1Po--xTa`tImK;4DB^t0{?NGi+X}{A%35RpdXwI_3>$l<_GHU(-6%M?5|HlG(XTkK5fzbX!g*bKF!g_q5plFqm9G)@@bAX4(HdWIXI5mf;OlvqpsOBan6+CiEXyJBnG@m)1{k!wTXwt=EcQFC(&NhrJlEZ6fdkBo;YmHZAqMqdV+Js&a;<!Nt}y%f^)@J-1!vWDV&RXf^%J-E@p|{r!D9Q=W6yYXBcnFH12W+|E-#X<1SB#KMC=-Y7W}C7t|*O^=Z`{v~g=d{Zml?R?R^hmjmo?pe}(;4DB^t0{?NGtLYNNAIG_<CpZ`C6UVuzCpZ`CpTN1OCpZ`O*QX)q2j@cn__RgyquE1$`ZNc}q5tD(gPMajaK7SbgPMajaDL-xgPMajs4bc<-F)~i@sAo$NX%b*XF2c{nl8Qd-qvwD^@POfugz^jdrg<#xS@UgT(SRS@r%B>nl6c5%-PGlB+k`zNqohePx0-WtLc)<)5R>Y`{ts~;9Rsv8<#VTHwBHmJi&hx_;1x5v~hVt{DHcJHtq%W3DhODace;R19b^)Tn@0mfw}}X<!G<z68MkdTuqlC{us{HbP4Jc$GMs=LH&JmHC=-J_02^+!MV^sanu&{gLBay`qMWTH3w~=|Kpl2p$(j`n5Ii;1LrrU=@QzYwrIN4@;f5${g|djXrt*5+Gv`CHk!_$jixPVqv?regZj|MCQvup#1p6$ZSo4#hc@*I)Py#54%C4*`xSWh6+gc7uEgUz<4Rt>bFI|Jcb1hp`_8YjU%vCM+29#e`p0+fls@#GHKm_@XHYp8zH^5*`1@Go2Y<VFa;G7)Qv3e)TsiO+Xmj=Q!sJFW{`@_c#LymXwkq$HT)gkB)Sy0VVrY*x^1UW!Berq0M;n>b<mQTxINGC)i_gU%vBc57jZJyl2JJN)7i*9o9Cxt>#e?JS6_gi_J6}Qd!EqN;P@Qoc_zJ~OlV$_)G@-qcR}$@&`Xtd_sdEzTH5=Hkq_Xcx*!QH;KS}7Hq|%2;=))$ZpPQhco0N0Wgl9)PQ&U!MmU`g&gHnIoePs-IlXku?UARf=ZLwK8Y<wK&YG>_@C%#FJ7MmA-x<8I{wR0zSp1sVA<6P|wim#;eDZUdpS38d`Hy5+Sp1`?y?p!`;8}x&7wR4JdU7l(G+L=WgmuEVD?fjyRd!_56on^FfYozP1oolplIi&YjJL6~ryh%In;6I7>+S!NrlQ>t?0jN(B=W3b&^-tkkO&?%?Q#cpx(FXMa`X{C72HHS>rZf#f8|eR}rYC3v=PRjc3);Z>O=>!WHmE0>&P<L>NL_W|OUcKF{}2P-r0Gm?;gPA+FMcUGuh+6T&ee1#d1F~BB{uV?cTV73O=rZ;vzK`ZoQql^^OMex`15HF&PA<o`M5YGUeyokhRY{yuldpJQBPc+Y5&?d>WRxU9lxeCXyab#`e-_XHg3Ii{WYCI8<$Ude>I&!8{kcv&Vc_U+G{!k@uzUErZZ5V6wXDhfcpD12j`-O!2YU!G<(z&=pS_)^#uA;9Y;NZ{!eK-gEnx!Qku@74V>SkrZZ@RdZOt}vdamnxgFLvRo)kg15au?(|+~D)ZrVgZF=E?N8`S^pcQ@Y9+FxVS=;o|6I=N-2j`+zh@EFI^AegLpXOZfXwvx+e+kVGYK6<k#VPTseo#YPK52W+k7n=F7RfX1UmHg~ae1cW*Tzv#+}G*)Xyd3SZoPE<HJw2lmrr_sHJw2l;7Ltqz<(0$Q7a&RpXT6P)C#CiO7r8>oOSh2X?{>cV1HFVnmuX@^p863)0TDpsg9$bK>w@bs3&l~)N#}kIKN3vXV3=qMAI4VxggXEe4YpW;9S%Se4a=1gIa;l^JsohEAV+9%@1k?KF_21K@Gv@d^A6rJ!%U+|D%ngw&3$W+Bj+pKL4YQqn_aNKiW9z2|gF3>5TSVB5DObPpHgIqE_JZgqk1J3VfbW^MhJ}&l75XP($!JL(Pw7kJ^IIA8O;ME%^MQHjdhY&mU^zs4e*Xp*D_sg3ljn<BGQY-*d?SW6vS~-*f)|ThIA3wWFcL^4gywv=I#x97YFH2ik;=5Ilkop^ns<MhK3e!)Q~=qS1n*=_u+--Kj#bf<{pf+MKEctEiH;pq^AMSWV+;E83bS3r?m<v<>y9;{=bRI?ARTnkqPz8fbgkiDn7TqUp3F?Mf#Jo<uWg7s{nm1W%#av^(uVrwg7=bEz*y>1@HXX&&WM5uGo1KAlO0R7w{MUQFjw3GGRj2wp-LQa_5(LcxV}DaC0ox>E2;T10!(0J>K2TDqDB(qOt?@OoN8`;eji1oxvGX$T!ecL?4=x6lD}C@m9QMz_<!bU58Fct71m!|7;RF1VcTr6cJWN(rXuK^jTN(j$V8P!o-zvGj!C6Z9C3qY3nk;4}0TO{5xnLGT57j%sNNy)5`Ly+rlYNUsULM*pH|G=tt2e4AdU<LN|tU+{f;i%y`EX|>>LdXMJNY4n-kXY?VRN@vkmf?v@mbOxPA-w1v~U(h*p5q&TCJ^h<5p!xKp;E(hzEuhQjSHWNDXS$rOpg#rwq~GZ(x`vFoN?w1{V!Dpno5k|7<_6lAmeLLK>R@iB+o+3R7qf}EmF}kQg56DLb0^(LTL^Apx|w_EA?hXA%WQ5Qpd|Gc>}|F(E9ha`PH;Q3jd_$FryT`%G~1ge>1o<ca5uBFd6u51zJh(t?&d{WNm0S5*~7d-tEgD8*c6yo=}qb<*w2)hH|SkT2qw&)<{kQo1_%x?aq|IvO8W@zWBQwq=}X#QaDOw{d`@d<sNhhupZS`;qhW%>%z<Vt{XmBa9%c?PKhZCAwBXU^2=g2LLB|LlV@8<2h|CzlF=n)36EWii$C*mg&fG*D1v{GYW@EFdsS~U-lT0U*Wf}w<Os(l^HZ#)&r<;1y!}K(>1ZSCPW=pfJIZ5y&Gt+Esvdvt<x#mQZV|Fm737%$7F*})E%vpkGnbXa#CfA%Nc%C`i^f7tnBEgHy`6k~KngxOj%*Ce2l$k|>i_E2_)Wpoyf>)c%O}W|IED>B{t}=U>LFPum8_i-f&<ruR2;O3DF#DQ=%pHPvn5E_bbEsJ+xXj#c4mQKheS-IyyUgL{Nb`{3L*{;Slo@G~f=RR7j55cXM+F}>DN|v_nkNOHG>@4ovyqu7IMF<1s?B8cg5V40SyN+<Gb;sGn&-_FGu8Y{@L%R7(`aUx*92cPubAV_Z1bkzo90z>f|+C97JS>hVNN!un)d|XGw+yr<_z<p;D_dYbEY}Rd@T5}`N*7WE-;@7er7%~7n=FzOTjPA=jIZ#(5w+$W4<z%nJdk=g5R2dn=8z<<_Eza%vy7ex!(LN__O)mTxV`JzX|?kelj<i+svPWf0|#-t>$h+e5<_vFn5}J4D+4x`rF)V9x(0rUU^x5(5x^U32wygxyd|iHWA!}H|9so<EFD<XYRyLm<i??^Mt&*@YCiw)0LkyFABbBUKV`WtP)&hUKf1bye0USc~|gV^MT+8X0_mI^Qqvc<_p0u%-4cnn{NcaG2aP(XMPm?(flI#i}_vfck`FvU&e4(HXIR*a0kH-+)=P2Zz{N{#L|_scr)%MxTRdPxR+eBcw4z<@pf{};vM9g#XHM2i+7W27Wa{B7U#(|iwoqM#l>>X;xf5rak*TxI3d?8?l0FY9wgT+-dC<!yuVzt_#nAv@gZ`};^A`5;v?jmC2<_V-FXWhEjXHw=FNF4t`w}~W4I@8!{Y_V^BCTmvw4!>Bp%1Td3&xCtmBEC!#i=KU?bP^j=T#`6P(8Nyesd{GX-bzbk60ze4^lqJd5|>d_Gz5WIl<bT*#*hp2nwe5tr~;f@ksRT+03Ue8KbiY~GXOe6irgd>+SmZ@yIUQoe}y;(@$Ka1k%y0lW`iEqFCw&VzXfFBV+PSMh#)0N)^Z17F7n@=#tXxRh_?gZWUtUGR3kg@^HBe7E4;d<P%SNAi7w_wh15ihJ+~!4Z5vkK_tY38wfVK9;NaF~P?;$z!>ipAvkEALR)=nV%PYo}c6zK8{xkuH<KV3Qy%#f~)vNZs6njHNn^T6`sK-@LPg!@f$pw=kR-i@9{f4mrv!71V7^Uc^;p^p9+4;tNBbmhrbm3l0V~f`9l6i@EiV$FW^h~d%^E{4bSI={IlTC{2gD$SMnc%fACLy1z*c#uaMVod<`#Qw%5q(FTS2{;`a7>c}48ad@FYp>}WT#xAC3aS+KM1Wbfj8xSL=%+r{3?5Af!Ko7?X8K_11+`9XPYVOQ`Y+*`1>-O4`9Pw)<cJJ@aQ<NOToBDjmqu}||0oGX}Xce2m%%bX{eXLqwN@vB@YSZMp&fAQ;FELd!#_Dz19_Y~aImfCmu1C9&EZMprBKj!{|{q0`%6aJhB3l6pe?HBwt?<csQ-N*i$zvZEVL+$={E&s^F1&7;%><|1aA1QdGJ=FfffAUDdk@j%=I~#kf;IZ~-`!`!VMsSQh#<sH^>^Q-3cC6jlZek}2PP7y3rnalC6|A*2Hp}*~^@8<wirvg^X{QNJvyHZ=ZQ@>nz3g<mwcXCn5u9UZ+HAX{Jyq~jd!pUm?rP5vJj0%BceZ`(IfCcd)9mgx-(Dbifj!IaVT<g1!TI()TVPA<0>K6LB3owr*~<klx0l(NP1vghud-Lzz3l+ISa7ku#tyRk+8YFKu-Dlk_5iz7aH+k?9%v7-cM9HVZ?Om4!|XkR_t@L*Fng4JK=1*3w>`p+vMU5v*!%1VTVWp-eAqr@N83vKsNkbEX{+pb`=sEL_HkQnC)sBOpS4fh$+phEDEOj%-X3Qg>??w=*p+swJ>I@1_?lg1XV`7*EWug!4SRx}Yu^`q-@a{6vh(amf*;xU>?!t4`-$Ku_CtHRJ=cCN___Vqo^3C*UkQF?KeOlCOY9oKHTFw;vAxu;6<lloZ5P@__Itta?YH(yd$s*Z@F)9&z1A+VzY6|pf40}#8|@#0f7svb&GuINx8UFQPkWoa%i73o@}kHc_FmgwuziFh%j|=8W5JCh?IQQvCfiA{Q)Hvaa{GwwBG@IeNhD<-vsr>!k<O7P>{GUfV2?<*$TRjiyM^Euk<B76*q7{9f?GwljJ$0BWw#OBCekbNs(syN3uZ^Qjl5}R+js1n^4c!)mVMV+dP`nJ@7fP+d%^Z(=>xmkZY;PlwWrngQ`<?f6KzbN+AnMu!7kK^zOY~0Zi3yY3w>?Bv6~5QM&0Ne`<>lVa7)^ZzOz5tUV^=7OZw6NVz(9CmU_`I_IJCT;C8ev{ciuVI|%MT+tFXvM0OV3nRXx(i9~i2+>LgoNTfrgk6<6#jXFd+M)Cyns1J3FY#J#LETBBvG}1LvELcnh)HTvQQYKhN#ne5rd8AyhoXTkPNY6+@FhS+iGqQE0zhHk#(AJUOkwJoks6X|Vs>r*x2+<&de{+7?Wn?@Pr!_}-{EHWMZ_;?vxcxo8a?VXEpWL~`<KJHMgUU;9YkoFMu1SrHo%h_8%u~6n=W$tI<q~)E^IL0<P<gsgQV*4TwOBVdkh}aLhCuG}hg<@=%O7eI$ekV3HjumZV2=WMI{%iv4&+daIT{E1n8smUl|%e0hdRVH4)s(y?2F1_e^s9TOzoEQ6v(09R1STsa_E1R!#PqpoX42P;asa6^g-pl=S^z;4D~R4(O=^{KIz$#rZ9Z|rAK*uME`q2@lXFXz~f!t<YX9r+nGCgT&|(G%<;JR2*o8P_xD%ICB{%(a`w2?AQX4|;JDN{6n8ZRKN-2JDa4tPyP85BGICc_sB=c{=D<E?<Sr)YlZ@Qu41Ji9yP86uXXG$97KTG?p*Z9o55u9hp*ZYaC=R_5ibL;(;_1I5;xr}<hqDuk!`TeQ;p~Uvpe>;|Xjdo>+87JNL3=}SSJMRp&W@#ZJ`;Cy9Z&0gChlT$JgxJYxXaz~w9aSZuBMKsbv_e!HFZ3#^O?A-spDy#&%|9#9Z&0gChoM|@wCoo;;yFPCnI+?g*Y>ES5v4%M(%0~b<W7$9N5Q<+{FZal99Wdp${{1S5xToj2!01!f=Q!6o=g7VK~$_6o<VF#i2Jsap=8J+|{(Dw?lC_JE1t7%}^Z9ekcyw5{iR%h2o%%u`nF8HxwV+Z*+Wm@@lWQHGb%~M|=Frg1$`}KPYyP#~*lWsmc$%qRit@cl<@=L*LxS<8n=ET<l_w%RH6KdLEbcRW5Ni+kbns%ANK)F7;5k%OB<ja+g2E5XfErkV_zU`9n<txwC`X26DF^>`@?hal>8*a+g2!OdtpQn8smUl|%e0hdRVH4)s(y?2F1_e^u`CZ|M`2L%*pU`c~!8|0;)bq;fcqF^$8yRypW{%IAG`NUP3he9cD(dOW^z`zDRQv375dH!QtI<xic}*W<hF^@Ymk*Y)tYT$36XJFlKHPvx?n$7Ow$OWYopJXD_68L5ZLUH&jPkh}aLhCuG}hg<@=%O7eI$ekV3HjumZV2=X1iyQVjkh}b$X979c$21P>svP21In*Jpaj2)tVP8}Z`>XP_&bafWap*UdL*J?#`d{U6j#LikF{W`i*D42nP`S&Wckj@uIhnYd>v&p!GI1A=<7q9*#9fY#r*$b4clB~Stx=h{tDWO%y~@O09UV_=S0?Ui>UdhmGI6J4j;A#(6L&QQKN-2JDa4tPyP85BGICc_sB=c{=D<E?<Sr)YlZ@Qu41Ji9yP86uXXG$97KTG?p*Z9oibHMVVL0qvC=R_5ibL;(;w^t8r&W_PaX34nIGoK;9L|0y4%!lmgLcKjaL~q39JDtSzivt_e$vDh-tYD`{_OK*9{+4r_a=>ZZnuZWAN=zImCrh58;{RF@fDRH^g}z3%QdNSv5Pq_^HeVDd0f_4xy0>p$wTE%dmWd0sNCfba|5}{A7TjPE`P`+kh}b$CV|}9L2U!MTMzaqkh{2HuLHTuA9^N`gMCcnu&&A>ew9NV;u?o~svP!3<*>ghclo#UiOQkhR1STsa_E1R!#PqpoX42P;asa6^g-q6bCiA_A?P!vp5Fa{M6`F$)T$@1i2?V0md>fe2PRf+(=+w<9<@o$=Fqi;i6vY2OiihMB#HKD)9tct6PL*Nnw>a>_GlyD^K8U6h4yG8bK-8U_(-8W+Q`~*7lXu-LVL7vIlEjWrxe<2HZJEhZ)4L0ev(0caNOk_6c3KOoP+YharX+U4~{!uL3PG)7gNxF;ke5!Xy0KxrrCg>INB@m#L-^KD}nY(eG+J|)H#9n%6=u#UfK5q+AIB&Kzq#w`Y@sNa{~G~p`42ZoQs5Vz7lZ063RJEz&VX8=RFSRJ+A0RT+tby=A85RiC!FMEPFZzyh+oavwm&#Z00VRpG132i=t0dcsAolew)O(nl8;-J;<{un2?jgxtd0aoo6HSQaBg&N9KDq5`RAJ!nvqL5}#);@v44Mqg?IWxYR@SquHa5xjJSVM@@5eO#9cyQQur0)A4KLsCBN6>H26Ih&Jw(uD_;-XyevP@2{qfXyfup_m8HNXyfXY?oUlK!6t_Gntp=+IL_6y6ylHLTuoP@J_($wX)M$~fpbwmVSjzvi*r#+p?_3AsH@PQsvp!_=zrCZW{;W-=Sv+&eTMU^j-ytCJ|r{^M;p+egr?_c1Ns)%v>k0gKjWItqYY~NxbwG9{55!BqT4HTkgNK?`M%pEz8p9(vEzI3B-(5G|M7QS6K0=*iC5NKp2WGD{=eJvulPBG1}2uCu`-EsHT@Sm&tB&F=4$#czT(cO_)g(m)Nq_DvBq7@61z{g(GSjbb#yh6+W7Qb^P}0jn!<Qfrg2wO@ZYNQ+PJGJ#NVp(IPU5Q^+`f~TD2W*+zaX-sQ+l=)`0yD)PJ;bIY9pe>Ob1J8bN;s>Oa`T&|cGj@E^yyn*Kxlah$8^Kh!6Vb2a^k`upZ;`Vae?z`3a5I2ZcIr`zZU=R$w_bX)TS{qNIr&5vde=gX(_+BlqFpU&er=tCTBP}|W4^e3+AKiYu4srrvLpr5M#qYY}irvLca*V?@RZ8ZHy8%^`kM$>t;(X<_HG(ATf)Lyhl8`NR6*KAOS+t@ULpJb3997nxvlUJY)x2aE{_O_{Wpx(CGuRx7$v+ser+NOU3wN&xr(@!NHpJpm~`E*jLk53zwI{Wlc*)N~&Df{lzI;DSn`li{Sb}9Yr(<|j%_%up6Uq0<p&Z$p}l=JS>A4NBOx`Z~`Jr`}X`z+dM_g1vg?x$#@-9ynvyKkZm-tW*JZSWq4_HArh?{{dg+2H-IO+0akCms}!cE4*=pTK)un>q*H*V^n?;JvKPzGu9DY42GSKS|9-dvBuT<$FJ()W`Q8M5(jyeTTANzV{l+zWd%^Xg2uXLFq%^`vs++eeWHVbK!fxpqww?dj#d2`ra2P=iT>SK+z4~&;K<Kf1Ip&cx>YElEN5p_2>WJzk545;*qh5nwoZToU7^5MRz}&?C|K=#8bB(8OOPrMs0fYUCAfJ=B$+$#&NEuS7PVc%RJv)O}oUG=Tm(9=4v`7v3fB}>~Wl{X_~8@tBKSmjv9r2aBg$mTkTu5OY@`IyPAUkR(->9S4W6HPy^A%)e-6wsE26dUQqu)ZA2Tl2JCO3PNI#=0s1FUGttJ?2>LTnKhXxb`uiX7pG132S0Vl+&eb#)>XXE|n%+YFeRDPKh5hx-)pQv8Cy8@4O@{tVqTZq(oU7SG|0hwCwQ)FKNz`W?hx41%G#qU}AJpIfpbhAc`uiWW0ew?{|ARK5pX%>_&<6Ef(|^22X!ioN(exi}G|fjFP3L|0EJfSVM$>a&UW$gJ4eBl0x3Ou}UbNS2P<z|N6R62;@(R@9HuVYA-Zpg()Y~@u6{xXo_B~Kn+w@PMmMVUdnvJHJN?tylRO;i?My1X^JyiC~r-918C(&NBK^;^2Fp1iw^s`UXlyl+JG39*uv`aasJ}pwtyH9@<-AHQMLKGn**g>vD9px(P%ay3BT#35NRo+R<m8hp&iMEz2QE#~t<;az2N4XO1B3Gi_<x137u0;8AB`TCFQHflM_LM78Os+(Gk!$1uawQrpSE3<uB|1Q^L__6Dbf{d34wEa<k#Z#(Ay=Yf<Vq6vF=VMdjT0P4W2hZ%OcMnsQWb4Pov2o@ma1tJ>O%E`^)#6}Q#YC}IGv88EZU4_3C^Oa)PuI9lLSwq8MFm$MRNt`(roHQ+t570d2|YGOWAa$;F)wfZAaVFxq|1?*|Y=gL>CHPNaxeev@2aAcnMuZyHPGJ6kJFPs1NNyR|;N9ms1`U&|<;GbQMLZm~Ifffv%+@Dx;->OX+$lrE<Dm@OHYH`cZ=J7QCBoqd4`a`vu+S#O_UlXt|*KoY;Z1FQo+C=fv(q`_p5Bk5LotM+edqf=|#RbPyd(&j`BDi9Ljd(F=m^b7F_n;q<bg`<&P#=qP$s@Kt(+j;4|Hrr?|O8jYgS^seB$^cEdUOcjC^^d60+3G}((=kzg+ryBZN@N4>vCeajHE4Y@vqB?4%9|V7(Z>WKer(Xnrq3>xLoj`vG{y{&}O!tVInJKT|=tMf1*qkV@zvxstjoO=2<rOh!&{@<`u%p??oI~eP7r`#3levH{rtX5>O;<CYE~PC5w=g}-WweNT3HCBunk(pP>MhvYY;CTg>u3kT9Za@aLO0Pag1eaQ&5d*`<qGDSoy{$DC*=v|ncdADbPp8@7MeZGGJ1eY1xrnVxsO&*xnQ{|F%Qwhw3pysW>1r($7!J8Kod8Q(vvh;aIoobo~CDMKf(RXzUFy)k%kHmH3yiL^e-AFILsVuR?+Kpgy0coxOs!#rV)Z8%#r3DdY?uMjy5CB2UJO`=>vHkYd)e+X`G<@oY+t3OR5&EHdW>eT0=F0HD-eOH+@HSg6=b8zonn3Ua;QOnjh(RnkqQe9A|!|zv+0v<4vRalZ=@uIMYlw*0eLT1!tRCri0no%n_VpPBfdCP0cBSr<l2>v&k~237%$7HQmf+=1jpe&FN-y)6<+Ic#b*CY-P4F=L?>1&NbVb9CNYY#pVLDo!QAO5L{p`GCP{x%tFD1<`T23>1(bKyuw^&`k1J>TJUPK$mE-1vsiGkxylroe&%|?>&>;M%p}ZBf;XA#Ow0^0w+P;1ZZvzFLFP8W+ssn4j~Qa_6ui^iZuU0^nq`8^%w6UnbBMW5@IG^oIn*3x9u$1g+;0vyN0}9ZE6hXYXfw*B1XHHT9AiGDF@j^v!`|o6J}&sUc|_QF^OWFI^3`}V(L5{otb8@m`%K!2-e=NIHdD+>!IkpW6w}c1nY1f~O*5|vz9wHyGc(Maf^W)KGt3F*9l>|xs}syg=6%8U<*Sp-$>t-$kL0V9%{=po;3x8x`>fi}1wWUs&M;@2uLQr6ug*5-nKgp$GilE=7n*Mczm>1t=hprp_=9{k-&|^b7W`Shy3|~5eiQsnzPj98Y5o-aQ@*;=Tw{o@l-HlamKe*|$cuQ1xxus-Y|oZ&FgKfx1vlpQe6zXLbQ0{u8}qH^4%0=j3wPo>%-yD&U^ni<cbj|7W`gdMVBKfiZYk(K5B34G-1HK3p9;I&B+a&h?z3T&QtwCP>qq3PN6nLF7r|Y4dv>32n=6>hJM+`#d6OrY$Gh`$<|R`oSjc<ui{=$mDp<+|{IYq~lna(~39mA5n7st|;(q+PdD{#W9LRC+vv3Cs4(9&+p83G+FX%o+_CvGU3>6&82k^({Q!`9(7$3}^nJ>%{g6<P#zcgQ)5rQN5NdC9^#*7vm%_DiO`OZ`dR`Rj@z4^&Z5S+kc`A74ssS&K<@%)SV!%PvJ!jt%S^S5afY~(ur%P=1=csw_-;dXq2;0ZjPBfJsM5uC%byieIZS@2{&kvHK@`82`P_*Cx9UHNRmv-u3p;_iID;Q4$G_u$R>V!?~~0^Wjq@}+{8@_gQkx8_BHi}*6$hI{kXf>-kuoXwA!9RzpaYj``}iEj|Rffw_Ryc^#vcr#zmyK-N?Rq$56iTiMr?-0C$Z{d6{=DP*&=G(c5_vCv8@8!F=j1&BT-~)UQ$9MoQ7hKNw^WHp&n*^KqA>N0F@WX-+bCUPt1Nkw*$M_LGh!5c>1)t={`A|NLpAme9pW?&$D1Kh>d486U=285T;7j}hAHx;=ir_1}lE?5keogQ-{ufvAM1E87O@5WDxt8A%e23rQ$z0Fx3%<{9^Km?lKN9?i-{Yw~lRpvsgg@jNd=h^y_&I;fvw1FmDd;|*_7tAS{}%i=f5oTsnY>nTEwACT_+0*8@O%E2&*KaEC&8ci2fm0e;a>%R<)3*0FXTT2|KQ*Fa=w!P7W|w4<f}M`mk2Ilve)u;Z0vP>qu`CaRB$QZCg?u5*4R6Fncy<MPw+l|Q1C%sA-IB5f+>Df@KJt3@Ckle@M(Td@Hu`_@I`)E@MT^lxQbsFe4XDCe2d=|be}_O><7GBa5aA__$hxO=stVa*su8;!Eg9G!SDD-!5{e-!C%;YzU=S(m*8J~tzca@8()3>qVoR7R+Vdf`05=ugs;#z_*^e<m~de%9YYXzJ~x1`&^Y*1IXthQ@IS+k&+@A_i2$3_e_^w}wGta(v%a-9#HMwvj@~<$j^4YNO})P$v8lY=`xGlb^%J?zeQhW219}Mdke~J2%X@^)1l{MpZX!R&b{6a`KkJ`2Yj~6Efxkz5+obVZJD=<E=T>c=)cEiBCq4eui5sbW^UoG}{O3DXHEG<f>v|v^LlAfCI-ZUph`V(iPsb3%-MWsaV+i6{_Xml*eVDv#RKmSl#(cek<LU3oSgMVm*75ZB(!Q0o+S(*S#FGdSPa;G-iS@<fK6ltkZ@JGU?j&8;O|YAE8B1q&73?Zq)=ql0yI^<e!;Pfxwh-Jxy0W9!yB+1VIYAG^G!DHK*EsZ~%AvPo8iyWGIrLIo<Is~Thu)59T<HzmFRjNCnho?u0`1qcRw6@h1jUmG5l<pSJc;$iqxWGu={lBIXYcRw^bqVJUD?6w!w&N5?(0K-d~Q?wD^|sa^xJ5K#y^~McGDSItKtLiuUH;}_tQA|EZ2CiKgTzHH2T%`@{y+uZ#wqNS3RF0_;QVd&lMWqZO-LQS3I<Ky?o)c>zY=+wbt{wfxKTB4r`Tbd}#GKP2J92KmVZq<fiv(ntg5{Umk|TS}Qbu+t7(k$DJBUtdAeI+4QERGukDb&kf}L!f;rtT;q2nj%>PaSG!)`Vdnl#lM31Mxq*Cn7!GT#(74ls=g;3LBj=Yk_Iz$2?-!Q0tW~}~KI-}Q8TroVwrlmd0epE_-m=yTjY|*2peF;l^im9ZZ$o&$FdWt@*SPdR40<w<OE1Ns_cnwt55r-t6&e?fih*VZa?!dNXyb<PeqlJQRjzT-s2FHwAQ!ERfi`XkUmk|TS}Qaz_sSUDqXW6zb7OE{&cyp^9DJ5*T<(=IxJL(ax#z~<zMP3K*EslGp>cdKdG}Vw#NYXBhWB&Tqt(&WqDOiqM^+c8<2&WgOuhI~^Z$QSY!YaL?|(IW&E|ysXyTXA+r?KMQlO5{T`(i@d#W<tHXg7^p^cV1+M`XMVR@;|KRYAdbaHMA>!6L-A6}cf>cfY;wXhCgpTOKTd#s5z7i~Jfo}Z}rcy4m;(A)&pM;l+XW=f)e*V~%^jwaLx>{D11%^qu|%|)9TmHQ@N{JbFX^p<=0YKY@69C23ikeSmGZR+N$E!Za%dtYs_RyY^!(dL1|z2YyOSD3n$_VCpZ$G<z^<aohF(^GBg=Bq8(rxbf%ZLwB37wy~BGoG#+))2>~KJj#Yv^s-*Lb3PNxlKJ==c2t<PvJ@6f%QZi8BfA^U_HS;h4xxK(O#>k^hN^uGq9d$BmI_u{tT=q*eB3lt0&sGsb>=UGX?z_SU0qheoH}r2G$MiQ)u6&o=ND>R8W6neMGwwpr3)`SQF911n6f1G%x}B8ED@|KLh8s(a#j<WD4{%a2#tQdYA(JOo0ZbKtBWR+vsQDT(rSj$^9z{_tOO2qZ4qC4zfvTHdqt1*KBYc>!Xch?ut!HtB+=HXmjdD?k|~b>iy29z4v<`BmZ^tM%oK|h;E>p<-c3$4*BmcS|<P9C!-I^m>XFp%>90HYr(B)EARK@If6N~t@nGO9R+u!Y}%MQ(N2Op(e~7ty3%ffyU{L`MLj4_FpqMnJ8eM)f(6u<Hj`N0-%{I>@~J2FqB24Ecg?n;?I<o7r#-1R?Ld1A?oBc8?=|-qbbr^(JwLOL;660a`y0&%2p&NDQXh)aP(k;1rSrwJd#b3A4x}O~p~D2-GeYi}nWF`dro*Wp?M0&mN6}H@wLcvr=$;xHK!d14u!2U@VA_wy3A$&8+}~xMDCnLYI#4_xEO;<gd(X+#3D(hM8cs)2qhKRVp(AJ{9WQu1HHg<^Xr|yynoh@3CCwI`O|!gbV@?)4nNFnfG>J|VJdNgx*Mq4>u!iPQEgeT^3!Y79Qaw$h3k5Hvb7?Bgp!tIH>3s1zlNJarpo{4QI*Aqvy1zX=hfbxd1+S(>bPAnLiv<_cmEyIA&Ja9<uBEf+9J*2PM!KHPql@Sk!CUAix_~aB+XZi@rQ&q~-6?n{-A0$u<#dnWJ#;r+LD$d&f)CKWbQLY3<$}xUe(`z+T_<=QJxKo#&;l7!'}
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
placements=[('nest', 'agriculture-fixed-sloped-nest-and-front-collection-trough-01', (-0.9, 0.55, 0.125)), ('feeder', 'agriculture-fixed-high-hopper-treadle-and-open-trough-feeder-01', (0.72, 0.55, 0.125)), ('drinker', 'farming-fixed-bell-reservoir-poultry-drinker-01', (-0.9, -0.93, 0.125))]
def rigid_point(instance,p):return tuple(p)
def stored_point(p):return tuple(struct.unpack('<f',struct.pack('<f',float(x)))[0]for x in p)
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[stored_point(add(p,t))for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,rotation_z_degrees=0,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values()),coordinate_storage='Exact IEEE754 float32 after translation, not hidden deformation; native versus final GLB bound unchanged2e-7'))
base_mat=len(PALETTE);PALETTE.append(('SceneOnly_OutdoorEarthCourt',(.30,.28,.19,1),.96,0))
v=[(x,y,z)for z in[0,GROUND]for y in[-1.6,1.6]for x in[-1.7,1.7]];f=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];emit('SceneOnly_ContinuousFloor',v,f,base_mat,'Single scene-only flat court support, no extra counted model');FEET=['SceneOnly_ContinuousFloor']
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
  assert -1.7<bb[i][0][0]<bb[i][0][1]<1.7 and -1.6<bb[i][1][0]<bb[i][1][1]<1.6
 for a,b in itertools.combinations(names,2):assert any(bb[a][j][1]<bb[b][j][0]or bb[b][j][1]<bb[a][j][0]for j in[0,1]),('Whole instances intersect',a,b)
 contacts={};floor=triangles_of(FEET,vertices)
 for k in names:
  tri=triangles_of(names[k],vertices);mask=READER['np'].max(abs(tri[:,:,2]-GROUND),axis=1)<=tol;bottom=tri[mask];norms,areas=READER['normals_and_areas'](bottom);expected=float(areas[norms[:,2]<-.99].sum());report=READER['actual_opposed_face_contact'](bottom,floor,plane_tolerance=tol);assert expected>1e-5 and abs(report['actual_contact_area_m2']-expected)<2e-7;contacts[k]=dict(complete_ground_contact_area_m2=expected,actual=report)
 tris=triangles_of([n for nn in names.values()for n in nn],vertices);rays=[]
 p=(-.35,-1.3,GROUND+.40);d=(1,0,0);length=1.7;assert not ray_hits(tris,p,d,length);rays.append(dict(origin_m=p,direction=d,length_m=length))
 return dict(instance_bounds_m=bb,complete_instance_count=3,distinct_old_models=3,new_reusable_model_count=0,whole_oriented_triangles_and_pbr_retained_before_float32_translation=True,actual_full_base_contacts=contacts,selected_visual_clearance_rays=rays,not_navigation_or_full_space_proof=True)
LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate(vertices);result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,.70);ORTHO=5.5;WIRE_THICKNESS=.0006
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
root=bpy.data.objects.new('OneWholePoultryEquipmentCourt',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole scene horizontal centre; continuous bed bottom at Z0; three entire unit-scale legacy instances';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
