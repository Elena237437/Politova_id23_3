import tkinter as tk  # Импортируем нужные нам библиотеки
import math
import json

#Константы и начальные значения в файле json
PLANETS_DATA_FILE = 'planets.json'

# Начальные данные планет и их спутников (назание, цвет,размер итд)
default_data = {
    "planets": [
        {
            "name": "Mercury", "radius": 8, "distance": 50, "density": 5.4,
            "color": "#a9a9a9", "speed": 0.04, "satellites": []
        },
        {
            "name": "Venus", "radius": 14, "distance": 100, "density": 5.2,
            "color": "#f5deb3", "speed": 0.03, "satellites": []
        },
        {
            "name": "Earth", "radius": 16, "distance": 150, "density": 5.5,
            "color": "#1e90ff", "speed": 0.02, "satellites": [
                {"radius": 4, "distance": 25, "speed": 0.1}
            ]
        },
        {
            "name": "Mars", "radius": 12, "distance": 200, "density": 3.9,
            "color": "#b22222", "speed": 0.015, "satellites": [
                {"radius": 3, "distance": 15, "speed": 0.12}
            ]
        },
        {
            "name": "Jupiter", "radius": 30, "distance": 300, "density": 1.3,
            "color": "#d2691e", "speed": 0.01, "satellites": [
                {"radius": 5, "distance": 40, "speed": 0.08}
            ]
        }
    ]
}

#Загрузка данных планет
def load_planets_data():
    try:
        with open(PLANETS_DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Если файла нет, создаём его с начальными данными
        with open(PLANETS_DATA_FILE, 'w') as f:
            json.dump(default_data, f)
        return default_data

planets_data = load_planets_data()  # Загружаем данные

#Функция настройки цвета по размеру(чем больше радиус, тем светлее цвет)
def color_by_size(radius):
    blue_intensity = int(min(radius * 10, 255))
    return f'#0000{blue_intensity:02x}'

#Инициализация окна
root = tk.Tk()
root.title("Solar System Simulation")
root.geometry("900x900")

# Добавляем Canvas для рисования(заполняем фон окна цветом)
canvas = tk.Canvas(root, bg='black')
canvas.pack(fill=tk.BOTH, expand=True)

#Логика движения
center_x, center_y = 450, 450
planet_objects = []  # Хранение объектов планет и их спутников

# Создаём Солнце в центре
sun = canvas.create_oval(
    center_x - 30, center_y - 30, center_x + 30, center_y + 30,
    fill='yellow'
)

# Создаём орбиты для каждой планеты
for planet in planets_data["planets"]:
    canvas.create_oval(
        center_x - planet["distance"], center_y - planet["distance"],
        center_x + planet["distance"], center_y + planet["distance"],
        outline="white", dash=(3, 2)
    )

# Создаём планеты и их спутники
for planet in planets_data["planets"]:
    # Получаем цвет на основе размера (радиуса)
    planet_color = color_by_size(planet["radius"])

    # Создаём планету
    planet_obj = canvas.create_oval(
        center_x + planet["distance"] - planet["radius"],
        center_y - planet["radius"],
        center_x + planet["distance"] + planet["radius"],
        center_y + planet["radius"],
        fill=planet_color
    )

    # Создаём спутники для планеты (если есть)
    satellites = []
    for satellite in planet["satellites"]:
        sat_obj = canvas.create_oval(
            0, 0, satellite["radius"] * 2, satellite["radius"] * 2,
            fill='white'
        )
        satellites.append({
            "object": sat_obj,
            "angle": 0,  # Начальный угол спутника
            "speed": satellite["speed"],
            "distance": satellite["distance"],
            "radius": satellite["radius"]
        })

    # Сохраняем объект планеты и её спутники
    planet_objects.append({
        "object": planet_obj,
        "angle": 0,  # Начальный угол на орбите
        "speed": planet["speed"],
        "distance": planet["distance"],
        "radius": planet["radius"],
        "satellites": satellites
    })

# Функция для обновления позиций планет и их спутников
def update_positions():
    for planet in planet_objects:
        # Вычисляем новые координаты планеты
        planet["angle"] += planet["speed"]
        x = center_x + planet["distance"] * math.cos(planet["angle"])
        y = center_y + planet["distance"] * math.sin(planet["angle"])

        # Обновляем координаты планеты
        canvas.coords(
            planet["object"],
            x - planet["radius"], y - planet["radius"],
            x + planet["radius"], y + planet["radius"]
        )

        # Обновляем координаты спутников
        for satellite in planet["satellites"]:
            satellite["angle"] += satellite["speed"]
            sat_x = x + satellite["distance"] * math.cos(satellite["angle"])
            sat_y = y + satellite["distance"] * math.sin(satellite["angle"])

            # Обновляем координаты спутника
            canvas.coords(
                satellite["object"],
                sat_x - satellite["radius"], sat_y - satellite["radius"],
                sat_x + satellite["radius"], sat_y + satellite["radius"]
            )


    root.after(50, update_positions)


update_positions()
root.mainloop()
