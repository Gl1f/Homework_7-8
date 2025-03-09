import json
import random
from typing import List, Dict, Any
from dataclasses import dataclass


# класс для хранения информации о городе
@dataclass
class City:
    name: str
    population: int
    subject: str
    district: str
    latitude: float
    longitude: float
    is_used: bool = False

# класс для работы с файлами
class JsonFile:
    """Класс для работы с JSON-файлами
    """
    def __init__(self, filename: str):
        self.filename = filename
    
    def read_data(self) -> Any:
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def write_data(self, data: Any) -> None:
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

# класс для сериализации городов
class CitiesSerializer:
    """Класс для сериализации городов
    """
    def __init__(self, city_data: List[Dict[str, Any]]):
        self.cities = [City(
            name=city['name'],
            population=int(city['population']),
            subject=city['subject'],
            district=city['district'],
            latitude=float(city['coords']['lat']),
            longitude=float(city['coords']['lon']),
            is_used=False
        ) for city in city_data]
        
    def get_all_cities(self) -> List[City]:
        return self.cities

# класс для игры в города
class CityGame:
    """Класс для игры в города
    """
    def __init__(self, cities: CitiesSerializer, game_state_file: JsonFile = None): 
        self.cities = cities.get_all_cities()
        self.used_cities = set()
        self.last_letter = ''
        self.save_game_state_file = game_state_file
        self.city_last_name = ''
    
    def start_game(self):
        city = random.choice(self.cities)
        self.used_cities.add(city.name)
        self.city_last_name = city.name
        self.last_letter = city.name[-1].lower()
        print('Привет! Мы начинаем игру в города. Нужно писать города, которые оканчиваются на букву предыдущего города.')
        print(f"Начало игры. Город: {city.name}")
        
    def human_turn(self, city_input: str) -> bool:
        self.city_input = city_input.capitalize()
        
        if self.city_input in self.used_cities:
            print("Этот город уже был. Вы проиграли :(")
            return False
        
        city = next((city for city in self.cities if city.name == self.city_input), None)
        if not city:
            print("Такого города нет в списке. Вы проиграли :(")
            return False
        
        if city.name[0].lower() != self.last_letter:
            print("Этот город не начинается с нужной буквы. Вы проиграли :(")
            return False
        
        self.used_cities.add(city.name)
        self.last_letter = city.name[-1].lower()
        self.city_last_name = city.name
        print(f"Вы назвали город: {city.name}")
        return True
    
    def computer_turn(self) -> bool:
        possible_cities = [city for city in self.cities if city.name[0].lower() == self.last_letter and city.name not in self.used_cities]
        
        
        if not possible_cities:
            print("Компьютер не может сделать ход. Вы выиграли!")
            return False
        
        
        city = random.choice(possible_cities)
        self.used_cities.add(city.name)
        self.last_letter = city.name[-1].lower()
        self.city_last_name = city.name
        print(f"Компьютер назвал город: {city.name}")
        return True
    
    def check_game_over(self) -> bool:
        return not any(c for c in self.cities if c.name[0].lower() == self.last_letter and c.name not in self.used_cities)
    
    def save_game_state(self) -> None:
        state = {
            "used_cities": list(self.used_cities),
            "last_letter": self.last_letter,
            "last_city_name": self.city_last_name
        }
        if self.save_game_state_file:
            self.save_game_state_file.write_data(state)
        else:
            with open("game_state.json", "w", encoding="utf-8") as file:
                json.dump(state, file, ensure_ascii=False, indent=4)
        print("Состояние игры сохранено.")
    

# Фасад, управляющий игрой
class GameManager:
    """Класс для управления игрой
    """
    def __init__(self, state_file: JsonFile, cities_serializer: CitiesSerializer, city_game: CityGame):
        self.state_file = state_file
        self.cities_serializer = cities_serializer
        self.city_game = city_game

    def load_game_state(self):
        state = self.state_file.read_data()
        if state:
            # Восстанавливаем состояние игры
            self.city_game.used_cities = set(state.get("used_cities", []))
            self.city_game.last_letter = state.get("last_letter", "")
            self.city_game.city_last_name = state.get("last_city_name", "")
            print("Сохраненная игра успешно загружена.")
            print('Последний названный город:', self.city_game.city_last_name)
        else:
            print("Сохраненная игра не найдена, начинаем новую игру.")
            self.city_game.start_game()

    def run_game(self):
        # Загружаем состояние сохранённой игры или начинаем новую игру
        self.load_game_state()

        # Игровой цикл
        while True:
            user_input = input("Введите город: ")
            if not self.city_game.human_turn(user_input):
                print("Вы проиграли!")
                break

            # Сохраняем состояние после хода игрока
            self.city_game.save_game_state()

            if not self.city_game.computer_turn():
                print("Вы победили! Компьютер проиграл.")
                break

            # Сохраняем состояние после хода компьютера
            self.city_game.save_game_state()

            if self.city_game.check_game_over():
                print("Игра завершена! Нет доступных ходов.")
                break

    def display_game_result(self):
        # Вывод итоговой информации по игре
        print("\n===== Результаты игры =====")
        print("Использованные города:")
        print(", ".join(self.city_game.used_cities))
        if self.city_game.check_game_over():
            print("Игра завершена – ходов больше нет.")
        else:
            print("Игра прервана досрочно.")
        print("===========================")

# Скрипт запуска игры
if __name__ == "__main__":
    # Файл с городами (обязательно должен существовать и быть корректным)
    cities_file = JsonFile("cities.json")
    cities_data = cities_file.read_data()
    if cities_data is None:
        print("Ошибка: не удалось загрузить данные городов из файла 'cities.json'.")
        exit(1)
    
    # Создаём сериализатор городов на основе данных из файла
    cities_serializer = CitiesSerializer(cities_data)
    
    # Файл для сохранения состояния игры (если его нет, он будет создан)
    game_state_file = JsonFile("game_state.json")
    
    # Создаём объект игры, передавая сериализатор и объект для работы с сохранением
    city_game = CityGame(cities_serializer, game_state_file)
    
    # Создаём управляющий класс (фасад)
    game_manager = GameManager(game_state_file, cities_serializer, city_game)
    
    # Запускаем игру
    game_manager.run_game()
    
    # Выводим итоговый результат игры
    game_manager.display_game_result()