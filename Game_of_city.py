import json
from dataclasses import dataclass
import random


@dataclass
class City:
    name: str
    population: int
    subject: str
    district: str
    latitude: float
    longitude: float
    is_used: bool = False


class JsonFile:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def read_data(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return data
    
    def write_data(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file)

class CitiesSerializer:
    def __init__(self, city_data):
        self.cities = [City(
            name=city['name'],
            population=city['population'],
            subject=city['subject'],
            district=city['district'],
            latitude=city['latitude'],
            longitude=city['longitude'],
            is_used=city['is_used']
        ) for city in city_data]
        
    def get_all_cities(self):
        return self.cities

class CityGame:
    def __init__(self, cities_serializer):
        self.cities = cities_serializer.get_all_cities()
        self.used_cities = set()
        self.last_letter = ''
    
    def start_game(self):
        city = self.random.choice(self.cities)
        self.used_cities.add(city.name)
        self.last_letter = city.name[-1]
        print('Привет! Мы начинаем игру в города. Нужно писать города, которые оканчиваются на букву предыдущего города.')
        print(f"Начало игры. Город: {city.name}")
        
    def human_turn(self):
        while True:
            city_name = input("Введите название города: ")
            if city_name in self.used_cities:
                print("Этот город уже использован. Попробуйте другой город.")
                continue
            if city_name[0] != self.last_letter:
                print("Название города должно начинаться с буквы, на которую заканчивается предыдущий город.")
                continue
            self.used_cities.add(city_name)
            self.last_letter = city_name[-1]
            print(f"Вы ввели город: {city_name}")
            break