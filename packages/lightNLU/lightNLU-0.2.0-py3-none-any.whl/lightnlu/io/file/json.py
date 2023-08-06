# -*- coding: utf-8 -*-
import json

from lightutils import check_file


def from_json(path: str):
    check_file(path, 'json')

    with open(path, encoding='utf8') as file:
        for line in file:
            if line.strip():
                yield json.loads(line.strip())
