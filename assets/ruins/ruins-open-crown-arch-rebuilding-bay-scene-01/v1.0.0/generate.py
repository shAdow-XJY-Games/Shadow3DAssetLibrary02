import math,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ASSET='ruins-open-crown-arch-rebuilding-bay-scene-01'
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

import ast,zlib,base64
OLD=ast.literal_eval(zlib.decompress(base64.b85decode('c-rkf%Z_EYalbM<C%|yP_anPRhO)^bumgBu1cD@YEFtoYF&f2-Apf3v@o~F(P9HXV6s6UphH%NtdKZgD9-g}Y{hNRM`0aOJe)#y8ufF>7<A?X3{_x$0AMXD7<A<N#|LOPe={NuI=8u2;J7wOPRPdiq!KY$ueEUY}civHFNzsICynXvdzteyJ_RS%H)%?$vtgW-wH;Cr~SY~MkV2t!RlTy*8ED~ISpGr7Ip!P8Q`&%%je*4C}ePi)6d<144eguf{_Dz(JfHlbg2VclX7~t_EfF~JiXlzC1I~WWw_|XxGC?6vtlM#>n;V6(Spd_CDuOouq_tt;8`;Slm`r*e<;->mt2_B`+&KVs`38Wxb0_w-;WOH^=$72;AV6dJrXrE$s2@HLPA!{BC<7^1YKNE(1DW(__yHqkRmy~o^W?==vR0{_Pt{dV3f|uy(zx)2r-wnRL?IhcNx;<64XX~z)?oN{}A6+!TufoTF|JRS-zyCA*eev<bk3W8M_w`?T{t-z27^5|?;_}j~*(sv8E<rcxiN_V~qq8CAx^Pawt>bmmn*_^dIEMc$;G4|Pz_XJ%k`nlEbZf+~Lr*22fvX+(7v|u<yZid%_2l|2^F07K%zU3^_%b`!^V-h?e>pE#JMb^iNiXEoi|OnP!BRH+aG87t1luC4B(s+pSb$&2#xI-TrRN#w;TKZrwLEsuKX)g{?hM`Z&dtfO<C|;B|24SwN(Q}<!p_03rm)Wsyvg|G1oksPUroK$)1hCOUt>b@+q=Jh`tIMpzw1fKgY=BHHT*A>2u{H0oP<1^ee&MMx*$%{y9MxkuX`JOm-_>F&+s|s981b3tTJ#N!5aKk{Xc|%X;B-Kkz4oP^p8F7+?yJk6LZ%wcW1_qUoL6>#k+NXnE1s{AOGv_Prv*Ao95iN8a90Bn!@oisx9PlF(z#-<ZU{42>8z1TpXw|#Au=wGh`STfdb@yCgyMhU;@y!L7SqJ^KyisnQ$~YIBk=AjHv@LY~)-v#Nu;?gmh7;3H(&V1BNe?KTy$}{6t|eQKHTcoE(xA>mkn`RSdaF!LhL*dY^=%GroYbAm5KxyEsCa>;aQOoj~S(N@L370>vr(oPGvO7Sv}9TF9i4V~;y1r(FoZn6`!?lF!cC2$m`a2Hrq82n5Di_)Zs)$)3=d^0+{83O}cxTma%aYtW$2(Tp62MBfEaje}_B86vvqK+OhJm9o2?jj-KwWHnHI%ISo}l*I*ta}~|VheUddCOHS&(i?u0ChY?*@8K%}(4;6(t24&yTa{!|w<|sdKzBl6%HVZ+bN$SyyF$Jnoyp1T>~Er7);NVCY>a_BlZ7HE7gVfEhRBj^yqUZ);iQSy!ko*xPNg}KDU%B%r|@$Iz~dnZ7Mo&mF5XP695Iq6nBY3ZU}W-|L}3eNg#qJ0oW8NUrRZ0Dav3m&V;XZ27bwpCU_w8>b1@sxu=eC7=1$#)oXiIpC4iqq$S@Enyo0EPQ%0k@wbAZARFeFo1Q5xy(;SnUi@Qd6F7bp7wQN@P1iPwD!>Vn|swYfRwLVML_B2(y^HeQ|TeTc-)n>p|n-N#7FPdt3)l|F7rrKOL)q47)*7F~=n*gcZ3`nh~vT8k-RlCWo+RbLw@-|AX@1xY_wnpvlOVs*KPOa}q)$aC7ZEYVXM+Hu{^tVR^sh<xdIUnF-g(Q3a&`$!QjD>H(W<@>%iHsld$Uw^o{A{pY#~48fp9?nS@Bsm`d=7Oy4nP<ujf`y?gb=<CqZR`B3KS}4Y@oQrOBNto8@j^K7!b;&)<U{`GJ?o*8;LE%n%l@y@ly*0CWR1&+^|?7&TufwqIOMfA$7~r06uHmNNnNRi*0bOQNR}3mGnaxY{L?nI>XT@pl(BJA$5|7u*WtMTZlKdk*QLkR=^%=X@T>tWg8rhLh7ZpkUB|(_?&Jdv1PEQj&!C`K)8ZE)bawCYYV9h9FD>hFjreh-H}9u-Pe)SLMpz&g+>8e4tuDT1<tmXu5dI8si)RL>U=te_;MSGEySDK$Wkd#3*{#*5r*8bSfS2vI3w{~&eRrC_bd_M^R|t|mcyO~=NbiU8SJ4}WH`YRnL5MKD4^~`Yaw-#h_J^t5?hEjwvnk)pcbArl9mWVY*@5VXE+>%)Jtn2b&?421>Hts3uA<?BZFxa5UyYkwY<RP+Cu6AhogXcaJ7Zh14%^KeH}?Hq~aS~XcVx8fswV81<tmXu5dI8si)RL>Ld~2%WWjK5N~cHOQk?9l%KRj7;?j6g*wCGu`W=LrnZoJWQhP@v~47|FrwQA=NbiU;lVIzi7?oPB{Fq}qfvO=99j#hlSG6)wvpIEys?c;l>)VJMItQ`hS;!Zp&n&nigMn~r`3!t2t;ZvPY`vDdHwq({4HH#|MKhif4FN;1B^AX6a%}s<RK5Vl4C|XEHK{b06R2E#UkX3uvf+GUq>qk*`~nWMrYi)z%I?!J;xLQ?1f^sC3@I3mLMmnu|UG@BT$D8Q>+`-hw!igi2+kJ*h&SHe26FTHuG_ZF~#bF%g_<{od1XLN9@lPIEA0;4-(LnY|(%>1b?hP*k<C*hv0L7U1p5=1bim_edzmHtfN_9bI>S{nF6J*PNut)v4+Mv8CxHCSsK8Rf>KT`ABQ~Hi?`NCX4m4#Rsa6t?)|5accX&?l=k`d!pMn(P9N3$d<e|Dbh`sNMKH7S9{k~M=`$g?tOB*AgO}*)cq`|gqi;rHwY?aq&1j}J!r7SsSA((IT@BRkYNmFUvlr&(?Tw8KHyAdb{9ivIn;noXoR7^8uGX#%OhjM2yK#2rIOp&D9>zo;Cr6aCgV@bW1xt4dX4Dt2O+0dI;^Be%=7oZ#`vf!Ui&rKdxiRtZxya^if|bhzGvbT4CC)EPJbbjZca>n}Cc%vM+C_=;dlHkUlbd%4maY&?$uHiMc;uSIg9pvK7YG)fGEb?mUXeI`l74V);2CZWEL<8mWa0_8Bu+0$s6BJ4U3;okgQ|6ls@+McHfN<;pO$KQUaGyYs`lclS`DmfHL|MBMN#doifVaTRIBTv+DvQIW?rL~6C1Uh*{IFbRBh&_YB@Po%h{>g+x@7`?T=dBkErGSh1%R=sm<-BTHZpbwO!ro?St3b2d}peUT+_~-adG}eeinw;PvnS#qEPu_T$mZ2P==xCl6~@p4>lt(z0@IU<SQ#YhlX!!mWv^>K3kTJbci0`8nGh_|ikZ7x;+k>Yan@kIR29@P*p~ySEh<u1l!Th2W|J)RqQbpod?(YOwT_d@Jy)t>~pT!q*A&E0-kpV!zs3xzx_m^}@WHt{42%*B?LL{eT_6z5Dh**~JfDF!8J;Jfs8FXq!%+yQiF^%b}PAT9$hx6L=U2E?A1!-Z|*9C)Ek&;IpUrMv6DO>_LFM%>3j8YfJVO(I4=>MtgF;cwKJ*YGVp6YdmwzCswmj!+cB-0-VuKyOW9ubNI=5?u`B>`333#Zak<WWS>&X?u2;{A;Mw=O%S|vKB=TI2cKR<ctCxR_!4a-2@x)*gudfXrdu>LQX5$9ORgE$^j*;@{QQ=}L;9QKm#9ZW8Vw122WtQxbDsj*2;zbXuq3&Y@(XkD*)4{L)c1(5(Ds(55p;tqN&W9BG$eR1F@3NWqmDi;{V+!`z2NYG{x10?>egWRbs_2yY$zu)wit})5NI7h_~ef3HO$FRuRlB_zejz6c*H4#+Q`M4>}@ZeFlT_TCxm3J1{TgsILw)t+=@70Vw;Br7Syg2s7)_Wn{J@?{6KAn0JR+h)Lsx!yHP-GhJUpg|JB|Cp!QY(wY&7I-L+qBF8*qB^;dgopW4m))K=oBHZwo9oARsOoL_Aw{c1DoSDRZ^wYgVSd)q~|x8qZrTV=I-P@wkqyJ}~z{(6(-^(M*dO_JA}B(FC~UT>28ns1U=TFYMl{_p<|AKBnDnh$^b>Z@-*y#Mjj$Dh9a^!<nT>TloO-Tm+leWSGL&)zxtu^#qC#isTOZt?~8$dD<*-p|OTVAu&d$crEW^^g_I<7@ue2iRm}19_=`3_O+qNp&dh7CbuqNfeh3!A%H|g#njI8$bM3P~{)rlZh_byoRB1kn#RIs6lGDTi_LPLD(!5TYo<cpIYOkYU3@Q9<<*#5EgX7eFfy?Wf4WkAX#l<4EQ`XfVP8+QHSjMkC-*Ci^o$O9Zc~9NcO%Y*d964KpG7LD#GWpMT*r$M=asRaOmdWp1DUPYwbW7e?I=mmGIOK_9=K05wrXV2<yQbo54CDwYepD>r9ss9CA=>&|nG=d3-kfmJvHcFd6noV4;2&V#>i)1V`>TLm=~^6bIYvY+|~{!Oe`gjNr%{S&2S??^}SEhwvG8&=&X)wjFOwr^7YqL$4H{u?D6C%zxgrfk3diPEHpeLVIs!J`-k6H$yOY+1WfgCx3sET*YwUKO73^H>N;`Df+HI<ADx@!(i{lvs)Kl!GI<q9asY_=*Z4;`^uo<c`GAJ&e?i=5pNxZ3v!Xd7Y*UIVUXXnig>33Z-snL498+jew7hVv=A@71Op~=&xPVhjv0pO4~{(ph9!d@h`|`}<P*>T+?hG{F&rr30K?oZ7cjV+TR*wPbyY5)II!mw!;()eU^w)MsXb@6s-6SIp=ZzB@-tyr5@T-A^|`R_x$84l9`J6)%k7xGy=?3+UHda*dv<OIi2We79jv$4i|tUoy;|(An%gV)cJi>F!0gAz?HIkiOzbaJ%i;I=qVEZX^)*EHBH_WcZ;Nkr)3Jt!t-lVnz{(>4uy=?)f`BI81Ax6&vH0}Z;xlI2?v}(5_;!4P{n34<jzE&u8MaTwn_C+ECcy0vmgfjt$zotHQ(VaQK8<4#*#Gi&^Ogo*;ko&#UXxjJ*hYD6gH88n9D;xxmX43&J!KW*Di*LIK9s*A$T7%VkcekG8lQQW9IgDg^0`5dK@JQO`L|kwPw20QPNE(KIC8@oN8l_(0wSA5GLOr^5J|%X1uE%LQ{XuQFypOt9u^AsxFrN4B;x`WgLu@XtY<yh>@ZyD__#|k2uKk@O?W};(Yf)69LEp`a!lsyxiO9*Zj3=U)C>f>?C__Jeabcoi-0pk3!_bvoW?*(2XNK{POxx0gR*#Z>F}JG<f70R3!QsJ3yc&=0;Bf{Ik5CQ*`_Ilj-Nmkz*jcLFnCM>^n<s4QsG0y18|7GFgr5Hm=j*2sr<t#0BdkD;4YSb-}sP!J6^HTa+;eE7<FrH3{sQ_9Ka@r_e+4M#(xG4K_JMmYyd4{HG6!o#3u|}i6u&b&ZF>c7vHZ3S@c0zKLg(HidA@+zurWr@!}v~8N*^Ocnc2ZRlt{X8tb6jl3@D6nkvU<D0eErYIY`gwmc{U%cNvqymMu+8>k2nm;mfXv0KS_;_W=HbgcM<3p6ZnpfrfCaj+X07$gM~d&_s5Kt7NVZ3aOu@bYyGA5mq%X2G0*er8+axuGrS2-as>fn$Wl5Hy1SfKu+<M~F2Z%nmg9W@W;QLmndp-nkK5%)!BC)<6zg5*QSseylT-3}++0^d_^PmFK|2@t5rzeV8>7%nru01_m>)g}nxJXK?16na)K#vV~}Z$A*bDmC1H6HsBA=m%(uiaFA1I7ekQ~RI1Io0E0=~K9TE$jPLc8;0CY7SE67tnWg}k)u^Qe|D3HSr-`O5{0}b@iPyUX!4j_^!92s)#hU$qTW}Nz$`Fh>MBt5G2pd=+400uL=M1@&$0-VtrnJ`(EjS9Sosj7S_=>N#;t45e09+JIt4%lqhwuy;7yP*tOiWq$r??Ryd>L;_I^!P|0K*fk<QW`5&dxytI02wH!MZDzpdj+Y6iIl&7OO3F1fW%%ywO37l(T=(J^7#oU)S~QA8)mSSHRSOh!DddLvRVhZ*ss`<$$LUOls%q)3`YYfB<GNdJEtONd!UWNu=>kSdv0d2OMB{#{4@$U;wA*-%f_?7c7CfP$;qPn84Q|#yapN2oZg?p>);YK;T&lSK$q0h={-utUsD_{a_>F^bt1=@J(|fO1fdT>kz>Y?Gq4iQs5v*1T1!01bp_`7ktkKgG9+AENBI<q{}Ht!raDq3go%RaPT=QsRj-TlU}MgLA(H$b@+5I7w=gF@G=9gk-WyIou}|XKfs<S;(w9v%|fKW0)wzdLm>610zf$T{J0IjgNVigV8q0A0HzFtU47~X5Sd^N0#f+!&WaH{_!Q*H5ccskOLJ<3Z3N({Xf70xR(wJLF(7%6o*cuT39ta}EbrtXrh>_we}W39D6SiE3eG-+lQzLJozHw|2EXRTGZR2$grzvcbb;l{$gKq|od-!*#3x(<keu2O_=X6TFjU(t_xB+$fP9O#To!9ao*8iyeqR85McTpc$>RldejQrV+tC_Q1;`8_Muk%q7Munk1mxYY@8f6uHUO#&Sr<e<$V5XtQ^5)cGZkEBU^|)KOXl}>65BhO-JEJKrQ1v>cN5ypbbfC$v6sxZodnnvtdE!HSGE#6o2b40+s@W;Z`Zn=KJTUPdwYl7t;=rS-O_HDkYEE~IxVH$yE~8FjmK`zd<1_rX+K!yHo+IT-%FLwbG1kF{k=?aKULjL);Bi`d#U>7M&W3ywWPi2ZtJr3rqCDD`~&uvTz9r#znmj)rs%s{gxx*LW_rD!UGHr$w)Yo^fFHx6Mj?^sh12NtFrol)eqIYJI=)evmJ!HEh}yuONo|w%b7D9Uf<bhB3<KFlfUG4x6=cR|12MEFmx9F%a9<Oi3bJ63Ih*oaxhlw=sdFF0T!<NlZ3OBGnp00Oka~h2s3*AFu~977<8zqSSbp*K8893;<Ijj-MTP?#^FLVDaPuG5eS3mnmx0egAHWkQfUu}}*zan$6djJ>FUQ)?hTu5xVo^fAY6Qb|f_2h75#l)PB3JjST|N=wx+Ug3UJkO)fM71c)gZkBuhx~O)-9vf&9Byd?9dvN+uz*k*oMCvT0al?0`~`Yy%?4c)qg!IUL?OsogTW@ON%-cIij0YclA6j$DCtHxh3(>4Sw_^wo?S^IWU-eKk3341g*uhOK&A(<fOdqSKIm3GsEM#h`h@d9sX{PRN9)st6c<BZQ%i&s0%C@Ve7?**zvZnz7ev80Qby(G@+Ik*W~V6vB?<x5w9~2_AnfI%mVyF1_0hYG|Y7sZfoEo1C!b^R$j|@^wHld9~}D2`hi~IPf{Z$_R=x6pp4XeX@y{Ps}>{WVun&Mtw>BO-O|gt_*R}JNUN81=_OyJ1WPZ^LZw?uEx|&iRC;-qR=UNLn6-#aFTa8#hT<=AtUN>f)p9qPWcPy0+`z{XBFiZHrmD78a_LoGY^&Ddq>fB&7%97qpLI7==vF8<Dt0%DOQSk^)fq(QItDJqGZxC>VTp_K2#l9HGI6ZrA~j#K)O^u5RaZ=_iQ-yim0BSswE88fRY8$zCS3P~E2p%ICAIR1t93!B1`YEP1!t=#LiJR1t=58Am;#<IQl*+!<%Me3=vt!$AC+;X8syWKMqO%~xK{UscrCRSj%`(Ch^xjKapjtPUgS$-eHM|{j1^~ymr!N!wT_G%>()rE7$<r$V+|eOD(dvAGE~JSRr#<*cIq~2nxK}xUk6C4?S!%NPp!|w`XsCP>JwbAr}_)&I@Vf7Twms<j!dsHlcgSvzNyG!TD=t4s;<=PDWTOiNv%SPR660BC|p&gRWqqoNw|KAm-;2KwR$y@%#~`SdWx3nDa1>xHCTMBx)Lgdq`BgZZ`E2zA{v>bdWzJoi7b&&N1VCRqn2)!TnuYMs>2wOh&jtFyVQfpBA>absN!0yRgNKEN|hnidNApx{!DE0#ab(-*20OcGET1!gR&#0&^2LiY}7PCE&rgNPq?Ys<EtG~s|tiI8fmI_N&Z$Rhw2BFszKx>HGLwM$cq*hNy8xMTMO%{as9I(t=L+)>~XwI(#oxc+z~yzG=Z(GYb)cDL40N-E!$eSK#=Ts!<|~bwSao&`e#8}v9)mBC0?)~A+>UAA$8&<7j6|@TLq{WF0f{#Wm^j?yK&HuB0IN$7tBLsq-8jvmxVfW?L`Krr$sNZ;dCPwg6(j+j->CJ=8F@~d}|>uq!--!l*T8v$eOmb?2R?kXd}{o*L=9qXSvam8|e|Ij>U~|G&;2JQiB88F&!_twa_ZODr?LOG^Iv%=%8GKQzK0U^QgF996B(|(3}KmO1LNs(7l5*FUbq2gdb)Gl3{TNB9dhvvz9{n8grQ&4d#;)2}%<rw;_%grBw4H5Y(2inON*980BM>UT8hYVFsp%Mr=%Q2MfdYD6BhSiuvtK3&UYhM68OaVi3c2(2Q$x>4DAE1?3LgRmHaOoo}W{9bz)Fryf8|mA#5eLY1xz)}Fp^_CbH#L5{)7K>fxBz^ZnGzDf4n>_HZe-SLuGxa4jw9GwPRkm!Rgm~E+yNEt1q@pkAy2Bos0rQ8{%wsGj7{Ftd&Dh)~19(C`))WdMLVI1udP%P(%4n*XndL!b)jLWz@bPysI)e~ccLpZgK3UlfyaYjy^a9SEtChJKq?2!G0GfjL3@kD@XU;06~&>15t#EkI4WNnv)m}Kr;?{EX_#5Hs0dk5=7wo=4(92AtAaK3ZOv`5xs*BB9CTjW6>)FGB5v-$xfRPn2{w4ZZbAFM)u&-!jqA#05ML-avk>H)+wGsJFN#;gZp>+Xd_fYoLP%Mpkf>_SQz?85vDQsmmxMl=o`v_E9VJe3-ynxeXQU?O5TOEH)PnLxWUKXlMOSGHb=FVLPV4;_Svl^kh*iQIAeCLL7tRH}&*V}wIEjg1O(iV2{>EXi={$UG5JAsY#VbRe9DD!vF8Y2Qs6%Uu={zcNPqbl>@4va!oTOfq+=cZ7j;=GqPV@J$~g3#md63Nlr=DhqKMy0qM(yT+J+?X0sts6+gtkf0re1$Be8C<bBng9_ONM(YnM<PP#)(FZBncMw*%8MIEPAhFwpjqSS^G6CQHlr2XfVXzD7V6Y4GFGxvHlrZVufoZczQuh{FPgFJ64;@IB^DVl)XE5V3DGwclh^5VR(t^TqIxHPjK$n%Asq8LQ@r^?Vo%XP_neY(~=9HPtgqcUs84z-sh11lKGTA~Pqyyo!H1Qdv5CM|K4zjp`F`|+?AKan4EW~8eoiXNmWIb1n31cjV9b_S{{h*-GgtG&urAx~lzH5w45<BZmkvhb3WL7(XxGKJYkj4me8dYfTTYpd?caVQblp-bP4#El#9fZ_Ln8hyC!62p^iq)ov4gx9N48&;}>_SMhRB1-83sq+JLkDuoxx1kZi*hT;lemMp<I@pL+N`D%Jv(&JnIfOUVCH5qNwl27O9z#XmYU3TPDv+px_1~lujEq~N<a(Y5KeugBGsWC;luxNsb%J=bh4D9Qqo+6Q`f|25IXFmY`DZG3yEJDBPzx=K7_1qvJjKPU1%L5z8r<xrm;A5#4ZbSod*S#CR`jibzNHOV6~Y+d_CyYRGrFZfXx~khzM#1X;BP55*<|-?^}ORA#05ML-avk+6E#WWzaf`&zS9CY}>q$2#}V<PlY0ZxWO)@l))~{zaS++Ny0pIkj7XRK9Z)>XghQucX9$uhkJA$D2Kq@L1oC<P;?MXr;u_KOdWKXDCdWCu!<?Im15r9frzAnw<E@=p1N?F8x`i%QE_uR%@$5WLn?>m1VTCxPE!@XR!k=*NftfGVg|;DO6+`42MZ*#vQ!lcW6bryI&&QceZ;DdDhqLK2L-t%oE|t$U0Uw2U1Mw#-&tph)FGB5v+4oFRPn2{Bv<MBU=`~7)*n>J9poRP4^ndMAgpjVXr08*-7akGICx>I#uh(i%MnN#>_R#i?85xZvk5AbPv`u0=s-^8WSozx>0~<&9dwk<ROnFvgXEzDsc^<-F%9GnPSCgmb2=O3tlZQNPQSQ=$+Fg&01dOfBaCEo?Feq@aGfkubX^vv7&}>31r77PBlu312~bBEIzlJQ6hl`KQ%r*jiL4tGL>;A*B?8=GdIxJs$cEY>3Sx?$$;z{@*S}xLpZ^8?h1b8=zt_K?;g7P{ck;esuD<~AKmQBhQiQ_')).decode())
PALETTE=[['ArchForm_Frame_DarkTimber', [0.30000001192092896, 0.18000000715255737, 0.08500000089406967, 1], 0.8299999833106995, 0], ['ArchForm_CurvedRibs_WarmTimber', [0.5, 0.3100000023841858, 0.13500000536441803, 1], 0.7900000214576721, 0], ['ArchForm_CurvedDeck_LightTimber', [0.6499999761581421, 0.46000000834465027, 0.23999999463558197, 1], 0.800000011920929, 0], ['Barrow_steel', [0.23999999463558197, 0.30000001192092896, 0.3199999928474426, 1], 0.8299999833106995, 0], ['Barrow_frame', [0.550000011920929, 0.6000000238418579, 0.6000000238418579, 1], 0.8299999833106995, 0], ['Barrow_teal', [0.11999999731779099, 0.2800000011920929, 0.2199999988079071, 1], 0.8299999833106995, 0]]
FM={}
for name,(vv,ff,mm,shift) in OLD.items():
 G[name]=([tuple(p[k]+shift[k]for k in range(3))for p in vv],ff,mm[0]);FM[name]=mm
