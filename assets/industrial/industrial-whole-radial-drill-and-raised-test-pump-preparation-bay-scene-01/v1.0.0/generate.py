"""Whole purposeful empty industrial preparation scene; two existing complete models reused rigidly, zero new stand-alone models."""
import math,json,hashlib,sys,time,collections,itertools,base64,zlib
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='industrial-whole-radial-drill-and-raised-test-pump-preparation-bay-scene-01';VERSION='1.0.0';TITLE='Whole Radial Drill and Raised Test Pump Preparation Bay'
DESCRIPTION='One new whole empty workshop equipment preparation bay, zero new models and one scene. The entire accepted long radial-arm drill stands on the left lower floor, retaining its full long ground base, tall column, radial arm, complete head and motors, exposed quill, full cube table with genuine T channels and all controls. The entire accepted open-reservoir long-lever test pump rests separately on a broad raised four-legged preparation table at the rear right; its full reservoir, complete lever, pump body, gauge, valves and entire returning hose with corrected terminal coupling remain intact. A broad chamfered common floor, full four-leg table with two side rails and low rear boundary establish a two-height empty preparation composition. Both accepted whole source geometries, topology and opaque PBR parameters retain original metre scale; only whole rigid translation is new. Whole sources embedded and hash-pinned; scene normals recalculated, no raw GLB-byte or hierarchy identity claim. No old machine part crop, rescale, component deletion, material repaint or accessory extraction. No workpiece, plumbing, hose-to-drill connection, liquid, loose tool or operator. Unlike the whole bench-lathe/empty-steady-rest corner and slip-roller/bead-former corner, the full column-and-radial-arm machine remains floor-mounted and the small complete reservoir-and-lever original is staged on its own four-foot table. Preparation arrangement only: no drilling, pressure testing, machining workflow, compatibility, access, ergonomics, table loading, stability, manufacture, engineering or safety capability made or verified. Rigging animation physics interaction not made.'
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];INSIDE_TESTS=[]
PALETTE=[('MatteWholePreparationFloor',(.26,.29,.28,1),.97,0),('MutedWholeTableFrameAndBoundary',(.19,.25,.24,1),.91,.06),('WarmWholePreparationTableTop',(.43,.37,.28,1),.92,0)]
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


