"""Original connected waterfall composition, three complete existing module instances and zero new reusable models. Lightweight maker SELF_REVIEW; no growth simulation."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='nature-complete-upstream-waterfall-downstream-scene-01';VERSION='1.0.0';TITLE='Complete Upstream Waterfall Downstream'
DESCRIPTION='One static connected stream-height-drop scene, zero new reusable models. Three complete original module instances retain the entire original waterfall terrain/water plus two full narrow-to-wide stream modules including all bed, banks, water and inset rocks. The upstream module is rotated exactly180 degrees and raised1.10m; the downstream module remains unit scale at the original low level. Their actual narrow terrain caps and water-top edges match the original documented waterfall ports. One new scene-only continuous stepped/sloping foundation supports all actual bottom faces, including the upstream portion of the waterfall underside. All original world-space oriented geometry and per-face constant opaque PBR are retained; no rocks, banks or water are cropped or recoloured. Original normals/hierarchy are explicitly baked/recomputed by the mature importer. The original paired water-bottom V gaps of20mm remain and are disclosed: only surface continuity, not watertight joined liquid volume. No animated flow, hydrology, collision/navigation, ecology, load, scientific or safety claim. One scene, zero new model count.'
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
LOCK={'nature-waterfall-transition-01': {'bytes': 21032, 'sha256': '1c8ab8375235ca3a420a126ad82f18fd25b95ea07097ee899247cf5282c44fb1'}, 'nature-stream-width-transition-01': {'bytes': 29420, 'sha256': '7c9fddba4d30286617458bdc7ba3e379a3a7c513aeef98bd803de99315974c83'}}
ENCODED={'nature-waterfall-transition-01': 'c-qBUdzc&5bw6MX#+XOI1TYV8Wa8McE9Rw<W{qdS_WA+FkM-i`8d<y2?h0$AMbhrtxZ4l{p%5qL;U+*rOE4v+p(Z4xbpn>a<WayTaS1gc<Uv9x1==R*_vH&DfAn|fvATN9XvXU=c)xr6n>**6d(OFc=A3&q{h6-C#}m<<PNL=K6J51t<%%7lM4^x>hT3<8`cv6dK2gl&L+zof2lBaWuF%pCk(LFSR5qE)w=BDCWy^>XmcvRk)EXK|<qPRt7R*vu2#vLd3cXMeY8Px&2(@q85y~b8(HB}{-fInIb4l}tw0UfE<!VPLwXK*>6qpsgxxt}aHkB>L^SKNY?agJ2>FjWBxDfA2CF6-~GTxKOZY{7O2UCRsb3}WXb%|ms-<QZ_;tR*6x>EUkBAo@h-(d>HL^0hPA7#p5^YBoim`^1Jt&aGO@xf5L7?#x5P%<}~t-mLPMRqTr8?rdX)=)k*lu7ia;)9GUoyf$~2<Q-tYPOi!9%?V<hf@gKFl+~xZA!YhJ)X;Ew#O62I1Eqavk)B0<%<PNVBCMP+W$4Sn$BUUK{s=}cOacf=2MuhO+u@P&{ra1&VM|egm^Yl9L}fOMx7|OfhSu?7ctFkf{0M$^6CCGoAO2Dp11TQ3aJ)MFRofP&KKsj^ks6RZHaB^Ld*JjEd%NPftGYOlPb2XpWnuG*wGzH7lz>vbI|c0!>315@w~a(%qZj&y;z!|9o?ZsGBL#Nc8A(qU|J#7+R|-JBC{{s->^TIkDE)Z`sViDOsWt^=yT~pwZ2pq-kDw9p@kb3F7H^=9b)~3#NbfIQX@(+)>9mS?@6;q;jZI@7|xPkylj2PB1?QEof?g265HVvH|i#H*v(@I37b^j-%W6st?_tYE?0~fh7!H-Fh0nngs{p~viY{gaaN}_R4$W@XA}8+Zq!^USZ4@#7K<UDV`0x_u|)HUBomdxq9R5#NsY*nm=@J!PkD1CWGoe?A)DHy))t|)1?zjWDLGsmP2`htu;WEiv{=NjU@{3N3!Z^&D!$E<x9)X^@`+LV;TcUQivy0AQOOLe_3Xxnvuxbn#87<ujrQ<Nc|>x?=dLv8vi>Tnm{*8lj9to_eJOLS_LUT2S5>!a?(jOQMyndE%1F*eGa#1VJ-K2rH)wk2#6}2fS{=hkydNy1X#|N)lN~5Qs$;Z6#Kx)IE9R<#2WM2%8`XBrx!OF|+7e*-RbGLC7oZSu!AaawYP8xs7TYmeYlt?t)^NqGuG%Y=Uu!~G;#Su<t9>O_)|zvx<_@o;YP71ss*L1p^jvGlWT~-Xnk+Sz6)Q{4yh07Yl6Y<IUYbJAD0Ypfo)9Y)oXlyJ3(4GYPbRe{olGSw$-~sLJk_7*-QJPN7YEpjwI_c~stBFw-p<@`{{X5IGv~3KwJ?{-<rm|H%L*Q5mSFx9MNJYkDW<8d%v7sSk%fpTD$xk~#F)hx6(dq45|yK7J{`1&aTKB^$vY#C_l0AU#{R`*Srk-Fi;S_{?C#9ERIxMHyEULAQq(e9h)S^-JTM&*Eu$qlriigf3|&&J%3&>l8=9p}QYA?h6gk?&jfKO-1?UXug<xB(#bC80DJ=9++vI30Cd!&@_6eHxPZ4AdsVox255<~}m=M)4pH1AbmexAEDh%R_5RKIN(#Stawp~%-M@-a$EG@}izls=zx`-$@@n$j8ne9IscSOaCTO=k$)u<ASHeO(|Y<V4%6-A8*QXp?)RwP6<5|I@x+RU3(xm@O`T(M_CR5UyYswlBph}iB)vZzWiWn#}t-P1T`zRpm%SMQL#wl44~pB_xJ`qz?46pQ(E&u}qiI<{)%nq^(fR<1BjSh2G6nk$!MQ-C)sb{Xkj#v@f;pkQL5bkiVLG$_1=2(Ll((x6r}M0pJ{UV}8Ynd$J_w)l2h<D3@w5k-+7QuZ<$6JJpxS1D0=C5oq#2&Y7?QWE8rM8?eBZ=x6X3c0-HUC(e|Un;*ATLp6($M>gQ+lLUMh{*Pvy*b1N!9xaxx^0jXTTy6gRm)XkUDmpmW1^yJQ7Ot+9NV{{I%ySJ+Zr+y&4EH|I~L03mXS9|^kI;fywpfu9+#K3iu{^|S1!M@vrdETZ2{bILV{|@ezz)7H6}-~85hHf^%P1mRTLyiV|hFlt>&u4h}BbONTaHV*RUcXXee+jb~zGNrD#mmTH6}x@Ct+C!wE0>h<6yph|nyIs<#E|UwUCho7>|h9%~X1_V9WKMDx9_SVW|V6%qj%T8gMF%S9qpnV~8mjTcS5gy*9tOmNYNVv``LQnMh5lD7@9%Cjekb~zS_NSYcERi$y*l<Lw;Q258MQQ2MJ*Vb5zXDsBVj(CbIO+wi`k`ZqMlu9J)i^0Z$aa({5=Ynl1tv*$e<fw#z1YePAQy)CVquxQRPX(~2qJYnqW~S`fUQ8`dW&5$=YnNiOWc94<>obqF*~5{@_cMq(Qk5#!_z<>w{K`kQ8u5s#D%Ik$hqx#SLbbfAL{$I7*ULxMAo6mpcq~>cE(h^m6N8LiFRm%E0COkBs>M-nE5byAkA0;Yn@IFUNerSu#tyJrUY2X+y*ywgRJFLO1z5cG;@D#ch<}~&u~>k$uhh<-tO)@|Zy+A*$*B=nP|?*IKmHQ3UqHOPBB0#gJob!Av|!l^BD$%3=-^JHd)EP@7QeUpUSF8#8Bg4~@8?bNt?xcz?3f<*#6%Ao_uqG)?uFU7K5@wl+d4h5ZClw3+dg_?J626GV(y9UxvRo`eY0^*#O8}(XYLwdHW#(nnIkXk%#jy%=BO4s^WuU_wb+S&Ep}q=g`JptVJGH|uoF)n+p$I8z7p%-chUEZMwrF97C$`nvxa!rfo~bIEZ5;b%z2vOaxL!bd&_Wa;IU(8BMjTB@ZKefk}Th2+S~{;+iLNy1Ftm1NA`T(w7C}BzLaY*i$Ali7TaSr#5FdTrykjJIh%_e(_b<ee&fd7x*t6A))zhTp@WYZ&2aaw1+bx`4tMUmj^T1Get2j<ll8>54NWn8@x*pa%DWB>>kKb_<29oeV;#&7ir-uPs&9N`&yW!W-}>%hoyDsbFMZ<!hRd~h$MnxLS>M>UEf9w9zOfzKD%`p6BExwP*J38?2ebFB7oK`#mJtM7>m=-n@4xRnoxPK5F&ozdmuj&sTZiqj%3j#E**CUh(iF4zi5GU>?L0<q9iO{e?95j)Y}Y)l*qI|Q?97oDcIL|qJ9Fm)m%Okur(W2ZQ!nhyqZfAOu^D#e%MCY}Q!}4i|8BBt&f0$#FZch1cs{sctFdy@^QBszN<Yz*=#X*qaZi+7^pySb94njcv2+)kbuS)XcZL6`ZT89I<!>Y3{q;L@^y@h<J{2AtG``(ZF1gKJEl=aQbMwoeJ(ZX@o{O*E)=_%z<N@P<2cFU0=E94o!MMKqZ+T>=zIXOWUA+1Joj-a=|L$*ljf2lVQWYz={&`<}T;F|1+$bp3e!2ArwTH)3c8?g7AG}@n>gVm;d1t~H+W3kt{4rT_>*wvf<hBjQ?_PRG-`#qv?$#gFp5tGC*<4TaPD>kisjbGI>*r6H=Qn3|8}HJq`n;R&sq)1S5AVy)+(zS%_r9WkM|x0q>*sWqec0xUhsWXf-!$)s-%lF6{rr01d3gO3;eY?tZTif^8;vc8-zo9@eB9jld7j-jzonmBT4bz#?(M3$aXQOxJbWBn>@U06ADEx#sn=ua;^W}<uA3;2^G<e)zuSA8=l`(Y+x$Gby|>-w-OV<hKPZn&zftdB!@6QZJY2nG_^6i*AN7*qqpp~c&0H;H_^6i*ANA7F+U%33(*JS#1RaOJ6X+!TO{G)ucLtqBAEoo?0`#0};tOadcuq3$ObP)r6oNF9W$54Nd-N{;{)^ti->>PH`1={XMn~w!bQnFqH1T122|RC^_$7J~n4uRT&14xOnnQCz=hE>si7ug5&{jH;Cex+V2HHkb=wu3$04mTaG>t@3KovTjP9vEjpb`2Aok=RiKx1?^O{XYnpc<V+=TbXe4thDAPcvv98K4GTL>H1ySAt$iE%Y&3K#M>Z(Zw{27E%Xj2hD~xi)kt7Qdo2uT}{`3UPBVir<JrCbTwT8$xiA5?Sk|YT1)Fe*V8h(iZ)U=Xg4jV6?7eK0o_8YXbtsH5;RHI(mEQTt)N?J18t%#-2i$6ZKgQosR&x61ohH3+5x(QQq)JEq)&r>n$pxyH`8Z8KSS43hHj(Jf_|2AG)Q;Q=RiM4LsXz$bT{bTG)yCO4}B5zi?p3a=?io}=>2pf{S|$Q9sqrS#^|r<@981Xhv-vu6Mcmq27Q=rp<C%6=uyx|>2~@X`bT;U^fB5=pQnGNr$C>gyXa2(4wXPl^tZH|_R}+<&(OVeA3aOYfj&oHroW@_()U5XPY*)-59kHZ7cjyedY%q~9;8R;t8|Ed2>L_%C;A%wh+YPLnfB5@)4$Uzps&#5^mY0V`U&Vy=o|C|y-Gg?{V9Euo}}057ofkOf1z*D&*@j7zoKu`K6-=R1bvg9hGoB@w?W^Ab!GZbdI$6!IzS)R`L@^jFyo(kWRLC_vvH3Cm;7RTEZ?}%`L@@2^3pf%H*NEa*;(;X;F4c#kL4RTIuG|cPnP9x>eKiBK=+H;xyn)Cl3#3(<r_CT5BECnWoJk1oYyb5&R_%Ml3#3(<r_CTul}&kSF>OE#?#$@$`~82eYSMr+dJp8-2P<plU4nEO~CWG^cy_Ze*5hHJ681>hm_ZJ9?xk1ls<E2kMYv77fSVGS@i}#mLGmMJL~uL^|cOfvl~Cpllh<9^(XFGYdrq^@2mWB>*wwN^Mai5c<D}k&!4)h?B{vrcJDIlKdh0m8$WL+&(H63dHY@X4L5$?7oPvmGqxIYX5OuzwRUHfzkL7mbC(#;F8`f=!Bao3@|U+0`##;-_XXv5+t>4Ua{NY6{wMG3Fti7b=zsp;|Em0Q>*wu1@Y??Ui|$Gok8b_%lADh_5B5!^>V4Bq&VIR}zdra47k*bC4=+&nzuUgv*l^brgXeeS;qCY1i;sT8%?7@oP`jUw{?k$CABSDWnV@H47cvR8``Mspqt-vs+=ZNob`q-o^HH5oK|2|{l#5WEPenTom46GW^l4~p*Ya`f8_q&I2i5)@RO!>v&P9dahP}cJG`5eCu^X6)HVeBJ1^a^#+HCBC*k0fhXqTeGzZ{kPC1_z(_^kfF3{6C(zZjLggr;JTu@tp`1Wm(^Vg;)Hb~N4G1$2RSVJEQwHT`<f_2yn+BdYl&Xjft9(2X6y)o3fR8({VQax}IV*n-^v+Yzk8&VkkXYtc5ieZy1t?S~t7`wpbR_a2_#ML55qxM8c_BXYiraKp#yJBnlRT?A*FD`xeZW4{+ZR^L|~i|-{k+gx$&Hx*vrS2X%A!s~m6+V2y5e5>I08@k(XvgOx*Unrldf64TR$9x@uT)*GR^*j&X?*o_Ju*+EGdVA`B$KuDTsZWkYe*-&@uHVf^H@}dJOHMB4d5%$knd>i4q~FD6w|*laF1ukr<4y##e0qX;rbo!6XCSXmLSy-KIx;HDsw|(fyf_7o<x`dyr=m?mR=x;1`4lrRpN8Bz3v?E8@>%9d;aO;BBfHK;mOKaTJY?lIWXJQ-E`+3joXm3b>By=wvMbB57bCkykTGYY%|TX;BHvzu){5+^A?t?GL`b$HvkGV*1DcNv%+Bf9*_vTyRUKCba_SYJSK#X5p)oTz;XSSUz$G`#Vzzh5SNvk#4LiBgCoXwmXIvjxcf(xn3yMpAF&oP#*4;3d%Yx#PU;KwTU-rT}kDdI5dLk$;`Nh^;xniBi&Kbp_gVT(Fxa=2CJu*x8i48aGoL4Zrec+N8W;%Uh-3{XzA0O8TF1ca*+a%p5*4=UATsbm0RzBy@86}tBas2QY9y~?>9<Q3jPYqCeZsS!a7+&>{n?1KYva_^z_DI<)R{Xe4_$O>9ub;00rtBUmPk!+By7_Y9FT3%()Ge;HN6q&h<vrKWFWcuN<NA4>HQ!eR;&&UDkFnb~82nf+{I0gS{eJD^8-@mU)~`30Zw$(Ab_V=yJ;*l?&a-d$ct03E-VcV4_ro~PDX0x6gHA>rxREx~7SJu!YgUzKfS!RGa}sJvtF}Dd{Oy?4l^;cocrxUtflfoM$bL<}5cERSiXTD!83GNVMr6MqUkrLN>b-MNW6l7bfg1CCRH2uGUW!Wd0@R;j&@k%7S*TZMgU&{cI2Sdi2CAX1WWU6=gSMl(6j5JF<~hyf=E+V6Xa{P>C@RdQpi5~HDoGjj<9xKMQAIAGRiLZr8d^w8s0*}<R-30hYeCo28oCPg<_gdiv<_UWs2jAKHqc7yG|z9YqfOviYoFW1=~`M&>&<hY1i95hM^lqDsuSG4XAAl*nHwg14{?I|Tl{3q?j*Dm$;}?Ont?yV^n=;Blgz!#@$~<bX=U*', 'nature-stream-width-transition-01': 'c-qBV31AdOy6$j?BM^}QMnVV#Ig-%#0huZRK~V%DAOhjVA(@0oG7~2g!eKTd;<2I}iz|3@h{&n#zFk&Hx8Sj^ipQdhh$riM;w`TF^!fhknIzSd)J%`#`Vyx2ruwg{|Nr~Hs=8BAHEVJQj^j=RIc|W;aTgX%pSB{$TU+Z3<&0gCQ{nUbg5FRdm@_u#qD8@gKTw-p0YkDURQdd6zF_v0G1Ie`$OTe?tmWk8Eb#?vD+7KY77O^ChP<5GQkWoTEFVF&Ib-Lq$nkrtp)aS%zLuBc50u##^aTwITEDHx@huGny|sjk(m-`h!0+>iN`iqZGIXKWznDy4?W<j6&mNg_0`!+m3j{-p;A#Rh2+kRb0(I_Y09?8lM5wK+sex5}WhD!jMNbl0LUb%K6ULSB!Y{mr)Xo}WvTHP}GqQ%<&KlA$yoS=w8gjffDuRJJKTPT?Yn@1Koe0*O81RQG{dIx5+VgGNcr(^}L%twzZ2w<UTNf<%mikJTmsEqv6$mhQRlr|S8LBI*^n0sHYO4Y@#MBGG9D}}^DneULMpnYbN^q7M;xYbE6-XTl*7;hP)LNLFL&%FF>&&bJZlRknS-PmQsx0UO$C}UQ33+0klqcsYd1{^p9@8p;?Y1SAWiXZB8>$QX@@qpupSL={zOpQ|C?ClDwUr@o(0nkxyqrL=vZB%-R!(*uap&5~GG8{hC5+0;p6B7o?FxBAm8B(1Dr@UNj)1?JeZq98a*3}bXa|ClQc!NtTMAJlXGL+2x6E5Zt`_Hv%`W#=)xvbeVFeQg{1xr?2ZANG_d72xE3NX?mVo90m9@_Ke4u^5-Bp}3aqh&alZuLSNPn%jx~3{TjUeizC$tFEP-geY)c2BVSS~z%@|4RaofjUyq|#SkQsrF+LQ$*Ex0hYe04gEoOUpYS1hy@_JP-(#*t#yMCS&*ll}u<~s|g0mE30giC|v{sRrxBsrOSXCh?kcH%FD^Ei;UupmSGT4LH$6#Y<c)9tkvo=He>Vo0x8cPwIDCM`HP^0zo<I-Cfb*T0;QEM@<o*wEFg=uhLiA|`3~azR%-IiIc>gU{rpx27Btvmfaiq*H6_cP(h-vntKRPo1_SkB-2(&l-XIL{`XTj%Y+mvOm=FHhe1c#3eI-l7bCD~>IYDoIN!Udf2FjK>^{<J9qWNkl6sRr%a|L&#wJo%viQ+YUt+Xmo3$m1YYnsWL+29Kdiq0XdptfFUb1&!H+EQ(Gsgax4{EaA&WmiIh{Oj12M%$IvYF9!5@31R_wkso!T^SC$GAO%pPMhyoKfjd$mv#jT^RcapX;g7+3OwQ0u&Ja>N^_W$)@o7<NNQ{@zwFd7he$T7B{AfX60A9Eh0CzAK;6PBUlAy?tTpo6GfcHjZIYMdZitEtgBSZk-m0p~(wTv}ibYWE*-2@kx7If?P!$MHhG<C&Nn+)^{UZp5$Qz<=sCmTl!+o;ED}o?v3iJtjm{1cGQBgEW%M%EHk!6}EBnh{9#g@JTT{Os#E=dBf8ivw95-D4l^B`&b98pBU2(P2_ngNUg*P<kc`($1+6iKlqkrZ1JMN(xM#F7$_1e9cJMpbnKG#5{jiFF}J=!uFERx~dfIxkA1C=;Hw$ZgVeU62gP?&FOp*%FXLc4#V&7)2o{#>j<4ZL1wSl6i$TID?p*7M4R1B|#N+IT6c>TEUGVvjQ~<${~kW;dM!tRfQKdU|Qj2C)4eb{l^3e`}>?oRh)<{yr#6VuJ$ZWlp@BZf@SG~k%%y2B&f)O2Gc2m)L_RlD6yT}PHMveLIf+TD@mamCh>+s!ODeoA)hVDCDV(h%$hQNn!Vz*=`$}LKNYr$5J91uCqdWV)HMf7AR^jh%^<bTAk#A_^bA6*8PwJpG<pV|o<VF_K;~$>nRP9yL5a%K>j;8tVFi(zL~=|byOvi_s7X}EBwB2dn>W|4WfpX5DZ_Dtd3q@+7Qdp<I*BMcCXwh#WCp*Ydw#)JT9;BBOR4Vp)u>5y$0UXuekJ$(N|gUd4hND%*ZfM93rP+ik`y=m$_emG`I_W#Hc5BSFXc(H!;@qo2EXl{Q@CbarW{XpIG!xK_FkECJlWxRatz07_w2$w<CF)=4i8iu9;h_fhlJizxK<koh9_NES6=Q5UJBcGJ5slt<IGw{4rCO8I7KNa687q<?H@~F7%9|LP0$TlmIO$Cf&qKl{B}xHl0?WU3E78|;yrv_QZ!Z6bk)d%U5g&hTAC_A(vn3O5we%gxpdOR@Yxv6q7a|OSi{BkhD$BO1zv0!Uo>(2)bTUh%pk>PKyOwN6c>`C{w66};#HzE$gi5A!PbJPOqA)mj+a|iMotRaOd*7e0bVgwUWRg5CpzTAlepBO99M)`qm?)+jH^L4_VNNxTUk3M^J|!y7N5sh!}ZuYA}J`gj*Nsn(clFMTu_8fn<Rs{?MWL`KkchDrXTXjIiesW?TLbzlq-@dSAfj`=s@KqaK`rBC^1iL-<xBqK}yOO1vyz~6qMw=@z*dlH92P#v}C<e&|`C;2+c|YOA&R2H*`bbB?&fDs_meX%o`HyF-1X8G_qYT5DY;z6vzacq{^`Kq-{+TL|#%gQP&m778<cDQIW|pjIQaTK+KKo%QaasL|Flo6C_y|wRmbY;tLTob@H**s0;DbD8@<Nf)P)R8fZiW7X$}`CXO0a@KeaQqNr=4pbAF#D8mp1QRFqvkfD4bY6Jpagnl0O@sg;=^H@=gFGS4oQfxJnN<EGm<K*vfp&1T*Bn0W2EP`a3#1kcgN>p7S!AVmMO(3=i0Z>+CSpy>zbaG%E(IGjX6T#?s2$FD}2QAu1jS{F&5=4!}I042>5J+_i6sUqy6;Y3;K_x!_F~_U1HK-|ZH5ezohxeSnj0QzPQWXK>pbl9E29kp)A*?|izQRR?s1WQAM(UcRYrL++)1V%o|Cr;AI5ud+t%7;C5fO5L2*F;2+@L7nv;xRTlnAlk;32pf5W}Eyv8z~K6Tw?SRf+@-uG7v8`wT_l1x+?!5=F9)Q=!!)xGA7EQRm_IkVzyJ79i)uvaZ18c*#W)l8cIxm~2#(B)3tKsY*qGvI8QV3|<)75X4fYKr#swH1H8*omix-!%$I!>QRHMP~8wk!U{aZU|En!E{bQ9lAK&zl$2!SqNFAe7kO2bMP7%T0qI4ub)cw{Dnb<vn$t90A{z}&(*!}&M51aaSTxG9B}IkksFD24lW1r^rjRv-*9FMP3i!8V8?^v83={~r%n*!tp;6M33yqSVY-p5>1VUr-N`wF^YY+w%2nB*{kYjpC!L}BmI#fl-__jGKims>vSgZ<#kSfL7;PT1EM_EWVKFVUUWwjB0GzKM%E<=vcU2JjN84^=UDY?2@mXock<v5jqlAM-)j!xA09K{?TXRo2h*GZh*t~zuAG1~r7WpEWJHAp&$bitk!_PA<%!)bR&Od*Z<EXF)R;^Xc8^)^}pmRhHvPcH3K%Z1BAzNtQcMToo+W{BaA>Gtaz_VtiASV5o!X;N%uC;nKw!|iC1mz|?wM=U#sOEHEUYSd^=*WEAPX0#r?c1+fzIX86PJ?DbRJBLG=lEC6^hYMl?!->Z@MvHO+T5og9MKO_k-e$POC#3gilY#nQ{rM&%^E&_YO-2@?*G|M_WXSnRn2anMY7!<R%YypzO-5Fv1hlRSV)XDt?s=Qxija`#YV>fO*WEKOiczvFhL%W-iyp3muO}dTl*vKfN`QAom7|9zqPaH1p@2<*cR`7=Imn<11R7C`l3mjha<}N=<X9$wI2Co<V7sR$Vez`m>q%I=!Hawn77xsdNm#t0C1N#gh6_BONP3Dkd4U%dF$tR&cqtL(wKG1U%Ak$a3j%r6@$=1I5Y$8>Mmyv6MEoY&@C8v&lF3toC`w`yi3$qcMEq86!@itInzdE!9Iqr|J#EKJLSn8P%|C2Y5~wV-HtLh~M5^Mp<7G9G$VHC4qe}XA0%yzSB(gDaxQ`-}msGM36mr~zDbqNPyV^Q6<ACS(&6~|=eEa5sC?0-i`9`$j%mOPG?tW}2=D5dVVzO>DCgTY%FW+HCW5Po`{G<Q(z^7rw!lBF0!IJd2YfN~E#%m9sZVL1Eo*9k9{ItcBhTH|X+=|ANQ}XcI!>_o;WUXlY&4||#!7~qJwZVjkc=+BKcOpqz6%!BWJ`#g0u5m;s4h;7ihjl2m!Gxc9nAq5rp5MmA#Kt7)tC%>vt`pbYa1YoZ$GxdHVq%kA<mbrv4xY*@Yw(*X`w@%A5;qqv^k0EbE<1u~dKL}L(-fJ<qG@9Ex2(Hva0w!K*70SS#T!k-;w}F#k9lgn75I`rzk+BQx}WA}%e<>if;~s;Eml9h?m^);8<*S~!mNIJt<Gg{cz)Vfj_>&KABffeyK5KQYxN$w%&{)3-<+Lhul3@p2FJRO|FppK{J8<#yVD<$8=B6y?eYwmU5Teme%`?ktAE|+yv>6#{3-`;tbUpYVw27Hoy8}MhUSN+VfEAeu==}mJ-HP4?ZkD3wky}2GdPty7k&{}2yG#J=eS;6A87k<9k~u%Z>}%2eYq}NXYLHHAGH0rZd@wYpBo76K&}Uu#$|GYpdG}eb7yjcxgpRF;WD@Z+%Rr9w8OcxxU;zt+-PV=b6H$ASHSVm@>~u#loL4_TA9n`&fyeJhgRoCaU(g68w>4NE|1IS#&I5KJ=_>h;4n8H+VPykvGPTtahnxCuleF0k90>3{`a_Dh=s2hZ+f=*19<GK`<VSK%z<7zfu1|To#+Vq?FwyI&~JM=os~~n`HPiD*m3)-NPKFIQ@<8YvF$8{BY*qe5#;X#Z72BF8MHyHu8VE0sbF<o;nRiI4~oW-+9oEB)HXO4j?^|Wapb-@Fm;bmG>+J6Ok6c%8?j*=3-5U;pVTw1al}p>n6eoZjU)cj20vWCgZK-M#tnOTQqQ=?5&Lvt%2wOph;PQk8>HV8pN)yr|0kE!Gp=z&Ck{;cP8%GlZDQg`Z4(nmYMYoi;<FA+)eNk9!<zi*$B$&C_;Ifd2ThuW?tfv%yrv(9UV&$-M;tVCKUFheM$Lm+JW%z6#p<W|xv=h-XMA=A?!V*}lf@@Z!{U>wB`~X>=7FjoELK0g?&{)f^l6?CpLgdgCaa&S6CCTZ`l&j>vF;Ur8RPM6sKICN-D|p`sc2Z`S+c7VKXLQ(4t`kuRL$Vvjnz-{K-V5DK3Oz0KQs-ipXP_vp8_>ccgP(i&vv)#o^zq*F`(8#fDF6t;p|EWWP#d;<e<LL_Jw+;3uK%OXfvRuNrhS`T=VpYYNt=6=E=0Hq9M=@f!b#P)H>msXBbpFS&^D&1XMdYk(#Ffs-4_O%_Bm!Gb&Q^C{XR>MQR=ms+}>Bnr9qTJ5r?P!5k}JBpSC_@$-|lhdqbXD%^XDWwP*%^G|y|9_h#LEP068&%&HtdvbPu?`UWEj&_!BFQ>EeDJy@m@(4R_e}(`5Y9209^K`VUpK#67*{*)VHBVPtFX5UemCHSHpZUMHu0y9UDa9=O)ZOoyKU7?UUfPG5_=?4u)`Ow-$h_o2ChmTLYNegJ8EyNqnu(uTKibOdwhDdLcO4TyR+wUqT=+Zm@~B&xc<Z4ib5Pft&}V<Xk%_PRcD?!R!Z*<7em*ANU3AR+oBRU$@N47>-?K5pY8d|}Dw%zuD}2{X$vSc1HMD+ZjVoO7`Z?AIFTa2;@Bcd{UNhvh`AxywX!(ts92noe+x+P0F|>Hf8V7#p__OAwcZc9PW#xGA@XyUnN6x}u1ZFz$h#S+aFN$)oUUr!Sr*9l&ZCRU*xBpj_125Xx-@1QLCe9sqEq-%dcHvFmH(KVssf7ohLwL@uxh8z9xp`OOa{o&6H~YPaMKf^0)n@+*9X$IVthZ<yy1!%Zsn)ix&wFN94RFxV{qt^FW}V+-ndiFu=R4LKBh5Bz`*$;Eq%XxR8ZN6de*EHqiHc@onw~{N%ayf#2!40i(})j_wpg;WXimJKnGd1O=&bhx4n45?U%Py=rChrfz0)P#p%YgB@>;LeQ2ioOGM6G+c3MUj4NE6(^gv@;78=t$)0pOm#vJ6y-tgNKVp=N1Hxm6gyC)S8$qfUc9SHfB<c2}ek__7o^7asDNrolo4a1=w4jHr;Watslj(}|22lDkuXh%XeJrg2oe`xzdcI^k*I1k!9$iw6uq5#?g$gEj*HqL_27|6}Jkc)HRBLFvaT=}K^mF2rEAEo`0#<Q)T%zYOQ#ZR1hJrkdtc-$N@XfUqdeKiw*_VFD2W8c&0frHCX{`p(X>gT&+dFd4Fy}S!PI=2g+w`MeE_0wZ%{P<0`9Q@;_jrip!>JBD~S!=nWVexQ=ojXbP><+)gZqmT|y4lv0W}iCrhL+eO$-jM|?E|(%&R@bAI33V^axQ-TY!m%^{65UWQ#zbNDgGu@nX!|Jw`Sgk-W~WXn(W`l#Cy}{p^}FlMW6Swn0Uz6{YV(`7%KK2VdA30UGSaLpFw$(o@3%=za5Py{p&C2NZ&(DoSQiYzZ~j}Z$7z?i8o8%p^8DBarFf|UE$U9??#t>)dPQ%zTXwTaqmKufji;VCmv(sRhti>#^qh`17luvVB`8UEZ@=t-}=+@4!rWDf>Y;q#M?SQ?!Z@0J_Fx&MFBps=pkIZ|1&hQZvme6^<D=)J@he@`Js$=uYAaXr*GVej?4M@*o%+g2X0u2*4>lZ^oP~;)+JYm@QxF8=Iw6?=2cra96bF+qcyZ_R3S}6_orvyVvcI6@>Kk$j@kdGr{`K*Lr-~joZHDkGxhr6R^?Y|O*6($z%<RMpBg=ztW5KttFFQ<dYa~gSzn?@o+>t<+A+^TPxrIry7!GbG<wx~H0Pdbi=_t^P5P{mIkl-2?f>aYi<Xzwzj4<L>)9t>Lh_y?CM_>57mJ3L*Nq-nveUBA*ugV}X?|$j0kTy({Pv3E#ZLAPiS(q}`=ySM6S;QsVh_k#-QY9Wj%mZ79R_)=Cq%VeXmcS)_JNpp4z%Y$#_S96u0OQ>A!CxfNU|e2YbSXz586EYe0~Vz$1FQXavbgJ|7o9N`5(*AX#CMzN6>_tF?iEI4m0sRMhgD-DjC;mY`p95{qVEX^6;x)KFY+my>KyZnv#L}HHVu%-kNR|9_WQ@AI`+z-^Df6SEb_h|Cod6{u?s7;SWz_;BA(ZhVG~5{Pc{Do&iT2@f{_b4zl`Lm|mCeXYoeUu=r%r(7c^#XH}AAd%|y;ZMkRKJv{-DT-yg)l3zR6rz_-%Qg3^&+Yj1)9Ld!j*g84q&j8e2_^Ro_g}YI~(|auz)~0PR&7%j<E^$8-pZxBGnR@d9^rW(#iF3bx-IN2n(emRrGx4Z@tuZr(KZ<5>*D`Vc?WdZ)f8xK<RD1&ye{f{S!LJwYK{vg9I}<;9$G)b9G2fzdx9oL=<=pGdNiTN5XXoyBg?oJWiuv)L4)~JNZLaXqPRGoY!f(;cB{wm#IDe%X{H`P3cj{^fuG@Tn(?2gr!B+ih2ma`bZH0%%e20#eZ)V~hpAR*sy(Zw_Z@=Gx|M1#M^OX%c-Wb^Fz=O`-Z7vV!xcGvt4m@G!Zgbt+0zP#3R_op#$C_&9iMTB7F6)6At3CRSCmy}7w$aLXcLu&SLo;g&dsx?8{;z}Aywzxp`*d+3O+)u@|9c1PmXmjSrsmCO_P;x}(du~MZqL3yy`<AL)BB$=ciy$N$y!m4X`1!b<I&mQk2O!E)MFMsP4nKx7vUcFtui0^rl*6R?sp^C`kDXq>?&T4rf*(iz4OFGyyclE(I=fdIdsCJ|7!V9=12Se2<@G1(XzApw_H+X9lG-{n*E&LL(5Lf$fBWTccT+p7M4y}va@8QG0i89>3Q7d^?r6<&w@4!axuy4L!liCxt!$nTxfG4FO$4J9NOXbe)o)){VvJt1E3`tJp=N1KD7Ce%gJ;3G0={IY(5yO1OZwBcDy5?0?30l4|cp9_e=RP%STzhNaJBU8qAb~2L1r8W8$+ibIjTv8oukE4NOe?H;t=uPMhkNAEBjpU_5wfG3v4LTQu^+%P_0|?$s0UPapk=E>Mmk8c*|0^}M>N5jPxo>7W}-&rkQWcwo`6c%b{!Bd5mQY+DQOchl{jR6yjsxtINJM|a2Gx0C%|M<@7@cRs$kuMckgya&4f^cstWyT5P}^_o8lUDt3E6JO{36RN)=4ZZ*6QYOy5{bjWJWFPeS;Mq((S53wFACE+P9-GR<AFeqEXZ?_h>UPg(;tdav#@F4Lfi^v|l8L{3tv~Mh<OWo9XpJj8?)WKG^!*m}X2DIa@cQXZs9T4PXz{ouOnm6RH&7pRE1LS=bO-MDUT<7_cnjjcnC!sQih2C{Gwabs?_cV`7d$89b?KW>$EK^9`1pNkcu4JQ=%V4*JMfhke~%XJ{181*be#iFs(J?vdhi4~{mKe!%d>;<cIz!P;q|MnGqZ-_Q)TZp?VmfrN?UWw!M~kuwBEeyym2o-^KjF!qi+^o`N?mX{XN!Cw;CEh^8E0{84en{Kd^bRHDh?0XA6D`(KJWjUSf9q=4jKfZuOX^+4uBc(cB5s&38WcVHQ12v#0Y?yz&FTxu|@Xho-0HV$pndemY(`@gVxcrb34vuK4YVM=zbf77agCXVLPq`hU}FnkALqg^qlY;?N1JpO)8+9^A;zl7&S>%R*zCXByLEQ=;->NBi_QoEO8-!_I>CEXZild9nE%nB>Kw&<>64cZWec400Sf2Oa_K2*{XcKt#)cHUn}bd0%Zbw4)(MlDwD?Z9Zhc;gEYrLOT+2B**=yeUas7v~SV)ua|v^hMjsHWj$5F#79?j$4hHIL_hW`W#WO$GV$k2kE3g97BeyJ(=>kfvl&*u;h&&YefOZWkM^5ga?|l8J29sF-|5WZbDug3ulREorfKN@tt*Of&5<4$Uz&z!+~w;Z3)j5Wi2wNIgO9Q>y%yci;)kYT@y4QI@kaOei)7jE_I|fF*cf>Wfb{gVt*(QeanrzF$uo^~+qUU93;Ni(y7|oluI2f6@!G={g<GC~uRZ*vMd6m`-=}80YEii5nfK$TKd>m=^2{4(Eebb3|Hjnw>0b$_*iU|luZQ0R=wLtl?qvIWC;QoV7rS!lV!!#<{M?-A#09ou;db=w(0R1}$ylOu7ubr0+qsX9dm4Rz$yjnvU0^E~ZpTg>HWO_>_It=+GcK?d3%6s34x5a&&#<meyTMj0+>V_`*?b%Ow_?4!#-MTgu74tPI^O+at?TC9eK&Km-Z^8?xOzw5&77=v$QU%P-nn-(C;PpzxHMLR{W#TrlRMRpYvjGI0=vH8?TFXB3nQnWee5TXX%OL3AXkw3<_x&f3+j~a_7m*hkT)`+&4lWuFXWaCXfvRCA<wqM@7ZVB@0{gAOHTXGhAfl~Z8lUq<RpKz{SMj)sEdZ#&$-7y%`+UTr%}+3;skDcO@kHo{R7AaHd#3GZZvX<5eqlRzyn!Ny1`~FOy+cn5eqlR#^SXdunTO(!emaD7_)G5%p~uryTDc~Oy+cnF$;qY;INDn++d4^BkwmOml(5gt1nMX+1j-9Z;w2>UTDNisvE5SNBWr2v6rH;+M&TegT~ET<UM1v`ERIL{7^I&iys#>%(dwLgTifQ^WRD_Xe^4xu~vdK%(XVH?QOpQ%Fx0q>l)n9FxN_uhPf8pN8EfLX?hnlj<u4Y!6YYihO9vHh``C51}*u^D9%2?<02<`T_G!UitH*<Ap>-=pQw>@zFu}V$*}h*nb2lJo(TVyRyusnrrur7vfpYRXz!DAfGQI*$N=~ZgKU!x8Eg=IM%p=rygQW-*<+~vuJcg%i~*{1I0;(GK3yKo>ClpQnnwYp0WJ9}vjY1qs{;6p<Ngn0VmWg'}
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



FALL='nature-waterfall-transition-01';WIDTH='nature-stream-width-transition-01';GROUND=.12
placements=[('fall',FALL,(0,0,GROUND)),('up',WIDTH,(-2,0,GROUND+1.10)),('down',WIDTH,(2,0,GROUND))]
def rigid_point(instance,p):return(-p[0],-p[1],p[2])if instance=='up'else tuple(p)
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[add(rigid_point(instance,p),t)for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,rotation_z_degrees=180 if instance=='up'else 0,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values())))
def ears(p):
 cr=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]);ids=list(range(len(p)));out=[]
 while len(ids)>3:
  for j,b in enumerate(ids):
   a,c=ids[j-1],ids[(j+1)%len(ids)]
   if cr(p[a],p[b],p[c])<=1e-14:continue
   if any(all(cr(p[u],p[v],p[k])>=-1e-14 for u,v in[(a,b),(b,c),(c,a)])for k in ids if k not in[a,b,c]):continue
   out.append((a,b,c));ids.pop(j);break
  else:raise AssertionError('Foundation boundary')
 out.append(tuple(ids));return out
base_mat=len(PALETTE);PALETTE.append(('SceneOnly_ContinuousEarthFoundation',(.20,.19,.14,1),.98,0))
poly=[(-3.3,0),(3.3,0),(3.3,GROUND),(-.65,GROUND),(-1,GROUND+1.1),(-3.3,GROUND+1.1)];n=len(poly);v=[(x,y,z)for y in[-2.3,2.3]for x,z in poly];f=[]
for a,b,c in ears(poly):f.extend([(a,b,c),(c+n,b+n,a+n)])
for i in range(n):j=(i+1)%n;f.extend([(i,j+n,j),(i,i+n,j+n)])
emit('SceneOnly_ContinuousFoundation',v,f,base_mat,'One scene-only closed stepped/sloping foundation matching the actual upper stream and waterfall undersides');FEET=['SceneOnly_ContinuousFoundation']
def support_height(x):return GROUND+1.1 if x<=-1 else GROUND if x>=-.65 else GROUND+1.1*(-.65-x)/.35
def triangles_of(names,vertices):return READER['np'].array([[vertices[n][q[0]],vertices[n][q[i]],vertices[n][q[i+1]]]for n in names for q in G[n]['faces']for i in range(1,len(q)-1)],dtype=float)
def layout_validate(vertices):
 assert set(vertices)==set(G);np=READER['np'];tol=2e-7;names={i:[n for n,g in G.items()if g.get('instance_id')==i]for i,_,_ in placements}
 for i,k,t in placements:
  for name,g in ORIGINAL[k].items():
   vv=vertices[i+'__'+name];expected=[add(rigid_point(i,p),t)for p in g['vertices']];assert len(vv)==len(expected)and max(abs(x-y)for p,q in zip(vv,expected)for x,y in zip(p,q))<=tol
 contacts={};floor=triangles_of(FEET,vertices)
 for i in names:
  tri=triangles_of(names[i],vertices);mask=np.array([all(abs(p[2]-support_height(p[0]))<=tol for p in t)for t in tri]);bottom=tri[mask];norms,areas=READER['normals_and_areas'](bottom);bottom=bottom[norms[:,2]<-.1];expected=float(areas[norms[:,2]<-.1].sum());r=READER['actual_opposed_face_contact'](bottom,floor,plane_tolerance=tol);assert expected>1 and abs(r['actual_contact_area_m2']-expected)<2e-6,(i,expected,r['actual_contact_area_m2']);contacts[i]=dict(full_foundation_contact_area_m2=expected,actual=r)
 seams={}
 for i,x,level in [('up',-1,GROUND+1.26),('down',1,GROUND+.16)]:
  def cap(names):
   t=triangles_of([n for n in names if 'WaterSurface'not in n],vertices);return t[np.max(abs(t[:,:,0]-x),axis=1)<=tol]
  a=cap(names['fall']);b=cap(names[i]);_,aa=READER['normals_and_areas'](a);r=READER['actual_opposed_face_contact'](a,b,plane_tolerance=tol,gravity_bearing=False);assert abs(r['actual_contact_area_m2']-float(aa.sum()))<2e-6,(i,r['actual_contact_area_m2'],aa.sum())
  ends=[]
  for ins in ['fall',i]:
   vv=[p for n in names[ins]if 'WaterSurface'in n for p in vertices[n]if abs(p[0]-x)<=tol and abs(p[2]-level)<=tol];ys=sorted(set(round(float(p[1]),6)for p in vv));assert ys==[-.36,.36],(i,ins,ys);ends.append(ys)
  seams[i]=dict(terrain_cap_opposed_area_m2=r['actual_contact_area_m2'],water_surface_edge_y_m=ends[0],water_level_z_m=level,retained_paired_water_bottom_v_gap_m=.02)
 return dict(complete_instance_count=3,new_reusable_model_count=0,whole_triangles_and_pbr_retained=True,actual_full_foundation_contacts=contacts,actual_port_seams=seams,water_surface_only_not_full_volume_continuity=True)
LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate(vertices);result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,.9);ORTHO=8.8;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(6,-8,6),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
root=bpy.data.objects.new('OneConnectedWaterfallScene',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole scene horizontal centre; continuous bed bottom at Z0; three entire unit-scale legacy instances';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
  files[role]={'path':f'assets/nature/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'scenes','assetKind':'scene','theme':'nature','style':'warm-handcrafted-village','title':TITLE,'description':DESCRIPTION,
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
