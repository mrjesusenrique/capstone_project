import uuid
import random
import time
import os
import logging


def generate_uuid():
    return str(uuid.uuid4())

def generate_random_int(min_val, max_val):
    return random.randint(min_val, max_val)

def generate_timestamp():
    return time.time()

def choose_random_from_list(values):
    return random.choice(values)

def clear_output_path(path, file_name_prefix):
    """
    Elimina archivos en el path de salida que comiencen con el prefijo especificado.
    """
    logging.info(f"Limpieza del directorio: {path}")
    for filename in os.listdir(path):
        if filename.startswith(file_name_prefix) and filename.endswith(".jsonl"):
            try:
                os.remove(os.path.join(path, filename))
                logging.debug(f"Archivo eliminado: {filename}")
            except Exception as e:
                logging.error(f"No se pudo eliminar {filename}: {e}")
