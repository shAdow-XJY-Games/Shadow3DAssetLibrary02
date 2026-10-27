"""Whole purposeful farm preparation scene; two existing models reused exactly, zero new stand-alone models."""
import math,json,hashlib,sys,time,collections,itertools,base64,zlib
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='industrial-whole-raised-slip-roller-and-standing-bead-former-preparation-corner-scene-01';VERSION='1.0.0';TITLE='Whole Raised Slip Roller and Standing Bead Former Preparation Corner'
DESCRIPTION='One new whole empty sheet-forming preparation corner scene, zero new standalone models. The complete accepted three-full-width-roll side-crank slip roller stands unchanged on a whole four-legged raised bench at the left, retaining all three long rolls, both end cheeks, four local adjusters, crank and upper release-lever exterior. The complete accepted long-throat paired-bead-roll former stands unchanged on its own complete pedestal and full ground base to the right, with its original opposed small rolls, deep horizontal throat and side handwheel intact. A single broad chamfered shared floor, low rear/left curbs and empty front/central approach separate the raised tabletop machine from the independently standing former. Both complete originals are hash-pinned and preserved at original scale, topology, four opaque PBR parameter sets and fixed pose; translation only. The new whole bench and floor/curbs are scene architecture, not extra counted model deliveries. Unlike the old three-station triangular-roll former, tube bender and sheet-brake workcorner, this has two new whole machine originals at nearly matching tool height, a complete supporting bench and one separate standing pedestal. No stock, sheet, operator, loose tools or process link. No bending, beading, mechanical compatibility, load-bearing, ergonomic reach, working clearance, flow, machine installation, navigation, engineering or safety claim. Rigging, animation, physics and runtime interaction not made.'
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];INSIDE_TESTS=[]
PALETTE=[('MatteChamferedFormingCornerFloor',(.28,.29,.25,1),.97,0),('MutedWholeBenchFrameAndCurbs',(.24,.29,.23,1),.93,0),('WarmWholeBenchTop',(.42,.36,.26,1),.95,0)]
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


