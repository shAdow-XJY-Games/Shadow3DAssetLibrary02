"""Static snow-camp pack on original curled sled beside an intact tent: three whole originals, zero new models."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='winter-whole-loaded-toboggan-and-tent-supply-station-scene-01';VERSION='1.0.0';TITLE='Whole Loaded Toboggan and Tent Supply Station'
DESCRIPTION='One static snow-camp supply-staging scene, one scene and zero new independent models. A complete original rolltop backpack rests on the actual middle reinforcing batten of a complete original curled-deck toboggan, beside one entire qualified open domed tent. The full sled nose, both side cords and all three battens remain intact; the whole pack retains its pockets, buckles, shoulder loops and carry handle. The pack is neither fitted to the tent nor attached to the sled. The tent retains every shell, floor, threshold and crossed pole. All three originals remain at unchanged unit scale with all oriented triangles and constant opaque per-face PBR; only whole translations are applied, original hierarchy explicitly baked and normals recomputed. A common pale floor is scene-only. Unlike the parked powered snowmobile and separate tent or skis/boots around a bench, this groups an actually supported pack on a small sliding carrier beside an independent shelter entry, leaving the curled nose and entrance foreground visible. Static illustrative arrangement only, no transport, tie-down, snow interaction, loading capacity, pack restraint, camping readiness, weather protection, human fit, access compliance or safety capability. Rigging animation and interaction not made.'
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
LOCK={'camping-cross-pole-domed-tent-01': {'bytes': 37340, 'sha256': '919ceb5b8ed80552e3f22527d2a32c1a347995f88f6faaddbfcc5fcdc4b06c3d'}, 'winter-fixed-curled-deck-toboggan-01': {'bytes': 39792, 'sha256': '8842df8c17b70d2ddb0488cc8158d0ea32ea883b9c47b7eaf3203309971f20b8'}, 'camping-backpack-01': {'bytes': 71204, 'sha256': '4d72eb96a680ad832eff4cc7d2d6c3ae892fc14733c11303562c9c3196edc140'}}
ENCODED={'camping-cross-pole-domed-tent-01': 'c-qCC2Y3|K`v1Q}6#)^ECJG_+7IxEi17r@p_ufNDHY5;|m_qMJk=_+hl&Yels3=#>42m7piyg1mcKcPY<tn!8_4l34Y&g5j*-ZTZ{?E_nnUCMR^UizDob#SDyK`oTS-E5TR{`+BcHr{{z~C_>hA)myFDeQY$97vBJ1dYEC`>QTFO2OLJ0!a>KQF&1W)=^L>75(M%M2984C*=}W?o`kLR_LRwsY*fKw(i%ejc6U<2<oTJI5AfFhFcKkFAPgyG>afo0mS9w%9SjeVt?T@-u@w5~eMkcKNTxv4I7}h3Q3BEi&@w7Ubsz@`}?6^K-33N8|-!EMsn<xJ=}i<YjirC@Gv5$czc(W#r};<>bwZnVVi5D9lOEjVa0w<mPsc$;!>oFN{gg%Zw>5ED6xDxNu=iVW7CAFs~@is_xuCQFgGlb`>XNv%Efb{C>f>C53@rd71sKNIas#TJq1FLaUDae_ly`Nm0y9nqo3@(r4x8v1SEy?H&_Yke*Q-Gv6vLCMzc|hi6q#n4guC8|WO9QBuq(nMJ{R7X{Lb<*ItatJ*)Ou&B7N9lJLR8fn$!|Gt{>;nf_So>LUa>{FOOKhLqU8QD3xnS}x7(G*W-Z|8WX#pU`3b2BX`lfg35=N7P^yJQsR7Zr7}>ewYSe{LYNOEIH$@pzeBS<Knuv`n5{MsZnYc9}$TQE_^4PDa|ioT8HS+_e0>+=a2-teof^n_rkSD<>~4GrhQEF1_uB$;m4Y%qnC<l%-IKmHS0GnSq$};+V;v?lIXsY!OSM$4o0%iefUX><VPEtis?(NweCvknP8yi>Jn>XQmev=gbRCjqMhbm7ZI~7MxnvHAOk>f?1CC{KB;0@Ce_zFe5iml$IID%V(>G?F!`aRD!0dv3(}>8QO2m)L6@2lx_{3U>I+_-?9{E7Y5QZgO)_;@3grruI%{!gC_RtTXy)ooWT6F-1LP!DXG*c!D6Q^wR+v|Y-ZM&U_<w@I>_qYzE<~)Wz)o3V?8uJ%f@?Ve#y+-z!<h_W~ejlIDOLd=A{><jVj3r6pzSY)!3>9GYf|W*xtE08Kd({W@U4738u%)^dgSf-2B4+Y-?-Yn&OE|@}^k-`8_G|$w}S>UuRETg4YxLFFwJa==CT0Y4W5bmbv*oz7&to+u3VX(JmttjdMd`sJL=loIgnp=1W;>WwH8v2IX;9wNGk7dg0um?4`U)o>Ovsu(Byh@d@7Kcz+^KASt=b#J_xriSfxaCE916?Dr?9`260a%AAxhyo3r)s&{&Ec5%tf;LMoTHxMWo8%WQs<VkrF${Nz+O-%84y~$plg4b&|uE(FudL;RRwz8`E61+b4RZ2=_PAkDa)aOe`NlH$r;Iyo)ElL|um|l?0`L43(lay#z)Z<O@CHs6<pLmkXjJ{-VlHZ#cZ=EF5Eoe(l@pzJw*niF^6qjH(k2fWr$?Q)_c09$z@I>~o>!y`W#o<@r3NCLv*TS5+Io32)c366GabeEPlHx${gh!4TGidCf5yOKGJ$%IIVZDa(g2d6Elb4y3Vfn;g9^!Pe+F2DL;c|pTIYN>g!5b|?^5qCVIf7q~5WjSq6{F%yrt4Erkxtzsm+SS)1t(ltaI}k{>*BrfQuzsC<tIj#&lE_{;J%{#!m^+<OR};8h2uG!2fMKRgTdH^1*~O~moo^BC7i6gdHo(M+yWlQc`+_Nu`CZ$k`j`Ai3#yEdCMlBB%jBhn9LNm5-!KOf_DiHVo&(Ej_=&X@sQ$R(Xr$E^+^bR5|FFtby3A=$HzMzpHO~$Vp2-^@nib*8rp006%i7m*B~J=G1N$&xRkQ#)0dR&_a=A}Q><2t_gig{nCOp>Pfm$X3AUO)$?Hk+^1|Ww`+S!h%^`qwg`z2*^LPrU2~K>zU@In-&C~G-K2I_yj|y5b(ZxALJ3c9TEBZW16}4h=1^t-hznp4T=9Eol$-a0muWCt&73JD*$Sj|W8bv$aAH7Wy5<C^PNlNq@Fmt5LiuZ5;`F-BxL|)dt!SU!z4qhVT{WSO!l4<fVYk2AOCnS0ODgOAd%!&-47@t>$h&ntyF3urp0B`hWO!g#K)QsNv3hLmA-i`_0c&il>lH(InlH(KqPnt2o#VJG$kQlugll=ZGnvr$7974W01TPFT7ZwMG^1DQ_^-a#3Y+FWTWd&~%Sh<~EI4cmGJlJZN>*M0!GK<^eQ@sB0!+Gh6I6NWB;fdClov`DRcp-CN{FTS2BqaOYAMZ`{Mx4IaI>h}6c!MAK!U8bSDpP|i10?%BiS7d=M|Pms@AFim3*vnVkriMYRwjk62oTRt!pW6rf_Q6^2n&$t=O-BVr;r%ghVjXs#7eZGLjZqLW%AJL^+g2Wx7ma%@~C`J+XGsPkPy#S;77ukn75V!y$21)>E`{+SI?hM-TLfqA!}eoP@nxSJ519@Nd7|d7m~k|Hf1dx8>vkvE!81Rf3>EAnU&R6bU3#{xY3u|PYvpY69>A|%RlUEre6JS>T}z7N7JGr%{mCFJ{4-7pYBG7;`d(rO1WLume1Aiwi0JLuME>4e_gY@O=NxWLRWL?fEwc9&NX40F%2nxxz6s_s=OT--;l~OLUy*NklMB~+H|9(c5|!E%4jJcT<PQ<rN+&v8$|Wz>j^h{>$Belb<ZOo>29>uk89T4BKqClOvsusbt!&@`qN3H9Q98xCqCt*uYUKizUH%0;`2RYMcrY4VgJq-Tax0!bcd<+bV--nd8`pSmgk~N=T#YPxY5!%nl80b87=jN;YRn}_<8B*(+5QV#}jmw-nX}@Vd;BcsIAoWPnC{!)b!V-V=K~zN=q@L>C%d{RDY$ma`@+a>**6yc8NLnyr4IIrlWYV;ZjQ*A#KekA)oJd4K{n7KBb@f-O4bnjnjm$;H*BT`o=JQ*VX6sZ#K3OCqG*uF3gQF^G-GsqcT>BrC-!HFQxohPusO#4D0ck@!smCdUotKk@DpTans}@`kHT7gz3fC=ka=WMh7oI*^iD6>N)%7^LliqwWUAkztN=K4B6>#miez}eRkTl=G3h-#a}mi#j;I5>fa0)Ab#AFCcf~U(nq~CSu~kDMCh3v^iLKo5eIj-7o|V7Gm5fTiVauAinDFsH9AZkA#Uw4K{W4n!I&~VUW`vJ5x4%cu4vIAOT70+7tvx(Cvl`;8tZg-n;qvG2lbNlc&q#)mVV&DfhO%{$WDK=%zxX_y-#g1K3TL&c%HgPZ}(8G)cW<ei|da5QKwxG*-s2O7}QpL$!-86k6L=qBTpMr9E1Kwng7E_ftbTqU$Y%zZyKItrrdE%Kb8?A(nlqkiF=Rfr88oLY%gfEz?^eniPg@aT}b{y@)wf7aPT)}yY*kMm>s%ra)~MXMA$=h2-9+XB!6M)x2yU^#~;07TFfQm$nd_R^x2ELd@d?`%$ve|V{M0E3{`wpTSfRdwojCL>Qa5mkB#&n(s_rTJ2Cv&NFS&8(c)C(FQ2d5_)c1Nj%;%wwRw4NNdAVL8!CS}XQaBBsyI>n4avVe-&FQ!IU~2v-<Ic!-~W16Z<xQ*@cdXHo~<9y<vf(_FU|bOm^vv-*zHj6BbTMhpD5+(Qn?lSyR|!wHI<L7<@)e^b?JO{>3qxkTJkp({)X%?_o-BWLyjXK8^zy{{L6Ddwk!I}i0m)94Xy88_IZ`}yUH%dj}k{$#BpqAg^v;G6KV&Qe-s}>_HnXDo|kHFsc2qO&BM{=x{9=F4p&{*RM#wdPN?h{aidk^MU~sC{EW;)r+Gup4OI?A>)%igY=!ld(>7?hfx0QWkX_J#Y=DMjL+;;>=7_}(v_c2!_Si^nL>saVnvu=8e<wZKl5M$vC%0JaLPuOnUW?9TXa2PtaY1(EU%R<AA)CNMdf+9!+`otPkRHU7@z_Fcq3t##q9xf9H{y2OgzD7QP=l<&J$um&$z(EWk~L9_tVP>C=<t(%Tt!}m+GK6o_CugM*&SDtSECMDhqgP=7rn{es7uzxHRLt4-HCdrN>)W<vN8IT{b@UZ>v0`<9j1^|Fqj;SVdOCGxeKk)f^2~i<Ou$CH%4I`IS!M^N!UbgLOZfuaBpjR-OX(j4$@}=IRR72sq{U_Z5$5KGJqU_$>d~ABd2lyA#M|Jn3noveRLu_VLCaT`ww%Qj3cykCA(rXxtV*8aO;GlNXJ-mEJl(e5ktlxflT0@W5~ixawd|<B&3ijwB3W*2#^8zNFP$kRNC&v9LyqTp$FLmJ;|Q5-G`fzN9Lgy*$aKhKC~T2KQtm6VK_M)g=8UZ_hSeKk%Le|mS8?PpSB0E5JhAW29g6Yk(`L}<amrGM|1y!Sc=8uVvHfjAdO6;?F3e08MzEI$Qj5aGiiGWw_pXi0vTima>yLo9>yB1B3B`s%tkJmOWR4@ign~V%q8a{pUkK25for3ITQ=X1=v7tpzTqt#d>l*=8^MIOcrAixd=<hC0I@_$7*sleF4?IE7kof`JPkceI}=SPV&79Sx4NTaJ*Ncx^E%t?O!Z0H$MDQ>O1FVh3UMf`vkT1Jyq8CJ=Vv3&-b#E7EYSS3Mo#xW?4ciH%uQs{c`HbCtYbXnzmzxX{iojTB>t2ZC0eEwhGfy+g_oiI#;BHN_Q)oWIlFVYw_&O1C;uP8SR65%V*1!`iE(Kg7<nCf4?(Qn@-xw?ZBDVqTr)tuJk`Uv=_fsvz|h#bER}>oQCQg(ldTJS6(+aIy9EQY`whF+We)K8Hyw8Dz)Ow(NEMAJDyz~rg`qB)DDiCbu%iXL-)Dub}*!Ry3+EoA<Y~UQodEFOQ%f|Ek188-u}A3=|)S(y3*3I!i|>l#B`&j_IIVF@#RWOIqynKW89VIxtmfuRHRKedd$RcjBh_(FPdNYP<Nxh{PwA!9@h36QCV$`saGCZB@({5AxxkAb)5eCzt)SF>s}M4U&w!|QkrGyQn?lCT`OaIgpQSU=z9HFr;)C7=sG^`l@6}-L*qX-oHWnHkj|@8I`o;rE~`Qv`Yd6eONE*_piB8sp?>^_uXX%)z4)Z$kA@p99qUR<$Lemh)bFMnEw!yHE#<i@E#<8%Esa6Ljpn%<Qae;e8*a4k#YRT6u6K&#rL}dHZrbs)QcDl&>y4&UE7FXqOYtkxhDu8@qv_I$v~-S29lFk1pP56STSB@rYfTrn4L3Jmze|5RW2I96@nUT;t@{`H&BND*>HF55*Y7B7E%senrqtfnvF5i$H;Hf7tPmf*Ti@)l|4;hgtFH^w3(~(c>et_{x9PN5tV|vw0wt^T_H|b(^=c6i`<8sJ-+%o0;oILICq7KwswbXbY^wDA$2%T5J@#|`&a}0b-IRPBHRGFh{8p{Lz0ur$XoUE|r;9~Le$Y$4?<=Nmn<iHM_^5vR*;(TFo)od_d>37GUMyza(nh@G>u>zxTP50j)htZc$bZL}^5}4Jarqc=c;7q5^RFcc@9=!_!Ioy?z(b=%lcqhC`kBs6#e}VM#kg@t+k82@wHRD~kl1-wFH@z*jVn2Nc-~ym<z#|oHzglO&G@Dr|LD(0j~YuK+$v7SpVd|RgZzf6e?PHRH2wGcmR*;89Ce2i2lUO2c3StVR!DY3rLFr~-(9m)d@%h<Ln>FP8Q%!Sx7OgSF=GAS8VhY=zf5iSK-sux_w_M-QTI)v<+rcs=l<D7oO^A#IKAs}J@%a*;!>Av(PGUU{gXwR;-E)_X~sQlUDv+;wUcExB%gB4n1&S72*tF<np6iPR0r!BpU|DWX<y}-Pk-^c5ve15gybV6pDXSOTK`qw6Ju_kKES*(=H<AuPlR2B?6Q{2weQy&)_vI&>Kj)bGltEMF&`hAB;MY9%=kV##*}?jcKiNrP+vPK$&95>*D3Do=f@?P?YA8>8c$c-?R&<dI){A3ha-~A&yO54W~G&{$42#$?NWV0_qh$}K6*tyLh=zIA2)W^M@aQ?wA=U8qxO;PW8d30r8PZ6T3a@x^#rT_rpjOTk^3UT?&xo?Ef~2I%hwN0>;C$>CocG9pNjnL`|-iL#dNu3Orsuss_dS<)3GXlRsH4hsH(%Sr!Jf>j~_AaLUH8tQu~LOCD%VxmfN<K+NZqlT(xJ|JQMEk*q+LHDXb04?dzLeGA54dYtA<=8ggIA?Jti_$w$Ar<0Yfp(7tB9Gv#Z!rnGJx)n6W`vcIZ6s`&D_mdlcIDXc8nUutI|^^0|^9y&H6zN3#k4@8OYST{K)+eeq$M@a4CI9J%~W2W@%K%`GtOqIXA_GMaYTyIcs|Ea)y|A$ONRhFEer#X&7T8?vI-Aeu1O9kdD*945noOhZlBFEI<mgkzGHCQLRy)G9j%LtVv`>T8^TdsVKPT3n{{xHS)nl8t2y1vWDMw=6y>f@%Jqtro2br4Q<Q2EI7iQJyd6GO@q$8jq8>ym$H{XgjA#y@QAIQxgyM-^Wlk8)X3ZiJO3`%8VHOYN^q?XO3~cl43RW|a7jb(3RC<1{R$JWf^P+Fth#wU3j3SbUYgoMUoXvVY{5a`KPjW5_;EcDb(=K6<22sGU{*QG9gS$H^Xk?qS~xOeY=jy~FX^t@_+9f1Zr?St6uWpLyJTu26lplt1Uo-x1t=o_F*4T>e}we<oL56C>xqinKhhs(h56Nu<xK@;sybj3iz6Ri8b=uGi9M3^(IC@><|@t(50U`I;z?5!E~_&qb>FP@XsBc`tHKxI6}2jf-*}?Rr|#^{%qt-|J~UbSJxGDmfK`6ljQRH0z0#dRhZqi)*#|NTg1H5B0U4=!@&Lei%$W2tCLi7)}nySaK|SqJcINy>PwO2jkFCv!1qSq)oyUatcz&6ig$hVG<hCJ_Aj(bYxKnkV$4jCw2NarvD@~r9Fqt;ohd)8$dJdCN#qh+6`!e8?~lrOx*~nWGaS{!!VbeiyLv1R)~4zJhUWRqB+?dd1M|Ik&94>7_B|ppt;r>v1p;SLJV~al#nG@MlM4;wA8F;E?R1<(ShuMwq#o@CKqEJxem+GO7o&CVzoGQMr*ALI#GATT5>Hmlbhi|8*MxMq#sFS65>hg*`+qx7VIW>V>{Yvx8neL0FRT8BaKW$H`01`sjZfbt>jkRj&|Bz=uh@XZ?ZS;LVN8X4wHv*4|z|}au@fu=iX7|C_G3$h=b^$-5=yZS~}2jl01p~(UJC(<VieDK8;i4DeOZhZ9jfT{RDkF(|(3LgURG%Oed$)vok%PMi<&=k~6ut3-_KuoHieG&{fOD5O}nq7)U(;cawMHIC&f|kS|~XyxKXuPQH$t$(yl|T!<IR7x5<fCe9&I+kmBr*Os6N30g4<sPpj}`5N9O-^Hy+(%!=d<Of(muE2V7J>DYU!pG#tcn>~pCpIBj+lX7>*R1DvlC_oii2MkDCI5;YNYOsSUUDzCk=w9~+=ai9f5VsLm-r0bw6F0U`5m4_5A7-3Nqq<Qpu2V({z3hBe2rA?2o8~l@BsM$PLrqcZ}Q)`L|(!X2<-x%hps(mJqM-Thhx-7@dNn-ej<Ou@6k(p1#ggV;Aiq@{FnSMUO`{&Pk0BtwYPB|eY98cGWARNh5QAY)?3rGPti}ih)>8*@GJQ%s%ZVRDzpvIzQAA5U;8uuh=JON_yhI(sHXMTs%bUI8rtU=q}9~EA-};t$$#Qs<iAi;8>~V54+eAlk^B+gli%Z8@>_gGeue7vsjgKetI~IfcC}WEtfld)%k64yC@obnl-opdB1VuSP>c3j+%rtmP@Al+jlnQ(6UYguLRNu>;k4A&hI4N%>RNc1d>CUeLaU8OF;aUB4^f}MRiyPy-zcpPO36|@LOz14N$Z)u(VBs}r1c!%Xzdz2gE88(FfmrEqg5lTp*mR|v&dP<ATv-$8>gK`J&e=p1$7<T#&J7~@mgK2CRr0#Y2&r4_}2t28#ORNs{u>brELPY*|f|?Hs@gL_nE<GEbZTps<hMZODp@kQ~Ua{BAT{-M=F)8)K0%&b^BXZD~?NTM$?u2O>C(C(X{DCSLV01p=)+DUD@Bn%Fq3&wEUaW$lsS%q^)PWj_rT0N9egcm9EUQdy(3TQ-Ky0=_t<wR`_h7o96^0pBa?SU8z;i71};#G_88ZurkjQMrymQqG_`tUD;<6RnH+tK9eY&yHZ!;xy9e~{9r{|er7H5`8BsXa{YYj)|s3ihNhlwz9u;LSlXI1t=~3Ywyy|kYhIS@rsQu*aqKy#%zxhPPnPz+>8;dLckLFH)za<s6&N?eEPi)k>cM)q2x}cYfAXGS{bfxb5%RI}bK06csrIoUyJ@X)+x}r%iXZI9(6Ls1`Zaztb=cLrgd5F64qG`>wl)h`?Y!kLyF^IOZnDea`%l^YyR1}{-3Pd<!xcVGze|z*!;cMLOL2}L>El=*QBi$lpK$;1^$_Qn75ap&pQ!Be@!>ws-+x{Dm`*;jJ=~|lHow9r`T8BYHZ}ThjXv+bLvJ#^Ow0bVU2cops_oFnO~2A#Wq0~M{{Pbc78^ft;dd_jLb&J)5v?!evLf%L{Z^kV%W|s2<$kOn2SoI7=d9h1Q@hS0+PvXh2c?g4yobuFto_QEPGvdfm{8p-Qm?fF-wxPe3>|yry;a#RA1~i?m3=ry433eg$I3o(9L1P&Y=0N+pqzgqb3--8RljMBm_sU@8=c39DsSE7LwG;R?WwviuIdXXy`10BYmhZildQ?_*~__A;f1*lzcH@}{zh&Ex3Wuh9jwH4s881C_wSY58j=lZTZN`*Mm9qOvH=>Ajc8kqn{WeZ-Tzz7EryJt?H05|YqB+NByU7>vN>&Q&=zgTHfTj!zfN2O>mJ@()W%ihRcJ@HgLSvABW)Ydncw(tMKxSYUW+c+h&Xt#9$k@ybx1@!bpkqJ6B^@s@_N)I>p~+n)FNx4J!$>Eag%jlk!(TV&G4fe*$q0WqZiqWwk_xlK??N1R-~dobw3QG9)zLPL%4q%MxZa*7sJS57)6evZ9B$cBsmhJ$<Y{3j>iOY0w$5xuK{;pEGCi@F_oN(G%}60otS}Xr1h)6U6_JQ>I?*^vye?ai~DzD4rY=wkwfNSE;*OBJ;*~onU4ap0Nt&7UPvKRkW1!r|LwRLgUP`dKn_3=_MsRHaT^w3G4^5!=Fu`Ah1idD%qC~UNBYo{?1?^P9}FjlV+=V4)5+=dy#q^;OeVuida;aLM%$fO6y#F=btktHvV^vws{+CA<8!h%h-i98%ZpL<pa<s!^*5ibjjFAf(KKTUyIeDxw#!v&#uRqBQMFyJQg3fK#9aDDCvkBDzk4e5?tk_T>Q`3hxz)nfrW?(&gk6?W*EstZ<L^Vah^{aFs=Lv3=3WfyT7Rq|qG;XLrb;uWZpSp-=nJ>~TKdD7!{WIE@w!TXFu#dm>0h606iw^4HdLB1Q|*{a{f8rEdA?-EY7tF0dw7B#sXttpCM^Bk2W!npZ5<m;7q{qbo*Up3UsahVWIg}e?!wZa{G4H`^f#aP3%(2Ni$&=|rH_C3oDuih4$+|HMO~#&u0O3?`n&7?W~lUc&xqiA%|0s1HdT7Y@sEP<qDnaMgRauszCRf3-@`>~QdRmw?EYZC<a)j=mG$<ahMse2n;3KP3q#gpM0(ICu6t>zN@tCIGx#2^+5@YaD*dM$#s>YzuR2w#(mCFvsU6oH6klpThv|{GzEf)HK)172{e$Py?cyS(zOCQ&!S_<_I$vK`>46E~2j77;>ESMhN;8*CJKsd4wsTCWnZv@)Z8Ms-^E^y54^2A{g-SD@g`Ll)teIDaomaZ7nM<afOG2fYx4NCThDtO4g`NMVN;5Y~?c7MMtY*#_cFqWuX3mt_Ig{!}GnY#3TvF=LSYZB?%6dtsH}v0c-Xi?Z{@vhM)9taQ)XddXJ6B6(&AckL^Ga7~=BIAwr{PAQyDi)7`u!WJU5~F9)WX)L@x&Cf^=<d+YnrYU)WX*0LwB?@uj(;Qoc+G9h|t2;rmX$N2aShb-y`CmD%B&jZfir<`=8wYJFDHE_<7S)vcB%VY%{k{HQm>CjcB-Rrm*zGht`|pKOJp;k^PlE_EdqG^u$nM>Ha6?n@bAnnHN7Q5NnEBiXlC#hzIK|6w5oun6e)G;54K2nEhgHy=>-oo*uh@pZI#^KBLzbUEfq~zxZYP663*tEKi;O<RNiEyk5F3`DCf3ebaACmG$3h^n1FU_n^pLoAxy8X4-WVth2D|Y_e{qT{pox3%kzd@_w~~^_-X6Uev5pOSBOSMA27G%^6z1VBL=WxKfuj>r-miC-uGlS-OAKesQ2<p<!li(jV%*M~r=bPnc%idf0XAv2$nHwX*onYX!BiwfwF+A-~T~dQY5?-z6u%CocRQa4TAsz27b7i2VKUmP@^Z->dTf-X`pxgKU@Itt0!W>^#=Ak5%1&i{?}QT~+px->vf-e9F%yN?GMTs`tUkWvTq_=aq!?jCSZ9bLH>fv7b@0e8S#ACdXI3r%Wzaen-#b#Vd`wzb_E|t_^>Wn5xcE-aF>_J}fzo?89<(yWB|s$Tk;|`R3+bR}Oh{#ruX-WkvWn=9~OHU_>rC_PeUTB4U<5uNTp$j{Ty_4F{hqezOwMFOK=3>bvLuU1opavo@wfJxwY9uQ(U^89KRcs{WGgXMQZxhyJYgQPoZMSNX`#-^u4v**GfuZ#>5<o;_6Mk6eG%_>FuIqavRj=RJow!TwdvGj8TO)!2_R=cw{o_II3TDyZ8Pc^lE!!tT?sW7%KA?k~~!i3_JA<`Abmcbs!n@#UCq>Y$o4D`;D%oR1dYDJLt;899zzZp7MU`L$KfRXNAp<dQres^&LUo<!WMKJ7G4E34hi36(uoo-0)2{eMf#eW%JpmA@)CRP&EK2Ia9M=ck-|k-s4b#e4)+P@Sxfnxu8l|B>K5|3^_5*OJ$w0cqXCf0SEYJcg#|L-s)pvIeS=)v%acjOJu>?muNcflSszKe8WMlGYvmQ`}aOtGNGhw8vm_Fq)7}a3h|;O;}642A#>y+<zLa&;q|h42Dq;MI0H2crqUA$aUQRB$DAL{TPj>Fb3_Y+oBWM2^+`_-2XJXV+%^L6<%r&x>!%UVjMXRI;nHNfmEcE=?IVk%pvFCX7XlCC#S<l`jAK_Vi!!@j=QMuz+v(*x{=)&;|zMEHfgO;oZ;4&wB9-R4Em!!X|0t!!)*{bh_+|BuP@mbH;^}A2ss3!$Wh#L7P0g>%WV)j2$RXl7)}o7p6BQ@gdBnnWCx5T$6^{ejeB0e1a!5Y(53GS+$NKgF`Jx?OgxVajK_=g97~Qx3Ymg5G7SY}0p^kOxc?>0gdhduy~Hh(%%tsQ%nEWQ|9Y9*Y;rahk_(Yf=5zlm$VC>Jg*-Bkf1P9GG@Qo_6j2xQuUA=$#RC5IDz~|$^~Swdxh*6Ya{p^sgsNm!XrzW^<TBb`#|ktit<{{@xveHw)AoDZf@Wkh`uv{TGIAL<lbgBc0zFoftI>vRgZ1QkY$vyK&l|WE9m$ULe1qF&ax?am`?=>$Bw!o44M)kNI7S}hac^>4Pg?6sZ($FTtf!Xg{}#9X<bFIzT2FAljYGH%@8C}CCU@g*@^1e1E@So}d*BFp1ox5mv4nTIZNqyk<tTZSwu?B9hp8W;?R|P4AP+F|`>>u0f1le!<U{m)pW6}qf#bXuSqnYMo>)RIvHtC23_u;S4jPgTv7B5^+aEC!o5)RAN-jk&vKMV1VjxzME3uQ@iAm%n+CIWm>?8MKBe@YH$Pu)C99+BlnA^SNy~rVRX!`^ucz}EWd&#|+LQbLWQ)J^F@*bQdPhtVNfVMwjK2DG)a6frJipgTyq;(JxO-t)Lj#^rmiK?abCPyu;6PeMpw7%o0rFE;QT3T;%)bCX7BRqW)#km2wLZ#n`8x+*<4-Z7srmantW=zwLsnoYLcwMh@=Pn^QnW*%#oIeEh9S8oct2F%$+uu}a`Wv>tq0(LcTU9^s<vk*9vrkv)nBzAFb<Taw+-k$th8xYY47)6)meyrNG%ej@FW1s~kQu3^d+Cn)blq-Z*=Zp@HPeNxAM^J#E&cTilTDRQ{zIy0`fi-~*q0?#x<l6!`oQLUMaDng*Ja&m&69?uSA2ioQ0askeN8LQzw|WIjee&4)B2rv?-GBR^O@eh!Q51<ZAIL3sj~j?r<e4No41M8SwHD+beoHtQeW(Kk7$$iVd@(b-z~M{l*$_Yo-r<cw@3W)m$!_jQ;!Gj3r21&mGyfg-!`n62a7*9R9adS)ZJ)lEz(eFY28FbYH4lJQA_JJW;89WIhJeYiLmoTs5JA<wDZlBHFH3>b3j*V_PenAUAWQAJ;TmDL)Oey)6P{>rP<fz`6FxgyKeWp&c05y`#M$D>|fpPUtOh{pXIqEYv!|I=d;0_H0+#orJ1*-cHWjs>(RPOOKabT8!fG;2x*<gT-I=k*zY@`d!Ae&s7+g&dk?f0f32S;Ru=UV)TXV?fArk158HBw`1Iz-^$2a)+K@H#?vT|!ubv-zNLniq(i)06bmtIp_ST>D1{3CqLB=T4(y`O?O<8-N_(lKtk(J_D*BiwjW>+)w8m$timS1mvG_0S#`^US*?QK`-c^!)NpT62J-ac`s{@72;jgS6wmni7E-gxzqS;mB~4~S9k6d7-RzqI==-yRkJnO!YaS`!h{T8UMzu*(&)W<5>2o+j%c>^cb6&9LicvRvIRS7*7pU9Qf08g@Mm*3+=-Y1QW`yFR7TI*5?gN6f3vj1rF&yrkzYnJ1`CTbmbpT`wB{I7>81i4)YOt<9|c8}w(s+AFkA59txwu(cs;;O^E|o&X=WRz2q|eHWJR35(z0V^**>5zWVRSO<~s4Vo&Sh`KrYEAIb<`KbOK7rCq`KEmPNc-X(EqN=mXU-j>r$Z?|h2#0$wrkj8BL$*8g*A@Tvh8rL0URGG$RR4a4bWcoK2i18g)-NLS%CUb{{iV1sq|A*7yJLGw_sWFoeM_poj<8qQZt{BtRP~qZ6Q#{fhx@dla!q^f%y3vkaTU{Lxw>?JSa(<x5vq5D$n}ikuRE++2-SF3%`K7dEmP!=<2a4@_n92WwRAtzRLv)D#-J)@l$=z}C#oD1iZv$3I=JzX`!w<$PA-lu?_ax3Ona?acUWsM-Sl;o_tQ9*6>$v`4!@HMyUwce!A)PQ<_9-pP^DFK#s8vqY=1ZT|NlcrStBr|H3A{65g5`MfiA5PIL<|?Jdw*f1P#^5YN$zCYX^t8X*e8QJ2=ekdh&WSCL7as1WnP4?1dU+4OAtoqJS*GjpU8oe-sT+kF1A2WFNF3Tc8!$3Jb}F+<y#hFpwOGCS(&dBdt5V$GEj8t@nc5gU(n+E<-FCi{@l=3?>I7j<nwPaWA|WNsdHovNhU~?XVp8S#O`9PUQaM=!7n07mUXJ7=sjQKT^q5tRvTP{{!$LolHk2nTg5dWOzsq637H>BsXFUxdl7Po#;+>=W!3BCu)<{dclL-dXv3rJAuBaPg?5*C%6qD2hjEq_w^=w;|B5u3?c_%g!RS*?s*t7^m&-u0CE5(;H33_2I?W)^9X$gk%Q2dY>QFW`xG#VoP;zojr$+PSac=3@`y*dO&}*Ao6JTAnZf;!(SH;<3h`t-rjS!GgPg%Vrx?eg^@f;J+;YiW+8)PDbR)Yl!sFaB$PC(^Kp@DO{ObvB*<?2I$$aiP&0}YfGg!iDZk8p$J*T<l;&-?i)ye9pLRLW$Sw!2Dn2$zeBV0#bhXv#U+MdE<+(h0)pQpGLkwsXAr?DDKP)d&l<N~xLTVg4>6dTA5++$!RI*=V0!{D}xT!n4qHf$z0bH5q<EsDu)H@O>o$-O+<g!S$dlUqlevEE)nCe!~6x6R~c+MdDIAUE-^XSi)6x8V-*4(@rDF?*0bu#4P<edIot@GQ5rILlIYle=j<%k3a}khbUOxs}|?7|(G#NFL<==eX^{^TBn2=eg<D8%$707Si?t`k@YKtqZ)st%NM0?L`zrkOITW;aEeiq3tE~$2@W#ZY6KUcyc^#FXI*rBZpx+IUPI59kjiIaad2T$L-|p!F8fpw4K9tOvQOj!yM|_xRbn-wpWpbJ$Mbb;cn`?kVodx_B!?>hqQj%@;bKz<N@0L2dV3_H~', 'winter-fixed-curled-deck-toboggan-01': 'c-rk;37AyXnQc*)j)=rSqo9aQB!~^vUe(ZjpMbap8U*4-7;L%<Xlc5!s~TB?El!XqE<q=g;1;81W6&Paaii-!R7~7)i5Ng58OJeX(?pFiF>%f<>K5nSdbg_=zI@4~_`V~D!+HO`_22)!y8YiLiyG#f(W|7SWZ5kxC8@zBCFjhZQM0<dHknMM$|tNYU!G`A);BelPbd$J^OaYWFG@5fnrl-{%}{1E*DtDXtZf*POx339>qab1Bo~jUYidlUnp^5p@~Slz<;gl+Q9i+!Wy$ghb61x))-HusKBcKKRo~ds)RG)ArKPzc5g&VcqHf8EIZX?i7A>l6#BhyG@ysQ@d28k!{8KK#BstAlO--r!^DnD!OeLDfF05aHFm(r_#Sv|6DjRLA&yRq0i|ZTW%?W&<x&DekMX(}N5w3{LTT_vXdH&+2hQzEys-?NHzH!lkdChL9kK+$=c8DQACq9vW&79`i#-z+wLi#4xrc#N<`Tm^W-zk3}=MQwsAI$lKy8jHBirMw?#FVDy`21;!g{ho3)UkI~{i4MO&0(2(N!__GoTp{Y^-Jqh^~<x@VZzPz3tCe0kE_dP&X|4noU>=tWJ;rE#;oa+re$(eUf&q6ualktMy<t~*4H*<OiQu)*{PdC1rLS_ai}nd@*fN}uhVPT$<GowIDsfnAjT62baeuO&QG9{lIi0a`29VaLa_5w@CRrPLDw8Yot=Yc?RIwjFpVE^jUVma`09S>>;z&ofl60N`-~Hqckpjqx7k@ujfs_$6OF0!o0{U7L%gYFK|?}LEnYqW584E#wV-)=B30YaP+vEzsb$e(JY_R8T2PzB{2Q8@&#0}-JhA8c#)T>?eB%O9{Kt<x`7?L+flHOiHx83*R&frh(ZCwY(&@F$OQtr)&up%(Z|wQ30>SKrFnFko)2ifYO~-1)=Ok(y<ho62j321pWY1^lS7{4$aeCo3a%pSpu>Q%W<^xN+pk?90MDuy|iOVt%wz{UJ%dpCgsW~f`;X{P|fru1a8dI`<P$j91UVh%xDVfK8z5MnXi>bsi39A?@vk<A|UzuuJaUi!DS11;%@UY3$@ofCvoK0pL{sVKVtn~Rpu}Xg+76|wvp#aUrS0O#p5{QJNe!%C)vWN5L5%8Kv*mEAUr%akQX;!%&A=vRJ3HU;P%e;oVJDY4y{V`v}7xMWdl>r~p8;NGJotw>ptV-k=^QIE+IJG<#Luw-(f0$SYnT=#Ji|+y7xL_#4**x$!L7B}^-khV|9MPXEOFdgz<c$>TI6JX|$*DX9$&m{l4f*(2z%y6U81QMvynEXBH_M*i-_!K@1BWJmk%%jQepC7)exKWyH=*F)E_<OKXD?jfIfJK_F@2$6CNF_V6jc-n1bwkUC=?B3?$wAt7V`(9p(q}1QQyJGpu8^V3-Plra|cJmejmc%OCTEchl3Gl;c#UnfUJiDkys?^_1zQc{^Tn$UN{o=M*?7BY$r0`L$O#O7z+kNflweAi771_j`@ADNH~V4B$Y*82t3w9xC<+T{#Yayj70sx%r{po8mSCHj{0I@fBvJ&A1&~FrB7j6#aK5J;k_7LThUx0bZ-qS|39o@z}NLP#4HYm;B8)Ji??89Dluc>!c0>o`^RaC#ziUlb3T^r-~{sA@~^veK`7#jxi5%DVjcLy!DvJqAQbB8f+(t}OBeWkfoQ;eMNIx+X1)Mxt9=GMraK%0yPZhat_b?|#0G;MPAZ6s>Dmw><fUs@ghSy-mnIdCRtCB@L?q_x;>U=_^olAlsTe-Fb^$(DM@8<B=#wgRMcAij3O`5$I=TW+u2|Q`sKhR!OIHMg{(#S8R=I~m_QBwah?@gH|L<E@QZo7Mnv!+D+Gv;Hm%raM2VCg<v1bl*ygaODxoA(_RF(DEIyZS(_ll|WTX&4Gy*#XExhtm5O&-?0V(R>ai{iq|!+MsxV(Q%FVcjdH&KGYy%JTBCp5?BXIyZS(_ll|b{!tsn-e|w77q2<q<zXG%CXXwo;?lGDnwP6iYCpl{VO_=~Zd3f+STzg2F6_5^SO4kqF)k15;5K<&F%_4d24`yZ^UqbdJgm!@#BGY78*A%rH;D9?Z>(OvD&q364sMgj6;pBP*|l^__08>-E)VN6CUKkM=f)bc`+6~Q@5j{>wpcC?>)<wdTrm}wo;N<<N4)yODJ~D|GA41G;^)R%J?MHd*;grkmYnMHunumM#}!j?=~?$-wV3tJ*)9+3GA41G;^)SCbH;U;+e)#a;Y^o@b#R+Ju9%7|51xT859=ysmfI9RH`eJJt`)te+@|JWd+FdddGcaPE<G3TyIIXac<C}Gahu}j#`?jJHi(Pj+k{*r_OK3algAZPap`&BsRuJ_#2(gVOyV}h&yCf;*9P&ylvjnUVfL^NZj;9qQ*r6J$9X}>8fFjcGA41G;^)S?wE7ycWcYp|?{W694sMgj6;pBP36K1_koP!ySeG%0+Y~=H)~hS77V%9V3i%9V59{DId0a6Sm!7X|{k4$KK=!aMV-mM1er~MF2filneIcLi>|q_;CXXwo;?nclUGL?2SeG#sFUkD6!jb<u1l&4Ayf~kKp!xhXxyE_pxPhXle8lj}tykXuDBV+j;?{cSqa$7tJ>~y$c$4)`;vu`IeD27p&S~e4w0g=P+dR{HW%?ker(FIn|J+k9=OyRYQ!eu)^VL%>*G;ZpPr0lkSx-IXvaV%)_mm@MHO22XM@*aIcbg;Ug7V*Oj-1<+|88^Cq($}FZH}6Bs6M;R@w-L$Z?`$-<<R}xZH_!y^nB|!$GSQ6eCswx9a;4J?>0wWJM{eTHa`rI@8lg090BwO`T%`_en2Vk8Q@5uKX4Q<05}>L2z(Ye2KXE>2p9~M0YiXef#ZOoz%bx=*_Qx@%iPL&04D+Ez)0Zpz{$WU;0wTL;1pmCa4Jv%j0MI4;{l)SO925O2!wzz5CNh<45$Pq026^Kpc;?~ltp$LFbS9pOaV>@rUGXGX98ydX9MQ|Uj(KB(}5ab1~3yi7nlXi2Ic@?0?q@@2QC0E1TK=b4SX4xC+h*24_pk?0t<jTAPyveg}@@&GXd&>OMoRn1F#fm1e)Y~l)$AxGmr#QKnt)OxC~eUtOQm8tAVcoYk<pv*6apmEpR39ufSJ<b--1?df;oo)xb5t2H;xYI^cTX2H@+!M&L%^Cg9(IZvg)ed=vN<unD*sxJCBJfZKrEfo}tM0N(-b1nvUv2EGe?5BNUt1K@|iX5c@7Ex<j%y+9lApTK><R^Wc%0pP!Y2Z4uxhk-|cM}ciXJ0Oc*-iY$yp!F)bKgqpN+oYR%r+Q58Rho3}LwdxwJMwt+IfdSvWzM}ylg@oekKU}^k;kLYDfHefbM94|bnZiX^k(gjJRW^cq4#E)b3fChbFb2)H*0s~(fgcQOzv|E?tgM0mHVIEYxU~QYQ0uhf0g^OUNN;kr{Ml4_ffh3$-P#u-mKPZb@f-dAL|uU>vIb3e{vs{`=8uv_3F)Py;fI$mHV+?F||IY;QlA~QMv!gy;iT@tk!FF^;fwc>lIV$a|-T%avzoZpWJKp>dk7sR#$(O`>|dzwLYid{-@qY<^HGYwR-htwO(spf0g^OdQ7d)DfIrQ>Z5Z1Q}4Cvy;-f->gum@Kh`Uz*5?%5|KvU@_dmJU>eZXodabVhD)(c(VrqR(!TnF}qjLX~d#zr*S*_RV>aTJ?)+?sg=M>!k<UT6*Ke^ZH)tl9Nt*-tm_hY?cYJE<@{ZH<ra{rTitzNxZt=H=6uW~=uE2h@x6x{#hJ}UP=x!3B|o7H-)uKp_bV<{%<+_M!X59`#A?M(l!q%hC*=dLKgOA2s@{2lQ^b1Kf~A80=7e$$$XS$5UqRVF^*omT7UPxf#7>Wn=`zWkT1nQ@;z>}4b01^&sp*S7U7d)mmiywz&$`_jkT%I^Gyk$><+t99qJw)UDAhg6&R);C(6n6I=w_UWfpCLVdI)fw&F+`jGbKGi0E<HlC&m-qgr{o`HJjeO>nmsykFi`jrM@yF(3+;;}1U-;9iY7@Wjf;G-9AMH#7Mvj;c#rNcxn}d0!F~2GkM@)<2dveUp!o1R$pOGWy4)UEw-m6R;Yv*9y+Od8UO&mG5knc3|US;A~I}7X9j`cHg)TD!YY)4&AG;!3ngSwVKB41(Rs7VX;*p9lKXyT}C3w53Gcfg%2FEMdh|Jj(^OkCcNG*3@1@5k(C+-BmL`ah7Xb`zKNpUt_E%lk3AcH2x`-jCTDXg6_L|Jhnfn>f|Kk<0rrTifj>PWPj2;#B`>6PNX$y=RS_?nm3i<^7m_hNMkg)_?X{WaOFpKk!UzH*tACW}l5|6PNd6_8Hr5;<Em;&uSx=^)KsM*0+hv`!W07VdV0D%zg(M`JvlK75l@*{_sC<e|Wp>cLI+CPXIfBCxIUUKL(xxo(7(g_phw)d)M2OFHTfVi#{zBzoh*EanrG1&G7xB?i1``9b6bZtP2%W8;f<J&w)K0^ZDnV^Bha+YHo_Z_1$6BSuPZpF(p@@#Y<OQ<w5sk^$gGEA#W_!Jv=#Geip-6IbCtizZ#1<$2aLbPs%6fpY!ALu+BL#ttrhvFFt$pYq@?npSp*2UKhHSYn9hRm~>t*y|#HRyzUWw9lfsQI;YQ`7oR=)wWd1PJ$fxk{Sd#8^!LWCze8Tq30@#hmtuMH_m2o?{w#m*3GZZ2qadf4P62*JN4&FpLamRI$5pIs{BHBkj#r3NOsglnxF0^W`(gErJ*R&!Tk-zAPPNrDdBE6!%^ud(_l}2$b)jNvW3evuIk1Og-thQ`X|J)QuI8q={Eo<Sp}6{PRiDL6S6t;m_hj`9&*mX-EY>|dIbD61d5o3Q73ch`v6ypwlg{&`d~*IdKQ0gJoD<WU(){z{vq!&{>xc8Hdsydnp=-HTc`bxV=k?NSo7ckY9?{p)>sqdJ`s{h}*`r@;s&n0=*OJtW`=#Q3skmP%?w5-DrJn7V9(?}<NAWNCM?317{LY_GaoEGU`rh&Iur5?gZ7kM>J_q)2%s-4i-g7LetGOvIzaz3-D6YO+)o1b26<2xCJy|`&vw6rHi**lAPFLS$9%JQn#X0|KEan{Fr1Lx}pPYZrkITb4=ft$8H2=K#?9s2~`r&-)9@cqX=vuB-UJGH;dA;=7=C$y;NAz{{x|ZvlK6_q#_UPA|>Rk8ewIuc8eyO-$D(;tx`=#Q3seAjS+omtIZ%zJQoPXg_);GSh%$_jmeR1#G{jDu_D#zKw`rXH@$m#51ec%Nv?fs*ECsq#{;PS98{n0(|if`{6kQYbka@<Y*-xX&~IXZ7XN|*EZ^60wPSgiZ|HRR?d`LOYCRPFuP7Sgln{-0GH`P=P6#=QToH>)Z}J}%h9x}2MrhjsZGRZRA<E_0=H_OPDG`R2V<TY9JS;wW8?d*!2hs;+r)Ti$$>F6Zy%VLg*K8jIJLb9>oUKN6q3`NupD>x1t7vH0;9KN5T`ub1Rc?0ix@zx(4n59=x>U(2;2x$^5C))nV#xeg^)W9c5&RUE#SYhH5o*>w-=DyDwF@IA8i)u+V9hd#{nu+A~P?q$grUi-Azp8g=u!@7#e*Ya~ia^=@OtSipf>i44>OZTv@;_$Wl{mV7R9@bS%U03;+d|&g`;-a>f^E|A}cib<2`^CJP<Qlv8!>@_NGq2=%SXVLinq;p0x`%be^_o=UO0LGzJ*=xZdQGZ4NUlD+?qOZU)N4}ZU-Dl4Hi(78cIJ6l=a^iRTw}p?8^qj_7xFx;tC)ICGFN`x!@A;nO{#GvS7YfO)>Rx+P3kqq9@bS%U03;+{Jk5F5Th@$^E|9SJiNDPy`(*_Cb`D$iyk4?T<hd{SXVLinq;p0x`%be^_o=UO0LGzJ*=xZdQGZ4NUlD+?qOZU)N4}ZU-Gs0^cK5TJ(}lXonvxMa*a8?`-rt?J(A~PUB%RElDYEh9@Z7tYf_CXxf)CNu&&~mYErK;_OPyE>blB5@6B|N*ZxYcNv<)qH`6_=^FEMklDYEh9@crU$Tg|P<$a*;VV(DrT$3sf`d*PeradRuq{=_<Cv^|&9FuF3YfSAYbr0*jcjcO7uKc=(b>81{O{#HuPpf-a=RL4jP3kqq9@bS%`SWb-Jj>etxiQw?17A0O>kkU?&cz9wQiyjZ&V;sSzW1xGt<KLkol$M#(qD*wzs@<i5SM+5L%|XAyM=gX=8Vrcst~_)MbdhD$}D@^iUwigbLJ(jbBD~ft5z*F@?%$)S#5WgI@2E?YMFRVpE9d-SE=)t!-pBU%)@0P#yI=Wu{z=<g*e7_?AuG77oHqy<OBPZImhiOb#5scX5`3&Gi1Un`=Yg(oOtr;c}eH_lV;mXnwJ{6^tbqCiTzjOyUW0lPY3xF$fuFZ`Nys=wJ!h3P{+iN>09P}`c$d4Yrrrgm-#%k?-*-gt<@1PDa7Ua9(!Y{)&HfTMqbmm%sTAJQfu@v!;D<k8}ccTPus*BP;bBJKU@5D?NTFeTb#7Uju~y=v*IdY;u|L>ttU=9#qPCey^%i>DYNG7-fK_UKHf6%tt$pwYv#XhpBVEQxy<Lp?R}lTM_$+wFDb+?kCZv#7xvokKQZ3Ot5*zmLQ7t^cZYmN{;kDHXZP`=?Nw{85+)v>m~`Hnaf*FS-FhRx68<emj}{ZIyvjCl<kLYu1@dX+>%(Qv&TsD(Q(qbHnE1)720NoCye@8->@#wi&k?uwwZ3`Mg&pydLj19CnRVCZy<+Rm@kaiQRfDZ($GtAvr}~T>`LvKvfqdE~o<_ax^q(S@U9#TD|0<H!BlFtQ*C#g#6JI<jX$5AqrKcs#e9QX5)_b$!_D`QZ(=zdAHV(F?PK(>ycbK`%=kV`cYo|vo?}(Qa;#=1bc21iUx7#tUiSOJv*!k5tar-Ab%)G=(I@9O3rR$If6Tf6q(pfvbEj=$`=7+<-=i;{N%H$^7#F0-2`K(4hjr<wRzwN@fIOEwf9TR^T^S^FpT(s^mbD7UMo39lkM=kG&mlWbpVttof5ElzDu8D8O`tCkAE|%;tbL7)PKC6*W+r$&7w>M_CRZmQq`C<K%)&-;1RL#Es4q@W*ncw>>Emgbv-frY4+&Rd4D1LJFkg+o@6CZ-_pvZ5_t8d#|W8^YdYes&tdTv{5k9g$nLC&KejjVpSVy2M~!gusT=YPI>?VcJVf2m*65x1_adaCUXVdBfMXSn*^6;-W$Za4DVOOsCj6PLH2z2y$u#O2-t`D{l%jr^xu205Dt4o{zW>P*MPkxysGrNh%h->flmnX85|lhd;wZ0!+$ZSx>&?y?ipYcZ~gBcIlVgHK4GysyT{kxvWxY)3wA6GuL+eS@0YN0;7i<i+#E;{U%{{QoyQ|Nn132RskF0PF-_1YQDOmj6~N@Dt!w`EL^dugQOp6W9&x0rmo~%YQ2t_!;mfun+h-@ZZ2&!2bYm1OF@kEm+_ez<%JD^5<gU*T8Rp-vaLf?*YF9elOn-06qXd1pXlZ4Orlhz{kL!fIkDD0Dl4g3VfQq`40nn0fz%e0KI`eKwqFAPzrnoI1=a&90d#jjs^w-p9PKqJ_if}1_Ncl5a3wgIAAC+3^*P*0T>RP2;6<l3PERWg3ikXowEx%%NBGNCg>bc(Ak-wb1p$=f}Xnc)A^<=4xP6OI_q@Jht5(xJ-Y5S7V85qSSje7R8TKbP|s7So+o=)mvi&-ur5C%^*jaj=mhnR1)aGII*WJtssHJz%W+lzP@fO=Dm^`{XYxj4@%nOZ=?u>0VV%y`1ifqFT2nd`ba_~(vu{CX_byInlt!J-Nd>*LA?UpVL1(5e59{=9fS~s}1f2^DI>U8&Sf_UtT=xs#BXkDm^03Y^z3yen=}ge&VV%yt1)bfyIGs@%bvh^Ye9lNtXQnO>>-27bpm%#*_b=BNdswG;6<j)<QwutSb9q>&^EFpZa*ffMpv%KLoqfA%k~y7G8g)7+b=4%jS0L!j)a7BF-VJcoB%KQjI>U8&Sf_UtTs2AO)Pm07TprdrCf6j_7@Y~aJgn2%x2q<Z(;1~vr*l$QP11V>g3e4`9@gpI0MDA#Ym7at)4K{TozAHRox!<0tke0Lt0uX|=uFV%VV%ytT{X#^&M1vKos+t1lHMy2bY|-Euuks=xN4Hlg$14Ax;(7Yy9%zFq;qOPXK*eL>l~A7l53341YI81>FnE8lg#Oi(x}rpsjDXGy#hgJrY;Zb^lpG>P3kqq9@gny1(#0e)UJILd%X5ndQEbT(OI_3!#eK+xh9#@*}75Zy&~5ny;mUUtl#Bfo%fSmlXNcZ+7q(JwCCiSq;qOP?_Rn*taD7RNv<(E%XWEK=e;Y}By&1jH|o5<<(j1T3Iv_?yF9G(9@wiU^%`Rj>&5f;;`w{={JnVoUOay<p1&8*-;3w(#q;;#`FrvFy?Fj!Jby2qzZcKni|6mf^Y?#_^Y{M)l;3SB', 'camping-backpack-01': 'c-rlq2bfb;)A(o3xfB7BUZl7zMWk-FFOqu!l_I@JM_FKL0=q1|gD7GFL{I@6iUOj7peQ0q5V3)X6;wdMidet`idg=0ZgRp&HYd5^{r=DQzV8?BlbPQ=nKO50&g5ou%q}Cw^lHlhpk5V(YGnYf?b)@<jO5%26Y?e|x0sPUB5zz?VeZ8I!sHgo9Y+@CkISEsG=ioiwHcE)ZdhJnQitYUlP0G(OKX;%mE0tGa$eztQTgM@IJH?y@~kGw6NZw5<Q6FbnvmRLz>MT^xnpT8xu^YHljL#v!|W$g2F)6D{%l6_*t`iN?WqC#p}AuVMvWWMbV%;d8w=>sG{u!HW{l09m{&L|cZ`45u>46w#^m)JH7svfa*K(Dlk$S|C+6jjq01EvDeRm#F?Y<EQA2y=PZ}|jqM9I59g;gC@2dPU`GswBhuR4bNNJXmk)C7!mzCnm$;!;i%50L-%#|G&%XDRAyV6r>C^g0ZUusTvN@`kaYI+lw2rO_J>5x(>lvfOnHOo%5y=AARxl%H7ax!MkY7#Ar3Ay8j#hFEBwm-ToS4L_^MpilnoSs%>DAnapD?2+SD~F!=|ChqZ{Be2H;>;mE%YTWS)GU`PGcCuCIIubyscEjv)NC>2O7Rb6W~I8a($h2kwS};!P8b>5w!Lx-@(S~YC5aYH8j?S3T9UA7mO|Y~DHV<yJ8I&n$$=@k6DJmq8Zv2Oo}E{>u01>S>d>`|9YB|^Jvz7Ul-$DAB)Qi$eXr`;wa3*rq$IaUr5DYpal=Lp6;smAH#f}@Mb$Y>KkqOj)M2LTFiUmlismr;yu+MOhprUWqsyhbOr2%FhI5C~a})9l{Y4luY54HG!rr6urr3!O%^zDp4KQwEuW1ET&kR>;rWl+wj&3+<sVTzURC~!&18bR`>T+dgreuoOUZ#JILY6!&!*1n_w9NE$S9VI8ShZ1f4;s)kqK_s`BhQ&=hm+j<nyb>1MP<~mT@J#IHa|74`Kd+br$w5d7M!1vk{+Dj^QzXJTK6d8Aw7Bo>Dg-GGwkxX=;f1^k(QQ5MNZ4K>*b>RMuy9ko|R$W2h;50()}<kD>FN^?nPa=Qv6Golb({6Lr-Ujg-FRs54q{YSceP;Swx$k8Q1)x>yQ<F9WpahVy#1V^axyZKUNkZHE`#4xpGodazqs~seE?lW~EYZXXMx~fRvQ9jGWBO%rsh<l(ejng(&JGB{Pd|plPYDl<aIOdX89!)U5Qhw2X9Dx+}|->Z0)&3z6d_ji|4vl=wUpT?>~h`eL}~rCnq-D6R88)Z3GNYZ@|bVqT}baU&+u&mC#m>4A~1!-v~H4T-hQEgT_`8b34jd_WE+`$wG4PtC{-n@=yWIOe-jQnEwmyHZla14xVFAR{Y00GBH@J==K%5gcUML0xzWQ&Xu3an!)RtA;qB*Jrl#8o1K3=?A$`4_P^>afMLC1HHiP#&+l-C)Jf1>L7!DT+583jH%gSosdaCN~MNZA^5roye1S6)Ogt`^uC^ybm}66HXXV^k8QP0@c%bg$ESX+YO||<KaY-AG~qVC*K38AYc_hxEx7%ZXSAH*?$TWF_uaQ?ne08v+=xuq^(rw$WQyOb<Pwpo4mLm0v-u_+EB0<3E7#Ss62F!o-n?T|pblDA>ZxUAU9_yMua<B5uDe<4U|r#Nt`lB;w!O`d^EDnPTzXbhn_JBJ(h;}4{WrJZ$^8tk6K+3bVROOb-K88c&GjgLVlu_%RpN}vl)G1{LrkXH+U%P>f0Gkd=DMA*5}PAdayOlDrMu2<3e?sSD{JS7mELeWVWsyR@xUc*%!6xAiPytiCtU2B7B-jo;{lHo?z%V0W>3k(j(F_YuiS#0fAzN`zGDB(=7P7?F6MQ@G}oi}iOCe3SBWzwQ|?}+4l$W(YxA$xtW8c>nd^4KN^Fi;$=wn6>HN*6Ky6JYtgM~e2`jzfh?U-R#IKxgXx{Q&c}w)Rj-TFD$L1&Ij`!%e@|w~%zt#E)E%$Z5?iReO!fq|kxMM(b!Ta8NOUq>MQRYTux~^A=AtF=!UL}`^Om(n%$J=c-=~%IM>sYz2mX-LmT=Ua6HU;XSWu=~4R@Oz!%KB<KEiKJk;4WpoSo;>od~i)UOZ=SUg!jGG$!0Ov35&Vyj$In`<AgW1s}r0Xi^a9X+-(k7$=&0GWiHzsvQjI@9LU8n2WsVrW$rSUSWI(Gr8i<S%{2qLJ7O_c=_^O9th*ytdMPH0*aEpbVkLKvQ&!eGCd*m{)+Ht@xjSN+%QlCs)XEVDKH~a>?6sn{HLZ4gpJ&b8ZiPc^8h!S;*=$%BU#qQecy%^O**(nPYqaxCu3XKh+N(D8m!E0*<Yv>i?%_s0)m~>qyhC!B%?`znH<BN9oZ|6Dibox%ynK=JQpVjn8^w>Q+H2ymRC`TcmTIr5kEPn{Y?L}%n)R}j^)fZ<Zfg1@q-QX9w)N-CGVZ^V4!ITf==$ftv}>%2=_gyhup`;0+N-_sb@46ckrVf{G|uIR^p!eS?U~~(+qx^CY14A?#yLKnADzA0S2XU4HLms;`S(iyx^cDND1M)eU)P7K4b{gd>!a&Q#m24L>-tmiZ>e+D-c#Za>05QK+J{PgES(><Kb87x{pjq~9#+;@JFfP#(m$52&s7_>x0kP*Z1t%;!(7wwu*%y0pIWblRer|3=F0bL`_#VG%=PSk=P`3hj}_*&YQsbNR_AB-yev0+a;f=GgGnL%tn;I@r*V%m?uj){{=JI-V4v&8DSn?4f3UZ8<5VA?QlDTyE8}jBO-TPM{w=j{RX^%nCH|1U)%j8C6VkUjKT7>W`dQ~kXRoYpNT2J*mHx5R-qww)eXjO);61{AKheDwR2#K#bvA0Rs`jdl+PA8`&PMIqFdL8J#~aCyI<EF-SYAFQFJGj*biJza6Vj8KctZM6lUGRZY3dWwZ#o;bmo)1Y(m$GY59uZG+^<H4j~*dEla$(9(I*}&->ql`o)6Sp{^$2A=Z4z{p3{zp`kWi)JH)@RwGO>e(Kl*;MN2$XKdOy7FWg=}uk#bB2J*j1vC@2Bz?V;bK73rAA0yuoTb&;@UNzr9oh_=fFEp1T{_VNp_R_y@+(CV;u=)hoOpP~uTwTBLoTBxc&X2AiL{5RctkCBp_glEV($5jcBV99E{{;N_0(G_`yuLzeA8xO#SH$sX^^Ei!)zS*QE_`Y(;p1Wcttjgi(r-FHq4N_up%Xfx6FQ;)ujq1S&DWQjI-R}v3*xyg#W`tH>Ky;L@MG2{J8@oEb4ro(FSE;9Vt$yG<Mc?f{Qd`8{_7@Lem{Qw71>48Nb!7`{iCVVA|9bd9*e(dZ-t-x^J{7O^Mas0KQ7`EdZ6X^mt^_<`1Kcd9xa2~pI57pb77~`2;1yB>oma5;5sB}G(Z78wguM5ug{N*_=T<)tgm|RkF!9l1M6gKVIQtVoc?-8*8VsQ%O4j6_4)Cgww>sg&m(Amyav^&Ua<b^xj#Oz`$5=;Yyb0xrPBaSp%ERILp?g`Ky5l|Ks7olLj^i6fiiSl1jXs#_G_k*ZCTs4sbD`_+#auIkCY)g0?)v+bUY6)(y;@4bnJpx>39S7((yLDOUDOrkd9Bt`Uu$yOP_7C*M9b(J^rFS@-7jBVvs>H16*K0NoYZ`1*Ag>C=Dh_6SAQcTnw#9wt|*W7RtfZB(H`xP#!8mdy?&;EmVRk(1~OxxE89yrO=&Zcjye&p%z?6@;c}SH6aQ5lk5+@;4-KS*OR;+`a&`^fFUG@z(A-E4Ph9`VK5l3fW|PA<VY9}O`sW!Avp#{Lvuh#A(;YWAq}!%3dt!j0W#rAm_c#|OoAM0i8&<az%+0}YnVrJ9?XKP;2OAv<Sj5C+Cc}njpS``D|Cb|u!!U$xC6REPgq8B87zSw&<E}#c^}*jy<q^{Px5}a2l~Mc@G!}TVI>TLp|FPJ8h8+LArBrW`8YfRBVZIfLGlS$2RFhvc$(zX@Fe6zDio3|giSCWCc{>eTVV@Kgz2!2<TiK?rowD^iR4T00?dTD;34UO?Qj#^3_D5g1TQRrh42c=SKwv19qxqJNWKQUVKFR)JtX(Q>u?v`3;Rg!gEwJ0tb%t)z5{Q;3U~<KC;2|?hX>$MI6(3Mya%h{G5Cn&NAMx6h4pZV<RSPNHo#NxDalXaFl>YZ*i3RWd<NAp3BM=#J$wmicqLwrY4oUy8CVQ|f(&}p!tdZWxP;^-_zwV<#Fhy3Xo8=^*KizugrDJ8_yhg~hQ+ZImca^G2`|Okn2hzX5jMjV%*1Ro@f>^sC*T}C{)TVhB%CIB8oq^Jpaho1U!W|WfzrtFFOq-3#n=#k2PBEu6b(#AH%T{MggNNK<|Lb=g%z<erjks>Dwu_rVFQv4um#q|8d#ZRWvq`!p&V8xSslNEns^F+Ao&B-!Lx7$mM2*rkHOe)&UrSrJLbNvb&~0nw|6LGj``+FN4#ofb+2GC*9nWcf6U$x^y7rT@4hWKHx`R)iMdW$=01OCDMu`Gamun*R>r4prz~=jbDglrMb3@IGItqgET*|`r8i<S%{7&EkI7=L(pQdHS$9XQ^ioU~u_=8LlV$E|tzxmV)-hSuDzGjwS?2DPWiC!x)=I`1i*Ik8<Slh@jrq;FD@><6?c25H?xYk)JYskQo5frwEauL#wg&w;VNokNHx`R)iMdW$=H7HmEk`VKamun*-4<1K%pw;#*9nVU<lI;+bC+?(;?0G}J+e2P@R^2(J#wv`u$U`*$tlaVcFMAsoUn*Z_J$LdxvRB`#d58ku&kAs>x5<QPFd#Slx3}CoDSHn^ob)@);cCrY;L8mVzQX4th*ytdMPH0YbkvalV$FK+Qwv=i&K`hl563Fl|FIA>RQKQnY)ZL7Sp}URNk9nGTpmO<$Wh6i@D1Cnj==;cO0?uUKW!@Y|8soOqRK;wTi{cdreH1wF<m1#AKPfQ<k|nWmzj3XDm)FImUb0E#J9!OkC!6%166iYz|zq%Mri4XP(Vst`in>y$`Pn`f<X;hp!FJjm6?xVy;tGa`!l4B^O7m)XFgja&gRoS~+4RcSmgW?h@<`C;Z$SnZdPo!eXxMC8sRc+9}Ika>61u*&9w+$=&0W<yt#orB;qu$=wkvxj15_R!-Se`os|{YaNp*HdE=Vm@MWh>+Xn^UW&=$T1ub9WF>cx6IOC@#7eCkv(hJySY7K_tmN*9>E2~3?@ck8?p>zxz7vzhT;+Yu5i9RIj#zmwi^(E3<$Wq9E4h1|vhrRNla*RIVkLJ+tmNW|m0CGs-S^d6?5pStJRE)BG2C8$*GV@X@An-8-~V&`eaCQn`Ml20g?!&pekU>f`;O}Pzw&*@NPcwRSCcgs+R67F!|kPi-FUp;ca%N?>mH0ZeEdSc@2K+=r5`M1-D7^=G2C80ryGy=`;PLve}VOl`F+Q5d-<GhJl^j+2I?u-J(x@Q_=SGoQRhe3Kk~c2%Ii1k{U_XBURyUF@BK%7pHzO=)ye%Q++IGf^Aqp=N69PX-V#23q4yu1A6@?_c{#fOgxgF1y774LKY`b1k?&iFk6-BhN9QL>KUm7T$Grc9+so&4<MG~ql=vOpf5PqMbGq?(?>|ajA@`Q>@e95G==>z^KZ*NK;{KDk|NOh%fBxM*fBn1tzL}C&$h{?e{6g<PIzLf<U&yEYK2Oa1Pq@9(&k@J}(?5SHzwhMe{u6Gmyq`uKkN5tg#P8_-6K=13UXD2apY;1?iTh9D{*$=>B<?@|8}}cxR8@0orH!Ue|NP!Q6MAfGDbB_3eMoJO2Y%mYdcf|L(<6(V-&&=*CFV=LP-vPbwf*}WG(O(l-xAjo=YBtaE#^hjBA%PSd)L%y5s%O!9<x**EByQ?(&ODNEPq}Q)N)+JQ9!zY;`94UviyGhTI3<@q_*>fRw3uYPN$Def6lJ6PK)1%nHi{OBrW3HeR`z%IoXSKky?(6ICqj>x~qP$zUsM%Q`kk*!k>s&tZTRyaf-U=w21SrUBxVaToBZ9T;#VPV0Uu_E#eh+cTv2N&i(ZUyPgXI=iyq|>-3NxYLL&>rcS4)y>G&epS2unpU*X=w#NhgFYMCn^MWGhBZgP8#Qcal(EmwvzTW6(iFxuo@OxR-aN7>RZy)fdXb~raqoz*#<2f3Lx0@AyF7$dM$MWX|K`qBc973<9`27C-=l=M**>Q;TXj;4;{CRXMqPtzR#jcl5i~b0%gGN74VVK#~wx1i+a$Ll@nsncD4TAMm&qaK~E}9np{PC_XqQ&(@U36N+(f3?&%O4j6wH){7cQnv1MYV{xAK8g`W&OptJQwlB(&9R*7T1^OiT+RY|NrIwe{NnEbN%ckrcQrmylqb954y#<sDso;X<YXITCzJv=TEhoTIBq$zp7aUG+)(Xp41|rku<*ihEA5ao;dgW@#`gI7fo-ac>2yeW$LtuM`#gGFJC(={9NR>{DvmBA5j;n<+zAr8R=ydpWk1S<@e*)A`f9F^%6U;Rw3ikE|PBGTVdB(r$v9rdPdSB&c3r<w!K&vspYtcvpwmttJ8w@RnJ8n-RL};7XE}@8?aY(eY&2gi%yF;#;vYs`Qw71mg7kI$@Pe&MZ9ClZXCrM>D*s$u<I_*RW0Ha*U{-j|0nwY|8oClLn|l)+4L}=Ck%jgB-=q2TnF``JjwFlhSE?Knv-k}mq8LVgn=XnLMLEQ97;l2r~sAVQmASFK71o+0;!M=E$GLLHgGju3tgZa^oG80J=6dWrAU^7+E4;6fyyK+!$nXLE{A3$n?V(540WLv$y(49+Cw#{L$VHZhI-Ho29X>DS3p1L4qZuhg&QCZIzkVUJs=bMfCX(ywuSz16<i4!Bs1U|Do+aJkj#N%&=ShQ#Uw9=)=(WffQzIH5LUoy7(;Rl41;IkC0Ivt9oz?7;THS1+{eR%a3f5CB_x-?9GD9WVF$?_@DvPz;V=@$L81Md@H62iSYZEN``z|$u0I5i!eg)jHo`OTJZu9m%z&XVn&fDh4I>~QCXt*3qhJEu3X4fDhRJXT%!gSdXTc&^4^v?t$$9WJ+ziiwholE?gBM{lY$CY{e6S3jge@euz`gJSJPd0|u7&Ne#{RAUHS~BK2E$#jlH^Lrg9o4h#*!QhkH9o|0+y0o3c2t*0KP@?E!Yheu?CjFiuCvmD&tr1F3ES{FW3tQ;UvkE@EIJ1<4_Zi(xVLSg4f^;cpKh>58x9x4C43XPr&zq-;@6v7#dg#%VIgKg4M7#9)ee34;-S$r|>%LhYv}92yeps@D2P(@<%uT-@zAfgya$U0ZQUWaE#<JxEQ~LN?40zE&LX$V|ly;tJC8$`~^y51(Fr;3{=H`pg2~=;&>@?JO`(N<7p^{JK+?Zg`M<x75;>GU?0hSfcP<7gg?Q@@DscYeQ_{0!M^mUhZArHjvzS#``{$J23;gwI0zeK7Ir1s6)kLq?Qtf_nK%ZMu>m&3W|)fU*aBN(8*Gc$Vkhi@y|6!Ck3(=6j>d6VfRk}5&c-XTE;b_B2u-{kn_~va47>u<upM?G*#$GPBVL7Wl5XsbBQYCWlWdJ+@oJoivq;Xu4mb_RV?N1zoP#~_Ml2**h`n(N-hjhN4#(*@6bImSB(K9fOu}y1k7Pfrj{`9Uo04pbxtN2ausg}_SO>S^PP~)kop>|8kB9JelCR?n_#r-yOGz$858i?I;U<!s@L^ny>+vwj!}u27gbQ#XF2=iYIj+J7@KIcg8}KRIg3sZ0^x`hujeGEId<PHUNBAk;kMr?%lDFeScq=Z!dr01cx8X8ehZ{+5#C!2cT!Rmid=Q_;H*f_$Lh=#ZhmYY0c!cB;d;&klcX2<-{rDL^i+k}slJDX3co2Q~8p+r26MO|<!mT8?;;T3ppTQSNzKFNr4!jE&kz9l?<4SxJH<R3q^Kk!f6}|i3y3-u<%{jMIzGC1Kb6f>(I^l&?s@p8)I$<%l(#8^&^y7qgoi1s~xv^MWOU!l3GWTIue&&c}E>2n2>X*MhaLghXIoAn`T;$wXEOVD}#^Q?eA=n#Ec<UQyJaVm_u$U`*$tlaVcFMAsoUn*Z_J$LdxvRB`#d58ku&kAs>x5<QPFd#Slx3}CoUvH^TXSoZOIZyX7Bi#q{@K;7nSGyk>-a#o>fS-eOIn|tI;Z7>#0##jW|cm>E-LStP~7_6^;uN@Wq)O>VT(JoEMl9NQ_NcM-aAow!#$O(aa*Tpxk|4y9&z2@=(;+tN-VFdV_`4rpkrY#>QIX6pkoo+qLC%7U)mP)M&s<>f11bhbG2N2RFe1fjAB-;N)VMx&N^dOa1V^i3$OXd{Bq!T9vzn;Ubp9jIpSb<uZ~4*eaD<Nvwu74iN;fY`qEtbSSPQJU#NTBBd@FDZN&1rI)0w`*FYU~EPTp3=(vz#8*uk8<|C)`wOl}4YvBXt=1F&IS=6d}ji1d^bB1bJ)cjDn`^}G9EYPyBzo*Gb^UmehYFXI#NnT-gzI}q0Mf^Rt{$L)eZE9J>U-`*<&HF2j(6XqxysnN#&Bb*)(RFn!>_r_;QXO<G>}4HvEP5$D^Fj03f)P>q`#xpNx$bl=iyru9#QkRfZ4;t$kC#fC4Q^=_l{@df&wRh`f~Z{kCNv8x_0zJ54gR{vT-)x>s9a+2Id}Ded0G}dAg>#Z<#nU6tV1-Gb<nYht-z>h{?xB^R32FCYxlv!pL%pGYPEc6IrD~!?Yz<Wv8?^>EnQD|qVcvqzqqel(8C*z)5kpG-nt63Y_Ch<VfT8gZ&aSS;C6T2Ud6R6Y9+55jpcQtv8+QhmUYmvh^^GYFHCo-KHhkF{<xE#kta@=$Ch`9n|F09?-e}rs@8FH{knB*7BR%j($C-TjES3N{43`Si<^@gac|o}XYBan<<+m$v{}^cLRrKRFUuH2?(y>UO<#Kii<-yFqQ@R9`0IjMe0Bhs8#jyfYJ7B=`Pl7+akJ<X!B)=bxLNe4U=c&SEdAtuaeLe><KMV_LEJ3X`l6l>+wsTCqQ?Y_x?L!X7~*9agUCHz7X2w$)I44mJvL(a+6!iPse|^v4H_?t^?H`xQ^xnP;%3n&g3A=oikn4$3KlWM%hJ!{Wkcd-8UGb+`p3;;t?#AxO%Z>*EP70^sN03Ih#_8<F^JsbWznC4Ma|=7(PKTf)xIFEI3G-9AIuReds#7g>l<g>%D!1l7IT$-Ek~^EmBnOnEoC1pCd=Fddq*)@=HirPtpfW_j#$|TbHvKNR!o+;%Q$24{@*H^%HDfSURb5NsqCxAWHDFSw|B(KzPck;_UdD@h)vmtkI6E3wN|lM*-MYfvQ~k8@0cuecgivsrz~qF<BY|0FEW*VR4presu8(ruQP6CpD-d<A(s27Iu`bFA63V~UfH*d$RajnA63iBo@zus*sZ!L_fd6xfLLBv$HHFOXV$XZN7b>2P1#4)va+Wdk+;=7?w0$gI;PM2Ze`C<%gP>RM1G!F*|&_yA~t0oRm;krYDA{b@}{!Kt7Umz9hV@M`=~k=_R2nUL@uD%lzr5QTu3bUQFSb8CHGNvEY?o$6Y5ylEBlraS=h^cR2_@>m3`EREaI2@s5%z4QucKtvZ%S-N7b>gm;0zX7WT?Mb3_)sr0k<=S=m#K$l|)nKB1PCJwq)k`<7Z(_AMi_h)vl?)v~gu8j;28TG`jtva-jkWo4gP%gR1;L>93r`>0x0_EaOXsFku$sAXl(P|M1`rIwX_%ZO~R%lUm&Eh~Gf5n0qq+1J&wvd61sWuIBg%06>M7O^RNr*ScT)-&aPX}nCI^-Q^68ZXmlJ-6I1jhCgLz<yv{EaMOCL&n9sx|KKOerdcsf80s8+%LUQ4(#{F#WIG#K66}Lziu5<?w7{PqQ{i|(zsdKJB^FQdddCLcv<v`+%JunMSsfu(s)_=3G4^P#WMcDK4e@h)>`hD#>=9|<bLUea$vtVE|xI__L<{i(Vud^G+q`xrtFu-&C1?sTrAd0?w7{PqEF<0X}m1@Q|_0>%hFF^KQJzq@dx%H<6^Paa=$cQ7Ck2SOD~iI`@M0oj3Kbk92blJl>4Revgk2o?=&v1(R`5isym)CSFK#>cEBDTPyH;<dyjX6ZSR0RI{t9#DEn_*3wsCb(eX6$nN{{t+ui|tbS!ebt@Y|)9b&LY$KKh!g4cDx9v$a?)h$>D2kg<YhkVL)aljrOQ;w$6C$ZS0W6IH#*LA=i9aD~`QioXV(J|#{%5`zT9vzDul|G5Z9v#zbBzRp1?9nm3Moi^(6pKANrq@VtT^z7S$J=V(;-PzyHL}9|?a_F8rDjq2_^_3>eeL9RFGXWvAB}hJdBnC~v}@9iXe{ibvAk~aKlVmtVIPfyby)gCRJQ97h0AZwwe3ri&uA>{qw(Ocy4m(iDaU9m?4xnHz;zo?&7-lfkH(avTj>)mD?JmDDMz>LlV~jaM8}k)TlPsbmVKh*a)IlL9*D-WPjnotgTEiNtn^Gork-@mK8eP%PjpPL5x4A<Xe|3g$MU)j{I6dv%RbSuc#Zt|gv+{<d`4ln;Jc%<r}cv=R<XcqR>N+=C8M)v2E{fa@cPxTTkz=U?Adxp<6sOLb_*^UojrfdZWOGEhTVeij?VUVYX)krVf(rbqqALyZh`y1hV44cjn4ME$QU$iuS>%ytou7-;_qpShxq%NPX10^xV`)vRl4zb|4v=Nj}`7m_jk#{?d9`2Kk@#ZIwh}=zd;v1exZM-PUlDWcgB>w9Q~cTaC_-rH~ydgcj}bClke#7)P>tCe|ItBc)Wk7PS#lYySTm>{SacWtXIVGc>hkFd`*P^o!;>A3;jEFIzRT>4D9J!R#49J09e_L|1dk2&JygC9I&y-#uvjz`ccM1dsXoh%|`X(B^zH1KRO#VFWV;6zDQm=n<9R~YaYo@1e+ptj^QVw&5j@Tn}be`vR?b=ACs@V);d!DIWMtSa=^w*Hoh1((vLD8T0_N8G#k~Ak8I2sesnf!UbaoBeUZF$HbwkIs9_O5PU;-PPehxcsne_lb4Q!2$)@5J9nFPr_wf;XB?oMLWaEutBmF4jp*2+eM6*%-c*(|!;YVkq=4IQ2+84=7XH&#agc=s{<D||p{6w_5YsDn%=jnHO*VAjT?KRWQ;m`E4h<%a+Ha@a3W7rh&6X9A#{KSaIOE$h3esnfP`~+eS*hlsg!AAN~#zT8U@e|EP^&@kS<|m>}v$J2C&CU+<?V&X--l?rsywhtYu~%}y#!EI<44Wc;!fP1GPXrs)kB@A;G5qLkiueh{9I%h<CxVUiql_1+q4X2YM)f0ekLIU{&FLzwOg65g?;QR7rm%0($QssQVque8aL#*gK}X+nPd{%e>{aJJKJ<RGPxV&b#~b8Z>f9AKcC?OM+RFUvor+eUi8HLxHCuVZudB`__7a<d)$5WUANlbLKe~8S8-;yzT_0W747;vRxvo#Su219Br<<$E*Qe&I=1Bfc@^1z53f71Gd&$2Qs7bI6x^cR$kFIM4t{cofEMGY{BuCBMkXorZDlvQ29CiNH95r(-U9EI;)jFuxRdZ3-=rH-dk8=ByuH~ekRr`4RSvNP)&xwBiAL{4C{W;Ok|MC6&pYrd3DE~gGqy5!zd*$D?jOgb=_E(jCt&sgyb^Kr1UybA^+WxAtf8}U@Rkc_5S0jzbyT2;`&8xsZwx!f3Wc)(+S9N}(?6+IWzIx34)o^>|{})6YzmWY^W&hmK{;F!P?yp7~zmWY^WnVpHe^nj-SN2yU`AO`rCiYho`>Tol)x`d4Vt+NUzna)zP3*5GKEEeEzbE#i68)U$=R`jz`uV?Me^u_0{CV;fv)TMH_BgRuvbtyDz{XO?N!xQG_=#m>spA3mhWl|~BjfQ!^W(rq*2kyh?$gvKnoWowQ3Fjpv23isxEall1DlX_SM7D{uCYn<PojS=uz%*te2ZM?e1FWf9M}ZwCdZXpnqhvT*#y^7j;m{;`iWr^9*<AwCx%UUeSE6DraqBuiuh4qi#k6MY<z0n!(Y>3^@(OvWZhMJ-MUAxN%T*me=fLxBH!b}_H82DguHh}zUPMe(b#DHoPQ6{`%!Gd{X}?AD&i-SjTM%Ag!jlI^@(H?DW0(R?1=G%+eE5Q*v}9V>l1FH^>coG^?nqapr5XFo0v~+SY_&T!^ykMltn4-E_5#by-2CWxcqlQHw5gS+)!BL{QKRtt!^|wT>n5?{yU+<f79Q3S?g(@JQrHd7jX(L&s8nr?0wx=rcR4^gck8!cU@;I{9NcJzolFLydbFMxQIjO#uT65pZ{EFF<-<X&UM<KXDj<$+N-+%k58B)Z=DwZPN-am4I2H-;httcvKQ+jwHz053jIOJ#@17T`l{z54sov2fpxOa*9YuX-IuN>>Y~#kjt@$fw(}Hqm0FIA{G?qZE#iHj>_oisTxfYN;^-Aai|a`3&j*6%Vr>R4VIq!a#dx5n?VOeI;C*;R#w2TFyE?RX*V%Sbzdibdsf>fv!oJ70>#YqN8rgPI3wvc8q!#f!Rxr!@`=5X8I!P_!QN}^)m3vCr{?~8VVB1N({D~%RWgMgy_9D*5H#D;Cq!#wdI7l6DeTHl5vrki>;hOsF`yZ;$DouS>XzH^{Q=b)y`uvOak#z~y$yCNc)+te+M19oyywa?N{d2~tM@!qac%<2O`#fd)NdLb#-mHbKam^j(nrHgN)Ww@`cSq8~hpGop?CwbKJf7@Gx88o-bfQJRy>pw#)S@=37WIgvMSYxTQC}xo)Zd8~^*&p^gq@erqRv8#dI&A*C$wBwxz368{qI`e#OwFJdwmn19}}M+6Q3UwpC1#S9}}M+6Q7R~^+|kwO#J+r_<WIA-^BVR*4N4Uo`3(c|BLYRPw4NDelY$<tI6U@#DfENe!c#S1Ew+#Qj7N-aSi_ig1Y^&KTKsDq!#|gLwru~+b0G6E8}op``_>Uw(7(Geit|gsYQ%_KRW~Oi+(+1{9|rq9HjQwpq1@U`nC1Jx-FG)kXrcn*8u|d5cIE%!+D*kf1>{X`}H3jXZ_2?S^vR_`v05OKfLZC>!JMayIhaZx`(Ytu<qyABed>e>k+K``Sl2`d)Rse>wbPc!s{Ng9&ldE^$4wd*m?x(ettbd>mIfq!MdMckI=e@tw*r#ay_!46_kN&dKl0X20%NK?H~)TgZfaOWO;ByX{ZX#Nj8VeAPE}6K#~KY6EG+aC7~=-fJ$&F)P!Vc0F9stq(VBhpv$y@tKnMc0^OiD^o8r825=}vvJ}*Y5^xDrCRrISf{JiCG$Yvzsz76?3$;krf~L?OszDu+b)YlUgI+L*<RG{L`ayT-O0p~50BO(>dXVe^nb3#QZcDN)^oOh9O2{CY0oPErDUd@l2Z}*UC<hmlyck+Tb?5*tk}g0P0(mf+<Y*WHBjH9EPjWnrgRxKmQ%FvMi7){s!%UJhVH)JaC>Tn|JeWbpBsw2TIv=LPESOJnKFozVa1#t8ISg`PHVlU0bc}&QI;PV3aMH730o(?QNiK#v;7(Wq_mI2??uMnX9PTH1KdgZJU=^$;xf&jXWv~ctrQ>mUn2wcnek<u^@DMx#>qxGH$6yVtg@q&+!Y%M9+zhwVaTnZ6#{+bJJLyMZ13V2|NN#~m@C-Z)FOqx_o`<cl4SXbhumfHKFYG3{8(xMNU^6^P$D8m99UeM=lJpC(3tol2B=^D_@H*^)r${~pPrz%i9yZeP9Bij!C!KF3{Tl3pci;fY1Moh400-d+$s_Oyd<=)-bCRFKXK)n0fa4^O!&h(!K7{>r`~ct3ag5IQlRgAr!?$pf<VpA*zJnj(U6Sv@+i(Kjg7@h72tK9bOFDm#^a=P0euY0s{sF(i?{E$ff2YUa@D~6U$G@OBax}06mLXXNFT#J|Ec`-8c`QvwF*^SRN|P*w7h^>%MUQfL30A<<a0xwrhO&4H&d~8EFl1N~%i<ZLvRDbLV{NQ~Rj@f$#X49Qt6@ECjFqt=HpN=#!fWv|ycAQhJ|<%eY=RBY!e)2{w#J&+9@8-iGcg-4$1AZFHbOUEgDH3wcEB`jiybiwGq5w7n1fyMYHW#JupPF+PS_o<!~WO@d*F@O69?f9*b4{a2<(Q#a1{2#vA6&SU~e3Uxp+NJ#*sJ#XW(ee!&%rDZ^i-~h=n*2hvF2RiNkRk&ciV{2XDcAya{i`2{;~a!|6B)@4&e@6>rD+I2#w@owyY5#bvk{*WnUeiTC4O_yDfKMYtLt$9wPz+=chy-M9fC#8tQjAH#?61zd}d;ET8%cj8mH0yp9__%J?;+wf7`iXL2#FX7AhBzo}`+=Nf#tN1)_#@BHNK8LTN54YoP1XhxLK=K283u~~t>=IUk9{*r1_5*%Q@?$K<-p9}IH+-KS-{5gPh4t8RdQ@V2@NIkt58x+w7(d4^@dW;eKjW|X2mXnS6=$Vb8CHQ+Vbxe|mc$ycFK{ouhhNa+Yut|q@d(Ky_%0s8lX!;Y8T=G~!SC=Zl3(FzEXR)Gw<N#C%Itfr$?B7=&wj!>tU9a8>d@nIb`C4DOG#eJ{>IB#309U}Mvr7xnsN3QmZrzW><#=KktDKxXt0m)Ly{ljMeG=sXJ_#kp2at@5o^j)StEKhXDKX=<&ex_nJj~4GmE6fTCyvd$*v}OHEYeXn2R;0qXWB&4mX`QCY{CFuxnUHk{wxl){b4vnviV5u3&9hL)MIrbk>57R&?HsbX(Sib!WXv_GUd<FV=?*A~}flXZ_efHk9O0HkjSOhOm(&N3uLNfL+JB(lM5epd**gyOJKjhO<#DpJYB8!)|2bST~a0SZ6kxbz(i}=*zCBV;G(HAU&EDvPo<@$?0qgo62Uec_int*=!b@%WfrkE4!J^XA9V!B=2Omu{mrSn?T1>b_X4|(D?+?bJ*={5nD!b8M})uVRy5MBqy@*Y%wcflj)erZlYr$olhpcnBBuxu!l%K#O`Mgu!q^>Bp+vwvPalsYy-&+Y#m$Ao@CFEe1<*E*02ZJeROPPo9K9g&hI0=hHYe<*$X6JV9&8<+4F2A$(8J0wuLQctLRwG*3$75ov$Ljg}umjuw5i~F(2E>USV&Ne3QM#US)5vw@JRu_OiFwe)a*$57@ixb@noQiH?ui`*iH1^Os1!&fa4mvO^>fv5(k6_6hTl^sw#h0NcjAbnIq(=y-?Dy`&GY!|WLQntj1OWxuh{*thIEc9eb3eql%0DR!ED#m=${{2TT;`-A<!PB6xQWk0eK{0#evUBtg+<@lfMIQyFcKgl>R$$w_W_{IEpR+^XR=U7=@k^jT~VwHJuj=U-_!wp`AU&2fAO1v7c#gqAE{8FCAYw-H~a$b`+<jr|?-h{h&9iG9v@VdM<&*WF|2HfN+yb-^Or}C!!8lJ>E@oZj?x8N;#V{Y-Qc{ARcci`!~9q-Ju__e$%zmn(h?z|0m^PaptZ^e7?j=U}J#(VL8{CYls_vZP$56|U8d0#$^-^j1yBl%c9h>z#D^BZ`7UdZ$K5I&uc;lueHK8}y#^Y}o%kWb`;`D8wokKi--Tt1r5;<xYuKA+#lC-4RQ4nBoX;*0ofK8-KoH}jc%F~61H#P8&H^LzLzlB@WAd<DOsuO_*gKgb{AkMMOQ*YU^r8ori4P4a2Jfj_~Y;#){=;hXp~{8|1Y$rt(a{9(S5FQdc5U!Y?%f0B;JY4l+l6C+O&ZROjzkED<9;4g76Urus4U&^=hyZF6yJis5NV?EzU$8$8goyNq-MxtH(RlbMh9{xIigYV_<kbH;l<8SkK`9YEg`3L-cet;h#d4zw$Kjw$|=OjPppYfyo3;r$1Z~51JKYx?ILdOsM8#<2hLv(ydqx)%0j2t5RiXZ1ENuK22^Y8eNd^gG6{AGTE@8qx1@fLrNj*s}KbbLvpCumHJd`k2)Kh6Ij`3L`v|IW{GFn*`UU;J-+yDwq<%}W@D!Hwd^#Uw8_N*Na!WsC|WD;Sp;<&26(b&}PMD#kzjEdPa$T1Hhm${VHWC`P0I(3lu0O<dWiW?W`erbkVqhEd!2mDixhPyABj6hA}9pPU)YC~1_Xqmpqc9cS#3vP8*7eWMY{M#kkvL!+^gLNdi@YBV!kMi$8|Bi%?dG7UFLx6#7LF<KgJNVYL7qm^-$(Sc+Kqpi{0xWcGQM`xoQ9j%Qk>Bykb<}@Zot|Yp~Xm4~S+12P|bTqmc^+?t;>KNA=Nk#)Yni#2cWE&<OSJUXVG$uw&qV7g7qd&?1MjxZM(a*Sn<PF9^V~{b}$Rn9&3^9fp!;LW{#~7oGk;aWiA<04`-xz0%H>Q%DYD_Y6jRD4Wbj&fP(J{doOUDQr&80ChGL~qfF~yiga+WdOm|@H|dXnsEbTeieJ&e9|TyG4cW3*8~$7C9vNn>K9faw1LP6RGg'}
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
placements=[('t','camping-cross-pole-domed-tent-01',(-.90,.45,GROUND)),('s','winter-fixed-curled-deck-toboggan-01',(1.10,-.30,GROUND)),('p','camping-backpack-01',(1.10,-.157,GROUND+.038))]
def rigid_point(instance,p):return tuple(p)
def stored_point(p):return tuple(struct.unpack('<f',struct.pack('<f',float(x)))[0]for x in p)
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[stored_point(add(p,t))for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,rotation_z_degrees=0,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values()),coordinate_storage='Exact IEEE754 float32 after translation, not hidden deformation; native versus final GLB bound unchanged2e-7'))
base_mat=len(PALETTE);PALETTE.append(('SceneOnly_PaleSnowCampFloor',(.70,.74,.73,1),.97,0))
v=[(x,y,z)for z in[0,GROUND]for y in[-2.2,2.2]for x in[-2.5,2.5]];f=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];emit('SceneOnly_ContinuousFloor',v,f,base_mat,'Single scene-only finite equipment bay floor, no extra counted model');FEET=['SceneOnly_ContinuousFloor']
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
  assert abs(bb[i][2][0]-(GROUND+.038 if i=='p'else GROUND))<=tol
  assert -2.5<bb[i][0][0]<bb[i][0][1]<2.5 and -2.2<bb[i][1][0]<bb[i][1][1]<2.2
 for a,b in [('t','s'),('t','p')]:assert bb[a][0][1]<bb[b][0][0],('Shelter and supply station overlap',a,b)
 contacts={};floor=triangles_of(FEET,vertices)
 for k in ['t','s']:
  tri=triangles_of(names[k],vertices);mask=READER['np'].max(abs(tri[:,:,2]-GROUND),axis=1)<=tol;bottom=tri[mask];norms,areas=READER['normals_and_areas'](bottom);expected=float(areas[norms[:,2]<-.99].sum());report=READER['actual_opposed_face_contact'](bottom,floor,plane_tolerance=tol);assert expected>1e-5 and abs(report['actual_contact_area_m2']-expected)<2e-7;contacts[k]=dict(complete_ground_contact_area_m2=expected,actual=report)
 pack=triangles_of(names['p'],vertices);deck=triangles_of(names['s'],vertices);report=READER['actual_opposed_face_contact'](pack,deck,plane_tolerance=tol);assert report['actual_contact_area_m2']>.001,report
 contacts['p']=dict(support='Entire original middle deck batten; finite partial pack sole contact, not whole footprint or load rating',actual=report)
 # The unchanged pack underside sits above the deck; its x footprint remains inside the full batten span.
 assert bb['s'][0][0]<bb['p'][0][0]<bb['p'][0][1]<bb['s'][0][1]
 tris=triangles_of([n for nn in names.values()for n in nn],vertices);rays=[]
 for p,d,length in[((.45,-2.0,GROUND+.4),(0,1,0),3.8),((-.90,-2.0,GROUND+.40),(0,1,0),1.1)]:
  assert not ray_hits(tris,p,d,length);rays.append(dict(origin_m=p,direction=d,length_m=length))
 return dict(instance_bounds_m=bb,complete_instance_count=3,distinct_old_models=3,new_reusable_model_count=0,whole_oriented_triangles_and_pbr_retained_before_float32_translation=True,actual_base_and_pack_contacts=contacts,selected_visual_clearance_rays=rays,not_navigation_or_full_space_proof=True)

LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate(vertices);result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,.62);ORTHO=7.4;WIRE_THICKNESS=.0006
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
root=bpy.data.objects.new('OneWholeSnowSupplyStation',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole scene horizontal centre; continuous bed bottom at Z0; three entire unit-scale qualified instances';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 # Preserve the already consistent outward oriented triangles of complete source meshes.
 # Recalculating winding on the returning thin deck flipped its entire shell in R1.
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
