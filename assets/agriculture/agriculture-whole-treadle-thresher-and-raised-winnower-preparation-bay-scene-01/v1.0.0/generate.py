"""Whole purposeful farm preparation scene; two existing models reused exactly, zero new stand-alone models."""
import math,json,hashlib,sys,time,collections,itertools,base64,zlib
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='agriculture-whole-treadle-thresher-and-raised-winnower-preparation-bay-scene-01';VERSION='1.0.0';TITLE='Whole Treadle Thresher and Raised Winnower Preparation Bay'
DESCRIPTION='One new whole empty post-harvest machine-preparation bay scene. The complete accepted treadle wire-loop drum thresher remains unchanged on the left at low floor level, with its full front pedal, exposed loop drum and side flywheel visible. The complete accepted timber drum-cased winnower remains unchanged on a shallow raised right pad, with its open upper hopper, side crank and entire outward discharge trough retained. A single broad shared floor, genuinely separated central approach and low rear three-post boundary organize the two different apparatus without linking them as a processing train. All source meshes and PBR values are preserved at original scale through embedded hash-pinned whole generators. Zero new standalone models, one new scene. Not the old winnower/seed-riddle cleaning workbay: no tall screening frame or collection pan, and the left hero is the full newly completed treadle loop-drum machine. No crop, grain, sacks, person, loose tool or active process. Fixed illustrative preparation layout only; no threshing, separation, material transfer, operation, ergonomics, safe clearance, food suitability, platform load, engineering or safety validation. Rigging, animation, physics and runtime interaction not made.'
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];INSIDE_TESTS=[]
PALETTE=[('MatteSharedPreparationFloor',(.28,.29,.25,1),.97,0),('MutedRearTimberBoundary',(.24,.29,.23,1),.93,0),('WarmRaisedWinnowerPad',(.42,.36,.26,1),.95,0)]
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







def earclip(poly):
 cr=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 ids=list(range(len(poly)));out=[]
 if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(poly,poly[1:]+poly[:1]))<0:ids.reverse()
 while len(ids)>3:
  for j,b in enumerate(ids):
   a,c=ids[j-1],ids[(j+1)%len(ids)]
   if cr(poly[a],poly[b],poly[c])<=1e-12:continue
   if any(all(cr(poly[u],poly[v],poly[k])>=-1e-12 for u,v in[(a,b),(b,c),(c,a)])for k in ids if k not in[a,b,c]):continue
   out.append((a,b,c));ids.pop(j);break
  else:raise AssertionError('Non-simple arch profile')
 out.append(tuple(ids));return out
def extrude_y(name,p,y0,y1,mat,role):
 if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);v=[(x,y,z)for y in[y0,y1]for x,z in p];f=[]
 for a,b,c in earclip(p):f.extend([(a,b,c),(c+n,b+n,a+n)])
 for i in range(n):j=(i+1)%n;f.append((i,i+n,j+n,j))
 emit(name,v,f,mat,role)

def box(name,lo,hi,mat,role):
 v=[(x,y,z)for z in[lo[2],hi[2]]for y in[lo[1],hi[1]]for x in[lo[0],hi[0]]]
 emit(name,v,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],mat,role)
def rod(name,a,b,r,mat,role,n=12):
 w=unit(sub(b,a));ref=(0,0,1)if abs(w[2])<.9 else(0,1,0);u=unit(cross(w,ref));vv=cross(w,u)
 loops=[[add(p,add(mul(u,r*math.cos(math.tau*i/n)),mul(vv,r*math.sin(math.tau*i/n))))for i in range(n)]for p in[a,b]]
 v,f=rings_mesh(loops);emit(name,v,f,mat,role)



def plate(name,p,lo,hi,axis,mat,role):
 if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);v=[((t,a,b)if axis=='x'else(a,b,t))for t in[lo,hi]for a,b in p];f=[]
 for a,b,c in earclip(p):f.extend([(c,b,a),(a+n,b+n,c+n)])
 for i in range(n):j=(i+1)%n;f.append((i,j,j+n,i+n))
 emit(name,v,f,mat,role)
def vertical(name,rows,mat,role,n=12):
 v,f=rings_mesh([[(x+r*math.cos(math.tau*j/n),y+r*math.sin(math.tau*j/n),z)for j in range(n)]for x,y,z,r in rows]);emit(name,v,f,mat,role)


def cylinder_x(name,x0,x1,y,z,r,mat,role,N=24,ground=False):
 phase=-math.pi/2+math.pi/N;rr=r/math.cos(math.pi/N)if ground else r
 loops=[[(x,y+rr*math.cos(phase+math.tau*i/N),z+rr*math.sin(phase+math.tau*i/N))for i in range(N)]for x in[x0,x1]];v,f=rings_mesh(loops);emit(name,v,f,mat,role)


