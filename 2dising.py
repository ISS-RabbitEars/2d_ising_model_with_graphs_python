import random as rnd
import math
import matplotlib.pyplot as plt
from matplotlib import animation

def setplot(sx1,sx2,sy1,sy2):
	ax=plt.gca()
	ax.set_aspect(1)
	plt.xlim([sx1,sx2])
	plt.ylim([sy1,sy2])
	ax.set_facecolor('xkcd:black')

def initspins(n):
	sp=[]
	for i in range(n):
		if rnd.random()>=0.5:
			sp.append(1)
		else:
			sp.append(-1)
	return sp

def nn(x,y):
	nnl=[]
	for i in range(x*y):
		tmp=[]
		for j in range(4):
			tmp.append(0)
		nnl.append(tmp)
	a=0
	b=x-1
	c=x*(y-1)
	d=x*y-1
	#corner a
	nnl[a][0]=c
	nnl[a][1]=b
	nnl[a][2]=1
	nnl[a][3]=x
	#corner b
	nnl[b][0]=d
	nnl[b][1]=b-1
	nnl[b][2]=a
	nnl[b][3]=b+x
	#corner c
	nnl[c][0]=c-x
	nnl[c][1]=d
	nnl[c][2]=c+1
	nnl[c][3]=a
	#corner d
	nnl[d][0]=d-x
	nnl[d][1]=d-1
	nnl[d][2]=c
	nnl[d][3]=b
	for i in range(1,x-1):
		ii=c+i
		#edge ab
		nnl[i][0]=ii
		nnl[i][1]=i-1
		nnl[i][2]=i+1
		nnl[i][3]=i+x
		#edge cd
		nnl[ii][0]=ii-x
		nnl[ii][1]=ii-1
		nnl[ii][2]=ii+1
		nnl[ii][3]=a+i
	for i in range(1,y-1):
		i1=a+i*x
		i2=b+i*x
		#edge ac
		nnl[i1][0]=i1-x
		nnl[i1][1]=i2
		nnl[i1][2]=i1+1
		nnl[i1][3]=i1+x
		#edge bd
		nnl[i2][0]=i2-x
		nnl[i2][1]=i2-1
		nnl[i2][2]=i1
		nnl[i2][3]=i2+x
	#bulk
	for i in range(1,y-1):
		for j in range(1,x-1):
			ii=i*x+j
			nnl[ii][0]=ii-x
			nnl[ii][1]=ii-1
			nnl[ii][2]=ii+1
			nnl[ii][3]=ii+x
	return nnl

def sumNN(i,sp,nl):
	sum=0
	for j in range(4):
		sum+=sp[nl[i][j]]
	return sum

def sumSpins(sp,n):
	sum=0
	for i in range(n):
		sum+=sp[i]
	return sum

def sumSP(sp,nl,n):
	sum=0
	for i in range(n):
		sum+=sp[i]*sumNN(i,sp,nl)
	return sum


#-----------------------------------------
nx=20
ny=20
J=1
kb=1
mo=1
Ti=0.5
Tf=0.5
Bi=3
Bm=-3
N=nx*ny
s=initspins(N)
nbrs=nn(nx,ny)

frps=1
sec=30
nf=frps*sec
deltaB=Bm-Bi
deltaT=Tf-Ti
dT=deltaT/nf
dB=2*deltaB/nf
#------------------------------------------
#ns=math.pow(2,N)
ns=1000*N
rkbt=1/(kb*Ti)
for j in range(int(ns)):
	i=int(N*rnd.random())
	dE=2*s[i]*((J*sumNN(i,s,nbrs))+(Bi*mo))
	if dE<=0:
		s[i]=-s[i]
	else:
		if math.exp(-dE*rkbt)>=rnd.random():
			s[i]=-s[i]
#-------------------------------------------

fig, ax = plt.subplots()
fig.tight_layout()
dx=1/nx
dy=1/ny
if dx<=dy:
	r=dx/2
else:
	r=dy/2

