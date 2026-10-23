"""Original hollow-log shallow sidepool wetland composition, three complete existing models and zero new reusable models. Lightweight maker SELF_REVIEW; no growth simulation."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='wetland-hollow-log-shallow-sidepool-scene-01';VERSION='1.0.0';TITLE='Hollow-Log Shallow Sidepool'
DESCRIPTION='One static wetland shallow-sidepool scene, one scene and zero new independent models. A complete original low sloped bank-access earth module faces one connected shallow opaque sidepool. A whole qualified irregular hollow fallen log stands on the dry right margin at an exact rigid minus90-degree Z rotation, with its side opening directed toward the sidepool and its two true end mouths unchanged. A complete original reed-sedge clump sits on the separate dry rear shoulder clear of both original pieces. All three whole source models retain every triangle and original per-face opaque PBR without scaling, trimming, recolouring, recapping, adding leaves or changing hollows; only unit rigid placement and collision-safe names differ. New scene-only bed, low dry margin with real pool cutout, and a bed-filled shallow water volume define the sidepool. No bridge, dock, viewing platform, walking-route, fishing gear, people or texture. This is not the old log crossing or twin mangrove observation scene: the log lies along one margin and faces open water rather than spanning it. The rejected undercut-bank candidate is NOT used. Static stylised habitat association only, no water flow, species/ecology, habitat suitability, erosion, physics, navigation, safety or structural-load claim. Normals are recomputed flat, not original custom NORMAL-byte preservation.'
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
LOCK={'nature-bank-access-transition-01': {'bytes': 5220, 'sha256': 'eee911abf6fda11593a2f0a3ca62fe82484e3dbb4dfdadf6848cbc3c82a2dc29'}, 'wetland-split-window-hollow-fallen-log-01': {'bytes': 27920, 'sha256': '9cf21f04b7be932f0846d33aace58ddfa88f63eb0c2e1a6edfac68eeec14dddb'}, 'nature-reed-sedge-01': {'bytes': 35680, 'sha256': 'e491048482af1abacc8d0e9d773840f3139863d2a17e8dece5cd1aea4b3ef9ae'}}
ENCODED={'nature-bank-access-transition-01': 'c-pmBO>7%g5Pl^oP17`OX&dMtGMfuXw)=ke*Gjy!g^GkUK}l5(Z4YaEW1BkbuwJ*MAyQO0ap@72J4i?fi6W#TL`^I4C$(29gv6=h1Q#xxkeK)Et#>!^+Nr4z&iBUi&6{s#b{rQgXHP$c5Gou%Xnh2s>4mx3RmrN=Y){IpN=4hTUCXPwQbu~c<W`+(El~tY;$+2k3bvb=IzE@UET>so)}*9#*>-E?ssqk6jit4uRLesEDT7<6CS}gAN{+PzHfce8mXw@oL41HOu3c=OR;4AoRua^fzhilI*G}au=Tgeb=j~c8<++wqD|>Kd3KNObmn_eA%T}csqEM~pD)vITU>Br}=hp2<!9<jtRpSXP=iD>4XH_cY{Cu@uEJ2<%E}nmUs#>YKr>(pw!Fik}8Wu02={jKslapYhhIlEI5tZsP1sm3yHk}fpt5{W&glE^f#t#VMT>r*LwzMHPsX7F~8d+OQc2$zEdnwy;z0wxtP`xFG7!(`SfXv~qcrjUKvJMGwg>uskD~5_?RaTy?nk)8Ws%d3O4INWPsc4SUl%vX&X_PQ-!p)RaIBT-3$WK;H!Cgst)#WW}VWGz8h6;%@wP}+XRtS+bg^Ou*P$LRe6pd;9h!M<MDg2zC1Q7|*jx^lOWw_-fc<3&-+$_&?%elH|3oUQVEli!Anwu4O&d$xBIWZ$;2&{s#Qz+-T4{blC;KU2qDFSOpkb@DFU<48uL2XCSf)Vs!1R58?2&llp5QGF{ur;y0ntQ40HY<~>FD}~dxw3slR3l$qTCO^_<DFeuhQca@s@zz2yjDW*0E;AX67xQkVU3<o@nedlwaA762Tuf%&b@kyNnAkiGSc<3I5ypk%^tByo4#=B#LS8L4FOpE^$Z8ZrWGZ!f%+9McfUQ3uEeW{ZP7)&8h<|twtBOb71E!^t^K8|imn@qY$Q`St+r^grs_;1YL|*=-7|`#>;2Ayv6YHM=K<uh$OMEdv|+<P#`A*vs}LbuE)itZju2cIVpZf;JbT7=itrVffz>b0bBl}OzcN0*mRsbI$%abX$#kXibFW+$;X*&cWEM-tVK$}uR<4e)Vf1@v6Rby6%X;sbQxesUl`T|lBb{orkD|+ZU%4w(?k9Im#{CRTv~a9F^{t5yw#_goe2FF!iJx{LbaHAIewC~@Q1i9!<Bx9KXk55{_qK2M@#OG>#!DBjXMMYm7Z?8k-ntoxWBPGgCjXBA9dASYm(>6ogugrBeLGkN01p5f1k2O#zL`cJU%y+Q+zj8pH<NAZ=6J+xY6;`E#?E!~V{&}p^B=RkhEeR-Hm=To9F7_LGRtco#eOfk^~J{ly&)XXZU*#*a6o&c*CM<b?o}sy8&7<FRN&=H(~Vy2;h1eaiZxNgd%v$Xg4|B_PH`?h92e*PpS}{}cCtq_njN&8o81?T*^7OfnD=Ao2s(sziuoUbN#Bn4pkX*agLb1`=pfn)=Y8lX+7Hjb5cm%PZxB6)#(*^jY|b49_6QmU_8#yb2JQi1A4Jc>X&*Wa?D*%RiKBDg2@gLQ&%z8fI^pP?_kuZh{?_x2Ada7BA0srREt}W2eUS~~#6J%wU!J~d{<~MrMtz{qe7-jL`1Zfv{$S$f&38?E`*=@rg8tX;{`T#gr&rD75vilSQ_ex30q8P<PV&7s0zDjsxfp^j?}EPWfR6J%_p;x5=~vuN^Kqvh#o^8NTQ7U*=Z{~^Rwhd3dy_w8gZRT2?qrJ#B~u=s%)bBYXA`6MubR7$&-CPz9r<dqac9-^4of}x{5`GRUiqYG9{uL~>}!91cl*$>x6H9$#zH<pd(giVcTn_nC-ih6)YD<n(_Nyc{{gS$_j>', 'wetland-split-window-hollow-fallen-log-01': 'c-rk;cXZUo_P(Nb)4O3YV45-8*K4n4+$g3Q4A>Y0#%0}bfwhfIv*{f|C-f3}3n6q?5<Nf+B-B742_=LUY6v8>-^@BM86{6dKEIdq{&}3UA0L-HqdWJ0(vC*6N=)t9t{4DRP6M!22I$x$wCiw>n9NLjmWS_fk3@UA-4T<O;qdVF=#=EhNYBXBB$6hYz*KvByxpM*X%ng$V)Qn68!aAQ9z*Po%;b!8;;i@9dW`h)$c!T$c=&36W0@YlQNumbW73GtqlfGNygbq~;$8ot>o>CBAO9NeVb9HS#AMPa;xf_(Wu)8Fv!WdtskCWmx?Mw!srD>N($np6S@w8MTxv!p`70?SH8mqglarAVuStu^vOAJvQZ<=L_S94_O-^!Fk|rxBL*s}^OeDT!6q>Y*?5w0rO$?zK>1=<Q$?^8qImzkqq_>Pg_VncRL^`N6duEbrOur2zf*jBu;&9j#vr}Un9b89`AP4V34@nx30VE}-#yjjJF;QAF#y>{pN_2E`Jn1FJo|Q^MXq`DIH970IqqZ&_O6!D}RFd!3sTql_wK|fr1X78t==fv@iL)@@ts{v!Gb<)5IWBrga%Of+YIH_=>QE2gEJwE8%Ok^)oS2**9UqgGokqN=QIkW%CdqOn4<o&i6vbv_r^jb%NLjKRc0WzLJvBL&R^OgFRFjYzlcmX~C8tTzWM(;%2Wg0@kJe99c-ViXy)af+_DM(%mrSBbPRWqth^9P-_w|U0j~SGeJjCAD!<V{e+PyS=3yYkYoJErSZ|xb5XqPtR|2Z@+)t(t0Z%@xi&Xo6OPbVXGnfiJJMFw?l+oP`swP(gq-MG5Z>3ygrE6HJxiFa9y%)g`4$l(gxw+rdrHn_0)kYsyKbZX2{GAQP#QLe-G8%gEyn<|J#3#HJ`l@KZj4=V6~DY8)H@fq2%srDWur}6)))o<;C?e;+t_L!_ByTcwI7~>d7vN<T$(Zx<mm6{wEmXV#9M9wIejACOl?Lir-8IE=&$Mj^4(t7KBw5~rEok?#pSqv60V$&L}^pDx1*IA54labi8rb3(5qSaX~W{bt_rK4f~cAS6pNaXJL*CBtmd0S0|O?^y8y+LoWj-+Z=9#gM$`w)9N9ZXnqe4@RGBhnWh%&Ik-4SJK=heoe6nOvjP>8yIKRd1yOvJ{&1Rv#@1N^dO6cnWjj<D<1$N#_1$IKgBf!S*;JhWHS2&2U5%YQ9Kg(phCkq(d?m7EWujn#oX&rvLAl3WcB}-5ZQPX2ahMD$tQJkjOR0k=8anzP%$RIlYKOG8M+J*BMO~Dl`(l;kO|fh(&MlaY@lqXwq4Hd~^n@p-3Y#$fRu?={m2-RayQ8^Zx5H8I&VAEty`23R}fwk&9Yvc9z{WvTmV0LVAXTc6G(jH8iYCKxYqM9XY+pg*iEn`sn{Smx&Wis!|VzKYB2-J($=YbnolI{6`NKwg(@!2mSkcurj02vR&wOY#)Y^u5aO(IP!m)8IHot#AYWX*d5{I%IC_)?_b9~hYlinHtF<cYRpb2mv=q6rjYJ(>GwHRvYtrTWU*RFom^KS3*lCsnaI#+)EUjxWYlT(KIETf138IJS_`dZGX1J-{qK74YE4=gd`w!MQD-q5%sv*K!AP29xnl7MZyRKAedV$->r}-2zV`Zm*WU1ZdxO>dd;1<i0i6TF{?dct{SjF8MNZnkNx^%v=B*`Xpq`wQW^&;)kPCtj&7;9&CD(18S*O>N(^7B#n=~5#eh}|#ZhC(fbq1fm%cA-H0T@i?_omTIhp9E`^;V0?N`_4@OysJox9GGwl1-D=YW}-45|fTzpRFW^<f3MBrBP3`>ti9`PUQPjZ!qcpCXE&qqj+C?pZDj{WHA0+9<A?>fQafJmZM92J|-Wdf%IV}GZ3xC@^|O3Rz=Y7?Lhbbyy?w<%^Qj7k1p72q3b#rJ2cDQnM^aY$lZWJYxF6!geD}oZk~ukR*WN&QiIWI*8dTYipGT&we2nR)MJ~QwXRDN)7<c$<~lMh{8M`$pCTOoukC52)wkEv(y`60MGD_YE?s|WZ?F{M@PBQuGnkFWB8*>a{!{sM7IJ>5AAw${`*Q?7R-Yn7@YfFXy1(S`eI1zee;NUqWNLl>Jc8d(hu=;GHUfjiU?y{iJ$(TJL%PD$;K9-@(+$*l`caYP753*!Tk@*oul!ew%N~rCejd;UH#!(8K5<T!#+&_c<0-QRmS1c)U8;dC_}GD2y#37x>D7F1JUOWksy9AaYSpwBj-0hc#?M?HExl}Z9X(okP{t#w&yY%Wo{##}+JkCFPLU2QX@ri3EJtrojFCp~i{!st5-#K6&$1;Te|otu<yk)MTZfB(dV8tB@_Uv^($TtI_~hrk#7aNSlJ=RsQ1CDF#8X$tNp;aYw5OO;#<{ZoQk8R0P~h0_RPjX}vGn+oJHA_EkBldLkEKUjeek%gLu7ncUVxNWx;<V!;fSDyAM*^7x@+6w&50>I%UgdRB<Z^P;o5l-h~=>zgQR;^8sT48Z&k&sd=elv?ehrLe0@L_r(<7#Zw0E#?~-vk_VXXKL}!H+GET?t);*X{XcVrB)3MXql`!Y=N}T3_@-Na(3rd{k#L_mMKi555WH}wXGsl7sdT*3*I>!Bjmm&Vh1yy{+v11|^a1EiUdsOkELyw75hPdJB(g!l`E*%$N-Sotr%4%hNTVR2Btc@ANXtSV(+n%2mQ)0~6KH@W;<v8$+SgxQIzED3CEq+}fR+wKEe^YITjF%aDLiDb71=W~(SjK7mGs5Sfh)VkrjrrZx+9;*{CK;zOKPz36|K?eiDo$gjHR_UFz$<YYzpIXY`~@XW$8~Q~Jm2Fxoyc-Ju2NA=QJrTKWSov`U-Ox0RHbdI_?@RE`Qn;KXtL!KRs7q=Z)}(A)y1~aV`QAy71(-|G~kDuD#>`8ee-NW%XYZcih})W_}<Q$w#i%CW3N4R5X<SYu7x&2n=7A{aeA!VN6YgC)+MSqJr>PvVrm^lPLE6Zm}ZCfEAg&LlWea><?y&yb&=&y`s}s!&+$g}!}4VO?U#>iZ6g<>Gq*OX;$pqiD5c;cIyGpeD&DYK0jhqjEI$1rO~&mDkE1E`HJC3~TE-9VK8k*PYQS?l4R)&Gof{lQmsXi@&bi`<<@Y^5L)*uA;*%cZ(V7(}QIp&XxZa38G9EJK6sk1k91;$mlyMq=?DZLFm-}%<V}5+8B1)OKU&d+7wk7v$RYE4K;xuMjquvKWk<<7opWnjYsl@5H7FX`cpA2^sSx(2L4X%ySDrLzy9apL4Q_-=4WvY1dQXOy!+ezfUY>g`3Vop2!)g}(l*5=9h^NYba>rO4)^Gl74AG#2PPcCkS6OQ`}YPi)i7)S2&!q#Pbd6xSuY>OkS*2gV3MIe@^_G*vwW)#Om7A{i7SA=)KYwmr9rkwj&6{llA8#)06UXgP;_BrQ^BWK(y8K-0S>iWGcw`{B`PRCAby`b~Qyb`B*puBNYFF}dZoJ6-Z@hjW35?M~i-YU90nt5Y_jMFh@z8#A$tX`vvuj()fFN!~ls&3mV<Da&kjNb&7#;@;A7C)Xc3wup!h_B8yiMeUh@wE*`+~)i+f#tjR<zaE35nH&;{L5M+@!04__<-0QO*od1lLnQ+{%#9p{M_4IJWl^53h%r_#^)}afZGq9itc>16Onl)e$}un8XK`1WsaGKPYfx=H;Cvj<26Q4a^=bxw2WuDf6GGNymz#~@|L+nG5?@3@7p?1y!><!UUQ)$Li%~))mLM&uKg6W+O|!`y+7z7R$rVTTyz^IeeOR_Y;p1;dUUM6jHk?Z7k{cV5SQ4rPh8idsyOxY5%|!lNxYIh;g(sPd^-T&J*vSS26+j7al_HrhdG$FPn^2IX8pFjIB>>DnGb8P>OIr<#h%uZql^vbS1ay2^VlG1_QNfRwS()=DA#<B^<nMi*PlDP&rX-VMSDe-ANM{ijHv|D_OQMZ%h{a#vMU(vKJZ4^;WJdaRc0h|AMg@QafVAud1HN8`_AZeG_z3xuKiXJ*}NG~wL}|3N8n`LZ5!*OlxNnT^~pTv<nJW3#fRHBlI7Xc^2l$K5RQKCJPflwN_AoV*;=Fr6cff8N{9{iDc6hjVQW;7v`W~$-cu?a7@%0kRad-(uf4LR9lK{C)?cZ<tUv2hEoBtHVrPo9=;jGot(EM3{EMOH%_~Zms`QX)fVHz4P}0fXC^tTDwII|H^At6sSzFIJGrl~I-WjfFXEkuM_A=q?h**5=-hD-#us#*T>WY4^N8oF<E<0I&*3N1`NgJ%4ttrdd8m*c2Rv5aZvDCe5Ab$5n6~S{$uJl9tAf!}N)}O7NQd`#N!S(ul+<+9RN%2#%nkw1v-m~zt^D9UdKItW^DO)ckAGVIH|Gj~e`D-0hghP-o{dl=5s`s@UZZf@_td2_dN9&rSnPHLm)J%}r+OhWH12AgRWjNmUQ9VJazN`;x@9P-KPwd@Xs^I4@%X8CN8rz6b!=yc5g(235&AC!t*tV>{QeEndu{g)S87M_W9TS!8z7OyF#w;!=4eH-VmVef+R3kS3emlq6`1_UdkvCzAb(v~<<ZP8a$C+_i?$7#+8~Mt%ZhB9w8&XMDBi3FrdkYUY^YEd24Fsinu|BNbr+zE+QF|S3xWRyHF7-fzD$GIFvx6~fUog4^vesMX+*UAB=EK_A+HE?&iNAKPwG_X@S61J$-|V#YJ2OlQxzPzJ`770zZOi(wwX0F7nqX>>AuV~ZQ&h6Eb?jbixUf)qEJnn|$m+}1i>(ps&(@3eSu|#z;CW!V?W5p)sm8DSgxXii;+uoRW&W(4t)uS8FNKCRyW;QW)ljT2>yw%LROq#HBtE!vgsi@-ovq{Q)V4y}7%kQnvntk_`^;B((SHx>KP6q}ucU#!Stg;x=-vAkO8K(3tUv4Hf1$C>Z-r4hA8(S?owa{n9@&hghDoU(Mak-}q!T57*5}-eADv|yXGsa+3uSsxva_}R;q_smp8o;y`n!ROdSL6$`YY*y<!nur>dSJrE=u)Ms*6%Bl=82XXQkY-TqzH%or7ZF4jlQ^gW^yU8WU^`4WR^-f~EwUf(Mj_ve1fPD`*B~pggo8*alicIj8_yf?8+|6~PTm1WllaN>Bx?1g&6%%1{;j2>O8!RD<e(31Z-(2GoRLg24~~wa6Ii608etp$^oCjs!bG2WS9|Ae3MzbOsGHfiQw$&=owP1%wj}hn~<JydZ*L1oQ%L&_N`@Nazg)ut0x;{h<$-!53l)#zH?5g&)KbjDrDS0|bc#6TuGt5D2LRQz03Gpf<E8*dEd#1Uf+`!AuwoU7#D}63m5c=ng$#IKkmC6rvy+MiU$jBcU(Ez&L{AU=%q*9E>M89>zdCB)}wslVAcQ!9bWna0X0;6le$O1k+(U3<3wtBRCIcLlz8yMFbbY0?2`3u$16ZSPUZ|AJ!9G533;$#=<6on_w+D!g$z1a0_gNi7*+q5!?n_VG2xx9Rzp4cK84?U>3nyuoGs&TyPR}!XB6pAHo5G2S9{{ump|}JOT${8LWU41W&**SPrY;6v0z)99F_d@CCsypa9mu2Dn7<5}bo|uo<opyaE?V6kFhHf?vZ|@G*P>-xB;5uED3U8*UQ33E#mkm;-wW?u8q$9|X8V@DBU{5*&hi1n<FJI1ESO0l^1wA3lT6;Ss?{@FSdrGw_7q6L<)x;Y)Z*@F_fovv3}MBKQ+Lg9~sOUJ!f%&q)+t!%KoM;b*uC-@vZ~e}!M*I(!dr2)=<=a0~XqZGyMqH7GsLQhIKs^c+g*`B71y`xNy#PEnt;6!m#WQJ+VsdA`7M_Su1&=Lkhz&oAnFJG*91*QHAwwBpA0g@~@<hgz1?XL&NNw60#%_3fgrKP#;vvuna?)`yF_PFvJ<)S|A77IodSsOyJH>wZe>drIqdO6zQU76*%YAL(#~jXH_tqknEL8cPqxOVj2fmOt7XXY2m$A~E<?CT4lE`*<P2yPjl!&{1M}{aWMDD}xP-!!)w~mF!(~WzgJ@v#>9oAUm#-osFSbomgS#o)O~uEjd`pUfz#GL!UL2jQ(w9aVpu_IIC}~E~HEj!T~RvDB9ULJv*4i2ksfT`h;aj$<D?W*tog)Xm)$C`LrCYWIx@zBR{8XD~WSMvY3_Z>&bmz!AyUg*R!!KP9-}V8_Ne@`j$6THjC%_4wJ>BWM|{K%q2RTt=CK6bhAiG_WQz3+t7zLY*^?ei%rR%Qnw;{^mQC=nf(o7IUCQw4Nv$Lt9dc}z)-AYXJeT1dZKXWpjo<;rI(cKY&>`RoD`~l?}JUKjiQ~6t)Z|@C?41sSDFu4$<D?$aQXu0(N%HcrfEYJ?QCqxqmBzJdt0S(1>Ta9osEs<Yz(q^*ccej_Q`S}bN2FN-dvu{&5MyayBk3_GXE|?=I~VsRwZ-pQe@6vi(oA>&n`pe>2(R#C3D*fWNzMoU;{GOu0rPH9t1te+`2lMlQ$#SjLiD$ko$pF1Y420wmZ2WXicy+nQJ#9cLzFxI&uflgv`N>1dU|Q-<;eJSP5FmyxW`H5g>wy%&iUNjv$a=Aemd6$-KKA!FFWU?@Q+49SPETK2Polx)SV4=J^3+-W^6TjLfy$k{Ng}g1yK*pU%T02u6@ue;0B`5J`~E^XWW1ieMC(=hOX2jp|=QKkw=%vYgK4YMcPPSK}|^bY3_8Vr9Jb!aITGbe~dvTWwtDRVx{%bH9U0HSu;I9nW$)4=i1`B5oe{M8@g<r8{$8qZ>~Qh~;$uk}>uoI_VWD<8%(WfB!~g9yUP6>3ni~+fnG3n}IS;_ce{}<&SD@Ehgi1UsF5D1Jx;G;aN`iHEplZ5`EIjQ(!rrqb_P6iq>DfFXME+`cu$&w8~p2vYhUBTA#fMO-T-yaXQbeoN)tn{$Q9YPUoM;#nSlaMG>kvoex)VuZ>H8U0D^Udw$&F8{!24eFZg~&Z{48b;p|yROZ!iI#0GQtB!BHy|0SX`SaVPlK6f-AEbuU{X#7cUPt}Rv8p)DtylPV^i8>BRh;H_Q~U8~Qq6X%IL&RlnjuKL<t?v<)7;vAZH2D2si}(7+zO}l$bL3lP{V0%Z&r>#-;FITs^K)Z_}OICXGMrAPIFte#HZ-<eVM8_y-)GYIe|v6_ff^^{mbE3Pf+=+8mc(GpGpZSjaM#TC#d0cPt;DaB7VLjY`+>#@5?S8uYm7wUdpTC^ghcFRuX%BQx_?5de7A<>JiGi9Vz2<uT)Bn6R7FTQ8G^R!#7=ut`8rh$Z1Xz1Cmka!!fEj%}Ix9T2!^6Mir+ysfTK!md5408cuUEw?<v`yr9v3HJs*0^Vot8xGxpdaGJM>G3m&#prWXT(|lH(xD=K7(x{5l`_@FqMf7TKQ&pVa&xS4mJZ#G^f*MZmqc2T$!&{3*s^WCd*w2S+;_s_Hx2fUu-n_-in%HamkGvA6_u9*X-SF%>om}_nYZt9W%hxZJao2tN`Wyt7$*MSwdH+2>^zc$ARh-5gP_7}GcK1hK4X5#E&1;Afo)nJp?>HUf^3puQWy1wEoUSui6LZlgnJ-jvx{oez{aSRwyQ!##({%>ya|rERqmI+{2hTk}pb46Hf*MZOJvKGu@ExDAsyN-NHo&_KUN*6!O%11ODJyT6!Ry>U;gvXD8#(%6F<haKCt^8W8>zkRE{X|Eka4<KZQAHV$h2{sjMF?!UcCVAu#Q#abnHPP@#sar0jfA1`}e+WQ1cWIRh*994XUBcdmr;^IL$-FhLutA{v~W`IL*)S@D^xW?WuwqPV*KWIRI_RDk-YrG@rJp1!(t#=BhYdN80tF6CLVrQ^o1}(qq4GQIjpTRdKrB)ot!elzI1npoY^ua#Ob!#|N8Sb*kZX-E8`s5_sg*Kwb@}>tIVBy+L_XUZ~=9ea!U54YYfz1*ze5f8A?$0UbHiOBJWNO=&m}2@|@h;xxAdUdAKM1us>c=5|GUJxaFT<<)SS+iJV2qb}Q#Do%4-VVE287<$X8hSS`Zoz)CY^gSb};WW1w&h$ghxW=LyPIKF2(Oh(5QGhB=_dTASaU9)P6e#0#Ep&7H2S`(|p^VdY(LP@k$8L2_3oNJmA&-Stz#olz<77EqJ1q{C@ZlA0d6v_4RA^fodu{;4a=K6Q#`llW!!Epx(|wYk`JO=KoRKn4*I+yPtUxthg~>QwkNx&-F6uG7jf~U%lV>{zq9K<b@+_zOCpDoO)G)wb#_9e^uNigF&kaimET?O{KEsUY_N?z@oUZp~9m+uae)JMqPWM&znzkHWiVBf&N61tDnX{(tS8X016I>td&t5IQ4$8nmj#B8vTW_h!DT~bBAm|J~vPHV|!|)x5^(hEm!%v))Cyn{w1A+Bn?YHyS^1Ir_NE??t5?MZ`|5g65<Sq3rXO+5{KIJc2e-*#6^p{xspoB8~mCysi{k?fIpPqZW`}I!w1cf&qB=ceIIdiu=?GYB7GgmL;1=YNTrvnD#2`x5=)$2DCyi4Tc`MZ|!ti7PvqWw{45^)c78L>X)M;)-8S>lU-ZPEs_KCJ!h_7r|+tMll{_#_!;bFP$sv(8gIwP`9p0!H96Z~BTi*X<XlZA(<F3+vNrfJ02q@s$oPYNA-LT`vZR-#<y0V!F&itiMtn`)Q0~O4x9z=eD^5+g7Q*5hI=oqb(_tY2HzhZL3uGkDo;e4SzvW(}yi2wr%6=0XBEHyW-Wmaf;et+p_+w9=Pgr`RmR;!p@)7>4){--ufC}vHT(QQHOytf7Tv~@9+ijHeBgOOPR(3{RF;hc?W)VYq_Z8!|F}<b3FgpD<5AUJCJAFD(N%+PNZ$NM=E}}@+e~4D(RN>SJE&)q?*vT7{*ogEwPfGS)b2}9~HLjxsN`+7o(_i)`!*hz+#J>{ha5;nA1skQ_B{@C9m_g8r$;~^*{1Jw(U@@KxyoCPgz?f{j>guYe({F{Tx!$Wvh^q{#l=vdAs@hck`qUr8Ya2^w0Wa7QEmq`lm~oC$=f-pY>6rc_nSL`egZxj|9HisB`G>kBKsU)|3Kx^Q-{;VeMv$KCC{!34QI?|E&YRuDViW+bZdq^;gnx%Id|=GgtHR&D~dQO1fozD)w~~f_}-s-I6{*tUqgKb+~YbRj7L|5L-7k#Y*<N^+SZpoo=IBo#JJhWVNT{!)o$ji%x!1-u85Q{+h3-;SU{M1!v9;@dH1*qHbBAyoM))+O{A`v#GJ7ZdspXpORv=BN>v{qP0j#x2(^Fa<#-d+L6-Z5O<rBZdo7J&T6LW6+zgWbOS}j#4GA*G1!Ff!-DY6%1vedO1c`d_{hF~?*`%2?VClmE$g2<uQGq*Og?^FKg-GbvzlRjybfmbK`#d5Hj%55lCD^v&-ah#vp)#H$98yP)`!(k2X8-q(ubE&nI94{>#w9SRwry*CB3o!_)~Yj`mG<t>{9Xg?3^KdlN;@Y2flJ$l^xvGw!+(A($;Dr^H<Up>wmOGC#NMZO^PTjDe8*#DYvek&^9+;+C0A}ucRy1r((!7Av+;cGVfg^(-mtE$vq<s?B*{uc<Cvz+$wV7>DMR3s5eP6zQ$fgEWN%RZ%i2})79RL$HJEf?xE*nVq`w7mYlmk7CJul$F<IQDz;V9p;+5r7?7QYAD<LNwjU);_J4PN|I;=3xc|GJ0^2sG(Hq<F0hu@hmLVmrvTa%a=LPBfwCxB#XxtJj>6X<P>(BaJ88MCb+IJMiju@z@PgZZN|H7^%_-;d13+2km^*L*JGT-5s+hQ3`u2m&{vi>()e#lR0ge7w4Ec0jW*P4C853ZUZm2<x;(<Ezu)95+>;My=L%Du6oZdsrHKh!{F^9M=O)-My4bSu=l$G5p<miF$^O02(<hHEdJ#CzuL75(0&No-psZRadK;uleKDKGK)vbIW^XZ?FU-R8^^uA{)6c18WOKA+wyF6<}Y*Lyr#%gzP1E$d@>QA<dEoQ$7VIwLCSpVg|yx2iCsZa!{wevzQmmen)cHuG{hAv|+1z8ts#vHd9NfBTAy&W{IMahoVDX50EEZ1l@1wF7lqn<3Lbt6{b+>(6Rijs95;E9qHD!%DhU(x;LRmGq{hD<%CX=|o8nO0`z1qndiDsS5{<peb<VQyhvx6KFxO1(bvm&>UJ5Yz?KM6nKG_pccwNS<r!zpb^SJc`$)5L0_l{6~GFZAO<(61Uv)~41g+78T=ubU@%mLYS11!66^@op$2q<P=cXQ3u;1F=s~at)PdR%2H^z5p&rzQUeKFhZ>SIM5D9$=_Jsz}5c+|Jpoadg7~&v-U;=nTGf0Gi1P4MZXbCBhK`;Z_fH$N=Cc#WFfF2w$gy0acfEltOmtd}ICwmSIB{<ZzgM1haCpa7eAqYmoD1xJ)EwqEtFrMIe2!ReT4ki(t1YMvrOoXWfr$Tq=22)@L!5PpKB48%WCO8}VKorb_4+(w<{UI6_LM*{p@PGlZ7?u-U4t9u#Ww46iDoBE4_z2b#Tnnj?2J2uW!HqBo2E!)ULU0RY!3fw2pAh^6@*xkl!A^oZVJwV+9k7Ss9+&`=VLyljMVJQDUAwTSlMmf5ei)7sJO*=Mu4@<eT=H1}^Wh{cA-Du$U@4q|vjoq=3Rnr};3C0`u-dgV{0hM<upTzR*YFL&Z(uWg4Bx{&g7@H4*baB#M}j}XZrBA6;0eJeun+daV|Y&RIXFRppW#=6zrq1H2(RER!MAV}j=*c+xFh6q0*(W41q2IV5uAdOTv_fEl;ysJFQ5!pf%^g~aOdFyxN%jv3s9B&3NAx6t|oUGYI0ZM8r0(Ia@U|P_bq$}^|%JychG>l4mY47=fT|o5AG)1g2r4k?iMuTet_HH$+hBcLo4n++=Z508}2T&;U2+5@a7EMLojg9;3;T16ZaHM+za>#jGPbm6Zmj1;TN!SJogLm+#7fYhzsK0K@eA*E5-$Kr3seiPD3fKE!U1KMLy-Y@?3ka1HlelMXnMT!gVCrk*myA;W}}h33leHb2YdwTqwa%t`1k5>&kT}*qw9d>T}(=9t3-EjW`V##`PrFlWW2?<$7`91jD)JTnjFO>rJpX=f$<=BDpAnQJkLBaecUc1p9Fo&dl}Yq6tQGew;7YpNk<F!(q<G4d7x4#&Z5#02jvv6Ab1`aBAKYrL@PssPB(b+LQmEdasny-u{33eN#%m9Z>Tgs{ieU`|s|BQ~F)Q|K}Y_EdQtX+bF#+i2dz@n%_aF*^i-SZ-$!p<ou`JnZxq`)^mR~?<Z0E%|cP%TcY$EhyT?3Oq6~r@lU_!MCrE}YTkeHzh|TW-Djg+t?i|=$r^mz-cs<|mn&VgCy3Eu^My&n?b72F8^lh|`66r2ZV@Nd{WMsNUUpGreOP<i{5&Z>-?H!8`HRB2mwM@W_)>9EyQWyl{$qZ)G;r6KVw-(?P}ti5X`G)s?lCV$RI=X~-BzkH(*u`iuHji;-!oTQ-fw`|?Ac8rb#lCvJ$<3LK)YFF?Q6QkN-G0fi_qv>k@aEigLmgiv-5ZR)-EUzCN$AY<pQUQH=DJ@O7_scJ*3t3MbSF?GWy^dFNN`SafONVMI}3%^Z(`lznlL7U*zMn>8EW^JKS?NXd5GZA686ya4QObJvkqr-rI*ill`5O^<nL0cjx1__x<_nPqh14u8Wu<tba5D+ly61|8)PKzA4SGFX$%v3>$`DzRbst_>F$kvIjU>&K|d8?q~d{cO&qMi;ww#x}W(M^Q8(820B-|m*ihe%9j?8@D|92SF+#OlrME0XcPKu-eO~UtJnEb|DUwZw;kPm+2gYI|JHGjp31_Vde0O6=5Dvm9F&i1ogF2_HCX4g{m>h`bv!P<_-VJOWUtdB8;=-&g>SKcB1*Vs#?>c=IA>@KSjp};Hy?Lua>!{r)r;?OHV@w(HIMJxH&0;gW4Gqwz{n)=__G-@pXJNC;<a;Y;_@TA$$YN+w8OuCSs8aQ&O)pYYv1%D9S4sXF1|ZIUS#=I%@ExC)>lI6v(YjhaX%lAB-fc;OHVo1EoqORY=}U6p460->~9jYab5vN`=&*SFMZl$pKv#6)Y4f<$<F5dfBFCK=AU!@QjK%H&tfoS!W@EgU=|bu4`@oTDU<{UWWij5b73}=aQ&LC1o@PLY{-EH1Q)<OC=Jb^1;G|j7KT7Bd`R#^m=9%Kzj!O-dJD!-7!HdGE{26r9$G<bg7l3T!(b#Vb-lY`5mW##@FwUDm0a&|SWa*`ECDxY16qPws0?{98defq3Co}g=)geG0M%d=jDb}ISHTLX3VJXRG(im*3*%rl!PW2)R0kuN37VlMjE4!Zmf%`g1GT^cR)SWj<9aW|27()49n=ON@FnOAbzu@rfsF(=!g{C&e!vst!5yZ;bl5_03v7b=uC>nk<kJAA!3@|+a4T$vhJb%xU;O|E!AycP;bZWJAm~J}6Lf$c5C9<rLm(0YAs9Ln><k@UtE62Cc7-mkU;0H6jDk?;4q>ie_VtDch=zWUNH7tSp)YiUaDw5G00W>uBoR!46o`cw7)Wp+q(V=KhjfDJ&<E@g2WbS;AOrpnw3!%|', 'nature-reed-sedge-01': 'c-rlqcUTlj*Y-~}V$J~*q9URq-~?tEV7g0;fQX6_Oduel2uM;yz?^ehbIv)ed1~66bxmtdYYuD9VfCwN_t~v^_O0ES&u{<wUiT7yd+I*t+;w`oXPj#q;uG665da`+48V+%03oeggk`%%r=`WEyZUFl#>XYarADVGr@H#PHtUg^oRpkaEuN-SYmgY16dRXXEx2BbYMDOXT5lg;S5Mc>xYV?S<RmKAc&l7<JYCabXaQG$)$f$%>fbTjH7U9`jk&f~);wL4l4F$xRp*?}fBs*#Ywx(U9!l!(`lRUejMO-<)VR1<ue7+>_&6_>+SQWMJ32isH6c3jTUu;#Mz_Sc)(Nq3v9A8<sTpy96i7`@PWMVnPDrFpQ@W)#k4ukEOiYLgPtJ(%LA|9}Hry>bEv{j5VsdJe=on?&9aY|HgG%}1tJZ0BI$y1?Cyi<Rls`I+R;||<d^9ws^3^Fijh{iK(P}h4o@$G`-`o7BAl*>ve>(mV^EP}d=c`xi3~C>ZIw!~T@3s=3N)M4&T94@1xc>*6(fl4$tNk=8KaHPdf2!X@K7KT;S8M+5y(A{2+qo0X?|syIolfiH=c}c*wcla}o!-yKV4yp+Y~|ZgQR)2jDj&U%kKtcGEa`E*?cIy^TO%L6R!2MeS&oX<>Yy0>^vYrJ`(3Eg`st|l-`h)?<vdG|PO@_+J}RqeTMmHs_Xm?kYw%GUbOy^l{v!LHeJH7EJ*+P;Efb@Y(yPTJCniRxdebpl_K}*<J0U$G^LJr%dU|R?w~X{SWiu^Xv<_|)+#*bA8`dJcd0?okznWgd5|UyQVk{cXpO+dcvP_RxLHlO~AGU&yt)Tw93i>}Q__7rYYz58VRq$hWp<+v@)ocyz-_@X}{hvj&Rz-Z+B0f3FwL3b7uB9cXej9JMjPBjzQrjiO^;Je1liWKcIVmnFy-ijMJw7_MMsEpbB+(}tKb56gzi$^Py+(O(_-cH7{WLxX<-+>=qvbzWR?8zutJ3?Z^adS0U$kmJ<>8Y+pLsfZDUU9#UaR-hYP7yul@C3cJS|Z*eW>~BeDoSUy-?Frji#h4UR>KXZm4y&41)En{%6mBm#+Dr(zSo2)2q@S`K=oUh6aZJrGobF4d^ZWpQ-8e^m3=x(TlZ?UJiAZ3DJ|opjFYcg`RghgWiXRd@S?w^YNkA4wYV~wHlhvk6vi#l~dzK4}hQ6@+6?rXtX{$U%f$N@TGtJEK{VFG+LcOqo#+4p4Wzd7^062d-%J2-QQ2qm&xZ$QUCW2)LPBIK1IDj>#LzxKApy(@il05{}*%gwP6>3mv8uoN28zNpXTWI4-S0Q%sH&0yY$s*wFb3Dr=ibXo@#HEkBUykSL5qPm;BV08K~4+KLeejPESu{wLxQb4y)B#9UY`EeGvN6Q7MC@16BK3Ub^UXYOSwcs}#}e)V}oDkUoXd>j53>Kb_Vp8#eN{1=RmEOU*ycQmy$14|)SLO#1TDV9?NcYJ9bH-}Lnhz4}?b&iOV7`sgy~=_?@$S|0-)h}Ar`Y9C)(ggzL3GzNMZwLG@Jy@)kv=`*yRzLr(07-(~PFjVvmpk-9Le;TLOhOPW<0U!IvNj?2pf_=78o@u&erN@QFCB>)rupDi}?~xYWyDR^wv0QeeQ{yd2XQkKt>BolTZxLJb=_@$vbPat9vQF3jO}ekn@;I@|_tD$Y{;&D;Rg=b!?fdBdD_`yFWAL$k1M~%&&wmv#_-XZaIQUBe4ZVoia|GzCX6t;7T4l!$EbacgfKFwHf&Za^kL8KQ_8t6X0(!lDJ5c}k2=smigFQR=O94OCe><>i2lQ&A`O9hW$0_~$>C6_OujeeUFxT`4Xb>C*s!(?czWo`<<6|o>ix#-!GK=t7vtg&v!Ufx3=W@fy#l*txRz2bJz+ENG7T$2M9+!Vv@kY_F)H{hh-kLL8VWa;oF8{FXrs8eQK}U(l<rf`O_Be6G1d+#$FFqGf96xT!8E6YXZZ}WiNxH7Y7IssOFj_bOEwqWFrX~^#OO@8x#DzRgDLiEI7n3dQcW0x*Z^m9S+QQ4#(F)%^y;!t`XRckO>}7#@k4+qvF-4ix>FX_Q;-HoT#5$cOSdQO79@qM%rouDMKQ!^!eL*p!g<r3(O?Vu4@tw)SfuTNJUQs5JSonE|VJ04*?BuU7dKhEm@y$n%m734z)fIWXBhf?g*7tn~m*4fTr0ns^{!2z4|9)wZEnl~ezaw=&7>ZpxpO8|?BWY2qa9n8cS~IH|^)f}$S7?lXyHZ}}X|^sEMLe=Gp5DV%X7xM`NLS1c_qD<9E4NtHVdFzumy*BsZh@~lm6KRail2jAD5g0cJ8zD}(;U3~fE+IqhFwaP!>pdwtg3uOQXdb&MckiBte&S~XT_Uauv`Ssxa)-@tACP)4=ROaCmr7Jdcn-jBys&jDJRYi7wo0CnkTDgXH}s_toY%n8(!L|q0Fnp)3fuOySt!VqKg4{TXD<Gi?j0#ysnY6!_+uqps&Q6`MPb@<Q}WN@sVS)m7bmFhl|C{sT1pA{Z+lyv0!uAIcFSsErrF_#a^RIVO|~Haba`WWAXbjRgNw17_l05wmc0xXI9VCSk0f&uyJ;VtcEvdR>RJR)w3FQKCGUnVP};eDnJPcgZ9uE9Kjg`C<s*{9~6LEPy>oUU8n=4zzd2)Nzg$(C=XgF0~Ns+oS+g^1|zsaAh>`#G=ys42Eot-JRlT8Km*Oe8`RJmT7W-<gAa(%77QRkeTcA35gh2>a!^|No}Yd%p?E0@h3J3zDYXX-4d{Q36?Z|@We_x@U&EjkjkJO`^s6IOr>+Y^P3pP;6sE3=Kr!mN6sV}{l2DeqE)RaxbwvoEt}6keu3e!Kb?pvKscSc=O<j9{Cv~lXmejQx^whOKw4<&?=s;adP=&e<dF(HC+9De_hUFT0{C<Lm!pm<TH1T+~X}?jrbIJIo`*xeSMcQ43i!2#uw1vNn-6_84Ge+|I?TOu7*kQH8C1i=%%R=rLvFqq@(v@BYoA_;k*$V%#_@mJl9xVDxPwN%Jy;hYM?d6?cycO;kK9$(ZmwjEOn}-VH-}X%6@}f*Hg=-#j7J0m2&0<NPCF0{X9F6w!@oDoFE)YGL*vl`?vnBmCj3=F+$mN4S&sR9TZz&^>Td%z<_1@C}Pn@>P^gTSO_icqwjUP$AhvTZ<l^o_Z!fnJ+R$MFUzQS`_m`yBiy;2f8_*cW{T1F8bkKXf*z2~KH*=cww9C5E2{_#>DE;m^4jU&fKbGhkj5Aot|ld)9#eiM%un4F9jo<1Uw@Oa6jVLSI;ylQ;<B|n!ZRY0PJa}T(fc&t0TTwGe9yJT1uOzh=Do0k|Ze6)*fH%mY0jW^PJO0HX$a=C8OG||Ej+BtD~=CYzvvGiNgz3qqW<~GiaL<=8?u4%THA7r|V70F#`Ououo#-gKS;nXji2#?E-43V~Ua>iGWw=vtxL+=()_>A9RyZP#T2g&!W3l8p|%jLudO%xt{HjK-wHVl*+9Iu9-|FGb@xZ18x3eVcK_PhA{^e$4t^{&|Xb)6NDo;OJ0$#)i7@yFm9()Et{@N&&rE)ShQUE%pL=eTUl`9Zo`!V#~Y`7@U{)tagB<{sy`Y&=@ocw+Ew<EwdrgvV~aFH9DWk8|eoNbggo6Hb?m<F%_zws7W^&PEF_TlU5#zI%0yF{j8>>CuYa#9r3;B@hc=Y&O?!UUV*!TymQ(ZMZkUCU#u5!f4^1rxx185jum>b73hwd{h&&y}Yl}eq!ObFFft$g`><QpRo*Xl39(*@h7_*EquP1KbQBGE>D)Y2V>`QtL^5&<sU1&^WZ|ex!a`sWX;HCxG>D)^1%Eh6;2FW&gHjv*OSYpFx;r*)9>QdXC2HIe*NOXck#5@`OJG~w8Y)#J+k7X85@a(x0;?=u{$ng{!-in4+$?P^Ek{{OyO5fd`^E}%sg_Z2mb8>pF>|2Qg~b$CoY5Gsfn0(7#%h{6CQU@ZA2{G#<S5b9`{_~NUmMJVH|vYRRE7m21T1Je7W{p6OY%uN+ro%8cOe5%_R16tCxEfjywk@dwFs9<-{Q@Na~c}wUfu;R|6ETKY29a@p_*d#B2C&DKhAt-AoR+nJrvt`(Bg1oOhz4Ijh`$DgUl1Tvj(aLM-ew>M`N*`RCotMc(DZT|U$@+spY*4pn&IV42v<Nv8*ytBfdsUpw#M@~U^86rOR=&CKJ{2UnO&ohgVv28VqYNA}pP@X$%_-^Jl;e>C4V6~;rK)Ux8jMOG>NacK)HepTwKxk=<NQo?V&x!k+ZHHA@hPc9#7eBC_sB7H5oxfhq4hh0<Ht7S5mKObsDZpy^CyGf^AJTBd$h{C;A77=;eH)Vop=cOygq8siQdF-x6#KMi*JDYg?#JG=)e3T}g8$ExQy}V-aScMxM86n!sgT$^RpOhsz{G7#QN5e9O2k&w>@z`fkn7LQLbE#pu(MEf@bk$l4M+|r)+RK|RR5ovPc`fM*J>l}X$c75{oYd0D;}6%@nQ;Mkykpcl(O#AZE>QT;ry7#IT)F#PbHd!(IAcY1F1OvkTH!LcSBgBo{p$;}?>-NFv0fGFd-$5;BZccnH~lV_+dek`vfdNl>J((f2aK;2?qAo%igRu|$z_KZ#U1W;<?^Tz-#BDf443zLmX}{QErzddiskaQk>B{y)hI4kxpvf)ReYP#vvF;a$C-H<MhmN!`g6J1xY5SyV{RF11U)qJ_*jWuCJR>{xu46o?=&FG>w8Ka2GC<|C;Q*LW3;fxi=B4!q9ZSjWQ<xGSZxlM>pc%37GAe{G?z6SCXrGPS4suM5|X_f)ZSUNaFH98?dIY?R~PY;wUT;E2`-1d7*8zhRmOqK^K-|M&g7Bw_~c-_IWgD6XyGT_N7&7VcRJ(D&(EYIenYuDti)Ji;c*S~xa_fK5ShK^g{1ws^ZyxFySTt)VKj(*7mvh?O+&`Kk&gXrw&Hvp2NMhb7G|<yF|{jc?0iV-(Ecfx<2+g@>^9jpuGgg{kyjj+^51{P<pRs16!u@k=UaV78?Rm2Wy~I85P6(>+8|mu>8FuK9xr?6C=znb7!WW%fXB5yOb)Pc-P?{Lk4fv2;`lO=QtHYrcC-9(i^8UD#qH*m#TJOq`*oEXx*Rm}xazCJMhm<BJYVE-+ZkKL!?(^$6R+2i>}7|>9+HLMIQ=Nv%Z{YF<a6k<)UeWGE=P=9B3jrGRbAq->)lZ4<)E_o)t$k1^TrNC6wYUAW;d&g43c82l*b15rd)On2~xP&tbtrMo|!A1JW>Il%eVHs*k{{Xg-;cm`(3PAzfLN=y%OG<Z=MzVADyT0&QEKt7)z(6Ph&nwbM~F)a;*(#6fW8F6qn<dot37Q{Y^47KF#GkpEC;Y-+qS6zj|yE9o;98Mcs4p?92UemHldS&sIlBr58Ttc2BeA<6kEl*|<FYF3DGC0-3lcM`kr_+~MMLGBtQC!Sk#&X*vC6blFe3Qu&DJ{b-pO9x|2;8<UG!54Py{8P|w~%A}I(ORRH)y!+t9txL=|M(rW2XI`B3{NmTg<WQ+p5`EFyKQHbz5}9ZEbtPRV<jAbg&bOwDZD{=E^IXjH%+s@)4Q3=gC>|x=9h-v_D~97T=92Q0u`8_h!iyhUJC&R%93}qvJlD!U>-orUZOHy1E}~~<p3Lf54eO2dQ|*G2)MS{8nCy_ljSsHmB6-~#AYXr(V-l0PN+XvY6!DCHR(pBrv)WjP#%G#xWmeB>cs|+O2L%d?ZkMviny5UheX)L64}Nl@wB&LYc{jPAmCr8;^`tqUR}xdJY`krMYiYShGjh_cKQ}idUXqiGdC2b%%n<iADq?i1+l;(jlgIVO_6j?F-SqC`N;2LtPv+HOb6G#E2iEh)^jdiI{rd8W$l-*o$;NHz%hU7b!|JCEEQQ;BjWAcrXeJMtABwB4SxZhftANKXLFQ)HvgG1{I*HY=@j(s3<%(<95~rRexpCFAaCz>rRYb}zA*Z}+hKrwCMY8=WVqPy*W-&bG!hG}TbB$%TFE4lTnowLf|722aT?Nd`W&Jc<5-!iA`l9Wuz47Am);4m`_~FFAPceD!f)L!Ca{IBBG3$r*AT)X=rS`5M8=BXWSwCzptG~0L4bJXAL|i(z7&mv>o)EdffFa_cUX`tUvff^lXe#e~p%RNuuV$s^`Dgp~3-5rRy;O+>(+c7PrPql~>(gsw-YdfT;psQ$MC0n^PKllN{3`KsZ{Ih_$4j3Q)2h|u`s}yUSDxB2mz0^H=IVKUFZPJRPdn!l;oSo(4}+F=#C3yYB7`CAS34T7?b3<VFZ)vB<vtESZ;sfnmLtxWvzh}N=lK-c2guHyJCWzVddY>O1LfsSW%8(yyVbr}4eN*Xa4+|`6j8-rj`~<!X8p4sSPdIz`?4CIH(oE++jz0E7}0BhJW}H>J&Mi34ts}_m1R4dbEe0cC!caR|N1^dW;Ja5WTk%c#@)loBvqPKof1vrq=+1Esq=~q++%NFdC;99B+M;KvPI8&@HJ=Q?YD-Is;=$Ly!Zn-3m0u2L$=R|FwaiwXg*wimD#0cFPZhpi?iN}6zV5qS|{Rjrj<|Dn`_U$a{JpY$>eJTC0;J8=lLwwjlSlgbuOI`GvA5ri+4N^7c<`v<Z9~ltZ(l1v4s4|HOy)+yg2KV^%fG_UvBgwTr561Oky=`eAVD=x!O)Av4VGilrJz7A2B(JG0R6=`DDG}56QUwB_i&+x!TOr_kmL6#V-Tooi!?3?S&WT`3dyTkqcfVqG$1kA}`)Z%$1L)q>#yde-evlCS#}M6f$Y#Ca%wW)4V0OdUfR7N&%RsKd`S4ZcYNps9DR*1wN(W4P6(K9-F6G?Tf9$##0_<%k^RwlAPokRz9Dt%8^}YO`#f+SkJsT>y7op_GP`DZ&1N}YD%E|u|^G<)v$5a8!yiK;mv`~?a?Gby5GF79DMDAxVqP8Y1W}*<XFSb^3{k)IV@$6`NjE%W>(Wa;*R;<fn#LQmKe;_jLW!Xu08ND+2a?BSv{|p(B+Htl<J@F?j*DEfx|vaN#j<K8=I^(BagO`?~Gk#_P=}E%zEJUO)h@dJaP02qWu(udAWshu9?q%nn5}_bjNHRHkapTVNn5Z{XB!@Tia2dxca*EZu&&A;Hfw(|E%VKzn82l?<QZ!*<oh=upZdH`Uyy`LTjEV)(P8^%j%~rDj*+jsu#bW>VR)#pOFqX){EPm60Cf(-a_xMkz%9wiJ{w*Wu6{RJSAOr=g7txd4%=D#(5r&Pbn{dj@l=lx)f@)7oH|0qN40lzXuVsLh<entEAny2buOUh3k{2>FT~-x>z=XIC!SWwI=MAnqN6cJnr?9%cfVrJ@**ph@iz1>z^0z_OiHKp62d-7><jzDKA6C2(qnE7}qna;qAp1Z<|KD$vb@O$p=*%%xs+X!)kawSq-l*tJ!j_p_DnhzZ|h-GPwt<&Ch>cOpf<Xk#m0SDPQ#pHRpf7USc&DKkk(JonK5&C-=s-Xil1Csa559Wc`>#%xW4mUuG`uJdYf0(MM+cvhjL*R+w8Y9z-^|TWenTijc4Tc){#>eUZd^VEe9EN~Ci%_l42g1231SAC|UXy1grgRQcEo|Mq2}dAuoxge9eNeX<%hp6|jw^U^UL#c0<=xm<=$z7$$Z&UrpUV*Siqu}F#>-BHYnNVW3Mdf?@r4VfwRtzKO0QXw6)b$I?+KgH^vFo)MDE|!Y!DPJo1oNWA@BkRs+MV@Bphx_KL%cqDn`^8x8<*j2sY2T_T;@%B?G0zWMpUur*H&wbEp(a~%`e9xjo`;gU$L1!HYU1e<BNtp+6(9X5$$~!F%=UVryKG+8a~ApWP<N}`&aMy4V~5ouv!7Yl;rVG$I7<p2QHvZX-wy}w87<XJoJCfy%)q?9Y#lb2*O#rsdiH9rmg~3hl!Jd7D)IWV8lF#9!`5g0u$tOa3y5{+q|3ufO*cPyeT6LAH^tm#LK-fxC|h>>;Vw~!l{2%N%JXxu@3gyQ%%-^_tLJH=cjVv(+isByZa;{u=F_-rdGGdHWJ&)DX1161#sw1l<2tjiOEPBb^Yk;C4v_EnFp;N*(%inkmCeOBdYVYNl}kikeV+d8!dxtTTuJt4XN#-{{myJT^7BeE?nq5559z8^<ks1`@~cTk%=Y5xd;gd#4_Q82tUh5lxn6hx9!<IMjOr541FwGh`q|h=6CjRUD@kk}Hkb9l_H`YfCs*|j5GQu7K%VT1F?G$KD~GiBY}M<)hFtl6G7(2Na~FBJkKSeAj(vzY@5nHT=Z9CH%}t8V#NB3gCa!p-RUOuYOP4%(CDqIs<SVis@XaY=>WPN($eZ-FaoMS2Im!W)*}iO@SzB`DzS<LH$lb94Y)${fJh|S64#eHFj>y*G`TV>n6PH`xf#eJtE=85-htK+)AhE6Dt@g{)^ZK%T$y&9RRLH9(7mTitS<k%vvL4u6o=;Z8>&1E-a8!j?eU3A?`C1R_wz->cxM#_mzt%KQU+XIeH`_*zT~J{MM-}!A*+v%hHOM@D^={tyUd@eUPGx_Y)w3F2{aNk&<e@Y-Q(F%&U0xFh9X(~9`Oposy;%LpnFjf)b`tST=I640-p;FsOX((&H(mW?-d-*q^2Bp>1IbUmMwyq(>$@#IK=#rMBz<Rl;W=9h;77OW$TwXISoxXe>m@h1pDMn&6=3DxmR!~w>nF-N0B^aIDi$p6EwdUn-lGJ@4Kx+SjxHYZy(V>Jq^&5%pTt&vSPx5&Y!aUp&6S_M+bFVrCZ#&d<JQg*eb)zLUL9U8&rhx2g7AhlbHsA(t8nA5#Spx%i$AG6%vqi{zp^}r@}8$5TtBP_-Q*|ceFFmJl4E~0^Kv(Bbe8x0rXgirLvX>NuJW#`%Sq<OMpkvId}xUC(RiJ1HLSc<ND0P2f7Xz|>DE5kzB~=<hxJh7N&zgcsUu$&3t+Ym>y6d0-dH_P!}?)0yg3vFM-Y^IWjlfclm-O(p&aCcLQoYdLt!WmRiG5OgBw(U+TaAvPz}7GCip-Ns0)5j3+jOyM9@Gm)CYfP3Oc~h2wFfh2#3ZH0v(_YG=NA5gQ8H7c54N#X*UNbOS=_-icp^RDn`2%0f3UUR~g!^5_m!#aDfs~o%Zsj-8{eu2Ji+~P|;p`+ARQ@Ll8)yg@&|OTiUG&ghD$Agq9Ei-JlD^!)n+FE1)YRKqrWSWQc}1=n0w78?vAWq{2W*feh#m!ypGnK|dG*lOPX9z!;bY<6s7igekBPCcqCc2bRNpSOs%oF>HXfFbg)rGTJ4I_E`<<XrHc-MEk@-8uWqg&>4EsF1fT%It+zD&=(RRn|2vb`wWJuFcF5s02ocX%%goK!xC5k(_t*krd`(1K8s)}tcRJf5;lPuw!x2(9~DL=&~`WoTY<na*a0#ehh4A-_Q7d51Q+1|`~+9wD4d1!a2qbbBX|He;4xf-U*Imhf`{+{?!z<q4W7UYcmo1@4Fym>^cjkvLg*b7Lk`FcJ88H4s37gO9S+lOCO8R4Xs=VW+iutbdugxBwA%@|4p-m|?1!IeuS>MsO?V2w!Yw!l_h_$AwA*t)=qtR0JMb1>!$;cf3jivL-h(45j+{_QR1rm^c+>@zL)B1eQ~|l7vZyk0K_18rsZdo^8);AtR2O-p0OW(}qk6~}H9%VAheXs21)^36qo$}GYJ`GOD2hZaQCHL%wL#rb6beIes3YxChW3d@v9wP)RFn28k7}Xns1hoLoM{&w?c<L0NR8^CD#(j=X-xYVP!rS;`6Evx(JrlNpCA;0+M^I;M9pcJaN4IW>VRTU3)Bg9M@gs$>VtM58Er+qQ9slZC8I2qh*D8H8jJ>@k*F`qMWa!FGzbkvlh9Z+1C2lv&}=jcO+nMqLNo_0MN`pyv>MGsi_uE78LdM<q9tf8+J&~E708S>(JsAcpB>0V`}9URv`-4kL)j<|C7?{&WgP7@5KTm5&=8b?hS4r_X`k_E0h)y-qv2>8?XsTsnTIx@RcI0V0WGIpw$naq&_=WqEkj!nK}XO&v>O!{oP_ei0dxZGL5I+3v>zQsC($Kz4qZdX(FJr1okf??b@UKjMQ_j(bRWG!zo5tHIr@ZNqc7-J^cLk4UZ9T%2}Oj@sH9L#C?J#*N(+KeQ79@LK?iA{;zAkP=K%Vd_Bo8sqci9j+KYaoUGCC87tsTB8(l%C&<)z<4()Rfy+<$6BXkozqg@ILU(h>LNN^NBpr`07`VBb<rG)%KVWF%5LJ6UQP(!FHR2CA1WTCs@BGeKp3DpH}p^8vb@DO~2x`MCZE@%Wv@Dg-_ztC6+5Sj{lAy8;8V4<N9EVLDx3GIX?LMx$*&_ZY}bP!^N_ChZqUg#|J7J3SiLW&SaySUOm2|^<6<090feX0p+!BcP(oQ2x7i;?zG3H1e0&<b?~KiVaf_Guur6vBi?f<XwOT{_V|;X;fMCA1NOgb3Otn)c}`bQ6+<jzSNikHEVx-roDo?Y+O--g~Hd_c-(JHMaMDUVHDKwfBBid+!P5-LuKNuh8E6_3XVr&fa^_c=w3$?$xsQekgnIKeG3JAA9eq;obAXyZ6N2`#bEtpTgez7wo-9fcF`G-e>9U{k*!ppAWb9^Vs%&&YAbwW8P<g?fsmsy`O8f_j9E7epZwBS;|6_Qsj5dR!Bvw?-5xxk(P4C*3x*;@Z~nex7>CxFTI$9PersgvKn5zL`ooDG~ONmBF-kP#+EqCW$TraJIOIpSiWYM<;VGp$(19PNIQHR+Z2D@@rk+g{7Sg-+nQDyUOf2b7()DW@rJ4UL{`I#?^}CWs&c{$n{HK*S&c1mmQ$WYO6?NXO7kc6#4MNe#uC0>3j5s*wJHAI`L(g;(Hy*JuOP7+TjD~X+Pv~=P2B&UDD&bxc3&HTpL>ju-a0>&SWbA+8u$Bky%h8QmQ8VePF=jXmpd-AY@3ya7k}ftUCdgQi=R0(7Fmrg@xY$W^4zfo9GkV=%!~8*Xj)I4c)G3RI)A+t*PPP<5AA+MYSmzoP4UeSwfIE6I(YEO;Z_=6y!C;-qG4?=PCrwMuo_$9`yFe@gEt3Y!9QK%#d&Ocd|7nV&5}M&PL)}1d;YxWb>~Ov;>X@L#nllj#4kE;JR#2CO2dnL?5k~j_aGOanYD|s8e8J|C(j^#<1wE9q&DWod7RQtCAS)rBAuO7PiA@KTQ~Vdp`WEf*v+Q+?B4n1h7aoE8|NLZG`#rOVdKc^L%F!YgRz9w@Zvj~y^=0G7IC)WrNnA%iL(sg2oB26brT>z6oVpA7)n5Kp#Nm2E0*_!3eb2#x>6X5(iO{lHI|>ARvt=21*ojNJ5&`aK{ap%7rI)Gu9sEb;i&*s=(;mhr|Z?A23@ZSwUnQ#Ru|mC6THC#>VXzCG+u|U)CMoQ;t49cVtIc_3p(XpAOi$|9*ls&AL>H`kf1R%frfO|kFFa)r0Yfqr0eyek@8dFn$q<kXb#OF6k0$Cw1n0W2I0^F+9~gOMbgz^x*iIx=z2?NOV`7p4P9>!5p=yXbcIe31u@VCx<LZOLl5W)-Jv%mK`*)*P1mC!j;?ouSi0T=66tzxNT%z3APrI=6|$f&^n+~3gaMET{UH~Iz+k$XLDy3uov!zT9J)RL2GR9g7)aN<Cnu1A*DowTFV)23`#r)*XX9JrTjw~Ncw_VGBy`UQW97qHHu2J$1xTUEACzA9GLc-!*`PPZueoK2Ej&HE1xeZe!Z@u>ahq6PHj9i8E{zLcsPV6`L$8TsLqci%@SMYUaebE@a(Z-W{PwQnckzM_@nrdwZ{BR-NmsH-URr59{-=iD#k#{2NMv|vyy<x0ck$wqcSvNhVfe)HP%bB(yGoKO4a0fFU^j1le~R?>7=~*v^|guP9gmW-s&9Sm<%)r)iBMx0?t3xHZk}1?8u?m!7(V|o+HQ`%Swp-%=7X_LrxJGaM-(8AF@H4f&e?CWg;kXjMdQ4;#=B=u+Qc5^hKS|gzfgMd*!^vi7<%Zr@m8wQCT@OL6!YDGZCoGZYZL2#%n-E|-b<EaWD7%$VdAV3@1-A)d43mbzDyUBkG_*OT=o7gzIAS)m_F>C;_cty#>0OQ>yCdXh3rrKE*`RGnAqs-J1KWh&+p<z*Y}Bc5~A^hy%~1%Rkvf}oi5RM+vaGSxHq~Wde@J}@w20B;_;8Ji34hW>&4?sOU{b}RMGg>y`eU7_MxMqszo#|-fx&qymGLM_;gF2yrlds<HC~d<d82KQu}ogIre^x9DR0@$vgi;iPhX4dse(Sro7lHJr^IC(q6t$OftPHSQzv4#cITgv3HA#NojeQ&F%Z3Ee<@{R@@3jF{|IYIt<U;)=K<1(8)^U+NeGLrRoNwN1wuS%%T{a+4L7<$8!(OY%Uw`pBY6e%-L_6H#$!?#+)N<#$PeLAD%0-dNyA4QJB0xv>s{G-brTXa3dp3&W)W(v~EuF_UmEto^~PRT_Y#V>U&meD}Pupi!{kAYLzRa_VTURw&Ze)!rWQ0^Eux+PJEdC$r#YzdRF6w#$>wNUgM61d6-v|SEowlF#IuSow%{F6J}={ccu-F9kyPKm{Qbg&OH5?3GHx|8-v9H>k7;4v51@=hU=Hj7C&}zl6e~5aT&FqKKJBXY)YSyCtthWR2;g!m1*>vJej9qj~9Df*kf_|^Gfofcph$%yUxTOFZLL*^JMkEs#cNilwagn=dv?rXUoozSCgG5J1aJqog16W&V<cnXTtN(=JGV`4B7eY*i?mVTuqNd-2&p>b}i(Dk;9A|D>%u8LfgrQqZb;J>0|ry$9D3xv?#G`aA90{M2t)h#fc5>Kak@0W{68w6~(U|^YD|hm&A|sF?l>b7qc~4J*&AD)B@kUb!gWKgA;aX-44$Tu3~EYsfblB8?TfRgP%0klehG7#cJFiw8QJGs>s*Xg=L;*WrK_4-Q_K&PJ?o-_Itd2A}QVHr0HEwp3G|4y}w)<CfC`MC?1Y-lG*u8OlT+XZm?Bs3WYH{pVJ{};-s{j#-;S!WaqP@XqbE=b&ELD*9r4-*;(=GurnM(!tgfl0HPi4WHry}k!td_K@oAzoILzX%P>4>>I~94lAg01y=HD(oIbY^89%nD)v*}Yw;hg(nMqD$7M6K){?yYb`c>ax%A_;p>1*6bAeqkTrsL!CWZukq8s7Y~)7r|9JTk@WIYq6GSJ9En#r`Go@M)UQ&YZ2o=Ca3vojF^FohMt9)v&W==gH=>diJ=mdUl>XJv(Qfo}DMV-vZzOp!^*BK*$eOL4ZQw3i*_uUvK$zjt1&MY302U%g@>mfQrxnM5qBx0D}jFKx0rtGw=ojv;ZAcfVSXI>y?E9^lwQhqI@p`t-%QO>3>b3CH)&pzdAxqaDjs04%MJ2ctIWI{T|ED^)Cm0P#zFCLltm?hEN@9K_jRQo)82o2!mkILpU^t${;~I<$aU(umo1XOo)WOkP4lkKcqu641yf!0mC5<dc#=g2@x<Ek{}a)fIg4~GawBH!d&GYlclf_M!<4d43l6wtfKXL(Yn1L0lF*SyVL4ZX#JTmhjy9+3+UI5&=vYYXNZDq<(-)!5D%kZ7$m}Y7y}(31tvlU%!a9u3-e(X42DH84~D`>Sf+d`XC+L4WS9mM_P!xYQgW1k_u0!|Ti;i>ZB$vC_|x3O3a6g0#N|~%+yAI<FJIbwP~nj?2HV69)9)(Wb5|~x<puf8zqT5w)VGBnZGBEGd~o}H)A#TbM_J+XKCk{2-g|Tb`HyE?xJevQIPmo3?_$5w&lG;;IPqWMo4aq2VUH&%p6%s5_bw}(lZb8NeecdFJbt6Z<z;P7{!!mv?(Kb6;SC;<Hu1|UR}^mfE1!#dZ4!U!-$wcOoxMD7_HKpCw-asRMXhcq>~p*!mtQY?_D6ktdB5i`3MZ8L!6uH(-mCERi&MB<b=@qn?7DcRzAe1juub8bXPm!_H#~fxu-8P_e}#Kbc98z#*%od;`jL|B8oK<uIQH6hh0hIK@~<%QJ}d_P(qHjxFJCQqLSfvkhfRF>-8qF@E|2H(yIGh1sBbT;_I#`3H*t_ny!!NUg$uplGy6Ng>aA%muiyNMtgBg0UYf71?9%2oiF7U^o7c6KH|`V6qiPhwpSE|CpHx0gKD@YZ^*hBPEA<jTlsZM4)z8KAkDL=bOAm<ndH`2%rFq^42R^<<s)|Ldeg|3j@aDMipijiJV>v5L+5T;D)d_-mTE9Z_Ph-2`8S74wyd@8;exDi}4|x+yT3!2zOlp!VFZy(jI9z%_y1W=*^*h?wIJ@_%!-Hk*@g!-nduf@S&&49G<oTQXN;f?6V|G3+$Ku4c;}WHimHjX~llUn?a?ObYr3HgaVO}mfD_$LTZd1Dk<Ekf;q=g+zV|G@WZY^<QV!R}ME@(BkaSwb+<c>(`_Sr0M?#hcTam6itrB?m(%j}%*j}O9bJqJpLNu^|-hMoDgWnIaNv_vUkLqD0Fe{MfX+`KSSYIG_~=4set!JGf>jF$46;qg-5m4a5si~W6G?9ACZY%Y5&*j#r0?A+Lzte%}Yt7kRr4B7d!x$JD&Ty}139d?F1J-grkJ>UQLeE;9`{r{iyy%0Fk)#lI&0>J^QL1oAfHJ}O<huTmCN+`bpung!y3jzc{d8i8Yp%S=418{~~&<vVDJqQI)&_PSkfInbpP3x6|LiBGb<@XSlqhDJopE?PI#<Wvo<?|-_pdeINe%qj%@?MQQl!VfthO*!UzJQ=2_<;*F0ukyczhSVZ@@|bcw18mnfp7=|15^MBIzt4sfrYRXra^m1hh*hlls?c620&McQSL2@htV(s+Q9_q1!*u<c^73mq(HXv&c+Z}00UtZEP>%L9;U!@S}%dtO@KIvQocvg>Jw@GX)u#^vb>A35IR67$bgQ}1^Pj>@~M?r=nlh_Prr<Tw$K~KK`P9ENst4x;RncqT$l%gVKK~A-a}agV<8bH!~X$Hsx7t'}
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



BANK='nature-bank-access-transition-01';LOG='wetland-split-window-hollow-fallen-log-01';REED='nature-reed-sedge-01'
GROUND=.12;BED_TOP=.04;WATER_TOP=.095
placements=[('whole_sloped_bank',BANK,(-.75,-.10,GROUND)),('whole_hollow_log',LOG,(1.65,-.75,GROUND)),('whole_reed_sedge',REED,(1.55,1.15,GROUND))]
def rigid_point(instance,p):return(p[1],-p[0],p[2])if instance=='whole_hollow_log'else tuple(p)
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[add(rigid_point(instance,p),t)for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,rotation_z_degrees=-90 if instance=='whole_hollow_log'else 0,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values())))
base_mat=len(PALETTE);PALETTE.extend([('SceneOnly_LowerEarthBed',(.23,.20,.13,1),.98,0),('SceneOnly_DryMudMargin',(.28,.29,.16,1),.98,0),('SceneOnly_OpaqueShallowWater',(.075,.20,.23,1),.30,0)])
def box_mesh(name,lo,hi,mat,role):
 v=[(x,y,z)for z in[lo[2],hi[2]]for y in[lo[1],hi[1]]for x in[lo[0],hi[0]]];f=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];emit(name,v,f,mat,role)
box_mesh('SceneOnly_ContinuousBed',(-2.4,-2,0),(2.4,2,BED_TOP),base_mat,'One continuous scene-only low earth bed')
xs=[-2.4,-2.25,.70,1.15,2.4];ys=[-2,-.78,-.14,.58,2]
water_cells={(1,1),(2,1),(2,2)};all_cells={(i,j)for i in range(len(xs)-1)for j in range(len(ys)-1)}
def cell_shell(name,cells,z0,z1,mat,role):
 vv=[];ff=[];idx={}
 def face(pts):
  q=[]
  for p in pts:
   if p not in idx:idx[p]=len(vv);vv.append(p)
   q.append(idx[p])
  ff.append(tuple(q))
 for i,j in sorted(cells):
  x0,x1=xs[i:i+2];y0,y1=ys[j:j+2]
  face([(x0,y0,z0),(x0,y1,z0),(x1,y1,z0),(x1,y0,z0)]);face([(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)])
  if(i-1,j)not in cells:face([(x0,y0,z0),(x0,y0,z1),(x0,y1,z1),(x0,y1,z0)])
  if(i+1,j)not in cells:face([(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)])
  if(i,j-1)not in cells:face([(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)])
  if(i,j+1)not in cells:face([(x0,y1,z0),(x0,y1,z1),(x1,y1,z1),(x1,y1,z0)])
 emit(name,vv,ff,mat,role)
cell_shell('SceneOnly_DryMarginWithSidepoolCutout',all_cells-water_cells,BED_TOP,GROUND,base_mat+1,'One continuous low dry margin around a real L-shaped shallow sidepool recess, supports every entire original model')
cell_shell('SceneOnly_BedFilledShallowSidepool',water_cells,BED_TOP,WATER_TOP,base_mat+2,'One connected opaque water volume filled to actual bed, no floating slab or intersection with complete original models')
FEET=['SceneOnly_ContinuousBed']
def layout_bounds(v):return[[min(p[i]for p in v),max(p[i]for p in v)]for i in range(3)]
def layout_validate(vertices):
 assert set(vertices)==set(G);tol=2e-7
 bb={instance:layout_bounds([p for n,g in G.items()if g.get('instance_id')==instance for p in vertices[n]])for instance,_,_ in placements}
 bank,log,reed=[bb[k]for k in['whole_sloped_bank','whole_hollow_log','whole_reed_sedge']]
 assert all(abs(b[2][0]-GROUND)<tol for b in bb.values())
 assert bank[0][1]<.70 and bank[1][0]>-.14 and log[0][0]>1.15 and reed[1][0]>.58
 assert log[1][1]<reed[1][0]and bank[0][1]<reed[0][0]
 assert all(-2.4-tol<=b[0][0]<b[0][1]<=2.4+tol and -2-tol<=b[1][0]<b[1][1]<=2+tol for b in bb.values())
 for instance,asset_key,t in placements:
  for name,g in ORIGINAL[asset_key].items():
   vv=vertices[instance+'__'+name];expected=[add(rigid_point(instance,p),t)for p in g['vertices']];assert len(vv)==len(expected) and max(abs(x-y)for p,q in zip(vv,expected)for x,y in zip(p,q))<=2e-7
 assert 0<BED_TOP<WATER_TOP<GROUND
 return dict(instance_bounds_m=bb,three_complete_source_instances=True,all_original_bottoms_on_dry_margin=True,whole_rigid_log_rotation_minus90_degrees=True,no_source_model_water_overlap=True,original_models_pairwise_aabb_disjoint=True,water_volume_fills_to_actual_bed=True,unobstructed_sidepool_in_front_of_bank_and_log_window=True,new_reusable_model_count=0)
LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate(vertices);result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,.42);ORTHO=6.2;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(-5,-7,5.2),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
