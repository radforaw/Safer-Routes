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
			lookup=set()
			for i in reader:
				if i['DfE'] in z:
					lookup.add(i['PCODE'])
			print len(lookup)
			data=list(lookup)
			j=[data[x:x+100] for x in range(0,len(data),100)]
			res={}
			for o in j:
				n=requests.post('https://postcodes.io/postcodes',data= {'postcodes':o})
				t=json.loads(n.content)
				if t['status']==200:
					for y in t['result']:
						try:
							res[y['query']]=(y['result']['eastings'],y['result']['northings'])
						except TypeError:
							print y
			with open('pcodes.json','w') as jfile:
				json.dump(res,jfile)
				
	
				
				
				
				
				
'''				
				
					
					
					
					
					
					
					
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
'''
