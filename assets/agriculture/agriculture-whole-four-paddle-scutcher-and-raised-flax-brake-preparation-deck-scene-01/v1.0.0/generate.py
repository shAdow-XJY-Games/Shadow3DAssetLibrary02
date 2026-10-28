"""Whole purposeful farm preparation scene; two existing models reused exactly, zero new stand-alone models."""
import math,json,hashlib,sys,time,collections,itertools,base64,zlib
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='agriculture-whole-four-paddle-scutcher-and-raised-flax-brake-preparation-deck-scene-01';VERSION='1.0.0';TITLE='Whole Four Paddle Scutcher and Raised Flax Brake Preparation Deck'
DESCRIPTION='One new whole empty flax-fibre equipment preparation deck, zero new models and one scene. The complete accepted four-paddle scutcher remains unchanged on the lower front-left floor, retaining all four full-width wooden paddles, through shaft, crank, bearing frame, two skids and whole U-notched side board. The complete accepted raised-jaw flax brake stands separately on a broad raised rear-right deck, turned by an exact quarter turn so its entire long hand lever points outward to the right. Both skids, four legs, all stationary lower jaws and the entire raised upper frame remain intact. A broad empty foreground, full lower side step and low rear boundary make a staggered two-height preparation layout. Unlike the old carding/spinning workcorner, this contains neither a carder on a worktable nor a treadle spinning wheel: two different whole farm fibre-preparation machine originals retain independent complete supports. All original source geometry, topology and opaque PBR parameters remain at original metre scale; only whole rigid placement is new. Whole sources embedded and hash-pinned; scene normals recalculated, no raw GLB-byte or hierarchy identity claim. No fibre, crop, person, loose tools or processing connection. No scutching, breaking, fibre flow, operating sequence, mechanism travel, machine compatibility, access, ergonomics, platform load, engineering or safety claim. Rigging animation physics interaction not made.'
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];INSIDE_TESTS=[]
PALETTE=[('MatteWholePreparationFloor',(.28,.29,.25,1),.97,0),('MutedRearBoundaryAndSteps',(.24,.29,.23,1),.93,0),('WarmWholeRaisedFlaxBrakeDeck',(.42,.36,.26,1),.95,0)]
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


