'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/worker.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Tuesday, May 5th 2020, 6:00:39 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''

from .platform_info import get_platform_info
from .config import get_config
from .database_table import database_table
from .worker_registry_validator import worker_registry_validator
from copy import deepcopy
from logging import getLogger


class worker():


    __logger = getLogger(__name__)
    __worker_registry = None


    # Work is the signature of the registered work.
    def __init__(self, work_signature):
        self.registration_document = { "platform": get_platform_info(), "work": work_signature }
        validator = worker_registry_validator()
        if not validator.validate(self.registration_document):
            worker.__logger.error("Invalid worker registration document: %s", validator.errors)
            exit(1)
        self.registration_document = validator.normalized(self.registration_document)
        if worker.__worker_registry is None: worker.__worker_registry = database_table(worker.__logger, get_config()['worker_registry'])
        worker.__worker_registry.store([self.registration_document])


    # Initialise
    # ----------
    # 1. Get latest work definition
    # 2a. Create the gene pool
    # 2b. Verify the fitness function produces the same results.
    #
    # Loop
    # ----
    # 3. Mutate and assess
    # 4. Lock the work definition & read it (may have been updated by another worker)
    # 5. Merge generations
    # 6. Cull
    # 7. Update work definition and unlock
    # 8. Log work results & stats
    # 9. Update gene pool
    # 10. Assess stoppping criteria (and stop if met)
    # 11. Go to #3.
    def work(self):
        pass