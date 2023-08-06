import os
import logging
import time
from datetime import datetime


def monitor():
    logging.basicConfig(level=logging.DEBUG, filename='requests.log', format='%(asctime)s/%(levelname)s/%(message)s')
    logging.info('recived a request')

