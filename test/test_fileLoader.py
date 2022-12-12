from dataProcessing import fileLoader
import unittest
from pathlib import Path
import os
import shutil
import pickle
import pandas


class Test_pickle_fileloader(unittest.TestCase):

    def setUp(self) -> None:
        data_1 = {'outlook' : {'attr_1': 'value_1', 'attr_2': 'value_2','attr_3': 'value_3','attr_4': 'value_4'}}
        data_2 = {'outlook' : {'attr_1': 'value_1', 'attr_2': 'value_2','attr_3': 'value_3','attr_4': 'value_4'}}
        data_3 = {'outlook' : {'attr_1': 'value_1', 'attr_2': 'value_2','attr_3': 'value_3','attr_4': 'value_4'}}
        data_4 = {'outlook' : {'attr_1': 'value_1', 'attr_2': 'value_2','attr_3': 'value_3','attr_4': 'value_4'}}
        data_list = [data_1,data_2,data_3,data_4] 
        self.folder_path = Path.cwd().joinpath('test', 'data_folder')
        self.file_path = Path.cwd().joinpath('test', 'data_folder', 'data_1.pickle')
        os.mkdir(self.folder_path)

        for idx, data in enumerate(data_list):
            file_path = self.folder_path.joinpath(f'data_{idx}.pickle')
            with open(file_path, mode='wb') as fw:
                pickle.dump(data, fw)
        
    
    def tearDown(self) -> None:
        shutil.rmtree(self.folder_path)


    def test_1_pickle(self):
        data = fileLoader.Factory_fileLoader().get_file_loader(type='.pickle')().load(self.folder_path, path_type='folder')
        print(f'folder_data : \n {data}')

        data = fileLoader.Factory_fileLoader().get_file_loader(type='.pickle')().load(self.file_path, path_type='file')
        print(f'file_data : \n {data}')

if __name__ == '__main__':
    unittest.main()