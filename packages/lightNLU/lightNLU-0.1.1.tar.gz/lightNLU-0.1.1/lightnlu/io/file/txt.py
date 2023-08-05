# -*- coding: utf-8 -*-

def from_txt(path: str):
    with open(path, encoding='utf8') as file:
        for line in file:
            if line.strip():
                yield line.strip()
