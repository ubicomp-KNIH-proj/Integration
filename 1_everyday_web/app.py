from unittest import result
from flask import *
from flask_pymongo import PyMongo
from pymongo import MongoClient
import datetime
from flask import flash
from flask import url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = "2019"
app.config["MONGO_URI"] = "mongodb://localhost:27017/survey"
mongo = PyMongo(app)

# Mongo DB
# first time -> 회원가입
client = MongoClient('localhost', 27017)
members = mongo.db.members

#홈화면
@app.route('/')
def home():
    return render_template('login.html')

#로그인
@app.route('/user/login', methods = ['POST'])
def login():
    id = request.form['id']
    pwd = request.form['pwd']
    # submit_count = request.form['submit_count']
    print(id)
    print(pwd)
    # print(submit_count)

    user = members.find_one({'id':id}, {'pwd':pwd})
    if user is None:
        return jsonify({'login':False})
    else:
        # flash("로그인 완료") #flash 안 뜸
        resp = jsonify({'login':True})
        value='1'
        # return render_template('daily.html', data=id)
        return render_template('weekly.html', data=id)

@app.route('/ajax', methods=['GET', 'POST'])
def ajax():
    data = request.get_json()
    print(data)
    x_survey = list(data.values())[0]
    survey_result = mongo.db.get_collection(x_survey)
    del data['ID']
    survey_result.insert_one(data)
    data.pop('_id')   
    return jsonify(result = "success", result2= data)

# 파일 ajax
# @app.route('/ajax', methods=['GET', 'POST'])
# def ajax():
#     print(request.files.get('key').stream.read())
#     print(request.files.get('file').stream.read())
#     return jsonify(result="success")
#     # return jsonify("s")

@app.route('/final', methods=['GET', 'POST'])
def final():
    return render_template("final.html")
   
