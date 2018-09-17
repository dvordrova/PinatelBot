0# -*- coding: utf-8 -*-
import telebot
import cherrypy
import config
import webhook
from automata.state_abstract import State
from user import User


if __name__ == '__main__':
    users = {}
    bot = telebot.TeleBot(config.TOKEN)
    State.bot = bot

    @bot.message_handler(commands=['start', 'help'])
    def start(message):
        bot.send_message(message.chat.id, 'Я бот. Чтобы начать со мной сессию пожелай мне доброго утра.'
                                          ' Чтобы закончить сессию пожелай мне спокойной ночи. '
                                          'Я буду пинать тебя каждые {} секунд, а в конце тяжелого дня напомню, '
                                          'что ты сделал так, а где только потерял время'.format(User.delay))


    @bot.message_handler(commands=['add'])
    def start(message):
        job_pre = '/add job'
        lazy_pre = '/add lazy'
        if message.text.startswith(job_pre) and message.text[len(job_pre):].strip():
            job = message.text[len(job_pre):].lower().strip()
            users[message.chat.id].today['Дела'].append((job, State._get_struct(job)))
            bot.send_message(message.chat.id, 'Добавил новое дело')
        elif message.text.startswith(lazy_pre) and message.text[len(lazy_pre):].lower().strip():
            lazy = message.text[len(lazy_pre):].strip()
            users[message.chat.id].today['Отдых'].append((lazy, State._get_struct(lazy)))
            bot.send_message(message.chat.id, 'Добавил новый релакс')
        else:
            bot.send_message(message.chat.id, 'Добавить новое дело:\n'
                                              '\t/add job <description>\n'
                                              'Добавиь новый отдых:\n'
                                              '\t/add lazy <description>\n')

    # Хэндлер на все текстовые сообщения
    @bot.message_handler(func=lambda m: True)
    def echo_message(message):
        print(message)
        u = users.get(message.chat.id, None)
        if not u:
            u = User(bot, message.chat.id)
            users[message.chat.id] = u
        u.update(message.text)

    if config.LOCAL:
        bot.polling()
    else:
        bot.remove_webhook() # Снимаем вебхук перед повторной установкой (избавляет от некоторых проблем)
        bot.set_webhook(url=config.WEBHOOK_URL_BASE + config.WEBHOOK_URL_PATH,
                        certificate=open(config.WEBHOOK_SSL_CERT, 'r'))
        # Указываем настройки сервера CherryPy
        cherrypy.config.update({
            'server.socket_host': config.WEBHOOK_LISTEN,
            'server.socket_port': config.WEBHOOK_PORT,
            'server.ssl_module': 'builtin',
            'server.ssl_certificate': config.WEBHOOK_SSL_CERT,
            'server.ssl_private_key': config.WEBHOOK_SSL_PRIV
        })


        # Собственно, запуск!
        cherrypy.quickstart(webhook.WebhookServer(), config.WEBHOOK_URL_PATH, {'/': {}})