COMPONENT_SOURCES=[{'label': 'SlipRoller', 'sha256': 'e84a2321da35ccd8397ea5316c6a660c6e204c3b3f1f7be831e2d129cacccce6', 'encoded': 'c-p;veRJB#viJXd3f<khB`Fp%;I{;#t?M{WHg~g0%J!Z;=kidL00D}Hge8GZQu*#r|GH-+A+VFwJ<pS>*f6g>J>5OsJ>BD9e);8N8qUJlkBs|y5(P#+PlKR2T}4szKAhz9W|~Bik%g0>IZplf*2v~TkQ-SPF1ad5jY*g-BY)E~vfR(ZvEiq=k;Ku){pFWm8sTD@(D#L(&z;X%5<7E0n@8cu$u^mjhl{`&W0Y|oCUNG3d64Ew5@n5Pnk<YZ^`f?h8srmwZCu}+U)^}<>EefF_dfo0<DtqL4yR!h42QOx23ZoVsnT8gX%Od)^Xu!&8_x{m$tug!(2tta@FAEq_bxYU`thV$uDMxRZL`%jd;hq+x_<ZZgJ-tgmfJFWH}7uVUwY;n3~Ah8NaGC+Y5a{LjVlak(2&M84QX638n0<ct_f1J@%r-m;_BU}8y@px92jwMA8ibOmCuuuhLo*gh>cMYkLP)^+}(&~mT#z8@IXimlhjp^jFZJO3i7~+l6XcaO?_%iTe?UR0&cvC2q{6D8QId0jr=|#5(vlGXMai41qAk(X1X<|slN!aE;m`zHicsvXoF23-%>-`usAmalFYadX>1zLALlEgt=Lb~<lYDt%X~va=IO?m`Adh9lF)jIgz_*RQ~$tEjbu8_0zH;%T+(bCque7^VGt!5eo3~;YBo1MC#w|1oYLY5s4&hGV}x~LH;sAVPcp&_tso+B#%YpeMji&TJ6PB>j6;p8MY4(ss+lomM6Z@ig!#M}=M7C(qBonP+Mj$T3R}<`o7p%G?s?=n=;=02M#bi2#?&9vmL}=FpH2=(ghPBVe3^i-o)LBo;>~$3u+IoH&2d7wC<dWs<0#1peDskGC=d|Lh@(mj1AQ8?!pNwR-A}QV#w;a@T&BrqVn&1652F&EXhs>^e+X&S=M{<yrny0Qp%x<ok8sr-`^yqOrUJoB8bpDg1<feH3ViBAgcuVF!b}l1FJ(gG6QJub3r7(aoh$-S3$-Gi=oxWhB+*1sfJ1W&hL|=Tk}~6YNQ=!@BR|W6#fa#Wz#!ohfaeMDB%P43%L!#7Q!wF&L?Qiwsc@#Lbw)(ACK+*0<WC4?N=VWLfuF>T(=1AIP?>_lA?Q*bi6}|rCasAuaF4!$LdPU!zTz4Oq(v;9@Yd6Q5DS8BX|*737EV>dFPN95l*1I81t`s{tSY2a<0Kw`3W|*qY_||9@v3V;;s_fpk_nCeB}i%9aS#VodC5GxikTZ|7A54B&}Tv4#kR0Ga`d|H!<6<TO8kifNFpX*Bc~=*xk%PPrXm?l8crdLsDzsMk;C{#6C%rTkkPsn>*uM@Cx%nuHx#Y|>IAg;wAPToA!#|m07RDlILtRRNdl%`C9BN9$wP#e#LX!Xy+~xpsXqco$d@pt1xJzk7Q}Q`1_6W3gr(@sp9X{^Ofm{1nucnKWvK-bdpHe2Wmn;h`p&?S;ev<b9U%!7sKpQ#bMEMxjkn&{Z@u^LKKya*^#{F+j~{N%FK+nr+w)KS`_;#*OaAcYl1?`I{qDo{yVsY)o6Bo%*!Xn*{_^JL((7C1pDWtASJ5i?8@qfNPcE2D&g01q2|v@Z-1d><c24O3snfO{_w2djwoh%xGB4(SI!^rP50YN!z^B(+5*6sxI_@}b>*NeS+T8IujnjILj<1Pqc{&_&)bYPXFkKT3MCf}=vmL*n|7YCsgl0VMpyS_uy5N)a!e16Mat|8&i2k=<2#hp$=ea#-OoAzq!Nl^Nk=;#$oaQm|6-g-T;a~$2G9Da~AhGc!Tyi6uyO5CB*QNPHm&GcgZ&|&|vrM|6gD)*7Nxn6BwpviTCx+&;sM^Ky`|ZKAQNJ^2`t*Z7wFi#+)IwQHY8~~djk31X%8(?D7M5Rt02R#5?$X>6;CwanicY+0GhSo+Q1zBJ!GhYvkg;oL>d;6IF=AkM8^+q}3l`}7jVIQWSU$HNZ0Chtpk&D(m-x6I^rpJQ9T(rBcsihgl4!LEJRl12t^0Shkbxt3!MBjU@$ZB7U|`#ar$*VIKZf{7#4-!4wi5+0&CqPq0*r8~Mt|Ar7SpFVi0HtfR#iZH3XZ1yZWzI27Gz#UNp&w+5~ddKRt*L!(tCU7-1Xbt!NFa>+a`E>IFX<rM3EJHUYog}2k%=W+Kd6pFa!_l#2ALFT~bIEnPpR%4}jD-0^e`#p!tG_YQ6MmUtVI}it}wQ$9%l?VJ6BA?M}HLMrD^AwZl9xq3vxS-v{0#9MgWV#z&YS0`T#h$$*blPt$|PM8O0D37HK^Uz}S}k}NZjO6&nR{t6oHt$DNgyVIxdyIUih8QZjWsj-R?u(i+PgRs8y)R>3~g|}tlRxg5Nw^R4CXAxo9{~7nDF0>P(W$P9bIQaS5v2G7|!tzrH(o#%ANNK2l%q}D|NiVmSNwmRy<J61%#c1M#KAdsaDp=TlW{oxL+D)rqV=mWih=M1XM@Lm|mFwZLiL8=U4rvb}2Rch>fH|IFtQuXSqk|tzo&13bl$e92aTW3{n)QB8=9GcSsKWm3NMr7^3>L&hCr~}O8kIE7*rPA~&rK3m_+WhoQuPo6v<V^X7>d3>5I{!i_jq8x^oXL{ovu2j1J%QiHx?*a_gtwSYxVnfVE^VdxhsRXa@GW5UwDc5YfL}K;4-@)4FU)w-}13bZFy@3_SVdV+=3doo)8WsEt947+3t-<(YU2{L6imE)DN@3IA`u8IdMrkWNMioNV~{F=*wgmkLS>2V5FLa-pb%Y-9VAuQzS*TLQ4;Mx|#&Tjd17E*|eNZdrJoY_|`j1+4N$^mx`=3$1OqB!l+AdXy2mK%K5@r!>QHh*#~lrePOx5B3<zu<A`ZPbAa8Qy08amk$r_i+KGeM8PR|LAhto?KgN!s6H=eg_zx%_Ig^9~N6CZKMTs*H>nB!aQCLGiN^p?QL;5)=R!W6!E^JHTgDPxsA)QTwZ5aAi%jq~r&`qpk=fpX4pg^^pHhn&(PaWr!%8t0~m_9?<X;b?%=foaV;AiofOk`MKEG;UX*lTyNhI@}sZKyCfJ3us3kH)3hY;emcv+ijz_DlB#6DNbwvU@A(Cx`02L%pc)dhO|g72%ZyrPuF6rCK`p36)^wq|f*m87G;XC%M0R79Ntkbx^-v>jqgE*BZzHyS2dseFTB+fJxdzZ|BhHJ-WxT%VdF&^ig~vI}IE4{~vQ$Id+IqPV;)6`Cu}-v2D35I~TGc*s2r$4A+bu?6G6{ifhI{$u*yuXNY&6;u@e+dv&CqOyF#n@@o6kCtf<(M;V`K<DJdHKAPYv;l9s1G{Kzdq+Ct_44$F^)|-{hI8^-p&~hHyGDZpf2d{JN%veM9-uSdZSjm!1Y|`@>tYvuEInbXz^wQKz54YEZa_qB=!c1kPC9^=H9HbRQ@aP8>KKMXuE?NK|ds@`_<bz#G9$wgh^wXbYlr1EEkv3!JOUwDvuA^xG{z4CVWQ%D{&|V(d<qvyyS*?hrF2gW*a)%oYv}XSob!d`}IUpDxJd`|hPmfM|(<I3~lMT)HNj&>g`Rv|Mv3Zc?sfDI=Qqy^WrVbf+Zo75jG~FYzcU#0(4+mV}9zAc7?Rrc?yXDA$+8YSRO6d&5C}OHBj|f4?4j9vBTU>J<8WO{?M@B(-%|2Cae^=oXNycsIAZe0e3t)}_9|2nXe0;*6JNSHZd}6aDUi*C7!RMwlD!yRUlM|dbgof71i9?IWFOpm3svq(HDhDWVK$@6xPHlOlf>gU7Gr|RXFA6avOJn4LS$IWcypu>0jdHWCQT72j{1L~b|I(J{VNmSy{RK{|n=lXrewN*(7Fgox87U~VwhlWb;E9l;11V~^Tb2FYasnHpAiocSSp3CxzqhFb?lvuMuMr@8XQOHHnsx~&_)0pA1a|1bRr4PH);Dmsnna^*>|W;uw%hy*e%9@plQ!2}(Yf)FJ$)vv5W9ceX_2xGc$uv>qN?#EgiP5hg-={m@I8fjfVKxF{558;B3G5OwdtOm5eD%C;?-@vI3azfz$B4{x>7)U_PMDc*lRmp<xNs)fz26v>mccr3)Wx{tLYqd2+96Kq__G;ocbCt<w4ql4Xp{XGkBBmLm)dkDj}=i417+Aso`}Lf-P?dgzQTvs_C>(>r|{z!Lvf&gBFSHGxmuoW4kYR`f>6&DF-L`vP|LR<BE)KjgeR4L48HlRbf)W4|+N><XOAbWZ6)BJ>ai`vXfI%MHR}(Mp;b?_bi4eT>6lFMNLkP#fcAJD0@%$A&p^BC{uHHO4NNvzzb?4e-uQl3@cJ5PAOR7xZQF@T+ruM$uM9G6C#8?jrj3gvj%pDuV)li%>$m{z&tP9$=9f^Vih_$_n{+$K>32Bg8-u6Zma#gBsjUvsNV+3bOj!J%1f<op4f9;_<sqBojMX_=I@iw1Izi77W7_T6Dg&FDOOqN2sp6|y26#z;~0R;w~hexz`9w)b`%m=xOM~+$H!!8C`=UhM7#H2Oh;*wiz9p-`Qc(8>F{*2bZxW&a=r#rfM4P2g;)5N_WJ@gran&bMUK;BIJD1Nd<wQYr}_)+91fYI^7F~5YIKBivt2zz^%uCR<q&mGpVLs!iT<_@P<<zbJF`94cD#1>`^V~HBohp<3Q;>Yc?tWry=~IU2!Q7}3_$fq1UVxI{&G6Kr&=%i1a{_gg<a{_sM->uWe<m0(|vw=S~+|i785n;Q1&5hAe_ZS@_DjzV+eV<yQXrwEjeEveOl6Eg=a^d>OoknP|HI;_i(W;_XJF(+<<oU`AKX05LG2dBwgM1(Fq8aw1Q%3Tlb^ocIo>`xlvOl0Fi5J@5-FY`uZgdXAbio;Kxm?0{^1CfGuxUcnxR-fRDBTw%SCRC$%*ky(pQEWvRNx<x`j!!=r)j=6oScW+`EqRk^W<?at0(xQnc)Um~u9NzY^(e7%bI!88~31ej8%(uGeefo4YSz&B^dAk_}8j84vkl}?CyX$QbuP-&00L}*hkgrB%y7B$>ACPD6x=RPisNyS)Jw2WQaBUtuvQ<K@L$>*-3nA4U}+cI32CI&6^O0Fy4!z=I!bz8i|t)Y>e0bevmF<cuOX{TKt6x&zg+_6~N4&X8_zz3LTTjMgAJW63_(BZ>-Q3Y1$irevioSan0&_!Ylowb>;+Gn**QRkZ84YdTLeycCyT`J|uSm_AsfVX82?+9G7%zg<TWb$eI1uv1>X`x?PR>?9{U#y~aigmp>sjLh3#2Hz+*oKn|!|aJqfEGC8OU~Vs7_$hl{bDi*$+MO~i3?iYn6FNttI;8>^=y`KP_i!(2lJM=#7Q^?Yq;>h6UW8Yk}_jElQ5NwC(mlr5kn<W5YO^CwI)$O8cpt}vmhtqp{CE5;*>Rdr&e8>6ML&mn}Vycu;L1+zhtFs21V?xyY{11kXhxW(yVXlrsiPKyZ-&%n;TC&+)Zl%&qqHTlvhxyseQ2UA0DZ)4?BgotKT9W(LNyMTXe@76y2@aJ>|t@7#@SLq3+q)Yq!6{GSB4Z08Qu%%D9&pSu>woVduN_xo_$XB?vHHtxSzBSIR_nt27vn{45*~b-YV)-R2-zEuKY$^$$tRek*nVM>|urvON!9-@<%~qP5<jC7C(`t8TcvS<+@u+)j=%wMCtBA26nEzw89fvtoK&#&F~Mrg7tgoo!ZQc*itIZ7+*kH0G8xSck#=FdHXJ;u=Pa4o(TOIq8(EICr#XW`vWt61{~Wr|qyU#HaL%_!J$oSdHVLvoe{Q4n`mH=<MJvQ0qv*%aHvYL(DMbV4NW$?}jqoP>by$rt@ynRbV&Xe7yMUTAcEvo7ugOS2w?Z^g3>*_xHQ2%i+!M?=JrMaCv?0xvf^~v~h9%=jGM;wfEJ`=c~mi_QS~RTE|ZF)H!xZJezlZla(qeB?)olwB5Fp;>4%IBY6LHS)MGpT?-cuC_sc6msC0;NQb=}+Y`-Fe<M>J-R-HtNL<mxErwKNVKh%xL7w9R?)g4AYb|Opf9uKehu0V9?=J}n-x|LfuijsNczt<geER+T`VziC6$Uz5Zk!ReOM*n<aa`qLq(i!le~`RP(psfETF-NMtW={{|M>lezBXtuH(6$GGJ?Y7W&y7GhfLifb<OL`_m>wpbRgH7P6F6A)+!5zvnUz)k#a4wL|B04`St+4CVuX_`no)`ySrsBhdc$=!ftTjm4_y{i6qK$xunNGUEJRciP=HnnVW60JXm<<pO-gR?=H;!ZAiBahH_|lZ5f`XgTCSlA9&`)zb**vy8n1Xx-NC}VZLP^?N_ZL2qs?ptg%%HJopoTnTP9O$X#i6K}m0?;UtKYFe@4`%GMEZCQVrcME)j7v+g>2s;62p)x^n!fUQob7KuujqDdC!b(mBWWsDCI|3*jkyMJE3Hutvhj<*pQF8o<g;+o@+5wzx$#`x*O+u9(t*5f21ks)(ly?u3FYfXbKhB@g|nFKMb6<_}I6Vc=4YmyYQeP&nhAF-M2nc1aHb4<M-W|zA<rXW%wu`DjpT~_tEZa{q$>IhUuaXDCt)1s`3NP<f+SrnVy<8N{yk;Kz*X5lzfvcFu+9s;ebYafMH7y5mg+{MD<<oO6{)_WWCv9{hz#Cy?LBi$N8pCaKpo*$*<3g-8<k<FN`{B%NlG4}MfXl-EZd79dsu?|caH;B43TwWIbWhP{Yjd(gobDud`MIq4^FT6bhFAnZmGq!sRcM?vgvP2rk<DXPoGBpm=-qKsR_&S6b=TDhSimzpUqGNm<5+O{CSJ$uKkfdI^VN7OV);C|lI=R4r=71#j)L%vUkd+`cP1*Dc;KxCh?X={DRa*XuB}U<Rry;Ms((pW5&i$QMZMV|o2K>DUGlZcUe+Td!?R02WJ6!6<*MtYi^nJ~-L)r$RBc*znEa}V-s3){Rh%4k+fRl(raLtV)uhl^Ke7R|I;K`ODJwZEdg3??l95BdhP-zVgYph!M7Xfs|aKwza7G{ELG0FQTs4gFd6VjSFUqcnMHZd&hAgVQ+|1wpj($3alw(=uZzo?$+Me3E-P3u@e8#i;RQu-v>ec=}xn#fh@kz=GL1ihcg1b8xOrjjF5*!2o5;lm*|1<}6*8Ioh%$!f98EX9ycMzaiWgH5J1N;(FZ@p_{T+mxgw6)dRCAQdYJrVA=uN6J#L#d3iQ^=P=<px)ZDhn)Vvp#qNbBfAf6SIY_fsdg{fPZSKn;=6mD&;TkS#{(J~#)w1%fa6g}!&(SfeD#d+q!LOOZN49khk$B`&{Ps3)@Y$(5k=9W&OTd<7$;Avqqqq0rU~RWft53`NSD@DN~Drs#6WST+jo-G7_nxvB+d|@p*s%Y`g!nXB8(WoVocNN6DsvrvNfN<wx|wdlabUglD-K4m{0?oA|QgGj`FF;`>w$wB+B-y=*&c*Wmqc%6M&GPawVrUhpHGT52tc>OIx$mE5RAhgYhks9RzQNz;wy#8J6u8B_?c90^07=dz&x~QK3KKAW-=60ym^X%a6k;GCVLG?u2L<m&0IfMCQ_nF4KVosahF(o`pRs+bqLNO9V)ikW%F&nDLysOO)upEMo={sbi?F+r8|<>;=GHiw#Z!p^U!8pkB+Ng)uKsGsMw4R9r#p0b7=j%}~d<-tezx%qE%|+AR8*-N%Q6!3ESPL=6{5W)}dNaT04B4;im!7r>eXDX}i-d{~))O1}|kyzzYjVBjg!$$dlH`ALzRMYTlcY4|X_Pts`eU!)=>r9z~D)Ix@2jQE4{qR9Tv77QFZaw`-k649trVn3W%ThQ7AudgPP*z~c?#PL>E4d@z}#G14U+b$!mN_Yp~gO^n+{dGu&^Kc&KnN>7!md*rn8l}6DU_~?BR0eHNNBZ@G4u3{0Yj3XN_9jly0bS=FBIkp)GsoqgiUXu#`{hndZ5Xe;_94~vvWy2@V!#y-kYzN$GiuShQxi~0&_=`?swd8!)T-$^>bp$2Qen7?N4CDL4%RQd_CZ-dpUz(9FFUO+uuufUmL4G#O9)dK!)3sG>#)xXxck*Om;6HDzQma%T7BB&b5fId*H4eBOfrGaKfG4wHSGz6RhVyF4E36b1Zh9;2$N)(G{GJWfk9t6;fvJ-Kix>s2#w|%e~}`U=00uN*heNFM*+Ky5*Y6>617RNdyi43EU}j?f|*YWUF#|G;8IW0S(c<VFsY~yWBSmGd~Z+kM=u)Hibu#s=|$sO@fcyxG!Gd%UgSTEM$e-0flhGIpAp#mEb<SegHNAF)P><c@H!G7MqCni6aYe498pbDGDfty2Xf^eht}~k6?I1d@g9Xi$t8s<D3Jhd$2~fuA19p`92RwY<h13|07*mb7r5X>ST5iCGrK*_mK-8m%uxYA6DY(k{H>Dmk~_~U!V9C>_J4LH?Sunyn{8&m6P4ko7UT8X4u?A^Qinj}KKFYY!<E-68q0ZZ><u}$%#tQG(Q}B}rYY2p+&zCr6ew3Q_l}-MF_zsBW*d^JFky}uW<fN~gRExuEuDl+5{ca~s_AE?m%75XnJ6qoki0gDy5Ff)BLaPo0#TlfqF$O^IT=-tEQ!L&kYoTGb6p^o?D(WC8>&g9rL>@9uJM_D;d+Ve>MuO#?Cs~+sr!-;xw`bCgT9uYxF0RW!F+3sD=`l)aapN9Aj>PB3}dRI^;k>0e>8BUZnUqiFvzzM<`=l!DjpTZ#oWKa#oTr*^Ic3PVmRR-DBAjBiB8cJjE*&yIOd~q$jyce(m6tg$}wp@;bOHIawG$M-^CbcR(yf}Ac!r8^v$mCm?Kg>uxZ+LPDg9xFJ&g$H$Xw1f0caLR}ouGMixl;nCM6<X&BCZPKZ@Tn+nopb3igaNeDxV`<X)ns#d_6O2Aaf${-Gv3?4kNjW^}Y-DS$~8y7mDMH1OZ$%MFu21Ez81e@6^<-~4MvuLdW8FwtF_>Mu&5zxJg_Ao{pM4e?u1hfC1jelmG+~qT`G*BxFER*^dXSKuuNcLF87ASIoo>omjrt7uW{}JV9uj<nqr=GQ5Bbc6kwg$GVvh>!-R+J*q25>tB8Mt)6G{1<Hl$*UZiA0y=+^G<1>VA2)TK?ARR&rv#7B(s9sn2w`wo9FIy&gCw_H?-D5WS_YxVR5H-%9-fNi@G2Z&VoX1E?S&<6TH5Sw%uozB=M(slS{{(w$R2Nx=6Aia0ab7zF7LF|{OYHVnz&+{*aela|>~xlepTBe{fgHRZrY0t$ac;=!nvcz`5P1D2hX`^rLHI(IsGfsSrYUKnxm0(O`bd=FiE+z(WN*+G3&)76<v9DU~mdKjv5=sypI-+C}(l6ea7JFQyKabZL2+^Gn-A`87qrgO4-0euVfH<i<sh5z9NVHfb}J;!Bf#`z>N5E(L)?9iHIO*#^6)<V#;)+;DC9K;6WPUne*DnCr}B8t4ZfnCp@sHD{4wi(fLy5zTxg!{J|Y}_kxQk)Z<tDrNq6)kXzy~QkQ+$sG!tzH4^G%wbM?ohX)LZ|q)-ui~*625}x!9lQffdFeyww*;lZ(A^^jec4r5TJd5Ta?oOg>9s^so;Ky1zN^3^5cM4UrK_znjm0v1JnfmxGVVM4*bDiZKObBx!cm>jt{Pq>kZ%cYKQ_N%>gNbz0qh--H7T)Rcr7$!5)H=&HKxKw=*cArlYrBG*YYbx!&i`oa!?gmF@!!_M1nO>BDpB=i~WMOR<4tr4GJm250&t#L1D!3hX4gj}=9MPYUV)ofKy&oj0RkDB*03aI)=|o`g31OfOg$do&Nh<iG(edo&P1<^X5ZepOHRf2zT#n4n>7@!eKz4WUcSD<#&8E!E96ZaqdTDS7_nv-ee;16?TbvTLR1N<3MdvLb5B!Pe|u>fiq?@Vh|hX9krtG$|id%BhXr$O1B(FcES?>|UNs5|QGlup5$Ni_)&_IU6+?3}u{XY7d%d+r<waI+kHHB50H%CWPkV$%OkkZ6H?uYC7}84{SP>7EJ*|wb|0|0SJIbt`x}Bdt4uBfpdBV<G`1%NxGCgJV==b4_1I)ieN02?1(MuX;A9^FVXRf10Nr@oMAjXo&BRE4N9kFDWdto3~{)41(g9K*fAJ_WWeW^(%!d)wNsW>t|4qNj}FG7uYAI*)zKt)vj#UHP`k;{;3rxVT9JB=WEo6MCne&pz`LKcL)Ckzdb8Ea`n7n$?8c1L<~=LscqE#Dr1~u>5*{B0Mq$3?;z<a~Ck9wUP&=QBKU+nYnPQ#@yXOBcbn&x3#QQ)~i93{Nm<f5x#iJhdsUT6>0E>=pPUtLgu^*cp!J}UX8Wy-IMz9-v+cON-B#zi_+aIB&WysGtKI_89ZtN=J#Rz4)#|P|1iPzWBRuu(%N5MI=2fcYnZB@Y5_u9&pnAaC4$2_Di%_xCF^<rQ9MkRoZ)2Z3#ai-E66qCO6PKe(nb$66n3r@rQ@oQZ*#j;8^TU3Kr0%AAcECV;ofj2k;E%WB`pF`6wrR&awWX*m^<dLDtDkWm$<RpJaf;o5~l>$~9H8Yk$x(M;)lesf(2J*>qg@LQCKrS$(katnt-^xs?No9pnyETD?>J|2!=F6=+ZKu48b}ARxj=Fhv%y%EJ=;!q^7_TBfHR!8>pjpIw?z?$*%!|a&Yu~ElUeA#sSJW4m(HfjRx6^EH^2Ky<iOovs_N}#URB){v347m`Ikn4YOSlsYuDPH2d7fHa;+R8(JPon$lB-)8Li*4!P;hFqnv-NjQfA1`0n_1>9KK0I*qdkqD^71KUuqB-WgL~hAB>Z9l3D8Z)2{oCn6XtQEA3C+SFJPe=VZ(eYx}#%9T&)DH}e{5{^Kfs)lbAxqv~Owekjl0go8bj!gj#=Ni7_tpV#hF2X^Iom5kLF3-ghxlB`nN28Cl!<C^6pX%A96U3%)FNjIDOos(0ma=*Skf}>tgOXw7^h=d)pYudI;vY&X~qEGYSVG_>ZjH9z*J4#ed`u!ln*Oxksuy#>;(8o>qpquDk(9Ps>>yhhPeWi|}*MVH5YXHP+HI!@kS(HyL9pd33kL%-KH-{#_@kW&+({@yQ9kKTI{VUVqYvVv&;IoFIn{CL3sD7udk2Z3*TomcY&9d!sykg?(TRRosP@wI8A@L_Z?tjA=An$=&cFi5Z5l9=<xbwZQ5;9_TIb6gsN8%(jIlz*jb5%sk5O02R*i@-5mL7kzysqaPRYV5Bzlp6@$Tqv>#?v%>G{P$-pUM(efVxpqmiP}SnTJlpD6jZwy!ve~qQBx;kY2h}wJ%gG5z>B1cM&CisG7s%NroyVsjC=;b$ZN*JE{mibYg!7-t4vuKY8g{SE^CrU^lyuJKr5s+^2=bwPhZe-L0>Vxve!39=DV$T9G#23e}dzD0R4^L7@agUB;z#sWoGv3MRpWSk)Y2r)&vFd9g`J4dT3NCbBvxHwGk^h9WG0NF_!vxB`J#rl_w8mmSV>5nnePZE}e4EfM07Iiunc*91rz2s906v~m^tgT2fBd_`+8Y4;|pagdg;VM<W@!oNk{5ZC6U_vWmj@P&^lk$srr&bREYz<1|2(*XEzAq)w~`xHonfT@bdJKuo_CK1=M56u5V4OON>?sK#djx(?)hkdYsmlr~`f?}CKfwLuOEa6Q=sBW<_Rj9ZFRv&Z>g1g*sonVIpNL5U{yQJ00Ro>FWs^n2L?b}?s{E8<+pycepVF+0JfN?+)144zUR3t}sSiT5+_?4x|x5M>U^}g@7!><_q8=wxqkO{hkT1k6IzlJEG^8NI%e0={2WfKAe_fAS`DIsNc)wCoE2nDkQ>;fc0b0ZKK;6FmJIY?s3SP5VmSDrNnsCWgK3h(`N(L}o6IQ5BjC(U&jMWoZBUzno_KU<8@k8GTVOSaOwm8Xb7gd)bwF56J>5ciSkYHsNN7jxi9war(ip1Ghs`zaC2J42fha+`wSB?W}0AiXw-5piqcQCLo^%}6I8#hX}%XxvbIrzrDjvYzZv^{@JAVU8y|B!fEI7(#L|F_I~V_^Bt1<sgG%4~I?hbOFB~;KzI;6yjQekKX?mX$88SO#Q=Wyxmh_gB6=n`l_=Htdp?O<ROvZ`ggN1=1LXE^U4E|ZMto>%kyeFmH8$`whk#2hL*Xd_&StC9hSPrr&m`784U}FY?BUk#Cu|@iqK`DXo7hQ`K`wyg=12e;WCuE_btH|$`g3M^|WYg(CW=*GftXH)-ZlHq+X@7HS9pD)RQ$iytLYY<1DpU?C~|BWxl=qh<uEH4X-ZGU;oQ=gw0E4P)yUqASA7Fs|8Ygb@}$)2jl#&o8LcPz5Acb*T&7e%PabIB}p*<X!i^`ION^y2m)qfj9`xONn-eUyYpP`r-%~MA;Cvly+3o5omC`|(TY*7ysqV1bQYF0r*@vMa#<zk(aNjngEl`lsoNChkS^edIvZHU@YB`DH}BqGdIemBR6%#Md=HOXp1*(p@o&y;kVo^H>$cgo+NVyR{vUOm)8m0Hf$~xCAeB_wS2f>ckn49J-qvQr=cZ^wO%^U{zW490ZzS{<Zxv_OP9HRG!e2|`s6T+-$^AZ(tiF0j!t%+^lAqAT<zX5k=HD^Dek;bfzB&K!`uys(*RP~}Rr0*b<gOy6t4!spC2$Qu$5mXHAsE$C>~|H<%*vo}M284<*QjE<#V88z$jaT{v<&*l_|;_6@2qWPIXFht-Nr4y&}eKoDB_pZNc>Qv%8X-3ZvVrpAWOVUB)M=g93oCbgwwjd&VCgMgMNGPD6Aj|2m39qPEdGJPGU}n{*-0K4MthUB^64vx3VVV0ys?oxNenEs>?0hRpngFyOn{v)h(8yI>M?|YQOs18GhSoeUIew?N8t%G(up5)(cgZ<+S4JAxGC#P)}M6|4oDN3mb{UA{T*<`0D`Ci9s}+cBbR;>1n%t5<Gw2e$jqDX>~^9cHo~qZ@oA<f~%`gp{v<W{6`;FqQ>-3k6R=XS_4@f8Gz7yx@IEoHPXz68WQ@Zg;0@agnD)Wn%%G8zLhdno#PM+nZ-YqKm}^I*iSzUi#9vkrgNUEWopy<m9oLNvM2Vx=oc5Q<G~&}`L>-T%wWFs3bNH?S9!jcp)6K83Z}5GP%8NXPp+|HR1yXC4T87DrtE>MaXNgw?BaWZPdSc6FGWrAomo_~9}ob0a~;+1hN1JG`bFy5psd_O^!;7Z8T93qCN^2h-lTPYc>UBtznx)NQuXk`BZ}@lR=at!b{V9|ZXvk5cB`ePV57L6XH~7L`N`pX9^Wcw!=Ok>+Mi!#xp+cH{cqcipC9+p3@2A7q)Mu|&Zp#WoG=NE-ZRf<|1=xZWW36BP#))GiwctuIgRb>V&7HEqT)L(Oc#*@ez>p_XPFS^CobY8Se>Wuy~NcI8V!RL9$2$@?q=D{Mp_CIer|_%D>5X_=Kqk)`IpJ%+{dyj;gty@GVg=bfvu@b>pudry{zVugY0YD!2=_BT-JOO;t>ZVYj;p^blP%`+!KBV3r{OqRO--IJb`t@=5x*L;1IMSZkO2-FwaSOHJ$4EboP&SNlM3_T!VS$CzZG_Z<Fa14A}FtjmOK-W&E<BXTE-S{fAkU(F#5M=#}`b8&P8)i8u_S-J>u2prPU#JQv){<Qkqz*2mfSl~OXP=E;zAr9H0GxlG*MqhAF$oYX?PJ{=`Ege0nkBbTs<4(&*RHqO9r;+Fe}3^DZr=^n79rUtokW|7z(ikq`Bdn}Q%=##-oMn>hVmQ!iD{0P!9|CNWf2Bkif^5xIe-!KUMS)61@ughY8naxSZsb=ghx_v8j^u-rUYy7E;RF{k*I{qt{II4JyleaEz_BGhK$JsxM<ZG4JZIz_0AG}=D_j9`d!9h})%(Mrkh$scgw??A=kk+trk%1w-y?88}<FCk&97?(thlSLoj_vg8xn^a;mujq&z6QI&EOH%{<v7qQfE2@vHxKJ^)Ey*-ePk(>^unLGx7F|M19WGHPKMw|hf&L~vhzgpn7ocWqJC^@RxVLr7fUHGS%DdZw(~1Qe1&SL%JSw>?v^T}?~t$Om7iIIu9Gu-9VOuVAmRS`<`4~x@f;UlRcLC5nY#YujdLuf26(C@DXO{|TvgqIikGHF2+C5?!)!sx@yX)IslZkzJC_4YEWLS5?F>LSc|>X~bla&Td!b`Ww?Qk`wwpr9KP&6n%MOHofWcey6P)3BYTiPj+{>1p_ZaPO<52up*v%$Sd{`0<Z~LJTv~ZrpfI}b$X;y{~e9whenXfvI+O+a@#T^IRVa>gUXh|Po45p~Am6dZ$^sq8Kn{RNeO@Rcm@|7P=`Pi87dBwwW#mosp&D+j5zOK?}<ZTmw9j=Jfc5HXxS@t{m;Mr5CsrLESfPLp}`!M#n@b<Vbs;&!~MT{IY>{f}s6!G1kJWHN@eZX>0@PM!UN7O0XVBXi;!nC^`lz+y=deUYeXu#!&{CBvMY%x6vb4$@I_V_*(#MSqTxTre+pcsd5fZ3gv?HPsx9jkD&vr=Q_G25GrIHCxIDSiFclPfg-2qIS(Yl^8V-ee)3f%lZFSpuzP2umyDEOYl8$W-yTCJBi~N-Z_uQF`A=!{!7Wu_K^%){F{R3a}l5G^R3Ag!xv)(~bU189M5%I1c;WsgpkjVfU6Q-|2r9fA;X;_17*!)fp1IXsKTo+iY}$)pDm+Ax<mI2ObadOu|VX9^_Ft`fVR}n$?Dt3GIW`QgzsDqyzol+hK*oguNSuUTUhQn%Yq#HPy)Wv$oql;fI5_AL-e?d$B4;KV}oERLS}}^5KV00PS-rIh*ZsBj5V#r`jqhOn#<WxdI~*A4MuVUU7;7M5Qj4<1}-!3(H6|P%1|NF>_XQ4#)@{6@f$p{w^U2{B_|;RGuLc)u^~?wqG1WopHbTu0?|`WYF9%b}X7!yCY98^UJ+$P7X14o*}@$32{L}RK46F|9`dQ2|XQkCB;uaT|u3s=eCK)t2YnC2JTgHQv{!)V+Bc-a`gs+{<N!m?W<DV?-#P%QsF7uR$hRp=~pf3a_^z-BAM{vT|>8$h4M6jW8$g0H&=8bVGCS-A{~){-u4rARE3R61G0t3fw+;RC|Hy6CK(0l-K~39eQk3HSxv<9bv-K{ymi0guZ{Zrg37|j-7Jo84!ATVkr6P{5f92YD*BS7Yi;mHL-CwvB*{)R9ADS+UrVKpPVUtUxU}MC@kc_{kbJ58Fb?=$oH>>6iuo;5x1lgkh%`9Ow%qvc&I>8(X*X)?Op@U$20`if3zVXPyHY)l(1}nkl4#&<AXKKA=e4@^CtdWjar8|mN8K-~@v)MdxY##B{p~rXDXmHT__Yrp9nrque&0D!Tp{4v8(r$Y$2j+-yil~LNa<RdDUjh*6!Q4jbDs#{0~LJa=YRjy@2%iZi#*y^hpKX`@A)!0{ThywIA?(%qftM3a2S8k4yntf>r(PS&4D(GYBK3DbF255b;W2Y2xgy&v!CCUqi2q2E@8HRvzM2%*nydUqkp$uoU%_lc&~FG?=eiw-s3Lw^7X=fE_13?8&o~@`XZ2uOBQ}eq!xw!GuLFu+po#FQp!E;ooU?pS~L7w=(KW_n_cz6F}I?~IJ%HOIA(yPRWhZDF1rUm|3P(rCbSlSqa(~z0L(Ic2-IH@Mg$B30-GFwR|cJNG=)}Kx@BZULq}Wa5D5;67+!q*^V9pwo6AQ-BpUx0U$#6<', 'offset': (-1.025, 0.2, 0.872), 'seat': 'WholeRaisedSlipRollerBenchTop'}, {'label': 'BeadFormer', 'sha256': '8e37de02728e8d81c767a62540c57787571ba83c41949962844b54a013c747e2', 'encoded': 'c-p;vdvnvuvhV-?6gq3yDM@53Z07;kXw?lNu&B)fD#_Z9<Lgq%w&Dn6$&q9yhT^;5{&mkt@*@H2?t7^sk>=Uc-P6;rQGWaFw~u)|i_<W%CfR(EL}g?ZWmv`&E6LJXyS&M>u(ZZeIBj2N`8>+4=)R2dILilCnpulHn?ywsr!y<dt!xqH)Hh45NfO3$@3-H6YsK?LmY3E%EN|53B1_dxSllG>SQYC+mGL}MlPpQ13Az<3rm@Q`ON!QYp3SWV^`f?x9^@0fwl1$uFRpy_^zg%R2Os~s@=@gk!F8NOLEw6MRAkADD!oORM`_tQy}UfX^6faCE{igc!=!y3-$&DSW0mbNowgTYoKrC`I48jLs@t8eJ^07@#pSz?AAGy(b-a!}xO#W>{@l0UU?A%~4P;#jx@aJR6$4qXXdvr?2D0ApKz8f(`Q_QgyH8g<(#JHi(&#Q(Tj8?2$<X8OCQBlVp|cjzG$L{&?RmCLODdR$>5^zwfk%)P<(k?Xs(99^RU}b5B}!p!77ZGI%~Bc!<Vg)h7fA?G$7NxK<7^dKp>@3^D3=T3hnupRnb$I=E>mlA6V9(AfOs9JL?~+<7LjLN-DNfJ5Vk{tD&e`~ayezzDsIASnkZkU7N%d$ZmjEUnOjAK_S7v8<ATPeW#wR{agt5G6g>4L%=5KX(i}uZ!YGXeP9VMmsR<OqD!Kp})T5*cA{5?*`INd$i@uem)dUk7gvJ2+cyz9cz`>}D^U0D|NHY=CvpgfjDC;gRZ>Y5u69rPRDb+>uMY%RRWf~WR&b2iQ7eIebtB@sIlRQkn=m7-3+4Xf1l{9v|U<g7iWjQ6h)84Vd>1SfkIZa~~lRUc9#4XBbE~8BHtSGD->Pf{F*0E+`n|V07iBqD=hfGkBCDV$g;QMs8Ob9$8LliLwS&VVLw`mVgqiA6f;S=jToh5N`)4scjh@fZIbso;6K6Q-&K_To_5qz4*D`GEMx8cS@S;ZV<$+n^)h!ZVra7-%eXLK>51{RvmqHG?OMD(qFfz~MqCc+?^dKPw%rolX$5)fabJR{6SX;c6OM1_cuO{*$O;wY;iEGIE~QeB>vEUOgF2#gQ}#XKfih9cl61Ov^&Sp<40q7$*nGAD*GJg0@9vQi=@h(Y6x<0LNEs!2&2c@-s!Sa}gnxRN9gjZ6X&(3>7{iv5;on0Uj}B#O8EbvP+`>L{OOX*Q21G%F23q>geee2efpBA&!7G9>k!MyOd)n`>V7MLe7FpkW%%MN$K;;OsnP5lkp9xua*d-umCZ58l7~@b^o9I2xRN{BU)8cE!(cPe1YRS069V`QgnuNmu&)?!)D~*XP02`6V}OeL8)Aesy*34;}l@CDH6vvW(sm>!okNOtx~o?xFH}&*=ZL>blB%cA~uQiK`s@HEowSf@#Rl%aXVd9S&b8?}$1bb-2SZUVG^9HV+p!B$r;1SUOFoZ)uC6edqXCd7WqYaUyd(r|CM+(dD0EK7S=b=ZxkE^8!6E`eB#gIO66f1kz#89kr&>HPLnIglg>e^N1)y@@z?4(78WYgDb3iwI*a*U*iQga=A;f9PjJWex%EMnb2FY-Q`IkUC<$vmeZ`<7`#}{sof((vjk~&al&DD^kh8jjoKmopr`Ig>8B3LI#R3jQx|1jsg)s9qLLF<AmFI?irc(&1h`Poyre^;*^JlNeX4s)n`lmLQeq9YQrC(`QY51yx8Jf>{!p+$;xe5&*9o0s&b_N%xD`qk{J6m5YBabu9d5b!7RA>i8YoMa^T-FH0N-kOOA8q(!3*AEdgI>*-O<Q(pPpECe}0VdNaA7^IbB6(EzQvG(gLjbT95v+)32t_Bies-zEG<sAOj6YTYk5!XgZ4uzo86yXME`A4pVCj1}ZYNy;ZlvZhv%eJM4D}-a$yG86A-%OPtjAyS&4B@S!s%VvJCRA$VAYb4{u}+B@^Yaj7f>Kzba3@Aq!he!)X^Uiw6rmsq#n-L6P-nvY2z7or~!b!vK84Js*3VIG*!_I8N(kw1+mL=T!XCb8-h1BCd^Y!E?Z^9?`v%oNNp*t$h9kBS>7$+ATOR!MyT$FJbg!HS8^?`lZzyQC3frY@~rYMg2WkoHM>5N}hS8WS_2@Jn5|(TgD2?bQG5JH%M-f2V_MFQh}Cc-i@a2^4;QR?e3Lp0Iw3!CHFL5K>zDA8(g1pCrTri!51VzDe#U;e0#|!5?bUcd9MyK5-^y>$+{H+QwXN+7Jg%3!e`C(y7<OV-s6t%MubDOb&F`(g1Tj!B|^-iH-_Cm^=A_8I(2$P2*|gJ2dOv4e4?gCZh`X_d|oZ&oWq)5}!a%<Z4vXG!vg*hM(IctnlD`22#xsBeaPj>==q+I1)g{`uAkyzVwNsyS@G-!#TT*bdNAyJK$u~bE$i*^zSbt_jkX|T^YosS`mmt*-Ny)CiHWHUFKG-K>%UoFMPC8TPDrO-I$q>TX6%|6T*R{MYeE0yMr-lBVVXploU~)by@3_cPGh-^E}UT$NrF!@)biNw1_EgjD~CzdK-facLPQ4K(iFp3NPK4`EnWsYuTL(weF~OcS8pMJn7X!h+a{Aq1nppxCNM6HtGU9bm-7&rM@!OaB2;C_K_T8Us-OjNY{Igam2h~c7WTz_MmpsB8M7<M2Uk`jp=`Qkh);+pWBYHimA_M{0Ec|oJq0+$JxEqC7HU3w@<9bqOgWxlHnk|iRtI4S}7HFxv(pR_qwpdg>*KJHenb#9o18Z&`q2pb*!E#=u4yx(en{K_0$QK9dg+bJwrL_Qu}A>*c~<CXYrX$WmsS=uPRmQcY9dFozJH>R2ZBcV47>6#)a;M-7+qmJ6eqU(tE+o$zXKc!BYCkp?asN7xi7Od{eL_yt1J5heN1T3x%Ih36?5<!pF!YE95*W!{w9sDal)f`qj!bDB^UhfgG?K1Rj|q2-^;rBpUiVhsNMR8Vi-#S~mMaC>`F%#s9y};gp~dqnzgTef!>Kbc1ZAEV~r8A=sJ|{>rYID9~6rq24u<U)(jHdC$<^d2H7JopQ#9iPY!WU9rn~TXY)IUOL#v8J~&pYJISeC%8&>-{&2k;GL;*E++s+kMRKO&1<q*r%@j0{eIt3_gxvI2L6NJJ5n>&Q2jR{5eO?;kg-g99)q=rpY{&S(}zKx`}xz&HK81ImQi?9S$Vx#AW;tT1|oR$gT_AiKx?jA03Ul=Z10l~ZY_CuVI$H{e{rL1AnB{LnW(QF^|iZ=qW$!R9`XQ*X-&{x9-#7vJyg~!VyVk8j2@#fJXyZ|Pq<LdjF;<^_JF~hv<D&q(2nG9+dJu~ws!~{((5)JPw?2&k6zEzdxwzA+^c#t_58@aMkH0)Mzz1%B;W-c?R(Q6x7r0)`R5oUxMIU}0$-nY251k1IAU#A8|Y{}YAv#&)T{kVTtjB9_5kM@>H*l{GXhL3=c8i=wfmf`;x1Xyv?`atW&dU6hBAI8xLM$&8%JqGR1!x~)A@K4g;RowT?>``;8`mK!zIw^DOm3$gWMK~S;W%_6dty_syiYc`Wt(I8g8v?q7qvC>wgrto?7t2z_o&|@P}1+;}W(oJd(A<6B;8G*>kG14+xPCniBJD>PG;QJqyQzn%>s);Rz8GJ)eN4gvVZ|em&sVj-hd51wcT%%-RzeM=4PsP;8@$0jN-Q)EF2H)B(cw^<WG$a$huibe{``^BM_oX8%z+jz7{E;@K9j%|PpxKF|JwxS`X<!grs$!r{G><LwvT2GXeUc-$2PRxhIl+8IEl=LTmo%3mDs@ZpC4d&lXmxCr~C%-Bn8yv5or$(xBCpzQcW!?QNey+a2LQH9p$%(H}olZt0Qi}G5VFhlGeVBn~CJc1x(k7)z%pR`By66L~xWC1`?<CY>Zply8i{f?Xu#EFN55bVsaz~wV~s9wF!Ax&pkZPzbvaioR4us7MV5X4kSfs0rfCu^1_YZ6TztrL7v_giaYnL)x(R%ZP9dU3oU?QMGn55HO5fgQ->7nkLa?xvjkHghN~g@n*oexc>vA81ae?f3OS3ahQO8A)g-@s~)#3AB~sDV(2r)wD*qx(#cvIAH$Rp|Sx-sErdCJWi<H-Dak#Pzp^A8Nd%Dug-6mVbUg!iP_mIPJ7LGeIm{sv27KQFaZdO4b&@}de&=V%rPT9Syy3{sn;@m(XY3tcZ_|~WgjU^Eb|D#-tF@9$zkL9q-t{VTsMaW0@HJ6)Wdqz!^Wt`&+Ae3^GVf2MrDs`Q>|f4?LGg$JVnQ^dryC^bGO_u7+Z8a*6%db52-X@am}I^8ujl%2soeNdA6H-O}ArOAh!1xXj8Qm4TJX#G>mH3NziI5z(ka*!dOCiAvo{3J(KEDG&dl0!yzGwAL$Ss;#)dC$njY?`HAJ>Y6vGB2{FM7qZn*5FoSNmSG1f4|4!IPUg0Xtc}t7uypmK6MOoS_EuM~^o6&Ge9g#(<*Ci`xhRtL|MVjIke0oF!A&tBVVwo)}&4$o)T18<lNfQz6hMFLX&}Fd#IsA-|pA*({aO@m4<;iYbjs~)bO1TbZNdvv{ckqeH9*}<Bplbukhm4jEAbH;7Mf}aW$`)2J&oaaftErp8Ksa2>o0!DfMnurT(Iug)A|`8@Lp-k6LZ1ilLN&IWF7yP%Jcq#TJg-jUX34V-&XZo_Jkd}}xOxLtg3^Qm<w)HQsoAP~vW+hW;$Z>`zG?su8DC%0Y^+yTw?6}3{$RAo`p}A2)2n))uwXjwHQ!k;>xn+W@mg6J2M5_WZ?eLSBTOVUw-&)O@k%zqJrPBVW1Wpn^pQitXDAg&xdET^=2T~$!L5o8kCgY~h@m~HNl^z<tuUt(od^Ta8_{`@GQ4^A!7cMXpow&BF?<-Lo>%}_4Uo`S3@?L2Z@d)L0_<lm8en6X?#41mYp4t!VQVa=t%K#VCLW3nok_W5#@^X&+(cGU!FnjOh!r7mOO7*$%8zB%>aDFZ&V~u*z8q@I>ZGx{Y8vMfmhm03K1g?W5&0nti`sh6da4ZbSya+d##+LN&bBI$F<h{=G{aH!)?0<iGAf)pG%_37rm0P4_vIh&-dy?Or)@iP*zd!5R0mRYQ<n_-`v<Drr@h)|GbG6}au1x25`}aNjQ+;-zIMhj5D$Ua(jj4XKJD+YC<}3bqY1sBjC+j)hLBr<8hv^m+6L_e0mj=Z)1ymdGzt-f56Jq7CxOWosG>$nOsRy>{vk`*{i4HI#7I>u*Z1-ImX0)H@Rgy^B8yXj)im6tmb4jFLAG(BY1FF;fiYe8WiM(!tENXxfg5jAjT;~A&{>b+AJHJ&#H^x0%*c7Pile)rn2=fH+l-fL$G4&9(AyFT3?^#_ekDn+A<N1nj_Ax7X!xQyL=!qw;G}C$vw0|5RCaAEj2Q5U?4PVqs>DVJc(?#&Mj)zn0A(bQ1e0JD7o-3On8v@N+1=Kgk7s{fic8she(VlDUR?e0(eHWPlfggVU7QD3f4n>U`-k((OW*5|+TA)k{qy|d^wR%kmp9A#I1S^(?mLIxiE5vyL$B*9`!;Oz*-Yi69UQBkcO<1y@~IFOW6wL5GCHBTT}SDHaY&X4N{;JBceMM(1l*cxmWOMZ?C^GP9Y*7-HtI}O5hrA8MP-RN((`R-k9S*aLH>OpXb3LPPT!vsGQPJ+Yk2kk{KM<>3+vM#r<dn&UF)>D@nWsUpqnJsL3du3aZ;GHx_^*l%kr&CZ@ju8jxgyq)~kQ~aYe5!8q6cL*~`YCshd|s2v-Np-Xb6E%k%f=XICVgx0+5Pu%xprqF|O}<1o=KQWgnwus3_b(Q6u(p=ZLrh1=gP^YUm;T9`9;Tb%FXqY2bp(m6aX8SqaJafpC+JM`efE7qb4{ds<M@$Sst--ei;IGClo-<9EMI_R{X<lOl7*}u;S@23A`Jt2wX6(M$A;S<5ODxzrWcb~O33W0}k8ZOFs6$RWCrZS^su+wlFrCD554H#vs1UQqXECP~nO)5%%l|0r{ub67mY)Zg3C)A5XB_s%2sar7VCZf!d9YtgK_M3PAI)82NZQ&nnA~2ql_E+PY^EDwG!qT@teR#Vy$X098{<B=qdGYqu=~inRY#y+xCP|-q#pnO}MErREnnZ?>&+Z%g(LNKJ*?l6KvJE}#K6h2NAW|c-F0RpCR}HytM13^s2vkOKJy?y?s;r4ff=e)272Exz@8Vd`((8EU;5^f^zh2B925qcsABQ#<`eUBl#lpkv`2cEGdmHn)w%W_Yd(pVXx?2c+jD@%H{2(tkFu$*j5M#Cs^C{6{;v2FUbztKAhTGJ{1lT7n;_d=LIILIVB4A|2nXq)A!W~UW(AhLZ;<>*^;HA+WE3NKe?oH$CYgr<V<MU4{tv5A}*1^J`dw2~X#`&r6NJn+-Ph^8m;syK;uP$G|AxXXP;&ibri=mBZhjoSl?GZ`r>u{Nr0c$~en!4!)z)z#1*lEcNYqb0mOHAU)PD5UMqv2_?xCwV!b-hNDt45xt_0I?ahn)_cW`}dr_)^D2_B98Ej2S^kO7k#T(9sW<4b(x1E99hOC(#apMTjG>(}J;86HN|0AsI}`jlcp-4ly_2Khjy@inUcE_p2PRY9!i+UmQ#VcU4vnZ7^IJ#8c9kIkjCEvnCN##tPNi?SI?4Qfp`p9gOOkRis{P+_Z!xG;zD39yYSbwf-my<A77BccN3`jY5Q?3Ic5;ls7EW%@lQZYjJo;!zBAJ05OoEN?_p<fj3>w7lorYqAEy13BE+@LhF<y{&~X<#%nh7NIj~yp0<B<t{XO6)YxsLBt;urE%Kli1&cN6oee`s4M&O!IEG}8xb1Q=g&*7<Wc!(cA(;P=&>0P&FE02%L(3YINC0p=3Takz0gK(37*8spY!T(dWD)?X0I8KEI-K!b=hBISMV&*o6ERMiHAkUgBfu{Xepbq`HTtx+S`yX!L@X0^y%`3e#>kbLWod!@0@E>oTkzhWi4bA{t1)dgBvhJLGBTgQxM&XKl6BOwvY`n5lu#2OcuNdH9p!1jbT{A;5{3LayD$@I8P>+Y1R&(5__4Ic(A@s@p;S}1HZnVd8l1^ZH2K182Z384d751nNl>@foS3mG326I|(>7xsqQY>>NsLG#i@cZ)D>BZmk=&2rI4Vm0IE~XqW+{#6F&{{hrBlSSlyp$u9t|?f@X`|A@ETI8oJKRAv-F4)!<Ti=8;4kR*UesTW$yxDzr&lIK&Z1vF{s~Bv@jjSoFWfYQE>yU2W(nCG{ZK=4Z*+JDO+fIXuIlT_a7b(mKIQ>5f#i2?LGjq(=0VO4j8X?AHdoKDQ#WwdC-`EO1~3mO!%PyF!Hs@<h>zse$wpbP%W`}9^VIdS)NS)7pX>Btq5r#jgTQ3Bc7nLDsq27f{~)5w!v{C5v^@b9L7^;16p_F5A|e{TRoAPIA6%w0(uKf+M2Wq*R35DHN2xA!OJR@c@4;B4sPPIaH<Asp{9`2DBaCus+u9*7<GM<sWymu{ES@8!Hv#4o2sY>zAk-aen(w(LzuC29vc<AFL!c6<8<YBpHkhRD0sjH23+z0ML`2Rp%#N%Jpq+OU1V&bda7=vR!`T{?=t05r;+MCvhlV&SiSVS2Xz5GJ$qTc>~;FULY2%}dxB6bDL9hrz_eBDta3R~;*{yn@wOUg5<vR2E^kOZVyd4UQCT{La(?>ZwYeq~t|6@Aa_wQL*Tf|8gs+d?gt#n+?ZFUOA-j;Yk15R85}lyYJnJt~pz;!qqzS17g@iM`Rt=2*5R1Ab*!_n%Q<gZ$=Fu!9MXvK0dvK{Q*D)5PH888_hY39llF;9Cd0~)@w~EKOO)*F&Tg4Nk?b1AC;P^@SBpE+RCI{w%hIvL}>XRfqkPaa|kEsj8f8h5d!b!U%?P&mnu{a}`q-2V0X&>y$J)Sy8PjuE80mL+lqk5NAdLa7_ov!i@pV5!w-U~!NdMAg9-cGvwcGP{Lyxt+wN|9P4+wJjf$tj-I91Q>rgF@`W(JEIqO7*-UyfB*U{&!EVO>iP<yUQE!m|4DBj6duu&iB!*4uQsf?)El@C$CdAmh;@&n=<X#HBTC*&k$!{w}snru`iqv2THW+PMK-+#&TP-*#a^Vro1D9B1*1H(sMV>y@kri6w%pB%_~y1d%Cf03sG2zA@!ZNy|sEopzlE->XT8_OS>;8qwY~;Njwcm2Cxy=2V%*7&+4*3Pa-X)1s!v(&+G&@OJpB^<vM3KKim}AUCoGGUAxc0UkhK{j*i~JlOzhsw40Do7^ixr;fO4*bQ+Kak<)sdg*!YPDXAOptE&w04TOaiE;owDRdF@<?_Q_V=_<#5my&51Pc2@lt*Rxeswp-))>z}1kH&zT1#{9lVuniDw4QjroCkc%F3!l9F=L=v^#c7t5L*u!+Wk=3V^TdpG~FG+=OkRnOhh+8@tvc_xS9D%CqEU@jDwV-BheBwWRH+}lO#nI3(!fXY!0X@O91L#p=dzeN;2up{FY{pNMZ=lJ-dgg=`6|@Im2(A8T(G|$&Rxr?HU>o9oV337t0*8;zlQ}H7fPJaSk%bIRd`tBn8-$Yq@rsz}&xMqn|fU>G7FY8;}hJmRbF)S}t$^l0DY21**F&kE<qN)78o!{*3aoSM?c8a^G34kPJ>gJ0sWAx6D?!Z6`&d4InH88MyGiw!ey$l$hR%M50G>?nD?h_r5+^E`IOy8+SUsRW>R3X~=xHa%-J(wHhfKG!5oG;<wxr*Y?xi_ga6zC6K>aZ-m~_J?Dxn7Mf+UWg;9E>LY%Jo0f8EOhHJJvNX|oWSTh(Aq<kt157O!4qKMoK-{>oxaV47OW)n$6B?Hz_^zQG*tkH!uSlF9Zzay-lA{I7PRc`Vp)S;|Nxr9}o0IRyoO}-olY;M~%YgfVD=<5_k81kn<_+hcs>lpORf_)eQ21>Iv!;cw0lzh>1sxYIw9cK1h%1WNpBCm$(IBF?$h_%0Nk#l$eiZispP@OTqy^uHkb%gMnHEo-Y0;)5!DTH3J-2#AHNnAbFz(Dfr&!-_lDz)v-q*<8&i-#)2}7KjCaFq(?@2mhr^Uv-7AMs?!MRxG7P01qB*QfT-lEp6*01ws?AKgVVr}RabxSH#)!S<04VNQqPF3QIx5Tj90s+>Zkex-qU{f$?LO(7N2+*OxElTPCg>9tCRPBC<1zN@;3DbyIUrU19EkVHM2Dl0P<F?u#x7Z*2>f#D7mb)n}Zu#J<cfA#c{uZKuNP9$z;9xx7Q#YnMQq@{~POyid-sZ!_u-_ZiP}9-7T{PCK3b{VyXTGX39@p*z4EDQElbOSF5tfsiz(}!?a&m<iv%#4^32|~HvI0BJ?o!QB*e4ZtfKRHkl+K%R6iA*4Bb;ozg)cb`ztRiV#U9N=Fga3yWse3T$Q<E}+OO)F{*N^nR}-|XjeTb*E?ELfn^#(_S0pvf4Q_o#D=B&5^t1m>oCAF*@j|uQb0wZEzH%XI%fZI%ed<5_Ebx0k=w}9%G&Ct6H_EAv+bSY5n=lcsD!79(n`R=#QQ@}ajwnj|LUT51Fc`}CqNF=&qir8Qc<5AyF^Hg1s$>wFizk!ak8c6|mFjy7_{<9Xfo;`j(H1atn+^RQfB<OR^#Pmu59=cx?3_Whap1@|EL}?;9;Cj<jjaH^6v;^XvK~k@FraMvzeLBc4tzXpIKy~&I{U|29@S3ET14|l9mL_{S6l{+fMPHN$$&2%t-WswYgLyvVh}DikI9yzS3cqO>Sz*+6gz}Jpmvj?fkfsiMSp^|O>LDEb2s4K&)Tu>9q8U{wX%LKUNE;cBei+Yia8OfC3)hcNcemhSe5x!iYFneugJ58pedh=KU*h&*<zl^b}j!?=mLtc_kpGwcPKG16Y{i+2bJ@2(m<lL0Tz{MPUx(0u^*dAe+=|s>!89-HG<pXZ<GYlio_AyZTnNRj12iT$LF@Naa+5Jcr`-Z?%@FkN#+ktnpH!=-cfK4-O=DCrnWj$>ql)R9_A0l$#D}?mv)jtp?a~eeXEf<#@B(_=kZMEW9d!$(m$sCE>};-xijZ$gg+n7)l)2*Y_q{NxaFRD<$4i$MG3sY5$M=g=l=?9x0bFu6OuLiL4WjXx<sNmmWLb-3$c<VTW!?LT15FgE@>;;JJS|mpAsPqgu3JlPL>oh6?NQJX3|X>E0o%e2_#3avggdc+=ykXItHy8for8B&dPrG@q&I{E}{uv!=hK~Jy{hA74C~TEBg$$MmFD?<6hp-aZ%S-L1+Wco~SgNn;ej?g4e8+Zbqw3qhj-J*WPcVoVfL8H@FiEuA8t3%QAPkMA-pSodVEZ?wU4+kUlgF6r8PD?P<0oDHE`Bz*hX(AdaLV<4rUH5+Edg>Msolj53bCejZJ-d|Eg<`sr@_jd)}0N><t*i&w1*|JP*9Piy<T$emQkWjFH*YW~A2e$!9H>7x3>G{aav+Y*oVND5bB>t|bOAj5Jio;q?Hp9d*eeQ_`!sVdnrCo*Up`v%u6CrNvd+Utd{Kgj15H(~Gi#A(FWH%CzVo>4}pfI}>-?7r=~9?5>%^A0`TMEBEp24@_d4V!7AdeR>!557J(>4RH=(t{x);iG<LdO<gn;MN1-S`$*o(5pxS=>`DtS_Kk@pC#qBV^TYOTx0q8*VR*-KPg6)W7}1_y~$L2`~H=!IBXp006uFNrrDZoh~_(yK3Pj_xhgUr;3_uDaosUAQ9GUAP@(N^E_o**;=geUkoUkXRP)Ag1QLN-x1s+{@<r@E=ZYwMEKWk36DtWiPiL|O_%<S^OV#RP?eVwka6Ly<kr@F0CP=N3ZTD-!(=>cE!Yd_DbqOm#{UobP!h4k5#HwZ0A$}TfJKBq^uQU~;*Dh7#3l&R*v|rL)M2Qb{bC^6?AP!HvuQv+o^q3JbssuiC+Wri@-S1X@^4hbmRinzmZucK{zAIbYr<KLEVIJB2jaOxFYE6X44dsefWX!ipwWTp?9j<CnDZx;e5wxzgW-L_0BzO?3np5kvEupj*o0QZjEt_T{tAi3TAh{HXumB>p7{TBg1llrH{g!aq*;yX)>VomQgb3ddA&Sfyorkz0K<Y%G>v%>h*Qr0CT^W{3T7ym0n=U7~M`u1EDCz9;kQ7!+YD?04OV&_0;A2ZhAEvks9k(y=-G=Qv0zNzlLjv+H2ht#5n&R;`R1m==;(G3Z{lBT9zM@cuoGpao4BL~_K3KrZ7cPu~;@Cie+7L93>`i2*Zfs+!(0K=}KA0Q?Z?Wb&!44;m>ZEvYf$L}^3AJEV@=-72+gy+cB;y(>P;z$QFa)eaz&Ij_0ii-%Dw3mkT7Nn9={J@l-=D6&=`W&wfBFrhe+Sg@S295tP%DXs^eaFKmG9?=#l!R`luZc?#GSO%(n8Aa>uE_85DI1)whNHB<V%AB@ZV!>bFjpMu@b>DZhZa~pyE0m72bvUyp0QVlRTuYJ8iGxBq5y^{o)c$_(QKq{U|1RykIM>-}sCxm{7!+-DevL9^#>WPXnxNe9d8`q}t_>sc+ATX1^q2nKDF-nA=ngFIPWk3esz%6q&Z9&*F=oq;wXf6OiIfTZeeu()&(x=HqNV-QnuLS?7d%{;1%b=uZZ9vbKcfU}9v~{AmT*{W>7TUx`iXk98t^gl|-EL?}jBfsfw*7uN|)JDK{Y&v<vB(*_$hrS#Qj8@5iyMw5>V1ebr<l`&VVIKE#WfNaxks$IUnrBm5&a$M0Ng~Bp2w-#Sd<qjfCUF*}U3yX|~IYhQihdPoyF;zq8vQV_Kc`NyC#v+Adx-G+HC>{5$!4}RFc)t&fXl&8y?RGoO+FI5ye%7R3<+By+K&mv8wK=!6*?{vbjaVFTn9#A`o`1wWjDH6g=clj#Z7bR4^=8nUW`IFRT9r-*toZ8u?Yj@w>0eiWe7tz~Kj*Klt9R!Y^y@+{zx<;+u;k$2kJN?<1kBnR!yMz2#0tx9@43XMh!gXG;3KU*oGEQ*RX4|I#VFTa*Lp4H_LVfJcD||dSS9Dt>QMASmp_(h+EnI{Dc}!Hwy=ue)5XU(@7|yL6<mZ=L3g|Uo*TD3egFRBKlx6BeDtlo>e_v$d!mN)|FEY{jz+E|$S2XgR8r|s*L;^jF5i84yEPl0+oBD%S-9x=-oLxNlGIzWe~6uT`k-+e{#p`8!x8jO?)Q;o^~F09mXCIpdkJj>5Aztg{>uLLy&B{4>h#0w(~H;suyN<Bam}l~+g07@s&8^_-QOC4kDIuzQ!tvPpm!6`yp_S>$PN+i-r|bQ7ULwoB`bG-(>m#+;E(>2e&=i=OW_!)zOu2Zps5;E`OA7F{`i5u8pn`)`7ghLEb%Up<U(LLMxKTUr`7g4hfO4mhTYMFu!12J=q;{JaClWtV$P)g)MZr!qb}o;1}C~3*Co>mIKu!4x5_BZ<yP*hdM@6(je+}35=+rG!kSf@Uc=4neVaG>9=OD}|K=W{5ds^$Ua7Jyr}eH5IJ>5SdeUO}yVvnoHWGvC4gwwVm-u`{8YRJX?|L#hIq7zfqvy}NFS^gCo!)rTjlyToJ1>q8;p(bX=;kda{y6?p)R^JPQHMlAXC$j50}z@|-_FFnMw(e*AfY!SgsS^RsAmVD-T(Iedo5G-IS!#vIQ&x!RG@Za`<V}$qRkH3%w4BunI_t>Q8xNs_XPc`ereS@9qr+h@0+)S8O)b{#kPj+8lPWfD63VDqia}KD3$vHkFK$0H7*F62!g+{P1ystwbS9_Wf$Kg`;_xY%u@6uKbS=~`w0QC_l~3f-LlMmr(t#FY*bh7Vfx`N>x|gXd0?~2QuijU^TX@M4*JcTg*8_P_dap-;Gx>}qqU1D$JG{s%kOqNdI~m*x9?XqtG4{)@I6nyXlKKyx{9>_UX|k=;=6G2zw5SsecT6cHhJbEs$3B__bB;|FG@nA_wCc!zwFj^Hdz)XDUWYuiwaW)e0}ZPd|#+#-te7Pri;jdFrGUZK91$~GY|O^tj^Q>AoI+(_k(DeM7i(q-0ixVi)$&k@be|OU6LVbxBrJ^&cAIg=RS_xNUzM0k$D&83bv*;t^Xd8?d7x&Rr?6vM?L9u_~WSd8#3-}d^ok;L&4!mM;+qEwPRnza~oezJ;F`!qvur4=JS@>!6|3~qRVUv*r%kt+N!xebNk1*B&Fj(!eGArNnhBv5AbfTV8EWAt$kjGDI*&hGrWFx`FFc2qZRu2F{tsoZA48%T*P4*-2uJqgNBN?;5p-7HrMb}vOd0#-zX)M>Lv^Lj<nBp<}MR=_vu#!4qs{^U7wB;972-S!kJ50M2{#^p^Y!#w-Mz&BtuMpL30n-QnLlQc4m>-4aCjanmu%Zvg%XlPkqg{?ov8lk2YfONdG|sGvU@y+Lu4m-{6nKS(+8NTUVsvqPQU)r+HI%-XA)#GJ!9c*7$P_xhWYZbo@7hIJ$UaCvOC9_BGgv<Ln<r?rYWIw#KEcpA0UV_}nf)aF8@6v)xfGB5FbMy_M;|I21Gj85q*vi^sZokz|lVS>NHbkZq~ss^Rusv--l9Zfq`njdqh+Bpg+gIM5q_RKtrm59?7n28m%GSW4r1;V;B(&G+H~y4vBB0Q*rfYWb_;Jdu11-DDn7KQ=WRLDbjPQtBWpFoV=~Vq)CiurY>I){#evEj32pVPD^`pIL+6W@q?1YQXnF!u`wjQ#8Qs(R8)}&DLS2!=Fqz<uEtEQze(8n#AC$CJ7o|nk`1qmWml>14_<M7DrA4wr#faIKjj*#A9w}0Q%VjQe$q~UMr!6$tm3gty<ge6-xfuSl8a|K<Eb;OqyTV8NRRQtrW_=+tT+R;{8n=ivJ4KZ1coVYo=kcKNW_SohLcq5Xezp)TskMa-lWmYmTFdR$n&Waj-qza<3s<GDI4KEvjo{<(v~8G=^vM4UV;IAc3rW?MKr-HfDTYaZs<AcY<*9rt^)%RR)brHu2XXM5M{F*@0)-@8pALPot*U=X(qGoxkbB*yF<6<GyIRE@&1pa?r5fWcpgf_kZy$dGxCT4nFZ`{v+#@Z7~1am&&yJGOGU!hx4e-J~DvI5&55RC%IyJ66O}7S?uwBYKWU3EaIZ({G)0djsUYet=KaRCptFaW@n|r%0sp{8F9oBNK^XueIOw;egu>2z?$Av4R5kA&&Yqw)hvnDGDP)}VV1f34P>f#Sd)ZABc+xa@F+VUciHsaI}M|ebVj`@ec9VY&VNdR7@NK347TsAa^tTI8m+c68F|eTLLm{6B>Hx>#<T`RUwx~`X_sVI)R{_HDQA!{aT{kAc+5oAk*Ln^64K_^xi48=mh4EYVd`&wunKk7-Ta3dF}jdKd^g|Gh&x?;h#TMj#&>VKe7V5dxyFuv)8)d?NM~QHaesWd;0b+`wIjukfBJwrNzY9cpI2`mhz&Jp;-*SoM8^h_8s+*9y?NR_yZ2S;?ss!pZhc@@Z5v+@*gBs((&f%a+j%x+;lG7$y_e)_xw7%Cvo{wc(Le%^zk!HMGJo?MXjBEl<Pq6YlSteUQWUL7`In4z{k^6;Prr6K1!-%Ga=4cdE+*aItW(;U_<NGpJVa~{;-3@tEV&2=nCXZB=Ua{QR<8T33oFGH9MZ7(vJ4H!;Xe6Wj7gH+@t^zS6}Jtp%#a)uyq`oISLL0`u|@<raX(lvPl&Ymnr2P-{>~RR^e4fnt(s=RG6h4K`|tXoLafb<BYYy9i%S@=Rtc4Pf$t}8e-gxeZj9c{<(j*BGrv;qw$1mAu>H+4<|%U${e0Mfzo<=g|MFwwwsJuuY>F=1zN@tKrMx<*sYsvIW>esXOjXF^U*3eo03WE}<Fcfa`%m+|4*Y3_2iuxdM{e~aUl?ECh2fo+ED&Tg>X-41_=8@!`dYib<Q}0tGD`K9OnOLNA3UU;Gg>N!*{34!-|yN{aD!|h*=+w|FCpK824?<){y~U_pK%agmLcx*Pwm0OF4y|2cl%tfRI3TpJoSbmkSZrVe~4l$i}zQ;EV%c*CFg1>_qcW6x(&?-UcOa2ksRfAUq2{&BMXVM)A&Kz5iUKFDqeNjJ^1+#7vt|TZ6|P;3?-dFv54;@`AiaLP#~eK%?Vs}(h^7GjmpxmBkL^_tv4Zd4ygxcAOHOH{`~6v!4P}v{{V>~pVt', 'offset': (1.05, 0.2, 0.072), 'seat': 'WholeChamferedFormingCornerFloor'}]
floor='WholeChamferedFormingCornerFloor';plate(floor,[(-2.10,-1.20),(2.10,-1.20),(2.25,-1.05),(2.25,1.00),(2.10,1.15),(-2.10,1.15),(-2.25,1.00),(-2.25,-1.05)],0,.080,'z',0,'Whole chamfered common floor with empty front approach and separate machine supports');FEET=[floor]
top='WholeRaisedSlipRollerBenchTop';box(top,(-2.020,-.420,.800),(-.030,.880,.880),2,'Whole substantial raised bench top supporting the complete slip roller, not a floating pad; no load rating')
for j,x in enumerate([-1.860,-.190]):
 for k,y in enumerate([-.260,.720]):
  n='WholeSlipRollerBenchLeg'+str(j)+'_'+str(k);box(n,(x-.055,y-.055,.060),(x+.055,y+.055,.830),1,'Whole full-height bench leg from common floor into whole top');LINKS.append((n,floor,[(x,y,.070)]));LINKS.append((n,top,[(x,y,.815)]))
tie='WholeLowRearBenchStretcher';box(tie,(-1.890,.690,.280),(-.160,.750,.350),1,'Whole low rear stretcher joins both rear legs under the complete bench')
for j,x in enumerate([-1.860,-.190]):LINKS.append((tie,'WholeSlipRollerBenchLeg'+str(j)+'_1',[(x,.720,.315)]))
rear='WholeLowRearBoundaryCurb';box(rear,(-2.150,1.010,.060),(2.150,1.090,.180),1,'Whole low rear boundary curb, not a protective barrier');LINKS.append((rear,floor,[(0,1.05,.070)]))
left='WholeLowLeftBoundaryCurb';box(left,(-2.170,-.420,.060),(-2.090,1.050,.180),1,'Whole short left return curb outside the complete raised bench');LINKS.append((left,floor,[(-2.13,.4,.070)]));LINKS.append((left,rear,[(-2.13,1.03,.13)]))
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
FOCUS=(0,0,.90);ORTHO=5.45;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(5,-9,5.6),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
  files[role]={'path':f'assets/industrial/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'scenes','assetKind':'scene','theme':'industrial','style':'warm-handcrafted-village','title':TITLE,'description':DESCRIPTION,
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
