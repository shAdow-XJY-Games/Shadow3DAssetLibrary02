"""Whole purposeful farm preparation scene; two existing models reused exactly, zero new stand-alone models."""
import math,json,hashlib,sys,time,collections,itertools,base64,zlib
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='industrial-whole-bench-lathe-and-empty-steady-rest-preparation-corner-scene-01';VERSION='1.0.0';TITLE='Whole Bench Lathe and Empty Steady Rest Preparation Corner'
DESCRIPTION='One new whole open metalworking preparation-corner scene. The existing complete open-bed three-jaw bench lathe remains unchanged on a newly authored full four-leg workbench with lower stretchers. The independently complete split-ring three-pad steady rest remains unchanged on a separate lower inspection pedestal to the right, not mounted in the lathe and not presented as compatible with its bed or work envelope. A single shared floor, low rear boundary with a deliberate service opening and broad empty front approach organize the two different-height work surfaces without hiding or cutting either original. Every component source is embedded and hash-pinned; original scale, meshes and PBR parameters are preserved. Zero new stand-alone models, one new scene. No stock, person, loose tools, chips, cables or active process. Fixed illustrative layout only: no assembly fit, workpiece support, machining, operation, human ergonomics, rated worktop load, safe clearance, engineering or safety validation. Rigging, animation, physics and runtime interaction not made.'
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];INSIDE_TESTS=[]
PALETTE=[('MatteSharedWorkshopFloor',(.25,.28,.27,1),.96,0),('MutedWorkbenchAndBoundary',(.19,.23,.20,1),.88,.10),('WarmWorkSurface',(.42,.35,.23,1),.90,.05)]
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


