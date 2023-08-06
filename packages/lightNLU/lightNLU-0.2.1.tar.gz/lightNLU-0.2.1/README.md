# lightNLU

一个小巧简单的基于模板匹配的自然语言理解框架。

## 简介

一个基于Python实现的小巧简单的基于模板匹配的自然语言理解框架。
这里的自然语言理解仅指意图识别和词槽提取。

## 安装

```shell script
pip install lightnlu
```

## 特性

- 特别轻量
- 模板文件使用yml格式
- 支持多源数据导入
- 模板语法简明易懂

## 使用示例

### step1:定制词表规则

如编写`words.yml`文件如下：

```yaml
-
  name: person
  aliases:
    - 人物
  type: json
  config:
    path: data/person.json
-
  name: place
  aliases:
    - 地点
    - 位置
    - 城市
    - 区域
  type: csv
  config:
    path: data/place.csv
-
  name: relation
  aliases: []
  type: yml
  config:
    path: data/relation.yml
-
  name: predicate
  aliases: []
  type: yml
  config:
    path: data/predicate.yml
```

其中对应的各yml、json、csv文件内容如下：

`person.json`中内容如下：

```json
{"name": "曹操", "id": "1"}
{"name": "刘备", "id": "2"}
{"name": "诸葛亮", "id": "3"}
{"name": "曹丕", "id": "4"}
{"name": "曹植", "id": "5"}
```

`place.csv`中内容如下：

```csv
name,id
洛阳,1
长安,2
新野,3
赤壁,4
宛城,5
```

`relation.yml`中内容如下：

```yaml
son:
  - 儿子
father:
  - 父亲
  - 爸爸
```

`predicatel.yml`中内容如下：

```yaml
is:
  - 是
  - 为
isnot:
  - 不是
  - 不为
```

### step2:定制模板规则

如编写`pattern.yml`文件如下：

```yaml
-
  name: father_son_relation
  patterns:
    -
      - [person, ~, son] # 规则为 [类型, id值, 词槽名称]
      - [relation, father, ~]
      - [predicate, is, null]
      - [person, ~, father]
    -
      - [ person, ~, father ]
      - [ predicate, is, null ]
      - [ person, ~, son ]
      - [ relation, father, ~ ]
-
  name: test
  patterns:
    -
      - [person, ~, person]
      - [ predicate, is, null ]
      - ['@person', ~, ttt]
```

在以上的模板规则中，对于每一个模板规则，需要指定其名字（name）及相应的模板（patterns）。
由于存在多个相近但不相同的模板对应同一种意图及词槽，所以这里的patterns是一个列表。
在以上的pattern.yml文件中，包含一个`'@person'`，这里可以映射到person这个类别所对应的所有别名，具体来说，可以对应到`["人物"]`列表中的所有词汇。

### step3:编写源代码及触发函数

示例如下：

```python
# -*- coding: utf-8 -*-
import os
import sys

project_path = os.path.abspath(os.path.join(__file__, "../.."))

print(project_path)

sys.path.insert(0, project_path)

from lightnlu.core import NER, Rule

if __name__ == '__main__':
    path = os.path.join(project_path, 'data/words.yml')
    ner = NER()
    ner.build_from_yml(path, base_dir=project_path)
    print(ner.entities)
    path = os.path.join(project_path, 'data/pattern.yml')
    rule = Rule()
    rule.build_from_yml(path)

    @rule.bind(rule_name="father_son_relation", act_name="test", domain="relation")
    def test(father: str, son: str):
        return {
            "father": father,
            "son": son
        }


    @rule.bind(rule_name="test", act_name="ppp", domain="hello_world")
    def ppp(person: str, ttt: str):
        return {
            "person": person,
            "ttt": ttt
        }

    print(rule.actors)

    text = "刘备和诸葛亮在新野旅游，途中遇上了曹操"
    domain = "relation"
    slots = ner.extract(text)
    print(slots)
    print(rule.match(slots, domain=domain))

    text = "曹丕的父亲是曹操"
    domain = "relation"
    slots = ner.extract(text)
    print(rule.match(slots, domain=domain))
    print(rule.match_and_act(slots, domain=domain))

    text = "曹操是曹丕的父亲"
    domain = "relation"
    slots = ner.extract(text)
    print(rule.match(slots, domain=domain))
    print(rule.match_and_act(slots, domain=domain))

    text = "曹操是个人物"
    domain = "hello_world"
    slots = ner.extract(text)
    print(rule.match(slots, domain=domain))
    print(rule.match_and_act(slots, domain=domain))
```

