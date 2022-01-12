from flask import Flask, render_template, request, redirect, url_for, jsonify,Blueprint
from datetime import datetime
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import numpy as np
import os

# 학습시킨 binary classification model 불러오기 (출력층을 sigmoid 로 설정했기에, predict 하면 아웃풋이 0~1 로 나옴)
model = tf.keras.models.load_model('tekken/static/model/model.h5') 

bp = Blueprint("main", __name__, url_prefix="/", static_folder="static", template_folder="templates")


@bp.route('/')
def home():
    return render_template('index.html')




@bp.route('/fileupload', methods=['POST'])
def file_upload():
    file = request.files['file_give']
    # 해당 파일에서 확장자명만 추출
    extension = file.filename.split('.')[-1]
    # 파일 이름이 중복되면 안되므로, 지금 시간을 해당 파일 이름으로 만들어서 중복이 되지 않게 함!
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'{mytime}'
    # 파일 저장 경로 설정 (파일은 서버 컴퓨터 자체에 저장됨)
    save_to = f'tekken/static/img/{filename}.{extension}'
    # 파일 저장!
    file.save(save_to)

    return jsonify({'result':'success'})

@bp.route('/result')
def result():
	# 모델은 불러와져 있으니, 사용자가 올린 데이터를 predict 함수에 넣어주면 됨
		# 이미지이기에, rescale 및 size 조정을 위해 ImageDataGenerator 활용 
    test_datagen = ImageDataGenerator(rescale = 1./255)
    test_dir = 'tekken/static/img'
    test_generator = test_datagen.flow_from_directory(
            test_dir,
            # target_size 는 학습할때 설정했던 사이즈와 일치해야 함
            target_size =(256, 256),
            color_mode ="rgb",
            shuffle = False,
            # test 셋의 경우, 굳이 클래스가 필요하지 않음
            # 학습할때는 꼭 binary 혹은 categorical 로 설정해줘야 함에 유의
            class_mode = None,
            batch_size = 1)
    pred = model.predict(test_generator)
    # 마지막으로 업로드한 사진에 대한 판별결과를 보여줌
    # 이 부분은 어떤 서비스를 만들고자 하는지에 따라서 얼마든지 달라질 수 있음
    # if pred[-1] > 0.5:
    #     result = ''
    # else:
    #     result = '고양이'
    return render_template('result.html', result=result)