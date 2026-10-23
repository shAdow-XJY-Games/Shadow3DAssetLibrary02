"""Original complete wreck hull and separate anchor landmark scene, three whole existing models and zero new reusable models. Lightweight maker SELF_REVIEW; no growth simulation."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='coral-reef-complete-hull-anchor-landmark-scene-01';VERSION='1.0.0';TITLE='Whole Wreck Hull and Anchor Landmark'
DESCRIPTION='One static stylized underwater wreck-landmark composition: an entire old fractured ribbed hull section occupies the rear-left seabed, a complete stocked twin-fluke anchor stands outside its forward-right mouth, and one entire branching coral sits on a separated forward-left ground patch. Three complete unit-scale old model instances with unchanged original oriented triangles, material values and components; translations only, explicitly float32 stored after translation. The broad concave hold and broken longitudinal ends remain exposed and a selected longitudinal hold ray is retained. Anchor is deliberately a fixed upright display pose, not a simulated abandoned physical balance. One flat scene-only sandy support receives each full actual bottom patch. This is one scene and zero new independent models, not new coral count, chopped hull or recolored seabed scene. No marine biology, water effect, buoyancy, ship reconstruction, archaeology, load, anchoring or diving safety claim; selected rays are not a whole navigation-space proof.'
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
LOCK={'coral-reef-fractured-ribbed-hull-section-01': {'bytes': 23392, 'sha256': '43bba80786bceb286b543bf8cfa98adc17de8b2206715abb41e8a7979722948a'}, 'coral-reef-fixed-stocked-twin-fluke-anchor-01': {'bytes': 17628, 'sha256': '01df580cbd575a3bd33c613450596fdb143ad2d5f8cdcf1683bc1ec3a06790ab'}, 'coral-reef-branching-coral-01': {'bytes': 36872, 'sha256': 'aa95ac7834462df1a317dd763b928bcf5b7add22c18db2e3b59c6e6d135d0dc3'}}
ENCODED={'coral-reef-fractured-ribbed-hull-section-01': 'c-rln3v650dB=}q$FJC$Ux}TkX(o2;hLZ1#<fUx!#IpR5UvebNv18dXMP5obrbzjcl<g==+5{=KE=W)WUDl-q7C2dfu62rZY23iP*E6~}i|x3pgF4xoBJEmlSh6m~fUet;Zr{D+N1aQN$Cp(K7=dK)<4=d@eg8c7|6Qv;wQJ*bgph;#2zmP^Lbh~u>=^OKvRN(XZyxdYYiZ4h<uZo9*}rwb$fPq_Uq3YQwWhRmLNk2rt2=zdN|W5Ag#7{kux4cSOd2XnO@e<k;LpaP1AntnqO8Ap--tgQ8-y}{m-AV`pUxzl4}$wg_mBNH;@6Jmj9Av5MLaV&lu2vpT(6Ny*-bmrn$IpwX*nCxIX#`v<g>oqfF3{O>-G)gQz_pOJvZRX7<#{+j-`CMVQBsNRLt-t;loC!CQK;ngLU}&3@vsj>x%*E>73SYK!ao|mTSzyc)mlLmTIzBGpJ<;oW+z@u)aL<Mk5x_<qa*d89MK6FZHp>$mG+Bt<W4=dstA#I^ua_SWEbzQ95hytmZTHK3_7EN@b4d>3*LEg~y6(O~&F{E>K)@Y;0@NdRl9AKJ#UUhB8^`EtAi|Wy@-@oU`1R4=!;YszC)UZO<Vd8`hj%F!YSUEL$8~wll9?<!N>5eZ7MC8CaskU!wFGSfb2dqWl?HqQYOI;w&*fpr;as21nICAs_~%fE-ZZ^ch>Za|HJ43Fs!Cf$wsop=rs+B!15uVTFD0W-qEStHpD0>@~udAmC5JDVgg{=ti*++Bfcn;%qLK)8oCvdNv<R^=8tkWB%rxk=FwL;t|!Gh~@HwP#d<JIfV4I4%^f393-$Q_EEIPIl+A8so;5M?^5YXz~r(prs15?z4rC8D?{faJ^olCHk8wcwH|*nT#Zy#3;249*Ey@hW$mw8o-ulzgW3Jzv3N?$_9nD+M$fwY)6%dcr>Muje((Bi8@hV@c6l~tUvQ@zQBv)a+yI=t38zG1e(xQG;fn1yw(r@{R%|}3Ye#xhv170(X4HMou=_`C36!op$h3SU7gYe)-aebRXA*f3vVEr+jM>tGrq10ak;(U^v@RWX881w!FXu?VA9OgNL2uoIeVPG#JJe@v*K)B`N{@GD^8Ew$y~Nf{Uo5Mw&!jTOMi}0{Z|)PCBw28N6frExQc#owLX)Tz%Y<MgBq$*z2xUSz=oCp2Re*|;5)kcqmWII&;r?Ubh~=^-RgTy{VL2R@Bf*e7YOB2VqFS9hUhjr<Vv`Zm(;acx_BvOklvWiMgHkXUR$u{=>P#XchJry^fyq=|XdR0R7yAoJvKW$7<tmGUYn<(E)3l*BLr><8WHO05mn2H=@g)1AL=>k?RfTW_7Hby;i$#&JAV$KWa5z-Yn#AIENV2MkYET_@v<N4c+a1;6Entm?KB(JY>S7nMTn<hEI6s|*?(FDl-__o+!<o>Ij?V4tw!z&TzAJh<p~vky(%6>)D%pEns|R_k2Zik+$o3$P?zj8ky9Lja4vh^NW`|VSA*HJiDS00<!t9eUkuhcOV~Qd(s5Fs5l{yAxuBWJQ2L+MF;_y*6V-)-B%O{hXu^UcgM_6U2u<O_mOf4u%A-gc2hTBdgWcPLynu$%JAbhdJU<8f=F)WJ#5x!u~_d%BBuo@EV60vxesliZ0QPrSqe?fHnR^2$hy%1=u+92ml!@qmO`l6>{rz>84y1eF6wdQiUxu_`R_Fe1OZClqlt_PVv0a28$tqoH=%$L_bc$FQKrK{~&=qfXi1l+Mkp(&z9LTXS9hgCrqWVoELVEg_fiE>C*Wg!@{iv-1e*0Y-?ip3tFxe^Mg_N}dS7aO}bH&*R}w+&$ri{Q0a`P(Rgqq@pAM(Wu{DdcQ|5)mVkeb=gcAB856nbU=$NQxq>!B1%;MPY(FDT<yq0*p>jkVQpRA|Wv-z&$@$=RUwTNKOwy*aFa#8j?S)eUK))53=WdfHjBhRYU}sZ#bkx>f8nUBfEV#A_vuwa}s?zd!W?22hibI2kgzvxsml9%W2ynf63X;Jiyu(OFEKC=aHD*SIp?Q5e#lf8k>!W#>En^?Il%pH-|JraW|KF!^`%4$kiUMRUOkG*Itgup*p4?s%RdRRH2UPD~eFjKBy>lOn+SaP(-bxy%G$$n}ZUSiA-NrRbe927X?|GSO;P_G_ej~0u$>1(!Ysy5E903V)^S_`YN+MgoBa*=GEsLY9pkzeFr&y=?B)~mM_s{@{5$^&3C_UEq&ro=@TD(*~NMP8H<p6sa=ody?ZWMi%y)4cAh-o;-&8utdn<KA0>pic&GpS*6hp2TV`LrGs^PW_fI-}V$;uBSYH3(_h2kSD*0c|y@Fg|`OxWCv8{`L{>ZC1mdSFzc@pPlvHWu8O<aqMcPxAr*Y4uW550za<znB$*KluLtjAx0J~z=9hDKd{^S_<5lF2L4!!27}{NKyZSWlnHM=u}$$Yfdl+-d8=`E5~qEiC`lg}+6PvOM=UuVY&m&zkZ!jzw8M{zVJt=3=NrQ8O$*|D#J3HN*0EHlL%Y85ajGP}B^|f7X79qGnj0@!Um<nqm2Uy~wsUSe`rYO^TXf`Hk@3BNteH?#pjsTNmdJzJ+6%EI(;n#JO24OOL#cYjJVsCueZ&F5Wi(9PX8izwyyI+*=o)$o?Hg&9J=rg)<a2!*Xcd4=HMf<p=-wA1G>u<&T4xkfSWOy>|)Qy7=K&-oUXa%eORKz`42D-tXrxY>qxVW5oIH4rCso-(2$ZLM5O5FVTGQmWOF2KlVFf-R0Xqj{ki4KI>rP!g2iK#!)Nw@uFxY6Y_bBxPCrQ>nyjtmY2pgE6Ypsv?}YA)@4=JDeZ$*S*NsbEtPdj`%EkAu;rUxnnt^S^}sm(c-n5d`skc-{Oezg(r4yRjaKs5K9$SO%JNb_R%M;ixK?EyRwrzoN&QUf=l9jmR5FbyWGcL5ay^+&LJ&hFNM?|kM1`o5FquVWlV*s`BtmW=b4d%t7P5xSAq^x7F-q2wKO*zVI*98CCG*Gv(h9Ma+)Eac8_5QU8_0UHh%6?XAZ{XU<R)@6X@}TOHj*XeR<af1R<fDgLT)G9A#NvI$ZcdP>44ZlwvjuCkL-lFlk6bNh@W&q>?HS*JIP&S7sOqpi!3KA$Zm+cNjJHhtRj0M?j`q=mE<0>58^(uhkTASlKl|(lLttEtR}q>dr1#zf;|x+3giHpLarkcM2U!={9!Fm=!Ly_#d^73KUuGDtmPH!WiNix3;!W}=C$BCKP~@R({p-Z4_>rhuGg>D>q~2S(R$g7U-iO&2p@Ybcv>(1cJ-<w)`!!-Re1NYhs{$z9kqV6^(%$9+utp)Jot%JQ0A<*rXOjh^784{yt(t~={Nn>vrFQZ)$l<yE43AB^~2V$)z25c*=^;%J;$0l?Uushi}zUH{&=Rf)|g%BJG;k9yfNMS*4pP<y3Y4opFIAK`Qx@lg<7nyAF;miOKN`jTVGACRi7<?{#mKe{M9CF;XgN9Po17+Wj|U(f4A&5dj9*})=RI>u?|T8aq6eS{nm*$uD9lVFyCb7%=W{!t<~qf+u~NN^@C`1P2tpEHjh|~zjLDSg)SkQQXjSM`d8S)2Y#}a<yv)W^}~+K&Y7)WYh7$PyT)4Ai!Eob9edr`a#laJwDiNqhv-KyZZx-Sf2rl--#kPQJhRmt{)?Mk+?Jdf{o2aabnR1Nt5*FZxe=P4dzbmkUz}}u`L`pqYx9GJe^l;?vds1qzmlPv?`88z>B^~{vyal`@cV1Odtt;?|K#JN^m4-u=09!w&r|<*>QS1%C>M_YS~$hFee<n8dgq*fH`Oce)-12ZY<-rEJ7z@}tP<#-JRPEJ`OJHAbbHTF)-G=Os`<Ue$LI@#{e|x?&`fro|8w|Jx?GnFXYXh)uyxozmpyirlI{)W*Ubg4e%^WZ7_~0?%?966bN6e<=;-M!rqus~0?TaMTIFm%?6~aw**a`FJO5his&!r1>&TX~*PX4yYKGMnTRsE4=oIkZGr_0N1ApBBUU~s|?Hl2JK6vSQP;wKzH-JyR3F1=l&r84q-w7W1Zt%v-!0WC6@4OPc^J4J2tH4_~f*-yayzZ^w-EGf12Yl{o@bn5e-nozm%z}Kt&H=86n_w7nf(SVO7V!1=f^TmH_udXZeT(DPw}LZoh2OVB+z!sX6<#~Rmv@8HegORTesJGC;HdY4$L<3kzndHc&mJRj@aqYZgsh;8Xb?5h4|%`<c@VM$ounYQSVs;)UNJ~AkXxi73wh_hr!D3EC+UjA2IVpOA0FeqiN|<f<1yYJd5rf~4{Y)n@98{7Kfq)36+A{y!sF7ObNSt8?xR1RlHl^`?&<V$e~8PwzJ4O=AAQf{@o!dsE&9~2Zu7!X9+&#$a%paq$E7va<m-Ay%ev(;>Xyf-TOOlsd5pT{G3wR>n><F{@)&i?W7I8=QMWus-SQZ9%VX3nk5RWgM%{YgD34LMJVxE}nAL4Hu6({^KM%8iuY8_2R_@d{i_gv6b;in_=Tuhl8JfG!Sh@3z%PKxkbJrOwcb<<~#b;~oI%DOvpFx)Dn7lfru`GA}s&ls7^{cMka@ViAho-y!xPHpdB**I4t~2(ma@?G&Ji{Ef_A1Xa$L(R2XPZ^)n7lgGpLtfDbH($|s%x)!mR`FKqi5<t&(wpSsRun%4|=8^^h`bInR?JO^`K|!LC@5Ko~Z{tQxAHk9`sB-=$U%ZGxeZn>Os%cgPy4eJ(ugu1UG*j<OeqZErQIU0kQ!*Yq%ZqfyIz5_<&Zx`|Xe+tZ?G(rF>yA<OTsJE{6INyf;8@AVE~&-Hr{==NfpQ2_vk57zOv<2LCoemaql#f}Id|g46E;|GyXh^*}aI%n0_vOM~*gPShX+=z`ZFsNdzpL*V_l!0Rx?!z2fNZgFCc9D#TQMw$lsNh?JA{~BgM=CT2z{eKO!A*<O8aWmu<b0Kfq3UMoBD)S(3>VRnfpTYvjm^vYLLe_F4WJKK%yCFYW0=d*4h<hMQxfL?1eGvCSCUXbmR0kj)fZS#o<W>hE9)uicIb>RKh;hhlRzkj&gqVc<<{rqjbci}+H%*XZ4MH4*97ljmYY5^HWI8frSXqc!$aF%GXAMIfCI;kO1Tvopyz-F$O@-`h3cOm#A0Iz&qCey@`a>S0Kjbm`Lms0)<T3g~4{Y)n{UMLhAMzOeA&=1?@)-RgkI^6U82urS(I4^{{h<er@)-RgkI^6U82w=_4lMdoS+_h!-SQZ9%VX3nk5RWgM%{W~lgFrA9;0q~jJoA9>Xyf-TOOlsd5pT{G3u7bs9O&l<uU4($EaH#v%0OulX=i&9yFN;P3A$9dC;|)2X&AaqUbAljJ|@$=qq@PzJkZ-D|n2)!ULN;Mqj~W^c6ftU%_Ma6+A{?!DI9lJVsx^WAqg~MqlB9qdZ1m!DI9lJVswpi~suRD`nmC7<J2I)Gd!uw>(DO@)&jNflVHxZh4Hl<uU4($EaH#qi%VOy5%wImdB`D9;0qOaFoZWTOOlsdCcmz8c+J?N&h_QpC|qEq<_9P{qw9<Pf+v~JTCuDGKb55!_49G-$HY^{CCtGMqlB9O&+7K;4%6N9;2_|G5QJ~qp#pG`U)PSui!EI3Lc}c@W4?Xqp#pG`U)PSuc*a8JO7okZh4Hl<uU4($EaH#qi%VOy7j;&k5RWgM&0rlb<1PaEss&RJVxE}7<J2I)Gd!uw;njkW7I8=QMWv1bz6-m{qv-Mp7hU?{&~_rUz`5<{{dk)*=7', 'coral-reef-fixed-stocked-twin-fluke-anchor-01': 'c-rk+dz_Tjd42~02{(bDg2J*H5Kxz8zRP?wLzwwokekA;E(A<~;IKQpJ7IT*&d%b6qETboCTX!XG110of~h8{Bv>z7b><k%O$$YBQ+qM3m^QIRlQeB?qDj-|oY~8}v)}pV+mb(${G8u!p6B@v@43C_eb2nh@9XT|vUVI1y>uzjy)%d|+uYK;Kb-FE%@o5c_J=z&xlAEl%ooBd!k2dy^0|C(eJ8rquj<a^+B1dv4a-~V_t}kBqa6!3g!g3%z1e&Y#%5zAe4ruR+lB$cD<T7`H@sr|{%|hcgSPNy^=}Q~T)tiXL!`lIFdM7}d*^|j!>#+nJ(=DvHN-%_ZC&~9%;v6iZqMpM{+e7<u6=c1VPB@bsnFAlIR`r!Lmf6|I*O{(szN^9zP7t>Plnl<Lw2p%&MqHAYvc;H6w<j~x#7&_V!mw;Gqgt<w(QO1nu^7ATUSpeS6p))#>D=5(#1?6o9?dcu|40n8=K0uXWGLniiN(+&=5_zwyu0(*QM#gp4I8z;s%@ne71LYVN<4<?(WXEwdVUeyWrYhd0xBIy_wbd?tEcwx=o$h_DG`<u@my+#7rY*+flm#ZFZ#ci6)$g?buP-79G)K#~Tc}&VgwL2aMpP)o}5I88ZyWN?^N%!8Ht9Iq}M9F(Yb5qcQt{^pAd<%GtfUTCUBuXRpt+|39{Asy&RH)r!eBQ>`}<H7&z2<F={UmpRbaFcM}YVJ1Ac6>}<^hk+9{tXPe0snFQ9Et4*GWeS=0E!m#knZg)1=5bV&y&9E$#VjKhOGFY0?|pf0BVO@I+_H=ab`(9JLK4wCGDZDTZIg_3?4*$G$riKw20EsT#X@#>UooS$b4APM4O=#}G^=Gax3q3*+K9x&y^zhdXWOKWIh+YFI<Ql^Q=hhDo6{Pe)8=zV`JBdxIlZocu}$g>Pa5Ns#`TkWT_<CkG{L+Z;j<bBpVk~b?WoIXY!e$Mo7oyMvt50%h_G}U{;fA(s0_NhucISV*qY5;qvE42-?KNL!z#91w-@V+8m1!~`*KCOE9JjyRYFu!FcFVO5cV;n!DzHAsSu4t;<giw#*rP7*g)EtNLJG_O&Q=>{4{M}HhP3e!!qw4MYWXh)-|gwb;0u`8v&N=*WdK&Zw>V~Blb}L&8wR>Hnol#!K$%>A)jG)wl(rThKmxF4V!Vth?r(VT`W~Du({V_m5V=SSn)(G7LoSOKnFYK#I2a&NI!aw;pYdt_AdOoM{BsTrWc){Ui9?9n4IW&48IB=#!k<N@zeET!he37`7q*C%8{63MB|2S%KSA)`!za{qxiu_(PBD05WR+|{*{+r^ccf8p(C|-;oINvcVoP!8x7Nc1!kN%(y%LDh{nyB6SLznc)_W(4V5SIBD5=Yoe_)24J%=dNNKMztf=Z>;AXV!xMQii(PI!_S6Bfy;yZxt@5^Y+8Rbl@X?O_!6Qh1!c3)S_Y|P|3i}G&+GvQQPS~@z^pE@uorVE`?T6V%Qhu0IJbEPF{e_Q@A@a|?bVUFx>`E)mps@dg@5`6a2-BnBA#aFG}vaQovyB$BRwL6K^S$o15!`fBEjqL7>VeO;3+fi!_Yd4&##Yc^?EZ(xCRnte!v3P!T|9EUn%g4`Mb<P;0qkbrZ2eOxsU|F_}DzY9Qn`qUBW;%ZCSZV+4!>J2*98BtTf8DL+*RJgM)eCMtRbGGcO<(=S(s^RX!BwuGwk%7$c4gdG-+F4MxNmPM<)`s2A3XY#q@R|1Bz$V<WG#(vijD87u{M{j(^F%QF59oChOb=aH%|?pr<ngeHO?-@&e2oLJ+gT4)OX!^XY%0DN8B2^R7<mXE9o?gH?3yzrqwLow3@}6R<n51Y8G!=&Em~ZCu?aIZ(7abO{-bFX*G*Ct!DA2)hyn$n#G$|vv~8<rCOSXJ|A>%`|&T5iHSG3^68cz+$f$;mR8b;&qy2V!&BTThqk)aHoX0_&+c+Rbk9#y)i%8S$=6Smcm60lY8>8v_nUdKaQ#E&YMWOsSR(HIUX$>%Y5nCi(KPNo%7)u>n*mns+}_8=^|ImZn9KE=i??IVuGgBe_Y~WEO&j=Ac=;J;A=p`X+Tct}>`aB%nIazC!Fb^I9{w4OAJ;2>s%*SsOazES5g-mlfH)KZ;!p&LLlGbjMSwUI0pd^uh(i$|4n=@C6anH;1c*ZsAPz-<I1~ZmPy~oWp^L+b^bVRztH`C5&{OFwT7##RbOxTJUP%d9ouPDs9O$!X7OlsV)U)Vpx*SgqS$LA#p)B;-G>4k;lm(wpb+m=9#Pb}echNRHHG>z?652`c!}A<GNxe<kETN0&YCK7O5iO%OJT+s?IZ8KU%w-h8bCx>r9HJF89vA~ppd_6Md^dO!T|$$ADex3pP1Ar);OVrEW&$q-&!Ed_HgGNYowSM01#SSJLoGBHxDk9FwbDG`72x^w9$En046dj5(n8=?aG18!1;DGoi)j~K2;2c)O1r56_<r!kl%eIoG`Nwv$ON{74f+7tz)o<K;xrDp2i(!I7<I_C?(t(AQ#w8S@H&BKU;W0?m&&dEb-tR7S=MPbrdG2twVL0J_dju!dm=SS#pJ^cJ>p}JJT>aBUjORh(!m)w3O^e@4!7s=A7CyKU@oDbtCBHOkx%0gUlV{+z~d2ZlYrB}XCfj)z!_lpB*o6cQ^U6|J5x_BnZ<^uW@DChnvJQ|Y)q}LI=kecf8aMU=r^4WeC~RkFK^e3BLd7N0?Z}!a}A$w2&XCUoXOw`I8AxyOb1WGiH`%$1f#x1&G`ve*4=*k#Y4A&Cj`;LPY;agt6Td&Q&UfV@zBtiHMHxe2gdZ%N#+NwW`3xpg`Z}A&}!xft!93xrCmSG{otjmYsfErf1QY*THp@<mRCN*?W1d@DjVTv!`p`KeQjJXo8k7+e?wH+xPCTOdw0F|uJMl>z&~yP|F{AC;|B1L8^Awq0ROlF{4->8uKER<kDB8==t+30hn^2T1y2j1>!GLPX)*LdXjv6q2)!8UT+~I&@zj7@?hI6LA$;fJ&N~zJ&v<<2;Vztvif1Ceb*h3~1YCqVZW`{$CBP-9h-RRkx)^vdYM@!Dry7BcsOiqe`sSz_ahY1{`jgMf|9430^he_lue|zZf4zTpW3s;c8DD*5`M%^0N51K+fA-ZolK1WXy03ogf(MeXJa^Pr@1K1bdw9xMOZ&RzC0{M)-Er`7UoF>vb92A1mVS8o_D6lS^yj??9`V)JOt@rWf1SUE{gbS(r^dV`wgyj)^_SRQJT?4KVm|TI@Mnqn)>GqLO6-h0wX|nv?WyIwEM`2lTtACFPc8kxV%Sqlf3jTg)H08D9DKo7AAM|Ya^LIE`|6X|e>{0?)^oo4rnjC?_AfZ@tK06N)Zul{`068j&PtV!f6Z5)ync3S@LY6S+OIO7@YQnO*8WF*wOs%Dmml)g(hv6QU-s3~pC6fZ*jM*_>(Ijc_CDyVVP9f>JvHVnu{C&VtiQze;;G?>GV_V2hCj>9x1Jj3Qf6o5sii$TYfmlbWijKa<@#Cdd1~ng7Q>!e`jh2?r)GIn(rK1QTFvrEt63gtHOnKdW_hI5ERVFB<&jpiJkn~GM_SGDNUK>MX*J6ut!8<o)hv&+n&pvJvpmvjmPcC6@<^*$9%(hpBdun6q}42sw3_9SR<k-#t63eW)vONGYE}noHLC-)n$>|?&FVm{W_6%evpP_#Sskd=tPa#_RtIV|s{^%~)qz^g>Oie#b)Z(WI#8=w9jMi;4%BK^2WmB|1GSpffm+S#K&@tVpjPw0CG&?Sq;5KKK>ckBT^`g`Hbd<{|KZc+##_2a+3@yPUp!wdn0xss8{RHiK3CiDb~&CLx7voc%XP{1Roe`-r~GUN#^E+8&3at6o|I-^F58!@@sG>=<7)iuGCzCSqy}xcz0O9i*J~W!F4ya|9^Nk5YhS!wj_2hc-Y(bW<!9bLpv#(Z%6>Kj>k(`{WzD_>+n3PzM=<{gjh_Ycvv~Wwek;!F?fdXI<31Dt@=FBBFA*TWM1cGf0rE=($S)BfzeIri5&`l{1jsKDAiqR_{1O53O9aR-5g@-rfcz2x@=FBBFA*TWM1cGf0rE=($S)Bfzr+~w>+SRU%{s5Q@55i~`%u0=CEqT%9N%Vz6TuVJ8&mS_tSj-|qHrpBs(OD)zNfVf-}fn;1)inerIPPs?Zo$Lg>%4j)caHNEvz<tI~3M|>(u*G@_no<zTFBJffrF;;S%r?Dk!`Nd=d32Tn1i7*D8#FBeY+k1-9r0g$~%En-nI%3Hp%2mEe{1dkS5!OCM3V3cQN`P~jTz8hAt^fj7{{>5qXM!JFul^a)@K_zJp<KBeBux{Ef`-SnsGt*pCgE8R<<0bT`uFCC)K0=I*A(EW6udMoRGdOv-U{!G1<^+ih4gY*UUR@Q^mPG6xvS8ru~g*xdk=*z%8;1AFv^boKIoTGkv6u1}sJM;woC9oG<q%u7T+y}mfzDfdk9r$|s8XX1xF8Ba_i@py0Aoxc5EBYqz7VypV*Yqs#!{A%#c{&dK1Mu(D-_moykAXi*FVf!t4}$-Q{)GMxcp3OM`X~B(;O*es>7Nze0ltGyD!dbXC;h9!PlG>A-&c4K_#XNXg`Wd|j$T*zdGP1yM+zSRKS2Mb@Jrw?(Hja6gAdcs6dnN|p`R;!82m8(QsHCZ$7ozg;^W}QX+lV130$H{A&F0cpQ0%tiBE%{rs*Mx-vEDuW`-m_1Ac~Pha?^YAER?a5>J3n(0L(=FMwa5`5}ql27enKk$4;UA89;|1HJ_Qj(St)JM=H$m(|;WFVidF@2a;0zf1oH{vOSs>A+XP|4y@MCh#@zDfM>XDf%J!2Xr2t1N<@gKWRSA1^xv5-&9ZYfIkKQ4=tnxz_-9}(qak&{}=oVT1poHDYTSAp^NE4;2GfYp+;%|P6VGBGH5yQ9pK3!n@r$T@U&2jqQJAjGeYmCIPjg|S)mlI0G<OrJJdu;;9T&W(4}+<a31*l&^lTTTmY^Mg=j7CA1Fls2QW`DE&', 'coral-reef-branching-coral-01': 'c-qCC2Ut|e^60C36ftAK91ybtGGvgcBcdo6Fkx0Cj4&{O0-~66&VpGnXV)BI`bZFS&hDCX*fl2%`wrvXdwcG?z5n5H|KH>LD1SE9)z#H~LLHbo5&CX^6aXyeD&M660=fov9AO)hkf2Sp^%`Ltp^eqXha|?u+j`lyi;RzpjZ3hJP`cQ()N5nIwedFo%>r$bTpXMoT-<H#Y?HL{3A(sgMcK*0(RP%bZ9<r0z}Cz0ACzG0)n|llY)FjKX4}>HGdtVZxNzeS)cr>F``7<Q*lLF*#)l;2dl42FGbk=r8=Dv$AE(dn8W^j!$#2wa6Z0W9Q5QQTZb*WSK5nQ@NMd40SY(W%Z4(-jptZ9}jEvW6ZHB~Z2M-C++r)(EVr}%gn9u|}n*`l3o5YYo+IVfaO{jiIY@&Vsq{3|yw2IB}koaVq(D;zput;r!O-O9G&A_-J@iqyOA&R<v!jSlZAz@mZs3EaoiOQ4{9P+0dqfLl3&h{Tu^!=x6EschBu@Sy;@gaIeSD96$P9GkxRif3$QJMI^rfZCTur6FN5SFiPulPUEKJ+gO_CFgP)k^FJDoc_W9IlJk8of|@*!NPJ6B0ubbz#9tx&&p)!Ev$rWLvMq_#s+5+qigLgf2EXJS1^QjM4r-f*7g%V7OvSiI6rnNvn?=qy$!pp)yxHn>aq)`7zE9tWAQl7B;;#j>>rP#?26%zY_5wVam?29nse|Bs^qLqAp3>*VfBsV2D0{Df<3g$^@Mfm5Be?9v2^M+ySOPOb*j)6N1CFv2nTtQ+wK2Wje;DzP7%-eA~C~+SfL}Js~9DU85PblSh6_{x%2+H@3KN{|}B)hWpvy&%bBuRzJHZ>9j+G^&!d1q_|Q07>DgQDu1c}vBJtu6fd%}sxcvn+IXGP&A6q*<A#LlwOw_}Ci`na{$Zy_NPLX1GT_gicD92;<2z`T)zIt0y2K5Mh*XXp<KD=Ryl<R7F5XXxbN*r3$5A=-JoCRiJe}OtYBy(37duA>wX3UR{+C+q>E!6?<f$|{db<47^Kf+cbaYqSsq_8&#~^>1Q}%BBU*r9=&B4R%r!g02M_0Al#eG!%{uNKgIEkP^%7LYrP>$w;O-Gr5(M?x3PZtjlS7*g_C)b~@yE-|m-JCrB;{^YAXVXfn9rXV)8D|&cSdPxF?ru)*9`5<;;NfPRjJu1co13GHr&E5LtLM*2ySaLJcq+3k$aH>ob$3&{dZ=BT)T501PB{~qo^FNPRGCn`E=HGssQ&DroI&Gtp+ge2##wa=?CRgmKd_^5_>O^HI{37=^-?QGfG##%mmd%>r+;m8MJYd+A`8y{vf#p7aOEwi|IUKjzbv@(7Cd+hPNR&Ml8`XvM+tH9KW7y>WZ*z;e0Sx*HqPXq*OYF_gOu>Ns-4{O8<mTIV$8)o-`p_c3OaeZd%AkKx;l9{yF0t9J(SgQ@pN``b#-%9D@T&MhpVHr@#u1LbyX`X=<ey_=<ea+oWBUV{FA%=f3jg`|DU@g8ojaY-rCpMc#+_}R-57V-}QI;PyL<$+27OI^Pl~@`ueo@>GFSBaQ=G_oYhYMQ{3D=-JRT>TwI*p-PO)+#-l;`*U`hp&D~WAfrrQ6hs{Ab++CDI#x+0eZZ2+~?#4iRxVyV3|8aCtmczxv(e-}_q>CBT_`CkDe;-H}N7w%;kZynPfpS*j1L<nqX^t+g`TNdz_H%J@&p)GhC~<UF0_65TZ$MWkHy39&XD21Z?)g^;W87So#c*>|PEj82&TejMN0<L0aPDTf{dfI6{yuPOXQ%%waEeF&vcMn7#-lhiIZ@kQxd%v8ZoAZuYB!gkO@RXk8gF0~jl_`nh<tQb&bChf^2eOs|7bGXf`_|@sR1WPCElh6od3pvv$Bc*&481Wqlft({09TB%EFs(z(ei$Z~Z;pJl)KnfpRGSTL_d(Y(Zx59}FmAbu-_9)4wmGv$K<n%fHXypPT9*8;Xyiv*NIF{jjmIc{m=RrGG~#?(L*eQY08Yd!a_e@zuu~IeqUvZ*%zK+WDH_((Y;M1l7=(!}F)k)|9cmrP(;FMRRlbFW=(NFU%0}n2pOc6Ix!;Z0)<ro9C;MHtG2~Pi7c2BHlB7u;%{PJk3{kuR?J>e?P-tF%<FlQ!$3LK|eGrlM@QXf7Y39_$&VA@aWs~4DmOfYZj<_YRuuke9n)pIXw7rs$t)|SDMn-Hh7!EclWI{G`aCmGwXo0hUdT5r9xO$gE{OfjmQ{Lt|E?|n2=FWKJJuk$h$=G)s<jxbGY;GTFv>@?=@p?&Q323FUeLNwg@keUfZ^06qFyRn;YWFm%#ir;@R)cnL|tW*FcA$wcb469q6UGs40&5#~sfne0&Y_(n?|eT9o;coKdcSb&R+gZo&h0?#SqOqB737_xupgBt`FCulP?Lo^yL|^7ifgQ-|l99iqKwXH+o8T*Lz$ois0gSYZC~UU3VsmoBk5?$T&YLHTp3JVTLF@mRNPTOm7@tIa;PUxcTA@B3fl*Db5D(4Gsi=pLs+ap!K74ec}tj|P-8i$iOcWbZUu9GW@3z+4i2Sn<0vQRTd(P#oE;IU90$9@b=Y%wmmCB{sA{KjV6t@S3))yLReN9W!{ui^`0)3^vBW9KL$99dn&A4L>w)C1m?yrP)`HNZjT2!MmWm?rS4<Y1{&w{r>kt@!R{(EWv*PO2aHQg<);~TC8?%N}+k|=f-SN#YLDM9cvboNMu2I^NsQ3Sx$9f0q0YV$BT%aPq$`k#>~dXE!1YQ%PtRQi7CcoN5lcvZM|*3F2d@tHlv_yGk>P{jpT*cp*=Aal<Tau&^+sM0Aos(FpFOeFR!sXu@4sxcM@{T(rvuYSft|2D(V7rMbg9b<EF(p{cKW3L3!)F)86TkhjGl(xBoR>dD16ie9gtiI2V*thlORh+%e!NtGb5&7N2=NEhA~m&$TNkcg{Gh?3HvJSKPT!yy0TY4Ex4E*Q=mhq4dR!obW@~Vo9$;adzN4kDen^@YBOq|21x4u_a^Wii0?|;@CoQOG}le$?pBgp7t&<S8{R5=(+0<l5$fE#o;@$ya!G?gfBKm7m8VnDe1qzWyW<E@yxN)ygxNJ7|#zPK61^^>v&UUTsslhI&Yb-|B-Htp*egeV7#}-vJ7L~W`8e-kNsMsZR6A4<}eg#hf^aHuyNc7A(!c8g?Yn$QFAINo#%P$is8QKKpd0z)w?j<ET%C=!6YoXxV)w?EcbN5q=<=F^9CstpY{5pQC;k5jE^~7w0CWM={UvMw=ldl{SS@T=RTMor}nODQ3KcSoQ9RI?Jh8%d-Fk4*`kMWjm+U8;dSta<qUlM$=BN)e%QGvw!POLr(0WR6qIW&^ToW4Be6@nmWAT=XAv(foq(g(zDO5wpQirkIx^mD4%pZN^Q<Ns_dL(d!rU-SnrfW8h%GwV;iI_eX#Wj_Jk{L~9Y2o3{_oeC#nlgZ;ud+5aZN>B>yL>n*M2olT(v<X;=Xssv0ana;e@Kc6pEv3j%K&4HW_V-I87SE7SG&-M`w%|^1SWi*>;!pIIDhAq1a>0BsPBYYNJgNpB}l84Ogy}=~Wg8`Jvq+b|CQ}Mzx=6!YziRut4W@JTh;QS-i+^KC5&w!)TM|rcdWF>;4(&1S3rNz^et!XU<`4TqeH2JfPM>mi+pl(T+LXzuscjslEZ3YL*FG%wEifq-J2lX_HNO?aPHs)tupx-E%Z2!&6zCKN!v_GgdQk`9hX*-GEi);U>KQ#Ui%<PKHs3XL=slP46tMa`{j1!tjzYEm=%pCVpWD3&l52y0X%lS$Jwq8BJmM^g%n8GW(}*h2e_N8!?*w)3?I#)+Kf<^~w?4+cm6Ee0ilS3+;Ra4-9HlD89E-S-S~8Z5D=GY;4B9hup;9r<^j2m%dQ5wB(yOvFR!yCj~WOUoPLk+oNt3nBP~Z&m8LCFpgDFe)`dtr5?I&^r4{KvUz>xcHug@t<)8mOU-J+y!zk3pxvzt%(KrnV-{s@8ts_FTlO|(zm~d<R<-wgFPhMZNe6G?rAJ3h*uQUmmecW;QHSSEmFqFrGPm$TwdE#!JE1-ct8okGRT^)?Z`L(pe-65Z%hO^_SUTO5CExt1lkz0MaJ2YCT;sLCP#E4mu)CpF*nNDNxvo&$dP!r$$UBel^`{wy;$A<B8fsj4Z1k-#tb6z@qk8AZM&Am<9R`CTamzz=_1|A8UM|-$7%tz(Co>F%;%U8G8)`ndXS7);ej99vzV->nk(CAJnZqItcN0J1n46ml%=hjE7!Hm5jG75c3e1yNxEd_1z8HNlhxaVCGkkLRVjNe*2W(so`qQ6r)Sf+Naj-hTP|Nl+W~mPrm=6yLHe6Wn$!MpbT#@xR+$r)6S2bR1!v4R88Q6)hcya4y6CPQui=lM%Hyk>2l?mVJ(b^Dq<Y(XSrCJ;AEc%8;9CjK~cXl@HRDVPJySq(TozUM9_}f>b4$p6``e|xkxQfr(*qX&b^E+$Wm$;6)!G0#JJ~CW0&hs*M>rkOk+-l`aO|#<{jAMzoLC^xt&==>8<MMnhb(Usby^Hv4X_Q$UJ93n!WyWP3otkVGSB79siv2ZXU!J`WF4I(reu7<^J<BkM7cE+%xtIGCk3w-n@X&Rd0ojjmkKgr-f^x5Yzi3_`duX(24rBaYO}SE!jN^)UN$1^~n-P!ko~~wrIcff8&AhTtQGL6<kTnN3Y9^#S$CcI(G7f&+rtx3+3<tlyZo*Hi@6qW0d}`F;8E5U+v~Tnb<pp0&c!=LV&F9b0@Qq~&1J7S9c50kIJ;y24%Nlm2jl*i47NB*L^UX!Pt@lK%y=M*{KU>$kFg*A4WORNo!)Q~)HEK*okH{I=r@cpph;2hApmWhVSj8f-P>ip}V(lyQjW$J0r1_Y#e*^ZYRwg}oSPDLFupXb#<?iP2)wv6?gnq5DuQ^=5<06cnwg!8bc`xKhpM`i*wH9-xbjlEM3Ck25wqPCh?VDI&UhrxjcI&voXh+1eZ!W~6Z8qV!*9qxyH5OwT+=%@?tutXICq-)|Zi7NCGI&1rauJUEa|1g0dkMMmqJ`M$)kc($2byr3pj0gOWs^~7#7Q@_8}kbWO&z5v4DV>?j3Kr=v1hM7h2qZpB|JA_JI=m7sZiYeN?V+oz1`?rVL0ntdsJ23Vf3vq{Hc>adSvXx-c39U#dWkTaN&VnIG;2v6j%0h$6G^p8EqDZ_dRZm5k9&2<;=_ibF{u8?hnqzSq;Y*n3Eed!vmjlv7P(80&{3h7i?YaxX}l5xXx`?O!#)(IIf7Vg*jtZwG-$|<Ahwn)&b+gj$>N0fo5?N`^Nat=a{i?LD{-oV{EeYBnD*7FyZkj4YBvOlQ^jVBom(QVTTPZPvQND*(Urz-3%Y>J7w%!ZCO)1b?+2@-#ko{xw;XSbvcE0A4ZvQgV0P|@u?nK>UC1}6BVQu-yUgtmkN}o7LAs6%zI?0yEhBle$`33f!3_&wM@phAJauk^40Q8<Dbq3Y)h0j7rSP7ymKZ#`Fa@F)@aH?;-iE%dHsNh@mOv40`_}Hz1;IWkyZu!YBqH2EA!*>W1SwEjg^yUXnKE)HcOu$Yopg|O|_fL@Wzk95<mCWA=zx`x5b)SH>0KBVxMRlSlz}K*TW@VpP!c~ZYwtguo2FCu#Ps$#OBGhU)ThTWKD}t{iR2FQS!T+PYo3|XQ61Uwkx;e(#RHgG%s3uRC5aJ|7b2tFQYfhX0ecH`C!}=L*L6su-*G;xyb05hAJbn+0l_h<joZ(7$yyy#dw?M*qNP^#iCo@)vT!$E#HZ?k{`~mf~rS>vP+$E^0nV8W3j=3GC$S<a)gB+EXT@^ixTSa{_tb*?HBj2LH~qnniF1wWq#e0h96`vBOYs>l#P*j-$d=(mgcaYi<_`@qa#iHkC?5OlY4YE_`S+x$$fRW-+L3*TNfqs{)^_z?_1u_nkDw&QO}NO+dN7Z?bY#ru3$rUMd96U;=a4LW?@Jr2iD0DX)-T<F8u!C_slb!qo^*|7i%2VN@Wjbv6VA|@k;rD(wTJu>>KVu%djYuy~@v>*MI7+moGcs($tJMAkTc<__4Bb^wQZcr!>;zbo8jFmkzy6Gz<&MW_-J7j=Vk}pXM3sF=2C8+}BSpRbRRd(`rTIfef9=eAk{iiI3fu;+xX_rN?u-NWH@EVC?b3$n)X-L6S$Cqqx7z2{u{PL-GxNf;LZ=;QJ}7(YN|DTwXUws{CXpW~45}o^`^7Hu=75stlAicnm|=Z-?>qfJo^|#ds{DTx&nl&Qg(p9GqP4788xj_YKX9lG^W%(pZ!|!5ZoHQrV>Onv?5H_vG@`htY3(d9<7zEsN~)vEt)%&8iLaO5e!V?bb`zHuqpptL<S&cj!#cEq|6?g?V2FW8CCuY0t$qIL$B&Pc4g*MDagYl(1<LS<E&q%EUe&Pu>pSmyfN;AKrdXeQ|cnDVKeptP{?q^Z0#i-v&EYFCkh!ee57}$g^hykC-0IZgb8tmA%B)SJKKuuV=Hg)&9(~YJ^GqlXh3w^YP8tnOWg7AOED}-B`&`27CI&n5+dqE<YBpZ>c+nf8>>9ZS@iI#qE39{kus_Jvc%Z`8=<O%#IEi&LT={P4sykk<Te#BIKg!KJ5ASOtz;+lpMIC1uHV}02BHDV_7b4nO2@Xs;o2dliy?fo)jG~mb(mCBq0^sW`s!TWiGMLwm#UUS-6z`BT194zlqI?M#yb8PS<?hdKd47Xl159#`dK8V$)3nP4w5dij@QP-We<Fr6b?BtIH8q{gnsXa5&Or?L>2L-(D}f{3w<Y_c8~0n>Vj#;>|H5G<&1<Cg;gT$3EhjX=OB7wFgLX4@0DI){#|Sas&Bu7vDZ2JzN@+wwY<Ym$5XJat^xEo2gY>h3CDD`-gFL{mN`omuTTwyq(LA{iL=X*RcW1bD3zYq{J*795RmWJQrqiE*16VeG|pu)bIYRw9Q=H5-~`M*_y@PWa@FNkLh&;uN*}8wdEOm5-sub;%)MC3`nZS*yn3FW>C0^{UhZku(+N}a9=>QaIEP~KC-E8`{98Zy`)>JXt_&O>x}UqPnukhD)>#pwuXzSUKA`nwwi{zYL~F(AN_^n@?&kN^O9Nk*kH`UV3V;dW=F|IPHCCT>&;9wE`J^TQ7lp3<?uKoxb#wlt54Xn*t(cCcYx5oWB({QyRjELoOu9w`@9|gT5tI!hs~<JkbNvOK;H9gfZXm>6e}_5D&zg+{poDqU4GQ*9IJajgYo+9cIf0Y<J{T1U(=EIfw#l^Fy(s^&b<@J%Dj!2-``$|X{*E7lNEYdwD$(TUB+H#&thR6b+X9+;Y+8pX}hvn!)Bo-`n(SB|HqHr<!X)2vE}iHOy+XHFc*VLOlIZ0^>W+mbMa{9$*i)QUg#%(Tr8N7fSFU*W98vdGC#*o=N{w7-jr3h4>j>K#CkT1xt+s0hlQB<EV3i=XWXc5Y{6YG+?S-69ae2;8*6%Fu39hid)RSiSE;AdZR{x@z?bd1NfY93;Slvc<oENSt>f9~AB%BcM6}6q#P_Y!FGA|xsvFMAkXd3@gcOn017BUrFqwN^@&jzV(Sq&%E!1T0ygu*em}x1Px?nW(NYP72$F0MAYbLPoopmPp(G;(2Ojt3G^>GMM&IxnTA#Ofv5Nz7+B)vhOp04bHb3ZB0z88)kzm-`OjW)Tj=Evggi|%9FOxVtbT0YgdSB;bEY|df68AY+zH=V@WdA}+J)w)wG`&NGw|BqeUjhotBWapRmFtIbI)MNH`a7T9eOn+ft(Y)@u_LHtw*vT3+&cMZ)VUpp?R@SZ0O62|L{aib~m3&3MgBF&rQ614iKGN_B?z(dfMf38#e}-9gh+@^=hno1w+c_Xd%VTR5#f^<JOl*qAI-uz#|9<BT##`)Uu2mxC@k7sPyboS5vD2{hM7G>^E`~4D%PoSZu<bn;;UN-jlGnU=wu>dCUBxYjy33{B&18%HpW>#xo+j=5Sesr9kl*~s#Q3Wz?3_gxtovdeOI@OuMSFwyfgkrv%aXXD>_K)qNH6ntB0mMPKg+JiRy+0b;eDN1XYB_3wU4PCelENY-_HBbkJV^mIXqr7gUxCmEsOl$-(s*KF!vOm?H46&88F3A!s03(d=nvUxP1;Qxy`_-eS&3&sNZp9`3ZQaZZCQ6+&Jl0&qanYBX=^sosZ{<W;@wL`zJU_?joN#IUA=3&S3j;qD_uFeoyi~@cZ-Xk|^oH0IebX=}E?q%int+7=4z>>+cv;sgcsDHCLHk&Id!^kb%<p4YkpK=Ry2MITzW^)L?wEOdQoU(j=!4-Or2ci1HEs9`cuKE6|ce;D%Ja+?S=HLs~Tco);~P?m2m#KmF!2>xJXk$d!88^Wy@R*m?rHS6gp#pDAkR??3sNjG9+cez+l5v$si*^x7p-Ru7%Vwpwn$xHWy`8@)HNPgPDbzMYSiD7L&!QJg)e6vvup&f{U{2$PtI+C_1Y^*7mv;cW~R6n#;AcpZLT1)V#u&-=+UKbC0RyHB>Un3~b3|3xS9ImM0KW9-#~G1%|7P$?u<E6=f8kF}mILs4GPctw9%HDwZ}Y`@CfCk4xuzOKaHQAd#PE6S~Sn|vPhIwTXHve}w=C3oJ?@*MVP7o~Z-O6(_}2Z?ek-X{OdK|UKPHO)L^h`4wTYd?sV)?1%9Tp>q<&nS3()=DQCdRJi9YmPGhS;VM)dMR&k8P;OLKDNDO7Czb*XqY}$FIPUCjhR-R3^`7Ell)Qi9D}zb>dWVz-;W<=Q>r}I?46~TbBh~T;PdC2la=+tyjY~euj$h{p)yIGgx6w@nyj7A<tZ$$;!|vYqnE_*CD9%b?GxTUzt#))-NhpN7GPV&zGy6d4~X^*Z--ysd!J*Zp&?dSBlH*Hn%?UbE!`h+Omo>Gn~D1J>-(eJW$YT>9B)bCvdE5EdxNvHaCizERem?dE6lI2sGVO^KDK-eMX}}E`8o3b^X<H!ypG6!o}G)IXW#nG(fE4lB$fIG%dRt9W2hG)@j0L<=Za}KNS<cD+OTE!HWcMM^*?Ln<fvDMN>{I&<Zd^U^>WFP>kSTjWD`4l{u^nv9#=F@!cxk8rmuc0HmHz<yCkune6A|Wsd<}xZeq~(m2TG9j%8M6;Ws7Ey0&B+CJdHQl*{n?ANux}W~dh9iW;X_VCP^-Rb(mF3p&d9{AFbJ4jj>-EM{lN$YodW$B1**xWQF#lE3hFM7a-dN0j^UxnA`Zj6GWaG-K?@7<r32hc$0f%#eToDas9bebG7w7m1Ri>JYZ6%~8hhpGDSp*m>7EI9=68;@8)DWsJPTr!01uw$o&-MK-HWkCrDzU)6;9WipYS4H?t$@v!^2y=Whky&>Aqyl;G8(H`UXfM{><YkeVS0Y3k+9|OX|Ox9PlH+X%~-r(13NXaYAVt5-I6A~s|Q(i|DPd*NOJb4{aoJBF@=fX4Z56}Eq{BwZbOYX4)Nfk1jPiv)LIy`2#wOhP)t__!FHS8kaTk<Q`Q0^D^pX@AGntcU*+)p6iepJ%~JIm=TkVZ-&D<kmevm-3(z1HMepXiwbKNfFC^qg?4E<$=Yawxl;wwG;A)=A}#j%6<%tT%a{^ETQ-I(MZmzWy2{CuA0ro|LbHsjY)#zOU%{53kQZZxKCv@miP0KJRXh_FH33Vkn9g-_FPCdWm(|<@ctn!<JY{WK$F?k)1y7y`{lfli8&%PmpImZeibsNq*H@7+N;bF+Og4JJpaP6ZfHY2Ul4Xb5UPDhP)kqUZVM$<3B$xZ(r2T=gWBm99Z1PU3j&mUaB{)ExX>2;mh`s5}*GjZ@GXc!_y7(gCnI0Kb~Nn+_J1<zYs~3gYz~;c{Fc_&-X{2S%PkcL2Ugxy}Z3h8s2G`#LCA;3!e}0I{b5q-1$pcZU0!rZOXmVs<kY%c{0w5ixNJ&;C1*o@N=K>(NZeucU?0kwYxBGqFC{Lcdb-%^@+n68@&lvSq4kGB8%Cy`p4O?C4!|tiY{g`)s8b>hmVQnz1#Sq;`t2!kbyF<FNzzlf3IIz);Q`CE(;xK5+6}J9~0hxbLPUg^FD~?EAo@)z3L5YNK-9y^^G=pUZ;J1hS_;Vvw8PICH^^E(C}#a?S%!*>c<q5XKwtnvbui#<Y_n7vR_x^BLCcM^MepM|9<92rzcEglYh=R_QXN_73O*0*b^(Adv+3E`d#<l{yIwNr|4Oz$mXOwLDG}xSs3U04n2zwkg9%6#oMipnmh}Ax4nyWXv!Uws~u*%KL2dWsrmqEM}vo`J1sH3FaONy`HC5Ma(o7^o*5?d&(n^~x`gh7enq;ggUs6zJ?|3r<)6Rt&)jw$Jj^baX^cx3Mai`tAF?Br?rWw*hY6q2@%o~*YyLqeH|ylhehWCn`2ADN={S3HVV<|of@q1~19pEz$a<SmhLzD*P1c&%;qCMK{8(%J6XieF&DYdjm%^%9q~N`BQ?OP_w8`EO`NQuMzOQJH@%urv2Y4NReR+L;O?e%D?f7;1<2jL2EPla}y90!4$LomV!_S?MC(ojI@_qSseq5e;I~0mQaVQNcC<i6L0xCdxC<<l38UU(6bs%5~HK7vJgE~+Vsz3v%4R+8JYC(NaLnCkjH)sg<;0lew9h!p!XrL81f-^|a41A$1ctTs~2wva~e&7M^pcGhvKXd{cs0{5P7}`JtL_#bifDT4L97I7PjD#?l023h`ronU=2r)1N#=u;d1EXOwEQ5Kl3f4mkEQHlCAJ#!KEQKww8J55bh=<{@9d^JJh=xUw4jUi~a^Mu4g`;o@PD3u7gDW7zZ*U7T;UwIH>+l?&!8N!8f51cd2=Czmyo9gtI}k$28~6mp$rmU^%91?z0q3D8sX(fcVx%OgK~$s?DNl-!TI38|go>mdc?!3|nlvHRi3e#$koXZN;zC*wN79<KBN`G&IudWvl5`^-NOuxM+LJCsOL~)Nq9=VwEQuriNHB3DVI+aXlTZ>#T*+wChBSe?Fcz99-!s7$I)he`S{Mc0!3P#Aaxn~pmf!>n6uAJFLoetFj}-X`UO^A&3O5va1MWi?=mSR-c?7OPU+53V6?q)8p&x|6Wkp_wV=w?ZfCU+#d|!Y-K=`c4&tOSfKyP>rEtKzX5Ck=#Iq3#oB!E<fVxU%}ns}0u&>F%O8BW|u0E9wcMfN2F$t;)z)5vU?P9~7?FcoH#aWIQaC41l?%qM$c0hvP%Ln<sKhhPa=L?)3LWDS`}R+D99GMP!%ktt+7Sw-fN6tacPC7a1cvXCq$zmQb2oopp(WChu+$lYWwSx(lHeTv*ic99Ka6FH#B17tthMs|=xiabOPlAUBF*`vrk<S=1y0FDp?$RwBShuv_R?1PgegX{!7oFTj5EICF7!4SAa2E%1?o(zRw;1)@O-^ewx4OYTEvK8)<Ur8FQg-2u!JRuLsM#z91vI&lo=Omjj@(0NxzmwO*Ku(d5B%OR9FUfIoj(j2~$Y=7FTp(A-H*%5uN%F{ba+?&TSBZ*#CpXC*QjFdp7L?Ej<S{8t?~_ur1bs>}$t&`Vydh=i3-X?nQ)D?>mcAojNO?t;r&jbU0cx#CYg&Q+AVp|pMOLO2DW#UQiXyAfO0+mFNvkQc8m&r!e1O{YPpC!f(Rc6y?C4u)N^8=`P>0ylC*VLEQd`oHIMcesg*wv4#GW8+L^RZc+L6k{hc+cGXmeVHlpw8XRpLim($eHR)S+dFEp1C1P#YRZ>(dUjE3HAB(4Mq9?LphoMzk62LmSh+v^!N(SK6OC(O}w-x>0W$M%`&R9Y8&)L<dqY8bL#;FKt7kXe$~`BdI^FOFPj3+L^}CZnPsEq{u-up0=mGXrdw$X&eorz3C7|4xtG&glg$fMGmD&R7dqRS&_+f7>%V}=wL+-ro(9iau+7i`eY&<L4So4Fpb`XsdNG@M{1IJ)QZfdGpP-6AgQ!ANudkqSUQ?6p=0P`x|EKhlW7_qNmtTEbR3;RSJClwHC;xh(>ZiAok6$I^>j9!Pq))qbQ|4B7t$4Umm+u39dtQeLw753H{D6s(sgvNBKOigbOYT=4=C~g-A6akU+6(a9;EweA{j$uI)ogdhv+EcOtR@nl0`G<AQC~2)4}8fJxZfU3^_-2<Sac!57SI~nWob#^a5oxhhC!wdX-+J$LL9VkLJ?5^cFos&(kOLG<{4T(o6I@eWu7~^eMeTf1@uI`I0`TztTJO6}?ISpfBicdY`^l<ZJpneLx@4w~BmA-_Ty9EBQ=&l8^K|?M!@05mhHbRqv@pT9KkEA7Y{UleQ&eNokcoDXS`>8c&9iN~&?hT4kjgN|H%cRT8PJDz6$&`jeWf5u}!?nrZ;)LB7xs@|D`Ce$Y>}p(>BoS2a?7pemJG^^P`E)m4G2n95m2R4yt9m8Ghb%3W1l<)Ly_l~GkxHCL5Xd8yn~6;xGJ8dW)!x5`shT~%AvLRCZMqe4|3)i>H$Wvgnc@>MlaHBk8}(ofY!RZr!p3Q%N#s<p~q<)mt-$aX4!m85E^>Y&IDs`jc@DmztMMYdISQ~~hyR?Vs9DXPIKs-r35A`2QD_NA4@{2HYNWl?R;g4XObhxxjm=CG*tr#W>%&8Z1$PJK`j7i(;zS!7=t^XvE)ltr~gMQlzDQNHe`Idv}iT8vw%7fbDvf|V}~E)*BE=HmZGEk<){F7kEt{(sdx3v&zd{!ot@>n0Y4&8d-AP!`n&<Lh;q!{*fJGN=BQIkm5N7S**9@q$zh27H}_`W2I!7l!}0>t>l#AIqGYRVSp8>~8vItiLd&P;5@^D|6~a@m#@U9=qPbV5~<~7#7u_;#pJ|imwI5^WYV!?4Gl1)EBYs*A!+uS~l7dF<)Ow#G+bL=G6WX)u-Y4u9ZErtbW^AZ^j%hOl=!c4I9304bSG(>fmc{i0WR5>Ra%9?3HBr^Wrz7zKHpH7^2!3=G4Ft)w&RILF-1CQ%{1g6=4pG>Mo4zmZqU4pBd{k6qNaz4Lm0d+MsEsePOJ@AYxHn2T}b7zGef@C+}_6Sj~Q6)Df{cH6ALsj>QhkQ*c$RO?qLtpfwfD;Z{!b@SWpEWBr4IGGC8DRL|h`#8gai-)yW~AmUvQQV_;%Hr6l@F<%!!R3kxD3qe%pfam|#XS?~&YKuN&E&41q&$f~yF4mkj>Wg?zmIEFOJZ=1pwK>dxR$KJB?O_QN-)n89U5>s|nI@KUH=Ra0@Zchwd7a3gmUWl5?rG2X_H7;|ByCe~spr=VtklKw(!^@MlJ~hKY+CcPnny1?NOd1rOT5ih>zhldkIG8A`Z?I>8?ud-@zU3<skrQBGs*9AEh$INWFnpRgM8S-w(-)YDwFa4$nz}jtWNs1_?L8kEZwz4JQ^G+IZodx>?`t(?`zTjJ&t`gK$=r2)qCR|8+mav2dQ4MOcOtOAC7gr#2P)1lw2H~41BCaKJ)sbzI>cTzJ0y<3Fm$emWpbJX7DUp7hR=_l0}t{Qq~L$CbGlp@N*xs#!jvfTt~Y3IER^IpV#NtRJ7K7yI;dH(vvuEDcdm@YX+5(Ml)~8acmB54x7s!HV>1^#~emkT~$8yMJ>7BKgAlJeuUQpI!Vjb2DV|wW3<ocB*g?CW}?1RS}te(ePX3W(>kK_ygWwigQdaS_h*Q7c>A9#KWDxxL#4r;b{P1+Q`%RPuhnsu*7nU|d|#11??2y{*B9x`ecjNoyGgVZ>v00VR-K5WzDm;CSJmZaJNIkSx{Q?0UoVeM7o}@<br>b>oBznb>+?E%d#i39vh%Kr(uAlilfFkUHN~s92T19)9<j=gBs^U&QCj|H5EG5X>%4vAE+6x$D0Ou>YGS{Nw~suyy`|*UFo*H>`MHS3<#l*FFT4B5dA%&9&5N?xV(+F>?}??P+ucCo_poR`yN65isQ#rShnq4RIi`)Aw7HyQkuceWMf$aeC$YP0tt6}B0kX)>3F}N;xUs*~H*bxJev;K0=2@|ul#_Uzo&Ws|i`m>w@-Bar4ck&ds<bIUy4Is3{+3o<3f<^0tqwn}IiOZc%V$=UB*U**q|pv0_v<U+%Ol9!FMaPeZd@BKbtw7N!1v|#A2#2~t~cv1UFmfI`EmKaA|FI!@$=&2&-={V6zTBCex<c_q>g!Z((v<HxZ<6yWUscDnlCjVe~gRH6@1@RougDYx`vcI{21FZ!cl6nvW9ePNv`m`!RvQfG1l8{cWLQ<(;$iGM!!A8NPUp>r1%CC-}rW?B0n(gOKa(Dm6NPunIBmFQ)@|6=_C`)i}#J!7y0kE*+!1lww7-8`OUyH@29Ap_mkHV`OoW!<|Xon=W$-G<%EyLrHSFcAkXf<wvnGr`;IS~W;33P--^WHCx%JgKa4Wz%eO!N5Q&z@he^M^Gu08<;q}dFH;4JLEFZR(BD+{hKFal)=dpQhq&CZb;MCTcjOQ<3wd_@$WNAiddxMC1JEC@x&4P|4I&UZSYb+1?&_GHUX)rmri_XLPM!O7i#}|>RJ?|x3?6zW)9~6^Dya<x{cHZWkT23;vswed>zQM#!`O$XrrC+Qi_byMc(c#i^gjEM=nw^gEeR&<;&cio5Ga77ik-oKaHSvLO7x~GL#oK(6_6$q4=^|}(*@67Hd^_J)q*GAleHOLz<BHDt8n1?O(DnM#*3HLF+C|qRUOzXzksLFip)|sm;q%jO^6f3vq#M@z7~i+z7H7H2_bSq=ak-4wS+J#^p@>IGY5l_PQt^xLScu$7x;=IiitO_`X(NirRqnKu%2qkfcpY=b;`{RYBjT$`IfnzJI(0G)BHwr&kv}3ke0xEex9=3{Ee&?Fls-jWMMn!q>1Mws66{D}V~aUTwSyI2n_{A~&ESY0->s$3y8~oihi|`nWD9dDtCxyDYl|Z0ZSw8B4<a3YERoM5eUU$<pg5F+vc|tistCmZpemGsnot8uLwTT39c-XBRD)VTKm~Qc7OcP;>O(zf0*#?AR00QR07bwN8bMPi3JswdXutznKr4`-E%*U~4+KDK=m71&7utX)_(OZ>0v(|nbcfE+8+t(}=nBEm141AadO{xvgaHr+u@D7=U@%039)`k57!MO*IK;zP7y%Pu3JinkFcp$u91MiXFbyU_0>ptOlmr(=x_}dufGXgsNLO$MJE#m1ip>8jC^guFPLVo@0eA3*x!?wKU<P<WOGts{kP5S5Cd`ACFbmRPDa?n3um%>uT37{(U@>e`<R;hvOJEsnRpeIK3@czY?11I)3v7e+unsmVawBX}<QCYj$nCIGkvn0RB6q=V*bDi8k+WC%PKW)l4>A;)0Y~8w8~_6x1_nnImLXG-nUJN(EXY=5HsnAq9D{Slzpy$3$KeEAROCfC52xTHoL1y%IBWb%tP6^~0GAYb2`(%0GF*Xv5CqqtFI<Hi5Dxv}CTQVTxCg(%ZFmm1-~~K|J8&Hy!d-X_zr!QA53h`W-Sifoz%$5GWFCBmm+%1IDDn+_h1c*0yi?>mc(2I!@IjFu;G-fx!Y4(3f-f)%lHnVShVSqv41qB~NFo3!N+|gOC5VcYBxOi3QiNC$3sRO;Af-rgQc01ONEKp9%8}}dtWK;+c~Y8GRb*9Chg2pNNi{`QBQ+FRgVa=HO;SsdwMcD6)+RQ@meeQB6xoc}k$U-mQ$y+!C*nXFkVeE+k*-8dnvlk%sUn*adqvt4M@2dk7e%@dH$}P;cLE@KC$8vSwgr73E&pCv(Ysnj?^reG{i(wDESmAo#qx8iv*%lT8-MRzP+m~11G6qN#rXT`!f;{U<H&QN-nYlSKTPz#t5u7wF}qs}<L_e&%I3T)i{}cO_L#ac*7&>7!m#N5TRe;2X=Kj(fh=Puv(Z1&jK9My3>W5oJfe5-@XWu@rZ9EP3tHdYoEqQe)TBN<c?uS-G2Qt4jl!@wwXOeK^`OD{HCBdye*NU84Vz2v#+H*KT4&<ygl3XO?^^O%IfwB&d^@i%vdMED>M6ggRYAVBG{;20_Ssf)vbu;oqiH7Nb@+B(zs%s;@{F@h<qh}FVAh;E^5;_y@}i*`$oGAGTP3Hvw37Xja!{mSF3w55Jgl00p;s>JbkbF}tXorlylAJ;2i|62`J(c?Ij!VjvW(C3YRR)6JIbfR4NNo^Z=WBRx6j-8Kx)fXHO=I_&}=61bLXHoQr8pTS(BMLIDcasX~4lB%yCE-I^RXfwSP%@W_Av1V<AcH`<0ZfopKnj!?#OAYe|<6I>?Pa<s!ePU2l|^rnGM^d!}TV=p>J<BULS}mZ#R<i=zEt`RXH<9vmRI{Cos6Dt|&laeuk^>|7MtNndvjXSC`fUw@y&9`wG6K{dL{LnX#|JD!iqNtHi($gj1>8Sfi!N2J61$&bbBi`Mr~tG05GRUXUE$`!6Vzg{T`l5DfNj9l^HLB{uund~q3E&GivZN!k*FFIHwXRR+Kci)t2R$r06NQd7it8V&B3$x#_Pq`=1`$K@_Sm7;O@I1$4&xrPwNT1(JynWGF{C+rU*Fm~9>lJITpW*s$fs*ggJf=xskD@)m_w8KQM{3umm>d#xjQxo5k<vOBlMhwOWxO5HzT*4xKJa!#zKO=QRx-O<N-k%mWOg>j&z96za-jUrl{8Z_qWsU0ppy4ED*2C>lC$|J86GGZAW^<8jh{y;uE^p_Hbs>0vWhIL<awo)Y^uC5H>?7sluWUzBC9HSAyqO+Cq+6bnN?9GQ<M}bDH&EZC9iC$WRbo~2575fm3~Uj*ha|&{gwQ%qmmZ}Dw$vhB~R?E<b?TIU_&LZ?4@LsJ(cXRv64~tRr1O{N@mzy$rFQ>%%#7Qzc?#7WVn*wX_YL|UCA_cO1>GT<cpz7W*4XAkg-a>I8ezN2PwJUU?s!*KWLfn@B'}
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





HULL='coral-reef-fractured-ribbed-hull-section-01';ANCHOR='coral-reef-fixed-stocked-twin-fluke-anchor-01';CORAL='coral-reef-branching-coral-01';GROUND=.125
placements=[('hull',HULL,(-.55,.4,GROUND)),('anchor',ANCHOR,(2.15,-1.55,GROUND)),('coral',CORAL,(-1.6,-1.55,GROUND))]
def rigid_point(instance,p):return tuple(p)
def stored_point(p):return tuple(struct.unpack('<f',struct.pack('<f',float(x)))[0]for x in p)
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[stored_point(add(p,t))for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,rotation_z_degrees=0,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values()),coordinate_storage='Exact IEEE754 float32 after translation, not hidden deformation; native versus final GLB bound unchanged2e-7'))
base_mat=len(PALETTE);PALETTE.append(('SceneOnly_SandySeabed',(.36,.33,.24,1),.96,0))
v=[(x,y,z)for z in[0,GROUND]for y in[-2.3,2.3]for x in[-3.2,3.2]];f=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];emit('SceneOnly_ContinuousFloor',v,f,base_mat,'Single scene-only flat seabed support, no extra counted model');FEET=['SceneOnly_ContinuousFloor']
def layout_bounds(v):return[[min(p[i]for p in v),max(p[i]for p in v)]for i in range(3)]
def triangles_of(names,vertices):return READER['np'].array([[vertices[n][q[0]],vertices[n][q[i]],vertices[n][q[i+1]]]for n in names for q in G[n]['faces']for i in range(1,len(q)-1)],dtype=float)
def ray_hits(tris,p,d,length):
 hits=[]
 for a,b,c in tris:
  e1=sub(b,a);e2=sub(c,a);h=cross(d,e2);det=dot(e1,h)
  if abs(det)<1e-12:continue
  inv=1/det;ss=sub(p,a);u=dot(ss,h)*inv;q=cross(ss,e1);v=dot(d,q)*inv;t=dot(e2,q)*inv
  if u>=-1e-10 and v>=-1e-10 and u+v<=1+1e-10 and 1e-7<t<length:hits.append(t)
 return hits
def layout_validate(vertices):
 assert set(vertices)==set(G);tol=2e-7;names={i:[n for n,g in G.items()if g.get('instance_id')==i]for i,_,_ in placements};bb={k:layout_bounds([p for n in nn for p in vertices[n]])for k,nn in names.items()}
 for i,k,t in placements:
  for name,g in ORIGINAL[k].items():
   vv=vertices[i+'__'+name];expected=[stored_point(add(p,t))for p in g['vertices']];assert len(vv)==len(expected)and max(abs(x-y)for p,q in zip(vv,expected)for x,y in zip(p,q))<=tol
  assert abs(bb[i][2][0]-GROUND)<=tol
  assert -3.2<bb[i][0][0]<bb[i][0][1]<3.2 and -2.3<bb[i][1][0]<bb[i][1][1]<2.3
 for a,b in itertools.combinations(names,2):assert any(bb[a][j][1]<bb[b][j][0]or bb[b][j][1]<bb[a][j][0]for j in[0,1]),('Whole instances intersect',a,b)
 contacts={};floor=triangles_of(FEET,vertices)
 for k in names:
  tri=triangles_of(names[k],vertices);mask=READER['np'].max(abs(tri[:,:,2]-GROUND),axis=1)<=tol;bottom=tri[mask];norms,areas=READER['normals_and_areas'](bottom);expected=float(areas[norms[:,2]<-.99].sum());report=READER['actual_opposed_face_contact'](bottom,floor,plane_tolerance=tol);assert expected>1e-5 and abs(report['actual_contact_area_m2']-expected)<2e-7;contacts[k]=dict(complete_ground_contact_area_m2=expected,actual=report)
 tris=triangles_of([n for nn in names.values()for n in nn],vertices);rays=[]
 p=(-2.35,.4,GROUND+.65);d=(1,0,0);length=3.6;assert not ray_hits(tris,p,d,length);rays.append(dict(origin_m=p,direction=d,length_m=length))
 return dict(instance_bounds_m=bb,complete_instance_count=3,distinct_old_models=3,new_reusable_model_count=0,whole_oriented_triangles_and_pbr_retained_before_float32_translation=True,actual_full_base_contacts=contacts,selected_visual_clearance_rays=rays,not_navigation_or_full_space_proof=True)
LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate(vertices);result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,.65);ORTHO=8.4;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(7,-10,8),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
root=bpy.data.objects.new('OneWholeWreckLandmarkScene',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole scene horizontal centre; continuous bed bottom at Z0; three entire unit-scale legacy instances';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
  files[role]={'path':f'assets/coral-reef/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'scenes','assetKind':'scene','theme':'coral-reef','style':'warm-handcrafted-village','title':TITLE,'description':DESCRIPTION,
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
