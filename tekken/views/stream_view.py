from flask import Flask, render_template, Blueprint

from pymongo import MongoClient

client = MongoClient('') # 클라이언트 설정시 작성
db = client.TEKKEN

bp = Blueprint("stream", __name__, url_prefix="/stream", static_folder="static", template_folder="templates")

@bp.route('/')
def home():

    return render_template('stream.html')
