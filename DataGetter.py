import requests
from bs4 import BeautifulSoup as bs
import json
class DataGetter:
	def __init__(self,mode=0):
		self.soupin=[]
		self.conc=[]
		if mode==0:
			self.debug()
		elif mode==1:
			self.req()
	
	def req(self):
		header={
			"Connection":"keep-alive",
			"User-agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0"
		}
		s=requests.get("https://metalitalia.com/category/agenda/",headers=header)
		self.soup=bs(s.text,features="html.parser")
		with open("out.html","w",encoding="utf-8") as f:
			f.write(self.soup.prettify())
		
	def debug(self):
		with open("out.html","r",encoding="utf-8") as f:
			self.soup=bs(f.read(),features="html.parser")

	def saveF(self,name,mode=0,payload=""):
		if mode==0:
			with open(name,"w",encoding="utf-8") as f:
				f.write(payload)
		elif mode==1:
			with open(name,"a",encoding="utf-8") as f:
				f.write(payload)
				
	def getData(self):
		a=self.soup.findAll("figure")
		for i in a:
			self.soupin.append(bs(i.prettify(),features="html.parser"))
		for i in self.soupin:
			try:
				link=i.find("a")["href"]
				image=i.find("img")['data-lazy-srcset'].split(',')
				image=[j for j in image if "500w" in j][0].replace(" 500w","").strip()				
				date=i.find("div",{"class":"date"})
				date=date.text.replace("\n","").split(" ")
				date=[j for j in date if j!='']
				band=i.find("h1")
				band=band.text.split("\n")
				band=[j.strip() for j in band if j!='']
				place=i.find("p")
				place=place.text.replace("@","").replace(" ","").replace("\n","")
				self.conc.append({
					"link":link,
					"img":image,
					"date":date,
					"band":f"{band[0]}",
					"place":place 
				})
			except Exception as e:
				pass
		self.saveF("conc.json",0,json.dumps(self.conc))
		return self.conc
		
if __name__=='__main__':
	d=DataGetter(0)
	d.getData()
