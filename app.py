import telebot
from config import keys, TOKEN
from extensions import ConvertionException, ValuesConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате: \n<название валюты цену которой он хочет узнать> \
<название валюты в которой надо узнать цену первой валюты> \
<количество переводимой валюты>\nУвидеть свисок всех доступных валют: /velues'
    bot.reply_to(message, text)


@bot.message_handler(commands=['velues'])
def velues(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
       text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        velues = message.text.split(' ')

        if len(velues) != 3:
            raise ConvertionException('Cлишком много параметров.')

        quote, base, amount = velues
        total_base = ValuesConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Неудалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)


