from flask import Flask, render_template, request, redirect, url_for, jsonify,Blueprint
from datetime import datetime
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import numpy as np
import os
from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.0pi7g.mongodb.net/Cluster0?retryWrites=true&w=majority') # 클라이언트 설정시 작성
db = client.TEKKEN


# 학습시킨 binary classification model 불러오기 (출력층을 sigmoid 로 설정했기에, predict 하면 아웃풋이 0~1 로 나옴)
model = tf.keras.models.load_model('tekken/static/model/model.h5') 

bp = Blueprint("char_table", __name__, url_prefix="/char_table", static_folder="static", template_folder="templates")


@bp.route('/')
def home():
    all_char= list(db.char.find({},{'_id':False}))

    first = all_char[0:10]
    
    sec = all_char[10:20]
    
    thd = all_char[20:30]

    four = all_char[30:40]

    five = all_char[40:52]

    


    return render_template('characters.html', a_char = first, b_char = sec, c_char = thd, d_char = four , e_char = five)
