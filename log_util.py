import os,sys
from os.path import dirname
from loguru import logger

log_path = os.path.join(dirname(os.path.abspath(__file__)),'log')
# print(log_path)
file_normal = os.path.join(log_path,'quant.log')
file_error = os.path.join(log_path,'quant_error.log')

config = {
    "handlers": [
        {"sink": sys.stdout, "format": "{time} - {message}"},
        {"sink": file_normal, 
            "level": "INFO", "format":"{time} {level} {message}",
            "rotation":"10 days",},
        {"sink": file_error, 
            "level": "WARNING", "format":"{time} {level} {message}",},
    ],
}
logger.configure(**config)