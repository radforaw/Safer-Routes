from SRTS import *

z=schools()['Primary']
r=schools()['Secondary'].copy()
z.update(r)

file=''
with zipfile.ZipFile(file,'r') as z:
		with z.open('results.csv','r') as csvfile:
			reader=csv.DictReader(csvfile)
			#print reader.fieldnames
			res={}
			for i in reader:
