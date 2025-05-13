import argparse
import sys
import os
import logging

from generator import generate_files
from config import load_config
from logger import setup_logger

def parse_arguments(defaults):
    parser = argparse.ArgumentParser(
        description="Utilidad para generar datos de prueba en formato JSON"
    )

    parser.add_argument('--path_to_save_files', default=defaults.get('path_to_save_files'), help='Ruta para guardar los archivos generados')
    parser.add_argument('--files_count', type=int, default=defaults.getint('files_count'), help='Cantidad de archivos a generar')
    parser.add_argument('--file_name', default=defaults.get('file_name'), help='Nombre base de los archivos')
    parser.add_argument('--file_prefix', choices=['count', 'random', 'uuid'], default=defaults.get('file_prefix'), help='Prefijo para los archivos')
    parser.add_argument('--data_schema', required=True, help='Ruta al esquema de datos o esquema en línea')
    parser.add_argument('--lines_per_file', type=int, default=defaults.getint('lines_per_file'), help='Cantidad de líneas por archivo')
    parser.add_argument('--clear_path', action='store_true', help='Eliminar archivos existentes en la ruta antes de generar nuevos')
    parser.add_argument('--multiprocessing', type=int, default=defaults.getint('multiprocessing'), help='Cantidad de procesos paralelos a usar')

    return parser.parse_args()

def main():
    # Setup logging
    setup_logger()
    logging.info("Inicializando la utilidad de generación de datos.")

    # Cargar configuración por defecto
    defaults = load_config()

    # Parsear argumentos
    args = parse_arguments(defaults)

    # Valida el parámetro lines_per_file
    if args.lines_per_file is None:
        logging.error("El valor 'lines_per_file' no está definido en los argumentos ni en default.ini.")
        sys.exit(1)

    # Validaciones mínimas
    if args.files_count < 0:
        logging.error('--files_count no puede ser negativo.')
        sys.exit(1)

    if args.multiprocessing < 1:
        logging.warning('--multiprocessing menor a 1. Se forzará a 1.')
        args.multiprocessing = 1

    # Normalizar path
    save_path = os.path.abspath(args.path_to_save_files)
    logging.info(f"Ruta de guardado normalizada a: {save_path}")

    if not os.path.exists(save_path):
        os.makedirs(save_path)
        logging.info(f"Directorio creado: {save_path}")
    elif not os.path.isdir(save_path):
        logging.error("La ruta especificada no es un directorio.")
        sys.exit(1)

    # Llamar al generador
    generate_files(args, save_path)
    logging.info("Generación de archivos completada exitosamente.")

if __name__ == "__main__":
    main()
