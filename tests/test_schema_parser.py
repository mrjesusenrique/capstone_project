import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import schema_parser

# ----------
# TEST: load_schema
# ----------

def test_load_schema_from_string():
    schema_str = '{"field1": "str:hello"}'
    result = schema_parser.load_schema(schema_str)
    assert result == {"field1": "str:hello"}


def test_load_schema_from_file(tmp_path):
    schema_path = tmp_path / "schema.json"
    schema_path.write_text('{"field1": "str:hello"}')

    result = schema_parser.load_schema(str(schema_path))
    assert result == {"field1": "str:hello"}


# ----------
# TEST: parse_schema
# ----------

def test_parse_schema_fixed_string():
    schema = '{"name": "str:John"}'
    parsed = schema_parser.parse_schema(schema)
    assert parsed == {'name': {'type': 'str', 'mode': 'fixed', 'value': 'John'}}


def test_parse_schema_random_string():
    schema = '{"id": "str:rand"}'
    parsed = schema_parser.parse_schema(schema)
    assert parsed == {'id': {'type': 'str', 'mode': 'uuid'}}


def test_parse_schema_string_choice():
    schema = '{"type": "str:[\\"A\\", \\"B\\"]"}'
    parsed = schema_parser.parse_schema(schema)
    assert parsed == {'type': {'type': 'str', 'mode': 'choice', 'options': ['A', 'B']}}


def test_parse_schema_int_fixed():
    schema = '{"age": "int:30"}'
    parsed = schema_parser.parse_schema(schema)
    assert parsed == {'age': {'type': 'int', 'mode': 'fixed', 'value': 30}}


def test_parse_schema_int_range():
    schema = '{"score": "int:rand(10, 20)"}'
    parsed = schema_parser.parse_schema(schema)
    assert parsed == {'score': {'type': 'int', 'mode': 'range', 'min': 10, 'max': 20}}


def test_parse_schema_int_choice():
    schema = '{"level": "int:[1, 2, 3]"}'
    parsed = schema_parser.parse_schema(schema)
    assert parsed == {'level': {'type': 'int', 'mode': 'choice', 'options': [1, 2, 3]}}


def test_parse_schema_timestamp():
    schema = '{"created": "timestamp:"}'
    parsed = schema_parser.parse_schema(schema)
    assert parsed == {'created': {'type': 'timestamp'}}
