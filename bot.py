import random
import csv
import requests
import bs4
import telegram
import numpy as np
import pandas as pd
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

def ua():
    uaString= ["Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/2.0.172.0 Safari/530.5",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.81 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux x86_64; 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/17.0.1410.63 Safari/537.31",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.12 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3057.0 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.45 Safari/537.36",\
        "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.21 (KHTML, like Gecko) Chrome/11.0.678.0 Safari/534.21",\
        "Mozilla/5.0 (X11; Ubuntu; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1864.6 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2599.0 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2036.0 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2705.45 Safari/537.36",\
        "Mozilla/5.0 (X11; CentOS; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/602.5.2 (KHTML, like Gecko) Chrome/58.0.2939.53 Safari/602.5.2",
        "Mozilla/5.0 (Linux; IM-A860S Build/JZO54K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.99 Apple Safari/537.36",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/Chrome/63.0.3239.84 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2527.0 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.68 Safari/537.36",\
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.222.5 Safari/532.2",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2163.0 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 (KHTML, like Gecko) Chrome/55.0.2883",\
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2409.0 Safari/537.36",\
        "Linux / Chrome 55: Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/599.0+ (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2946.0 Safari/537.36",\
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/530.0 (KHTML, like Gecko) Chrome/2.0.162.0 Safari/530.0",\
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2442.0 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux i686 (x86_64)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.50 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.6.1 Chrome/45.0.2454.101 Safari/537.36",\
        "Mozilla/5.0 (Linux; diordnA 7.0; BAH-L09 Build/HUAWEIBAH-L09; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux x86_64) Build/NPJS25.93-14.7-8; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/70.0.3538.57 Safari/537.36 Hawk/TurboBrowser/v3.0.0.4.9.09"]
    return random.choice(uaString)

spreadsheet_url = "db.csv"

def tracker(url, TrackingPrice, productID, user):
	df = pd.read_csv(spreadsheet_url)
	idx = df[(df['userID'] == user) & (df['productID'] == productID)].index
	res = requests.get(url, headers = ({"User-Agent":''+ua()+''}))
	soup = bs4.BeautifulSoup(res.content, 'html.parser')
	print(({"User-Agent":''+ua()+''}))
	# time.sleep(20)

	title = soup.find(id="productTitle").get_text().strip()
	try:
		amount = soup.find(id="priceblock_ourprice").get_text()
	except:
		try:
			amount = soup.find(id="priceblock_dealprice").get_text()
		except:
			amount = ""
	if amount:
		currency = amount[:2]
		amount = amount[2:]
		print(title, amount)
		real_price = ""
		for i in range(len(amount)):
			if amount[i] != ',':
				real_price += amount[i]
		real_price = int(float(real_price))
		
		print(real_price)
		print(TrackingPrice)
		
		if real_price <= TrackingPrice:
			avail = df.loc[idx, 'Availability']
			df.loc[idx, 'Availability'] = ~(avail)
			df.to_csv(spreadsheet_url, index=False)
			print(f"alerts turned off for {title}")
			return f"*{title}*\n\n💰  *{currency}{amount}*\n\n🧭  In Stock\n\n🛒  [Buy now!]({url})\n\n🔕  _Alerts OFF_"
		else:
			return "price not down"
	else:
		return "not available"

def product_list_keyboard(user):
	df = pd.read_csv(spreadsheet_url)
	products = [p for p in df[df['userID'] == user]['Title']]
	ids = [i for i in df[df['userID'] == user]['productID']]
	print(ids)
	if len(ids) != 0:
		button_list = [
			[InlineKeyboardButton(product[:60], callback_data=ids[i])] for i, product in enumerate(products)
		]
		reply_markup = InlineKeyboardMarkup(button_list)
	else:
		reply_markup = ""
	return reply_markup


def start(update, context):
	start_message = "*Welcome to TrackAmzn*\n\nStart saving money by tracking Amazon products and receive price and availability alerts according to your preferences.\n\n_Commands_\n\n/add - add a new product\n/track - track a new product\n/list - manage your products"
	context.bot.send_message(chat_id=update.effective_chat.id, text=start_message, parse_mode=telegram.ParseMode.MARKDOWN)

def stop(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="BOT Stopped. Good bye!!")
	context.job_queue.stop()

