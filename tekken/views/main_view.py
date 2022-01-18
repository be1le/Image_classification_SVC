from flask import Flask, render_template, request, redirect, url_for, jsonify,Blueprint
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import numpy as np
import os
from pymongo import MongoClient
import certifi

tk = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.0pi7g.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=tk) # 클라이언트 설정시 작성
db = client.TEKKEN

model = tf.keras.models.load_model('tekken/static/model/model.h5',compile=False) 
bp = Blueprint("main", __name__, url_prefix="/", static_folder="static", template_folder="templates")

### 폴더안에 모든파일을 삭제한다 ###
def DeleteAllFiles(Path):
    if os.path.exists(Path):
        for file in os.scandir(Path):
            os.remove(file.path)


@bp.route('/')
def home():
    result= len(list(db.compared_face_result.find({},{'_id':False})))
    

    return render_template('main.html', all_result = result)


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
    try:
        test_datagen = ImageDataGenerator(rescale = 1./255)
        test_dir = 'tekken/static/img'
        image_vali_1 = os.path.isfile("tekken/static/img/abc/input.jpg")
        image_vali_2 = os.path.isfile("tekken/static/img/abc/input.jpeg")
        image_vali_3 = os.path.isfile("tekken/static/img/abc/input.png")
        if image_vali_1 == True or image_vali_2 == True or image_vali_3==True:
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
                if ab == 0:
                    result = 'Alisa'
                elif ab == 1:
                    result = 'Asuka'
                elif ab == 2:
                    result = 'Bryan'
                elif ab == 3:
                    result = 'DevilJin'
                elif ab == 4:
                    result = 'Dragunov'
                elif ab == 5:
                    result = 'Heihachi'
                elif ab == 6:
                    result = 'Hwoarang'
                elif ab == 7:
                    result = 'Katarina'
                elif ab == 8:
                    result = 'Kazuya'
                elif ab == 9:
                    result = 'King'
                elif ab == 10:
                    result = 'Leroy'
                elif ab == 11:
                    result = 'Lili'
                elif ab == 12:
                    result = 'Xiaoyu'
                elif ab == 13:
                    result = 'Paul'
                elif ab == 14:
                    result = 'Yoshimitsu'
                elif ab == 15:
                    result = 'Zafina'
                elif ab == 16:
                    result = 'Ganryu'
                elif ab == 17:
                    result = 'Gigas'
                elif ab == 18:
                    result = 'Geese'
                elif ab == 19:
                    result = 'Negan'
                elif ab == 20:
                    result = 'Noctis'
                elif ab == 21:
                    result = 'Nina'
                elif ab == 22:
                    result = 'Lars'
                elif ab == 23:
                    result = 'LuckyChole'
                elif ab == 24:
                    result = 'Leo'
                elif ab == 25:
                    result = 'Lei'
                elif ab == 26:
                    result = 'Law'
                elif ab == 27:
                    result = 'Lee'
                elif ab == 28:
                    result = 'Lidia'
                elif ab == 29:
                    result = 'MasterRaven'
                elif ab == 30:
                    result = 'Marduk'
                elif ab == 31:
                    result = 'Miguel'
                elif ab == 32:
                    result = 'Bob'
                elif ab == 33:
                    result = 'Shaheen'
                elif ab == 34:
                    result = 'Steve'
                elif ab == 35:
                    result = 'ArmorKing'
                elif ab == 36:
                    result = 'Akuma'
                elif ab == 37:
                    result = 'Anna'
                elif ab == 38:
                    result = 'Eddy'
                elif ab == 39:
                    result = 'Eliza'
                elif ab == 40:
                    result = 'Jack-7'
                elif ab == 41:
                    result = 'Josie'
                elif ab == 42:
                    result = 'Julia'
                elif ab == 43:
                    result = 'Kazumi'
                elif ab == 44:
                    result = 'Kunimitsu'
                elif ab == 45:
                    result = 'Kuma'
                elif ab == 46:
                    result = 'Claudio'
                elif ab == 47:
                    result = 'Fahkuram'
                elif ab == 48:
                    result = 'Feng'
                elif ab == 49:
                    result = 'Panda'
                elif ab == 50:
                    result = 'Jin'
                    
            print(ab)
            #파일을 삭제
            DeleteAllFiles('tekken/static/img/abc')

            #결과값을 저장
            all_result = list(db.compared_face_result.find({},{'_id':False}))
            resultid = len(all_result) + 1


            doc = {'id': resultid , 'result': result }
            
            db.compared_face_result.insert_one(doc)
        
            return redirect(url_for('char_result.home', result=result))
        else:
            return render_template('error.html')
    except:
        return render_template('error.html')