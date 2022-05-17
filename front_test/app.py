from flask import *
from flask_pymongo import PyMongo
from pymongo import MongoClient
import datetime
from flask import flash
from bson.json_util import dumps
from sqlalchemy import JSON
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = "2019"
app.config["MONGO_URI"] = "mongodb://localhost:27017/survey"
mongo = PyMongo(app)

# Mongo DB
client = MongoClient('localhost', 27017)
members = mongo.db.members
result = mongo.db.survey_result

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/a')
def survey1():
    return render_template('one_time.html')

@app.route('/b')
def survey2():
    value='1'
    return render_template('daily.html', count=value)

@app.route('/c')
def survey3():
    return render_template('weekly.html')

@app.route('/ajax', methods=['GET', 'POST'])
def ajax():
    data = request.get_json()
    print(data)
    return jsonify(result = "success", result2= data)

#회원가입
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        # return render_template("register_test.html")
        return render_template("register.html")
    else:
        name = request.form.get("name", type=str)
        id = request.form.get("id", type=str)
        pwd = request.form.get("pwd", type=str)
        pwd2 = request.form.get("pwd2", type=str)
        
        current_utc_time = round(datetime.datetime.utcnow().timestamp() * 1000)
        post = {
            "name": name,
            "id": id,
            "password": pwd,
            "register_date": current_utc_time,
            "logintime": "",
            "logincount": 0,
        }

        if not (id and pwd and pwd2):
            return "모두 입력해주세요"
        elif pwd != pwd2:
            return "비밀번호를 확인해주세요."
        else:
            members.insert_one(post)
            return render_template("login.html")

#로그인
@app.route('/user/login', methods = ['POST'])
def login():
    id = request.form['id']
    pwd = request.form['pwd']
    print(id)
    print(pwd)

    user = members.find_one({'id':id}, {'pwd':pwd})
    if user is None:
        return jsonify({'login':False})
    else:
        # flash("로그인 완료") #flash 안 뜸
        resp = jsonify({'login':True})
        value='1'
        return render_template('daily.html', count=value)