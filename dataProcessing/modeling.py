import os
from abc import ABC, abstractmethod
from dataProcessing import fileLoader
from tqdm import tqdm

class Modeling(ABC):

    def __init__(self, folder_path=None, file_path=None, apply=False):
        self.folder_path = folder_path
        self.file_path = file_path
        self.apply = apply
        self.next_list = [] 

    @abstractmethod
    def process(self, init_data=None):
        pass
    
    def export_type(self, path):
        return os.path.splitext(path)[-1]

    def get_first_file_path(self, folder_path):
        first_file = os.listdir(folder_path)[0]
        return folder_path.joinpath(first_file)
    
    def get_init_data(self, init_data):
        if self.folder_path:
            path = self.get_first_file_path(self.folder_path)
            type = self.export_type(path)
            print(f'path : {path}')
            print(f'type : {type}')
            return fileLoader.Factory_fileLoader().get_file_loader(type)().load(self.folder_path, path_type='folder')
        if self.file_path:
            type = self.export_type(self.file_path)
            return fileLoader.Factory_fileLoader().get_file_loader(type)().load(self.file_path, path_type='file')
        return init_data 

    def process_all(self, init_data=None):
        init_data = self.get_init_data(init_data)
        if self.apply:
            processed_data = [self.process(data) for data in tqdm(init_data, desc='now applying modeling for each data:')]
        else:
            processed_data = self.process(init_data)
        if self.next_list:
            for next_modeling in self.next_list:
                processed_data = next_modeling.process_all(processed_data)
        return processed_data

    def add_next(self, modeling):
        self.next_list.append(modeling)
