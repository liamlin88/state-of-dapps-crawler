import pandas as pd
import numpy as np
import json
import re
from functools import reduce

ORIGIN_PATH = "./map_data/origin_headers.csv"
TARGET_PATH = "./map_data/target_headers.csv"
MAP_PATH = "./map_data/map.csv"


def get_map(origin_path=ORIGIN_PATH, target_path=TARGET_PATH, map_path=MAP_PATH):
    o_df = pd.read_csv(origin_path)
    t_df = pd.read_csv(target_path)
    m_df = pd.read_csv(map_path)
    mapping = {}
    for a_map in m_df.values:
        mapping[o_df.values[a_map[0]-2][0]] = t_df.values[a_map[1]-2][0]
    return mapping


def headers_transformer(mapping):
    def tsfm(s):
        if s in mapping:
            return mapping[s]
        else:
            return s
    return tsfm


def rename(df):
    return df.rename(mapper=headers_transformer(get_map()), axis='columns')


def add_colnums(df, header_name, value=""):
    df[header_name] = np.full(len(df.index), value)
    return df


def to_NA(df):
    for i, row in df.iterrows():
        for col in df.columns:
            temp = df.at[i, col]
            if isinstance(temp, float):
                df.at[i, col] = 'NA'
    return df


def reviews_transform(df):
    df = add_colnums(df, "dapp_reviews", "NA")
    title_j = df.columns.get_loc('review_title')
    author_j = df.columns.get_loc('review_author')
    date_j = df.columns.get_loc('review_date')
    summary_j = df.columns.get_loc('review_summary')
    for i, row in df.iterrows():
        result = []
        authors = df.iat[i, author_j]
        if authors != 'NA':
            authors = authors.split(',')
            counter = len(authors)
            titles = df.iat[i, title_j].split(',')
            dates = re.findall(
                r'[a-zA-Z]{3} \d{1,2}, \d{4}', df.iat[i, date_j])
            summarys = df.iat[i, summary_j].split(',\n')
            for each in list(zip(*[authors, dates, titles, summarys])):
                result.append({
                    'author': each[0],
                    'dates': each[1],
                    'titles': each[2],
                    'summarys': each[3]
                })
        df.at[i, 'dapp_reviews'] = json.dumps(result)
    return df


def addresses_transform(df):
    df = add_colnums(df, "dapp_ethereum_mainnet_addresses", "NA")
    df = add_colnums(df, "dapp_ethereum_ropsten_addresses", "NA")
    for i, row in df.iterrows():
        l = re.findall(r'0x[0-9A-Za-z]*', df.at[i, 'mainnet_contracts'])
        if len(l) != 0:
            df.at[i,"dapp_ethereum_mainnet_addresses"] = reduce(lambda x, y: x+','+y, l)
        l = re.findall(r'0x[0-9A-Za-z]*', df.at[i, 'ropsten_contract'])
        if len(l) != 0:
            df.at[i,"dapp_ethereum_ropsten_addresses"] = reduce(lambda x, y: x+','+y, l)
    return df


if __name__ == "__main__":
    df = pd.read_csv("./17-06-2019-dapp.csv")
    df = rename(df)
    df = add_colnums(df, "dapp_bigicon_src")
    df = to_NA(df)
    df = reviews_transform(df)
    df = addresses_transform(df)
    df.to_csv('result.csv')
