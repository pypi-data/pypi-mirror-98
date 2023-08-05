# -*- coding: utf-8 -*-
from lightutils import load_yaml, check_file


def from_yaml(path: str):
    check_file(path, 'yml')
    content = load_yaml(path)
    for key, items in content.items():
        for item in items:
            yield {"name": item, "id": key}
