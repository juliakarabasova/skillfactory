import telebot

from extensions import APIException, CryptoConverter
from config import TOKEN, VALS


bot = telebot.TeleBot(TOKEN)

'''
Content types:
text, audio, document, photo, sticker, video, video_note, voice, location, contact, new_chat_members, left_chat_member, 
new_chat_title, new_chat_photo, delete_chat_photo, group_chat_created, supergroup_chat_created,
channel_chat_created, migrate_to_chat_id, migrate_from_chat_id, pinned_message.
'''


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    text = ('Добро пожаловать в конвертер валют! Чтобы получить желаемый результат напишите через пробел название одной валюты, '
            'затем валюту, в которую хотите осуществить конвертацию, и количество переводимой валюты.\n\n'
            'Посмотреть список доступных валют: /values')
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in VALS.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


# param: content_types (['text', 'voice', 'sticker', 'document'...]) or commands (personalised commands names)
@bot.message_handler(content_types=['text'])
def convert(message):
    from_val, to_val, amount = message.text.split()
    # TODO: too much values exception
    # TODO: too little values
    try:
        total = CryptoConverter.convert(from_val, to_val, amount)
    except APIException as e:
        bot.reply_to(message.chat.id, f'(422) Пользовательская ошибка.\n{e}')
    except Exception as ex:
        bot.reply_to(message.chat.id, f'(500) Серверная ошибка! Пожалуйста, повторите позднее.\n{ex}')
    else:
        bot.reply_to(message.chat.id, f'Стоимость {amount} {from_val} в {to_val}: {total}')


bot.polling(none_stop=True)
