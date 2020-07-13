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
from .platform_info_validator import platform_info_validator


__logger = getLogger(__name__)


# TODO: Implemented EGPOps
def __get_platform_info():
    # TODO: Replace these with an Erasmus benchmark.
    # The metric needs to be stable on a system to 1 unit as it is used in the SHA256 signature to
    # identify the platform.
    performance = 1.0
    return {
        "machine": machine(),
        "processor": processor(),
        "platform": platform(),
        "python_version": python_version(),
        "system": system(),
        "release": release(),
        "EGPOps/s": performance
    }


# Add the platform info to the platform info table if it is not already there & return it
def get_platform_info():
    platform_info = __get_platform_info()
    validator = platform_info_validator(get_config()['tables']['platform_info']['schema'])
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