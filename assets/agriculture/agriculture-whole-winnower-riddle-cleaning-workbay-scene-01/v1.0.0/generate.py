"""Original complete horse feeding/watering court display, three whole existing models and zero new reusable models. Lightweight maker SELF_REVIEW; static composition only."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='agriculture-whole-winnower-riddle-cleaning-workbay-scene-01';VERSION='1.0.0';TITLE='Whole Winnower and Seed Riddle Cleaning Workbay'
DESCRIPTION='One static grain-cleaning workbay scene, zero new models. Two entire qualified unit-scale original apparatus occupy separate stations on one finite scene-only floor: the rounded drum-cased winnower with its high open hopper and sloping discharge trough at left, and the tall suspended open seed-riddle grid with lower collection pan at right. The distinct complete output and handle regions remain visible above a shared empty front strip. Every original oriented world triangle and per-face opaque constant PBR is retained with only whole translations and float32 storage; hierarchy and normals are baked/recomputed, not original GLB bytes. No extracted components, duplicate machines, rescaling or recoloring. Unlike the existing silo service yard this contains neither silo, barrow, tool rack nor basket. Static illustrative arrangement only; no grain flow, screening, airflow, machinery operation, food suitability, navigation, reach or structural safety claim.'
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
LOCK={'farming-fixed-drum-cased-grain-winnower-01': {'bytes': 33300, 'sha256': '3098d0b8cb1e6fa79732504cb0110b888f5628a8a4792dbb3c3bb6c556b5265b'}, 'agriculture-fixed-suspended-seed-riddle-frame-01': {'bytes': 78976, 'sha256': 'ec572834bc42d6be720bc1a753d390a4fd3933e94605ec1783df28bade8a9ef5'}}
ENCODED={'farming-fixed-drum-cased-grain-winnower-01': 'c-rk;dz{-<l|R4QLTPC!bZBYmBZR)7nKr*y^2?M-Xs1v5g0@hg?Ur;VGZUF6(<H-CY88~1A`}!61W^QGS;dt_l+~SF7DQPEMMYsn(2B}SQRK1c;=1SF<YsO%zk74j;D5~Tlap_5&OP_s^ZMPBHtFfxvT_svw0s!g=@7tan>TLQ7fj~!sY0-AU$7^YN#&A-Y%bUqT-%$=X0rJ}4^9az>q}+2Qn|pI#Tx?`IE(B>PBa(_UXaS=)7cC%TZ_WM{h?sK69oj@!ex{Xwr$%N%p`Z?Sa36YFBHsVyVx71vt$2`;g|b@sS69aWS*+gncdx=&7?Agow;luo!fx}eW^k!(4D?8)fLF6yHbJVg?*_&@4&85Ad@Wwl7Yc&?)-G7C$KA(%;7UtXLl;!%d{!0u(cP(t)wD0qlAuJGIRdwfnCU{w|F7Fdl%ZECzl<_bOriS!Ww4v8mkz~7RJ9W)nl6P#u}D-4eQ-l!&a_gy({~0)N9n;2b&e>%Vv7gg@LYgCfOIr5A^qEa|P=A-GO9hE}PE>3WM1|Cszj*$Pa7aR%@^hMU~dyT#~a4#hCwiH6j{n=zFy*o$Sd{EwbI+n9hMt8s33qZg(J^3E-4KzK|@WI|KdMd}>&SXtfR-*<6+)EIpRycI(+;S1z0E3iM`k>5H<N0&2m$in-d^hwF6(x|5mK-t0i0W@uMB-`|(q8^~w-(p^gez3Hy5R0bzt-3cTyTGE+9Do1zH-IpC?*}WT!L|>|FSZ%Lb?M<b{Rwgs6OKU7IEwP!dP;Ubp(KZzi_2;thPjwcknuFOa)vIL3o?N<r2{$3%KsM92cUY%bwN8~1vlZp6!s*(cOlLa#(it=wuG86@%=KV8p*eecsX?;2C4p=|>V+|q$}P?g6n15kxvpWO_9r_9|C%+`Z*yO^zhs}1<Sk6_N-9@Bw|mo_=a-7`V6u+}91dXsW(PBaR28OPNn=3~(^rww`qWliQIz=)*1^)yL9_nk_Y5R+s7DgLK%=EMOZ^cTOc#0sX^iY-0Uel2(R^g8;N3J?Si%&{7jm>f?8<iSMb>hL(AyY>VFp8Q0Am;fE}71>vJB|#OQv@VyQnGBo0%pXag{ApnN-(mrV86eXK%W%E0@As^tN!w3|S#N<b>Q%BoqyKp;!o`1O0+#F>SmR5AT^B2zFxXv<17dg5dsI*`2qwD>tyawKIwOww4qeOlLCL!Bnm_Y~sDW8;=Zyon7f1O(AwLXgvpqOKG$7f^>c$*|(ErO<N&1kO~E{Ui73hJG+vFf!)YW2Lpr5zCtP4MY9|2gg(fnmIS)91GzF2)>D3q>Bg|n2a<)rx#3ElG8F?{#p<*T1#|33vy<99m+ZvzPjKJ%V6rROUr1k&+8%5}k$w48D6qX00{Jwp3clmn+)j3kseW^BXJ0D66H7=oov)Uc!h1%B4Q&s0oYS#x#pdlnI-XC`=w@O}%cCP0HmPJ68*zl!J83~I&0o3Z>=nyP(=SM;26y5HaZ|#o+t{)@_R|0=hYeOdR^peVH#?{^S5ZT4E!!zbk7c_tesgJ@$&O}S*@0c9iq^$FR~E(OtU<T4QioRU-<4aRLa+6uJ2%m^!c!m%sa?2EN477UTZy)&2h45ZMWz!j{kgG7*oio92*=zQ`-?c19knpl=};Ay<AqGBVR;oUFT5z?u$j?_>3XJPVZq694ThQANJ*GwdyeV3-hP@U^8GDO=FTtOlvn2HNMjqc*p95yj$F$&BbMh_I2LwGy2hem6BUj|BmR5x-Gb+_sh%5&IiBa*b+)h-Gnjh1d~0lQ3yxi~SJZSZ*Nr-;ycI6#Zaa?cc(HJlZpbS;$%{GRNGuX<WIxer1J&8jx^z!(q2!ZNrCW-}$5N$lY-?^Q{4CRP(FGVU;YD^iB5fS8qF&T5ARF0ONtzRlcy`o`>}Q#UMZCH*lC&kbnOu5znpUF{d$Lf-rFRV!Qfx=3Z`{0Q%bJZF*y0;DZd$)|9o`!-$<vvxbSLGphSM0C_V1u(Rd*@cOWMOrI^vS9xTINsNlSmp$ncWUCYH1s*rhkTWUQGb8`z~OI@4@qQAro0zp^E)Y&X4fBYSp)mEA^G_G?%4mlYz)tO_a9tCKnEenVe_*sumxxGHr`Q3GqF1|z!*?Nu$o(N>kCEvJsXRo#RB`mV5kq-y=BxV|l2zqV=6Us}j$E7ttd4FtI@B(`lfwzTAcufMk7al6Xnwo|({-l3A6_+CDnD+%2-(A}NNorPyhcBiSdLtFOtqlT_&Md;u_1`p6tcE`C8r?uiKAsUWZR@io8QO}D+B6urxEvNc`hFo^}AmoJYm}|Q(y+fumB@uRni3od9*YYeY7NW-yx9a#tZ_ts_P{eg3t{INeR;Iv|3!b&2!)ASuxCyiVCREcczv*^mx@iy3-`ufu-O^1XB-m;NN?BO8q7!wg2~5xOVr~S_zy605t9(Z0L!uR3mx-|Pv~9U~)(VBG(aLsoZ9Gt$UbvpooccPern_pR*^zoSi@e)5qu~{HtB$sHj7Dd8rD(-A#J1ds=hU%Uv^lGJx|_xTzyyloIofjUm=$d>Na$N^dNgKR5zFz+=phA3thw!);dgVtDhK;-_z)aynoVxm(%-UeF_j~>XQ6&!mu<SbcrqtjZdJ2f71ia;uxu-4hD}<Ntx}I-hNG6}VZn_szekx2E9POLwXC{Uu$#1k^X^)KxxTao-g-4`1r`jY`xUmNQOB_&^{n7FX@y2=oE5bqX4rFV(=!p!TWKVQ_sK}ac1`Tb-3aT{ZLgHT4sObd+LmYrdULgHyuG?;DNF=<cXdomD9n1iuzGqCziz*t8JaA5rq}Gf!mLw=Y$~E+Nvs$&8mw?6ieYbh)DF>d&(F&M%?Ypi;87J&F%)5<iLlDx*~Vg4D}T(yQ-}pr=~EvME0$?S>{z|Lvcei0Q3^2Cwxm%~$Cy@~3T09yE5>vklifBg&$cmcXbfTzWvS)T`=}RVpR)K=*<oXPF_xWSFXp+iQe@lAAJM3bA&EC5|9hFz5VpoHlmZ;JC9QCMOS<}1&W(EX!zL^2xlxQbkDYw2m~GNit{bzxC=D{xDcKQoH5!RJ)yF>5WQS+VMvKMJ2c^%lA|?i^N7Ec5JyI%_X7%T$^-LLQF2Aj4v-xc`a4zyGa;}YG6OKfpQ4f!ZF_zr5A4H3W3}fIqnBgAYdXSwJMXb8E&EgS@F0GeztQ?Z)w1^q8+`2K@<Z;Okzq@9jca?Ht^3OUOHv@~OaBZbjZllQ~lwGGlIo_}t%+lc@if2LGWXz$y$1=qJ@aTX!WLtH*DQW_mR#=%ZsaOvi@oGLIKZJv%ZP(w0a(<oq6dRdUsL`+lvDasP{;s`+)Vfrrr$GO;o!%zsK<V=~_I`nW{zKE%iAAhoZR*cu1G=-V+Sz85X1_SyR!zssSv?)^Ee)(*JKeIp2DVN=NvN7lPZEc&JK7@LjP9{o%QZCJw&?lv(5Jg$r<v)|ru^oFy=F}3*pX&T=S19QOy|U$W=!W=b~C1PU8@<>xn9^i^o+sVRzyEzu>Y%_Z#Lq%k@HQwnK!U|lm4rHwE$;?^;J8-16{aA0N#}v(O{$idUtBX2DLlDCOF(o#l?ExO!8neYex<}f@nM9G<CzUV$CG4iHCEisrg>CsXJEKY$Sg0z*9TlX~caa=VJ;ruzxdFd(TAmM}%MH<WfGhhz2n6PO*Q-{s8`+39xL<23Y&`j};F*^k)32+xz1(e92>17oWNv5-OZtazk<LGozLG$_H;Nc6T49#CNT@r@}A82flWHWnCG5<a-ZP^p|1Ezo-3WC8q0s^alr(nCidjf#;N%+JW=SFtsONSBAM?9)5Fy6m!3*F!zfJbHAuC_lpX1zo;<xiwbkUs4(}73Uj}xF!zfJbHAuCRQ@hb%v?2?$bI-yHde+(sQSA&@y2MEJp`V3Ee{=|@6lHxzl?{j!*LByQIJFY<cQ<QOZ@Z^$IG}Vkwa8GWqpXC50UJP2>Vj<l<h+#b|wm65DkA34Sx|0e-RCT5e<J44Sx|0e-RCT5e<J44Sx|0e-W9#PQb_e@Hz~R!0Sjj3a?|}SiFvd<MEn>94FxW^xdP_`0@Dq2z)*P=D-SAhF1bk!7Bz4yle>L)e0x$H6J<V;QRF52pc~cU!Q`{b6_r<1Y?kn0Rt952*x5E3!`BnEP`=J$HC#S7)+RebOMYA3mlk)bP`Mi7osp3>0~$>JXiu#kxqpcXoEORM>-v*KszjjnMh~CG&mJHU^dd(FawsuN(dqiLI765JQ#&^6r2bzo<5P;=B)+W<1#$q%dZ!8@t*c^Qp{!6!~0sk66ZSjVJcG>a~=FJm#M;H?(>+cey*+$H9QF)9&!jgs<jdg@Tk^mgr~9=jn~mgM`Jusz$l%JbTY;v&90-69)-Cz1|z%$X$!{fVJwFZ!^bfg-J>w7$KzwF5Qn!EWq3H=>f;AyJtD<iW<6YrrCX$UINs`Gu7e-uGFAA!I8?{svgo!ruSGK4b=?ixnC89=bD8xpuSGIUW$I$CgCFKHRrtO5(T$&5iZVPLC-pJSSsCUs>tS9)WOz7E>SL~hALcSu_`Ud1$Is`plgXa;kHtT8(>ZY&{`eoh7}v#*KX#-PbD8z9ZQobX!4FfJx|r+Whq+7@elLFX;^&V3&lY8v$AAtV_te8u%w^WY)OTD5Kg?r52Xh_#Fqf&q@5PTgevWf*D&G0>!T8Fr=i@Sb=O?c!-Z=YBC4Oh_vE&;Et%M5S|JLy&zUm|;=IgeP+bYF;T@~i*sxV(yg+*VS_np%df120AY)7B*^@z`TaGdecS0cZHhtStPJQev89-^TS(a?uz=tJcC(9c4k+@Br8KJ%cx+XU>{#vrAiSJ3Y6aHO>3Yr&pvJks&l+fBg^ZWPi{*arqiT`@#IcfF&(JubuR3O5ctvS)lkh4*~s`$MY_PFLcYADCFYG`K*CCtcD}Y~Nrh@ztNZxH#%QPl@SgysHnkDe<KTAFA-n@Rbi9tgI`;qdMNH=r6-<>&Fsq2O0kRy%PzyrwlLu)g;3GBEyvb`rDpVV!G~uhwfKms{fQzZ&qSzhdW-pT#2bYop?cssb6MacD@o*|8jmArg6g8m0=ohTz?s+am(!>!!-W6J!Saq;AECZn;w{@h0SQ&&~2Fs30*usb;A%oYvb<AUmGIVwrb-S<~YTd-|)2Y-D~$2r_DN58&m&oKd?+2FL~xWmAN|jmdr~P-E{D`4!n=>z3bo?UY|&~ZFTUmGp7*lI~{!XHOCPi8#<WI{l#5RXk)4y?HP43-TQ5w*J@*G+v_8FZA^Xl%ynmJV;UQeKekRA)7ay4buf)>uA2^~xx@FagK2JZ+v;GN``mXrnAeu>?mLS*nAa9v%xjA-=Cwr^^V*_|d2P|fyte3KUR!iAuPwTm*A`vOYl|-CwM7^6+M<hjZPCTNw&-GBTXZq6ExMT37G2D1i!SE1MHlnhqKkQL(Z#&B=we=5bTRKE@XRE|ypK>}-bbh~?;}*0_Yo@0`v?{0eS`}0K0<|gAECm$k5FOWN2oCGBUG685h~342o>gigbMRMLWOxBp~Ae6P+{Ijs4(v%RG9Y>D$M%`73O_}3iCcfg~iV<vh7adg`W+z)8{fCqR%4F5pT>-+&urP_$|Xc?X^4yW0Mj?Tb_+y9(StvMIQP-<)b_zzsN)9(fM?)$S?AU`ilHA9=@mSNS+}<PSH<}IF9-h{qzyX@tOGTOB_de#LqtBIO;_F>@1F#v7f)FoZ>ACp0YkgL7$?Jzv#Y*u&<(zzo>nPU?1Y+FS<Sv>`Wy7B7(n2R>4#DJMr;XT+k=(r;j*Zj>DplzY>Cd5`Oj($7|!vFa9q1;r>MS_A%^p$}(oTD9f)!AL&cH^T&rpeuibaHhbFI#EVZI&vX>$%JPo#(m9kzoGa!Ol|g0I$`R*^d!;&3T~%^q{G$D+ZR(ASxry?NT)u2v%v02#aQ$WZEArqo;r5Z`vdDvL5^jH4UW+`qC&K+J%W;vXjEjQ&5&2%0U##Vq<$hUzBIsWf>@%Vcl<h+V`w+qYM6f@pl_Sm-^S$g}r5v#il;cM!N5(JKigJ7^$Hlr)j{gzkV%-pV%K1fv{2ftSM4oc~iuGYcoe_D&dLq=2s(PwXe~36&qy7+au15VK;#`gTLnQTwNa_!f)E^?LKSWZ0h@}1yN&O*``a>l3he+xV5o!z3s6RxgEkvXK5TUjZjrv1`dO|enPZhsL{UPF9jrv2xxf=C{Na_!f)E^?LKSWZ0h@}1yN&O*``a>l3he+xVk<=d|)E1&qe~3_9h(`UXswcAgBmP^YtQLtpvic+P$ZC$rBdaqak605#evwD44<f&eN30JuJVSz<qMsabT&x2%`|_<1HTLnX2{m^1tphdw^38o8IV1AjN1qWn?z68EdF^8#BG`xc_^Xn4BEOHns`Sk&c*Gp^i60`w5ApGrZ$A3O^N1Yu$%_$rw?gZC4Rc^VUME8<USY8Dia-pnQy_uYGFX9E?ROtez!{X^W}FGea|C<$1U4SS*T>@X3K(mwH%`NAm9ZSJrA8dDC5DHWYgl+KHbQuvWX!|sL?eLLOk+A;Q;in9jy5LZHQpGD*J(^boXxe^ta*%oI^&$kc$TwwLu|YSUwimG)>sYeVGOKh|8HR(oB?Bz((hTE4rju6q~qam*aGLmM5Gg89GngR1V<x18YaMYI1eTxoeYy;7j(fCq*I^;x}g`QA)N+O;r-ADGmy@J>98C6VK&m)FcbDb0fI>B_bdkBLYRwmE}RH^VLzON^dy)EAAn0Bgfs*T;9|H879(8@3*l1u7+6RxSOizXHQ*w3!Gw>)C%{AMfdkjV_0Wd24We)Z+z9PR+hGZO25x~<k)8^1_$+)LI*@k2Qn(H7fR#vB!gBZ`tbtKT>32W=1^yK_BHak5!B^lu*o<^DY=D1*Z@^ZhTVWG?9lizIkZyys;NOA3PNX~G92kQCge1}=?0|>i5lA6TK_`3{{tMDb)6fIohaW%&X$H=RAHt6zhcpLS_zC<BE<kz#<l!m!Ib4MFA{c~c;Fs_rq#uHP@Ekl3A3^#N_#pfmUVtl*UI8D5-@z+z71FEVa(D^;2nUcJfRDl-;C1*U(oe$G@EW`cpF;X6xDNgY{sK24y$L=I{|o;Iw<5h2Zic_ZDB}xAzW|?u_Zf#7cOtzLZimB-FTq-*YvC?9!kA#(gY+KwXE@TBWZaANUidN`WlT2iM|wYe6^=2c7~e$tP52rdYfLkWNQ>|Q9A_MFJc#r`_z#$2%rd@>^xN<d%r;Ii9!2^nd<TNY9OE&hkHPm~t})+u0_hX*I4m$uHl9TKB>V^#8m-3DNS}tE!Xm>oo<;gB{5OOR$2f@eAp8PsBWnB>>2Kjz5HZ?}myx~<zk!(1ZoG>0Rd^9jF-|r9jP%d&dq^0|j5m<J0e^xHV}<cH(zoF)SZS;_-a+~f{1w(1YYi~g;Nx$w&e&j#HrC<8Fg6<FjJshYKE@dLe)mZ7@S6(~56pTbF2kWM6UdRH7Ao;ye=?E${F0Co)6a^}n%Jtu*ZlsN3cn0*?`x^7E5lE{-BQtChAIEvm*y!kUH41rxk^m+U;OMGC8l=Z{4z}K$=8+Po^Op~`rpw%q=f_5j3?&UkT(A5;}gj5RxQ%TbdR5(zE~UI_vgu#xjMMlno`kC2cIxzYGv;_n9kku{9J8Jb^F}yCu(E5_uoDd)W+1de69|rzT>*-;9HlM@|u1pMTYPG^^xR;j)h9R=Mxjjj@Ls<O!w7$U8@pLT{OAEFT=llwxzPJ48OeZ*oyu#O!@zG*E}Vr>n?bEjuKP-XP&FZ)DE0qhN(UIx-u+&7Jd7Vwk0Nh_Wbz$A9y)l#zl%no*AzM*yGXt6`pu44;`cL(Q%Pq#zWWPxQ3@F$RU1m#Bt;$e)@>xW$d>vDu)PiiV}T@pbwGkiwOH768jLrKE!8V2|=HVFJwO2d;DPHmDHv2_QlhN%D70eX#XpI<0R-KZB82!<%n}dztA!Io=T34U-TW-rQW#cN0d#teA&3@Q<Oot{xV;SJY`%I)+K^`BFGo#76tv8@51Rzi-+NRV{Ew`(bvcy=ln7`GJY{0%JwH^`}mIg#0Jw}><wixBl3v87WqXU(eEO^j7Ri)4Np;!L;U23<DyS%_T}qqA2~#jGlEC-i^yNYQ}L0=FXIt?<YQ+d*qQ0m%<m6u!Jab5x~V?A(%6x9WA}9)UOTX(Jr{eoEqLYFyWMR3TzuV!&s(tbKN)-CIpyCUSXBA_fe?hT3l6dGbJO1(n1Gc2{y+q~&Phn=?+>)WDcBRYvELtPhh^9Wx3k|LI2F6g=}77C4=l%iawbyx`va@7=bnv}{{FxQ?74$TX<xhvJK|AD>F*DmiT&h4qzkbxJ{x=P#Yh)pm%I)8aTBQtt=MxWu@Byf51aMlF{Cl<e^c0J#*xOc|Lw&-vjb@dB(N*bV2AsDd@RMTd=K_?yYaCCyYxJ)N4g&S-~x7_XCOTTJK#a=Z|5VOj~(!oh0hN?{@7#jgBP{LWq9e~M<@0?H(LvTWz}s(8Rjxo_?qXxH#Fz&XPHbHwkEYCW`BCA7N#;~n9EdQ@m}`x^gYFkpX+CzOVMY1J>oZBaGdecS0cZdBRV`fYtb<(s{x+Mx;1Mx%2Qcu9A?uPq+=AnhcFs*tc87tM*e#UuZ15SdgU)q#ZTIPR9uE%_}kHmo4*><!m}@XrCo-(Ocnm?ll?<ezj}Cr%9P>z-#R{VZT$MU4yH0?n9Ee*_u^0;hun9Uy>eYqhItI=;7t$QD#cu;3Ul94nKH~{KnGKqGR$SF@O$y2j-OZOU0K}MvWVt&y9|Hv4^I#2;>%t+qbS2%rV4-XrN0&L=-<zJTN%D_#{aeJV)~l~GR$SF@R?V?$}s&-mJGk~r3c$}G5x=nGR$SF@H;==$82@rp@CCm_-n6$Hb&iwGR$SFFpZ(#eG~|E?Wp>$^0_yyC&??0tK@}*C*i|G4uPj?E%7_md|geRL>(TY$y2q~ajkE~KR9?^)pxqf-|bD*;UPXei9_H~twkE(QLWVoPeS}Y@+72_*msYse?Mvp(kXbV63<JtgPMVK2KF7albVf`_8qjR3L*{St7Gx~X-KExE81nvM@oOIZ6@|4A*3PfJ7%$e&78%4$?Zh!XyzfEhaJgW?2|?#9nJctg?NHnz`h49{%+eMeBVH7;H&=!<E7+Q', 'agriculture-fixed-suspended-seed-riddle-frame-01': 'c-rlq37izg*~Y7CzylRf5akfZ6$Eh?rms0TW&{L55fO+dip%c6t}Z+4&Mt_GG2X`87|o?IUeRbY8e>p#*DGG}h(}_KQDcl6uXw~W(d2uoXKJ@*wyU~_CL}+<5$EB*-ESTJ*4uAY^)#@eW$|oA2sz27<bkDx?6YY9`N!AP=kwW)n#sr4tjM-z+v_`W?KP8Y_HAm<wdV5C6(|y&(UNU#%(h48PTD`Z%AROVv=cS8HLJ4i`Q}_JjLnI$nzgkx`36)_GdWhIe9h#;j<0F0Ux{Nii`;XyHLbZu_k?91zV`6mACIre9^27gpXc3Z$gOP4wPss8mbT|wc-e!R@Ou=eTl2ilY_vVsiT*T3o9bH|qbu5*+oJUy(T=8U6y1#Gmb<vT`B+$>&>Gha6`_YKv-u{sgT-FCHP39%<@0l3vo~sjRb_oCwA0qy8eP?#Z(i22Cfddwnnx$l%@s|&^%d}4L$0+o+t9%s*3%KAv?H^QZOi4ejq`G=v+WC-TVt_J+8I;d8Do=n#?p4i*tDLp^_|(Yo^d=o^R>3N|3=Kj^_|(Yo=Ipsvx#FSsqc)hXJ+C+OSU5$ZEMdR#Vc=J5pC;iX(=W%(I!uExkA1}zV0aGyVdnAEw!TeXtuXksnTA}=4BS3);S_W25}H-k9M}TH?L^w;H|Di2Il!Vnm@YP?M)NTMDv~bwrne(AENE`%`H;SE6cvKdGlFb*@9fYBXInN?1Z81gt2KlVd^?zY$8us+D`a-VzwKTyor`v>x$-%&c^1}`WCm5X#KL>s;nEFh35H`-QL_-G8Y?V$#o8@TGZ3og{UU>AMb+W*9BiM?BAM=u6Bo`xwWCCxwWu1;khA?GHuai*^brOY-_Z!IgdNJp#uYkL=ff6mli&aVExij-_W!YRq}k3pCaA8(OhfG8mYHsId^Wc!8vYwi+FSXH_@i-Z^FO7|5N@=`u5lOpYm_YzrVp}8-53sB#=CMmTPyXAC!pZn;ZF5!`tg!IF@Dfd8lJ=w~9rmA@-kb+t9TgD6Ser`}roM(%kB3d$u9lyvm($>szC%n>(5?t#-oi$OuTNZSF8NwD9>nx-8exft0%}%M0=}!-ts{%{R1TfNP_zx#)6!F5kSev!%Xl#ch^%e)SBDUE@O0fd%!g!6t!1&@}LkjGOjKJco6Qn*g(I_1N8IORrDrjn$_&Xn&@tGqwqPVrzR6aCUBNu3wSk6M-8y%i8N3veBcn**4xB?*%rbsG+52#Fk;@#D`ewN7=-%2o=rd@wZp8>ewdhN!+I=0VBO<&Dhl3a5Q&+2bx4&wihSGLbRK9bVatc6Iq1EZm!+!3_6x~BY%0W(_QjnOgnR(c|OnbJAq#tUw9%{wdOjan0DJ+>f79F#10*IN_~4?x}dUIVUd`f7i8O)=Xh{5E_8de7z^59UPkdcH^kiFi*__;qetbMTZNN*vq#>&%3Nnh!BQ9$J+Kldnxu}FO$Uo}ZEhegZqCO3tNltT`xWs1$T#7>jH1@n_3gz6C0PW5bi?x23-@!+PDt9Jmt}oEP`#_BS@rEfm-1ozVfgi96ZymR>4&k2{9*a^qu`H*rskH$b|jg}hsA1*TC>)wwQHT)cx|FKS(~cGHVvC3Y*Da5z#1KEWGp<fmc#N0D-KNgn0YaOVbVahMxsQ9!aa?<1%Zjsz^K3>mUVcobiwX}#-+`T=vqB;LPKXuM`wGs&b^4bp7nWMJ_{*CeVuz_)L{r~YupX)(#GcY;#PZdP2C|lobSM_+OQNm^v?R0rS95jGM}z%YjW5VHMcHptncVt32S!_FD%O7;pXE|8*=V4zE;Q=QgC)kv}1LycR{cmcPW1BXkNLDuiUVpC}hCiJX%<`xt*L;Sm5O+we@5$ckm_^Mv5;b8k*`cQnfYh?$gwzJcnW~=s@3&Us6-wSl`ysyehk-W^#0SeM>%D8(mTek$f{Bb<g9u_NDF<)Y6k{8d|dXrH$Fv95QpssVtvh+(S!hW*#zg-mFDSYWVSdJ-=kP8Utg9BOOic+4@HJh%NoRbS0WAl%GBK;8}YWimz(Uu3p+wzXlg2wR)J_?BQ#9Y!)LDvruWeUz8Pzes*DDhk#iL-?cZRtovNJG1s}QFyS?dffeCh-@bCOJ2r)~wKZ+a+V{)y4RLeBLjHiJHJf(>Z&`glJ2TgkYo85w^T*qV#U@(G6#p;j#8Y-M=^%t-6HP1T{%0Er(=r`|er%!<vt7e@!ZZ@L?ciSEeJnO3Dnv4D7cKT2o0yEd)fu)Ga}2{ytmQYJ`hpJVY|eHp>d0nW3XAvrboZHbV}(~{BnwxOFmP2)!b<QfGg5`iO~w)_oZ*Me!iCu}E9F>@V|riMM6+0(VWiAhiqAV9R~j$Wm53Wo(y&d#=Sum|?S*Z7$x64ftF*0>tF&tsLs~eNGUAS7*{Ou3xJskwpoC>4;GvZFWhSknQ6d4S#jUk&ydv+Ge%ayiwE`}#y?JFbzrzcr*x|J|FYD~cx>vYh|3z~b&)t8%8%gu`U%21&dDz<F#=&-=xq;i5y*CDo)*j9stpD;LaFbSVleXNXBR6UIH)#ZKGTz%{B1Dr$1y`BuZ88<6$qKI0kO$M)fJUXq`oSADrADnVjaG7{w$!K-qR~o5)R3acNQ7y$k}H+s$fzig%Ad9eZqk&($Sh3?ep#W<)AituN?F0Q!!%lfbNP<Dr_p$bMk@&;z8CFjG#RGRO0G23+o%<*s8O#+<iT^jA+>9UY`22zwWM&eDhns?C)~kXmSV~(i7Bj%^mnZHv+Ce2OR2(2g>AW#khZ0aVH=@auHc$&Y4)+LidrszZXCQ#Y4Wk1iejt$d2#SIrMbsWRM@7+W8UBmOF?Cq&Ob4^VbinW(kHrs8+D|t;h2?PZRx|?;EhTt!>KG~cs!{M-mH`_98JCm(rhJHE6qYqva)8i4^M;lK$?=`B~wz|@VRwMo{9$F1W36eZdEkEC67CUHz*~Fcx8#g>+xprcBNzy*CY!gNV}C>uaqm|sc`L9GW{f^=_g@?Y`22zO-KQiu=MR><6hr@bNO6*q0(iY%a>={4{Xk^b~oWYPiGgeY0L5q$iIVWz)aCmXlG^pv4y8C?qi08;XY?b8p&h~pIZJz#C;@^jHS%DV^|6PprDyQZLJe!;tA7zn2?Oc9Xl1{k7=BgTTLQi7)H{F+bGoGHeYk#teKYk+*a<U;onVNanq}~)l=NCddn}GIep&rg?(zU^c{%Dgr9KHcFHL{Tua20RswrB*K4svES7}d5;)GEO2ra(;ki!AvEm8aGG)IxWsjM-6O%>?ZnPczpRiKgi80G5JO{F!n3+hKR@}#pw*OV=iaS1Tj3xct7~jZlgqdX)o;|`io=C-vc%^>ib;JvgyHHgsX4)~w$B&6{eoO}Sg69QP6ic3N+!&#h3g-eNwsC!+4TNA$*nl`NjF4V1!`u(X#8}dGgJmQ8Cfp~(F)L9R$3!A&z%;478&HGedclb$3>&G~s;x68CK8V0BpevU&1A~3vvo$o&k<HgN7x(J5$;$Th3^4yF{xP6tk@A~sBlxooK!q!$8Fzea6&pE9^#&;EEv3<xRGKZWOg)?8`TZEPzdOT$|E6Ub~JsmBY$s5xPa#=_dhe1j2m&&Nx1njUO42$EWYsaS*Cf`5l=WJ--hvT2ouGxq7rs89<!1@ZZHl1%g~nhS+`knzx9S`1$CsGS4{VUEeG=o_J|0DLUfpLO3XA<?$>OI!q;&I*0C16V3p<-_bWsLrQ?W9K2yc)LVy{GWYVxw7QZizRJ`y_YYGwNByGPt%CtlJ(b>3O;8w}FCc6gkf@|lx(zL9&!z0hn3-OR%NCdyB`dmVVvC!9z8z~Z!A$^eAxIWNDLNFgx9tTz|oDVFclDnb&i*R_sFr1RbHvdAt_@%muA+&9?bPtknm(~f#jM;V^xfp&dnD^vj?ghBC<P{1(FPI^{U{w$aeXpPrA9#ClWB4FsUbHI7i;huPYs7IwSlA=+OGuc81(z7{IA4gkOD?P<aJyhZVLGO5S*7c5+j6~z<w!D_wD`^~j>$O=C-N;vGH$zz4Ss{A;&3@%Z(y!X_&pu5LS{xQ5q6%nk{j8R?tacPVwQynNn*+6?!_wgr0se#ZkWlW8OLhQ*O94kj<hRSxAnP%3ggMcj~gkR?2yYg+uXQb(8WSvFH{-|wiVI|b|tfnQ&?(S*lxs3TnHce@;A+RiggNW_>`G2jJTDu<$EF?b4nH?wJ|rP_FeXCyX}O$?0E38@7v)DFWS>_8*<T!kQeQf{rGut(ROi5-g7nl3d`P}EWFNFd>hj?Eq+7DBkfg(S=g=h>`>i>Rl=5Eh4k}6%Ks{~PlsdrStM!u%_5FbLE<Qky!=*V-!~w+TMDj4QbBr&$4Xab9(7m+xA(j(%8wN{|0V*;v`o`4bvPlHW{$Oy-Qe!(N*)j!mHWY6s23e!C2ibmehYOc<nqj^Xn7WMZy4Me80o?-kxDsc%Es2puuT3ahhLV1bu01&QV-4=rK>Z?UDINGkxXz4@$H#yCt|3?apES{v_@gOV!L%<A~i7K7=F)!oREt%r;=@J-%F^(37%fuC_V_eZFPK76Ed8XVT(^aEp#}Z!cFf!4=Wr)ZbkAeyzXB99&|~D^{69Ws3Q?e8D`3|imQrLd6w2)M?4nbI<yrS`W%ZTqVHNgUdi&T?2hNlv%>5nf0=8>3ub2A#EQ!<eYV)A3LcZO^39_eE9?-(D$duFA(v-yd*eF6O|e$tVSCcXQPZy23x!Nvh*J|WiJQ#N3n5o)@pvVR)Z!l+!P+{JG~7Lx$7AML(ku)lynri9T0RpEx8oBu4#0CM_uEWUJZ6r?u=sNle&0pLL$2TA$&Ks=zGE?pD~~ufa46wa>IYs&;k}8Jg9M&L-1zz-<n}cY3$^g5C>lH+xiNwv5pwsMFgLCfw6PG(3mXs$iAwV$>gz2pzbE9rBeZNyM|NJebwvmN3x9a-<OlX&zTEx$)cBlL-@bw)R*iA9w=e!>-2*{Oo8_gA1b-kd7q>LU6K1Tecq(NEZ@o`(?7k`}Zt|~p<>HoYnISrF#qDH>&SRkvrZ^Ugp^7JCVTxmV4O2W}hH_mZ70PwVcqrFlM;4~I5i`ti<&&YDXBbW>?-`~U%6$gXZ3X4s#!Aa4%uwa+7*7Pj`(Iw%irK-lhDY;OA|9&y@rp8b-|{KP3{xHp>sYArPPpN7l13>1#f?}f|HZ9TDF0yz63Tz^ijrU7@(I%k<v(oTL-{X}v_knWX_&DPw{Nmf_O9&qMe+?be91((;Y-EB4PVL%H+=9{sNutkFO2_8{(eHJ@+c9id?Fdfe<ptr9=yDhh?keQ;;~TWQ&t7nZ^X;{Z#sq<;{GwsaOux9!=*p|mu-X^e=A)2Gp%sx&$Nwj_m6FdyMOF>CHIekY*oH#vs0DaK^`?&PDNv2C(9=RyYCvHq9Ar+sZeV;{vf~(Ro)4;hI9BV7^b{wgj&O42^ne)=a`95YdFVDg<8WomKiFEIhGSDi8)p>R1$M+qwfvW^Zcp!>`9(QY}?|0$Tu2|Uhym;Gv>}G_^)eVotarTdTd6=jZ-FN9$Gv`%Qp_G%M7fm(ej;hYcq{gcGfbtzjN*=E%SC+%?K^?{trHQxR%$Ac6#hpe9Y`bPrE8!HaOYSe-(3k;RhA-c7;C`oR-E#$<nweSsE85OXH$sX<U>njf;|{aZ$1~E=rchMaj~*C|Md8CClTYVA6i_sp*~eUM;w*z$bMR>A&9NgnZP`>BgszP496+VB5{>Ew|}C-ossrdb)Ks#r|}c+V`<Z3!7ehwGHpPS3SMQ-Tq{}`cpif*4Y&6$&}iA_9s(nueOoKD-&S6G6BXb6JWeD0mds6V7xK`#w!zGyfOjCD-&S6G6BXb6JWf0Y#7;<MDc4UG6KJLAVcwMTQU&8wjx{LSASSAoabkUy2rP`&m-_VBYTtG$nN-6OD5r$NgVu2k}3F=Ce!h2FIeo2^Zcyi9-oe%C*k+K2_+FS4mysECH=@|WCC;o8BaDRTar3x9od5nAlncFYLJO!YciPFP@BZaATop`pb27;?a1~d1x=AS8Af&_Q=wDIWHOwLB6~vjB-6-9vNM?pok=oeG^ru8p|i;hvJ0+%40H^cMV`BAaJOYynFZ%wI!(v>9TdwvH~IoCe{#{pjI(%+FOQotSIfN4n+~YaGVj~^jv-neF(}?+ui|5#N%XX<W6^&V^E!ney!h(2FS~?4bu9d;W8qIf=Ka^P@TZQ2KXokpsbk?!KNkI0vFuMT=J)m^*5&B|Yx0>QcNMraSN9$#<h2p|ch5L(SRb3-<NQBy&eNt_XH#seyVSmqO<LIW+N*6)PsXdB-s5gRGKxNDr0dEk`ka>hlkxJ8!q1rie$E8&b0&bFGXeaZ3E<~U06%8}_&F26&zS&zmgXt_3^l?%&S$5g?hG{rbJni-rJA93b&vCTX?J&S;`7li&|NTB@cC#AbPVQ-%`yM*S!q1xsVy-d?E&2bvlgF^_^dP$v(_NYKYUh-Vb&Ug`N)D=n6-vs{z*U+n6-Aqd^8z48S~UgT+e9eXv|t7SFd^V+AbaQT(rZluG2ElX|u2VsV_HO^K&ipIxjtWotAmuoFnekGS5ZAUd248iFS1?`mbVMr|^Rpi(Jk9sbk?!9SeW@G4H>Qg+FyH{HbH%PaO+?`myN0ie-O#adqCQ&O2YFc?Yqbme!?8me!?8me!?OF0KQWEUinGEUinGEUinGEUinmEc&lvX^ra1$kiEXpQU7JpQU7JpQYvEzDCK?K1<2cK1<2cK1<2cK1<7@|0<UK>BZIjT+Pp4#r#}czbRQ-zbRQ-ziGL+UQ)8Oep9lvep9lvep9lve$%q(zlx=`oF|K%R@{#$S=x^%S=x_ixw!sUva}yjva}yjva}yjva}!3vgp5xWq*2cH9uGL^H(W9^F8?eAD@|d^_r2>bo}HQXJkHncxx?Rea-2a54(On)sKHN{2(p!I)^{Ga*B?5-}v;R<J%j)*<-KbS7x2v)2@z1|5eQE6n^kxz6Tfn)UoiVj)gz{nD<}D!k;=8{?xJXr;dd`{aEy0#j-!WxSF4<`T47up9dd&N0*NIJ$titmzMdx|I*-le3=Y=P|Li|Ngq6_W!|^PAA3y8{GJu|D(3gTXjjLg|0?En3O{(U$Z6c4Iu`!avGAuK^Zx5t_*2KipE?%))UoiVAB+C0SoWtESMzf<KY!JpZ%FGmB}?l!B}?l!Ef?2IN|x4dN|x4dN|x4dN|x4dS{D6Rv9y-+WWEQN_9IG`_9IG`_9I#@uK$%R?MIX>?MIX>?MIX>?MJjM`mbWypI%(e&(-|=Rm{)D^_!BV^_!BV^_!N9>m?;i>o+A!>o+A!>o+A!>o+Zn{;OD8%XzZMX~q4BlBNBKlBNBKmW%6uB}@AeB}@AeB}@AeB}@AeEsOrESoWtESMzf<KYx|-^R?f9VEyBd)w+MKN5fMCuxtNR%?r~sJT(BXe`w!CPn`;$8h~AUxlRwB>c_pFJV|?>Dr_<yHr)a0=?+kj_Wn}X==zfh(4Ri_Q1=Z`icdeX4H-;^L5GncI1?d*po7TPWHa|qA#8@vmV}XkWGHl~`)2A^WC!RDWLuJN+P3?h1CrCOd+_YEidVkz&n`a}_D9?~SINR&$K3vt@#kbjonFlC{aDz`b(XWR*Ksut^>HZ1ckscVcd1y6ua1TNucCvyRV?gvEXG&V>BVAvbu8@VI?Gwu>$n;}`uKsb(o#P0WcWPe$HKmN|9Y~p*D<%3@`)#Ndp{QTa-HQY>~&m?pJ4G*ynj7ejIWM`eewSFWMQvkF}|WsFBapgV_`4XS<b><$JO}J$ItqXA>B*PKRGktxvSDDe*TG1yZl(#e=>elw~B?mj=BB9b?5ce>BZdMkA=NlXE_Ud9arN=A3yL_T8alxhR-v8EbNQ^_hezOV{R|SgC}!)KNj|Ko#ia-bzF@fef&ICvsL#qT~_AP<1d@0;)7HD0`bK^HZ!?PH&-&RGYDTa<*bZx$~YzSI)m`vZ$2~g(zDa<QZcX7kGYR#XC9n3<*^f8pW*jz{&TsX6*ieNo4fhB4Y1L*mEmOq+LW}_dt7cekWEip1IXs2pZgSmy3YZ&gYsR!{2ZXa`=?L)yMI1)GqNQa2IbERwsM~eY=zGbJ#qNt%4@n*EaJ_Nc`UvB{9Q^G@#e=omR9`nmr54#=EppiR?m4t$s*o#T#ZA09KxR&DHnM%{27R)T;$2T&LAx1B2VUZ24N{Lc`~olkE`($EPjeP#FIsw__35jJXyqvA4@sJlSQ2Pv6N3dS;UEstMQ|cpE<9LaQXcEevwx3{U86e%a4Wqy3u31RV?gv%<b2WK5d$)(~G&i9}9cA&T<y^I<Bt6_3Lo>DlNr>C&T9%KNj{y|9i5q*D<%3;=z--y&nsExz2JH_ByV{k3N2$yXyU}#~(W<%|9AW2W9?_wuZa>`271m?t15db?MXIzA&xfbWpaeA>A78@?&F*cU&H4oSD{eIw<!$aA3EFyZm^~o3D2*IQP<YZo5;`8cql0>mJ;yTf<#`%wwp=eDCh#GAEYAAAauU$3>heY%(4;-5X$2(v}?GqTPTt86TVOfHoy<Egd;JJ@RiSl-z^(Im3_p*mQf?WH!JiNL&Av{>aY(#**=559l6bqWc_RFmy24CeU+$t;rxV3Ob4mcmMvVouND9C;m*K23mukw#WJ5(Bb%LM>3L(gN`F($WA0mYN54ccQTsnLh7J(WCGchj3B$Yf9KUCa{SPN$Wv|UW2SvGt>H`ncI_X3Y@UuY0l52><1X&0Q^A=4?Apt9dT_>%tMjaWo)zOe=aqkSX*d&rUHjda4C>Z!CIGwRE9z8mCIGwka-ANW@#AXz=;LSPq;0x8PqNalJ#bQ5#RKbDAikn*X!<XAFI6(HGYDV#>k~6?)v|6C^E!j@yPvGey!yidO6GO?G568Fn@`O2yJw2)GyLAoe=hg4!X{H@)6LIqfQ_!L3@;PVrlhUj<8r%!Y<k*)KQmGccryGMh@}|tWL{?wmSVt@d7VL6iU&{Tb^38Ne)REk*7QGhWt`C&?2V@Bc))YJD*4FQe$!)L&eH}w*Hce9i+aRy*}j~4ozFj!=xJBSvc0HB*m$vQQ_kWVbK6DMi|Z<9(N8}X_4u*qgX~-0AJML0(a&-geg5dnXM6ft&Z2KR7HyTY=$jwQ_HsSk=8~CPb&39zv*?2#i+WTn`drSUKjkd?R(I=8J^d+X(FYxiw#r%b&5vb!xgKuA_Bf-bKjkd?;K!mK6^lNXv*=Gbi@wcYc0o^n%31V5$D*xr7Jc($*<P-P+oW!LxTinmEc)Qbq8^z=Kg(J4LC2zRr@j4DALi}qSoA@#d|bBYZRuF_r!QYB<?2%I&D)ns`AW^b`CQGtIk_*(HgefQ-cxgLUe$9UN2$3tH|n{NPt@F-qx4+3_to5+bM#!ePu1Le@9Vj6PpP^0Ue<FV{?*)jf9Y9{PcQDh*ZQ(-!}-If&+Uorau#tej`P^lv4~qQmTd%!dql?~o^>qZS;rz)bu40D$0D9}EaF+mB35-QVqV80o^>qZS;rz)bu40D$0D9}EaKUZ<@oes5!+rY+i-sMnvp%RUCtuT1@qX`v50vci}?3q*+wqQV^zl@p8c4|s*Xj>`!SDI9gBGOV;-wI7BTO~JXUoq;@OXRtm;_AydU#;)3JzWKbGUui$!dEv24S6USi9h*e+)g=i)ezJspd<^<vpZu((HbEaF+mBA#_DVpYc?=5;LMS;r!tbu404$0Fu+EaF+mBA#_DVpYc?=5;LMS;r!t{aB7qFBY-w#j*|O^&Laji`Xt_5$A$=?CDs<ypBcud$DXIm*uglV-e4O%wtu@BIf;=$EuD+Jo_<^RUM0%_hTNbIu`Nl$2?YbEMne|dA#XZ#IqmE@#)1Pw!K)kDe_b)wo6!w^Qls-Dp`u#J}lb^mhKTHOYy8^DV~)q#j28}m{+nC&q|i!S;<nYDp`toB}?(FWGSANEXAslrI=T;6wgYQ;#tdbe0s4I+kIHJDdzUHv{or$Y2A{R))GpV)-Xzz)-!!rwvo#g*B(li)+bsnu0512tzooWTze>4TAygSxb{%8w1&}gaqXdGX?>#Q;@U&W(i%p~#r1=drS*xH<@oesX|2+SWt-w!JuU4$OIX^6rlq~4lBIoRAC_$dOM6%)OZ!bFOZ!bFOM6KrOM6l!OZ!bFOZ!bFOM6KrOM6l!OZ!bFOZ!bFOM6KrOM6l!OZ!bFOZ!bN%kk;O(%!QV%QnSlFKOvnVhKyn71PqQJ|#=f7?mtNZ|uXeja;_)Y*5M4^Fu8cpA9Nmdd8^b;<G^|OV1CrTzodDWa$~BmW$5@l`K6!)N=9JppvC$j9M-}-&3;m{7}nse0s6;EU^#EHpOS@Y3aM65|+LvN=x7MC|Ua6rw_|Ef~D`6lq`K8q-5#)ASFxR^(a~T&Pd79_d!aQz7JBe^j(jVrSFWCEPWrOWa;}LB}?D+C|UZ>NXgRoK}wds57M$6pI$6|H`Iq^o8ot)Qf!y9^d5^8d!;PB)1qYQy_7yI+jz0`o{5sB_e`{0d}l++(z_yBF1}x(Wa*s^Ef?Q~P_pz6hL(%(Eht%f7edR$cMOy)z1yJW;`;zfmfkn$!*Wb|vGl%ymSy|my8&tGy)P{n-%ToE>7Avt^qyD=OYc_oVcEuurT4E&SdL-oov5_*PLz_R_nk^uj(O=_rnK}flai(Pno3xXZRs7PwDb;=lBM^HN?5)Zq<4qX(z`=Smfj;OVL9fdcYe~+J3mU6-sdS{`5uwp)k#b5>L^)yZ>NN%_i)nEdo?92y$_>g>D`+WmhTHMuKfLW`FOcaCGW=f{c}ni=e_qz-iP;pzdhVF2I{}!o%}w1^t;{-?X!>1H|);^{O|a)>bI)jHn!g?>T}ThJ&3O~Hafcv`7=Hnl(#b#jC+Xuyg`2^tCF}1+y82RHc5Z9F&{FPHrD#Yx83dl`C%ijD+2%d#A<*3XZrJBi}PweulA>!&#U>o+MjAZujcb=f2#Ssnm?=kspj)){;cNnYCf;#&uTue=JRU)tmgA-KCkwtn$Jth{-<+zHGls9>CeW>;bFe_4|0E0{JzA7yq6N7-AdkFsn+=wtTV*iRN0)xNI%ja+MjHWpSB<a2>-joBZQL8$kx!U$(FF-|BhHceEQ?e05SwRgbXBu$WSs2I*e?K(*4Pf&>hJLvW@#Ue{X|N4Qd%qMnOlp|L)j!WDIl+tZHy}H|TEezdAmQjD?PM|7LLhcZZL_XLpq3e{cD4d`98u7%~w$5oe;rAQsee{}%DF#Dtop4kgAB8)}m{sU;~g6*?8R<B3C(&?IUahZ@q*G^`Aq-4nVeYN|sG8EA$~Lus2#hfXImQE~>E1)YV`HcHKb&cT_fWM8r$bU&1yhEnsO^T^&PF`dkZ&L<1VY_f<P2t5$CGsymAA#@>XnvNO{h8_&7eR1|s=%J`-Z`5!I^bm3oO3x>UK@TH`qvR5@6uK0p=cCjz=rWu+kYvdU=n9lR2&I-omy>#wIE*wwo5)e*NV1aTpgGtsA<d)(+Jc%6Lk-73kAYPdXFH%BsHq+`<e_=ehSE)B6?7F@LspYcavbzHay)7|mYe`R0W~$DhOa}v4y#VGmYf7V307^W;TzCzkP{JACzDg5ry_Q?BD;{&pr?^D5m{T4v!G{@Q*h=~ayImAMAj~3dvY%HTv!by=aBQD=OIQ$lJm($(2K}uGJ#AY--dphd<W672l+1ayW|40Gx-*|1bPXHkp%fZxg2^qnN0Q~bIFgOKO$FSBxjLppx2NekSXMc<Vxt3WFK+>`7!wk^e1F7If68hpF)31eg>~ECAUCtA=i<wksHWO(3?mjIhy>O+z!2+w8AULkvpJwkUQa(6UbfAyU1-gb30iNT~FF!aT4i*cEKu7?k3&PZg}Wqau2x=dLMjn3cT?E^Z{}&e!7o52z?M<ISt-;82T`I6drkqJOX_LUil_DgIo-~m|RGHMV=&2L!Ty(p_U8C6VNA6)9K{b<SFP=@XZDA(zDQKapqe%@*MOzc<X!QQgQ|K3UV3wEqQ^w1bvD89@ak~e}Mi0B`$&Gi_jP0vmd~Fe}euAXMTtyuR>pi7q2B(ksF~mlIzJU<PGu`^eyriSYJn8hrW&ySHkj5=$r86b@1vt(06d=1{`@0`X0P{E4i7hgRUdLAn%gDlTV<ZkoRGI8~G6WAxhi?%a5TSlV8H?caTq^pOVjDaToa<`Z=s_Cm)f2K>vXexC5U50{R84?k4{vUqZjc2;4*dMF_nIpZm!D@GqtJ<I|7c3*YsJ_NV{GND#U?&Tmd1gvG;TOZq52ls-hZpaY--=p*EDvK1XjA14FpZ^$#`cVt`o3_e5Y6Y$;k(Cz8g^eHlkZU^0tK1ZG>JJ1pIc`}0jk-SX)Om?C#;}fNSfRA>8?m~B@FOrdTG;}n5mApoFrMuDB$Zqtn<ZbddvO9enpIZ7ld{GCjqhsisWE`CUoj~6sACO7Zq#qEIegv<4N*wwbK5_aXJd=PXXbfjenuI3lKVb0%nM^;$$D#iuDLMr@g?<U|Or>f1FOsGNp6E~agzibF;ioj60i6NQP`V}E3%VDbO}C&k=`83hcxE#ip@X4=={9sa-IvaX&Zl!|fB0e_=su{8(Y@(@(EaEj9NnHSfG)t9K{&Dqx(FT{Mu*T*&{1?aJ%AoW4}~5|7sGl-dLZ;bl-LfIhd>XZBXM*Wx&*oeXGY@4Qs`26vWD(V$3w@{vGj1-K$k<8(<5O$hAx9HLy6I_%tEtt9FEq}CTJ7RjKh(mp-02R6X_n*hT7Di%``{bq3yH<)-l=&ZAFO*usjBO47K2OhvuPq+5w9M?Syv1%A{>{6?7Fw!J(7svCv~-m7=TZ8t58~!c=-3Jpp<G{GEY+*Fx9QlQ05%(r-Y&L666o6X+?>Q!pB{F$$+aPlMG=dMZ5~dOAj9E<J;O6Z%a$kM2(w(sQBb(hK0}1@uDbh4f5#{A_w2^gQ_TYxG<666huLV0sumf_@kJUHSufbP2r-dKtYKp1qWQ5Bfd$te*amUJ1RDHqsUJD0&U_8hRZ(*F>*}UQe%p2d|>nLa&8yR?-{jP0*X*gAQEtEzn!&t?)`G{W<jK^hTVyiQWdi4IawFGq*!;ht+EO3;IjwFX5r%=sJ2Q^iKHTcz9zybUnQTKix^Ypk46FT6p6g=som4c%+-&3%wU!IhlT)o&!CHo<;Ab579@VkJ1NF%bD~+=!2-~M0!7c1o{Ykb0)m>81ylmIU7fwggyyxT}02P-+_LIew#i{pP|2l{*L|z))&*Kp--d4d9eH~^tbTY#qi$mp})tOOL61{=nL@T<@EdXYUtJUNA!96GW|33&-9P5zJk64eF-JL2g_HWufUgAz^i|O{sm{Q!jU(iZ@{}hp+BZSgZ_;El)gsarhkL}js6wZH`2GDZ=uAsuzVN#F1;CEzlFXBeUH8mi=WdEpdY~MCi)Kj5c(lT;1+oPBj`u4`UU+v{TTW&MqnNNgnkD74F0|g{{0;KIsF17u%3Pi{gQr)GoR6aL;sD@xDTU1*?stYj*%dYv2M!Pz4TW!!Zu^SqMNaY>96S%bW8SYe70r}!gt$1w_*L*BXn~%06Ks@NuQ#F*mmqGx*dC#K1csRw`b4cvm<*NJ{k@k&IYsJ(jjaZbQpVqzDP&1(d<P!n*E8sN?)hDuvhUJ!(M_f#zM!kQS24EGpm8tus7(NbR3(&-lP-QJMhYTw2r-x&qVeXJTnP8iH*mZ2`mPUu@7PK5jEL+_|&n#Q-fJhi+v35*euRIp>g&ZJn<z>vQP1G@Kc;khE8VxhQBDA3V%#xX-3!-HVrxrp7|I3C*1<N1?$gJY$lrxoz3=SU($YT26P5XvVYJFn+2W4Hiw6{VRN8!aCUPX-50tqJT{PR#fCzMvTfO1wm(}4UC8FadN7+0osSX&V0i%a05$|ihqJ}d#W*trM-GA>1W%4&JFqA;%64L3V~4RLphvKSVLgf+3Oy7hhQac1=;3T<939J!gdT}AJL5<Lv;iL8jqS>6p|xyxR?k+jqo7BzMp%z$%c09rq6U`D&}Oy=yk5tSh91pYU@?iUgsz0u1lGh_p{*E&I%cvqXdA2ymSe|2kHIL|tetg0J1`0f__q_<$&SScB-tA18kWbI4t6~Bc#KFIBe52`7FJW(3G77Zi5QLP?Cb1g=*es^wl~{{od!LPoe59RVP`?lVkg1lr?AtZr^A=~v9sBE(DT>=wul|bE`(mlE`~=Jvu{Jc&CY>m&u14wFM`hwVVAP+LBGeAu%&Dny9|06y8@m&lKlw!BlaD5@cZm?=;iQDmR-fJg<cCEwBVYrhhEQq0<WxOH$ZP-SL4jJ>_+H~@X*ol%uUdnV3lJ(Wj8}_hKJhO&)BWdTj7H|ym1@!Hg*esx|Q7yy&YcZgg4ef*Rea{kzcYqpm)G4$FbGyROqSf8|)XXo81S!kF7^7C$TPQ7iwC??qc^s?}cwpf|nkEK7cc);K)PJhv2PmvNPBP&<ohP>{sm9><Q=->|t1+!ybh`iV~;8@^R?n@Yy-=-fy74!I|@M<QeEQ@Zu%xTkHqWAF%JTr`U7s570lbXJP#v_B-hBP~sw3J`a5!zWffn`bX#=apwCt@-p;gc=t;7Lv|hXI(7|vk-f@ZhrZ7K1naBWpP_$7iOXU68uT^xV|e{~_6GC~_E%Wkz}|$u39D<_U)WpFw=e?N!}ISz-+|Rn+1u=0=(`w!pRvEO_o45@-#>?cKY)I~{*Dp2jeP|Dh`on1@3T*!pI|iZ#3+0Q{R~#WWS_Fnp`T+k?q>gF|APLD-NWu@4>B6LAD@1aF8HoLw14Cac>LdtMefDtA@&H{JTf5i2pbT2j6KPoX4^!b#Ak5iQTS+E=(dq9B9F7JA_JiVBhRqkvLTUSk>9dmk>9fy*h_49<OO_2MScfg>;&B@GBol$+aWRnIwJBidxh;BsfoP8Y9fDuSKeS_B7enaY~;`I%x=)#B2k>FiHw7ei@XJkci4o;8~BWgyv@c(_JHmYd6!L$#3DvyB0g5+Z>%<ALe0qg@XAMQQsg~+>Tt%0I8Y~&#2GUZhsGnHz&nYE9r={mk<Z!3>_bK(ALH{Si$x|!rl8&_DEATjf~BCT$fU@J>>q3zbXtVq%#=t5nnA6fqlPpz9hr)f(<3vWGjRS3cy&+co{<zvOpELV-76BonHiDU(Ag+G6(wguXGLa4Hp98Cp<73`L@je7bD?u#+aJE(8@e}Yi=c*mq5HyW2F~sW-48X*L=E$x^CJ78<o=Nb&;>ZZMP%E^eCT|X-WsJALKj8`;mm@_V(4O&-Up=?K^H|1h-`;*J3@DiY>!$Fj2r|#2)5f|{JsYL8fqGZ8V-RT0;>f$dl>XE)N}x9I23wl<Y1IMJaPo|2%H}p*(tIFx&)<nM5!a8M@B~C%n^}g&}ArnFiO=!>my4eqj7Fm=&q4nP)lPZ3(dlIC&WYpv;j4ZL=C$`cZbyxIJ*M60yQl~4a=d+BjZu>s7MR61?R^iZjOc?9ce->yG5Fz&8R7hvpHxErN=}jL{>sq!fHHfXoa>S()hoXb#>d?4F5MJHJk~+uKkg(Ezof$0C&GQ=JcLA6`TpcuDx8R2WR|v1HXg#fAjB%iSfPg-7mT{oC(0LJ^wdJHJk~+?)Zv26`TpcuDx8R2WR}a8bA8@;s37R6(c5P-uUPB(^TB~t>1U~v9KRG>BXrk7WO*k_7Clw=&93-xxF6?d%4bX7WO)>#!s;Ld1k*WyHqU3SI5Hsh0nW`EbMhG##hwo#bSJQEbQev%URg#xEeqD_<^s|Qa<ry{_l$Vv9K@Rzn(1Yb<FLheB#O6-j9X7TxU58dmUHfCs_Ox?_W<A<Evv~U%Y=kS=j4XjIXHEi^cfrSlG*Tmb0+eaW#JQ@$-MvfsEt'}
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
placements=[('winnower', 'farming-fixed-drum-cased-grain-winnower-01', (-0.9, 0.2, 0.125)), ('riddle', 'agriculture-fixed-suspended-seed-riddle-frame-01', (0.85, 0.2, 0.125))]
def rigid_point(instance,p):return tuple(p)
def stored_point(p):return tuple(struct.unpack('<f',struct.pack('<f',float(x)))[0]for x in p)
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[stored_point(add(p,t))for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,rotation_z_degrees=0,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values()),coordinate_storage='Exact IEEE754 float32 after translation, not hidden deformation; native versus final GLB bound unchanged2e-7'))
base_mat=len(PALETTE);PALETTE.append(('SceneOnly_OutdoorEarthCourt',(.30,.28,.19,1),.96,0))
v=[(x,y,z)for z in[0,GROUND]for y in[-1.25,1.25]for x in[-1.8,1.8]];f=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];emit('SceneOnly_ContinuousFloor',v,f,base_mat,'Single scene-only flat court support, no extra counted model');FEET=['SceneOnly_ContinuousFloor']
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
  assert -1.8<bb[i][0][0]<bb[i][0][1]<1.8 and -1.25<bb[i][1][0]<bb[i][1][1]<1.25
 for a,b in itertools.combinations(names,2):assert any(bb[a][j][1]<bb[b][j][0]or bb[b][j][1]<bb[a][j][0]for j in[0,1]),('Whole instances intersect',a,b)
 contacts={};floor=triangles_of(FEET,vertices)
 for k in names:
  tri=triangles_of(names[k],vertices);mask=READER['np'].max(abs(tri[:,:,2]-GROUND),axis=1)<=tol;bottom=tri[mask];norms,areas=READER['normals_and_areas'](bottom);expected=float(areas[norms[:,2]<-.99].sum());report=READER['actual_opposed_face_contact'](bottom,floor,plane_tolerance=tol);assert expected>1e-5 and abs(report['actual_contact_area_m2']-expected)<2e-7;contacts[k]=dict(complete_ground_contact_area_m2=expected,actual=report)
 tris=triangles_of([n for nn in names.values()for n in nn],vertices);rays=[]
 p=(-1.5,-.9,GROUND+.25);d=(1,0,0);length=3.0;assert not ray_hits(tris,p,d,length);rays.append(dict(origin_m=p,direction=d,length_m=length))
 return dict(instance_bounds_m=bb,complete_instance_count=2,distinct_old_models=2,new_reusable_model_count=0,whole_oriented_triangles_and_pbr_retained_before_float32_translation=True,actual_full_base_contacts=contacts,selected_visual_clearance_rays=rays,not_navigation_or_full_space_proof=True)
LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate(vertices);result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,.70);ORTHO=5.2;WIRE_THICKNESS=.0006
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
root=bpy.data.objects.new('OneWholeGrainCleaningWorkbay',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole scene horizontal centre; continuous bed bottom at Z0; three entire unit-scale legacy instances';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
  files[role]={'path':f'assets/agriculture/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'scenes','assetKind':'scene','theme':'agriculture','style':'source-preserved-faceted-natural-ecology','title':TITLE,'description':DESCRIPTION,
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