COMPONENT_SOURCES=[{'label': 'TreadleThresher', 'sha256': '2448a1e6b3f66b6c2c412670b45a16b123b1c292469c4e153e5437e9d4f1656b', 'encoded': 'c-p;vZFAd5uI_jJ3ZB_IMKW&5lKhfH3a5^fIGNODoRsa^**&@{6(!LUV~UhXO16^9f4_KuZjz#8XHvWOPEBm7U(sj)4WNPcFTecqDGg^~>_^u9Jc$D9CVU8{R-Oj_l)m}#)CwM!Nk(P&VHz}}Bw1S1bhWVZc^YK%AnjXO?&sme^3&W(;%L+Q<(FR?;bNK4_l2L&)t4-Z)!fhKQ8-rFCR2I12-GBrqF|DTNt~%L57InIqO5U~CJSpxy{N6F2l-528&}t7m)9P8w(!Go`=9=}_E6=FMmJ#;j7DyYAWEV&RkoIX8pL_y?CR?L+Oz#x8ctSGzM>WI0-Jh)O<G{HSXdJaYnp{M+a0_AkMql`51%ePyVGj7+IIi?!}Z5=&wj^Px~^d9Pa4Gf2<*HCcCPgxcH`~&)tk!?pRak8PjO(y!F{x`{8c_rQlOR5PVnAV@csy{n_0f0+G&_ABY)GfuJ02oO5&L{OOsVRr2(?raGF^YKTS8*O|nWYZi$L;N^4L3MPNn2EK}Av@Y9gGj-zC9oADYFf^M89KH%`<Y#pRozyM$-Lg&V!A6RET4=1-3Aa9a%K|@eY7*E4>I9>S>t#L_EQx7T>SkmMktpF+wAww$~CZAj5gnk4u!JZ~bPVk0to>*btM?-=FW5-EOc%llbUJ$-AD@iTiBEq3IQ($G%vd*kYvRFnz9#}-!b0W!QK+{K?`*{#V${;1V4G0JG)tDDPq2=B#3Cu|n$3&FYc*DrJSw)fNh%_OX69$`Tlon;SYLX^dMtw20ATL-f302ErN=!9Q{B)|UY_$X_(>Tj;P0PTfQF1Sxtvn2}5^PK{_Ok#3q761SWzw{W1_J54TFUAOh*TG26Sy<cQXcZ$(~Y9t_Se{F)RYvZnYv|NBmiQmh=d5W3g}AxJV^;T$&x-3#(XNy!eAXJYmrbD&>lPxiCEbrAS@Au<(QlRCUmXCEF2SFW<jzDaw5ZRdhgRV(w4_@a*x3$Ng4xwk_9PXAo|I2pq}Pfpoz60%GZ)W;3WiDlZZtUfkt4iGOUj};5W@26ZI3`WE|dhLKCrdu)qMHxDY(INTyWvHAoX#NY=7mM=RRenn3FTWMM&?fN&8IhJ8pb#kjL>f`Imz@tP*Nu95vGEUiIy_epxoy8y;ogjpuNiIBp0MJuqPFuwI?L{79{)Mi4+rYV!vY`$FOpwtDe^(Lf`vlWpP0}>InDdHNE-$9Ua5w%*~_!CGv#)y9t5G_vpr9Td%kUlQ_Dc2Blhc_V*av9EM+}Dr81q06%20lxD7SPOj=-9Fw@4au|`yW4C{Qb%s4Et|BU0k2Nx#rLB&pz|-*PkxW`NO+&lD+i%!^PEyx96kl^DA!H_<Z*9{QCOb8#wmwE80{-dhjQ9<Q>G*Sv<W0J-;UEwUyKAJXfvm3;Op`bzIeY(NV3=k*gg0&D>8Xi624oLhxqP^PT2%bZnoTs8;(qew?0i-{%;njlOS*vCkeNO!iR_f0gTQN7U%}i2k*?&*`yh9i5=hpMJW4Y^Oe-vA3_m+USASM@JZ1AUvfRU%11@G`O++>D2Mn*zKhO?MZCqD`Ilz;Q-P(wI0+4!trak<VG%c$yVciU7AmHS*#-ZmespF%cKiB_|kHk<XeMhs|B@tVrZ67)h>=d=nS8Y2i;-QryumGGgSIh8)a>&Rr*s0WgV%NA!Cvij$eQP9if%orMV-(`FiG69Ol(#yvEL<?k#PC1+|HZYSdcYC>lwnL`QC~VXeJ^V1bVt=Z1JCcOG2z(k)Q3<c~{yTo3y<ro$Z<-|?w6q=AxXwFo>Q3h=E5ceIe961?DBNZ<JPL1#F0-NRF>?9U%Vd?cQp1x`mrK}<6=JG1~RywRh-YWIri(}2(2DYdEs(${b_<#)phrn4aPDq2+Q4Xu=T*5Tc%!9Yc3Z|~IIpwk;3+zomig17Hy8EIb@o!Cz7c^%RDF!;b3(`F1&h9P)Z6=N8#Zjsiu$Q+l-d;p}!5%_-X1kIN`RQr`j`|=9w){O6RIp*W753`$)wwma*vL9Aumz3UN9+=Sfet_>oZyHW$KWNTyLYN=|@bR0;fP|YLd4?W5CJH7PNXcx3GsVGSn1NJc55VzP&}e_no6X<VfWGf;jcjJ@(%PlQDMrB7K8p{+`p#2hA|@2xmW5lr2$J1Sy)T|agysHs+`no0bRZKgJGYoX;pZ3S+#c|R<);v&rJ071($N1gyO6|;hy<2Nw84Cn)QkMZc<O^b)THMWEbKmWCWdw0rc<ynmzy?3!PCr(!Yp^n_3+q4R>>-dum_O?ouxFu9M3RTjV{qq;RjPEe_#S7=Ada>8u<>*dOs(9-@;^6;r@DLF!x0U3u2-ZI-motMkP%%@#xFoOOu2ZJ~&^1R5Qd7Z9)h;hGO6k1(31+JsG;MJfi4Mx2KQnK=<(DjRQ(HJy*KNTK~Qsy1#l&?#dvp)S5sX2rm(TP3Y$YT;>*}0R^5$zU5Pw+Va*6-L07kxdk<FJs})OS|&^9i`yTQT6jzCf+!1mq}P!Gea75La^jqnqtvl4lDL_LP&rA@naoL7Phdsagx<>FLft@-+t(yTwL(jz0j{ROXd~RYRGYTibhc#hU*CGQlua*oe5uLGaNH6^EsVMZhYlP%t<+b>8cwYN&pwo6>?_L+7U`Pj7)MMSh6CK*O^cR*MGiCyX(tY1HKu?5LF|IO{~9}nDx^MN@DETvawZ7}j*|zeixM>t>nB!aQCPzuN^p?QL;5)^R!W5(F6>C*gDz}yA)QUbZ5RelTXoeDbQ9-Tov7#Pls=KJLZ6T6Q&*i**%6l=)8{UI>QMXV>ckyZ;AiofOl4SLEG;Tk>~*?W!@b9+HdGj#9Uz(;kH&>&1a28;&OI&0ebsu&#K~Z^-Tq4Y$)S3$s2BBJuRT++BD}Jo^acZ{R7-`QPzhElea6SgB+2AF$^F%{@Q~!KLj8Je8jy8RYaj>g)&>vF5d^jaCTS17okOGl=pM^1!y*a{U&v1T4`KHIk2#ziJH#lbc|Fg5uo>Ohwp^B-3)v8C)d_!wYbFYNtQ=o+&EzM!<_q%-@y=6R19Zw6??+M(FTyV6)%IyXymYXSGQQBptIfean&2wozArm8!JMg5E++tnPtgGD%^R}l$Z#KNet&4IhmMR<0)OFkkCpgtymvlr5LU9Blkx908LVY^*gY_xF8XQerH9*VLOJ$XMq#G1(vn#qQ4Z1yB6#$J3Ljk1nu`{|$DS5-KDls9$-@g9l79M=jIxEKuhM3szP8oZP8~)2_ZND|BU?;sg7)&rE??}~WxXPnx(vhc$sKOou)ARjhu5IlQJo=y2;ZA$vnBg6iD&P5N3N*QKFIRaL328q=>R}O#owQ`PP$F9Pft{{_2O8;HZ{cuT+GHLeQ-&H%FuO(AArDs#>ZrQJ%vAM;ZNpaOeZ@V<c9yyMe{2AkSgndgHW&IO1y_`n12jrm4zJGBl(8jB<Ja1pl&7j3gyq(a&I4>RMtfcX+5U`DsGpHGHy!km2B$802EujaK+<L$PUcJNF40U$M*ioDG4H4ogPgu<`Rm~6ej#@DX;H~ZoaiOC)gTxB|LARY;O<y7x3dnx4J*9Z%xG=WR}BDR;Wy5m?Wva7xCLmG_d^KKI|f--KHIQe#H3Lx7m3Z6f}F!<G;a~dmRSV?FDwIrE;1rTCj}VdD-MWY#o7YtK|o}{B(<IE8b4)OF||eoX>FkG6}P5Iy0ErX02_^0FHkbE1ef`*)UT4hsa>yHQcwLk8AO~!9!&CE0P>-i5yO8ai=eZkckAk&q=@1%d9!hE%Y#sJXx*Y*vwWW*cv}tEYJ93@~y5=_zOz|1bS(IQmt{6VTi3|u^+zKI)=D8G0UQp>By`~{MynZ#YwEGJDF~(VuuVNz7&wtN5O4652sW3-~AX)$CTa2i(oSM<1ky;>bPBJZH9$cJz%}jtmSXkIms~@KFqA7@Zx6o!7{i05Z|`kC9KkrJ@!e?K#-=BCD6!7M$-PU-+URySxXp#2(vf__^9!{R<~UqfYjjdxS#q{D6++ALyAvvwm{JZ`q#k(ZJL#eY6nf*U)004l{#p)j*bcco#$9D{GCU~L$+JBQAP?KvD#6WHidc3e0ib2bm4&PykHHU$eP))Qdn(W4m0def;dkD(h{Icle)Arq8WNKtyiUT@UKMe(ZCG*TDKT#tNT_hx7VY`70WvZUgNy93v}&ZLHM~n5QmuQ(d>}LQ8e%$oZBYM19+*zn3z2ds&;}NT4~f%BZkb7Qq54%t%zUSr+bu!`0!L)40@(Y!!7-R8wz6Ll5kF0^L@lxfC^#GAimu)oTz0~a$gFpFLkw}Q-~J6bTj9EdHIIr%9TOoDlOu>lkE$&;?9llV6wTNF6Ht}E?eLnfc&+#8Il2EuGDlQ)K?=FA}QccQ_|xtz{(fiQ5ROqQ23A8Vc@j79g?arQsom4TV{sJCnAsD+B#rEd7tKY3*C-p-K+TB8b$VYOYLirz2n?IyI_yn#eo<q7s_FG+J7IrkCcV=p^o<`$^A4m0{9bQ^NL8&+)!MGB!hXUsm=CA^Npn(in_6dHrTY8zO=<mF{~n7h50m;+nBG$Mro@|^V@2?CF-e_YMs2?I=|@5D9*29MqG_1aj8Y>`$zvK=Yy*zwK1#~+O5;0irB8H*+#w|og7pY@?*09pOUQ={xR#i!VPZ0F@;;AGP}@X<-2$bNIf}np?!9`CB}(9abYTV<OTzLNo=dm&Jo2kVa0<-rf8Es$U<vRKkVdV{W>qCUxV+X4dL9}WI=A${YKwZZ*3|!R~QdUDo&DP`ql*?m8~WDy_#AH4_DrJ)Bk+a&6nIdu)xCIFs=Nwz5<zumq6ejcZ;ctz232jNJy7P(Y=nC_>4>ND^%^6Mkw4;z>l$@?n@@rZT(wnXu-6nHBHlmcgSr!4{GFKo)}vh7KB}2q5$v%E3T?;5eN+13&sIYsMou-SmvDSrg2N^eFC-XMAm|(9An$sdo@bgB)M4DE7J_w{;?)0^Zlir*j--dSXPIrtIF~_ghJ?{<UW*lk=sEvAw9d<dVWd+v{@73@7*Jec+z$23Z?{3n7|4hIzduzmC;#t6Xp<m)ob;g&69a$rBENYfe+(~b*_Qt1-#KA9JT$44S5MuJ%@4zYrJz(k(V3`Vq!q}79aAt8UjKD$NQpVOHfVniZ`teK20f05a4A-1|9<&5eO>K;J+!xyrdz;3a6HkgD=Vf%va5;Si(`cgh~)X8S27uSoIK>Vkw1;G-8A`inSkwQ&zJH2f>14C?=ap1X0r6G2sCw7Cg|voxVH<uqS&2C$|;ZGbomF3VlEh8KQ<wDP#V?2ExYSFajY+v;aL)FY3!$GNT2f;KKi?=3&{5x@oepb3+<eDmH~*giuK6OtTCNu_p6X9_&yj1F_%M?%2HLB*>ur%c@|h>Q((A(LR?{QpQH`!qA8p##V!L#=7tohx^Op%DVOh4e_cFA{1mrj0!IrN=URZCqf{M$e|}zaB~BiTO(v9Gx|qutqd10nAdd#HwpdVg&|PHG~_#6Ip5DF`O1%=Cl!Z0O_QXyN;pJuwD25OT{_^&7qov<(t-Kz+jGcFfcK1yiCI3Ume}OnPiH|+mI@9moY&6=Pbd*PnhGxS8^!hVfTP^38Ctw=5vi|&%qcIdX9L?bwTHw0)o&l(U3+qS)^uR%EC=DRyx!JL-2)go`>Wi;ZsAEEv`L=32ZTwH^ED`XTeExG@L?DpgRr4Pc=$$Oe}`qB$*m-s&=-_(FVWj)KDWYV_UQA#HoHU+V7ywH9$ms!0zX@&!D#Gf;bde2#fqzZqMOi1Bv<BLkZ!^%qr?`F=2EnBJr7^slf~jk(b{a#G6`dW)im7QENL?=A|J+?-lA@~4;a&RUv-1#^J02j^m60+rg7tgoo&`*c*itIZ7+)(dS-w$Sck#=D4P)1c{ZcP#Hb<qZGylKWl5L>vFr+Fov$?*<AC8%wSF0@2I-Y7d@<aU8(U$h5f8;TMFk#}gu9Kjv>(B;9Ko_2nSn;@FeBC+VFvFyT?KCA-KRHyT*=K|>*UDof4aQ>?UUDOy*TOr`Qh?>bp6|hH-Eo4zq<0sjBcMc-kkk@etCA~eY5lVYB7%eFtU5jk!l{RZtK)l_MPA4vy@8d=sQxK){&Irz~QFtvMeXlxyO_1g0Vlj<&sKAtb@IZ+Y^zn-pEu(cYA6u5?2rmrXmZYd9n)f9M||S_Q6?eQG@w=UzR_*dUN*ioRILn@i*)B$McJ~=a<&!-_EYiaiyT6oyW_K8e^{{78-`oDi5Q~L_`0Bg<`F;HD1qY{{qwK^*??i4IyaIU@f>rlJOVn*2)3|3yqkLMR3|z=O54CT$B8+HJt`9`y5ieMzbgxliDX2RLuJei*=nWchHN@e7|LaZZfyGTh>a0MY0Z@h1=jrOAk$;cLWav6iWL1vjy+Yh}aq$P1edbSssu9{rma#<%c)+{x%bzXjbID*OB3AI-K4uiH!8@H~)G=XgB>?C83T!EZfYZ{i;<2!PM(KZ)_C;5B}6&;@BH;SKKQwO8Pqur$L;AS<!$|wvK=^Y0AuwQ#H+c>*%STdc{-|CsP8pI-y=9Dq*E3S(w*h(oMj}{xlmQ;MKF=efa13TYGN{?|2)5;liH<C9XNl9+AF2nK+*>-q!}HwVotVlIl4x-@iVqwWh%qBQ|a%R$s69{GXqR9?##Bq>$~iduIQL&1BE)9&MVk&3@QD?y77-q()*{T%x<I8gSi^`e@V<sEp!ruo9<5Srw54mte9ewtL6l<ytd|Z^D^_gG)>Kaxr@dw6d;!6k1*Ak7;rj3y+iMBdA&LZOjMQdM^?0MPrS0YY2UcgzI>Il$I-)-`7SqgLPKgi-~8p#hm*S&ok7fCMLXT(je;2jB`?Mr9sGwuW;xP&3)!%9m_~tyzur2yg0aLwbtz~TGR06MwUq9c>I$}OQyz&+FyE$7QW&b4){~nBJI_&Kc`_l35gJ<*6XXc??_TFTVcFh<=Mb~?Pr1Y1_RndlGr!?D#}N!?&xXCrk4O83j0n=URb5&?^t3KPIemd+A9suqUGG*Y1L^}np{`H-K{?ZSRXqb+SLx{rtuZw0Wy7GbL@~YAm~V`9wtjV^8@M$y$|9FsYKu;;t=>yaOAZc@C22cCI_Bu84`4=zMJZmS&`DCSSvMRzX-rB27<ZjU=BDYlYC%<-ttj6CC!)<l5{ca5u?J0p<287FI!h?rL3ZPQ9V<N)N9R}R<MG`ZRb>_b;dc>eWjr}1%!1)xl-v{xycvOs-$EK&B~0N!ri-_2KGogl7Us&ZiGER#sGnXl&{uwwOD43=0BB@UNX83HksBSk);AY>yI~V|B+HuaGbVpbbv8<ET}LU=HBA4papGcwA`TH*)nw0V5q2oLxb%hw_Ppaq#!Yn?56>SVDZBZPG|s~X66A64Qou20KoAmq);scEWQcCcv1-+i+0?PCL=&KLOeT33}?L10nDOTQD>jcK#Y?o)lq2J0PxFoBI{z{h#sx26hI|=h~=SfwlC?ZF#=R)Nt_|5%XA#U{q^9@MD{R%#hA7l5Gu`AG9sVBj;IdglJ(QDl7Yzjm{2o9#0(Jxb(Bwi-gg5YAyKwphjb?bEyG$Fm;i*h%oez<(uzWr>&vsK+}+ZMZ1+oWCi7r&%VY;Rn<1ISXTQU!Y_BOXVN(&%_MYC`glUKh{V7L|!#fnTLOP@TIJ`-sDX$5RSsJFrvGXp%`Dw%!(}6^`J6Sl3N%ds*sBE(gFD=C^Gmui{G??+6d5b8~e^mw=bJm^iy4}ky>{$Tpwb_y+5Xz8!4C=KNEsS}Anj!dJQE>&W2W&+?HbWibX2ZYPF<WGMXuIfR_Z}Y(_7za05j9#I**ySc$4P8(JYu}sJpgMHq{O<Q^HF62D*aBN@x~7XfT5=?rPe#z&d-|M9I7QUPs4}NeUe7g{~?ViDfJ%>q!BVCW5m&u7e($5wqU5}gso7VNJOhniGy(JY(eV|y@8%g5?UrQ69;KJHK1!?5^K^bT(=C*Ea4sg2wv8t%-0dw$)kCgXHL;TE!7lq8l}78qeU}B1Oy$=ga`M7E`LS<e1EQkeWxnug06E9={7+}&2cBKgNLcueYF#aAI591b4YdlEaL%}7;wb{WEl<cj9T>X^aNBAbPy(s>Z!VuT0LD?f0rp&I(A?4$kw;j!TOcgIVcP0)ALvPt8TjoEEEy+rK<<U689L!@DT9cDt1NzcYm|Q11ga$1<vGB|MMoFC&*)^T|YfW0wq!at+R`_d>RMM6xVis8s?i8hI&gx5>9-a@pF<4(<a!1A>dS6&h*8p@24Aa@6%{4>krbK(i}dc32By@gtE07B{1G&B<hl2_a386Sz<p~1T&xXxAs%y!KI$$z%5B@U{cW^CiI~n`QDz4v3@kJ6_1g^){iE&;t6skXdbd_yvTnRjh{u61CteJJ|i38S>zu`2cJHVsSCq@;B_UofVd>?Y5;_=I1PiOWQ-IQ59G={4xQs?I#ibc;ynt3l1mEx52zS89XRgk$4U1kheDhlDUOTaZ^yVF=pG@Kp93|S-JWJkj+ZIsr~qIH6k->SRLPUe)r*So!f3Ah-(AU7<LLcnhZ*pMNxoQ&H|Qw7bJU~`fyRCA_cn&-u3a>i^W55-r{dTpO&X#{(1^cj3bo^g!k-ZZF6gka)x9#)XvT6I!fYe545rKxqb!JS@*t~Oc}ta$1tJ%yRyAd{bU#<vHWP(~2$I((sX9BgdPJb_Q6S2bQPfMjCnuxsktI<$9gz%R+pP!0lG&b=Wg|U_w3HTf%r(BSliMtjefWiIoZa~FP9*mwA#!!;9_RQoPrQwe=HMbZ*@LfJR_YJQ(2A#{n5t+!&e9zm4VBc5_th2l_ZGtZ0+(CG<D$5j`&W3BJIb*?#C+q(!KAeH#S&G~6pW5FmN@34am39=3(`44hDzDAo^Y{Rj5zB#OvsoqW1v~_1^R;^wj9#8d%m*Aq<Ub}boYdg*2rJVOtf!+;ya=kujgTAy^h#ova(<Xvb97<GFk1M4xbhNer=wyIUp(HB!nTw{Y=q-#*_=Eflk_{`7KQxK~_BBK?tX&vmjlj48Qfp*m`nVJx->?H8dbPup!yZRw-sB>W*oxL9TB%`92{lo@C$)K!k2@5Tb@mcCzyC+16*q$y<Epl~!p*fn`$vs#Z%JfMkzVY=I(y@M+ZqWV&8^gTJEu>{WgGlhkw8Yh>Wi&-T!5>D1meQk<nov;kcEKn5;bUz=Y=O3IbpnnYrY<lL!#OrrJm*=qS~yH`o1`&QVbpr--T-P$d6%Jq7vZ0zZ1(It9ITjJ3^?0zrx2V~y;&3Y&M9Xx;vlI2p9OtOlEqI`YC&r*LmmrPv+AxX*-b>M3QO`Mr*3^IF0m|C*D8<wPfZ>5Rv$>nb7gh@W3k&(s;-g00gYmL7mTWMU&RzhaE1<Ov#eQlvG)t$+BqNAHLp2nQ<gdHXY-$R!^_v6sh@P?_6YI-K!kwaiqV1}V8MgMpx{5FGG)6CO=-x<|{jtduB=T1ey6<O#_Gn2^K59nK9zUf5JEc`Do2z!9f>^W{hGmh<&fyj`VW{1u+YtoV6vKE4#wO&EF;UG2`cP6<s)Jdfhk60wz4&8dnRV5D>*T^(UQSxh7a)jCqHtw}JDb5Lw^fj+KXj+I8<X$n0T6bE%POEpjCO4F|p*z&As8AK()?43@k!Evx2ETSd1X~vfu=ZrzSp@XA1%uw`r$qt*IuN);Dg8HWBfU)p_d_huGB`+>S6@nkyP6<ia|6@_{<tgn;|~16UtPSLfaPvWi#tBJO0Ktj->V@Ch_r{K2=>S0J#}NMBUP=z=LCBQN;V%X2fgmFgqn`tdeK;~%IA8YKXZQIcwD*<FxamiO=b?yrJqmcBO}Fz%1ITz7zSthB*e*)$O`N<xsNqPah$NB4$w()meP4M4n`8V$OtFfZs|$P!q4=Ab+JeD5KImgVA-RA2r`E_qxP$MrvFn7#>E5;Ym4u;;$R3}VqR&nUTmppZgA@{T1m<Cr(e8p;vDEfiI-g~Jy+k$09;X94z_0RQUAdgfxiWWeqm5aLzD7xrJUNhjVvIu2@@fe%<bpNG!ZF|3b!GN`6%tlp0iPd!BEE8>F%(Jwmtmdp<@}wAc96If<0(1o=mtOZ?OCkmoF)aAJ|rv7EJ*|x7pI~0SJIbf+fh*dt4uBgLC=?<G_J$NV=3fJV^O?23P@lX}f!(pR3?4>Kjn%{x8w-ivu4Ywwz%+Je~dHBn?WZWhtWhksWckcm<UKBiJz*f@Hwwj@I6{g|#Y6D|Zhrn8$=q(N{j<_3CI6<lNxe18TQPra_1p?6C>fHnmlXjJp!v{iJPDaYni~Tdk~Lix<po%t&qCvtkZ3YRGeCq)2#t7+8h*mWwALDBmSv4MFdGD*kL85oU{dBJ7&~r_coyf%k!?5_c#uFcb2$iwBj9aa2K~v;h{CX-?=Yaj_qpc%W>g2iuGa+!Q0YjRgXJM!}lI5!-G1L$8bs`8mgDUD&vdT}8YYp=|f~fc+@(1}2QEqG0bRI7jZVKM%cuiNyL*Te%1G2IAzHht#DRB~Ykd?rYzuM27Jj4D9oGF7#rU^p$r){4V+a<J4Jj?)G25#nn?Rt7Nl9HF#PiZsnV0(8_Y)4URy^zCQow$aYKVx-%hJvlj`Bv`H{sr9^C49zruL+?A}@YNKY>GDsI;PONC}Oq+pxa$I5Hsw<ES3@PMY)Yr8#lWtO3q10|oATfA_J!klG>k3<ySI??)U#;{-v$8*Yx}=|1%V4sK{M4ea*2e&G;A-zhv$EeLeqQ@l9T%~*mDa`GvjJz%Wi*?cd=FjRS+i2QeMxN^W!t$Qdmp4ab<4MoxDyMmxu5xYo;qBj>=7cIM%Z^r@UILZebgx%6t!9HX|f_IGh*j}t@s%?zDYxrn`i<gKuG+Q&$|eWGLC-pBbX%VG;{Rrr(5?MF=OjWR@$GsuUco`&&im-tnKe2cTymi-OOvK`H!pkRX-7jgX-772BEx_6%O}E3Ri*klUnr0Ag|r04&BO|Oc|>$$oeA$XUQt1ZO}OO46a#DlJ+3AH%m`HpW4die)r_msobw`kDzoEdP1jwLnN&1p6$9VlKsT<4t<&j57Tf4XB?dk+YzC9(jUhRzCAZlgSCs&g8^>BhrPt~f^H_4TaR4Vnk#jm1Ipzh-2fn7tC3v8&!YUsF%caeLbgBsaeZj>8;(>twq2#$n*g=<A79&wuZ;tJfzKL-X|^F7qWYb-KHA9La#3U+M9j9!`SDA0Yp3HI3bfrXB;3Tu{cjip<UMf9uC>N+1kwgI?tJf?#EIBFjuBDzSe%45$5Rq?EgirzqCq4|s#F(CkH1}B*Yk}kA_L&x#8zu$+r4t*X&OEn;gyn4WeF=ly(lS5{0EfGL)Ea#D}EZUe%p&+FG)-xa7&9!`$EMMA?=rR7g6Fzx;adqWF!txyQdk2b$ZMw&wIkKTMF=YuT%KROV7GijS2_5-Fw{mu559i78ci*d1UvtzAAfLYa%>uDOa>2W4;xtEsas?a7BYc35L3iOY2f=#zHkrf(NmxIigP65=wiqNl6XjylN)0Iw&^=B$q}aEPzNYMliSrfmo)fuL+kO&T1hHXf)pB5aC-QM3Fh8!w=U4NErxp6V7PmI`jv7m;3pO)?m}_O;?j3E#HTgxb=lk3acfxIqAJQYbbo-V@n_(rnvJRw<qx3`OP!{K3Wil1mt}Rq(Q(`#p9i?Ac9H6b=?E|{~*IzQV?>VqlIvsfjv3wLtf?JXN8P{;@Cie+7dL5@FoIMx7e5}bld@}4<-howcK!>V29&HbqIWGNvo5qyrqX#$xDjHx49${NX9inpycepVF*|UfN@9?144zUR3t}sSb69A@EePf?}zJe`VH&vhu<*#cYqy!B^z`Jy^=POevME<<@*U@`8WX(&ZYzhE}pd5(o)Lq>1jz85DsPu_yt&m>P8?i#D5RL=b(utqa}c8Tz#z@u;R&UD!up9MRQIX_$2j-d8f^F7)7MjqGOn&3BS#a;E!yQhD)~7dX?9=L53p8>>gWD@DUH}2O3~Q|GwHoCDkrpntJwvcI~HxEbk3%N62jol9%ibnu0XjAV!F-jfavs7b~;yMs`ZfLsV{Q&eOE{G+|G7==yKgIU%3la$We*A(_<C#uB3ACo^t1#83ENUkO3Ahs(yiuPo1Q`!U}MA+=2o-~ShR1g4!#{g+R9x32>SD^{iS)u$VnCt<V6L*~HMZ+2nMl}e81l}8|3b=!)U=hd_-`yC=4EmA2gBXvswb|~+Jv)r{lzrM7{Y*;{O+jOiW%o9^p#4d|P8|+(1a5EOE9MifKm!b5{Zwa<gp1}LPZ-irmR&O_(anjV%hVio@1uLDcVF^;DnXJiCrPT%;X=wywpDzj>`~CSRBw+k&ba{UE_FuLVJ};R;Gff|Zki5#BHc0XH`TGwS*4ZD|zkRy=@W1D8t?Lixm-OpWvR?kt>05Giz|^t)2oh#vjbV`SSz`Hlr~5)~sE88N5y3}#y+2dh(kgPpXvHYke%Ep>Cc#RYQ#;R8wOA?V(aOu{gATt@YuXeBktyK!eH&QC==0^LcOO2Udj(vCR6%#Md`6R7o_+lI=}%5(kheCQ>yF)XI;Uzt|Bkxq^myn>WPB7nNF|jHbj^1e<m$u4``T>y+!TGN$-+g?_wmEkwFKYdZSc(5>4U~icx*`=4TjJ>x!)%e)|VehSU%ZV5)zuYK1@Rd`78U|_hO8z>$8iuXP0liK_$nllGs&da}_yUW$sojV`~UHuHw23!l;&FzpHp=RtAM5K18UyMitvF#!+}jcJBVBW!MKH8qWeu0%sdp3de}P-MHn4U9If~MFg`RiJuG6sc;O*?SFX{WQl)?Bp0rRLquwba9Y>bIjACGIOq%?g%t#$u;1eB1cevnB<4);Pgz#nVU%TDQlUh5D<Lv2fHMSu3s)JXy4=EHRnEn{TN$`l-C`-KBdl7b_iM17(zl(*_ek>I{)|0BBLp^Ry-;RZPHV0naePe$^`yq|pEU@-vY9w4k`L&Jzrx?jh=XW!)4iEYPER|Xli<aR&dbh=X}dd~bOQhRi}uTtBRIPXCAym4#DC0WC2Gvz^teqTp*@t<kqHRRr)MYPU?bIRWFVn$MhF#&MW|;NpxyiS{d*}>^*IiqkU9KQ3sj(Xi~Y=d(rB}@Z6?X7TBbK`P$?UJFMDGDi+*v@Iv(z!lkeO4zYOLpuOM4Pc9mDJ8Oman<KPDN6-p&z;K?;MtV(8}xkK=_*pz*6HBN_@mz{i1@F_=<n5F1RelUw}_7?=e-sDF8yJ49`r$LcxHY_Xm5dC16bcXEdJh0hlDSMOFdGYqCgMK@uu%znIgGUtIf2?-%WbHCYk<>zPd7XA!Pr+t!J+Z1<Rr8d?`#ibT?uKEJgS0=P%4r?(TZjCw<2HVN+(%QIS|$TkvcOFOC4b`#Noe$*eKz~2-MC36tIUMuaTd0yF!_k{*1j$FUA8PL-qXT#5jo(83nx*_gg8HGA!35ndHUW@TIP?LjDl4Zq@KfbH_K)&5>t@!b33|QktJz2|CeOWzick&K8{-nuuKq>iNE>+V^bT~e-H3SKAN0`ed?;ycAMX%w%?I)XXCx<W)}rVr)_oA;y=TIhqLf#^|7L_$1jiq4g<Poc5o2d2=~iu3D{?(yxOX|K9m1roRZS9FBf5+{aNSa+Xwh=k}zP=&o&+}!<3Pcj2Yg3xca+Yl+g-3{OFhXts7AjAE`JDquZx1`=FuX8a!{fm(4Xim8_5R?<=KbQq7YQCr5i+XR?{NyGOqYa5$}nbbUHXa0p3U3&$>D5nbAm0&Sdf-^4xl5gB6o;o?1DOHB=O?am^xI}%4{WA<3)WYH&sn~aRgSuKgu!5>?}6P0-2r(-~=52d~NGySJeLVp$~8M5lK*k5LI(s8OOx{Kbx36;6}f@zJ{T~bprj_CNWT;u5CEl%FLy4lxY=O$<WD3Y;NUbt1#w*KPvqPd~l1qcq3%4D`XEJZ{qNWM1`{deI;m8%R4>Fvd1**uF9$f2a?a9~JX>bPo9&o(PlzI0=g_BGrMXORo3EXRRf0i+mS{CQZ9(zlQp_K~Gj5)6Oh=GOd~4uGz9=wt+bRE%2wV-7r#{0#~ddqn-%)T~^izActgUb6x-2yW-+9r+T~(v{`iquef4M&BV{&nrL6n;|uFhOeUpd><s-Ki?dpfrY1AXIs$J4l{iL${VK~rUrPbBrU4C8C+G}f{K@>MhMzcF~e*@$q~xp$f>|qC%YDhm^fzhnA#bDUh;_4SeUjqO7_A;m2QJptZg@ml7Cj#wU-?T{Q!fv<|jDA^YpxhLb;bMJ?}Bv-^QW%udtg<p7^jN8s7FpA!y+|i2{c}4$`a)9{7<9tukMA9KC5}>hX?)?Xc!vL%gKV-eFN)D=X)y=uu^OHs9b_y8#l&%GZ80?PFuY=M|626*DIYHE%oL_`=Gdk+)6!b+{zb+p*n&XW8%MgJ(~prrPIwW5$n}ZTT?vxbXJ4FRHE!nnjEpH0)K0z7+AjpFB&Rd~U#Lo!})P`G>euw!yq_w}okUJ1qbDk@KX@J~V*K5&55RC%IyJ66ThoS?uwBYKW^36md~?{$Vi=-vP5bE!#5;hdNf_W@n|r%44=S8F54r2vqv^y)Tz&{1HU1uhukERlLbUJVWm(SF?m#%MgxH##!d>H;}2~aZM5ujg(qyz@zkkkciDGIATXY?W`FUuoPfB1ZhlVqzLn^h-Vu8k2ZAl`)(ZgyHh8BL&ohdb;i@b6@m8f;0@L-1gkS7Zqd>_8n)S(2CL;xtwx+tm=8Q2<e3DNJUqyIZ}i(e>^7?nD-*g0tEKL+*+>Way|=>(sR?^G3cd7HO+B^JBQ^EN?z2v-b3y>uU**}pdvPj8KV}oE)am*r_Tev`0LJH1ayHxNR=)LDeT`L8nEXt$as@^rK8kdHyyg@Qh)!NC$7$wd7nZSRpj3_lV&<&q9Q@dszBxjw0e_dE1pd14BreYqiE33`HQP^&q0YKr{LrF77cyw>7dsXWUL>X;FXV;M4yT7$I}Z`yzbSD+LR7un;01uyk|*>`+?5nR{dfg+lAhZp8n50y5F5B(#Z3`@ijEZ|Rm$}%2<FqS?zOK<cfViAa!ZA$Xj^#$qNZQ9rOUmCwu@xShj$I#S{BOV0LsSObnh<dM8X!d_(gTZ0(#qT)=?EUCJo3Io&@4XlA>Tu#+&36=!drMTl#B<gUD(kmM`pC@!+ld8~!}8kH2+mEqvU~;`ru}OL;t%>64ClP`*{smn30plUXs6sPJCrtqjN4wfr}UX`_>S{v!;$;-<ls8Imt`A0`3ci!-P4T`?}Hk>M?vCq!DDXj^W4Z|98^{gxZGRnug&iuq|;{epp3H26>U>T!flgmRHa18)N!^vyi4-K#(9V%~|PZzetJeo>8(mF&dDz7gt=%`r_GP2#U#`vB50?fdPIofE|s0<OK$rS5x-b5F_(MT?5Gu4R}4IZj0(kAF4yi2yFB;L|E6&Fgpb;tKvWz@u$VuqwCukuQ@Iu;Dm~a~23P8ud$fM*JO2Brlh)OUVSahsG$X$)v~3t^Q-y6{Dpfn0+SBety@Eo;l*VgxUVXUS7^)2WI|*{@qS-%0BJj<#)LG5$(ra=H+vR`&{N!t2d~6>J3C76_+ghlt?WO`)97nkhx!zbETAf+B?&@^NnWst<Y)ZD7Sn1gR-~c$T+@`KPWpu+A5h+MVH-!|LXee@|xcTtp(ti7&9FJvkV`Ch~)xDz#t^B$su@U*cnGt7?q`0Mn*JDw1o+g;E;&Xn@_)g{&;?U{%D9q<NpE(f){)', 'offset': (-0.86, 0.08, 0.072), 'seat': 'WholeSharedPreparationFloor'}, {'label': 'Winnower', 'sha256': 'fc69bd11dbad44c4ec7bd8ba34da96dff6932c8225e9bb09b25389d1255b41e9', 'encoded': 'c-pmn`)}Jw^5^gRD|oZ`f@IvHCHav=3J2#TPR7_w9N3=8?&<`Bk|>D@CCVfv+X?c&->0g&N$O!|2Di7^$YejOtE#K()tp~``Q<W;r|}|8th@+|cw~*U)x0?h^Jr|%!o|2b%EHB0Ynp}e!n%tWi}WtaJnKU|ofUTx{aW+zYm`~n=O5k$SLc6ToPX|FixfT5yJBYL@qCqF;B?{r^2;xcc)m<C>Qc<qmpomlS(wj~c&PG+Tov&=Qlm6Uq7ik-Ra`__k)}!Bm}KePTA~-)T6&OAcx_zYoL$}c)YGFM$L(GIapO~!69khuiGslOvM5iJH7dPjm_>`Cadv%ue&gGdFq_AVX>$_aN8@I-@+L30X_nh;we8-Y=U3Mkmmht*?X|p?-MhKC`Ec&r@2IQwmb$)Sq`hZMeb!y=#@qAjH&+**Zn*E|BC;0IUGiXst74XBXn!|LlgJ={ndU`v7G~=xF9he!Q4)m<;5S?@qY$(hMO`bjhFKbdKxr0#OBV&Gm!+%47{g7%1&UWWmSv?2w49`?teHg9DJp@XA%>b{ArOta{B{L=Sm`oaSVg#uGU_!;F%#w+rt8Rx3u>37C?BVHi@PuzOY?D@j{xX2vI<N+ouS!cOhd+F3^<wOQNjFU3IE*1;Dx(19i!_si<h4D4saC_UPnnvc#Fny5e|Whd6dthoQEUWtr0k(2p0wB4R2SG_38B$R+~h*XWh)=+`|7CX<-#J%$tm@)iPtQ907<Z5*RQekdrAaG6AaM;Sdw%agw6sjtD)AqQn|Ti_y%qwbG1;f(;O2^&n6jts|N-G6(|aV!c@e<i}vIu!uBjiW!Jg@B#=Z!H+atanF1ij-nn{&f+nlWFC%YF=mMu;P^NNq(sMI5{{!>S@|dfqLeiS0|;V(lOkTMKxgSf`<L0}FpL>v3)w;zk#`(n(?l5n1m6*=<{(27jXmo(%_uRgMAHF;T_)j!g(byk@-fAP@tk)sXdGvgB)wBw9^?`BldhV_NrJJIrP-IpjV6<L6a%dfO4c7OAZsG#Gb|D8&|Kvap&EoNz|12wTPE>{pb6u-XZ;=(8KK}mKpmzZ6)TJ)Tc*bRLt_5CIl|VaEj8uMfMH3p^{jkOROdZz@D0|^l5m+@IVeK1glJ&|pdi4r8}I$^KYAZ7KK}FC?+<!!E<fI!y}9A%_h+B@@9WE}bAEVt4tavV7ay-L-kt|H=hxh@@#*Zt`OVF_-*@b{VfOWgH{d(kf3|YG&WZBcN6KrRoT#>|ycaK3%T<p38FGn4ilz@WJw~%m8%<y6rZ1!^3t}1eH|EQ;#rTFfj(VLOEAI&Z+NaX#xpZQob&;iuH?%paVOtt`Z5jOpkEbW@pfQdnRyZCzp&Gi~EGkwR_<OZXBIo|#0Tj%vd-VVww7$hlZsc;8d^OzHrTIh`920oUx4S&cr3-ZkrR6v+HU`gEbF_P6=uwvDdA*Ah_S=JJ!+vMb4Do}f_CV>U7L~Q6R_UiUm9?c-hFqlC+zCq%=sffC+pKT|xKPi$TEs=Y8LzQ@sC!GBXpS}ulE`Z{Q5Z>)baT56Ywh<13(U_Bc3xOG_pW;BmMB^B<B}fNgWkk+xaHzoDxM55P@1gfkxz&s_}2YfEM%YrFZ34UjsG6B2LsnVJhiI+{20?Cm}MF{ZIwg|%+PFO0aiTGqrYl(%jq-7$_&B;t?GdEG#pL&+kniUM!8=*@x3=#Ddd^M)Y^gpMTWMw>bBqR4i0Yn-8SIug?SE5!NNXw7QWwR8Oek9ogs)ZpfVbQhgAz2hO0ej81vk5Q5F(FdK`i8*LKu=$wReX`Jl@yTDRWNt{iumk4YcrlNh81zt-qs)u^O2g?V70?R}r#2mUx7fgYGM9sv_zfRO$&8$e2iiEsG9XQp6=A?cY1bWA!)nl5u<m4#2h@hkCYZ_UK!ch$%HE@_0A3m0pb8mAnANc(JY5N}f+jloP*__ZqB=mki2J9WSK4j9Y*pG9xtks1SDcD~XCihjQ+=j#DaSUttWT6)s}DUAj%94C7|7ewOdp2eG+MNRw~X8L_V1yrCVZSHTNz%1VPj$i#Q?alju*71$j(MLsxD>?)0j@~01wgDw8$BEHk1Slqav;ev3<aPQ@@8|`D@yh`LOHICrsM=`Kf!yt!aubVY@F(_XI_%!F1Q0R*A)0;%I)8lsf*-qALka|}*E&`Y{7ZuV{(#^47w3ShTFQQt&Oz-WGRmMnECIaj@-b#eL_@kgT2wz)Uj{z!5FGnSP6yjxSV4UOAD}@B_}6mczK+8Ao)t8`V_Cq_bDWKx=Pn(6r@RC%IXdA*@R+QY#>HwZ=8HbbhZq=&0*N*#cPW%1y<S=gmdGpESfh~RNs6%&Q1Whx6P6mP@8Hw{urFPRqQ)>CKllRRmFVQ}!i7G_-->E+O{$gMTlk&h-Y(lVz4nWP>>10IQJRZ@DZ<sW_;BIUM8{<{#@wuScQzlh@q<F?f`;xq2cW<qJ%T4XF9^Z4C#f#EoEF1e-ZnUY)bP;iBlOm$u|GCc$)3@@va}#!4xTGjSJEl#nyKwFe=&B;^PCB%h{cYHHI7eq=)&z8WLoM`i;#8HVXFLt?Tv~V*xDg|P;~h_Nb=nJl0rEhTf>K%vVNG583&m=2Zv=Wp1nqf;|jZgNJZM)k-|eq@xRj-jNBvM28yBJe=lE3IjM2fo-zHrEN_!)*QRmMmi}QJoR?;&-M7?zTRmV!ZN)N)A?U8X=)Rz(g9TeuO=3(Mny0orNl&1nF)?G-Wcaa>N%2ORk=w_;#AnHjr@90`W(j@_xt)~1B)J8tdJ|l;jd_VaH-d9fQ*B`|Y050tF)XI7(rts3O~}&HVhYvFtsdK_IrM*Qf8qf$YJ?{hxg%;8li1bFb8KZmC~Wc(vyg_2i3~lRNpeEGBuc+&%m+AaU0-()t0S2E=-8ruZTxZ7IL<`J@tqb5aaNKVH7#an2^j;d{o%8=2>q%>d~=GK{-nlucYB|GQP%!Yf4aR(-|<=k({W3yxU&^R)(VKcE45A1+b<RUlHU1;TDj%RpK9$Ydiad?u3H;pnBLb<*hf!SnXrDu-nmK&>*wrNp&YJdVg1Ct6H#?Xg6hcwx1*0+5HKy7EJ>FlU&SdQ7SKCtVfV^)aS!DXda(!Tfb^bsct2tfgGSZa7%xT%%Ytn;hs9&`g!4o|q^n|>l3%10cVyo0XDWd}BhS#V)qcS;N{&=#-BRneTCd&B(}*NC+T)kuZ=bNdMt3UZ_nkvmV?~g09gm~W5Oey_-6S?(0k5tJ7(N}m=P(2T1?<8)T8ddb`YJ9Sl9*OHVZ(XTGbD)GS-&h@4otm%$i?-VaNpwf&sIZCPPR`8V75<xTMg~U&PixCCwq^|cE_BRRg<mb5>2+xOBBh0NnD6c*dbJ(lspIsnFWt(I1#@B<0QN%w*=boSr%G%Y4()_7*rAh{Si5X_Ociy+S9RcLr4MyRDk;9_J;Iwe9Ff{Z|pmznW{?T6odP`xY@%JHr}(b3kAbzj!|{^;Th<9q{ir=pWWUvO&)NB(I5v48i@wM6Gl>8+AK?(x^!5U4!24V%2F9&u!mlxBz+UhRn9PiU=!PXFur7bhuK^+!zDWtnI)JV&a$~aJkVx`9OF2grleD7AEdY+(UN9lM_%b^-QA-^3mUYf$5E?O5`^5AM%)<I{G6ua_bA`bpT|d!=y94kPfs6F<euWpQk6S?PNL(K)raGg6WY4RqGK4DV%U}-XGB4BCJ%I}1ue7m3!O^fQSF;G-u`&m+wzA2dC9{L#t2(HysVc{)~1DNrRyeJMWu(E+}%yWPF;N@pPlvx(xzFYbJpfz69Dpf9bx(7IQAN)joe?drZOeey!X~&vWj59msa<*Z=0s}V9>k%?c&{yF9vSY!Pw5S9}g-UT{m?P=HdM#RqkP@(vA8!j|c7n&JdB;TVQlIruX}F-Yyjb@fe5=?O-I=gxcR>S>yv(dq5OksEm7wBFA14R!X|VzHRgmOizPtl<0xQ-xh^XXro{l=J6<)M(I2%vWL<ap^7X9<0ZiOM{FB9TC{TnyQ*yE`aZqBhYf}EU~P!Agd#0qnufcCk~V|Vbu-L0c{&vhXiV3A)rp$V%jwDI!i~2H#*GhlNUX>3k1@zL9ZMerYjIh$j-$IEAK@7DZN^KvRfKOx<egHM_<FS0S^WGZpKB*H@0Ok@o_YlG%wu}#+{~j;!e9~k)<?|pDb7>YNMQjfnlRuA*|k$*T*<Z!Sc?sGbSPNI`6^5Tn$@RG=QiG5zWL)?lueRgz00ec-!A>OcY4zMd~tOi-28U&=AR$WudjWa{q4q^v)|9J&aVCMb}?JchYJ{6cGtm%K2b*==|;C<bCO}tq7(|qvFdooQc6c3Hzif~xs(;@lH0Y^krWKW(N`|1b-aU0%%P~wiLkH-nd<0vPYsR470n}MD)Kmi%^4NIYrFGeADmk)wqX9zljR53Z_YlPUy~CD!t3>i^N(-OudGkMon4<d@IM`Q94;T!kjNuZNh0E^fNg5xl7B*^rrB1dH(bxa7m;c7`p@5P@Y=v&Ub@V^bV!oe%Oi4y2F&DQF4))SAI{(0K=N)iB}<uf{yYk%NjeM@|6Q2mk;o-J?vgl%36Eamun0ZlQq0}%Zkd-w^K>0KbGMO$gCn1skj(@G)8mpJ|9WJj1laR*Xyji0kQWgS>fg_At}fo#``duIqd<%uzb(UKItsFR5)bn2H~)SEyqo@`hY^MM@{o2;?t@@k6;U+y+s_*tg@lK294_h52)HX|7nJmN8sex+<GgIZC|f6lGil0#0Eb?b!N^XY>Zw<ZngtHfd}BhrNU9_$kmhl*4U=vH8#W5Z&>b*_Z@;_v*ZEs}Zwvo;6M^wOoJJL{IpB@OfUds%>ErvYLAF|t(j?9FoLBE(pKZ0qVDq4WLXb<;T(9{2U!TB_=Wih@gnV|_&=31eXl8doG-Vrl*j?_bY(b<(VpUwByQ=DQ-2i<w>HsRExEid&X<1fBB;XQEmc@4W_=lLf>0%O39Xi$Y2~aI&4};d$wU0yV3;j7y?qcC__Iw02>%EQnbX)Ib;=O3xV%;r-KE=Y@cz%?ZYnb2HMu;(8!FB{KM!q47Q3^)BZ@5j3dYV$B2DrQQL9;>0jI1ON0cuRhJ6T6+K;pT-N8l}@JMH40d*gUAktJdrpMOzWZE8AEdrN=r(Q80roS$-U3gyTC1od?kgAvBo>+84gAgPyLyjZS^yl=k_^T>Kb1KI;f>`Ayvihy+?Jx$g0iojn)dA`$<7glTeJ1sGZM>`F9?X`wy$#NF%v}${`CO5Rd=W(7>w!mjj=-KJes&_ayjjw?RlIi=J6NQY8fFq@Tm@IMVN9ajPA&DzW>Y<&49YT>QI`Uc#s6s_WG&%5uWMsgwElBZk&bZ-(n=;=<v9@X?ei>OT$G{H!>d^3RkAC|$v04$tW9ZAA6{L$<hX_iq9cu07zinNqRj``Ug?eTZsn;4efM1awZddBzZq|Y&3S&=_U8GSGO-)>eJ<b+%#s9QQi)=F)Ytul}5Xe3Y2<aIV2>?OaR^E6uU*?Y9a4Lr)5`2vwa;-8#%=5<T4IkKzq+?mU#k8TL<E6BzqS~(Fl%4vPiab((g5?9%I~x{{>JJnOcwzQ{+pd;l@^QJnbU)D<g85I$nqmN*;pGz=8rBe7pMc|0ph3+AEH=?;JgFq53Um&WQ9w`y6rP8OaE5aoj}=7<okKPVX`CXhkAh(%f?vGotbEZH=wfY^#Hsd!4meFV15Rj6E|F=vfQmLLI|h`Gbnj0^*f4<Qn6~NzmF5-J<TJ7r>I1p3g&J1c7va7DY65bff+5gRo_b7o10Ikl<ku1ERG?*8YXbv7l8^Zuc%Es^puWwk!>6KdWm2|!6*!|=H2TVHM}n0is6EN^399y*6H_)E3EJ+{v`v|ZP#BIm5KgXz$cu3(g^PGXX<{@S`FSyn$Eg4=WhY=nkNH3X^-dm77tl3%d(_A*!%ItweOHj8avV*0&cXvHhOgRWaqx5nyP%}&W-qt2ZV6z&#Wp2Cs4@^}P`{<HFbQ&nW6C8^D6XOPfGx$xX4uBKA^3ND!8Vv4+AjOp-N%O`i;7UA5f#jj>@ERhFVcm<alm-By9BHaNU?Q^&x6_oDE$G@nDBi8VBl-h$a@EJe$wpbpcZVN#rMHonkD1^4HYP@6dnzv5i*c5;_@lVBKIdG7$_X6HI5UBXl-+1KOQ?9(7FS^uP2lIoRQ2lqM4j6ptr!p*2F4Yw{lBV@D6?kFRM=GHGpLt%;F+<$_8qw#w4eyl$0ftLZcY6vKeI>L~WlEwkT7k7j^h~M9(uFbQ-IuLwsHMlsy!+)eM-S%pdZ@px6~A@9G#^M3sxR-#$cLFVA_vB@MXZ0rDIJJVT4#t)2iSQJa!hsCuk!rB+YZ(eE<l>Q}!>v*|su@wPfxzw+A$RRNx!zbamJT3y0|Vfdo*`%tmumc$G42{3IHyQT<t|FF&^<B)J);Y>o2pB{=C)F7t%=`kJ0V^YG;KE9=pWE3?)6B1T&@!-)=Z&#ezSVUGn3&|Bq+k+wCEKTxFvqlhR50bHl(LC!9C`wsD=RIX6=N69sJn|Y9F#cmK>O!#lk8!3fv6s%HX$Xa_^%Q$>sV^ygOK1(uD*9oBhh7r;dlKM!$#AQ9NEvy(WVBU0QX@+Dfs9-DN%$-oK1)UiCdtn{0|Y#W2ht(L^AKGa{sX@wUUck|MMnc5j77a%NXZ4pzw?P*xyPY%EIpPn0Ad=&QMF4-t&cs0PFs0L&+&88dC4)i(<4Pb?l!+2w_j2O5k>BRkj2~W>21kj-g1r_0ER(H?2=nm(*6qdq9(j(G}rx~j-=kvitd_i-hd~}^5tUuej8x62PPU!0*(9J?QKlHx>ng(&U0Zl>x_>kfO?)~Y34X~#gm5V0Ui0~gxg6W4X5D1ISw0J-6=DT-dJu!Hd_EwV9Yxr$fIOZMERCkw^S)i4vMT{s(NN^<&3Uv+gubDFeI;yj{H5fdPG9sqd-(Aqo|j5S58LVgVR|8$N)Chx`bHR>1kCK=t-odw7@af_`)u4vqX00myUAw=aV}ky{j0Jt1D+Y@z>H9_oAbBFgbwvR)9~QZ&_(LfMvB92MbhTJ<ihY9}Se$4foZR2KNTS!V;Go#ly0=ocmX=)oQhsV_z&_0>)#`qyg#6C91M1ZFE{=g=0P%18x?~p>xCxm9nv(c)pqkCMP~9$Dn5A3+WGn*lNho?uN=9LiHe`>Fzq`TV?{?2#OyZq@r5{uM@VItUQ_$+ghR{nXD$5H%XG0p8vXSrZ}|(LYSm@m@5pZTM^F2WlF!LnL}S~i0;`9jHc5lTV@QuRYozR`4anRn2xb)Fd%i1=z`8c0(UR4)~Jx|dx;&$IYNA|g9wz#RM6s*+HD=ScRfDyDqFOsz%r|UQ>!H%fUw7Ewm=VjUGnDRstK{_dhPfBit@8p_34c=-&wCI#*E+A!1Z*d@|rTXrAV{^3IdS~TzcP{-$Y7E@NNx}=t0h%3ZrJ;w`Z&6udOatP_c=bkoc+3e7ANhopQY%D4S>+%sb$>%o7*(VdqDsKVUdYEfac2_rwM1a;aG+T_wU%p+4eaw=ZXsc&tcBLRmrwjuV&*2|}1r5-$UqT9VcqmSnMSWWDc6O=t0rW_&_ZP7UX)%YjV^HT>$nYITQV(U!Tulqk>PcqtFHg}PL?Ci!ki!Ts*wV8{vAL}4iSK6TNF1Op)maUW{BLjeC(Cj&#dGsB=t;U5o0f6ZXlIQKQ+w??(Vap98Ixl<8wMIQU(T&sVbUWB*EywQMwC6E7?AH`jQ&(NGAqB$o%$v`k<#`&Q$&YL(AT-HLU=T@(%A~-P{8FwQRz{vxcSn*#;l%s>2UfqGaolaL)xg1c&BxT939V^0dYqc6|+-q@Co)Z-Bx6I`e%?n8i+tcAKYTau6I;%%|UF|JpZRnQjRwz{E+j`?IypPEh<I3Q~u-gKGtUVz+i-6vyV9<nqS|k9_zQ8R?>HmXmq{&q7ei92<#xe;P5wE_I1h-p)fXxl!CfXmj<^H&({lTv;T?3)zZc2+=KDeq~Z-t@1g(yO#J%A$E8xHr>4N(VGt-<F6dkCs+-e2~+ok0aPj^6E}p<Y$U^`TWp{)fZLeL#c#>SHo<crL?YGz*Lr8z?7J^kOzR^Cu7|M<Oe*l+2|$iuOs#9mFT)S&H*!7zL7I!w83MxAY}>;qUY!>tc`QA($K}f@O~eBFG%j8MR;4GyR`xFf1o%SR4CpBeN6e67x!n^^&BfxxuZ^XoZp&j=%Wd#W~O=C0?jjd9K8h^@ZL=Z8_MOy^H?+F9N?u2>rsKLPL}CVXYi(+(sV3Y@&%Mci-(5={OZBP8DwBZWbqzMWs5$myH@4jLN)ax^&z@liGIahlgIsFlCaw+bB~%Fc(iIyPxio{jt!Q_c-&!4{WPii>82~+id9f1PB2Qz?e<_$Mq3TnC+Dthurptr7Ow9gH(5cXe*FjN?DdN3X`a3K-u<xiH=_$`1G*h4CCQ{P=bFJRZh!FL`wz^J6!yd%LpSxF){>Uz!#3z-ZzD{s!D4S2bVUFNfO2@pYVEhn1m9XDcC`3cm4h;*<&MG+t^kan7an=e%3ZQ)q(EKRx9h*;stXXQ>e{*R!p}b$q@^w{uPRZ&xe6kns0@85~Avw6>A8Z@|pOv3renq>=E-swrla<LYKK4OlYcbM<oVkAWyq^sB%6`YDkneghgeV1DzEv_G5FhN|Hbi_7Ie~DMxS{b4uz7qBX=3+im+3v5XA)dyda-VdFM-74dR}s@>xQ_L9`^o206mg1w{Q9JzzuEJj<Mm-Vx@68-Y~;^dgc=+aD5Qm9_;Yu~8liE(;3`#hfO>?^%VU-`$_?{Zgcm^pLOSpG)XR!_04v&{zAgo_7f;S~?d$jb}D8#w|U`{w*#f$dh(b!S3YvmaA3(nisEl~HmkmPff57R5?dY_*}8wT!ZPTwp8OJJaUGJ_Us^DAW~607D9yiaI_kGwCL^6-w>K1d@?g+H+=KZp5rr6>C<t0JYMQWo2JnUg7t88I4v+m|1wWKESF-P`EF$Oo_T-vGrCT_j*R31SspvV6y>dPxP71O%6PlL26b?H>1*~QNDRwXz%^nQ@6Uh$(>km&B8n^ip=2>We1ef6cF86d9M#4eJ~6uI9s#Y<8%cn6R>l@R($D+BWaY^CYr#CFVee4h1WNsWgLA2G#aJZICpgP)7|zP@y6Dbth7HBuUhB+-;*(aS=--5?x;jAyP4Od=0C3D*ZoAC9I7uj_hY&G8xQtK3RltAPq)%N`o&f}b>P;nnC7g$I5Zzrm2{PX3>wG2!8OZCXb)05S^E0RC0;%YJ13`3Exx`vg3@0}NO1}{U}0r<ZP)c6`?2R8Jk6r}aXckw9L|Q#tWQ1Z&yxh-o|`nmtw8BPpCaLdZfbgwZYII4N5Zuxq)tPxBMGD%0K{t*NEm*a6cfj!aQHd4#^oP3hc@5gL*>wRm2Ph`(%ye~Z7U8NM>>Gd8ir~102`wI4$>zN5?d~d%(p1=&2p?E3r*Bc=QosSyPHdXNl5YEctIfVfm^8N4apG*0yS<!|GQ*|*j>&HQT9-rgf=Ho0y<A;tOOWD(xNJLvGVxaRk)rbs+1W({!JpaMz-Cp2#;y_Xe6(cJXIyE0CkhJDhcnYWEQK2RfYI5-gdN?vb)SzK`NK3@r8;d0__*NizxAdZcZjo8i>Qw?&^)gIz7!uF{*@o=-B=Yyxnb=e)7t*u2rMb!ESdScfKoI+^40*wP7CF-HlgeZ)#1z<A!pD6&drbRBbUvrNfmCN+p=oWeQqXS~D$F!z6eRtC~~jv@M~u7aK|{-DjwoiL4Gv!~k+B5Me=x)MA7N*C1fal=WM}WoKu3ls^{?9|{uT8zMx(oYDD)YXDLu0!`v6R<2Wjh;~I-tgr?f)EloxbQN4<Q75m<cb%lRfZkiMhQa|KTQc`(irdg}y8_>B*vulrheyH?K;C79G!ig%@pv0562TC09rwWgKWL~gBorZM3-M*tSf_okfTuhaRVpZsO(;+sg2s`(Ng1dc+ZYu(?|{_@lY`(bAGl7i!wI4~>D^n>MXiB^T4+`BVF=^fTtWoGxTX{+IXmbuBv|_d;{XzagbKJ+Bu9RzKQVRqokhrx!}WLlA*mmS-)ZO{1akZh_UDpxN)Ql#0xCiIer8xcPJG~N3>YZrq(zpNP<B^O3ps%GPgB|}MENCYT@33#W7^?d#t4bXC^nzSA}EW8gi7vE(xlHSjj|A1cHCUYNdjG#I>iMw;ZI{x%11uR;w4*W-P&ici1|c(*<H4s$TQrx?=ipw{(Z9tN~&EBmHPG^wEA13l_>%u#N4K2bh+SxDWK0r3(BO09!uYYg0h)I7l6WzEd$=R^nTME`7}F^cewc<);ZA5AEcRw$sr8sgszlxd<mw7zBQ>oW+Vp~DfHy1k=p?hHli;taU>|FZ~`B>|39t^n07MtUq0L2o=z96*^<&%pJ}vZQZ|-+x*%}<n_U`lm1^Vr)xpQM+@`wa`&+t{{Vt=6I8Y=kBWo+Mb!d^amCp_EXTo4C%t=(+ILs-flcuT(TNZ{kZQ4?9o3Ws1jJIXC45j0}71+Xg0`HHW5s3|~-flJ*X;aG>#?J%Ps%*L@`wx|7vL<J4)*Ensr4ffc4i7r^`}0e>XYudg>iq2OzilNuyxI(U)AVQ%NU6eU5i7nve}D1OI{V}1x67-G|D3<IZZ6KR@aIY{xBS`eS#n^=2h9?aEf3a^%rHJdtgvWzUPxRDoR|fG588Y<RocEP?}uT<RIa_P)mqFQD`}2)zNzw973a~a5cENtKeS`olxC1A;ExnFXcfVytIKy6AI|*}E+AFV-Gmq;_Qh`GmS-P6Tz=*|3wca2*5<lxcb)dB>f_&0N1YxITuFdWqI;=CX<yg;kU_35KEB_Yjh>sL1vOc?==nZeT;E8_E$kk!^G+XX+$29O#8H1h`X=|ggqXg%fUtbBv)nsqQqVAqDVJZ_-+z>2T;H61e0z5F*6-Kua@8(yRkyavyIR#9t*x6`1LEU4uB+6GdMVMnj%VJ=#Nm_`BHX>j6`L)FNqh_Ic7M|<*#n5CZ}N>IXA@b9ju9Qx_^Q?=G-ZP_Z&{DT-@edS-WZav|I4o-OT0>uToe$F`5SwZZnnM7ejN#eetYmJti%wC=q)Zz;_$K@V$P)eRApu4qAKH(8Yj9Nmm(J>aE1XW%qpYQms`52s=0XY)&}m@Ni0R%2&-3Vdi6K2?rq-Jd*qVd{+oF~BMEHc^-_gpIjwhfz*#jl)I){g?`g*0*f<QzI|ex7uOrGzjFMo|nT$rKr|tGh^x{SPW&6dr)ftZ3QTY5t>*dK2xwuNzxqgd@zaF|0HKu=h+=57G4P<pN{7CcZ+NrqJpp*p$61*89RNfz=dUpKT-S0nsR5Dec<0KSvhkvy|CDd+gKl4#6YO_N&bC;=Jris?Cl?{GWJ&FEhzeU-4G1$W=KQ`|GGnlXZl5Gv!)jr+DP?oD4Mia8Cs8sF=Jh{e(Rl5LaA_xA)Hf7J-)=nqiF1z-g*r%L7VwR#O`N=H0*<TO<d+#vnzYWXWXX=+%$_7>C9;WZ_vd)10n+G<VDphZ2ogd#mb<l6#9IUuHxc9-)y~k=Fo~&I)8C_rjTz<RN(o?W8ynTPFUbW>PC!h1^t9CLB%Bx2E?@c-7H<j?O?Kb}YxR2gk^2|k3xd?9VN%9+Cgd~mLx6h{kvKy0hw8~8~9$&T=6{ZOIdfNB-z7Wg2<})o#7m)*DJa<yHOtJG*kMbl~oyU7G^|G`OxfZRGDDxejyID1J={gEs^!Xaxu3$sj&Hq5={M+Vo?&H+HsD&}{?=H#|nVH(8{$~W+i|$l6kJYKGPFpQ?ET0NZpgcIos@b7}qtlk$xpwTUc#aB`D!d-QpsU_wHgB07oO%{eRGBRS`wYsft?KJDw|<N(Qabh|{N>x9^tF8ZfZom33$o*<4?Zu$l)*fv8Qxx8|I;qZutJ}HdKG@Rji^yb7jPIxw}+Q~(4cq=o;Tdf<{F+#*2mZEYo#!$W@*58pna}0cbK@lk3S_ie3_;E@I@fmES#}Ki|BwNCEDa0QWV`jf*~dhz7K4v*@9d<u^@H>ac?%Jk6n-~`{d*tgHbu%x+|$aK|~*rqc6vr3AcvQKK!Zverp^~7ims6=<-Fl%xBPX>Nj!c-M$km6YwI_I-bPDtx_^faQxSTH@bLZCvOC7_BGgv-|Qbn?rBwFw%TQ_zZg_Bak*W9$U#z@%ytKrh^Pd~k4CCL&>qwR7&N567mro*JV{9orCo>9LAIritNPn_%&LoCy0N+JHP}sJkuVg0)Fr3^QV#E!Ps+`ejy=+_k1VBjt?+NeYt6St33Ro?Cjsq8#i*sJWg?DDl^I9q$EId2c>1<nN)=os%uq@@e}J7sr<Sg)B90PMs*S$GzP?{Qvj)A*&gAQ;0N)1*_b(m}sev_`QNXJX&DLS2!=6ky<uEspr%EnE)rrAXbrRIPG+T_IEfq7&29%taERLKSY};(-abk&Mh{xQ{0Cdwwq{iH|ohYG&$tB$ctz6sg)k*%Xt!wXg0Qw0GCe7d28NRRQEfvbW+tT+R<NZw>ivNnJ+2n~2E2d$x9|}Xu&Xe44639`OS1AKObD`DdtB<3JR(&06$H8{E<zAyK$&k_)Y*AfnE9YG3pf)_4Z{%2;5E5YJYd@Oyu`%QGii2v!yc2|*H=S=BrZQ+`vWdTrLPMGyn;m$T{Z2me>}k~0`}}B-edllbF!s3c_P8(Vt_#c}Mh-RX)|tK%@!h|9mOS}Y0mnPRfvo>gwkg|S{`aq?Y4>$deZtv!(q<nRz~zYiZ@80OF+G8~rDzs=e4iTP`iF?Ps6PLo9ET&n>`u$~48sYIb-3ACX|VE`?F}Oi96{+x-+%NZbjFXw<T{|HH&xA>EX*_TpK>)zg0&3c7-gJg?tTLq6_0C@B+;PMq5+Sx^YNBV-@Q{a8lf}lRq0FKCSv}VB#5!uE6!m1&MG$kGb~1{EloyVvxHC}B9cVks@9m+faoi4)i})pc14w;L@VXY5hiZ!%px8$(R4~s=XVKZ^XuG~Y%WW7q*XKZH$O#1b=KYdry4PJfkJ#Y-_eL$^c~<<`vv`+@E)`*Yv=kp{cpTl`YCkw<pbRtUoCk;-(>4Z@zb9?Kqu+Bsp9kM?E|r)dUf2CNsH96hNN1#zB_N8cF*p8Rl57#T$WoMm}T4AmjkxW=azK2^QrAT9kcM?Lbu*aa;03^^a-<fSCD8#0*}8-N*QGS=BLe2MTDXMrU;G(aYIN^w1)C8ndtg^On07sZFB0;))wV3FCSb?x_?+_*q9&*gn3A@Jre(%sAtIqID#2R1aZDqJ8$Kh&qHo4=;{qLEWRXz;W*q!QNalao!(LUsjRqZaAk(%py2%|;<zgBRE{-Lkdy8O3+91Hi?3%^gzxTrSwnyF3vJan4OR<cD0A;!A5;`;Gvf%K2<Ot}3$j*$$}IQ&R(JbTAm(#ocr%x3?&kHpO1aZE-#5bcH_4c%%t`du!v+ND5On|gbK|yjK~vb2x@`Nd7KJb6<w1=ieO8-IK{sQ{LLUEm7J>mjqTq5>;N<?@e5ZrH%lT+qlj6v&e&!3~YrAB4FA5e2G8+1&JR|+bAn3|#<@%EQgZ98E)mt*@F?GH7n0C%+DH&#;ioAcnYe&J1vVdf>{g=IjeEXR&^I!B2l4$rV4#I2t4@c2~-+SEUT7A`SpUV}snn3kauP*|rbkg$&D7Lb9|4x{N?t5>^xk}1CZQVC+L-S#m@1;&8N4eeA56a%iKH{u2eo%HqmmQ&smtA%be*Q1J@%JOQ5;#m|l1`vl#`jSo|G6;AprAyuCMRxH$x0lJH!4fFimW$GwBCf+Iiw!Ex%~aphx42BM?>t5{|oRUEEW', 'offset': (0.95, 0.35, 0.192), 'seat': 'WholeShallowRaisedWinnowerPad'}]
floor='WholeSharedPreparationFloor';box(floor,(-1.70,-1.05,0),(1.75,1.05,.080),0,'Whole broad common floor with empty front approach and a central gap between entire machines');FEET=[floor]
pad='WholeShallowRaisedWinnowerPad';box(pad,(.23,-.12,.060),(1.64,.79,.200),2,'Whole shallow raised right pad under complete winnower; no engineered platform rating');LINKS.append((pad,floor,[(.95,.35,.070)]))
for x in[-1.55,-.05,1.60]:
 name='WholeLowRearBoundaryPost'+str(x);box(name,(x-.045,.945,.060),(x+.045,1.020,.490),1,'Whole low rear boundary post outside both original machine silhouettes');LINKS.append((name,floor,[(x,.98,.070)]))
