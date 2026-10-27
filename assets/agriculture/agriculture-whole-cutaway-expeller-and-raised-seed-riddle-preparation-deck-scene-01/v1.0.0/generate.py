"""Whole purposeful farm preparation scene; two existing models reused exactly, zero new stand-alone models."""
import math,json,hashlib,sys,time,collections,itertools,base64,zlib
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='agriculture-whole-cutaway-expeller-and-raised-seed-riddle-preparation-deck-scene-01';VERSION='1.0.0';TITLE='Whole Cutaway Expeller and Raised Seed Riddle Preparation Deck'
DESCRIPTION='One new whole empty mixed seed-equipment preparation deck, zero new models and one scene. The complete accepted corrected cutaway horizontal screw oil expeller occupies the lower front-left floor, exposing its full worm, true open hopper, side drive and empty collector. The complete accepted suspended seed-riddle frame stands separately on a broad raised rear-right deck, turned by one exact quarter turn so its full pull handle points outward to the right; its two skids, four uprights, all hangers, perforated tray and lower pan remain intact. A whole two-level side approach step and low rear boundary make a staggered two-height layout with a wide open foreground, rather than the older same-floor side-by-side winnower/riddle cleaning workbay. The new floor/deck/steps are scene-only architecture, not separate model deliveries. Both entire originals retain original metre scale, geometry topology and constant opaque PBR; only whole rigid placement is applied. Source is embedded and hash-pinned. Scene normals are recalculated and GLB bytes are not claimed identical to source archives. No crop, oil, person, sacks, loose tools or process connection is supplied; the two machines are independent parked objects, not an operating production train. No extraction, screening, material transfer, machine compatibility, ergonomics, navigation, access safety, platform load, food contact, engineering or safety claim. Rigging animation physics and interaction not made.'
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];INSIDE_TESTS=[]
PALETTE=[('MatteWholePreparationFloor',(.28,.29,.25,1),.97,0),('MutedRearBoundaryAndSteps',(.24,.29,.23,1),.93,0),('WarmWholeRaisedRiddleDeck',(.42,.36,.26,1),.95,0)]
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


