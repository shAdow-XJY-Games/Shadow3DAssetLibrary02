"""Original two-gondola aisle and checkout small scene; maker SELF_REVIEW workflow."""
import math,collections,json,time,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

def dot(a,b):return sum(x*y for x,y in zip(a,b))

def sub(a,b):return tuple(x-y for x,y in zip(a,b))

def add(a,b):return tuple(x+y for x,y in zip(a,b))

def mul(v,s):return tuple(x*s for x in v)

def unit(v):
 n=math.sqrt(dot(v,v));assert math.isfinite(n) and n>0
 return tuple(x/n for x in v)

def area(p):return sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))/2

def clean(p):
 out=[]
 for q in p:
  q=tuple(round(x,12)for x in q)
  if not out or q!=out[-1]:out.append(q)
 if len(out)>1 and out[0]==out[-1]:out.pop()
 return out

def clip(p,l):
 if not p:return []
 a,b,c=l;out=[];u=p[-1];du=a*u[0]+b*u[1]-c
 for v in p:
  dv=a*v[0]+b*v[1]-c
  if(du<=1e-13)!=(dv<=1e-13):
   t=du/(du-dv);out.append(tuple(u[k]+t*(v[k]-u[k])for k in range(2)))
  if dv<=1e-13:out.append(v)
  u=v;du=dv
 out=clean(out);return out if len(out)>2 and area(out)>1e-14 else []

def planes(p):
 out=[]
 for a,b in zip(p,p[1:]+p[:1]):
  u,v=b[0]-a[0],b[1]-a[1];n=math.hypot(u,v);out.append((v/n,-u/n,(v*a[0]-u*a[1])/n))
 return out

def contains(p,poly):
 # All classified cells already split at every edge's entire supporting line.
 x,y=p;inside=False
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if(a[1]>y)!=(b[1]>y)and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:inside=not inside
 return inside

def rect(y0,z0,y1,z1):return[(y0,z0),(y1,z0),(y1,z1),(y0,z1)]

def build(parts,holes=[],mat=0):
 # Each part: x0,x1,CCW yz polygon. Union boundary only, no internal faces.
 polygons=[r[2]for r in parts+holes];allp=[q for p in polygons for q in p];lo=[min(q[k]for q in allp)for k in[0,1]];hi=[max(q[k]for q in allp)for k in[0,1]]
 cells=[rect(lo[0],lo[1],hi[0],hi[1])];seen=set();lines=[]
 for p in polygons:
  for l in planes(p):
   key=tuple(round(x,10)for x in l)
   if key not in seen:seen.add(key);lines.append(l)
 for l in lines:
  nxt=[]
  for p in cells:
   ds=[l[0]*q[0]+l[1]*q[1]-l[2]for q in p]
   if min(ds)<-1e-10 and max(ds)>1e-10:
    a=clip(p,l);b=clip(p,tuple(-v for v in l));assert a and b,(l,p);nxt +=[a,b]
   else:nxt.append(p)
  cells=nxt
 ec=collections.defaultdict(list)
 for i,p in enumerate(cells):
  for a,b in zip(p,p[1:]+p[:1]):ec[tuple(sorted((a,b)))].append(i)
 assert all(len(v)<=2 for v in ec.values())
 xx=sorted(set(v for a,b,p in parts+holes for v in[a,b]));occ=[]
 for x0,x1 in zip(xx,xx[1:]):
  x=(x0+x1)/2;ss=set()
  for i,p in enumerate(cells):
   c=tuple(sum(q[k]for q in p)/len(p)for k in[0,1])
   if any(a<x<b and contains(c,q)for a,b,q in parts)and not any(a<x<b and contains(c,q)for a,b,q in holes):ss.add(i)
  occ.append(ss)
 vv=[];ff=[];lookup={}
 def vertex(p):
  p=tuple(round(x,12)for x in p)
  if p not in lookup:lookup[p]=len(vv);vv.append(p)
  return lookup[p]
 def tri(p):
  assert dot(cross(sub(p[1],p[0]),sub(p[2],p[0])),cross(sub(p[1],p[0]),sub(p[2],p[0])))>1e-28,p
  ids=tuple(vertex(q)for q in p);assert len(set(ids))==3;ff.append(ids)
 for k,ss in enumerate(occ):
  x0,x1=xx[k:k+2]
  for i in sorted(ss):
   p=cells[i];c=tuple(sum(q[h]for q in p)/len(p)for h in[0,1])
   for x,sign,j in[(x0,-1,k-1),(x1,1,k+1)]:
    if not 0<=j<len(occ)or i not in occ[j]:
     for a,b in zip(p,p[1:]+p[:1]):
      q=[(x,*c),(x,*a),(x,*b)];tri(q if sign>0 else q[::-1])
   for a,b in zip(p,p[1:]+p[:1]):
    other=next((j for j in ec[tuple(sorted((a,b)))]if j!=i),None)
    if other is None or other not in ss:
     aa=(x0,*a);bb=(x0,*b);cc=(x1,*b);dd=(x1,*a);tri([aa,bb,cc]);tri([aa,cc,dd])
 return dict(vertices=vv,faces=ff,face_materials=[mat]*len(ff),material=mat,yz_cells=len(cells),x_levels=xx)

def topology(g):
 v=g['vertices'];f=g['faces'];e=collections.defaultdict(list);stars=collections.defaultdict(list)
 for t in f:
  for a,b in zip(t,t[1:]+t[:1]):e[tuple(sorted((a,b)))].append((a,b))
  for j,a in enumerate(t):stars[a].append(tuple(t[k]for k in range(3)if k!=j))
 bad=[(k,q)for k,q in e.items()if len(q)!=2 or q[0]!=q[1][::-1]];assert not bad,bad[:10]
 for i,links in stars.items():
  a=collections.defaultdict(set)
  for x,y in links:a[x].add(y);a[y].add(x)
  seen=set();todo=[next(iter(a))]
  while todo:
   x=todo.pop()
   if x not in seen:seen.add(x);todo.extend(a[x]-seen)
  assert seen==set(a)and all(len(q)==2 for q in a.values()),('fan',i)
 volume=sum(dot(v[a],cross(v[b],v[c]))for a,b,c in f)/6;assert volume>0
 return dict(vertices=len(v),triangles=len(f),euler=len(v)-len(e)+len(f),signed_volume=volume,single_vertex_fans=True)


def finish(vv,ff,mi):
    if sum(dot(vv[a],cross(vv[b],vv[c]))for a,b,c in ff)<0:ff=[q[::-1]for q in ff]
    return dict(vertices=vv,faces=ff,face_materials=mi,material=mi[0])
def revolved(profile,closed,material,n=8):
    vv=[];ff=[]
    for r,z in profile:
        vv.extend([(r*math.cos(2*math.pi*i/n+math.pi/8),r*math.sin(2*math.pi*i/n+math.pi/8),z)for i in range(n)])
    for j in range(len(profile)if closed else len(profile)-1):
        k=(j+1)%len(profile)
        for i in range(n):
            a=j*n+i;b=j*n+(i+1)%n;c=k*n+(i+1)%n;d=k*n+i;ff.extend([(a,b,c),(a,c,d)])
    if not closed:
        for j,reverse in [(0,True),(len(profile)-1,False)]:
            k=len(vv);vv.append((0,0,profile[j][1]))
            for i in range(n):
                q=(k,j*n+i,j*n+(i+1)%n);ff.append(q[::-1]if reverse else q)
    return finish(vv,ff,[material]*len(ff))