old_count=len(G)
PALETTE += [('SceneGround',(.40,.37,.31,1),.96,0),('NewMasonryWarm',(.63,.57,.44,1),.92,0),('NewMasonryLight',(.72,.65,.51,1),.94,0)]
box('SceneOnlyGround',(-2.6,-1.8,0),(2.6,1.8,.06),6)
# Two scene-only masonry abutments leave the complete old crossbeam ends visible.
for sign,label in [(-1,'Left'),(1,'Right')]:
 profile=[(sign*x-.5,z+.06)for x,z in [(1.18,0),(1.5,0),(1.5,.84),(1.16,.84),(1.16,.76),(1.1,.76),(1.1,.12),(1.18,.12)]]
 pad('SceneOnly'+label+'NotchedAbutment',profile,.03,.87,7)
def voussoir(name,a,b,mat):
 angles=[math.pi*i/16 for i in range(a,b+1)];v=[]
 for y in [.05,.85]:
  for r in [1.10,1.36]:v += [(-.5+r*math.cos(t),y,.90+r*math.sin(t))for t in angles]
 n=len(angles);f=[]
 def quad(a,b,c,d):f.extend([(a,b,c),(a,c,d)])
 for i in range(n-1):
  j=i+1;quad(i,j,n+j,n+i);quad(2*n+i,3*n+i,3*n+j,2*n+j);quad(i,2*n+i,2*n+j,j);quad(n+i,n+j,3*n+j,3*n+i)
 quad(0,n,3*n,2*n);quad(n-1,3*n-1,4*n-1,2*n-1)
 record(name,v,f,mat)
