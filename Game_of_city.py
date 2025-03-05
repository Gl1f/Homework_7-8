import json
from dataclasses import dataclass


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
    