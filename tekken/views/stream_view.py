from flask import Flask, render_template, Blueprint
from datetime import datetime
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
from pymongo import MongoClient
import numpy as np
import os


client = MongoClient('mongodb+srv://test:sparta@cluster0.0pi7g.mongodb.net/Cluster0?retryWrites=true&w=majority') # 클라이언트 설정시 작성
db = client.TEKKEN

# 학습시킨 binary classification model 불러오기 (출력층을 sigmoid 로 설정했기에, predict 하면 아웃풋이 0~1 로 나옴)


bp = Blueprint("stream", __name__, url_prefix="/stream", static_folder="static", template_folder="templates")


@bp.route('/')
def home():


    return render_template('stream.html')
