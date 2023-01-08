import os
from abc import ABC, abstractmethod
from dataProcessing import fileLoader, observer
from dataclasses import dataclass
from tqdm import tqdm
from pathlib import Path

def export_type(path):
    return os.path.splitext(path)[-1]

def get_first_file_path(folder_path):
    first_file = os.listdir(folder_path)[0]
    return folder_path.joinpath(first_file)

def get_log_point(idx, folder_path):
    if folder_path:
        return os.listdir(folder_path)[idx]
    return f'index : {idx}'

def down_dimension(data, num):
    data = data
    for i in range(0, num):
        data = [w for i in data for w in i]
    return data        

@dataclass
class State:
    current_data: str 
    current_index: str
    current_result : str 
    total_success : int
    total_fails : int


class Modeling(ABC):

    def __init__(self, folder_path=None, file_path=None, apply=False, dim_down=None):
        self.folder_path = folder_path
        self.file_list = self.get_file_list(folder_path)
        self.file_path = file_path
        self.apply = apply
        self.dim_down = dim_down
        self.next_list = [] 
        self.state = State(current_data='none', current_index='none', current_result='none', total_success=0, total_fails=0)
        self.observer_list = []
        self.add_basic_obsever()
    
    def get_file_list(self, folder_path):
        if folder_path:
            return os.listdir(folder_path)
        return None

    def get_init_data(self, init_data):
        if self.folder_path:
            path = get_first_file_path(self.folder_path)
            type = export_type(path)
            return fileLoader.Factory_fileLoader().get_file_loader(type)().load(self.folder_path, path_type='folder')
        if self.file_path:
            type = export_type(self.file_path)
            return fileLoader.Factory_fileLoader().get_file_loader(type)().load(self.file_path, path_type='file')
        return init_data 

    @abstractmethod
    def process(self, init_data=None):
        pass

    def handle_process(self, init_data=None, index=None, folder_base=False):
        try:
            data = self.process(init_data=init_data)
            self.set_state(index=index, folder_base=folder_base, result='Success')
            return data 
        except:
            self.set_state(index=index, folder_base=folder_base, result='Fail')
            pass
    
    def process_all(self, init_data=None):
        init_data = self.get_init_data(init_data)
        if self.apply:
            processed_data = [i for i in (self.handle_process(data, idx, folder_base=self.folder_path) for idx, data in enumerate(tqdm(init_data, desc='[dataProcessing] now applying modeling for each data'))) if i is not None]
        else:
            processed_data = self.handle_process(init_data)
        if self.dim_down :
            processed_data = down_dimension(data=processed_data, num=self.dim_down)

        if self.next_list:
            for next_modeling in self.next_list:
                processed_data = next_modeling.process_all(processed_data)
        print(f'[dataProcessing] proecss all done. total : {self.state.total_success + self.state.total_fails}, success : {self.state.total_success}, fail : {self.state.total_fails}')
        return processed_data

    def add_next(self, modeling):
        self.next_list.append(modeling)
    
    def set_state(self, index, folder_base, result):
        if index:
            current_index=index
        else:
            current_index=''
        if folder_base:
            current_data = self.file_list[index]
        else:
            current_data = 'object'
        if result == 'Success' :
            self.state = State(current_data=current_data, current_index=current_index, current_result=result, total_success=self.state.total_success+1, total_fails=self.state.total_fails)
        else :
            self.state = State(current_data=current_data, current_index=current_index, current_result=result, total_success=self.state.total_success, total_fails=self.state.total_fails+1)
        self.notify()
    
    def notify(self):
        for i in self.observer_list:
            i.event_call(self.state)

    def add_observer(self, observer):
        self.observer_list.append(observer)
    
    def add_basic_obsever(self):
        self.add_observer(observer.get_logger(dir_log_folder_name=Path.cwd().joinpath('log')))