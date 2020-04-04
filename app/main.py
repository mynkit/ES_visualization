#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from src.es_view import es_viewer
from src.es_view import read_esdata
import base64


ES_DATA_PATH = 'src/data/108792_score_data_株式会社エヌ・ティ・ティ・データ.csv'
ORG_TREE_PATH = 'src/data/200124井上_表示制限設定フォーマット.xls'


app = Flask(__name__)


@app.route('/')
def top():
    '''トップページ
    '''
    text = '属性表示制限エクセル(組織図)とESのcsvを選択してください'
    return render_template('index.html', img='', text=text)


@app.route('/upload_files', methods=['POST'])
def upload_files():
    '''ファイルのアップロード
    '''
    text = ''
    upload_files = request.files.getlist('upload_files')
    # ESデータと組織図エクセルのファイルがuploadされているかチェック
    for upload_file in upload_files:
        if type(upload_file.filename) is not str:
            continue
        if '.csv' in upload_file.filename:
            es_data = read_esdata.get_es_data(upload_file)
        if '.xls' in upload_file.filename or '.xlsx' in upload_file.filename:
            org_tree = read_esdata.get_org_tree(ORG_TREE_PATH)  # org_tree
            org_tree_formatted = read_esdata.format_org_tree(org_tree)
            network = read_esdata.get_network(org_tree_formatted)  # network
    if {'es_data', 'network'}.issubset(dir()):
        viewer = es_viewer.ESViewer(es_data, network)
        viewer.save('images/es_img.png')
        with open('images/es_img.png', mode='rb') as f:
            f = f.read()
        img = base64.b64encode(f).decode().replace("'", "")
    else:
        img = ''
        if 'es_data' not in dir():
            text += 'ES csv is required.'
        if 'network' not in dir():
            text += 'Organization Excel is required.'
    return render_template('index.html', img=img, text=text)


if __name__ == "__main__":
    app.run()
