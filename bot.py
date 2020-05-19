import telebot
import dbworker
import bot_conf
import sqlite3



bot = telebot.TeleBot(bot_conf.token)

country = ""
travel = []
#ачало работы
@bot.message_handler(commands = ["start"])
def cmd_start(message):
    bot.send_message(message.chat.id, "Здравствуйте! Как вас зовут?")
    dbworker.set_state(message.chat.id, bot_conf.States.S_ENTER_NAME.value)

@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Начнем сначала. Как вас зовут?")
    dbworker.set_state(message.chat.id, bot_conf.States.S_ENTER_NAME.value)


        
#Список поездок
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == bot_conf.States.S_ENTER_NAME.value)
def user_entering_name(message):
    
    name = message.text
    bot.send_message(message.chat.id, "Хорошо " + name + ". Можем начинать.")
    bot.send_message(message.chat.id, name + ", вот список доступных путешествий:")
    conn = sqlite3.connect(bot_conf.travel_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM travelling")
    conn.commit()
        
    travels = cursor.fetchall()
        
    for each in travels:
        bot.send_message(message.chat.id, each[0])
    
    bot.send_message(message.chat.id, "Выберите место поездки")
    dbworker.set_state(message.chat.id, bot_conf.States.S_CHOOSE.value)
    
    

        
#Выбор конкретной поездки              
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == bot_conf.States.S_CHOOSE.value)
def choose_travel(message):
    global travel
    global country
    if message.text is None:
        return
    else:
        conn = sqlite3.connect(bot_conf.travel_file)
        cursor = conn.cursor()
        cursor.execute("SELECT travelling.travel_company, travelling.cost, travelling.departure_date, travelling.return_date, travelling.description, travelling.counter FROM travelling WHERE travelling.country=?",(message.text,))
        country = message.text
        t = cursor.fetchall()
        travel = list(t)
        
        bot.send_message(message.chat.id, "Вы выбрали следующую поездку")
        bot.send_message(message.chat.id, message.text)

        bot.send_message(message.chat.id, "Туристический оператор: " + str(travel[0][0]))
        bot.send_message(message.chat.id, "Стоимость поездки: " + str(travel[0][1]))
        bot.send_message(message.chat.id, "Дата отправления: " + str(travel[0][2]))
        bot.send_message(message.chat.id, "Дата возвращения: " + str(travel[0][3]))
        bot.send_message(message.chat.id, "Описание тура: " + str(travel[0][4]))
        bot.send_message(message.chat.id, "Количество путевок: " + str(travel[0][5]))
        
        bot.send_message(message.chat.id, "Хотите её приобрести?")
        dbworker.set_state(message.chat.id, bot_conf.States.S_BUY_TRAVEL.value)

#Покупать поездку или нет
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == bot_conf.States.S_BUY_TRAVEL.value)
def to_buy_or_not_to_buy(message):
    if message.text != "Да" and message.text != "Нет":
        bot.send_message(message.chat.id, "Пожалуйста, ответьте Да или Нет.")
        return
    if message.text == "Да":
        bot.send_message(message.chat.id, "Сколько путевок вам нужно?")
        dbworker.set_state(message.chat.id, bot_conf.States.S_FINISH.value)
        
        
    if message.text == "Нет":
        bot.send_message(message.chat.id, "Зайдите позже, может мы найдем другую поездку для вас.")
        bot.send_message(message.chat.id, "Бот закончил свою работу. Для начала новой сессии используйте команды /start или /reset.")

#Сколько путевок нужно
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == bot_conf.States.S_FINISH.value)
def to_buying(message):
    if int(message.text) == 0:
        bot.send_message(message.chat.id, "Вы ошиблись, попробуйте снова.")
        return
    if int(message.text) > travel[0][5]:
        bot.send_message(message.chat.id, "Столько путевок у нас нет, попробуйте взять меньше.")
        return
    else:
        bot.send_message(message.chat.id, "Поздравляем с успешной покупкой " + message.text + " путевок! Обращайтесь еще.")
        
        conn = sqlite3.connect(bot_conf.travel_file)
        cursor = conn.cursor()

        result = travel[0][5] - int(message.text)

        cursor.execute("UPDATE travelling SET counter=? WHERE country=?", (result, country))
        conn.commit()
        bot.send_message(message.chat.id, "Бот закончил свою работу. Для начала новой сессии используйте команды /start или /reset.")

if __name__ == '__main__':
    bot.polling(none_stop = True)
