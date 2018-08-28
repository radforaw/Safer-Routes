from SRTS import *

z=schools()['Primary']
r=schools()['Secondary'].copy()
z.update(r)

for n in z:
	print n,z[n]
	break
