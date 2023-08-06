# -*- coding: utf-8 -*-
import os
import re
import csv
import pickle
from collections import defaultdict
from typing import Dict, List

from tqdm import tqdm
from lightutils import logger, get_file_name, check_file, load_yaml

from ..utils.keyword import KeywordProcessor
from ..io import from_yaml, from_mongo, from_csv, from_txt, from_json

func_dic = {
    "yml": from_yaml,
    "mongo": from_mongo,
    "csv": from_csv,
    "txt": from_txt,
    "json": from_json
}

time_re = re.compile(r"((?P<year>\d{2,4})年)?((?P<month>\d{1,2})月)?((?P<day>\d{1,2})日)(?P<time>(?P<hour>\d{1,2})[:：](?P<min>\d{1,2})([:：](?P<sec>\d{1,2}))?)?")
voltage_re = re.compile(r"(?P<voltage>\d+)(千伏|kv|KV|Kv|kV)")


def extract_time(sentence: str) -> list:
    res = []
    for x in time_re.finditer(sentence):
        res.append([
            x.group(),
            *x.span()
        ])
    return res


def extract_voltage(sentence: str) -> list:
    res = []
    for x in voltage_re.finditer(sentence):
        res.append([
            x.group(),
            *x.span()
        ])
    return res


def default_type():
    return list()


class NER:
    def __init__(self):
        self._kp = KeywordProcessor()
        self._entity_dict = defaultdict(default_type)
        self._data = dict()
        self._model_path: str = ""

    def build_from_yml(self, path: str, base_dir: str = None):
        infos: List[Dict] = load_yaml(path)
        for info in infos:
            # print(info)
            config = info["config"]
            if "path" in config:
                config["path"] = os.path.join(base_dir, config["path"])
            # 增加实体item信息
            for item in func_dic[info["type"]](**config):
                # print(item)
                self._entity_dict[item["name"]].append({"type": info["name"], "id": item["id"]})
                self._kp.add_keyword(item["name"])
            # 增加类型信息
            for alias in info["aliases"]:
                self._entity_dict[alias].append({"type": '@' + info["name"], "id": None})
                self._kp.add_keyword(alias)

    def add_word(self, word: str, word_id: str, word_type: str):
        if {
            "type": word_type,
            "id": word_id
        } not in self._entity_dict[word]:
            self._entity_dict[word].append({
                "type": word_type,
                "id": word_id
            })
        if word not in self._kp:
            self._kp.add_keyword(word)
        logger.info(f"成功添加 {word}")
        return True

    def del_word(self, word: str):
        if word in self._entity_dict:
            del self._entity_dict[word]
            self._kp.remove_keyword(word)
            logger.info(f"成功删除 {word}")
        else:
            logger.info(f"词表中无{word}，无需删除")
        return True

    def update(self, save_path: str = None):
        if not save_path:
            if not self._model_path:
                raise Exception("未指定模型路径")
            else:
                save_path = self._model_path
        logger.info("模型将更新保存至{}中".format(save_path))
        with open(self._model_path, 'wb') as file:
            pickle.dump(self._kp, file)
            pickle.dump(self._entity_dict, file)
        logger.info("成功将模型更新保存至{}中".format(save_path))

    def save(self, save_path: str = 'ner.pt'):
        logger.info("将模型保存至{}中".format(save_path))
        self._model_path = save_path
        with open(save_path, 'wb') as file:
            pickle.dump(self._kp, file)
            pickle.dump(self._entity_dict, file)
        logger.info("成功将模型保存至{}中".format(save_path))

    def load(self, save_path: str = 'ner.pt'):
        logger.info("从{}中加载模型中".format(save_path))
        self._model_path = save_path
        with open(save_path, 'rb') as file:
            self._kp = pickle.load(file)
            self._entity_dict = pickle.load(file)
        logger.info("成功从{}中加载模型".format(save_path))

    def __contains__(self, item):
        return item in self._entity_dict

    def get(self, item):
        return self._entity_dict[item]

    def extract(self, sentence: str):
        times = extract_time(sentence)
        voltages = extract_voltage(sentence)
        keywords = self._kp.extract_keywords(sentence, span_info=True)
        # res = [(x[0], self._entity_dict[x[0]], x[1], x[2]) for x in keywords]
        res = [(x[0], self._entity_dict[x[0]][0], x[1], x[2]) for x in keywords]
        res.extend([(x[0], {"id": None, "type": "voltage"}, x[1], x[2]) for x in voltages])
        res.extend([(x[0], {"id": None, "type": "time"}, x[1], x[2]) for x in times])
        res.sort(key=lambda x: x[2])
        return res

    @property
    def entities(self):
        return self._entity_dict
