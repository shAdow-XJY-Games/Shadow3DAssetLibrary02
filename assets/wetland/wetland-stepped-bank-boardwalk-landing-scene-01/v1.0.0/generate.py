"""Original bank-step-boardwalk wetland landing, three complete existing models and zero new reusable models. Lightweight maker SELF_REVIEW; no growth simulation."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='wetland-stepped-bank-boardwalk-landing-scene-01';VERSION='1.0.0';TITLE='Stepped Bank to Boardwalk Landing'
DESCRIPTION='One static wetland landing scene, one scene and zero new reusable models. An entire existing two-step stone entry module sits on a finite dry bank, with its upper tread meeting the top level of one whole unchanged two-metre pier tile. The whole pier retains all ten deck planks, both stringers, four piles and four collars; the four full pile bottoms meet the pool bed. One complete original reed-sedge clump stands behind the dry approach, not in the step or deck route. All three published models retain every original GLB triangle, original constant opaque PBR and unit scale under translation only. Three simple new scene-only volumes form the bed, raised bank and opaque shallow-water volume reaching the pool bed, with conservative rectangular clearances around the four actual pile envelopes. The old wetland boardwalk scene explicitly had no bank-to-deck access; this composition instead centres a real two-level bank-step-deck interface, not more deck tiles or recoloured plants. Normals are recomputed rather than preserving original NORMAL bytes. Static illustrative assembly only: no certified human accessibility, navigation, railing safety, structural capacity, tide, water depth rendering, physical flow, ecological accuracy, wind or plant growth.'
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
LOCK={'harbor-dock-module-01': {'bytes': 60084, 'sha256': '405124a33aab044d596373198a76766a0acee752b3266d46dea748070fe4c14c'}, 'village-low-entry-steps-01': {'bytes': 2864, 'sha256': 'fad9f4b6662df4e29c0596dde11c36827dabba71ff43b9b4f2502299495583d2'}, 'nature-reed-sedge-01': {'bytes': 35680, 'sha256': 'e491048482af1abacc8d0e9d773840f3139863d2a17e8dece5cd1aea4b3ef9ae'}}
ENCODED={'harbor-dock-module-01': 'c-rlq2Ygh;*1*r1MN}*Z2ndK`EEE&S?q)X$guPNk5hPR_pav2k2nnQsh&;jG6@92+Z`eT*JF*Cfr~yT>7wiSa@~qFscV>5IIoaHD;`jXhKEHRJ-#zo6xifR;lsj`bta~R;896`!!1ApCr|t%D)QI9Cv$IO7tIKM#dd|+8SXNP1RZ>$~mDMwA(4?x$ipuIv6RAt5zEjF7O3SJ`4eU|eX+~c6aQD3Ytn92AWmVPXl@-)D)IB$APIgxHcp4z9XKsqBvwDu6omEjXmFluaB+g}LRaBNHPUMcAGj>O5cGlFg>Pd;NsrHjfs>W4T<&;*AKP6{sWohk{vYgytmhLmPq^7K@ykttUUuk9SxG7~L%1g^ivwGH4)t2oTp|YZE7F}`LxT>SeYD%U|DIY()vUcJmnpm~gc3eqyS-;9Dl~n^u#wT<holANZ>i-G~L;1mAG+daMo!dPW$xBp5Lg8RERG_PZxyh<%ekhoqmlw&)4(f@eu42X`Wva{t({<eoLdi>n!@=ArjXGyewwo5!B^9NOR3ciCoA@t37zsrp`Fg^6;RaQqU}1711-bc!bmFg5p{A^4N+VUsP1(FKKQ~yIAI;B?YO5Ed>Y~9&K`<|*l}M_U8!9Zw4TVFY|D7WeU8^V658QsW<I1|{2E$r|s`9DjHRUr>4N7Wis>;XJ)|4gG7+O4H;K+f+LlT!8Qat?VK7+G*2D7t99)4WE;^N``Ps+{e8KRq{yrQ&xyzUa-5z5p@o6u>%yd48Z>JJ#@1LpGqgKh&B>=>}H{(!+;K4LJ)hYZb0+_NR)>0EVXRniFKY9~x6t2(B<Y-U37@s(4j(S27@Gji56vR)(@it5VR3R++af>Ax(snjn>zRQm!omEaN$mkrZ$<EQ`nncH}V-D{Z&eA&Y3j_rhaO)pxRR2(e{$acR;dK9?4nQ-&h<<$r_Zi+`h&=ZxMDo)%A`2Bp6VV-}Xpa`=hZ`8pwn;RST$`fNP%unOnYURZf;qYMk2b1*L$l_)n>D{M<Ym<Y_Zfupa(7s@AQBGJIv=9dJsK{^)hkP0BtJq%4CdyC3JSu}L|sABut8cnBSGrGt!_6&ZYYv)1Zf+}FUZf%u^qzAjD-RvT<?zDMh(!=55b_jBl5xx9YH$n7=kYeiRED2teUdHWfc=^Xm2k}_)*ssPneK+;?UD6shX%UoL3kP?U;|CbFxO-KN<-Y)bAfGj1=U_2MFcmWegCC27?(h2)oUoFqol1s2~z;gb5lB5RT;KH^K&a(cBCb@<QRp*dUm&SiJ#g<7|Wt=<dqR7@#1zI!L|HV1P(4FVctsf`y^X0rJA(Mhs98%`ibE8p@nNc*k9lx+B;Ck^EpNmv+)lTLAhF90K#VogQEPLl=v3OUl7rvMqqQBBmq3y03(F-}&2$(&I=N;IMRGFV@%6eWlEFk4u>8B4TDMF{gA9bIMjCX1a^G*OuaRY)H7SZgASy64rf9EJ@k;TFNGtB&_FVVnf1A_qddeuO-ZEC1R$#h?y=TX0{UX;%nEgG_fIN<7)|@z3RD@CYB_u`x;+M*~F5B^|efFNSNs!moU>s#LQM=HnAaP?rSe*x{G+<9%Iw7A>opbho*fkVcplnl9Y|FrEFqJ!g_8dHYCh+k4xG3TEfg$B4)aanCT*7W-BSjSe%HM`P!3dZZQ^Do~-*azl)f~k|*nHu{iN$rh8n%OcxO|TZx&)iHNzcy_o4PVp_XmY;W>pTDxLw-|=MKm+fmJX8Vqa*<R+!dTwl=@?@raT*_>(@nmKz5i{LI%ybbkvz3VHS;%6~$s%UYx}HqWW)^#{_GI0cJ@<;3JxhDCz7~5<_GG4eT*6Ej5i?tfnLQ_qnETp`neHOiHe#R6Jz4vVeeU*TeX!5<B4(evMa(|Sdvdaz{+#Z~O!v5y*=KD}X0{SB(_O?&7ZEdCiTH%lUh#1FJ6a#7SW-S?@^7)%Zk;A#(j&pTuY`5q=WjmPGUG^iTJLU_>FdS%TDq^4neK53GhIZ?Y$fKDE@DpEO2kZe5r1@hhjeU6IM%Ff+Sd}+eN8M$+4x$@CYB_u=VoF<!c6zLl#Q<?%xooMrn`ulE+S^OlCs6(M8wS3o=kJISX_Cs?#uixVirrDtgpr5#FLrsaS1bBM9gd@W)>$R=Dzk~rn`t~?XuY3<jHzpW&4gN>%MGX6EWL&M9lUwPu6o|`;;d$-Q!YbdyOYETZx$IE@GyOh?%WK{N=C$>JOk}%8l31^PwAeUwu%b{phleuB_X;anF19Nwg2`+TE3PdoR}Q7cc7T%DTN9oB7X)jc{e%-i?ht7cD&Am34bJzWe<_>Fc_&xvmr6@bj^0JGim2gBu&axUunz6Px+#7;s|~Cr-@l8F%B9Jsp|(*OgQDbYvE9uAH)`E2r$~$|-v~GP@sLIb}~rX6u71r`88YX8v_$b6qE9@#f0L4sLAx;>N}=PR#B{S2l6t#AGXrt;3GY)?{0zF)el<IWoJaY?*Yl*nRED>>hVyw$3;*TW4(9%s;ihIWk)VZQ0l}wca{1Ta#^>?h%Xa3y#e82wSFm)?)jVBeOlrk=efK$ZX%VWi$WOe(lI?Pq$@e&$t`2HQAP#e_ff~Q?|_F&6U|b?#OJNab&j6*fP5xU74+cw#?QCS7vLnEi?bRGTS3;nZ=tcvpvg^*}mz>Y~QqHc0al@+tY1XxBb3JBu+=7U-ECF06jOfil+`Mbv_RD{+ny@zM1V)=N#+nk2yDE?0Vx{Y#b|d9Nvca%WQAXJB?#!1M{EVT$x^Rem=9F_xI4ZUR$Se_<SAojn~(u!T1&%-^v`{sa{~8%=odG-z{dJdiC6YnL2sIo9#F*@nA8(TQ>H|jJJC2Sv=d;+g;Nmek|r+%jW*djE8#dnZIo7-R$WQKNj=5#qO7S^%>(^F8<1lH`{TX;-}g3t>XGvxJkDDWVScgcB*ge`jZ;R${fcj-ZI;p^G@S5cKu;`)mvLK>;LTf<1~&_{4l*l>rZBTGrm)OW7i)&2J^ec>{GA)&#pgC<G93w#r*EM{$#di@oZb)*!73aU$p*YwrBpbt#9o5!}O}Rwq(}-+4aY19Dn`s*B^iV@z<aKYwM5y`OE+O<$wP2KY#h3zmj^EztAd9hxOKa+4_^&-kf(D=kNaf!}JoZKbh^#_)hhI_vato&g{XG^(V8vIp<XWcYpq2devK7GVA~B`r|at-(~&L_GNyL3*xO_duC7DasKY>57SGu{$#c{<2%*=-Pa$zrm}s<bN$I|Z_YW@|J~OgrdPeSCA0p|u0KxW@V3u}Z-^yqGpjmIywWhghDVzQ<9yt{IMJ`~X>A<Gv1yaY>(|e<jTetLnd4Z3aV)2C*qp8U?QQk4YtvvHW<$quY}%M{R<diw9p>ZK#@L6|&y73S$E{7~IB~%^ai?*3T-9%HtCw9HKc4+~_T$-)XFs0(c=qGjkLSNEp1Y1|9=mSs+?Z3|qQ$1zs@1hc-Kb1s#Z0d2Q)4IEwWRX0>(6LVo;kCvHJAEl=BHAg?B6L-{;|s#OZPKno$LO|b^tmzWuEJKmiF2nbISF6bgt(!WZYp^W?Ad;W0xW;sTZVkQ?KWtb3MQ0c*(NPb$>k%U3Sa${~x1s)1K#F40|+TFQ*(}Rob3*xt{0iw@!;~rS^*aVscZj=c)5%uN|1SFE8tPY^JhXuKlg^MQa=8dY;-YPPv{(v)2Nao|m?($xXf1&-lYG*Ynlw^n6WO=ccUZ;g;)o)BR1Jil=lLV6T*&?emt&I4|11JsI~Vm&X5$r2UFAa~}V?46q~qlVw@_>v<;a;*@*GKR}U{)C<zNsZY*F=R4xx)a(99eTp1&ulV1-{gH&doN`J0|F*r7+C7@^i^+G?>-p;Y;2>t-9c4YwCRBFHz2aYAFKHM1JQ+VtEQDm-o7~h(;$OGhzP*0@o3dB@C;iaGGP#L=Q}*NEkN^MX`1hZG{O6zl=I5Ucb^FFv6wZq|<;QfYi=8~-lcJ4O)^;$tt~c?&lG+_h<*e~%G$_CFbvsM<=eh1@@<hB-{f4^ZEZt9+lj9`wSE-#_uIJfz-5)WhT+gRJ<$AvFUYCr2ULHmHhPr~pINB~IH}!fRI^Rh1OODscN{*AvwI2FB&vm@>vT0|RFI@OQ!d_0fjt}DpyIjw+AUr<NUi-!5re4o8kMg{5XKO{uzPzmGq1!p-o0EP@ludh{FQV&dyEx@~p5gG$)}q9`Af20ft)KRXj+eeRd2+rxTYA2B<)pnK5f8eYnd|eqy;JVTzaRhq&GD~&HRdv9{)R`#O%EpXxiMA`se0I}W2x0|(4N+W2@?|SP2Q>J`WUMRlW(p#%~}x1N&KduZfEj4-uXVp>cQl?{VBf<w?g4?qMgZgdsYu7*YkOD`E=`=g-JV@T+fHqgUPkNw@sU4{k}c%Y?RKmzN{Wh{>=v+65~HtSC?pK^0{rd^k(&7^6dFLCFXzi!i9-;CcpgPWkswWOs?B&JFKr8oM>lq-JaEh$@P4+o!8XW_15i7uIIz*!Q{SwegFFY_5JJn_y4AU3*a!=o#gJ&1V+GUID+I6kPoBaU}!<I1@wm9pe^(u*#q{6PS6F$kQ@VpK|xd41@?rNus5`aeIW}Dfo_luA;^QC5QDzZAC7_{Fcgk~<KRT-00C%5vKj0LJ4175O|muY3ay|sbSK#z+Q6Z3Aao?z5pv*2*ar?Ec>o*@2f;`fOL8o9h2vou6q785lOPO(U^vO)5QSsOO#?^{fD@n}^nwV<2pmpY=0YLKLf8q4U@zE%<Q~um+QC2wk_-aEHE<J5Avpy~;X!x;?jU&wTn!JwIWV2%bhsW)fthd_$;;pjm<#8_3X&_}UKj@xU=mb771Y3Ka5|g`=fZ_>F<b%vghg-z+yb}3-LM4ihlk-&SP8RXJWM7z8U6tip%Q9I)<QW{!+CHi$xC4dTm)yq9FlY361Wpig?S|B!F_NxEQcpaJ_#4VWAFehCAk#ha3$OW%SbMRtKbp15f+nN43ERDa4jq#xd3j5li_k$NOB>R!F4bVrjncrH^VHr3+9uY4<+z30M?PLgSF5KJK)aPijJS4HGT}6NN$4P;dyusz9#uKY=QUSGuRj3qhohm4eMY%Y=oC!GrS3J!w2vQY=tl3U+_Kr0)K$QCfE%3#J#W$?t}Z`Td)S6gSY5-7oLF^;1!auz_ai&d<tKY{0d%$FW^IXhvYl34R*oT;eC?t!yfn%?2R2scEr!29k#&c*p80<@jKWJTas*vKSEpF4o$HwHpTWBz+d492;dK}6Rv`9;NP%{j;G-_co8;`+yIDgz^?c$yaC_BQ*a!fjM;b`9S31G&c=x(C*rYKi-%*7WDv*Vp_q@wB#Y6)!|+Hvo#g2_1+(xF?1J4fgn8H#i?A;az@u<54#$yr0-lKDuoNd_1x~{mcq;w_d*OlDjbt~BVQ1`t5t0$?ieWqghmahCQ5=N*us6xxcr;GJ0_;Pw4^GAYSc7v&&cT5=3#Vfx$x1u}N8l+~MY0Ny!I^jxP9Qk}Ps8yz8b^^Fg=N?YhvM-hkH>>?4CZ1E$s8=fLM+E&B!}Sv_$aQzi%DLLXXDHG7CuAr8GHm^!P{{@$@%ysUW8ZUQj$yYM!X5{#J5Sljdge?o{Q(>rFaGY6BpricndDZyYXIJhRgABT#2i3Ek1`E@kM+UU&nXxT09FcBzYm;fal?5xPasWya2DnJ8%ifC3qFygSX=KB(KN&a6MjwH<P>>H{fl!8Q&rK4&H@t;3j;5<O{e3AH?VJC6X`U!}uD;aUIEZ_$IEwC-5PX58=}|7w^Z%NIr(=;0nAPFClpeK7|YMS$u%x12_-&QJvJ6B)`OuFsyp1&MHhtTNP0|sc$htM@RJq{)Ej*Hdosb)Gn$>0Ug=u1N;O(!>{mP_&xrDzoAl1RWr4_YN_^C?bUuNOC6-TsqQLQMOA@{sbBF!+={=_@dtj2U*iuXf56Z2JKS0AslLNK)sMKF3aH;n{*HU7F6w7QlBjZ26P2fWlkBZ_RfQ_3dXVg)EY(UKszM|~s*TE5`>R7p9-?}x162prnq+HruzC;oQte2#Qy=5L>KoifavL6?{*7H#3z99=``AbIS4XKnbR40MRD;w|l0((eYKR)9jwN}l8mUI8W7JrZW7P@jcr`|iBRNi;q)t}j)g+RWRGFHf%2fr)3U!K_qAFD_$y!yViq$~XkJ2nvO=+r{NU21PrZkGq71J4AKatASbQG)Usz%KwIa{5oW~$TF;Uo`Nebo$gm>NK7uo_P3ICUbWQZ<><G&(nf&gl9RsXUyH8ETH2tIj2Pt~yJdt<F;yle}16pe|IGs4GccsV-NSsVme%k_**UYJs{&-9YjNb*;Ki-KcIOd7HXf-J)(+caywZ-J$MO_oxR*KA@JUi_|&l3`!5FrIhYcw^F)ZT}^2|ox6z6==xi!yp)cM)P3rH^$5vF)N=KpdRWaPIZypVEmNnfGbx>~E~WHOwTRM9YB8mI>D)3pqw5z@`BFNTsmIg`wVLE=6<4d&8nvF}diAtgr=C?WkbFVaspr*3^$N*X)JtlU+N|Cr`KEeJy{_I;?~!~@y`$b$@2gKpexg29AE{5(Hj>-aR`rZ}N<Bg8TlEE{kJT1RZ>X0kZJ=|{&>3C7h00&h@r?RheW|`9`JMVkeXahbo+SCCdR%>_9#tzTtyRxadQrVf>237^rO)WxS9C_#ze?rj==e(gpng_=ko-gas(w@3Rg=JPbYMUQb_(o9a<{-Pft>@*0xd|k2<#cyBd}MX4aqivR)M_(Z3Fv~+&9oJ&_2*HkVP^puz#Ra;J`pvl3fFb1OkEI)lZai0-Y%x5a>Xub)Y$=T?6{RpOmieK;_PK1Of*Kx&(TV>=DQg92)2z__sQgjvrOG!1wAGN)TvDY4<=&O8W%%qjXT98>L^Au5U@@rgU@*6fQq9{jM}Ao8R7-@SW=hrQfY4VcpmK_P&(OZ~IGFU(5Vfzl53YaS1bBM9gd@X7gM9QZ~Q6FJY#;h;x>8Ovi?VSKin@?Q03^z9yEWY<w+c6H5}-b2G6aVWxXr%Es3cX0{SB(_O?&7ZEdCiMZ*!*6G-gvhlTqYp>iV9ZM3{eT}cBY+^~m`dTJ7B+PV=OPJ{*VrDBbo7j*t_q7)@-9`NU@0-)_+LLgbH#Vl<wI^ZS*Tj;PjjyF_VoAb!ZYDM)%yf@S+4x$*%vK_1x{H|UB4TDM5uY)+C><M8Holf{&*ev^V@blgukp2%O)N=RU(3XXgqiMf2{T<p%xooQ6B|<IzV>3KyNIW?JZpuC4Iw{ad@bY^CYGdZd@W@YOG19a#D<WK?r|v_UklmTO3FreDL=t{En#CTDHpNW5Ha($gnO}Al5i38wTM|PNw^n_4G9;q*pP59=4%NTu~-r@iwzNTUkkVwizQE{wJXN<CQqidE5`O6Pu6|ez9wR}?}(V~WuC0(#`Y;sX1d3v%=Q{jX0{SB(_O?&7ZEdCiI|>+V(d9t#Oztulj+$k#-6J^S@&hny&`7M(w?lZ#h#Nrndu&vFw;fE%vNG%&&eX@zV>3KyNKzto5enxdoq1?v)JcuPu6|e=Xw#d&)p(spXEJS&y9Uf_hhDfT*~aTwkI=NiJ0jwVy26TnXN>ev#g`V{!S=j_P0JyUU_4Ci~U{ElXYMAcRvxcza@IIz83pCp(iul;}T}Nh?v<*%<S)kBIdsKVy3%@3zr{hv45NJ<U7|5ve>^nc(U%x{#`@F?B5+k%>FIIll9!#zf*WJ(>*R__HPZI%xooMrn`ulE+S^O60!e#+Wzlp{}sQd?f;&w|9iIn`$YWp$NxQl|M&d;_lfxHkH7x->yN+w`0J0q{`l*UzyA2^kH7x->yN+w`0J1VJ~jV+YJbK1)cp0wUw>rlkN<m^{_kP>zX$8bzaRg8{QL3m$G;!{e*F9K@5jF%|9<@Y@$bjKAOHWK<KO>1M*sI1{oiBse~;1sJx2fc7$v{Q_~o#I`0Twm#y&W0Z_ACR_ulHtKOc5rqJ7s99b8$rcjIq+wMn#J63cOA-QJ6J`)+0ZTv@kwV>ADyLr1x?Ztup%p87pRZmiq8@q6QrPG8rJ&2^pl(}^df?cm174sLAx;>N}=PHg6{W5A6~oH#MFXWWfb_H<<CUsq1q(~()cxpK;$uAH)`E2r$~$n1V}<&-@gnXM15oLV0onfce1&2^oa#hWV|JGim&iyIriI5E2)UD?Em6O*khwhlWoTa#^>#<bXd<jCxvvSrfIV)wNpvwPf;**fFMY@M-XGyl~3=E!Ufv}I$@)Ozd4Y)!Uhx<@RwFE}#WBW#)OS&Qvcj?DHfM`rt`BeQ+emd*TA`?VvpJ>8a>J>zc7)?`~|{&i(`PuVhyH&<r&xFfT5#*x`NW6SJ*bY->%+A>=oT$!!Ow#@wN%50CYWfpI)%=RotX8WcivwhQ++5PCsY)`jkhxfe4`TNQp-t%tProlM%-*<06j!m0*#yjrgHt)E%1Z^_Mu>|8-PUG-*+}Ce!tCwAy2IKJe-8+qA(<bx1^H%-$-P^u*-mXnN;~n>w%{%TbL7U8R;(~GFPUG;ns^8vLFS|B=Jp1wN$Fm>Lemwi}?8mbo&wpV&H~#&A{T<#9*x%;;fG<0|A8@h5`vG5ect7A`m-hp%aCkr9ivQ620aw_(AMnh!TY9gsc|Tx|!}|ema(F*rj>G!_Z*qA*V1JwU1M2zo{|~+Y(f6<KU*EsJe|`V{_5MX@0?kM^gPma)*bVj~slQRPC$xaJB-_H?&<ff>N0J?(J+w=FFQ^?I`ny91LYKrhhz^EBpeuAI*&PmrZ0G?Ik`V|&bJ!IElnNnCDF-@JIsiIQYE9>w(-~dgnaW{0nnMuspclzrPyqSR6LuoG6DWw%T$@tb9a>V_2lk_M5OkxIOXs3=M%V90<(70rp*I``14s^le$XF|fWagO!$3F+j)oB=N5D`hhT(~C9UTwHz^KGGnnuwv8pgm$P)f2CN?;t6!DNz?VIoX|Q(!vD=}-ZK;BX2G3u>W~QaOyLG!~AfG>py-qBFXFJe4cy7z9&c8q6d)6KbFuW<Vd3eIN!^Py~G`9SK7yjf4{@oeUEwO`&sDbVk>oK;<EHRKcvo_mO7Np}(_q7M!2>=F&NEE?fYYk-Q8phKt}*SU_?CTmkbF-&vYZ$JKBRTnjfPz8Q5r+yFPjVv>vDR=5rBfcr?^2Y17HFb`%^dI0XBbUWNgX(3!m=@L439-YzkHzvNHbS0JVf_vdXk`KcDuoRZT9FlY3G*|+s!apdT4Hr_n9Im2t9o$0cPCB=Q&glB9sC*$EOW>izH>n<?;|W*+aac=oEj$IQ;c0lD<nyo|o`L6J6Uj}m5jMb!@G8ky;bqtiuff|S--b8fO?U@BAo)S!yG$R#=OjOePhbr^36D_P2A@)TAKs$$3cNt+Svt3d&glBLsQf7%Yv5z}48A7$HGBzQz*q1X$;aSf*b2+xaZ0OT9i=*WiPG!vE~Ss?+*UfH>tCYsIy$z({{YAkvQ_', 'village-low-entry-steps-01': 'c-pm9+iuf95S^Anx!*4>yhQt)1h02}i%_dlfmA3BYARkT9-L&GSaR%Yy(v^xBz^-vhWrMf!+0GMhoni$#g^rh**P<3X2+XWc<_1|0E`;|FIEBG)T(=D#7`2TNac*QL?ooIVo56GZCl1soD^C}DZC6t)D*I?^SoL(;bm6l4k?loA(J4E(Ag{-q*o+K0|StXF+d5a9G;QL@1Tv;^jeWbaZ@iCAA281zs^WUByCL{_@4w}=(j{Ej6an`q~vKSQQ|l$8I+{Nj<19a{4gUo<8D0^wV)}Qq@rY348tTU)@hIH@|{qA7zT~~xZ7%@x+E>R?k8e94rBS+Z|K4gjWVO2zD$=poSSyhD4T9(qPAr*?l~;AvCPJ8W?3%voFYwy4YK@-hZV_R35T|_Yig>?7&UCqvwFSa+$u_8&}yp-*21$|T-$YR&vB`R!kLo^w@gNDEHX7wLtiFyIdv`fuS(I>q&>d>+i|3Vs2g{a0&Zy`QGOuH2JR--BZE$$f|CKkS4sx;t`fSa_to0Y!A^Bgr{AmYzuVd+6^g?aM9rX)`k13>K&P~k=S5(n2s|Ib%159*J(+$3my%d!n(E!7BOyNo;*-|Vh&#u)Bau2dJ;vfJibI0NZiJta>88;>XOon5l~T_%aGbn!l&0D2vF<xw+Q9%nti#e&|6*w>MQJhQ!>esZ(l+Ep)A^!j(amXeHl*_ry|%rzyR|<NfX&YT|9e)ZR%Wz3+u$}w$rtY;pIgN&wl%wn)SPG{${7X7Pokc}`l%ATB5El-I2p4uL-puLpXRu(eA!AN9$2<H5;LEx4U4k9-^jLOj+5C1$d2v)d1lw<i<3=0PR6PDUG}j1gU;tuyBv>+!jDS;FL(Cf+t;t(@oyF1>zgz1#v(X-#&NcO9$ufoY2Nejz^^|8Z!Cfb8pd!=+Z4P$fpgl%FbuCRn}c_M{GGohd^V^1oNMp@1ABh~o&5!L_Gj4pe`>!Dm*5IKgf(~!E3gE2U==RI1GoX#;0Y|lEqJEAZsKzVuA=vK{QVUDZ{xiN_wZgr{t7bhBliJ3Lhch-NA5GY3$tf+>Kty&o0G|T$oJ*n;w5}mu<B*3ehJZK-LF;n34prz<^', 'nature-reed-sedge-01': 'c-rlqcUTlj*Y-~}V$J~*q9URq-~?tEV7g0;fQX6_Oduel2uM;yz?^ehbIv)ed1~66bxmtdYYuD9VfCwN_t~v^_O0ES&u{<wUiT7yd+I*t+;w`oXPj#q;uG665da`+48V+%03oeggk`%%r=`WEyZUFl#>XYarADVGr@H#PHtUg^oRpkaEuN-SYmgY16dRXXEx2BbYMDOXT5lg;S5Mc>xYV?S<RmKAc&l7<JYCabXaQG$)$f$%>fbTjH7U9`jk&f~);wL4l4F$xRp*?}fBs*#Ywx(U9!l!(`lRUejMO-<)VR1<ue7+>_&6_>+SQWMJ32isH6c3jTUu;#Mz_Sc)(Nq3v9A8<sTpy96i7`@PWMVnPDrFpQ@W)#k4ukEOiYLgPtJ(%LA|9}Hry>bEv{j5VsdJe=on?&9aY|HgG%}1tJZ0BI$y1?Cyi<Rls`I+R;||<d^9ws^3^Fijh{iK(P}h4o@$G`-`o7BAl*>ve>(mV^EP}d=c`xi3~C>ZIw!~T@3s=3N)M4&T94@1xc>*6(fl4$tNk=8KaHPdf2!X@K7KT;S8M+5y(A{2+qo0X?|syIolfiH=c}c*wcla}o!-yKV4yp+Y~|ZgQR)2jDj&U%kKtcGEa`E*?cIy^TO%L6R!2MeS&oX<>Yy0>^vYrJ`(3Eg`st|l-`h)?<vdG|PO@_+J}RqeTMmHs_Xm?kYw%GUbOy^l{v!LHeJH7EJ*+P;Efb@Y(yPTJCniRxdebpl_K}*<J0U$G^LJr%dU|R?w~X{SWiu^Xv<_|)+#*bA8`dJcd0?okznWgd5|UyQVk{cXpO+dcvP_RxLHlO~AGU&yt)Tw93i>}Q__7rYYz58VRq$hWp<+v@)ocyz-_@X}{hvj&Rz-Z+B0f3FwL3b7uB9cXej9JMjPBjzQrjiO^;Je1liWKcIVmnFy-ijMJw7_MMsEpbB+(}tKb56gzi$^Py+(O(_-cH7{WLxX<-+>=qvbzWR?8zutJ3?Z^adS0U$kmJ<>8Y+pLsfZDUU9#UaR-hYP7yul@C3cJS|Z*eW>~BeDoSUy-?Frji#h4UR>KXZm4y&41)En{%6mBm#+Dr(zSo2)2q@S`K=oUh6aZJrGobF4d^ZWpQ-8e^m3=x(TlZ?UJiAZ3DJ|opjFYcg`RghgWiXRd@S?w^YNkA4wYV~wHlhvk6vi#l~dzK4}hQ6@+6?rXtX{$U%f$N@TGtJEK{VFG+LcOqo#+4p4Wzd7^062d-%J2-QQ2qm&xZ$QUCW2)LPBIK1IDj>#LzxKApy(@il05{}*%gwP6>3mv8uoN28zNpXTWI4-S0Q%sH&0yY$s*wFb3Dr=ibXo@#HEkBUykSL5qPm;BV08K~4+KLeejPESu{wLxQb4y)B#9UY`EeGvN6Q7MC@16BK3Ub^UXYOSwcs}#}e)V}oDkUoXd>j53>Kb_Vp8#eN{1=RmEOU*ycQmy$14|)SLO#1TDV9?NcYJ9bH-}Lnhz4}?b&iOV7`sgy~=_?@$S|0-)h}Ar`Y9C)(ggzL3GzNMZwLG@Jy@)kv=`*yRzLr(07-(~PFjVvmpk-9Le;TLOhOPW<0U!IvNj?2pf_=78o@u&erN@QFCB>)rupDi}?~xYWyDR^wv0QeeQ{yd2XQkKt>BolTZxLJb=_@$vbPat9vQF3jO}ekn@;I@|_tD$Y{;&D;Rg=b!?fdBdD_`yFWAL$k1M~%&&wmv#_-XZaIQUBe4ZVoia|GzCX6t;7T4l!$EbacgfKFwHf&Za^kL8KQ_8t6X0(!lDJ5c}k2=smigFQR=O94OCe><>i2lQ&A`O9hW$0_~$>C6_OujeeUFxT`4Xb>C*s!(?czWo`<<6|o>ix#-!GK=t7vtg&v!Ufx3=W@fy#l*txRz2bJz+ENG7T$2M9+!Vv@kY_F)H{hh-kLL8VWa;oF8{FXrs8eQK}U(l<rf`O_Be6G1d+#$FFqGf96xT!8E6YXZZ}WiNxH7Y7IssOFj_bOEwqWFrX~^#OO@8x#DzRgDLiEI7n3dQcW0x*Z^m9S+QQ4#(F)%^y;!t`XRckO>}7#@k4+qvF-4ix>FX_Q;-HoT#5$cOSdQO79@qM%rouDMKQ!^!eL*p!g<r3(O?Vu4@tw)SfuTNJUQs5JSonE|VJ04*?BuU7dKhEm@y$n%m734z)fIWXBhf?g*7tn~m*4fTr0ns^{!2z4|9)wZEnl~ezaw=&7>ZpxpO8|?BWY2qa9n8cS~IH|^)f}$S7?lXyHZ}}X|^sEMLe=Gp5DV%X7xM`NLS1c_qD<9E4NtHVdFzumy*BsZh@~lm6KRail2jAD5g0cJ8zD}(;U3~fE+IqhFwaP!>pdwtg3uOQXdb&MckiBte&S~XT_Uauv`Ssxa)-@tACP)4=ROaCmr7Jdcn-jBys&jDJRYi7wo0CnkTDgXH}s_toY%n8(!L|q0Fnp)3fuOySt!VqKg4{TXD<Gi?j0#ysnY6!_+uqps&Q6`MPb@<Q}WN@sVS)m7bmFhl|C{sT1pA{Z+lyv0!uAIcFSsErrF_#a^RIVO|~Haba`WWAXbjRgNw17_l05wmc0xXI9VCSk0f&uyJ;VtcEvdR>RJR)w3FQKCGUnVP};eDnJPcgZ9uE9Kjg`C<s*{9~6LEPy>oUU8n=4zzd2)Nzg$(C=XgF0~Ns+oS+g^1|zsaAh>`#G=ys42Eot-JRlT8Km*Oe8`RJmT7W-<gAa(%77QRkeTcA35gh2>a!^|No}Yd%p?E0@h3J3zDYXX-4d{Q36?Z|@We_x@U&EjkjkJO`^s6IOr>+Y^P3pP;6sE3=Kr!mN6sV}{l2DeqE)RaxbwvoEt}6keu3e!Kb?pvKscSc=O<j9{Cv~lXmejQx^whOKw4<&?=s;adP=&e<dF(HC+9De_hUFT0{C<Lm!pm<TH1T+~X}?jrbIJIo`*xeSMcQ43i!2#uw1vNn-6_84Ge+|I?TOu7*kQH8C1i=%%R=rLvFqq@(v@BYoA_;k*$V%#_@mJl9xVDxPwN%Jy;hYM?d6?cycO;kK9$(ZmwjEOn}-VH-}X%6@}f*Hg=-#j7J0m2&0<NPCF0{X9F6w!@oDoFE)YGL*vl`?vnBmCj3=F+$mN4S&sR9TZz&^>Td%z<_1@C}Pn@>P^gTSO_icqwjUP$AhvTZ<l^o_Z!fnJ+R$MFUzQS`_m`yBiy;2f8_*cW{T1F8bkKXf*z2~KH*=cww9C5E2{_#>DE;m^4jU&fKbGhkj5Aot|ld)9#eiM%un4F9jo<1Uw@Oa6jVLSI;ylQ;<B|n!ZRY0PJa}T(fc&t0TTwGe9yJT1uOzh=Do0k|Ze6)*fH%mY0jW^PJO0HX$a=C8OG||Ej+BtD~=CYzvvGiNgz3qqW<~GiaL<=8?u4%THA7r|V70F#`Ououo#-gKS;nXji2#?E-43V~Ua>iGWw=vtxL+=()_>A9RyZP#T2g&!W3l8p|%jLudO%xt{HjK-wHVl*+9Iu9-|FGb@xZ18x3eVcK_PhA{^e$4t^{&|Xb)6NDo;OJ0$#)i7@yFm9()Et{@N&&rE)ShQUE%pL=eTUl`9Zo`!V#~Y`7@U{)tagB<{sy`Y&=@ocw+Ew<EwdrgvV~aFH9DWk8|eoNbggo6Hb?m<F%_zws7W^&PEF_TlU5#zI%0yF{j8>>CuYa#9r3;B@hc=Y&O?!UUV*!TymQ(ZMZkUCU#u5!f4^1rxx185jum>b73hwd{h&&y}Yl}eq!ObFFft$g`><QpRo*Xl39(*@h7_*EquP1KbQBGE>D)Y2V>`QtL^5&<sU1&^WZ|ex!a`sWX;HCxG>D)^1%Eh6;2FW&gHjv*OSYpFx;r*)9>QdXC2HIe*NOXck#5@`OJG~w8Y)#J+k7X85@a(x0;?=u{$ng{!-in4+$?P^Ek{{OyO5fd`^E}%sg_Z2mb8>pF>|2Qg~b$CoY5Gsfn0(7#%h{6CQU@ZA2{G#<S5b9`{_~NUmMJVH|vYRRE7m21T1Je7W{p6OY%uN+ro%8cOe5%_R16tCxEfjywk@dwFs9<-{Q@Na~c}wUfu;R|6ETKY29a@p_*d#B2C&DKhAt-AoR+nJrvt`(Bg1oOhz4Ijh`$DgUl1Tvj(aLM-ew>M`N*`RCotMc(DZT|U$@+spY*4pn&IV42v<Nv8*ytBfdsUpw#M@~U^86rOR=&CKJ{2UnO&ohgVv28VqYNA}pP@X$%_-^Jl;e>C4V6~;rK)Ux8jMOG>NacK)HepTwKxk=<NQo?V&x!k+ZHHA@hPc9#7eBC_sB7H5oxfhq4hh0<Ht7S5mKObsDZpy^CyGf^AJTBd$h{C;A77=;eH)Vop=cOygq8siQdF-x6#KMi*JDYg?#JG=)e3T}g8$ExQy}V-aScMxM86n!sgT$^RpOhsz{G7#QN5e9O2k&w>@z`fkn7LQLbE#pu(MEf@bk$l4M+|r)+RK|RR5ovPc`fM*J>l}X$c75{oYd0D;}6%@nQ;Mkykpcl(O#AZE>QT;ry7#IT)F#PbHd!(IAcY1F1OvkTH!LcSBgBo{p$;}?>-NFv0fGFd-$5;BZccnH~lV_+dek`vfdNl>J((f2aK;2?qAo%igRu|$z_KZ#U1W;<?^Tz-#BDf443zLmX}{QErzddiskaQk>B{y)hI4kxpvf)ReYP#vvF;a$C-H<MhmN!`g6J1xY5SyV{RF11U)qJ_*jWuCJR>{xu46o?=&FG>w8Ka2GC<|C;Q*LW3;fxi=B4!q9ZSjWQ<xGSZxlM>pc%37GAe{G?z6SCXrGPS4suM5|X_f)ZSUNaFH98?dIY?R~PY;wUT;E2`-1d7*8zhRmOqK^K-|M&g7Bw_~c-_IWgD6XyGT_N7&7VcRJ(D&(EYIenYuDti)Ji;c*S~xa_fK5ShK^g{1ws^ZyxFySTt)VKj(*7mvh?O+&`Kk&gXrw&Hvp2NMhb7G|<yF|{jc?0iV-(Ecfx<2+g@>^9jpuGgg{kyjj+^51{P<pRs16!u@k=UaV78?Rm2Wy~I85P6(>+8|mu>8FuK9xr?6C=znb7!WW%fXB5yOb)Pc-P?{Lk4fv2;`lO=QtHYrcC-9(i^8UD#qH*m#TJOq`*oEXx*Rm}xazCJMhm<BJYVE-+ZkKL!?(^$6R+2i>}7|>9+HLMIQ=Nv%Z{YF<a6k<)UeWGE=P=9B3jrGRbAq->)lZ4<)E_o)t$k1^TrNC6wYUAW;d&g43c82l*b15rd)On2~xP&tbtrMo|!A1JW>Il%eVHs*k{{Xg-;cm`(3PAzfLN=y%OG<Z=MzVADyT0&QEKt7)z(6Ph&nwbM~F)a;*(#6fW8F6qn<dot37Q{Y^47KF#GkpEC;Y-+qS6zj|yE9o;98Mcs4p?92UemHldS&sIlBr58Ttc2BeA<6kEl*|<FYF3DGC0-3lcM`kr_+~MMLGBtQC!Sk#&X*vC6blFe3Qu&DJ{b-pO9x|2;8<UG!54Py{8P|w~%A}I(ORRH)y!+t9txL=|M(rW2XI`B3{NmTg<WQ+p5`EFyKQHbz5}9ZEbtPRV<jAbg&bOwDZD{=E^IXjH%+s@)4Q3=gC>|x=9h-v_D~97T=92Q0u`8_h!iyhUJC&R%93}qvJlD!U>-orUZOHy1E}~~<p3Lf54eO2dQ|*G2)MS{8nCy_ljSsHmB6-~#AYXr(V-l0PN+XvY6!DCHR(pBrv)WjP#%G#xWmeB>cs|+O2L%d?ZkMviny5UheX)L64}Nl@wB&LYc{jPAmCr8;^`tqUR}xdJY`krMYiYShGjh_cKQ}idUXqiGdC2b%%n<iADq?i1+l;(jlgIVO_6j?F-SqC`N;2LtPv+HOb6G#E2iEh)^jdiI{rd8W$l-*o$;NHz%hU7b!|JCEEQQ;BjWAcrXeJMtABwB4SxZhftANKXLFQ)HvgG1{I*HY=@j(s3<%(<95~rRexpCFAaCz>rRYb}zA*Z}+hKrwCMY8=WVqPy*W-&bG!hG}TbB$%TFE4lTnowLf|722aT?Nd`W&Jc<5-!iA`l9Wuz47Am);4m`_~FFAPceD!f)L!Ca{IBBG3$r*AT)X=rS`5M8=BXWSwCzptG~0L4bJXAL|i(z7&mv>o)EdffFa_cUX`tUvff^lXe#e~p%RNuuV$s^`Dgp~3-5rRy;O+>(+c7PrPql~>(gsw-YdfT;psQ$MC0n^PKllN{3`KsZ{Ih_$4j3Q)2h|u`s}yUSDxB2mz0^H=IVKUFZPJRPdn!l;oSo(4}+F=#C3yYB7`CAS34T7?b3<VFZ)vB<vtESZ;sfnmLtxWvzh}N=lK-c2guHyJCWzVddY>O1LfsSW%8(yyVbr}4eN*Xa4+|`6j8-rj`~<!X8p4sSPdIz`?4CIH(oE++jz0E7}0BhJW}H>J&Mi34ts}_m1R4dbEe0cC!caR|N1^dW;Ja5WTk%c#@)loBvqPKof1vrq=+1Esq=~q++%NFdC;99B+M;KvPI8&@HJ=Q?YD-Is;=$Ly!Zn-3m0u2L$=R|FwaiwXg*wimD#0cFPZhpi?iN}6zV5qS|{Rjrj<|Dn`_U$a{JpY$>eJTC0;J8=lLwwjlSlgbuOI`GvA5ri+4N^7c<`v<Z9~ltZ(l1v4s4|HOy)+yg2KV^%fG_UvBgwTr561Oky=`eAVD=x!O)Av4VGilrJz7A2B(JG0R6=`DDG}56QUwB_i&+x!TOr_kmL6#V-Tooi!?3?S&WT`3dyTkqcfVqG$1kA}`)Z%$1L)q>#yde-evlCS#}M6f$Y#Ca%wW)4V0OdUfR7N&%RsKd`S4ZcYNps9DR*1wN(W4P6(K9-F6G?Tf9$##0_<%k^RwlAPokRz9Dt%8^}YO`#f+SkJsT>y7op_GP`DZ&1N}YD%E|u|^G<)v$5a8!yiK;mv`~?a?Gby5GF79DMDAxVqP8Y1W}*<XFSb^3{k)IV@$6`NjE%W>(Wa;*R;<fn#LQmKe;_jLW!Xu08ND+2a?BSv{|p(B+Htl<J@F?j*DEfx|vaN#j<K8=I^(BagO`?~Gk#_P=}E%zEJUO)h@dJaP02qWu(udAWshu9?q%nn5}_bjNHRHkapTVNn5Z{XB!@Tia2dxca*EZu&&A;Hfw(|E%VKzn82l?<QZ!*<oh=upZdH`Uyy`LTjEV)(P8^%j%~rDj*+jsu#bW>VR)#pOFqX){EPm60Cf(-a_xMkz%9wiJ{w*Wu6{RJSAOr=g7txd4%=D#(5r&Pbn{dj@l=lx)f@)7oH|0qN40lzXuVsLh<entEAny2buOUh3k{2>FT~-x>z=XIC!SWwI=MAnqN6cJnr?9%cfVrJ@**ph@iz1>z^0z_OiHKp62d-7><jzDKA6C2(qnE7}qna;qAp1Z<|KD$vb@O$p=*%%xs+X!)kawSq-l*tJ!j_p_DnhzZ|h-GPwt<&Ch>cOpf<Xk#m0SDPQ#pHRpf7USc&DKkk(JonK5&C-=s-Xil1Csa559Wc`>#%xW4mUuG`uJdYf0(MM+cvhjL*R+w8Y9z-^|TWenTijc4Tc){#>eUZd^VEe9EN~Ci%_l42g1231SAC|UXy1grgRQcEo|Mq2}dAuoxge9eNeX<%hp6|jw^U^UL#c0<=xm<=$z7$$Z&UrpUV*Siqu}F#>-BHYnNVW3Mdf?@r4VfwRtzKO0QXw6)b$I?+KgH^vFo)MDE|!Y!DPJo1oNWA@BkRs+MV@Bphx_KL%cqDn`^8x8<*j2sY2T_T;@%B?G0zWMpUur*H&wbEp(a~%`e9xjo`;gU$L1!HYU1e<BNtp+6(9X5$$~!F%=UVryKG+8a~ApWP<N}`&aMy4V~5ouv!7Yl;rVG$I7<p2QHvZX-wy}w87<XJoJCfy%)q?9Y#lb2*O#rsdiH9rmg~3hl!Jd7D)IWV8lF#9!`5g0u$tOa3y5{+q|3ufO*cPyeT6LAH^tm#LK-fxC|h>>;Vw~!l{2%N%JXxu@3gyQ%%-^_tLJH=cjVv(+isByZa;{u=F_-rdGGdHWJ&)DX1161#sw1l<2tjiOEPBb^Yk;C4v_EnFp;N*(%inkmCeOBdYVYNl}kikeV+d8!dxtTTuJt4XN#-{{myJT^7BeE?nq5559z8^<ks1`@~cTk%=Y5xd;gd#4_Q82tUh5lxn6hx9!<IMjOr541FwGh`q|h=6CjRUD@kk}Hkb9l_H`YfCs*|j5GQu7K%VT1F?G$KD~GiBY}M<)hFtl6G7(2Na~FBJkKSeAj(vzY@5nHT=Z9CH%}t8V#NB3gCa!p-RUOuYOP4%(CDqIs<SVis@XaY=>WPN($eZ-FaoMS2Im!W)*}iO@SzB`DzS<LH$lb94Y)${fJh|S64#eHFj>y*G`TV>n6PH`xf#eJtE=85-htK+)AhE6Dt@g{)^ZK%T$y&9RRLH9(7mTitS<k%vvL4u6o=;Z8>&1E-a8!j?eU3A?`C1R_wz->cxM#_mzt%KQU+XIeH`_*zT~J{MM-}!A*+v%hHOM@D^={tyUd@eUPGx_Y)w3F2{aNk&<e@Y-Q(F%&U0xFh9X(~9`Oposy;%LpnFjf)b`tST=I640-p;FsOX((&H(mW?-d-*q^2Bp>1IbUmMwyq(>$@#IK=#rMBz<Rl;W=9h;77OW$TwXISoxXe>m@h1pDMn&6=3DxmR!~w>nF-N0B^aIDi$p6EwdUn-lGJ@4Kx+SjxHYZy(V>Jq^&5%pTt&vSPx5&Y!aUp&6S_M+bFVrCZ#&d<JQg*eb)zLUL9U8&rhx2g7AhlbHsA(t8nA5#Spx%i$AG6%vqi{zp^}r@}8$5TtBP_-Q*|ceFFmJl4E~0^Kv(Bbe8x0rXgirLvX>NuJW#`%Sq<OMpkvId}xUC(RiJ1HLSc<ND0P2f7Xz|>DE5kzB~=<hxJh7N&zgcsUu$&3t+Ym>y6d0-dH_P!}?)0yg3vFM-Y^IWjlfclm-O(p&aCcLQoYdLt!WmRiG5OgBw(U+TaAvPz}7GCip-Ns0)5j3+jOyM9@Gm)CYfP3Oc~h2wFfh2#3ZH0v(_YG=NA5gQ8H7c54N#X*UNbOS=_-icp^RDn`2%0f3UUR~g!^5_m!#aDfs~o%Zsj-8{eu2Ji+~P|;p`+ARQ@Ll8)yg@&|OTiUG&ghD$Agq9Ei-JlD^!)n+FE1)YRKqrWSWQc}1=n0w78?vAWq{2W*feh#m!ypGnK|dG*lOPX9z!;bY<6s7igekBPCcqCc2bRNpSOs%oF>HXfFbg)rGTJ4I_E`<<XrHc-MEk@-8uWqg&>4EsF1fT%It+zD&=(RRn|2vb`wWJuFcF5s02ocX%%goK!xC5k(_t*krd`(1K8s)}tcRJf5;lPuw!x2(9~DL=&~`WoTY<na*a0#ehh4A-_Q7d51Q+1|`~+9wD4d1!a2qbbBX|He;4xf-U*Imhf`{+{?!z<q4W7UYcmo1@4Fym>^cjkvLg*b7Lk`FcJ88H4s37gO9S+lOCO8R4Xs=VW+iutbdugxBwA%@|4p-m|?1!IeuS>MsO?V2w!Yw!l_h_$AwA*t)=qtR0JMb1>!$;cf3jivL-h(45j+{_QR1rm^c+>@zL)B1eQ~|l7vZyk0K_18rsZdo^8);AtR2O-p0OW(}qk6~}H9%VAheXs21)^36qo$}GYJ`GOD2hZaQCHL%wL#rb6beIes3YxChW3d@v9wP)RFn28k7}Xns1hoLoM{&w?c<L0NR8^CD#(j=X-xYVP!rS;`6Evx(JrlNpCA;0+M^I;M9pcJaN4IW>VRTU3)Bg9M@gs$>VtM58Er+qQ9slZC8I2qh*D8H8jJ>@k*F`qMWa!FGzbkvlh9Z+1C2lv&}=jcO+nMqLNo_0MN`pyv>MGsi_uE78LdM<q9tf8+J&~E708S>(JsAcpB>0V`}9URv`-4kL)j<|C7?{&WgP7@5KTm5&=8b?hS4r_X`k_E0h)y-qv2>8?XsTsnTIx@RcI0V0WGIpw$naq&_=WqEkj!nK}XO&v>O!{oP_ei0dxZGL5I+3v>zQsC($Kz4qZdX(FJr1okf??b@UKjMQ_j(bRWG!zo5tHIr@ZNqc7-J^cLk4UZ9T%2}Oj@sH9L#C?J#*N(+KeQ79@LK?iA{;zAkP=K%Vd_Bo8sqci9j+KYaoUGCC87tsTB8(l%C&<)z<4()Rfy+<$6BXkozqg@ILU(h>LNN^NBpr`07`VBb<rG)%KVWF%5LJ6UQP(!FHR2CA1WTCs@BGeKp3DpH}p^8vb@DO~2x`MCZE@%Wv@Dg-_ztC6+5Sj{lAy8;8V4<N9EVLDx3GIX?LMx$*&_ZY}bP!^N_ChZqUg#|J7J3SiLW&SaySUOm2|^<6<090feX0p+!BcP(oQ2x7i;?zG3H1e0&<b?~KiVaf_Guur6vBi?f<XwOT{_V|;X;fMCA1NOgb3Otn)c}`bQ6+<jzSNikHEVx-roDo?Y+O--g~Hd_c-(JHMaMDUVHDKwfBBid+!P5-LuKNuh8E6_3XVr&fa^_c=w3$?$xsQekgnIKeG3JAA9eq;obAXyZ6N2`#bEtpTgez7wo-9fcF`G-e>9U{k*!ppAWb9^Vs%&&YAbwW8P<g?fsmsy`O8f_j9E7epZwBS;|6_Qsj5dR!Bvw?-5xxk(P4C*3x*;@Z~nex7>CxFTI$9PersgvKn5zL`ooDG~ONmBF-kP#+EqCW$TraJIOIpSiWYM<;VGp$(19PNIQHR+Z2D@@rk+g{7Sg-+nQDyUOf2b7()DW@rJ4UL{`I#?^}CWs&c{$n{HK*S&c1mmQ$WYO6?NXO7kc6#4MNe#uC0>3j5s*wJHAI`L(g;(Hy*JuOP7+TjD~X+Pv~=P2B&UDD&bxc3&HTpL>ju-a0>&SWbA+8u$Bky%h8QmQ8VePF=jXmpd-AY@3ya7k}ftUCdgQi=R0(7Fmrg@xY$W^4zfo9GkV=%!~8*Xj)I4c)G3RI)A+t*PPP<5AA+MYSmzoP4UeSwfIE6I(YEO;Z_=6y!C;-qG4?=PCrwMuo_$9`yFe@gEt3Y!9QK%#d&Ocd|7nV&5}M&PL)}1d;YxWb>~Ov;>X@L#nllj#4kE;JR#2CO2dnL?5k~j_aGOanYD|s8e8J|C(j^#<1wE9q&DWod7RQtCAS)rBAuO7PiA@KTQ~Vdp`WEf*v+Q+?B4n1h7aoE8|NLZG`#rOVdKc^L%F!YgRz9w@Zvj~y^=0G7IC)WrNnA%iL(sg2oB26brT>z6oVpA7)n5Kp#Nm2E0*_!3eb2#x>6X5(iO{lHI|>ARvt=21*ojNJ5&`aK{ap%7rI)Gu9sEb;i&*s=(;mhr|Z?A23@ZSwUnQ#Ru|mC6THC#>VXzCG+u|U)CMoQ;t49cVtIc_3p(XpAOi$|9*ls&AL>H`kf1R%frfO|kFFa)r0Yfqr0eyek@8dFn$q<kXb#OF6k0$Cw1n0W2I0^F+9~gOMbgz^x*iIx=z2?NOV`7p4P9>!5p=yXbcIe31u@VCx<LZOLl5W)-Jv%mK`*)*P1mC!j;?ouSi0T=66tzxNT%z3APrI=6|$f&^n+~3gaMET{UH~Iz+k$XLDy3uov!zT9J)RL2GR9g7)aN<Cnu1A*DowTFV)23`#r)*XX9JrTjw~Ncw_VGBy`UQW97qHHu2J$1xTUEACzA9GLc-!*`PPZueoK2Ej&HE1xeZe!Z@u>ahq6PHj9i8E{zLcsPV6`L$8TsLqci%@SMYUaebE@a(Z-W{PwQnckzM_@nrdwZ{BR-NmsH-URr59{-=iD#k#{2NMv|vyy<x0ck$wqcSvNhVfe)HP%bB(yGoKO4a0fFU^j1le~R?>7=~*v^|guP9gmW-s&9Sm<%)r)iBMx0?t3xHZk}1?8u?m!7(V|o+HQ`%Swp-%=7X_LrxJGaM-(8AF@H4f&e?CWg;kXjMdQ4;#=B=u+Qc5^hKS|gzfgMd*!^vi7<%Zr@m8wQCT@OL6!YDGZCoGZYZL2#%n-E|-b<EaWD7%$VdAV3@1-A)d43mbzDyUBkG_*OT=o7gzIAS)m_F>C;_cty#>0OQ>yCdXh3rrKE*`RGnAqs-J1KWh&+p<z*Y}Bc5~A^hy%~1%Rkvf}oi5RM+vaGSxHq~Wde@J}@w20B;_;8Ji34hW>&4?sOU{b}RMGg>y`eU7_MxMqszo#|-fx&qymGLM_;gF2yrlds<HC~d<d82KQu}ogIre^x9DR0@$vgi;iPhX4dse(Sro7lHJr^IC(q6t$OftPHSQzv4#cITgv3HA#NojeQ&F%Z3Ee<@{R@@3jF{|IYIt<U;)=K<1(8)^U+NeGLrRoNwN1wuS%%T{a+4L7<$8!(OY%Uw`pBY6e%-L_6H#$!?#+)N<#$PeLAD%0-dNyA4QJB0xv>s{G-brTXa3dp3&W)W(v~EuF_UmEto^~PRT_Y#V>U&meD}Pupi!{kAYLzRa_VTURw&Ze)!rWQ0^Eux+PJEdC$r#YzdRF6w#$>wNUgM61d6-v|SEowlF#IuSow%{F6J}={ccu-F9kyPKm{Qbg&OH5?3GHx|8-v9H>k7;4v51@=hU=Hj7C&}zl6e~5aT&FqKKJBXY)YSyCtthWR2;g!m1*>vJej9qj~9Df*kf_|^Gfofcph$%yUxTOFZLL*^JMkEs#cNilwagn=dv?rXUoozSCgG5J1aJqog16W&V<cnXTtN(=JGV`4B7eY*i?mVTuqNd-2&p>b}i(Dk;9A|D>%u8LfgrQqZb;J>0|ry$9D3xv?#G`aA90{M2t)h#fc5>Kak@0W{68w6~(U|^YD|hm&A|sF?l>b7qc~4J*&AD)B@kUb!gWKgA;aX-44$Tu3~EYsfblB8?TfRgP%0klehG7#cJFiw8QJGs>s*Xg=L;*WrK_4-Q_K&PJ?o-_Itd2A}QVHr0HEwp3G|4y}w)<CfC`MC?1Y-lG*u8OlT+XZm?Bs3WYH{pVJ{};-s{j#-;S!WaqP@XqbE=b&ELD*9r4-*;(=GurnM(!tgfl0HPi4WHry}k!td_K@oAzoILzX%P>4>>I~94lAg01y=HD(oIbY^89%nD)v*}Yw;hg(nMqD$7M6K){?yYb`c>ax%A_;p>1*6bAeqkTrsL!CWZukq8s7Y~)7r|9JTk@WIYq6GSJ9En#r`Go@M)UQ&YZ2o=Ca3vojF^FohMt9)v&W==gH=>diJ=mdUl>XJv(Qfo}DMV-vZzOp!^*BK*$eOL4ZQw3i*_uUvK$zjt1&MY302U%g@>mfQrxnM5qBx0D}jFKx0rtGw=ojv;ZAcfVSXI>y?E9^lwQhqI@p`t-%QO>3>b3CH)&pzdAxqaDjs04%MJ2ctIWI{T|ED^)Cm0P#zFCLltm?hEN@9K_jRQo)82o2!mkILpU^t${;~I<$aU(umo1XOo)WOkP4lkKcqu641yf!0mC5<dc#=g2@x<Ek{}a)fIg4~GawBH!d&GYlclf_M!<4d43l6wtfKXL(Yn1L0lF*SyVL4ZX#JTmhjy9+3+UI5&=vYYXNZDq<(-)!5D%kZ7$m}Y7y}(31tvlU%!a9u3-e(X42DH84~D`>Sf+d`XC+L4WS9mM_P!xYQgW1k_u0!|Ti;i>ZB$vC_|x3O3a6g0#N|~%+yAI<FJIbwP~nj?2HV69)9)(Wb5|~x<puf8zqT5w)VGBnZGBEGd~o}H)A#TbM_J+XKCk{2-g|Tb`HyE?xJevQIPmo3?_$5w&lG;;IPqWMo4aq2VUH&%p6%s5_bw}(lZb8NeecdFJbt6Z<z;P7{!!mv?(Kb6;SC;<Hu1|UR}^mfE1!#dZ4!U!-$wcOoxMD7_HKpCw-asRMXhcq>~p*!mtQY?_D6ktdB5i`3MZ8L!6uH(-mCERi&MB<b=@qn?7DcRzAe1juub8bXPm!_H#~fxu-8P_e}#Kbc98z#*%od;`jL|B8oK<uIQH6hh0hIK@~<%QJ}d_P(qHjxFJCQqLSfvkhfRF>-8qF@E|2H(yIGh1sBbT;_I#`3H*t_ny!!NUg$uplGy6Ng>aA%muiyNMtgBg0UYf71?9%2oiF7U^o7c6KH|`V6qiPhwpSE|CpHx0gKD@YZ^*hBPEA<jTlsZM4)z8KAkDL=bOAm<ndH`2%rFq^42R^<<s)|Ldeg|3j@aDMipijiJV>v5L+5T;D)d_-mTE9Z_Ph-2`8S74wyd@8;exDi}4|x+yT3!2zOlp!VFZy(jI9z%_y1W=*^*h?wIJ@_%!-Hk*@g!-nduf@S&&49G<oTQXN;f?6V|G3+$Ku4c;}WHimHjX~llUn?a?ObYr3HgaVO}mfD_$LTZd1Dk<Ekf;q=g+zV|G@WZY^<QV!R}ME@(BkaSwb+<c>(`_Sr0M?#hcTam6itrB?m(%j}%*j}O9bJqJpLNu^|-hMoDgWnIaNv_vUkLqD0Fe{MfX+`KSSYIG_~=4set!JGf>jF$46;qg-5m4a5si~W6G?9ACZY%Y5&*j#r0?A+Lzte%}Yt7kRr4B7d!x$JD&Ty}139d?F1J-grkJ>UQLeE;9`{r{iyy%0Fk)#lI&0>J^QL1oAfHJ}O<huTmCN+`bpung!y3jzc{d8i8Yp%S=418{~~&<vVDJqQI)&_PSkfInbpP3x6|LiBGb<@XSlqhDJopE?PI#<Wvo<?|-_pdeINe%qj%@?MQQl!VfthO*!UzJQ=2_<;*F0ukyczhSVZ@@|bcw18mnfp7=|15^MBIzt4sfrYRXra^m1hh*hlls?c620&McQSL2@htV(s+Q9_q1!*u<c^73mq(HXv&c+Z}00UtZEP>%L9;U!@S}%dtO@KIvQocvg>Jw@GX)u#^vb>A35IR67$bgQ}1^Pj>@~M?r=nlh_Prr<Tw$K~KK`P9ENst4x;RncqT$l%gVKK~A-a}agV<8bH!~X$Hsx7t'}
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


DOCK='harbor-dock-module-01';STEPS='village-low-entry-steps-01';REED='nature-reed-sedge-01'
GROUND=.08;BANK_TOP=.53;WATER_TOP=.30;DECK_TOP=.83
placements=[('whole_pier',DOCK,(.85,0,GROUND)),('whole_low_steps',STEPS,(-.45,0,BANK_TOP)),('whole_reed_sedge',REED,(-1.35,.98,BANK_TOP))]
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[add(p,t)for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values())))
base_mat=len(PALETTE);PALETTE.extend([('SceneOnly_PoolBed',(.27,.25,.19,1),.98,0),('SceneOnly_DryBank',(.34,.33,.23,1),.95,0),('SceneOnly_OpaqueShallowWater',(.075,.20,.23,1),.30,0)])
def box_mesh(name,lo,hi,mat,role):
 v=[(x,y,z)for z in[lo[2],hi[2]]for y in[lo[1],hi[1]]for x in[lo[0],hi[0]]];f=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];emit(name,v,f,mat,role)
box_mesh('SceneOnly_ContinuousBed',(-2.1,-1.6,0),(2.1,1.6,GROUND),base_mat,'One scene-only continuous bed and ground datum')
box_mesh('SceneOnly_RaisedDryBank',(-2.1,-1.6,GROUND),(-.15,1.6,BANK_TOP),base_mat+1,'Whole raised bank supports the entire original low stair and reed base; not a new modular library asset')
# A plain rectilinear water volume filled to the pool bed with four conservative pile-envelope holes.
# No invisible mesh cutting or deletion from the old pier; no fluid or depth rendering.
PILE_HOLES=[(x-.135,x+.135,y-.135,y+.135)for x in[.13,1.57]for y in[-.72,.72]]
xs=sorted(set([-.15,2.1]+[x for h in PILE_HOLES for x in h[:2]]));ys=sorted(set([-1.6,1.6]+[y for h in PILE_HOLES for y in h[2:]]));cells=set()
for i in range(len(xs)-1):
 for j in range(len(ys)-1):
  x=(xs[i]+xs[i+1])/2;y=(ys[j]+ys[j+1])/2
  if not any(a<x<b and c<y<d for a,b,c,d in PILE_HOLES):cells.add((i,j))
wv=[];wf=[];wi={}
def water_face(points):
 f=[]
 for p in points:
  if p not in wi:wi[p]=len(wv);wv.append(p)
  f.append(wi[p])
 wf.append(tuple(f))
z0=GROUND;z1=WATER_TOP
for i,j in sorted(cells):
 x0,x1=xs[i:i+2];y0,y1=ys[j:j+2]
 water_face([(x0,y0,z0),(x0,y1,z0),(x1,y1,z0),(x1,y0,z0)]);water_face([(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)])
 if(i-1,j)not in cells:water_face([(x0,y0,z0),(x0,y0,z1),(x0,y1,z1),(x0,y1,z0)])
 if(i+1,j)not in cells:water_face([(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)])
 if(i,j-1)not in cells:water_face([(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)])
 if(i,j+1)not in cells:water_face([(x0,y1,z0),(x0,y1,z1),(x1,y1,z1),(x1,y1,z0)])
emit('SceneOnly_OpaqueWaterWithPileClearances',wv,wf,base_mat+2,'One bed-filled opaque water volume with four conservative real open pile cutouts; not a new model or fluid simulation')
FEET=['SceneOnly_ContinuousBed']
def layout_bounds(v):return[[min(p[i]for p in v),max(p[i]for p in v)]for i in range(3)]
def layout_validate(vertices):
 assert set(vertices)==set(G)
 bb={instance:layout_bounds([p for n,g in G.items()if g.get('instance_id')==instance for p in vertices[n]])for instance,_,_ in placements}
 dock=bb['whole_pier'];stair=bb['whole_low_steps'];reed=bb['whole_reed_sedge'];tol=2e-7
 assert abs(dock[2][0]-GROUND)<tol and abs(dock[2][1]-DECK_TOP)<tol
 assert abs(stair[2][0]-BANK_TOP)<tol and abs(stair[2][1]-DECK_TOP)<tol and abs(stair[0][1]-dock[0][0])<tol
 assert stair[0][0]>=-2.1 and stair[0][1]<=-.15+tol and stair[1][0]>=-1.6 and stair[1][1]<=1.6
 assert abs(reed[2][0]-BANK_TOP)<tol and reed[0][0]>-2.1 and reed[0][1]<stair[0][0]and reed[1][0]>.35 and reed[1][1]<1.6
 assert all(-2.1-tol<=b[0][0]<b[0][1]<=2.1+tol and -1.6-tol<=b[1][0]<b[1][1]<=1.6+tol for b in bb.values())
 # Four whole original piling soles on the bed; each complete low-column vertex stays inside its clearance.
 low=[p for n,g in G.items()if g.get('instance_id')=='whole_pier'for p in vertices[n]if p[2]<WATER_TOP+.02]
 assert low and all(any(a<p[0]<b and c<p[1]<d for a,b,c,d in PILE_HOLES)for p in low)
 assert WATER_TOP<BANK_TOP<DECK_TOP
 return dict(instance_bounds_m=bb,all_three_whole_instances_retained=True,whole_step_base_on_bank=True,upper_step_and_original_deck_top_same_height=True,step_end_meets_deck_edge_without_rescaling=True,reed_clear_of_approach_and_steps=True,four_complete_pile_soles_on_bed=True,conservative_pile_water_clearances=PILE_HOLES,levels_m=dict(bed=GROUND,water=WATER_TOP,bank=BANK_TOP,deck=DECK_TOP),scope='Light literal full-bounds/level/pile-envelope checks only. No human traversability, access, structural/load, physics or full-domain proof claim.')
LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate(vertices);result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,.65);ORTHO=5.30;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(4,-6,4.8),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
root=bpy.data.objects.new('OneSteppedWetlandLanding',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole scene horizontal centre; continuous bed bottom at Z0; three entire unit-scale legacy instances';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
  files[role]={'path':f'assets/wetland/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'scenes','assetKind':'scene','theme':'wetland','style':'warm-handcrafted-village','title':TITLE,'description':DESCRIPTION,
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
