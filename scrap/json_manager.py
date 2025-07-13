import json
import os
import re

class Manager:
    exect = ['\"', '®', ',']
    
    def __init__(self):
        self.dir = 'data'
        self.file_name = 'items.json'
        self.path = os.path.join(self.dir, self.file_name)
        self.isFile = False


    def write_data(
        self, 
        data_list: list[dict[str, str]]
    ) -> None:
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)
        data_to_write = {}
        for item in data_list:
            if len(item) == 0:
                continue
            key = list(item.values())[0].replace(' ', '_')
            if not bool(re.fullmatch(r"[A-Za-zА-Яа-яІіЇїЄєҐґ_]+", key)):
                for e in Manager.exect:
                    if e in key:
                        key = key.replace(e, '')
            data_to_write[key] = item
        
        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump(data_to_write, file, ensure_ascii=False, indent=4)
        self.isFile = True


    def read_data(self) -> dict:
        if not self.isFile:
            raise FileNotFoundError(f"File {self.path} does not exist.")
        
        with open(self.path, 'r', encoding='utf-8') as file:
            return json.load(file)


    def manage_file(
        self, 
        data_list: list[dict]=None
    ) -> dict:
        if not self.isFile:
            if data_list is None:
                raise ValueError("Data list must be provided to create the file.")
            self.write_data(data_list)
            return self.read_data()
        else:
            return self.read_data()