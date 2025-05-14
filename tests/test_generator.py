import sys
import os
import json
import tempfile
import re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import generator

# ---------- TEST generate_value ----------
def test_generate_value_str_uuid():
    spec = {"type": "str", "mode": "uuid"}
    value = generator.generate_value(spec)
    assert isinstance(value, str)
    assert re.match(r"^[0-9a-f\-]{36}$", value)

def test_generate_value_str_choice():
    spec = {"type": "str", "mode": "choice", "options": ["A", "B"]}
    value = generator.generate_value(spec)
    assert value in ["A", "B"]

def test_generate_value_int_range():
    spec = {"type": "int", "mode": "range", "min": 10, "max": 20}
    value = generator.generate_value(spec)
    assert 10 <= value <= 20

def test_generate_value_timestamp():
    spec = {"type": "timestamp"}
    value = generator.generate_value(spec)
    assert isinstance(value, float)

# ---------- TEST generate_record ----------
def test_generate_record_valid_schema():
    schema = {
        "id": {"type": "int", "mode": "range", "min": 1, "max": 100},
        "name": {"type": "str", "mode": "choice", "options": ["Alice", "Bob"]},
        "created": {"type": "timestamp"}
    }
    record = generator.generate_record(schema)
    assert isinstance(record, dict)
    assert "id" in record and "name" in record and "created" in record

# ---------- TEST write_file ----------
def test_write_file_creates_jsonl():
    schema = {
        "id": {"type": "int", "mode": "fixed", "value": 123},
        "name": {"type": "str", "mode": "fixed", "value": "Test"}
    }
    with tempfile.TemporaryDirectory() as temp_dir:
        generator.write_file(
            path=temp_dir,
            base_name="testfile",
            prefix="count",
            schema=schema,
            lines=3,
            index=1
        )
        files = os.listdir(temp_dir)
        assert len(files) == 1
        file_path = os.path.join(temp_dir, files[0])
        with open(file_path, 'r') as f:
            lines = f.readlines()
            assert len(lines) == 3
            for line in lines:
                obj = json.loads(line)
                assert obj["id"] == 123
                assert obj["name"] == "Test"