COMPONENT_SOURCES=[{'label': 'Scutcher', 'sha256': '3860d10418629558d843a395f2d3492b8014ecd0fd536405fffd14781454172d', 'encoded': 'c-p;veQ(=HlK21m6uem+NX9Kil3$WY;ozLa$po880^75*dpbd&B-&z3ku*ukR)T!@r+!u4Bt^;21h>xxh)p*8rMkMRy573|%P+rt%EId~_9N?Vkwk%Y72XGP>nd4g?bM&osU%<cSB2%rb1RRMq6p^gY2s&8C-U#De6}iPiy#|XdEpn~%<{9sO5$kK`Q?{iTH!KH=zZxI3-u*WVzuz|MHEg|zR6V)E(0}7q9~XZVG`#mEP|{^k|=LoWy#V?sTI|=bSIzbwRLfMdVcAlWd}bTclha#OAnu%$>b`Gg2}|~WI>)pYx>wp{Va%!*6GE?*`;Uu*I77QMa3!$+C0s6ZJKSKW}Bwj-kN3`(`=h*w!1xh_>Z&mi}#;CdUmhV?R4$o<@?JIXP*6*G540bBv=`97bWH{q)Y1+W9}_5ccHtqTW`)TUZ21Je93)&iUTVS?xKz5uZl&IQKS08ECApv^W&SwDs6)q#(5f|?b4qu!Z_$ymv@PEwTdDuO5*FVSj~COud`%@g}n*qIRiRNmT43efi=sLJf8-Hz$~|BewJ;l!gR4piDnjsh0kGpZKX+G<f?p~M#=0(x=Uy_G>PzQ5*IXFv7qs;7eZ1U!4)kKL26C2#Gg~sRa{tiNiq*&OJ<f^nLiJG0*R@@*XY1Bti@_Nq)vk{6TtlY5QH4gi-nAz2SfrsFt5pzKn<DNh)@G-9p>RQBJ7-26DK$$D-Y)c5--+WSS)DNB3lJkk`h>dSaCvFwnBm|NziwZ00>Kv0$dU*xCfN#_3`sOSWcsjk`7B;($uaKEX6eQXF=YvKmdBhGs2pcTwUcsVey(PX~WNH7%PJ*BJ7msn-YHKnq$FQJ{GT>*@8gEij+k0F|m?pP6!V3Kp47BVB7@O7ynLKGwSB5O(aEpN%P0b(TIy6h-j)yW#xB4O2g21S#_UgoX|@6*^*%Qmw{&8VBWF*h@<dE5P}hD_-h&wi`b^IM3(T-O28yRK}hG7k9MWe&{|dfF_@MHGc34i91xP})wiw!ERc|04CtawIR!u)6KN-RwYgBM)DN?c^)3t6f%W?;4^~U72<~ZVS1INL$aeWqmZB|a5Jm)AicJ~}WlmTKe^zMRFnJP@XlY7d_=J-su>&ZJ01sI#()1G}q5Zj^f{aO!f(C)0U`Dh|w8?deR;Y|9zJQ$bGixcp=V>q_X&DP~EeX!Z`Wj>jff>Z0xeH+q;l68vu5HBlfCeH^rWq|vH7S24Krl55>Wa)?Q@68-gn%E<sQUGa=0&xYtO1ecESRs*5y_TR-t(L*5OxZh<&3z2z|3XZ{%p1)o*<67N-}g9WW*`SGMv#P$*?#GGU?u*Qd?gzkXgBZ6%-qS#1EHD;)K3yhB^+HWvwu#m6mxBKg@%U-FoMJ`#${e{^Q>-ywQ00`qRhD)7O{${O<HK|9<u9{EQ#op3#Ovzu$knc>m^Xa(Q;a6<eQAKb&1&o_Qn3e&c61e}a!M!{s!{-eS>h<#hVTs?+bPPVZ3lT-AC0Om(__S2^})KMJ_PpF~NrgXE|2TyGt`bD;h4q3Rs<sgDzB|D4))(f;+q&t{1qy%I4@O<#jP-;)$UyDnAi(YW2`$K3GQGr)m{Z)g>Ht9s26<Dww;K#L=)eMF-jzTgHYH0a@pJ8sPbBD4A2@zvBFWC87`u~n={#yIx}8!VP}uQr5W>uZ>DC6}AztLeTb?MIp{R}sDC%_dKBX@Um6)SM^9R_FO@N%bD-n)kPQ6UQI*#!sfB{<!Va4|?j2m451?tSeuYe(IsDCtsyY5-&@~FF}CT)5&kM!V%znJ@P6Ji+VMlWACYMEp>t=)rpB>)LLCB>Pclp81A5Dt-X<8fp>1_DoXsqxp&nIw?s+Gk0~D4<KdNQaLdKFD83p~M@h6=1|ARv_|~Ian#foQUho#u8~;A&jmNJ0^u(&#^J9odmRe3vML|p>w0krGE4<RZzw8dm;UP^k+GeO$9gv}hqb<K%RxrN~a<8Trc3#s=iCG<9tp*HKWY+dp-Hv*L@xkqA&?9(<*l|gU(RS{{p4Vf6%bky$DJ{krW$1#tRWZ8Z&mGc3m$~ConGb+;KLX#cy`cSqyXwC5XkA`n-kR%OF2{Jh^kIG#(oz$>*4D$St&-9!%pDWj-i`1+_U0t{9YPj~WWody02Bj{$$%uDA9;ozJSGYz7;t<(SqAySiIODEK`OBa;P@3ZI$ZN&^Sc_+`|i@nV#Y4bUA{PF4_MkK@j=*Jd8$mrgu<JuaH|zTvfF6z#dC<T-2aS+R~<hky=v|_HyA+S=NIMN9PohEQwY-1OhZU%>3_^FB>5sDfi#IW7;lz&k-wbIeb9%R4V;pN-6zh>u&&#7N;c+lQ->&co_i5(N=`K&?wiOeSrw4<AabCyk_H&#3HoZ#B^oOHVCv)tCQxDy8m6O>@6f1six8SE4Mrc_Uk?rDzDQ?5OmqTmmOtYo4KwrTW%Q*@!U_-07a-MiF-Dyb!j7RB`C|cOs(;VM?n{p-y4N3&9zkl{D$p(bc;kSQP0N*TvDUwD#_q3Po0~F-E43yNN5V_QUo-kS1DClaX~4vwo^M!np}M>@V|Qz0LT*V7{GAXEB&A8}d~t`QhWIyBFNpGBz*?(y%G^nE;*9jT%&|WvaXSy8@sdhKS~{s2unTQMZ>@8oZlK5=YLcR_LQD6gPR)bKMz}Loo37gQwq)>MUwW0wqL(Y4YO*pMmx8E;QB!c}$f4azePyg+*BbHYW7)>OvfN;iu6d4e#I#{Jz#Uw5XbPC*NTZNe;viO2`tKjaF39_@v16!0YV!sE0p$aGl5pTOxtDKIq84Fu$Er;Va~MSlHqu2%KgZ=vsj$a|Jt@4`g<USBy=lA+!^r8XzG5xPIa0^!nL44TuIkbA5k2+Q36&jk*%3WM$?8%4XX@A;*WhRInarhIU@R*?s@UuGF^4;kcWtOJ*gHTpS043Cqq*RgY3|(7WZajX7fhTCM%Nv#q@8T4cZyn3+x6Nr1uMcU3rcS^f=ZPt{DexdQrQ#UMrKJa`$^%io`g?H-YR@wuT2F~p&J!sgWX!-vDt#acEBX9p|`VX3?E!$S>-f>^wE4FD@`VM{(r|DPJtC-l+(DLXW!e5ZY*0N(=LQ;2)6owKf^UMg*8@=ueoOSlU(zKd4_oBF|GkRWsmnG`A%kNzDs$Hbs7;b9qglwFSPJ#bFhyl_>*wommQj5&Quwf69D7KXn^(RO%%rSAe(4@zwfI1p7c=x|IzCoDe*0NZ+%)I%p@hlob)^fD-ECa56siYVU~H>)9pE-9P6w-R9IyztC$56<shpef_p!x@xe!$b6ErU*i)m)Cm-EP^6<pQq@VsIqiiARtJImPuU+-E*F@3&^@Setz!KA(puIe>${+WvvYru3U4~)&=nA)5j1hIet#6FlokJLd&&B{59xl&jQ}sg<U%%rOx}ZY)ATKf}q<xxp1JqJv-gUYs$Ew{qK2|U`?+^GLubu8QmjtMEB>udbJJNR9$Tn<+B3A>q*#)jgrfF|1svrE8epUi__ZlUy*ps;hpsA@G>flIi2vUaX=(!6sn~3^AN_sGpYk=O>ouk&5B#d*~|B8jUQEe?LzC4CR_A-<rqlDyPq<(Rg?4pFe9!Vn_1YTD?%Rj^+%SQZXD&CqW>S2!Eqhp@r5hnTK7?b3p11WmZt<Tc9c*QGTcl6T2Y(vlems7y5yn(0TnLw$VYCsu6?VxxCH}Mvvx-J9ztSc+>Om&`j1y~dvNYRTv74;3U;u_bj+w6XZ8b`)blI?(N24S!@w9ijY7+RifjkJF&UDuc5xn}t7A=Cw~3*DmKIeLyRj#<-S-weNWy8RPUH#Ce7dBJT()b(S+-kyVu{R5O%lRM_gEmqUo)Zlv;C)01MsmzEf$b9<nQI!*_-e^^yH#l|{#6^ZVv6Bl9d7e-M=jd5r9<kC?!qkwzED?RrYyi&>!YAc+LAsPv%0wTeTFO8uWOts^t`(TiQkj(pz4^1QNptM7AMSW;jI2zt<^Vc_yz2H?3>+P9J)1|=;pg#SZDtA0t-^R+krR#W4jKwrf)o+wkf^uE5)rB^DXLqlYfnLWJ!U2LP%E~F3TiBI)ew?fujDI4P0ra%UU>~mp4yi4y^>v4QPk!jiT3zvH~UuDMVW|+Fc)!4U?iKyU=N~^@VC9xJRH`0)WC<}f+Ua2EB`m^f(VwN(ea-u;$k8sWx!=cU1w$3g;)cg{bJz*RJd{HR)lCqi(6~NT$1tn$44{><`>kpxKD@L8l(jv3V2>g`{r}6(?8Zir@#HudGP|P*4}+F)!MZl#zRq=Wny}Ck`WNNM=y>Q>95tgaO9~Lbh;){Kob)r6iI4O0Ovo+H-r-IlI#XDk3H<{@!pkpJoLVurDqd6(tZSn?4EQhhTJ2FNS~wsyu)&!%E)tr+BZ6k^$H(L0)$lI>V&-Bq3jEc$)l6!c++CCUkMe7x#~bmBRFQO=R1?*&Si?2%SoTRJ(9iWZ`NrUExZHi25kh!GCzzsq!|V|N07J|ny-$57N&ej<h2zD?X=LgQZ0DuJmt4ZQk>H_n>RAl0=>L|BspYN=LM$SgX)9#-qCSG_bEfN0?ZZlCxA|a;w}IIEVhHP_D}B`4Ao<55l~ny(_bQo?GgS8Q78t3M>^)AdWYpukv|P08E)j*ZxR2rvA=d<#oOlutWA7FiVCE*#5eU~d`9527R0a*xG$zasR;QBjiT4D_BN;!y=uQE0blOd^+;+K6hsM7fTSzp*^?$E>OrbquD0{~*;0e~iG#U3vEO_hppng&>S$%+<ir3-GWLZj>UFwZ;g-Xi;)D2`4iGOme9s-K-p&q;?hR~&1lq^VNY6x_OvBi~xGI>T7`S&?n0^jpfe|6+eL$6EC#0g4fcB0mY$m!-0Z`)A)Z0EpVh}(JID5~Jc%&EHs{o3&8qz;`!zvL8SOrkjsh~RUc6T8?Ij*6!rqvXSkhDj=6;?Q9koSShLjmSdHQoy|9^fq<`J<F~&udWkyUyB=RzdDmp@Hj>ZK~R2c3%AU{_UkFe#*A9g#9`S$5kLfS9Qsty?@}7`?O#BEJg&<*gYT$6HaSDG1wa2)4nK%;UNfHI#SBMm;DXWA{YNJs?ZC{xRt~Zmw}(JvS2dx^Kdq~4w7Y1WScVbp^7Z@p(5no$0TMKf)2$HxtFzE&%^6G68E%yt__w`vdUyYQ*jsLQfFKSil({7bH73+`gGlw{h<A<93FmguH3{tS3cNTE8T~8M4dDiqzq_q%qI)hVQ@FeXSCycHls!MuQq%GBz#C&Q<g-PXs2A64NJoC$U6}Onk3Z_IzpNGu}nD59mMM(qP{swUIz0?(j`~6!VnW4f*o!pewFBf6C^oIL^qu145<n8^u%NxO^`6)U6S7Bw%&ev{l|rPNINHo?(oz3<!_(79@%okKi{99O)h_X|N8GA&n_-JVwCQ2>-FjHXXmFE-Z#5gtd`RlTj_vw<2IR49a4_%TffcuFjPuBb_o4SN})JXA=KltjFcs=*M<8R1yi5wB9zn`-jUkLsTkV>U1$DAhC006^94Qehc<l5@*xkSMY0MACGB4S`93%sH5xE~AIkJ67q3r0oDmYflY0E>!`a6-XXn=E-%c;i;F-~RaMN_7rdTY=l7p4AD#9o?d2;^<W<`=UK6a+-MUe$2BgcC6kKZoowMCtEk~Hrm(=XJllLrX8PME+s`0CjgXCKa9Uy@eYs5%coS<WgCCf89i^&{=*W9hO4*|RSft>%8=cTDgycL%#=oh(=;>%du(367K$4^<EsA}hYbB}4w%fj50Z{Em#HypwP8BA~7H_p{6M_pj~!b!I*hEK&4zvG97*Jq-u%Tt~7<Jp1*(UK83)``KnjGN+UKV4mEg^=f<|UEAwDYi$(*51gJ8u8BR+6iyFD$#AD4Z7oTdmlYUg>j*fLsw@Q}e?wZ{U>!ZyQqP#a#I#}MTLbDz;v)nBC%!dc(p8E@7Wnggg3KV#e*6BPXK(DiHN2y31cpohI;e2X379k)T365h{PA6*lSXaQn37D7dH(LzX`?oEwwx5S_vVttsb_rl&(B1UXKzSS$nx0(vwp;8vS#*x7ERe^J?sHDRkk2fBe5#3&|Q5R@wYLx(WoO(8O2p+6;8{tIwA=!!DLx%501WzdpL=&!fOXRnil`nWcCnfZC?8*v_8=v)8sA|9wyHRP_y1!nRmAJULxL$#s=v&5c(JiH}U)+E!Qx=uZ}DRr>W6e%sjI!Mj@Dao}o51GhyOci>Nz?H|dJA2PKC&$&}<rk_zK9C+nOLTH>X*N8rW59lJ{0;j%LiudZZ@)Q`tMskCBh?5M-kTXyg|ff(nfymL*8kNr6d<5@_AFt=V^ym?EKI_-pUx+?OK{mRb+>oq#G$0V_@{8dy;SP#;}R8`LbejMcaPEDRzt>*8TVieAHD)QWG6;Gpd;qTPyb!t^E!Qaa;N6Me|X8@P;PJ?c}!I`OiL3n^n-&Y+gWE6DTQtF#YN_&1lEuj!XTp`IEoJ1Ugpd+@tZVPF>)uPFUCrgI(Y_=0B_h~&p4~gAnUbkYc)kyy`pQ-GRxbeopQ1Fu^#mENP6_apI3OHx1>ta?XCUeqOxIKNf+yAolN3EQ#!+hmOtboyXCK&lHxuX-B$ZCm}cTH!sRwLPu8_b7QVzT6f>xfL5g8IP0fLb1_&T}>Z3d>D^f23Oy3^)kTnXi^<?r7dqIq4*mn_!b`?GY)g;IZL!!_H1ph)QnLmWxi(0)GWH1|z*F*y66B15Id>Zt&gNGGWwctf+v~tL!n?U8Qq)INV{ffBhMP<quaip$_!n0}p6uSyPe%0FHYhWojv4am)|>$w%l{w9I})>NY_&K~5k^3un62NnoN=QDdJCJoHl}^<Jpk0Pu^amh~`j!+_>i37?8J#2isq+YTP8j3l4yB+d~SHw`C<Y2JI+B6k?TvQJx$2$klQ%)=)zBI+HvWD>QkWF&GvCe%z2btHnIhVnGzbvNJ<5@q>yT3jN~GOV?Z2|$R-d`Wm-XeFV}@zp+5t!`ymc83)>#I>^<COgR39NEA`vEZw!zNW;4?MFa6czkUWrXecy=bU|q+^3)u(*ESf;T2Nh(OrP<s2%4Yx=4wn9y?42k{#&e;dM-EC$mRwnWcNFiO6&XDSey=*F0v?AxiXLR>@ijbXdCSb}P3uasjZ{W$q>rs<cOR>U9-OjCp~oA%Rg*aSg2pY(hRXLKEX=!N1utTVuLwyKG|*9_|jd6;PuQHCZ0o0{~>lNo;UDVZ7P{0BaMZ#JZsKNo@cs{Z63q!jA-iv8S!1&Rbf}&zjsE`buP;h4+)YB#Y+%McPnO={_1rBV<U%hzqAEi`*Y9!C2AmTBA6Th*pylN8#Mrg4P{-BR!ZT1<zz8PIPe^KsUf7)}&duZk6Iv!8`sDysSl;*9qCklSNqMPFX>vY7RM#(%lrCvKr!WLC-TOR>Ppr&qyL1E_A}wTm^m5b>SgpIq0bcVaC!4SXAu3+(~8(<F(g&O5cWg&K;)caK#<uId$-aY7B4n08|q65G};#xw@6FdbqxRmmya=|55YE*4ye}{nG0lR0Z_(>}Bz?-yHx8Wfo%P|3R_jj)XCGQ(jxe9xCAOZ`LWVKj*(xIFmTh=S{I7jfhwM<cP}H17w|ke1lMP5VUDcAgsb-(?M5nh)8f=f_HG*^xI$$hJX)6;e-%t1%9@Xhy(S86Ff7b2#$!5R+-D8p-!s;#(RiF5e4%eqD-0MFj)rIKIv}V$H;?AJvm2^lGebaq911TFpPBUcsuKU7)=|+Qyc>rMzcoo4Ed%s4%swb<Ufg~Pomj@Iay$ykx}_1@(-kePtQ|o!tft>eTi2Sm&APyfDjg^vXYdHk>=}xT)D+l=g3632_RmhFsQhsRQe<$g0Rjr`f=RnXj1>=P|@2-kKc}ZFI1<0h<r$nX*0V$&X$~;SdLKxzz`_JF1)L9)}T<&Yr+e?x$b}VCEuSjAlp4=z+*XzW+vl}dIV-~Yz{m?pmCeKy_Mm$>z0*eKezVg`Z{(+lZNOK$oDsGp?1Pw?q3rH;#8Hb?vxouGnU&DW}A>zFlUaK<Uw>*1bM^4OI1SF2O`uoRQ=3P<&&<lZ7vE65hTw|(w%p{>K=i<2Z5+|Mo};Af$WUBMV>_Ad_ppS?Y03BOD20#l}+>@Qd4TsHrM*Xo^LZn_Rg37a(2+eGm+d?gvg&OpE>9&^~BTYXbvt<etB?!%S`<-8Cmgs5+lq=nrrHg4#!HqP4|5(ZSO6F`6Vv5il=39IrgvcCij$MzmLfp4CkDkMN3~!QI%D}=$K=LW8NAkTy3%>og-wZluh#qm#gK3kBo&088fC2R4ZSgKL}#0E`598D|<?+2Nq2?PiSk6{8UDwbpsUNkr8o;Q-ZG|wwSCuxaPxvq9f516P(c`^CpV&G6<l}Gd2el{7MC~0-)~YiaOM_fU~(}#<w(a1QI+5?%5-Jg%g=snlb#=YZEyLmMQVkG?^3EP={zB5s7@2VN{~-nC2RgamR9sg9);afbKaZ0l8TlIRY8M!oOoXpBbm<@Sa!MqcsJVN&Tx@rPu(;9;?{`<spp6RTGfudhLz=it@8p^%>4G&sndL#Y{iDW4EJ^N3C&8Oo~JsKr9F{FztM8e-$Yy!MHVv#16^16Cu>B^YzIp{k1!&9Y*+8+N7YT5!2n;t#r!udaP`$>15d_ddoWE&3@YdUg-}wz3?~dt*p1?h9qgKNhVoELQ%fn;;%D5UC3!C1tCew5}!*=mX;>YTowk|(Gv_UC*@j}9G%-bYPaV+TuUE1;T;-T{d`DHHf&`6^D8pGr;Uv7sU$W=8!7j-g_^2clQm9TH)oAcIcpp%ObWh-CPQuqs=(-=KKe2+M@G;MDR-tD`lRSTcZJ`kGi#oE8t_}ATF`dkLhIc55b%dQ^yaxa3^NSqEiiBTFijr*hZlqcz*kQe%Q+`XIwC`6o<DWwd7HKb&JyF6jaEUm;2<^_cjkajs1N2yLV9^%Y3w%B)@x^(5Fn;O%93CEl4sp*v2m}(Nx4sOlDIh*t7#!hkiX6>YTau6IxF2yOSo0^@k(ezxA?ZALRG%4x89J|Z*%SrpBN>AZ3+Zfd$Q~-0*2dyK`-><B7p!M3EZNT{x57Jy-X$dLoCoV(#Veko_!?=ZX1Gt%?(f!_~W+Zk6Z8uzq&Ykis^1ki(B5fDz3MD-)kTWh_uI~2o9&yJ>RDEja0Q3?-T4HsMvgzjt2d41vPEG&7!HEmCxUOe&#b4(`n^CKxe;tG?>{uQ@@xkCPs>lm6IvF7zSthB*e*<$O`N{xr;SLflo^60G*V3DeX7YU?M3njBv8;QctoGex?<yi#?i$U~;Sg%N`9xkU7R4wO`dU?H{W!EeB{>TYP6$Tyg`HHm|f;FPGF*H@Ni}t)%4n^Do{vaSjZi#LKExo-6TW@mT>;TMo8HA5i<z7lFS6gnnUANkfzJX|0^<xUD=Ovk3zsZ{Hmj$vhD$jt_224mYB7AZyM>4LU;^pYU_XZPXp$2X`GyHwF>ZOPK*eWAR|Z{YVe{Bi3nyxb}qoz_zN@XbTwT4u`sa4?qAk4yk}ly@&OYE;wgcG7h}<hNLUW!<|$IkiiPjOS}DJedL#yXlOub`oBcSFE@NVY&pZYd)oV_NfuO2%SuG^Ed}Cm@k%NKMzCTq1j&Fe9Id@?3u{%C)&dSLm`9WjuEjgNo*fN>`zjFYfZ9!l24A;=oK;Sk!`$Y!%5W5*f_Fb@hr0Ddw`QxA^=t8hxvgtboA=BZ_cOo|i}ZI=Bs|^>tkQfd#FG$IXS-QL&?}#bKfCZV`b{*$6@^`ke;2xdBJe)YRN)RK24+H@cJb&4N)3rp2Ut|5I-#?|#eQreiZe0cm`RD7vIn=dM7GZ)Sd%znyKR3ymXRSp=lE<28@IKqh?hN7^&akU7$x4w<W|)b>>UN?&>asKA=TCCSwE^P5ioBgPL4%LP1;cch3dt=`mI{J7@uQhpT{$y7sI44y<_5cIWsxUoF$)s`|A;0Jw#e3n=Pur@$9&RyJb3g0ldKx=-8KM|D4!vC0%z0By09#QeMTvcgt9umcbX?tk`O!YE~L#%Mf8rduP}j<WnGoflyZ<0SqbRRn(zc8A(^E%}~B>4Iqhmr9Ef(aw~kTs<5-F#j2GKGAsN2r*rywkp^<}4ZT_)$f}5_a9@yF*{>77XuQ??y;vaWy8K?ooeem90?}-4atykRSF=*O9iTRq^6euNdoT4kajW|xxDgAkg`fLHkvUwV><O})CRlelBw6c1+E6!8a2li9^JFzeE+3o&w!-pC(g8BuL=zwZLgJ@7A}=sXKl<EsFiWy|?&#>J+w>bTW9yHsv_BTFTIb%+$(X;a?e8LYRw9?(%xkFm53BffKN07M>Kj!?q1-nTj`v6kSAq4DM&`$;Xv9;;ZtY%+oYfZx<B_V8tTI{#jbqQ?n&l*E5AyXY_4K8BoqXZ<k58Ohe0{qIrEfz^XcusZgq1z8UAIHBpLpJ(r$ul-53k{jqrG7}9aInc<9xw4XC`B?5hy(vArd|wB&HQ~GYM`z5Uw>Lb#%QBB#>?Z5U<rl!tmEoapjn74iCo+KK*g|)aHw>=;PFOm9B4+)82h}Wh)LF2ReYy8iuL1AseFpPD>wcB(_`@naiZ|?Q&cn;hU(P&TlBucDIyN6Cd&4Fb2qb;FeYEOyLNm1!~>;-Zx1Ou?L(OqU@<S32n}$B<MOid1XSKNQP9UE><3Yy9(EHL=~9<@NZ(NHL~qNweU0yZ;kLu$x~Ir3eX@*suKSmC5uqCtSZD${WYV#Nc4(hL3-s<HNH@>L`eH3-9?o6iLMTlCz*)D(;jF>VVxc$=6sk8hFvPa+k;-|C$Bu~S~V&i?DpVc=ex4SeOg*vTjr5H*m_m=w$?;=+)}P+M#g+ARa@$#(&5Sqr4kHv8A0nxYsN%1Oo9iosyUlZ+Y(B9u}Mh{;-YRQvN|Xc1CmP<5f(tC79;3fgFq}(es2hu9nR_?m2NWK6cFKCB1Dlnqf-yp1W1(#bQNCH%ysGy)~@i270tn>)tj$oL1q~&@)dMLYw6$MRzCiU`{@eSP&nXYOA;T3xb+=(An@J#?JNL3IuM2g<Xr}&LBQ0-<E^hCf=R^n-2?l7sG>fXQ23lJgzXIM$!Q;QNR+Q;Fbaxe0|jbJ&^W@INJiaaWBQ=;4p@CKIS8F}!`}ouoGYr+-#aPIPC|L9hgr#ORK~ZNk_aT@8Yxh+cVIIFtRuiUCW!%|LR2b}BY#@E{q*TK79-!EuD|KKOus+<hVH)u?C>kupegi9T15IaK?#-bCy4Z60wA2t2@V9FwAj*8${y%pNfr<et`qPJu(;yGRRZzfL-09hB4xA$FpcYXxB}K<6QT6Z&z5Z*)|qAg6|QbwhfzdYEgFUes_-4HNdCxYS(vh&HmKdZ3NjQyW)Ikkf{%EF)0y^${(rT{N<O<BH1+Hyt=dlsSza4jj*#n=BriukXb945gBa<xq|rulm1s^{0jb`^JVfP|<~&WCj}!KMhpzu-oe}c+KD?zLJtdPm+E_w#Ffx)WK3^#OuR}sm?cuU9mv|z8l#mI)F`*EF1>SuBf1DvO^<?P3yvw^ooj6#tDy6O7-M~Bvn@t{04P5+Ym*!lh<al1S1+rDQt$2A}L#wjiW;mTgDurdFZY98;>SRjDUF-9!bBoM|C4{z3+d6VPF;q?LvRJgizNG{=eUZvBZ%T3LN=JSxu!Zsj-tR*r99uMdyWNhHww5-GpA9Kk+4UNhAbm80wK<ivUV$?$jbI#dpwO}3oqfXLi+@ed&raX`%T~hY6*Fk28KM)CSB29BDZV;;_x_`G`p4yOpU&U^_t_ik^8ML4{W_NuFaPKbE!jHc8rTRDW@AlZknvt(`9-h)Tq0CNiP?nUBfZ|gR@%}k4~)@_QLg>2)m+S}E2&QPJoBl;N;&sd1)~poe9xb$QyN63fbU3bVHT6m=bzrb|8VA&a1l}k-R<fsGOl_0;lrmt`5=SbSJqzl?19reQ6u_)*jFb<V^^}`qu^dXQt3#4`7WJYy#M&FF&duRq7SuMxajddyuY}V<Xf_Uh@5xYpmG}?TM|d3F*HwZ_lbn{`Fj$Uk2aRW2yKK9vk(dX%KrAf?Bn9{^y8b;^Eck8cD}22sH-~3Ri59f&TTbLYmGt2bzE0T81+)DcOB2n%Aj!MhX{2ysA9XuGzxFY&fQ<NO8X#0lQ1U@&)G(n!ZxC#8#jD8p0!<}%wX0%@f~^k7#u@#^B-OfS>j(J$%W8xh)fL;PV448M|C8ON4@cbu!0~I)?1vNpzyMs#GFa~smjV2MpecoHA-~1PD#ckaE1U7aFt%_(=8oV)mY5CwT=h%C6=Nl!s?&&dX2V^^KGBud*I;S{?mGdMhI-sda2B^oYq`D;ryB!>Pd~^3*5u6Y$i_1g9o(5U*OV<IEW@!{j1sR<fPX-4xT^nz34rkcl*;>FYuo|@4h%bgtMzuqU%SS_=@|Ls4=6Hqb`Yr?pS6=CLlDQft`qhja0LVfrQ?S5GoH9;XAtk?ZLP2-z%A__i+e?+~J>EpaQj9>}T%eM4g>wGY6dNWqQ#@wX*T|swLLHY!{cc<MAFk`M!N9n8AGMm1Jwku6A=MLs`yp8sJ(8o~4`^cyx{}t9B~T#1OnKHf0}NgVW*VWhdVwe9D<5W-5A+AB>`_{RIKA_h6&`-LlLfr%`#%Y+QZZL-eCv(iyX-^T1}KrD{!D=f^jXZS>p62`j3e+<QdP!-u|Z9{rjI8IH3MTwbr+)kCmZ+&olO|J3l5!}~nD(e8$EdH!hsVJe4j_R{}*ZtLg!eegI_$DBTuqv7W8B){?LNNDt)eR};*yLFY!R=G*b;}h7T!W0uev-WMdFW9oIc~48zMdW}VE}aAyWx0c-gNzAQ=jnZzbh1QlqMrn-D9AjA$8J~ETpUcnk)NB%?TRc(yZzrJbN*#>Ik$1#T7qSQoXoo*Q!qBQasBszY%iyMsBqNURVUppUyfwICF9P<#Yycx3Jy=Y>acUnH-v;s8+Rrh;qIiP=Q#ci1G-^$a1z=C@nyCI>{C)+ZB?J2IsapvlG1P}fiTbhtPkqj2Y5G!FksPNZ#<rcDI+5pBfNQk@pro{qZxYmF|6?0G@@ocj^Z$k?vP&gK|{q2cwTcWo4@c-GCw|hUn?b(YLQI%V6?~I%xNZW?$NIj96r`Ux;||s*n}jng>#oMi9W4Ji8elNkE=zxhh&K9%OCfEEngatYj+lj-HA9lTh|Yrnk?JoaFdZydEGcb>G1XXd_xUxx;Fzhy3*eKYkhru=wHW4j-zyW?5FvHbe#I}+~r{8gvx}zU|NS)A*fYKrV(xbwJ?q@-s0q~(9OOIJCU6Iy~v5JD&ST-w)GdoizY(13lJP6wZUw6T#1NEkbG~M<A9S|C<9%3d+}IR$Gs6GhmwKAi6Kp?<El~fv{`lJOIJ3>zQ()hEE15yUy=wWH9*Sl#h-`yC>@1Fw+~FEcEIo_BDdzMbAYaP=wt$ZRE%1_5Ss^*d%R8V5w&Aevld2uQ%<D{vjQ_nZYLtf2@V^5$j2)7DAA=_?>pq{dDXL=<7|*Kd>s|w`yk==#pWq0;4iV@&$`s0X>4XX0Llxe9Hs_%s^nNyeKGh`eF<t_ng$_gOT~1v1tn)FizBB7Ta)ZMoMPgb#bat`00zkeQe$cAUMX1%lU2G6S~<7fLzMipHm|+xK<Eb;yfi<-8J?%dEfvbWZ0UIq(f&3L#eap>Z1ccRE280Le<}nmoF`e}5XiWqtOVdkF0|Ts^?vlCRTtUpIM|*x+-t~}^w~Qss%vfLoE1H(b<gG-9BWrV0$KUmkEVTWO!z$GNi}2U1fk|_=NkvC3>taa#9xOXkzS7N20Y4sCm%d}8a4Gc-&?Tnylo%G9v9vo_eI@xL8FL~gNlPX(N`jV@RNJVqgM?$onzXN^?&4@vJK{ayD3e(n{o9QB%DWW_OSt6w#a{nJINK(lQ5TxX0gZjsUfakPQ*p^@yBI990O)|TE3?nPIauq&CW`Lm4|F^GUD*Jp5}ZkS%PT%2qM>^HO*8tZ?X{2*n7;?EUDJgg=3U)mbv>4Wcu*1CJBi~N-b63UWPw7h|NcE#EyX4*)S?#DZq9JvY5(95$33fXDa=dHgudGPK-(7@6I>5hu<Bh`oz=!Dg*8Q-W#nuNLFV^+_I**No=z*6;|oaSB*HMFdul_$rDK^xxbg2+~~LawBN2*tPSWMtWw=zvyle$dvAjkjwb9~D74Z;we`?S_te%syH9$Z-Z25(ypd-+_TtoxevBqmsgLWM+=suk0~nu6#o271TgBGjdNfu^Y4S78N(hWZd=%;P@tRXKAo}oP)la)1yRgbN1Eq2f5Hn{@=YWhbc@a2j!0(cjz^_YB^71T^s8-EYvwgi7zFBw6A6hhMLI%y<a>t_KTPnLf{H?FvG0RZPvUV;az`r?hK|)lWZg2y@D&+w^lXoS>k6&IvjilwaiN>?H55xu@)^Ss&pQ2$6Nwso)3xavt)xGw8(#`LdGTlnyDeKnmfN1DfU1@UXq3$x7^XA<^x0Z!+Ie@ZpFWuX7+L5pX9li$=xq#mGeRcE+3zG$83(o>^BS}%PCgV-c6zEH~?mGIl$4O)j5z7I4Ry=s=a9J(!C&@i)=_59a?VD3BEjh{vm}!d#<y$p<Ne*mn@HY?Xi8N$B?nK>jxE4{}D_ZE}PXFCLnsM9U%5=#=-TPU<adGBUjuj(FjT7F2c|xSc2W_i`AMD(bqVI8|x@w+G@JAZs8*_t!Rx}VRHT?*k2<74!4ZID6$}IQ1?x1<8i@76?-pui+yJbB?R!%1__w~@cXpU*hXcB)t>;p)rwC*=Qc21Nb1cbfOr0IK%3s1^RMT?5Gu4R}4XPnAH?*C%p69Igrf={c0G_T*yjVrkA`@y;<S(R)3$d}0nu;Dm~3l<2{8?{S#MEor=9A2(mmvR!+9vh>mA(I|5w}uZ{SB#dDVD_0f`}tivdKSp%5@!21dwKaBJ23Na^zZh{UG{MY??vI`MuxdPeAs1PT~)ZxWlmr90@ZiDkqD$R$ii2NH1e>2CQOEt`wcl)Nx8?pGp$?SXolZPomRGTd!Qeby_HAC`Gx$T>;T7B$&@Oa>~8%0=cD;f&_)7|$uZLjFll%nL~^w%GGLGr*ya?xD(#H3DU8Z8s4^p3CfmZKNN`HT<n^cDKYuv8JbN%jqV@j(42BwK', 'offset': (-0.95, -0.22, 0.072), 'rotation_quarter_turns': 0, 'seat': 'WholeChamferedStaggeredPreparationFloor'}, {'label': 'FlaxBrake', 'sha256': '1aea08abac9e4fe1f534f2f759cf5ce15b1f4df0ee409a351bf50abb97984452', 'encoded': 'c-pmn>vG#jvgUt21x`<#0APU-she%m=vZH5w{|?XLsC!A94-R^k|h#0NKgPsiFWwiH^0m(00b%7j-BlYQ$Ss_@>ZEyS?J$>`|V>EPvb?DSmSiQOjMz)oA_Q$tSpLiHEEBc%(_XUdux<MUzBgXkEgTZPT|*@Q%PoBoxgt@UY`H+;{30^l^0PFkF99AR8bZ!#>z?;$;SWfx8GXve3@qGRLs23dAjgsQ9euJk(Y0BuZZW$8>dO4#zmYiaxX4aR-|c?w{Eg@ZY`-7wYBshpXjx9b^Y@4IzUe!KaSh~_~&(iDkltY;zWg^>t`xYlQmWP%P3QeqV@9X>ijyeqiGh8S4pwTRGSyvt`^+Jg4?{{cBgCi|9O6Sb@A~-V0ZnF-?97G7uWC41N$xG>9WGpTj1#xy4kHa=U1;UFFsv!zmE%LE!17Iv7%KmOEc>BIJRZ-IvQ_Ms)@2WwI5~5T4svY69HGg^)_8)7NKB7)JW7cC!AZwU209UbhVh!==qm;l3USYV%@Bg#8UJy&eA*|(da76t$ej)v=*~WDJw}AQz2x!h_a0}N>+=)`W)Q>$|Se$;$mh^)nXOXveKnmSb35bxiwP681z=m)ZDkO34mOHRC;+9O+z3y#~Uf0u}BGSRYOb`&A~oaWaWgjq7ASM!bZL(m<{5V@j5N~)HtOvvBHejM95INwM<sDXju-S?=H$F)(lM&MI%_B)3}6nrZj9aX`ExqyM>j+HwEyQq9LtynPM3jF)mgU78_oNN*G)DEMB7XI?m%!Lec`l-_6oQ8Npa)>C&^ls*I2`RtuH;)(2X5LUYWNDoVQ3ay*(Ro%1iPHjii=EL(6!+(2!{D$iqD9m$l+Vgg3QLrr*8;S~B8eW6C4HBSMf2OO>yxPX3%d>&05WlMr3r#5O#D2m54Ry0{hiz1p*1H#^z{-|u4F4B2CriM4shy*B-5%VHjjY*WK7Xg+>H>%iJ<0OjbzTJ8keEZ&ifAQh(SHWP|fBo^p^~=}S{QU0aC;t2D<K;O&yget;q`wy*t}fo3hu7y<+_3fO<@@vN>+@jX*ng1>Tr;a*lV}%-vOUK?KJomcj^}qfUf1>fXJ=l=^&FdZmC9a$-~M-WC*9Eg^wjf@pHlm0(*8u+zaimZq5cG>`iCl_1g$ah5oS2z)@RSC^D}qYny4E>(!`0pk=x4@t)KX5Ma=8mA8c4)@4byhO!hTiawC_!<g3xXF6~FU%vTA$<;^Zna_NE&k+hto#n#~YYEJDQ8JhJ#y^9kKy2B@<!O^fC(GNX!hn{}wpsXXco_^}0tShxL<RZ=HPE>*bh41ILS>Xt9k)C<Ah>LnNUSs!A_m(zlPHh$>lHS_8@n|G3BVlrTEo&VN1PiR=oSP(#3g_PSp1UPVmi)NH<9gV?F&%EX_!h-CLmDVeR&x~qQGjnfxTS>*J;4j!VtV7h2i@V&bq~+1sy{!*cqF|vRZiDS)PiPccWD7ue4|Hy(dm`bXNuL=gj&@B>1#OJ^0#HF$yDV*ZA<iD(@Ke*9i~<T1}ZYNz4dMf-QMuvcF^k*y!|N8X)Cp&Byko&&}AjbgAbe$5o3rl48g;C3k<{6K5fDC+;OQa0zi5kf$#UOYCq?pIxhmE%L}Yqi>b@yn2$*x=QlBtn)tOw535EcPg9r&CbYd9;C&cO;xW;K=8Q?t1;hXm{xTb|whIhD1k4o7Fd1pOJe;e1=8)c8=3tdY0O0r)JlbC~vH9H_(EBcFgqRDL)-E+pIRZ%gWN{ETDNl`wnNawpD%|QtknDEqeGVLAEcd?`{Tm<KJ@K;h1rvDq{p>kk4tT=qDF$n4p&_KS^nWZaQ8rG91(s>D!F=N^NTT^@5`jOwanC75*nQ%Rjp({<rxar@H*JW6CwY*>dEr#+;jxLW(p3S~3?>IUD{X)|o?xs7U!tRjALdSeU<M`OplN)Ke1~Seo00KmVKS<4e?K;u`z(Wz<uO+<E4Uh!G|f1mm%-;YDJwiUpMg{}#1L&_C_9E?5Df*8k^Va#x-SCa=<ZQ(Om;-PSSj5jT5KF}vgx_fJ=Xf~m!bQ6(B`fT;>ueShy#%&lCLrSjv-}k$r>=lXyh-XCkwP?(hS|LnF+ZiH*h^697tNGOXsuO=RKX;sU%lDwyms}ES;n$&a*7d9Q#AMXy-9ZDT|n525SK(u}$c$4KCab6uEuPQdBFvbWfZ5M1>oX&ZW2Mc$@B)4*q%4drKjDN%5s-D<g4BFtrHk5)wLaXt(mdGS;wb4S4pUY-3+pZ?H<&GRHV#-Y^p2_HKMy0v0*YC?rZ8EW8o@iw+hp*!$<iG4^8W^BMmD<pX<?NZ=^Fm%1eNW^r@Jsx1m@7$hk+(pgNu!*Zom*yX~m6yEE?4j0niG~9+^;B>qr?-;g;bK;$PPrWmGB1?##Pw45$JEO8=E<2&;BYNsm`={QiJFLOa>NB0lu)tVWR(gw|dxSOI1-xs+gu&hcrnw1dT-aTZmQn89(PG>e{&Qwd2BYKlSJF>5)jN-RQQ!4CFa;~ZD=W%iFn~$5^zaLlVC7{`cpDj~x$GxJw0aUBlD_p&zh0XLWC=GK$OgMb;Gx-qAa=kc(J<KAH2M$HSW{U=^9oOQ@q}F3iCWTco!~pjS_Oo7LRN*U&V#5zuNANG&VyaD^6s#p{?FkokDoA9hesMqUjF$BLr5ipmOQ31)>ZAU*X}Y?=s);v<Ik{xE+W~F(6x;(nP{TC`)$QNX!}Rc$)bKf1fp)zv<U3K;3vH&*XkXcbXVlF+6UxWI2eF*9!VA&dSoj5owHM~?VpLAe}BO5{ux>Hozqj7P|O~8=}B(+YhsLO-<UmP+hxbY$U7#{y5X}}%v*4uc0KyXaFfCksI@EdUQKHd^V4Smd?8SukP^e6V*>Q}RD+Jf11UVy(DR^{m_7t@<=R{0D9bi*`QVR=2Mh;vq_7HhvP!kZ$Xa-!bZC5%c2Tl2{1w6YCXUFXi;`CvnO0lKW(FttJXvs;f%RnZPhEh2#$#5{PV`vfd#i}{90?@QfMsZ)B8i&jCB&tkUU-k;)9%>38Um>UXYcfcR^<JtQ&&1kpVPB5>N6C^`~h_hqRtnS*ATf^94xULWNnl4dCF8hCH6b(08vtOpo^Z?Y1#<ARP-bxgYb0+G6QQw)ZErw_#*+@Ci~;)5a10{oE>+VDgI_%bL5AkLmZxIkI|iD9e}A3{L%4^ZNcIokjGX{WaViRPpl%MRz<q>HNJNjK^{0r`D_d0S7q$!J!U7@y~O$wn<zx+1kz$8sQL2LsD<tky_|4WyZNRY4*NArhs+#OD_tlP`so^~F-ZgyS{8v2Muk=<qb!X;Swb3nKiZf}S2;;)JpMvEYg!nBetC@X_EU2o6Mm`acy_AkcvVKqI51`v06K?J$8rd*Vfc$cx-;ZLSsPxTgq}<oD4+X3slpBEE(t!4o?K(%rv6@3m_Ipf(Cm~3d$vz|OF)m2uj7=&mZJ@?1q&5P+EIV|F;{AXZiThz-tZleNA0i6AR{lu?!zpK?pfGL?VS=EJ?oyapx0kXDZ&!7tDs*kTA4QpgXkmVev}duX)1B}QX-|G562>HkA`mjx*8yGe?Sq92o1fk&t*MMt7D-YfF)3qGUS@(I0#6wHEpbHwaClxD#z+U7+$2`iqI|akGuWXL21Qtq1(R-O0!K$!~$gqw4rQ5QVi$8=E>`WuTQQR-uC9n6}`N6AJi-z!b?Y(lf)vvZ!Zbsg_TP*rKiPN<W?fmmGp|p>S%Q|{^GYxKdpX9lYoz(RcfaGN;^8*)HZn93Oa6S18l!Z(_v-I85A%M#9N@}uk7_`Fe-1M-GvT?IRW!*uXR?+CXf3kR#jK2V!W}T+udV0ZO87xmr)W=7gWOfPc#ZpnW?dg*WhXF1ni<E(W0-JW)kQ0y5ZxX9a$x2B}1hoJz=CnmId=97MesOm59z9I5rsCW~>3<_FF{$>7DR!<PLkgX!JJ5=MvA63|_JwNd0t<c(dMpeh%uis~7E@i67c#vxhCVAETU+{g&nUfLC!~U&qR><GeHt>O#jR0xT)k6S;^~6lbcgAW8$_QTE@j75DQ(jRr6o5#=Tl>>_jrpPl0_%t1JryU*PYI~3K+aEpD(il^Vsvxl*XLmN^fTA#DAs3vbk<@`Z)?-51NNR_q*vs>K!z!?xBvyk&0ecB@=kP{^$0rp57bIEBN4mkKYM9w#MSXs~CBtLU0NMEA3BP>g(Iuq?Hry(5lgew);R|=tDMcdIz8AIrbM9cP4KC=zyfde{|LV5b!^(Mp~qNCU$hcB0?#k81FJJJ!PVaUv*p~?d(oI|#OXN&fx_$vX3Q(%P{GoKg1G{A8WjJstP6L#Y@&Yvc6?6=Ce>|n_}I0Xm3^Vd<bQn^z_dZz>1G_{GqSASf*y$&So)OKiWXE}(6Ra{s%br0sz{R36*;ZYU18IadJbPs67qAD6-^tPrCw4cmCJOpA(A60SCXn%)gkxM)eP3Q$>+-um{KDp8{g4!7Ta;sl>3>{tLSbn|tkk>OJBB6$l$a;7i*oOMFAdJ>5)PoB;A_f?&)uZQ~zKt@|mCu}1l&>-sj-osshf|f#RgrDVc)V9+F>l*>@F87ryh9%l<f@9=yFq~0cciGu!C4z-;jK8YQ+1bdq|LBAz8K}2U5+ZAz?iQ4;z+fhmeV6z%Z-~1#ElPjSWb@-oX{XmzAEGFER~sB$LcQ3$D|AboAFXA7m=eePH4Q+CqRTjth%C<yEX(YleCCFG)p-GsdrW`+_{~rNOC3AJd!8?8RqGYXdUwQJxmz#gd8<3G49Dpb0}(t$d`r4C<ysvIV8_*6(u2N51<U(*4vM-|GW~FLH?lI|9E-*$H(BvKRN3Eb#Y0|_{YWTzkfKtx(aAl?wqw=zx>Df<;$z!n_bLS^U;F5Lc8Z2`zK!e)I0V`5!ts<o3$sElO8(pXfP>--HFDC7y3`7jNC(R*FlI91u(d{q}K6{beovN=*<(+er->)Xd_b{-|nfwNL<lA_Dn?{C$n^=iUJ|~XZzr6v}nNmy)Os|uU@}=e@<xl-XgvF>izkLH|Lkur$1g^og+%9^HfI5jW+_NB#Q;~TorJmb^Sj{W2af8(jTp71>AAn=+!^}AZK2+XfU7lLq8pTrfz=D+e66wE_&a-I)8uu`kMBnM$?G`hdHZUh0`P*MM>~BN^%{an}gpu8joI+sEB-X!j`+e-7-H@^K`A8x!d9th5$|A?~)(wb4j0neZ(<C68{1lx}R_ILd^sFALrMX7q9L8ZHUiRD7#kBmEmbR+U_%-3Tdwn?AQN(O?Wr`$D1*!AU}^FM0r32Yg8yT3A#^PTZO<wG>Mkj&qD4>vkOZ4I}Imlk;Zx1fKj$i*cRuetP{wxB?qpzP9E#2S4=gFbV9(^C)A5XB@{xM$3+t+-2^#0(S!^n8Y8gZUi|C)jlH);aI%fScpgnvg=<cbqQwwh1N+m5ca1?Bt;cDSW_r%ccduSHTGL?jkiA{WveGL)|JNtt$MZL&EQEY^&(M$LOlW5Jh-jW|=wbJ`t7i)$H4>}h3f)!Jfa`|TN288FWfWI~RX8on>WCz`1e0a4-8=a%2@>hzCZ0Oj;PhrtEoKjc*4DL;L+cCuF;DJd;bHcC05$8qjd`P6?`7h>Xl$@<1EG(xa1+lD@^TIH``QRGrYkbwi5BC)kj2;s;~+5H=8er+=D0=No#T|Sw6vI!y)0c#XS9XF;w2>L#04VpJlLb~7V3^IIk!LeC-KdVERn_u_?Jp6p~j}#Uj}m@uOZYpKjr?E>>&FSS=Qs27-3?)x_a}LH1*Pt7t2+V5A0V_uB_J>&>oV;zKK>z5wcmNr>UA=0(>NF?X={D)mm~AQxcDN8uHp}4PPe9S+vut>(`oaSZp5WIozPXI0ba4L#N*1+%&!-JV2-KYYqw-?}@gQ`ew4EO<z$@*oRP8NCJf<k%S<qhApqtLSVHbnrwJNGI)PAXZKZ<Awg5}Gd(t1jkYh7Y|8#5eP0|5?e_6Iu)$_U7*EJ><_uC@%=SZAx?WUkxBqSHN^ObNY%Z#229bJgcoX0&802<kCDuJMZAOaS*yqGfZD3Yuou!XkNYvlcQI|4$pL?}9YJMm&$XdLyjP4wYV?3Tk@xrV_Bryb8GBPy?ROIjalhu5gJ6a^YoJ^JQi`wMcuB45CMXx{FuschJQYnPmOVbHP5Ia?qJ2IElme46522!}(px)VX*Sx{dqXJG1vWMJuwVWUZ;`Y=1Y{3xBe@Oh42GBXf0npI0Mx-179FIaa)?C2iNCn1|N|;^54N)=<0ab{6Hc}$aXs#2O#MGkB5qq;3r%3Cg(69>dOK^wHGYCnK)>i4HN@B!m@ou(5K-3rsD${h4BNf7Q3}YhYeJ~Yu!~m9K+TMUrX<o?{egem$K9Ea}Q_D&RqW%|znh@u_#1Pa`p88C810Eq!$gfknQh}CXtqn{7LWAaW!t+eq4s}IPZBG?-EB~|8ufQ44)c6at9aL|Q)KlVEh+oxSb7IO~CZO#-PTQ1uhzg?#XO1B*qWqY)t!NS7Aa@tTv71i)ICsuPIv<VbGapE1o0D_cRK%l3W*J^uBH&d)N|h5e<v9zVI5B!rB^q&nRd?O)<(95601i4V<^)2OvWG!~jz<e)S)gV}zVoQKhSmdiD<7JniE%^lZ}x({G(EIk_OW{p4+ozMsL_ZD=f`#r0NIOlVQ?HWUhN)$wFy!ZUGRBWn}ABc6KG8MfdDWJwDaV@C31e!?B-A{v3VBXhj(d~O#T-cNoi#gX&{Y~Asr*}s-i4%e?WqvN1JYq<3uA`O->xd6K4xrcNh%xWRlQ2mYF!U$!P%H0Fy+MR^hr;45NZ~_#=4PxH7LH`Oe`iE^?=A;4Qrg^fXF$ldj5U$ca$hz+}Ai)e%1<0j@vOi7OLN9f7Zl0BJ3%>&*x=md=QwV)w;PB3`^$2i-%e>*qNSxWs@f9w5(YfG5<Vf2${;64gbb45}yIt<>u2j`X`sxzf3NT1K|sRtM`BLHD34pr@xViWf(n9<Wem&{aVq6ia?kyg<}|Y3p$uOHQF)GX430qQaRRqkP&FGcuHz>SrfZwwS<7fBE5!T*_z@O`xpeV&h||H^d}JzgL{RuO@PM3ka-;qf0vcg!>ze78=dB{v=Z>D`;o8#$;^fvibY13Yg#_7IjIn2M=+kEU}-?)iffLuJagsaA_bp@Jq59m{s({m>&8`6zs_u?<b>1@dzpG{bbxI9wS$h<{?)nNTMgn=t(j@Fj?{D8QFkOlITD>MD#qOE)4%ca3twuBqfU@4S+Bfr(u$oTp&d?0K0OJL+3<#EMo$QX%wqUN=n;Mj<347d4RM2qvtpvIXXM`a1`C;x05aobB~eBhm$N3x5vejlf}w8Y5*7ph1x|7R`TQv?^#WGVKmqM?<2`o=ajT|mj&>YS-xCMFz6DP-Jwa=heG2%cY7Nnn%5~C%YJU{%~N&kiYE=z6Lg5)3Af|mFq#qv&J~XN?mRP%7A&_V!WNRVFky)ZbCui_WCm|LeoN0JK{NvGRph!Rwz(KA#E`r;N!8t{)guCZ4+2r`jACBeJ=qy`4^ET`Ne8ey*8^h7lTWL%P){N)r3Gzst<M}EH%sJ`h%&0qhY<)^q<0k~%K3L0SqFbD0|`JnT7t)kzHSyEOfD;phU9xKCgB446J)tA-NEtDle*Eqy3!@zLReJda;tb$7MFAXjyQAIbL@)+If?Ov59x^X<r2NJDFhvBtZ>X*W5~_IIoTXBL*?1Do_M~RllcqlHYI1qjDcq53+x9$Y&B$L_ae_8k?8@V>Fz0Qtx2?$nTT$H;=3eL#kut=VUNkm)f8-NiH$@{<m+SP-XuxxH8K&|9q>4Dh?Fq2c$9lIpz-x$T;wzJTbenPxPR)N1I5&Is<LIq@LR8qPpIZglA}>NA*rDO(Ls(P@>PaeiMtoHR#oT|PCjUmeFS{3PaGuWh8CC9Zh*2^?DL*id8{=9mRbF)w_0KYB!8^t3zQcK9yd+Ert5Vu_!;A8uj$htXMwX`BR!pdJ44skS9{jD;v_|44dBEGI&kTKZGROlDJPF>Qi(q4xiewZ%>Vjiwfw!)t0mHZD}7S%(}4MI?N&DBdOh@P&@`MM5x-@=1i257zE}1GGVlLpy%l<^dvJldahT82RU#Y}=`DVmMa!Ao)bXGs$ylNee3GD<GZ(@jA3ns?a?7h_$+fSoYhruua<%k@3ErWRk<J&qWWz?*I=>>7f7D3j$IUVeo}H9O+C$YxoVX4^TQ^?^81Z!gP?!w-0A2dr4_txS!F^QIGuItB3(8Yw7^?E<9}k7UW-x1#2O98OV_ML5;lk?NsZd;z$H62w7diTh-jsRM7eVs)zXBEa0H2{b4p4JWua<$xk(uO&&LnTsmf*4#f}V|Dsv<a;4bGjpToUU`C2|F!ylgXcn->*o_i%6;PLq@+zaMcnxz%a0bFbA&xld#m#N5HuypSN1%V80<Znb@#)sKbE-4M2hZc(?QLa%&VZ@oqLF+wq}3=W2EDg=0YLUvXG{cXjd3H`WAAV3EKw-}}W55AEmQz`vW3$zR*FDYJqr3r2uih$h>a1-R?wv>-s$Opf=xHpOAZflEM-nc5Mx1uO$APR`Ihhzx$N25J;BdQ})t;PEUM+ho0A1nvGqhSR#ZN1H+kzQ5A^$|bwZJp7m3Ljvw-vgS=Y@W-g7|%kZ#fF}fd3Z4b&iqM;lP!@A*hzY~&>RIhDY*lDQtqX+-;7k4-rOL<3WSqyw+tj};#YdXyVzrS2quRfVA*4V2r`G*qxPG6rvGCNM&$%8YfJ77#U+8j)9#g4>m^A|bA#J}(Mm>MH2EBSli)xPM!Zn1id;z~3)eWb*>bQodyo1LJ`4Ol5c-)xB@0c;N40Wl<F;}|ZWAWLg$TD_q?1&%I4azhT+BmhPiW3g4F*FQ-%fLfZM5y-hlgIsFa{AcN|`4@bMa&%{Yd8fb5W)EN*vhsYAxCVhHkTE-vbZ;O@J|*1`pdKoEz0I1qZ=>!_t-J;X$g)vk(Q?rJbWweO;AF)Hk3s<6mOqmm5AFwt`_iJnj8R-l>9?m5P>p9}c(#C6@sspcouMa^MR`TkqS-+N(-y=MpZ2$K-?2EAQ}nbu<aST7V-FnBC-PL?8e@?ErsljI~W{FC*rz!MmTeW8FK{z1eGJ`&y!4Zfi<r^PUxRjuK5kTKx+d5&>@pR_VSK5=l_iy=1l!H03jiXBSaMe~D+fp@?hopF$T<1lb3gD%_#Oz)Z-~As$rDM@bEd(gs-cOmjkKg^T^z#D$Dd54H(Q+>|4@tvND)LbWD!#D3fUtSzHMel76XR5osF*AOp9sM<X|U_VKNfyuzC8Q41p&ape}&tht;lem7=R?f(Rfdn~bF?DGtDGaLT``Wi^No9NolVcuFb*h#Y(ig!A$vd0S%TeacVX^$e!LFWSS!bIquEEvfg<ouz%Fhen4S_(%zCQm~XuFkm-I<WQ*$=6F{bOQ2xxv{Q7S2jm?6pns`4g4R<AOxd-kCNB`xH3Bz)_cy0}Lr-D(VwlnMpUPtx#&WCXn>K(w{SOxpk`TRj1Kj?Fie`XV0E}@$r&=ua;`ON}|l7R|~1V2^H=;d-m+tX;d`c>f>I`aObS7FOQ=QID5{g+1=!$>GBwxjneINYttyN@~T-!?fW3bnOlA9fIG3`nnih36q&;%o*g3TDFofwc&`s3eP|dMIE`8DNxC8}6LN6C_CQ|AML_18SOTO#Nc~jTy9GuWN8h+m<20M(jz0Z#n{gu+Y+cDl`(x)->pb{19rM%H{w{LIC2~2;yoQ<ou!&!f6LBV~{u;<2mTzUm!#$e9^&t9bBOzo^G|p3pZta^4Ih!vI<|9)jU1dZDjpM-Jn)M`E4^n%x4D`3K{CpN2ot`<h^Y!f!JpD<fly(7!SlF|Bw(I(&`$^^<dYY;GNjya`j`oJ_6j43tkJAX>oSQ_##zE=904L$YUTS*5Hj~4x2aapakvfK6D>+Cv07%p-lw<g5QrtKu$s@pZgpYq-AKJ(aN~m&VyPj@ua@O9xe`R}oY^?MFK3f>3*@k?G`a6+6*~r;)SwwD)e79-492Wv3b84sa8%ng@%_RdR!ufB!0LXjb7OMFp1Okabt=lO0COIT_kMl=7dn7?Zn^P<aI$!6sgfxgGPF3b&74f&L<9a?(MP>lvn;^ADw%w};Pt)+$h^Ul2RV8cy^^&wIiSAJ{i@lar9r4q6&C_1we=Qb*^eUukVxi)Rko8Npix}~tZVs0x4JF`d_q3p}O^+Gnk{KMkr2udDx@DZaimYqXs0^^%y@!MEo-N_i(&O54kL=#ot7mUpO@zlS<BC>f+_%!Sr7<cSu53^m!7!I`XkA&&Sg3|c@E~3_C)sIV!qZV~GE#9Fqvj^EIVdLvq?bZb7C@v{BN$wRKq6DtH<ZhcWckRj3rCv*Dtt?Yc;wFLjKnnoQY8Z2#8X<iPW=Jxil|u88f>E8WHnZqWw59--Q`<>Qd^MSTd;+~2R^ps_F;<K$Z>lD-)+>+6!76g84{3p8IT4AQ&*3-kp~q_D(=WVu>TJ=)VCLkh_i+G`vS2}`(OnxAG9zAiem!>-j<?qL^hG5x+TU`q4N&dd@wl({&K^0f*npF)rs-`l2#{2dCLH+k}oNl*yfT{AUW4afs(xgn;~Ew0LCF{3@8=iQqdgwVeO-Zhu>I@d_P=&)1N2&e)tW;e+Ss{SMouZuq%m(^e03KmG5VW<--g>IGYe0IC#=(OKT~+r>7-dKscDDkQZPPrW=945dS@foP#Hpj1~pgxc=!yz*=k)l-@<zyp7va<1E58toAxi60&O1F~)b^di>c%B!A@NEMBso)~kJH5o{=m%<i!lg&6U`zNY~;^zW-Z^rYJ5L({;X6V-l6$uez-95J^kSzhji&=h3Zss*xc$)ZiH3}$CeRsosbBs|3BmX<utn~yX0WQVW+W}OrA`CD%DC^;mTI@wslbZ|1#8@|LQ@~@ACVA>;OW4;TB1EiE(06r6naj?Lf@Bfdh1*V-${nNX=+t-PMHLp_o>fH^(ld{_s;4;D0A9m@^RYpz_R9m3_DrDX83WA1JWxvgEe}_y8%V^z7fgQ?s5#*BwpI%*B<TlKqv~AkfkphaTYHF9&q7CsaHMkjzOpZxYi_1{@<hKG_I8WgH-Z#pzMXR^l?M2$w+J^D7Ap<L$uHgw%rJ1bF8K?CIoM~wkW1kNS9sAw+N8HKycX)aJ^3A_(PvpE31}!vw3_|*<a5`YcSLg38K3FgRy#C|k<;DM;zp<__&M)cDrCfyhXSZ+3)&W<?iV|p;jWvQp#(Rks72Ts}azaI%n1uu%+4a%X)1Fp&t&CQTavgWA)?%(^Npor!m@1!*avrTZj6Ue{H|k8A(jhVh{C&R`RuO)>{P_0b{drKrMMxENx2w-+am$zQ-+%mz?>ES|w%Y5i-E+EU-hlocA9-gdLsydJ6Ll|@R65W#-(`@iix2M_v*Ecd_E4LZi=OZO#nrVW-;xJJ?7Y(ljoXOWk~$g;VR>@DkEE<GFGyKF+F9->v~hfx#mM{j>~G)8F|Mv(et7fp@=Y+P-TbOu_Ns1pmG`=;`&^A%Tto129oJP7M!gjDuH%_S861xM5aI3yS8TT!CGjo!x%-<|X&;1WQs!jgIortcu#J@8>{yr3lnu%ZW<3&r-%VeTV@SUIS5QNi#Ft2O;b=HUriLh|b#tAAIueG1?(jia!4MwkEx}H3cv((r&Lsa-W#t)0RmLSXPIR~KQZ7p13<Kc6RYs{Vw+vWSbFu8!2JY2KEJaO()vGkU2HV&Cw(s^maG`JiEj~gc6gGIhG-g>(YpD)7zov$IGGq9A&GA=u6T|X80&VeE3i*jD32%;W#^bZIZue9@d)9s4eKzSFjmBLSJ$=@BetL{xS7}7oZ#?mrsaImg49-qEq!KzqSsl56uzY%UDgib!%|ZhSy%{A`-Zer!hXC!~x9{I8ovQb7D23eNU#(Dq+AZ-j-;+d}9kQ8wPxUfQv_Y+G_`T{0`j`C{W$VRo51)MBzB<fcz6eUTHEdV=>Lo*2u5zSq;9sFsZVWuS#+FsPENIRUf-N!S7+gcr5#{9|-y?F$nIvW@dXgW^qMQAM0@!=sQU7gO=I+y=ynZ&UD)%t`V3&1<9O*o;*=ebIlhyg*&0`z=_ASGTtHb+%IJ*B(?dH+irOI&Oh2RRhosOP@-Qwn5t9n%<QjX~J_=^rV49jat`|nse{&B}M|GIAL*T;SEmXmKTrON$rbElHu_|haS`oMlU{g>UkNyn?)q~-D5Y%yVqkgu|Ro9{bpnb)GHrRySkAd2Ts>Mc`}{M1Lr1e^2p-cS83l@D!&YL%!gaCq)^)y&1k6kPfF65g)JleF9aLptZ*HkWfB$E_t;rpU>>Q<(>6Q#;pxSLA!){&o8VpQSwOboiT;_FHo9Y<#b>eT0JJvyR-)cI?Y|ZsVhsCmy|?Jj1ncIM5BZgOkugoG-H{V80~e)%NP^GxvW?P*OVf<sdAuKk3{2_5t3_B@B4<(@nt3FlFQ<V}>^uSAVz5GFoAPpMHhkrV}-ea21DPbo=zO4;m_N!1J1W*<8a@$@=(Keyx;Ts#zNHed&Pf%xxy_9?+i>9KP04e!nA>ycW(~!Xl1{A|=}7!y!25J|;&@7<?btQqzE3hqFlSh7#y(O&_{US@y{hCL^bE+PGI)`{?>9a$xj?jiGcjf2u!y9!Jwfn&ZY@zKE9jjBK3xt=)NV;KZIe`hsg6-^AcnDH$cS{nw6hbn%uXZynw2Yp`>Yvwsx1u~i+o)vj&*<nf|8q1y!r0g~EewmYm;M5Rc+w^IH8{RnGE85lCyi^r-tf95avmi8P@3~6c|*Bdl%n^jl7bYpYvYq*=vA_r3ZZJMwKNIAU3^ROOIpF(2T2bNO1VE79sx8^h50NvZ+lMwRgF>3i^&ODKPgWBXCQ9pJyYsaW>%B57ttiTMC+xh?T!H1}puB^@;<#eew`VRXBLG{cQbd#MC>!<+V2MPBtHiu|{i=T_>7Br2`Odo(U;XFq^`iR7Rz7|y{23OTdP>a$u7(sg~W|%D~IYU_jIW^dtZ0B=|iDQVz+|B^>(g(E0+_b&%gcc^NbQ`pCZM&B!`M0*Nz2ZRV=l?khNb?Jl5d?bP(xBWcmO=0k?{DK!;#Z(%n<qZ3n1;!IC=4x<Ct2W7$STXL<bfZB&}#G5$I(Qqt|;#W*bW=vHRMZ1932+ZwYGB3iVkbTv-^g?+6|CEUcQc_=@=U`KCd{eR?Lzh+`Jup;{z*$MkbrY>u^Y<$+6vmXW1X*Lu5~*rrzg!3;tcO9mCiY!rK$RsE00S7IAXWuvcgLO2zknaW8rF3j~gTiqGfDKjfXV4;Fm;Qo43uhSmT5z<JbX9~!`Ai~LW7lU#8<33E%aEcV1cHN^GL7I9I1{$V)|p8<0?E#ET?r#jZ*=3u44%0s?4e?>AyqSCkTeK|zqM=-fQTGK*RizW;641>o)&5~*@Lpa75XPvv>L8gj_ElFrJGHR&-kFxWjm+jcSQ*#>0X4I?F*S*cz`A=yO<Fi+s!Tz09Z2d33j8$8@jJ#$!LLn8AB>H}}#<T`RUw*5`X&2;IRJlr6Dd&(dacg@Pc+8xuBUPQ><xrbn=YiyPSt5~E&DG!jY!&LPyZH|-Vss&c_-?*q5%cGZJN&Uve4CiB7g#$N+40|GwG2|S*_RvKAYUzc!ocM1Nb%zzKcG(1bKAt{)!PT+L-p&pDbp9xv4*5txxPhjo_6={eO0>q-CUMiZJ1@-+BXCm`*TOS+y!VmPbaMW8|c=uB$vxQ8(%zodr2A%B=Gq&u*f9~w!ef%RUk~J$d?)`2}4McT9ffFIqCY_O?SS2?Q#-QLqz$&mp3jZ-QTR2B$z}JQsxoP_MrYbWzUkUaDbV%2ynht+i&H<&nCAP{PB)NuFKGHeB8&MiYG#+cl@DoUU9qpUxw)+`B3nFtoU4&C6&(_ama}q!h(51q{SCCE5i47zOkV{4@PahNgA#eU?_6~UT;)5Yct~rp9tsT8V0;oLS>c*L8sUJD2Vy=7`>V6HFxuRhNawYo9`Q;`Ta8HDYFy({ILNb9TDBX{MflIL(n)jMVDsmYEcAIUT)M>r1xqg6u2W(7V`L4vxper0~LH+6|{5z!+fy=-|~I1tx0y|RzHe`@daKu-iv}2f{aG}Ql1h2A0=FVtwLXNlh7U-qq?D!9x~Va4_W7omXcxinaKO)T?Yzg$OjT(`wvG6`5rVd^B;^4LN)wMfbgn_aHD@>_a6?qR$su|7jmUqO`!U&r@vEL2I=`z6pcLIUpZ#M&F_YutF+wX-hJyfGM{+)R@y|emD@f2;MrSwNSvR>51y@X?U79Jvdiwq&;Qp@{?=q8fy3k|=>&>pe6JGue`X?s0x4x}PT{K3miRQ@m@K{OWW8lh>&+26AE}40KmOy>`}6Db2aniW{}*ToEi3', 'offset': (0.8, 0.4, 0.252), 'rotation_quarter_turns': 1, 'seat': 'WholeRaisedFlaxBrakeDeck'}]
floor='WholeChamferedStaggeredPreparationFloor';plate(floor,[(-1.65,-1.24),(1.94,-1.24),(2.08,-1.10),(2.08,1.01),(1.94,1.15),(-1.65,1.15),(-1.79,1.01),(-1.79,-1.10)],0,.080,'z',0,'Whole broad staggered common floor; front approach empty, no navigation claim');FEET=[floor]
deck='WholeRaisedFlaxBrakeDeck';box(deck,(-.12,-.10,.060),(1.75,.90,.260),2,'Whole broad raised deck under both entire flax brake skids, no load rating');LINKS.append((deck,floor,[(1,.5,.070)]))
step='WholeLowerRightApproachStep';box(step,(1.73,-.06,.060),(1.96,.64,.170),1,'Whole lower side approach step, not ergonomic stairs');LINKS.append((step,floor,[(1.85,.2,.070)]));LINKS.append((step,deck,[(1.74,.2,.120)]))
rear='WholeLowRearPreparationBoundary';box(rear,(-1.67,1.01,.060),(1.96,1.08,.215),1,'Whole low rear boundary outside full original bounds');LINKS.append((rear,floor,[(0,1.04,.070)]))
REUSED_ASSETS=[]
for row in COMPONENT_SOURCES:
 raw=zlib.decompress(base64.b85decode(row['encoded']));assert hashlib.sha256(raw).hexdigest()==row['sha256'];E={'__file__':str(OUT/(row['label']+'-embedded-original.py'))};exec(raw.decode().split('# BLENDER'+' PHASE')[0],E)
 prefix=row['label']+'__';off=row['offset'];rot=lambda p:(-p[1],p[0],p[2])if row['rotation_quarter_turns']==1 else tuple(p);trans=lambda p:add(rot(p),off);mi=len(PALETTE)
 for name,color,rough,metal in E['PALETTE']:PALETTE.append((prefix+name,color,rough,metal))
 for name,g in E['G'].items():
  name2=prefix+name;emit(name2,[trans(p)for p in g['vertices']],g['faces'],g['material']+mi,'Reused complete '+E['ASSET']+'; '+g['role'])
  if 'face_materials'in g:G[name2]['face_materials']=[i+mi for i in g['face_materials']]
 joints=E['LINKS']if 'LINKS'in E else[(a,b,[p])for a,b,p in E['ROOT_WITNESSES']]
 for a,b,points in joints:LINKS.append((prefix+a,prefix+b,[trans(p)for p in points]))
 assert not E.get('CONTACTS',[]),'No untransformed contact records'
 for name,p,q in E.get('INSIDE_TESTS',[]):INSIDE_TESTS.append((prefix+name,trans(p),trans(q)))
 for q in E.get('GAPS',[]):
  r=dict(q);r['origin_m']=trans(q['origin_m']);r['direction']=rot(q['direction']);r['name']=prefix+q['name'];r['targets']=[prefix+n for n in q.get('targets',E['G'])];GAPS.append(r)
 for q in E.get('BORES',[]):
  r=dict(q);r['origin_m']=trans(q['origin_m']);r['direction']=rot(q['direction']);r['mesh']=prefix+q['mesh'];BORES.append(r)
 for j,p in enumerate(E.get('AIR_POINTS',[])):GAPS.append(dict(name=prefix+'OriginalSelectedAirPoint'+str(j),origin_m=trans(p),direction=rot((0,1,0)),length_m=.0001,targets=[prefix+n for n in E['G']]))
 for name in E.get('FEET',E.get('GROUND',[])):
  g=E['G'][name];polys=[f for f in g['faces']if all(abs(g['vertices'][i][2])<1e-8 for i in f)];assert polys;f=max(polys,key=lambda f:len(f));p=tuple(sum(g['vertices'][i][k]for i in f)/len(f)for k in range(3));p=add(p,(0,0,.004));LINKS.append((row['seat'],prefix+name,[trans(p)]))
 REUSED_ASSETS.append(dict(id=E['ASSET'],source_sha256=row['sha256'],unchanged_scale=True,unchanged_material_parameters=True,offset_m=off,rotation_quarter_turns=row['rotation_quarter_turns'],new_model_count=0))
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
FOCUS=(0,0,.83);ORTHO=4.65;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(5,-8,5.6),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
root=bpy.data.objects.new('OneWholeFarmPreparationScene',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole horizontal bounds centre; common floor and raised rear deck support entire scutcher and flax brake';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
