import re
import pandas as pd
from pandas.core.frame import DataFrame
import matplotlib.colors as cl


def get_es_data(es_data_path: str) -> DataFrame:
    '''ESのエクセルデータを読み込む

    Args:
        es_data_path (str): ESのエクセルデータのpath

    '''
    es_data = pd.read_csv(
        es_data_path,
        usecols=['属性記号', '属性No', '属性名', '回答者数', 'ES'],
        encoding='shift_jis'
    )
    es_data['id'] = [f'{symbol}{num:03.0f}' for symbol,
                     num in zip(es_data['属性記号'], es_data['属性No'])]
    es_data['ES'] = es_data['ES'].apply(lambda x: __format_ES(x))
    es_data['color'] = es_data['ES'].apply(
        lambda x: __calc_color(x))
    return es_data


def __format_ES(ES: str):
    '''ESのフォーマットがぐちゃぐちゃなので統一する

    Args:
        ES (str)

    '''
    if type(ES) is str and re.search(r'([0-9.]+)', ES):
        ES = re.findall(r'([0-9.]+)', ES)[0]
        return float(ES)
    else:
        return None


def __rgb_to_color_code(rgb: tuple) -> str:
    '''RGBを色コードに変換

    Args:
        rgb (tuple): RGB

    Returns
        str
        色コード

    '''
    R_val, G_val, B_val = rgb
    return cl.to_hex((R_val / 255, G_val / 255, B_val / 255, 1))


def __calc_color(ES: float):
    '''0-1スケールに圧縮された数値をRGBの16進数表記として返す

    Args:
        ES (float): ES
    Returns:
        str
        ex: #54b0c5

    Notes:
        モチベーションクラウドでの色付けは以下

        | ER | 定義 | RGB |
        | --- | --- | --- |
        | AAA | 67以上 | (225, 21, 13) |
        | AA | 61以上67未満 | (230, 157, 104) |
        | A | 58以上61未満 | (230, 157, 104) |
        | BBB | 55以上58未満 | (230, 190, 104) |
        | BB | 52以上55未満 | (230, 190, 104) |
        | B | 48以上52未満 | (230, 190, 104) |
        | CCC | 45以上48未満 | (156, 221, 220) |
        | CC |42以上45未満 | (156, 221, 220) |
        | C | 39以上42未満 | (156, 221, 220) |
        | DDD | 33以上39未満 | (104, 180, 221) |
        | DD | 33未満 | (104, 180, 221) |

    '''
    if type(ES) is not float:
        return __rgb_to_color_code((30, 30, 30))
    if ES >= 67:
        # AAA
        return __rgb_to_color_code((225, 21, 13))
    elif ES >= 61:
        # AA
        return __rgb_to_color_code((230, 157, 104))
    elif ES >= 58:
        # A
        return __rgb_to_color_code((230, 157, 104))
    elif ES >= 55:
        # BBB
        return __rgb_to_color_code((230, 190, 104))
    elif ES >= 52:
        # BB
        return __rgb_to_color_code((230, 190, 104))
    elif ES >= 48:
        # B
        return __rgb_to_color_code((230, 190, 104))
    elif ES >= 45:
        # CCC
        return __rgb_to_color_code((156, 221, 220))
    elif ES >= 42:
        # CC
        return __rgb_to_color_code((156, 221, 220))
    elif ES >= 39:
        # C
        return __rgb_to_color_code((156, 221, 220))
    elif ES >= 33:
        # DDD
        return __rgb_to_color_code((104, 180, 221))
    elif ES < 33:
        # DD
        return __rgb_to_color_code((104, 180, 221))


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
        lambda x: None if '該当なし' in x else x)
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
        for i in range(max_colnum):
            if [r[i], r[i + 1]] not in network:
                if 'E001' not in [r[i], r[i + 1]]:
                    network.append([r[i], r[i + 1]])
    return network
