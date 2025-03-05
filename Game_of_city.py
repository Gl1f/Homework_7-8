import json

class JsonFile:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def read_data(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return data
    
    def write_data(self, data):
        with open(self.file_path, 'a') as file:
            json.dump(data, file)