COMPONENT_SOURCES=[{'label': 'BenchLathe', 'sha256': '089cd0ed8a81b7925a17f52e8256a840159e9e0358fdbbb5f5db225140be62b9', 'encoded': 'c-pmn>vG#hw(fsE1$L%Rfv`Y|q%M}pVCu-W>}Zc;`$(EeGCV96NP;3P5P$(t665l_@Aa+K4KzSXNvdYgRA`{@z3!K8=!YME_!vA`^JJYyK@nKX@G)3eNgBkR89fxMEC@PZ{0D0m#PgLE`Nb-*{4@>x%#Y_m*SaqJBAi=(R#-_KZAVs|SZja23ga-obum&#4U*VOGAs9&L9w;wksq$RKm71RD_o}ubzIY^?mUU2V2-A_`z23ecjf1+D4e<ZHg}6~9kiBNvbIucOQn|T`k7u^*Ei=^Hy+w_@zZujpZ<B{p{hNdF2g98PMvNR<Vkc-mEF|Og1BhC_r85^ErO-xFBWazojJoSC^lJa6&r#@`|)6FEosq@?$!!p>-R9_Mh<t$H?w_RI?r@jZz6ijn_XVy(ghuSX}L&>+Ti(SP3@i;dY&bDZgy$=<NoBuY&@8BeEOlM{=`*JJ(TsN)>Th^l=Y?7X%T+%-1<4lSHqTt@uyS5W-*<%^B`I}L;QB{z42tkPs{3QT|S2KB6tLVd4T&MD}qPv?xqfnYNej+KT9_8qP>g~zi2-??klGRM(R+raA~DPQ3VRBafj98IGuP=5VvJbj!b^v1%=YMJcfp%*+-UDWT9G<OC+c^w$z<vfij@1|DIQOFROF(o^^W+A>)4C_zM}BaN^G0g)uzl9CPu6OGjoYHI-5she&o46*5wmL;*uCSlk9VLzW35beC995O3DtG_~L*H{}L2m!_DdyBzn2lY`}W*q=B<9;urL1<mDSBDG`Ut6<R<`f}Xy#L+u!hprHvWf6rCOe{Z&+5rE(<9P$CgpQ1S??;;;Z)1#h;0o~Q->N}a1Z%1%B+D58<qam|;R#{K%EQ~3cG(;DzmJM!k$6OzRQ#|aZnjXs`wKlhcGDznJA3vkpcsb}w|wILS8ogl^yIEzfPiv&<9*<mNNW&g=y_j;^CT|9coRtJgC7?jFP#Q|(eCuA9e4D+HVy3rQ65-*rySx7(>2-;6+or)mx<?LENO^d!?FV93=)l%F9trC70{AqEZJg-21{boCFa!2`+JWER&po{h{ki;=hAVWBdf{iK8ZX?BuFV?j`5O^GjT-<l|}uD0y|y?lZlMWqb`@u;i+&pjrL=2h{f$+hiX5mlN{z&(~%(FKP4^6ack9sX0_w~CkAo;-VZwcGt1mwC3Y6!yl6vygmYqB>FF+gyeyaeFeQc$ve1uI^>Xd%60gU6?=kbYL|J8lKOn(oDu+snLx8`4C~vYt>ZVNkDU-Z&IN-rZi_as}f(epr5oBHz=0%%y`)$CCO>)iwp7gYuYNVM)R=vG5N;U;)f)*(zFY?#3g>SLM8@5aJ<Gg6kwc2qy?NSACxo*=^{EmTnb<W?9hAj6;X?X7lVnIuD?yOF((wv!<#Hz=y<1ZajgYww^a?p4FPc`tQB^)`=+UeMz5VU6anNOS_f!*U8qXQoCwhc<;_8T<4$Isow`McNQ9=xuNh`TWh0k=&spx?RcI}?ZN?@-Gtz@T?p)hPwx)Mh21mV%h;0cdn(`S-;c30Q8jO)#1fy6!5T;TpGXZ(>q3gsV;D&!WI4y(hbGnS%=>N`*60WJdKZA;93V$To|hohH$i^_%|~=AhV8MXf#94rGO;g+_ns7DED54=^Ge6p;Do=Xv(;HVCR+xMj6b`6!iKRY+xv0S7PvN|T|Y01;Q3o@s5)a4l*zE%=>eC(X;m!c3|aElN`NYso0s7Pn`1!2>Iab(gg|1|#&j^zYa5-x>d#;$In40d3t?8eI4n(3?fc{H`4(?kY53rrK-Jj;R55Ousa>+g^pcZ}iJ=(o){I&4AzNmmphBp@hdH36*x5B`}KJIa$F$<`Rv%4{lrvot%5PDcRqF*Q+5kBbz?=#$#B_sy7~C+CC6)%a@Ity?{~QohNyl2Ris71%<ykj7jjK)xB<&hw<K4j#J@FL`>{VP?EXKCTb%SLE@e3*JS{&mSw=*o!7q83@^o_na2;~ySvFK^F1{daWKJil+CIFDWP?FC4{II3;<epUce1%SFnR%6g^*-iKe4DJQ~*PnM}R2J!RI2c#4&<LD!xpXGlhO25O#>7S~h^D*-KMwU%FC;fHA1tF<J1LeaC?CRF485e;w186ay-Q>~z~e<-N@niZ^`@5$g(?#V3h*DSFf!UZ{ciy)<6Q(!!JJS6lii4zt&ORwE?dv2d)!7Oh-5Jfvbc3<)0sjBbxoY6-5i4uQssTcLV_w@V58C8^<JmjpBnB7a^fnqK9n5t8QhVvJ^;KP9?*Wv}QoeG37b0)(v*?DfKPrO+EgWnGRnP_=M6ET`;J`MU8^kT@Mup)zFXZXcyhaiFDk!p>eghe1pKYme<{n}&rJOW#PvuX~%`1R|c@S_fU_no}hlFq#i5-QBLE*$zKTCgg?c7@_|`15OmEt&D`Nsr!NefsCew{QTjK7G2G{&IQq@#6aW;u<CAmsiuzpDsV%;7w>Ed2Gl2I&hn!@ckIY6K}7e<gQ;55*HvRvRdj>)zo9Eo#Sl;uP>A7P?MDdy0O<k{a>ZPmZdi&vUiL@i8?a%TW1<QzgsSZL?!k3<5tAPrXW|~60!JL7mMRg_vFl_|Je1x;ynA86}5j&68K$`6!t-0WbHc=ks3+u$4<9@>~^|?SG?}W1H9s`+dFgIfop$?iIlR$Usy}T3g{&%ieyccO%_c;uJ$U-E21l4eiTWnB1M7AhL2CiY??-4K*UBwnLs{+%pQ{LPRKOh=HxPVZAVd?MmQEppk~V81<Qs$BoD8Hg-z=vM0R^Gi6XG2MrEh_@|3pLKcOb4v^l);TmSULp^m&aC9{)FZbb<#3&F7s$SMv9H&*eG5buU$3zHAH%}1ol(*$p{x}0`{NE!`7Dl_vVD_@c6NCKhAlFjW3wzcKYiw)H%t_$Y`ij2Jk+AO1yEVdw$;Lo^izsqPnHdfuIHMZ?5vV3fp-zIgWUh%4a@wfH?4`CpcHh$u6JKf&kC3bsq!ked}164F2$=8?tKVU4qML-}dHj6N(C9~+ju3ak+QXeEnM1W8oww%yUX3e&QTrx?kt#fdZw-0PSiMXD-1s(`-f3rRW%fecP1h7@$FY<!q!>}T$`O04}gA8aPn#i<mpeTzB*pxglT0pUx1thV?GSN?ZBzxjj))xWhi180G-aS65J)RuPBUtDaKc2oSAGzPjF<}AB(gO_X$KKkYBc73*8Eiw(Yt4!2$R{s|N?2-uaaK%3Og1Z`I1;u1rG#d|7QYkn8J38E<|&D{DCk-r6KlDNIf4qbBn43oA};YfVp1g1i}Q7u=ZMA<H)cUfngLeaLK7LtYs^H&v@{tqVw#|GcPL8}B#FxHkK!Q;NitAQPJl%M1fj8%#xlk`?CDx|U@Nc^s~(?m$D`8|{YI>LqG?g>JBh-D0*ZnGsn-P5M?3<6l|XjEh7cyCy~0Jnl{24!&w>fGvzgy@E#3oxg}5%a7GzJ&SYSq5;bJ1>pliE>o}$-%JJ<mgwsfL*;gocD9>?T^Wp6OCUFn8y@1#eBbKGNA?30+TUQY3HboR=4=?$b=AH;UXvP%ZQ%fw~<C9o8A<tmK^6NS~#(ZC&(nWFv=p8@bCSq;LhB%Uv;6*v)rF1FS~NK~qXmKJME6Mi7xS#Tdj5g{ZC*G!)aKfALQVSa}IdR~wWDFTUqv#cOlPFMml8UU_=%6)=tj?N&xq1G78qW5UbqTv#ZS(B#W;lM4Q4oa8f$S53Cp2$&CQC=4T$(Y5JzaX^zxBs9OX3P4Ub)9Uod0;&rk_aN_@m6?E$rfTl7<dF&l7b{KX@#%}3znHa$HGfm{<Yh(Zfip6sP__^6#2t1{bLb3gOj7?OMf6QgOkP!27q+x4M@%52hyn~<rPoKCQ0UFmkRe^{0CRzUgUWg$0TfvFlB@%gwG88xrvC!M^+d`8v>1Ag!h78f(gkw5<ptx&m(`Gf;ICrn1@Re(WnIpShr(a$IXaE#-zlH%3WmKItPZEDJ39)PSGqq$eKMR&)|}w1Oll|H5qA>?RM9ss8b_g`ii7~|7hPj4$5+4UTCs+n+O8>9#&8%N|HMU06886{6otp)fLmftPVPP1c{XekuP8)!chp)7JAn(YOZ+@URa+L5B<J^<b??64p^t*{j4-=1mSAxJS7Do`p2+kEFXB1Dc2!4tRwLYp_p0}NfMDhDNtMd8HJ+P`j@l`=>b+I{gaw8_clvFtmgoovHJlDgnmzNo=Q)#d()~@*26;jD-k9bAY+N_9MZiBOD6>+kU80A%&VqeUIxLUlO@D2!L3lRsU_;`Yv8IYm|}~ozO5UmY>u&BgA90QP=sJ|YW$ML|4YH@5%tx4Tp8Ns0Lm;9a-wB?3FZZh-UmN3>^0e?;&GDHqypxJCCmYnLo7U45M>vJR%5?A3*XuDF?17InYI1Cp>+eWpNZPlZjTu@)b^+^dhi&eg!j`uc!W<eSA$q7Mj-<$%R*&Bfkr`|oTVn%ka{{KflO#cv^)xL<24CqivUG{S;NnT@aB9q8%gFC8*6<EVQQyGgF0eqA)jd>vPZ^0jKw3d!F#V*PLm}G-LJf>C4`1DeZFqsGw9t|iP$^k#^FX$JCi)o)|y3reAmQOxsv@T(Ca^~t^XS9K-bq8QaJ7<D;07Jk6#`$rmzDkcy(NoCX`=R>KNXRVbWI1gvw;It4NqaXB(InYoAOwqBtBksC*147G=X-7InTQ^br*kC2UI{Ga$=m0TxJs^+m8wV%AZ#p82LIAd9h#2ArBZ-oc{+)bZKTu9>Twy@9rqwqg^qHK$(SHW0x2XYP^0IK!yqJ*I68VBN*ZjP$b~-B}!jtrNFvrJD>^>wTD$c}6BHssDW_SF72#6SX?iWUcjjP11PcabT~lc(e!kb#io~cVraMre4ZV&4O3fx*?-vdow@N$Rg!P#VdB8cX6__B=>o6V=>Ub*UC?=<OWG+=rlwo!btfHGxE$_>+6P$7?%1eP0U0Bb2l)x?v3t*2nyySKam*XtW>=(!3z9-TFNZN2<3zT3SuZBa?ger2s%QLgW3~LmB%7t`p;<D#@haxvOO`BZAk~^faC|%+-72YXr*H&fz#8M_2(1uV@}~h^V12IE05gqq|bIKi;aHeHCJXz0o$kWQ}*&JxUoNyg>aKuB*2%}kqAbj(%FVgG$amVp2lN5H|eXkRrd*G6OejJb2r(Zn*KkGi)KfaH-?Bo>DLmiG_|%cz6ikDR(X+bxn^aVz|Ymb8A(ZS4$aOEug}4=G$fyF*L5|Pw|Bqo?jFzevv9#1W&+y`Yr@82=0AeI==G{+HdNHZpK(hEC|BVUfdz?dmVv^1$^(hD1FAVQPBgMj`65Wkxc@2$nn<p1$lZszegy`Jp7Z&*JWcLIHa%e2+~uUD^((965@lEpmv?@%#A+e~1IA+B<?wXbU%U*RRYOiSOWZ7USDRVpB3j{MKm5b{m9RA$jy9fxBr);BxHpjywE(l851D&1feuR_*jM4&z#`2@lAPT|n%#KRPoX?b+_?%j6RrkLBaGt*td+~%Ap|he8ki$D2m`R6=X;z^bR~<3ojS<QnT2FVko`2Oh4K&VpEfg_1Nsc2zF{V*P+2)SH8{*y{*q{70~ZIe9|B<_vO**S*hPh-E!Y>(o2N!-Qq9*uf=)f|i#4dYy+jsv;tAw)cvY^c;Xdk&(~kEzGNHA|c<V2^rwxcvMV7#@Jf@1+ljUE7UaL?AC_t%jz>v^-jGxnnp(e-@S_dqY0Nu>A^kF<Bz*EL?T@yXKi#@|OYAr#7^_E0(2U+NFrmbbA#@04w-3~?g5)qP2o~9i@p;1HtV?wT*TFG+RQ4(gJ!3Mp}!qf;Vf?7ls)#%!^u<Gk*Y|mKI8E;Ib=qh-%Dsf;#2E8Le@e5vU&P$ZxP%SCDJq~=Gs!$GT&%sl&{L~QU#w_BJne#B$BfQ8qi-_({UuJvBj>${0>uI(l_X+=7hJf*pA!;+efjFvdtWW+c&4=i^czM-?$Jp6XU&xb_G*3EOGRgo}#Zg}jJ+?L132doa&I0n6@Van~Ft4J4kPT{e5E<v6B}KzN?$h}+^1n|{BuuDcgxKI!vUr`5tO*(^HO{B?24~8T@3Up}c%X{<T=w#$5u{<w(J8|WL1oia6slNKC0LXfj}qyD^9YE77e*>hpHeW`cPDwq$v^tf*=Z8rs(q?<0~ope<NmHKRBzkqo(@jT_G}c@O9<t=rjdb7Bk+R#aez5bLqwu+Y~82*8~KnlEaof1cgCT}%!;T%C!c4e%^U8%oSA~ZUnzh+d)Q0(63Q{4@HgvRY?NS~7F!%bCeq@J1(JJ1WwseH^D2iXq17+`16dYKl^ya2RMO0)fm!gvyd%uslh2z5$}$9w*%Z3<Q&-}$Xv#7?hX;XUd)rEebz5eBo@2`cBMUP)F<$yreg;ve^7)7x9jOR3ckjPC;+kXQ1p)+)3UwnRg86AqMg&ZWEaS5jd&OMSP$ap4+Gj+S(Np)p0-ljIyFCU+&SY4DMkkv^7a2#LNT;2YCz^Dm8Oi!1QD9E%{@xp>Y$+fIWxX$tM(fik%?R}MPnYj*)DihkdyVr^<8V^8zQ1=4*8by8A<f4plYbnr3D}X2gIb%$S(77`E@>=m*oeN1`r>6hwdhv!+y~ngW=BUIN_Dw+y?OnR$lmFy29wq~^||qEk}yaxko@YfH0bD?E1mM@N{5dQsIx7-zCHTa#ntuYr;nc9@AkSqdvtSo^Wnm?Ij3ZO0;iDNvu@De`fvY%-f;Bb1Nz&ow-?uMt}Z{{@BolZaqvKHxxXpM<v_&Ta9VZ`)u_WZVr6!%n}?)vXae3U3ACaV?Y@XQoigV@2=%I@go@OcS@^tbolBOyl$kpjX9<Y<Pv(+cWx|*FyLtkUwaP6iK$yx;CjS@#l_TCrCqb-XrDcd&h1YlE9~esvPk&#S-hCp*?Kb1U7)Qksblg-WvSjZ&aZ>9%ZUkRwpgG@;QbN{<-BhWQa?xeP!PoJ2^r_-WC4L%#B}ICBeN0)h()VOe%S<p+a|O!VO_;BEWvm%p4Omu_JT0Fxz-!mEkHl{hBqkc-uoQyYR@6xrv4^bls64W=ZE(U!pBu|l7#*FI&pv<`SP4@{oIW7cmL?B`vlW?1IWZdq#2hq~WLx8~ncVi$OGfP0wSEsWVgv$OAnS@NwxD&)3H1O{8UJug?~b`F$*Qm-QR2H~lM%@MuNyw=gLw<<^XseX6sHRwqb0l6zlqMouNT!`u@TKX<HV41BNplyR7Z|MW#Mf|P`h3ukOiE_$~aN-LQQ2QM9q;;C=GI)lwyPe=wz6zXUvbg7w~GS)_|xi<x~dl<P8BD&N6e(4!8Lv_u-c5S67F=T_F@@Ety9~T#IcNiKDO?MfHSKUIsy>1T^iY0I=iD5&+5qw>r+{k|cv+7G$?coUFsSoFf#(5XNga1REz>7%kamu5S}oR|~_cBJbL*&*vX5Zf-6}0jZRRpBLBMfEF`-8wBZVQgZAvaMTJpLDu*$VW_~cuzw*Y<{a;Nyx=%cKE0;7;_E`WEGHbW=l{_2cmM|gJ#m2UMhO_|%svh|fcf;z%FpJB&%MQuI#WM9^{L8KiXM6oj-LL!AqxI9Uu6<!Ja)y<8AuPZlDcF=z5Dd$pVx9$k#n1)PggfTee(L<S0}AE=RaRuonL$3?Ay%Wc9^}7zS_g~QJ2i76L&z)xGQytiEvft$ki3aYO|ijBubh+zWOqjS$-nrIABA?FyRK>fs_?VN<~=VsT5$cYAV(9A<TkhMy_ykwmghh$tEa@pwl0m?Vq{Prm>3etzRy$E~Ym>UB3AT%ngrWbl5-Z^~jKZ{o&%{+lwpf^H1m37elZi(Fvd6%ZkGc(m!K9>gxNdvvljuaQIcOq{86a6r>9DrPO~BpCnnMvOBw96%g#I(d&QxbVIK#8myb7c{iCsMRdhOnBs1U&lK(1*B2iy-rSIX)@Vw;E2)q6CJ&~!Q8M!*xe_Dx+!_`W-_k*^g<tsHQj|Hv-Lh^LtV!;)*G`LNs)r^x0~9>cqEIs8-!2ZkPV<1JMc$PYnV$Xg#m&{_8+(5nk{H1>3gX*h<@IIwuE4cRg~a)u{pPnfA1<zS|M_+v;cB7}4Vim{(MAQyD6jvrRVxG>{Dq%F0#3Or%`PAr?KC8fp5XkxYQP}7kN7$sH@y#ohiT+*$*dUON6+<CJEodAS<qt53DqW1$<_#tO*Gb|nuy1mPuDaC*`k-fUc9yUw(ySY01VguZBW6QZ#%O$TX^>8kMA3UG+NJ-D9O~ESMOh+H(JwR>nZC1xiYPGeDUjNqQ{H3Bvu4{_E6)G7*TL$4+&|mt?^+GxvOgnAQcd+;tJeV)tKuh)JK7imdYTm2CHCNmYIO0bqOTPVtaTjcfN_Tm*H(25gQeRt2VQTK#hIvqfm3Be@v6RP<Wa=p8(DM-p17h+#Mp`3&sZNHURn@2{+;VBrO||-`7Tval7%e1>s`uX|#;g#kINTX=-!l`YzhMMbyo=Ij~<zn}CpA35|#=L_kn>0AFC*Bk;&xm4oA>b$1aim$F3~$Kzirt(clG)urCLi`OZ{I6vjx+n{LMpUJeDhbb(x*Vk{~k)%$$VVrJ?d~732XuZLJ_N1#WT2I-_R?}2XudsZwX7invyfLHY&)8xV&UYH}-i?OmQM&SXTJ^g|lN<9`@Gk**j>S%gp4s6-Hzu2kW%|D6z)*QH-f5Z2gzSDC)P~i_;tF4M04EWLz>9;*>$TwGR7ewrCn$s0%{CHTb@J5NTOvQ5-E{HN-H%C3XjNQQepjL#hM4fKjTvw+C@ID^-))(O3wz>mU_lkLr7>NQUBdmT*6#dftIC}1?x`HIn8H4wdZrVp7i)h?>)#;5X2WeaGQ8~Xv#akH*1vlr?M#UOpnO5{qRfDT@eK~W3Sp-yV4KkhG!ed?(OqoTY2H?R<>Cta^e)&69Xl<gx4=K6*_KbWe*0c=l8OVVtNGxaz+fJ^@MCaJ(1n#VO}D6T*8)QBc;Zq4-(s*Q+;)>L5HWW~$$s4O3f6y!x`YN$U-9q&hL$xW4#(nn6f%_7vMdy}F`iVyb|PH*(R|7muVd)RC~wc!>PEKMOVk-}4v$kL<|s65fb~n-k8Lba`jGZk36_fN_kW>*8mpthWQi@yj#K$&#;wSd`pt0L9TO<^t38>#z)ePTAZHv-T2?X^86Fd8rnmz{1VJ6;X~cNf%OfBP`qg3Aq*dLcH3p^yLJUfjKp6lgH&;5Q!meC0hUL~9Rm+*L0`l=ec95U=gvCf`ep<Cxl$h}CPONtLJZ=-FAu9A2{80iVn1gOey2p>hCBhH<(FqJk{rIyE4u8Rb-k1*Pnb5-DObF!ew25XJURp*;l2$9F%0+O?a~54(j^}IQgYs^&rMlL8A=@pA4GZ>q97Uid;0pq;_yvP{J(o7dyg<!ds&}c_0P6vN+u^Ahnh@6r|7OSRT&bb$vX4D{dN_Di0F46FbbVwGu^>B6Vh!Ud!_^*Qu{N!gSQm6YH720a?@sI98z&(5EPR|kBw4ihzhuWGRvqJ&5u;Y5CCX$JCEj>97QP$No{Ux@wcH7i?`tXY)*H)*XjUP0=tK!_QJ(H;-qIhTnB{H0Yt5ercqwtQl8U|lt7E|}e-Z(^ay;+&n2nuumXT-}BCGwU%?UMYiu4pn9Qv&!CAr|VZO7eWn+9FdOEe$igl+rg;@7DyUmA#+ubUGRem^FNr_F=K24P(67(Rjp=7t;0&5$BnhvZx@?44=z1PM;?9AtAK94Cd0Q)M^EOsa{oL#eGzAUTNgwl1iZuf3VJlv~+Au3<R2%HnbD%THJIdz}Vzj$G5L^#S2*D%@xBxb~Zb6mk8{9QS$^1V-!92-3^hV-?|$hZsbq@x-FGZY}9XC7+5G-1~W?Q>Xe^6nElpbFBQ_FN&<qC9XY%t33tY`5L-8g!G|daQL7xtG!4zGjbjgI$78*&?^=&f;Fs-2$FDLs*gg*8f6^0Y)jfT$rgEAscUwx%$wKD=Bg6lc~-#Q=TFOvy#hjAsDE1i^6mPs<+o-G$jnRN&KbD)LXK12%Pwk@Smw2H&d$kzU&rBaa`1ILto1GPY%W+oX}BTdqG13`%#$JN<3pIwY2|#iXsTfBX;_PV8L8T3>ZuQ>b@P=!I5}+_24Q^!SB1-yEce<(!Y=vCjzb>roOr%XPpjZ@5t3*x+D;4VcFI9@uM%pbKMr2Kz0l#ShGst)!*rXFI#RvJ1aFId`h<O<Z9oitABg3r7a-BPso0ITQL$`m*TTcei%<W&Ike%AMpQYo9apv2k&^cxUfV9)If1e`*%r{vwwtu}PN<KzVhoi<G09DiK-bH0Jl5BSw=&2}usy8B@9|-<gfW)9XWfFeE-`1kAOy9(`rbEjS?nRZE3VCTL1uGck5<=Jp41e{QFhlWU0go8c4c3(2>?@;<TRsN0oxu{h^J{-Sx(n94?k5U<mpgplvE}DBT81GTUn$uTGKdzeSyVHk<*cB>|x&}zlIU7qBulC@1|E5|GK>R1tF$g&uhrov6VeZD4q)O(*o+uutN!5#381$ZNXnEGfAFo9ACw4?#TeEJgsGTYY(+=#jDxS&TQJjVlxl2G9xx3-{3CDlxNowy^8Es%2_Qdm0PK{1VJ#%SD#!iS>ji}lLerlF8G($`H+RMsfeCTj{fSqA*Uz3fpcL0e`+Wn8zkk(9vLJsC`!H<Ctsq#cMr5qZQFo?TjPzkkP{$XqdclmwjFCcZRd5<E!PQvY$I*ZO=)-X$+XnNt}v~94F&2YC9Wlh3vQ-}JIHUWb&NGmh{(YQ_HZf0o*!1({=;uf_}>rjzo~To_rq@({X142{!T=b!V)4h(mzv_Q2Bn6NS`JFe7=yD5iUwbQ+#C))wD$21cKWn+X@AwuoZZ@|De^XGKNV2+uJy>z=XVwn7n)a&O8eIxKrN$N0+cbEgw&SU7gRfFy%PJ&^U$Qwk*YRWM$)9WB7>C*nYJ6{Ji};`QcLSxQNPo_S$y-nmAyT5EepiQ<A%IC`~~&SP&yBX(Jt+!9c?0axxN$ZHTxn#dC@zpQq==4mtnLy5QqVEUKf!z|W$srLr<%t}jHW=!pnj7@_!Xn9dr@$v8jeLs<B{gs6%Cjns>7CsY4vedLT(Ovdnrq_2|0;F*LCd=JT%>!0k>7cqT|N?5b|Q8y7huc80#cZ8;uMamDkY5o#GmCip@H_rI{FK5EToG4<xvPl6UHioGTfy)BX2G{Dbrg|(=j*BTqoAPK=vV*2Fl#<)kvW4<wz28S#CbnqzcBd039VKKKK3g&cvfF$3EL5o{>##yF8*mUy%fk_lBaoBz{^ApIR=<&2Ie+_`?FxTa%%GTNgh5D57405>JLmPq`^%5k`9E)d`gC>q?~AwA&E>@v{c|NL#DDcimS_!F<(3~ov}~;zd<Rw|mS6M-XL9tPNHLqz0?7pRZ(ZdScpST=CDWEsUVi;lZ$^JtP?}RaPglv;O?kA^WegAcKk|nlRh!aw*9Bv0F==5J)6Z9*-d%pU@XB=&R0ZB0^)(G*M{ark;lrn2I02N0h-h~1`}VNiKXu3S-_gK5J)StC_oLuZD)FfSRr6g2xxW1PzA+n~J7N%YSh}eBK3rbkNMIAk2lDn#A2jYDdPnkTJb{tK{XUVDzPco7`D|xN;&gE8A`6iiaqVy4%Q3ER&Og3Azk2J9jeNL~0<W^(Wv;u*aW@j%6A-cq>tX3mo29_F31{YIkT??cLf#FksJEC!;a76W_BSnOG(KNe2bK#xQr>L1FIQ7GD5Jw_B>sw_I%~iyx%)5A0G32YNOZOD9f<5uNvHefKF1~yCS#(@r`8IBkWa0ZVV1JI{PbyIlsW2%kWt1Z1|?R(IcR{mT%0BVd=OAZF}GXBR;sy}ca4FECW@t~2{5xte*?09W}|*g<B3BN`_DlT7$LDi>!lsbf?9Dk5+6eo^kl*CDX#E$_GqSM!Unbq4lTt&G+hps^ZDs%zkd>(o%LV!&lbJGY~Bz2muJ0KCr7YgO8ePN3G;WjH)6+(Pmg;f5_%Ka9eFEcBGV*^#Dd5so9dO&n-)T4G8Xl0RolaF-@jKfRVi`^g}lwbN}vL?HTF}&klXB_O(%xUGKI9UQ8xKr^#uOQesS44p6sEM?<Ku~RArezdL`Lvva5mtvdVIovw+47c$bomd3KL2%Q#KJ?U4DYu_=d(8k~-RB*&wk;Zy!ntKN#5<PT<1&HjV{*n1#E{oAs1a(G<k=O<O=9-<%blFme3gkxu=>P=?n$G6WZ`uZ`9imIoN9#Qn@soL$cwP}zc^GECQ`n{f-f<s@;WVBh;2<jqGI={Q+@RmI(^S1kw(0nmf|JQd~e|_91)4*MQYKL9<^3Vyt@u?D+^qzfw`>WkrCi6}1$-${MA88X4rkHZB|J!<BmSAlJ`bytLebYZ&w-Yx_i1QQD`|?>CkKRW~S09C(2Ae3zyf)9>shT-R`XQZqH~qRH7t-$hn`F*!HkWgswo@fcX-t>Tu)6Rvl~etX0C%oBM{egBXWmYGJ@;4+_wkj|W4ALv!O>~YJ?hFA+;B;(O{Ffq9-mP;JI)QiBZ7A|#p!r<1?+ROUTxRhpU$o7_?dJZNz%u&KdZoseSmkJ;DRTAyY+Y*x{SPI%<%T|`X6>#MmzNIGpgX*^rGfI(ww|TXGAaiRzt;&^}OL;HrMb}vOhkjXOxmpwMwRZpiIv2=}a+q_voK;Ih-;iW1mzBlu#P^alotMO$-PlCD{0ABCbpJj>r=e0^hf6scEcS3W+rdFC3F=-9B~Nr0kRP$2DlG#=(<zcYsrz__QL9h3W|#L#e>?t@>*bp?@1EIU-_t?5FvPY#j4g(|R~=hpx`jz_$*UA*fYKW)Z1>BjccoYn)umGVE)xlXTcWie$s9+>ntH|C5<8olM$Y5F#YTWVSP@L_{S>zPIF92KlT;)Ez^5d*N6$&!Yr#C>gf-kU&%FIPSQa$*<Dss<BR~tK>i>%)YDKNnSvq8w)9impC5w<En%ie>Z&pR*b_Ne<8`J|DFVv?(WdZ6#VEiX!#~APb8mLR~9<@v8!oh{N9#ZsWO6q%p%O?2s`KdELB;h$s`eCjJ`v@o>x7~ZHopuBiK<beBVmAf3ZD81AIO*zOAjMq0CgSjuGd!nHmtPLQ2S~A%m+-6c}Ne1|cX<MGsS3B{FVuiNRc3lkB<(8)j{dJf?PDz%Y42YOHnJr7O5l-#u?Et=!x00Tuo=_O+KC2>e(EqvkJghUckyOM`MRTYBD8v|opz1h9b34o`eo5e=jLPzYK$Pwo;xAO~4q<+=YThGxuXj-!xfd}5{<VLNQZ*Kp8+kDl9Nx*9tV9)0p>jN#dRLu73UAXEtu6=Y+==N(V09Wy5gHP@qWG(ZJLMw<lekn>gOsCVF5_DA^;+Ebu0`+RS~zw_!bj6E^DJ>d&8bV0L-lY@psljtiEKm3cj<k=&d>Y|7Ihd<oHKA89Iu5|70Ce<HuXg}+-PxQh?MgAwkNshRl1i4f!i#@?lwPN!!2N#+1Ps(vPUCH6Je9tiamnO`0bFflF<tg90rM|hvN4_L~#*ZL!l~q$rWrUN3cqZO+v1a{OlB&;pv%ybvvEM<ail;3}NHj8PsR56&a}vHDyl)#$Bfdi+yVBo{RB7HnB|)^$UQq`7cUDpRgJ#;QEnP<5v*b`nL`0D~yQUzm79uAcjBz>z`4!c%8tjyhJ1}w$omF}6^@}-Bj}PlVv~SUa%-e_cj(v;!+Wd_(`Z;m?<zH>8o%o~wEjFo_ko}!*anf#+@^qd)E+WOx9}=Zb(z9-^V`=35h(A=0ysJ_7RVfwvuy)En8O2(xY-${uY$(kh_jvHobe$|%AUA-f=vxlcxi)Sry}KeQ13-59LN1OXdG(u2R0Z&60pCrP(0~*L_hgVK%O%N0b>ZZpt6uy3=ZWfEQ;OBU5K0EBW;E~JA3Ho{SQ5E3bZN#j;=+^iQg~C5lHVF7__IP~A&-B(@@W?zso>M5AZh-yJ|XLjg7uSa^;s=$^+)j$_=b@ESPlqFMx%ZS&xpUo;Nq|6l;IHhaJxOxhE{{LpEBV_Pg!gXmXcBSnN9o2O*xM%(j_YX^&gHLsqaQRqyJ#c2&DOEf=1T`ktvkG=;<(Ab!}{47>;Tcf=o#`7LF(bw-BRF;~3&!3B6B-JB+4GHg?gU^Y~g{eSM_*Td5~SyxT+d;M%ogDSW_&A6z@Y4Pr9S$}YRgfd6hLDTJM@zCO7U^L2hd+p<N#e?qY%EvmySoSfAPY*-~)TRM5GGp?Lroxb_>^XCs2Hy2N4TwDJGpoTX6', 'offset': (-0.43, 0.38, 0.808), 'seat': 'WholeMainWorkbenchTop'}, {'label': 'SteadyRest', 'sha256': 'bc3ee412b36e15c08899abafa86c2d33f16f4442764a3a6b31e0e5c6d599a4e9', 'encoded': 'c-p;vdvnvsw(tM`6go4tOA=`t+aUpLG<8A<3^h!klFXjHkFU!m+j1--ONt~rF%;kZuHRbSlKe=3I{RL#NbFWWR<BpDS1Z5#^2^68ybfbOvhL<d6j;F`E!I|^Mq$y+!uZ-M=2;LlQ-5mZMc_}@%`C_ZYZ_7)f8Dp@#7fd2^9%HyM1Htv{qoB%jc}1BSz#^wVy-^tNv!66K99n&%GbFn!bPAaNfZT>B2403g+-7RNfPCaS(YrUltxisOHcBNzBVqePA;xIjBMeD<Mu!Pb>-oaGaAjpC>V|07J-&TD|*;U{Va%!#>wU7*_CI9@pPFNS?EX2S$H2zo7MiBemrf;9y5Q69<<eFZL7_8$L|00?BeqM$8*o_wA!t<-M@N&_2JC3-(oWB5|ddMKmbi<U12iof+r)`={ZkkUC?B9<IUOS>Baj`S3KLtII!a2E?QguvY00sP4)m4>Hy`%nz}@^^}zBclOWHNY;7o_EZS_42J|B?tYk(Yt##idv+k1YCJlp0(6Uafah4Eti)0xy@p3GT4dioRJq@O`7;RzVXEeQUO_D_#1qH2~+y$AH2a9kLW|L*)XVfPz%>I3PMCkXa=Q2$n>KVoslY)3A$>~>0Kb3VC7IT_}wpA=?>6n&I?gS5jc(#lpD+*?XHK#cUP4~n&A?<6Nh12UGx5f#LpZmlEc^?>|r6z?%96m1un5P0fA!IVQ0zb<Y7(7{C&w=8FvgU+m-iCCHmxVxRF$PltlbF@Y!zrOqC|%-3_=mPdpk<by)4s=1NKpBORU~O`R_b@1kj&)-0>Lp!;=(6{_*P1wOs(rBO>d29^Fai9#z0~b1ZHk!jUyr&2pE3}NL;4MN|pr{oqi@pUx4)34lgNWo<-DQYTd-i7=Q;N*BF}<M*S6$-ntIrWf&Xoo6sy7?I)$3_}8@E^F$a)(cH=8Mp@IKAn-vvpBRS7K=jCH6Vz*#WQ)G#6S-Dl9*!fRDaod!XbM8eCeLH$Lhu_+HLp(Q%gK$*HzBwcKNc~aC&`VK5+?u=w5V@oN#U~utimaHi)l!rGVvqK4k;6{S|n3K;+G&xtemzN<Si0TQeBgZlXxd_wC+K(370LBRREOIz9(65X9e*!;X}7XvSfvL1#&X(i0KQG$5Q63oLG=Vi^xZuC;E~;_|#j;wwq%J1o0EWG!7#kUM#bi`cjVsbYA%Jat86pXb?d{^a^+`f<5<V0SM=(zKo{cQ<nP`^_hi0#zlC2&C~gDNZOgyFEdFP)Bb%{$F%W+2e$0SJMZha{)hMHe_VQlVgK~w`PIqk6@Pwr@`-=H{&;c5AKspkrlsHS&oAG<IU8M_U2@09r;`t7S664=z_I@X3x15kRq!{+!Fuyl^ntCMR=2BK-509Wd7(P4YCV5RAD_9(u}|lIHc9;GE%WdRqdLg`AXd&XuKnytwc5utx_#8<p)b(z0z=;rpS)$E$$!VMlX&_8vVRG2!r*5e)x!8^GV=IPwGN+S<lla_cnvXo%~Ey>8J!fQ&w0&f&#7M*01B-1@$kqUHl_h--09Tu)!6N20f<KwB>mvrAFM5s3hQ32q5QstDR**tNWL8J8`6Aa$YL4Mw|slZlU#;ifG<6#NwG0`zFbhhN2Z=+NuJk-IR2nBd@>$%hfSY;(5KE&=}&F6wdJYOpE_vk$WxgzCVk-eB?zz!TKR2OI0BrnS6;?pQSZik>^#+@r4OAZg%kT^LafwG(M&2MW^#KCYvm0D3#3KksWT&qDV%#(y>v^Ir2H|($JMYuGXrk9`Ib+mAx)G-%SGS;QGjnXxTTE@mEZ;6Li)zP4?4r4>pnfUs`30W#77eC>%i%#D2Qo=W`{Olg)=?-t9GwkJ_|@d=@g`1bwK(Wj;8!>SOE?>uVy*5PH}n%nZwlDf`OV0ZEw}>pwk;3+zxsjg13*ui4+~_XD9Z&4yyp3eBg|U7(=vS3Z7QQn1&y>=<r+Qj!SJm0Mhdae7|*q=1ZQc{mLV{yu!Y<_`6~n(0WYzFsGA@<|67;^ss7FQkud%F`@0<0N;n+G@KAUXw8u99*-En$8TnX0QQ|{_`zeQV1|Ku%twnLpF2^Kq&Zk6_5d7z1&{VuOl<zH2K0TGG(ybSrM=4&r<?(#eG(sp+mxry#7t<ssTwy%5hS~VdY?Uq7|Z=f+@H1l6t<k>++YEPpP!X;bHEE$pF*&f78*iIL;quOA>A1f3#3W3#(I;?i~PlS>VrSjr00|(>^^ZOMs(e#Q;IRSn?A(B)7*>5v~sHb@Z7{!WQ0KFgUNx;N*iE}CzxxCFELQz2XiNXU<M`Opk-Pb`3|jmHxFU-(qi<${q4|T?z2ormdgTONWhQrkd~Qv^kwk5Ny-WzoX<e2nPP}OA(S0MG4O{1$XNfL4Bb~AadfBKgMAjp%RrAHi`oGvn~_UBVx@oI4Bg+nCJ$v0muf{I4n&qnz9#f@0x5G#)*yf|^9`T9)R##!bT?Ke<d)pP&k5l`QktaBXSYAj0{@2k1yLUKGCw4f^@OF9^u!sN(V1hPCvh_mVXcyxLv|-woA8`$LT_zy;clSF?Q52zr@~8Qk1eOcXf4v2s&!kfI~zLq$4ReJA$m#iRI`<lxD-q+f|^1?2M(Q9>I-8Hr`CX1AIdTIh4lujbS-m?Bjybw0d8;Bf}uy79B330B@SXWrvLsy?1H_2OdLZM(wNWq4=5ivlSBf?$-O*_5;YIEPpsOeu!ljE;2@oc^mAD5lo~tS*pbG2-Pq<vI-7=@Fbtfw>Z(K7CeAZ;q@Jr|`a~uUeTGTZRmaqJ$ZgN)bC*7KsQ+_CMobNUR-egKrUk~b@}Y{oP8WN)^Z3+;34^l(Of&OnUKmu6mT~Uf(PrFNt(VN43`X1SFJ+t@s&|S;(b(0>GYw0^D=SKGFn~#wD*S{=uvFO-K1L=<F6T+%FQ0@@N#80wU#(1sJdC$G$N{@S;GsE!Aa=kc(a_sDH2M$HSf~uICopm$l=kn#{QsYDI0Y!gD5rHj&%U=A-5^^b+b)D{2)6oyKO;301sW^I*HSb2NvZkFGDEWSnA8BBa>o0SJkOH5e3$dK=rkZ%I@re<pNa5leXx%w_>oB8=N+D4$y6D)69B`<c!2HZb%fwcHq!Eb-&Xe>nWF;!-0MD5*KDDBZ+#*Vc9PEhoa{UXD-EA^56q|YewKOJ)6G4h9dwpiSg5S55*BEbgRF)Kp8cRE2j{fsvIp?7r^mLOoV%6g;f)Q+KK)5S*+9}4=`&GZ+UiSZ8%6u+3p?Zi64Rbwy*xnW^F377J7TTNFbp51aAOP_+3dQ$Moi^T9XY$C2D=X}j~>ctwz_TAY_(q=k(z^F+gALg)$WpK*;X=zH6w+w8GTcTIaGlFf^9;kT58S0LPD#y%Wk%jCoJbS(j+f5SeJ<0X^;Aoj^7Dn=mf~x<QmgYxUcOlL)T_!84aEGQ4PGUDBw7V1A<HkuyhoU;NjpvDd4;eV`0E204?&2^n=>~qUU}zQ#4stDC(^8c{qbYvIdU*7h-cZ4bc2e1KT*e><?JZE}IQSu?Olfgy@j!t8oM=r&jmqfG4l>f-el6DI$Fo<ZO^3(lB6v4jh80$sb+fmP0YzYP@oINZTN6bq>`4U4N**C|UNzc~Mfa;4Don`v3?zurF)jQ4<a6?^s&2;lpFaKS~l6^Kf!w$viD4jN=~IjAulCIc#ceM_&6T%onW@xsN5zN4&QajwQQrle)4jlVl&zim7i1|KbG`o<nGQ#~*@O!BLpk9Ih44<PIV<$IP0CL_m)FG+UjcL#10@9M^cW3IR7I@>|94$YPG+9Fs_KFj$aaLc%0pKF$>a8+NfRj2VmdSn*-2`@F_{tu7I>w}}dY+7L3{PesB7?cw+(0se)Nk%n;%6`v67Wqf=JW4jMKi#qVWUp@mWj$VS7UDHxEKz7N#)7X%pu?b@fT2h?g8Yi|QN#7P!T1fUV(6hIB>J3?CrMQimqvxQ;iw*pA5V?DH$nr>bgWlr>!tRF4IqG)iXF_!91YsibHaUFvMHFSXqvUI+M(i?-zr*Nd6kq2JBx!K%r--;S;dc}i7XH5YDd>h{NSgDdeL&DW?J{P@Nn}**Kec^gqKON;Upv{*ku`r8M*#nB9kwABof_ecjiW`6x6|afy&)Z+2nc)o(^}ZsR-NNInRb}>*#>pG$2;uH@I6K)V1S|5oQsgU-Z?MB9e=0Bjcub>ecL!%4m%)fx4X@+k{g-__mT?H#Ka6XIV)Ra<B1vQ60TPFr5r8s($Iu=%#fWgiw(f2PYtflOUO~@CCKrzf=iCJEr^=P09BH-0~u!C2CV&(0Xr2h2x8TcP=&u4su+~^o_hYod_Gp4PW5F7J80=S_47@ilKNEZr-cdVWIcFDr%L-sc*beaI^p)QJDHN7J+IA%<acy@L#L&Th;z#89r9JLx!pd<iwxliXfvI`N()F6Ih*(ZZUjFZRRS*ju#r7$N($^T4Q3|i9jXB@@?1DVPoiObkNlYcDw%){7<EPs!`sh~G>q*oVC)c(C38p?P6Snhs?#}5o$#xG?d))gUPZ$!z`i&XVAE2vYUzegBnEXbk>g_+kGcY5o46k^K0hM2UBf6@!HHxlIAvcRi!*;B$$XRD8z))7=V6(Pl407=+;?OU2znp9f%XfHZD=gLgOA8Uo|L&T){FIRaE_Hx+%dR*{+##GuHiagBsjY3DNSODUBxKrxHKd&-G_8utd8=oXmLa=$YVBfh}$yauyXrwJ^I>_(jIY^sY1*}aBZu5e9UGuGF9E@-Rd*cQICfj2qbJ#IE7n=E>_CPG7k0qqiaNtR(R5S@zUMn*4)4mV|l*)?!XO?hX=auR_ytlef1T2Hv9ZG<c2jJCDSHCQ_r`R#AG)K0~F6jm^3_C&o*m8xz55=k=dCnf+AaUjMKLYBIPm*c1~!Xlu0KvdoDynzR~pIB!F1bCw%6gfu&C+U;THI-F%XiwXG5^ZW%2=Y%+5?Vm?j7O!6m&2aut;F6Pt^Nl3EluY*Ddx!(~M8)d>_kTOef`NF%_%8!;o?o=s^>w#^$+T<Qz{{H^$l_&Akrn7*bJqU+Y!b5j;$??8_;1O9KWo%_Yzz*F5f?3X!Ehu^$t9v?T#xOhtVMC{OIYzX9Kw9Jyr$!h0f;JvC6c~K&1?u$Z^T0M3CkQa#R-2w(5}1LX69bIMT?{89!yRREN1<Ma-6romi8)H5vrTzWrGQ+|!`FAj)_xSN41v-lj0INHahF)qXISRK#<?a@x1s~)blq3op!vL99-)8kyiGLje6T}iJ%{&<CfTB8nX_Sz&Vp4K+>P=Hxn-WsXfbsQB&DRFm#8j~#2M-DWjxKLUWaw297bHbz<Rx2tyQlRpwl*)kw;Baj(AFrA(r@rgHE4Dd`gUDk`X2ut-_o{ZG;89t85v#jkh09|GG3r4yoUd7gxW3^jgom{lDK|oQ<x2e}DSN`Pt>AN6vctuyK0w=h?-{rT5h?=F7!6_QS~TIjy53)$Fv$Kt3kXv~T_9j84FUo{-3PkY$%vl-y8b2aB1uB1yR)=kC!k_9r*oQX6<j(mu;bTkI}&o%w57?(p`3r<jo+Hu1E2n1|6kSq4RcG|!8DFmLtPg8y4z&@s9^J^64(Ncq<I)q4Hm?EKByh4tz8lgl%NoOA`;I9;nTC?@rB(DKV7jB-;U_fJx1Nw)Q{HD1jN)cEL5umAb`6@6{cWGx(0$@nu3Yvlow$s^`!QHu8E*@v^!E7HtcU8e!+oSbDIjIN_(>_<9)$(mpRUT2kwQB%M0TP7)+yS?4ERu-VJ##y)xuEp`t1x5&+3oUNx^UoHt1S1l1*q?bTUyHf%=h@Z8`%`;=9~AzKM5lWlnVyz|FVGTE@a)rnpAy>5_{n-gil&wONRH(m(QE5L5KO(!^TtLa@ZeAVv<O$hh=<bZf|CAD$7v8JVP1A%l&vD*OuDk@NB%m<^4=<XY^2^XJ&BVk0b5^CZxRntMucLuZJ2ZyaVp6GpgBDI?fZY7y|MT9@SbfVFkH~dTH%^YFH!B~lbiAB{N2_hTfHYqlw^9%i+8V2wtCZKixC~-ajqQ~+40%GJ`q2jy&=sZ<g<H*ek5i>GrLDbQ?{Xp-Q%Ik7DQ?!R?QW<t49NVHl#5cbp$G-xSFiOY1vjsB*7(^ESv4#vu_giPU2a3?cf;GI=|Y?9tN%LYafT!H~M{^+{MDf?D+s{R(m`1akkpa#Cy@W#kyMveT;>-@%$h!*D$}Yj}YT}>1R`-#l$mYF;>9D^9;ACiAjG?8pPe~5OB26m+ED5LO9|^M=1j2galpdLL^>zdlX(A+_BZ__7|;bIGf29X&#S%QfnpDIAHs!w`k$(2x^=^<t?&I9s3iV<dcvXVQRg;eDjtxb=nH!bXnvB`?XJw!6_!RhorG*{xYJo8^(`brs{eD@Z%uQcY5;1YCZqN7Nc;o(~<XH>v$5SbAP8-r&a561^Hftd5&7czXJ|GZ4YSI2b`JCmxKrC^nKkyA>$v=ky1ZQQab+w8VM^9>I&uMkR*~2BvWzZwHss=6&2Csz!Q?8O1r98M430&{gQ_+h231&t=L92YQHSdDkmZ_ym7Dw{NSV**x<Kf6i&%b<|1|7%yz`6bWrH2-Tb$$A8OOAW{A;q<`j9Z?QGh?685)U&?9X@&gt0~c=(aA93|}ECxg*AZIVt5woAgbWtnsE;L-AQ)Z7*ZSdqICh=9UUf(Q2iTGQns%^fX(DyNA@H^DmB79|RaA!z;an*BSnib|2w?vAcNgOCL^DI?=3*buRx1#@VWuJPR2@O#u?sHlN!$Lt~ZU8Yk+<lKI;p9vU(#dj&3&;<JKfd@1+tTCwq0LQbCMYRyH*zd-C@(@NAk=&0aBS1Am!6T^*XS~oAZem!`V4uB0%u^)wS!mh-@Jq~sjWLKskM>q+ph`Z(5mB?vfFyNB1=DpB=g9h-fg^-b@4ahLJ`7+vr>zErO7oR`$|rCq>Jz!-3^lA|Aj&=_)Qpf)C5E7Z@~O{sH{cNxh5WkaFA-=N*4o4bAoQgKi?pRs7yIfks;FD}l<j^6&SV};ZkX+$Xmiv&OD<tl_1B!3u;&P9dymsLVIHDJf6AqW2zmsqkPaz74reHI$8?A*(ljkDu5?lFNi(*X52W<b$;0cIY)=-C8kuE!>51@71t~q82G_i1(IQUtUsaW8oNm=aH%GapdkcWQHanICLRHg=NxinBjj=3HH&kaTYObO6fSt*QR@lb4A^2B2X7@}_ZI@&0-ow+u!2)VDqDG5Dy9a>mIEf98M~qjy2ViZ2ltdSNKB_H1t=|YVCj3AE7<$@OYP}_Le$wpb&{JabEW97xC0R86Z!(FJ$^g<p8YM$IM&dq2+2nqQ1VcqfY>neYBU;;>I0&cC2DI+b8|cNP;&~z~aTSlV1@sn}B$~7f*RASzDtL$AgO^Py^L0ed@@O6wxl?vfshUDhqjk5wsO*Mf&7k9%`muh{<<F>)?9X*<cB+Cd_`2{=j~#T>oG@eQ>N09}U+q+ChVjblJf&y-Jm(2hOt|C;@|-4kLOsghFSP_6)KTH_RNcx`y<As+mnE0FxKqo>#<%6c>Xp|ys2b?g^H;^IZo3C8lqHr`<Oj`C7!$?_5io5P$EJY0UoDAna&b?EGf8-US{HLNi<s)i&!{ctyC^5;Z!B}8Z4G4=7V8$KdP7VSPH-_RpOa>oHX$Aifkj`%5`YPS%QTD@nyqF1MTS$x_md`MTILqlmbMxdFy2Ef>XKsj9^y>dVn0~~*FG6=?Z?=ITRpiXk&@NGtfD_m=tDp9y**b7`q6l+d5k*_{b;h)JV7xntwWBD7x_=3@sntBV6IJ=&nOpt68Q%*z^Bh+8p7}&cwLFXla$0=4S+Bf*Xfd$j5+TBcI6RIoo6P=CuutJa)L@qN&`?*y9g;gryob%mz*a*K16`)xWnI`A(7cVM6oCG?;>uGizOFcmTS}iFboQ{i@2&>q$t#jn)1SIuKSO!TxQ_%&Sr-N@Q7Ky+>AHq5SX2zxy=EE#$)dGc19SlU3Ql9+}c~n?AR4g8m330#$Pvu+fg&%UlRvPw){?+Wwc<q4H32xxdu~~h*2Iyvx3amO*b!93ArFhMbc9Bn@v?Tx+b={7%aq)yf>-k-g&BL1o|EXqB<GHytI3AGU^dzmxt34=>T@#dO$4s?Mc-((u+t>=|RU_<1@#+%@#SNUq;F~s*mtQa#t}TKdz$X;IGt^aHFFoxV*&XA@nUf^@rqX#nVwtk7z$m>JAQvN}i4PJu4mX4TSk6E;pLTWplaqZwN7Wlw-e-$t4V@7Vp$n<rY=h6@rdERygLPam3w53$i&vhDzDApK!5UjQDa~n2<AL=0Lad3+x9$Y&E5C_k3lK$@Box^zej^*2qs~C88UkpuxXdSMxBpUPtUPS$S~H7dXX6G6h-W-b7JehW~ZxC%Xfx%-zD=%N0$idjV(qZXc4snmGbV8wB?p7M7H5nlb#=skzK*vcyx88k!IT*!OGZ%M7a$cgM8XpvdGBA*U7O90A{R7Ma!_uTiCzTM^v+J9hS2aEcb6d6ipQGhmt3zo=!31Cac&nlDh^FnQcG0h_K?-rz@!pS`9}f0B95YK0PQ`q>`3Eq(WEg*$N4B-Q}3K+u6{>r3;CXi3T7tw<%dNY5P$qh_ryPnPL#?OyGs#n;j&1wRd#?^bSQQ?6D+WrL=pMVI(3Ye`7^Y4=-YKj3P{uhv_kcW@6b;9JVfGRZO$j`H;pf1Ua1T&{Ads<4Xl2AVl@Aq+~tM_5{}0X8hT7r1ecaL;AGhQ3k5Cp4}s@C`sYuyL({zoMLdyj9LV=1K@MwWZzH9%`y?O-Vc*-CPns=8||&m<)UmL;5@pT!GcWee|Sf?!#ajGVaVY^hnWvo(jLsWY#qIG~l<!w4md{h1I$9Am9gi=uLBT)2AQMx4?YUH-+->zq}yq0X{=>Bt>)1=*vXp$V~I6&NOe*k>Iiwf{|OJf{Nf^HaK_Y_ED&B9Z9u)c^hl!Zr9}3E@~mGOpBB)zjdXapxt2SUaOPxoZt$0bNN^ELX@C5pGDNV)%JB(PxYG1Lu?J*;@OfKRrzhT@eNlNY%b2=>#)SI+X?~Ro{*hYKz~y)XhJ`(5(v<Nz%54U|H3!YWGbZ}YJs+qMt&Ud?ki1jyQK)&-2gX1K5k3-xP^T1R~Hv+vE5B=amxo+CH0o?ds~PCBJCj=g8lJ$&$BT-BU7!x=LAOxDls3VgI;%7K}|>RcGFnzN-COt{>&Fh#^Wk{fXROIXfbnmrl_JD87($cPNwk12sra6Ax@4&Hejd8U933@a#C^!_@q2b>AV>SqhvNi7!?R7-!Ao}gyCmK!MoUFc?c$l3b5?4Km?gXoKgEtJv08X4&!oxhP5Gg8+9&(E^)84S}#dzx*Objj8-!8{OM=!s{{vnFye)3Rpd${SzN3xX3N3G>OC4i_$=_ZfY8qjDp_dKKCZP>AGeVQ<Tha;+)Z%%MKVo9i{pXYkei!m?Fr4<sljAu<Lis=u!+7s{NSl$nZ_W3W+`hwXf0k$q#uQ@f5kdPjnFm6fo)am(G)OD7`txY0}ud>YXo3Z?_qlciG4zW5gbJD4NF&=hbO6SS3?wFm!fV=U!enu`UaHk_?OuD<$;e68^JK1{u|1Wv!DuERw|m`#UKF}ujDdd1QdfKh${e&w%#|DwW?Zc$p;t0V``)5E1&RsceIE_h8^-AFuTdo@Ie4vDd2KK>}_hRjF`Iy?|#+}_2`iv&0Z_p*AfMD8`oqu@7Xce9nk`$)o;j<@c1yWO82dhNJ3CuTxSbGQ$CY;wl4Rw#XS*mE&fyJ0*WB}KvRV~v>2EPc{;?S-xyOvqVxe4mFZ6CtZ=a(n|MpkNKdvNmAENqa2uT983ij+N9?!luf#Gs<mUpP+sejm>>A?b3{}5}C+tUwH!xLIH3NIcz&Uh>{dq`zbz#=``br|q8%U629@3Czl)#{RxvzhtRw%}obUEhnT=>NZ=_~Ju<XtX=jx%S$m-~J^jjNYP>uj^ZHMn~ow~BQdwD|T>jzFMeU!DDHWV@Ai-C2;l+4BTW+9a4R@m3#f549Pl4%6apRvKiBupm*icb3h;J_S-3NOc90z>r3!qR!XKO1evJhw^k|0V&BV{W&9-8#!!M<(^e7VXbtgS=sMDUeM3WG>}_P^ws)6UPVNW`!dbSK27{$>sx)^%Q+nv)$=m>Y{1!*jb?X~6VYYTnvK%UEVb#BS9b?kN9}uK$+26#41));;+p%pUlf_cEy^CD#AyV&OEGY53K>Jwz`)sB)t)9x(lR3s4%mv{_QRPpl)8x}KnjG^Pj&xaV3c|ErSM>qWYgTy*-v*nZp4DEAF|Q@SiWkNdq1aRe%RXIMed|TE{B;{F!LWa@#}FSt`60&iy4ISGL>++M^m^8qMvM)e+-JPeCp7xy|g1|^Tok>WU3^~jL4vI>=|6Mo+Rr*p3YKFzf-T3&;9Pvu~W;hZ_c3f3)vDn1sq~wW%q2?ZISLLnRn>ZJh-2R*9gYZ*|1p{su%r!(cqgiQ#QDjC_NY;6F%%EW)y5QNp3xmt~DujOuY&uk!}ExsMSc)@Yhi>b4*Exhtl+qe_cJb`88kkaBRCu_cs-4?>@Y?6{n2@oxo=c!*pAd4^jV4q>t8;TP~Z-d$aP*c79ix$=d1qh7xUe3#m8pk^c>2fV>B8p;~K<Kp+vQaqD|urBKA~agm6!#}Xv8xuBAuYv~G>5ngY|Wm1*7SVjEpDqYVRRa6Ebz6nxmWZS)p@U#pcjfhIgr>cbwpk9<zE&e@P=Amj>Rf?bH+s^i)+Dq<c61bH|remSviIDY6wu>0?Bi$V?Pco8#r`^+n!ZtltM2;##44uTEfwy~|GEQDa*0pI=2H5T1!@+lDOZc?(xHjA)ySMRG*_&1q;c>&bq8%Cctu$?Ej>?8BJCsH+%w;64E2|kB)i4Pj#H;3#I_*m+9mOUil~7)H6WJV;i~;GTkthowQmYY6u0bG?DW7jCmmSG!p`LCuUKdc|8!AMRJEQ9lR|H5^2s8_?Y3I812ed2vVo7_jiF(uJB*>~eB2vb_@X27c<Y_^6Z^0G{Cwy$F<iirTzT@@;zFWVU1;9rO%8-D(%YZZ}n7Vqr^;O6($n?7If&G7Q4_Iy_6h2oA;W&eMa@mJm0^;{h7z4$zfdaLmXdIDERHSZ*F+I?A2W&o=8iZE5=4XN(E*RA{@vRgW>xYtR!LH<0TPC)dk_sf}8YNJ2cHl4stOLL}B#i;3LR>1EBY#@G{PgKp)*|1YuD<FQntprw6|;W>)ZrI$K~tEOL__*DLJPI;=ZExR`V-2g1P1a>T5D+~W%u;5qzVWH*9pW0NQC7^ATYpxgb;JEM9NqR;2GE6;0jRj0#s_e^Rq>BPWJaC^GS54%~cpheDB9D!UA3RJ*_DH$R}BtvX|DYy@3@>C~C~^u@8j^@xZ>P3D)%gi#=5G*yWU|XD^6mKc!-sGDM7!`;-hXS3PJ6vTK7F6}Dv0M)IQ49A$JtMxsMJZfUvGocTCgPj|TbSL=*$&#(Gh5dF!aj!>n?c_wl(l9?qhk!Al=4l)?_2-wK20ZAVvcqc0|LLt%$eDwamxJF?5$<jZ3#=Cu8Hdym1Wvo8iAUX*<O&%@|T>fsC&Rk{UcwTh?vQM{Zc6r{GO=Z8$a4Uxl3d`u+N_{<*SJkrCwLZPRu*hjxKxNx>sH4ggOVyMvD@7Z^Tk3B!7a1JWZ5=LC>AY_Rws4-n`>k(OV}o{YH=A+N)VhZ8vnKN@yI#Q$q=#m)CKr{~J8+$)QHy;}6FT<0vyZrc@$b>a*~y!K+e*Z|5(X_aeM~~ys&Lw1#n)%=-k)11e_j3l@#6jeoV~HG-k)92uM4^K^3P7+l7j<|j^#%g*OZRoj`2xi`9-JuLh@6@iP?zYBdgxOR@%=hFN)EQ(XOMe)n3ePE9p-CJoBi<COOYmrJ@fy{0c+Ur*wx*1Hb;UfnAI~U3`4|{==D9!bM0GbT_NFtZ~ni4<A1M&375(Rcy^w2iJm*)qwsVcGdB-p(};)QE)F0sdb>Ae3MBo-=DwRS`D9@VhuG}x#;yiyuZAX(p$VhHg|T$pmP)PT2e=YA?!{b_mOn<#d}hgj}Dgm2u&mpvk*1@%KrMToa6H9<owOa#T#!>yYf}L<5gYkDz9@@*SNMWZw<l6bzD~^81+`ryN+iTWpFsELxj7xxMH)%I0|pc%iZ6#D*7NqlQJj!&e=qk!ZD(A8#nykKWno?S--4j;@i3UW*kFu^Iu*KSrT0$&4t8ph&l~XPOI&G4(do44m!gJVFg1d&|5;C;PA4Y)SM~(soKg6M%5-SI<Gj<-MAeYm%teYK)O|Csc*LoS5<4V?A9jk)k!Q(+X$;a()1c^-t61F%J;zCz5N&V2#rwK;Puj!Wj(E>dc@T=HPn+8!>_dtzp#@yD(@c95q}w=Ix&bwv+is%IX>=mj)E62IxjmfrtR){(h2<MFWN7U4iV}qP3ZdVCVs#DQp}ja@v}Cmg!WK&M-Ct?pPrpac#SNxk%5H186{NSE5dUQ0NTB;-@a8kRiEQf3c15SwL%4IH^k4pZWMiX$Y$<1)!Q`D2DP@~w`wHlUyh5*-tlk`pM2ZA49sA@@=CTfY*%|JDnnWBavaRyU7=O(3p~2VhE=;5Xfg=ihL~~$ZcEY;<K+<FBXY`hBxWmmk?*XcyZwLy*n788|87|3p3|VbYBsDM?qT}DF6#_A&Us+7%TkRdtMmNLV+Z}_jlznnNB16abpN5J>qnoaL54dm1ee!oxAhY26mQ?Fsz2I_lOy&#xzWLfVR;2<|9vW_b%@Kn^1tIYetzBuZ#1>c1ys2bZthR=H@+YVi{7(OuK#5>X31oko1#3vlPxApG2&}$Ul;pQEsI+0v~*oW5BTB2N$@f+x0kd~FTv(KeeWkNylS7Z9W0|D^Bi8gS#@)9Ed>{TZbr9DawP5M|B%l4x6SQ5#&K)ql?f^`?}ALh*VL}{9|8GZPV-PTpW&^g$L%)1vebS{&Yg|dnKrv<I6Q8v!xr9-WnbWhB@VSJ`ugkzwX^%Y<#uoh+6dWY_5|z`GG1*}-=DetV?vTLurFya&;Fz@=-UVQZmwX!pTAyvybaSvJ~CE#^ZxP=yKJK!dic?=@Vo6qO?+I$VHn*$ec1;MHE+Rl%A;(4!b{2i_%?p6m0YTMGUB_@9zQd8nRvKIze;fUQVZGobd=x_lByQ2T*4;0M3EA0eEYu17yQW))9<z11GYTbf?Nl)NbQa!%-Ohp=;CBKCP$EroXYF1JCyRC#qKk_;sX^hdcm!!bS(c`zZpODuj3@grMf)!(|k@gPW^`NqBn3tWfEU-t?^eBGSf1S==iTCadh*BByS{c_I23F<LsYB?rT-)w%VnwA51Qq{M;@;2$0kkv)y5(A}U4lt&!+I6*Q_PGBBmL7mro<JW8O4lAgn5A=_HVRfFxjX4Qo+-Pv6F8txXeNIEJnaG=)!DW{ic9`>Vj4ieKou$9{N!k@_7nzy(EbhX1LBgms-)bhK&c_Dd4xv4y&aqMc=lBjRWtyD=?U<Re_#KgG2VPg(?SY;k1w^W;bhkZS-`mA3dvdPYfbyR@wgM`Ny>!;{oP3A~^)uGus%yjyb38x(921KglQdFH7{HRWXT9jss5wxdbrrCg!>yssrQ-f`r?OI%5;uzvFw=)2}<N>X*FnwoAXkltfH$f}+wtIz=f7bT3R~!ia0E0>M6O!S1dfn2X+$)xz_Ym)I;!xsOpk|X7ep)dNll`eMv`C)RfI}e%SzeV6d@qDnTdzKkCR+8Em39JbPq)HrsFw8kby8xw)^^S{(WBb*?7kteHUkpK%hz!<9b;q0=N*r#9kV0|H*W^tI9+AX$Yhgv9a2P^9Ge4pmHk0JMD{dl>SMk&;NN+hF^oMSyglKIdgy{y5hn*7dv&I-RDACz&yq*qHsG|5=s?#0QFY2bnD_OjbnR}2)gQ-j9`)IW25>nd{}bUPS6olRTq>5up4g{`xc<H(ZmO?8Ea%}2Fo)CfJ=1WZV;yb|RvN54<a?77M;w7NrLW)ml0xH;U~-*U(?V5?CJXZny~je$QfMtxIK~)fox9&brUwsOlF(>m)KUkYrT?94*n9y;{0NwxTTTT$1^5m@7E>D;!kiWHOsD_Wjt;*`sV!x{JI~~`Zf-x-_nrP%^=J3@-eA>2sX9aAmOafI#MW!mVVUkc)rd0&^MS{cJdtve`+Ir$8~t{lcANE%wFTXSWvU0P*D`>9?;Wtj#e}_t!YI8|Q!lObOiewr`=rzA91+0VFXh?Hy*M?eAFByh>dX43^5KV0026bmB%A$ntJwHMkH#x0U4G_SNr91yk0O0LUQ3DwL|<L3=4lq>7gm*K;8d;vV&SaW9MBP_DgqY`_`8%O@YjVWRe6?ZRI3)M*?ij=o>_N`?|L*CLJrN{V#lLt<HgGD&I|lFVjXH(*3N4P@NY^|kPug=Yux`|ro5nMs;;E@@mE*SAQ`#oqVewS1Mz|Tb=;K2rx;j6QmtLT1HpXSwY~N|(!=i-vfawyDf`ym0I_9XwPnbihrWws%7^zBy0tEpR|6;;uc~`{K_?PO(BfCBqY}{De1#o70%5X%eBntTVI*k^R^+_NjRO6it-F@~+TjwiEfve@dNw?mbiZ0Bq#y9d46TKa+$@f7F1WPhA|qg?BOaV@)$Ap?uC>PBQe5E=TFPZ7nvT=8$m-6B(8(SDaYEj4)8NWX$w}S&Nx*q=mQ>CaBT0?>-GX^Sq{Y{4E5i47-jJeS<wkwgG#M>pFqC<Jfi^UdD>d^7p9tsT5)Gmagvu=UymoK<l`iHrarDhxj=Eda>tp3^;$q(n+wYoVo-&rikEeYA>6qw#^ZnpNnL<F?8$-5Zk8$BidueD<leV>tP~e7B*~s%>&V6Elb87gwEXeZu)4Xp5Z(@D0uPIgKUf+vl^7U&3PU3<Ug3Lza5?&F1CJk4YtI(y~1GR_7DcaIW54l_YhrBCBOUW?%T%7&#t^+-DRC9^2{fDExe2X2J`47f-JLM_+c!2k^@bNx|soj4#WL~|ka9_xro@xTsPrZRCq%z6EFA~|R!v2{w8Sd?G>A6bFJszED-1^2c{94+ya+KRW{Xy9qRb*UU$RCs);L<9&Qst1{gP;F)H2&Jvb^(s5Fw+GvX?Pz*tQWWf1_gmlF2Jjb&bXSwm@K`jGNNIsEli07mqd(CKmPgY!`ao@gC!D;{|h6^Lgx', 'offset': (1.27, 0.26, 0.638), 'seat': 'WholeLowerInspectionPedestalTop'}]
floor='WholeSharedWorkshopFloor';box(floor,(-1.65,-1.15,0),(1.94,1.18,.085),0,'Whole shared floor with wide open front approach');FEET=[floor]
top='WholeMainWorkbenchTop';box(top,(-1.40,-.035,.76),(.54,.82,.825),2,'Whole raised workbench top carrying the complete original lathe')
for x in[-1.26,.40]:
 for y in[.08,.70]:
  name='WholeMainWorkbenchLeg'+str(x)+'_'+str(y);box(name,(x-.055,y-.055,.065),(x+.055,y+.055,.79),1,'Whole workbench leg from floor to top');LINKS.append((name,floor,[(x,y,.075)]));LINKS.append((name,top,[(x,y,.778)]))
