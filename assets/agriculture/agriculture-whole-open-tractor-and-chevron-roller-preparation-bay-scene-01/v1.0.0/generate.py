"""Whole purposeful farm preparation scene; two existing models reused exactly, zero new stand-alone models."""
import math,json,hashlib,sys,time,collections,itertools,base64,zlib
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='agriculture-whole-open-tractor-and-chevron-roller-preparation-bay-scene-01';VERSION='1.0.0';TITLE='Whole Open Tractor and Chevron Roller Preparation Bay'
DESCRIPTION='One new whole open agricultural preparation bay scene using the existing complete open-seat tractor and accepted chevron-rib roller crimper at unchanged scale and material parameters. They are parked separately side-by-side on one newly authored hardstand, with deliberately unconnected rear linkage and implement hitch, a broad central open staging gap and unobstructed front approach. A low rear boundary, side curb and two thin contrasting ground guides organize the area without enclosing the machinery. All source component geometry is embedded in this self-contained generator with original hashes; there are zero new stand-alone models and one new scene. The tractor and crimper are reused assets, not new asset counts. Fixed static appearance only; no coupling compatibility, vehicle movement, crop processing, public access, working clearance, engineering or safety claim. No people, rigging, animation, physics or runtime interaction made or verified.'
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];INSIDE_TESTS=[]
PALETTE=[('MatteHardstand',(.28,.29,.25,1),.97,0),('MutedBoundary',(.20,.26,.23,1),.95,0),('WarmGroundGuide',(.52,.43,.24,1),.96,0)]
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


