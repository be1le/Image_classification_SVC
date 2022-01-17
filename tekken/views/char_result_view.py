from flask import Flask, render_template, request, redirect, url_for, jsonify,Blueprint
from datetime import datetime
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import numpy as np
import collections

from pymongo import MongoClient


client = MongoClient('mongodb+srv://test:sparta@cluster0.0pi7g.mongodb.net/Cluster0?retryWrites=true&w=majority') # 클라이언트 설정시 작성
db = client.TEKKEN

# 학습시킨 binary classification model 불러오기 (출력층을 sigmoid 로 설정했기에, predict 하면 아웃풋이 0~1 로 나옴)
model = tf.keras.models.load_model('tekken/static/model/model.h5') 

bp = Blueprint("char_result", __name__, url_prefix="/char_result", static_folder="static", template_folder="templates")


@bp.route('/<result>')
def home(result):
    
    char = db.char.find_one({'name': result})

    name = char['name']
    face = char['Face']
    result_list = list(db.compared_face_result.find({},{'_id':False}))

    all_result= len(result_list)

    top_list = []
    for i in result_list:
        name = i['result']
        top_list.append(name)

    counts = collections.Counter(top_list)

    rank = counts.most_common(51)

    all_rank = {}
    all_per = {}
    top_len = len(top_list)
    tr = 0
    while tr < 51:
        
        try:
            all_rank["rank{0}".format(tr)] = rank[tr][0]
            all_per["rank{0}".format(tr)] = "%.2f" % (rank[tr][1] * 100 / top_len)
            tr = tr+1
        except:
            break



    return render_template('result.html', name = name, face = face ,all_result = all_result, first=all_rank["rank0"],sec=all_rank["rank1"],thd=all_rank["rank2"],first_num=all_per["rank0"],sec_num=all_per["rank1"],thd_num=all_per["rank2"])
