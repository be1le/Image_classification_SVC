from flask import Flask, render_template, request, jsonify, Blueprint
from pymongo import MongoClient
import itertools

client = MongoClient('') # 클라이언트 설정시 작성
db = client.TEKKEN


bp = Blueprint("char_detail", __name__, url_prefix="/char_detail",static_folder="static", template_folder="templates")


@bp.route('/<name>')
def home(name):

    char = db.char.find_one({'name': name}, {'_id': False})
    name = char['name']
    Rank = char['Rank']
    Winrate = char['Winrate']
    Omega = char['Omega']
    style = char['stlye']
    story = char['story']
    enemy = dict(itertools.islice(char.items(), 3, 54))
    ab = enemy.keys()
    vs_enemy = []
    for i in ab:
        if i != name:
            vs_enemy.append(i)
    result_list = list(db.compared_face_result.find({}, {'_id': False}))
    all_result = len(result_list)

    return render_template('info.html', name=name, Rank=Rank, Winrate=Winrate, Omega=Omega, story=story, style=style, all_result=all_result, enemy=vs_enemy)


@bp.route('/search_vs', methods=["POST"]) 
def search(): 
    char = request.form['char_give'] 
    vs_char = request.form['vs_char_give'] 
    char = db.char.find_one({'name': char }) 
    vs = char[vs_char] 
    vs_per = "{:.2f}".format(vs) 
    

    return jsonify({'result': vs_per})