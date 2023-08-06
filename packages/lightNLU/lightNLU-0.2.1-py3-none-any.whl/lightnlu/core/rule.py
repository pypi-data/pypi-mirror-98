# -*- coding: utf-8 -*-
from typing import Dict, List, Callable
import pickle
from functools import wraps
from collections import defaultdict

from lightutils import load_yaml, logger


class DomainNotFindException(Exception):
    def __init__(self, domain: str):
        self._domain = domain

    def __str__(self):
        return "domain: {} not found!".format(self._domain)

    def __repr__(self):
        return self.__str__()


class RuleNotFindException(Exception):
    def __init__(self, rule_name: str):
        self._rule_name = rule_name

    def __str__(self):
        return "rule_name: {} not found!".format(self._rule_name)

    def __repr__(self):
        return self.__str__()


def helper_func():
    return defaultdict(dict)


class Rule:
    def __init__(self):
        self._rules: Dict[str, Dict[str, List]] = defaultdict(dict)
        self._model_path: str = ""
        self._func_dict: Dict[str, Dict[str, Dict[str, Callable]]] = defaultdict(helper_func)

    def build_from_yml(self, path: str):
        domains: List[Dict] = load_yaml(path)
        for domain_item in domains:
            domain_name = domain_item["domain"]
            rules = domain_item["rules"]
            for rule in rules:
                rule_name = rule["name"]
                patterns = rule["patterns"]
                self._rules[domain_name][rule_name] = patterns

    def match(self, slots: List, domain: str):
        res = []
        for name, patterns in self._rules[domain].items():
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
                        info[pat_item[2]] = {
                            "word": slot[0],
                            "type": slot[1]["type"],
                            "id": slot[1]["id"],
                            "left": slot[2],
                            "right": slot[3]
                        }
                if flag:
                    res.append({"name": name, "slots": info})
                    # break
        return res

    def bind(self, domain: str, rule_name: str, act_name: str):
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            self.register(domain, rule_name, act_name, func)
            return wrapper
        return decorator

    def register(self, domain: str, rule_name: str, act_name: str, func: Callable):
        if domain not in self._rules:
            raise DomainNotFindException(domain)
        if rule_name not in self._rules[domain]:
            raise RuleNotFindException(rule_name)
        self._func_dict[domain][rule_name][act_name] = func

    def match_and_act(self, slots: List, domain: str):
        match_results = self.match(slots, domain)
        res = {}
        if match_results:
            for match_item in match_results:
                if match_item["name"] in self._func_dict[domain]:
                    res[match_item["name"]] = {}
                    for act_name, act_func in self._func_dict[domain][match_item["name"]].items():
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
