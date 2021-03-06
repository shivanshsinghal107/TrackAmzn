import os
import random
import requests
import bs4
import telegram
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Set up database
engine = create_engine(os.getenv("DATABASE_URI", "sqlite:///database.db"))
db = scoped_session(sessionmaker(bind=engine))

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


def tracker(url, TrackingPrice, productID, user):
	res = requests.get(url, headers = ({"User-Agent":''+ua()+''}))
	soup = bs4.BeautifulSoup(res.content, 'html.parser')
	print(({"User-Agent":''+ua()+''}))

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
			db.execute("UPDATE products SET availability = NOT availability WHERE user_id = :user_id AND product_id = :product_id", {"user_id": user, "product_id": productID})
			db.commit()
			db.close()
			print(f"alerts turned off for {title}")
			return f"*{title}*\n\n????  *{currency}{amount}*\n\n????  In Stock\n\n????  [Buy now!]({url})\n\n????  _Alerts OFF_"
		else:
			return "price not down"
	else:
		return "not available"

def product_list_keyboard(user):
	products = db.execute("SELECT title, product_id FROM products WHERE user_id = :user_id", {"user_id": user}).fetchall()
	db.close()
	
	if products:
		button_list = [
			[InlineKeyboardButton(product.title[:60], callback_data=product.product_id)] for product in products
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
	products = db.execute("SELECT url, tracking_price, product_id, availability, title FROM products WHERE user_id = :user_id", {"user_id": chat_id}).fetchall()
	db.close()
	print(f"\n{chat_id}")
	for product in products:
		if product.availability == True:
			msg = tracker(product.url, product.tracking_price, product.product_id, chat_id)
			print(msg)
			if (msg != "price not down") and (msg != "not available"):
				context.bot.send_message(chat_id=chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
		else:
			print(f"alerts off for {product.title}")

def track(update: Update, context: CallbackContext):
	exists = db.execute("SELECT * FROM products WHERE user_id = :user_id", {"user_id": update.message.chat_id}).fetchall()
	db.close()
	print(update.message.chat_id)
	if len(exists) > 0:
		context.bot.send_message(chat_id=update.message.chat_id, text="Just a minute, checking the prices of the products", parse_mode=telegram.ParseMode.MARKDOWN)
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
		lastName = str(update.message.from_user.last_name)
		userName = str(update.message.from_user.username)

		res = requests.get(link, headers = ({"User-Agent":''+ua()+''}))
		soup = bs4.BeautifulSoup(res.text, "html.parser")
		title = soup.find(id = "productTitle").get_text().strip()
		code = res.status_code
		print(code)
		if(code == 200 or code == 503):
			print("Awesome")
			exists = db.execute("SELECT * FROM products WHERE user_id = :user_id AND product_id = :product_id", {"user_id": user, "product_id": product_id}).fetchall()
			if len(exists) > 0:
				db.close()
				update.message.reply_text("You are trying to add the same product which you have previously added. To change the tracking price please remove it and add the product with new price")
			else:
				db.execute("INSERT INTO products (user_id, url, product_id, title, tracking_price, availability, username, first_name, last_name) VALUES (:user_id, :url, :product_id, :title, :tracking_price, :availability, :username, :first_name, :last_name)", {"user_id": user, "url": url, "product_id": product_id, "title": title, "tracking_price": price, "availability": False, "username": userName, "first_name": firstName, "last_name": lastName})
				db.commit()
				db.close()
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
	user = int(update.effective_chat.id)
	data = db.execute("SELECT title, availability FROM products WHERE user_id = :user_id AND product_id = :product_id", {"user_id": user, "product_id": query.data}).fetchall()[0]
	db.close()

	if data.availability:
		alert = "ON"
	else:
		alert = "OFF"
	print(data.title, alert)
	buttons = [
		[InlineKeyboardButton("????  Current price", callback_data=f"price{query.data}")],
		[InlineKeyboardButton(f"????  Availability alerts: {alert}", callback_data=f"available{query.data}")],
		[InlineKeyboardButton("????  Remove", callback_data=f"remove{query.data}")],
		[InlineKeyboardButton("      <<  Back to product list      ", callback_data="products")]
	]
	reply_markup = InlineKeyboardMarkup(buttons)

	query.answer()
	query.edit_message_text(text=data.title, reply_markup=reply_markup)

def check_price(update: Update, _: CallbackContext) -> None:
	query = update.callback_query
	user = int(update.effective_chat.id)

	product = db.execute("SELECT url, title FROM products WHERE user_id = :user_id AND product_id = :product_id", {"user_id": user, "product_id": query.data.split("price")[1]}).fetchall()[0]
	db.close()
	
	res = requests.get(product.url, headers = ({"User-Agent":''+ua()+''}))
	soup = bs4.BeautifulSoup(res.content, 'html.parser')
	print(({"User-Agent":''+ua()+''}))

	try:
		amount = soup.find(id="priceblock_ourprice").get_text()
		msg = f"*{product.title}*\n\n????  *{amount}*\n\n???  [Check here!]({product.url})"
	except:
		try:
			amount = soup.find(id="priceblock_dealprice").get_text()
			msg = f"*{product.title}*\n\n????  *{amount}*\n\n???  [Check here!]({product.url})"
		except:
			msg = f"*{product.title}*\n\n????  Out of Stock"

	query.answer()
	print(msg)
	query.edit_message_text(msg, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)

def change_availability(update: Update, _: CallbackContext) -> None:
	query = update.callback_query
	user = int(update.effective_chat.id)
    
	db.execute("UPDATE products SET availability = NOT availability WHERE user_id = :user_id AND product_id = :product_id", {"user_id": user, "product_id": query.data.split("available")[1]})
	product = db.execute("SELECT title, availability FROM products WHERE user_id = :user_id AND product_id = :product_id", {"user_id": user, "product_id": query.data.split("available")[1]}).fetchall()[0]
	db.commit()
	db.close()

	if product.availability:
		alert_message = f"????????     *ALERTS ON*    ????????\n{product[0]}"
	else:
		alert_message = f"????????     *ALERTS OFF*    ????????\n{product[0]}"

	query.answer()
	query.edit_message_text(alert_message, parse_mode=telegram.ParseMode.MARKDOWN)

def remove_product(update: Update, _: CallbackContext) -> None:
	query = update.callback_query
	user = int(update.effective_chat.id)

	product = db.execute("SELECT title FROM products WHERE user_id = :user_id AND product_id = :product_id", {"user_id": user, "product_id": query.data.split("remove")[1]}).fetchall()[0]
	db.execute("DELETE FROM products WHERE user_id = :user_id AND product_id = :product_id", {"user_id": user, "product_id": query.data.split("remove")[1]})
	db.commit()
	db.close()
	
	query.answer()
	query.edit_message_text(text=f"{product.title} removed")

def remove_all(update, context):
	try:
		user = int(update.effective_chat.id)

		db.execute("DELETE FROM products WHERE user_id = :user_id", {"user_id": user})
		db.commit()
		db.close()
		
		context.job_queue.stop()
		update.message.reply_text("All the products are now removed")
	except (IndexError, ValueError):
		update.message.reply_text("Usage: /remove")

def debug_connection(update, context):
	msg = "Bot running"
	context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

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
	u.dispatcher.add_handler(CommandHandler("start", start))
	u.dispatcher.add_handler(CommandHandler("stop", stop, pass_job_queue=True))
	u.dispatcher.add_handler(CommandHandler("help", help))
	u.dispatcher.add_handler(CommandHandler("debug", debug_connection))
	u.dispatcher.add_handler(CommandHandler("add", add_item))
	u.dispatcher.add_handler(CallbackQueryHandler(product_options, pattern=r"^[a-zA-z0-9]{10}$"))
	u.dispatcher.add_handler(CallbackQueryHandler(check_price, pattern=r"^price[a-zA-z0-9]{10}$"))
	u.dispatcher.add_handler(CallbackQueryHandler(change_availability, pattern=r"^available[a-zA-z0-9]{10}$"))
	u.dispatcher.add_handler(CallbackQueryHandler(remove_product, pattern=r"^remove[a-zA-z0-9]{10}$"))
	u.dispatcher.add_handler(CallbackQueryHandler(products_list, pattern="products"))
	u.dispatcher.add_handler(CommandHandler("list", view_items))
	u.dispatcher.add_handler(CommandHandler("remove", remove_all))
	u.dispatcher.add_handler(CommandHandler("track", track))
	PORT = int(os.environ.get('PORT', '8443'))
	u.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=f"https://trackamzn.herokuapp.com/{TOKEN}")
	# u.bot.set_webhook("https://trackamzn.herokuapp.com/" + TOKEN)
	u.idle()
    
if __name__ == "__main__":
	main()