for j,(a,b)in enumerate([(0,2),(2,4),(4,6),(10,12),(12,14),(14,16)]):voussoir('SceneOnlyRisingArchBlock_'+str(j+1),a,b,7+j%2)
for name,(v,f,m)in G.items():
 if name not in FM:FM[name]=[m]*len(f)
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
focus=Vector((0,0,1.0))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.name='Preview_'+name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=7.3;aim(cam,(6,-9,6));scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_Ground';m=bpy.data.materials.new('Preview_Background');m.diffuse_color=(.43,.43,.43,1);ground.data.materials.append(m)
scene.render.filepath=str(OUT/(view+'.png'));bpy.ops.render.render(write_still=True)
if view=='thumbnail':
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/ruins/{ASSET}/v1.0.0/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':'1.0.0','category':'scenes','assetKind':'scene','theme':'ruins','style':'S01-clean-geometric','title':'Open-Crown Arch Rebuilding Display Bay','description':'One static reconstruction-stage display scene for the original ruins/repair direction. One complete previously published timber arch-centering model remains at original scale and shape, with its two soles on a new finite ground slab. Two new scene-only notched masonry abutments and six faceted rising arch blocks follow the original deck facets while leaving a clearly open crown gap. The entire old timber form, ribs, fan webs, posts, ties and ground soles remain present; nothing is cut away or recoloured. One complete original empty wheelbarrow stands beside a clear frontal approach, retaining its full tub, wheel, handles and rear feet. Both old models preserve all original oriented triangles and constant opaque PBR values, with only declared whole translations; no old independent part is extracted or counted anew. New masonry is context authored only for this scene and is not separately listed as an independent model. This is not the old breached-wall staged workzone with separated raking shores, nor an altered break count in an old arch. One scene, zero new independent models. Static illustrative arrangement only: no real construction sequence, installed-load proof, masonry bond, mortar, arch-bearing certification, human navigation or repair safety guarantee.','bounds':dict(zip(['x','y','z'],[max(p[k]for v,f,m in G.values()for p in v)-min(p[k]for v,f,m in G.values()for p in v) for k in range(3)]),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
