from abc import ABC, abstractmethod
import os
import pickle
import json
import pandas as pd
from tqdm import tqdm

class FileLoader(ABC):

    @abstractmethod
    def load(self, path, path_type):
        pass


class PickleLoader(FileLoader):

    def load(self, path, path_type):
        if path_type == 'file':
            with open(path, mode='rb') as fr:
                data = pickle.load(fr)
            return data
        if path_type == 'folder':
            file_list = os.listdir(path)
            temp = []
            for file in tqdm(file_list, desc='[dataProcessing] file_loading...'):
                file_path = path.joinpath(file)
                with open(file_path, mode='rb') as fr:
                    data = pickle.load(fr)
                    temp.append(data)
            return temp

class CsvLoader(FileLoader):

    def load(self, path, path_type):
        if path_type == 'file':
            data = pd.read_csv(path, encoding='utf8')
            return data
        if path_type == 'folder_path':
            file_list = os.listdir(path)
            temp = []
            for file in tqdm(file_list, desc='[dataProcessing] file_loading...'):
                file_path = path.joinpath(file)
                data = pd.read_csv(file_path, encoding='utf8')
                temp.append(data)
            return temp

class JsonLoader(FileLoader):

    def load(self, path, path_type):
        if path_type == 'file':
            with open(path) as f:
                data = json.load(f)
            return data
        
        if path_type == 'folder':
            file_list = os.listdir(path)
            temp = []
            for file in tqdm(file_list, desc='[dataProcessing] file_loading...'):
                file_path = path.joinpath(file)
                with open(file_path) as f:
                    data = json.load(f)
                    temp.append(data)
            return temp


class Factory_fileLoader:

    def get_file_loader(self, type):
        option = {'.pickle':PickleLoader, '.csv':CsvLoader, '.json':JsonLoader} 
        return option.get(type) 