import base64 as _payload_b64, zlib as _payload_zlib, ast as _payload_ast
_BASE_COMPONENTS_ZLIB_B85 = (
    b'c-ri}U5_QlajtuRensE)2pAES-<iC#bRffkH@so_z!wBTw8@q@&~Ql1jC8Cm_`mPUh^p#d%~^|URQbNOU`NC5p~qxA86Wu-l^OZB`+xlL-FH8}eYpSf?r--$'
    b'Jbw88@q_&1KfU|-_{aATZ-4vv?&JK&?|*vp?(sJd-~Q=;KfHT<`{7?7-n{+r5AVMF$M-+}`Q3NFdwl#T|IuF_-+z4btw{Ll)vu>7N_u@a|1r7w&-st~tJnX}'
    b'9qeZX9>9}dkwSZBPO>%eI7c<6BZrD(_XS6e7RQa2r85L(U++Ml$lW~<9mrMCv0doM7F7;4V)*J&-N%kka{oJGK+_RBuz5Z)muJE8cua%R?fK+Ec7#@L#8i63'
    b'koQNG95IeO#yIX6<LG0I<Bl<oKE}8&GSz{x7P14m`c0WTgeEf2HS#Wy*5jXcErCxY@5|^sqD3`qDnD#0pGbBioktEE#~*DReYA1p-hTj(9yYX9&6ARhWsT$O'
    b'=;)gZ$6gFOwi{1Em9s!~harg@Z+FbbTNgNq?ME__m~wN+q}<e~j184L2uRM-_HJ0X$%Vqs){y34o;4jgRpZFsb8PRO%=U%6DlP1_MIo=(c-c#G`iq$xI>GtG'
    b'{p`yJawDeFBc_sZYzOjz%!qOHF~)Jn7{~7NM*z7I!~BXD$V)?Vwu_$ZVyB+?X`n-hj+p8`;=B$y1#}3}5x;UBaY~Px06Ku@`0H(A#wm~!K+Fv`dw<<G^yFI<'
    b'>@&xae#wAOWZ!DwhD_u}jAviF>H4u;=h?9txuMCirP`2u^)s?B_i!(xMD}GH@?9e8O({=~6=JuGRJVC@RMO@Go*^gCKFf4U%pBlhJhnwS>6RB!LpCWB$G7Kn'
    b'M9h#)%Ej^RNglW-cAuEo9;BHw&?6=sqG6?LSgAZm_aSj&3fw-=?GxmHq4$Vm!i9TJfqZ|DehNDh&%Lc<40)QM+mw8HkA4Fq5>LLJII)s(+?a9PamMk-8Al&y'
    b'9Cw_d9xGxWuVqdZCn~a57wp9$ac#jK(zvtW0do@5peH<{``Duy@jM@UI$|31gvX+hzFxgZPLgwlSRB=s<TNNdtxS#-ZlL@uAxTWq)4o%`(2x}_9R1i1B%AYT'
    b';G~8NUp=Px$id0&dPfaqq?<>lUsup4H~1>jPv5W)-yG*c{wF}zWv(NMqysVJ^F`#(xJQ18XWdpil1Mu9Lq0-9K234tff&w(yyJM3BTdJgFQQdsIyn$p*au!Y'
    b'3qy`E$>*cVu48-dXA8nY-X#_C^0RQ)W+gFmFvNW>d5=Wj<+3-qygeY<e=j4Hwf{Q;NZkIhcelLl-%+PdxjVljfW(a-dtb}j_#JiVo4M=b<A{4q{uYzDvL-LA'
    b'x$Ei!b`9Lz2RjwWP0g{h@!ae<dG$`7?Wp53d7(*N7V*P`&<Dsb%&;GrAy?FA*D$5O^Fn^+g<DRPT}_n!x(oSn7j7X@b{)}|#+)iSTBzon$lhbwGO&Xs9HC!j'
    b'>sOgL$Mzp@CJNN9PVEfbSYdaCLn4LR5op&<+0_@g#U&27w$Cn2z^%M+z@2vXy?t(30{#Va@)dgOb$0%ZXzGn`@^yCpg<<N2X!33EXOCSnt}(sXKXdo9a9Uzo'
    b'GI6)+iJbUI+(1dxKylogrl-#z^LlyUIghGdBD*hf&FQE&TTiy?6PH#=;|en}x&4lBOWJ-Uu|L!#ZmvI3lkbWAq2?)ADm_>#9Y}Q_nMMp2M;}=ndt`CczD}o6'
    b'gN1Rw<<xgMQO%i|)@0oMcs4C0E)IV>`*a(`9LNHDi4=H?mM4o=x<xA;$h4@V$Eah+DDgBW@5bfnv51_wF~gj51MvhYx9HBPO({gjuGw-rdMCP$>=~cHbG*V4'
    b'C#Qf5`HXX6u6ql0NzdM~6!Pd<xYJ)D57mV`_t826chkb%La=v8^c@R#|G?fJ(YGta%|qfJB&F|F$XgZqPKCTtq3=`Z+Z6gPg}zB4?@{<$6yjR&n6(mb+Yrdh'
    b'c<vD_@(HZSKBGhjlFvj@qa{*<#gmWgb?r!Q^W><E)S#po^4XDl+C|++J`+ei#umwk^th+yn5Qc}H%xflEizr^x$(#v{hzG(^<dilA0EDa{BZx}-B+)AUj6l*'
    b'$LaGb%t~MhvzY>xFq<f13A4ZR>$`#_l-G9^OQ^5!8kW#zLt&#eVs!|j1JVy}k}l^QlHq3n8Zw(oI7r4Mg9p}DLAsucV1}C`*CjM0frB^5C{n<&8^Bt4(E{p?'
    b'C{wpXj)tztaEN7eI~6o!mS53~CUbZLBj*3{6PV%qip`-R4m*`cjVq|JqS^}Sb3YFyzOQeQ(?{Py2?z?AdxwCakZ!7shV;0a#}f}-DE3ZR(2%(k3J4m)v#B}='
    b't4W{LXXgi`<NGHb0YM>i_zDOL>88pI$Q;6<qRkc1khYi$3hAb5V2E_aIfUZ`9#%RC3rRYxU?E;RBNQT&R$ps7^z<9R5SdFdT9cxaRs<&o`idxm^NJG~Ax9w4'
    b'46h42EF>%r3CQ()T>1zU(oGe?5HVFEm`flT4e3Kl0ndsu0wbs1*p^ulnuYHpN&`c>sRV>JSBE5rhRg$G^5}K&+#wUPGp4BPU@T<r?HvS#h^Z36Tms2x$UJtX'
    b'g5EZC$3userdv5Iq?@aOA!4cshU9tN%00p9(U7^X<bZ|*a0quuD&1t@5EjQ5G^Bui(g(=CkjN1{)OQdRBGYdILuAd>z>wUvn1}jY(2xS2v~pS|Esuuu=*r*_'
    b'mI(9cC6NdFL_P$}qi{xV9XbdK>D##uf<j~uAHk43M^>3NDGm*B;7w3oHbKxWc8A2$O@`k6MzAIVDd>&q@=3OM@KLc2f<h)eDpt@bNHnALb6gRe?dp)8?Sh^b'
    b'E6ZuIg0@yS7`TtfDMUB~?e?&2uaUP0UzM!i7qO78MFvB}RB&@u-CmalhLnCFcmhM}+)t`QL(nM?iL8RwB&#M+pGY#TJKlpkV+TPYH7q{y;Jiu)VKs@G>&kG5'
    b'2ZwNnNC+o1B!P2X5?KMPi9izCCqa8W)Lb2s(dLp<oPCf)E{ST<Qw3N^pR@`XBBrVYa|xuOA^i~g1U^I5&vi9qXKY^25Md$xvX=)##8iP`E`dZeq+h>F=u?CJ'
    b'o(8frwxXv7v5<b-vVb9Cs!A}IKpGm-dct5rpGFpn1G~PHuoO3W^$QlG=JI%Lf^N0l6w#O&0gh(DXgDXlHVK>s(IE3^Z4{Hhu8})6l9|llwM8d^DMjafEJdcu'
    b'f~L4h5E26o&uQS*l3@CB2|J-J+Q>(oie4)hv^E;c6WBF<!xyAF!UW#Cb`qA-7v-IVrN~yyqbbhy0aI&A1Ux5zcjJPQ?RY{{S`x#7qggh92@OeTw`ktVVGDj#'
    b'E&l+8^mLDa9QyLPkgx`mR~B5x799{uMpsYhkX}BaO=wD!SqxqOqkA8#OI1}oe7h{0SqCj&<F?Hblv8ABQPCJVkdX04YwPAep)s<<bl4&-!s(?)Djd@f4wQ!O'
    b'HyUYJqY1}P_#mhn(qP{#hdRJU>+_8BV!41WD5tCdKJe%W%B<z_z?i=Km$jzPcuq!_mlI4vSIQHL8V=uY;3jj6$*=)1ZDT-!WAFh`Hf^vq0A-FYc#cF`!*ia7'
    b'Xlw<@EewK#b0mcxJf7p>omB0X@gtjG;~MK9;fR00`joZ*VB<hd=J9rGTR+WsPKMj9Zw&gSZ3nGY=GI&nmLeYp3mzl(N_dXAzo0WKA#1`5yVVhj4AvEIGYPc<'
    b'kAVtzO;Fc>l_^_1S2(7^11)Vs8Z@yIr_E|uPWQjU8a$!}2G++fqZ&Bcl+#B7XqhhML@{2(b0U6ZOKZGg?WUZ7kArEAYp{Q&)j!~PbKCe<@SK9So7C75?<6qA'
    b'>19)FE+;NuLZEl#1>>Ul2HAJICTh71rZ~Np4K0ySw1$j}4NP&pEQ(9m&n;~|ZkHUKlOz!ey-Vq|+=qjfr7NO`JhXy64H4FpP$|JVy+n?K*2n2}8G2YlYkL*>'
    b'J|P(BkR~TcTxwW`OAT$Xyqvgkc>+`N1h?2y^u<AI)X4yo9eR}MQ<+9{1yg21*9cllENcNShpmGsVHVJnbDzg_4v1iiOY*c6bm8o@7^2GwOmR7(*XJo~?LF+O'
    b'DM_D^Q2={RF)xSvazSI9SPeP_)V7?r#;!61BOZblmXmdvoVd;njd8i5*MNFQrJ>j7f{}TkV7E1Oy$@3yoTF0#^eSmvt}9~q>4J%(67*xCls1#44YW3tENzqp'
    b'#gwHQ9F!vVlC>=!vluPoIbybgjy3U4#)q`zxS(d!0ElR-DF(igaz)0PKI%Y^;mS%{SXhkL3awa**h{8RJZ3SPgLA5w&7)&Yyptn5q;o`@P1jHjZ8eQE_`cm$'
    b'IR+tCLvIfk78FyoI6Iai_L7}D9<vxN<2hosf{r!aA7*$+OF{~2HVuG?wwhw#X(HLY%T0FZ?cbhMQ55zi@M+24U@>AZ5=X3tO{|DIS#)yX7*MM<565_T5>NdP'
    b'x7uPchc=s&A|R43YVf?5vY?o>l!3ukfzZNy6wG3@jOX+zv=wx$2@9K)6pP8nLu{eGwDp_<#}s%1T<U@K%%sN_9qJQXt7weYHG*s7mLiHAj+)J(IWwaF^5|$2'
    b'oeCT?Bj9F}PatYLkLGx}x{v+dlGZaZeu6&CJgujQ(41Z*ro*tD#bgPukKE1?yHz|#hMk7zbmKv5o+-ykCo1T;);Iv`6E}UJ{*fAP(odmv&%BchR1VHjy9G37'
    b'8QLP=ZgK6W&=L#E(TZCc&&l|>j_bIC9Y-~!1Kw_KwHr7N!Zx2aJg33!CRM6r@`hI4@^S@L=LIZBRH<mrVluql{Isrju=A;KWIlyn6jqL0;`ScT@%Z&lTH_6C'
    b'H{poguyLSWr@{TBCi7^!E!VZgc+h=`)|1L;j+}577?>kh5HrDUf)KkEJg1MN(6U7fM}oWIInqxvJgzkk8k)1{1O4_VhwA&aM<1YR%e<c8M|0Lg0AP;X6zwo9'
    b'$M;H4zL!VxA>cWpPsDS2aEFBFBrzU5t~Cx4nzQHwJxwRqpOWYU{n980_EN-i+;Tb)%#q8<*`YaJs!B;M9%!+bh12JSIKer+0*8+d&k_Grcw9>yK=sj(7JVXi'
    b'KK09ORUbV(uiRl+&XT%zcurmO<XF4)Iy^o~FeE%D!Sjj2k-RcC4=WtWlVghuNl0rlHsLu59S2M8n!Xr;mX`6#DR_>A0GzX!tm5@)>%Ja(AzL}JpM&1RTsZQ0'
    b'kjHa8Jny2RR`L3jRi6aUCu*_+TAD*lrZ6l=wj}Bwcz#r2V11tQZw1dO@VFL^#&yPXGCV)3p%&r#C@16n6SsVP#d9j!ZhARi2UF~=X}?qgz;b-r&Ou`JQIiq$'
    b'+14S@QYy;H!f|*`U+-j(=XmrwaS64G)<-#_5B37R+|QNuDE5A?)>QO(j$5usfH_(b0B$!gc`^Au2fb{%aQb`-y=As=`d|vZ1GsRcpC))*YaCQGXVC|H?kO*o'
    b'JU#YOj$F@_^&6Pemb;)}PD)FaEiA`N97w!D@0To`K3<oA=k(-diFi&F<H6%v;-Ew{XVC|K??dXY`jXJ+I`z;cwmOweJ&wScmXe5IyY&KCz7+U5$g<tb!JZow'
    b'j+`4T6>m4`MDX*<OB_`Ax#&{i{z+T@0Qy?6uhY8E!g53vfni@i);u}EZf?sTcsNJ)rxnks@Vx(GHwXXDBq1&FRz05M@o_M%aSis*wE72J<gF}KC4CKOj_(zo'
    b'e8pCi%iB4Wgy!gZ3as7a{F@ptqB*`s__-%3ji-ZLLUU$B|Aj4Dww+JJp5v-+J!glto1DK^<7G6**9<>*D;3y;1Fn%LT~vNyYklSIe0)T6^qe==Zt}tb!ETaL'
    b'uJC&-TIfrY6#>oBJQB8qoxF0;tFieu!SfVtLhl>3u$&kVT***|&<3}g)RXEJzdX2#o%pBQ4P3=8Z{M>Dnxo%kuy&Jtyc*A=IbMPen^&IvT2`tBIH%Wt^9`$y'
    b'ThCKq&jpCdGTd(ZX-<t7;hYxX-!=7$tBh|6&gm8Ue8YZsp4NO-D{zjEJJ@qv(|T?YYd1AnhTBcAP)h%4a89o?7og<^mm?0Ta~zrz`XCpeb@TK}TfaXSuyxsj'
    b'xF+;p*zdG{`Mw>dgyw`v;sAS2b**0&u;1r8C-m=g0bDn)F5dwIxNe@9tikOjpEP?uF@WpYDFSXcxk}sbQ3mJGoZuXM+>w;B26shsf&?A5o}HFH=r9-1oZtd{'
    b'-j)=sP7V>x3B4{`a8Qnxs_FV*?}c_wko%3;b-b3Q2=H}PkS^Mtgso>+%5u&jVC%B!lz^WX^yr(1uS1H2fCL@(T#Z}Kr3Kf}oZuRKov25ZGkhJNWl7cJz+?A6'
    b'X*ow6u=VU@i{%}DpXJtjEZBX$rmDnl$T$eT_tSpgEck@yB=mYmInJZkqYKB0@u25W;&N^S>mT8$f57^zbuhr|-nzvB)^2e<w*j_WbZb8a$9122dOk5g@1HK5'
    b'ie6tU$3^u1XW>Xcg{~9zC`Cg1M>y&qus&%yR|DQ>iOD1muyzY+IadR=n{4T&pMvAMFL^`vPjGmSL+|I5<1%``y>OBk4;t5XIroJ1k8spKV13GR?g_lF7n4aG'
    b'VC^O)Xw`TVnxp*`8`qNOll%^JU#}bo&$}!f=|2%~w<yMg#&uiHrGfJ<wXOca>LXW-+JyFxrucN+fzI1<#7>NdwVRqO;Nx1RI2lI^o>S2ID&_bIoljJb<P)*='
    b'ZuRJ>L;FWK>L0K^ZaFsy&RdGfBo454lPlF~yo}~(KLy9NjH5lS;{@l(z7d-r4Vr>Q=dTxz^i$|}3^_8`&vjz`BOLV)Sf8+*>%_)^noQyVYd5*NAjZSmEpPo4'
    b'8`sOxoo+WMC;Ig~5||@h$HO^lvVhk|`e|Q`K<nx*oId}=g6BvaR6Iu}p#+a>jf0BkRJ?!M+E1bP-b25-tuQP{>?SZQM~60#x0_%4DYUMxa{8kmAw@hV!sA-)'
    b'R^a2P#<j=m<5qpJ{*j?gCc6Y3M^j$MQ7}hLmf;*VS;6a5xAj5AbNa8;;GACfE942z>F0#d>w~bxTf=i2JPu?l*XxG_Xr0rA)0N5*&*}3Iv@YnvNn$)Gr-z#4'
    b'-*Uxsq!Tqfr^j`f;GBN1IzaDL2RWxI=X;^`4;D`EKhXQm3#a!VXkEjFlf-yXj>JJBaXj8`d9z!^bE+5*%4us{XFNy7QS7**`b_wK+O~cQ9e3)q%?lpS@$h+D'
    b'ISD?`DW}2b?Ygb2u=`-)Xg)FFISIZ_tWWDiZ2$4wy4T}5{a3~7BZs|f#B=cekt+qx!}Sr4=mYjo+Q#dG=k)osW;jRA_g1_<6~E7tBkOW58mo_RD#1T>+n0De'
    b'NBU`lbL6}jw2ql_<j@#){U%4E<=ib+AK{2T6?^_5FLjFow2oQOb6gqDQM-9GM@{Akb_?4+xZpW`e1q2gQjVMt!Hzq^k#Pq*j!LLW9Dw!l+c*mK&or%drJ!{d'
    b'bO@FD2VhRv#%t(3N->$hu==zue~q2zgd^(^>^!Ga!USJe38!ZGI^J#fD6#suO&_d(q=byrF>6@6#kF1ynB&&{0+usv_v^8oR<}G~#d9irpVjKN&kA@BK98hV'
    b'w;fy`-2w;vKG?5yzgmNzvlAGWqvz5Zo>SLzgHTSCB~^y!6O|+RH|RM#<s^7MUOAGF2j@rqcCHi8N$@yWN(9e#i_p47QA<)6JSTL7M{^dF1-w3S`(9u1oZ9tC'
    b'Xin^PXycUeoQ%%9ETI<g`uIg3tbdjipTG*bpDvvU%c+}x3Oc{Dz_9wXHUC!doKo;{-PX8<)}2(2)FW;YKmSy`K4H-Z?Vq~k<0GCE;dXOR=Tsw}Bl>tWC-%i+'
    b'gw|nNI01ehNlVaHv_8TSebD}i+qv5Y=VTe=5}FhH_mT*$kF;<y{CuL6!02@ru=)r`^g;WlZ0BJko+D1GXin7epy4?UeqPzT<sLs)AK^p|I%plHR@Z$!wl0qM'
    b'OFd#NCqDTHT;D}Z=J5LX?c938a}vCtE?uYFEx<WaWEp#}KsgSrPuTPUk2_M*eG+}Jb#<quemt79)?os3<moIAw_EgSyC*T>Iq-FraF%sd#d9kB9*e}aPTm#G'
    b'S=Lq1b+4pgCEx3@>+8C__krfDbtl1`X|2zP<wPmrtoL#fo|E8t3jegPPk0Xg-jtT0h41T^lndNHS~o)Sme~6KX|4MO=Ey!c6+CBJ>I7psQR+D7h`!gR9KF{z'
    b';q{r|c|PBkJS_O0URvMj!s??Tt@^<C+qxNs)+dj_t@|u2N46vZ&RLF9c)Z=#`~i5s9k%^xz;i-?pK}n-1g}f5gtUX(O*sJ{2W~sRlkl8`kGGy855j@hWm{kw'
    b'ey&qt(0z&2C+{#cN2Z=WzCr8VE}Vw0XD1x3H;6sgsT>)vE4u$I^(`Zw6VY+7gmgmNZQ)dS9P|>~st>eIaO@=~6^7-=5UMbT9^V!i)^1@P-(rMwqUe+GoCF`Q'
    b')ou+xzNIa$Bc2oC`lu=%9|zMK2jIB&+q$aZISp+$-PiYf5)oX#H?MgyC?{&k){N%}qT)F{1kwc0yTmmwhOOJGoFqy)yxp7_4;=@Zgv)r2<SoJV*0;EZ`bRms'
    b'j&JDkKs#%K=6hx9qjtk``qU#ZEJsZi@%p4?d;^aM%8~IP<2hoyg69<c_*S=g%Xm)4$3fWQy5KnlA8&CR-zNOHGpXIa9t^tw!^5|a-~90K@$vnehqoW@zr6cu'
    b'g6XpT7{U;SFoYotVF*JQ!Vrcqgdq%J2tydc5QZ>>Aq-&%Lm0vkhA@O73}FaE7{U;SFoYotVF*JQ!Vrcqgdq%J2tydc5QZ>>Aq-&%Lm0vkhA@O73}FaE7{U;S'
    b'FoYotVF*JQ!Vrcqgdq%J2tydc5QZ>>Aq-&%Lm0vkhA@O73}FaE7{U;SFoYotVF*JQ!Vrcqgdq%J2tydc5QZ>>Aq-&%Lm0vkhA@O73}FaE7{U;SFoYotVF*JQ'
    b'!Vrcqgdq%J2tydc5QZ>>Aq-&%Lm0vkhA@O73}FaE7{U;SFoYotVF*JQ!Vrcqgdq%J2tydc5QZ>>Aq-&%Lm0vkhA@O73}FaE7{U;SFoYotVF*JQ!Vrcqgdq%J'
    b'2tydc5QZ>>Aq-&%Lm0vkhA@O73}FaE7{U;SFoYotVF*JQ!Vrcqgdq%J2tydc5QZ>>Aq-&%Lm0vkhA@O73}FaE7{U;SFoYotVF*JQ!Vrcqgdq%J2tydc5QZ>>'
    b'Aq-&%Lm0vkhA@O73}FaE7{U;SFoYotVF*JQ!Vrcqgdq%J2tydc5QZ>>Aq-&%Lm0vkhA@O73}FaE7{U;SFoYotVF*JQ!Vrcqgdq%J2tydc5QZ>>Aq-&%Lm0vk'
    b'hA@O7J{$4%V8;Cq4<8@jzj=6j|K;%Z-~aXheDm$&+qWNP**T0B{-58xef-O#2><HW(-$SZzUzND`D600@7CY_uloOgxar>i`1Wz8-~Y?|H-CKd?&0m-;}1W5'
    b'{OjF!KmPeY-ah{N!<+9Ozq|Y6kMF+w@$JLiw?F>y(~s{S-+i3_eN2?x|I@pVkAHms@b<SeW&Y#$KfQVP_?w4s|Mb5f-pywE*M~Q6Km5bH@BZ=qkAHsm-R~YB'
    b'Ki>b>d4t^l?){JNKK}mu$G3m@#(nd<KfitZ|2}^Er+<I*@%w-I^Bga~|M=ri|NQ2sS^2-+|K;)h$2Z?TiXUEe4~PR|w|VgCSHt_n6C-q=<0*B)I4nmk#;_NF'
    b'K{6J_^MnwF`<&qNEv)?PYeol|@TyFNumYP4Z!Lzgem?p}&Rml5Lwsh8zmYQjX872ce>G&;cK?Tmb%`>)zMB_>esIfQg}J!^v9lEdK<sRR2oO6*MSgu(0AlBu'
    b'r~t9`^<4vqZL=Lli=8AADnM)nxGYG3HGtR#FhZ0u!A--vnf5b);CW~3FioC?dWhg4gF{2eonyj9gkaabmmrc8V2p@MR78YeM1OW`xFv|>1c?hTqeVu@%@9+_'
    b'(!`B#aM59Nyx@6865)tRRD_Rja+5U*MD83EenJTLeZ}e^k{w`8;WR2dV$SQPz;uubv2jrw18h-cv?vI<(&&L3x^LEx7qYW+pwBNR*W{X9lWTHKuE{mICfDSe'
    b'T$B4hR_>S$+_QscLt6U$v{@V?@Z||JIYu@{`5QPocI6STUpyrC|GoQe{<jw~|NQuekH35K?#;)?f17>#?vH<d`|$oZ?;pPX)8ofa9u`YYj}kc4X@xES@B|A)'
    b')}ojT?eqr>PfV*OqE*vns}4Ql`RvSqX8b3Ra?8ikgc7eO9wJbDKc#>Y-?N-R<ILg{&^TVQsR1ZHbmNQ<{L|d37bm>@pRv?u3j#k>@C}{Q{>&-!^CsVaee=if'
    b'ub+L1)5P5?-ZXLd>X)YpEW9zT+K5(d#L1U8`=X~`^!$sSfYCEBdJ0C*!JtX_pjj9<4d2#%sn4B0FU`dLlGWdPRSI}T<7WiGk?<!5^5V}%iC{~?uKc{Bn2F$T'
    b'c+i494R`b!N)x`%L2nYhR0QS<tQL50pw0BN5jNsS*o>cyGJcGWKzB#95}TPuEbq|QpD?$dFqfY&cb_m<pD;I{Fc+UN_nt7<o-ntbFqfV%cb;B39SEEoEmtlN'
    b'0R&IWO%XSKI6yRax$ZRj`U&h-(sn7S0OXFp86lSeCWL*}ycyBmJi=`g=AM&u<OvWCUczCx9U|l|l3cWi2)UpuP7=QrA-5r}Z;IG9{vHeLdee5hDFfmcaJi|='
    b'?RIE@eu22!1iRU!Jq|FiSG}O;#%<In*P2YMi8Zk%*2J1v6Ki5ktcf+TCicIf*dZIU!Pk{W-&Vq1R{DF7ZC!OL>X(jH?Y>-ez$xG-H2PTX&y)nC(sA}oG<&8K'
    b'dyYI@$vV=EJ<yCj&Wt_Gj6KSXJ;;nb#tb>ce8>@I)B)xjI==jQQ{!jNv477UqC>8^vgU-lS3jE*ps047JsZuQ4K~Nxt=(IgXYJN5eXg}zyTDt!pEpfj`L2@x'
    b'yWdr+l(#S{=Vgz|cvq=1>_vFjqf*{gs`y8b7zl!)81E`o%DYOHfS|mqR2lCoRXl+-`f}b?s`z)6D&t+HN_khQ!rxV@_O6n>t7Pvg-PyZJn^=2S$=+3ZDc9ar'
    b'dWvIvSLsQzy{mL*?<&2R?d)BpO|ZSIv<bF%m7euIdspfCkI6N;CfDSeT$5{ZO|Ho`xhB`-{*RSw?<(yUePiz``7!S*`JL}7RpPr!mHDnxj?DLlD)Awu%2aGN'
    b'qn*M2lz2OXeObJn!Tv<x+Zk-i%SnFN%SnFc%Sn~^a#Cf!oP?ZSfBvFSB|eo@nTm~`UhQq9TbW|*ZKOk{S$i9a`!<pv@ivnG``<>Y@aHHh<87phe;cWy<rCgU'
    b's)V<ZDgl9gdju^W|D;f5yp2=|ZzEOs+ej7vHd4hC2qP^1ZKR5S8>!;oMyl|)kt+Ocq-t*?+1p6=Hj=%KWN#zc+en*SdmG8#MmiB}ZzI{;NYCQe-bS*wk)Fx5'
    b'w~_AbZKRh!Cf3B7SQBevO{|GEu_o5UnphM2-%zZ*jkHVh?zfTrkhhWizPFKp=X_s2hE#cvAywWxL1+UengP>^0qymppGmjZk1j~J*N<KXyuE%j+*zMD`F++b'
    b'y6g2L=w(#aB=EE6jw<gZAhZD+&43Lyi`w1VTbN1hZY_N_wY#;v_l^9J_l?5e`M#0+A`srBz*Fji!M|_h5byQ<++OhaHDJb~c%Bf#aGw)g{^ETjd<U8Es!W8i'
    b'0-FnOErzjvKKe$^T$1rad}fTlkuv^f_}FOg8`=9t_P)`by>GOMwfBweeWRCh?R}%CIJWnVo+R7*MtAnU(Tmy6-Z$C=+xteFV0+)_S>Lnwjh_FQT$5{ZO|Ho`'
    b'xhB`-np~4>a!v04Sh@DT(QeT<_P$XV^S)8o^}Z40w8EBuIDOxU#aa||aeDsac#i_%6-`8=ri(_k^Vy#gZ|Acwi?{RHp9p+ApG|rDC=7f1DC~Os2s(1Vc>9RO'
    b'qEEdq9}L1P+K5JNys6jTMY@&g*WN`sWD2%-k+|<7g%R%}g}?V*B*fVLGXnlyB+!k9=dX4^Ed{&o^NM07g1_NG3-&bJ(a)a~0wbWeh+ZlJeisScB_?=}nBb#0'
    b'@><V}5isK?ql_P8!S5nrmDtQ=?;_c|NcJw0y^Cb;BH6o0_Ab(Mx7oW$_Ab)%wSv8iWbYz9muv4L*}F(DdYrwBwEmb_6Ki5ktcf+TCf3B7SQBevP3(U|vGy*~'
    b'F3G#!MG8aSMGAY~MIxR7K7Az#c_{a1ItJEzLTqy;nmN;nIql7)pGmhjlP*ZNH<MllyuFz;+*zMDF@DwzyW`Cy>IGNUlyLXzXHx>{ts%BK8_k>zHpAL|-CLMt'
    b'?Y=I3rnURJy!VuT>7LNb`S$*&hqsR(KR(K+bpQLG-n@JK=6CNOet7)mf6W`=?|$?4&yV-7`@ksYZNBh9e)nS5zmj+K<o|XTPpi&id(-*``@=W?{_y^XfBMUh'
    b'@BgY&i~RRl2Hli5sacP#UzVymE}DJ#=C|KJy#Myc+1ny`TIR*9r{9ZPWhXt=AAj|AH^u#Lzn`1+<DYf;@WbPW?`44g+x<Vi`}p|B_YZG>_c$Bj{hROp`1qTL'
    b'KhDnn<G(+?eftmZzWe>`<bQpfhw~4=efW>rXrJ2RyDz-nes%IVp9fxl)eYhbTwVj@0W~a2rUBKYg=|qgPcLdPV`d}Lg64&eBqz?)$_!GvdgO>X3|Pp6OseEj'
    b'h6vPgJ4CWc9oeFeH>S}n`eNKB1kH<an@@CXqdIa&%#k}6hRB_q92ZB6(8GX^8!tJMJH(X8Gt)$#nI`raI<d#li5sG<h+*54#-r~*=^Ie?{*%35B5#-I%R>6f'
    b'm%S=vFDl4u3ihg=Jp-~QK>7p`$h|L+hnK+Z?19@E0yj1Tx9f#NmP(P6S$+Z*_EM>k))L`39MhbUvz>n7KjL6r$V)Q?I<g1xyUiC0PFx2%E{?sqZIQedBmy;o'
    b'R>{jVhJxV$gRbeNO5Ti-?0G<k&>qhOMskNJ+yLb+Vu)+B1xH(B2d*{45ymX!%u?Yd&LZdQ=85x2i|d1onIo6ST3K@!*5rjQbJBZm%*O3`6kMhrblrfwk75gu'
    b'_m%1dSjZM7@pz|BS02@z2ZRgpvqNTocgW-q51IVsA(KBnWb(I%%>4|P$sZq9U}4V?g*!tK*Yla2Y|V${k{kDHP9<gvHuaeOp|X2?BX__?Ouo##=(!OS6Is8+'
    b'_1`f(o;^clr9_^OFw6<5kv|tV?$^f3N-;fGZz8+Tk$Dq$xaM`g$lh{B^3l4;J?f_Z<8{AC-f%|p2A-`S@n}INf9pR<8L)uN!v)WC6ikCga>!6WL~K(akyqIU'
    b'r31+pjfu?jWP`@U9n`pqNphNyod%_Ur*7QyFO_?`r*T7t{SB~@Lz9@`C1>lH$*d<D&vnP}3bmi}PG%9)SnH_5JLSeqdXjT=<P;q@W44Z%v`As5li1n0qj-)Q'
    b'DzsisO$9Etq&kkf*&=3;$Ok<e7st-Wv3Xo`5>p*dBPK7=!Q#0urpP=pyYWazW?%5|Q|t?a5`m;Mp336~4CzSe3v*6n{U)yai0Tz`xD<AOFWmSf<!+yNqy*p#'
    b'ATMHKI)X<xD6>m6a+he_E)m&likP?tjp+!3GFQEg2_(;g<T-*oVzXx?_JB>EkjSGad+;QWouo|Nsq1*d7=4^(J%P~QAmpY)96250xSMxJ-b_34X4)OInU3u4'
    b'P`L3zTevv(=GKunw~oBIbw_P(E4xduH=CZUAZ@|q*t=;*-rYL(?$)t)w~o8Jb==*p<L+)9d3Wo`yIaTI-8$~>){%F&j=Q^c%-yXc?`|D=cYCs1A+A1MA_G}9'
    b'&e)F!vtLJMKmSaA8=3qx^4j59_0&$&1tjk=)$`QclBe5}nu+w}b4#9lY{_$v^?2?fDefDr<R@6UFR+pyU?o3K%6^@c{5UE3ZBp{Xo!oajpEeAUxnLpIXWW7_'
    b'a@X&4{R(wG&HG;D$%ijJ_w1#oKDBkqBTfzMuWyyy+u6Lv?d^>_n6WO;Z#;6cg_f!I<S&_?d@R^=PX&8wVa-z>aj<UGbv*Agv?qTR_S~=Do?3VEl*fzCc*wyo'
    b';<p>e{#eASlz5t#;PH3{^#?=@uP)>1$A-pDLDovmyfpSnNG33H`yZW0H)tg*$mTWf0LrSwaJr;mpK9YBjH2c~`M5&;I$Wq<+NpU~ZrYQa)Fmfb$vIa3*;Vop'
    b'5HhZDdwF9HVbts@H`z%}<&smY+)O7qk4w(0lGCc(tSULF%FS_-Gq~i8DmkIbK6oF=sj5OvRZ%k?>_i7S@4&}3YOGL`9M5tbUk~Tq|KZ`=#}D^k-hK6IdVS|!'
    b'-$55&ulm;mG-D3;fM(2wiUh`NtAu9Eu?5{t^thV+QP7NnwpEn=0qygzn#2{B;bvnsIAk`~M6gzeI0vV6bv)cF4&4<yB*P8n=I-7X9S%Hpbxi^uGY>3+0%N+t'
    b'3LZ1B%iJ8%eu86spXnVQ(-$oskMZ4b_<ob|MhlD4CiryO*GK`qpu|JE#R8rZbv(mcOehnY())kG56#{E(0$)4pLA$OV|v$5aEur%Q;a5<g2!~<RJhT)-5NXs'
    b'93Ima&ouP--zXMq@U^-4#lvG+R+)1w2k_ABbeVz1%m(WyFh&gK@tC}56Y!V-Ujm9I-DnYyiEyKJO(YDkTc`dMj~Fe%XEZ_Kx3z*w_)(y1Q}CFA59oD?R`Hk$'
    b'H(HkDZ>VTU{}vRm>wqNr-#DQmae^DHFEo0-F*-OVb__Um;w0k;c7LbzPk>;X72VXvfTqL%59Y2&PXxvY$HWM?nWQv(L?<|=e~d*Nt?H&WW;iC!oil>B=tXx='
    b';E_fQ=J7`Jnmvsbj)@f>(BA2OBQ`iDHn`EcCVjt=CO9TdaHGl2sejdWa7=P|qZM7#f(M(9iFl*Q1l<ki;g~d!1PMEP$^<=6YbnApiD0y(LuX2GOd=Sq>0pyG'
    b'9@963*zPHs^uea$F%@pKzOn5)!i1d&@}zrcG^TIW@Y-~Pbriv9qLIgA<`FsvxY7D#fIY}AAt3$%W76WA2%kL#g*TdDG9Huh0i86`z)OyfNda%PqHBQ+PIAt('
    b'XGeiCeUcUw7*ln(M!<BVl?je16MQ)+?w^fT92`>|+-O}BSrQgFCKb5R$~-}reg-|lmxF==W121p!I*Bajv`>hXbF$$Ux_l@H-f_Uo49=M0AotkZ$xNJH&~@;'
    b'BdCnW%<Hs*-`~{!zYad8Wjv;j038L!bc1yi0V5m3fXB=MjV+iUzL7{HVDJ+`?FQ?2tP*^L78Dq>e8mT2y1_b%fDxl*JZ2uDD|WuAeLR~d=?324bWJKAQ}kmo'
    b'7}E{bQ3Q+_&A~Bk?w-x#1G;My;Db#^p)pwp8!)CWrymFy@eg6JDe!>qT~mS@yD99Sh-4JNVp`I#QDBT1EK!Umn2g6{_$R!si5SkqG0nq`CcEf9LKpbrwxht9'
    b'R&|}$@Ei8VF`8f+9@F59+pdYEAQ~Ri;6`&(Kc+fKH3`ok^~2XwV37Jf+$l0hQA`LXrOi)~K@y!ZgVZnOO@%=!ct54(K$)8=oa1`&e>Z_Iet11o=G+A5IH}Qs'
    b'wp`R>We!}VMUCbNmMeO)%z-cIc8=4_GuZK4j>+}Vb`j2TQWOGRddQ`1LZXnwNtr;B8`Z8bNCm%e=%;^lU~O>D%;;Ky$GW6PGaR_Ej*h1dKdAPT89ELHILAr3'
    b'AaEI%ezehfseT4Nb{6y;C7R><16DaOKw>otsm~EU5r#S;$xw$LzLg|(Hy9+X@R9JLw}b`SPj!nuG)bzjR0c^5*J#%3By>>`A%#8z1_vL<Wm*q}QBTHkG$?GH'
    b'2~1M61(Hfa124N&8>s{du9xA$y21<KQM}*#6B?Q%OE0B?L6e^JWpEbDRRXBum;2%#F&(<fsl<U)Qa~5D(2-6G>rRXr-4RG}o6*rEHJoEvPf4CZ@`P1N++q(s'
    b'T_`CMtQW&N>P56p0tp0?j7E{6lTH_fMN;c!1}Wp`!9^Xx6$YsgtQWV4K+l9qY7Fc3wMxGQ<<dkTrHPP$7m|MEb_|ltgxH9X%N7amrIJ@CffaJet$~Mjl92SX'
    b'ePNK~fdfw<$@f}x;5EJJ!{99A5ZZL|oJJ(%cZDSR-HD--jCkl#T&*{W39$i@^r{Slqu~HI-KJ3{<lyCdAef}zm;xSD{qjKzZ94g|snJjwq)PbsBP99w;}|4;'
    b'M<~MMVTtfc09Cw3F11yq%=jQ9I5;V+AI>siY*ieEq}Fo;Qg)27X#2n!9D$^dGk{6*fllTOaA~B46bbtaA?Xp?%phekA@<l()tfdhCpgFDgg?<(MH%@8zS2?j'
    b'hA*1q@^bAC4-#!EgVcv1`Bn!X9NIcK<iH^H0k1fQ^_-XxA9@-V1-yeUVU0aFNglxr1d<vqvaF}1#30FIb>Jzm^dYZEM1ZfENlz*Skk^~~XpUH|c>+i~Y&Tt<'
    b';FGP=z@YA*N>E6wCc%JK$gkZ9T#%@*A_Z2_@A3L&$%+Q4)jY>^3n&mk0l(Z|25#v{;1ym?TY#fUV!cElso^rqdP*t`k|<UQ*3-$N5h6mJ)d=e@^%G@I4>aoq'
    b'!dg;Elqlb(TX1zLr;7(qAW6>^9GaxVcw*?}H=R6#M3~%{h)9GHR!Nm$y%yGk7U<-zkR-W_&Plbf=A;^f)FS>=M=v^48i%9dfG*qBK}|-Y49{09EaS6LG7q9b'
    b'Vzo>m_1@Ylqa&5IBV`6j1_yL<S4fhCZxtUA8sm`=dg3OuN*dpSYlM8Y;=m6mN+l=3p>^tpQyjy3Lh|Tiu1a$F9Q<OqgpcxtR0-D8Vq2k;Jf7tHSxpbG!Pb@n'
    b'RUTfitO=z50_XLl-j<X8l<_3rk3it9mzQd9_=pg7B+AhRgQlhQmIv1oTY{kyB0`GMIO(|!Px8{Kz=g|}Vq!h^z-5Efa2gTldYWOW;NsCm#iT1~M4*d`)umn)'
    b'e1vt<mHGk+T;OS`%qLME@gy%%jvkHVqP%opbkFT1FN2>$*Yrut0dfzoh$LYrB=GzsXHbJ!ui{BwIu*JkgcPk(6BazlQ$|?1D6iHFc#@Z%i>|04Rr-375bqtH'
    b'<h>(|uyR@1Ge)Bz6Go46bj>*_TGgvhcpva2?*m~p(qbBs5anvPiDA9ER5kEE;z`~|LeG^V4ZW&?M_24q!zF_CVp*yhz<aJ5&J(Ps_X_$53%|xEu_w+#pN@CS'
    b'B^~&RB`btrJ-Pp=CM<Z;3?ZzR<*>h|bPAs2C+Sq^Y))M6>3HApB<~v`^C923`h5wHu42_mUKSJRi+pmJsh`95=!%h@G(-9?@H#@Sv`DC<qg;ZaU$}%vgj{*+'
    b'CvH8uu9<XNU0I^f?bYQZrw<8F@<9|spAam|2|;+2tKkB}dSN+v=0m}gd?<t{*MoGG5D{v)Ot7AuU@44QLq6ro$`W0FPNt?wNR2>}T@839)Q|gW!ipz(+3W`N'
    b'nUA!7IR;lPT|N;e1}U#!B;lmEexrty!g^{UIs&N|N%axkpUV0*oI;X>Sj5im`awv(6N0OjDk)0OMV~in>z8A2h0n!snP5E~_hgJHU_XUz+(VPLFDPh|7*23-'
    b'l3%~@$4Vf@N*H0~<B4|PL?A`^1ztz!$H?Au!DalE)GHwRg!WTgzZ`>aH7KcHYw#%$MkDFD;DT!U=}B;Kl3TxYp-GyvbPSSTzwpDOT*A%~Mp*eE<QSuokfL;|'
    b'M2K>Y2=Lm-hb_v{q_}<!hm+j;J(puWAr%5CNzVoMCz+ZQ#~>xfOsKKf$B5Jjq|_J@k=C!_@X<&NN3mX6zlMVgekv*VaSvRwQq|F=SRjykDQ~#--1apbZ9O5$'
    b'fdcdnKt9}QN+%FVQT&A70l4*Rcn$=Td}T#vbM!-l^xQ}w^-HrJT-Rv%aM#E3oC%~XoeDfZ>FLKxh;j`EPlyQVO7b;4R{|+lLeJHYk$ra0jX>&UMm_iv`tor<'
    b'Frr)xR~Xid>(_8_C0HfNVHR|h>&N}fhzK#<#IWA>H5@)`$nekuu%Jg+zkUrbfj}yOF%!1+YdG9`VmME*o>U8vqYL2LXZk5uacGiXzZ|1UVmQIUNirHq>@^0d'
    b'2Ozj2tdeRUVZn7x7m`FoCB&YDMFo!$F|4tNCdsKf!J$cNI0mW4wLhU_Pe>AbH8DtH!ptCLLVuD|s&dW}Tm^I?^>Ghe^HE8yk9*BAND_NsKglW8%IHr@a)kLw'
    b'NfROVl++l03ag*cu_q*nJ#e+Ph17?nmKdbO@KfHRoI<J$>*dXQ43f@-=qTStSoEyXo@R~8AW1|t2B{H7BRzZ;2|5W$b;9~7Ow$&7jX|1q3gG&CLJAXM)>w3k'
    b'jM$6IX=1eXgtS<%5%NYo#}dF5uYw%RFA-0YL$`v%liYH~7jM0|u3<|fkcx~E2~P_BBzpi?`ddgDzt;%UHoMnGAXV{G#goD$QQjCN!rnc&Y1^q$NE0E--LynG'
    b'JR+1t$mRs+mi`2fJ?EC#3*Z`PN|IyJ=#`~fuM&1OayVL-%#}duI-&ifmv@plD-hO3vW@_g<f4nNjo>7=+^d0Guiv5wj<Jq#aT{S1gVc3$44wL6%iz#DmDNvh'
    b'oyw+DWss!jHU_ET{iFwp`|UBbPC{CA0{h8N>+C*JNIfFJH3gN_ue=0s{k?_c39B$4w!KDXkQn2hkYwD0M?_d70v_dY?N9L7i)-xp#2_WY4nRnb(4X}3P9*GV'
    b'grqvb{gk(ea14@+u!TYDQ@pPXQpNY&<$@nUCm}65q5ag>h=9);ZCfoj2C31kSMWV|DSkkR2wf=qLhw`AR$=HdLP_0v;0kg|3XU*qs7{G7?v>>xFxq-LxT^Kg'
    b'BWzo40;Bz;h7&)*W3P9mepe`ft4!)=PsK&T$y>#Nzq`vNtCAQbf%IhyxN_z~Dul1Ba(hfp=a<SL$ylE85wS#hVUP-5rzOAzR|%){6^D+9ww%t#lLXQTq&O{O'
    b'1iU}RX}fWd38a2HKY%O9srBR(5PXbiTYsXE7}k@|Y5fLIh=f~y3ohW-Mv6m|#BjkgNTN<6e7%e7*E{$+B5tR(&~vWnBy(;|gmt<0CkiRyttW+S7M(Kw3;%-4'
    b'gi{Ohg&$24!|Aw(CY3cJVr7sj;cIx@zJ|lcy|SKKK=)j^Fso5s39%=Bg6q^)61d`(lJsm&C6F8?%G(;{=(?j)l&n{fL;FbsTt`^6PSa9B4jmC{ILC-`If2%z'
    b'Lxn`RSuZ#^Nw4n*0xA2YS^%09B<xaOUV`gcE+oRudLik}`kEM|Bqjut`rs;`9KiKq7ZTwvtB~|AYl{q$L^*h;CSOqG+b29C+R}6JQQp>@z>Ps_i4f(wgeZjA'
    b'%j+FU_`T1(-un!hLDB^hc<(L`$n*-QXr1(Ospy3Eldg?=lxM;^Lf1xcQe4-2a8g?8!=gz+!;Y~w%In$)K5OJ{y_Xp}X_TXN%B!E?I^|8L!XWkaUakyM#rtU~'
    b'*qZS=`NePyKlN2uuW%ZQV~`wUZS=H;Wmr#kHQ-9Lp%(&G>!HU8A!Wu`E+pN%R|csPqP!QO)&7KzJt0Z#Wrj|&vMiBdy@>Bm`sjd+uqEP2suSE#X&ocrqfy#s'
    b'jm#kRIkyxBso=*5Ehw(jVZoCYozQ-&>#PAEVe1y<g+VHWRhU|@;AeMzNFft+(f}6{+)qzy*vKIDu^e6bMM#x0!nSRMMbEi)c_9LAJ)PJqAtLm_3&u>Sh7&)b'
    b'tyi~`x0R7e6damVw@f0Mq=xehox*bR7XC%Du3seKnZ&wf5^E%oY9yTTm0*ytppfJ&Hr#rCd7UJ{zuvj6KP7x-e!+oB@~n&C(AJYq+e^UXBO<T;DKT_PjLdx9'
    b'GV`_IBVvj2$RH7P3bn4W2lrFmzMxbFNfc`g>or2`$-|D4dPBc)ARkXeC-fH-c??WLz2Hg92-|-3^>EbvA0EDa{N{&;kB{%)JiPsI|K;6R6HuS+#~=nVh(Qcu'
    b'5Q7-RAO<mrK@4ILgBZjh1~G_13}O(27{nk3F^EA7Vi1EE#2^MSh(Qcu5Q7-RAO<mrK@4ILgBZjh1~G_13}O(27{nk3F^EA7Vi1EE#2^MSh(Qcu5Q7-RAO<mr'
    b'K@4ILgBZjh1~G_13}O(27{nk3F^EA7Vi1EE#2^MSh(Qcu5Q7-RAO<mrK@4ILgBZjh1~G_13}O(27{nk3F^EA7Vi1EE#2^MSh(Qcu5Q7-RAO<mrK@4ILgBZjh'
    b'1~G_13}O(27{nk3F^EA7Vi1EE#2^MSh(Qcu5Q7-RAO<mrK@4ILgBZjh1~G_13}O(27{nk3F^EA7Vi1EE#2^MSh(Qcu5Q7-RAO<mrK@4ILgBZjh1~G_13}O(2'
    b'7{nk3F^EA7Vi1EE#2^MSh(Qcu5Q7-RAO<mrK@4ILgBZjh1~G_13}O(27{nk3F^EA7Vi1EE#2^MSh(Qcu5Q7-RAO<mrK@4ILgBZjh1~G_13}O(27{nk3F^EA7'
    b'Vi1EE#2^MSh(Qcu5Q7-RAO<mrK@4ILgG^r!r`-SW@bU5en}@geUjlTv|Lgzx=G(`&Z$He^Qyee;KfihV_?Jf!|JASE7yk9#uct4j^!jf79pqPjedoTIV*l;r'
    b'xBvRTE;Q!;w{L&^@c7;D-adT%-Q(kTzj=K7aR&VD{x6U3Kfd|)QE0DbkZV(lxztu;5VB7Kt^QX#RqfKJ+SZ?XB0Y|fo=V)rpGXfQq_@;!3f@gFmC=@&J(+lx'
    b'8ElwSrw(rUX*>=N$5WR=Jv!JdQ;E6xoPC+{X}E+b#_DQrZH#YSaB(WWmUzmUjTT#IDd#czG#^_^skt&f{7<z2D)HPYIG>!@YIJ{d#mAVY=z||WhPtV_>T;PW'
    b'Zv5<W+IDEuN6(9SmYRBerc<k@?eE77)w$$p4xBk6(`h%$vBo%sP{;Iyoa0nOb1}V`&9)wr#_I!A=ec`;-g#~{oYCf9QbG<f`xnk}EyPf!klYw`T8g3hdHnN$'
    b'G5tgfk`lw`r8F-=`tqZl&f>lXpW+-3&JCLXs-G?5V>(?Jd)K2X%)Mt!KWT_9!*d&vOa!&iXal8Xd2zaM%7X`u^faWN&QMPy@EFdSg>8Bo8^`MdROiV#K;L|N'
    b'-8tN3t>(EW%-!yEIA8xdv_YQ9AxA%t?=Pl}r@tSr4oMrFGTG1af}7%t<V5V_WXIGpMx8S6mSUR&E&=BB6D>$e4A-IfdAU$(K6S*bRjI9%QJpbQvzfA=S2{1U'
    b'QO!@?j;@YcVNap97N-|0`FWz8HT89hZMfM;RwEe=XS35TSf}-8%!+8<NavJO_2G1{Uc3w0&GXuz%~h=PvdhhrZabY<%HZAAi9R@WPKK1xJ~^=!(o}hl)p?8M'
    b'PD5-So!c~<YyO8Z>YPavWH+zCN{%Vy@%oU|L247{?a=(=Plx^#QgklQOU^NaWt`W>wZv&2%w8<`+`LLIrL{6%ACfvaZRT}FnWG@3mnpV+vl^!sN*uG!h<=`5'
    b'=E!R8g?D<Ow;bXitIgZ*dBkkBIlzMN#8@O-aZEMZQpwkrODZ*;hE>S9&Gw7c4^m=ggw%rbFTSBZ{rz}-Na_H!dHTe2VzoB^KS~Jm+BQPhWPRa04{t5G2wjua'
    b'*)Q|1)%jSEYqHVmoVW+)oinSm(MF3U)XA5*-KQzCK|RLz&s_7C$U&q(Z#%T<!-WUm<|t|{o!VvIN=~)TdsjbZi9e5i^2H~<80hopb;@&nNb2CU3AJRGry5_J'
    b'Q%JRxo>K~L%-TDgS#{;P<JTNrYGa};Jf#X=q}#X5!Whm|=Hry}lqebRACh}W-XS>$=bJcFf~$QRJYC|K=KDF5DZB9;9Omg`{Ye*X(>4uP<QK6v`OxOSPxJC+'
    b'@YkJm%9$6iy-TH0-$Oq6MQpe_C+-1y=egB@M%yw=r+sJMRZjg&k_!czDQk81j1RN6alAexb#U68TeHpUo95h9TxrlXTaW5_5bxt2a?J)+2d7Qg&Q_EciT~{='
    b'#;Dmkw3ho$6R@Ls(&B~mI=dsslH#C+G@|X#ErT;mIsH~K*t^f|4>kXA1I<%yUoX1+;_FA9H_4$VsN8rC4pYvoQ{23ANUl2Q3D)LjHRiw1c~Hve%n8=!2Iq`E'
    b'eS&qkI_1;Lp~1fS<g7m2WS>5V)Xxa^?D4FrL!LvLT{CZ3=M`)L9IGN}161bI-zM9X=b)&eM<Mdt<ZQOFYm`rao5ZSv)8<T;tWD1QISz6jbpGW`R;kT<h?YXh'
    b'z6E5KY~HiB?54SA4cg^BrIk*PB(_-Qv2$K5Pac>h!@7s$9g=f^zB#j6Yi>5=JhJ9Nhq}(J)<$DaJB&wO7Hn?b*rzGaqg+5<7DQ-)Q{tpgc;LmrQNllcYiPF1'
    b'G;bg0K0WFn=yu^I0G#{jTSHhSM(c3qtoQ77mrGyD4O-5hIqQwkf~3S~9nPHfns+=cq<N9(2i+Pva|mmc7N7p6IcpK;g+j>51J8P4Z3Q(I&QhQLAU7`o<_$uO'
    b'{mMG<gWOn*>xb^wA3r{NQ%Tzq>l5kFq8|-V++wu!Q_BoB%uA;Z_UW0r91U4fq>V105XML2x$+5!wnLjfxaH^WQMWJ?=lNjXQ6V->5qUSe&AY&PV9vS42)sv)'
    b'FcH*3I0Jq9;@<pMZ61ldA9Z5j%!Rsn5fp<j#kEm|3qE~8u!VV>*g^@_CEUe5tkp<H!`bZ2Vg5Fcyi=aX;CUoQ9_DY}_e9c^YjMEC{8)8B+RRIv^7Osx(;qUY'
    b'F`QiUJSg`wPx(x`ERNA<)~K)N=grsX_4i9HfJ!`f3eG1dwi<1!d8kVBPBE2SM=uV0EyzAm24AZmzD#-9c4*T_xBTh)MLlyKw2a|A9hAhKOz51aBaCNGCZzHD'
    b'0M&W!9-w!gTMcKlQc}-rrdc8`OWxI)V#-r->BUgu$7?}SV)(oi`>-<a@~4Q~6UzLz9W=x3-#P~{sGrz~WFn}AMjNQD%ZoF&I>!te?P*BG-6ZIoGYi|HhvHxA'
    b'161e9IY8fhdfhqPWKYMv&KznR<eBZb7w$~kOLaKf;FPKTi*c^~lP>OiYgfn5yQS1GD<{C5exe0QiQzi<d4J}-dwDcqWU{Gao(@9cQfH#hb`lDg3VdNUlGR8?'
    b'gW2pw$*ZlD`<Mk$n++91bR{=j8HZVk$<3>-eyMNDxH1ke^}(rga*brHOHNINv{Welut0fn-+Jf;yROcslLTXL*uB(;qz+P>G;fCHpAvAV*Sk8|1?N-qt>8|t'
    b'zto4M4osUq==ahdF*e|7tIjF?PR5j`7hldsp7QCKdDmTXo!t1dxG#-GvK7ZvqZgH}%)^V1-o=Rf7}u3}`b>rU823^ik~%<bo<8uLsc)X4OR}NmK`$)HhL-R='
    b'za$&1&Z&D~-Z{5A8*H>Wrn76s&+U$*Z(GY)**|i*GF6E5=WT~JeYo&kra6kHDMnnChM6-Dh%WWSL<Cl8c&QIb9h^4K`Oq)*rWdCahF(hRoKLU1#@^%VoTo$q'
    b'?#^K6Jmo!bcOYN-hvXiTcSz2``KD8HbuS+?8GXY3l!H6S|124D=9My!{2n&;ah8*BI|=vJ%-Qc@!__%)570Z$tp+sOmRZWU8uS-3WkajBzto4M4osV~Yqp`~'
    b'Lock^hSm=~zh;A~gVSc7Mf1G=n|FYSorZflw}GqMHFG?)?EzP<>!k;v4uIMpYJQ;g=c%@@7we0cCx;eMc*%ibo}GP8pM2~YdVY26W2)!RuReR`Gy~7C4p*mq'
    b'dO0-MH=mx>N1N=-DWtKF;+;Q+H1<`zv&WFI>HxL*^w-I;59OTyIyv^GoU>mivFgCIIhQ9JTjKnDUTJJq@bh`Hu|>{L5=#|VQU7e74C@|}cSz0w`sU1fZD@(o'
    b'^Xs+2m}i&BhCh6Ma^dd9I?YY4r}|PZ<2g9YiLpl8>gm?n>7Wd~aaaBLwnLjfy5&#zdI})^pDri8SfsiZ;yl0(>&4GGILwK$hL07Wz64eKgUTsR^Kj_KUrwqX'
    b'd9kYcr-I+WOHc?CK`n$c(3yJ)gF^Jo?TWFFexJSnFdXyg`wydR^~w7WV_(TWe=lL|`_<>~S&V&-``rBptkp<HgW2rdVcW4!vz|W%TO;x)@6eZD&mOkL+6rna'
    b'l%>ucwjKNK>-odBV;_D!d)OAM4osVK=T*i&(RTK{$_eJ{&*$9#;o;lI5BFc*ef4U3eK#9w-zw`>A76J1nZqLN7BcG+cMF+qJX^c$7BUYHb+?fE`mXI3GLM4$'
    b'R=7P*!ftgYQK#&V6SrHPC@$V<Sf`z5=eFln|9mW>-0s*HQG3M%vCYn#h$5z+;@WwcRpq4J4tI-<<9;!5e`CA`&R#KP@%a9}Eu!|Dcp4z3YWSu7VtUxPHb73>'
    b'J!o|?Wq;fhF>%>1rR=wipR`NuJn;3(&k^hg$dR`A0qt1^E+6;H@m)?DASVqNx~9d>Bjm&}?dhYJ&->#?+O$_rS>k8F;4ZTEwr3r|;s7}#;;?EQ`ZhpL+dsnl'
    b'W%dix&drNcf9;mj+v4`i>BDmvpqH!+M(DLH!1nsR%jtgKS>{yaguYo!1LO=?A&7kj#IwYXAE1|0y>{DqiJ#r}@oJyldS#uzb{5Kb73T4$%i1eP+ENF!r|Ene'
    b'r~Pu`+@_r;gH?_ju>P6U&U^Lha^f_mJ$-(Uet-N(oA&0rg2vBYIigb-(4M%=?{R>fxIYeK)HsZ3fSfd7{j;p=V&3m}@!4KEW%2ufb#EM@*RrnLYv;JEGvfd`'
    b'-S0cUCaRpafBn;K+-;q9j)(mmV;mu8j=?S~4Ol;mtZ9E7h5_wK%Q|zf-@Bad_Z0Wb=`U8NG(gUPbzNH4&wJxJt$t4f<fH+1UiV)k<c#oF*7Z-?`ypu_f6@Rs'
    b'(v~`)J<B>XPy6NMF2@a!;|8psv)VZikdvn|?dj{o?Dxlyv}vcD95jCNfc0~iwYxp*`fwT`XFwcwIXw<@8XzYP*vC~}ALhK@@8Yw)a?0ZO0qbXxwYNR%`p^xK'
    b'Gs5px{hr$ZIc>oDIp{jGO#A)bW$l&I5A@^#?ddOdbXj}lh;96U_AKknz5Wt81LCL4>G4zIemT9uS{a~M8L*ENpZfvraoV2U_VG*q+BuGuH4gLsb$A)j9@(3^'
    b'0eUU_?%n>Xi@(|cIRo~CT~6N*?v7`__-llm5q4huzS}-U?Xy>}I_Y}8?wsHIZM!aOuN-NMAJCql`-`2YnMF=7Qn~XOyvj)f_Jet`a~vQij%iQd@9eC8A@L(^'
    b'+AF6l@ss!O2SwK2_S9v+GYyb44T!_4aah{`Ic-2*V%g`mX}{mQti5uYQ@`((BRaVO?eWWg#|@C<_WQld>3-i?(Ng5}8%MkMgUdd5=L2oxck$U?Icf3xUOD~X'
    b'bs8Y2+a~XqBQ_pk=Vjl$*Y9n~1MH5&s&Uxb06G19%QWp5Gz;m!+z3f-|6W((FptnJExPTtcGhUzZ=<}}Xuobn2O_t#a<S~3+Xz9D266)gxoJsu>^8SZ5_^|8'
    b'KvGYf><;e5N@c)6+uJk1Mp2jeZrXdgf0F2q14L<i@{mRq-Fdj3^|(}$n`D%0LqxR!`^9N9c^x6Cj%iYrD^Jsac#>xAmgL+TPkTkFW^PEM{IWNSBLu|}ajCc7'
    b'`p~=cJ<Uaw3j?;0UbjeY_uYo>Huc|bNok9MxPK$Lh}+$$tb3)s23J98ND$;D2%IZJM3n(sN^x5s#`hkgmW{g`AV>m0BVn&3xd5i|v|E(iU7d#L*UjyRm`ZLI'
    b'_3KxAw_+lx@5SnfCe=0~$VEB5K^lkHsm}^~&wehVlGuGjcxqs!A)?X{TWv$aeg)kUp1T#4-K#b#?;r6*+U{F)y*V=C?Z1y#)^6MeNNR1wcu;ga*dGL9rZhk|'
    b'x2Ada$7NkN3VV;3x*#2|ju0gcQhB>u<<{L<@FPUY4XF@@hzditpK&$&ZUxosepstyXBFazxYDNW7M0ex+AT_TOG8?f*WJ}_v#Y2&Bt-KXqI)mREuzYh3`t&h'
    b'SfP#x26f|ZQEdx`IwB>Z^7e{~)4I#rZFUhQA-X#lM3e->-ou<KD!L&%Qn&7pq8||qB5${-7}j9eFG{LFgdw8DOmT!LwfGRT$2AeKKN#Ycp4cCvc@5E6hKQ1m'
    b'Q-_F>S`%%Es3E&tjm|hk!LTV<hIE`X#8z>&)qVxjI$ot|#D+Nz5hV>0dAmg=w|3{<W*1Rn_T3o)5hdA^{n5VJYImztR2*U}zwRc|-cdA3K{-D{lr|_1X;oVH'
    b'I4O@1m8AYz86v8T*u<%=hA60_@~~FP&MVasaivY$EvjvCRY&YnRo-4vdD?bfeuyYPB1A=$gy`NwfGR4xA-mLR-FfZ3qNvUjdAmjBum;0!QL0-Q(yF-bymp&i'
    b'MTH^35Z7SXdl+vKm4>7&(z^57dv#Hrr*7OWs%*iqTT~xFRbC#k;Z=FNTh-R>(ryptwnqE@xN2)$?Y%#!qKXu8bwfnC5xZ24gF2*DWo^}dTh+A>mLZ80Rd7gp'
    b'N964mRl*wWyUi}5%8)#RwrWU%PAsl_@iIhI8Dgt#W3u-eohyBDEb{h?65a9$QL0-R(yDC>u=k3eit3jaU7bdVk|TiC4H4yr><9f83`4fzVyoS)(vT`cY?W7A'
    b'?e?H<P`j<FAJK6{-fmGfY_{?vcBvw7f2-oU^V%H@Dk_f%1`(yfkcNm#BX+6kyfC6wDk_bzm8KYE=*uHQRD)}`s3%+P7A2!-86ir|REM;xty|08aV4Ts84~Sn'
    b'jjO%4GF4RT^I&sBM7a?=dJU;EM8U8sxZmt$jjR2(Dyyw_E2v2#(bA9TgCcLYC^_z?w%RSK4^?f5f@-EXq*ZC%(eI9S73D_6m59=~%0oo;iN2K~qJ|_=G^D}^'
    b'1yxiYV)m!FDnmq-As&p|$guZ=f*ci91?!0Pj>@Yey0glwd#i;{Yj<vCgsAR8zxM{Ei1O2jRG7A^Oe6ZB#z7mPpomfh_jjDO2E*>OVOvwI13b9y==~J-iV`V)'
    b'fT*QGV_KD#JcFO|08xIDcOS|SQDsQd>B;PQh^P^%Fmc`@Z}-sGwqU3O(mRX1IwHlY^7bkyPfuxxmI0z9uKeD27gdxSkqT1<>og>;+L}Y&-KwcAtr}n}zxKhs'
    b'Co{dgjpc@j(gwvLt=fjZy$>p?C?}%I5K(2w*zPy8j}euJwMvFQS4YH^Hf^`4w#8K)v1U+tdqw$e=-X{}6*VM8^(jet%g>Dv)o)o2m?pL<)$e}pC#)XaFG?B|'
    b'Mu?I*-VaewR~};&TvvSqf+4NJu>ZkI5!IvJmm#8tEI&k)8xrjrQgMiaVO4Oy*|)gbZ>zZ4YQKVYod<V6tQlmysv|^6gH+z`R=IU{-h1>^MFnYE7$PbRSzr0p'
    b'?7J0Iv-@GKk~Kq!BjQS%wp&zM<7&4k)h!KaRbJN&yUnhm@{kbCYl!ZCs!~OjAzOfL0lD`wsX9;HxLZ`)f?>#FI}A}UZVSlWW{=ylHVhFZ!Lau*o{EykLifMA'
    b'-qyI<{UD~iuo%XOlE*B=2vPbTd>kQ4SN}s=6}M&W{$NOJFzkMkQbqMaE0!UmhAbfC)4JV_2vH4&GDK7vV)m!~;22S3JXqKD)!wU!KFN4BM3gj0<?U|OwyaHl'
    b'gs3E<!Vpnm#IjbMS4SwQX7|HdC2P^WPnKvLXw!C!N^4xDA?tRPx4TtOYf(Q$)R+*>Yl!YWjJJp?L)Punx)$AgZBw16Zrm-ZZNV^P-LCTXiptwsbhp`6)R15h'
    b'Q4$P$k8-J~?1pUO(z>k8enc>cyxpR5Sc74|sJ><pdAmianc|REZOhu-9u!ewOkAZkuJ&G#TtxNpFAq^L57}C39K<253TvzO+bV8-aQD#n6ry#+79bC4m2R8E'
    b'2vKEA4(#@zh!PL(y{V_7%8*^EDwu~vdt5zOhKMRd%$~Pk*ljBnm4|rHue*t|cg-N@r9|FtQQDw5q*ZC%<CHu?lpLBWWr(OUViTvf8ls?z%EMYEJFikl#FaK}'
    b'x2U$oRUNTQRe5_w$tf<~dHErt{D=@0Q4*qiuh*%l>W1u6w{7^|Yn$pkk+)k^zXql9c8gNo!jM+Qb?3F)>?$e@35K`^!`>@ni>NdtWwC9;_ugt$=cyZaiz-_%'
    b'>=xArP?fh^l$fcG5TzC$V)nKr2X+TT+fo+0LsUdbi0-`xrK0-nGr#wG-6E<_6ML)gFQUSTZMa5f9igCzQU%?Rj?+fiN_7iE6m08wwfCt_-O<+}qBM0CMu=)#'
    b'PG*0IrY%JCkXGd((Z1O#4;hf9Rr_s~*WJYKn|e*6J&zEj4XQ(0)s{U@*!z^HhzkAYU)X(-O+~pOyHvlJeZPWTlqfi;Rek3bCO;ysv}rp<g()m?wZB!WTNu)+'
    b'xbD36ntc(K2ZX4Ik`N7h-}YQYr6Gxwxa_>blt%=Ex^cItvIRpPuuEO!?QT_FcV2tVuA)jA5)5?-hOqY)j73x%u}js>eD~nq_d>;a>c-uooLhrozo<TdioE@z'
    b'#7usGsKw$#%<i`2z}{e3M7a?m>f#cj!KD$R`X$1!_n`G6s!tPp&(<!YM(mxJ==4Jrben={NXH37Y~>eQ4Nx#_<5eB7cU}~%BT`{1ukKZ_E!}y5+1nbT&5dYP'
    b'b3>wiwbg)Dg{4*dZ6((>WjC?+m~QCLk&3+CqLv2vA*~AQCT{ODA1bQfW(#}Y5M4y2A-mMPnLQ2>6-Tv7cV2r>M@t+mP1`N1Y;lzb>{1tbyIWPao!2x()HEbS'
    b'>l&haZ#6EW+K@y_U3Xq#8W0RBZ?~v^K~jTZw<y)k4QZ9%c3y6XC^sS)M3e->-czh9Duf}s)UfWn_Fj-w=cyZai%MHC>=xArP?fh^l$a@x5TzC$WA-&Uus;~W'
    b'ma^C%qIC_?(1wWW3dU)KsD2+YL^nj#kiD};XC9(pS{2-H_PmDZep}_$R{Iq!>v*;IR-^8n!w^xLx^g2##jtkg-DVe2V)ot10TJbfBs0TitKF?qQE7y&WFyh<'
    b'BZj!MRdL;x#N9@pMa3b4r2mx>d%?JFmD&J766GUy@&nq_#k2tyid!7*%?vHh-z%m+KpKV!lIFA#qSCYkWE&u8ZqbPL^!Yrw5sD=@BCc0s?{3r5qB<hYmE>0#'
    b'G1&ScqT)8(?iMAwiM;)yL`oWwj!1D!N5mnb;)vi(ah*}ph*@rlt2|<;Q+azurLy(E-J)b<DMLhwnd%TxZ4J@=!O*r~a6?+v$Im>C5Y=zihCHNI{mkBgXm4vU'
    b'>{c*t3hp<1S>q}X5tWB{P!fx|hkOo0zR{EsqNES{A+5^Wl)7J3ANBH(thI=eMCI<uD{qrm8X`)@tDHu7P~&RM*giy5e(Hm}MTwL$M3m?@rd4eX(fz@&O<udl'
    b'tGtcvdmn&MQT@JeC_`FR+>mJBf?>CUBB~6TQZ+j35L=biR%OVHBi|kNzOkzvN964m)gQ)HdHY56QB>sZ7Nus2Lt2&Aj|ICYuaefuYj?*fX&tY2A6G6arT;2J'
    b'M3oWWXfzJukXD7YRb|ZNCDFb&Wg&-Cb&#n;6l^0zscvC}s5)&S>PCo?QM3*bCC5s42ZOdMkLb=C2W^CcB1#o>BSKVzArBFiM<^(Rf(-E0kN6@f^6HQoN964m'
    b'B_~Ql7%}wKZRp$m$yHl5<cNrRFpX%HifU@BuRmYb{U08_ef;K!hmVi%-#oniaR24qS8h*>wjYyXQcQ|TF)1d+q?i<wVp2?sNiiuV#iW=NlVVa#ib*jkCdH(f'
    b'6q907Oo~Y{DJI3Fm=u#@QcQ|TF)1d+q?i<wVp2?sNiiuV#iW=NlVVa#ib*jkCdH(f6q907Oo~Y{DJI3Fm=u#@QcQ|TF)1d+q?i<wVp2?sNiiuV#iW=NlVVa#'
    b'ib*jkCdH(f6q907Oo~Y{DJI3Fm=u#@QcQ|TF)1d+q?i<wVp2?sNiiuV#iW=NlVVa#ib*jkCdH(f6q907Oo~Y{DJI3Fm=u#@QcQ|TF)1d+q?i<wVp2?sNiiuV'
    b'#iW=NlVVa#ib*jkCdH(f6q907Oo~Y{DJI3Fm=u#@QcQ|TF)1d+q?i<wVp2?sNiiuV#iW=NlVVa#ib*jkCdH(f6q907Oo~Y{DJI3Fm=u#@QcQ|TF)1d+q?i<w'
    b'Vp2?sNiiuV#iaZ<mGbrHi@E>d;p5}`HxF;`zx;bzasSu<^Ub%9Z{L3C|9K66hk*b5=I!HO9!0=czn;GEDZRdvKfeC2|9UCz{-=kxj~_oi_J8-){cpd2{Ps^j'
    b'{`uo?AO7RbyT^~;{I5TMeEjY=Z~y%GkMAG<djI<F)%1mHBCPb^;q{&SRsV+~|K~LS^Q-&cz4_1izj=K7@tfa%|M33XA7?wre>i1n##Ho=y8gE{>VNxnZ`=KE'
    b'AKrhQ+w!;jA09t^|M)@v@!uYPdVK%*-M{?w`0n3+{OO+`K7M@j?c;AAKK$wN<G;W8`2D{=KD_<M_iw)Y_c!mp`|<zR|Ku-^@B6<bCV16t5Nmt>Gq-pC+vw8t'
    b'{6|`nel;X=e*UBFnDTA3!^M(ADJ}VuQeE0H1tCw)W8tk%!Nr!R>|1k{3%@=R&@H(>7SJuZ6b&vM7!7dv)zOe|B^dH?v5@_NBLg0OeJq5V35IZBG=u|320Z-g'
    b'XejYUf&tx-3$ak*fg=MRetj&YTNxSPEx8m8>A;Zz55GDZYQB+RKsV$<EYy79$bg4m9}DGHMh19GE=5B*aAbhP(-fyze2i0zvDP4PuZfT3usizHrqDu}rcz6s'
    b'T%ocr>FvvLdZXDF^v>Zpf5X|A^p3~*8_vF<_dL`crZ=2@N$-4|zv1i)de?HCzv1jlde`Ip4QD%7otu2f-p>Y5bXqcz;JjOEHO>uaxu$M_#D!l_+}8sYhr`b+'
    b'p2LA2$HOlu9uM?59)4c&k`DAZ9)3abe4xki@bik-a-hfY@C%C913eCh=gH~H#nswM7PfQoBvm8l7*fEtqb;kLRAQaNaqYO;9?{>3LE?=>NKUt55Oh1Pwnx5^'
    b'2!S``T8or&8wNqQ<7#`<8;Ou|E3-^(w_y-;JFc}yn{FgR;0>8-P1Wa8Tu#dx$W7tolZ?~(-=R&ix<x+B9NChqZ4$$+*aY5^Yi*L#t;7kwC0E-d-%6a|TXL;U'
    b'=6~TvY=Upe)i$ZO5-0eUTx*lsZY56eExFbvZMu~>VYI|WSAzF7#2ob|M$k{^5xe0m?IbysiRepOr*fFqsT`$s&WHIr=fixR%VECG<uG5DdYG@#=u29+!+ecK'
    b'U(mWuhxr<fzNED~%-3-AlxD+jpLO)sWh^>rg7cxJHSf01I$ZPxwNpJzZ8-Y8+BqNQZ9Mvd+T}2B<I(5UF7+^P<Ixw?Zijgrk3O$<n-23f9(_S=cbK;c==5yE'
    b'?`5svs&4zRH*;!RK7#0#2p;&7%Eh0gI*u{`vl$o6k<00ase{ZxZN?>YG=G!@+F_$WJxJwxn8NNTFQds9ly2@OdOEckm&_5|O_+n)jLGY@NLdDXX@;&vQigYl'
    b'<x-@sf~e^8TBEOIUeFqjKC5-Ehxr<hKCg8<%-4AIS*`1In6L5Z^IE&Ze2qt+)w=n^e2qt+*E$^LYXaJ@*C+aQNLe?8aC($5>uiGk;L+N4m!jW|Oouh(dW(QB'
    b'YhG^=a6_)PNN$Ojak$z%)K*<>t1^`vv=y~gSKF$(8yS1h4Y}ST{zk?gbVIJTNDDU-Bj|=)Z;^P5BMi4y(v0PEHuyGbAhJ#stJSkC8V=%~D4ZM5lW5k7Vr8l{'
    b'#n7x1#j4|Z49z-K%=0{kW}PV30?%V;)~RBV=P@+PMduDGus@?ydR~8lS>yf}^oGMPXb#TJUDiAwr#QNJ`7bCQ4%9px>2hpI?2C${t5W}h;^{b-qbo39)*M^w'
    b'_@d(Ia>Ku%csb7H=+e3_=JM<qL1C7+b<av6_OlF?S(@*%;@IrcWyQhEZI^spYe@G`PDd3_n%mJrnCAUp&i%^CfwdDp!z9t)icP?^6I_}%w7L1_Lg@E<3-2Q7'
    b'jDE^9wwQ=lVlHZpy-0dVYw(R2muF?49Uu?1<IFC{@T`*Fa*U00dg`Lq#52qnZGfKsb4yQ^g+e{*>$fY!EcW$EV?S`8DoxC4Uu^*9C+rhzpwr)1TY&jt`ose0'
    b'Jo(iY0DpTvQ5u~?zg}t2>-p&X`qfH<zaXC|jn2JauXH@9gTs^b!Pldb^kJ<ZkYq7U&Cy?08x6mpI66gtQSp43-tY|lWxd03iiaZ|4o=Wt&>NngzpQsU%;E6#'
    b'{6)pV>G=zK!?W|3^)81w9G;vH^Wr-`B?Ou8-d$#cm&f6GMZvid)DHs};pnw`3~5dN_PFzhW#>PmArWnoXU|rpL%$PzMpMw~`FU^ibaN+a(vXy%zk~+o$m3IL'
    b'zW30|{4{WhjZV<dee9_yTgsJ}pua?BCdtz_1FH|19||t9(My2T(l!%K#T}NQzq%dZoOz~xC^#xXf33Bt3Hr=T&|hl-YJxs96ZF?w0G*)E%mn?_N_*Zg15eOj'
    b't28=6pP32ztCfxib#Qcoev0j=1pSOYx%nTN8Twz)8xFsqIXFdsS@V3H;^-XxFDM=k)I1#Na%__RqT=W*{Vyn<j&nIWO@CQ)Y?}U};^;j6FDPD)b2&OuKP6Xx'
    b'{xlvZQ9q@V8}PL-ljWBc$F9*YD-K?>PpN+&IVpU2Orm~n$kQc;l-hCG@y{_y^fzLYh#nYHeO@)A5ubvZ*{5%XXJWSevf`;6r+7jS45cpduX7PCRX>wYDzRr`'
    b'iu|J1#Lom5Z2(^cw0iP=@UWtG6EjKvIcj6S4NOO+>p#N;%!K{KOxS;h4VWqWiJ7wh3>$!x_7gK{|2b-V-Uv|r&3GG}xSyDb`_EB39@NqCse6|WOWnI1o*hvm'
    b'r|vK64ToRQ9G<$rq<KD0aeV6jqT=B|&BKu{N2l&DD2`9vUsOCD=W=}N{*vbC)cpm;@u~ZZikIVD4o}_3@ceuuv;NIRG<cyLpO+a4J|yZ_gUfXEx;@5va-j3L'
    b'-2LaYB%+Pdw#0o;;T`xL;WL_oPT$9T@{y?$v-g+K;QV>a+qtaXNj>ws!6i02bswucIpfbu-CrUz)90~<=U1N`^Ao})cEKOnc)IH}Pshil?mwd?;B0!LendDb'
    b'b$`9Rsj2(KOx<5^18V9%F;n-~+W?)qPt4T)XQ=IY!wo!jf4$o1)O}*6?mt8Acu+@&rtXi++#i{^KQeEBWZM3~to@Nm`y+GqN2cr#%-A29us<?ie`LD;z-;}I'
    b'$@(L6^+%@akIU2_nk_%>E5V^@`kTqp-%e)yc0L!}PKy4x4E=#w^5eb@9GIRzEIWT-Qv61~3mll5znRQDGaY_29|4X^%im^Jo|%-t&73?lC4Vy+d1gZXX7cgO'
    b'bo|X^<C)3$+swtYQ}M^tzd5q}&5_k_jx2t2VC|bDOWzz>`R2&NHwV_eIkN1{kyUSwEP8Wb&6^`j-W*x+=E#CK2iCheu;R>-m3EFSc5^GWZf>T)%+1u?xtT&Y'
    b'2iCbcu+q$t6?Tp+a&uUXn;R)Jb6};N0}I^TOnsZ1sW`)|vvX8&o7=2y!z^uco0V;tg>7!8t_`!S&COJ`VHUNynVL4tk~X(l(S}*j=D4?F4}2>2$d_Udd?@z7'
    b'cVZ8GCicizVh?;I_P{q{4}2o_$QNP{d?5C~_hAow9`?xBVGn#9_Q1Dck9?l>z-MWXd>Hmt-i5uL$5?OXf!f=76!y3`VGn$l^|;q)4}1{zu=ijOe1`Q#UZOql'
    b'G1wb<3zqo=>y11+d(=a)xA+b$^BLG%d<B;I2<(l#0n2;>_C{WSWj+9VBk#X5pMSl@*I${BzxK7Ga|b2dXJSguRp%x-Hp9%gU)CDUzMwZa<$h7`e3;tkocm?9'
    b'!*P0t1Ko{Hx?fTooprygb~?=6=(PJqy|HQcOKPL@?w8drhq)V_c#pZ%`gH7;Scm2^8oM4|57)+8-Q0%C%=uqrqu1s>ZpW*ql#a@~U*C)fHb;A26zIVG|7WxW'
    b'oOVz1miQ?j=nF6Heu<3DeW&{T#C;;>`!A5eN%uS(S$dyNJb{*UzXT>`zH<!geB14xh`IkuXz+BOTUsZcdE%{yCEc%W1~w61h`IlAP}2QcQ!|t9g_v}|R)1#F'
    b'y%3Y`*Xj>Wx));7{c4pxZFE5=-LF*{oOCb5r2Ew>$74D+IO*==l%MNbj>*9LIB#g5F6}N?xj7m5&oKeGA(xDRO~-$R5%OU+0O#gE#|GgzBZONC1ZdX&q7A@V'
    b'`_HjKIxG;tDg4hc0yLk0(FWjr{^!`B92N-R<i1Z+oSvndiKpuQ^Y0mw(V`{TFKZ25@?X>%y94lfa!(%>%28Eq=4RCA7Yh!{sDFk%qQ4D;U=#a3xB9F=XXMqi'
    b'@nw3J@AaYZ^6M9shJI7Hs5CaU@8`M3J^QknSgCzqC;#+SZ>eWPNvU5{nfFoQk^#U|eQo}E-Ke9g+4#mwsegvf(9Z~`I`dNd*XvKr?VlI}oZG+N0L0|}i2=aL'
    b'{p$^Y&F-J*49@O<hR&YW>%r;$>vhKF_fK>N=l4HD=Xgx#h9~%IyNLw<$>UhAQWN~wn*iL9OGZE^_^&oXKFkL21poCm2*(*A+)5yT6Z{u!08j8=Z-aDLAixv+'
    b'R~rGG;J;u4c!K|W8<fKW0iNJ*)AM>Ag_+>Lga&8XFQ7Aa0etD(0vdfu>sSucIv(chk`D7V8huIYe3-A%=nGoca+t5t=u2AH!+ecKpVs?N)DOg$*x*dgC3Xg9'
    b'R4#m-hNCa34bG!nQac{!?UD}jHXMCP?R=QG;phu$*K(M*;pj_h*TcMxM(6hPm%ENQaC3Dt;%%5Cr<*wT18&CE*2uSU3JTqhYwc0WO_&4RjH|72BWDK7jSQu='
    b'-Gn*7&A8SYZMu!<K)0i9x4in{t^<#hUfmG<QO@fcl9RiQ!>#a!Tx}8X_rdEel5ZqN=9b=uMc@s&+9LHvVg%lhYb{dSjl>ANA=g@@O*axF=!TSbvc=BCYXcX^'
    b';IsSZ$r-(GJbPaOOunQudN*`l=W>*vOFhcZVDcrM+fjZ7lP~Dprlb4}CSTIo9pz^*`Sdku<~_3uWcX#TbL0%p>0P+t21lP)8l0-Sq;xsT)1@BfX*l}4((N!$'
    b'!_jAzZqs3&hNI6b?GE!a8a?l4HOs39NO?DP&vTjAWzV)Em(w)!L3f9l&A4EUcGTTzF!{X7^&o}oLFyiMJ046vuX1xY(ZiX|xL}OnZo(MEX4JOan9xa|SS#WJ'
    b'8D6B}966)=;n~6zaPoPbTR2MRc9fs%bd;ar<nubaqx=jfpVhhfqx=jfpVv7Y<!3axwe56kzo(H7E3R{OJHQ2Ru5Aak@XWQ1q85X>wo&K;Emyb0-$vx13z=Nq'
    b'4qkDQz$={<j;UA`c(tJduL@J(6+a5RnnQtC>L<J`s`K?Y*8LwIzJ2^~|K;6Rucp^`GYO+e7e22@989=-eV1Uu=iv`iFyvKtEmC-VeTSK^UPUoWg9&f1?=Z>6'
    b'S97!Hsmo0;>287<W^VXA3^)gq-k<qInWjiQR+#XLvrLtMbO9#a&7BprF@4p2TCw8$b`!Khe<iZJc?wW|?^PKjzqfr3d{=?;E6_f@?R{8lK=}=5pR~kh2FlMs'
    b'`(%wz?{M<{+=o4A*cabstbE_sm!Q#EWOw@{p!_+8JZKpxZJ*=cXQ2EHv`=q)-<cGk`~tL3SmHAR<wu}>=DDR8b`29we(0M|(D){{>HVt#<@YfNG=E8KMzH*f'
    b'v;Q2Pq5rSPiTAL)MUl;7h%o74_H00noN5|W>%F!fG;B)Dz|t38dcj$~?}_?B$&i8afmsY$)Aq;&uF3nGqye>Np42|D_D|Y=hf3X*B^8r^@)OYh^L!ZR_DA5F'
    b'KTfzkqpYds@eNcHNaV*ZAGBxb`G9U8RQpAKpLId<d+f-*F5u*g4+3sY75is{2$UajdzRpIO&)>r`<=Up+OuS}532nlKjZd9J$AZ}QET!pUwi;uUd28}SD^fg'
    b'+f?+n%K|h3<<CAys6AI&b`}{ZzsEl+e){Ld{^ivJ<$Iicr0xBibO6c^IQ#Uri;oLXe!<zN$7c6$ia`0m{ZaR=>>nFY{yYXH)c&IB{s^`H56k*LqQ=jv{!JMu'
    b'KjZ8pZSV6-0m?5p`=q4tiSlok-}eA0`}ElC{!JAqzvA|H-M6xT4?y{S{z4rfTKCrxD8KJ7Q0qgl{>>9kex7jl>1|JQ|IH33KRcX#dfUav2`E3|?9&g6_Wf!0'
    b'IQhB95Gp?tH9leOkJ^4zexS#u<bMiKegWFQ_uU?!5hy?6@&mH>>hY6t@^kNBsP#it`=Ht{^85M(G=BEj={`o~H*(VbHOl^df0TQS0{3^h0{8Dp_b+9_$uD#N'
    b'DyaG0t9@YY_u76`exS#W<Yy94egfKmo?A-)L=N0v6c5}#HeElLh?8G>|3a+~v)TvN{;cgs?N58`NPeIJ<u{!D`}(T%7zM5m`;!5v{YwtIzAY6ezx4ivy5};f'
    b'ePHdMwEd|4MUNfXp9Y}(0JQ%+x72=Z1h_t|6K;Re+b;W;0+ipc9D)4XWy}7e0_FGkN5#+F_BxM0H3H>FoPDJ2bN>R>npXJ<XP@47@o@vnZ#et(*zEqT87M#F'
    b'_7~l^-9D)Gd6l*QtOIC#>#}8k=YjJ3`UEvUPU_!Uf$}TPKGOC+zciryhO<v^yZAT&<p-R7dTe(8wh1S{O}PDC_pR*T6HtD?{|_49x@_5BXQ2E({-egvsQzsp'
    b'DBt7kBW<7iZwo;A0cW4ycJXlm$}c$kl&1UB7IE@hk0H?b(EC=8Pgwi2wjY%r=&>pJp9YlQaQ5%}(_Z_pWuW|w%MZxjtH)2p$?wG(8)|(useNGWpS1lIHGY;Q'
    b'{}X`n1JM3bhDU1IOi026+`<>#!nn!f0JHG^3$;p*i;ZwP#6<^GqCkR3GBpJWC`d2#`WuskYeW(vZaXPUQHi6B1Gq_g8!BU57aPHJP(sFSS|y0OuTi@`0jMhq'
    b'Zr$Z33D=4wRN&So>C)Gs?tXWG>ld6Is+wB!i;ZwP_(ccQ21J5LcCZNvNJuZp9rGTp&LasPw+)fz%RZ+e0e!qc-Nf(0TLmsurS-Z9Lj{ubWEqk&l8}K`TG}uD'
    b'tw0e4XeUuX9qxbx-C4oxB*7})hLr?VL<R0l)X};H{lDzJTaO*bkuCgJ_(mQ;67qiWn~w*c8Q?qcV8*~a7y`kO+7_V}DUg(p?7{r^Q@J8*vwL?ny}L74)&77W'
    b'WZG_#Yh_$A@=_6zo=SlTPV1xMPlv=nrNGXZwwAip+_WZypm2t%C<uUVinLacq9e;x6a)~PM=C{RDhmDzbF*5YbP7j2F^Z+-Y9Lc7TA*U}auIYnyca43)(cvs'
    b'O{=+Gpi%^;qC@~RvyN1X$W#;r5Sv#jMP(`q4a9JecZo^i;8wKVU|F4(CWTNW;(dhpE6mM0&I^SYBoj}=*1>5Dm7)-DCHg6^d6YLyiq=5OdfHaat%~AF;Z`Xu'
    b'Ez;K0B~+wRM5-;?QqlTFu^v=hDIE3kpsuGRAD9##Q;)XlrBzWpDbgwh?@b4Px+|(wipsPFHvi}~>ZwN<w8EvGSY<m4k19+GG?b-vWW`|>isDIORw-zQVmOmr'
    b'P<SeZr`iJTm75fSy5U5NT;3@uuiIu?n^{n_W;K@9DHlfzD2gXVSf!vHVc<-1D9%)hOtnQ@jRHKEy5S6gd4z!g;Gu0egKTG;C@gaWU5+r0N`Zxy7R)iR5u*x~'
    b'qA(RD0$}P@Dn(@~3Id4DJ(a>U6$O8VxmnF~gd!T|5eAl)6KkYWv_Qq`0wm~ioJ>>-Y@2D3Hmv53j!NN}iV^|vW`(Cxc&4HtfY>}!DKb-0@K>0d)!?X81m<xP'
    b'mX_OtN~LIliq)w}(B-Wd!=#WS3@y@@)!Z>rDH2mrA^?`8Or^+7ML__uxn)w|z(-S5@av&C7A8f6ThX@7W_4Pg6lRrzc0mDumHQ}9rSMc+;33{71*@%Ar!dS5'
    b'3OVLAk4lb7k?<rk?I0FbMe(Evs}!s*zT!-BAC;*TnQ99>zzol&9w$>^-X6%&0v?r^6bVz0w(6BtQ8X!pA~7#0;7qVN?P#CkdYq)$0-OH?&!rw=QlXw$<GM4?'
    b'hDp&{9@$LWaJp4dJSp5N1?^A_XOatwNTrBWTeQ`vbq}(cy5Y=@dP=J6wwcvrNhmU=9?RS~T0l`eDbgwh?Fa*Bl0$K&QdFibuvN?OT<V51C*~0b=psd>Qot58'
    b'kIJXBo~KfHrlNo@2eCk<z=o4HFA$zuq%DR?Q4CX25CBeFER&+O)!``$0*K8cl_D|~1xt&fJe8s;s?grZwx@G<rcz|4qJS=k;zFgsv6U8S6D-|+3sj20RFnt+'
    b'r;SvK$W#;r5Sv#jMWre#oD`L*6qwzt4JQPEqG-p-B8OF`qJS<J6pl)Poepioi6se9q);geQ&A!SoVHRaDpOGqKy2=*6rQQ59M_{gttS{L(3_3c6%76gb8{)s'
    b'd5oqg2q3p=kxCJniu&qB3xTY*$1p%s5vzF`bc6X2i3IKO2cm*tfj}f^4}+25n{^#eJq<n)&5On&4L|en(KU_MF%7c|(XKKXkex)-5sX}j1jy%Sd1>x$6qp2o'
    b'X=Lp0mZ?nZGnN6~ej_c&4&bi+=9vsF;5nv}4CG)kG$oPj3>(9f9Ff3L&Acr4tqRhy`dNX%;5SmhXvJ#IK!(g@SiFhVtU{C&AP1A7DXFqtwR;jxM~%Q6qM2Le'
    b'Qoy=Uc?8bDnMkXDE0u9=b#|;yJ;Gpludj=e3gjR%G$pYL)L`T0Nzo7qBGb(6qiX?y=MlKJ-FB>2N$rz{v!IDghRA!#M3e+~4NQji7%6MvX*O=2#L|%vIHH+x'
    b'UK1;19)rVnmDz;aVXMk&$s-Jv*l$a;gx?C2q41tQa(3-1Pt#JT2t-p$=eAbD;AlN+9gbBv{upBK1BcU<^Hd7YEb|aWi6~SGN9@)IOG{A<OHrL7G0lydp$v*h'
    b'q;NRR(OM%VObJMlsT7%+WGRY5j7n4rX0;nE-BVHvm7-A19eM_&bCpQpa8W~RjfCw!B08-#l2BM?VxK6gKolm0XI8tx(mf5*Q7IhN+@)vTIa*Vp1WUJbHm$)^'
    b'#*}~*kxCJn$z-A^m^)A@nAL8ubWgoYREk73x9gc+j@HN~!_w`@O=~KYF(n{HrBYOCjuaFHa~CQFv)T=o?uk-{Nl^{c+>$-hf;p{uN~3VCn}(w`vJr}=C|XYt'
    b'p`hj(wL~LOxWJ_d#EhCQ06Z#EDI!r(5CEBLwA`jnk%@}x0x-?pDH2gpK!?*h+Lf13Fte!OuRWQqQYqSrmDZmHck;OMqIEVAio(ow5&<yvDwU!V6$Jsr+^n=S'
    b'(GgOHXboiRnqNpWch`|&DhlXuTHY6W19W0~oA|4w8G0&3+a5%kE!?W8=%^HqnS&+*G+RVZrSMEe#Z%HJFCEaX`G7P<i2zh{3q@cm3dwq{HIj>5ipb2IgpM%v'
    b'VxUrRlPCQti8WIxGSS>}ae&Oa$Sh%TF;Ool;(B7Gb$10t%)}H#xnY5#Vy04H+f0kJ<y7+)sT7fE3scs#TviXMKI@oMPqKbtZdRMBPEm<zr(y==+9hW0tiz{!'
    b'nz^lA6_qTLqV<rXrG|>XLQym+gu+st_LOu_b6Uv_rP@L$+NwuOHIZ3IoqEVhgt?QaQg~uIaL-zAYj+Av3Zzl+%pF%nrAVcS#Dv}MuYoCrP(-TJrc*IQq*73A'
    b'VNY4?ykY{(I_}gfCv#^iMJ8rwiy4p=oS3QX4k;}>bJtZ-sZuE_F@3uGYhg+u6qV_;a3)K2TA`rYLK5ZM4uqD11&U0adMH|exmk_Rgd$sFwtTPdXlr+NObVnI'
    b'@yzX4MP*N=@WfPh@mEolr&4&T(}q*gkf%~mZ6OqG2SQ7SlUYZddif*;tE`|?v?Ynvl}yTD#Ay?iA`vSWx&ZK~Or^+7Mdi4fo7TiaC@ND?A^_FgLQ$BC0y><Q'
    b'SC<3|W}%AsE6mL*@em4+?E%XcC`p2%ieXZqfXma?3z)mvqF5$H>pIR;RIaPJy{A%mrlLdus=0;2F%<=LI4!M4OemN|L*lPez!j+!ZRsmCTZC0nB~U2>v7)C7'
    b'fT<U$6p^W@;#YICs;fFhW-3Yqpqg7K5>rtq4?{6s;ZkH`U6SYsQ;%15m{vux%Ftxid8(p>qB6}bg;m((R3=4%6opwdgkrjCsT7u(A0>(^5QRxmnZ<Ns=|EMK'
    b'P<X1j!&-(`J(B_{kkv5@RZtg5%eWJYNUTfhio*O0R0?Jpnpiqe6(tmzYVNX@KJjWN5dk4ZVirfBE{RsJClr-g3nPlc{3}!nYUz_y$x;;s3Y3!Y%<X!)ji;5N'
    b'H45JfxIC?PveiX+10GMM@XSILQIvrwR0?LH3M}0VxFVGzQq7%uD!b>^h@p)*q@d+CqnkT;GL?dwkS~hD{7X~{W}%9gYQRENRHvv+b4#K;qDUoDcmpYD`Lt~{'
    b'LT_|hw!BbKlfXq$1)?x1EVDSmOQDJ*Dyma>s<}f?+4a^FDZGUgv>eX18d>l}Dg`z1SQO<T3YCJHkng29A`unUDKgdErKgE{n~4<OLJHRQpe3Pt3!X})peDPD'
    b'q7b7Bm4cZB4omkeOG~A&Omj;TYKtPYXS*7OZ)u|58Dct|ci{0<3eU`b6h#?`LZx6P9(zdw4@5<Eibyqg>Is(KMIwcFkRlLMusog#<7EYdA~Q4YL{W%QiAupt'
    b'u=J8*&Qw&Vs7!N9f)|2$B~o|?DGD*|$G40-Ps>CV3d_v$5=9k=!ldxbq&`@>r-^zhg{PW3^h7dGOR#Jd-a`sn?m-KK9z2ms5t%tTqA1M2K&4=&V0p<oW-6*v'
    b'WU9GKPhRr8>_<dENRg-%@Z3VBpe8R>(<ywQQb>{%YrTK~Eve75nx1tXS)!sKfTY8*@}oM1Cn~B7z%+NKaLh!qh7PCow4^?vV5VTfUwb-Sq*Am^4lOmY<&Z&9'
    b'p4PrzC;~A*stbUr7pWAHs3<QPqLG-Z)+sVkQC$G0xjRK-CiOLRIIZU;Sb~C?4(BByI1>}eIt8`|G+UIeC{Jr&FBFBCtJVd;)T>mAN>r4WY~4!C8x$QOZ;<vN'
    b'0`god)7)K0hN&ndKDNAFAGs8km~kgM!qj7>><UF>CRoa>GgL(hg(sR@E)I}!7n$WY9_gsG3yOAxkrOMe2|p+#eVTS3l~+YYPo=;OCoMHGti^QIGAUpXnk^&='
    b'wQc@+>C>2X%&8{{!7w*3LmL#4n2Fjmr?FlnCIwQ1dFIZmqIikNpvc5D(eAH_DTPpEs?(NJLVl)FP;DU;SoI2%B2uRwlC#C!l}b^GS;1lkWTGa+q(GWB&D_?m'
    b'ilQZfgF;f~S&<h03PsVR5DH6mTDQ(_n$t?=G}RVD(RLuL#_xUBQKudf<za4G<$_RnVup6FC}?YU3QP*5%=640S4Hs>@<9=a>C@d`15*m2h*YOdr$UuTrJ&kE'
    b'DB2DrB_>7UPQ7w6ccxNgVz#`P0U6q<Fey;Jz%zGU6~!x#07WIHvUh(iOeut-GM(0$Q_)bRQc!InMGI{Q!fO036q!2p@<|F-SwW|0OA@VU2xTyE+U%GVQcA*F'
    b'FGK)%l&4a7rlPW4&CRMJ=@gNvDEGO#Do`l`Q&B*N)8;^>U>2%~ze>?irc$&eiC4gtRz<Pe*LR9UtRm?GVCrQmMP@2W>gY1DqNh_-rlLdus=0-tFck%KI4!RX'
    b'4HV3xA@Nt3n^kTj6dv0HmMu^o21OOaq>vIT+71NfZnh|vNr93;nxb-D&Fwvv!ZQ^m0#MB@6ppDVl!u|Zv2ZCou`Wq;gsDd>Y!nJ+8Jf&GPgRsqM5?*dTEJBz'
    b'lLF<LtUmuzG=%C#UcDYDGBZC)6ovVhs1(d%I<d5;DoQ9S)7(;$goU*-DUbqL3bRlJb%C^uJE5?|x}>hC0#TS0m05-+mJU=!35BPcJFKNowAx8fpmvg0$BN<z'
    b')S~g~^*|AcwJ=>#n16vv!7P0eO9!f=gd$VTUDk3NUcDY7Af#Z~0(B9ng`w4m2}NZVs)(X6{|c3YTBstGnN&rA0u?<xbGx3(9%!XcjUu#in?S4AYl-r~fX7oQ'
    b's0sO^C<9Tb6wE>uSh{C|M=C|6nmhIM>0ly}A{a<P%cso^9Xy#zK}`Y|MIlBdDh0DRB1oZ1Au6g<RHnHlIU7-=5-Ea#6to=9wi>nCf<VjA77A+Ou_&rQ6efjb'
    b'CgcYxj&MXpbqY^4cj#%N!FnP^u#ke5H`rDq3!X@&peDPDq8vn_QZSRigCyi9qM|xQrkcC-)Wl#jks??~k%;MV!Gfn!DJnDjQ51z3Rj3rq#A8@maz$B+>J*k~'
    b'Zb`Ol!Q5FQMQACz!5Lx-R&e0)R0_|`xD!Pgh(e`cCRheZF=r~OQ$(t{Q%~v(ysY2^^!8gIru_s5o=m04%q%Za6y{%|QZSSHg5-ZQ71b#!)7+AdgJ52X6v06X'
    b'TJAv$gDuM|(6S$e!ZLGmL{SBzFeyAU1q+t$sfnIS;i={hJ$Wh6lKL7&@Q}h$Dd4$*N<mFtYI#eb2%bxkh&ef30C-fUQe>i{f@CFTVt!Pos6<6|0hs3Q6or{c'
    b'R!Vo;z)R`_1v3RJND^u#CNBv^%T)`s)WmAKq5`dbJt!n$jkR_|fR<nxf@M;)bU2!#Ab_MMvU1frg(oVi3&1pYr*O=qzJ?B`4YUMHp<t%N!C!l7Vx&^E?Ex)K'
    b'wB_?bQGwRJUMK=FSFH<xsTZjfk*KI3*}9RKH`pmMQBhq0rnx&sVkTHtEJ<x26}S|cnQ>QBpL&6pvYWc1XbF}<Qp}l(>J*h}Zd@E7<1R4EZ9*v23yQp+SZS{n'
    b'fFe|4YNFh*KvAJmDR5$?r6!tFF<quoWTq`73AJthS?SY45t&m@5`tmwXqgnz5;IYI=5$*xqGM7ZHJE2^zbcBCcnk_pOcND<6-9X}g{L}gI3?tJDh1URLeW+|'
    b'R^#_R>$p=doy;An6p@$}+_Tu*+8q;<0%_VjbLUl2yd-c?WMay0_t(UfLMSrTY0IfNB2y`-wh#*JKnjy0Ql}mg<;C2UN>Pa!+F}M|1t-I#K*~JL+}5s&q9x>m'
    b'Ldq9dkrw_6MbV@X3QKibx6W>w(@GXQ)fPh0b|9?A?|s%$ryhzHU~XC!iBNcAwtTPdXlr*0ObV1Q@XQ@oMe&LwKoN<l?A>1jQwpJoRHsd+qM=BopxQzx+72Wo'
    b'CPku7y>ya-RaVd`usxs^4V9DA7Ai#{RxWe_;8B%IQJIR8+O0~gA`uEyk?<;dPSsU3bBm4)Q&B*N)3W;f3q@uYs))Zz(U7N7v?YmFz=e_|C@MQDg(FsxbOD+z'
    b'SncaOg=Z=%+tu8xik?mpnTiqtsOA=mz*H2_;k3LmG*B>$hQwc`fGble+S11>rc0}$SncaOMIu)8bOA8+GL<4T6(u!|nOI%bDJoM@A^_FgLQ$BCLU|af8#9-p'
    b'66=ygN0@rN!p5>HidBXtv(8Z!1qyGe=5}iVSFubAlxG&hEE+;}BduOfC_FPiN)%-v3YCIcOedE1R7D9zq?$XeWoRWbDUbrm>MbvYDyR#jW!woxCe|f&MPdFW'
    b'Dh0C)O)TxHiV}*-G`Ez&AedJs1!^a0b*w0kKrI@rUQZ}2u@<H)sz4MbMP-&giKPQoQ9|LV<_>GQ4Xs`e6sXsu)lQ;-1ocn68Zl5rV&y_t6y{%`QZNfu#L|JP'
    b'D51zybC)%homV4<2nZ=?^?EIUp#F(h(E|!<LcS;p^RG}TsD&!9v}A%?Durd5TN34$01}NQQpA?Z9t|y@);DzUcq#=o30xFqAPSX&SsW3iP$du*)hQy?+^MJR'
    b'MiYq?(Lf4X4rgxY;K@`9YT~gd3Nb2CDVPcQQHmo9QBj?uGR-Xs!H6Q2ND&RBpylMW)u`pOM_N{}P*9UyMNtK!FexlE2|P+dz9TBCQ+TSmLr+bN))OhBg%pmM'
    b'4i_zWB9$UCvmZrK4x&&gn2E<xlE4#DQJo@F&0TteWwe<{5iO)h#1yP(!BeRem6>rTib9MkR0?K-Wt0?irlN!*TdKKTPwI=bWY<O!TbgL3rR=t}pXk8jsT7`>'
    b'<t2(T5QR#?OzMNBdzxsZQbek`Q%@v|yiC*t^!6JqE4YP02cAr&$jqD^Q55E1qEawZu%hG~GZob-D%0GOj)P!ci4@U6ibADmo=Z!I1BIt1FSWcSP(;tAaKxOP'
    b'E<p1rR@1Xi;facZ0Fn;J%8%+4k*KIH0Mp!^A}|xl8akXd@{;;M!A!x5l7t$G$xEH0ZE|?2iK#0p(%RPxMIz=$bpbH-GL<3|6%{2zG!t{xIz=Tastdq0cc&=K'
    b'q`p$R(?(u`B`BEba8VM1D>0EwC@QuGv<wQ<6%}di>p>yOgR~t8%-yD5uuO`Unn+U=1due*>Zuf-sHiRg)7+iHF%v9XK3{BkyD@MnJTv32x<2(HEoE0Im<g7c'
    b'bv@ZNQYj+S+$dCO8Fw)-%WYx^)C&r~o>*zG6@Wt0r)l?5byZY|R0?dHX^}Rais?L+!ZXuEB?+}{{(0%sn03^tSIcT{UWPU(GBXnuW<d5Mt=YI(x=_tsyP_g5'
    b'@fZ}9m?ql&wGgG~6qV?-aHgJ+U#S#STS!81TlH9t--RMFr=BEd!`#s_DWWB21@|oWwsuFyq(GWB&)j}h6fX%J6rPx}EB-2q@>B{>b=q($j__0psx5?~?Lb(K'
    b'-}|iNPQ7$8ccfB8Vup6FC}?YUOiT)-%=65hS4Hs>@<EY_>C@d`6H^MI$W*5-r$UuXrJ&kED6j)5Oo~XIdMH{Db5|-wC1%Tu8IYl!43h%o3p8_EyDExS903X`'
    b'C1FKc_$w4elR_vg)oI;2yJ=1<6$MmV2u0h0uo}PjSx23E=_CcKte{i0C5cuvgfbX7Z3<M1K&)Ko0>Gmpl_D|~CAC|TSVht)GE-6Zb9GgsQY5CLfDWfkiAupN'
    b'R1trbqM=Hq!1jP<i?S*z6)Hs`R*`f8F!d^xqB0dFb##?j(IXV7=%FbJ0$8fKMMs9ID4@e>X=P}j$jqW4@mDF}@>Ghp^wEmxP#y+FvD(*n3P-Hy=>jxcu-eym'
    b'3eQwjwyU{W)m5D$G8H8PP|YnAfvG5zhoQPLb15RRE=hERsmCj946CA8WoR<%992<5k*Ve`YXMizObV1|=EN)-LUkjpUQZ}0F+Zv+3iGc}DVW7{VrfTJ6ey6?'
    b'$1}HE%g~BtQXmDg7-pdg>H>?WQg~urQdg9LC{zk&8JbwyQxzo?k!tR=mOk-nClk=yZ-H4Hfm$?Py&fnsu@<H)3iB^fDVU{CVrfrRlu%Trxus|U!MrjlP_IX;'
    b'okRf%>Yr#eVnShwl?z=_1)?x1Dzi{UEFGwd5(-Z>cUV)|X*FV?K#dr!UJr@#sDI*B^nikyklz)B`4^}Z)It@h224yv2}P!wyR7NcH8UwtzQF1&FUi@c^PpwR'
    b'3k5X^Toi>ERj3ry;s{t;vX3p5!ZOV*$=OQ)NyZW>QcIsshL*$W8#;JAm4cdhEQ&G^g-XFp$WKxn5r~TF6p?D~)YC+hiA0KIAO$UNFgJAYWGV$U*;N#U7?r3L'
    b'%p~w63HgPns7_It=9VN>M3G9QNCr|AVme%EIn;@ki7FJ9nf)k=DiDQ9VVQ}?Ns_=FQBj@3Q_UTEf@QLvNRce0aKsd>WWf`u6p@*6CyH_qg-XFpuuPI-&Qw&V'
    b'$W(Kep469kS;2^akRlP&ev$=GrBYO8mX|0B^RG}Tm`Qy}^1qpi5{hi8=5{@iEYT7y8%1iViHVjb+A@BU1COUtcxFzHD9S(-Dg`qI3zqJwiIGYXspd{Sc`5O-'
    b'9~02qZ-Ghy&rMVcX7W-O0E)^~icD2h>559Mmg$|M5HpLq08mt=QdFX%lH^uaVwRUs6iZZ;2#}fP?m9Bebhu)=(<WMKA}BmFkxT@D(|XIKXxWcMMY*o1L~Ft?'
    b'6ponX)dhf}Je9%|6$Jq#!IG76*C`@VQC$G0xjRK*rY1IYIBnvkiGqTe)Yk=o(?%*qq$(<PMI~AjexXRjjJqxX6qTtInW(5FImelp{n#lgQBhq0rnx&sVWx>z'
    b'EJ@fSa49M?Z?Kd;^%5`fxO7F)(nPxenP`hnQJIQDxlPL(Oo3T6l!BpNv()v(N_%qw6iC^vv|F{fDk@kig(Y6IND``)1Xe0VWhT4gRNvC46E6uI6pnd&Q2csI'
    b'3e25(YN^2~(5`~(s;CgC6oGlP5B^jV=&2N*XbU+>21MFKrAX8hYhHKefw>z@Ej2g=+V;S&iVB5FQJBZckWVFnnM#p~wvf|HOP@}(Hr+yDn5U#_*9|AFsWK>#'
    b'8cfRy#-<#KijGR*n4AA-*OEZiK};ybAfCBZYc)5C)*2e87nBvSjxe$*2L&z9Tqq**2vftl`KRq^g#ueO+9t=YiefcY?i7irC<uU(z(h*|7ae7yqNJu#Z0?B^'
    b'auA~_3jPXnvsy!Uio!g?z|w)a`R^2PE7qz9bU98YDg|aY&7;C<?qrx0NSUW83Id?SgO-plI<ibfK>)FNrcz|4qTsJEH>(qPr*O>UBrF}62eD28r={&c>Ut=S'
    b'hDjku7@9|w)!eK$-JK#Z6(s_+RgcxCyHiA_q9B0S+%hR}K|xa#%9e2`rWLAy0%bk4LKVz9I4w^Kvr0j`pn$(d=Fz@Wc%m(O=NFi}5GfK$Nq83&aXqop+H_Yz'
    b'C$_ne>klX@RVqa#UbFO8AfDO&MJOWG7HtcKq9I!8lTaAuH4C=QI00nGq(DIotNXNE96(V#Dbgwh?ScZ%B$q{%N>Q1%z~&!CL$uN-p$N<qt88cCw24W9vL04z'
    b'XgRDxQ9LQkDh2IO3}=!H3Qwi*R9j$5VCoerMWLRO^15xNl|F$2r6jbXAsj8BD4rBym4bGJfiuaWI8!My(H4EH1`0={NGOO&w5eBC3R-57P<ZMQrmUNP+8aHf'
    b'kgXbRcGp!=w9+S`2+Ykt%55rmB9S5?)r(d%RM!rcG;@oNu(72n3jPXn(~5?KA~BCJu(X_5J(U7(MO%{m={Omv6qwyKk8-QIX{Ap>QJ9Jn0kC#gDn(@~3Id4D'
    b'Bb6dD6$O8VxoPD#ps0p<oP?$2_8?O!nn7queL$C^eW6ldcGEm6t>&(dO5vD_5&_z($Lf&ZDLhkA5I}5RsT7r|D3sgaP)sY}0tM3HDsAm9tJBh?5Q@OOpn$)^'
    b'+_Y;JP>4Yyv1PjS(55xv2SvX^U>;#`8l$~d01D9-?R?=@Mb%8D$joaNV@}UHR4PTK+M;ct#O8%cQJB{(a<o`HDjP$j$ju;`^&o;=95h7{r3hUL-UUU!ieet^'
    b'g(6dJQ5(8%zd0&}W1d)LI}4``M2c+SR<uKL>5Ae>AryglD26l1nUZy!6bdm&ByQER!PHAsibOpn#lCIMrVuHzfm_iIVy-KSD23}%(2g*0rhX`nREo&7g*?yG'
    b'rXK6f1yE$mJi=g84vK6omBKPN|K_y$r|oHl0`r14yK`4mwvI~Sh>8+RV;{wO|Dx;2GZke{?}+ivdcGgTXo`}fMKgD{fl3jGM;KUI6vf*7i!(_ur!7hLbewcl'
    b'3M}BPsV7TPGdJsrjZTr6iV^|Z_JH*kNvFt6ML__uxu;TirlR1lFgNQhl1@>G$4RlY+#W<K1)R3B6ctZL`$VO{?525CSk3JWlfoIMq98zf1}Hnrq-alh@Dv3B'
    b'#O9ewk(r7zbv@cU$E0ZQ!emEVyVL5lJSoyD1?z%B{8jFwDwU!VZP8yrMidD|itGaQg2JySRu`ERXpG8>v}RS5i&Topyk?PSaV_yF<WAwKwt%@2%()bacze)~'
    b'7VxOTq;Oc0SYZ$s2T&AG3b#tZx}XqelFOn<rHE8pG>X<MID12-Fw_%kU3cc*F)7+37}?Vf#c5R(Pl~ikK|2(~ndE|^QYk9a7TBt_UcuQ1Dn($PlAK?+&8&w)'
    b'gu=tESO+m2Eubi#6lRrzc7%a5$)VU&DLl~@eXE9fQHT`T7vd2{Hszr3l}b^mN0_v3{#kq4PJ!QOvpcSe3WiA$40H33_Sv{SU^VjXI<iDXL4a=aOr(&FElpAI'
    b'SD2gC$hT8C<`D*#mJ@5GQoyZf`>47e#AxRWP{_8K=22xecL-F9z*Lk7(6$GxUcsFrG8F{@#O9VsfkOsOQSeuoJ0vPaVjd@9X}LY{R0=pPYX<^!Ioby*1!gzR'
    b'qugrlP^c7zsVETu+k;A_s7ysc0I_+bQbeYrd|nU5tVX^<(Hf)XNZU4t)oFQBgjEXK1qJ+7?xQl5A`@+ai-Uyk-Lw|CxSNQMdO?xb6DzIDE-27t*V3G}tcr@B'
    b'O5usuEO4goR+&nXnYO^wGx%l|1M{pG1M`|ijuwz2GAYnhnf6@|7Y9%jPYTnepj}XiGs$I<r&4&TEnsQvKoawO5fk;qn%A9q%uEV2@}+&(!(laYr3hUL+M!sS'
    b'NiHZdm4a&vynKx)!lcNtFi%O*o;LrLN&#)r?m)__D4G;PQHe(waVD|3Wm4dA3g@U>wI&6vO*c+2$q<h)vMC1z>tU%*VVRqMwCQfPNUYREp+K4_?FB9*SmFr7'
    b'+L?EXfD-`A+<rB8;!;qLFlfk*GEiCts8D#KqPhTvXzoton2N#y3Fb~*3eP-<CD+ZJESDk@6_spQkCU`VTkN{|PqZA)7*}(%o)YL3fq9%vzMDJI3LAwY6BX43'
    b'2t;#tio{eD4y!OX>+!oz5t)Z#JnLX_oUBxeN>o%rayE|kw8xC>dJs#rd|C(qbEib5NX(->9`LX@6k8?*l3i(Ukw5^;G<VmLAu1{%IU7fN+KVcnz>6xh#A954'
    b'z-d#aQe@^e3mzGAmZ>PA@S>=1=W)FJ^PBH(UjOvw)6IvsZ*D)n{LPC$8HNO>Uy82iimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c'
    b'=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c'
    b'=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c'
    b'=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c'
    b'=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c'
    b'=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c'
    b'=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c'
    b'=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c'
    b'=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c'
    b'=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c'
    b'=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c=!&lBimvF2uIP%c'
    b'=!&lBimvF2uIP%c=!#B2|8^ey%b(tSy7}<-&F#zI%pCR05ASbp7RZ->`0(~GZ{NMSeevhFzutWR;^wEHKmF~+#~<GR{PWv)fBE{mHy=K|`0o8rKfix>^X}8~'
    b'$EU09<saYteDmSv`#=1A^X`xDfByg8eERhEyPN<0=HrhypZ@dhryu_P=FROte|Y=-f4+V9{rms>@#X(KqJx+J`tH-sUp~CK{g2!CKi_=+yAN-^zrFeW`(Hl%'
    b'?)~jAKfU|-+jrkDP#^x~&Aa92|Mvdlr;m&D|NZi>Hy;{b`#*nr^|krNMHh<kHq>O2tM#iF%MX3>U%fEjL=)Zr;yI4chf-=zKIa-;j#2nss&{`S8BHnl(fCxN'
    b'@zrNza>;!(AvXR{_{w<P79n1fEkfkm!WC~*^f7pEvMG6ITeuqF1Hsss7rtX1(`DzIMnVcPr5g91reEUU!!<9r#vZO2$~|6j&0wRs`zydU^f_zq>cx0bOo`$c'
    b'o=(3AdJ308^Z+a56tBk$;ZQS#NH>EE_COzWv9<`Ek_|R{7kBo-FA5(Hm3{})N1H=1H7sklU6$`8^tsQ%YVJ)Dx-L>o_45|096Fd9ZL!ukpPVxxw=uXZPMIp5'
    b'JS{FzT*_HCF<`HLV|FgS!`DPUE#0nKjHQHoW09RixF1sww2-|b3pu`pQgSBRlQyo#LMi2t-5Oxrp<cYimUb#~c8RzpxSc2Tm)Py~*kK1>t^V#Iv0^MSiy1Qg'
    b'Bv3=Vv(a+c^DpX=$>HsR!dt%ZDO&e=tKoN+J>65i4?A1_OY}SFe%WTpO@yc)TN~qh0HAO4LaKM~X3Ea=HGd9$OSl8AxA%|VG8X6E^$aHOFqmaMmg~A@NSKP='
    b'+l@=2K;Q5p9C+DAMVH*3bUE?o-;sQLb-Gk++njsZm6l_jI@`Nf!5E9Vf4Y{jg!==e>uA{peZFXk*E6n5ZO4y}-ne*op~5n`UdH$%$;&-ES^7|xGu`Jcvz4oA'
    b'3?$O;CcO#q&T$U=_3gVk@2_Skg}#f(%gWeR?0!SEr$t<L?rums&@;a{6uu3X32}eFa*$(QJd)xM3l+uND+v|$8&i&p-i`gJ;IM-YE_1~_Oz?PY*uw-*NB}U|'
    b'm39tI&ZNS>%l~3xhPS?^*zN#=^||^Z(=<$2qRA3Px^D8JSrU6I<_TZvclMtz<}d7RvoAUGqLp&jX8Ay8w&{8T4u33Pnn}A`<xBp$gDNhb$NaHe{FyGq605hL'
    b'XYz4hFGI|C#^LO>eBWJW+hSBK1#NusTE1%TKCZ{V<?U^{OF!)G@7<4oXA5Q7rG6evI_{g>a&$^3w+Z~+`QzW;_SVT4K8EeBluM(JH>J8AXZhpt`HEI8{!lIr'
    b'!h4(N3qg1frCb(v?U8YIv53uA5odQW$fJ>UZ!LTwveMOX_nT@+-pJ`#4j%bxKC6dh;$4gQEBVGA>T*W8vw5R?N;UPg?D^oYXJ8k8j@;dl`B?wH?4x$5Cg0s^'
    b'=WF?@z4ySr^ffo6yS5ANuun9h)^O+S7}B+TPYtQ0JC{Z!9Q6TZZw-Cv`{vGWbLlt6y=~=<b@|S1qo}B#B$u;8%Aa@QbQM_}*6NX*jvC3KMNG%mFdbXMbZiCF'
    b'73EG{Q3~G9*@rtPR~}r>d{wpG$JV(YT-be8b=}8yf4Hhn7{_)6IkpeRRkgu5u)zM<)&kelW8sSW3>@2L;F_wtuc_?)(8AO!s?fdCBIZLYcdw{$_e#3}TvMln'
    b'BU?rs*$m;DdLbNJWqfFb^|2Ms$5z%K+Ew7ts{Uh3yALgEzn<dhYpN-~regbjYs&X6DZkQc;wvq_KC)`@dWts>EMdKx%FU}O+&r?x`+6$fk1Y7Vo;vsIDRV!t'
    b'ko9WnSdT1YJ+hkndWyM^tmVGiI?!vXmc6Eu)N3lQzS<)6D=PcGrdriQOI5F^QuUgux{oaCzM`7$Yb~z4p8C@(t<b&Fg66BK_`cer_^T<9y`K8m>nWtZnmXz$'
    b'ElEAHBK2wtQm?d{`@mxE>#60wnj+aFYh<sdVEVv%=_3m%ueG}LTFY^-vwHbztGy2_fxp&5+-t2|zMewQYpH#`(t6XYsh+-`it=kM<G!MD+$WVNe>-(3FaP{z'
    b'eWBQV^<p`K(0t)ln+Z((MQfgkzbGd#@t2voSUfZFm*uQ5@s|y1W#TXU{=~GeVd~#P|HSdP3A~V4;uKgW7-)zT?VG*lQZyw6K1EYh<WjU81F}aoTVyUp<|@i}'
    b'a~Cc};VMeP6R$i)W}c-|td`(07;FNF1kNCg6K7pxu!-ugpeW4EKw~J()pT9#5|x3vA+xe$EmVTSb)<G;SPpc~^C;S;+j1$EWfU|-il(H<rC6M`U0AuorC2=5'
    b'RW8M{&-aE(;oDI(bIonJws74RJSn^tDLnB~U<rVpOVMUFXdE{T2CkxlnA=AxMXN^iiA#~F0R)Pw+^J`~(?%{uq)M?0k(oDgT!J>O1DC<};6bD)V(LU?NX)Cb'
    b'Mo_tdqe$RjhCd5;O;iG|2<u9hs0>_JTKp(1o3mhfGAuhM&=4tFU~*iFrX){S6et3hVsWYvxwdG^N?eLWRaD#VLyF8j20JQ6n|6(cNYRvp*-fM<Vs6K!Xoq>?'
    b'F}P8*V{oWkMOE(9GyMjN>ru@XL@DAz5tr>jBz|6AViahI6iXln4UwWLDR3#4_!O7f9W$3=@u*n16wCCBl}k~Zvbg3pTwB;~i^QFJfolujZBe+hyB%S8OH%5y'
    b'n@O>(6^Sbal;pTl_#UGwm!c)y1S&;KyW=&G5sJv2-JyF_;8Jh{NLrmXaw#I$qg>xdB`!sxDymt#F=S>UMxYY3S{2V_Xc{V9iY5GI!@TWk43(Jz&<I){hUF@$'
    b'<u)3ssRPvv31%RQ;Kf;qcJN|`LY>l0QM@LtukxxUBE{lJjfO}8B?Yb&Q6dx3pFq*(b>dPqWo0f!=0>N|Jt}c264%_mJ8kAtWUfc`trOAQP?F&)s+qej+=hDB'
    b'-)NW=LGJpA6irEuhDcG`n!0THd5t=R!c*`18wFC{DwU$;-4t#n7v@EvW|Y9AcoeM!v(XSKprpu^BFVg9deoW<ny3^lpMh7tEsDz2c>!;VR4G7_skUfNizSJ7'
    b'gekQL5FSNsg%4bcrX<i1rRYl%(P?X6SSy#JHVV(B@Z9Y|6?0cIh3DGB^x5sXQ_pi16(xXF-on~C!895o1<cK*K$Imbs_#IEt6uGEcjZ#FcP^PzFG(0A26H%U'
    b'q$&y&nQQLYoz_t)up|+sXxoF@>dy@|ZL{$(IgrHXxExJSo~$ct&<p^Qcs7ftrqY6>wb>@-3<?Kq;;42P|MgT37=$TEb6z0|)Vo4Y=4e~P#>3>O{ea2juqO7&'
    b'PMsoArieFO4sWO%c5oE(49TbEkjnw1Q<aq@7t$JLI~GWixGWJSFJuxU$;e!FRY@MT)^JIzba%3B7E4Vb6@3+IK5zHl!d6%6>f)Nd^o;sK<{+!9?c))<h&{L3'
    b'eh%jaW?!#nc5EDpBogEkS(4VXs)a7*alv{yE>I6X(v;4VXQK5z2uJRcg@VY)rHE81>S+r>w1><=Lw2pyTkP4u<&f5E#EBStmpx{)KqxAawUv9LJ!YppD2lDE'
    b'(wn?7tqw&+uC`G2jICp#a#)duSgTt5TICFt!=m{fQ(I9=>aDX>4(lvgTS3aKsa8kitz2!{R-kMhy4n(BBks?HipkO}B2-KkC@Zm9T9j{HwJb4>sk1a6W8T++'
    b'#iL`dWwT)77q;~s+b({!3sV-~#AxYL)(18VdS^#AOPl+|Jh0A^pf=)xF0LDIrd_}yc45jA*1b2=`l77J)>vA%-%KA9WzjWuT9G}oGk9M2`AilUPj<=dof2CX'
    b'UrsBsC$mW8Pi&S%-dzZbVXw&U<jJ1Q;yqawOcn8DLuQd(AJfO$RB3IHEV0|1#pS(FF<I~kfn&2kS)R?(R%D#TiM^>hON%fevss!uhr(tlP#f9$;>n5aV~H(G'
    b'U1f>HI2Q3H51R$k9#l*gF}!1I%&pdsp3H(YiWt}|fgE8(W0^cF#rl<O7nzWrEDLT(M3%_DQS@XMOnXp8cC?fT!;~eh)@R;afd#jt%o|0p;6{-eVbU65n6py8'
    b'@38G6EQKtKOcl0W+{rFfAHxfC&{$=&G~*;gW=VLQimkB(>of29&H5RUDT_R)X32Je82FM%)tFs9Ik8W#kR>_xN!*ZGkT(D-Dob5c6qqc@uhwUt_`o8!3Wd$W'
    b'j>)1i_N=s@@5dsWC6Z-neMW7<!?MJaMZ)?L*esZknau)a6*fz=e#UdTmd(-@ne5ms?Kqx2n+5L|8@BZW+b;2B7sH;Fg>9F7vWsKSeW;C@k9wN>RF-y1%4}Ig'
    b'S&1!6KE*N5W`U0tHVdp@*({Yk_shx03Y&!;Ve)5Bu56ad_OWz|V}>1J3|V8i?J0PC+_Ljv6Pcx)GF7N7P?lq}v_M(dw{T#=O)oPeLRg@-$krIFAIR2siES6N'
    b'+NH3w)5Vh`n}wZqBVxeEm?c8_q%kH-Ta1M&vEx`_v(z<?QRjYLeXJTXOKWLot7WsW=e{^`W^2r?8lzf2ubxb`OJ40l)mS;jvA|{tWQ|o=zb(teo`dosL8t;b'
    b'Pbsivsi#axDhmQ-+rtoh-gOps_F#>t>_N6H$Wy9`>|-)t3OldQky+{~>xRk#WmPVVGiIGH%%`5g0v{u0cL+<%?r_F(SsdCQGUto9SLMnA7Lg^gBY#`P9I+{y'
    b'Lr<1Q#btqeky*O30$Y~TDn|6=&e9%NFk}{Iz>?W4nY+8_?iJXw_$~|AF5$F;&1{y;)mUGQp*H4<Tu+g|u&qyK>B?ej%$ie#v0N6cmCmwRtR>G%ktLD$Fyh3O'
    b't1)2_jalxj?4F$1EQ#%7ZFkW+%sFQ7EC)|^WELbr3Kj8WA?^4Io2Bh8EUcf|ESa013>L{7C+1rUOGE%jT<dpF&TN*<m8Cl|s0#VsQm6{~4mOZwk-3ip8I`5>'
    b'xzC+1b<Ix>WLf0ilDX#xOJ&cO`gyISvygACom8f@b0x9+oNN6qK*eN1R%fTO?CkW+)|l_vwvO0+4lE9@<hsaaiQH`4t}(~Wg6>Z2*cvlkV_fUIwKjoj7uW5='
    b')R?^!#}fCHBqs|d%jZ*)OWZi-__E}+YJhpNaBD>>bvN$vx*Mm?%G_fzx0)lYeSn!2sj^m*D~9@1F=V?4OAsIXb}G%wKfn3z=Jii+KHYqH`{wrJ%ip~ClOf4*'
    b'`lSR)pae>w1WKR;N}vQvpae>w1WKR;N}vQvpae>w1WKR;N}vQvpae>w1WKR;N}vQvpae>w1WKR;N}vQvpae>w1WKR;N}vQvpae>w1WKR;N}vQvpae>w1WKR;'
    b'N}vQvpae>w1WKR;N}vQvpae>w1WKR;N}vQvpae>w1WKR;N}vQvpae>w1WKR;N}vQvpae>w1WKR;N}vQvpae>w1WKR;N}vQvpae>w1WKR;N}vQvpae>w1WKR;'
    b'N}vQvpae>w1WKR;N}vQvpae>w1WKR;N}vQvpae>w1WKR;N}vQvpae>w1WKR;N}vQvpae>w1WKR;N}vQv@c%=CZ>KW6{OQf7n-6c_+`jzH<gvf}+uvV*cXNCD'
    b'aX}7~p?`gSd-K;DK>z7$^Ns)N#qzt$U%gm=_mj2s;r;E+LiX|xAKw1u?YlR(FaG@Y*PHKO-2C+Or@y`U_{003e}4P!FJFK6=EJ8K-@X6o=lAb!-hEpBIKvlS'
    b'{_DF>H-Gu?=Jr2s-~W8`{qH`!`Tq9i_wRrC@Voc7zx?#><8R-6|L-?%KK#p@cgxTJ?fu73A7B2@Bg%OB`zA&E)BpC%#~=Rr!`q)18UOp`UvEBqdi&iCwEL>5'
    b'*Mu0YE!G<6lXFeM!A5iUSNQ6M{l*mkzn-smp>i>JZ?Y*V*<b^VS)!m1gZmh=3&GS7O0gb-G-zvlz58pJ=t6~ASBMI;E{>q@r7)(|_jBI;tp1OU{<Prt^3QM9'
    b'$!->euU@$4j_y@+kdeQ?2;xWn{xbM5^7j`FrmtS)k-xtzKV{_am#<#bk-uLT5k~Z9M&!4U|M~m|_AeuUzl@CE!++|?->)O%514;x<nO08{$~V$*Xu?Qk-%ag'
    b'm;Uoax;tA=`?SA#XG{6Szxi;-_~cFEGdF<`_gIf^$NuU4FaLFW^Sd8zZhpky`u+P4KfX4v&E~Gm<+Lm)x#VCR_P^fVTas&RGTJb*2e`A*cu1GY_(24Sj>fR5'
    b'u*B8ZEcoR2h2K|Kh3&g^-zs}pdzykC;Fn$SY5rsGdut%OlMNe_gXmnF;?aDKtIW$H4Udkh%SRS9Q(eu=uaHZnE;nX5y2ltpjXCeRiV}Dq7>=gO?O?lyNIR+0'
    b')?KIE1G>Bme%e)AG`2!kR^bkxyLeniH%mA}KcX1&A<OK0W;DB=xD5BiW$1?pLp}x>?jgnOye&5S?)uHHyYL5*jkev{UOtc7b`W^YZkuqk*CyONc@zGu590Ga'
    b'4Ndw&H0eXpr0+%dKO4jeFmd4a|NcjqGC{?50!)Q&hGFv9mz6s(?SqAxfzxJ$ouK7KE<0mFSU153E1YLst|pY7A()kjVZ$&``#kPvAT^LU14ur1PQig>X$DYQ'
    b'{*z}|4LT}Qkjf0<+Iako_$pZf6GRiw9^HJra<Vp00BS4zlp(b>e$J3wbH^DW8%S+jeg=|j+mA2>DNLDgV!3hQtjIP&-`xi$Xvv6{CRnadxjX}?x#hTU*hVy@'
    b'I0MNovB?cbxP*<U%M)-~I<6a!l(x^^Gy}=CaScbNC_651CIEReL)~pSkgv`_a&?Aqh~106y`6#N?Uad<WJ}@Q3?%QSNLR3_m@rjJLzy9*UzP#i4%%@FQgib('
    b'1*s`LPeE!fHNHF*33KCPg5B~IJvF2{LpmUZDH`w61v3LFw8PW*_Oi-yFu@CI*VFizvMdPWdUCnzY20?EF9>x8QuEAl>4KH065I@=u!Qm8ry%(mGZ@mP8PT`x'
    b'3B8@6Cl^Ie6IKK(3+K4Teb@N7bZtC{z-b0jv)#CK*s3<I567nvCDKhmYA9321j*)%Dfb=59Hb?VhcW{xw3Vt(L8?<?!D_oQ1*uHY`05393R0b7yFTy6H6Bu5'
    b'rRu;ZxckK!vx;dIM{yKKaTG^!6i0CsM{yKKaTG^!6i0CsM{yKKaTG^!6i0CsM{$O5p7#N4v_tLPu3_m}0B6m^?zF(LF^3$a{p{y%4(+E!e)zfO5r4G*)Z7P1'
    b'&r{6v`jI`_WbDgbVt@b3?d@-Wy}fz7AK8}t-Y-8*Ddm{Fuf?P9+9JIxp*pktz%Bo-q`@Yrk5HH7lkugd>YX(~sDrmP+GPmEIBz_KIk=QfawXPaa&BMB8*@sb'
    b'l;Vu_HN<Q=%-Or@vkfLzC#{h8A&z#jbWPSQ=FX+=r|ak!^Lp=sPs!M{qknBN$CzBQx!A=7&W8PT9c`>OmJ-8a?l@H7@HFpQ^qib)@|ql6C}F=DwGZ`X7}-VL'
    b'_hV-WTOKw_ytzK@6ty4W-Xm;pQ|}VDAEDkMaBnm35xE~>-XnBhPCYwzU#{-i(d2R$n;t@+FtK*x-X(rt5=J=ze0#Z+{vR=)`hWPqa_C3627Az3KhgvoMdL$l'
    b'<lRVJegkMt`3Hn>(i$L+0E{&$=v_^oUw4l_328`(fI`&gPfxVP$U{Pm7W<=4v<wN6q$fum0kCyQh>XVi&Wr$zbryJ4&?&{)5ddj$@N9(ItB~CY0&4!BFNL(7'
    b'87YRBLUBJNhwX**V+bfS_JglgJii1VF>(mNW1$!T=zXlhNOTE90KL{fjLhsb1W*v(1^}uAr!X`j>KMY>pdbuwTgJT6^_B!9+m7KTNdghZ_Aaq+UeXxEP%9&W'
    b'$V1DfTNnR222qEWEi?r&L#qxT?9h?{h_QeV2-(^Xzi>1BQA+_7Kmim$0Te(16hHwKKmo26;Q4P<n%!QByq9D3Xgbz!-@W_g_RWVs{@<J1zux?QIoN#q=MV3H'
    b'dH4Oz_y76B&CTr>6140_f?CNYgb+<|F2yL{BeM@Br0QJpp~m43A7`hy$A;2gHO@X(Z(S)S%U9Xu&-r3&Od*u^(KhZh7FR<yC1zKB2_+)~!nTiw*3@caNTs-)'
    b'hLTKl)drVMveCK&N3#51mx4(pTU%W{&_2Pqd!HM_mf!j##}eFKU6mM)v(fUe?|D$Phj?yFBeHFPdHHk81TS`pJNf2on-81QU#D-D|6QuDX89*Cj<XD>92oA-'
    b'P33pe&E_(2=E8<Bx1HTek3MEi+8oPKi_-RBj#-tq$8yNBv^|t#)}_s{9JMe#VK6(aOc$GJkEQ7n_uX@Cx^!yqwK!cK_x4zwE?*ILSe`c5ZF+L_lLkZ1mVU}u'
    b'*y+<x8Vfg{`YA&pCs;peDCCUm(XmWS!5+2H#0=q4znz&VJv^U}8Voy)`}r%t^t|pTt<y)XMvsi<nB{1DFbAzij|}FJ1!;RM$E-+?jOCam>GHww*QCph#E*BE'
    b'JMRt)!4szSVWT-{UAkm3cw}Mvc5pBgYjrk+8?N5jz-*7lO?frw0qBf}+s>rNOLwy|TN3F+NXasutWdnBHskf9d!U1*T-%Ui#a&y@6uazYHfWjfYTmg*BLOpw'
    b'zr%eG(u<X*DikhXX2+4iO22K$DGwCi!%SWFIvcc3c>C~7dU(@p%r-q|I#UoUO;spdzD{=g(L&H|$g$GUEgR)YFN>XnwkOowWQ9(77xf&oJvKDcnR*S)RE0Ls'
    b'DR1}P1s$yu-i92j9Nu!K{%+ySL!^Mtc=h#6dOT}68*`bSGpD>%cuiI)T;5K0`$=!cpFxflmTx&z?XtVspfjFIK9hdR3&m%c?Rm<nTiYyFnyOH^yqoOyqg@8J'
    b'A;<a-Y^`%<(p#MmK>dVwoX@1kW2dt*m+3k6*j>a*QxyuA_mkazv<byF<XBsZEoWL^Bn`7c!-QwO&!m@!SSMpH({t*vyNZ>jDikgsCcFJ;kCJW3v92Xs&g8o6'
    b'aW-gMK_@E|kLk|FT&CyLdkiC1nyOH^e4Om|!!2yKF~^$PY<ZLK!l&7wGhTZ?lfL0j$7~1CsW%x`%rsS_aQZaa@yA;nJpww`^k~bWLKi>J2F(-R9zGYp0nZ0*'
    b'$Iz+w8BPo}Ri|+LJlXk&n_xYHIo1|y%cElVs5BYW4|RTeM0_6!pzW*b)M)C(PE%FdK)r;MDIe+Ycf4^klMv*WLMo&}Dx^Xxq(UmBLMo&}Dx^Xxq(UmBLMo&}'
    b'Dx^Xxq(UmBLMo&}Dx^Xx<RIkm2l6`|o=3;`%%0DeG;)5l3-mv||K-1KZ+^G@!5^h}^!pD#E`P&rwtn_D2Iox3PI>~gH$(6K!Vm3?B(5zs7rF3R@S`IUY-=k~'
    b'l{E|9xE;~=RTSB21KF!w*ul`#v~vz0_JAjOj<@&SlpCJBi5qOZV6`b6Yr=Cic~N+wu~8Mdy@r|UYF>VYTq<*UF~OV~1Mj$I5@^o@2ThNg@s%&oPI`2)>^RlV'
    b'*(NVmkHDurRYf9mWJ6E~&s{ApW1A&fAfG`V5KLB9*z-Vm8C#-ij)flBhUc2XQFTw=`#zxK2AHtpPWwS*W^HV?7t4co7zEm|(?)wc?C=Hp$9jC$P3eOspQA-?'
    b'twEKU029zIZy3g+r`Zgl!gx!g1{25o&NQL&c<TkUzM242p_^ftjGhWJVC;m7YT%d&C9h4(bwcqdtmP*7V3qzqb^?wRu?~B)M2z7smeR-0&p`5%8f&(g>L=kq'
    b'vNQuIO=u=2jaTD@rcZ)YW(bEin=|6;q%Ll+dg1u!)&ng<>=Yn7sS(nv-U(&GkX-M;Xr>^U2{rYn-UP$t>4FrdOgORJxNufvo1pLR0~55g_CxnG9Nf%MH=H}q'
    b'5Dwdj84cv6x5<pA+^xS{oX|S?Rhrb{R{CL>8KT*>%lL3)ioNxNnE=!}1dgj4{rG3}fCbW&zM9hcGEL}z2qbT(Oq3*B3h!nhp)=XIbOoD=2~(v=)8296q@UG<'
    b'W<i1!C$vcsq#18`2vVNVu?wx2(RDn}K$`OQ#VhI2KSMeog(({E(hYZ12GW%7;b=<i(iAV~-P$IMDa(Q|uBWwa{RG>Yz97^YNK^XrzY4ueRB$tprgRe)BtK&Y'
    b'L%K90`r-kY8Qr{rgcjc8D}t4Ub6n%6KD*=Vo$D)Snt_B4UgHOrBzyYd?w_whlt?!LDNX7~D*iNQOu6qc<{-7+i)98<dn+{5DM)onELd$<rXZCm8ehGjPC=?u'
    b'Y}e=AxW>_G7ULTD1b4rMpP5uhp*V`8IEte<ilaD+qd1DAIEte<ilaD+qd1DAIEte<ilaD+qd1B)g!8-)V0T({J!>Q{|MvIS-`(8e+gW-Rz^|`wZ~l5CAK%Wp'
    b'T$tKEI-a#`IQ{T$x#RM~^{3(9-w*kDdU;;Eu}3?GJ=$YT{@5?Kx4-@M_U7^CVh`kB1T8*Q@4X8?CDW26%{L|)S3-5B7VlEZWhC3;aboL}ugMy37K+-LgSR!>'
    b'Wdy}IZ#;uIXYZ=dHkepl%fD*8DTPvsGuAJEEL#e%OW7n>Vhv^)!*0B(B%h35R9wBoQ;7TMIVIoZ%Q1OhOW4n|wuoa)F4<h{Vs~f5Zi<dJRvSx+VHr^zs%m(W'
    b'V=YQf&NXRG4lb0i*G$@lcr$kFq3W$@dFEP!v>WTuPEq<1<{iTHHuDZ~`VnG&px!3lAyPj=yhEtIoOyDrzFgOnBgp06H9KftKB4wu-XmUL9ysR)?Cq6Nnu^4H'
    b'>h9qK$&nwSdfI{IK^GDG>_BrWb$@oYHws)witZbL4MRdWsr!#30An2pddrgM7uBN)LK+expvv_5QxiQe@{katmHa3IEki;iX}D2G0Bju+qIHXD<>Mm&V{HRo'
    b'6|_Ndb_77W7d#uG_7Y<^f`Eel=Sv|yWkxF9r3%~+$zgky{1^gii2X>EH6!))h>=489t*_)KyOkNMxsj?0_cVOVPs~fA%KGLHULm1IEA4JQO6M0?gL?H+cM^j'
    b'uJ;=l*>((fKoW>Bws(nr^OD9OhWZo<L>^i;-MaYKF^D>}Y@y?a8CrD!VTYCsK#T=^K*-kq8OMvs6;cYI01BW03ZMWApa2S>019xm08czHJUgT8nK@SvGpHU-'
    b'w))4fK|Yp#WgdJe^4{J1Y=ciZ%l|4NRp*Ld{>5<jj<ZADV<WLSxD-q(+1k2L<B<eoe6cmA5K8o^#$ATus)?@J;Ic_JTKQ6G+t)&CYPB(>Qrtcxi8W+XVs_P+'
    b'P|9%w@h)Z`tGBKclWjcEIyRdSLTvvg#VATS_gR17P=dSX$T1vZA^EUx<2_G~_6WC4?Go)9UvkbRFJmiq(OJIv+UBFC^VjK{Wn`uLYL<WU;x)@?%5ib-+)jQU'
    b'&1^>hGxs&~XSGZBh7!_oE7A5)j#-K}$8yYCv^|s~7NhNv9J3m2kL8%<=m}%tuSXXdX|Dz865ri%MY?oW@3bUc9`JTplP+Hf_>0o!&Vilw{FI@P^PrzF6mnwp'
    b'Q%1tglzzfU$f?s$83{R;dT=NcldA{KGco^n&}C;PK@ZO3gNDLR&>oEW^D?%dvPn2*^?770hb%waV>x8~d1NR@EI`{sIb;QTWGII$L6?t(z6M=xA$p9v+;91z'
    b'|MKa4)L4#Lhb|BQ=L^xdgF~5Ece5eda3#(LW_#sr%JV)CKxe$Lb|yWZq??V|5<(|JO2+VHh2q(>8P62m105{O+J+n})Y@{U*kv!XLCb{a?amb%37Bd8!R&jG'
    b'UaT}#p>X*!JB|!i?QKI&c}e&lX6mxn*`Rg8BZX(u!<%Mfw&^+3nSxkpszTxNb+X%!7Ikhzj+J?C*(gtX0_+^Ly>;d$D|E^OrstULRiK&9)azlUDzt%4d1UV{'
    b'=xELFHsn|p@Rl?62L@-J9tCv9^Q>pm<Ne9mn9KB>Ipw8VYqCP&@^-S@PkP+_405bUe9M_?m)*?<o$;pene<bh5<bIh??_JF+GerRRE5Ij-DI~P?HI5PIo3m9'
    b'Yn?Nb9@TsR>L)z7d?r0!C7q4AOwXyu?jly2s!+JRpX~Od4JEcA$68EmIn(-dXqXKeCcM9WCcV6vIvI1Bo>PzARjf2sp>X*y+3iRBjch}Xbs*VtCf8+;vq9Sm'
    b'I$5E3^>#MqGCil>V;Hg0RE5Ij<7BrVZb!3?Io6<N%bR=`KFtQ5@htn9^bL19W;=jRy~(g*rl}f*)2GRfKi;nB5zw&)Mq3UQy7+lEXrAy$@VWR6cs^)5hEBcD'
    b'aAK&bI)&rs$<9CA(CQJ)u@+Zb9u>PsrOBXvsEgAh;`>MdZC_QVMpG|#nyS(U>Lr{^`AC1idySi!f*`*XQXv&mAr(>~6;dG;QXv&mAr(>~6;dG;QXv&mAr(>~'
    b'6;dG;QXv&mAr(>~2O)<)kl*RnJUYH-_HVwVDf6Qpo&V|mFaLFW^Sk8_{wRH*-+%b=wS8?KwsAJ!IFpPqx#VEnS1(!<8(Z)Fl4giAlDIb6G8bN&@Yv{B1e@AQ'
    b'RAo&<w{=(aT@_WxPRsVHvV);#Y3Bia*#n;CIp)5b2CgI7urVokZnY^K%gd;myez!X*qDlZWDPUb)x7))xm4!zVuCsKOWkqJoKO3}Xe>Q$$JZSM+DDJc?>W^T'
    b'u;o4A)1Ingkrl3{3U%<*)#5U?Nup);86<PhP<ht_VczpVm8l1+%swV$?lC7*Pa%2Vy>H%iW1sijX+MZ&tc}g~VtLRGV?J%(Yonca+Gyt|Z?vCvQ~IFE=V*~z'
    b'Yfxn-zy!3*8-}syX*NTsFy7Lr!Nl>tGfk*G-g*J8uO`4$=w=uuqo=|Q7(1b&8aQS`$!pVcolraqYq<$NSf&4uoq!`nti#?c5o5TErS!4$Gm!kG#+ogr`bjvD'
    b'EX@E)6Pk%h<JCB!>60Lp8N#8>=8X6{sf*jIUN}Cw^+1adI|ay2YJ~KvcS4ykB-cAInkh(TLQVatH^Fdux*&xq6HY8QE}RwFCg{8SzyvL={m}gk2RAd+4d>1?'
    b'gu^ysMgw{2Z8D=Nck3?~C$vs}l_qt#m3|mzhG=%}GCmxcVsHImCIGb#f#d2%KmHj#V1YEHucmaqOcVMa0?FGc6D7%(!n+wr=u9>)UBRYe!c-~Jw0B%M>1Q>e'
    b'S&$&b32jmYX~r8Kf|Mt8>_Y2hbREw#kfywS@k)C1&yWsCVT#7Pbi*B$fi$IiIGPf>G{p;gx3&pm%CaDg>uGIUKf!jUF9>x8(v<%EuR`w<72FJ@Dcytx$<LU<'
    b'kS@)LzIXs;MmKLDp@sMOieP2o9M|}%&+hno=laT-W+0)1*Z6@Y$)0|=`{%0=CDKhmN|QR0ia*U6Q|>#AIY_PdVwr&y+DcWYAk`_cV6|PDf>fqxeD#7l1*uN4'
    b'U7vU38b_yDjBDT%-2E1QW>O)A;wX;dD30PNj^Zee;wX;dD30PNj^Zee;wX;dD30PNj^Zee;wa7#&htKi-D%PFtdYF@+uvV*cXNwxXX#l0zrMb``Rh&p_;$C;'
    b'g^fAn)N1YSv~0i+QBZrQ+_C*oewOe5?eILMJg?W-qwT^TZ7?Q(?3dfy-~M`g^Jr(Whr+j-M8AliQpz!TUrS54Gv6$_b0t(~mLIs~-<6SMi!V@@<dgBGrs|zF'
    b'L8ybbHQHqe#W-&~g*mvCO>!mHU~+azm{SU+6lbijA!f^A&fZm@Z7{Jqm-i!%cCmC#)-2}ErS7Ne=oj;P?}AUs*tDa6Z867~T(Y^?#RSfV{d65|tTvVs!(#3@'
    b'RNU}1?^^VnoNMx$99$@2zZta;^=25^McwyfX9!y!Hc0$naoR0rZ!_-@vNwtMh}hf2{D8g5yF<L*=G`G&UranXT3@W_$<gCt$C@25FP}=gFz*qmF9?{FK>f(F'
    b'C_O%6KK1zUf#b%HFg@+y@}QN7eRhmF)w@4C<r`J5BbE0Jz=k0qoD~1Z5rDBa1if#`^DFDo2_X#$5m0LS{Hck?7kNmC(Q<xNf|em6l62juBLKDz3DH`{v>Nge'
    b'fU({IuL^phI6DF$EexKGP<x%R8$m!-|MR7g#xf)2?otZwhvcxmRDKKrg~Wa&%9@cPd&I~g0FQ-Y0HAlO3M0`a3<30N{xCAL(-1&GcpCty5}d-&gs5W(YYT!f'
    b'v~3ylM%SATjBGoG+aL)<7~8wVzIjPw5JSz11R@VDn{HkF>lj2GTDH*k!wjuDfUrYL1|Y@)J|JXk|BU0s<T5D*Pyhu`00mG01yBG5PyhwET7V}W7@nP0_RQR?'
    b'hnZB5CSCobCm|n8!*X`xLy;@lgb<<$&ZQXTD`fVegjAg?KGZne!{hv-<B_3w<6`!)dh1FtS-!+Bf6y0OV+x_P54CZpvA7ztDKWe1ODGwc4z_(Tw5C=YLn_7X'
    b'G?Zkbt2Vf7l8x<t=dh71|KFuxQpwg<R}ZvLFz(*x#<1nL{>ZTecUM;>hU09s{QG+z6zw6N+tP(>8(?1k;4;CBUE)r@`P$~g=JeO;o8^C(>Z@7)$&2GG!zl-b'
    b'yK__dopiIg44k>JnLoFaeV9;i%!;%%l7kkc&7mB!9&L`~h~;Q=Acw3*TO&DWF}i#x{I%#(1MRRBUEs7ku0$73=A9Ozi=*5Q>(IrqpT7)kug~;k=O+z@od5ik'
    b'v9MF3pEMS3mh@AGLQb51(oo2`)T3jWm|i_<p@~_*qkcOx6?%9+A2k?us`m3&fa%%WPgtW5T8p;Fa>!D&Ih12oqV1s^u@G&J<dAh}dnAV}Ll+N)z6xDz9(sJc'
    b'*k$=)|MH1^&{&RHfi4L9k1Rmn4i05v?ah{Gqt!SYnC-c@DewF|0G;vF+L`otn{GB{OA4I`DOtml6^i%IX1rH)4|K3JYa4Q`SZm9fVwb(l1}zibxjR>ABw(iT'
    b'm$UCdda=?}g~H{_>^L%5xwj2D<w@atn5oNNXM@%WuN9t24{w@{*{0`AX9{AasS1V5*U4@_TG+V_IacbqWurXlEwFRY_UM_Ltk5YhnVw^|=YeKAQ?H4cs?Y{H'
    b'<+Z)Lprdua+mK_Gz+2ALUmBcwbQI7T@3fvtkB2B{V=mKk=9HI;t;q_7%iGCrKk1eCGsv+*@hxYnU3NDcbjIVxXVOo3Q}_(CJt#SKYn#PNQxyuAcaz<Iv}?dN'
    b'<X9hpt#!^!dR_AYsGsoi@|pB_o^&?mGCijryNg(9szTxNezMz-HkH_h9BVVN<xJ}vqG2{@nD7wyne_5>>SWAidQLrdSFzGmg~H{-WVavfIkF8o)`eutnOv7W'
    b'&IWBO=wyZB`P<o;%k-Rjk72}0QxyuAkCWYgxFyXt=2(-OEpPH&_%s`I#{2AN(l^}cnC$>M^(MoLnWkzKPM;<_{&>rxM?lA#7;QOJ=;G(upn1Y;!RO*P;Q65K'
    b'7&`Sn!-=7$>J*NjCp-UeQ>#ZX$J$(Nc~tBkl_rDwp-xVZi0>l-w0%{b8cn^}X{t&asF!du<s<$54mNIP3WEGnNQG2Lg;Yp|R7izXNQG2Lg;Yp|R7izXNQG2L'
    b'g;Yp|R7izXNQG2Lg;Yp|9E2SHKz^rV^XT}V*~9sg#>|g)b^fRKzx>zj&F_{!_@nfKe*fXe<!{){R?Z;?=S;{>S^~6ZIq&|$5ABQ`t_?C5spwhYqvPOjt12-y'
    b'H3>YH{lItC64zS;*PmSA+jy30&e6jT=p3K%_P&2oLy|XfgNzoSHbo;%bE+CIiYY8IrWUuCEK^<0%de12B`zl>m{W(}{Z`2Ntmol^rNqsUN*8AzC3@rbn_}l='
    b'a~G#a(9@23;&3^x5tu`#E)SQHO%lv<4;c^e=W5FCc-p&+EHTwa0uN-HQ_bL*dgpF%AFxrQirsHF{U8>TwlLdE<1w3w`K)%I&GdGxp^Nj6mH4cC&j&3#M@!aP'
    b'yD2jPCZPG<FpNcqvKc~!@diZ=CXRQJX+q`kMha+TH36nVH^VR)9TH~1*a`K~z%dgFSeusXgi=sg%T4gXD&2hS1RN<z9rk947{fg&r7NAEf#fH($!syzPr`v@'
    b'X$DZ5&>BqIsKyB`oCK-N5DrZ<XT;Y@J=tFMGVsxj2O56ZDL{5oTccOKugQcVx!zCFOhGaeD&$X{28N5x1u0CKaALV};jG9uLEqg6CTMBxZtiC|xS64DICq{Q'
    b'9JUcN+QCbwk{K<wTerA4p%L<{G^t;$bhj`wM6+wp@Zrc5dm{%k0jTx+8&@~F>(A)u3ZyArGNq4Yn$XP<NZwAFC`q;y-pxQlpRsZ23N{rJrb>|(yyL=2cd7}k'
    b'e*`H`XnG<@GhXBnq&%Vj78)s|hj^ZWH033WSJH8RhIBv*Q#9VC8}5$`q$$0?(PG%8DPGWfuT2<JmIYy4PiqtU3AQtRL8vp3rgYnX6?)I7;AS9A=?yGMe#Q)j'
    b'bZJKP#d9t*dUFE_4Y|ix1S<>YxW-RibH~>^*H_Lo0}1`O#t$q>_VmNOJYR(<k!}J~n$%xZ{AtdZa^GRhL28{8%M7IUz*?wNkm{6Ju-dLnK`K);zIs8Of>fv2'
    b'uFt!1jiYZY#x?K>?tVi)GpQ^>aTG^!6i0CsM{yKKaTG^!6i0CsM{yKKaTG^!6i0CsM{yKKaTI3==XoE%?ljzb)<|Cd?eDL@ySc@;v-B*0Utize{Pm`Pe7o1k'
    b'!qm_{&fag#(0&-DD$m{hq5RC=``ht(I(c5>ut$4;J=!fy{@5?Kx4-@M_U6$xVOz4h;#2kByWmqYEm6{ZW0G+tRA*}OE~Q*XGA$k_wm$iqtnp@{sGT`@Tcce@'
    b'P>l1&Gl+BcuKH|)iPgC*yeWlJiZj+P#?F?)>ryt!l~{vW#;_Z2D#<6~7Zq3U@TlQFdQQnV`EpF&*An*gtS#aglS?)iyV%{?u$!Wzjn&3dVpv8LhbkJL<XDT6'
    b'lXFd4lY<K->@|~iA>ND~d#HLVTAsPq812?tv`38I=H-XzO<sP4-lnAo=uKLFeBP$zhv$oV=SJs?wLCXsT<lYmL*&I%Xb;{UBJ;%|a%y0HWCfJIAu*pic=$kZ'
    b'-$#g^b}V_&C&WHGu$+q7pPkQ*64sHj`UYUbkPuEP`{M|}SdW3;l;rtk^JsIBhJ*;HBYpm~L|2PEB*bW~KFU1HkPt~)YSa+`TZe>b{a{*w_z1vQV}Mr$jZT~$'
    b'0g(O#&qk=dh}exFpk)8~Qb^aBky>`C^Y%k>*j@)ehJY$zKN4llNCiD&<Pd<zLNNf)+fap(=n{qidZ~UGnb~Owpdh>r08|N1VQ50sF@&|hKp5J#jCrH$9R)_V'
    b'9m7421R{*>U1Hz7q%nx0PDBEchn7vZF8*~4q7E%v=;>jGRvkdtp(O(lV*wu!vbBH4@nUiflmaM#0w{n2D1ZVefC4Ch0$eS?6Aui}&KY}VX4S(ysYg?){_*RL'
    b'+euc*-1|&~FHzpRd!KFaDQEd#C8X+H@yov$?$2?4&+*7eYz{63lS;O>F4TAc!5Cj`jVXi@eX4Pnp}1<It2Vf7l8sirQQG#U(3)Cp45<{i&q!ho*_4=F^(B;Y'
    b'+(5jG*~jXwE5&3R544WWCWH{%ze+KRQqFzWA2^iY?m2P{hge8H=-YVDlcPPtZBx5M`^J}?bIHrtid}S;Z@#wqsOkK5`eqqfslJ-!pS*a@GMaK+oIAIZ-$yf>'
    b'(f`bS&GcFAjd_^Ve8f7mIgmq^p{<b|vI=bu<bXwJa~y}PL7O8vWC^-_B=i;N67%e|0A1j*`>j70&f|TSpNqpAfAzUI<kJ_Q?HvL;jrl1<A!jx}VJPHe=ckN>'
    b'oB#ZTk&siOpE441mh|9ICMHe~nrC8;@1V=hOmiNb#|I6CorFCY^XKJdU%ov!WbN4=$q`G>=17iMdA0{~z{0aRkR#Te?SUMz>|8t&_NsHSZP+pGVsE7f`im#<'
    b'F(Wx-#kn}ppD#Gy4i02u9nF?tqm?xqnC)G*DG%~I0G;tB+L`otL~b@_OYocsDH*_%6^e(-W;`r(4|K51Y8!H_@M_DMVwb(l1}zgFq&rt=Bw(iTC$8^7da=?}'
    b'g~H{_>^L%5g|`hk<?Y{ln5oNNXM@%W&kCMN4{w@{*{0`AX9{AasS1V5*U4@_TBNxRIaap0WurXl(XMmQ_BxrHtk5Y>j-F$-cYJ0#Q?GBCs?Y{H<ypMDprbXs'
    b'+mK^by<5)Ip9GwFW)#pF52~I?j~63nV=mKk=9HJ}tH}z5%iGCrKj}I4Gsv-`?=5GlU3NDcbjB;hXVOo3{PzsAz5F<JYn#PNQxyuAcaz<Iv;)94<XBIDt#!^!'
    b'dIs|WsGsme@|pB_M|3vkGCijryNg(9szTxNezMz-Hi+1U9BUb|<xJ~ipJ6s=nDAoune_6;>151hdQLrdSFzGmg~H{-WVavfAF>TO)=^~3nOv7W&IWBO=wyZB'
    b'o!Z%$%k-Rjk72}0QxyuAkCWYgxV_9a=2*j-EpPH&_%s`I#zX37(l^}cnC$>M^(MoLnWkzKPM;<_{&@SLM?l9K5^XtD=;G(upn1ZxzUSgM;Q65K7&`Sn!-=7$'
    b'>J*NjCp-UegQ`a`$68ixc~tBkl_rDwp{`7ii0>l-w0%{b8cn^}X{t&asF!du<s<$5ZZvLY0)qTfNQG2Lg;Yp|R7izXNQG2Lg;Yp|R7izXNQG2Lg;Yp|R7izX'
    b'NQG2Lg;Yp|9E2SHKz^tD^62=U*^l{>Cd>bGuSN6ApWocxeEM{Q;`^8X`_0E6Z$AC*hc_QTzWw<7_aA;lU+4dL^Xcuo|8w(ck?gD1Cm^6}MX2p}DFgrfe;-c<'
    b'diC<(Z{B?Pw_iT~@XsIK{`~s?{POAM`#;{Sm?rmj1JZnMMMXP^FF^kBZy#<xzFr3W;k)-IC?{`wdTAxmN=yZ;xCZuZlmF$veR%tBu@+iR|8(>52ecpf@0b6&'
    b'{O~Uy-rWAj?fai^zVCnNU*7-nanbgFzWwyWBEsz-e);tCFQ1k_@#$g1>aV*b?Z3TqIhs&X@V=Umq@Tpxt_^4UxJw`J)9=h4&e+8y*~PsE@QC)~vFfMO$D{Qh'
    b'4|TtI?A(h7J6}B3`A)tc@&^5Wb3f)y=RcZ%H|rmy{&=wZ<FV=&9&258p+@UtN~XrJC%Fm6-6i*X&b&uu-^K6;3LlR&d^}Y1U*7Ib?qv7W-IjI7ZZ`S+@nH4G'
    b'W7QuIR{t0GJ3Bi6=6biE`VSI69xVQsmfU@e|5)7L$Mna^9uJj$op$NqQ%*kike3fV;9nzqJk;~{TW|8Qt9?FpueZI|Dmfi|w`q+#bhlm0!Izu6m>?c(f_ShA'
    b'zPRNrDSCVKHDBG+4GtW_m$siZl;HD`w?50yd_MB#WuF0jaYZgM#dPp~u*O4|<+_&-x??XsUB2gm``$QjlkYY8u95vnr`zr5zbX1&NB^VPzo2<*?4GOMmIACl'
    b'Q2TuHFCT$SI`sT;>|Ot{SKWu6Iu1Q@?C5lxTm54X8b_Wn_R;)f*StqwF&}!U*w5iNHuMLcC63(E?dIwm%ldH}3MTWx*+R!A3my6y<Jhkl$6n(f{L%Q>1kHml'
    b'kB`4JJv3SB;N;+gzg!%BReS6;<&i0Zhu+g2c};g{n#iHoWJlf-9h(z)a7y5z*EC1o(j0nEao}P7xD)F&9NZ45u{yNA?C9#cqpK?qtt~yauJ+)%(qqd?53Vdb'
    b'xUTTvvchAl3XiR=I<~Cs$cny0E9wreD>}HU?AW5RgKNr;E$TV8qUzv+szZxv4y|T7w3zAOdY)s;c@C}SIkukV*m9QRYZ;C&XgRo^<=}FbD=4KnzLMhjDu$zr'
    b'7_Oj%;MfX+V>9@VOyEB>fB(=N_Cr(HkIx}LGKKu$B<>?~xDQR?J~oZ{&@ARd(})kuB0e^e_qaUXLvv}roJ#xcRAxMgD{Wufo6TRnpsic4Jf4N-;kReJnfUEZ'
    b'cP9Q~-SpLq%*0=&O=04fuU=FpeqB_=^q=<1xZydFco37pwO8l46!O3~lfh#mR4PGh&K;->wwXF|DI#+|*o1&>c@fFBuI7nK(X>>k3<k>%Q%e<r+Zif@YiqOR'
    b'Qds8l(-;bK{j{=w;cWn%mmL_9p>1G1m7=LAaD|YKOrjDjQOR)`T%*WbicFmkPTZ9@rSXJ@<5INQP^lEQ&p950H*i?uZlf`@-G;YR3U8^?u2HmUmzdG7ZD>3<'
    b'gc~YDdvd0+5GkM|&y^y`o+eWnGBt)nhK0gMDus{S-DN*Adg8>+a_(hPEPKmFL!^L`3SCj4s9cI=MGb~(i>55z7rs}a+k!~ZwjF^h1vXEWN&zJ`DLj|LbDb79'
    b'bAfjw6e6w(m<-FB+E|zr3wq)*WL(V^DnWB6E<<P(l}k~XSEO*H#1$fn5KL3Zt{@ujq@yxKE0&1d4O-;u2^5Y?;ixX#ZjzTE9(hY$`=sAkh!kz!H5wv?mz9XD'
    b'Cj^kfrD&#z)VYnx$J_A7+$SFQOaYoijZmIT0VOqx!lfwGAlM{miXtAqBH*ct!Z*RDC|)Q}{icpdv6#EjMDBvrXvm6!B#uk5tlY^{?=+ja6YuDfqTFdRDVm}p'
    b'l>$mKbVY%}b19lF5_RgeEkerF0D>7#r04;JNC71kx}rcq4(62`2D?WQH=Lk|R7JV|^(gapAh~~0Wl}85QKKPJKuM0SC{TDVMYBbq-jl=Jym^t6+><jYnxYbw'
    b'0!p%UMS&u4Dcan~)T!6DYPnDY2xd5uqW0NcsM}`Ha23@k3OAS+Lk)wWe`qVb4{gQChc+Tbn|g&yfhe1(6i`z857*qqQ$Kn(2@nc1mm*UY)n;}JB89hJl-L6Z'
    b'_r%(0h!nUv;8H+IjUsU=5;d4N32?kmT#7_hRLiAo1tKL=DN38&#P6#{QhiFLQk3?oo0v^hCB39tDn+$aMYYsfn7mLaN-OarCWZ#&e^k$9@YI=Cdv-=(GSom-'
    b'Qxl+lP3JXE0Y!~eJryZBs)@-^Td^YX{xr&W=vt^0wNVh`c#-PhOl7E<t0yNPaIG;^js>4O^O_88VI?lAjiMT^s@l|c;ILGV1)my2@TCf7cT|oAzx~ErG@3D5'
    b'F@ZIK%CX>ct=@M3qA^e9Sn%6##1B4BK3iFns2mGE*?+5ixgsu6jiQou)v9?MRF$b53x4~Jcx@ZxyN@-M%CX?L96915lBDdAc&KR<)p3p9?(v{6qN*~gtXllF'
    b'#G`VrTV^`1tWkx#P_@}npe#q_u+ol&xOMk(*=?<-a#+i~glRH}3v)Rv3Lc5dYF^cDSuL@Hjd*V0x^ELgwn34~vEXyHWpSU2v{hmwm<s2OWD+mOXeI|VRXv-e'
    b'1$c`V5{ArzLkY8cj<BGR+Ob*CL#$FAOs0w>hREC<jLA{t0}GP_iYkRn;=*aBI5G>o%SARz3z9CeSrT`q;ND3BKC#I}P5p+8N|NQCoXG)AVd-L$xX<yvvRT@U'
    b'^oGph*=v{kymlFGpp>~n>`^4wDxjjWl=TLO$zo5ZU?z)q>wIBGO7GSc%zH8mN{M`6vjpyZ!Ja}KnYS3XOD_-+IWSLfyT&B3=`<smEnU-TAC|~0*t_^lW<g&j'
    b'>Wob5jATX^iIi;x^MxGsWd&ohgj3Wn<ee+1m@K}oyCmk$LRbtt>en^u2evGMy?YIIjWEoUp0FU1(vewOzPAmY&EmO{zxG^8rX<MufFM+(oQ~gAqlA+zk<Ajx'
    b'%Q0B691|U^^fXtdzQlne*^Aff!$6#kJztH=5hSsX%Hbs$mC0d4KHVK!HVYiMkXZt(QrRrzJ6-s2;7TI?TggU==5%fB*es50dayua(UMuB<!<s2z#>-?I4}gE'
    b'8pW-#g?Xb37HQV*$t=;cr=(lsBr)c<gg=Qeg~}m<P>pi>@I{^Vr^!NWQ_@-3M?0_t@&`#oFJrh0lMu<aJ*pB6*(k=WMxi=bI(_-7WER{{#Y|>tUHL4tC7-Yq'
    b'^7>^?WeQALzyevQb~)WnGH>+a=|(THS<o|)t}%Erb5<f5P+TCBSs)A3E@%;lotS5{$gZ-mWx<nxj?9uAc{65CH8D(Cz>?_EGWEI`s>0Ih$W-I|^&<=OqolAv'
    b'mOy4nO_mhdERp>23q>WU^kK>Z7RW-i%juIe^FBYFKCdS>OUip_EU{;$RAm^lEMSpY$+SyZH+{@m2^LR}Fy%BWE1QMA8JA*3N0vnbB|BPXvqqS}X2IvYY{@Ly'
    b'l4m7Y5G{$3zuI0Y$5a?dGWkocNMYGl0Sl}`^)PojhF3BRW<If(rLds1lzDU&SqwQMBN(HOk*P8JS!2vJ#ITk!GVKBu*k#e!w^M0e{`t*!H?Mzs^XcZp+c&o#'
    b'U;gIBpA1Qk(=R1Z0wquaB~St-Py!`T0wquaB~St-Py!`T0wquaB~St-Py!`T0wquaB~St-Py!`T0wquaB~St-Py!`T0wquaB~St-Py!`T0wquaB~St-Py!`T'
    b'0wquaB~St-Py!`T0wquaB~St-Py!`T0wquaB~St-Py!`T0wquaB~St-Py!`T0wquaB~St-Py!`T0wquaB~St-Py!`T0wquaB~St-Py!`T0wquaB~St-Py!`T'
    b'0wquaB~St-P=YHZ_;xD8%b(tSy7}<-&F#zIOdk8ozy1C7cQ?1U9~Wd7=R*Jb`u66pH-P@r*XA3O<5w@*f5+v&KmS*blXdms{q4;{`SK4R-u~t7yZ_hTx%IYf'
    b'1X1{}=uI*Z7kj_FI)U4w2pTjk@)Q`V#n?h@Ns#EKLD2u+y-=|fQ%USSL*-$C0`Wuj9nNsLyClzWr#GW_^M9M!Xx&^k^HqDgTF)0DnWM|)?P|Gb7VY@I!}{ab'
    b'^TpLoa~=uL@76cX?2n9jecd!|Q28|er&+i2%O*uRN#ThcrsBqGrkqhydZuiOmWvZuw3DNW3AZce@M5ROQ|n12mzr7WjFeVO%gk`6a3JNL40EZxFkBiVlo4JH'
    b'cyfo5HdabunUKsXu1%8GS~6pmw?f(Q4^_gCC~X}#E@*4Rq?cA@ZDqU^nhC2#_=haz#}qf*TQ3xsK2)3Uk{%943oDol73YMvG)X_Ew9uA0t(|jRa+yaJ<CU_)'
    b'dL9OscpOw2Kccp?l6fb!3>TAkK4)AT?ws@?-I@zWG&>$sStu4pPA{Ezg5|5rD(N^6*IW3@Sx%SlqiJ&<bhUEMhDpOK$8(*9(S$R}v}fE1PBWYyRXXHanQ(mx'
    b'9aacD4=TolG1iA`ES8{khAQJn)D||Bn%7}zWDN89E`sYYpO`RphT0P$`7{|nqH-EIl=hNw%k#w*mI$H7!eq+Bav>z1D&5~BU33dKemC9TKZWZj$VyNs6ZUMx'
    b'fjFIT42281)Igj`x#PfK4G<S5e;E!C7_0^2Vp#(VB^;Up;(RI;)Vg>QZn8WO$62Zr4U9G-VLZ-Ltr%pyk!gVEBUFn;#_Nzgnd-&CcyW}HNTA9U<B<_ZC=RG|'
    b'$#4dZSwo2;l?~_6paqm@bLGGu{!QY_HBoUymurVhXw(i$^j+~NXw)7`G+p&*Xw(Kt6uhe**i<0GFqWt|qUfr}BBM@J98q@F<B(A&szaWcR6QOUb)w>kI#-W?'
    b'O$s86WQmF+np{1wJLMd;ff8-59wDGnTPRWG>JbtewSp2&S3L@Pj3yDwA30oX->Ro)4;<_XsJzOnyvnP*%B#G}tGvpqyvnP*%B#E|fLHbaVaJhQbYx(=`t9`Q'
    b'=DcZUXLoJ8Ts$<WM-!&czI(A}W|7I*A(*s9kH^0$pl||iUqE#NT%ZJeZv@g=S^*0XFoHNmodDfQ{;B}O3DBM7uL`7-{Kz3_$0(JZO;3NCJdw%qQUFkehMws4'
    b'QbmC5P_jh;TjE2A09RrYhyY*WB#B96ML8%n$HYo3GIK;gkzFO0a*<hMQfhFC*FupYC<06j;VA>c{%Z`8T!7#E-(&T5Rz2d8Kiz3Gl#l%BZX@CS<Y^v#^p9U^'
    b'eYw^euckLm+cs$o9>2;z_+@#wnJ=y`UNp_>&n6`2SsMOr_6MhfP4Dzi;$QX~j?c;X>}I-n-?bTDyqT_V-(1gwVuHHVAmx(Z+WIZieH(heCcJog*EX}4;m9*G'
    b'%}3eGti<P|j4Oqcw=w+jtLds)pG~jQV)C}xT&F4M)A;#v(asllA^5Xp0N*yV{C_TIAK%Q|>t7cirt8`3`K<Z*ZnJ6HO>ehkw92Gb5u6eB@QggT7#mDzkf2VF'
    b'AvT!OwlaQ_V$ez)L@%!s28(U5&`yt_H&`yCm~>s!eC~T@lK%W1Ns<k#He7tCN0b~^?!Ib<7-xo8WNyG=bgyIv8*7GD95A87tj2aOxwmMk2akU&VKh+!*frDt'
    b'>|yIo_T(xa=%4RZ$qi|=kr=Q|`p^R*fosk=B;kmwmv@$O!KhV|g<Dao*px2XNG#Zk-YX)~qe5y4PhGuR=QSr+;lOT{UX|PmN*jp-Hzo9n<Y&N~S_9c;*nir$'
    b'EgXVeMF883dR4kcUfNJRxSga|BzNj_Y7J<MX#a`dcHc;H6$$JR>sRUeu!&<~;9j6!6`k%I46%fvu3>J$ZFdJ%(rp9n7|C<O9JNRcg|>!;f_}K9Ut`<tO&$sG'
    b'BPWL=k<^QNp`af`IUI?iUPH!6fL}W~9Eql0um}bH(8}RR4E5Y7@|!bF9!dUo0?nhYePaXpH=9QTd>6WERE?@pHL6C{s2WwHYE+G?Q8lVY)u<X(qiP&S1OEVv'
    b'Y{#xqUn9$=owoDKQFFU$KaMu@S#x@onl47G*pe~YTrXFv`QmEy_w?$%y(IvMQv3Mckgqf~kH+WgfIGjLw!g2M#b2-6^>o$0^_J;e^~n(~T>0bAhg9huhPvGi'
    b'En^ka6j)deK4a;quoRfx-U`&|G8FNv{Tkq)W7Ydusliw%Rqas`DWFL#O<qaTN|jaoKu9wVl8h`A0}IKNMKcMI%mF>)>Qh!?!0#e-$A#F2rgM#%a*8Q7OLvxQ'
    b'UrzDm+11$>SZYO@XvjVs6NfRbB#s2+m|;vC83eE`<^~FYWg&wsAk`^9fX0yw@`z*`j43>WI3n2&WA)4+2}m}iqiDhq`%+Cf#0?oSX}cZ3&;juJCyp*RM&=7u'
    b'Bd)J)@09^u7O9^{BCao4-j0yB>HrvnGYDW|zu%a{0YHd7L++ir3IS4xnWNj<snlklLFL^bpxw^8E#itx5#fJ~lyX04*U@9kDe2=lPrj`n*(9Q3DyCv8reZ3l'
    b'Vk)L$DyCw7ILwo78VWxQ5A$~PnI^vKvN)SwzW+{>1@I-%mq@^Swa?Z9;QPM^OjPJwrXqu)qBlEC)LAkF!K>Xf&oRfTcbQT{nF<M2dr(011PLX`Cq+7mvI!pR'
    b'2!=X}0fb=uz)wX4Lp;R@-!pDLVWk2#O+Y*o5X%I_F#$15K>QLQy9CB90WwQqyb>s@1j;FaGD@I)5-6Jl$|Zp^NuWFuD2oKjAptQ+K>QIHdj!TE0WwE`yb&mC'
    b'1j-qKGDe_$5hz;($`ye!MW8$pC`$y&5rHy9fcy{`I|RfH0Wm{Bybus8M2QoE%m`5_l~O5{QYn>EDV0(wl~O4KQJ!)mP-bp`c^i7H3J<nw{bH}y-`3N2ZTbjB'
    b'+Eevxz5KAq8=$KEvM24+n(ksxKJT#_{+f)VQ2JpK+FZPtuHPqG{<+8-dgo0D<4ef=d!IK@{qKK=JG{v'
)
BASE_COMPONENTS = _payload_ast.literal_eval(_payload_zlib.decompress(_payload_b64.b85decode(_BASE_COMPONENTS_ZLIB_B85)).decode('utf-8'))
PALETTE=[('Floor_SoftNeutral',(.52,.54,.50,1),.86,0)]
MATERIAL_MAP={}
for key,base in BASE_COMPONENTS.items():
    mapping=[]
    for name,color,rough,metal in base['palette']:
        sig=(tuple(color),rough,metal);found=next((i for i,p in enumerate(PALETTE)if(tuple(p[1]),p[2],p[3])==sig),None)
        if found is None:found=len(PALETTE);PALETTE.append((key+'_'+name,tuple(color),rough,metal))
        mapping.append(found)
    MATERIAL_MAP[key]=mapping
