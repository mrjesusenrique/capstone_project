import sys
import os
import re
import tempfile
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import utils

def test_generate_uuid():
    uid = utils.generate_uuid()
    assert isinstance(uid, str)
    assert re.match(r'^[a-f0-9\-]{36}$', uid), "UUID mal formado"

def test_generate_random_int():
    value = utils.generate_random_int(5, 10)
    assert 5 <= value <= 10

def test_generate_timestamp():
    ts = utils.generate_timestamp()
    assert isinstance(ts, float)
    assert ts > 0

def test_choose_random_from_list():
    options = ['x', 'y', 'z']
    result = utils.choose_random_from_list(options)
    assert result in options

def test_clear_output_path():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Crear archivos que deberían ser eliminados
        for name in ['testfile1.jsonl', 'testfile2.jsonl']:
            with open(os.path.join(temp_dir, name), 'w') as f:
                f.write('data')

        # Crear archivo que NO debe eliminarse
        with open(os.path.join(temp_dir, 'keepfile.jsonl'), 'w') as f:
            f.write('data')

        # Ejecutar limpieza
        utils.clear_output_path(temp_dir, 'testfile')

        remaining = os.listdir(temp_dir)
        assert 'keepfile.jsonl' in remaining
        assert not any(fname.startswith('testfile') for fname in remaining)
