#-*- coding: utf-8 -*-
from flask import Flask, render_template, request
import pandas as pd
from janome.tokenizer import Tokenizer
from Levenshtein import distance

app = Flask(__name__)

# csvファイルを読み込み
df = pd.read_csv('dic1.csv', header=None)

@app.route('/')
def index():
    return render_template('similarity.html')

@app.route('/similarity', methods=['POST'])
def similarity():
    # 入力された名前
    input_name = request.form['name']

    # 入力名の形態素解析
    tokenizer = Tokenizer()
    input_words = [token.surface for token in tokenizer.tokenize(input_name)]

    # Levenshtein距離を用いて類似度を計算し、それぞれの行の名前の類似度を表示
    similarities = {}
    for i in range(len(df)):
        # 辞書ファイル登録名の形態素解析
        words = [token.surface for token in tokenizer.tokenize(df.iloc[i, 0])]

        # 並び替えてLevenshtein距離を計算
        sorted_input_words = sorted(input_words)
        sorted_words = sorted(words)
        similarity = distance(''.join(sorted_input_words), ''.join(sorted_words))

        similarities[df.iloc[i, 0]] = similarity

    # Levebsgtain距離がどれくらい近いものまで出力するかを決めるmax_distanceを指定
    max_distance = 5
    similar_names = []
    #distance_values = []
    for name, similarity in similarities.items():
        if similarity <= max_distance:
            similar_names.append(name)
            #distance_values.append(similarity)

    #return render_template('similarity.html', input_name=input_name, similar_names=similar_names,distance_values=distance_values)
    return render_template('similarity.html', input_name=input_name, similar_names=similar_names)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)