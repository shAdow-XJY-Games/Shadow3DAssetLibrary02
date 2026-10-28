"""Whole two-digger empty preparation court; two complete accepted models rigidly reused, zero new stand-alone models."""
import math,json,hashlib,sys,time,collections,itertools,base64,zlib
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='agriculture-whole-vertical-auger-and-rod-grid-digger-equipment-court-scene-01';VERSION='1.0.0';TITLE='Whole Vertical Auger and Rod Grid Digger Equipment Court'
DESCRIPTION='One new complete empty agricultural equipment preparation court, zero new independent models and one scene. The entire accepted bent-boom vertical-flight post-hole digger occupies the left rear-aligned bay, preserving its continuous high bent boom, full converging lower yoke, complete gearbox and input enclosure, entire helical flight and all three attached parking legs. The entire accepted broad-share inclined-rod-grid potato digger stands separately in the right slightly forward bay, retaining its complete broad share, every longitudinal grate rod and rail, four full hangers, whole high chassis and attachment frame, full eccentric linkage, two gauge wheels and front parking leg. One broad chamfered common floor, two short rear edge strips and a short left rear return define an offset two-machine court, leaving the shared front region and a complete lateral gap empty. Both original complete geometries and all opaque PBR parameters retain their full original metre scale; only whole rigid translations are new. Whole accepted sources are embedded and hash-pinned; normals are recalculated, with no raw GLB byte or hierarchy identity claim. No source mesh, pin, support, wheel, helix, rod, handle or material omitted, cropped, rescaled, recoloured or extracted. Unlike the old mower/subsoiler court and tiller/seeder bay, these are two whole newly completed diggers with different high suspended-auger versus low wide share-grid architectures, placed in an offset empty court rather than on worktables. No tractor, crop, soil pile, workpiece, operator, shared drive or connection is present. A preparation display only: no sequential harvesting workflow, boring, soil separation, coupling fit, wheel movement, mechanism action, practical access, support load, ground stability, manufacture, engineering or safety capability made or verified. Rigging animation physics interaction not made.'
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];INSIDE_TESTS=[]
PALETTE=[('MatteWholeEquipmentCourtFloor',(.25,.28,.26,1),.97,0),('MutedRearEdgeBoundary',(.30,.32,.27,1),.93,.02),('WarmLeftReturnBoundary',(.39,.34,.25,1),.94,.01)]
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