COMPONENT_SOURCES=[{'label': 'RadialDrill', 'sha256': '043d415280e36616e937090f669ed0b62cec508970ffdfc3ce53d0aaba8dc910', 'encoded': 'c-p;vdvn{!j_?2a6x=zrMKY!sNq$BOr`B<tOlmStuI)LG)m5n|iINyoBu!GXl~lg_;s-RJlATHIxi?j@$!0&$XaEhMf%Y%I{PHRB7k=ml+QTvmJZ<hjdNVDE!iAQ&GoQ-cWTm;`Oq;GJUORIqRB4v@LD2TYH1-p!y>h2ZKlBD#nz@-jr52eMg~8VT<(FSt{wj{>edT6L>q{Di*3wOvfj_a*ZE9uy%Cn|X5O~wfkHXaQGcU=aC`eoLBwA@PwW7M3>f|%Mwr+0EuWuc+wDH3*2cQ1Db@0g;kLP~ijmM^)cxe=D=%XFGi5F(A^P8K?TSxc9**eV<npc}=+Qv-VGSfEAv`sT@mosh4OgmkD@b}B>n-8C^9KCCI?2bOT{c!v7($U{BzCHq9*MhHeg|7?hMZ0Buy+tp2>+R*u#r22Jx7^LA(9=TiA=ql}I$K7-V|4}QK@=rw2?PqC09BYSQSUtx!u%+)wR6>+mu`|o?o6Awsi#fdB=NnJ7R1vsHwd)An`hc|OZ`!|Qv#Uqzg~s1#<Ub}Vri~)GmTbp;ANgh@cCb(FsqP*tEC>{)}^oWHFXQ5X+j?BaONdcNsH$5)XOwl$}rOi;&2vtwsyPp%AOY<t<S8z^ax%zj_J(}r!)(IOx<S>E+L44$*36(ZfOsGwxr>CRPQm4Qo_UinlNN(=@Miz3D)I!T1XWvEsJ7p6=j6e9A#9tOgyih#?hUpV4Qm%kPv1`6!0ulf97dX?1kErULTg87tjPABEgR|TC7nCR28RI4wxXd&F#Iw+Yn<=gLImB50!aZ+M1pdFx1AYKo&#~Uh-1DarY@hGYQ=AE{8AGCY~TBV%((e%F9_%kSqjISr}qHnKYq2T>GGiC~oug(7i{r&o8&_R2Wj5(zHX5#_~g^AdKyY>u8;7#9%&w6wS64;W(q!^1}?WgZd?MOK1{=c_LvyNQpcNC*gWU^PAG((aOt`ZG-*?)D6ukoGwMcSlV4kpsx5)38N&ML>aBK`yhnvE<6ks1v528&`hf2g*UUcKf}PM<z)n|K>i7#zO6{UGMG@+g!vF8F1<0*y&$7W%|I`H$~Yv_##)6bR!uk+yk;o|^XFLXwlI^T1WTLKxHLG{XCX9#afFx)RskPaP5vsFr6PiX_W^NQF}ng+nx8R{gv@CYrQnX#oq-bwOw?+pL|BX-Eh8#SH(rt|3b8eaC83*DH1h)OtCvJXwjQmit=))x_f~PXEu?%OBMA;CKCR6|l-$L>2jX_8*_sxOuu5~bcybtW<I#euB}gCm6T|>M`Ju3-3u;`@>aIw5Tf*MVot9#^IfjbCCg>_6#=v{xP5qSU790dbuH0}v2NVfG<0XqIj8^`XsWWxw9?fFv#_q%q{A_D$SA?;MK&LfNumm&OUP5%o4Tu-#QL+Nt+S;|hSYRF9(5IaZoPq{mfW#Hf0ZXjhnP=;*_s+NPgO4Ase!p>sqrt_etK0L7TYi3j{+WNj`E-5B5AQB%m!jVvu5LcOy&T_O-f+d%=kt%3x3`zh(9r)_)5^UkCJz6Bb$UaDM_bN$IQxyTrdx*HeP!8)9n0>WSY6YyPtPp7duCdOezA0uY2*gn?m|fsYIxzsDH?W;k1e}%iXSJ(-1dyR>7JnNTOwH14(s-Ruprcw_qUsj#3DL4I<f2{8vRIGpHS;V9{C?c>Te*t)TlS>gqFqQQIDws20l6za8GH-jyY=0ytzhnYq-|L>?a<rVW?$mVg%#yV5`wmXphzwa_Ordb0w3Tr0dDPChcdMtkwa&rOhTUQfYz)uGE}GS*`PQy`p;0bj=)CZDP2??&!s2*c-K7`aw_Kk)@tGDC@{qOFeZ_)|Ic)Wk^J5xCIDMtnBnY$qWI`RU@xMKdV;bId)&F)>6k?QJs+X4Qpe~E$Ydlweie;OWQa@!9o(zZf=l_b2H=7v|gD7N@9MD@wgcc=6QpAF1|<cd_*0ATs#Me0(_g{Jxyd}310B#(;NRj=#ECF`SL_7+w-H3N8-nYXLPN=3u%OQmnNY3bJhFnPQMsF@mQSAs8$t_fr6tgzgwC&TX?BcQ9bPonklib!K>APfr|3Ay|?a%-Tvs{e%S94yaSgcEJ;EV{6^?FUD-&{`OuiqVvJCRF1TAOL^u4|CRKNp8YY#w07&&C@cr8L+ON2)&TEI(<u&H5WPmB#1C7T^@27L0mYV3bvL0Gxl`OTw+%ci;{SfaXXXa07J!njy7||gD07E)V1|Ae-C#MI8iGm3Ray%WcymV>Mt{0~umCylj{0bT!Y<RKx-5S#S?$XF&h9=Ejz8FOhSlSoif!|zts!YU$!n?At)`}q6ZPfqb7(`g+e};p(4YiAC*|@_17Jh!QjJpFKuzd1CT8e21DJ}Jn*@eVsKqL@H!4~696DM$2lbH+pu%>;ZU}5uxG0j=mY#Rj|b9r8eD0r4SfuCkZIUnwu$SPWAkozEVptF<)7~=){YS1MbTKK`#$q!7R#2hq?t&nffs1HjYb^;AXAIx75bIg5_&OBDrhzR&IKGHB#hhBzX+9a&-V0-~m^DaiH<3rdn6hn6;fK1fy>BxNT5Jh);eWgEos)ZYF4N!94a;;iy)bG2I`K#0BrVQfR+7O6C;U(g)DgB&+%gll_2q5%)#~U!!<)s;!wUG(A1vT(@LO75VN3rq6985_6xTAWc_j-NONk}_7XYM39ahW7hV(3>9bbF{}qz91>87C1;Po2<P>0GEAC^83%r0A>A(qopaXWn=#+!<Tjj<xO9Wbj{KdMlPiFIGHOWR-JV45AiBjlrQqgLW(HD`O42){sXZ$u{<t<pzs%#dC}!rj48f%>LYF6?kS06$)u34nk`}|J{So1bP28cJwWu+I+!(K>5U;Bpf)29_3pQSxdjUV^t=FIShjc8|l)gpQB=?RM_Rht`t71!VVYG-ZZMiFf=+=&tl!gII@ndQw#b~$LiAa5k2*+6Dm98vLkx#(NmY|pIXP}r~*HW&uAvy0%J+>(F&bz4|8~Mc-MvsgS`VpGk2(88qEZ^Oj6^4CS$&~Uomkq7#(x4mUgnKK3LR>+HN*ZUa%&-vY>Q^L#R}-g`ZFf)>iU@w~=X-%6^i$>lgk@lD8JVZ#H>_)DIgKWP`0O@F?Gcz;?hSt)a8CX$+oRV_D@mfb>y(AuH`Z`sx2a<}fm>5Tl&NbsYUsXLMuPGMRQJWJ9o32mBeXnOaz5%WxIfOn;JVzA(=a?>xsfK&R~SZXn;2=po&uyv8~WiI)!cQN|Zqcx!vGk0$t&aNn05nqbbf5-ukIM$gdz>&@(+@{+OQ_s5R)*p)s?;IEwCk+onA)p_UA0%0aG*}kObF<7zxvUiX_T@8}NNnY0HgmSF2^ukP~B_*>!q8ua@L~!p16+XD4ITtm6k3BV-d~#)$l7}ZYBK`Cy8Ks7#uTp1feeGCZyG<1BUtj1UPb@Lb3EImOt9-R*mDP+`>M{(YXIHq@g1f}g*`S2)lq}QL+)KRKJ2+Ed(&__|0_;~A8tty#IkVdKF$8VbK0GR)$!=`hM@RW{{zz4%hBPgnyQiv(Jaf~L1v~f5(!c8TBw$q?sfs!Pi*70#9WSHSJc=?k4>62C!X@!809N!tWr0wU#<Wk)NMO@ouy_Gt@3cB1wapzPbLqqCotff0C|IAn%JIS-Qh%o;JIt1}RRG<RX7$mVXV(B;psRtT98)DwhqTj?=?~~=%TqwHOG|vxyG~=>I_x#UQ{6I@C4f{<0T{SRW#!M4)kpD{UGS$%<pXU(3b%9tDXkpseD-ON@YgwOESbWe^1hWm)iBbMbr`bu&Cm8BRt=*jP{2-P)nVY>WL1Iux56hbj(?hoJ}A{XxT?_w0okQh7Met7hn43OXcel?X_x4*EtG*D^;u<Z?1`h?Uo5kRL!KuW#n9T>%M72I-kcrksTuOrdNMU39F|a``IY+rkf3};b&gL*kRj~hRtR_p&o{8}9^SYce9;f6g5i_;OiCKp#nhNPyQfFi*S6j13TyVxj!{UTz8*+nuQt~mw>r<S@b^xG{FGoCxc+KqqS8e0PxQe!C7HzYgbPwl;U@E_!R$RBK)`oal3uxr?2n~xPJpZ4(J{l{fq$!fJHw(LmCvWLz?~jyok8r_CzZ#JRKZ&JUMYuLvDT>o#jesci>7x40c&o?9{4y)eQ`K4u4tM&2w<Sq{LhYLnP2hr*^jE`e<?>Ne^=T8d-Q5tCub_$1%cXSzUwd^UJ=wsXXUCjPGLk^h?f{2h}VvqFiO=Ny=n;beIf*@PH*zH!nw{H9P8Xj`4zey6q=2yUG2&~I|FiijP#=L6-l=aFIHvD&f&3?j>;+3&yZ?Tr0{jaD~uBZnqOy!2o*#!&)O6_-Lrxg`AAAl5;S-l#ebk^uNW*E0QwW^u5*etIVCFU@gCRhR7fdDj=0_HXJ7kPr0l&|6&VAh+btlTx^V?w29|)naN`|Nsb&>W-dcJLquuS2K~?N9<<T6DAgQM(phJfxlobGb7ytnNjn6OkotMaI6`!`q379&YNW8We;us`jIBts*FS`W~1Q`SDODBOWqO0+IM%x+-Pbm6B`xS8p{O8BrQ6J5<1L|OUz_I{!t>WeM>{z{#Y-+w8cktHU`zAHpwO-oA03(LFz#79&#pZyqkShj2!0m-h6vx!;#jlDzuFWnOLNK`Fu%Z#v(5nv0Dv15T(PDw%9kC^YD#gZTsc3gkm{)4&A&mw!$rDs%G^u81ontuBaJ-V&W_KsFQAfY=;Pmxox5?W3L>~(j+};EcX$BF8M2uHX(H)WR%umEqECzX-c5bp57uk~Pu?)}LWZ`9GH85EDrW&{tFOZFOXy~jR>ZE}3naZCy-_?n|UeP3JgPqhg$s3#%^Y*GAa4)>EPFP=H9f5QpY^r?1Li;)Rs&{(Idn(F0<$9Gz(Q*LITk8(~Ck@TVCMK0#lUvn+qYf_fV{L|Xuf*bpN^i4!#MOMv)5A7GV(?XC-%oJ>2<@hMU|tiyOD|xtR-O+kJ;3Uo{4CBJGMk}&b`1*L&}0;Hh|X)MA!+y)$N75^LX}H3w#RJSBTWJd{AqK=SRmCS1NKQqblFr{sb`oq0$nMw1we*wkIa^;Rq%QO9;u3C9Ua#twgC2ov{qdKv<ghU!y_f7FLDvG8-l?bX1f}QF(|ZKNE-Qq1-DyMNA0VJtZN;;IyMLMWmQFeN43?N<8SMUK7a>qzASeCR~^+XFF8EPJA#T+*`)Twhb*bXJv%>jUsr2h9jY!1MY}Yd520AQj(u457#t4Pj!_uqE?BuR#Nidp4ZO<aZh*l;17|-Y`}n4oc=<qSrdcl{#T&EiRM@bbWjmiGuMIKG&OFJ)TUx{VAY|q7EVa8Zn(RV(8P0yE4+WgD(*Wq$6yVX^f*Um6g}+fmzq%F5T>7Ll*Om!N1^S~o?AWS2PS}`5_s~>idKqRU^(6?1;}(+C4GPR8zC=P19axoMD8#MpQj6Vs$O#j&^HzHE{(*?1f-)bLxp|@VF6H9ro>U8f=5omxxFR@-iLyD%hk_!z(80>CFiUud;PezV=8=7Ls7S&ex|)p7`%U$wbJmrYLwO$cH>~SCa_<NGoyu1x4|}lRqrBHo)|ykNcQ3B^!0zfm{GeBs!KZcqd1O9O=9`V9!lONX4`>0^l0XaCS(a-b20ffuRFQpH1(~rb)4+TJQ}ikR?(Oim;%UX<HU1{CMwmV7RaUCt`5h>K%=z6N&hNbH3G1KLr_`32D3(9l<@kpkj_(Px?9>Fx8dXV)5^aK%#c9qA92EjfLWzja@cQZEL*RO1J(Fbaz!h<F!b%>O^v-~sQ<&k0rP+oEIktFmHf28|YYr<nxkEIRmu34LBx<}|c%ODyc(ZG!^Q@EP1dyE`vXi7D_?lCziM~S0VW1P9-!Ul^<?A88((3ifHIms$99urUXGNQu(y$!lRB0{6!T&Jk6Nd$6_1@mN!P-lWGL&F3)bpzPXf(L_?ZdlUN6t0d#tQ!Kp+71E4^&l?$o=t&Pv*;BamF#E{dZ&@5HkpN8&LFXqdV&CieY#P!j_7&;<K9l4dN`7^I}wqGmdTKR?V<0#YuSw{Bo~exP#D&EsheYwi7|h#jrp6_d`85C}<AcN3}%tCxJ+wo30aYOg4}|9p_<^MUaMtz~yie(5hWUA)j`rs1YLRqL%46czsX1Fww~-U*I_MLz!z{ad)w$&ZvlKnWSood*wQ!Pt$ze^V+Ay@HoQf%FRXR$_G1SqWW--sFMaQ6tNd<uO;5b_a4USl%$iRGg>4%v5jL4;sH2mB>qL4z|F1VWXtepaorQU4+_@}?20H+frw=N(@*LiNBGfPx6tvJJLVI?0;`q;w~t||j3pX%>?W%*jNmbwd}Ho?jF?CVrlr|>_vzx#8+CwdgGE1G-~RT=Ikb<D2mknRO$77Xhl}5@E^ltggzR)qTNmelTwb5wIN$Vaxn4~|*AMi*L0aUgb!7KUOTTy9tXohiiKin-L@C8)#8o?G8L8h~uY-eX6inRd9hX!ZK9GhpPslE=541?!tqgT|zvl~j;tvEv{vq{)Wwa*Yig1myeQ-8vG+_Qdkm-+aF3vw*5)!_X3ijsX<<;BEYwh!I=Qo!)IZ~+rlXz=QuvU^Nfc<lw`9U7~tNopf^(bk4v?rTo1|Nm0^ycrs-O_7|I<uoVwWG-wYG$YG9~d)Li^;FwTz<T~xTP(lQFZ3Qj4{@!H(mtM#0}IzB+GymXr0fR(Q4*quAK*0rDlJ(%uc*jwDF7;EN(CK98`gvC-cwdk^%p;aoRst+gNI++cfh?llkNF_WHwxzP}Dx%-&cW7EV{Xr{Q4v*;MG$VEV<sE(q;;`{{N{g2ql=SZb+5>(%%`%B|BqZPf~a2Y2Si8QF$oZc3vIN(MU>XI>cjX;Fbuwh4eUsmiP$xLZ<n`kUanmTJcIC5&bSY;{02NqmIkioNFzm{b*sJ5I+4e0KDAAO3myR^MC0IjSSjU%3mf#5L!jaHw$R=%26NH#%w5CeuAi)R@=r-<&sUQ)jC&hiOY9i<<G}KR**aUcMzsA<L)t^YtS(lQq-(v}l%|uZP~}rj{;<R7fm~OLUi?hWu?rZ4~MVR7P>xS&7r4tcpm2OE6g!>;0qea(o?ybAMrA8&fjBoXj2qt;}m5g;po}W18H>!qepW1Zp;WEAw`?*-ONG(byo}211`B;U=D+q~!|c_tlZbSghS-Mr$#3@@2`jfT`o;)MicdFt%xns5{NAMu|QEAzQTFE|#>3;$)JLpkh{OiC4}ZffsrY?2|PID|_b8=Q2g=$Kjt;S~4}Z)Isd5Y`l&k#`!6=7o_dzpA$cv`a}pb?aj^GcO<D}+YjS)mJW5q6KEIcP#=-Rp1bQH8?*AGhAFFF1N_iS)18_;u}aN9FvY;1?o{NtS1O(d@zUL?)wL^CZo%IxKSi#A_76Vc-D%LNHn_|y-w+-k)Av=!3gzYiZ7J2wB&I#zqn6MDA+C^T2Tmdmfn|v;uhU8p+fXc;Y<RL{NM0+>!Hd)H!i_HJZWimPx!5lPt&5I`4etz$0b?l2hC1ji8~ZcTk~v#X6|){OF5K_*Rd4@GS09y9w(--oE2<ZLXG)RpO3$Vltf77DlG;)^Jy%-e6o)`aK`IV6M29Ssdx}K5N_yA6+(?yyl>;ceHfC#$lnH_XNs#tzy^2#qF`bo?GBUpNwyDw^If)5rAd@YhSdb=Eu$eNERP;C)%d2n}DMVh4tvnkl&^X@WyHT^1tl`L_0!hReaou%1gH3A=qWufc5UhT<su6Xd5-%N~p`}fT{Q(^JLR!>Hz~W#e^d}#oSkW@O!E_9$#z<BmF=0$rDmq=1DQfJpC5e8rsM-s4>j8cVqhkdOY|y8<l~SkV2{AsbdEKO^$~gL3L}7}Ey}aQVj`BxmAp(a1Ec(=~A)zvVB|G#5jE8DRCK*62EgFh|4+%A6ghLTQP(yhd@Ve*V5fWwjRlI&A&@!x*jtM}>$aF<`UMlUN%If6?RIYAmM|K7!IMby!y<@V2a7~f4B!{Hqvc96kh^<9H+kbv-Bc>rLbZ49vfS_#8_Gx2sLw}C6J#^=xJ8H*?5hijqs7IUWK++bB)L(?8Z!&vSmRY)&nh2RIA*GKqZ^2_`Hc_Jcx{M;vIGa(L)?1l{Neh6T4l_4_Q08NxQ>SCm#F!VT8Zs*^Dz2dQfKA7zMrdL@U+`~w$Yz-8S})q@{inNwQ3cc}M2%O6dLIDkVHD;#9y4C`K7iE;Qes`u`M5Fwm3}ACc;SZvz{pYNk^PRA^Rps1gT4}(C;sF3AxeVTe~}s#l}e8SG8Zx=W5idK6-DL`mSAMjwpyV$k%(H85{LfGs6lIvoS_;_vX!PX5=Y<~4WJuf5^K^dOtXx=E#V#g2wqm7^4BpL$K$1+rAAS~ime&sG)i}4gNtfNwD7u49{WA;di;#+hQU%ra?dQU2fEH2<WhNEYe|^VRAe|6o3D4WEc|febYIf9L7F;pqT(W8937-7b?|~}4DQtcRN{3J1C7r!>t4R9;d<&_hFq(}48<e0xAnp1wbMN)3+U<eb@sZ~=>rQzdPM2%L9qn2`XSr`ytWqmqky}=Y3CBI0o<23ldyx&+iV#jV3Jn-<cP}H-=m#hy;aAHv?dT%$niv1Z;43!Db8xrB`2SQJs1Mo&pi&ZVy(bUwvxX`y&;i!N)+MJl1)h)NHxw2v0EiD&Qm06l3;h9qD-0MAX<3~mz1{7bL7FLjwCq7rX{4J9;Wm#2wZ1RI^ZCfG>Rw4PaFi(M)4GhFf<MsGfv>X2qrIr=|P_Im_H-c<3->eNCTIiC)9-DKX7_-vO`=F_7ng@Se#=+QZhvTkppt&7B7vX7b*^$0OB?By^>1`rB9CXyOw=;N<WT!uiz-}o#1@dKI!t?5z=0Jhe*^wEQPS!^K8jU6U7)60CEC_*o7}uk{~ndtRlS7n`!=MPZAM1HKW~S20UhxFDBy*aX#4{<(ZfeXx!#uZ)LdaIz?sK&$YctNQPe0WKQ&aXT-KG)K2(I-33t~f+Te7!ODkGjAgcj*~VlJ%$Os_sTa&MFKw81u@#Zof#a@*ue<a>SJ*Zcg@p)`=O%erJ6~0gK;M%<lsluSmwI1zM%992y2c~}*kJ1ev1F@9W!YE_A~mH3ZF8+J?B~v>$j1PMcbrcG;F5?QN<!q%rH35!6+7Z$G!zFHQK=5x-7-^mMAlU}8;6K7CCxQ9hle9ezD@RhD~#?M!rTIvwc<%pT#WrI+{j(a&_9G^2KqCNXR2Gp6s@8v7#(vgam-uen5&Ifq;vQTm8H{s{MC9j=InMqB4Z}+1J#Nb=nsO}vP)O*yOus7)dP#Bnn$#?25u}P(YgVO?>KJ1#r+Cz0=Ag6)LTew59>%YMUF5f^Ck#VEBE=Uz<f3bEItw=Aq*+*rWSRmY5`{|IUj+via6Ar8i-v@_z+>?C2_*=m+>hQ#5##)#5L3*8p!!WDjDoV-674@%M!T-fDaL59|7HSoC@v}*vjP*0ZjV`3E^gQ*XBL1v_~rnER*_IYaL?)Bzvr43l!O*&#NXN)6K>i{uSkCuj(_HCXTV$Aiauyc1EVH^0qg~UzZ}$25|BN85rAN+h0XW%BkOmM50Y{?nDSRvA@1p$G>*^l`P3`g-r^28ZzB&%u=V^Y(|!jH65>dL~n^LZtR!6@1_2Lw93C}?_|BbM^Hf&$BJa4bs!Ywsx5wzxbafbuq_BlQkJHfL~bbJOl4t^wl&7klEUB8B&WZ22f&_0{g%px<sBO7hMc`G8#YoB`4y>XlSV2Ut_{#Q?v%@2WudB5Mx?XR*3Ic`6HaHt3X_8GpvgeuRY$TQpg#K2&vRMP4JmhdH}uJ(|J)UR=bdS@)KP%n=c)y57bdjMoev&=NPTCP=2^M}kKVleO=bC}{(m^0->*id;utjL$N=ex44GN_(wL=f+7e9GLeR3&$}1Nf#0KLo&m8tu#;`<#6q(c`vzbp<NwUUCG!0Ue{MwTQuuhAOdnHbaeS)*s^4mKUEd&w5&zVKFd!=6|)#Kef@t3usdwg3{p;f$XYHvt4)H#5Pud*P5Z3+Zfd$Q~-0tR)#pceXhkwAbB1#VGF{};BATBd^gAr@#Fao~m?&%Trd_YFb7<_4$<{Bd9K$36IiUrk(!f$7$z#XWCaCD&`N>ogDrMCv0_1P7DJo^KQSMygti_X+k8lx#kXhyC8DgqpVAX3<2=%H{7aKXdZuWKy~h(AlpJ4VG`7v71eo<6Mf3EF-b-k~28dCm~L@L{?yD(L?BzF>nQSfKH0Nl=hp6H<rtT7~y2wNmSj>wSslANAnO&jx4~kM*|ULj<84VSM~Dt&sCTd1GKan-_;_w30-1dDY0HGX<j|Yt;1*~CC{CGalVOjpbsTpR;~10i6@Jb7)5P4sEyvI_QNj%zYT<bVNgj!lk!QWoa&gZ)FZPA10g@q9Awcf5-E-kW=n2eKxtproQ)cEhBCf-z#O$vw~rs(btv8Bh@f7Icn=zj2NUk+$mX!T*Gc@qx>c#s7BEzuntl&J05q~^L8i{r`UnTU4+_SC*FGodQu1&o<;^Hy1?Z&+c2?={SfW7=O4I)(I)1U?<DupZ<L+tiN9s-Kv@At5U#27u7pI^yU<4}$Ly!#k%uw2UU07RXY30Dd1oPy<{`AT_yqX;iqLE^Uvks`;WN5fp07TQl9-CrrGu=vvxGV7PCv9J~9;?=DwX%LKUNEz@AhmhVj5*GT1|X?^M~Z~Qn}JrCZ<%-!yz<f+))3UnC*sdm=?l7;C&I4TzYASJ5qKYHDshLB9A-kEa`E8fY7$hCD0P5EE3Z!IEOD_Pn>eQ#tIoFL0yjkuW^08gpRu<gam04p{^+Y*hWwo4vng!M)~+I6^ibA&y2C*bIm0}Xs-j@;C^(1aXt4CDt_sHbQC&F!bB5yNSo+kY9Yj#5UhS*jssxAe1sm-1I2C%yne?@DO#CjFIZP5`#fkZU{peN=5m(8kMm4xMCbY9{?Ad7syulG@=(m^u9P4H&U3Uf~YxXLFkv8>a>x766(?dLlhO?42TWz>(G4_&`pAjqSJHw_RpA1JBIO_7`07D9S71bH7jHIemW+-2414tNNVbA4!Sv$A3%JXKca!75d(`8Hl@adX<-o)N?jkITa)jpC{5m4d2(`8G)h}^94R_*s@N!vyFy*O~r!P#>H&E_T_J{Jeotd!PIrt?Z^87#~)YTs>RCuVt(6*pqRwRBTA%Myc2EPafyrZLuCZf~e`A#JD|C^(H#^;xt=&>lMnbc?U+<C8RmwuvUN=2*e<?jC_r`cW6Uc+)7ErG`5FG@E`SW^DD5mG<Y(t2U|gb28>HYx}#%ofgPtH}eK+{?jUc)lb9`q3Wu)p)VJq`J+9O!nDBpQ6uDIm^IE*M`q>1t(4Ul1LKjZ60H+j28ClM$2H4I(jMgNJa*KD!gjiJd&eh6<$S%~gQapbBH9HEB4JDK>!xXw>?fW#=xOOa&in<OakMwo!$8%bKMoXpdzps{HV#S;hByfy^`pEMbTc{Jdg8b?KT=268&3|>a{$C^HI`%eMUc&nJdDFZfcd9CZ(r(sfhT>O=%%IW=TT|zKfci|J~sB$0X}OOd9^Ls5Y=~D`d}+(%SBOs@nu>sM-Hi*pW3PTh5~I5D~U02asKOv0C^AGvTF7OjzAqr>#p-nf<yE^2ZmVsM4W^=2T>Aqwu)LABln*}qe^wL^!V%LaXp`?A~FE}O)RxSw%#uno`&JA5nd^IDoa=a>IYF-;y$8e>02$WJmRPRny0;p@Crjgdg)TleW7BBkoHTuizxA9RUIZzG!}=a-dBvmIz2|j8C3uuI<Y?kulKu!pS<*}E7hoQu<QM&o$r<|?$g5Js+mW6zxHbBb*+i;SW~WOM!ES`sJ7Hcslyc&3MCloG7havtr-(lFbN*Ss^%~{WlLDfi%m+Z7iLv6k<~#tF(A1#7GVKIDlvl26$r#K#rKAA+2Jf3F?8d}HiHPSi4cp-85MK5AwbGNpt--GnXAwrtX<}2Ynp>jt2bLuapiM<K{5iG2HMIcg;kTU8R@+lYbbo+qf7K2hPZbPvoG-7yY0jSK5Pg>0`egN(jZ`};_=?KAc9H6^~?kP|58Pjg^;-%Erjh1?8#vtEa2tNs9ZrYbfCbh2^vFq6H%x&Hl`0M?ts;YJO;szxBN}8!$G1d?%j@&qBD}C7R*Yn$;^G5F^NDjt`Pzydj~c{z&ZqsBa#>pDnz9sIntNq&F?S2u@w3Ka`R1H>i+%ZH}w7;Q2SrW1dX9q(i+mQF-oX>KRv`xuRoz|MquFFNl7gwr1ZWTmP7%eU=e{`fJA6+1Ofy6yAL)8NyLm550-J|`g(wxZ37fO;NE)Vp-mH)Sa;Um_(9;}?jSw$GgRTb>Jj>pP7^<7E3IF-j2=WNVodL|4FwPJP=BNjwmL3F8d>t$<Reo@U(uTVl!)b(p~djIPC@XJ-a$i<Uh9R3s?~8%cmky}C7pm2Z(<#yaZT}^qRi*XdbUH=f731r_k2z7iq@YD>R_u0$-%^k=5o2b*q^eIL9vI!CcjA>$43!g{JkOs;#h&V-v1Y=19?3e`Y-SC=0JrFR%}XXtM)dqPQ*r&gJgl5-}J(mD^(oFDK|j2>FR2i<1}<C{au1g98xH>T;`VI>!k!s%H12E-&|{CG^`-9b=uSs*@>YlLYIZ24(2W7citB%9J8hjm#);gZwa<gp1}Kkkc-9^&0cS}!>Fxf4dZ7^>Q%DXzz(F3`Cx4hB&}B9ILllt4)~bR(BEHvLe9m%#@CnUZ~vuR!saD2D5e>p6OvY$(E%yGxqScON<07a_P0;hAO8FDt#<q2@|u2KOQOr)y8}%&4!LSRfPmR*6PRPXlW1<%?VZW_6j5R_CiqCJcNdnjvx?*}nlZ|i*R`BWo?#``sh*R6vRNhP-pZrsgDzh`oYyJLp}c^vZf;=~<ImTh-hKFZ=@f7gQU%@Z@`hBddH(U^r+;w%f?T88-gNc8(LJ$-^#8DDog9r!35E~6NBKylL-pmmbaM0I>V0E0Jhw#~YO`=r<9+;ab1R{@xEVe*cG{qF8~$1nN5c{HPHy*!WcBq25|+<4mK=mO4i6LjwFc_r+xMc6o7?lNx98Vyona-dtCGuACU6yLTV=XdBS~unI<Dfn48f?DV!f+)W>yA;BRWK=yFnH88k4}kCo6Y<)iUUV5KY3I^gE-DEDPI+I@`G8JA1Wyg(7}g^~9;#D*KHgx%&^Nf-Lbak>tX`u#Y$m5l)-tJcm^zjE3FOldysyEUdS<Iziz@If=PE^rtK<PB6+cE~!wWS<8qF3*d4Bz;UbeQk`z$t}4f3-mP@puP(6^H4#?*q}FR#&*H16?mdyOw?9db&<KGIS}#;tmeY!>#~fW#K|N_P{8v5vuWTfai+lsx;%_`eCwjqn-kVRSCnw$Rv3GXXebqgib$XL&*K<$LI<Jlo;p!?>=xRn2|8bwSs4>HnqYjCL&PZlQ1|T$_z8;BtjWn}y4hg;GLa4|k!gqE6>iuuuzn3yq?c)#%slh*$Km}@R?3Z5^jygNbmghB9%haL`D`lhaWlOAo(Jm}%hoe1o^1Yq_%wWED3bM_~u5zI{Ls`sn;>}@Qp;Yn(o}FV$t0V*FCkRfBP1yt2;B@$S*~Rw^pK=^YJ{2{{4@Obd{(=D5o6o3zx3oOBX;`F}jmnREh<><BIwSUT9_Vbcl&wkYyn6fGMqke&EU9|@=nzE@p8C3d_G|1VNM<3poNlM1hG3((nM+mu)bNwT_dLB*&W2HucC<f-N^Tib|GQ@E=lgv!i^<NDP9+UI&za;mPKty^@95`?f9kDyG+n28P#$MqiwcvCIaTf3YTr@Is^U8>Oc#*@uD>!OD~^csBOCD&tj^Q>AhMGv6S?NC121t59=lyuGm(~pgrB?d{hAC(z5U-LbN;1sIkz#)N_b_2h)nz`8`zr4wEo>A+skMlB76G8v`#vl#ck;CIJXK3**z2-o^-538#lA)xUU5Fksn#~dUQtRa;sR~?BEczF;17+641{{dDX4z{POId+$AXu2XYMN=$}<mzJ7rBJOu;x{9^0yH1aaCkuk#C4>!N-MH$V|!H+?S-=+~Yb&-g}Fq#8;*#`|3H{iM8Ryu#-p=5rXa$hMWlWG}_IUm~LZ+R{gH+Se)0S+g%kgiW#2{s{#YT?KwOrl3CQlL%lgu^NKAsJ%oPU<~i%a;b^%9%xCcPwts*5avT$)Zil_oUEJjl4;|@sw{A!<AS$D9x^vFMpx_s*Ue1!YD-|T^hP^x+EQ^nw7ii4-MbS558bp`*R=EDkYPEw*Sf@jw-Hka_!(|Uxl4>oc+B>zE*kMR!Q3Wi-(K(`P?o*aFA36)6G#SB1%E>y%njym^iK+WS~oDFCNS4X%ImUMSX+ALYh*?w1&-GvohgJRnC*XM!Uf*avYUr*w8D06y1wA5A(6q86>)WVk(vN!k;*|&Hn-mK(}`2WDI_^7`6O&I(Q)Y^CEfV5w&AevvP>~wwOwJ$O_CLw4MKq9v`7<>SKBGC}&HR-gn5?amr`;TYn95hOeUpd><s-KHI)T1-{pEQG=$jnW^JXUO3BOYJjIolA@}M!Jn#2Q1Q|<2tipYc{epEIX+n&IThHNWM^}LiIFcJQ#%9DkDibktGw>qlC{WVO6#B%bK6a!<e!y!?PUi-KfvIn`3cT&95rsCQ0`?*$9anO>o^qu6;`v&1HUYZhL`=N5VUZf#DGH}dr4Y`4*bZ4RvE9_k6N@cC3(le_Ojt#L$sueFa}*z*UHQ}CVE`yp3OHn*5*J0S^3J3rhIHn_&norIb-Goq2{{tjgPBxH1e{EzYa%4YB}l+c$EE4K6v&NYN~C%w_x8nbsxqa7v3KCMb&jdqll4%iv23lmm<FZlY7atHw+l|F<(y0{}FY{HkkA6t}yNHM&%#2GM=^BM>*iKMgBY7Nv4>dgt=HWi#@(i1#$IGA}*?qKPvj+6JU0yrF**JK*uWF?5xbO@|5jOMjTND!j!&!AIK3JKZ3~B!J1;KiZ@w^XXHHRYL-B2>B7jBahAFJ4P^T8v?d9OMoKMJ;9dqlNW<m?9I+#yb~cO(SPHNmyd<PDQiS<b#K|lDmojvWF7m}B?04sz{COaA5UYHr|5g0i<D)a&*a%f;NX(*Uerwovn^#!JJ6{#za)tT8;Z9yiILYIqTo^~c&6mA)wPIyJ^I#pT2HUMPpx=8NtdW?occIWq4b@gdTdJqF>e+mOOD+lE=0!a9vlpXc^kX!kN|mgiM?U<e9U%9)l$_1>xt7)b%5`p)6ed5@tQ>)nhz|ml9j`b=0iseD%YND!*@b1K87P$_fS5TeItOG#9u<K^1Ado~1b$sP5|yWkMAa&;n)<C`_@+IqerVC42^lmGs~w95cOc@{e7?()WvHfUJJ%54-;B5*BC3wJ$p2r*JfM?DT}kotS65IYX<0YXc=q~%*uaA-Zi?VjG^`-0Qm*bm$e(s~uYI3X^M{p8w^VqFx|JIs8v0d7nmjnDyNYJKc{k9lWT9LQVClGy?%g%*NLT`!uhB&$pi{r5jy_>w5|3=*sV8nEDe^XCyh%oZx?AhPR<B(SA!~?OKCWlQgO~1a+BwMwS`ylfU7XEg`{sa4O%fRaGi~vpe66A{NxIfH)k36Dk%r94PShPA*Wy%nP7579@Zaj?8Mkv><z32ObDny9F3z0FXT><AMt-+oo)D>Vnr*r8{hb?9)b(vt*P2CR{B7p&F2BD(DH=E{&HE8L5z0jp4ZID6$|QB1PQQ7jOMW#Rz2(VK536c?tmG!H_Vv)bUyf-i*ChV>u@4}f(7NCK*f~)gA>h~>O`5*PFmt55P_(E>=~_8cAj7FB<o<7#E)l>L6?|G}q<Q_3-?xH4HuYrPJXDoy{m7Te>DO?agc%D2>5bY&JR<(YDN>h9*QMlv>Z9B!YRIIg%&oyw))k|rAeen7&VGJZj-Dl=xrEvN&0b#4Vh3jajsD$kvCBU1;JwLQ+{ZA}2T!}q%Nq*!xy<RSTA=E#Hxz+X9J265B8@2QpE)K&-hM;Ql~V3`?@a67%{9Ysg-$D5x!zX~mR^e@<LE+uuyhYet7J+QO?Ef_o7?m2Tl}TUW&lneVWt9LV*k+#ST1k`3<3h%9Dr8_opCfpuCnyY$cR=RZIOpaa7e`X;?p0WKVIHmJ{cm>`XA{9*J1', 'offset': (-0.85, -0.15, 0.0625), 'rotation_quarter_turns': 0, 'seat': 'WholeChamferedPreparationFloor'}, {'label': 'TestPump', 'sha256': '13936290c50a1aaea946e5cba882db4b4a7a7835593441b3eb1bcf6a4556e4ac', 'encoded': 'c-p;veRJB#viJXd3f<khB`Fpd@Jk$swyxti+0<r}l<nPf&gD{+00D}HBufIDr1IUL{&mktLSQGUd!C!B*wScTdV0EhdirJj%P+rtOoMq4d7*K?h(q6)1rPqzh!a0*rhew9>o`b_FplQU&|mwhk^5QROjgUJ8AMqUq*U2|$o({k)4q}AULH&gFU^fO3OB7^e)**lER&etmtMYbK4)>{EWB(H24g4NWKJF|eP<Gfp+CukILe%Wy2|4?%o?*aUK$CtqPm9a<P*I%u5Zq-Zd|l%;fH1SKmK*&;*&KR&4SP$jqDb|9*1lC*h;+AkMhR(_4VbAYX;GDmE~#Rg-xDmb9<&uFPb*X**44BwmWA3@5`&}cOO5vW~bF|waxy`yPNlyuK9*h_K`X=t_qY<N5*^V$av3ayP=MZPt=jwczt<&arN%g4fpgh@{P#94>yLl$`>)vSzU*v7p-V%_8=WdDlp$N(9a}ZCZV6x!@^t6{8X)@krHyfXub-))F{`Kmcj6hxgV_pYCHA)#PF9%zA+}=I><K;br<D9w2D`mkp@ei&@6}o^dH6<bv_H@IHiR)@`Z2A(|8q4TgJ_OY|K_+XiU;L%ZzavOy_<^ou=uA>I#(JBsX|E<9NC$X2C;vwB`g|JR?vE-XvJZxj|1^%Q#o4!TK0MGzkgtDb0gg32oj7`GSB6Cbx!9h4VB>jHU1A8AB)-l@8G+TY#jJa23s|t(PP;iWg0M!yCtI`dQ+0l@O0Ca$~ZgA*X&?f-(-h=+@w=8*^_p_Z=fA1Y|x@otNwHYmZ3LxQ*g*<`@ap)?lQ5?$IRDi~$ntlt}mURT>2}*9D=wnJv78;3u*UrZUq4K1_BJuaXdz$3EjHk9pFWxAYaPpcq;oDnx%qfI&;#gI^sZij74uof6T^!WE4Zu9oyX2|Z#oTHJG5*SQ}r{hStan{2r)k!vuE!vYs`T0;VTzKUdpoRa<=fr3U}2Vv;VeI^LS=oss-C=70Wo&<W#?}Mnx-4>%bSnEs?vdod`Jq+#$_9jrt*wv_GVgsU=K5<ACOo+1>tivS8a-w6RQQ{MyrkwYURXM&)!=Pz6Mv(J>kxwf?WTRMt$UA3BH^$V79}+T%*GRC^sMMP=4Kji(!}?@Nyvl0~yNsvQ=8K;a=}i2{Ct??&G7DHP5}@lKgCxK*^?+)bB*@9nvQ_E>wcgYl6B06-7`-nEX!?NJIE-8x-C<Dz8l3o3ZY8wo@i4L`hXpAytLDKt2w5P^;&ehS79t6#Q%I*7HRX={h_(@*h>04~<TG#PLzsYcTE<l{pW_2zoi>61xTa2mh=@;yrYT{MnEEZV@z(wNt^fYrhd-{}!LWbv@x#se#SK5dJ^#eNUwyo~<cBwxB-H8myARjzUSE!GF0Z*_<J0;3%bS}^cVL-+u85pog)9FbppZg9pGQ-O<5xrzren1_r%tPTLjTX4j_tJ0+Vt4A9m~8}c<CheLT>##q31106>9u9@b(8-8qM1$)V6*496vhJ!?Dxqa1XCZ8uBJ^z3^uFD<%`_;6h>fI`{n$eH<S-tz+up_=Gz+c|nid!9Too`3i#MEyy2$LwH<9Qy%)120A%&&>YR4(?mKa_OLPaXNEVOTAnkudm>AWoQCwRhl35)(s*z-v;@YNAmK_jH_2AxeNCEAG+C}fdduofo@LSm4Lqqijq|O}v(=L7J<&C9BGo3AH|PwXjR)Of)1x2s)EPSJsg1I>e09`Q2W1`kDqRw1E-kMB0eVR*yGwIRfb-PIE86L*)p(AbL)BX9_)Dr2k%V>D&di~noRo;f?lp|HI}j}J)?m?2>E+gg?YyuHlqCF^;Bh_d&vb)3F1|zYY)Bo&5Wy}G1^Cv3JDSMQ5xn3npf~<~&>0SG`|#8#+w)_9N0w_=#|iz2Mrd|u0!A=Xy}xYtis4fbDoHe|RRyH4;AqP4hT&sZcPpA(i|85bZ1HN<V4xzsws+3mpwk;3+zomig17Hw#E`ThhoKd@ZinRpcRsMjv=~E_p$qQTiO>yyZjmCg%q*MAJOHHn5%_-V_{|sGRr{q&>+%xwRx-gBHG{_Er4KSuYG`%J^)M={<fs+qjtOmV2Y4U4QxeS<A&V4V!UPe3hu=&FKJ-gh(}T-I!2|>0n2nZxwy;QdN-~g2<N`Q;1&#LCyx9Ei4CsA#X=E`Yo8~TGtfB`j?X&10sINR#CSpS2ZCSY0iXho-)cfpOL|FEJM*Ud}8WPd6b&CNU{QT@#w+B36`4oV(6w?q=8tNaj3rW(DNFa&B4aS?KZs;w?QxEjvOnO$q!uB(3qFL8&S_K<(xvoPLJk8vYwr;DO5BE)EMSCpv0T4ORSxN(p@eF;{=n@Sb{9x+j2PRNr4jQJVkZ;kb_lp2ZC=Es*?B9+w<~~bjq);z?D1ZDJA8DA0OD}`ZO%hgkus#E+x{D#|1Q2!%#lRa1AY=7=GPGa1MA4mYPpOB#YT-p23zV!|u2hS)`h7dJe{-AMltElMYXWf~yhQvpp`R0QnO%?u0fe4!c|)eUyfj05Yh)-eni}{!Ask3b;>7xF_s67(+)_P1%=}*J1*AHiGk21lxJ=VHwagE3)XV~CKcsX`7EnlVax)3NmCl8_fg-!FNQ%A+Ej{GvYU+<R!kvk;X*-+FmJI&!rFRlp^kT&mMOK>Q5)id8Y61=&ShQO?Ul?oHwFW%;P`0rzEH_xBE1qK<F>PoLuzRx>RBxK(K%tOU;vjOy^xr#(Y>@Ylv18x_)aEn(1IkDCB;mku{2<@L*jWVi9jh`a%wZ75*hm)v{TvoErNRyucBJq@6}GvM_NL)B3<Im}bRE`BtYhcIdG4IjQ`_m#^D#Yjol`11;<96U?$T3->OXf#iK)QP;xnE~x4>9hd~_nW)5RR_UEZ~!!eH+J(ac=xmqxR}E#u6(r^(naTQ8V68H~2wUr9UJRPP;XMQzt>R~M`ZuPi9t!2l{%;@~G#f|Zj#<85RTXR@E<-s)L!Nb=Uf_w`y=Al<)KK{nW}1s>`x2y6#T(i*xun@0c9HI`LQLP#IQ7qZgcLy-O7F^837g&5^DuIri)CZik6mdmtrAsd3NI^fT6&BVbPJC>)oX7ZC<^O<>uc;_ju0Xk)m_d@xe#`oDS<<-_{K)iIYk1{^f!aJLTeKf(Jg!?}4&;)a)lX5u$Fno#zSZ`LAijm^?hqm+3kv>Y`Ke*jvN9;E48;=$UGfC)lOL`uIl>~>~1O4=&pQdhlxIHJ7W1XcJW-22snFSK%Agv&Rdq1e~!3UaiQ3LqcQ=`r&AM8@{@Wh6spZ+AHY$553)R{P6+Rm3w9Yy=s7kbDeOH6Zu_VUOof7r9iYDO$|8HVALE3Cj5E8hs_Jr>;)eOeh<&4+`D)7%hyJT&zK{W_TN!=^b=U+{tJ%7gmSRCR|9wUEO`L4>S7(7}`r$emLXtu{`sUA*y`nGemaqZem5g`SlK&rxthKiWq}_OQqOYG#xjP>`Yo!Oq-T?d}=ad;dBYRwdU|=kzd)?=Q3&v^eyeg4EIo1<bY`X{3#%+CW;dCRVI+_oQ!$xlWr-$DkrHhB{(GHEm^>C^{1a2F}B_hB#=py3c{OW721d%*0x%CUFxd7ubNrVqhL*d1?iuUC|yc^{|A5&l9KF>bzis#R-=6fXh_TF%@<71gj=lBZkFvd&;H~pS;mir_Z|%ehhnTj45QN8ok7#Xb!C|><%PNVQW%zxDaEnwzOO-Yop1tKs_S1*3nU$rqDix`Q->xXli>3{WwBNu|!qlG28Rl?8tT`7|FzFNwO#>RkFVgHIKFrvu%?mAPXT&!IJ<UvS8|qRe~yX0ORp<R!{h0NDD?=lbY!jJ&Ik%OJ%Llnz*=7RH*_Fbaaeqv2BP(J=uAAAt>lRr<dcdyc~6_FUP9dkodLL?sQ4W@~;9-+op3uNSymq-e5J}cF+Up7)1;su{SN~QMW4#ik>u8lElh*=VzN1Puc84Gviv0YE5vR5%nCMDUcyA$`XS1tR&04=u+9}7wm;$lRkH9I-S!WTant5Gel3W&(?I$PM%o$=VxjldKmJ#T{`{*dwz+FD`nEJ(g5qN8V$T;?QPWX`n3z>bWceER>;}sE+Bk#>+2UeGTS}#@my7=M(B@SlG#G;r)Q-9GOE>d;In$Cd@EpEo|!DLnD8O13B-1}e%t;SW#}iiBm~5_Y~p9jvDkw5!7fco_`5HT1=i;b|EjLm!?9BVmqEOYrm)Nkq^RIXebLfs?;(vGT6<B_KDB}CBb)&=A#S^l;+gOZgU2*jgPVsD;0Ifyk>s)&bgg12X#WyN(kJmbU8s+xRIF$u`jMsK8E>@0MaK~Cw2PM9uH91%tZr9$c6K<u=(%8b?jP(fqEETR6wKFfld(4f<e)&`0#((oLVDbRMfwbol3Xe%MO<#m5vLq))XgpXGlh;y@>#|(80^Y%HCi!^$_$RXr<lPbE!0X?s-M2#2}l0qR?U`8?ANOVUZ@XLyfsnOW6|7U0f)VnWH%&pn`e4lpQ-q(GU?7h^PTB%pT$ZPJ!3V5d$|w2$w134T>%%QDl39#e_PQ(=lB#rsa-|-Jkmw%q9_2Z_%53hc)2v)@EU0EQq`GcI;4u#If2LLxzwleLYNrlQ8kN?iFdd1%W1r!PcjWus?6f#s6Go;A=NBS+NG2fKWoe#E39*0n8P$6&45&{G5oA>%lY1vG{}9^;5IUsK?Rvz8B^~KkEwA@XvD0?Wx2mpljUi$v*?-%3oWifRj3TDobc7PnG0D=JG>>-2&(E&=60B%yiS62vI_DY0^@3mz+@1NA&bI3=^a4f)!GLrDpvtz1%=p~c7u~rh}K=+vK9Dwt{j7;a;D+})ce7XT;*mAcLn4#S%55_-1=G>d6SZ24yWA5RUZ0zDM&#~Qd4VBAV;WoXF^U#C#*KNPgD`j;iyEmxTd+!ZGH#?niZ+~_q%A8(MlCcjd>~q0Q6tk>01r&$nO0lm(j{$vL&f&i*Qp303cAHNw71zP`g_V982g-NCz~f6+*I|l#@J`NrDZ#$ExTIMO~Z?I-ODhX(|!M8YZbY^%9v4lV<x&PIRZ-5hL(e>aZH$VK3@)nsH-7!h)dH$H!pX^PquO&WEJ!>XO0Id$58gOmoA2(kaUWdhJ$T4?0wERB1;i?ckv6)Vo&(rOJW(lnwK_`}y#+ufW_kI=4=qSyuO1(t!>Az-lIKdN@eBczu>1;1f!kCsO6$_!)m|CPz{ObyTAxsnR@>DhFkiXSrQ-$&i*}H);SC(`$Byq^ng=<bjiHOCr@2vqQ)ay_LF?`lhfXzCc|cNOFn_CHnW;P*u-+EvZ|kR8_HVP}Rk&m6}dr2&frXSG=k2wXvL)2G+7p&C+tFZLF1rf5M0WHY|><`n-Roc@R>jlrL;XKm)cQbjsuDk3{c?Btc|N8NR_<a_B#(U<)N1>q3S{RFXz`{)~AZhL-1|%W&{Up}f6Wh2doxYfza$G<B<l)t?5bcycQQQ~B<cFI}dJ7=+0~v7$}=@p=^9@EJkr-1|PBoUr=ct>{c+($n(oV5TkMOCUtj9)X6@)Jvy=HWJ6q&L*OvW1I~hgRy-kihAM59V9F(aG){XwrCq$`I%L^hUWuQS2c&j{`K$g-rTq%GMW}RD;WgC(vhsH+6UmN{h#c^Zeg<?5F0_<v>nkjYEbmHMt2pvFbt1D*idmaY+~ErAjz|#w!Jy@f--I;F(gX!8;!jzn2dDvSK;|~5KI}(Lqgq$IARmBa>di0U(~W)7q4$g<?zCAt+AZMK_mm}in|z>I>RDRfCP}>xmzL=ecJZRuHSrK3=h93SFU58D<ABvmFmMircP=LQaH5P=b!rPz`q}56VhZ{lhL9!bx0G?E&{GpsN@*xwb%=bXs^=5s3R!DO&<hagn4cSQzdB}&rAoMkGOMowG^0jB<OYoQ{JfPdW6H&h)+BtbUQ+~BaGzUq$}TUy!m+X*R=?C+Sl#=$E%y)Ke`>#8T$WtcXc_s`TgC+A0IBSuU%r2_HpCl{Ljm)^K193nJ-9}j=Uf=d)ATDJavv+q!E~RUULR@j7mulIC46zj+8=k;i~PjERPee*M{d01!IrSMkuK?yeB@LrQXut9%!C=8yV{8ZqFC=#2*L-{UHm&MZ6*%6rS+2eQ?%l)L{PBm+6nLFV5dz5)!_VGWY8J<%idoSH`E`&#y0GlvhE@<7DHEv04(sj16g(2VtgznExi>6Q{M0t?_z6o3F1cz54t28+vU}XD#fI@%S?}Yh^y-ZAMJnBCXBq%lDTTH?&pMs!n|no3+aP(L9XDUZ{LLELfJHcy{BV)zr(qmX2E?<zct1MMuAQ?ORJyz!9M6q6)SI63{I!>GRJPHjk0g_On*Dk(1D$mp51MF3kOP5Uog*8qM>C+mY^RIF7RwHgL_0e_asTb^FO?LgJ>CdElqarS+<P@cpUVdEVG61RlJpm*k|ukGLs~E-2~mRGj)z9ArfWM%g+9&ZH^}fY95}iL$p2pK7UQOkbjSO2AeJRFlL<$c8uz@;XeaO1{9MmDCmL!!_T$`{(6rb8ijzcpHJi(wqAwt~olMCPVA$nx8(rt#wkXJ&D6ORbyVgeRW=|O`R=AY`c{Zdo|<Be|{o*ynIcPLYB|$>GdNvlQlDYv}lg0*Td{_Q^yoUDkPT0CA!N`1O7IoHVSnFDx<jUti)+iRz)PiC73LV&ED}hajnJCESOu^%#`FWC$on@EA!e%q1B0gpC)&)@Hlxsf|~W-%Dkzq_Y(15G}cJBhR~--xQ^#XX}N;=eRX6p<||V4Xe}nLUKXtjOk7t}n={c7LX!qjcX2`z$1VujN#oUgLEC8VF(<2VKw9FZyGP(f{yjTi?f$Yg4Q4Z$BK70)Pbw{$8arw~ahEN;jv&VQDQnG1=P^IgE<Oo}5T?ef>(_5cQYWn-O6W*GFkivqc7YDfAxZ3+w+izSt3Ya)vg#GUkLa|pQ<EoFsre_S7zUG_iahs9#q%&(cssQ^tx6Sk_bh`fgVy~IA9m)Q2JLEtOI`Vz@Bo><uR2ypE9$hRR5uek5W!~~K^KI$LIw~xi8ur<B5Zl>1{_-DqRECQONN9RWn}cD!tYyn36O@vSvU?Wt6K6GVXQ@8uu5AP21lJZADAGyd=yMc@8(n@Rm`fys5nv3SF`yqQ+-sLnS}1M@<rd7Smb-msaGSK#A=C__saN`249f75NhpF4(8MTJ{58t=Q$}75`dBERF6WDMAC-_N0@8GCppp{Xhh^=wWd@rvlN%n=`zhnxBezmdLqeo=BEC519pJwQ}C5Ko~TG%aFSnPCDMTWEk5#F(0NA52H&l%bBZ$<I#j?hwC0fOu97J%8g@V4ztRlB^1EvoQwJ&s%mo@6#+djWz;Q36HZ27#HU*$R`3Oyl7S#(UBS1Am;5W$yYrIsEzM?%*V~<a9=qHb>y->G4;1}Z)Yh0lF9?h*3GbIzqnZucF8+52LB01-Alp*>_Hyptx`{2$+!Z3hEpQbY)RO(kc13trfq1us6=bnZU4@9CzgqjgTONbz-p*;0@-8FcGL|J|n`y30j3~Qxh0uVw`446tCsPcBX<CLpg9v|EN5}e7xpWHIpL7HYr2tl3+O}wnHC^6<kBB1R(y|yva5EXh;4zWgntKSM}C(>C<=*~xX)Q*G9ZN$A(k1eJH2?4jVU>=cz$?Q>CX6asP!lG0{N*|~GoX5;tM2X(ZG9njoaE5BS-O4UbvH;j^^BIyrC}Z2vsoQpFV$2Iv4N>Y26<5%Dz^BE>MyO+4FZfq8;&Yek+AP|by~n%5DGI1jh#D=A%pL$Tqd3wy9x-0c9)L9oQes`u`KU4gm3|}8c;N>Ez|d9aq1GE(&QFTmEc!}ho(2!2`#24!|3!LFTxvNANG)VY#)zFJFN*B%EWyyBeY8SxA`y)`B@TkAwFRv`bO&lM$^4keNF2>*)qt*nNvuh;u<bIAv4nT{J$PAP(yt>r4UZN<o>@f&Cvm2b(<t4Ivn;B?Htu&^?Qrk=U4BNScz>acxKqdPg06EHc`1I!SrBFnWg(_w`{ho=dJwJM&LMs4XBl^xpu-h+kY&`tGpf<QQv*<m-$6VnK2M!H`KpHNs&^T3rGnfQk8HiI4%RQ-&Ouo~PtRZGFT3p?uuxe2OCt}8CBiO<U<cr}b=V9A-2G~t^ZIj;V~H~f7yGoy7cr72Y1L1UsVsu4(K!F`+JH{$H)%~Etb%;gLRYV0=bRu@G+U5lm^Q&441wXnC>$vZl9z5IdW(8PYUG3{!b6-K>5rMgG4`!S35@#~iNc}cK1P``#eTf>=N@Tk?Wf3tOI=A8OKcTup&lmm&<{O#Pij>^9M_7+$o1-nlUnfvNd+_xonG9~dlrtLg_8rFKBk`$HvcU24y1uc&tq!B@E^Ec@d*%@L|p}d5Ekbvkd%y&%i)4txy7NSya-7^0Pz|He#s?;iYGBa9r!=#$4U1Ed|%zuBZuBjJN$Osd4W(i1id3tNZ9RZwq&DwF-8RdO`s6FFri99S?-)wgco|V?f>jbQWuB0H#^LLCrt9iWZXfA!0ZflRvQEwx4GY28TPq$QCaqLV{bx-WtKFli5{+YZ_^ZNM+U4nCkm7Zf_p~~qZrF>2(yhy|DQ5Pj50r*L6O})%O#F>hSE^gw9nG;Tw&Wx6c!>#o}1*f?0i){0)3AHQSOYQUYb4G8C45*?2JeT@CmI4#M0qBF3U!05UD9OXq#(%X7je5BAeg~qc~gPVS|Y8OG4z&rC}WOmAGP4v=j%^*<VuGU0AtgrrwZ_Q_*x3(I=XZmDq!$p(EeM`@R*Y>@9?O1unOW$3<~5_HVEocO1)n7ty&dm>N7&(<!Ft6jj0Km}7}!-Wo?-ZL}nvBVec;ljajFSIZGcd<HQcW^^B@R=hxe5X6>UdS=ga%rU7RSTxlfL9n5h$VjwqfZ`iG^*6{Ye--kH$;kXU$kq@YN#}gi@g@wj!qTro;Q2TpmnR@l73yB*P=~4(aHbNUk#(<#!xs;M|By(06vCB~l;JlniY$M=onahLiEF4sG~m--Gh3w?m8d(Sx%#;ZuVBA{>?5FimBeq1H<C6V;w*p9CwgX_yv2K7dHSp<uuSS-oK=Dikj`V3vp|t)_q1vPGF`9T!H+0EdsUzQBz3Lz8mTJuvpuw1DhGCrTwo~@Z2%4*$iSrarTImqq<GxcBobRB=T3!C)7F<~tK_$Kuaa^0wK$W4o(4>JYrE7b*XyBUVogWOF40@s61(+b_gkqyAVuw0<BhDh{{Sk8lSGkByb6V)JhjEoQ!iOaN~;4QNy-v6VCR4$&P)~tDKH}pE$Pq=L-M1y@~QVEJvUTlA@9&g-QrAW*|3q`#ji-~8Q0Q!kb-UCWGCgGI-w@colXs+t(#MW#+(|26($AWMUy_a165#jP#=Bi>AXOWuXTLg4Q_Iv|J)UR>&}d6<|@GNv}!@yg$=E9=Y!85vcR2YI^(hL)0?l~RK{c${D<oYJ;0~e98S@U9mCQQ9b~52p*78#v?bWAg`j1vm0vD6hz*B3orM{w>`TcyDzZ|Cwy`G+MkTDm3rvF)CBJngnWoKwb0Z~AihY7Jf%MG?iWb5cNlMJ3#+}ly)56HKgjq%9&_f%#!?zU`I>p<1>kX+}CI^Y}wE#r0b%B7>o-8|yfc~~%Pz(LENFYE50=Foo|BJJcTBd^gAr@#FN$5pB&%TrdcQrx4#|=;u_~WkNk2~-OzuLH90Mp%;7I(aHm0WLlo?Al{5NQrc5$uo0d%lh78>wmy-Y3{XP_p?T8T7it5^CCd>qTQVE04c>{LJ|?<8f&|Kxe<XG??Bz6EB}EMp}vu9V>P4q8Xg&lMp9cA}g@d_&!n;1wJXL19VdCrL^CS{ZTxd!B7f>)7dU@CFI~|TH$oDNAnO&4jsU<M*|UL4zWk=SM_xJrz(t#0UE{@-{}>X002iFuasCXmQ+{QxOEw=q~v+i&+b<-4)mbJ%c_-@E3ss8n3AY12V0}}sQuuxz~2HwKQpMLp-K6;QciX3M&{G82?HSw$?oUzG!`k24|YQ`*iqV(HRnSOIzt(!aofWt>h|!1yN;wAjR@+c2=kz^crf99+*tBgq+*_Ng%#U@O{Y?$DPX8NTlzf!0nmsD1ev;z>mzM&PQPFr*yuG$my(A&DQ}qoD?l$r#Hvaq#uD{4D0Tan==jBkkB2Q|7<W&5|2R(l(r8(VXuhaM3@&a#Wxxnl3<p6vz~`3I-nWIdQ<hfT3pSWXln$=NJG`154T4*p;MsuMO$QAxS9gH%Z9bUW)O1oJ?h3s7Njp%jN2)cST3NpqD;VO^lYKMB6+JM-hKN#2=^L+VaeT|glHivYc(8_`Rz4MbcJ8J0n`nkB3cKe2E_4A!;C-N}#2rdB%!E8;;=#w|IIJL1>Hv$5u1@GIaj_qpxDaimI@^p2+!Q_7jU@tmM*f<_5ue-k2VH3y@^gmIy0EbuyNY<xLs{?f4*Oy34s-xjMZw-taE|O@e-XF?9fS3~y5jG02V&${1k|J%#!#qU?5p3X#Dwu>1#I(pF7%?A^rd@3{4R;{<J4Mmu<?)kYSj=)m29@C26u2ot$dUCtt<!LU<kC#o6CQWOuLk>I|I^b_Cs9U#D%N9XnF|1FyJd$@u`if8Ht}RgPd5=+!<CPLE*wsNi?ikb0M#ya>~j`s!C;s@^xzfiM}h&bDA%=9Mw+gV0J2AX-Bz}9rNACEBbkz_!GWzkY4!`#E=U2xsx69BKGpyTeaWo1#K7Q_rk-h!P(<-=Hn)Nn+wl0E2Z16Xk95QvvF8P?Yp_@)GjXt;zlgE7GCD%d1`TqV~!BVG{U+|CVZs}X+zyW!KsaEPU96xnGqWYOoy*RV^11l*+df{0Yc)Zyaz>Klz!CZ82%(qr<tX^pLX4D#Eh*zveN#PziOSiKPO{;Sli!4?xa92o0->8^B-67t9Bv|1Xb5&4Fb7TDj4pO6t)A_k83d=gS_TX9om)4i!xSUER2V&lT}K~pm6MJT(g`c?LofI5?9@A+R7GQ_vF;7_}904aMTTvG3^2tk+5U-Oxtde>?fYL=xO0UOoKU$akMvVM}De7zaJU+`clUR)*Ph=19-xRy;!$`ZYIvHN8GjArH-!GzBtk~0AjToi5q?%<}*vjZMeuG`uNw)p~)8<(#NrBJF318Lwo!FmFckC*jEmG)-ZIn4V@vX@3i#cMtsXfk-k(g+b&1ywWqyyD!!pW+x=34N<8>~g9sq+fm>FsHHIOO7N~LOxnCs|#O!exh+~e$NN94@Bth3wVJahBGt041rMg&J{LRu`&mL7o2Ee|FrB=u`d*#B@FuXOwDkV>42`fOoFfL2H2b3%Vr(u*Xe(JC8?L|nJ4yi9qs@fJRClS(qNp}$?ex$17$P<sm;A!?0qp(ho5#gf>VM8bOXW-3Vr?8WkmUX2X6$W;*_qg%hF~xjZoVd1*M`my9)iJlVCc@*Eaz!)J$G1YYr9Mg>uBcEb!BCgsv@W$~OjN-nc#u;y$IYp;grlt3q@)tctH(rE2gPGRa%m*O0*F*%1f44oh-HfJHQ}<uSuF(3jmDcCB794PICPv*L56DrqznX_1#_CY3jM*_<zBv`IheG1)78XJ%j;exN`2|wA}gQ2BEL0f4TT*(riANZh&#`+djj8`*GzrjqXl6|K;EZ78U##LJl=T@L@<fCu6<zs4^>pj2f4@5LfFp0o*eeU0$%Rl(F%%X0tL>Nps|EE5q7%8#`HnO9kBYKV-Q-&hQA4RI4V>Hy0;RVow)K67qgNp2eoZ8ArVN2YlJ|_-hs^!unqv@kR%3#3Q?&@j_k0!g!=F+OObDf>#yo^>2HT$(fc<*9ekl9Xacp8){uUUP(tPV=^=T1{Rw4L0t0?0CAE~0GJ9%R5(R{Uc?@;|5}~;f2n_Ha0oWWQkuX+#oQx|sX#>=J6Qc0mOP5Vt-!Mr%V%=#|UG9r^L5?bXXEs7VvPl{wd`jz8Zo~!=iWoC{e1?LBcwjzI2OIkT#T+{F*=CoiYc6TceoDmh%Ftp2T&Ey-$?BjXNU!xHgwdL~?U*y`GZk+~${Ar&@tvZ~r^$M{L)E_;mxO!1@^ne-PX}tw^khF19Wmk=CwU6@D~Ax@104Fr-N<ks#e8}5k`M^D0&l(lKXL_hJsJ9k_jtRn!Uij6N@=V1Hn2|2hb9-<0oT8q#bK^gaa_0D0QpR}t#-L?O{X&7q)5Oag~HG>w-jH8ax1x9pZ)38l|hGwB}BGKn>yk+F;qq9vQRX^yoLPMeUZX3t;=xfO8I?Du!Zsj-fw*^8XGiwv)PQ|rjj*`pAD&3>3ofIAbr$>H92gwT7ly%wOH)4o6s`fUVcQ9#lJ>Zm*=nlWjey<B{L|d>7x^pR=L#%DZaXV`|g8r{@2a#AFtm1_vLHj=H2BL{koFOmcKiFLpBb%WIKd_*%)IS$9N|(yu8yr6aN%ZVmc!DNUQhejyh)*Ibk$olq;)iITxK+CDo~(t3S0^CFkBsSM))LuX5FOisO(j;GEzFW-<D7_3_QS_m^$~7a>*9-7IgL<eKO2-+%lECoIU7l+AU=>{*>tXF&gty3XnG(3a@;(0`DRR60;!zDXz7?>@Y(jfUr@XhTgFE^55@@2+no^p?&)M9w>HP`L?vEs3MS5PB!K`$)3->KzHoCmT!BK@-lyG(aG~V}AWs^l^Q2{^9lc)oXW9$>XXdZ<QHaMV?lfpH<7s8iJ0ixGqC5s-;-(DxR5@LE(rF5$di{#deJ`t~&R#{Z-4L4?;AuLMOhpjVuS-i1KaR^8KgAc7-B-S@p!}*eczPA-Vkzw}LFOE|KJdV>m#Zh6ty1eV&6V5{84$@KIPn5DwN`Or4<cqMXE>4*e<13J*qE#w8U>w6_u=qXIZh0C2ZTFV*Q5=Bjcm=G{uiz3LK6Q5|8`Pinme+i82-xq6Qz=<UzSBQ!!_gVqaGmgThK>JdlRR8UV^4F8RS;0qrTM@51GZSmJWq7(gaH0#bLlhe~q=fpod>%8ckP21h^q~m+f&)P3ej$rC4ROo676aSr&m8da;)8jUYg!WKoM+ZP?K0PxQ^BQSpBMk|?X(3c358*o-0L|XlZ{JFps`haRh0NlgN}vL@TkNN=T}GXqWz&gF)iSkcgG$-(TiFupU$l#g+R<<ioqXHQ`(-d+x&_&4va4JU%}^Gz9Q!kzu23rZ0#DAdVN|mJv<Jc6VpF!j)i@nCUN-SP!KWNYqNkz;`OYY++7AeTy$Ou!cf-)hOoJkyY*>EWL-d1P(iyUy^T6aIOWB&V&JVAj+UU2_21}|QJ-9^C{l~s;p8T5lDN<JmF1OQet0DMMTu+{=eyZ8YVSAq3Dr3X2$TQlXG-b7pkk2gtJ9gve`+YQRsim__CHq?^N%9+KK|-T<&GY#`&BiRAtTG*x$C=im!sH{)P5Zjs=W1D2Y^TN1MdW}NEUnl{V&eR`g?I^8=jpv4x6(Klx#q8M?}No-H_K`^(o&G{b33|Q(LvH|{x`{-f0<m)Z7jPIUKt}I^B%W4kd#tK>py(_jg01z(>%uQ&8O`)U)^lJp~IbtYn_{26dawloud}+f-$dfv5!Ti4!s_qA<Y}d=i0G@L(oR>F7rviJSXMVbgJ{y*+1GODGmGL26N3%Di_~8z`IVtz<GYYad{fLjPKuY&DZa)|1gU(nxTsy{Sv?RL)64WA`Zi7_vvLHG*n!J=Ym_A{Dp^-`EibYrIe0Ti+IEd&@O+|xlG*LrC$X&oYX?PK5Zq~ge0nkBbP9VF0Dv`HcqQ=!pnWccjfW@zI(t{f3ayBa%IdSu{#noXJh_Yc4W~egOQ95mGfGnq}A&3g_``ARXQ4!dRNMpKUaStB=F`@oFQ#4i@YRTkd9ML!(H|UR^VvI7mn7!EC97i$vC9#zv9GE#ao=b<+#~bVaJcNzZc2ZD&1|Bq^%!xE^7bWE<iAlR0cEcVJRX?LGrB;t3Td0syH&xrMnl8W%VqKA&26g#bF_Jsbf2XdahZS@TDs2q_5#_FpIdOvK$+F1(2e9vF2euj`BgG+efBSNiX~fzpegj769GZp_38#(P7l`-#p-f<WDu|$RldUN6m^8^>s0o(#Z<UAhezTdKkM<4fV0~Jc@6r()$kix^DR_f19jE&aicqfbWBZ+vl4@RKWGg(R>S<+GeKQpS*C6#nb>xl_W(~7lS`lm!M*$sS$!YspxLDpyc>uG2~QWtCL-e157NvcuegKKrenoYAki#nImhVV@kI{E9SPFLdicX^V-V}gnod*OY;+);ks(vLZRHtmah94?Qi2y>{nRLCJ%gA5)Ci=p%Aoip2UDdAp2=nh7NqsgjN}^+K*baG68wVz;;+OuOV8}Ll}c8s%vHD91}gNbkD~(7}jP$0-f@e9ZlKTnDBYVqjJW~2|~@=#y56XX*BY(iM<XkBDEab4S1COMm|{f6l$t%zBO>ZbGL06drWwH%okPD1&tzy98~O8iM|x^y`S7mp1e}PYMs!Ato|eFl+R%9*W2P~cRMWqNRaj9nSH1Mmo4(&VNSB;=t-DMM6=jq`&1BDFCpTh>iEN=ANByVIW61M4F@__;bvo{#>!)7Z#u*gMIcP+>$kqR(D)HVt{iKMsVdfFA)cZ8l&M()t)&Y~E8}uc;obu>eRy1xghV5ymMU;B{qLk<a{`W>BcOKH4iz{l;OyY15tWf5%w7>!SNbn?(6Ktm7n88xoo{kMpxsYYzSI9I{_Nqw9jsdjRcA=-qNctqY_ri7R>{s+g*dG+AGqAfGYKboc#zB5=(l~?ZB{E*2DA@WiE6OfNCW!4x4{aD340d`t<+FWHMFC8YO0>?XPs8(gaEGJytD0lu_}jtj3!j6lJ#}u!w>BM+U8PnHlNRpeCrSH>QhN^<Y$@{7Z{27FjU#`ic=IIDs{2!r<v2au#7YVrE&xiGiOETfQ-;l5lA%PcL_=0*QF~_d4@<-qhhMrzD5k+jQizxPc&#k2b%lk&WWbY_ub-l>vrdaWvF2oJJ%54-;}r@CaO+0$p2p@JfN$iuB7<st1GCHwA?<T@$Ah5IRp2rxG929(XfJ~O1ZiNK|k&4Ui&_&=J!jPZmIATbt^YO)by*iG`V+CcNtH4^RA&=$wIjrz%g<E+?y-fk+1|UzLXu2fbRCabo2=ellpWPp7>%$k|KXihd0S6P?u@lx72HgL&$0(mfiKNc<|EwYMhgNpe3Qr*n@8t+cyVX8j{Eem}!gWKLlLSmn2<lgTD=nzg!SXvJ-X3?ppo}#QbMT`0t?djGG!)x=Z<syc3`O;>@Y+D~6LA`Q3tfLZrcIw&lY2c5X;f_q9=7XBv<2w``+ZeSd*cG~g@M{Ro{1<syj&)&@dlnz?SfSHIFl-vvi+IyvfoS&fgC+{ER+9_km$F->Vr;>X=SfOJgje*1mnMBze!+Z#>lw#O)UrMytIs7UErnkkUsR1|Xm*9(sb-~$zWT;-&B{i*L;!5{8<w5|?S<yzmfWpes83@1^}0zrDCb}^5LKNpGA<<fL1d7$P{ABt)+>9ONh|FP2*qop92eMg-A{H_c=3q*4Xv;CW`yqv`j%={beyPaZ}ecHf#t*)Lm`;VK<%PR@@nat^{TA=E#HxPkTI9d22ky;e?&$!8uw_lTUrIdTxI@7rGv}X9V&}n5WH+$;AF}I?~IJ%G@9MebADjlVYCc7K|_09R!4d4A)3&7D4W-0(C2_F1V{popJg71g3CI{e^L1!FIp;eY%85z;g(H1&Hf<q!k7a#xp^#1bZ^3f29#{UB@Ht-4', 'offset': (1.31, 0.6, 0.942), 'rotation_quarter_turns': 0, 'seat': 'WholeRaisedPreparationTableTop'}]

