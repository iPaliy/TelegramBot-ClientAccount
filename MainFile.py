from FuncFile import *
from threading import Thread

bot = telebot.TeleBot(token=TOKEN) # use token from config.py


@bot.message_handler(commands=['start'])
def start(message):
    Remote.start(message)


@bot.message_handler(commands=['admin'])
def admin(message):
    if message.chat.id in Remote.admin:
        Remote.admin(message)
    else:
        bot.send_message(message.chat.id, 'Ця функція доступна лише для адмінів')


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Записатися на прийом":
        Remote.day_choice(message)

    elif message.text == "Подивитися свої записи":
        Remote.check_appointment(message)

    elif message.text == "Скасувати запис":
        Remote.select_time_to_cancel(message)

    elif message.text in Remote.av_date:
        Remote.action_day[message.chat.id] = f'{message.text}'
        Remote.day_time_phone[message.chat.id] = [message.text]
        Remote.select_time(message)

    elif message.text[:4] == 'Дата':
        Remote.del_appointment(message)

    elif message.text in Remote.time_sheet:
        Remote.booking(message, Remote.action_day[message.chat.id])
        Remote.day_time_phone[message.chat.id].append(message.text)
        del Remote.action_day[message.chat.id]

    elif message.text == 'Назад':
        Remote.start_sec(message)

    elif message.text == 'Назад >':
        bot.send_message(message.chat.id,
                         'Ваш запис не був збережений. Спробуйте знову. Необхідно ввести усі дані (дата, час, номер телефону, вид послуги')
        Remote.del_unfinished_appointment(Remote.day_time_phone[message.chat.id][0],
                                          Remote.day_time_phone[message.chat.id][1])
        Remote.start_sec(message)

    elif message.text == 'Розклад повністю':
        if message.chat.id in Remote.admin:
            Remote.adm_full_timesheet(message)
        else:
            bot.send_message(message.chat.id, 'Ця функція доступна лише для адмінів')

    elif message.text == 'Розклад записів':
        if message.chat.id in Remote.admin:
            Remote.adm_busy_timesheet(message)
        else:
            bot.send_message(message.chat.id, 'Ця функція доступна лише для адмінів')

    elif message.text in Remote.adm_list_service:
        if message.chat.id in Remote.admin:
            Remote.show_service_timesh_adm(message)
        else:
            bot.send_message(message.chat.id, 'Ця функція доступна лише для адмінів')

    elif message.text == 'Розклад по послугам':
        if message.chat.id in Remote.admin:
            Remote.select_service_adm(message)
        else:
            bot.send_message(message.chat.id, 'Ця функція доступна лише для адмінів')

    elif message.text == 'Вільний час':
        if message.chat.id in Remote.admin:
            Remote.adm_free_time(message)
        else:
            bot.send_message(message.chat.id, 'Ця функція доступна лише для адмінів')

    elif message.text == f"Добавити {Remote.fifth_day}":
        info = Remote.cur.execute(f"SELECT * FROM user WHERE date = '{Remote.fifth_day}'")
        if len(info.fetchall()) == 0:
            Remote.add_date()
            bot.send_message(message.chat.id, 'Успішно додано')
        else:
            bot.send_message(message.chat.id, 'Можливість запису на цей день уже є')


    elif message.text == '< Назад':
        Remote.admin(message)

    elif message.text in Remote.list_of_service:
        Remote.add_service(message, Remote.day_time_phone[message.chat.id][0],
                           Remote.day_time_phone[message.chat.id][1])
        del Remote.day_time_phone[message.chat.id]
        Remote.start_sec(message)


@bot.message_handler(content_types=['contact'])
def phone(message):
    Remote.add_phone(message, Remote.day_time_phone[message.chat.id][0], Remote.day_time_phone[message.chat.id][1])


if __name__ == '__main__':
    ReminderThread = Thread(target=Remote.remind)
    ReminderThread.start()
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except:
            sleep(2)
