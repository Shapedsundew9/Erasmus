'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/platform_info.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome
Created Date: Friday, May 22nd 2020, 10:30:36 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''


from hashlib import sha256
from logging import getLogger
from platform import machine, processor, python_version, system, release, platform
from .config import get_config
from .database_table import database_table
from cerberus import Validator


__logger = getLogger(__name__)


# See https://en.wikipedia.org/wiki/BogoMips
# This function will only get that MHz & bogoMIPS of the last CPU in the list. The assumption is they are all the same.
# It is recognised that these data is flaky...but it is better than nothing.
def __get_platform_info():
    # TODO: Replace these with an Erasmus benchmark.
    # The metric needs to be stable on a system to 1 unit as it is used in the SHA256 signature to
    # identify the platform.
    performance = 0.0
    return {
        "machine": machine(),
        "processor": processor(),
        "platform": platform(),
        "python_version": python_version(),
        "system": system(),
        "release": release(),
        "performance": performance,
    }


# Add the platform info to the platform info table if it is not already there & return it
def get_platform_info():
    platform_info = __get_platform_info()
    validator = Validator(get_config()['platform_info']['format_file'])
    if not validator.validate(platform_info):
        __logger.error("Platform information validation failed: %s", validator.errors)
        exit(1)
    platform_info = validator.normalized(platform_info)
    pi_table = database_table(__logger, 'platform_info')
    __logger.info("Platform information: %s", str(platform_info))
    if not pi_table.load([{'signature': platform_info['signature']}]):
        __logger.info("New platform registered.")
        pi_table.store([platform_info])
    else:
        __logger.info("Platform already registered.")
    return platform_info['signature']