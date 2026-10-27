"""Whole purposeful farm preparation scene; two existing models reused exactly, zero new stand-alone models."""
import math,json,hashlib,sys,time,collections,itertools,base64,zlib
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='agriculture-whole-cutaway-mower-and-three-shank-subsoiler-equipment-court-scene-01';VERSION='1.0.0';TITLE='Whole Cutaway Mower and Three Shank Subsoiler Equipment Court'
DESCRIPTION='One new whole empty farm-implement equipment court scene. The complete accepted cutaway-hood Y-flail mower stands unchanged on a shallow left staging pad, retaining its exposed whole rotor, two broad skids, rear roller and entire attachment-style frame. The complete accepted three-deep-shank winged-point subsoiler stands unchanged at lower floor level on the right, retaining all three deep shanks and broad points, both gauge wheels and whole raised open-eye attachment frame. A broad chamfered shared court floor, generous empty front approach and two low rear/left boundary curbs organize the separated implements; nothing joins them into a working attachment or process train. Both complete originals are embedded hash-pinned at unchanged scale, topology and PBR values; only rigid placement is applied, with the whole mower rotated half a turn to expose its original rear cutaway to the common view. Zero new standalone models, one new scene. Not the existing tractor/crimper bay, hay-rake/baler yard or thresher/winnower workbay: this contrasts a low exposed horizontal flail mechanism with three tall separated shanks in an empty equipment staging court. No tractor, crop, soil, trench, loose tools, person or operating task. No cutting, subsoiling, drive, hitch compatibility, continuous motion, ergonomic approach, safe clearance, support-pad capacity, engineering or safety validation. Rigging, animation, physics and runtime interaction not made.'
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];INSIDE_TESTS=[]
PALETTE=[('MatteChamferedEquipmentCourt',(.28,.29,.25,1),.97,0),('MutedLowBoundaryCurbs',(.21,.26,.22,1),.96,0),('WarmShallowMowerStagingPad',(.42,.37,.29,1),.95,0)]
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


