"""Whole purposeful farm preparation scene; two existing models reused exactly, zero new stand-alone models."""
import math,json,hashlib,sys,time,collections,itertools,base64,zlib
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='agriculture-whole-round-baler-and-twin-belt-wrapper-staging-court-scene-01';VERSION='1.0.0';TITLE='Whole Round Baler and Twin Belt Wrapper Staging Court'
DESCRIPTION='One new whole open bale-equipment staging court scene using the existing complete open-tailgate round baler and accepted twin-belt-table bale wrapper at unchanged scale and material parameters. They occupy separate side-by-side parked positions on one newly authored hardstand, with a broad open shared front approach, a central empty aisle and two short rear boundary sections leaving a deliberate central rear opening. A low left curb and three thin contrasting ground guides organize the court without connecting the machines or blocking their front draw members. Both machines remain entirely empty and unhitched: no bale, crop or loose film sheet added. All component geometry is embedded in this self-contained generator with original source hashes. There are zero new stand-alone models and one new scene; the baler and wrapper remain reused assets, not new counts. Fixed visual staging only, no bale transfer, loading device, coupling compatibility, vehicle movement, active wrapping or baling, actual working clearance, engineering or safety claim. Rigging, animation, physics and runtime interaction not made.'
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


COMPONENT_SOURCES=[{'label': 'RoundBaler', 'sha256': '3cf594034b88bb89ace19566c92280d9722a310fdc6f9d230ba4386823bc2075', 'encoded': 'c-p;veRI>w(&zvF6xws^DM>_D?7RUsI<)};q%J2=NzOU<K3<ngwiR1MmJ~^LVko}*_OE+JFSZk4_wG_fBF$@0Pj^qhjq=-XzkSNWSs43~aX(L@zz7y;u{P3ha=T28ELq0W_GIoa#zAI`{V2#><6}6R7xw{v8VmoHDz45xz8hVh{dIo!ci+ehzX&IWpQeGI`SBz$k~mtszy0=GD_o>WhEB!Y`I0BGGxzg(6po#IojXOi2%Je0MZu&9lQ?(6BFKs)iSpJ>mMn~vdQn?L4f2^@TUXbom)9P8y7*z){ZD^hd#JKTqnj`aMkCwJf;@><ROzOE7Q{vC^y=#D+B5xG7EYE?vCM)tuf3h5LEJ9<Fq-*A&~7Zg?bEYhrOkL~ce-Z(ud~am^G_F^*>yW^$LwF9Uw=IF%)c3vpJ+7WT8(C0Vl?B8LM4r6d=?zP#%N~i?b+3v%k$6IJlv-^Fv55m&<In4I9eP2vY01XFm3Eok=*-ZdJ{+mtT4{g5DjSq2>-=0r;!ZbxCtMqa2n=m<kS8pdEgqS#?3N{j3~J`iu*7oECfMh++_YDU<fBkyb3a+j+rsd{Ci^@_>0`gmnrXnZxnM{0<}-#!pMU~I9W#oHDQ&gN#V_*K^AEg5C-ya8c=Z%+~z#GFSBPvCdOo$tq8n)9-zbzb1Yz-ENPb5p!o=8lPt+|BFxw|&Wjw~B83LknO2S&Ff^@*dSoD`j3&znVGmgHl*TURR8`D<AY~l+v;acN#7HtDh$j&@0w#f-JYW<Cj3GjQ_?1>l(<<(mX3K?f9~Sf48WnD8%N$2bLJzeV8$}RM<2)qrX~RGUYCH3}A7Ktb<toe*;<M{{NPCwXaZ(Vx#6}T;Pt4)Rvt>j$i;{TOo`Wu<fVRm<iO_);8Z4znBp4pkhD1yZCFY&@V`CZs)@je6NikUn8kz;kA}F#o&lud-N$w^A!l=AlW(BLDVxQodDLPaeD%-!W_EK$;<}GRy`OM|>Fm(-(`ywH*jITkK82KcKgWREcmzj~I{@pTw%%E<cUti)W$U;BLUE?AFRis#|Y}u8_9$M29)bW6pR0#ppBRm>2-hHBH8ayC)AX9`weHJ<nkAnp-e0fhnNe(!Td-+)bnV~A@YhsIKL^CcDDOvdO@`lDDnc@(Z{3$hBQX#Ql!8=mQ9D*<RZvv37pZeo43X8RCT!u4dH$M&q0-|bKgh0oXu<)mWYqs8d-@f-ho?ra)${P&(Z$4dIpT4=~=l7?d`S<HjmuLL&?u?`z{XW0AI)8gMx<0$&hON)1AJ49@&%A+U{;?!_xD2LO;6Kx`+@ll6?H)RA=lQYIwH^2Qfzz=a%lzBV79W=5(|CHx%!Rhc)E4az%BF7T1scEgv)jKRQqZb%d`#sh`0<?Ez3j-4?;vhyzz=>ly(d;h<L(O@u1o(9WJo}BU=Lf<;KuN$Q_FY8b}tJEjj>TIi6*Uwy*1P6gR_Rb`x>U)$mTBja=fcc`-v`#WkhfJW|wEVbYYn)EvHG*7(8DtsNEAovmmQ?vHU@I_-s5l7`A=-K~LSGqn<h_>qxDmp1LUOO05hT6Tw=32?7pSH^0jYOMvs$%*!||>dknK-F?+t+K?D8teCdMSvfZjjpUFR4eVaaSa}1%0<*bwL*!jp54Q8tE>V*5V~WSsuz#aF+;Q<8if@KAP!cT{fd@nZzSZE47BX}MFL(>-jeqZTheO-mKQXHQ{21bql#5wlb)6`PX@+)}7GQ)oYV=o~UO9aR@kmmLTGavRD>&NnyJZB^S&(}*6~ui*D<$@`c(*oSpd!7uch23Q+Z*oP4SHRIx9{h9fCDm$tl0Cqd<^j518Yp1F+>@L;9(u`xKz8O@+@-8rZOJ@sc{6p-@8HkB@fkk<<Y*p!nzd?+j5}Ne7yBxeiPDG6TQ~<!>H|&qjs1FCbYdD;C<*#!wKz203k=1AOi65o5_G>uBYk2W1?V!fjG@a3p#eJC`r;Bq!N1oj$c8e{S|LEzdHkZ-`*P8%-E*2ON~{IfUSKN?}eK?PmPI~P<UGvHhK{x+nst}Jc|g+{;#-y<3dX%TDER6frFo49P4(EC#;@Akd|T^LP|^hV|MYgNkk-&Cea%6O)@W{lW*#SKAcI<Dp}ZmW=%Bf+HI?3V=mWih=QlN7lnCYRqNrgiL6K+g4_m?1D%yLz#Pvo)&^aoqk|tzo&3NAO3XpixC;3e&3Zp4W!b=FRAK*qs4@3N1`A@M6KFzQjY^tk;?c|COPhoh9;`1wsvcs9HX(!^Lox7&0?1hXo(%0*9#M4nphsF}5ys0v_3-1h1xnUEm#W7~{k|RAzk6-&${;SC6@fSqULyXQ(9a3D%q~fT0K&+(e1KA0-kPD^n3<4UQUli$!hxhTNv$t-e@t4<Ewu}xJm|4fW1KQ~lAJipvLv(2izII6Av7dX6DD)g#}b$zCZV@BxKKAxWcL+GQLWI@Ly;|~!DubqnL6u^v+g!z@Xv3(lgg%-JDw`C(j1q9sD)8eaOl9I)5`hESi`9`;Ms?AjD2Of!6IGp9OH;-Lvw)LyK$j%(IN*5g|riUu`{Os{$6Z@ynl`zLnov@U+^DLK5`}r2ab~msf!Y49&VmkwMAhKgDAm4IuGgRuv{q>cDb-Cg%7H*!-aG<4Vy3wtd4Ww96~p-j+|rXxpP8K9j8mrNAz^yoKV>zmmSgb0X=o8{d4Eo9@gMz@tI6zSYRwGE1lRQjfd87@A0V(6$WPqh~~zlacMRi+%nFsds>YB%6-Yi$zXKs{!;qMp?dF7FY3EmdAeXpcx6H94F*uDQU^bw5-gqU86P8)B$xA~@R!fReUi5h>Q^h>AP?h>26DhQHh8FyAg~=UNqgvR9UA>d_gHqBtX7gfiZ5iR{f99B|Hm9wfgNI$)4ZN%KA4PdY+E7AE`)3dw)%v>!Zi~Id+b=g;+n}Xa?Ka!8RDI%xCZEyGv1G+K1=TNZOYr&rvdTO-Y&}cLL2X__jb_)R|)rh*`f*NOef=V0$}(A4FKdQjBgp+gfcdK8sd784wVA?!1k{q6&!#M9p|AbMeD>=wV)lX&G`@GBDjCT+oGLf3x6^v3!9BmSm^4#w5Qz``%{!t=wot!EyJ+ehixCT4-v+#9INe;iPUzVlL2&iOq77vuG{I5iS^PZ5n{fn+u(2kgvD~o{=12vWosCZ;=lol#UP*5oKBmTJDpB^OgazEbAHfvUy%Lx;&3SXoPhtH2P9LGEL*Yc_VOaLZtebs*FEV^)}DLxqM!Lw&pmv;-z1eZ+`p*F9P8o1nGn_Z(`Vc5_G%P#K?dOA^QvJ<VA~Bh3GG4=8q4#CHrbHQ!yf(okrZO`J8+aA?}n(Qozv5l@ae+?2QL}yfGwArX|uJhDKn<^&X;3_yw8L@!5Uf6CE_6esf}X+z9T{jR!bWXK&w}`dqQHp+I)e5`iW;J#n7bP#FK<ziQ#|oQ`705*nMUjOc2wUJl=7KIK_WZP+b$Ma+Z47)YAu2SQsY%0mS(7hzRe60;%x^GyYJcNPKht19V854@5Xl2rdRQC(aR?G!-~Bwj%eA40r^Pen^M9?-S_68a0TIk9d4QSU6}<_PZpz_p|An(&PCy^Y32={-Uu_j6-5kfGx*+yX&4jr|DkU;@zlo=#7jizSBh@?oj0(FGWhtQEoaf6oO)nAD-=yXR}*?KtT%*{_JPK^i@H8ZE9GK*r}qQ8A`Xa0T$ba?U~|bBb9MLL@9$%C*jBDQ-D4S&JVEKsR8UBzO*54-#z6=R<2=)u;M;puh=Z}qc-s^17CA4yDi9}gO~luSFcOl4tW$VbI(0_*`iZd+h<wED%VAij$M*NwUf=?v&L=T7TGiTTGm1G)a$my4IRkC7ETn8=CNd2N6RWw7@t+o#F~3em80s?X1Cj;{Rmm(WV-fhxc}fsHymJ4@dfeY_0>^`)^gAhF%jw0|Bhq6gY&)a!JpG0#^b1GK|=-#A`@{?y6o?LwJivqi0>Bz(Ye9|!gH6*K3UV+4vvW~kB^_=Pf+|x^W-U)saHt*{RZ1z^5;+EU85ydhd+UIc#MMqzdAKWVNwjU347aBl%pgw5^#j?TrqOvpfyV_=G9vd&)k>KdF_OGP$ZN4DdS0^OqF9i%**gcF8+Ig1wlIY#4l7_1QCHENo!$|RvNC7!Xs*CqGc@DeWJ`L@Z1+CBt8mF`)SYO#-tzbSt+~^`qi$n0eaePs_*LhuC8ZR;Ce^b>>j9UxVLklY9d=WXFy<DH9ul)N88ml{t6>K)(!5XxnE4?n#6FNUo!IFFm3DDUCBt?dYh9<f>AriOt2}(RA?)posJ=}IDW;Pv`^a!E?Z{oZtEjZK`P{o_BZoabj;Jb!kaK4q1)ne1@E5-i)k3&fDAsMR*r9Oh!gzzq4SJ!jsv{*LZ`xu#<3t#wxU!AlzJnO5Pj9v2_9UCyJBj+v;1Z^nhN5m?KA8y<n68=za|l6r}X-_<w42i{|6K`d_pRyO>PK>l6@=r;IOlaSk1>-MM?l2k0e9mX>w2UA@xc`(9$Mf?NVeYREf-Zma?e$SSszxIZaDJ@X_J3kfW$O0*`r0<kW~ij{Pi$n3&vF=7>b0nS9>TkU~9Z!o<^sEz$v@Gx^kC5v1vA1#oA8w9Nrh9fbozNKQiiL4b=r?51<jd1BK^H#j+JY`Q>uC5vtDH~WEDjYg<R)W)MD(WIs1m>_>ns;fTy>S5df2vayrVr3@PRMw_O2F>cE+A~4dLxmh!Q_W(3jzv6p1jEr@_>553*DHFB?NOURdnC&V8|o$^YR4zGyu3VNg^BpL`=V07)h4spDs>{Yz9NAt-q?o8vfy1n)S<3*))qobJU(LTJBy1j)AE7CrW~L~c0f$DnCqia6tr=&3e?PfVS!l1F%Skuv=%|vd!Gzr#i6nU5xFeW-q9R?VG7e35D~t30sY?wJsuyGkB42yefdH^l8JmGEl3%E+2u#{qsJjOjF3kE8;83NxmOEHIEv1o3znd^!lG^iWMj63nqCA!Q~BKuxE78C-4UQ;O#Y=}?U+|5CuG6Ghb>72xh7mqB;@WFVn78@F`#)-6V3sElBLuPS22zS2WOLaEXd@;=U^ZBVApK=y2r=-vd58KdTA<HkoF%D?N%C=3h-{2KTQ0X5UvUJ<aUVHN>RWDPC_>5TBTuVHBwd#u@v(OnCQeK7Me88lH=xl&a_nY;mMN#4!`v)Z?f(w^8G1Q@e4B&0JpV2zscbpsw5kds+$pWtA5~-sW<s*%Nxt@VT(5S8tSo1=_s&~Z8#U|l5r9spvbudV2(IhFbdKvT!clq!tpW<L$_51;RY$AVg^LKcUOM2405YF%w_{qH#LXD{?&)`ch{c87}^$%O-ffdtb%~5slB)GA0DZ)_YW$6<Dlb^s<ubV6p^+8Mz1lwryR))#A6_~RMLWY?RIuZi(G;??CmQ!fr)z!H+MuF=e05T<xaiu7|LbLf!liTA+Kjln}ixpmgwPaU<zH17PKIYwppkK7j*axFj6jh^t{z~qfB?@1cSgQjV~CD{XCqEw70MfzB)w~vR<5f7fH-sOBD^ygDOO8dmdij6D5;0TWMlR6Vf^I`mSyhj<gw;vFdTI$mO7-35;pmuMUFt^KyEG=D6`D0deEKEs|4Xct<qICS8?5RgOE80v`tVqkKX_&NCS=rTrs(G(kAtQ4S1kfU!%U<hwQ)ER&qWz6fzOf*)qcz){|hJn$tEF+iTpgjq02$o`G|a6ziJg9%4GAx8m9j634M8S!i*w%$gZc{h@*qY-BIAPDT%yH9Wayi&m$w|i{&KV4pb_~aeANBzIgFNqL8oWJ?!#o5)B=XN@slh&KlKh7>sue@(&F<&mmF=>@%&mz_3#5r<Fc$;^An-5zmrK9D@IdG4p6e5%g4|%5NQbyJxx9cDhg@Um^x#f~t$9p>3MbSa;_OWxw6U{PzEmIxd?Wn;>T+u#sbVVLU^JEzm1tPOAcEP#PVgu&yeOdnK>dooLGeW|5NYvLK&o17cT^gT1oL-$F7^Koa$LZP`V~->`6g#;r!YJ42p?|TKyiw_nS92ncKsS2**N1C*ZP8$ElICtQ{zBc{Jb;cpVoGN<)ibZoKAyd~rh|W@sie|b%RCs(qJ-$cd*{=MBGO?2N@v>?y{3NQyJhm4-P<m6Nf#g;#9G)bPJ#2#1TkvT-CQo|^G_F%y%8}!bhzBj*Le{vJoAsU>&x>u=I%B`;lYRqc~;E5t_)ApAqml?!jL92-~9Ux;a&HitS2OV+}sEI<Q{F<Mg{3QUiW#cQ3yQvQ$NK?HsY={yP%}M)o>cb2`NOn0i$fij&*6u(jfBJq$TxM(NjIuim4_}rUYz#LbXU#LKGx<SZu<iniO-g$*1`UnTVeG?)+b8Z_S-8yrU)p!-YQ!DqM5kv7``s=I4v|8-r}LCW|h~)SQ>^U!QKYrok2?Hp(S=S*`f&U!RE{&)$-#knJ;jdjE*eWY5eVZJJ~1{V;pn)iDK;3W-&5h3=|qz;#3FqfkenGK#CgDx8*Obwm<eg2}Sj>>YiVJh&vj31=3LHgybCi`hY-wRP>H(E37uOq1JKc$_>RLCtDsV?N?mJBfHF8aGIH1EEim@Ft!grR5stceRntfN?XWy_k4<TeM~{@jOj!&P1oIOj<<UIl|hdj>UxR(1AFc)8SdLcgs-uX|%-)Z->B(gL~HD?Eb=?hBr5|L>kBApHx~gHICGN>MdNnjv&VQDR*b20hymkr=El<f^@I1-oAs2#SP<hS>yxrwVwyZ8w_X;Nn+pl%cvN!LZqgtnqC6@ILPy@mb|c9%RjKhD4c9H<h9oto<`~1-)hx$YfU%?w+QnbNxpyc&5ErKoqC5e-S~>|0GYn4Id({gap*{?A0{as`T_NXW(aWw`xcx;90K1Tj=WBb^r52KG&%5O%Wyw|O|3IHzd7(Aw-_AORkf%u6DiBiY-nLz*po>yFhOI*D4deM%(pUBF)I(FX_!fWsx{mHHdUokz-sCi)iZTSz0$V{>Lv7Wvr-Q0hM3YGMP2NRBTe*5iLD~wE6OD;Nr%kqkuo)#Fw+Q_MVdBEh?_0$bh$`#OL3KxleRIs4c56*3~3<dp8j|Z@`tWd@{uyJR4OPqC#bOwX*@xLZvq!O&L~}@-fGxd&S2<J0eh9rA-7$oQ`pgVKiR#r48h`uTbR%Q>NbrBG_;H{@i&0uQAkZ%2v{6j$9Pf+&58EZk0v8PHA3bw$pLG;P^qS(Em3EmO;L<fB=u2f*Z}a0gMc+G(0Py6R*990=*8l2ZklccY78g-EQxcZ-{_7bT)BDhW+G7-z;aB}84xP<E7`HnU=`E{vdQXc8OcB-cuc4nA(Mm%f;!4mpZ8sZM@W?ISIM`DK+CY!1||R@1oH*lc<T7C^Kx~<RJ&UlkDY!6&SV};Zkg;LJ#*Y3z*PlWc-3A}V!|dOpzS@qw+Yh_75Y=o@r6?(a6>wI{5ZTpLJWpu8=LxZma~n-YZ}pII*=S>D-UNeDU{3}wQZK+r6p1{DoCkv8q9dk!X--dUsWlgNW?N!*Jdxfv||CV*I@=H5US*A4C-|pS{U;JHA9-TL&Y_;?y*hy*bJK(*Bk!LjM>mqLz`tEv-kLLFq?oHg{aZu(Ch&qGfrZS;}PT4>;YJlASKoXosVi0Q0aF9jW>QE01Q24|G4jHJ3lLOv#6HHJPRL2_emB_|0n4=Nu|{&AhnPo86(c7qAaq1umwYh&dnOdi9|FuDRB@^tp>FA&>N`9<m$mhX5w@@YXj&FFo`v36}DYDAS!r=KZ2L_BmFue^LI24i`*(3IH@y*oJQ$(qF>nz4$GkH=|s+caKO(<RqoGKTISRV4nWt1hl>$G*O}Ym=7h(EitSfhDbr!R^1Ay}*UxhvFvWmN9w5(YfM?XAf2Ss(lAw!(MpRFoJE>LE9jJGia;dVc6^}IDmV2vLUU#o5pr_}ridP4n9<Wg6I#(VZ6iXhTT+`#db=V07-2KBi<^AXMunK3Abntmy%t_bbT|YVEAR12L(~GwTbl9MsA^pnFaDxg%y(J<EC%!oO;e-WyFa&%R5a&6c{%}z<T4*%a_>;7u4AEI*Li(Z#!@I2t81FF>wMnphk5Q&9v7ao0nNM0-=PB~wQcrFxrKB}5si=nuJ@g~r+i|z2AB{JP$GB|Nk0u+%6J)j1JY=nSk^d|jKZ_=N`u>uBM&9<b$lsF=K0S}A3&X$X9Z1xkxFkMM00?1m!aPYyq`cjGAXo0OZyo963j&DuC=4ntDK$Ly30hs`ZFP~G^%C)ggA;@m+><W99d%zi?!h6lu7^Mtv)j{b$r;e)95nzmfkN!Ufhsqe3g<;lcwsc#{;vbMRm6GL?JhImF_V0`7;n%eFuOy2tqKB-``qtr42N8&Y%J%wvGYcOWmYt)i5^Lv{<<yHj@(0kMijW9!^U*(9X*X=EW0JlHX?n0${aDugXpFR@(tT9brP~G5Qf?Cl2>l$8r$Zgun<A=+T>EjR;?Nl=zA21>SPr4((K8}sCtkN9!^Ij1K1+#0kLF^Cso-<O(HF&1s!v(FYMgbOXM&@=@REi0(=h1eMN{|UAe_UU#TZPL`!in+4_>E=fTG<EA@wDKE=~fOjWcVE42rQLr3byyXs1-x`8mi#ATy+To#ve{|-lS*Rjm=nC!f8YVb-;r(B{_HU*<&jTMghXdH2~(Smf2kfCx+T2HuGE=GLSG)%~t(PN-l`2zhx5L*rDn?2t#$E12-(^PlFQ6oQ<nP}et#dpL%`9|~Wh%F`~4`v`+Lv$oVUA^Wga$frQB}vg>a{w20$#k0(km7#s(15BHa5gpc{DvY9WxnC&HzE86i6~i`G5kgu2A1@#aWW;Yp#jlB;s`1o2T8TG)_{yVmQx%hkaGldufhe!cr7=iquRF-*tT`~%&Y9qngYwD{?%EgH~`5WtJwnORj;R26Oid@<qdvD`Pr%Z^e35TtyW0Ep`V?h?W#+dD_lmEBGCpA?tu(U-LLJhA|)kkxFV70lAJpcLe1Q-&z9-$onGzA)3?$l1w9Rz?pAiCQ?6D+$HbnF76(LcnJa$k{e$n7{(w7D|1jRkeg_Yrf+S59$t252D9Tqy{4Dd+x!kFAAS6jyq7EDkP{f(b#^4Ud2vf^_+?F91bQ>3Xcig&dsjF>#LgVfbU&WOJ8~2O&757TU8}~|Z2iV{|H!k;;g{tC{xSK*pH{VSe^W7BeFe&&Rx=4m2r~<Qt`lzO-FQ#D_QttFHROQfr9tywpV8%4}6ySGSwV>m|hSs@N5pYEwdedBAx$6h?7U(y1WiJo^hZlrBz^C^d(a)T(3&}ua$V~HnYnr#|NU&K8LC=j|LABu^HW+vM8epid|H-wN@>=B3-n<-ByD^DSHce8N{C>dkexuW3<6eoA@|@tSDEcbBqJ=2IEg5D}<4)<<Sv{t!Z}G7<bcebn6*}eHs_}-qLndyj@ZccWO@RPwPqv*!K))#%)J8uo5(v<Nz%5GY|AlR&wyETPhy_{(E*S*8`brYqZ3qH3H$Y9`kGqmT?!X`XYU74GmfMsTcYJVFTyOZkw}B`i(j1Z^*dLE~)Qzc*RJ9hL6YL?V*nE%<dI!S_YC3v1i^ghIKG*yF%s08l<H~)2!G8B>GJSZa$lDufDK>Ph%)yIhaHdZ}oE(X)z)q9<SWy)Cq@)heNqLsic{2`1$;}P?q(C^?cBv;R55Lk2*2NCZLohjX0Lu;yM36be8MRy0)BT@nFfJ!(84bSEJ1)_GN10bjte0D=n`_*9j8;<e{OK3(n>Yu0P~v6RD$kX8vN%6q)Rw)*>^<r~_#*JTK<F0+l{7RdAJ@vMjor!vGMg|F?nl`DBAF&4#Zh6m<O(%Pd$Q+j)L<}_@jYUD*hbqPe(=z-3{$%=R3>@QTs)a@KR%T4XRHzw>C6*9u<6uVv;_>+rlH>h5CDy<Z=CS_xIThQ8H57OIB?NxlCC5V4^n;R0IUGL6e+zbB?nv7*Pv|rzeL9`4}3f{oMAltcieKwg34)GiD*gIVTX%XQW-FU9fKiA27F;D?Y$|iovO4JU9iDCqI7U8KH=5sXc8plBd`Irn+y#f8-PSS*kco{ZE89h5qAyV-J~6=-XqnUtyb2r#S3P)W~4UnSTQFU(F7#bZ%L8x_%JX^^Q{n1LQs7{f;9xS^O^Xw3w)x7WRI99!mh=C3SIg;ML<)9JCtac33<xJgUZD?sv%L@0E>=pPUx&~u^XF6nH;IX)}s<P<p_3bf%KhGup)89cH8chD=kBQ&GES@Z0y#yB3_PAwR?QPew26vojz4lu(uSPLwnethtyVOVEw4AM7nUX0#1&3NL|`d0)^`3uJ)~3Mi}3gXP?J&m1m`x^p$r+{4O`M$C<U@TeUwQn^jY!b+Tzt4L$-9yTv*U+`ItZ;0UzL>$882OuLe<TN9Esdy&9Mn*>w-#uAo?gbM?)k|kSh)XYeOY!Md3issg|Imo9#2m_%m_4z9)<Xu!jSeZ#RsjX0I8xu(GU1`s0zH9`hohqR0)S}Ri3LiV>`KL?zd6foo<A7d`k7QLuRJbdAj7(?0*m$dtdo`!yqN*<=${L&<A!ar=Il5d%qFE_zhMsk!l56Ei*!k(86TA8<4R>O}HTQGBC^Cyn9CL)cr4ja>mG}A((#PRDahtQ6(_~3fX2i|`)8TJtaU>1NYoZB|03q>HeTYL~lyTJ88G=cYO>;{{KkZGw5i_=`WTpM7c-1QReoe;ww6?#E+)0UCb~CS_=0C3D*ZoAC2CBZ>GzjIZM&WRWq_7>ZezK9%F(@|TsYAQ=^_-m57Yp-|s*)@-+6IMVPve^9Bxw&)dy{(VE0JzK_YaOwtXh1%IfA3U*O$;KU=ayBX3w;3mt;TjyhTs*;9(lh;EbcQp_$*QCjD_H;M+5u3%C&|-5VehKI|pB7j!cTZaosN)gg5Zy$U3dt^p9Q)kwndv#7YSbe@KXB=%2#UhkXy$vmnYo3^9c>$J1?A77gehm8Xjz-J9ZH(QepQGchckJb`fE{pUR=<;ScK2qcBsGZ7hDA9JmkR%cx@!v28$UEScU31591kwhz?tJf?WP+GI&H{1Fu{a4$&XOePT$PqGqCq70sZtj!kH1-k>p7x|%mDZ|vDFIMX0O_Knud=?c%|g2Dq#hv7bR7R|A3Nt=(LO~#82aGMthOM#TR1$Ze@`vU#M6jr2UfaB1-&7HHXQQjKtw-_7tPAPLCN8ql(}|C-!IH&0e?klUJT~r5cqEcC+`m^W8DUeOg*v4fDwCHC`RFsWlNE8_E@}NSkk^YD;5OI$YVHRDz){BWPV|%~+^{N$?<6HRs7GTf$LZY*JEjlcHuOvN|Xc1CmQ45f(tC5+fK~fj}%%)^7-xEzWY0BsUtb3yAQB2yw`qQAvd>0;Ea=x(R2ra+Ugny({n;RuV?Ed(-74$f}QRN}9TSMOSJIe58^!6b|^9lAebt?tIJc34C{cI}3mh7s8N$yw89%2$;Hfyz`xqKOpNJ*n8&xqK4|~LE&?@5RNmjC#QX=4~F0aFj_&eOrXGN2pUUx6KSRmHl_-dcfjg{&Ova~HP;DtI15x|w!0~<PC|L9hgHcp@3e0-B@sx*HBzAD?7(3NSO<V{ND>1=g{V{{N4{VCobUcO79-#HSKrhZdcW^~!|>k$cKDTS&=h(lZ6f^|p@hnJ6GZwr0T9ln1P207N^B`9W%ksxBnt=!vjqGCEJAf75E$ZrhTwBkzPe!IA_9_SYpVdP#X3Uiy`L@kQ?HZEC+3~DS78+SxVvW-VSy(6<zXa$<dZB+*-q=#J}C?`6hUV8*ouOWcz`e7m}~m~)f_rfZFA7nGZ(aLza(UNZ)iJ0Zc~!HT<V}HNV5%MB+imX8{s<poIm1Asy8tYQMsWwPtoSnggxD&>wg$$g#5L9x;5G-lR8=(LUb@Pk{iB0C;YEMLQw7DvXRRG5<p6DT@f*%5P=0geE(nE4$$pn>YqO4?Y>GJtXY-PSDkKPo`lUN5BCACKA5FBS1CE3R~><D)io6_&)d+d%y;;vut6$?p`~sm!1mSkW5`|kJa3pUAhb<7){)4GscK@E#i9xJEhV@fi&T#3rWBW<ROGh;TPRQ9{odEYu|=yl+wC}MD`~^{S(Ad5%~r4ksZvkY=Dg8*1J1P6g0atmLd$%A_6gT2{yn-pJAM0a(-A(em_ad3AA^v*Dy$Aj@%7pJ^9$qj&+8ALF3<n_?5%Nqes)Q}F6A!EU){bTM+ZzD!;c_g*2WkH8J{JFUvv*%NQ8<gF&hzlq}Tg1M_F3soiJK4%9Y=>T8q9{CC#awr>k66%6YUZ7`@l!uZik5r9q?%_)DxUtYY-}^3%KXk7r&97a>*9-L5`($SqGle*E+|Ur~^+BDPmuvuAZroB{nmJaBNeTk_qb;6W;>bf9X!%OF?h7w<P_!*g5op*9N_HQ&ect7}QV#fO)3YpV|$x8boRaWoi0^W=V?NLXK<ldycUvs^Q1BYc>JNZohLZ{N!?uC7ln-kx5*^#--8TebUI)g`U+YF2e6YvUr;5OiF}b(MrsFU5Y>@yx6Y3P*m3Q1=E^G+T_L@Q&=<-A${s4?;8vbJFmvCbAqHBPzOa%b(yhnhnYfW;GIjiBsKhV@PiQhgU<E_?Jj>AvBB+pDW?C+Fa+Lj)dW$JA4#Y5QKyM7H20Yyeua%r;~rGvNDEIm2pXp679xC$hZVf6959PGD>~9rNgS4i+Q&;aIe0_QnZP%dX?I*LGz|w^LpMRck*^$#3M99V1w36WtQc%;_4CS*VIr?Y7BoMKK#mN;;6h*Ku7#lfc(TD8r>Y+OeQBM-R^Pl;zjpm_r<hxFrIV+|M`o~%i}{hyGkXxerbvSX2Vj{n8C?WheSeWD61nA5SmZVOvJ%Ps@X_GLT_3KmDhz(&n`f-_wD=lN~WrF96}+t_@@%6Ky8El^p}6pW^3E@)unow+O$EfZ1}zEiTyA8#bxVwxPwl<H}Cy2n6JE&Y&F@{zE8|hma7~GH?XfzDmMn6Tw}|q-S^Wm1h2uS?1S6jba;8$$@c`GawdshikjpHv#4f2Apmw>SyaDUhQ7WuC~uGrtI8cjKiDRnA$vOaOg37o-lTP2ynX7RZ(bCvsCx9^5k>bOt6e`?n+6%Ktq@#Zx6@Hmuvxr$U8-KS;VFmrd2*}V4a4$g(e7(fmV4N7^#88i`t@-iy{P2sd!=&uTVIRhH@^1>jovd)Xa6!=H_2p~>$E(+TrDb0G2+{3-xj-qEsL7>v@~5r4*221N}Mzy&QDxqOt3mn@BPG;FVzsXgJl$Cp2c&wt7bMXrr^rY?dWbvmZaJKZ<0CxHo2VpSavPJGC@uz{*(laO=VpFGa%awSE$=Z_<-<9r^8<lHs6K(M;MNr_5lhGPdakN+A=T0g^AA#A35}T^a3}#VL)$~9h`(VLVTGm0rQlUSJSDlPv8I1PD$z5mq3_jepXlU%{{#9OBk@|XKRm_q09ISE}r@J{OX@(Sw<`L@S|VhchiWP__&J0Fxq{3*#!+1Z@}}0dzoCrQ_1@HR(-9MOsaV@;w#S{*Xi3#+})#JB{+PorTqBDNb*`ZcL|F)pdBgE#y9EPh;tv3AtnUA3v8*`fLyt=NbHWp(b<|kb|13rlfz9$M&)edYNX{J5F;KOslT|PC)^lHdGlxLk5q*IEKYLVo6BQA&F7@!)GyvHdIKwTbm$AFHNH5O>5_3o$A2x1qlz1x+z8$5YOoc_**%Kf*s20<wQE~H8D7*8x@~~qAgN7e+QUjjRD$GtOMjYXR10NbNN*<|tLAx>Kn^86ixWdOrH<_kHgB6%SH4tZeeG+woz5ZwDgLm`s0K(my!i959!EtXG3+Btsa-Jqg~+Y`g9-rM*`kvX_|ak1@@MyXBKd0pI`@eBv8h=LqrNSdQiWN886>y!w^2EWYN*O8_9)S%+UQ&4>v`3)d=hPgoZ;)J0N(`(_b=A_Xn-#n#j^%98;6++fbzyU7E=Q}RdOw=z8PFq--4Q#W`huvrJ{#vK*<@(;>fANwn=s_r<hoJ^O)KhfL`*5)L7`YH;(Lu&MIw!R<3RP5+(nvt!pPc5c&ZIZ_O`ohUckyONDYLTYBDOwBN*`_^+^=ZJv0)A{yTIeIaP!JjnuwKn}9JN*?%;3#~R^eH^uE)n`7p9Blg=?lt5~`s^JR)wQ;A&Waw@hG+8)j<p*gfvkMxM^ipFCVXD;s9G^|f>3kQ`Njb&jYi%!@z)_pq_(5kfoIw6<b!8Vp{CyFdkglR*YsiRaN+H6U({U}G>aHHXxOV0eI??1zj&5B`4It&zbvT!Bkz=LFz?%KY1-WmtG`oYJ!!KKHQ;hY{wLf?wwRuTxl}ZZ9llQmas9hPTvVTbSdPOnV0NeFJBHy@$2#2XtkhU}%=RWDjwk|&O5eWsC5Xn4AaWI2Q%qI!CJXTly{BBwl4>nO=x_eZ->}(jAXCNTnj|C|DYevqN7?#TOVf96)r>~c8P%%Pb#EOz|0xNgZT5;X*uFE0#vi}bT5V}E@|q=tLLwrH)ctCOX$6S7{8o+AF37H^a+R=B&LQE=t({q*F&$S&sye?*P@7*Dp5%2I!jVSJ)Ng)y3U$W);)fbBx{yMAzu3}<JNUjKzKBUbj+qAy!`QmWj(^i->LsMJr)%6GU#2{vr}K8C`00-yP$%ixRPlNB=APJ4{W@;S^hI>6A*oibZqe(f?X!DVmFj-KkmXhfX4$s(4S|jGxg%ZfJ+xgUQx^Uk=vKTWm&+X!pDcTKNfHfP;PRKlkxS+^KV?Q$*qAIJTWS)B8$ybL6)FFclde9$bnmLyE+-*vuqX$7`QYNM!xyuO5hMPa8;I>e{Bz2lAy?r5GaV72e4}>W%7vdb{;DOu?-|K;85)kmeTWL)B={1j`YJ80xUF%ehvcB(!zAFiDsw8w8WH5g4Pn7NA=2QBn$^blw!X2UzVJnDooO;!#vmwt1700eh_&f)gieHVaSa33DxosVJ+IT-{3wY2dKkUw>oxa_dWNOkZd>dcVe=DYOjG(K`uVT{AmzWQ`eWm^bU`C*iY}YJtGMu_ygaC>NS)Q1DR4)oEadU8<~|X?1r>Z+7Ibp|p}*LHzwPm8Tb=C4t$ySS;|shnyyJoef{aG}5}px%@eY??E7zCYBs7Owsos!DkE!eZ$Fy@sOGz-hROH?Kt{eq(<O2z_{fE7Td=DC!`49RBAsT+hLCAl10tbHoahGfL5xZS3SE^MTR6q69M@CC0J%5T~Baio2!YsJ?y&>l+DfhH>-@5blCtkjlI*}aZW=}mhW+M-Y^V9gjF#}wCBvriZvVHLL-_z#LMQ$W;=o}@LK#_(If&A46&Y(a_S({V1s<b7J#%q<OS4GxaI$Ezo>>N@bz4`RV=Z|OCXOD*1TmKtEo1_u', 'offset': (-1.65, 0.37, 0.12)}, {'label': 'BaleWrapper', 'sha256': 'ca534a46db73a01ecc6a36e17117b42199104a5d45a46f778e378c51b95ab460', 'encoded': 'c-qZ<ZFAd5uI_jJ3ZC6MMKW$FlKd`(Q^!f1Ozviql<nQwJ-R9tCDAq$ilj+Owvx(!zj%OdlA>fMsk8UiotnsEvtQ6?01cpl)?fbemycO^6UKgI-QOlrU|oj~!Q2WKX|cA7`!H@#gQ&0ye@gHCcuw!5MSJ1rg*Ek~pnaeDX&Pi!@K6L<m}EmMFZ?2$S*tK#Qm08Atvi4D%U@dIB2BWwTKL7S`kW`Ry7lwhD4eQ%ovR{T1ZtK<Q7|jQB+gYxy%k9k<*n;1Sy(BxqPmvu<P$x%F0almt~|8t;KOl;AOC*k;gvI)5R}1W;&!qiPofpQ?4*7c#6|1u^78!3v;CVaoGqhbnFVd0al4#ro9Ei5xwez*>pUph<&@2A+ufc${Kxsl<-3m`JiFKFcDnZP>fP1*bI*Rm_`9Oste3#tRf)Ne+?(}=db9oj0{@iW?AGh^%U2igK3#ElALGD^gZpT0`OD%q$*4D38NDXSJ@;70emgJL7$l`h`o%K0XmDSzBo%$3Kl3n8BY)ko&a7FoNTZ+#WO?szgMgMP4Pt9XOOl7Vq8jlk$cQR#ta;|&ThqW_P;m)>6|6NeWJz4`5U862%9)>K1iF>^VNT=D2<aKo0bx28#0spp%c=CRj3O(eW%uKoW#ng8zD#+IuQQ)kmJpff>Cd7B9Zs{vr%#|ZN|H2Z%A=0_ELqZ@g6fwOMEN{hE^-+v$re^|TOyLtILrKbMB{w&Ltr`&=Y-m1IwcHdpvNq?GMb3RWQfigU<0I|EpnhV4;b@-B@{ytWHB)Xvk4Fq1_VL{*OFNVFh$8deZ%4eaZcZ+nLqmy6pHwUI!pb#Wgr{}VA}bup8^HRd~Mx_#chS%TbljNtp!9WD^J6Cu89sH=Mf=-I=@+Bc6wTbT0%t@5X$wsTl5D|3Z98t2nR$71vQ|KmpLtQ$NG>k<tZRP7uc+vNQgitNM=QnS@eHIYsAzOtioA9<T#6#^I$$CKxv$tfRIBXf@KCt9wK!#sHl`7i3#u^x^A1k2-g_C;3Z5VT2BHYYcFWo3u-FMpHgpxe<PI=p4?&@WY5!Z_GOte@Fb+DnzaaW!XWiQ-P79T4X*20;KW5TC-(RnWCRUiJ0LdD%kt^vg-AExBugOmNUF)u1g{brooC^Su*G<~4uZM<N+g?e^&-@@XOX{<Z?|h=x@ANNS_A}r9Oer`cX(ZZF_&osWPp@tz-btT#ac1?6p`EPHe|X9G7U`-6Bh@BZFIcw<K;E25eYqDCikxc;)9u=`qB?onDZNA{_r{k3NFH%8*WQrEVxgms*q5Q)y8w26x^_5x88c+z7OBO`|!6*Z!{jh`uO4M?9~;2e|z?c|GxZqan4`foRb))zwbU=zI%N>xjMh(imgv)@6WHU&b^Ui|FNWXy$I%if~sE$jh@AGh)!EMo&6Kl=^fL*zUsNEbBxEXs~nrEX0ybPxE*9LT3xMaD?qdE!J+DOkLceaw>$08*FM_4CeFST)<KI4;S(O}Ky~&{>7O(?!Xr2N$fWRzXbMstEzb2mh-SxK0;^B;_qo|gPj%gKYaU!%{(SEEYU&QM0D_UEBMAoQVQ&o~Wj&}hB>2}b<w`C$$(PezP1;X1Su7)Z%9~A|<<f+A38^_xijB_m<$~%x(e*4#^1R-}@khP!v+1ZmZu|5>-+E)Ezjaa8mA6WN>!GYCZ>7ta#Ixg<AV5**<ab%&2ynh0c^QXAy&BK4_guG@I>CbK#I%2?mAY2clOh=wxPz9p@<xIM78eeQ5WjF9Ty^S}C`tKiim$8j@Y*!E<KjCMUyrGyBw8*44~PPMtI-`zWUK@)cnax>|L*n1W7mCtWL53?YlyEIZF_;!QzW5jgm#Z6V1?JZ_ZQtkIeZonQ<7Y!T6I8%8jiO7ZCSzmCdj>-D%E+#0y1-WwHh!`ky+b2bvNn_#(Q_8L66`a61xT1;iAZiJ+H@X&z+B)DJ{krW$1#tRWZ8Z*Bw&b7P;e6nGb+;KLX!xy`X){U3Fi0v@S0&Z_V;9mt#C$`Y^u^X{m``YwKavR!Qj<=8g$%Z%23@d-HHc>p^4E&XapY06zXQ84zdsk!R?^W1?V!fqcv-*bp36DnKf+2jKV-G&)@IV)L^a(ew7w$YRDW&0XF&We-@|XYpRxTzRTY#Du~xRpCY}f@HhV;IrotVY&Yq53f7e>WG$|FBm}K^Rsfk?D2rrw-BVInTC+k(*H5Lki3kD1kxm0W4u}B(PlKA`=Ads8#pBkyU(1NVO_WFlx)o9rVdf?Joln7FPv&V+&7U`vMeCxLF7PZB@HmfGxXJ<OEgsYVCv*AOrXRZG)zY$-=R_OZ%OI5Fc`gXf7>^h`z)OWG0_Q>G=7bjG|bGShtcOY2`hYYJ_D(yi!thi5Oxg3$R7(JQ~h@~c3*fz(Y^ivdQuoK1Kq-p*A6Jzv|Q>IEB*J&*!|6Gb5jO!sa6EyNO+0(Yet_laG6_@1_6Ygzwmxbb$MyV?#9T3+>#pjJs})ON|V(2><*`-?R}woL6ipr*3Ydo=1!6m=UJ9yj{PBt+j$5zmGrIIt(9g8OevetTkBk?8z^#znxyEh(9%PZk*YUY3wNe!-Bs(}h7A7srB|sedb#4MCM&~nDTrDaH3f%`9NMkaSH>E4tr3qtmTl}S%MBLkn&%itOdEy++`)B63<_tYQAjJX7pp1#^Y>yG<o$E(7^;xke8xXO`N*Cm95_uL<Xx1g+pxJ~)h2~GjG_b^>1{}#<8r1{*yF;U6h7#}E*H|?G~R?^<aAYEv1Z~Ns6%zEj_6xg_2~Nnee0_uD%<C>1Nshqr$_aV)uB7C!O!9|nM=38SXRDNvDfQk4)-4K+E8JzcYtWFJ?fW6bHOds+_|U8xGy@VOq>ix*BvgUoouT2ids?I)ygvkOTsG)N^dlRN|h>nLM2$L>=|z(vm}@Or0|!|!sjG!72dB_rUIEYjS8~CZY=QFY(Zc<V3O9*+uAgSkFK$-GMP3ceKcRlO8XCFZ~s4I4yV8hG0JIN&$AzFMmLtNkZBh}HUwLJz+d5-nZg<?$Jbml`$ew#%sfN9^Ay(rowCRKk-X26`+S@78tXJ7UfSD58J}t4)p~CiP4Fw>zRz1U!JMfwE++uSPtgGD&1*8>$QGYyet+nyho1CN0sq14AE+DFP`x)kEf8jsk^w||9)p#J&-;7k+lOJ6dD-*LIiVcuEWI#OSy{y_kSKdu4H4Y?UX2ev(45N}z{idnO+NYHR+5J&HYWY_7a3&(NnfSTOnvRDue~OUcCRn=kVlr7<^=8KkyZY%W0m!cSn4ti<EK^_RoQ_=wc9<_8$*kvdY)Z3VK1r1%fMgQdwG#Ls82hyk^lVstaI3JlZ|?)+C8#OVRyRKn>~KhIVF4dkc4+vN$=vqixM*Ui{+dhy2h`=Ff9VOL9mgt^xTH)6^eHOR@PTeyK{J=1d!uH0+Gz`eQX=`;yo@t?AAal2%9-er4lCYv<8&HUB5yeI}%F4P(kqnY|=(Gk}tqk36|;{?2{aFTkx3$nVGvd&_0E$q<EQyWWd-mXRgE(K345c?}#RP!V`tZfu0TzYx6U1xGDD_E>L)B#KoAR^UCc>v)v|?#$09eACZloCr`6W^E=}C`45p<*|*I7f5OAdt9wST>>+k*RHE7SIz4LGB~m(o>tyqh))6X#o}>7Q(ay?KKaMfKX;R$6g;}mDDV0%ftKN}2+?)}Qr>6zYLk5ur*~K<I+QuvbcHz`%vnETqx?bwjV_L8M@?j4TdQSYWXJ#b!WgA}WIY^ZBT-yI=5O%OC?LS|}+Bcadd0;D&%vafxMu!8-Opk|ePFY~$iJNsgJub0}iGv#S96!+<Wubm23fVnLs$HMr!C`%l?A6kf?44H2mZD>87G^W{uFEQd3TY-yh%tab-2|8f4FimW0K+-u8Nut!zi-M7&=@LLVvD%ww99J_jglzul$~lIv!jEGm53Pb{cOH<1feB`I%xvUqx?LlbO8sAe9%APDSb}DSkK7J;|&fq{uh;tC_oJeg6^qm_eC5-Kj!CN=VYH5uQmZb5)tu+rYza2Qxx%|@BzeaSdfJktb?DB2n@teAikVvx6ixB3A~o4eV%Gw(AaveJjYLRZgYupnJZV}$x3T1KW{#|;P@Drb1U)^9;uFjaD*afBZ>`GKeqh&=VdOE@UuVrVmB91#^ec(gfdPJnKDE+B!vN)+10?DL|Rg#1|aSoFi{;V2r~V2bOP$COKLei(wu)|&J3#KD|?f%(RmYI9#DWb@b=+NW_Y2OK-C`eie_wcjvN+2`$vpOd_B-OJ?d?KN0sqlW$lr!{-_EAB0M_$H6^A++Pm}R*$4Iyeb^JV`-5`WIrN_g?jvQP+we>s>`?iJM8SHAJ`#qmlKXQaY0;AC6)Q<4y=cl$vhXXB3{I|+`!-G!aX1H(DbF6Nvkt~J$%HM+LGN|CIXyC>mCqYYJ$49+zH^S@HH0eRgYU@#mZ%_ASbH93;yX1aD!j8d#VytB^m?lBvzwqGEt-bMlJoYi5pcnWo_yrXDg}i3u%^y(UC2LduZK7uAZnm3rNoauJm0A}FnaR)a77Y)k?`3IEe1)Ij8B9jKU~;qzu&}?j9J@zY1l*Ad3hKXRT_SVoK*!JglG<{YJtyApqBEcaKs7`p84_kbhpNby*rabbve}K^T}XqHEY8N$Qst;-lJLq_Ut<3ko>d+QB#9OJ+l*?bhT>TIU-?pbm~?wv}TR+lYU*KFQcd}G@w_80YR^X{x~4^<D+J?6j}o2TT^5>YV#bGL-RyMgz$zD@F80{QPXvOvgh&qrIgmDyJt`2i8_$E>y{hSr`?#|Ycm6?@$tzf8mbC=T!9qB{Tf1+DY4FNQJvM}oV9uAZtvKs84|`qZR&a?LVCAc>BjugpPoAo^vwKUW0-2XHC+h}Xo*i~r>B2rgdVoBPJjQnCXh6=4W+gjWx%|b;;<g4)Hu^+R;%om$2M*T<d;@$7ixNDfB7p1L{t$Rx8dxIIk9Iz2Nn)^5qPsKbc{h5BNicFW_%JN`|@?<W5W*l=$xmSMt&UR9dSoef%g158O&^P^3p~|1X0_Vw!IP0!sn#?GraX3>amK=?WA|?j`v2ey82r-{7($?3#06mCl8)re*b95==17`==2ZWA>*=9jB;_aaU)mue>tjpQ0z5y9@?G$k&^eydDz>2;-2x;uAYo8@KEz=8#gu$z<atm^U<!f+Wx(}?8ke0OnZ9WJ;2oUCo9!a@t%mRE?zgCA*F4#L6{9@(xEHMY=uCxcrH3|Nz)tTIt1V8U<vGYdf$`HZkMdw<i47};BmR3;0~)et$!lwG6GIC3fQ9HprA{UcuiA>s;Z_eHwC9K&e1JQ9Wv8uQj{&7ddLy=v%|ze?@#Y?mCWez=%?CT<6iY7{-NEaJQ+XI6WVEOes!c}eG1^VK6ZjbnA6x3Hf;dojg|RGsFCiav;;`2T1n&@2NuyY?9=3Wmoci_V(z6i+B*_d9vNZy$`Fl?yQ%`IIP?n9Dy46N*o}6r8&ZN89z+pw1d)yzDkB-uvePPS8_kY{HX=_xnsU*Ns!km;1EEil4tdP3ls@*JBi6NQo+1IJT_h4ii4%cLq_yt0iHB;0okniYRxFlj(V_hwFk;ZPQOOxGh)#KJaKiyK3_a=@ug|e~kQnlP-ZlFiPgD691;yn$H*jqNKzXM`v=a8xGJt7oT0C?$w-KN?l1Us^YCz%Ni0_w$sQn%runleGn8^SkIDh95O2wuhlz10{T!+ya!`?vpQi|<8>Q|H_9d75a9lw7{g9!$pjr3{U+Wc!qi*CmDJx>z|C=w2>V__!bujBBx^*}Q$BcYu7p>n=<_h`)L+FqCDrTHrXMmj=C+<3YQK!#(2Y)FD#rl6k*CHoLO`@Jor-GmjE@q$4ayF{C2h5rWb`~4c);Sh0~QrAHB1onB>8pN;Ka^COnvYZbfbNZ)Z)Z_c9cwe@@QysHkqU*=c0BFqrkE~~`KxsZBn(Qo&;i@z1tu1L(<1Kc-^7nHXqU^L!hlfs+EYMO9cA11iTleh!i2OC8+@9vQK4W;lzsYc*w$qb+=D5_KHwg72C`iAgs?2S5BiNr;1nTOu9Wo)iO|K<SD&ub04;bdNT{{K(GbC3ds|{w_(S$L|^-nbC>~{}w{z~9_o}N1&oY5@%howyVtZ;hfZbX!fv>kkKT$;qk7<cmksN{sV5DyYxDEsf{jm=liS}+K+n-Z^Mm(;?_PoP738+&g(!k1O2Dn1w569P~XC=1z4nCxl=YA2T;Y;t+meL}Z-jKxK5<wF;VBR1Y{#1>;meI>=eOLVb5dXX~r>76R};qku2Pl(n$I<7e&b(pd!ni9<{?F~2R$Yt4<d{RQm0%AjsgM+2+wuCl7>^>pmO_#Mif=&F$Wx&}eWt`rC%infZezXj7rwU=a8QG?)JsuA)e}DJp%9D7SwzI%F>nI#o0dKmhO9suuBd>_U%d_<nsYhdXk6;s8Z9p;D7~Rt`6AZ&+5VmwUFUJV%Zjcta#3`W)J)n$Ri73DExfVQf1NuI)jo*zRK!1%g-Ma*^20qyV!DQ;^;cRjfB#WTP)@5*?BJF|XDDAM`ha~1xavg0*ib`3_^*lVjg+?DmE3-f;?cD;askpsZQfFMoLQZqNMEz<V(5LIZ=m+iNa(IM(apmTsapk?OW!8Oo2h>SpEz6ia_F`tiDh%!?`7B9Es4!Y|c7zUQU&e*f?roC#B;SeJwVS)lS%`I3M!@0gEGA6QdV8KMz)xB$N2e3+l+D``qe|SA6ZYm#pwCaV_B@fap9y;Q_@J!y=HsisUust>w1wfvi>u#1dIz1};qcFQ7w40!-`~CZ+lTYZOOM1%@2K_a?2q${vrF%rUED4g(-@}Cz&Yp~s`imO=#VO4-}!AmbD;9BY9As@31u)7s0cQeE-A=b9q`zPQZU641WL+A_hA;WUy_R3<tU^?**BTLmT~s)cE3b#{0^_on>>t2=mbT9@V=96KpXEjfc`#|*-tKCoxMLN9DFA$=jHqJ53kQJtWUq6U7jPDNT)$f)3usnjU-75iVTVNC^u<R{|Jze(RkUJu5M}V15@ecKYqWW#};+gNz%NNOg~ezP97kDc*2w{&T#wk{Qdc>D-xBBs`CIQn6u1-$xW0HHRzxf=Kclfo8ywuYVH?)#{}Z$?qIvDlLd=p6*vphf01wDp$eoiDW@GS8S-Zbkzo^JZ0u!uCtv49K<4@%=T{f+UfH|r%s{B($Mt&BJq?F_v?F;Ep8e`yuL$j?{cJrW;nK-{Sedy;tJQcx`>EGEZfz6-5B}UwVe3w~DIB+qlHpdxc@QUIURGd~ts>w|sxrHaiZ)n9PqoxDrZ;giCt&LX>Pg}y+$>2R7EPFRmExB6(0M*V+KXqudH2ur*Y?gD-oYjU!-annRJi8+JDlnGWQ2YC@V3!OqxLL`l1z_z@%H6eqc)V7NlkOrGd}<4C!)vm*CZ%p`RsvNKVmXjGkZXbrfjnw_JErzTM(&{SQS_3u3nA!-I&^F)DftR;;OR>r)60kkp!1uvMja-2j3;sDT%Mc8>jNITGeEB5NK^)yC}3i(I3;~HWnTy&qq+R+F6;mu+>f?-igKr={6Ah6bU!+{3tEgFu$vgEXK{!&*roiGtVrG+4*OlXQ)lhOvv-BMbw=ei&Y}kK*)-7@o4jetALQ8^BZW17v2tm7YFyOOS{8GXC7W(%M_^}k3XrjVruND!_-@J@Hl}O=WluEhBO@eQx?XvFhw}a%gfhqNK&VrFiw|6KC)l>WXQZihxV8x_O-u^iU}(`dYG!}1;CGkJm0Fx6RXwy15=E`*;YlKd#&PGl-~MVwR)Xel`HV~BFx#-`)7djrL6|tdV_OQ`I7JenZBz!R>&yzw58NHla#jofLcQHgSbMDF*u1h1P7Pc^17`I@dxFi$%ZFOhCE$14&+SvK8#BbGrX%Nw^y-dY6O3omQ!{`jQGXLILrW_BO4S~Ou{*7$DFIIi&=}9lt<I_)^7jH)-Sa>R@1%cJ=2Q3*V;ABVF|6<F6fok8|z*z))%#IIFw{p(Ih!2N~@9Z$`|6YM~>=_3}B;ZRwsgd=)aLJuKl290>X_Gwz^2&AQ+J%-kC2KY3^vYR5^7z`4X&ityt2a%zne^nvHDIl}bj`hL6rg0_z1e-XoPM*kHV%10`vauJPX4uz=KPtf+v`&g?PQU8Zvw{q8W?O&Scr;)koAPzO3K-2)n0)|3PUfa6|B&sqpr9NLQh<Rw%uA_G5~O#sydsc$4moasX6I*GbPjeWKc(NB@od!cRvz%S-Mt7u@90nM$FOBL6MNusVdvuLO?a#?PYI7j@qX*huw<H5TTk;DL&eUjNss5FmcT|R?ZQSZnlv#4byBiRCCLd^uhwL}oqP`(X$-3@qzL|J~F{gnu`3~Q}p0uWL(Ul5*ewf;~S2Gtf-t!`yqc83)>v)f?yg~<-$H%G>+oVZS^`kE3GwjlxS;OVtZn1-m(pL3EKJas`Qq^--3!)wlU#yJ<dqjsET=OXiudh9SAND`crhc_{4q!OT5EwgklHE{q}K}s*@!3~dDbchoD7gbIYG65{zbhDLP8oB`3>#{H)5UT7xbn0~#O^kVgsv%ELQE?5edva#_$Oui0n+5-7$84+VuI;joJ$Sr37+pY(M$}}nZw~;F9VfBD@r3be4*;x9kRnN)2w_qifJ(m;XuR+v0buND1FG|emh+P)H;3L5nP=g{<UYxw`G1k3lvHYw2GR%_k}=`|D#{}F2TL$kwDHy`P9&n$q{LA;cQ&AP$KFT}Cb_RO8Hw{boCeShFo`v37Oq=ma#Zk+e*`ZpSmtp;w)5mREOMu;pi(u5oJQ$(rb$^1u`of;GnqugpwHitD>uB=c|mg(^g-8!hs@ldr)~)|md-PxV)w;X&R!U=yxwzqH_UVHFhz$;?jX;pgJ)D@c&7)TlAwoUe!QNmJ9(>z>+5G3a;ek&G>>dNE%#P0yxv|_K;MpE6fgSS0kBXe+f_aw6ibRk7{hJAYpd8x1>F7BI+NHBK4mX)CT9Vk*2OI;OT6kw2UHgGtqNx!UgP$NAZXK?Kv;#vx`VD>Bl>QJJ1z2Ck__`U*n=Uke0Cja2a}(zCEAs*hxj|GQ(3_-SyDK2xdo)ts(|qxBT<(GyZ0Dn$`psmBDnEMt?NET9$e~4x_nAn1CxsWGNUiU$oF<6mk*<9qj-vJ_hB?^6wi=WN#l^Y<3;|nX!<Og?U@96^BswU&mw<M8u;{mN=+F4J+Ci^PsAm0Ujrb7#TlC<C1Yf>dLUPB@!UChrUP0CAYP*|sJNt53W17|gE-P-`Z$zBvp#MgzySw89l(j+-$&XX$CWX=J<XP!f>(}F1Hcd{#4bFnl2Tu&lbY~CZ?5~FeMxKQM89^A8Ss!vzMPCV>M0K3(4-E5#%=C*R)$BfTUM6++}fGa>ev-c8luMmqrYwowc}jLzaa`-&}L(+du4{vjODh3*(PK#%$Xx5xR;~|@`mx3;yhc26j}9qEh@isjcs#LSco8bZj#lz^;Y)?^gRkhwKIx(X%A#))GbIS59bq-0c_F@fLOBTld5c@2a%dmgSI&ijjyK2&i&G7&i;KkEt30+5czfGHwS&Co;V>L&B3!M@X64dk%<__dZzxE?5}t}iRl&1$4TAM{#ePo>8^LBS-ycVzr^K6@w6;1$NsI;?RI<0vERjHD28)B$ET$)r>M%RV06r}!ZB}+6RtK{kj@b@RLZ9Lgp1{3!dIh&2^lk{4^%53pg#y=t1f+e;46Ddss|QLH&1A5jr>$bqICll-#GvfSLnRd=YM%{1G2S5M>6MNWZpzL=hEg|&2p2=ojCFa>Rzs>LtP6v(>J@&_?9M)KxZsGNT4TiPmrY<!(T<;Xag^q6W36OXu#HGTSsvbb;mT<ppa{6<aj~$5zswHbK&56E%yUOF#hk^1;C6`NK|5Fs@4=(CiSmsnPLMZd#q*)ly?n0t(t&LS1WJyGs@3S)n_=%JZH5+vMzmg$8Ja80<ywwC{iTa0M3IT1Jlme_E(XTa+bFuk=P+QcO-<Gb-q4ZroVLuwVeBJrA-QY8Zq6i+)Afht;Wj6nobsdqPMIgj_&9E@0I?5B>lfyl1M>I3Mxp_RFh1yjD(_my~W><t$r()dMF4<QkG_gT!f{GQ-_Np33!5`<wBU2B{#%u+$gi-+LxBTTY-0IB(L*bFtTAI!JQwG*gS0{HscZ+3znUf``SWH)tyO>rmdTkqo<r4jTI&Z-$Rojw*ysRbWk6?8JL?9I4D#FrW<;t=pT25zos*5o_iYbJEL0AcHu(n+<Fo4i#+t^xw-RU7|>H-p7fm&dH5e*5DoyJS#unZ=A5rC9g!h3&!0Q<yiHqz%UTFpHd+PMf`iy#+?jhQLVf>)gsYVIa*W+(c6RN`4xBI3AZ5vKeMu+ow%EAW;-uUsI2YPn{iJCjN|2__ENb0p{W_~3`kHGbSR1;-yCoH>@@cj4gyeOb104BcBqG?RK!CL;%g!QTxG5O)LO(4M2+)zhElTPCz&6s$RB}JW0!@P>u6g#AB)Dq`0yZ~5P2i8al0WXiAN=UziX}{UQ(D~d##M2><@;U(Q9z_UCPi>Ko$h!yrFW#NwRoRk4?)G|qjWUrk1MEY>unZI^{jk;@AG%QN?<yz+z06FH;)E0n`i15v)hT0Vq@iG3J-?CnLY_|vL&(tJ5TOoO;O;Jk~%;q<z7nr%`})u03#!uY`fHxV1{351?ysm<{_9IE5Nct0}*77u}AGz^-TMxDoo1(TGj^NZDctSy2QNFV!d2aQ{CX!W3-Zz=g&WT-^4jEfD$jOR(Y<(lg06HqPFa9j6R_Dqt60=2MGPlppu3r<<nX@)p1*SKxPvLLYkdBERuO5QXDVbmfYck(t)fw8#U+*Wqgs1J8q-y03Y0SEZrDHP%mW^2#v*q3HNhEQ>@+7wC9N**jBX~Z2`k%@YMBt00N*n*p0~4dt4tuHX5P8Fb=%>hNLUW!<|(3Y=IS^mm+afU#5a38X8cV{x8w-%MBl2Hk@JHJ?;I7{i~dom5An>_{8Djl~e|dV8vhvk^x^hT6^CV)~YJ49Z0xf9+N3YkG#X{+0h^tDRwvuf!a-mhK~inl?9x;hPlmcm2u2^3GZ&w4t48^Zp~IJ>(}B1b6Yp0Ht(1*M<CGvB-Ou=BH{67V3p=uA)bVwy26Y#1ikW^__KBLpDpHzuxs(}LKjd3-Upg0+@Zw4OvuwN9=u#kqZ$&W4zQ?9bwX!_i{02nZren6ww{!@DSL2Re8J`<SdlnlyKQ$&mXRU9=J;$18@IKsh?hN7^&anV7$x4w#8=f6>@5Xn-yIKcL#nGow0=}q4#&KaI5}=ZYSNApC{(Ar>bGhkV|-l``#g??UJR4I@D7RJ<!Yd5<}CP{m!Ch})kCCpve}>-+(H(2igg-v@&b5+Bhaz0&i^^F-AcM{4M^7PhXh92ESN7jJAtN$hz$#8B}=y2sG5}q*&-~6745BIbC6GgBMcmM1#*BPg}jRT6jw&lRcbSow;KaUa9(N88NS>&*;dtww5lCrD}DZ~>~|k8=<_lS<TeC)wBD0d5mDi;^JithO8lbnRPXolmbQ!PeR(8pz}ay|&E_T_PnSp8tdwq^U7JezX1MLnyDN{}>RLo@#DeSA&;6pv94=Az1c6Tzth?L=RO>?8P&ZI;8l&3tWJywH!p;F(@m;Tcl7`4P(F90<koc)?f)f~}AALPoFiWy|?&#A`x9K-x#?~)cX@BaxYL$DxCS!hD+uug+tVAxmnO9KrA6N0~ej<(&)fb13Lb+Bm9Pf}6t^(^Pji8WG(Kt^XyS3{Zb5>s*j7O?Uvdm~1G>$!kYnGFwJ;>YZ)YI3kck)}me|Y57&eu14Q2H+GgmwXkNLbke+jTo6`-$fr`gR*U%)=Wv<7jW#3=q|W{y3EI^|=WqY#fyCjc^h^9wep}bTc{JdgQp)9H~oknH;1W0K{uGkz@FqsJM1apofR3`;ULWdT#Rt&-8L?yGqwLacghizqAz}8wdITpEV3qZA~^r{h5|NTFcpTS!8Za&Ns_(OQLU1?R0!YiMIQNM4|XN{|#f#GTnw-R;@FIBajxTb?1BEBzVLgaNvltr{W~EIn0uv>*%<a33VdDQ<b_{dHn6_xSmf`5g7pgCYD+w+a6R4Ps8xm2(OfmI4(<A0UAU}RpLLO<Tg|-t2*MR{+g$~hyjaZL3-s<HNH@>L`eH3-9?o6iLMTlCz*)D(;jF>VVxc$;*2VS51rVbfwu>}(obG_*0pL>I@s;O<IZ<wi~F>+xHilqd$94S>`kqS@VKE|(Tt4wR;sqtN2SA+6-p%->M{<kE3Fw5)i4Pj#H!{%J8erS?ZqY~71u)4%tTfP<-~yG(nN#>5UIroI@cf&%ardM!exuII*78HOxFcO_=X5kWX|ZQ#1#Qj1p-}%H#Bn{`h&GA@XH1yjA-@d%Nee-*I3kH><gb1R!iO%r1uuAq40r^E%ALA;?8&6fxvg?x3d8F=s*|}koOso1_4tSk9WR;2qqENclYf7O%-)+Lg90?5VkY0Cx?BofR`Hxje_FXK!Ms2G>-5l;#4=-m|p0(16ChQ3_>Se^E<%~hmq>Q_)bc*lcT)U!>r`eW#ijSNd%H{jSwi=JFpo7))8PFlf-~fAu1Kgkw35fF2?h3EJnURUwzX*b@BcAH+26UV25AH22G(?(jwBI2}-DZH$kM269D0CPH^DhNsBElrR;$omSh3p;3fgT0E<xF2n2@sZz1>`G?6k|0+`12U-tm4xIl$U@BM7iz9kKOmiffI^Y$u?BGPKnFf34of5HR7ANec`Q?}Cvwcq9d8HymY2W&;bM?A70sDm~A`)ZGsymtA})Uy|~YQH38d2MJpLatMiyrg~55Tw~6&x(r9@Ut0EJ9E+sNcAS>Au6{t=V{t}ny}|vbp2QBoRH7gzAyafIhoYa+7hCJk&#?;*0jE0LbftVBsJLta)6W|*&Am<xW-2|-~Suw1*V=1{nNX=JJf-LHLFtE>fH^@ld#$3A)(;%ce^y_DkaDBsx6SMx=qE)^BP)}{U$?(4yhEDk-C)td#-;~1ag;uSAxuj1%$Ru+d5)DF;q?LvRJgizNG{=eUZvBZ%T3LN}v2zU<>65yx)gLIJRi^cDo%XZ7ppWKWkF3vYQnwL3(KhYjdb+y#hyC8o@Z^gF?rCd;Sr58ULDGoS(h^m#u`)D`wD4GejpOuL`FNQha&-_T2~T?C)2<f4q42-{-Hbt9R!Y^yfm7VgAt@TC#P>@0LW6Fl%cHgN*kQ%P)HU6FH$GO3Wq%AL;e}jnbA@nKVW-M!EL8R&z0#S5lqodFEAzm2&Q_I*i`y@pbm5PH7OC0{$t07G^Q|bn)@cyZ7f_2^S$%(A}<X+~%5R@85s?lXD#8TJH9$XAhj-ks8sz{k}Rn7`qZM9|aHcl1fMV&3EbK^4*8GjnVMEE&5QKg^M2V{kzL63BJX(hq<%W29?|J*pfIJjiGsRyN@KSFW!-`e6q3RDYS8Xn1zV_SN6B>WgnMUXCGdlUA*>2wal+tvR9SkRpxe8IbDrht}*Dij_WE2qh5;juH%_m85EBA5TWh{RczLnM&TXVxx1@YVIPEO++sEhoK0jYY$N(~;|t#bZ*5j6BbaqhoK3D1<QS4K|KZh;CH^InTsRsI5vd`<Y1N$PsE&m3s5gETRuF{3dW*9Y6ke8-m@~mYRatq4QI&B?jS}6BOv$(e&JX|&T&0)#bW4X-H5T)3t>Zy`iKVECu=*>#UZc%Szs=mfNAmf0r|}UQA+SN~r83KMT66V;<7;ZDCpCtDZYcc9X5ysGNuVwMGC+J{5KXT8*R$EtQLlFxoSgJddnfa5e>&?0{_#oo^l%@}u2PAvXFc(cpDjg=866#TNhEZ~GCMK>q4^B#L>z3SnoSHO^kjrknQw&m>;kk0-@bpZWUAiBArx|lKea#wYB$)={PYCsY%QC~eX5t~MH|)1#^0-!SpTwJT-J`qJLu&5W@0dd`NAv7){tH82QnDSa+cHJ8uk@RC1c>pIkv1?!k{@r@HW_#eQ*s<hnJU~d{6KxN0OMS=s|ukimvt(0$^v(qyF2nO#aiTOhFr0FLx0AXq$A#?CIRI*=VU+lh*m+^-~-DW~O09)sqL0D0=wV+x3%g(;!2p3&G{}x?Md4o5jt1tNN>krySnr*%$3@7?-I@yYsA^&VE;!e?7PL>-|2O>C`casgfRU@+$d>6DOh3d-mDQKke3aGF#>*ERU13MTIFQoX+-bvFos9QS+Xbri;h{KU_G8N)zJzq=SeFR_Ez?m~_m~qD_Kj6l9*mW4EhnE)r9a^7CbKw<Jr_ZvQvQoPXI|&TSmG7GRkmCi6bX6pT%6T>mW~+skS1tM&nY!Q!af<)5#x-;i-<<EJg!eH82;b=7_cw{qDRxF^%0QsjgmoFMI*?+n^BJ2(h!g7amz1ne_XUTsyMpUM9*PDyDvl!GwO{-l%j?L9o3Bn(*eH*1flVaoWX3eSH1?(%PTSw=JT@G-3L+cctPK2mWQMt4XLyP%=s20X90mCbK>D48E;<=0Bdq`FNeoHOn5JCn`C%{}^4g2QPor0dgGf=x)`S~zwIljzfmlxX8r{5H<H_sI~`zj3ewY<bgwT)VSK>`uhd*}8cwp|Wg~!%ap;<xL~E(&_ZOeDx|{YGy!bcBQ@fH~Lr7LjNXCa-`bjv7hF*q~p{xcNc?^6Do7`1=AWg*=D9>8qxM&JI2w)8=SmxbhE3%)=AFpUL<3yI&iC{ZT;l&qB)`41_%z4+F-Uju0%v7NWQlc{ll`8+EE6&^mgL0s-8y)<WMqjI54CsbzC)SW}8(hU%IkM`x<YDv&ex|USLD70aA7^{yfY_=~GB_`^Z#k35LILa%+Ck3!tklI+=hU6{D7a_lXCRpQ|#lN7Rl@&Dt^Q>vAg9F)J{G;C3QnWN_H%Lta*Ak8-+H>wSxSJ+J!C8g!GK;p?aX-vtS`FV@dd0jZzy%?31$%}gJF^1>;HsR5oUNsFp42EVE=LCs6kAOvlxm~J+p<OpSP<kVnml3j;GOdPX#OzjN7AbCV;EKJ>NC2L`#N;g3(=eC_h$)B}(?PLc+KfvIn`327KJUwoyQ0`<)&wGsaH*qNbE39Ul2Yy}=4KMq1A!y+|i2{c}#?@mb06%h})yAv$qZh5pH{NovJ#V<z5HIPocUV-{+RQmBdQ$72%{MsKu0#H*TH{C4J~k$Np7ErbF>``Y^QQBS53CFtdD+BYheIO09GeYzl-*7~c=j}E>TSNaVBdM0K8zhMydCa~y6b{Q5hDi`2X&&aMEu|v_mU@XA#nIUbo~!;r)-0H-@cTl-IsCoLy69lHv8BBE?eZk!=2=c=}DMNMYGu9`_vHEuPx%D`uO9rA3g(ScUr!q8xD1>!_Cf0gO$f@Z!+SDA`qzb?fXy;(fBKfTpz7zrmA_9g?Pr^Q?6zSwU#a%ql~l6-EAP#i^nxdNHkJvsRH*h{6Qi%r{IVk0kyMXRKQYz?GR)!m60OMry`!I^k3T0ad0tiR|0>x-pS9+xx-XvJpGR%&>kMV(W--Bb%w+(Ynt1{)@xH?nQpz+h%*ZFp2wX$lYo+k2e}B2{<_cm?Rv%9fbQNh)eY8bX+VE>HdrDxVdp}jl^&|ChgQ0$w(i+|*6Z{R3E<{sJ)37QPR;1YXhM}bUEjn${L~I$d@dDdvwdzA#1D(0gO6GmMQQRg&B_rNiTEhe`SF@lG$1;8vFfK?kX=~Cnt@U|28fxnrgK0>n79a}8t}6OCGg|Ilej!fB&t<&)oflqhIiKe;)fOunvg+rzu2;9x;<PI*~5>X^bT2uT9&nS5dr?26Bi^z)#(~H04!4;&@*vYQvCGg71T&tZklL3dwWl8;9(s%W%wx?){s;y*S8>;Z`-=pu2<$Km=-eKO5rK%*6x64=vQ57a_^z;BAN5%-9WdNg>pH7vT<YGn+w{Juml~xd=;^P-sVkq^a=};1!N1)0&ycrQLrN8O>zqK{ag1P{n+CmvWAG|1AA6Hc<KIXosoRN^`6$k$Js2lZw|S%B$W{`(-sfPw`%&5By6qm8~5~$G-OV9qVD*(mhZx*g--4fNGvmM8(f(#`B3*^7Vx<^b1I(|<B%E|-hz2Tq{WH0)xr<9?nu#Byir{>PbSM41Z8e8(254mN=-jPCqlVMqk*@9P?_bP*Bvx3burh+(UVD!x?j{IWF<Rsv8#vX9dt}nMw9sYV;}y#4qEpwKXy)(M+i9fMw6!RF)lnQFBL5+(z=#m3gkGIh1~z;txp8-feJn@3(~y)FgLE?zWzt+nqXC~^&?*<Ct$;I5*I8Gq&I4p@QC=yY$PvNu1m=Twa3ONYRII=%&p;L))k|rB$!<$&Tf9!j-Fe@a|yHko4vf8#}3T=8~wYza+iJD!Fy?bDrxw*%e=b9aF@%R-s%Oa?|LH<NaZ05UnSCr!~T_HGGy*I<Xk1?p7zeP?tG&eek*la*~;yK{-W%SI5Lhe<S)t&khV&uRM}*E<G;K*ySS2@IyVDwOpKWhfJwuLK(2e|2pEI}wmAf^3OnOy3Zt?Ns>q0ziMB8y5*!jSdG+y+Pw&sK&L0htX#F1xC9bR', 'offset': (1.65, 0.6, 0.12)}]

