import sys
import logging
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.logger import setup_logger

def test_logger_does_not_duplicate_handlers():
    setup_logger()
    initial_handlers = len(logging.getLogger().handlers)

    # Llamada repetida
    setup_logger()
    subsequent_handlers = len(logging.getLogger().handlers)

    assert initial_handlers == subsequent_handlers