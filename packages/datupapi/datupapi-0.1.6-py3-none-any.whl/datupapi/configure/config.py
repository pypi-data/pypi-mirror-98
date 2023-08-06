import logging
import os
import yaml

from datetime import date, datetime, timedelta


class Config():

    LOCAL_PATH = '/tmp'

    def __init__(self, config_file=None, logfile=None):
        try:
            #Initialize config parameters
            with open(config_file) as file:
                params_list = yaml.load(file, Loader=yaml.FullLoader)
            self.access_key = params_list.get('aws_access_key')
            self.secret_key = params_list.get('aws_secret_key')
            self.region = params_list.get('aws_region')
            self.datalake = params_list.get('datalake')
            self.logfile = logfile + '_' + datetime.today().strftime("%d%m%Y-%H%M%S") + '.log'
            # Initialize logger
            self.logger = logging.getLogger('__name__')
            self.logger.setLevel(logging.DEBUG)
            self.file_handler = logging.FileHandler(os.path.join(Config.LOCAL_PATH, self.logfile))
            self.file_format = logging.Formatter('%(asctime)s|%(levelname)s|%(name)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            self.file_handler.setLevel(logging.DEBUG)
            self.file_handler.setFormatter(self.file_format)
            self.logger.addHandler(self.file_handler)
        except FileNotFoundError as err:
            self.logger.exception(f'Config file not found. Please check entered path: {err}')
            raise
        finally:
            file.close()

