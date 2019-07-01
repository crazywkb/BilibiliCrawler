import pyfpgrowth
import pandas as pd
import numpy as np
import json
import fp_growth_py3 as fpg
import matplotlib.pyplot as plt
import pylab as pl
from collections import defaultdict


filepath='D:/Machine learning/user_following_animation.json'
data=pd.read_json(filepath,lines=True)
data_list = list(data["value"].dropna())
print(data_list)

frequent_itemsets = fpg.find_frequent_itemsets(data_list, minimum_support=0.2 * len(data_list), include_support=True)
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
print(patterns_df)