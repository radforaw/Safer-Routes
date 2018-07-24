import math
import canvas
import zipfile
import csv
import requests
from StringIO import StringIO
from collections import defaultdict

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
					res[i['PhaseOfEducation (name)']][i['EstablishmentNumber']]=[i['EstablishmentName'],(int(i['Easting']),int(i['Northing']))]
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
	print geom
	start='2016-04-01'
	end='2018-03-31'
	token='19fd8a6088b655e8db3d19ab801d36a924d9e17f'
	payload={'GEOM':geom,'DATE_FULL_FROM':start,'DATE_FULL_TO':end,'token':token}
	alt=endpoint+'?GEOM='+geom+'&DATE_FULL_FROM='+start+'&DATE_FULL_TO='+end+'&token='+token
	
	n=requests.get(alt)   #(endpoint,params=payload)
	
	data=StringIO(n.content)
	reader=csv.DictReader(data)
	res=defaultdict(int)
	
	for row in reader:
		cls=row['Casualty Class']
		try:
			age=int(row['Age band of casualty'].split(' ')[0])
		except:
			age=999
		ac='notchild'
		if age<16 and age>0:
			ac='child'
		sev=row['row['Casualty Severity']]
		res[cls,sev]+=1
		res[cls,sev,ac]+=1

	print res
	'''with open('srtstest.csv','w') as f:
		f.write(n.content)
		'''
	return 0
	
	
import canvas

r=schools()['Primary']
for n in r:
	ep=circle(30,1000,r[n][1])
	a=n
	break

print getaccs(ep)

w = h = 512
canvas.set_size(w, h)
z=circle(15,128,(256,256))
for n in range(len(z)-1):
	canvas.draw_line(z[n][0],z[n][1],z[n+1][0],z[n+1][1])
	