TA=[]
BA=[]
TBmaxlist=[]
TBminlist=[]
time=[]
MA=[]
uA=[]
inmaxlist=[]
inminlist=[]
def run(frame):
	global B 
	if deltaT!=0:
		T=Ti+frame*dT
	else:
		T=Ti
	rkbT=1/(kb*T)
	if deltaB!=0:
		if frame<(nf/2):
			B=Bi+frame*dB
		else:
			B-=dB
	else:
		B=Bi
	#print ("T = %f" %T)
	#print ("B = %f" %B)
	for j in range(ns):
		i=int(N*rnd.random())
		dE=2*s[i]*((J*sumNN(i,s,nbrs))+(B*mo))
		if dE<=0:
			s[i]=-s[i]
		else:
			if math.exp(-dE*rkbT)>=rnd.random():
				s[i]=-s[i]

	#-----PLOTS-----
	plt.clf()

	#-----ISING MODEL-----
	if deltaB!=0:
		plt.subplot(221)
	else:
		plt.subplot(2,2,(1,2))
	k=0
	for i in range(ny):
		y=(i+0.5)*dy
		for j in range(nx):
			x=(j+0.5)*dx
			if s[k]==1:		
				circle=plt.Circle((x,y),radius=r,fc='r')
			else:
				circle=plt.Circle((x,y),radius=r,fc='w')
			plt.gca().add_patch(circle)
			k+=1
	plt.title('2D Ising Model')
	setplot(0,1,0,1)
	ax=plt.gca()
	ax.xaxis.set_ticklabels([])
	ax.yaxis.set_ticklabels([])
	ax.xaxis.set_ticks_position('none')
	ax.yaxis.set_ticks_position('none')

	#-----TEMPERATURE AND EXTERNAL MAGNETIC FIELD----- 
	if deltaB!=0:
		plt.subplot(222)
	else:
		plt.subplot(223)
	TA.append(T)
	BA.append(B)
	TBmaxlist.append(max(TA))
	TBmaxlist.append(max(BA))
	TBminlist.append(min(TA))
	TBminlist.append(min(BA))
	time.append(frame/nf)
	plt.plot(time,TA,lw=0.5,color='xkcd:red')
	plt.plot(time,BA,lw=0.5,color='xkcd:blue')
	ymax=max(TBmaxlist)
	ymin=min(TBminlist)
	deltay=abs(ymax-ymin)
	deltay=deltay/2
	if deltay<1:
		deltay=1
	plt.title('Temperature and External B-Field')
	plt.xlim([0,1])
	plt.ylim([ymin-deltay,ymax+deltay])
	ax=plt.gca()
	ax.xaxis.set_ticklabels([])
	ax.xaxis.set_ticks_position('none')
	ax.legend(['T','B'],labelcolor='w',frameon=False)
	ax.set_facecolor('xkcd:black')

	#-----INTRINSIC (MAGNETIZATION and ENERGY DENSITY)-----
	if deltaB!=0:
		plt.subplot(223)
	else:
		plt.subplot(224)
	MA.append(sumSpins(s,N)/N)
	uA.append((-0.5*J*sumSP(s,nbrs,N)-B*mo*sumSpins(s,N))/N)
	inmaxlist.append(max(MA))
	inminlist.append(min(MA))
	inmaxlist.append(max(uA))
	inminlist.append(min(uA))
	plt.plot(time,MA,lw=0.5,color='xkcd:cyan')
	plt.plot(time,uA,lw=0.5,color='xkcd:magenta')
	ymax=max(inmaxlist)
	ymin=min(inminlist)
	deltay=abs(ymax-ymin)
	deltay=deltay/2
	if deltay<1:
		deltay=1
	plt.title('Instrinsic Properties')
	plt.xlim([0,1])
	plt.ylim([ymin-deltay,ymax+deltay])
	ax=plt.gca()
	ax.xaxis.set_ticklabels([])
	ax.xaxis.set_ticks_position('none')
	ax.legend(['m','u'],labelcolor='w',frameon=False)
	ax.set_facecolor('xkcd:black')

	if deltaB!=0:
	#-----HYSTERESIS-----
		plt.subplot(224)
		plt.plot(BA,MA,lw=0.5,color='xkcd:rose')
		plt.title('Hysteresis')
		plt.xlim([min(BA)-0.2*abs(min(BA)),max(BA)+0.2*abs(max(BA))])
		plt.ylim([min(MA)-0.2*abs(min(MA)),max(MA)+0.2*abs(max(MA))])
		ax=plt.gca()
		ax.set_facecolor('xkcd:black')
	#else:
	#-----EXTRINSIC-----
	#	plt.subplot(224)
	#	setplot(0,1,0,1)
	#	ax=plt.gca()
	#	ax.xaxis.set_ticklabels([])
	#	ax.xaxis.set_ticks_position('none')

ani=animation.FuncAnimation(fig,run,frames=nf)
#writervideo=animation.FFMpegWriter(fps=frps)
#ani.save('2dising.mp4',writer=writervideo)
plt.show()
