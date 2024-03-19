from data.subloader import get_json
from googletrans import Translator
import datetime


async def get_weather_text(data):
    icons = await get_json("icons.json")

    city = data["name"]
    temp = data["main"]["temp"]
    description = data["weather"][0]["main"]
    wind = data["wind"]["speed"]
    humidity = data["main"]["humidity"]
            
    if description in icons[0]:
        weather_icons = icons[0][description]
        text = f"<em>Дата: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}</em>\n"
        text += f"<b>Погода у місті: {city}</b>\n\n"
        text += f"Температура повітря: {round(temp)}C° {weather_icons}\n"
        text += f"Вологість: {humidity}%\n"
        text += f"Швидкість вітру: {round(wind)}м/c"
                    
        return text
    
    else:
        text = f"<em>Дата: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}</em>\n"
        text += f"<b>Погода у місті: {city}</b>\n\n"
        text += f"Температура повітря: {round(temp)}C°\n"
        text += f"Вологість: {humidity}%\n"
        text += f"Швидкість вітру: {round(wind)}м/c"

        return text
    

def translator(city):
    translator = Translator()
    source_lang = translator.detect(city).lang
    target_lang = "en"
    translated_city = translator.translate(city, src=source_lang, dest=target_lang)
    return translated_city.text



