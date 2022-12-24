from dataProcessing import modeling
import unittest
import os
import shutil
from pathlib import Path
import pickle
from pydantic import BaseModel

class DataModel(BaseModel):
    attr_1 : str
    attr_2 : str
    attr_3 : str

class DataModels(BaseModel):
    outlook : DataModel

class ApplyModeling(modeling.Modeling):

    def process(self, init_data):
        return DataModels(**init_data)

class NoApplyingModeling(modeling.Modeling):

    def process(self, init_data=None):
        temp = []
        for data in init_data:
            temp.append(DataModels(**data))
        return temp 

class NextModeling(modeling.Modeling):

    def process(self, init_data=None):
        return init_data.outlook


class TestModeling(unittest.TestCase):

    def setUp(self) -> None:
        data_1 = {'outlook' : {'attr_1': 'value_1', 'attr_2': 'value_2','attr_3': 'value_3','attr_4': 'value_4'}}
        data_2 = {'outlook' : {'attr_1': 'value_1', 'attr_2': 'value_2','attr_3': 'value_3','attr_4': 'value_4'}}
        data_3 = {'outlook' : {'attr_1': 'value_1', 'attr_2': 'value_2','attr_3': 'value_3','attr_4': 'value_4'}}
        data_4 = {'outlook' : {'attr_1': 'value_1', 'attr_2': 'value_2','attr_3': 'value_3','attr_4': 'value_4'}}
        data_awk = {'outlook' : {'awk_1': 'awk_value_1'}}
        data_list = [data_1,data_2,data_3,data_4, data_awk] 
        self.folder_path = Path.cwd().joinpath('test', 'data_folder')
        self.file_path = Path.cwd().joinpath('test', 'data_folder', 'data_1.pickle')
        os.mkdir(self.folder_path)

        for idx, data in enumerate(data_list):
            file_path = self.folder_path.joinpath(f'data_{idx}.pickle')
            with open(file_path, mode='wb') as fw:
                pickle.dump(data, fw)

    def tearDown(self) -> None:
        shutil.rmtree(self.folder_path)

    # @unittest.skip('for some reason')
    def test_1_simple_modeling(self):
        data = ApplyModeling(folder_path=self.folder_path, apply=True).process_all()
        print(f'Final Modeling data : \n {data}')
    
    # @unittest.skip('for some reason')
    def test_2_origin_modeling(self):
        data = NoApplyingModeling(folder_path=self.folder_path).process_all()
        print(f'Final Modeling data : \n {data}')
    
    # @unittest.skip('for some reason')
    def test_3_file_modeling(self):
        data = ApplyModeling(file_path=self.file_path).process_all()
        print(f'Final Modeling data : \n {data}')

    # @unittest.skip('for some reason')
    def test_4_object_modeling(self):
        data_1 = {'outlook' : {'attr_1': 'value_1', 'attr_2': 'value_2','attr_3': 'value_3','attr_4': 'value_4'}}
        data = ApplyModeling().process_all(data_1)
        print(f'Final Modeling data : \n {data}')

    # @unittest.skip('for some reason')
    def test_5_next_modeling(self):
        md = ApplyModeling(folder_path=self.folder_path, apply=True)
        nmd = NextModeling(apply=True)
        md.add_next(nmd)
        data = md.process_all()
        print(f'Final Modeling data : \n {data}')

if __name__ == '__main__':
    unittest.main()