floor='WholeBaleEquipmentCourtHardstand';box(floor,(-3.30,-2.65,0),(3.35,2.65,.14),0,'Whole common open hardstand with wide front approach and separately parked baler/wrapper positions');FEET=[floor]
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
 ('WholeLeftRearBoundary',(-3.16,2.45,.08),(-.54,2.58,.38),1,'Whole low left rear boundary; central rear opening deliberately retained'),
 ('WholeRightRearBoundary',(.54,2.45,.08),(3.20,2.58,.38),1,'Whole low right rear boundary, not an enclosing shed'),
 ('WholeShortLeftCurb',(-3.18,.18,.08),(-3.05,2.51,.28),1,'Whole short side curb leaves front approach fully open'),
 ('WholeCentralAisleGuide',(-.035,-2.28,.136),(.035,2.25,.145),2,'Whole thin visual centre guide in clear aisle, not real safety marking'),
 ('WholeLeftFrontStagingGuide',(-2.88,-1.62,.136),(-.48,-1.56,.145),2,'Whole thin left parked-bay visual line, clear of original draw member'),
 ('WholeRightFrontStagingGuide',(.48,-1.51,.136),(3.03,-1.45,.145),2,'Whole thin right parked-bay visual line, clear of original draw member')]:
 box(name,lo,hi,mat,role);p=tuple((lo[i]+hi[i])/2 for i in range(3));p=(p[0],p[1],.138 if 'Guide'in name else .12);LINKS.append((floor,name,[p]))
INSIDE_TESTS.append((floor,(0,0,.05),(0,0,-.1)))
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
FOCUS=(0,0,.90);ORTHO=9.2;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(8,-11,9),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
