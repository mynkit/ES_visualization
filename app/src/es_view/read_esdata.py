import re
import pandas as pd
from pandas.core.frame import DataFrame


def get_es_data(es_data_path: str) -> DataFrame:
    '''ESのエクセルデータを読み込む

    Args:
        es_data_path (str): ESのエクセルデータのpath

    '''
    es_data = pd.read_csv(
        es_data_path,
        usecols=['属性記号', '属性No', '属性名', '回答者数', 'ES'],
        encoding='shift_jis'
    ).dropna(how='any')
    es_data['id'] = [f'{symbol}{num:03.0f}' for symbol,
                     num in zip(es_data['属性記号'], es_data['属性No'])]
    return es_data


def __assign_first_row_to_column(df: DataFrame) -> DataFrame:
    '''最初の行をカラムとして割り当てる

    Args:
        df (DataFrame): any dataframe.

    '''
    df_ = df.copy()
    columns = df_.iloc[0].tolist()
    df_ = df.iloc[1:]
    df_.columns = columns
    return df_


def __limit_columns(df: DataFrame) -> DataFrame:
    '''カラム名がNoneやNaNの場合はそのカラムを削除する

    Args:
        df (DataFrame): any dataframe.

    '''
    df_ = df.copy()
    df_ = df[[col for col in df_.columns if col is not None and col == col]]
    return df_


def get_org_tree(org_tree_path: str) -> DataFrame:
    '''組織図データを取得

    Args:
        org_tree_path (str): 組織図データのpath

    Returns:
        DataFrame

    '''
    org_tree = pd.read_excel(
        org_tree_path,
        sheet_name='★属性表示制限シート★',
        encoding='shift_jis',
        skiprows=7
    )
    org_tree = __assign_first_row_to_column(org_tree)
    org_tree = __limit_columns(org_tree)
    return org_tree


def format_org_tree(org_tree: DataFrame) -> DataFrame:
    '''組織図データを成形する

    Args:
        df (DataFrame): any dataframe.

    '''
    org_tree_ = org_tree.copy()
    org_tree_.columns = range(len(org_tree_.columns))
    org_tree_ = org_tree_.fillna(method='ffill')
    # nodeにすべきでない担当は除外する
    org_tree_ = org_tree_.applymap(
        lambda x: None if '該当なし' in x or 'E001' in x else x)
    org_tree_ = org_tree_.dropna(how='any')
    # 担当コードを取得
    org_tree_ = org_tree_.applymap(lambda x: re.findall(r'([A-Z]\d{3})', x)[0])
    return org_tree_


def get_network(org_tree_formatted: DataFrame) -> [list]:
    '''成形された組織図データから，network情報を取得する
    '''
    max_colnum = org_tree_formatted.columns.max()
    network = []
    for _, r in org_tree_formatted.iterrows():
        for i in range(max_colnum - 1):
            if [r[i], r[i + 1]] not in network:
                network.append([r[i], r[i + 1]])
    return network
