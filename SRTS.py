import math
#import canvas
import zipfile
import csv
import requests
import os
from StringIO import StringIO
from collections import defaultdict
import andyconfig

try:
	os.chdir(os.path.dirname(__file__))
except:
	pass

def schools(file='results.zip'):
	with zipfile.ZipFile(file,'r') as z:
		with z.open('results.csv','r') as csvfile:
			reader=csv.DictReader(csvfile)
			#print reader.fieldnames
			res={}
			for i in reader:
				if i['EstablishmentStatus (name)']=='Open':
					if i['PhaseOfEducation (name)'] not in res:
						res[i['PhaseOfEducation (name)']]={}
					res[i['PhaseOfEducation (name)']][i['EstablishmentNumber']]=[i['EstablishmentName'],(int(i['Easting']),int(i['Northing'])),i['NumberOfPupils']]
	return res

def circle(sides,size,centre=(0,0)):
	midres= [[centre[0]+math.cos(((math.pi/180)*(float(360)/sides))*n)*size,centre[1]+math.sin(((math.pi/180)*(float(360)/sides))*n)*size] for n in range(sides)]
	midres.append(midres[0])
	return midres
	
def getaccs(pts):
	endpoint='http://fme.tfwm.org.uk/fmedatastreaming/TfWM_Self_Serve_DataStream/TfWM_Self_Serve_RTC.fmw'
	a=''
	for n in pts:
		a+=str(n[0])+'%20'+str(n[1])+'%2C'
	geom='POLYGON(('+a[:-3]+'))'
	#print geom
	start='2016-04-01'
	end='2018-03-31'
	token=os.environ['RSTOKEN']
	payload={'GEOM':geom,'DATE_FULL_FROM':start,'DATE_FULL_TO':end,'token':token}
	alt=endpoint+'?GEOM='+geom+'&DATE_FULL_FROM='+start+'&DATE_FULL_TO='+end+'&token='+token
	
	n=requests.get(alt,timeout=30)   #(endpoint,params=payload)
	#print n.content
	data=StringIO(n.content)
	reader=csv.DictReader(data)
	res=defaultdict(int)
	
	for row in reader:
		try:
			cls=row['Casualty Class']
		except KeyError:
			return (0,0,0)
		try:
			age=int(row['Age band of casualty'].split(' ')[0])
		except:
			age=999
		ac='notchild'
		if age<16 and age>0:
			ac='child'
		sev=row['Casualty Severity']
		res[cls,sev]+=1
		res[cls,sev,ac]+=1
		
		
	criteria1=0
	ctypes=('Passenger','Pedestrian','Driver or rider')
	a=sum([res[n,'Slight','child'] for n in ctypes])
	b=sum([res[n,'Serious','child'] for n in ctypes])
	c=sum([res[n,'Fatal','child'] for n in ctypes])
	#print a,b,c
	if a>=1:
		criteria1=1
	if b>=1 or a>=10:
		criteria1=3
	if a>=20 or b>=5 or c>=1:
		criteria1=5
	criteria2=0
	if a>=1:
		criteria2=1
	if a>=2:
		criteria2=3
	if b>=1 or c>=1:
		criteria2=5
	criteria3=0
	a=res['Pedestrian','Slight','child']+res['Pedestrian','Slight','notchild']
	b=res['Pedestrian','Serious','child']+res['Pedestrian','Serious','notchild']
	c=res['Pedestrian','Fatal','child']+res['Pedestrian','Fatal','notchild']
	if a>=1:
		criteria3=1
	if a>=2 or b>=1:
		criteria3=3
	if b>=2 or c>=1:
		criteria3=5
	return (criteria1,criteria2,criteria3)
	
if __name__=='__main__':
	import sys
	for n in schools():
		print n
	print schools()['All through']
	print schools()['Not applicable']
	#sys.exit(0)
	#import canvas
	res={}
	
	z=schools()['Primary']
	r=schools()['Secondary'].copy()
	z.update(r)
	r=schools()['All through'].copy()
	z.update(r)
	r=schools()['Not applicable'].copy()
	z.update(r)
	
	ctr=0
	for n in z:
		try:
			j=int(z[n][2])
		except:
			continue
		print z[n][0],
		size=0
		if j>250:
			size=1
		if j>500:
			size=2
		if j>1000:
			size=3
		if j>1250:
			size=4
		if j>1500:
			size=5
		ep1=circle(30,1000,z[n][1])
		ep2=circle(30,250,z[n][1])
		ret1=getaccs(ep1)
		ret2=getaccs(ep2)
		fin=[ret1[0],ret2[1],ret2[2],size]
		res[z[n][0]]=fin+[sum(fin)]
		ctr+=1
		print res[z[n][0]]
		with open('tmpres.csv','a') as csvfile:
			writ=csv.writer(csvfile)
			writ.writerow([z[n][0]]+res[z[n][0]])
			
		#if ctr>10:
		#	break
			
	
	with open('result.csv','w') as csvfile:
		writ=csv.writer(csvfile)
		writ.writerow(['school','child rate 1km','child rate outside','pedestrian rate outside','population'])
		for key,value in sorted(res.iteritems(),key=lambda(k,v):(v[4],k),reverse=True):
			writ.writerow([key]+value)




	

