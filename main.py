from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging

from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler

from consts import TOKEN
from commands import start_command
from text_messages import echo_text_message

# получаем экземпляр `Updater`
updater = Updater(token=TOKEN, use_context=True)
# получаем экземпляр `Dispatcher`
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# говорим обработчику, если увидишь команду `/start`,
# то вызови функцию `start()`
start_handler = CommandHandler('start', start_command.start)
# добавляем этот обработчик в `dispatcher`
dispatcher.add_handler(start_handler)


# говорим обработчику `MessageHandler`, если увидишь текстовое
# сообщение (фильтр `Filters.text`)  и это будет не команда
# (фильтр ~Filters.command), то вызови функцию `echo()`
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo_text_message.echo)
# регистрируем обработчик `echo_handler` в экземпляре `dispatcher`
dispatcher.add_handler(echo_handler)


def caps(update, context):
    # если аргументы присутствуют
    if context.args:
        # объединяем список в строку и
        # переводим ее в верхний регистр
        text_caps = ' '.join(context.args).upper()
        # `update.effective_chat.id` - определяем `id` чата,
        # откуда прилетело сообщение
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=text_caps)
    else:
        # если в команде не указан аргумент
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='No command argument')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='send: /caps argument')


# обработчик команды '/caps'
caps_handler = CommandHandler('caps', caps)
# регистрируем обработчик в диспетчере
dispatcher.add_handler(caps_handler)


def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Перевести в верхний регситр',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    results.append(
        InlineQueryResultArticle(
            id=query.lower(),
            title='Перевести в нижний регситр',
            input_message_content=InputTextMessageContent(query.lower())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)


# функция обратного вызова
def all(update, context):
    # добавим в начало полученного сообщения строку 'ECHO: '
    text = 'ECHO: ' + update.message.text
    # `update.effective_chat.id` - определяем `id` чата,
    # откуда прилетело сообщение
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


# импортируем обработчик `MessageHandler` и класс с фильтрами

# говорим обработчику `MessageHandler`, если увидишь текстовое
# сообщение (фильтр `Filters.text`)  и это будет не команда
# (фильтр ~Filters.command), то вызови функцию `echo()`
echo_handler = MessageHandler(Filters.all, all)
# регистрируем обработчик `echo_handler` в экземпляре `dispatcher`
dispatcher.add_handler(echo_handler)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Я тебя не понимаю, пошёл нхуй")


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

if __name__ == "__main__":
    updater.start_polling()