floor='WholeChamferedPreparationFloor';plate(floor,[(-2.31,-1.35),(2.01,-1.35),(2.15,-1.21),(2.15,1.20),(2.01,1.34),(-2.31,1.34),(-2.45,1.20),(-2.45,-1.21)],0,.080,'z',0,'Whole broad empty preparation floor, not working-clearance promise');FEET=[floor]
table='WholeRaisedPreparationTableTop';box(table,(.600,.020,.840),(2.020,1.080,.950),2,'Whole broad complete preparation tabletop under entire pump reservoir and hose footprint')
for i,(x,y)in enumerate([(.710,.130),(1.910,.130),(.710,.970),(1.910,.970)]):
 leg='WholePreparationTableLeg'+str(i);box(leg,(x-.055,y-.055,.065),(x+.055,y+.055,.880),1,'Whole full-height preparation-table leg');LINKS.append((leg,floor,[(x,y,.072)]));LINKS.append((leg,table,[(x,y,.860)]))
for i,x in enumerate([.710,1.910]):
 rail='WholePreparationTableSideRail'+str(i);box(rail,(x-.038,.090,.385),(x+.038,1.010,.460),1,'Whole front-to-rear low table side rail with end caps embedded inside full legs')
 for j in[i,i+2]:LINKS.append((rail,'WholePreparationTableLeg'+str(j),[(x,.130 if j<2 else .970,.422)]))
