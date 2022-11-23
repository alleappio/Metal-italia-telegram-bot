from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Updater
import DataGetter
import logging
import datetime
logging.basicConfig(level=logging.INFO)

class TeleBot:
	def __init__(self):
		logging.info("avvio")
		self.lastUp=datetime.datetime.now()
		self.d=DataGetter.DataGetter(1)
		self.d=self.d.getData()
		token="Token"
		self.app = ApplicationBuilder().token(token).build()
		self.app.add_handler(CommandHandler("start", self.start))
		self.app.add_handler(CommandHandler("provincia", self.searchProv))
		self.app.add_handler(CommandHandler("band", self.searchBand))
		self.app.add_handler(CommandHandler("mese", self.searchMonth))
		self.app.add_handler(CommandHandler("lastUpdate", self.lastUpdate))
		self.app.add_handler(CommandHandler("update",self.updateCommand))

	async def deb(self,update,context):
		chat_id=update.effective_message.chat_id
		user_id=update.message.from_user.username
		s=f"\n\tchat_id:{chat_id}\n\tuser_id:{user_id}"
		logging.info(s)

	async def start(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
		s=f'''
		BENVENUTO!
		Questo è il primo bot (non ufficiale) per la ricerca di concerti, tutti censiti su
		metalitalia.com

		Puoi cercare gli eventi in 3 modi:
		- per provincia, tramite il comando:
		    /provincia [provincia]
		- per nome della band, tramite il comando:
		    /band [nome band]
		- per mese, tramite il comando:
		    /mese [mese]

		per cominciare prova con il comando:
		    /provincia milano
		'''
		await update.message.reply_photo("https://www.metalitalia-festival.com/wp-content/uploads/2019/02/Metal_cube2.jpg",caption=s)

	async def searchProv(self,update:Update,context:ContextTypes.DEFAULT_TYPE) -> None:
		await self.deb(update,context)
		rec=[]
		place=' '.join(context.args)
		if place != "" and place != " ":
			for i in self.d:
				if place.lower() in i["place"].lower():
					rec.append(i)
			if rec!=[]:
				for i in rec:
					s=f"Concerto trovato:\nBand:\n {i['band']}\n\nData:\n {i['date'][0]} {i['date'][1]}\n\nPosto:\n {i['place']}\n\nLink:\n {i['link']}"
					await update.message.reply_photo(i["img"],caption=s)
			else:
				await update.message.reply_text(f"Nessun risultato trovato per:\n \"{place}\"")
		else:
			await update.message.reply_text("Non hai inserito il nessuna provincia, usa la sintassi: \n\t/provincia [provincia]")

	async def searchBand(self,update:Update,context:ContextTypes.DEFAULT_TYPE) -> None:
		await self.deb(update,context)
		rec=[]
		band=' '.join(context.args)
		if band != "" and band !=" ":
			for i in self.d:
				if band.lower() in i["band"].lower():
					rec.append(i)
			if rec!=[]:
				for i in rec:
					s=f"Concerto trovato:\nBand:\n {i['band']}\n\nData:\n {i['date'][0]} {i['date'][1]}\n\nPosto:\n {i['place']}\n\nLink:\n {i['link']}"
					await update.message.reply_photo(i["img"],caption=s)
			else:
				await update.message.reply_text(f"Nessun risultato trovato per:\n \"{band}\"")
		else:
			await update.message.reply_text("Non hai inserito il nome di una band, usa la sintassi: \n\t/band [Nome Band]")

	async def searchMonth(self,update:Update,context:ContextTypes.DEFAULT_TYPE) -> None:
		await self.deb(update,context)
		rec=[]
		month=' '.join(context.args)
		if month != "" and month != " ":
			for i in self.d:
				if i["date"][1].lower() in month.lower():
					rec.append(i)
			if rec!=[]:
				for i in rec:
					s=f"Concerto trovato:\nBand:\n {i['band']}\n\nData:\n {i['date'][0]} {i['date'][1]}\n\nPosto:\n {i['place']}\n\nLink:\n {i['link']}"
					await update.message.reply_photo(i["img"],caption=s)
			else:
				await update.message.reply_text(f"Nessun risultato trovato per:\n \"{month}\"")
		else:
			await update.message.reply_text("Non hai inserito un mese, usa la sintassi: \n\t/mese [mese]")

	async def lastUpdate(self,update:Update,context:ContextTypes.DEFAULT_TYPE) -> None:
		await update.message.reply_text(f"last update:{self.lastUp}")

	async def updateCommand(self,update:Update,context:ContextTypes.DEFAULT_TYPE) -> None:
		self.updateData(datetime.datetime.now())
		await update.message.reply_text(f"update done, {datetime.datetime.now()}")

	def updateData(self,t):
		self.d=DataGetter.DataGetter(0)
		self.d=self.d.getData()
		self.lastUp=t

	def run(self):
		self.app.run_polling()


def main():
	a=TeleBot()


if __name__=='__main__':
    main()
