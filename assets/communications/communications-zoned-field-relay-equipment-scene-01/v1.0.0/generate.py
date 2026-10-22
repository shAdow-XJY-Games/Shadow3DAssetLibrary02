import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='communications-zoned-field-relay-equipment-scene-01'
import math
N=24
G={}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def record(name,v,f,m):
 if sum(dot(v[a],cross(v[b],v[c]))for a,b,c in f)<0:f=[(a,c,b)for a,b,c in f]
 G[name]=(v,f,m)
def box(name,lo,hi,m):
 v=[(x,y,z)for z in[lo[2],hi[2]]for y in[lo[1],hi[1]]for x in[lo[0],hi[0]]];f=[]
 for a,b,c,d in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:f.extend([(a,b,c),(a,c,d)])
 record(name,v,f,m)
def pipe(name,points,r,m,segments=8):
 v=[]
 for k,p in enumerate(points):
  tangent=unit(sub(points[min(k+1,len(points)-1)],points[max(k-1,0)]));u=(1,0,0)if abs(tangent[0])<.9 else(0,1,0);u=unit(cross(tangent,u));w=cross(tangent,u)
  for i in range(segments):v.append(add(p,add(mul(u,r*math.cos(math.tau*i/segments)),mul(w,r*math.sin(math.tau*i/segments)))))
 f=[]
 for k in range(len(points)-1):
  for i in range(segments):
   j=(i+1)%segments;a=k*segments+i;b=k*segments+j;c=(k+1)*segments+j;d=(k+1)*segments+i;f.extend([(a,b,c),(a,c,d)])
 for k in [0,len(points)-1]:
  c=len(v);v.append(points[k]);base=k*segments
  for i in range(segments):f.append((c,base+(i+1)%segments,base+i)if k==0 else(c,base+i,base+(i+1)%segments))
 record(name,v,f,m)
def wheel(name,x,y,z,ro,ri,width,m):
 # Complete closed annular tire (or capped disc when ri=0), axis X.
 profile=[(ri,x-width/2),(ro,x-width/2),(ro,x+width/2),(ri,x+width/2)]
 v=[];rs=[]
 for r,xx in profile:
  ring=[(xx,y,z)]if r==0 else[(xx,y+r*math.sin(math.tau*i/N),z+r*math.cos(math.tau*i/N))for i in range(N)];rs.append(list(range(len(v),len(v)+len(ring))));v+=ring
 f=[]
 for a,b in zip(rs,rs[1:]+rs[:1]):
  if len(a)==len(b)==1:continue
  for i in range(N):
   j=(i+1)%N
   if len(a)==1:f.append((a[0],b[i],b[j]))
   elif len(b)==1:f.append((a[i],b[0],a[j]))
   else:f.extend([(a[i],b[i],b[j]),(a[i],b[j],a[j])])
 record(name,v,f,m)

def earclip(p):
 cr=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 ids=list(range(len(p)));out=[]
 while len(ids)>3:
  for j,b in enumerate(ids):
   a,c=ids[j-1],ids[(j+1)%len(ids)]
   if cr(p[a],p[b],p[c])<=1e-14:continue
   if any(all(cr(p[u],p[v],p[k])>=-1e-14 for u,v in [(a,b),(b,c),(c,a)])for k in ids if k not in [a,b,c]):continue
   out.append((a,b,c));ids.pop(j);break
  else:raise ValueError('Non-simple padding section')
 out.append(tuple(ids));return out
def pad(name,p,y0,y1,m):
 if sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(p,p[1:]+p[:1]))<0:p=list(reversed(p))
 n=len(p);v=[(x,y,z)for y in[y0,y1]for x,z in p];f=[]
 for a,b,c in earclip(p):f.extend([(a,b,c),(c+n,b+n,a+n)])
 for i in range(n):
  j=(i+1)%n;f.extend([(i,j+n,j),(i,i+n,j+n)])
 record(name,v,f,m)
