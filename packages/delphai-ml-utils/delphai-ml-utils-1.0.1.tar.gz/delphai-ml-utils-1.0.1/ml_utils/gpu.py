import logging

def monitor():
    logging.basicConfig(level=logging.DEBUG, filename='requests.log', format='%(asctime)s/%(levelname)s/%(message)s')
    logging.debug('last request')
