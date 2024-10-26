from opencage.geocoder import OpenCageGeocode
from tkinter import *
import webbrowser

def get_coordinates(city, key):
    try:
        geocoder = OpenCageGeocode(key)
        results = geocoder.geocode(city, language='ru')
        if results:
            lat = round(results[0]['geometry']['lat'], 2)
            lon = round(results[0]['geometry']['lng'], 2)
            country = results[0]['components']['country']
            osm_url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}"

            # Получение местной валюты
            currency = results[0]['annotations']['currency']['name'] if 'currency' in results[0]['annotations'] else 'Неизвестно'

            if 'state' in results[0]['components']:
                region = results[0]['components']['state']
                return {
                    "coordinates": f"Широта: {lat}, Долгота: {lon}\nСтрана: {country}.\nВалюта: {currency}.\nРегион: {region}",
                    "map_url": osm_url
                }
            else:
                return {
                    "coordinates": f"Широта: {lat}, Долгота: {lon}\nСтрана: {country}.\nВалюта: {currency}",
                    "map_url": osm_url
                }
        else:
            return "Город не найден"
    except Exception as e:
        return f"Возникла ошибка: {e}"

def show_coordinates(event=None):
    global map_url
    city = entry.get()
    result = get_coordinates(city, key)
    label.config(text=f"Координаты города {city}:\n{result['coordinates']}")
    map_url = result['map_url']

def show_map():
    if map_url:
        webbrowser.open(map_url)

def clear_fields():
    entry.delete(0, END)  # Очистить поле ввода
    label.config(text='Введите город и нажмите на кнопку')  # Сбросить текст метки
    global map_url
    map_url = ""  # Очистить URL карты

key = 'caa0c4f70c3448c5b818f69bc75751ef'
map_url = ""

window = Tk()
window.title("Координаты городов")
window.geometry("400x200")

entry = Entry(window)
entry.pack(pady=10)
entry.bind("<Return>", show_coordinates)

button = Button(window, text="Поиск координат", command=show_coordinates)
button.pack(pady=5)

label = Label(window, text='Введите город и нажмите на кнопку')
label.pack(pady=10)

map_button = Button(window, text="Показать карту", command=show_map)
map_button.pack(pady=5)

clear_button = Button(window, text="Очистить", command=clear_fields)  # Кнопка для очистки
clear_button.pack(pady=5)

window.mainloop()
