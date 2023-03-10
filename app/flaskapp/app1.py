#-*- coding: utf-8 -*-
from flask import Flask, render_template, request
import pandas as pd
from janome.tokenizer import Tokenizer
from Levenshtein import distance

app = Flask(__name__)

# csv�t�@�C����ǂݍ���
df = pd.read_csv('dic1.csv', header=None)

@app.route('/')
def index():
    return render_template('similarity.html')

@app.route('/similarity', methods=['POST'])
def similarity():
    # ���͂��ꂽ���O
    input_name = request.form['name']

    # ���͖��̌`�ԑf���
    tokenizer = Tokenizer()
    input_words = [token.surface for token in tokenizer.tokenize(input_name)]

    # Levenshtein������p���ėގ��x���v�Z���A���ꂼ��̍s�̖��O�̗ގ��x��\��
    similarities = {}
    for i in range(len(df)):
        # �����t�@�C���o�^���̌`�ԑf���
        words = [token.surface for token in tokenizer.tokenize(df.iloc[i, 0])]

        # ���ёւ���Levenshtein�������v�Z
        sorted_input_words = sorted(input_words)
        sorted_words = sorted(words)
        similarity = distance(''.join(sorted_input_words), ''.join(sorted_words))

        similarities[df.iloc[i, 0]] = similarity

    # Levebsgtain�������ǂꂭ�炢�߂����̂܂ŏo�͂��邩�����߂�max_distance���w��
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