import pyfpgrowth
import pandas as pd
import numpy as np
import json
import fp_growth_py3 as fpg
import matplotlib.pyplot as plt
import pylab as pl
from collections import defaultdict


filepath='./test_data/user_following_animation.json'
data=pd.read_json(filepath,lines=True)
data_list = list(data["value"].dropna())
print(len(data_list))

def generate_frequent_items(minimum_support) :
    frequent_itemsets = fpg.find_frequent_itemsets(data_list, minimum_support=0.07 * len(data_list), include_support=True)
    print(type(frequent_itemsets))  # print type
    result = []
    for itemset, support in frequent_itemsets:  # 将generator结果存入list
        result.append((itemset, support / len(data_list)))

    result_patterns = [i[0] for i in result]
    result_support = [i[1] for i in result]
    patterns_df = pd.DataFrame({"fluent_patterns": result_patterns, "support": result_support})
    patterns = {}
    for i in result:
        patterns[frozenset(sorted(i[0]))] = i[1]
    print("-------------挖掘频繁项集---------------")
    print(patterns_df)

    return patterns


def generate_rules(patterns, min_confidence):
    patterns_group = group_patterns_by_length(patterns)
    raw_rules = defaultdict(set)
    for length, pattern_list in patterns_group.items():
        if length == 1:
            continue
        for pattern, support in pattern_list:
            item_list = list(pattern)
            for window_size in range(1, length):
                for i in range(0, length - window_size):
                    for j in range(i + window_size, length):
                        base_set = frozenset(item_list[i:j])
                        predict_set = frozenset(pattern - base_set)
                        confidence = support / patterns.get(base_set)
                        if confidence > min_confidence:
                            raw_rules[base_set].add((predict_set, confidence))

                        base_set, predict_set = predict_set, base_set
                        confidence = support / patterns.get(base_set)
                        if confidence > min_confidence:
                            raw_rules[base_set].add((predict_set, confidence))
    return raw_rules

def group_patterns_by_length(patterns):
    result = defaultdict(list)
    for pattern, support in patterns.items():
        result[len(pattern)].append((pattern, support))
    return result

def transform(raw_rules):
    result = list()
    for base_set, predict_set_list in raw_rules.items():
        for predict_set, confidence in predict_set_list:
            result.append((base_set, predict_set, confidence))

    return result

def transform_rules_to_df(raw_rules) :
    rules = transform(raw_rules)
    rules.sort(key=lambda x: x[2], reverse=True)
    rules_a = [i[0] for i in rules]
    rules_b = [i[1] for i in rules]
    confidence = [i[2] for i in rules]
    rules_df = pd.DataFrame({"rules_a": rules_a, "rules_b": rules_b, "confidence": confidence})
    print(rules_df)
    return rules_df

def unfold_rules(rules_df) :
    for index, row in rules_df.iterrows():
        if len(row["rules_b"]) >1 :
            rules_a = row["rules_a"]
            rules_b = row["rules_b"]
            confidence = row["confidence"]
            rules_df.drop(index=index,inplace=True)
            for i in rules_b :
                rules_df = rules_df.append({"rules_a":rules_a, "rules_b":i, "confidence":confidence}, ignore_index=True)
    return rules_df


def count_repeat(rules_df):
    count = 0
    for index,row in rules_df.iterrows() :
        if len(row["rules_b"]) > 1:
            count +=1
    print(count)

minimum_support = 0.07
minimum_confidence = 0.6
patterns = generate_frequent_items(minimum_support)
raw_rules = generate_rules(patterns, minimum_confidence)

rules_df = transform_rules_to_df(raw_rules)
rules_df.to_csv("rules.csv", index=False, header=False)

rules_df = unfold_rules(rules_df)
rules_df.to_csv("unfold_rules.csv", index=False, header=False)

print(rules_df)

rules_weight = {"confidence":0.5, "score":0.1, "play":0.1, "follow":0.1, "voice":0.1, "staff":0.1}
def add_score(rules_weight) :
    rules_df['score'] = 0

    # 读取animation相关数据
    animation = pd.read_json("./test_data/bilibili_crawler_animation.csv", lines=True)
    animation_feature = pd.read_json("./test_data/bilibili_crawler_animation_feature.json", lines=True)

add_score(rules_weight)