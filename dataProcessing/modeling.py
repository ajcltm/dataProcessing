import os
from abc import ABC, abstractmethod
from dataProcessing import fileLoader
from tqdm import tqdm
import logging
import traceback
from pathlib import Path

file_name = Path.home().joinpath('Desktop', 'dataProcessing.log')
logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s', 
    datefmt='%m/%d/%Y %I:%M"%S %p',
    filename=file_name, level=logging.INFO)
logger = logging.getLogger('dataProcessing')


class Modeling(ABC):

    def __init__(self, folder_path=None, file_path=None, apply=False):
        self.folder_path = folder_path
        self.file_path = file_path
        self.apply = apply
        self.next_list = [] 

    @abstractmethod
    def process(self, init_data=None):
        pass

    def handle_process(self, init_data=None, log_point='object'):
        try:
            data = self.process(init_data=init_data)
            logger.info(f'{log_point} success!')
            return data 
        except:
            logger.error(f'{log_point} {traceback.format_exc()}')
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
    
    def get_log_point(self, idx):
        if self.folder_path:
            return os.listdir(self.folder_path)[idx]
        return f'index : {idx}'

    def process_all(self, init_data=None):
        init_data = self.get_init_data(init_data)
        if self.apply:
            processed_data = [i for i in (self.handle_process(data, self.get_log_point(idx)) for idx, data in enumerate(tqdm(init_data, desc='now applying modeling for each data:'))) if i is not None]
        else:
            processed_data = self.handle_process(init_data)
        if self.next_list:
            for next_modeling in self.next_list:
                processed_data = next_modeling.process_all(processed_data)
        return processed_data

    def add_next(self, modeling):
        self.next_list.append(modeling)