PLACEMENTS=[('LeftBay','Gondola',1,(-1.12,.65,.06)),('RightBay','Gondola',1,(1.12,.65,.06)),('Checkout','Checkout',0,(-.60,-1.45,.06)),('Cart','Cart',3,(1.35,-1.40,.06)),('PrinterOnFullBridge','Printer',0,(-.425,-1.43,1.00)),('BagInTerminalWell','PaperBag',0,(.15,-1.45,.76))]
def placed(v,turn,shift):
    x,y,z=v
    x,y=[(x,y),(-y,x),(-x,-y),(y,-x)][turn]
    return(x+shift[0],y+shift[1],z+shift[2])
def geometry():
    out={'FiniteGroundFloor':build([(-2.8,2.8,rect(-2.4,0,2.4,.06))],mat=0)}
    for label,key,turn,shift in PLACEMENTS:
        for name,q in BASE_COMPONENTS[key]['meshes'].items():
            mats=[MATERIAL_MAP[key][i]for i in q['face_materials']]
            out[label+'__'+name]=dict(vertices=[placed(v,turn,shift)for v in q['vertices']],faces=list(q['faces']),face_materials=mats,material=mats[0],role='Unchanged complete source prop in new fixed scene placement: '+label+'/'+name)
    out['FiniteGroundFloor']['role']='One new finite floor slab for the small store layout; not a separately counted prop'
    return out
