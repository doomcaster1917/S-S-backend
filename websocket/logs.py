import logging


formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler = logging.FileHandler('errors.log')
handler.setFormatter(formatter)

log_parser = logging.getLogger('websocket')
log_parser.setLevel(logging.ERROR)
log_parser.addHandler(handler)