import base64 as _payload_b64, zlib as _payload_zlib, ast as _payload_ast
_G_LITERAL_ZLIB_B85 = (
    b'c-ri}TaPU{dL8&*^fE8$Lhw%d&7+a5hY>8u2K>-43N`8)cf+MBxi1hf^XF%+?;|76ImyVg;zVH}w6kz_CAl{jKVBCX86@L>`+xuHzy9u*pMLx=zx?ZufB63U'
    b'|M2sle*F38AO7KopMU)6`|wx){x`q*&A&Uo8*SKsC8khg&oAM-<FId9FFB^zU&?o*9{4Yeqov$y`fo2+$nIZ-T1v{}8d^Nu$VVC_6+lBc?7x_L4!vALTlR2A'
    b'!OywoJJ9Iia;rVHP;Vr72h~dHO?r|0X|&Z)ddNvGB^|1iQv2>O=z+Lv%PH!0a|IPz#0}^d1+1obQ%V<5rEadEUvCgMkY6t(V1IMGgcn8<U(!p)-~3WuD*o1&'
    b'_Hy9w@e=3v)%^WsyaYM|kl`f|8{$hyFM+`V3c0*=3&;@b=WO3afc<ZOVWUd;8;UuAax-v*=|WoIpdazOE6v2wUUXM{X>c?;LU31@NoNA53;&oDI)*vM3kv|h'
    b'Uh`R8e3k<GK~3R61r|04ly5s)4z(QtZL23Vk&9lFdPUnyXbvGBp&`TH)#}g~!!eE&ub?@kk$VpZx=Ja9?H9<FP}?cQfL?RiSJC7FZ6ntsrEFGvEwM&?mGNyH'
    b'm&oAh4QQwp0f`*3^b|)&M)B)qR&%yuI!e!IgKe;zkK|Y+qa*6e1ZT8hggnq(@!eq*0kf9k+8atCx62|9#J1iNx@stF{rK6+sg$FjLxczAbkXIM%DI3lP2viw'
    b'w8Ts7*Nf>Yvr6q;VU<>KfmIsg2d~}bwdA}OzGDrd&_)ggr5uCYUom{6rJ*`U@1>$Wb(tmrZS^Q<`Dnig6_d(MNN*=HbPlK)?Mf!ZfX46X%?EmWH=`O21KO>W'
    b'`hZdaPZXK_3B}l*V~A+Hx#uD?6Y|;!4WlP8O&v|<L#>#$9Zss7E2PjME}%*?yn+g)bOBZB<`Vk#7I6g?+TjPI35@pFfB5BJfBxTp{NWGqoD<K^sz5o0fw2zt'
    b'(>v!-Xt?Yo7&Or^V(_7*2X+Yr>+QhE)ONsfSeTp(`c0WQ%m}8k#sHqSFq;Bk%*y!~q2I9A(02KALIdn|0=Id>&t{{?QfgRf>umdI*CCGJy;rp1Jc9o^%Bty^'
    b'QVi}2@oiz0Hj{uhpD`o6LY95leI36|o@(Yzf$V@{k?f$CHN6YGt!u3aw|3q%VIgz>zf;hGNMAW&7+=&+h{JxXNWm+;*pHy6Pe{mq%rEH^stQhM@e@L`AMwS>'
    b'dG-^?>7=0k6$(1%iUq@EM!f`dgE0yRvxY)EFnm^yEA^_emLAGc5enl$uVE0Fq1RJA>VR&J^`fm7G&x#KN5lY@*b-XF5o5}La>nS}uG*?*a@T~ETyC3f$$elB'
    b'0Ifn{-%XqJ8WYlo9Kc42mo{^R&0`E7vy01`Qd?p-MRBCdd}>B_JkX&cIK``&fIwoguT%(<!F8D<7pROYB(ea}gTgr)l#F$4C=_4L!8ERoa7kOGA~TWSw~YED'
    b'^yrudjpNAU;7Zno%{<&DK==Tc2gC+N67@`vm!u_G+;WMO&5O}WD%<^dRi@Q~bXR9Eu6zL*Yic!rFxXuNJ7<LfD!BOY%@IND+Fa2^`$H|I1Pu>~tg;D_!7M_+'
    b'Ls-|OGMH-fO;?dJx#^q0m2kv^lMTxFkW?xmvcV!cl&`>4mA+(~+l~@2;p03op;*D$cluat88aCYK*aRqR?o&Llu`PFV(730t8`KhHwx5o#2XAIncQ)vl+BAN'
    b'gjBfONkpDTbMq%DAN=(#{PlnQ{)hkm%g;aj^nLjLZ-4lwA7AHz!=@paV51N#^gA@bftmuju;6P3FK|^eqW7Wgku2KCYiuE>a3P}ww5dRBM3thy4UketD<c+t'
    b'Hnw<hp<#e++BqB|LOy!Icb(AG4h(OY5*2)(_*LphD`=S}!V%5cX$mNUH4c%}kFmFl6vY_(Na%7Mu`Ii>hK9}qU`R3deTEae*MLYsc8_@WR&Z_x@Ib!V+?cy@'
    b'ASJahP@s6S9D^=PKVSsyxQ~_UdZ3r!J4i@G&VcMvqay9`U|;Z}1|8=%pfNBzf__`Ym10VK*oM+NE-fR7bp-V9l<LHyUoZe9Y(rI}<HqlheGqB|eK+VlTi^~5'
    b'sTfDl9BSw_pU@KUOGg61#<t*uCc|bBFb1R?o392z)iA<<-&T^5_ris#5Hay;-JU8ACK+jgiYXX{%y0(Xqv~@+NkFYS7*&#}n!(xu6%!c}zXz^e)x^afAN<n5'
    b';Mcg0#e^;}t)Un&y9Cp=cwrb#t+4`17!Xw_6jQ{;#XS~I-DeoBA|b7XCegN6k~v6m-4F^I4JB;L8A-}ioh>8jZIu*6dbc&l%%<LnM7EE{&`4(*W|YqpLKzSN'
    b'M~vfx=DtdEKG#ImpyQztVGeJD4w?{4xJHb7n8Vu=%%lvEOg}JrDjf}j)kAOtxncT;!K!hokytPn+IB#*kLcpY7?3I$$@)NDHcLIApo>BuXfI+qH2~$)`~qS^'
    b't3wlTzCgp|LMD>fz3Z_dqOBhhqj~M2aXEQs6$%b>0@_6U18JC8Hgq&5bPNuh+suM1Fn-37TOH`3E5-PRZ4oKX=zG~Rn>d9<${IKp6-cv)3EYoSqZclz&)ilF'
    b'>L4@>2odCDScHtwis%(gjpde0*J#^NW1#O+XCV&^>`*ZH4m~ZUtzGEW15)+i6pS*!RbOQ{#ti*19c;@qpveZ7$8Z3v$cS|x1PKLQ7$k%KJh2fmVTd?Th>Z+P'
    b'nn4^85=ardviDichf%F1<F~e~B68#fMO;v@Mlu|aMgb*Rr8!feEmf#?3^gT9fs0lG71YrHz!IoYTgC@7L&2kIVi>E=Pf)X{Q)(@g=akjt2^Ml_sWFnh*~W)}'
    b'TzIE$Y<WV-YMBEpno%kHyn@3}{!jxPHB(zD#()eKM^Zq1G4D$lDH^OFjH8r=(<<8asG%Nw9*d#HN1w)J28?)oT<S|AeBuda#OQ}%=!4q6N^R#Pw2_@KW`RR8'
    b'XJ#y4t`<N|gF<pRit|Knl>2-{1YP7+gH8ic0V)A;v5gXnJ`IAQ2q<KvNfeo}L!6;=Pbk|fT31ROL{l?jtKinosw@R#qw@q*9T<Yr3Zvp|O-Lq~4I~3NT1C9D'
    b'd!Si^C^(&~oD!bk!RL600l7`v?1Cqd*+TB@=w@T38T1Z;G$?9@(-Y!F597=d^0dq`02$*v2xjZ-b*<X-wFvSCXC_NArqjqgI_^Q0=w_k6U>F@1YAKdgR&aN='
    b'YghyOZp~)yfI2wDS4z+HI?Lm}B->!c1ssG#E)S*;{Wg+rXP-s)#YliIh(5R^<H1tJa6{?V$oZ@vut(1zthKKJEoWdpRggq9k`qeZ3nh{`w_|O9gb^fm@-|A_'
    b'r~+&Y?Uj)clWr@?7`9kHP%k7KVj<ij)DBl(k?7!Tj4=)6XOHt<wRx+2B7ou1)$qnD$r!>5Z3n!MA!N-H(U@TwqLbFsHnWw5NVamhy^xjK7kman2cumSF$N|w'
    b'EQb&3<CS3gP|lEr7?Pr4M@Hhwg0YP14@+ycp%`jCA)O!W_71zn&*!I<0_>7tFHC8Q4Q|6kF>0|=^9O5AXiU&h7_iX1&=}Y31y#y<UgZoGE!`D4m~ODqb#G3f'
    b'Kr~h8I!cJL6nUUX;FvVHreJz8a190x1&uo-lL~x_U8&{3jC8Jv0LJ>ldFY_N8DV1<QE@d6;t={{wSQ0;C%ch-8Lj)M`^<7GgSjgv&Y=Bz&Uw(HF=a}TLuqm>'
    b'W;~ct9NZSf*2&z4NIBZ525UTLF6_sFQ|JP1;#vm9!6mCoz1nTaM<Iib4|co3y<q1wk2(N-mk;W_w`>eUI-#F6J_|uFZ08CB`v_-PnD18hT5c7<P|!#znG>G~'
    b'sR2FN(Z!JDvG$`OT;hrv4B+R%u7^;OWdeB#0?P(Pqv^~o1`y2g))E+36~LK;Gyi0&v~y{V+ecB~6i9{*eB^^-pmsl3&rm&yE1{TNV)jQUXU*IMK`qQj0)%$1'
    b'O|c;a*85@$j97vDFcNvNU6>uH(-9z+P}Z+24~=4&(|_BPvdL_+1{&BzIY*A?vIFaZ3C0kRY?tkuA_f#=3nGH(!@yn_lnOMnj58;%wzrq#;y@Bun_xA!%JzWK'
    b'Df3Cg2f2Nf+~SgMDE`bvbWHS6O|}#}(AILns0-qNh{%&FD67DMXgM{W(+>v4d<}vDy~-pxY9_L?U_A53L}(B;In1^*@SF$?E*oKJ#CX)X7l`D>;ht3sKJ?z+'
    b'IW0m9h{L#Q%^@&ef}k+)ab2SA%~lT4m@s5cVe?qffY~T$1`LFD-}bpBQGnUFXNaqg3yQR1qy@i$8hsFe!h}!@_8`p$;l>99Ac}Ar<eqNmtVl_kY~cnYIy6V3'
    b'U9R$2TDvW1b6t(%tDkeqN?qAG3m-jxX_3p1nVX=faFH(WF;D?0YCdduT|I)lz|0&42K57hVLb-Lg^UN3^a7&(ZMp@y%IQ5#bk2}KAKW+v(UNC31x-@%b1h&Q'
    b'ZI!cOHU!Q_Z7UkXVXQ)la52xVa>D|o51-q#MWfIt?DL#@VGLk`ImFqTKuwTiB^o86Tn2K+qFOsnBdQGo8S{M3QNzxt5n<qJ2WN#)p$i!zm+KP7Yi=5eyUaTO'
    b'4nDTx?D5Pj(g1OPkhvmPjCVzByzgsphmFi-Wws(MXwjIHqZRlV$<<))^+hpq;I-`9Gg{OV4CN0-`#Phg^Kn8$31cpHaN2<p#bh|@kh8@+xMk6FIFtle(@?+M'
    b'Q*mxsLLFvX@j~lPbFPB{oD<B#{%=@z!ok%!tN(>fY{mR8Lbx1;MNa_xKsSMxN_7#!r{NS?prUhKK5#ck;f|ibq+Xb9&1P@xotR~vPp7zSk@zH`vi)9Ums2Q9'
    b'13GR!wGWviV~o#ClFwLZgZooV>on(nwAfTEF~`zt9n=kCrW)wkCcG%n!;~oH1p*rsKON*ODy8%B2b0372-qjS&g?$7iYb;4<^wb^#vE}VB+zRiRq!7qhf!kS'
    b'R`t#$eoT4F?6sy!Dg1g^1ddX~)Qg=ASph@Zo>%Uqfd-+TJWToU`3gt`9N76NXF(I^T!T6Z>d%>xdnu3vbaw9NCA(qxLfb*?T!s&MB{`tPZGS5tH5$=yE&v#4'
    b'1okl9Bdc<K0_B0Rs-(3yIP>XJL8W5Km?^OKcF9AW4uF18n`<{S*Aly}<)MUZpYE60B_X3BK~O>Y;+M6Unb~)|Aww#MdQr+4$S}3x0t&Y#tx}G`o;pEy7m9S-'
    b'<J%6?<s1h&Hn4`!ss~#h5|764!Ef*ITYB@jv~!rjsFx1w?-b1Fju`JMlymU{<|J#FvOn^<+YyS!9@X;+QTM41v<`Ghv4v2d>J-#xLTftM_120C10^;L^hylP'
    b'ro%Huf8Y!dwQ5ZQsN8J$?OaJ;#K;Gc+$O;11oqT%XBIOCu;t(*0uJkop}0<EbG@TsLU)l{9;E}b1^z#s&xW~hLP?p7M7qy)Iy(}Vk%zB?f%_Aw7~PMX^3N3{'
    b'HudED^=pVe$10rWf$tDD79Zj%J|I@OD)YL_3JI><F95lL3EzcXTSSkbGM3h?Ay6e|zZsnorFtZ18g@DMPiDKI{XuQz3L-<FJWyQg<PKLxQLD7c2TjIrhiPRb'
    b'nc}G$7DE>3V?HKr>(o#6xjk5}J9A@l%9TJqz^<tSm<~3G%%>0dyMTcOl0Y)0WDcE#5`)_3f+<qy*n{U1AbmLY&0<QJsPid!#87I_lXq58KA7588_mwK2a1i)'
    b'894th)YVs6tu|*zgW~?7mEyyWIC0XBN~(Qdz!3Yk4~27&HEh|cL4ZVNMOI&qz?ha2k1`+wXeH6Ca`^<qN5-fZKQ@AVo!QRaxR~V?Tb!aq!W_v;7`>QF-rPAr'
    b'mE%l7@r?!t1%0f=Cy*kakYPmYcBsQdInTlHfdo`^v_+B3#j|D$YiP@}X1N^$O_hsbA$t2qdw^ELY!CCOjK*t3f$3}H<1!9;Yc4=#&xiORzU<GvHdgsqfQwdq'
    b'Tz{N15VXX=HEGNmgD<r0GHY9&*dHQSd(Ih1BHcAkZKy45=7UCSv*M0~H^VkQ7vnliWYXK~bjzM!f&<Xqjbbu)Yh;R59;PvRLU)4DBo7v-h;xp}*(j39rytZh'
    b'7ly$Lh!Q<4*<qxqNDeO1#Q}Ye4s0DBRRzNsMp*hNA?rWI_EDsS&U?Hb2<zO9hgliVCOJbfae!6EQL}ejXd`M%ZtAbgD!wq$aujfeO`I!rY~%xM=sMIltwM}*'
    b'm5HZ|QeQ{25TJ9z2Y3GYHWOQ-<lxvM2MA;1-YIP?y>UGvLfhet5aS~9W1CiXR=GvzU=F|{>**?f<~A2TI6^+I@(McUVl>zD>QcDq08spa5prSmqI|gtr*I<>'
    b'X5e)pA?MMCArKpdy|W@8;}q5dANCp-V|YPHLRnxi{+N?~o!QO@q+I@@+{GAz;oY|W*xFJHd|trE&AwuQ-iEOq{kl?BPeqLi;SPa=B7OLSZ-(NoCLVxm_VAKC'
    b'(Kuxtoc+}``QY<bE~l}lN1rbtCf=C9feYQl?SewsRMDl;q?TPYW<DQff)Tb~*o6REPXX9b*5spe&4W8xpeFsK_9nj&dWb04KDDxvOakW?Rg^~KgNtB~0z0Q}'
    b';4n^Bd<=kq<@3=%&RJ6}p0wuPlEUZzKGh2BBuH3f3Aj}-F1M_d#Od0a;n{AO#ua)}>xETJbSfn!=R56`ii0|g(^=|SCip;UAXwne7?_>?6(HzXZcdv|q3tO^'
    b'wq5n05U{UZ1yPWxj->JVO7$L#!HO$@gPT*s`FIqJV_RP{^(c{v+s!gJ`Ilo#Ant~!nL9+dO23xld*yVI$WX0fk=D!=Cr*CB+(w9)BS6(8+xfaC5Zs`_eY^G?'
    b'$Ov&~6f}&X95RTb^!bF74{5ltQVZs-`;1m@=dp(t5M$|F8=<)88U;7UTof+_7wly|jW~D1%}u+U$W{zo#V*?5vMW?2mqxoOOo;f%^+s-OOdopfJyy$~&qTRS'
    b'irT?sZLsIr21&MN6#MINixS2#hTadxVQW8UIteWXb(pxF*EUjOxMO1gIbf_u*CrIrk82?4te8qHA<o8yrovrXJa=qZ+Z@I18t@+mEl3iSe=1xwT9YKS8cYR`'
    b'WZO>c1oF-*L=$ra4lAvkla7wog>j#A7H%WD$ZY088BQfA3fno=8PWC%lNNbGg3~0F*ukVg4dj_y&?O&}<idUB=WPywYh8(t^Eu?3l%Q_FG>3aSAS$hp6FOi<'
    b'&nu(E*V`O;wT&$dbv`4$uuB1p3SqQh-1Ec_XO!He&o0S+2kJ^bueB+#9f82~EOQdZy?y6#%v5<Mz4NhWuqjsLG9w?-aLvMx;B(_DPk}()e)6=Bd#sUQ8z{JT'
    b'#7>^Ld}Mcj*cpb*by7Yyjb!Wcy5pm!$Q}6{+sr1<Xg97rK%t_n49n*P-JXn>bImvM<T(#Upaio$X4zPU^6K10iQ%fgvLPyro5F3xNf-GfXJcLys+HxrB*JGX'
    b'gIm6lk9twKe9pkVEu3<UmE6jWEqp#edb3@*kq_V~tW8|o@f(Q5%r%zIT>>A=YhNd|^MPpMR<Fb*W-iy*s>F!4+kz)dFvXk%!D&(LCoKhAAi?*1Jk_`WWAYpG'
    b'K#bem28Fg`%LCl6&CQ~m>#m2P^r7{QdGU%9+QFsagBw24i-*wzv_8<BTDG<}vPG^KfpRb=vr*Lxvt&7Ys)p2^GYxz4%S=FS`f$F<Yv3IXnBR<(lxVbp;A{bf'
    b'e~pqV&sdO+xQ)I!C2^;3<AgpeU=Mb2Lg8atTMXw66%y+p@Ac$~<)aWj>Z@kqoX7EbGvJk^UoUK;19L^0+x8LbJW)DqL)hRFcILu2pplPq8##neRJ@~dBP#kD'
    b'xR48rj)fNCQpDf_9@n$%Sqjgma={)({MMDi)k)6(!Yd7uQ3jvY1fGzv5e}0`+gX8`R^ar@=>cO0bT;zQ7L+qHj3GQ7g@MNRjd4!bxmScw1wFxhT-+&Jxp#UU'
    b'OfEJH96XYN5-k^2Gmp1K&J@UE=aF3qK#KOmC#d_ZvIIHDj;~AzE<fyc4pcQ-VYw(^K4fB|Aq&w#R#wrNdHD(CTk)GnxF0a`(JuSIJVnN5!@SeTW(WO)(7sM+'
    b'ug^odioyG3Fd8&oOGoLA83oz^9|v*i!8$9qL=_V=X?2{=!HJI=P?xMo6VOMrvrv52)q^1quBo}Wi{~CCp7OCXzfe3TTF~pc%a^B~c&NyY9=tcE@d&`F(YR(2'
    b'p{OuR<-U)wH_G`CS84g&y`LK}JI^%_E_G12UE~xEE(Cj;fQe{)9m~1h4M{v~ao=V(d}7x)ed6X2BX5kRohy@E-fgebDci{f9s;RlpHA^1K;v_{TBfGte4De('
    b'<5i!bKKQ`VPE=)ooVl}_dH9KYxDvb4JZ73vo|zNrgRAep_nnVQ`M4qso@%hp$^&2AngOC;bKO8v37ni|KE5{E577@6lun^&ofR6Xa|bD(Y^+nU+@l@&ECscO'
    b';P#xBr&S<}xk0<8VV!kwyB124JNM=gN6iVI9)&9i!!KY%_9`Dy6`KJX8QNxCE~GAf#&#3=#FACYDSN*#%BKhiN~zdErU~WRSLeEB<{`tr&uKe&e3>g-6#Ns('
    b'UW18fpy=zRTokVzc8Exa9ok!`oGE`>;B`aMv&uYkE3R#lNyBgKs8AS~vX=Ux(DsD(AOG;npMU=CKm739b!8B{v!C@%+yvci$0a9&pI*O&ufnW}P3Yzqnc8al'
    b'!Rt3xXpGnME>Lt8J~te<L*GluCUl(ly4dN0a30XsOzGfFuC`#c0N;W?ZOm-6>66CH#%qV#&}fSN^((3Z+GDl9b>i|2*X)idwy0`<(J0?-E$8zj9+=}kSLi=('
    b'B(&q=cJ%Sn>s?=~^lk9Sh4Eva@+~~mx`H#;gPYUBVMiQ#zZdvsLbkzom8O~!vD-Xdv^25!{;jo^bB%s{p84@!9c@BiS3kFba?fJrG8q+jPd7u~ONm_JvMCj;'
    b'Hy5=4|82CEzx(A6zyE)J`T0+qy9;WXH)C@J#_s{}6BWFjhbPkQ7+Lk3p}9bv;wc<?AuXgYmpHk!WOoSI+1P}Mu5C6WHgo#SsXrCVdGdg}m+fr-VHXn;S`Xe_'
    b'!DR_swBqiJPp#H|%WmRfv0ix|AGH(4>qa0U!>Rd&*3fu1&tI!v_?nx+c#O$Ul4V$Fja%8E<->b+c}m{a_j;j>w5tpFB!LeB1|}4Cjlxxq6~k`}`hbv+1lkc*'
    b'-kFm8d?Fu$B#yfosxx0<GfzD53QtUEcxu=V@brY)N8_<#KT5Q196U;skiO*Cb2dLJ&Q(UP%kUVRRr%H`mlh#O?a((TJ$~?-_p;b-RUS3EC@9hDu7dR3Zd!(3'
    b'%onD4WdSFy%~oU&I~o~|G-#UVC|$X{&GLul{yNj0*B96!EYb#7aEd(+J?z99=d%No9zTA%t==7$*WL0M0ax+cJC(b^h9huY;o!pqKHj`;&ywM7H`21Z@4Gu}'
    b'!o)GzK|UUHzGXIW6@^cYxN_Fpz1+UFyCqmIrhbOj>*xY2wT%nxqeN@PC0pK%ziNhe!@gM1s#U2geDK`YdG7TtgU<)DBoEreem;)LV!^Hy_-qgpN3a`KuX>P_'
    b'-HWdKt#aYt*;e0AbxPD_ifVW-oO#oF<Th-+q@~w8n)}O(=I%&+ZtFz99lTHps#6r8^U6*teLl!5e$eKI?p4fQ32rI77eZeu<txLS?D5`*#yOugKWT3B!E*1h'
    b'T>R?16?K&|FI4K>{xI)Fv&L+f;&JcQ<@}Ks*mA!!_W}DOkQUjPxo??g+SVb3&AheokvAVXazokhTavs<1$%1S(haLzPe7C6vj*Ota5-h&<h9!2u2Jk59g=i8'
    b'bF6kCj)w+-oR>3g&Ay$nR_-o_*<83;!?p-qWL7e}FJm4vwzFRWe8@X${OX6po-gz1uHWpm$8xV7#-My8Qii=}fj4II`jVUi@5F4E?Sh+CxPcv%Rk`8G4p-ZG'
    b'p1{jpxI^pGFt=0l8P}2cz--vzV;<tA;e*ezN4PF6&G5F8#0>8nhgQ;iyF5)&jp}($)$cvx-Y_0l;nU7!tG;jY`$2MFC%JR||A46G3Cn1AnjL;Y0dLfRbl~~Y'
    b'8m>G3TP*ALI5;$OGi&hPyQ|wRG(<ZgZX1*R{UsM|S+aZ4iKP5qblx4-c1rUpH21=de$OyB|L`)ygAd64iLaRBt>sNo^I|uiw&mku?zi(R6_rZbAl0U^hkk2%'
    b'<#JNZ?kY&k?XF>nMJ!s?`oRaseVyaZ>1yG5PM#^^x%A<8)M^7Z@4x1q$iuD@jzN|Q!S+4yX1v6gIf)~eYH{0dv|L_v*U&Pz&hXR<rkg`n2fQ2y(;A)(tUT);'
    b'bWNgKy->+-r%$rLemiT^b^Y7fqAWT$(^OsTN_O`eTgvW*v{y=bZ}sgARhY$m(As;nmcBYa#W)pW;%?u{I~MIep=b-DHQ1%p=k1SgXNo+f9)_I?^{bS4TZgZ<'
    b'@X*^h4<NjqpYj!XcH3IBn-Ai=*@wGglI_~<x>cSavzI^xUbhjC>j~<c%-ZD&_SRrK2^-#dw23TK?z0A;^48vPY4+^|m8W)TmKXT(UboB43RW+QID!JXT{#w>'
    b'87}h*7hb!{%h5rMbzDL#1{Vw#o!9O0T1-1_&D$NoIKA_N)PC72A}`^By=3nYnP)J04*9VAJ<;)xc4;{BawfZJ6V>cD!E=)f4f7g-gSzdas3f}=H6&&Ds%0nz'
    b'ePx%Mf2!>`MPB@ZXP%L(nR0H}yIbC7_k-ZRPH?Yx9TcAEYOV5=4j)%pv*5~V<K|!9qh7D8b^{))8lKp<+ZM-lo7!P{QfhEtKC3%kw`IldRUc9^eA#(-;KJkR'
    b'iKjnOFRk1%oY{^Wue`4*oY%EU8Gd7TThMk_6?Fsec_{O&i&jTlsMt34*l$m<R#2MNZT)DO-M0&^jCHd@H~8SVuXEh%tp|yB!o|Rw_c24u`f$x_0C?>u@9%7l'
    b'XGCS0z>5oly)ULmN|7A3(Mz^^)p>->UiMi#5tw-o4Cg6PmI#3I9+DPX;k~56hH6cjXjZRu^4qzSEV18C*>q+9cBZJx&dmf>7Q2GgD~T;+_EOmkWqf7!?F3br'
    b'#(Z$wd)$`4GC>XB9rghK7<MYFHoy0bb<fw))s(L$igwN-@n|m3fE7C}#<!9Maz-JOm5bRakd;>#^H?Yk4+lSK_Su8+a>J^<p}5+MD@JP<lha*B{bdWhr;_W!'
    b'<6@G?({1)jA6|FQ-QV%j=$BJdo~h%tfL!GcDe~Q=mpRqUZc8}ZC0=}OMB^o!!*7S<O<mnC@tjw@?Xf&kH+Th9<rWLqih*|pH!iaCV0gG{6KU8Tdc1=BIOgkf'
    b'co^AU+S_<y@!Brm`oueB?54uQ7GL@1HQu-hvg(zWa9)*_Xm?jdVs^JJLoDX4S+obhc&S<9@}A$qmo2*-dkacqm)#F?`#QOulT*Hik>|w&FXHD57_41zYZc$m'
    b'$Jd*r%c|W#?Nv63S0jXBZy>v>+Z{G>ITm5MznSK;DXWI}eOJoxw(D-8l~*5hzHklB67SjNN!`fJq)2tiw=%pl{I;aSchRn}<DHkC*UiXvv_nb_V+;J|#A-#P'
    b'+T7HPmd{OlP>WWyskHtNX8Ss`ol{a?^~$$Y^K~jv2T>lQ?V=T4vcuQJ@all5YXjc20tugZ=@Osy2X)Z8V|Uwgq}*=1D;gV8%WH1<LYbIlWxyMB>@8p@!p^I3'
    b'ZwM0E>|P#!IbqU;^_SB$UCe(uH@qP>-%LsGh+NI?R$D8X-3xl9fVU>UoR4Y~mk(xpkJ-vsC!{gjYj^C{&Jz6v@P2%s_t3rG&;E95$g8H<GBF~tmDr^owy2V<'
    b'X2a!tlvnrCB-{E?O1XRkykwL6EWW&JNXjQKKsvZz#9pj-Js*u+5#*hBfp>}bOPg<}qmj3iWFEUI8S1NEW>hk|DO`Jx7Y{>3-hG(-jjDXlS7VQ3IhQLWuYDdS'
    b'4f%c_zl|yJ4rpGz9C<zVRa4+?(Zvp;_!}JT9Ui>8gm<A8zZ?3(XtHa<xQNB;@cr!{U?X0Z!b@7o<rhUH8r@Zlmep-*5X*OGm6wn5US+$R&0p%&kfRuQ6H?|~'
    b'm2s2T4>tQco1HVzVsH4fSC1dZdYKI0er`7e@LkmTvSK$-Za?JRynMeo-#UENoHo$R*T151R$gt^F59qXbk}jDobG$;TWEzwvbTlVJ$otXMl0X8ow;wS@ecKP'
    b'Bd0r~Z;Lm4$0sk4D1isd_!<qlX7*62J#3*5608-IZ1qjus9D`K2)TeoqhD?LAB^^OMmuMo+=9dViFrX}Z*z04GAaX#Lg!W1tyNx@n^h^mYs`4hJG2S{tyejI'
    b'eWbc$blYvDtnNE2?^bU3%Jxpq7u+gZ0MKf8aPr_bUj~z81tMGBN#M6rB2hcPorS4#{q59GQ<R(ermSKmn_KCu<a00ArJ~*1d^_C~<|Q9&_J+;={)gZH{MWzx'
    b'<qzi#e8+cuTe5F#=H-#mj|JO*d<Pe|w%h%5^K@?K`vhL!cEFc)qFwU7Y`%hl*j#y0Enj1b|J$1n?G6|2;)yNrDbM+u1qQEtIT>1UC9ByB3!}X!ooflaaI>DT'
    b'kH-MZrHH`SHAK6`O1IVeyfu&4<;K=;W%8|IUaj7_s!_S4{jfJ4@}-dD;7d0~<?F7>C%NPc-r1y~6EMfH$M-SvI{C^+e7v{4U6<$`V_%}V{&r-46OO&L(g>kj'
    b'8AUD+h4otVH_d?Sl=hZO>&Tei+rVP`?zvi-z#!?;D&NiOuS?~7JH2=EwVc7W(r|ymSvnx=&I{c6vS3~w=A_OGrg<2OH@m)GVE<)J=!V`jfE(F+YgH{&%U%ko'
    b'^Jp)RD`;79-2;C_d+ikx{lQf4G1cqo&x4oT7T#H#Db;QN)zR`NciY*$nN-GH+2xUsVy{=RE2a2u3tOY&`hZ=v5~-hg9r(f5#M<q2fpx@Q#+Nac?6)ZLY#eud'
    b'^XO1X5FZ5F0jX#&pXLSG?30vayl#f?w)3mMc^<h$-pd<{zb)*_aO`&IFYxsMe0i6HqrJR}`=;8k>$<lYwyQ!8djm8~*$_{|l^3i-@TUOk@f*1KR>Z_Nf3rPD'
    b'H_SN<_lPBg_p>z2F?#dC7w=}?ebf9P^sr;mR4&Etv_UqqC2v3$h7{KAU3}>y*Tz6voli$DEC-(TihQ|4kKAi_-fvp?3L=Pv%HwBK;c_*pkn3x7S&fR~8<Z02'
    b'^t>9i3?EEv1^bw<$?e1MHs+XO{Lrm^fF2lfcJi7~Wp))Rm66e3wO3_DzU(~lPHUHMA=`^{`3Pg(C=aVVsg7iiI^S{uwmvxV>U_Xaqnl-6@rsWT#=2LdWZr+@'
    b'xvO^YRnr${x!chmnD7N5YgL4IHfO&0oO|BvRkFLx^4=J}kq!fFZLd~&O)-TdFPu#mMLgIfD>vVkW4-02@D)#mufDRZ&X=!o1hb30?G-$PvMU^RqYIkB2fw|?'
    b'Z|8)vf8N`h+}Zz~y)E-onyEU=@b;b0`7O)z=GPp3N~}@mRi3FF$nM}9IPqPtDxI6z&q$`<pcv-&Gj{7TxmiJfMypw8RhyPlA0)f?o_av;c!2Vy;N_Ej4r+Hd'
    b'tDWzD#C)2WmN|w?29@Vskz~xWhSQV8Y<wKZcOz0yv4p$Mr+j#M@Fhe84a>?)rg3|EiQ?tT7^+7fI+)YKieflq^!VVlZ{@Xr_~GXtfBFx9_~-A#>lD*uFfZS?'
    b'{|fK;$7HSYbv2aRgIoLa>rT<+OALHlj16l$Bww7#cLVU%o##DMA^H>sYKOmGK!d*nn(tcgHQg}E_Y<aeaPhR4*Ovue1a9e*)rj*@HD6j`+u-N%bJ+}E{qxCu'
    b'^-kUtqx%AVQ!4YV9en*QI!`T^$Z`>QTjOsMD4Tg(Dm$oFDjVc=jqd_)Yg{S9y_vVIS;*T5BfZB+@oS9Kt$p%*9QOs58|2XKrN4pif8+AW9Y&gK!t2!!H;lIK'
    b'fie%s<@7!y@ufV&b}g;f1dH6Tw;~bJK5L56eR(RqX^*_<wEGHIxM6QbA|$a?HpuG=-v!=PxKe_9D-s`lnY9l-y5^(!i9+Ig&bfJ|@O@Xd!?Jw&oaJit?8V+!'
    b'%nNlIB`>_Sw9Zk1?>owugC`eBIT@^c-=)1=nJ;?c!sb94xKw>PcnUW6gPN4j{YXk_&r3%GS9R@?UP0r`T(pms@1eRLu(M_K@cEb-Ju(1+kCk{y;AK7)o7=)g'
    b'tc8=85&gxG_Qsb~P)LodMJe;TpbKo`dtnd02{C2frt6!0KYO-y)ff_Y1M?kad~GtizwNd?Ji+$LwSJl6#M^ccuDlJ@t-T5i6>6n~DHdj)^{SLKquZ*{vbt>#'
    b'VhL}}W;AXyo9z-1dnGw0e|!&dM3asm+Uh=+#d}<~A9w{`*^j#tm+i-0!RCHIl=8V9gcVx380rNo+h<d;xh-3<qiwNT|K7F*jaBwm6)M}7l4f*UHCk48%|R^S'
    b'tyPW5K2({`Wa$%C7F*^!xzWQSS6}a_mB2Ub4sP%3KJQZ%63>bx?xP<e9JY&DR%L?Ci*+6)pL_Mmr*)a{LFc^*_I7PiA)%RCM)~wU)^taeDK<BS%ky|#wPp!5'
    b'E-ZIhGVqaq;oB2N;G0)RuCh|$27t~J)gys_L$onQ(?@{D%)L>(!y}WqRZ*rI-PDYl)lG9y3wUcaV(M&G3vWNEACl}jk;QvNwv{RZr|gxA#AAD@BG|lG9#XQo'
    b'SDp%|?2Rfsw$G<xb5po#H`_wB&i%G2sEo2Vs?gY`j8vnWicxdAX$@-mZmmi*_MykVN@M@|cfb7MPygZPKmGXg&p-VA4}bjAxn1>`E37DGHUOgs?l|sNvkfyc'
    b'Zdh8=LLNU0w%?lXPGaECzsi?TyYu>UW7mO?Q3p@lRy5aWJ0Mj%ZOmm=$awCnct1ZIJD-2m-px<`(%6l1Q|$;v-oA@-pDpiT1G&#FsN1T&2&^RW3c4+dtH45$'
    b'UqJU&d&7=cZu_SCHt+|_7|Z;pfBEs}zxkhk{{6rF^N&CO=^uair~mQ&_kaDnAO85q-~aLZ@csY!<Ny7q@Bi+{AAbAeZ~x)<Kfk`GzQ_LA?cXoly)^d}52~D)'
    b'Z96*`X6B);G}f*2Td-Fbw@vkKd!#O~er_M*BsXK#r%*Y`BG!`<IY`I!PHvxIH`(1mwSp3noAk!A(I;wVb@1CX@3B&LAEi0@b%G)AZ4U8X!;rCW)4YdjMYYEs'
    b'pTEKHRv+47<xZr6ca2g^v<j8mqzHae(oe8zXMp0j*kaEZI^(T!{<X1B(!9mC;S-2ndOEl@@kWc@V$~KcgEyt6CR&B6En2jzW7Xau8vYXdsZ66BvlmHExpqJq'
    b'xvqg=v%hVIa~XF~Urhzo?Qb{zQ%#)(cLjr%rR)lSt6%6k({LuC2DMZ&#}Z?VYbq`}v&TG4zd3|IA4{WE*J!ZZ+y(L1-PK=Qw&9!M`fYgl%-`Z+u6S5pcxDHs'
    b'5~nkI0vPJWCf}VuTS_S{^9)JEi?t(^6uvC(DsGTJBd$7~^(8Wi4A=ZyI_p9)NOL?RBWN%x#}5l>_8W5>yE`KiHl}mDq{E%*@Iqj*;M?HN6dZ<tfZ4aigbC|}'
    b'S=*#DdI8aJda)hQj43&c0fT=_XL1;?Q-+i-(^<TbA|rjVvyyaXFVAR&>|qnbdSuZeE7MsB`){npTe>>l)YUZ_8->VYI(5D7N)rVaSVfEIP&vsWwyD#IN8n9{'
    b'+qcd^bm%6@eicT@obQHpKcAXk9sD-Yd#se-M`<oj`dpXf`)6(ymW+Ly<~>v^sy$XxZ5Mq(lbR2~O%>*9ixv&<n}-N~Qr1tfYIoQuRlT%+b?}o^Z?T$k+c!*6'
    b'GCl-1Rh)~hS~dKnxOA-ABSgbrVm}o2hr<5LRM_^^?7#f(_y6=i{_cmLfBVyqOJ=v^Lwu~q;KKoa<wq`7cjTQUB^W>QlAaLOdwX`!&+pQxm(bw+U3jxxZcm|V'
    b'f;DLR>@>qWnSFxY<aUqMN=nAQO>=eZ*X#BH^lggwP${!d5?u4Qmy?X$Bzce3N=n6UR*=MA@T(%#F7T^D)#mi8BEP+2-ar-M@ukq<0PmxEvvA)eJTk}s;G@1j'
    b'B9*1cPIPp8dh6m~J&p~h{s`0`aXwVGA-Ga&xE!#-_#Bt}Le%;5DNo`lVj_bzS3*mP&>1{Orjw==DW?=+z;uqi{5G7j$`ynMIHoQMpNg3v4Y>dK`~UvC?X%)|'
    b'c-sg$)WK^A?yRtH!Q#?>7(V4$i`b8`YNBQEW^G?CEfuRhQc%lEg{n^@)a>eD@ll4D;YW$yJ_b>XO9zWj6vfio+wDFy<k%WtNOPwrZJ=^T60y5hsijy%sx4B)'
    b'J}Bb{P`Mwd4}3Rfe`V;SB=5oPvnyxs4GKG~+?G}FuC&BNt5CT)Yj$<4+!r*%AJ2+ER<i!$SF*ko*72sW-Y>0dYG9AmRLBjinrIo^)TzWHu=p@REw1+MQ;Ge<'
    b'1U1JxSbT~h=J-*fw@*OS;?lw514Xg4_I4HZcF`duz4;8=L}9MBXwB@tU1`_{rThRY_XPQYuO^ZoVIL)W50<3cMU&Jt<3n&$)w$ZDMZ-^uOUKInK{NdEu=qn_'
    b'|1To3ubvj$s||RG9WVMV>CVH~9aMbe8>{!v#*3X>eF{|*tU<TWti*DXvFa0Fv7}_I_{dkwt_&3)`D&SclHlzFKCzr+top=PEGZQ$KJ(qA_*X@$UEo)Rs?F(F'
    b'MSgq5d^|1w%Y9lLpB*gbE7oiVkSeACHD-O|_7(K&+r@7n)%1!`OGpZQH%fUouaCf+>~67INvY6Hl6|T(rzNr8%dZZ8o9I1O%I~8z7rQtjV~!P$n(q~sjD4Ht'
    b'Jya{IJyzIMf7KO~g8)yl+cqhtS;oq3QUpIK=_gpVGrU<Bx>H)eI`~Pdw^(IM{YAT!w(>v4?g~pyvy4^Sv}jnzs{KJU{3Z5dE$d?~>o06AD?U3~9KK80=qRH@'
    b'@xI`4M;2UQ6*Zzm<s^&PCQc-tU^m%q-#7`8k(=~ZBi<Yb-x8eTz0B(1w`tyErR+XRb2Gx{>-0uW^;TJ_(6=exBDHebLM6R+(FZh<`4HShO)j=&(d@oqh~NhW'
    b'{Q#<VgN-_si|W_LK1uTyt7)};lN3ebLvR!IxYnLkvrh_3$BKPHwEG40Lr;I`>Ay@p{p27qCZ4H$@)ESt^n;L>Sm6NX9ju&Y4eMXU)HC!>>-u5UJJ?Nr_gJm0'
    b'WbE5Cr+SF>`vm(o%@<fHzmL+~%eR-6jNPPpkJZXb#ctM()UNRBLe-A&t3u@__3J{vy>i|_KOPhR1wAHycBuGbab4M~eF0Urh~I&VDVDLjC4IT5WU%-wK`ks9'
    b't3HQNbF72KhZtgxA0>MG07NY=9V|Xg6iaJw_v_p0ulj><4&Whl+bFdJt5CH?ir5Eb`~WKV1Nm96a&qAz_EDnuU|~1?Rf|-1@ju0G3rkG1jFlU-W?09{y+Jel'
    b'@tpW$UF$D?UF+Gg;;Th=O%Lp`nhv>vRTC|Pn>d+xg4LcXsAbi@c`~tosGw$72a8WL#0)=5^zKQBT3Rwzd!i^7)z+$_+b%kSq%@ylo2JRdwyYW5w<rz!?M3|U'
    b'NVx~7PkS|8`~><a$$PLQ)-D>OrV<~5n<&V|wk(=`Qdl}x?FpLQj|ascg8F|ALH*<q@zwJp<q+g0Rycfl2P>yp!)~8ciDe~Y)u+8;S;<)SX|I-F9jiX=)$;o&'
    b'&D#fiVp+*p^=YqIRw`C~+$)@veFjxK!mkRIo7Arh{r1ZFcvAcq_@wxkpa1mxpa1;JpZ~}o|Mm~?{`C+4*YAJ+@lXHxcR&90(;9r|EaWJo9=SrzvVoLO_rF$N'
    b'Ul8Zv`W{2*^{7+h?$Af~@6dc>DbT%_=ssUWJzINyj@DByqSNtN4$F16AAvWy-h-uNb8E?`6Vq@b)i<zj5`BRct69&mYFN#1|IEbAl9s`{RByp*S?l0=Nk!p%'
    b'<9mrWd!&pOZQrP96)ai4(>#A=?6+6d6*$DtZ#%iiojbJ7og#W)Rbs*)fG_GwO7%nRw^!9Iu-qd>^o_z6JBEtg=6N2!85xL@%1u?VL+fo@MDI&XOt=nK+oxps'
    b'23Bs{s$m^0w`~!9qo%~Rtzy5-^S4Z@IEnI^Qu}N&#hKGwDLp=!Fty7GQ|A;X`9x?=nEE+k>YQzi{oE+LnG>B8q3+?jPlUqjVr=l$SfBL`pS)E5>W~`~p>fWG'
    b'#yJh*MAOz^)48Ub&(&L7yj`o$b8(hyyjIG-h}(S;cP-2&TUHIzIj4)StF^vZo7POv7gBBcHP6M~F_&N4xzNfvTboP32QB#oaJ<+G>|CnN6P9hMwoK<*lnt-T'
    b'uVF5<!daMOd%yrErtYatCv5lW>@(BN0*vV#GeBj4e7G|oUIr|@G1s1}m5fc~J7L!9i3tuvY2^5l=hAXc=Q?%f57QaF?D$piu-U?TfXw2vjYn|inIT_V&U0xQ'
    b'YRCd03kcxfR(|UlN-RFRWR{pZ0}O-J>8vy9!3?+QY;*P6irT-;{MKMhZ1r!mg+<aYC)j`c=bwK1kAL{(&p-e6Z-4paPv3`6ZtAL^zxBZw^~j%*7?>$6(Y*;?'
    b'f`1o}UNL}{PlC5r-pIzA!EYvJ6a0dcMPoP6o19(EU9@6+i{9~ao;;lAqc-yN;^#acz17Ksaq_o^Yv*E^Q%`*<H`-8quMLIy-7283RNLXj8N!Iih<$veQQQoE'
    b'GclXsH(J3n^d@IF+K`0)x6_8=CnrH-eyi-RyZ$ctJH!%F{!}COZwP)fF*=io#%`c>9ukZ3-*y{{@3o<Ky8bTsJH)ap>6^iCCPrrx(bx^N&O>4`{+nt;fA`Bz'
    b'KmGErfAhm1{vPe<Pe1<lyhHpP()>Bz(No4e?6|nxHqRxs`7mle#@b?M?oq;}^f0c$(I$Z*_1H0!tIxq|sx_=H1cnqsI-<>*^wQF?n+)&4Vrl7M?R9KghIQ!M'
    b'B=50Wc6IFLV(Peg$%L3)9lJ^M9xP^92fs~q{d{HnR*rS-CeeGam}4EhdHu=pS^Dne_y+cEqA$Q&j&Fd)7rv-Dma)4;Z^3GgW$@;OFX_{T&3-G#I(C!jJy^`K'
    b'4t|?z-)Y|vY_xXV>c=;*n?&!yVvZlAdhXesBJ0+mrbFK*d5_h~YKv{7y8MKM#OIdc*<nS&qd~XIK}@lX)s%x~^$B!4jA{vf0NoB{Vv1#~IFe~*b*wm?sAeBv'
    b'x74a7`2loGZ(@pNtVVB|)jjkJ3%3|*gH;(yg6>&HOR<a<8A`G$Lsgd1tjbuGp)|8HR%Iy3td3O~N;IotRhH4r%2<`5G_x{RWGKn%9$M~^Qn|%L<rejnJB(3o'
    b'_4IP9gO*$Us@&=h<yI>$w;Er$(`L%Ufh^3eA8W1lE3H5eu9;FtpbhrD1|^Sm<zB+duaXvZ1l$>Vr(@g<{$!BcnR=%a-VFX^9Nn0DufyLA{$!}#nz|;Jo57!q'
    b'#yeB*5ZTS(PX_Frsdq^8W^jE>zl!|<%gWHz@>9*=*RS!j8d@^+9to<U6+`dPry5u?^B#Gsp(R7_aiJPoG4w9Asi8GP?=Y1bS~Bz=@u;CCL+|zUhoQf{Z*P$`'
    b'`7`!;*~YyEh%H!D{vvkU@ipwWGmH6sf_;?cEitHx*1_UDM>VX2#VM0$_y$;<eaVJpusD%Z4eMZWPN*8z!P@jvv@2uf>7xpkyRj?{MX;V_QIUz*CmEIrQxsjQ'
    b'S()-w5vCfJDNhw;YRi%-PZephVU_Y!(WV-fDNhw~B3AFiqSjh_7hCTkjeEQIwqR9jY1n=Lm$3UjtmXF!_EDPm{a;M94pz06X!r^Ef&ipcKf`YOznW+ntZFUM'
    b'untzWmS|W9i&{&wD`R!7C4%K{tZOX|tY=x(S{n9AhGoK3wU%gBraW0|iH2p$leL!EvSiAWwU%mFr94?{iH2p$leLzH)%&ofwMuiD)&`<X?cUbEEm+iAB6i#V'
    b'HSD$zi}`(meU#>H|5p>OgGH^S8rH$0ToMi60E=2nHY|fht)&{)!J^hu4eMY{Yl(JctgN+Eu-uJhttEo>EQ?x8#6HQeOqin9Qq9Vgr)n+LuuOTX)>2!ROnIu-'
    b'k`1err)n+LuuOTX))KLL9~QM%Zl9jhz4r`p3s$w3hTZpn3A^vZT7I8kAEkNU|HVY>U{!00hM#~h2tZ2pGwinitBIDus@4(>>tI!DiH3EssI@e^GFI1GB3SOm'
    b'y4KRbdX`nKrD30BSSCzWYl&uM%9FL0XjrB^S!;<cOQt+oYpI4+%9FL0XjrB^S!-!ny$_38D?~pI8+wiFYB5=B?ZB$m(y;sfFJbq6Sj+Dd?4vaA`@fiI9jt0C'
    b'(Xb9y<&tLj23XZvs$m(dYAw;Q4pz06Xjlh}T1&GlV|A@1g5_?kYb_0|XIa%+8um$sWx`aomS|R{JXvdrhGoi=wU*ejWXhAZmTFj~JXvdrhGoi=wU&m}`>>|9'
    b'a-TA-ht$^Pi>lVzf<>(*Vz>QY!*2VqnBOPZM`_;ne>KrMSkzjo;V0ld0cfdyhTZjlIngp$)LN=x9V}`s)vylMw3cXB#>!et1<T!7)><N1&$6hsMC_9c%Y-Rv'
    b'E!C_{d8*b@4a=0LYAv;8$&{yRE!nV2d8*b@4a=0LYAq3~_hC_MmH63><@dDK4y<Y|4ZH9E5_aE*wfsK8K1%bx|BH#%!K&604eMZ4E@_5ufK{!f8kWJT))Ect'
    b'U{!00hIO#0wKTgjR@Yi0SnkHU*3!UwmQ}5#VV`7JCQMapiDqTWleLy;Sf)H#Yl$sOraW0|sfJa`leLy;Sf)H#YiU@$4~tqW`nLM{8jgGWwYFeYYiZbh|Cg})'
    b'KCI>U3HDK%_x)c?v<_CamT341_<{hWR6oOR`@foK8LVn8(Xb9ywU%gD2a8%uvnykDttEoxZmer94XkHb)mj?%Nrq*@RJE39R;D~zYl((s%9FL0*s^5GleLy='
    b'SfxB!Yl((s%9FL0hSmG9rnS=WZT0irRPC15+JZ%`C1SVzU&C(uu$bQ`*hgvJ_J1|eI#|?Ns$m^0$|ce84X~)SWWzF8)LN=x9V}`s)vylMw3cXB#>!et1<T!7'
    b')><N1&$6hsMC_9c%Y-RvE!C_{d8*b@4a=0LYAv;8$&{yRE!nV2d8*b@4a=0LYAq3~_hC_MRhMa=mYa7zY{9D5(y;sfFJbq6Sj+Dd?4vaA`@fiI9jt0C(eM-S'
    b'1p!E@eumxle>KrESk+phVI8b$Ezz(J7PXdUSH|jEO9ac^Sl3z_SkJPmwKVLL49kS6YAw;MOnI`_5)I3gCu=RSWyzE$Yc18VN_n!@5)I3gCu=PYtM_3|YsGuJ'
    b';p46S@A1}-_jqTId%U%)J>J{L9&hbjkN5Vf$6LG8<Guap@zy5tcyGUYytT_b-rH9mZ|x+H_x6s*Tf4>Mz5U_w&W`YSYY%w5x9dCJ+vgqc?d*=X_HxHtySL-5'
    b'{o3)?4()hnPj<Yw3p?K0cOCETw2rs-R>yn0spGBv)A8Pp>3D08biB7KI^Nm`9dGS?j(7GtN3Y{PVhiEsR_7g79aSahzT+s+eZP>9`&KVO_ib8%UbI*Zx^0gV'
    b'bl=(}=)UPG&<E{Mh3cb?hLszltj;96aw}FPq-Is_0kT}w?8@CoR+5rkz3<5)Q?#pgTv>l=cI93#OH<9ROc}CjmF&u-q3S#dDtCKP(@99V_o;eJf$Dug)lw2v'
    b'Zi%XFQlR^`ba+w*N^czZwlMFos)mxF`*x_MSjLL_OR_3MRq3W#m9eVq)6B|PRWeFub*w5kMYAeam8zOq8LP@%&8&<SC9-673k|Irx7E->i}BtxZwnSVO2lr7'
    b'MoqL1)@Vw!`v|*b8!^pKuv@xO6Rm?qvJws70E=`b8-4=bvW}SQC)h3RsEO9W8fl4k_t@$u_(Lrv<#BJn@)oSJmWJIEkC<p3EV7nnSI4TvBihx$Dr<>`b+F1>'
    b'n&BH@m9<pEGFT-Z(Xb9ySxYpmgGJWT?0$&__&3K(cwy^4UgAr#zv(60-~7Uag_ru$>~EXl%1gDs^(EkMLAY*z`wLTpZxLm1S1@RK8Tis1_>JI!z#*C=#Fs$3'
    b'MCF%Irn7h)_&wo!cV&;IGhPeWEga)vC`44J6Q(WAKp@PR&M~7$fQBEYvwQsfs=ma-oe{-B`}j4+7vmi|(~JxOP-<~HqesTC0L#;vUm~p$j(FR2Hjj(}3VxW*'
    b'>XGp)!1{E;Ag$rogjxyH8D?Y%Fz|yr5x^tMG~r>hg|)~ABTLbp2^GyWFj9mm(^)1A0TO<g&g>@8^b+Fj(}~EKG6qCsZ8{NvX&`3Iu-U?v8KAzxhMP!eb=eHy'
    b'&r1&O3NJ>ua7Am25p6G9vEh%0?=LyOWN!p{HkNGRv%9=iHntTD))>qpVMBqlx--|8+@=#@`gHc$m<pRs9`4Lz!YTul!=2@r&1SHHl;F-19ENHr@uj5cOtbb5'
    b'!b+UZIGYWBonaHhT4b!c@KUln3nD4gSzbz=&g#{RfT+mQ+*z8#P%{N##&oXAiG-Eq?6V>ZtIWd|hPB98CFr_`J1d-FI`J<~XY^`gMW&aU+*#9vMFyyOI`gck'
    b'#A>O<owZC@W`J6!bJh^+ufEjjtZl-w)!Piq+O%&QVYN?Z_lo7O<E0LF)-faN4A2gDw!<qnTNSq8&K4YoN<)Aar!#sLA|NWOC3m*uFw`mnv^<@&-dL;orA=om'
    b'6BeyDXIR#;eOm}?bvmn8H-Bv}t+}(c85xp}e`7j_S0O4Gu-2!udvzCU1Rl0AtVLF>V*BCF4riE7{EO2Wy}D7AaP~Bv$txC>24`Q+S%s(wID47S;?;s8hqKq|'
    b'tX=^qTsV81&gMmpVuZ8z>Fi#pC>l8Xn9kt^g*=YqWrXPro=p@20*u3*2w+8m?2h;{(sZVod26&I&u=rr&}q$c6nBo|0R|##FQZQ<4B8lI%@c#IyWw!)7z`4Q'
    b';BGkZvB(=+V=&QW$TZRTc?Qd;kHerP!<uC{s=MKsG2rJJterkaYUO9`GaSR+aLgF+vj+>u^4UOc1!)a6*hot>8PsA39EmMhI(_`zs;97R1{-n>y<!L)i!E3^'
    b'ebfq8>4Q}kY&?ZKaCEjIw^=(q-GPI-MU4s!pwM8$wRwWqsDH~ZUVZ5`9O^aLplcY5#DdYqpUUYgGYYl@y0g1Im}SUZ$U<zVugxfiSAVe4+2D0X;V$Z+ar(xJ'
    b'gAg_X8@@e)J|i&~2JB$Nwfn+~#TriK@5`5t6^mi0w$kZKD;8@z6kBomETqL^F61ed(^pn3#F&E1%V!~7lF`MO+UaX67Gl^SQe8d^X|aS^?>0!8FVScDvruFG'
    b'X1=~GSOXg?q{Tj_g>HNnTsZ_f@CnPqPh6hpTnBceJD6fHPjb3rH>Vbzy&n#IOot>36l^FmPjxD^p3WHB^k77Ce9smt*x+QI?mX!o9XW92Vdybq=*7YX8>Q$e'
    b'htsHcbp8^SuY?r^5sborGkjQaREs0nP-dR!4D2MpU}^a<WO)?eV}=VhWSJ*BK|2Xh$(Q9TWk%7vg$p)}nWs8`I|(qBwtS_{C<c?puw!|K(|aElL9ijsJlz?-'
    b'8<&SV-EhpRxB5b2OuW#85pB4|<|I_(^3^y~Lq3AZV9JD^nkGRFqZ53Qrw4<cTeYvrHnl7t#{m!6%x<u;(LB`$5T_>wYs<&6z@p%=QJKEJJZl_reqy+>d>jls'
    b'4vriQ*^cFF#~MqFq7br$<>PqZv2gHU$QDmuT*C=5B%GF(k3)jT!tsM4TRwexjVQ#Ba9UYDjtU+NhY*Hr_4L&>s2E8xWLrM+zsF)zxz}n-UTt$4Se$TLU%u8?'
    b'ETk7!V;jrYUP+}nsrYXe!&tH8$sMK>%*XcC!|CHEp1wGV#h8RXV-WYH$t~6(Ng~D-<|7k04UkV5()+jh>SP!v9?oOi^06DvSdf19uYUG@_K(Q~)noDAYQ8=x'
    b'$eC%JxaK&wU=)E|Sr;=OJEQeP_wl!Q`r;%M=NV3%)AF&a%vhp_G%e-6JUPXwhSRUId>lS!EZIYjdiv_56=xfy+&i|#(9T%68o<vuePc3<Q3+%5zG%Ka$;Ilt'
    b'a+-HcUp!u00c#ACaqo@UT$5rf9cYp9h|?EI<uhf&tVfq@#axqRjIlr_(R->{&da)y46T&ugX;_#%zAW1XTCa_#tDciXwwJR8B4X0(Ile#`Xn3YAf|3iA6#cF'
    b'-9kq1;niG=ZK`n#z6sL@*NUYb7BadXG+$h7(~Mj2O`1NqRxIEahKzH?#$1bSjD?UZU*oYD${9<xkkOgJe08ynu@Dz@+Vn+R-tkzfg`D-*s@I>hjj<4O+@~*c'
    b'g~($8x3D&So!opBCeA3$*=GJ`F^m;UcSeb>MLXA+=nJQhpLqJ>VjFM^eQ_>SnQO64cSeaWI@waWNaXq!+`^F2g{ArGVw>)a5?zp54DF1iTFB_a(tLd}N_W<X'
    b'E=VngamLauWOQNK&9yj$Oan%VY55|TuVyTL^2>4hj>%FMUmO$Xv4>@0m<ykH`r=|KV=v^`g{)al%le2GGP)o&UtTOVoQa|fS&N~Zv1AJwUDlefE|wb3MA5~n'
    b'#n8@Jm}-8;=^Klsz)6fH`sif7zF4X|6UBTiUw&;ptZ6PNhULp)vD9!Tiat8gm*bhTVb-IMPQzT2rOXzY$keM_&eOUx6s?ryBNxt)!L8fK<-R&u%Grx4Xv>$|'
    b'8B6t$HafYlPnL4_V(P~7<#EQ+J!CnSuN;%53_~XJwKe)mSh0|k7}6K!%oit18HP;c%X1b(TCtFm7}6K%%$FxiIeQ^jzG`PNlrxs>A$=Loe08#vvlnt@BGhAO'
    b'XDro2=D2)$jWW(&%yD17(pN0xB-Umb%U2c?IeU%uo5e6zEO9cCiCgn=Ose7Z@e@y9oGfLWM4ydn?n{%UtZkBsOca}sV_Eez^W-6I<Z@q~EamKlT-COG9Ft}&'
    b'NHs^HdNM;@Ok{k;SZY6geKMFc+c<H}ac;r*gNyFR@^QQ}z3V>y7EfQCY~w7%1>LlK9Ft}&(L=U;`toEOXCah^DO``CoUvpNX(N~W>SP;dA*8&u<>Qz%V?j<i'
    b'(%1;(zA@RxxP`Hp!gXJtY-4p!M(M}$_19Lw8sk%nuzWpCwy|`uMfSLS9Fu0shFkAx`FfgcW46dBrefW4Ue@zu6jR0?s+=K%TkrMs)x|b>GK#5KkD;BhR1aw*'
    b'm;3r+n>-oCM;VJ@oUwEdIgaHU$6}j28D)g!<GACokXsmX#M2iS+my*Drf@xmv|=H*Fr<w@?#qj9%48H%xE@0}W62)UMj-dq#WrO!%4o~SabU($J*3xPsa}81'
    b'Hf1u(=*!3P%3~q7ur|k7zHu^2nT#?{AAj>$sxwM5g-ah?_=MBPPdt5bu?@I|zT~5m`O;#W>Wq?18Pf+BK9)al3qvL!fy`GI+f-+iWD3_~XlE?dLM9)9%-0vA'
    b'RA-HJjOl~xjHO%1<Refu*WwT|P2=;u<%8>trB8l2PTw(E%Hli5#ChytS!m|MC!W5zSjyN7IW}eNmeaBhPGZR9BbWK|VyWg#luQ|W4CRa^Tgc=im-*^qspd?S'
    b'Oc{F&?Tm$~=4YI~u~@2AizWH9RrB@5Qq`F##bf&5I$IBG8lM=JFNVcZ&6z0q=)_dTc&2Qa_2i>dGuL9N?o5>YDV<r)%X)VvO8&IhLX|UQFzd-jF7wsJQr(#-'
    b'`SU=Fp`Ec*3z>X$GGAXT)t!lwk7^dfIAiG+GWlcSZmz{r-I*x4PG$^zSm?2UlNd71N5tk@EH#{ok||t|A+1<Ow2)~&E;iR<so_kNOyPPA<%}g;$mAoJ`RZb+'
    b';Y^fFjd~32jHO!0S%1S^i=~D$QSy<?V(2TDo~$;Lk9gf&i;0Fa(frL~7&8{<9X=*MmM_y6P9Hz<^u@_i#!2+$bo$a{DQlZ#B2&iZ%k=qU_~apN<Z@q~EamKl'
    b'T$#f47}^;NQl0rZnISJGGQMIgxu3p18O)h&oVeyVw_yCi$H~X?6@J3$<8Sfw#mP3#LP)tOT#q50u|yB)Po>S5C)+p+p)^e4dJN@^C3{F4x!hML+c*m$<@2F8'
    b'G3|_nn-BOIr*BNQF>YZj{s7#3eX@<!IT@uM%U54p0c#AO8kVny$u^b_GD?lh$1!Q9Y`FEBmanGCHfD>AVk*`x=Vd)kMlogVp~@LDxOE%3+*c>tI14caZTUDR'
    b'%~-03to`)$$u`bHOx;*Mj!83??jhT;eC?QQV;C}ujcVrOxZ|;qTNu(tAos<|Hiog?BWd|Kws<VIyM&*7`toEOXCdUOmF45uGGoae(ncWn)yX!_LdaEX%g1qG'
    b'#!@|`*I%k$f6;xDQEUYA82XBZ+``&yWBJ-*6lbBaezO?HiX~4*F@<YBjx9D;xsRWC`r=|6atnPnI=L?`w#k!GOc|SxW0L7z;}(YO_4L)nHhD6NDO``Cov~C8'
    b'+5741i&64q4O6%t!#HE<9&#MZH%<;AhKw>!AIFv%OP~C5;uz9dit+Waa29)57D{jnHgdTyE|xO(;?ASAd>oTJ7IG3p+Q{X;yjZGCCNgF0F_bfw>>+LBa$j96'
    b'RVEXSwtO6uW-LrKKjZX`#Zu%X#$w9YeSNW1b|%WlF@5=XZ9S~%f^Wj~<s&SXD$YdNM<@6)$E2CEVb-&cPQ_e{rK&SgHudY4^Rix@iLxnb4^_^P!K`N=xy)A='
    b'OI2s0Y|7YUXlE?dLS`SG%-0u7RcE5?qngDq&RDvI%;8wRa4eRp&P3UDGGpMDFps4j7Bc(DWxlvrsyP#7Q@9>OTCsqW7&80FWxl*vsyP#7Q@9>OIb+EdGW*D7'
    b'zPebdITK}5qaH&$W2qK$)?ce$f6h|PnJD|nWij*>OHEdr*+;x;uEj*nnP~oIF^m;UcP7fFaOr~!pK$v4iKj0vmg>=b*+(_=rNvU+nJAkwww4;{v;6gBA+wKM'
    b'=BtaPx-(HWh3hf2GZv&e@-t4~$wc5Q#*%$hGhbf})}5smt{HAxF#bTUd{i6U%*IbRef%w+zPQ-NSO_Wiy_FV2I%A0zGW*D7zP#9GIHP3WC228~GnQ;2vyWWn'
    b'tBY-hGfMVddlo}GV?jwIe#Yq=i*3Lyj3v9mHD6zB)16VWE1hnxvlXz$@NxCq&9&HOIHP1Ao#^9E%$c%b*0YaJ!(5YX%oZ8N_X3*bJgqy^&`Mc8a@q_T+`4c3'
    b'Ghdx-<1EA!wB_Uez!^*RkiHwxe0{Qwvk+4^mXF&#XDr=A`p&?^T$61KW1CFF@^R~@$3kvl$P!OqoNQwlGKwi&k0GsC$Sn+MBar*@WE*E8<jNGT$575#vWK)0'
    b'$bEIPjk6GU!M5e&I51<W9@6)3hU)cqxNkCwjX)klU$Kx|YzyaDzOop_S!k@^EQYaSiIY+0&d@*?KH>E76Hi~9Y-8L)pYIYiUz%)VZIg^Lx0rIXD1DYcatlNH'
    b'mQwT8$u`bH+(Fuwk7LV>rFux;NNT=58O2$M8-mC3acr5fbPws9N~5_ZhZu&8(oP@8mKjT*{Bq(LGWv$q?iL(pv4>?L1-D=$m;2&mDQ7R_*p#tbPAe925<|9p'
    b'`toEcXD^guE6c|*X~vR0q>WtetCOXiy-*saj6H^S#==zdGfv-_EM=U;SWFqauTPe;wn8TA$MW^p*29{{r-$Y1VX~B^gDtto<>Qz%Q#RasPs`WSWGS;nCNlNw'
    b'mh-ZnClmFueB{CzGPw0#PhVXul_wLKGWHnS8B6t$HafYlFP6%aiELE!7{(b(_mJaQzHuy;%9Dvq;hK+QlE*?$Vn`dg+!q&1mB~b=a6N{!Vj(9nq>Wte%ZsJT'
    b'WFk|z9z!`}$sW>1F89^NQe`sHXv@d(W5!ZFq}N}mUVqL~WipYCTpmMTv5=Ekn`12BIGLzSCK{)Yzj-XxnW&h;r4KHA!s+8Dp1!zP3Y<irpPF)CS}awaiHa#>'
    b'`ryLH@&`_0$l@cH`RZb+>P%Ej;d%`1jD@EU_!+0~WTILvmg1wD`TAn8>MXTz&2ZC#@dt9{qZ+rt2Y$lo<8Sfw#l<$pLOiOFrVp+&mS`c1k6h-<i*1@SN(p89'
    b';5uW;7P9!rWxl%Dra7aO(54TrGZvIY;Afn^vDk*&=XqKq^wZZD+f-+i5|8OC@wFAO#_)+@`C?dX)0|O?k4{WgjAzP*SuZ|1HFGVt>CPy{RIFRh%X)W4DW;4)'
    b'R5?QivtE4UGGAS6)16UDY|~eGmSo0KEoAYL%Y1#YO?O5qKFU}O<BX+S$l~KsH`ijD?u=4=RAUT0apJLnTNtwV2xPvv*k(AR6jQh!Lt3$nXd#P_K<3MfZH6;S'
    b'F@@_flrxrWA&ZYd=BtZshBHbrHR>_6GnQ&0XZ;OxEw&lXD8)x0i=nSrz%9j2=#1q{C!-8!l=+**FlH>yA1Dn|xaQ0Bh117RJbiJpjd2ToHafX4O}4SNNk%bc'
    b'Y`#pNoe3egFr<w@?yHk+oP~Hms4ZV^XDro2=6?G6WE5v1<S38j<58IzOZSlFSiZ72#4u!(a{72|X2#MdznnORG?udO8OuCrLtmUs<P3#e`Dq!8JuM659XnQ&'
    b'PhXx)<P3$9@)J20Lpfu~9@5X+n6FMIa)v^VP5pWd?Tm%F<!79}F`3AChq3tS8}s$aMAjb2HuYG(`r1NRn>^(emam4%M3xS+O^wUPac8D%xb>QrucpaFW{Yf7'
    b'^YU?QaqDrijj3i2RnCyXt=s72zB-x68Hy=r%g3>0#!@|`jX>_}lZl+6n7Xli9Gzw?-9xrx`Pwm=$S`)kEi50$9gl^)!;pSR%Y1P%kzvR-e&)(zNGlfd4nz8Z'
    b'E%W8cM9xq=S67yg<IapFdq_W~WxhI@$QcT`^21sdLpx)s9@6VCRj<G3zR5OzaLZ!oD;Dw&YtxT!MRQHIafTY}H;ZAcSn^~WQ?cgbxMSm(`}m2cFD@n`@6cx>'
    b'm;2IUB616TrheU*7u%3O=re`uzOopF96?{Nr>`#7U|*-t6t4T)>iz7`^x4SezP@@m`z(E?aNRdnFSgT<h{;r}`@-s}b_SBi<&NcJNbjk6_QnyHk7JUTV4pry'
    b'xb8##hnK`;Vec!}gX`+W9Gxs=Iek25=^-Zzdtb2_`ih04lZ9-jkH`2t<YZy*EA+7kcq|-&EaW(S<E0)Ra<Z`Z6^kLxSSp#wLWb#s3m>nC;7sd%#bU@a7KE4~'
    b')9K?8P!Bnob{=U=-UFH+waYVPIei5m4>_6E`-+`=jWZU6m?7KgYxsBz8CKKPN0P$aELKE_8FHMyv06xVR;)fA*>Tsi6;x-%>Z6*43M(Yq14GW=%okP*sm_Yk'
    b'M=pyYo*~nWC7!;xT1a(PtRYPwTxZA?OFDgNwUFwpSbfB^81fl%#gb27UM-|KD^^p~9z!`pu2{<HE3<_-lQLwTKDcH`YY$=l=Ds>xh%+fu(54TrGvtb;oxV0('
    b'h%+f_%|}s-p`RgFEdBKL*+PmPNM_2%@`aNzn=|J8&0-&CEX%?;ePgw(?rd7)F@1316HXsL@$|*Tw8k1J&$u`Qt}~WsA*(5W_vOXH#u_M>xHtr^GnQl_tB=g)'
    b'tBawHHIRq6I0UX4i(|_C&3)~R#p1)KpT54Bo$-+!;^G&$mIWU6Mab%-Hht-stnZA1T&0s=QdqHo{~5CSsBOMDM+9dSq#&LAlG2QYV*^80AGOVw=V;-K!kA8e'
    b'NoB>7RxIW8l{1!Zu~Z+?%~$6r<7~rkPVPx<#==pgCjK@~-^ni+Zx~DUS%LZb9Dx|0aaKBcDUD?z&X#5B(0n{$Z}SKD@e@y9oUP7VBM)h(<>P7l84C~F^K-TW'
    b'p01y5B6=(~D{x<)Ez(<RIdREx)52_7rUcB#^Y*!&KK|BEU!N_@TO4w0vjUG{oUwEdS&ro^$81@KVe2Vj`AS%^ur>=nXHA!M*8AbHlz95$Y;_hN+r-2L$GL?x'
    b'TaPIZ^A&!|>Emzp^wrsVyjAhyg0_66ov|=S{EX8#Rx4mzVJxOf+}CI8@fJ5uTyvaT$g_o*x;G!kGSeaM<0qcJxLQx1EyPDkiy^I8>WU?uzI4VCJ(hVJfVo!d'
    b'$+LyntiWS0XDo5XQchnvW62(i-z8wavn^SRgRh=Gj*rtqp6%?!SsQc<d0J?vubmc}Tku;7%-2_IwHQ#kHq&s+<BX-wSjOoaXDr=gab=awwOVqXt+j>a<Cr^R'
    b'=^l&!W-){n3)?MYan)tMxLR_Vt<`2I9(!7`7$&UW%$LqsqQ~Nj%zS6Nw$=|{JAE9hr-eA%{E4&v;1=SvP)=VtEflxlO3r+B^&E=<<>_}*nB{iHl4mUK^tCe<'
    b'mJ&bX^qswfeTWwP_6PIz)vL<vITP0$H!aj@VVu5UvHUmQPxDv*>0f^Q`EUN`pMU=^|NP_6fBMHC{^@^w|NY<n^3zYh{OjNR@Q1(u<<CF=>Bryx_3wW8;~#(j'
    b'$M54`{rlhihF3QAR6e_IYj@iduZRBZrl{=KJ#DdHUiWkfj>&Iw>#@hy>T|G~Y6%+;zjrOBP<?m5Tv$5vZFcuqt*CVD+a&wlXDQ?sqA&95+10U|H1EM;hIR1U'
    b'RQsiCB`4_CRBvTihHjF)#fsULv2T++uXoR__S8bTm0caXN%I~oW>^QmNp<q*ax1wFzXL_i@eS<TL|=fl9Nz%HO|@UjnV^A3z1M|x=qAZqte9OH`!>nVI|E9o'
    b'^`qUZUmd$i^Byc_SO>pJwN0<&JiZ(HZNkprT0U;3WxgWd7!e}y9&_EmZj!kNi$$^pw_z9aj$`BlpIfSBhZRMO1l<Y%Ex|HW9R5YCPq4euP)qT*Bew&Rm|htx'
    b'jz^kV9jlEBqSXh`Ek$Yx{&wghG%bzqg%%l1G_=QlVdEADZLlf_DbPKUNC}pqDhFv+WvoafnpG95a*$?K#;P17nbol(2WeJSsLCUnRT+EDL6V{OLaQ948QNpZ'
    b'J=!U^n5NtzmvV~~%ALMkZuP-(tLv0IExz1pspTsTtlVlP<>}z`=H+tl*Sj8EGNleHJLr2&NFBh+t#p-NDJklxwlj6z74C(8Fz)RPz0>J#27fX%ZcM$`!EXkC'
    b'GJ5VzU6aYZ&=1DfouPMV>t^sLL-5Ab=M?$X0Pl^<moYq`O&$BiD;U4RxN2y{(0jZl2A0gcLx^%{$<RA=C<d0yyhm?pXvNUGY^8>l4821>VqnS4dt{=9Rt$a7'
    b'v+w`@?VWcItts03cF=KJ=CQy#ihK(e^|^-K_H7Zm?XF^epMf7Fde`?=vocnkjHq^XusE*~4c`E3QzX@{j1?zas$Cs?Id2n9y&GJd^r@y~uso>~!E!%+N5iSX'
    b'^-PL7O2a<MqRxS;R#FYCL?&t{)vU~8s+JNB>pZ4vE7h<{WTMtm&B{EcYA+4@Zl6{45^P#_TJM2ZoZQk&JFu#kB<#MwYtVg{)$;oc{2<ZW{w|u8v8rAY?LGlt'
    b'^mi%MkFeYRE~Z(=s(MMZtAnrgl4k1N;Hq8{P03(gFKJ-8pT4J;#Nc`+RlOu(pJY+zKv^$|hE*a{^^#~-<}q0>X@+$kll78lSS2!5FNtPl9+UNwgnhTqih8Lu'
    b'*IFp-)Ok(d9lf*#i+V}JZu`3k-F8_qzt6xA620s1s#zH;>Lt~#4i+VkX!r(L(@Uyd87t}~)vgY{)JvkNcY}+1Ni`*dWxXVV<$n5(UQ&bWnH2SshJBJnodZ?9'
    b'q#9O<Ow>!NS((RFy(Ajec}&$ys$rGLM7^Y%m3d6nOB(jwKC9}b+_IPWkw&?>F?S1A^^%0$_je7t@3LBcpMf7FdfVScvocoIOQPK;;EVn)rTP(e+uy}B%UD$}'
    b'iFS4HwO-Opy&GKBOQI<mtm`EWEces*^pY4{&!noCB<zzc>KrKRCDE`-WU5{g&B{C`>m|*w&SSD(5)G?Frs^fptjuGwUXrly_E}Xgp^QC0y+&S}a!W7mz^Y!7'
    b'u>1b5LHAu&%kMMrgG6upyJ%L%s(MMZtAka^qZz&d7WI;7SH`M(Nwlkjul15<>fPX~UJ^~oU|lb1V7Z^Zr<cUwdL~u9Bw?RqQRhHeFNua#B2)E}XjbMiSubgZ'
    b'bsm%Tl4w{ZGF2~$W@R3e^^$~rx6g`tDfg+hdO%XjJ-xIAi+V}JZu`3k-F8_qzt6xA620s1s#zH;>Lu0g6Y##jYpH&O-Su}h%`#ThOR8NRe5sd2Q||^B^^$5z'
    b'2FrR$1k3&O9lfLm*E1>VB@O!|i#i9YdPy~`5}Bx%RI@UVsd`B?tn-+vmsG<lk%@XqH7oO&s+TnEyM0#GOJ!=UGU~xsSKZP}JFu#kB<#MwYtVg{)$;oc{2<ZW'
    b'{w|u8v8rAY?do7v@@R%{fJMC|+Lf`YUJ~u<;A_34nR++4s+UAlGFaD38d&b9@98BmxSmN>FG<)ZS=2dD)=Q#cmB>`RB$}0ZOx8=9VV%chy(Ah|iA>c?qFI^8'
    b'WW6L|-|e%iUW&d~JRZG<dh<SkEm+k{5_aF;HR!&}YWaNzevs&Ge;3WlSXD2HcAtPR`n#0sN7!wD7t<_bRlOwI)xp<#Ni+3sa8)mfrev_Lmo%{4Pv6r^VsJf^'
    b's$P<?PqL_Upsbff!zz)fdPy`Z^O&rcG{ZWN$$CjNtP+{3mqfENkI8yT!oJ&QMZJ`U?-lPcgw9v--O)>1u&9?b?6$v)&~29$^ZN|^Akn-2u9}sxqFz$%>R?gw'
    b'h=y-~HNB+Tm9e5;Qtj&COT8qTdN;VJmsC?SSk_A-Snj9q=p{9{o=H(JY1k)O)HzVqOR8a&$V9!Qnw5D>)k~sboySzYq#9O<Ow>!NS((RFy`*8^?X#+0s;;$A'
    b'$FY=~_X%vls$P<?`~I#$_gz-Y?=$d&L~r}MXjaCmdP%hV1bororBpw{Zu`5KW*MvMCDE=9zSc{csds~`dPy`TgLS>6f#rVso?a4z>zP#bl7xMdMV$j>y(Ah|'
    b'iA>c?qFI^8WWA&r)_F|UOQK<w$W*-~nw5D>)=Luh-99VorFd_Lcf7TyJKovF9dGU1j`wzI$6I@|<DK2u@z(z9cx%UXytl_X-r5))@9n{kcXm$4TYIJBt=-Y_'
    b'-hSx#l^xLWYkQvKtzFLX-oEB|ZzprSwRbswZMSl~w?8@F+L0XZ>_LwAb{)rC`;6nQoyGCaUgCIf_i((mUpU^|Aslb*368gR0mnQ0e&fBJzVX)H-uRW>yz$ol'
    b'-8jD;v4wDR`|b{_j*JR)-%%vwz8gr;Z7Y|M`!=jVFIuPs-8Mi8xo=(y^lWQV;0Fy)#_A)8gq53~s;D%pa<i3npJrEW^Qy?xtjhgG)_;;+y|c;EP_wJ{R8=)<'
    b'R^?tU3rflEdld1G*3{ybSwWR*3RLdcsw$J9YX4Ftl>*gUxu}OEq}<r9rH>SN-*^tQehegF9QU^6?y#y3QlR^WCnZ>hsuD`GDq}_YrCC*>s&dn;%2-wPNoIAd'
    b's2DY?DpVDlnpGKlEmS2#?}b)nt!8M84XxU@HMG!Tyf+!!f<+e6uv;z>)2w4fB2w)>0`CY#O!NcjmQd6r>tK<NM8h}08X>86pJ2DVBBuEPcF~NO%y)x}w4|Ea'
    b'gR37854Dt($GttcTd>MY5_ZomTAFpN%1feM9V~K-XjjInyd>Jy!749lhHrpHUJ~ufSe05tyE^!qmo!uF23L7WH1#DI=-(VK;U&Uxyu_Def7460zxjpv4lnhk'
    b'+21z9m6vLNkskal2-odze;N3TZxLm1S1@RKf%U^2_>JI!z#*C=#Fs$3MCBK2({vV(1HUJH@2>2zbjE7|yM<#s426j5bi%Zy83=?K(>Z4J2+;7ubas!QU)7g*'
    b'xHF<SXdl1E_!84}rWqLmpw!}YMvshN0hXsTzgRyZ9Pzg4Y#tc{6#Ouq)g$9qfc5EwL0ZGF3AGZYGt9^kVBiOLB7jGhX~M&13u}=LMwX&G6Dpc%V5A6Brn5{K'
    b'0wnw}o!L#G@g>CDrxTGeWekYO+H@iS(?HCaVY7uTGeCWX4L6a{>arQYpBL*3aD|r~-4(4ZMzp<b#fCo~zQ5%BlD!e+*;ulL&+hV8+1OSrSYt4YgbfAG>dstW'
    b'a+^+s>C@R~V=8PmdAKu=39AfH4tJJgHk-i)Qi3~6a2Tqg#Fvt$GtJsN2rF?q<7_tkb%sq0Ymu?)!b{2SEQq8`XL%`gI;&SN0-_>Ib7yG|L(LR~8PmBcClXec'
    b'v(JhwtTGQ<7}g?Vm7wb$?yPWz>BPS{ozbg}6`5XYa%W8w78#)C>CCgD604;ach)jtnE`5@&RIjOzxq<Av$hG#R&O&bYtz1Mgw;Ns-7A*Aj+Z*zS;vg5GeA4s'
    b'*$%JRY*pBTJ6muVDh&ZzoX+S~h=8c9mfYEr!%(XT(DHQ7dSk8Tmo}ZPOjxwqoMBnV_H7}o)#<EW-Tbw^wC2v%W@Jb@{*CDzUWKS&z*?Wq?$uqa5qQ|fuohXh'
    b'itUFxJDg!U@h?ti^y)@c!r9YwCa+jj8k~JOXBDC%;Ou2Oi&qPZ9L`>+vw8)faN+E2I-3_YiV@D<r?Y#ZqG;gkV>*Wy6!JKZml38jcs5Z82rv$JB7hYMvOD6-'
    b'NYj~S=B?3=JipBdL#H**QQSF-2N;N~y^KDcFlb|-HP3Jy?uNsGV=zcKg1h0s$0BcRjp0b{hGU}f^9+_xABRCphBeD@RCmKMW5CZdSUY`;)XLA=XE=tt;g~Vt'
    b'XAc&R<+Fj@3ep;Cu#uK%GN{E6I1*d1bo%(aRZn5t3^wE%dc_bp7F)1-`luDG(g&+7*mw$e;OJ~aZnJiJx&sGuiy9ReK%v2gYx4xJQU8`-y!z5>IMi#fLDw)A'
    b'i3OvJKb6y0W)y4*bZ2*aFw2m+kcHSzUz<@3ul``8v%%|(!d=us<MfRc2O(?(Hhg;oeMVv~4A{YjYxji}i#43e-<K~PD;C30ZKczfRxH+bD7NDASxAe;T*y-@'
    b'r?0G7h%p71m(N1FB%_NlwbR#DEX1%uq`G_-(qaj--ffUFU!u?QXQ9UW&3t`Xum(0(NQ-?;3*GoExN-<|;1iaIpSV2Hxen|`cQD0Zp5%1LZcZ&adp{ibm<~x6'
    b'DA-VBp6XO+J)JSM>A{HP_?|6Pu))bZ-FebGI&$F3!_Z^K(2Io&HcHV`4yRG?==>!tUkNJ;A{d4LX85q;`2X7bnjTA*+`9iV8*gqmGUGe6wsr<2NCvbR3<l#-'
    b'%Nlq*lAlI0wD5m-@EkI#sw=X@tmp;|_&&V*Ub1c+2IJ$B%rBk-9VbE=gg_5WCm_wDNh4%Y#qh_{?nKCfkm#W41SFHsCgrRuT0^@NVGKf{|E3cVE!Cu4RYe!m'
    b'q-{5$)4jJ21t&rpghmhF;LFdV$Kybk9_uxXLGmKPh-jTXRyv^)Oe#UG5q~tgJdv4*P@+1h4tFyCkW?5!kG<m0;%!PcN#Xz-R`h!!HbN*2AaqaCtePaT04gMG'
    b'6tS<FU~z>0N!oRjBp6VKL=I_L50mO)u>>w^w5+E|5)Y_Ff`_!MVM@WmiD1Ox)M%1~1Zt7^AuVf~QnH957;!i?n<P<zS|o%>%UY&XEU3UqNy}=I_<w4_socx5'
    b'MJ}7324*^(+Dxj=w1|6=Wvtz#`r=e7oeIB$hHhGt`VQm?kYs<gb4v0FQwr)>;7LS+2cZ<zw_rnx6M?UQB%Xk7K>Ufc<nJ3&Q4d4MBj>TzB>5StmSMmAzS{il'
    b'%kM)yL7^7@S|K%cLG(<0;wo|M0WM;U3O_MO@?*p=k&=8DrWDkn(9g(;b2LeQDyk*0C2}cBNqq`kjhudElO%kqmc*95OsS|_p|=^9^M?%$b!w5T0rKfn>grkG'
    b'N<<5Pi;$W+7p!@a)4W5aaJ=jSS+Q|4&R=7~k-8YzF?M7)f=WSLxmwoIdtl0zaim@b9&0$0z+WnQPS!h|jP#OK8b`C`iQWS<I!Hx54IPkJP*oa7Q%gb1fE1BZ'
    b'Q)fdTB-VA6#?jQ$&@%8BUT|dIrogw1znm(KBhyk3v<%D#AqDd`6~1NsC8{)zOv~^s(lY238yuOpffpL1;x!&<$Wu!~%RtWnshGEc7m^D)Ri%K-JJeFpQrE8*'
    b't{=S(ypW8zsTAZ25w#58BC8pAwW#38JW8dv(eI$4o0dk85}1oNxyB^YIVJgoDFyR3!?%bO^g<Pm%-b}2l)$7@cB)(?VtzY(i?j?(EFl&1HjN%7Fd>D8I<*wE'
    b'3`{H`HS;KqUL!Ceg@!)0G_(v%EE|r@hlr;c9wkJRf?U2*ElvH)F{MMj6!e9zIBGwwhmNE12~!H@rQp5Bh?&Tu=V-n6fR=#?DWqgxs?!q%CbH0wr<R14foUzI'
    b'VqU7#69p!#&`_rqv06TTO5MEF@JXU2FgihM=A{}vQAmeL>1FrGO3MYs)1-8om+JIHfze5%6sBbzy$438jwAI_=u12ivRC$;w0C+a=_Q*azEE49>>ZJdQc*8O'
    b'?<E#glTw{p3R@yNQEKX?=)J_cZc^$~OJmD?n3NCoQox8O;<YuA@@ZPcCrL|Qn1dA5O93OEh?nP}A(|HPNz#%R=^!QbQuJP9RJ>{j4S8xwY{|=bkcxUKdap4m'
    b'B%#z$r<TH&DVUTj%Fuhsh?_~dnHKR$vYNS@l+6>-dv*H`8oFr->WPrtLXwzN&MC<!Oev_Bf=?0&QH@emFNM7+o(M@XB#C8(*UTeZB63kG>ZRzt#;8g)Nn(;}'
    b'8CFXaD$_F*^F;7hqNTJcHT7WhY<=P?aqI#9LoT`>CP}<PzDr5I3sVZ}ZRmyMf^IZPVv=eJY+2Kkl6o6@p)niCaH%0rEr~4=xhNI&HuOTn@>)%jn50_9NF~xB'
    b'0#WMfZQxr(3o=|vO}!1)Ts%rUOlmK?KvqodQk*8WQ@suBkR92ANfMLPvd-RHG^s`PHt0({3bI)CoUHex9tD{(TjkmEWbds^shGD(>QRuzQbV0u3R@y_QEKLG'
    b'l6n+I8EEKJOJmD^nA8vRHc357KTVRjLoMQ4q-76N3g&IHdK6^1)DTUJ_!eo22t+BFx5?^Jkl|88o>~%HA_7q==54ZilwM7eIG|bzTXOw!;rh|rWc4V$nI!Rw'
    b'TEw@=YW8kYpB^QvN9j|N@2I8FqeNu5B8{W*Ij1C_Fr{GLX80D7BBK+eXx^sKqeNuJB8{W*!T5%6k(QAW2vRX`Q|M75GF)n?Q%gb1$Or_fnMWz~8u92Vjiafh'
    b'p=D$QDmXG9BA%wo{XLV$(bUq^zZ_FK)Js9%(G^GSr}a>AG(KTU!Mqf_*BCJ}WA+@a_u-SIWn|=nl*~(2dZLKTm>TlblF%|TazQHQr7As9L}pA4b!ri-<<qCs'
    b'%}dn+Es^(DAvN<-g`OyeL#1&vcaN;}_=MA>aGIB@^hA--NvsNCTGr8fWOS-HGB4HWi6ZaPq32}1H+rJTyS-?YXUh}4M@BA4#k^FbCyKlu2n}^=DQFoPogg*y'
    b'QjMM{GO9sCpIRDPM&1@~I5IEQ=!qipWYHiu3#n!JBxxD-7BP;@OLcmphzyq+qG{;?Eu-Ep#*ulcPEQn(;Zj4MS`u1DMlMLjyi}(ripWN(p-wFYEp`1mj?7DS'
    b'dZNh41r5!#w20M=jCc)4=7~Bzk$wjaUA55f$Zhh&q$JWgCHaIY1@%(!Ng|~<rKnyCds93SGGj<dB;JOPY>CK4si>Et_Zp)@hD!}~Y8h51`ApA{%oD+1iI&u+'
    b')YOB~v-OFq#IXnX54oLun3UynPD#ECQwr*B=!J&m$Z)A4PA!2gc~=@zQg1^qG-d-CE;Zz-C9x$U7p0=!hF)k`t~b2}Q>PYr_&`2=N?pATe2Zw|4RA<Jy$#k}'
    b'JW4rCDlfZ0R&0FAX;L}W+rSR-C?%LAF-a}!?7c*jN>p!yzQm&-i)GKrdJpPRkQuX8o-I%Ij>tu+sJEdP5(}zH5|dO*Vaw8{)YRM13yF2zB#B9?rLko_Osa=^'
    b'8(_qvAgV!<xI-=CTcjl-5T&5r1{gd&5>1lWLM?c@L_TRsNxcod&=^(CCP{2jEr~4=fhZOAHuOScRJEEUaX_^cw&eQ7!u1Q3)T1B*QA0B=;#*`jYd5KyN1+$$'
    b'_8l~I(~{JqAj5?uu?4Y;l6=CHf_WS9Eg~U0QHthml6n+m#*ic?A>V~>k(RAYshGD(>QRv4QbV0u3R|`|rDh%_sn<Y;OAUQ$X>8dKllt@_f)S6>rzEjOwKVlF'
    b'6DKX{r9@xrhJ*IgddMexK;)tn%uB(0$&*LXB#BAXB0fo4B63km=B2WFB4ozYkf)Z!mWW)Gig~H5o~T!oBqpgAv06TTO5MDa_$1MS%$QO$FO}$t(s8Jij+fmd'
    b'E1kz*PL<MenwQG-M2XR9NJ(OnTGr8fVsy$lGA~u=i4wA3_MEKuLQj;CQL|N^El>2G7`Y%7^HPPLC?PYZhB~zrv`mankeYd^LQj+!)u5qIEe$Qxd6;w_=A{Zf'
    b'QDUAf8sw2MYN-cWCPpqu!Ms$ZCrZe0sUez{;gh6gV&sC9%u7{zqJ#{W8uHYV&@wS{K`Q2@Dm_s`HcAb3YAI-`>sJfck6x<M6D3A2XlSOTM670F#49*5PgLoN'
    b'^gC$irlrvnC1kiFjid27rzD>+rC?sF1xSfe4N^2O)#!;5GGpx2AQHycB3dR!E=a|^RHG+K$Z)BlPA$XgAfG;^>4}EF5-o{Q4N@}?*65`SSAo+W;6KKw7}dHw'
    b'%qE|6O7dNpQZR1=FElLYvz5>gr<Q=0iIEFZGH=uAQ4*h$goZq|B(&r+=9G$gn@*3C_|zUW)Tw36M3hgTQa5iie2ZvF%y1z!^EQnhB{9=!IGVdaR&0Ej{Wct#'
    b'x9RjKiP1?Uc@k4C>*zf(I&~bWw?SXxQTQw%dQRFqJ&p8|O%k7`El>8&$NnG{^)~cEVnH=Yo)1(lg)R9sAf%?=hF(al>n6$Lo~os>C7%pDaHQS_7(8Tpnk0{Y'
    b'Qj7Q&X_>>6f_fWZ#G@d?rG{u)#J5OGL?B8@y$!w47!@*HYRFSdVoO9IN=3a5y^uTwTTPNUpjrxB^7+lPaQzNS>QNAZsG*q_@hy0SvzwI7qtFX=`wkkqX$k64'
    b'^vTduj>hMll6=CHf_fYH7LoXrD5R*~276OHiaug04~vR~@riGdmVBfXQc-V1FC<TpR+A*QsFuQ(e2^4UQ;$L~Bo734lO(pNmd2KRs5Ib6eF!k(QR<W=wy2h-'
    b'{$=8%W#9v=jXe+t?Wgq+PxgSwMJcG4qW2mjMrO>OqiGSJBrR*2Qc^EP?=@zzW|Jf)sg}f+h+LG4dMSFZF&oH?si96SVzqqwl)8E;_$1MS%$QPBFNM7#o~Rur'
    b'wU^x^D?L8#G^w5HrC^8b<Q7bln533<_THjNEvlD7U*d_7{j%p|y(jfVEt@31P+Okty_G2y^HNDY5i(<Hs8dT}OGGD1&Ae1nPlTvO4Si~9Y}pT!`e9xwsV72)'
    b'3rS)UwTMrWmWW)Gf_bT|o(LH(HAK@QK1o_4a#2d=rLuY=WVqCjr<TN)h+LG4d8w?Ps8^FDeyEnhmR!GFxPJ6fSv?UV7d14~B0fo0vv-sF^h8-bQJ<20M=gb('
    b'C?mraX&jBuIVJgoDFyRV!zYQ98Py;~^HPPLC?hi#X&j9Y#y5PDw9JfLkcxS!LQj;D;Zj4LTIB5m`SdAGPgDxDWJWbe%{*A4moi)hPJ4j=7^7lTlgHps`J7Xd'
    b'@4}RVc^h~kc~v2*G>)d0fR>q&3sN#~Q|VFinN=D`Q%ge2%*X|)n766)DEX`^jiae$%)}|5KBaEnMjoG+w>8c-rDooy(4*vVsFcIYE|3))pKzKKPV+XE9wjq6'
    b'iB%y?%Q||`j7}9t=4~213SU`d&&hgk^e7pbF<a%?@<i{Mkqc5WZ`0^ea;Pe0d6z`B6tv8YT#%Z1n?{e48D*fMPc02CGviUik$Ia&kCGYHM1#C>LM_9$NXyI!'
    b'1Sy!e>GUWW87?(M)6xT4W=0@L$-GUcN6E-=sUc4-2`w`t5Ts(>rqiQjWTVtjr<Q`2x_%u;=50DXN@fIthGtrZZ^?K=r<)X~N9pt^`W-ZM)k6O<W&;^6q$JWg'
    b'CHaIY1@$)YEg~U0QHttqus6k{ATx%PM8Z2E;#;I8A`qpb-iBUCUJ$A#r8>0~woGkGO+5;|&=^tbCdsQZs->}IK1|ByLx2&FlBXoE&8U{9{$=8%CA<{=E?V?W'
    b'8<B!~B6_GXD!wfP?a_J=zk}Cm(v*^VB6_GXQ+y)_8uHYV*plzsKq~5q=%L1lk^NFbomynH^669R>WScYL<`@(fz;F!VLynsDThhrWrxUW%3EHiN##^e1Utmr'
    b'lwgv?9kr~p_YzGiQ9Tj*5^qzINfKMwdr)tKteLIyY<aSGL?=o`JrO;WSWr!p*rHkrTOtBcYU+vTp~Sjwl0+xf(%7;dCe=ed5ioea?KDZ^4z-Bik(PW(3sO)|'
    b'1dMnazH<c)(X@!)k(PX63sO=~L=PqJ)n$_;?x>c;mV8YMQc+Jt4>d-`m$jgwPA!Ekxqh*5{Q@QRHhggl8k%Vlzay*3*S7+W)Z5TQb^8t)x@k%3ZIH!6lDLC7'
    b'MoB(lO2Isl_#KfDxhO^RMB-aSLiS53nYR)DArdlNO4&S$_z00&nNl&YA-{Ezkl|9Q_Uo75vq*?sl$!m*<u@x5GF(dCe#LnEacDvoOX;*<D&B#V*X0hAq$Pi;'
    b'Nq>z!m?SZYGuTu@hD&LTzjG$k3-h;vUvRNsu|y}d%u|y0EZI`MFn=r1&`gU&C$y|nlGpgyQoS&LD<a7+fLbI1p=F;^f0TnQ)eG~t0u4d66!Ao8d8#yy#)s>0'
    b'($n&{0u4#Ej27B5PDx$?WlQz6`buNuFQD>OyQD4il=AqnrFvTaR`A|yP%Wc{wyaaC<HH@&vC@T+B+F>bD~=Z0vQMeo4k`4Ch4BclyUtxu=oJg28d{y!a_k3b'
    b'soz05ZHE+k#lpx14Pmy7swGS**bXW5isg(djicGpw8SYz+aZNsu`uF6Lz*p3OPW%$9a8BP3o>eI$g`zs$y3U@L+DARWl?DyX-n*f)4rorbcfKBiUn1raWq?+'
    b'mO7=XJA|HetQw;zG_={$w6rNT-60t-B#Y(Uq;q=AN{^}EL3^KCtcO0OZab^do0f2>G>*pSoRWOPl!AF$c#Sci!F<R#npy%{vg`$=WL_9vW6Vo1A2N=nmWY;x'
    b'kr`4k4-Ky|#t_Vhj3d=TOxEux)u{#g#-~lGnP(S$;vItdmvLl0$jiQ?Wnt77DIV(e=~2e0;`A@^G%dsbOUuHj4Jl|uphp=N#OYsRR4o!4q-9~$hLki~(4&Z^'
    b'>0e?tEzz{(Ddnl9K}%sohg3Am(A&sgrtgVWwMY~xQNHU_n*L?P8_`mDRsgAK1QLDlS#kQM*sX`4I}6z%BzeOg=MR+R6Q&e&*Ks$>OWM&SdD~vK$jkQfnY%#V'
    b'uGc*gs0C*Ql#=d9?$kVSkvQ!^cNQ`MNb<gYs#B8h+LW5^Ebh25TAUS7L!Vk2Tjs;0eCW;sMs`m=P0FWfk=4xdnJb;+T=#=oa+p%kT?c)#Clq%Q#~z~Y9%LSn'
    b'vV8KC<hwGZqPvH?N(vWLlX9I}WJL1mQ|h)0WUq)8WF?fE?jG*AK5>;e_K<XkAiIYou?%?#CHaIY1=~GIcL*aTG(^)<OiP?noLU04Xf*&F+3rcYLvU6=?Rjbm'
    b'swGb;Pc4aBSW5uX+)LPTLn>2}_^3T3-DeYrJ;)xC_E4u(XAhM<uu1`>X1f&{#_ZxugFW}DrKpxZr9QPZYGG!TaAZ3<>29s3NfL8aOQRNk2Mwobk$o##m~}x4'
    b'wv)5&R-B<wdo(S;oc0~0IJE?7VMYdN?rZG+A=N2Ktkxca?)izs?}0r8?IBMo&mJ;+U?vBt*e?ef#(c6i1$wSiOHwU$N_A?HS&~nm()@MEZ%BGz^#@4JepOk2'
    b'If|>qX%9tv=u_&@@*Am7^Q*u5=Wl=d%m4MSfB5JB`Rz}C{+r+Z{(t=TxBvB*fBp8?fB5#x@4x;1-~8?mfBfx#`SuTg{?%Xn`qxsfsYMX&94)3)<f_b~)YI`b'
    b'B^GrWKciR!-;KWle_!kA8XZvB>WnS4P;2=C=q<zFgZY;u#Foy6mGO7%$1aAv20Lfl4}M>?Pm6bH^}Kka<4dq-$hW{dRy)fSI{Wowy|op+Q~i1H@s;IlQBrQC'
    b'o+W<(W-Y}&{uJe^`XzQX<Q=TrXeYRp*VX23PM072e#mRAZ@T>0g%dbgU++9?%dFLM!-M$2@2tMSx<<U!?~N$o2K##Ud-@&h`(?@p(V>;|2=Ueu`?2qAUPE2O'
    b'^+OjHM{bTh{@5B$4Q>qA4}Nd-8tWUdAN$_u!ius-9Vd~or+dHQ8{l_VUtnD$zJXmBoz=~g_wioda|8U|>NVCkVn6o1(Ul(H3~|J9o(%g(d;|Q>>I<xE#5b@D'
    b'qbq(AHJ5hs4age<c4Ob$yoCCO>xRC!xG`%y>pA9$FKGCOdjtH==nJfCz&Ef9qkCZ1GGgjDJH5BSH^A?$USoYD_G8~0-5aJWoI_zg`n^DW1N_eF3#@CzH?Z$d'
    b'KMp2pEr)YVS-W-W;>Uhx^A*%F+&j?4$riJgFn$%|%<s52+#BF`MqglE1HOS>7|pb$3B5pK$(S1>_JiMBy~g@Rywk7$>Vp^S>(_q;VF&AFD{!vx4e&dwFR-o='
    b'-@rO~61)R;W8d4ng!+c-hC0a#oTK$)-<iCIx<>1VdMOgT!}WvT8@<N*2JFW!=o6TtrE{Ei4A*mS#5ch2tiHgyMtlRiFq$dau&s?#>6<a>2Kc?zYpid?e(Zar'
    b'GgGvbM-#sD?jNup`_ASy)HPf`^u5J}8CvQo=fFpb{KLHgerNOr)-~WQqwC4P4D~&y^VV$nvF~hNLtRs~gx1dM)JIRp_}sgTw*q@_;`y-4E38hNKaIW03LPfz'
    b'L6<q9(_%N)d1uEr$y?avEfSx}pNFn*Q#iMj8|%GE;lpnH3YHh`UA=A~m)Fgm_HJO;SFc?r??9JVkewE9VAt1iT_*29SC><r27ey9zNYCicn7+?uIRLQ1G~Pu'
    b'=Q8=z(2I*~zTmR~U0>;P8N35sUTtz(?8Z7THu<0%xxxC%i>uom=;{K9)8NlTmlq;j_HH1T*8-gOZeZ7E<SvtUpv$vjr^OrC<>{%*;?E=3XNW#~cd+hLHRnlQ'
    b'dz*aTJj+|5-KTjz@H)eFn*Dk3rAu~Ly@_4>bEnaMu=i}wH`ROK^+}u0YCqO}+UDwb3wz@y;XUc|jd*?T=IYlEb)UTX`t@VoXMV1ZZ(!XgaK4WHSohhVtK%D3'
    b'?^&F$UpLf!2I%Vd2G)Hd=j+&yb)N;gI=+GRp3OP>y#sZh3A*~dfpwqI`8wXg`qKyR>7Z}G7bkVDj&ESS=XJh*-B9m2p{rXz)O~8_>(`HUpBK71zJYb0-uXKA'
    b'W4-5wu73Sc_bHyM-y2x(`Jt=d@1X<x>*H}g#DL=w9;kx#$PZM!dXz`S-{T|W|5@Hr9RE-H_xb>T>O+WWaR3Tu(0M+DL^J83a53_G;qK&-aFp^W%y099Ja-Qv'
    b'PHlQ9BxQOie1SX^3L!H2J%qU->S3HPFiq*9Py&LB3b3SyLVN?pp@(p3R6VRzCJlu5MGp&=2|Q}s18vEi17&*jAYI5qh&H+&cEx0w>81^vsuvQ4hmvVLgx(3G'
    b'eF&oh4up9FG}aF($&Uk2Wq>u{A@zT=9%ibM`tlE)Zd81Ys=E=OqK8r}8r8iYsM)KBT~$fp=?BaDMl>Kt06OS;*j1Sn(|)kbuhhMLXjR__>h|hkRG1WieXz8z'
    b')I4PuDE|9kIbNx^`Cx@zDT(-C(OjtzNM+JMsvzoNp)!F-ZF`_C>qtUb(?cnyhPrzXR1(v}Q(;ot?ZI-FQUy)Bkn)%h7PFK}b`RF|lA>A<mg<uFKB`PgCp}oe'
    b'vZDcO+dWX>Mh`QUNkgf(rH4|u232z&s3)X{UAvHCC=V79ifDjZ5>m?L!BSgN$K=6^KvMqT!BSoFR=+Bf0wWI=ypgI1s!R%aXj`c&KxNWU-q_bed2t$b5FYXt'
    b'dey^9m^6?#-}SJt3;EN4H9Z_=@cr{g9p2*9!&8-IA*<Jy(4~RCH!of2OYCUd$V)$z@#XS?2@kw4E=ot6tcO`)U8w2#Vt7Y`L%HV%tmxq|13dBL+o8AXVOM2Q'
    b'DChBVw;VPq6L{9P0d0#C$`|@SVe&lS!Um)r57fkx!&6apc*>?N$M@(!+67XA%V8u+*knl{-tjeAZpD+5n0I`cNbxP-7V>P%VWlc*kd@9mqd_3ccT;+8Icy}&'
    b'9^dvusj$c4smex!t~}UT8bF!AtF}#OtEAaO8Oj<7COmM?AxeenUJvtR+wSp!@>X(~*oFLQz=|Fg(rL@LLvPo^uF6J(N~&u)Y*Z%jtZf6@DlfKh@uEtV(Dw@6'
    b'F3JoECojm+qX|*L((05iO$bV>jlWLXYe-4h)hEw-F=}f_Rh6@)P^y<H71d9DapDferAfmsJ+#-P>?FPw4G6a9l+LL|T6Uw$7D-xa@10smn2T1y2(qD1Xtwi|'
    b'^6Wuc3SW7e(j??Ic6Z_+W$QtrHaOASl;rzvG~4LCPN^E{HnjJNONyIh-O%)+rK@F8;xEh0%m0N|T|C_Qzx+MwaYTBfr0b*~KnrR|5<_}g`8o-gIvBjiK@o~{'
    b'6RIXSC)w7?eS5MMIZu(iklVJ)fe@uLcQ}QwmO&o}n!<EasVnI$S}6%DavP<zC2u+t387URa^UePw6vtgN@PhVw^+h#kgV*19!SL|2Zk0xBVkDAF=@{=@Sk$g'
    b'ni)d?89M75k(!<rY0!pr2Ew;u%};WtGp`WJ0cA&rLKz4PzLO1|wYG7f$%C{K!tp}|FqNSEzl3}O(BM?P67s9ErGwZ!C_TDxm*WrF1dH7AN70o`u&hC<0UMw`'
    b'$ghqtD&;YiJzc2Ah5DRjOXZ*`KRSf2F*uN7oka@+T4_N+3BwA=<V<Is87WCLVgM^SJ(M(^F%kUctcj99iOy)MwCXI}a-bC>xim09B!@cnHVLm}NiULpi?+<@'
    b'2HtYyB@im(B3fl7NQY1ulZT#~4RDe-9eO3sc4a@8Fey~&m=XwGe`q4e9z|&E5--o9$Dl9=eEd}??2+oAg|!lb=@OLk97233nLU4{<k@B`gindG)c_z%H@!__'
    b'+KG7+c4%^>Go%Qe`H889P#KKSDl0cSgu*~L^z>|i^FjJ^1gav@iKOTfn`9nKH}_xVb57~B2vr^=LO)cHc8qGB5d@%4u5@KwNARe|hc1#VW{u{itNdj;?fT;E'
    b'(}OJNX-Y3)sM6Uht`f%{;LNk}p@WHCETwxV%eiuwLwa%V;h`+(Q))9TWV(LEW#ZTa+_&&|A0{=CcmfJebK@?D6g32}<!PMfkb(vRV@@~D^OHDjnYm4wf(7!S'
    b'pUA>a@|_FQ`IM>!3$)C}hYqP&ylAGSPN~k88Z^j<E|P38<ZP6>F_{N)o@?L;8X?Gs9+dN3S=Cj`E3Wj(hYk+)!+6ahSvY|{aGp;I{N<;$lvood4q@V)?C7WA'
    b'lq=nOi0pyuCz8xO10FO?u5|RArk0>u(v;HFk{G&rHVJ&`NqNnwB~K~O9TK_H<X8_l(%8mOScP@nB*_a^OVl3fl&WbVXS;E%L$Z*^sMw5~9oqZsLBn30IE2co'
    b'yzT6vPpQuya3oCbDhabXgC{h+@U{zcvm~P3c;dm&uAJ`tPPHUuhG)78$wDfkF8IPt0uwm3AdE+in3RGBZ0bATaKXpfLnNa-Q(#C*gEKV<%X?OdobS{UR7;*x'
    b'o>~&w=9vORvXITFF4vPxA|HI#mJHivN<|Zb$x=^VUPyKJfFtFXr_?m~Q-jQPR|(AVs->uwKBYdjfUjP;=OLYz5+G{;FTF`%mDe7crUl284ox_qk1X~kft#M^'
    b'nmAI<dP+f)3nnANMjuroH~nc`_hh)AQk+@>w2;r9lBFEXN`&j)B=XirZOODFO(|(YLw!+kl=AEWN8?kbR5W>^24T3bDv|G=T9Rt1Q>s%-ftJ9?1<6txW<4^C'
    b'CIz`-sXb`EliQS<CQQ^<6-TMh9y)u_)BetA!P67bAPmOzn9?&Yi&9IY7Uusazf&!eQVCNwub@K1X<CGZI2`sJq;p2Kis%#=DZzCgEW1KBHr9a=7TV*~QniOT'
    b'rD$44N+wzYM+C`oE~aH-fk|M8*B*lAU1>^5Gdk*vildZg4>%g1GNq!~8#Rb^Ri%J2QcF@TbxL(=DbNylrUz-}bV&PT_Du?MHCTJlq^`6nHO&~QuPTmGpFQAc'
    b'oDm)-#Y0m=Xb`4vMqlY!PA*kTqZXcb2K|m&gw0#dHW|Yq&0JA3$|_gcO&Ukm1M<~q86c#f$td-milY=~4>%g1G^J!2Cp3(?##tkK&QnWJEqO|LYDv%%7_}kI'
    b'{1aK~n8j$)IGQ~q%|FYOie|Xfmla2;&K_h2<<qCsEmN&%CErh}S%wSkec}pm)<e-A`jk4fxGO~d%^&{zKh6@7!;j%1lbCA>b^P@1JiWIByB{1J;TY(C<lc|6'
    b'58g7{`Ou-SUpLhIxT1Ha{b1+gimr|?!HyB%!S2}Xe8ke%tsClnIMX}Lp9fz(ow)=%9}8WLcmwJ-*@s;|6Y8BSKiK&&s&B5`Q14@`UdQ1FJD-7djd!bCe_(K9'
    b'eI2{K`v%nc(5`cN{aD`vzplZ$k=`eTy@U0GosSv&hU<oUA5eCV_XgPcbhB%`eyI1kXzzIaVCO^CzVW)D-p8?><GlfPKFjSIuOI4s3fwzfH`ezAxo@yur1#Nt'
    b'=U{JuozJbihU<rVpLq9<*AI3+F7F$!8|r<~-Z|bIVCPf%uJQVz&gc7`=O=!w@7(~$U~eG3FBN!C#{6LC8wsxA`k~%;8NB25gPkuz_{O`_t^3k~7wYTQeSKg9'
    b'>V0v;xw<#N&bK~X<Ml(G?~8bc>&E)tHSrDBi*&xE;vB0V>wCe)HC8v$`(})Huzs-fwHn`W-B9lfInMFk06X92agEmx^}Yw>9j_nke2K_6UN_YF`jK<Eeys1+'
    b'CD&lxNbfsO&cWUQJ71V`4R_1t<-1nCxpG5&WjuWIw1l1&*PUA#XM|O5Uf;SGw?uny#yP>u3#VSQKM%gj13gx6VwZ`a*JwZ3dB4Uv)qCLO-4CbL8`$+-2=C_d'
    b'gT1#QoZy|G#PZs_uiqW$@)Eh%<Q?$(VztleE$s55vDfGw@cQzt&+0Ag>Po8D<_+xnlBUn*E$s5rqSxph@cJU3&+5-(FRr&a1Je$6ec{Vz^A>h_0m^H%AMCsY'
    b'<;3o!59^CEzK*xBtLr0Pn>Vn_YZX3|cc9Bl240hQ!0VHDpVeE~<w>;H=pFF#jMiuL26TO5=`?u@>_5wMo*=3#I!n$m^_x$6F4682L?3va4Li;LJowT}JFMQs'
    b'u06cdXg}C{g6Ny-J@EP@&u6tC>psbIb-abW@sseLAo@nUKFf3U>xa5e@_haJvF;N@SI0N7?vp%U$9}B)1ku&;4XpPp&)2UT>OMhq^?L*BKFRZS?8mxK5M3SL'
    b'z<ST}9R1#bx=#>Y{ocU3Px5>n?_mAugZBi{H{gqtJXgmzu->ygU%zgs_XN?^tsm+>$@BH=$GT4tT^--Rx=-?a9s9A~6GT_PeyIB-&(-e@toH=b)$g-J<g-NN'
    b'vqa>xMC7wX<g-NNvqa>xMC7wX<g-NNvqa>xMC7wX<g-NNvqa>xMC7wX<g-NNvqa>xMC7wX<g-NNvqa>xMC7wX<o{bGBLD6m|LKq4{`Q~#_`6?NAM%%PfBN>n'
    b'fA`=1`0dNT$REG_GXDDII8h<;_}Xg46G$U>C?od@a!;sLK1$U?J;(1wo)<Xvu22hU?81O#!VM0If3q9exKs4CG^lJN^2eA*X!!}?3$uA|yyenUYnfDOoh@@c'
    b'S}G$DY=YNjufVOaWvY2#MtIr;`<H5EcHt98Bm5s@63^?|-U6@2yaX?Im=|2i8w=a533Gxkw&w!u-Xu=&h1sj6YC1dPMCj<lsc(WWw&!Yx{a~=)?A1D#JDXWs'
    b'J2&75tv}Fx;D&r|M{F^U(;d-05;y2RV$X3ToibzRyC*%};L+u1aUSD~7#b3><7<`M|6>YLO=plx^*<haVYFP@5VFeAO1>O_k4I_kGk~Ra)?R0)ovj_`XPWyb'
    b'ePvn>qs3V6mPeO3Ls?JU4t6ob6?C~ze9$_&d-Wv9or!Wm*Zb=|(!2OR=!L<n)uBFnJUi@y*IRJ4rG6~dZ}eh$(Wno(_M`Gvrh6~1!M+{o$ND>7c;}PO*_z(U'
    b'pWb8r$?A{AdQ;Wo>)1VfKO>|Zj<yZ<r>f_{c%DK($M%W4VDCDu&32}$Tj2GW-FdDXyh<3|6XpbaQ`H-r#0mE1d;=W5e{F0B>rGUDG}fQvuGYBR*~lMct=GDp'
    b'zpxK-+|ew*s$^4crCaa7Qd4Jm#NjML3?l`_#j$mW`k~m5Q`Rvj9bxHgqXYTe2V7WZN$ZjLJnuR7NtfGg_nP}B{lc`dPfIIfcb&Ce&D#caJ;3+K<tA|<7x|)h'
    b'k{r;hz4blPzwjQYKik7gK>6ie&6M`QSKDv3oqi<tPJX*sUT1#0o@#fF>h0L|<6DEn*LcEbj~VD?sJU@X)Qerkwea-}@cwa}mc(}cc<6=2@pXVo;l^b$H+XII'
    b'3hcZz=mxu2$$1@iHPstX=QY^%zVc$vQ~wx`e9BGoJ5%KZUu??-*u6cR;0v?guafUFs1tgzDHr?d$6~!EUtL>u?q6-|+jZBCuQi7uO5>3Yw%YDo{q$lNS9-?a'
    b'83W`EQn^F?qmdW(GUd&6%zVoI#`QEWc4_ef>biF5M7r0;cX4(#!=FdGuFS4?k`H-~^y$vLT(@8EHf`=*>kryr*z<m}eHT2P(DlArY>poa^&0HEOzPZ{Yp82$'
    b'xuNcE7f#rBnbQgNrk_6&=}kS|m%ZFzf9mPH)aM2}m&kox_5Dn5K;73=*PF_VT_u3-sd9q7sppOD;RO3KIq#KCAJUn5{$Qv#XT7>s>fF26Y3Q|L-w*0KXLVl9'
    b'^kJ7*Z&pF*2O`~hr~4Y24|`$pBJ*@z4|E~jYva7y`hJ2x4fI`VU2h{7&=N%NoLsfP+G%L+U+2sA-W<+-0n-J&+Ea^-@dKg$eARc^)3qOOB%R(~J-?sJe3jQJ'
    b'^VwogdUdIl67x8v9-Cy$s?1ZBI#)5~Gml~E<GU+pKgWsMNG4(!e`qI8=8w>08HU9eOYMB%qnz;Zsh#D>yfeN5bsNk8T1S4<PR%*RW5qL!bDq&&o{at)BmoY`'
    b'=r+e*YPf`kBz5IdtLNxlUH}?tRH!3p^_1(;`2_m{It-SZA7udZh^8f+7;BS4L`^EG4V~o@T1VtKLLMf^l5j<5{3YZxtUb?Adt9%L*gN*nIpVG4L<upg#u5%W'
    b'fs^U#Wj(*2M~+36f^g%E3G0|~5nRr`hUxuiF^xcxF1L~kI(mKc1FqdYNf%Jp(yXxF9dUtmZN%mBND--CrAd}u50`k>qr^0RO<8Js<;#^l$1iKlWohHPTmdcP'
    b'*H?--u+n?D+)bZGe%f4FS2_1?!=<(1>taKR#}bD>8%uq()bVEXdXjq1$8e+QC|SlP>r@0+k9g@0U7fCn>gja&c^0o4t&g6YKFJy7p`j6;dK&PG%Q8o-BM~2e'
    b'K7ziAyN0H*<wvj+qMgJYJS<J6%L1i*+7D-pKz8ByckEYE`0PNv2B&vEEu|EroSY0-lI2yy(QI@Y$B!Y6-;{Lz0d~ZE`E`_2u7(G}#xd({{0c|cx$<4$C3YCt'
    b'$F9rm$VZNqml}Jlv8LhadY{X)fX3WPlq_#JsSq*Ra10wp3>vN@@-6D+@{DO5Nyiz}faWBx(GH8{=QLc_@G#@Ntz1s>4t5w=hD$ueu^mhaS}wVSBJp<YTfX6Z'
    b'v86m%={LW+U(($(wMKfDXNmM}iVLV`FJ7!p8hKTeKaAl<dBtvE2Xy46A>^D6d(Lf%9afG1jNjY%wKSSMP9r29og-uIe4lZ>qqeZ0w|Ru&vyS*C>p!-nEYJvP'
    b'5^+b$If7<S9}HKvP953m$XHuqw^E8Ri^mvyny;2!xJE~}SEK!Ww{dLam~xbxP7$y0kF)txE|m|DDfghRo%#5QCOPe34O8r?@pH;Weg;wp67Qz3Cu#@kH8{P`'
    b'ZTm>~QXD_-p}1s3E~!T<Ka|i$?p5*!STV4Ud|k5giY!Rdgj#}x`;p9CyVVgxr3&bXAiXwu8&_J%=}i$s#?s~wpkbs~QKIk2;5vQ;qpNz1lY=@^4J|^kSRXNY'
    b'oHq>f%9!XD;V;4nfGLbtlJ>Q5Ud-|iR&4H4U3R1q$Ph8yI<m(x_A!6soG*W{8y(Q4hx1L;1=O)T3#4~bTtGd0@nUgC?wlDPM;3n)TZel~L2{gY87`&U;RcVP'
    b'd}On!Mq1qDlFo>;!?)J>!FKvQ^s@%b;+%3<E6bIKafX9+9V;aXT|CB$x7a?Ir;)Xd)jety4}qLK%5~;iMravndJP}!L{Gn0!}aw$GI^Xb70JR|ypeCNke(!W'
    b'*xNgia{VQ?whQ&zo3scno@yv}^5ZqummjaN&ir@@_2tKl)$ygc>p9-Rdeh_OhH_@sJ--l6gr4u5NUWgF)0YL*eb%(ZI?vWt3*^c+udu!>ceST>pr5zco2V`a'
    b'>q}IZj?vZYa;%^3)R}9pke&p0JxM!Iuf5;9Hh*rs#`<#Ol}mNz#%riAH-5J~-t=}g$vaqgYP{TvzNC8L+T7<5ORVqI<sJ0K8PgK$JX2e(k0;r@T3T0%yWCKp'
    b'Mt;`Z8#(H7mOh=Mdb?c?*4OK>m%In^Xj(bLjZ||9^(DAjX<4G&6FTcA(ra#d%>;8R7g=L{InWC0Oud#+U&6Oq9B+ENnBxtoH@jVLCm(ifkJog2>BdAYp}yr='
    b'LA|?TjrHxu)%rNo%q7&9+%9+27WUI7J5$u<V0|g-+AX?zU61wi-8xgvCDfPTF6L<i={5Iz*XGYf)>vN-v~sD=)N2j(Wqj{f$DiK5o8%3sJH1`+L>F}B+Pw3$'
    b'#=4g0J=DJ|)>z+eTrH0;(_AjBE4y89r_Vz_X|F#+T~5;HGgNQ4>%n^Z4PRpbwvK;;q?qnh^8)J2Z+q-~`Z^7FbJn~I^&0%<**<?Vasl<^Kuf4A^I9W4>E3#2'
    b'yvglqf_JdK?DlFqIkRfMcQhYRy>kk&f;vxJ7Et&3(h}=DPg|{!GtXROJ^Ag$uG+$W-ezx_x*V=2O}%oBj&83;`}uBN>E;F0m*cJ`Y6t2y_&X2hO-L@Fo;+yj'
    b'S6$iH1=5rAt=7h$;J%;X9jr6Oz1oSs#CqZ0+-DI>tncLI9rVUI(-P}ES6eNRFWp?Pts}|3+ESl~e%9a{nd)+$KA)-j`n?+Nf84K!4cE<fyQZ-X!lny4i~zin'
    b'%?hzmA@8Ho%8j4+$V8M<4i<ov1`NFIk*S!Jwp4dcCS9=LMbg@7XTnRV79Oxr8FN91p@&&J7B&r9BRv+{-5-rzlGF}#XOG11g#JeDk$U_OH9zTmoix9V2}D<q'
    b'178TmZBZuOfRT=);}ItbA33FrQTGJ(u8vgtQDVDE)0<v+e1&?Kytl8|bwQf@!ewi`x#flIwoEo$5ZS)4%PN;`0@)sF|BtRjgObMz9i6i54j75(3b=gHTNWc>'
    b'4v1_?=PT3&UAq8PE%b`ALK}qrL3w(mSM6AOjcPC1d+Q|8rRgWgd6mIVR9nY~lInp9m^8c*V>?Ot7aAJ`kn7Ph;ozmc36#cjCUrn^cqq{^XpqS*Axy+N;v_u1'
    b'LCN(%SI8+5Dutr6Q%J=u##ZIt&7k*9B<q{xylt}gf{s_&aKj5DZ+W51Et5|d1i8vjdrXd8(A&On&KkolD0@k*dx(ajl(Isjr`)>&3*?;5nPh>v!^lMbyHb_u'
    b'w}_GK0tB{X+3jH21smll10s9x2_p}(_kybTh12(Zq1KIh7}bVTNOX&JoHz<42rg=GA(1bMhuHw6fM@__UfL@I3NJIM1Cql;@?)h$&PsEfA4VQHkeG*Y2-0It'
    b'i45e>!-E9O!pM6n>2C+=Z&N<q_`<SloWA9ShPO<fUJ&alpY1E|+%ySq<<J;$+Y5<pn=H2-M7}sv8C{76rIi)-T%#K7RMyD~9LN+1HemUyklB*|S9pBuYZ6=N'
    b'6=jJw2xqWz^;WX-Cgtiq)m}3A=1HVW(>u&5+FPV$9kjh&IS@zR9NP(k-ahGw(Ll^P)iUAXrM)ts@-mZgvJlJs))%7Wu7_Pm9E7VE^B~g~xI#jt7`SetDUp_0'
    b'<{>L9Zv@3}P~JnM?JbknR~dQV@ZpBZoSWV-=cYFtyX_6jZF|j!OHNy3tA+H!YfJh?uxf$#w-~4HsnmuVFth4l3|5BVqO6A`2F5p?q=%$SgN^6xxss`t6kZ~c'
    b'E0;`--Pn9#PoE5n<)Ng#uZez-x0Jc(l+I~lR|4G^v%)0hRVv|g5({HO;%i!CZFwqvZ?a*FrsHK2jyH=lrvXwha%E**jz*yz=WLMynDZ!0QEVGjEJZhxN!cHh'
    b'IPw(}a8)K?()1m#ID9FEN%ELp)AB-^?7d{-eM6UMbiB%-tK7GfhLGnuq``eh%-4<LE=&?cv4gaTMwAB<!Aa`~EtAwvh_#gV@YE3%rN0BIAE~Qgb++C?zIRxE'
    b'N$DABXCR-k_71Dw&@)a3VA_}_$zxTj-#n!}?TkvZ`(jzKu^UlkoJ5r`goQ?$sV(zsYD2Q~+W0UN>Gc}LITILrF)C&w{?wMI&R}^>H5iV$Du?X}kXRnJU!XlG'
    b'M>Oa2g|P5c!op)x|K)c?fYm7VNWk}+V2{LnB<g)fT$d*WTzy9f*IyB|8MWH+ir*F_WkO0w8auIrRCY>d28y_H7^R+Q$&+3Te8xtNhY`_gkd#HEC<H-qpS@>N'
    b'tK~9#C}t<g5v_MvRo@Wo#W}w8ittXUd*^7+*VK5hCEFMv9X598o0M}HUr^>=QYSZS3H#$5Lm~fenlnLK#5d%E$CQj9k!zkN&0>B{r3kXPV)I#&(o0vH-JEQ{'
    b'kStn>BRRG@Dd)2C3MV6Pn=HSia+`F(r0#t~kv8djNwfQgUTjk4k`mV_Y#~irT+-JX-7KU@VcSR~r?jfDqZzp_NMxhY2};k<5{%+i$ks?|2L|VER)dCi5)#AC'
    b'ID0pG+ha<Th8F~MliIf$eea>PYqTJkgz=qk$aUkCCYdj6={5#PlZKaMaAp~_7bE&5+1+dzUlaBk*=>E9iSTBP=1f3JMzBW`Kx>Kl%GMHOy@$;w7^d6Y6J1yO'
    b'n9^aygKw#Qn-T=`cEp-MmlxG0!EBq7(bT>Ww}vT&Nx*7^sAWoJ5}O*)=rM^#k4YFBK%lEstv#tu5^+W)M8&lQ^xUlnNnk*IOIxCjh*w22NJv?O0VKG+TJNMI'
    b')&AH+GWu6i1snY<tTM}J)j7u(bbKU(?IdT_(e_tluu5ZUV-Sf%t8+xhoEN2BWvWLSVIy^g{pTD52}*T*n2GXcjpj^X?9GUUyAm!d?QeWV9<0QyHlJ9PpnF2;'
    b'd3C=~yOA*~`KnT`Qc6nr`a*2lreyS}N;0Z6pp=4=d%loumMN7<y=f$t$0V^ljM8$FL#8RENfoKIsw_YPLeyf!m>^s{m6{SgLkoHkf=65uqb-#qqSc^g%to>r'
    b'NS127D*+_?6N!YI=$)jl+B>Y8mcgn#$5%K$wbMv5&ncbL&aT9fFO~%xdr;C-S_bXO2sKIlI$NHv2sM@5(#98+VD{A-&6$7{l<-yQa;@e0n($RgF>OAh(dl-Z'
    b'-C*Rpoa<&Zyd=d`LQP6di8zDMQVabwayLrD7GBK4RVTSLRi-4@qo7l0l!Y!iA0`Qzapongp+RVfS&RjeTx`TF3GJ`Y`?53=B*9_~LZ>U&_%dw?suQ*dEw0cI'
    b'XWG(L3wjXhTe;STj57$~GDgIUjiPU~My^4tv-K`IrBC*U9)j5^cEEyYQl6HHRj?qLgz=#ztSWP~Rjp2D3wn96tk~E^A7-)5@rlH_mNiJTW#))<48umzlwM{c'
    b'y<Vd{X98oF_2c;D@5gL;>I@cJ2WUFxsvNc_L?6Z<=3Gn5bIzxXan2{KqZYYlDc38@l!h&QW<;oVg^ITxCJBiyiExF&Rw!-}(J9G=P>ez7UxgkPxf><HVwOe*'
    b'6h@{K_?QQzfkieGgqm6Cgez?+s*~5hvuGGCVT<%ETG&IAmNF{Zk~tz;E!50S#@@_M8IkrrT1lVm4?PsKQ|y2R)ucKtgH>^kFX{Mbr;P2GqdjT0+9|eV8v~@n'
    b'#twbKEW`Lj;`;RmW}hu#f1G2GYuMGsClc1_WsT-cK$0EA@yRSDYl-<f=bVkdLsOcol59^vU$Xszxt5lB&ZmrO&L^y+7O{U=-Vc+yTx92Udbw{fM#NYQY4pH2'
    b'E%}0E3XJHG1S?~RBNGtHiHO{dl3csT9f6Sn#Y3*>mnoI;!IgT+R=VI|3+#}4D!31D$X%8=KD4E(7W5#QjAT%JEUI@M5pIZ_qEGA$)6O`17oAP}qjad9Vux73'
    b'-f7i~W$i%=f=V18?G&rh9Bo#s!?dOA7$_wjJLj^fWz;Sb=UUbv%$5-&(lMNJ%jwkdaVEl>HR^Nyimo4j(=toVT4KJk&6&)JXu^DARnYRZ*~R#eDM`z2Gbp1v'
    b'=X{EF$VTJH^5V$Y;+du-cW`iD?35c=V?<}0l2`zpauai83K0>V(!e6xN4W<i_kVbE2hzauu8-V6k~?#H>!``m_+X9XPSPnj+LBZ!Y{4z7VT;~4JE?^|$X&2g'
    b'MnzkqjtDK~Hj~_lI*ZvUBVzBOQ~G3o=pmV%Vh1e9CWUDktUBlTf{qU@VO5)>?P_(IwnQ6)NErV)M|8}2IXN%L`M3tfTEhNwjzMk)W*Z-7qP$t7ITIMWtRKfG'
    b'e-G9YQlE1sw@H)DCsrlco)CQ@*nWX_X&L8y${6Q-!a8aZ`^EA$B^f(<m;07-&yqJJA<5lY=#;ynaz`|kDan0TjA3K~aby?~xf`Sr(IaxVnB@lLupp-?$?aZ@'
    b'AxrNAmuO2<ov>wOIzz+w(3Y%P&_kA%GAi0qIU-t}#SXFan0B7CchOm_KapT7_k8C}uy<HBErV5gj<0ZhYNuEg=4hi@eN0=bjR8`yv12ZiSqAMQajs<zj@k0$'
    b'h;$5MakuedCXP32G-m>mtRKfGvsA1l<}1!QlMywWPpnFrd!lkx^fq_Z{Zi+A%Bbdi!a8UfSza6&TSV?gY1o1*g7Um!EOK|fOlkChI2}h85J#pE5z!%y*dGz?'
    b'<H!W!$S@*uH%fBjAG1{D{=D3qZ&MO1#?Yj9!O@nWI$_JmbcTlUp)Fmtpob<F%guh+QcoQbS~k%)S|it>)!BL%ozf@!Ll4316gyx+G^tL@#41>jOv3ok5>}Nt'
    b'+NxG3vjx4pSXON8q7Sp!=J-V7T+14y*)nrPI)-7RXeuu=kzTJ+oil;4%ldJA^7mu5Jaq<(tphY2b5#!86QU2}4|A@i<vHh5#yIB_)=`T*c`+<+WlHkw2znn;'
    b'IgZF3`(ct~EQr%l@&(Bh7||gOETVmsJVP=J<ZhG%%coI}M>^yYk1(Y$KDZ+<*-8@}Z7He~PlZUP)8*L|*fM$+E$kslCL<YCqb->ug4OAer$uD!&FpM__AXD9'
    b'B<+tq6txp}z=CR0pO(R@ILDWCe6&->cFfV9u-fbtTe6OU(xGFgzMz(Id?IoE<RO@5En$D0V<->N#PMM!uud;)WHUiYb`ZxWvy`kQ=IfkumLAlU=Bgyy6VR7z'
    b'zhJJVWuEgXqbgGp>(Xz2^B8^p>hHe&%b)-AAO7tRfB)^5-~RSr{`sGN`SZVg`Talr>o0%)@(<ts^!smLj`LT4@#|mz`b+paVgL);AAOu+oOtL>Ur>3e2_|*#'
    b'wG@6YrDvuiesoX<xAUw`pWqx|dF=xA+sAo~yp!=Wz*lxB{B<N8wUy&UL)O(Fxo%HM?h<W+*Jgi@{qhsQ-nCkz$>}lQ|H>EBy#@Yq2ff^5ZgjpmOZncC<j0R_'
    b'ePPRL(%oC!2fo;7i>>lwv0kIE7O&jemS?%QmCkbOC&T8)*G#^jlB&ECal|`5$&Fsk`th}-raF&0P6f)(0AJaCXHy@yelf?rpW|`!*S?r@ziU}c+ZOoC9rSXq'
    b'`1{V7x>8CwN50f=PMQ~fvDv;y{{--r;fn=xZ*w2`Vp}e@*^k9~jsEhn2Xk)e4;|i}_WyzVeM{2>cYP?4Lq89BeIsJ8)Hf_u?G9S_=-y;i8dyjyFwWpo={3}!'
    b'0KT@HKiO1E8)uiY21ih^(6Xc|#1VVw3&Y=mzx)KWd%dpuE^jCw+Qppjp}*XMFSpu_-Z>v{ijm!zI4AsSvwn~M@!(6t7i;GJnYh50JN5lm`=MC3(U&XzcBA0Z'
    b'k9(J2!kzonkG}&S?w|8i#^2<H?s&&9deO^O8-Xn>eAABwU)s$Xda0Fj<2T|(Ul{%l{N*R0-RpJ3CoblE5B=p9e7V)`^zQwcEho+izuc_OF#37$wc+pA%>6TQ'
    b'fv<MzVypd7tlQ`>_dKF+m)~=!JNSFyz?ct@Q)l+5DId8Vf=Oq3vz79Hh&jKOBfq9Ajf4b})4wLh_~Gae>?O<S>lHfrr{io=V<w+@7k*{?JM@>I0snZdu6jIQ'
    b'Z(KaAx0viL@RwWYmyLC!L$I#D4RAN+$BDn*ncu;G0{R2n->;PaSK&fmZ%f@)KLFvj@Oo*FH~+*N8~GCb!Cw3ra|a@IhTgES-t@(8{CZUeykL%6IESrADL)7P'
    b'f%U}m+B^zy`F{Xj_@(jRqrdzNxPRqt_`Su<@1eikgD*GTjot~bLeVQ^nRjQ-hriym-@$(Z`UBe+>vrP@<APsr*~OOo!DzqfUv7Fz*N(sGXgBcp;Hg#4N*k_1'
    b'9<aOVDV_MMwaed``g7nPSRa&zBjnUSip3l7E92jxzx)iif8}oZ%6BurhrZ{i*PHG}?{9a=-I;UZuQ%;?@SlMG!1l$u`F}7z`1O`uY`Gtd_M3jw(fW4$O-H+d'
    b'zXv}VCeGRhzQ=UeQ#$ciYj-k8D%;WRFyVxMU_J5UFICE*-u%({;FrdKkN)yA;Qp1n<tyLK{2uzAqh4>i8@&^*4;;kXGv~u!Z`$wRKLP!L?TdB0@q=-}uea=C'
    b'%l%-q-}IY~*0<wtI@%5V9r*FJHo)iQ^n0GtjbE?b@wJ^H|2W78R$@lpJR9Ktad_cZ2ERjp`5AEk3f=IDI@|XVUv5Fxo9IT5Om*Jeq`WahPW<(T{0{yT&>z?y'
    b'?)mDEAlF-Pv4wsx`eSpy-1BPJyY{9d+`!+1=L63kj)4n>NW8vJpAJ6wl6xwx;Z4L_aD6zlq;Xa-+UxD7)bTXr_*IQz#8Q49er-PP_VNMumtys|Td!=>2eE%h'
    b'd*9Swb*2|zG%YU|6Ss%{asz&~Yuvrxny7Gd9m2h34!8Eu#k@QB>kah94qI)Rp8)sSez}PJN7#mIis9aVU4U=wHy?Vx>&3H3xk$tF9N9&0J>Nu^7~VXEddoX*'
    b'!`HSi=jmqSm0_2j@^*9IoL_X6-n=DnXPdggU;JqACco<Y&K!k%3lMItZn(2?ydH5Ae6g)u?r<0FGyHP#Uc02T+}flouz#C5(N6G_U*yRz^5hqJ@{2tAMV|a3'
    b'PkxanzsQqc<jF7c<QIAJi#+*7p8O(Devv1?$dg~>$uIKc7kToFJo!bQ{31_&k^j&5MSg=T>A(8R-?<9DZq@qRsWP}z-f*k1;#SSLooaPkb@KLV^zD=;+^LDU'
    b'RhMw9B;w7=kN4_I-l|!7uO8-3dB2Uaf*aKgcd97fEEssNUf|7Qhxck7Zq=LKsdT+lVtcE&_q}4pw+bQOE3$mEg!4|R>YW<dTXm|pN@Q=<1>dPizEKH%rvm#<'
    b'iRq2f)*BVIcPe?`ELwf9X7$a2+xO~iZ`IA)so1wuDsZbv;a2^$oyu)nHRJZ`)ooSk+bR;cSEg^TM&Mp?#I3@NJ0&5vic#*A%G)T>w^12zry}8IalO6TdYgp>'
    b'_v#96)vw;EoV`=Bd#hOZRvqJ=3d&oxoA>HQZ&l3RD%QPME_<(5_g<0mtpe#grP;TN!ta!<-YAv5QK5UMGWceZ>%AJ+n+3l2>U)3UE$#d7g73Y2zWM6=-iy0i'
    b'FAeX#u)O)Y^zApow_ZTsdo}$2yXc#5+wZ;Wzg1^oug1aNOWIp6h~Iu6{r)@en=g0oz1#hX7ufH=zrI=VXs_PVUa_amQd4_{Z?=l=>=pdkEH|`OX=$s-(_WdS'
    b'y&6xO)vfkwYi-r_+N&wHSLA4`z|vN2r@gvTo5hj#Y9nnHhT5wOwOOfjuTJV-k=D%;v3mt8w~A%%73$n96S`F)b*nh*UU}5L+N_&ZY4>X4Zq?)6s|CDQoOG)&'
    b'>Q+tGy?U^lMNRi=nr;?!-K*!i$uO|TZ?H$Muu1K(S7?5#$o*b{{mt_JTg(PqqzZeq278<en`{z$TozkA8hacbd!zzega%t&3VS>bn`8ugTm+j$40}8bdsJRq'
    b'G-CH@%RWJlwnyo-MJKgKWwlA9wZj^Ao1^SLPuLbO*(L|u9s}GK``jM$-F?cg+q7UiBxGCkXP=<=y3g*lM_{(aU$$3RbhE7KW>wX_ny$C%S>CIad9xDdy*i&;'
    b'6-~E_sqU3C-K(W~uW0PelC<{<-rg#vyH!hcua4<n5!I~%u3Lpjcj}OC6<^({y}DIHbgzEtUh&ke!mW2oSl%j*d9U#1t)iYgrAv2erf$_O-71-St1j%lnzOg+'
    b'+1{y?yHhrFt6=F?t<;?=ty=|0KVNV3&ffBYpM_4Jg-)M^PM?KNpM_4Jg-)M^PM?KNpM_4Jg-)M^PM?KNpM_4Jg-)M^PM?KNpM_4Jg-)M^PM?KNpM_4Jg-)M^'
    b'PM?KNKPYtix4-}Pr*D7tr$7GtZ-4tY-~RZ!fB)NWzx>-De*f*SfA{w&aQY>F4Uh4kh%4G}1bp@Sn>Syu87o(PFTWsPzMmp*TJUBCZZ7Ce3tSi0YwU7U12=TW'
    b'-!aE}Gehn%5SO%F;br%s$F9+58F~KA|M^e<7pT=kuK'
)
G.update(json.loads(_payload_ast.literal_eval(_payload_zlib.decompress(_payload_b64.b85decode(_G_LITERAL_ZLIB_B85)).decode('utf-8'))))
FM=json.loads('{"WholeTower__AntennaPanel_1":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"WholeTower__AntennaPanel_2":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"WholeTower__AntennaPanel_3":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"WholeTower__CrownBearer_1":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],"WholeTower__CrownBearer_2":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],"WholeTower__CrownBearer_3":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],"WholeTower__Diagonal_1_Face1":[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],"WholeTower__Diagonal_1_Face2":[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],"WholeTower__Diagonal_1_Face3":[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],"WholeTower__Diagonal_2_Face1":[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],"WholeTower__Diagonal_2_Face2":[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],"WholeTower__Diagonal_2_Face3":[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],"WholeTower__Diagonal_3_Face1":[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],"WholeTower__Diagonal_3_Face2":[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],"WholeTower__Diagonal_3_Face3":[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],"WholeTower__Diagonal_4_Face1":[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],"WholeTower__Diagonal_4_Face2":[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],"WholeTower__Diagonal_4_Face3":[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],"WholeTower__GroundPad_1":[1,1,1,1,1,1,1,1,1,1,1,1],"WholeTower__GroundPad_2":[1,1,1,1,1,1,1,1,1,1,1,1],"WholeTower__GroundPad_3":[1,1,1,1,1,1,1,1,1,1,1,1],"WholeTower__Horizontal_1_Face1":[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],"WholeTower__Horizontal_1_Face2":[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],"WholeTower__Horizontal_1_Face3":[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],"WholeTower__Horizontal_2_Face1":[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],"WholeTower__Horizontal_2_Face2":[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],"WholeTower__Horizontal_2_Face3":[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],"WholeTower__Horizontal_3_Face1":[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],"WholeTower__Horizontal_3_Face2":[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],"WholeTower__Horizontal_3_Face3":[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],"WholeTower__Horizontal_4_Face1":[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],"WholeTower__Horizontal_4_Face2":[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],"WholeTower__Horizontal_4_Face3":[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],"WholeTower__Horizontal_5_Face1":[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],"WholeTower__Horizontal_5_Face2":[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],"WholeTower__Horizontal_5_Face3":[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],"WholeTower__MainChord_1":[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],"WholeTower__MainChord_2":[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],"WholeTower__MainChord_3":[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],"WholeTower__PanelArm_1_1":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],"WholeTower__PanelArm_1_2":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],"WholeTower__PanelArm_2_1":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],"WholeTower__PanelArm_2_2":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],"WholeTower__PanelArm_3_1":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],"WholeTower__PanelArm_3_2":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],"WholeTower__ShortAntennaMast":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],"OpenEquipmentRack__Chassis_1_Left_HeadedPin_1":[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],"OpenEquipmentRack__Chassis_1_Left_HeadedPin_2":[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],"OpenEquipmentRack__Chassis_1_Left_ShortThickHandle":[5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],"OpenEquipmentRack__Chassis_1_Right_HeadedPin_1":[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],"OpenEquipmentRack__Chassis_1_Right_HeadedPin_2":[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],"OpenEquipmentRack__Chassis_1_Right_ShortThickHandle":[5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],"OpenEquipmentRack__Chassis_2_Left_HeadedPin_1":[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],"OpenEquipmentRack__Chassis_2_Left_HeadedPin_2":[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],"OpenEquipmentRack__Chassis_2_Left_ShortThickHandle":[5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],"OpenEquipmentRack__Chassis_2_Right_HeadedPin_1":[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],"OpenEquipmentRack__Chassis_2_Right_HeadedPin_2":[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],"OpenEquipmentRack__Chassis_2_Right_ShortThickHandle":[5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],"OpenEquipmentRack__ContinuousOpenFrontCabinetShell":[6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],"OpenEquipmentRack__FullGroundFoot_1_1":[5,5,5,5,5,5,5,5,5,5,5,5],"OpenEquipmentRack__FullGroundFoot_1_2":[5,5,5,5,5,5,5,5,5,5,5,5],"OpenEquipmentRack__FullGroundFoot_2_1":[5,5,5,5,5,5,5,5,5,5,5,5],"OpenEquipmentRack__FullGroundFoot_2_2":[5,5,5,5,5,5,5,5,5,5,5,5],"OpenEquipmentRack__HollowEarMountedChassis_1":[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],"OpenEquipmentRack__HollowEarMountedChassis_2":[8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],"OpenEquipmentRack__TruePiercedRail_Left":[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],"OpenEquipmentRack__TruePiercedRail_Right":[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],"WholeSolarRack__renewable-solar-rack-01":[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11],"WestDivider__sports-court-fence-01":[12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14],"EastDivider__sports-court-fence-01":[12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14]}')
PALETTE=[('WholeTower__M0__Panel_Porcelain', [0.7699999809265137, 0.8399999737739563, 0.8199999928474426, 1], 0.6200000047683716, 0.03999999910593033), ('WholeTower__M1__Mast_Charcoal', [0.07500000298023224, 0.10000000149011612, 0.11500000208616257, 1], 0.47999998927116394, 0.44999998807907104), ('WholeTower__M2__Lattice_OxideRed', [0.5899999737739563, 0.0949999988079071, 0.04500000178813934, 1], 0.550000011920929, 0.23999999463558197), ('WholeTower__M3__Brace_WarmIvory', [0.800000011920929, 0.7599999904632568, 0.6200000047683716, 1], 0.5600000023841858, 0.18000000715255737), ('OpenEquipmentRack__M0__PaleAlloyRails', [0.38999998569488525, 0.4300000071525574, 0.4300000071525574, 1], 0.47999998927116394, 0.5400000214576721), ('OpenEquipmentRack__M1__GraphiteFeetAndHandles', [0.04500000178813934, 0.0560000017285347, 0.05999999865889549, 1], 0.6600000262260437, 0.07999999821186066), ('OpenEquipmentRack__M2__MutedBlueCabinet', [0.08500000089406967, 0.17000000178813934, 0.20999999344348907, 1], 0.5799999833106995, 0.11999999731779099), ('OpenEquipmentRack__M3__CoolGrayLowerChassis', [0.23999999463558197, 0.28999999165534973, 0.30000001192092896, 1], 0.5299999713897705, 0.20000000298023224), ('OpenEquipmentRack__M4__WarmGrayUpperChassis', [0.36000001430511475, 0.3499999940395355, 0.30000001192092896, 1], 0.5699999928474426, 0.15000000596046448), ('WholeSolarRack__M0__steel', [0.23999999463558197, 0.30000001192092896, 0.3199999928474426, 1], 0.8299999833106995, 0), ('WholeSolarRack__M1__frame', [0.550000011920929, 0.6000000238418579, 0.6000000238418579, 1], 0.8299999833106995, 0), ('WholeSolarRack__M2__panel', [0.054999999701976776, 0.15000000596046448, 0.23000000417232513, 1], 0.8299999833106995, 0), ('WestDivider__M0__honey', [0.47999998927116394, 0.2549999952316284, 0.10499999672174454, 1], 0.8299999833106995, 0), ('WestDivider__M1__teal', [0.1899999976158142, 0.4000000059604645, 0.3499999940395355, 1], 0.8299999833106995, 0), ('WestDivider__M2__sand', [0.8600000143051147, 0.75, 0.5199999809265137, 1], 0.8299999833106995, 0), ('SceneOnly_RelayPadPaving', (0.3, 0.32, 0.32, 1), 0.94, 0)]
# BLENDER PHASE



