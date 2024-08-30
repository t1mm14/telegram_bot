import telebot
from config import keys, TOKEN
from extensions import ConvertionException, ValueConverter

TOKEN = "7145239780:AAFhlOL4v3Jp9S-W13XAKCJlxR3Ryz8S0qo"

bot = telebot.TeleBot(TOKEN)


keys = {
    'доллар' : 'USD',
    'юань' : 'CNY',
    'евро' : 'EUR',
    'рубль' : 'RUB',
}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id , f"Здравствуй {message.chat.username}! \n"
                                       f"\n"
                                       f"Я бот для конвертации валют!\n"
                                       f"\n"
                                       f"Для конвертации введите значения в формате: \n"
                                       f"<имя валюты><в какую валюту перевести><количество переводимой валюты>\n"
                                       f"\n"
                                       f"Пример запроса <доллар рубль 20>"
                                       f"\n"
                                       f"Для вывода списка валют напишите /values")


@bot.message_handler(commands=["values"])
def values(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types= ['text',])
def convert(message):
    try:

        values = message.text.split(' ')

        if len(values) !=3:
            raise ConvertionException('Слишком много или мало параметров.')

        quote, base, amount = values
        total_base = ValueConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Огибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)