COMPONENT_SOURCES=[{'label': 'Tractor', 'sha256': 'c8bdcab6a6f68318a8dda7325585c022d460a7529ff12e017631b7155176f859', 'encoded': 'c-p;vdvn{yvgiN&6u3#<0$>ecl6smnQY+iC<2sJ*l9ZEkE|<juNl1hR0u%sJqFw&(+rRD^0E8$xu06Y{SONy~=;`U{>F4N|Uw-+NMb}Xh#Ma$BjYBJ4hDkdQgTl(fAZy1_auZyK)>V)#tRf4hMVfimhv<4<+=cjQErOdcvo6j)yd9sP{qz0VUjr*If+Ct)!E#Am1j&?oP2!FB%P+sQqQx@J(5RTJFL|1%d63WJXrl5>u8L?8s%aX>;k1a-Bv(-pW<{FDdFv`m7uJ$mQC&-S@|j*+7ni5!mp)p0_~E#NPk&ze_~eYoS5X{}$F7%!c^a?jqqhvQFezH67Z+!jz8zd=(R39Tt1N6^Mfc&XT~5CpB(ruM1#O_9tx?eKbnU@E&(1I2fBNX#U9aPH?7`*x%MWM1{T3ZrpQt120(hj3taIv!uqL>C3tV1GM|SJY*~RPg_n$Ahr%y>}P1D6P4vWxA!n=551*>A7X4K<#n1lo_uaH$iPAjK@vch}9SA+$+SOjrw5z>-^)-?>{+*&0wTBpE@(>p7V(`A%gTaz?NLV+-_k|4|I+mzZw$tqpt)IL~*RvZR1t4OWlF16wyqX_^lx?5$<i3+T%6%7|;(>cMpSk10iK{lgrL1KlAWwEicAj;`eZtxK$Q$j11@MQ8LB)AD4?$fjWVoJ=T8PQ#u7Rxv&!kpXj$g}9`D#S8IH1`^j)d9^zT4`!VV^Z@C{ib=-{0%+R66AW`m;im5Qinh$YIxS=JjyNlKS=?wmBuqb87!<Yq1_T%cTq97q9P|05{+d9*dkqrGer%6WLm?Csg|w^t~n?0!mMv$W!6z1O=ynSVY&#5Y{Q_e!+A7~0UOQdI$RJy^la#0mIZf-XMsZW{#vB7Ft)yi8BLd<4+-H{=_(_f2DdBFQ9>1|kI%2pvEc~CL7aQm$J9(BN`ziixdIBbl;n#j&uIfHE2GUQ#pxaYo=3%$mOCowaYG=jVo+qZO^>vwgnRBFP6I+pI-RbT03{EuLLvuhun3aX6_M?V7k(NC(ZaLNqw8xPCP<<M_n@hT;0%~2@PaG|k)GXp=YRV?`0)PYKQ8>?Xz=>e$IH{#m;C(h^fUi{_38YKAKsqPcBkL(KVH0lb2h#_yWong&!->GE-%mgp=1BCB5HY;g<*1*5ZTAJa=h-L^7cE*>+Y+rtGq*c?e$#c*l&XD=6p4ogxP5_!!Aed&VEmModc@h*+1b1Cnu_7s=vi%x*$AD&*-&R_IyN-2ZyNo7g6T#t4RgJ;XXdmz=tIa`#pEmnuS+ZFq=7nnz;QeBt#}wu_Dgl-0y9O5HjmtZ3uPN*J#O=TyB!DCcB!npJ=jJ#q^dpn>@><2^s`abCwoco#(3s)qA4rX_n@By@?YHyQ625VQ<t9=m$M@M@m0+P}Y&JN<Vc`)|Ic)C2hck6O<s}r1A3GtZ)RlK##miqM}}n=h%I&TT7jAL3OYYYOSsm^`vM&gl@lOt^J{3Axnv`I#)#Ig>&z!7jB7?B|k3lxE>9zOoLl4zD4oXh&oE+)gttPD8RQK-qJ)yO7McWh~D`3UUxKd-RDPE)t(<CJTk*@x+)G68ll~#30TpU?)_z_Uk;yz>o6l$OttEO3^W{V`Q5U@*>#xvwX@iJO*5r!=<sSaV4xziwzukb*zJ$@ZioFY!8-`@oX&7CJty(~F7IdVeCSMQF-9mu7u>B%&<%g~=<HwQj!R_$0Mh*ke7|+W_6zQ+^U|kvd5L-Jz3d8Gr}22{qx>qOr6zi<t%p@xC8bxGJ0`Tf8{&QB&!Q=<2aOp`2@^yB0e&+XFemj5J@`x%OfcYO`FIiLb0<#IWe!qFd;rI<pwYpa7n|SJklr6IjVxy3(%j{XQ}%$ReU|J+&6TIhL`*2WsS3AR5hM>A^}qNI5tjSk$>7SvNlLWr++YBOpI?-7v&REgPZ3B<ZyG{MOaI5)g#>_@NMM=98;m#2{5V)lW&!9!P5Vx{h23Y))NEb1?UdV?%S|1k;92g+QC>LJe7J8SD>_uczd__cXT=RL#xwNQpi4AV_`%f44@{u6IcOM9Bj2G>@8)!(TNsQ!xWDZi%zcs0!i4Aqq6L4(M;d18)64Kno0t_IoG(DC>0*RB5ttoAF$_im$VC61j@*|%QFOQ0*TPq*TLj6*0VSK3E8SwPf8UJU-~2W=We`_tO&|_sFVX&*($6V&nOl+u0fe4!_#maayfh<sYh*%hNe%p+5Dp|Q)1~vp9ZX0HyP<j{{)K&(?5tDXox~^3NQTTD`(sK{bObq;r9x|&rI5vKLT{~ep>Cka9cYrGuR=@rMYfuS<BjajrP_4Vrn|+1|Nhder7U{6;!90dX2&f-)Ur{R*r7v*PAm15v4&G?$fJ+s82ie6gIT)XbBrUV4YLE>{*?!5oF+NcD5RCxOVot^1$&7L^8S0<F;Wq=`GS9d@{u!1cHktvmv3>Z=27#+s!a-W7{)0M(s@KbN99bZu*-#ADZJN(9WJD^X|xT)(CMh2VkyQsP>1SR9nn)qb?Nzlo_gwt%J#YJfSw^fb*cWbI&?=h_?dmCGwBu>%gT=`@w+|D;m+q%8zKzO4iL?iPyNzpE_TZ#ckXC1?o00l6DNbwaR)1DCx_~tqE^&)z4lGPitx&e(jN{XQY{sJLL^wJ>=_>;(=?a!qzG2eqUXeK6~3?6ra~SijS6zWZY}W096{K2z$C4q|KQLVJi5lR%B&BWeIY9y+(-HUzs=zkSRqC^jqCgNz0K&xvK2DzLdb?-s}J}yyJo7e#>xrwu9^PiuKB`yhW5@=y9Vf#Gd_srJE_3=L&|Hc(~$Pk-Y&}cLJO}pd%I|YKgsU<@_;6IXR3_L34qZPH1Ml+Mx0vILRRKQiGN;NE}m~0ZnRRVgx|B_1Uh;!okIg8CArAG)^zUMtaN`!?_SSI)QWP_Yhbi^Q`5EW0r<;wuADZsqITEYCuQW|1uYWZyQKRl@0ebDN_sOU1wbjbgxxy4v0D(yE&(7kLMYvA8-U4R5*Bx)nAHsrrIiV$B|2At#W<LRF<~-O_fvHTWRhO@7Df;o&~^#D{THNcLH9a=vV|Gi1T(2v$5eQHL~7OxcSH;R)o(8EGJ4)SAbIxQ=VA6_im$;!PVebx8-RNS_k^7LY1`|ZFt1h4{dBK<@j5RKE95Zup&b-!YXTdfWOlTsvnb4M)jcBO{Z$)s453<6LTeOeun4Va72}OH$s!2N+Q`9ulG2=7#XPJVbf&Vl%pQ0aw08wRkYljA0vnfMR<C6w8%s{;+q9vuex>PwwR6cHO1z^(UiH_;bR}>I*cw{f6<xh{F5auhhQp}>l#N&=-d%?XQL1@|$5au#fh7_drIcUptBUAPbC4UAUvEou!**8@2LvLLttCE(iWkl<H(6-!<wfS)xP$4vpI<+_pAJ6yy#s22O-qb%df&c#<{ci<q2L{Z!ldBf00l1&%7WgB%J^lk`Lb1YuihD?NOMTxB;U)LT!tw0<6e#5d?bET)~eHSqgInAeKb5Ns~8du{?u8;OsZ=rJ5R3)BFcQ8uHsn;+hv}{(ab6ch2>^fmMCV1R!F@n2E?Vrnh8@6!JzF=Vjm(3f*r>!ZDI(@EHz11_X>+pEwwe@TFTF)uFrm7P0Dq|o}HUjIeMY@tYF@}68iTKNMg~Go3AEjzcTns^hrd%#JS8yxGYV<V~aU`xt`0c*}53=hHgMTSIIWezgn-vEUSfPm?5><wn8W^&|Q#e#4_5nAre{u^_*#Q<t&TVq1O_Tq2%!wV*fp3GoXxyJx4t9@R-;jWI1^zrnxUK2PEPVm&XgtQQ-ajypQr;$2_C)NVS16{3FSLq%(~<VFwM{GaL3Xxg;e$f>>6R(Auon_-W?L^Q+q|lOWFRCL*7non``U?}W~*<3q-D#qi!Ic~~%ud6z{oadS+kcZ5^p@Pwvvf(e=e%$_)T?VJ-DkojG62Q|Aij$VsagqAEYbiKyO7t5=m?On5Z2-lC+kk94ABbwxk<|MfvKCoV`7E8_54|q;Tbn+cSaM$nqUE=8{wHacC*fh*Sp)A&fdnw61l{5a4nLHfatVoyX=BUTe{)jgxT2Q%&W-z8MKNAwE&7$1VEOYufi#g7an6%eBR`_*zLQ)kgNQ!tD5kl_;tf@3-lApn5y`zKLgjx6yLpB7HEnkG}e_GXPFtHzUA)XkI3|i|!;1F)~E0kfP>M)MQoNom=$uBjRPeH=k4M_$e4EiMpP^8+V>rlKbECYe3w5*L!qRZeb{p{=(R+go(U1RUGqx*rct34y(WUqWaIiLff+Z!y)+0gk;g=Oafj+C+lCl9G%ZheStBNmPIbAuh9GzT*!)nJAOPTAiC8SW45aw@5Sbc-z-I6Pn)cyUZLpw%bRouGkiaVYJ<ViX%U7VS@Z%~_NJ+Euk$`UH>#g?tS+(G_*CnQuif0v*Ag7aDj2@_X92*+mg-O4vc8d7+#IO_-_Zh+#isKLJUpM-aFd!Tp1eC*aqh=yE<0I;Zm>V^1v!%p2aVxj5}Wj6zsEVMvVtu_2`qC^drC!tw!2W{IMY^5syz(D)sZ#VWP~_sHjP7Siys2$Jl=U@okEEJq!E(v;h;?l4^H#&uwyVl~?XYBs|@l;h(DOZ=oaIGVg(<#Xc4!up9f^jM`iVa5-w;RG-e?z?rKDDF)Lb1Ln(m6g&N`UtE$0oXMSGY5j9%af=d>92z64a5PQ2_gHVP=ZE88Rii8j(g?f2_6qwb35+JBTj8%mH3A}QO<Ir`)=plIlmKsDxg;+;Z(DJV1N(0($xolbatI4>4KCrVq^<i&_|H)82C@1h|zJx=s03@K$0_OruddGv`_OjEc;kioc=wtf#9VB682v}FFUB|WyH8*n$(n=v5$k#_4JA-NnZk5Swc|nu_Jr;@TCCKeSxi_MZLGeLbl!DS+r1E9fWU91WR^o!P%c`&`53f>(dypF@`N&DDGj0bzE4#oG!714s18t-v(>Z%7yaMX=$Be#7A$YW^6zPo=D5<@eb|rAhKDH>W@-m)aNb?8rXt{e^a)Q@mMq0{eel1^$;<ssomC-kH(_5t*N*zsKt5Hslv`0J*k>Y<Nz|ngHHNizW8FY|2Vk0@!8e!-v`o3%`NhA?~CG}^lR%ktt6{KCA}tQ@y|)JQw*T^kFc$_Vmx*%JZ+-8G`qpO`Jn9^HK6w~5q+=<e)b15zru0t5H)DsIz<PiAf<=6Sf)2xzx^V55eYJ?TE`h|CI_y|>tAgap;Cg|%DDq|@<7c`)YBVd7r_u^(f)GH$er$?t52Lqa6H_G^!Uh?W9U~2y;%lP#xWp-RBa<M0U(gSL}P-<tY1If@A(8Wfh5MFmPaw^C1FvJUiEjyRRHk;<01y=v?i_wz8tKySzjEm6g-$n(ZLDxWn%grvmTIFybc|;m6W<Fgg0*mx$wzTi*zx}gnh3#uvnogLpgTwvbq!tE8mL~oYGBJi)sA{++kYGVG;7+9cvc=2?IDn51SlTAMPgNrUbW!Y@-&2vUWRS${y#y4XBI&@S+O=;DD#F9S6cTO}G&tsUzfqpGoI)N3geEW~)#~$K?e=vDz?zSo1WCzS7A6gIvgwG>BY*7>F|u5p^VY5nG5Lvjnp!@>-=kdAMXQ#B}q{TL<wf%$>?XeLb{IReLlVT>Sq2?WHf?vNp?w%V9LC+}XOSy9cRo_b2yxud<vEJ0Q<JnzHbf1{nRV;eG8AVIUp@v8BUs*afh=!LrE34T&oBf--J3YOaR3fNFj4%dLLlKD6_LLlEk%h2c+Vk?@7XfBJYE+9`)Qju$i`^wuoYoeMew1{gs^eR_V-wozu9a;Qug<f|+kPl7y}j!kq|8AhOrEMoB@_dgQfVID4V4W#CmwOrrF>pPOggE(FrVp*n9B4{%e9}<q#8I@5NlU$Qauc8U`>AEj_Vf(lo9!_Si+$12by!U|QbRYf!b<(7(GCY7IC`ciU!n<)krIXIL880P^m3=ftU`c5WoWR;DoVh6XU0cj&Z0l#<RrWx<0g|RPmbg`%b0MO~ro07H65QCt63%Re0mnQb`?E@nD`78V9&L<6d5mz+v5u@9ucLew#AA%_gB`f7x1V1Bc_Ge6aEigF^UL2q`3K&9XYkkib0Wvz-@pFH$FqwI-|KWbN3GYVf1I74UijbaV!m2Tk|2uhzH{gusP+;4*!PZIW#0zvD>27IQan&S??6gnf1tvBxH?VEB3*L54!o-<fMm`kwT5?e?uo91*6l+Yh}f}xodp{iYX5e}7xcs*+WX3UsE)mMw|BA&&PI&}%-;usg7L-c(+_8ai0|O7uRff8d~<egeg6IQ;tUQ>9osuuZqx*;C6T{a(^V10xrzP#XNYxaeDo&kIgv?dD!uyW@0ax2qRu=>sOjVjHS_WiK}}<(dA2nB_QlzUv)7lTo;0e?LQt8r%ER$>oKAw+e;dSkD12f8nrB}rTFrtY@X9btxBsxrlOR!N;kGzl(?=C}XGm1?xMaXTJ;?B5VgYc3<zBuaF>vAAf1F*OzkhA-u0ymQj)|nNi@D#G?rAuL{CZ+I_3hXHeoc5c?Wdb5u^}%Hu#s|~7Oe3h3}=4#xV2RXJOr~~i8F1?O=)yN$>2f7S(v0zURGd~tz+O!sxn`I*plV_b^KIIJ!ATkq@)jT4X7uHk6;RE9u-ZPbd_RGg2pT#BW%{U-@gCX*&BOj4gX*pfzg8Gs0!B{R1TYCQ26%ekMA0tG-{KsM*Ks@Jb(A<v{9QnV=j~A5}B@NeD<%;M2}~0h+W9?*?qHqw9jPC>^?1;vdwzfeQv63L8L}vRa~LF`ZVNkBWj~jN1!r_tIjH%mSuHB5?q4Gve@n)e3#hHG`Whd9UOA{K&U3OgFtKZ+C`!DiT;=-A7bHg@_Ym}>z$SPuv_mW;+<%0kZuE^PmypF&yUh_4fDI|$YQV&iq>N4n`JRF!qoQ-wW+BI!<x2;x=RI`r7b38#V##6Mj`bQ5_HTZE%CzN!SIssj-@$wu<+pVmnl*|KL4cBYE$D_9W4EYhu1OKI6vjyHOWHuXOga`(GrH4R~K*I5~p5zQL<bW`Otn9<e~K%9oi$}*jK?SF2*bx>0zp>=Kwzm^ZY?go>;BsADChsO&?U`xz{S5#>;u|pjOwbRk^Ii)LVaX+RTFnoqB^aQ~84M0G__9I#$SNK6Iqi50fPw`iQQ8j0kpx#2M@)+95E{<H+l@U<s}kO%6O+GMFezH5=I~CRs(X)M{9L85~?Th7#wXUudjpF|<Kr#W<Rg<jg5Ix|oHB@r+~>ZcktB_P=fYQHx?Vk&C`Fb;x%uc@xwtNaS`UCe~FlEk}yrIFQ5$_Mfmjmc7lnHKBPBYIK-{*89bz%Z3>({u#(*V~v4je4xRR!sN|Xi)HTU9j4%R7~h1OTnmaEVuRd+$p%{ia!<LZwBn^how19;+BPETC*0aYp$B<qyxicsv!#Kl;Yd*d8=348*Ig}VFh;n8boVMV1dAUoXG$IDv?(8GXjv25>i~{>A(3ezU~yCc`jd~4qG)}Ccsd4DV=-Um&SarOsYP<4#sMp+=%+~Qy->Fy;1`P>OIx7%KFzISG1UeTJw#n?+hV9PLS?VhBu99eX*iB(DewJj;Vukd*{7|Bgi7;D+U+yw3iXa$(uG=9Iuvf65NgJV&LV=KhVnF!&?*fcAyJlJ2bZS;EyG&tm;eMr%ol{`xfTWL`?@-9s@1Jj%FdtyXF3n3H%xZmq&YHWkZeN}uj*?`Oj&URwEd^oHf0*3!eGYcR+u_MFQQW@NTMtDeZlCD?x-C{@w-SYpdLM@1BtPB^5{At;gYvUZJDKesR>JN1u1=;h1Wc0;lcX;vI==dprNIkZnttv?G^z09m%mu<0^Roo%$U`6XU%=)sP0DsJMpKJ=PQ-8=;ADv*6$Cgq1GcwOzKc`;T`A6$+@)h#D{U?LGjqlQc0n9y4C;K7h3eQX~ZuA&hGSQ0aF9jTe3>0E~RC3wdv8IX`Q1bLcCPc^2J|@6s%u{V$Sv(n`Y7KpG}PJVs1VMOozjU<pQw&d?gg2}iV=lsJrL&K9)p$RFy#B(-KLBXPK>(*U{wCT&fch3i&ki3;A)kKkol$-It96&}x{B6rFPYN=-6(<pry$XZrI5LwvuO`!51?C~=~@dtD5gqf+Z2f8kNB>se5HAlRX4r8Wb_vM3>fGAn}-RJaekmuat5*@C%gFL4Wo>7g#tsa0%!Y-UX_&ig$@>LJl)9*6mN@o%1J+k$-+FQT$yL(juJsrO+UiLbDV4;lVuk1c3mPq9&ff0b$R<UUcxck*Q<@M)iwhCtwRPlLJ%t`LyRX;kQvSbFS`}E@*#8ZV~o7M!(Dk?S}x_U!I5={g4!Ur(TVtX(IoH_~PK1%{Ywvm8K>dmwMB*`c%0$Q>u$&R@gq`g)JjQ<#ky2RN1$0$>#I7k=abwCnY=PB~wQeU$1mLxSWspy9(Jq%*)-Pz7v8^n`F@dU|qgLv8~o+4|5#v#qckAr9N<XJr3Gx>Su8F>lM;$Tl21oS+iCJg_c-xD_+?UJOY0T9CCgb?DA36f=ekSn)%?&z?PWkdk+8bx8XOG;@^;&Qvn+drlshrJgPTD7kbbJXRx1NcaL2rc7aT-k0<Z%g)jmSfZaFa!#=3$v<Z>=o*y#=Ov*>;897vgSCCpxxySc*rDQPR1X06?{7;Z4eBN+uZG}4C7p<tSslbwKHSJu`8N1L=S&#uxSgm6aMnxnkW#FakjcsW*EJ(+?H&%G0FZj-Vx(GjIW9?Z|HGLm6DEuc&3K!yfQ}Dwrwr~3lSvGO_GKleAPVyeUAcBos1%0+I=}0bqfw;91{;<?W_;Pl471#Wn(>v)RY=@%(cF-$=ghkoeQO*oc#;1KX7=iCPe;R8OuRmOJD4Xj^4o>@&hN656idAG#HU8mCVMZF(CZGS-Qjhk&<tdUEfL#dkbMfiOa3xNm*Qu{TmF&UFF#C6VmyjnZ+};RXIgfR&{j<a)o0)8pm91ydaq)VyKi&^NAL##n_~NkIOz#t$cy}Ac(EH4D5cO><Nh;STx-{rK2?tmNF8p8=&|Ow<{;mzlvF7vhwhn13E=UqA8{v+=IBOytMpZ^Uk!yPtH;6#DqE6B3IO*3AQ4f&C1MmOB08_9w5ADyDwF}4zp#(@LR996*~#7rw-9TybJj%!>B~v3C%Subetyp4&)pG-D@X;HQ69cFSp{_B^a#ddVJ<pI%rLRWm5mDR!ba!q>t5ffijixY0(5^x?cOkza#wY6nzHM%y-sn<O0#p&dBw2lJOeJ)>0(W0GvSJflKde`>SwCaVD;bC3?i?j)YJ%@9VSG^0!XEmeTjF)JZ{4L#Dg6TgjB`^+?%R)A6E5^p<&Ivwq(DUda#00W2e9!h29bx?F0Kk%(Xp#gV1C&VuD!a)uR{BneAX9agM~Gna)yj?oxHOTKx_k_7avg!LU+<t?4M$tN^&<2cn^4s7Jl@hkGCCXKu)<hWbV?4&%<8mjhMBKL}pZqB`$aPAdWm;`(uO$OW!RDscTXkp(ZUZNWk?o2oINzp&<3cpQf)-3lm;I~G!pyR@Y)cN2;$RF~^pXDZ{bP&>8Xx?;6Y99TUA4Yw^XVx4((VRmsq$5&fX8Chxmbd9h;D}9b*=QA33l3s~a%a+9Bc0wVX<cR7@5pT?f7LRA;owGAiz)f7$JroOr^U*>W+zpk6FM<hMrc}yQ)Geh7PW4*e4W)jy(UYQrJ-AVTT!7Z-_~1i2xPH2?w9XfAcAc&1ZaD*?92iN+l)ak^wTVX038b4B9#7L=tg>(%H0pPK-1vhGoF3L32qyVfYl996ZXe#xj$~PKls(f4Gx&@Hn+ItgR9#0RuK3NL;;cZhy=mGWU}Miguaoe*5Y%5Ed<pzA1;Ue-l&3_j^1X`M9(VV?*Tt^rs8B$nGev}Z$1rX4$oy!Oy^_6#YW1>6kf~*XZj?>$&ttc>@2-YG(};bl+*z_DbG?mZzkb5y}E+U6bL8XZs|)P#Lu*XcCkb95KN8~VA&yo2r@@FqjrmWru|bDCglJvYir+`6_=O*rPV9V*2^U|)eUZaMk@(<!R(9wO^gG52=TINmF4Pt6(1*J%ih-LeQH1aBJg`a=obc+Bs3|X)XJ%j+sZ>yn=lX(j@&_!&Qjsx_~5qWiU5@Aa6(pU&>6}&Pu?B1QMZpD+;t+|RM|_dGW3JS;=yG1BjxSSM5jU`SCj3)wyM==3mCf2mV6ID05k!{Wa>XIk0AGgP+&F=%=Lz(E6&56RM&W5D?lzq5TFj!!4eG&C{6p9$oS=fkB2Q|7<d02A=z1287(UoEg?K?aPdnj14gi7Py|VVFB~nsZ!>FEmDW5BE;f${9bAh~cs)BB1j$x#azN}RMT29};0oX*G|X*gtBi=d2Jddtj&$p>Zp~UN%hzHBb6eLWHt(1*haJ%X#MN&|kns61uuAo<5KBT>-H^f(f?oMd?AZmb=_1}E>WOUE;y;Bhb1fFoRN)RK24+H@Hu2!&ViMPoD0P5EWvUZ8D_rcxCOkJ|-PvYb;->7uZ7mSgGY;3pj#zKo9f)Ok$j=!*o6N>-Jru;t9;$kecQ}Yse`tcLY6A8H0cYPG4dxNm)p1!rsw-YEe<((dc|=XxaSDOz#jg6TTAUc)2EjIuV;y~^H|b0NfcCrGJTS?e1tgZA@YCucmUXh(q8eOsl6b{t8G3mEyulFY*q3Mj8ryEgT^|fc+U&;^O4>A>$+crNJp^A^@Rh7sYolsNy<0>DZAJURusO)5fC~ezE=jAjq>xupJ7i@fU8Ocd`MNcLMC6tFoY|LKPHI&-msQOpt+Xpy+3!D{)6a`#I9<g-X3?wlfwYR43U|4Zk#`*wjkkKg7jxvJl;2D5vH@p@yP4HZ_B5AXX%<Si-O#2|6(uh`YS-0RM{afN5;tPTH4pNjC^Cmjls!fa(-`Z{!h5|7X+zyWz-f$X&(alfnK2s&Y{hrPu_q0IY$6G)IFY!zXhvX^e)R1l;WW)=xud<GZqshW8(V*5q5Ua;)jIcoj>r6MY5yT|rzLXP%)Ew}|G0=>w-a%2sJ@qM7|E?&(P#&!a22+G+KBHM77c&u$gSNDrStDF9*HXHDx+o4IQ9*$nNO1RAYZSRzP=9B%jZGw@W`q8*SC96I#fKRQ@|k-R(9WZU5|J_?Rkfu=HdM;x`r{1&W7!%Pd(_5qXOTYnYh4)qjYZwPxz>xnpTj_#JTl|yVkhW(e*kMN4fz(tX5-j!(Ye6m1ANyd}IlH`t$O+&38T0$BFGKUEhSDz5DRWR_rzowF93e3{!1GIz;`QmOkEyZ@DZow=L$|<+y|?FkU+y-%z6MZXp3B0sOyF0+4sWEvx2DU<jlIYTX9@H;D?d`y3IX?1>l&ZH|~E=sX>wGNw)>4yqCtD~rEfx$D`ZipT)iH?h<j*>=BLcp8R}Mp&ifsVZRss2`_QNpO#nd8Ara<>IIQn%-W7b8!+Jz^ybgZ3`7mgrr}RT||f<mpOCeA{~pt)9&ky!ZJNZgpVqQ4V|_>18?`crJcO8tZUJzG_c$K$BpmG7V~MTac!wbc7N+t+1pYR;c-j2q8S<WtrTskk4lCsE0jVo#AP_GE2$Y1)i4PjM62eQIju`5ZN(-b75No4HIc<Z@fZ+a8Vj=kA~hR9=NbgsGUfLMb9u0{JOs>*Cz}E+e2axBQfG94;hF%c0)eigYnr(Z{lVH5L9wDa*tB}H)s!!3(O0}m@VZ==EME(fdkdCO*x_SKs2+y64IH;G@ZAROECfD0Fhc_JE(6lQVCwAgHc()}#NvAHp8db6qE1LC0*)5q#J5O?eK3QU3yzF{;@Cie+F~@0>`jE6Zf#@wpyLi$d@wNx-g3j=1UnoNsw3UKC34tC;%dRH<W5Ip+guV0B;^_*P;z$QFa)eaz&Ij~0j5G!Dx4#KUc0yX`8Q@G-=D9)>HC<!KmUgAzXR;(E9sz1$d$B+^lOX~D&I{I%f|_Ta5f`2;CRw(OLHl^uZJaGKsdNgv0s2ih;9S|L;Q~j`y4c}WVD1(jqA5h1J+^_qx25fOwUOIpJoAV-dTGc#W6{>Xc!f!!uL!g_#>ZY(USGFe(e@%kfAU#yU$t_Y{Wz4^x7Nx_thRL`RuaO)VCM3YCpwfd2MJpBCb=Cyrg>25G2`#34&-zqKz$1KF>)iAkmvP4^g?Lcb=xrrwM!ZfUbYF&ItK@tL!3(pOZ=*Z!94?C>iM$$Mebl*DfK5_I#C!xd4lAN7C0*M{q3g;rst0Q^3@dq5t+N?+$d}U`?x(w)%9#=1Ey?@{t>G@w;8BbCr<e`_&PsFW;&QUcTRus_eHJQgTS7ungC&7}#?Opp?6O_)_U8Uw~=bbgUz&6GPS5u3UP6?OSqi(-(;xvnCgpuC(X30$V6g;Qc-@%&|qYx7+O`ZEJ4B_}P$vm0ho)3DQS1Ses)=>lHZC(lEvWI|?29-PtFkSp0i@es=oi-?ox{UTp@wX$I(o_*LO__^zI_cke%1r+;4l{^|Vv|D3(CF5jP>)30;MYx!q)V9C(|RmTcqaF~rXfkMV-i4_#x-idgqh!V3g!AEj^aILhaRc4COj8U%buGL&jwv|+;dcOJOu~5#vRnF+WF5i}G>XZtRDd3xiTbRZ8^ZBQ@??0URC0vA5L3g{l(35MPe)#a|FHTpGTR+?DuHARKM`}p__Iv8+VB|{ddmP@&M=BlaFW;q;i}xSjHAcg8TjZfOGZ#JHhxZqk5`2pb#&hRE8&qz?VoU63ID+KK?LHB+K7UWl^2x@Ma?pnRFpChzuk3H%%RVkHPd~mnJ%8g5YpGnd+^s5Mt4!0X(z6;#StHPK9oJP5M!gj4UB@$TWl%WcLxj2;RIy!S5=XbB=kBgrg?;1^-xxm)oo!?(93$n$Y3mZ2vO*cbtb5{&d!6ydklg&2UqhDImxy!0HH>@qHFH`w=Q*q+VKnTH9)%SIp|IX!>;#3E<;3Pp@K04%`Y@_8E~!zXyOkc9l)xDRfWuXKsZX~wSXE>3-mP`quP?C_H4#?-q}OY>owc`}s`p5K-tMG4LL(S9XuT9>nNRCoJ?8kD8tO@m;lDx=ePuOqT&5S$5r2WJtdcMuU-ho0)1#wq_b@y;>AvWm%sRcvv>OJ;C!H6E`!IHuLUcWWiT^mqO2nAq(Lsk;LT4niBNY&mPv1_(z(%6k*g!&Wh6$CaL-@`nK)e6#`}c~c>T?`SA$RzvW~e~z*7h?uTcgf{Wix3^^)kI^!&=$sd({%_U$#ri+R11KoqXTU24*l{`X$*Kva8*{%}|!JoP<}<uTUx(15eJeWz};3j1R%z+NNxSYwUDbdD+PK#6IOn5;GM&$PY%*)&2$p*qOelf43}?$}}vq$wt-39YjBTNIE07bne-#v{bE0>iqcTse^tyX|ST|@x4zJJ$UTv=E<+iFhdFp!R2>59X$lA#m&^I`lp7a9M<RQjW#!o$}FSZDN}rxtNGV;TR-3Lqe)Ai$uX6baFZg*Z=3@OiQczQum5GYuF~l$H(`04Y%L;8G3Ly)Z;M^dmPO5aTB<I>2ZCtfq-vSc&QCo=Ot3gl?}OCK(n9!JxQfHfcX;e}Rn0|W3Q~S<#<wfdB<=S95YPFy&E?$2accpVDPl73!c0Ng)XMcg!VNB#+DEqZk*kh69ljmgeoM-ojhnOEJrwL8btK)|vH4mPhe{Q_9-JV{8wzwo?cgA^G5pJ{3D~D3yxOWhKa>AsjFQrDAdWEK{;U)9?LEAkBn)Wu*BhUwVaiBJ#t3iTU;M)^%V>r^ehe!7HkGJpfK(iY(H+psE@-H@0ncl0W%CyvO6JFD_O(({spjdJ)1Q6*X0n;Mxlg}Ja5$}{ypm%qaV;FXgh}*hMM|`BR(%_O?tN0kgur)!EngatYjYN{-LV)tTi1`}MwV@In8`?~yl$jP%H>PF1O4Y;%z%xqv^D=){}GlbxK7d>IdpjvEb}?ZIQ1mlMSti-%DBFuT1QtAs8vcPF&+OkH;yje+R0n4n_U$icyf04A{kqi!>yLK^*7y%#zXfIAQ(t$gW2w=Vi6T1`QA$P-#;7ITp8%n--*YndLF0XLuudPz>p@_an-PyZC0gx>B=VUYxFRjMI2Im-ORWKNZGw(F0xuE?S(|Qk4&YOVE7ZBTk{7)0J?fWCu8hK#i->!E5QTFU&Ao5N7Rm0&6*qaO*xgy%?ivQxSenIVJE7kKUTg+@h;VRe?Y#zUp=z~-6Ut&Ix4_-LBj2e&2v=1RoTh)7Br2+Oglh%;grMF085pmMb#IBKh>9@W~FHmg4R?_H(OA0gt8cNYOpoQ&f^dh$1EOGI|I;9AK@AcQ};^AT9~NPZP3cOJxrqHpS5}I+zy0(fWb@i6FbBA^|+-#xpQ0k{$sSijYF|tVKv)4@bijjc-fx|LCemQC~&!{KCglYeq=(cjaTnSFIw&Dx2A#ZdBePhc*%gR!y>xYX3kO3<68HuzQM3|1tgG`ukC2s#>RxtGagqn=A9tayls4Ahm}DiFPqrw;3U$^vE6`2*=^*5Wly7~-sXD?`klXR!`NZM+hM+_n=WV+QF2hRUnlyC#rJ>mEP3)m0lpl}{6pL+>tO!3n^LvA8C8FW$$3&|9~r>qi2P5OlUz|f33E%4EOyvFHN^FMh`6Xe{;2GSeZXu^%Xf6cp^kO9*;r|?@|f;TN*qxH0+qgfABYo;A3@~WwWc>!&6+I4GxDD@HA|?qbm16boO$kU1(`lPE=hu;kx)w&xR(d_wrtz(otn}}GNYcAPWLvx^S{MGjLu$B2J3fLvGrF@jZ|Bzj67#?p%9CRW1U~EF|7g7$!}FZ?Sk}*Dpm<I<rorP+}fE18Z&-%gsStqIJNn8;Y(bXB|FlpsruWuP~n?(xA>t%j3y)y-z^?U#2x(I#7_5wuZ842Xj#^SM0Wf)TP^*RWcK9-8RV-a59ph?9VveL@&jrlEw@E{p1r*%I@F+!n=*V64QoiMmFp~e^YrlS-t|d0zgx(3s{^yFTf0M`aXxpX$(@h7i*&}!zkzPOmn6Ad*|@^&?KyEYEP=<jk|UPP-@e+6K4D?9kaVeOC}s#L3fCn3OH8`His{bNuU!s8YHU$<`0~NUOZTgFN*goA-!oX?&gu~CpF{R6NreN<bVPvit=f4j2|t_MN|1zuKL~px-Iad~<%$-X|CFir54H`iOqc8wyq|{bSLL0`zD77Xks&OYCq!DDs97z1|G^y_`nE5st7hqVm4Kj32E0C~;A=De2%QM!A`JuDDxosVeZSLhUJ7Dv5~DYhUURpoM_5XB+hSJ_&FjdRrp!t7_uU5k7h`DMZ+@)YmL_PpP0^%jyGjaQ%FBbAiu74+HU)BI%0lk{Vvawk`;iJhtqMB1|1dXp;IEQATGs?Sa;+cP!Z?8!ig!{lLy+F6UCJZkFFGRmwK9E4CZRntLUn^DJtnRX9+S=)EhWM15|MZBcWo$`BOXXL+ke<f$a&Df%zw~62-fg-41^a&fQ<f`J$T&YT3u+j%j8O5^#avTJ$?0PX{6_?C>n9RKjUUW=68e7Rb1|A?Y?yzm@8hsl`@eW<#t~`D0?doiR07wLD?bF9!V50n>;-D`46Y_)sc+=4ilrK11Of!eHb%e;0OwYl(jj8s|s6UZ@dv%`juzBWxVyq#m+AE@#{~2eEx8DdG@G_z4d<pksAx@', 'offset': (-1.75, -0.35, 0.12)}, {'label': 'Crimper', 'sha256': '418f7cb0937e8265453c67441b26b5e7648dab884199c1c264387c9ba5a8c0fe', 'encoded': 'c-p;veRG>i((nKJ6g+3^DIi8z@>>!qoVrfp<fJz1q->wvJ&&%6LK2dQ5y*gKE2(_<+rRD^KuC6yx_fV`Y{R_v^mO<1+mPRW`|VQ}&7vfTjr(~ThsHE|2q(sP9<H-AX=l;M$kI3tGh>`Zi)ENOMv@xzlx79BOXG<#3)4kdWE=Ol-+pUJjj;%dx$`AY6K5Xe^Eetg`6hRYXc0PN3^y*KG|8Q)2(uzh<GeM^(uJ|4Ues0%Z+xcL*7eQ#)s2UqE`C{d|I?p09;z(gpGI-$`?i~fc^a>&(p?5wm=vw^>+6df&kSZ+G+xEUDhu1Zuy$=>?Mb#;w1Z^QPM2ZQ-lVr-Th`iEYi)PBX8)fTSJxjtU3zBM?YJGYfAity<ArCwV?4c);fyPS`YjD-&~U~l8qWBOhBK}Nb#G)iv-S4k`pwmc&o?~YrzA9z@IKxc!K#?284Xw80$Rx}{n>`d2$st*$bw`X_Kd(7Woba06{k71ET}kNhglvPc@c)Of%O^VAj_gKH}dGg7^jP692TKb%%kybxykuFSYoDVlv7Pm7+EO86!S2mjgPYNYB3Fg*of#Pj|pD}HKS@{OodtK8rLDg8_>|xRU8{3VPU?a;l89%LO3yiVIvD7zzIYf_fau7iu=?U(Q=|>24KS5+@VDgDI^7vTbk!oDJUJM34t_2!_^Xam`BBUZj6E~m!Se<8HL#xXb7_f({sF<xyEH`%+n>)EfFdH6j2g77;qe{Lt_%<W14jo2NOclcvYmU!bme?xyt9poTiS$J}*>IJ<)qi{b`_8y2_jQq5aJ7!)2k-D|jWc<YAVy*m1NZ@S+LY7aP|&CyenP(5PuPA>a#wWt%j>b_HXSI8LyME#|covxOOUW=sIj!rV1LT6qx^(b!m|6KeN0%u*w#%|b2VBp4Sf>X4;qL|h7VFE#3<q)6|XVCZ!e#RRBhOjE+JgOPPfOh_Tj2FYrQAv3Bao=cN-u>ltIU>X)1qQRx=(I;%ou#MC%i55H+<1<QV@_@wxuXI8Cfe~oeqiGaQT(kAw`}V#6@x$fcuf4&r|K`)>&H0-fetv)cng722balZG?=Fb@>F<Zj>kn@){F{qwZrJ*K{_*1G=E56T<~y2T@@YKJLh!BWSnf&3agUxmZnxufZO45<uiYctvCOx`i8o;ogQd~1i-yPabHojwzd#>uNVNYtUL^%HJjsL{&5zEgDYZE|mF8Xa)Z?B%#Nl}|`2*z4V;|9AC-ieHjnTJb4_lLPY6O#s6*wcimxYAt#3)w8&DO)g1{-5MI2*#E@ikg<Bb&SAtI@tL?I*e{Rx!Qh%`VS!>4FY{w49{H*5LVSLG7Lxnt8h3#R>-9;j_`;XxI+u7d>@{j(X~#tRuCKdg`LAE44CYl4c7lC_%uv<K}l+VF_@7nt7E(MZFoXv3sa`OPg>(ZIXbFsI@b7Xe5VZZ)o>g#@ZVQ7P54eOspwUePKP=&P%&Q$&w$Jcw7(rQ{CZ?i|<f89nwH)yjp}F5C!<wgF9Nt&=I`gEuuI6d(a&YZTs-dsQU9`gvShQZgrhFOlXF7mlj||Q#JalPOqF^3GxZGssqwjaJ1!b%LpeVHoV%&?7pFu5=UCRTMZbfNbl{Pb2sSrh6i_pUYFqQ2YF5>x<OLVN<6R2tj&WDtPyR-5M>yGhjkJR!__Wn0*l<TsVo3MY8-*@_iosJ$wPHsd9*LDux`c5HkV^Q-uft?MzqyLueJR!YP;m99p-@vZSMzoA9|B$O#4A|Mq|PR5kP>yOa?4lJxvcD69p3t&aK>Eg!$Zx({!1GR1y!s@hfPwzvj*6cV|HFyIUihnb@>;sj<otu(i*UgQ&Ul)R>3~g|}7VRxg5Nw^Q$nXAxo9|DE)wE))r(W$P9bIQad=v2G7|!s;mkX(^^5q_osOW|trv$3z0lG~QsoapuLrVl)XrAI`XEl`L#Ov&Ncr?Y332F_-H$M8T8Xi=(`-s`c>LL{@YtLwtkCfzC=AV2)=Pt3j9O=-?MqCqFQO5_8Zru0p;=v)<21hcqx5RoK5DYs`I-!NP>-1d0t;qmrf>d-O8+(k5Yr2kQ%vs)rb&O$1@bPz-{h05Vd4$3y#-M-<&X>M126R6T-ZV}X)&&z0)2R)24Y_U~SsyE2F?XH6gugqMiF#`Jp(F0)J0Ab>FPEuX2>mbYeTZ_P}|EvbR)3E@D}GF@6<?EWYVgIj7B#(CId70x(k?j$*Jk!5LSnU_!^Bj}c-=a5>q%u;CPCZV@BxKKAxWcL+GQLWI@Ly@f}p}!ICTsoVMv*~Wh;Gf@mXDORr?)XxXmFBo5h*}tR2@V}tbXqxI8EZJT20Z&vj<K&SH&~=Ao?{#_ZD<a#dsCN|fJF`z3TY<}5@$p|!9ik!ynl`zBPXIhU+@DcA32kR14rqD)WxYYkD4b|ZBbamAWm_R&LjFgELTc}T`ufO;e#sda3P&d!)+J_R>wJVSU0gwoKxqyb4E|3Fwye~Jsmk`RCdf|C-e+Gr%UahJE!)r20x3>bRxq7V_8}0Bp#_<w1#_+Pi?3$I6FWzQ;)`ldIoM8<<>nd#(w3#Wa4BnI(C00{p3)+cc>TjU9UY|up+#&p!5a<s8mY_zo8PWoa`ANBjYre^P~t?&!R(;w+`ypYuzA^l12kLV7E4SsE;799WY6I=<OUD{YUp$c6k{?`Y67ToemzN{Qn<wSOs>7QBL!Ep7~%hy0LAAEV~f0A=v5@{tDNO9qh4V1&V9NzsNOTm}iK0p5hvyQ_lDxmijEc&vz-Wu}=fyrGtHx@r5?t*&OVn39b_E`?5n5%$ZKc<pjX+DH>qCc@sy;B+Pup?++d4p(|rlz+ZYtC(evDRPS9t8-$fC=Rr<-9)q=v4v!A>(`7%)yzFp$O(@4c%P7oLMpiKkB+5ZnLj;e0P~(G3T65U~_}J5;$tRa~C3$#ZL()%wjZt8gd*;93Jb4W>{S7-rl-GsLyM7IYXzjGS?#T;>e~~qJcIvpNNA$!_8Fpcay<hXGC@)LpT47IE63`KNUs>d)bMnG&1!UDJfNti5%-I}Jz}DM>1kC`+*-M9iDM&i>>)4U*MxMseM7f0O9-etHEl4|ocACs8zr?mX#dOGc6q~s^;xQ@1KVV@>Qxd1yt;V*Tu{KM{R_l0EIy{umOWU~SL0)85WcNXU5E#RLlj_>;ai>lMXFJO4<$>s|4<0t=^x(*S`Rta6H1LFi+_TOz2>b{85cNt&%N!OwmV4T9+HQxfYGAPbtRJZfKMq-k`|43$opFPM!d7Zn=An|Y`Sq3C>74bxdL7iQOB_Db4+?Z8R)?@6X?aZNBaR`Z%wIk`Irw5U#J~yZ?*{`?y{XQ@Z_yx6l-j-f{>5(M%ibAs*pz!mLd{L5-zr;I4qiB?9QMPJY!6~%9>nV~FCBpSeHbp`>SH$_)ravYz3(e>9KqEA9WKnoiesFK0S3Aa4VoZM@2Q%mfj0QyxyNTmr;lxGgHm}Vic%klK|3#MNVh?_2UQ_&qRo_yO^iIR(}NpGkA}g7$Zwr|wyoL^+Fgf^L!ylNYNY5L411AGUJF0{u~Kw?Yu6c=n$uv<y6)*|8*U->e1K=g%w4EUl~_@pQ6mon_Ma!TEi52}qxUf^CSj%>SZe$l*9xO6n6KEu3OAJk`wc2fz@aa4b4La`J8rYAq2DhFy{C3re!%5!m(b##lCIaStzfmxqS?IImNcM(Q5s~lqG`=ZTJwOK&1DHBSe#ndSzQ{zSsbfny-Txu8XD`mjwV=TytO7YtuN^WOL}oeupggot?2~ffTjK!uj!3ujj7DQld{h`Z!E7!MZ~l3S{&5yP46s<L6Mc|RUJcNbx)3XS?IL2S?@3wR`y2wyG>pbo*WBj!wDAi9E*7YWm*cJ<HR^QDR-u1@-Pn9Oj!bC?ZjZv*`a<*OpT>Uw1IbP9p%x8Ew&$V$o6^}%pdMj4HvYQlL{TAXqKmo^6#@J^mP`D!*Y+=P~d%ZU)D#EBHr$<OUloY+aVfe(ruz;5(TpqL4k}GN=qMM0)vB2)ox;!smCHMLlqKb2$tc4>AYy}H7TlC{XhWgGSQu2qfU;yyt=;`H!O04Bw58lwiTHmp_{Ej<FEE4%EB==Ov?eF!)@uq)Y`9ilA^WY^**9}Dm9C3JVMTK7bxmJXH5%w=YYC`!H<WHbA+@pQQCLPdv~53OPBqc-u}h8b1o0?^9APLGy3Zsm%r~El-yCx7f0&&-9ZW7@GR}P4>bO8qcx7t643b*(Ho|UkE@v}N+31jBkovla~X^&wlH3g6%o=UT#|*f1*>F?eUw-V$0JCYn?`if#X+?AAs=j00>Jq(9V<%dyf|ihJ;weC8*GOuL_sZeGkGGag40hT9qg<W-RztLIfyuJ<H<=mtm`jeG1GLXiaUhdqBQZ8xeO=rte8_nmn1J}7IZ11AukYmYC{Jnvdp5dglB}AwAv{_sU#JurgMSzCR&rt5KN-TZI$lS!ICu~#^rl=9mK0Jw<-tiY+&l9CMo~de|&g%<B9szwid7=2GOu`=c=YQX_OC-RN03|mE}0-V9O3@y|SwfFnU|ld&(uiKs*LwOGTmB1m53aS>)n|Llb&I8TT4CcUxQ_wK4eRPQCCL%J^p&e7(1D>4-K7H5~ow;cZ~*-KPa%v}U0iT+k6Pz@V%iJ@52wl<BS<Dhh*qm4*H&$fL2Z^8iXWx>IBk36Gd4;4)3v9#ww*Jgl7Uw&&sXJ)H(Y9IrL8Ea?;$wCRSsgd=T+Wz>N*Ng<b`iY73oZNEAS+t17C;bi5;O#<S^2RkIE#_&#PkS1M~?r~;HQk<jk-p|J*Ry>pOQXWFWM`Hw59IYjfU}%fpT$Fs*mY_N*hw-Klxm1o2L>Ypj(zy*Ck|SOr0;ywW!Ibnb7GdGUbTFaM6S6<2#JD4|VV`I7m6qm{mgY;gfv>U+d{PTYy7&OZgIus%?>@cx^ICb~Ainyau5SML<ej+3r~Q9@xFW**<HMW3UtU~adt^Fw&RTEI|8a43e(ilTi}`9XN}v|>tW)>MIisHwmyU7sE@<;9Ocf-oaFCx!X-<j+6^aV=T*``c$?ZCDGooM=jBmN5*72Ui+%zM$;ofbsr%Adw<}3>~GS%_jo*InA742h3SL9JVPgh}4!0rBGADoRA4Vb_81q1%|oAZwsgop1f60)y9UR=JtxH3NfaejRPPoGM887()?2-_wJG1%Ny5yiPqiTNi9?=)*vx})`+=q1#RUjOrt8+vWgU~an1-E{PYy199X=$_BSFGqlReev<)%?)X>ji!?j<Yuk%(4WQWD2SCui3P?2#LrGc^qK@k;OZz@ZufS}+$>zA>(E-*EzUsj&;&;|DG@H0^!c|7x2;dIpn&Jc%{O@wlCu1di<_$tZ_NE|i0DIKPB5=4!_#!I&Ri;tXfpH7UvCKSy8n1HCVAxM0XQo6Xu}#6VL0)+&s$rCz(X(zmN?ve?n<)@O8PquCt;GZk|_-sW$PF?lcp>n;$TBcd2by*)l;pQYLaw9z}6>Ji$o=)Lz+iL6DHM!^vW=p<USHXJoDX$e_y;c_qOm(wh<UDf>~JMnscpaF|@Cq`T6pFV~|GcaT=$Yn)B-Y>+?oy8f@XSaUuy@YQ-1-{!H|E@s^~8Y@gZF`$v2xduH}%(;QRphuPz<jwy&#NUVx0bXQdat{YMxg*pP2QCtmH;j}EPBa+|}OqRuF@8r8UYtv*J%`BXD>SU-Evxh)y>)J=5^@aYJCU>#$IC(yTn)TkseCn<D67gO%Hb}RD(5FbaiRVXYxrX_DZDccMD>6xGFUFqU7OgCdJx^1cGuH9Qaf_%s*X9qaT};Rhn`U&LLj5HqsN@6M;)S<I;3eU`_?!9*cM?sfvP2rk<KI+TF*T0W{?c2xc=aL1`6+j2q!gK-C0#5gL*@1L+jk_Xmu{3SS4BQBUk7B>zrld!kR<jrSjC0UI+B{EYI+6mlQ7SBTJpkbE&qWf#?g4EA+NpG@H}45gPm4gx7Oqa{Jn_s97$dO3gI={>CmZnxX_KS2@jCz`<i2iwB<!dO8qcd(xHzuJSdA0SI8#?ClQCh2ZAH7(;^kAs5VUwJlQhXl48Y)MsyX8B!N@sZ#t~TYLQ=N%anr<3*K57A3lq;7?_~7!jC4TN^?f4DrP0ZFHJG3HQRrgs#57@HPwsinM$Nysp16v3M#r;>5X+8O(~Y5N%pn6IgLqUWREOo_Nq7!&_^19k(0Sh`U88tO3xU3dL`V!9wex$I@OX5YYn%spO3+i$VZ?d|JR+Y7R%gHeCXsfzJD8Ta-~j^^k;tSk2Y-2l6F*bp0d+aW)OHStT7wuNZ}Tzg)X!rf4M=uwPmn5gP}tOoYP|tx$SB>fjw{c)BUu-5G;PU*(nX6a*jQqp=FFnA^<oZg%qoWfW>hvj3<@QwP^Q)c<cizABkurIjqq_WgdxsMV$k-XE9EZ)<>aXL%=Vg6xPYW89iECC5S3E5wpdaZo4z6F)~YLX_6xvt2_GeZ$Ef5kwFY#Ii~3h2$lMkjNxZ6E$Rc=WIDBsbRaT6A=JRE2#Fx5qdfI_-!*uIMA?3oi<Jtr3~Oy*0uW*|Ul5+>N@1vTe|08RyIWbHoqh!lSv=!gCOgR69C@XZ5bIa%6(y!@X9C*Z(|emT4N+k*;gm0UMnX5DvnoiUDYAAk92@G?kHaN4^6+Rxm+3%K(yTn1C8UBfd(^gBhL@HIhgOhM<s_W(oP|r27`&=7gb*GxRM+iZc4-U)V6Ve`O(0acb{N#_IJ7Y41!{(@IfsgCXgy%V^06737}p#A%}m%dQ$w3&AG7!Pa4@uh8igo-acuSgkeQ^3#<9<MHG2ToBuI&MLFayL0xJDZpz+2J1c0HZEGG9IZRcl2ZWh%NnP<_1f1hUY<bRQ7lva9>0#XYZk}=}3D#{}J2U{?7=%lStoJd5YNr{7KVr@Zd550k!Ofpf&G81Q4SPh^XU=nN6Dr~#*VpQ-Be*`aURQlB?gW0D8Ah*f}&eEB15G@iNYCG?vY=!`A*!6T?Pd_~3XJoGR=PFBQ;)F+_>%v2xY}j??h|a34A1bzA?PSnJ$=d54Qe8jKdB7zGT=4*TP6Irn7X3Rl0hNSZ<hP)D;@nBCn(j!w%akjXbf<V^>uq(ge&ux!sseg?{;GI&)ad~WW$IhyCPJ}fbwmkV1-!Qod$NGLzZv4u<)n)WXX3g3yea0S9r3Q8olsda!C`%V`4-WGFl^JFKv>~c0fu@@L=ug0D<hu=@Z^F$7y`bJK&&ZxLXd4FH=9OtjXz0$%8G!tY)l$vF0l}|RRQBYMxr(ecJDFDlqL4lMK}vckLx@|9$e~4^7@jr1|}8tFs6ro9C&+Dz5DT~Q9MHKc|RUEipNNDq<P4`@#5fFJbD(74|F=aenuMKvp6`A4go!ns0+h?;2lZWg}5X+QUC~HasDJp$ppEj9>|q@99k#OR6Ya&#CsHl6_=E{AUhVVuHzo#p1|qROPg;H96R)O*5$X8?n~T1KoTA&Gcdb7&6b=HSI$ubKocm$F1)ak;9fW{YQhVn+4g@QNnoAR?%G{uKuMA)7vl}O4#Fck%N_!a``qts3>RLfY%J%wu{XigGAo+YM2|pLuxSgm;~GyeBMMy5VPiV?j-Ey_mfaF&^T|S(Fh}@#7*C5ZZ&-UvCnZaSS~gwnmG8R7wz()QM3B5T$+6w3RU-m@j{;GhjG|teJvkXw4^9H|Nd~YD*8^h7d{3(~Uriz{r3D>xtuO2$*GuGBMCn)Oa0I**>3v0rTwVFrL0?NxypERQ;Bl;Opm}hV%SwYG8C=Q4PpFF4V=e8$@z9aF(Z0IU4&OppP~vi{cvKdbbN>$Sa@VoU4+&X@(S)P+wDsi@ow6wy9c!#`%txco&HM%F91%n1n6#c~v0C_i87WH1n9*aPS@{C}K@eLF8JNAmF-N3&VAE9hl#bRoSjtSaZ-C;viVNq)>zFMjBM)aFTSIiDGS6%t#&KQ-3Y4kF=73XLY*6=dhX&M1H-s~Fmx|^$6mh7;obZ9Y!_;&ZX1Iq&@Ec_cM7UTIAC1xpaSaWK4ib#WR~cp{>P~2_AsKfpr#RFg=LqOt#T<;$1|itoh+*yDv(3+pQ@DKQRTgSZfn`$v>a3PH0LdP!*#c$e|I?}o$aKB-20x?x>{WgG<IJ<xYoyN7@6OP6)t#I*?j}i*Xak5DK?W|}ukEiQB_;N_CXwipoI4Xj&D^igR?FWzy;=tRx6&pBJq?)d)^?>+uGd4y#Gd+#Bciv=70>qJ(f3M!K+62zjCZo%;RC23C9_>fCSAosQGq(*XIZeEOLCS2AxX*-b>Q%UBF<bk1}V8drk3kjEko{WZQbwMa|x@ZZaVM@jZ|{JnI#7{(#`o5X~v^QnlY|~8L;f6JWv*@3UVS<nT~EwRUUDwGIp30d=Fjv+z(WN*+G3&)6@49FbpYodKjv5=!b{GUp<&H$vp-5omMUAxUivh?o@<akw@Mn*EcZwA-#qAO{EUz(SLbi)B}8a&k;h+IeT0NB12}9A6k>VO-F)l>!ia*udv#15F3m;eJdnVw?QNey1XSbw41rowF@+ehtniw$?r#!+}mlfaj(Qlc}{R<vc6!cXdzCKG|en(+$sG!s|SYlr4H7H?ohX)LZ^INZ@nRv+~gD>zNSb7+Y|_}_GH^x1oXEBgWBk)MFIgj5V%Dt{lBn{)Hape53xYYSjIsT^6D!|aMut7Y;J&>z#n%df82pT_|?XRM=W<+THNu$RdKx$1YQGCK%_Y&MX)~_?Wr449jR(9J}1~iP_g-7Ip`e?E2!z{Z5EBxssgSL_?Z*?N2AJpfWdzEXfl0xE`wq`_q7xoI#%Z3MKd_lCm~LbL{?xY>3yOo3Vc#h2k4|cOX<8Bg?>7n!lMd=lWn*3ByZwZdcnHbqj?A>hYn!bqk#xAhd875t9rWsQw>Jt1TABW@AQsK3W1}{D<#&;E!E96ZaqdTDS5%<i}y{O13f75vTK#+>U)*UC2GsT*6cm%Klmc>yFlm{29-24DIe9!sg2#rLo%B%5%O#8evwX6k>aSZTXLfgr9IhmHfk^!%J^EDJ#3?G55IWmM20Dob?sJ}DMEAcWWxQpH~nX#Jk@mOi67W>YAxCVhHA5=-vbZ;jhhi5Q}1zo1X)vr0?jyZ=4+C!Bo7Z#-FgKpKrihaovM4LyhVKtO4I)(I(~WJ<6+Ag#>3OukMy0&X<3PA$@pQ1i&s(^FoGR}AxH*%VJYo>TUa|)X)O+6gL!m97`^fduU1Es7^K)C1Om023=PR(mi#$G(&<bmBjT>XyPvcp)!SFS*=l9|TD)L(Yes7Go)vSJ5=}r-{gxC7j}HT*G~WvGB!tz4V%8AU&S&D!E`p5y63uW!Vb|h6g)X27ybm;0xI>ACnUJSkJg8iZ;u;dA4Y26w=7i1)7yGe^v}|7uw((2clq1-!1#*D=aE)(Hz;4^0x20vsuQ@)O!p3gxD&pk`RlCOr?8m7$&^cH&1$#%qIkt!Wc|>hh8rP57N=(cfh?8R;QI~d{LZN!OuYIeQR>qen+2`?GC2J`redV1Jzsp6vQD!ap($&vLbJY~fI@xSd4ekUdZn0U0Ze9Rya0FWB&Becc)2^iJ&V*#mUZyb8#^Gdzn;TdjQZx+2N>*&O;fp6r<RllwissI=Imo9#2m_(6Py!fI$h)Y*wlb4yQd^<aZcQKwe5F07`Eo0i?NlLXrxv$%RKVFWKYY5P-`C4<%qhO~YJ4QCBBsK90cT|S2SwwpKJN9Lj*F_kj6rK~_5`Kb+~jz48M|hsbURqB8|B*<TK0ZP;>@l-Qox;9aLt1}D2mMD636tB>EvVI<z`-O2<bz^K*4FuYEIG>Ng1D=1E#}YSK&w+(%nQ8AOS++r@EIdFv>XUvTis|vq^5L=%?NE8!=<6N><vRidU_3@7H9^Piy<T$Q_r+WjFI0YX0LYe%(*Rxuohd9)n0eauE&pNDA8l>!*z@kU`Oirw;Af#}sl_Uo6Z=s!F=bXd4ucJ&kLYlcYUJ?R4p>Z)v&tJUBW%vug46?GZ>D;;%8KbP8BR!j9Q9ZQCW;PdsnY(>#2bL^C+!=xo?d5>=D_ICt>vh0Y#q1WFGEh=dP&sqO{cOoCgFgllz39Ye1}38ZTP#B1eC7=9KPQ%h%dcu1@N^ykf?$=^7l%8_Y1s=ZEBd;jsZ>2TOMQ~`X}Fm$sG*%0-2+WL4SvE{Nzf2SzlF2^?u0v)we`3)u7?iZ4F5+ME?B>;I3+_G!#2#!G7pw?aBeUqFKv&Z=&jyV!1p~-ob1f8oAS$rBqvZX3@vGVwvRk)rbs>lq0e-m4+kZty=ji+h&XoOcvo~ja7fO>ISl>`qcnMY2`s6zZSUNhQ@q^~3qq*pFg?F$u4gtTAMT||lZRdbj;sV@#sv!@t^b$ZN*7*z}(I<Y?kZ}z&SpS<#{E7hoUu$#Tdo$rn*?$grZ+A@#K-qx#QZfi}1$1UZGR;10hQnjTqDjlwDP%6Ptml3qCv}P<+!6bMPtC}<Glr7;XFE%NuxQ<aX6ImUUhylqZUxWn^sl*5dS0E6}l=Thavcp*}((3%trho|F5+RO>Z-#Li;+g=d5`m`Cj8?8vf3SB&P^@STChgv2H4d}#+kq<AeG!ntYDjHCdT+rR3I}{lN$A5AcY$U11irhVorS=M3t>n=-e*7>1Wa8#-USXsFp0P$`@sC))KJ}DC<4wF!f^)n<g^dDTFl=A&<cuW0tL>Nps|EEk(j#0##Ev54p@EAISB4@!*zlk&Kp(f@a~dUC!xHhhgHcZkhE`eNg|MpYotKQ*@43lunqv@kR%3#3Q?&@j{LCp(Zj=UEJnT`uD_|z7=AzehT*>h?C2}mpiAhLw2Ab`M+uehCy3?a1VA{O5F7|RDY2!bl-X0$k}Mz`%u?_Run5(SKwyaf9)Zt66H7)*2-CR!=|;d>Y+{t&2ic;H&+?74fS7mEUPp0ES}i(81)A{Z8Ik;vkF#jWc3Q9Y*+r0{2r{$BRup{11M`6f*wD{cbLdF5%|TPoT+pull91)Sq3wvcO-b@{GlZrf%{EMsYHQ-Ve|(n~7p_V5Cgve3Hx%b7+I*U@Cp&cgH{*hk&mUo11o0u6)bYj;qJxo<PWdy0>id6kltHzJ%clIQCrRcM-x@?rC_-R?58wY6_X%`6nfj+sdAqL?2WwWP^i`)Dm?vek$-@nT>p#rWoU4=^&#R6=w(7POFVAaeRpz@4H+V>;FtpUI1lXb6j+W0ge13gpklC<+&^GB<N6IIrs)=0|ize8&l;C<SQaL6~DK0~)$ZrL<P@cg1y|0C1i&k&8+ezA1(uVP~Aq6X&tzijLrJk(K8K(6HoN1{AW1j<smihkT6E0%><zHQ#zx~T}gwHExP)yUuASAB}s{>MeeewRorE&h}%^#nxKK#$cTjS=##TEUzlG`u;?Dh>gI$-J;K@17AF-9=R_$)DkqI>j0B2+|)nNRSMULVXHWoeZc%V@<YSAN%OE&6hnG^ci+u5wu^=h3QQ^g)+DE~nd+29Yk{5A(IK3jg!fr*|JdUU(&3gj7LyyZZhWw><y&@zcNfQiFUXtG(`;J*#`>4Cv?h$T>S1+L9q3hYwOor2|#-T?V=SaQVJ58=l*u54BmisQEsAxW19(TYR1~w|4rVaT^|65=Vm}G*9mLiG=ml2NIS~c9x3?ZG;cA2+97A`R#i-#`Vql<=gYCx89(3->Y`RtGd=zUgoMUaW$@P4ME3sTvtgL^-}D29nZ|lpm5}e2z588V!OpCj_%0L-QToI`yfP<FeeSq+D4XxV?;$aZuyIB#&&};gISHlpYc%F;uw<K|MF_c68{oOE`)|7WNL_TS~u4@s3T!G=nfx+6$Ig6zs1=J3NOn^%<1Hxs;rD*RApRJqeOe_Hf2%*rwIT7R~e<g+|prH&BeT18@N~BVkv4OtX`$|Yp{K{Z~H>uBe(eWU)>`#LSTc|OJ$bjwBl-?^J{9TCpCsY(i?qcGtn<EA<z+jjc@!WVeC(jrsMJ1S+{!{zIf4n*?lqT9F4}^FnIo=^YZi<&aP64u3vNFFI%rfjTxMsbVww0hO#;`0ipTy%v2m~q?-8}5_;1@sJvi=dUgSty>H*YS29(d;}8nD#lMw61!}k0Pk#s!ZFaUzUv{dOsZATy%7)*op4k7gUsASChI{Db`}XBw2J@9ylC37Y+UF`6%5s&Xa0>ehrE+87$u+i&+6_S+L-4lPlzngwPKTG5oqSL5DQA-CrKm}MFpFyT69QoGB}etQW#|h}gYwSVu&Ufc^n+c}8M3GIz+|JP>P=eb<=dwY`t7TQ6;=BW9#M4vvD(d(wM$$>Nx%hOx6@Hmuvy%^U{$Ybc*@~@9^Wc=!?3)IwEtq2<sNq&{nNEuzdr7xSDRdY6IE`I>x-29#y2IQ(R=3k?B8Z<nvPewPRrvf*`mS}KHp#aw%8YJS=79zrRgGaAcz)L>MT>@{M1Fp1grD(-cMcqjc`9)#bM@IJa@ZlX5(TCuKe8kcPp|a&G!G0%=ydYa_(c<wFJu)Ihpri=D^rg#`WJrvb}KWx_yH0NuG5&{4q)M9T|5fJ~Y`rLc#G_M=oVs=2e7Gc2lWCuO}~X7aRt3!|dQBG#~M0wgk*`QeI7`zCL~bM>{2@V_yPcp7~kb=Qj`Vt}kK0qMvO%UWP8?@3(vA+Yi@&H_I|wp@(1n3cpPwY8>Dy4#Q~o>17`@RNR2)4fis+hNqJC@m>5{DVbFB)aOgm9@pvHOx)e0KP5PPt)={ehc9_8oV$cY9MO)HXyd#0ZN#~c$q-Xt9NYu8)HEPh?kp0!zBoEtv&U{wmVI)#$;hajH7-+H?h(Gkexg3Dt|x2^rM&qw_094qm?deB8+LgTEb}?(IQ6T#i{8MB93A@NPxMbCP^*-TVmkh7VH{Pw#mQTtn|%#-B02j<ksDi8z^!&|>nFpDIzqP#5F8}6$xM4#iHJ&&d~c=dKL_z^p$rV^?Zso&Jdabzp|odlVn|c!*v_DN+pN0sr5fvNU&GyW770l4*J=D3Am#Al&%=5g6@|pGk1VBj!SEL%xBC0q0NvT46CeEOFlzZL%si2NJX+@-Q9m{{Yhl#4<x;9JD=>rPcK&ZaIEZSf$}09K(WTnxJLKzm)iZ0*O>%~>qXK*%B<g>wI79>WA5GMuX&h!M0LmNZSWFG@RLQld`etxdeG6({ng$^#OGOW}1tn)FizBB7Ta)ZuPBF3c<}tN10KN1Psj<*)r;hA}&MMsotz6sgB})EXTi0H8AoK$a-kM+F49`>ZmI~!ww)DKmXnz}r;=jUfwt3>iifDM-4~3wG^CSx#0y)g`DtX{XF0|Tw^>NguRrii}9BhXT_Zspg1NIJ!>RMYlXGQz9;n{qHV{Hl~kd?3eXv)XNgwHGXs}(aR2sLjz-#B2U(a75-{yGGS)OKul;92%N`QX`8sHyk)-hzGSZTm3xxbXJ4FY2xfnnjEpH0;%hz7p}hUpz~m{Oo{yWmWwk@04vY@7rx@+T9MTFTYw(+U!FOxEzuH33rk$rYB);DVoI|-=~7O{;?u1s?R?x$Ke<-yVLSL!*Hr&9d343YOFkFdy^4I6oEvgZ{Pb8MB_&gxeBc*rmA_9g?NVEQ?6!7wU!|)t&FqG-ESaM#p9YJBpNBT)PP6X`MS%t@7}5zjifWGRjKRVI(Gh35=7hV6=kq}XB1oiMVQuVOOuh;EFlyU5pk^US1U{_K-A^8YMgdKc14w|gq3m*32$!g%mR(+xH?kR`CWqA{JQWYugegQG-{^)_P44~XWTD-s1c(JDa7}S9gVny|3IkIeSu%6%!7tu>|A8WzsYLprKGbjH@HE*TJnUR&fAgVr$2r`ouucsiqESz55$J**Kt#(FQQ`&Nwsoyi(WtNp56PZRQLOZEVnu^%eJ*|2sF;;j&!;A&~}kdSok;4t$0Z;mpdlDbN23vBpSBB<u6Vmm(1J#{uxzaW3rHJsc|T72q_BJr2I=xy82+#y{lfkoP^Y1Q4aX>!NptmH{+ZblmBD6MS$2I#6PF(8FCd4Fw+qM$~S7~tz7uo;C~jQC(^L^x(p4+;XXtKr?k=OJrYr6#qIKc7E?oVQ1D?Ka$J=;m1B(va^i-tV4e_Z@I}pP<9j>b*ihdDqqfc@^;Zc9O5cE22Nhy%dK{q>p<G<UfVE1f%yN9@x%p8L{k<`I)7NY67xfHFx!tzdH$wBHWlU50B>MTV0U#aGzTf`XxGi1K2%Dly(|45=o|KmdH5I9|S~CUi$drXV{`EW{0=T4tPpg7X?tkbncHleukG9pxj@;@;zA(PP3&T4pSRlw~)Gy^3@gE@J@@wV#lADC)P%G69ne>>t-hWIxXS9?Avrk3d&+p1nFh@R+Fx!9FOUU=2ftmlHe-NVKXB>prMSvUq6SM!g%eDIK-9DEq)v67upL*&`rKOXeKSj~V<NcK|3vPZl<Xk1?p0@5=cY*%I%ePV|lB3-0sRzg0%0uG(G=6Z*5Z4|_6)(H&9{l{jj`9a48wngbM@c16ETe}oR-e7c2Xn)C+U69lDs73Q@mgi+Rgv|Uj@IiCJBQT$H=q9T`QydS#iJqi*8c$pIW-~', 'offset': (1.9, 1.0, 0.12)}]

