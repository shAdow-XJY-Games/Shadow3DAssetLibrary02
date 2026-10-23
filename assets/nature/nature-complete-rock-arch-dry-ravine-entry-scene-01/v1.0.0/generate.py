"""Original rock-arch and dry-ravine entrance composition, two complete existing models and zero new reusable models. Lightweight maker SELF_REVIEW; no growth simulation."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='nature-complete-rock-arch-dry-ravine-entry-scene-01';VERSION='1.0.0';TITLE='Rock Arch and Dry Ravine Entry'
DESCRIPTION='One static complete natural-rock arch entrance leading across a short exposed ground transition into a whole offset dry ravine. Two entire existing qualified assets, original evaluated world triangles and opaque PBR, unit scale, bridge rigidly rotated 90 degrees and translated, ravine translated only. No cut cap, rock subtraction, new stone count or altered passage shape. One scene-only flat earth support seats both complete original bottom interfaces. The old ravine floor begins a real 0.22m above its sole, so this composition explicitly retains that ledge: selected visual clearance rays only, not continuous walkable floor, human navigation, road safety or natural geological formation claim. Two old models reused, one scene, zero new models.'
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
LOCK={'nature-asymmetric-massive-rock-bridge-01': {'bytes': 12568, 'sha256': 'd0f513ebea82282482509b6826e06d2ee16f33740941e74db551f3cd98780bd9'}, 'nature-continuous-offset-dry-rock-ravine-01': {'bytes': 13028, 'sha256': 'b1357c3ce1fd9855924f27d1f1466dd47dbad2a63e438d0d3f9f565987740c1d'}}
ENCODED={'nature-asymmetric-massive-rock-bridge-01': 'c-pmDcVJWX_CIXO>VUE;7$TdF?9nFoo6<rlopb@VrKU~V2GXQvbhqrGkD(x<hzvzVhA1wC=6-SEL)0feu%O6%`c&lkR8&;Z-${b<jdC&l)z?4LPfyM{_pE#G=k!})&70gA00v6|zUTumH8(4>QEYTN%`S0#qqxFsGdqkfyF(l=POEg-ZFZ-q0!>5{t!A6a>=32KWr=DOvGQ1jS{yB|F*}?VyA73Pu@Z4}wAfjO4#e@2Yse{%FKiUsj8!NT=lZ^j7TfG5-xt#2=HlyrHHyu3E{D<SjiSt6Rc*JKZLSiB-Rd>XvYAC?cALv$bKBicQKi{fQ!lbO9OeqQ)#wn}j4rpsXcakKXeFw`Y(%vdSEa~RYZsNftyWQm!|t}3L{9YP6d4g2Z6bTM*(P#(lX6;2W>Ga-87s`*B&y8LN?#7w0-s)qc8SjVsw%U~VJXY8m(7{zu$X+x7;L4*YI2yd2!#^N=Xw^tqLx@p=)o7DImY;#j~H)|mKt-61D(Z``n<(Rq*$GDEV`@2WO10wT>jF=%tW!%Wpr7}N@^@lx6xW+w^{4O@h*qk94)pxEEN`8i3u-Jh1y=BsMZ^?s1m<wKyO%?Qg8lF5q7}kFeh9ujK5;n>f#dJE=dsiuk>3@y#b2+0b&>q-xQR1d*Lva;mC*^i^N8gvD$^n6p7<S<wmR194#vH_t0s<mQ~zPZg-UUS|9jjeHlhlVlvz87H6P8vkkNKiHgKYGn3LM<ray(a;LGX+Uj>Bm1(>ZSEa*jH2EY7=I@d!yqw>Da_Wpp$$s-1i@CPMYOKekn5!20E?eB}orY^efFqdU?^&k5GVB;&->Zx+v%`XBzF9We-KAD@E)JII*FIhIlVq<nV-;PwRy6P`U{$M29T{e9lhr$1?utshaeNb0YIK^D>{h#DGS=FAPZmmIWg4yTN2*dP<qEA@9xaKLOZ_sLMxj<HWGb&n;`@<GwK56HwW?^TH^^&O`PCoJxZ~Fg{w9mnDt+G68l^%em#MYQ-ZB64jHa87E-y0WS67=Ix!%cYXKo6A9vYQKqr%Hem6(V^?$1rFk}5S)h0L3qzXTekN~_Rllrm*|a#Q$iH4?Q}qLv1kT5hEgzs&#jVbR`}U2BFys>XUMrQVjwl>R`JGPzWRee;U0WvWogm6)nl-JY~G{&r(da)m}EZ}yEOKF0zd!NN~6%*bJ>vUqP}zlG6-8l`TR*_T#!R&HuuYF4K2`k7fd8HwrQcq!f;7MsaZ=GBp1zXedqTUH?t^6MTHtOq6QL3%R}s_P!qtOpJ2LDuYhzZlE#E2rJz&#Kg2UT$_2;7#w#<hK`1UVSyzM=8a72Ze4MKG~#7xz}Bt_e~Y6RmrqUm0Y5gOTBl6GFlcZ_qR)`kg8DXn^m=3tx(D}QjJ_DmB}>T7FfLRg_s*SkVMDa$iU?bL|iZ_N$z{QumMYh2>539vK!gUZ)l&Jl$f5F^9K*|KZ!u9Xn)D%D!jAhGKEAYk!w_cb<Gq(M0_)Q<)74yu@|VB>gEw>)YnU<QQ~7sDN{+MQk6ue)<jEVl}eS=dt*y9YN<w}mi@_;$yF#;X{8dGLamX=|34K||9QMOGuPa_U|Q`T>V@%Kcfj7JzFV}k-epe5m%j@snKw7TB&)pK$5>IpWpq?{A-)V%vg^?VVeFR#YcH4l&Rnj-b_AHqZ+3aPO7lB=d}y~L{6E;^>t7SRJvKhjT&0$(+7Z4)q4=G>)+-4*{6E;M@g>|2d+qPS*GlAnsQz!0bZv?ldo8|s@r57?8woHmH4~01?xMH`!HF+MkelJ}#-8MkuI(X+KXF><`Uhu{usMUsefxXSoV^>#=Mfq~y!!KG{jH045NonB02`~q$*Nb}<h$nnq$X-6dHbzCr0kzP1@WfZO5%-k(~QvpIQsDWK78<yE+}j{c9G=l9Zpg-V+C>a;TOmk)Ao|Rt3v{C%fhu}%GnRdme0cjaBTc=@>EJEgZy9e09-s%#l8A%PXisI6~uZ&8Q=D3m|=usNC2MxjGV4|CDM>HsYd_~eYcKot-eZjbP);S2y%dWW8;n_2;zi?{z1nTts;ZR#|DMJdFc}3P?Gt1A3=P&_eI|<MP>H=pX0|5uJGZfcWv|t;jQcMqFu!2xy=8n1o2x3^U1EYy-B}wje@wTdbV$V9$UCh5O3UZ+J~3Mz0xX#$4vZ*#AwB2+~s7w5PrS*Wx6TrBl6u3j|k%V_9OH@*BVlB;746B82!_Y-wz;X*NyWC;ZsMy_tj0_uu%~2DRugA!po!R?{WQ%zjIZ^>Y#AsxpX?D>tv#@)zO@1{>@wL_mDw$X#jq|&k=n_<OVV{YIp!%pEQUVww91^RagMtwe@!Lx(LV%8^Z<hrvog$UVM-@LJ)r$cf^P9h*JcGQ;vT^EcP&h&z7LDE9zMy+5ZGt+d~<EFTJ;hq{hBMcFz$9;KOORk=v$TAVXs#0`Tl@X09Un2Qv0}XaL?{9K{!G>S9<QF)RS5%p6JwP3dVkUn>c~**S%@bjv5?OM^}jN85H$Z#)n5(*)p(Q~T*C_X5)W<me9J?_N2DxHDOOW`H0*ad(?<-lm@G_dmzoL+6qY3s!ngsWLo2|2&rrGHu`Y=2uVe|9;(Do>P6RxIO!7$-shM937j&UwW~Q1f$b+^dNorNxeOeU2{o>HH5o7Pt8}&t0xDtKj1U>?Bu$hEFjtiC-nc_HkDiIt|z0O`$@li!)yBnhPIH8tJ_+~PwdSlEo&wt3(k9DzDVY-JXBAPjA^EetONNa2lwgXXSYzg;GE}|9Wkw}4lD2fd^K6JXB+?G{N4IHhPud0@eBEP6k<-uKO2vbzEI38X7d%Q11rxjpUWTaJCd8;;tHtGZQpk1pZf6u{Ug1b19VnrPaspi-^w4FJt06RWZN=MekPRP-rq%fUV4c8qJJ#E`hq<`pVf(#G*Cm>3{IQ+u#P|5K)0(?xee=n(Fyr^`=e+1xYt8HFE6wcR-ct0$ZeuE)oq@_aXq+MueQ*q&u4o|-rJ#PXG179c9w*454aXntAOjSs3EgXbNZk6E#*2jHIRQkzuQxsZs6EC7m~BH&Cc6bnr50P8pyl44%H1VYoU)@PI)3PoNE=*VdpTbrJB4Dww{mdJ(g!@^6<PnN!$}_`O!~`cp)8j4$mp=^mwmIPX6q2eolj%?q4P4TCSRTwvVx27E<Th_qm;S+|RT6LcM-)M=7m%IJq_E+(rH~i<Rzt{u|HSm-g{&?^qq7{<1aSG3=6OUN;FpuAqSm^@7!jeay;NhL6(gKCBDCkIh`7>t`Im*^-)Rm+Yq2w62r5C*m4u!=e?Q&EwJ%LdxdS@}*CBHeSx<;J$h~raY3*>sjAABmsL8aSuPGyPhuyzmt}RyyJ03p4Hcl43x8dWOamk&Gw7c7rHLnQ`VM^pS2ari_M*t3)P2}zj>lfzd+aK={!0Riyn>OYSVi11)+@rc<?>pWd7nE{N{WEy(O`;e)Id?_|l!t0rKH*A8Xw){Atg--?aqjurtZZS^bA2!uXsM^`5rNO;l)BSwBMh?5qmqB@{C|djbBL*%P`iRL~i^fgHL(cjyaY5D9%?01Sp+Fc5}7Zx{+u&=YQf;m`wy!L1MvAus|oAcEUK4PqDtN*D=aVKj_`Xi&fyh=Ev;fEG%i2<`(T+yVE49p*qK+zA$_05?=aIn;m)Oi&NCV1`DhgEDA>1}KFVXoh=W9?XS%VIj<i)vy#6!va_ai(n0`g%xlYbb>_aitl<33=j$_5DxudB20q*kO6}r0#YFzCO{s<!Fb4qT#&*{NB|j3huc99vw(mO3ZWR1zzUNg8D>KjOaTX^!Bnt;6Efj%kONt;1eU`zxEoeNKCFWoPynmo0lcoze%#)DG??AAy*uk)wZ8_l%XVb14Q5XbX5V_T^Q+_{P_pQoZ5_fp-+h>Tzx+HoJ0Pb+`0FzwvRKv4u-NcuYe(>lvm?1xZ}u{@etn;(BluY1-F#YnnBmjM7IX-Q#Bg*%@&H3x+{KqVf)$T8(UJLAi0sY9`i|g^?AgKW)4}Yx!R&>>?1;hai^1%U?cFJZ*)RX9T{D<naP+{3J)^kZ<bezMgvIXnW{~X%FL9quuyLQQFp@26&T~0yMsa)InLuLtE6JDnW!xC4hMYb#fgC)k<XHWg#UF5O&N8yFCWc$trxO_~E+Y4C+p1^v*=xNM63snd-bk)q+^q-AQf|Ys8q)mGYdY4pEjxo-_gn)x)#;Ru)j73%9XG$+MG{9`Z9Vd7S8ny8X7Z7HLu*5Ug!|9SjpS=m>0xzPxzv<SPu?<=oPQ`;7ZQ<8YmW^e&m0`AkMG^aU(Kl`edeq8&wb=$-u<MB{P<*NJ*&^kN43nNgOjgt$6u4`$F4NdzK@>e4)mu1xajol<iPr`xb5yD{?3#l(%JM0cjhG*&(^l{%8{h_Lp33eWjtGF!~Jn&Sj%{_ZT$T_TW29ZTkXfWu+uZhf%mrZY%h+U{WrIM*)(Fk`kbJDwnuDVe#n@{jV`GmM;9F6n;n&$*kvN0?s`MeKifOjPfDJi+xVHCG_|bb*`Big+5Vo$+Q6l*EhU3-XOn1N*I&M+mTcNo$Fsd=edg{-=N8)S<k-Bm0sh$;5c0#$#>Z>o>AOdx$e2Z&d3H9aBAe!DdXU8**7L7Tc#nTBqJ$_`-^H^tQ&@M3Kd3JzZycY`3(Z(Ce%Kk?EK8wpOuxz<8GMju=S@h?&fc7<<LL91apX|e2L7oPgJ_~*07+>MrL3HtPj(K4=9Zl?R-c_Ec1~D*c20!mitRfavrw;v=7iN@d&>5Rl?(NS)n{uiR8K(0+zUBuE;8^k<i*v<`9~t(?}99TG_wC_<n&#U%a2E<FT*XM2l9Cd?g46K*S(R?%W*H@kX`pfuCGUaoroJkIBo(4+!m(bmM{>RbSmx)8MrMBLPnjA`$7(G3sK0Sr{T^p6Ssun$ew55&QOHRd;~J_LfjWhkeQD`PCg4ahC4uoe7zX=1qJQ}3AkaD;+CMreZkAt&A2@zBU_(}Jl}%5#3W?wX~_I%BVW(N?IIh3IR|6UzJkHQoR0-_Ru;?|T6=LY=WM~8p#^h36U;fxPmh~v>ZDRKFXE)GBY5+JJ!rT5tt4vwW_?HSBO?>_-9mPgZQJhd5bpO$U$VtjL%Q5rp3o88-g7GU-05a#I5#?z5yC<|w!LRK!C;|tp7x&q2%YV)+?(akET075&phAneT%BdmD4=0^OUuokF%51#uxaxd#5F6FAOJh&dF)_u6wxMSK`U*kHyl|uey0opU{yfX*4}^VrPK<+m>)H>0}dKc43hxEp9xwRMAA|^pEuj`C)YyJTQenaJUZ@wPlgv>jzTXFPZeN17mfEiHJ7UrqId5x&`R8jQNZo_SWC|RU6U+^v^`((n3CrX65YFMTO_lD|w-G_}&#dR-e^j>%d}GpS>=t!{)`xos%obEX^T)_M$j0+A*8_&G0NQUy{nPbxvI`A)EdqqXUK|a*I1F$?_pFwE5dyj;$^0N2o`Wk9Ffx#dS2@oX@fKzq_zMckJgHnviM?@GsOyAzQXbKlF;EZR;}Vp|(z3LG3VF@!S-;MYTiE_K59;kj|3J*>v5?{`3i5l>X~pdGwvaP#VAg{(ye5JrdFp>YWf~d%@OUs9$Vtr<CP!_jZn>bcCD=^^VnNYslK}-crXWZU2T}Sw4fZ^%Rn`HDv21R70WMS^sQ2tWFfNo)F|S-v4p-L4Gp?`A|CYihN`+$;gXFAusBLoMj|3qVdR@x*;!`fV?OcnNSa8E78c0WWN76N|C8VAWw-zW~4?oG!S{pApA_g-$RiB0e<T7_b}v3w;}%_$X!MtI~s?q%YY1KEOMt9<X=h1V<gC8<j8;0kVC1EGii}&Wg)9cK+dMa&m8=%M-FxieinfDM*KfG>j%#', 'nature-continuous-offset-dry-rock-ravine-01': 'c-pmD3tSY{_dlp<Dw+AHOw)BsQ3BlA_ab}mDgxmP6?{{)zyhnV3$x2xG@oT!KC?_y3$08g&1cHa<fF8*)PDJ>ewt}NwX)L8vh-*Fv$HC9!&w&j|M0_|FL%D@+;h%7Gv|0GJ2xf15deIr1~?W9&_6k8aJkaza@pL<=yGMY&0*uMZYQsdRu0JFoerl<k&PmXzPUC>rj1u5_DWI|X`?hzT7xn|S!Cl~cBcc$>L``6B0}lPKn2QZ)eYoQMvpC5I;?p(r%aaaMJOH4Oz8&qM8y*|f0Zk3C2rp8@>-GM%*%H=Yz}uC@67dzCOK@145!0wcN97c(IVbih}L8(GWk*kZ!NOp?P9w-N8v7ZDst@EIf_Dut)S4FtH{W;XJsi|c3eYYbz~}>K1B{&h8xA5Sy||}A}iO44x{yXHdl^h{0)mo=HT+Nx7O{)mkx7gj2|W~h<r3O$DW(X+b{rQRp?8N2U0-O?3t*<VRaYsw#XXuBYn$8qVbVD>WlPw5UJuYI9V8TcUq>MM+<$CjU0{BF1OWf&qyn>yU?pNrz5vi8SUl^Z4pW*Z_l<n(lT+CJY;((6~$h=6*+jT47Fhx(!KF=DR2Yaysh_*`%LiCtuEV*s484|ueZXtpu)GH!foSutKETy@KPG2dA;GS8JIK5@>HcY)0*$L7uiyk(TXf<uFDpoNcC-^%Z^TG-*(=~r%8M7f3q|r*XBygv^ku1m%l!n1O1eyQkAizV+Y11rz*YkE^A(Xu1^i8HhO2=IlRr9Da~k^zti$?IiGxd;;6WOKJg;EtvD^$T8d6FtB#eHeWJpf6*rOrb5P2MBx(2lkqfx_c~*>)9mS+%&U6;0=h~7n@iK4j)D1oH)(jgaUjlEFG<Yd43~YWnKgfoAm21x!<}A$4!G}l6B=6S5I&+;o%1O`VSXGqTXp(+7y-ugmnhcr<Rg^|0{cxN~tui4&k8^5+PMXx2^eU}htBc^gcHUU!ranw}{^o+W=AukSpE{GupwSxjnhI~a%R4pFW_9P-cw45|rC8qPa@W%(t<U@#Q@v9<)+LkINv+Rutx99kX>|2+$RH_G8}*z@tv2cEa0vG|&dR%UhTxNI&9=o$uZa4&q~UxnsWnC|XVe+J8={vSFzWOst<k7cd)?%2Y^Fia>5QCKeS4oOq!h#Vlm9z4;2R3f<?VTP?~~~hvbx>8J-yIvlWZQ6l$@B7m^4_5*x;mLgZd0qMst|(c1NZ?!^=_EWVP3X2zd>f8Vy=jgO1g}1=66e(O_UT7+DSK3aMsTGw_zn$@{!YFU-oa@gwj#mOQytJW@*YF+@5}t@lnAI`Czs<_unSB`Bwk;#AUJm~<+W&WKx~j?!w4D!o=^G#b^Mmg6G0D3eBSFsgJ0&ZIHu^wQ4Qy>I)-+TyB+$lLMVk`>Akaj_byWU$t9L0B6|UVS@xO^v+4bW1)tw$H#m!)j^J1h&BVzY7-^rRH=RwFZ@NMvl{=-55WE0cjeJ)95$@J`n0U0;sLq{6ONm!0}_mWx}TqyuMy5A3jx-&iBs4*y#*<gPOxBy-}|-nhc!5=zUSB)B*Di1L%8m7>z0ezNfi}NL7?UYf#|}&ZN?-)dsH402=CcAdt8*Z~zVJS^-3RY80@~uk`Gum%42OvCzA*4O3$w@Xh!tu0(KK`D`!5LZDaISQCV>ZzfoI9loyp#C2+w(O+B>K%7%)|FJx7u`&4NYs>46oVp(JhJT0~u;c`9zGN#aZd7UNv3hNBY$obq{6Bp+>GZW?e=Cn}<Pal|&yTlGC=?gE0rX8A4CWTi-pBv)z%!2?p>^Tc4eyD;;@R<OwAb-NLF0Q*o}tgAudRg_<orc<UM`UEeXahWtrm0*h!d1c>G_wh3&G-77B40#Yc|xvRS8ydwN;~Ac<L2_c=4zE_mk?m_s~GNvRt6r)5f6j?zs<HDxc4;g<magVtH}LD-zx|X9?{+@^e{yv~sTKjsNM5+v<gj*Y6U8#bcr^wAbk`8jRyde@id?vOXZb>&+0$mCXJD@xMARqF?9rXfW<FeGOT*^^y<>58HNvTx_w61j6CdHq%+=s}07#7~5KQr1zqM@TjA2(}Ux7$l|JmZ#~|<8<lXeUU+o#?P9R_;D&JeQRjUP#y_TfPsz+x0r4MIA(oSmM+U@O9)5;S2>nfHC|;TGA*-f89}pj{yg)|n=|uzK7Qd~c<60y%7_ZyZ+A_*BBOt!JxTPhmeYJ#N*tLb`o%=%;pC4L6z594!b7j5ol}&raVDZ)~QM9XgpusqM-xWG`<+gx$3-<?Azm*#hS6*_{Zw6``jC-aYAlW_c4T!4}LTJy%(@7wlHh&4-u6VP-`1v2(Sq9AONCV;4-?y=R9bOU;_Zhf_9@@3K-WY3;#k=n*7hkUzK0NNc7zn#RPxR($(71a@Bg@%$P6fo))E1V>-K!<M?(eg7R@$6eIOJIueP!I3pfNsI<h~dh5T75qjdc5==`H+PzvI<jTwrcNN3QNf{)zLVm(e#qdp2m?eqATa(&g=GAl!dPdrQA<&RY1&r>p5ZTPuUYApJZo^#sFC+DW@VcExP(QA%&l)%^JW9<+3jC%Q0InE!UEICs`dp6M6O!r`N3BFi7HR>m0gGfBbnBGEDEo$B8!7Lz}Fx<yu&<+B|Bb!+g4Z?z@s#f~I@NEy{Ge~gT|8ciN(T;gY^ddM~NwIh#^Z{G9gyxKg142T{<jxQ~e<;$(h;{L~VLd%(_%?F2;iPMHXDQsQRft)yB<Y)7_=JA5^Xdm(-UnG{y9x3$YN0NS7?x6T`>t6oVM7~@wse161avIDY$?+@Zd?GC8oYh@UjPu*~$F@&5cgpN8B($6$&iZ<#dC5_;P_(toZ-3c6?aM!BZt?xI<jj3Ve*B!~=gh-rWRn%^ibc6Rk<-KG0K3;?>?b^iWrN5Bb16+1y9i_Wj%5D7OQ~EwuzTIb7Akz#>jkpT?(&muV@(i#=rEkbr592*2UuB_6MA9}xqkh)x%0zraYfQRQc!usyb0VQn-46f>Y0V4OV$iB;N|gRvuW$dvOY=VA^mtizFcmwe7Rg=_m|yM^S=)ZhjupgbmVjV_V+-}Uu08Wh-Xr_w4nHGKAewC@%%EmyRe*05MSH0&(mbVcF%@)D@3`RVRL|$RgoOe?7v%+u#gI|?f$MpWrr;CO?UqsU}afO_L`?i#o<IEE_Ksg9~6+)qsEd&D|x@%U^yQhOec#jRghDT0-DmjfP6G<7Ww^<!;deQ8!VsYu=&8|z{u^@Ldpjl%x!+j6)#?SUx+U{U_SNkcu_8A*xdMP-Zo*%<KqZ7G22h}E5~kO@Uh7xa%P5XF0mX{%lF9qUpJBYr&1}q*9ShkO4K{gS0DZGN!h*bxo%zWpa0v;bLp!|va&3n&4DJ#CBmU^PI}1hBC*UlRX7s5*%OyuB)jjdEX#jm_-rA&TO*Rw+%5h*dY%x|w<WP(<7IP(<^1GoL|!_QM)s^JrUiRr$!mKTlBXNz`{fDC2|M11JT!AK$$YtlUb1x{VcVW2yFYfz<`1if<;&$*)zC4X1?@!h+-VcVpH_Y7*?##^@`Iz?FHa^d?(K13D<h45C>B}%qa{yyo~W2imL(MX<%V32v3giOn;V($7sfPgv69R!<>}fN=bFzh+(~8)&ZTV5usN{tVwkzavuFpmZ;~uuE;r=#;C*_#I>pYjxg<9)moqG1E|*vin<wnNT%O4B<#Ng2-?}lIC+xgjZpiW3d|>%(4zPT7UT)u6ekinnrf?5ln?h^6HidS0Z3_3}wJAJ+SMS&q8o`5j^^T388+62LH|T=bZqOC4-SD3h(Pr2RJ8;|q0*(T_kK_BW2gg0I7stJ@4>sb}JMM#z;22)L<45o@jvvE*9QVUP{PzVSfW{DxV>on&CeR$za2IGG67GhUpoeClg($ce+CXn;1<_!D`=C8ope^))7<dRe!vN?2i4X^!Kmmi`VHgbk;ZX>I9`Fc+K@w^WhY>iAfME~;Di{lo!5A0`y+8*~0S8t{1rrb$4@R(q4Jh;l2bdub#z8E^0}uVc1x|Pz20|$$Knb{E2=s&$7z)E-B5EB0Q*oRMlVB7)0nfl_m<iJ$4btHScoLq6XCVW!U=d`(%P=2uAQzTEHoO8aK>-xOO2~&wSO&#V25&+kyaBI6IaI;hFaeTbGE~46cn5V)g-tkag7q*1o`d&bI&6b2FdOE82WCMvY=^n90CvJW*bO4Q2#euESO_1$E?5dH;8S=N4!|d{99F?0cnv;>&tNsIgQM^k9EN|v8h9Euz*=}0j^JJddj>3r*)!l^&Qs+ud!8E1IpwJdjV(J5Pj4^|=DahQbHP>3?y~SnQyYwfIbRIs+-^fiOH2DRMGeNmod4DLoUFb$m~*vY&a3We)5>!Hyq6n{gE{y5|2`iIbfzMQ<<45_I-eMt_FzoqF$?`<R1Y!v!6rg(QXVxXZxWip8qa>?L|Xd6YV(YP8$FMVtDu7}o;J&Ieo@^`7Je2+!;%Qy8JkM>%p6KH((a}`M|^EQyYURkKb=ll&Sh<9vLXlQv9qK7IIKPAF07Avvb+~9NQxG}IveWIh!)zH_7GXl+L6iC@1{+pNxyw(W;t>;-?uSTuxiuk(un^MR#whm)|W;3A)c5v<#gWgII`;U65-1y2hy|Go5=db%Ch`5yFL^qkv~bnu*c~b>p=nRKauZ?6aC`A>R~x-OyECip?p+NdVFKFc&fQcIJYW-R>c|o;<jwtHS^jv5j1XOG`)ASf$(ddqH8Np6E;?COjtcEpN$pEPZ>R<I=^Q*9hVnJGFE(Az5Mb-I=#mRGaIW4%?V<D^AeeOIF_<}xp=biVP)mww%FQE$mYW7?~8l;#pGB?wDA0eEc*F?eF7VY39rYI7q*Afv&2Z_KN&(!rEv622ToQG8xy&BvO3u~bS!M^dHm!=`tz^r%{zYI<#}#~i^hj9l8qb7XMJaVk+YfQ$oa_HAZJ?$c5H32U$_@L%SPC@-H*N81K6uI#Xhbh_HGYj2kGtOx?=yS#15?$c5mU>e}-X))*Ab`DC|FbVL#^W<Mi0a>9G4#VBZ#v-KGh9z3$kt#bVdl7kj;)*b~NKSJw}FH5GP+{jql&fc=;T`?f*Y9rnSl%#1zRVC>-Hu^+Qw_mm`cZNsrY9D)6sudfOA8}seHH_PFh-<yN|ewjLF3Yow8**nIuS5wHH;JUt>2K&A3+p>kk`d66ePO<6yHF77ouJ3%oeiO>ddV{DBZWZnn_gl2bd?&cBZ&7u9tB}JtzhTt%J!50ZQ!#n1oiz3DE#${FWig3!^64ADR{7!G#x|blBa@{6JF@uGh3$m=qA0p_g+csc-Gjn!*VPn%{V=OPZr(0WX#WEG=iilN%H&g?>R0n<;`f_nZJ0kX)RX^Z?R8mMWy>DKG}%bM7#|_-ydF!cT1C=*kLg7@S=MHjFXzkR<5SG~?+WPVtd%6Z$xQPYE|0!B+vDd8%W1N?iD&U~-&(8<a=x?n%gHLD<_awfHMDF;nE3TebA{xDZd6mL6Xkqo`LkX-5<^$zQSpq2@Fgc>A}8h3uIH-!d|^3q{*HV4YIUb?efF?+%FQQF+3MN-%478J1u^3O^?N;!^w3iL^|PPl$oa_HEawYr1B=;p<?IQ;Diw;{mROY<OSP*p{<gw;)eP&_UDA0-3#?{cuzq#Ms&o(5G9`{mtYqGEhwfOlx?zQS5UX1R)~iUYW}UFQaX4~V$-E~HdaP{*tWQ0#u9>iEMPq%6!ip7xV+__QHC8!-Rf}S^`agMu`Em'}
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




ARCH='nature-asymmetric-massive-rock-bridge-01';RAVINE='nature-continuous-offset-dry-rock-ravine-01';GROUND=.12
placements=[('arch',ARCH,(-2.1,-.10,GROUND)),('ravine',RAVINE,(1.0,0,GROUND))]
def rigid_point(instance,p):return (-p[1],p[0],p[2])if instance=='arch'else tuple(p)
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[add(rigid_point(instance,p),t)for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,rotation_z_degrees=90 if instance=='arch'else 0,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values())))
base_mat=len(PALETTE);PALETTE.append(('SceneOnly_DryEarthSupport',(.25,.215,.16,1),.96,0))
v=[(x,y,z)for z in[0,GROUND]for y in[-2.2,2.2]for x in[-3.4,3.4]];f=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];emit('SceneOnly_ContinuousFloor',v,f,base_mat,'Single scene-only support, no extra counted terrain model');FEET=['SceneOnly_ContinuousFloor']
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
   vv=vertices[i+'__'+name];expected=[add(rigid_point(i,p),t)for p in g['vertices']];assert len(vv)==len(expected)and max(abs(x-y)for p,q in zip(vv,expected)for x,y in zip(p,q))<=tol
  assert abs(bb[i][2][0]-GROUND)<=tol
  assert -3.4<bb[i][0][0]<bb[i][0][1]<3.4 and -2.2<bb[i][1][0]<bb[i][1][1]<2.2
 assert bb['arch'][0][1]<bb['ravine'][0][0], 'Whole old bodies must not intersect'
 contacts={};floor=triangles_of(FEET,vertices)
 for k in names:
  tri=triangles_of(names[k],vertices);mask=READER['np'].max(abs(tri[:,:,2]-GROUND),axis=1)<=tol;bottom=tri[mask];norms,areas=READER['normals_and_areas'](bottom);expected=float(areas[norms[:,2]<-.99].sum());report=READER['actual_opposed_face_contact'](bottom,floor,plane_tolerance=tol);assert expected>1e-5 and abs(report['actual_contact_area_m2']-expected)<2e-7;contacts[k]=dict(complete_ground_contact_area_m2=expected,actual=report)
 tris=triangles_of([n for nn in names.values()for n in nn],vertices);rays=[]
 path=[(-3.3,-.10,.9),(-1.11,-.12,.9),(-.13,.03,.9),(.89,-.22,.9),(1.97,.13,.9),(3.2,.28,.9)]
 for offset in [-.04,0,.04]:
  for p0,p1 in zip(path,path[1:]):
   p=add(p0,(0,offset,0));end=add(p1,(0,offset,0));delta=sub(end,p);length=norm(delta);direction=unit(delta);hits=ray_hits(tris,p,direction,length);assert not hits,(p,hits);rays.append(dict(origin_m=p,direction=direction,length_m=length))
 return dict(instance_bounds_m=bb,complete_instance_count=2,new_reusable_model_count=0,whole_triangles_and_pbr_retained=True,actual_full_base_contacts=contacts,selected_visual_clearance_rays=rays,exposed_ground_gap_m=bb['ravine'][0][0]-bb['arch'][0][1],original_ravine_floor_step_m=.22,not_navigation_or_full_space_proof=True)
LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate(vertices);result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,1.0);ORTHO=8.3;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(-7,-8,5.5),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
root=bpy.data.objects.new('OneRockArchRavineEntryScene',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole scene horizontal centre; continuous bed bottom at Z0; three entire unit-scale legacy instances';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
  files[role]={'path':f'assets/nature/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'scenes','assetKind':'scene','theme':'nature','style':'warm-handcrafted-village','title':TITLE,'description':DESCRIPTION,
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
