import telebot
from telebot import types
import COVID19Py
import configs
import re

covid19 = COVID19Py.COVID19()
bot = telebot.TeleBot(configs.token)

# Функция, что сработает при отправке команды Старт
# Здесь мы создаем быстрые кнопки, а также сообщение с привествием
@bot.message_handler(commands=['start'])
def start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	btn1 = types.KeyboardButton('Во всём мире')
	btn2 = types.KeyboardButton('Украина')
	btn3 = types.KeyboardButton('Россия')
	markup.add(btn1, btn2)

	send_message = f"*Привет {message.from_user.first_name}!* Чтобы узнать данные про коронавируса напишите " \
		f"название страны, например: Америка, Украина, Россия и так далее."
	bot.send_message(message.chat.id, send_message, parse_mode='markdown', reply_markup=markup)

# Функция, что сработает при отправке какого-либо текста боту
# Здесь мы создаем отслеживания данных и вывод статистики по определенной стране
@bot.message_handler(commands=['start'])
def start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	btn1 = types.KeyboardButton('Во всём мире')
	btn2 = types.KeyboardButton('Украина')
	markup.add(btn1, btn2)

	send_message = f"*Привет {message.from_user.first_name}!* Чтобы узнать данные про коронавируса напишите " \
		f"название страны, например: США, Украина, Россия и так далее "
	bot.send_message(message.chat.id, send_message, parse_mode='markdown', reply_markup=markup)

# Функция, что сработает при отправке какого-либо текста боту
# Здесь мы создаем отслеживания данных и вывод статистики по определенной стране
@bot.message_handler(content_types=['text'])
def mess(message):
	final_message = ""
	country = ""
	for key, value in configs.countries.items():
		if re.search(message.text, key):
			country = value
			country1 = key
	if country == "":
		location = covid19.getLatest()
		final_message = f"_Данные по всему миру:_ \n" \
						f"*Заболевших:* {location['confirmed']:,} \n" \
						f"*Сметрей:* {location['deaths']:,}"
	else:
		location = covid19.getLocationByCountryCode(country)
		date = location[0]['last_updated'].split("T")
		time = date[1].split(".")
		final_message = f"_Данные по стране:_ *{country1}* \n" \
						f"Население: {location[0]['country_population']:,} \n" \
						f"Последнее обновление: {date[0]} {time[0]} \n" \
						f"Последние данные: \n" \
						f"*Заболевших:* {location[0]['latest']['confirmed']:,} \n" \
						f"*Сметрей:* {location[0]['latest']['deaths']:,}"
	bot.send_message(message.chat.id, final_message, parse_mode='markdown')


# Это нужно чтобы бот работал всё время
bot.polling(none_stop=True)