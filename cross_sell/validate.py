import collections
import json
import pandas as pd
import datetime


def load_rules(file_name):
    with open(file_name, 'r') as f:
        dic = json.load(f)
    f.close()
    return dic


def predict_top_n(rules_dict, current_atc_item, top_n=3):
    if current_atc_item not in rules_dict:
        return []
    top_n_list = []
    for i in range(len(rules_dict[current_atc_item])):
        if i < top_n:
            top_n_list.append(rules_dict[current_atc_item][i][0])
    return top_n_list


def predict_top_n_by_list(rules_dict, current_atc_item, current_atc_item_list, top_n=4):
    # X1, X2, X3
    # X3 to get recommendation
    # remove X1, X2 from recommendation
    if current_atc_item not in rules_dict:
        return []
    top_n_list = []
    for i in range(len(rules_dict[current_atc_item])):
        if rules_dict[current_atc_item][i][0] not in current_atc_item_list:
            top_n_list.append(rules_dict[current_atc_item][i][0])
    if len(top_n_list) > top_n:
        return top_n_list[:top_n]
    return top_n_list


def load_atc_table(file_name):
    dic = collections.defaultdict(list)
    df = pd.read_csv(file_name, sep=",", header=0)
    # TO_TIMESTAMP((EVENTTIMESTAMP::BIGINT)/1000),TRANSACTION_ID,USER_ID,RESTAURANT_ID,RESTAURANT_NAME,MENU_ITEM_ID
    for idx, row in df.iterrows():
        time_stamp = datetime.datetime.strptime(row["TIMESTAMP"], '%Y-%m-%d %H:%M:%S.%f')
        dic[row["TRANSACTION_ID"]].append([row["MENU_ITEM_ID"], time_stamp])
    return dic


def main():
    rules_dict = load_rules("rules.json")
    atc_table = load_atc_table("atc_info_after_11_10.csv")
    not_int_dict = 0.
    result_list = []
    for key, value in atc_table.items():
        # for loop the transaction
        sorted_atc_list = sorted(value, key=lambda x: x[1])
        for i in range(len(sorted_atc_list) - 1):
            current_atc_item = sorted_atc_list[i][0]
            next_atc_item = sorted_atc_list[i + 1][0]
            current_atc_item_list = [i[0] for i in sorted_atc_list[:i + 1]]
            if current_atc_item not in rules_dict:
                not_int_dict += 1
            else:
                # top_n_list = predict_top_n(rules_dict, current_atc_item)
                top_n_list = predict_top_n_by_list(rules_dict, current_atc_item, current_atc_item_list)
                if next_atc_item in top_n_list:
                    result_list.append(1.)
                else:
                    result_list.append(0.)
    print(not_int_dict)
    print(len(result_list))
    print(sum(result_list))
    print(sum(result_list) / len(result_list))
    print(not_int_dict / len(result_list))


main()
