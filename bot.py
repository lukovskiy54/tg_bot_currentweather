import telebot
import requests
bot = telebot.TeleBot("BOT_TOKEN", parse_mode=None)
API = 'API_TOKEN'
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hi! Enter your city")


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    data = data.json()
    print(data)
    print(city)
    sample = ''
    try:
        icon = data['weather'][0]['icon']
        response = requests.get(f'https://openweathermap.org/img/wn/{icon}@2x.png')
        if response.status_code == 200:
            with open('icon.jpg', 'wb') as file:
                file.write(response.content)
            print(f"Image downloaded")
        else:
            print("Failed to download image")
    
        bot.send_message(message.chat.id,f"Temperature in this city: {data['main']['temp']} °C {sample}\n{data['weather'][0]['main']}")
        photo = open('icon.png', 'rb')
        bot.send_photo(message.chat.id, photo)
        
    except KeyError:
        bot.send_message(message.chat.id, f"City is incorrect. Try again")

@bot.message_handler(content_types=["sticker", "pinned_message", "photo", "audio", "voice"])
def handling_other(message):
    bot.send_message(message.chat.id, "Wrong input, try again")


bot.infinity_polling()
