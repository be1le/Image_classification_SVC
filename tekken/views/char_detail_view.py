from flask import Flask, render_template, request, redirect, url_for, jsonify,Blueprint
from datetime import datetime
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import numpy as np
import os

# 학습시킨 binary classification model 불러오기 (출력층을 sigmoid 로 설정했기에, predict 하면 아웃풋이 0~1 로 나옴)
model = tf.keras.models.load_model('tekken/static/model/model.h5') 

bp = Blueprint("char_detail", __name__, url_prefix="/char_detail", static_folder="static", template_folder="templates")


@bp.route('/')
def home():
    return render_template('info.html')
