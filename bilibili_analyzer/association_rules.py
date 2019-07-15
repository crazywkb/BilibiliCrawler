# import pyfpgrowth
from collections import defaultdict

import fp_growth_py3 as fpg
import pandas as pd


# filepath = './test_data/user_following_animation.json'
# data = pd.read_json(filepath, lines=True)
# data_list = list(data["value"].dropna())
# print(len(data_list))


def generate_frequent_items(minimum_support):
    frequent_itemsets = fpg.find_frequent_itemsets(data_list, minimum_support=0.07 * len(data_list),
                                                   include_support=True)
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
    print("--------------频繁项集------------------")
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


def transform_rules_to_df(raw_rules):
    rules = transform(raw_rules)
    rules.sort(key=lambda x: x[2], reverse=True)
    rules_a = [i[0] for i in rules]
    rules_b = [i[1] for i in rules]
    confidence = [i[2] for i in rules]
    rules_df = pd.DataFrame({"rules_a": rules_a, "rules_b": rules_b, "confidence": confidence})
    print("----------------关联规则-------------------")
    print(rules_df)
    print("----------------关联规则-------------------")
    return rules_df


def unfold_rules(rules_df):
    rules_df_temp = pd.DataFrame(columns=["rules_a", "rules_b", "confidence"])
    for index, row in rules_df.iterrows():
        if len(row["rules_b"]) > 1:
            rules_a = row["rules_a"]
            rules_b = row["rules_b"]
            confidence = row["confidence"]
            for i in rules_b:
                frozenset_i = set()
                frozenset_i.add(i)
                frozenset_i = frozenset(frozenset_i)
                rules_df_temp = rules_df_temp.append(
                    {"rules_a": rules_a, "rules_b": frozenset_i, "confidence": confidence},
                    ignore_index=True)
        else:
            rules_df_temp = rules_df_temp.append(
                {"rules_a": row["rules_a"], "rules_b": row["rules_b"], "confidence": row["confidence"]},
                ignore_index=True)

    return rules_df_temp


def count_repeat(rules_df):
    count = 0
    for index, row in rules_df.iterrows():
        if len(row["rules_b"]) > 1:
            count += 1
    print(count)


# minimum_support = 0.07
# minimum_confidence = 0.6
# patterns = generate_frequent_items(minimum_support)
# raw_rules = generate_rules(patterns, minimum_confidence)

# rules_df = transform_rules_to_df(raw_rules)
# rules_df.to_csv("rules.csv", index=False, header=False)

# rules_df = unfold_rules(rules_df)
# rules_df.to_csv("unfold_rules.csv", index=False, header=False)


def trans(raw_num):
    result = 1
    raw_num = raw_num[:-3]
    if raw_num.endswith("亿"):
        result = result * 10 ** 8
        raw_num = raw_num[:-1]
    elif raw_num.endswith("万"):
        result = result * 10 ** 4
        raw_num = raw_num[:-1]

    try:
        result = result * float(raw_num)
    except:
        result = 0

    return int(result)


def check_rules(rules_df, animation, animation_feature):
    temp_rules_df = pd.DataFrame(columns=["rules_a", "rules_b", "confidence"])
    for index, row in rules_df.iterrows():
        # 得到rules_a和rules_b
        rules_a = row["rules_a"]
        rules_a = set(rules_a)
        temp = set()
        for i in rules_a:
            i = int(i)
            temp.add(i)
        rules_a = temp
        rules_b = ''.join(row["rules_b"])
        rules_b = int(rules_b)

        if rules_b not in list(animation_feature["media_id"]):
            continue
        temp_rules_a_set = set()
        for i in rules_a:
            if i in list(animation_feature["media_id"]):
                temp_rules_a_set.add(i)
        if len(temp_rules_a_set) == 0:
            continue
        temp_rules_df = temp_rules_df.append(
            {"rules_a": temp_rules_a_set, "rules_b": rules_b, "confidence": row["confidence"]}, ignore_index=True)
    return temp_rules_df


def add_score(rules_df, rules_weight, animation, animation_feature):
    rules_df = check_rules(rules_df, animation, animation_feature)
    rules_df['score'] = 0

    max_follow = animation["follow"].max()
    max_play = animation["play"].max()
    score_list = []

    for index, row in rules_df.iterrows():
        score = 0
        rules_a = row["rules_a"]

        rules_b = row["rules_b"]

        # 计算confidence
        score += row["confidence"] * rules_weight["confidence"]

        # 计算评分
        temp = list(animation[animation["media_id"] == rules_b].score)
        temp = temp[0]
        score += temp * rules_weight["score"]

        # 计算播放量
        temp = list(animation[animation["media_id"] == rules_b].play)
        temp = temp[0]
        score += (temp / max_play) * rules_weight["play"]

        # 计算追番用户
        temp = list(animation[animation["media_id"] == rules_b].follow)
        temp = temp[0]
        score += (temp / max_follow) * rules_weight["follow"]

        # 计算声优
        voice_dict = animation_feature[animation_feature["media_id"] == rules_b].character_voice_list
        voice_dict = list(voice_dict)
        voice_dict = voice_dict[0]
        set_b_voice = set(voice_dict.values())
        set_a_voice = set()
        for i in rules_a:
            # 如果某条规则中的番剧不在animation里面，说明其已经失效
            if i not in animation_feature["media_id"]:
                continue
            voice_dict = animation_feature[animation_feature["media_id"] == i].character_voice_list
            voice_dict = list(voice_dict)
            voice_dict = voice_dict[0]
            voice_dict = set(voice_dict.values())
            set_a_voice.update(voice_dict)
        set_a_b_voice = set_a_voice.intersection(set_b_voice)
        voice_overlap_count = len(set_a_b_voice) / len(set_b_voice) * rules_weight["voice"]
        score += voice_overlap_count

        # 计算staff
        staff_dict = animation_feature[animation_feature["media_id"] == rules_b].character_staff_list
        staff_dict = list(staff_dict)
        staff_dict = staff_dict[0]
        set_b_staff = set(staff_dict.values())
        set_a_staff = set()
        for i in rules_a:
            # 如果某条规则中的番剧不在animation里面，说明其已经失效
            if i not in animation_feature["media_id"]:
                continue
            staff_dict = animation_feature[animation_feature["media_id"] == i].character_staff_list
            staff_dict = list(staff_dict)
            staff_dict = staff_dict[0]
            staff_dict = set(staff_dict.values())
            set_a_staff.update(staff_dict)
        set_a_b_staff = set_a_staff.intersection(set_b_staff)
        staff_overlap_count = len(set_a_b_staff) / len(set_b_staff) * rules_weight["staff"]
        score += staff_overlap_count

        # 该条关联规则的评分
        score_list.append(score)
    rules_df["score"] = score_list
    return rules_df

#
# # 读取animation 和 animation_feature
# animation = pd.read_json("./test_data/bilibili_crawler_animation.json", encoding="utf-8")
# animation[["follow", "play"]] = animation[["follow", "play"]].applymap(trans)
# animation_feature = pd.read_json("./test_data/bilibili_crawler_animation_feature.json",dtype={"character_voice_list": str})
# animation_feature[["tag_list", "character_voice_list", "character_staff_list"]] = animation_feature[["tag_list", "character_voice_list", "character_staff_list"]].applymap(json.loads)
#
# rules_weight = {"confidence": 0.5, "score": 0.1, "play": 0.1, "follow": 0.1, "voice": 0.1, "staff": 0.1}
# add_score(rules_df, rules_weight, animation, animation_feature)
# print(rules_df)
