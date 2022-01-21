from flask import Flask, render_template, Blueprint
from pymongo import MongoClient

client = MongoClient('')  # 클라이언트 설정시 작성
db = client.TEKKEN



bp = Blueprint("char_table", __name__, url_prefix="/char_table",static_folder="static", template_folder="templates")


@bp.route('/')
def home():
    all_char = list(db.char.find({}, {'_id': False}))

    first = all_char[0:10]
    sec = all_char[10:20]
    thd = all_char[20:30]
    four = all_char[30:40]
    five = all_char[40:52]

    return render_template('characters.html', a_char=first, b_char=sec, c_char=thd, d_char=four, e_char=five)
