import asyncio  
import telebot
import requests
from telebot.async_telebot import AsyncTeleBot  
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from bs4 import BeautifulSoup
import DATA

bot = AsyncTeleBot(DATA.TOKEN)

def keyboard()->ReplyKeyboardMarkup:
    """Создание клавиатуры"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    # Добавляем кнопки
    btn1 = KeyboardButton('Расписание')
    btn2 = KeyboardButton('Информация')
    markup.add(btn1, btn2)
    return markup

def parsing(soup)->str:
    """Парсит и создает ссылку для фото"""
    img = soup.find('img', alt="Ъ")

    return DATA.URL2+img.get('src')

async def restart_task():
    """Асинхронная задача перезагрузки"""
    asyncio.run(main())
    
async def periodic_restart():
    """Периодическая перезагрузка"""
    while True:
        await asyncio.sleep(3600)
        await restart_task()

async def main():
    """Основная асинхронная функция"""
    # Запускаем задачу перезагрузки  
    asyncio.create_task(periodic_restart())
    
    # Запускаем бота  
    bot=telebot.TeleBot(DATA.TOKEN)

    headers = {
        'Authorization': 'Bearer YOUR_TOKEN',
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json',
        'Custom-Header': 'CustomValue'
    }

    response = requests.get(DATA.URL, headers=headers)
    if response.status_code == 200:
        print("Бот запущен")
    soup = BeautifulSoup(response.text, 'html.parser')

    #обработчики комад
    @bot.message_handler(commands=['start'])
    def start_message(message):
        markup=keyboard()
        bot.send_message(message.chat.id,"Привет {0.first_name}! Хочешь узнать расписание нажми кнопку 'Расписание'".format(message.from_user), reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def schedule(message):
        markup=keyboard()
        if message.text == "Расписание":
            bot.send_photo(message.chat.id, parsing(soup), caption="Расписание")   
        elif message.text == "Информация":
             bot.send_message(message.chat.id, "Вся информация берется с сайта " + 
                              f"https://gimn3-53.gosuslugi.ru. Телеграмм  bot с открытым исходным кодом. Ссылка на GitHub " + 
                              f"https://github.com/Mike-Belov/schedule. По всем вопросам @MikeBelovv", reply_markup=markup)  
        else:
            bot.send_message(message.chat.id, "Бот не понял вас попробуйте еще раз")

    while True:
        try:
            await bot.polling(non_stop=True, timeout=123)
        except Exception as e:
            print(e)  

if __name__ == "__main__":

    asyncio.run(main())