rail='WholeLowRearBoundaryRail';box(rail,(-1.59,.960,.360),(1.64,1.005,.425),1,'Whole low rear rail tying three complete posts, no barrier-safety claim')
for x in[-1.55,-.05,1.60]:LINKS.append((rail,'WholeLowRearBoundaryPost'+str(x),[(x,.98,.39)]))
REUSED_ASSETS=[]
for row in COMPONENT_SOURCES:
 raw=zlib.decompress(base64.b85decode(row['encoded']));assert hashlib.sha256(raw).hexdigest()==row['sha256'];E={'__file__':str(OUT/(row['label']+'-embedded-original.py'))};exec(raw.decode().split('# BLENDER'+' PHASE')[0],E)
 prefix=row['label']+'__';off=row['offset'];trans=lambda p:add(p,off);mi=len(PALETTE)
 for name,color,rough,metal in E['PALETTE']:PALETTE.append((prefix+name,color,rough,metal))
 for name,g in E['G'].items():
  name2=prefix+name;emit(name2,[trans(p)for p in g['vertices']],g['faces'],g['material']+mi,'Reused complete '+E['ASSET']+'; '+g['role'])
  if 'face_materials'in g:G[name2]['face_materials']=[i+mi for i in g['face_materials']]
 joints=E['LINKS']if 'LINKS'in E else[(a,b,[p])for a,b,p in E['ROOT_WITNESSES']]
 for a,b,points in joints:LINKS.append((prefix+a,prefix+b,[trans(p)for p in points]))
 assert not E.get('CONTACTS',[]),'No untransformed contact records'
 for name,p,q in E.get('INSIDE_TESTS',[]):INSIDE_TESTS.append((prefix+name,trans(p),trans(q)))
 for q in E.get('GAPS',[]):
  r=dict(q);r['origin_m']=trans(q['origin_m']);r['name']=prefix+q['name'];r['targets']=[prefix+n for n in q.get('targets',E['G'])];GAPS.append(r)
 for q in E.get('BORES',[]):
  r=dict(q);r['origin_m']=trans(q['origin_m']);r['mesh']=prefix+q['mesh'];BORES.append(r)
 for j,p in enumerate(E.get('AIR_POINTS',[])):GAPS.append(dict(name=prefix+'OriginalSelectedAirPoint'+str(j),origin_m=trans(p),direction=(0,1,0),length_m=.0001,targets=[prefix+n for n in E['G']]))
 for name in E.get('FEET',E.get('GROUND',[])):
  g=E['G'][name];polys=[f for f in g['faces']if all(abs(g['vertices'][i][2])<1e-8 for i in f)];assert polys;f=max(polys,key=lambda f:len(f));p=tuple(sum(g['vertices'][i][k]for i in f)/len(f)for k in range(3));p=add(p,(0,0,.004));LINKS.append((row['seat'],prefix+name,[trans(p)]))
 REUSED_ASSETS.append(dict(id=E['ASSET'],source_sha256=row['sha256'],unchanged_scale=True,unchanged_material_parameters=True,offset_m=off,new_model_count=0))
