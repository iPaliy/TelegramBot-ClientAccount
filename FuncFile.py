import telebot
from config import *
from telebot import types
import sqlite3
import datetime
from time import sleep


class Remote:
    time_sheet = ['10:00 - 11:00', '11:00 - 12:00', '12:00 - 13:00', '13:00 - 14:00',
                  '14:00 - 15:00', '15:00 - 16:00', '16:00 - 17:00']  # available time for appointment
    list_of_service = ['Послуга 1', 'Послуга 2', 'Послуга 3', 'Послуга 4']  # list of services
    adm_list_service = ['Розклад: Послуга 1', 'Розклад: Послуга 2', 'Розклад: Послуга 3',
                        'Розклад: Послуга 4']  # list of services for admin`s console
    db = sqlite3.connect('database.db', check_same_thread=False)  # connect to db
    cur = db.cursor()  # make cursor for db
    bot = telebot.TeleBot(token=TOKEN)
    today = f'{str((datetime.datetime.now()).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'  # look like 04.08
    first_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=1)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'  # look like 04.08
    second_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=2)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'  # look like 04.08
    third_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=3)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'  # look like 04.08
    fourth_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=4)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'  # look like 04.08
    fifth_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=5)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'  # look like 04.08
    av_date = [today, first_day, second_day, third_day, fourth_day,
               fifth_day]  # available days for choose from today to five days later
    action_day = {}  # save day as value and id as key for next func
    day_time_phone = {}  # save list of day and time as value and id as key for the next func of adding phone
    admin = []  # list with admin`s id

    @classmethod
    def start(cls, message):
        """Says hello and opens the menu"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Записатися на прийом")
        btn2 = types.KeyboardButton("Подивитися свої записи")
        btn3 = types.KeyboardButton("Скасувати запис")
        markup.add(btn1, btn2, btn3)
        send_mes = f'Привіт, {message.from_user.first_name}!'
        cls.bot.send_message(message.chat.id, send_mes)
        cls.bot.send_message(message.chat.id, 'Що будемо робити', reply_markup=markup)

    @classmethod
    def start_sec(cls, message):
        """Opens the menu, without 'hello'"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Записатися на прийом")
        btn2 = types.KeyboardButton("Подивитися свої записи")
        btn3 = types.KeyboardButton("Скасувати запис")
        markup.add(btn1, btn2, btn3)
        cls.bot.send_message(message.chat.id, 'Що будемо робити', reply_markup=markup)

    @classmethod
    def day_choice(cls, message):
        """Choosing a day to make an appointment"""
        your_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        cls.today = f'{str((datetime.datetime.now()).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.first_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=1)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.second_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=2)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.third_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=3)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.fourth_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=4)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.fifth_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=5)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.av_date = [cls.today, cls.first_day, cls.second_day, cls.third_day, cls.fourth_day, cls.fifth_day]
        btn1 = types.KeyboardButton(cls.first_day)
        btn2 = types.KeyboardButton(cls.second_day)
        btn3 = types.KeyboardButton(cls.third_day)
        btn4 = types.KeyboardButton(cls.fourth_day)
        btn5 = types.KeyboardButton(cls.fifth_day)
        btn6 = types.KeyboardButton("Назад")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        cls.bot.send_message(your_id, 'Коли Вам буде зручно?', reply_markup=markup)

    @classmethod
    def check_appointment(cls, message):
        """Check an appointment"""
        cls.today = f'{str((datetime.datetime.now()).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.first_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=1)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.second_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=2)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.third_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=3)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.fourth_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=4)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.fifth_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=5)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.av_date = [cls.today, cls.first_day, cls.second_day, cls.third_day, cls.fourth_day, cls.fifth_day]
        your_id = message.chat.id
        count = 0
        name = message.from_user.first_name
        for j in cls.av_date:
            info = cls.cur.execute(f"SELECT date ,time FROM user WHERE name = '{name}' AND date = '{j}'")
            for i in info.fetchall():
                cls.bot.send_message(your_id, f'Дата: {i[0]}, час: {i[1]}')
                count += 1
        if count == 0:
            cls.bot.send_message(your_id, 'У вас немає записів')
        sleep(1)
        cls.start_sec(message)

    @classmethod
    def select_time(cls, message):
        """Check and select time for appointment"""
        your_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        list_of_date = []
        list_of_buttom = []
        for i in cls.cur.execute(f"SELECT time FROM user WHERE date = '{message.text}' AND name = 'ПУСТО'"):
            list_of_date.append(i)
        for i in list_of_date:
            list_of_buttom.append(types.KeyboardButton(str(*i)))
        list_of_buttom.append(types.KeyboardButton('Назад'))
        markup.add(*list_of_buttom)
        if len(list_of_buttom) == 1:
            cls.bot.send_message(your_id, 'Нажаль вільного часу на цей день немає', reply_markup=markup)
        else:
            cls.bot.send_message(your_id, 'Виберіть Ваш час', reply_markup=markup)

    @classmethod
    def booking(cls, message, date):
        """Make an appointment in db"""
        info = cls.cur.execute(f"SELECT name FROM user WHERE date = '{date}' AND time = '{message.text}'")
        if info.fetchall() != [('ПУСТО',)]:
            cls.bot.send_message(message.chat.id, 'Нажаль тільки що забронювали цей час. Виберіть будь ласка інший.')
            cls.start_sec(message)
        else:
            cls.cur.execute(
                f'UPDATE user SET name = "{message.from_user.first_name}", id = {message.chat.id} WHERE date = "{date}" AND time = "{message.text}"')
            cls.db.commit()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn1 = types.KeyboardButton(text="Надіслати номер телефону", request_contact=True)
            btn2 = types.KeyboardButton('Назад >')
            markup.add(btn1, btn2)
            cls.bot.send_message(message.chat.id, 'Надішліть будь ласка Ваш номер телефону', reply_markup=markup)

    @classmethod
    def select_time_to_cancel(cls, message):  # corect
        """Show your appointment to cancel"""
        your_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        name = message.from_user.first_name
        list_buttom = []
        cls.today = f'{str((datetime.datetime.now()).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.first_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=1)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.second_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=2)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.third_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=3)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.fourth_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=4)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.fifth_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=5)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.av_date = [cls.today, cls.first_day, cls.second_day, cls.third_day, cls.fourth_day, cls.fifth_day]
        info = cls.cur.execute(f"SELECT date ,time FROM user WHERE name = '{name}'")
        for i in info.fetchall():
            if i[0] in cls.av_date:
                list_buttom.append(types.KeyboardButton(f'Дата: {i[0]}, час: {i[1]}'))
        list_buttom.append(types.KeyboardButton('Назад'))
        markup.add(*list_buttom)
        if len(list_buttom) == 1:
            cls.bot.send_message(your_id, 'У вас немає записів', reply_markup=markup)
        else:
            cls.bot.send_message(your_id, 'Виберіть Ваш час для скасування', reply_markup=markup)

    @classmethod
    def del_appointment(cls, message):
        """Delete an appointment from db"""
        date = message.text[6:11]
        time = message.text[18:]
        cls.cur.execute(
            f'UPDATE user SET name = "ПУСТО", phone = NULL, service = NULL, id = NULL WHERE date = "{date}" AND time = "{time}"')
        cls.db.commit()
        cls.bot.send_message(message.chat.id, f'Ваш запис на {date} о {time} було скасовано')
        sleep(1)
        cls.start_sec(message)

    @classmethod
    def add_date(cls):
        """Add next day into db"""
        cls.fifth_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=5)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        info = cls.cur.execute(f"SELECT * FROM user WHERE date = '{cls.fifth_day}'")
        if len(info.fetchall()) == 0:
            for i in cls.time_sheet:
                cls.cur.execute(f"INSERT INTO user(date, time, name) VALUES('{cls.fifth_day}', '{i}', 'ПУСТО')")
            cls.db.commit()

    @classmethod
    def add_phone(cls, message, day, time):
        """Add phone number into your appointment"""
        phone = message.contact.phone_number
        cls.cur.execute(
            f'UPDATE user SET phone = "{phone}" WHERE date = "{day}" AND time = "{time}"')
        cls.db.commit()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Послуга 1")
        btn2 = types.KeyboardButton("Послуга 2")
        btn3 = types.KeyboardButton("Послуга 3")
        btn4 = types.KeyboardButton("Послуга 4")
        btn5 = types.KeyboardButton("Назад >")

        markup.add(btn1, btn2, btn3, btn4, btn5)
        cls.bot.send_message(message.chat.id, 'Яка послуга Вам потрібна?', reply_markup=markup)

    @classmethod
    def add_service(cls, message, day, time):
        """Add service in your appointment"""
        cls.cur.execute(
            f'UPDATE user SET service = "{message.text}" WHERE date = "{day}" AND time = "{time}"')
        cls.db.commit()
        cls.bot.send_message(message.chat.id, 'Запис виконаний успішно')

    @classmethod
    def del_unfinished_appointment(cls, day, time):
        """Delete unfinished appointment from db"""
        cls.cur.execute(
            f'UPDATE user SET name = "ПУСТО", phone = NULL, service = NULL, id = NULL WHERE date = "{day}" AND time = "{time}"')
        cls.db.commit()

    @classmethod
    def admin(cls, message):
        """Open func for admin"""
        cls.bot.send_message(message.chat.id, "Ви увійшли в консоль адміна")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Розклад повністю")
        btn2 = types.KeyboardButton("Розклад записів")
        btn3 = types.KeyboardButton("Розклад по послугам")
        btn4 = types.KeyboardButton("Вільний час")
        btn5 = types.KeyboardButton(f"Добавити {cls.fifth_day}")
        btn6 = types.KeyboardButton("Назад")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        cls.bot.send_message(message.chat.id, 'Виберіть команду', reply_markup=markup)

    @classmethod
    def adm_full_timesheet(cls, message):
        """Show full time sheet for admin"""
        cls.today = f'{str((datetime.datetime.now()).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.first_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=1)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.second_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=2)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.third_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=3)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.fourth_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=4)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.fifth_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=5)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.av_date = [cls.today, cls.first_day, cls.second_day, cls.third_day, cls.fourth_day, cls.fifth_day]
        for i in cls.av_date:
            info = cls.cur.execute(f"SELECT * FROM user WHERE date = '{i}'")
            for i in info.fetchall():
                cls.bot.send_message(message.chat.id,
                                     f"Дата: {i[1]}, час: {i[2]}, ім'я: {i[3]},телефон: {i[4]}, послуга: {i[5]}")

    @classmethod
    def adm_busy_timesheet(cls, message):
        """Show busy hours for admin"""
        cls.today = f'{str((datetime.datetime.now()).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.first_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=1)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.second_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=2)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.third_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=3)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.fourth_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=4)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.fifth_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=5)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.av_date = [cls.today, cls.first_day, cls.second_day, cls.third_day, cls.fourth_day, cls.fifth_day]
        for i in cls.av_date:
            info = cls.cur.execute(f"SELECT * FROM user WHERE date = '{i}' AND name != 'ПУСТО'")
            for i in info.fetchall():
                cls.bot.send_message(message.chat.id,
                                     f"Дата: {i[1]}, час: {i[2]}, ім'я: {i[3]},телефон: {i[4]}, послуга: {i[5]}")

    @classmethod
    def select_service_adm(cls, message):
        """Select service to show time sheet for admin"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Розклад: Послуга 1")
        btn2 = types.KeyboardButton("Розклад: Послуга 2")
        btn3 = types.KeyboardButton("Розклад: Послуга 3")
        btn4 = types.KeyboardButton("Розклад: Послуга 4")
        btn5 = types.KeyboardButton('< Назад')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        cls.bot.send_message(message.chat.id, 'Виберіть послугу для розкладу', reply_markup=markup)

    @classmethod
    def show_service_timesh_adm(cls, message):
        """Show time sheet with some service for admin"""
        count = 0
        cls.today = f'{str((datetime.datetime.now()).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.first_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=1)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.second_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=2)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.third_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=3)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.fourth_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=4)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.fifth_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=5)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.av_date = [cls.today, cls.first_day, cls.second_day, cls.third_day, cls.fourth_day, cls.fifth_day]
        for i in cls.av_date:
            info = cls.cur.execute(f"SELECT * FROM user WHERE date = '{i}' AND service = '{message.text[9:]}'")
            for i in info.fetchall():
                count += 1
                cls.bot.send_message(message.chat.id,
                                     f"Дата: {i[1]}, час: {i[2]}, ім'я: {i[3]},телефон: {i[4]}, послуга: {i[5]}")
        if count == 0:
            cls.bot.send_message(message.chat.id, 'На цю послугу записів немає')

    @classmethod
    def adm_free_time(cls, message):
        """Show free time for admin"""
        cls.today = f'{str((datetime.datetime.now()).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.first_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=1)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.second_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=2)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.third_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=3)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.fourth_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=4)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.fifth_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=5)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.av_date = [cls.today, cls.first_day, cls.second_day, cls.third_day, cls.fourth_day, cls.fifth_day]
        for i in cls.av_date:
            info = cls.cur.execute(f"SELECT * FROM user WHERE date = '{i}' AND name = 'ПУСТО'")
            for i in info.fetchall():
                cls.bot.send_message(message.chat.id, f"Дата: {i[1]}, час: {i[2]}")

    @classmethod
    def remind(cls):
        """Remind you about appointment in 20:00 day before and in 8:00 in this day"""
        cls.today = f'{str((datetime.datetime.now()).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.first_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=1)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.second_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=2)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.third_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=3)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.fourth_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=4)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.fifth_day = f'{str((datetime.datetime.now() + datetime.timedelta(days=5)).day).rjust(2, "0")}.{str((datetime.datetime.now() + datetime.timedelta(days=1)).month).rjust(2, "0")}'
        cls.av_date = [cls.today, cls.first_day, cls.second_day, cls.third_day, cls.fourth_day, cls.fifth_day]
        while True:
            if datetime.datetime.now().hour == 8 and datetime.datetime.now().minute == 0:
                info = cls.cur.execute(
                    f"SELECT id, time, service FROM user WHERE date = '{cls.today}' AND name != 'ПУСТО'")
                for i in info.fetchall():
                    cls.bot.send_message(i[0],
                                         f'Cьогодні Ви записані на {i[1]} на {i[2]}.\nЗ нетерпінням чекаємо на Вас!')
            elif datetime.datetime.now().hour == 21 and datetime.datetime.now().minute == 15:
                info = cls.cur.execute(
                    f"SELECT id, time, service FROM user WHERE date = '{cls.first_day}' AND name != 'ПУСТО'")
                for i in info.fetchall():
                    cls.bot.send_message(i[0],
                                         f'Завтра Ви записані на {i[1]} на {i[2]}.\nЗ нетерпінням чекаємо на Вас!')
            sleep(60)
