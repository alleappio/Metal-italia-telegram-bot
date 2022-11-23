#!/bin/python3
import TeleBot
import time
import threading
import datetime
import logging
logging.basicConfig(level=logging.INFO)
def updater(bot):
	logging.info("Updater started")
	while True:
		time.sleep(60)
		d=datetime.datetime.now()
		a=d.timetuple()
		f=False
		while(a[3]==8 and a[4]<=2 and a[4]>=0):
			if f==False:
				try:
					bot.updateData(d)
					f=True
				except:
					f=False
			else:
				pass
		f=False

def main():
	try:
		a=TeleBot.TeleBot()
		up=threading.Thread(target=updater,args=(a,))
		up.start()
		a.run()
	except KeyboardInterrupt:
		up.stop()
		exit()
if __name__=='__main__':
    main()