for y in[.08,.70]:
 name='WholeMainWorkbenchLongStretcher'+str(y);box(name,(-1.29,y-.043,.25),(.43,y+.043,.34),1,'Whole low workbench stretcher')
 for x in[-1.26,.40]:LINKS.append((name,'WholeMainWorkbenchLeg'+str(x)+'_'+str(y),[(x,y,.29)]))
plinth='WholeLowerInspectionPedestalBody';box(plinth,(.94,-.075,.065),(1.60,.61,.615),1,'Whole separate lower pedestal, not a lathe extension or shared mounting bed');LINKS.append((plinth,floor,[(1.27,.26,.075)]))
cap='WholeLowerInspectionPedestalTop';box(cap,(.89,-.125,.595),(1.65,.66,.655),2,'Whole lower inspection surface carrying complete independent empty steady rest');LINKS.append((cap,plinth,[(1.27,.26,.605)]))
for name,lo,hi in [('WholeLowRearLeftBoundary',(-1.54,1.035,.065),(.44,1.14,.48)),('WholeLowRearRightBoundary',(1.03,1.035,.065),(1.84,1.14,.48))]:
 box(name,lo,hi,1,'Whole short rear boundary section leaves actual service gap');LINKS.append((name,floor,[((lo[0]+hi[0])/2,1.08,.075)]))
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
FOCUS=(0,0,.70);ORTHO=4.5;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(5,-7,4.8),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
