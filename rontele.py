import telebot
from config import keys, TOKEN
from until import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Привет! Я - Валютный бот,чтобы начать работу введите команду в следующем форматн:\n<имя валюты цену которой нужно узнать>\
     <имя валюты в которой надо узнать цену первой валюты>\
      <количество первой валюты>'
    bot.reply_to(message,text)



@bot.message_handler(commands=['values'])
def values(message:telebot.types.Message):
   text = 'Доступные валюты: '
   for key in keys.keys():
      text = '\n'.join((text, key, ))
   bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Количество пааметров должно быть 3')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount) * int(amount)
        quote_ticket, base_ticker = keys[quote],keys[base]
    except ConvertionException as e:
        bot.reply_to(message,f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()
