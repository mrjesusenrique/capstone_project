import logging

def setup_logger(log_to_file=False, log_file_path="log.txt"):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Nivel mínimo para capturar

    # Evitar agregar múltiples handlers si ya fue configurado
    if logger.hasHandlers():
        logger.handlers.clear()

    # Formato del mensaje
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # (Opcional) Handler para archivo de log
    if log_to_file:
        file_handler = logging.FileHandler(log_file_path, mode='a')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)