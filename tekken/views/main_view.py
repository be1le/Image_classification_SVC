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
model = tf.keras.models.load_model('tekken/static/model/model.h5',compile=False) 
bp = Blueprint("main", __name__, url_prefix="/", static_folder="static", template_folder="templates")

### 폴더안에 모든파일을 삭제한다 ###
def DeleteAllFiles(Path):
    if os.path.exists(Path):
        for file in os.scandir(Path):
            os.remove(file.path)


@bp.route('/')
def home():
    
    user = db.char.find_one({'name':'Jin'})

    return render_template('index.html', name = user['name'] , Winrate = user['Winrate'])




@bp.route('/fileupload', methods=['POST'])
def file_upload():
    file = request.files['file_give']
    # 해당 파일에서 확장자명만 추출
    extension = file.filename.split('.')[-1]

    filename = 'input'
    # 파일 저장 경로 설정 (파일은 서버 컴퓨터 자체에 저장됨)
    save_to = f'tekken/static/img/abc/{filename}.{extension}'
    # 파일 저장!
    file.save(save_to)

    return jsonify({'result':' 인식 주우웅 '})

@bp.route('/result')
def result():

    test_datagen = ImageDataGenerator(rescale = 1./255)
    test_dir = 'tekken/static/img'
    test_generator = test_datagen.flow_from_directory(
            test_dir,
            # target_size 는 학습할때 설정했던 사이즈와 일치해야 함
            target_size =(224, 224),
            color_mode ="rgb",
            shuffle = False,
            # test 셋의 경우, 굳이 클래스가 필요하지 않음
            # 학습할때는 꼭 binary 혹은 categorical 로 설정해줘야 함에 유의
            class_mode = None,
            batch_size = 1)
    pred = model.predict(test_generator)
    # 마지막으로 업로드한 사진에 대한 판별결과를 보여줌
    # 이 부분은 어떤 서비스를 만들고자 하는지에 따라서 얼마든지 달라질 수 있음

    for i in pred:
        ab = np.argmax(i)
        if ab == 6:
            result = ab
            print(ab)
        else:
            result = ab
            print(ab)


    #파일을 삭제
    DeleteAllFiles('tekken/static/img/abc')

    #결과값을 저장
    all_result = list(db.compared_face_result.find({},{'_id':False}))
    resultid = len(all_result) + 1

    #numpy.int64 타입은 저장이 불가해서 int 타입으로 변형
    face_result = int(result)
    doc = {'id': resultid , 'result': face_result }
    
    db.compared_face_result.insert_one(doc)
    
    return render_template('result.html', result=result)