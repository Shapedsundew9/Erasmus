"""A population is a collection of individuals for a specific fitness function.

Created Date: Friday, January 17th 2020, 4:38:35 pm
Author: Shaped Sundew
"""


from hashlib import sha256
from logging import getLogger
from .config import get_config
from .database_table import database_table


__logger = getLogger(__name__)


class population():

    def __init__(self, p_config):