def track_alert(context: CallbackContext):
	chat_id = context.job.context
	df = pd.read_csv(spreadsheet_url)
	print(f"\n{chat_id}")
	for i in range(0, len(df["userID"])):
		if(df["userID"][i]==chat_id and df['Availability'][i]==True):
			msg = tracker(df["URL"][i], df["TrackingPrice"][i], df["productID"][i], chat_id)
			print(msg)
			if (msg != "price not down") and (msg != "not available"):
				context.bot.send_message(chat_id=chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
		else:
			print(f"alerts off for {df['Title'][i]}")

def track(update: Update, context: CallbackContext):
	df = pd.read_csv(spreadsheet_url)
	print(update.message.chat_id)
	exists = int(update.message.chat_id) in df.values
	if exists:
		context.bot.send_message(chat_id=update.message.chat_id, text="Just a sec, checking the prices of the products", parse_mode=telegram.ParseMode.MARKDOWN)
		context.job_queue.run_repeating(track_alert, 900, context=update.message.chat_id)
	else:
		context.bot.send_message(chat_id=update.message.chat_id, text="No products are been tracked. Start adding products", parse_mode=telegram.ParseMode.MARKDOWN)

def add_item(update, context):
	try:
		url = str(context.args[0])
		price = int(context.args[1])
		link = url.split("/dp/")[0] + "/dp/" + url.split("/dp/")[1].split("/")[0]
		product_id = url.split("/dp/")[1].split("/")[0]
		user = int(update.effective_chat.id)
		firstName = str(update.message.from_user.first_name)

		res = requests.get(link, headers = ({"User-Agent":''+ua()+''}))
		soup = bs4.BeautifulSoup(res.text, "html.parser")
		title = soup.find(id = "productTitle").get_text().strip()
		code = res.status_code
		print(code)
		if(code == 200 or code == 503):
			print("Awesome")
			df = pd.read_csv(spreadsheet_url)
			df1 = pd.DataFrame(df, columns=['URL', 'TrackingPrice', 'userID', 'firstName', 'Title', 'productID', 'Availability'])
			df1['bol'] = np.where((df['URL'] == str(link)) & (df['userID'] == int(update.effective_chat.id)), "true", np.nan)
			print(df1)
			if("true" in df1.values):
				update.message.reply_text("You are trying to add the same product which you have previously added. To change the tracking price please remove it and add the product with new price")
			else:
				l = len(df["URL"])
				df.loc[l, ["URL"]] = link
				df.loc[l, ["TrackingPrice"]] = price
				df.loc[l,["userID"]] = user
				df.loc[l,["firstName"]] = firstName
				df.loc[l,["Title"]] = title
				df.loc[l, ["productID"]] = product_id
				df.loc[l, ["Availability"]] = False
				df.to_csv(spreadsheet_url, index=False)
				update.message.reply_text("Product successfully added for tracking")
		elif(code == 404):
			update.message.reply_text("Product is currently not listed on amazon")
	except (IndexError, ValueError):
		update.message.reply_text("Usage: /add <url> <target_price>")

def products_list(update: Update, _: CallbackContext) -> None:
	user = int(update.effective_chat.id)
	query = update.callback_query
	query.edit_message_text('Choose a product from the list below:', reply_markup=product_list_keyboard(user))

def view_items(update, context):
	user = int(update.effective_chat.id)
	reply_markup = product_list_keyboard(user)
	if reply_markup != "":
		update.message.reply_text('Choose a product from the list below:', reply_markup=product_list_keyboard(user))
	else:
		update.message.reply_text("Your product list is empty")

def product_options(update: Update, _: CallbackContext) -> None:
	query = update.callback_query
	df = pd.read_csv(spreadsheet_url)
	user = int(update.effective_chat.id)
	data = df[(df['userID'] == user) & (df['productID'] == query.data)]
	name = [n for n in data['Title']]
	available = [a for a in data['Availability']]
	if available[0]:
		alert = "ON"
	else:
		alert = "OFF"
	print(name[0], alert)
	buttons = [
		[InlineKeyboardButton("💰  Current price", callback_data=f"price{query.data}")],
		[InlineKeyboardButton(f"🧭  Availability alerts: {alert}", callback_data=f"available{query.data}")],
		[InlineKeyboardButton("🗑  Remove", callback_data=f"remove{query.data}")],
		[InlineKeyboardButton("      <<  Back to product list      ", callback_data="products")]
	]
	reply_markup = InlineKeyboardMarkup(buttons)

	query.answer()
	query.edit_message_text(text=name[0], reply_markup=reply_markup)

def check_price(update: Update, _: CallbackContext) -> None:
	query = update.callback_query

	df = pd.read_csv(spreadsheet_url)
	user = int(update.effective_chat.id)
	idx = df[(df['userID'] == user) & (df['productID'] == query.data.split("price")[1])].index
	product = [p for p in df.loc[idx, 'Title']]
	url = [u for u in df.loc[idx, 'URL']]
	res = requests.get(url[0], headers = ({"User-Agent":''+ua()+''}))
	soup = bs4.BeautifulSoup(res.content, 'html.parser')
	print(({"User-Agent":''+ua()+''}))

	try:
		amount = soup.find(id="priceblock_ourprice").get_text()
		msg = f"*{product[0]}*\n\n💵  *{amount}*\n\n✅  [Check here!]({url[0]})"
	except:
		try:
			amount = soup.find(id="priceblock_dealprice").get_text()
			msg = f"*{product[0]}*\n\n💵  *{amount}*\n\n✅  [Check here!]({url[0]})"
		except:
			msg = f"*{product[0]}*\n\n🛒  Out of Stock"

	query.answer()
	print(msg)
	query.edit_message_text(msg, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)

def change_availability(update: Update, _: CallbackContext) -> None:
	query = update.callback_query
	
	df = pd.read_csv(spreadsheet_url)
	user = int(update.effective_chat.id)
	idx = df[(df['userID'] == user) & (df['productID'] == query.data.split("available")[1])].index
	avail = df.iloc[idx]['Availability']
	print(avail)
	print(~(avail))
	df.loc[idx, 'Availability'] = ~(avail)
	alert = [a for a in df.loc[idx, 'Availability']]
	product = [p for p in df.loc[idx, 'Title']]
	if alert[0]:
		alert_message = f"🚨🚨     ALERTS ON    🚨🚨\n{product[0]}"
	else:
		alert_message = f"🔕🔕     ALERTS OFF    🔕🔕\n{product[0]}"
	print(df)
	df.to_csv(spreadsheet_url, index=False)

	query.answer()
	query.edit_message_text(alert_message, parse_mode=telegram.ParseMode.MARKDOWN)

def remove_product(update: Update, _: CallbackContext) -> None:
	query = update.callback_query
	df = pd.read_csv(spreadsheet_url)
	user = int(update.effective_chat.id)
	idx = df[(df['userID'] == user) & (df['productID'] == query.data.split("remove")[1])].index
	product = [p for p in df.loc[idx, 'Title']]
	df.drop(idx, axis = 0, inplace = True)
	df.to_csv(spreadsheet_url, index=False)

	query.answer()
	query.edit_message_text(text=f"{product[0]} removed")

def remove_all(update, context):
	try:
		user = int(update.effective_chat.id)
		df = pd.read_csv(spreadsheet_url)
		df = df[~(df['userID'] == user)]
		df.to_csv(spreadsheet_url, index=False)
		context.job_queue.stop()
		update.message.reply_text("All the products are now removed")
	except (IndexError, ValueError):
		update.message.reply_text("Usage: /remove")

def debug_connection(update, context):
	msg = "Bot running"
	context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def debug_tracking(update, context):
	df = pd.read_csv(spreadsheet_url)
	try:
		msg = tracker(df["URL"][0], df["TrackingPrice"][0])
		context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
	except:
		context.bot.send_message(chat_id=update.effective_chat.id, text="Nothing to track for now")

def help(update, context):
	msg = """
/add <url> <price> - add a new product
/list - manage your products
/track - track your products
/remove - remove all products
/stop - stop the bot
	"""

	context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def main():
	TOKEN = os.getenv("TOKEN")
	u = Updater(token=TOKEN, use_context=True)
	u.dispatcher.add_handler(CommandHandler("start", start, pass_job_queue=True))
	u.dispatcher.add_handler(CommandHandler("stop", stop, pass_job_queue=True))
	u.dispatcher.add_handler(CommandHandler("help", help))
	u.dispatcher.add_handler(CommandHandler("debugconnection", debug_connection))
	u.dispatcher.add_handler(CommandHandler("debugtracking", debug_tracking))
	u.dispatcher.add_handler(CommandHandler("add", add_item))
	u.dispatcher.add_handler(CallbackQueryHandler(product_options, pattern=r"^[a-zA-z0-9]{10}$"))
	u.dispatcher.add_handler(CallbackQueryHandler(check_price, pattern=r"^price[a-zA-z0-9]{10}$"))
	u.dispatcher.add_handler(CallbackQueryHandler(change_availability, pattern=r"^available[a-zA-z0-9]{10}$"))
	u.dispatcher.add_handler(CallbackQueryHandler(remove_product, pattern=r"^remove[a-zA-z0-9]{10}$"))
	u.dispatcher.add_handler(CallbackQueryHandler(products_list, pattern="products"))
	u.dispatcher.add_handler(CommandHandler("list", view_items))
	u.dispatcher.add_handler(CommandHandler("remove", remove_all))
	u.dispatcher.add_handler(CommandHandler("track", track))
	updater.start_webhook(listen="0.0.0.0", port=5000, url_path=TOKEN)
    	updater.bot.set_webhook("https://name.herokuapp.com/" + TOKEN)
	u.idle()

if __name__ == "__main__":
	main()
