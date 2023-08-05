# -*- coding: utf-8 -*-
from typing import Dict, List, Callable
import pickle
from functools import wraps
from collections import defaultdict

from lightutils import load_yaml, logger


class RuleNotFindException(Exception):
    def __init__(self, rule_name: str):
        self._rule_name = rule_name

    def __str__(self):
        return "rule_name: {} not found!".format(self._rule_name)

    def __repr__(self):
        return self.__str__()


class Rule:
    def __init__(self):
        self._rules: Dict[str, List] = {}
        self._model_path: str = ""
        self._func_dict: Dict[str, Dict[str, Callable]] = defaultdict(dict)

    def build_from_yml(self, path: str):
        rules: List[Dict] = load_yaml(path)
        for rule in rules:
            # print(rule)
            self._rules[rule["name"]] = rule["patterns"]

    def match(self, slots: List):
        res = []
        for name, patterns in self._rules.items():
            for pattern in patterns:
                # print(pattern)
                if len(pattern) != len(slots):
                    continue
                info = dict()
                flag = True
                for pat_item, slot in zip(pattern, slots):
                    slot_info = slot[1]
                    if pat_item[0] != slot_info["type"]:
                        flag = False
                        break
                    if pat_item[1] and pat_item[1] != slot_info["id"]:
                        flag = False
                        break
                    if pat_item[2]:
                        info[pat_item[2]] = slot[0]
                if flag:
                    res.append({"name": name, "slots": info})
                    # break
        return res

    def bind(self, rule_name: str, act_name: str):
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            if rule_name not in self._rules:
                raise RuleNotFindException(rule_name)
            self._func_dict[rule_name][act_name] = func
            return wrapper
        return decorator

    def match_and_act(self, slots: List):
        match_results = self.match(slots)
        res = {}
        if match_results:
            for match_item in match_results:
                if match_item["name"] in self._func_dict:
                    res[match_item["name"]] = {}
                    for act_name, act_func in self._func_dict[match_item["name"]].items():
                        res[match_item["name"]][act_name] = act_func(**match_item["slots"])
        return res

    def save(self, save_path: str = 'rule.pt'):
        logger.info("将模型保存至{}中".format(save_path))
        self._model_path = save_path
        with open(save_path, 'wb') as file:
            pickle.dump(self._rules, file)
        logger.info("成功将模型保存至{}中".format(save_path))

    def load(self, save_path: str = 'ner.pt'):
        logger.info("从{}中加载模型中".format(save_path))
        self._model_path = save_path
        with open(save_path, 'rb') as file:
            self._rules = pickle.load(file)
        logger.info("成功从{}中加载模型".format(save_path))

    @property
    def rules(self):
        return self._rules

    @property
    def actors(self):
        return self._func_dict
