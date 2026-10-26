"""Static snow-camp parked vehicle and separate intact open tent: two whole originals, zero new models."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='winter-whole-parked-snowmobile-and-open-tent-preparation-bay-scene-01';VERSION='1.0.0';TITLE='Whole Parked Snowmobile and Open Tent Preparation Bay'
DESCRIPTION='One static snow-camp equipment preparation display scene, zero new reusable models. An entire qualified twin-front-ski single-rear-track snowmobile is parked to the right of an entire qualified cross-pole domed tent, both at original unit scale on one finite pale scene floor. The tent retains its full double-curved thick shell, floor, raised threshold, real front entry and two complete crossed pole paths. The vehicle retains every front ski, arm, roller, single continuous track, saddle, running board, hood and handle component. A visible side interval separates the vehicle from the tent; the offset parking position leaves an independent open entrance forecourt and vehicle-front strip. No skier, vehicle occupant, furniture, fire or extra snowbank is added. Unlike the old campsite social island with chairs, table and fire, this is a separated shelter/parked ski-track vehicle relation; unlike the old winter sled corner or ski/boot bench, it includes a whole enclosed shelter and entire powered-vehicle-shaped original. No snow physics, traction, driving, camping readiness, weather resistance, entry fit, navigation, load or safety claim. Original oriented triangles and constant opaque per-face PBR preserved with float32 whole translation; hierarchy baked and normals recomputed. No rig, motion or interaction.'
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
LOCK={'winter-fixed-twin-front-skis-and-single-rear-track-snowmobile-01': {'bytes': 91328, 'sha256': '56e4588b093aaaff5f07a20b22261ab8d747c6516515e2110276f1e56b13761a'}, 'camping-cross-pole-domed-tent-01': {'bytes': 37340, 'sha256': '919ceb5b8ed80552e3f22527d2a32c1a347995f88f6faaddbfcc5fcdc4b06c3d'}}
ENCODED={'winter-fixed-twin-front-skis-and-single-rear-track-snowmobile-01': 'c-rlq37izg_4wZ)_aPv+axQ`(%QAgV53pSV%As6>;DzGCF0cx_xVzv%0P)s%AMuJY9*NNyP1G1QFda4VHi^c>c*UO@HD2+E8e<akf7LU+`(~zJP4|v|e!oxti=VFf+WWey`n}ins$R{pcKso<I|0BiY7;Pg4Zwj*7cJaUQPbR9*HSTcOU2r{hPtMjmd2)vsTBvUYiew0Y#zN9FBv^^eO*IsUDN1!Qx=WhY*ranW~!pHVsl+nbA4k23hPzLimjCu&8xA3imAyQHCIeMa!W-+%?3PIvDE)tWko|{t^bE)rB<m|8kJ_HRcTkIDxJ!7rG_W9N=>iSj7rU{)T~O)uGCVMnp3HzEA?chj@Rgwx>2c{mAX}_+m(8%Qg<r#bfuB3G_*<st28PNv(m6C4ZG4vRT@sEk*+k8M{PZ-t??}t8|s?Z`8~~b@6dIP>+9w;HEwFCo!!{jvb4To?fSYUbu~?gG}Wv=Zf4#37QDgWGA;kIMVnfh>uc+L$t5-Q>sQXNTSLY565>nh*RG@TM!tMjuyOtRx~7#$B4&n&%{Xy=U7nD|*QF6Lo2!corTDsZBIa;)QK2+nmq9h1<SNUPDlmv|w@nQVb?axXL+7q<rm_XrSb}nB?3s-<O|`R{8k?Ip)NNQ*plQvBb`4dQR$!j_jSXw*b%jo%StaBPy+kXp+0vTY+Vypd>(IknYSvT10=vzwSzXsshi=|<0@gdXv9Xp4JH_3|)=Y)c+;cN)Q`2Uw8i$USrN`A5JqQKXM3H41o8)~JNfuZ%TjQqYjdcxj$eGc!q38;|*ay@X6c}}O{fTw8OV>5x(_YimR9E~Io1FZT#v*I#R?(d<uHW2Pe4lniO%_^TPqC^j5_L-Ivgnd@DP<OoS;-RGEV@8bsk2C0XY^Sl7;4p)y1FKOknnW_l`XL7+?odT^HnuXRK_YaQ2oY2BN}#yOi{-Q47O-v&GDP+aQttst39;7p|*KlecgKcBpOb!4dyh}tSW3g9WGYbzL^Y{^T)3W85}p%w4j!1)@K7`ZR4g@sAmjRwG~ranl{yi48&-K=Ir1wqoG#bb@NIbaGO>);`mcpv2j(?f;t?E*4M9I(zt2uI-C$R%UQ;%n&!G$jq4kma3J#M8b>CplBSiE|Fo3jXhs?>gXb(W?f*+9wRFl(rEGc9)_lRF?O3K|m~xIF`<`nks1k3sDQL6xT$Q8y^*M&2CGB+D+A7sk>PG!If-c{T_b9`4^U9?)E%golt;M`cL(ATf?wBdl)aCscsqF2TDcdnpnt#g4_R_M`rsG&TbB9${D*tXmZ`ri7O*&38l}@I#D7P#_0^V$XKv}teUERi6jZLv{+Oo5Es2h%{IhKQWsO9vKGPD%-DxH>w%_$<OryZ2V;XM4Vi?0p4?Lyr|x$W!|+4d|-739VvwE22`I%3|rmb)eD)Vh)FzG)kl<)B~7b52f9OY6xrj=jvC7gZN(@N`xxZ5ejTG&Fmw|7_zJkUt+UJ>gv-#|^yWruq%_E%lpom)EqkG}W)#)Kcf)_ToiL=N&R{(L(=;TexV+f*JF1dVos-)MEW=DWkUyEGV?~C~1h2ljnF%8*NRSv}ubrtwm_sA2Z{%ZMU_Ziqm%9q&{AgPFs^{+N7K-mu@q=LWtL*oL{#ZSI=wHh;g4<%vMd(s@2XrjoT)%r<Q8>o$4`LB_`F{Ytxu*>g0jdwRYdB5wlgDv}&~TPUE&o{7AQA-D%N6GG@!foAg-21G_4X*#Y8MdityAK+NaKAYNu@aXJvXUXIx~aW=y!tMPV327|brVZ~`Zf8rIhRpN36?{a!^tHo)7m@N}uGxB`ROqOW6Ey)nCNt47SGcPWgMu};MGG!677sSwJo}o><L@x>wATirbk#?Op4#s3tVm6;{Yu-xcHLpb&R?BVPA`iEf|8Se7Za*y36SH-Tv~IVv^&oE)vuR>>E8pyC+O!esZf#kpnDbmRklXR53+kL!%x(~?+eUkzwe~bj9&+0%^I>aG`(#|V^Tu`CiT$*-r+xCYr}Ccmlot1KYe(}bV)vBM&gNSai!s|KrcYUX+o}hyJ<ZakWxS<GQPMMJ%OsMg@*=rYYLecXLXEkkC4t<@3*=7e(IuCVjoBhGs$=mjCYcu7VNiz{)Jer^GCWxvvw31wC(o+sWC=H>spoi&rio$Gd4^3#S$nl6vSYSNjGMOF)vCYdiP<W#Z@R<-dsJmb&1(Exb7NDs(p8(*tf^~SUSD^DpGsTZxM5>sLtR75At!CDlQSy0lw6H*v_-C?{G8f}xg4Welp{BDnN%xnCr#V5WOmib$~jgt?Kp<x$edt(16DCPw2sQjT9u~h^1P)Rnyovgj+eCfy{TA!z^v@{EA6!wq1USG^|0%W*6VG#jL%)abk>adGnN$9V5obbn}OQoJv+94)2VdIFikxv)6%+?&CR0H4BfJEh?p#QAyWR<gqAdoq@$rCsOofG^Q$q9bV{@R46l~U=B6}Dx2%+rlC`95U&krUaMGz%(kh`#v-F*)F1OUGlxsw_Che%24AnqfJ%(H3tI%VrJUu$<%QZbo9z;94gJoNmZD~myXp&Wioz3>^b~2sR&7}V%TAG#rc;-EdA+;optUevnO6sY!j^>k|m-1ES*tY3dR@zFHP(?bzy(k~=q}r);nQKyel~!ViNRe?(H?n(mmSH6wBjs<CXxU92Gi8~nw7gKdRocvYPAYBUD5d2;oyC=CPImvuHj*Ybp44R}nvwL?ZrEwdbW&-j)KI6Fz7gg1hFX`Jp_kO9`IY;oRG4P?+QcW+a%@d+pKDsCKP04d!^EfAEU8VaT-UU}dcVRO^EH9~mBgbxUS*^$Ut^}8)+|&+DK(_ZbSmfT@Cef}vX2HnS~i+A)jpSSG=J2?VLxTsNy8|mi*iRRJ^9tUgsrEuu?NRoJDEzg$0uyte^Y~F=@{NjM=PNRT`SKgbp7k_iInO1H<8B4q~+-C3Se4QGUba}4o*KcqohmdM!7Cwe)TTlr2Y4;XgKq+HKTnlfrG8@R!OWh9YGIPnJy7$Zl~qHc|@))^54!Omm8X?XV(_Gh9{D?ou`H3DvICVBE2EIKuOseIz-8}hF<2xPIsa!!N}gQhSOF{)6o1<3)x9W+Z%cONkmo+!8wDfA+(aDmH)O6SxGuuNz_G`o-R)jM)Ipygk7MB_UOSb&_f9|7+RTX&|@qebv@fR+tiH|&Y1kC!px3{I5f%|kxxZ3x84cft&^t)E0vwRI}Qd_NAuO7WoH})st-p=#~)u(x<%hRRZ0y;nQAa&cthAN#8E@IBEJG9SY;|9#sI15^0tfK;U?E5nx6A&$JTL?r{zaU|2i}GUa(-$^P@rbx?EMMbg7#yb09QIO&Seqa;@l{d?_>U-DWzT!dOQ~axKsAi)%2lVYT&1=Y~?{U8E!2g)-k#VsWcE$x;h4v&0ajIdrO(%a9PyPZ?Qv!60dvj_uEzlDWj3W8j=gOB?x<@8UX&-uvfAR^9g~I)PWJLXU7C$_k9K69s08amY@R;n;ATZ1libgmWlAk!R%IRIA|{RJY`(iK?`0ma}#GMpY^2V$v&7WjL5wIBxmVnymJ5<%R}9vy@VtRl3v4>+KRgm@KWgRE#i&Ppeh%&STxmK6kAHQt{YE)n?kcu{{Xfa;l#@g|4V+w&qu%nRLEa>R~pW@`f}s9VeD2F+ky>RI?pin>c>r(bSSQ#+)QBOmGd8mbZ{f%2lv|Gj&|ES;;)-F)b&pr!?J68R$GXa!Ezv!bijSB`=qMl3MWdq_$zC(3fnzROZr3mYD+9%FO{=appug%Xc(K$B{@g9o@;!XOcRu5OF4_p@(VGJ1pr6_`Di8z~gh3uSOd~rIx}0D(Rp?ovap9xHi(0wu#}vuT)Q=A#4rLnz-PyOKP#q36W)%twk%=rUVXHjvS3lCpV<yU8Xe|5^T#bQ~on%nfNr~!qYG`3;&SLpI<xZaOh}wy^bqv>3Mi<Qo5*Nr*ROJiFB!LeC%-wj!QP2$l>WyinPmAWT}zKrXxB=LHy6wvCn4G@2)QOV&kJ^n3|FFmz@?mnx)|c)Jo#2LemPK$t3=#qfe$CGo5uEU24X_EAX<E?vHNxCplF$FofdtwB*oaIi>GHd40O<jhV=KEvd(pAJ*`B!m$T$)ZYipp3-qnio?7=do}$jH;&AfmBzp41x7tPJIn32_}drxpR6!_Q|P&m>f|PICDdq_nborOsMCY6&>nAg5H`PP$K=2^%9|Y6F;-?FVL47<51ko&1##Ujb6sY~SeJ#x<TznHd}2_3RJY4quGvo614ufKBNc_@I6*yhR#1LSPn9_{N|ik`O6hTuX2k(HPD~G-6nqsCJyqt^C}qZa9E-wntdJfyC-@5Dd8*7IDHUVmF(j16h{fT-{40pXsWNvRQ!z5>IGR|6>7TS5QZ4xo22_LpK~PP;*~3iAfUM!GotHQbtHQ=-EM=k}q^0NkevriKaFj-G!|_UYjFMwYnQ3$<S?-wPl$aBxZL%$s-9W*o!NLI~ostt6bPPW}+d2lO+#8XstS5w~Jc{c;TjX3!cW^Y;jqC??&Abh(5_)v>(s!Y}-Y7c{=a^9y=`XknGO(yf&Hu!-g?hu$$?>=C?CdUwlayYi<)`67QkrR7&&z50ip*_t1e4BEinPj9q#fOzitZq$5<=AY)#xBqrVgAqJDu6C;Q(Um*&D{^#@C9S!UqEHTE^XEc4FL`U(Mg?EUE&-wf|7!fM(gctydQBd6d#YnFCY0?13q*#Yte~GSEiaFmOI><$^lS6?NVJOIq`{2+=JxjQTh?cdS&Z@ZG3ce{4-y``e5-jg(6ej0`x-)cv=oCe!jwN(Rp8Q>kRC)DWN6%haS%wkBiDn8K70OOfHW_$u^R=A0=VW6l)z1qxR7O;y3$Le20u4-jt(sUm+dtYzQqT$BJ%-bLJL6V}&uJ$=i!|90<HC$-eguWMM_;(t+$-2RYf7Oh$1e=(bkc{NRIC1R+y^|sDLxHx+z>h(BzaPqIm`LvUNy`i{XcM2|dQvQPxvH7CQ<(rP8UoN$tcXjqn=k4t~u4>J4`fjK67@9ZDWWn`mJ6X>4nr0?rRA9;+Z{GE~V<w}k&#?<UPv!$+*uMCBQ;VYjz36(Y$a#!-3bgb>-;Zel^Z=(E4LF)z*7fP6QI-qJMU`Dn1vtYo%JBhQ<EP5H-muNG9wObel4e;ISm`(eaPb|aVvRz@*E{}@-tJLMPivZ9*7dPQp^)osr@a2BQ{_Y;ob%geS=U>ZUe@)FS&se;G@nz}^`=&q{%{6Xmj1MKx-9+ax)Wyvu#-g<SaAm7kP2|U8$*MJT`+>+g3^f*$8@cz0$YnS1cg-K7;$V^G?Osp=bWP7K}t^+UZ2*Jai)QV*K4t&fUXtxUpMSz852oUx5^rWOx-DK3^EO^tT9M_j3?RtX}D<=O@rd8&v42LA=vpiA*87L*nhj6?#s_WmDT-NYbbxslXtxpYY`Q4eXKcLk@_s#bjnypm{uyz!(V*8Z8>H+gGVZs`HHWPH;FGczvGlO0W#BCd4o^dEN}2hr{WAgh3;b|lV&+%uazus{)*H8WU`#@+hyfXtYpeAXY8}IWLblc6>k9-a=opWvwX3%bR6>)UmtG)S=|443&@b`(|Q@P$1-&-M(ol2IA2gftQ<yh1y-!sUo?BozSpLlJFwGn#*dH+94*!ozPN(4ZrSBjVB;84&O>NxR#}69tvO~HPH5|zQO*R&*7fpkUpLcsIo*%9ekyL>vC0`jY(pz617yp+nsTl;L-Me#`w_Xl2vUKKW48PbqS2#ApZz7k%y|pJFpLb~zpJmR_f-7F!dIq!`TS-jciHjc^sBGhq2!4lHdep!=9x-<>d7aoSABl2lBYf~#2s?h`AUB3$@%V@H5Vv3`PM0|@*H1%)m3iLF2|4l`gS+yKgYWUdTyWxjxS#Hm>cMmW7LBi*hR%_*1Wk(#j?)R9zIdYvTvxbohp|1xaGa~rmI-$>d)Uhv0BAa=li?gQ?j(3Vcex;=>vg0$I_RAb~%<l8T6lH>Dz%GIF`>ypihqFvliHeW378-bzonP8wSm+zM_ANlAWV>RDb-;Rwdu`_}$ezhn=S6=YRe8>eCjVspRM0t8jn5>}(}V+l}jbj*=g`ZF8$U$3vdKzzy2vc<-yPbA$eKEH>Td272Il)VX)Nfj&8Y<e;CmK94F6?8~vN^W^VeqGZ{(`KcaCmiL&t_n`Y#EOqtQrH@QkvDEqJi}$Wpv9z6a^i(BF9|+_*mcA6U%dzyyp#L08-wyP^v3y1XeR3?HHTpb;uuI}5%Oq~HOyVZXByO@y;wH-^Zn8|`Cd(vlvP|M8%Oq~HOyVZXByO@y;--=V`*KX;Cd(vlvP|M8%Oq~HOyVZXByO@y;wH-^Zn8|`Cd(vlvP|M8%Oq~HOyVZXByO@y;wH-^Zn8|`Cd(vlvP|M8%Oq~HOyVZXByO@y;wH-^Zn8|`rji5ua!leT%Oq~HOyVZXByO@y;wH-^Zn8|`Cd(vlvP|M8%Oq~HOyVZXG;W5md|r3_W~<kDV;6re3~-8<|C;?*b=rFGUmrY_$(PTU88z%6?=R2o<>kxg%gDb=xqSJ28F`(&K3_gxMz$~ekuP5);|4Nq^1KYz<A&AKcHZxg2<uPVdH=pd*nPE~_w^&f^wW0U*Ru%IbK7~}P9n@+IT=?alWWV(mk;f;$d?bjcabk2szZ@4A8HGcFVD;5Y$_Pv5X3hG<70yOm|%QW5MLFH&kN%7F7xcT<k@jU?Bx-Ac^x+W|Hh^rWAA_8*c)b35y7S+f=xvPn~DfF6%lMIBG^<!u&Ib(QxU<YB7#jt1e=NoHWd-ZUJ+sJ6%oc>5n=2V5yoB-VeAzV#$FL&>=hBlUJ+sJ6%oc>5n=2V5ysvQoBsFPv}5f3uNr$h!*{X#E_@pn!aML+EdL5ipc5>HrC2V7F7O?=9zMYG19%U1gKlsmmN&w6a4@_NA7S|sEJLZKupG<f&>f|3f{(HM7_aCGJ>mOUejjdtL*PUB1j|q0FqB#jhhup-^g`*I;ZrO>#VdM1AGig}Ti|<eDEtlnj^*FsNR&DpR$#dTc1P)3;d3lM$18e6Ke!Fc+u#Rq1bhZxVEF|cjZ!OMC6+6pKT7`y{)y#3@ru4M0Peu@4)`G)1^<A5VfimO2BlWQDlAvQK$QM5e2L|kc*Pzt2!4X)PvCZ_fq%n)u>23KMyXX$hh-fMLFv07k@ztlU&3G*3U_09H{1!e0EteCTIiHmgHm;{4$F10CraM~ofCKAkw^@Kz2Ijs43D3}TG%boC9xK|B<fLW9UO<{aWDd<?}KiMd+_L-7!D)hei)9&y>KjaO>|Ej3*8gzQR+Boz_I~Gqx4SbnYa&+Zi!Ja26n+HJbn%vphu!tVgvL_G@?`k9FOJkFczgf=#$uqN6$nB><zzw3Oq8f5qc+fPi%zU6HO>}JhWih0^?EoLFkw8@aU5m2NU3zFb<Cgpc(om_DD3t9*NB;)dDAAc>+vC>0iNs#DjSBOY8%a;1SpdkB49r^iK>*Y=S|FlThjeI2p^6p%SGZg~5qm;V~ewFI2(furD4D!-+63F*I=^3{89krA~&eSZ;+WDE$NsOFW9l;KXFm;3=4l$78Ssh9ve%Y=ONJ+fiyOoPy;kpriD!VR+&RJccEbV8U-9iN}+$4fafoOl*UZiBnPP6gUmb)4)RMr(sm$*LVz17?6VBfq}<wU<Zsyj7jW(F^Mx!>NGeL%QL}2>1UxL@iZQz5;mma_h94k44e+56MH94hrJVLqtuyj4wmP@G?ac0#wDJ`qaraCro$g$Djt7;vtVpueBvw^pEwt#&Vlo=JP%xyegP&Vp2K5Yq8bFe2-SEz58s4+5)%{Ogo%msQR+On5X%c;21>sSlM*lBF(I)Z%!EI|et5hD7r?%W%ESdwnYak0E`&?4yae_~>HmSM#LIY0O3Z=-;8mD~$189#OioNmTntkZm!i}qa5<Kj!yJ@;9kj&%;8B&B4RhhoFdL88;4(-i^u%SLC%%PJm&27<UI_=H^qXKNUdKaA%!7mAEtrSL8*l{}2`h00Sc$7p>Pol<%WGf(O1}-M#G81SiTRL#YhgYfe}SvPPP~idyRZnQuE7y&0Un)D`a3vMy^TjI@y2ggW!^j3aYvnT+%Aq^{D)hT1NnispWtyE$g5b&-#hY*);hyj%9r9mp4M5&fxL>_;y~eAD}T+!$cPXbFG4+DgnEQ(4amr-`XeIrr>LF;#=D+a_QW{Z2V>1(EC*u@0gQotvFwYnr>h?&y5i9Ty>EAn3Z3xij?u6ej`&^h=ntrKm-tmEqwPv^AfK~iC<pQ?mh!}}LRrd};y|9(S;&FBiaY#J?S~J2I>CSM!Mcmj&#3tG!%lGz*>sMQmppKVJHFo*CI8PMx4J#wUZ&(RGw*Q^9lDQ_t)uVv_pMYc<*S{oN|x=u`OaxORV@4euLa+mu41W&ZvFLY6-#~I`q2_4-}2VbR(X!!pZsif&@RV!zj97>(0`7PS!PxTdf<3x%Yf=YpBzj1z%Crib_4rzEc+k$3CB_ofxj{A62E1c_$|xCZ&@aO%QEp>mWki8O#GH*;<qdlzh#;DEz87jStfqVGVxoMiQlqJ{FY_nw=5ICWtsRb%fxS4rhXg7a*W<%pV97V&ws<qaVE?8<2;plwCOMItwU>zWZKRHeA3wxcofOBod-Z!f!7q}(%a4hV4FhrsZb_&-c`xu>T&bsL;EB0<wNgF<jaTZN94=%GC4hm$z(`9nXr1=&inoG!ur#8-oGy|?7rI0`}*<1^wV~}l`~8|8I??~KVH6k=zV$l@}c_i^5uD7CH^cT__K)M&mw|9iwOQKBKWh2;Ljq0KZ^+dEF$=`h~Up6f<KE0{wyN+vxwl&B7#4Q2>vW0__K)M&mw|9x5`Wd2P`Zt(6Q8E3YJr#63a@Mh~-2WkL7q6i{)4tjpb+<f#nF;6U#ku4L1#sfmja2)!Z~ZcE@seT;WZ_qdS&zy*CYyPT;}}*dNRNVGfpa;6N-7gaug2{DkXgR$V_|>iStw*UxRbe#X-E^N_BeU3C4Nq3dS?T|d9)`dK^I&&9cZhE1+R<xL8hjw{rzFcZs}uph2kd%yu$9ssj&?b;jWVmTLP`)k<wSk8xeelBzomW$vZT)_^8C0H(jg}9C#2FtKq1_#4X7!HSFc^Di5d%;LJ0?Q-dP>^}Wqp&;*js%%AJO;~S;Aj{J`@m`}S3?a<fPG;NmTRCECc$K=$Fd&QLKSGR0m}_=EXe%ZMl3hNdXTxbW-Obb5p0+Wo3Y#sO_0X*cQuyPunEq;qQResKXHARjEaYKUhZBuaW^G953O*&eD?EQDz2Tj(x2C<SjzwA@4r*BZ1=*G9#*pKf9jkEl)U5eS*`LM*Zg66Yr7m<M^A0-KgUu&&;!S^-9VoVyTmRm6T7fX?7}j!3(LeVEEBu1Ozgrku?x$@E-VwfuuSa2GPO$>%dxWQ)YIJ&bFw)Z<V=?H=LS?J${ZDCg{-SkCU@Rd$<SEbCLh`#<=m3W<nAj>CPV5eIVY4l2<uPV`BqlW<v5u({qu7<#$F<Vy+j0ii3s)*5$q)**h@sPmxy355y4&}g1tlpdx;44YLyx5&nw3I^NO+lyke|BuNdpkE5`csin0E@Vyr)}80*g~#`^P$@i<GV#Ih1+F5~ggvD9%!Gae5IOUIwVOv9PMcz+Hu-k*nz_vayUp0E#=`(Uh=^Mrk|+!tfB%x+g<S%tA#?!9VQY8b2KzN(3(iLtpa&I@cTZH&zWa9)tcGL5lX?sZPbayrIpxsNHZ6d0w4<Gf%Nma}jkG7{$nv$33wvyw3w$H!qg4re7nJ}q-yPfx`%k8$_K-IXl!Ap@`Jq-2>_x$1_GGb)z(nf<1|sAQSvxqZ$9N|y4&m))#n+3rK{U8rQ)|N1*mR<hK?ThFaha#o*5C|Tw)0(p*QJ|t+DW0_Y8`p>b<&jfnlSmt>GeR3@21G{i6+YRi?vFv}~Cmc&X1pdabOZ=8);<qdlzh#;DEz87jStfqVGVxoMiQlqJ{FY_nw=5ICWtsRb%fxS4CVtB@@mrRO-?B{nmSy6%EEB(Fnfh%QcjPlW@|hj^%#M6!M?UlaW<E2>3w^Qe@r;UPzT(d_A5*f-dmQrmuaqqFCo)c{Sju<5ZKslDyC=@SPsy_XtNPumWSOrB<T;jkkDy(SW&R}SKgUu&&;!S^-9VoVyTmRm6T7fX?7}j!3(LeVEEBu1Ozgrku?x$@E-VwfuuSa2GPO$>cjUo3@?af#u&*x<7UUmJ$Sm?yEZ2P-e!M`*a{c(^eRGs7*P&fDx=NPo*+2eVSF&6eU-;lSB}@6)j}29_Y<JH=eUvQwzx0XSlq~g7d&@sFDwg_OeE#2+EZ2R3JjZhV7_`f=T!#kz=UA?113hpo*TsQ8IhOK)T{xEQ2KMDx_CN3wj-?&~e`DAse#<iPTb7C6vP}GzW#YFi6TfAd_$|xCZ&@aO%QEp>mWki8O#GH*;<qdlzh#;DEz87jStfqVGVxoMiQlqJ{Wgp{@;@E<pN{-bNB*ZH|MP!4|6?7!ucu<UPT%(z6O}C2`>Xm*P_oP$$T+29DZjI2tdeEBpZs!+l4bwj9<OG(P7mZcmh1hXU5;hmAm~5GQa;cF$Fki(pA5UiE-VwfuuSa2GO-KG#4aooyRb~`!ZNW7%fv1$6T7fX?7}j&OBi?Le>(C%9r>THKmYT<<L7uPmg~NsKXkT|<@)isN6%2QT!)@Lc88MXdiM28HY-`Ki{*E9s#wY&{M{8wmhJBS-eM)o{vUP293@LV?EK*jB};wYd96^gT=xa?9Lx1%&@RVv9UAnXW4WFU^uV!P7YF*}Sjq=>;aIjC*q3A3|G-Z;mU;;MjbWGgEz87jStfqVGVxoMiQlqJ{FY_nw=5ICWtsRb%fxS4CVtB@@mrRO-?B{nmSy6%EEB(FnfNWs#BW(9e#<iT+c56P|8(SkI`Tgq`Jayb&;RZGkFXj%70Y$Hb;SlH%k}<-w~kY?%p1r!rD7@n$U$qBEZhChHFZjs{r}|OwMv%j^gy0tx!w=j<yhtog8p+X<pVu%EZYtA$*@c8!ZNW7%fv1$6T7fX?7}j!3(LeVEEBu1Ozgrku?x$@E-X{KgmFjyrz8K<k^lMn@;|rFsmTny{So(!cl)~vb|bJaZy4Y76zoRe%<oTpyR}Y+-3aW<(>g=gEyW$*ho=5MwD%6aH#2d?Z_s|-G75GhurGh_$OBaDM&L}(=U#8ElVLXk`|`BT5Ozy(hyO(LpEKSa<0;sUz`p$Lb2JsZ5!knHP$$D~1oq`=ogwU&;tu~&`%iVxpJncT^bhW56JDz3xaV`LOL8DTam7lH<3L`;Qa*k6Us~%7V<}&X19@6!AqVm*?(iSA|Ddj1;t!#WIxoqAd`|zN9LTF!$`gMGWhq~Z19@6!AqVm*?(iSA|KPvO?Q>rBe{)m8ZUpw_<=R=nZUn}7*H;8}GVDfRU!K+(!fpia@E?W$jO&`nthn$&cg>pRLcwkvmftOX>qpO&<QLEVcVvF~r=8v7t9yzPoQcC&e}=ThGU;<k7S_?Z->>fxmEAbJ<lgVNcV7EJyZPGw<3xM-+zV>mn>JRrmox2U>_dk1CpMFNkHynoS(L#z=KpqZJJ@Y6zk2dz?uNJi*=`=;>?7L4Km5%y-(KzHOnVvokRknv&E(!=@#H&4WJaCwuD{lf$Zjc?d7FFw_U~BS?Zd%B#osn6a4j}A4rfZS%t4X1A~ET6C>O@8j~cdncO=i=b?KW4?*{!y@9Y^5S93Ct&*>y?eD+9h#^sx<ul(yE@l3A;-mB+-nI}(WE`H-!|N2=MJ>gQB9-s9T{SO;1ZvEB(;Z7VW8m)e!TT^er$;)y^r)6TvfBNKI%gJ2wRv&Nq_eP1e!~2Mp#}D^DxoLNC!+U-6<f#m{>xH#TbuwV~VDGKd7kKw~{zG-4e3%ZYytrqucl+>#-rJil-9_aWR1Fl>A1v~2e&y0#RG;?F!QzVv3%&n2{d`vEREFwprMKPZ<6gFQQQhA5_EhoP7plZJR$sq!%<yXQqvI>Zwq+0O<gTUqq&ntoN9*LSrM7tKjj5jdT$NaMhqv?EifZp#y!PkwzrT~S9hIT_$3A;OpZ84<^t690^2VS}IQ?_i%Gc31Z}lEItY?PWXt&M%yp!%a(5qO~n4$F-+BEFi0V6(eC!s&wv)8K3$#?b_ziOWEbze9)L+#F;r}lm6<7QufecWp@)JDCl28rfnwrDx>(aa0CPY~Ol8X@ku|D_DIHFvH59lN{Ni%u{7F7LO-xOxih8+L7Sa)0lZ22EW3hu1UbJ}}A4{BX4Brazvcw&u=L`(mFx(&tti&HmL#nNzMi%KO2;CT2LhaMu>ju>*T?b#n65rc{QrHPt_rr?%r{sGd1nbMn*{RED(?(HoVg`k^xYVGs<3-Jw60J@Iv@|ILI${ok7#>VJFTP&ghM;8@s%ugAiP_<AgS17DAY?f7~uoQAK*!f5CW2^fyA3E12J?!*ch2VJ2O`aloZ2VZ+Y68b?em<Ss51_SnhzEFj)eZld6*~fx3421n)FaJBA_rr1obb?{v!bsQ?=3>qAn+@k;xzPW<=!0MZjDck^879DDe4PMCfDV&jDI5;_!U`~93LJ{BQ(zTLg%qrW8nB@rX25i)#n<UD8%BYEwQvAbLnF+AnQ$Dw&V*)|4+p|VXo7ig0vrO1{BL|-1Y6)RSOS~jWH=bM!jZ5XPQusau*3fb=525a90g~<I#>;-;_GVI0Q<ulI33nQ9n3tYZr9vbzi=;n@Y87uu8zY!pS!X8<-NO#QY;=G9+|&*|2X-Z6Qy`p9LD;0k+vc+>3>O{dCVJfToCg6c-z6%?PZ+bx!;=AtKIz8c@x^jU%dZrHLii%%e&gk*oO@1Pi!Xl-fph$`P{C1M|Qz+wx8Dyu5K@1ebq2`+ADqA%@6%<QoDGsDKF#mKDE8PtG$eU$dLZTW^(VbIDPk{yKsFYmfYLW9<FXLPh8R0ZC=;E-MsFuecQ#;HvZawHopSi)n3N_WJup)GtomVma*@tCwq&zubvu}t4pzrWmh)r5sUX5Fh<Ei?2Ey>;;@Wmq}@nN`X9=LYwG7mZ1?(ndCRUH>t}lnyZ83CJ$Jp!$xQjdJ|g*!?OoUD8}41dbH&R)?dpAW+S7UR^t@an%Cl|j#H`GjC+{tmm>;;)w(TW;yJ@EQQ_r8dQwH}EoV+Zn{!uHc{_$s*%5yTSx=!+L`Q_)XGrOPo;`x+!QtuzRul#JUJb8NFg=M~84)3(P?1LB9hlf_}?af?nc)zH<&ZWAd*HT^i>tS4<$h8T*w(m2Q-V5hU_a=OlEYf+{wN&R%K2s_7Jbk*?>i~P#cTcSnW51Z{9d>q-mEmmh{0G@};<sP;=}u~k>$@!y4_-D{JoK}toz%gL#fm2eiXYwg^!?nmROf#G@o#v3I%i*6KX)y)-4)#ydH19Ilk={<f9}DHy>-~1%zaPa%h{L8Q#)eaUeIUG7Jt}Y<z4spsb0-1)-KK;Xg$<MlK1+{c5k@$@=mVK;g?r=-|RijyXTB9ySQs>Zkr@-xwqO|^<kGh`yO^>l}PlP=KbFJd?)7vR0iwwZ6xcY_L>U|Mf0zRh$G*BcjwI1V)5F~28uVkC3aC;bJynjDdc%-FKSb+PVU;rzFgov@$e9F=^qliE}pvB8@Y3!NPF+?q_(Cu<z%G(NS|A6bkA**yvw|5@0QCx+sWC2yH>uw^wvq<oqHagp*FhilRdph=S}h+|J6$wT7RK^!>+yInLWjbF_XMM-SBeeH5e{Vo3gJrZraNkYIiC_&r|!7=h36~vW}<_ukQDOd(uxvc-vmC5C^>Zp4-r8q(|+}T`OPF?*;n2NAi0fwH>XW^QFRif@?GTRCr@P{j1xp(@1Y#daSpu{(bkLts^|@15}3d4e~sC)OOS^Z~S5}Z}{62y^9|HQ=W~uYYTHMf$g|DIeBVRD#O{G+Jeec+i^0~Mx5OX<-_btZ9(NZdr=)yd8!{O)8GH~Dw#(b=I4=y`FW&aejaI<pGO)7-+^o33b+AZuYm92>lJVdzFq-8!q+R{C-`~=RQP$M5%`*biO?Oo!rrhCbb%>;9%)~E?ExnAgWgaH2J`~k&m(F6?_|i|#2D!R8pi<tcQA(dzXdiF#y}_73-*IiuqPY@WBp&nI0(zdFagHFLO2-4!{LyGNpJ|hPJ$I+!DKiTj)p2Y22!BIk@%`Zt^aFSt6>dHg$-~32v~=&!p}|3fMa1E%!C%04|AXqU+2Kduml#t32+iDfE{ocEQN32>ryxij)LW|9nOSha1N}5Bj9v=JpwL-I#>ng!39tQ--7k97B0ruwa^3y!f|jJ91r#IZD@uDxDsC*;5t7WcP)GuHp5MD3T%Pv@pTK_3}?VrxDkE;+u&9>8%~Aq!w=y!xE;=ibKy3)1HK7&!R2rf{1{&^f~#O7TmpB()o>{^?y;LEKR;64^FpCwIX`~t$<viAePheOqf4@3G`lLk@WD@~SN9yE<a<Y+QC*60y;E%%mzLy*K0QpR7~4fYMaiSiI8MHwoaGO1emE28Q^kQkRUGKE6ia=oIMAnx1AVGE&}S)@`c!eCPZd*rhH>HNLF8DK9c%O7x6^hW;H~S|ddqfuq3AO;ZRh#-BVGJ*lXu&nug^q%&r+K_FSB{WRx#wMentIhJI}u#Y5P-a#ZTrvpHa!kc^%I0ynK0HhWmUIqh}F8&mw}JMFc&I2znL~^eiIiSwzsYh@fW?LC>u+^7p7l_`i~w{k5v@xnHLm=>LLMrT^<x1ChG>zgMOEzj4()_j^@Ca=&RMf455h0+wX?3s&+su_VjLnZQUbe=lkbM$68A^zDpCg&)o3uU5&3DSxj@{%X}EjLf|;?#f@SnvAizAI4(2$CJdkIRIm^iKU6LS<VbnSf(&y55-8F#xji&dpO?DNGwNUJe|1WgUr=e4Xc*#Bjos|jW3tvK)&a5yRjU|t60k4K4*s;)EUN7z7z-Yw9Y~f<W=19zDo7`Dto`VAk(Sy6Yko#CJ7bKvmSH@zL8|PvFe!2l?OcIzPINTCBL%yG54yWCd&(-eKm9L-`2XYql=P<E?@5cXj@N~w}1Xl=BJxCyJz0rUCFbauXT+(`>-r^bmB1+#h0H5Z{6clgm-Q)FR}k;nVW`A6|<i~f4nyPIenDzP)3xH@#~@IQQkv&f%19vl#mJQkB9Oe%4Zb)DU=E7X{}#TPpC{Me}wCVM;Ct;GXzUHb|!HA>xX4O9P_&Sqgr=7dP$GN(GKwFiX&zZ9Nl)qqc4oVc7EoLbq~5@UcJOsapu^k-1?)gW_j5OHJP#f9&x|yex8!`J)Ut7IO9^5U!3x4=JlP+-HSH%5GwBUz<T%Ysy-}#{Oxx$PxLy*-QKyYlHcjO*}d_>9xO{+*gsk7z5Tboo>n<Zj63O7ck5H*yr*}}6_>zWnN`>B7RU&c5hY~8>hVy<MHx>~Poa!o53L{NJ(SO&d|rP_$OQdqJ+J6bs7%85!vr3keLozGrF?fpC-lpHSZ4ijpdZVJDEzSJkg1uEdkhxm)P3Npc+1)$V)yGh363v1b!Fz>C-xFUK7HR+@r;Qh#P8os2#%Nh@s`ZB`cK?DANbN$@g48q<yI`{DL5W<!OqNtdv?0}9sF-s#Z!;>+;=YPAvl({xai}5?@D*w=3V)AS8>;Chl=qpJ-4gz{KLiDuXph}e{@E5PNo`VL<yO&dOVa7D6>mZPoa!o53L{NJ(TxQKCeF|WP<**o>%lIRA&6;S7#1d^gH*AkszY-mZzR|r%&m^^0pUm$iSTE-M5bXkE`P3uU>F(&2$z~c-pMjGU>jx?pgD?Df#MNYhCw<-Yj2o&O4bKzif0r{bN@pcm8LSd)wQ+SoYszwqQ`^hqJbNU7i{&{_}(R;=JmQb`AgSU~$9u=Zmc~KibvjPYcB~ZIJixckZap$-5{oO2`z|i83C_2$b1H>ru2@DDT%v+d_E{<vo<o>stvKzaDy?>l-JN!11gXj&HsFac%&v5c=UEN3*Utw(aI;`Fh|;I1I~SI0gcaivzJ7h~s5v94&`nIRwYcPLsNM6IWbVJ?X5jLdCCt@0#kfKUDL5H{Ddds$X{{f9HdntL5hxR4nD6uIQy?+3syKdn;M?zx!=!ZrtOvR(Xz%eOg-E<#^r28(RC%v6K(=z_DyM&}SGwwmFjt?4shpE-DV}qT;|VDh}+T;=nE{4(y`hz%D8d?4shpE-DV}qGD>7Fz)z%o{sP5>G*!0ukZVLKD_y1m*oFhCi#DsN&a8Sx%@xNB>&Gc$^WxV^8ZTC<^NeG`G1zlUO*@}?y;L7`&lfL{VbNrewLDR`&lfL{VbNreiqAQKTFBE{VbNreiqAApJCjw|I)Gl^53-oa?{3_U9#^G$`e<7P?7`rT%JFa19=rod9v>i%2K`*2lBMeLJs6r+_6ug-lu4+I>sgY2rQF5g;4JO<^q@OYp_iAI6`^*=kK^=AAx1Erx3~upMBLO`x-2hJ&sTg*%zR>dTyVBlcD<pbnhUn9+ga3e}rP6f|H^9CjNQaZpgk#kxZvto}^c9pCZT)(|w9=etx(c9zEIo@UjzXT(XbAGTBoI<?+|fcgem6%Vduult2FVyDr&BV43VGgz}41UUkX72FqlRBa}n-1^oPcE^qJeBZTY=a58jXfbKzr?RThT=zd4AcOVq|9h^*9J)UC!rAUVEm-Ruf8;oV(hyAha@4pA3^ghK!r>=C#J_5^RPa%|h4w>qbeGQh$9!Dq-x?rbE_7PYndkUev<d3(wWM6}2vd0n1A^QS;em<AC_xBM(_60Z@x-UTYAj0-LR5EnGBiK6-iv12wCafM$vHwyev+czjT(Wn-GTA!_<?)wa?UKC=mdU<GC|`2UJ1*HTV43V4gz~gmueoIZf@QLo5y~NXem~!y%ftKo0wH;RPKM_B>7GK^UWQ60s7H{!0Kx1RsAR(G@f3S2MKX_V&bTDc%reO{vrO{LER#Gl%OuatGRZTuO!CYulRPuaB+tw;$uqM|^2{ugoO395n$%5@eH@m_J`T%dABSbKkHa$A$6=Z5<FHKjaabn%I4qNW9G1yG4$EX8hh=J)Fz(nd=-4ml*f03{_6ruDf5r4<&#^-9_seP(zj5Q<;*DQ4sdy)mXPL?~JpHj7zae&=ILcM=_Udio{u!TCD|jc7XPL@}vHzXFeJ5uY9-RHnBYgGb{}<{R&$;q%C1k?t@gmfdCnM{Sa`|;C`;(K;mtpGhBGl6=L*H-K+h51^#$ylv{bv2KEMCX;!BrmMk-v_U-}QIX#;xMmou5>zcn@>Cc;wu_D|z+dr-&VA|3}H<`BTIIuZyeVab0(ar=IMsWGR2v3j>ra+dcgE!;~!hZ$CRi$x;us(?%)T`q7qFd5(8fo!r_k$B$Q?)Y^ZJzkK$@Ry}Ym<pX_kEZYt2!m;dsU|)t^;wLN<KVg~p3CqM!SSEhLGVv3ZiJ!1c{DfuVCoB^`VVU>|%fwGuCVs*)@e`JbpRi2*B#h-)w&{^M?hgiT@p7EWa{hQoW#&%ZUA+CmAw@E6=K=6l;QtrNw4DdQ`h;w+P$qZYRmtS)5&80={So={q4y>7<$0N$e!^rjq#iG<p0@LTf4s2%w4L|w%L}`&w)3r=Ve0WzGP(YE`SPLn<>kxszCrv)MDQOG!GA;q{}B=VM?~-+5y5{%1pg5c{6|Fa9}&TSL<Ij45&TC)@E;Mue?$cTX_c7*l`s*@i7*~Z`Tc}b@EDEdXc&Q|{EXcc|5JBU{Lht4@jtOQ#h+hI@juBo#s4(l6#p}NQ~b~Q>HeqlbpLaCIvy^TF3iAk2JDaJ{xAp2IdCAB2f_j@7r<gH7sFC4m%?%^m&4&$9u6z8TmdWnPvRT$JtvU#Ki_9#X@iNgz#fpsG7Tx53-*C(EURIvKPTJ|%l%+F&hq5v>igm$aE3S-W@9-UX8PYCITy>hZ~zR0z2G1$4}y9AC;Jxq-`6-FM!^_37|VlU5mdn5a0r%%z!De-6W}l`4})c}4@`n1u{;tEg?*t4j>ht6I07c){8YnIgQGxxXSj@azgzHHwTj>9d5Sptv^SOf-ozc^lkFcX`JT6T2;1r8s(AOwr~2_u#ZtbuW{8qyyVo5)TFJ8i?;JW_$x;tLZknLvZBLxsD$jA_`6srv%kfKnPH62v$CJ+5+^PqTrF@`Ij%B-nT{xEg59}MpD=wVb>L)4={6xippQt$S6BP%3qT;|$R2=w;iUU7Uao{H^4*W#LfuE>2@DmjWexl;QPgETEiHfP8gmK3_vtypwG0*InXZ~-^GjS|(Nt|Mt#3`0ZoMM^8DV9l`VwuD#mPwpqnZzlUNt|Mt#3`0ZoMM^8DV9l`VwuD#mPwpqnZ&G6mcKDX=E*FRc{0mnp3E|tC$miE$t;t3GRtJ1%rcoLvrOj6ER%UM%VeI+GMOi{Oy<cflX)`BWS-12^^-8}nE!Ole>&zr9rK_6t@+Pq6INuNu9zm|@0zOk%7!L!So$(0-#>4?nEUG0O5Sv-Bi=jsL>0TFU6x6^ER%LwrtOBY)KT-@SGZ$$w0ODiUiPZ~@#msvnacd&rN6l!4y`E~TiVV8Jo(FuGf%JGR3y`OK3ZEuMnve3h|nJqp+9-wpVrI&cAx%!zE$pW%iV367wwB>U+C@UMfbpR59sITMF(Ly2nP83<bC|?=wR4%>Cnu8Z@uGw>w#^aitn>ub9>L)!SZ+aoYE?<Vk#fTvd%fndW$P3pQq%j$8{Ia_q~8+S!W=xVk#fTQrG9ram9+6lYHIdt0(`z&|YoleR)s*f1wOhj~AhyLKz|dmS1O4f2d4of0%l_2=(N>@1h5mJ<#vucjyhma!|zgUC8gd7>wm$^iR~eOZ<do;xnO)KHw6+Wtqx{v8<E$3CqN1LRr>H{FY@ZAI2SisP@Ax1FQVs=dJE}p{L@{CiE7yk6xhUM=t6kwhUDBmVvvAdq<wHWGVmIg!7av+wHUIn@X1bHw-nucX0Psd5-sdr)z7w9Isi^wYC2oOZh+#9LshCeKPD4yRb~`!ZNW7%fv1$6T7fX?7}j!3(LeVEEBu1Ozgrku?x%8E@9m9{^ySOKX<(U`RjZC^Zx_6ZZK8', 'camping-cross-pole-domed-tent-01': 'c-qCC2Y3|K`v1Q}6#)^ECJG_+7IxEi17r@p_ufNDHY5;|m_qMJk=_+hl&Yels3=#>42m7piyg1mcKcPY<tn!8_4l34Y&g5j*-ZTZ{?E_nnUCMR^UizDob#SDyK`oTS-E5TR{`+BcHr{{z~C_>hA)myFDeQY$97vBJ1dYEC`>QTFO2OLJ0!a>KQF&1W)=^L>75(M%M2984C*=}W?o`kLR_LRwsY*fKw(i%ejc6U<2<oTJI5AfFhFcKkFAPgyG>afo0mS9w%9SjeVt?T@-u@w5~eMkcKNTxv4I7}h3Q3BEi&@w7Ubsz@`}?6^K-33N8|-!EMsn<xJ=}i<YjirC@Gv5$czc(W#r};<>bwZnVVi5D9lOEjVa0w<mPsc$;!>oFN{gg%Zw>5ED6xDxNu=iVW7CAFs~@is_xuCQFgGlb`>XNv%Efb{C>f>C53@rd71sKNIas#TJq1FLaUDae_ly`Nm0y9nqo3@(r4x8v1SEy?H&_Yke*Q-Gv6vLCMzc|hi6q#n4guC8|WO9QBuq(nMJ{R7X{Lb<*ItatJ*)Ou&B7N9lJLR8fn$!|Gt{>;nf_So>LUa>{FOOKhLqU8QD3xnS}x7(G*W-Z|8WX#pU`3b2BX`lfg35=N7P^yJQsR7Zr7}>ewYSe{LYNOEIH$@pzeBS<Knuv`n5{MsZnYc9}$TQE_^4PDa|ioT8HS+_e0>+=a2-teof^n_rkSD<>~4GrhQEF1_uB$;m4Y%qnC<l%-IKmHS0GnSq$};+V;v?lIXsY!OSM$4o0%iefUX><VPEtis?(NweCvknP8yi>Jn>XQmev=gbRCjqMhbm7ZI~7MxnvHAOk>f?1CC{KB;0@Ce_zFe5iml$IID%V(>G?F!`aRD!0dv3(}>8QO2m)L6@2lx_{3U>I+_-?9{E7Y5QZgO)_;@3grruI%{!gC_RtTXy)ooWT6F-1LP!DXG*c!D6Q^wR+v|Y-ZM&U_<w@I>_qYzE<~)Wz)o3V?8uJ%f@?Ve#y+-z!<h_W~ejlIDOLd=A{><jVj3r6pzSY)!3>9GYf|W*xtE08Kd({W@U4738u%)^dgSf-2B4+Y-?-Yn&OE|@}^k-`8_G|$w}S>UuRETg4YxLFFwJa==CT0Y4W5bmbv*oz7&to+u3VX(JmttjdMd`sJL=loIgnp=1W;>WwH8v2IX;9wNGk7dg0um?4`U)o>Ovsu(Byh@d@7Kcz+^KASt=b#J_xriSfxaCE916?Dr?9`260a%AAxhyo3r)s&{&Ec5%tf;LMoTHxMWo8%WQs<VkrF${Nz+O-%84y~$plg4b&|uE(FudL;RRwz8`E61+b4RZ2=_PAkDa)aOe`NlH$r;Iyo)ElL|um|l?0`L43(lay#z)Z<O@CHs6<pLmkXjJ{-VlHZ#cZ=EF5Eoe(l@pzJw*niF^6qjH(k2fWr$?Q)_c09$z@I>~o>!y`W#o<@r3NCLv*TS5+Io32)c366GabeEPlHx${gh!4TGidCf5yOKGJ$%IIVZDa(g2d6Elb4y3Vfn;g9^!Pe+F2DL;c|pTIYN>g!5b|?^5qCVIf7q~5WjSq6{F%yrt4Erkxtzsm+SS)1t(ltaI}k{>*BrfQuzsC<tIj#&lE_{;J%{#!m^+<OR};8h2uG!2fMKRgTdH^1*~O~moo^BC7i6gdHo(M+yWlQc`+_Nu`CZ$k`j`Ai3#yEdCMlBB%jBhn9LNm5-!KOf_DiHVo&(Ej_=&X@sQ$R(Xr$E^+^bR5|FFtby3A=$HzMzpHO~$Vp2-^@nib*8rp006%i7m*B~J=G1N$&xRkQ#)0dR&_a=A}Q><2t_gig{nCOp>Pfm$X3AUO)$?Hk+^1|Ww`+S!h%^`qwg`z2*^LPrU2~K>zU@In-&C~G-K2I_yj|y5b(ZxALJ3c9TEBZW16}4h=1^t-hznp4T=9Eol$-a0muWCt&73JD*$Sj|W8bv$aAH7Wy5<C^PNlNq@Fmt5LiuZ5;`F-BxL|)dt!SU!z4qhVT{WSO!l4<fVYk2AOCnS0ODgOAd%!&-47@t>$h&ntyF3urp0B`hWO!g#K)QsNv3hLmA-i`_0c&il>lH(InlH(KqPnt2o#VJG$kQlugll=ZGnvr$7974W01TPFT7ZwMG^1DQ_^-a#3Y+FWTWd&~%Sh<~EI4cmGJlJZN>*M0!GK<^eQ@sB0!+Gh6I6NWB;fdClov`DRcp-CN{FTS2BqaOYAMZ`{Mx4IaI>h}6c!MAK!U8bSDpP|i10?%BiS7d=M|Pms@AFim3*vnVkriMYRwjk62oTRt!pW6rf_Q6^2n&$t=O-BVr;r%ghVjXs#7eZGLjZqLW%AJL^+g2Wx7ma%@~C`J+XGsPkPy#S;77ukn75V!y$21)>E`{+SI?hM-TLfqA!}eoP@nxSJ519@Nd7|d7m~k|Hf1dx8>vkvE!81Rf3>EAnU&R6bU3#{xY3u|PYvpY69>A|%RlUEre6JS>T}z7N7JGr%{mCFJ{4-7pYBG7;`d(rO1WLume1Aiwi0JLuME>4e_gY@O=NxWLRWL?fEwc9&NX40F%2nxxz6s_s=OT--;l~OLUy*NklMB~+H|9(c5|!E%4jJcT<PQ<rN+&v8$|Wz>j^h{>$Belb<ZOo>29>uk89T4BKqClOvsusbt!&@`qN3H9Q98xCqCt*uYUKizUH%0;`2RYMcrY4VgJq-Tax0!bcd<+bV--nd8`pSmgk~N=T#YPxY5!%nl80b87=jN;YRn}_<8B*(+5QV#}jmw-nX}@Vd;BcsIAoWPnC{!)b!V-V=K~zN=q@L>C%d{RDY$ma`@+a>**6yc8NLnyr4IIrlWYV;ZjQ*A#KekA)oJd4K{n7KBb@f-O4bnjnjm$;H*BT`o=JQ*VX6sZ#K3OCqG*uF3gQF^G-GsqcT>BrC-!HFQxohPusO#4D0ck@!smCdUotKk@DpTans}@`kHT7gz3fC=ka=WMh7oI*^iD6>N)%7^LliqwWUAkztN=K4B6>#miez}eRkTl=G3h-#a}mi#j;I5>fa0)Ab#AFCcf~U(nq~CSu~kDMCh3v^iLKo5eIj-7o|V7Gm5fTiVauAinDFsH9AZkA#Uw4K{W4n!I&~VUW`vJ5x4%cu4vIAOT70+7tvx(Cvl`;8tZg-n;qvG2lbNlc&q#)mVV&DfhO%{$WDK=%zxX_y-#g1K3TL&c%HgPZ}(8G)cW<ei|da5QKwxG*-s2O7}QpL$!-86k6L=qBTpMr9E1Kwng7E_ftbTqU$Y%zZyKItrrdE%Kb8?A(nlqkiF=Rfr88oLY%gfEz?^eniPg@aT}b{y@)wf7aPT)}yY*kMm>s%ra)~MXMA$=h2-9+XB!6M)x2yU^#~;07TFfQm$nd_R^x2ELd@d?`%$ve|V{M0E3{`wpTSfRdwojCL>Qa5mkB#&n(s_rTJ2Cv&NFS&8(c)C(FQ2d5_)c1Nj%;%wwRw4NNdAVL8!CS}XQaBBsyI>n4avVe-&FQ!IU~2v-<Ic!-~W16Z<xQ*@cdXHo~<9y<vf(_FU|bOm^vv-*zHj6BbTMhpD5+(Qn?lSyR|!wHI<L7<@)e^b?JO{>3qxkTJkp({)X%?_o-BWLyjXK8^zy{{L6Ddwk!I}i0m)94Xy88_IZ`}yUH%dj}k{$#BpqAg^v;G6KV&Qe-s}>_HnXDo|kHFsc2qO&BM{=x{9=F4p&{*RM#wdPN?h{aidk^MU~sC{EW;)r+Gup4OI?A>)%igY=!ld(>7?hfx0QWkX_J#Y=DMjL+;;>=7_}(v_c2!_Si^nL>saVnvu=8e<wZKl5M$vC%0JaLPuOnUW?9TXa2PtaY1(EU%R<AA)CNMdf+9!+`otPkRHU7@z_Fcq3t##q9xf9H{y2OgzD7QP=l<&J$um&$z(EWk~L9_tVP>C=<t(%Tt!}m+GK6o_CugM*&SDtSECMDhqgP=7rn{es7uzxHRLt4-HCdrN>)W<vN8IT{b@UZ>v0`<9j1^|Fqj;SVdOCGxeKk)f^2~i<Ou$CH%4I`IS!M^N!UbgLOZfuaBpjR-OX(j4$@}=IRR72sq{U_Z5$5KGJqU_$>d~ABd2lyA#M|Jn3noveRLu_VLCaT`ww%Qj3cykCA(rXxtV*8aO;GlNXJ-mEJl(e5ktlxflT0@W5~ixawd|<B&3ijwB3W*2#^8zNFP$kRNC&v9LyqTp$FLmJ;|Q5-G`fzN9Lgy*$aKhKC~T2KQtm6VK_M)g=8UZ_hSeKk%Le|mS8?PpSB0E5JhAW29g6Yk(`L}<amrGM|1y!Sc=8uVvHfjAdO6;?F3e08MzEI$Qj5aGiiGWw_pXi0vTima>yLo9>yB1B3B`s%tkJmOWR4@ign~V%q8a{pUkK25for3ITQ=X1=v7tpzTqt#d>l*=8^MIOcrAixd=<hC0I@_$7*sleF4?IE7kof`JPkceI}=SPV&79Sx4NTaJ*Ncx^E%t?O!Z0H$MDQ>O1FVh3UMf`vkT1Jyq8CJ=Vv3&-b#E7EYSS3Mo#xW?4ciH%uQs{c`HbCtYbXnzmzxX{iojTB>t2ZC0eEwhGfy+g_oiI#;BHN_Q)oWIlFVYw_&O1C;uP8SR65%V*1!`iE(Kg7<nCf4?(Qn@-xw?ZBDVqTr)tuJk`Uv=_fsvz|h#bER}>oQCQg(ldTJS6(+aIy9EQY`whF+We)K8Hyw8Dz)Ow(NEMAJDyz~rg`qB)DDiCbu%iXL-)Dub}*!Ry3+EoA<Y~UQodEFOQ%f|Ek188-u}A3=|)S(y3*3I!i|>l#B`&j_IIVF@#RWOIqynKW89VIxtmfuRHRKedd$RcjBh_(FPdNYP<Nxh{PwA!9@h36QCV$`saGCZB@({5AxxkAb)5eCzt)SF>s}M4U&w!|QkrGyQn?lCT`OaIgpQSU=z9HFr;)C7=sG^`l@6}-L*qX-oHWnHkj|@8I`o;rE~`Qv`Yd6eONE*_piB8sp?>^_uXX%)z4)Z$kA@p99qUR<$Lemh)bFMnEw!yHE#<i@E#<8%Esa6Ljpn%<Qae;e8*a4k#YRT6u6K&#rL}dHZrbs)QcDl&>y4&UE7FXqOYtkxhDu8@qv_I$v~-S29lFk1pP56STSB@rYfTrn4L3Jmze|5RW2I96@nUT;t@{`H&BND*>HF55*Y7B7E%senrqtfnvF5i$H;Hf7tPmf*Ti@)l|4;hgtFH^w3(~(c>et_{x9PN5tV|vw0wt^T_H|b(^=c6i`<8sJ-+%o0;oILICq7KwswbXbY^wDA$2%T5J@#|`&a}0b-IRPBHRGFh{8p{Lz0ur$XoUE|r;9~Le$Y$4?<=Nmn<iHM_^5vR*;(TFo)od_d>37GUMyza(nh@G>u>zxTP50j)htZc$bZL}^5}4Jarqc=c;7q5^RFcc@9=!_!Ioy?z(b=%lcqhC`kBs6#e}VM#kg@t+k82@wHRD~kl1-wFH@z*jVn2Nc-~ym<z#|oHzglO&G@Dr|LD(0j~YuK+$v7SpVd|RgZzf6e?PHRH2wGcmR*;89Ce2i2lUO2c3StVR!DY3rLFr~-(9m)d@%h<Ln>FP8Q%!Sx7OgSF=GAS8VhY=zf5iSK-sux_w_M-QTI)v<+rcs=l<D7oO^A#IKAs}J@%a*;!>Av(PGUU{gXwR;-E)_X~sQlUDv+;wUcExB%gB4n1&S72*tF<np6iPR0r!BpU|DWX<y}-Pk-^c5ve15gybV6pDXSOTK`qw6Ju_kKES*(=H<AuPlR2B?6Q{2weQy&)_vI&>Kj)bGltEMF&`hAB;MY9%=kV##*}?jcKiNrP+vPK$&95>*D3Do=f@?P?YA8>8c$c-?R&<dI){A3ha-~A&yO54W~G&{$42#$?NWV0_qh$}K6*tyLh=zIA2)W^M@aQ?wA=U8qxO;PW8d30r8PZ6T3a@x^#rT_rpjOTk^3UT?&xo?Ef~2I%hwN0>;C$>CocG9pNjnL`|-iL#dNu3Orsuss_dS<)3GXlRsH4hsH(%Sr!Jf>j~_AaLUH8tQu~LOCD%VxmfN<K+NZqlT(xJ|JQMEk*q+LHDXb04?dzLeGA54dYtA<=8ggIA?Jti_$w$Ar<0Yfp(7tB9Gv#Z!rnGJx)n6W`vcIZ6s`&D_mdlcIDXc8nUutI|^^0|^9y&H6zN3#k4@8OYST{K)+eeq$M@a4CI9J%~W2W@%K%`GtOqIXA_GMaYTyIcs|Ea)y|A$ONRhFEer#X&7T8?vI-Aeu1O9kdD*945noOhZlBFEI<mgkzGHCQLRy)G9j%LtVv`>T8^TdsVKPT3n{{xHS)nl8t2y1vWDMw=6y>f@%Jqtro2br4Q<Q2EI7iQJyd6GO@q$8jq8>ym$H{XgjA#y@QAIQxgyM-^Wlk8)X3ZiJO3`%8VHOYN^q?XO3~cl43RW|a7jb(3RC<1{R$JWf^P+Fth#wU3j3SbUYgoMUoXvVY{5a`KPjW5_;EcDb(=K6<22sGU{*QG9gS$H^Xk?qS~xOeY=jy~FX^t@_+9f1Zr?St6uWpLyJTu26lplt1Uo-x1t=o_F*4T>e}we<oL56C>xqinKhhs(h56Nu<xK@;sybj3iz6Ri8b=uGi9M3^(IC@><|@t(50U`I;z?5!E~_&qb>FP@XsBc`tHKxI6}2jf-*}?Rr|#^{%qt-|J~UbSJxGDmfK`6ljQRH0z0#dRhZqi)*#|NTg1H5B0U4=!@&Lei%$W2tCLi7)}nySaK|SqJcINy>PwO2jkFCv!1qSq)oyUatcz&6ig$hVG<hCJ_Aj(bYxKnkV$4jCw2NarvD@~r9Fqt;ohd)8$dJdCN#qh+6`!e8?~lrOx*~nWGaS{!!VbeiyLv1R)~4zJhUWRqB+?dd1M|Ik&94>7_B|ppt;r>v1p;SLJV~al#nG@MlM4;wA8F;E?R1<(ShuMwq#o@CKqEJxem+GO7o&CVzoGQMr*ALI#GATT5>Hmlbhi|8*MxMq#sFS65>hg*`+qx7VIW>V>{Yvx8neL0FRT8BaKW$H`01`sjZfbt>jkRj&|Bz=uh@XZ?ZS;LVN8X4wHv*4|z|}au@fu=iX7|C_G3$h=b^$-5=yZS~}2jl01p~(UJC(<VieDK8;i4DeOZhZ9jfT{RDkF(|(3LgURG%Oed$)vok%PMi<&=k~6ut3-_KuoHieG&{fOD5O}nq7)U(;cawMHIC&f|kS|~XyxKXuPQH$t$(yl|T!<IR7x5<fCe9&I+kmBr*Os6N30g4<sPpj}`5N9O-^Hy+(%!=d<Of(muE2V7J>DYU!pG#tcn>~pCpIBj+lX7>*R1DvlC_oii2MkDCI5;YNYOsSUUDzCk=w9~+=ai9f5VsLm-r0bw6F0U`5m4_5A7-3Nqq<Qpu2V({z3hBe2rA?2o8~l@BsM$PLrqcZ}Q)`L|(!X2<-x%hps(mJqM-Thhx-7@dNn-ej<Ou@6k(p1#ggV;Aiq@{FnSMUO`{&Pk0BtwYPB|eY98cGWARNh5QAY)?3rGPti}ih)>8*@GJQ%s%ZVRDzpvIzQAA5U;8uuh=JON_yhI(sHXMTs%bUI8rtU=q}9~EA-};t$$#Qs<iAi;8>~V54+eAlk^B+gli%Z8@>_gGeue7vsjgKetI~IfcC}WEtfld)%k64yC@obnl-opdB1VuSP>c3j+%rtmP@Al+jlnQ(6UYguLRNu>;k4A&hI4N%>RNc1d>CUeLaU8OF;aUB4^f}MRiyPy-zcpPO36|@LOz14N$Z)u(VBs}r1c!%Xzdz2gE88(FfmrEqg5lTp*mR|v&dP<ATv-$8>gK`J&e=p1$7<T#&J7~@mgK2CRr0#Y2&r4_}2t28#ORNs{u>brELPY*|f|?Hs@gL_nE<GEbZTps<hMZODp@kQ~Ua{BAT{-M=F)8)K0%&b^BXZD~?NTM$?u2O>C(C(X{DCSLV01p=)+DUD@Bn%Fq3&wEUaW$lsS%q^)PWj_rT0N9egcm9EUQdy(3TQ-Ky0=_t<wR`_h7o96^0pBa?SU8z;i71};#G_88ZurkjQMrymQqG_`tUD;<6RnH+tK9eY&yHZ!;xy9e~{9r{|er7H5`8BsXa{YYj)|s3ihNhlwz9u;LSlXI1t=~3Ywyy|kYhIS@rsQu*aqKy#%zxhPPnPz+>8;dLckLFH)za<s6&N?eEPi)k>cM)q2x}cYfAXGS{bfxb5%RI}bK06csrIoUyJ@X)+x}r%iXZI9(6Ls1`Zaztb=cLrgd5F64qG`>wl)h`?Y!kLyF^IOZnDea`%l^YyR1}{-3Pd<!xcVGze|z*!;cMLOL2}L>El=*QBi$lpK$;1^$_Qn75ap&pQ!Be@!>ws-+x{Dm`*;jJ=~|lHow9r`T8BYHZ}ThjXv+bLvJ#^Ow0bVU2cops_oFnO~2A#Wq0~M{{Pbc78^ft;dd_jLb&J)5v?!evLf%L{Z^kV%W|s2<$kOn2SoI7=d9h1Q@hS0+PvXh2c?g4yobuFto_QEPGvdfm{8p-Qm?fF-wxPe3>|yry;a#RA1~i?m3=ry433eg$I3o(9L1P&Y=0N+pqzgqb3--8RljMBm_sU@8=c39DsSE7LwG;R?WwviuIdXXy`10BYmhZildQ?_*~__A;f1*lzcH@}{zh&Ex3Wuh9jwH4s881C_wSY58j=lZTZN`*Mm9qOvH=>Ajc8kqn{WeZ-Tzz7EryJt?H05|YqB+NByU7>vN>&Q&=zgTHfTj!zfN2O>mJ@()W%ihRcJ@HgLSvABW)Ydncw(tMKxSYUW+c+h&Xt#9$k@ybx1@!bpkqJ6B^@s@_N)I>p~+n)FNx4J!$>Eag%jlk!(TV&G4fe*$q0WqZiqWwk_xlK??N1R-~dobw3QG9)zLPL%4q%MxZa*7sJS57)6evZ9B$cBsmhJ$<Y{3j>iOY0w$5xuK{;pEGCi@F_oN(G%}60otS}Xr1h)6U6_JQ>I?*^vye?ai~DzD4rY=wkwfNSE;*OBJ;*~onU4ap0Nt&7UPvKRkW1!r|LwRLgUP`dKn_3=_MsRHaT^w3G4^5!=Fu`Ah1idD%qC~UNBYo{?1?^P9}FjlV+=V4)5+=dy#q^;OeVuida;aLM%$fO6y#F=btktHvV^vws{+CA<8!h%h-i98%ZpL<pa<s!^*5ibjjFAf(KKTUyIeDxw#!v&#uRqBQMFyJQg3fK#9aDDCvkBDzk4e5?tk_T>Q`3hxz)nfrW?(&gk6?W*EstZ<L^Vah^{aFs=Lv3=3WfyT7Rq|qG;XLrb;uWZpSp-=nJ>~TKdD7!{WIE@w!TXFu#dm>0h606iw^4HdLB1Q|*{a{f8rEdA?-EY7tF0dw7B#sXttpCM^Bk2W!npZ5<m;7q{qbo*Up3UsahVWIg}e?!wZa{G4H`^f#aP3%(2Ni$&=|rH_C3oDuih4$+|HMO~#&u0O3?`n&7?W~lUc&xqiA%|0s1HdT7Y@sEP<qDnaMgRauszCRf3-@`>~QdRmw?EYZC<a)j=mG$<ahMse2n;3KP3q#gpM0(ICu6t>zN@tCIGx#2^+5@YaD*dM$#s>YzuR2w#(mCFvsU6oH6klpThv|{GzEf)HK)172{e$Py?cyS(zOCQ&!S_<_I$vK`>46E~2j77;>ESMhN;8*CJKsd4wsTCWnZv@)Z8Ms-^E^y54^2A{g-SD@g`Ll)teIDaomaZ7nM<afOG2fYx4NCThDtO4g`NMVN;5Y~?c7MMtY*#_cFqWuX3mt_Ig{!}GnY#3TvF=LSYZB?%6dtsH}v0c-Xi?Z{@vhM)9taQ)XddXJ6B6(&AckL^Ga7~=BIAwr{PAQyDi)7`u!WJU5~F9)WX)L@x&Cf^=<d+YnrYU)WX*0LwB?@uj(;Qoc+G9h|t2;rmX$N2aShb-y`CmD%B&jZfir<`=8wYJFDHE_<7S)vcB%VY%{k{HQm>CjcB-Rrm*zGht`|pKOJp;k^PlE_EdqG^u$nM>Ha6?n@bAnnHN7Q5NnEBiXlC#hzIK|6w5oun6e)G;54K2nEhgHy=>-oo*uh@pZI#^KBLzbUEfq~zxZYP663*tEKi;O<RNiEyk5F3`DCf3ebaACmG$3h^n1FU_n^pLoAxy8X4-WVth2D|Y_e{qT{pox3%kzd@_w~~^_-X6Uev5pOSBOSMA27G%^6z1VBL=WxKfuj>r-miC-uGlS-OAKesQ2<p<!li(jV%*M~r=bPnc%idf0XAv2$nHwX*onYX!BiwfwF+A-~T~dQY5?-z6u%CocRQa4TAsz27b7i2VKUmP@^Z->dTf-X`pxgKU@Itt0!W>^#=Ak5%1&i{?}QT~+px->vf-e9F%yN?GMTs`tUkWvTq_=aq!?jCSZ9bLH>fv7b@0e8S#ACdXI3r%Wzaen-#b#Vd`wzb_E|t_^>Wn5xcE-aF>_J}fzo?89<(yWB|s$Tk;|`R3+bR}Oh{#ruX-WkvWn=9~OHU_>rC_PeUTB4U<5uNTp$j{Ty_4F{hqezOwMFOK=3>bvLuU1opavo@wfJxwY9uQ(U^89KRcs{WGgXMQZxhyJYgQPoZMSNX`#-^u4v**GfuZ#>5<o;_6Mk6eG%_>FuIqavRj=RJow!TwdvGj8TO)!2_R=cw{o_II3TDyZ8Pc^lE!!tT?sW7%KA?k~~!i3_JA<`Abmcbs!n@#UCq>Y$o4D`;D%oR1dYDJLt;899zzZp7MU`L$KfRXNAp<dQres^&LUo<!WMKJ7G4E34hi36(uoo-0)2{eMf#eW%JpmA@)CRP&EK2Ia9M=ck-|k-s4b#e4)+P@Sxfnxu8l|B>K5|3^_5*OJ$w0cqXCf0SEYJcg#|L-s)pvIeS=)v%acjOJu>?muNcflSszKe8WMlGYvmQ`}aOtGNGhw8vm_Fq)7}a3h|;O;}642A#>y+<zLa&;q|h42Dq;MI0H2crqUA$aUQRB$DAL{TPj>Fb3_Y+oBWM2^+`_-2XJXV+%^L6<%r&x>!%UVjMXRI;nHNfmEcE=?IVk%pvFCX7XlCC#S<l`jAK_Vi!!@j=QMuz+v(*x{=)&;|zMEHfgO;oZ;4&wB9-R4Em!!X|0t!!)*{bh_+|BuP@mbH;^}A2ss3!$Wh#L7P0g>%WV)j2$RXl7)}o7p6BQ@gdBnnWCx5T$6^{ejeB0e1a!5Y(53GS+$NKgF`Jx?OgxVajK_=g97~Qx3Ymg5G7SY}0p^kOxc?>0gdhduy~Hh(%%tsQ%nEWQ|9Y9*Y;rahk_(Yf=5zlm$VC>Jg*-Bkf1P9GG@Qo_6j2xQuUA=$#RC5IDz~|$^~Swdxh*6Ya{p^sgsNm!XrzW^<TBb`#|ktit<{{@xveHw)AoDZf@Wkh`uv{TGIAL<lbgBc0zFoftI>vRgZ1QkY$vyK&l|WE9m$ULe1qF&ax?am`?=>$Bw!o44M)kNI7S}hac^>4Pg?6sZ($FTtf!Xg{}#9X<bFIzT2FAljYGH%@8C}CCU@g*@^1e1E@So}d*BFp1ox5mv4nTIZNqyk<tTZSwu?B9hp8W;?R|P4AP+F|`>>u0f1le!<U{m)pW6}qf#bXuSqnYMo>)RIvHtC23_u;S4jPgTv7B5^+aEC!o5)RAN-jk&vKMV1VjxzME3uQ@iAm%n+CIWm>?8MKBe@YH$Pu)C99+BlnA^SNy~rVRX!`^ucz}EWd&#|+LQbLWQ)J^F@*bQdPhtVNfVMwjK2DG)a6frJipgTyq;(JxO-t)Lj#^rmiK?abCPyu;6PeMpw7%o0rFE;QT3T;%)bCX7BRqW)#km2wLZ#n`8x+*<4-Z7srmantW=zwLsnoYLcwMh@=Pn^QnW*%#oIeEh9S8oct2F%$+uu}a`Wv>tq0(LcTU9^s<vk*9vrkv)nBzAFb<Taw+-k$th8xYY47)6)meyrNG%ej@FW1s~kQu3^d+Cn)blq-Z*=Zp@HPeNxAM^J#E&cTilTDRQ{zIy0`fi-~*q0?#x<l6!`oQLUMaDng*Ja&m&69?uSA2ioQ0askeN8LQzw|WIjee&4)B2rv?-GBR^O@eh!Q51<ZAIL3sj~j?r<e4No41M8SwHD+beoHtQeW(Kk7$$iVd@(b-z~M{l*$_Yo-r<cw@3W)m$!_jQ;!Gj3r21&mGyfg-!`n62a7*9R9adS)ZJ)lEz(eFY28FbYH4lJQA_JJW;89WIhJeYiLmoTs5JA<wDZlBHFH3>b3j*V_PenAUAWQAJ;TmDL)Oey)6P{>rP<fz`6FxgyKeWp&c05y`#M$D>|fpPUtOh{pXIqEYv!|I=d;0_H0+#orJ1*-cHWjs>(RPOOKabT8!fG;2x*<gT-I=k*zY@`d!Ae&s7+g&dk?f0f32S;Ru=UV)TXV?fArk158HBw`1Iz-^$2a)+K@H#?vT|!ubv-zNLniq(i)06bmtIp_ST>D1{3CqLB=T4(y`O?O<8-N_(lKtk(J_D*BiwjW>+)w8m$timS1mvG_0S#`^US*?QK`-c^!)NpT62J-ac`s{@72;jgS6wmni7E-gxzqS;mB~4~S9k6d7-RzqI==-yRkJnO!YaS`!h{T8UMzu*(&)W<5>2o+j%c>^cb6&9LicvRvIRS7*7pU9Qf08g@Mm*3+=-Y1QW`yFR7TI*5?gN6f3vj1rF&yrkzYnJ1`CTbmbpT`wB{I7>81i4)YOt<9|c8}w(s+AFkA59txwu(cs;;O^E|o&X=WRz2q|eHWJR35(z0V^**>5zWVRSO<~s4Vo&Sh`KrYEAIb<`KbOK7rCq`KEmPNc-X(EqN=mXU-j>r$Z?|h2#0$wrkj8BL$*8g*A@Tvh8rL0URGG$RR4a4bWcoK2i18g)-NLS%CUb{{iV1sq|A*7yJLGw_sWFoeM_poj<8qQZt{BtRP~qZ6Q#{fhx@dla!q^f%y3vkaTU{Lxw>?JSa(<x5vq5D$n}ikuRE++2-SF3%`K7dEmP!=<2a4@_n92WwRAtzRLv)D#-J)@l$=z}C#oD1iZv$3I=JzX`!w<$PA-lu?_ax3Ona?acUWsM-Sl;o_tQ9*6>$v`4!@HMyUwce!A)PQ<_9-pP^DFK#s8vqY=1ZT|NlcrStBr|H3A{65g5`MfiA5PIL<|?Jdw*f1P#^5YN$zCYX^t8X*e8QJ2=ekdh&WSCL7as1WnP4?1dU+4OAtoqJS*GjpU8oe-sT+kF1A2WFNF3Tc8!$3Jb}F+<y#hFpwOGCS(&dBdt5V$GEj8t@nc5gU(n+E<-FCi{@l=3?>I7j<nwPaWA|WNsdHovNhU~?XVp8S#O`9PUQaM=!7n07mUXJ7=sjQKT^q5tRvTP{{!$LolHk2nTg5dWOzsq637H>BsXFUxdl7Po#;+>=W!3BCu)<{dclL-dXv3rJAuBaPg?5*C%6qD2hjEq_w^=w;|B5u3?c_%g!RS*?s*t7^m&-u0CE5(;H33_2I?W)^9X$gk%Q2dY>QFW`xG#VoP;zojr$+PSac=3@`y*dO&}*Ao6JTAnZf;!(SH;<3h`t-rjS!GgPg%Vrx?eg^@f;J+;YiW+8)PDbR)Yl!sFaB$PC(^Kp@DO{ObvB*<?2I$$aiP&0}YfGg!iDZk8p$J*T<l;&-?i)ye9pLRLW$Sw!2Dn2$zeBV0#bhXv#U+MdE<+(h0)pQpGLkwsXAr?DDKP)d&l<N~xLTVg4>6dTA5++$!RI*=V0!{D}xT!n4qHf$z0bH5q<EsDu)H@O>o$-O+<g!S$dlUqlevEE)nCe!~6x6R~c+MdDIAUE-^XSi)6x8V-*4(@rDF?*0bu#4P<edIot@GQ5rILlIYle=j<%k3a}khbUOxs}|?7|(G#NFL<==eX^{^TBn2=eg<D8%$707Si?t`k@YKtqZ)st%NM0?L`zrkOITW;aEeiq3tE~$2@W#ZY6KUcyc^#FXI*rBZpx+IUPI59kjiIaad2T$L-|p!F8fpw4K9tOvQOj!yM|_xRbn-wpWpbJ$Mbb;cn`?kVodx_B!?>hqQj%@;bKz<N@0L2dV3_H~'}
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
placements=[('v','winter-fixed-twin-front-skis-and-single-rear-track-snowmobile-01',(1.25,-.25,GROUND)),('t','camping-cross-pole-domed-tent-01',(-.95,.45,GROUND))]
def rigid_point(instance,p):return tuple(p)
def stored_point(p):return tuple(struct.unpack('<f',struct.pack('<f',float(x)))[0]for x in p)
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[stored_point(add(p,t))for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,rotation_z_degrees=0,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values()),coordinate_storage='Exact IEEE754 float32 after translation, not hidden deformation; native versus final GLB bound unchanged2e-7'))
base_mat=len(PALETTE);PALETTE.append(('SceneOnly_PaleSnowCampFloor',(.70,.74,.73,1),.97,0))
v=[(x,y,z)for z in[0,GROUND]for y in[-2.2,2.2]for x in[-2.5,2.5]];f=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];emit('SceneOnly_ContinuousFloor',v,f,base_mat,'Single scene-only finite equipment bay floor, no extra counted model');FEET=['SceneOnly_ContinuousFloor']
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
  assert -2.5<bb[i][0][0]<bb[i][0][1]<2.5 and -2.2<bb[i][1][0]<bb[i][1][1]<2.2
 for a,b in itertools.combinations(names,2):assert any(bb[a][j][1]<bb[b][j][0]or bb[b][j][1]<bb[a][j][0]for j in[0,1]),('Whole instances intersect',a,b)
 contacts={};floor=triangles_of(FEET,vertices)
 for k in names:
  tri=triangles_of(names[k],vertices);mask=READER['np'].max(abs(tri[:,:,2]-GROUND),axis=1)<=tol;bottom=tri[mask];norms,areas=READER['normals_and_areas'](bottom);expected=float(areas[norms[:,2]<-.99].sum());report=READER['actual_opposed_face_contact'](bottom,floor,plane_tolerance=tol);assert expected>1e-5 and abs(report['actual_contact_area_m2']-expected)<2e-7;contacts[k]=dict(complete_ground_contact_area_m2=expected,actual=report)
 tris=triangles_of([n for nn in names.values()for n in nn],vertices);rays=[]
 for p,d,length in[((.38,-2.05,GROUND+.40),(0,1,0),4.1),((-.95,-2.0,GROUND+.40),(0,1,0),1.1)]:
  assert not ray_hits(tris,p,d,length);rays.append(dict(origin_m=p,direction=d,length_m=length))
 return dict(instance_bounds_m=bb,complete_instance_count=2,distinct_old_models=2,new_reusable_model_count=0,whole_oriented_triangles_and_pbr_retained_before_float32_translation=True,actual_full_base_contacts=contacts,selected_visual_clearance_rays=rays,not_navigation_or_full_space_proof=True)
LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate(vertices);result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,.62);ORTHO=7.4;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(6,-9,6),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
root=bpy.data.objects.new('OneWholeSnowVehicleTentBay',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='true whole scene horizontal centre; continuous bed bottom at Z0; two entire unit-scale qualified instances';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
  files[role]={'path':f'assets/winter/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'scenes','assetKind':'scene','theme':'winter','style':'source-preserved-faceted-natural-ecology','title':TITLE,'description':DESCRIPTION,
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
