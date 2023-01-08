import logging
from pathlib import Path
from datetime import datetime
import os

class Dplogger:

    def __init__(self, logger):
        self.logger = logger
    
    def event_call(self, state):
        if state.current_result == 'Success':
            self.logger.info(f'{state.current_index} {state.current_data} {state.current_result}')
        else:
            self.logger.exception(f'{state.current_index} {state.current_data} {state.current_result}')


def get_logger(dir_log_folder_name):
    now = datetime.now().strftime(format='%Y.%m.%d %H%M%S')
    if not os.path.exists(dir_log_folder_name) :
        os.mkdir(dir_log_folder_name)
    dir_file_name = dir_log_folder_name.joinpath(f'{now}_dataProcessing.log')
    logging.basicConfig(
        format='%(asctime)s:%(levelname)s:%(message)s', 
        datefmt='%m/%d/%Y %I:%M"%S %p',
        filename=dir_file_name, level=logging.INFO)
    dplogger = logging.getLogger('dataProcessing')
    return Dplogger(dplogger)