rear='WholeLowRearPreparationBoundary';box(rear,(-2.310,1.205,.065),(2.010,1.275,.235),1,'Whole low rear boundary outside both full original bounds');LINKS.append((rear,floor,[(0,1.240,.072)]))
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
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in[0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
INSIDE_TESTS=[(name,add(p,SHIFT),add(q,SHIFT))for name,p,q in INSIDE_TESTS]
for bore in BORES:bore['origin_m']=add(bore['origin_m'],SHIFT)
for gap in GAPS:gap['origin_m']=add(gap['origin_m'],SHIFT)
def measure_basic_geometry(vertices,triangles=None):
 assert set(vertices)==set(G)
 allv=[p for points in vertices.values()for p in points];assert abs(min(p[2]for p in allv))<2e-7
 assert all(abs(max(p[i]for p in allv)+min(p[i]for p in allv))<=4e-7 for i in[0,1])
 return dict(review_scope='basic whole-mesh count finite bounds and common-ground scene supports; no working-clearance or load proof',mesh_count=len(vertices),static_two_reused_models_one_preparation_scene=True)
FOCUS=(0,0,1.06);ORTHO=5.50;WIRE_THICKNESS=.0007
CAMERAS={'thumbnail':(6,-8,5.7),'qa-front':(0,-4,1.6),'qa-side':(4,0,1.6),'qa-top':(0,0,4),'qa-back':(0,4,1.6),'qa-wireframe':(6,-8,5.7),'gray-front3q':(6,-8,5.7),'gray-back3q':(-6,8,5.7),'silhouette-128-front':(0,-4,1.6),'silhouette-128-side':(4,0,1.6)};CAMERA_SCALES={}
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
root=bpy.data.objects.new('OneWholeRadialDrillAndTestPumpPreparationScene',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole horizontal bounds centre; common floor and complete raised table support two entire accepted originals';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