INSIDE_TESTS.append((floor,(0,0,.04),(0,0,-.1)))
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
INSIDE_TESTS=[(name,add(p,SHIFT),add(q,SHIFT))for name,p,q in INSIDE_TESTS]
for bore in BORES:bore['origin_m']=add(bore['origin_m'],SHIFT)
for gap in GAPS:gap['origin_m']=add(gap['origin_m'],SHIFT)
def measure_basic_geometry(vertices,triangles=None):
 assert set(vertices)==set(G)
 allv=[p for points in vertices.values()for p in points];assert abs(min(p[2]for p in allv))<2e-7
 assert all(abs(max(p[i]for p in allv)+min(p[i]for p in allv))<=4e-7 for i in [0,1])
 return dict(review_scope='basic complete-mesh count, finite bounds and true whole-centre only; no complete-air or finite-seat mathematical proof claimed',mesh_count=len(vertices),static_two_reused_models_one_preparation_scene=True)
FOCUS=(0,0,.65);ORTHO=4.4;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(5,-8,5.3),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
root=bpy.data.objects.new('OneWholeFarmPreparationScene',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole horizontal bounds centre; one finite hardstand supports complete reused round baler and separate belt wrapper';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)
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
assert abs(lo[2])<1e-7 and triangles<=5000
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
 'components':component_checks,'connection_interior_points':joints,'all_meshes_connected_to_ground':sorted(seen),
 'single_prop_count':0,'new_model_count':0,'new_scene_count':1,'reused_assets':REUSED_ASSETS,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'basic_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
 d={'id':ASSET,'version':VERSION,'category':'scenes','assetKind':'scene','theme':'agriculture','style':'warm-handcrafted-village','title':TITLE,'description':DESCRIPTION,
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
  aim(cam,pos);bpy.context.view_layer.update()
  rotation=cam.rotation_euler.to_quaternion();right=rotation@Vector((1,0,0));up=rotation@Vector((0,1,0));points=[o.matrix_world@v.co for o in parts for v in o.data.vertices];xx=[v.dot(right)for v in points];yy=[v.dot(up)for v in points]
  cam.location+=right*((min(xx)+max(xx))/2-cam.location.dot(right))+up*((min(yy)+max(yy))/2-cam.location.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.15
  scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
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