START=time.time()
ASSET='retail-two-gondola-aisle-checkout-scene-01';VERSION='1.0.0';TITLE='Two-Gondola Aisle and Bagging Checkout Layout'
DESCRIPTION='One original fixed convenience-store small scene, not a new set of constituent props. Two complete previously delivered double-sided gondolas flank a 1.44 m nominal central gap on one finite floor; a complete belt-and-bagging checkout is placed toward the front with the existing receipt printer seated on its full raised bridge and the existing paper bag seated in the real terminal well. The existing lattice shopping cart stands beside checkout. Original source geometry and opaque PBR signatures are preserved under exact quarter-turns and translations, with no scaled or recoloured child assets; a simple finite floor is added. Metres, Z up, front -Y and floor-bottom centred datum. Empty unstocked shelves and fixed empty cart; no people, roof, host walls, cash register, animation, functioning conveyor or checkout, verified pedestrian egress/accessibility, load or store-safety compliance. Actual reused props retain their declared limitations; the 80 mm belt-to-bridge gap remains real and is not described as continuous transfer.'
G=geometry()
if '--source-check' in sys.argv:
    print(json.dumps({'status':'PASS_SOURCE_SELF_REVIEW','review_mode':'SELF_REVIEW','asset_id':ASSET,'materials':len(PALETTE),'components':{k:topology(g)for k,g in G.items()}},indent=2));sys.exit(0)
