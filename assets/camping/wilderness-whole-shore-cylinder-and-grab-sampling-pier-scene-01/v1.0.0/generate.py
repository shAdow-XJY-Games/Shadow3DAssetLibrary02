"""Static shore collection-device preparation beside one empty pier: three whole originals, zero new models."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='wilderness-whole-shore-cylinder-and-grab-sampling-pier-scene-01';VERSION='1.0.0';TITLE='Whole Shore Cylinder and Grab Sampling Pier'
DESCRIPTION='One static wilderness shore sampling-equipment staging scene, one scene and zero new independent models. One entire original two-metre wooden pier projects from a new finite raised shore edge above one opaque water-coloured base. All original deck planks, gaps, stringers, four pilings and collars remain. On the dry shore one complete qualified double-open-end sampling-cylinder appearance stands on its own original foot at left, while one complete opposed-concave-jaw sediment-grab appearance rests separately on both original basal bands at right. Both devices remain empty, open and unconnected; nothing hangs over or enters the water. Unlike the old two-pier fishing rack, tabletop baitbox and chair scene, this leaves a single whole pier empty and stages two complete tall collection-device exteriors independently on the shore, without a worktable, net, chair or bait tools. The tall cylinder is not raised onto an unsuitable small tabletop. All three original GLBs retain every oriented triangle and full constant opaque per-face PBR at original unit scale under whole translations only; hierarchy explicitly baked and faceted normals recomputed. Only the water-coloured datum and shore block are scene architecture. The narrow visible shore/deck joint is not claimed seamless or traversable. Static artistic illustration only, no water collection, scientific sampling, operation, closure motion, deployment, lifting, fluid simulation, buoyancy, safe access, loading, facility construction or safety capability. Rigging animation and interaction not made.'
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
LOCK={'harbor-dock-module-01': {'bytes': 60084, 'sha256': '405124a33aab044d596373198a76766a0acee752b3266d46dea748070fe4c14c'}, 'underwater-fixed-double-open-end-cap-and-spine-sampling-cylinder-01': {'bytes': 68296, 'sha256': 'b8fe08b154492a37ccfbf519793df247ae23a00634d6c6794f238f28cf499b59'}, 'underwater-fixed-opposed-concave-jaws-and-cross-arm-grab-01': {'bytes': 41440, 'sha256': '3d4ed8f15b6c551841f2686e714d37ead31672eb7b7130188a24861fa260ab02'}}
ENCODED={'harbor-dock-module-01': 'c-rlq2Ygh;*1*r1MN}*Z2ndK`EEE&S?q)X$guPNk5hPR_pav2k2nnQsh&;jG6@92+Z`eT*JF*Cfr~yT>7wiSa@~qFscV>5IIoaHD;`jXhKEHRJ-#zo6xifR;lsj`bta~R;896`!!1ApCr|t%D)QI9Cv$IO7tIKM#dd|+8SXNP1RZ>$~mDMwA(4?x$ipuIv6RAt5zEjF7O3SJ`4eU|eX+~c6aQD3Ytn92AWmVPXl@-)D)IB$APIgxHcp4z9XKsqBvwDu6omEjXmFluaB+g}LRaBNHPUMcAGj>O5cGlFg>Pd;NsrHjfs>W4T<&;*AKP6{sWohk{vYgytmhLmPq^7K@ykttUUuk9SxG7~L%1g^ivwGH4)t2oTp|YZE7F}`LxT>SeYD%U|DIY()vUcJmnpm~gc3eqyS-;9Dl~n^u#wT<holANZ>i-G~L;1mAG+daMo!dPW$xBp5Lg8RERG_PZxyh<%ekhoqmlw&)4(f@eu42X`Wva{t({<eoLdi>n!@=ArjXGyewwo5!B^9NOR3ciCoA@t37zsrp`Fg^6;RaQqU}1711-bc!bmFg5p{A^4N+VUsP1(FKKQ~yIAI;B?YO5Ed>Y~9&K`<|*l}M_U8!9Zw4TVFY|D7WeU8^V658QsW<I1|{2E$r|s`9DjHRUr>4N7Wis>;XJ)|4gG7+O4H;K+f+LlT!8Qat?VK7+G*2D7t99)4WE;^N``Ps+{e8KRq{yrQ&xyzUa-5z5p@o6u>%yd48Z>JJ#@1LpGqgKh&B>=>}H{(!+;K4LJ)hYZb0+_NR)>0EVXRniFKY9~x6t2(B<Y-U37@s(4j(S27@Gji56vR)(@it5VR3R++af>Ax(snjn>zRQm!omEaN$mkrZ$<EQ`nncH}V-D{Z&eA&Y3j_rhaO)pxRR2(e{$acR;dK9?4nQ-&h<<$r_Zi+`h&=ZxMDo)%A`2Bp6VV-}Xpa`=hZ`8pwn;RST$`fNP%unOnYURZf;qYMk2b1*L$l_)n>D{M<Ym<Y_Zfupa(7s@AQBGJIv=9dJsK{^)hkP0BtJq%4CdyC3JSu}L|sABut8cnBSGrGt!_6&ZYYv)1Zf+}FUZf%u^qzAjD-RvT<?zDMh(!=55b_jBl5xx9YH$n7=kYeiRED2teUdHWfc=^Xm2k}_)*ssPneK+;?UD6shX%UoL3kP?U;|CbFxO-KN<-Y)bAfGj1=U_2MFcmWegCC27?(h2)oUoFqol1s2~z;gb5lB5RT;KH^K&a(cBCb@<QRp*dUm&SiJ#g<7|Wt=<dqR7@#1zI!L|HV1P(4FVctsf`y^X0rJA(Mhs98%`ibE8p@nNc*k9lx+B;Ck^EpNmv+)lTLAhF90K#VogQEPLl=v3OUl7rvMqqQBBmq3y03(F-}&2$(&I=N;IMRGFV@%6eWlEFk4u>8B4TDMF{gA9bIMjCX1a^G*OuaRY)H7SZgASy64rf9EJ@k;TFNGtB&_FVVnf1A_qddeuO-ZEC1R$#h?y=TX0{UX;%nEgG_fIN<7)|@z3RD@CYB_u`x;+M*~F5B^|efFNSNs!moU>s#LQM=HnAaP?rSe*x{G+<9%Iw7A>opbho*fkVcplnl9Y|FrEFqJ!g_8dHYCh+k4xG3TEfg$B4)aanCT*7W-BSjSe%HM`P!3dZZQ^Do~-*azl)f~k|*nHu{iN$rh8n%OcxO|TZx&)iHNzcy_o4PVp_XmY;W>pTDxLw-|=MKm+fmJX8Vqa*<R+!dTwl=@?@raT*_>(@nmKz5i{LI%ybbkvz3VHS;%6~$s%UYx}HqWW)^#{_GI0cJ@<;3JxhDCz7~5<_GG4eT*6Ej5i?tfnLQ_qnETp`neHOiHe#R6Jz4vVeeU*TeX!5<B4(evMa(|Sdvdaz{+#Z~O!v5y*=KD}X0{SB(_O?&7ZEdCiTH%lUh#1FJ6a#7SW-S?@^7)%Zk;A#(j&pTuY`5q=WjmPGUG^iTJLU_>FdS%TDq^4neK53GhIZ?Y$fKDE@DpEO2kZe5r1@hhjeU6IM%Ff+Sd}+eN8M$+4x$@CYB_u=VoF<!c6zLl#Q<?%xooMrn`ulE+S^OlCs6(M8wS3o=kJISX_Cs?#uixVirrDtgpr5#FLrsaS1bBM9gd@W)>$R=Dzk~rn`t~?XuY3<jHzpW&4gN>%MGX6EWL&M9lUwPu6o|`;;d$-Q!YbdyOYETZx$IE@GyOh?%WK{N=C$>JOk}%8l31^PwAeUwu%b{phleuB_X;anF19Nwg2`+TE3PdoR}Q7cc7T%DTN9oB7X)jc{e%-i?ht7cD&Am34bJzWe<_>Fc_&xvmr6@bj^0JGim2gBu&axUunz6Px+#7;s|~Cr-@l8F%B9Jsp|(*OgQDbYvE9uAH)`E2r$~$|-v~GP@sLIb}~rX6u71r`88YX8v_$b6qE9@#f0L4sLAx;>N}=PR#B{S2l6t#AGXrt;3GY)?{0zF)el<IWoJaY?*Yl*nRED>>hVyw$3;*TW4(9%s;ihIWk)VZQ0l}wca{1Ta#^>?h%Xa3y#e82wSFm)?)jVBeOlrk=efK$ZX%VWi$WOe(lI?Pq$@e&$t`2HQAP#e_ff~Q?|_F&6U|b?#OJNab&j6*fP5xU74+cw#?QCS7vLnEi?bRGTS3;nZ=tcvpvg^*}mz>Y~QqHc0al@+tY1XxBb3JBu+=7U-ECF06jOfil+`Mbv_RD{+ny@zM1V)=N#+nk2yDE?0Vx{Y#b|d9Nvca%WQAXJB?#!1M{EVT$x^Rem=9F_xI4ZUR$Se_<SAojn~(u!T1&%-^v`{sa{~8%=odG-z{dJdiC6YnL2sIo9#F*@nA8(TQ>H|jJJC2Sv=d;+g;Nmek|r+%jW*djE8#dnZIo7-R$WQKNj=5#qO7S^%>(^F8<1lH`{TX;-}g3t>XGvxJkDDWVScgcB*ge`jZ;R${fcj-ZI;p^G@S5cKu;`)mvLK>;LTf<1~&_{4l*l>rZBTGrm)OW7i)&2J^ec>{GA)&#pgC<G93w#r*EM{$#di@oZb)*!73aU$p*YwrBpbt#9o5!}O}Rwq(}-+4aY19Dn`s*B^iV@z<aKYwM5y`OE+O<$wP2KY#h3zmj^EztAd9hxOKa+4_^&-kf(D=kNaf!}JoZKbh^#_)hhI_vato&g{XG^(V8vIp<XWcYpq2devK7GVA~B`r|at-(~&L_GNyL3*xO_duC7DasKY>57SGu{$#c{<2%*=-Pa$zrm}s<bN$I|Z_YW@|J~OgrdPeSCA0p|u0KxW@V3u}Z-^yqGpjmIywWhghDVzQ<9yt{IMJ`~X>A<Gv1yaY>(|e<jTetLnd4Z3aV)2C*qp8U?QQk4YtvvHW<$quY}%M{R<diw9p>ZK#@L6|&y73S$E{7~IB~%^ai?*3T-9%HtCw9HKc4+~_T$-)XFs0(c=qGjkLSNEp1Y1|9=mSs+?Z3|qQ$1zs@1hc-Kb1s#Z0d2Q)4IEwWRX0>(6LVo;kCvHJAEl=BHAg?B6L-{;|s#OZPKno$LO|b^tmzWuEJKmiF2nbISF6bgt(!WZYp^W?Ad;W0xW;sTZVkQ?KWtb3MQ0c*(NPb$>k%U3Sa${~x1s)1K#F40|+TFQ*(}Rob3*xt{0iw@!;~rS^*aVscZj=c)5%uN|1SFE8tPY^JhXuKlg^MQa=8dY;-YPPv{(v)2Nao|m?($xXf1&-lYG*Ynlw^n6WO=ccUZ;g;)o)BR1Jil=lLV6T*&?emt&I4|11JsI~Vm&X5$r2UFAa~}V?46q~qlVw@_>v<;a;*@*GKR}U{)C<zNsZY*F=R4xx)a(99eTp1&ulV1-{gH&doN`J0|F*r7+C7@^i^+G?>-p;Y;2>t-9c4YwCRBFHz2aYAFKHM1JQ+VtEQDm-o7~h(;$OGhzP*0@o3dB@C;iaGGP#L=Q}*NEkN^MX`1hZG{O6zl=I5Ucb^FFv6wZq|<;QfYi=8~-lcJ4O)^;$tt~c?&lG+_h<*e~%G$_CFbvsM<=eh1@@<hB-{f4^ZEZt9+lj9`wSE-#_uIJfz-5)WhT+gRJ<$AvFUYCr2ULHmHhPr~pINB~IH}!fRI^Rh1OODscN{*AvwI2FB&vm@>vT0|RFI@OQ!d_0fjt}DpyIjw+AUr<NUi-!5re4o8kMg{5XKO{uzPzmGq1!p-o0EP@ludh{FQV&dyEx@~p5gG$)}q9`Af20ft)KRXj+eeRd2+rxTYA2B<)pnK5f8eYnd|eqy;JVTzaRhq&GD~&HRdv9{)R`#O%EpXxiMA`se0I}W2x0|(4N+W2@?|SP2Q>J`WUMRlW(p#%~}x1N&KduZfEj4-uXVp>cQl?{VBf<w?g4?qMgZgdsYu7*YkOD`E=`=g-JV@T+fHqgUPkNw@sU4{k}c%Y?RKmzN{Wh{>=v+65~HtSC?pK^0{rd^k(&7^6dFLCFXzi!i9-;CcpgPWkswWOs?B&JFKr8oM>lq-JaEh$@P4+o!8XW_15i7uIIz*!Q{SwegFFY_5JJn_y4AU3*a!=o#gJ&1V+GUID+I6kPoBaU}!<I1@wm9pe^(u*#q{6PS6F$kQ@VpK|xd41@?rNus5`aeIW}Dfo_luA;^QC5QDzZAC7_{Fcgk~<KRT-00C%5vKj0LJ4175O|muY3ay|sbSK#z+Q6Z3Aao?z5pv*2*ar?Ec>o*@2f;`fOL8o9h2vou6q785lOPO(U^vO)5QSsOO#?^{fD@n}^nwV<2pmpY=0YLKLf8q4U@zE%<Q~um+QC2wk_-aEHE<J5Avpy~;X!x;?jU&wTn!JwIWV2%bhsW)fthd_$;;pjm<#8_3X&_}UKj@xU=mb771Y3Ka5|g`=fZ_>F<b%vghg-z+yb}3-LM4ihlk-&SP8RXJWM7z8U6tip%Q9I)<QW{!+CHi$xC4dTm)yq9FlY361Wpig?S|B!F_NxEQcpaJ_#4VWAFehCAk#ha3$OW%SbMRtKbp15f+nN43ERDa4jq#xd3j5li_k$NOB>R!F4bVrjncrH^VHr3+9uY4<+z30M?PLgSF5KJK)aPijJS4HGT}6NN$4P;dyusz9#uKY=QUSGuRj3qhohm4eMY%Y=oC!GrS3J!w2vQY=tl3U+_Kr0)K$QCfE%3#J#W$?t}Z`Td)S6gSY5-7oLF^;1!auz_ai&d<tKY{0d%$FW^IXhvYl34R*oT;eC?t!yfn%?2R2scEr!29k#&c*p80<@jKWJTas*vKSEpF4o$HwHpTWBz+d492;dK}6Rv`9;NP%{j;G-_co8;`+yIDgz^?c$yaC_BQ*a!fjM;b`9S31G&c=x(C*rYKi-%*7WDv*Vp_q@wB#Y6)!|+Hvo#g2_1+(xF?1J4fgn8H#i?A;az@u<54#$yr0-lKDuoNd_1x~{mcq;w_d*OlDjbt~BVQ1`t5t0$?ieWqghmahCQ5=N*us6xxcr;GJ0_;Pw4^GAYSc7v&&cT5=3#Vfx$x1u}N8l+~MY0Ny!I^jxP9Qk}Ps8yz8b^^Fg=N?YhvM-hkH>>?4CZ1E$s8=fLM+E&B!}Sv_$aQzi%DLLXXDHG7CuAr8GHm^!P{{@$@%ysUW8ZUQj$yYM!X5{#J5Sljdge?o{Q(>rFaGY6BpricndDZyYXIJhRgABT#2i3Ek1`E@kM+UU&nXxT09FcBzYm;fal?5xPasWya2DnJ8%ifC3qFygSX=KB(KN&a6MjwH<P>>H{fl!8Q&rK4&H@t;3j;5<O{e3AH?VJC6X`U!}uD;aUIEZ_$IEwC-5PX58=}|7w^Z%NIr(=;0nAPFClpeK7|YMS$u%x12_-&QJvJ6B)`OuFsyp1&MHhtTNP0|sc$htM@RJq{)Ej*Hdosb)Gn$>0Ug=u1N;O(!>{mP_&xrDzoAl1RWr4_YN_^C?bUuNOC6-TsqQLQMOA@{sbBF!+={=_@dtj2U*iuXf56Z2JKS0AslLNK)sMKF3aH;n{*HU7F6w7QlBjZ26P2fWlkBZ_RfQ_3dXVg)EY(UKszM|~s*TE5`>R7p9-?}x162prnq+HruzC;oQte2#Qy=5L>KoifavL6?{*7H#3z99=``AbIS4XKnbR40MRD;w|l0((eYKR)9jwN}l8mUI8W7JrZW7P@jcr`|iBRNi;q)t}j)g+RWRGFHf%2fr)3U!K_qAFD_$y!yViq$~XkJ2nvO=+r{NU21PrZkGq71J4AKatASbQG)Usz%KwIa{5oW~$TF;Uo`Nebo$gm>NK7uo_P3ICUbWQZ<><G&(nf&gl9RsXUyH8ETH2tIj2Pt~yJdt<F;yle}16pe|IGs4GccsV-NSsVme%k_**UYJs{&-9YjNb*;Ki-KcIOd7HXf-J)(+caywZ-J$MO_oxR*KA@JUi_|&l3`!5FrIhYcw^F)ZT}^2|ox6z6==xi!yp)cM)P3rH^$5vF)N=KpdRWaPIZypVEmNnfGbx>~E~WHOwTRM9YB8mI>D)3pqw5z@`BFNTsmIg`wVLE=6<4d&8nvF}diAtgr=C?WkbFVaspr*3^$N*X)JtlU+N|Cr`KEeJy{_I;?~!~@y`$b$@2gKpexg29AE{5(Hj>-aR`rZ}N<Bg8TlEE{kJT1RZ>X0kZJ=|{&>3C7h00&h@r?RheW|`9`JMVkeXahbo+SCCdR%>_9#tzTtyRxadQrVf>237^rO)WxS9C_#ze?rj==e(gpng_=ko-gas(w@3Rg=JPbYMUQb_(o9a<{-Pft>@*0xd|k2<#cyBd}MX4aqivR)M_(Z3Fv~+&9oJ&_2*HkVP^puz#Ra;J`pvl3fFb1OkEI)lZai0-Y%x5a>Xub)Y$=T?6{RpOmieK;_PK1Of*Kx&(TV>=DQg92)2z__sQgjvrOG!1wAGN)TvDY4<=&O8W%%qjXT98>L^Au5U@@rgU@*6fQq9{jM}Ao8R7-@SW=hrQfY4VcpmK_P&(OZ~IGFU(5Vfzl53YaS1bBM9gd@X7gM9QZ~Q6FJY#;h;x>8Ovi?VSKin@?Q03^z9yEWY<w+c6H5}-b2G6aVWxXr%Es3cX0{SB(_O?&7ZEdCiMZ*!*6G-gvhlTqYp>iV9ZM3{eT}cBY+^~m`dTJ7B+PV=OPJ{*VrDBbo7j*t_q7)@-9`NU@0-)_+LLgbH#Vl<wI^ZS*Tj;PjjyF_VoAb!ZYDM)%yf@S+4x$*%vK_1x{H|UB4TDM5uY)+C><M8Holf{&*ev^V@blgukp2%O)N=RU(3XXgqiMf2{T<p%xooQ6B|<IzV>3KyNIW?JZpuC4Iw{ad@bY^CYGdZd@W@YOG19a#D<WK?r|v_UklmTO3FreDL=t{En#CTDHpNW5Ha($gnO}Al5i38wTM|PNw^n_4G9;q*pP59=4%NTu~-r@iwzNTUkkVwizQE{wJXN<CQqidE5`O6Pu6|ez9wR}?}(V~WuC0(#`Y;sX1d3v%=Q{jX0{SB(_O?&7ZEdCiI|>+V(d9t#Oztulj+$k#-6J^S@&hny&`7M(w?lZ#h#Nrndu&vFw;fE%vNG%&&eX@zV>3KyNKzto5enxdoq1?v)JcuPu6|e=Xw#d&)p(spXEJS&y9Uf_hhDfT*~aTwkI=NiJ0jwVy26TnXN>ev#g`V{!S=j_P0JyUU_4Ci~U{ElXYMAcRvxcza@IIz83pCp(iul;}T}Nh?v<*%<S)kBIdsKVy3%@3zr{hv45NJ<U7|5ve>^nc(U%x{#`@F?B5+k%>FIIll9!#zf*WJ(>*R__HPZI%xooMrn`ulE+S^O60!e#+Wzlp{}sQd?f;&w|9iIn`$YWp$NxQl|M&d;_lfxHkH7x->yN+w`0J0q{`l*UzyA2^kH7x->yN+w`0J1VJ~jV+YJbK1)cp0wUw>rlkN<m^{_kP>zX$8bzaRg8{QL3m$G;!{e*F9K@5jF%|9<@Y@$bjKAOHWK<KO>1M*sI1{oiBse~;1sJx2fc7$v{Q_~o#I`0Twm#y&W0Z_ACR_ulHtKOc5rqJ7s99b8$rcjIq+wMn#J63cOA-QJ6J`)+0ZTv@kwV>ADyLr1x?Ztup%p87pRZmiq8@q6QrPG8rJ&2^pl(}^df?cm174sLAx;>N}=PHg6{W5A6~oH#MFXWWfb_H<<CUsq1q(~()cxpK;$uAH)`E2r$~$n1V}<&-@gnXM15oLV0onfce1&2^oa#hWV|JGim&iyIriI5E2)UD?Em6O*khwhlWoTa#^>#<bXd<jCxvvSrfIV)wNpvwPf;**fFMY@M-XGyl~3=E!Ufv}I$@)Ozd4Y)!Uhx<@RwFE}#WBW#)OS&Qvcj?DHfM`rt`BeQ+emd*TA`?VvpJ>8a>J>zc7)?`~|{&i(`PuVhyH&<r&xFfT5#*x`NW6SJ*bY->%+A>=oT$!!Ow#@wN%50CYWfpI)%=RotX8WcivwhQ++5PCsY)`jkhxfe4`TNQp-t%tProlM%-*<06j!m0*#yjrgHt)E%1Z^_Mu>|8-PUG-*+}Ce!tCwAy2IKJe-8+qA(<bx1^H%-$-P^u*-mXnN;~n>w%{%TbL7U8R;(~GFPUG;ns^8vLFS|B=Jp1wN$Fm>Lemwi}?8mbo&wpV&H~#&A{T<#9*x%;;fG<0|A8@h5`vG5ect7A`m-hp%aCkr9ivQ620aw_(AMnh!TY9gsc|Tx|!}|ema(F*rj>G!_Z*qA*V1JwU1M2zo{|~+Y(f6<KU*EsJe|`V{_5MX@0?kM^gPma)*bVj~slQRPC$xaJB-_H?&<ff>N0J?(J+w=FFQ^?I`ny91LYKrhhz^EBpeuAI*&PmrZ0G?Ik`V|&bJ!IElnNnCDF-@JIsiIQYE9>w(-~dgnaW{0nnMuspclzrPyqSR6LuoG6DWw%T$@tb9a>V_2lk_M5OkxIOXs3=M%V90<(70rp*I``14s^le$XF|fWagO!$3F+j)oB=N5D`hhT(~C9UTwHz^KGGnnuwv8pgm$P)f2CN?;t6!DNz?VIoX|Q(!vD=}-ZK;BX2G3u>W~QaOyLG!~AfG>py-qBFXFJe4cy7z9&c8q6d)6KbFuW<Vd3eIN!^Py~G`9SK7yjf4{@oeUEwO`&sDbVk>oK;<EHRKcvo_mO7Np}(_q7M!2>=F&NEE?fYYk-Q8phKt}*SU_?CTmkbF-&vYZ$JKBRTnjfPz8Q5r+yFPjVv>vDR=5rBfcr?^2Y17HFb`%^dI0XBbUWNgX(3!m=@L439-YzkHzvNHbS0JVf_vdXk`KcDuoRZT9FlY3G*|+s!apdT4Hr_n9Im2t9o$0cPCB=Q&glB9sC*$EOW>izH>n<?;|W*+aac=oEj$IQ;c0lD<nyo|o`L6J6Uj}m5jMb!@G8ky;bqtiuff|S--b8fO?U@BAo)S!yG$R#=OjOePhbr^36D_P2A@)TAKs$$3cNt+Svt3d&glBLsQf7%Yv5z}48A7$HGBzQz*q1X$;aSf*b2+xaZ0OT9i=*WiPG!vE~Ss?+*UfH>tCYsIy$z({{YAkvQ_', 'underwater-fixed-double-open-end-cap-and-spine-sampling-cylinder-01': 'c-rlq349dQvj3|Q0YN}k0a?Z%Ad<lB3oza60ofN3B!H7-AOj&2CKDDB*->!;MG;XEabNK&Dhe~>f(v@xSM=(=?kjq6-|wsHNhLkuoK8nR@AKaO{m1#F{7$F3&pB0feto)on9MDmGNJ(hJkwNxfp&n?CyyVuEGJY^5sv5dUzRgBTo#Un;?Y=6|D4e!v1nPe!ZsIou?;B=mlcO&wo(1Y+ZMU|y860(Ik`ED!m)}-v<#h{eeF5Rb8{++@Blge?NwBf(|^XYoU+gY+?F$0|6OiQS+rRHg~L5_`OKQP%W}d?;;~Q#b)zV{pgdX@E{o5OMN4Vl5tXH-wu+KyEN+X1Lor)nEK)o-Y>O|Al+CrpOTsqXHykSqmD&nJWyQ95RNqL4DGkTNw$f<X+(^8#I6@v3<q_-$c6LFyqD1d&RR_;3!N!K*{!^lp$!Cb(2#xE1s&9@u`sS#sZ{y1hEyYVBMe}VH=p30_61NpCEsf|oT^zyzERMuWZ1GrS*cL4hmtil<ZPeSsXgnTWU@OPbRSd9|MQxEXtPtCrP-#WjHm5Wijpf?PW8sR5%2+sW5&l1ng9zhDqI6swx2-5t9x95&m)eR-Ly-kFV{>MXZD_PC9x1DgR#ps)Ru-0q$73%hhp^`u#VM7A;d+g<sQO@4gI*M=sKidi@R#_TXc>CMifwaZI5a)vlojk~u5C_aNx0Zn9>QQm%SxB#(vWc<s&X1qs1l<QibslYG|>u5aII0fYK^KgwkTXYysUU=sC*JPJ`~%w|35Mwx5e?)S&91YRo$tG6o+v##9~-1IJB~GQCy!Zm}XlnvVb~|``S=(Xb?2F7MIy77FVKAv@&js&e3O3VKio#DxS=aj-ZCp{hW-gO^7Ut#_j*pee~AdM@ut$4k-@lMvb)S-A$*yFkBKLohhLiAB$GbEvcUBl>WFagfkR}R9roA^;uqO=%_EVqoZ)&a?<~@_!w-JIy<>as4T=2&ncDEFI`u3g)Bj3!C&Z-V=V1V%?ZU8RM<lCc&Ml(tjlICar9?)k_2NC9(^e0Y-xThQf{qxnc_SrQWlAaOP7*{#j({$S(RL4PW2G$`6t25)w@rr#`Kp{X@v1T>K#dCO(z4jI$4RW4J}1o!#zmO?f)x!>9E()O^egJVga2>(i5mSQc+$ST56jU#gdzYT7$|}VGA!P$5TN?m9XbkpM$V>n7dF}QFuUAjbh1_Mwc$YHb|%{;-SJwDV;{jQRE^O#*<{Nv*ctt6^|$l#fPPPFakSJFSV_RmPU$e&Fu7;aJ_?CiDO(^6Y7$x$__1wV16jBJj)h^@Hl#c_>71X6ITWmi^Jh^L;q`?38z*!LM2VBi?l}A|5p#fWo;1YLMkeWlorRrxNw|d&voQFb6vUaTu-hy*O%+h4dh}uVp1_K4i_#EYeuXuQ)fqtv5`uu8hwG0r;jSHSYI{d(J1n8)Ok4SJS^NiT{QBJD7ZYk1DB$B!o=_uM`EPz`Z_jmI&Q{d!_Lo6pJZp#c{8U!Esb(>qOr)_NZD)*NaX_b*4Imm_0q?pi=2Z;qd6MI-c{Iexf_pRIWMj{tI(X~S&^sDiVFHgVYoE9SkHiA2-P#BTDq}YF?|U>n-nt^D#G=8&a#4>P;sa{9$6GF$myS6mF3zB(xp)mp);0ndo(s%Uv_8ya%oX%xMDV{d=%$b#;?M-L@m=d732(^K6K3R$ptyIUGHW3Fb=1mw%{2j94gkgxDD@TFTm!~`;QnkZTPVC?u#Pf#j`OQI4DD_GxTO>E~nzEDk-dNy{c-KhIG!X3eixG5M50yppw8EPG3=^BTDD1V$NXI5r>6h^YwGs;Id-<WRaUwUKkr2#{88=iYC!n6E9!%sw)gt;OewA8XJK@rz@iw_P!2#ApM`)?h1HZ9#1ZA^V#+P96rC_;R?9iw9TL1=5u(Q9*@uE%XLsEtD4~h+WR`I{2Y#e(;jf*StG_>sB!Y9oAmqbz5pI^In5;b2*;v^7Y`||3{Ocf0*2NUQhi41q@lT88N;BFxqa!*1e`vH!|MvTB_qQT>Hqm$4j*<qAQ_q~eKe0Z;P(4Ht~$ncCaw)|`5D4Fh55(jXFUgXWasUDUG5_?>P(N??hN?tPM6au8KZDSf%MJ}uh$>I=y~cG(S#6IH>zY+ZC7Af(s{R{o&)nZ)4_JQ`~jcOPJ{4Pjlt!2JNzDB05^I3RVnfLaI9XJBz3Ngn)C;}!hw3KV(D@@>{y{V(3$CzLgv-K?BW{7hs)^*Nm$w+SA4NZAr`Mb$O+>okD4-S{5U<#<Hk=KJ9rG9Y)~1nmLo;v<E)wV=(Kz$#kr1)X3K55YT9(yr_DMqW-a%?Q_};lu?Ie54;+FX$S*uCx9zWKJ78>^R*N-_JL}PSJwi{by6Sv8Gn#kR(Y*ND&w9&lL(86wmc7Q7UDjHz&zOCNmi_f=S$c_Pz41Uz<4${hs{P0-FUyTO4Ow<(WZCJetJNbfrK~q=NU_r+omVakt=1#GPOqU=Uwv8?UeZ`^*D#Ttf%;@teko#ILJhj@$`EdsvyM^AuOY0rZcuQS+q`u=ZH0>PcNNiC`k;lCbLNC&Q*n{1pM9#Yx27yD$3A)-l+Pku>&MdtwIH-aKL_I}6VHcUhnrRz9*4)9J`MZQ3n4o$Fz_cg4;?*Kt4O=s>vDR$em9*tBXm_nzx4+2NG?2O<01l2(zHhLrq_vhI`-TBE)N|9*DvYwuh;MQ27G=xmB;lC=1d(v)TLi;83*F1dmv`JJ4L&@s&{vJt9PF~bnuwLla4rm>*xaMz@@StNVmu9w&TxV2_zoGr3cdGar!+0cfj{oBI!Q5NP5h7$K_g0BpgmpIuf3M*M%!eKMuj2zGQIVrGU%r$3+}nMWolTUboZbbLtn*)lqOz-Pv6}ztiKe`>NLPwU_l2EtjWi+2;=6($8C06ucIOVYa`|yr6tue_a*jH}3(KPfZ}5UU#|{C`!J7$EVLszuV(?c-&6A!(;b(bE%+kY3%lT9C#fU@L|+53(Dm~H#<6D{G3jGdeemjRv%^u|L5`Rp~P`uBQBR4r>(>8ad_(pWx&EfOsBTpJeE#pow0P(ArB6p*BDGJJii?S=kuT!UfcE!IQ%{b#xa1G40u81&|~SYswXTod%)qz2&LN@@Hzd?0A6GGG1s`xarE`L+)j_%gOl3j^1J*T%7Dv(v(<&y)(&5tD(AE?4$}j;>WHPUPNj3yArL;NVS>Az`UDR+aoiXUs!LQj<E0zbB~D^}g5yN@x!oB5>R4hZ18KGNJA7E>9=){Pc6U|iy<RW=&X>+d)fG9W$>;U?>MBczr|xl>?(a1ZrNiZ{GnBrg2_;sPT@R((f!n>ldIu84)|0+Lfm=N;yYsKb(SMY24AkS)>8Lt&;&}j13T`i*^gQVsR2~eB)9$a5dtcQ}C8q;R49g^AcKXt1P82m9EJ`8`+wG}!my4!n)j0!CPbh+Jx4({1IPFKd3UOGi2O5RlU#0nOAD!py4vdAvlg_8t>m-fW2Vt)|d*Z1Ri^5ZD5uvXaFhu@<-S73#>DFI$Ym1AB4&rjVGj7t=6$t0i)r8Y^)N{+}uFpb5p9fxt!{<Vk#`M$q(|^RxK~!oz3NDY==?!507(?lF(ycL9z>bsC=}0eY(?@XQ8NlUp=z+9*(~A>_9mnAF2kM$#PR~&;M4aBEiUTc7GbF-Q-#E~!wAPaDuf)N3v~loTml;PuUr6Cn$c+o?fJc|bDnapj{QdySMy_yD)I{OP6`4L6eeQaRt21zPisGt6k??e47`Dr&4?Ez%RS(@k)z{K#b@d{+@Ir&?+8OW~ulX|0G5Qg3lpdeUkCj1@3#2nmD@vRN{`53(S6!4~op@;_T1OmQ4h!QjJwRPoc)mIn#pODxSUONx^;o(bZd^>_>8hTg#M8A;52YK+(}5ZB{G~{`>l;ZtV9f!Hw-EH(2Zc-H;W6Q|xpDgJ6JEjT8^+I>qkr-ae;*IU<`Uwv+3T$7Ox^qH8?5e4*)#6!(button7^5+UxcoMaKg!ul2p%c;?OA-Qm<H^<UoK<JV7)7WYTR_tt9P?snU)2M<@1wFf}bR*xPWc>vU$`h>t!djuYL?GTuz-{El9K7hYI#V0rbtsSf%02lPNYTvFO(&`BOD9g3>_j>CQ!6Wy_HBWs4aK!$2U3*mhcX~bEqv^lP<2)+uai`Z4e|>+i&v`Wc#~tiPv%kk*9}zh+fBMZh%lSJ}gm78taUP9|x#+&=Q5^s;iTy`&0Jq&&9~nEM2JqVYsA>phtv)q`i)?r81JtXC1PAat>!Tt*cdh+Bc8|9nRdi$rJPw!Rs6ybODyV&c>h(<3S|&q?15SEgWGjCgV92O(&}PCViEH=Uw6i~+kdX0;W7qVri`oCa>%NgP`<pTOJDTKHA5+BSUl+5#@tC!l{mmGv|68e5{XdoYf8&2g_-F#3l!fD@EF4D@w`uBQ)*sD6e~vhg0*#?5+NRJDn!^du9&LMQgTFZjTB2<U$3r7%4eijjgX5q9w1Bo~+d>mK7Mj6{XitPzdL15Ew7oiaBBs35#q7_y7BTyqG5K%qa8va$MNIy6G5Z^jS)1A4jI(uUUWd&ZDe8}>{zFAnWgL9;w;=J2tsf1__{L73>ule)TFQH0c~<9VK4~N6($+h5zN=u!Kp78s{cN3Iy7`!WG9J<Lp96`{|Mn3nd#>>AC0@M0K|;oV3~iPm?p@GQ$}={uOR&F;Uu^tDg4>nxwtId{aQ|iOzO#Lj;~?XLW_^+zPZ>|>*FVX5k#U#RLzA3e86S7sh$PpEjM@L5AG=AJ+x_f5Rm$A|agAn3nd9JjyF$tw&%RyON}2O=>aL5V%=z6oZIhI_PS$;SnUuNS$X~`>x74nTx&EpDGUj<iagZ_3M~bJ6d0taqWX$?N`IRy0%uVG9jWtKa<WJ0+BVuZom^DYl)PG{u91&9-h*@()Oz|XU%@Hx>g_t!*#FSrR)*KO2oe;C;h?we){bfvb%k9dT>Yw{BW12@C2N~0R<ao-M<~8R<#-tCNUm26maGl7Q{aJHF%<Zz~h?x7&nj>P418a_mIi9RJBIdlX=7^Z{%bFu%t`pWA5p%t<=7^Z<mNiGjT>q>&BIbF-nj>PKkE}T&=6TJUBVyJE)*KPXuGt^tI+5`!%Tqe{X!-Y`jEA3jug>{hwn_QmzN>Uz(`TBL?SmKS{OUQ4rMz-e=d|vv-7rwbUo=>y=jECCI|j(O<Au%l5jXv{`(7Dyoiu&(Mk(*^QITMO8ShzpXM)?6aq!}U3GTm)M}G@Rj)RQnuWXg%c*^*O=es01FEal0>>f$ZuZ;J6)2mu%WX%3$KX;Tew>$H&Q_9@`Za<8YGRI-`$+M))@hsg{CS}gc&fm|GGUxaE{8dusIw{z=TFP8+<S%2cTWVLvT>sR68S^}%ILMgiBgIq3Jg+G)GG=|C{K}YghS$k5CVyhq91&By#H=|Yrv4MN=7^Z$K+KvWVv47}{;$#;5mR3DYmF++5i#YLm^DYlyiR7#5i!*p`^%W>mfMvv)j#)N#x##O4l<_s$nlgh&1=q!j7c9jzcMDB;X08q`?KbVnA>H|5i$3lHAlo82i6=Bb39pdM9g_%%@Hx@mo-PkTqmqKBIbHy%@HxzEo+X5x&B#mM9lMuHAloeA6aum%=4NxN5rfTtT`e!-XFSn|9Sd-p$qPRCTQS<(PzUiaee!$8?Q*pe4I~)^zCyC4kwNNMxS*b4%fH4N^(+0f1?lnPOI`w8U2kuxQ|-ZX3FSq^ue~(s=lX;{ze}fb5#sdMt_+PkD0iZPr`7Vr06)t?L6k%{V{ImG1nfKaXbI6c6^N6xsBR!Hg4y>*3Or4JCC_`-VNJ>G9SZnRHMJ7KdRARGA_;NFNu$4^q0h0Gx|&Nr5XJtdDo2olKRn%{xTm!9cq$#)(rKmN#=!Sm=~I4erbmJrAg+gW|*g{WWKA0`L0TILpAD*@qTn2`lDIUAI*aPXcqKGv!Fkk1^v-1=#OSWe>4mFqgl`&&4T`D7W7B6pg)=g{n0Gwk7hxCGz<EpS<oNNg8pb0^hdLxKbi&o(JbhXW<h^63;Ls3&>zi${%98TN3)<mng#vQEa;C`5B<s3Pqu!Jrhc;Luk88jubjWK>*wtH`DoV9+3WZ0_4{ACes2KBLKqt0Pa!mfCQyR51d5?CG=uqQ=fhlR3N4@vZ5hmi=FkcjqFo3J-~?z3akOzLhc<8`EJnK+Dxf`dgr#Vg!XoGdo#9-x=fXMA1-iisv@2ja*dPa1qg@Rvp*!?|b!gYY8t4h9!UbqAfc4ND`oKkKFM<mp7y81bXfK6}p&vNma<rGjMsR=!u0(q!Tn29N!&bCg;R^7<0JsM2HE<R52NkxX-45Fz2!r7Uv^T(YFbIahO=xd|9WWH~;a0S_!i_KjPKP_t-T}A3C>R5Gp}h-khp{jocA?z`cf$mj1oxr65AKD@a0Wbp_5rvbrouGXgLV%*2-9H(>_xj59)<##1xd6?*ax#gfe_jdq~L5Qf+x^E0gochfv3<uh41D-1P-7*fbSwu3V%oYcYIe0QFsyUi})@IF?a>-EBG!3mGC;+*YRB?EP=PszJ>3Wz%qCT?K}8x8Jq|2p?weEod>JneYEf6yH&6jK0^BuzFQ0D!>4FJ#dqh!2KWN)7x-=iTmpyC9>RB*z$W-N+JED_O|TihL;D@R+YDRaN3=iUyDe}v{DSrue0Mcm3%{fN9p7CG*Ta9%{s-S(4?CfOay|b12kB-wR@sR^4V0VVHfVyjiE^xR8{7%a&^A+=D0jj=&;o4>rI~UM{0&;6ZKbqO{sz0DE!wt9D`hu41Sg_BQE96@1dl)`w4Ia_l}8`}UC?$>Iw=W^_oMj!QGE9pJPAF}_E1h%_QNx9D%w+(Q<SISIp~A7kJ3wd7G8k9X!|OsDbK^p;6Uq8@|2h0HE^SKD|Y2ocoTeReTqwY1Kx)IX!|Q(<ske62BICP1eAB-pP-@Dl%Vo2_yC5W9ij|UK7@~9INIULP~{W&3`U|Isf<uQhc96?+R@4=<tz9a#-Sajj8VRU!!Qx;L}k44E&KpypglvGq<jxQ!!)$hlqt$j@EgoPJ3~2B`4#?zS!ib|XDNSxqJ+?fl$i=B4V7ZF#md>rF-l`)F50<Dk<v&xPKlt6D07si%JE7m+EQhn(p+h&MA1f-1<DCZYbAy@rj#pfly*ub+DfHDX|HrpmY`jtEK)iuCn?L&E>o5&ot3W2d1%j5&Q-c8k3$aH9A$-KQ@Sh1fDL~Dx+^`EMra$sG0;=#tsIB;IA{dDm0aa`w8z77kgN1lTB4=T$M#d4N^7*Op(QvKkJ1ipJ7^6a#jkWg+X32vUm2jBg!Uxp00R_N>58^1oCK;eSUDN($<P%BE5npi(4GP(!!RXZ>4mlzoC5jE>B?znPlH}?x-wSDLz@Su!B}O2Vn=I-JeZ(NR$ORZV28=dRK<(d3oe+dOjiPE1K@?}N`W#E?LY`Xfihds&}uLcW-Eot5VS);gF+>&3`aX0hCo;;QAVO23B#d8nXimSI~qp9e5Fhohjtu{hB9TLG7;@W7zYcLxH1Lp6qpEcWwCN5+B0DaELP4@&O&<@oC)VB%axgEXTn*q9HS0s0cOH;XZ*1*x+_oXw(iS>jAtxtnDBPY({^3(o|J#~wn*e}>7(7&>!6e;4{4tmecWlfzl__xdt&0nvwG|8%J};BtrLw8_trM9`dP{iCN@d@SkXt@^1&ZczI8YxzJ)y9U&bA0-5h**V0SIp^i50r@aP@E{%_=Hdxk%2iPe=`gSqQZ*53JTza_rn;>&|;TG{k{t#JOK%Yqk8>ZbS23g7adEy0|JyJ?TV@S!End2V~qe%#60jt-w&;^&e#1>attqwi~lTlP6$UH!-J>Q@u}mN>F{ojPmiAL_KV-7K-UbhY|c_utiFYCB8(VA%?FR{pR0zE(K$-Ey`0lRu~XW`SqyT&X%&{H(6%HqjDavS*F@(Dq-{&EXlAxMab4)v@e1eP1hVKd?$2)a)vC<KvYBt#Fs&tJH?Ox2oNLzta+bxP7@g;=^rf@5zr^;uiNURwEOy)%Uf+!w1II?|NOU_st5=A6BXMTd_@j>*6++_=$e!s9%rYs$P?LeSj4n(_*Fi?E72veXa2BS^o|Wcwqz8Mo`8dM!pSxtzE2sy?3IN$8J9yJbvv)^~E6tQg&8+9em;5%XNPlKlsEK!4tpOthX!U^?N=G7B9J6{ruCeQtrI=^WX^gMzu+(t(1Mcz6!2we6j8?<9+8}p`P$&q2_J>u=>-(e^a|%H(mSmrDv0EABv_TXWXNX8+lKn@#<y4?mM4TKR9ciX7rc&tj-yij5fSA**R9K8GVe~yS~3GnR9r0s(-`hGLG~4dz+KNUkg)j|9ekT=CfqQvPACP&m~t(o0l^B8+{IhCaBJpx2T^*N>fIEnU8GjviQtC_E_!RA4Y3$E8Eo`FP@_Pc}q|2&o7@(8sjkSt=&QG*`L)ruAY?<H{-rCe`Bl)8o!j>e|fXyU1R2IvKShDDi3r|?OD+)wKMvHDvM`3SHo23`Z1}ere2pc`Ws_)<$~Rb!(acLd}7nAj5r(jHO6rDikH+@mo`-w449je9Y+>(<G#jt%Ho_qzD%=ux+Zroxjnfv6w}(;CI#=heWz-SVNv;q>My6SQ2#NyKr<f4iho8tuY4u>{s~*uo4%88H^%VGsb#6(W_DH^?7dwYXQR(a1+kQG^XSAUU+zpAV--64!(_V+%aft<f|T(%Mt@`6o?QQm`eD1Pl6O2?kdhro<}Zuw#uZ-#Z=Ss*HEPFM$#yeVs>)Y0Q%_y@4^<X_qmRAe`D(u<*CrqH&C7_b(f@+PJHe->G}pAdCu=f)W1NltbDj4mdfv5E>#%>kYV<M2*64FrWkGWIyR)_C8{bRH;&1eMa__3-*vZ$cTb9ksh@sKn7{lEM-$)Gj<M`AqzfDfb_BF=SxUVsu#^cE1-}>G~sfQjvF*zz(B#pVzM;2$9k1=jWA6Yz&KC&1ZePppR`WVM<^f&r6fD@rDzFI*Gd^Lk6`oHgNp#Mux+R_ARBb)=v@wF1x;A=fxh_8!r>qgv0TP{QbXoy#`fIl7Z>bViv(AuCgG{$S@Q_!9QInWfELvOUbp$A?)p8$Q)_JvdN>bVU#=^7ex^?z~dM(f7w+4i77NBwS|2RcDFP|>R3hc0-XJP7R|yoT)#Jz*HyVR+rz3;Mt)w4-1IUM2U#E7Q~PXCz)FyI>O9NiYT+cs)D??G%^*KD-VOpvCKC7=YKnv(e6m8TviCLbQc23x?t~@Eo*rpa}BebeM;B9?Zon;PDVe8-@8W7A8Xl+6pMcE8sJr5^W`v<5h2epljc=U=d7*0$7H287#%C-Vm%ny8_OIv!NJPp<M;%K^RJ4E!wrPTEFLZKHBqP9V~ztT!i)_xBwQyVz?CTrLY0wFb$TVT>_UtenWfW@MZh;>r)vwJ)=kBgf;uMt}EV?^2=v8ON68QwUav?lyc;u5B9|i)BZ9JH-3KKD@EycW&D2lgMIhKkT3dK%DsCvOUzooU+etuKcqZ7w?|_9=Cr?z2R!l6zW3IBtY2eV;XVUz*>~URA8VKPeAW^-X}n<H{vSTlo_TS<B_49par<7~^O3%<6~5w}2lsA%=p(&vR`}H|zwb?b`;m6&(1(`zp?x#=-JSojcK@)?EwTFAj(ywLeys0ng}X0$EjVNA586HXAxqra{&H}G;|J}7#-l9pbsJs@J~I1z?SkJ`OT7P)H-oQS_np446<+(`yTOu~-|2m`!dL$Oub_YbciK7UFSW!?cm6ZjWXt#3yaTH&@rMiF4jw-92Yp{F{Mo1L)mD4HrhhLpzzYA-Wu4mU8RU1I1Fi7%lUJ+nm3^)Kq|C6y&ljyw_x$USzONO2aOrvKN9Bj~zFFa?8m&@4I{T0YgUTPV!t;(<t9E$gkhc5Ig1uJw-Pn3n9r?AsuN8jzu~q8G@7~hr`qT<f`DUeBtR2*vwwPpz|9IqFb=so`wXYv6u*6eNTC8q6?d|k&EO5ioarH~>ZM|<+_|I=D)fc}zs6BsWS4(_*n`P=hVh6P^zG`EMZ=1eS-PR<%uN8h^>vzGk9(_gcn~Zn7b~yNJt5>y#MU$lLx$F?i>#N#H{bow}z}U}&ovwXN_m}bR3qK7$a_BX^T^Y0gtAn~qncLkLZzE;yKl#hJ;kVZ(HXXYnwXmlx@w9JV>YDfi!7q0lNRFFUmYTXD9{k(nJ*v^?&r_dEzQ1wD-j=`3(~LgzTR*05p0qCUw>71j%-`r^A2Cn6^x<8JUb_xt9N)P8jiNFQe-eZJdy=(|sp2sQ;4xEHe2m+>fAwf`jN^jfPisr1+l_J9{>KTaj+^>xU$=NNdHwqXQvRH-+Wea~sj^rZ$9u-Fzb5aT)<~UxRe@&Q*XZwD`AqQr%MK;aEDUADM|K>Uf8_<Ow5=`rr~1!+QZ>fVxIHjrptda8CAB%UDJhGyF>ZOk{i=SZHcFnjwIF5O*NXqfR!=9|e0@mmG(MCv##Xl77-wT_-+3xuop)taTj<-Oemn9tb@JS^v@s{`l;*|g|M<Xe$v$s1(XPB>iZmC-cpClRp82oj*aq8^Yr9R8#@`s*Htv^`@WWZDE4$sO8uyjOztPVll7HSDO^t57C28Du;V+%l<<~b!ZU1bFH2%hYjs8oVAE@V#yiWBzeWo-Q#uys?jXuWM%Hn_a8>QOZ#@&NGPJc{oGPY71f6*U_-Obi!`1fr0u6p(8k?MmbA<gJ-jI+^47XL5Cev&+^+Y&W=LV+fWv(e|*{L0iZ3aIvv*Ql~Mzxh~c>XkW75{KdOq|x6PPvgD^TECn0%^sR8z9*D2?kkJ`af3clCsZs=!tXOu#(ib+H~JgndCN!Ft5@GUGd1?Nr_~;fZd5(Thf|jp?2yL4)&0k--H+d&{N|mAX53en3!{IA&-~`e`0l@}qkf*75nJQ-V}9M1eEq&TTG#istFrj_=ypYN@IPm3(<eQhH2TZp|5LbOa>S!gsl``CQpSB{@vr>4x!P#u-;;0tIX5GQ#^V_GHToOlS>O17^~J(eaOti3XPsm*m-!fDX!McA*61UPr_o0iL!*x|4n}{Ok8JD!?Vt_5_&!o&d>x~2Z=-K%jI;~3!FBlB0XO377PuW>cj4AuxQ({ljzpga>xQ-)oTPsqEC+24bcRN79P~ij15Spfa6FubmOd9j-(A)ZZ9nJ(Eul5o(b^#w+CqEqp!I+YP6P!yq3r}d=m=dwL#x36=mOngDB7W*f(=fAVQ7cJApJ97Bhk|5A9_Py7>9NojDkFHRNY4!3r=vuRJ2oJGI*f_^hett&ICUUgaWh$FipRY6hcd%wHgBX5T?&oKp~8P(GWo!fnqov#=`=%3!ntXzyv5qTMng$`$!963It#}+UXF7vtSmiK)V9YftmV!qnY}>Bl_&tdbI0d4a|l4a1q*z;Cz?|QP_xfBW!>&sDRCAH^Ze6gGI0f?H0HU7Q+l!hIScT1xsK#T#NQv*b3*uO4yEeJ6r>+VJ+N%_6E2f*1?5vGuoSBCtLuRz-?%6gPY)DxE$_8dneoqo8St#8|~e22V4nD;cB#3!#!|bS!?}!z1rTBugZAFyDij4t6n$d?Ol&mZ@b|oQ$FvyZ-OTte8H3-{o}PD`^z|g<zqo^SH=xyJrd;p%b5H>e(3{Krgn$k`>82Y|6gD7xhYc|*k8sJPi|MnoR@p@LqQpHUd)*DV#b^oGv>UQG3UjMIWK0+c`;+oiy3oX%$W0H#+(;3Hhy<sm;A+AZ1r0Gv&dDPto{9d-#7HoPs+@Pj)A|^eT@DxA36qeEuW;}I4RL_jN8dq)Ss&Ds+mvKaWsRED(R1A=#M5Dmu483sZUjWG)bH_L!4{(CuJdDDGT{ZS;$w)LcUTK@|CiXuat#+r7YwtWg%ZF3;9Y}$X809FZ#qLeS)(C(C0f_Lu>uJQt7jyji6E0ny0J&+t&K_M)<x1{vU8PaSE<jdf~by4_|g%nYeJ(5Wv?!T#snDIv9?xUixoc`gRT9=i&c{>+7Q4XnW(jgw{p5XmfF$Lf_)r7j0i$|1`sOkOQp)S3@muUF1gV#x+VSTnG8l`f)WxpOYVeb^xx0+Uw8L+T%}uToHA_)k;VF3F2z28?K2u<If=dbMhn5j?ka7DY*WkPs``)=W+TD89qmdm~`p3r}mmM>Dx<}K4QwGlXrDCXVP2tmoe!!w<}}Pf9}7G$$v+ulqplYizhv5%GCdB_nR}tf&FDn@#J=8%z5E+w}?3}X3TjpW6p~ib6(7t^J2!F7c=I(m@((Yj5#l6%y}_m&Wjmm&*Rzic=kO0-*+DW{@EK6^o*tHn>Qw8{D{vzur6l*ZC7_p%9#DlnEapk;TesODPr=ki`n0J%-YQUW}N-ra`W#k|LO6{#JVph>Yuf!o3BcmG3vec=8gB7^7DVcxK4imoGYr2Y0l}s$+&mHMoWxsC(U@|`x~?$PrcTZ_jC={$v>W2P<>1@=DvxzdD~<5abD`?tCD8Sc`;+oiy3oX>gIIcWXyS~iz!xS%y}_m&WjmyUg~1*n~1II&-{<Nr`p^;%(AxB_?!A@BA=S=_0}INnwjBazq)7Y^4UWyYj2IesgEY|soDPDGA_+RzBCK@(k$dlvyd<CFP<+<$0f;^W+7jig?woi@>Q>K(Pw<S<8^#b=&gV1m+mg)Lcgj{0z1J2e*Kfd#C{lnOiy*_U%n5}pQR8F02R96J7N_EBRA8J(+}B(?}!KM_YG`155x8pXb7jGJr#PuG0+(LpzQ;_^yfQyX!G<ZJI8|^tsVO6&v)Et-Qdul?|9MDzi({=?V&%~{@{al&=G=YgAjlYa1v-}>EE|@hORIK?GP9Q-Sqny-SB59oQ&hAe`|XR42L%Nbx|kn>8gKEvW&a@r=!mIf3Q0!;~h;~>YSJ`UCNKI{542Cb=GYIW&GUsXLX*?sKGuNmyXz^^XlP{knxE5C+U1{S-zBCiS!#l92-<2W%`~{;vS7wNqJ0aQ-b|vyyKU*65Otg-A^`8a{pyqeE75^$3ezte=sD;@s#oQyQU;LFEZ|Y!|WvISH`WU6eYP%WX%4zUfM&--0sVFj*>F>-}C)EDRUg0C#;n+$MfDMo21NndFjwrDRX{Xlx&wW*U5#0cSxD*jr?WIbxZBanCqYVFJqoZ6bBjee582FnCCU+MaHZTlwTQ>&Ma%&w_0;VO#Z~IIU=TZiCJ?*O#LTj%@HxhftWQ%#1v0r)*KO2UWi$9L`?Z5X3Y^X)d?|cj)<w=*k8s}x7@Cbss6eDGNyUNagZ_1M~<hAX<l<)WK8<N`IRy04A+T_*`GB>#M~}xj)=MctT`g)II!l3nB&QsBVx`AYmSIHzpObT<~m``5i!>rYmSJyZdr3g%=OQjBVwLMtT`g)`N*0hVxHHmIU;6#V9gQn%`f~E<T{aYp9c=>+@kg4K^Z4+`lrsb)~%Ov`|*$Ke0hF1DIa)ko6b*<I(MLq7sk)fd0ozVdu4n{;fn)_zwdPAJ{e!JYSCWeTMFKlGS|t*$A6IWzc;Q)u)mCVbWSC>T^W1-{2{^pmvPbYZIT=Z8DDsyXOiP7<5_V}lJg?tE6!DuoL?DFyl`-}&d8YkfBCVil)2rBiGfn){&(&>P0AdH;sNDS=6DYOeU+3sFS{mQC}qy?v#(zwWv-Ln1skQz^+x_O=DMYJWz6+Y{g*M%BZ`BJc|KA+Wz6%M@*-o_2g<LENoRPSEMxN5*MU`<BVuZom^DYl)PG{u91&9-h*@()Oz|XU%@Hx>g_t!*#FSrR)*KP@I+-;`#8hwWFJr1(Zdb-s|J;8W(>&rh$e89M$5X~MuQ@L=CVk-i%9wP9>qN%v&zd7*ZkIJj#N2<@91(LISaU?o@np>rG3SLfN5q_8)*KOYov`MJnCp!-N5ovWtT`g)`e)4%G0!8`91-(;WX%yV&ui8k5wkw9=7>1^{iWIOFU|h_k?i*;XaD|4_WRqje}5$V_am}@e<WK!+4{-;{gLeXEBp6Hvg_yU-yg|dzyII9ey8W`H<e#k{mfm&^t_CipSg>ep1TqAGj|cw^E+aG<}PA-4oJ+;+(k^!6N&kmyNKzzBr!j87co8GB<5%CB2NFE^y{jhxr>;dx3a&C>A5YpD`R^8%l(%zJxAs^$e5l-b3A2C&$T%(GN$L_oL?E!b9Sy18M8k>a~CnU%g@|J%>CzQ?jq(m@H2N2b3FN(yNEe2{LEd%oL_$CE@G||e&#M>t~Y+>E@G}*e&#M>u77^!E@GZX{LEd%JRkX)yNG#S^D}o5vp(=McM+4$?CE-QwdRPJ{E1m}L`>}xv*w7H`cKT7BVvjJF>8*9DW1fvIU=UK5VPipnDR@^nj>PW6JpjJ5mUXfzl^DFxm_7k{d50iO!J82AY+=398Ve3yym>fnDl}3D`V0bt`ixvKWmPNxn0&A5p(}pb41K>V9gOR$CEWj#GDt_91(MVS#w0pb;6n>Vy-vV91(NfvgU}G>z_48#5|8!b41MZku^ueJg-@EM9liYnj>O*&dzlrV|reu$D!((yNKzz8!<m~7co7*Bj#uBBBtkn#Qe-%#PmFon4h_en4U`#^D}o5)ALPYe&#M>t`mOdE@FD#%KkE@=eFFgjOqC=_g}{J9GT-FV|pIV@su$=*XF#)n4XVweq~J0*||<+%>Mk$UBuijKXVr`_n)7+i<slU&)h}K@#JUjBIdmCGj|ble)*ZZh`CPqnY)O&-uRijh`Db0nY)O&{`r}^h<P6IGj|d5eB@{DBIbF`&)h}K`oPcJMNB%w>tq>|zrGHv(i{;}yTq(HBBuTmv*w7H;y}!rBVvjtF>8*9DKEsVIU=U~60_!rnAgdyIU=TdV}BV_-EzA!ruygp%b4a7$3ez4A32^frg_bIkum85=U2w0Gh8P!W`EWk5p%n&IU?r%v*w7H<G`9DVvZ+kj)*xgtT`g){IceVnCpZ!N5oujtT`g)x@FA~G1ot9j)-|4vF3=F=Ob&5h<RSK=7^Z}fi*|O+53mt`-j=j|74$EWIz9teSVt#{7?4t8`;nQWa}qeKiSX!WY1sO&;MlC&)LuaWUt@<Z(qN+>~p^E_vVfFsxt1jd!$+yv%kybO3Il1&6xZ*K3*B*V~Uvk>tgmd9<w&HzZqx02h#j|ARFy|CfN3#^VPx=wyI|Q^nXfK*X%8(T>isobxgr!rrd9Jp8B)@LQ~%Ia%*+-hI381{Iy?#za9*k@+tWTgAdOcYRc;dJQ*x3$T8&ui;|=}rcC|=^Y;eLnA+_Wj+rv`zpwr9Kr^N|jF~ZWfEiOf*Kgds&x|QA1s^m`m@(yd+b>R2raEc8W{@cl|Hsy9e;F?f-Co_Uj9Xu`r@H?#p7q_6)p3w<^G{z=Ii4~;yXird^CIJs&EHcwzcOB&{HMxwB4hIBdXq7=%XKSb>Oa@Nj42L0k7P{o<oPIL$_vkH8B=~)A4L4*_~t6>j2W}em@(^&8MDrqG3$&Ov(A_?>x>z*&X_Ulj2W}em@(^&8MDrqG3$&Ov(A_?>x>z*&X_Ulj2W}em@(^&8MDrqG3$&Ov(A_?>x>z*&X_Ulj2W}em@(^&8MDrqG3$&Ov(A_?>x>y2bw<RZ>#a0ruA^$Ur`O==>#9tjn(gVeeEPa7)2C*8`kEkpU6tumvps$NkiM?U^r_jNzJ5qwS7rLtY)@Z5q_3+oeQLH>UsnZd`_ybVUV90TlQi?G>Q6G$UpTH*roS*gsZ4)ioKu<p!hEGN{e^i?W%?iClX1T%&2k@#x9B)E+tb(8qW;uuPhX#l##OUDeVs3gPtEr9{Q^;(YqqEFJBadCv)y=K=ZN~zj=c9HJdT>_FYJ$+=`S3Ymgz5ykCy2#jI);MFU*&g=`YN?mgz6|G3bwGL4Pz0`lDIUAI*aPXcqKGv!Fkk1^v-1=#OSWe>4mFqgl`&&4T`D7W7B6pg)=g{n0Gwk7hxCGz<EpS<oNNg8pb0^hdLxKbi&o(JbhXW<h^63;Ls3&>zi${%98TN3)<mng#u-_GtjKp#WdgVXFSOU?<>fES!$7d>DqW!Jy)60QmL4zUIVNKgh)w{T;WS`ZuH7^zTsbq<`Cb+v>lc+eH6P_6GPW(2qPpKjtv~Xny@Tx%v@o`o3-Ty_)F$Q*}>O_vxwswuQd^bbU)Fq!biF7+)nYA75p#5MOavjIVQGIlflH8hovX3-NU^Y{b{)a3#LB!ZrBX4maTICb$(}cfj5Fx)<)p*MsmdzV_kKQ+RAT@<RQX%k`sOs2}G_{RlVc``)eZ^|0<gU-w+2`&^^{_I`c)Vtvc4ND3SSMQDp41P!4P%t1Q`ilH$a2NARpn5%zpd@0&em<P?FB}CCiVF8=~ts#as2IbHO+Ce4SN~nPL&;gd9T>^`sBXovy(Vh!S;Uwq=E6}chWzZFJU^Uv+a2}itJzyQ$b+8Iffm7iEv=_iy=mmY?BDD1Pc29%8a4FhLVT1nnf-ggR8C;_OwZF}1H^U}ygBP}--2zvD4+3yC+N<Fz=nn(oTC~@~HVA?S*Q322u7g1^1a_j`2|HjY42PT1-V8Uw2p9#oqrDw&fsrr<?m~MP+y<jzJnTZd3+{w*FbVEMdmr4R|4rcs&^`cvgDEf#_MqJZyWvcj0ejKzg@^RNFPuc1ghyZ|*7w=^Ul~s5_c;qTzM}E{Oc}p4^aYLYQOI~*&a)cd-;i;aDNkv9pG3w@|9o8I`z<o=I`~nI@7u_Dls~EQ{T~@`{Ar)Y_mN~g?4o@d-;a_p`SX1(8B@D_e@w>If4<KqV~PXcuahywlkfY<nDWB+4`odG<@=B_raIyKnKJ(D?Ki6ZW$gO>?do=Ae9g1(Rrg=UyKEm+$3e#1-u<XLo-&Sp@=0}GWZb*gXVv+YapmUEs_R6?<j?gcV``V{R>stSu74R*9C#kdnBvLvQO1-Pp4T#_{IWiXnC>~S&X_Ulj2W}em@(^&8MDrqG3$&Ov(A_?>x>z*&X_Ulj2W}em@(^&8MDrqG3$&Ov(A_?>x>z*&X_Ulj2W}em@(^&8MDrqG3$&Ov(A_?>x>z*&X_Ulj2W}em@(^&8MDrqG3$&Ov(A{YQD;P)z0aAw&zZf?nZ3`Mz0aAw&zZf?nZ3{X|J!}e{{lAU-H!', 'underwater-fixed-opposed-concave-jaws-and-cross-arm-grab-01': 'c-rk;3!GeKbw3l55P~G+K}dom!}5@X-DK{)^9-4}gv~=R5JDh`B*e+?Y%*puvzeVu2x%%lXnnL`h0=mlP_&?88bkz@osR;dsa6YW@kLwvu(i_Cr+wMl|M$(@-7~ZI+_~eTzxexQ_jk|!=bQ7r&iTIcKi}+~yKC^8^;3xGFFr){=@`-FTQ*&Js4G7_T&Q-fI@GnRP%2dN)pDh4Ro5GKSIVXGaC8@{L@ymIl==&m=w&N6Mfb;7I4k0*uI{e=h01WTT!ON_BGz@dyKA@)4Ro!FHPCR^sv8b<mGXO0*0sgF*WFbr_nSAY`1Zrw$6p@mD%@19<cIYz`pSEU%B4c7x}#Da)OD}hjla>ID2Y~g7yI@^-;zHN9T+T^E75$ZKUyBCVr)C}eS5m22a46*(R^QZBtIA}4;4z$zLCoQLVvWcT<Xj3FIEql8u{ozu~e)U&`7?Dn#0iEi8u5l_7;YBn>jQFZaVKZt@N5k3YX^(tk<3EIUjH1wnB{C3ODZI@?fz)S}B*S7)RkC3aW*@<2~8UJ*_)fxEiWk>N<hVZz^E|BZGs{!E$LAW^@zU?=R+el}ngTzOvWrvsj82tHaUqfl|X%!^QqWv~PEz0E6{a%EQA&)UWO?z+yvX^P(?bsT84!s`=<}VJMH~T!;=0=CSt1M(#9^d?QBD+h`3YT2t8@+Yvk7=MZl{2kUsBL!#XrtmEGg$@X&y<%a`i%hjVqzEm0+%vYi#Lqq6Z?>rM75S>SgC9PB`kL=oQ!UVeMj+V-p<q+&ptVR)928#n#GycJRk?q%1^GG+L_O-f$jZnwt?R1di_KQ}Eb>o!}<SYGk8yXW27Kgf{g;L*O-Ja#r;6d}Qt_oKSm>1Q`NFiF-JA?>_=r}&ybn|ex?9LAr`eD*7sNAc&4Y^5wkz>xZAG3A5joFH|8?<%&8QQYi4?2{kL9f^=Bju4{^p!6S>y)O@2qPvcM2E2by&acFoEa#ORJ_p8qXUcy2*ZtCSj|_9CiLtq>;`QklNuj$3t?U}*57*ForxM(6-(_#-HU?3LbYj-y9;@k_Mo=o&N3o}35Z_!8p;<dm|fWzbS$J?jPX`=Tr2KHtkDs2uvprY-^D_k)xwh|TJ(DTnQ`{*E)Mor3P=HOh;>`tcDK_V?@n|lyHnli?o2n<7CeQCTMkma@kyD4b4RfsEsyBD@&E=<=`j=PG2s_~>xoaH2Yw&!L5kC3W~wdTv#XNd*%PynOb#GNt?uYARtkO9dM4U)J&K358~S$aFAgJ}+M$<L*DAe~y1UAi;;v$8M}NLLvKQKBebpE4ZoG9fTGPHOV^qUYB&^j63{^c)j`odNT_;``Qx6PXE$=ni*RW3U3V9e_o4DRwgNZ5!qk6Pa%)L<2%b~lgVp8cHdgWD+@L?2(wsqzE^F!6*{=&AdRndX`;BcWkx~=Z};i3-azUAf04wF7Nzj?54urR!%zfdX{hnw3glrVQww5_Z6`reJ}wruOt<->VBIn#_~r*#PyJX~x_;_UT~z38r9fBj`|T(`DfeSfiVV8>woAST6ny}@+5{jgq7ja7sV*PtHbVr<t9uuYdf2JF=<pokjgD9~RX*@;b!z1;6PuF=F=tn5n%M+zG%g@dLoGy<Cr?W|l;fa?Z}eOK$9iVbNN8ZzWUZ+Wm>Sr1F=W6ce*6}FWzKk0NVm5HUS?$`<^9y32qB9*jL>69)?ni4DS#1fVjPbIo7J<LWYUUSfEv}UK{sd(H*I#BTjFs_tr?(wkRI`SN^!y4D~L@-!W>etlV*#zUMdT$v!Wm!ol6W7y8)n^z_CDTsIN}|ZFm&EK$I%Yez9T#TUuuUwHNyg&Ic*1vviDa`G+Dvh6zOu(e62!fFnCftjRxED%OQviK9VYY~twenc$++#H*wICeX<Mmu+Hx|EG)JdyvP{ButR&{(@5OYzv6Pjt6Nyy3%^a`F57w9a7$*&P>PV-#Lrf?Us}B^OaO^}fjiPv_u9ZnR$y6NU7v^X;hHqIJJC?CCzH>~)n;NqZo6QM2Xg<sbory8WN^x&dN3(jJe6?CB?gZ(ZiC(p7%VpPGw&_Z9#J+OV)mN<92&zGlD3<z*eOkvJ4+l^>yj`0)#F;j9zs`8Sao%sDO~3qv8@jXPcxNfzS(<ldP3+A7P#U`146|*F_p39f@s90q9d}?{o#l-6>`by}tCJ~Pan^I9spsU+&~qnqPO+ZT9rZln6c)Zy=3=|a#kSREZTX+2LicPl7u!uP28Xboop3#OU}!tRdQMKV=Z+Sa&0K6ZxmX9%j(hGTTCp(cSRM5&oiM`p%{=WidD@A$Sz|4Sh45W67duHYV(P5~X3F>Bt>JQ|-saAcfq_D0E7DOzE@MZhYYq-!TnS5OXMM=+k#naE$=rl$J+T$BM&gi8CerClBAx-OChZ9cQ)`x}nXy=^H<4`3DZ6`oD^$%;y0)(Cb<6>Z57}xz<e=)dUv+1!y5)@5-_pBg<C?1{wBUrbna_MXGMKN)e+G-iCugz5q%D>V9zZ=R-PD+IJ!8$JVpb-VOr?;gt#In;T-;8jU<7T(iE4bA`8HzJ6Tn2uwqx-`rn^UICCC)1_7e%Jo({I8lWb?mO!%c|+esv*2`h!<J`+pEQZRw7Uni1Q#<G#PCT+d=GLEr;lSamCB{T8n?P}>ZoJ2C7cH&8sSjW?LTvv&wEjwmTg^fk(d8gg>jZJPfTGphOqh-I!W`wD5$}pz}8^<dL=U}HpJDOb`uOB>;X><^aw=<+ONkhgviDS(Z@Lx(3$3JF)iDvX&OMX@ioI_%gHb_o>F{NHrGxqpysLt%z<G-x~4UwLtA=^YIJDnakgB7ob-9*|((2b|{o@zv5?~?_+o<MJnqd3m)m_(By{MxV+EvNn-|3(7SgII`(1UAqnK7q2^Eh)QAd`iT5R+g+AB9*ifX)A7<BqLT&JRHZyBFd!A=B(Q$9&<8SfQhE?lup)LNJ1->F}AlFDF#-X<v7Vy!bE!h$w)fWjxBAc{X7Ee$Ae9oX>ZBIt8K|1e=~Gw%N}2c1ll4wNn57ETEce@ovbK-OTIcQDm_UnWG1_!oY<>t$H4Uz+LE2GC&!wcC7m`gDwAY6eLUIta6FCSB{Mo!$I^+EWyNAP#+}A^^(VA;Lf%&s+lZ}z8B-RH2JzHbM(@`~;53}}(+I5JCPZ23Slbnq2!A@VTfMAV&oWbX94D1d)-&>!kLjBd2%i?LI{Bt7C!I;9V)f-Tv5i1GBs)AAp}q0?{BsHOnZ(Y6)xyR?X;)R>;gF2i3pNc5m>cl4Me~(i8e%d@dweYI>zabFwe8m0R!RpTUft=Wb1RdvCoy(Aok&h%@J`B(g&(}hbDFAW(w&&DwK}3*2XoiDO|@|@n1tbVJ~#=(V|z@-@JVM<gU6{LK8e92H%?Dx!#Ih_m@Z>mlQA6#B0U+~Suq?+Coy~r=cx{?=fw36ZEC=db+Yb#8b~DU4n|;EiI%Nnr6+9MAQR$b+7fkQmeYX?ed?z=2^?0YW&E~2GEZjwR!941Vtu=#$mLT%W5*^_-_a-8N!TwwVGDL<zj(ZpEikcuBGw6QO<cfsA{C2Is)1xj#A%{+Gw;S?=}9oBopw6$pilke#PN^iPmSEEsew#9et7%gX!P`bM3-K6CEauP-J`cZ{qNaB^N-{t{QaBntR2~q55zyd@Oy2s<IGbpZ%*fe@W8+YYW|Tgw#E0{y~qv1$a&S(Pb_JRx8449E(k+cw;6~B27XW@`~=};+iq`*Z-07Z6tA;EnE9n9VdfVRGrx$K`9;LcFM+t>7ZEeR1mcEYM9lmmV&)eSGrx$K`9;Ju_H&E-_4tTeU3^DQzj{yioweIe9dW7Y=N6a$4Wsjy=fBRq{|9R(=<xD=3--BRwjR#4>NJ<%($Yq~?Bxq;xd)H#bvw{eemejANBh)O)<d-*otxggO#R=#x#qoQ{Rwk7I$U4UIW6~r-1q)vc!CZu=YC;2DulmO2!E*%{!$_Qr9${ih47aO;V%`!Un+#ZR0w~m5dKn<zs|vR61|SjqjmHenoV;lNe;z;=h7LJ!K)aZf>#>Hs0a8AT1cz$s)wfImBu}^9C#s}MJ`?~M|;x^UXFIp!7GhlhxX5+C3wA#F2(C9bO9}cTt?GqDqTnyL0&{B(+ujS6_6`vCY?$v$%3@#G@3;=B_I<thfb$Br65x@kLFXFE{43A&ZGsjigJ)ST1<;5OKTw4(Ao4_x`cWmdub^}X)UdXTu)teE^VOmA<w4>A?9QmU-)AD%`x8b#fX7zv5v=#2YoSOvdj2X#Egr5F*w3y{4Qda8~9>ymdo-DUkvWcvAo3>gG1Y5aB-I9QNEb@r6ytK7ZEeRh?x0B#LO>&m~pW$W_}68EI07Q%r7Elei1SAi-?(DMBKt1H5QAM4|lY3P|c5nT4JN?$7Q@6G1m3t#O88;j^^cv|F!Y>-^Am!c03LaQjCLqb--ncahdYVJz6+X`Q<Pz+?w;tg?PE(3l+j&DulmO2!E*%{!$_Qr9${ih47aO;V%`!Un+#ZR0w}5$zPnu&oK<V+;HwGhSeRz-LuCy-9h<mgPo9^KHaeQrH0j~kMa0&Fz5N;@JL5I9*2yBzvqC>Q;@F)k6!?J0rCmNq|ui*|E{ZJQvl9}z@GkS0M3TMqw|kEIM$|svmvmjKN^6u?XVO-rC8**HiP!Hv`0d;<NEg*s1r0EH^g`*v=hPFoe4P;>-aRR(FKqTus-$fnhiM{`)Rt_N7Hegf)zIlt9A;m8Q1}*V)ahLHHY?Pm#cl*neL6BJC>9172mx;ef7y{?&FU=C*o}WJT-0K6!+NvnuwPjJXdwEj<}BVsE9rN55DrCh`oM~9=%V*-uP!ce6NUq`@SAEuQto*OZX#;V(NRR%r*T=__Gm9J(ini#xG${U)w>#UccI&68___Y|QCBtNkM3?bp63ch8)=jJ|~L$@b?yv*%9JuY~{MrCqtpp1;G4U&5Zgwu6MdeziR%?2TXhMZ(#&ZZ7-&dyKw>X<H(9PWoQcuY@1|yp_A{g?r8TCG6>IJ4o2;*Q|d553F9Ad*#oz)Q+t`-~!ixa~j|M&_?z3V~foG<~mE?`t977$4^(UpPFdW;pNtC^WE~1b!zF`-kIY%yqw{h(2kOH*mxAzmvq>?T6M<C(M}ERxUKE*a*Rh|JZ|fFSb0v;VePnFUl@<e^(9}R+(o(DS~tL7WBLL98q*2zmtQ+d(h2aFuZ}P;vAo51d~A~M_#7qQ`L)yPJ74>A{VB+&qWC=<IoM(_+I;-Z0oTm}$IUQYHwC{@^X`08J_D~8<L?w?hB_x)h752ee)Z=zI?v1CcQx`y7kT44{4O)^CQP}D*DLXNT_cMnlgUmsS?p9?7lM^fK~8!yu8Y9Ury-Y|iE9PeSbrMy8eFl)r&qI0emf8Byb5v^^2!CsW3!N1WS5JOKi2cf95ULa$Rf|ebqO-sE@Y8QaP=a$jUbmi2iN*B9xu;*M@_;WKQ1`)*F@~`?9{EdiP+<7oSQ}L>92h0BO><tJ^Qtv6tOq{FGP=u*yBg7FJX^ob-xn!_*#!&!k)gigM__)wLK;5@tXFFggt)L`V#hdR`)AmkFWLkCG6>IJ4o2;SKCv<-uSg&B<%5{)|aryv$|gidwi|OFJVt#+d;x!zh?al_ymui;PDeY{`2E;#B;a7Q#lEP7u*I<i5UFiHh4<J;3>DkQzG{C5obi~^^15VVsHG2dm;uexDB2XG5E!8@RW$bQ*MK&MC|EnJ4o2;SKCv<i08EiPl*`3P;2m%h`}$l22Y6?JXLG(l!!fjZ3hW^{c3wk*c-q0i-f@owFXa#82nOe@RW$bQ?&+9iP+QEc95{wuUY>BZo~~9A9yUS1(i4UDUU@wRx1`acueClU$M9`L5H>Da(!VuF4t%CawUDP(}=4si}RdMT^8rv)-mvMhHFAQO48xJ;QEqIi;q-GEcNq|YKh5yK2j~Q-OopU?X>#HZ#+#tYSGCt{;e^N_SI?emulftKYytfUiR~sUpq?D3GmmLPNd}=IuF14GuYSQJUAV{CqX09IET(N<<s$cG5$u(e+634q58iJ7vt==2ES{ev0>~Ss>|2l^-BERfK%*LoI$7HIv;1<lW_)}X3n8AaQ?0TUqhcmXEn~DJvfoh!5Q>4a}GTnC*u132~OibE_2O)T^5-CtSrE_3MWwgpOr<pvN(}0ZTw%Oehys^xgMuv{Xd=aAoc%rJYKu;bH{2D_W1Gf$DR|h$Fs-w*F@~`wc|W0Vo(2ruRJJXuiv9b?-Q{%{uvM7D`JlywZ4Qsp4I(I*yC$GehGW}+71%-`qlQ7u*YlKFB10nQR_?C<5}IWggw62<Cn0fuk9dVuU~CX347z$evz=pk6K^C9?$B2CG7FF9>0V=eQgH`d;OaAFW?hAeuBqO@c7S<$6wz3M0VzjkGjjY&CW`A(acX}uX*7!fjDvhec5~N{%j!rm22Og-T9Nx2jZ7Er?a!39}UDKFVt2){2#SItmn3Dn+n9xf0EVp#prjGjlmaV{G)6xz8H2GWj67}u;(bVtuKaOMwyR%vDSa;yGH}D?)T9ABY{|t|5J~AA`ojkocz+q0<pGd@iPwvV*Stlmp2Dv?O#^c7wdJx#^8(fdSi3(#d_T`oA_eA{+Vrk@%L|@pY!}8;Yaq&&VA`4PXyw=yD0a>lF>kX%l|x|efq~w1>*1Dd}sE>A3hU^pMHE%_LgVA5Qt5D8F(%bLw}Uj^~LCSl#Rg`WBj9RF1{Fcs4<)PV%W3BZ0n2Rmm2etFV^}SPx*sDtoz+|`^N*Z9{<&k|9&9WcE~;ZKp@ukyz_@23dDLJ9oZ0!wSQS%U#!;&8-p*_>y6FD7wdJ)Y~qXc`e(NF#f+y$CCqqA#Ehpz%y>$~jHg7*cuK^Kr$o$nO2mw(M9g?f#Ehpz%y>$~jHg7*cuK^Kr$o$nO2mw(M9g?f#Ehpz%y>$~jHg7*cuK^Kr$o$nO2mw(M9g?f#Ehpz%y>$~jHg7*cuK^Kr$o$nO2mw(M9g?f#Ehpz%y>$~jHg7*cuK^Kr$o$nO2mw(M9g?f#Ehpz%y>$~jHg7*cuK^Kr$o$nO2qsg+P8h}uqr<=&D=NMz!Sa`vEm(r>L;%}Qw!2ry66q+?_NC1oX5F7*U|55J#&_1`dmlX)AjW$uFrLJ|9Twy71wXk$$2_lU(!K4Ilp#zImYAqjfa=xuj@B2UXJ!$Kl|`<jLY@2bE7;Lq|<1J>*R#-xNJN*VO}nqmn+!EW%h9eJG;!zfjSL;xq{za=66?EKQ3E8uCNYWwhmokJ-ci@=Y)O1_fGDFzkcccbs`@A^29?G!e1(czf=f+sSy5BA^fF6_)CTGmkQx86~bRCguhe>f2olEY8MYxh<K<%#6uM#9;y)WP=$zxDnvX~A>yG55f4>}c&I|eLlq((p77T%pTADT!{a<2zMkGdCqbSBd<T7(z6JR$dLK=r-=_CNzMrPhx9KIi0`dyF4BA)HbVz-N%U$$msBssrJ7@;|F5L-vCrzdA(O=M2kXO-0Xm6%dAoX1_chmP#<8EAc(W&$S`W?vMp_A#)>91%D<QCcl?Q7^YkorEFd+D!H<6c~M(=7TR-2-_K&7{AiAJA6Ft#mcCucO(J`re!S=x<TuK3w<G9QqLb9^~)QY4kVrL%JUFdb$?cZ=$)7b5Y~N^!KRoVO;moeEJC84|zYGPJc%~q8lJ@pf^H$JDmY}25Nki{sA>UitEF)fPSAIfP8@F(aZFYbR*=Av<=#CriG9TQR5-{C)9Wd*GFj)eT*K2e2~thSLmN951FSO(C(wNAkRXLPtd=j#wTz+M6acX>En<er^WOy^l#J;*-ty6JwQt!m!QTG`Y~!8!SxARN`F9~g#09(P5(~+LAxM#Q32XTItTI`)Odvc3pF0Wb%eU;Q*;#aC`IW%>A&eMkZ+;g&>p1oAocw{pQfLn#;0*TLKo0y=uyZ=>0J6B`d``$xtI1pyG*Zx)ZdGFoPLTLkK_6@Eu+uUV~~&0`SgDjiR^>iM<r-iXgQ?*7Wn6AO5~@IKSiBxdXk=ie1a|{icF1EA*(b5?GfsM)ZhCarD>5Vkx|t89IYfppNITBT|_5EPL3RaJV3+HzKLRx`g`S1(TvEn$Wy2_N;W-BHOLyRpy`pBk((iJrv1=9L=L3>Ci*jUYGg*_8Ps};67&W7L&!fQi%yB07C8)gm<~ewS1AdpzsvI+&5E2Fc@DLnp%i_Qo`rl?f9of5dgK<!Tj*Dy{Wi)#>ievY(VWPv$T8G<j#kkh(U%~<L}{8GnHzaK<lE`3(0(VahScAB{|e2I%!zyjwT@Ai{+PZD`DMD8=0(nk+zNRsy#w06PA;VWHvHG<%*g!6*HG&#bP4?leHHSn`Wx$!g^_nbzKebh+V7!DA@w)rU!cX2Gb1mc*4L<)zE00WKCi!p6geyMUdZ>-yP^G?v<^~#tNxpGc4Tqno2c~yt*1YwZ$N&7*3xSuOCq;H-bTLx?bjoc{3fn-h$7!YjrZaDCPnDC=tamEX#*{de1|TFyqs>QZMR=)zAK`?gDK&cH$PF+e}nM8>`Wd1+#r1MpRZJJ>OZS3*3U%=!q8RsJ{t|hGhh6x+NEzUtPaBZnPctn6H9K@pXX<TuxBfM|FDETTLodyRzcXaRXeP06@)!o1!2!tLD;iZ5cX^pgngdPV)CDJxAwUA_pP3A#^3YT=eqMgw$^3O44I(wod*}VPyW}Hrkv|bI?}TRw*7cWE&Q8@1D~;W=ALEhz8}?}PtvUK|I7rgFX@zSyFa&e!Nlj=@N&UEDufMH2pg&pHdG;Os6yCKg|MLtVM7(dhDx&GLi0^i&F&7ceqM@ZZjJR5P&6xRte>8u8CPTd92L!`8tZSGYNo8;-@CB!e3c0Dh^V<6Sw9P9DHwbzt{KR@y1>pS<I>MU(f1^uifa}!rVGKur{U7iG`k2adpfT9$aGeK4d>xnfGkEoFXc>Ji;$rt%ze;jBUfZGrzT+*b41Kyj)+;z3B-+<BVrbFM9gB2h*``LF^f4OX51%Y#(g4Y+$UnjeSx^aeIjPuCt}8ZB4*qtV#a+UJ`vAP#Pj1Jo?}gBS<dE*^>hDN?&piKN7`b&Us*2di?L^2meY!u<-@*Me+Po)*uEICD93VjUyPWRV>!Ps_H5P2*?h5Qt03&zDhPYF3c{YP+F_Ot`(n>lLD;iZ5cX^pgj@D|jjdJX7Y|$3e9bRzwCo+%FaGdy>_OKrjy0FJf6gJ|gBp(yO|e(8*rNR6GcRvEx7HP&SL_DZM}@GV3SmPP!iFk@4OIvmst`6*A#A8Z*icC}{6*xqU65VoS%3N&x--V|+Y2EtG|&25hOBlLF8!=O{XD=qxb(CB^z#7c2j;gd=F}w2VvdMe%n>n*IU;5;ClIrI*cY>yBVrbFM9gB2h#B{Zm~o$o8TW~pai548_XT2>5Bp-qeIjPuCt}8ZB0dq%PsH=%A)deWEvvJaoN+7S!?$x1erfKC?BF-v9*F;G)wJyHAKem&7bM=d`s&Nx8i@6nzSZ}uff)Kvvbw$){f@FR_+pHIl+DE#!w#d&Ccaqf&)@p%fmru@ru*(dtjGW2t?voM+L?F$XE4_GWOaS9_6r+>FV_BLbMeJ&ozx`E)`^JOIuS8jCn9F+M8s^Jh?uPt5wmq7Vzy31%+`sB**Xz1TPGrB>qNwCorsvN6A`m@B4QrrADVy29r@x0v)3DV0yq8eJJ-0cUo}ew>EL~>XLPte*U|l;zA5MWl8)}j!!0^B){gRPhnMTWe&gZgx;?*nHOg~AI*oQ*rjrxK<FfI%!n|BIFITXS%j^@V)3CEE_{(Mfas|J;%<mKKR|&CxREYJXLaZMZV*RKP>qmuHKPtrfQ6bik3bB4vi1njFtREF({iqP@M}=5FD#ZFx^7_%|(dFi}dY(DUE;09VEHrnF%x!rljQ&|}G?y5ixs4~oka?oYLUY<B+KyALgWu$YXOrr?b>3j^so8Aqe7VltpRygg-qT9g;eGw?b*4OHN;U&c!Pz(gnZUVrD$c}d$TUv3C*w?fG33RRGS4r~LS|_dPRFOyC6Jd;4yWUJ)C<{5Yj8SVK<gpb(^{O47t`gCm(vEElFz0qAoV>$`ZRtOq`v=0|F>xiq`tSO3uo}Hkovxz^KlY?Bjg+DT5}q|0rCdA-kip7gw*%ati+k#GH3D~^x^|UIM>}_&SL>M7Xo|wwE&z8fon@|{lHk80?viNo_;L==i1>D&(9Bje*XUhCyatD'}
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
SHORE_TOP=.875
placements=[('d','harbor-dock-module-01',(0,-1.1,GROUND)),('c','underwater-fixed-double-open-end-cap-and-spine-sampling-cylinder-01',(-1.25,1.05,SHORE_TOP)),('g','underwater-fixed-opposed-concave-jaws-and-cross-arm-grab-01',(.80,1.05,SHORE_TOP))]
def rigid_point(instance,p):return tuple(p)
def stored_point(p):return tuple(struct.unpack('<f',struct.pack('<f',float(x)))[0]for x in p)
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[stored_point(add(p,t))for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,rotation_z_degrees=0,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values()),coordinate_storage='Exact IEEE754 float32 after translation, not hidden deformation; native versus final GLB bound unchanged2e-7'))
base_mat=len(PALETTE);PALETTE.append(('SceneOnly_OpaqueWaterDatum',(.075,.20,.24,1),.55,0))
v=[(x,y,z)for z in[0,GROUND]for y in[-2.4,2.4]for x in[-2.1,2.1]];f=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];emit('SceneOnly_ContinuousFloor',v,f,base_mat,'Single scene-only finite equipment bay floor, no extra counted model');FEET=['SceneOnly_ContinuousFloor']
shore_mat=len(PALETTE);PALETTE.append(('SceneOnly_DryShoreTop',(.36,.32,.23,1),.98,0))
v=[(x,y,z)for z in[GROUND,SHORE_TOP]for y in[-.099,2.4]for x in[-2.1,2.1]];emit('SceneOnly_RaisedShore',v,f,shore_mat,'One finite scene-only dry bank, no reusable terrain model; small shore/deck joint remains explicit')

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
  assert abs(bb[i][2][0]-(GROUND if i=='d'else SHORE_TOP))<=tol
  assert -2.1<bb[i][0][0]<bb[i][0][1]<2.1 and -2.4<bb[i][1][0]<bb[i][1][1]<2.4
 for a,b in itertools.combinations(names,2):assert any(bb[a][j][1]<bb[b][j][0]or bb[b][j][1]<bb[a][j][0]for j in [0,1]),('Whole stations intersect',a,b)
 assert bb['c'][1][0]>-.099 and bb['g'][1][0]>-.099
 contacts={};floor=triangles_of(FEET,vertices);shore=triangles_of(['SceneOnly_RaisedShore'],vertices)
 for k in names:
  z=GROUND if k=='d'else SHORE_TOP;tri=triangles_of(names[k],vertices);mask=READER['np'].max(abs(tri[:,:,2]-z),axis=1)<=tol;bottom=tri[mask];norms,areas=READER['normals_and_areas'](bottom);expected=float(areas[norms[:,2]<-.99].sum());report=READER['actual_opposed_face_contact'](bottom,floor if k=='d'else shore,plane_tolerance=tol);assert expected>1e-5 and abs(report['actual_contact_area_m2']-expected)<2e-7;contacts[k]=dict(complete_ground_contact_area_m2=expected,actual=report)
 report=READER['actual_opposed_face_contact'](shore,floor,plane_tolerance=tol);assert report['actual_contact_area_m2']>10;contacts['shore']=report
 tris=triangles_of([n for nn in names.values()for n in nn],vertices);rays=[]
 for p,d,length in[((0,-2.0,SHORE_TOP+.30),(0,1,0),4.1)]:
  assert not ray_hits(tris,p,d,length);rays.append(dict(origin_m=p,direction=d,length_m=length))
 return dict(instance_bounds_m=bb,complete_instance_count=3,distinct_old_models=3,new_reusable_model_count=0,whole_oriented_triangles_and_pbr_retained_before_float32_translation=True,actual_full_base_contacts=contacts,selected_visual_clearance_rays=rays,not_navigation_or_full_space_proof=True)

LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate(vertices);result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,1.0);ORTHO=7.8;WIRE_THICKNESS=.0006
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
root=bpy.data.objects.new('OneWholeShoreSamplingStation',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole scene horizontal centre; continuous bed bottom at Z0; three entire unit-scale qualified instances';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 # Preserve the already consistent outward oriented triangles of complete source meshes.
 # Reuse the winding-preserving scene path validated on the prior loaded-sled scene.
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
  files[role]={'path':f'assets/camping/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'scenes','assetKind':'scene','theme':'camping','style':'source-preserved-faceted-natural-ecology','title':TITLE,'description':DESCRIPTION,
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
