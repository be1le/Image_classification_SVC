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
    
    #첫번째 높은순위 
    counts = collections.Counter(top_list)

    a = counts.most_common(1)[0][0]
    a_number = counts.most_common(1)[0][1]

    top_len = len(top_list)
    a_per = "%.2f" % (a_number * 100 / top_len)
    
    # 2번쨰 높은 순위 
    b_list = top_list
    while a in b_list:
        
        b_list.remove(a)

    counts = collections.Counter(b_list)

    b = counts.most_common(1)[0][0]
    b_number = counts.most_common(1)[0][1]
    b_per = "%.2f" % (b_number * 100 / top_len)
    


    # 3번째 높은 순위 
    c_list = top_list
    while b in c_list:
        c_list.remove(b)

    counts = collections.Counter(c_list)

    c = counts.most_common(1)[0][0]
    c_number = counts.most_common(1)[0][1]
    c_per = "%.2f" % (c_number * 100 / top_len)

    print(c_per)
    print(b_per)
    print(a_per)
    print(a)
    print(b)
    print(c)



    return render_template('result.html', name = name, face = face ,all_result = all_result, first=a,sec=b,thd=c,first_num=a_per,sec_num=b_per,thd_num=c_per)
