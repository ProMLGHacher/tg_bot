# Обратите внимание, что из обработчика в функцию
# передаются экземпляры `update` и `context`
def start(update, context):
    # `bot.send_message` это метод Telegram API
    # `update.effective_chat.id` - определяем `id` чата,
    # откуда прилетело сообщение

    buttons = [
        [telegram.KeyboardButton("1"), telegram.KeyboardButton("2")],
        [telegram.KeyboardButton("3")],
    ]

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="text", reply_markup=telegram.ReplyKeyboardMarkup(buttons))
