import requests
import psycopg2
from datetime import datetime
apiKey = "e23914d0c5248567cf3d0d5303df36c3"
class Weather:
    def __init__(self, city):
        self.city = city
        print(f"Погода {city}")
    #Валидация значений
    def validate(self, value, min_value, max_value, default = None):
        if value is None:
            return default
        try:
            value = float(value)
            if value < min_value or value > max_value:
                print(f"Значение {value} вне диапозона [{min_value}, {max_value}]")
                return default
            return value
        except (ValueError, TypeError):
            print("Некорректное значение {value}")
            return default
    #Заносим в словарь значения погоды
    def get_weather(self):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={apiKey}&units=metric"
        response = requests.get(url)
        try:
            data = response.json()
        except:
            print("Ошибка подключения к API: {response.status_code}, {response.text}")
        weatherData = {
            'city': self.city,
            'temp': self.validate(data['main']['temp'], -57, 57),
            'feels_like':self.validate(data['main']['feels_like'], -57,57),
            'humidity': self.validate(data['main']['humidity'], 0, 100),
            'pressure': self.validate(data['main']['pressure'], 800, 1100),
            'wind_speed':self.validate(data['wind']['speed'], 0, 150),
            'description':data['weather'][0]['description'],
            'timestamp': datetime.fromtimestamp(data['dt'])
        }
        return weatherData
    def save_to_db(self):
        weather_data = self.get_weather()
        if weather_data is None:
            print("❌ Нет данных для сохранения")
            return False

        try:
            conn = psycopg2.connect(
                dbname="weather_db",
                user="postgres",
                password="123",
                host="postgres",
                port=5432
            )
            cur = conn.cursor()

            # === ДОБАВЛЯЕМ СОЗДАНИЕ ТАБЛИЦЫ ===
            cur.execute("""
                CREATE TABLE IF NOT EXISTS raw_weather (
                    id SERIAL PRIMARY KEY,
                    city VARCHAR(100) NOT NULL,
                    temp FLOAT,
                    feels_like FLOAT,
                    humidity INTEGER,
                    pressure INTEGER,
                    wind_speed FLOAT,
                    description VARCHAR(255),
                    timestamp TIMESTAMP,
                    load_dt TIMESTAMP DEFAULT NOW()
                )
            """)
            # ===================================

            # Вставляем данные
            cur.execute("""
                INSERT INTO raw_weather
                (city, temp, feels_like, humidity, pressure, wind_speed, description, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, [
                weather_data['city'],
                weather_data['temp'],
                weather_data['feels_like'],
                weather_data['humidity'],
                weather_data['pressure'],
                weather_data['wind_speed'],
                weather_data['description'],
                weather_data['timestamp']
            ])

            conn.commit()
            cur.close()
            conn.close()
            print(f"✅ Данные для {self.city} сохранены в БД")
            return True

        except Exception as e:
            print(f"❌ Ошибка БД: {e}")
            return False
        
    def run(self):
        data = self.get_weather()
        if data:
            success = self.save_to_db()
            if success:
                print("ETL выполнен успешно!")
            else:
                print("Ошибка при сохранении в БД")
        else:
            print("Данные не получены")
        return data

#-Подключаемся к базе

    
#     if weatherData['temp'] < 56.7 or weatherData['temp'] > 56.7:
#         weatherData['temp'] = None
#         print("Температура вне разумных пределаов")

# print(get_weather())