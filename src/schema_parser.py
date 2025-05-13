import json
import os
import sys
import logging
import re

logger = logging.getLogger(__name__)

SUPPORTED_TYPES = ['str', 'int', 'timestamp']

def load_schema(schema_input):
    """
    Loads the schema from a JSON string or file path.
    """
    try:
        if os.path.isfile(schema_input):
            with open(schema_input, 'r') as f:
                schema = json.load(f)
        else:
            schema = json.loads(schema_input)
    except Exception as e:
        logger.error(f"Failed to load data schema: {e}")
        sys.exit(1)
    
    return schema

def parse_schema(schema_input):
    """
    Validates and parses the schema into a structured dictionary.
    """
    raw_schema = load_schema(schema_input)
    parsed_schema = {}

    for key, value in raw_schema.items():
        if ':' not in value:
            logger.error(f"Invalid format for field '{key}': missing ':'")
            sys.exit(1)

        field_type, _, detail = value.partition(':')
        field_type = field_type.strip()
        detail = detail.strip()

        if field_type not in SUPPORTED_TYPES:
            logger.error(f"Unsupported type in field '{key}': '{field_type}'")
            sys.exit(1)

        if field_type == 'timestamp':
            if detail:
                logger.warning(f"Ignoring extra detail for timestamp field '{key}': '{detail}'")
            parsed_schema[key] = {'type': 'timestamp'}

        elif field_type == 'str':
            if detail == 'rand':
                parsed_schema[key] = {'type': 'str', 'mode': 'uuid'}
            elif re.match(r'^\[.*\]$', detail):
                try:
                    # Allow JSON-style or Python-style lists
                    options = json.loads(detail.replace("'", '"'))
                    parsed_schema[key] = {'type': 'str', 'mode': 'choice', 'options': options}
                except Exception:
                    logger.error(f"Invalid list in field '{key}': {detail}")
                    sys.exit(1)
            else:
                parsed_schema[key] = {'type': 'str', 'mode': 'fixed', 'value': detail}

        elif field_type == 'int':
            if detail.startswith('rand('):
                try:
                    m = re.match(r'rand\((\d+),\s*(\d+)\)', detail)
                    if not m:
                        raise ValueError
                    min_val = int(m.group(1))
                    max_val = int(m.group(2))
                    parsed_schema[key] = {'type': 'int', 'mode': 'range', 'min': min_val, 'max': max_val}
                except:
                    logger.error(f"Invalid rand() format in field '{key}': {detail}")
                    sys.exit(1)
            elif re.match(r'^\[.*\]$', detail):
                try:
                    options = json.loads(detail)
                    parsed_schema[key] = {'type': 'int', 'mode': 'choice', 'options': options}
                except Exception:
                    logger.error(f"Invalid list in field '{key}': {detail}")
                    sys.exit(1)
            elif detail == '':
                parsed_schema[key] = {'type': 'int', 'mode': 'none'}
            else:
                try:
                    value = int(detail)
                    parsed_schema[key] = {'type': 'int', 'mode': 'fixed', 'value': value}
                except:
                    logger.error(f"Invalid fixed int value in field '{key}': {detail}")
                    sys.exit(1)

    return parsed_schema
