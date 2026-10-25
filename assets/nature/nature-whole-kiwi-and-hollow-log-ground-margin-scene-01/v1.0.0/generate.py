"""Original complete ground-bird hollow-log margin display, two whole existing models and zero new reusable models. Lightweight maker SELF_REVIEW; static composition only."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='nature-whole-kiwi-and-hollow-log-ground-margin-scene-01';VERSION='1.0.0';TITLE='Whole Kiwi and Hollow Log Ground Margin'
DESCRIPTION='One static ground-bird and hollow-deadwood margin scene, zero new models. Two complete qualified original objects remain unchanged at unit scale and with every original oriented world triangle and opaque per-face constant PBR: the irregular two-mouth split-window hollow fallen log spans the left-rear ground margin, and the entire low-body long-bill kiwi-like bird stands clear beside its right end on the open foreground side. A finite scene-only earth floor supports the entire original log sole and both original bird feet. The end mouth remains unobstructed and the bird is outside the log, not squeezed inside a shell or presented as a nesting animation. Unlike the earlier bank/reed shallow water sidepool, there is no water, bank module, reed barrier or crossing; the new relation is an intact ground animal beside a dry open deadwood edge with an empty forward strip. Neither old model is cropped, recoloured, scaled or split into parts; source normals/hierarchy are baked and flat normals recomputed, not claimed byte-identical. One scene zero new reusable models. Static artistic wildlife association only: no exact species co-occurrence, habitat suitability, animal care, foraging or nesting behavior, locomotion, biological process, navigation or safety claim.'
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
LOCK={'wetland-split-window-hollow-fallen-log-01': {'bytes': 27920, 'sha256': '9cf21f04b7be932f0846d33aace58ddfa88f63eb0c2e1a6edfac68eeec14dddb'}, 'animal-static-low-ovoid-long-curved-bill-kiwi-01': {'bytes': 61600, 'sha256': '3f0062d1307b495c735c5e9b578a2d88670bfecd94799a9667ba40f532657db7'}}
ENCODED={'wetland-split-window-hollow-fallen-log-01': 'c-rk;cXZUo_P(Nb)4O3YV45-8*K4n4+$g3Q4A>Y0#%0}bfwhfIv*{f|C-f3}3n6q?5<Nf+B-B742_=LUY6v8>-^@BM86{6dKEIdq{&}3UA0L-HqdWJ0(vC*6N=)t9t{4DRP6M!22I$x$wCiw>n9NLjmWS_fk3@UA-4T<O;qdVF=#=EhNYBXBB$6hYz*KvByxpM*X%ng$V)Qn68!aAQ9z*Po%;b!8;;i@9dW`h)$c!T$c=&36W0@YlQNumbW73GtqlfGNygbq~;$8ot>o>CBAO9NeVb9HS#AMPa;xf_(Wu)8Fv!WdtskCWmx?Mw!srD>N($np6S@w8MTxv!p`70?SH8mqglarAVuStu^vOAJvQZ<=L_S94_O-^!Fk|rxBL*s}^OeDT!6q>Y*?5w0rO$?zK>1=<Q$?^8qImzkqq_>Pg_VncRL^`N6duEbrOur2zf*jBu;&9j#vr}Un9b89`AP4V34@nx30VE}-#yjjJF;QAF#y>{pN_2E`Jn1FJo|Q^MXq`DIH970IqqZ&_O6!D}RFd!3sTql_wK|fr1X78t==fv@iL)@@ts{v!Gb<)5IWBrga%Of+YIH_=>QE2gEJwE8%Ok^)oS2**9UqgGokqN=QIkW%CdqOn4<o&i6vbv_r^jb%NLjKRc0WzLJvBL&R^OgFRFjYzlcmX~C8tTzWM(;%2Wg0@kJe99c-ViXy)af+_DM(%mrSBbPRWqth^9P-_w|U0j~SGeJjCAD!<V{e+PyS=3yYkYoJErSZ|xb5XqPtR|2Z@+)t(t0Z%@xi&Xo6OPbVXGnfiJJMFw?l+oP`swP(gq-MG5Z>3ygrE6HJxiFa9y%)g`4$l(gxw+rdrHn_0)kYsyKbZX2{GAQP#QLe-G8%gEyn<|J#3#HJ`l@KZj4=V6~DY8)H@fq2%srDWur}6)))o<;C?e;+t_L!_ByTcwI7~>d7vN<T$(Zx<mm6{wEmXV#9M9wIejACOl?Lir-8IE=&$Mj^4(t7KBw5~rEok?#pSqv60V$&L}^pDx1*IA54labi8rb3(5qSaX~W{bt_rK4f~cAS6pNaXJL*CBtmd0S0|O?^y8y+LoWj-+Z=9#gM$`w)9N9ZXnqe4@RGBhnWh%&Ik-4SJK=heoe6nOvjP>8yIKRd1yOvJ{&1Rv#@1N^dO6cnWjj<D<1$N#_1$IKgBf!S*;JhWHS2&2U5%YQ9Kg(phCkq(d?m7EWujn#oX&rvLAl3WcB}-5ZQPX2ahMD$tQJkjOR0k=8anzP%$RIlYKOG8M+J*BMO~Dl`(l;kO|fh(&MlaY@lqXwq4Hd~^n@p-3Y#$fRu?={m2-RayQ8^Zx5H8I&VAEty`23R}fwk&9Yvc9z{WvTmV0LVAXTc6G(jH8iYCKxYqM9XY+pg*iEn`sn{Smx&Wis!|VzKYB2-J($=YbnolI{6`NKwg(@!2mSkcurj02vR&wOY#)Y^u5aO(IP!m)8IHot#AYWX*d5{I%IC_)?_b9~hYlinHtF<cYRpb2mv=q6rjYJ(>GwHRvYtrTWU*RFom^KS3*lCsnaI#+)EUjxWYlT(KIETf138IJS_`dZGX1J-{qK74YE4=gd`w!MQD-q5%sv*K!AP29xnl7MZyRKAedV$->r}-2zV`Zm*WU1ZdxO>dd;1<i0i6TF{?dct{SjF8MNZnkNx^%v=B*`Xpq`wQW^&;)kPCtj&7;9&CD(18S*O>N(^7B#n=~5#eh}|#ZhC(fbq1fm%cA-H0T@i?_omTIhp9E`^;V0?N`_4@OysJox9GGwl1-D=YW}-45|fTzpRFW^<f3MBrBP3`>ti9`PUQPjZ!qcpCXE&qqj+C?pZDj{WHA0+9<A?>fQafJmZM92J|-Wdf%IV}GZ3xC@^|O3Rz=Y7?Lhbbyy?w<%^Qj7k1p72q3b#rJ2cDQnM^aY$lZWJYxF6!geD}oZk~ukR*WN&QiIWI*8dTYipGT&we2nR)MJ~QwXRDN)7<c$<~lMh{8M`$pCTOoukC52)wkEv(y`60MGD_YE?s|WZ?F{M@PBQuGnkFWB8*>a{!{sM7IJ>5AAw${`*Q?7R-Yn7@YfFXy1(S`eI1zee;NUqWNLl>Jc8d(hu=;GHUfjiU?y{iJ$(TJL%PD$;K9-@(+$*l`caYP753*!Tk@*oul!ew%N~rCejd;UH#!(8K5<T!#+&_c<0-QRmS1c)U8;dC_}GD2y#37x>D7F1JUOWksy9AaYSpwBj-0hc#?M?HExl}Z9X(okP{t#w&yY%Wo{##}+JkCFPLU2QX@ri3EJtrojFCp~i{!st5-#K6&$1;Te|otu<yk)MTZfB(dV8tB@_Uv^($TtI_~hrk#7aNSlJ=RsQ1CDF#8X$tNp;aYw5OO;#<{ZoQk8R0P~h0_RPjX}vGn+oJHA_EkBldLkEKUjeek%gLu7ncUVxNWx;<V!;fSDyAM*^7x@+6w&50>I%UgdRB<Z^P;o5l-h~=>zgQR;^8sT48Z&k&sd=elv?ehrLe0@L_r(<7#Zw0E#?~-vk_VXXKL}!H+GET?t);*X{XcVrB)3MXql`!Y=N}T3_@-Na(3rd{k#L_mMKi555WH}wXGsl7sdT*3*I>!Bjmm&Vh1yy{+v11|^a1EiUdsOkELyw75hPdJB(g!l`E*%$N-Sotr%4%hNTVR2Btc@ANXtSV(+n%2mQ)0~6KH@W;<v8$+SgxQIzED3CEq+}fR+wKEe^YITjF%aDLiDb71=W~(SjK7mGs5Sfh)VkrjrrZx+9;*{CK;zOKPz36|K?eiDo$gjHR_UFz$<YYzpIXY`~@XW$8~Q~Jm2Fxoyc-Ju2NA=QJrTKWSov`U-Ox0RHbdI_?@RE`Qn;KXtL!KRs7q=Z)}(A)y1~aV`QAy71(-|G~kDuD#>`8ee-NW%XYZcih})W_}<Q$w#i%CW3N4R5X<SYu7x&2n=7A{aeA!VN6YgC)+MSqJr>PvVrm^lPLE6Zm}ZCfEAg&LlWea><?y&yb&=&y`s}s!&+$g}!}4VO?U#>iZ6g<>Gq*OX;$pqiD5c;cIyGpeD&DYK0jhqjEI$1rO~&mDkE1E`HJC3~TE-9VK8k*PYQS?l4R)&Gof{lQmsXi@&bi`<<@Y^5L)*uA;*%cZ(V7(}QIp&XxZa38G9EJK6sk1k91;$mlyMq=?DZLFm-}%<V}5+8B1)OKU&d+7wk7v$RYE4K;xuMjquvKWk<<7opWnjYsl@5H7FX`cpA2^sSx(2L4X%ySDrLzy9apL4Q_-=4WvY1dQXOy!+ezfUY>g`3Vop2!)g}(l*5=9h^NYba>rO4)^Gl74AG#2PPcCkS6OQ`}YPi)i7)S2&!q#Pbd6xSuY>OkS*2gV3MIe@^_G*vwW)#Om7A{i7SA=)KYwmr9rkwj&6{llA8#)06UXgP;_BrQ^BWK(y8K-0S>iWGcw`{B`PRCAby`b~Qyb`B*puBNYFF}dZoJ6-Z@hjW35?M~i-YU90nt5Y_jMFh@z8#A$tX`vvuj()fFN!~ls&3mV<Da&kjNb&7#;@;A7C)Xc3wup!h_B8yiMeUh@wE*`+~)i+f#tjR<zaE35nH&;{L5M+@!04__<-0QO*od1lLnQ+{%#9p{M_4IJWl^53h%r_#^)}afZGq9itc>16Onl)e$}un8XK`1WsaGKPYfx=H;Cvj<26Q4a^=bxw2WuDf6GGNymz#~@|L+nG5?@3@7p?1y!><!UUQ)$Li%~))mLM&uKg6W+O|!`y+7z7R$rVTTyz^IeeOR_Y;p1;dUUM6jHk?Z7k{cV5SQ4rPh8idsyOxY5%|!lNxYIh;g(sPd^-T&J*vSS26+j7al_HrhdG$FPn^2IX8pFjIB>>DnGb8P>OIr<#h%uZql^vbS1ay2^VlG1_QNfRwS()=DA#<B^<nMi*PlDP&rX-VMSDe-ANM{ijHv|D_OQMZ%h{a#vMU(vKJZ4^;WJdaRc0h|AMg@QafVAud1HN8`_AZeG_z3xuKiXJ*}NG~wL}|3N8n`LZ5!*OlxNnT^~pTv<nJW3#fRHBlI7Xc^2l$K5RQKCJPflwN_AoV*;=Fr6cff8N{9{iDc6hjVQW;7v`W~$-cu?a7@%0kRad-(uf4LR9lK{C)?cZ<tUv2hEoBtHVrPo9=;jGot(EM3{EMOH%_~Zms`QX)fVHz4P}0fXC^tTDwII|H^At6sSzFIJGrl~I-WjfFXEkuM_A=q?h**5=-hD-#us#*T>WY4^N8oF<E<0I&*3N1`NgJ%4ttrdd8m*c2Rv5aZvDCe5Ab$5n6~S{$uJl9tAf!}N)}O7NQd`#N!S(ul+<+9RN%2#%nkw1v-m~zt^D9UdKItW^DO)ckAGVIH|Gj~e`D-0hghP-o{dl=5s`s@UZZf@_td2_dN9&rSnPHLm)J%}r+OhWH12AgRWjNmUQ9VJazN`;x@9P-KPwd@Xs^I4@%X8CN8rz6b!=yc5g(235&AC!t*tV>{QeEndu{g)S87M_W9TS!8z7OyF#w;!=4eH-VmVef+R3kS3emlq6`1_UdkvCzAb(v~<<ZP8a$C+_i?$7#+8~Mt%ZhB9w8&XMDBi3FrdkYUY^YEd24Fsinu|BNbr+zE+QF|S3xWRyHF7-fzD$GIFvx6~fUog4^vesMX+*UAB=EK_A+HE?&iNAKPwG_X@S61J$-|V#YJ2OlQxzPzJ`770zZOi(wwX0F7nqX>>AuV~ZQ&h6Eb?jbixUf)qEJnn|$m+}1i>(ps&(@3eSu|#z;CW!V?W5p)sm8DSgxXii;+uoRW&W(4t)uS8FNKCRyW;QW)ljT2>yw%LROq#HBtE!vgsi@-ovq{Q)V4y}7%kQnvntk_`^;B((SHx>KP6q}ucU#!Stg;x=-vAkO8K(3tUv4Hf1$C>Z-r4hA8(S?owa{n9@&hghDoU(Mak-}q!T57*5}-eADv|yXGsa+3uSsxva_}R;q_smp8o;y`n!ROdSL6$`YY*y<!nur>dSJrE=u)Ms*6%Bl=82XXQkY-TqzH%or7ZF4jlQ^gW^yU8WU^`4WR^-f~EwUf(Mj_ve1fPD`*B~pggo8*alicIj8_yf?8+|6~PTm1WllaN>Bx?1g&6%%1{;j2>O8!RD<e(31Z-(2GoRLg24~~wa6Ii608etp$^oCjs!bG2WS9|Ae3MzbOsGHfiQw$&=owP1%wj}hn~<JydZ*L1oQ%L&_N`@Nazg)ut0x;{h<$-!53l)#zH?5g&)KbjDrDS0|bc#6TuGt5D2LRQz03Gpf<E8*dEd#1Uf+`!AuwoU7#D}63m5c=ng$#IKkmC6rvy+MiU$jBcU(Ez&L{AU=%q*9E>M89>zdCB)}wslVAcQ!9bWna0X0;6le$O1k+(U3<3wtBRCIcLlz8yMFbbY0?2`3u$16ZSPUZ|AJ!9G533;$#=<6on_w+D!g$z1a0_gNi7*+q5!?n_VG2xx9Rzp4cK84?U>3nyuoGs&TyPR}!XB6pAHo5G2S9{{ump|}JOT${8LWU41W&**SPrY;6v0z)99F_d@CCsypa9mu2Dn7<5}bo|uo<opyaE?V6kFhHf?vZ|@G*P>-xB;5uED3U8*UQ33E#mkm;-wW?u8q$9|X8V@DBU{5*&hi1n<FJI1ESO0l^1wA3lT6;Ss?{@FSdrGw_7q6L<)x;Y)Z*@F_fovv3}MBKQ+Lg9~sOUJ!f%&q)+t!%KoM;b*uC-@vZ~e}!M*I(!dr2)=<=a0~XqZGyMqH7GsLQhIKs^c+g*`B71y`xNy#PEnt;6!m#WQJ+VsdA`7M_Su1&=Lkhz&oAnFJG*91*QHAwwBpA0g@~@<hgz1?XL&NNw60#%_3fgrKP#;vvuna?)`yF_PFvJ<)S|A77IodSsOyJH>wZe>drIqdO6zQU76*%YAL(#~jXH_tqknEL8cPqxOVj2fmOt7XXY2m$A~E<?CT4lE`*<P2yPjl!&{1M}{aWMDD}xP-!!)w~mF!(~WzgJ@v#>9oAUm#-osFSbomgS#o)O~uEjd`pUfz#GL!UL2jQ(w9aVpu_IIC}~E~HEj!T~RvDB9ULJv*4i2ksfT`h;aj$<D?W*tog)Xm)$C`LrCYWIx@zBR{8XD~WSMvY3_Z>&bmz!AyUg*R!!KP9-}V8_Ne@`j$6THjC%_4wJ>BWM|{K%q2RTt=CK6bhAiG_WQz3+t7zLY*^?ei%rR%Qnw;{^mQC=nf(o7IUCQw4Nv$Lt9dc}z)-AYXJeT1dZKXWpjo<;rI(cKY&>`RoD`~l?}JUKjiQ~6t)Z|@C?41sSDFu4$<D?$aQXu0(N%HcrfEYJ?QCqxqmBzJdt0S(1>Ta9osEs<Yz(q^*ccej_Q`S}bN2FN-dvu{&5MyayBk3_GXE|?=I~VsRwZ-pQe@6vi(oA>&n`pe>2(R#C3D*fWNzMoU;{GOu0rPH9t1te+`2lMlQ$#SjLiD$ko$pF1Y420wmZ2WXicy+nQJ#9cLzFxI&uflgv`N>1dU|Q-<;eJSP5FmyxW`H5g>wy%&iUNjv$a=Aemd6$-KKA!FFWU?@Q+49SPETK2Polx)SV4=J^3+-W^6TjLfy$k{Ng}g1yK*pU%T02u6@ue;0B`5J`~E^XWW1ieMC(=hOX2jp|=QKkw=%vYgK4YMcPPSK}|^bY3_8Vr9Jb!aITGbe~dvTWwtDRVx{%bH9U0HSu;I9nW$)4=i1`B5oe{M8@g<r8{$8qZ>~Qh~;$uk}>uoI_VWD<8%(WfB!~g9yUP6>3ni~+fnG3n}IS;_ce{}<&SD@Ehgi1UsF5D1Jx;G;aN`iHEplZ5`EIjQ(!rrqb_P6iq>DfFXME+`cu$&w8~p2vYhUBTA#fMO-T-yaXQbeoN)tn{$Q9YPUoM;#nSlaMG>kvoex)VuZ>H8U0D^Udw$&F8{!24eFZg~&Z{48b;p|yROZ!iI#0GQtB!BHy|0SX`SaVPlK6f-AEbuU{X#7cUPt}Rv8p)DtylPV^i8>BRh;H_Q~U8~Qq6X%IL&RlnjuKL<t?v<)7;vAZH2D2si}(7+zO}l$bL3lP{V0%Z&r>#-;FITs^K)Z_}OICXGMrAPIFte#HZ-<eVM8_y-)GYIe|v6_ff^^{mbE3Pf+=+8mc(GpGpZSjaM#TC#d0cPt;DaB7VLjY`+>#@5?S8uYm7wUdpTC^ghcFRuX%BQx_?5de7A<>JiGi9Vz2<uT)Bn6R7FTQ8G^R!#7=ut`8rh$Z1Xz1Cmka!!fEj%}Ix9T2!^6Mir+ysfTK!md5408cuUEw?<v`yr9v3HJs*0^Vot8xGxpdaGJM>G3m&#prWXT(|lH(xD=K7(x{5l`_@FqMf7TKQ&pVa&xS4mJZ#G^f*MZmqc2T$!&{3*s^WCd*w2S+;_s_Hx2fUu-n_-in%HamkGvA6_u9*X-SF%>om}_nYZt9W%hxZJao2tN`Wyt7$*MSwdH+2>^zc$ARh-5gP_7}GcK1hK4X5#E&1;Afo)nJp?>HUf^3puQWy1wEoUSui6LZlgnJ-jvx{oez{aSRwyQ!##({%>ya|rERqmI+{2hTk}pb46Hf*MZOJvKGu@ExDAsyN-NHo&_KUN*6!O%11ODJyT6!Ry>U;gvXD8#(%6F<haKCt^8W8>zkRE{X|Eka4<KZQAHV$h2{sjMF?!UcCVAu#Q#abnHPP@#sar0jfA1`}e+WQ1cWIRh*994XUBcdmr;^IL$-FhLutA{v~W`IL*)S@D^xW?WuwqPV*KWIRI_RDk-YrG@rJp1!(t#=BhYdN80tF6CLVrQ^o1}(qq4GQIjpTRdKrB)ot!elzI1npoY^ua#Ob!#|N8Sb*kZX-E8`s5_sg*Kwb@}>tIVBy+L_XUZ~=9ea!U54YYfz1*ze5f8A?$0UbHiOBJWNO=&m}2@|@h;xxAdUdAKM1us>c=5|GUJxaFT<<)SS+iJV2qb}Q#Do%4-VVE287<$X8hSS`Zoz)CY^gSb};WW1w&h$ghxW=LyPIKF2(Oh(5QGhB=_dTASaU9)P6e#0#Ep&7H2S`(|p^VdY(LP@k$8L2_3oNJmA&-Stz#olz<77EqJ1q{C@ZlA0d6v_4RA^fodu{;4a=K6Q#`llW!!Epx(|wYk`JO=KoRKn4*I+yPtUxthg~>QwkNx&-F6uG7jf~U%lV>{zq9K<b@+_zOCpDoO)G)wb#_9e^uNigF&kaimET?O{KEsUY_N?z@oUZp~9m+uae)JMqPWM&znzkHWiVBf&N61tDnX{(tS8X016I>td&t5IQ4$8nmj#B8vTW_h!DT~bBAm|J~vPHV|!|)x5^(hEm!%v))Cyn{w1A+Bn?YHyS^1Ir_NE??t5?MZ`|5g65<Sq3rXO+5{KIJc2e-*#6^p{xspoB8~mCysi{k?fIpPqZW`}I!w1cf&qB=ceIIdiu=?GYB7GgmL;1=YNTrvnD#2`x5=)$2DCyi4Tc`MZ|!ti7PvqWw{45^)c78L>X)M;)-8S>lU-ZPEs_KCJ!h_7r|+tMll{_#_!;bFP$sv(8gIwP`9p0!H96Z~BTi*X<XlZA(<F3+vNrfJ02q@s$oPYNA-LT`vZR-#<y0V!F&itiMtn`)Q0~O4x9z=eD^5+g7Q*5hI=oqb(_tY2HzhZL3uGkDo;e4SzvW(}yi2wr%6=0XBEHyW-Wmaf;et+p_+w9=Pgr`RmR;!p@)7>4){--ufC}vHT(QQHOytf7Tv~@9+ijHeBgOOPR(3{RF;hc?W)VYq_Z8!|F}<b3FgpD<5AUJCJAFD(N%+PNZ$NM=E}}@+e~4D(RN>SJE&)q?*vT7{*ogEwPfGS)b2}9~HLjxsN`+7o(_i)`!*hz+#J>{ha5;nA1skQ_B{@C9m_g8r$;~^*{1Jw(U@@KxyoCPgz?f{j>guYe({F{Tx!$Wvh^q{#l=vdAs@hck`qUr8Ya2^w0Wa7QEmq`lm~oC$=f-pY>6rc_nSL`egZxj|9HisB`G>kBKsU)|3Kx^Q-{;VeMv$KCC{!34QI?|E&YRuDViW+bZdq^;gnx%Id|=GgtHR&D~dQO1fozD)w~~f_}-s-I6{*tUqgKb+~YbRj7L|5L-7k#Y*<N^+SZpoo=IBo#JJhWVNT{!)o$ji%x!1-u85Q{+h3-;SU{M1!v9;@dH1*qHbBAyoM))+O{A`v#GJ7ZdspXpORv=BN>v{qP0j#x2(^Fa<#-d+L6-Z5O<rBZdo7J&T6LW6+zgWbOS}j#4GA*G1!Ff!-DY6%1vedO1c`d_{hF~?*`%2?VClmE$g2<uQGq*Og?^FKg-GbvzlRjybfmbK`#d5Hj%55lCD^v&-ah#vp)#H$98yP)`!(k2X8-q(ubE&nI94{>#w9SRwry*CB3o!_)~Yj`mG<t>{9Xg?3^KdlN;@Y2flJ$l^xvGw!+(A($;Dr^H<Up>wmOGC#NMZO^PTjDe8*#DYvek&^9+;+C0A}ucRy1r((!7Av+;cGVfg^(-mtE$vq<s?B*{uc<Cvz+$wV7>DMR3s5eP6zQ$fgEWN%RZ%i2})79RL$HJEf?xE*nVq`w7mYlmk7CJul$F<IQDz;V9p;+5r7?7QYAD<LNwjU);_J4PN|I;=3xc|GJ0^2sG(Hq<F0hu@hmLVmrvTa%a=LPBfwCxB#XxtJj>6X<P>(BaJ88MCb+IJMiju@z@PgZZN|H7^%_-;d13+2km^*L*JGT-5s+hQ3`u2m&{vi>()e#lR0ge7w4Ec0jW*P4C853ZUZm2<x;(<Ezu)95+>;My=L%Du6oZdsrHKh!{F^9M=O)-My4bSu=l$G5p<miF$^O02(<hHEdJ#CzuL75(0&No-psZRadK;uleKDKGK)vbIW^XZ?FU-R8^^uA{)6c18WOKA+wyF6<}Y*Lyr#%gzP1E$d@>QA<dEoQ$7VIwLCSpVg|yx2iCsZa!{wevzQmmen)cHuG{hAv|+1z8ts#vHd9NfBTAy&W{IMahoVDX50EEZ1l@1wF7lqn<3Lbt6{b+>(6Rijs95;E9qHD!%DhU(x;LRmGq{hD<%CX=|o8nO0`z1qndiDsS5{<peb<VQyhvx6KFxO1(bvm&>UJ5Yz?KM6nKG_pccwNS<r!zpb^SJc`$)5L0_l{6~GFZAO<(61Uv)~41g+78T=ubU@%mLYS11!66^@op$2q<P=cXQ3u;1F=s~at)PdR%2H^z5p&rzQUeKFhZ>SIM5D9$=_Jsz}5c+|Jpoadg7~&v-U;=nTGf0Gi1P4MZXbCBhK`;Z_fH$N=Cc#WFfF2w$gy0acfEltOmtd}ICwmSIB{<ZzgM1haCpa7eAqYmoD1xJ)EwqEtFrMIe2!ReT4ki(t1YMvrOoXWfr$Tq=22)@L!5PpKB48%WCO8}VKorb_4+(w<{UI6_LM*{p@PGlZ7?u-U4t9u#Ww46iDoBE4_z2b#Tnnj?2J2uW!HqBo2E!)ULU0RY!3fw2pAh^6@*xkl!A^oZVJwV+9k7Ss9+&`=VLyljMVJQDUAwTSlMmf5ei)7sJO*=Mu4@<eT=H1}^Wh{cA-Du$U@4q|vjoq=3Rnr};3C0`u-dgV{0hM<upTzR*YFL&Z(uWg4Bx{&g7@H4*baB#M}j}XZrBA6;0eJeun+daV|Y&RIXFRppW#=6zrq1H2(RER!MAV}j=*c+xFh6q0*(W41q2IV5uAdOTv_fEl;ysJFQ5!pf%^g~aOdFyxN%jv3s9B&3NAx6t|oUGYI0ZM8r0(Ia@U|P_bq$}^|%JychG>l4mY47=fT|o5AG)1g2r4k?iMuTet_HH$+hBcLo4n++=Z508}2T&;U2+5@a7EMLojg9;3;T16ZaHM+za>#jGPbm6Zmj1;TN!SJogLm+#7fYhzsK0K@eA*E5-$Kr3seiPD3fKE!U1KMLy-Y@?3ka1HlelMXnMT!gVCrk*myA;W}}h33leHb2YdwTqwa%t`1k5>&kT}*qw9d>T}(=9t3-EjW`V##`PrFlWW2?<$7`91jD)JTnjFO>rJpX=f$<=BDpAnQJkLBaecUc1p9Fo&dl}Yq6tQGew;7YpNk<F!(q<G4d7x4#&Z5#02jvv6Ab1`aBAKYrL@PssPB(b+LQmEdasny-u{33eN#%m9Z>Tgs{ieU`|s|BQ~F)Q|K}Y_EdQtX+bF#+i2dz@n%_aF*^i-SZ-$!p<ou`JnZxq`)^mR~?<Z0E%|cP%TcY$EhyT?3Oq6~r@lU_!MCrE}YTkeHzh|TW-Djg+t?i|=$r^mz-cs<|mn&VgCy3Eu^My&n?b72F8^lh|`66r2ZV@Nd{WMsNUUpGreOP<i{5&Z>-?H!8`HRB2mwM@W_)>9EyQWyl{$qZ)G;r6KVw-(?P}ti5X`G)s?lCV$RI=X~-BzkH(*u`iuHji;-!oTQ-fw`|?Ac8rb#lCvJ$<3LK)YFF?Q6QkN-G0fi_qv>k@aEigLmgiv-5ZR)-EUzCN$AY<pQUQH=DJ@O7_scJ*3t3MbSF?GWy^dFNN`SafONVMI}3%^Z(`lznlL7U*zMn>8EW^JKS?NXd5GZA686ya4QObJvkqr-rI*ill`5O^<nL0cjx1__x<_nPqh14u8Wu<tba5D+ly61|8)PKzA4SGFX$%v3>$`DzRbst_>F$kvIjU>&K|d8?q~d{cO&qMi;ww#x}W(M^Q8(820B-|m*ihe%9j?8@D|92SF+#OlrME0XcPKu-eO~UtJnEb|DUwZw;kPm+2gYI|JHGjp31_Vde0O6=5Dvm9F&i1ogF2_HCX4g{m>h`bv!P<_-VJOWUtdB8;=-&g>SKcB1*Vs#?>c=IA>@KSjp};Hy?Lua>!{r)r;?OHV@w(HIMJxH&0;gW4Gqwz{n)=__G-@pXJNC;<a;Y;_@TA$$YN+w8OuCSs8aQ&O)pYYv1%D9S4sXF1|ZIUS#=I%@ExC)>lI6v(YjhaX%lAB-fc;OHVo1EoqORY=}U6p460->~9jYab5vN`=&*SFMZl$pKv#6)Y4f<$<F5dfBFCK=AU!@QjK%H&tfoS!W@EgU=|bu4`@oTDU<{UWWij5b73}=aQ&LC1o@PLY{-EH1Q)<OC=Jb^1;G|j7KT7Bd`R#^m=9%Kzj!O-dJD!-7!HdGE{26r9$G<bg7l3T!(b#Vb-lY`5mW##@FwUDm0a&|SWa*`ECDxY16qPws0?{98defq3Co}g=)geG0M%d=jDb}ISHTLX3VJXRG(im*3*%rl!PW2)R0kuN37VlMjE4!Zmf%`g1GT^cR)SWj<9aW|27()49n=ON@FnOAbzu@rfsF(=!g{C&e!vst!5yZ;bl5_03v7b=uC>nk<kJAA!3@|+a4T$vhJb%xU;O|E!AycP;bZWJAm~J}6Lf$c5C9<rLm(0YAs9Ln><k@UtE62Cc7-mkU;0H6jDk?;4q>ie_VtDch=zWUNH7tSp)YiUaDw5G00W>uBoR!46o`cw7)Wp+q(V=KhjfDJ&<E@g2WbS;AOrpnw3!%|', 'animal-static-low-ovoid-long-curved-bill-kiwi-01': 'c-rlK2YeJ&*Y~+g4+7FVgdjbEE!kufvNMFxJA_Ukq-;neWFdu6rGp|(Kok@dQ3MNOL)2tO#fDfB>>VE)ilSmyzH=u#>)9}OXZG=ZzxVxp-^2d)@SmGA=brN4*?VSpc4ifhA7lf7TfYN{jR6>zK6=#Rn5>c#UujJ8;+R>!B42S<slPZTIc9i%vA@V)5<LrdiSA$ME6Vj1M-S~YI(mM5Z&&a5#F*Ha`M%<k0)G)IJA2z>md3`E<e-6=WP1RW#3WB!98;7v2ghR4wZFy26!~+tKX|4uo&NXM;uzn8(&DTV?nRD&&Rl<yuc$P$*k8zZ9bM#$=7WX4QeSjwenHM`l*K+@T%NzUJgYc2uF#+D%Z<+S`%9z!Wu=7$s9#=Cnjc*<C#$e9y4aUh9L-gtvx;*0R$+8bp)aqrBsRJT_sA>sXO$Kd&5ADZ&CSB-aSFdLx}+4RDd9oQ@s;FjF$Dsdl#gEZFZO5Urg1BSs(cvl_YE&7FBpVA@KpS-kH=v>9*329^2*S&(yY0@V)Pt&R9d(&I@e!blv7qbA4dxP=umb6>Xi7<rQGO(qEde#o_t?cZk6j<(b?RO=yFsk&hwWSR_)?1jxNdf7nero`~9<VU+oXRtl57@;|z^v1kRRTMcDyCA9y(Z(VST{ngw*YoI5suVYF}7thmC0*%%^vo{ukrY=7=Tp5^kAKopv9f!akE`LLY4FrmTyT@CJiURI8ehoz;(Us76Jkdv?N`FBXJ>LHbnp6@Tfx)hiA)A@{}P(8IMH=R$zV;h1qS&OZt6j>E;I~)HRUFe%tMX<8DSitCFPQ3hr++1H#boN3m6+Gsu8es|o)yyjP1${5c&nhC$$A>zv`J2vX?T^!OXGi#E+5fjV>$c#m>1#kMLv$f0F1{Xfvx;X&`xg5CW_vZ31Zh#2RXhu+g~!^`ER7cheD{Kq9P(OC2z79LLD9kyRTFXV1}^m3|0lgmH1n=1cRBe5g}KE(e7Bfpk9EX4V_mWFvF_M}*hG9A_}g{uy(qIF7tLiA6`<R3C8c;c%fVw}d7PiW0^)c<<EmcMas2oYHyh`Pvpew3Me{T>x1iXUQ(E=T6gLHjt4w6hFDNO?D$Mj36)ucPE-fze#m4xH3uYA*W#(p;md!zJJ{VoD@eUJGu&65TY=2o%Zb>x0ft42f`bL+Q`=j#;iVA`UZ|&%-9c8scb_woY(l=m+yR98CG_SS8ndYu`M8U9q#Rd3w8yi!s9j!8RaK_@S9DFy9S)37*m76uUv|zq3BPJP>Us&Rcjn1elZb<<@#2b$Li!-%%)zCjKL?=r!@kQb<C<(RaE5ZzDLm4q?Q_@BZOwWkn<0V=A9ZECfaC-O%f0N3})kfmUcIF(Mu4?~5LnjX$P__H~0$+J%Vb($nip)Aqn|AtAPM-j4@ZCc{!u7{Q@nbhXOmp(Y@Fl_=PA24C)iNR1UzUxp(SlrGu3p1{9lpbutU})qe{m5vfXBu`K3vzt#>~ww9_hnE78c};^Ow!a$CZi3wd|}CUz)$rUpxpi&KEt??7iIyN!mZBCq6Mg-kA_<?;Y>5YyT1*Zl~Lw7>`3vcdUcE7O<-CkBfw2eS+XvZ%=}@y94dG9gg_KrTpa(K8}%P__~}hC)-!dQxahaPES<`js&;c6`z#o;tp4ZV0R{Y>`s@{$%Ak>s`L_Fj>N<yds0#aF(tXHcJ;X9(OhDZg_tH~70<yM|63tp7}~#hyDQ1<a=Wz>R1MkV6I@Prf=7!eu_{VOqQ~QKCAs1wiKuE{rzgQ-cRG{Y79!$@x&e4B#baDagaO&@fg&Y1(0MFM61s19*pn`a6E&-XawTHEQ9pv1sxx<~_IkpjcIeXF!ipB7D=wH*zz;@MyJnT*ducY(R10y;==7oEhmIblIWlVWxRI$NaEXbp@q(h<f*h{n{QHHBN=v8n>{?%dTAtqZ_w?~}dbi2+;a7~7r%(8M`b0Xt$8>s2t2@hnB#|oEsUr>t^~Ayb5ZQ1zi4j+bk$7svd1*L;^`2$-9d0spLdevKCYcnh-mFjUAyX$sG_}#X%<{ZW^1^Y3zH&ldIxZ{oMi8%)ykeXoFBzx1`n-7X$jZULl^{zsquFJ7dA{O__)f3A@Po_F@eAjocWwv1ed1tQQ7I>$Mw$h<UmQQu1rBs>w=*fh?MUE9Z+k-3Q9d!j;r2M<osL-4bhxVyVeX^^JkrO<d-xHops32srSHsqmjst)#)HSzc#p^J!aYhghhioUOmk_AQR=wEg5%-#cN*>Q3hwW8Bn0<QPfHz<I_?q+F3YJiT#Q7RH{<O88;Ohmhlz9l<HRL|_rRGz5{K`fRT+s-Oz^l89eibn*$T;AtfP0e5z00r3vNef&TuGDAY5HJ?YN9gN-#-dqJ<#B?e7Vn#&~{Y37^KK@E*85cEUe<2(NG*tgkHtS#f)K4gzW}cVdDw(UTbRqOEQL)!p_4N0P&p==3D=gvQ1h6(a15*lr<)um&9A)0o8H7{aH~;WT+c&^+Qg)5Y_JdB6yrF8)GJbmN%Ifs1xbTfD}vaEUZB;S8)GUGed*cu$f&@!v?L%R(4o4aA$guoF!g>2RC8DEP4<_-^8G#@js}Pm;%luR13tkH0YOq3r=bzPa4k(Iw$_ywmNndqQ5^xY$l|I2?92GSJC0$`7orz(Eufh?Wzy18agi(U}-;Pr#?c<1u@2I}$7e64pRs_+(<0O_S-doJ`|9M3hV8a{O1MGU*?t(rLCtiMLZyUD6%n`vvx#iB9Y;lU&%-$Mf7c0?EM~xUqE%;nbz=D4M{e;tSd7aq{-u$#dff^n!`5#6)cS63pIroem3egf(EcWO15u%IUJ4OF<qYNTr|{{{@+h|EHOBN1jRa>2DKs9j&dQvlo{7M)-<mmGaMM@bF$WGCD6$`-qOa!%xX-FZ`qg=imNV*tu%N>i+RAXXx(EL{~!S?yiWYcR3=N{?h&9-PPxh$bB~+zO1`n<t*Jl!4=8$m+qhBu0DUb{XOyaYQ=LVBs#78pMZ<2>eY8UoYoz<)PNILco7(IczC`-38WRpY6$qUuI@pSGZG42YQTl7p9l=Ns~5rLa(g@xMBq-UMnYG-BN7J;3?K{a5mm9;{z)!}^Pfb(*Q5U^f_Nt$?<1g5g2!I{IN(Tf{v!hko=Aus@2-}^cn`kaL~ta$)Pbaka(Jl$Y?nNqe-HsS3kjF-IQYI4cu%4)1bmZ?Upjqh^yHTT`VSoiUyt=Dfd9NvEmaZzcu_MAN4?ouh&MlVp_1c6gF6XvkBml|e#bTSh4^TPS{gof;R{8Cqu$(C!SSx0JB1kM)$q{{YlOH*#^y>heC$GZZQhK{PYLmfy#qDOb0)%hd3j2eZ>@!RTdUO?Ufis=5Wn=|1`Xdnw^E3?PoVu<F2vrbHx)fb5&o(Bdm8?D(RLwT-0V<*180PI+|fN6Zg!}SD#B~dUKhw!D<S52M8CW`KaDWwB*!{GjWFjV$2vcaFy|!4IzNpt=Oo8EKaDWwB*!{GjWFjV$2vcaFz2Kh=A7hM=cf_ooa9*NrxE6ytn#h35OYp)tn<?db53%s^V0}(pE%a}X@of^^%zB%bCP47pGKH-vWf#|gqU-ZW1XKym~*l!SFMCN@H*4}-|$m^ulAaHc$qr!k+IrX<JX#m=zQH(k@)|29-d=KC&#%^=6LP$D<!H!$MgMHY51;IpHxzvna_^V#=q;@OtqqO$Fv0+ZZ%;+U@lEhrutTNdL9{~{a^8Uhmi3r*DckyKR?$%66tJg(MQ|vek@t0`XZgd_tn(KCY+lZVuy||Yqm_oOUm!{Qk{Db_S5z`wY9q?9gJC_InZ_J_;v3WYh(9(x;MmU$ephJ|JgO5TG1JqKTpF4a_>^8&cDtTY5y;K^$|s+LwQK`X{}7SDqG;HY=Nt?1+K~#xGG1;RoMbpWdT=Z3tW{ga8<UzRoMbpWeZ%DEpSz~z*X4-S7i%al`U{p4$svZP#a`Ofg~KM4fUWuZY4niZgHFhe#G_QG8l+k9A5^FU<ht;+z6V&2;AbhDYSsmxW#b`Xa!?&i{n<%7RKWi$8DhlOu{XWJ3uFxid!6af-7J;ZgG4Cbc30=<;VYfLLB5l4sLftWQPLWnu$8yG&~b^?BK#}KNRA2Uyz^{%35FpFZ6>tDC<B?NQE?rLKy{hVE_z<hA10CeHa8o;c}FhLjxEFBcU0}X3!Xh!zgHuvN<$?F^~>zP_}`VFb*a{dz9^=HB5lX&=F-vXa`eZ8pNQCfoRBpOz4WTD|Ch#kOkdQc84yI4Y|+@WiRLfKFEhYDEmMx%z`VyfzkoJVKx+j8>JhZFbC#=2c-w%VJ;*CL&+eKuYD!bQy5}gn@OanFvPeP@{*py5aZfRB0Ys6#<iJ5dJ02~YqJ#6Qy5~LH-+>Rh8WjoUNekqGl}#Rh8Wjo66q-nF|N%d(o+~>T$@Rxr!d60Hj_wCVTjQuiS!hP7#C9#=_w2`uFWLUQy5}gn@OanFvPevlSofth;eNuk)Fa3b54?;!Vq&#lAgj4b54?;!Vq&#lAgj4b54?;!Vq&#lAgj4b54?;!Vq&#nqkgK(o+~>&Pmc!7-G&z(o+~>&Pmc!7-G&z(o+~>&Pmc!7-G&z(o+~>&Pmc!7-G&z(o+~>&Pmc!7-G&z(o+~>x~{`Dn5?hC@O`sVf8P}8;Mz>l*JjoF3x%xNR6&2Ck~Nzu=p9tDW;4~nHHT`Uzfdjo7qU_BK*w=CrV4rom8{teb#Of<>+3P9FVeyFm~7NL&~aRwsruTiTJIp~>oF@jxE_-Qy@O2FY^FN69+L(Ag-q6LraA^Zlr3;ow!l@{0#{`VT$L?wRgRFWvIVZn0<OvyxGG!Vs%(L)vIVZn7Pu-~;HqqatFi^I$`-gPTi~i3j;pn?zX0qaQn0J2hy4Y|GIkR65b<?;65`8ni{t*-RW!majt62_(G<5h9)ev(3*6#(1a=jzaEs&7*j2Q}Esn=xSJ45tI3AB(MJL?icoKFMSKt=MQ?aY)hFcs@$L=8x`wQM{<X~4}$1RTYu#d1K;yN=CCt!cUdyPWeX4p%3QF?JbUJE;mekl84&rugUi!_vJ*kjbk&SEgi!PsLoz|LYQ%Awd}G{(+iB+8N4V>H3eVid|z*kiQBUSgcqTksyEJ$4vv@R^QXMKpF4ytm*zMhtcs9q~CCyNWK@QSjb^_ZU5}qv(pyOzbgwVTaKjpIO*d^uZ1z7N0)sDje8h^v35b>?+*YVL0(Q8@q}`>?n9|!FvoFc1<39&Vw-<TjG1>U>Vmrk_eZ{HM~D{9}yOh*?2?BHFHOY#hfE=?i&*pqkaY1*AU~pmBa@_jQ&@WSPU`Oce&ESVm|M!XXUV%zbM8XmBM142ePjr=J_N(7~&mi^>LlpUtV+eHA{F}!ugb5>jqiIJJPOAIZ-s!GUm1W?W$pxG45MI?3iNot%CSziZS*|k_S`F_uY7dWEpec&fVA7GS-^8Taqnfo?Bwa6!Y2<KTUDlKJTY&e#$M6JK90Ef-l>srX0KAv5edHnVwQMvae;#x$#r?6w4U*tsr(xG5S_P{4~WFdj-jZDdziTY<614+_$?D?Upg;Mvsg>mNCyQv15vP?TDYI_{<$QVb9w|_C`&zgg2g8oAUO{-7MoXceG8p@!1}han-S<r)7-$RuDU;7=5cCewt#8y@KSy6!U#=EQ+y=xo>aJkG70CH_DZcmNCyQv15vP?TDYIIO@&LDR1t(TyAz~oh4j(rUCBT#4?V0b6?*=rKx4ixiLAZnPrUoK2GeIV)U(o_-TqU_6m{*Q_S~m`F2CgnETfMng*6J=f=c_)-lg5v15vP?TDYIc>hfU`X232OLn=o3Gw0qJ^PM76CUrs>FMOulG<Uh*0bIj9;5zaWM4y!^FB^|FvRHp<0KYC%=Oz(tr-^cdHcLjBP{0iT5)}N%=19@HN-rh#0Nu6`gb)uwM=d@W25x?=exa+d{rioeRiY59#AW&PQk@qa-BL!@-NSJk*Ge^Y1*e)`n*Ajylj5DMD;~Fh!q`I(@}^W)yNJVM}Jf!f9N>Ir5eSxEH_Twx;9xowDi?Vk<Nk3%9MKFm#MuzYNSy8YC4jxL-j>EXh$}(L&s??nr<nTpHVkSUw!$!m*zinC*o<FmFd?s4ACFCvxi*rm`A?;<j9a(i0m|fvQSFBW3IfrV7WwVB(fvY$8m*>D`w+pUnTZ~H5HAc|0?l6SYOdN=0_#@3D)<!(Y@5K_av($H#H5ZsYt*5BYvgdO(kmnZ^J|CE3$+7644LVU1Ue3kM?C^KgbQyxQGw5?o?;_b7k^RkFS!Zy#JB+aD#GrlW(;$yh-m$TK5vSUFOdT%dZUK58apYVe^KiQvS9=`NzMuOCmcWeaaIYSIovKPtdli+ZT;fo}mA#?mr!;9H2UwA63r}t^1WtohpAG_%czU`%-;c_tzRMSDKzHQa}E5l_Ii3`GES8t}n79(x*H@+p=z7G)}oe`5@v6I2Xv%7Gy}P_k8P(dt{-!>G*WTTcdL&t@W8ANgjNnz5KJZTB3I7zLWzAv$jdg&*aE8jz1)c?1=O!H*j1r8>ier`>JkVG*0<|{;RtGBA!qk%#W()ht_&aQK}l78m-2x8>rBIsXnds@j*M3{!{bSGk5M(M0O|#P+!vZMRr8`lpAPY*6oYNDK{t|XsvhswLm_xAWrg~jFG60)4oK`Iod}#SU0wU*7}vL!{pQV)sW{U9+X6OC<p9mcS|1~9xazHzaWY1i1aBpa9lAPr`$mMs%~F2PWgcTtGfT9amoSAkE-W~*7~<Y<J9@*>Z;Aoq$whOTI<<sjwl6L(^Y?qhZT_>$^q1ubbXN>kv`=H+Lv|vqHz%)=;uwe?jjvpYpPFmXx&3NCeWdEuco6AJF1Z#Iv!H@(703*mueIjt&vEF)`jX<(+Spy>Wg$}jjH)06Msl8_$NOdw9kcFY2V;#qJ5@xnfB>Z)u&N_f9HQ~qK)&<q*~$s0JYes@Hsxdf^YEg9sGcgpWs(~`~es7VPm!M@wxWbAGGm{xX(BEe=WwK7W4v!&n{3C>OvoseV_-_fhcgGbU+-`hX&wA=>``xgv%ibWfCMpV`vIqlwRly&7dWup-clAT0k2ZjB+rfLThLb!%+^0fzS>*!bp@OVJJjH42(s|zirnUY|ss5H%Nyopr`i9*Hjn}-J!SkEwmXh8DhZ>Gf~cj3~)j`<f6=lY)AkP<fF`oJV=HVC`4HZSAqonp%`T`%z=I|2<D@l4|8Dv41+}|7eT4^`P>qeOJD(vf-$fh<#M<R#z9w@fN}z?go!W>)}vext6>Uc!X}iP;A)r-S+E7=7T5qe;DhZbx5HML1qE;;${S&a_Pw~9QQi!@zz-#G8_L^YH_U@_*pG5Q+zMr|816!O7u*gDVJX~$@*X$<%U}f@MtK+x!77*pYf!F%2VgB+3y-0E3?71OU^6Hv6*vkT;W~H%<r7c=+u(Y58s*dQ6x;wi;dzwL!?SP`?12|iz6dYCEwB$xqC5#N!(O-(-az>Vyb5=~-S7^|ci<EpgnQvVl<&b?a39<cAEEpRK7a>d9UMV<1U`X>;c@s9<(Kd;cobCl8s*pU1ysV5a1P};I19(%890yfJbVk!!EyKz<&W?^oPd|$XOus~1$YHshu=~D4!^)_@Fx6)@-O%ePQ$yv*lB$J32(#uP=mdVPhcOy$50z(ZB~<=fk)soID^kRtVc#8?}hEdWd2<n5xzg2c^|rKWLSJ^z)LABhK&h}3tw23a-(xxSp4A~5BGJs(#`PWW*BW&5c`H0eXAgT8e)vGlEiC>F;|r&Z$f<C#KB=PxA|JX0bw!st>)g;OE8b?o1=0t5B&2-J#RYZdDeA!U5K3^<~1er8e+~3;=dv8xaO=^t}{yRxMsE`oKSwsn{f9e%edX{1Ku4UWLm}rt0sFteBEam|Kh$r<=BP%NN`0Y80V@a^O|CerIN&DiZNG}ByXk|Yf(w+VhIoWG|e*RbB*bjY#H-dzP-$8guO<XbA#A1#hiP@PgA_OS#Rm$sdRo0+iL~8qS{Mkx93>K!%~0s`diMkj9b*b)%)3di!9?UTi;9J>!}EEMI;#KswDH8VvMDd#AS*xR|?6SDdyjEC3UfcC3l)-%;!4pb6LhbmRG*-VuZa$m~(^JF~yvF#7|Sa`KdCgdD}tqOE11yX$9ARXu5PheWqpn&iOu)blZH(c*Hj!dsoh0Wf?#5KwB^WTqpuu841R@D#^U27-LaLT&5UvrI5UtVyuNi>S75WySk@k%;)-S^yQW@kHuNzN67$7MwoMh*fGVNd&Eyu%-0+<W(<(|^`=&^D{8m&WZ5jscv$K}Nx5^SW!$1}v~+CQM$351)(kKI+$;iI841R@6f&<V##j^*mnp_vDI{;Em|r_g>S77sv!J78%;(zr)Gv}%%wy@$sL}{aMwoMh*fGVNd&EyujGUIf-Y`U7bGET+1wZt}QK`{mMV9eLd$vj^cCNFGpBR`Tz31Cz8Q-d|;MdSZf-57zIF~}^HN_Z<LgF&Tm@9?k%@kuT6jB#U_|5!i%b3qKtNcgFD(10FUHzaDmW(jx2C-v`IroU4rr70rP-@a+82>JiCA{arUTI{jLd&@3@a0m2#j7pjx|LT*n||J88BcDM!>?6}1Xo6aaV~|-Yl<-zg~VlwF;@!7n<>UxD5Nfy@Ux4$TE={?_1D(4jCm}JroAE=V95w`ZV)@Bm~)T#X^IaG&XSf6NRy9tSYrv#Odc)`YdP66o<5|LbpE9R%Xn?;SG=3=nQs}}A8qKpeeTjoaAhPI=c*+0nqrJaA#s^v%#}j&W{R;E3aN`FJT)`UGUjt_+|bH0=COQsy0#IPj4<a0v15uk_lTdSm|w5@X??H!=DsbK@crp4ylr=-S;nUZjPxFg8)_LBzEH#aQSwO3_@g`ADLpbqM}jLN!8lhXnb#C!ER`fKQ;fN)BzZH%{P&AUT`b|z-4ZNgK3A)qeJo=h%bHp}jj-1Ub8ZkjrkHb&_-Tsyb=<9YC-d(j3i0%pwx!&^J|!%E>4qy)uInv@#jZUqQf|qV!(z5`bYFmeX83V4j5aHXeM5}CRS-W7F~(Ry;x)wlx3);$gt*NPPgu-tt~!tq7IWYB)pTEid0g9HcLnp{as_c;9rHZvI=n8#P7w2&l6eg==LYfL5Yx}5)8hxp?Oaz%JDRkV_tqJ$edqP5?JekcU*#`v>?OZ_<P+(o;#ML0RA+7Di_(VcJIc19Z9?>^&KnP3EwxIN<s+Z84biWDo$R`8!{od*?Lzd!=qN@ybR6eWjOL=_=(B3%Gabj+RioJHIOb3_%3(l938xd7OCfV9)#su*mtJ3N9S3Tp7{n_RA7mpR=s4w!h)Yp_=E|E^E|)&>S4wlH%+<!T2OX9uPaa)1P)>j6XDKD`b&1-c`%=!_m)u0Qy%Z-;v41VJL;3Sex0|KXt4GVH&s-GRp}gYw;Oc4e#fNLiB0FL96{4@``l4~lL-a@0{Sl2*PGY>O9<OMe@)Pr^>iHD$mg-==RJ~pz4!>48OMSY*N~NvuP>8;W&viBoQ=4@EOZniFBNE-0>Qf!cNgS7r#wjPM4%(M>`y$>_9m-G2y>ENWk)M2HmNc!#F6pfs1J{pld^AL#a&OhglVteqtn}oTjY2yi9Ny4VzTpPDyt2)8LOYauuZ(|Edho4G`A&AT&<^D!$Nai_eoei|P8fZK=qtLuXgq|g8+xj`KcaEURg72F;}wllequgVJ)fd+td~ma7361}G+nJ2G+Ehn{L2s?iu4CWC#jvMy`VI=H4fpY$c{)K$7M1un~kG=nb;3<RWvT*XP=+4<;s*v(no)slw6%>RsA+XoA-p=zB+rf-0_`vrDHiShVYQuq5GD1>?+TGwX3|i!|@OvitIeMU6meaHc8Hf;~_j0+2MY*964J)ao=%?@>66djJ`tjgS-`uqdzL~C&*jTIL51zc!RtZjblDllFuM-={VL)CG|4oHsxX09y8Qm_l;A|ZvQ-FU#d^}`Af+l_1CPE%2x+22<?dUDQ|IHHXEnBMf<XDUo=j+O8F_`v-iL}*?()Pw7h$P)NNkX?@V?bo)^MHb?g*5_2&!H@xxgmcIdv8hlft}l%Y$ae4xpAp&iP@!|6{-zdSojPJVZg&`x!JPV_C7H%v$s+6kkt5Pe107mZWiqCcwck7%6o7UNa*ctzusx0p{=&!>pbR0r#&>h%(FIA(9L>fc|c{DrotKIP=1pQfriUj12F@AZb*q5F#TDOYh^HXEm0Mf<XDU&LXmL-|R$*Q!&ge0srEQpv}03e_2Ubg_n)mM1HedwnNPm6KQgB~4h@SrOUk`d$y&ySA?^zuQ)!JQUgK(OQw#-*u&Y)4Y}n<)O$9<)rpIJ1I-$6*XH3?S#=+h<=c_qH**`CH@3?D;lR<#duXcUeP$^C+1Vt^C=pqoWy#mdc7$38huu*KIdJkq<0u9)Nk5hvfB2G-<3TtPf;j8MRr8`I4+ZM*=(Hh6Ya~oebKmxpQpx-k~^nPlH_|EsP*?v)W%(F>#LNLRDa!pc=?x#lhT~qnyPeP%1OF!@2Pd=*AKRkzkjH$N;ygG(0vd0-Y%VNnkYZ`QH)ACDYC=;I^Qr&e&j?KmGV<$Cyc&A^#A6tU>yBXi9bOOi^eftmBbt5Egi>vswAH($!CzaR0r#&l6tA6UMi_C*H^0RQ%+L-fIkZHN86Y3mhMaSsZOB2`nYT~9^j8|Uncg0yrnvnpHzqPb7-AErMgpUOKz5->OB(nOR9+H_3nB{YJPl$l<l0M(tSld?|sK!Y3<VwOIy;iLiVNnr2EdB6f33geM?$?Hb<qLq;}}O+^^ohek%3;HCLrv71;@+uMqtphehM)k3#$ja+r=|yb6g|CGiG1Om#4y3dyG-&#4a9OC|L(<ax!Hzbf-?uBptuV5oly&uiwLR+days;oSl8M3d4=Tx8S;J8G_WutMlFA@8OJf}Ja{Jezczb}7S`sC~r-satlRQj9kBA##h@+RrVsY%iwK7Yu*BA&mV>66+=uaIIc&JEdD#PjG!e(*l*+bJbaC=THywL|ySe<M);J#w9^B0FL9D~W!P!=mviGki);><a1nKj(&Un2uw-3W?W{=TrytsgQgc@|^0>-@p{{JfL4$U0=lWfIkZHN84A#bE;2u0=3r1C8O~Ge{}nXJf}L8pCX>q--r-#o9c-8Om##YraF{wRG;cl?os_PI+aE`be!^y>WFw)Ep|ihRm-6v-wbpr!|8~4CDN&$lSnY-m}s2x%78PM@U0K<I}g;*?l@3SyQe@S?RPPoYxfIitKA)d-xZ)MKDt47eDr{x_~5^7*$4OIdo|MZ+iIF!HJzT?U+Zb(op8H3KKnouTdGaMM~ba4K9X%o`0&^g@ZqxA@eyb1iH~l!EAY|D)&U=FZLRRp+|~pilD1cprf=6Yuh4W_X@BjjjrYXu1bjBJIl%+9z==-=36KJHQPzc;kPQ8xKFaz~2PEzO0}?)?pucwif&SV(2!_BgXsZ40X=4}xqo9TMyQj@y42*-;C|g5I7!MPn9m;ml1}4EYh(;L=?O`fpLT8knp(D(IZ0%P<yFd)&LLS7SjDud<y$0+k?b^KtTwp_K0|yjADI}pxf_Nx~1>i;Lg+!PSOCS|xD)fa#up9=W90)R81uJ1N%E6EZt6?n+M>!mZ!qu=IMxz`JBVhw<f^?MWFc!AJR+x-(GE9K$VJA#SIUT0J4X_)sP-Z~}+yu8k4oZHnhrO^5@=@~NFTDfqghG`3{tgFW9=K7uVGi5__d^-VGVsHF@GvYyxe!X=L3k9FqFf5)@Ca1G3Y05gF+2_`tU|d8mcf&74A!As2W#LNcn+>bc`aN6$KeEQM!6X_!b|WfY(u#Xu7lU$G~9^tM%WG~;Vrls<;}1I-hg*t56V5T3*Lhd;5L-E!L9HSd;<GX?uXmqUvMwXML8D^z-RC^97cH<?t-u2J9r4?LvRSr!H;kh<xzM5zK36+0%ZjpfuG<vP*5uH82kZ$!BZ%of+ql&jXjI<S$G<1vfAtglrO;ZP?trqmr=e9FG79Rh@C=t3SNPRtQmV7<=gN&G+`~+yC~m<H=z}4!#+g$A-oUmSO<0n<r(-GI<n8<Zj^V!rx3%svu{v-17AQ_7R%0~JP&7~7jv)+C@;Xb(1*F%uPA?oAHc~H*zYKRho2#d^<@`PUW7lv%VbuAdGX0uKh~esL0N~@VguM9b{WdcSUom`jbM#YHf9ajFgAuYN7<ZR&PKCz))Hk))|5?PlUQ4nZCPtJnN4NUD5F_>mcg!IUqS{xJF%I}$9kab!8)^CR>0y=#<6Z}7MsKDDDA8#o6Y92c$D$1H}kU+mWVQuxmX!1XUQm&nTIW8i<yK{VkvAXTh7u@rm<AEf~{tQQ4VGU*&22Y8;Nox8_KR`8`)TtW7%-Ffo*2vP>y4x*mZ0>n}~8E8_%w1H?nCcr?Dw)C(B}8P<CO{+0AS(%R!mLX0Th?9V{PZKFemevxBS<Wg*LBcd~ogT$FR!mF#YIA1g*#%!=6k>_Ijk<$PAk9%e_`B9x2R0`@4YU{|5MiY;N4><P9K<w~}UJ;|P7>rk#^tJu@*IJ*|*wQMbWo}FNuP;O%D*-PwIwiV@8wuQaMPO%**cd%{jG~3NGQD(9m*jwy<b_>c|*e>=S`<U%RxsUB(AF+S211Jx$+t?ZQCA$aZJ#0VwoSkKdP#$7;v2WP7>;aSyu*2*;`;i?%d4xU0F0fzNV<;bEkFa0aA51~1u*cb-jM<K%JjPT8wpzC5P(H_=Vl{1bY%idEfj!IW*)FrajPhmnB5Po~+;$S>N%jhBY<rvCgz_f#I%{fcX?qvtyX+0t!q&$2A<7TgJFK;>z3o$!pRx~FJ6p8v3zT25PgqA=jO{CwU$M_vXImHBIh5zv*Q~3pyX||F-?Q&n4_hzWPbhz4Kd@L^Z`*Gue`7zhJ~pTABFc;GcjmCUZ8dBTeE!AaZHczpws?HnY+jpei$WP?t843L>u+m_vZ1ZMEzQ=<_9jciXCs^FdfqVC_8MO2E4t=abp5aBT1$TY>He0nmT}eft=%KRDUo1)eJ+{T6pOAE6<v$RuTPv5*UmEL*FSorT1J9XBEkInO){@37F|myx>k!{zjpi1*DYgyeH_34M+Dd#3Fg=Lk$FwA=vp(;wLJX#rl|X_vyA!mQ~VmU2(UL2%&-3<^O|DOwMe3CJ^1x6Eyu66jQRC7-l$2DU~eRtUmrx~HN~Q9RYcbU@arSW3+}Lt`Slk)GB!toy^&yk{Ro-Y6pOB95Pesie}DeEb3aH{G5>ykUfySsU~eRtUtd7xHN~Rux{JO`%)eiq{!16jn16pe>dnrP;FL%(|Nc3d*A$Ds3oZJ-Ynbo88h#H}^qpAI_hSR!kyH71<O1KXQ^|KeRsB1k>$VM3$@fK7{rjS1T++uW4t!Tovr`QR?ayi0O1=Gwc=hC!&q&n%lk)A#mt&@?*Z*}=66sSPI4=8rmfCa8TS7Zw^d+J%>H4B^8VmX(>;8zw&#bMfc2B6Mu0Pr{#Q!GSu2I$v>8ReBk`m&lNT2&`-`Q2&n%O_Zf03Oq`V!F(#w8j@e`MkhjY~8h^j~(gRa>5JtIn%kL#BTI(ds@Wb=v@S<K0oRNWZ%OskRB~xQh*hcEadOL|@YNMdLIs^hehH5sg!yPpywt-}>F7em$hUM14zIcTAa@bEP_?7L!E!)Mt*9#$2Vgd*~~#$W9o2iReqZzG$4rg8s<5KcexzQaAOs{T}t`p4kfZe^lmU3cD;%z4rM<3iVT@&wXzAa=ChN<#L7kFR~LxUn2U!xJ2XVk4*fbaT$&WK2uZqXKFN-z~^)-|D2BcEYc5r4yfv%aqF>&?1a&mh<-3e(Rko<Ox>SgjH2;D2{$X}cHgHgDaui4EbnJ_Q7S%oMQJfGPo+MK^tsQg9q%ezrp{7nEFwE$^d+Jnj8Qa>{z$~1V2q;i*E4-e`{)%4|J;Gb68OA8;hz^!pGEqC&ma{2Gcr9Ek)1I5UZNk2Q8YefhEK|gU7_&LENG0Paq2(yjgC{_s7|%<pg$DTc`1&9hG2szd;(ksO`s;qn!w<4Xa==V)`A+^9fj+ltOK>74YY%LDC<F8=m?#m5z0nTA38xdXo|8aG=MJ91Dd034vnD~#6fG6{QP+za6o&M?V&9=Apv4g#y|&%hh*rAvMWS`2U4Ir%I<IlNYD>rQN}_~=nn(Hj*_209|Xf75oIE{U<izYz9{>G8%Dqw@S^lW5{!fKkcu)DWS9t(VIazZkOtEr6NaN44ufGj<iKc@qhTmyfe*%_91A10-#?syass5oY?uR6P)^bAmRtfeP|kp<+V3A`qs)d3D1(KNi!v8x!eUqo`6&5sIr85>EJVqF%W)N~gJP7$Py}n>T9}WL|CZx5un`uZTmYr88LopRD3`z@?e`CtqvXHkcmv!7Yf-L+m9P_Tf%Pc)Z#nLUy|4l02Dlpb!5y##<rdfkcfvu~j*|bD<6UqM>_WK<cEH_m2=<`d12@9Ga39=?@>aMR4#WL$JIdSPHh2IYgaarKz<xM8O;-5t$NkpSri$>!Z%1l)WxFULKG%DehTl>f3UTXRD^2n77d8cLitw&xJA%HM;hT1yS43F1x#60Rg;@9P!~Smxu^wYMtmlf`6k$E*+&2+^uOOM<2iLoDT^-d5etgU@4WEm-+!8+gu1~|w+BUa@A33!$BJA9?B{-KAym#Y`!B`@}b9(=-Si$;S+kgJj64qlGQs*N}SkIMJtk;6iWd-ZC=CN48${M@E&x5`3Tx-<|Zq+nR!`*+1v4j)cIT~)C*4+~RvD@m1aE+wx!MUv9!^?IDV~GTR9oNVb*5|tEVl7Kpk7fS@U<vEFvWoRu@VTsDz1BPyE4cJTOQqSN=cE?<8d}2et6jq%-`B<xu5o>ahR@vI$r5h3U|mGG(V*SIxvb#R?;Q-r5(#elC|JV!T$?9<saU~!EE|g6wS@ItS;cxS_*_=7UTYqU6+ABHugZ+gHhJPzHH7%{4>~9u-&D{<h+q40f`$*)ZY#vyo?mZ@+okUh+7#j6la465Z)UjU>Q5CB)@^=u|Fc4@`}R`#!$Pdb7!K>X;x<KC&pG!^gz5K{;_Kzf`5En$2lk#+w(eLaE8hId>fdR)b4U~UmDDn&-T5IZ)z?(EY*sElR;G&d!|13XItJtC>*T3yW;<p5{*xg-({c1!HS)RnrhN5_Z9TkoFP@S_Ix8kLS3QU8NGV-L%2c2K?Y^&F((IZ`WRZRt9hvGFjpJN0os0M^6Q6^%c(mCxdDxac%Fte?6q^4pVwcG^<l8kJs{cS&kS8zxPWhmFvPx?qvQxcAZ<p3l+a^y@MRvmIt3*FoN6|R?qw4<9nu^9TUX{cftm)W;*=my-9%<ZF?@F|eBK?}PYN`J^bzEwAB2}g}71^m?>w)P%N>BeXQx@3?qc0QvARk2I=#NbN335X;F5&~Nd;X3b`SmHaEAIDwrA$?q$n%fHX!WQ2(z-tu6D9xD_<L`?ya}qv4&SH!hjG&MAxnh(p?1RPt3+Sb^+n^9C+Lr=`y(31cvTW_kQ)Qzrl|H#JC*0|{ZOJD5b3|R`!D69|7GRs0|P=hAhJU_!13nyK2bI=^T{GRVe}=UALNW^9Q~1rKS9oj#zlNMKP6kP{pYF24|n}Gr0xfQUL?Ef57YGNzN|$Z+0&=B)U?sWkh+WPROdsz{gb5r{THbsJ7M%yq95dmX#9?hZ1uW}rylpW`!<9pqH&B@CGiHiAuk!HemuQG={o%biE==sf7j*TD&xQYS-HN@8^QsR9m)ai+RaV1)jyt}B8%*V(U*vRkTarj^hYNC1UVxb7x97q?hEAr)u%eN?o^-FTBILFN2NMO<FxKnhmO;lQXN`5kq)gF)vx}$I7amiqazvV&~aL?YCg-vXHtu*`vJ9s*7%_J1B!w=_|WeM#Q$1#KcG6e-CDaJ&}n!G9>K@spy1;PIEIgB;W$2Cgjeu!5;aca-}zsUY2&Zpwu1kk2GRY1`1jrIDD4m%=6*oUKt?G;Uude`52z_Vy&?Al;@^@Vf^rB9fcDz`fZF48c*OSuiUS8^q0EBmVeSVcfghzGW<v_}hZ2+}f%^fKqb!GcFc5~q0+jq5@-P?yOHnR`#oGOVR-jw~%e4CeO+q;dR>1_A2G^pz7S?F@1KNyoGh721FcY?*)b9s$J<980n|3~YC(50016&D3a0|*?;3g=9V%UdrAMA#?Fdyzjc_-}E&W9gBc>r#QMX&_!MR_mW4OhW(xF6;HaG!QpqID?O!Go|G*2AMHABBhEYS;u7C@TW@1FA$>36H^6*bYykd=gaH0XM?aDEYmCcEKKa9_91!4BQO2!3mTn;5oPz_QT64UxpXp4mhaY73fuXNjo3@I?C7KH8=!^;SH2;z$xvnL`P5_fj41SvmFvSS8RxnzpzOn=bsI6>s~7*avs|dpX)u#6mR@?q(siE8{)ImWQm-g4~qlmjSaDGGjRUd5bM4L&SM*5J;rcY&sE^Ox*^tc9ymX5i1%*1Q6lGfO|f&=7KxlsHpP#eS}Bq9)u#CHyS|9<<70+N<b1m+ey<=|BIolh<G}e|Q>@PwIG=2a^;iPut4*<<E2~(qMc{n9Db{NpIG=Bd4=>v-k#oGJxJJ@;iJVV1#XojiEs^uprZ~Z!6A^CJG)*Gs+fA{u#x9Zb`Id3ue6K0i=L(!pHpO}@f%Da-SkIMJtk)uNzTFh-wGN!mH^rylJ1CKJyr#I(pxqKVpKOX7E?6g#^VO!f#`PHyVffW9k@M}Qxb#FziJZ^3j05L;O|d>#;C!+v)?*2ruQtVcuB>9c7J>8ardY3a;C#L*{ypi4M9vi(;&$o#C361R5O;fiy+qDq8{*e~oM4JS|Dc0J&Z`^ZaWQ{+$@%%PIB?$B5bHJr=bsI+?pxqIwjtJI42Shx1<tD*Vm;@9^Yezd+BsyIoI^G}?@jgpyU%;a*UM8w&dvUPu3jbQ>i@qw?@janPtJRXtK<K~d2d=%(fEJPd;jOW_kYfN|KC6FeMd&NOwI%U+vmMScK)Z%d!L_@t&;QbL7s@l|8w5^pP%=p9I$fUo9h2}pZBJ9uXe6pCFkn@pFi)t`Kb&1dQADq4}W^Y;Th*A$#Pea!r_GFljTF68m9PI%{pN*x9Myd6&7>fcBIu0i`#de7}OWxf!ikp=M9H-|3#SF)bn73#~tmUaNlzKe(1G|`?#jc(Z!!z#+|!m$X$Q<BO?64vHFr#%;(Bl-NG{Fu_(8+v5ZH2oF3fQ3ZDGU*r0D#u^zh>%;(Z`Ylc7ny@wXd=>=a}#@mah$X`A7t!2FI+o|%+4MB<opY9!H8S}aR$ZTR6^H^%HXl@yQzIS|ZUn}^JE7F6$S;cznRxqDS&#f8e_ipB~47<!Gg~Kl|og^>0Ej&(sW|I71ubQS<X<R!j<~A?vsuLD--?};KhQ;^pm>AR-;ndL+gY$;Ny8j}~ZR&Y2!pVJ~ltx~&RT?`#OATO!WBPvhX!4WN(G#*fZBl)e>Wg$fPI*%5*?7(+@2f;dwxUDklBo_ICqBytc2r^~tWLlmRp5_G;tH!H%AqLF-Flo*-gjLm-M=JL#|p=yoKyY5Jx?f~w3Xyx?W0st{&%DPbH87yVS&DEL0=Zth4>>=eNm05K8aTr)r;x`?5o6|OKKPJUnTxm*H<m*tD>6H8c}^w9Y5VtqE33|DQ~m0*DC>B$+4)8RKH|viMr;`tE5%^k`z%Lf4{Co{d(taZS846Ul!;~qB;_PB#}O?5!EO0N}@Vaoq&CX+ZWX_;J-rr52vpR^c7JZX^p79sE+hE8AY|DI-+`6(2)dlNmg`do(*&^$-jX=m*m`njv|;#5$UuC8`Q!_U8s+bhR|61)=f)%w86i%$G`CL#<*P{pY35TTnks@V-2jt$1+%gkA*NFA0_y=x%d}8z67^dYS&bDfX+}8Wlfwb2D(CRl(nG-bc0?Hg_3{!s3-J>%TQhh^`H+pp%KbP&;VSJ2u)Eoh07rUlA$?D{>`PnAVX`Et)T@-&>z~OYzwU*4LSlt$)KHfUFsDmuYhP64x^z5${x@KM!`6UMHvg-Asr@x1EmAvU?NO~c$D#AhiNbaJSaWjhD^u-FG_wLYc}LTKa~9-1!lo)7>IHpq{5Xj7&@Ws1OuQ5=D`S*BVY&=Lm7-k$**HAg>o2=ay*QI1+W;Vpqv5|U=b{Z43rr#S^G}TOq4TWI;?=z;6v$yELa6=As=Nv<ia{w4|7n?fdaS&{4f;dP$=Ymu9x()LQMKuAtwE7SRCjdg_!iSLQMKuAtwE-5R-m3EY|%OVba?gV(f_|(!*N9q=&VHNe^oo2YNtDnDnrgFzI0}Vba4|!lZ|_jP=;9VA9W;V(f_|(!*N9q=&VHNe^oo2YNtDnDnrgFzI0}Vba4|!lZ|_jP=;9VA9W;V(i5v($5Mp>1TzQ^s`}cpnnu%($5Mp>1TzQ^s_=t`q{8p_g{obZ)=Eg4X=>?OCdd)O8Pj3^jr$*a}9N{k5EVtYosGv(IIomRELfepJf9(DzOt*C*Y4N@JA(ah1C(|5ZBcb>4PMFjV;PQ)yH+XMEX<1THrcgB7KdaKFzs6Ul!Gf_#=z-X<ev3iB}fYj_L&LtHk~#bqx5g68|sJr}Yx(tD^eS8j18p^`iUY+FmC8kxcqr!}?Nv>;+`fw;I+L`wN-$L}vQ3KwlEom-r)z^l9y=K8aTn)tBl7?CX82VSNMsE5!eB`l>)*5!IL0i0X^#NY7=7YDaZM^|GKN3FeZl=+HbH=v<P21Ai{bxdk0XFqb0Iv0?Ap1|Kc4yKRR3Y(sq1$F8?7cDOctw9&>J;&wB9+OW%=iydtV_OJ`_u>?EaW!TZK!N=A3w`=h)e0&*hFVucR2(ZKLg0c(toBVDL-BI%2O{#+(ZXC)u>^}MZ9qih5FR|F&Ho{)B0X`kr-8RMUl3(}Y*6#g~f-(iW&lcF>rlL&6?vr2VG63ZO>^|FJhuaBdC+t2uU_U(!<uL4Z`4ukwYM0U2>vqL{nqOx!4tw2R*iTPFISG5+-q>GHML89FT^IJ#Gf>XJUN;f@=^T_f*z5A^T=>;4dD!d9*iX+!IU9T3{@7m+MmZRJ-67cF&O<p5d)<-P;g+E+!(Mj`cDUsz%dyv;fF15)l#8*~os1psQj|-v*PV_X?sAm;_muc=J*`H$8hhPb>~PnjT#LPK0d~0SQLe{cw-7sAKT1FLy8j13CS>F'}
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
placements=[('l', 'wetland-split-window-hollow-fallen-log-01', (-0.7, 0.45, 0.125)), ('k', 'animal-static-low-ovoid-long-curved-bill-kiwi-01', (1.15, -0.15, 0.125))]
def rigid_point(instance,p):return tuple(p)
def stored_point(p):return tuple(struct.unpack('<f',struct.pack('<f',float(x)))[0]for x in p)
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[stored_point(add(p,t))for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,rotation_z_degrees=0,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values()),coordinate_storage='Exact IEEE754 float32 after translation, not hidden deformation; native versus final GLB bound unchanged2e-7'))
base_mat=len(PALETTE);PALETTE.append(('SceneOnly_DryWoodlandEarth',(.27,.245,.17,1),.98,0))
v=[(x,y,z)for z in[0,GROUND]for y in[-1.65,1.65]for x in[-2.2,2.2]];f=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];emit('SceneOnly_ContinuousFloor',v,f,base_mat,'Single scene-only flat court support, no extra counted model');FEET=['SceneOnly_ContinuousFloor']
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
  assert -2.2<bb[i][0][0]<bb[i][0][1]<2.2 and -1.65<bb[i][1][0]<bb[i][1][1]<1.65
 for a,b in itertools.combinations(names,2):assert any(bb[a][j][1]<bb[b][j][0]or bb[b][j][1]<bb[a][j][0]for j in[0,1]),('Whole instances intersect',a,b)
 contacts={};floor=triangles_of(FEET,vertices)
 for k in names:
  tri=triangles_of(names[k],vertices);mask=READER['np'].max(abs(tri[:,:,2]-GROUND),axis=1)<=tol;bottom=tri[mask];norms,areas=READER['normals_and_areas'](bottom);expected=float(areas[norms[:,2]<-.99].sum());report=READER['actual_opposed_face_contact'](bottom,floor,plane_tolerance=tol);assert expected>1e-5 and abs(report['actual_contact_area_m2']-expected)<2e-7;contacts[k]=dict(complete_ground_contact_area_m2=expected,actual=report)
 tris=triangles_of([n for nn in names.values()for n in nn],vertices);rays=[]
 p=(-2.0,-1.50,GROUND+.25);d=(1,0,0);length=4.0;assert not ray_hits(tris,p,d,length);rays.append(dict(origin_m=p,direction=d,length_m=length))
 return dict(instance_bounds_m=bb,complete_instance_count=2,distinct_old_models=2,new_reusable_model_count=0,whole_oriented_triangles_and_pbr_retained_before_float32_translation=True,actual_full_base_contacts=contacts,selected_visual_clearance_rays=rays,not_navigation_or_full_space_proof=True)
LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate(vertices);result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,.60);ORTHO=5.8;WIRE_THICKNESS=.0006
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
root=bpy.data.objects.new('OneWholeKiwiLogGroundMargin',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole scene horizontal centre; continuous bed bottom at Z0; two entire unit-scale original instances';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
 d={'id':ASSET,'version':VERSION,'category':'scenes','assetKind':'scene','theme':'nature','style':'source-preserved-faceted-natural-ecology','title':TITLE,'description':DESCRIPTION,
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