import bpy
from mathutils import Vector
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=128
scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for layer in scene.view_layers:layer.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=4
scene.use_nodes=False;scene.render.use_compositing=False
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='AgX'
materials=[]
for name,col,rough,metal in PALETTE:
 m=bpy.data.materials.new(name);m.diffuse_color=col;m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=col;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;materials.append(m)

parts=[]
for name,(v,f,mi) in G.items():
 me=bpy.data.meshes.new(name+'Mesh');me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o)
 for m in materials:me.materials.append(m)
 face_materials=FM[name]if name in FM else[mi]*len(f)
 for i,p in enumerate(me.polygons):p.material_index=face_materials[i];p.use_smooth=False
 parts.append(o)
for prefix in ['WholeTower', 'OpenEquipmentRack', 'WholeSolarRack', 'WestDivider', 'EastDivider']:
 parent=bpy.data.objects.new(prefix+'_CompleteSourceAssembly',None);scene.collection.objects.link(parent)
 for o in parts:
  if o.name.startswith(prefix+'__'):o.parent=parent
 parent.select_set(True)
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
triangles=sum(len(f)for v,f,m in G.values())
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
if '--geometry-only' in sys.argv:
 print('GEOMETRY_READY',ASSET,triangles);sys.exit(0)
# Render the actual exported geometry, not an unexported proxy.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
parts=[x for x in scene.objects if x.type=='MESH'];assert len(parts)==len(G)
view='thumbnail'
if '--view' in sys.argv:view=sys.argv[sys.argv.index('--view')+1]
assert view in ['qa-front','thumbnail']
scene.cycles.samples=16 if view=='qa-front' else 128
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.28,.28,.28,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
focus=Vector((0,.25,3.05))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-5,-7,12),1100,6),('Fill',(7,-3,7),800,6),('Rim',(3,7,11),900,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=10.10;aim(cam,(10,-14,10.2));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/communications/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'scenes','assetKind':'scene','theme':'communications','style':'S01-clean-geometric','title':'Field Relay Tower and Front Equipment Service Pad','description':'One static field-relay equipment layout from the original communications scene direction; one scene and zero new standalone models. Four whole original types at unit scale: a full tapered triangular antenna tower in the rear zone, one entire open-front pierced-rail equipment cabinet and one complete tilted solar rack in the front service zone, and two whole original court-fence modules across the middle with a genuine one-metre opening. A single new6.4x6.6x.16m closed scene-only ground pad connects the front equipment area and the rear tower area. The complete source GLB meshes, oriented triangles, static poses and per-face opaque PBR remain unchanged except declared translations and collision-safe names. Original equipment feet meet the pad top; full object envelopes remain separated with a continuous open front floor band.71meshes7644tri16PBR. Distinct from the earlier small reflector/cabinet/radio communications station and the unfenced offgrid wind-turbine/solar/cabinet grouping: this layout separates a tall antenna zone from a front-facing equipment-service zone with a clear central visual opening. No new tower segment, changed antenna angle, recolour, extracted component, cable, power link or communication function is invented. Not a demonstrated relay, transmitting system, electrical installation, secure enclosure, human-accessibility plan, construction/structural/load or safety certification. Original dynamic hierarchy and custom corner normals are not claimed preserved; original static world geometry is. Preview ground excluded.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':16,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
