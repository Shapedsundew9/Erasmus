'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/work.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome
Created Date: Monday, June 29th 2020, 9:45:43 am
Author: Shapedsundew9


Copyright (c) 2020 Your Company
'''


from .config import get_config, update_config
from .database_table import database_table
from .work_registry_validator import work_registry_validator
from logging import getLogger


_logger = getLogger(__name__)


def register_work(work_config):
    validator = work_registry_validator(get_config()['tables']['work_registry']['schema'])
    if not validator.validate(work_config):
        _logger.warning("Invalid work configuration: %s", validator.errors)
        exit(1)
    work_config = validator.normalized(work_config)
    work_registry = database_table(_logger, 'work_registry')
    work_registry.store([work_config])
    return work_config['signature']