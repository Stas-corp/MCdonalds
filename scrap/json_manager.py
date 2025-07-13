import json
import os
import re

class Manager:
    '''### Manager class handles reading/writing product data to a local JSON file.
    
    It ensures file existence, formats keys (optional), and manages storage logic.
    
    '''
    exect = ['\"', '®', ',']
    
    def __init__(self):
        self.dir = 'data'
        self.file_name = 'items.json'
        self.path = os.path.join(self.dir, self.file_name)


    @property
    def isFile(self) -> bool:
        return os.path.exists(self.path)


    def __key_replace(self, key:str) -> str:
        '''### Returns a cleaned version of the key suitable for use as a dictionary key.
        
        Replaces spaces with underscores and removes unwanted characters 
        defined in the 'exect' list if the key contains non-alphabetic symbols.
        
        '''
        key = key.replace(' ', '_')
        if not bool(re.fullmatch(r"[A-Za-zА-Яа-яІіЇїЄєҐґ_]+", key)):
            for e in Manager.exect:
                if e in key:
                    key = key.replace(e, '')
        return key


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
            key = item['name']
            # key = self.__key_replace(key)
            data_to_write[key] = item
        
        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump(data_to_write, file, ensure_ascii=False, indent=4)


    def read_data(self) -> dict:
        if not self.isFile:
            raise FileNotFoundError(f"File {self.path} does not exist.")
        
        with open(self.path, 'r', encoding='utf-8') as file:
            return json.load(file)


    def manage_file(
        self, 
        data_list: list[dict]=None
    ) -> dict:
        '''### Reads data from the JSON file if it exists.
        
        If the file doesn't exist, writes the provided data_list to the file and then reads it.
        Raises an error if the file is missing and no data is provided.
        
        '''
        if not self.isFile:
            if data_list is None:
                raise ValueError("Data list must be provided to create the file.")
            self.write_data(data_list)
            return self.read_data()
        else:
            return self.read_data()