floor='WholeOpenPreparationHardstand';box(floor,(-3.35,-2.70,0),(4.25,2.80,.14),0,'One complete low hardstand for two separate parked preparation positions; front approach unobstructed');FEET=[floor]
REUSED_ASSETS=[]
for row in COMPONENT_SOURCES:
 raw=zlib.decompress(base64.b85decode(row['encoded']));assert hashlib.sha256(raw).hexdigest()==row['sha256'];E={'__file__':str(OUT/(row['label']+'-embedded-original.py'))};exec(raw.decode().split('# BLENDER'+' PHASE')[0],E)
 prefix=row['label']+'__';off=row['offset'];trans=lambda p:add(p,off);mi=len(PALETTE)
 for name,color,rough,metal in E['PALETTE']:PALETTE.append((prefix+name,color,rough,metal))
 for name,g in E['G'].items():
  name2=prefix+name;emit(name2,[trans(p)for p in g['vertices']],g['faces'],g['material']+mi,'Reused whole '+E['ASSET']+'; '+g['role'])
  if 'face_materials'in g:G[name2]['face_materials']=[i+mi for i in g['face_materials']]
 for a,b,points in E['LINKS']:LINKS.append((prefix+a,prefix+b,[trans(p)for p in points]))
 assert not E['CONTACTS'],'No untransformed imported contact records permitted'
 for name,p,q in E['INSIDE_TESTS']:INSIDE_TESTS.append((prefix+name,trans(p),trans(q)))
 for q in E['GAPS']:
  r=dict(q);r['origin_m']=trans(q['origin_m']);r['name']=prefix+q['name'];r['targets']=[prefix+n for n in q.get('targets',E['G'])];GAPS.append(r)
 for q in E['BORES']:
  r=dict(q);r['origin_m']=trans(q['origin_m']);r['mesh']=prefix+q['mesh'];BORES.append(r)
 for name in E['FEET']:
  g=E['G'][name];polys=[f for f in g['faces']if all(abs(g['vertices'][i][2])<1e-8 for i in f)];assert polys,(name,'no original finite sole');f=max(polys,key=lambda f:len(f));p=tuple(sum(g['vertices'][i][k]for i in f)/len(f)for k in range(3));p=add(p,(0,0,.004));LINKS.append((floor,prefix+name,[trans(p)]))
 REUSED_ASSETS.append({'id':E['ASSET'],'source_sha256':row['sha256'],'unchanged_scale':True,'unchanged_material_parameters':True,'offset_m':off,'new_model_count':0})
