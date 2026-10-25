"""Original complete horse feeding/watering court display, three whole existing models and zero new reusable models. Lightweight maker SELF_REVIEW; static composition only."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='farming-whole-horse-feeding-watering-court-scene-01';VERSION='1.0.0';TITLE='Whole Horse Feeding and Watering Court'
DESCRIPTION='One static outdoor horse feeding-and-watering court scene built from three complete qualified originals at unit scale: the full arched-neck horse stands behind a separate empty V-rack hay manger, while a complete low stone water trough occupies the left-side bay. A continuous scene-only ground plinth joins the unequal feeding and watering positions with a visible empty center-left approach. All original oriented world-space triangles, face material assignment and constant opaque PBR retained; only whole translations and explicit final float32 coordinate storage. Source node hierarchy and normals are baked/recomputed explicitly, not claimed byte-identical GLB. No old parts cut, rescaled, recolored or multiplied. One scene, zero new reusable models. No animated eating, edible hay, water supply, husbandry/species-fit, navigation, accessibility, stability or safety guarantee; static game-art display only.'
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
LOCK={'animal-static-arched-neck-long-mane-horse-01': {'bytes': 93884, 'sha256': 'ab49e582fdd487e8bcbaa1d41e3621ba586f54ccfd129993dc8e17300136fb20'}, 'farming-empty-v-rack-hay-manger-01': {'bytes': 29172, 'sha256': 'c5b9f6bc8e1c4a1050337c79c3a3455c7bd0f881592129544369a387cc1b2322'}, 'village-water-trough-01': {'bytes': 19800, 'sha256': 'bf438f4364998e10c80c6ce265b9fde0c06a9693b98b38803757864ec04f299b'}}
ENCODED={'animal-static-arched-neck-long-mane-horse-01': 'c-rl~2Y3`^*EfFdAT59t=`{opkO13v1KF9-yL6Bu5J(__kc1@k5_(5KPz0r@C`|+`h{Dcb!3L-(ii%=G5k(&XMG?z)?#a$_Hq5;<`|`Zs|GWMd?zP7sXV0AbwAr0AXJ#@cvtP#;063JzAl(7bwQtY6r^lz{<)!7vx0)V5CM_#1HzhwiH@;PTxAffXtn9qFF}O)w+sw4A)U@2VE-ib;O>(txws3jl6XGYO<>qB%XQ8m8g)M$&LVVsRR1n|F7DRdRt%gjG&q^7Oy!gJ_X9@9H*{RwGcE`Ol@4f!d>G5e(@^e%2xEZ6e$LC~crDf$0&&|%{+xE;#i<_K|I4(6UEhlbdN^WjiX58eA{PeiI^pu>mRQzA|#7wj>FD@l3H7-3PD|N!el-zt|w2sTlj!U07K8G7PJ}oa@voC1WK(4es>TIj2>>Je5CM&g1_C)kJwKLI#3L;vmDZ{nLq{pS?j!H+X#!t)}H8C?KH!dq})VR1&*;)A+Srap|#>8c0<!8sCNZL5f-pp)`H!3qDOWSJNG*lQe*B)+eXI!9-rvGl#il%nQt=nf$&YGN(o7zL))`F$ls$;X!7F;wlZOjb@ro@fT$jZo1iyM>6qY;;$ojv-xS&neCx)v(xh*gu{J#7ry)dl}OCO0LsGj3-4zhaUz8k6k*S4?sln$#yPCHMcUAi1Nk$TUWL&rDCr8pGGl$2~C@P0CNn$c)R&$i$r~Ek8dkf$xB$aK+3x+>6F%WThaOI6D8jMV@ercs+M6)Y-34Wk1wtW=Y@iDVdqUZ;8B&)U>#?sR+_ic#tx(;zs6Xr=%9{a@QC3hA-R~H|sDp&Gx^sl+SP})A+V4Ol|hWytw@I4Ez#FP01Y>H$DZ!o}$%3;WtZeT3)^uXZ*U#n3Rz^F@<MfJbw3Zo6=J<v~RDVDT(2x^y7N_PEO0o?}2LDaaGppaAHm_eih}1@{Sc$_??_v_}z)$(|Po3tjO1H|H93KDejPxYy00>)^4(FVGc&6XJn@4rs0p-5L<#h!I9uha3#1CJPF<eUqWI68gIAb&((G7v>(mk8L6l@B`X6fqIq6^N`A(u=7rz=&3R&)^At7b*=nAiotu}|+-ApLz|s8sXn1NyZrZ5)!k^FPgOFXg`S3{@d6>Q7*;$!W<6GtDPE1RP&qj+gvWBOo<WC%r(wrHrKGd2q4YgsqM{@7;;_z2CKR2y)-019yx%$@t-~Z$CP`>cjv2asjW?Z3hnHl4-l&9cMnt?|E3GunwZ~k!p?UI`^3J(zCrw@%!NlnSg&zO`pG`>~b=#<Pn+`WeuW-2cOD|L(^KRb80_B$W`;nY!R(eTu?tn7@uaD8cf=hs+6<J%2t*S$mEq4Aubmoh#lvrvuQ;p3eA^xU+RRE^^z{~kUbmn+=9W0!k6v@hIzQbyY3;h8B@(J8X(5N+9eXY!H>77Bi=X|;0wXSOqsP&_|i8K1%fgqvswEveZPM;7kQsd~18I<zg?rQ_a|H8CHfnKLrCM;az7Gh-AUTZ~D^!y~PZc(u06&dkp3h%x3zUPEjxoGzR8pVRI2IJ`b@f~|$!?$%fio6lqSINY3PD`eShUYFbE_SrlMyhO(bSJCz1ZkMYs7~-|?c@wq&+zuzI^SNg7oxsGK_W0d{zY3G^fGs+I>^7ISn8)j|dtENKiyQ9^I+W<MIh+oM#&Z`M<@30GzC^bxF$#wg?S<+*4u{9)a(b;g#J}{k-<RlIvbhUgO7z<7iC&M_>*4m}(%OG+r^n^8`)p3mv<E}&aJcQxM33DUjaP-M_<S~RqRnf!;uQX@M4KP1phCMHc8|^D@j12XviX8li1vHY?m}LnFCM$Y?ZM1NlOgv^ZU4b<<?zlRx`S}^EH`6(2LBE!)RK~)pPMmqVt$(DUay{gyY%bQ^KQ+EyL<NO(WX282H>vEe;G${8OQZ~7=>ou%R?IN@wH_moY#$TQ6t<YMwlH<TQ<OR-2g8&z!z>nf>=W$iKC6G;J>Wbb=aeI!fxFOyMx%^470&y*$=y$DDnJH91$J0Tld3DOz?%7kZ9Qt2Ptevcx5|o#*ZlS;UH!02&-#{+qxg5G#%ck{19{q*6sI^r4#AWP8(g?apTgV9>Mxofc^SnPDj{cPP&*=xL6dKak|K2?y$u?CW{&M0oK<gmF*0xY-gfLL=E}?%gegRzTgVm7hGmv^9Fr@^=0YTx-0Us_>-413O~!k-)2qe$cdvzr{xa7V^QrlD%9olo0@~hx$S(v7==H4`P?NfX;TUh3WLAVE-(Lq#!u`myuRR%vCr+aIlTO6!|ic+>@IJj&+T%fn2Z17X7H}2xq*fokD3yi+gsr0PM_OhcYEE54zJgVD)Kek;s<nS=hV6->Vw^a50SQa7;WziZSV2eLfiLk*QR@$J~wD^Mz+B1a$S$2qc8?`o7ds<Iq_&G!O_Cy)Oa3`*X?!K92i)qk4Mqxw(%n$hs#H!c%ufC4<5@peR$O8_VMHOL`?%8t$TfV3~#fWMA2ozhe+GIBS#VQX%<CKWDD%>P%Sp+?T9Z?t2&Ph58ypcjDaI~@NRQ?oOp1^gW$sE#pQB2U3i4-_Tn*eST(xrHXoL%4G)WLJ|{o^w+B_AQYW?wPL0KjkuT-3CE9#$lQ4QMI1y=kU*s@4TpqJ9CYo4a^U*LS+PxmF(Zk|%*%JjpaQU20x7+Q&eG)rDyEi<HK8I855PUw5&5L2j4X~Z^;LhuD*?hb=G24S}7Hp2Fz#chl*z}o&&F-*Veg>rzW%U`<?|-BC?9Q94KD+Ct%g^q%Tz^Kj6IJyY)^GIH=egPH^G5Z}<wUc5i8iOl<953o+P8O+b0G=Mwck<vjpXIw@i=VZzW`3JC(()j@zXGgPM3BrrfB_XN)iz#dK`%^2WHV_H~l5`-E93N-gNyqY|(swVS#vXKhh2zoQY0{C=mGj=kmI2UVhfZX16=SqUrHCac_1z@aGqU?!m(nEp{#*JEz_0z#mkHw(~|jim=~g6*(L?{T=3TM)MtZLlH$;hz6zn-zh_f>n6+4;lBAY^hEPDc4GxaS%yZH{68r|@68sW$u|Igr(Sp4ZZG^5bh;f_Nj@L{8FUq%v$H4Ky!hpgzia4(FVU5VPCK26wnRK!O{6>DjXIDQJjaLM^=|yk!FvLO1LBB&BwFwzk^-kKatXN{=3Rl=H-gJXe-^N49r$~O`Nyuw#$9*0_&#ZKy0im%6!-A*2#cPtuov*~qOsZ0DOBM|#2-U``0wx}y7}*CBJRDsC9@@>1Ridf#LnrkV0T0XPLtiw;WLe$%W~`lQHUatq2S+i<lHwKInT{U&g?6|M<Qp#121Qy&xXgL*g(4Q7}(JQzs2lc{C@J`H?|8qN(_UKA9lI;7o5{=$KMEAf;XzLxA53;cXi?J?{(s?$~8D#h21DWXYWjOdCm4;r_X{H5fzvniTF$->9R$$|K2zY!%(`ye@(HVFjx*dey7<J`ERB(Y-cWd<m+hRa2EMC#h;Kw-ZXf84mbYJcoNM@(q+HNl5{z4x+GoBXm;isqYy<Hjq~td2%{_7Frvci3h0S9?WEhtsrhN$)3V0o^DA@`6CH(|o}))=7s7E}DY;`f#OBfCxNePwjSD$ex5pz3Tln_aj=93OcShLW<L3FN+uQ9<o6EWZ1`51BXEYvo`Epc&!{zkYth<0eA4Njwz@wBXTrg08N7SBZl2~+m{6h6b;Q<~ahAVK|u;iog;6??wA4cH;?p8&%cle5yVRSig;!lU|W^#Z(Rd&Zs<Ny!HquCJ*Lg;mQJvWsDpV#ZSnGm?}n8<fi3haq4+fBsK<@DJdHxombE2=LO0|jnRG&{l#b?ox^itY!|)v?R#aNX2*i7U}=znSk6Y?*vF^<CoT2W~f$1GmE)&5nS-@<o#1#_rK^QwqFMeVO=NMSc^pTZroW*yAgz!0vEGvnSrDz>(;PLV?R&BnKXs=O#UHNB5g}qXLgNnjPUr4}3016yL}EN}{3)e9_eLjS9SWTQpVV_7?E~yCIwHW^&+lMztduC~#|G{U7JR>$N*QH{}5z>E4tFiH;k;3PQ))!Q*VYE8DPdn0fEaxVSi95`(r~?uMZ&+e)wOdRAUovVttaTYqUNZCU<uMC=~-ng7dX$0B0q@tXbxKb|nd0W*v`14O?eM%xr(ry)ik72>ZDH+^zzM9g(|JMv&e%xx=s=kkb{`#5^^LNn|)!#w6hzai$iBX$~MUIWBmL)_=UCaJ{h2jnNWzbIM3<L+B1-Lv?ZW&GlMPU*z9)0T0w`)BxLPkj>&4n%`-ErqOWiqRK^_+^SQRtkxmCH%|C$1P*N)}}2hEo1IWqdBuJV;-whkLN^#{n22aYqG8>=CwrpGR3@BN!(2F)|`O!92}58U*5uR1y5eTMf&#HW0rB}O#`GCmwjd#_kHO>|AD&SMuP*<U|dTf>zZQpMInBfVvLnS;${hd_t2x3F<<MsZ<kxf+?SVYO|y)7tX};sJsRwf2J>8#bxkp^CE}MU=Cw-VW(nsudrm$acuKK?`C1d_zit_GU(!~dw2XPIt~B{98XSlQ^IVg4O);+};+HArwMyb<31|1*Vj1(bGOw(#jJYpYKPs?{d93(%brjei4d%Hf>zZO-OT;fz%xjgz%@j|s{IvAz#zXS7KU%6*@WnN2q?XQiE#ukV4w5JHbIbU-IZL(g_9$>58jNcxWL;B?z9_^mQ;e}vNZc&p*Jf|GjQLtietf_(=Dy5*W|3vgV+Alf8tjh-^IVg4O);+};+HArwMyb<iqS5q=l22ml~2Z6!hsTlr1n>iS;kF^Rg`|4{;_4eXHPeOp95#2!GUNnuBDK5O)>hS5Wh?@#!4Y^vxMJ!WVdC^*E)UQCd-)n(zNs%%b3UN__5{DV1G22=bEf*ig_&&zf3W&RT4K-yz-Ub{BvRt$OkGc6yj0$yyt)RxEc{Bd6xMfSB^x)zbtt*>DAxfG{c9?FzO5t{e~EA3lKXEG5Q!F{tEHh$M;0UTxZIc+ah9aTkd}zjflCA*qfQ*Bs0uoPV^gMo;zZvA?7te{58Z7`fs+p8+yyVTjWX=KQAHgm_J13+<%`hCR3S;qiphhd#*@tua6Crr!x2cc1rrSy+<DLLisRxD#Pi37kbMTPgDw%k07HM$xuG7r5de8`Dn9hWHaTX@2ZjS(pUY|^}8l19qNHl=Cs4B)~f~TopY{ARG!NCUO20KT&|6}aQYRA$`|$hO3x8$*}xTv%14lqjASSu*OHCaqI|SjHnN%WX>EvVW>Ui(InZsR^mn<2QqIQd8vnoxNfNDxvG;Y7+a0eX&%5-EpX#C8(%Sge^^??V%t(2jKix0VLu-cP>R%Sf?4f^?M0z5~D@0z=<wbm2V`z`6+au!BdP9Fz-Ct21QW=b=s>f4QlXHh=t5aWpL^)~qhRM@<+r6@*`bJD0wfUavVS4DcwDzjkzo1kboT83vc-Ak{Lu-=bI$zIHf2yMTMS3F0OGIAM<wbm2!)TAJ+au!BdPaX`-Ct3iQyE&%7yikX`z7y_<|bAOh-zNnSNVS>T1xW3HBIIC$BqPO-HP-atoEVwbe}Z2fl^PQbt}@t*J$(Vbos9(i3+V}k)8<h3Xu=hxrmSUsKlO7os0PBuS)z4)wYOFYZ&7h`rV?ny5i0p_4UE~lyUoew-U(@DkiJVdfcVHIpVWJv~ERuuJt&juouRtudFW!(7F}rp*76$L05sA*8I_cNKXWLiO7fQT*OCvWMWUK&P9A$&*-nL`zzv$>bc#E*>a_g&r0LBe}9nH@X87WnoQ^KpAJy@&Q1LCq$<tii~aV7)v!p<ubtnQuC7dzzx%97*uEgr!`E0>a=QHJ@y-&hZIPY`@(Pg;)x3z0_Nc_3P|b_@=&wrr4b{AekMUGVJVW(7b=G(_;p#pmaab9J)~!f>QEF>-SwT~EdVWKN*04y=TTS0r2IZuwFV#y>Xbp?>@HOu4JwuHx-&~>fEYcG}ULx|LniuiW9+}t^s(BF~{gsKop*k1wMfJS=!&Lc|j7OxOuWeJ7re$gTMQdMDXg$+yY2B88$S=oFs4cH6w^E^c=(e<OJC6K9%9}S#&gq<`i1hGvo^LWuo;YhzSZ#~+M37gAyrRpC__WT^9#ywT#7BQs;%}(tDIephl6a~lo}t>FwRpJt;p-16Z}&c;&>E)OQh8sFTYc|^Dr%K~-%@A|i}cXCeeB@-%1`HetKaTCs)+RPb;`UxR-Iq}m_ln?q$h&BMC2u1Uc^UxWMWUK=0$w;S0?_3YF@;rwN2~!+saMk?o;|n`CAj!UvG13eEh#E+AqGlR$N||bxdmTe6mWn73~YxraUA)H>#{Wvvg;b)-BajwEiEMTT7lcxSL9ATcjs~yh7wdbuQwgJu0y$ROghB{;I@Z!+n9u@Hmoq8txZq#apPQFAY(KE_8;;(|V@zf9xo)KGEW|^29xEm2OMxnQr^R^6g5xr<OXtccMz`mg=F~@^w}?Td2Q2*jlBvEz%P~ULx|LIv4TL9+}t^s(H#se`VsYO#BViJe8sKOl4?2lO9<W?F&>!RR2_l)+&{!GPG`~d;}TANQUxhtroG_u!f8HZdkWeMpUa*MpU0vhSn05FY3EqS5!WNjASH3`Lvdb*lbv1MSM4`tLFIsV)!ZnrSVl3%HyjNRKZtusD-b(P#<3np)tPhg68-trb(99WNK-jHrDv1HBNm*Icy`_fUk9IExuN>`|!1lEymXZHWyz7YzDrjvPt;LV>$TRph@1R$;{P0ouu*CYMdE}Y~X?7V8b^97qo&>NK3(O-~$QDAT0wWAqkS99MW<S3vHo2R6tq*ZikN08SX%O2ULWv&>gBGtqPT)2lR%TNNYkh=mi6y4$?YM1Ny;Wh(j6&wc#EZ1`UulfO;?#MnEH^jUXOILMk*t+63-|(U1<!kT!#+FcvbQ1=1Ff0OP?9F-T*eB}{<H;6>^M2TX+N&>CrLaKlt602!$ai7*r9KpUiOzz_3a0dzpx0ouVLSOQ&;c7aZ?3|7G1NbiPja39<ceUbKsp0ElYgn>v0LLYbl9)=-Ehd_T=51U~)(%~=&9)T^8f;0v0g~#CuNJE+iqhK5CfDEJ=Fa~zQQ;>x;3&z3IkPA+vPRNFR@B&OiItg;%c{m8ukWPbqco9^Xg>)87fdIS=vysk*8Sp9`f%!=1!(4a+-h#zQ7sEn03ddnN(&exe-h~ff4bnBR5>CJ=Sch~StcDNaG;Bb+0oKAN@C9r_x(ObF&*3Y06zQX|5x#+MVJp(D@EDwf^RON1c6btggr8tH(%rBN{sYfK9@0G61DD`;*pGBS?1f+9Pk0IGOYj{00snx4RDlEVH!yY>>0vkoG3++>8q(L`6)3?<u{V*v39myLb~`(U^ccJi<=GwVeWdThJ5Z5TV;>>?2;PG#tQPwe>8EfKs<XQ64AL|3G1Ou8*_TMagwG(JHDqUzo`tWWF>A`cNBTW{2hCV>b^+-H_yJn7%kT`+XW(aWFfY4;^a}g}9@d&&LwXH<gG45?f06zRSHaKPFkpUs{{`(>2UeW5!*?;(iFIYAk(Op9SvPh!D~q%&i)B4oUsefeC0360VFOuJq*Yl3Hh>LbHIde2mDwORoYg~GkJVuJvJ@7FG>+9~qgWbigtQTBz{aq#tO?R4>`pe0Ww8XL3G6PG&7ABaWaGO9o4_VAH&QpVv3xd#wL;p8x!7bjok>U~=3~>?OqPr^nI*AVY&L6;v^{If=CFCJGt$niBb(0_vhGN`vo35ATgrMP?ag|yC2R%jkF-DQ#g?;GY%tQntRGv+*05nnhp~Iu{p<lY0_g}gls(8EVyQ?|*+{mYJ<QUPrnAxP5w?kCBF$tOY%|MccBFPTp7CowKi>9+d?KlXB*OgK(P`hj8xiwsP}kW$iir8OtQ*#UVuk}|m|t5<^c!M+jV`g%5c6w&iN8X;Qc)seuJgj&{Sh&@?OpfYh?x6${Mb`w*l&h;%!z(O%yUQVG{n3Hh`)w-f`6%$a@QHTe&C!XoHJ^yv}fK0%lNj9wWZnxzgxyFt_|^T&G|bT9Eb+vS_)a$6r(Q+@yirrtP~PAOE~kfcPwMRR^2X#Eo1J>z8=q8#ynO{hwh06`=h};*JNE&%xj7GWr}&NlDL`Tm9I>c{wj4<E_1oQYz2?Hr<e3*e(_|hILT8+YTCW5W&F#Mc7A{g(cnNd7}rwBx~3R?QHWor7-OZ7xLLvj_Izs@^R-@i=L5@_`vP&VTgE(AeGVwmV1G22=bEf*ig_&&zf3W&RT4K->~uP%(Jz-tez8?MOStZj)ua#iRkDo7-*(hLkyW>h*RH+Y-}$SW(cnNd7}pArbxkq)q7c7KF~&+EakGRsNVi$We69YE{3%<-+?T3<|Hm@sv6|rjAsXzD2J>8#bxkp^CE}MU=Cw-VW{NkguOZd-mQNltH`NlByfM<?&njESM~gk}pV6X*Wt^G$Yf`-hwW7g?qQSUUfUIkZ(HDjIWr{IY3W=K~{7%i%mN8%J{)xpbWA4ir9siN7Vjimv>#s(GlcK>q*JNE&%xj7GWr}&NlDL`T>6KeZ-czNM%X~Z6627?R4(Ybr%3H>>y+{0iT&-joKQ|}Vf1qxaXmB7JjB5qRx~3R?QHWor7-OZ7xLLyO{kK`he69b){Uck&+?V3+E0!^j)q)={MuYv)V4iETt|{iVMEo+vyjDrvOmWkp<)!|$uE`gMud{^Ts(9Hi&x%R5iZ5n7=C9MSgk}6w+}WfHy-P)d4@HA<tpHiq6r(Qz;+HALSSciKmhjsdzgWh6tw$GsXBl%}&i--6GUl=B{MDz?;G}3U&ox=s6!Tglewkukt0ZowxZZ*v{qOv6PJXr6c1t*R=NtZK+W%}B_sm$}uU`MMWo%15n6&bh-=e{XqQSUUfUIkZ(U$=6%M@d*0wivh@NcnSS;l;=iu*pbjJYp6Pkv|_^H@2ZA4G$bqQN}ZWL;CtYl-+}ig~S)xS8S$y$|^7_Wnj*cy+H3cWe8I|KZB#BI3a(dihITIUf<{Z@V9l+kZ5}hs-eQ3=sW>7;Os>I}I`V7$E)%u_S#F5p$g{PdgnEbKCl_|2QJ%KKf%%nc*Ze%wtaU8)BY2Vy7YIH9-6|#B`Qj@0nimhkKro+W+{Qa&&jT_SwKS4~AU}@j{yl@?Gs?<(Esug~?Ny{EaK62OHigzZ~lhlQ)>r%X~&p<s--_MlzI-YpF(SQ9jzN8re+w=(}p<`|Gw$b#=i(Wy5WM1Vl2MPx@3AXIJ-s)ZieMr!q0`zO6`W$Evqa$njJ8qP|~|3e?;0*yyM75o9DI8Oq1CWTUkxA8nS6Y^Ho#8?*-A`z=duk+DXq*Jwys{q&wcL&KhXnn<)B+FffTm#_c3wCKgEsz?v5jr@TROTRx<My?UtSrzHw>-71zoZKd+zp%!ro(S>^kymti5uer=+N0|Bi1@VL&|g*eSH!3FhVfMOcuEhZsC}9)Q`W@3E{W=s%I6+(s3j^ES063+mqcq%q=(jC%KQ_`2fdTj$@W-Tq({5f8e_?0Dym_sCxX00<Rx8R#7BE%Vo#`^MSS#ECjN$MTf`UDbBn8~8g6m*tVHYf2bdx+cw~ljRem>#%F|kH(7nCfaqvZ{${k-QqHSrdj!Sz}Ql76YpMB1wiu4q%=e$|9<gNF1Q$>0r$SXu%(d9*aTH9!ks@o&t)7nOVRo!2Vr%K{!C`0Rc=RYmga^0QEm`s;UYnbYx@(;;BC|{LarEIu3P^R0`dZv2%?aEMIow!@U|I4&)sUEs5U#I`c{fbmCJFK=vdLqb6L_SpKB0kz95qm;4Px<JtO#GFJzoD9^GL%p2TvY$nJ4}{8KRHEeQ|$#mt>FP_h4+{&@83qEwYufVV0qm6+vNXTX`3Y4mey+d+bhV=x9Ka_uGA?Y(nD)F_<bVd_enscCxW~}<W*f>#HY25_Ncl&B0l=75`PWrUnGO^RP}h$8m8MyGsmf{+<0Y1^~WSCFRK4Ft=g#b4*#Hh+5DHVZE4*;vgaG6+~0SqKi01kR{wO{qV?RjR+9R_*5<NEPXu|1$V<Ash)?Sr?U8kRMD<T)&|g{im&(xErZTjipV%`|{%G|IDf4)DKdoUZv!eJ+4Zoz+QWl@@B+n>cM*j1=jS{U}k)E}y&PYFf*-FkXR#K*QE7HT)X?nh^+_!3NnbxyNPXu{|$cO4&#7BEnVo#{fMSS#ECH{u$T*Rj}jPX?Uc+y%u>B&^5H(ac2|L#6TBu{H~=c4xNikC{M-Mc?8)I)1^YpGw9V{5ypN54NN)I)2S<NWM&wd?ASgnA;#OGIAM<wbm2&uEXV+au!BdPaX`-Cq%3RL={#43>Kjo-18meLieop!XG0`DT~v$^Ex~Cq0<lK&CY;(sQ4Gr!*j;vfO%;B-0ue>EY}6eyk_&IM+$0wJp*UL0%#9p_&)*(H@o96RLR;AN^H{zoD8J@#%f9w4Q0LzIADWdTGWgW#hIcib($58g6yzsu=ayqCXW{w<0~~X1=KGA75Xcv%jTE>sF+PuQQ^`UFwm3vP$b&q$h&BMC3ztF5;s-GO;IA=OR9>ZS+^x{T1;=^_;Z`e^)Nfll~4|3aeqdztC+Pe|(4Be9@=U$Bi9fH7wH8`rlR3niM8~wWC*94U6<>_nI9pA$Qt2D6F<cdLqaxL_SpWB0k!q5_>{5FXE%WD)Bc|^CCX|KBu)!Yqgv+Uu`+(0j1YZD*_^UTDQ&q>Zl&5c!%1*?>t4Mht{q8?{mt>&{KV}@nJ=z$4dQEJyz-;<t1HS#HV$R_Q<+DB0jBc^jFsX74b#&-1604@?Gb*N~b(mBwE80s!q^kj@q9J+ZV1KD=&Xht+f0=PW`YN7U@Yiy<GaVX1tv4NDQlCk)ERUeDeM#^6nkUvPe$^d4<S_YF@-gdsJdisOCj{^j9VRhH75K$9SqFp4X4(&!?)DKYC7?_Q~=v8PUG5f4WUA)4qwi|GS4JTDMdW-FDTvfYNfsVD*&-2PIm!B0aQ*Ij+`YoO*Q6Tarjm1bK<bhw5C!M|)&qPpHmCeDqf){)XzD@@Wl=_67PZ9a_V5TPj2AmdaBZTB}sP=re+hYCD3AVkATPv{sAQtP-15BbzCo)*+P<)hd;tbw%Z=46P+9U(|P_+KV6~8OcySt)(J1%fx2c$YxPp0W^oZ@YNU^;;TN?#aAt;j;|_E318)*EWS!Z349gPbls&%*41PxX`hzR_zg8qS^nISm|xgsd|hEz@%0z`7hf?k#qm`trVPGrkEw{S$}!dORWqgzzAkH$|1vI9M*Fmy#=oj@Dk5S~96Z4AZG+pO6tqIx3S3YU%7BDa0w2UeIcS5F-)DC_RDkwK+e2HZ2zNkdq@AH7REDb19cg#y3e}({^g-GO?uHsr2L>V?2)&^;#K91x{64#S&;W)Z9R~M6JT!t7r2Ia+JD~}rB29&n&=i_M22y^XT>`X#@!CCt<DezPfCH%mvcL{rn1pl^OaM2uhG|IoeRhc;!z`ryK0AJ&<7}k-KD&0%0p=s+_t|xVF0dFWzt654^neveSHM!}34LJ=QhuKuzt3?UQhuKuzt8buqz}V`FbIajW~7^8y>_4Dqe%IEcB3E-o<RBpJg(j6xD)A4*rwg*xEm?I&n_FBkcX7tXO|0;;RU2Gz%$x?jxQnQ_u29L92KPeK0AJ&<6)%yK0AJ&<7-IyeRljl$2XDk`|Os%eee#_ceHy2?}rmePrxx)1rNZ7NI!)4U@dHbPm%Kb>>h$ma0V&A&yL^c_$5+)pWS1y70x2%_t`xO+u?hp{64!K@DyA?dI8SE(~tvuk?w_`U?1#<-;w?f7q$BwuOa34+41`v|3%90v*Y(UG8Vx1-`ahS#o4RC@3Z6gIhIDs@3VUwjzc-5<yaZU?{ln#v=Y0Wy$`3LDpG!*-A8a5Y9i(L+41`v>mseosxy9{V;oX`pB=x?u_4liES{Z%AD{_RexKcs@G~SJ<@ed~`y4O9fAHOc{Q_6Oi`2{PjNj+j8fk0hX8b-!8L7+?*<S#x4bnEu&-i_g9gucl?HIq$u?x~JtP_i6WmylTJy<u!?{n;nv@h$)_<fE8kPcwI7{AYP2+|>}KdZs&vEfLEvq6mC=a_;th26^<utqEmX&M{F_<fEUNHf?N#_w~?M4HLQGJc<<6RDGBGaK`;$w()&3CzV>vFS*svx&^dBvyd5fK6pdESb$gI)}|<ZCQJ^0O<lYk9B07*%G8n*do@Ib!RJ(u3*d9-K-B=gLDmB$$GPa>_MatvQ?}f8_YH!<#!+7!-la<NH?*E*ibftZ9%$)J;Fw^RJIlAR`wVh&C=O+q}$n(Y#bZUo<jN*+sU$+gXJO3V|!Q*o5Wr~`U2a>^4T<Y5a~hoJe$I1F%_xGUSu=aY<3vwVRnekW%Jn)q(|7RY$03B-a`5odxI@y%h_?H$JtSKAG@D@fb;|QE?dpku~SG-vG>^n>|u5q>1p;MThBJLFOYu0K4BZ#qwGthU$W2G<Ln9cEz)n<H*6c*!OkN+&(5)3Y&ZKE>Cfy(_B6|7&mw)6{fF&k``K?ue`6QfbL=Jd2hu;-uj~L**fpfr*zYXBUS@wI{hR&CUSY2>h<OFy|FGBDo2*#O>-c6dZ?j{p1kw^Qx5d1}POw;{u`wlM-eVuJa!AX?l#V&cK4le<R){GZ^D#Ta?m&7+O!=74*;lLz(kd~PV!mc)S#_k<W2(k{$G&H^kk*Q+5%UAP!0IBc8&f;xC-w}x#D2ney_l8DE(f0O^r+mn{X9v8J119HIPTKEqY!V3?V;fZn${QM_x_!4im#<^4(Sx(){i}{=(d^R--c}$VqNDQbKVqU-L~<!pB7@>$4FR@71t@kdd#_PBK&u$w#t<zL*=7St+a%{PU)}VL;a>$!pqN2((umXDVA`vqxVIHXD{CzTFVN)<l7PQB^vy>^GQosU#si>7cF7kmk+MKW(n)DvWoRw@U^U9J=fe9EBHi>p-Shk{**QZ##q9Q+~YJ{<NdCd@Ed#PYIsk*R+ezBqpPFBJ-^%(TFVN)I{wL!FVSG{>iL$izSbWl)>y*2FU?0hYzgbJvWoRw@U^U9J=fe9E4b0M(Ms&822#GdI2<SBY54NxiDCGchVwOCx!mY5e6jy3L;UX94WVr*?)mqY&{{^g?~@OOVSU@<<DLw|`da?sPlsXMwxU?~g>M^%gTC{%D5gEA{i%`i<qfTsls%s+uhp6%4>@C3iuS2r-(Fr$Jl|TmSgNN=<*5w+ukqvcl$XxTP^r8~X7}3_)ZZU}Copeu?=Tt4Ki6TjI^c!gfiX?agsnySP0tsoacw_7RMh4UQ%9?fcU(O5&X6;bNM=dfit4+~Ck0$dePk+M)aD~AP6zrdoF!9vk<16Ig1lkU9m?!+y~1QDzhLet`ODFFDvpBFVQW!7%>|8l@7}3$ql)uduUmaCEMM!>3S^~Vxi(YvcPlIZEG_l#%<iv>a!2*>ZE{jS^mlrAmP&IZ(j$`J_-h$;bKdLzaX<76%dd#vA|_Q$PVMi{YkN+iITi6~9xwb+puTY`N5i{%j8b2C;c(#Eiti**-l_au%VX7xu9nLASNnwJRHTRImt)tqA<DeiX|hO<NdD_LO3U9@>8_O9+B>XHMEq^VN6KgSR#2{V_*SB|A>xbbf#!Ouk|u9`|FOWryUr+7rudlxdEqz3Zm6H;Ln_Fdy8IBRkkVTf=_y(d7yl}z^!|LND$*m8r*(qzsxB|$(>g(WRNWpCAAMAHA4T=!9Wz>8vE=<E@9SqIkvz@&Dy--8t)KFrxh=eYs2;w}*du5CAE$}yhw2f@(>g(US(g{_X`P@wvTl!vFRBNcYs#lNEm{wHPK)N9@I!f|nC45AJ5i2k3`Ox5#hJ#9Vj3TcX&mZXdfr;mXRMXho~+go?t<b-`7_X(LQ5!xls^NlIoKf<X)KfkC%B;;(sED+ypRYLkn(4swE_t$BdrV-!4K`A8q#WT2eg4sP!nlQs0!_&Gt@>}8)|6h59=YV2X&w)^oDq(@el`n;7*7^8Uqcq^M}olHiJgmbJAKMZ2?WR^M^L1Hb~H(ljcI|0*7|~(1+9q9vBDNAS0EbHDp3Av_;w$k{|~rK}Vz=AsHsZROo`V3v_^KFax?H<>zB(!EES-v=`hBb7259M%ozq!hBc+Ly+?Gu?t}d3`feJd$t&sLJCrTK6V)_hcu-8xo0cjKFC1I&&RHW)sTfW3&z4KSOa-T^I$yO4-dd(q?2I+tc3?*3eqW%59{C|n2B^IOo#Qb0p=i`0|oFfEP#PX2f{qKb!-{=*z(ZO_6onp<3!KLE#a{z2WhzT)CHEXt5|`C2hK{jggaeb8x`KYYFlV6D|lY_XF|S2gJWMiVhQVOt=aI6C9M0h_vEjZupTR`SkDDt%L>+W&3&<gFAeIT{eCp5zC(!LSTR_`8Do|Uak)+f8a}mqvJekBwbm5><J=a~DZ<|$-xspY3^z=CTZna?-<<zWh;`dWO#5Akbsr;PJyu+&2<tKDwux|=g`?%TorS-#ZDYpD8P9Z=%0Bj-vP*6(ciLUXUushumGZe<&D~`J-+WS_Qkf!rRp(QTdQ@ExuB(!DL;PXsE!9+|xvUIZBvG08jn6AT7au53>hiusW%y^0B&5oj4ZoMDOcB1M^C?C>vaW|>8WT}`UTl;jfB9Q#U~t(zO7dR?@}Iq079NX|nB2dxnf%Iy%Yk>-v{psi(zt2Q&z^m!^2NFtsz^@+d6meky1a-_V~+Nyx;>)2P#N@B)%_LaD``rO+H>dDr2W12NK~HYsLz85s>|#0=LM2vs)uf?{Vkpv<NUv^DSW=TQLd?;2=Wq<mvwm&pVkA~BkT5v>V(SBdZ72)iE4(*&|DX-6Ft`=`3N#9l`-Pe{1&m<Fz-}Glxr$Oa}+7RM)DD4WGZ9Cr+F!2vthnE<B{iRe5K-%DL*zHjIV)sJlzkEuY2OF8%lJ>&-tf=HGWV0cMAT$GajMW#V(-+z8M~`$74@W8{aW_gx(N)i#UAWrd@kb3TY|q3;45}%OEX-y+i``3+0gV=OpvzDwjvfuixO$Rj!D%BK8Z3*dJ6vS_!)c36I4qYyHC=+H;kwBCU!YNeAp%04ZQ6(M9VQy5PGe9;5fd?w~uq>);W3Z|n~4#&>-@Lhp|qOJ969#-n!LD-6JQGdw~ciXF=!e7D47_u<&F4AGvGJPiAW)=2qtl1Je2dJ@tk>>kqac)bnMHrPF+<MDb&q#d!R8Hc?=Eu^)ur)mAz(-N7T8RBcHn<X-jGsN%xJ6|GmJwv=HwudS1oLpTZb4EkFa@l1+nO8={!8w{C)^!HwafVp8EjZUR#JZ1>upX=6oY4^LF%Qlw4e=%44vEaXO!4gHn<X+|GsVr0-Y1dyohe>^c2ZRM>y-WynLnE1ze}~1$b8c>4$i+!vA$MtzGjMbUxM>HQ>@3zD%NumoIjdkJ=ekcrYXKU{z-|<yi9S=FE>eKzGjMR9bGMv`JE|#W6#{Ea3l9PiOe5O@rfEkB{JW%jDzzpQ>?EQoUfT;-Iw6}&J^phvWoRw1m};YSkHBEzG;ek{=G#a=Sf2N-Lo4ca*id0FZN$0k#jN<Id5Z#8ztmP<eblSd~LKu&Jo>!gXc`H<KVWzb1WgOuN6EeBa!nqhFJF{c+Mw;b>D;Mh$N#q;JFT?Win@xjpk*$->x8&*_>=Nn=3NolZ|G4MP`Mn(X5d2?N5zVjb@IN|5~jXs?qGSVD2cD%ts7mK42A8GMiJ4W^+Yme5%omugI)WHkuVueut@}WuuuR<<nfWh)I>nT+A?E7yc-a^*P1HU(3j3?k1DDo1vZvb3H>n5$1*}nHz@kDB{yR_U@gk>N6%0pXPCWT7jz1EVdONsgk*vVcx0y*Kd?o$=ppPb2mdh5$1Y^dLqmXWimGm)q{w?tH&sr%q2s$A>xbbf#zK_(-GAVo#Tk~M40Ot>WMHnRLR^hG#e7}X>HJ%k%&)gfX<I--s${EBv12B=Sm_y5$1Y^dLqmXWimGm&8kFvS|@adCE|<f;np1Re{T-h2z%z@NUhERJ=il>K>EKq2fPa@zvIK|954}SB6j&>Aq%_su{S*joCgD;G1C9W955ScHjKOJIp6@K17I%PI<|~_Y&oy{GZLA3nd056wn=2ZW{NvqT`Q6Kohfz|D~Jk@Jvm4s^G8#BXlQ$h%r`CL;QY%J>uUw)Yo=KDB{;t`#d@r)Vm%kZ`J*Y;a~+&-n&R(|?~};v%n<+M+$NEEoFN`^YOO@(dWN`Mrvg*_#)`obnKK&VOM^N{WL_B&2j^&pSl1bx#~EVXw%}aP5bHih!g{QNb4Ej~$2>T%G{m>&fVbv=x8{Ji=76{6fQ2@1xVyA+>hZnul;pOm2;Wn?sfKHB>?g!+9V0Yc!aH1uzxZyYDLy%2S4gJ_KYP!?kZopoYuV;Ptm|ZZYYMS$TeYecgjn}664qnIb&9Yab8edm@BgJI;vD&@uSQtH#gC5B@SWSTEa8_{EY|RY8zx!8rPH@Wg_A2hA6m-_PXGIG$d_pF@jrW6!unc$-0du3-Is6Lw6=uxSXsq-F8Eqju%2t~ixvFL+8kxW`Wo`MpAs$M5_=0YT=nj@mazAy<r?nUu#+Xctkfe>;lp)ygx0cx$L`u2@+BI4HQ8nf>ucTpWn)WN_oYf~14~$sl~t_gg0E!->$&E>SiwnoGn4~$7f4?w_7B4j+k6dgtUWXg-#!064fn4)A`DNQu)z?oKC(5mEyWEF?F_ADgmXIf2*die&yMOChV`|sWwZ^$x@|?V?hD_RV%>MX7R7Wva`ebpIq|Vdfd_jYRW5x$L+-t~?hP}YF=K1V2fDuLkNv8PO6B=yffl`_0o$gjB6*Qa@zd4SVf%Yau`4<X`6GT#S4-YjTzc}wx58#sl)vD|0=3bxV@XAAzVoRJb^f3a0{aHMEs10XG^?hT96DR6meO9P@<r!R=aXJgT9wI`sk}&L!o*5)(#CyCpsf@pL-~DQ9Vs6=xIj5E`n9mND4*tH)Yy^osj~BxKkB`qi1JnE>sj(oRaEWVX>6@>a`TlZlxO2xsWcZNJw<c$SJmH?MX!!fMS3F0tGYbRqll08sJcBgry@T3sOmn_oYLIgdpbkycy^xu{awc;kvz>~({a_*Kb!TEepEZjB0XAv*M5m~YRe>9R1Z{-NS@XJ%FDXEh)?SQ?U8kRM0`;_(7ez4Ctd#K#B2WF2fm|F8SGtU-oqBHpPt>T%9Z91lj0xkq>A+LZHC{zLVCa2Bw_tfJrU$pBCqQ5B0jAXv`5wL5%Fm~@LpZ__vFRVs=Hoe<#53<Vf|3~3H$F*-(IpxDdr5%yGT#bdf2>WxAOSO99g6%g1k)Ruh)-&kM_vKo=}~L_@a8Cxu$%YQ&ByL@=o(eG0hjnqI`++LS;lT7sZxh8Y_xv9Q0XLNr=Ulcvi(fy*{gojX0}H0GoCtDt}^_=$^IKAVX!Od{&hNZJ`=cKC4QGj!+XRpH+2$E>IgOpH+2*?obbDJ?*;FUJ#Ge>a6NsNC7)iJ2V&Gv&Lst5>g3T!Fb4nc1YWSA11(L=!CQrw1Iq>0-cd|hW0QWW<n37J)j#Dz#Qm}v^Vs$e9zhlq$6Oc<yloO(p<>YW>u4rPJ$e5Ry7srRG6sEs%9Xa0n@Zu)oi4*VOH2ZYqyRqBOhDFzCT#I|LE6OhFHSIU&+>R*5V9H_-xEl4WF4l!4m%B(x#~J;mZ3$Ygxg{@`E8?qQO-@>t+e-Yi+11S;D$6%^G+tVLet>v7QUQmKCh$n)_k}C%-#H`~6tw93;der{`$6($&#I{9ePQ8lH0@ONcMMx5*S&Jg_&UQ-tGhKNzyj3?Jy;MTm8s(xTQvtlRd^8mAEJK1RZNthi1Q)??0X6XBj+$H;x0*;4J81IqV<rps@%ZL9s>e(`TDS^DKssb2k7VKV%)V`UVn;{Nd}l_|nkbw0(YN7eOEjO(iUx|w4#)Mp>>AQfzXQKI}8U$3Wnu1%1hc~X+84FBxjV#}nKBPYpJrU+lw`4pobS=U1`jRW=ls3%)ab+r$?wfDKOSkZIcG$wDo+C-kwbYEbTS5`%OXxup7S^eukdiE?;q$h&BO5{~tUc{&IM|)J=9uc4Bg3cpoF1{L`t+x31YSPS;&q*SAnxoaHo2cjCd(6M3zbuRN1by_QkFqG&R8ItXnaIn!yogWh0qv1>dqjLuJ<$0G&AUj3=DKK|=(!fjN03pej1iyax`@pxvDt7AMe`++p*f0_UnBVlGBTAh;?o=zu~{ZI|5xr=tFGO%R$Y5Ou(f;E60nQ73*V*j7~O&WK?|)%xS4y_c;~>7vaoyBYFNH!tvS->!h6>2mhV~XfV4xAd)A)4=b%JpXNLIXgk2Ju#~I=;zFR4gxt<|z>lk5*@2TBXB6CJVyy5QB5}8*<#KAe5A=Y&U=W&Kuw=Fo=GsL=&k+2@C;GEGA>oE_`D-Ch_--jhK^D@QB6`q&Ke9aV>PTwMt`JE|#X~p8GaPgyKBr<<A#ruEhDUtc6WgMJ;nPPpd;C#&#>%Ii%ccxg6l~t_gA~=6E#d@xT^G#DccGq5s%)CtT;W|4cGG8;r%St^Wk@=k|_WrayDqLc3fkftyrudn)ITD#~TE@ZomnqiQ3eML|vF=N7erJmHSXsq-E`sw%Q>^DYINvnI4G-;<$a#_wUVUV%M9#5<@WcrlByvthBIj)kvBNfBBIkTUI4N(2M9vZ2fP?2uLRjB6c#b86^|gZMWF&Il#t`ei1kd?|u<m>C9Fb%+2ORNpx=dzjveCS(`0460na#;`HYb?z$#ljim=&sYu4KeNdSt9hXH{f&sghZkYBam-`|3!Q%+w5JCQPiPlG&VUG@C0j$5D-Dd_`tMveB%N^6z{qLpGW@Qa;TEoxjld)AROJp3YxrE<}2)%mE|i)M$=F^C;rec@52}h)?rKXEZc-bp9fer+K9F7m=O_b3H>n5$1+6nHz@YH6lK(2Rg42@kRA;YYup84tQ%0`2W8-AiZbpX6Ar>v4@XA`rnuX>i4YO>>Th;q<2D}|L5j_w~j3%A6qKR4@zX_Wr`11-Y1dynkoL`(k6+_?@aO8n59wS;;&>&Wd3N1W8WVvk@==&9GridVtuXPe9aW=z69rYrdW@aRjlVCIDa(7dai@>O;a3yd*R=23(n3Aam53BB{GjQ#FyUNB$2tEA%3snQd2x~dX7ZqjD|S*-60a0S4PCaIhrBXbq42ghFG^PIM*}8x{r~t9;@J-(Gcq~56&wM@vS-FtvTSWIpD21;H^1eq0RFjnC;)16Of<VG(#2Pb#0S0Tw&u}A^zsQB}p7NsIedtK4gYbXMpH8#AsW9*clOLJe@1Vy3W5UjTK_uwvTG2MZ!sDSdUduzaiFR9<<XCdw)LYueV^AT=DW6OSs;eB^o~8c7r86JoBw2j!&H1XcZrd2IE=*vaTscUjoE0%Q$(*a!XiWD}B&HOIY`%;JLY0aZ)r`&qZ)uQ>^DY=$9#8z2Ou81piX`o%&lW;nLkVYk0!CZI*D|R_BvA{^Q$SR`H=|Fs>CK>zZQpB|!YLj1SLWX9??T)h)lu64rfLcX*jqoD>b#a}iwE6zjPT`elmu%=*TEpl%0wdylP_@a`o~YPjWqr!3)8Cod;)yzuH?tN2hf7}pArbxkq)5+HtA#@9+bYzgaY<^OZPC9L~WXUKh4aZ)r`&qZ)uQ>^DY=$9$35&Mk)N|Vo|85xgS!ZZ5M)o{Hpwp+pz-&c}2ezN&)tN2hf7}pArbxkq)5+HtA##zT6vV`@ujty9C3G2ReD7C^WPKpNWxd^UniuGIv{W8UmO^x*rUD;MDAOD~be;#-{iR1BW)(i1FV=HU8%c_SX;X`H^bsi%64KdmlAa+K?1Do70#JbKu_TMMOx^1;zS{?}}nPELvLH&kUk9p8eLrmwzQzs<K<E5(d#g;EBnR}+m2k!4F6`gTsKKz1|oZU{|yRfuM<@skb=k=7&p0A>c<Ri!^RK|#pYpHZCVzWwYR*h_~@$eA!uZ-17UiZ_INT%wE@06MotEe4MC&*O3=v-b&ZKkeiBFR)ff{bJ&L;1LtY_t~T(_GM)mt8$Vb~*b?8)khTmaoS*6v#DS8s#q<|KBT=lymRjC2jw(lPc1qozKgEU3&Ddabfuq>4_k(5P4OX7x8Hx(H>Q|N5rRjM1NJ?Uz)p?8&cKP6P3WuX<tbqd78&LmCLF=Hdyht>M4u#XxA!qTc~7|o-B*%f$E7MFA;fJmlyGAJ)k|ZZjXpBst20uo^40VCyP(@zq<Bwh02urqd-3RK!G;vr@3x*wSruu!^i&7ZF;LBJ$#!7FEOd<&ojenL!>8yyh`L%U0%eewSo4ix;-L3tpW5`)%~TpKJn;i_0zG34wX3fxg?UOx!$<0qPlL+J%M-Y_mM?<w7=!qU}2zhUO`xGi1b8|mx;Wr%ZvE5Hqahfw@1Vm)dS7-=7%%nPR~9aSo6*?W!aDdS^9TXpr|~}bzoRcSx$d8VE?PDD$-N59>!eV7r3KTfhy7yL0%>DsxB|$)7n6LRNWpCAN^H{zoB}dxejz0tG>~>P9P=YxFnLNx%U2AQ?<SRQtM}rbdyDT_%<Jvxtg^9tAeoF5b22^FB5rLmlyGAZJ<4}ZjXpBs)zBFM#)R|KB_dH^;B5iS6-efAL?|kmVdhKS2L^2JI<a~w!PXsEbk&cv<9?i2tW0Yvbf4HRir0^yh`Llbt2-UJu0y$R3{=n`l}LuL$yJ3T_SJ1+9~bdz_gLiNg{cg>xze(sQrGg7FgLOSr+Nx+pMw2C%yewL0D~w^hA)CiM*`Ki}<uQ&>mU0N5mJ^13hO>Yk<m!omVG$r}8w{BKZh1DwQ$f)4Uh4StT~BMmCG`PGxA0BIVaeK7x!)WsLYVM@4Kl%-zjg%XAisvlx5<`y2j-t8fKhm*E$D{R}_i>l{j)g&6JAD;obt{P*AZ|FdC#!?y{vfKuB1PKD3zE{&952ju`4l+*5a5<k29zxg}_`Zs)AB5esxwd<g4NcCrTyOFxV8S&ZO?U3^8p!l=9J0a!QLGfpIcSg#ugW}Kb?tzqF2gRS=-5cqR&qG)mx(;eF+y}#v^6Q|M!zvholwSvRKdgl`r2IOl2jL;eK+3O!dKflCHd1~a)Fbd1<RRtH?%o1V!epfU+1*dT4w!<JKf8M;JOwk6@@IEH4SQh@QvU4jXJHWxM9Qy&dL9nKGNj930lWw*tVFsJmcSu646Bi@h86HC9DxUrJ^*Xr4R{OIBV7;c;3&Kcn~-jT4R8$JhsTjV4jbV;_z1Qk-3E`shwuq(N4g!h!l&>V>_)m9cEK6=680h82YcWfcmWn7T?o&>w{RX_Li!Rs2j9a5P>?Ec0Dgd<;ANyQLje8*7vVLeufZ#D34Vn)k-iD9!*B2hyo2-|cpH9)Yw!Wm58ycb3ID(;q^IBn{00BQ$4EbhlfYOp_Bqne;WXUFO0chxeg$7ZN%kG=N4g)r)>?-N{@7$zTbnrwv9d8Xx!L;2xZNkQ$)9{#V2UrkG&>^ZI^P^NCnDyy-McX|Zt!{Okh}<QdbD(C-AGusUxc|%Jq|{=-#3jk+dR{zSjLY`D3g3BcA8~e(N;FOXM<T$;r;99SjK#<f1j9V8FOFSX3e*ZJCrUR+SUqwuWPB0ZC0`FyA{mW(qn6e-{|Jme3`w_I$qtdO!C=hrd!4t&z4E<dt_Er__@w=EMvabk0<6@#@v@W>GLe(UIR*pwzYz%yiqD-n^mm)ZUytT^w^r=pJ&LLFMCE6M8xaH$0oObEHWOvEH=4ZgW0CI*W$>S>umjLWXx?_cr`NaTJE~M2rvFm>Cn27ux`HybDeq|jPL;XOWOY85~=AgebpdVIHu=8sZ7=4e@PcQyX0bj#)Qc{jxz3#hZUX|jZQ`utR-8KAvPPyC`6B1R8P<zmDpodMis23n#kM`=T(hPDATi6NyA$W)3L&_DCSgtS(6h=+tPly!JyKrDE?nIJfZx(GehHBke3DWvM4Xa9$6$$b3x^azp^M_R3@lj<@!ar3)-&|`y<J#0(n)GQ<@_xFUn)ts$<pWH9^`@_lOe23df>6Quzaj=RUnn+Ve=BBFbYr%DCFTTX@~Axx6fpmqd9a_DCXmnj<Pt{FOv`q%uMM3fC{nW6*wu*dIw=704^1JklIdc~KtqzF9jbFUTF05#`H*j3ih~vLZv{Y#?(({0;26A?6lj6v0}GNTv>U*~Rfy3VZo7*uz)ES7q$lt6{fZ2VccCentFu8GP5lu6Y@Dyo<5hoQtml?3ia@2R#X2dH7ile!}@P@ZWQ_`+DkPM_){Pt_ol`-xx|FEvY?6<t`|Vl%G#%h8=x5r2OxF^XI6PN6Md_;sg&=LRv|?)2cO8MOqc^(9SbdM_L`KU~k_JY9r<66WT&OU`QF%f{xG?8X|27aoElGgr-QFYEMn+0|`hIpb2*K1Hq2eu01tnFu0Jqz=pm3Fz_Mufg5}KQQ$}FheQ|&qahh-G9+O)KMpz|?Er0HEOdhUNb5s;$ig1JJJRmZ8FFDF^hVkndSEv{8TujZ2feVjpALhN4ubwL4ZHiHNQc5b+Bt_2NJqfE*yqoOG^A;ef?fVXNJp9uso421h4DzoLk4#F+0X@P7s%9Z6(Ier5R-mZh)F*i5eNH6AtwE-5R-mZh)F*y#H62%h;{o#nDn-W7<(d#^stsN>0vEl(!*ND!5+{OCOxbrOnO*LnDnrgFzI0}W8HTvnDn!z7<(d#^stsN>0vEl(!*ND!5+{OCOxbrOnO*LnDnrgFzI0}W8HTvnDn!z7<(~^^s_=t`dJ|+{cJ=W>>q`g^s_=t`dJ|+{j3m^el{Z3?H6Iv+Ztj#o>xf!rI0>XB|Vx#dM<_Zuqx>X71B3FBO?pelC8)Pn~h`?qDL*NCuomK?6E4N3f59ZGI(4qkv>Qw{j6d9sXQKsOL|`;$^{<hOQf%nNIz?s7lFJi$`P?grt+eEQF-F8EXo~~3F=pg{u}Zbv|lCmtHk~raw?ElMfs&UqVl3#i}H)d_A=>@WYXsv=C^B=vGR=F+oX)=^Ax(RD8E!5dktCdk3{*UGT3X#q;ECMFR?)q$<y3XdE&1m$}g1(>eu^L!~6#ASBU+Q<W+&ZBFZn#5tSF^k)F#E<xV6+b3tW9IifP6yoh9IoDF1dh`)h7H^kh6j3QV|5y`}0?^+XI)v&v*tUZnMcI;?N;fp`vGX_85{M+&0mGK>eU2YC`w0YRWPQ}*@>~ssTqg{Zn#rWAW{Dkuh@ZVGMy-b_dH{^dm6#LEFu)}SNl=qt@w5NxZ(E80->~Q&Cz~=oXpXj@^=Y!g?yRD>6(Rsgl2X?rAq`cqcv;JhHyx**$P0ed){bnufaO-RH{`Ojb-4$t9>~(p6-4iK)$|>)!`)E(@xLfP52O=Gay)N&s2O}Mfzb?GL9)@(7_H5AB*y(!lJzVRrM<X4Ly{@c1160QM7_GnVgtQa(x}CA7&DDC`EbZB(`AGAz_w9`x?qsBsvG?td9qx3b)3MjR2Rq!ENM~ZNdoOmlvyt*=dZb{7J0IzM>~&MI!(E7UA@;f%*x@ckx)gieOzd#8k!EABTcOJR{@<SeM!qd)iX_6lR=fP(w|<O>wQF+D{2URZe1L3gh;iKju|bIUy!1&#%yo|6b|NC?JM;0???lAhN3yLU=CL9+7~+8|pYW$Y%#uGjeZdmmyS2Oj$CD*3W9|AwcdTWM+XjdpQ;fC+h@F;j)(4kmtC+8qKH{8Z%yU#}^VgO!j}_5lig_-GotE%pS1Tl!xm;hig85n(_f@rwwZE17Rdvgl$BO7N#XJ|pPD}X7bEPd~zSh8&w^_zKcO@XkGUl-&dQ36T1+mi<|1@y1e_Zw2$uG8QX9;gv)WlylKF%`cx%=#?`j#<n8z6d2G1?X&c3Q%3)~se3^R*gRyu&i)xf{5!qGiluMf8|ro(p291zgJC=UlDiCzcNp;w_7|C#64BHzL-qrQTdGB1ZW`WLraw>jsDoLcD5C^@y13oc48<h?vK@{prdPG53*dYlwNQhz*9AUO&3fKU6OE%x0<bgm;vauM}Pb`o}M}u<L7Gza5mC_N*YkI@TX1FOos5=(vcCLiDIcdMF?5QH|^w6rZ8~hwV`A8Zt`~$xNv7vy$_cN3HTtahb{&k&$#6Dld{jJ+hG=%BL};v0{gZ$s^L&NT-e;D-!4H$MZCX%@@5PJ@RQ8`R!xjF{gS&@-)uKSIqb{=BQuQ^^5r7F~5G^=GEAt>e@}Kl^4c*B8hW!UB1Emmz1`LV$@6bb_$EXNDs<OL_U-kksgse>X(WBQ0_#0QNCy{UN1FD-m-U_^xc^!l{cmoJ`3jl319fBJk8Om++&jRQ$4xqo6S^_9+5oF9r6`3KFuBKS9Sd&KH9Gm`$PG<{A?$6;G8vzr^W4IITFct`DLy04?C}P%^et)Bat4Imxz2QcOpF^dDJfx{h^$S_@aE#T>P^*O+I|zlhU8>td}w$nxM&C>$4+lTbiRfvy0138uySZ7kf|==@H4(+#z2z<I~)sepS~m;-md4u|JeMnwLv?Bh;mzJ*LDwbwDUj^HO`-HRVok8@1iGGm=OT%@@i`y1Yn_NS@{q^~<_`5nq%qdf%@ozf^|ih{}s(XpV}=s6>xyq(_u5DkI7fm7(#Z@<n7qv8D1N85-Ln_87(-pcYiuu574;FMbt7S?wB$6516MfS+)FS^Re;d;{!*2Vp(F9)ZpHdJLYx*LK*2ucz^|efSCIKY{<=jPHHGw7WYPzUyk|sqWOS#fXPe+F!CMh3_U%M*B-PW$>M#T@m6!T6mtSvi8*5L~z0#P%U_#ieHma17xK9K8u=A8`>dl2W_-#OX85mL3^kNjkLQxx(Clw-Hr5a=n74t8T3Kg2YNwsXsP}6ngP%c?BLd(a(gcf0tfgY1!)Ql0S_cW8q&1jd8#o;$G|8^hPE&c={U%M4p1MuXm^^7hfdnH7oG5(rCkRy3F##5nvA|M4e2zP0{vki%tAT~W@zWB79d>!b6~LcWZS{oH7&y+6_z7i4hyyGK<-0&A1u}WR?huM?}t^837ugA(h2YYWWz-5PLGFS9pu4e*obr^Y=EgS9kw9d0-Ina6u{$1ABRU_Hq3`@NVmaOm<LN>C(@npBrJjzup8-a*a6F6CG0`E2cCk}um+w%`V8!awU7f3A$<s*h2zJ%2l^biJ-N%@_sAk#`-90E-m<@!5Kn9UoQ8ety9qJ-<f<v2RHcTZ>lESGQw<c|HWAk4FSSb%Vtw5~DWip0w?7ir<G^)_@S>`N0`(TuO8&k5U`x2<*RwUe@>pL>cz*r;8a{QbrzQORrQf5%t=3mn^tG(uM_!9lbYHAsecR!I5tguSTh&0SC9L~y73;C(YgxgQmCb=ukH;n7yUQB>v&T*ie>db_OZfB4M>O1^*APp1Q{4Aa;pA_aqOWBI$22Rc=)PFN`nD(k9AydXwyi5M+7i}%w~F=H^0lnsd57N)IGqiWU#mDqh`ZG|uHnb;8ZE?4qz^QF^x-ri?)%ZFrr37v%aBeH{-f_VA=^Y)mp}W580+gET9huty8V%`9tW;dgz3GmLt9Lce`@)8(zmsDDF@q3kY9PZNz(DAyTa~=J-4)+ylKZ=|A;;PR4UIu`*`s-|KNrNsz^S9j7nvU__&rz*CIBn#AemV<_ky5so(70pLD)Lf4QhksY=EC6V8O+FHGel$jDU2h)-i!b<<FJ#UqEM2Cbh~y3H6XKXk<|ZEo?RB#L>Xf6qxHZNEspZf~p77*aiv;=knUKc!Ea3|B>ZBFHO5J`{fuAMH_zJ)vAsKKiQ?e+~0>Zg4TRP1??bEnXTT)A-YEBjxTw#_T}Zf&y8jCxX08<U_d=@oDa8zJ4p-PM%Y#vTPgtfI@S$u)`Sny}%r)bj^Jd-FEu#uShlHZ1S?kb;EKb(nE8^agRA}x&307D$)}{ULo?KoQn8pk4o$b<y6E+e^ugdD0eh3S-Hj4H|kvod^qVIStL($#BqymdCI6=Q)H2z2=X$Kmvwm&Uz9I;tp?2zm8UW^FI1l9LL?tSMxioBe43XcHmk&D)yQU1UW#6)qQ|yq`~@<yk&GzjyuYr2ud1ZKj>SH>WU#-k5$vx^A}z^lT)U!w0(Ns#@WrpzpNU=CJnfqNCHR`4@n_<{r)Yf})BcJK!#BSUq*U-akOtayAa^0X3%hOJU$;cs5_{d-v7avNukG5M7l}v{wd+8x_t*S75DBS-y>8L|x<1nS*z4BCj=l%d9@y)~V-MdOX>aUx8*BY_W9>SS1nlSsA{~gmt_}O?A=<qT{BOka{@SViy<Fa3ry@<&{zj~foo;LGIuPDpk3~8bd)@ZhU!`rY_17J-qt8Q{hrMoB?BORN<^6R}?5`&yovhvSFaW#We)yh>o%LYsv+vP*?V;FT&qd1bBN>hz{Q{)C?;eF6{UW4`uqV#Ij=u0Zki}Ymor9F$gMz)GMEXQSjJ=^m`b|TOy`i7<t%ewTLsN{sp`Y~8h8TNrKk3H}u`VC%Hx04AZm@4P#Jc^FupWnCA8m-Sr;|v3XNs|>lSuz)im|8jlm65cV^0?q#-7ek`fF2+J-eUu@1|JaHrPL!V%@f2e`<<#->qUjw!!||6k|^(k^asUV^1fM{?Qa;Pv<B7sVT;uE-H*YouBmArWkv6Kk461vA%7ve>BCqZNdK36zjfQ#d>Um{k18^-q26_L_>_dp`Y}dh8TN8Kj~WyG4_V07<)rM>7xxX_TYZfj~ilLKG<&>Vtw6U-)e|;`y*jJ4#7U!5Z~%^Z}qvi`rKQ6?yWxeR-gO-LZAD807DdDS^', 'farming-empty-v-rack-hay-manger-01': 'c-rk-O^h5z74G~KCvhCdNeCo%Gl3+KnN4?f_20&xmg6|F!LfsFoCMoi_0II}wlX_C>FM=mW33dBED#U{P6%;=aN*(`iWPZxP;x^F7ld*_pqw}a5E2BzjaS_>J2gAi)zwog$A?{Md%x+fdVlrR>-TEx`PS)YZ&VcJ->)jlkL!x^^;0K~U#$4uZje-_FIMJ*b`bkX6j!Dz-&lyFcGOkpVT$^6D`+=^SUvjW3H1V=GN!Oysa7roaW{<GFc?i~mDOsc+W-NTX|0dCmFcq=D{X%f?p02u&#IMn)Jz{B{ru|r;m3=W;I$<7yTpt}wAhK-K|7g=qZXNa2yV23Bv9w$XsO*)J5e`LyGxx;6enSOUTyeEV?j;e;rxQ?!+<lj*l)a|g3;=1<i|~7++xsONNwvI^x^^te=ZgHyx*P=;uk=wuEWr4Ws6>53%Z83Aigc=TE@jFu%$3AC)xqXO~N=(6TcJ00jOw&?PhH@N|I=C)RyHiSy1D^Z>eD$=&#PTqA0GabJ0?)F8i%kH?<ZVfoE~JI5ZQFnt3E@wW8%?(Q*(UBJxkC;zdkt3_=&S8(=0_n?|PF@{=l<M>gJKv;<Zrk=pj-I9gUSN1jrH#ZI!Kb~}C}=z<fAe%MwogxzqqwW3CypgpwK9JTgndl_PWsugu$agO*ar$AXT`LCI^mVmYBy0O+4u-3S4taSve#n+9su7I`Xbz`lr6`PB$pKYe=0_I*n`%Fgy=3YM=O*aJ0y?%C@js?s$h3kN@4fSCXG;1)l6TBXU&EdOVZM32;sS2X>P2E(ZIW<`bRKJld!HYPv`Aq60W#6V(*y-%me&!^MI^1qPO$6(op?OxZd4*dkojF*-7O5rR+MW-SrDoU$)v+J8R6j|r=@&D7+s4e<^ioRgNUM`$An+u}(XXK~PLVN!k(rGne^87uY$3POMay<W(3}r)O>!9~eTxV#8K12)328+pWl?G@gso-_TX*`bR@JMhYE*I6tXfsO>Qvn-yn`UGL#~AU1A7{_4Nw#40E+-lBMrK)p;Kw^Hxo8N=bRre0_kfhy=xcJ^1Qa-uhbUP(z~YV(7w$<SD4H+p|ox!S?^bS8E$tIKM5N%kXT@Y%tY<hN@Y5Umx5{~io^M^J=64)r9~J`ZmP>^;1=M~>mUt6HA^b|t_m$;5(iIZwf9EO%Q^{|(IsU2w)T{oY3uL9j^9m|pwiE*RGVS9)AAv=5gV$NIBi^K8lVUKfiAal@m$4k`kf@a5S*(_t8;#<8&uVE+46Qn(yTD=NAXPBtd2fhX@Ffb&7d8H-BEb~P@$dPI#)UL@}XmgPo1lf`(2;-m5R}kL+&IC(0(-2JDB=Bvk2<4`OhAG>F_hz^b29IJOd7bQ<T=TsoL|agiL)3!F%H{2~f%+NZ(llRUu9HqMrnD2s6^gyBRIbwt`de7HJL^tuNvkKYrzOxHy~jU0n!gXEuI5fE8<njgzFkfhIqt(X8JM4n?gfeinjE&JWINQ^?WMA6<8m<|4PMP3dNK%XBRbTNpcVPqVN~er!uO9UUW}E-|sMWgri>Mm$isac|0TN2jim?UC=#i@<QIH_Kcr=@m9I7i`@`rfFmF0GY%!t?w;%!DEYTKXErQKOEC?vE!IVfg8ud`Go{llq~E-KA7g_g)y=<aIt2%reUTInb|E1Bf~}{mx%jgXR*Mx<rubZt)`@d95;F-ly?FH&OoCbk{z0j_md<JXP1&7_2`8Yr;eUJdg6Gh{rHKK&mTMn=^Tg;9e&s#W6+S|FlhBW31`7ci?B{(s1wWRL?!$*hdM1OohAIVhdP}yI&+Reg!Q`AnrgIS(yI(L>*Jbpjx>ZdlkQ?ewK1X^)2fl6>Jq`$sTI~OdDTV<)zm`kj=XAILN&G4NRwA>imQgV%uqFwR$XQ@BPxTS(G+4%qPhglkVUDs<yDuU8B{t$)vmni5;QZY*My<Vt1dw^gGwoeQA#ztyA{`rDa|IW*{~+iT;>HyB^1LcrJ2>EitDAa3D$C7Swd<{xQnSwf>CL;n>tQ$wR9bV<<yq(mU>ZPi>nq&KEDBvx>20ToL!om3*s}-zoeDhMmv3ar31#9I>}BAC|DAb7m2jjU|LO^vaGb2L>5BOH2}TzDc#PhRole2OD2*EHmf-e)3%W9*rehN+nEHr{|ri7%f_%NwX|x_>RV_;3}jjkh8am}O6APqL)j@JZL(f$GH*I!O*b~ClfBWOe(KP{V+T);2{5)eWHojOctNW%!_4y<%LUC8^_gLAIhHVDHVH{AIe+b~^_RQEOpnX2up{TO%b$)N%HzyETQ?lnwl&hDGMaHi&m2Y$wlPN52&Km*jCHv+rU-6g(29NF&e!>=!NEnTK}RKW1Nb!B>H~2!1os?p6<A={<W$CREyFT&%W+NYU>A*~1{2}Y6C04~*d|a3X(lxMj%nHCWXEwph+}9NyE+g|FAAg~$0Z%h=2+b<5lDna1BoVxB(hEVK+N2#NJ{1*y+k6?Q2$U5_K%5N&6pqz<1)4=4wBhPcg5o{wv;8qz#`PvL;-1%rHd{eg|XC7ItpX?X^Vn@B!ggVagMFAeJGb?YwTEZ9g(cbkSUvGk+s!XwkVcDX?BuW+LEz!wm8og1wt&*P7(=ME)s^ewV9S12+>qKK^zRpHqk&^n`;Z=Ae3w;34>%QXW%m3F3Kp7bu)&8!EExD={GVPJfSy&m2rsr3Jhn>f#V`u*Db@v#BYWOuGyxf+m`exL5a$3a|}wwFbn$@g-x<dGu$#xXWxBVz-8zji3^Yj$J#=ppJEIPLnt(3lsjW0aMns|j)AddYRG1Nv0ZdlB3Y(keQTpoW4ll;3^jHvxqe7iYS<`oih?r2I~HV4<feJV82vInJ!UXR_QlAV!ng!23k;-Z6KPI%Dq)%QX^mcVrhp}jG;D5d3~Fo_N=2c@3?$c!vTZEL8_uUsozoNN*_9+X7PRLR@^7siC%bWCZZ7@bFYr9^<9PxN>{@7OOYz+FhUjb?jZQXgYjm<vMzw_<3Bz5(l9;WdbO9!wZjy7W$)`J-)S78!7A;+*k?DqQ$xL_6623#-H9Flekt0DG!*XTT-EbW|Io~m|k%aBoz%ryG$KW#4T_i&~k_ly|W2tpBZAT__mS)R@4jKrV&{=Ys&MKAaHgnb<%XFnUYa^+3vrVaWvmL2*b9AY7bFkF9Ikwa*%GIP^QLZ8Nih}M(CUmYNQ&;GkE>&5OqXe0i(@DWEHQ$jdFW^V2zR<DM>OnW`NX1WgZOQ7)l8PTPO{w@H2am;Xqd@N$=X8++d(Bxrzk0+_l&6m#SANww&{N>&;-1U(JpBHrj|<}~doShUfy^R&V8>6rfekE7WQyW}4J<s6$-~OV&l_I<Z*TN3{WCVkV~pudFovhgD=~(rtIU`UT|1Q9l$+stvvPxSm$FN_7q0gz_rsH$l)K@2w{oX)i}E>T4_x;s_b9h2w=4I-^*&{{a))xGvJ<X5l?N1x1M7L1;!+_74&-8r+g#k|KrW`ZREP&QurS5#T)fRgJ`W+D9+iuj7~(06`+0zg2QrH=m5Z2|$P~o`8(4TClZUtYBgUWpo@HW+1BJN1f0>x#Bo|XTgo!B*6ykvmEKG4S7jN^2&!4y6GkZHedZhm9fgjX4*eik8Ik;DZ_gsFi_n*iARNwK@+jS21O5k-4?iJx9A5W*4_{hOt3B1n1y&`;Z&lJ2{U#wq#&aZQ@R|2ndaIXjx4y`UvuOGc~afDktf4|)O^>^Rc*nc@=JjR&b1Y<^Y(R*N^S8$A1Fs3IsW<;0w_u2Y)ez`KT2jR0v?iY;dF~)ckj1kfGnb<?u;a^c6SDt|D6UtOthwp;xE~v{l*WvfW^?s<<={o#QsMsHZ>qE+efOaeU;JOb!?S_iI0@n(Bx(}W|2-gSU)8~~hDv!bSG3Cq3!-}d@;aXL`s_a$1q}1SAQ@*A=qI^Ml6t0gdPbzbBxAuPVv;Wl(zWLt+dDt-iwJw7H@V4SjfA2TBn8*~trtw4X;eY<Fo`;D{5&X{HH@%-vy_<`P%py$I@*ijZxc=LB7Sc6_zdiDK^Ls64jJIh_ojjXh%!n?chm0H5D>R0ut3O_7471-PT)h{rgMKrQ=d6D7!w-J6!KFMrH#aAQhg@P~B2xqpxRi&9Oc6Zf6&n+oMR=Qsd>(%I!3S4|oXN%eMevXVx%jFG9&#oZ?-#*CKIG!7MR=P(eEz_GtW!CJiD5qqVJe3(F_9^PsT{(@M5YL)@(B|YnMHV;KYac`T~ViMAtr{p!V|$%EyTn`rU<5LAtoj=MKDztF)@)@gtz%qlz%pA;I%wV)zVzt=Ta`FYI`p3uibhcrfO*}?sF*@Q?-3Area8Qqt4(DYmCR>SZ{(cJY8N6pIKu(2FKP%^$Ly2{oZFcTuG0}``(AuZ&EezS{|lqX)YdeiH)h+o{I-u%EMGG&Ba4ru`yNK=i+T1@_9(rz-t`5Ujz?1kc+R1;2~#n@qQ6J<U=mLT7<Xx!{-lG1Fz*_s+Q(rDu*yJRoinhl|z`As-?M@$|p=r)%Lk~n?HR1P&M#c9;Rw(E~aWBCZ=k8E~aWBCZ=j>E~e@tCZ=lpT)fSnqW4#|2Yb?koL%SPx8D1doUa@Zz-v6*m${yY6-C|9%fkb`0(gyw8G1M2(eH--dedLlU+T<_^-aV3`QI1!#}s_0Jf^EBFlMYr%dy83u*VayXXD--P-EW$*IUw>`W~pYcf#)jP?eK9{08{F3u^S+pz6LEes@6yzN24<?}mz8fhzrW_$76_>QU>Pi>dW3!fQNCtu+$^Cq0V)xtQXA5nkhAhTajp%|kv9_g#9Tx9`#?^;Zw<sB^F<im&Xwbby0<B6!c`+q{7dIoK1$0~>O1uLy7d`x*YfpP|-nje|W=3~RT}!95Y&U%NF9_C)c(h8)~0!rT1e^XG5hbb9Z9`hD-@l|R=x*b~J^K7N;ndm{MKCqLP+AqRV+cwj>g?iJx}{)q7hVzth}o+yU3<KdnN?ynsWd!l$?Lk{j0;cfo#`SX7{qW-S', 'village-water-trough-01': 'c-rk-dvH|c75|BXidbtwd;(zw6%AqU-QByp5%v;5LJ)`~h$tX#k|kNm12!8FVo;vGsHljFN>v^{T3^+IpqMz$bjF!tU(;#FVcIFq*nj$;W1XpOXL`=vy~){|d-r||)9D{3GkebOo_o&u&g<UY{qCl@b;;ae0G2HT{(TWJzrJ=+cOco>naTz#y93Rs_EaXB?Z^Zw1GlzhI@&ur%bLlgY*uTky(yI`tC?0?wmw`Dst88|<$?97OlP{Ios{*8V4$Zw(Ah{10+qo$>I_sa?+&yl+ej9ux6YLZ+B=%86Ty`|D+i9c18u3!7RxlRzdqgCnru!@-H^<tGE=jej;`jGsX;BkR&6XxCtGutO&whgt*QESQ>rOYnay;i`h9d}JFGR=He?p2vdPxgbYmU+q0l-x--cvoYIa9!M`mua(aL&xup+F*`7dU~Vn#d~(<0?0GvYa6EEtUkqZ*6C1(IO6T;ss<tJwZ1os7L;zpNsr=WIhEEl8dtJw4^VSxjwBH@9R<%q0>nT!`W}v>^X!;ZQK5Y2he|B9WX(i|fI-9{=AZVzsiw6oS!Qbb34%)I+)+rhxTeaIh?tYf;z;MItdR9zClxEYr@G!U<l|l5Sj6MnR_AE2vzYNG9Eu&ZgJr^^)0aCf(4LO<CF8R$E`Qq^5R}wd$hUx`kB>0+m{MV971ZX4lr%%~=%;RO)omq}!X)jcgJc7;LiPQhGTI4>*hzIy9uisC1|ma~K<N7%z0F1*Jz#lP>ih>l#ir(z(u#Os)tGU8`58GE38`4OZff9c^oAeA}~2Hm;>2Ml{`EVOKldaA@Gz-F;T0W5L2Hbe-N%IHwhgL=8O}i*ldRbOTyG)y;vHpA#({C$XXF<x^c<WUbHwOK+JS3UHNV3YtO+#q9Nx?DawRAvgO_zr7wc`t9pyS1qWj8{{EeLK6(by4rLtOx20%e52Fy^$JGfMlfuIxedCb*0K$QU2xT1EQ(bva+Xy$&a&!JpQ;;SzpBTIM-Vqe(Q~&rF}UHdZoR!k^pIxgG3)-OMLZ{eume4Ji_}8VU_5BVLRJd~dni`IxPJmgubW^g_Jcd1X~kQhh4eu!po|7w$h(nsCu-Q3O)W^ZH)rW%h906fY)ewRdbRc8hZM5OOf$n!IBw_z@hBMQB&zmWBxDrYhmBxN-98f03(XBJ>{vcjQuu~pb>ocFkJD70P5PQvQvD)&%wbQLNKm~1n&vE^777_9G{D6{IHH$Of~eulAVRmw5?Ww5I-nWh!4>Gg9P*cf%)p2S!}RVwvkI71vk1d(s_wh?)IVo*k9j+xf<HgGz`}p~?Exjswx6FoSqe7Ax=L8u`eBOA6mj}uu~x4N7Pd-Q#HNHrZI!U-oiY~d`eI&d>=!>U?Y{eAwq<P3l?pz+X^i<*-qsIuZN<92m}@KiC}9y>DY#b^=hsrgA{SNMR|*!jRmLJ0U)(*WqHpquEs1TP%ulG`cQZFw`0eVXGM=zwO~0)IHifM(rr1mor!Qt(xt1Rmw!JD?#HNh%YbjyT3neUStBgf#zL?kIS+eKE56?XsvS#&*UvE&tycXNqv*d@#))anxG51cy>5I7+VqIS>*6LNk!d3~3*p#rStr8Z!Q^KMbN*Mir51LHBIWN*jFLUItM)&b+-|t47EX$wsl;`dG^1k{Y{%oJ}oYT*Mt!F%@(6`T-Mf?}&+y1@$NF94^M?8IEtv=zWPsZUTFXrE^c1}Mc{yrfuh{>z|9`U>SDH2bCzI{IZo6&uzJ{xTkcbf;ZNIV6#_wplkq@7dWKF`NO?(DDWQGYl81%3w3d&cj&u1o!`c!hq!oJbvyc=}{KUVgmt6?Jo)AJgOdb&IFKk4t@=`MR!~pL5gWdNCEQN3)n8ulSw%e(~q$-*jFtUh-1w>GWgU3i(-GUtWH^=HIC=;xUE%jIS@JAHVC%Yu)!&J)hXMyP0{f>ioFX-|5G19=z5q;=fnu_t(=YSD7D=cwGH>)nDi*Jg(n@`aAVS{axh>^KW|8KOxUM<tp>$5x=XSLi-^;#E1A0AL8E^em%}d2-nl=4m9C893pxMt+)_VF_Gv*T#8N{#QQ|wM>p<79D9lG#SvVA8?b`t3e3a(coQdxp1>|Fr1M9J9>E)=U4{Kb_mjm#_y~K5?m;6i#{|?9t%r#;y0C@l7Cb`Q3(2aAUi&c&=V2s%fFEHDuEI44U=nUb1%fb8iRqYyxtNbdxD88i7w*PASdDwpj<r~i`>+{Xu^o@%aXf)%@H~Ekm+>loinsADj^Y@4aRGjai-}&0b1(weVH(kCxCmt^#}uMda3x0LT8t+;9%Hcvk6|a#ooGM`ZO9VMq6Haj!ZxDYumL^zF&-xRFdoFYh(aT(VK^?s3{(@X#wCd07R)3%6EP(5Bwir;0-EtOUc_Odhp`VGcnz-*eFf`qHEzXXqKh#O3DlvMXf0;rCHxHU5q%E_un|AUJ4D~X1DK54v5M#_+=Lpe#4@7GumG>)7x<Xy$9N07(TC$ik7EaJ#&Rqrx)eH|!iV^P=m&U~=3^A*5S@cCj*p*geTF$Uen&zTkNnfY=~GthR>JFM+-PC8Rl#ig#Hat5Vf#_RQ&wD(ux<S?uf?{iSmfTTf<-P$Sky`x=W|iU`C2Jqk-HMEJNB1edp1<?mz)03Yxi0Ov#mW#s@U$eDz;}y1#@inY^Y$7d#@_Cd#!>+t(36HT?va^l(49kDo%(wQNp6vzL;W5h`I8`Y%BV%gvBiRVqQzki7ytp_o`r#ixL*KQpRFVl(6iz9~QYQVY+vj;=Rci)4j_S?>oMjZN>YV5*F_}N?5#?`C^VuyifUJk$bNy7VkB_Sky`hi`<p4$VCZ@S}9?#=PbNmY3~)PJjZeB+xswHa)sv_1^YaCKc>@<*S?ce-#+i<$7f$_P^==ag6Aeq`I$b)@$%!f4=M6e+P8P=+y1@e3iWZ$k16_Yiux4DOL$J_oHtiLMdra2efQm$cIu0Hc9r|=OS{dFDf(-=Twl(4D9{)Ea+Ui$mvoySQ}o>w*Gqx?OrPU;`5C(Z4BdZ*?mt8Kpa0kW=gUoF67!zgp77$=)%-s3*FPSdewvQSXTs)_NS<FeF`x7%)A6aJJ%f(hPmMJ}pZy9r+1VT@v*hzm-(|8LALsn!IO`ST9M93Ve<i#)$HScCnN%~&bRKhl^G;WqxxCQNZ8^umoa4*+D>ElsesY}S;PW<bv+|l*AfJ@ibK|=|Jz~|%ivyonec*WAILCR-jy0A(_r>P6oZ~Db&YyYb<?AbtIS$q<#@Qe9`FVZGc|ER+7w0&RjUR62;zB>S<(%KKd_Ru5aE_PtI9|8oT)kn{laJjv>wEE``5&79@ALe}FcYH?qt|(;$8uB?twt2LV=^u!dMRe$B3y1gKbeLJD6^gomC<VfhG7IQD0q%@9d1N9bc9if1ZH7Q{yEN4EW_Qn8s}mp(UBOB^Kl6-BYGJw#AsZP3ZfMli<@vQ#t|KdshEc=Fp=m)EW{)%!AhblF$H&GF=~m{ViiKT6?H`GVBijzm`ijn?!s)`j0jPFCIbW!CmP3aOt+p5O{Z5Cu0#zqq8iS@b9fo8L|f5>_wf;4Bl;Si#S!elI-={aA8W7yyNT|`19%V*;{?$YcoPj+jTW>cgDf`Ter&}~Jc?a-3Qt?lrw-sy!SktZG~!;O_hK`e(Sa_aT}Y!758-j5k7GR^!#4B~<>yYX<34O5x&?1xyY;MRJG~ykaqHR8aeDP(kM+!G551nj2Y3mu5`7gP;vinYUZQ((828`_>?67lDZGfaXd~K&SFjOp;7OuSA_?Bxf2TT`*zxzp302J3)3-OQP{N;|EVnS*s$jM~wD!;aepK*^-Cy?G`e9y+ZB?<zy;lW`T$He=l`_ufqKxykQo<s4CCqzqVm5p+*_xv7zL;&rTq$AEcO@)l$rp2MVorRq$h}t;i(dO;Q7a`Za#zA47bPrerG&k{&z|~hwDntC@w@1v`yoz!`@4{rywv>=`?vP0`yoz!`8!xQKc()6h`b8+I-K$|-4F5dQ|x!Y_IG2I{Sc?V{2j8Jywv>=`#0L+ckiz9Gu;pI@>A@0!lLg=zY~`F;{R4$<)!Y2i1?NEL!A2dIWKvs`ynE)g1ru>{A_+#@8+lTt8)^gzT2Ac;>SMuWda|5UCGD%y};&{JpX-gWM1#Pt(ylOADS@E#Idg{o%}F!`}-jIKfH65$#(WJ^L~5!V|_k$a*pTQ;r~f^agOI3;vCP2o+{IM%>3X^)6C_Ces0S-4(10azMQ|@F>|)(`1sh1=klCs9wg5CPF{U+pH(j}&fk~pdXDnoyRO=tm`nQH7n|F1j+6Pyjb-Mje0}9H$H~WDJm04T$IJRo&g*eqyg0|PawDufxvn<1<(!}04>!*7vL454*PrF~F~|3H5zcwAz0Gs^3>*)AAIyCp{4f66Vx0'}
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





GROUND=.125
placements=[('horse','animal-static-arched-neck-long-mane-horse-01',(.65,.55,GROUND)),('manger','farming-empty-v-rack-hay-manger-01',(.65,-1.65,GROUND)),('water','village-water-trough-01',(-1.35,.20,GROUND))]
def rigid_point(instance,p):return tuple(p)
def stored_point(p):return tuple(struct.unpack('<f',struct.pack('<f',float(x)))[0]for x in p)
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[stored_point(add(p,t))for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,rotation_z_degrees=0,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values()),coordinate_storage='Exact IEEE754 float32 after translation, not hidden deformation; native versus final GLB bound unchanged2e-7'))
base_mat=len(PALETTE);PALETTE.append(('SceneOnly_OutdoorEarthCourt',(.30,.28,.19,1),.96,0))
v=[(x,y,z)for z in[0,GROUND]for y in[-2.5,2.5]for x in[-2.8,2.8]];f=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];emit('SceneOnly_ContinuousFloor',v,f,base_mat,'Single scene-only flat court support, no extra counted model');FEET=['SceneOnly_ContinuousFloor']
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
  assert -2.8<bb[i][0][0]<bb[i][0][1]<2.8 and -2.5<bb[i][1][0]<bb[i][1][1]<2.5
 for a,b in itertools.combinations(names,2):assert any(bb[a][j][1]<bb[b][j][0]or bb[b][j][1]<bb[a][j][0]for j in[0,1]),('Whole instances intersect',a,b)
 contacts={};floor=triangles_of(FEET,vertices)
 for k in names:
  tri=triangles_of(names[k],vertices);mask=READER['np'].max(abs(tri[:,:,2]-GROUND),axis=1)<=tol;bottom=tri[mask];norms,areas=READER['normals_and_areas'](bottom);expected=float(areas[norms[:,2]<-.99].sum());report=READER['actual_opposed_face_contact'](bottom,floor,plane_tolerance=tol);assert expected>1e-5 and abs(report['actual_contact_area_m2']-expected)<2e-7;contacts[k]=dict(complete_ground_contact_area_m2=expected,actual=report)
 tris=triangles_of([n for nn in names.values()for n in nn],vertices);rays=[]
 p=(-.20,-.75,GROUND+.85);d=(0,1,0);length=1.50;assert not ray_hits(tris,p,d,length);rays.append(dict(origin_m=p,direction=d,length_m=length))
 return dict(instance_bounds_m=bb,complete_instance_count=3,distinct_old_models=3,new_reusable_model_count=0,whole_oriented_triangles_and_pbr_retained_before_float32_translation=True,actual_full_base_contacts=contacts,selected_visual_clearance_rays=rays,not_navigation_or_full_space_proof=True)
LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate(vertices);result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,1.05);ORTHO=8.0;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(7,-12,7),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
root=bpy.data.objects.new('OneWholeHorseFeedingWateringCourt',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole scene horizontal centre; continuous bed bottom at Z0; three entire unit-scale legacy instances';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
  files[role]={'path':f'assets/farming/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'scenes','assetKind':'scene','theme':'farming','style':'source-preserved-faceted-natural-ecology','title':TITLE,'description':DESCRIPTION,
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
