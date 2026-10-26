"""Static wilderness empty stove and separate intact log shelter: two whole originals, zero new models."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='wilderness-whole-unlit-stove-and-log-shelter-preparation-scene-01';VERSION='1.0.0';TITLE='Whole Unlit Stove and Log Shelter Preparation'
DESCRIPTION='One static wilderness living-equipment preparation scene, one scene and zero new independent models. One complete qualified empty camp stove stands independently on a finite ground pad, with its whole hollow firebox, swung-open front door, open flue, four legs and both carry loops intact. A separate complete original roofed log shelter forms the rear-left storage edge, retaining all roof boards, posts, raised bed and six original logs. No log is removed or placed inside the stove. The foreground of the open stove and the shelter front remain separate visible empty bands. Unlike the old raised canister stove, windscreen and kettle cooking tabletop, this pairs a grounded empty firebox/flue exterior with whole roofed storage; unlike the long splitting-machine, barrow and log-shelter forestry court there is no powered work bed or transfer cart. Both original GLBs retain every oriented triangle and full constant opaque per-face PBR at unit scale under translation only, with hierarchy explicitly baked and faceted normals recomputed. Only the shared pale floor is new scene architecture. No fire, smoke, heat, food, fluid, people or new reusable models. Static artistic equipment grouping only, not instructions or approval for stove placement, fuel storage, fire clearance, ventilation, emissions, heating, weather protection, loads, human access, operation or safety. Rigging animation and interaction not made.'
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
LOCK={'military-fixed-open-door-camp-stove-01': {'bytes': 48312, 'sha256': '1e5f0b3b11cae806539b0ab831f47a38d3f6c4270d7e53aa45e626d303c52f4d'}, 'village-log-shelter-01': {'bytes': 125876, 'sha256': '5058affb0c456d89623a83319ed5bfc689ac114d70d0ab5638c7f744f9ce16b1'}}
ENCODED={'military-fixed-open-door-camp-stove-01': 'c-rlK2YggT*Z!GH?^Q**QB)w{_T3<RmnH;>bVLP&00AN?5E42lO$3w<f(2BpU_nGdWp`B+u?y;J!`@KwwTnvoKeO2h=O*`VA^zU){eK_)yw5&6_slsnbIz1=ZxYAm4D7BE(av2&Lz@#_I-pPQ87Y~QCS?_-beNGcHY+cyAhR&PAf-b}uW<$WdHIuCjzyK0U2?MWMrReY?0He2mXlrWo$X!Tl+={TSp}1_^Yb9=Xm3lIm6|eX6cnU%utnLVlnz5?q~vAhqAX=V<X&n@UjFFF4O^-`)sgB<b)~vfJ*nPQUus&a-8O92u#+M)QgX8<jf?1uDj7U3KPM|aKPM-DO84x7tdaRsJLiq=Ga)OldrnanTA*s!jWv1{<QL_Q&d3@&yqz8YF+oQRK`!UCk}IXpWi7|W+(xnP*;BJ3-RPE&u|Fy1F%e78&KsLG+}7UVVS?Tmf-WZ$^ce-Ez4Xky(K&qZ(u^_#vPWli%`7OGRxD`juiX|~7_x9^Zf0RtL3U<Nu~SFq7mX~I9G%jku%IZbL`B!k+zA5;^CxF@9hX@!DnBy^@iJj#!DU&6nK?Pxqx$C;jU9)unj~X&Wagx-uK79n1>G}8MIv^Ht-alz7WwCO+P&U1TUuHw%G|cdKX;nP=JL2)K3V3n84BI0cG=3P8Kn?IS6VEkKsDi{kk>s+jz<E$>YtrEDajr=+{HbDd8fne@ww1?XK|y@S%)pn;Y;(N%;7T>rdf2z?KVo8^~d8VR^{?~d`_?3lW6aH6l70GvUkp?zZ^c7*X43VIub4N`E2l@*Pd$TRnyLycE;x|uIqL<?H-t!6$wX#u5odSxvpF$BOM(p$j;3!%$^*rnORs^kUg@fFe}o#zI_Jt9N4o@??^j(_vwFG=L}2^EQ#59qq9dz8OO<K0HImK<fz72qmnb~JZaR$jk>u}dmN)l+Vq^X={+@@$@kND(q`JJ+Dy`<ojcT?j8Vg?o}^I+GwS3<?XE<up4=powCiSeJqEkpWbC?}N!n$OwWlRz_v99qoJj}stHU@`4O7)o)@0coF-g;Gx;hN=)e$eI%IvR6T4s~hVVJcJUunx&C^JXl-lY73Vx=RC#*E1-xI8;+N@SHAm7hByKQAk<aNx8FXrJ3Im5;(a!%<RhR8TiHx`(CO+uKX+Dv@;^8(Nyr>-40#onEKgC70%G94Cjgi&TO{bXW7*-43_g>-47Lj@#yP+HH1RUI+FGR4R-#Am#E)x)vXGcth<8G&ELyhgp4RNqvXM=POY#plj!h&i%`%aK>(eqhzSiIlH&ihHp9ww)WT@BV*@wxZJihm(wtGj^cBRC(Z7%JJCLytbqMbR`9vqPUx}uTyX}@6~EQ7s=H&4o6{3-)I9(As6o)>u*ul5rTGwXE|)vbu*n(-SJc4C!(oRSPn=QnmT%O2iFVqoxyc2J>8PDbprn<r%XZs8+~-(sHt%%uZnoRY*=a`-(QWfMZC>=*VaMUv=Wt86x;(`PTbI}E@}}7%N9VE&<H^{zd0Y^Z<sP>~9;(fT63K?o?!ih7E50;$yfJW=a|~SNT_Wu6*e&oH*9dQM?t{_s`JBZ`lPfZa9+$%jzdIwDVI=x73_gc5&7Ef4lk5&-HX(I5i*=;AY>;=lBioj(cw=*WeRj9gV~;nGp7`B}S>GFbAnh(!+>!K^ZzNsCi6vss?zB1VKKH2%rOQ?-J57Eh)5<rJjyP+P-R0r)5}m`Ga@+0bjMJOujP$`#JTw>!x6c+S@;aPuuN?!G=JGky40{gN8WcL59=Ffs@i-#^l~%l>d3_#q+9~I%%ZWMbvDwl*7)!T3-jT;)PoNhu6~sC8z(4T<$`NOAz-rA#QtnOcaOjq+k*my!QI40*A(uD@;v&r@7i&J4PKR9cu`ps)!xHX}JS*|}ibKlfa@o=l=F*zi6Its$Hn+p$@VetI_6}D9eTk{SUH<X(#Pg}|<ThzG5J?WFxljI)(ex(Jlb8y8$&V)5bW#P+W+Iu)$Z3UH8CiK_3*`e+oOp^$`ivP9c`Ocr!pwrPl47m*I8L@Ffy%`tiPpzy#bc~*$G+_`DsaY7;P92Q@34C#!;xSE%GO8wlNbQ6qjYtr$5)=_I}m8)YQERuD^Go=t@Q9GS>I`Mm8-tHeD0GowmkLa9$v2cF1M!~;UgalCmue&vgUosxUXz|x3_%m^OSL4a_#pd<-W4@z20Qphuo;N1ALxj{8v^1!atb>&?z6s80yP|PvRqJ_c_WaaJ!Olp@{;Q(^IY<c<jl<0Cr(dX$5X?Qa&i7z~^*3%FzQCP6%Zd@sb@ix|=cuILF)NQ`43$TXxz&)TL){BDyYgsGm=N^WTU3R=mZ6@upnK)c$L?fh!qR{@SY<CGv_(nbPH|ZagmKmpxZhQde;)Q@UK$HRDod%$ToB<Q11PrOQ=aGcIM)Kl{5xUU4Z?x?I(b$EEzxWm-VhHRDp=j4K(gN9pI~(nno>xFf{5@|`M|W3I~0xEg0wuDBXERj#-i2UTvyRhvt5)qdXQZEdy~xN5&Dm+e&LW?Z#jl`F2=ugVoy?N{YyT(!A0SMBF*ZWnmpz*YNIxooE@H{+`Ps$6l^epRlxYQHKs<EqW2xoSUe^M;vU7`SS`Dwpk4<z`&9UzIDa+ONtLSM68jW?Z$oG*|8CZNB#KVFOp~SLL#usyrT7eNp9RT=h$pn{m}gRUVJ4K9=UHzr2rA8;h_NSA8$d)i{*qs_&{?_OUcqeOKkOkEOZlyDFFcD$P}YRk`d}EUx-qnxju8`<EG)Yop|9Z&I9>E3WpMc$~|dakbaP<6Pd1tGz~XUaq*>Bh0vxQR~0zui|QbR`QCg^;XF%uGT{(uee&@l)U0<{ZaCYtMx?5E3W3dl2=^KUnOtG)!Zq~)qGKUc+4oSVqW=C$*VY5eo^Hrwv{c#c}yz4v-yIcib*preI&VxPsMq;;wlc!IG0ge#hV%DGK#BsQ=FG8u42rLD;X7Us{M+qcvJH6xQauiM{yO0O5TjCm{fHYS23yN&A5tBRabEppGrO+S8=QKm~j=WrMZe*rH99o;wo;H-<7<ITjgI>uHshNQk=&si{T(!OUv-++7e{zYLKm^2F}*cGMvjO&eq8?oXaTA*2y4S8x5STjb*r!Ve4d&t&>5vP6pXJY2a+l46-#d$kt3t&el>x47VP-tYj{jaVc-cl?>OT^e4jEdLCr!d62E=mYl8ghB+nmm*&cDJkIuuAlom3Y`+My{lYK@rJh(^*)rp7-wCq4#=zNLW8iGx39`M$z}dbNWcyB#?K?rX?*!St6J-02Va_t{XLGg;kH);8&0jy8vj)!QY#GjF6lZg`4CgY6v-#_1bJoDwoGrtZ44c1xHh=wW{`%RRHE=e6{cQgF**vx6Z2lTJo10}gmoejP4*J;~^s~9(XLG^N=3q>&<k>te!?}#&Y(B>1TwZZDkNj-z7&x0d2F~V@pUoWuXY<I<=8>PxBR`u*em0N%Y##af++lm7pPkvt@aUPx&(3dtc4jkhc4jNXxs2lM%vOeT8O7Q8&Ckwk2F}iGWw?@I=Qlq)zxmnu&CkwhmYkj6{OtVZXXiIR+wTmV?PW1Jmsgyf{rv3g=Vxa>KiiuOob6Kv&d!8>b|&<*GohdDJC>a7L6)4I8~yC8XyELuXyEMJ=x1j|183((KRY-2*}2ir&W(O{ZuGNrqhXG)xudharVNj+)jHdEbhg(RINNJtaxQPi*&Y;=b9pn)_9>n1O$N^PrZQZ~uzgBr`;^Z1DV^<2I@_Ccwm0c)57ODbqqDt3XM2av_5z))`8wNEbhfAHY`@UiUZAt}TxV;zfwMK-z}b4Pvo+kn*?O+C^;~D`xz5&eovr6OThDbKlkC}%&fa~L;nC;nI(x67vv(GjoV~Nq*}Dk?XYV6)_TIt3*}Ddvy+^R*?0rEQu4LG|0G&PaH*ogc-oV+jdYwI!*V(go182|A4V*nQ*V(giojn6LaP}PAz}d5Fojs%0*|TT^XU~%joIOL<*|TDuJqNbr?3t}4XU}YP_6*j**>hK&JzFlrl?;2fT!t$d_I%Y4^X!?b&ffRM<k9y^2F~8`mElT;y|XLBl?;0ySB5JY_O7iAS2FA!SxnC5dB39Xo(!DN3-<m?XYa*y_WsMj**h<tz1uQy_CCwN`8;Cpt#tN2OK0z`44l2I(%CyH1847{44lt9_P$AH@1b<|zRAGZJ0_jIOEPfw{>Z@jJZ0~RboTy8XYYv&oV^>;**hQuXYYLsoW0-C*?SzFy|2;PyBM9lb1`uCKE;x=_bCR>-k}&cdv9Xk>|Ke0^LcH~)xYZk(a*5)lm9C%6HC6#_kgud)ADdBn}H<i#?blSrpK(WrehvRz%PN=zA7UV$9GnB&2*efd91#lZvW}_|F^Z@bUwytTglx2hh)mzU(+=wfpy8S?!}P*pOA^WHYPD%3B^hv@pwpfFN?buB(Yy4JrDn(Ir-mK9&6l9V<3?DTsY;nhX3c{^OV=ka5>h~e<0oxISVD@lmB$xMAoa*ar=KGZj<$$)n4$Q$QKgXzhd?!k$o+YxIYuwbIW~pJjHXx>G^wl{w8zAPIPW2yLTkq&cHwP3@6dE@#%SVdLET?-A*Wn3Y^+lo{HUndJj64{PFaBDc_ot(DRl=p5KN~=i{gI@#JGHk@G+@GRZ!}EKkmx$Qb-@){}J3m4N<a;yms%(m>+RQIm=PM9(9p&$s^zWXiLr|6}X)X}kY_*$tFWf4QIS{DbA@?G#jrssO7{MSQD3)q&NiDrr=WY5;3cWqhkn^?>!L4od4%ePDguse_WUfM?MeC_R%J0UP1Y87OH6Y(`B`+LW3Do8!*8bUw8Pwx$bkrx~>ZwxSeBoJSV|FN9PjYD1~ORJ5ovY_tQmqqbo6$p*CHTWz|C>_9s;L}?>(03Eo~5G78alNzJ6Ik|u?+-Zyw570yBz;bI!1E!G|5*LyW=z~-n>OdWV9bvgGZ1{nGx){txoq(P2?IH?LXJBX8u|aPaU>Dr6qogaaE9^L+s~fNz?l@7>9oQX~y|CC5*pqrd!bj=AbVzleODO}G0m~P|#$~|Es25l#>I>|PZvpB<{eb;orxWz{2lmIE&L|lG8~{6Aplcv-AntTU$>qSyVYvq^UJ1OC216p9t^i&EsY~f98VVc=%e`P@7;qR30qaX6fFtm&4-KbGU?%MJh2D|Ck+{<jC8L0&V5dKHjRua!odGBr0~`a(gJCfnm`!6LaRrS7j)T-ybPeSIb6|N0Y~%uSX*}2nnh2bTZ^LN<O#)7Woe|Jm2rR^%Oq5IpPKKS4&@}}(1$RcFWIAv<ERTi7S-@E|0}|tCCU7RCuAysbE^sa^&!%~_0JwnWz;Z6l2hOMKP<lPx0K5Tra$#>Fa3StoPm5>?a0%{AguTVU#kjMGZltBarMOcF8#e)O!krngz6!XCmP2A0tpu)w)D*O21#ktVDk8qu0@u<S%(~TdGw^22v+BTGfVW_7)uaY=JMeZ|hi|vg9l$#<w;Isdv<bKgcW$GNbPw<zx(j#ipnHM$Vs4#HE$BYreULhzHq#d17Q}ut+<gG}0A^kl#QKB42hoaJw4NRUK1A)QCAsNg;KOu3YHXoLfR7-4QxT(Efm>0dJtQ9mK1w>IFQIL~ZK#n3$;W_?A?`XNwzdPeqlOO2$AOPiZ%7ZKCxB0&Mo&oY0PaA%WFRJX0(YWDZ%94~e3Gt)bQV1Yd<r$Lgyhq}r{U+J@Z~PxF4VXhk|AJ-@*zEqo&i3C8rhJ17WgcDk^}GW2JS|UIq>oGz~|{X%A+8?0DOT8P<jLH0q((_0+hT6e36P!x`g%u_u@_wO2WV}O-1QadI|Uv?#zOfSAeg;^Go6Jmw_+i&KivG>%iCPHF)|}dIR_d{Cq3DMehLLp$+)<2JHv#ho9HMuWtk2rZ?$Mx|`kyzEAJMyZ@pOfFHnzo8Z|GfgjR)@b1U-3Gfs6>R#Oa2>1~^ycT}?6!<ADucv+V8Spds?SA;_bKvK605v|LFM(geZx6yxUjx5JjfWul4e%TI?P2)oAn+h+JOasYf#1S!Tj8hgf#0LXqmVoVJOsaOgP(o?{(u^fLGs_gf5UIv;isQ~KcU9sko+0=GyL`h{PYX(7u47R$=`s#!EZa^r$2yypvIGs{1f;mJp2?q`#11!)OZ?_M}S8#_PgNOW58pm@f`ej9C)0L!n=p*1n>m>`8@nb;(1)h@$Cc&@dB<FQM#8ju?H97n-G7&$A7`Yd*QzdVlOUDJPRw8fR)56D1DhKikEOz5U*i;s{*TvD&keDEUE#ki8tWgTB444i|UAX;N5DXCdz7x{qXABR9n1>tGaj>o^1eZAnJ*KQC-mx*id``uYO2pi1%>S7avn2aW?R5@d>=!P@IMPXNiws^;2prUdL5c?4uf@39yOy3|{@5nu-Is&P0u~MRQ<t@g=0crWWE;T#X^sM6?996yHGlAf<@UaWxeeh&G}<u)Sz2zMy8JHL$ffUwlOuid0~#_zqgWC!6>hR}0i`DeOSII0P*}kW(DQl_Jg+F5v-sL@Q`&FFF7_2rp`<3LnrXexz2odok``EG`n?!^a(g9fb{=?7|Q9i=UzK7t+NKxSXinL0kg7M063qQfJW(*i8hW$tSu3yNchT<qzsEe!|rewf!O;m@fW=mcQvz@e3|p{6?KbFJLcm1k%UoGVuql?&2t-r8ls*$PkCAhv)<BBTk@{L|?>9U(p-i`iOqOenKEpG|?Z}A9n>xdjfkRax}!m0NfjZJ4aw;5O9#Fgwl#)AaEe=RDsW~0A3*mi^}41aV79dL{2R+ObiDON90sP$xz@>L{4>4TU-siT3m%lX&^=cM~O^PSBwy&fuj*Q^~D(?3z#KFibi6b$OdL3avI|9Sm0PhPF48+8sIgsTtf^I<ALK5IcLK6Ilvq-1~sxp9xxA)(-=O^2j-(j6G%<~PC(=|g^vq>1*mb3I8PJ;3&li4&lE8YI1N5;CUV7O;ABM6d7_<|3Y-e57Vz;5;0$PO32ifhGZ95L_-qz%7Vg+lG8;G>k>G^S<^t!6>x4sGE9L>`2{)qQ2C)RV1QFpz$wJ^lk%oxqCKdx1iv`fwUEBz~5nBDwwiLJ&QK5@V#d6?sXze7f7b}1(5Eb3UWnvX@6>4O_->ZSE#Y)jb+$7cj*B~l-!{2LxYjLL!N^S<;4FC6qzt;iR;Z8r4ECVh>MD&Nh*8|t%PA^!w6?iM6VgMrH7T_(oGZ_BZ0NfyMM>O0fHUc-o|HH&4aS!kwM8uUSxeIs~BH}7U!rj2T#T|%(QQ`sM1L8hJ!@XiNa5H>95|OY4xJBHLXn0sW0(=C%9gVvW0Uts{Tmips1#X4qA>vN)DDYAEc?|rz4Y*A_h#HTG?ZEAbh-=`pCxB0&#&}5X0PcVfa}WtTfjd!Sir6JWz!0J!S3D-320o1_cw9Us!oaWyLdy*C4DcCfng9*Y0-uG?3*h7DfX_kGBvB;h1Luo5&=e9c0AGO5i^O!X2)GD$o)XWCJ-|KCIs-m_5%?ms&V;tTz`gMKb@1^^z?Y!)255L4_&TCy0V3oz;A`S#Xn9q<0el0RX2JJw0^fwD+0d{bxF1n77t!)I@NH<iUc4gS0lou&-iT;<7x*q}tVB$_2YgTb3lXzVybpXIF|ryl@d5Ay+*yN?4}l*dM%E%G4ge3}&dn%!3-}hIW*uVUBj884vjSE=0e*t0S&wM>82B;n+zy|84*XnvhKTu8d;$CdF|tW~BfbNEhp5?zlCObZBWmtIw0sNvR(y#_c|iOG{7L+Ph&d#F0sexxxF6B-EAUtGBO>MxaTs_Q{@;wdzXN|q)NFw7{{;RC%Xf;e#9zR_5DO2&_kRQb7Qdm!VQ~a_1W~gUK0XROiW-kX@)+<Ke7+4nJ`OyN8rvax0(e3^3F&79X;0uf3aMj4XghE{3+d;CrtQRa98xDl1?@>(yCMCesHi=Iiy$SmO2A6mUP!+rDr?W-(jZkqs{*W|y#nbsMOE!ZTooZzNvjU5uI-2P+oGoS60XXSs-o2b*3#aA^t+;t_9m{X+P~nxy1=?xZEc^Zrqu)1)80qv2co|A9<I9hR!?gHY@mIJ(gUKQ_5rT?_|`zH0j#0Dh0>428QK9{4Pl{{b{6m~?Gu!KEY8$E!gYrB8OFCUu(5Ww_Ni#3H32r!zJN!YXf5#BLi-w?{8qHozQolO-&$xXz!dEeN`DmRYTx2&sT~ym7C(!FxW0#{Q?ypN-%9%h62FS`wI6YvtNkI`Xl;RQwZrgqE3Gx|x7L0~3;q<T+UK|$YhQ_GT03An?Js!vZ*h_K8?FmbqpfBK+O;E)J}MmApSV&X)lPE)o!T)-9~W-zZ(J8a%C32VUhM>=N%O(aKFt9sr<Mjx(*!)MX%_=8*4&WtYJQ+!s{jvI)O4VZS_0AmU;rN1;Iq!a&Zt!Z(p`aF;qi*_SvO!e)Tji>?!fNwcxA1o))UwhHL5_e7qAyRURA53T?V`iHEP3`y@9>846T}WiPi_$2Oh5rU-kp`!<~94=@0A=kJpDU2LcD;P6L#r1JmL0hVbPe;2_+o1uKJrgW>Trv@^BKftTaX*%;p;z#-a|S|jZWZ5VJEJbslnR2vQ)u3e39!?Y2=5%B)iC>aSHsb%8Z2yGN_6uh5_k}P1BHX7eXX=8w6;PKHY83!Dvjn&#{*JwGw9C*AH?q&nC;qkG!n+wd<#-lZ<S{^VDEgGujYZHJIV6(Y)jy4fEQEQKH6SM+g0c@V5ou^F#PQsm$C@BOM!sdC}g_;d$!<{UY6akB1r!A~c22Mugj6=y3;1pO+MI1~8PKD)sZJIV6I30G{L+=dW49$ga)3uqvnXoevdS?M=;Z6ZcW&>x#&Lmj$06n-<h>~l8*TRk+7Ow+dhX^b}$sFJuSau+u<^t!!@-%IpHXk@2c3jZA0JuQwfN%4)>w(w9&J5^X2waFeGf{E_@CMkK1&bYl9dTziN)`bZ!HyRe7Xud~Hm^m=65tY8_8~5B1l|bC^R%0^rNE`I(*b&y0hei=@NKEK9Jm~I7C`R`;0oNi9wjS*D`96LEOr5Q!JQjWvI@8gcKooo8n_xUz6d32fNNk`M|`gZu7%~Bw41ecz;&?G33~ei`)WP#ZJo9rxE^+vLGJ+I0Nh!Ql3Recz|IO-ycBpT?yN+~t-xDhrz<Sp2D}aNz6vF`18;}rZkSmcfg52t1M}xj;GNnAwBQcyF5q3T*&Fj`6L1smtV7A&z`J3yALh?Jz<Y3KJxcBc-V2)pF@Np@-iJH4pyYnw{jk{!);9w;W3~;#EPDX>0Hkik-7UZ^Xi=9DSt0oxw7|8=Z^f@jbH(LKKJc2b<Vrpkm-6!W#gtAnF6HBKCC_!1=1M*mPxAfvsr*d)fAIID5_&csPVV`66{-%bP8F$E<SBS9Tn!@6((3^0P)({Fc_v;NS2fb8HZ=q`q^eYjYS3B0v#1`aIQhcyZpezOIElrT{1tnCwB$-Y7FThibeeG$C$YGa=Q>MsB_E5Qj>Fh-h_TYyx@5{R=5e`_kFEozT*=4cQl70#rd-O$<4T_EEX|dCEPgtE5{sYc{59puzp=QIkIr9HuH<8J<zJ=Kj4S`f;!2+DEX|dCEPgtEV#m*W!v;jgYwr50x)s0VyGMeOPi-s$R=nTwizD)bh0v|IyX~Ba{0HNXTXJc4+wDJ=w84x^yOOImm~m-Wa@7ViF6~OL+F-`{_`T%Z5Q(Si(<X)G6)h_*qeo=|Rx<LQ(#Lhi&=cVHmH*<jCy+pU0tvJy5W78<aXKPg6>wszgR@diT=j8Ms)W;#hO0JCS`Bbks)DNqPF%Hch7yr;R7IS=&IF!`^H;-%dxYNIG(rDy(tCa@KH{ss5#D3;N0$7$y9Y=3!q306<PSEzD#DxhJ7&q1{D+@Z(XF_$dt^gxORm~~!CCbz`Ad`a5_v2Bzz%PTT`N8-;4W#u6<6|d9IUvqE63A{%l0q$enp9o%(xr}$(4`HxExQ(m5<E0^o!)mM`m2fD<7G0WmoygjH~u5ADMAE4ocpN%kflpt+@1yYQGg%^2$eMT-jAVGUF=Vq)ycr$@!X7Fn4}rjyLNuB@7-?yp&8y`EM27kuvqEWO%u%uj(loR<2vgFg*b-Z_%Crm$&FwfXiFSsQRV#@N!kZbbEL?;~@(@VJjK#3og&s<T(BcB;c<=0{#jl;IBXe{t6`EuRsF+3MAmKKmz^>B;c<=0{#jl;IA@2@2FwlyAXIGogev0zP7-&)Ec{D4Y~+;5v5{xtW6G}gW6-)tVeF3o9uG8Bp*=z{96O;o*jT4$cz2;Z1Mx;&%ZUMrql`8iF9g4EvXx@8+E1@bT0J(_Monmf_+&29A7KyPU+ac30N7Q>DbLH18d?lJ@O<Z9Xom*pxoKhsS!TYsR=&QsX0E==^T8fqy9P6lg^_HfEQ33U>j-&ls}8t6PFVxf1<A^F8Nb+Y1A?D(?$VcfVu#?&?Uf2phK=vt%tr*vZt7Fxo%6Y_7pQN*MG^?o?^!3J|el=Q_Q%MS9^*XS9aB&V#Zbb)t+L;<+`opt+-tOm0c??_Yu{8E3V|#o?^z8UA3o}aoPUezaK2|kr|icAi4698JFWJx$==2mwu64`N)hbdF3NBuIwrwnQ_&A<s&mL$3e+kaXFsKt`(PlQSG<lN?!TMj4Qj!M`m2bn>r6D{in|Zr_TeY&jbJY^T7MZ_63Vpt<&c}_@$l*Z?^H(;JG7i(Yw8VFd_bM*2}^EJ2&WK=6{zEmv!gV-Bh9{9+z#q=%c$!+8K|p8TxLd?hA`QO^8=q`+lTtcfI{_LR{9BeOG$o@f!OZh8})lqkd!XtEBn9IZZ>KPPtvbz0EgC^RKqH2<`pqR(<tl-zUwbo}d4|Rd4>(k4bac{y#R~uD|x)&q?!3Qfh^s|8t|hYy3}1bNjE=LI)P#sXw27C}}SBJXUn4-r>MENpso$op<ah@m(@pj@!b2?=A6NGF<v=!*ws0_%0bP^%RYNxx{zLaM}KePwy@9T{2vb+g-VPN_>|Lm;PG(;qxWFONL85+kbk##COSXxwibW|Fx2JCLWh-SJ%p~maJp(xLg|>KKx?IIvJ14x?d04U7{x*mu>SddbXsU@wi;OWL>q6#p7~qlx<V%WIQhG%DyW-@wjZ8TzgeJr5?%ov*LC2Dul*tA05t^cR>H{-X@_B8{Hc^Ci25~57-!bb@JHo4<D=v^{Y0`f5i)-P{-Q2hUd&T{d`}r>#p(PuiEc6=;87YytLcD@s-)(eR*?swZ6Q%-f{J_`j<u581(S+9ouf!5AV$jKiRLpp`H6S_X%q6j0^Pd^p<|>ZM6dztg9AIsh1M4l5tmhJ=E`#%)o%|b3!?;Df$QFhX;msdf%Xv%iMcjqj0l&JN1EWePMg6%KF<KX9YH1d3}(}zx>UK(8vX$Q1`U-Fqe1b3jexyItBK%zc9?@`55xLT>fCj;o|pn7mf&9jeqZRwnfe{Z;1(Et1;(wx%`~(@*?M&LEr2MS^0(Q<nlLvIw8V4UHy=5<wx!>^d%JSOMutqGH9C~ZCil*k^7G8;l8t~i#7+MZ8rFw`;qJ6@@Quu+Rl)bPq`lMFJ71X_x`P|^ka842?tJeH~4p;<Hx6GO{*CAu;!5Pg~#TFzI0s`xbxS8I``M%bMN<WJ9}av>)U%nTz*{jJ;C7_kLwxd<OQt!%j-5eJW;RQdTQW=SQLD;*#*0%o$++&_Vm1fm4CT>%WXUK*AL_dPHcI?|J~2Wf-n9)I&7<Tz|z0mFTC!d9t{GbZJWSDm4DOcH98RLdf@8t3l|rKxE@}&&yae7M|-A*8*cqY=XJTiW*%x6UOVoQ(B@|6hkJM5qEEU%FZ@WeS|MK7%D?N6whiCibE|&ziwg`s;(Dz7yYJFNp=Qqx37p*{E5z&a`ObaH<++TNPkCMLM_!lvk=NzEvy$h2<UZo^T!#CL`-01J8SWSE3og&c-^!1M^_-0%ughgPmp?ytK529TrBFqxN^PhzrBW-ZPBqC!)#xH>OLeF|d8rn;$R2r4>!-SOF?r}LYC>J8Aq6On8b_YRHll8%Q*)|7=TcK@NnInqS=|@dmolg|wWC46LDY}hlaq!3htTEZARmnYj-ac^O&ur`m`OvaBXy#2K>2&SovAzJ0rM!EE{Qy!l}}i6=~C)VMbwL?Pyt;={b?%op&2xp2GC%dNdsv%O{Xhp7+ptK(p<WhuBK5mpN7-*G>=BoSh|6-XbCN(F_c3$(lxY<7Sni2rwNo#lV~X|r%D*9<x~To%c(X#mq*?OFQ+r`xtz|%=kmz!yDpbmGOdXGhVBYn(}2@x7H}5L0m|R_T!Cv5a1q@U`7PXul>XWD&`<a6(Q})87fh6IDBP=Wd+NP}`D?Gfs{grgU&8$8dHYK0Cc-!WyuYMviEvr>!kI@B=CW-Q2a8amT=renjmL4;D;e8l`5W8sis)JG_#$aOZ^+$|Hh(qf)1<l7BgaSSJXJ3HqWn@G{?604M09qq_;b?yoHN!(`t|##zb4J49yy*$=c#h#)B6W343&o~|9)I+QPN!bxB3gobLCT|Ga0V@sQPlMT=}$M{ep6F<=^g~&rg~wpDLZnaJ5Fsz9h<Jo2MO_n=qH{e5L)Igt=^+s+$N`ahNEVb>H2xBw;SwwqWW_33J(ZRW}hX>#99Ma@kIKPU)6z52ruui=0{7&&vrP{c(4Q|Lot65eIhF&C3a&cz?HURes>$jlua^r%=(m(*ws{j|JBwZ#(bS@rJ+Mv|{f3VEx6r_4_L17-Vq73a)-FU2pfzG}VRx+F-ENbZa0uVVoYw*w!Y%^+ekrK>Nd1b*rCQGq~yMoIr#3jQ!%}-R{~R{FkGme&YR^;n}l}1p5{~r~kI|8pGe)nY{G=;O6w*p>~gtH^}^0w@T>H>aT)ZQf7v&#;~q)MX=_c#^FPadxg0ktMT7?&whQ*!0d48x+o8+a$eWU7hHZoMt=D9Zyt~M+{$0v7g2e=bX_Z7@VZgEkv`qFb$_Tv|6<N{TKO*8cU4zcb-7)xlk4H~uoY0YtbEO7qP%!cSi}SOHTO}}Zn(4_E5CC+Zw|=Ozpk<))O^d>aMzn3)*qOV6CO0ysaxq^(*K^&fp>=o)=zv==l)&t>kvJZdS|e`XPQB0zwLRU9~Okr$1#@i@M}Su{#D1I-*w;gFxR8c%m}%TheIpFV=d!h&Cz!Hur=T7HO?9y=6YVx7KM&|F)G|_&n}(E1J}drF1ulqKJm5jf$2YwGQ>c%zhU$@WEEF;-?>uvPFtY=RVgQ6rN=5Zx?Qy<R441{P{oT!hKu?y(l3}dH?-#M+yK{U6({?<-W1x}Z<oGh&?rM)?nkTG_<Y^wkVeA;1yAh^ae2OOa9?wI?q4p?ea-7~pK^KbUtX8{(Mq2Cm-~^+a~bYO?jtVGeZl3qFStA(e=9#)$@B5F`ulGcke8m1&sNB`<!^$uMgHCf*?cu*?eg!H*^$lHM5gLN&YFg7z5()8J(9n>k-s-ahJGe;_(0_EHT6V3e<?EfrX(Ui33V>=V41%U1P(+7-x~S)Rluu|!M7t9vgmfWu0$r^0a>&IS^Cw;<U1lm_abK>8TlJxdB8m6)t#vaa^lXo@{zfxAXo2>%zY9v_x{Mx`yfZ2O8t<t&qn4x2bufj$p7aebC-V?YY2@%zCJAScd;^&voA&te-m=(G06XyB3oa9%smIW^h#vytC5EnPzFt=B4podB7fsb16Gavt*cu2Tub%wxi<2*+tyMee6B^_-Uz7S^JbbtGk`PbTHv)b4>*q&0vFN};1XH}Tt=&at00TBiq3M|ggDEc6XGm4Pl&VJKOxSZEhNNQ9-R<pxp_jI<^FNGd{@JA^Q1V=|2oSDlj6ubbe5AQ#ibsW3!gHVePQ`{QXDy;&YlS*#gTjJ?72izT<T%ZLz3dkchTH4DXx4M&HIw#%6HLxGbyh8rF164mA_P9PL(U)MRWh8xbj`}nL|=s`A+FfhO0FvnyV(nSuUIqXSsGloaOQfarUerA<lB)ggDE!6XGnFPl&U8Tvz!x&OCbb%of7=M30_Nbes=E(eq)5|6CZ(GkWwq6X5bV|AeCFpRkoY&P#gqyd=-Mq3HR_AkSr@ZIkCQ9p|@D^!#RM56*jf^t>11@;D!cqUS@y->=4bQjeY|!@MrepP}ga(^4MiRXuuMl{rf&dcHNt8)Vqn{yiusH1+5cA^$^T4f0%u=U-f&`-10FR^x9a&vPj57hae9#VY@@@+0?ABKbJ?7tfWr@3>B`hx^Vd&*FNxf4NVs@+>aTea-#L{l)8Yd86M;o}cjNHac>4e>7(gaGl(DTn2f)KbqGEkk{+cyxua`?snI9fArZxVD_vd{^+v>LtQIhvu7QF>SxyUN1tivT&Gp8&Fiw~Eup4c1ODi96~prrtC->PE9TDkN1y+Mo7D>WqtAaVpTitDc%wi1+$ntA^_V~U+{sYaDh9Z}c8oaCG5WkK#C2N5fR(Sgp3=V)Z59vQ*Ib^LTltjBTltRHE!`e7-*G)A?JwhB?k_IS%dPyv<*mk_*Ny-GBq;v-<gFs_$ImT!Ki(D@cQs_y7a`xaA-^vEou=BzedX^ooq=q)KC)gfGRsEDtYv<!BfoBn%(`*p_m!GKZ%gFYDbf78AFv-XVwqnL1`b9}Ec5H3z@f;5oygorBEQZ=ChS4xJ_a}jIk9{{J{~w8Ik9{{J`p$(nXr66o&n52KHLjg_7r6GlaXupMczIWx%PDA+5?cqUyH2%I%K-?{rFtu@$->=4@Yjj5P7_OKc0oW{YGT<i;;PcL*Bj&nf-EPz`4{DId&d$dHGj{t55}C4ScSoI`~{k4e+@#@^_+FQWJcxq!##G3Aq-?nPpzSD)MH0Rpib1s>qx1RgpL2t0Hg4S4G~AufkPC{||e)Iui', 'village-log-shelter-01': 'c-rlq3A|0!_rUjbt|H1DW#~1Ty?MYp#}p+IN)#1&rp!EJh6X8>p;8nQqLC7%;=R%&LsCj570oG9(J245?!Eh3_qgYtt$x4%@7J$mf6iLpz0cbFtiAWT>zsRCSDyhFwGxc6m3uf_a3W)EI<;>%E~Urt;RPd78jVZoQ!uDtSdS5dhov-1Ilu3)!Gi`5uh|E>)NDSWU{J4uVKvWd*uLh-%mx_^GILVurHm{XHoV{9L13KTAT?!ty_Dfs!2l_ZQlm6HrO{>MQU>)H2yH2y!sqIx3>w@kd?K~``0ht)<5C6|4DTE68nqwUZ@_>aeG2Li7~H4+@V*5DMidOIpPH6}od))RO1~ZhA{~1TF6=p=pi{qI1-()ljTlx~5F4WJ;6Vjr;F3dn4!fXWM2`Uj`d!s=aABXm;Ms7TZqFXW3t9{wFnCz29#@4YeOYRQjO<kWla`s0nw6H8nUhs7wLw~LUieQ=c3M_$T4p*lrRHXZ?NW2|GE=kjvUBRCp<~gj=<#4S!}JAXZ4GkM!=vS9WTZjYysYu#>m{4TfPx;qk8u*|=yhhsQC_FzMx4$`%SzA6%E|aQdOf0`$ADw>IxQ{ga7J2APF`wW9(bG{^%%~jr{<-Ho1$j9xv5~4llJeM!|)!1dL82&vLoS>o}Heaotg;?jQbF`=$ZfODTKSiD<tmK)}pXyK?86D-5=I(V80RlMn(;Kj2JPjU(do31>red*uK+w7oFF>UHEeC+IPI5S=*FGY4uVrI;TsE_U${iydpKFQ98V``wi;V?<(w)apdI(eQ^D}2FyG%U{?Hq*>u1hI$&C|0dtQGm=`}_S}GkeEsYMDo@~gpbTaD<*PxkkgJ#h|GscIrSC6aU-0;D}A}iaouy^l*VV(OGj0&&jRf7i(fdn*Y#6@F<z?NjCrDtPf;UGx0Y1yf{INs=R(BwpNNmd?&Om=2wZoRYyS$UZmxjDJHxp}F%8M)c`;?2y2mqd1MdRBH`R%%90ZYFMgKghn9)lV=)YQ6f2yNn2XlhXN|78xnHG}P-f6R(pEkbZ0fq#rdvMxp^SVgsaSWM{?(=+vTF+h!e)8X_~f4;i_cM^@gQUD6t4XJ+N*<fNsi=fW#9JvRduJ}WgZCnptF7+!aoS*ba6-H#q1Jtq@-=VfJNre)@(<={3X7$DgqW*JN%S^w-~>VNbe<RssNtn^&JEyzvoL3%C;eu&NRpY+_!oXkwHI_5n{Fv4Hoggk>OBz-BR9@79v??PHy@@>e-%l6xbG{2W)dTQ#CjmUOC<)k%8%g78jK~BklBm!BbK}Jr*Dl0uBEjv9v31uJsoRl89`K7^KE+aEHJ0k<PBEc9*momd-8c9dUJhl-M>_%4d-AK#JI(j=`UPs2D_lWTQq34(p1#Jrk^%>C@yQkxJVpIFxy~9uA=unSgeGp+6veS=vWYRm@WIRH8E+$qwLPl;@Ub^`RnK_si=m1%1nOQCuGLj7tzBj}TkewDzRi+*sH9$5zT^+*|GE#HWT?1rgrXI^aq-MFcAsbRsy7?MpWF9p@UL@U`PT{Bla?<mTWf9@^>WYILc$_$fH3+YGT>o51%H~UumKk31xDg<aA4@DBJwjea-m#1T4^gfG(%>oVSVqXmOLHwlT3XIgK4cup5Yg-q_mYI@&xPmApLcN9{JeJTlLs0X!&`TD$H_0*ru_W9Et?F<-(bWYSKDF6z9x))8|+-{=y6QAckd;R?(4^RE$nN`dhTysu+WJ0TufQ7)xlbGjTz^n`<gJ$Mfde%J$LP=A7B4`omgy`aD`=O$M)KUv9FFLQ`UQJ$~u-z7=6>RVZwUubgleY@3jf*wZgt8tmkgZdM>7{*Gl{8$K<tBWXjRG8!>sU88P-fBlLo!$1&k<)7Lq=uOH*Ju&*hT+-t-nml`q2)y9l-(S1!A=c4=iv7Wp3(~rq($B4;m!HCIg&6xFGo3f526Gq>3Y?v^~y~eEf+Js52Hex+@Q`U1aWxZC~PXl(yeaeW*y~dZpH;3HUd>Q+a`;HNldzmlewa9(Sm-XDEx!srbTufQ7RrJ1K#N<9@#N@u?%X;qGPd|p-<&bA%UxwV}kmp`s#=hja+K9<>uMv}HX<tU)$aAtU>$%gl@?-L>>&tqrqR*witmkgZdM>7{*Gl{8$K<tBWXj}T<ICi=X2jT++;@za+{=6!uSM=tzD#nj5tCeM#3WZ6Gr3P0F}>ILv7Wp3(~rq($B4;m!HCIg&6vq^uMv}HX<tU)$aAtUliX{}<XP93Nv<|xJ$F;qb1`MTR@zTLerI&;;x|SvaPFS+j%~_0L+*2SeE7N%_vw9B@!T&LI3<?6VZ_^@Z~JY<&i>^)i%fY!(F@MS8+I9S0bJ|Jwl6p@f4RemaV`s9dC2L!VV7;fIG6sp4?C}Xxx<LD@0Q0O!MPYQ&gFtK8=bqRyi;V#pI6v~dtt;l_v_|va6(JoFyh<4ZBo1yVgs&an=ofh!+Q;VjTrmpMq|l@X8_|~!(J4bvW_JaK780IUJ0=QduPPx8^#92o^8r{uT2=&>S~B3h*cxTxwM1WfY)-73FBOFui>?6#Mt+XXe=4BqjQTX=N#E<Uk2YCom)&8*4EK`ZOS^gm@w>xqjQT1<6LxZF=3pG&MhX4eRV9EFwRBi7E{)_#e{M0I=7fG<Ss|&788ct<>=gE!q`{m788bC?daTM$~u-z815a8&MhX4zUkaz%H&?-%eYoLx0o=_Mdub1#<}R+V#3&0=N1#53AyN#d5fG^&VSlA<*H{t;4B`p)`%J8US#ZR!q|7ioX2A0m@q$md91G=<F&A_DeJkn>p8=S^;}F@uho$Jsm6?R(S1!A=c4=iv7Wp3(~qIALt?|1p|3;s-IuX1i7O)}`)<S}mV6m~BXQ!(dhT?s{Fv;uFYC36?u#$$xtp?{iz(~1(ta9nakZXnuy2tmU$kc}_BCRRRb=dI!q`_`{z_~d6K?#)tFgX*jMu`xrmW`<v1G)0E~c#43S!%saW1;A3FBOJUq9A!*M9mj#uAAQU&dG^`|iuwm&BD3lYKX05=*{}zL7ZbWj%MgR(?$O+L!fOMfb&*_1sNa&&8DWT4_K1cw+x1#U;0&p8wPjYi(1m+OT{6>gq2Warj;jjD1ZQ``$XBkFCcs;Th`+ZQa+8@mko|l*!zSOqk5Yh{;+Rb964o99=6TCUZC9QAIUkv0=goYn>X~YZJ!4I+jdX@3krGSTbSsO~-}_lerg}vfgVGCTnHHWbQ^x=3>NTtxVY=abm<|uYDPOb4XnIGWI3=Zp0*(d>OAr;>4H9+>1<@%*BYwS{XBm6C<X3?Z;&9Mhv;jA@?R<4!;*Ta^LY~>`U%zMojKIMojKyzKp(+`;;$}xfhu-x!3qISt}zZb2nl#7b7NXWyCcfPsiMAuNiTNZOSjzOttTsGslRhugeNE_BCPb+cxLs*f=I!yW8|wUq8lcVP8|$bDvVFs}bwDn6h50&70a9GtNc#HDR2K?(4^T?%Gd3hQ1Do4PS=74%v5K#=a!3jF{}Z5tCT*W%P~2i7)H9)3x$rve&+>*DAU%zO3hN%6cxQtk+8WX~6omQ)J4~xf?Ngtr;<SEf{ljt&Etwc8r+hULz*C)QCy0Hs<JS$C#t99U~^W*NDk$$B4;m!HCIg&6vr)8!?F`UnZ|LBPO}mn8{xIGRf6OOmeRglU!=VBv%`8$?c2a`KhL}ebM74Y<uyAT`w<saA@VQeKKAeVcU!AHmz3FtP~I18?c>>&wpxzt?j+IO@wVPM&BlUHP6=md-3=P+g^-owRzL6wq8#!-V|Zmiw9i$ZtS|rSYOwR|0w-SY#oxZUWa6?_r-v1FGk;VoFro%Ctl3Le<E>fz_u6P^w696`nt(jU)PJj8d%5H>tMikGS>T&jP<^FG5V(CBpK^C@nT#l9k<C?$E_E`m}|*(J(>8BkYSERWF0)2tcfR+eeq-4i_td{C!S1VCLzOX-zIt3k8Ll8*N9DCN1jYxQwbSfvo?8M`>~yjNuKd!l4lY!`bP4eCzBkQka4X@9`<CClM^!Je4E@CJek}h5;EL_Y;vFSWOC2)WOCp1W7~_-H*z2MWO7eW$ncz1^i1`FXxw`9>ImCjeDd-A*IqfJTiD)!Z7=?K$D56Rt=%eYZ@_jk{%}m4n7t3%UW~qtE?*($zYp79jB8bMa;eyQdU1^i+g|*|tQ(8;bq(0|;;|`9i}X4eu$_$cz8J9W#ps)k69cxr7~eOLxb<Wb!wDJ2w8?e-*!E(WqfOSqkL_ek_Qj8FFGk-;ocOWr#kf`^ZataAa6*RHNIrQT`LXTA@S1&&ysrJ&PR1n9__6K9=o`s<er$U&KAWwsJ}dT|?8CMf<Fn$e+h@d{lYQ9sVtjV(x_ENzIoXHpWPI1`!7+Ouw!IjAOHJ<@^WTSUFUGZcchQBh_4MNH5w^V;pB2e<{n++me0C-4;Kz0{Ci~*YwilysBu@O;_TsuzvWs_(-Da;`|5TAF7v1-M<oU{g@0pVqX6$Ri*!Sm7($V9XaPQtBNB8w(ycYH~Wj%M*`E?`Kb1`MTR?y#=aW1;A3FBOJUq9A!*M9mj^mRyV_%if$$iDkB_9by;#AM%%n8cDVqi-Zmd|A((u9Y8?z4m3jR?&U&Wj%LO)^jmsy;j;!KgL}Bqsl6V!-;&pG%5UB8~wJFFUDiX`tnZnd@+mrGs&TS-S*LQp6&5tPI8SMH$K`rjW(Arh68onIMjyrbKC3lUgIQM1N|qFuVh}u^t`*B_V<}@oUPY5)L%MZy~e2H=W^8ejvk-d>+!wX4c5mUKMvV<hpbOrJKaC`oP6Rf;W$a+!6EzZBv>DJyv5n;b6)L<uIUp$4%uHP!RyN%4{`QnzY?}5TThSpamc>M=HhO5jqfDcFL%5p9Ov(nf5_{?DF3+a$$BOn=kK0>NM1F{KW=+HzE}I-J^zsSH_AV5dlJtH+yCzQhve0`+~RKkv-!tsoZ$H<c>W2Ve}d<q;Q1$b{t2Fcg6E%q;`7hcdUqC0D^(b7yX~PK#cN*NZ_k5y)y>Z>P9N~HJyK>lh1Yf{>UeJbI2&Z>SB(9s{p?Vd^HR(D#g!&^DDoPI+PM9Pv5W8;?(t!aA{;BeZ`gku?Py<WAHA*(*Y#}o@yCWS9lBQ0acmgJq4RRLV;f#0eht0H$FXrfUgNmui~VrU(RB{bjn0eOxW}jVdVH^O;(dtsKT-VH8_O4e>f{zz8yt>@@VdhKI<y_eEXJ{MU8s#aza@${uW`KM0qw!I2>YNtU7tkp=C;@4dyNzCL%jcq;wL(e4dXcRb59%(ZhN$aKA!E#)-zH3MAy^7xzTxfwbN@Q*sr7FjgAxF_kTbCpgqnN`*^kg-SZFZuS51XHm@Y{;E=eAjqlYSKc;{F0so81z891AN!Xt3_3IIDapU~m@(=n?_P3b6zC7X~W=~(gUgIRo5C3iX=kN0VOF#RXzW<{3^!-<&asC%R|B24a`12oXPe1=j)c(Kl{)_Cp(fcoIPv3tfYX4vO{D<s&+~+^E{jYrflW3eE{{;Cb$Ui~;`ESfWXiGl7_02!jp5~uK?f(m(KS$?vRQ{pue<lAU8t3oy_g`e+<MIz}|10??(Kvsn&!5Tu8s#5qPxDWr_Wy;y{|fR?kbi>w6Xc)&ME=opGR;43dwp%M_G8UII@V0{kK10K_ZsI|^H0f*<%{u{vo${dxZD41{_z^eD}KnljPj4$UXSn9eysUN$C^9;xZD41{_z?oNjx}Y-+l9s+n&U8!uDg$Kd`qB*<auM<F?o5yxNa7|B!jb<ra7QpUppB<9NjniGQQ~<F?n=_G<sT=O2<+<8q6;{m<qfuW|k^`G>qN;&O|-{m<qfuW|k^`G@3Bqx|ExC;OGK{qK~2wEb%t^X-yjhKJ7q7ip$@WMC6F&SzEIJI%*dN;-~*O>umC;+QnB(c=^wjFZep&#RdDT<kHgWHxc*MAtCsI36~|v>mQh?BS1}O>umC;(LLCjULA_7$=!cF^#Ku`=jQS%qEEEAfAJG4&ph8=OCVgcn;z@i02@lgLn?&If&<fSUe~Cd@TC!?25_1k52mes@q<Fw&K<PcmMa@`ZIOZ?!Vum?SJL(cM^@`_4%0otdaPW^z&7>J^A~Bgzd-r`Ktc6bmZStCv5+-pRan2lO!JgtNwjAem+e0*XZwes6GArokZ=&`uS>f9EbRmu>H?|zUnnjN=k}dq3lfCOOI>tf_>#p$K_)k#<aB_3+>VC+U39w>!U`EI;#Fs-x|&g=<n7qf{ygB=}dz9$WfO#cs*T5jr}8bjG@+bs?neC_U^U4H2Q-Y=W)|b=Q{3s#Lpb(^zgh`OzZZDA2|;C7a1>7M~(d>e&i(8`2TC+yl)13x8A#VS$LhjG-J<)*Ax9MlR%@N+je%h_klg`i`Kdw{rnj8O*hqwtuL*ke;+_Sna1(ZU-ZMR@p`x}UOKYQ$A#yK>#DVG$NB9AJM{OP1Uj<L$H7|FimgA|>pJ?kH;Im{^Kp*W(Rhm0{o?;g@q#@hLHw@}@$rv#H2!sc>4X~Lcuu5E;y+@?*n<-y@$S~9@sIw{_}BG_pGU{PZug6S^kX#Cy>!I?reTftZfzR>=+8+W`hx`VuiO3NAN|C-myYgJSfd|q?HB)%bv`=&b-Rv#tbdb0`^7){xi^W9tn+aW)p&hf5AuJI|AYJ=<o_W5|1<M{$JN#CTHU7GUb+)#od3hCUa%LeJJ5vIb^N29*4X|{htZDKb<eEfV828f`|s({#i<kSUo+fJweFAcUk5bS-5ULQXVG`Imqx!(qdygvwRYU~i^B6^QGaufs(%CiMaDsYaviEGLjQ;#xt==Wf77tW>$x@l#yZa5OJjWKbxourzh@uWkH=g0II3Q8+1XC5==x$^Yu%21V%<we_bIH=-mTw->*4x%>FDq6JCXG+;kfIE4;O=NWIqz=3gD++|B7Ibnzo~#?<UcabuQshjn~)pApV2+|0l=)c_)bQI(zA|Ww+X_yli|v)NviO4!4u|FAsH$M|XYnsLBrZPpG5MKUm*;%@whI!n%(Ch#h02Kx5sl(NCPGm)7xK4*a3<uj@FEz1KKSoAA6?OzZaW{TB4M;NSbvebDU~|LEVhP*0{Y{?T8&o?Gwur6{~!URuXL`kP3jpR0cuAGXJR(OS2opQy`SUo)0xXdV5-dNPgUp}%-Nw|*b4hwI{{(T{T1GbiHL5v|*G{A0W%(&%q_utR@!9ks5bAMYg5=s#YEYP`O#2k{@o|35kY@0nA@Uf=0D+e^QAV7>kPrcF(-j_aWHI%wDNukB8KXTnkSnv+j)u)kYZ2d(2jGJaPF`{_Dr>>sgXtOjVTyEXcg{pcavOQS!zpwXXCYd3S;^_M{7|4$N`7mI1#j((uN7yOHi7pbGh{^$qRlWB~9oCn&wbw<XM;q~&;82@@bUrC_R&tAQIhwX7+wAStDXJ62LdY=_rUs^~1&@P$A@z7tqo?GMfa9zAK`icKnOnTTa7Sp;N=co50kw$;f4*k{ZkL|jS{^cgo7;o5L>u5a1>OuSm@&8Yb|F>#Ko^!nPrcIk{HnL>nH)}_pd$it+?d16f>-70Y*XPWs;;_P!jotbl)cW~nM9Ice3$KXXpRul=e<F5_q1JV((NDY&dTIT<gY%%zKe~?kmO{sg%!|deZbv^*qksDTtK0GU2j_!zFCFo}X}De?YEN~=Jw@Sl_R{+K2mSHV_1+n8SKbqO?$KJeqo1e?ryhC!p>^~F>s~s#PvLs4s6Ew{;Ci?&UK;%<oXVU^dm_(0TI+WG{Dbk5NTa_az;49U_~##8NB@#(^b@b6bu^x0^&tL(`2Q!zKkiMp=|cbJE*uM<jOa-=X=l-Pc2c!oPK)!)z`dh)*k0?Jjn><wooT&o&{$`dtPk^T>qO=q(GTwY(I)LoYqY=m_l|I%%y1(2%Z!*kX=hraKWkSGb!JEBr8W9P+L_ik-^D}5JBJP*4)253IA7AvwEk}QDdF)qgkSG0rYBYYD4(=5t?SLS!v5bqXHM8o>zmG8(S)=!t<fIWVg07IVLPqSp0qQq(H~sr7dLIn4?jmlHTpx^nbyJn2KyWAZ?M0?{s#LS>~FBY!T$bh_xJMZ!oG6<EZa-3IJntnca>;-W%bDWMy(&m_UQXZw0i>T7nUeIs{WvYb)8+Jv0E=y<ozSm`;NZC!G5}qx&!o&*fECs!f2gp^mAdEuWc`l{wx5E{yhG38^>M8`Sl&`IFWg=nAYv#&)Yzwf06Mb_3+=rLw}qP*1dGZ|EA7EpqGQaTfgyLQFy()G`@e->zPQSp9^-458LCuXsz4B-^T!b_mrBk^`&+66YE|&x=%LxdpX#<HC_+b#Y>|fcTZtX#IGY-x8wZuek@F&(cjr%Hyixbb=10!{w32m5A3gXG@fGhT-KDGz;fYGtP{J8wFcRm<*<v{nXD|xvMisKVwG7#kPTT4R+H6Y-9UC@ZJA&pb{s3i%CQQpDm#^>u(MblR*$8#OxB3mtT}7R+OT%)Le`meVVAR0m}DhEmSojg33ei@2(ltOo|R{3vj!j=uu7~hJDpVnS&h|a=dzR8X&_Hy7qBzfMXWo>?yNTJ$~v(2AltJmSOz<vbp+XwWwT3QIa`5j#V%znSYwt2GK-x9(@kZ0AoG~Tny`~tX^^E^GggJ2$I?KiG0tYQ1#AGw0jw8$l0C<kf?Ue(W~<m_HWcJgHjiD+MzQH2r?ZJ{61$150l9`f%6hWitS=kHhOrTBEW3tX$8Ka(*{$q$b|<@s&1VbQV)igw#vW%+vDK`Ijbm4_{vi9a39Jtr%nCskvVLqho5H4noW@47TiEq%Jjn6vHufMJ&8`J`EqjdJz*e%gAlI^+*)!}3wjAVgR?O~TkFXUWSFpR-)9gOB1mqI-EL+6xWwSueVh^w@*$g%Z<Q!JO=CUDdAjpC2el~_Z#Abq=$$GG#8RMHkZelO7^86HDf|rNmCsvVv#<qgo$_}xOY&+Wrav%GMeayaOr}B^CIDxNYudwy(b@nFP#@=Tiu-)u)_BH#4eb0Vmzp_7=;EI>zW%x<F5<i(&=R4SoYy;Z?$A|1ywuQY7@@@7Sdy9R+_JZ8Y-eG&#Cu}Fko$On79DkSX0=bKo=AW_(yc)=A{3}+4m*pq&Dsa@`Kd@4~9LRF~Agjy|vk<S$L%b@N{5N)hNq&G?{CV~r`-MFZ$II+@_6FMwax>%nJ$5|b&)#GE*$b=-zmnJEUEnx_59i}}ACP_cCA^TI!_z>f@$S4X&*AMsw&xCS%FpH3fV_qe;3@npUW+&2={%D+;!SvS-io*3ZFxt25x<mQ&U^A+ygwhrhwzbnG@rm5^V4}9kaf7t&*lwz7RW4Kn`iLWydB7PJe!}-Tkw34`TPRjm*?_kAe-@lyd@vO$AcWt&*NkGP(B#sU_Oy|;#c!wAcyhJd=$Te_XgRUkL6eK%lO40FXjcjCclt(1=*FK$-D7XULRzA-h=1ye!K(74*WF!41a;&2J$vOnZLz%@K-^;%Ae-j_+mZ-<P5%s-@@<a%Rw&Z_woDrLwqO5oqRLDj^D^{;?wx;{7!xkpUW5WCH!IjC||)>@@IJwU&mkK8~E$|4gL;)mw(9b<=69@LEg;g^C^5fzYFADd@8?#FXfMce2mZHkMKo&9>{ro8DGz5^93Lm@J;*y{x<&r<Olpg{yyKzw}9NjKjKgFjr>iJZ}O-3c3#Y12Kh37kH5&D<Eucf;;-;)`4fCK$kqG?zLwAAw}QNtKhNjz*ZAWgALo;J6>*yQ7UZ}5GoB$Di?c-r9F;|;P~tnD3CF2o5C4gu2=YX6m~(Nw$QK-r`eHZ#oPWvp^6&YN{8#=v7a}A|iW5XRQ9)D{)kTUpL(~xsM5@RZxxyB|@lW_y{5LrM;9u~4{2<7K{A>OLFCof^A9xvYfR_?d90GZWmln0e&zyl|qMoosmS_U9i8xL)66vBL$cDlZ<waeQ1~N@l6gi@XI1}WVB2SzyP7#$rRuX54UA(L~8RW_0Q(jH%=ih+*hSwCo@Y>=ekSB?c`Digov=yV_XesUx_lhYXr-)HvmM9P%Kz0!0#rfhAF&N}vafP^2^c8bK&K0+c=AxB2SF{ry#YN&$(M|Ley+wa9KnxQj#8@#wTqkZ2Q^hnfL);~1i}~U*(L%HV*+yJ0T8sALVvrY$^F$}nM+^cvNOTrgi>pL;kln>Vag*pGdVuU9ZWF!4onjuyd7__~BW8-}Ag7D_#BgzoxE<u}Vx+iROcXbQyiwdEt{3A(A;>~8Su_<x#2Aoc#5v*`aiO>X<OSkd(N)|mhJqX_nu&MC$Kp|tkBY_O2l1Qu0^}EByEq_T7EgeDLhKZeh^NICkXuBtcwVd*zk~c;d?OZ$CE`J`Oso(q#j|3KSSMZ)8^k8@rr0Ll7axk<;#2Xp*ekvh2gT3g5AmE>BpwF&uqYBs#d5I<<SOxycv8G7UI+QQcuH&(FN(Dw*NV;JOR-wK0P+R#t$0cNC=P)<BwiE0i2Y(8$bI6lcuVXN--G;Kyd!=RABoRFelC6$pNJjeZIEw^&%^@phIkL;d*T7{fp}az2J$hnOFSdK5?euT759r=*;Jk&bKy|3le|o}2H9HX$cyEfvMk85GGCUGm1RSa4P^~kQ`VB*Kz5UDrH~<coGc^D$qKTnJXNO1vt%7vPo~RE*+|;5xoj!h$aeBV*;#gxm&;S6lqEryl+|Skd7`WcvZ6d*mX~MC1|S>AO0upzT~-5GP1cv^%9G`3AWxGQ$TQ?cvOCD`vbO9hJIMAR+si9thCE+(1ldt$%S)sqTY+pPFO@B1W0?gqOP(W{OqF>c^Q0x4$dhDgkfmiaSw)^F(?F(4E@#UHasbEyvX^{PJ|~xgTq^IDtK?)k6y#7jPhKrY$>|`c%ZYN5yh*MBxkf%Jd&=IjuN)+Y$q{m_yhdIpZ<JHzt@3txr@TkbmkZ@$`LJ9jAD2(b)v`#AlUK?9Ap6S+vX2}r3qcmjesZ{+BBz0zCP&I!<n?kq$no+v`JfyvuLXInd`#XTSIV^@*UFpaGx7<!9OQCYEbowy$Q2-0$h+jz@;<o)<P!O;TqN(6vp~+056CO!3^@nn99bae${}(f$bs^HIYvGtXM&t5d&r+9Q=33;k}t{f>J(K%m51XeSy6o^w}RX%56O*kyW9tIpZrLEEWebes*m9~L9LUo$o2Ad`KH_^-<KcA-STt!wfshYFMpK3%0Hw~N|jV))Jdw6I$2d$JLHRUgWLhfhw@dqMZOL4ZTXsfOMW5ug4`?Lk$dDPawo{0@>_YFdROiOxl5K-pUMiV8pvwuD_KRARVS({aMVyg$Wp2t$a3nStgH^pkgBXgs;ZLeH+euxbwFC`dHJ3EMLrM5%kp>mhTIHtv*hYMdA!;$-;?|03$ly4Qq@yk;5b7KSL0M4kbTr8s!*My(m<xE?y9cJQSCvtSB`3`&Q;fdyhaUBDe5d$OEpmGDpNI5O;mH$O0`jKRY!G^x>Q}Rda7QkzZ#^5sF7;4nxGo1(^Vaib(F2nRt;4a$ShS`WvJGw9msYnTb-|3sC<z5>H^hQ<*H^No2h}Sr5d5egB-8UQ)ARnH5lYzHBog^SF2$lhpEnLl)6Io2H9JURadFY)Wsk#Rt2i2x=?im*;SpXx~WuEA7p*iL*=P{ssqRl>NIt&x<O3^IaN(jH>q3H43IO_ZEBjDsqO}Ox4Ki^q3%-iK+aS5s5xq`S_pEXx=$@oi`0W4A5;&hCF&uy4CFHPh<a2lSF1p-QY+MSb+fu2$}{RoD37V7Q0`avLYW2Uro$O*Ukddn;h3(TP%G7QAfHpK)zj)(H5ue&b)9-jO;R^PxmDc`Wwx3RWwCk~%HweEDL8}e^Pzq_98amW>Us4F$XC>h>LvB6+5~cwdQELmo7Gz&-%@X=E$U769?199JL+xquKEz<hiZrVKz*b>1^KDkrFN^&)Yl-tR$r(u)gHAU<bJhRZB#F-VkigHJ}6(QPoV5n+o5cQa~t6dwtoWkeQ<14->UD_PauC%KdK+pLG=R27gUk@Uae8<psZJ~L)oU@hw`!d9LhIv?t3_c?e9bVbvV9Pzo_4puzrE#uws_9j<XmXmKCy&w@w6kqIH5*$|_@31X<B4XO*=oSXDt*wJKXDTc=nxLDsaYS=Fu6tg}F#Wu0!FVV!N&2U*{$W0kPD^_%)lrCD{MoN3j7QpG9{r8Jx?0q3y22Gr}qQNpTi)w41{W>~3KLo3}nq#DBUt7>5Vtp0$atddYpvMND2)k=X<%W44S4~6ZOpk5M=23D4pYuO-etFhI@a;%mhTUyPm=GHmZ`5@1?&b3-wZLAI;J6P?k3#<#R&LBHmove$jORR1nyIEbWORer!Pmn#WE37N6tE_$?`&qrM7FNEM17)Dq2TBj?GAI{Y?V+3p=UTuSY`+ZZec)(e6<B?(!5{})1FWm9K~^5fJS*GkZ)IAIpft5wL1}Asgwn;j97-=Z*B{Pcdq=3Zf}_7R)EZ%p1v%ClWsSDRS(89cvc_8ztZS_)Ag5S2Sl3%OTDO6`&6;Z6Y~5<z4)S(ux;4YP!<r3pwl&MT%bH`&2RYxm*P3hHXFUM&0c)W((Hdh7hw_lM2+BO`ZYVRYTcAvaa}(hVw%-l)MQ}{C?za|OkAQr{deB;GJ!}<%EVPDMOROQ*NGR7>*Fm|-ng-=g>mDcz;M@{8gYDCxejOZ3tjDa!t*1afWj$%Fw4S!sfLvoeV?ArFwO$1IqV>F0Y^}3i1NoZuiuJO!-g+J6>()kVleNX#26CIV)q2x<+j<}5`_^{rU2BK63*;{AL+d$fm9-qoXVynh-m~6<ve|kS$_sGrIXHvuZ$bSdIG(e1S|3|qfc(Px)cVBw+<F4!6V@_oxAmyC0?KNu2+B*=1}JY>??Cwg&h3UX*uDYkMR4r4YKCfsegyfW^^Mgy)FRX{)EJH$q5M$k&@Wa#9A}1punt?5K~@fx2ptzXDbx~V%TQ+MYiqCdopsRq)%x8MAr&eaDibOfst~FgIyICMIxAEsR4<es$`0j*>`>ECtB?%svA(xt=zA*^+GqV_9kTYpvETa5Ix$o!^qW;F^oLbGR4QbJ%EM7Hlp128<3S!D$_kwjY7#mJ<T;_Tp=P1HP!7nPQ0vesp^Q)?kc~psLr&=IPy>(+Ld`>UL#KzTfvgs)ANtZdIdmGx(?Z``XM}#X4uCvh)eiAcTBr)hDxt5ebqCHZ9$9ITlWqNIoARp57dtg)A2Q<2o7xut@XcbUo_)}Wu`i$au+w>xa7=m4CyzSIK00ihFkZ_p{fM)A$sr@gzS}-rk9~_w82ffywE_DYG4`F_Vk6F_*p#b2`X=s0kty%EYAf!A5u<PO-hKo3!ic}=aB?g*OnBGW3bDO5VeG48$&~e8o3f526Gq>3Y?v_i)v;m9daq3wucc$jgt4!V4HL$`daq3w`|4OS;oiNM6zSM7WxdxXJg&mBA{|R6jD7W9o3f526UJ-l*f3%2t7F52v9I216UM$emP}d4hAGp%_G9!-$C3#T%`X{?4HKTR?!a2T*Cvd8bu5{(-fL6Vv1G#Nn~n_=#=bf>Oj+->3FEbNESWI&)v;m1*jMkh31eR!ONMNdI5A?f*S-wC<&(JbW$a7#-H1sn`7&OM#ECCsUlJR>jD5+z`!e<=ab?6LPK=oDwI8EzB(8iJa+gi+O}-4d%O>|7U&g-VzGlSazGKAXUgpc_8@W&UGWI3+DI+HL8ehh1k^7o2V_$M_@@4Ex?mNDWeaU^zm*H8+A<xN1OrCXp8J^7?@?7o9*q1!_8Zmj6_GP>lc~16a>`R`FeHr_b=U!jNzT~;uh{<!Z5!1c)WAu$YSNk%&cXP;lb6<w{ZVq|h?aSDgystN6^1j=M$$NQUM&HQ$bYI54<bApkllR)bjMpOX>wOvflK1AmjD5-bZePZ}<bAy_<9FI_d#Fe8niuznzqdE7RAKSddUqDt8_O4e>f{zz8~n08Qf3u*Jhy&v;k6yY_IMub9NO1ykG9aq@oJABGyZp&aXc8;q1VE3a10pBq2svi(H8pHZhN$aKA!FIV;<#C5zf=SJ}^!Z&W+B+t9^DTtGLqS4)#ke>leGnM}Ki#dM!FmeBbbzJ80*gFU|@3(0RGX*L|ry9p7u5Wd3`^k3;s|A?p*@PU68K@!+`DCsDj594ARUIAq@)x;`H97H3c5IpH|*KE(U)5kC%z6UX)XN)!)q_IOR~<JF#QJw4*bA^Yx-*GpWxYy9XM9<^VI;w|AgLH_yo<{z?Op7Zs~KXjabNB*JXd$q@pd2IOya+ia73-Xs|{-HMi?)($ImV^29ujU_@|IsmzE&s&N{a=%RlC7s-{-Ja6${We%`>)PFc<*zq&tJ|z@nimb^H20zdOZ`4Lv4;V|IoR3J+~yA@4x!_Cw?w}{`n_?{|VP8c>W2Ve}d<q;Q8mj_4y~rKSBQS8mIe+vUc@t*V<m1v3G5@=$0l}$A5pPb+|qH?=I1fLw$e6i3#cz9PA&b!~H76{@vxr3vX%i<-*IH$n|PEk$zfNNUG7FPwW0+dujBCYV@nj*G(O&zgpPXiOh?|v~EW~z6AXh_!k+cri1;o=HLgO*E%w<BkhL|mk--{>8<BH9bPXljsGrDuji>AdhsoT!uGf?TI+W76Lsb8XT;W**3r)eQ1{a4Cys|2ujkfyJzN(rjd5~vcjZL<Vll1Taelj_`;thbzm>rb{rxmyy+ZWggI92NN9%4~IeeYO`kxa2I^Gk#4ubd(;y;N0ApV2+58^+F|9@8e=dxz3G|PqK|MPbzs)c`dq7ukT(chh@53)Y182;Uf>L9DL27l^zC(Z$RPTcQKv^wf{Cr$u)0&D8}-HH3zK#&9f1HU^l66DCZ-<>G@fBD^s0U!sk1+L$n;CwU4&Hp36J7Mw4+=~0%iO^BMJFyAmCdOR9JJEyJ=Uw3V|Nq^IY>?S;zdMojmw$Jn0AxYj?@shS>USsVfvm@`jQib*aTUrGANlU086WxXy+2RhQ#ST*Jxmz;9{Db!86WxXy+7l%^mm6$82cXi?!7-_U;SMm6UM$rzUyelN4~pg#z($;@6YI){;rV;pS$bX*mv(uI5XqP*uTXvVeG48$&~e8o3f526Gq>3Y?v_i)v;m9daq3wucc$jgt4!V4HL$`daq3w`|4OS;cnB{t<|w%%6hL&cv<URv487f!q`{uwJGaZGGV-yjtvvWzB)Ec82jqIHeu|mW66|tY?w0LYd=QcbS#-L^vx%+;mgoBpX|FYV_y<iMojkIh)FE@GWtg1#Fw!zi4!9xd+p13EfQD0jD1OL_%ik-`|iuwm&BDXLoTw(eaeW*y~dXzH`?UB=F8ZZ+;@za+{=6!uSM=tzKngzy~&rcFS+mdGWI3+H6teXDI=zP?Z@aFxv%*$JUcn$+1Qui*~uZ#y}pcn$#b<4ljmL|CePBojJ}cQWM9U<<T=@h$+NC6<F&|hwJ&2|@@(wO*q1!_`ZD$<&(*#hd_OJte%inL`)R@VV}tL<2H%ej@=uU|g8UQYpCJDP`6tLfLH_w?eLpt%en{~Bkl_1KLHq~tAH;tU|3Uo!XTKl#pZ$NS{@cDE_@DZJss0Jy4>b9IsS<rZu<y+J#Wg2iZBOjK#x~{mUmt~k-)_X)7o~<7`<gKJExcoPY#bBrxO#r9uOH*Ju&*hTxfhu*nTrvVwKC@DT#PxoRz^(bZp3e0u)9ddh6x|6^+A!|YZJ!4I+jdX@3krGSTbSsO~-}_lerg}vfgVGCTnHHWbQ^x=3>NTt&I4=S2o6C!<6-2oABg4TVt_g!q`{uwJGaZGGV-yjtvtgb1yPsG8ZEzYh}zjHcXlBwI7qY8}UV-oEeJ^6TW9omDpaJF!t54WXgK4O<Bj138Qa1HcXhzy~vdHUYjskD<dXzH)1juBPMHQ#J@eXf31!UQ`UQJ!mF!Wu~;%;?5p?MlyxkbFkVZ?h6$6o7nv}bixHExGG-kcrcC$RkICGP82aXu*zjfOYm<HVW$a7h%81Fn8!?F`Uq;_ZocJ=Cdyy%Vz4m3YRz^(bZp36RMoiYqh#?o*<UVD@<X+>;kQ;4sU-M<`OYS>HOzvgAjMpOfDPJaYFEU{=7b7NXWz6J0WyEx^{g}+%h~e4ECeOyc49`wBdG7UP>`R`jjhH<58Zmj6_GR>qJSY1ynR}5blV@FDCTnHHWbQ^x=3>NTt&AAni`nFTx)GE2+P)0$4Q=wi-j}g2dEafs<h{Hv<F&~9bYCWOFEU{=7b7NXWz6J#x)Ia8_G2=4Bknu1zC%76^yTe~QXTTSpD$xy^0}fBlh6H(n0%J#%jg^VoY0ra+>1<^eAeg7WUY*t%-x8|T#T5kl@XWRzNlzVhm)O_w>)b5@v8MtdGfn`h7_IDxNO+ok5>|VH_sZ?sHo2+hitU>V``s>3ktWy?2|FIcQg9-Sm%dr?SC?+_HM?tI#_G2-6Fc4$(Y)^xz^Y%vFrLVwRdxyVPD7A!H=nZBG&uj$JE}<=$nocKc@C>)-efO<j1h)o=jrWms=8hH<Ot3Won;@qigQV)ZWb`CViROyIIHNs_1$qV`}ea5|h46?cGdb(wC`yBG&uj$JE}<Bqn{C+PfLQTd4D}A7dW&;?cJ*%h#_XKVC`f-8?b7w5?y)eoXBXvCcDoOzqu_zUjQ@$JE}<xK=t3`!Th5GmN>GTsJ9GdpE-zi^w`8Won;@$-X3IYVT(Bjl@Y(ruJ^uF^Tc-$1O<wyP3qKFSjK2ZYDA5%hWy*>pbJf)ZWb`CViROyIIHNs_1$qV`}ea5|h46?cGdb(wC`yA}0Hil&QU&Nlf}OwRbbz%WU$ToRp)_%n2ECzD=HUlJZJo?`F6M+2pw^DO3AIOr8UiGPQRz`bM5hlQOk;Gp-eRPEN|y-p%j~W0U9hq)hGI49`?Hc^{FKseK|Q?`x7WwRbc6M&4&7Woqwc9h1@L<fPn!#J`(KO!{(5V((@WlfF#t6ES%XOv=>W%_Js$ncBNq$7J+5IVn?nH<Ot3Woqwc5|h46?GrJ1Uz3!ny_-o)`ZBe5bII+e7cCyrJ(`D;b0jAx=DDZMS^HYo&S85$UP<iT+(oTgGhjoDu)QBs`-J>ny(9KXnA*D;eLJyD)tLXunA*D;*D5okywf7Op2?WnySY`haYg#NeoXD%{L+oHi}X79F||*~(S7k_YVT(BO~;8JQ+qe-n2hA%<lKV9zne)+`f^KR?`9H{zD(^Ca%9bYncBOV#H24%dpGNtToql<WK8YdOk&cPslA&?O!_jlPsq`I@ndT5W)hRWOzqtaYh{x>oRp(EIU&QCHhCQ-<(0(V%`iusysncnwNJ=L@=Q{u_HIVsNZw1z)ZWdwRwNH6Woqwcc#Y(f`$AHt_HKsPY!h;yO3KteAs@MKCS_{xX7r8R$CEO(ce9SkXdX_=ElB*knZ%?ow<Pv%CNb&D)IK2}$umir+Pj&=q%Tu@H|v;;=HaAF?cGdb(wC{dn@LRiGPO_0NA8<RncBOV#H24%dpF}}LCadtjD60WjP+;Ei5NedYP#mO*yqg2cqOrSGk#Wf`-mGH{rPY*ruK>WjGu?b?2|FIcQg9-YTqkj{wHH<?`B-9Z#r~w^ykdUnA*D;Kbs=gP0G~X&G=avS%;)d?GrKCm!wSX-Hg7GI7!OX-px8D_2<mVxCM!SH<Ot3<(9<W%_Js$nc64f=$iX7wRba#NnfV+Zq_lWKW9$H)ZWb`CViROyP3qKFH`$OO!g%yQ+qd)nDk|8?`B-9A5~T{9MRt<iTq|w$&KZU@tCu<yc0bi_ggmlw@h?jw|(@SXM6mZlU!rRjgPiYzb)m9cdRduI&K_lL;Jby^?9#x60L#$lgL*xuVQ-M-A?=a%s0-~YaHsY$9#+9=W^8e;l6HrJ-%1F!TPx4$3fpwQ-9s<bpPCQ@`<;E<0OfP@Sfw`;?H}=Tb#W<=hdF*nm+NP{V$H6yJtMa+3Ry&?a9{DBYyO}is@Y3?XK~iB>Ux#w}j&)%Rgj)jq(q*r}-yQ`=7}_WZ#YQ54ETHC($^6CjXFqkIO%_{jcPoMB^mOKV*N6@(;DA`6p3(kbi>w6Xc&D{{;Cb$Ui~;3Gz>ne}eoI<ewn_1o`K`H~)~&{o?WuZT~CzC($^`@(=mk&nW*;dzya|wf~v?Lq6X#%0JYe=AT6Ee<uHs&;8=^4{iS|`6tmh)c&=M`F6=M!^7u*i!{?cGO&po=d-Hqo#taJB^}4ZrZ~PmaZDQ6=y8e-#z|(Q=T%I6F7}vLGMl(@qHCCR91ojf+78z$_VCBgrZ~Pm@x8#nMvvndjFZf!n8sDS{ZaEuW)sA75YIt82k{)la}du#JO}X{#B&hOK|BZX9K>@F&p|u~@f^f+5YIt82k{)la}du#JO}X{#B&hOK|BZX9K>@F&wrbEUi(HVyO(vH?WNN)-m)j1klzIB`2Uk?oeAyw|D{E{45+s|G~uXv@7{17=<n8jP)Gk?+UHB<H`!XMyMz67or8|`hd-!wooe)F{;!8@FOB}p1&#i$5X~HS9sS%|D&JWXo)?R0-H!ge0s1ZQ@1F2@kveMZkMlsgWE%gUTJ#s~-TMB@&xY5_OXL6BiW>b*q|wio4M&9SabL97?dT`!hCimn)|b}NKddLyI3D`j6YSl35nK<~#Y<!Sr2Z(Jh+izGbvw=v_XGW%pFpF(4Z#lm#X80X+Uq*{;is{`){*(JSUrgUApV2+58^+F{~-Q@_z&Vgi2oq|gZTgF#6Rv$x9K7piwuqhPe$}4o3yiNJ3FabFQ>)%WuSlW=r|Ewv(b8+v@@-@4I1mrlJ%WUo7#r$v|hUNN1L=Wt<nDK-#a?#85v<at<j#eGp*5|wJV1@v*%O^+i8vdkangu&Uf*U@y?;chr|1zHO`l`Gp)bdeM)%z4VyNF?X;d$`J;T&&a|#K(+c~4_nbLlJFRD&xuOYaXIi5@uEY9GZNqk2qdjS7TBAR>&M$7-l#g~=qd%mbX&vluu)o3n2KyWAZ?M0?{s#LS>~FBY!TtvO8|-hezrp?n`y1?Uu)o3n2K)P;+TUE(l$`+b1g2Ogb{T68vNg+L7qc^2S&(H}J}bp4vxXoWvKp)=tHrv3?8e$M!9wgfR)&>h6<AevDobH!u{x|COJ|v^5wlry){?bh?bwB^GwZ@GXQwd9N`frOs<RU8L{<@GMRq(Z&(3BIKsI2NSY38Hs|K<ftIy75C$rN)p2jX<XRwP{caYs#ZPt}_VC_M+XIHQcc0TI}vLnl8m%ui)0@;dP%383-EDK~7I|pW&%JM+wF^e@}C$Z8XOS5LI3OkRbflOnZ&1MVO0FVP%FZLvRjx7bbl-<o%vB_*G$f0Z=yPAz+(?L#W6WJto6I%mv4SSUJWW8BmHi!*lBiLAW4ZDur$fmMe+3oC3b`P7+7P7_cVYZAt&YohcSrHq@u44T`_Gc4VA2yg3f-GeH*l;$5O#?ZNjbyj5>)Cja<JoQOK{lFQ3-Vg_7`uV3WNSgLWjC{D*b{6y$mOh<-N7DVD?qMbcd@70eQXKHCG1(Yh~3L(ft<x2U{|skY!1jdtbomBL)bu&1KIs-410*p1UZxSU_Ud)H-X&5USj3>DZB(P564feBL9qS1-X?SVjJ0Zwh!b!_7VG-eaTMcAH#71U&mfy>)Gq<O}34_&pu$g+2`zQ_6_@<{m6c0e=xxnFUiaBlXxY5GOx~euou||wgZk2*{f^|dmH52>^1fl`-1HSxtG1e_OMUbPLMm<x9m9nF53li7c0#_Wfgcekk$BCtO_s7PvlkLsKI|=rFc1z<@iBXnIC2$UYUn@RWA8&>;RMe0JHe>>^t@gdmfIL+3)NPwi)DR#`$~fc)p*#$M&-qSQmaJugAN<aRwjG$MHTO`|wM6AwP$wflTAwd0n2v+k<S+9p03m%dY`>4IjW$_*uLbZ@|-eCU3->@aDV~Z^PU2j{G8iDZiZe<h^)*K8O$DBl&1Pfj8!-^Ex2waGRga8}clWS-dvS;H`N(knMOjKcBbY`5^Q81-viM<;_4g;{$n1K7x-2Ii8=#$MB(iFv!7tBJaen=EFb^<DK~^eg*FhvNs>gui}^Si$Pw@3wTX_A@2&ZD?gKW<Egwp$ojko&*S}g2ap~3X?!(*p5F@cR(=D2i|^pCf_#-f&EMt^@R=ZI^0oXHem7qZayh?`FW?XI4?upvH}UKEjr=A)jo;4i<oEEod?8=LALftp6?`RsmKX7L{3X7Dzs}#_@9=l|hx}fCJ)a74Dxc4%@acRO$XWbmeg|L5mw{Zy@8XZ}MSLE}dHgZHp3mm@gS?+_=8O3@z7yn5{t$nUZ{=G+Zs8yCC;3MHCdfDWQ+zuw=C6Q!g}={V<j?U{AXo91`6T{0e+J|;d@^6dXYkuV-o{_xbNFlg36M|lYxyqzDgPSe*Zd3qCEvrp1Nj~Qmha{J`A;B!;y>~q_(6UM<RShm|Aqg~h4=-I!<-2zjuQ+HON7Mnq729~qLes6oG2=StSHKfef%r_36v_LJe1O+1QafQ<G=9(d>@ogIJTF7mhy1y<7Gt!af&Dl$H}6ys470=mEqXUD~XT!=TN@k-$VJC{{cmbl2A?(m7shcZvTUq6yL*9NmLUx#aSTF5~qtZ#Mz=A$a<o-s3Yo&43HTjRWuaoA`fJq$QD^5SJ)tJ(O5JQj%W$8rD!Iai*rO9kZnY3ajrODbO6~wv=ep3nW6@ii$!}V=ZO|j@<k4mG&olm&R}~BsJDlsuDC#4C@ukciMU8~5}n0qAWsw3MMrU}NP$vIG=P#R8bN6)T0v<G=Q_d}Y;Oeh25@u~T}3z16J$?ug}72&CHjKwD+)w!(N7EpIamx3SBpWS5M-ekCWeX;Vl2q9Vw4yy#)(NFCyDW5g1A=P2=Yd8y|_V45x0T7O-vPiL=SNpl$qidD3irRC}YHMC<EbKA2@^U6QO<!9DT&i;#P47$UDRgF<sm)x`XU4E)~;67jZe1UZOvgAz~zyYs7U>Zh~{u;0(5pgnEBCrioc%wwMoczPMM+759n7AQy}K#X|9bcm(7l;z6-gJS?67`Gi;|9utp?r$9a>o)jy^(_#(CHR2iZtXM17fm|nw#q;7t@fyh2#4BQvm?!RrvRS+e<puE^lvQFml!xHlA~=KX&q4iFI2MVQ#d@&?<QB0>Y!t7HIUwhVyTk@@r?>~o0<i?jqhbY=)uIT>OK@%joWb@LP+tPa2C-Fa6Yqn3Uu+leiXGx(kROYk;zO}Zd;#(c@u~Pkd@jBP`K|a`d?mgS--G;K>=WOKAH>ffe-;PCLGg?D1LPm#H}ShTEG+pu97291-V<*@IbPzQL*geW`^6q8pNWs4yd|*xC#Xxg2kKlZSxRy^j*}&1N%^)Y0mqvnB;OG4K>0xIhVrG@3*|@gD-<R}P~Hi*?}hqqI6|_tJV{mpSxJ_c6=Y?3D#%l16<JkQlc$3`UDlK}WQwc}vbH=+o+)d|1|S>Ay0V^ZC^JE3$~2iSvt%QXjbx6@m5pUHkj<nmPmvYniBQgw4wO8Z0j0h?8_H>L?i4tK?HN#a;5bF*%cin5$kwu@Y$038vLMUKGP1cmL6(DZvaAl}3|R+Cs?3Jc1kN>wGuU1S>eb<BF3*!~Wk--5WqWy{>?FH@>>@9gon=>f1;{I8H+h-7To!;VkUeD&*-Q2Z*<bdNedX112*@FFpd2KJ%8?*P%HeW^93{tt952VpOJoOmK9p<aI4Fg3FqD4sDk$CI+$C@Z+Xq8^92}R(G4dLDJ;>|jBso!DCocebfovlu$a7^oC>O~~p<F3@Lm424K^YC_CcqhN?+x`!;g}#N%bVmhkkjNX@>V%r-U;$fIaA&)XUTg(-YaLzyX8IdevtRe`Es6IAeVq#A{WWUa;bb2<fHN-`LKLUt^m10E|-tXC*?CBpOH_=JLGM03Y4|-X(&&~N1!|)?}IW2&fNiLu>BFJKMltna+O>yi$NC4HS#%GByR?Jv%FD0D{qifq0EqXL76KTLU~XwgR&CNJqu^BeIeBEg5z2Ff_zDC0J%ZFD%Z=6@(qx0$j$O~xm9ilxm|9PZ^?J$PLMn0`|>^cf!qypxBN(cEI*N7g8Wi`CO?;7$-N-=%02QMxlbMdc|d+Ix5(Gzi%@=%KS23begS2d+yUinIJX7PVEY$P{{fCIa=-jh{s!_l`Lp~<{wiMv`LbLm56b7|D^NDcH=(>MKZNqB{2I!4aPA<S!S)ZK{w5p;<sr#bNF9<PC6!Vo)CnL@P{*s1s<bK(vb;J;ov6yGDj=(<N~)qdSycyFU7ey%RW;NZAkR>zsT6glsspl)I$PCJbyXV3G}S<rQkFU_56djo5K3)zI+SXvGL*7#t`wZZ_S2!>5ROu+zDiX&Aahiv%23&ggXHQDnXZ19LJ4)8Dg&j0stTp1ItxlYl@3LO+p9vo3>@hyPc>1^K{i*8YN}eOb3vY~&QYz@d8$3g_NuKqU$s*ggS=RER2|es>Qa!Gs!LQCb(y*n<dv$sx?J^8y+QU?SE*jAj~WPapz5z$t7fV(l%eWsC<W>YC|y-2C>OxF)^G;fuYmg1aI{wa)BrUc<Zv}a4OYWcKFEC4NDWfC%7)TXwSjV>>I|iu>ItPUoErpZu)Q<X+rTkM6{^u{0>}w!oVrF$R5yUUL0zk^Q<K##Aa7AOsVQoznhA2Inx<}3Gt^xm?^1WDJJsE4F37oRj=D$9Qwu>ZRQIU`YLR*f<U?wSx?YV}qo6#dmO{B--3w)wnhxb=ICnjq!S;Khz7&q@)dT85wH)Mf^{9G8EmLDaj!`4k!)k;Y3uThJ5z4LVb||yed?<_I+{17N+i!>Zjc`1y{ttRoiV^'}
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
placements=[('s','military-fixed-open-door-camp-stove-01',(.85,-.48,GROUND)),('t','village-log-shelter-01',(-.65,.42,GROUND))]
def rigid_point(instance,p):return tuple(p)
def stored_point(p):return tuple(struct.unpack('<f',struct.pack('<f',float(x)))[0]for x in p)
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[stored_point(add(p,t))for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,rotation_z_degrees=0,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values()),coordinate_storage='Exact IEEE754 float32 after translation, not hidden deformation; native versus final GLB bound unchanged2e-7'))
base_mat=len(PALETTE);PALETTE.append(('SceneOnly_PaleSnowCampFloor',(.70,.74,.73,1),.97,0))
v=[(x,y,z)for z in[0,GROUND]for y in[-1.4,1.4]for x in[-1.7,1.7]];f=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];emit('SceneOnly_ContinuousFloor',v,f,base_mat,'Single scene-only finite equipment bay floor, no extra counted model');FEET=['SceneOnly_ContinuousFloor']
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
  assert -1.7<bb[i][0][0]<bb[i][0][1]<1.7 and -1.4<bb[i][1][0]<bb[i][1][1]<1.4
 assert bb['t'][0][1]<bb['s'][0][0], 'Whole storage and stove intersect'
 contacts={};floor=triangles_of(FEET,vertices)
 for k in names:
  tri=triangles_of(names[k],vertices);mask=READER['np'].max(abs(tri[:,:,2]-GROUND),axis=1)<=tol;bottom=tri[mask];norms,areas=READER['normals_and_areas'](bottom);expected=float(areas[norms[:,2]<-.99].sum());report=READER['actual_opposed_face_contact'](bottom,floor,plane_tolerance=tol);assert expected>1e-5 and abs(report['actual_contact_area_m2']-expected)<2e-7;contacts[k]=dict(complete_ground_contact_area_m2=expected,actual=report)
 tris=triangles_of([n for nn in names.values()for n in nn],vertices);rays=[]
 for p,d,length in[((.32,-1.30,GROUND+.35),(0,1,0),2.5),((-.65,-1.3,GROUND+.30),(0,1,0),.9)]:
  assert not ray_hits(tris,p,d,length);rays.append(dict(origin_m=p,direction=d,length_m=length))
 return dict(instance_bounds_m=bb,complete_instance_count=2,distinct_old_models=2,new_reusable_model_count=0,whole_oriented_triangles_and_pbr_retained_before_float32_translation=True,actual_full_base_contacts=contacts,selected_visual_clearance_rays=rays,not_navigation_or_full_space_proof=True)

LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate(vertices);result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,.72);ORTHO=5.5;WIRE_THICKNESS=.0006
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
root=bpy.data.objects.new('OneWholeUnlitStoveStorageScene',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole scene horizontal centre; continuous bed bottom at Z0; two entire unit-scale qualified instances';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
