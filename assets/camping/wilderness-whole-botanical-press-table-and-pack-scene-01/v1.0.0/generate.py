"""Three complete existing props in a static botanical field preparation scene; no new reusable model."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='wilderness-whole-botanical-press-table-and-pack-scene-01';VERSION='1.0.0';TITLE='Whole Botanical Press Table and Trail Pack'
DESCRIPTION='One static wilderness botanical-equipment preparation scene, one scene zero new reusable models. One whole qualified empty lattice-board twin-strap plant press rests on two original tabletop planks of one complete picnic table with its attached benches; a complete trail backpack is separately placed beyond the table end on the same low scene-only ground. All source meshes, oriented triangles and constant opaque PBR retained at unit scale, including old tabletop gaps and all table legs and benches. Only whole-instance yaw and translations and shared horizontal centering are applied. Press wrap soles are fully seated on actual original plank tops. Original bevelled and slanted table legs retain their existing extremal-point ground contacts, not claimed to have planar soles. The empty tabletop strip and separate pack position remain visible; no specimens, labels or contents are added. Static illustrative arrangement only, no specimen collection, drying, pressure, preservation, archival quality, ergonomics, load or human safety claim. Rigging, animation and interaction not made. Original hierarchy baked and normals regenerated, not byte-identical original NORMAL buffers.'
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
LOCK={'camping-table-01': {'bytes': 69956, 'sha256': 'fd079692df4d487e45042741af039e4a9fd44909e84cc9048e20910fadd90fa9'}, 'camping-backpack-01': {'bytes': 71204, 'sha256': '4d72eb96a680ad832eff4cc7d2d6c3ae892fc14733c11303562c9c3196edc140'}, 'wilderness-fixed-lattice-boards-and-twin-strap-plant-press-01': {'bytes': 63712, 'sha256': 'a8d31f2815f9462249b0bf406c4814b885d2cc788546f3346a2fa9acb7216a6c'}}
ENCODED={'camping-table-01': 'c-rlq349bq_V`~_D=4DeC@LD`!C`>ROlC4cG7W+VC`17f1=IimqL4rcw<ul+iVC_Qc&_WMsCeT+M#c5M#r0aR)pgxf!E-%V|L^s54R0pX(+}|f+2v<vKK<UeYO1R1y?R~UT@2k5ClBwh0ia(i1>f%iFlboCka>lb)2CO}7xtW2II*gxs;;uWwyv;e;SrPSYHMnz7fi$|1&2<qsu^EZS1_<gMZwIH?vd^#rG-U>Gpp*RSJ&2H;c)lj!udso)5l>0g*}U1nqJs*)V#u)$|;yvIL!I3sIaDXyz@oznE7Kir{)z-shU2?sp^&=S2<;Bb<M<X^_62MS9L266;kmjmGxD1)s>S|RmRuO!0(1tkFOeE*t5QFMpe4<^vas?xUZ>W>jqcVS5BT>J#J|2jER%5OVi2Dv6a)S`qoaat?OSo&ark>araof*!e3BMZ?i(X-QFW_mW7XtZ=Bz`HRPkOUv+!q7e1U-G^xnji@ubOXqcuhf_5pkx+50tSmZzeo;OXCe_wd&Dla5N=j3^C<~W{La|7h)8lA~lNk+1La}h1vO>kFtXOF{R9aFJE&2avMSWG}<SjI!*zIsxX>q8mG*(&~qb|qYyjUn250!+;u+-obhs)x{;Yc{VZB{r{r%%d^*}gNzR&~c-kOg(sQ>yE$XSxL{>+9>P$Ihs)a?CiYV%Wgp11p9&yBkt5ba0;|3wwr&3WpyyvTsGj(0(Tt7xoO}@ljnfzIq&0iEIvKtV1sJYOrK;gVD?eW4ysq-e4$SgYnG`mSr{=D&{SQLcGcFeCKej9EaacudPctVeE_v6RPS)R9DS%3?ElJWhw@3P5tmWQ_*|TP&h`JGiq>diN{K)x!KMLmxWRT7Ym1D#U+ta9L!RT!;(-aj7MC&G#sa#xD(9r(pYgg9Ep_C09E5$Gpbw81|p@QvXW4^I3CBa55=NI-EuZj?{uwj#9@6Sh2$k}LP%gjzWU)UsvmAtKa#6{BwargipSFp4C~wH$UZ|GHBqt!qYx`~oEVD5;$`UeDET~8ip~qgO7Pf=lsThNmhyC{Bw9+-1s{dR4LDA3TqB>;qTA^7*fu)7blaUC&)<bmS(rIJUhK>~CE?Q2vS>+&A~zOxA~zZ>4n?CenxIRIW8_10YDsZvNv6|tG!QDL20~>KoC+f)&LA{uAfFG*1P0_iaEiC6fyRRn3gsV#NF>&15YVR0P4M~1nTy8GsjoV+s%B#SB<fxy7EfhWOqk$Y>R^fb%DRb!k&?1lcyos&wcRXf3$e0LIJ1Fpaj9dGuz_#{&w-f@l*UT3dJx$%8!$A&CEMhM5}YE!+v0_2F;2|e;ss}dk$VA8E+v@_;6YLn-;y3QY9JhmZh;R%(MXmFv65JH3nIa>H=}+mRMyA^=|jUkEO-MkoDuO{UQkd_yrY6c2M&SZA66y5xH4-0eDj?NDW9+=Zom1${UTof?Iee(u7s)X$R2&u?MV2EKK;{m{h0Peb){@<zu?ju5gS{iY<%^~;IU#RTTERElP#vM9~;|EKm8c%+AKDF8SC0?+<lqqvbYj48+Q@2Sn_4+8;cWPHnwwL`7s-7UpBsS$HkY8?NT<jNZI(x^i#mjvD5y|Az~(5UMd_VVsorfT?w0G!L%b`@|CIU$L83Pvax++**)bFHnvFF`0B&!FBdb}V(LnmY%z8H*w}9R>Br{Saed{>=2(!jIo8~<7BL%l5wlqGWpk{Ve)_Soo%_m<*;xCs@s&F+zHDrlvav<V##g4F0(Op_*Jf9XnQVEl;sOzyV{HT0m9RM$Ogj=LUzxu7u{m}&2$|WwPQuI<5i?(j*|kN?uCGMQY!|UPc3eOEvN;wu2-zHK?pTYMjk}0hEcvoI)=WSBnAyHg%51ECnfXe@%ytnoTSUx!C1rE&7PC9|ikO}2Ma<5{Vs__h5wml*h}pGYgM`_&oQT=AqL|%tx0u~?w}{!bpNQGHd!2;Yxmd*PTrXxe?jmNf<jd?_FJgA>*C1s!*1pWH6-CUh{Y1>J<wVS`6{T#}F2wBKdy1H?b%>a)MTptGR~0c^yAUy3`w}r*%MvkLD-*N3b|GeW?Lx$C?MuXL?Lx$CEkeX>twYRg+(pb{$(Pw$hlttQmzddD`!ZWA6ER!+5;0rL5;0pVlX9|cZA0RV8~fW*{_>K?6DK@4P{b6g#8g+pRClp{J>8CkCv<uzUDuCkUsPAh#`Ygi>ndVni<FJ8mQ3y>X0pZ9l`z?2>iV&<-SpFsDVA7l_%g*R8+Tu(x-70l%*I{BES7wk`o`kKmyPY*SANXK+Lw*5+;Q<`W4n}%EmAhVGW`^=bL_l2xKPYw%b_P7C}MN0QC$g}W5Ki|Ve*x!>&NEUk+QM<odcSP*w`Xv<Ext1mYB&FQ&+-di>d3!#&*+BKQ_mX>nmS2$AXm2vF47oh}pP{n8lJWn`6!N(~phq+*f|g#@d&SuiSC*Wn;UPjV)3(zB2t3usL>;Qg&?@F+0{o%#H;yyS@@JJ9b3O=3WuAxm3h#t`@U<?1<Stc0|nPUJ<inN5t${5HUN}#LUKB#4MJ4nH_5)W^=EY*;xBBo2y04=3WuAxm3h#u9mX7cM!9C?I&V(uOVV~FCb?3T2aL8-a*9d-c!WvUQ)#DURBKQy@QzDdj}D-druLwdj}D-djS!%dkrzOaThU*C0}Ou8X{)*o?>QW?aS<5RmAMxQ^f3EQpD_DRm6aQ-|P@g;%0;Mx4_AJ`>8g`>KC2OcE3+T#@_;)*Uc{Pe&?B=+2(?*wlmtdSvz)iJG>09mtEd`@6}E&ADF*feI=WWZT$P}d|uzj-i)$d?ePA3*qh9>rBVA%-R$zFeXo3hf3oApX5*gjZ+1Q(zigX);w@)8dE&ul<8J5hPj<XzlxOjrGe6fped5Pv<7?+QzOv&XqrCafD?gt<J>th^<8HI#B_ltpeLK&1Wyf32c7pk5>*gP3SH|3uoxip7k5@av{PTZf{$c$W%|F@Y*?8s559Xg>{t4!vVEzf_pJ4t8=AU5x3Fe>eYyM&D52E=eyS&-ASAH=6{NJ8`*t$f<+>)KYweycxJHh-DT>tzYu78?6+a^ids+Tk8pX~gtoqxRA@roaJo)^zQ+2z@KX3qTJ`scTue{gJVHom^|Pj-3pomc*r&Oh#a-e~^G&fnVk$E%&~<@$#m7ozzmyFBw}&UUu<fB*Vln}7b-u76nki{_u~@+_Wn=5O!+{uRtW!Tb}<Kf(MH%s-9pFGTZCc6qaJul((O{t4E9^3Ol)z93_6$<E)}`NylB?PdN6)_+p%?6pQE#_xB2!b{J+=Jf>Z_D0V=F^z2|jCS%<`%O%6%MGcW+bG?)M_ZffXX}2Xo%#hfG=HP#50{*1)Ba4Fbh<wNkv3_rsh?N8`%S`2Q-4TPf9_g(n4O&_{lg`;-NCU7(%R%xKS)#mQthSEq^UmHLFs%NptsXsDxa;t>XdZ+?4<!7N&9oWhyJMIG^f1AaWUHDQ$I;Jom`OiFHckdD4kE!cvF9=AKChA+#mVHOH)6ZP6o$L@~hD%pX@W`a%t*s6D&vlHEGf&P5rpcM^k;HQ}%352k{@oe-Qsc{0H$L#D5U~LHq~tAH;tU|G%&Jub-KU_gs4AsyB1S|7Dc##(y1_qx6&g<~B-~MA|s<oUJ3Iv*Lg1%*^<w`l)gNq)nP@>gUqMsd&$&sXt3lQ-8`HO2t1<uR{G}j`%nECf<L<{w-OY8UIwD?4h)mPW8XH9Y);~%V%qf6SCV&Q+ybI=F-&9PjbY+$v5%d1mmTC=J}1%)K5x#X?L6w)L$x}t*M{n7cWimlPmsBKG|o+BbPSuPyJo$rY}To($v2tc{JHU^^JDpDV+}DKZySz{)6}r;y;N0ApV2+|GmY39C|}@h~u^c41-Z{ILgDJ6pn!dp%uzjP!7Am?$85e57-w9pfij{IU0@x4NYJt*bQ1kTi6r!hC(<9x<V0zp#*wD0uF_KFbIagQ7{5V!U?b!SkMe*GuQ{3LJMezvK{OUZJ-l$N7)_P!@;mWbVS(^y1@Y01NK9?9}I>AU^t9HIR?7Gad0$LpsausAp%FhP?SR<2FId1`=jg+$3tH@1fnRTa2T3f3}q<GU`OZ$En!!byFwr600SX}G6V`%!XIHW%E>Su?uLipMwB<grEo8t1Jh7WgDc?_m<1Q1ya-N*1+WMnM)@$ThOsaKCP59<K|RccQ{hZl2<O2PxETHbm%&x=C%6u7f!kpX+y`r+0p`ItI2q;1a2ia6T9|=y22{gzI2SHNc_GY%^WiL*k8(a-05`#GI0NMwa2uQr_rN-o>tHcF0C&P2DDQwITmrYkT`2E@6>vXX4L6{?0Um^F;c{4xayeWNC&5x!g>n^C!4)tSrl6bx*T5XO8J3}329@wVfO-z)bMQE{QG2PTsts=6K|A$#cp2r(@E>><UWZL6H^F=GK70autM_qht{#IY;3;?kUV#np7W@_d1|P$};4}CNzJVX%7tm@4)lBWCTB`PH54Dea8`i@!@HTGm!jteKyoT~Mcp6@Xf51kR8{seTDSQa;pnL~Dhn>_L@BzvXU|01Kv{fBZc2xg_4yu)Ep*rBUulgExQLRz7R{w_G)vwS*?XH@rJ(Z<?f^Wf6-@=aS5%>arfJboqGyDuM!Sg7e2c_PGoz<7{CVUBx!bo+JDpDhHJ3viW^VCF?6V<V5hB{1zP=?ePb+9T`6(}o|t$M2g>Qt1cs>!NQ9i%#|?kcQGR8Q4Q9jf}PLFz~~R1H_hs}s~%HC~;pYSdIUQ_WVVsYBHMsw>K_Dxo^59x945s=BC%I$RAwIYh<O5vs2$M_H~0t4S)Z`k?Hirl@|ZUd=~2Uky}q)HGF#vR0k0hN)9j9m+a2Ld{YqstG73sJUvK8l{dwd5o%31?nhu9LnR=foilWR^3o`Q<bVrRjZ>>9<BCMYt<ua3CbnvZ1t*oTRn;LNp-(^O<k{+p<Jfcsq@vP>JF55sH@c<)lKTJDF3RSQ)jA$YLU87U9A3~E>l;iKdBqkEo!y8OWmU$R1NAe^|*RQy`WxFe^GC!ch%+UEOj2r^VC)9Ty>FJj&iwLtS(VEs@qZCu2!g9)wSwMlvk?T)KhAux(4Mn>UnjY+MwP+`Hs3-y{TSSFQR-=y{GP0&#G5YzM}3^udAeb0_79xEwx@fr0zv|ulloEpw_4dP(Gl}Q4g!7>H?G(s7KW*^|ZPZ<(=vbwTCXypP~FreWW7#5Zy^faNAu+^^W>W6~(Qi{#1RZTA*y9e^sD&(!Dg`R;2%?K31Qojp{4)jrvjjth8>To9X7dwQj5T)cfc{eSq$&yX#^d({Y{9KdBGZztm5-{i6P%HmPq>eyjeezE(~3Zu)DroBp@jMO*qmDF35&)t&YCN}*J`o8Cc}=yH_hdS_jxL%Ijb9@^Gz^uaoeGOXL{QoXM}2<1V#r`})hrQ4xwrw`QctCqS0$`1PPYH$68`W)rwYCrvh>Y`hrY^6U?v-JXfq@ImiKYfY5T%U{bTs=!K*H!vxlt=6N`Uriju0>g^Pt+&rN%{(uSLh}BP~Be-&_nc4JzO8JN9(bAf<9SK)^)mG&(){tGxgc}Jbj^Fs#oZh`YJt2_tk??4$>#+!*zu|2IVn&pdO|t>Kc?adW1ejkJDpNj?q)}B0W-9qO8;x=<)gw`bv~n>T118FVh#HyhvZIr|a|e#V9Y<GxeqVbiEMeLVcM&OV86YP|ncj=-zs&o`Z6ZK1`pgkJ5ut4%TPr<Md)Z4dpc5N57%p*Q-&k*4OE;^-uaADF2~f*Wc<t>pM~2so&AJ>ihMJC|}e`{fK@_|BUiy{h9ugzCqulZ`XI}d-Q|)Vf~nXLO-LQ)34|a`Yrvg{+s?t|4VPwU+919@AWVGA$_gB1?4TeLEotF(D$OeSKqAf)=%meP`;q=)6eSldL7Dj`g#3{UaKEP`KbO}Kd!&g|3Ud5{j~l;f2lX2+@yciuj)_rS17;If6?FR_w>goKh{6$5B1ynHI%REzw1Bhm-L$`-_+OZzv?ymHk7yN5A*~2pZaB#FY9Y`-0E#Lx8k_%U=6cIS%;%M+$yz>u@1Cap=@Q9Tf11hTRl+ru=ceItj^YGl%uU9Ep0WicCvP}T3c<cJ*~a1LhB%_t5sx$trDxJm9P%A`dNdlA=XjW2y3Kug0+`rS<O&3v-Yu?S}m-0DBD>(TWzdPR(F)$t@hTz*8WyUlpU>Z)&Oe{Yd@6xS%a+utl`!elw+(e)^XO+Rt3rm>qIMJ9bpYcIn;_-$6B`4A7y{*c&o2<h!sT{wGOkuDz?f{mRUPmy{wkjt|)i4`dA&TfmR4*$Wj(POYw#0itN+xt4>IH?$@2{qh1^*;`QHlPA0DHVlSOBRm4=c_s0(((r;ZWTgr5sv2sOw5!1d3#t-VX;p4U<rn*DtMD3!n%M%i&x{p<a?Ry_xDPpR-@Yjg_THC9|Jm9Hj<-5IgkS*m!V@8(0HLSCUsc!=+%gYCKJy68AeAzl38xrm^x<z`dB}{cqEJ@jnwUkXPNtpU(Vnf1I*TjaD%~(sA_GMy8!c^D9hJ>lE8EXksT@y=Err0>=zUl@k(^!vqah!-vEUlO^Rm8VaY~WZQx~^4H%=ourMSBr<#eD(B#w#DU6|sqp;<3vcB;45@>$Q)r6tRh=H`-n;VzMQUvC;gkgOXBSfMfl}u+AbT+v6BZ1G*k4;y&)VX(7gjgdcOyHJ9R8OSq4FE;|-uNy6q_Lt`ywH<l#)xO;A**pP4^_uNFWA!QotH*u^b{Fr+#djMle!p^xHV`Ep04GGh^rnfuR5~jK)mLz=DrcTLK$1io>IU?oD&$%=)t$dJ(_dVxehpDcFsqR^4JeqDt!so1hDqYu)X<t-V%FOnpgqbZOX1)@$Ym1m&Ux}F6F5)3$Tc%?}!p}d~JU!MDrn)AUq-@4o$|ja1Ono!4Az@~FQp#qmCCq#!VrILDnJpq_z7p}8y3WZ*9x1Tj{-Gfu<sPr@Z?E0w&myK+C8oL(rn(ocElIZ{;a{F9P1p5f+85Q8GPAuw!ps&CGhd0>wMERXuSCpj7jdumTBKt`!W64!tR+l!O)N>-jJ1?aEJ>L9W@1Ca%=QK;o3WNK^OcC1?ILEjh?x0G#CUCQv-@-rvwLk{#(OK9-Pijv)n)hHB4+pUzD)aK_vyY&b=keSFH>E1-|fp(m)+NknBAv~nB8mpGWCt!*ZVTPTZ^p?`Z8Xt+icy>m#HpWR}?W@_Y*N&OY~*x8(SyzWva{82}R7-`h1!8#nu&lnd-8&L0_i2Y~9b7sV-Yr6tP*`k+NCak+6v+THBFuABqk4UR%uW+Kz<rUf4EkI}$drLHFhoe%u{vTHBGZi6vUwkucd})^?<9?zJUMwwtvb3E%3Tn`muE!d=~S4Xy1+_*VB^Mr%6~Hs=}|YcadAB;n5Pxrt&!!neBTCW;Lyo3$MYcXiKYw6-H*=iKeC?MRr;HD+x`!c^D9l7#VI%x3rLB4+p6zKqvqHoLF)Wva{WyG6|I<$am<#qQI6nc1F{FtbI(%vWM&_vs>L_uanCY!~rWn>yKSZP1tT-pyv~e!fg~*}9^L*}9*I*;=A6Q{UJ+p)WJrlTv1DeZI_mC1Pf~h?y-SX1)?J-iz7nK3&A@UfY)`R@r^MFH>E1-z{QxFYn8=FLs~q%gpu$2{T(n%zPzgcAqX{cHiyG%ytp4sq1XBwLxE|SY_*ezD#x5x}u2Lx}S*ITB0vg-`F~#FEiU4q|Da(e3|)5#LRXPGh0N=d?n)VhV7rc?dc&2eQ?uqDNk%OD)HITaS>0LaFD}PSHe`cX!;-0?MS%U%FEJq{h0Peb*0Q~UngN^i-?)8#O&H4X4h9DX10qM>)I?fd>QN7Y}|dB>aw^JF&lRgvsm(F>Kls_UuL$ilQJ7?UuM1%F|%F7%oY(dUx}F3MV@KDJkj)%dgnJXz5iBeuh{fO!%;7_Ngg|KdSc_ZhbNcq5KVq}|GxGs<8NumE>C5#PBObZmBl(quXcEu?C0{CHi>CJxW9%kpKX);@cYA)Uz|KWtFF`MB-TmfD^F#yPQt4lUM9Og#wTw3HrY>hp-nc~#_h_^r}pT(OdmF~H$nTz*S=}T^?w7E<F>ngZlF4uwq&+%>SmWW?R(|t^N&aT*lgTw=AWGT#4H|cul8BIWwaxR2b+z%o#mfg@s?5EwC|Ol*=A<{J>th^<7@Nd%Of5#%CqsxnV;EaBY)<KADfMP+LrA6toC!->k)4`+hOBtGhZdx_;Onk+2!4_v$M;)<6?WY!^`C8e*^P>lKDT${M=yr@A|MIUwPM84PNc=G9K}hVDVt$(`NB(yYpK{zU${?rVn$DS2ADwrX4n>{8)3!Q&~DTGHuCh-_*@6Z`$|D&*vYH_(`&HH*>FNK06oK9`jpvyk)fG7Z2>blVEdcgIBy|mpAQu<!82;^Zb<&KkWR{!2RGA5836-xOnAfw%N#^jpB!$clf!uQGQnY$vo%NjCk{EC*O1I%`=y!&#~v_`E%@Z<!{Y%q|GyYrO%P(<@s}@bG5TI&#^bpn$LcYJ<s2k=h)|JC*O1I%`?rV&#~v_`E%@Z<!{Y%?Af?yJjb5rZ_9J+bG73Y5A@t=dge4~$#bN$%d_XA=gi-l=h(CH6+OqEm*>y1&y~NW&yi+!WjrG~JAZ4RBkk2r@E)<?IrhPORD<^z{x{!a7_9#U>p#KzPq6+Itp5b-Kf(G>u>KRQ|NQT*|Co11x%b^k!To+ld3HaWvz_gI{fF5ly8p^9&)y51Gk<$u|1tMWtUtc*5##0gd&F|(Z}00r%&tc7G35E%@*cxn?F8#T!TL|I{u8YK{5RKswukGVp3k>Q;zn9D|74dp-+Q&Qy<h(@yF~L(c6rmjSN`^X{bR=59e3aPC%e4)&MSX=zy4u%Wy~$v`CB{xc(v2)_5BlzK3$gZ(#=uRbF^<e_OV34=oaNBy&BWzIqD0soY7RSyxA<<=&l>~v8i4zP4yGaj<r+u3+!Ud=i1b#zLGX+u6M!y%x$|d;iaixq^UoTeLKL;PN(`=YNzaiv^M#vew5la_A}L9DouJl)~9|XFr81+bJR&c=9cGrUfbIpzj<kT&baaG**WxFEN8~&`_7{qrRo2QE^_@#X`@X(^@Gy+G_^;1p<AA7+8_DFOQ-z2lbz}pq_xQ>`%Jl9I_2k`od08O(xgqA`r)T(KU~xPO*)AGApU>P@&E2S9TOu9&q#RbIfGtGz^0A8-orHc!RXnP@5a9=_iD}Qjna?5wY&ZP#*Mvl>GXRvu>Hl0M%q-*q)D6l6#wf{Q#xBye{Oi^mxPz5{*a!F{V7`3+s;mt9g7yl9Y2s?j5hhy57N}XRC}p3>26q``bX(}n&O}OOZ&^#ty<mb_{&REe2}L8=F-&90}97F<!M}uHu==g0@Sl-bxQk}r>TEbE}y3MsJ~P`Thso?FJ7ABVD_x0cB)^H)+V3qGv#t=>Mxa}{+cvtlcs*;)6{>e&o%Aeq*tx#kXZf883`}ly4A~xN1l7G*JYSay+5Xd>*tr#@qY`JYl-Pw;Pgi6*|RX-v3@RX;y=~?arW)Mq{fHRq)mN_|5>Ohovo>#Bh)VmFHQX!j+**2;@4FC^EBD9YE_w?vJ2AM<WoN`bG|>$9<EaUzs$|2`qU3fd+AjFQ{_x~t|O7V6J)oSruZ=aT%AKxKPOF?kO*UW?Y!?LrA<EdlQjJwoz<>?d7An`X)o=Llan^(xu$-SU%WKM&x8q0Z0Z;J)o7DX_NB)oho=5gxhm|hNmF@~rhW{~qpAN?pKE7+bJM}~PjLMcT>l60AH;uf{U2Qa2iO0>^?z{vA6)<cey;z&8Lbn$wOW?&(p^Tsn1J%#5BVC?<OicWQ@$Jjt=)37X3c7p{`BZQY^tAAoB1Ep>nELPQ$3R=ovx36q)nP@>gQ)0HzvF^_2&!J)SpF*QrAB`O?v$#+i8dVVzkMpemstv`nPdo>iqk-n@{yW!+uaXFP-XtZ%0%4Y`yU12FG7sn&QLwv!#b_e(ijxJdKOdCZGCAI&o=%y_@S_o~C|M+Dp6R<Y?Mowx<1&U%WK+qx@2^&vp8>S(|*a&y>rho$F03NB#ZGO;f%}Q$IHPXsXXO?cb!!ocE}f;kIL=_o%i+*%EsFrteYR8RgCy?@?{$`5x7Q&;j;CDSMA<w9$K1V<=<pdsO2n<FEsiLo3)7CA~*=4;TO;l=L3eRnB`<SK(IG=sl`aQBH*`e$)4;R->%Wc#rDIp6^k;8RozlC}r<aUEb(Dsw+^gaNnc466H!54_Cr8n1YhtqdFUIf@LU!_oxQ%QO$mj>I2SuR3E_YoJQ|aU5aw4diXbekLqHSi!<J%dY<QdRG(I>)HNt&?@_(C(R)<yLwTS39@Vud*Q&GCI<-t)fRf&$x>7x*?nFuNQSIQoN3{cPe{b|2)h|>Ox4nPU_o)6;{e&BTkLtfX-=o?^|DY5~*?UymHF}R~dz9_n_o(iHau5BH>Zrd|pQEJrsD7_H>sBa(_oxQ%Q4QXsn)^MfJB;X_ta<f;#JslMZ7=@hr=5M7$`AVd-o#ZWcJX8?@5faBqO(>f&Y#@Llc~HPQ~3=Yu1&X@i>bUHQ~5QKtJ5~-Vk+;)X1^n!4tuiMZ$37DIOX9IPd0wY$7Wnio4MGGOFm|ClJsI0C!Wmq>&a}tp3MB<$;=O)%*Mr&*|>NzixW>~apK7=ZataBttYeN$dlP|<jL%~_GETk=VP1ACpj70^kpi~=98RE<^7n-v-u<^Q+Yq8@@ziI$yDBtsXUucax#_oW3ylP_|3^?zxmks!JSWXvhhPcHsfO2%*AG0@-d5(q!+U|@np7NPiFh|WabA?W`6KwHZGpb#>JCaoOm*e6HjJw>&Yx`J((Rxp3IITPiDupC$r<)lWC2z`&pCipEs>fFmCjJV?D}b{C=Ch$M2H)+VLpk*$#c5V()fXne28N*uIh;{mE6v&ayqpY)^XlCs&zV{joF4=j=~*nOy#{Gt1}nPj(s4b~cZ%cRQ?%Er^XEeuDT3;wOloAbx`Q`Jav-`gb)q&-pjc(HChu`~UaRza^&fPjbtp^oD7t*hLq%HEA&VrVsy;NagoVw@doEsq<a#?UqmJ0U!LBNO6H%z98K`ZEhNjruI|$khS%8_W|~1+fw~c<v)^0<)t+BG1ZQf2BS}!c3pWYe}P**rBgoWZPJj|ukYW>wZ$zD>Go580Jl7(+jsK={|EjL{2%!Lzv6!dJ3uo~xHW|)urstk*#erwuFw+Np=<}Op$)W$y;1HB9bgaG3kp#d!oIK%><67uc7_9?73=~#;-?36!4Lfwq9g2%xvemdaylX%0G*&4%5KmV4u<Yvp|r3sMWA6P=NB1monK@W;O8LBEy6s?DL@K2zs(5YRthmFLjz;D^@4Kf4TqsT3=W09&>xOOc_a*k0nYC$2H;i!L*Qr_iE<<y1AX8Sh~no&I1WF<U@(3T$J{=cM>&I$hQqNi#`)dG@h}QbfC$P66vJo;LmWQ|=;!=G<S6GCBBSvWcXEzGs)X@yGRl)-B20j4s6|-|lVJ)>g&8PkKpjknnQ$t~Q(+FwhIw!%$}{0~I1SE#MJN}+IWP@Qfhzo51dH)Qzp0oHvoLoW=26akq_g2%xB%q^a2}iw7s5D{<KQG%0%Kv4^UIEU=a(G|@UswemtY>{EI?Z3{KjJ$ZkNIeSOr(3yc({6E8&lDJ<99hPjD^V0IN~1hMVCg=XV-6;dTey4tK&@lxyK$xCSnV<@ia$1NgZcZo|)wn0pQ8QO<2h_rU$I&iVbvgYXbEz$GXzfu-;;TnsDma}`|Y{L*BN^GlP5@w3v&S%dWd0P=#cO8', 'camping-backpack-01': 'c-rlq2bfb;)A(o3xfB7BUZl7zMWk-FFOqu!l_I@JM_FKL0=q1|gD7GFL{I@6iUOj7peQ0q5V3)X6;wdMidet`idg=0ZgRp&HYd5^{r=DQzV8?BlbPQ=nKO50&g5ou%q}Cw^lHlhpk5V(YGnYf?b)@<jO5%26Y?e|x0sPUB5zz?VeZ8I!sHgo9Y+@CkISEsG=ioiwHcE)ZdhJnQitYUlP0G(OKX;%mE0tGa$eztQTgM@IJH?y@~kGw6NZw5<Q6FbnvmRLz>MT^xnpT8xu^YHljL#v!|W$g2F)6D{%l6_*t`iN?WqC#p}AuVMvWWMbV%;d8w=>sG{u!HW{l09m{&L|cZ`45u>46w#^m)JH7svfa*K(Dlk$S|C+6jjq01EvDeRm#F?Y<EQA2y=PZ}|jqM9I59g;gC@2dPU`GswBhuR4bNNJXmk)C7!mzCnm$;!;i%50L-%#|G&%XDRAyV6r>C^g0ZUusTvN@`kaYI+lw2rO_J>5x(>lvfOnHOo%5y=AARxl%H7ax!MkY7#Ar3Ay8j#hFEBwm-ToS4L_^MpilnoSs%>DAnapD?2+SD~F!=|ChqZ{Be2H;>;mE%YTWS)GU`PGcCuCIIubyscEjv)NC>2O7Rb6W~I8a($h2kwS};!P8b>5w!Lx-@(S~YC5aYH8j?S3T9UA7mO|Y~DHV<yJ8I&n$$=@k6DJmq8Zv2Oo}E{>u01>S>d>`|9YB|^Jvz7Ul-$DAB)Qi$eXr`;wa3*rq$IaUr5DYpal=Lp6;smAH#f}@Mb$Y>KkqOj)M2LTFiUmlismr;yu+MOhprUWqsyhbOr2%FhI5C~a})9l{Y4luY54HG!rr6urr3!O%^zDp4KQwEuW1ET&kR>;rWl+wj&3+<sVTzURC~!&18bR`>T+dgreuoOUZ#JILY6!&!*1n_w9NE$S9VI8ShZ1f4;s)kqK_s`BhQ&=hm+j<nyb>1MP<~mT@J#IHa|74`Kd+br$w5d7M!1vk{+Dj^QzXJTK6d8Aw7Bo>Dg-GGwkxX=;f1^k(QQ5MNZ4K>*b>RMuy9ko|R$W2h;50()}<kD>FN^?nPa=Qv6Golb({6Lr-Ujg-FRs54q{YSceP;Swx$k8Q1)x>yQ<F9WpahVy#1V^axyZKUNkZHE`#4xpGodazqs~seE?lW~EYZXXMx~fRvQ9jGWBO%rsh<l(ejng(&JGB{Pd|plPYDl<aIOdX89!)U5Qhw2X9Dx+}|->Z0)&3z6d_ji|4vl=wUpT?>~h`eL}~rCnq-D6R88)Z3GNYZ@|bVqT}baU&+u&mC#m>4A~1!-v~H4T-hQEgT_`8b34jd_WE+`$wG4PtC{-n@=yWIOe-jQnEwmyHZla14xVFAR{Y00GBH@J==K%5gcUML0xzWQ&Xu3an!)RtA;qB*Jrl#8o1K3=?A$`4_P^>afMLC1HHiP#&+l-C)Jf1>L7!DT+583jH%gSosdaCN~MNZA^5roye1S6)Ogt`^uC^ybm}66HXXV^k8QP0@c%bg$ESX+YO||<KaY-AG~qVC*K38AYc_hxEx7%ZXSAH*?$TWF_uaQ?ne08v+=xuq^(rw$WQyOb<Pwpo4mLm0v-u_+EB0<3E7#Ss62F!o-n?T|pblDA>ZxUAU9_yMua<B5uDe<4U|r#Nt`lB;w!O`d^EDnPTzXbhn_JBJ(h;}4{WrJZ$^8tk6K+3bVROOb-K88c&GjgLVlu_%RpN}vl)G1{LrkXH+U%P>f0Gkd=DMA*5}PAdayOlDrMu2<3e?sSD{JS7mELeWVWsyR@xUc*%!6xAiPytiCtU2B7B-jo;{lHo?z%V0W>3k(j(F_YuiS#0fAzN`zGDB(=7P7?F6MQ@G}oi}iOCe3SBWzwQ|?}+4l$W(YxA$xtW8c>nd^4KN^Fi;$=wn6>HN*6Ky6JYtgM~e2`jzfh?U-R#IKxgXx{Q&c}w)Rj-TFD$L1&Ij`!%e@|w~%zt#E)E%$Z5?iReO!fq|kxMM(b!Ta8NOUq>MQRYTux~^A=AtF=!UL}`^Om(n%$J=c-=~%IM>sYz2mX-LmT=Ua6HU;XSWu=~4R@Oz!%KB<KEiKJk;4WpoSo;>od~i)UOZ=SUg!jGG$!0Ov35&Vyj$In`<AgW1s}r0Xi^a9X+-(k7$=&0GWiHzsvQjI@9LU8n2WsVrW$rSUSWI(Gr8i<S%{2qLJ7O_c=_^O9th*ytdMPH0*aEpbVkLKvQ&!eGCd*m{)+Ht@xjSN+%QlCs)XEVDKH~a>?6sn{HLZ4gpJ&b8ZiPc^8h!S;*=$%BU#qQecy%^O**(nPYqaxCu3XKh+N(D8m!E0*<Yv>i?%_s0)m~>qyhC!B%?`znH<BN9oZ|6Dibox%ynK=JQpVjn8^w>Q+H2ymRC`TcmTIr5kEPn{Y?L}%n)R}j^)fZ<Zfg1@q-QX9w)N-CGVZ^V4!ITf==$ftv}>%2=_gyhup`;0+N-_sb@46ckrVf{G|uIR^p!eS?U~~(+qx^CY14A?#yLKnADzA0S2XU4HLms;`S(iyx^cDND1M)eU)P7K4b{gd>!a&Q#m24L>-tmiZ>e+D-c#Za>05QK+J{PgES(><Kb87x{pjq~9#+;@JFfP#(m$52&s7_>x0kP*Z1t%;!(7wwu*%y0pIWblRer|3=F0bL`_#VG%=PSk=P`3hj}_*&YQsbNR_AB-yev0+a;f=GgGnL%tn;I@r*V%m?uj){{=JI-V4v&8DSn?4f3UZ8<5VA?QlDTyE8}jBO-TPM{w=j{RX^%nCH|1U)%j8C6VkUjKT7>W`dQ~kXRoYpNT2J*mHx5R-qww)eXjO);61{AKheDwR2#K#bvA0Rs`jdl+PA8`&PMIqFdL8J#~aCyI<EF-SYAFQFJGj*biJza6Vj8KctZM6lUGRZY3dWwZ#o;bmo)1Y(m$GY59uZG+^<H4j~*dEla$(9(I*}&->ql`o)6Sp{^$2A=Z4z{p3{zp`kWi)JH)@RwGO>e(Kl*;MN2$XKdOy7FWg=}uk#bB2J*j1vC@2Bz?V;bK73rAA0yuoTb&;@UNzr9oh_=fFEp1T{_VNp_R_y@+(CV;u=)hoOpP~uTwTBLoTBxc&X2AiL{5RctkCBp_glEV($5jcBV99E{{;N_0(G_`yuLzeA8xO#SH$sX^^Ei!)zS*QE_`Y(;p1Wcttjgi(r-FHq4N_up%Xfx6FQ;)ujq1S&DWQjI-R}v3*xyg#W`tH>Ky;L@MG2{J8@oEb4ro(FSE;9Vt$yG<Mc?f{Qd`8{_7@Lem{Qw71>48Nb!7`{iCVVA|9bd9*e(dZ-t-x^J{7O^Mas0KQ7`EdZ6X^mt^_<`1Kcd9xa2~pI57pb77~`2;1yB>oma5;5sB}G(Z78wguM5ug{N*_=T<)tgm|RkF!9l1M6gKVIQtVoc?-8*8VsQ%O4j6_4)Cgww>sg&m(Amyav^&Ua<b^xj#Oz`$5=;Yyb0xrPBaSp%ERILp?g`Ky5l|Ks7olLj^i6fiiSl1jXs#_G_k*ZCTs4sbD`_+#auIkCY)g0?)v+bUY6)(y;@4bnJpx>39S7((yLDOUDOrkd9Bt`Uu$yOP_7C*M9b(J^rFS@-7jBVvs>H16*K0NoYZ`1*Ag>C=Dh_6SAQcTnw#9wt|*W7RtfZB(H`xP#!8mdy?&;EmVRk(1~OxxE89yrO=&Zcjye&p%z?6@;c}SH6aQ5lk5+@;4-KS*OR;+`a&`^fFUG@z(A-E4Ph9`VK5l3fW|PA<VY9}O`sW!Avp#{Lvuh#A(;YWAq}!%3dt!j0W#rAm_c#|OoAM0i8&<az%+0}YnVrJ9?XKP;2OAv<Sj5C+Cc}njpS``D|Cb|u!!U$xC6REPgq8B87zSw&<E}#c^}*jy<q^{Px5}a2l~Mc@G!}TVI>TLp|FPJ8h8+LArBrW`8YfRBVZIfLGlS$2RFhvc$(zX@Fe6zDio3|giSCWCc{>eTVV@Kgz2!2<TiK?rowD^iR4T00?dTD;34UO?Qj#^3_D5g1TQRrh42c=SKwv19qxqJNWKQUVKFR)JtX(Q>u?v`3;Rg!gEwJ0tb%t)z5{Q;3U~<KC;2|?hX>$MI6(3Mya%h{G5Cn&NAMx6h4pZV<RSPNHo#NxDalXaFl>YZ*i3RWd<NAp3BM=#J$wmicqLwrY4oUy8CVQ|f(&}p!tdZWxP;^-_zwV<#Fhy3Xo8=^*KizugrDJ8_yhg~hQ+ZImca^G2`|Okn2hzX5jMjV%*1Ro@f>^sC*T}C{)TVhB%CIB8oq^Jpaho1U!W|WfzrtFFOq-3#n=#k2PBEu6b(#AH%T{MggNNK<|Lb=g%z<erjks>Dwu_rVFQv4um#q|8d#ZRWvq`!p&V8xSslNEns^F+Ao&B-!Lx7$mM2*rkHOe)&UrSrJLbNvb&~0nw|6LGj``+FN4#ofb+2GC*9nWcf6U$x^y7rT@4hWKHx`R)iMdW$=01OCDMu`Gamun*R>r4prz~=jbDglrMb3@IGItqgET*|`r8i<S%{7&EkI7=L(pQdHS$9XQ^ioU~u_=8LlV$E|tzxmV)-hSuDzGjwS?2DPWiC!x)=I`1i*Ik8<Slh@jrq;FD@><6?c25H?xYk)JYskQo5frwEauL#wg&w;VNokNHx`R)iMdW$=H7HmEk`VKamun*-4<1K%pw;#*9nVU<lI;+bC+?(;?0G}J+e2P@R^2(J#wv`u$U`*$tlaVcFMAsoUn*Z_J$LdxvRB`#d58ku&kAs>x5<QPFd#Slx3}CoDSHn^ob)@);cCrY;L8mVzQX4th*ytdMPH0YbkvalV$FK+Qwv=i&K`hl563Fl|FIA>RQKQnY)ZL7Sp}URNk9nGTpmO<$Wh6i@D1Cnj==;cO0?uUKW!@Y|8soOqRK;wTi{cdreH1wF<m1#AKPfQ<k|nWmzj3XDm)FImUb0E#J9!OkC!6%166iYz|zq%Mri4XP(Vst`in>y$`Pn`f<X;hp!FJjm6?xVy;tGa`!l4B^O7m)XFgja&gRoS~+4RcSmgW?h@<`C;Z$SnZdPo!eXxMC8sRc+9}Ika>61u*&9w+$=&0W<yt#orB;qu$=wkvxj15_R!-Se`os|{YaNp*HdE=Vm@MWh>+Xn^UW&=$T1ub9WF>cx6IOC@#7eCkv(hJySY7K_tmN*9>E2~3?@ck8?p>zxz7vzhT;+Yu5i9RIj#zmwi^(E3<$Wq9E4h1|vhrRNla*RIVkLJ+tmNW|m0CGs-S^d6?5pStJRE)BG2C8$*GV@X@An-8-~V&`eaCQn`Ml20g?!&pekU>f`;O}Pzw&*@NPcwRSCcgs+R67F!|kPi-FUp;ca%N?>mH0ZeEdSc@2K+=r5`M1-D7^=G2C80ryGy=`;PLve}VOl`F+Q5d-<GhJl^j+2I?u-J(x@Q_=SGoQRhe3Kk~c2%Ii1k{U_XBURyUF@BK%7pHzO=)ye%Q++IGf^Aqp=N69PX-V#23q4yu1A6@?_c{#fOgxgF1y774LKY`b1k?&iFk6-BhN9QL>KUm7T$Grc9+so&4<MG~ql=vOpf5PqMbGq?(?>|ajA@`Q>@e95G==>z^KZ*NK;{KDk|NOh%fBxM*fBn1tzL}C&$h{?e{6g<PIzLf<U&yEYK2Oa1Pq@9(&k@J}(?5SHzwhMe{u6Gmyq`uKkN5tg#P8_-6K=13UXD2apY;1?iTh9D{*$=>B<?@|8}}cxR8@0orH!Ue|NP!Q6MAfGDbB_3eMoJO2Y%mYdcf|L(<6(V-&&=*CFV=LP-vPbwf*}WG(O(l-xAjo=YBtaE#^hjBA%PSd)L%y5s%O!9<x**EByQ?(&ODNEPq}Q)N)+JQ9!zY;`94UviyGhTI3<@q_*>fRw3uYPN$Def6lJ6PK)1%nHi{OBrW3HeR`z%IoXSKky?(6ICqj>x~qP$zUsM%Q`kk*!k>s&tZTRyaf-U=w21SrUBxVaToBZ9T;#VPV0Uu_E#eh+cTv2N&i(ZUyPgXI=iyq|>-3NxYLL&>rcS4)y>G&epS2unpU*X=w#NhgFYMCn^MWGhBZgP8#Qcal(EmwvzTW6(iFxuo@OxR-aN7>RZy)fdXb~raqoz*#<2f3Lx0@AyF7$dM$MWX|K`qBc973<9`27C-=l=M**>Q;TXj;4;{CRXMqPtzR#jcl5i~b0%gGN74VVK#~wx1i+a$Ll@nsncD4TAMm&qaK~E}9np{PC_XqQ&(@U36N+(f3?&%O4j6wH){7cQnv1MYV{xAK8g`W&OptJQwlB(&9R*7T1^OiT+RY|NrIwe{NnEbN%ckrcQrmylqb954y#<sDso;X<YXITCzJv=TEhoTIBq$zp7aUG+)(Xp41|rku<*ihEA5ao;dgW@#`gI7fo-ac>2yeW$LtuM`#gGFJC(={9NR>{DvmBA5j;n<+zAr8R=ydpWk1S<@e*)A`f9F^%6U;Rw3ikE|PBGTVdB(r$v9rdPdSB&c3r<w!K&vspYtcvpwmttJ8w@RnJ8n-RL};7XE}@8?aY(eY&2gi%yF;#;vYs`Qw71mg7kI$@Pe&MZ9ClZXCrM>D*s$u<I_*RW0Ha*U{-j|0nwY|8oClLn|l)+4L}=Ck%jgB-=q2TnF``JjwFlhSE?Knv-k}mq8LVgn=XnLMLEQ97;l2r~sAVQmASFK71o+0;!M=E$GLLHgGju3tgZa^oG80J=6dWrAU^7+E4;6fyyK+!$nXLE{A3$n?V(540WLv$y(49+Cw#{L$VHZhI-Ho29X>DS3p1L4qZuhg&QCZIzkVUJs=bMfCX(ywuSz16<i4!Bs1U|Do+aJkj#N%&=ShQ#Uw9=)=(WffQzIH5LUoy7(;Rl41;IkC0Ivt9oz?7;THS1+{eR%a3f5CB_x-?9GD9WVF$?_@DvPz;V=@$L81Md@H62iSYZEN``z|$u0I5i!eg)jHo`OTJZu9m%z&XVn&fDh4I>~QCXt*3qhJEu3X4fDhRJXT%!gSdXTc&^4^v?t$$9WJ+ziiwholE?gBM{lY$CY{e6S3jge@euz`gJSJPd0|u7&Ne#{RAUHS~BK2E$#jlH^Lrg9o4h#*!QhkH9o|0+y0o3c2t*0KP@?E!Yheu?CjFiuCvmD&tr1F3ES{FW3tQ;UvkE@EIJ1<4_Zi(xVLSg4f^;cpKh>58x9x4C43XPr&zq-;@6v7#dg#%VIgKg4M7#9)ee34;-S$r|>%LhYv}92yeps@D2P(@<%uT-@zAfgya$U0ZQUWaE#<JxEQ~LN?40zE&LX$V|ly;tJC8$`~^y51(Fr;3{=H`pg2~=;&>@?JO`(N<7p^{JK+?Zg`M<x75;>GU?0hSfcP<7gg?Q@@DscYeQ_{0!M^mUhZArHjvzS#``{$J23;gwI0zeK7Ir1s6)kLq?Qtf_nK%ZMu>m&3W|)fU*aBN(8*Gc$Vkhi@y|6!Ck3(=6j>d6VfRk}5&c-XTE;b_B2u-{kn_~va47>u<upM?G*#$GPBVL7Wl5XsbBQYCWlWdJ+@oJoivq;Xu4mb_RV?N1zoP#~_Ml2**h`n(N-hjhN4#(*@6bImSB(K9fOu}y1k7Pfrj{`9Uo04pbxtN2ausg}_SO>S^PP~)kop>|8kB9JelCR?n_#r-yOGz$858i?I;U<!s@L^ny>+vwj!}u27gbQ#XF2=iYIj+J7@KIcg8}KRIg3sZ0^x`hujeGEId<PHUNBAk;kMr?%lDFeScq=Z!dr01cx8X8ehZ{+5#C!2cT!Rmid=Q_;H*f_$Lh=#ZhmYY0c!cB;d;&klcX2<-{rDL^i+k}slJDX3co2Q~8p+r26MO|<!mT8?;;T3ppTQSNzKFNr4!jE&kz9l?<4SxJH<R3q^Kk!f6}|i3y3-u<%{jMIzGC1Kb6f>(I^l&?s@p8)I$<%l(#8^&^y7qgoi1s~xv^MWOU!l3GWTIue&&c}E>2n2>X*MhaLghXIoAn`T;$wXEOVD}#^Q?eA=n#Ec<UQyJaVm_u$U`*$tlaVcFMAsoUn*Z_J$LdxvRB`#d58ku&kAs>x5<QPFd#Slx3}CoUvH^TXSoZOIZyX7Bi#q{@K;7nSGyk>-a#o>fS-eOIn|tI;Z7>#0##jW|cm>E-LStP~7_6^;uN@Wq)O>VT(JoEMl9NQ_NcM-aAow!#$O(aa*Tpxk|4y9&z2@=(;+tN-VFdV_`4rpkrY#>QIX6pkoo+qLC%7U)mP)M&s<>f11bhbG2N2RFe1fjAB-;N)VMx&N^dOa1V^i3$OXd{Bq!T9vzn;Ubp9jIpSb<uZ~4*eaD<Nvwu74iN;fY`qEtbSSPQJU#NTBBd@FDZN&1rI)0w`*FYU~EPTp3=(vz#8*uk8<|C)`wOl}4YvBXt=1F&IS=6d}ji1d^bB1bJ)cjDn`^}G9EYPyBzo*Gb^UmehYFXI#NnT-gzI}q0Mf^Rt{$L)eZE9J>U-`*<&HF2j(6XqxysnN#&Bb*)(RFn!>_r_;QXO<G>}4HvEP5$D^Fj03f)P>q`#xpNx$bl=iyru9#QkRfZ4;t$kC#fC4Q^=_l{@df&wRh`f~Z{kCNv8x_0zJ54gR{vT-)x>s9a+2Id}Ded0G}dAg>#Z<#nU6tV1-Gb<nYht-z>h{?xB^R32FCYxlv!pL%pGYPEc6IrD~!?Yz<Wv8?^>EnQD|qVcvqzqqel(8C*z)5kpG-nt63Y_Ch<VfT8gZ&aSS;C6T2Ud6R6Y9+55jpcQtv8+QhmUYmvh^^GYFHCo-KHhkF{<xE#kta@=$Ch`9n|F09?-e}rs@8FH{knB*7BR%j($C-TjES3N{43`Si<^@gac|o}XYBan<<+m$v{}^cLRrKRFUuH2?(y>UO<#Kii<-yFqQ@R9`0IjMe0Bhs8#jyfYJ7B=`Pl7+akJ<X!B)=bxLNe4U=c&SEdAtuaeLe><KMV_LEJ3X`l6l>+wsTCqQ?Y_x?L!X7~*9agUCHz7X2w$)I44mJvL(a+6!iPse|^v4H_?t^?H`xQ^xnP;%3n&g3A=oikn4$3KlWM%hJ!{Wkcd-8UGb+`p3;;t?#AxO%Z>*EP70^sN03Ih#_8<F^JsbWznC4Ma|=7(PKTf)xIFEI3G-9AIuReds#7g>l<g>%D!1l7IT$-Ek~^EmBnOnEoC1pCd=Fddq*)@=HirPtpfW_j#$|TbHvKNR!o+;%Q$24{@*H^%HDfSURb5NsqCxAWHDFSw|B(KzPck;_UdD@h)vmtkI6E3wN|lM*-MYfvQ~k8@0cuecgivsrz~qF<BY|0FEW*VR4presu8(ruQP6CpD-d<A(s27Iu`bFA63V~UfH*d$RajnA63iBo@zus*sZ!L_fd6xfLLBv$HHFOXV$XZN7b>2P1#4)va+Wdk+;=7?w0$gI;PM2Ze`C<%gP>RM1G!F*|&_yA~t0oRm;krYDA{b@}{!Kt7Umz9hV@M`=~k=_R2nUL@uD%lzr5QTu3bUQFSb8CHGNvEY?o$6Y5ylEBlraS=h^cR2_@>m3`EREaI2@s5%z4QucKtvZ%S-N7b>gm;0zX7WT?Mb3_)sr0k<=S=m#K$l|)nKB1PCJwq)k`<7Z(_AMi_h)vl?)v~gu8j;28TG`jtva-jkWo4gP%gR1;L>93r`>0x0_EaOXsFku$sAXl(P|M1`rIwX_%ZO~R%lUm&Eh~Gf5n0qq+1J&wvd61sWuIBg%06>M7O^RNr*ScT)-&aPX}nCI^-Q^68ZXmlJ-6I1jhCgLz<yv{EaMOCL&n9sx|KKOerdcsf80s8+%LUQ4(#{F#WIG#K66}Lziu5<?w7{PqQ{i|(zsdKJB^FQdddCLcv<v`+%JunMSsfu(s)_=3G4^P#WMcDK4e@h)>`hD#>=9|<bLUea$vtVE|xI__L<{i(Vud^G+q`xrtFu-&C1?sTrAd0?w7{PqEF<0X}m1@Q|_0>%hFF^KQJzq@dx%H<6^Paa=$cQ7Ck2SOD~iI`@M0oj3Kbk92blJl>4Revgk2o?=&v1(R`5isym)CSFK#>cEBDTPyH;<dyjX6ZSR0RI{t9#DEn_*3wsCb(eX6$nN{{t+ui|tbS!ebt@Y|)9b&LY$KKh!g4cDx9v$a?)h$>D2kg<YhkVL)aljrOQ;w$6C$ZS0W6IH#*LA=i9aD~`QioXV(J|#{%5`zT9vzDul|G5Z9v#zbBzRp1?9nm3Moi^(6pKANrq@VtT^z7S$J=V(;-PzyHL}9|?a_F8rDjq2_^_3>eeL9RFGXWvAB}hJdBnC~v}@9iXe{ibvAk~aKlVmtVIPfyby)gCRJQ97h0AZwwe3ri&uA>{qw(Ocy4m(iDaU9m?4xnHz;zo?&7-lfkH(avTj>)mD?JmDDMz>LlV~jaM8}k)TlPsbmVKh*a)IlL9*D-WPjnotgTEiNtn^Gork-@mK8eP%PjpPL5x4A<Xe|3g$MU)j{I6dv%RbSuc#Zt|gv+{<d`4ln;Jc%<r}cv=R<XcqR>N+=C8M)v2E{fa@cPxTTkz=U?Adxp<6sOLb_*^UojrfdZWOGEhTVeij?VUVYX)krVf(rbqqALyZh`y1hV44cjn4ME$QU$iuS>%ytou7-;_qpShxq%NPX10^xV`)vRl4zb|4v=Nj}`7m_jk#{?d9`2Kk@#ZIwh}=zd;v1exZM-PUlDWcgB>w9Q~cTaC_-rH~ydgcj}bClke#7)P>tCe|ItBc)Wk7PS#lYySTm>{SacWtXIVGc>hkFd`*P^o!;>A3;jEFIzRT>4D9J!R#49J09e_L|1dk2&JygC9I&y-#uvjz`ccM1dsXoh%|`X(B^zH1KRO#VFWV;6zDQm=n<9R~YaYo@1e+ptj^QVw&5j@Tn}be`vR?b=ACs@V);d!DIWMtSa=^w*Hoh1((vLD8T0_N8G#k~Ak8I2sesnf!UbaoBeUZF$HbwkIs9_O5PU;-PPehxcsne_lb4Q!2$)@5J9nFPr_wf;XB?oMLWaEutBmF4jp*2+eM6*%-c*(|!;YVkq=4IQ2+84=7XH&#agc=s{<D||p{6w_5YsDn%=jnHO*VAjT?KRWQ;m`E4h<%a+Ha@a3W7rh&6X9A#{KSaIOE$h3esnfP`~+eS*hlsg!AAN~#zT8U@e|EP^&@kS<|m>}v$J2C&CU+<?V&X--l?rsywhtYu~%}y#!EI<44Wc;!fP1GPXrs)kB@A;G5qLkiueh{9I%h<CxVUiql_1+q4X2YM)f0ekLIU{&FLzwOg65g?;QR7rm%0($QssQVque8aL#*gK}X+nPd{%e>{aJJKJ<RGPxV&b#~b8Z>f9AKcC?OM+RFUvor+eUi8HLxHCuVZudB`__7a<d)$5WUANlbLKe~8S8-;yzT_0W747;vRxvo#Su219Br<<$E*Qe&I=1Bfc@^1z53f71Gd&$2Qs7bI6x^cR$kFIM4t{cofEMGY{BuCBMkXorZDlvQ29CiNH95r(-U9EI;)jFuxRdZ3-=rH-dk8=ByuH~ekRr`4RSvNP)&xwBiAL{4C{W;Ok|MC6&pYrd3DE~gGqy5!zd*$D?jOgb=_E(jCt&sgyb^Kr1UybA^+WxAtf8}U@Rkc_5S0jzbyT2;`&8xsZwx!f3Wc)(+S9N}(?6+IWzIx34)o^>|{})6YzmWY^W&hmK{;F!P?yp7~zmWY^WnVpHe^nj-SN2yU`AO`rCiYho`>Tol)x`d4Vt+NUzna)zP3*5GKEEeEzbE#i68)U$=R`jz`uV?Me^u_0{CV;fv)TMH_BgRuvbtyDz{XO?N!xQG_=#m>spA3mhWl|~BjfQ!^W(rq*2kyh?$gvKnoWowQ3Fjpv23isxEall1DlX_SM7D{uCYn<PojS=uz%*te2ZM?e1FWf9M}ZwCdZXpnqhvT*#y^7j;m{;`iWr^9*<AwCx%UUeSE6DraqBuiuh4qi#k6MY<z0n!(Y>3^@(OvWZhMJ-MUAxN%T*me=fLxBH!b}_H82DguHh}zUPMe(b#DHoPQ6{`%!Gd{X}?AD&i-SjTM%Ag!jlI^@(H?DW0(R?1=G%+eE5Q*v}9V>l1FH^>coG^?nqapr5XFo0v~+SY_&T!^ykMltn4-E_5#by-2CWxcqlQHw5gS+)!BL{QKRtt!^|wT>n5?{yU+<f79Q3S?g(@JQrHd7jX(L&s8nr?0wx=rcR4^gck8!cU@;I{9NcJzolFLydbFMxQIjO#uT65pZ{EFF<-<X&UM<KXDj<$+N-+%k58B)Z=DwZPN-am4I2H-;httcvKQ+jwHz053jIOJ#@17T`l{z54sov2fpxOa*9YuX-IuN>>Y~#kjt@$fw(}Hqm0FIA{G?qZE#iHj>_oisTxfYN;^-Aai|a`3&j*6%Vr>R4VIq!a#dx5n?VOeI;C*;R#w2TFyE?RX*V%Sbzdibdsf>fv!oJ70>#YqN8rgPI3wvc8q!#f!Rxr!@`=5X8I!P_!QN}^)m3vCr{?~8VVB1N({D~%RWgMgy_9D*5H#D;Cq!#wdI7l6DeTHl5vrki>;hOsF`yZ;$DouS>XzH^{Q=b)y`uvOak#z~y$yCNc)+te+M19oyywa?N{d2~tM@!qac%<2O`#fd)NdLb#-mHbKam^j(nrHgN)Ww@`cSq8~hpGop?CwbKJf7@Gx88o-bfQJRy>pw#)S@=37WIgvMSYxTQC}xo)Zd8~^*&p^gq@erqRv8#dI&A*C$wBwxz368{qI`e#OwFJdwmn19}}M+6Q3UwpC1#S9}}M+6Q7R~^+|kwO#J+r_<WIA-^BVR*4N4Uo`3(c|BLYRPw4NDelY$<tI6U@#DfENe!c#S1Ew+#Qj7N-aSi_ig1Y^&KTKsDq!#|gLwru~+b0G6E8}op``_>Uw(7(Geit|gsYQ%_KRW~Oi+(+1{9|rq9HjQwpq1@U`nC1Jx-FG)kXrcn*8u|d5cIE%!+D*kf1>{X`}H3jXZ_2?S^vR_`v05OKfLZC>!JMayIhaZx`(Ytu<qyABed>e>k+K``Sl2`d)Rse>wbPc!s{Ng9&ldE^$4wd*m?x(ettbd>mIfq!MdMckI=e@tw*r#ay_!46_kN&dKl0X20%NK?H~)TgZfaOWO;ByX{ZX#Nj8VeAPE}6K#~KY6EG+aC7~=-fJ$&F)P!Vc0F9stq(VBhpv$y@tKnMc0^OiD^o8r825=}vvJ}*Y5^xDrCRrISf{JiCG$Yvzsz76?3$;krf~L?OszDu+b)YlUgI+L*<RG{L`ayT-O0p~50BO(>dXVe^nb3#QZcDN)^oOh9O2{CY0oPErDUd@l2Z}*UC<hmlyck+Tb?5*tk}g0P0(mf+<Y*WHBjH9EPjWnrgRxKmQ%FvMi7){s!%UJhVH)JaC>Tn|JeWbpBsw2TIv=LPESOJnKFozVa1#t8ISg`PHVlU0bc}&QI;PV3aMH730o(?QNiK#v;7(Wq_mI2??uMnX9PTH1KdgZJU=^$;xf&jXWv~ctrQ>mUn2wcnek<u^@DMx#>qxGH$6yVtg@q&+!Y%M9+zhwVaTnZ6#{+bJJLyMZ13V2|NN#~m@C-Z)FOqx_o`<cl4SXbhumfHKFYG3{8(xMNU^6^P$D8m99UeM=lJpC(3tol2B=^D_@H*^)r${~pPrz%i9yZeP9Bij!C!KF3{Tl3pci;fY1Moh400-d+$s_Oyd<=)-bCRFKXK)n0fa4^O!&h(!K7{>r`~ct3ag5IQlRgAr!?$pf<VpA*zJnj(U6Sv@+i(Kjg7@h72tK9bOFDm#^a=P0euY0s{sF(i?{E$ff2YUa@D~6U$G@OBax}06mLXXNFT#J|Ec`-8c`QvwF*^SRN|P*w7h^>%MUQfL30A<<a0xwrhO&4H&d~8EFl1N~%i<ZLvRDbLV{NQ~Rj@f$#X49Qt6@ECjFqt=HpN=#!fWv|ycAQhJ|<%eY=RBY!e)2{w#J&+9@8-iGcg-4$1AZFHbOUEgDH3wcEB`jiybiwGq5w7n1fyMYHW#JupPF+PS_o<!~WO@d*F@O69?f9*b4{a2<(Q#a1{2#vA6&SU~e3Uxp+NJ#*sJ#XW(ee!&%rDZ^i-~h=n*2hvF2RiNkRk&ciV{2XDcAya{i`2{;~a!|6B)@4&e@6>rD+I2#w@owyY5#bvk{*WnUeiTC4O_yDfKMYtLt$9wPz+=chy-M9fC#8tQjAH#?61zd}d;ET8%cj8mH0yp9__%J?;+wf7`iXL2#FX7AhBzo}`+=Nf#tN1)_#@BHNK8LTN54YoP1XhxLK=K283u~~t>=IUk9{*r1_5*%Q@?$K<-p9}IH+-KS-{5gPh4t8RdQ@V2@NIkt58x+w7(d4^@dW;eKjW|X2mXnS6=$Vb8CHQ+Vbxe|mc$ycFK{ouhhNa+Yut|q@d(Ky_%0s8lX!;Y8T=G~!SC=Zl3(FzEXR)Gw<N#C%Itfr$?B7=&wj!>tU9a8>d@nIb`C4DOG#eJ{>IB#309U}Mvr7xnsN3QmZrzW><#=KktDKxXt0m)Ly{ljMeG=sXJ_#kp2at@5o^j)StEKhXDKX=<&ex_nJj~4GmE6fTCyvd$*v}OHEYeXn2R;0qXWB&4mX`QCY{CFuxnUHk{wxl){b4vnviV5u3&9hL)MIrbk>57R&?HsbX(Sib!WXv_GUd<FV=?*A~}flXZ_efHk9O0HkjSOhOm(&N3uLNfL+JB(lM5epd**gyOJKjhO<#DpJYB8!)|2bST~a0SZ6kxbz(i}=*zCBV;G(HAU&EDvPo<@$?0qgo62Uec_int*=!b@%WfrkE4!J^XA9V!B=2Omu{mrSn?T1>b_X4|(D?+?bJ*={5nD!b8M})uVRy5MBqy@*Y%wcflj)erZlYr$olhpcnBBuxu!l%K#O`Mgu!q^>Bp+vwvPalsYy-&+Y#m$Ao@CFEe1<*E*02ZJeROPPo9K9g&hI0=hHYe<*$X6JV9&8<+4F2A$(8J0wuLQctLRwG*3$75ov$Ljg}umjuw5i~F(2E>USV&Ne3QM#US)5vw@JRu_OiFwe)a*$57@ixb@noQiH?ui`*iH1^Os1!&fa4mvO^>fv5(k6_6hTl^sw#h0NcjAbnIq(=y-?Dy`&GY!|WLQntj1OWxuh{*thIEc9eb3eql%0DR!ED#m=${{2TT;`-A<!PB6xQWk0eK{0#evUBtg+<@lfMIQyFcKgl>R$$w_W_{IEpR+^XR=U7=@k^jT~VwHJuj=U-_!wp`AU&2fAO1v7c#gqAE{8FCAYw-H~a$b`+<jr|?-h{h&9iG9v@VdM<&*WF|2HfN+yb-^Or}C!!8lJ>E@oZj?x8N;#V{Y-Qc{ARcci`!~9q-Ju__e$%zmn(h?z|0m^PaptZ^e7?j=U}J#(VL8{CYls_vZP$56|U8d0#$^-^j1yBl%c9h>z#D^BZ`7UdZ$K5I&uc;lueHK8}y#^Y}o%kWb`;`D8wokKi--Tt1r5;<xYuKA+#lC-4RQ4nBoX;*0ofK8-KoH}jc%F~61H#P8&H^LzLzlB@WAd<DOsuO_*gKgb{AkMMOQ*YU^r8ori4P4a2Jfj_~Y;#){=;hXp~{8|1Y$rt(a{9(S5FQdc5U!Y?%f0B;JY4l+l6C+O&ZROjzkED<9;4g76Urus4U&^=hyZF6yJis5NV?EzU$8$8goyNq-MxtH(RlbMh9{xIigYV_<kbH;l<8SkK`9YEg`3L-cet;h#d4zw$Kjw$|=OjPppYfyo3;r$1Z~51JKYx?ILdOsM8#<2hLv(ydqx)%0j2t5RiXZ1ENuK22^Y8eNd^gG6{AGTE@8qx1@fLrNj*s}KbbLvpCumHJd`k2)Kh6Ij`3L`v|IW{GFn*`UU;J-+yDwq<%}W@D!Hwd^#Uw8_N*Na!WsC|WD;Sp;<&26(b&}PMD#kzjEdPa$T1Hhm${VHWC`P0I(3lu0O<dWiW?W`erbkVqhEd!2mDixhPyABj6hA}9pPU)YC~1_Xqmpqc9cS#3vP8*7eWMY{M#kkvL!+^gLNdi@YBV!kMi$8|Bi%?dG7UFLx6#7LF<KgJNVYL7qm^-$(Sc+Kqpi{0xWcGQM`xoQ9j%Qk>Bykb<}@Zot|Yp~Xm4~S+12P|bTqmc^+?t;>KNA=Nk#)Yni#2cWE&<OSJUXVG$uw&qV7g7qd&?1MjxZM(a*Sn<PF9^V~{b}$Rn9&3^9fp!;LW{#~7oGk;aWiA<04`-xz0%H>Q%DYD_Y6jRD4Wbj&fP(J{doOUDQr&80ChGL~qfF~yiga+WdOm|@H|dXnsEbTeieJ&e9|TyG4cW3*8~$7C9vNn>K9faw1LP6RGg', 'wilderness-fixed-lattice-boards-and-twin-strap-plant-press-01': 'c-rlq378bc*~i~1<4r{Iz}s<A6tfF+AHWWBD54-BC@3HdyTdZFyR*#9f{1t|8WWAtgm^`x@r;S_ipC2Vj7Kz@sHpLZ#uLR`qtV2~eBZx&rk1y7r>bXn$@6?XU;8}s=f`wab-i!@ySl4-q+432A1;aLwSN#@aR||o(<UFiye^f`rwet%m)EtV+tayJA)BikUU$^OT(&)%_qCvkZ%k{ty*ZupO&B)Ww<J6?G&CHmtFK#<&gC=Nb`%Z{_1CSaugf=~fx6-TGUe-r&stvBo@&E)b<^x^^>yvpW_v>*IA_J2jelKUmp-|WOXaO@G-ca5vhC^i!rWZ8)v7zWJ?*o;Y)u!^zRvcxRBlna*;iPYY4<J2w6>yS`Gx6pVT7+e>+5JuwHJK(j&xI|E!|%4Tbj!hGVLw(zErMhVP;9H)tB$g6jJjut(n3yUpD7k(AnNpKp5E4l+EQjTT<5Fe3`tjsWpW*nytv%()opUVC86LEJV-7U{{N#<kI>4;dU=3rk161Rw6cwU;;G+6WCmW3DyuyaB~SJR6{VK%_W#{4Z(yrmtZ0_1QT%!W~>SX{cl=?eYT^2o!QPjx|-@hH?y7X&A$2B!a_(Y*PQpI@b^?}t8c!wKVPf0m;4AHYAy54@62V8iUpaIp;l9=rb52n%0nUDZjH`Xg!4O_7PY2**$!)Tw?^!)fTGTT#&-2(OfH*ho`L>MLmVCc%_*i>Z86n2wsi&4)SAtsKiFY=LrX3L`(@hZ!+CZ*zNHz2wxAOMp+hiD0b8sPn{wHF-j^@rG93snmxjqo6;dcy=!AFb%PGjT<KkORgs&}yG^Bm`bh;gXwx?5tg&PBmI|H1UU7F5KMz<!W3WZEl+BW1EYbUitxYTL_UFgI~Q_ksv99l0$go`$6qt6JqC2dDkSeo_WfOOiYOSwT5Zg0*mMTDK!eM0LpoNzcunU;)oR^_d9BlfmbrakXllF4W0x2Emmxip(wWEEYI%Hz;lWS?>yLrpkCJto~$NVT_gwx)8^vCA3uUdPzI_HX{d2K+TgyZM?oP;uXJY)6O5y%@4vn{#R0WX|%}2kL|Mq55!rq&`|7tB=<w>XEWQ0Jo7FGhyG%&doHV{iUdy&fz{Z-(Zg=4XveJG?a#*287s9Kw=y0W7c3_I2t;v{WtgnxK&+%JK)0H=1eYaUmwt7!}0h!U%-IVG#7^!wwRl3Z(UY5ypZcm*VmOyFt<5X=xjr2>&vp`7Gl#W)<|Y$5Vpye%$6QuJIqdft92TehRgX@^7E*Ntan}ZO1t%SWOKN9p-H===uXbQHJ@u8>>R9${VtzfmugOR6f#TFv+IV#Z>@PaaCXTgdHZTu_4{mYu6;Z1+_<a>{g~UFZqH`&&i2ynh}QmUcHP+H$4)$K+Uz>(`+UmkvfWG|7`MJDEQEQQ?Qg>D?{nL*yHfqbC(Jx-T&en!OnT{D+e&<|v+Ui@Sz$S;>>qgCw$PMvN|b}F<7nHc&YEGgrC{d_D%-P+=4>ZQPRlgovR*!F<<{(rdFeV{vR{2&$Nb!+G>%zors<e$XUjs%N|wjwr}DV0v}SXMBjMI;X_kLzH0Zbg3&*1IP%IFw_YaLk>~8{rM9`lICh$$zpRoUnhJ&G4Fc7M@yxUgZg=!3=Ku+zg>${<euw64A_s0_cSYU;9a_EDx^D?QkkZzvb3L97#y&lFBh*WgdKeQa7KbVO7gP~wBjPC-$Qn5%d6o>}n;b0F!ipQLFYl*3RjAx{BZ8Ngjo*tyIGl_mHf?&MVi$F9I3563eE7Cye$oV6Qs6QMHhvPkoDq1?~;gCNP2!vxUQH{g7UmDZxD0&!BFjm@`KNgI~Ls5TJ6Hu^xG!acG7>UNi)dQ-MplTsj7<+|%nqhQz&iGApWJHMzO~x9cN_B8pbD8-ttR3o<$<roGpD_7oJI6;)K4#MBiMVp$%*Q1VM?Y^*_|%DwLM!H2Nv>f!Tl0QH8}}RT^L~T1?>Dk>ztKMLH&pw6V;lDy@AH1cweL5<j<3JZJC4-8W9vSoYtO-+>{&las(t6oUIB-{0ujFVK<#_)fwysS+PL>vkM?euYt+8`INN=~k$FGgeX#rPjradGcOb|Peb9O6L%ai_9(AAx2LM;jjU9;er~`)E<=S`8j(;#_J^&cmQ%%^G&*n;v&hK2XAe}o7_h|Ou+%@r-zN`bCj0CL4n{bO;D23UUI=OVADqm7Vkytbsi^p(H!sRhux>BN2$nTF^7vAy(C=w6GqOov1W?fk_*4=+Y^)^EO(p^a$Hxal}2kRTEH&U>>S9jcDV@oS%JdA*Q7^dpMYSlws)kD#)>eI%Ko;doLZViNblE!f9(i_2rJ?M{F*Lz&2?L7JuxZvYvDq`m`WTzk$$5lEIO@y6!tkOuNoXD_05()$&xI<{D-i#>~;l5=u(l<XP0`?7MG?obAz6b++FZ>iMr6Giy_((M7kMzb*(Y|FN);BxgK$YwOU%(8JSg-7m@CQmU2Li!xAQ9+|8{&P-L!wV^2!u**h~RD*hcq1Sg&P8ak{j^Xgmohw@73ty?^_xIfj;`7Jj_Nh#e%PUH97=BB|F5Ufmk4B&HQ>{hd{88iEtSwF-t2a!s=XkVv3MMnDoSgRuu7)r*W|fqo&{fE?Sy|#$q9ifT0M_L?9Hkx1n$pbKod0P<Gtis~Ec-cJH>ae#CrzNw{8L0?}F%S2gCI<*jP!dy}?UAJgVC`oyAscHV@_i#ISg=EwGG2W~A&bLMa&gqd~3j=Ew|#BttKYr`KcubD(JyoCMH(uvc(6=Nic8X_^?p!m%W3M3+~9tygQLV=*4pMCyPh;fXMxI+uuV@RTOgAs^E;|b&{Qo7tamy{f*U*-5>ThVc83)$D~KzSW0Xk|SS4a8j%8VuGDi?M-_%PpVZ@0!nW&H2=1qDSe}9Fk3v%}8If8SUel8i-Y_ZuR0!#l^prV$39Pl?(RbJPpQrdY+=ejScYWl|8kZzpRj+m~L+=Sif(G$4g&KUa-Lav5wVLD%WCRD4d7}H+IIouKh)=wK04<D&y|RSvk~`T}Q+5K6E@0iuR#)AZXuV^tyV)x`F9^^|-%J$IKt^OXgtUzN9V~jrJvVLCi|~P(2h3_aJq)K^@g2!FV64hwWAHTB~DNuBaZ3`)fa8y6-(63-+P&k#J8=xP(1cJI+^sPtKX{^>NaKd(c2A5vWLCFdVG3o+*FWo4<0f3-rYLRT{uGum=r9{T1~?xbjB(5<w^sjr1u3+=eHjeL0Gua3s{H2Ew5#A#`2+%2z(_<6tZnT`_0H!A}s4nQ%0Haq#Tof6`x$eEpPNk_JxJz^Z)Fz{wi8*jPWkQMIYzWDTs!7Y&?rW9s_vj8Wx3*E;{?|8*-fs!Ex)HMFy~hIU3(->0#RsXwD?=ufwH1Z_>*LARrC&^KvE+6}rJ?Tjs3P=9ED>PK7A0NNG0D{V`XcA#CLyU;eYC2dawp#y0rT30u#c-EDZ8dn!~P8v8_1FP~y11D?X;_KV5>}pfP$r@OdFB&-M#-0z&KD5s3Eg!z1>)h9HvIbV=iv~{Cz{P9D>aI35oUDOW`J#c7ZtVHT>>ulVeB{1+y3Sb*Cu?9;zG&cN4P0FC<y&2CYB*T~tMWwyC*9cdkNfy@?rpDkowFKF*1)QK(ZI<XxcHMVwo0ltHJq%0Rr#WUlWy$!$9?=6JZ;OQI%hSUtbtYeqJfh&aB<1vy}H`eaIywg<%<SRy0PaUvw!ZJ(9h0MV4M164O}#F<iz308ab)s^IG3oqxM?^7fr18TLUL`Z1pWWV2hDs<{elI7frlFLoit*Cv|M~P3^Y^E}B^Fw+2q?xQFLgPtKj5oEMwwTprbvbLYQsp7tiLO_k@~#?_}h3(Ws_gzkv>{~mN89Sl8~_Qp(qPud5%59awhV4gn&I)nz(7WS&Z7Wnk1z33o11bPVVi&FcL59*_BP<j`tht{KpwaTy?)LL8EkG@4ip+l(-rF=99I*7JM>47v1It(?oMW6aX`_ZnnKQ+(+&;w|9lp2H{ZI6#c=^fCMf%ps~oC}R?Tyo>0iP^a1#z`GxtVptP+l`ARX5+RSCv|M~jg3ogTr@Eom)tn1W2<j$+;-!liP^aA#z`G}<EJ-%_9f5zoxP}d!{rZ+*zWm3NfY1o+1Dd$;l+*Hbz`fYN<RDjsa@??vTC!EE9+KcwO<{pzRg?zRAVJu?NqXA-;Gr}I#&CdnYgnXTkTY`YTu1jJ33bT8Z&SGh)TBFsbtl@8>@D7%=WdalFRKln6+<Y)sBu?Zr4<DId2YT`82X>N5{-d-MH)%2Q&W|S+%2McCHmGxqMzYn4K?1R_*ARo%=>EpVwMu=Xf{fWfWWY4Qi~YWHnY)W9!^Eu^L0%*gBU@tj>2gw$4oxt8?6qt#i%9>U^w$SD9FygKlh{3no_QiyK?sHnBQK+}QG}iItz-Sb2|g6;Br5yne4PPgb(>WF;$)nOJ$%#L9;zRz5Vb@|cO0S52&ZXkz6<6DyCISb5dN%7-RaJ~XlNn2D8FO{{!qV&y|OR^H=W#gj!V2Ia|0R-UZJmd8x2yz0i5$4snz=*E`EOsu@>#+JuStbAAluQIXnsvBE>nppYJjV+IvSb5crEsvR4`OuA(_c&MaWN~$2WtS%_S$VROmB&o1ylP_QLlY|>npk<v#LBBCRz5Vb@}Y^9$4soeYGUO>6DuE@Sb5CE%Bv<;J~XlNp&KjjajxP?YdwCo@?<3|PgY~gV<uK!bz{q8CRRRlW6NVER$g^u%VQ>1KCFRPnOJ$%jV+IvSozS6EsvR4dDV?AkC|Bc(2bS%I9Ktc{k({I(!tD=4rU(HGV`jInGdzhe5hsSF)cH%YMJ>^%gl#bW**Zr^QxAa54FsEsAc9cEi<obnfXx5%!fu+-s4=wlh#<;$gb%QX4mv?T)swYnO*CRT)swYnO(<?T)swYnO*CRT)swYnO(=-c$JCSwcg0(YqXZxb==71YqXZxwcg0(YqXZxb==6xdz`Cy(z+LIWOE`1vpJE2*&Ij9Y_6nbHV@J=n+Iu`&2hBM=1N*-^B^s=d61Ub97oG+uB2r)57IK52WgqjakR|lN?K;~AT6_bkdc-5I9KtcHJ4AaH6;hLHKlG`UL(>nTWd0Md5uWRY#qtS<uxKLv$ZB8m)D52%+`_Ic$JCST9c8>YeZUR>qtf}uMugPtu-0ByhfyDwvJ?E<vq?-JZY_kCfS<2gV~zAgV`Fpmf2dpmf1SImf1SImf0G+mf2dpmf1SImf1SImf0G+mf2dpmf1SImf1SImf0G+mf2dpmf1SImf1SIk(Kv2SMj9vEGfyJH9MF+YwpJ7=g3-S&!CN5elDzK_Uzcm<>$OwX3vO?Tz+n=W%g{>jaQkNJ;OC}`MIi=*|S$8m!FernLT4Qa{0NZmf5pWBP;K5uHs4S*=Ume?!w6B-!nLv{m!8qtGYU7zkhHr`wfGG+3yw{%zk^|VD@_h2eaP{IGFuTz`^WUzk}KHeFw8=^bTgv<sHnPtvi@KPj@hTChp)W$Fv)>XXRD7m%l&P{C-LMeGh)quG`n9{7u)U=x1+!Pt~jadhvSk{vVCE$Nzsv4}P!c7DKPcjlTAC6O5Bye>VUA{MY=sseY@xsm^P!Kbu#7yz$fPk2ijL<Ac{9Z~XMeD{uVt#!s(5-uUT_S6+X-@zd*%H-38KgV!H#{Pe~vZ~XMePp?0l&G_l&M>qf0avt@xO|Sfadz_TCC2bAe+WwcnwxfPz{rg{Akf3d-KeRt>Z~qJB1E2$FE0o&W{`bgtrGd1g{cn`*h|kU_y&LTT-2*kOf1zw|=-&3fEVe7{2i=eMM+xiS9NP__J+NhO8Vnsw`(n#}Gz2<?zC{PnPzpc;bP!4(LJiOc)Yum#{ZKz0j8a1=1PxIHCBhVg#!%{DY#k0APC;x5Q6sdGMp2x`&|%QSXaq_pX*6^+Y6MYo9CRFwM5#s^4;@bvP~r$W3VIYujl|ZYp-0o<*fO4`LZ{L+nn=gd@zCRGGD;sq$3l-qjl)rLCUhoEL8+-U8#<fj(i}R0=0WGte3U+snxIXnF$E=4&=k!=_M2$|bODZl^>4l{gf65-I0F5t71~N^9EldnKr_hk?$l0;p^IrRs-pv`04>l`WOopq3_Y2$$a0Q4p`FNIJ)J@;petw?MJYjNK+mA>AagM~3wjnUM+Q%$Gofc9H;2-9>HE;{(^xu^CeaU|KcEYcm80lF=!J9+vU4t-4?Q1oPp2Q#MbL|A2BMrtmqIV4pCZa8x*U2rtwgjJ(`C@h5OFhIL03YrM8s)CcQy2C`WYg;imroRhbY_VB+5hc)IrzKjdT<ACb}M_v-At-FHj?clD~rf3bAGp_07<mu_cFZZiC*2=$FwFIvsjCol3XRopd+!Zn_<%m(v~4J5Zw&CGUdXg&ZtLHtvPqi!G<&o7K?O$jaIDZ8{Hn9(|AQqx<PW=!3KdrO%<Y(6y*>CQ3d4eE_*R2U&U;`Y^Vfi*Fu<K8kGph<-?yKrf-6(C_Jw^d$62`U6U@q{pF;qsI9t`2_R{<m{)&<Wtb6=xLO=oSuO`gHjh`>pJK<Wb_JpmY#z?hm8K5uB8{CFVJ6*(W~iY=*#qHWcGP_5&9x>b_4yDUWdL;zocK&t@IZ3EqVu;yO}mXH_)rd;2X3ax*oat4ZTMnLO-P6(mk|_K7oEhpCLo{(&y06>3wACBl;BjDRNMxFX*4pf70*hA$o-V4gEL$4>IvEk-(57zC=d8qOYM}Bi6@AiY>)sw59kHqI`<B5l`c@op>CPZV%mFY$2YYt;Dv_ZN)l7+fVEuo~0ecbBOF^+DZHwpKprislV6-x{G*`UZI!hP3W8S8VwM;i@n4Ee0CKtBesFifnq0=+C}UM-BY}QZ#U3B;#GVG;%|EjAJiw-)4TLGeGL7WKA?TY0pcLBFFyN=4TyOVbdcBwrF>#Abg=jc-+oR*#QXRR!rumqdT71)l>SbCqklpFMgO2fgkOZjA^0?i&*@7V1|24bpj5pGLWANfd`lvNJVnGX{4FTr(75=Tg!m6_Eri%wd_zRVNHGdJN+bj!M<bvkQ0r@yOhS`lD`asSaVYdqF$N{J7h|DgQEDrc7!4hbto9S*#Np7xk<}f=&f*B@5#lIhbSE(pI#C=Z`it>m0(1g0yqh>$OodJrdx*WoequUwx|o5??IUJFXNt+l>oMY3=&{IToj5_vfzA;Jii5?s#60Lc(S!^Q5zWwMF$?)SQKX<LWNfHdATrR52#BzViB@Q<$RZOF(E;rcEy&YJq7B-H%nTPf(FyGojfnD4aWeE|aSEawE0#l-i#(!TB9=jyA>wi3RB;;gG(>zDqB|3MrdWXpPZwuF&q9=w#F1hebefnVzAe5d&V!yO&PM6U;vDEXs4)R0&xM|gSSKUu^P%Ts%Q5)oLg<Bv{&;bmm<ydNW{V$+pNLDKmxv#s^enLwx)L>xMahey7b6F=kd4crmto6^_~r`e7060j%omHGi^M|lQ}J_gE%aLPGn8%-S3$2rjTA~=1HA^hX+f5*hhC2@C*hkLp*JF1i$%Lw3SBA+;s)_+aVzvz@k^A>i<_V~p+*}@-U7V^IXeZJybXGr_zg-d7k5DKK&d6zdOP%XWb{;Vr??Ax7czQ=_>Q;-dXHFzjGif0LsyI6BC~gkd!hFtXWtb?@jK}6#P`Jy#0BCZ=tJTWWbS<NDD+XW78!g%JPdspx%shpO#BJ@CvlOuR9r5ef<7glL5409&qALSk0Vo0h;`6)$ibE3Iq@R&MRB#bPW(c=41HO=icDNDUW2|So<~Mr60bmCL9D+LZ;18K_2Onkd7Ib(-5}mWly`{tq3??~5$)UJUFf@r_)hVG_z3zDBK|F+`xN@A_z)3(EIx;RjwsiN`^1CL2gUv3Z{i=~U(kPvzoYb8@g?+2)VLQVzk+^+Sl1%zuc2RK%LDj^<OBFTEdC&VFP?-xDgG$_BfcTGmj4l3OCcXc%v(UWkY6K5B)3A@t>hE<_F1v5d>o%G@VBjGKWIO>PW)LsE&c-ii+Dk7CwG)P%kA*_rhFE;=nw5Lw?(ObasYIId<oyaCU%w2<I^918z6Uw?k-;uuZzEmccAZxx5RF8Z@Hh`4WB*aYsk@F(7oiYD7CxX7rL)}8(G{SeDXbf>g1cq<RIuExfizVEBA-)FW*Hr50Hc92V$`NNPHqb69>yr@cEYf5IL%c*2@Fs$KoJ41Uf{1F1`>$Wk7x*0`i~Y-{OBnSpFNInEVpii$mjbnEXlvWds_LB&8fK8=;MIOSz5QULFcPRE|Z4ww2?c<KzhBFDXYuM<Zi9$iw9X=mfcw+(izQ6QL93WMpDjIR!dJjz^x3l#`&7keNN@G4fdGv2q_o>60^|Gvx`0a*&(_oh7FsAIHh#p~oZY1LSOZBJ@N=eW0wDDQHU0kq61SvKiWpNE_rKG6W4tznm`@%0<vcGL6#1WDB$fHHM(%NzjvI5Z}gS8?+5ug7~Hb+JOutWK@oVj*=r~yDZ41(4}%QN{^6vXdX2pD7gf>1UVRiY%GH=!<HnzITd;;vT~RlBaea}C6AD&$TQ@3px==zP<p&P9eO%yj7G_CL%)sOj7OHvhMtWrN8+3BLBEG=O_fK>8PFMWy8N#EfxG~Ef&4y7Pm||C&qIw#DEUL^50SGIkjV?77s?-_#4NcIx)P<1!`2@`e}s(AmOqgfLoY@~=gB5{DfCi#IWn4(S3s|j7a_Bk$jhLYA!iHZmGWxn)iNVnWmaAXy-xlDnQN0bLT{8;A%oY*>!H^pH#zw$c{B88*(pz!%jIp*+vFX{&@y=^^iFvbGIfi*9eO)*aGJbJ-V41~o+;0g=g8I2)p9K|akji4dcV9I8M#lcfv!QU=gJ4<!_bH2`H1pD`6%>J`52;HDIbSEE+0g+zn6c2{s9p`A)k^@L!Xv^M&y5#&p@9+^cNx0C!tTuKOx#@<vQp(MEo=PQ+X})TKRL-d|ti?eG#><K%CD(pF@qyQ1S)n3yAx9`4{;L^c9r43fXuG`VvZAgRL(^Uq)7bDQ}RsLT{D7M(J1O>(JLx<3{A-uh74u#`P%q8uT^f=2iKoTn}B3Qa2%EZ$RHbsavr1E$Caw+;8P?<SOVYc@IjzBj1I-iyC(#UvER-MvdE1aszY&^7oE>Uw#Pv5T))$R^NlZhf?=p>j%&eklo+OqI?AUh<pg8KbD_DKShoEk<*W$AECw?l>7wx33B|g{9Jws{Su`f!%_G<^zZU-DE+wn4Eh;r{2nF0fPR6aVZCeNgQ@Z4kl7bBn)rsx$JNC5?0a@Mw%V!WZydKnSNoN$+N|Wty46_iSI4Svr=K*k8(ZyEvTEOrRXaLX`?~VugSxTRP9>}M-B`7w<Bc({9$Cqy{yTYNTxM47=veJ*bz!BEtu{@p+N{RBjN*SxdvlHQQY9-dRb$H=CRQGEW9wL(Soy(?tz&0m<pDRgj)jTU@p5C8Th5g^xA>ghUhK-b8(Vp+WR>%3tm^7m<++koZYx>ks*+WnD_P~Ol2xuMxiTl!Smjg4n|8h3`~MLC3;Xr{KQ-?;qxT$bvwV*B|Mxjm7-~I%icpZ^&^Qf8=_rkWjwnBqN<b47LR2Fu2~C!t?;Hv}l*Zc6cg8`-Q6nN8MWdmk?dLnzGpF70DLvnr2%Sii?dLmFpi^i(dT%|M*&840`HuA*sve(V=tZ1nLTAzm=*0+{1)W9H&>QQyl^>r3ooGLeIuV~VdN!MypiSsqBYH9yYCW|YMa`6grqH9qXbc?%J&KM%P3t+-JbdP(^mtkTU4R;+QF0-4A^O!qi>M9ShEn6v+moOtq12Js+6rw&ucy+{Gy^(=rlWM07DE@KhV}HU9omi>lTfk)+JU}j?I&DWd=?|JnbZmGq#R1mqC7N@8pomJ66g{{iF<%XcE6-$cK>7K@_m$p*?m_dyN_*T_skAv_skBitXqxQy>wMpeJkIaIhftcHL`o@nwZ^JS7o)Y@;#n|**#$+yRWW^*}ZyI-Wa2OujpWQZ`sK1)oWsQ-(Ho~zRLHRT4wjCRav!Jjd>Y1M@zCfzJu8uzZ;k5?^<Sae<PRY<635Ob|aVP*IH(Cb0e4M%UWi0Y9p)Ma<0sIc}|^V>p4a)uah{Kt)FybRaeJsUB$s{ZN$NBJ;cFmO~b)#9mBzFEyBT-IjP2MjiM@h^D=K<=FQ8zd6_pa`@cCav)*-8ylT&+dPkm)XC}fmv3iFcXRDn`w%(bg+OK5QW+hkFt;TA<I#zvC@4Vw|wNuHeeK%I^=veJbz4MN<)lMa=_T5;uqhqx%_0BuaRy&of+IM5sj*i*BR#kGj9S5`ajjY<yG0W|mN-pQk!7QIfR_*ARd8r$hed1u|A0w-Fbj;4RVkMW)3kS3F#mK519kX-a$mR1|%j_KQ#=MMT>s@AQtf*u)R#ap4jyxT!F~p74JMwg_&UZIf@5s}!I>+5uy(3S@>U^w$SD9FygKn(ek*8yIzPPb^N1l$=IpW6Z9eFxdes*K!J<e4;X}`-%d9sp~Co5Tb%*4v8CRRQ)vGSpbmB&o1ylP_QLlY|>npk<v#LBBCRz5Vb@}Y^9$4soeYGUO>6DuFOvGN}0DxS38Wu`n?$;y+}SiK`p$I7d2tlp8QW936PR`1BuvGS@Lt9Rt-SoyF9US(qCRX0}e$kVa%p&P4r<mp&>)s59V@^q|x=*G%>oU3@!ewUf@WF;$4R<iP#iIrDPtbAx<<wFxIkC|9`)x^q&CRRQ)vGSOSl~+xyd}w0jLlY~HnOJ$%#L9;zRz7rN<vq?-JZZnnOnI`Bl_#sQdPkm)l~>(Zy(3S@%7<>O-jSzc<yALU@5s}!@?j0U%EZd6Zmiysr(@+qH&*Y+)3NfZ8>@HZ=~(&Djg|K}SMj9%E;Hsy2QyDPn0ZXg%&S^vKGZVvp_ZA)w9LG!W#&UIGaqW1c}&a9t6FA0)H3s-mYK)2%)F{)=0hzr9~xPCk8>4I+V3)B*K`N7YkD_U@5s|JyVe_7y(3S@>^g2_^^QCpvunMP)jRTZ%&y~ZyvoGvT5n|ajyxT+>$s8CJMwhQuJuM%@5s|JyN(-Kd5?1yPulM?V{;-0vpJE2*&Ij9Y_6nbHV@J=n+Iu`&2hBM=1N*-^B^s=d61Ub97oG+uB2r)57IK52WgqjakR|lN?K;~AT6_bkdc-5I9Ktc{Vp@MrsQC@rqqqqJMwhQ)|!m0-jSzcwvJ?E^^QCpv$ZB8t9Rt-n5`qZ@hTIuwI(C0cjW1qts@y(y(3S@Y^}-2>K%DHX6r~sR^H=W#gq2C%-EW|gV~zAgV`Fpmf2dpmf1SImf1SImf0G+mf2dpmf1SImf1SImf0G+mf2dpmf1SImf1SImf0G+mf2dpmf1SImf1SIk(Kv2SMj9%E;IJ5*}?2tb2nD+$kQ=<25n^ZjyxT+XU9fX@5s|Jdq!+z^^QCpvuC?*yvoGv8LpAlJMwhQp1m4by(3S@>=~<()jRTZ%$|)JS$U6h6;ImlR%5@rFtU1g9%uGDhi<Iu>X`lh!NKe|3=U?$TW~P@?SX^Y?+qNxely@;_B#OwvuFJdX3zH>%%0IZm_3(wFnhM{VD>!S!R(p1gR30VZp@yQS7q<_liu$qy?DKNz2C=rzmN6$<Nf>6UVk?G{&?f3*B@{E^u`CTKi>H1jaT0I>5ZRWf4uS28?U_nc;lznA8-8h#s{xI-uUT_SKj#Pjh|kBHk<L&d%xc1SHAD#<o^O<v^1~'}
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





GROUND=.08
TABLETOP=.854441123008728
placements=[('t','camping-table-01',(-.3,0,GROUND)),('b','camping-backpack-01',(1.1,.2,GROUND)),('p','wilderness-fixed-lattice-boards-and-twin-strap-plant-press-01',(.05,0,TABLETOP))]
def rigid_point(instance,p):return (-p[1],p[0],p[2])if instance=='p'else tuple(p)
def stored_point(p):return tuple(struct.unpack('<f',struct.pack('<f',float(x)))[0]for x in p)
for instance,asset_key,t in placements:
 for name,g in ORIGINAL[asset_key].items():G[instance+'__'+name]=dict(g,vertices=[stored_point(add(rigid_point(instance,p),t))for p in g['vertices']],source_asset_id=asset_key,instance_id=instance)
 PLACEMENT_RECORDS.append(dict(instance_id=instance,source_asset_id=asset_key,translation_m=t,rotation_z_degrees=90 if instance=='p'else 0,uniform_scale=1,source_meshes=len(ORIGINAL[asset_key]),source_triangles=sum(len(g['faces'])for g in ORIGINAL[asset_key].values()),coordinate_storage='IEEE754 float32 whole rigid transform, no shape deformation'))
mi=len(PALETTE);PALETTE.append(('SceneOnlyDryFieldGround',(.24,.27,.20,1),.98,0.))
m=Mesh();v=[(-1.45,-1.05,0),(1.55,-1.05,0),(1.55,1.05,0),(-1.45,1.05,0),(-1.45,-1.05,GROUND),(1.55,-1.05,GROUND),(1.55,1.05,GROUND),(-1.45,1.05,GROUND)]
for q in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:m.quad(*(v[i]for i in q),mi)
G['SceneOnlyFiniteFieldGround']=m.result('One simple low ground for this scene only; not an additional reusable model.')
FEET=['SceneOnlyFiniteFieldGround']
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
   vv=vertices[i+'__'+name];expected=[stored_point(add(rigid_point(i,p),t))for p in g['vertices']];assert len(vv)==len(expected)and max(abs(x-y)for p,q in zip(vv,expected)for x,y in zip(p,q))<=tol
  assert abs(bb[i][2][0]-(TABLETOP if i=='p'else GROUND))<=tol
  assert bb[i][0][0]>-1.45 and bb[i][0][1]<1.55 and bb[i][1][0]>-1.05 and bb[i][1][1]<1.05
 assert bb['b'][0][0]-bb['t'][0][1]>.2
 table=triangles_of(names['t'],vertices);press=triangles_of(names['p'],vertices);mask=READER['np'].max(abs(press[:,:,2]-TABLETOP),axis=1)<=tol;bottom=press[mask];norms,areas=READER['normals_and_areas'](bottom);expected=float(areas[norms[:,2]<-.99].sum());report=READER['actual_opposed_face_contact'](bottom,table,plane_tolerance=tol);assert expected>.01 and abs(report['actual_contact_area_m2']-expected)<2e-6
 return dict(instance_bounds_m=bb,complete_instance_count=3,distinct_old_models=3,new_reusable_model_count=0,whole_oriented_triangles_and_pbr_retained_before_float32_rigid_transform=True,actual_complete_press_wrap_contact=dict(complete_sole_area_m2=expected,actual=report),original_table_ground='Existing extremal-point contacts of slanted bevelled legs preserved, not planar soles; no stability or load claim.',not_navigation_or_full_space_proof=True)

LAYOUT=layout_validate({n:g['vertices']for n,g in G.items()})

# True whole stored-mesh horizontal centering, not nominal primitive radii.
vertices=[p for g in G.values()for p in g['vertices']];SHIFT=tuple(-(min(p[i]for p in vertices)+max(p[i]for p in vertices))/2 for i in [0,1])+(0,)
for g in G.values():g['vertices']=[add(p,SHIFT)for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT)for p in pts])for a,b,pts in LINKS]
def measure_basic_geometry(vertices,triangles=None):
 result=layout_validate({n:[sub(p,SHIFT)for p in vv]for n,vv in vertices.items()});result['common_scene_centering_translation_m']=SHIFT;result['complete_source_instances']=PLACEMENT_RECORDS;result['whole_reference_glb_pins']=LOCK;result['new_reusable_models']=0;return result
FOCUS=(0,0,.48);ORTHO=3.8;WIRE_THICKNESS=.0006
CAMERAS={'thumbnail':(3.7,-5,4.7),'qa-front':(0,-4,2.4),'qa-side':(3,0,1.7),'qa-top':(0,0,3),'qa-back':(0,4,2.4),'qa-wireframe':(3,-5,3.5),'gray-front3q':(3,-5,3.5),'gray-back3q':(-3,5,3.5),'silhouette-128-front':(0,-4,2.4),'silhouette-128-side':(3,0,1.7)};CAMERA_SCALES={}

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
root=bpy.data.objects.new('WholeBotanicalFieldPreparationScene',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='scene-only ground underside; unchanged complete field equipment at original scale';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 # Preserve the already consistent outward oriented triangles of complete source meshes.
 # Reuse the winding-preserving whole-instance scene path validated on the loaded-sled scene.
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
assert seen==set(FEET),('Scene floor forms ground; complete original instances and actual tabletop seating retained by layout_validate.')
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
  files[role]={'path':f'assets/camping/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'scenes','assetKind':'scene','theme':'camping','style':'source-preserved-faceted-field-equipment','title':TITLE,'description':DESCRIPTION,
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
