"""Static equipment-preparation bay with two entire qualified original machines and no new model."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='agriculture-whole-tiller-and-seeder-preparation-bay-scene-01';VERSION='1.0.0';TITLE='Whole Tiller and Seeder Preparation Bay'
DESCRIPTION='One static agricultural machinery preparation display scene, zero new reusable models. The entire qualified hand-operated curved-tine tiller is parked at the left of one finite common floor, retaining its complete transverse claw rotor, curved open-bottom hood, compact motor-shaped body, two wheels and high paired handles. The entire older hand-push roller seeder is parked separately to its right at unit scale, retaining its broad drum, genuine open tapering hopper, rising side frames and complete parking foot. The different front working silhouettes remain visible from the open front strip, while a continuous central interval separates the two complete machine bounds. No loose duplicate tools, crops or filler piles. Whole original oriented triangles and opaque per-face PBR are retained with float32 translation; original hierarchy and normals are baked/recomputed explicitly. This is a parked equipment display, not a connected sowing line or a resized mower scene. No powered operation, seed delivery, soil processing, human accessibility, navigation, load or safety claim; no rig or interaction.'
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
LOCK={'agriculture-fixed-walkbehind-curved-tine-rotor-tiller-01': {'bytes': 87292, 'sha256': '8d0d7d1e0b89851e567aa6c39b40aa4f5c20759fd62fd610ba854e2a86ca4b46'}, 'farming-static-hand-roller-seeder-01': {'bytes': 22100, 'sha256': 'a135d71e418f83475ac9344e1e7b9435be8eec9a8c7bccc1f2b8e50989ecea95'}}
ENCODED={'agriculture-fixed-walkbehind-curved-tine-rotor-tiller-01': 'c-rlq37izg_4o@#R6HRB<#bt2b-}*72iz{?MlLxN6%d!*S$1T12WEFUB!Z$O#;ABjgV7kTpo!5Ws6l0?6OX8gni%tw{5ARI(0H4}M1L`t|5r6rGc_|+H8qa@^z-?x;}qZNece^{>h*iCy1Hjpw=S8nA42F~OL`&HiqOf67tG&W+tASw@2s7;xpsBDJ)UalOr~ll*3M~3CEJr7HLGElnklXE_NI8MX7&jSYSudw><NxvTUWb2p6W;>+d<fxVAP&hSKHAD2dJHBWT~Te;<C-P?G0_Pt#&c}TU~8?vWfn|_Ewy?BL8u7ZG2;As-c54qcPdGHrXC;?_8Nmwvv69w!ptNWOGAfXH8>ELtAq^6>q9(OF~;~V8?hW0g!|S)uiGLsTw%aCeom`ct;CuPqq>CKvUWNbCVn9kt0lRZ){C=bfx03i?SUH+T%3|P{dlIjrPu(=C0P(n$DI)<C>bruGD&HQHr*xv9)1C&4xs0OHD(~Dk8Y5wF}D5#M-)=_GBk)?TD{#BY#LX*EF=(G;B;XwAQr5TN4{=lB5gq)|!saRAOzu4`xvxXmwM_VV5M@<HkzkQ`~l|Oxw**aog=OZMQzfZFiJyH$T-j<Cbarr`cw_GHw4f+l;SlyY;EInV?MDKg~81E7SH*v(1=>vhnt(+GtF(OyfVzR%2Ra8n0zG8)$k3BJCY(lc`SlOsdMZ6!NLon&w1%qBCC8+}hAt)0*56?|@!5G{!qg!(nT(p)=9Gx+axq<C<0!IcLyAECyP_Dq2eFF+RB#I(jWEYXGoIqA8Pj#+z2hAuR>{lj>HrCW#Rw+uP%fbVExr*#tw|L~_`UjzkC7n4*9;v#TN1v^dcepGOX6{I4{@Q#GNi7BWeCq8*a)ws=#b0Y;-SmF(!KS(So;sOj89YVT|T+K_}Hf)5R;Hop3z&@&4f2^LKbF@+qVT>VpFLu(vrC0f`3P0yZ#tKp2PNw&lP@tPKTOj0pdZ&BEo3r(BWkXn<ee<tj0d~8+6%2jRZpB+@CsYC}I<XmOc{*!CTv<{|fHEnSi_Vz>v*9glfZNwsan8oq64X|H!B#i%srkHw7(b5Wa!{7=sXGPZ9Yu2_B!#pPm=Q=bl-o6^#WL-^LqKP!JDV10cR@=}Kr)NmE>8WJ0le1IHDsJS4MNq@kOa)6aGf#~(rM)4Qg4V&b7zA50b&v08X;=#Zqb1ozmDij~w&j`*r&cl(O0w~yy(ZqawsR8+EQvNU9TsS`$P3S>l};sf#;1`Qr#6s^^jb_6Nh4QBXTzF!#{cq;w;41AMT(ez2NCK_G{RmT)bXrMcEqU(bR-k4;~`wa&a~xRYl}QG(d#rKxR}&;QhU=3sAUFJqCNf{EhJpDbgiPJ2s#48%h)Jry1A39y2$@7B6=n<bXM0Y<724KlUHYc4AuGa>a35Ux<Fo?t?x`B>@<<=2_jcR`|7S%a$%>TeGNNF*ma-G*#PyBlfAhM5`z|S!Qh7DT#I7GEuzO>lt1*6<k}^0a2;j9$3!Zg_3>S6*OIGFG{d8@m7W!=<LzD0U*hiCX+8pfY-nw!ZiU1@y1fHpE988Q#2s=D#x8Qmi{ovHshe6M#Y`m{8(J5@u2Yhooyj(;)>%-e_6T++*MfUnn`tBHHQvzyip;c+Ts>=T;4gg?dE>=x4Xv%9rm0j&S>X&)S=ZWBVs%R=jsI)nof&7A$=n(?l5{Rv;F`ILi#%*D9Xknjo02)2@i8~SF5d*rj3}SAW~yufyI$Q=vnmNg(3<G%Y>j7H#MkafYNz=qX@bs(H?k9nwt!r$jc4tYp00J^x;Mh;XWTSbxhtrg?oG~MYIBRTr#n>Kl4xy8#oKEqE;H)PI;+mEbL!kWug<Rv>SA>;GlcmS%u--B0O>X)xsYT+q6aw_<UWvjK*Wc53Q-DNKe%9Ui{PrjeZct&rvX?X*aD0ND8zPG)Nwtg*Q{42nxK^pkY+V@wRU!;;^S$T#&2k7U9&3Q0%y$l%nWQiM4<S1+Ihg%)_7{XVb<2wf<1uFni8qZNeBlUe+F#MsAT2(L`PRc>&j$%>!#X?ovE&PU2PKVDbc>NsiCv04W!A&tP2F+m^c@X2BCZvaV{O1$R3|m(?QM~k_&HuQ=W(tC%|^1POC8q?P#cJYG`gwHbHP~O+a*I?hV?LqF3KnLKY9*Z|sDMH!rVkXlhv72@!mG?L?UBw36VuJYxtQ2@-IH+mor4^oo1oA2&6&#yeKR<TaV-C_G*!K_Z)$*G@fS>fGszm)DZ*9Sy{`=wVD4F4zKg9dBr&TO985$~LGjv;U0Qr%#`j*?oN?zF}o+!zSnySL-rb?TYh=EoLnc>^M6&gK=F7!#afy>k>MKwPXRIt%0ZscBG34P06lR;Hki|HnAbg9x1cSf{pN}Me(M^Fs*I{&8}UQniq#LYfUsRBBy0Lctm1es~`uQnruy`W`MrQddM<kf@8+We}NYSUd#``n2iZ$W?Rg+P2Z0hu^4PKJSVfwGu^;+z{E|`&TKX8fFS3_vIlg7Am%y{qEf64c_}|DWjLN~xn6J{Iqk}Ib6yvOXWB7x&URGTQ7bU$f6zJ0h*_jhwwc*v*@0sQZcs<0G7U35*R>tcfTWvt!NG!<C+wzYWsc@rw&_`cqt#6^SDKN6ElW0~D(<D>xS59eL15Z3a4}>^vdyr4$8=5bOGGZK4#)H@7=r4CGw`zq^S!|KO;4+zOJVjzlatDNSgcd%jF%Zl)3FWLG#wu{xw8J)vFrdt&uoK4L{WbVP31g#N<thdT>LAy?gsrzCE60ion`iG=<G}-R)H1M&YiMg@$4nD7tE(idGi-6ns?G%m^_1*09TM`Br;as5rEKnD~MLhte0umY3J*7_&Qy_PE(^!Q@>6xU#HL48B|)QrC(=^)2+c*N-mLBQma{scF85oT(x#VwN9ngR-j;Vy)9R*S5U2AX|)yTm|SeiRU4~D$yOywwz%`gGOI9Rs}dbs+|XKf6=rNzqGECpAy=zgjf(AxRLq^SmS2q>+ZE}UGbk%ojUC&SDB0!=$~G%fvV0*xzjn^B>;l8G3v_Mi*It3jZO(PrUPZMRU)9&I)93083hIniRA&YKbht5g%!=wPxpuE#DL1rE!O%M8P9xEUd;NO3L3IiS)$z-8R&>=~zh3VAbqda3*U+d}e4$>uc1UJ(wYyfuy%t}a*RP$+tX!wUzL#8d*RPfvYS*jCu4R|c_3P%&W4GWucFWZ*zZkBcRdQ#vS8zsqR+*El@Orp@joc7>1w-t)71UTs=FG)m&;QUhRuBt4?iBW7AG$_czeb-MN8hZlM%jgL{n|Mf?c35>m|a@A#+7XSR&Z&aUy$bcUYW@te<54HKJLu*3(j1>+?gxBeyv?|z>RiLSsWH$w$`ti8|lFQa5d*IS?gEJ4Q=37WZu$?)%ull{v#;kKUUP$HZ+n&lw>M%&{bW{&GFP}iTDP3sUmk-e#xe_aT0CGB%zU{VI*@TN86aW;AUm67&?X>b8XkP>Wm3~=DL{~Gkn_#JaQ$9Ua+!V&#_(Kci}~@wIs;3_wnLmI7a3Qj^|jmZ<%%-$e9-1VB3M~n1)TR{dCgS)t)weYG!ec?}b^u7pmPY(e8F`cM_1YyDy%4(%h34l^noU*Y5;Oi_kUO$z1SqeAn?~L=3hC*(<bG;P{S1xA~?^^azD(focL?jkce;K<5~)ZJI8<Xl9Wsy^cqfA2^<6+qM^!(VJ7g-KyPPwcf}XqSl*NrQSR{W>{c?ZVdYCo8*FT;1ON=hG&#opGa+>B-=EC7#N!67!EaRCjcXcnw*#kHeAm5{OXh#RI9{TwZ>-~UJx@4%P~#MH%y|Hm=BiZ88Hv6(Y1Z2oEA;n3cyUQAb=ypT*Ibn^k7J04hY2zP-VGu*r-mArdh2bO{)S;nqJ2BS<qSVWd^Z5@K+}E7F6NH!1l-{-y&|#2m;?U{J@FviZo+h#_`3#f<ceuI=AhZw(Wv38=y_o@u))uhY&cH>l?P=1b#U^+Ewb&salV2m3s6HJMf7IGYvR1VPL@^t-$kQo^3jTY5Im=R*$X&A&D$t*nZ58Im9`_Az>6;9|kC9c$QmEkzSRG^s826P^BVmGiF=h39Xn-I!zQ4#5@yXHMlh&?9}wiDbnyg(|}kGLlPJejHprD;3{L_U%@6#)9}hEGFF`;Ekjog5?iPwx{4L~VS=k=R@rT<x^7nz93|#cb!@b%bVim_<<M6W+r&!v2tu3XR;dL~Ukjq>TuEG#<Oo%VC9BFb$qK5|K_xLoqJ!!~idCg2w2kVNP)R%xE8!yu2X>Wy(Jtc`P0QfIA{c1VjU9p+C!FODjR)|_@NCa4NO<8)p-#cGKzEJ}S|d|bi`+m1Q`DGcf`2f}`2gG2XtnYHW%4r13d&AXU2V;YdR>v;gqr^_dh@E)TN%e=Ih?gvcHvz#^nym_k_FhiA2Z-=rykYHT;#A#&-FZ~@EV8U#w4%sh8CA?gF}G(g)Kp>oF0Pm-B9iyQ=1QWjYMKSj-jhap$;liqj)4f0yR2jb!v3VI3M5QJaEZ9Wh4WmNlIY*f$!R$N6rWj0ur1NkX9MwT9;ce*%loma}kYck{*KOWS--Akk>e|vT2!Pm+ysg|1!SFw5_t%<mxJtY5^1j;l+jc1*T)ynG;MuussKIP|qhpJRn+th!zWC76fS;kj(-`2B17h|1HM?Uj=7_Il*uP57K$t2z+oxkQ<JN!#X}OC&&q0m)u}iPLW=fiu9{jWKe-cmMWnlJqkzSqfle4IyJgR)oOIj3hdE>$q@7xPEH@vV$Y)n2@wq(nQN02$%i>F$iXQ~rXMg93n14FtOA4dK<6>j2gSRV<6AVtgyVUE>%jyCQYm^R9I`Ll099M?2XF)BGECR1Qj>NC)>Pbs3Y8$z<42<er%ENb)kQkfDZ1wvvZ>6fNI>S_p6R;f5(X!;2{J2~VFW%+oE$FoGHs{a^#|9hF4Vcc{@PIK-Q>{aOdnvnNSq7Z6gY--O+$1DQS>u|Ou!Go$PAd1m(xN}-P({Ft9Eh7t6+`IaGmU}`i2RbfK!X6-I@Q~7$oA5C(s45tTBMch7-__6&RH0D49efv#J&tRQpyL)p=Det9ezgt9fO-QOx6$1e;#w3&4BW0k|NVUlu%<K<B$Kn;|9$lYa11j$M=^WX#QRV5&o}m_ZPv2aOrF<vWnEkxL1_Lk<C_xfgTk^&_Pgobr88?q6n=%?!$`(W^j>rklB13K_QLm@)H1=+QDV9u3SB#=)T%4nG1#`c*12(A9#t2bCy6tj3Q(2eImO;2Zin5S$H_sX%Z-R<8lytWpD(zBe|r4-c`BM7mqLlwkXr&<;~tA9CS>S%=^VUhyX4u#K!YHv-oOHI}`G=G)b|X1|P6g2XJZ1}Bz@KQS0D-+{S$<_b9N1WZ{;o>M1G`EzOz9l_4VD0V9dP5o>d+99}kzU`D%f~(O9<pI1h*F<7vFN*lS{t0DfuW8seS%S!1z6f0UtdmKWBP^F*ShozS1)p4Wb4a4col=Hf^kfzpidadWMJ{I(Mf$D@3A0`PqzbA$sbW>fsKBV?GF>(!vSN_R*p@}FZTmDaGR(}W6a*g3alvsF1g4_L6djgN!hgO=rnSE9XXY%KOv&;*3kJt5cUdW@^0HE3RWRcabfRqM#X9?F`fgX*cSrvea^2#Yl4WQ5;6nU?sgj-Xr<Rw|1C1$xU637@9>erA%5ek7w8%|qnOQ46gbTA*GS{%nX~C`T6bd|jEjXF$pfGWE9M3f@y3!fTTx~ae7=7C_GM<56oQIxxK7`?d$Rs?5;qvA{EW|f5>*S!tm>rb!$U&tk8XPabKYw>3y)$vurq1}>c>C&3@->m<5)Rq0pt+fT5iId24XM=xA(VJlzAfeVr5kkjrYj8m-T_JJ`Mqt$-Yy9;{NAy^(XYE?Z`1WE=(tI8UVeAWq?y5oZ94?8Y8nrgSxw_@$E~LE;2x@JJXx!#qVW!yg@5?QJ29u4#)DI<rt#!%i7FcJSza}bhY(jy<9)}hrt!X8)d?Gzm7K7pyZgl_Y(=}1b^dC04}zc?XGJboRkJ@Fz^H0}&#Xp!rUf}dRr~v1Rr<5-s?K_HHNGnSIZmu9{keu;NuYHcqa@lnK~)FvjY=$-2AG2V1J?@lorj<SK}GSt^Z;auq=ExjK}p09ysGxMOt*qD^sVCEo#Ip2uB>{u5)UTWKd2;ZQ(YBhJe3%bVE<Sp>a$ArcY;cyS84sO5meQGx1z+OwEbRS1l6?PugHZ6_K#H(Kug;nl-N&Y?T;CioPL7+V^%fxXB&R38vW5bbE-K1Y^$QoQ?P%D{Zus5vu&f25GL5)twjGNb4A;Zc@@}CY5h(`=dWP@iu`A3`%5Pt$^b}%MZp2wicSE*0X(acB+mAVdqD0csHz9PUy%uv9w4Y}-dl12vOZ!}bpX>0su~2xvMX_;f&<u2P|bPlz)Yg5D?XK_qL8%|&);3Ql4~D=1NaqX0@Q66OyOZJWK?6vu36D+MsNVDqUlJ<nMiJi@v6uLT|1~M7Lg@Jr>gxcx^5`g-?ysr11`PczM2Dg6<v)G9Kf&Wf`Z@xf#8xr?kaHh3NSyXj6svnTXEiRUqfih?D?p<xjDW4&1b{^Zhj?HaHzwNygLr7c=Lb>;jG_HEXV0`Oxo7mJf<v@wmmuQfV6@`9VYEpF>8MrPM2fWeiftKf9K=uzfs}8{C_1fSR~UpcQ&4S>~O4-;r}g^7t5UUw?)yx2lXqFDcmk>bEMI)NTXkoM!zDBenlGnie&vd0^a+h&!YZl1n~Z-4>}q?5$=NyMnmA!2>AC<_&fp)htIvxXV5?>2cq8S0CW@@4CP>S5IPVILc^dOh7Lh}(NJ^@l*gdM(BY^C)k0Z|jzs;?NHhS-0cbxoy3Y^OU;ERpa8q9&tN6Kjw}hAP8Ls4Y^_PUF+<l;uq0iyY@4OSLc>by@!t1ubspMOx-yaSd-3P1qf-gT3zA<xzlK=R*DAz|3fA7Y7a(YlP(}Rkc9#qWqpkk&66*E1knCU^qydFecd|sb8Z%cH<g>TjupO3rVTopal>+MiiX5GMb(ND~~!eW_T&eLi0l5--J%&-k(@s_Wj6cx(LWp>=W5#Rl0N4i)hza62wezOJt^bb+J%75y}aDB%b`oS9d!5aF(8v4N+`oS9d!5aF>$s7Pa=qPjo_^x5#y$+x}41Cog@QH8@_^QL<6XB6)40x@>DUU(N!oS3e9gFJVb1(3NL!lfB{*QRi;ZPDkc_8?|S}1G53my!9a5R*o!G{u0Iu^>YXcTzF{^&R;k3-|ASDgUm1av(3Uqrp|(P%vNldqofMEJSuF;;QQ$?t}>i)Sl&@r?uUgRLhkdH?H1;;)UHr{n{6*5Vz9oTlWT{i!cLZOU0n?(lybe!25BCF862h9^BeTgt>IFg>W4=|ROz4=QGQP%+bkikTi%%=DmQUJoKBwtnG)pM=-^HFIvZ?OqW*fKZ8F`qz~4^`}3!H7b;s%e?xAAI^GybBRoTJN&n13m$vwOC^5k`+wXO?s$G3)|I&w?MT1+(=J>rli!X|+8Pl3r~8x=nf!Kn-zECN8v4N+`oS9d!5aF(8v4N+`oS9d`N;hwqJ9#=`{*J+c`$gz1K~|FM&c*?!n;=CCqD~b@iXu~p5~#0pd18VllX+so^ofHUY79>GG5thTiE;ErAj_v>fG?oKeQ=%?7mUqlUp|_d3)c3!ZWQ-C4c9&!Qr%>%alB4=bF%+HcQEEU%WAVe;k%F@d->1DrS06G1G&JnI2Tk^q^v<2Ng3tsF>G-h>5Mgar@Euo^A8kxqwB!f|t2y;OV$_+QB70=e5C8@on9swPoIZ=BVhqBj%UL<hLVq>zd8cjGs>~$rVS}n9-xZ2qKltA5Z(Q^bfw@5*5l9%H;dY%gg)D=?81*2W#jDYv>1S=m%@)2W#jDYv|`=@RR$4S44E?-5dPkF;E@@Ub7GNlYQtcyf660QBaNoKY1AV#c@!M1Fv}m_{HO)JRZDef0|GBhxc*dF^Ql2EWF2~vmTtC-tx%Z;n-a+R`JirJQ$w8Z<vx_KYe$2XaC+xp0#6lnArV#sN#!S9t(f-<=2$F;*np6FOTnwRebRs`@(1cI$Ft7UwSnB&39r_-t_vIoE}un^q^v<2Ng3tsF>+N#Y_(>W_nODuLltmTW{HMPx_T}*HXUW9~+~7<J(JoPJTPs@>AzUTl@AYnJ?$JBh>t#t<iI5{o$cvnRl<=+CA_5Oim?}>E68(|LQM)PZ!F|W%_O0g3rGFHzhgeY1V3d*o!ZQx-xk^6v{~SgEjPnHS~iu^n*3@gEjPnHS~iu^z$*yyZ5J8BZq)j>rL~?-tZo(IqxQZ@<@1(0}n~^$^P&@4m>8AcMpX31nMVOFMT{jCr!mF-t*EMp?%a6C9hb27(U~`vy^<xb%XKBhvG{9`wau}obEOyzdrJx;g^@H`Raksgn#(yawQ)*`@Zn&KRa2<#3wL4sF>+N#Y_(>W_nOD(}Rkc9#qWqpkiJRA||%}&Y=eWpBG~E++5l)D!O;_v=YDcmGmQF%Vn)mp}btC?vh?O`ONYXnf!Ky2AvegxBl{_5`UZDj?g~5ZSS7{*;?Ye^4k#_*m+d6si`zC&2L9&;!}&F)+zl;Wb*x$%SiNtHS~iu^n*3@gEjPnHS~iu^n*3@^9jwn`FxW2$;041T5)}{FrU0{%dO#MN6*A69x*%-_Ub=h$#3l%7=HJa6-stmAF2QPnz)j8{_3msoBqB+$-A0*g%dZ=Qu4p=T^;`C#Cj#qY`ZCRw@#8W@d->1DrS06G1G&JnI2Tk^q^v<2Ng3tsF>G-h>5Mg^s6hw`lifvs?)}P4v*Mpl;o4V%%g7)!AlOBQ{qpy|L$Mm=C7QkEt8&eYP9c)!%D9i=C&i0ylq+Z{`vct_}iNgcqTn@dFGm-Oy-h_w{~B2LMAuM%NOO7x&HF<^1gHW!5aF(8v4N+`oS9d!5aF(8v4N+`pL<FEro17RK;vPRK;vPRK;vPRK;vPRK;vPRK;vPRK;vPRL0<oa(YlP(}Rkc9#qWqpkk&66*E1knCU^qydFf{vyR-ej$F+;GC9}SI-`o&I-`o&I-`o&I-`o&I-`o&I-`o&I-`o&I-`uqxyJOMVx|WbGd-x7=|ROz4=QGQP%+bkig`VV`2WiK>=1uI^y-79>$Cao|F_p?IsIS_{S^2gwtlB#wtlB#wtlB#wtlB#wtlB#wtlB#wtlB#wtgpLa;`BwsF>+N#Y_(>W_nOD(}Rkc9#qWqpkiJRBJNrD>{<7$X5I69H{KJnbuksQbuksQbuksQbuksQbuksQbuksQbuksQbuk%_?(@T(9#qWqpkk&66*E1knCU^qOb;q%dQdU12NCzIC-$r-R<oW+&Na5)q++(-q++(-q++(-q++(-q++(-q++(-q++(-Bx7=}F+Hf5=|ROz4=QGQP%+bkikTi%%=DmQUJoMfS*Pn+r>kb2j+|?39Y@7%9Y@7%9Y@7%9Y@7%9Y@7%9Y@7%9Y@7%9Y@CGTw{7rG1G&JnI2Tk^q^v<2Ng3tsF>+N#k?Lw+_V1Gv;I}h`qv}x9u)OCz9YQx+h0hlIO*&RpL^z9C9fKMZ}_)8i<P|S_Q%7+-X5l8@@(=sXLWa%<LfW@-Ch-wV_xMQTCZZ#wxf1`SIMN0&;R!aN+!B`cJqKx#l7z`%JLb%`h7h+ri=%EvAv$PO~yv!Z6~rm%9xBl)0K*u&SgxF$;M8`q;1RwWK8<VY)QsMSIj0weErV<mu7aWVrI80W_GJ$X16M4c3X~#&Q;9pR>jP2Rm|*G#msJ1%<NXh%x+c8>{i9hZdJ_ewj48^%b3}%ikaQ2nAxq0dAk*H@pJl5+FuL%Zt5tBarx~CO*wZU{=?t}B{KQ#2*JM?K9|Vkw<83{!*JY^Tq3_+^c@TZGNDQ)TNf^r7q%G}$_x9B3+3f&(0O^KOj;z9-%jg_M0Mr2(>6z<Hs`m~zDJ_I=eNthFCr_GR>@@RiVEe0ZH@}%g?*0-<>lXBk(XD>Fnh)t_KY>`8Ee=x*05)+Vb55@p0S2KV-0)88upAe>=|p=GuE(YtYObs!=AB*J!1`f#v1mFHS8H{*mF*1KQsvi@N$s_uM<!mypBa<;58D}z-t&93@>s=?Erd@?cwwe+=J--x%<I>WUo3ZUqdAaP?>}1UoE<QFnk^Z@BPpQ6rz*hH4V*#*U4xeyiP%j;dL51176F~N_ee8ad@?$HSlUj>)_Q1dv1XJ$X@fP{25d-PG#27zs{uFSHkDT@ZLb5kHAo3R8OCem;&V#G@0J_I~~gDXezz$cNUbh&<y$<*<2{+qS^F0vIS5sKy&DGWQ(9&gyz#beouw+RJ0HsjfSGrp*$TeK||1RbS9K%qNV5<Gy<)Fas^t3YSAckHk4<hv(RWX7BxcIh#Js1bR24ivKcj@<Ix0k4wUDh)o462Q5%$PD1i**ptVr0MXkt2KI(w710|7%CZhFFu16^pBlj9Xc_QjU5OYH=Ka?_;A4-|a52eiIhf?P9LnUW(8!2=7p_IA&P|93>C}l1`lroneN}0<KrOf4rQs(kQDRcRul9|qB%;kqt=JG=+bNQi^xm;1mFek#?{9Vf2{9Vf2{9Vf2{9Vf2{9Vb}xu=x5`MZ?4`MZ?4`MZ?4`MZ?4`MZ?4`MZ?4`MZ?4`MZ?4`MZ*t&SlKa-=)mW-=)mW-=)mkt%!T(K|S-Jo_SEuJg8?L^y!=j9lLx-`mKd~!u$H}3uS!F_BCah$u}<ABV{J9Vj|z%{7UYaA|~?Xn91|UEM_LJ;*a5bO+Tvd5yh(5B#|lmU87~%Q*xYM^vU~P@a|3Lk^`X}2=hqteI`fH?-@N5W})P1`#$hK7-qwV)9(QtK<CorIaczFYd-`!4>`LMGK^hWX7br_6f%=nF_Gu&O2|aM95Z?Tn8nQGRor8TYCF7s=gxH3)u&_g)gh6Jm%MZ;zWS!2O8)Yji}AwihAY{&7vt2-5lSZVSO3pQC6js={b{t4N&D~JHAczTPF<Fhm+_KGEAsV9`2N4H$hBX_M4stE#-v`RPYH+IxJa2B7b$b&B4ut|q|A+rl(}({GB++#=Eg<J+_*@Y8y6{a<055#TtrOHvDCJU!eKKv;4G&zTzH=5w<Gko-fjf%5}EvVgg`bT$1QozF}FR(X~}USl}xrhQK5W^Ovq&N@^Tr{cF}S2+i82Ss6E;3p-Luu99$?bY!5D!m&<VDg*C<tYm67x7%!|bURYziu*P^{jq$=7<ApWG3u}xQ))+5tJwj*Qp?IxfFkN4mNx%Ig^SvJ@APc$h3eY5Y@#_x9(!aWNJ6TgW0sfsy*9*o%Nxt`ktQQ;yCHdYDvR*JAO7eZ1<oh{IC`~j0vbiIX1Eqrux?bQz=_8wFcrhqr$fMt+bRv`|qKRk_8j2=EIT_WXA?O%170Rgyqv5C)&46+Snu10^|3^VN3Qb3IMqHoXdd{VI+u)W+#{GVGL;BC}ei2{s7dh`e@wW8S$6kzoyDlN+D<<8YZn)qJxZfr@zj?wQD(@X2=l9zqTJM=|i<G~0;KQ{2C!Dle$}i81(ue=%ay;UkW+_j6>-%Z*TUX#`Uyn<<`R#9~Z(MvO{`&9b-1q%ksr=^Cnx*`&2X3JCE*-O4%DpGwl-~a4m3Z%ntEBwn4{lDsw|)nndYPO%m))6u?wgn4HBZZV)|tE0tM|JM@BgfvZ=2su<p*9T=kHziD6Mzg336^6^EhpP|NE|#@{P@prU#sT4Zd`?oZso&o%ZXl#Z3pxdHA8b)3^TOTKtm(<ow7{cT)KWu$=Gv<;}F-UAyEw)IYwyZg`Nsf9GcWmoKfy|2|_|`qbv#-6!tYfd8^=TllNLerFOdliXzE5012=V}D(f=H+>rMK_!uelF~YR`jV)^YSv8HO9s14}i~)k13Ghw|CTg5$*@a`Noe5>f*OUn<Hp*8ru9&QNJQ+X9(@Am&rgoBWNdvc80usQJd4yW(;i(dHJF?htOsWZ4P;PnGCcaL;EqbzrLtnx$XQ|D8{H8_6=d*NHIn^8O0b0W%%ty<0af)G+sFw#dzgp6ywGBQ8r$D`-S7h>t80X7$d$f!ZG4y5dEgs;q-f4kEXw`(w|-fITYe)A9(Fgqy2FD*Zy>SANuWsheDZ;;}hUzKvcCMn#Sl#_hfjnI8Od*)9sVt^91;p#PI_lYWIToD2U((LDcR|zYmsNoyo-U;~<kDar_W?p8$CSiQ|XE+oHeB5<p4rhWHHR9+RM)1W|n;<QE~7A&uk1AZr)|?|S+xFH@kL0&$%D%FA>p$$bSQ$?v;BIU1rm#I=x%aYBap7;>>v$Pi~kF6Igu;&sTyZXrY554jvb$dEsTTrMGG$U{OdClNBl$B>JaLWVdSaxquP5U)cnb_*Hee#qqjLWcYy<Z=liLtG2F7$;<ik0BQ;g$!{v<YKOnAzp`E>=rV_{gBH6gbevZ$mJ43hCC$XauOj!d<?l*DP)MVAs2In4DmYTVz-bX?uT3sAY{lNLN1pOa@Nl?pNWfnCLdFn?-j~q{T}n-xX6c>$ne{<{*#XvCEK%pn2$Al{ADpKDvDWr9A~jFD)P5{KEQmkP$nCvm~YR?XX71<*Ft$-CL1?d4$xhcBeB?oi((U%$;NsX?_^_FUleOZV^`0`U)k6RWs1hDz9<fg#;d+4{))z{z9^21#;d+49}taKeNkRfGG0Y(4!PK!=Hk0hrfBTyi*l!uv19Y`p(Sy=Z^3*#AIHgjoW$|{AQp~-$U7Dy?s#|=#&Ha<DIhT&{!adyiQ^bPkB5J!)87?37D{q2;{Fh~>!7TIs7}5Iegc%_dpPBBoXp4j!P|w1PU83gdY7Xtj+6WMGV}4t^!~jWP|koXqn3Ox1eBv8uXt(1!t`xxyF=s5*Scjq@x@cq-nKpA%9{73eC?{U(}%rsZ#edcz0xvH|Di4Y#MQgQSC;K3<)1%xE|q_~?O)w8e)jPTXub8neoM;Z|F(^`zukO6%G<6xKiz-j!y#Vtq?GU2wLU%RpO1wL4vwUJ{-{KH>%7OqXP@hqa_h9^RQ|ieekA3up1YXV+i>@PN%_~m|9bk^<vZ|C-fNF!{6&0g`tq8~@s&rcld^Z=9q9{Wm*Jl-OG)|1)9y*X^YW#5>oz(6;@<nH{M1eBq})B|L0a$lFC?WrXvRad{kzRJDYw18C;jMkSKzmgUL)n`_TA~9Zn+ZQ^Hf60$G?16`t0Yf#2?%)=MkOXpz@RMIY-K|BW|JfF1)!_%1=D>Wc`Fc9Ura!*ChOnW0Ux)mTBp0-`knq?}KykzNTs6f@kb{Ugj-4690QxpXm7=M@GCnFEgZRLU^6!M@Os~AMx@snFlVsC;hDHM{Q3JDUji}|KRGW(GWP!(ZBvdL0$ZIXmbQ@PD7i!i~1EoJ40w^D3gJ9M$k?S?JSTlYI7RejG@g1@<nY9q0JcDTp%x#f%ao)KZf>)Mg7Wc=f^@ZM%}P4hJ7Q&80BOXV<eQ}w-=3<aC^~s<zy7&m6K777vD$Oc=7EQju)?gnY?0*_`V3oh?fC>9&)~2$PgDoE=C9$;!DWI8X-fR3b~jiWQcbm7yE<^aWmv%sE{H4hFmNbGQ@?DixEPG_!4rlM#vDSLM~<r8RA{Y#XccJ+zh!GDrE5IA?MqL3~?dkVuX+(zJy$?5i-Q7kc(MDhIkipu}{blH$yIl3K`;W$i-qILtF^C7$IbcFCiCegbZ;i<YJbPA>M^t>=QD?&5(<sLeBa(<|}ZKui$+t^EpD9?D@`o7cTN$B{KZ>tl!}MWXbld|KWWsA9t9qj*5IWAHSH-kBa;Z9|xH)63S%#GxKRV`K+I3aY`u9%VgsPi+$ZixdHRZxX33{nQV+>eqJ_q^+i5bG<Nk|+>wo)P^M_S>WlopXuRr+;*My%>Wku+XuRr+;-F}}>WkuO$#@mDIpktinu}{fnWC|)FUlE8#*W;txOu?c;lWQIiWMAcFqJ>@gRN-=hZ>yz-MPQW9aF-g22*+dm;w&VanF5m>igpM4By`U$h&uh&+i<BRczb4!xt9?p^D!d_p7qJuD&lO<EvtFPh))f0wt4sk2dvPs^WUC{Zi)IFJ-R%Qs&w(Wv=~F=G!k~GG?(pTcRu8`FA%Rzx%dEm%cZpTQ%-FGH*0=;S1invgBT)x87KX>o@HRRWdg}JuAHKz|FW&UM`bwf1!+|Us$7GSfgK9qhDB~Us$7GIho9rKytNhFuelU4~>LRgXvv6gvsyt^rLt245Po@L$2?U->)V2NR!{?A-~Q;t}l{xI`S)K<oCqM@0XEZF*^ngp}${7e#MNeDjo^-^{2niQ;Y7N*+BL9r}!)Ba{S=9p^=K;S{T%qV|dqJ{J{rl6+ivdQ{nuBmnwO{-H(Ug{K_B|*K_Sxa<*+!=Grf1uKiNx+An3k{URpqT0C%QbnNRV;|~#Eq%xoR>lXaV(g#Y;wQoN-3U|LdRa<7^MW4go>ElYy>-=`U{e?1;e&G)pH;dbhHTs1$`h_+6B|NVWp=b60dM+Q5JI6oFd3`9H#Rt>70}i9-^<ngPxcKw>&%1t<Cb8-7or|%Ghc37+eE$7~N<RCZ>%!3w&r>p*yd#{MnyKUmXI~ngh$btU$QzdjN+$I#3N0m*_TSQHf|7|IwtlHj$tNH6a86#veZK!pu3i~8kJ*=Nzl`r1`a(_*GA8m&pE4%(vT>0yX+IlZ5x@G+J9BoTVrC~QW_F@tW+y6UcA{ctCn{!kqGDzzDrR<~VrC~QW_F@tW+y6UcA{ctCn{!kqGH}oL`-~N*W)w8I|giKoX&8e&(Cj1Xx7BTqt{<pQX-Szju8AC!RHd0{C0%kcoC_)SSG(c$7#uNB9%<GJyD^&uwPN3e2GlRWb*QI8PY$|aq`<~d$6cI`R%k{Sk$lV_E060Jq|9E7q$l%$_x923+3f9oc&-8`@tIagEj02YuFFgupg{pKUl+lu!j9$4g0|w_JcL-2W!|5*03L}VLw>Iez@l#D*Y}d*|#u_p<BrF5i6z7M9992DgTs2;WsZ$qFc!KEs^IYY$$DH(&r{TC_UuR=O$uM#*k0HXX!*J$#W3o+1SZYlII}Ea}!gcB+o&R?^&7wC3y~le9zKsC}*STkUI`RbD*4qW<l;a9L<MvKAKDK(^v@QLbQP1p>Zmdr=mq@6dH$4hmw3R(^zyoS_b7Zv=kjje$yJtv(TAnJm}Y;cciR9fBW~6Tt1*;mJg_y<pU~a`GAU9KA>Wj52%>s11e_ufQnf@pkkH}sF>vgDrWhBidjCOVwMl6nB@a1X8C}OU%Gur&Q4U!>_o-PPE^e7M8(WbRLtx|#mr7r%<M$P%uZCy>_o-PPE^e7M8(WbRLtx|#mr7r%-e~Gd-BYlJhLay?8!4fsXP;WQOLz9DRXg3%3Pe1G8d<$%*81wb8$+_T%3|J7pJ7m#VILsaZ1WuoRTsZr=-lqDJgStO3GZEk}?;wgbcY*$mPjW=JI4Ib9u6qxjb3QT%IgtE>D&+mnTb^%af(d<;ha!@?<G<d9swbJXy+Io-Ac9PnI&5Crg>P6A}01KRx+RPyW-B|9n#U&#V8uGvwBTq|B`cNts&@k}|g*BxP<rNXp!Lkd(RgASrX}K~m<{gQU!@2T7S*50Wys9wcRMJxI#jdXSX4^&ly8YePc*^R6F-+<LT>x%Fr%bL-Jk=GLR7%&kXDnOl#RGPfQrWo|uM%G`Ril)3e2DRb-5Qs&m9rOd5IOPO1bmNK^<EoI(LMBJ1A^yEK1`A<*&^GW4Dx2>&D@4MB&L)UeO3J%Nh@*Pvc0e8<-^7T6hh1=g;SdP=>7>=3djxS`^{v)3lxmUqqIcDuwF>8MrPM2fWeih5^;s4<Jt<hBr8@pBa`GX7=$?)IXCzIj-<>eJJkw}K$E@^Y5(XU9OUy(+?B8`4U8vTl7{hIZ=f6#TV-|xLQRPnwSUI_QzwnxbmwjlhX`>2vnIkG=q|DWfT{O<Y@_=nT~tmNwlPr#r5;(=JjuWj-19YY2wdE?A_d`?}RlA9)BO!6)j6Zyk`u~^BZ-k-hPtYp&uch+xIGSS0Rf4or1M4w-qe2J3DxIFgG<w_>wd)U4!l}zkp|7Wi%%WL;suH>uk*caaP^UIVx?fd@-_do7SO13UM3_twK&nx-RyN2MU2VbD%mrfpwfAM;UlAGQ>0Z)6lQOP%kE`D?3A|==N^>el)V<La)W8;-f>UF}QN+#{Ub>N{&CVIH~#eaq>Ci;Bk#+Q{$#^vSHpHng!-_-q2D4E!aam-^X4mp1%WzJtone$gt=KPhEIe#T(&R<EH^H);l{FRhBe<fwkUrCwsS5oHum6SPuC1uWENtyFkQs(@XlsSK;<gCAvGUu<P%=s%RbN))ooWGJX=dYy9`70@N{z}T6zmhWNucXZRD=BmSO3IwSk}~J7q|Es%DRcfx%EkVwm`P4{@$M(;FMV{2^4TI@=7L+V2`_oSv*cPqemg>|m;WWS9&0F($!|x<ZmGrFUz%Pbli!XI{EOjpiA;VwLU23`$1S<$kl&6Fv<pM~N@Vie5rY0<=x53EP}%MEDw*tY!a{jrd%{9_VZU&pyih;5P+q8KTqrLbFI*@u9CutOFPBl+Pq&7Rb#peBme^RDv$3?q#?qXPMG_l}I2(&3HWqO<7D;R@;%qFE*jU8bSR}Erh_kUsVq+0!W0AzhBF@GliH${^jYSe0i#QvLBsP}jY%G%4Semo3w8X}`IU7q$Y^+<u#zcM$Yxps&;m5FsAHy1c3~Tr?tl`J7h9AQkehh2)F|6Uou!bMQ8h#9G_%W>E$FPPU!y0}JYxps&;m5FsAHy1c3~Tr?tl`J7h9AQkehh2)F|6Uou!bMQ8h#9G_%W>E$FPPU!y0}JYxuF840(1Xj($Ra@0&cyLYVyScjnoacKYkz{phnS?eurR$&)XHH=uK~&%&IG&O_(ZXJZJTk1nK7$`HN~eLnl_%;(V;(WUfR8p4;N9rVc>!aLAa+21|C3Vj)Uh5imY;jf^t((eH${8jWd`u(AVzlLr`A$%fyGrA3(1fK}shIRqh(PLf(JPke(-i5x2X2K`J-$dU=C&MSg-$vg-^WYQV@1WhlHMGs22R;Qp5#EjNM~mST;rr18=rs65_yM#RodKT+??n;t0IHL7ftSN4!V!8Ht%Og6A4ZR%Rq%=MW9SLc@hZwsfUe2!(<Puxpl15~PAinH=p6d|P7=x_YNOBZq@YZpwe)%IE-1TD2Ypg|Ba|D_dh{9eS+p6-&1e%Ehz6mpP;Nz^qra2B4a#k33;o@b?NDw<7tr55xfsfe(M4zk8jZdL<(JSG=<_?5LwPy6gg(D>C6rg9%jokv*Fbp<x`IBrb1jtDqN|aK9CSUD*Q4v`x69rD<qc>j@=*-k1m#WWMl=zfh;D)M7W8#gk1)C&%G=ScXfm3D?tt<R^bIr>O-J8?@>}RmGy}~-cSCtMx(m%lbJ6#p{2sao%|Q#$eNf(qzKiCgMQ9I{d(gdTAvzU31m#2M`)CO|9i^d6qX*Gav<&?a${(U`bS63rJqqQc=m%&8YCw-e`8aw6osAmNlTbd1euSD(FSHuU)#%6Ql*^8)Usr!J{>Q$Np^VRacNFD2zUxSN+sHYTZ~Dg+DSvz9Hp(@hpDX3Q`);Lt{BIXXdG#fa<>Y0&Wa#g6^~(4(``ujoW!(1aKXZDJF_WM3pZ-#2^`3fPZz;3(-?8|;dKoi4TzS)<q|Ee5<Ymmph14r!Hom0&GA4F1^2IZ9HX~vpPng+^h)KPKnazlpw4X4u84(jb5N0+bVxmtbFJm$;tX>(D@n!9oF|iY-2N^SYW-}sY^)j0gF>61w84)u*Fq;uE(<ieT5wme&HX~v-zRYGs%*ShP?Yv+eotI(j;$)4Pm*-{Jx;R;b=H+=Ac3iS%&C3_b6s?_SSSG{jC_WCqo&Bx2J^Xg=9*biA2=C*O94C^=aP5hBc}c$_US1}{=_iutIpXvjNyaPU#w(JHdnB+8tYJS`!+x-a{a_9I!5a31HS7m#*bmmQAFN?NSi^p>hW%g-`@tIagEj02YuFD~+YkArp5q|<8%2K;ul#Qb9Y-aLe^H41qTbQj-xXRR{SAUykk!qBY;GaEmO#d~6f(6H@XG%x!F2dL`Rh`;Jw~@I1R}pT<U;Av=id*4Swe4kljq+Lfmy<V^!J1M!u%zKGAw%jy&rx4y&t?!f()KK|2}~J?!Zy>`S+vXJ(GUd(mW{1Twy585l(^f6#D%8NSF;A1MkA;-^bAB-^alFG??L#=iiTo_ZjrJl+J?kESM9V0CO&j{zBqP^1X=Zw-yHBWk0=juZ*95YHnF(@_+pCQ{6IV@+v0s2>l>;Oc4|La?IrUV-_=$S8>nxYO23i6Lb}F_8?@?d0A%iS^W!{$*Y*ibM_!)B43V~Jb%n$X7VcTv7d7Gb7-{v&4uBOV}HF@#RvR*T6n`le^K&9eI|xKIc{LLil^<i!e@I=QSxIoM)+*HOUXpOW$!ggCiSkl^P5U0?SEsz14<@(c)c^N<O5zfE5EOVzwom}u3j1cXym$F`(-@i{*Ig;WK86lK4nbmW#b}a(*E37iy3ovB4y4_q|DiglsP+*GG`}J=IlhuoSjISvlA(Eb|PiYPNdA)iIh1zkuql|Qs(SL%AB1@nYR-W_dI{m^ZZ56^A|nOUwl%}UmUajO?r>zvh8!QiVs=!&G5f(J6XvWy>?4@&FEQ5{`2cMhCgeWrsVg=-9Vp%Q!$ah<GM*oCiTAjg0E!K{_B^yN+x<3w%Jkg^4@!M@-lwuyhn2N%6P-)p2)Rd#_Q^ToYRAhi9FM%j7hz0Tx3kz&&F56A!jF2=IlhuoSjISvlA(Eb|PiYPNdA)iIh1zkuql|Qs(SL%AB1@nX?lqb9N$S&Q7Gv*@={SI}veD{?n8H^yEK1`Ohbn|NMV4l7s9', 'farming-static-hand-roller-seeder-01': 'c-rk-dz@TVeg92f<Q?)N<V7X}h=JM7+{fH|Cy=@1y$eY;WYh4-rpxT^-Q6j(GwYq%JWSVufVNT^UV;Hc6cwm~LQxROE`>^^C8Ai1){4ebX$4eNs!}U{&z-qDXC`yb+-2jZ{*m3!{m%E?`JHoq=XZYR_xs)1*`CafjpK-D$4;V478702+OqXPB$dxQg~+M{ksc@OxT!+UjjW1X*z4x9xqP?>UBYWKPPWT&!_6yO!h7^atx-24(a0Xh&8Kr&2&;{;$Y3;*@5BI+Rk0GwM^^1R5Xq+ca4*v8y%&vSb6wsW=I+7W<<^0Sv#;Q$@=S})Twi}K>tqY<ZZ5;Rwq%`f_dq5ScAb<P?oYW_q_aKY{6K$y&Mk!ZrVG8{RJg;<rMkl1>1?{-g!AYaPG!5okb&BTy}5>N7kY&APO8wzRPA%}y`H8e_10n1j8ky76-RF^4i3q>nsw%~g>-fxH;@k(defa(H0(`fGENti?JT6SJp&o&+}WGz>u}s?IGb|a++L=B0rpK5JSB7ePBvV~^{?#66$-h&u$%77b4n_llKxaJ=+f#qT}?T*z<O%>i{o|8r@NeRe<p>y-7Y5WatHdt9Wb!3+(1un(clC9Zn~$p01cs8p1s{aknaumLiLQp>8XzBx!LJ1ly%+ib=t`6AIP3=E}!pUM$2Whuwgz7v-EQM<~^g8wx1cDt*f*^PvKtADBfaIo&0udBN}dpT+w!Gi%VWtn)Q#vlzLfFCjX9Y>7APHR3{YfDyrq3mUOn@^th=^IN!@oP-iBW$NQ;$Y24}^=-{0%KBCFRSmk;QaWO_{E)B4Tb!kG6z{>2+;l#t+-BdQu;)fINant?Yxr7QGPGPTux4j)NS*Un$5r25KjIvtZfZq0P!bqMXoxSNym+K%h?TST}s2bIxdNdw25OB&mdQq=E-Gwo_Q*IxoYRDH-g>+{F+l~e(o^jlUJPsLNVhTbRHWw@EO0$z)jC&22;&!oD`<`@uAeCv)Wi$IDs|xOb6OH7s+v#k3SE?}32Wf<%vZt~T1y3%7FIycuHw<H8Yv4v~lcK)UG?YA<`FqJ4Ot+#*Fth7L<#y(ZE<7Dm9B7NAx>Egx^d6@zvI<+D$ve?-TX943X?Rgj&HFjG-3!H)Z|?7ej_ojSE}gF&&&gt8-mSLCx=Yt>-q6|>VfXVXwmfebMYY%+EX7H6d3SWK-QI`kiv2e>U$S9+vHPC1v$s8y+K)wXv+nYy-95;*zqIS{r&iDGO|Zu{oT2UBcC~uD6=9jB4-VzRJB!(+D>u-Qaav*FE`M`MBY9`3ePi0mbZv6sdoXK%hr7ioAd06ux3g_PCi6U|Bb9g7<uW;UBaF?G<gQp_%#6p_kD9Pzs-~)XG}fqU3GYWYw0PW75+?2`YVlrN)f7XubTz6lB}>!z1EMbuoa;|oz8yDW#c4E4SFE@-$lP4KsA6bqZ%Vm)oP43B6E+{^x(wY@*EAHYKvxwkK`ZK@=vpkUD7qPs)>^(`SyoYhMM<c!gqo<mNX47ef`AcMG_%ekSuko}k9^&Xb9o%LEtV+isKre~H7z6I-7DI`vSMZ;W-5Z^X?khLV_G7PO|Q8;qi8?XP*o$Q*IgcqX6+XvGO-9Z%H?TAOD5oGrmm|7b3nbgx>!7c*$v&>J-uiJ#k4F%OK5`KtGOD}EINpySqamO#Rt7Zhu~aU_6h1LEC*Fin#HN2c&bov(;Wi^$6M33me%GS%`IEK$+xy_-?C;i>L48dbhazq$z;^>35U?&Zf47RRZ`$dweqAoKWUtwRH>L$T=E2-)hN$u^0QjvrHad#z_TVe1IPGj6-6?yxGD)ev7&M_YXKK5FG7OPt#fn7D^_jrldF}JSCtyUr!%?ftcvLp{B+u&_fVAT#C!RiTO71wpu5{~cOo--r(vYD+OfYMO2rkNZrmKmBK>Qg^817#pcI5nC9cNfre;PP5SdGIeuQJEIL#`jhFW8=9(wWQTM5-v6hlks=u+^MiR|34PV*`-UTLMi(z5Pqt?t@LcOy2^y>;E1&1<$FGk_+a--?xuR&5Lz%~Xp~+cK1xswRp_uOy`^ie<zMgST0YA&yO)Os*7;M>0?yE9&)EA?qHOTT#*VdS*1_3h0(^#)cZ{UV&YT$raUvkuX(O6KQ5;O(b`{TJEbf#;R(DI#x96FGAMcl3UTLYs7?ne$*jlU#zwvDu{|A&`gN@sO*f#j!|7?MQe!FJJ7NEtC03r<Ywd|g20T58q^tUc+%*6v8EA^hbt=D*nCl`6A{!zOzKR!88b~Ip`%{K8gz~Mh8EW>3pO!Wji@K2uB0|54AYFm?@TL(5NA3Ka12C8LpKy9t|=zUVN+4-nIRrv8PWj^xi_Jjuj@|c7>;EPcY?XBgy!8e3^R@tqDoB(-zkb?8{!Ea{{If#$r|IKOpN+aLZk8se6ivcDjoX^&SoduQ(&KGX=?FCOLw>TSu@+yl-t87o}CP}tWEvC-i@HW6*X4b+cNaZ-kPL$!l>$<u=L<_AJbb&=%eVaT2^Iu9EDNn?)g369f5EZhC8;qX;`DMyJ1!Dnm!8Uk6F7OSJW|>PREf8-rcP7xOmL6#$fokV#LN^c;pu&cy~>=s=Ut7Mq|2T`zOrN_zgmTmGu-&HPta}J!(^REXM{F_h<}Iz4;3JjHFuqk<eEPd%OYSF_S$v{$Lf++UBh^^~HOJ2tN;QN)6TH2cLRV%2%|_S{;Pne&~>tzjl$8^yiiF6>SG)Jjv-V<t5#OoYP;*OZp2rr@xf@`q$z#@^htKdL6EO<$tQ*lgik&WWIKETJpX_gHoBQ_m0;%RkG4`*#XvN2hhh3u&z;!GnppRIGTo6hT~`^erJQtqXo1GxQLcg7_Uq5dpcN%CeSIsQ)n)Yr%7}w@Kl;lC(%?|0$f51X$sAv<-p~%m`<h{v<$e6A~YTI%>mA#(+IwD__d23OTu@)Ea9u`ark8tKF;{+fP82)+@EXNwXYr)aew?H&utzG!u>Ut#;M7D9ZG$JaCQc5f4u@e6o7m3{FpWPP(6;zlRx;>z-kE}3cx*iTtgB*6o4n2j=q)j#|*%SM#;Ut{9JYT&?vd*Z%3Yc?g<G$9DsZBZ3mw^Ea8XiaTYs%{_DBJZ~bUnMLe`#T{e9GE1O2*ra;E#W%!un%U8;X;~po^&086_OESX&bQtF4WjYAP91bw1P|qOoJV-7Jl3#-4)-lMuQ=RRgI`5i4-F|Gt&f&@Toi%*=o;7uK<K%5lUZ`hD-VQK+wY+eAUk84y%JGFVb`2Rjz&N&eobkxkglifqfRmBUC*qon>^~nFd?v0rr~t+xTQ9)12-$rSay!fM%aGaU(HX!qkjG~u`=1Fs6Zw5Hay`rW%jqms3QK7Pa0NxZ%3&pNC0eJ`yGRA9XuS*XM}bka&Y^dc4%Eq_vnfV4&?b`_Nul$B=hJzlQ3IU|JeSr{g5tCuxSlqVK}p&S+)Nv3HLam7z%6tEt)*4e3~Z(rYN8FOT$*r&z%E3EvH{lwu&t<NF2pqptO@UK^{N|Is~>&uEiBe0Wt`Q$L3o{K0gO4%uE#a)X1nd+`-f$`>FDjqcl)G#>Wim)Ia<cq8fBd6<l8~UeLK|S>{Z5nJIJ_i2O0P6AmhFrWW3rA)%+dCz2ow%bkp+}4Bu!j8LpPO;^ourx%aOREYtqv7W?t-r`j@|gUB3*n15WKxwy640qkQ3u#X+UKBIbeD?XRaMkHp>V#Oyi_LQ~&uk2ZE0kHUN#v&?<t1Qy8R@95CD}gH^F#!>N8E_dQ_ayI`Y!a^15XomCW>59v_H@L)vw&wIqO(kJ4v@v;ImiVKzy`!(_RO~sxDc_J<&MR`#fbgP=N~(5;>fv>asQkOcrqw2jVa<ow;x(qk0*n2e_jC}s>lC;pN9;O@w^<@dhDInnIX?ZL*C~HGd%B`f$J2!!#+hIT+`ug^WlZ#aZU0*p;+Mg|3vRR%qyJ_wl7@X5ppi?NV&h)BF^O<A?NarkaKxQ$ho{D<XjG_$=PRgT-_q%T-_q&vd;jEV~*4<LeAAKLeAAKLeAAKLSAi$YJMVLpUBr^$=A%MADHqU<c34u8TjVm4<rw4yGF{No^&Aj`rwsP{^pVElOMhOIw`;U?i-Uc@3^HdKl3AZNjV$y))(%Ta;E=dKYUQinf@EU@UWEMI=!bZf8@3uBV&qq|K5!wx`}w}3(1i+%D8VU5ocriHWzWGo4>yz&erJfZ!OL~NA>+g#(h7Lao<m5-1n1uoY_joeLs<L-%n)R_Y)cS{Y1unKap|YPh{NplX~2@m5BR(BICZF$T;sOB7WnuPb6C&J+fNHzcYA4az^VlQhw*>UrG+$e|A#FADHq+^0vFLs>|=Z=^-g+WA1qAds5EyZ~w~MQqJ_ZW=*kW{N4p?>hc_YW3@k~h+q5FIjeo$L_B@gJuCe+%D8VU5ocriHWzWGo4>yz&erJfuYe~xKM``yPlTNF6CvmPM9NFH5^~N@gq-seA?N%=$T>d|a?VeLobwYQ=ln#<eOrk*=O;qW`H7J8ej?&ro)U5{PYF4fr-Yo#Q&L`v)k4nYDIw?bl#p|IO31l9CFES55^^q22|1Uiq};cah;w;L$hkZv<XoPr$=P!&S0@WOS0@WOS0@WOS0_t(sa6znu1*$mu1*$mu1*$mu1*$mu1*$mu1*$mu1=P6-&P{d)yYE6)yYE6`-zDA&tlcju)qE3)5*rGGv2*lPKevMhGoy@W%){(a$h36Z$oaVTBdwo{7hYvNy=nObJ>;hHP>ZV%8Q@h%kom0p;|KK``%o`wdN|{_jDevrE~ed_;Zqy%#ci`G}myYd`+E)E9Is8K2&SpPx#LX|2g45C;aD+%zx|v{$mI5A3K2m*a7^<4&Xm_0ROQA_>UdHf9wGMV+ZgbJAnV#0sO}f;6HW%|FHx3kA1>_PWaCW|2g45|Ns8ObN1f@?63Uefz$C?{98Z!4*~XffA$xD^8T}+_&pP%)4cDTu<x!Aoq<>KzOO=bHeSj5jtWr>uY_@9G?7B202PYUI68?;ph+rCrm3_FxQZ;AMl&f1OwzeDgJ#nj;2K&@C(}Gy4_r^@(_C6Wn}C~Wo%ijRW?(aIq(!uZHUl@)1+<iwQ46qzwosTNv>mvewt3&o*$Lc9t#l@>pi6<5(x1?~DN1d?HoAn)p_SAQY^Pn+NE1j0>hz~%kVc)rPU;3rP#Ty<D?#T`2ADzXJhCYV%%Nq|T5^FdT5D+o4FCtw+CWXT54aDlCc2Og01u$WzW4Y(;QP?pN*B>pz^l-@h<4C5z-!RjK^M~pfgeQcV!Dhz1pE+Mm(gyz9(X-kyXkVe0eAyimqXufU^iM0rRYZBjr3vapdPvncpKeBz4T{vJMeb;2wg#0x(j$0-9dfy9{M=&<MdJLrviNv_({5(^0b%k1>Q^d&>q@P_XF>zPt$wp&*`(k&(h!0ApHe>4){5GfUczX)5E}r>GO0oeSp3Q{387wT}yvOUjlxKzCeFTe@#ySpP<L+Iyy+hz+w6_{S9@|Ex=o7h;F5u>1p88^bFV`dKUOBT8HRPdJgy;T6faN=y~AtXnl-6K`#JbK<g9qDf$-hTWEcX?xSx5zm3*?^cngt@VjVzh90DsfG?r-AU#A!fk)ALh#sMrfiI)=2t7)#0AE4tQF@$y4E!-#kJDj#9r!w0hv`ZB8SrOlJqdlE0X~D)SLpBQ4d5H}COt*}NWTL9ihfRCrGKKgfN#;S>7VIq^gH11=zr-5eS<=wBe?#LzE1x_6GC6dMWJufi*yq3q|o@#ztVST3UEqjQt034-)TB<dT46sd-Q#p1)LR{5&8lBkmdmAgia3q2mOdn0iF_?8~RWBZ(0ak7@8mYFM5rZ0GEVL4ZTV~rDecnp~az}&_B>G=_j~O3;hrMf|iGVLB9e1hJFkDExiqVo5qEfhsK2_0w;zh11E>30jGs#0%wM1180Zk0q2Dl02hQ70T+dq0+)uuz%a&M9%6rQz3Rg^+n>IpYgoqnUb)Vm+2Bg~ar)kAlABk^xp{^Bczo}u^1Bd3Z|++$-2Q$0nCGnW{XhKoSOogm0rWZU-y11@KePCsbL>Cn=6U}yH`Dtz+g#vW<PY|J%lSZ-%cgo+ZYnPJP0I1eaUonY==YP!cPR'}
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
placements=[('tiller','agriculture-fixed-walkbehind-curved-tine-rotor-tiller-01',(-.85,-.10,GROUND)),('seeder','farming-static-hand-roller-seeder-01',(.95,.25,GROUND))]
def rigid_point(instance,p):return tuple(p)
def stored_point(p):return tuple(struct.unpack('<f',struct.pack('<f',float(x)))[0]for x in p)
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[stored_point(add(p,t))for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,rotation_z_degrees=0,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values()),coordinate_storage='Exact IEEE754 float32 after translation, not hidden deformation; native versus final GLB bound unchanged2e-7'))
base_mat=len(PALETTE);PALETTE.append(('SceneOnly_EquipmentBayFloor',(.30,.31,.28,1),.97,0))
v=[(x,y,z)for z in[0,GROUND]for y in[-1.75,1.75]for x in[-1.65,1.65]];f=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];emit('SceneOnly_ContinuousFloor',v,f,base_mat,'Single scene-only finite equipment bay floor, no extra counted model');FEET=['SceneOnly_ContinuousFloor']
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
  assert -1.65<bb[i][0][0]<bb[i][0][1]<1.65 and -1.75<bb[i][1][0]<bb[i][1][1]<1.75
 for a,b in itertools.combinations(names,2):assert any(bb[a][j][1]<bb[b][j][0]or bb[b][j][1]<bb[a][j][0]for j in[0,1]),('Whole instances intersect',a,b)
 contacts={};floor=triangles_of(FEET,vertices)
 for k in names:
  tri=triangles_of(names[k],vertices);mask=READER['np'].max(abs(tri[:,:,2]-GROUND),axis=1)<=tol;bottom=tri[mask];norms,areas=READER['normals_and_areas'](bottom);expected=float(areas[norms[:,2]<-.99].sum());report=READER['actual_opposed_face_contact'](bottom,floor,plane_tolerance=tol);assert expected>1e-5 and abs(report['actual_contact_area_m2']-expected)<2e-7;contacts[k]=dict(complete_ground_contact_area_m2=expected,actual=report)
 tris=triangles_of([n for nn in names.values()for n in nn],vertices);rays=[]
 for p,d,length in[((0,-1.65,GROUND+.50),(0,1,0),3.25),((-1.5,-1.50,GROUND+.35),(1,0,0),3.0)]:
  assert not ray_hits(tris,p,d,length);rays.append(dict(origin_m=p,direction=d,length_m=length))
 return dict(instance_bounds_m=bb,complete_instance_count=2,distinct_old_models=2,new_reusable_model_count=0,whole_oriented_triangles_and_pbr_retained_before_float32_translation=True,actual_full_base_contacts=contacts,selected_visual_clearance_rays=rays,not_navigation_or_full_space_proof=True)
LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate(vertices);result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,.55);ORTHO=4.7;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(5,-12,8),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
root=bpy.data.objects.new('OneWholeTillerSeederPreparationBay',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole scene horizontal centre; continuous bed bottom at Z0; two entire unit-scale qualified instances';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
