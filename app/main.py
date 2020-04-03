#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from src.es_view import es_viewer
from src.es_view import read_esdata
import base64


ES_DATA_PATH = 'src/data/108792_score_data_株式会社エヌ・ティ・ティ・データ.csv'
ORG_TREE_PATH = 'src/data/200124井上_表示制限設定フォーマット.xls'


app = Flask(__name__)


def save_es_img():
    '''ESを組織図に落とし込んだ画像を保存する
    '''
    es_data = read_esdata.get_es_data(ES_DATA_PATH)  # es_data
    org_tree = read_esdata.get_org_tree(ORG_TREE_PATH)  # org_tree
    org_tree_formatted = read_esdata.format_org_tree(org_tree)
    network = read_esdata.get_network(org_tree_formatted)  # network
    viewer = es_viewer.ESViewer(es_data, network)
    viewer.save('images/es_img.png')


@app.route('/')
def hello():
    '''ES_DATA_PATHとORG_TREE_PATHから読みこんだ情報を画像として表示
    '''
    save_es_img()
    with open('images/es_img.png', mode='rb') as f:
        f = f.read()
        img = base64.b64encode(f).decode().replace("'", "")
    return render_template('index.html', img=img)


if __name__ == "__main__":
    app.run()
