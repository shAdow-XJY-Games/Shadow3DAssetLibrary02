"""Original whole empty handling-frame and separate equipment-parking bay, two whole existing models and zero new reusable models. Lightweight maker SELF_REVIEW; static composition only."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='pet-care-whole-open-aviary-and-table-carrier-staging-scene-01';VERSION='1.0.0';TITLE='Whole Open Aviary and Table Carrier Staging'
DESCRIPTION='One static empty aviary equipment-staging display scene, zero new models. The complete qualified octagonal openwork aviary occupies the right-rear side with every bar, two internal perches, whole roof, grounded plinth and fixed outward-open gate unchanged. A separate whole original worktable stands to its front-left and carries one entire original empty vented arched transport carrier on all four original sole pads. The carrier is rotated exactly90degrees as one unit, its grille faces toward the open rightward inspection side; the table and carrier remain beyond the complete aviary bounds and gate. A continuous finite scene-only floor and visibly empty approach separate these two unequal stations. Unlike the existing wash/rest corner with three independent floor objects, this layout has a genuine carrier-to-table support relationship next to a full tall enclosure entrance. All original unit-scale oriented triangles and per-face opaque PBR retained before declared float32 rigid transform; source hierarchy baked and normals recomputed, not raw GLB bytes. No animals, real enclosure fit, transport suitability, gate sweep simulation, care procedure, hygienic zoning, access, load, stability, welfare or safety claim. Rig animation and interaction not made.'
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
LOCK={'animal-fixed-octagonal-openwork-aviary-01': {'bytes': 127528, 'sha256': '579937d4a29e5169b2dcd163da302296f23fe671fb94069ba33171e9ea5c31a9'}, 'interior-open-worktable-01': {'bytes': 46720, 'sha256': '78ec9cdb829e12c333ade0356adee759b8f95bdc7f037fe93ce946b0a487265b'}, 'pet-care-fixed-vented-arched-shell-and-grille-carrier-01': {'bytes': 133572, 'sha256': '1fc927c75450a7ff78f0610ed808f565328d95da26f571c5d84cf85cfee62168'}}
ENCODED={'animal-fixed-octagonal-openwork-aviary-01': 'c-rlq4Ui;9b)ZXPk(QNKNJv^CWTa*ULO(sbmA_TB+MQl$rIps!ACeGYNnUzqdUsozo!RK_S+SDWV1tbR&KQgjgAZhL1emid6F!^p51KaSu)~%)VLLEB|DEw6!T~zNIq=!XIk<bTx^gzVC$lQEvpMZe^eU$2Q%}{)moHzve3_M5eR%QSeP>2dboD=;5$!tXjOe@Xx$}<4W}4k@t2eXrv6;iIrB<ieTkg#4ocW$3o#mzFZtXB!QoC`nwY1Rc)b{VVvv!<sXWMx)Q=d8B>U7)7OK>vX9?zVt&vfTOz|79Lpzh4h`yZQGY958pX70)VR-ai~UdaEDkq1vcc<O&2n`ynJ*J*Z9jrrxH$Cj5`OT7b~<wd;q4M*U2?QpZ#sx2RDEj_Z_dAN44*{MC!?j5NeT!sUvcWk-6)a%w-M-R3Z7Fr9n_EN2Pq*X&<i>+R9`JoPIvmJFk+Ug$3RW0<p1^%3ub6=~|YtJ_qZ)|o5ocIDMMoJZ<FPvhuR5A9#DaJ|_<1d_Iyi_q!rPy92{K#^r{pj*iuen(3wijBpPP4sOdk8dYFCDHm7anTD9oDNIT3KAI9b4}9y4Tm1mTL>`?)>u7Qfs~k>SD!ehdb>>sA;#?S?Ot7iZw0oYA&@F$!*Jzv^x7h*xgXfX`-VX(ed{7!op(fG*dDeQS$Z2j=3B1&L!}s#pN!PaR~GQWseuGV(`jbL!(#rmUF*c#5SxomlkR(s6<}T?)KUZ?N04rtM^C?DgnZ}wRX4GobRnbA%|PbM_awli8@rdS8LXKpzBIU_vUn@dfqYf^si!8QAPUye-%kwQAf4`>PRZ;$TvV8X+<5y2B;&esH5Bfb>tOwOiq*Djf~_8^mNP<$Vj3<Ps>DsjAROQgJlY2BvqgrFjXK~MIARlu0Z38I&Oemfs%?kZh%~Y(uz86fLwvHiaKt9T!He6I-V}M0v*W}*y)%n(2-n$otC)*9my5g2Fn%bNUp#(V6H&3iaKt9T!F<Eb=&~C0wWc5+yJ=(qZM`B0J#EV6?NPIxdP)Abv#{i1vZi^@Y69@U?aH#KP__wHj*pw4VEjgkz9dqz+8c46?NPIxdM+X>bL=N1x_mJxB+qnPAlrT0dfV-D(biaas|#S>Ug^33VbA25T|3Vz(;Zgaa!gId?Z&88!T7gBe{aufVl$CD(biaas?4r)Nupk3W8MBaRcNEf>zXV1LO*VRn&0<<O+gU)bVu56~sucAWz3!L5$=I^0dqq#7M3nH(0J9MsfwY0dobBRn&0<<O(vbsN)966(p&s;|9nTB(1392FMj8tEl4!$Q2~7sN?C9E69;tAvrDgK#b%H$!VD@$dOzj*<iVX9LW`u4VWv)tfGz^AXiA@iaKt9Tp=M9b=&~CLP9I*xB+s7gjLjW1LO(`uc%|<Qpa5N!=2@oB~W;Fd1?08B4~Z2Hox3i0!6Vut7Fx$t7|Xi-QUnQ&SUM~{1K>XXL<Qht$U=kxTvdmDoe<f+nWo$3uMMGyl&E_8+qY%OKiH)7hbp2rW<?Vb<1qJ@fTdTG`8s`UU=PzO*i?%>qc$5ImI{p5JIX7;)mLAfr4=F`7D&ys~zmL7Y;*gZ+F`V7f;lRj2#snXt-8^Ja`Y%c-*+&?X?$M+iQ2^vH4)D*?~*ywNC5k^6}=uMXb_NZMjohfDe`+;cwy~0RD!8kHBGQmoOWy;679lx4+*F3f`FO7jKZ7^2(YL*P7;z(>v0he;9O`?=_bWuPipPi(Sfp!xfzqv!~uMPy?@8knuw6aHrMk)|OX#k2E_A+iNJU(<(ak;?%rL2m63=R+d+~g>Aan6RVV<y)>|6tG2KVl|R^=e;6wah>5{k-Qo0R`>1XKVX(lR17+?64bT|-PzmR;>7foNTEqLTwYZi`^d4Cr+>~0gg8s{p!sM-;*LY>=5ROL|a$7Z*=7(Bpq;uSdrQD1*y)7@vrIjAZ-x8tO5p-KT-kQbxf1w6h(EJhYjS*{Y3UQ)a_%OI>x0O3odr+t4V^9-xZoOXD=YN9XHk1SIzt}q7TI{N{X>l3a3-hp6rwy%hXmPoj`#hXH|FB-+ksfz{amBr0nJ&J(rF9o79B;ger%o03yDy6n)LmX|Lnwi}^YHQ#cwEsf<aKZAy#}7y%Hxi1wdG@~GWjcVuntg@dAI;A(`_AVVzgO2q1R?40k~6@eM?@>UAY1tZ8*5w2VthwK76D%d#E|z>J9f;d3}1Fl~xTqzz#O^;9ffdQ3-9{Y95D}Gg7@n&F*}=iGj5?pWlICAE*#m0$O(wBy?6FLU-yoU(~|VIv8F$tz!enSUGyI107|vHs4%YKBn6s8%Z?oMeWxNao0d|h`5JxJIo(xFD`UiOEWv~kL#pP>#WY}qAu%6J*{VT0w0n(p>@LQgx86v6ImxoouqY=)oEO(a1E_fR;Rp9MV-nzP3knQ)2z<oIwN%kB3YgBIums!>ny3Ww9c|RkL#S&IjwUjk=MDXb6Mv}ou_r4)kRzvq%LS(u(|++L|w?bNa`Z3i>xl=x+HZ;>yp(auS?KZ)@4$cX<cUZB(B3a9)`Iv3WPxt3_>8+hm;yJS4a>c4})|EvI^*Tp+ka*48aa=f4C9Ad$Rb!y5<}C>z)p@7r>UyrS{S0;%wfn&aV0NtQri?HjlTP(B;HrraqGg<pT?C?3o5{eVTm}eBAB9Jve^=x(*oO9avskJTbEq{iZ&%+-ZZS99U@fR*u5i%Z8h2-EB0uXL_~ojjvaOMpS0d=^aFO?+!exwQxNQNssj)sN@Qq8o&;8t~Fsy+RVEEP_mQ1zUlyaY6rxEHjh0p(_CmC>$Q)!9+=q)j=R_e_k3V*<3Lmb7dL*s+&PfHvTFE`C*~Jh-2)4)rR8>aSY8Y7mi(g!X7;{m?`=2V^S}&#-ff~Kaxnxv3qI)`fgWrj|AcG*f8Zz-H@JS^{x{xy)8O*s?bag)7MmxaQd+6^=fysF67QShZh`xL&>t&H-&xq{hTKdu_zte4O$?84Y5pFrh2<5<0q()Lu3A#b!p=OO@4aDZA(x6dPWQk~&CbKOw|dP*u=KHmog5e2^LH<=96qwt>gG;&u-SzycX7G15A2UG7`s2-9!s9#zeEy|5)OAAe3s-NWho^jl`-4`_*p#oN3%4h3~o(=S{KDAf$?_SZ`e_Vp88l0E+<l^8H;0a5<`T&mY9WiahAFZwZz=zz#AYsL8t;FE`qywR+6OIP$lcRp7425DUzfqVHv~{W2KBWN(&<i%7~;Xuc}dgZ$WMHUJo4g4b9Hcd)r43wmP1b;YCA;OvYSttOpdI>moU235AFXRTJ6pM;<jBSSuAW<7p~bMa}ZQ0K@))+gG3ixn~iY>lR3cmwX$E6ph44l4Nm~)r}1o)Mmrd$jSW9gU)UEHF@UO&_QiF?W1jsR)e#fy<Vq%5bB&)>8?BP*?;f;JMYNLzT?ijZ@=NTnVkfJKpV!V^LP$Db(h0QCm%$!mcC!kxkPrVL>^Egb1zYxDp3ZM$lXg!PL-GjlqlRw%(Qll9g8%*x6Qdgd|A?3iBvBUU%zvzNMa~*<O!sEnOrMV_?0>QJkh;KsTG;{6&Y|_;;T^Bip_@FGp=gTfP0f_jY?@)u^u-l)nWqWVa0mfrBn+HRE8DnajQ}-I?yz%Sm{x$79v<2R&3%C?lqTUelA7F3{6aPCpP3xxM{TXo~7f4CZ@#+miU!9W@utsj9{5xkpZEJYbgUKehnHBnsC$DTCpswSdY-ewJwK?uwp$z6W82{Ct<~UgeI=J6wktn^$1Nub14z%QXZj6Xf7rET#AhunuO*~V#u9vNq6Zz%f<~&LhElt>R0BNp-E_cjg0+@3<yn9>uaQ6U&8`Ilhpbf$-|2E2u)HS*T}G9JwlVz+)1Wk#d?G$sku}VhZXA)ni9>Wl0cX82u+FRQi-2S@i9YFqPbHt<W9H{qx7ET<A$b0>u-|Gugoz+Q>yhfDe)^ZAT*^~Uz7UvH9R0RrCNWJim+lmLQ|@xFKH51tVd`{HFrw0uws4YUNo1=NLaBRp()c`DhqTekI<B9E|vMYlo&HKWtux>L++HN75A(dH#B8KGitG4q2o?A#rmXLO#KQCnQn@iUa((>BLd<RiG^OU3@e!V6rAV<r(p$ipMrJAB5_#3!e_!(cP>K13YI<v>&`_2oh$JvSa&Ys=Uj5^d2!vbNa{5&BgdW@C%RYB*ss)a!xbHR20;A^4GCBJgfa1)F_t0WN}n<&o^!@BBwXo}#>8{hScZfvecG6K&Kt{+aHUTi6VI7r84|Aa>0`nIoy#X&G2OYCpK~SShAXB!7E6bpaAg%YaWejsJpIA*@HDbRvEv3TeG-`r&mudN8WOSed1T@_k(`7?EPW=KcuplJArVWTOD3L^$w^4W(r1&2=X7!s60!98Wa2rYoP<OyG4xzK(7Ajfme8F`I6K$6ZBQO1>Ru&Eyo!{S=yT^v-JK*EvqYa;R_cBv*_b8z+^bS|ASuQy(dQ<Wy64Db%o2U>PN{p29M^MvZp%dXoMc?j@wp!p-E$H@&oS<}@hDn%p=5Y*P9iH}fpHIvN7;G~lcZymZQOn0p@5zwr$b3H!EI&bh9BKl;;~9dZ|~u0<+9oA^35F{#p`W8JiScPA-hxO^1T*G>Fu5lw|kmZlyBY@;a<2t>q~~GeMv?u3b$`Z@K8V>r(}FsfuZ3yJDGoVa&sR3*j?@n<Q`l(bg0$2uibhiUj@3h0p#8j$6ELp9>3=#-)1uS0-2-Dx4>ny@pcw-1~+)dM8XAyteI@j5|OXAW+?|ZNb9&Pm&TG&nMugN62@@pYI~^=Kv94MF)?G(xJniT$Xo!;;*`gbK7xQ=uGq|dH}4(nvDGU;sw+@-IW=9*)-K1zJ;mks?7iW(8}42wfO!~@3Wy1bguxcnEM~Zy#9+ZJp;-o2mT3};MCb;j2?`JyPo$LCubEAl36zj#lCg|KuU=t79%e$}VF8k5r#t}Hej6-6wnO`8G=;MW6&X}@$OL2{Atnq=$WzM#`Rz~y%AgF2<dRjGK!%wh@i76H=mc>lWs)RmOpPXh%s!Qb66oP1+(leB0d7w~34&(=Zp1XTn1HZc28&Y>gV~Y_8>C@2$UJNiXM;eHh!hfQsD#l5l#3*Tx}=hUsj_s)24o<C@i>D}!HC5Ml;$!-l8~6fJyR7;;xHo+;%WuBOX2?Jpg!CN5Lxq018K2q0wS!W33PJt_Jk!IYLKQ0gblF6nh_wJraa{+BjXSdST2FdTtLFI7z~=_cLxI>p^U+eB!oy(S!DwnXag1+Qwbm6ig4#Ag%vXa_TtRbh#-LGMx=0OrI1_6acn38Z79dL0NqY#Zh?eCr72H64M4$y`L>)yQ21CT={N>R0u7M58-S;{vj}<$s6S*4xdn(AaRHh4nh<WJ;4~IYvjCU*^=U$53PvN?g%Up4t0Yni0hs5vBJ@fq0&Y(DEF)F%lw^UaNgR3~QIBXO1b7D#sX#ksxVhC}M3JVPqq)K7pmUO%5e38Raj#cGc#<-U4Ta1l@HCe2Us9Fb(ZE<lnY#rf<r%nn0?Dg@J0LMz0EW8++=Va-VLC}Q3qalR`V8)pR7h$u0MBv(EEXA|F-fZo5SW}%;b8!{hqw@snlMTLjRt^#z*5L4n1m!#aH1O^$*)gw*PrBhE^D*^%_VROv5CN#nOB)0Fgc@%y9pq?Wk~|L7X&~Ute8UyO9W(ADMS>=Q<9kJw?V>l0TOCUA&(ap8!(ZJ5CYN@$YH9|QyQ3?(ahZhDKt)ASxA>~9A`EG4h3O=k}?>Ir&6~7beVW2RFGwmhS}}|xQ9>z_)H3a0EekC0SnB`m``Q~-3TW*#D&b8#L{R2xXqysX%<U}2{Ggfx((7?0E}{CnP!R21Y{rq0xAaqF|9H|U@&AJ!4L*bkVFa+6Nx*lGfQ>~Mxu}yz#t9#PNGKx7<Hip2ql<XP;+)ViybqhB$UwvdV?gXx)WGnJY*txz%K)=Xv|K1jA+PC{cRYSo3S*&0;cTL#{h=x)ZYMsnHi6Lvhz4M0Hj7Srr5?<5=#Q(TM^^j4uprH>@<_P02WKQZPM5lOd#ImA}EEB1Ec7w?34#ioN+o)8{nh>4D<!|1|0G)h&74ywE_weg^(CC3-GThGq6B2@JXA2u#AwHW-^ob-UOD7VFk$EKn4R7W{_qOUO598I9%m&(pG@J7jnoXCK-+<5;lers6Y{zj&TY@JW`cm@W8Oh(@7hFL7)T!zzr?Il`}eq5wOPv5&5)z0x5f?5duS_h$n3X&SRc14)+7Wv|*gv0s0US0fRcpX~IS2OsEKqjbh@lQQ$OZ0%ML$QcO9=FanP2DD=1ql!7DGDjNg_M!_dL6N;TY;~YJiQiu*R6~0rUvjoD5lyM41l`uk!X;oYlfpJmD&}>sA6P*h6w4y27^fzMQ;8kRkoD21|fGOSdwtx&AyUNLqUBLtin1yggIZgA&aGqmVl)!Qcv4G5+5LRh|z_F`j6P>}p3Zx9@vIxlpRFrv7VStD<MiJ04r%6Jx%3+5L9J@*}(TOaqfB-j#QCTJj&l!CuvQR{li%4S-MboNYMF!60$z-C_nV^401&mIi1#v1y5bya+6v1;55?@5eAZe|#L0~+T*+l2Gu>u)B6v50u5F9XgPHICygyB6%AdsCTaPw6TK9j(Jm`wJ;237zX8^#F`G6)VGy`OBLh%^_$nE-!av}!gl35<vdo9Gj=SzIrGuTg~hOB^yL!ut^!$`HAXgy6#+=w+&m5Ev2@kC4dYeDO@0zcP{w%FTHu)B(ng3{K7P1%HAj`nm(75M!nZ$pHuvNy<5Nrd9o861oB<3C%Q<G{lsqT+`Q*mTc40kbwi(G!8L?A>Z`1f+gehvqBm;f=xX}unc=WMzVal76mp(7aC_0=V%l7Y&gKu3<bd7d5UA%#1>m9%_WdDO){BPuV)Gz!KNM~SV)2)u0o~&6@jrjWNMx^AlX0w7Yt`GlXOx>2pqwt9y5D{fchLCWl4rz4fizy4qd>xvBn~yES;DU0%!J8kI)EJEneT6Na%Kjt+TaRVb&;OLUss@jalrq#&5JSeeJN`pC)65EHF4`)N94-=#A}bhV`*!LS_hzj~Vw_`aBxreXX#*mzj_i0s~|weOAyLrYXH<I%kcOr4yLx%mPDXmWJk^Sr%eQ&$-T7<7{d8TqlV`7ZArJ#0-A(owKG1(+SLXk~nk;aqP3LV*TLMZ+JUv7$8q(cncj^s3ClISFD?<@SEzGHB6RFX08M0p#$yUv&CX`(#mhrYt}GrHkoNJ5~rbN@ClOZ<}dvwKxYk8sFRriCE?pFe4^yKscgTw@L9ub`a~wfN$^e!;u9v<J=O4gEHZ0&uritFB7}rSN#YYFM;~zcJs_JkJYt*7BQiolgCy|@lBV^UJ}W$D&5K0Cmv|Bq8YM{<Vh6u9nzQCrp23SW2@Q>rl!REpYn|q-aiM4ULQN97|ASDU2)S-4jo(_FS;K0c$t=bpq1!+R6%)6Ebzzo=9eh`2k<iT`geDU=gmsyohar5|>5<SaA%tcVH-vT3riUSXS8bBejUj}Qi5tSchS$RqzKeJX3*NXp`CwVHsN2I7zN@-P=r$3;CLAxz*7&;`!hexJVWHuYC6k`sEZL0gIJ-H<Ze$i3EzMg-{5G}66Q1Dov*cv<wTEsSA)HQje$&qgliAxIx@m-PKGE@N*=9u7@v8rJL=w7dgm5|8>5GzmsjjmZ{u@(C=)Mu+zH!8DGOKKdvg>4)_ZDRmx^skxc(QYwC41Ffr#AgJtCP^ZBSg@N&UBZ&vcPqs+xw*jBy{r#5qz?bJxX3(;ri6W``r~JboU4ma>7r+N?wEF`Vh?jH7Fu9J_?`s$Yh!hQf$zUW%)`2=<2Z&kT1vh)~q}S6-?lw3Q2KwNiw`94~JU`zI`i!0XZ9d*SHw^T5${)(9NI-uyl%#)2eTZ&;TiYmL`tY!OsdNJ5I(5GBiF)=lBR2FAkp>4!~nZvV19)!3rdWK8`|;l)}A_FJ;qr*TH!S=7;#kJw|Q5Ku9*28BK7E3Ry#?8A2nZ<dZc6b_Osgz&sc-?u^Kx_1{irKoO8UrTET0F0iYq>@8*Rd$QzY?+JXy4|yY20y-3t!q~$5roaUg0`mqKrYAT6Nh^~l85$$y#A9TcC0v8#IF<;Fl8H|mxz4XW?~GZ)%{8H0BMA+Z37xPZ$|9w!A;t)mNoc4{e3D59ofr&|QgnJ42ojub5{zO!ppPUm9qffmAWMQQFiVSjWBAsHGYKv)in$g{pyj|4Sb2P5Wj!B&Kqigj@s!FWtsHG9p`kJf-i%C=B*>BkZi3vBah^aXMEY71BtUb5S8^D@CK;AJh9yHM1FQC!@Kj$1jSFK0m>`u24!C2yx8gi8Cvb=1lrCC^4Tj|yB|$+-hc}6UU1A74_;3|QVfh1TI#?qvAf#aCPxF~Df<sx3uf3I!o>v*7YOf2{qg((fcd4w}rF?dp828(-{La!Hsw}lPZMTtBjFHHOZZ9EK`%99ceeDcF2+n-sL11qSpX3vnDGcNoO^P>k!7x{*LgIV6VW2)d6}nDDB6AUNeugtWgC(<QMw~RkXWQVWm1YptwI~-*5tj1F(kdrP0!)ebp76FF!MVn4C=!ihy)@K%S-ADG*fpF%Cy%Q=A)XEH8KQQo@R((A+u>(vjIjqCD#JA%d^knWug2_<#rRAJ9GKt)R^<y-NnpInDqi=VIvA_swol_z#v(L<dO@d;oBsw$l@x=!mN3kK;@n_3oeNPNGN&{d1fDg686*@Yk2$1iI3tytaee1eZU<gniE;tLJMe=}r$p#qM38?8!NC)~)@`k&!@VQ;w##(z!JUT=bz8ms@4aT{Fe0uup{LZTzBd2B^=eF+^@|1OO!~#lr)bI30L3#V1Fj}C?|;U=T;ST&@h?x~pf-!s5X-@cCB$@)wT74u#s?v$W0c3^J1mai0z4KUwTI}Q2DKX}LG8wQP`g1t9@1`*;Rm!E^ot?wCU{W0K{pc8Za9$?aJi&G?IuM~yFm{cV!DLT5Yr``gqRL8h!E4^cr@U0+~^Q;xsV~Ig8@s3>9Rp)Jm&qH;dArx@7GKOwOf`1wHt}!poSxm;io~@%b=!%Q3nr7ZXi<)vL6vN$bL9N49e}|EG#!<X^{P>OoHr3GZ|z*MuReI!bDhZ&C;;snv<~Xnum4w_zhG+_Tye1{%GukyJxh+XMST77S?=129Axgu;!CAtodME8Pt3-3Ch<<5(g!01fMenT`z-DHUhn8ko{5`l(dmFtoJ8rVE3N|cK=ym_n!rJ|5;e~PvfxepT=R`KaIV*|IzS?uY(Dhm7;_MH6JBBsQD;K!kUl9Va*4vAJlwQ24!!Qra{>oWh5wjql^b-Z#cUaWIrAUWp9*+b^o}lEXaO5tox@Ttox@Ttox@T37j4c>;9<>>;7?iHejZW$}DKAjpCP#hNz#=u;xodSo0-mSo5VMtoc&T!=C3PLD?J4;-Kt};zpvd#{)sx8_m+7?2W}?-9J93ltI^rb^rLS&q2>uNLcsJNLcp|y?0Re&uCcp&uCcp&uCcp&sbRZ&sbRZ4_60u|BQuo|BQ!q|BQ!q|B(F!^&d=xb^lC+b^lC+js9`7RFM5-*yx|hu+cx0VWWSRgpK}L5;pqBw_60+F9{p{=Wm}0c)*^n8~pn{VNb)le|*Fq)O=ZB_n!rJ|5;e~&*QM}pT}X{Kaaz@e;$W*|F{V?$bKZO`^PmJLH46z-9M*c-9NtfGRS^3to!FItoz4pH$nDeN#G)zu<oDpu<joh`2^XIhjss4gmwR1gmwR1gmwR1hIRj3hIRj3hIRj3hIRiC{lfZ>By94ZCt=V2c^dZYpQmBZ{&5#eK>Ebfb&vkN(kGq;cK?}I_n%L-4PWoo{ja+|->Bq%eZF9Q`1&Nsej*NAohpde^3-(w^};9ouD_m!EtnH*-RvFnDxZ0!@9VFJ(R<KJO|dTgGB5uVUg3BB_0lVR=3|YKm8P+W{&}z%zTRu;$@=RPuVwY?@4qx%|L}EfXG5{8K{p_NbH~XCPu6Om|4J0yxc`pm9nb#U>SGsepZm&xZZ@iT_7e|S`Jc}Hs57HX8>7t6{n5WRTv+K~VwCC1N(U21YyaL>@Z0*s|F8dB`<u@>eZx5ok8>IhW%-=rQr6lzXGfc&Gomf<`;2I7bbfRp950NvMQ27YjxK=X1<`rYi=wllm%;I6(MzMv(K*p2aJ(eCD0&H8e=Z!)jV_LM|HIpIAK1I?M5Bs-?4P?<{^jd_+?i3PjZr50fD0=fOpG#JS?OTnsUMd6;a4xcEpNNeZ~u`-75AQa+{(|q_s!0XGHr}9vF%(~>0n}%>B>q66Hoo8+<)$W!?wKbe&A1jx>3b5d*5y4U4L?|Gowr!qfBf&7gjo$7-hP$(!s=2|0(yM_g(Ypr}I4L_!EsP{^PIwJ1f8Gimy5|%Cs@c%<~)vRyvp%WxBG`!NgPlDfgczw|sW)tq<**yZAERu<_xC|19V3GrLOp-|ju9lu;(Kl5gUl{C2m2GJEgbGH2uGpZflszk2IzDWl9XMw!S;zKM0aeRGrO7rz@C_eaiY7|t28yW=@NW%V8PX^foHALE>%vNl7$jd}RyJP*GBvg@tzvkm_GBFMTU_&FCc^|K*2-vmGBLq`4*$hyyhpO-;KekNq;=fKY;xgUPvEkD{&{$OJCC1mASHvX4;-d@Tm6IsbOG5P??RQ_OM^d)5FS2jkOWsEYBm3$LV{jl5*vF$$e^|SY=b~G{i0J8E28}In*O{I)7k(GQCW80xj)s7}cA3#?AU}Kb7#wZh6$v5%Tf6D#miElkW_oYWKn)~#xUD>GO6MuTOmCsNA*_lzMjZx+`51hTng_RB_MwzaxbTILEF#nlUJ~meVGpT%RFdsFTks8cL;cV1ar#UEn&gzjTH#g7+KJfSjjViwTBipRJ<C(3_j52MEGSLTISm|J5l<CS!2NO^Iu-p$n^p~&5+wQq1zdcvQ*R5=7*!aG0UE$0q)5a(h+s=iR4kkvKuB>!0@zj6H{pYh=X7jdt-yMH3SH+uu;>%V(c@1@Dlxbs>iEZb?N(U38OjlMqn0V?x<^J=0*2vp#|2KYpu8Mza_IIrOkvHDt%qY{wC==Vxg_RB_MwzaxbTIMMf6D#m!uIR(w)@}je)n7zFFyNoR(|H4_c=4lv@y!WwsT>ngNae5D=QsLJoTS)|JnJo^Lg9dfB1Xns(9DmEm`>=KY7HNQKpSiCbpdmD;-RXGF@5eVB)F&l>5)$l1@H{yyNdLo3rr;9{T|&#yR9NMwu>*GQa&hSM_bI%B^CQS;nf|GX4&<g^T~V_@Rsc_&iS;>lx5lFxHP?Tz^(RzJDo<`_F}+i=#85P0{&qJU`kBqy5d%MR2?bM*L?-TcT}n+!kFpG#`#O$2nx>1183{b77oAE@PDG!YEVugNaqSRg5yrSe0AGQ$H;CL$npnA*;4CG1}aPaSpkRQKk!{Ox2DiR^?VP$}D45ZW&Mgr`&&<zrT{_Fn`al+g-&+YbULI=~o_gW|V1Tl!-Zv3o9K=j51wW>0sh%9#!s#$_K8y;n>qv{L$B6Ze`^IE{rm5tbD+Ql@2CWKH$Pi2NO^I$IX8}|KDd;tN0%}=UG|#fD5Bc8!I1hVWoqKl@GYE(!s=2|8eu5|M1*9R;##s*NT;u54bSOw6XF57gjo$SowepD;-Qc^&dC?IePDJtXA>AZhOkg$_HE+W!iWxhjCz~gNc<7xUkZ}#8dxq^Pe4``Pym~uRi`ID=QyxVU%fO<pVCPbTF~<0T)&}n0V?xZvOMXe)gsPD&F(x7Aq?saAA~bW90)btaLE3@&OlCI+%FsKjr?T)=NKoWTtOpwO+b@>2;-ybH8P*)=Mk-CRXdoU-UoTZ)LTfobLZnDWl9XR_n=?d=q=Db^K1PKP)RNbj@Vn;~ZmI`u@uE@^#(k!OtZ_>$-6s`$9OH)^%@%<JM?fq}EF-e=xCHFRlE_#yIy|#%jH^l5b+Qo?Q8ZiPd^?<ySUFnPsfjlPmcqp88?AAFB1zsvS+N)=MjYurbd4ma$qdt>l|nttVIQXkxXVT=|2IQDzyd_2f#viKqTk?mz08{tv$O`bz$TH%lw4XZkLTGHtA$>ASGf!NlsBz6&cIOgzn_+}0!g;#0TxtN0u5y4A{RO_2+uOdG2;MJ}v#FtJ)w<ibh^6HooeZ9U|(e|?}|#h3KI*UD;5qYI-<8>=;qF06Dgv0BsU!b%4dPyNSjJ@)@Rx6`lUxqn!+vRYH^!YI?mYE88ZD;-R%)>ON&(!s=2|8d(7a^B@X)UV>!E8l8mwWq^{QKpU6o(>mQI+$4P>2P7CgNdj9Q|>=%PuYjXkN2y1-$#GM%4$!U3!_XMt372dtaLE3+EeDjN(U29{ioc2)ZSQe`+NIU{9m4ax0Ti2SQkc_HdcFMU0CU0VzoEcg_RB_p88L@|Geb4KbOz_KDp)n{VM*^9Z!@p&i%Tul4;>pt=v*BWLjA(x0IDk6Hm&{p1$F;*3oAjW8Y_uqRV}O?<YAkItPBAIW&*0ugBK+XzS~-^*!3?1334q{Gp7MFWDI9eqC6}wD77{ZYe8YvawcfDJz*Kp88?AA7b0#+^=fKGFCodW1RbSVI|YTt6I6GtbD-6TDhgHWSV&DKjr@OuGyc-bC^F^_+Y<^kAC3;R{lQ^J>kqK)5a(>pJ#SprGtr4rYkEQOgzn_%I}N!pWM6Fc2$fvxACL@@&;!{nKnk5s_m*+>0n}%>B>q66Hoo8+<&g#^P9U>+f^~z+{RxMf9K37)5a)MwOth}9ZZZeU0La1;;H|X`_GmyUim52c2$fvFX3ITT*$QXr&QZjvC_f9yIfi6VB)F&l=~0dYfo!&pp=Vy*2r-0J9803jEpk1I8e$;2NR=AS5`Whc<Mjp{sVpes+Nb8a*;C_8FCM2E^-(nqf9LiDP^UDiBYC2D;-Qc^`CP8fw9J_HV!J~V$5P>82dPLF@`cS%GAa|rL1%?G0JphrGts5{!{KhPj30_s<!6Y$cG>PvsG=Kvz4_q&qhX>+L~u0|Kzv3eQiy+k)MC+`}^8Da4TzT!i|hFwKd^J_E@7h>2-rXWsSSmvF~w?u`FDVjq})N=kwV3e$n&bXZ?C?^<EKuJ@%IT-P~L9_1NeG+L~u0qc3UeoUN>_c{Vc2)Yd#38GS%o6K-VmC2bwJm9;hDMn;+1ns6ge{jl5*vF)@q&qhWc(AGIySzGgLWR$6`c{Vb(owg?2$mj#wI&dp%Yr>6;GPO0~MxOdlx&NG>{`0E#T)vcxXXr+L;#<!<bMZ{y$S6~LE?>$@2NR=AS5`Whc$!C*=TSSJ+1l6E1(kBKhR4W{Jh|DKi#0_?Mw!~Wpi)*km>6ZcveLoCQ~xRVpZmUbMPFN&Sjxp3LL-0ZFJIxz#hOMVqfBjGVks*fOpG#JS?OTnssEJw&&g|OUt1Sl%EcOHBY$?wtTPvDs*Q{?wRO>@taLCj%5-I=gNdj9Q|><>dE-reZC^$y7kem-{Cw7M=3-BWkx{0$FQb%|4kkvKuB>!0@zj6H{pXo?-q+Xmg_Ux#hs($pwqNJW#hx-FqfBjISSc$VOpG#JS?OTnssEJw&p&?hNMGBRTFS*9QX}vD*?DI!_Ou!qWor9UOIhh)VwCC1N(U29{ioc2{+4w5+B>L?{DH@Qz=^eYP#YO#y0G?+ZX>I5t5|zSw~<x3Wjy8@#n5$wK5HEt9_LKl=h0T$yQ7VaHg{p|-O)xynJ%ooTieL0+$z@It!-pgZW&Mgr`mtCcSjo;ZSKO_yQ7VaGF@1Ex3-a0xmB#aTieL0+%lf}Pr3hG`jtof+WXB)xp)_uk(<B2;>^Xn(Tt2TwfCEqveLoCDASdd4kn)FKjrt1@`2)ghNWD*3(?5R2VA&#H=~i254f<>!Nkf3Tv+K~;;H|*`A_ja)lx3r#cE{b11?;=8`j9m2V7X`U}EJ1F06Dg@zj6Z{HJ)Ib14_^f;O`90T(XbO>Jc511_v|FtPFh7gjo$c<MiH{!_e9zLbl1(HmL$fD0Gz#y7I^0T)&}m{|FM3o9K=JoO(p|0%xDqLhp8!Z5P(0T(X5o5RS;2V7X`U}EJ1F06Dg@zj6Z{HORnol-8oi^s@oIgA4r-wkAB<pVCPbTIK+4&%T|2NO^Ir`&(k`sCg_x6IjCtxx{yt+S<!bGBuy)+a0ZCRXdWFTRX7Y^>IAcc0l+$|$pp)%tBE-^3nk3%^tA{rV2?dL4I-Vt>qY*2>b~2eLI^N4*t(whgVL-V~i3T?9wdI_mS_h~Lks)+Z}}FtJ*nto+KxIQLt|YJIYjZ(_B6Tls^D)%tDaS2jkOWvte3EBPj#`eC^rs`bgL9Zjs(Co6xjG0y##v09(3<eONn-&XBtVzqu-`Gbv7W*MvX+e*HPr~Xs!Kk8Y0@%_%FTzogQk=3(!7cRc5+Q{lzybCKGOst;8yRg#1#M3;=Z5>hZ{qm(;d^f$3)mk7IMwvENYk^!?>0n~D7RZH_4kn)ZkJ~!N{onZYxhnpx+266UT8rqyDAUGjEusr69Zam&BD%2B!NgPlaa%|IzB~S6u8KGR#FwqC)<U~5%Cxas3+=*62NSEc&@QZWF!9uX-1c!i_vE+ds`$E<O${5Xy%;WxGHtB(Vz{u<!Nh7Wh6^hlOg#0Ua{p0#!9MW#1&u1c`y<<|toDMrFv_&C+6(5wN(U3Gy<je^bTIMMf6Dzw?M40cuU*-w;uC**wUyOgR2N2>HdcF4U0CU0Vzn35g_RB_p88L@|2*{bf3y05_rHJld!x8f#ov5xkCi|Eg-<y%%Cs@c{Ef@E?r~wIgNae5D=QsLJoTS){{dUgY3*3bh0To&ZRgB|4;UF`YVBCcN(U38OjlMqn0V?x<^Hqv%gYUHyT9J~&D~Y}jbGh8XX8&Uyv><Wrj1c1ww((r9ZZZeU0La1;;H|*`Oi~qN56{ixZ`pwD<5!Slxbt-11_v|FtPFh7gjo$c<MiH{a5$CpYK=kXa3v!tgQMV7e<*jR(+5QD;-R%`XCopI+%FsKW_PRVYgB)Y;I(g1G{kH14dRkunQ|4OssNX7gjo$c<Mjp{sXbPuk|CPT*Q1ML*L=dMIU5jl&SS2rL1%?G0JphrGts5{^RC9Mc!D-Mb2qt<pVBU<iJK&KH$Pi2NNqFaABo`iKqTk?mzp#|Mym(f8FNBZ#_>MHvXHB{Z-Ddx+g8=YaaOeTp6QGWF_Ck=XQQ2m-*?xz1hmY@WIdK{MuV?D`k{f#wZh6$v3fXucQC*!Tk4cMo}MsiqD2@tADQk2A>VJpUXLpWv%I@pI>s0O&{NL*2>b~2Wwl$SoS_xwT^M%17B>M@`v?2@TD(m{$}RgTb?atl!>h5n|R;@Uu>N6hxI)0r7vp!W@eOG#wZh6$v5%T56k`Vxr_f8a?Tgez4X~V4I4jm#lEMJKb(BR%5Q%4yPy8ZvE6e&zw?)@{Chw3*;VA1{lRxzx%tyi=jGlsd%czSp7*Qy`M13GW-EV$pOu&U+wEVp@^5Uv`co+LQ-^-p%2>zG{8O|?)z`#W$6LSjt%j<viLqQ{rGtsFT$HJFFfq0ZvT7p}qdifkvaN~HR>;b3CPtg1Ol5x)``#B7zUp!hI^P$Qx(6%d^e22T|G$haq3zWVwc(k0FLx&VoC7`J1w}uI??uON?Tp~(MbPu%_j|r1|9;OGN3V!p3CCB$6_>!7SHSU#=t}5Kw?#8>oQW=lKJ~kz8XRlTbG{<FD!K-a*T5B5!kKkA)}!sw%cECCvv8b^UL9Q)y*9cQj@L$)!`av?Uj;wcz*%+BXgmCDjb0P&fd2M1@N-6VHT1pb!}0v+I{aS9)zAIW=KPsO72~syGLE86POM~Fcup&~lna?w*2*nqCDX*;!Mxq)eI|XM+}?AH5HzlN`o6a`KKDnr<?jx9{69UG^JVY*r`<Mw{*K2Q&%f^0#zV)yZRKCs`e@^gTW)Ur&701dvoV&t<%@gsa&7$QPaMzBf7|i8m4EX4R`PPM{h8Ft-~9VtuKyoz+HGY#|EXJEw|1?GvD_Qpb?=%ECPw|=^}DZMtBZ-z4tTz@iHXskSgx|Ii9xqM)^XSKvwa&w9s5|vt2XbjGU(q&d%ow(*IF6$?_;~*JBw@#`se4jKR9D$&_CC$|1(!u8T>8R?F%O^w=$lOc2L)v7|TU_DjiIW`eVDOx|kU4fafclm>6x2<tqD|7-gdVD0BPU7xR1YU%&pDIlBAlx!MoCW9}U*3;lvuk@a(){qY~0d(9@%zi;lf)^l$B-9OxY|1FR7pZ@dSs(!xhoRQC;E<T^LeGW2L3z>}(-PS$_-Bt_T8Y6XFE$V1Jr;yXo<jjqpQ|Qys^vTaJ>eaB+D?eX9r?5|B)IR#>db>EbMZY*_wWLkg&M9dx<2fU3q@QDJqqTEN+DO;g)<&apOl>r(&$>1;)T^P@t6`{@t-W-8Z0)snj?QO6J{RQ~T?9E6enb0K_#Nfn;~qgicRn2PyW1nk<8U_QmGC=)T<w)`d^P;W`H@${5%WgO)iAr;1i4@xj&;b-@cZAl!*M(0X6Hh-M&L*wcY7&haU703qL4>k9HnqfBLNxW%cJYzczu*WCV5#j2gkW+CuEG5M>oLnhG;irlUGE0;kY;213BePv=5H^qMIO-#9Z)7__+mg$Ja*t;b#_(vr!DkIAU;Qk%Xg+GB{?@E;#OjWO+aQ+z7`TqnqJ)b95^lZv`3q^L*fn$A2l0QP@8s7yX5i2mRy6Rje~I_K(l~`;V!ZX=E&S_m+>T*lT3$AMyMmh8ua%KYm>G1xChv2K6uc6eHvL@A}<eUc1)BSnit+{mPmSCPw|E=o4#oF)`W!&sR1vG1?Q$Rkk(ppzr&*$`g!?eJIwk$m@)Z{Uh45$VrTheHpe(k=qy<`$s&#$dQaZ=pR3>axEicu7bK1Ih&F3e6)kQ*2GvY+EeLZV$>hoMb*W`Xa_uB*~G+Xb1YZc-^3^r^+%an|DyL_dQ9$XF<I}A^w@4aN9!Yo&e!^vIotXAIa)u}7|~%)>tE&!{kz^LTF=qqc|$*cM7P~q|1zibFUE5W^%~6+hCbK&ER&rZnw|4@DY1XwkpEcEv9;02Icsg9pKm*7q`mrv9A>mF`i8vJdQM4ujp}1+FXK5QZPYj9a-(h3H{_5*ZKR*0^Csv+qX?gdMETPYeDZ<$z{~QdAo#Q+f*u-Yf-ZyKm=9bA$1C!DU<Q6iaQ#f46`TdRz>D&H;Kh(v)ZvKvz-H+GcffH6<OBE(dIXLHvIG1MJ`P9B2QGmAKZPUa1333|JsdF~*arRo92_wpxD@*TJ#gFu`M~AS|L=w4UdRq!1^xd%IAT8VYRE^fhT|mjf#~x;oZIS8>Ww)Y-~Zr$&EI?V&QIOmDB-y(2AK^_ekot|o*jJ~E16G!`lDsMTE(i4g?uYNb<3A_E1Q@YWg;t^Sa`0Av5uPjQdTxGv6885V&T;)R&~_vu#PS7PjH!ATmMc2<2jA0_a3aD6I=hT2A6rW_3vsho>TSii2nMzuYU)H%lu@8eHs?~G#u>H@U&0E!9ER(eHvx<8ARrn<dON@e7tr({8l41jL;WCT*eX7%i-r$`Mmn8;fPW2<?wSI{D<@G7@seP<K+;)H$x1bf#VFs(Q_aMUzN|eUzyMUUjxT$Aa1`DBLB5;#5j5p#Nh34#QFG3AjZA|j<0}-en$Qr;EZC77)6H;UA5=S|K_c$-wD2W%h%@)9Xe~z>wfXg4M$$}VJz$MuU)fN?xY#Zdi-lISu59p=Y06Nn}4c-b=mjB-#6#Vc&!iPwQoO?^j#URb!F9dA5K2u%y_K_uWHviv3_k8LtXk>-JMvogA;3Q=fqmuRWkZ&eC9*_-Upx6dG)XU@I7<4yy&4m{?>RE&%<-@T>O9SoK@|dRdvp2Y*q60IILf5J73pfH2%Xm4Nd=sc78+CzoF^h(DZL;`ZqNF8y5ZZvh-`q`XlZ9IqiJYyNQPSBbz;SIeJ}ea%_E>-gXxGs}}jCeWLOu{d~PF!}+7_wOZDnD*3v9uJ2oo@>ezaeNDGH%?@k6ZR?k9eo}J2@!qlJJi1?5<PV*H2IK~~j_p$DjlT=}`*Wdx|1LP51-<+^(3f8h8NpSMA#8y@|0+114SB(p(5Jr!vV$Ga$G-}C{T*<8F^rI|g`A=eW26Ln{HtMnmcTKB(Gr3DK*0EG7mV6s7_IGs<C!ob+nJBiZh|pb1IBGP!td)LYuOK@vrAwsb$fItjK}sy-vht*LI!dkjI1t>Zi5WsvgnTJyCKK8437U7Ob)ki', 'interior-open-worktable-01': 'c-rk-S#TW18E%6);)H;)2_XbnHV`0LiMbD1+OaL$#9$;N8*pM9XC<#>RpedOYK2b)r!d4&sZgZy0+quFFL`o>JP=ZrC5n)Q2dEU4gIo`ow-l~a9x%yEj{ax5cmJK8qet^XiFTFt`?|OLzxv<VZ-!-JYUh?q2q7n4B4p3)gxtGhc<5NMGBZ<c7W<ABC#tn-qtdK5ihafV4m9eu`b=ShZYgY>s@C>b8-=ZR4;LOadi7qzE|!XqRvR;u^%`BQ^(w`=QgLRC8YuQDjLj7Lb{{L&DhKIYafkn2saUJ;_uo)TYDp{UC8K1Ptdd=FN^VJ|lj`2Nz3o-UiU+GR2Yi#v&cpS_*P4~lscK=WIzjC<8<pD3RHf+$vb#s=HA_mbp)3ABTQxP)v<*6?DX#xdHw@iyT*clySK`*yXzRU-q6&NHNp_*dy3o2@EGY*))`2eSASDH(<zcXXaC)lRtQHPYSB06`#&~6{+U<q<aBS)c*)Ur+c1-TC7G|fXX;)RIX{*H*+R+RM$Z-^#hNE^^vpTI!)eli?GtEY|Id-7hh_k2#X)BuRD4MQmMu$y1Hp0kuNDtCU3^KuJa-43<?1O%YQ}x<JOeK}52zxa(IBGtHKMzW*@#uIX9P}i6Xn*8Js+9(-%4j35kGg9SX`fy>4py4g#$;tGxO(ib&(aS96n=lPui2Qbw%l%SOdhN>jua*ul_S*U^l0P$YO^vmH90m?pPe{BuU<27NgS=rR0r!*^~RRUn15lUhhyo1Thnq4$1!yppQZZYsq`~ts;XhrDO2-T*{bfiwyl^Y6{2H4xHVen26xw*>$UC9t#eSg_*4e#vo)G@vp&6)Y;+^2qM_)nshfW1u`7e2+O*iF3K^<FI<Beds--!GmLVU@>Acd+`3FTCq4O(ZaCWrH`fHk=&SZ1)QMRDcY&IrGXPZ?&i|xZZw(i_IJmk9@8XmcS!#4jKzH{@g!QtVNP5Tsjy`^7AlePVmW3WYUw*}oZ=l5Z!PfgsX(e`O}`n0n7)Wv<;ZJ$o3PdA%SL)@o|iyNx0nz6iQ2DdtLYlPgIv2N8Uw^jzX7IJHc+&bB^wKKSN+io=_)WT{uw~n}5O+#+=kXs|0TQ`GS6S=iQZtYBNRV9O42f1}S-Rep<w;3)@y4rTDYazFKHn$nBPdd6l>7gr>o_vX-SLMnWeQT!P2z-prj*nLx4^37N`PbSps{87-YOT5R$TSVkRN)ZE;M<2@h%B&n*#AmV^iDCL7}0vRdmVf)Ofsz&VWlTpwMN=$`Y{$C+B~Qip`bVyH9eQ4?OK-YTGw_xYP;Uru0pf0{W}IXY}+u>Wx-fRXJO_$3oGAQ*vqJrPQFUI`6{U{s|!TVD}<W!5~1qi#kAP1k?t6(W7;m%O*4Z@-PY)Rhynthl|@xudXuj?u7yk4Wuqs`NKdqt#6lQ33u)#oq?Ms7HI}hMZ-y+_vi%NZMNkcwW^MU*&OtM^?wGWWrtC7(6J@0*+Du|8?3|@^a+cD~S;~mHC6qF1GHWR{C8q#T^OaK5mQ7b`dd^ZBIZJ6SpRTlWmeS5yN=LkuT~D{7n^IA2HfbBCVmeC4w@#OlxTcIWlUNEjUnzAZr^Hv6O(}IPXDRiZr8M%DGU_v*y_At3`pl)wd9R~qz1gAhwD;p%djEEQ^hmS1ty-IC`VZtyEtnY|ANT)rAYIU`G$w%RhHGi<U<5V?Got%#%jw*%=~T-LZ`UlNbGxqCA@6#o=ye?`z4Yu2!*OzCZ(2sK;?wO;p8d9IDLKM-Y*owS-Zh+jy{A}up5{|k+c9zlK<_(qRY2A4EdAe|f#I0B8dx<gEnf*N+qUv#V7pqb9#$R8%~t}~G4gzfHTW-rc>>T>-)0U2nycmc9BW3`Wi(>|hLi6?rkSpr>ubbTja+T4*>1jTndT~1o=>u_XlkxD))hD3#Z1>!J<lgu*EJ_s8|#LW?_#E#nv&;}tXq2b_hCy}F;#^O==A%~ncF*8C={-ImXM8Ghsc?G&d+~v=ie46_KWi8pZoK|%Qs&(Aj0Y2IpDBYgtNV6WG9u=*vcr*M9zE(bCmnM2uHaHaa5~wqMYS2FUnc1&WUi8`@9H;8lm1u<#1-`+*3LHp}rF0=-h=k>ZMf9Vk@IK6FJI#UX-J=PUWap^CBGOF2qqTLLAlVoCqiM-}@`gMf&Fv|KEv4c<p<0%_95r*!zp5<KGDn?+veK@5Rn{+B^}m-C^HDcD%41yaw+JujlW_*@>zF{}&Z2%4-q7AD+kiQ}XRt8)pZ{8<X#1XD(g#J!Ibt+mD+Us86_mJaq0Js!zu}KEH5IDg72{C!rrabnae6eZu|Lu^#nv<b0IRl>YJ1`FatbuW&zftVib+IiFO|nEvt5xqImI(lH;h?<Jg9xZfh}^u4&IeELsMmE-X7g;&b2JoWwlembT$%N${z`7Qr|t~*J`FRnS(HC{Y@i}w!QAI1fW!Ty3jesRri5B%{lAnXs;5d!<TJ&fyUJp1qXpd5z~&nQKRcj&?<FFX$7T;~OOkrwiKh~sAzA-=#~Fa{i^`ymb($6*lvdVkE<W31fql3(XIB;*ypo)GW%A`s$yZD@+-^pbxr9Qi!N2{?4&wpM-d7~*)Hj^mJ>lRxI`F+!YBmpBaSywVHeA}!?ekRO}}#2bY{omYAgFRwq$^D)GchOnO_>!;S(A?wK}h(rHYk{x6>xre^qLu~ROxt*-0udB%b`8c_r+)ZEaCby6Rxs&XnuY1TgatXPdTuDAjt|e>9XUJzsk$j$ffs}|w4AMu+WFy%`?j=KHJ9&ugB9D+8$)#i!eO*OvCRdQF$#wMgI`T2HhTK7V>1!|f6!{|g9Jz_U-b8xHm&m8dt@QO)azD9^>?C{X>t1pf`7(Kc4Aa+PvXAKGJ~BdIM~FopCLY;BU$>C2kU_GJnDo^on`ycVap|i|E+hTq8gdnVy^3rgH;}DFrLQVkA@76aeUQ8llJ`OKK1kjN$@?IAA0+RC<b9C55Bdn*2TA=e^}p2rQvXZ+FZI9F|5E=;{V(;u)c;cdOZ_kPztsOy|4aQZ^}p2rQvXZ+FZI9F|I1JR|K`5y7vFs2jrsTg^WCy2uV4E()r-#w@#mkrVX;Oz>=og#m-2pYM}*VZ`ca&T9DLE(ggMH6L4>ot!kpy-wG!qm7hzrxY9++kS@iQb(>UGhq25U4bgx%$pL;5Yy|s2<32}7pLcHGYrBn{F)!KcM%2DnMqP*Td>r~Es@xDssD0d;w&O(^8v*3M|%H#Cg<Zst3!rxzC7t{aY_58a(Za%C2XLh`>ojAQ0UeDi;vy)Z-qr5t_eRzJU`ajN2oPI-j3F-gvdTu{%KCAu*8|d6URG*IdrRx7UI|=>Zp>t2w|KathpCjk9>VFi!kp2&^N9PqepH=^(ygIafcz&t+KhDk*@2x05`QA6maX7H*?J{}oVjqk_2XgF(d8YqiU73ytRz21=e)s5F5B7)g9YCi4$*ULpZh2y#carYoV?fv+tRv(+MHq(>;yJ$dzvVcDcmN^ZUtV1Ag~t%*%};pL_liLGGvxCS2jI;#zQA5E27Hz7hd5vyhe7<oI=&ubdDUY1q+hRS1bqzkgm|M6;yk|g>;8H;mo^6T5GUaIqXq9tR$n}ZID&CBvUBpsC)s+8;1B8&htNOo9wqdw7X7-mF_?$^j{580X8Sr3;yq8-y>qnCsz0pfV~FEu0z$vRevYi4TH`|tKb*g7&(-JtwPUO-%Inu&dTxAtT!>$I;ANk~UJ=gr4j?<JoW?eQ;!NbsmoP`UFNkoIix5Y(66P!yVa{qL#8K`-obK&My^+f4-hOoMsT}sAz7pc-+=V#mrBu#h8$fX;a+LdmC`V_V%2BO^ILcj!qg;eIs+AB=(*N*X4d2<K`X8^y`af!ZDf%BYSJ+OH{>SUF{*SV=6#dWg>eBysK9By7vXi9$Szf~WAFs#yKWcs{`X8NphyKU&dGvpjoh1E_&Rt0V<MmkoN6jxq|D*F2(*Jlp*8frSOVR)6+&lC?p3kHIqwK6+y}I1|%ZYLv?mGUf^668j`mdp5(19Fbp6h?U?$_UWtZV%H4L5nPKa78%$o2mTI-Wnf+k<_43<&#!b%gwmB8<ZbaenLe|CQqq;sJzs`VI#AACCd&&#v?BfG*_7=OGTjvoyZIUN8oP{SXI?<1mPSy<Z1dAI8Ine(u*R4nZIDddA^D|55YT!?|$e^AIQCrcJlC>Wjw^Cye8eol_a&h4o<se^8e=gg7>BTImIGkrwiK$d9j!LWmdELA-nn$j1=pw-XTJg#8>@Kefi7{Xoxgtt-Oek8AHV4*P&}U7g0+-hN~!m4p63aVB!+OPHhF7eqM9MTnzX33HZ<FlV(A;wX0^4v2aql|x+U+*3L1MSUg2(YXt8)Jv(H#nzAFOynr{1yPR9I+deZ32~IW5J$NPaa1cIF7?0E|5E=;{r_Rr|4*NKz5LY({eOziWBm_ftpEA=?AaTAJs-w-iX!?ySVssTA7d2N|4-3)u>R*`$nR`~{^#>)`XBNM-jBv0{`Ee>`Y?*>e~32<A<hdC`k&9I>3@h5#&O8b$wycp#x(s8aYX5VKF{?(^h*?`>3@hL2_X;I&yn?0Yb>At%jf^{`M-SrFQ5NQ{V(;u)c;cd%jf^{`M-SrFQ5O*=l}BgzkL2LpZ`n!FZI9F|ML02eEu(=|1ZDi|A+s6`64`fJn-zneo+q367Smcj1XUY<_e#~UJ=gr4j?<J9G+F8I1@SZCCpLo^CBGOBE(UxggMJan6p|5ag@6dr+Yor8>yV`_0YMea@dRdN{FL#7viXwQaOul0L7WeQSS4i9G!J4N3{~-D0d-_auMRFRzf^Zzi~|=s{h05`FDTZd{+I>wVtT{53lF%$JxoM|508Y+CDtLRQ(@kCr-biyoB_Bcs;itH=kAibFCNF|Ka(i>i;-93H{)qb5GU(;q|DWBj>Z~e-yuv{tvH5=M_1hRsW;BI<$RweyRFD&d#x4kn&Ie{d74F{pb9L-98wD4&;cR|MPV}dHiVC7@o6|6K-D^@$-Lj-0eI4);<sR@$m|Zu%AEw|06{hhY{l0e#OOd96~&R5YMjTo4xQD@JDZXUXT}QA)kkM03p5+-(D~Vg#8d7jFS-bKOkR^apMb%e!b!l^f9mJnHW5|<+1YM3&H>Q%aPARoPhg!3$6O%F~kAmBm{eaXV`j-;1B8&hY-gjy~GRRY9pVA{P=l9A;i0nu6u;W3uEXDKt6^(NJ8j0*v}C^|A(>E|5E=;{V(;u)c;cdOZ_kPztsOy|4aS<(bE6$+XJq3MR@T0@@IrNXhq;$SEq5dw;$O_<?#Ch6lWr5zJxi-eO`p4T!c8Pl`v<y2y<2|A&znv;-KYFZ=`b2is;-^IqXG!CB)IW3vtv-shq{ukK#<^DEE0$j?Oxjqgn}Zl)Df|xd?GoD<LlRztsOy|4aS<Vb%Zs?|e>l>wo<FA6N&!N5T4^kKuO~py$JgfB%!D|MBmC_!y(8{)gY2VExa>-=z5C2>s9J)AT>&1MA|D|NiG3MOYt3QT-3`o{2z+^HhZX=ksa$AL4{@9P;1)K)m2DjA{BG`ea{({^#>t|3kk-VVeGj_=XY?@__pcj`;UKF#bOP*E1;', 'pet-care-fixed-vented-arched-shell-and-grille-carrier-01': 'c-rlK34C2uwSK7sh>D5`D2P}A8B)CG&MEZPGPHn9(lRI%2yLK|kd!nP5YQ?r0wN-af`SMtb3s5vh7?7`2?taV(WmJ1InTp;PVfD{eUf$Z-7o8$+?yNvuXz0ZK3J@NYwfkyUVELhchcht{figOoH1j@XP+^1MtzSNGxl3_(1EAV>RGw6cX-yE(`UWDcW7nb;J~aovx>VGW_8Uvp?9EnsAqU^2%3Y2`cCK@=;_~f<#5k%-_mVQ>Rq{f+ogj8D~E?xEgcS4XLik6xfB+&<`l-Hm9yp?dHSq@o|B-PwV?0R-eub!);lnaf6X6Sx*Y#nw7j>!f7_mcW!o+s>g(_C-FDBOp`pIsA&fmRxGc6WEID(@_<tqd=7*RM85|rw=9m?|!?Tz64E4@FK8!H?_3;R^d*TshuM8v1#t5@dh(`#_Fv9FYgh7@r@9SSS)QcG(8FdxAN?qlyN>{b3)>ZH7?urUsQPdR`yP{H8RPKr@T~W0ws&z&6uBf}KSm-Lkrr1?1brs7?&g@D;JAC<IfA8YueM?VV&_6ghv`5d%z5$FC5{A@FBn}O(I$`;u{=s2{y{K<l@4-C-z5U0`juM-wRhw~>q8ra>)(>5=qIc-9o>l$B3B9EBJ^Ke&!t?T;6}`(2>FpWXdtg~YE-QIa?}{FjN$)6q!O-Bq@aS?b7z!-2tEk;!y+f#^o_?~}qi5)tLSj*E(PDhwwH7UkiAB9di&A3I-J(T#d;tqBnpDP3q83f6<0cap{h;HI$1d4(XmI7q#9*90VbS9qx)(}zpT2<;u&O=7#}sxgMif-pHHqm5_YEk!($WB>@ytfm$^0|9<`?b$J;O_v&qs};CI^;|mtQntr4L%sJFs|gMd&%F?SmH4Pvi-UybxP%VA;Vv%Z}M`cGR`)Y|OP%*=c;k6(%uIew4xY{1>zNN-u@38RX`+nbMn94E3GVH{AF7F>=rF@KE1ztA@jWo<8f~gBI<(c;AB#jQje52OV<2{QcveG^=l5S>MvYDPkz>|DnE~{+M(Ux^?IiOWJC7Ee25<52DOLR5*xe3PH3HLv=ic8plv?JqEuWw>W+`EkuC>h@w^_@H>2q<Kv+?9zdxnfO4w=O#0MlHI@p+Qf-Q*#<3JLV##<CwHig8qUdhg9EA>}XrnIiMv_DkItE2i>M)988&Q-gib_)y)efU5wGl;)qNq1T(cNJb<u<w%^~_RJ(<~J`jH1#;6x1|JO<l88=`f0F8&Oc(EH(AbQoYqEQeJ6Vjer_wxv6oMqgErxcuQ(AiZXT2a#Qy#ms@?3`Y&Fs20$&d+|)A5wT{wIYGZ$vsbiL#I%cIX)hx6#eua8vrKwj|TJDu;Z=9`$K#j7})F>;}R#V`<#I`y<wa7|Si>$QVB2(XsTYZ(H23c)tkk#T8V`w`B>W<Z>?pUo%A%rPqfm&m=sWn#XQwyQ(2&gsInp$Hmy)`Zw|C6R;#{Pq+^o|}b7WL!L5yi5>Rmb6-4=>xxX3ZHMTGfldjvG3lcetm&zi;Uw;e~vlcV!&YaXl-0_Z;jW99qz`G`@Q}vaoAZ?ZSj=;UD#`C_dVZS{kRYE9z*-+>C2$)iWti2d(Hic~x)x#vNZhbsiWtN?})2Dx^w#fmJxLy?TaD9DSaR?&0|Z%NF$Z4tE}30b${v^-}!LVtXML&kQTvvlL~pa&TyLg^ycx{P8%i^!1(+_obzSC#@J9=p7hdeA<fM&{V@K-cl6eaCj#MVK~;$I&AMf<D+|DxN8gBqcj>=u?zoEs+1~mDV-X}Tr8EtpW&4{bo6SuoBmge%btUXrXEChy}Mqll<L)LRI8P`ySrvbNJaby^+HrEluETq6cr*4Zh}oPaV#{<q8Dbx4Rg_+^Y@>B$Sn0x%ARN~yilfPyI7AiihdT-jUba5g+C2?sEhGG3KL^5Pj%!to%WAp$e<X*grO?gY2u+$(o~&du<<)oT9!fzYuQPvt-B=EJ5EyfB%3CymP&;<5pj;nl}dsBS87UFci`cbHYBV*F=0_*szJ1$u_&5k`%Rv*sF)pYHKW-@wb8<=jwY?Cp^WXmGEU9m4~u0dQ>7^mJ%vP-vlCUFv`s~oNtQJna#9mj7)?}n-1-Ymc`A(7QxxyOvX`dnR7ajdo@$d66pfXZsQT2OTu~*w5Jk1oM`XlL$nGll_9%XomJ9JNEEl^cd6sr}@-Qvb>Xl->P%f0vBluxTe^9KKnjWTNV-HiYnD8(ybo?|ecJSU16{_6z3Q=ooF;>7Wu0^ppO=}VQaLQU#($*r_xNG6O*pxb7i}KW`T4;4A6v|DHszRZy#i&f%#wfPE7{R91#i(|^7_|--qtMD?1YXliJ^t6uTGXd)ElN{Zi&D#L(cSqg|5Q&{q1?;O<z8-WWh(7#i&FHju`No|aQZ4ueJQ$I%ROFxCOlSJUWxL*#?zuy>3k)sQ(lRv+~P{Kw+m|j8gEUddgr<C;03W*C|2wiuT-oyzuQNZ(Yw9)#>csVnDSMVo6hdCr)zrgcT60M32{apr?@=HdtWI3)T4PRK0bBFdBp2x(=E?f`lak+YB`$ZlC4~tVo>d$tjd#|KxwG740iCcRxDOWQ#g8U(Oph`pDadW`K-nnEKQcd>J#0dOHsQGy5!tbmTR3?aJ|zCE=8sE3NDpvO^?Y^YZctR&MLT4=(K_>QO6Y=o(rv2aH$eG`JAktE5#?ip3805^Tdu^>HK(FDNn6*;x-cZh-#eEsQE&9^d}(2(GDDb0y1IT%DOArYR4s8oBEY<p+5S)72hcr&;pv?g86h(kMmh6#y`%AntwFpJdP{%b$7*F>F)T7xmuWV<BYn)UJmtCs5dpuX!J)vg;Es1U^&;O)o7iSS+&?{nN>@jrYKyp^N;kJa}+nwij$=Bx=T`}<0Mt5+_2)Ga%mZb+(naBQElBNsNQjcx;spe7Ex1%(rTzySZ67!MQx`De#brV&-&w^^B;HG@YwI(CI7j9@4yMe@vpL13*+NYV23|$%b;8;ib1WI#jg~~!mror<qU(UR1Y`KZCK!)s!*3nbQkMc7L`iKaT{ZlCeC{ji*hL{l-r7`TrGsB5L-l*>@jN9sM?-Icd;PzsALD#T`ShxT<~&x22oVi<tt|!ly$wMTIM7wII>jRvnbcAvU-(THOrt<F1NRn;IGi8MR%>**5<1g%Jue!s1~bjPNRw;+6$^uDYiL8t=jH1y6fe(f~plNZ8pMMvDW4^YUO&py`U=XR!FT@Yj+ym-R(8>dZFD4sTb>QPNQD#Zm-bmm3Av6bno^oy2E*=ouIl4?N$h$4{c7Pd*btTlAtORDg=+VEQ2au&D%4m>H|C~mop7&6CMDQ%(~uPY|kPpM1^`=k0n^t^)Zt@@u*NNmJ4lKRBOd{as`XJKJq7>I-cR}n$#vdFel4atzN0NH+S@fHuGDbu%RZ)R(--_e3BQWD4O{GGO0;%!i!t>OBF0C?d?KXbhoz+qo`DFZy&;<Qf+TVqVj~EIH^Us)Lz9$<w~u+%8Dw5Hg|3`@$GH0s46Im_Qt3dqBiGIomh&9Dme>|odfxgqiUtQc;=EbS3I!6j6L=}aK>eqzGh_ON3P!e=Q~{3F!^PVT{?2%uXm5-mq*u*Fo*Rg{dBj6$6@`di;ifRPv)@RWR8J3?DIEge5m1#74#NckpK3^ogu$$?p1qV()jkNJ2g!H{&ovu`HJ73-Na$N$&Xz9?h%g@^yc%izg{uojm3K9uzuz)3rD=MSZ{KOjpxX7zh`(+<5#b)H}2Z^#wHHyAAiH*5tG@L^ZdDOSH%1~{&;y4hxP1}ZFx<N|GR5GHsbjYdiKe-Tt7C}pZ<A!Q!TNceX=drs?9y{nZtVa>D7N2_vbsDJYr)phxP1}ZMklZALj1)4|?|L?ZL1vyr#@yJ^N%mujBSlpC8MEn_k_-Vf}v3+GE6Iw&iu4ee04~e%(D6H*r|cKG~Mn(fA)(arubnKj_&f+wwZvSl533hNe1UJ^N%^UPqgI;4_Ey?2~PI9S^zl=n)%>Ijm=&Y|HCt{4jUVf6%kfv>M<wWe)4vC+m3~xyLex_1xdsme-N{FmqVXKG~Mnk$bi0Kj_&f+wwYcKW7f>*(clbI&#lv4(r(`+wwZ{bAdVDb0qj-TV6+grg;8?o_(g(0Iw-?yk}YPIV1kx>b2n?PeOU#dMM9mLC*B^*Uh#WIr2AW%<DuhZ5GY@$Qu`rgnxG;7kkf~_odsOHxgp&L?)kWJCSLQ9m&BL`Jb|kIj$X><BS&M)oC*MoY#rG9@l)w`y!V+mRGkTzkX)9G4zypzof}CCX*Nc>J@9Z-s|K>_;)ArR+pc#_B%6n2+y(Aoyg>KUMDimu_HP7BL7pCF~@l{-zm%Fb8RPbnBxXO_-^J?fTsda1D+0S2y6sA1K1dNCh#oa*}x{ibAaap&jU6Eo)2sWya3o7*aFxRcp>m2U@Ks2;Kjf;z)OH_ftLcafR_Q=0owyR051o21a<;;26h3ufZ4#Vz$<_P5QUx%lz=i&0jfX^r~}==9AGzKcVI3Mk{A~FmB4&p4`5GVFJNzA0k9C*2iO<b4|o-@KX3qWAaD?HFz{;N5MU9o7&sI-3^*J(0(cGZTHr|FC}0V2G;j=XEYJfS2P_4a0lmQSzzM)|pbvN*a3atToCFL2gTM;lWMBwb2@C_PLfrzV0H*?{0dD|K2hIS_1l|a|X{>>~8F&kD7VuW!ZNS@svw?R2=K$vd=K=2o&IjHFTmZZqxDa>`a1n4Z@Lu2&;C;aRflGnQfDZs41TF`z06qj<349p13b-2h2=GzhW56}QwZL`2^}r3ljlfO78sKK&7U1K+t-x)-PygOGa{r%qY+SVEM;a!-<Zb7L^GhN#hxI12Eptph`mTLl4(mOR>VvHDczTUZV>Z4QCv!9g)(81*zr4`puwFS9XVBYNCNqci9Gm7u$4cXP{&iky<MO<iWBxaO<m!Z@vW=Ui=bUH`*{5<??{QS`jpgZejyiYadvP*H_ms&8pMQ8#dqMW<mN{u_$Flj!((71SlUW?rYit^`@x6V=9L>4O#xdDj7v^X!d23;Qvh+HZ)<zbG^%|STY<#b-n4>jg@*`IllH3N_TNmc&+Uc4GS^ao=^{HbS->V1aXbf5#yzXgw<yf3SZ)2Iv9M*GeniCx>jpO;(d8LiZ^J0$Hq*og@ZkC>N;?;Q;CoP{|%*OZXoH<&<CV%sQAI-Iz39?sj%t^~R%jPFbuVZN~WpP-qv1!c4_x1~OH0LH8$7F9^n4>k|t%do?((71S8(AFIYit^`@x8iYj@FFHkH6vKB)38K)`dB`cDklPRzIFzed<`o_v(Q;8iUpbuX~zaITmNo+gK(uhxHtr=0wLz<9PmcUTNd<yqKdk>D7jfo2BQRcy*q|Nz11fv+=z;XO7me$<an#yIai!*{e6^q~)At^OL35v9y-5IIP#$G-l&_`-M50bCZo@vbQeG(Hij9!u(|Ebu6uoEDq~6HjUZ%UR^OqYsTa?3m?D7avNlCU6`Y5r)wHy_2cQ)r;cTOuO67AF=%b@x~J)tV{rz(jb$=(SkJL(PIRm^j^|(Jl{PNVi#b}8UTxU8S$fWiSLa!rw0wFo8{eyQ=4cI@{J^U|d9T$>kiB|iPFl`cHa}T<9ZPE|i^F=2O=C8`w_li}IXBrjCVT6`9IXLwEzD1rUdPhf$l|bGW7C+8@6{D^v}Q~`>VlagmfIkE>%tseJ6+Qts~=CVK6NbPd-cE^jX`UJ*F8<I9E&sPZ7h?S!+MTQbE0FVaXkMzue5P_Ud+*&^lHP#&C+vDygJX~q~+6#+4x?aGe>LK<na44Rx?5N>Ww*RIcM4YWa)J*t)(mu>oqow+4$amVUFh9WaF6ZtqXIs2E4T}KUsPmOKT&G!+MQPV>Z55SIp6xG5P*KFHdqCWN%%Vqid&Y8f5k3>D8x>Wqhw5n4>XhZScCM>6K$~2EC1CGILnZv1v|ptTc}2U+0xJF3*cOT9aOF*tl7G&WTs&S)8<ddNCW{t8?aP4V!#K_r*!g1lg-M=A`AEW%HAz*RiygvN){Q*feJ2d;5hsnsbwlW3sm{%+VU~*24T`>2)lvjVuo9H8zde_+DKxM{CC92fuP-lG`AA>%tthwKX-4$?Bgu-dI{2>L*RFv1!aYF4qimGzP6PuAel$axBiEx3NstyfKGuIW`?Djgz)6-rRLuo)>epw!Ip&akKQA6V@xAV_**3da-$9rRjB!I(Hpc=f!!L-rs+oj^DYA{mmHr9l%cHdDA0L+wYRjpnP>8uaEheuHOrNvewV~^!E$${QP_7C-1BOo_#gn?|FXm{N(*G?}zz*&-0V#C+~-OKg{=go}WBFc|XkiVZPt<{N(w``(fS>^ZlOZC(loN@{_f1<b8D={=EB1m!JH5JNfr^o-E(nxgGcfa0l>7;7;IEz+J%Iz&*gdK=?(fu$k@yJ`H>ZxF7f|@Hyb~zyrV+fG+}H0=^7<1$YqnD)2Sn>%cdFhk$Pa-vYi3JPbSnd<S?G_%84m@IB!Bz<&Tg0DcHO4*UrCG4P+jPk{ddehT~y_&M+k;FrL!fL{Z@0e%bo4){Ir2jGvupMXCDe*yj*_#fb}z~6ws1OEX23H&ece`A|}17Ifb6yT}A(}1S~8v+{v&j2<Co(Vh)cs8&J@EqW|!1I7jf#(C80WSbH2etsV1YQWd2-phP8hA0V4e%0RTi~U@EZ}9pcEI+)4#3NS9f6&Ioq=6|E?_pWEAR@S07O6$C;?@l0#tz-PzSn!Ilykf?!a820n7tl3Csuf0QLm-0`>+L01JVAfPI1efL8(g0|x*H0tW#H1Fr@S0Tuy^fkT1AfWv_!fY$)81&#!c0+s+r1IGZz0zJTSz*1lt&<h+7oB%8b`heE~Cj$MzNx%Rw2&@2328Mu@z%Z~1cs+0ma4K*b@CM*?;0)kQ;ElkWfYrd8fwur>0dED~2D}|O8+ZqB4sb4T9`H`!eBfQc1;D$33xW3l7XcRo?*%Ra-UqxNxD>by_yF)h;Bw#!;6uQbz=wgWfUALz03QWD23!MN3tR_W58MFU2;2m$0d59v0X`1g3fu<V4txT*1NbCxC-5oYF5qt99^hVJ1Xv5)2Yed%3~)d2S>SWP=Ya=+F92Tzz65+3_zLhK@KxYzz}JCq01pA*1il4)8+aIa1o#f{DDYk2G2nZ^_ksTaegOOscpUf<@MGXVfu8{X1^g8F8Sr!97r-xpUje@cegpg#_#N<j;19qbfj<F%2L1y4H}F5eUxB{?e+T{n{1f<J;Qz)R{2Kr>fu{gZ1)c^x9oP`q2zUmtG4M>_S-`V_O@QYB&jp?bYzjOd*bI09usN^=uqE(9;6=bzz}CQvfo*`70NVmD1!e&+1GWRU2X+8n4(tf*1ndm#0(1ehfn9-D00kfdia-e{0~MeO)POqB4a@;{19k`I0u5ju@Je7lum`Xwuotj5umD&H>;voz><7FG*dI6mI1o4pI2d>}a0svnSPUEr90nW?909xrcr9=wa1^ivI2t$xI2Pyujsung%Ya_sc;EzJInW2Z4mc6$2TlS8fI(mda569itOSOERWrkPBC-F0Q-RZfHvp#tX8>mcZv@^1tOni;yahN5cq{NW;O)TKz&n6*fOCQKfOi7t1MdPZ0NxE;2)qZl2)Gz{FK`L)KH&YprNCvt2Y?R(mjhP-9|EofJ`7w1Tn&5#_$cr(;2Pjs;5y)X;0EAE;3i-Va5HcV@NwW);5OiP;1j?dz$bw_flmQ<0e1uU0QUkTz*^uw;M2fofct^Z0-pmu4?F;T0r(>DCE&}zSAYkBuL55Kz7Bi?cnJ6=@Gaomz{9{Jz;}R0f$sv3h5dBnQ4RYhp2^`mRQLaRc_K51^(M0|b4<2x$|;BS9!K@|4Ka_ydW}tEHog}pb2J9l2id*_rySNR$Ktf_fEnNP90POMmSfYg(m0-fombkpJTK;$fBW`b(5r0YX6ZR6nnU)f9M*dr)q7)kdYz-r-S}Rd%+Wn%a`-Nm)n1Ujx@At<+OceYvh+HZ)?^lk^%|STY<zFuF-LQ5vT;oI)`dA*OWs<TpDewOrL~d8VZFwtF&p2jE9Pj;m>j-~Ww{Nqw=T@lwbM1VZ;^Q%)~in)%lKYBFh^t1+Te9h(<{f~wC{---}D><bJ&(+)3MSxo`0QJ+PFL~=4efNwPE9C={YA}oo8{<^6ABFe6P-#qcv=D_%4>!Opv{LV@_JmSvEgedL2t^DT~8;jZI@VzPDePqd7O(I3|1R!W^vuZ!OGEmR`rw+Q{OtUSrdkjqlYJbF^km4&TMH+y>cO7v|{N>6+TN$UF|~)u)bSe6JpuqcLc0@Vckzm1A+*_r#2EdX9lPY|F9fSZN&3zs@UdT%H$mv?jgUuyM2WoD;9kvp8w_^kO!?SLe*p8a6q67t3lU$X>lMCoShJo1ZMbj-|Df#bLe1rZF4e+b_(~oSSSMlf89ej@E#;7Um~QuVZO#WN}!pv1!c4_v(r{S~Dhx?_ybQgY2yfb9C)=P3>D`9*6bnQ^zvCR}ak57_>Hc-P82Su{iB}V#YT;$G{x6<=AwrG>+$A=an`t&x<))lU{AuxLJD6iC5=YoV0v;F&p2jbLMCbn;gE2Wi=CIuiluGmUEWPPnKTC(pt*muwG-+n2qo47v^ZrO*W3n-nuYHYrtCz^OL35v9va_IIP#$G-l&_b;TU58I!|zu`IVi_SS_tx^}vz_AN4x!+Q0pV;SG82j*xDS{uCXX?o>Yoc292<C~siU=G`IY&upN$MdiAN*kBw#T>0kuQqJlEIsGMtMe>QT0Xs)jqlYtbF_v{4&TMHnhCO3Z_G){Im_lJORr;TEoE_7ud!*&#`pFMb2R5B8^>gCU6`Xa;H`!E$<pgsS{qp$)@y7Uv+=#UVvg2~$>F<LmfIkE>%tseJ6%)z7MaIkz53L#jPKP0b2J964PN&&y>cv0`<|HbP0ukfhiy4F9V?CF`PX@+jmz_5j@G1C8#Zp1o^#^Wc@`%vpI*$y_v)NETEixX?@(FI1lg-M=A`AEW%HAz*RiygvN){Q*feJ2d;5hsnsbwlW3sm{%+VU~*24T`>2)lvjVuo9H8zde_+DKxM{CC9@J%zzZIHcnVUF6`ni|Js_0Jq{EUgXolcv|$G-e%_Ylb-*gVq?=Pnupi7N>n*&iG#5n8UUln~s&nNn00h?m8~di#b}`UX9tfS$fS0>y^(jFo$iu*u1gQ^g2hKyN;{#;ygS7e?KDs9$^0WBRcu}5&8E3^S_^!=O_RBym?>E>p9==d4BSKnD@iHp7Z^l=O^!nc|XkiVZPt<{N(*G?}vFm%=deqpS&OD{V?x``F_vy^Zy|~Pu9MX_tpG+fK$&;{yo6_dw}`(0Q2tw=HCO%zXzCq4>128VE#S8{Cj};_W+-m?*T>|^^aV3>7|XAN7pujTq@nxBp>^eTShz%>w~<}jYlOMlTH7~)wj4D)(6@As~_fj9M*IE76Zr3<7)gGC));}w|}8JvS#7qO>!D1ZCsuE@(X8=oW1#@6F96lS?B2SmBV_DpJU^gd0ggrak6djdBJBY4VBY4Y2)hL_d2hu;pKt#ChHtMzH(U4@pEh(Gmpz0FHW`%KA$!7#D=Yl$!VOladqxL{^*enTMOo}-ejGl$5#&PIew0fW9D(0<HgCg=HK?U$!VOlalN@4UpcJjacwM*?{PF{T}O_Y$JO{XPOtZBzg3R*UN1I|S>wsl2RXlQ%$5(mZpqqc)A%Z9btm$rbC%58`Wx|;Ku7XA&QB|M-_v;ixjy~9vsULmY5mNjdYDX}ktU-C)>1u8S#D!5uB-d}dD9frH1)BT=iX|(Yde>x?dNyXBIoz{`F+0K=O1$C(ec^g``djic@GS-y)y@yIkRtF((w4o`RU(xn!smHkeOq$>9=@vO=4@Z>6v3OD4#ht7v(d@VpF~sC&#06(fB>S&MPf%X?f86^Sm_YY@5dC`SQ9mhi%jNoI_q~=4fs`zOD=BR%=Pu@d<dpT2Fp%zP>$=rsuq{%@<xf@0GuK>bw@^8EJBx@2jb61)pna+$qb``9AaS^t?X!{KH2M+hlg*z~gRd>~i*DjUew|yDpJ~o;fBnC&)8*Svc~h*X<s2zQ5gqMvz&b#!)_x#T>TvVpcxK$^JQJ=5U-I-^M!seQOeZkTnL)q49OT(MC5;7|Y`*U+2plv-M(DKF6v4d5&HVJ$~@H$FbWtuK)c*vEF2jf&DX|WBbdFTQ@G*^UD*)@;J)pv6!QC*O-;hak77oS=ZO%^!UN&@yG8lVzwr04D6rz9NSi}c=3q&=dnDF@_8)gu&o!f@;OfS&oMKH<MjBpXDy#5YYgn4`5ar=%eEFgmd8;(kHs9e^<q{&$I1RVX6A659$$N!_GIR84!OVae7PsvSRP0DI$!3PtrxS`!!1tr&vRrB$7%fa@Aq}ryWjturhDdfeqYq;ozi4uX6EM`n=PKVLC<sIwQE71ktVM>W%1f0zPd?VOP$D_zE3|f=b+Bt^Vjixbvv<klpoZ<TB?&N%cy~QR1Z^@*Tehj>Hc|Hhj-2E-#tTqKb+qWPxbe`PZ@d1$W?n+!*?kgpFDU}zUhZI#qt)9el?br!}=hrZP%9D#Pa!HS`*8G6J+JE-h8rc|6W_i@<Yep9Ls?dWaY5le6sD0TfZolZ@qj}4xAt>hxO)@ZGZKrEfRi^(>Sa*pKROp(#^;71KDC$4(pRSlI@3owpo(TASXE#4(rV)+dlq=&64#EvaP9dSZ_Yr*7(1^^M-^IWaY44#|nCj|Jh%=K8ZQV%3;0vWLwMU1I6o;90plAtT&%*YwP>dzh9TEX^@q}dh^M)R&POXHRf?xZ$8=9>OaoUSj`7nIjm3SNVc{gL*8r;#yJ!Y>&++Ia)0o8f^k@HKAFSg@?4n1dd?ejSkG(39M*F^G{r-Du07_kp6i@B-X5_YtA2F<dhuwl@aCm`$;*%SKrheQZ@u->-mZ0J`m8$P{%<{sIojK;A2LV#w)I}-XixV1XuoyikzVRO6SYs8o;hA$)%~LV&Gw)dkM=ZgUfNr{{Ae%o@~nNvTQBV)Bb%Kbzq5Yka|=6?qsJD<@^`y8nb(O7#4>ap$%rZbSteraRBlX%9Og!GPFW71yiHjSG0{3shdeTgygEy!*w#)Wug;PwSCh%Bvt(Mk$>i0O$Ros`vP`wzkxYB7BboO8NGJ08`1@VCJZ<u1_a)Qyd$a44yt)N>#=o<i-;d?@V^5avA)LMWqxaewYQx>WbFZDPf^26E<*?q~&)N15U;OsHc8&|OookfCdh^M)L$e;b*UpSVwlkD+SZ_Yr_74v|c(0vLgKXzD<*+{SNw!00eQ`V<$Y~tbCqBvc_m6!pi9g6m%)(*4`DEMgz3%=bpFy@9Du?yvlWmW>;4{hk2HDnBIjlFIY-{{*E;CM$mBV@+E9fo$aMrV!gRC6Zn@_g2e1>zS<uJ&~VZHfeTU+07hP5>fvT|5&KH1jlEskfb#yk$|6Q5*j^&jH2nvY`^4(k)2WNZ5|<jwYAkd?!F^U1c{AH1Gm9M+pp=J2>Y7v?n0k@D8$hx18m)Z~ZsTo24)J=Y#{SkHCN9B+?Uk5xaqf4z9LS9tT%zU1Xcd!UzR?YG`~X>ZrMGJRH^aR0X+#T@PJ)(@GZecO6(lOO5Ht{>^QUOd`My=S8KNz*gO>#Mq7w7=ON^y1N;=FLlci<ckmMP8n@&v@&lJtV)c%kS&*`?~zTF2AqK<@~-bzpu;h>+<`${JyUB`?@`j?M=>5dtA3PIa>wU&Kk;Ly}h5a?G_Ilot)!>Z08!~u-<&K?dGQ*o}3wjY-cFtu-<&K?G}$7n4C|8Z09xQus-q0wsRJY^C72kSZ_YrcJp60#^Z-<F)N4l=96uIxzU^?pFy@9Du?yvlWl+X>Uy%iLAEtj4(rV)+ZsQd%ZwBM&W~_duVV$h#UIXk7ITo5!+P_{wwBLuuCyEmSvjmXpG~%7>l@Cnwx+Qx9M+ppwzYbT#~Q0KkHdQN$+lMiahzi{ALmLqtWSKBt?kE<H`{|jRu1dUXOk`W2d5_(hxO)@IXo`Ug*i=gq`Wox;q{_5YT}Td>!E2Z(sS)GhxJ_N%<=Y!^;q?z``3#{dxbYI?Mq&Mv<G^5)_&`)m-cq8t3;nsC*1#&=K^uGw_87Cj`nTqy-j|kCwqRh-+J+AFZG^@+9#9w636SSx?i-vC410`M|+w#FYPT}ezX^PdDcGTt(W$Y{Jt)~ugmZ2^832{zAl&Z`?~zTF2AqK@9XmWy4LUOKK6mn-fd^7Ykqvk-FCJLvYj=Q!+Lu^XWK&`y5Md*#|7EWHOgVV`DEM6Zr}NCJ2M8^&QQu>z4>I@!A+lXmz__8Z09xQu-<&K?dK1BXpZrNoW^0j`DELbTOGZd#UEsgSvjmXpKSZgmt3-&<uk~ZL*=mEe6sDvk6gW*t#6QRO_jrX^U1cx59c!D1X($(*Rg`$;tyv%i#f>3VZHfeTgzuSS6U8(tQ^*xPqwx74QE(e(;zE{_2!dpt=@v(YRu!X-h8sH)qjZ7YCg!yVZHfeTicHzZ?*@6tQ^*xPqyX$;PnLKu-<$!hsWi)Fo*S=H|DUO*N8c+=Xzic>$&!r!+NfB=6HL=daU}<{p-b}y~3N9_9ZVr+5^2jYrpl@OMAQ4mFctUg!{ksDCTHyw|>YR?c3ISnWH_~^P~ONi${B@_e|72X?o^(eO331_BY#uUOd{<ym@JF@$#d+$jh_#8E?I`hvfHl`F&k}Uzgw4<@a^DJk57;>+pM(`F&k}Uzgw4<@a^#{=V*r?($qaLmlzE%3M2J1=-FT%3-~|pR?^-9-1@P&T&DubB%IXZ$8=fte5UF*UpSVwlkD+SZ_X?Z13A|uANVVZ09xQu-<$&*&efKoDVsT!}`Q0*}iqnYm@kcoWv{~)|*eZUGwf^l6(f)a;O~Eo6jcOg+0mo2HDnBIjlFIO}1nFa4s`WEDMMAI#$qI{Nb!;F$Y;WtT&%*YxxZ4O3Pu8mBV`T*<?GmzTpgOYZ}YKVZHfmvK_0pSU*-{9*6abPqMZ84{=(}$1w|s_2!dpZ9j&**&YnCa#(LZn{2s1I6c8QtT&&`;c<B`%xTIY<*kXs`J^>!;*g%}fjO+_+G9>r%~PE>ahyG3Jy!kb{`KO~Ug6D4`;wO*?SWpNwcmQ{rM+G2D$!@u3HSfxxj-E4?bZ*OqkY?YZxcs)vg=3strw5>Qtz3leKMIZbDX}a`$hX(vIm`bw5NIV(%$0bM|+W%XYDiIdT9^I@9XmWy8ON_zpu;h>vB2&{kr_VF2AqK@9XmWy4LUOHa+XU<P7zmqd%RTt%7W44dt-j-p|?gny=lToa2IQ=Njd(-h8s{j;B13oEd{`XDH>c-h8s{wV(fTay|{Ro!6AZdh^M)J8u5<@pvGoaaf=DB-?B6{bmw>kdv5&!}`Q0*^cb`aFWj;TMm`Odh^M)b2ok@S>GVrnkt9&=96uWAD_#{I6+np>vgQ4xA?<Z&teX;a#(LZ+1BzI&XtzKAS;LU=96u0eZv{n)-=e<VSVD0Y^~nnc*bhX<FG#QNw!x1@$asT)qEVYa9D3X+1B=B$eZoK_;;d&!+P_{w%i}Qo?sl-n@{HOxI7o;u%7eAoThxz8a4UhwWE4y@<V#AJ?5~U>zp~>9<d&)esuqO@o2B`=B0hf%a8UzFVEU<z4g-Gu61SltUBTTZ#{}R+S{!kGDrKi^<L&^Pj>xCzxCqLUg|v)wNIL!IbL7Y{i6NN_MjJ!_B3x^+FQK*XfN{etbN8?FYO`ueO-QEm*3ar_jUPwT`uSMb@_c=eqWd0*X8$ht>4$(GyMF9ouSV7(Wo5G7eThOhH_YM@8@j0;Z`qbB;O&2Z08!~u-<&K?E}BrykTd?Aln&AIjlFIY<u?RFKpQPG{|;dQx5CLze7H5yRflU!Vhv9hxO)@Z8zNX#pC&bY%wc`^~oH`_C5P;ljJkVNe+d>`s9w3Y!A6}n`C{1oSdVD!+P_{w#JXo>0_KAD~I(uR{V|nvH0U}m5;?7pZkQv`sDw=fNU+F;aq7sjQ@WJgu{CC$+ot>qu*v9UDF^dhxOy%X&<+>dJB51F^|J~^U1bW|8aiCYCg!yVSO@3vbFsf@@9K5&Y^HvZ$8<U`-9gLjKg~K$s8V+=fWJ;bKaQ4dR`;uu%7FoDIU^u?J<Y-T<6U3_K5XZ^`raOi${BfH!tl=UVgL(dU@7<>#djecC9PZXVnS!f9p}q(cW(TkU847t@koVd$Q+8`>h*~^iuDcsD0A(%<=lF?icNEwg<g<w5NIV(%$0bM|+W%XYDiIdT9^I@9XmWy8ON_zpu;h>vB22ugmZ2^832{zAnG7YyG}%r=t!UdGIUmY}~c)jg260@X&dUN4B`J@zlc(Y?#a()(6?M4f3*op4)ifoEu_}$?Bguo^6m951!lD`4iX29Fx^Qb3EH1pFH>6#?g0O7jsNj|IG1hjepVFYZFe8)jxAQTZ{kCzqlreImqgtIi9WM^Cw4LljJbS>Yq8Dt*!6OU9L&iG|1|oIi78h-~Yh*3EyP(&m7M-$kh+ND~aD^_0Js7HpmNhz97k`$?Bguo^6nKI_iRCeN9&X%<*iEZ}n!f`e%-3Yw=tCo2>qs<Jnq1Z9kf<{+Z+1YJcFKz_!d`TW?&QFLS)SDaTtQ&yUuF7mwDSa=beC@}ql7Io|$Nj@K)c<Mk!wcs<bbqy5&4M|-<BudF)JXA1Xr=A`v}=A`v==A`v%_2cznjmPV;Ixnw(Y97*hBkvcl?=dH>r!gn3Uoj`G7pWhw&uBc_Lt4CRX-RJ3uB9cpg}auP<QDE)+L1fHcj@%5#pF)!T1@WruBDAT-PJ9~t=#FZZb5G4PIq++aw~Vbt6Pw#?cTT3yIzw!z3Vl3dhU9Y`<vCd{G^gsPa@AF{*zIj(Sp4C-%rl(>+<`$C(nJ|l`k3`IqSat8ee?<74dmW<t-jv)9^T~H+lJmC&hB$s2prP4(m-epF9@(R1WLezxuKGZ7k0}bJUjez%eUF{dl%s-aP-z3HoXNnbb7>ETg4o#U%3d_2(9U-Zshef4bf!*01Nq6~8@U<agIBh|ko&T{<d1a_vpA{EzESj%DSrKFDgj<HNnNy!xRvu^c!-Ru1dUC)+;!mZh=0?9!WKIdFok9M+ppw*BB|kB#NselRKrPLP$udh^M)Jx@P6;RiX5!+P_{w$Huo$Rz$CTg=K~z4>I@eYSsXlFuMp4wb`t^U1cCUHY12eS>UksvOpvPqsDw<-fQ-;RIPZtk<!E-s1n$eb*&12U$6+H=k^4`F!5ru1#_nWaY5le6p>rZ};ujCTkjG<*?p-vaQuy&|8gp9M+ppwzc{Xaazp>SvjmXpKNRUG33qmV33u=dh^M)+#kH2U>w$)Pv-ErJQwD$p7X{W*7F)MhxJ?!%wav(9&=dFb<P}bk64dYKe~Utc(hk|^U}WL<wtv<muKy_-g;?o*Sa!&R-JJFw;shD?d{eNnWKH%dM|UdCwqRh-+J+AFZG^@+9yrV9IvnHe$oDBd(ewVdzv>d?JZt@v=@1K);{B{m-dkS_i6Lrr_Fz#HvfIv{P$^dIsbjy{P$_|->1#*=kxpd_U`A;nSW(+pRBUo4`=C3{>OD6Pwuo;wmau6y~*a2$6}w#VLkg-KNi1@<@slh+HxK^X62|K&(_PE=bt(G{d|5uKOOh;^D0*)_as5KJC+4^+?L!qFo*R)R@-nk53=3Q2aet0Fo*T#lWoI2K#=WzK5*>5h&ik`pKKfM9D;23^MPY`Q_Nw#`DEL0zhV3!r*T+sKG`<hrC9tywwRT}dh^M);oipb8Dz_$a#(LZ**4q}+4=_A)>JvHH=k^4e7kQ99J`-n4(oL+yMqd{-OmS(-H|ef_2!dpEuVHjA2@a&%N*95Pqwx7wfp(NvAbX9u-<&Kt<{^|&!=%%Z$8=9>fi3?EoSAg-h8sH?MJ&uwHzvk_2!dpxj%S4!8oippUmNLc`nRhJ?D)%tmidi4(qudn8SLmJ?5~U>zp~>9<d&)esuqO@o2B`=B0hf%a8UzFVEU<z4g-Gu61SltUBTTZ#{}R+S{!kGDrKi^<L&^Pxkz1zxCqLUg|v)wNIL!IbL7Y{i6NN_MjJ!_B3x^+FQK*XfN{etbN8?FYO`u{d|5upWn~t_w)Jvd@kqr^ZEUJem|ez&*%5^t>4ej++|_och|hVanuD@HGaOs$rI#1{qy#Q$6>w6t1fzfEC-It!Peuj-emL1W3f-=u%7*^AB*3{^87PLZ8;AdvvSmrXY1w7^Us{1&+q5+`}t0u7gxUM=6nCL<M&WgXYX$E{<UY^`{-9sNo3}*-ek6Aj>+fDpE1wluwFSfZqVCUCTpC`@nTm0>L*RFbJV%(xI8cBnE%B;e%d_asBGhA={YBwL-wg0)+<N->$p4@=CG|d$F!I|z2=JjFSujnT#v(glXbp9uQJaiO`kTF`czKZ`g%Fkad|GxVZGIu$w7bECO0KAb69UO+cL*wo=ciuIU1+&IUd!g#jO6*=APz1ZSFcQ&x<*_jzO<7uTh#_Ym)u5PvxZ5tydd5F3*KI-W*l0e4Q7^Hofl~)A63r^7DNXdD{N2{WQL}tWWP_>sy|mtna<kmFIk)=KHjxJm=q+$nVFd{eJAuZT60TM)LGGAKG~Hd!I5v{>OC}HargNO}^ug|J*&ufunM;^*F3I*?jU?>{B_cXaDNQ;<vFp|IATa&I8A+9QEVbdU^BwGbiZt`=$JTsgr(dHC8$LvJtCWmQVZn@gp9G^(Kd!46@ZZ%fZ&;u-;_z$z!ok<*=Ups~?Ns#`63#M{PL|9J6xNk7w)U&GXNkpwIVvzTZ39??+uQvtiGai?-Zrf*hVN9*6ZN+w&-JR1UTthxI0#PacbXDu?y#U;SA8HkRj~Icm#!;Fy)8emq+*Z=QeV<j?nfzfaeG56=#(Tb9G~#pAHvWP2W2owFQlJr3(lHlI8e`&16=*}wX+_-!oDKXcTU^T07HNBwxVUfw+a%*mhc`F`(ozyCi6Nr-9'}
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
placements=[('a', 'animal-fixed-octagonal-openwork-aviary-01', (0.7, 0.25, 0.125)), ('t', 'interior-open-worktable-01', (-1.25, -0.65, 0.125)), ('c', 'pet-care-fixed-vented-arched-shell-and-grille-carrier-01', (-1.25, -0.65, 1.025))]
def rigid_point(instance,p):return (-p[1],p[0],p[2])if instance=='c'else tuple(p)
def stored_point(p):return tuple(struct.unpack('<f',struct.pack('<f',float(x)))[0]for x in p)
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[stored_point(add(rigid_point(instance,p),t))for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,rotation_z_degrees=90 if instance=='c'else 0,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values()),coordinate_storage='Exact IEEE754 float32 after rigid transform, not hidden deformation; native versus final GLB bound unchanged2e-7'))
base_mat=len(PALETTE);PALETTE.append(('SceneOnly_EquipmentBayFloor',(.30,.31,.28,1),.97,0))
v=[(x,y,z)for z in[0,GROUND]for y in[-1.9,1.9]for x in[-2.1,2.1]];f=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];emit('SceneOnly_ContinuousFloor',v,f,base_mat,'Single scene-only finite equipment bay floor, no extra counted model');FEET=['SceneOnly_ContinuousFloor']
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
   vv=vertices[i+'__'+name];expected=[stored_point(add(rigid_point(i,p),t))for p in g['vertices']];assert len(vv)==len(expected)and max(abs(x-y)for p,q in zip(vv,expected)for x,y in zip(p,q))<=tol
  assert abs(bb[i][2][0]-(GROUND+.9 if i=="c" else GROUND))<=tol
  assert -2.1<bb[i][0][0]<bb[i][0][1]<2.1 and -1.9<bb[i][1][0]<bb[i][1][1]<1.9
 for a,b in itertools.combinations(names,2):
  if {a,b}=={'t','c'}:assert bb['t'][2][1]<=bb['c'][2][0]+tol
  else:assert any(bb[a][j][1]<bb[b][j][0]or bb[b][j][1]<bb[a][j][0]for j in[0,1]),('Whole instances intersect',a,b)
 contacts={};floor=triangles_of(FEET,vertices)
 for k in names:
  tri=triangles_of(names[k],vertices);plane=GROUND+.9 if k=='c'else GROUND;support=triangles_of(names['t'],vertices)if k=='c'else floor;mask=READER['np'].max(abs(tri[:,:,2]-plane),axis=1)<=tol;bottom=tri[mask];norms,areas=READER['normals_and_areas'](bottom);expected=float(areas[norms[:,2]<-.99].sum());report=READER['actual_opposed_face_contact'](bottom,support,plane_tolerance=tol);assert expected>1e-5 and abs(report['actual_contact_area_m2']-expected)<2e-7;contacts[k]=dict(complete_support_contact_area_m2=expected,support_instance="t" if k=="c"else "scene_floor",actual=report)
 tris=triangles_of([n for nn in names.values()for n in nn],vertices);rays=[]
 for p,d,length in[((-.51,-1.75,GROUND+.35),(0,1,0),3.35),((-1.9,-1.72,GROUND+.40),(1,0,0),3.80)]:
  assert not ray_hits(tris,p,d,length);rays.append(dict(origin_m=p,direction=d,length_m=length))
 return dict(instance_bounds_m=bb,complete_instance_count=3,distinct_old_models=3,new_reusable_model_count=0,whole_oriented_triangles_and_pbr_retained_before_float32_translation=True,actual_full_base_contacts=contacts,selected_visual_clearance_rays=rays,not_navigation_or_full_space_proof=True)
LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate(vertices);result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,1.14);ORTHO=6.45;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(6,-11,6),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
root=bpy.data.objects.new('OneWholeAviaryCarrierStaging',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole scene horizontal centre; continuous bed bottom at Z0; three entire unit-scale qualified instances; carrier supported on whole table';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
  files[role]={'path':f'assets/pet-care/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'scenes','assetKind':'scene','theme':'pet-care','style':'source-preserved-faceted-natural-ecology','title':TITLE,'description':DESCRIPTION,
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
