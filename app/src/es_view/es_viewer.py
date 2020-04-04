import os
from graphviz import Graph
from pandas.core.frame import DataFrame

FONTNAME = 'ヒラギノ丸ゴ ProN W4.ttc'


def get_label(
    company: str,
    leader: str,
    pop: int,
    ES: float,
    color: str
) -> str:
    '''nodeのラベルを取得する

    ┌──────────────────────┐
    │       company        │
    ├──────────┬─────┬─────┤
    │  leader  │ pop │ ES  │
    └──────────┴─────┴─────┘

    Args:
        company (str): 担当名．カンパニー．
        leader (str): 責任者．
        pop (int): そのカンパニーにいる人数(正式にはESの回答者数)
        ES (int): Engagement Score.
        color (str): 色コード

    Returns:
        str

    '''
    if type(pop) is float and pop == pop:
        pop = int(pop)
    elif type(pop) is int:
        pop = pop
    else:
        pop = 0
    if ES != ES:
        ES = '不明'
    return f'''<<TABLE>
    ...  <TR>
    ...    <TD colspan="4">{company}</TD>
    ...  </TR>
    ...  <TR>
    ...    <TD colspan="2">{leader}</TD>
    ...    <TD colspan="1">{pop}名</TD>
    ...    <TD colspan="1" bgcolor="{color}">{ES}</TD>
    ...  </TR>
    ... </TABLE>>'''


class ESViewer:
    '''ESの描画クラス

    Args:
        es_data (DataFrame): ESのデータフレーム
        network ([list]): networkのリスト

    Examples:
        >>> from src.es_view import es_viewer
        >>> from src.es_view import read_esdata
        >>> es_data = read_esdata.get_es_data() # es_data
        >>> org_tree = read_esdata.get_org_tree()
        >>> org_tree_formatted = read_esdata.format_org_tree(org_tree)
        >>> network = read_esdata.get_network(org_tree_formatted) #network
        >>> viewer = es_viewer.ESViewer(es_data, network)
        >>> viewer.save('sample.png')

    '''

    def __init__(self, es_data: DataFrame, network: [list]):
        assert os.path.exists(f'/usr/share/fonts/truetype/{FONTNAME}')
        self.g = Graph(format='png')
        self.g.attr('graph', charset='UTF-8', fontname=FONTNAME)
        self.g.attr('node', shape='note', color='azure4', fontname=FONTNAME)
        self.g.attr('edge', color='azure4', fontname=FONTNAME)
        self.es_data = es_data
        self.network = network
        self.fit()

    def fit(self):
        '''nodeとedgeのセット
        '''
        node_ids = []
        for edge in self.network:
            self.g.edge(edge[0], edge[1])
            node_ids.extend(edge)
        for _, r in self.es_data.iterrows():
            self.g.node(
                r['id'],
                style='filled',
                fillcolor='gray100',
                fontcolor='black',
                label=get_label(r['属性名'], '不明', r['回答者数'],
                                r['ES'], r['color'])
            )

    def save(self, filename: str = None):
        '''画像を保存する

        Args:
            filename (str): ファイル名(拡張子は勝手にpngになる)

        '''
        filename = filename.split('.')[0]
        self.g.render(filename)