COMPONENT_SOURCES=[{'label': 'VerticalAuger', 'sha256': '15d6f3c9076c5a68182ad3c5da11e772e15ad59b741cec1a47c012e6d254dff3', 'encoded': 'c-p;vdvn^#vhV+V3Z1>`l%!Y?z|TOm>Nt**mD*WOuI;tg-iJ$30t6@)5|#uuN#(nr{&mmj1$I{I?0Zucj7Ib5>FMt2?&%)>_P4)%N`iS1d7<&Jh(q6)1&{vJ82eGy9LMp}*!W2nOuVo;3xoM0Ggfh$HBqxU4d!z{X$Dcc3KD9w@{&9H<3DD862wX0NHdR`8eWnaaTIP_fBW0t8o_cE)AQ2H7S5M6j+}*;F2Z2!q}$ZVf~D_F;xP0lSrA956Hr%K9EWLRmJlo}YDIMo)yZdiY~0+QU*EcD*}{iq_doq{>*AF)8qI>xAC2r*;-_)Ap_eTJlBU);zqz@*bxm)c1e0}`trNe=6L01dZ+g+RS(|)wXY%ci+5gAo_05M*SFYJ<wOehofBWI~<E3l9V?@58{){(3B=u+fL-l986J&m-{*2#%_P5-h*?4<-b8-FQ^DTGyDe{fTe+ajRx6T$ZkX&A*Y?1gr!4we4X||>EI()!X=q~|75E((18u3G<7it=$tI*q`k>4`TjY*8knNMG$EQr?eIyDvqCKH3f#E`6`)ZnGa7QPX${K#0ZRy2;6W!_}L1NmFu$YR4YX6rCC65mUVIem=dM<ZRQ)Fh>)#dxVtfOs_CIElTf5ylVH(Kf#GjfWsx7}-NiWzihq&^i!}&W)wN9Q#S?=-#u$i&A=-`l|WZ_m&PfT_y2acUppOMdZp$;Tg+dIt9*xO`I8%Bu>+G;mtCFas~2Ad5)NN%fLeLfRm7rH8m2Z1}~aZdp$W#_r}CalE9}?1bj_HG>^nrL+7Z@7Qy5W@G`l1&HFWR3(*x(WMpI>p_WEl_#t<oIFPa98RKw`Whvn<UBtYQJZu`qE1)chR_m-eO@a;eLeuag%z+5rAkLFX%|Z{u_ypP{1~xU6GFgIW2?5~%5Go&29mb7}I!nAI;c1(bSDM9%HzzVmJi>3wxTV!#N(16R4xm4P7W(s4tqq3BX+~pooOqKvKVxWOtUwZD1&h`+1qOxKprEE%5RuqWj4~%Gpw`6weoBxm)G{t<NJ55VL@~OjsS^t3K()uUgRtqX!9TQ|9(4_YL~mo7e!3oeX-ae$ZXF{?Yy8=#9=RF`mKBjHcOvWNpeeehl0}eB77kVNh%K}Am>_vr_<o4-1fL?}{AtVhBMO5%K{!Kqt3V4fUO|)-VUq+d_|z%$Ou<)9g>IQ77`GxvW^tTp(V$p>z?pkd@YRDf?i=d@l7Og)5I7YMoPo#6KoJu71$QFz3nC(TV-d5splR}a(@LiWeoEc&;!b^kMda;8cf|WFlR{eRgm?nG!`R~<=K#UTwh5LR94jQSjHiUyuYN*QIPoLAypfHGFhkOlRxf8=Y*W01<2WJQ5yIk(C+`?xK%!w8%Yz7tjOZerFq=8TX9}r2_hpc#Tv?MdiD^F}KB6i3kKQCJ%WuH{`SueF1{!c2gh591HCbmF){t;Ei<6}nO?)R`9NJ!Wy^w?eLqS#6GwPf8n?{L<0DK=aLI0^Y^Rq39r<H0)wWmJb5UB*S0L1o&g^J!8vS5{hM~G=6-jNC6H1%X<_|rLY_BCxX=$vR|$!IcGi)|WAQkkpAZJ5U}Qp;?-cfWn_fBbOu_ZxRG>|cDkx;?+R<?rv$Kl9%=pRO<Y%ezb3py}_2tD6sRFGshRH(ast`TXPM?d_#Iu*~1r#2}w0gvCFx(%5DHMPz;+O+OPEe<bN*I#%nb?X<dQPOH;(I=0g~qsPvn?O5hpk_0yyQ6aaM9hutxP7)*ImWN%Zb$CkukGSQ@34J|7%L~H6B=)4?ds$v;c|j5Y?b@fuPOJTj{+}Il%hN*wfyeyQOO|i7EWXsD7>$kz#3TCO6);b^xjk%5{h8rSr<Ui8?Ox)`#;~T{!+Jc}8blSwqqD{C{xw)}C7YWNFYRm6e5T2A9nw=;Z}K9QCTQSE&1sxfI#1V2s`pISyt|g0Sl*yBd@&w$hfR+@=v!y#sBdkQwdJj&zI9O6k+;%iMEqcRIS5cFTj_n0SpuA=MqblqP_D*v?7UR1rH;R(IuS`-XXDHq>d8rHUF}}O*ti410&gSMjQA|G9&P89oug#MUsw3L8TMzo!95q>qj)x?j^c2=^j#nd@NEY7G?Aerc)?RZPyF|wGaTCX%M+t$&tC(4CAl*9t&S7=5slF7&;*QNrh0$f?&ZTLK5Io&s#ON0ui$9P-v;w>>XuaQ)&<DlPb^-o8VppV*Y@7IA9Q-dgZn|RL-6*oCz4F^!qAFbx5N7icRsMjv=~E_p$qQTiO>zdZqZ)7Of8$rJOHHn5%_-X_{~?`Rr|F|>+%}&Rsz5lC56W0r4Lfs_i1&C^)O1S<fs+qjtOn=2Y4R3(_ljD!8#gYf(XFFUnT>RieBhydT^O2m|!4L)6vpT7giX@s}!UXxd4tIL8JW*FE&3r1A5+F8d=Q9rn$=-EAIhI`yx6B>MKu`iI`A$R}@xS5hS~fdS6_N2+RJ@s6T6Yv;z|@TXz`1!RHspx;x+ji*Er)OEC>0rJ?>YyO8h;i3G59V!TP>hTd{K^*|raq-W(UY`?H3nsx1_m9sII>pDci)6@-vG_#8NaNk5$@j8Rh2ayAvg*3nzFVI(wF454z2U911VFD%QpkZ1H`4)}(upm{#z+m*k{`F8}?u&HhM?@!3DET#B(l8U39tK~UB&_ho`U0ftE{3QRK-e)918*pRjMd-C(0=U_MR&SAWnuZMg%@otP_k~hRxLK_@7>V;)opT92663d2*iQ#67koBJ}2NZJ0}eS2tD8N?n`xfX@+)XWI}FE4g8)E4kWGOmG#B$k4ag-qk5#K`90E9$;diq?j$*JnIv&ynOAYtOxeaHD}S<p(FK#+B=nX#7wQIz?7ku?dMmW_m?i6}KiUd+uAFV#*>);2_^&U$vyw&6SA3<&N^{%_L@kWE0*4MP+O3?gj5X|910H=S+t^o@8!XZl&oPdeHZ%v=y;%#&BTaIkP)I9r5IJM|?;S)o$osFcW8ehT<_rD<$|v?D;XqP1<Xsp$i=e(^l_rHb48j;2=^~)dVLnqT>~LX63LjNrn+s`g8dhN#SZ$~496~p-j+|rX)H$JVZKp%ukLX+1Iia#cE<2*{UHaCc`lrsZJuJb`;xnE~x4>AEzjPwE)5RPfT;8>z!eH+J(ac=xmqxR}E#uUBpvl;;Td$Zn8H~2wUrRgLR398_MQt}5R~M`auPi9t!2l}N%E2d8g0+*p;B90Qr?Q`9-ugxGlH{#}_nVEbkOon$f^4vr1s>`x2y6#T(i*xun@0c1HI`Lg!N$>iAuH`Y2I>Dl=CCrX5Tl&NbzSq(WOQTMGMRQJWJ9o(2mBeXnK)Qu$MO`{On#DUzA(=a?>xsfK&SS@$onLINOvi(woU`$rGtHx@r4%N*&ghp34SHq_hpABm@}P(%L#ztb2Pwu^Oo#{sh^A#zdyE}$By(-0Dt9nj~sDyxbMikWWrdH{Y-iugS84?b`SKotA3KW$;;}TP>yw0?h>rBkrd1ViE@yX5W&44l=$F^=A736KK9h8^U0N6NFJWpko41^WRwb$zDk{m^R?}K?bK1Ue|@2cJh8+yCulEEtn$^KRaP@%smm}7pIu@6`^9+2e#OG&TJqwscgmP7;3bM@SPoj3aTrhT(pCdiT$4@Ei@Y`5&40kf0%O?hiwNP)23E7v>YR|MY;}*1iQ$^9&JmtY&f4@ub}=5#j``t~tmJO1-Dyj`SN!UTpL8dOrx5H-GIl!-e~@$_32hdR7x8V@Jjm=k-tie{v3Lf>K|J-R+G#?XMB$lLv;Cd@wwT~&xNa}<_h!GuFGVu~@{mC051Py=pg%=H`}B-94(YV)O0GDD#nl57h<)yGmYWVylejT*K~x$}p}R5|i8Q+b=d_x`M>yr+thmjGeM4`}KDKstViVp^2=9dNHvMUxoM6qQsPzgZr?04_t-%*BUuhETNJmeELS{TComchRL9^q~UO;Stx&<jI$6*fQ@9cCp57I2L0@{pe_hxURmCj$ZP7aS5MtE6H4?!U)?VeU=Pq;qr7Qp82?~>17T>E9mWfnhp$yBcfQx7kR>5#Clp`QU_ybT1b?iqvCJtVM>8U6cOlvZt^06ziXXGZ}1=!lmMX9fy8pK++bh&j)R_j3^CxGB*eHFD77>G3gj*ge({2mDY%8R6#eq@Y96jCtDoPA+msB|GING3nJn6!FX?n9<$_&76p{U7sspDI@2kU0E}p<iuN*C&{dJ8BH&|)xOzLZJy8}X4meV>4yV;sB+n>E@_Txc5*5soW<u2)cqcS(f!Wa93GwSu+%TcAN$Uq0-V0giPUl8!N*iy6s^N`>ab^W4$m<kqwr|}lNOEJYS2D$2GwWCER#6AH(9Mt8&uI|vB?kmd;93H@?9zodz(VPc?7Dv?c=?h%pJB7lBJ#Fy}Qhv-Zk$kdkir&X=isYuGoIRIuNz!%CXpZ|IZ`)iL#*H*U_FWxlj00gz$+F$LKAH{c`J@vZGNo-p~rded;uj9qOf`S-|dY59-)D6r!yY0D3RvDD64jw&0058O~x|mHju^UR^VXm!SNo>BM}nJzBaXO50~`wGOHqXBs5p@^Z;eA=|=+Q*E9ts6Ov-84iRp(tZdOp|lGvwTfM8-#K7@c*(R?9C^|{?)%udQBg}<K4H5S&+|O@CF_kFH3<U{{si{%A=BBb(nAM(H1=@y>a^IXX<tXZGqrCp{!R~N&+Z%(3F8BMcFvoB;cS!Tjy}iWw<Lf5!Un@rS94Z#yvY%BftR_Ek(qM?o;uIsw8OJFJKlMCrT0aCctuiyMNy~I1uwSs!vQ}i6-B1Idnhenii*NAfz*;*52;Hi22hbG25IAXfVLWdakOv4krrx66<7{yS~R6sN<)Z4t>u*P13`#grYwL_lU5Q0Egz?h0cdfwpBxu#xo?{2uvy+uXiGh*!^<NmaNDK+8Bm;M=c-IJ*KrN!I0WQlkbZ7%p{jIo)&a1GI2`F7v!_6c4!P*~v?wC_#yJhjh9v?mDam|JC3|FkuAZN?(;kY$I8h4sZ7%?+n3@{#_*hLX408tMy-?5Y6L)*T?@NpE)siL}dPwvm=EP$;2<jHAA^V?#Pnuy`5kwK~<RUUy<HUqC@$J($Wk@X{+Nbq-?5|&44658dR{Q8xHO@rBD@22@gdaHNWk9rm(ItbzfLD)Xo3a>X|19k^XKY?)3qSLAj8g1$=!3Sqvrhl33wk(!?xsq}UL{inic_ckVoCdB$GLmiIn&M@J;i}l+F^Mln`c?xSyk~@vD^~+A{#vR?ypc};I>MV>h}ZnU24hG5SuXLLlMd?P<8tdpGVXGBQYGegpuC_b#k_7K4;x3<f<LDZbTLFBKspn^wNmI_<&%5NgQxEL7E|mf}?#V>5dpv4Ha3?3|~1$&Xj5qUeO}39f-H}m)%pm1qmVgL?MGuk^c;)V&?owG<riXNpZ-%y{HV6l$GJaAZ<(EqGpx87nMY7?TRg0JPb)d;mGvtxKl8j#Kx3G#RD6e7#kZ|ag+^2>9h7p=mpCiL~)~<C_8L-74tv_stAB0zD5+xdTfoOV=U@%G*Hl64GthUca_!y>);icFMTe4gJL!TJNUHwB}b`LaHKhL|9Y+Unu-T>ZTCgZarp#vPfI!A#RCT>SXq8{3TLU*VxQ;(e1Jvmk@Ed3howA}J#6BEDf?e5qZGc_{m$4gKXS%?DV(vpj<-ylZVIfQ^)r>d4>uB5^#O~$=On*hMTWLtI23?%1dy;SKvQHkiiXZ%Va78BvLdGF<jDXorr~A0VOv>+qTuM|7mjl(=#XfS%pv+hB7i7-l9eO<O5t9WP(5v2wi-#Ht}4}y=l+ff`vM)*C!NTqr03Z=!PL*X<*8%G?{o@m927+*Y$)at#>&lI2HHsC7$I3+_N0o&V8{kpqO^Rx&ORlL+o(m`Y19<>i0U~Kt)j!fLrG2#d(py;Sm?DO&pK_{R8ETT9VU{~qcRS35FVmw;-m>dQqY2+f(UyZ<#BY1Y}iq?Bkmc5-T6V%@WiNAWm>l?_784=+H|O@OonaXvojIM&}s27+_5VZTsoQ%roTvGtg4@~2-ZtXCgQG1NaHCKmLO;EgXnD>Zm6KIF2{{TBwlb0@v%v52Kh|fG2lk_RSB~;m7&E>(A;PcCtx+gQ4EGch{J5qA+{QVUHd`CS6-QtKjv(&?I5+ES-4+}^BMu<VXR>N6$fF@piZP5OQ|9t**2g0swL?P2(?TkP|g^8so!d-C`^UeYhsYk5`p>ApTCiJ%55nR!0BOIkXcx*T=MGZSZ!SeM#~YQO~iEOQJ;D~9`9aHvbi3%q|dWWbs`M@L)#Q_kGqq5&nF=_RG3?)m?J7H$7i?A@_^>qX7_<EJ>XJkN9_EnQV)lwR)Sy=no4s*xSO6527z|#&-I=o(X&<DR~)ibHwS<aaMISBjrPWJnIMH;9UYZD$LvDfAD?SFXLWpIC`N;FCU#EsfO|<7)%6l-AM2?G=lHB$$kWn7F#GPVge-xsD@Pd2ybzqsx%}KZdv*K->Z>8d`*5#&S3nhuP=*QUFMwg>i!ur}KFg7x7cn~=mEp;^;N76+G4UQLHRbT?{eqlVBF9EqitJyCywR@IQD%J}2Q^sn0W34k`_{$_*M4dhkyZ17sjHg9VgKg05ASYW3G--LFws_nU|7Uqsj4>Fdyh}NvR`)dBi}(Ata(823HR2Z=v78{)lojf@Dzj%6?4i**ZUi+vQ)xnP=y{)#;wGboqJphp2r@2ADG&^ND!dETAAuy;wpU)df14>X)qbh{dnnT$u^HUbFw60Z(HhKkz|HQQbBO3Uqq(au8YU_Bp19e+~@`3T_7!Ea(A($&M*(r8>ecCy2U!6PuqUo^_!>p@Q6s_%JoI#$_G2ktom?|sFT`S=AmTltxfz*;6IF5Uv*7Ji&(o&DC5uq*h|a|I|lQoMVPucCdv$)@*cMICkrnU?+@)?5B@46U5Ped8Ut#7JTo2iKH}av${|OsBZ*2Q**Hf?q8S04ktETK5Ebs;CTp?;-hI0G<3`1z5L?^*PuI7<eR2<5o#XzWAFeM)x4(V3`1{r6&5aALKW$u`|9*LWe&c>Kv&DKjj=Uf=dln*O4qGH5%zLlNY)OU0jyQHYk<ygRXRg^U%CdOH_1XxzLBW{hDwmWR!ul7XQ66WWcv~6i@P79N`r&edpsC-aLAZ$5ewHEb>}(&HwHh^$zxQSGqnnHKkC%jk@1&)?`FMHt_VU{J{M-4>B@Vz<F4uUqb;ejA$@GF%x6Xnv)wy2(@S*<JUbe=YMFyf!mEQd0w_AE_P-iW8hT`!TYSxncjS<tcxctqV%a4~Aw<K0;Ri{3Lvb9eA(L9XDUZ^4}SOzRX<s3AFR#PwYS~^NJwR^i|t;8qu%(s?gK|-N&Q3c*J|B-+~NuNJku;NF=-ta%9t#q4a{?avnzr4NvaAEGRLxk>+lquhl?rAvqBU=*o@0u6?x*)Xc_LJ=dIWVb*eJ6Eky=pIff9iHl8<j%f!JB%k42nNDrO^c?{hf+aKZ=7iufQnVgut0pWu}Lkk)*v%_*_dhV|o+CQv$X;pqeCJVh@eeAgjZqsz6?NQ?l@>57&J6;h&dp&Am0;qbdS}B`Nm>t~rU2(=SLp`F!=h)=91QBo5<5jd}h4&3Uahb+#NyZVYE4su^GY^E1)o<y(>yvV3MwuOG3QteM%PMRQEO9%hf5I;J2}A+abf&|SP5@Vg<kQK%zO8O23s1y1v_G9n2s!DL=+_Kv<w98Mg~g1LnaOiBA<GJ6QLG_QRWTAt{SX>u0}Pm|{psM+kT%p2KeFA?uWV~uoc2z`!(>v(>WmP?r5S4S3OzV?zSt;NLE%cA%HiR)@=b0#_-chVs0&K>s>Mg>B4Nco;GXy?p4=42IoPfNUX_Xxbme_;Qa-Cwq*!E7c|q<&ofq|$<^v7z=??y`l)5yUuuOIvf&bIi|45KRIigsJi7=IuL@)T<WzfzpBbhU`+~0v(z|lGrnE9cCj|d(<#R)oXws`DwaSlP6ZH`8%c<29uqNJoi$?^KiBBc4~E6r7E|j{4e8ApPm2p2JLc#OI`Vf@Bo><uR2yp>+-avlsA(VZTUX6g#HI{g+ys^5^)F|eAx2Z4S39oMUxFrmJH_&;<zV?gup6&;w1+c$Wlg<vdU3*SWVUPKTjRWdnA6mvoIJ;(>NQLAiQi8Oi5MdylYj=3dJZtho`q@^IxWVsZ_E}kgmOuH86V5BqQ&Ys!dZ_Lj^bGv}8fWU#V9w)QTeknQ>mGXpa>yS*}5{7m>}(zUY^d%$Nl$<)xRG8aCm#5s(kB91V|5_SSU0T&0#`JSQcEWOV0mQ>8h=0|N%@kGCAHK-y5wYRbS-sW4zJzr<an6!{g_@>@`YMyoB}TNO*k84MjN;3O7v$aUANDI6YlKi<Fi48ih;3mQ`gDtq1q8XCr!L;!%}UPzN#3Rvt=M}P7X$`!4!7fwciYJ_tK5*5~XsZwo3p`ykf+kxmOi_5)Gw?5#Pm|#}IzzRK@TOoN0z7W&HnN|HgR2iuh^EgToeykggaD@Bl&PC`jfO(&$GayvzN3tScz-lOWWRv;RFyes-`G`<6!hr!11T~azeO`AB9wAYdUnL*K0xiQ@>X-n8oJ^O5=Y`S`%IscjLdEJ9R%E+hfJ3xCxnr_}fK8EpiR@6Ccu`+bV$8N8pzS@swlUKX6?#+7al)aa-wJ4RA_HuO<Y#n;9AWCF#aUi963?i|7Sn;`U|DG}k4Wca_9!j0bT2h=E>l2CFQ@*T$IMzpiQelXC5A&ZRnuxKJ2z+nu-leUfjBIZ%h0LYc4%VE3senhVh$CT(0af&<5MHlF|HT<n;Eesrn)xsHfHbX?qFB}H40Iq<)PUFKxPz28pk8XtJwpvCP7N93pyW_2B6aK1R5{=KmZuJ%0z0tqviap$jzd+MCM8GIC_YaaQa`Q3dM!uqkz;xhGdL*da}I8{=pIq9okw;6ekkVs8iw~m|7KR?V&qRgGuV;L`LFt0;>je4NPK9nuTo_i3A0_!ym!RDwKX4k%c^31X*h36`Ykbg`7s|ZlXh84OwG;$JL1}eZR}!k*d{Ss6*MQ<99*VnTy0wzvC<jGloiYp<?^>PRdviZQRaFde=`=?r?<;*W5vxQU@=nM*m(7KqY<$2_1Mnb?)V@8m_CJWyrP4GE+QKd0HQAUb~%xqJX}gzRq5E+dW_*&-E&NJt&q4{UCyCfY;VxZxnF%i*e5D&qu-q&g9tq^EO+=h-;u#KRKeZ2>I>C`PEyMHJ{+(5-$m|Z3|t!#lg`8*FWG;-=8-5R38xV@dr*kSRwF|t%N_}Xw&$E6s9CYbp3=>%GBT_w^pM7#(j!JZ4&J6Q<N!F?8i%g?vdiwevUl2)Rk=Q6=@AjD(cIGzVt)S-ILqg5689QF_NwO;iOhPK~^7)Lk5i-dN0E9i*RzF^SAYP<gL93y#s0B(f2VmVfYW+uAH?Kmqc9!fDjfZ43d<LkWA@<T)D+d>*$4w@F9SBjRL>ml3d>dDh5^uDfaYn+<gUydH3Ydp{J7$KOJ>mAz%zyXG0*1+3k6@<ba5Lj1mBvKp}SFNtKN5%sDFwFZ5>H|JjwSYR)rjc9;Q=ndI}yxC4ZlbcQ-K0s@WOJnXFuk6k;jEc>~!H>1)r3!2nKk4PnN+Z1ZYA-*>!3PdQa={z`k7{yq2LzrzuCc%_BVwC#fEc4TvdAD+6GCim!CSJZ|q3}PK*fte~g$R=8CP}3`Z&i;#-;+QTJEN$VW>0oT)q?c#U^*fhz(!jSh$VYHF3Lt~5UD9OXq#(%VK29yB0KSO-#Gj6;g*OW3PO~7H*)_t=xgPQo6%AnJPCa-!KE86oZT{0Z%7taG#y3sisoaj?7`vCk$2;L?{dStf-o<~Wu<tW7w2RD3P*CsvCIz<nS#O8;F+3EK1C<53P#5q3mo&-IO1xfCFvXiL*<w>pJ2IOjyRS#h{>4IeV|(Y0R2G_TXgA}J<l=6q<Ub{RCB~3gx*R<qICll-z5|!NR2lkTTDjk&p85IbR-=ZK;}(|OHq`^U*({&IUvD?xGM$fUg}VXsuplIHT3v~A`V|p3j9ZQ2UArt<5mg7UxaV_%N6m_IGz&MP={zBrw{2m!Kg&t5zW;n<4*20!RdkQBcOYZ55pB{TRBZ<6ZwISd}f@i#d}_1ik1{uCiSn*dW8*;?6Hz9kf*voubO~NHyd~GSCpT<s!xBCxYlNaTv7UL5ABw^gkposIHX9l0i63l2CiCPn_opr%9-7UL}H8N+=&os()#*hz52D?E2VsY%WYE7(}3x2V;4H*W;1k5tm$akC3;I*;>v#6{a)w~$Pxd=cqi*EH|E5vl_HsV9STKxYKxyI-fAItN;pNN6Q36-;!I^>kb^qH&~hJ1!;lL~Di@mUxpkzWQu}#_M(#9UMIswE@~im~d9~wOUhSAuh)C6za!*;PE9YM4=F-;9xw&J`&BY3ng72b9pWA^dFgmD@-t=^0KDr_0PIp7E9Qw~);jiw@n5M1*{9daTv|ZTHI(J_9{2~q9X{xUr===2K>nC+(K^pvr>jyo+r`H_EpeaY_Nk?SJOw*UvG;PwBV6zs2mbF%XvEU#!7<c*_gg{+?Ah|60wGczQo*Z1dF#_kvG)P|ZYge*a+YL7El{m@w2@amp_Yf&s2xEk;Gm9GcO21CZhr9X~1J;J_@or6pPX4s1JRx`5<P<Bumxl<pE)Zbt$+EKu=vM`UTIlCR0s%S@xJ4=bU)V-!nR4!jSfFXFLND@p_Jt(4uL%M+H$Y9`kNccI?!h1YXyb+-Ot&g6?s?-XxZdzQw}vPn(j1Z^*dLGgyc^RyQq>x~Pq2reVDrIh(CZEhsA=o17md}dJbv%-cg|!Vj|=w!I{Ve7!Sv?2^0LWdq@~!<u@VOln!%Yq330L|vI0AeA0kCj;FFv>KqvWLO8d>&AH}m7yrw`n*>)>ef);+J6|9RrnulO==m3^I8i*ish&^h*s;ApOS7DqF&@d`|SIOEUbcuPT#CpD@y1K@#%V;Gf&zpX6zln382PIxst?*olCyT>>MQu5#jNYU6gD(Pq3kdzfppu3r<>OL0)v+6?Pi7MaLWq#v&*Et;QXDVrhFl?o(w?k28#U+*Wqgl{J#3<G4<FohB;9C4P%nA32aUyp3HRf=us<Rd#YcOd_<>EQRHG?i=t#e^eh)wZG_C>wnYvHwBM1W`6llhQ!(NkgA$hoy;+iM00`yWuvZ}j0uta?gO5Oh@I)1+4<4eUE#@&BM0#xD`PRl|>^R;l|aB*`g14gi7Fa*hf&n%_ASB14xl$OpKY%q_`_@hVO;nnPD5M+?zm;-7z85$nn{zx<8_+!j%YB~uKcM0D8q#dZ%Bh{L%R@Se@3uZUwq&DxFF-ICTB-@`9370nmBRAhN@g(@g4O*-rsFhE|pRIBjO)*b|U9*1|y7=--;(eg0z#U37%!EAU;!!tdmXIiQfJH}FCv+CL*pE#d&W!Z+o1+{zc@K7DiSVA0zaeqNcH92gD=kBQ&hc3nHg;oI5zl)l>OI|IKaAahj-x6m*gFc&p*`#`0;;P*v3^un4!_)iI5`#pHED)16slMI>NiTEVSHN<`#esCUNn=wc8`hQ<z||3VlDZWk-vU?tA<#W$)-XzxCAR|W!shCN;BXMjzG)2z5M6Mv<vCFGay;BSA5;?#GkGciT~o53<GB+Yqr{`8t%|s1{txUxif4E^2u<7fuk;84ltyUS5ckQ%1Ek8X@>H)GJpi(<@TKB%gWicQ=B<FrGsimoiID*hfmk^d9(77CY>1cXnZ8ABBa87C(Mp{5qnwfsod|)g0_p|eSYYy!P#>P&E_T_K<9_mtdv$yr*);AYh_E=dv)T8UEIpYjaYCkywuCG#Nrai93ix6gmsszXi8m38|nrMPHj|k8m~#pjMzC~I(+dcpQItaO*8=#AS8Z@i^v2<=||m8<xk>dnp*1g)2{oCn6cGMR@$FCuiB*U&&im-tnKe2cakHQ-OL-P`A@6(Wj_(egQ|Ng2Z7w`7!3DF3flqe$F;DJK~_6Y9onVa15;LCER090O1w^J85E9Pjcb;Zq&>*n*~(S7!ne|e*F8S5O6Tj<9vpS;b4<H{MI`K)J=3;ZB>RcyE&8_bAE&__&N$i|s_~y{&>sg2zP;4pg0+Lvg8@#$hrL+0f^H^<TTdL<>LYb@z47HBT>~IqtC1YT&%<nH=}-<Ak^Z0lxP58zWybV!Y}$^huOrjme|%#)d~EEi1ANvnbhRzn5anlD`fw{}%XyK$#y72&BW=^ur*<m7AxGQ8QsPWJoc{)qWIFA@EvwcV!x2ae)VTNDZxR<`_BbZQF~{O0G&zuxplhkfl@WC!;ZcRUSa|%+;<%nqR1p~f|0b4NA=~T~3s1xF)(EeZd@D*=0qTWuQQ|$KWDz(Gqd4NH{_3Z_i1LygZUVQk$doTsED_RvNp}$?ex$0y<cUWrxTL2Tg>`z2h%>5?^Q~3_yxHsIe)7Vzu2iGk!EW}RcD_5NxKDG7t70CRy~?9wR<$O=V@0{58ENw^S8b_}LWj#M<VrBqWgJ=;S~Di9U=lotRn4Jv%9e1H7n_t+LV4LtWOYzZ3`j1GL|6ckN{pa$1p={5{=Oz$b~vkrIJ(hzn?ZzEM2JJ?jEXzl5FkY$&@7nK%vI<Q)-Ln1HO;}K)tjy-J`yVhi|UT?rAG>@A#XF%do$Kh_`t`M2tEvP?^$+F;Jf#li4T0VAPfn}hXhE2fGLZ|d(VLgCK1=Q56u5d6;%#G=5e$TXFLTe?1Kfoq~~e{#WH~cry^)9;Y~!MR@j(csJH`GA9M^tYqjNff*lSNRgv$l6>bX|%25kuC3pU6-{y)$AQ{&Pfs(xgn;~Ew0LCFn3<wpXQjr|#%hJzxy!^&u<onCbH}!iQ-(P-1_um0_@Re-P74%A4MEWyA36<|Bh}F{sKscKc95{GVVoOOWv!{k7SwJ|L$KV%W5vm)3z!3jE0H1><R*V)Org8a4NB}E-$b(8BykyzLh5wVpBj%kpH$fPZR*Qx~hAR9!BMAOTCrPkkJFQpx`4Ety2r{$BRup{116+Y(Zt4G5bLhxxn-5K0b4jcAQ$m*4hL$7XIyuQpdIt?bnynupww5&7Q0|pUNh=`Lo0x~F+)$jSX!Ci(p6<}~FUBPypKl#sdf`hlsl%-yL<b{-vmJdEWTK9QpxVP_qkmli2S_ph0K}3Ih=T>*eE(l05a@a`^k3fP?Y;^eELoM(R_$(Jo|w%h7bycbznQr?S138ITWo=B)m0TQ*R5$)=DP%$IHXb-TIv=8?4`P<1ajB-{N~yqvtbFLZPK=muucqB61yxGO|Wk+!F6Axa!l(|T)I*xzXjMrc>?eEz7~!Rn!VX<MsZU~8^+I;6s%;vfh9;U^<YhoA}v?oNJ}jk`+QJnneQ(@A@ky2qwCA_xBoI7;q!tS6w~z43CXL>YJ(KtT)zKsWt{(U``f4M5C47n*0}v}c};(=CEev8oxUMk2mi2z7ec~pjWG-|-b)NG>vYfLgo-FJ84-M>*L!nESz38=7|j^v%I{jtMQ2z^b*ks;S1ne`xwqml`k=$Nsp~qqL8J@#Ci(_uG5UP{>D`Bqmu?OhAyv@bEG~TJn&%%se)^NM801#y=B8uztj>uup#O(m=j3Q;OGtd^Kgvrg9jG_orIVWvSMO`1;d@i`p(YC#HQvV$H@6aei(kM<t(`Wg+=R!L#L-{~&6C@GB4K^~frRC=jU^MIiQ~g0Ky<%je*2#HadUfq_4fSwtve{Cc9jykiY%@?cdN+Rs%2^oLC0lW7eN^1Qml6w&&<l8aKwiQb=Rn(T4Njr_hjepuUdqC5TcO@KJl$8vK(w9>U86duOK(774isX)e~O;q%z<blDq$KOUM%c5=kx`4F~+AArg32pXZ>AgyEnwd=gd=goE`KXD28;FDEglgMW&${0yTg<B}33+LesRC<jgx01jNGm-2LThgC5a^KPl*UU`Y7sE)AmE45yOYA#<jgYSu~z5S_rghmK#(0Z=SvYb|2J>vM966#5f;rpS~F9MD7tOMHOZ}1~Tkspp`-PvSva?<G>`)6mJSDmwIyE~qAeDCzE{p$D-&aPaEF6TAzZ?vsNjTxLAwMitjhcY`d0ipTy%vc<3q?(O1BuLm)LMYED!h3cBn!Rt|zZWu9?c)#%sl}g4paQiO_S3(7fI2(Nrn8&MWopp|rLy7oq9xWpZx`jYqv0Mp`Cd%`W-wp7IoWEmEB!tLLz&NV?9X6dp;R&ko}FXED5V7IGX%H7rtE{OaXP%b?BsifPdSoAPel##gHcqqzaRkiW;Lq64MS%*4e}(jVexVg(GPY>XULw;1Cx!GqBUuqS8t!&=&QMe1yzq8U83mzQ*XD=zFqkVGFb>Nx6^K`A=oUgXH=D6)jZ|!K2PqHyJ46oAMMYi!j&D4{@<}1Ki}_@xlApcdMat)I&+er<oCo#qj$~o`9ICZES{`W9hS%0*P_B?BTiWRw%m8vvMhN|bJIoSfEO&S*jdHI`Ed&o6RghDb3bnBANv~l>(EbJi^pyj)odiDAm!(7biXD`(ro@W$((<gT+VGQyA)s<BPR2~PaGJV%DDc!PqvrUJVXxliS3-UIhETo-;r@=;+GYgT@>J|YEHto%<Euj;^!5P9C|!DqjEN&Yi0)rp^b39%$9(8PRgt4l;@}Of3#Cl8usNN%r!r&q<r%L&pHVM7X5td@-%cA8Oa#o?T4Gcn|T?{(8Wi;z;E4%ns`XXVHoW`J?w*qifiy(a4VDF@K7>8PP;Fal1a6QN1PSy@;jZ)#LZp$lY_%)Eu`zyR>IdAaa;?>E@2W~T9F)WoNC|1IrkwMV(N<hJz&e58sy5IMPhd(j?TvXsg%jQO$s*|8I|)|_N3M7@<n&J1rISWYQS1o%9}q|x3UG^Jc?6f(WQ~MN*AQ#lyh^Jy@3@t`sfR$HGTsw(Iw-Mw*S&Gjw-Hja^>h|Uxl5Moc+D1D|+$+w^G{HUp!vaCv>|2!9h|Q%(RDvh$sZf_eQLK26t3C%0QRyUOX1n(=dh{ihC9ZhSa5w?F{PKW<|=Es;tw#hP&Y`av+8Krf?fY4oKd;`13FyN1Z~V+b5<{N-+G1lUx0RQUKlAp_38#(P7l`&kpfG@@q*t_K4cCsaZNkeVb3EIA#TA5Zq2gj0_GFeaOq=>`_jaO1<xpuj>}y4f!$8DmlZ~Q2@RV5^kSuU!nqjd?A`wps8(U>Hw4%&as#p;Hi?dsPba)tMU?*yfigJP?n1BrUE5LD2pSf1Y4c#S{!0x>BVDeX8?Nf6H;TT>&_fm3msKj1udW3ZW1MbmgcpW9SHpZgO}zfIKy?-xVb{Pmn~iQDcY~%Q2bX|%_a~0vLG5>_LoA?!g&$}4uR|^X%Rf|BNtj}ymCKk(TWS8b{uRkYwk6~OM2`b7S**hbB>B0mAYs14UV-LkU&<x@}nsq8xuaycvQ@oIYFqo>U`q^D~(28Hu2ZtkVq{@wE>T^-^mBho<dEz&G!cEJGbh?*yF<6<Gv`nE@%`na!|2XCi+6e_kMCOdG?+Gt948pvigs>Q?|j}Z+E$AcQ-74r_XxUW*=(6WsCfGxRY!#JqdFw(Jc1(J{82}dx^NHJpM56htGi7otEzDhC?08aI>>gW92E^n~XT32m~s9``(vBH2w-AS4V4#sY>2tA)cZ8oU2(vt)&Y~E8{G4_Z!Ic;%QA15{;Bvs=&SUe~^gHDL7(BK<%s<6|fXwJNQXNWuyr6sfep9{g*Oy)YZKl_`CB?e(lWeuT;j<|0)9Q@zEV@S_oEWNbJ0(zBO#S)fLvOowo{cT46qLxsw+XQ1bXF7rxP7`(?LTu2>q-K3K0*gY8xt(BHic)<{j*yHIGQhH9#z9o17)^=!ZBv^vKGaQ!-->e-7`GWs!^P^C)O*Rc<OX$R0gmx8m|J~uMrho#@bM=6XVH~E=n<p_*Kd>E?yc*Q9S5S6@G^wZ49E-YfrK&c!9#LQXJIUpl+Tm(`L_*sGy_;Kk<T%I8k)hM}Ys#lBQo$;{zp+$oxWY9b;cPtvYDz<Zmk7JghhGFbnM1X%&;)0l{dbPz30P7VG=<2vDDSrO)3Th-Rt0o%H-aHT+xL?Li9)603B_x%~)h!76+pg}l@0Du)u$1W*3Qu0QbO%IDziLa92N!jh@sv038oHG%l*<7e6Iar`yQUopOVHxG<Pi(#R<Ej~S6G<DCtG;piyKLb{0$jzl2f2=*m`KG#|{UP)kG{G*t6onOZSU$PVyndFS;*1oXukU=8#K6QW*g=ZSkOdqoglM!qzr5A|z3fhRo?s)Eyt!;#7A=3mrf3Z;$hgn;KWTOFq<nocMe$&Ya3;#W<u!hPPmz5NU9tZL#pZojX$0C2myLnZ_ghTzzz>Z!l1b2F^-#KSC!$xk#gdw}DWZq^{fU)h~6?7sSz%PLFz6mLp^(J8`+Mhx#pZOjBBu`0K|$fOJgje)nVNM1F*TV{bI6`yQjrmGWHCq9UbhX{JDqQ(nmZ-z+>LfGaAHAK3U^-?)Mc*`KVdgH^fKk9?V&fDOk<l(9gN-l(1Y5(j><8Oh6q>ryg7&7n4mYBK35bF2T9b;W4O31**(v!CCUqi2D5E@8HRvzM3i*nydUqkp%P@3PN3cyDmsG!(Y}(=PMkp2B@Db9$>5sJ!b9L?GpdEPRznEe`u<j>(X@Uz2l%lzZMg)42DvX80}FX=N)nd+Lj0R^rGwzL38-rjN8$GNtk+yBq(_?fLaBet5SYfTLr~Q~=B>c=SV-3mgH1kiaH~;1ywK98IBBmR=DV(a_NrIz)m)B1RXVe*gUO^7it{5Q)bB04etWfd', 'offset': (-1.1875, 0.0625, 0.0625), 'rotation_quarter_turns': 0, 'seat': 'WholeChamferedEquipmentCourtFloor'}, {'label': 'RodGridDigger', 'sha256': '0d69445ade61a7426560fd815ee4bb89e7f36e85951309ced11de95ee5897d97', 'encoded': 'c-p;veRJAKv+w_W3Z30LB`FpP;MYL3bsWdZ`aW4FWqWs@=Wr=XfDDR-ge8GZQu*$;f88^Z5ZFoXdG1YBFdEHEPrprfPtWknFTZ?D!)X}%k?}A~qQH0vCqXlt`DtK;@i+?OVA4#JNpqTp6JwF&ex5WZ;dC0L%`nauVH!}epWe}*;4u%<FiCqxM%BWx;itKg#L?RQ<(FR?;e3(M^W4v8&gU$NotdA_qHyG7>&(f+dEktbC<?}Tn8cYAQdfDBL|NlDP3AO0j=F~G<P$wMu5V7SZalPf@nPA$kAL2Hcx4TTw_y|vhqjvrSrV=2rAt5tao#w+zCOS4OrPd6UPk#c4Vt&%BTcfLc+-z3&8^8dHz(g}o4vozudXjXUV3KRZMiM8cXM&`;oLLdp+Dnq>d&}lL{fjoh3e0^N+!m8AoCOVXT0V9%*NaE>$9tiPdD7*$2c(J;2~NY{xY8>K(dfWq526z5PG6uPSYeZ<}<@LMrq<tjN33Kd>SLXh{D@EjHgCcK<38<rHy0}#730F(=cC7m@8=d2Bz;Cr^Yxz|I|}TWb)(bGV)Vn7EWizn24E$nKAa$Gz>E1Hd&^|?J|mt8Py9?;)v8=WDbFp`e8;R<!PvU@blas&lv36)SoM;cr<^UOE;4=Tm{B7@Y7N9Sa6zaoJYYbzyv1YDx56+h)`C5nNfQhil#s#=MRZ=6-=f9polUa2;~G^oUMX13uy8W1a2;qNasdAD+PfN;WHj*AsWs^T7b%kni+pJiC1Y7j9SNtlbmL;2vX{YnqkWR+BI&dS%zj~8uZSXgxT0JlH1!X$c;r9J0<v_13kqtgo3_;6o6PbL0}<-7?U6yr{O3dSqlti<^n-P?)c811~e>9QyQjdGxe8*g?vr&LCpj)LcBCn_?O8Dag>lV<DidhxnM!eXGC-*?KG1`gc-g=XM#tXknV08#7jb=uoyL`x51jwG>#JRLl`fXxe>&8Tq@37q{$M~4Fck$<tQsrlQR<IDS=Y(ylY%0MiNo8C|MFu&XZ*{86|!?af~d0B!`m;H2@i?g!)TJNu<Ja4j7fdT!L8%Z;K?$n?RS6G1Mm(59T9cFwsK6M2Ja4lkf@EMN<gRH<@Rf0)CQC{W$#ML%SJ-vrXaF%tCUNL=YW<Ac#percBE)WBNlMx&~CkJeg3RUxG9-vT+axnQL4N5k}DxLY_R3x}pIJK7bnT(I_;{bQN%agabkVp@t~Sa5=^*9O<v)G+7uEe@@IpvNKD8QlgMU+_r#fnS5SmIneH4=C?U<XRexly7`C+5T3_5{bf1M!%-N8IU#<YFb;xv6-2}f4gpIlYV4D&^813%a=&Qe$IDylYzeUnNIAs;&5G(!@0oua<ZEs()u}cK7rh~Q4sSzH>553m6DAVO6_AVBIt$0boMB8@@_FT9LZAoNY`pire(Qa>xctYp*B|uGK3?9Op55^G_otuu@0*WT=ltc}IV~#m_u}&U;_dnH=KPu~Ha?wxIKR0$_xhIk$C5ba<9L<^e}k{iL}Q-Dli!(JGSji#{a23Lq5tiDr)@j#Nr%36Y{xR+l1N?W#7NwhR~4)w)cP%$jN2YK+<yO<+a4X!*F$bg2<2w)!QD3ydEM?TAta%3>*&yNTPO7YSPf0hTd&akZ$F)Xf*}5p5NiS6<>*|o6$5?Pa@+%gv?Bu_Q%@ax(3k|b#3d8UcSd$M4TyNLkuOPBt;fAJbgS{`kSN8*mvF(AY;HnwwyR0=nI`jPL{C}0$%{;ypn)$nCrQ51dA6KWy=S^6Daf*F6U*<n2QNnb&Y<bj2YqV~9QCb*vX;Dc)VDUu+VWPqjA>P|`~n2nLvD7T=9U2GtC5$qWLK;49NRBdYpD~=sZI>-wQ_D9>d8ro%yze7th~Npfe05*tXq<?+<LT~S9XDt1%F-O>uS)u)eY{s_#VZ#1L`P=mh->^q5$8je@_z`ID!{Eh4jRK_u7MjZNEG+%J%#<#Mcx&Znd2#h-rjon<ij{x2pHot!^=V8t^hap;}cydJ2xF{B7_eo_Q6E(LDou2C2o=s=+`-nzr}OeZSou?A`afZGyK4rA`YOt>9Mdd2QAQ+<D&`5itfRLl@kw14~0*yJS(#Gs~tj9{{O-1is(eLGu-N)q3p_U0!3}N*CC&9@2PB`Y;pgjHpx6!>CZnQ55Em32pEDcpi9@a7^@|F~c!of*8QZUuFZ6O+WH9KX}X(%rH=z*>E0YGb>7xMFv)hJpjj#;L+ZSiOtVWpPsi#BgBktn!CKQiXK4P7x7+Lr#w|AW<udzS-8=PAlYuz{p?x9SoVL$y<68On}K-Qy2AhtK0iCw-5w8Eeha}`N@xfv4fT)3#ZSqOTUb~bG2S@!B7Z)b_}~v`+_ef3wqICdExLBoD#Vz}bsgg1N#;egI9ug>xNl;sWSK+%gUNx;QX6257wD_TmuTqVgSnHxFoTkC&@iq-zD1)x%*bppFc`hCf7{oX`z)Q2nKch!8}e(sq+!M$J@h{}Nm=2G^%+RjT?|ksgtB8O`u;!w8L7YHf&JPej&66lWQ~&PunbfSKVDnlWZiP9TCCLHyMg_i*W{)Q;?h|Wh<%YIlCLp+jv-}s!5Rb*dcNa@nCdcV2KL6tgxrD~_&p&UNLnNd>$BY(k%fCl^@1o1y6kQkr!1YMC(hF}NiFj-iJKW)j^w0{XRtKkF`9(lO6S7eK#|>3EJbgHmmc$UISGbqk<Nv)ZaM4rh7SI5(mM+wdO`7pVk<3i3ox|^>H-qlw`jF;zA)CXYV~>afh=QRSZ}aOS2D*qV&2daV0Uj_*oHL8zCs~UVlQ?^^xxl$ZLs%`iDT%5)aEn(1Ij1XB#}V!-Q-=AIJ2<6VpS%EIrO6h3+XJR&p|O$Dr|FMTM8dlVT%iCZ5nLC(6?Gn$6=$!I&co1W9NvzwVXD6KcH_N=ZMPox$J<x!`y09{bT3Q9#r6G^_fhhTVO0LUOKTyRvOLW!Q)jMCJfdNFwLz;{nBVQq-B&@4>TG3wfl;hlfh`&y`{91MfJg<R@8R2@^rzH@XCtP>-S+&EgXEpBv?A>3tmRXNha$_?k``2FG=4zc)wcd3gj)-D#!x6LEwR2f*^LlB+<~@S~Pl3(pacWULa{7B^N?zpM04Af5Ktqpb(>+#`Qe&(PVUkY`IK37q%hTsssLv)Qla_*s**iHRGR@n$IjVBs<SZ4bUlTydTN?G<nFjIj=^iKFQMFF3$K&gm>0^yLf_MiS&Km;t7^aC*^ViVDKCdu-&|l!gvy-LnZHzE$6W<eU!jodYuDj$`-2k&L;w4CJXY5$j)Q17U9dzp8j^(OH(g>xj844gU-?m3zd<U!UB!5msSwLz3)}z;F9KC)Brwq)TqnJrCn+sp4fow)1MTS4J3V$I%DTc%lXo-qi8pMVTU|HVww}ImnW!vxr54TMyz!ihQYHGE-b3g3AxTJRwNtjDQ~RH{RK&E<5%NMhiy1kSPdSkxS=Cap>YuB2>p!6EtT+E8R>ExOa<q0)5hsH+5bEwdyLS8sGeuCv->*@rF`t`a1vb68*?wqQ!69`ftDdub;z%DTL*_u(>);H_xKq8^5Y&CxyR&7pP;1WNROLwQ62H*P#!uX+d-_b^%jH&9rU+<I1sCol={d|x8Xd)n|UxFkx$N`eil%53&*0#cARxn0eAv%xkQ0{a#RJE$RLABmt-;es~{63(*!u6Kl0a%dQ&T|UHB#R668Yb0+#P$+2Q5fJ?R`W4_t0WvsFlXBO2|LkyHRX!3z%7!eQbFWg2E22qlf|Heg|rvS->g-B+@#H`{Kz1+<if?!gg#?Ht>{pZ-4RsTBkEx&$5o0*T_f@VVXgL2J)i?{SweEVpyidg-3*x9o;CR?0Se6A`Kj%MekhjQ~pfXiy0)U@W!3>|S5kFZuow^MA9#Fr<p*-e6PU4Y9#r?-1hsAT;2hk||Oz<bc?>H8*jjTTv~ah2y)euy>7?al+pg#(0_Mnv|yC8oalO>Vp=e+U=YWs@?W}>q%kioCv4y5~dFbIwLT~qI44mPs-83@gWOR=g295p~w9bW*EHO+k8ont&@s$RkjRRl5|9T6aXjXPDwJ!ObK>;_PmyoB0*6JPs>sB+JCig+fQn`gF~u9A3SxSQ%zg%En((c$__>=>Ovly?tZ(a=fn>-%W0eDdZ^3!fy#OQ#e9ny)iy&){pXx0CGs7r2?`jb?@&!tNR>VSxKRruv^jY2=rx&%+}26!#a$2UR>2g++!EyGpy^dIkpb=mIlRO@kDUD~a`pu|?GA(k(fExGn__{;k_c>}qU-Tgc2Kd0!+Ue2!y;MrIQqOI`^V8cDG1j8BszH#KaI}T5$oo6*m5Xl5&PsLKWuK?>1`;z*&(#gla1ZKA6lZHozamJYr>>gz*(gwww5q8iJ5C2*Fs*U=9)YYVHkeWD<o-ehnc-#Y}qhVv*pd^jU7#zqikgr`)#01Zwu?+TL}TcJ^{cSY@i=CrE)sw{??43wgPAf7%E4ivi3VNwa$sMR*pnlaXD+PikeE6`GcQMc%Lv$lAL$isxk~7Eln6TFAP~A5}HqSO&YLT<@?$P09u$i6ktdSkWF+LFywKAM2rmZMC6m^bk^h|aQvcgnaszg)N(BIPiz^Q8<ZSybZZgD+LlsW!F}zS%>VSZj?{{Cf(=);0m+Qt<39`m#QT-AuaPMGkQI%uxCMPX<bWxZptAyNYs|aV#=IFE@<L@o3IVM)+2LQf($UkENIqFWVf;L^WA4<qTQ@gZwP0q`y4bayHVd4e&J_-?czgb|7~nLWZ!9HL)3LJY3sSahH^a1rjVFc5n5M!utz|502NhXUd;b;i(H%^Mak5-QY&|T3ad=DqE~0f6QA5S&EasLe5YP%*fOT*H_A2><aa&I9Q^^{2o<L7Wox>(95&f{o59O4hM_!c%k}!$Tp`2iI0gS8dGGdmaDzp56=D^s8#ETV7)09T3Kh`SoiX^d|(;K|mAQ;!x)M=H}Inp#c;2k@fn$VFHNvlFJ>YWwHB=n~V*0oufk7oiwg*-A!!5l3%zYp3680qlH-mLb6^A^B59SD1erky7XHD}fZ<)r@?^=-1Qq$;rP+AZbN(dfJhs!H~cTU2z=sk%ubB^8!rvkc&x_IKn)=7cf7D?17;M~52(up4mj5wjAPAmxRzPfFng6%Uz4>Vf2qANIE%P;Jm%m43snu)rN0|22!{;m*jwosM+eZNvo#2juMBy}0B(m&-kIG%g*BH(dVnz<#1EtoL=WBaG4`<)ldZku+9~tmkX(k04QG!yEDAm=$3qkA##6QUr)YtJ*Ql%SDZ9F@F#lSPl+bf)3(NZ0Kvxi8t27<|u$7Q2u2)38%^p=N=pEhp%*dXA-8e4e6<nE;c%+`HZT%omR`qk;#!~UY}qXlp0;7GdU{xWsKc;NBEC(DvG=yNfm-(=bWJ6altt=V!Du!yNzjSP@GBL)EVd1yq6(FI;Md*KW*01hx^(fvQ)`_8;sdP(4$k>{gR$j&%9!Mv*ik%fVWiB59bB8r@^iuK}}(o>hu7@Kxoi&;8EWtta~niopYTTWU^MHs?z+JsNlZh$PM=fGm;-^9-VRtSJSwa9=EcM*d(tmL&z*46&)*w_BJ=2PD{@Xg9|R1584U>_OfqtHHDkPTsQ;u&I+oU)x}2W?6xqAqy17nw^~?V_S+@P&xrfJke^NHF0y(g^M;L9O(3#Yg)PeTvg)!U;|cI?yR$JMvI?lWURQ`}IfMQdeN=(woHh3l>iKB@a1-V>zG|42544%>#@q4?BDk3FdZ2;heg#6yJ!&1-fD>U*;GK^-kQI(OHw8<16+)>>;I$DbYm2z=qo<Q&tlRq~X9T(<7zzq7i9iZ=B`8_Nq3WEWwO|=kdnY*A2GDA4nR5!-S&_y^?k5a=7D%p%fW!U?a%hl9bA$~j23Z*Eu+yn5R)~TjQ<b=N)1qe_i;DtFo=s{*P{kgB*GZ~v0q_e6mBF93;oC^=k&pwjgAQI{ZsWA#Rdb^2#>_-G$C%U6$p+SKRaABcI&?~2QQ3~l39Y3)j)MFlAd_|#X5k3N78$y%f@;}hklT4czFQn-bC_hwEm5uzTmnoHuYm7B;A`8JI+`p3uQ;!me9e;Fn0cK8Vc)q&XnTB6nYEZ#`{krTo^rCtHfFb?Y9@|LSdKdA<&|B1y$Nkes$c6lpOWplh?ZHI)hVI7BIizmSUMe11up_gGDLJDo_ybzP-&zU^OO_M{ze|;nY`PG#H;$s)@`*o45x6{IcV9%i#>U9EbCU)hSOVQGEd34RNWSs)WiI!(cOYZhFVrGyZ;zfO>UmfDV6PVAy8Mj4K$thk@g{I3V5J?kuQe{!h+kS;$;r#r<eeDT1S@d>xg0GRz+L^TVlZkz#{2y7o1#QV0%T*4z2w9VUHgwfa0St3d-!^iZa)k>6uziRj^oX%^^Jri|B!KlP&|BGbXjg#bD@Z3QRm%O94~Dfl1DmBQ-@<{RJ_8UygRok*f2gj*l_J&Y^zT<A=%&+q72HT>fO4vtlh$kgHYzIu>9V&SS`C1<qU2%?i#_C2bsT|0J?@P35u(pdzfY<3lK<BjS&iY*oAx1qCiSZdDfnLF_a6+2$sGF#;`1!Bj`lDsX%VrfMw;rWp0;kZnVlQRKQaAcx|NU@3(xQ~=qfJaEh)Ag4k{(8~3O2GDaoV$0)@CEyUsD)$Sb7H}!~giCuzydw^tKjQYRybq!Aj*k_(j#0G#YD+ncq&;s|0#3DC5g?&@3rO^@F;T*J%uYgC<4GL?qqfO%sSR6J9z~j7f59s=>(2M?%8!;oW|fJ5)4r*znu9^_`uB@>H=bl6HLW>zr~BccOcPX9?Y+7G_{1ywWv9qU=(nJu_sD1!$F>GVcVl!<WtuPyPeIsF+0nAwyR*R}&m_BxcZu^1W!y?U-l@;E;D2@Ld*9SP7D0giYGtZ-N&5|a*zUuTpM~S$G)U$_p010ONJrvj5n=r@i8;4G<!I9SU(~Wa50CGm;G<}z3B;CCR>kBtv82wR$RHhMibS1~4(QXiUw4A$aWOm+=D2d5Xk2-3i_EGI?|?d~(Xz;NWS=z+R$=fk%*JF0c_yPpE&oUwz=0NZ4hRZa9e$amL2;-^32;^(79c?kkT5@1S^97}isJ&>yh7*0F|u!YN43DLBfA+x24N^CmWFbgVu%quUI-fRKA!z~Em=}7iE{7b)y?l8y^ed*>ivCjbw0fL{o?E&m*>~l9=QRn<Hp(PALm!6*WOn%pDpL37%O+zI&hjt&VfsEZ{GW|AxWhqh6l*#LKze}S8VB$JXvs^781cwFd{|4B}JnLa_l+6x;X?H+G`nP|9;0C^usTj$S9K+Ss2ZdWsv7chCJDZu=aif+HXCX^zi!Z^usw#{Tmr~Z$6w~zCFJ(KK*`reU5|-bvACaSUV%oL{82jzO&46*h#(rE5NCY+Dmt|n&n^xRq4%Nzu(YfgF17QMdl`>&(zG#0;F3HnS&+XVP2nqI6u1~{aLFz31G)t%Pbg9qh#bqD#eGTeh$9oEH1Q~__^=uwB^k1ZkM@fFei`9nv;tSQ`AEhWQ39@>~cwuKV9U}4N0J3OJ{Dj&hlXHnSY$$TwR=*yX%nI7z`y`<F%!G8V<&TD@RQ{^Xy+|gm&G2ydINMaWfyTO6C!@YA=Fd;<b+(8->7wKk*lNxC(~cltven^tLKaf;iz!2dTg)TSe^Vaa9)c$X^F()?G!<wNx{vH*qo{V5<YFN#Z5kt|SZdI!vkxw1hv&hB$WQneQ(CdH&YiS;ITnL|};HLnW^HP$o{*`D7V=x_n>jq*fb8p;9&G)%!Q6wc6C#e8_t;a<Ws+`23%rh#$}2l70~KnO#jk5;CEg*(IVmrlyD4<))4)h*U@{i%WEuuloFMKy4K22vkOK*;$FxqO6KYf=e)26r0_HZ;}|6#JAzp;*2KI@8x86Flc37yEwEu(eLx*HWr>{&nHl`+F6;GuGLN^-igK<>(&tZ91GX+{3I_|Fu$vg5M#RZ(+SaH>}j&-6@Tn`n%kVQP7ohAh`Tc#(3iYEFtWoZ=xDKocSlH2r$LCsb8m;ji-QM_LEF8#I|*-ZWs1~~$DdSM3N_Zz-ol%^cpO5F^S8{Ml4WClO2c>@5+h8EH`j09k)~d_9RAGu<{O`!wKH^R4oG9)`pYOEvZ14fDXU%q{5Z(6t(rWsO3gno#V8zaRphx>DxOA*nZH%5?N+LA5Op4siB0y#-vL6BTMb&(2Iso+HQ@m|eOGl*Nc%>#q*ND^1+Di1wS>h7b%lfHkR*~2#B#CZwHgS!l|+*TPe_J*5cUml`kOPVs*yE0@vRPgJ8YF|<zF0RD!RkTT?->&8!yTGCb%vih7+=k`4GD*W=mpN>_E_4v-vMmy;LUHD$JIC#8wx*XMU0Q%Ce?;EMak*5A`^NvK1u=I_b%2Y54u@&x;XRb42-oFi}7pe+`L<))08cQA-*OmjJkv<$RG@O2(XwY>(kxu+EfiNSd8xsW)2lh71`#g;Xi;MIFO}90e6YVuQCTMS%;8XSi77y|v-SIQ@Y`1$=<Y9B|#`VuGNS-Ai`UnIV{emwX9zpe`QpfQE)KB54P3+zS~^a{-I9deNV}gdIin^rP_*Pz`bFkF<g{nyX`8Vmnb|pPfAPL&kNb7wR?u{E~3P_7=FlOLHrgOeq2?`SW%&rbm^LlQ>P{40(yV;SiyfM{g?ng#j%3G@U-7Qa_T5_yRsbwIiE+n}(6}MW4rnnj!Lvi6N+=eCsjYHF$(XA-_8KmI$;AYo%iX5Gpa76P{<v7^q5ix!#o2EnUP`uLOs<cznlf2VI)s6tL_p4$JzA6BBj>0d4nr+9u3HROnCmd>sO;fg92~<j3JHPOYOm4yRE&K4EC%&?EKeG9SqKKPwBTq)bFSDrA=Kr6zLEOGxSEB$)D;xl5erzb=ns;ShwOnr^nT3vU$wdo7l80--$Eh)%thLla|JplUdx=umM5t$XYdJ~cue<C@@K&6qtd)wNl)F}qK92M-FUQHUDO_suQ<GUFuHI36-y%`Sj72~rYW@cFPZ0F{0t(3tRj0bt-MZ^(T|<ou-A&7!x&=4tpid`Qx0@?T{2B&Cg`fYeHcbc}>?@}kK84haSht)dl<6OCxpIk6v3tPN=Gf!9}q$+6$DjKuqHRt@MHm?WAs3)?Oav6S!*z6UQ`OZst0e(-P>=9yJga2C!4dK#tMhir;!$mt5&o<2m?3p)HA#{_#bbtG!y1Rd~o?%_~!&~|1>BU4ALsMvnJbzCuwS6=%iz3XKecep@@OYR`csDl?&qj#?cppu}C!$f#Jaqi`<8m^<BWyqyE;izO}<7v6KdhNCM$^!a!{5pT#X?1~x;+$a_$U(83tq5bp0GPH8hnj%9UyW1AaRBa1oJqj_(>kBwE)P)s=zz*%PN6@&d@FIDCeZ}SD$Lg|x_XPf?lJH0z*3nsIoTc%7`Ph-w~6rb@26`?N}%3c<4>}U(%dJKjmdh<B&W-5l)!jTv8YXo-Fu2NWs1FI9!!0*(OS>32bX$sQ^10(24)rYWlUdsk?-v|SKo_9wc-&D`uC!7t$2(Rr8ExtE?(rnh(<4>@t(drK!3-X$rq8oCk=f1KB6WJ|DM;81RIi)xT63N#^S@Oq$OkQ)_7o7Zt>DOc%cq75kO3%Fes&@u<j%^vW;6F+SnV$4GnJRXy0jLubZC^+PFkwA159;Ka$1md9mcvhs78b05pR_?IKJnw+ZCVNkw^~H{1TtjwHGB8OLUu1@KTVanY0U`p9Nz4|L8y6dJdA*jX8IxmHnG)^lU$X<o}Lc~UbylBxW4Q@9;z2mX{e5II4n^Wf-VlwcwA1j05X>wm%$G0cMKHV?9zC%16)jt~u1z3Zb4E?2}h6N7~qlIJD|nz!Dn9)Z3mfhbo-F)z)otc<D!r&$b12e5zE1!BoHPs*~P8boSJ4O-?JyrYp-52TcVZw}HU0+BqFjL5Ic;5Ybd;Ymc%QW8v_zfWG<nEbskRx|Yn<V?krVN9=RKGwqS?++Y#H`?{C@Ub@#<`=l!C>|BX#n`_gR@`<h^CBj%FPz9pHPb1k=oD2U=$K=PV_q7ETx~cfn<HeX9Fyh~&X@Bcr#*!UIWxKsR4X1}KL}#WE`77>JLZT?4-ic?N4i(!FJvU58=&~c`}Vk1=}p8QlaU2eNlRoKNhdOqdlTWr!1g9<h8v{FcN-(QHt;itI#jiQGj-byvWFCN1meXZsVqgt98#MXDZ^i$+zaLllA}>FA*rDbi)*Nw*)qkb#N9E?HOQ-b1G0{Q?>RS&#vZNZ%BTpQ`~&;*EI7H#YhLMiRt#8X^)JqHfd!EKv5GHHT(j`JX#zG~t-St^7(Y8rpWZn2tknwVl<BiIuw8Wl$_f|3NRe0r*wldzT)1DFUqnmFhTMu&qDy-2NEkJBzr0v3ert6r*A09vd{XdJpZRWOmp0{UHE>MObU5!2zoo83tzUM&mG%SfC-~KPC-e>;!3D`;p;!hNVlhYgYKfnw{$eKgnK)3AWGszUKAB?9ObCPXX+sPxci}V)xg2NXGMyba-Za#;61+m=+&*7}BMUap_VXjobdPFhx<{P2jRSsM?kf*<;oR$U;k0z~x$qI63kQYC!1vIkCkF!uLJ)8tz3J*pA<zvOce)#T<<Nib3V(HH#w7C;;P=|Jpyk4b)w%T|;1^lwO)`DmMK7SIKtHMLGP3YLyddlXK23A%ab|o}UpgX3W|F<MCRvk~1e>i8w5+uXN`iyg;N0meI6`&xhUDZHM;r%s{a||Kwi0X-;|PK-`K==-sap+p?v*+z)(JiauCK#VybvWgq0S;|+$;M!t?u0F8#LG&y2raE6*|S!YU2s#_Dy8Ua_3;!x<Y`rCuC<8(A!iDiqOxi1Ol`#aEnp;Kk$tdnF{HLTA*nxB0mmz_N6AcuPFj{H^5DhkNZMC?jaxiXybM%Om|aT-1EX!O1<IxUJX$|q&Xl%us0g*csHVVWU4iIo!|&TDdzn}zuOs<P}9;|FB+*?`TXAJ?|h5GXjFy|(AjSu4W<{*g`baSL#@RIj+Hui&;ri<Nr;mrkqy{M@(?SIf}9lG0X`|#Qd)0D!BCR>7~$mGEj-Cc_?cGlE_PTRg2{mcSaw(-g3JNdsNJTXZvR|`Q87Tn*pR!8#B@TJxK~Q87bMlyHEumdD;atI<g@oxf&*O`@j|sSawU;0z70Ukmc5P9yVSn_S>Shp(9aAiS!hx|s+3b5yO9OtHen#7Albb<nIxjc@xpG%^+hOErvcfiL1!rAJACXx6Lq`z;I3ooMk9iHDN;FTEFMgxpAU+~Dv^QKJc$FFPNhauz|hGKRr?-*0BBr80XFrXwnuQ%oKT<z2jO|m(xv9%PRc9BAPTTck$0x<kpYQ%8kBncOKkjN!N-@4U>J8#YyT)ogEDAYs%XBQPy#Mq!DYY*C<aH69QfQ)*88TicFNMq&Vmi$(I*?|kym&%I~oM{T4GZJW;Zz+eCH_+qQM^<V{Q}ENpX6qgm*V<hpP2ZwPvrC?Q4mG*^Mcg%{ykyX+$&tY4tlYBs^XWjKY1(C6W-7x3{r{peUb8JX@XBFvUF)an1i-=;EtCN%n!J5_c%kFcb1rh(}#FT0x@J0TvxyozPk0VmCICGd|RJmktZu6g}9DIg)pV!HU!o`)#`utF#XJxxi;#+3@8FPxVmNd%DA3lz4reBvmo6w+x(pd(fMOR9EF$eXp);b$NXWa?C<%(u@)qRIhf`Z&dQW_@*k3c^nJBXd!*=9g@7utw^KPn)3}eKfY6|hFDbDW`k>R0bA_m>qX#ZIq-%+pk>~i|8r>CrFPvKki6N;1WwvGm@IJ{2&RYh3j=#4OZM6(NEQ#$d6<(Znp?wWV4oaY7})BPvo(ekG8NU9tc;|pRAwk|HwKUlyTYH-a=Ech?UdWgPGwKpQJcw*dGYazKCc(Sm=B22qw#^fiiiq#Z6-VBS>orlr)s~~Gn_jp-WU7J8k`*)&g^dTUURW8%|_|wMzpR}NUbahJFo3LvdbGGxe+U_nV<Q2o?2Yum_uYS4MBIg2C348v~l<}aeY*Ck}OHf3^_PpI(+{v@1!A%O)LRYAf$fEOYj6n=||m+7L1d0l38l^)2_#jSg_SgHrk)tuUci^&*_*Sw)VG?J1&sRVdfRg{HIO)YMh9ZJ=LA5{ZMWc4F@|kh3!D}lUjyHKd<el4(!U!l^L5a7RDn}C0V9K28Cl!<C^s(Sr78|cHyZD_1$ddcMgxN%KrLh501*=OlTFbh=m=qYudI;x}Rj;qHnX{aS~1ujH9(-GrLm_`u)7Xx92)Du(naU*T+uypquDcu+3z1>xu1Jy`_$>SAlG#YXBr_HI!}mX_VhuI%~tjQGkzs-n=yVwrqMiGHplI*GXvaKfEy=-Zl=@20mLDy4sq2i0U(uK3dD(a#5tOl+HHGaY3Z7ckNVuLxHx3xulf%*#8Y<fV=~4p_)5FAdm>uxc9xUk_BRRIRnHoM-n77IcJifb5)YckUEh}sM1_4BmQQ&UC%qJ$P7Sy6QowiHoGO^X&7D_5tWi}WeFQV-6$zb{700`LZ@MrTl~~teYY10U2^P+z%4y86$=$lgsfk(UBrkVs_JlglA%g2=_)~Cn;s*|rSNd<76QE4Z5MI!GP15rqawg=cApNuJEnwB3y*8VJu<r+kB+%%H4z>+j4PUvcHauqmij1dxS~Q~1jAg$rgdpGW1<Qs!Gn0!oHeI>2}eb-$w(!XSKUN52W7{A^wLn21rVv!2s&3FkjND8YszIyvRtIh4M*!7DttqQIONW#6vGt(QYHf3hEtlkO8o)taz9_v9899#WI4v2D+-G$BYp1Q;gSn}o0Hv}vxUMNKBgq=VTgO*vbzG`z28g&;KPM7Bp@GBAPowpsvhrs2P&9UT*uxs|95Qa0|vRz*+P78O{mg7Si#HXi`qc3OrXHoP&AgvCX!A!#F$>FyaP5LbPj^MSo1r<4(Eib<aT#Kvy-j7g@;+mebYL&xp4XS0gwVEYX=rXz}g3l1JW2!D#WFtIkK0PUp{&HmDR|%m#eSpr%b-R{EF_s0qpP#`JfBfl|)4PGeilM?`DX_(+og3n-Cn>cv5OhX(_X-h9zA<IG84o7hn;l8-c(O|09H)gC`b@mH@7C_4iu<Yrc+9`rxN?{QAOVocbiZljbUnBC=}HFw9Yff1(A+ANa|P1^a2;$}g{g4MmZeUG}07Bkr4z)WMqme=!G+ytaAM)HCNqwVzV5OdBFc$aM;qm$Mr*1X;F0j5J!ZXmQ~knVlI~1!Q`Y@DP_9O7awMKF`>bEx!KMI49)ujrVgudPy#Iv^Iq4;AAAXd}>%-q##QfUo;Q}#jjpq11Z6;#$Zn<#Kr<IzW*=I3g~(=^bfD{c26Y^R=i4St5!D%Pr`1KhtmPqzng_SR~k8<S1y6<)omJHo>#M~%y&elnL#Fnp|x(Qz+TD)hH@bO)0-=U+=e-nwn@u6k~lF`MeVX$G$Fo)2G@O&$uX&Gap_9!{FYz~=Lx*udRjR)X!d5a87EDpZ5TgmGO*I=3Z5Xn)PprSXS7;@GcC1Z?D0mSWxhZEh(i|t8eW~BzWtZ!h@6+gpoFG}PDo$nRtv27=KTG|rE&V_&F>$tF8=%ct#Na4eno$-<YdcV?Vce^2V5P)kDy`J#t04>uO)_`w>u}YLq(jJ4hcT8>;0*tJgws77tI*uD(+g&MIWD%>Qv9uuUt0DxwmpNdaunl`Rh7`L!=A%R}dPQ#qiVB$9ESW&b<OILaLy<Szb2IHBUc$`1m&;SdbgZo2$0jwc1BcpZ@Q6oTGz*E!po;@F*{-w6ETLlTNNLF5lNi!}q4xLrqpLYP=5@*Ef=Ui!)uBwbcfdn~2zwI_eK#d2+jtq^z$lNLfDHSPmUDv3;0^NaT0SuiuJ3u5V5+-=1E*_4<|5Ta_bQ<w>pLgjRVnt9Bx506wnbx=g~TmV(|@JhLc+!;v2%++E{}%^IU9yeB_*chxfOgAk4L@#DbSM3#ePMD1?e@%8t{W`!byS@pzM=BPt%49VSpcok$xe2Fv{wuVDwYKU@L)#ur-B4N;P51xb-4B>#@66^$r7v-epbn;JGR_tMvWn5C>M0?}7V_X2I82}ru(o1!^MZl^Yi)FXcakolhDXJr^`byEOzj<VD^PJujhx2xy$s;sEVT0ETW0v)_lIkJn*HlnXW(;3?tA6}xSR62*CH@-MDaJuGyzShM$45u)_F-^x(tg!GnY22iaXavjPg<`I_Yv$WjOgkSCjNQ5rI<1Oqk|Tygw{Z2M=l^NpRSomfQ?MEp@xK>v=S-~58*wB0L|{#Z{JFts@8ERh0NklrBH#|4e`^zx`8@dWYY(ks%463{Yu&3TiFuyFWSXL?Rc<*PrhxQ?qx7vdj;ESwyXR$2t!%SaunRcze1^;7<hJ$4Wn}UPwydk8)C{axSFIR%F98%XXKPKN%U0IAm159Rr>)2u=4<;`r9z{VWxg@o@`LQ+`;tyZPpoZq;t<?r=@I7R_Ep0=N9_SV}m7E4<9|^=-yLr*U!FP1S!s~5L{ln)lx&STU<XpRee>9lq32)zEk0bL2=G#_n|4v#Wi~Bf7@>Se7{c~TXOX&Q#s?U4@vS9pMr!%@0q95f0~WkWW3CDS{|RT7852P^4YYn^Ie-Q^Gfuza9u<X_~G12oJB&CpSZ}FU~`_Hdx@)m_H7s}qagJx9=lmqvvDv5M}F>x_e=65&E|iT&iR+g<=n=yD+!hfax!tB4V+EoT>m3j<64D%9F;z@oud{X*tX1f<lLF~RgY!|1^Y)WXW!+YJi7|#CVtxEz@f*36Dns1y5@Fp650^^%j^l5r)0dEPIZ3z{ErSwO2eLPgn8yCb>iOK!?Qkw0gryV_IMh)jGSbQ@b=>RA7)WTGxYG$EAd-*qQ*Xs;xLSMj~;eGL&Y_C&bXDyZ+Iw~AD^tRl#)v|ONM*^+T(ZnG!r-X=uZI-A8R37pOz9VLXy|Qxl5P?uDC1E#s}(gcWG;%95MCt4m-e>H#NvrIE&QoPy(He=~Jg8i#8d;WaLy%YX>DQx5GCG;X)SVz^DOhU8!jPRQ*6)=uhJ$!<o4(_7~ZVY@F&b+<CWeg^u3(f@_VR7)*7^D5B-RvW=sPHzavu>t<Jlt(~0Ry{K!LiVe5Qv8^B6Uer5u+W;XzQW?y&2c?QA70I_oqJBGgSlP-zm)=f1mesQ;fgVb_7AJ<(wT|ud>!;1iBVVerKK3=(PG^w~sVv8WUIC=&-qQC_&mFZ3iEf{mO67pzPwd?4A2S2!&K92xA&(BDR&Ha)K=MmnI`@d$v8!3xMtxgMrQBu(W{})YOpFs8Ci;+<<=&(0E>(KpVqecIzq18hXJ^DZO2BtP!tL|*OH{z6I`MP^n%ZKfHb9whj>X)7NR=FmsuF`=RY_2Z($pA1c`CY_4JbK7Spqo~*y?QOa*BziiO1Z|0CbZlw8mW5y>)~ZI;(UOv|?`ChbZ~8GOwNDK<Eb;Oq!pN49`>J76#=`vGlyBcz+Xz62Ag9n>_H#l4+RiFNL8+@+1o!3K>6bS^)695L#utYCno-<@JDD0k)U5@EY<ZeU1)`=~|gNXGISy-Lw0Kz}hX4KwiFzqp27hGd|CFSk9OwLAZG{_{JMn8jVagiPvG1NReZ+0gtjf$cM<DLQS>Jw+8$>Z!?CmBZRjjd{GTu&?w^MpklYm^redL{^VNn?3DtR`W*oNkGxa%!Mv|`g==>=D1Rf;de&zjXuxHO{C9+tY;ipaa|^L7cEmmv#MP^ZxTre*py-G9fH|C&?dXP69jkD2uu@~?Dc_r%IN}H-Dt-OdlT9@K3MN-uYf7jp(PUwsf%jafSyHW~3rid0taEoe$n@fAOA;E5j9RL|z4X3w5Sx$Sh#vv7v*uL5Q-JRfq%oC|A<VlXp04y?%F(gfI58%PzgzF*T4uYqP$!=LM;U03k6wS}B3Ydwv5T7eO0e}>S6D8#-YUdtgL%*6PF_et$>XEk=0<<*mz`#{Vr4*kZ@Ewn)@x}%e|I)m;%LH7LZOu!s;P!{R8LLSv;Cs&whsy5`pr9=doNbS>BnfomFl>@&VBfy6+p*aO37yb+{j5D=7EckN*YDs@-xrM78t4cC{pL+m82*@)ZxXlpJq;eVVP?NPURdR7S4*z0Ue?9B5>4zpCu`QALpLr<r$(;jY_Cy^9nJ%GalyO^=Qz99GZvumPdnMouLo>P&e-C=Hns8)<p#PHz6rVh^rTC+yJm#@PMAqyOQGPFR!3R(sI*9<Jp^g;sf`pxGB<4(XfJ~O1ZiPL4Vt}y>`9Qw}j4Rx~0KW)UDhBQM0dF(&WKI-FY(M#k+=Xr3>Y90LR3wbMLNbMFI(2{;ezI0(zUb(a|dqCJo3J9tRRelA>Tm&YQZcS}xOiaMfd*lgMf+mN)F#@L<yYYMhdOAd=8x>|<{h%QvT78gi5oFw+tb&NnLdk{sAtXGV-eRQLh4JL!(MYq6_)o8b4lkVq^uZfacVE_qY;aUAfzI7=$;6=RbcC%gsogh+!A+LnaxZrzch?rWpE&LkNwV=$Dy!9W=r*elij2%iY&;usC04TQ=x!%t?_FLlv(!O@dG9`!J<X2{Cv#QCls>KDo}Piafy$G3d|>4@ll_x<2Rv4wzbZ#1dL9^>4T^1{%fB4ul7p}-lZqLBN)p83Q8msId^nUm%9hrV$IzuWj^U7f7TwZ0e2<OA3UoWwaR1nG_1B|IX2EgXlJ%h08q1T_cRDXQtDr`)aHQ{EM$rC^v{F3xUwSAm`x^0`FV{>@QdKF1Es{2SxD?P8UEKEQj8OSoaM^_~uymsb+*3YpVeMWE`c*B6CUY_jlGBDFm1pV=nE$^Dw1E4AG7(V51*uPwu`g-t6<x!F};9CIU&jPncmi(>{jwo0y4(PVq!zrH!Wy1|b=*AsAbj+sh;S%i<cg*#RmFh~h(atdCVcE;Hh+GOdLnGp@0ZJ|>nI3;3u_VJHTAI@*ipG=Wx{2wBnNW1', 'offset': (1.0625, -0.1875, 0.0625), 'rotation_quarter_turns': 0, 'seat': 'WholeChamferedEquipmentCourtFloor'}]