执行结果如下：

```text
defaultdict(<function default_type at 0x7f88a96b00d0>, {'曹操': [{'type': 'person', 'id': '1'}], '刘备': [{'type': 'person', 'id': '2'}], '诸葛亮': [{'type': 'person', 'id': '3'}], '曹丕': [{'type': 'person', 'id': '4'}], '曹植': [{'type': 'person', 'id': '5'}], '人物': [{'type': '@person', 'id': None}], '洛阳': [{'type': 'place', 'id': '1'}], '长安': [{'type': 'place', 'id': '2'}], '新野': [{'type': 'place', 'id': '3'}], '赤壁': [{'type': 'place', 'id': '4'}], '宛城': [{'type': 'place', 'id': '5'}], '地点': [{'type': '@place', 'id': None}], '位置': [{'type': '@place', 'id': None}], '城市': [{'type': '@place', 'id': None}], '区域': [{'type': '@place', 'id': None}], '电站': [{'type': 'ban_words', 'id': ''}], '正在站': [{'type': 'ban_words', 'id': ''}], '引流线': [{'type': 'ban_words', 'id': ''}], '子导线': [{'type': 'ban_words', 'id': ''}], '甲母线': [{'type': 'ban_words', 'id': ''}], '规则': [{'type': '@ban_words', 'id': None}], '所属厂站': [{'type': 'attr', 'id': 'attr_ST_ID'}], '所属电厂': [{'type': 'attr', 'id': 'attr_ST_ID'}], '属于哪个厂站': [{'type': 'attr', 'id': 'attr_ST_ID'}], '属于哪个电厂': [{'type': 'attr', 'id': 'attr_ST_ID'}], '电压等级': [{'type': 'attr', 'id': 'attr_VOLTAGE_TYPE'}], '儿子': [{'type': 'relation', 'id': 'son'}], '父亲': [{'type': 'relation', 'id': 'father'}], '爸爸': [{'type': 'relation', 'id': 'father'}], '是': [{'type': 'predicate', 'id': 'is'}], '为': [{'type': 'predicate', 'id': 'is'}], '不是': [{'type': 'predicate', 'id': 'isnot'}], '不为': [{'type': 'predicate', 'id': 'isnot'}]})
defaultdict(<class 'dict'>, {'father_son_relation': {'test': <function test at 0x7f88a967e940>}, 'test': {'ppp': <function ppp at 0x7f88a967e9d0>}})
[('刘备', {'type': 'person', 'id': '2'}, 0, 2), ('诸葛亮', {'type': 'person', 'id': '3'}, 3, 6), ('新野', {'type': 'place', 'id': '3'}, 7, 9), ('曹操', {'type': 'person', 'id': '1'}, 17, 19)]
[]
[{'name': 'father_son_relation', 'slots': {'son': '曹丕', 'father': '曹操'}}]
{'father_son_relation': {'test': {'father': '曹操', 'son': '曹丕'}}}
[{'name': 'father_son_relation', 'slots': {'father': '曹操', 'son': '曹丕'}}]
{'father_son_relation': {'test': {'father': '曹操', 'son': '曹丕'}}}
[{'name': 'test', 'slots': {'person': '曹操', 'ttt': '人物'}}]
{'test': {'ppp': {'person': '曹操', 'ttt': '人物'}}}
```

## 注意事项

1. csv文件和json文件中必须包含name和id两个属性或列。

## 更新日志

- v0.1.1 初始版本
- v0.2.0 增加域（domain）这一概念

## 参考

1. [keyue123/poemElasticDemo: 基于Elasticsearch的KBQA](https://github.com/keyue123/poemElasticDemo)
2. [liuhuanyong/QAonMilitaryKG: QAonMilitaryKG，QaSystem based on military knowledge graph that stores in mongodb which is different from the previous one, 基于mongodb存储的军事领域知识图谱问答项目，包括飞行器、太空装备等8大类，100余小类，共计5800项的军事武器知识库，该项目不使用图数据库进行存储，通过jieba进行问句解析，问句实体项识别，基于查询模板完成多类问题的查询，主要是提供一种工业界的问答思想demo。](https://github.com/liuhuanyong/QAonMilitaryKG)