FOCUS=(0,0,.70);ORTHO=7.8;CAMERAS={'thumbnail':(5,-6,5.5),'qa-front':(4.5,-6,4.8)}
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
root=bpy.data.objects.new('TwoGondolaAisleCheckoutScene',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='metres; Z up; front -Y; floor bottom centred origin; original props translated onto floor or full receiving surfaces'
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();
 for m in mats:me.materials.append(m)
 for i,f in enumerate(me.polygons):f.material_index=g.get('face_materials',[g['material']]*len(me.polygons))[i]
 o['component_role']=g['role'];parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
bpy.context.view_layer.update();triangles=0;component_checks=[]
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-14 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-10 and deg==0,(o.name,bad,vol,deg);triangles+=len(o.data.loop_triangles)
 component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
allv=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(v[k]for v in allv)for k in range(3)];hi=[max(v[k]for v in allv)for k in range(3)];bounds=[hi[k]-lo[k]for k in range(3)]
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
qa={'asset':ASSET,'review_mode':'SELF_REVIEW','blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'mesh_objects':mesh_count,'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,'components':component_checks,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),'status':'geometry exported; actual image self-review pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/retail/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'scenes','assetKind':'scene','theme':'retail','style':'original-source-mix','title':TITLE,'description':DESCRIPTION,
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
 qa['tiered_render']={'profile_id':TIER_PROFILE,'authorization_reference':'Current separately pinned R3 operation approval; historical sample contract retained, no old approval replay.','native_samples':128,'resolution':[640,640],'gray_stage':'omitted_by_authorized_profile','samples_by_image':{}}
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
views=tier_select_views({'thumbnail':CAMERAS['thumbnail'],'qa-front':CAMERAS['qa-front']})
seconds={};configs={}
for name,pos in views.items():
 tier_before_view(name);aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
qa.update(render_seconds=seconds,render_configs=configs,status='images rendered; maker actual-pixel self-review pending');metadata();saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
