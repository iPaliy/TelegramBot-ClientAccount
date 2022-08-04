# Telegram Bot: ClientAccount

A Telegram Python bot running on Python3. Its purpose is to help with customer accounting.


## Starting The Bot

To setup database, you should run file: `db_maker.py` with command ` python db_maker.py`.

Then you should run main file with bot: `MainFile.py` with command ` python MainFile.py`.


## Setting Up The Bot (Read Before Trying To Use!):
Please make sure to use the latest Python version. (*Recommended*)


### Configuration

First, you should make new bot in @BotFather and get TOKEN.
Then, to configuring bot open file named `config.py` and write your `TOKEN`.
An example `config.py` file could be:
```
TOKEN = 'TOKEN from @BotFather'
```


### Python dependencies

Install the necessary python dependencies by moving to the project directory and running:

`pip3 install -r requirements.txt`.

This will install all necessary python packages.

### Use

This bot has two sides: for client and for admins.
If you want to open admin's console, write command `/admin`. This console can:
- Show full time sheet for admin
- Show busy hours for admin
- Select service to show time sheet for admin
- Show time sheet with some service for admin
- Show free time for admin
- Add next day into db


For clients, there is the following functionality:

- Choosing a day to make an appointment
- Check an appointment
- Check and select time for appointment
- Make an appointment in db
- Show your appointment to cancel
- Delete an appointment from db
- Add phone number into your appointment
- Add service in your appointment

Too, this bot has reminder and you can choose time in file `FuncFile.py` and func: `remind()` to remind your clients about appointment.



### Credits

* [iPaliy](https://github.com/iPaliy) - Telegram Bot: ClientAccount