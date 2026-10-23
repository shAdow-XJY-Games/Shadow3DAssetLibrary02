"""Original complete cavea and arched-entry forecourt scene, two whole existing models and zero new reusable models. Lightweight maker SELF_REVIEW; no growth simulation."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='classical-complete-cavea-and-arch-entry-court-scene-01';VERSION='1.0.0';TITLE='Cavea and Arch Entry Court'
DESCRIPTION='One static classical theatre-approach scene. One complete qualified semicircular tiered cavea faces a complete old exposed stone arch across a shared open forecourt. Two intact unit-scale instances of two existing models, translations only; every old evaluated oriented triangle and opaque constant PBR retained before explicitly declared float32 output storage. No column instances, old arch cuts, seat-count changes, invented roof or new individual architectural model. One scene-only flat stone base seats every complete original ground interface. Full transformed-coordinate checks, all distinct instance AABBs separated, whole actual downward sole/contact patches and selected approach rays are checked; not a whole navigation-space or crowd-access proof. One scene and zero new models. No historical reconstruction, use capacity, structure, public safety or accessibility claim.'
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
LOCK={'classical-continuous-radial-tier-cavea-01': {'bytes': 79700, 'sha256': 'bfd101d4be77f680802d1e1d3ffff9e557949ac70b5a08efd4dad45fca401e1d'}, 'classical-complete-voussoir-arch-01': {'bytes': 41332, 'sha256': '8db64d9e9b8a754108ab6b0441685616019fbb235059168e8a65df888591d27f'}}
ENCODED={'classical-continuous-radial-tier-cavea-01': 'c-ri}37k*W|HpssZkKE!Oe5Kuea1GQv6C(9gh9g$#xldq*pfXY@yU`<geZ}aP~mg07D*+kY*`bsheQ<r*Eyd#*SQ~e=F9I_|Nrmz`%mZbd48Vfe9k@h-uF58+~qSq^&Qx;sZ0pz7%h=!3KH^Uhqi4-1t(@?BxeTK85P_&IW;*wF*7YaxK41(e(7ncX&FI%u}DzEfyt>!$>~8YYPAg-7Ev?2W<+#w_26O2=@}_$si+)QGbDI)_27)&Xdt*wNS0*;*XcGYI5lw)%7Qzv&#DKfrX{ftLc5Rdem6HNIC(^7dSV9Mir#612B)Par)Ks{PaDV<O-b!LFgd9Az_g6yq@cd(X+yCwNkJLOgHn2@r1u^=FflzSBNK}R^-dg?oES7bC9_{puk^G;S|>3RO9y2pr>7_OPR<BQNu@e;a3&h)HIilfrY8;z${3V5a3J<DJuxW-*~F9#tT7`qd2j~Zu|dfh{n&nG?M!?>Y*`0k{T)-1)02}r(2ZzBw;>*z(4IBbfVPA-uwVUB1}3E^BVOG?u<Lhsn8m+mN)j6GJrJ3c-iZTi^iE5~mJdxEno+~QO*JyHjv8zaYlMU%l6}xYnLU$I(vy2<`n#b<7Zhh?VwZdO9F~$XG;v_hwA6tkgX?6b4^6HfoR*%_Hzl=aQex)NL8wg&gND;R3F?QBo<(ce^IkN%8A0f+%=F~CL9{alCTAuG^+`!h!J9w&L9_?Z`ANw^z0j?Rh&RF)ba$Is=myhHq9MUnrLzIllh!~-V6+8~N(fF&N*tV-GAubExK2=?#DN*f)q@iJ-Jg*{yUn#cExjijHO>!5_8yp=(K9JIH7zB>*<NxgcA6C>1UKr^s8y2=3Bj~HBa!YIYbG=-hL&XZOHWQrVkHqmzULsU&cA%q7Ed>6>|cCXO7ifY0~1GLr-Ze3W2@~xnhu(*vC=j*nGF~JaG(Q)jgVkE{0AjsG@{gh2qdKq?S)~5s3!3);|C9oV$b%;nThCy)V>YVl13t?gL|d7M$y25DZSgL4ei?xM;seZy%IB$8>J0QOK*xu(}THNNX>|-5cXe8ctk{0WJp+ab(HywLLzHNg+xR}M4~9%UlJNxJ1nGjSWNAx>Y;Qqv)01f!-0^_S7?{jtQ}sP{TCe-8W|HB5jL6*`v0^~9sCDqtK_7<m<S$hpQ8LLjERh@9T5`~8IJ9b%-YSc@R*3un8+Bqm!bYzQ86)5wWDJ~BOhRwVxs-cMMOu%ghz))-PbOO$NhutP-K`tfT7_rwWFg$Xoo~Z`GXo06B1oJBs!G#k$)dUBf>)>Lqj8?A83c1T@*T+jY7<B&dK_L=Qr$Uddi>_dNBJNO3chmPw6!@Gnwt|Q*Ar6=-8rd8@5?(+O}`qpjB|4P#hyEsYxllX`QgU2Lme6FlX07_}vyF#1<mO7D97sA?j`m(P9fRVhdrT*$FDKH$KWpOZV?puc3YVB&T=Aq0jcjK2voZIT&G!3=NB-g+o&@zlDWFgwys$V8Mu*Sz{2#R8(YWcy#s9no-fL2;CPEU7Ie5bEv;_a4d$0MMlL$(5^|Lr;8f*HV{(1hU)^EY)gVWH)#~kPCDWihu+T?=hQ%$TLa;C15ptnF?ItT8Z~Iup#42fgy*~sIBfsTpt(#2G>q7A9N(eQ5uxGX;r}6s5%;kJIV~TVa}04@M*OE3M&-N-(P2D<m{B5P!a^|}M#O}NBY0tMF$}30jrl%0Iy5FcCNw4{G&=Nd3|(3XsTq3DiQ~b?V)TFBhnyCV`43TyxHpK{pt~)Ihci2rdyULYZiP#QOkC%MMMQ>1`HR~2>BFv#Q6n=ky)V`9h}uzMcem$$md+}=-xhE=64*jS?U3*=XA9vuw1BgHjI)8L(3psr``-kY2GGwBun*y(Q2`A^hvGQ9|6Pcol^x4Rgaw8m?17e#45|G9I}jEVxczjr2X4PTsImr>&_Hw)jv1Up_E(We!xn8wc=&n`ZoNpKK6+esUZlu(uD*HYI_4+(UGrq;A<e#Jerm#H4{ftbLg856K6lzCce*Tf-VS$veXp>rS6J37EbA4P_1eqU&$rKBmOEXRJFQQhFUvjOBdgi=4;pYJTTi_FCG#n3_p)-j&Ag7&y{=Bz73fvG%UPS{YwyU`wMyHV*Z67+E2rz?b)4>Xb-J!VFB$q8Ym>$)J6}*}1M|j>m$7oXE?&p!URS5<3iQ}&GgzDEhBvbHa)<r<UVqATR!-N&>p0!(>U3R!-f_@q)@FqgGqUwZf1J&{*QFt>oUV)4ak|&l>AC{FOwF#W&9aR~XY1vsjbYy7XlqtZ*Tw5N-RtUfU4f2E3D)Mo=-%0Sks|GwCqGw<mD6?cI!^bxI$c+wCsfMI+H5hZO|~AV1TlZPWl2^}*Tw5N-RtUfU4cGs(nqnh%}FVqY`w&g{ml1m)L1!P7q8=VudCB_1$z7Pby=Gg8b@X8k!`y&&n)prEG=haDXWf~)B4nDebN1Oyh44iP~R)m_uBQ@ILxZgoz|gF>yWJf__)Z)FI~LI>ids<e|eybb*N*#J|QNqj_vUY@$m^Uadlc>h>z{)7oX7Yu8uL_6UKl~=y%)w>+%Zg^$P3t3hVXS>lMa{?Q~fo{yri8J|2HsUl>=mV{DtkvE%AEj!fY=GKFI&z`d?697ndJFHK>taCOWZrZ8`q!dwyHURM|94cjqynZn%Y>X;`@VV*RFxiP@Kt}e`zwqvd~g>!+c<Gf%B=LJ(Z7X-N1)rIqd?Kn4?!nx1YaUL{<^Pnl5`vTnS>cV-@cASe%;au<PIPaUndEXSy^#Sg6b>X~kJFY!U;o8R4ah+od*EyzeZ4=;LR~N2xY{#{hDO}6BI<D(X;kwQguH^#U>*~UFo$a``G==MASI0H8$*-Adxo|xk;9gf3u48RStWDwC-qmqE?CP|RaNTYS*X;r2-h13%=We-h9c~KO;kM)4VBcSezU;(#=4W5O;GyMwy?*!F&fEEL=P6cy>9t*+<Gw@8>vUh|DR+Js^G=;!@!X!VmHDuB!#p#tu3$dq{brtrGiNeiG^!ldmCF3%3D;vQ9*ttYHrk3^m2jP%&)Vgg7yHQAk<1&n7|Wb)kDJqN3-r6^(A2E+qgOar270Q)(T-18uTNN)?buGAu$?|(8*ImZnS8&{uF3ZoaWHut5FeAr2XQlb+z?Nb#}jcjd7Ke{lgA%@X9|613jOPFp-)YrPwlZmU%bBP1>!X37dD>p&^&L)?_S%*cDU1Jsncae&$CBjZEmge1#?;+=vzDAVB?|rrRB_Nd7v--^4F{}Jej$Fy-q(I_amz_q+@&Lv^>!76!Eb-uMI8BoR$aroTYEFI=)&*VyV;eK&R`YbygL4nK>;F^t_u}vpVC}R$xxc13l>R{H)Fo(`MDDPRj#*O#Dl1yxyrkyB>8~9_Zxmf8*FW4dr~C2fA2?I@<9G?fZoGZO8VQ!giX%cG`~pGKKv$h5fZ1@iB$CnL^xbN1RO|{-zLr+tFX9(2u6jkG7-VO<_Ek!g#P9<Hr=nl_`uX+c6GJVSJjx__Q74*%HRNC5&_1aa>sZ_@XWxFSg@YvV>#P;llA~3CE))9FMkl>Qvl5u0?NFs2KChyH9#(Id9YNUfacE9CbW_p0%upAN$n#vCrLqehRmj<xZF7PU}<W%X0V6E%Bba^Gv+w?zY8y?#?;!p1X67-`B@J#P)IDSd+~&bbI)mBRXA|o6~jzz18)+tj*5j7qEGWw!`Nr(P=wwPTL9e*&Y0IBRx0LdCVWr$@jQFR`<F;4o=^C#eaSubiD?f_h>tO4iufX<L0!TKpztFJ!>;<$SHc<v3B^JDLQS(&1pM<UgA6dv#&9`$FO;ow!`OG(P=wwPTL7|dhVoc4(__NK8*!!htJ8P({|jPwiD<V=O(c>C)Q5dO6P6b4xhtCr|q~oZ70yr%`eT`-1U4}AD!oEJABR;ownoVw4FdtyYw2H-_<c)ee}FQ+u`R3H>dTf)B2**I&@vUK6hG&I<L>&e-4WG+&v$~+x4l_I>NP?FYDQbho6H2U93YL?f8WK@(KIm>a@PFU$!IWrVw*eh_mgq9bw;n!oK^2eYc%1EA)%){`00C6Q2+hACHOuylMBN?HF&SFy2gIj5%BwV-6R_o9#F*OyRgNg=4|t!m;3R;kd9J$FC_Izou}^I$Str9WETdwqu?#g?Yvl<`#zwbBn`;dB%3kho&$en!+6DaA6K~xG*2uj(OV>=514$s~s-P)eaZtZQF5vv4r!BDV$RrE}T;wE}UO%$9d2a&V!b4?sK?s?sK?s9<&|T4;H_Epw}(JdEeo}Io;vH`Pz1z(=Fjz#o@yBi6va0IIekw>k~`3K5>)_*CCd09pWe#t~V^<dc*d{jUTtKqeLHnD46-Rv&TKOoNu$=y|(jh&Z=X#$+y8@$G@(gtIDx9uY9)2Q|Hr?%zGF0dO9^M#GHP&(5Ai2yx)Sno)c~S_eU$P&y1aa=L`Qc<%tvO(`QUnzZrdN>-XuSm@hf?qHkm2s?0yF^ocKV$|`p5_+jk{=4>8waW+Q<xbW=S$De2OIs9I~=y0^-6V~e!)@3`k(-gMTCv1c5*e{ds7xvfW`-?c3JPwGD$>W2#Sv+otr^VxmI9oi<h`+_-kN&lU{<VZL;BcYeEur5nq2Dc`-z}lv?J<V3xVz7b?)v7Hq0DcnN9eUc+}-Cz;c<7L3x&tseJ&Jkk1^_eUH&@p_c(2zI&EL{e2>&%>n)gXEpu8P=vBNGS)C!vCo*UAWPq0pEfdH4o;ocL^w?_tvAyHjow3wud7yV3^fw!~ldfN@Po0(rdYPIBS)E%8ZfvDa%LAQ%FF&EvTR#7H+3}u0PpCAN)hW{SPv*2d(8o=x?f<TAdufw8Ef4he<u|kAt3#0*%xQU`3*QI%pGl*fA1{F})}fAed_wy^p?%x2J*Kdorm&s1W4}yce@$V3ZRgK9vtnfmakCw9Hih_`Li}w<f0;r*nnFL?j()d<@n8w#!FG%vOBh#{Fs^LJIJAWEX$j-gc8q6B80VHS&TYqWVew;-x^TSMj`dl>@#}Emn6-ps))J0cOE_jN;g}WY2it>#8`|@O=+{QXG5@RFK@TnG>-D?WcD~-MI(D0Uz5Y6P=ZfaXpS{Ov9qx4Apw8zI?pbq`N0_fX!uHt9Qs>KZr}f`!w!~hRJ6)DLtxugV%YEbXby*xLwOzsHE4n>=?h>7@%gt#!fnKtke@?!gI+)FGv>iUziB8*bbJ|XzA1Gfr&j0MUIGYb?JA7^wownoVw4Fe&sg`DKn$~zWf6{jNTq-(k$IWRwfqtTi{~1V)qtW#E_0V?s+$%b5$IWRwfxa-o|GXmh;_GzYVD0d^T6Efuo6~jzJvjIi*5;Qdb(7BLv>iUTi%#2dbJ|Xzw|Qj_YjfM4a5_)2cKEqKblQ%a({=*A<*nxaeIMD8oiAuR{M;crZO6@NJAvMK(@u7-srO_*c7CDl@N<ou)B4nDebH$hx-MRyJFP>V*XK^_&~4!Lxzjq-X&vD?fd6@_e{8$DScf{=@d^9o6ZXZ`X?<b8Y)8yZA?BtKXWMBz!oK^2efJ6bZaZC8=oj1RvO-LJLQH%-CbYiLkG5mHnZkH8g)!!EVT?Ik7;m=YxG;s|!W51LhYQDo!-eC*b{xN^aQvFWG3#*Qn02^t{MwFr#uDZkQ<z&EF3c?s7v>q;F&|pOd}s-Cpu>eZ(BZ;-XglU@OPIGUVXk(#FjqTVn78kGH~%$5*7?N}&M6KT&M6KT&M&s(JZK5$K}$IIIb1mRIb1jo+Ky`si(g~V>mT8~?{MLq?r`CJZ9C5CmT*1eaN!!p60Tt^;Tpygu3;?U8pd($BwWK-!ZnPeT)0-TgliQ?xo}Nl3D+dH<9;&k?%x31^^j(5ncs=oOaIO%?(W|Jw2Qm@U4Of{yWi=zv#-sl^ZoMIiMO3^e^xuT^X*Bz+=8vQ;he=Dtx^N#rDk{WEGQHi$N%=M++qKH+=0@+)PMBHqRhLT>+CB(?KV44ZP{?k$Nz45_u@KcoU)ktNO^!+V#w3X|0q7ijBI<5or7j?o5`GRkDJqN3v_;t;Lj{+eSR(obg>R~wBr-j>l4;xJGRplw$mqUgYDQalkXS*`whCkh=a-FfcRKEK8Tye<A!)zJf4WN#p8_lTRi?41C}rbEMc5DTo@acFg7e<Y*@nBu!ON;31h<&#)c(~4STE-@{Bz`Mekp{2Xm#v9uF<&+v9hy?R<N(>ey}a?eW)%x1DcKRy($f+ryo119iF$q8IG(G~2fB2j(%S<$-?nN*h)uVpBurv^>xg{%(-<Tw;AJb^ko<^g<i`&t9rW-r7Q)mIr#LB>(fej7z4EIxP?M?-KH`I*Vd!nAB-`pc8V89Y_1Sr81}GfgV0&6{}OK)J*2IJkXDy>dWf1zVs$@S{~??PM=}NsnKH%b6Otgcb`l6@B3*vKkfoutV12`_=NU-Li@I3drV<FO<_B2$9|c@{+h!6+K%{`LflLtZnh)NmJokSh`;UVFH7i0OXx@2(eIWp9xP!z*pBgI3FFEV#+B_Dhn6rtEn$4xj`3^><J=O)x$QVEEPk9)7mgR(aZFjlG462TxVD7j+7gayOE|7A;kdSh<JuCAYfCt;#d*ed%;Rx)|7Pi~FFP@ixiM%Lo$KT7{w-5#+}*!rN{zewcW$ZnoI{;&o4-!H?R?v^+Ob`nbLjnEp!?fgZ_h>4`CP=E*8i~F=k~JP>9X8ued>H!?pgDvFi-9iwtt_!EOovt_YZgWVX+!sZYG=e==ShAP;|O3H>d3c`f*<ZYxAj}s<C;Jw!`O4(P=wwPTL9ea_8IdzjI*oDs6|)v7*y<+?=)(=(lIoXKije7($On)()SOMW^k!Ic+D<XI%9^hglerkIn<E9X^MPPTO&F+D@Q9oLR(wo?4o~=6Tu<pYuhh?YKE@C(!xda}LhW<~{cBviLbdblQ%a({=*A;?a$)&1-AlW#<vv4nL=ePTO&F+D@RaN*K=CT(-kv=N;M(KL?3U+i`Q+PM|+B_D^=sdhX`e>^w!=;pZ$jr}e4R`l8c1bX~kYcUp%!ug{&<q1(XgbEkEv(>nZI$*&o+#<r`Ab*Q5qpRiv(VP9OG)))56cEsEiVr~j?ww<;k?7L6ccb~BDw$o*WezBb{E5yVn#KgyALhB3tXgkK6DU3H$7-J3>#+bu}@n$>!JJ_t_!W51LhYQDo!-eC*b{xN!aQs@rG3#*Qn02^t{MwFr#uDZkOPE_6F3c?s7v>q;F&|pOd}s-Cpu>eZ(BZ;-XglU@OPIGUVXk(#FjqTVn73`m`Na~>FP3mlaky|!aky}Pu^s0@OE?c&!nx1k!nx1k!g<hkT!&cvI)q+F3Fm!>3+Hr)3+HRw5l2h7=5e@ionr~tIhJspV+q$emT;Y83D-H6aGhfb*Ex=BFyT7K60UO`<-+xhC0x%q%7yC|OSo>a{m9|b_H~`;N7s#Fo^Q%d4=v~W?su>4eBZO`*lqHC_t%NHo$q^AJGS$E_b<ENcD^rJ>tdc1J(O+Rtlm>S-@e$N`G7mcJjV`p<IhRzU+n9DmXcg)iSLUE{_lgv4T&&2O!I%|Qb?I>9y#p)p8D#qE6tLv{ohA?*L;UrH)W##yXhr|%}LW#=D*E7%baeHo6~Izbm8wVnA7_FoD%3_9qMSu6xM4B>#`l&X$sqE3fo{i_RHk^h5a@8{vr+*j|1Xk@%SKa7LOa^$)A(dN1QDlXT;y)@y9r^gmGdCW69yd__2iXV+rHO62^}uj2}xFKbA0lEMfdu!uYX-@nZ?&#~$;2`b-x7ZH2oRh@0deCrh?_vU6Jh?%#Xgby|lyug~3I$1BwL3iZ80eXm{r?%z;N7XBT_B<8$6_pEL32;1Wkw#OrEkB8U4`?pn-g}?Wn#GKdX?%#%Z&)w~b_uSo{c+cJKiMQ+X{t}(mq0Z}b&x(n#{a#`Fy~6f;?fSgmMW=PB^ZMNV`?y}%-}S=&t{3)qy<MM=AJJ(Y>bySptUeOrvrmZ6J|RAS&$DMd8%yu57@wol@#F4ZSEu8_&1t{8IqhFJr~T;Ww7=Y(_KTa-_`5lcvzya+x;c$opl|Iw!vD8V&Hjqb$!Xl&-RtT!Zf;KF=H@hRZqEKL#l_ioIxfz>({XY3osNssxVbrvo14?P1^Uu2`^E8pmz0y!xVgL6)%m|&3UvPW<bj^`Z|LuF8aFqmadUGTH#etobMvgfGrPxW+}xbTEzl3gbz-p^bo`7jCujeb*44eP&i*Z}i_^HdIgOi})3~`gjhma(xVbrvo14?PxjBuSo71=j`kf-NELKVH^)PdC8aH?Mx;l-Uo71?tIgOi})3~`gjhma(xVbrvo14?PxjBuSo71=j`kbW|SgbC7urNobadUUCtJAo-IgOi})3~`gjhma(xVbrvo14?PxjBuSo71?tIgMMO^M7wUeEVlPI*psVdtIHz&CO}t+?>YE&1u}+oW{+~Y24hL#?8%X+}xbT&CO}t0zL2MZ`gg)>SHHzbQ(8z_qsZbo14?PxjBuSo71?tIgOi})3~`gjhma(xVbrvo14?P1$xlq(^#z9kGh$o)3~|2*VSp<+?>YE&1u}+oW{+~Y24hL#?8%X+}xbT&CO}t+?>WO(8t6VV6l3?lxpSVG;Z$hb#)pyH>YuPa~d}{r*U(08aFqmadUGTH#etob8{LuH>Yt6bp9NJ|6AwmJnR0~#l5bcbw7KLXWh5n<5~Bo_juNQ=sliwzj=>m-B;e@S@)0kc-DR5J)U(xc#qS#@#i^#F4m!rIGe&a%+`f58Q@-57sjN+g)!-HVN5z)7?Tbc#-ziAG3jt&OgdZ`lMWZgq{D^rX*-U0Q<x94bzyD{aIdQibECtBxzXXm+~{y&ZgjXXH#%IH8yzmpjSd&)Mu!V?qr-)H(srD8OyRtotqbSq0Qb7OaE^AkaE^AkaE^AkaE^AkaE^AkaE^AkaE^AkaE^AkaE^AkaK5&kAKO{iLfN`-tr*~5R~N1o9WGoeI$XF`bhvP>=y2g$(c!|iqQix2MTZO5iVhd96&)^IH`<Qta7(yP$<~E?mH_v<x^U0paN(ZC;le$O!-abmhYR;C4j1lO94_3mI9#}Aaky~L;&9>q#dh2eTEhKuwl3T|2e{YOg?nd*3-`_r7w(-MF5EjiT)203xNz_6aN*wB;ljPM!-acihYR=7wjYk`WC_o0vUTAZPJnw|U3iA$aN!w_!-Z!!4i}!`I9zy!<8a{_j>Cm#I1U${;W%7)hU0MId5-N%zwBoT&kwV8;aOsUdtF_4mgsQdS)#**XNe9Mo+Ub5c$VmJ;aQ@?g=dKl7oH_LTzHn~aN)V4?OQvKu!QH>*}CvdJHWlJE<DqAxbRHd;leX*hYQcN9WFf6cDV3N+u_19ZHEibv>h%y({{M<eB1Usd&XPB_bJ)B@ZCy)dtF`lZpGokcPkDTzFTp)@ZE~Th3{4zE_}D*aN)ZZhYR1WI9&K{#o@yDEVdVjn`8;!foAK%_nranb#>u;Oot2KS2|qyUee*h_m2)2zGrl}@O`4gh3^d=E_^@eaN&DEhYR2L+1{tmWZ}2MvUlM-<pB4(y6_#b!-emH9WH$5>u}+_U55+b;W}LSuGZngcd`x_zI%1J@Exneh3`^@zhkj~LNDt#na8pFlMNYT*?Znglj>(zNAwlN{J%#r^owS(_bw~e_qUT>`#HDs|JAbo?VsO2oxL}Ed0DJj|9<K`Xt~(tg!#$-zwyiX*-`&~>O5$<*yfpo9sU0vwN4?ASpR<NJZQPt=EV_l?ESf&l|5qp`>FGw<zk!ojJNHme?N5|v|MZx+reY$sDD3o9<*F+6LI%tjU7k*`>FGw<zkx{XTGds#Zmu$>O5$<*d~rEU)EgZsDD3o9<*F+6Z6Q{tU1+D|9<L>|JMJT;c0JbKCzBi{!i5xJz(4F^LE5G@2Ad#F3aaWm-x8W!8Ut@{jD$Tug7g)#AW$>=Q0Ld>pbXsAGDqOSvKGpi513tY&OS{Yn=xz5112Tg=5^4&Aj1S=RwN@=0J}yr+KoOCtd42XnDY#?-Ay3Pd4WT*E$bc9&nEH2<I$MHs?XtIuBYNa8CCK=V(th=Y7{Y4_Y2@4dW56Nj%wH=eX8+(DHz5Hji)(=E>%|&b7{imIqujdxUFFkJ~k8c6A=KJcsLi&;4EJ+t<%I)c<GeWOuKTbN%~S_TTgD&bir@{~PDf?9P4nQ|JF3&v}gf_xm^JWySluf9k&PpSqv=r|wh!sq6oL>bm+quYv#7Ysi1<n(CjrR{5u{0sg6T>wo{8^<O)#@4ub@+FbE}=~>gi@f_*jct-SZJpcJOp6&b_&u#vVXEOiB^Ok?(S<1ihoaBG<Gm!tzx#^#JcJaUExx~Nm%;Dd7p73uxEBH5_1N<BJ`2WWJ`@eB-{%_oO|5NwW|Ap(5|3&xIx%b_<_uc>Ay?O5ad+z;v?*04!uKV}@3HSK9&jE6u1LQsj$bAlw`y3$mIY91nfZXQ*{~MnJ{QvV=LGJT}+~*1Z^Pf57K9|USE|L3O;{V=riT^FnE^?o5<UZfXeZG<Vd?WYyM(*>C+~*s)&o}<BKHtcF29o=nB=<SV|D3TT93xw^nOl7K*16~S+L~KGxBmUtzvrCj6YJ-e=Ukr6wTh#DZh6k-*<3@KV*T9moXfMhwl~H4x#c;RXLHZxsGnP&b9pxR!jAg6<vEvU^Nhk#Kes&R@@$?RIqK(@=Ukr6b3#Y`-13~uv$;oh)Xy!?xjefV3ePLd-12+MvwP0tsGrUAB~$n=!^|zuxjdWiuuS1QDKob`=kjd6TQr653eDW|oXfNM&es&a!!>iub1u*3yLeOhZr#i+&$&FCzmYJ7zj-io%X2Qz=5JR_;crpQ-13~uv-z7MQ}`PpUv7EM<=OnLmrwZHEnjYV&gI$s4W3W<n>t@^dCuhl--nvQ_gSX!Jy&jd4&^y~?`&rC9b#^IK)FOTl7~omsVGrMelS1DOJtId6a)(r1G)U<A@Ctm2&IL|!{EdCq!3DqgT+Zvlolf;!IJnyBae_WU>UTklLDkHSeBHA6(Qxp^2ik-CCFpoW5_*1f=NZNB9<sc9wn8)O5|}^IZ_3zf?PQgM5=++kP9Z&NiDDzmZ(6UAfaF=sR^r0!ohIlDwC=t5{yKyI*B5+!P;1&1_>c`!MY>{7DnoW^^prB5yS&}kc%R5q!HK%OGJ}8qzTxBG=$Y7&A?{J)g!T_1=s?)IPxTE4YtM-4M=0s7Hmse!J3kGU_0cRlIElX*a5jGNk<Y7#$$<=qz&l;b|IZ%Pmyk5H{_lo?MZjAJ8~UK50VHbVu?=VY0?|)O`d^uCCOkia$QLR=?nHnt_SHy27m*wL{HL-3<3v{{;(vH2BsmGMEZ~+;1J~ck#sT?9Ev4U$Urh298NOH2=W{m1CAljqBNC^0!QJK=g2rR9vqKPQpsR4795LD(#Zre37mwMGRQD81)M^jN9l`XIyfDlOeB-Z3~&aShSJ$&E;tvTyhOa@Rq$0ZhrCQ?k=Mc3$pVzlCkw%a_+$Y}mVishVwAo?mV!(1$!xNWybZpMmR=$A$O>=;Sq@u7R)Q;$TSVR@?}G0lw~V|;)`9D=#9QPY@;>-JSp!=|J^(*JZWUQgHi8?GdyjlbHiMh7#9FeRYyr2Bk6;^!5A-3ofovicXd(9@`GkB9evTzRCR@pNa69=FW|AG?4&+R-jqC(>BKHaTntTg>izPlIUy$A4Zt@N6OR@*tgWQ+oEAj*Q19D%Jz2pFR088v5-;smhL9!3_Jvjs(LhgI=BRK*dL2fTOMoxeyu*81y6Zr-Fg&c<+Ca1tt$Q>p}$*<tA$Q>hR$p!ENmiU>RBp1Pp<Q(iY`3?LHxzpqfxdL86?kxG8TnDdXiSy(VxdGlF*I<{)P4Fgim&sM~7x)))zmq#emVU?UI=M|0Nt139O_HQP$e%<7Rf$N7q)U0gJoxlaa*G(CA*m?ME9D3C<C9zDZ;}tpC*c#!HHE-JQb9=}1*F1YVJSamuENqocz;NG2(#5gQW3ltk&2^s8S=1{2d_d>8O$R^!J^W`Qbo)W#lT`xQK=S=|KebAshCt7$94&@gj8H=gyXg(SW+q>wZ<{|2>6IpQi{j%RthX7Jt8IISSk&cmP$zja6FU&%SffAF*s_<gXN{N(oh@^L12(nMjA;*lVC7dnu^ltq@pwluOR6K@|g4*d4aq}W}<X1sVq&$tD^KesU%eet4d2y`ZlR1&Bd#-^ftz5b+EcrO<ITXR|BjeRhKqnY}Ev7N;Ra<F>Y#swWONTw-^&4V2D&pI)MHT1w*9}=>+;R3=ES(r3>iUa4=j7LyyT)Bp4}$qsKHU3XGB>V0olyFdDf$=$#la2DyTWZ(XpiR7WZx)t2gk_0T(o!TMl*^v*+IEEtR4DTF>~2sXqL52Fv7fK8Aqiaux#Hb<@)`k*D)61n2&gEn9r<Vv6q+JWtmD~Uen2zEs75%fVk7>`^j^g&m!D{`d~_wHbK<jNq{&w$S$_o!4(>IL?a9!F_KDH%-0Cl#bbsR~#{dIF`DrG8*Pd{P;)9smwNt{P&U3Z^1g9kCt)4neL4Vx0+QB3Bc!9u5vit`=hbEch&PA&B*8a5QqEi1j#d9CBfZ^+a$Ya^Z;n6mSZ15s38*;0w}ZShO@1oQhmDBL5=zB64*Q#~I)ZX*#0+lH>)wh<!cqW$<OhzCJh;oQWQY1?PZsq*;<jnk~%*=SmHbn<LE!=S#1mbe{AY_!>TW6(x(nMbhgiT_`OE7vqz<=(8o@60A8+dPRB@d{b%+TOch5mm{}8dP8~}d>grj=+_nC3M|n`S}LssS4z!b%cOU~cad8ry(PT|zK2{B^!*xe4VGvsy(6sy*GW&pR!Qr@^~kM~R!bYe4ahae_}B<;#1bu}wbF;+hf-_U`_jkY$H=`eeIRWCw;<ONV`wY56-%^|Hc2LEN>9N)lD2`{ko!p5EPV=oid-9vv(LcKutZzQCv69}OC4aAv;*9MoF#oC?F4rs*A8RxEAT5U(O&vo`Ud<)>J0lr`WE~axi6$IrSHJ+kn4!?x(D2YB|1r8OFw`=NL^sNq`lx?<aSBBrTyT3<l-@=4}b@-#M9FE(of(|QUdHp=`eU0xgVu{(oygza$Pa*kAcUqL^tW6^fUOg)KfYkotDmkXQY!TJtUn1PvMi((mClocpje|l8#7c!L#_JJC2hJ;03hQLpm;90xwBPC{32GfLHKIZ|S0R6}&3-L1{nf26zLX^p$>>{sjM&Qlx9rb?G*ETlx#7x1>AZ9enZ^N)-7oykz;7B*`kM%6HJp07;ko;dMjmFWr<3xj$Y5VMNX=-<0yohD>Bl&JX5C$p9Ra1;K){E)SCO$c4Z{avCh3{E(anuR^c_^26Z6$fe@AEd~~o3(A9~!g6u2xSS3vBA1j4<5e71R4xUULT(6-?J{5)xtN?Gm5?6=AC-r~9+At*CGdI_R$2}MgOJO_@gEEZ%Vp$YQdzkISV0~ED=$}+%i>i5_Ly7=tc2Wf%n?<<Dsr$qQhHpj3Raaz!Jd$-%a7w#6;@fU3D!jJSvs?TA#xS@IjNc)3WmyKU^V1$xf))fuv&5?7>V3y%r((qv>YOjmBQp0Fh(8^i;(NcVR*&BqU3sDJ><q=K8gin<!E_=R9p6d9{G7#UAci=8!r#6zT60Ggxo~TU`@fMa;!WVb5=93ncPHv0drP!u({k!o{AZ)1=vDvF25)}DYpV!$t~nbQk>ipY$;DeX=}Ny{3Kqj<T$yZ+y-oePg~1R$?d`R_@trSSZ)Wl!za@*A9Vsd$sOgFqz-atu(RyNY}i?j$9uf|GG@bg`DwgAEziVk__W*w?_K0Mm;t-UUGd&ko{w3ttK1Fm-Q-1Rafy^5&%mpbyae-6cd)yhAg{n&(*x`wcbC^-9_b18lzYe<F-JTDJ|p*(x8nFu1QX?F<j-(y_X2y#iSk!CZhM2h<zDh09Fs|4lH6N9fa59|OqP@6GdTKEz!bT!d<@4`f3UxtEdL_?Dh&h&%9l}kMM{$|;MHILO&TEoE&V3_E&YMg8&bM_1+O&uwlqY}1T$p?M~^NK1&7M%I5G;#!@yxEDTr}A92|~ZF^tg>;0WZ((D4V3L@pR(>sjzw<f>rYi~>g?7lJYI9QYh^(dh5d;ArGx<)-pja4d37(BI?0aq<{gb9p>C9=Yb|?+M@p<XWJQCxR1^YlVJ&9(*3Tw&>+a;3VWaq7PmGUy!HB9puUKRB$SKxik18_#%2a9-IbFLoYuKz68F6UhV=;2dAT#yMi;o8R+Fs=*wB)EVP<{zI+9I1-b6%%X#2D<a(elUjtu5t|$6(5x5AsXV8~Rz$M5fqA!<$%aH4ZzI+>e8@b--%a!0t<dV>TtHIUCC8N*Qf@_iMBlnZv2j7=dQJN-i05{;1LGn5|1I&;IqcmOq5d09Iq@&L^gPV~Xiazs!KIDd>&$fZvkQ<IZ`waXHxe@5IFTgL58;L&K3GPJhS@hXA;5W#PLZ9shcO&;4`s{n~d*nu=2ls*dkQ;+O+Yj!S_rk`@2fzc!jYppy1P>xN0e$up_!Dvy(PxLiL&!ak9y|;lMs5mXeH=V4A44x5m460*MjuWEPk<-ThcAM^fWM#*r-3KIljy^jz*FEU^x<^yG<X_4IRiWko|S)<z496PJa}H7iQHNF5_n0zfYOWdW$-dSxqy=2!QbU8D7`BG0setcUO?Yp2d`u6UY5_ve}aF?b6~&8x4>J-{U%?N{|5g?ZWhMJZSXdhm@VIsi833nS7A40S-F81QEtkA$ttKSvhoVXkOpeXZF#PIM>dqXcrAcQN?zrToL4avNl}#iV1AU$!#FDd7Em;0zN{;Sz(UGGSRUmeMaQcUET8f)_%L#>VJsE}iz)?_*X4praj>|u7*<#*sT9PkIIM_L3M_@(B8=D4U}>eO@`hYYc@%t9c@tJbDW?>}>rvPvN)Q-?+!BoG$H2#w(#le~j8Xxtpu7but5j6V;8g)uUa16DLT(wxePyt+@|dz*4pypyRh4&Ok1N%cV7#iro=|FnHIaK8$3`u%mQq<+Ay-jC!BFL0ST!YFse)H1tcDT^Mk2Qo$4?X(rPNYZ$stM%7^AF_Yb*5?k5U`2x=M%=rql!L;nVs`1EnF@5TAr85lS2whfh}HcxwbUQlgai<Y=V{*hKjNr5oht%38b{DeL9NN(-=svJs^p%59Vlcr{lx$xkY6!M4gra!aMP(ot!NS9|42rJd3V?1WF-qofPiMR^*f@k&>)D?a%U$87?bptMmwmY-6(gWZ)au+B<P<te<n!@4PnU?OsxacuVndn*abR=J0g1STma>=~tx(gUv~STCg?*bg}$j{p8(f2Fr#$;rw9aDeg&tgkXiNycjcEJaBJ(~#SSIbsMnMCq@5Di2iB!F1(wSgMk#48$uPHdq-34nyuUI<tTylp)G?IYSu<j#PHQhAN|!47^6dhAX4N(a3#)xn?XlRvDpuDL<=>1IH;}!JbnlD9_?G4mL)49(*3TotTd%gOio9%GdIEWePY&*#(=ZOjX9?H3c?FnFdZn?i<Wm)4}P=WaV4=1!V>}L-`K&qVlrx0$wv<FDbLYS;+0iyfz1%qfA%!$X?|Y@D=3;*i7YB#f#S~u-VFda6WS1V<vnZd|jEN?8V%-5L~FdrtHVuw+LLMEL09)?t24#Ls_I8#N4+ST&%pI{Dir03AjXAtQ^8jxD;HfEKv^2Zz{{d<;qg!M|rNY3|yuhLFrq{3gu0_mMe3WdCJ@1+xYY?<sD@exC)=lQx+&I!Ik*r80M_^!1t8Z%2D}UWevDS`5Ck78f7is*D5D4tFBen;eDO*3ue`I%KLbKUpa|c^?hYM-q$OqFsrUtKEV42%4y81A1E8}zCk&QnRJ7)5$_w7OPD=3Dx2`WN%<XXy)J*K9LMWD<vM1<kHC+V4>7}O%E#cx%14;J3MiYw%_u2=xn>Kv1-YV_N4A1nkt>Zk!Uy`0dkn|F37W`N#<6XI7IL+4d~O4`A?LwS{5kl!@+nFiDciyA_@s^!tLy-GD9upXT=@$83ZFDpzEC=V9h6omZKLc0cj1$c$~Vexa5s+5HaM=n1HZ#32{>l<fP0YZjpN~a@O$L?W32xG{(#&NjN>1{ACVh@F}fGri`-a@zkT37<R)Wm?FaWGHyz{V0C)hoIm+wGPvB3;y@qjf2t1@5ge_7IgNKn@gmH5OJc8UC7&k}3qsT4BxH$$MLv9Ji&2jKJa!WB*eg=O=ZaK!s3Gf7RD==Dq0e?YmHTvl^cv?B7ysMm4eg%KUXjucE0ncExtOd`4XE9pVf#<+;7%lIE=fU$BE$hJx;027955SAyMU0jW;3e=9MhnJ@@*DUYM$3B`6TgGMW6d98Ok4-ABli);#7*!favx(%{0;t%+-8gkqHf0PZ`f8vQMcel)U6m3I;g9P>cg1G3+7dI)x?-602Wa5suspUVX&}TK;4GEe;9mNEv$Z`e5Mowi>W(N`jt{r-HzA8>X%AU^;_jj<y+-zl<rbWt6$+&Qr(5VFAJ7cORL|Z?}NY~wXC`aeP02rpa!Ymqwk*ppHM5PKcMfcfK}8d)F09J)xqj&6?HHAz7|+Zt*-7v--m%=YAtm?`aTkjRKwH*7zwq(+G?bF5Pe?<tfR)LhtT(R!MbW4^)ULr9#~JUs~$n$*9YsX_0*&2`&ckmt*;(K-+Mrh8mk^h-^YP*sz?19ecu3VpvI{uFcKPq4b=wfDfCBEu&LTaJ*hNSn}N;LUoje*sm<};Ts?!)&|GbS_ZI3|jD{BKlX!npJ%`coq}meiE!FcF4K3AHcyFa%z-VZtw#IvF^&&<?YqbsD+o+c?8rrCB@!nSb4P&CM+8*!i)u+_UN;|b9*ipTzJcZJDl*Ox^)OKoTwF}q<pLRk?0+^t7MQJy+2iOCjoW>aH3HDT*s#lZ_Y9g4Z{sDVh?X7meD-qURO$L*Z`yJz~57<ZTsa{i_QTu`Y)IVXp)c)!-c=dxNsRO}*$X&-+90U$h`=~dRzG@nnrv3#>QHQ8~@k)aYP&2>`<Zfd0W`ddOAoZ4#styB(sdr$5)e&kcUc+GN>a*ap$o-8GJ_;PAW~#T9q3URGv?{AZ)#2(`a4brOt0UF%;CSQ+#{C3v0+y20=hWxH=T!|hMx6{!MsAEcPJID<0XYT7##C@BmQdA+>NIegng=#XoeoY%Zjw4h^@3jHbR0h~gD+zVLw!-51<q3Q!(LM7fOC+0Nu8n21?M7{7suGE;Hy|7pE^^W56)K$!Dg$kfv+JqTYW`c2rfjf0FJ{&;36zhP@ShP1{bSE)FtY2^=<HN^-Yv6P?v$r@X2!Z9d#wR5}zzkUsqRvEAUBS9Ji~$RcPrU^$m43xLPfN(vs?0a4kM5uD+|T1J|jKptQ8Q5!{GRN~!Owo4`$K8Fjt7LEQpwQ9nlMN9tB^D?a%cCELJls)bTh{RI33pOnV&{~7ohT6$FdQ2iYITrCIlsb7F!Am>v*RlfwkM6N96h_Aq}uta%vyZSZwwfY!rhq?>gh1?Exr@9;5ja(4skv-rZED@}Jqka#5uRad@R{atD5xH;G@6>(ZKIAH3t~mf6z!DYJAJl{3LA4TWuX+ePgxp?rzj_2bg4`3BkB))Iuta6`C-pdZT&)T_teyZ*Aa__js-6T-B3A`-)@krGmZ+xwto{oAs@8!0qMilMBKM1WN<9yrN3J^NwTs|IEKyTEqh10psUfg)>SgdUa_7_w>Q(S6a<wq`T?4OSiBR=7^$+k5H5_(Dy#d}p?uz=mdK0{fTo~rZzreq+M1*=>{TuvSje`BD-U06*_osSGm9#(cx`W!aRaJ|`>o3fvbyQ7@!AsHVU=GzmUDLF>m_rTF&~&XH=FmJ~9?j6|V-C#==GF3Ov6w^if%&w&ng?@eelWk5Pm9AGS^zAd<<}ah4b_5RL9Kw+P%WfA1U{q{)S}hfYGJUj)(E9Vw4z!eydKhSt3-Pkd{`@t(qdW(umnCKnyeKEi{sNKnAb{yrL;%1#%f8eG+0_|hIzWQRtE27wC0$n%V>|{{ZXw2=IKYZvUo46J&Ad`tX2;1<+PTVr^{*O@m^kQg?YNX7KHa8tu^N9Anh@{Kc=<8JpGs!jQ3!zE#~Q9tpeUFXzej0SI{2E`{P<XX5q)Rig>T6C1A^Xs!wQ5@hYYD#QazZtfW1m^}*a%8LX^T(gtB(s{&ThDr=dTv#NqswJO>u%tzJ0YFbro0_K|PV0EpUHWl+o4X}n*U3(dGL`|@!RzrIg$9XNVmR3`H8?!+;7_NnCi*TGrfDu|PZK?W}8U;paYf!pYt*x!XD?)oujnp=)@2Q*B4^X;Mt*5QUtG2d9t*ga?vD!A2ex`b~jd<15KEtsW2gYe0?JFEt4ZsFkoVEwYOhd4t)<8Re<Dn7QNNcDa!&q+&Hr5(xr!kJ3fK9Z<+C_}freIU8iFOSmwi(z=Yl@MmYAwJPS~HA9O?wi2Qfm&=wU%H@<aCU`R$wdS42-|lU~A;^VEnZK+aQ-0<F75)7P)*Fe@}r=A(tQHuN~M9xdIq}?ZNiQ6~vh90Cqs`A&j$*U`OPNV$^j4J0bT7`mzhyMT^%;YMr$NFae|PX|0>q6YQyVM=n8o27Cr1usce6gT1vx<et%zz$A>uM3nRe`)bL^C29S@ei)g_C>a0_&{B}=rws%LVw9$!Bn?c{1|c_48w?J{h#iEI3@}3*g4|#&6U@Zu9fFeK;Bajya+%r)a0Ev3P?U@UM`<IG8=*Z1K8H~~5+!57vD#?lp3}yG<1oTUqhumDQ5%okIPH1xd5re)D47CI(Iz4Hy!Hb40!IEMluQGsX;TrYC$yKqmk_P4+6?Vw@MWzB(#zT`aF*5!X_htzoTK$YnxoAH=W6|t=4$i6d0HycJZ%BEKubqjpuG;ht_?$aU0Vb$(w;?Hq%8&)Yh#cWYfHhU+61Jf+A?sNHW_J|_7?b-_9C{dlJ++EHnwiM_Kvm+T%~!DR%xrj)!Iy?)!G_xjW!!;jkXS4r@ex-PFoMI*Iq?huWbM~X!DUaXq&)I+G|Lgw2#1#w1r3?X`8{#+8aolwXNV*Z3)s=%>+&DO(av>25!@qW6LUQpMalW>sDx=Y1_f=+DfGD+757s_Ab&6Z6~->dk<-+_BHsmwifAYZ5Oypdmm|+wj127eSoxE+XL>=HX`lOegJ>aK1BLK+Y9d1K1SNB?FaX3Tafl^2f>4y59y$G2t1@&*s?0xVel}v?o;ikb{sseeU5ZoI{}{1zCb#modi#6Um~5<PJ^eluaHh_XTUSsH%Mo+bKp7cTcmT^1@MCQ9nuBu5_n1b9_f;H8N96hh;&)I3SQOrAzjt3f!DMHNY}LM;C1aMY*|(926zKocSO6X{RRG|9Ygv{yA9sfenz^j5&dVpe$jpbWxUJ!DeV-f;$78$)qVwayzBZ|?JSrF?|Jm|+IcV^-t*}fwToZ@ycf`a(|!XB;k}T4MY{q%g!hN^-?iVthw=Wf{s*?KnpRY=iq{S8Pp!CKQvXvcso&CWfu-<XO8;B?8!UtOGWs3u4p<iNWpxRutX>{0uPaF9^~b=+bWDC=1+ao{AXU&Sf)(|=NEP);U?n|2QYF0#SVb?0R7I}_R?`b3Rnu#LHS{8SHJnRof;IJ`dNDmj4+F#W5=dcs1Q?+|f)t@gfl+#Cq$oWGjL{!OiqY$Ub@Xybb@X~*Jv|7io*oOv>cL2{dK?(1KaLcqHv}8%Parka8-tDY%1Dj%reIUODpFIuIoMpUu2;votp(UZuc_D4Tk5UB)_N#XYrQSlRu4yNtG5H&>5)k7^bTMLJsPQl-U;la*GB53$Aj^DU8H!u3)n@kkJLr)26oduNZs`AV0XO%Qg^*4*i&zW)KgCc6ZIxYiF$9ax86*zfpcvVn54JRpVa&4{lI>DE2MsUf3Uya2C2V35FDsKg)~r41yl9*NU8c@aIoGHX|SFSrt6)N()CO*Q-2yMQy&Hn)4L)K(?@_K^aP|4`m^A(dJm*$_2<Cn^k<Ns)5m~g^j>;RobShiWA!9GSs$-Y1Sjf!ktXVsz)5-v(j<KfI7J_TG)12ZPSpn?P1UD?)ATf?Y5H_<x;_MHy6y$NdIpkLp9#*?ha%0?XM?l#;YhRfSHM^Fkw~xTuY#}YqmW+J=Y#Y0(RwXhb1VQC=wtP9`fK_^aG^c{X`%iG_=f&G(i{2`aEU${X^H+O_@@2>(wq8naJl{>(sKQ6@NNAiq__2Vz<2Z+Nbl&Yz*YLoNUQYK;A(vq(rSGTxJI9Yv_@YCuG8o0AzGOB0r-I)qs>Lh29#~k=jjo+2HFH}(iiBj>mTYLgCFaQkUrM8fLrv%NLzFt=+l=X`E(1k^kqnv{t5Vr{ua_F`e)#0`U<4a^zGnweI?R%eFwNhe-~+oz7yQ3zlXF_{~G*SUyJm$z6;!?zpqDY>-G9tv{qlMqrH!k-6-3wZ`5n!nrsiaN8hA>q<^pf2>z&VM*30T2kz6iBJI-;fCqFF>45$d_>;a3=_ma#cv$}w>9BqjJgR?=bW}eM9@oD>I<B7pPv~DFozPE$C-tw8PU@$@)A~0^r}Z=78U0(NGx|C3oc^6&57&qnzzg~w{RjP`{u}t4z8C2?{R((R-;Z=f{~i2YKZx|Z{s;JnehBFg{RVhLKZ0~azX{&dk0IUE{{sKge@6OCzYX5je?hvf6XO@WPU)vW8Sk?3tNtsf;$1b)>SsY6@49hb_u!f}kKw`Vf__QQYveaB>G_Sz`em>n-U}L6^{ZfEycagE>DRy_crRjH*RO*`@m|#UQ~whzj`!lmE&Uc)67MCAzxBVtQg|<A+|loVW$<3ckdVq4Wx=wBf>hQh50*D@0Si6`K4ut39Il}&fEA29Mn2<l;|cHyqX5zqMrE+FQ3$EBQ5CFeJcLx$s18;)9!9Ee)C6l9#gJ+mAz+A60x84@1H+6*kiv`zFv2K}6k$YxQO2W4QAP|HW0XURG3tPIj3A^sMm?~e5o|QTHGM1?Yg8~Q8Xlto*ubcS)WB#2HZrOpH8PrjO^j+tO^jw>GouDlGouCA!l;GR!e|M$G(wSD8m+<BMmSPyqb=Chh(u~@v;*52(Mau#4qykPHc|(p6WGb9i`2=82jh+UMnl|VbOE~<u|}NH)kpvnjD|=FMh~!u(HN<R@eKHk(G=+!qZioAXpYp&NCK0LCy|njK42fC6;dCgAK1@mgVfLH5B4{nLh5e}1P2=Jkp>#6V5-p(Db*MZ4mLU?4K~ujbmM8G5$<_1!Azrz(ajiY3<rlB-I0bHBf*hIPo$B?C~%aKh&0L=4URT?BaJr3f@6(jq_M_$aJ<nMX}mEJoM@yVO*AHflZ*jKlZ+|g6k`z56k{ql)ks5{YD@#C8AFh!8Pmb(MuyQC_h4SoYh)V3jF*jB;4EVV(kx>RILCMvX^t@$oNGLXG}o91&NId!%`+B&3yg6{3yjyn*Nq8CuN#ZNMaJ_;i;TtKVq-GWVq+<|)OZ1Dsj&=PX1s{B%y<iY%XkUtEn@|^!kA$+!9C$haHZijW*V!E)!=GlHqvTi4Y<a51!;}34qRuvinPvH53V=nBds?!fE$e0kTw{bz)i+Nq)o<0;77(ANFN!S!Og}Jq|L@waI5hq(pJL+O=CHdX>0?x8E+$PGd=}BHQq6r;vV&L@N;9O@vgDm*a7Y^-b319>;!ijYms&uUxQy8?<0L}>;iWgA0X{Ac7wZ(jYzwVJ>VYWL!>>%58w~R$4EaId%?ZN7Not#esI6xL)vc~1P>Y((m~@8c*yt!>5y>*JYsxiG{ar=aqzhDxzQZ=%qPGT#xdgy<7eX+@E7At<4N2<p9D`DCy@KaI0c?EzA{?kUivh6+Bk{aDdSi0SK}L_74ECgfM<-;$o*=Z1<xAa8m)1UeGWWloI&oaaUMKxd}p-5{q_a$f^iPH^TtK+qVc`a7Wdwlz)Qvj<SrV&fxj6)8c*Rq{4#jixP;tq#uf02vCn9Sd-AK`RpT;pSB&4m-;D!Cd)%L21FsoZk^9~F1N_7I$>@N4_3Pku;~H{*7&pKh#$lr)?&ALh|1_>6cf+^|-ZYLH;o<8&_4DnE?bAn(D^lb;+c&RV$NWUUYo3s1-!eZn;j$;+BdeJY8gRsuc==1_Q`YYFRPionUcUAYk5*|L^BP}m@stdGjX7P<f<haZH*UPl6I*Qtb92KRo^pr%%hsPV-P3W<Xyz44%<w$=<80==E)DUNso9lz*+!#1<)@8d-s5O%Pk4AZ^MTR5Jw=MNW1jq6El)zFyv$pSYU7Dhf|$SDvZQC+q>o~$PfGE4N(|Z0eBVaR)4qIN<`o)8c_Q0(Wu95$k64uZgmND*M>{^D9UpH8>otY-ntZ+3PE*)UlW!;X%M|v@<oks<m_i&(9tXtD6yj#`xFOD_5NDIe8U11k{bKTdK|h*8KbpKB(eI|v?<Vhev}+3E#P&-UFWO^f*@^Sa&%S=a^Wn}@%$Hu<<vH#<#Jo=Tb)ItPcQNnO=@rlI8C#hTTQ|%z<LV0LW8QD(c{p<>^F^b|c`jW{W&ZJm>#-G&MloL-ZN;uixX${hU7mTdkBlA3ym5=M)P3Ah$H(hnS(7h|Hcj3p)@AZ_VH-@o4cIo5ZyUDR<lBsWG5Nk=A5FfG*mslfJ7QwThrYNMh|`!~*m%a1XOF~uYn?AVTRY!i`_=r?a?jE)f6a>LWY6KaADIv7*xqxeh>!VeL(6*REPa!?uhtP(kNT<tFURKH+?x5gwH0E69?#GGhiS9wkBNVY#ph1-+4bN)?x<t(I#|}^%c4z_w~2L`d|lWElWzmI&E(sLZ8rHfV_!_ZFW5(m?<4lz;`@$RSkCyw)3Ufuor>G;k5#;f)^Ap*81u`!PiDm}-b345ANvsVePhk67{+_(dRtx3%gQ^CUyv0~+U8`>><<2A>6r4zHr_+Gf9sX=%m-bskrn5758cNhA>T7k8*(bvAM<z*jYEm=HZUKvdrVgR<2^K1bbL@B+;wSve_zCVXgn{@O=3Q=cG6aVzr=fJ%+Jj)&3xDMWqtlWiucfdNxSqKb9GEtpTEECavv}E_nqC2$=mVwqrF~}uh-wF_I8?lJN^A@@0ZE<%iq^_984Yuf4|#tGkM(nW5ABH#pCQB4|cy;ykGod!|q3m_oIKD*!^zte)o?Vdz{$bxbfrmm>GX4nEAD{$2~n)m1BP8vrV2lpO$3ayQtUGsbL}J^jy)Vz0ADdg1nv+ZT#b8#r2u7^Y47YoJ^chpU$DwzZrdN>-XuSm@hf?qHkm2s?0yF^ocKV$|}}hKde1L-NzkuOkM}entWNbY4SF)E|aed+hFo-z_wX@+px_R-)8KK#rFmKXz_i-zFU0X5feK;IPci;*}O88`3?05=KmVZ3+7vkb3{evLzYj(d87<;dR~pK=8x5mXLrVS9P~Ha-$~c6)h|=?AoE)bZfx~mKg4?`bb8B|P-!ajB2EAFjhj@P`ODi&o9)YQX7TAzqy}{#choU?9V~0|W&P(Gf16mB$=8K#F!?rM+bq6q*k+4wGxo*e`+|M6_&#FaExzxl=ZMdH&6Y3^4sK{WjTLoT|JsN+=6{tt$l^wwwz={7y38xJUBO~VoyD-5zs=jJgIPSO(``FYzA|%+Ulv>Hbo*<nrJ0-7cot{sbRSPN$;--X9F5*eV@{pMVPV2~=CK!Fr?FyAV-+0y3G**c>NK9rX*}D!GKcxLJ>fLw%xTP9-fHe|XJkj#N7QM*G~Tq6dA%q5vHlXueY~9ZozRZS+oAm^tk>l0rF|-Fr^&aI_OGyCCf_gG*FqdD9tYa*LfkAKH#!D{I9oi<bUX<CV)1^VV?*dii}xcPCqlnlyx-}V5ypw_I412e6Vj|L^E)wnaZS~NdBZu2aoyE`d8yf5aBUXJ9M=f3<qrGD%z@Is)PMBHqRhLT>+CB(?KbO|EgNq6=ruX@-HYp(amr%mBjo{Ri6Kuj|D*U6GqUYL)?c%?&7|(*jyfi<gJn&=EWLi?ZDL&}Ul+E);@g02v-q}Qn=QW0*cXfM3-;0C`-pwF_`V}1c6<nV#*R<_;ysuv9rkz%_IR3k_XG1hSFf~T9<iyRC*kh~S;x!z*g_lq$6)oyTU$CMm1CZ9$@G1fkcauA*cv7w$5<TpcS|+Hhpb{=s?<#L_^H0kTVHz9taSPei;vM`4Rs%P)G>J-ENk**(Wc4U#JViLE^LFvw*lK`@omF4TYQ_bFBaby?4!l^5&LfOeMd|j@xir_$A2xIYCDY;by|PfiGj?GLAzMosM9t-+}Vfu@NzR*45`!g9`_|Mf9j`dES}Wqwv{{YuY>il*ixt4e|tuK=9><N_-LG|(|w$AwKDUC5&38wnA12soLR)b4NDVP{HfDeW!(#S2Irs2`hq%*XT_r%nO|G`F6$TSH0G-khBIHb!(x5J_7VN^$k;!bKX>zM)?Y%okC)TF6WTF(JG38#^_qOWv`>ZYH2HSY{uTDi;`>GWT8M+i<3Rgeh?~XZM#q2<XN$*~jt8M%EZ#44YzX~m@qVP^MCf;m_d6Xk!Z@-0$l=lUm^r#`6!Uyjc6ySchcchld#dN#7yC0GaHp8(*uidDW8h-_i+x)#Pp-7Y_r-*8=HrG$m>s5-W?o2{Y#urMH|wLTzpgY(w*G|qcg=U0byFrXzqRDBIcb{8{I|JhshiwU$K-XetjU)}n<j4)>$3Q|uniX925g(fw+-8D@omPwSbSfwj~3rY?7PMH9Wk-vgX>W{J_X_?`S)wdc3gjsXa4Sr@wi4E!MtFzzhaku*^fE>;f%v^otO_ge#UpFNG$WD_j;IfmR4YX@q>kC*8QDl`1a4tyqmvaaaeuqgc<bsH0JF`-89F<7hwK=Db<3T+)>Bmb+D|-m(99AVr^nw7GD>(!Q$J1ZL|2cVVf<!&Da-<?+f<P;`@kwxA?vzCU$)OXa9diay{2`J=b$R*K<ABb3NB{J=b$R*K<ABbN#>X5>ePM!OBPq(Ljx;NE$IfgXl=~H(_<W@*vS)hs}dmKBWAlAp70e0!Rf(VX!bMgjARm0gKRIU<8YTMajcRMM-h6I4OoyoRnn0AzOkxLQ0V`>^EdfBb8yl9b1+>id2@A2g{RkNae|6;A12R=`m6PtU!X1Dv*lo_hcVOs>psvwi0;)sS>FIRw0#<s*q}6HBuF+8mR%+Ak~p-kXr1wWose|AtV$GMGO=$3=BgIG%y?tM+^)w0*pWm@`90IB%!}K8A+nRD8!&37!5`v28F>GFa|Lw0@em=BL+pmI$#~dpg33;tcysLBK1gpus&i?28;z`5reXz2lOBY<-s^G4l#HPYydVu3@U&P!G?%IMX(Xr2r;MxHU=9b235c&U=zfk8rT$UiWt-Yn}N*`i4fA9v;bQm2BF}S;FE|!7}yeQi5P@~t-w}@K?K+uY>gO1f^EPyh(Q$C7Ho?cM1xO(Pay^|U^}oKVo)1w54J}P>VO@<4v0iO(vfrmJ0S-3!Omc3#2^-o2jdX~5BN0rG-413b^*H}1`WWjU{}PTA=nM<h8Q#g6Tk$-pfT7T?2Z^T0egTw5QC;*Pp~H<@eE01zq#9+^g`-QlEGw>gp^GBf_+IJq`o8tOd<V{Qpf=IJG}jo2C(1X9Yh8q4I*h^8c9V;BSXL;WH8bYk^yFrbfgS2l>H`eCel#$TfD=`FfxLSB%{Dl<XNOqWHdOMJcl%zj0MM%F-T+C@A8f(<JhnCP6Q{C2}l#kB=-Bf&m&D@zsoy?Oh%eQrh-$+3rJJRG?4x>?~CAc_Pf0=Ax$S<_6xl;5QUe?OmHS*&>Nfu&O!{5!P($!#Go%Y2b_Z#q=2u0uOJ2kz`5XD#9$EkD)=g5kOs~J=OG3|!1>^O#2^D)04_ibhJvqwuOSj6$?IexxDYWI1ug;?AqJztH^4U#gR$UZa4}*q9$W%0K@28>OTndx!6fia@J+;E3b+hhh8Ro*mxId@gK6Mf;9H2nbntEPZA9W_vVyz=zJnOd1XqG95rbLaDsUBIFdKXqd>1j81Fi;FBL=U4?}6_j26MqR;2Ol>Rd6l17BQFyt^?O02J^x9!S@k^1>kycJtFZs`G9NyHy{QJ!HwWX#9$G)3EYGjya9d)eux+>20sEnLJXFGAA=tw21~)s;AX_&O>hgi1u<9#ZUwg@2FpPo=tB(N0!`3FBrLLxd<uR_K0*4Fe9nIR_%o!>$rtR`jJG4vUozf~*A685OU66!+KKcP`3C%ke2w%C`Ih|-@-C!r$#?9Rjdvr_Up3y1*B&JLtHyiq`T^-jvJc!x_LBYN0QrgivhhJA`m4qV@j8S=f7SR9UPq9QlH=fUat!G>Il+Dt`DdgP<Rtr*<6n^IFC71Z*C{0W3&*GM`W5L6IR~C2XOYg43+(ri&m&zRm)I{JUqlpsBbUL;h{31e74QmT@Hu!Dyowln0sapDju?CiUIVWo248`HfPWwc-+<S_>xjX(;0^EwV(=aKC-^5~@I81Fy!rpMcWym#7hxEmcUiUq3)pJW#1<+@0SRp=5~U4pS44`4E$2fypK4F^WKZ<;5qjk(@y4sY>qqdy7}GSy7-KwJTT20d&+PvHoiE@Woy>3EY-T3qX_JPh5AUGC*Ki%Kqr^Avx!ZsnXz(rEgqvva9o&LjXz&m^d&qo*3eJqx?0Zx&ORy&F2UJK{5o?kChzdoPWKG&nsF1W`)?)h^6^bpznzCO|A!R#Qci3;J@RF6-@2<rDK!p-3Wi7QoQK8hzSj+4$R4B7FYuf%sg|wBkmfK@gP`BX6uEPF7g$k==t+XeopdQXo+{^Y971YD|soQD)qQXww#k$L$p@O;vKXb3xIx46`@N>7@Hc&wwf;U{1ZK8rY1aG?6Yzr0CA$ZHZZu}$fI|MtXeyKySF%t}R2u?7I7;o4fxCb?oa4+188pW_0R_n(TVGXQ7jeYi})xkQeWz<<cthcuq_0|9zY(JyH_Y!WhMn;o0`%c1dGn%ahs&BJ;2p@#%)vUh3tx)}$)hoCSsweXy-xc@}^BqRJy$jWc`915fBT&7U)d#o}cKY7GotA+a-|shLS(vq>jI4FRF8hGd<@+vo+lP#9>w!J?5u?X?VXqxy^!gsmefBY<&-!7%eZuIs<M6nBiV7!e01lu*9UO#%XiyJ_;1C)#z+pIy22F4Tj-Wv^9EGE3&;rNc7#bXe<8T}eTHyqoK!Y|o2`AB@9iD_IQKG}9Y#L6Z!4WtEXMEq|8JmT(Xpn((a1IT!a30R1K^I(r3uw>{7vUlr^uQ&!ga*BE87`wiA6$VeXwVN&!BZ%4!alRp@H83>z%%d+8Vtg-@GKe(!E^8&8Vtkp@H`rfz*V@42BYu-ynqH{@FKj32IKG&yo3f5@G`uN29xj#yn+%__PJe!SJ7Y^UW3=rU<O`?*U?}W-hemIU=H4dH_>1ouE8}lSb(?SEi_n!x8ZFxSb}%p9W+>mci~+$Sb_K8J(N(czG<p5&ef|{em-B{_qDzY(dWu;MYXa<%H9WObHUkMbXM7K)rIVLoCD9_bKl?dqF(j+@L+$O6%RAg+OJysqgvlEh1qHC=l2umbyX{ut6E=&>cZFJ|6e|;xzlHQgR{BdY%V&hOsVQZrZmo%>K=WrdtTJP`rK)-KhB_r*~|RbGUoS3wSF!k%w%f+u}5oh4p6o7eyY*U*Z!R)KG)f(R;FI}1ZQ)>*<5s1SvA##tXiB~EBqPxd!kx7W#!p|{c*M}%yemgKJWKMTq|!FX1%muS;;70q*^&5)n8RV@O56#Fa6o5R#r~;1ZQ)>*<5s185q@t3{0Gd(LMTH_e8bwN6N_r`{T?^m=!7f-ShjSTG@~=L$d8-Y}ecM|Lc$GrKF_yg_14>Q{E+$2bPF^ury42pRA(rc9Q%bxnJ_a%Dwkh1*^R0BhPC$Qx2HCu2*BftJ=SUBtLAQtA(}R=aI`L&#T6JT#c~NdpmmdsDUY`OFq_q?`0kEKF$HAye_?T)WU4@?v>t0YIm*Pr8*1`dmlzG9d$7EO49o-3$xx=k*9Q&+37O=b)yWk+dD^k6RF2_x&Ht)1M}e', 'classical-complete-voussoir-arch-01': 'c-rlK33L?2_WrFBH$-p)Tu?&91%)tMCKE7S?8q*=vc-^0$UsP7G6^8ED(;FXi>xXlE-XP&;i0Kg76n8=abKQ_3*x@Kr=mXJ?{=p%+)1V;J@Dt9|2xl|L++R2yWhQ4U0q$>)l)O7a6lIh0Feg)QceTt-oH=p$*DOdCBaB)o5`u8f<?h_PNX=T+9tI}LAbc6xFls1x}<a{3>M`D!ztZb_em-9rFqkQ8L2H(%YxyOP;n8GJ!!7gDJ@e=a#0|)jmt(QscnW%PA$qAi)E?(t^aG8T2!28{fB$_l;MZ}nw%P(7zyW;m|5f&j~!QB6fBBlhl>kM*FHtT6tl1}7%@RnBve#dTw0P6DF}rl!C+CVGW@HgI229^P8?TU63k1<3Fj81ghNH6S|YzRY!;2q89TD1WlBjTIBp#N8NwJPk&=|0qP&!m;o_XUl*oioQ40Q7uq2XGm{NkFOUycr4VDyGRkG{RF&ck>9e$7<y*&m+53E2zs4y=a#D*E_!a5$VnbpwQp*)nyEyO=UxjBWcs%jRkMJqG=RxUR-Rz4nsNOoQ*9L$YWwsfm&uoyFpgmSaXLM5d+h1tbLg_Ba-M8c)PmZ`<z(5O&Rc3w`TbS$z9@bBwT0xJ|ODhn1CkHZGUmJJ8<+G2%^4>xOms3?Rcw*DzOk(41>E{qtqj(@h<_~D#f>@2C1ho$D^<&2Aj%7VjE+oa^@6qW>ArVOh*dL<!jqfv3oi^JL0L67~<Nx2v<J1<yN94d*`3l?F8tfFD59k1!wvvdDpsb+aej+wb7<Mss1l1M=~n3HFf_{iVcV=-K%f0u4ockWc_UKR>Y$S%y8gq0#uhgxBWPcaX?eY~;rb+j8P_CVv29h(yghC}FL_29hX(vgM1{-L~JUe)2K>iZGw&)HYy6b5^Sus@l9VVjN{8SWLtwk{0i_A4$ORe&dq)k{X^lwioh;&2yiY4cnh>Pkz`$TWWfUa#Bb&&*73iAC<pB3GuzpYHZ%V3E(2?lOPe?o1CBXSQ^kN!l^0)UYdutHMRg(gJ}>wRC@`FAzxgPBA-jZ8aL46CT^Xq@XY-oMd%;ek)H`!0Yq*(_Nmp$-C09veu8s8}PXU>47BblUeEN@q0Xem(QC~OMQA3ha)-R>`uYpxbDTFqDYeU@pybz^Z8uf%ye&hx(Ac@xGKv69=AK-clrHT=Jr?C(Vw1<$IO-KO{PX(OD;3R?@kZ6eI7?gs7G*;)!o_`<#n@0yd*2;&!{{met#g->vEa>&R=<)+?lQnuP@;DnupHrotd5tx7+W{^d-~rDt$B4Jzlrp6Yx#3PAnXBV=o`I47*sXaA<7E9E~d7aw3s%Xk=+5XjSd1KK;85=+>vVl|=78{d%?UncBvUCwZtSFO+L?JcrL_B$-XCQ}7;E@KJ?ys^Ctf;6JR8K@|d2!IMZKlhndRCERYR;hkb#WOH)y|4NF(l`S)}G(SHW9)#nc)f&;O?SM(+u%Xl49=};wiswKZkIzbJqItPatJeKmdeSm|9{j=H?aj#W2hz>X;jQd1E*}<nGu(djScc3CVJml<r}9W=xV?eQj10Rk#SCJ;maXDSM6A?O2X*e~wJxx<3T_8gNaXK{=kJaB`&@_p`*&>LvwgoB3f@{W@Oln6VvRQNrkQ7w-|fOd*YCl>&m0Q9E;<qhGHYu_PrB7`al8`M+~*+gME>cCTMozU+FH(^I0JuXEiH$g&xa$FJK*+Y_<TpuaOoKV%OTU1o{2}{NLn$&K^+qL2NJhpz+Y=CX4Y~X-J}(LmFHV}hAV&<Uc923tyrU3ys?u3PdaVJ8WJw6+2Xh)JZ)VLvQ8-AuBH2VYBn6^bXbCphSo?pa#AGN6Q`RIobP*ZoU1J9lb>(h9U%c{2%}8s^=0}!hx2jZTv_7OKj5zBo{m??Sa)xt@EPWrNB#XclqQjW4gbva>hTl#TfwM19u}|PdHw;ft6F?FP6T~Pv|kMY94A~!w17Lq6R2?j-N_t+bYHa$yl$T_nJ!dQz?&IJq7D4MYBlis(>;OeHHe-N_Q^m5@Y0*%$N57_U=BcsZoQ%ITMwz#P0kgI7A`a>&d<+}iwQ?kOgJ&v<g5!9M18BU$%%&vhx$swiNPi(<JJeGzE#-d#KVL`eI?<<V3Sk#tu0aCDr|D%VZx!ll5k?M$pQE%>RW|PPCQIF)K?Nt3~uxAa<xYNWcljwkd1k2+x~A7V#1d?O!!*7pzMD2<8I#0)TDT;ajmLT@|&oR35WVh!im8@_PSeL`f?*nlj0@cbXRY8Ii&_B9O^3xCkBV#yh)|qdV%Gu!*?&uQl%SDONa?y>M-GJ@$*F!)Co^tWNA|T;h|RQ$}J6RV8Wrkl5k@1AH^AJ%Ew;Im*R@wK;5yaX$?#`)K?Nt4Bp-KY&GoGfaR;hzcqhT&VvgRV#1d?O!!)S)68$>h+bD%niRjd{t=nK@}e4;aHy{&oEVH8gXkMX-yr%1(Km>`LG%rxAH`T-LE11b#`+qh4dY_MmpV-NT8w=_kp3e`{}H7B2-1H9=|6(>A3^$06k{J2r2h-j{{`v)g7kku`oAFkUy%ME#dtmna*oHvcs>epj>pA>FLjvkwHU`JLB=;h#y3I6H$lcXLB=;h#y3I6w<yLjR*>;oknvfN@mY}ZS&;ErknvfN@i~g|dLhU)C@#k9g&^0UxR~&z4iml><26)}Yiq3-udPX8;wznC;_C=|z3b7wBUX&7FerXySI@YZaHy{&oEU88M&>qx%z5Hs!lAyBaAL5@A#*c9=4^2>;ZR>mI5F7dkh!HGbI!P!aHy{&oEU6!$lO?vIdfc0IMi1XP7H?V&vZQI(-qYCvC2i9a;4!b4gW9wTJ(qAGEI%hn~)W!Twr-cbsY^~Y53yeldo4d&-5DRU%FVx5y+7?CvIE^I?91gOg_3Cba8dDsLs2iho~MmA1~sR3oKXFbu@gX;fuR_cUM#Y-o)bTVj)K$N7<aXaUJL=2RbqN=yK4-)y1MZlde8at$J>#h*K`GyoSDpuQYt|{p8o>s|O1#zAhGW4CE-A6F05{9pykLCLdi6y12Snadd<xuF~iTP27a~b{!MOvfC<QT#b%$pd)lS=;G>P>GbV>D>UbY()4qoIWH3G+vi}ySoXP`Fs?>NInWWh9CUGYv2^<OxN2y|ZK)ZD4b8YM6Y1O6h^$1h>}yR$qPQ9z<v_=3mn-{TB??|XOUydB)fm#JP$bHY^3x7|D$@?-i9~r4zH*=+!%w6iFK1nDx*T+|9L#e>lJgvu<UHzsTK^>c$DuA-4yVHLz~E%G4C=!PPzUOvtplgPad09uKzkyb4X42wa4y<2;CyHZr^7jDPlpSj5u620(4Gb7!I{t)nxbtCmqH4p!sTdF!37sVGq?<GGjPMj&>YgxHiuSlAzT7pw3mPnnU{kf?d6aOt)T^^qiq3gkeLPnv}uq5Ex`kA(R!d0Tmc4jMQcD$Xb)M?1#K4ef)3CQx}$9e-9SJ`=!3Q+T!qZ8&<|}_7zjO}GxSB<83rM<I}AYE9s0wS&>IG$?G4w$)i4Bd(GGzE7!KFKNVL~L2u8p#$VWR2f-n@aVGP=AC`4v16rs(9@h}Q<U@Y1k2qQBe#-YuJV#tHhP=a<eTn`Z_gK22X;0Blkr7#6;Da?ZFU?R*!I}xVC1egprp`8r3AaferhISg<2{*!2xE1YGxC@yx;SRJj;dYn-H^XeSH^Y5!H{1h@(cT01!#tP+3(?Mj2Vp+Ug=J{x!V<U_7Qk|}3t$B@7sE=li{UYN02aZ+Xcxib$Xo`GqFn}$z*2Y!R-t_eo`Th|7B-+=3(vw6um+w+y9O%YNmvJ)(5{1xP!8)sqFoQqBXa|6MY{oBhUefJ*n;*M*oDkZupR9tcnSUn3ihB?uoqr{ZSWe}ZSV%{gw60O+RgALyaGGmb+kKRAG`>=;Vrbg;Ujn(-i7^W--XZM19%5MM*9wY4u6OD;ZwBl!zb__d<X~7ehA;g7w{$gi1thPCwv13;Rmz_;b-_3zJ`CG{ThCPui!iQ1?_iGxn?olIJ}loi7VGEYGT5X6cbJiHaUBKIWxLeQiV-UJWM#$R}xMPHaT}LD2n=4VUrUN6Aty2gcE~J&W^HWQQs<Ta^hjap}vxEV(?pQmZ`M-I@U8iiYGMBR!@}wA*y4-p}vxEVsN2*p;}b$R7+EbXN(=JJ}9h{5EH)CVZztqm-fw3FAlDJ_Dk`e(|f56?d#USghPEL;l$u88kMMDzP;G;rFi*Qm#GsTXjB6e4)v9U6N9&OzeW}GZDslD@SN>utE}_SONa?y>M-GJ@%q=VP;GzmSeg{ywXKdi{>-K|FyT;NNjNdMb^HDDoc)z+A{4*T@P2uy{>3#g;ZR>mI5BwUn@eQMZNl=^;gxp|lTE+5Bq1hzsl$Y?#XbMLO!f@4w=^kUQu=+xyz^Srz=T76CE>(i<QPQXAo^KEKa1!aMBgC#SwugIvAzar!?+mhYmhdKiwR%qFyU)4_5p+RAA|HCgY+MR^dE!tAA|HCgY=&$#y%`a{}-hH3)24u>HmWCe?j`cApJjz@q85I9FL3fd=%sykBbRk>M-GJF^*A!jBkRBZ-R_(f{bs1jBkRBZ-R_(QH*1(Amg(j<Fg>+vmoQMAmg(j<Fg>+a}?wCLXc}vT#VNXL9Rh@G2u%cCVVZ%Yp5XCUqP<Ff?R(Ex&8`r{T1Z;E6DXXip@0zGB*%p&JY(94)v9U6N60-ncE05=ZT96hx$swiNPj^%*_Ouv&F@PLwzOT#Nf)cw&>hakU3{uOgPk65>5>MYdz)vAN{q*N7P*}Ei&Si3oNhkd`!bv8osFbHKb15zQ^M0Vj)K$N7|gYaUJL=2RbqN=yK4-)y1MZys1xZIhZculnX4c@jO$*R~o*!;iC)G$Io7A@pZ9~BaowPPTaT-bd&>~n0$0O=;G>PQJwGJpC@<hh=@4l2A0>**YK5wFV25BOLn_wvc=cMLXLqPWpm=jb)cgh=)~ls%Rv`c7b}jA(8N_59ifSvP~Wa&!dP}&C5)@lQ4Vy3E(cv)T`Zlx-EW2Fyil5cE;Q#wLVf!jOc={PmlMX-=qLv|LYIRst}d2N-yT;D&A2T!<FKI_w`C%I`x=ojmVK>B7+0gC9OwvL4!XFySUUZ`)+7E}@AzxI<9}hjW3#p1vCUfVFxNAlffudyj;&}n!4_-1<0Z7_ddGIyX{~qcgg2};4s*R@2fPWpVVAYuu?zOW%dp2<@7R;{ddIO|U)a}cxyq{BSiG|94#Nq4V`3;NOnjviOne>T|Mt%lnRRbEYfQAQYQtvTlflGSI>E%(5&myqpEBzX@IbV!YQtvTlflGSI>E%(5kA(RM@#neQ%*ih<>Yf!6qn6ks<w<duASMQ$>Ij<MyfsE{Vt9c6HS>cCOS!D-TLXVSWBf?w~py#P1DKxrjxbK+n<@O<~`HUI*!TW)th>&KbxL%M40HvqrpToX{`HP;j#FPA;rmlzR$^L{hWO6@AqHBs_)*5toBb9FMT0R-S||aBf>;SCX0zq(pa~Se=OGYDb}s0J6T(Ivd->g&HeXaK#keqsciow@tg<hD9_0$M}&!vJQ_?ij|%HP>+0lluSfG4Sc-L@KXvk1R41QHb@Cb2h8dsBk3VW_9iwFNin$NV^m{KpB20AT(O{yPG}gU;axC6Op*Y$1K%Bf2;^h61%$ZH(_}T5O_D>c+k@|5(#~)f85hgk^Sxj`2#*tr7lkbkMY+D`9{ov(_W}-z6OgL0W5{?!l-ypFJ5-W?uii-(f>M-HQU~D&o9J{12wp$iCc1dBPBa_8MCuyvE-|1Mq`$TcF?;SaL2g%9%NI32pWE?(XjANid#^j_h(UHkwqLVb%?WJ%u`zkouV}asi_cw5|*MXCL4=BdDkRWrjBgQxv5@eos#F%KxWHHf68tdN8JDT_OoV>F~akB5rIeB-^$$NBoA0)`VSW+18g9N!3O9~SmnJgwcNn_o<AID-35Q>xCf5XXM98UJ-xc!;gf;?9_V!V1&Z$X~1B!!8NOcoQJq_OTD(W7}^)XBS}6es)MrjvI#oxIOkHh-xg&ry@Y4c3hm<k@LbnCQr4G0{0HtlNvm$-Xp4vqufZ$9jK~eZ7_ovNlmGeq&-NDNKB&6HI&^;s5scjm^4~wYgfcS@&cx@s&<6@pXj%+xNFI>rU3DYsF^WlflGSI>E%(5kA)MtDEoKY}%PGUb*7~;~#a>75<C9qeIF?oN}q*OAX(!v8o=+#;O*+Abb&rF9}~d(67!<q)&5>S00ZqHGHYb|F8D{tNs7y+JD8yzQ!m15n}GV1IAodPp#}XNK`K$v^3vX`$0$?8neb&{Xu6jpg7gy<eoRgC~H4lTzJ(%xqtsKBlV2YqSwT7Np)y><lWA~D5><NI=Wb>FHv8ieoSuX-<_@0_(N9vQU1=cFB#3YkFn~di$yj2&M21Wep8@!M#>FZmnDU{aze^*)$yJK67?nOE7X^|9CYoV%ZF;}@}c@vhjM71I=-$h*QM??ng@D_t=Q&)j*m&#;_+5)zxR7g7T#BhDd*A8J~Y1SJW%`*T4U__Enl3l^?mF7SiF0mQNFF47~kih%)H_~WAtf*#HP}6Np)yB_0{Rqd{AGazCwNDy)Vnu*2{0U>Nsz5Gvl|Huea)$Ah)RR?wy~=Ua$67^(K@XG-qAi-^zSj-f(s|b;<k#67?nOE7X^|9CYnK^PxJr+;sYsLvz#db@@+S*HF9|Y$*oLKVUTfd2_|JZ%(!9OUpNJXe!?5=@VaLdlr^oCpO;G$I5?3lg6UKoXf;etYfoP=Zn>g(#7joN2){1sjp6-`l7x<eTDkQ6JJhKCw;p2IkQ}sk1PN2iY-m1sp`I?yEap5lt(oxD>rD)G}dcP&QSwKv`~}oJs?qEp}s<WN#pA3tIL7v=<=cZ)R%H-ZaTg$|CC-0ja40|SasZy-_Y39p%OP()JDvneVq7V?g4}1H!{13&)zsmw8ioBi&v+Ki3`uM_BEn9FWlZ%G$>|bY2Sl#?H!%O#|!F;4UzH~Onr56X)M%KsHsrXxS{TK%J;}nt37r3l#hK#Zdx2xc0N&G(Y333e)$RN(uw7UuI@Dd)~&PD&=vodKV!RLEQPTY#*#D#U43==L?%5X)xt_lHFbH?SUMfbr#Vw!%GcFvYxxVtrbCr`O#N%q3r5i|m3Ymg1H?i1N@M%I2Mmg5W#ou1dmlHp7p^fHH!2g?pL?e@wosifPai1mod2Nl7PimH>{`*ke!1bAP#%M+uP!c)g_;UAC2ATAmIu|6-utaO>hj@*C#%c<HCWmCM19|WCPz)EyHd8s^GH{Bn*Z5d2dRrzE|uYV2PDQ)7)xR-NpsNESC<df(d9<<sW0Ww+;n_h{)09*5+$Gaw(2`;_()Oc{x<7I9DCc>A0c*c`%_jgU)7{o8125unuF&Z_1&31Qe<v^FKbKxgYvC$MPf*!-?R3Wl}oBa%XM+7{=rW=s*m<GuhLhjUxE5Dxlw-G^D@=+H(jba|Lfz6)qUGvuUJxAuFaXos`u4MCBNNKu^Z13)K{oqf%-9Z(bbpcKz(&}p}A3CTCU5D@^v|*uOPm{=9sYr@r{<-?O9>BzaTjaJ7<Zx2|G7Qb!fRRF4f0lp~$gNc6-L;M)}zOinM=}kL|DQ_Sfc2V_|<&c7LmCE3^N^)J0ccngjLK)rICpeQCKaH_F%LjOVqm&ueq65aiq!<lK*P>~T`sW2vym9EszJu*Var)1e%lCiTT}Rg!U4l5thp<D^0LtK}Bu;8?2cvD6&fRn=HZ^QUoXEWC~=`#MrJ?wQvJN#p9;f%0iwS}$Fmx}0@wLi5z+Om*-&F6`^LIZqJeT5phReUxL*my|uH683yU;`~9_^9M<FaK2%X`G!H}8&SSapX%UTOOm;kBy%lg&z%fitZF$&`8d~7_FT)H`>CqA7OfY}fyTvorn2XmRr4Qn4k>94y7r-b8kg2lm!~dgUHi~HbvaWVoaYOBo^Ree2y!owMeYTn9Q$6$ycejt_c8B5B;H>L`~E`ebSMY!m9ogaQe1tiW8d$X_euuUtd>udgZER)zMnGh=~UJI6pc&sr?K!}QrY*CRrfyTy`iLWb#<rw1aaf$=_F^Gn=Vi4i}&e<eV=aL`-`f3d0K8i-!Sjr4ZO#f)t)(+&k*G9ou3%?^8rb9XgT!_bbQPp&pizC+#_yWs%byFFrRfK$}P&tyy87+KMygV&#0>BAv6bC7aHrj)V<PvMpX42L)gzx;?|w!K>0K-t*<UmCpl9cnx`&js<Wgp*RY?<na}z})w4TVZa>>p_One{^-Rxx-e^8ElznFu8}{=+Np)yB_0{RmW%UGkwkgQ7O=&;djN#Mr{riVW`<Z7<o{@JutEy+7G-q9`6&w3X`#Escvr1t<BaK^M%F)GL{Xu6{_3W3%)#XpI6CIkfE`RFl;JLk##JY*@IscKYUnILelFa(Wk*tsC)_sg5*L~ux6aCfxf3^SrWcyd{?@`a%-{TBxe~-Fo8JuP9?{OO1I#A!*-=h&)bAJzW{||G2k5l1%I1^5>_V+jiF0l6cF!%R39nOOW)%N#jY3=XfvG@1z;BTL`zlRI0xyy&SzlR^~B@loX&<fh1Z3S82wRZW)!rum@gWKB6!wqerHDrLWcKEmw+Cc~CiM9jugU-+%x}$9m1E33Zf~(MWg5J;(y22o|UEylz2EAYi+Fmdm`a=)625k=*0Ry2g3`5%&hC&}04B2Q0!x*?0M#4C2zm7@PejP<<bKrU?fP5%}$q<ARYrl@E)*c?yVJt-8MwkJma1&ey#V`|XG29B%U?R+dTVMj*0OMf_+>CY#%!AwDPFM`{;VyU(?twdC0XzV=!y|An%z^u1CEN{5U^dK!N72rO$KgI$3Tt5%EQ58h0v5t*v<qQ9JO&RzIXnr=VU4vbhq>3r!yw@)YtL{68(;@K3s1xIXrG4N@SL@O_$%-?*a{n=0`{P-fY;y!coE)&eee>z4ZC17ypDD=ya%ts%kUPwYwfeK4feu2X!pVw@OStSzJ`PF5&QuA;e9v&Kf(v_D|`l@!cXuEd;;IV$M88ELi;)V3%-Q!fU`g0d#J;HhOgk?XupCJ*&pyvIF6mb{sF+gh2P+K#@O$07OTrnVP~_3tR6d`)n_NMGuZ{~WY(OW&Q4=Z*@dhDJBOXh&R`dzJ%e4!8nN?OOV)xlVQDOtHD;HgZOq*464s2hVlI}#E@$Vmi&<;57qcwpW$CN~Gnk)sVHwQBu0ZQyy;xh8$-1(hEWp|`A8W&Upl!qYvUaQ!8^HRp&TJsNk_mPdTEVVieOPxkh+WOPvHq+h>&*tE?ahL0C>zd3vwSv!6|rnKgyo?f!b({#%VEVV!mec@HjIsAC1^*oNvwbsvg_G(Y%H6?#<5XsBHB@G2AjabY$}`1#<R(63@c;P(3Y_~*i1Hy-OKJ|H?jNJt?UMN7up-xGIl$=g)Lx9+0E=8b|bruEkS!5Th8XNxoib{h|Ob<u!Zby_8?oyX0ylH{cJINls(24v4`1w_5fRj_5rqmt!Cv+v5jmU+sf9nHSBL_*RY-J8TKUG!gjDHm}G0&(`-AdU{A5#>^b&4+spQ_7uY_wjXld=VXv`G>`nGEdx^cy-e51XSJ`H^i@k+*7yE?0&E8{Quus|h>|6FBdxw37_8s;U`<VTmeZziaAFu=LUG@?C0qsZZ7xp<j$PTez*_Z5h_BGqjenz{W{mK5pzGr{1f3fe_Z|p1fPxf!L|77(zaL!NTr}E=?V}2rMygpjS&*LZY6L=$jE<c{1&g<}#c@wlJ^Az5IpTSdkGkzv-&KvT&yeYqkpTaNY=ks&;#rzU}HouUc#V_D3&|biO{4(B>XYzF3inrr#emT!TdpYmKJ>10&-jTQFSMW6M<z3Kvd3PS*ZFo=KgSX{<xZr-?4XvN|<DGd2eiiS_+w)#Li+APyd2fCtAI=BxK|BZTAU=v;!w2$gv;%pF58+qyAlj>WE+5Q?@-b+K@<Kk0U(1WoUdzYxd_IDYMLU9rc>&Mk<Iv{uVm^|O<|SxH^C>*S%lHhmW&CD7iI?(eXiNF6{5n37&q6zq-@qsE$^3S-lldL|dOn@sg?2ih!*AkK`JHH|@_YC#{6>B^+8g<7K9k?Z??rnXU&`n5`TRk&^Z6ruA)m+ZM>~%{#uxGX_`_)L;}7u#d@)~zb}?Vgm+%MpTC@-FC-_RfjITkvj6caA<tz9)v@3WyU(O%r>(M^Wht2L_T_?|4`;wu<vo}BO2)7v4z;KF9{bVqSB@<zr?+BARCd8Cq8=m#m6Y7;+J&mvXZZw?W@mbxI!o*iP!Nk`Q{!e`0#IgK-aIbg08lSbZ>bpB@#aQp8F!7a6F!6PSO<(feqqSnwHyKQPr4vki9pPjB{p`p3Gsxx!ezU%+)J%jIEo@OMw)rv<w)t9|?B}49{k-$B{ytojL(ZLAvFV!(Cce@MCccjFf8zUmkLCXAcr6g*+EFXUYe7<&_(~_3_&UOPy%uB+P%Fl3aZ;H0N++23I>M$enIpx;CcidJ_)>=nUyG}M-{0ZAN_Bgm#&DF5lXmD+!~Bjt{AYgOo{<D!5WZ$V)mn2<L{mA)K{=><bxm!aRdq4(nU8f6V?Mo5@b~x0w)I1HU1>gAzCrjR4qp+za-d(Guhoy2vo1GX4!T(O_b@8^`yAzvK831!In9@pD-B;&=U4mw$~dv~{V;wG`u-3<H+>(ApR@j4Bj0@~4}X_s!u$ovUpUBLko<*%`~}HBu73QSb-C$s(8W4j-?|4!Rt#S}EnayRme<&CT*FryewB{JcM{9yD2;w19pykLCZ9O%kT7nXc2NKM{j_7wM}wR%!om3{$@!ujoR78XS3e)M`tftt<)+I)7pvBBRX812b>r|6USE>EemTCrBzyfj!g)fn^AN|^_amHR{J)xCIi9P;(>Vc-Ge;P-IRAsw;CMJ0?eTCnG=%zaI@<bhDsX5F=b>#3P2fa01yazS0++y<a1t~{dlFm<=fD}z9PJr!A=HC&;c~R+LQ6Ownn4=c%01^VfL3TP01vc)i@;^AS+#~#xD32#FM}-bf#2Fk-Va?M6Vkyzn-1NqHLK2O1JD67pe=Mq+ZKAl70?c@LfZ}oLst;i+LC~);Y#QP1JHJY{?HM6z))*7Y8do_zSiFHeIdtMvl@=JH;ja9V4$@YH4w6)pS9<FHvTSzJZs1JLi`<p5CowJZ4gRfG!#G>Z2^pfQ7{I|(2jwL$Sk(@jxUBOPy%CN656pa6`5hU-de?)4C7$}OhY>XZh`66zVWx<?|Weu%z)d`&Vada6Wj=QqrDMk!wqmVEI@1SCvWaIzX<J}uoUir+h8Hu+hCcsxBL>cb6_#t1@qy4Yt_r#L*87mdJKO*2@k`A@HpBB;c07+`6tk>fVJ=tJOa<4eFXjnkHTuGK)V_?!+KZ+o6xR;ZSWMVv-XN#2NKF*1H6cK18j$l@Ep91_Bq%KTi{vPiS}7|)%s4|-DsbOSFGLS_o00W7}S9V_`3l#f<3SUcEM|CcftPw%&i0>'}
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





CAVEA='classical-continuous-radial-tier-cavea-01';ARCH='classical-complete-voussoir-arch-01';COLUMN='classical-complete-fluted-column-01';GROUND=.125
placements=[('cavea',CAVEA,(0,1.75,GROUND)),('arch',ARCH,(0,-2.75,GROUND))]
def rigid_point(instance,p):return tuple(p)
def stored_point(p):return tuple(struct.unpack('<f',struct.pack('<f',float(x)))[0]for x in p)
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[stored_point(add(p,t))for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,rotation_z_degrees=0,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values()),coordinate_storage='Exact IEEE754 float32 after translation, not hidden deformation; native versus final GLB bound unchanged2e-7'))
base_mat=len(PALETTE);PALETTE.append(('SceneOnly_StoneCourt',(.30,.28,.235,1),.94,0))
v=[(x,y,z)for z in[0,GROUND]for y in[-4.2,4.2]for x in[-4.65,4.65]];f=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];emit('SceneOnly_ContinuousFloor',v,f,base_mat,'Single scene-only flat courtyard support, no extra counted model');FEET=['SceneOnly_ContinuousFloor']
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
  assert -4.65<bb[i][0][0]<bb[i][0][1]<4.65 and -4.2<bb[i][1][0]<bb[i][1][1]<4.2
 for a,b in itertools.combinations(names,2):assert any(bb[a][j][1]<bb[b][j][0]or bb[b][j][1]<bb[a][j][0]for j in[0,1]),('Whole instances intersect',a,b)
 contacts={};floor=triangles_of(FEET,vertices)
 for k in names:
  tri=triangles_of(names[k],vertices);mask=READER['np'].max(abs(tri[:,:,2]-GROUND),axis=1)<=tol;bottom=tri[mask];norms,areas=READER['normals_and_areas'](bottom);expected=float(areas[norms[:,2]<-.99].sum());report=READER['actual_opposed_face_contact'](bottom,floor,plane_tolerance=tol);assert expected>1e-5 and abs(report['actual_contact_area_m2']-expected)<2e-7;contacts[k]=dict(complete_ground_contact_area_m2=expected,actual=report)
 tris=triangles_of([n for nn in names.values()for n in nn],vertices);rays=[]
 for x in[-.3,0,.3]:
  p=(x,-3.5,GROUND+.7);d=(0,1,0);length=4.3;assert not ray_hits(tris,p,d,length);rays.append(dict(origin_m=p,direction=d,length_m=length))
 return dict(instance_bounds_m=bb,complete_instance_count=2,distinct_old_models=2,new_reusable_model_count=0,whole_oriented_triangles_and_pbr_retained_before_float32_translation=True,actual_full_base_contacts=contacts,selected_visual_clearance_rays=rays,not_navigation_or_full_space_proof=True)
LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate(vertices);result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,1.0);ORTHO=13.0;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(9,-12,11),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
root=bpy.data.objects.new('OneCaveaArchEntryCourtScene',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole scene horizontal centre; continuous bed bottom at Z0; three entire unit-scale legacy instances';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
  files[role]={'path':f'assets/classical/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'scenes','assetKind':'scene','theme':'classical','style':'warm-handcrafted-village','title':TITLE,'description':DESCRIPTION,
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