floor='WholeChamferedEquipmentCourtFloor';plate(floor,[(-2.260,-1.650),(2.010,-1.650),(2.150,-1.510),(2.150,1.510),(2.010,1.650),(-2.260,1.650),(-2.400,1.510),(-2.400,-1.510)],0,.080,'z',0,'Whole broad common equipment court; open preparation arrangement, not working access proof');FEET=[floor]
for j,(x0,x1)in enumerate([(-2.250,-.400),(.050,2.000)]):
 edge='WholeShortRearBoundary'+str(j);box(edge,(x0,1.535,.065),(x1,1.605,.210),1,'Whole short rear boundary outside entire accepted original envelopes');LINKS.append((edge,floor,[((x0+x1)/2,1.570,.072)]))
edge='WholeLeftRearReturnBoundary';box(edge,(-2.355,.785,.065),(-2.285,1.550,.210),2,'Whole short left rear edge return, not fence or machine guard');LINKS.append((edge,floor,[(-2.320,1.120,.072)]))
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
 return dict(review_scope='basic whole meshes finite bounds and common floor support; no access, loading or operating proof',mesh_count=len(vertices),static_two_reused_diggers_one_equipment_court=True)
FOCUS=(0,0,1.0);ORTHO=5.70;WIRE_THICKNESS=.0007
CAMERAS={'thumbnail':(6,-8,6.4),'qa-front':(0,-5,2),'qa-side':(5,0,2),'qa-top':(0,0,5),'qa-back':(0,5,2),'qa-wireframe':(6,-8,6.4),'gray-front3q':(6,-8,6.4),'gray-back3q':(-6,8,6.4),'silhouette-128-front':(0,-5,2),'silhouette-128-side':(5,0,2)};CAMERA_SCALES={}
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
root=bpy.data.objects.new('OneWholeVerticalAugerAndRodGridDiggerEquipmentCourt',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='whole horizontal bounds centre; common floor supports two entire accepted diggers';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