COMPONENT_SOURCES=[{'label': 'Expeller', 'sha256': '95ef56d0f2d2729c37e9f0200b277262023b46ca916ee43bdf76345330bfb77f', 'encoded': 'c-p;vdvn^#vhV+V3Z1=cmryKZz|TOm>Nt**mD*WO%J$li!=)$z0+a{|O9I<T<-6bhb<gMpILW>H-c-e)(L8$kHQhZu!(aaLmyby>4<au#9u{%v8?)fipBj^O<~?{%#v)FFuW^*o>vWR%4@Mk>E&p-lhoPSsK^U&nEb+1+j`~KL(U*zgC7BUN;gj>1zx<^UELSl-FTHGGe@^4bUU=yu490f)l-gOa^zBJZT}{wKY6qF0WN{p(jad>ejTN<`x`yiH6FoL=?=EicT(orXr)l*+{(0x(RdY0&1))D0Sx(}oak!zE&dN*tC~I8Y-d^3grZ-Q5$vVu|iQnRRw$waZV=qbku;oS5Rx#xkPq|f|a;x1j`~SGQxqbif+BG{)+i9EqyZ3h=u3YmiWA0L6?lt#lP>;s%1rl!=i64W|xKcfujW<`fmpAV}-Eo&6Bj1Sphw#bp))|39J?^5*HZfXh_C(c|-eeI(zGGY%lX$rb{fwH%>!dY{;|wGsc<?`ah>i7XMMO-zAWV&v9)M)en61Om2>lsREzaV^@E?gPL7dpeG)S``nq<b@_mXk^Xjj-{;ZYNG9mdhzAf{Sm#)>GB8k2>$9Q%o5+%0?~h%%xGk=qMtlJUxqXj(+>DAV<5#8sU7DRGf+pl;$DnMa@!y%L@UPyQju7CbeYC{>Eq@j5lKMKJkdEc`H-5KOZWP^7jIQL7|~=G13GQ```nafMar5i~%SAQ|B3v1oFPpU-g+p<{qf=%jB+yq+(pn<))L@KP5Fm3ji`hDMVKCxk3x;e|6pn2ZWC4_yYChIg_~HXt;iq^~L9MbSE>mV(HI?+M*fLV2c!FyeIvh$6yPL2Y#FM^j9SJMx#S>`8ba4W{5BkvPHxiS84DlTwSZAI1+n%X|_MGsz^0)0{n0$GDD-IGhR%Y=t9RSjDCpreFN5#bmc>%y`;bl9B+{Cvg(B(uF9FrJpX0AXSp>Pk||V6viiVl2TbuGNwV!U<$6ohd5atVkWI=5^Vg#Vmfg$_oCn{t0VLds$)igHzzrXz{YP0po)_exa*bRnsi41L=&h)L~#AY#tdkpvl!H#w#M;8NHisSV0w-LsTB@d#>5rIS3ilVbK-5nnAQjckr$Qu-|(mFiKo7^+7!MKex<r32w^NFBSb~iPWX2cdZhcNsGsQex!_;MUXp5ku?n)uf*EHL5+8cegyf2JVo7yxd{Ng-*&wuy)c2=^j*0ihx50QB2s{ftQr1R@>Z|wxMT|C5r8ZPV;;{}#Ytp%%d|xH;1PWkAyk$dhz{Rs5qwjHYzowQ+oT<7>tXAtx7>A{rIwcUE<^f@nn9PgTGb&mqj3hszb<6kh0JNmu%qK=?+&IQfFrRZR;)tbi1h4??D^MB9OK<8sX5*dv?R)>j`|H2ox`Sc=^5ga0#pNA;e|PbTKVN^mx#BNxuV^Kq&-d52@84XF?yhdRV&l`rhpW50D|gT||5y``yi0sP`X_ke7E1Rbn!W+MUV5o-+D)hP(ssJ|-?2NE?VPu5r*mrAP4jZ$C6m|-|A0hMtGA@_K6%p=joK$Cw$nbNy6w|0w>#r5(C!V%`tK}_vhq;VOD!3<neT__;P~8jPCB-8e9Em)>Fd!MTL05amRGEHr@TZ_>)(l3+~$lb9TRwGGU5@9cy0|FQ-5Z7(`nPQ$5xMY+BzYHu_hhVd^~`@NsLFEm_9PT1}m;)ag%gC-qob_Oq1n0q^Gpr<V7k?(7=<L(>SYip01Zv@0qSyyOo<Xy+LRAVm#;$TOR$PZ=Ip7zO_--mbbS0)<IcE-b$Ad>8GZbg8<XVN$-=aDZqJZ<aHEe<!U^~&Y@~8b^ImOi6D3zduCHlc0&AQ^%};;9S9akXrgJ81kB5tkCy$?%2Bf7uPc1r4Er<P;GT=`Q9K(`M{&4b`YsR!_%?%kn#j-=yx=LIC;mL>42PC=cxn{w`D=i$q*>;Evtx&TL?g61Gyx-+sor0;d-?E*PnwvxjB1qu=_@!|^4TEOIQLVxWE?t|G*c4ZCR3{h0~Kl7-rM(sPH%W{Kj?J`-oBTnKJ1z>Y(}ozVJ*O&51L~l#t>!bg1fb$pXIef#^^F_T2$r%Ak~k+_glwrz2vUiuUw+bE6iJI0E^2p9+N&uX91C#__ah2qeLZJQJ6a>w7nbPdFW1q3DJX>Ey4sbfQL_J1JZe3=xTm&nJJiI*v1)Qb!~=myh_0;kqhAX5j@)8FtPdB9?<hPX@r=OMRS)o&AbPY_C<6M)G1GuiJ4INr6{blB1pCy^**~zVl3-#QGe!mq`Ziin_n=1jlZAm=9dE=u=o~$wUp2hQX1+XiwkMakXT?9hff%9lDM>Lji(;?!=Ch-xd>Y?niDO$R;!tdF_-H)#KF_l4aw+j7W3i0iLJ==g4PF<1D%C7z!)#kSB)>x(8eF;PX59SO2R?II12eq8uej8Zj6D!=!Ny$k;dF->CBIaPhf`dYrLdkCN4b;KDS6&;Y;%~kgB^FqD}y1$50Hsp#U;gpOc~W$|a8ObbHE__EifndTN4`b<4GCu~DC2hSqOxi<>ftYkNZ=4n&qnz9#f{0x7d{)*yh;^A}!zsV<XdXjMig<mTMK?+M{R(kfmxKU@7V*%4o;o*$-ukK7lsb}m>tNl#oQNt`sz>zItq02VP>J7fWoB?9NrB=nX#7w!g%tiEC?dMms{Ce3>4kDf$2SN2oee(F?o@XwRpUJ222imwz~X^C5bsYOs%kkCPsRxA4}V-2g;fJYz7GWM1A2CH->bBrVA4J`pyZ|1;pqe%`F3W*X2kv*pW-a%x6y?;&|13RELpYb11?pc#W0?8?qcVTQVg8GV8niS?R2xBayi-7(P^O;g%hYLGW_^1loTu5uvunNPV*|xj(5p0v@v3+8n*)XHpc89(n)3>gDN@Yh}c1+*9^sPhn&+HRxSc0F`XFQc|fw3fiX-96Si#a^FylTUQ!P)_)nYq+2jb=ew#%c3`CS$#FUNUns7;US+mUgnJKG@WX+HN+kE?5&@Sy8%!0ZgiujlVDn)^_rOmyt=F%6gJ{>leWx>02A`Hyd3c4We2FSzs#!9_l3sVh2nT4c)CpqraENLS^=vwOk0Ly~iN^|0f*H3>0FN)3~l{KAMbfkS&vGXTmlFTY11=k(!AO8rw}zNzLRJrRFos49U)OQUi2q*Hqpo@k6@Jc{Mr>NR|$EamHsNy!~{rizoP%NZ;ozo?ywe6D}tJhR^W;+s#kp8&CaYq~!gvZ9jITj{^8>w|i{Q*+O;SdPE@1WVIj<$ZauLtKhJEpub)Blf+F9t8+p*=q$akP#H-fEYK(iNeL0$`$0(#u4&GB4d7!(jk=s%TZQJ~i4Dm<{Y62kAnB{rnb=?3_Sa4wMZ4(>J7f=uX-=?S_E7nH2bI-~SnDzj!)GbnX#CZ9i^!V9G(vx#vQaCRtg#|@G!GbZjHn2}m12rcgYjxVR;`vni@ny9(;+4<hRxGfl`eU@-IJj*8{^EKne0rzWf0ymJHR#m7JMIl`~2PPW9dOfn|w*9L%c|TNi&lGKOXS&0iK=q@rgxBSvu1bO323`JaN2DaT>ZZE%x@cOrwZI8R*c^uxtOppI4xu_Y6e)=mb#U!)bR<1QITk59j>cqNPKFf>@ozXQ=}kn!^#fK0&8EJy}K30cj(v@e}w1F<cqtPf+JW9L<AlJw?#}hTfS6X_l~EMZlx7-E288+YCGT{pVOQowGKBP0ugeC8)P3ufk9~sHwH(b1YDuCJ(;{xq9m7GILS_4{BN;;)mN{>c39NMXJmOaVMJ0d6y@{IDsYLoV?`Oa6y>}h=G=-B;*)#x4%9Y4E}?ubPFQ>Ku*|H7<);XkXO<462%1(1DUq2ENpme6FZy}-a1MeKt&Y1>>QU#$$?%Fz*s|T<)l=St}*Z|w^cEa!|@Z`ms9tYQGzW7HP;(h_|tc?=WwNVBSh3tiwWGOIU=NXehN8jImbsfo;%J_Wr`sJTzdPWw6hV#5*b7w6>kww<RGSm6St(1$K6ATHmJ+AYqN-BHXI&T(<yd?I3UPzzG7CTg;iqet&Y<^r`esJ!ptO1c7jk`r_f>L5IHwaIL=+)ywM?L#8afkBuFOfATw=Rf@<@Vp?Q{=%jru!HqVBtsJRI6h%}NBQvsgp0CZBkn83+N3HXx|@Vq&qKt+(6``G~yx)Y!X9_sM)qymxf<<}ZtQoSx!YJ(3tr}U?LBnmMYm*KyRV+8tdf^k(724kDYIz9n&optT6Buwp>%wK0xNb~u6AcdVmhZGE+<DX{6gS4nu1Cx?i{1#(j(0rc6Js6}*3pUS^x7fD0h~u@lcvT?)R|el4A-b&4b<7JO`Ahlw_gLLzkzG8!#l;&evU{L+mw3m7DAcY)F5~4abJA5KGUR_XWIVmK#@l%47h8Pf8$tGx^$I&ayip}#-pXFyI7FzvQL_AY8Ao3Zq0ceyPV0zYTeUD1qS;~tCmg&G?a@Bvb?=1qWTy+4l4JDkQ<~5|Yj6@Lz9P?^Oq6MJLzBITrq`r<OfkApk&Uh+O^7YTusKlL-?OVbHlPQ#U$Boc_v59XB~M$-#KQ<(2I8e^dMGRo`)TIWmrnP*QL`BN#Q}%yGWYW#KlUG8!cF_+z<GJ{BI|pub97Qz(#KQ;@Lizp0PD>0k#$J&(|G~3L3U1+<*p%w7c;F8(%UAUCj^@o<Y|*3hmlwk@jyC-DOCT?mB`d>?4}p<vLe`JzUss9y(9knT^R2z?;$I~$*yOGa%3(<KJQfuzZU!}n~Sms%}b1I#=!%ZeKBlYr7M3D%mUd4q$Re7)NTdm&Ix>^{rEkq%Or!#Y`_Au3(-|fi?Culvt$N^@eK20T`haqw(P!#*a$STc*P-eWj3g7b8mtvI@BBX6-lj!1QljHiB|zO_h$x~Y>{lrsts`BcWTLjZo|urR6_r<1D}ijupz>VVToN?UeE2^pJb*uIy>1a!F<Iyz@A(Fy<M&8oOa3uLv4ByEbgHBQ=FREBtaof0o)2Jgg`8MJZKW&2gNgaY@KtXCVickL<#H?(mFSw`mLXCB+(Au5@R5S{kp^zfkjy`_4FVnwXK2c+Sb8LWB-{T|CTSEhexg}G5%|g@n7eW{qna!E$Q)WmipwDN+d|A-L~(NwNJ>YZAx6*5@G<w5Su1y>51}`dEaFqJ@(||;CiS+L1YnC0ztfiFsp`%Rh!b*M-if;_J~qwKsii-GMa}7%$An9p|MnAfb7>Q4Wr}>Dkfj0MX|8>>HHs+O2Sfz)pMSZ6p7@uMDj#9N#Ob_yJkD_W^2JvgXfF*@hNQ0^J3lLJzpfItkY`bCyDJOsDw4ni=gk`D8}A(`m>J8Xr)i15ISxCjPcniJ_BL;YPbWuTH-Rrfy6anvA-Q#d&+{kad5mNIJ7r%f-D_H=?h8Uxq<S(l*|?0Q12J$Lv8Z!&dDY|#WsE$#_>_NSX!znKsqmnQ-PT9bFy{epiPLbpub8V*&-_sq-aYT>9k#=Y7~F{8fwesBel6jlF>&tKE!G%(VXiN#AgU#!0+pTOWH3>Rwd^sNrsZ1LOD~(QxO(eINI(JyOW^Z0$vTsa{%z?NJTg<*)pj&o#xP&@qH_P>n*<*e^Khftn0wCKGF^&TgiBQd3ILv7psWZ5ijWk`B6LtmHL%?&s#H4gYIz`J8&1t%P+je-OY0Zur2SrJU&y4^@RaLqVR5M6i(%;X0a_i<U<(~Z-tfBC-#AdPh?rt7S^x!;?Z94R!oyTrZb&za)#hRhmGKFSH)4(V_W5*sOl$e{zIC$w)D_y`|{xN@dXX=^z>qpt7kllX$NnS_h-}x{<iQj+_5@|gdeknA1i4-E=lw5vL8!0u~lENRuTzi(7*NlsbtwGeXSDUD*9ScfCWG&$Z1)H)xtrgILqRt7TI)LW~E&&wJpvTYLnD;oTE0g38y6K2AnMb<JMIzV@~TGEnR5}fjKAMo(73nRkCjdJkvTl&lXgZgqk_(ZIL!u%@wq@3=m&Q!r*wFab$t4#n~F%$BGF_cVhkO)X%*kE@+UG_D~WP^dhOoyrUsmPLw29Vq8%kV-?h#o)-aDE;u`?#3}VWD*24sdWT&~6j`W<AF>P6pNe-i3=R)|@v}Pc3g*}HR)c<Ejw(S0)mY}zm3T44>r990x)Lr%+4)InLZV|ifm6>#^|igKt1%)SVmp(l$)0Mz601`|Xn>*Se+9OwQ1C5DtP0mL55cbBh*lS=WM^!L6S2t8mV#rekfe1qBe!=uXLW`?*{7O?>tL#*bU)^@>XaFtpJY0oGikQ7?(q)-@5~z~`&k-Ty&-VRd=Lp*nEr5L&yL!H7N$Ozye#2`lO9y2b%B~>N2D^cd6KZ3LHVQS1I|Z~o9=$lY2nHtugYNu5!fyQCj$DT0$Yl9z>aVq0Zb}|9pn(0B>Nhx6H<k-q<X8A^rhi#Vvv}ezzKVdoF|>`pQ(^Z%@l4d8E0xTuR|~TB6*lnt^$`FG?x+(;`E%gN*Btu-I0LunM46kIE+{l#4);5kuueVgfW>tRg4u*KjS%=z>c5pveNYUMF@?fe{839OH|tt<z%SHSF8|@=c=apdQGcMl+%s#9Be&A_ZR`j;<3Yzq;oojDJrwn^BZ$_<v6BIAa2n^&uCC|eXc^8d0yLK#Y%RLNxgG6UbyztW|1j3ADFtTIUM$He}Dh>&J};G)m&mbcMuGVygF6YB3Jow&nxS&n|p8rS`~-nk+*F@ZVifFWpr1iW-tu<AZ(~4VopWa-C&iak`9F`^nfyMCHB`iPT14s)xC$OfvMMW0s>vu3)KjcE9-m6$sUcpG?<KZXfV$sBpC@LFyLOt5pT$=#72_6yq4v<czj1IAc@*W6KO>vDDdiv+XRz3!#wSBoGLPP3tFI0%X-!ITW9(3$TH)~b;5DwgDq04KHOvKq(;v?J&<i8^2r1LVU$kD)N)Nmi%!+YA%qFCN^QLnJcehY_PVkEt%_&9FK3$ikm<@1sB#keDv9HnX`|l}_sijv9I3V(kQyl;epH0rM{F#OsN<3Dc!c3x4s|r%e!TqiR_rzGzV<)f-2ML1?K&qX{eQl{xf<R5{{Hgs*H^c<uG2=4_44A6tDB2k_nVn5*2{5(mAltGvRh~NkweR?dGED2CP1a6wvS*MN+}E<uG%ij$YSMsZ6r~lU`%!bmy{YlkXboP$Rn-}G$)NLLml1kc!Qq!MGN^@@*)kwMZEU23`vFOyWp(VsKNZbFVi30US52-A|!k#i}v-0tLrycH^!&mFK(}p-=L0^jaN_h81#|@XNW(nGaQFf@BhIoU+twc-Yl}j_jRS$|M>lm9vjq|1AiwTf2L+m%3EzCW^A#z&D*OFSC@CB`D<0DKK53cWI&JRVLbLil`g{yVF`BUj3~64dYR|w6yVhAZI?NTzohl2xg^&ZCs15efhzVN2`H5G`LBbVv=PZUtl!j0pVG`<y5=8OcQ@}Z&E0h-Ug(d+UvN9pJq?GjuOousnwS5+B(&@Hlcx#k8YlIzeZ(6LwHM@1xt+5{r4V@VrrruW9V2c^qYFy<TNTM7h=Vk*z$n{<z?oEK=?}dpKS_I=@VS<1#`GqN$^Nels3wV*d=@7SvN}wvikxyuM>q)Nns49#>*|fUvxa+IMPRV>=6-=|KFdgxA-cNer|WmMPHMHu2#gao=FPj;7q!~d*>XhYQIyJoNHycDe|;i;ym~{LLda+KH2p}-gl1-sh-RCb9%hf5+NK~<A+abf&|SP5@Vg<kQK%zO8O23s1y1v_G9n2s!DL=+_Kv?xk`;NL!Mw@)x}x@r$?Raz(!6$YXnCSP=E-d=>}StCsM+kS%q!YvCll{PV~urd2z`!)>v-PF%O%Y3sw2dhuf1eSw3xV>EZPv5xUS|ld!m!ACk^86Jn|$ta$sbex1VVt#g;T7L7l815-;5y3NP{>I2vp9m(Dbp&18zykIR3lv=C~nsQs0@bnrNW8s~4RGbe+`{FK1SSi$3bef#DuY3h{|M5}d{4$RkH>Km8n&>WJ+o_Xsq8?pVPhAFDv0Q|^L)2*63u~N-HFvT#KY*pmBmnvR_tA)2!tK*ca+(EvVfoux@)8}o=dV_Yk!IiFjOL%}z-&GwH(l$LUDdojvMQgrKEnx^kUE#boB#9&h`yg2I+6~?k&WR=qo{$V@oyElzgQ%9$@G%JUGtxF2t6KTzhl29%NEp8~dAFChpa&+nE*k|?vY7eow<>09VwA_g=&jlMx2aw#^K28OYck1Tf6;s97kRG?Zkop$mbm#)Prp&tBZuStX@A><)LE=@rdc9n+Thbrh**u-cOtui2Ew^{XS!al(x#FxJ0-hg^u>Qlm4!%Jo#m)Meu5yt=*cBYIW_7y6J*FQ2@%;oeno<O2iDGL^@R7$ig#lVhBg)O{;WCVy6e>xPN>z7chi_5SpJZ7F?FEM>bpQg!x)pK132!545p=k#oPDjPhP@?B3gRkWCW;2I6X%ip*dcv<5FTbQDcvNKlGEu<zA>;AMi`8k8Le*e2?Z<D42r%RSw{+>Vs2dY#GkuD8;s+Za6|N&Z9dQ-NFFoeVX=wP^llub9@0`q1=&0?oPvq2WEcwcZ6LgVhCy|-}+2<4IUv;$gd8N#R4tETI!epggQ)@gy)4a1j<rftThF73$L-=FTj~B{K*$)JLu6AXJ~OcmnL4+SDYBLZwP36&(k($9-=~T%He(lmwhLoHOPyC8BTJeJNA&N9iP;*aCne<beIq199=UF<`J2eEFL8?OZQR}I|&7(^m6LYdCbfqPV`<C$C|KtYN)2wR#xu70${hzt|Ng^91ujOZri4bu`EzE9QCuQxP;aN_7wMxP{+6?_%}0Rk4trJ=55U0{_fyE0W}Iyqves=13+dJM;gZ?#;e%_uqHuDq6<DBl?I^F?*tkXejor0UF8WmZ;70r6uUL)EwOnLJdPgXB%J;?Sv+xJ-zXrpk|7-<(VZ+WvVK5<p-n4jiQ_~g8g)(_1lXo8L2C`&ff`JX&rW0{J`&Qb0bK)=M3ZJ=Sw${D0q^if@Uo?(A4dry0YR2F^9uILo<dKfbo;PMUJZK>e#g~^k@|j@zvH-Ff1!>RO>MsmzRp}6?)5wN0txKus1g-hueOf;1<}Us9MZdfnsSFLbhzdY(v&)QK{fjKY5*$nJ2;es*Himm-m2lc>RE<dtCNCCMk-J1gUu_qb5In}x3gE-t8TjoEaZt8MQjJfa>^oz5CLG?+8liX?*3|AF#S2-tiYLUPknmI7TCQ7)lZM9EJ8rmxVV19cNF+7Y%!3s3bH2$UA-YDL53D~T|C@E!r4xMfUi<O4kIu9Uh*W{OMLgopJW#$xaq@~c(~1k<K9lA0LI<Nq82H3cOPfU6#MbgpL=AVwVz`TE_LO^{fevxW)<~iLSOo!=k7S4-VevM;xP`)_rpo8c!HCeG!FSKZs@%T$1lRkfj)z;zvJxTi_kle1|EGMQxk^&!0k%%2T4iPRR9QM@u5%Bk`WHXx?opsao9Y5q0*oTAf{2^7gCa2c9JW^*Bj8ElP<D$o$l$8-NCH~{B+D$FdX6JAaaI8+@2RpKE;=hQ360SDAX<@r*bMkv(HP)3%yy^-@0-#p3e%lIxK)E%<}nU+yN4#J41an02CUxdDvMQk-2tWS=Mu7=c(AHS@5K0dQNnIY6-XFt`l!g9Jr*##<U-7J&Y18t0BTRBFlfu5;02saF*c)nTi*;vSacvs3s;}zA2-KH<!dV6@!HslIJD|gSXzQ9)Z5SKol#Zn3rZxRz}r=Z+01x4q)G`2gH(F9v5XJHHg%d8nnzcK66xCPmu%nc`Te`_lQ2k4+SIg>mnWw{#v;bO>8O&&M#zf5!{xUdP8!gqUk82S2UmI${HLEZFx7|^)C0XD+u#)Tvm$5d2v4WZ-^Lo?56oXB9AYaa;_zjKA)nUSB0Qsjs=c+X&iC2(UNSAfT6NYnoqD?FGrl#9mM3!=sr*_e}MfUh%LJG%${ePV=_HJG}T;XkIG0yH$d?ni3)sa(Cd&rCL{IdU|U0MB%KYz*Z8D)fM1{Pf;(XAD`ud@z0{@-RV}$ENsn(R=I~`>0Jl>S!l~-qPgV)TZ(Qp9cuAWW$5WCT>JSasPi&>@1fvpnN4WD!-I^wQ2C|ND9)-HuXZ(b$ztrHp(FgYBS#UCk*Syl!L1Dl$tADlED=dKIkCl9Z{JMhYO%t%`X5$Wi#`xK3`t&D>+uUq$-k1KihnAx*64~HF6)6&H0Q)@9fh*^0>#Jx<*{9o(N_0rioeHBS&es>~)o<-y>Dd0a+$RM;4VdpXR$)_aHbdJ4O-IWv@mu0Z#QL!Ny|5o}&i}85oF*iaf(zo+O0i754uzvUwZzX8Z?%wnK}y%4@wR|s&Qu74^wAN9mOEt{hFmgJxs+zd%`pviJp-@MIRDPq$;g6@GxGe1v(e+)*=XEjBk8VO?kNv-W#8-b)wFc;`RXyBuLgz5z<1H4FKMzvAqcpS-t_e43h0K6JKYVvvgto}g-_j?F-=_s_`NnQXt}Upb#A@z`9&JI(^Ov@(f8@e*H7x&i8S~x*AIGtPtzRxo+%%BmyXDhnWl%$Y1*PC!D1@}Eo-g(g5Y2_ICuIgi$GmrAvt3C)gD8up21wY^#gmyG)P|ZTUSzj+YNT^l{(4S2|iA(FOyQd5XLy^%_3^tEBiVrZ|3ToDA*dh$GbHZ+WFI_@`Us6CZC4nyOoGx>k0who{*hYK)<RO6rrD22?Xds;8vN?|L4AuB2zB?PzyATRp>=N&%V$E_ccYp?gqFC@^PQb$35hOA1&O{gy~kb#XT=vh146K=hhGfM4Ce~1pDLhj(1~vN2XeX*9ndg6k<MD4SL;S0W~eX^`fzwm1O06{GD$j7>|qa0XqB5rNQ*#x$?5fVx+a$&~7F+9<+cne-h$kNn`_d8b3seqaY_acYsgwwUpMIu|JYrc1Ae)b}LsB6@H}^yo(){hhTDO1C|{Yh#+%_HEOr1r`tbQVVn=pFe-9a$%Q0ziF>8gdQMVZUE|hew33nMO+UNeBskE65ie9LB3IvwGg4x<98^Z{QTxGXf!_f_KQpLgp-K6;R8DoQM(UH>gn@9#-0ElXG!`w67gj^A0Ya%dRl!aTIzt)Xg<}m{sN2II?mCigG$N>%JiCL&;=x4vap&8gQIX9labVLf)o2MA`sT;7eGfnYG>%$;P2K(W2&b6#bHPDqUbA$edAO6}sxF8E>{28@s{2?#qJDk}Wi9?CHh#X~<4YwN#@*A}kGz>8Xj!OeNwwjCi<@&9FanCf5hMpbYbxu#s;upzw6v>WL3ngpEj{uIuVzPs;3i0HXu#|yM*}xX>O^29y{-JIX(z<oC3ttUcA#31RBQHH*}j%2nAMn**}P-MxYZDWSkmfW$dGV(F)(uXEt5!sU)+Mm7J{ODBJu3ZOX!n$hAWD=X8$R4>FYazrUG{;(J&M8REP&Jm*cR6M5zNT+PXTSv%tk}Y$BU~q&j;V<+#avz%lMMxjOy^X^8OKcIR4Y9r9~|&$_ZfzWd%DihBDy?1!;C(0NlO1AEKBIYPdBKy_8>)sO1RHkUh)Ajcx0Cao}rLG^N1{YEJjjBkA6n8%s$ix$#X?g`1e+%7aunoGVZ=I3{5)ex&P+f=v)7nwy)_O$YyGy~oc2yB{nSN|HBR-s+D1|)CxI+pXA(>0&5q3I#@!oXh1n!PrvhPz>xK}MozZVj7)eKKreV5`fQ4Gbw{Dyr>R8A(+s%~0M}29Tt?+@I5OS=pkti>+n5v>$D&jbz(=|M7<Y-md%!AJCyk;{$mWAr<c0NVd((*vo29<$iA$v|JSL^Sxya&W_Dyb~kySIp33JqqMpStt+KPW-05aUDscpTE)$Z+=vy|!b`m@OPX9_n<Hc}jX-y~PN>v{w4rWb;M7Jnr}3J!%!q>nrp>p<@=hAE*u)Z8^Nqp9WpV<e^rLPV^CxjKO`B@>)2hdfSg_SgHrk)tuiB*Uuj!bdw)VG?JIRsDVdf3Y{QV|=IZnj+pX%<>K_EAC2E!ei!m=UyaV@)Jkk$56hgRtZ$dt{OCdMOEC0-{)28Cl+<C^s(Sr77dwsO@S^iI0)x+ka2(*An22V31`9MdY$Bo?;Ko@rSQ>3)*=CVgA@kJDg|U>vOt)vQl7=#O&(-(2aez}iOX!2mnq!(Oag!8Vi4tv%bddP^N$Z+zKE*8oV=Y9!n6^Dvt=b;gE^r0|b_-W{5JcQw5no0hHW>jboSA6}a_ZyWn+1D`DnUG0f{i1IU$K75kB<-ADW!<<&j`R-`FYp3!Xa<n}xC7r~>{%?T8ApQ=xg=)??<nx18<KA<>Nd}17<LnRH97~YU<a|kj&QS>}BkDx5pbB%bi1?euc0KQ?A~OK-O^{k4+w2vDr(t+$L{v(?6(wu{^}@I)@g7mK2<(PYZ1Gcn_1#`1bIBnk0=MwUR4i0H5wd>Cb`c|fl;21&%Hoj(Jk6dG6t?LxqMR9oW499E&0Z&ulNXV7Wg6uHcC)uX_->mLKFvL@ihE@CDv!2VwVDWz72}F#q}{jNw52`@8!oSq8^JJ_v1wgc&6ucyN$?<EHD}BzU&2;VY%)>_<z+XK%|Y2QAiXpaWdTGgHG<9+2qZH3`<imuk}L=5a-;E61{GdWAvU=)D!p(+fE0;9vtUj$SE)asUFKzLnuAHyo31B*l3xL$lGK+T8LWo9&B*S}*h1kAA5#+bFvPvrw0Z*Hz1K>7;KPA3Bp@FWAPowptRC+@8!DJoT-Q1<{}=A7kTVCF$Js)B{y$J@AFSZz5<_jEG)<tut|*$O$R-j_D`HG9RNeub4>||ISv~PP!4BtxsuXu;g+nz%*=oV8<lbf-+gy<fB<C6_P_lMlF$Amwz&Iq00i{A*Dw-obEd5x>;Wt(z-w!w6)Ng-$Km3O7zXR;xEBT-+*p);?`WT^v%6BuwYCi)I&ZYzhHlCE)Qd-LFsbNVM5Dw-s<ONuS=|&(h#D5PU=irGIqs517T>i-uz>41pq0$F0S+?-|1(U?X-5#w?5Qb#cqG6Ds3jd}Fl0VW(60F!y>y>_}1Z*gZ%<Qojg&6U`e54MZ=>J!9Xv=GhH%(o0NmTnKCCjuSas*r_XL&i!K|_#b>qkhTC5twcliDeM%fiP^BE;o}l03zm&olOPi?9D`ToLm5=J=%-9+FEP;-@lrrzzmuOK`|l<X>$G!L&!nM*pY<HjrYzb8ATm#Kr<IzW*=I3Fvw<^iQwyR$nC!mb^-7t5!D%Pt0zUi<1Gjzni%`R~R|2TP%U>)m05I*R5Gq=Gz1(Z^)!DwAL*Y*rB=zk$;2Z)9V|9+=eBTwn@u65;!qbN$s*)G$FpZ2G@O&$uX^Kap_9!{1#vf=Lx*u`&v0RX!d5S6~!&3Z5TgKWMC!p4Lm`5sRwIuzG%4uXIg5-*yoMHrupvbBMw;ndvtSk@#f#AEplE6gA$rPIw5_PHQQjt*H`b}UmF*H-u?dZ=KcR%y)o|IU)|8hjht%vN2hPd(!t04y$~Aa$r!^S<F&-_vQGD0cBqIGlM%s3cD*;Zm8X>-2BR6HT*Y0Bx#$yBQl09#`jx{*Irmm<Mjv$eMtof-cZhTW|C&GpvlxB4`S|wzhbuRSi;yblZWWhybIpqnA3pw*4=c#c-mOi?>@_>5_JIB$b?wvRp(UB`q5mi^sdS*;e3wpc-(SD0jfU?nv4>i$T-10U-rwFy@-2Bl#Lio7P`QPOEvciy5SAym`$)?A<~=FPXB*3bgBG?A6FzQko8P|Yecaw%T)(-vdE*XBXShlSw~EtR`5CR^Y*y_=))0JL#&wZ|Q7#3&%Xnr{28Sa*M7X=g71bK!Ft{f_cX!ny?Sl}FL-rHDSw)tOWkl_6eBo>4jcSEFgIV>&S2(DnZVbtn|8h&nlK2v7E^H0sr-qbr+SKPcC?jDw=nVJ53Wl&jZwYpS!}D@db2|B_D9iUSiZU)KaiUc@0U71MX$HWCtMpQyZXU2I#$wqmb=)hHSc>WhE5B0o8dQ($RnO_|Ih?oqL>{3L3LCth8?&sZl~j*7zovwGGGq7`&(se%jq<|<w8Y;cWj^x5(X2b0OioWbofH53yz{biK5ci$laBA5owr|}93j}18`0(COZ<y)YcXR6r^jtl3GJcGj$A-kK0Py*02`TRBMk{XX(f~&9Kw4J0h+yU-@g|+RjuPt3Tc!7DuoKvR>V*LdIjoikxd_BDwipu4N7Ih??p?{KW`W1wWHw<KKWif@XKJna&xxTY*+e?4TdtG<=CIWze1^;7<hJ$4Wo4OPwyeP6*1))Tussu<>esXGjhtABzh`pkRObqs{Mol*m-zSeKrhzkZF*gB^wqmcQE~6n{|d9={zvmX(?Kh)p`BqxrM%ZWU%1s(W6To-QV~2>Djj{Kf#$5g3Il++iD1Qi|Yrc%CBmXazvjeUsSkZn4dA)ePF8T9JOuzzhgCiz2Ch@mK=S;RE~Y?1Csp2Cm><byXM9GUuI(#Pu8hU%i~klV!~u2K9}}wxofj!S&E+Ku8ZgaFIYBXdli%9#||<k*qo>5e(dO9Ive@x&`;bZkKHP&SvZ)2BR^k8_iOSb&DQ^r&iS{=<=m!el@cst<YeM!*x+m`=lbtH`Cd3n-8#mPV4Sww{0kW7TXOD9{5nRfi-M!mwteK_+7%O*dEh59j%|88KF1MnIM6k>gOkuk*k5K(z`P*i)wIj=)8~J5P*NK9Wh2ZrKdD3b<^i7dAq;r*^Cy?5q07ig#t3iT-~Qdq%V>r!{`3p{)}5${hod+Qqt&N}UC>Z*4W3JGW%3&yO6JGs>r18NQZ3>UAAWZEoj%RP&0YG)!Qo>qWb4yXf<;L3S~zzJljssfa<s|)OW5Z=B1cU9Ou`PZ<xLH870x2HJCZ<WW4`ZXWZou4n2emtdF_y7Q*Q9WrQj#Xfl&k2x>C{nx%#2Cz?(;Lit}=5<gL;L**N7RxXa$48Q6O3i|_fI1>jaG8Hcp|m$q?KaYd3VTQ|EZZ0+Ri?nO>)6&r4)V_QGDy{LESwgEzbq%@dm4GR@fD3b4uSpCNCsI--VF5R7YEUKqr3_TS0nw%I?*E*IxsGl|~j(n-g`q<ZSJDo)~q|yuvdI^xc`=-9nb7`wxNOZerDy0L4zp!(we-sR$+gp4xf;`%cTK?%M9!P%iO6ML?J9afo+o*5ysTA9+zzmYx`NkUFL^agQV((FQmrA{Fv9IeE-{sd>YwV0zM*;XQNVt9WbchPL9W9zyps6ipY6FxBXE&J}5UG-5QDtKAt1<~nQJNYfC{IOqQ-P8*lqHZ;g00SW4yTwjHSw6+8Gv5AM{6u~-I*=4&{?Hb(DJ!$AEM;HrFrcX2SPu<VAA}8WVo&xH#aDEilyuB<NYcQC4L2Jws_#ff@zrShr-Yzd6ESVh3qG3kv#CD5L#)xazBb_#dYml0k*?hcn$fI9!H18bS=%Cv!X|(?%91qU~LxgC9*n>rebW&_&noLF=Lhl;pS@ajW?_`8kuYoufryhB1g3WkFq<+hsd5nO}WkY#+)yvtHdyNgz$ERFUp|{8bzEORP2?RzEJVKUtCL`y-uL%;0jIkA9<(jgSp?n<gVS9Vewmw&1Ze~p$1%*$p1t*$r9I-Ft-xRVn^&#L0rCoh>ObO5A%L_517Mg>5gtV)v*jW2P-vJ_W9loTpu1IQR&<FzHFlLS1`HST2n$*iY5#54Bh8K&5~*@T{N{Z&N_FugG?{>TawUdWYkgx?xp{OgV=loNBjtwoi(Qdo&tOaKZ&S}3}N0CadoBtR*p`ygA-$t_`CH^ezDH#uhfaB|EmnN$47UtageOekXU(5eM{KWldiB{ZM{{9(+2Z_%bmQCgp$Wcx#W#Lt;24sT(LBub+BHk22W4YfIfFNSmS8IPC}uT8mgs+wpC9p)wA^i7s?aB^;>tUdoRtB(~r@FE7fs*o%`@pD}au<6q3#Uxsj1PEPV%mN@*0i%g;P3TVSN(!%&@%SCXOtQHK|cep(s%g+;CzIF)mNSU5{I2Xutai@;F>ewL&Jeq6eemuHAZHA<nH>J?&mXFM!_=+U4FIW!N;Esv(%>Du(?9Dhz&hZ=^lbrAvnO-Tx3;_B5CZU9)XctBU@T}kotmse0DX<2pAc=qOj_`v-#Zu0a~G%O*hRIYA8(BHOguU)TH^M|EOw=j6}x}`fHYW7uInmo9uyNsv2c-PRabfH`hV4Jvm?(Ge&NFag3m((K{(5>D{N3TGb#3x^P;!7Awiu?^ZZ*rzUU8MEksK*W`k=0ZzZ`iZp!KA~@*Cd}I|56q9X0d#8%B3Mk838jb@!));WG~5qt*6w8aEOX5WIpah-SKuUc6Dcbe=`z^WyURyE8Qh;>OM|<-WO*{<-KBTQsacTV4e_Z@Il*x@V%`&Qq)~-RM(!yqjdy^(l;0=Lj!xIx*y>a;anV}L9~HTnWV1U?$s}K(f7d7lRh5xuq<cD%IU=At{&=_$uUo9OXBCZefWN4qWhO02Pg6^1Z;bwNj>%$Wv-Oxh87hmTT2TC&N$_T-2d&uBL=vpf{*KrEU!QGjVt*5!@YHNvMSg5Q7n@WU?Xr6WvmdSH)<F2i1_IY99}L$mvR!+9BQYirjz!$Tm60B6{96*m|ZT;Zh2RMo(1x`MA-hrQC>dB4$S-q<GY=Fm3=<I%RjjXgRQ?mWL{iHxGQ9iUqv#uR=t5Jq<oWwuM(-{VgJfD8BXrk^jx9ko{!En?mcZ8e#>oIS<20x`eK`vJTlHN<S(}A<Jc;>QhAf@h5z>M;^vO;{j4S6=o~YZ0J91n{ZRcxC@v@W!&!?{@QSoE&Zf{NORva`Xy|MUog%?05u?kGe|-9Ib$7KlMWXS)0hVJOQ~', 'offset': (-0.8, -0.37, 0.072), 'rotation_quarter_turns': 0, 'seat': 'WholeChamferedStaggeredPreparationFloor'}, {'label': 'Riddle', 'sha256': 'e7b9e686ceb21f6d0dfdbe373bb97c059a3d3d14e2d933f941bd2eee17aa886a', 'encoded': 'c-pmneRI>u((nKN6ngg5DM@5(Y$pV;(bmmEV5#K*H_4t|*4O2dEhQF_B}I~*7>e)y^sjqHl3x<oI_FYFBF$@0Pft(3DnI@7(}z5|iV{DzX6Yh}!!oprWs!wR5C&EehCw@zf*=m9%iLdt9qV0mH7{>N{InMSb(mY{r|(`*&QAaR_VkaTRg``i%`895LO=JDS!kt6yzcz;(@(8vk)=60m2>sENE0>pi+LPPRk1Eq87)FJOXE14l~I}$Dk{UgOw+h%UFPY+%BUB$we%n#>9uu!adLLyp=Sp_9C!HP_X`hI&SY{K#o=V)cJi=D;}unQGCvQKvUPHPetO~A{#72$mT|ev!}eu#N9(MX-EJ(q&C70gd-m|(r)TGHKfL$sUZ>mX+QW;t7w=9z`!zaS=M~P*(fLep_8Oh-)~nO=muGK3UU2UZNoXbEZM?SpWjRlC>QZ5z0eJ}j4a9b=*Xc61XysGdgk_dvOA11_Ro<pnoF-S+Rh}*r8s$0)3Tx))`I_tI)Y2-VAhdEniVHnZF$ZF!WEMvWO}z+9qKUbmT+!%7nfqB``7~HL52M@)@3OQ2<at^YRu(0Nf!gwEBtMSRTPvr%r2fm;Copq=ZQVxYoa)Pb8Pb}Qgz9OGEX*&{+{fcIEz5M#u}%bj+WDlkvSrMG00}$-jg=IuFfT${VU$_Z5UmTVOaUFk98qsfiJ^*+cAkc}08>gZT2oqL0Pw<Sg_fD05IzWb80i)$<aIH2lof|Qw`z`k<!9C^Dxzsj`*1?=-Of`2?<!0QZ-nNkz#c0rNlU_-l@cPZQXH~*nuKebEL;%^7`p-B_6@S)P+2&Tfkl*o<$d`=lrr^m+S#0%%?a()HjD)ow{v==9RyLCqgN3&O@|X?WqFz@>r0rYRxt~cklMee$J<EOvPf~_6xGqV39l~q1A;>%jw=ZvnYE6>I8fGQnu2DN(w~)tp46wZFsJpUi)cm&TlmTHlIrMa0qDZN49m6N<^}VFS?ouPj@^3Wef>6k_xAm7=iX>MeEH%1#mUPHetvWEk$?a4;p~(jUZ2vbrQdJgpTB)|I=MJK=Z3A1C+|)#E>69XWB=jjiwiyua_*GVIee}<{X^C1b)Tr7t2)n)Ro7LH{ePEHSe}=JykD8Zi<2aHLkA6gde5j&AOEG#@e_J}hF+N96;b1vp`4F?f*waS1JCqaCOM)B`|h|EgqM~d1dgw!?jR2dA#^yGbkv=@gEgTsx9$|tN@9J9GH&E@mtr~H*QNbHm&G!sw_>}?qe8l%gD)+EwA>iHST3mD14HvsXm)Y@QE&WcI_i(xKK-Dl-dO3UF3P%6tMpS3Wj(2tArqnl$FD%ZjnFA>^3oCDd_D6riOOa(USsdE?k#P?1+__Nx7A8rDjG@UbP(M^%UXFO!2&Zu=aT5ObnaaB+^tZO@neR^)p&SmI^1ya4T>+vG*B8Z7oi740lwAfh88kbf)~6+^v1srdgHO{K0dbU{`?r>F$bYJJr#!u&Cu@A0<7p#kN%=NsHV?D=4}DBY63FUaJ1!j%L;?5u<#mpX6GfXl&(#OcWVm<Dl&U}qi#mM!T8{2H0Tk$L%%5KuC<71JBjD@n9cLxBWFsRF-94N;9*sQVYs?Ocl4rgTq^SckRC_i`?(jkpYu@N7ar})3#?loR+q~$A8&nBTt>9jM6Zqguo}Ch^bYgDgtj*$ypO#gn$dpHoY9OhK?LCAH<Lk_M}F)XdhnPim|$``w#8%-7IP;~)2slgBp!g{SJ3Ei#hcCVYDDk5TO*s9xU_buajFrpwU3g6XnW_WF%c6Auj|5%UIfW*r@?2>A;NP1nG7#Gxc!Niooh^>@bj~Bt`B&^`Y8fw=|e+EY3YA_T>PBw_sq%Cc#ZjHxflD3Y2brC)NJ5XN7#Mj%*@es+fH?ix!klN3JwY{j*8N$*TZ8IS*6Po3>riZbk^Jeb3DRWTXczz3O|@S`GE<P4hK!s(a3jb*4sHrcNQk23iszjgSpQ#SeOu<;L7J}RMIpvk6uQf+r+H!;Cu#B%@AX>iNNd_ijhASK&JZlZ0x@9h@yM_0WQ8MS%$iYpR65Fvgx_hJy!bn_1OK{Yjalyaj8}W;z-UCov#`FoZ*zY6=^_Pqmi#!dZ4zvHDh;UW<qX74O~wM2a>Whb3VJnX&(C5)Q*IMa6obl2@NNFI*Cu5=6RYs_WLwx7ZC(ci-=+lDFHIGP3Ub5F4PSaxkF7-R4cS}M}k}sPS$cdGqvujb#H?Q|M=FcOg6pR@l2DIIdK_?S`KQ46FPF}wo+dhYq+&WJo{L#u`kRwn5FA8$2elzFektrTy|&)Sma2fkaprAQB(TwA0#fw`^S!Bq$29`8UF$0J$I6vz-f9Xb#bcZ(e{niSQOSUic?&q^N4<qtCdn=j|+QJc&7`yTu67*coT+^(^Y+S2-(CrQcu)VbxcoP)uZPldg`lVDm&z|BYN)BQ;*s|RZrY;1Ab<oX&}P_V|i7n5|1PvTEnf!w>Cr=+#MjAOOM8-*<75KY2n<`V%!&<=S-XoM%NuKrJr1?w~BgE-_^=91xvy!GfHnXf=HDq{DerbRQV&mMrLUt_etq5A4QLe-zwCvR;ED_C0h;Tg5B8QvAKe9?0`wyLvQEO7~Z?bdY40gQRC@03P|S-!i;`4H+%<KOOFsw$f{A*y%$yJwd57vD##^Eb&Cc4DAI~Y4AtX)g{ATlLr5ip7E;QYQ?+}l-D8r_zwon-U*rD}Sv*Um?lyV$sNH!&0`-%_F>pl6M(NpqK)rfLTHYI$=FUl@wGT)ub&80X9UUn&QzRpIx=)`d8lcN^{@nq;<F(U0e&P~t?UzQ`-d2%`Rb?<PKm$slPeDUwt=o24{V?Ypb7|i2StRBS;15ZEIDE#yTcjl$=wFlK@GIL*K2l)?J^%hJi$H5x1dXwlU!CsJ6TK1?%CBCh`&?GTLtCV($HoL;vAv|ZuF|Odtf3cl1+d~zt76rwVq=U$hC%pHr~8B$01Fe;TrcBS8tJ?m=nUg*Yy_Ih8jg->BaTRWB53=12~?(wdOcadYu4@o9`++DmjN52Fbo}ml+<MC-L*+XtReP~;D2*<4A_rsg<d^DeJrb=<|J3@<)0H#uy*+>5{<sGdYpM~OKVjEM-QC#PVw_|(jf^0hrFfr-UWIfp*QYtU58<2Ob(>6m$^2@pls@|*@{tZUv-Je+z&6&?%KRQ0`F-b@I9wBsvqmxldjV9`BOUoxFdhy7~tqvXZV(s=9k92VmHa3IfO%p_sJ8Xekk6DpnfSj&_&N1lpm+JVP2bSHqUUp7UD4mpbd+UA)$vE&?XHrgnxsEI(<z-4GdhQ8881L3iq%6SQg(S96#r^AIs8vAjzX=jl~m8ZC<6A;mRnqKBrM)D5qv%1zU?qaFdp%fwn9zsAB#fqT>O!P@ktmVJH8v&Ldd5U?|MPpbZT!ykmRafZ&Q|*G-!sDejQph?&7ccL`JFCE>n37aQ~~vA&|im+lp<XGV>K!U0Hy!cR5zbI@SswWahCejdm(^d;0k?u)jPjdw)8{v*?JkR5o`7(#9I&%Wn%`Bt`2J#0wKVs6OP^M)1%k@?R*y#|2CFcA?kcYDv=;ipf{Dp-$ty5_IHyiw;E7OCSSy2GCKo{fj;Y_`mzFz|}7bmaU+n;PYxe`<A-&*o;`r%y)Jtk;27{4_9QcOWQ`T>F`>QCGLcHQ!Zc{Qg*vt;;ZOf4pY^7&=z4+(8&0(q>*SGw<s+-mz5#!Cn-FOshMVG#SV*+7g!eS0vaN3}-cBt41y8{u83V83{WM#1oMKj6_S1jwv&;Ey}tIO&j8{6iS&9jHRqA@{f_FO<_~2COwk3gO<&jTtTdebQgmZ*0|F=A&rKB{PWLIbP(K))u&IR&j-PJtp56IbbSzf5mhkwBFGh;CRlI0-I+H{uugENg0%|1xNHPrvrmN(*=z@sDNLj=iL0?~U>jU+s(jcQ4J&EG43Te!r5(LEJNaa;L~}QPtPZWXKQ8D%+amm-ISYS1#SW0#`Y-3b=_=4%iS66{BkPJdQAAyY58&p5e8~)fnSs`d(`8|?q8l*ZW4174k|G%*k7;dU*(P}i)^r<e=wwzdaq-r25!<x}`c?^Hbr<J?@hyNy4QnTf_KU=!A5`84h%&f}IzJ@d7FS-o2lBsrq4`Pge#xd!ETG>N$&!FG7Ye~tv))rb-;pij)LW45Q(Qgj9Q6+se$$2O4(E}#@b7lZaUIe4isW~`i~8U{&!8%j#)`WL1y3Q{^vqQx-Xr33w|*Xow}(b(UdKR=;8na_v>!VXD3b|h9%-PS;}U(^?aD1G_}0sQt2aRm_~)qES-9`XHH;C4Q+~lsdW_5HX;+JEJSgjFw6Ld;&W;S3idU!F?xr`42&23W!-V9wg4Q=HN&co=i|JC9>6fKHn=eARu%d*BQLh^w9NgMFtH;6xn30CG+XL)RvHGpH-@kP?M>;&hnvFcq6c+nL+lsBNBgcLRm~GNRm1F;omDp<Pj@fqB5MEBj?`I!y=L7pAZQ?f4D-(feGEZRI8Pkvc*yu4EMRd_Uuj#1a+pEY#d)n3{wG{=)GUc4^SUP2TJ2WpL1lX$A-A0t4f#CrzF!6x{%;M1TDm+gw9>=eZDwjdyX2<t81G^V##>kiASJbZ0TGG^RKv2qzB%Ui;+LAzyaqkLOo5g9t-m*(AxP_~*)6%ND+$r-rHD9w~Yvgo}h)j>*qI$~G@ev(I_CX!<+c8ni5kv_6{siwJrT%jgM+ZEt!4IkTG;$k5<9Kg8>Zi7OBw>HQe*f|0eJ$Sq0wipB$m9y3MtlSG%?)6p4Qg+3!yT&~y~|KMwq=^}$pWG(Ke2Y#HvO{V!vw;C*;~Tog6<TijUUidHYo=HKd7{@VGTn5vp!P-*rrwv;JE$>4T0U(Hstzl|A@4%r_YI%%C1R4|4Co-(xz=9%hS)GX<(z_{%%~Ga@&Z9T%7BKM%Cak`<d%K@L?r@1<*Zz&a1&Ome#y*w0x6C8LtJRE3M`DDVj5pZI{sM4jcA~`c$)cEW9)j_q|{8QV=_!>0cJXtD0*7d;R?!aAzfZL6+rJ(3xW!3oea>!NNf$V1PxNlUoz3@sYQi?(864_)*d^vLByOF_S%Ev+8pgQU~nHHsG`C3TMdUZAm!@XR`1d77ND*EFAX6q?srO^5OV^r9>&|fPjK17p~`3vMCA5SLK{W>GYoR5-)Io<Ps}NgqpN5C8;cV^acL=n5_#TPP8l)E_~P`vOJ<Q8?6u`5=2p_Re9M)8DAb(I7M$dD?eU_g;V?Ou12<LYLCam^IzY-zVJk%Y&#G_GFn~j<<m{w1IQu!t7yTsPR25?dq69e<GcmNU}Jhu8$B6_`#@~z@B?-M?C+43g%*IR3B90<dyQM0(Foe&+ZcmiZuAR}p?xLnnQitKE<Z)o2h}jG4DdFx4Q<eZFxqyZ9$e7jGr$O*7|`=h->ov!l_Lm3A6L+1>KD;$Vggwz@2V>Eh{IC~?|quE^;)}op@mkP<*`!whC~eFMk_-sSsEpRHq&sIaHP$+az;-JO)mYKCNQS!zUYVTr`7cEy>a7h0^-I8J0z#a@Q!GZZMv$|N<N)=xQfEtNiidq;Mt6qiV?^;n!(==o(u0a?HzG89VAtqyEdEeMBsxuQjg$AIST;Xxm|?5gvNynMDg$uOo<(GqznmM3KLFvLeYl}#+8KqOezcM1VLjHQKBX!Igy4l!R#KGf!lih;pOk=!ZJFL^*@|l{QAM`ce=wr-kuRH{`&UiZ|_gf&pncGy2q`TC;vJ<J305h+U0z?m?pUX2F_vUShb0_b)LG)zVX|94N*C<p(EAr97!qkFf@jeY+BMq&h5Hjj3}7;vuiGCbi5_jCWd$P=81^m*;jNS$W(_ndulKeSF{h6sVJg&o-V_(g#Y!~J~+2pY{C3(C<vIGzdU(&dJek<vDIJRoxXo{dS-q6_2m2%E*~A0IL+2-ij9((MQrD?jN-yXE&iJrcA9ThcBZR2QAlVS{qpZ$FX**JgLNRNrBg@(oq}(x36s09ef#|M-Ra8<y63l=1|bN{Sr*~sDo&?<?7j9$W)&8(U=s^mtLPQ@rQb2(5`{b1E$igrf;4Dn;kGz<%tI6C+~FMog_0rv?7%5Sv{yoCDLTcvD8q$k|LgSP?Cnc?e;Xq6a3YtM*OTFCIwIn{6GEP&WB2mYOTxS9KU>d;19b`?XQ=RK!?r4j^u6BG)<z-l;0Jz&>ukbZX?8)$aHnAqCTUbu4H#vsm~A=SlvzUTuSu2}tm21y>J?K>k_H59b3(mHRDvI*MO1FXq??eg6Z!#(+cbt}zkd7Y=_`A03-4$XfziUh3Ts?*I4lb+rDuP9|7L5Dt=6+NPIEoy*_&TZwp!C*iwVng5>u;JeER1{qQ}!$#4Kd{?19-oI%l$H_JB4`*=9fN0e4llAW|c-F0RpCSB<!COno%!2vkOKJy?y?s;r4ff=e)272AU&u}BhSUq)9B?l*lG)Qj0eppA9yqtNC;zfY69Sh$}&??KIKZ)3jaR(pwfFB-Q<cMG8pk?=O2@1^Ai=J&Oc&A3|nc|dzH^USsw@nGh8hT7E31g6YdMBSCb%z_pZvSM?Al89zPf{sF?Enawg7+w<IvLNRU7o8xwyp$!<I3E9`()v*2P90|6qJ!57*f>8GohuT9?2jZ^&mtm(!20F<)obF^Stm-eWm$~uUwl%AUSdFdOdR{tU&iHxr6N5|-SiCLCt*?SwB&^~TK)@5jHB63LtcBM;Ypm${he05PNT^M&i5iJ*e?19J6m=-bekPcP2+RI19<wr=GY;l1JRYzyi78>^h4?i@eu3^A^$i@bV8sy;>zoiR+^UerpbjTTL!Dbrac;w_+p9H@xUy(8lGRpO;)4O8N7Bd0c==lIkG`)<s=G7dgiPFUCdI%q|(2r)^2~Yb)^=^8iE(qGnq)emc9x6C8Tn@78RRnnU*C*cpP%nej`bM#Z4XfFTwq68>x%~Vu@r4>aiHfipLF)8WiitVxxqqWi}_})qpR@aDqL_NzNb$k*d)NmW!-#^m$ZpYfP@gb)jWSx&`>$4X10i6_S)xoj|Rj=}=Lexv+8QNLC6rPF&c5bTrA<sCPD0H8mP5D&Qbbd(3T@SpXZ3J52Y}1Vga+?w+SKfKCtbfQFVeCC&igcoY(_76KL<y)d3sLgpeO@Z;Hpy)B4LCJy3E7djMG<Sgp!vnGpi%CtEO4I2V}vH7!Xh7&TNwbcx%J}#oLsLM?g7Bxnw;Z>Rx2x>DOClPJsop&X?hykp|wAF}EX<kVUegvhWIgm?AQ_D(6!uu0K%>+R^L=e<bo`$^d20TKdY`+f9O$AzpwJ|UO2=-Yl2+wmZI5fFHeK*y+TkD?PVGYh~9?q_r?7(*mq!Re-(3#ZjH6^C3VFKF0!+V=D4N;*Va11bPB4H<@JIha^%QOynO{}6*KlT>62+XDtJ4^=>qwEyXRYIaDACJa1%ka_?w$mC?stm#_p0n%_CHgPwkWul|N!QI@ZlwkTV6V%3fIz5&uQ90CRkScZ3)Bo@)QXB5Xgy$+^1d0iF>W^etDUflriZqxKK9`L;h=B<H5yTq#i2a_Kz5QQ2FDY|t33d)HbF{97j!;pOhBdI2sGaKkpM9EwC2=#P22fVlbb`eMCN&PH@QvoIQTy#A*HoEq=7U{hIowFs>-U!{mvGQ72UWEiW81#ZBybX3Y-mS-LW^)lSyjAOlIOBRc8z6Eimb5(kfiHwqMlnj=u*lOIGG}LRZ0L9+ibtHBgyiM>R@!!)L2z?1SuiCU$Wc_W2p1%)_~kKnzsa2VIvQ0u;lZn(J5s7;LE6eX$c#9VIKT_n7L2MZp7R7;wo06a@|Nh*}J9^aNBA_7Dw>>OkE{t)8y0-(||Bj>6VwWaDjluzKP34(bAWditV#(eDm`g~~Br8;DRWk)BZklL7CoVjC84SGksf`x<BB)%dtB=OiWZt{)#!SrR}-KY9NOo~<x!!|qMYDk|3<4E2hLB%1kU6)%J1!4OzJTb8ux$<NnScu&Xro#d#zq?_HE`EZ)CZ@km0f${DmQI{CIcOPZS5{Ky`yz)t&>pnytT<S?SQ$|t)lZt+r(ZewIy*;@<!+5$?JVi3nFrIA{&k*%a^N^n7#r~ss`Y4_qnEWR5jJWPcv40>Pe0rWz7l!}9>q}rTosy)l0T9CCfO_JR36c#wkSq6i>>NptEFyq-kD{<XC6!1hK2><&p3;veeU9VmA0H}uJMQt@QIAv85J|#bRz7YIA4?AVt>$O|U<ed!7xq^PK`Pa=2J^ybuKUlvWF2vEal6L{@ClQAwHR;IBQSeolXeA$#(i%0Hijv$TQ!#Z+}fLQ;Mg@y8lorYV7e1(hlA9=A_|1h+*Y^BOrsB$+mgdJAx$CR6EP{m__7R(Ev+w8DQP5#e%ms#*H-Jsu`NVkA%f(!NnFfMtsW8RyBCQ1W)$(#9>~q8dlYFL1ry={tji66SW@HDx@@8+k(SbeuDRA{wvC%5vKOMVsIwyi){6ADCPc2Tt?C?!?1}Z!(I<Eo>pWr(4Uv`lV^X}5V3JT3t;fmS(cxH0-E?1FrH^kQ%&%~{Q9P}RtGR!Mk-4WF`)xuRVia)rB5i%OL{&A#LB|?v9P`yU;bxNs$s7?wrEFSHv{)`k{DpLzk}_k)K(p!v@`E6@9@4i5zOttzdSKIZcO5?@Gts^Qif`;)n@5H9OUxRRRfJa@>LD_caa5Cf6C;OM>ufqIo7DkjQfR@&{X)@zx)pE++{yfwCXP_FJY-%I!l@~#by?2vTb189Tx4{PrfEQ@h6Y3jaYGc#oCCv1%%Zi1rR4RBlR@qg(7pCHSW^Vf(&FMqvOg=s5@=Z~sto~_N&Smjay%dDV+~!PN(FmZGy$2eR^I4GgrB{l&v2G|&T553Bl_7LyB(dRxk9q46p1tdZxMK4*7?%@B3x3ujw@n`9pZDxLa2G?%cEuXb9c}P@cdfoq@bq})7{FgWy;lRtZeM*WYH&j%R6G>e%$}I84&sp>$U86cn2y-vrLmrx{QUQe0{}V<$gAo*fdqg8?hTf6Q_=VMP}0kQ%k;X%aR1%jfCGlS-CBp`o=djB6B!ZS1xSiAMq=avZh-}S;!H#pxH^euQgQd-b7*-UEQ46HRZ%E>@W%V9=Z&<AE*MebD&-v3{2vhB%p+57^+hApNGP4Gnf?=o(BBJh!%8RxR5$`DnhO(A}=URO5QM}x6r)ll)fVRA1{msfY0nXoTmjR%E&;Z$OOe>Cn(x<CAchwpyyVvu-<SG8<abfCK&1TKuIR6(k92QwI`leXH>!yj%XxP@^fDz2D=jcs@X|(PvjWH<kV|gh*Q!%CFIt+(eicPbP1a*KbD4WP`9K)RlTh?-u$}=rWjWS2f=PL1ZaD*?aTs(n~Xtk^usKH038Y3B9#6Ix{=<d>hyyx&@!^vPeNXO%?WO{7y+vrpeCG;o9cYr;C%3_iwt-ycavM(@WoZ1ddv5{Ekps4_Lv00;dHvEZc23|s<rr@U<*Ng%tzU1&>z=O)786OG}Wu(=w09EXU@BvPHXc42K(8g$;{=M`Q>arF<fk{oLu3>9B`&jLY!QQEWifoZK5d(=cJ+z&`EWd(tR@xC+X!S468sm>2{eX5fgu>7qp8#l80b&tN_a%2}F=N#vQd^)HD4bYA~%PXjvQQZX>jZ&?V}XX6x0Kn&t+#9;20nJU{sCeHG)tfFt{@P0N*7vN)Pw#Fm4N*$32r^jYBN;QP-EDoJQkK5dj!8@E-2q&8t9q_(-kG7VDU;;3+2l46Zgokze*4F*FQ=NY?Wd?_ax;0F(#$S?*GG)fgCLUZwCa{4*QG||Dq{IMC>fo;`j(H1atn+^FMfB<M@b%0F0`{faiiyBr32R3~}(lzJdLF&&S;3z;Y?e?GO4-fDb4Gk#U_Aim~s|z0w8^$mm{u{yr^RPBr)+}0Lec0gQRa6FyV8@^ck^)~kT6*7P)~YUTxFcK~9uo^juYAMn)zKvQI1M}@5W7jyV3&Z7db4I&TVSgkX>T>W`$;>}y(hXiYppC_ixtdmU6I(lXT=<!L=zBKzvf&B-qlKdE5(u!)?b)l2|@3CF81safwaVXL_Lw?TK>1t#ozCtvkx@YxI>A7nUJSVJg8hu;|3C?4X~(8b3$j0i~ZO{Qqx2aww_eDsYY;H3q=1+!WFS2*4y?+Y#AQ%_Y9xg%!YGz?i-<QcmIG$IvAPgtA>ERBj6mmV<aMsOaRyS+KOw;8;Ox)9#NNeoI;>_zOQ|&5m3h2^lbBZs>8JOA${Q;(RpVPI-BOsLK4P)*sH6j$eLucK{fbDMA9kOS=cE`;0=aA$G$lIb7H$SciowgwAuG5l(bnG@b{dsJcMdk@RclCYolgJms><79YuR*+5+TL!i51>S11k)Ddb($?pv8jH)*U;YBwg3(7j5ZGv{){rLAgLv}*XTm3BNU`|XD_`gxv(GtT*;SL+>V6)_d=b37w7+Ap`>n&Y0&k&98)SH5Ti&K~D9tDEeXu6)=mlx{k$O`~En>v8X=g^u0&t2Nw-8Q0t|{Ibj)E>ZRb5l<8BI}7j4A*2uT$lTWUtagwtiOWpbIAAMmuLL3>>`f#AVj#qR>JN43L@pjjf4w1`af+e#e!AOsBR<%=l7;q%{8g*M`+Gd*ho${p<jyMOvYB}WG5>xMziB7pC{q1hr%@zdJ&MMAIEAZl^wX_qkWsniPaV6ByiT3phxtfUNtZcogT}FEaLs&@qz9?J%sl<s!%i{x`%jLYhJSr?1f}zqQ@RBlB4K3@Y}f4&@24~G(9=A;3!*C+<LGYK3=h?lem{or)v1Xh+;Ws2jNl0$4^q<$vY9xy?s3-|mpX=Ch2lsz0EpFUB5wGrxV&^sgolS*iVweEJhl-Q6jSBYc9m{#0@mKV`^8r5HV(A|pCt^_Y)v{u^PRRnUW;$JDk8OpO<u)jIX+_J8?T*?Z>Z3AyO8h`AO7Dc0myscmR;*iVF;uRYTfwWR|y@l2OKt{?5P+DZH})b=sG%}WkQ2U)Ko1l))s%ecGt5<6_Ek3Z(^%8vh6{=@iYxzjj&3|Q(eLW&>&9h68{b*^GLO<+Qm=fZF_qW{AKd1YLlw5g^DIZ(l5y_BE(OsFqBD|PQ>785A;D{nI1D1oB$5RE)(GGL9eot*OqlH8dU~%dvL$;UD;wjtu(F;^~fG<yefNBY9c&t2v@WsqrO$5Esasja8-j!2!^-}r*$ngW1$)*!Gmbk9AT$*38k&rB%~q{qoF3UI4B+i;!6`@7C@wCBN$wRKu4yk-(oI1C#!?-y2*51f`xCe5Jl>Y4o6%efV>I>x{R)9<vR2Sdsq79lGb3;?gh(PnAe}Zlqh%kEUeU)B=?pqp|HcpmcTwtapODgK;XOa+j$6lbifP=$lDx91A}R@#~WXP1rv+wy9f6FLrRxqE|fk;3vtGKq{BX#!ON$KjDX_UK!Ms|G>)821gLHtW2(?`2P{6A7=%u?<~qR+$B*i$_)bQv6IWj5VO8=?JY(C;hy{{zjSwigJ8&5S))8PF6UP8kAu1KlQ9N#ZpZ4)rW+UGoufFPU(0+UT6~li6*wGi#K{Lpew2Aa<f)Xm<PY~Jt1VA_o2o5-&G~3c#${y%xi5CzKu2P&AU=gAlfxr;|7U7(OCNf4#2-Udxm0iGEu49zm`uU=b%&uAP)8P%;t0<01szt}BL=*nDE`mRbSsrDqrwtlk(FGX_BeMsrMZrcqvhQesHU0l$kCjxr>@@Z41?}43VzRt9v>g$*sYqUOLTCz-Y{LX0w>G~1s=vKU3?R(u@DP<-`s8Wae3-C<9lHL9bxO$RuW~N@_%W%}@!ArigOZ{1<mCKomk>mIm~14CKpaRZK0XVdPz1*UU%vl8@(N5lnfixsd3UG-2OC<Y^wqZ;4o}KzlZQ-#^Iz>sovVc$&#SLM*6KC|FVEYOs_fS}a(76iungC&8Q5d~wur@i*ZTO&nMG>D0!-VcYaNlFn5w~cnJwBlz7+>IW0A-aY;$oLN_&25u!Zsj-fu(099y({yWLLGw&pgBpEU_s`PB-VAXS>l_%kpY4LH)$FvcM}3LX2+=?5fae43n{p1k^GD>>)&VbF(Wh(U;7l};C=_{-^=x9_c!-!FdsaQ61E(^uBT+tV}pbtYLb|LzSfxjLZgSbhu+v$m#C$oMX?{Ib`7CLSuH#C$^VkzDUzDXnQ$DP^=`l$$SsRBJJ5S<;-^d8VqvLOG9CJEISJ{IyZjrc#JZ0jE~Bu!_mYvk$M|zB~0QxCp6&?sok_L~eQV?%jt!IJrT-n%G|T?19reRwMd<*jL9#V^<>O<M2)@sdS`kzR4ixZ{NS!nhnowk%!vMT=abJ-kx7b@GZWuTsS*@(6|kYEwQ7~7?LOV`#{Y4>@6|N2RloGLL2VGJVMaFvcG<-#yGz?dH?F<?3Fiaq<u9qz3TL?DygeZ=Gsc(8iS6TxUPdRnx)w9CZ72ygTfIXBGkP_6`L)ladbm^?*68A*asn+m^n#!&L*-Ht`Y6sxaLoETAK~32xdJJf8RxC$1x<=|Kl}~CH5uaTyPCXh}00~wAx<hsELH}s5ibBRuF{3ev7da6ke4Rn=`>bby?-ZsLQydL5c209%WJiX9xfeR~e<b+{$28&&6lAG4P<d#Zt75ux6FsuhC|X-)3UpJ=uKwQ}_stVA!DbN|<FntxxrY<7*nICozUU#~*!RHE~iUBhVFp9wI(5j3<}<%h~MsxYv6UK6}=C-g_2w`_ox3^q)TKK7VouV^<|aH`AT?j}R<Hj2YoePV|2)t0NT<lFz_S#lS|Q*~CCXZ-xm~iAJbr6QDi#`t4iIQ}sO#rcgNiQ!`YccH{V&F9V~^&bFDPr)HVnv{9pM{H^YZ{jd5ZRqJHDhfcn2rVTTgFT9Fu4cRrmU(8TetDJ_H(63M`83PZlv1K(f1&t5E+c>6dgWEdku=28z?}2m5ktAj*dXn$VqMQ8y1K6AFsDHOCllU~Ma?i$f<sPCR?UK%zEu9B8D=l?zk~-hNdg!9xOfjsfdUEFxMGx<*T|Zcxg*ozE2rjSJ?dmC5E#6MFYF2Go%3*z;U2Aj0xXMY|pJ3&54!g?y@42nNKkmILP92kxD!Jn(p_1P?V-ga*XP;dCX}2!Z*|IQUd7PImB1}2qJhrckea@Ce!+Kh&F2V==XyK&zfTuf1JBXNIah~3XX(vxh;cMYC4s*}px!ZL!7l|oI`MI9lEJ>5J+kX+y`DAlB_tBr4lK{&UF`2hvuAppc<@&d9jgNyIBDeb3Rma^fe_hyqP0F2(Z=|*RC^$UsN^-VipG6BBUs*d+^m_CRIpI*Cx6}>}LYu(9%$k6GLc*)9n(H(9KgK929f#rw^X!j0lixnTyGg=;Mt`;Tcp0XQlw{2C>h1Y&c2!0z^zdU?<9Az$n)yh@VHn*Zz3hXAinri-$-Qi@;i+VOoRQxsC6#KPPB>ZG<2sYg#N9pmRe{54E!DR>CKA`eu}fG)pLV1|n|w3`e(pn3#Du{2fh{##kZW@mvE7LnI$KxwWl~ms3Yf`Asl3`ss&wSDW=HfNe{aJ~xHXiv=3nVQViEaQNm}rC4-!8s<|N}ZQ+5}FkrOH7`hsd5T}Gf*DVfG}{Wsh=x_ILxZ@6yuHQ4dw>>oukwrYo4BW>#k-HXOUw+j#qB#p^zcU-fGnvr~KrTR}iO&YEY4C(E~W8J)nQ}Cg5;Ba8bHrH|0Xgk}iPWjS}P1@IZH=IQrQv6+-Ndu5-c*lIfa-p;r62soJltzN#-|*a;KezzU)efCZa2^$-mOsnS6Uko_FtJC}k5$cv8}(JSl-kV-%pka(|9BHSQ7v6r`yR!+)EIq-d_AvzW(j(moMG#z0pAA+_b=Cv(ZKxup$0Ttmzj2e^2RBLsR5QMNsDT323Iw=pkbxiA_T3em|-@c<OpRk<TPO0Cc6%Ym^fzhnA#bDL3$6@SeUk#O7_A;m2QGot!+1nl7BYVwf8s>`T+)S&EGf~o~P%n1j@a~((~@4{Y@N-{R+F;=7}HIM8n(uSO{89o<xCzA%}TU2M>JDgw~j^Iga^*R#mF<j)Cp*mU#{Fl0I99MRaYfoTH*Ajp12+gJJCwNFXg=+tIX*jR~JuJgHaACqbxr)A+^?D}zSfHnG>iNu;-9vjfkv-^d5co<>cx&$kxzJ8#p5vB!kB$9&N=UC=C|<e=f8N%S>~AN<X`<iXDmIQ+SM{U33stb=)9uPfE=dR+e<8|OiteQW@iEAqc#PI5){B+O+ZS?sZWYKWWPEaIZ({NrjI_5rgwt=KaRhdMUlW@Dwn%6+;wDRD#*2vqv|Z75DOegu(g*P1?54QsLx&)9p&)GVRaGK6D<apt-E6=bToUy=kzBcYZW@F+W9dD*nxI}N3gWJbLzo$hUX=Rd?jjLu$D2J3fLx$)N=jZ|ByjJ#%Xp%9CRW1U~EF|7g7$#3;I?UMA0I#vlQ<ros)+{T>+8Z&-%gsStqIJNn8;YnPVB`4BqsQR1VtU{f2yZEj|j4mV)-!66};%=|c9{|UXCwvAi%i2j~$G>2ic`3>4*%}$-%Zw-VOx%tXKm73n>LfikMSNbpeIPp2u!);0d=VWRNNSYpEPC^_dw1`v(%o+tvfTQ@tlBodA+U8nccsg%hqj9}VCKJtZhe*{xm?-!+}Z0h;%L}{4u6Ikv1H!nXV9n$8<U5mOU*(tLr77$BH>?R()EX%Zaez5$3aM2N0c4Dd~xyC{lhw;gGpOL%-n}>5A2^q_AE(-1I%<qfby-zeJcq+Yy5pldcvotuVpxP_wm;=Q+!VqfvB?Lw!xJdlAVHgvylC&d{Wuh2qz~pgaz}2NQ)CS>y01md}Bj@8;shjAe}4|5R}P)*B2FhZDt&y6QNwBVL)3YROSUfJ-_`?5cAzJdNb)Yw~J<krDV4)_KmRp@iL|<a})iz+W?SGY2UBEuiRE9Xt+($W!rX@l%AAV7c~{>yV@KI<j7QoJpTFICjxj+1s|3r-Q52&U+lmi)w#E=33lXG-?N2r0xuNrq-2I5qfx(<XT)E`L-K2F`jSjSdu)X2EuM6rxIVm3I%l+01hY>>-hbY;p<s@9AUSORWh)`)K?5`YMf)IF!;csU&r2T}{eeBa-{e|<{%)Vim1^|{HE%urjnc|U&!3{$isSt|ZWd&IZ}GXB%RQ{!w{Cp%iI=aHOe9yiJ<t!z-iSlu_%wb{c8Ih`{@kVRvU~CKABg4;O>PBnm>4A;K#@gvVJv@901*@jDQj~GR~@#*-gqOj3~JAM%XsUJi=AESlb0X<_3_>5#p%5+_SXLbyKxdM', 'offset': (1.1, 0.57, 0.292), 'rotation_quarter_turns': 1, 'seat': 'WholeRaisedRiddleDeck'}]
floor='WholeChamferedStaggeredPreparationFloor';plate(floor,[(-2.00,-1.22),(2.05,-1.22),(2.20,-1.07),(2.20,1.40),(2.05,1.55),(-2.00,1.55),(-2.15,1.40),(-2.15,-1.07)],0,.080,'z',0,'Whole broad staggered common floor; front approach empty, no navigation claim');FEET=[floor]
deck='WholeRaisedRiddleDeck';box(deck,(.30,-.20,.060),(1.90,1.35,.300),2,'Whole broad raised deck under both entire riddle skids, no load rating');LINKS.append((deck,floor,[(1,.5,.070)]))
step='WholeLowerRightApproachStep';box(step,(1.88,-.15,.060),(2.10,.65,.180),1,'Whole lower side approach step, not ergonomic stairs');LINKS.append((step,floor,[(2.0,.2,.070)]));LINKS.append((step,deck,[(1.89,.2,.120)]))
rear='WholeLowRearPreparationBoundary';box(rear,(-2.04,1.42,.060),(2.09,1.49,.215),1,'Whole low rear boundary outside full original bounds');LINKS.append((rear,floor,[(0,1.45,.070)]))
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
FOCUS=(0,0,.93);ORTHO=5.25;WIRE_THICKNESS=.0006
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
root=bpy.data.objects.new('OneWholeFarmPreparationScene',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole horizontal bounds centre; common floor and raised rear deck support entire expeller and riddle';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
