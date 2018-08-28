from SRTS import *
import requests
import math
import json
def dist(a,b):
	x1,y1=a
	x2,y2=b
	return math.sqrt(((x1-x2)**2)+((y1-y2)**2))


z=schools()['Primary']
r=schools()['Secondary'].copy()
z.update(r)

file='May18Census_PupilPostcodes.zip'
with zipfile.ZipFile(file,'r') as n:
		with n.open('May18Census_PupilPostcodes.csv','r') as csvfile:
			reader=csv.DictReader(csvfile)
			#print reader.fieldnames
			res={}
			for i in reader:
				if i['DfE'] in z:
					#print 'scool',z[i['DfE']]
					url='https://api.postcodes.io/postcodes/'+i['PCODE']
					ret=json.loads(requests.get(url).content)
					try:
						if dist((ret['result']['eastings'],ret['result']['northings']),z[i['DfE']][1])<1000:
							try:
								z[i['DfE']][3]+=1
							except IndexError:
								z[i['DfE']].append(1)
					except:
						pass
				break
			with open('saved.json','w') as jfile:
				json.dump(z,jfile)
