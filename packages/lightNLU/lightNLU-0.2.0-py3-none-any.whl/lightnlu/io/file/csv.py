# -*- coding: utf-8 -*-
import csv

from lightutils import check_file


def from_csv(path: str):
    check_file(path, 'csv')

    with open(path, encoding='utf8') as file:
        dic_reader = csv.DictReader(file)
        for item in dic_reader:
            yield dict(item)
