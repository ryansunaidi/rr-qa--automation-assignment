import logging
import sys
from datetime import datetime

class Logger:
    _logger = None
    
    @staticmethod
    def get_logger(name="QA_Automation"):
        if Logger._logger is None:
            Logger._logger = logging.getLogger(name)
            Logger._logger.setLevel(logging.INFO)
            
            # Create handlers
            console_handler = logging.StreamHandler(sys.stdout)
            file_handler = logging.FileHandler(f'logs/test_run_{datetime.now().strftime("%Y%m%d")}.log')
            
            # Create formatters
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            
            # Set formatters
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)
            
            # Add handlers
            Logger._logger.addHandler(console_handler)
            Logger._logger.addHandler(file_handler)
        
        return Logger._logger