for name,lo,hi,mat,role in[
 ('WholeLowRearBoundary',(-3.20,2.59,.08),(4.05,2.72,.39),1,'One low rear boundary separates parked equipment from rear edge without adding a roof'),
 ('WholeLeftEdgeCurb',(-3.23,-.25,.09),(-3.10,2.64,.30),1,'One short side boundary; long front edge remains entirely open'),
 ('WholeCentralGroundGuide',(-.29,-2.25,.136),(-.23,2.18,.145),2,'One thin warm visual guide alongside central preparation gap, no real safety marking claim'),
 ('WholeRightGroundGuide',(3.89,-.25,.136),(3.95,2.18,.145),2,'One thin outer visual guide for parked implement area')]:
 box(name,lo,hi,mat,role);p=tuple((lo[i]+hi[i])/2 for i in range(3));p=(p[0],p[1],.138 if 'Guide'in name else .12);LINKS.append((floor,name,[p]))
INSIDE_TESTS.append((floor,(0,0,.05),(0,0,-.1)))
# True whole stored-mesh horizontal centering, not nominal primitive radii.
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
FOCUS=(0,0,.65);ORTHO=10.0;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(9,-11,9),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
root=bpy.data.objects.new('OneWholeFarmPreparationScene',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole horizontal bounds centre; one finite hardstand supports reused complete tractor and separate crimper';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
