import datetime

while True:
	a=datetime.datetime.now().timetuple()
	f=False
	while(a[3]==20 and a[4]==57 and a[5]==0):
		if f==False:
			print("ciao")
			f=True
		else:
			pass
	f=False
