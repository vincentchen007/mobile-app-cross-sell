import collections

import pandas as pd
from efficient_apriori import apriori
import json


def load_csv_to_list(file_name):
    df = pd.read_csv(file_name)
    df['ORDER_MENU_ITEM_ARRAY'].replace('\n', '', regex=True, inplace=True)
    orders = [json.loads(n) for n in df['ORDER_MENU_ITEM_ARRAY']]
    return list(orders)


def main():
    orders = load_csv_to_list("user_ordered_dishes_2022_11_10.csv")
    print("Order count: " + str(len(orders)))
    item_sets, rules = apriori(orders, min_support=0.001, min_confidence=0.2)
    d = collections.defaultdict(list)
    for r in rules:
        # X -> Y
        if len(r.rhs) == 1 and len(r.rhs) == 1:
            # d[",".join([i for i in r.lhs])].append([r.rhs, r.support, r.confidence, r.lift, r.conviction])
            d[r.lhs[0]].append([r.rhs[0], r.support, r.confidence, r.lift, r.conviction])
    sorted_d = collections.defaultdict(list)
    rules_count = 0
    for key, value in d.items():
        # rank by the support * confidence
        sorted_value = sorted(value, key=lambda x: x[1] * x[2], reverse=True)
        sorted_d[key] = sorted_value
        rules_count += len(sorted_value)
    print(rules_count)
    with open('rules.json', 'w') as fp:
        json.dump(sorted_d, fp)


main()
