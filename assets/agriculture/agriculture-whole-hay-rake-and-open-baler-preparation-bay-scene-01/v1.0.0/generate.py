"""Static complete high-wheel rake and complete open baler equipment bay; zero new models."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='agriculture-whole-hay-rake-and-open-baler-preparation-bay-scene-01';VERSION='1.0.0';TITLE='Whole Hay Rake and Open Baler Preparation Bay'
DESCRIPTION='One static agricultural hay-equipment preparation display scene, zero new reusable models. One complete qualified high-wheel curved-tine hay rake stands on the left, with its whole wide wheels, swept blunt teeth, long forward draw beam, parking prop and rear seat untouched. One complete qualified open-side long-lever baling press stands separately to the right and slightly rearward, retaining its entire empty chamber, outswung gate, raised platen and long inclined lever. All oriented triangles, per-face opaque PBR and unit dimensions of both originals are retained; only rigid translations and explicit float32 coordinate storage are applied, with old hierarchy baked and normals recomputed. One finite earthy scene-only floor is the only new mesh. Full original finite soles seat on the floor; separate whole envelopes leave a central strip and a broad front strip clear without changing or operating either machine. This is a low wide gathering-implement station beside a tall open chamber station, not the old narrow headgate and portable dairy cart arrangement. No crop, bale, animal or operator is added. No hay processing, compression, towing, usable workflow, ergonomics, clearance certification, loading, navigation, rig or animation claim.'
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
LOCK={'agriculture-fixed-high-wheel-curved-tine-hay-rake-01': {'bytes': 163316, 'sha256': '1df52f9a4b73e469bd345613968f47f656b93c949b124ac1cb65853a5bb5cfca'}, 'agriculture-fixed-long-lever-open-side-baling-press-01': {'bytes': 31968, 'sha256': '4ccaa92934fd6d09d51b0c7edf82313a29a93e88ac260275fdc6cc779317f55e'}}
ENCODED={'agriculture-fixed-high-wheel-curved-tine-hay-rake-01': 'c-rl~2b>f|7Wn@f5fD@qkst`mnm_?32V|!d6j7oQL?tck0*kPV8wer_0wxs1teCT&XE-?{JENEob2`Lu>Uo}LIQ7i={;zua^}gM$>aJn<`TP0*jPsfDOY>gUtJl?CHLqSbGv|yQ(gFa!S<(V7UjT6Qm{B7a7nj!5l-CvySX?}_yt2Hyw6?0cctG*6S=CjQRW(I3QKe|mobt-D^6H|a4jxrBKhi(kKN2tQTRgwKx~8J45`{zk1I0`F7S~M23W^5=9I7cEaN^?P%F?-btayz5cYTX1tIF)Zhy*4rnbh#d#l__dYpY9Zq#4tz=FY3CEU&DcQe8Di>W-=`FPc#|XHF4HRMyC5%Zo}E&M7adMI-BG&MK;1P*o(g=9Jf#7gfzGuPmyWS9MZ(S<!-7<>hl~q-}G{Yi8M|Irbbk3+o<SRask6Syxq8GqhsntmCBcVOTH9d)i~`7L`?$&aA2|ol`WU8mlatR$V$BEm~AjITP(FFIrGhR?ZEsE<FkVTxI{=oGKJ5t1ewoG_AaJZi9Kj#^xRFv~V0&CG8qpH5L`?$_L4&0{_>n4CP>D(9Fsi6$|lfRhQS)O2g(=SIsLbtt>-pt4ho8FDonXyw0eqsx7Ls$DwPTG^}q?CH_Te(SoY#lce@Z71K|usYUe$i^GjA9#U1kptQQ|*lcs7v9-f0%Z6a}e#Xjy=#H~FrPVX#5X9!t*vdNmb9THHRaeYK$JWj&DxF?ihpx9rB#!^u>T<hVrEZtzl-6QL7N8+TGtgVL4JJn#n=HrYD6D3PtvCjc*rWB>in)RRhm4Mz8Xe5dXnCq_Q{*_#p1h*kin-HpD7fRZsA|45GHUTm&MK;|TF_uvtg&Iku|j7MjJ2yd9BUbr9pq+rB4_kf);g`tsIHouZM@-HvaPD9#H*>asAfU=yjs`xX>;mOb0*%rDrHCJ$st@+RyS`>#q?6_Z_TW#>e`}NrPbJnqIu;ri>j)zJ9u9%nm(tL^(x-HS7T&5PS*y>R*uCBdaN`t@W<*~BA31e|5$xX=G3=8*og}Ua_L>@57xP0E}aYi!8#YprE`%#Sm(mIbT0Y_>s%z4&c*&<or~tux%eNfbFo}Hm-vHqE~f=b((I=~cC|XIZdy@QrQM_H?vFV8M<Huov4*f0phN4X1-5%*Nqu9vt#<8&cWrs~+zR=#t$a~=-y-}uQ(G~;2x};>uFS51alKnPXA%2R)@0h1>+Z2mC31Cp#3I9=wbSdW=i_g&nsQv_*VN6MCr@>CMNNf0o@Q0Z0nvOIF*};fkjIvn+UI((UF{gGbxgL>oP1I<t8@<j<RIhbl~!gAbk2%B+N+(G$ZC7g&O;MX2#2PWw|`ugS4;PmR^snq9Ih4I_9heHm~5+A(?^$9O6$#>SY3+0yXR!15ZPZ<<@htBtPE{0uPm#<tFCC8ye#F&l0UAh8=28$sv3ih;V-FLdpM1eRR*R6eh)h${&oa^4?Cj%c7%QpJ7WHJgnth^;{J9-eh)hm{&qxv4?B|ncEo-MJHi2fJL12G9YH@kg1^iCBOLO#<M+6Kgv0)J{2up@aKzt^-{bxfj{4j2d)z<5F@HOLkNZbB?r+EMa{oy9+hP9mhON-DKLPCJehn_2Dzj_3+6Cq1+2xbmKAD9rHQO!;H@UOQ5dT=W-t4-_Uc0-o)9JG+=9E>JR~8RAG0->IH`F)WH_|uSH`X`aH_<oQH;4y=eS@LC_;Vb8wBk=Y`~ieN6L6`H3us)!;_?w!VYmXq#Rty&IOXDOhZ7Cn<MH;2cQ(AK;Ps4`5{_aVKzQ!ZZQ<mkzRW51hSrpdGBmq%W_88%x;eFV)#d%{O@@B5qy6lT_RFp&`{A;%yx*+SMg8RFN54R@xNkB3Ttb(YRaBQxugz|8^*bI9XV>9V=2z6zmCl)BFTe-XR@asHEv~Arm|0OdrL45JZZ1m8gXm2;B=EOV#VJ@D4vT5>_f(A&R6m5`=?mB|4LK&VXR8Je))ZCEu;cD>bELuU>?V!<W1ym{8qKP<cju<a-zL?i(`&K)#S@E5%Sz|fR?IJ-SUjL;M(Lay{24JZJ6vii<U&|^ysCPNy(8E7FBeTmTc(tiS5{TjG_J3_5_@eQnpiye_`$=E7&Eb09<M2t3wOJkAf7!uQacOR=VkVh2>bJtx!7D*f5=f2jyOE4KEI-T!IU|ri?CCy)f4SzCoPfV(;1aG+TERo?60lTMe+w_vD{mnTPi(-I`;lzSykOMyrysjm(fXcDsgm1)Yal>#_o(L$CHI_oj0x8M*P)#tlVa-EU&SL*R)a``&DzQs)wMn<!0%Lf&QUH(*7?Pi$=qdWIWtA&_5gw$p3=jU@#mA1rt$uENCAKgu;mk9>HNR4Ru<f`cN#A6$?k>u~0mLH>hf|pg|}Wwwp{uW64M&5e+Yq7ocx94==4g34edjEH4`(cLa0nXE2!UXFME?$CH6%68jX4W{r&|V}VF45=qEoP6y~<RMXK=A}faVh5|{sl2ddv9?JSG5eo)Fp=8voqsNt2&&}@c*mtMg`WeagGZ9N9V##<SD9>Feo;5WP4<!=eSRf|*8Or)28VUzvp+qF4?x(U_&X9@6g3&}U5(=7iYt%ygJNuVtZaoSo8jY5a?2+nh2BHz?U?7OL#p5x}sSCuja*0qdm_TpD)aNdlJ$Jzf4&}J)<fQEE(l|Z9b2}b8iW6mpyqjf}N^5JYE2iP~YWH^Zs4+*4J!;fQ+s`9M9XsN%;l%@jc$288EUTC<WkL-%0~A^^Njf@*jdtVq!wv06c>7V_elW-OgXZnW8rqNZ_7gts>o>%Wn@%#<2YB0Z%fz#BudQw4=H=dn+kUuF`;l#KKL^jtAhp|mET{JMo6+X2$64!%My)4#>mhaPUYo|oHiX#47ixU<`CWc~o4e*VunRC0*`7A!;s`brLb2^=L?{Ov*nkKnwxbQ<9Bg2>gm7Rx+7QX%h8$!zgtns%(Hv}GgEG852W2b=8`zi(Z_hCq&%p*ZCd1ovOeS)$fsM(?_8gN*a~mRTOh$4alMOpq<}LDdNkqFa3VJt~!+kiyhFc_-OM|LyEAwXA2#YitVUeVdXZ71u#;r%$1Q=~J0Y?3Lt=wobZ<w9lXybKfqlIT!(XeuB$-HH@;EXm}aYp@?oa)Ua^Oo6#91G;#at>2#j9tF5Mwf3aybUeqFrmgGtmSB<mSfw{at_mIj9pl<MBXjuFnPw<d5#D2ZaIf3GtSO)ywQ1%Z_9bkVWNz)^Bj-nIktnjT+ea-12Ud>%Q;-n@dRr*nRm-MT+a!1+fD@Yyq<%(T+a#in>7*6b8H85xt<ejge9VRx17WEoM0m?5zo8j9IodC8)1oLp4W3Qm+LvnMp!bK)7bXja51-ljkIJ~A0LnwOzK-)IvxM6rm8wy>9o2TGs>&SSClWX18nY&)7VAx%H>K&rbSGz!o@JwZJ)!1s21!Wjy4W-%P?*%8$V6P;-P3H*0*1ve<B>U<$}pTJRC{HWN@%T?jH41)ev*y;^A;Oo`?m4vW8?RZp$U3;aEHp4q*+owq?cRj~JZYPUSra`uD&~J)}|(yXrxCH*xgG3_fi5VaGPBA?$5HEI=;Az6FBua4ZmxC9q@Ba3T?nOE(6hF+3hf#DcL{7;hpd7fvK2!B8+6i6jH)gLs7dF%XW&!b#Lg29rq?LWO87f|__5!hvKWj>|-ODxyJINeIP4$v`OK<H(4AKfKhVK8_3|{2UoGb)?b*xp`4@Dz<|g<N3KUk+&O@-Ufu-OB#I;advAWLF{rU8nj&yXnK_<V+nah1{1+xG7$_l3`J!P@?4;<y_FD%#PDF;?-CC9o9w9{^mbaz_Zkj{d@M*r+^aa)A6=8(%L^r<$w)HZ7jJD@uLUFFKr|S{->vAI5dN{zeqN({VaVPC!?A`#DiOdD+!v4H5SA*@a43dlBI@V3uz}g06-2x}7mxW4w_w!Rb&6i+>N$n;x5;s_d>!X=nTI0mDvLW?r=es5FRPHeHN_&0w+hh_c(uuckr;LhI~i_tnJKD>W_K#%LA=Yw@$M(xfPS>E)PTI<1>?SMNci`{Q$OiFeAtDn89kwZp9OsS#8aEylusma0!YX``B;-p*S@y5vRj_9Xe5*j2O6zG0+C48k5QaJaDtG-2P=+dS1qwvJQ@!L{MH<ypn=t%75FSW!ts!==fb&o&Ymdc1riS=aD>Hj_MBYVIa|x|cvyOG+dLP^*K<+hZmUjqZoO8GxNYflEZ<JYb2-=1M7&WB!#14jSlI4%JRVIXVz>_9wr(f#?RGMkZsR?>@o$OTyNzqaZ0<@37nAXDXq&nn4&>SGa4?r{2b~32JQxi{qj+_0L%&0fvv#&^l!rt4_S^i9hTRD{2}vP)#UF}pOTSf>Y)jAcy{UzxIrO~w$;$PnrWi8Y((8QhYT<Yey>5PK=GyD#_lIribiVhra59HZH@^+%+Ue$V!8UX{lJ6ZY63n5~&DR;ZcDnguXIna*@9iuSHjS;}vNV{@szbv<fk@PjXV|~F@uyNK6bnSc_V1#2-2UB=h{Ym_Xf)Y4xaRysh{$D1JSfLXG@ktxl?cR>c(L0~z;PsNjl|I%_&dVS36cDwYmsOU@x|sH$jJvPCvFE1#Palj-%T!&V3S%hn_-OhN6`fd`+^TP`F*VXvD+}EDXM4|(vi-#ubvn#YGo|V&j|^GPIy+}^FuKj_x+_94dfEn%0`-l@kAmRPU8HGgCp2H&X7oE;|wwMN;nXTH;!yItpm?RsL2quue<C|Zk$RJ@kG+clhI&)p{{5s-%wZ7Z<UqcYmKP%Tp}5WghD~Qu+U)%JJ1je2Af_*4Xa71<U}l@p-2=LSMi7)q>0+@#%U-Ji=$)xd=)XU)UyJgm~_NHx)t@g{38h-7mV5qE1YM8p-9XgG4Vh);1$FH6qSoLdm_q4f5Hh|&IDu0MtAY7d?bpuxo|9QFLR>VDLjNX$XFn1yFVJr4%}b_^}|8Gn^-jN-wRKDpQtp8mg)SM%*T&7-Xe)$Ac9kO4A(^Q><U2sD91m?BGE`V7!CUQF&>OZq<9pU7FbKzzIY?@X@)p9h^vi&Z@erP$j^_lV18c6u7UYQCATM%_D~2Uae14J_&LFO7=Rvcu>BaYH|B7{2;kBy?zh1a3+3sAaK3{n7TNxTDH06hY7@s%1RX2ah&hiYJQa}$&avT04A&t^bfupoqj@?qmbWA0+yCwsiew)j!iwaNmq;|{+Z#GEV6V}FxYP?JaS7+=$V8rwOy=hXv@$Bsdm<bTMsSYXmhmK?xsmd?ut<i2iEJe~4ybsZx2Je8Pd@}2ZT*LHzdZ%Azx{Ax3q)}to4u@Zyg$YByg$YBzCXny+kZUeIN2$NQ_izpJkR@6+<5JzzQg9SbW-~<|CLib&y`a=k%td*T=uAM(fO}>;>rAckO<`EgIpFpY8T|c=1BzebU|pl4+H%KV>k|So?a5+Je?5P?)L-zV#Dx;kn>t2k>^b@k>5=*x21;C3EN|(k;wD5m`LR3g&Y<dN*`>Gbw(o3+hQ`X-A6)hQ^WRHBP8>@F(yN%c{F$z%x=YF|3bmA{b+mK*}kJxQ9C}Iu$Kt&I4%$p!C0deXY(3jO&<5pdNJ6v2G1^pb4;Sa`Wp0kO0J!bJ8e;I`S9|}nYH%YX=S`m9vL-bhW$=|8S#>D{Fb3YJX4_tV+@qDM@;p@u|Q+>P&g22tRD7IkB6G7$6^ul)|;t^vpHFY>LHoo#nmIhyo{IIk9im$4MYNY7$1$t0_Mic3!$-k(hjd1w%$xV7O|5~O^036zQ+=gT#S#&#v17-V>$S)xjv5iST6R<eb&Ym#DY!zms<~lcq<9z(}hqdr{QOB$27k5lA%OC`f+<mnh*b`>d{;-KA9QXtb$xdaPtcA&K1q219IQ9@y#b3j^)#XFkVA}yn2w^WuT}anTX_7K_nCp<yV2+hs>*jL?k~aMuXw}oEVLS@^fM|9?Z{)_Ev6Q6=V<PQ9<+BD8~wLg_c(ZGH)rr3S?erUKPYc`8hFxEAjj)2nX_WBK}^=&xr{<lGk!HiN8GZt00sJhw`dG-W2nyK;BVuSW?@wP@@WB+1!b3uOMkpR(bp=2*?0i9;-`SSch}@U7@NVp3`Y)y28XC@y*sJUR?+``)PwUgmXHPiW(BJWDYeXo2@eK%trH0*ejwY6(o~6oCie(;oMfrv1TjnNH7w~s|%5EFuyKD61iMYiVC8UTz;l1Dv0HDV^%mZ77OM#4q`c7PKpZRIW3bEU5F>c`E?=D?B{xpT}b3Kw<sz|hI0AEpsFCJ$*Fk-p+HW*yHyqBHoG-DjUoKy9LVQ1hJx`>eqCrDbIP@XM1JES6prLK4)6y<p5q`J56Gi}XfVI~K`6HszoLRzPP413f@FU4LMR@|Z(fi&i}^V*w_iPq3X(YmVN?~w^IIQ;<>T`CRgjG2<-~B#zx<k3fH%cheibO<&~8NEiRSaWYFNHbV9BH<MTfR(0fUYj3C}-wXJ&E7{$lJ0<1$|S%7uNz3!BD!@^g>wCq|4v-jhd!_Yq@yPx9nfM-+=+ZZGv@DSz`pGdx+g`=?(kJXzX*;Ho*EEd6lPyt$sd@1-GEUdIQ{in;CT`1WrTuKhaR=dGmc2OUd!@~4hvyL4W3EbXWBt6{;$iI&+o(J~t+T4v)!%WRxznT-=IvvHzjHcqt6#)+2MIMFg2Ct7CXM9XZPXqk-@Ewgc=Wj;<+4ESH&(?_Om>$q4roX+x6`|s$#hT{N32ke^p_|37+WEzeG;QurD=Vmeu#{saujBLB9Ov7=P)0%oRUNVk7na1+Ueq|cVH<L+`OoO~$M)prtPs4HB9-*?Q;kex|q3V}&Jmn?h)FT?pEA0`D<(2&sjpg++Z2Sm=@goezk1!ZN!eIOegYhE_#*Z)<Kf+-A2!rt>491Tz7(c>b{0M{bBMiomFc?3sOba*|`r@Y#?2n&)pa?&E!(RC53?1>aJM4;|cF+btJEC+8l$DZ2woFI+Z`;_%_qUJiiZlg65XDad4#7_f4#Uska3p??h7tG~4P)>#9*)P)M3kO_vQqLeTV{m)x5wMZ53!GoL9$>62xA$BAhd*55W_MC5oirNK@!U(#Gx(h3<I$o2m@dj*bNTF@=z#&_OJ&G#&R$S=m4Ey2$n-&5bOzE;V3MRf+L^{bc1174uhf49eTh>EJwm{=n1{x7%Y#0QBVx~!8k0(!LhI}^o9voPJpp+02~A-VtFDQ2M0obn2hCQI05>he*;(sU=mDyd4;`RI`8^X866*R+KS9STOBBlerdFpznr@~bKS}VM5k3_wEWjLXV~2O>G4|r_urP<b-r`t@miiRVySK0D_u^|^4jZ`W;zsyM8{7iXnE5;%QE9{jEJEJkJoa`PRngR?(1W<{L+yt>^hfKkJj?7R~=Vh(zdgBZE4RE9bXh3QGd%X9mKB}@2urN^*^Y7+Tz{BNiRJ%P{*@({dI%nTW*SIxn$iv8)Th#FT8Ppj>pAUZ;-Yvo%h?rIzDa38#lbxxtr*-^58>sJYtWJHgvsWZ!!Dg69(#d?_g2A<Pn=*)AD_@ht$hD&po+AiH^VjY_H7DZ(N<a@54jHS)qM0Ti>`ko!l4^Bac5UGi~JgCF|bYKXduuH`5PaJu-9F{x7F=GB>_7uKwNWr)REyBvH@hxlFsS?@GOZ$6q}2yEK>A$)IflZA+tV87{+*qdfxcNufQNCN`(g27xxDbuwr}3ECjgh7vBXlR?|kXq!OWn)b^*&i%<{kOgu*vheV^E92pFS4QV^?n9ltho8BfIzMweb$;gU>in#f;m4c!TzQ=PvxU#Bx0iif&UGE_`7VibL@)fvd7wAWi3j5+JL|>q?~?d8^7z5{=ic~D;>^_&XIIOfVRyj!YJV*E$GM~x&R2b~?1OX5PB?!Zh~<Gem+XS`RX;5I;oPzt&R;<+gE+Uy`745D1ZR~!alVRS8N*qzE6!g7upEH1Zg-q_dSclV=TE#>3wGaDGT!qAyZ<X0=MKT<5hddsB-nhUWSq+co7a?#bE07LqmuESFWCKG$vAfiHjgM7=ODr6BPHWpCfK~DWV}}oWcO_)<2`>MyZ<X0=Z=AF9#JyRK_zTHQZmkEC2U?(GR}!5Y<^TS-t$Y?{a?vAca*SsM9DY@4P^6?l5s8@$mTUAJJ&MZ&ok^klWB4f;rCd&U%B$meS_u^r978$?msj)i6-*}-ET#c`z@b$=)SF#aqg>hUlMFCP|EP*&i$F+1DhRp?(_Wq$>(Ug54%3}@NK5ay|kHcxeWIqm)FTO@pGohe4+Alrpdgc@-w$t=Vzr%6W?Z<%!w-BW}3{!&3wyc0Povf@YAW$ywe&#JJ`R^x;XPrYb;yipAW(LV;}tNk26M}M)OYg*VaDvaXIhwv42%rIDZvmS&Z{lOPsm(!*V~Iom$~Ma{!hH;0)H*o_E^fx3~SfsXvzeao%Zf&pYk$+Ye`)J#m)lfZqVlkzH}l>1_Z0+6(8IB$o2`*WNfU_QbL$&O*1WJG@@n-|sJTg&&XKwZxO#ZrP{AkJoIhEBW%)@t)jgVtY|{(JWuS=8FYhT*B=4WXCowGyAp7?AJ20-;>FH6-&E5d~t34y~m&K#0DtF)Hv3p{yV+QWvv&B>z^OmEI#(p=ewk4pS8qTrXgn0w5^6%MuYv0Wi<T~2K^ES{SpTK5(fPe2K{o6W!I%0@haTQUZ+al3$ML)NW0@*pd<3`_Pu0p`;H;kpPjJmgxB;Ac-?owvI}0*t?|0=j%9bersevx2bMkXo+Q_wy|C<sSMzSzUI#2Y;9X>R{PxU^qe?{C0qKkvcMF^-*7twJlV2RWKwNObUp={M?Ac=EKkxM9)m<+Vfu1*b@{4QMiQaXWc=9*XuNN;&JIj-Ans}4g_rrO<{95I)o-FG;adpI#rERxWbn#@_$KXM~rM+1C>i$lzdb0HSy(Ra0vOIS^|8s>W%P}ye?P^aRv$cmWzxe~Wb?SKJZO^30HXR=fm!+tWI<DAqT#9_9<H`GVOp(uZT-)Z^5;}J}u356KgvNju(^%56tdqv1j-_ohwskD~NY{vtrLX8()3Nk9U9&ot=Z>y@9m_F5_YfW5mlWcVcc1p;`EN}XU!M7dCvQ1?sTlNqy(b@c=4w$tZ@nk~a`Tm<%Q3fk^0K}+iObqw>B)f&cZkJ_b3J)+$Gb%2#cE%EV#R1rmUUVm^!H?G+cS~&o-F&gcKU~DFP6Ug<)7<4S^E6r&8t0Gp1a9iDm+<^ftKS(dh*~ey8AM$`z}Rw>UeGHffU)M<DMs<nxa1H_?wz;De{$$uRQ&l67so@U+(a?fpqS4EY}V+2E3TYl8$AaG$wT{ZKJWRW7$W#MszHFMc0~+rO)Y_)v-KxbnWX{jsd!dsQ8)r*SPB(FQ#>l7t=b&i)o$X#k9`xVp`{TF|BjFnASOdEax&Wrge@N(>lkCX`SQ6w9fHjTIYB%t#iDX);V5G>l`npb&eO)I>(D?o#Vx{&hcVe=Xf!#bG(?=IetuINyoI#@nTx%crmSWyqMNGUQFv8FQ#>l7t=b&i)o$X#k9`xVp`{TF|BjFnASO7OzRvkrge@N(>lkG<y_{)w9fHjTIYB%t#iDX);V5G>l`npb&eO)I>(D?o#Vx{&hcVe=Xf!#bG(?=IbKZb951GIju+E9$B$_&>6q3zUQFv8FQ#>l7t=b&i)o$X#k9`xV!qB%antyeNxtGQUp$`fzkE(JnTF$LIgQ`6jAroLOs3(uS>7YInZdT3<>NIRH_MIG#XlSJ+4M3_TWQlA%LaL6-#v3Ic^+MZyz*T5<zc$Hb`A3S*sm^Evx!W~FP~GM6IELc$IWs+<rq=*z2Uf7UZ@<is&mnB+&6bL?G@AJ`GGnar>&G%ekso(Y>-#>-7^Q3=NUH0E6;^-o@#@<a%_mk@`dqJ7(d&6{1oP|!u*xb{AHYP&&H217(c>b{0M{bBMiomFc?3=VEhP!@goezk1!ZN!eIOegYhE_#*Z)<Kf+-A2!r`c7|dV7VEz&Y^OrD~zl6d3B@E^-VK9FQgZWDs%wNJ_{t^cBmoS*Wgu(nJ4CXIkFn<-sPhtFQ@9|TZzY6nL&hu9b*b&OHEQe{Z5sIz-tc|dr^(0vE7(9;U<FEsi!gScjD#dRvYe#4UvruOiYCMUOy-~KewFz3n6Yvz4PeCgvgBh^DRfgYvtv1jOPC}iNP-7EH9)z+7S<gaicp9F;@)_6(W<mw@v1a1;0IMDB3YDl+i5kzMWPg<HZ@mC*VKY33<#Vtz%!WD8*P4yr1Fc<QcQ_e!PDYIvP%?<JLF;AM1)hf&v3wEQ!(6C>gRQyv?Pu){9ibL=YEk25l#HNk#Ci>OgO}hHEMI{RFb}FBWX;2Gz>*nR3s7ePYP^P$ag>c)TVM}(6<){kb=VVXpbnx|4SvIx%-=c%bxuKzEhsqvWd~SqLMQkeY{habbcOk_2$I%({KhPq<Fy2JmY~L)C|QECCDuF81>S(Sv3wi4!$LR}23ia8o3Lc|*HYA3iW={r<e?~gsP!IngSX&aEZ>EmuozAUVJ*h*A(qS)TaG%*QR6+79E`Gqtq-6F{2l&*<v*YpPJ=UGkaZe<Q<ls`Jri}#M2!znatO)}vHk_U;C=WI%MW2cSOzQM2x}RB53^+6>N%)$4r=@hC67YcqpXi%U-&2d8_Rz~Z&(3m!%%Aleh;@~j_Y}-a~^7ZjFQ7qcDVH!8~`7|r&xXp2f<me3Wix{;rB>OX2h;Roi(WO8A^^q*-_RPa3FjFpJVws^oMg{HH@^*#qZIU%$~gvbuL7WFHrJWls(q^3i`o+;7csOgaDim7r<!ieEg2EWUlQcsB;Nwe1($ZP<EX4Ed=4e@HLiSLm1Y=MKH!%i{E1`nU{Mx>RgT*-=gFMl$~Jx01@~GzQgi6h{45hDU7!+#_w25X7R2=opq@314^EVvL{+ULma+`AF=!ql5iPZ0moaH;rBR8K3{na>Rf{wKcnPil$~t-1_R(H_yx;fU?5xxSHVQ<O8lN+$)_=|N1f|Y<2RHnMcGozvP$4r_#c$uSHRV9Eljbl#_uFcKDl`l>fD4H7D|_)Y?;;4IuyWafn^J85L^d0z%=VR{7$vxbDp=N&aJ4?5+!G%>`be*H5hiVcEoZ=>j=0JZiaH}M*L2<<TIgnpw1nr(HbRZqwH*}tu+K%Svz65lXVo_0=GkjbqjuHSn>(dKcmi{QKKzN&PCa|)-KjiXk+b+<<8b{xDD=vIo56Xon^_VP47XSdr)H+l$?jM^Q_&hVbIQMk7avn6#NP9hAQh%_&v#z&!*moI`^T*ZYWuUvNhHo)=1dZ>VRbj>sYu8{sPt3UHGlE<a4a|qt5-Pu?I@dN7?ySC+is4-P#k&J*{zYFZ>nitb6f$vL&B-eF$|PLXA!+xd>$!SzWEM(9!CGWfyA#tcM3-p|u{rwU&HBb_42cK#i^_c`C}DYIV1cgU(hrEW24J!UOOKEVdrN?*dCcPn$uV3~F>o$<tBxbgQRz0_<h=z_N!m86Ji-oMt_Y-&3q9crTxZI@3_2CrTEhY%$)`C&Av<qgXzQ_xyU83Pn~uewSF!%)dskJO?eaJO?eaJO?eaJO?eaJO?eaJO?eaJO?eaJO@v9_Oi9i@*K3x@*K3x@*K3x@*K3x@*K3x@*K3x@*K3x@*K3x@*K3x@*K3x@*K3x@*K3x@*K3x@*K3x@*F&w#*&U%o`aTIo`aTIo`aTIo`aTIo`aTIo`aTIo`aTIo`aTIo`aTIo`aTIo`aTIo`aTIo`aTIo`aTIo`WYld)ZoMc@A1;c@A1;c@A1;c@A1;c@A1;c@A1;c@A1;c@A1;c@A1;c@A1;c@A1;c@A1;c@A1;c@A1;c@CaTV@by>&q2#9&q2#9&q2#9&q2#9&q2#9&q2#9=RwKC<F^a;oQsy(b1qtD&$(!sJ?Elj_MD5B*>f&hX3x23nLX#?$<DJ3T4v9=Xqi3dqGk4+i<a4QE?Q>KxoDX^=b~lyoQsy(b1qtD&$(!sJ?Elj_MD5B*>f&hX3x23nLX#CW%itlC(~HcF?-HM%j`K9Ewkrbw9KA!(K36^Ma%3t7cH~rT(r!dbI~$;&PB`YITtOn=UlYRo^#PMd(K76>^T=Lv*%nq*?E>h%j`K9Ewkrbw9KA!(K36^Ma%3t7cH~rT(r!dbI~$;&PB`YITtOn=UlYRo^#PMd(K76>^T=Lv*%p2%${@cWEx94X3x23nLX#CW%itlmf3SIT4v9=Xqi3dqGi6$QE?%ErjS2V$p0+l?-lYt3*)Dd|5=#73i+Rf{Fy@jOd<cXkiS>R|16B3LjGrA{`&v-{MBdTn);4+wHCA1{#AHzi2>X42LzX9Jh;Sw>u1c^->p-_B?fHE^Ewq=;>XS3-{<*`#BF&ep~?Fgg-2V$z#d^>k1(*OSv{8h#z70eE$w%WcEVD=lMrABXpd!k*cn>cZyRle-<_ZZ><S(2w;Reg9=3zdSaycp;jJG}%WSzZAU^u}_>7K^n7-8JPGcu)dE%NgY<{w6s+MaXS>ej-_}S}My6x(i<R7|moR+EGwp+$%ne3PHI+lJ|`RVTBnfaAQEOjOS@Iti_OM4{WvaZ&MWgkh`gr(oeHWMb@D|^f~VzTYCV`dpK^<C<kaM>ZJXP$rVxzuhGDvWsEDNAks_p-T0ENzoqc1V>G54~xHt82oomaTMcGhxzA_AfVLvTZ}{bR(v|OI;KG{M6GkYc|%U7NkcR@l|V=+Wh@PV~kkZCV9}*aYo$z{1vXQ2@jgO(zVTmUEPhtjF@b@v-{CT?DidXO<2wWYc_sc^2_bLjQHzJmR}gUpAlzm`?h5Lru~ih$;m5RT@!w=$4b{W6DHjQ+x0MFvhDCy-Hn*~E_F@#$)cs1&yGoy{4nP6v<dgzlI8zIHXE_DP4f6%pEu$wj$GmDn(#Nju5fKLVba~9W`hxvZC76LkP%bgrLGB&oVGO6?cjF??(<gCi0ALP%;sYc9Ad=MHp!O`9%jUYx~_0_O?dW(6|QY2OuFB!>Sx4c+db92jhOl_bxpX#^6VP)gtABKb$mnjWj6n|<`peV8zg_%`)w_EYO%tV*YPduR=DlznB?zI+@xh{H+}7uS|<CYypH+0e01M(adz>N)W5dYryWisH;SLU`0_2OUWc_3e<?jG!{v1{$Z6sxGHF&%MpX|#?y$-pSx*M*5gsxrlHu|?8QyoDPe#P%h^l!b>p!{s@$~0o=7_6<#U*Dw{dkJ^{mDBvrtTL1uK)6v*^PX~b#?OGKX^RtcbxkQ>(5aAIv;Wwv_He_cm31lla1-2V_qqlIOwECzHK6(V)7}H*VUtw=f36sJo}+?QFTR4x?)5+z2%r0V$P$pQk!2+YyH1@(Cw)gzlY5Dk;5DLlh?y_b@F&T&5o!2jt_pYJhRiaHR)%LNjLI8KaTcinEgusPu%m4^haHPOD!KaqLJUYZWH+wlXv~8t4Al#earoMS!S4c>o+UY@`c;dM=u^J#^3v6YW^;N(w>*MubZA)KXr7bN7+sp?pt0D*VW16@iaT0_B)RCXQ+PebABA{&yfAP^YY&oGt;A=9VzN&w`=4>uG>UD#pGSz>gv(SbKi1*u5P!xI68WCX84$S>BQy^V%@_-#c!b+?RlvX|1EjyqMFQx)oUC1me<2|b@F(;o*hs79mo1JtbW(${5aa5VfHJ}i}lf0^=D465vSjDVWV@wb(_eSFnQOvx_Wf-+_&7HZJ!*Iny_q9rgHS%^_Sf}DHVEmp*Za?50vQ6%Pz-uDw+K9X_@7>{<WU_me<2|b@F(;o*l3EJC60IS^cih`Ej&A&Foj6m&6ra>o-4fnz-V)hf25)xo#8r5+?8ZR#%Tsp8J;jQ|JHbE8B|)P8pW@-=?|gGbVQwt0o>PB3tVk`G1FNz9`whz9!S=rVASRpX=)6xu5ZPz29-}XRJR%_3Ql4WzhZ%+0Xs<@>$>1Uy`g5Z>+wkk^h^>moWJflGoLvljpwW{^W67ozJ-p_aT?p$#5Swk*R0(WK{L&e8^>Z-#uhpKX7@S4Db7%cEoxI``^)$|87ou{K%;Fo_I_iX^-><{0Bb4&qwf2{Jal;$In}M^bI^FkNh2}3-o{;vD^_X=nh5pzr@oTT0*h??{XF6w+-xX|GQlK<F_63f&Q>Nmh#{B=?fv~h-F9E4FV8>PFTuVdJMWk3oKheXBYs&{`a_g!d_4Uhe0nad%@l?7><Dbu-p&!vHxA>1F@9<?&L5S1qWk!FdSt6OUz*`!_W_ofpHMUG73RB4i15CSayRroB&fGg=Gp7FbPWGP%ICHfiNA);czSuhe0qCX2Vb{hr$pz394WumLuUPm<u&<ESAT@a5x$2U@VqnVKgj&6CsIZ62`+Ra5_xJaxzSSC9n*pVmTEi!g5#%WmuNMG&l>+g;`k6f*G(1)<7kel~4ia!$nYyWi`x!wQvd4Vp$9G;4)YY$76Xs%!e!CS~v~M(_kT74cEg`ESJKm_B#qzV7UU$fLq}XI2+5e;Y|Bo0jsfG4d=k0;Xb$!%M0N=`x*a>vAh^AfCpe5EW&aTTnZ0D8m__e8n_%bz@u;-me;{muo0eso3OkIZh)s?6WoU7ZEy=b124c`Sl$J<!*lQo`~}Ouz@6|CyawyBTo3oa-{2v*0?RAle%K1{KnBYUJPdEcyYLv6k3l`W2mgR4v3wF9hY#RG*o@_7cpCl%AH$1Sz6j64zu_}@70XxQdH57Qhu5)u9bSen;7xc0%ST`fEPwQ9cmG1i!Sjc^`ye`=`r&AIKSjrDO2)bJIxcB@oZGIBNnY-Q=$P7-`zbmm`=z{&r5|Vy!i1$R?Qxi}w1@UkOj!1jbWK?LjchYv(v^E0CQP=;JronBzDr#b-nqpvcMrmZ&v|6HyT@U|(l**dG2uk}ajvcjuirG@watV{SMG6`Fxe*eP)wNmE_F@#(!s;rJqQzi@8jX_9)}4_+h`BPgx`B_Y(qT;e9&3rUE569)!jJEh{-m&hhoBR-(@`peA`pQ+&u^rUNdBbyT@U|S=+LEC?*_QG1k>J;jS&mySAAy>B>D06DHf_9*PN5-=(ez2ipvH_aIF8U$rCLJq{C=w$UDn3BNUNtgCCnYc`H^Z8Krgm3tf}Ot#5A6ceVtOI;H_eARGw55j~metCqu$6><KHrhim;l4kPadl02i5TbFX2PT^_c%<LY?FH^CQN;ox+eVmbHm;J3mt#<zY*>}h>oQVw4b8m*Ef%G<#qhcuVdYIbxiVdA4JF0uG~-2G1)KWbzInIDeSWp_F3}ZXTkb2tbW(G{CHuX<@ecV;Xc>J^L6K?u+LK1XDRHn6!uvP`z(ch7L$FJXRlu=ST4PiYadx5SWdo@C$2d|u-twnA2EHYV9y9B`K=#M6YN<7C6m09ldoiI*U9ZyGTHAuBcNpI2bK@-%Tkx++xxP#hvoD8vg{*!Uci^7-`MjAzD&AKzP&G#ZB9PFFH_&0=LLMZ)v}d><-_~((3@5WmT&LN(l(aQ@5}Q}St{7`0=`^!$mxPTkKoIs>*U+}GTG+j^ZPRO-FaTXmj_K<DOf(dFLytGg<$#izASBH`TV|o)!L<kJul$PpPzcVV9z7?va6fTxA$eT&B^EYWw-Cy=LLNE!5-4LZa%y(KRJ1YVEOjGoVCr(=lA8WGfM?~Uci@Se1biX;LD`z<lFl)+2-W)`!e<2d0xPmzxj2AVEORAe8rJjcJl3gS=z?(`F*+PmZgF{FW}2h7A+O*c?4f3T_@k(m&rCKpWm0M@6PiAzC3%w3c>Q>eR)vVEIax3zASBH`TV{-f5&BlJul$PBd0AD?0E!VCS51r-j~TXC!gP!sqfD70=|69x)p-u(kr=Bi!3`i`AU{Hu-twn-_U)TV9y9Bxx@0Mf<0@XWRiDs@|8^OI=THyCi|Ud1e9EeKNsT9|1Za%2R~RYSU&bP$DesUh4^#+@n_w6F^NBO-9r4i5PvSjp9}HlLj1W9fBqxJpAR~#lbctp<E>-5xcSLCZgXdMH_ute@s_<@c^!ZFQnA~vj!9m|hjmQt$~d!*$$lxXW9bKq&6=>(rP!|tOM57`Y{IgSq-(;`Z)BSZldg>YnlRZWW6LH?eV4i>yna(BmM84b!85wJxyL3fZKK$-3BUJxk*jOM6W0{GwwW;L%Gj?7lWj7#Y{JxcscXU|Z9BWU!6tn6Jzd<~V-uFPQEb_S&%U*&p&kQ%bwsgin+dzR8;2P&*(PJlChYcI)?>h<&+qK!2Agnvm#%K^u?c5w%f^;X_|2n>TwN1>Y;!NyHWMaY8T&P1vQ5U8O_=&FbxnBd3!UBEU=v<_NLM%a*o38R6k9go<=u;1T@#L<)62EZgh^M%eodHcld)wJroKyE6aMU&E^cnH2@kxytDAdl!qPU1Et~LbnVzn$3Gdgcmus5|ldg>YnlRZWW6LH?eV4i>Tz63yH?LU77eCe2%}>^`w1MKxI$pB2rz@}HtDY!w+to42%lNR4sa+Xo)-l;H<#k+$KNsT9h4^zJ{#=MZ7vj%__;VrtT!=px;?ITnvw8gamUU00DXy#I9ip4k6d%^{)DK@uH@tI0&FM?Fy7D^4-#u=-IwpA;AJ#Fon|<eon#q1CuVd*4ip`p^)TP+32}^q#-m~G)vX7)|!qRVKn+cPyjQyH0*_M6JhCfr^rLGA-*yG7G#b!<T-nE<36#F${X<Ng4HvGALa;vLr!foz++qKPvNms^xO_*%UzGuUqsqa$PgrB|s$uz}gO?c|(o6_#PHB1<7Yk1FwKbOA!hO2AB-}QdmwatWG-HpSHm~6|wXTyN0?^4%*zr6LSG{t63xc=5>(iHnO;jC@+o(+F)xz8J}t_i<f{FZB*36rjj{hBb@mVM8LKU3eOt_im|=;<`YW=;5{mYdTQ`!!){Tf=)c{CV6{TU=cePG9?`Ynus^u8jSfFxi%U&xSu!-=(ez9}wJ>rr4|rKU2RsO|f4SmbNv#XTzU=*m;YqYr<DvvDLNBgh^M%eodHc%f4sBpQ-Os*MyVnH>D}AtK$WGJ)5TZu#Tk-4e#7g^HKNw&6U^jS)I1J?dq81Wqer2)Nb~j8)_!|rM!*{@#jMPx$yptLj1Y#{*6NXxe$LY#GecC=R*9s5Pvq0KjZH_H?FJWn^y=oKCI)ZAC6`*XEk>lGOZ!btl`%eR=DlznB--ASjW_^^Uh}_ll@X&$I=fJn>AsnOR--QmiDmsJo~cjqZ?Z`VCgrq&4fu;#(qthY;)f8?90@5scXW!O-Q=2SrcxNI@FE*ny|Euz317N)901Cx+Z*2^(@ym6DD05`!!**&3VtWFH_&8t_epc4{&3%COqZ)L*3Y~2}|49d!Bu{^wp^iab^QvHD{)4n+dzRGR|zkWSjGzXJ2;vj=Cm%`s{&jY}SPLnmx#k{hDyrHupWxzI^M{DXy*w51Lx;+GfI}D`USVOtv}idG=-MyVNz|o930cu~`#du+LyO_G`k@Huj!pUq1TQ$*!&m?|nj<Ynus^u8jSfFxlq3=h>I3?^4%<KR;Etu~`!iUV6A2`!!){8+*^QFRzJAa&=Ak)e+NN+f0~rW$f34$u{Rb&%R83m%1k0VfmryhId@3dG)9x-1xALr48(z&q@w0p6JT!_^u;M-F9_M@-jZGV`|rV=d+T@ekrfxLj1W9e=fwI3-RYd{J9W+F2tV;@#jMPxe$LY#GiA@e;&wko|XLOj;jVzd|1b_4T>}C809xGT_t0?8<-7BCV3ej*0Jn3#hG<X_B*;tmVRJ)&b};lDfVl^(mxbiHeuOER*x@BzcD*~nRI3B*My}%DYk6F)OV*IUp{^IhJh5DHQ_G@tQ<(OUlW$TrP#6wqwWS)k1wNb8<?HGOu91mYr@jE6k9f7>bp~qFHcCWA4suT6K?<BX#*+tYr@jE6k9f7)ZM`9@ny7a1GCeYUEPhtj9B`XV#_A%_B~sVFSp%t<3Nhdn(#^MXAY#;uL);;n~g1-FzRk#_4qQ{wt?B{%cLt~zb2gZZ8o-S!qj)C9$)_8=5+%pHfzFH^q4r%eb2K2OW#s#*@RJd1FOfE(Y6iDPG2Tn`#sDCEPYF{WfP{pJN5YTrGr-uq}Z$pfAiJh11a`v!qT@CTQ*_T-N5ScWwdPrv(uMJSH^x#So)S?%O*^Hck1!wst(HsQe0QZy(T3GQhZp);QS}!%sNK-4NO<b*zN{qgOW*J#)ow*eL`_&9h3czu96G!=R*9s5PvSjp9}HlLj1W9e=fwI3-RYd{J9W+Hjh8QzOW+2a*UPSZOF6~%T-qL)DK6eSkAMOZ(bo%EO%PT_`5U3a<G+5@=mU@lBr!M=UK^Qzmq$yWa$T%C+y2om*pY*vb2ZgIs3BgBg>=qW$8DTr|rw6>*OK(GTG+jIr}p8-N~c&<$J1UrC6S@FQ?BdO|d*=UzWD9JZE2SkvcTR@~C}zw+YD<%hUE{(slBXeVJ@?@|=B{`tIaW`|_$eGgB;2*q2LRotk2K$i6IXV|mWLJmvdCQ!J0#m!p#hq*$J|FT1+gJY-)c+nhXSUv~SR&7=0^K~u|9EKk^%Z=E_N#qyASIcuAn=j_XS%^s9udDOmq`s{%zmZ$B@r0e7%`!d<)<T?8?_1(#%_T{}#C`++CVP8J_*2yWBhwRJJHkRk?%M11yoML&@zI@ZXk`&9+_GQv_@{oO*Y;*FQeVO|1<Wc+bt0ShRSe~#iuZc`bu{>m7mbS4xXI~CpdU%TEQTy`er-~HI)AnW3b@GsXnQU|NoPC-4?&MMX@?A%krdW=#l0%CprdY1BlBEqS=UK_CM;(!3xzkGSu>8;z%fVJM$ve5qN~U(5oM$DI{Z8(*k_++YLj1W9e=fwI3-RYd{J9W+F2tV;@#jMPxe$Lgk3Zw@j1+svvXax6Y)!FuH7j}QhcB_1vzm8^Zc4FtM=SZ3bx)*N&a;w9-g#HElBr$iozF@p`<-`3D_Q!1y(ih1r7n99voA|~*n6IRS@w~=N7|RA-&mfrFO#nG9%f%A+no12`!e<2d5^R&x4HA}6njsyFSk!_O|kbd`?9o+z317N?_Iko#oi<B%MbQ=GR59g?aQR=yocGB$u{Rb&%R83citoI%ir~WJH_6U?8~KZzma0^VfJNd8+*^QKYzX{#oi<B%g<i_WQx6~+LvA3?0cB~*|E)e&$BPPeb2r}+LvE0ek;Y^lkCea_jx15-oxz6S=-$AJo|F}t<R*`d!&8&%UhpHvG-K_GU+<+VfJOR&3VtWFH_&0_elG4`r0>B>^;f8JnpG2DfS*_UzWD9_dNUZNi8?0*n6aXxy3<Gr`UU{eVKHf_b~f1+2*|G*_WyB&U>VN`N}J{rr3Lueffu-x1`v6n0;B=#@_Sn%g@wrPO<k$`|<(7O)2)CYF{Q@=RM56Otv}idG=-MyYn7tUp}kT))afkvXYOw=Wi+Yu4W}m8`wLamAqiDXH)Fm(MnFP-;`qSpjI-;JMU^%GPUcx^I6Gczw_>BB^Tn)h4^zJ{#=MZ7vj%__;VrtT!=px;?ITnb0Pk09)JGurD8#GT^+|;_7W5y)^VFVy9<gl>v-#!F0Q<e4?3%p+pdmDUdD%YOzp}zvyRDrDX(Mc2a3&_u+*j4uL(<gD7I|EvX7)|!qRVKn+cPyjQyH0*(PJlCQN;ox+XkvO|hWZtO>vOdXb>muL(=rD7I|E!85wJx+c7SQzzFp6DD05`!!**O~#f@nEEbtP59Lj#e!n9CVcj-MS^0#CM<2E*s=+qeNUH$dJMRvZD-du6Lxhs4l`o1O~#f@*zLQl$ABN(+)Gew)`Z_Yx=2v$*MzgSWn;@G9N(p@t82oe&+qKoX2PT^W4|U$w#nGC2~*#tt_jD_=_M#OYr@OB7YT~}ny|EuV#_AH`jD=!t_g2_p|fk736rjj{hBb@CS%JcOnsNSCcIy(UV>t?Cj45ar=Zxc2}|23wrs)!FYoH=n($}Gba8DnVbYbcUlS(VWNg`lsqa$Pgs*y{NKjl?$4l1s6ciuUv9y8W%sRgKsjjZPj_WS!;<l?}l9%ye9aFn9&a7jyU&`ya5PvSjp9}Hl{NvAqA1u%8bZt%gnPVEqpZW1Z{Q38ZKXae!;+(qkQiwkn;?ITnb0Pj*h(8zN&nEHblD5aWaa|p+DH-R+hjl#l!_k7hb3@6&^M||gI$r+h(QdmsCV3ej)-ko~ymLdzWWSWxvGfDQW=&Y?Qta1+r9JFD8@??2NV+C0{YJK#FzL$JuL+ZF&U-d|nffkuO?dsL@hnd3&x!Wq+}N)POWW9cHhlS<M~1t)CcJZtVXkc^Ou91mYr<rk^PUY~roKyE6F%sy@osF^gx`B_tQ-3^VQCwC&xS9*_wn$CdJOo|!NXkJOxV@kILwI2Hs?JXzU=m0)?>h3TaI^QvnCu`G1iU!nsC-O_dOfFyk^J<SJ#AZduo_#n+cPyjQyH0+2*`w!<VV=QrCpnY#istW=;65abw-suL(=r*n2j7`CqjoTwN0mwi)i)X2PT^W4|U$wmI+F@MY?|)HUHHVw@YBHQ~NLj&WnZCM<1Z@7eI>i(ek$>YDK3tA@L_nK0?f*slqbZO(f(e3|+#bxru2U&p#}T^+x^d5jw$*0HpKy>mm!pZ#xyE3f0{pBwJBt7DRv@nIcPyUsf|luY(Zc^wzx&xQDNA^u#*e=g)d7vj%__;VrtT!=px;?ITnvw8fv&&0bki#zrg>o*O_cyX_1_Yuoq8|uk-b?7DzzHOu@w-9@Z8>SxT$>H!G;+NY?Jz2_+|N10PmhC?Cr&>>z_Sc<$iYH4y9KPyQPkwz;!j;$Y&`yWB?dtfOkB7MS>-h0+hq`{yv6Lr&>R7f*=S9cTemcJ@{_L2`-Erc@G)}yj#)%ixIPqc{CtghB#EWU1crlF=FQ#$g#WYU5n8t}0(>U>B8Yf;%<HU<;oOm%GCn}crrn;w(Ox@OTv2Zw@<)s;5|1}&37&>6r%*StzZ6?!j9032H!9O>XX*dpm^<`w+O=TL6yPVe4lkt*q?8!8iSN1E@SiYG|iewt(^)j-5s(KoZ+x7^RJq^e0ehF2-oZ~4k8K)l6SYBz5Xe_VnmuM`nmto^a7>plbFn)x=_z?!<M;MGBVK9D#!T1pd<3|{bA7L<lgu(a`2IEH<j2~ezeuTmJab@scB-lKqWj0S~naxvLX7iMm**v9XHcx4p%~M)t^OTm^Jf&qePidLWQ(9*8l$O~%rDZlxX_?JaT4r;Wl5s60*g9FuY@MuSwocYETPJIot&_FP*2!9C>trpnb+VS(I$6tXovdZHPS!G8Cu^ClleNs&$y#RXWG(Y?qT<5(r?CDhtbYpYpZ|O7pF~NYiS5OU-#;RB+_i1U<^xZ8Sj*AtdfI$er-!tB>bMp*@AKgUTK?>q2M0=i{-^u3T=z=K=F?{CS@un`i0T>TH!xi#W4jxe4N6A)>seovjDDzRK2b9Iv!3}@$#`Ds**Q`&$=BA^Ynj^Zyfv+5vVU>gN3~3Tc<CEGlRt~jeoV_UP$_xx!+NIk>*y+(#))Htl4-m-eNi%vTgN9#rt$CiR>{xIPrKKVjwk>4fXy90cu>p7e|3}1U0dF-<v;!TOq;(s?>;R*Ge2eX?YG^l<rn)uY5OX<@E$GGbu?`^J)`^vrmJLZx1QOcWVFAY^+n0(hkE7{C8Iy<nQxVh=cS&VBPEmkxjSdHOzp1x^f4`y{dY`zLd)cbZ-zXjW%6hFf~U1i*U=&G>Y2{3qpM^ZCyotDrt#+VMaeX79iJ$f#=qlRCChp0yWZX1IZMUzdX!9amWt(dEt%#l70dgBWSX;7EblXtY0gryykAMCIZMUaoUHEdoTXxU|75yKmiJ+1gOcU_ob^S?a$aCQQL>z0m~WLV=P7oMluYt8XQ`Olr8!H*WIxSWDkeYBoTXy&C(T(Zme-MFnzK|)=a=Rz71KDOIZMSf-e}HJF^yZAvs6supXMwT%Xx~<i;m^>D4FIg70c^dGR;{kmiGtAG-s(;-e)A!oTXxUzmiOImWt^*qB%>&^8U$ml`QYW%myXP`#I~2lI6U>e4=DIzcAk_S<X}J94VRPY0gqHwM%oBiphSOvs6repgBv$<WHKjR7}?q%~>j@^GkD<ifNqCoTXwKZ!~AAn8q#5St_RSPji-v`5yhU7nj)ouex!^6yruY1O1oJvH$<e7mst9Mtl7|yAHGe|L-l`1efPB_;(~LxIC9ZowU=Y;PPCC>_b}wmv17IA{j2PlObE1*29mJtxfIW$La5y_KP2<Hk$f}A17Oz`k5bRoYvHn*2yq?GF)EMuMC&h_$R~VHGa-;d7TV9Um4AL&#?2J(TtxA8$TJ%ILxqdn9+>q3>(k7>mseYb_(a~4|l!__rpKN{ZJU3FJW-Lgu(d|2Ior{oG)Q;zJ$T~5(ei>7@RL*aK41W`4TytFR%NdFt{HIgZrT{xE~6G`=Kzn9}0u}p)j}~3WNKhFt{HIgZrT{xE~hI*B|qI74C=s&)*MsfMLkPU?^MwZ@^nvz6BS71#96FEH8l_;b<5E?_l{3you7SU?i3!QR5<%{5zI^hfAR)Tnv|Ec{#L!;V>HB!}2|N8>M%GW3W61H7-TT_py8*u7K8X8LY!{9khc{Fa|!r@&kAmrFVw0SdK-FD^T*ESpE~Pg0^raT!ZB`uqzx3<KbUe{tNzr((U0mERREtt5EVIEI)#4VHda>uE+9v*d4~f@$fO0AH#<z-2qO(@&wel79~Hy@)NiLc7yBSCM<7)jxYgEgio>j6#k9Ud%`3vC!xj-DES{O{{uI}9&jVvg5@pH2`0j1_#Dg6;WL!(0#mV^iW)bg<d;}}3AaIKxD{^4@^<J7Q=k<7i{*de3zY5#)3Kb68n>b3*I0fHe}cW>4!9G`JE1#FgEIIA%WvQ-l<omDu$+M!e?rOcu>210g1zC-a5t8BLr*A&neaW9-@~^k-3uzPtU!&sQ1VACe}sFX2=0NuVEGp)hFLHhe!}u6_yMK&g*jNxL5+J+@)s<Bf%UKt+y{Tf@~^NToCKBd8<xMp&nSHWRAE_#8tYN=e^~wx9)SJfes~DWhoBG4g_FUu=HmBPls*uuv8+ao2T-zw^#Fb!hTiZXY`}5@^o4m)3oWgA_yy}g=m&MEQ->N4qvVb#yQ5VP2f-td!7>8}Lk%o|)>aLEcd+_F02ZRoLe!{7$u=n4#(EU`LmD<>xe-DzA5MX`)_nZ7vH}o>#i+9wH6BIDb|~A<dK`lA7(9vPlMsbPumpCo7U6d%D-1C>4RuaKjmJ@PSCrk=dI}=&1U!x9(-4PKVJYlpor>R`tr#R>8R{%Uji*p@ca+`TdIl1(2{vQ783w@Va0Ya+PRDP1D+vQ(1?sFojb~7@Bg%HPo`XZ+S$H1H=b;3a!%EoGT8`g6tbrilEYvv*HJ(Gs&M4d2dJ$6a0=$IfOK>Qh31>qW>rDK1vIGo*b5ZA9)OZmk_d?mdtXJSLco|;B@>LiN=fEoHW}SoIuGSzp0?tRB^HJj!l-wI-_qJY#!{Igf8<u~AA#fh7h91^=`0Z{TA@|u)XDDjCj*@R+`3Bxoj)X06A(j_H3s?h3!B#A{LQhM^y^npchnSEo%lPr7gBN@9<KNB_hrD~MCqMt(d1CbWcYE^Uj;qDHqi*)(H5=>1v)5nk#U;#sPj>9rGP7UH%ziC1`?bvNSFxNozG)d1^2>i8HO<L+b;O~W%YN>i@se5E=gRawJ!&(J<r~W+Tb(8@`0CgC#`2A2KHEQ?y7iv9qOrVQrosNkGMat~gMJBvehGtq34?wKgMPU(JL2`WJKncD;@r~)|0KCH&MWQkPm=e-Ib(O6Q`_PHi}24D&f%S~?1XdM4mdw|#j-2TXRUDV?T%%4oU3-id9^2&J#ikA^KUOKd*K|j8@AU0%MLiFwB2%J$#=ca6PH)sk<oGFm31YLU4EYU?AJeQ`G)gWl+6C~d7@q9UM<7ALrXp@J5MZr^gb=utk^to%2TVvl<9xfvYjLJ{<-4*ul0=b8<?(=vE6!RgObtyde#>uqaW&-Pn3-QtY^MevXuWjoF@){_ZBV7cF#C(mDun08?`L$AF}0KvA+BDT9$tJ_gCkLmlj>CWjW*@|MqOL=;Ld&EYAzmRkA$4%myXPal-ndWI5iLPn3Muk)^3)A6#ww(}Y_eHa@j??=|9y<NjjAQx1!zo*KADtUu);BfemE%hb?sR*SX!W{kM~A*)Ir8Mj)@dwQc0%Q1h`yz@n{%@an9y7jCcUq;)~%uZj%zNeWVd>MV4W`6c%Ja=h!9(`Hr4!B^oIBDe#Ml5and$-l%)M@LCSoZyf8Rv^@9=yberEd>E<2;es^Fkw**ILh&tHf`wU0}p=Y_NKKS&ltsr!UK~&HUiY^4ej3_GRo!DjdGZK6fU3^1_<bZ#P^dh8Evv#P!`qrEYuRBJs)34;yipMV(T8sxA_b#~w4{Q{vZ@T=mk0;=$OHMl7$*m7lH^=U?`e5u<KBtH+nowluTTm$C0@<_BL!-=>+LeHqVPnw>{qmb%^AT_iqw_<AFjwq-88Pz-th3L}<%U;h4DG3S<xj9B`1|6eZ<3vO9s#PZq%xIo-+#A+j!V}sS>%W~{7JAGM>ZRQ7Gme&sRvoH5tc~Yw5U6<MCPR9rSHYN4m-k00=a~=0NH<dakbh$l8=y+CD+f=(xF0<zy9f#MfEm<<`GJ7u5vAn)!%(&E@D^-m0^-NdE*lwEHpk%Z^&HAEb^h28YM9JvSH1n;JrTi}|FSGBfI+pETxBF%Gy;{f8{_=^J+V_7QOFy(;c!@oy=va>P_fNUlowHOd&kNI4vOK@c1|`dJ!uq0QIo_C0lq|=<*1b>9?DE^~^(SB0I<@ZXQ!~E}e5(GPO&wF=p-VD-?my-cE;FI7Me3k7OET35HkQ}PSV!)bD!Sv;%uhY9Z6w2wZ`izF>aeMcGaHv}Y9zytpLkKfRL8nSnTP({Da~d0apbg02J1<)dXzF~Pny}2R@sC7O0#~YRsG^J=%2L8Km0iQIj!<DKOTE)-*k)HPtBa%>c@w<3_srek%8%9s~2Y~|NQ5HT!tU-dC{<RW$={DUCS;h;WB%#7?^(NqlKBptM^EG$fQVy%j;yYo|LK{v?s;vQOaPyQmkJoRloT7<np>P{LE${>U!*(8G71*>37#0ChFJio7r;9k0rYC{KJ|3#VZ%@oq2uk<}}yUjqRd7?ZrRd=#bf*=$hfWx^dof*%PT2N3_m#`}<)TuFGXwP3W7Nd(v;|;a?t~;p3d^>SXYEnjLq?JRjRS8LU4|_3N$+E`#=G$bQ{5!e!7u8S;<rdf_tY{|xzGckOT)Jii$_zq;$lx+j!bThSwvIP<|2m)BiWyL_-mrsCo~GQGdtLvUT)_4V$V&!*d4(mM0ht3q(y$fRKU_&L9&&%670p}X$5F3P8vynB7=>e0#bYYpp9QT@8>k;|a{g6!8_n_LF{Bgj9x>y*pz>rr=|?)~!#V&JNuQ|Io~JJq^+qJUd}PL1lhV_J8e#z!3{t}p*N^}_7Gr@1`8)`ou7Ud;LFr_`aR9oXoa<+|6`-je#^A3vo&-gQ()cg^y8N*=qc<mX;Lr}_?^-00fW)uWTg<Mr%#+V42lpJw&D*QV|`zaG*44B4+c&aX%GPlo)XyH2?b`aeVd*IlQ0elzU+y7K&5d*kGi%+Fu^lp6H<rzxH8U8l9nT)*(ARG;zvh3=Z=^_=nSwdr#&{3-R1y3vAPce;8``276(mplKQ`d``PM%S{g9+WR(^6s^%t4Ak~^`}_<?zO2qj`j;?zk6-!j`Qmg{UgXfy5qWQ)87Ao`E;@Himuvgmdog_Q!c}=FD}nz`1Qr*xeUM7xV%n=Uu#Wd>RCN$RXzMTzmA&pE5rJgQT0oA9X0W@^4j4te9UusF2lz>m*+BkoO5|D!^bw4ZzAK4b1tuw;p4oCJt=07P}#$e^D*4SKZ5y(jpro9@Dqjre)_?I_&EUf#gE)+>H*!L3x4*54)|#gJL6|3Xoa60>|L*zt#zO+-@}&dV9T_!|2AMB?}C5c7ry{|T5rR<`1uEXh@XGMr}+6C{)?Y);CuZ11i#`3tR3*v%GwD(J6rAX)4|#kKkwRFpW5=@+mbujGVSfZ{m?%CE9_+b7r%R27VHRzfra0J&=Ok1;aDCHhe8`@3q!G#d*|(77Z{G^a5xHfh27v7EM@-8?$8m&V>uqiz#h;Uj>qzN7z>?XFPMboB$xnQp*u{)aw<%Oy`d+RVOa*HP-N$M6ydiV_JRFi4wf><V}Ixk^RS!;bD<CPh51;{hm+wTI2aaVxftr8KLlY3mP=p}gdhsbu$1`>5lFyFELXx(h{GXp4wmP@3K#$_pajbjI2%$h7}jFB7S4k~a3oxc<)v@|41r;AC6-sh#c(u?f@`t77OsF1FdDAM@_M)$j)ie>GnO~Qjc^>C0Jmd#JKPE<!eqD;%RAu?m;%$_9xU&HyI?xZfc03ehkIcroCFVJ`7rzyW<wREu}s5*Pzg2gIF^q?JygR2cpA&6;W4O%Q{Y)FpM@u3A)E@&WBEKhW9MePjOEMlA}oh9;dLxuhgab&I2Yc)@(uVKtO5b&V|hNj32WdYcpuC6;qP!ETn7Kd@}KY?TmtLhBP>6H58!gR20p>^6ZjWg1=qo6Sbhc{!wql~e1YW`@E^DZZiBC|{0hE=Kf#~jTP(kYui<X^3;clP5AYq_2M@q6SpEV(!u{|F{140j!O!pzWT1uh5PpAy4X_b*v^L<^vL1z}>|B^OR!i#%*bMEkY-hE$Ho<eS3zoZBZ7rEKvKyAWS-V=Vz-zDvmU~#cTU%f&bi%Te)zNwjR>M2+7JfTh`?b2>evjY5@6={=eDv1qGe37Z(39J4xiNE3b#G7J{MyZ~ypF%T^%l2X9ozElL!K<#9dduzlWqGQc^#7<mOr{t%j5?yCO>#F`N50H4_-`u@M7|V7n2{nm}O1axr;m}vLWZRK}P;P<$#*V$iHvMlWioEX7yxL^*F~<UNTNSg2|*b_6TN=@RH$vU@{p4|6~mOlQHm5#=t)r1OH?U{F5>8Pe$(_-5Q`_#_wlmS$4B?A$!>wi!uwbAAY*oM-D)0f%Ed-SniE;shpR4V%ZbtQaLXdV_A%IXFHsS_s4R7oI7{HdAJXjeQ++_4d>;)SoX!abPt?|`(xQ3=g!VJ&v(VLE6%0zdf(-?L&WNms*H~1b<ulELe%bBtz~(AoquOs?3%36vb;`7UdQr!r*?HL<-cB-61UHpqh-6@8->_)&`DaB_LIDhr5`4Ie}U+_@eVCZ`43mG5vvZoQ_Hg5%YR%gwr2D!?I(F1OFvM%I+pU!PPtIra{TRDmhE==_Chh?iQBX+?I(F1JNaE1ncuYx$N$t-=ceS>;k5j6nTPQDm{f8=Mt)6XkkiCXWYVmjjH({zIN6iYv?c2i^2_BF_SiC9UMIu-!1CWRKK`*~eEic)M&Tcl@$wJZ<K-V-kIp~b9-V)h$#6f&aeLR1huQD<)3F@4l25&Bl9uJTl^kp{QOk1NlDv-PbxrN+*p<JzT+7t%)5B(J*|i_#bu9hx__w#YK2fohmrOoUv20f|`9#Iiev;R*^aHi4V^`ksiHfOR@`;LF`yHRCSoh4S?)g^!?2PW2Q`K6=>lsgzXESxrBlC5NiHylJ!UoSqrF1er{t*WL5eEJd2L2HS{t*WL5#IjUKI=5gUZ+|3?TRb3Hn=KliQn$HVw3B%*7)sd$4~adaz9+B?P{;ncE#`hxI)_lS7p25w>PfX<T|Y*e*5AItp%?7WLEUSK<l5`oyKN#OzWr>M;xPNT919a*Jv%%x=zaLnAV4~T^-XpYSc&LwM^@=Pj;W6Wm?xsc^%XG=lpBmO6!=`QIG%nx|V4@cK&UzYMIt`QeMZjK9ue1nATAf4trnAv>sc1=?7Y-b)A&gF<Yzfc|XnOeZJ=5>j&W>L+cQ}9uqnlww_5fu}3g_ghyL~t&37k)^d$x*g7Pm=$ByYqEwSLkMQx2XtMqk9x`73X(prSyJ)hmPU~cR{L@TE;UCdtJ>0}U|0jOW>h6=e-?O^=WW(=SiWfaIe`H3-6nFAsieGs##lgIo;%Qz?aVIaP_>~t^9L$T!4^IzUkk&Ez!HdZcUQB-QV)BC*lOMd8{NTmp2QS{nI8w$(#w4!g8z0Ld&gL1fGmLBb#t(CdLuPzrOyZ)x@zosSv|j!(jf*P%Bd?>6mlnBeGZoA6w!=MpyK5K~%W*qvWp{Tiq+&V#NnXeDI-+)UEahJ~W*>Krr()S|#i{$cYef}H`$=BM(hr?Ko|U4tnTn<SvYRKRXbq!c*>0zwC!}aCq+)45$?I79f!fuvl)tlYZHm@-Dwgeb-m)-7Yef}H`$=BM+ZdnmjPn@Ai+tlwImE9#<6wsIBHy@N4)HzDIH6&@(Kl|HL;O?cpIqXNO8>}lJM{g%+?b4t<+znhu^ko5aVwc(L@Ji!mgIFTuWM>o$F95++fgyKOEDr9yY@S=CKXFRwB52#3He0DQeHCoM8&dQ$>b9iOZ!P)$I=hfu8v)K$0sVLcF89ycI|h3qT)Q_Guk+hVZ6vU?v!KvD&rwz5-;+N%jFo~)5Zx6<Bh&?%N*mM84nqgc%#NY|0m*Ux_wVwJWaRn*$_{o^$+cJs+iVMv?r)yT947*qKau<M|+eiru8B1b*h-wQM6~OVp@;U-m8jfT}OMkDyH=h?RBb{)={)4sA5`=(cYqpX<bKqlq#n6A?<alnATCWXR2aakI~+%ifLU(d$=mz#`uh9oX0R;<QsR&A%5i<2Q!Qp`NrjPi0^sE2@T_ozH!SO;-5PI<PvXG`Ul6YU^!q)#&IiHE}4>X+zOVHreqwqg5|a;8Lw->a^#e3%QxhbDOtA5a?+G++uxAereyMilLMw?@`D$XAH10S;Kk$zFD5^DG5NuZ$q!y!$WJTer{$BMCa)uwTcu<<-dK*7lI6H%xn4?^<Dcb>DOp}eEcZ;wQl8~#DcNqfA=gXE(tegRrex^{mRqG{DbI4Wlq}n2xn4?^_OqNZB}+fB+%qLhd6uK4WZ5pu^-{95pXH1xxsdl&$otAC?@NwbmRqG{Ic`~wmXhVTWw~BTmgAP?j44@O*DUu;$*z1h_M&8J*NMF-*|k3#dr`9V1Iw*avXo~zT1uAfvRp4EOZ!>Qn3AO*SnipUU3teRDyDYHCn|RBcYLDaLf%&)?<=3YFIrbPdtpkZ^@+0=res>@ID27AruCAu7p7!dcR727N~ZORvsb8OTIV=>g-WLNlCxK+WLj4^dtpkZ^@+0=res>@ID27AruCAu7p7!dcR727N~ZORvsb8OTIV=>g-WLNlCxK+<U&4GA)hLrd@70?IJrPdruc&wQyjyKDIVg*6j$+Lia&TU#WB2?;vrs4esFSuluUl`V)BC*lOMd8{NTmp2QMZ+crp3Giwk*5g*>Hv@|5It#Bza@EXNzmDN?c=w=6eF$#VR&9495q>xkt_DOt+1oFXO5c3EzclBNAD$4SZ34=fi*$x@!>6e(G@%W{*HEbV7GPD+-3V7XFCmhvp8NXfEYmYbwxX+O(xQgR_rsgS3XPo9z-w=5S($#UGXoFXO5am#X(lq|<B%W+b&yslZUl#*R}Cl;Y%YL{XfDt7I6Vk0V+eqgykN|y30r%1`NU6z}qWNAOkaZ<AM1Iv|CvMcZSM8(uD`9#I8{f<vmT*y-@<SFHor$p-t+VfH|txsrgNX4|yp*<!Q(|U>as#HwtF52@_F|AK%?@YzC&Y?Xx71Mf&_VQFr>k8WQQZcPhXm3cxw9cVDCKc0qiT0{gOzSS%^HMRbPiXH<#k9_$JvbH9dWrV(R9wjaDdhj;lmGMnDHmt%I<lA8ZNgC*4;BXO$X9r=FyPEh^Ge)0H7pF+k+1M#;m7<ptk=KQrI8T|nT$a_8H0L+x=l|RFMEW6J<aO*{{RIe*<k', 'agriculture-fixed-long-lever-open-side-baling-press-01': 'c-rk+e~cW}eSe(6fH6O8jLnaNmo)(cd*^xcd(PaA?X&N2YHY`L`5{cMbGvhQTlRJ?`@@HE93`bLLbQ+wg$k6YG!zk31+`L&NEL2V(mz@W8mUd>lB6vNscJ>4rd1(rLaKhhZ}#oZ?#+8M>w)}rH`>|H&3xYbzW4op-}imLGdou~HaSEHdHb`3{CJd*PaZvV@KoNb*ZoF*^i+P%ulhBw5!CXd`Cp%}1=XOQn}a5~Jr%!N@@u*MI}YVe=p)*QZsiO46Mn5;4yr&_N0j{OLcU&v4)UW)8`blp_n*pFy#=_IKg#YE^3|ZkZm7xwryuD4dn)fg)TnuN97Zu%SPZIuwJ}`_D%kd(dHBvXyh<fk^SxTGIPWdYz;Kq}3d&vZ>+?)(TNdN*_5H<(khsSyJ_x)tGUm(02XiH8nnOm-uj34dxxm><0Ltk|q+*FdqY*45$vjl`b4wAq^>WE)lgb6NFw<hgtIjnm-3fOkt3t^~p%3Nb6Rb%E({x&%EkER!azLuq(TDt8#Xo`CZB~l4=0aDP-YaYpo84KSn?Hc`-48*JDdq{iRwC0JZdNOSS1MQMa&un8&(-IHrD}Ub!J=O+<f=g<=jBd#m2wFPrQAGlfwu%x?GDX|8QP&{qrTLv&iw|LFa_<ChIq8$HOfU$dc!MMaa4=tYVNm!a<!hTf2Qfx{9Mgj$a&RLZmx+|D$e`<gZ1t}%$R{3@fN0#JW&hk^~2?AI;+fsW^+YsGUJ2D`l4551DXjM^WnN%4C;-DXscH=T4pjd;RNp`y(3lv5Y_gBTCfm~hDmL^MXnL#W`o+2R|AuvJ|HBav2qJR1J-CRsNwA*XsF_qBTi)Zj`9G=*<USI%2n_s=!W@HIt9Uk07r-}kHrdDxSFds>x&p5OF1xGXe72IxGzD}04JaEn8UV*<@65gh*z$I;ktcKbi>bKCM9W%lj!F#7w{&p9VhF}#l@i3K)po0ClbK=V&)NO#XRR|*i!jegi^Usno4NB({tBTnd5{$1B=Gbd9|Pkj#8|!O#^zU;ULksD?uYNpuT8&)L-;!xb!>g2*oJB@?mLdhLuiRVSI}Olo`JP0j&xc{f;{_F01ZBj0~kO5+7w9-QBi(=$}WDS3CN2#cxEn^5$X<7J4Jp(Hv6@3}?oJ^@8g?+$e&@m3ss2i@?XAOY|hRo)1HyQhueQF%w3Ua%YU}iF38`V$N&y1;%RBLHYvlu})(QY*WxaozTwu4JXL9MYichMD;~cZhG9|?rc+22Krgp<{Eylb|ZrN;^IBv=TmL!9@vtrb9+KQ$e1rzN;L?KqxUNXT2KpGK`$5uvtSkMf>VIl29XBVHmoD?U+@<&5~vKOLLJCFyMtx<?{v8YGCk0Gu~}&}YyL3P#xSaXn5lml(}Q7_L(H&|46^_|tWZd6nQ5j=W!xRYoOt*?xLjwu`}B!&z3Ek^gKFhuezZ|*`h|P|o>s0-Ly7@@G@8eYZ3WH4t%spEFvtu}ydK5~e<y_0W{vAF3?+4FP-n|_sk?{I2aAh-ZAT?o0)GmcbMrf(wO4}MFlWD3h7`7tud$4Nx)@;iDMI?6KXp9smAu79`GkKwKbo8MDs{h*J09AyUT(mQW3LCbX_m$J-aHB6tv+4ys{sU<o?CtuCeAJ$&rjSpabVxk<9WPZ_i#P3Zm4SGmBu`dn_bZ(|4%P~xUl`?{(JZB4V#}R`%BXm?<7nrBK3YI_JPyrVQs$xS8OjArj$FGwkCbQgb@!MW5GiuK{HmCl!E3A1U#^MiJOl5r&n8O=f20vEK4rr7iVgB`4~^i#UrSBD1w-ap_5Mpm7q2Wy2kqIeq}`06!vFPLp2ObFDN6b9bTf;Q58pZ;1X3G_GhRXHC0;&f5tJkh4AiRAFpwFooge|3G2-?Z3l!Ir*YYcC&Y5c{ou%uGS)Gi4>q4rn4+kTt*Dx+vI%M7=yg*w44XO@yB6|vY5~o_<rz1l5yR-!McfR{wou(NZOx))!VLF%wFf70;hdAfR2ojkwiU|(v&C9R8Bq*9yl5#fVbikAK}^<Gm}OGXm#!vE=rH7z;r7eI{b2JktZ+J-Mimq00AttNHZ&Yl(M=sMtu$-;+1S04p{LpUf<WK<Y#_E?hq=_s3uO#PA=zs*YUP<`!)FsZeCX)@WBU&sWTFoqI&#<U1F(C*Dlb<{<sx#_?otNQ=?74g@^U@3NUbYUKSz;aot|2v(UoXskVw-@w7L@QK_tdh>8WKp5mPErp;$9?rBZ>^_yRn&bgTn9;<X;}dYVbED7({3j+mF415G@(>P{~>Vr42ev$|4ld>x%$aKzMVkEvCfAUQ>;oO&2)#N?_boWB+`iWQ}DdZBtms4<ArSC-1@g_;qe)*wPf<#2k@c0{z3UGxC6)*_pOMh6ltC~?z^j<}X4cCDBt9aGAtmm2XcZ6M!@DOuA?jX0M!kaNY<tm&mj{7Q4gQ8Q-suB=~EOVuMTrT4g$o@7`-F`Hg=H1E)*YKA<^E5faMPz(E<Y0l32wY#B6Vi{AXKtFbJ5yodwj1NT^S|f~43*JL4M>H*#;aaw0LRza}{_YrIQfC`F<b#$|7{*G&i00~;<(088hg+IzGQLVRmD;AmQpzwd)O20bZR{1haEzW*9{OmovE}dHH=(hLKRO4RJO^2GHLkhVX^sxvZhmxP_krC<R&<~ZphJgMJk*A)+SDC2wgv(XD3;NiY4@m6x5AsYNflLP**aCiN&}2UEnPQsrbjz81(cTtrMi`%M?IS!jkIbQ#_Be#B@9(JRK;c$Z-2eR^bpQKQEW$t!o;+C^k9Tlm<@hrg5oTpKbcH9mS$O+W0+ck9?Wcdum*7lR^?O828CdCIH(q|>}6fRylutSjE_hKb~Y6_^5&M>Re@%P{%`2EW~!D}pd(hhYUY(Rj^DPF{*ch|1BJG4I;v({;1f`nj+i#<L<hAxhEACd`c#_~R+QvfNZV6+V4<3t6j`V`$eME4jBV3~&}!KfeWAbVhD(;BA<x1k2%o4T9Zd`43e_|Xlo|WfW*8rJ(9j_@!vdSxNr8oG+1!chSwl262Jp!ClN`-3VZQ>e1aDFuGn_DJ5tPefG&ro&zoz)ARJ8WfAX}xd(<vtF#9$3{Sj}J#rb$C({i>>M+Z044Dbmd7k^{shm{j=C4I&7{5tA*<a8e3*gKC&ITbPQ`^XM|_PkOlD!!~8X=BBb`+4q#LFib}jrFXq2DIsHUqE31xKtSn<PHI6NQNpK@rfC@#EFqW_4Fi@1aon*i#fUfpRqXa&4cjnS7*!C4ViS@8O;JN%a>5=u&)*VMpeh+t9-4JQsp<f`oWd4^Z9vke=r#r+J6ukk%!EZ1OYePF8g(Ubx6t>%KOnzRajUePP_<NtFa&uIb4T6iNsW>enK3e{dU`cLAn1F_Paz}jOM}oC6rndMX4r*hg2ULBW5<Q~!FPMr$fyN#fE8thkD5Ev8(a%&@4FH0BT|BuQ3-ZNR|p@t!_I5L>R>a_X}BV&X&A6+Tbk4rV1uF2O-i-SC9*i#w4f;&U12aStZ;>oL<w5Pic%XOI6}D=CRmX5S`M;cpY4B>gjz7$B><%LrUCm#bdzao!Bi|L4#3}WMW}smbcR>FMoZE{#@MLogCwsj;yb9J-#y~vd$%66!a6`#42?n{z@kzK_XwV;n$9^y1}$TF)CLHTkR~y+Vb-K$x;>y8Vt3n*L<t$gqh=3~frn2?x+xYUU3xex6&%_&Rb1#a%*`Nu&~?S3c27yDn{D@Z6w}fT2l$S`+yin^)1<gaAoDcX&I9>_WonQ@B<aA(mVWC>S{>kuu+%U`f>O>gC_XIfHyL|2(9X$i)39xfb3H4<q~Tj?!!R7hR%74cV(Mk|yzABNq$fo*qaxJIrLjK1Q@5D9mbPEuTN;J+r8o{-CVJ0H{ir65@Bsu264oI2PeH-TB_{EgPJ7TNY|vk~ee~fidvH5*vf&@_t8)$f6}WAO7Y@zNvY+t7{RaL>6|;HWG1cx^lH0NiX<MVMqm3cP^fuN85pC*rhJibpnV~gRnE}qZxq**s&b>KAvn)1K1~D3JE`7~4%goSRQ}sax-``xPik`t~bj{4-HIPr4=kD*iqYp6l6`C^?nnm#t^s{&k?2TDm-cqzIE^ldSmcd)5k|9o6wv#1LL8hI>=WNx;5~^$?lih4Plii?9$znH0S26{8)5)Sb*xxfnc__Uyg?Ys=l}zpJOj{(SG}|Ug^=!K&<lmX}hY4)9O+M2`NmV1$PD!DDSF*I%HAT<T-k<{ot`+Ug6)}IHxJgYl)AFUJv2y)(^5k}o9O(dNYvHdT{&hDYd-fkBk5^t?9$R<M_?vH3S|a=x`wMOo=KLeCeolxvUxtzY<m*kB_Zf$gpM*I-+GjuJd>JO4zt6kv?^f@3^lt^njp4LX^wUbwj~g#j%8`x7O);Jo{hUWGB<tY3j+{>}C0CHmaNbO=gga}<<#4{7tS4*9MsgLLuOb(dA#xen1m{iUB60z_glvKH7P5hS_|l(&pPU_g_L*m16XE(ib(1jXf3W?tEfMB?8AkrrGY^jQKI1U*lQ8E;`|QV@FT<;TDEGsAoo})@b86GeuZi%%nJ*?{&L3O1)DmINmto|eeSXp9ea2zrCt=Qy_Sug)UxruxNA5pg`Kz4EeL#e7{8Kd%b3W=^ggIY^k<WcVgpr?wIX~KGKjwTHUiBZj|2#eM__sgU{$t1)KHZYxGw;3SKKI_V6n}f_A6!i<O7W(b&$^plo|9taf3UqG#VGf&#XyR2{NM*tJUjbO9li)F>)!6j72&hbzug(X2qT~CL4;8**Jm8w_M>l&bGyhew~GvOyT~xNiwtwS$S}8y40F54Ft>{gbGyhew~GvOyU1|VE^!#wSnaoeXZ-r9CAW>2L)^PgyVnW%@AHiod{%I}*9ie`3;XTobgy^tvY?-qjME-ZtCzomGtN0(zL<k!kL#y<osGwh8&CWCxQx^8$L;0Ej>qlgi#ZW{xhd@Brm&Zr!d`9)d$}p><)*Ngo5Egh3VXRJ?B%Agmz%;~9nKKhMsjdmPp*Yy3)E+upenlzj!U3Y!&+?!jvTwYiCw=4{=XK!hsYGUncNCTf$V@oB?cTe*$Kxu*$u~DU`)Y%ylb%QyW#&G@I3{U;~H`coNpnYfC_Rgxed;@k?l}bUQCAJJWOtf+VWCD;Y`U0RFhW_9nLyYptih{Sa7z8#wtt)&JHo5{=Ayp0p~l&D7l9G8rcQsU1W@0N4Am)I8P9l+(7bV63&xk54jQMe-oT<BKyevm%f3|2gd*J`~UNr2yc0-+Cu#93%9!>{Dm(U8Gh<&U5Lll{Q>LqwEO3;i7?8Yot<_07~(L>Ma;(#hfywKK884qauM?}#NlWj^z1X&F#mb;jRP(Gw6C@LIIT9v6>;z$?=Q-i$a16CxF08s$4xOFH^q2d*?88#_r>6g>%lKC27kt<An2Pzu!1(g8Q0YLuy!`Vc@y~Zh3px~h48tOJx95edHZHEbo+&4n)bZ=*5CeYS%$a$=#Sj5y8kQ1d;j@4_qrXwl;Vw#Jm<bVbzVz`k^jA)t&w7s`}_ZKffVETfBNEDDc<||A9wg7yzS8!x^e~h*t;)u#xKIi=Xwxfl-to~41R3)bK~4DGR*BF!`v=1%<Uq>+%7WA?IOe6E;7vRBE#G+GR*BF!`v=19JNavUd<<0^U2kG^5e@Vm;dmG%eNl?o_lK3!IlUgdv~9kggO80^Pd-D&X-~2zdZF$r_VTy{3Oiz(LVbz=gaWw^ECPMwCi^K<Ji_Szi`)`eae;LS8w=%`_99SmJH*wh$OuA%$i-@{#WA3SL)+jt_*XzGR)=5aIf5zxZf6=>!(|LcU&<p({oCW3!G({-BWV7EH}k?+!W(+Q;es>!Fm-l>&qbHzJ%4U8zA4_0vY!CkaeF2pGzS($2XH};Bz^9i@6!j`0nyzXulrL>mhId!j~Ue{><1XT}{)LMcDZCwQdsT{GWX4-j)b+z6>M(gYCyVea2zrCt=Qy_Sug)UxruXSmJwuF|3{2&#q(fhcEqSBIbO27bC))FT=?H?)zWw^cjbdpM*I-+GjuJd>LN#AG!bh;Gyz3_W=<;|L!LeG3TSsMVRwt82Q`>L>T!=nDe83_G8YM;Z^@hjz4$4^DN{Q-(MDCT#re(%Wt$qxXTw~<ZnImC!IdyF!Gadmmlr37kBw$yy`#6@rV0>2;+K8!d-r&CBj|47$cwifCwW$33vI?K6`POFUG6>Bln+R<C^hz9zN!7J@ekO2$yzFCt}Wj^NsZ_5$1duM*i&VzjXSH!^ls<oFDD8A9KD8ulkSNe?GDHFPDGvsaMCa)(~N=S&}g4W6mJLoG-)3Uw8Ihm-iWmk)MP)KiX$M=6o4m^&h$aV6Do1K!hLN>?C5&N1cl>=gTnixetgi@{=&<NBiu@oG-(x{v-FFjgRcYciy``eCbQB44-y?>6-ukMJfKy&R@7E|LqAW{`u#A?tZZS_oNv4_4&u780EfFdQ^&W{6Bs1ccpmGZ=Sb{^F=r}Gqj7#72!v|Gqj73Uxbm*^&rA1m+LbQAF%#roZCf)xm{$K+eL=CU1XTsMTWUuWSHAUhPhp2nA=5$xm{$K+eL<>c8SBQ?_pQp!>+!E{rKL)UUBcYmfw8i!1&m@v#*Kp4|l)9@OR(;x)A@@-+hDOZKID0@!#L|HHM#jy(z@s{OhMXd=Y-*z9%|zMfmB7$2;Q}Va`AP<j}GRbGe0uD}|Vk|Ji4*5n`?f<cl!ZC(0FJv<u{AF1Jw}Mm}P0qd1Im5px^GVH`hVZlgGidf<E!MtyR*B8+z7;}>Dh=QfJNTrRg!9OmQaHj2Ys58Os^nCp|<C=N&S$4Knxi6c=Cj|;d?qx>j`x50HC<@a&=Vn>KY9NxaapXl{SOds!?SL{A5=%*#(MB{jrFXBYz)e`8Z712*ipyyVME!-6La#PsLO<^xLg}vMq_Ht9$%S~Y~H-)|26!vmc*vm~}FIR4_8_5lDTt}{k<0`U|y{%u*-p{XPzpur=8`#~A?D|^x|7!RqWFNVS+ycjKWEc*GXmFUsf#VM1!m$S!``|v_)!20x{vU?#edIiH0l5{<x3b@*UqlLUF0kLFUqW`kc}L&x(l2AbOTP?0D%rq(m%af$2K&vyPB`x*HrY(BCF5`&@B3Z)_3U@)*TZKw$+6$1=isxKY$HSDW;owWrpVX!ZDu+-{^aXpBE03Ts+)v4f8E)qS|ZH(GK~BuUw?m$_Zf$gpM*I-+GjuJd>LMSjv;@J@&7LHg&+'}
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
placements=[('r','agriculture-fixed-high-wheel-curved-tine-hay-rake-01',(-1.40,0,GROUND)),('b','agriculture-fixed-long-lever-open-side-baling-press-01',(1.60,.40,GROUND))]
def rigid_point(instance,p):return tuple(p)
def stored_point(p):return tuple(struct.unpack('<f',struct.pack('<f',float(x)))[0]for x in p)
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[stored_point(add(p,t))for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,rotation_z_degrees=0,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values()),coordinate_storage='Exact IEEE754 float32 after translation, not hidden deformation; native versus final GLB bound unchanged2e-7'))
base_mat=len(PALETTE);PALETTE.append(('SceneOnly_EarthyHayEquipmentBay',(.31,.30,.22,1),.97,0))
v=[(x,y,z)for z in[0,GROUND]for y in[-2.10,2.10]for x in[-3.0,3.0]];f=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];emit('SceneOnly_ContinuousFloor',v,f,base_mat,'Single scene-only finite equipment bay floor, no extra counted model');FEET=['SceneOnly_ContinuousFloor']
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
  assert -3.0<bb[i][0][0]<bb[i][0][1]<3.0 and -2.10<bb[i][1][0]<bb[i][1][1]<2.10
 for a,b in itertools.combinations(names,2):assert any(bb[a][j][1]<bb[b][j][0]or bb[b][j][1]<bb[a][j][0]for j in[0,1]),('Whole instances intersect',a,b)
 contacts={};floor=triangles_of(FEET,vertices)
 for k in names:
  tri=triangles_of(names[k],vertices);mask=READER['np'].max(abs(tri[:,:,2]-GROUND),axis=1)<=tol;bottom=tri[mask];norms,areas=READER['normals_and_areas'](bottom);expected=float(areas[norms[:,2]<-.99].sum());report=READER['actual_opposed_face_contact'](bottom,floor,plane_tolerance=tol);assert expected>1e-5 and abs(report['actual_contact_area_m2']-expected)<2e-7;contacts[k]=dict(complete_ground_contact_area_m2=expected,actual=report)
 tris=triangles_of([n for nn in names.values()for n in nn],vertices);rays=[]
 for p,d,length in[((.30,-1.90,GROUND+.50),(0,1,0),3.8),((-2.8,-1.90,GROUND+.50),(1,0,0),5.6)]:
  assert not ray_hits(tris,p,d,length);rays.append(dict(origin_m=p,direction=d,length_m=length))
 return dict(instance_bounds_m=bb,complete_instance_count=2,distinct_old_models=2,new_reusable_model_count=0,whole_oriented_triangles_and_pbr_retained_before_float32_translation=True,actual_full_base_contacts=contacts,selected_visual_clearance_rays=rays,not_navigation_or_full_space_proof=True)
LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate(vertices);result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,.98);ORTHO=8.3;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(7,-12,7.5),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
root=bpy.data.objects.new('OneWholeHayEquipmentPreparationBay',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole scene horizontal centre; continuous bed bottom at Z0; two entire unit-scale qualified instances';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
