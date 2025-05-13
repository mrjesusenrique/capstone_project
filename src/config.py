import configparser
import sys
import logging


def load_config(path='default.ini'):
    config = configparser.ConfigParser()
    read_files = config.read(path)

    if not read_files:
        logging.error(f"No se pudo leer el archivo de configuración en {path}.")
        sys.exit(1)

    if 'DEFAULT' not in config:
        logging.error("La sección 'DEFAULT' no está definida en el archivo de configuración.")
        sys.exit(1)

    return config['DEFAULT']
