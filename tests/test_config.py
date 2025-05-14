import sys
import os
import tempfile
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import load_config

def test_load_valid_config():
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        tmp.write('[DEFAULT]\noutput_path = ./data\nfiles_count = 2\n')
        tmp_path = tmp.name

    config = load_config(tmp_path)
    assert config['output_path'] == './data'
    assert config['files_count'] == '2'

    os.remove(tmp_path)


def test_load_config_file_not_found(monkeypatch):
    with pytest.raises(SystemExit) as e:
        load_config('nonexistent.ini')
    assert e.type == SystemExit
    assert e.value.code == 1