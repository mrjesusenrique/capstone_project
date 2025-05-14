import json
import os
import logging
import time
import uuid
import random

from multiprocessing import Process, current_process, cpu_count
from .schema_parser import parse_schema

from .utils import (
    generate_uuid,
    generate_random_int,
    clear_output_path
)

def generate_value(field_spec):
    field_type = field_spec["type"]
    mode = field_spec.get("mode")

    if field_type == "str":
        if mode == "uuid":
            return str(uuid.uuid4())
        elif mode == "choice":
            return random.choice(field_spec["options"])
        elif mode == "fixed":
            return field_spec["value"]
        else:
            return ""
        
    elif field_type == "int":
        if mode == "range":
            return random.randint(field_spec["min"], field_spec["max"])
        elif mode == "choice":
            return random.choice(field_spec["options"])
        elif mode == "fixed":
            return field_spec["value"]
        else:
            return None

    elif field_type == "timestamp":
        return time.time()

    else:
        logging.error(f"Tipo no soportado: {field_type}")
        return None


def generate_record(schema):
    record = {}
    for key, spec in schema.items():
        record[key] = generate_value(spec)
    return record

def write_file(path, base_name, prefix, schema, lines, index=None):
    records = [generate_record(schema) for _ in range(lines)]

    if index is not None:
        if prefix == "count":
            suffix = f"{index}"
        elif prefix == "random":
            suffix = str(generate_random_int(1000, 9999))
        elif prefix == "uuid":
            suffix = generate_uuid()
        else:
            suffix = ""
        filename = f"{base_name}_{suffix}.jsonl"
    else:
        filename = f"{base_name}.jsonl"

    full_path = os.path.join(path, filename)
    with open(full_path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")
    logging.info(f"{current_process().name} escribió: {filename}")

def worker(start_idx, count, args, schema, save_path):
    for i in range(start_idx, start_idx + count):
        write_file(
            path=save_path,
            base_name=args.file_name,
            prefix=args.file_prefix,
            schema=schema,
            lines=args.lines_per_file,
            index=i
        )

def generate_files(args, save_path):
    schema = parse_schema(args.data_schema)

    if args.clear_path:
        clear_output_path(save_path, args.file_name)

    total_files = args.files_count
    n_processes = args.multiprocessing

    if n_processes > cpu_count():
        logging.warning(f"--multiprocessing limitado a {cpu_count()}")
        n_processes = cpu_count()

    if total_files == 0:
        for _ in range(args.lines_per_file):
            print(json.dumps(generate_record(schema)))
        return

    if n_processes == 1 or total_files < n_processes:
        for i in range(total_files):
            write_file(
                path=save_path,
                base_name=args.file_name,
                prefix=args.file_prefix,
                schema=schema,
                lines=args.lines_per_file,
                index=i
            )
    else:
        files_per_proc = total_files // n_processes
        remainder = total_files % n_processes

        processes = []
        start = 0
        for i in range(n_processes):
            count = files_per_proc + (1 if i < remainder else 0)
            p = Process(
                target=worker,
                args=(start, count, args, schema, save_path),
                name=f"Proceso-{i+1}"
            )
            p.start()
            processes.append(p)
            start += count

        for p in processes:
            p.join()