COMPONENT_SOURCES=[{'label': 'CutawayMower', 'sha256': '4fa35def86e80c2e057f7e0af60d974aee2ff67b2fda53dcd9da6f4ff70b276e', 'encoded': 'c-p;vdvn^#vhV+V3Z1p<l%#l&0Y8#JwCXsCla;fxoRsag_g;rfQ38ZfED)9iHc92X-~M&aNJ3y|rOv)LRk5YfJbHS1dipv3<(FSRrO{2a2x9Agmc*eojUK{@m4-pu9Ix`=KG;})Hm7kA#a5c+Noqy&WgO1KMQ%-^Y#9fep0!98&14y-K^`q`tSqPBV=G8=D_O)F@0VYGX;7nt-seF+Q(v-Vp=Logi=&asHkrz!d8o!o9EamPN*0-l@-WSlB+eSsG?`mVYDIM|-N|QqZCqWSU0(ZW>EVat_CEb_?c<X(98RM+91dMC4YMR((?@R^qy%x}?CR?L+P8z7G#anse3gbxp0Al|bCx8NX0VtvH!|lY&$&5I?!&a%YTLbkoL^pj_;lghZLj6E?B4Z<>yPKY{f@ErMkDMu>cyg7tUs-HjJZq3-0$ecZoECedUN^V^EG$#X%SkB@IKyH!7866DfLoahdd3&0>EmK)4KpA;AHuR>Xpk8Ev&$rgoG)qM7X_%daXR``aZG72^vwA@hV+YuOWdto`vCU#!!#aB$!w?DUCU?vfF5qS>qs0H?*9g6(_XB1lA&3hiMjSqPUOpnU&v%gzZZ2Nq`!om|!O&%4WgROu?Ea={)nSGb^7(<6CRBB=R|=)ux)`O&l#Iv_eFaSPzS6Wou@HETXmrPteLjAjrxSD|}ccG+aJ2KvCUUNS|iG!dj*T(P9Gnq^hHkCTf)=d$S7C380y-;+VQ5asdVf1$sMBr$nKtqG={pMgW5r1Db`Rfuf8TD+(4jtC;Erc^-^sSQfoZ(=?ce8cnk_q`t$&Dq0kC2{$2i#Au*TK{`qv48q1i7Aifvi4_xIDPe{_PICo3-V^M!_{&vJTW>YuB^<|GIayI<D~l#!lMu>lL#tM<5O5{rR*;crT_lF=lr>J1r6Sa0Ho=JMW!OoyBh#F~4Hv{Y2)5}ejIBIa+**Y7<tm%ek}W22NEjt_-h|0K%!z!)Ns`hE&;+s?&4YzlNj$Nbve8Q(0oi3++56!H;N=YWjOc+#gz%e2OBt2$8kb$%2k~ul6wZj4Ku5Q<&1tbi(={=N=qozJ7Mv$UUe?zzrKKH*i;zh3O4yj$K!%-l0qQ6YCLxv}T~b}b1PyXi&~|oDZwi3$Zz9G3d`-!=nMYa1Z?a_LWVMVzgVTtXlL^rZr&F-Pbts+3v>gqy!&LeX7ON?(5pgg~H4CO;P6!T`!6=F&dYl75`a;VcO(RV6GP=3pw!tErGeAr!(E{|ujF)DXb3@N=y!XF-?|uAm@%JmgKj^*rba8$5=9-`1pMB=vuRmR$^TWGy;;Hoe!^PEyx97v_^DC~{_<Z*9{QCOb?>qMIM2C}4G0o_opf>Qwv&G~c_Jpk*uk&1aM;+z0pR2a3ycaEcY`My@-w=k0i^T7FBVO_bq=r{S&~HG=XxutEQC{mgew<44m-P4o&EL{)X4d;&b`&-J94)SLA``ScI#u3rn}(KQPmciw+A+AVi5YzjUxRu5$y_``8?I0P+b_7ybLygV<PI8>aB2mUi4&-i+a+GJN*7j6D;qiw2OI2C>p^Y6qQ6E<uH<r)Y&F`~r1?aX`6{Njtls2VCQbMlkeZVu-|9SD&8glKUDIyQvT742=(h*YM*Ys98PE@UY7dltYN4zpUzL7pqpU4orOO5Jc_%19fB@iScWLejaDg6qwTSX+HJ)SpP`8#k;hgF$h-B1SO%?T|h$Dw?w_&aQzF>jL#F^5D$(;vRy>ttdEctPX$Mv8$H4W~#_zuO>0d<tbt9j@HQGjpVzoUr^l;8z#5xw#6gZ5zHx`(G$*`6OGJkmD537xiz!v&4dY|{j+XsUaE)#?_*ry(Dr6RK4Oq^IF%%I}61PHw`?uZT$A8x{yshgYix0~MLIy;FDnc6V@a*YCCo-d>PpA&#v$b{4+hW)8re_ni?f#sFpLg1c1<bi<!L63OP7<5F1wfOJ0s->>bk`I5V8z4B>YUSZyP_q$w<@p$Q@Y#Py06TMc}!>X*3(ksjz6WZSQ@jmb;(U{hQ#*D^<2_k?1znKh(!v(Q#=)q^AV1faw%!czYn>lfkEHjYG!Uu5t3L5RLd9nFj_33?gX=E`MF3nxOI7JUw+GmS{sJ`-4nTQF6w`Jj0D}rRVQTL1Q5MjChx#&&3fJ6bJW#<+HDE$1QoZAB)uzZR@T6)tEQX2XnZx>>nF_FMBi8mN;oceJvA58+#hZ=XCVhg*^oUz%uZqq5YF_)V<M8T8HkE1Mi%K32LL{=ncfa8P6fzFZ}V2o$zt45b-sPKcSlOLEsX>-spo<_byqu$R*n71$(eQ<w0GMM`!oskqZXQ7Zk<0B0-_UWbnrAf>R56%}L)pRjHoe0d1q38z#0c50qj|c86pD4QB>5fSpjTWm=w+I#+2b64Du5^pF{(U=efAyQ(ltEmnHG$Zdy+r$KOh3oiWo|(lkgcibTRwWJE-%f%-5QyYTTlakCxin@%Vg<%aeE^YPH(AR7-wOZB~j~)cPH_Q^E6FT$G#x_EMp0e#F+7ngy94#l1=EXbS~5l6uCW3QuI}5=^;;7lW@3^-MLhomfEzpc<^6edbN~AFIIf1$;#}wC5T!!>JmG&@6c(bzB1NuYV~>afgEFBnQt&l*L#j}#I#{{fZLsVGzCnuuTe-Vaj;M$`X3xDT#)x)+m4ZnsLdDr2b7PTNwNb;;*f7~qGnP3#HvgRbLhtj4$@gfKL^E3sj$t3Z7F=vg)J_mvuUsmL*Hqsjyi&D;vB0J^<16OQ%kk!`Iw$M>Xgckxa^poA?~!P{&RKW4l3|7`%EU%EijfAAJxKdcQA*0pHFRwFgQCvG*h4YrO{mMmQm*1(`4LN-b*G<2BYQnR?<!m)q6#)sO@^~n}QYLl^Lbq??a?oD*S{<uu|zWK1Rk#Cg({Wte!=O#BUY8uh*tR7A<NO<bd5;;DI@Uu<d|JT0?*5(C9t7#<I#wXk=zz$VvwfQTG3Db2vFxh*3`C`o8^OGrF;CxlB73vLV>21OCje87r)@ass_;#y`1hzVM!*z4O$r0XpT34`TVACimGc<<-`yPkZTLA7y-@g;$${eKf(JWcPj9p$XoZD&=wlVDJ<Tu-wcRi!dGP{r=EW4{hnA1pdPB94oOX`0oN*Ak1VrBjw(2GFZ##uybIZE_!L|r-$2fLOIr1n`W@eR$6WraFm0zf(Y*Ypt27xXwF3q;A2mX`aZdEOU}a+8<2eZlN)6VNnfSTSbc4&ukAXD_OCDGkVlr7<^<{GkyXCfv&wo#%yk)t!BZ=Ys<5D-cC)S80|F36G2dog_BD)UqMu$-seO>;se}4-G86wtO~voe+Ft9ZNs8@>YI-Nn6%^c}{D8~7V^SwuFI{4x(m4zYIjk+Wp;+RqQMd?ccBRQq!5%SQ<*;KlXJK?RBON{*&q&M9=C;e)x!H&4fwte0n1*+91clih9PsnAI-wEjIs~D2OrV+11!~RbI$}F*?yp&N-Vhiys@|}*krndu#pDgXRM91jR3^1l6_mA(PE-X`cqJZJBB^f0gg_jSnz6Xirp%a4LiZ%Q^;po_wfzyI*w|5UECGX8uU{?`jR{i&aXz=fHby<O>%tz&mI9ul-K($#uB@8W$FbrcEudEMs&~vhcC4zSWU>*{D*z?%wN=;{<k^U7tD}y)hf25SBLMuBb*Rj@EnxC=|7K|**<Q<*+Cwo{!baN@6R9zOYNIS{OAE-M1o{R70nF5Z)EL#)Q3xBE*I42lnzGGy60I^t9mQeB(zAEcQho3E<iOA#?UffzDsVxB$5x#Nu{to+JXif{gP&+U=q{}T+9Lu>xitdW57lC9i9q&2z?K(=d(Z$*G;LfGVzgsG5D)8@t*IULh}c0G?Gq(Gw`lt>n8(?u{D^g2oBj2IFt6BSVzkCYPQ)yJNJR|pPZAOHyUq*cz34C@iSqWat-SS{-t!k!k5-LXBymCfrxz+6;6z}BNd>h=Eu|Ng>sa948tLqhso3rWv@h;~J(R~=;x|56RjUJ@`vTl}_qijF&yVTx1wS62!2ZYbv)3UiQs|;6Y*y+vi!PvX?r2c-xlL8^<EUU{rClDYzSnUAi7btHa~WS9(Ie4<S!%cm*q+YjX))ix60A+sY@8-`cjIf*O7Es`8^ek{0NJw<?crdh=p>SttxeF(tF&KM!rs{076<v(-gzneWTkS2oo#K6%V4lk2Qbu3FjHwc)va{3L5*c=fe~~LQHT!G&d%N~3-!(wP7b@WrkwZM=Ywr~C0-t}JJ<L*`+_PA9rOzWHXE^v<9ijy&HHGQ&$P2jyN#r|>|8O38JP}q%X@ld&62|JU@H<IuhUhyeWXiI?p`S+NaqzEB(u;{I!ou(qZg_k)vgF6M9?sYpSoLRGDkvXi}q&0qblC9s$<Mz=Pd)pr>U)8)K6KA`IGGAi0$<R-E&?$YqlEcNq!~_PRg17wi;EZSXn%3vL#-eY>OB0Cz!=-y{MeeOAN3z+Yvpp+_f4N8<Q5QRi7tD)Fe|mU5jxrlRYhfovn#KKZVHfTxLEB49UL3xo}o^9N$2XejO0OLI9;|;6<le>ZAwoF@8M)Q*KqIO+H{s-=#PNs0U)YIeVTg_?(E@R1YK^3UqdC!;fM4w17pT$!?R=7X|;XQ)-2CU$QUtx^ShI^V&nRyyXQ$-U+4z0s8qdvuA#3d&ey%*OLml{@7a!%!7q$KPY^2V4(rH6}5m!vxk})8ce)zKsqX5I_0_N$x=`A4<N9d+kYp~Le`6_V7=OyzzKNE5v(=xP7BtC=u*x_B(VC5SzplIkB@VV^>bJ+rq(i3YlBIY=ejd~P~)%e_BjoW0K|U8v{yd1WPSMbhVBP*hBil}?4Rm8?AasoJ(h!*skqJ0N2j%Csx#=WS#lfiw+Gxp9o!IndzHmoqx{}(sfq*-^?3X2g3a(32V&j0P!8MR|MS>=q%5lUb-YKj?o}xN6D>-K_w!9?gqE6aTJWQAzRWjO;te-p!G>4_SkhSVa)WpaM{|}3i;3tw5*FiQheuQE%d3vq6o@YNk+#%Uj9zAwg#XS7mK*#FeqmFey)`nma{#$Dt+R(HGgDIuM;{I6J_v`_@Hx6ulPDEOm#>Y6aHZYkGpgs2z?28+O_*oC2rxu@h?uBuEbZ?-H!PWV7Ao=9f}q(xf}@ys7FaN3?>23;&i2OI6NynEm>C3n&k;O@nk;55S=X$3`ge3o2Bct)BuKt&i%Q860f^x+j9r2|KA`xDifv|kMJ?fSEii>v$MC!({YDGaDW{Xoa42sDi!?ccWP3U#jo{Z-00DTQt=gUXWJ+jwTEgzzEr9});$ifJK1%S)Tg0MVp<HGpu`CWrQ|&ewbuph-F`47aIc!2;IHaXE4G}u@x*^o341tm0mwj`P@iqJmeFc7QWh@vRR`Us6A_jryA%O^5n}FJKBxH45JkhE9Ql2^>vkof<ThBy-FX?nNCJ^)}S|PO+852rjAy(?>o*Wi|{UJWQnxinzB_f9;kBu>TBnzYN)lDAUP;k-b#i-(8Z{<g2w`SXxK3Z5$V)=~9!hhReGLydnFMRK<gLoBYPU#V@X$DuneRy~6i%vj#Jj|B;Xi)l(byfFZ9y~nq$vx~8rfO0f+XMH2$V(2b8Wi1{J|r#(hT$;?8#+*iP44>}Eb~m<eyBn(DC1UQ_P7bS7I<ivp8K}piv$7stCi{AB_1RUvQ-)mM?n^ihbCaE@Rci(b7I2!MY3R{vv%HRVd+tKeIKvyNuVa8TAKx0k{lthnu@!NC3OZxXu&AcOVlaX0e!met4`Q_UJMUUDp#&A8dpBpS!Ugbe@va!*0OMc^SMK6V-(&GvoR68Z!=nSkQ=PY;BgBC&WYMJg4QKrk0#(zYcOLvtq@&Bx)-0NMO>N0U`~>GfZ3->GPM<Y9&*p@nJLh!Bp7z64PHZTJLIm0>nI~pdWZphR_q$@KE3(lN?d3pA-TOzm)F02@{hcB@1Gwo&xhB)eR%Wti}R~1-)ptn?Z%t4-_I}4uKaIyK3mO43)nfj&aro*PSue|YMOl)G+9QcVq(iDaQvYR+=7a*HFXJ{_*|!@PNZNIjBmN5Xmn3!GDk7i#<)p?jf`@1x9<~r;xA2nYMO6Z6wi`XnCEbpzt{z{_I(TF?>(9N@aoOk$8$o!_r~9>*B{R>-kx7tpMN{MI)`&khYOFE8#TiENH8(Py;UB?nF%NU2b;!fAHC6fmLp74S9<-A->&JkL7jQYGV_wr7i#8ZAp&xSOv)m!*jMKt&)-}VbFEdKgs|*5t1KMe#K|a#wG)W9{~QF)em=CC1bN_@z?RJI?v{CJI41_|%;|VVxT23Lh#8<`(BqOG|McK#9n#K*r91PoO_qmq-~Rpl`trjYdw-pA5Qjq%xBRwrPs2fV_9O(+x8MBvhR|->k2hoDE?ySEc$N9ITD1>hIPu%h8(W3ILof-JFhLHvDUB{D>FrdUgo`A~iVBRfbqt(IRo?G$unE(wyN;h~sb@@I7RiKwtq!OsiH|VEC0Uf$VbWC)!5d7nA)-co``w3soxipB*6@$F5g5&bo3O++$Em}JACQ3b`Qm-8lUnU@5+|u1^YZ=cvs!KHY(8YUQ%m(S<MV%gCVD)7OI$*h&+eM_qfI7jW_M}Plx^0-?s8LQ3nDcV%i<E<<)=P>8&DgKIs%nZTy|FCv?!}0lHd|d7R7e=_`A3clf^W;ad38NMqf^54}n(ZwU0up6a6tw?qcC_@_Ym}>%Eov3|sFd;=O3Bk!}s4PmypP&yUh_1@rsr$YQYnfYxH{n`JRa|Je5pwW+ZQAsRP`x-;Y65zj9O8Ajuq86BJ?#R3UBUXYe}?(boEi}0QmO1C%nCed^%Q>1=;{z;|frp94P^7!1t>kw?5pE8e>M#uh~MvHMogfOvQU%h<?E!Yz!rf<K7g7*d;+5_U)(_j_nLzZ~-FlE(CfDh-%PEDRzrRMLLVjPWkD)QVb70=@3EZC{l_9|7bD|)5%PxkiiG-y>DoSVv5ga`2Sebuo-MzW_PrFxhw>Cg|UB}6~4E9Bx}C(#apaUMrrt3fhQUM`v(c(P>3Z_zpe3qXIC{!z(>Q7n`imR|(87M;)*ymin&41P)8w?S+9Fq)8H%-KA;nB|9IVK<<!cJohLf7C))Mc|_EOeOMN3)Tev3IeyC(<d!5lHMGBrLKucwWug^VUN>5#J#LVNy(IfB#As3&Lr8FKvD>p_u6?auFy(mPnnEiCLsH8h(&=#l3+v<l{Z<<mzkqCq{^t%;cd9dv^2>{8VJlEZP*k;Qc|%6wa%lXda>!k%B~|}Dcss}p$GA3xZL2ov!(o~{y>#J8LqopPN2rRy<|U8Fa+}-u6jZp=)^4_XlPg?VhsR}dm#yHE?{wx2>O$c5W0vAf_OXxR6_)j6AN)ha~(A-f)+InST#gHc~b3#x(xxpm?Bv?!xrh%+)9pA?ibNU)O6cBNtF>5dXp?NL{gcCLwF$`{2O6L3}DeG>CA*m^Gb^4Gbj_)j$G1+8dlO5=D#4+3=yV61VIhusmJSXz#}Be^6NP2M4)9@D;*Pn;Gfx?@I2F!LzNAbhf}$_rDECYmEeqL;rN!x4vaTL8j1J}hGl(Ci3zKZfVTVe+9pgxR2WP+TpKYQp%>Ai6)d7D@`lhI%-qzC#~x1?G4#}<$8;d!<W3gdEJzj=FIu_G(!JC~C{qb3eVl|hJZA0@B?hm`=w42^(@nQqxrL4kfc+Np1OlOqlSik1OVPx%&tQUxcSXe&v>vc3`Pc|`jGG1jW-nMr(_Py|8@u~>cTl&08jYyo{K)PCAbXK4433A4SGx;fZGx1xF6ew%8GuT^6KK5feF0$LYt_knN6YzHlbb_diOkdJVR)aU@#McqL`q75NCRn@4DlE-{^UiG`-3GIC^~X06ek?fs#9V=nmAj~x&yzj2a_z4v5dr#kxmWh8kn>-X%?<q#zdCz4t@kLi&o}!NP6>d7Uh{!R8UJb0iQ<cZp>y;4Pg*r+cz<}y|Ba2h&u1hbcF3hg&oj!?jy$~Y^xbz#?leHRP4UmiGGh3YrlO+-+Ecb9WK$~iaW?M>fjmG=-uf7s3dG7HWi;I>Q27u;X3+VhFs}@dA&!r-c|?eSAP4TETE_7uku%&Ru@<(!q!Xk4~iw&Fj~N1z-z16Kn2|W%{mkBC2(KjOx*CFH~EajBwqE?V=9wm(X)%UlCarK5nB<YQNHoe)mvD~$H)>zoJBZkVtX(IR={Q>ZCeVE_z1Kh&dK_N1gR9kY3xhL#24u`N?`oQNEFs#|1rvxDfW_icoUF7*LsRPxYU=#vn5FlOe*?eOb@*{@b{!?_2N;jc!a#MUOcW9kCC82<B+1`$HB9B^ei49m{c_Lj1c^1ad03F0(u@%6Ndl5*AW`DOBNjsfDjhvJ`k5&ATPuRxpIp`=lGcp1ajG@MOsf-?vg?%1S<LtC;ZWmlMdVDJEunq&gnM49k*X1p$`G{@Jq{fdwN@PFncjZ1pq^!V7oA`N|a2lUR0PDdUM_X>_~zbhs-zIya7*`<crDp{kCEct|oObG;VXhw=yhwt)jA==hoij5XUZQ(hxnz;cc2i?TA7NZioU|AXWFu45K#|+*a6ZLsAtcyd#EL7*F#stEqiUm5@pz?r5u;ELxhRE88{`frSW?=O+0vJ70B=K;NT4lqaKzmv&c9M%^My;%G7?9>B_67l<W2J}JwFdJw58HRzaYd||`4nIhZu3v)S}_F=9_?n^@C&!x#6^tJTG{OIT%JdR0G2xvik*uQ0_!GJWc#bmgkPc$EA>GqEXO1_QueJd35ErbOHF1LzDMR76quU@OwYAeV7upkvNns7J)EqyUXRaC`B#~e!>^U*luYQs6n91%mMY?@CrU(JW?F^v*ZW=tQbR=hxd5X6>U26i`4_J~9eEShc(|5F?+Wh7cRK=B=6s@Jn9vtGxnF<Du7BViFNBN@jTsW)+)sXd`rRET4bm@v3_kSXfWsCN+*IWxYci6az^583%}up-7TU8W4b^~QwriKBj$Ola3ohiJgcUo%^!7!?<2&|Je@`{&rHAm<3^p51jc_Gp8^z|4xF_TNjWH><-QpLwOKS`lEG)W53L5(gmZV-;PX$l7~aGy$2e*M9%62tRv8pWZn2o%I@NFZ8oDa6O$*yGCBI6p1tdR}gsM()-%{DqK?Bcxz&b9`U(TA=K3S`fRoQwbiX;uYD_YQqWVM>2B?oGUa+bP&U?dIPVa>rJk6$4?EvW`2p!}f3x1ndWR37f@HbWB$KRSp{PI~@i%F(oJoA80+S?Ri5jpUK@(>t3xjl;A%>RJ>V_q`)?2yRdlIM{I!lpHXrzI0R<#`1NEPE(qzH{_DMCo+wxHQbd7w4arMfd|Ms##@n$d{UjIhEa;QMIO<9475j1KCfFI|&k$N@zvG~LiAMgO@g{5G9glg!tE-x<+@jtdu3=gx<aKV*?V$xQZSFQm87yy@)AEcy>WjJkl&tT{ZR8E1Y;N2JJ1vO{N*HR(ujSqeeRTC1>Ja1a}mJCo5F=}b<E=P5E=2W~yjsgnE(*D?)Kl>DlLXj%<c?ln6p&Iu0OHTNlKT8I-QJn<H_?zDWJR{gyuA(N${JA7MFp(@_iTW?4MvpG1DuNWYLtuq8@d$R1z0(#qwK`->vEP(*+3)~`<{x5VRy-daK2V0<NEaPAi^6X1aa93jltZsmsus`mK{c(r=!LKeZE5LNOxy2nHT;;B}g21mK3W&4^Bnb9Kqdnh7^o>Nd2A>mbAt<+bf7$PL1|`&V^wx_;dRCG(5b!f6<&8$A`2d~$>eFE6@LUG@cs4X#Y@nP};l*rlrcXkg9EmKzPLlhDrYP)_f;vDa#aT+{%_tlu(<w}=Ksf1kOJCv`ex?<)i#?KuU~-@U%N_|tkU78^wO`aT?VqYJDh6m+Tl;P+B#qD|>Xl~e#gdxp2Dd(=m4v)t^2Prq#(^$`cv-d5awV25&L9!7<zQ>{F17D}5%@hI^b3PZ5}K5cD&<tiZDb*-O&AD4-fk~XCW&xyd~h3*4UbZt6v0XjIzt(!gu8<#>UQyiyIx2)1`*Ut5dcDC@nEw1arMa`3vHgJGf(WmwyM-<3K+W1mV6ID05q~1L8kuW@<<Cir&nwoSoIA_mz;+?DQ~R6R)AdE>YV61B6x{<29&z}OJw}wz{kUuF^s#XvwxJNVQI81Su|g7BL)}0pfX?tD+Wc76!_fH()%{ER%L0$A>m^4m@r0q<r7}djs~$vu!AoIVmB!o0TuvxJkZC+nA^lwDG_%C-u<K<>DEKtnzdGzuf+=HHf~64-ZNtkKB57LtKX6!A<>mqp}yr}NeIi!Kv+W1E1!xzTSsQvqMpch&Hr8K0*bKrfu<67C^0Y-^0bKuALpaEf<&nUEGko-&{^VQKQ`gU8S2h9!vZ%&4{n36W*dfUVn?jE?GMK?JmlvLpLJ&AHg*N^qKC5H;~n<m#P6HXs)~TUBj6mlgWfEnx;i@RM|H(H=J&<OF^i~4Gfp5-z1&y7QHd7gix1f5@m%P|Y|>Z$3GH`DvLB_+oD-)1x?5Kdv8<BK7S-TBkA;_SmZ6vBz#9yKj(vUpuc7Uh+;wL_(q=CbC~4zxvO*v#--;OA5MvG>_)0FWW-Y^X9_6$Z?VVvWkWUU523%dCI54D;S5f<KWh7mtGDG>gHGstB75bdnms>t<Rr;b;#euD~=ULewK3&q!t7SOmya;-=K9W`uQ{g_(v$EeLL0)^S_Iov><D&dtIHL_Xd%V-EZn9&#aALDiy6v?#m9p&!^}V-1ox0@(L)?fN*DT0_JWm}iQT7laPeZJ`WYt%?kT%o}1f1Ha_9R&mml?8gz*c;L8hg?Z^(K-4F%V)u<((=5qx7RM+6c!<I>{XE{dDVgBi`8hBMa?M`K#8M|8qR%FH8Ho$Q>8RWi#^{V*cYIe$`IIA)@*Uu6`sJR7Hb5oWfPu`bjMuq@UOPsROri5mLtDi-Yk<R7qATErZ6fZ*a|glB5UuI$iquLQ*fA1)Y;qr{Z7V?m_9>Arm?U93o+5cWu}8i1*W;cj##rK1`w;7~|+{*bWQTgZ?;(@a?$?Bdj?}5Bl(g54wqI1=&oTTaUPFjY~b?Y+rGt8vw*=H551eO`K016XM|`J>%0K*M~OWj7T3xwySh~6S4OG<7->7+c?w?e3mdwwGHVI)puI@cq6{$qR3oDm~EFMTQ)FWJ00IppzVGx@h1WNztI99?}1xZ%^SfGNDI`s3;b^qJYsh_a75W7F%sGwU`fz<I-+HWD<wH>suUMXi@#mE>)E4<$N<<kvD6ybcDG!38itQXSf%8tEMWnt8z*H+@PLw8q#9P~;-~)V-d;q1Ef#|G(xhr^p`wY9^h>gf2=PN*9V$;U6oaST)f<IndW;AkRSX+CZGQ&d?zRg%d1+bKqETUBx4VxU-<2)q(?a9gQjhHJ)~m9&r6$7TmT*NgGU{6)+EO2-3|CYrgkXrva9WpAGbXBG5<G}j%^`MLmr&Y@O+qRXA1i7ii-Y1ZAigvdW&uQMHiFJI2()F2?=|MKv$H(J*9}LT94vf`g(y;IbUfmk04W23rqK<}T!;Q(?eZXB(Hv}Ay~%1^y*pJx*yjNWtd@MuN$$;ALScuGEs=c~;x2I9uE2K}G}93H@W2cS$omvX1B0ou$Gbp*1rv+wxCi$CLEfRHCFB7|3vv2>q{BWWw~z1gF#?KX0|jb}(Kxa<5uv)Zjp>7qJ7Dp_#2|Rf4Sy5tZ~&=}hxe99b{~kV1+$Xt3yp1aNi2|*YlJ|_*@43lu=WAtfH(%23Q?(Wj_j~<bM)aiW+UGZ*WdJ|(BBWgq5JOuJNimG=n`@zEh7CIqJ+x#6U6dy0wA1C2o5-&G~3c#%I@l6i5CzKZW8PlU=gAlfxr;|J;FW*O)MELAynh){nvmMDX&y|AEfgpF76$t0d3w%a~;JoNwsJg<*34!T_gA-8>i8d^|Wr~HfxZfFfzN#S`=)=ePk}#8~Xp%9w_<jveVSJ=d@}+#bkMHXgMOTQ;@u5e9#ai*@g?m+}gN!IEC1m;iBIV2}(remfm@qHlHT!$qrrr%{nLK^98E&AU-6OI^I}9bWk#qDPK&iQ>5i6<HWf*EbcFc11Z4;H1G)_txgW#{}+h`rk)J_mrr@OrvnEoTBWqrryDj;!fKO`RD!GD>_VL@g&f~6k3iPywgoTWuSr$*yA;VeBvM$0>y`}cP~Xc9zH5DceQA-}FbC7N=~zeXCx)u9UAfW++qdB0rY{mXCUq_@U1`s63ARw4!27*tm}7%xZ#SEZq^Y?L<7YzxR(i9BCP*L6U`-A+tybVjOT!p@>?m~X_vfFGk@4s7^8D=WpSF^HUTy}xX?o~{_*L$-K#H%=-+#EU&i=Um?bGFl|2cnaU4J;gq+gek2J?@0&yu4<?oW@wVK&wX3K^dzR*<(lFT_Jdl$Z_)K9cK$8>Ka^B43PVjB;&vE$3pAuB1BE^UWuZg>vq#bVeVv`C?d8r%;GY0bi=yz$}KJFF(Ee@bTO);3A|7x|`+Qm0a`e<Ht|`<m?8y;Ig@H+g+!9s`~W*sH0Ag2d;$5$Kiu~q|(0r@?AQ)`f%~SHX5FrA`dm0x#;meez>}p;9K0vojE&gP`L?<EwQ8i0Fo!S`$Ww8@&hr;CmTzKLKE)8G(yzBvcG*V`nbA2yLfwc`PT1O622-)US)1qk<(S?a@BIU2B70AuFD{dYAM#cif7)+pm4;82zA$}V!OsDj_yd$-Cwl~`yfOkD}5X~+sINlMqG3K&$@u7s8B>O>z+8>UgyOzB)9+JSCA$4CE{Fg4M&L75azV5&$C}e!l2(CJPIoaLSend*a-?R%8AXH;GeRr@L`l?TvDM#cPmM9Q2=KM01j8_r8?chU{#LAd$-bYx4OhqR7Y6#lU}d>c8=e6Uf&~`eESpl2#sLap!GtSWj?KU^^oIhDySzhhW|uB^p(}bVUdkMNBkA;7F&ezaN3!U$ET<5_DT5SMf+v@#iZ34joV@H{6*{K$q|fQg%DlMcj7+}vJx?-e|p>^me3l=>_`QK<kPhiF|d(nHZ+jXn_)slrV+lg3DE9-`~JP;srnoTQ^*|tsTnFzyS4qyCC;d`vuq~osamENtzRh{d@oyK{fl;sqV{62hfcn4=L9pDul#~+4cS$$nr0}AS&qUf^edD~#=w(vY*>|4LE}U4x3($U;A%S^R$eypJ+V(YlEh3!5AuUibhW?00QP1(>fa5^WIpwa<g-EfaSze=cS&c!md*p4m6ozKNu3vOpE~Hba|}zW9zOU)(Y?pMZl3(Q3{zyf5L|w{)zU+-T3pYxs(z|j%3*yT-)eKiph!yEpJC;AM=fRkx826i_xos$lV?&=B{SS)RPr0AOhTgf?X#PI*^Oy3US%dMk2A7Ggvp1T$o6f%&)G7sSWgSpMfgAv&7DLo6WaNShlmLl=jpwdc;-)o48s*}Aai)^W?9WeVhU1zZija((j@KX{}9jl)8=w+<G7Uo%LFl*_qfCXcfN>n{r8Y`FQ<8=n#Z^c`n1*Ji=gdyq}<uKB)Zu_!O>|;9eKEv$G(i_Hg1YOMlSgA3nW}afv%|?9E3K6f0;D_`;3HFTUF<0@_&p`QX2Ne5$4;Ub)LR`fOnIG0ge7<<MT938Q;F*+iyQy{oO9gXofz1^h*5Jm8fxmR2+uU?a|9VXsEab&l_%K^A{dU=Eu4Cl~PivX33DVrG5TpvYEKKPrnLqIIV?beL6~T2uWNE$1Y(K9a@nBZJdJNgrEC}6fu2U@E)+`OAT^u&LXxu6hmj@=CM@DqD=-f8Lk7YWmP&}hi^Ef|0jrn(F4}H($@SN{r5(q;AW9zNVUrr!7`hXj8o0oop<|Aq>Sqesx@wwNlnQprsKcj#?i%FJ9*1>v#-LACue^zlCf1f+$w2Xf6={YJaoGN!9Y?O%ytJQizpe%_eP@s@Y=BA%0QR?UObl7vp4}CO1cgQhSa%^tNQh9vohsNS2k&1gWYfzaY$u34)h8jMfZ-mj&rWG7ZTk*GL=e#;ZJyO&ELiV=xT>fhS-maQOkcpfd`U5{9s~_s2!`C6*ubJVk)JZ6_`PAI}tH5IBfJGA4}h(c$X@@?~t$Wm(MIg*U1^SjuP;FkZ}8abBGESu5P~Bf~IzuX$L4ToN|~NV5yR{sOn<yr|J?^tTZ)3(3*<rW(!J=P!>Z@1-3fbc^qQmn8jmiX8^j%BV1!{>Q0rcg^4QN2CbOeZW1N`tjufgb|CZv3|^X_*craB$1McPz1!0FAEW(k9E$x4tJ&m%4@;uqWj_>xmYpY2;9$sMnw7x=KQf_J#;f+D7p=TqcE`YWSTnC7UNT_ou!ydenR8V1u+lxNZ!oM)BfjR@*wM6&jR~J;JS=C-J3**<+xW%~D}zQ}HnG>iNu-x!y8(}~-^d5co<>cz&G!cMJAd1TvB!kB$9z#WUC=0^<e*}=O7ta*@BZXj^5p#kd=IwykGNCT!TfKxg=%*@DF5V;^Q6u`Fo4Su`R_0%xuSX!=9VH^?6G}nh^x01aZz>rLD3KUfZ3du?dgU?9jkD&vC?4WG2Od?i?9;}Dt-Ij6DJx!g2=UNO>e4-HCc#f;6G(*mQZWy!ZE@)^W6OkGJSYlk_1O1p_VFeFTEcmVsi?P=n)V*Yf1$)1?Uc8x}Y)=gxM?Nn@azs6&(k6y|*Orcjuej!RYpuI^*eo6@m8f;P=-ag4G!kx2S0@65DJ{h1GKBt45p=m=ApJ<e3DNJUqx9aP-?f>@=$tD+9U*tEFzR*+>KWy|=*%sR?@*3a#`|O+B>IJvDXD?z6VnJ|TeX*Ys@rUYv^3kI{rGb-KQZefUc!fU&uhJDc@$E8qG%xkf7~RDPyeae-y{+n72(UhfnQh)!NC`)TH+7nZSRpj3_l;>}r+Ilv=KTm(`L_+5e$_;v0}T%IKy)vB0kwl5vSH|u`>LyZPaNTIo(?`Slwb_W-(zff}7KBtFRI~Nh)--LESLR7un;0A!zk_Yrn+?5nReR%~nl9t;l8qeN75FNNz#Z3`@iiQ;=Rm$}(2<B;5_S*MJH@~0DbW4G!s9U)Mq9$Lpq{+RHy7Oehhj$I#nitCD0LsQib?+|eM8Xnye2+b10sZX@?C28~CJjj!9*1H^lA>@;%A4dA=$p6hJ^k9|AhH^ZWrsZr9=vpav(AV=@HH#*0KQoq-yCvjNh%{?rXwDdZ&l<aN!Z%p@6zHA<i?WjMBTBw7GB*cEj0f@SMA?z8eEw!*{S<54%sixJC%LKa8e_~TQE<Ev^deWT=?$J9Vz;9H>#^9$#As*L75v2w4ecBsp&`PL?{<&G_W=hD$~sOTiyDlF6QDmdNb)!_w#CmtYjz7_w`V}eU53$ND_bD?E^?hwC=Y*Hck{S1h~D?q;7k}<;7fH2wGI6Wi7KQkmFPoa{pJefC%7%3O=oJlDvL5H?H8S<wxtDm-qRG^B>tVIRP7nlSR%9L3*Qh36F?BK8fVz(sU`Ap!UEhMKzxEn7Y+_OuJ&V6a=$R#o52#wV`K*crMv&|7I&M=dlAb|3>?6yEtW^Ht=4VtFL>Ho6O7m3-_7K>8oC#>Z#WkhEzCN_$rZF9QMz+$&k5U<8vjKd)hkFxC@MA_^ps><tVqi`a#)Sabz4{$Pda6k+w>zRMBMj;J>;)yS$b=I=2IGOpKWhfLTTlVa$AiBVZ5`*yIqrGVF|_DU8U{Eh8fuCfdS;NN`BR@Xe>+KYu*GK7TYsqVazL(d_A*', 'offset': (-1.8, 0.3, 0.192), 'seat': 'WholeShallowRaisedMowerPad', 'rotation_z': 3.141592653589793}, {'label': 'ThreeShankSubsoiler', 'sha256': 'a83bf91aa3a0ec8c25d15babe94e506413dbc96f932e51b05cf920f8f7c9377f', 'encoded': 'c-p;vdvn^#vhV+V3Z1p;l%#l206&sIwCXsC^Ef-pN!i|e?R~fuB|rwn0%1vDlT^O@?O*qdBm{PnI{V&K#g<0%=;`V1>DP>Z`|Y<+X*7)%L2TX4k~p-kqx*1T<+C&lo0BkHHnUl<xUue{#Wb8Wmr1n9t!y>Qk|+*SYZ7J4IN0>8ED!Q%Yz1j<C5w3D{r1~$jcC41=zSjKGxa4)7HSq`vp5>5Y?G-xnultf#Bn&zqhyh(C=b&-N#d+=ohEZ@Nv)`^r91gduZ_#A(~Bz~Ej|2j+}@|ZU-|gt42RbQ&~WH_X_zJPnm&5VAPpCJ<Mi_K?8>);X&Q}JalT5!CQq_ipJdhy7L#UmrdhL?YO~e0d;d7Qxcu<x+_&3a%WK)as}ENn&wTqW<LnCES#PL2>yo>(s5|Q~?#}wm-C38WJG=4b?DF-+htF5s-={@rEyBBaV+E^xmZa1|mV@SSQ>=$9MF~=tZ>S1kC=TZ|Q_niJX3=zJ#mQo7rG(gEF<r$$Y5}h!`aKTPGzv56&dNgSJ;*}~D6kgvExEI<lk_e~C(ZFHT@&aQAv2m-f*&hdSmOl4QKNaXTI5_Km`vg@Q$!>AOm{s>lVC!$w4hbBMlsdY6l4irtstkGVU$|eVaR}|L6l*lX=H#7@;n&NFfl#R>ok~$77>viBpBx_qT6H{F06193cmBZgr-i-M`<t)GtauBf@GCv(Im8{!D<>d?`B~bTS1nE^HB_RM2m5}qR-c>n93K^m;ez}5ftg1rbbH=eN7fQ4Hw+=WTz?3e*%a%Dc+a#KCx!BHVj5KPZD4wSz5v5%PPzDJi@sZ-V>!qNty}5#%Ype)Lpa$u(ME4u7)l>GXedYW=4gRkPwXeQASK>SXWbw=1k8zPY9`msw7nw=tj|NxERl9QkzK{tYTtYVn~8aQI9}*FaqIWU{%rxF*w1Hq*gW#X)NkHCsLVv*4a8tH`Y4JA~YK(Njf2MlGo|EXDt%YOgtGSL|@cFvYHYQ1j4jAW7<;ydR)BF5DUT-#+)a2^e_#Rd6?5+A``+1CYKX#tR$Wg(cf7l6-FVGJ0Vucg>ifxqJ2)JHbZxTMbsUGb}Im-A?Acm!Hn}{LWuqvrio0L*5(zHaZS*5F)huJ)S;rD^PC@OV%LPg5fS4}a2ISqt|aJy<RyVoQiam1nvyW&mee;SRUp+%HlPL0WetIWG+BqzJSJXK0Bl4s<Qrv$3zFy|5gB@$2aDA;SS1a4`GV^(-w=5(b#<yR;V-m~(RBm_Ttw5UK(dJD3<eWmgyoP~(5!QA=-G{T{<rVFj~~wecIo#Az1N@4uTEcI@$<XW&;0w<r;9UwczZ^Yn0|jazx?p#Y<P8c$rT%)Pd}brU7h)T$NqCgYw&4IJn$C;;FU<O)5YX{l#ge&a=gPA%Inbo_MvLK%6s0zqpKYIHBrtu3F6Pp0q?-;S71&wY8@RbuXRFoTgNSF_ne-equm=~dx&k8+BDKBarh+>OU$EDlfx7GFQc6t;}xy`BFVrcArk&Ck~t#e(dy_>T6K=O)iXRka|aD#Sz7st6R45fO+#9gg_W;JpgQ*l8^~VkUTq*|zeY>0<Z=@tuzgLMk2IODVtUK!O`c@Z1PubIIZ5)Z&a>5=>OImmORQ=WC+N2aPe%RDpc&8)dTI}perlntC0~_(YNM<zU!}_hi4rF$K!D2NWw&YW2ylTOc}4q4wHnW{{ZzM>I^mq^EQs~hT3svZNfBd(Znt5r{k~v<MYnTJe3Lu(u6p4XC|UC35|8Ua@7grD<>FfuUk|9GBwo!!ABX~c>;5fGWS|5uc#G(be;>351J`|eVwLUrF~Va?TTSS+RU9s8gl3y2U`5xu_m{11F?<>lZ_@5awW@&hG#pL&-LS&RG|c>pQsuqICLN{@uT~8PDl%((t8V-4?%?3I-)$4TJ?xDn;DR`I7QWwR?&r??&WILcfHHK!-Kqt;;m;mz_w&qgsVo3Mx*vh>k9OF6!Ckdp`m`=DF>lTJE|+6GUiv5#)qz&0To0?VN=mOVcT8w|*T?(7pG0F?j}QWsFhK+W9l&QYAn6vwzM%)7iGm3RVlo@f!))fnNwUm9DhnUL@hfPwx8}v>ch#r&-KCMmT(~rM`Qj8kU}>K$4x;+XQ)MD16yB7DTdfF^-A3InzC(oN{^z21?FCEHekP7{g8>wNeo@ZN0S{O{MIbHBG=!9f{>SV>GBYL;SSIlX<Bd~44(6jt0Qyklu2ZnE`@|U=)^(ds!Ny!}>JSA_GCz*8+$rb7eG^%c8U|?(A_qE4X@D`FpsyNTqM^bMrcQof0ww04VLXj|heo}dkw$D`F#6#BacD62MLG)?L?_T=_%lAzFk_!y`d^wPtnlD`0a8sD1JsEi>==rEFc3gS`uBL?zVwNr+nw$>fg-#Lb&FuJaX`tY<x00$>)$s6_Yc3xO&P?MS`&zU;U(g)G5s8a%iMxA2q5%)!`m*^<)s<8TO$*43u@r+gm55fnJk?zZjbd4su#vt*kxtgI%V!8IdMh`SL)d3$)cIDH9;!Kcm|agMwLzIt#mHb4HUUOO;Yq#Xz4yrNsk_GggcjN(^8xEmJI&+rB_Q?^kT)Anyd`REkV@6s7r8Y-=W<~ePyg+*Xr}=1KGyDvfN;iu6d4e#I#{J!0ldpP|j(ReT_m|iGzh2(f{CJ;exz>jvXTvQJXLL4=5kllY|3D$-R7w6E%zKJ62^<m_t8Ku#wIp`Z*|ON`-AMY)j$2E^Kij?M;Ji82V02brfqf&XGD+&lFS|(u?T%h@Lv?gvt)N?1-K_^wg&M&(yIysKC$SGnq)Yz*t&*R13e|!5r><-nF5^VDA9YT>I27v@meXD0A*;GVV+71rsNO(Q<n$X(yZNouXFMcD?pZ!HV$8g3|Bzp;9dsenKT!sq_hNBjY5K{Ui@oPok$JZxz0;*QP=iEov2HgWX!-f!Tt<cEBX9p}(_f^d4MeS!FgZ3}47f2lr9-|BpGG94o{qr*VDXzPB0OShifIoeS9zY}EmOg=@wNYpk3=bIte{x#kP=4DrrmTmy8<9v{T=o$SSIm-1@s)F)m#*hd*(XyMi7U>{BJC*i&?J2b(ZsZuT{00xiI0PD>gvhOBgI@J7r-%|H&>7xYx-0vJIaW43816m-=WH}2m((@RsW%RUjV4lu<Y3ip>x95a%th4mOOl74dvp}L8q!mPP?*|n=IHx%mHGq#jHR^nF?v|2=CpIAc^cNXr3rSz4&RBhIsjuxiiuSKB^pFRZnC1lS<$+Z`-?PekMl5w1hQXsNOjfFIv(5TGn$E7MkBoUyTd;Nya-JTP(`>`4Y{G!`UO)u%JKM8tk+zidBhI|M=*hV86srOGEEJzd=`qvp54cps`$1c`C_(qzN>IP)J@3#s^m71AiVIJJUzoywY7gHff3**?JY`LS<{=FfnV??lMF*BO*~QPXb=)6FN#{A4zFzz2xH2F1Gl~<l<~<~ZgK1S}tTE<_SD_FOdQe~hL`>sgh!zPL5*AAmaRf}8;CO+}%xfQSKOSQ{^IFf2;XR;7!heea=jTof{(&R?a)_4~EvePUWcZPLKR$+T$g|K0dn+!}*WxiP&{rT#L_fD6*$<Q*wiWP1zeozxPF%&$kNvRPZz#H7vdXL#At)_T3R5a(k6D@|`7Rn65RFVmBoOgp8;>VMpGQZGvGTD^NFszh!!t>#rua|vV_V~H_vN|9wr)J=WwXQ(Tg8L&j!A%hC_AW2uxnzuh-~ezHmM>SW#VYo&eA*Dlyry!lMRS-#@YiYK4|TbUIM|uQsKlU?1t>2B;=$^<HTd5mhktk4+sW*+gO(N0E*fDL8+VF^CP%yPi1j@nFYY--8G>Z%EDkpfG5yqTh?S8EH%15!^>PU=ld|26u7EvFVuhujChcKwc97O#?QekU{xaSg5tE-I=m0231UEohMF_#x$somq#o7)#t0<|VW=0y7z{L!!ajGBp3Syu4@k@e>0Hm_g1!A$h3I1E-f23Q$)FwSiKJLk3&pQbypuL)>4;gr&6=rseMXE*kIzd%^Ao`Y^o#}9zHyFg1bHMrQCmH)PZ;$@@(4J`FG_F@4|&QQanKXIN|vX^kguV#{x{L3-ULvu!V-iX@1$TbLLg7-q#`&GMvyqcmjsTxe0zqm5%hJ0Z%;wS{pkfLrV5HNb3Hi`l0=BbtYxU1ze4}@6+}fP>b`dZxvSCloTO?8$Rl|QqI_1_CL&FZWgLek8RnZ5u`KYf2)>Gk9O&7zcnpM0znBzQp#_3Hc_vf3rXea*;@RlU`zjb!=Y>T??Q$}N9x&`P*^tWe11|3{>e}tfidLqU2P4{=b9UE1xcBjJTlDvw<#wAlE%@yA%$OS$4FCv90&1ZbQB(tGe6Pk|-EIAVi1VbS=TbhkgxOeSfD#6~LfZu?JBs_*V6k6x^k#cfY!a=*`ZLuTbl27aiPG_Y#ry_(*@mFotF_%2E%atfXCrv1$D1eT><>FX5HsUkIqVGk&m;GNvZ&tI(H<4I7j6uPpUs!~rsVOnO{pQVl1MdKM=WG5$0;jvh$<8kmPOGxSuHs#l`X?@bWP?BoHIlU63F&J^`zE+dD#)2p2?@S?if|7D@H5$3wS40i53}jf}o74&hAoZv%bAMol`Os&6HHaSpvhk4{~WDu0h?YNtBAG+1FM(eA&}{M)gSPQhAV0!<=jmg6g3?LC0A&Qa?$cmSZ=6Au9G-KG&s+ZlxKmP3oIs?M&|tl~Sm39TqXios#`HLcT95Y{I_ql2^m2%Onf;2o?iJg)=oUBwk*;I2Or*kg=X%IWt6=s?(}$->9#2XNS+gDdpP%-t?@n>$OS(BPAlu>!E6kvnkB9@-i0A^Cji8wX@S<bThH7NgW<Ru|Ih(v*HenUQ&kKcybR+jGLIb9G%eK*D2o)@K($Wn_!`($Qo4F2~l?)+ZCNo8@n7Dr&%4Tt8_(!R~0XAS)Z+d#B(m@dUR6I4bOD88ddeLa+>c~qX%Y6P0Y-AcQ`EHp!k>bY`1sRF<K!+yDPJ$-uA5&1`+rR(2qGlS%DpaeGU92=Oi%n??W=Q@=N-*7yhpf=L6KZ%Vk{$Ova?weo-MkNp}#KXWY59mFyt8){M3#sN3^!Oge0o&281*Q7w7sU4|0w*6PR2A{kXVO6J3Q*1I%X*2M*?S7xJ4Kkkuts^ZH*?F&6VFK1aX#YH%jL3~c&pxJclv*Dq6N_(c$5yi0xSoN2@nNHb`@YX@R3Nxn+flarKip%#O-d_3Qk8e72_-XplpbVJls_wx&xPRc2`?OQ|=K3VU2krq$a*@<ED7w>a`$v4P48ubZHgr}1`xy5(Smv3;IZ%aOP{yqW0z<&HuxEAYxo?|&h#)|JwKCni1i-@}TczP}6lBqOXmUr2;Gi<9bLO8X3-+?<Xk`|bAw<{r@%j!zJdW39fpk_*1(UmrC3OZxEOnIWCF+#xfIeOKWhZPtD~3nth%46@jVmAQEVJ&zKcY@*Ygxqnc%M(hbrjwWvoR?mzRhUSNoH`LLHj^5iOJc5G?ly~EqyamwiBK8(yL^>kf^HUn?Qsm*S12JL++A&&;>q~<j)K_$!W+I@381-xQ?<_5Dzhg&+@zR_S5UXUrM;Zdw%TpK3!bB|KuNf&wGD;xHubLz5np~Z|7&1mp&=;?RMk!>7Qp8r<eXWJD;uQqeT$KcGo%bNC!GmM_$KO_HEFlEpd@kIhl|oe7$2S1$R>6F%4Cek>SPlT1pp;g7FQPR2trq79{Sr+ECLp*vMdqw|l>#H~!SbH}ffr;#sl^^Bf_<=lh_o)u=)Ky(efGUcNs4ct*(h-uT^m_3`Zd&Dn+Z`TgnT8G;fzv2wKBs1a66(k`K0ukt9)OycD~LYT+3kKSlK%aNs~E4}*1`zv~FP-kAU%)Dgug_?O;h(v@TQ?#gw_T|~fv)5Oo)7Gj^LL?PBt1KK&<75=X+WE~=U=BLx_y$@{f;{j{KtFT4yJcP)&XaZM%-sejZ~3SKe;MsY9+&j^r-umBkQf{;kIa)SIN$#B?CRpfYkPm4aS(??(Q^H^bWg)!*Yt!9eEapkUK83)`|)N>LdMGi1XeSj)~og*3@3j3S!1gZcnBuJGLP28C1^^c3rc!B6(`{$iL#;sqih`mXHu2fJ`Ogtadp@6V=eWJ>B}OS5U|w&^(65TzLF%1@;Xeqifr@Q5IJ<d{r1B@&)(R3Yxqao2#n^zG%Rt=8NEm{49G73eEzQ1Nv-xciIY^1dGYSmX{|POHXrf^uB|DV@!3B=6Fr{2A&DW&XLrr|5u3@H*<D&RWt;V|yWCXSf=G?TvbaQd`Kiy}2GmBQjzDD;mz|Y3Ey}8hB)9~VMX}vI`Ys`pWN{r$9c*D*-j|cvL!gy;?W54@M1M?^yI6RbJRd;KdT(Xk%GP^{crO}jq+3JiV<cS1^MkZp!Ti2DvKZ4<kWOeV#=cn=qXCS4-%y(xo79PMgQz=$8wK-~h!+T1rJNp1I!nNutn;L3iRb<vfwu_n*p7F5b8iw|U&|D!AD@3xY01>sSbIx<?%{O^G0sn!N4C0Sf2Li094(Oo{p#|~TX-M5Xt5-tv2VW$Nb`M-4($O+?CW3^=R;O}^e|=B3xK}}vuvj(Ppne&PfRh6#yb^x?v;wC@p2aI)M|T`Djap2M_Gmx)xX##*lEzJHaIhtFOd{YGJRiltdP;?X-lbYCQI7+L!?uOBCc?10h~k}0y_a)UaJA$Ww~gw;mMLA?_b=-P=|`hk;Fqd5>g%*P^_jJ>0jjd75x!6-Z&TvCQp+0ZIE3)j3%Ti^AQML%<9Cj@Z8W>yZJ9$f7IGpMGvFzOfd3YtJ*Y?6;yCLr%zgmtoR+Y@<@;pR(o4V0;*~49Cayk+xNL+bf&w}J-5z86l$XZUf6MnwSiNg;KQjCZ?c*%Ge`5K%BY{=O}NRlf=Qh*|Mf;2c7&0#RB)oUfOJwLcrUClAL&ft7UzW?w4~v3gYV9kDWv)XMFpIWXb-sVYB_<c)$JwwX@en{|8T_<>Oh}#@qvbhH6jTC;J6o3wB`a9$H>v2e1z^rBoM^oA)p!}hn6IXGn(t9Nzu2calnQm`pJ`OFVt-a_{9OtIvO~oOLHp)Q^_`Bo2cvUNHkSOQrt9IWJn}24TtbU-1}3JNep1or>**gO7lu)<`Y;L)s9@Uj~Z6empx!Xs2L(kPXs{?<*CQ(ZonfX%JS<p(nO$TSSuY9fDohN?9d8CRT`9gRJppPnc3=<;EZSC_=d?2@;5^Uy_{wlmi09yCTvUs+V10Pn=lPgVKCurRU`?7UPOCWu!yd4L;~Hx`AXe*oUiL5g_wHum<}YH*2$vjf>cuRpOwoj-Ahema+HwL$4NNlF>{Y7F?d-fHzK9T(oMHpxrN0Gfc+NB0Ro{+6Go?gOVPxb7pNK%eiap0(0ai3<wGOXF>V(8o4sIrO?Pb<ZS3yD-NEhxYBZvT^FzA}fb2!GFgPAEUhOV`wFy#UUC{ZkG60o+C(wA|`vSng*A|rbmX`CgCO3z^5}Bvb{qQbH<H>)Krj(R=kp|KT8Im#L3d)Nj_XkTbP_*+_C{84zRj0&$G;y||bq9W54<<?UV;PAP!<-t>H86=aX%?<qri7L74t@kLYgp!WNEY;P7Uh{!R8UJbft*I^ZpvCw4f(%e+cznRy|Ba2NV@IKbb{eTg&oj!?jyxNY^xbz#?lFkRP4UoN&bx%Yrp-JzV)(<J6xi}6?c$j)WH*~(Yw_HP)XQEY92mM)UABg!*%q#47t+z!kS06-c|?emwx-8ETE@nFY}k3Ru@<(vUW>n5Q-(&Dq3K}<+WA3BLjE8Tc>ia4!AFICeHTHn|wyv60iEn5q9$lboJBoH~NSotqFuxly5wA^#&2GF`plskz|-O!5$2O72rJ5LVKEmbRz+7>dmwMPWn`u2RLm=8fPZKZm&@S<3B{AE(v!3A<C2~_L6xx4M?wRJw_f}>dU#CC20*zD*9ne54||>_ncDc#iLsB2*+l6@wiqzMt(MpL-vjz2T$VBlX!e!PU4tnWFS9@g9B+0(DR6zF#HF8M?#{+C5w&*KnROdze!3i5To%yuH53ObM!=~2f7?mB;zM6xuj4Cfr`G<R^H(=`f<#;QeNleP|@2-o8OMwID*9|q7cFpc6*#HIhVH>qXK{-P>5Z)TIFm`uAWzf7kYEu|Ln;57|s}OwwVEsjfYYu<M-Q&<BFQpA<($Z-QLRZ>$Qr?vY%UfbK@Pmq)9{ch<XQ`rcgVME(TMgKm-G9b*IcQnz7u5Fx!wUh6!`TFbm`BJj`m=-%=Spn1-sJlPew66}HVpVIhL#xykW>ov*q_pzlE-%AHZvOS>yOqi(_JXG4+!Y}0jtSTg66vTUdak(yG2wz<X^c7vNKvX{Sbp0lGLUW??eBt$U{3I{sqYw3#@($O3|j&*LA4{x~4G#HQpwwMeT^oi!<EZzR$K*_h!zHfzHzJ;)$z~xr)s3<PR{=;jvT5aXn9~NXOMib6Gp`|aTsEVp!bj-2DF>j4St~Q*L&Ji(G%BJ~5^VNLFM=hg-j2Y7hsueHL9|W;wmx0|4lszKV1B<4cC$zQ3!BR$|bpsUC_;>3HhlXFpY%y6`IOQ0Y=twlh1i3|I-o$aH_5@g|5ZfLJVMy^HQ`DiZ1)S-VqBOpxi9=g?;XPY%*RTQ8Wy<hdug!t-5E%%x9ZZO8s6#Yhd#{<TQjAK}y`Z^<WZbcw;z)z+BcS_n97J;(d$f@g(J`$5I|)UyDeUo{SDL961(r$ut6D9w0g^pdu?31lOOLB2Ak+2Q@BfVQvsd-$jZ@!QuaWgnKU)LW)5i(dI94e|q75K01R1#WzBa##l$4;}nna>Ua_&S3HTAweSuOu)bt{K=z7;kp=&8?iw{}aNa=jiX8*4h8cZl9nPdwdEJKszF0jGU_x8BNnhxed@WVzHNgY(o(QGwp#r)jX9$>~5o-%ZLAHQ;c9CeBP22B!&z7+Ox2HY_=6x^*;l&-u}YKBUDvG)}?rp;FnfaZ-j~aYABLJ0UURY*$jXr999U>QddBQx>#!^C^oFpR&LTlY;M~NsrrsDlj^zkG^!x5i3q}QK9LEJ}LUoUE#Os%$j7r2K?5j7PMWs&^mWMg#00k{7GgGkM%-&3(cE8e3nK3;fGNd@R>D7oHXNuFVYbiGL!77Gs&8?CAh4Gpk=L9SS~n-4aS{0&=%=~Y?4J)9Pk^s^<y5DvwsLQ(;!93A3BGr)nMaZi<4rX-~=3Vlw8w7oZ!3%v#52e_3N}6{Wa&&SR1;<w-ptt;%&Y4hEp&$Cll}qYa-aXK!CL;%g!R8w=Ed-LO(7N2++R3ElTPC!Zy;&RB%7U0!;(AB!oQsQWD(O1Ob~HpeFFgZNVS6;17OvaaJ4C-If-&ym6IWZv}y0Llh8c4@eR0jYfOEjp!SxY7O2e*h5gVd4JjOb_ONXwDs1DMtW8Oe-HSX&m@gTrTYM#{o&JKX7gMI`FJ)oQf#1{RN=)iIMXK~PPRl=U?<7lLQ@p@q@WJaNwJsGelrS($@Mkdsz5l|c1vHf8h)h}tcyLGhhTD`0LvZ?M36ba9<^W9GwmO%Fe(OUSX+Fzl@Lhi67x!n^<qg)b%R@<(Mn2QF!|zt6X!q|O1!LE>A4b57N4yVwdG)I^e(mUe-ZdSAoL4^N*bD!k1FL<$8BUGnN1i7>0NFwPbP^-aeQzaau^t;U0HKBYS0<V_(ZHbXrgWxKe+3KbYl=fy%gynG!_pg+>g5-{=U#2Y0hPWAJ|rv8chL1*V)qV0SJJ`p)QcA|FAyN0_XG!#(_uQkaQ_|xRdh0K3D;IDRRj5sZ1<U&wx_*e~FG?Z1{NCa)xpDwD*saG%TH#rHJO6J;dSS7gPp}V8vhvk^!GPT6^CX)~YP61S4E9k4Yk>SKi_E>}U{+6g$L0pmvj?f%{rGuNL;$7;~H0Dkb8sz`LKcBi(waTeH>5`n7n$+{TpD<~=j!R3sXJr1}jh5<YJRR$;#7;z<b0yAW7I&?}#cKU?R;+G3svyXOBcbOA-+eW0nt9ZC$$ggouy(RUzKkSKM4MP;fJI!j#a$0jaL8tTqA!vZ%&4{n1GmJGu+i6ge#_9tf<8S-n6&$_U28@q~l(L-79;SPIo;`dFWRYk$xQE(33L2njOU7f4-qq-6p^ZVlDm_^j287EMvUhJ#isN|0Exo`G)JQI2`O#0G4CVrPQ#-r4k^Lf#qkM8OrmQ}LZq8eOhu<-KDGW4<>c!ML*v9HelIkeqUy6y}}*6eu#BW)Z`Rw?f3qUj-J!$PcN#a0_tvzB2xk8)x~duP}T<dY+WflyZ{0SqbRRn%cz8A(^E%uv2=4Io*1g*|8Zax1j0%8<0G#IcnQKr8#hrwjUdxeUjAw1{4<k7QNERJbnyt?buHkk{U-{a(&!yC}aGF=+$No**@wn;f4mV%e;eZU?VTrGjf^OW1n}&WT&zufmO3aLs}&$n(_U5@ipO`8343%c0^*7t)5hfr3*T)t)3Pk}^Yf4%mwCj^aof^4~-gSn=Ig<&_cwqx7Ti83@NoI>{Uz{dDVoBW7&<k(Ktx;#KR+|1}x&)7t(na>oU7+0DF$n*XqhU-c7l!l=H1s2|DwJkel}q;M5jKdEJf^z&Lgb>LR+fyr2XaWEdKD#<FPWzabG4X#;ElJ+29ua~~Q!O_cRLFf3ysl?Z}dr<n`xP*2Ahe%l2UE6g%lKsT<4n57n`$;r~GmiF#?Oahk=#O&=-<+9j!djs8ppQuSpqrRh(9I;c^+34Rgw)aXI+Q@V0YJP~LkYuA<NVq&nI1l}%s>78>Z#4w#nH!+?J8a0B(A;t_{vrsHV$<FpEV3qZ9_Ih^_`YJ-bie@C^EOOW!vSrZY3~LJDuN9pzUrhX($2WztI99?}1xZ%^SfHNDI`s4g7DCIAV7>X++s0aT3~`XGzd`I<aL)ok;dnsV<ftf4dCVb3_%H0q}2PsWr0gZn^L@3~!C_O371M!U|9~PRf$t9woC#HLNnkPyN-Sy+{IEEClJLOV#*7#S$Uymvk3V;)l9AOrB&Y4o|zQ8HIIvjEERj3?DkNKLc-f+l8OJ^sH;usBo~`-G`m;$`<!&VR3DlM|OAXRoUBG6X9`7xuO{v^Q};AsgF{JD=HL9Fw|uPtxK&L6V)&Y9>l8VOgn8$DDA~2B^AdPD`q0AgAy?yxil1E0Yqvsg3dJv#4^SAnsC|SEDvdR!_g*(2;UMRip&|EmbfNB%0!^+Xi78JsXth|Jjhox2b)%JvKm(}m6W{pc|Z!QC0}#Wdvn%MIN)PTf**#s4IH;C@ZAQ@Gz3082txw$E(OvcV5;KrHc$}3B;q>mf&G7|qCTXM2b?X0?F{V6X&-W;lCLr`3W{R`1!_ysIKrDqRNZ1@`k?a;SbZ=#2;OqT-vm3HN2*igy(P^~LU~Icvy$7}jBj&EB9M%0q(I5ufz1%G_5tI7BnE^EQK?9d>}lny-KXDJjC_B({-!U_{r>bDy8jNaqpxIxE}>V_BGRuRN~nB4K`b980K(aX;6UI>i!Cjs?5-Y`WC7t|nt)$`MW}8B0z>?_2z(BjSTb5dn8wu$g8?f}jZ^7ekj|Sk(!j^K-!q&v*HIjkR*QyFjw*a9Fp@vAaT+bzPU}`K`vn<_AhWw{MZrhh$2}1C#>V9a10|nb4x0M*oL23Zge<QOEl0$43X+%eA2bAMw&4P)x1`a=RtmK<Bdvf`Z(<&za!Yfbrp?C*d$L2<zw0Yuc>|1}l1UwJEFn4=8Ob$YU7|1Vm8}e_eH4eq#jXe-CAioXF`)>71>SuBUz{&6^<?Ou-sRn%P8_UQmC{!4ZeX5-%_biw3NGK<g*jI$Ilf<Rfo#=nD_*`|)2i&ZDURxpN?{qPTMDqJa(}U06!Q7ig+*q=975ZsZ5?@^7^)(6SuEOM-$H_$zDVVm)TOv|r6a#3*g|;%@AsY&jt!c<-E1zBrj|C0pA9Kk>2wWCkUpBhnw(}@t-zU<Mlkj`Q0Un2&OYH_#=nLaXQyxeWh>$Hk{LA9^w0^(tK4aU6knaa`*3cZ{{8Cxr;88&bN0r%`fzqZzb@o7%s<*aOSTTaS2~CxVK&wX1{v=qR*<(l&m}@dl$Z_)KGN%hsnV8Kae9nqjB@RFE$3p6U`chV=bKL+E9Kl<8H_$?^Szj+PGJz40=`qUfmsYcUwnG|;p3TKz(q(EbT`YZ`?%)m$B&=>;zJH{zh86Rw!2RIMD^+aVMm=D4P42XkHdTUNTq%K<-2rp`QiLsZ8SVLMIUOiaM9y^{BU_C$+x(hICFN|pmGx)TM|e80W?o;_lbn{#Rn3Wk2aQr3QdF$(+J7`%KrAf=;QM0^!&}~#T&n0IRjQX_EnzsDo%KnC%bCrxdx!)Dz3{UjA|*?yNYLKWl%WsLxj3(RIy!S6i2sY=kBjsrhO2iaSQi2bheSDu#M>G#tmO4X>C_1GMIHwe93`6D#wuA{D)sbmiU)Qav?MvAyY$y)4D#-eiaFWetYmBtRM)5^%iF*D7+{qF=vv0%CaJcQI>H@g%aJZBa@2)I70vkxJob8=@t&FaxCWEO2^&m5=&7XVbxE1z53h7{kBi|J#eUR|4BYVBLp^Ry-;RZPHV0na(+z(^`yq|E$h)&HWP=%p#<9EFGJ)fhVk&ab3GoPoV44=;q&M17wzYhR%bMBhrzSwtry3KaCQ|+boJO1|2>73s4@MMqZWyT)<9-QCLlDQuAPX3ja0LtfrQ?S5GoEF;XAtk?e4el-%FXQ_i+e?%;BF}paQj9>}T$<MV*~xGl!q5WqQ&2m9oM2vL)8PXtyY8F9v()<oossVFvT1Uy!XKyUI<w3}rFPQFsme3Z-&l;L$naQnup6pot;)TWrccxEiO!%gau_NBER8Nz7FAAU_yISNjP8u=miT{@t+50jPd)25nG&+(Y#JUD6q_r}MyOqor(3TIczj$2R)yqlP6_5AS`V=-xwLH;;Z@hAB?D5L|w{)zU+-SzJGGRsB@+l*9WxzR~W6L2))||3NE#Bfb1@yNzG(_rar1o;jH+=fusyN`B*$lhEjW`*iwGyK$Y2SD8u6<3rk_!sJ6f&-QJ;FW54#cuxz{MdUyb&7DLo6XN{DL&gNF^Yq?Jyfn#0u7#^OOnryPZkE+t98AHHpPS+BiY!UH`9CCc{$+DHw{hG`f@Ol7%)2mEFgCSu{kM>8FQ<8^nn$<__oUV0dvNWyWZc=fBe&T>!Qn|u9pVJGV_!sb8yDps;bi#Hb1G*8x@LB8650^)Wwr$DQ&L`SRh^$X|6`nz(y%9iFyH>HPwm?WcsGYIV9`%EK2O7xk&%oM-h8<Hn_ZOA41N6QmH4e2QR4tdaTrFoM=$%Jq2d}muep`YUw9~)A0N-Jl#)p`ONM-C+UIZPG!r-X=~n>`A8R39pSBWgLXy|Qxl5QthgPIO8z0DTBF=qChM2xAbr0C`r3SfnXOY+)ilehJedt7G(I$hNjEu@@?Qo^TcX@P<^dEXK1J=6I-u$Wla|=;0T_hQf*=37hnaxPYsUF>(cl%DHOy~=yHU26`YDz{iZU2=pjxOHf<gL)nz6v{$oc+DXiLEl=Rynryli@`Zq1y!r4wA}XwmT?AL@7wVHxm8lsfLwM2D<e3;<2or#R=q4(sej7q%L(_)vup6E028X%I4VDU^ksb0#aFy4ZQ+L(Y^TdFdwC(km&Y-sZ<Ua{zBx|{AmDyu6F2T2!2$ITE0M@2a<d5P3{r3V^gydMtxIEr3|wIGe~ad3pF{2YUz(<>`|gimEL#A*Z0e3`2$Hca)z&?1biPP+&<qtMFk7@2Tix2scmLD0Llxe9Hs_%s^nNybusu;bqOk7ni?T!OT~1v1tn)FizBB3Tb=AYPBC%J;xV-|0NvyPsWCToua&HY$tv9jt(e>HAxi#Pnb%%+AoK$aUYcLv4Byw|77FEFw)FjnXnz}r;=jUbHhJKuCDHJ*KNW%&&XX)~2;?x$%H)9`xzH-(Rr}G4R{njn9S7UfntKiTk^y^%MRl#roU@{bmG0SmgJbO)NFXa;`_Z(IjR~J;JS=C-oFLS^?R?{al|dsfoA~PxB+|>V-GE2g@8pALPot*V=6eJ7oxknF*yF<6<G!f6E@%`na!|2bCHhjtcYkp&dGs0r$2+DCS^r1gDcfNFx0}MWyBU;!am9JmW*->9WsCfGxRYElJqdG5(Jc1(J~hPE3yip^I{u*OhhxC(PRsUm!>Nu{xY=20u=0@YO-3A11QM0LeeX#SjUPeeI<%&ls^U!+;u-jlxtb-_TDowIGR`u0zky629@Zow(MYMK3fxQY2M4kF2#(khP&;cz1uO;F4q>{WGE#&&D&m_;|D_Ebr;QV1lK8vxO>V$+drN)d>3@}hc7N~p*B+A984|asX|5I9Y)pmKa_6f?oKct$eD36lB$V9W%Z+gK+kM(;Rx4HpbPrZb-C(nk2K0MxgB6Y@>|H3d(nB@%&`S5z)IGaT+FtvZ0IuKGvmJYJDn>s>6ROn5^-b=>PwfE4=TdSu+virk^@l}`RZ^JzOtTUKBM~3R`h2|R6b*<zyjb?r%*ie+bIm}hoCCznS<yKlBTQZdjvDa0Bqi|c+?TvOOC+jQan)>JK!$JD-Ta3Z4VsWab2s0yXj-_16W1Qf9ff>6#M-%t0RJY$1qo60a)TQHR!bhxH+ff5{P^V+)JR%xn`k_H`#@~qUKKY*`Y9S#kW?wxw;-6OUEOQnCv!vST&7zpJVo8g9S}ABswGYCeAJyM6W+XQ=+?4OE(cIH?yh@#K|2zbz{_XR_y)Ov{`Q@A^a%^Yf0%L{iW^Ca!ZjIha;89Ez;);8*ET1S)kG`@>{;>PrTg7FCHWBJ>b`k^*etehPPw$?C?jB|EgqC_RrDn}u(ipo1rAY>hRnyEs5=hVBC2~$3!U8YA0glwHw~^#mmJi+ABP+lXHMl<F@n@M;VqaaL|S~%wp{q`&K)WGjyI~SCdqKM0701>478$wSgGkp=tL+N$7tYfAXKKA@3*@3OI^(Uar9=6N8Qb<8M1OZalWsI`XzKsQ$~~c`LGWl9nreq{Mb2Bgb)z+Mw7bl5qC#(d7)@gk=C^gQ{aqKQONyY&H^HUb1L|>%1QJ3)7-d%3$7omYm!yD){lIdd;lAclSR$~L3*Qh36F@sy@$igrR!2og4zRP6xC$XL*`cRA?u3KQV`5O6K6laYe&xv`CP(m|7I^QpJNAR{*C_KcCpJo?%=(|pZbNu)_d4xUS4Ck&t*<u^#WCQy}k&fBFMs5iPZA2e<e(YllwI}S4z3Zy)%v5z-Wfw3Y}KAa=WV^l)aTl#`%T(pzILGR>_nqn(S`;{I|;SC)DZ*I3~wTC%`PDd;Br#h0cIMN??;y@XE9^&ZaObOSjC7XqapZlOn+>5yRJ?{`~y$?CR{n6p6<F1!H~eCj', 'offset': (1.45, 0.4, 0.072), 'seat': 'WholeChamferedEquipmentCourtFloor', 'rotation_z': 0.0}]
floor='WholeChamferedEquipmentCourtFloor';plate(floor,[(-3.05,-1.50),(3.18,-1.50),(3.40,-1.28),(3.40,1.43),(3.18,1.65),(-3.03,1.65),(-3.25,1.43),(-3.25,-1.30)],0,.080,'z',0,'Whole broad chamfered common floor with empty front approach and separate implement areas');FEET=[floor]
pad='WholeShallowRaisedMowerPad';box(pad,(-3.07,-.560,.060),(-.540,1.160,.200),2,'Whole shallow left pad under complete mower original; no engineered platform rating');LINKS.append((pad,floor,[(-1.8,.30,.070)]))
rear='WholeLowRearBoundaryCurb';box(rear,(-3.15,1.470,.060),(3.10,1.570,.190),1,'Whole low rear boundary curb, not a protective barrier');LINKS.append((rear,floor,[(0,1.52,.070)]))
left='WholeLowLeftBoundaryCurb';box(left,(-3.170,-.570,.060),(-3.090,1.520,.190),1,'Whole low short left return curb outside the complete mower pad');LINKS.append((left,floor,[(-3.13,.4,.070)]));LINKS.append((left,rear,[(-3.13,1.49,.13)]))
REUSED_ASSETS=[]
for row in COMPONENT_SOURCES:
 raw=zlib.decompress(base64.b85decode(row['encoded']));assert hashlib.sha256(raw).hexdigest()==row['sha256'];E={'__file__':str(OUT/(row['label']+'-embedded-original.py'))};exec(raw.decode().split('# BLENDER'+' PHASE')[0],E)
 prefix=row['label']+'__';off=row['offset'];angle=row.get('rotation_z',0.0);co,si=math.cos(angle),math.sin(angle);rot=lambda p:(co*p[0]-si*p[1],si*p[0]+co*p[1],p[2]);trans=lambda p:add(rot(p),off);mi=len(PALETTE)
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
 REUSED_ASSETS.append(dict(id=E['ASSET'],source_sha256=row['sha256'],unchanged_scale=True,unchanged_material_parameters=True,offset_m=off,rotation_z_radians=angle,new_model_count=0))
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
FOCUS=(0,0,.80);ORTHO=7.5;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(5,-10,7.5),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
