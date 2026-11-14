# 0x88 negamax, PVS+LMR, 150k nodes, v1
import os,json,urllib.request as W
V=(0,100,320,330,500,900,0)
N=(-33,-31,-18,-14,14,18,31,33);D=(-17,-15,15,17);O=(-16,-1,1,16);Q=D+O
Z=(0,0,N,D,O,Q,Q)
Y=["@@@@EJJ,E;6@@@@TEEJYJJT^rrrr@@@@","  ## ,@E#EJO#@OT#EOT#@JO ,@@  ##",",6666E@@6JJJ6@JJ6EEJ6@EJ6@@@,666","@@@E;@@@;@@@;@@@;@@@;@@@EJJJ@@@@",",66;6@E@6EEE@@EE;@EE6@EE6@@@,66;","T^J@TT@@6,,,,## #   #   #   #   "]
P=[[(ord(s[(i>>4)*4+min(i&7,7-(i&7))])-64 if not i&136 else 0)for i in range(128)]for s in Y]
F=100000;B=150000;Nn=0;T={}
X=Exception
R=lambda b:[-b[i^112]for i in range(128)]
def E(b):
 s=0;w=m=0
 for i,p in enumerate(b):
  if p:
   a=abs(p);v=V[a]+P[a-1][i if p>0 else i^112];s+=v if p>0 else -v
   if a==1:w+=1
   elif a>1:m+=V[a]
 if not w and m<=330:return 0
 return s
def G(b,e,q=0):
 m=[]
 for i,p in enumerate(b):
  if p<1:continue
  if p==1:
   j=i+16
   if b[j]==0:
    if j>111:
     for t in(5,4,3,2):m.append((i,j,t))
    elif not q:
     m.append((i,j,0))
     if i<24 and b[j+16]==0:m.append((i,j+16,0))
   for j in(i+15,i+17):
    if not j&136:
     if -7<b[j]<0:
      if j>111:
       for t in(5,4,3,2):m.append((i,j,t))
      else:m.append((i,j,0))
     elif j==e:m.append((i,j,0))
  elif p==2 or p==6:
   for s in Z[p]:
    j=i+s
    if not j&136 and(b[j]<0 or(not q and b[j]==0)):m.append((i,j,0))
  else:
   for s in Z[p]:
    j=i+s
    while not j&136:
     if b[j]>0:break
     if b[j]<0 or not q:m.append((i,j,0))
     if b[j]<0:break
     j+=s
  if p==6 and i==4 and not q:
   if b[7]==4 and b[5]==0==b[6]:m.append((4,6,0))
   if b[0]==4 and b[3]==0==b[2]==b[1]:m.append((4,2,0))
 return m
def M(b,m):
 i,j,t=m;c=b[:];p=c[i];c[i]=0
 if p==1 and (j-i)%2 and c[j]==0:c[j-16]=0
 if p==6 and abs(j-i)==2:k=7 if j>i else 0;c[j-1 if j>i else j+1]=c[k];c[k]=0
 c[j]=t or p;e=i+16 if p==1 and j-i==32 else -1
 return R(c),(e^112 if e>=0 else -1)
def K(b,m,t):
 if m==t:return 100000
 i,j,p=m;v=b[j];a=abs(b[i])
 if v:return 1000+abs(v)*10-a
 if p:return 900+p
 return 0
def S(b,e,d,a,c,p):
 global Nn;Nn+=1
 if Nn>B:raise X
 if 6 not in b:return -F+p
 if d<1:
  s=E(b)
  if s>=c:return c
  if s>a:a=s
  if d<-7:return a
  z=G(b,e,1);z.sort(key=lambda m:K(b,m,0),reverse=True)
  for m in z:
   b2,e2=M(b,m);s=-S(b2,e2,d-1,-c,-a,p+1)
   if s>a:
    a=s
    if a>=c:return c
  return a
 k=(tuple(b),e);t=T.get(k);u=t[2]if t else 0
 if t and t[0]>=d and t[3]==0:return t[1]
 z=G(b,e)
 if not z:return 0
 z.sort(key=lambda m:K(b,m,u),reverse=True)
 w=-F;y=z[0];f=2
 for n,m in enumerate(z):
  b2,e2=M(b,m)
  if n==0:s=-S(b2,e2,d-1,-c,-a,p+1)
  else:
   r=1 if n>3 and d>2 and not b[m[1]] and not m[2] else 0
   s=-S(b2,e2,d-1-r,-a-1,-a,p+1)
   if a<s<c:s=-S(b2,e2,d-1,-c,-a,p+1)
  if s>w:w,y=s,m
  if s>a:
   a=s;f=0
   if a>=c:f=1;break
 T[k]=(d,w,y,f)
 return w
def sq(s):return(ord(s[1])-49)*16+ord(s[0])-97
def uc(m):
 i,j,t=m;f="abcdefgh"
 return f[i&7]+str((i>>4)+1)+f[j&7]+str((j>>4)+1)+("nbrq"[t-2]if t else "")
def pf(f):
 w=f.split();b=[0]*128;r=7
 for o in w[0].split("/"):
  g=0
  for ch in o:
   if ch>"9":
    p="pnbrqk".index(ch.lower())+1;b[r*16+g]=p if ch.isupper() else -p;g+=1
   else:g+=int(ch)
  r-=1
 e=sq(w[3])if w[3]!="-"else -1
 return(R(b),e^112 if e>=0 else -1,1)if w[1]=="b"else(b,e,0)
def A(b,e,l,r):
 global Nn
 m=[]
 for u in l:
  t={"n":2,"b":3,"r":4,"q":5}.get(u[4:],0)
  i,j=sq(u[:2]),sq(u[2:4])
  if r:i^=112;j^=112
  m.append((i,j,t))
 m.sort(key=lambda x:K(b,x,0),reverse=True)
 w=m[0];Nn=0;d=1
 while 1:
  try:
   m.sort(key=lambda x:x!=w);v=-F;y=m[0];a=-F
   for n,x in enumerate(m):
    b2,e2=M(b,x);s=-S(b2,e2,d-1,-F,-a,1)
    if s>v:v,y=s,x
    if s>a:a=s
   w=y;d+=1
  except X:break
 if r:return(w[0]^112,w[1]^112,w[2])
 return w
U=os.environ["MAKEFUN_ENV_URL"]
def po(p,o):
 q=W.Request(U+p,json.dumps(o).encode(),{"content-type":"application/json"})
 with W.urlopen(q)as r:return json.load(r)
while 1:
 g=po("/game",{})
 if g["status"][0]=="d":break
 while g["status"][0]=="y":
  try:
   b,e,r=pf(g["fen"]);v=uc(A(b,e,g["legal_moves"],r))
  except Exception:v=g["legal_moves"][0]
  g=po("/move",{"game":g["game"],"move":v})
