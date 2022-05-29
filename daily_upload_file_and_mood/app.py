import collections
from dataclasses import field
from email import contentmanager
from fileinput import filename
from importlib.resources import contents
from unittest import result
from flask import *
from flask_pymongo import PyMongo
from pymongo import MongoClient
import datetime
from flask import flash
from flask import url_for
from werkzeug.datastructures import ImmutableDict
import io
import gridfs

app = Flask(__name__)
app.config['SECRET_KEY'] = "2019"
app.config["MONGO_URI"] = "mongodb://localhost:27017/survey"
mongo = PyMongo(app)

# Mongo DB
client = MongoClient('localhost', 27017)
members = mongo.db.members
fs_test = mongo.db.test
db = client['test']

@app.route('/')
def home():
    return render_template('login.html')

#회원가입
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
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
            "count": 0,
        }

        if not (id and pwd and pwd2):
            return "모두 입력해주세요"
        elif pwd != pwd2:
            return "비밀번호를 확인해주세요."
        else:
            members.insert_one(post)
            # return "회원가입 완료"
            # flash("회원가입 완료")
            return render_template("one_time.html")

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
        count = members.find_one({'id': "S000"})
        count = count['count']
        id = "S000"
        print(count)
        if count == 0:
            return render_template('daily.html', sid=id, cnt=count)
        elif count %  7 == 0:
            return render_template('weekly.html', count)

@app.route('/survey/day', methods=['POST'])
def post_survey(): 
    data = request.get_json()
    print(data)
    return render_template("login.html")

@app.route('/pop.html', methods=['GET'])
def window_pop():
    return render_template("pop.html")

# @app.route('/ajax', methods=['GET', 'POST'])
# def ajax():
#     # print(request.get_data())
#     # print(request.files.get('key').stream.read())
#     # print(request.files.keys())
#     # csv_file = request.files.get('file').stream.read().decode()
#     fr = request.files.get('file').read()
#     print(fr)
#     # print(csv_file)
#     # print("dsfdsafdsafdsf")
#     client = MongoClient('localhost', 27017)
#     db = client['test']
#     fs = gridfs.GridFS(db)
#     file = request.files.get('file').stream.read()
#     # print(type(csv_file))
#     # print(type(file))
#     post = {
#         # "data": csv_file,
#         "name": "S123"
#     }
#     # members.insert_one(post)
#     # x = members.find_one({"name": "S123"})
#     # print(x['data'])
#     # with open("file.csv", 'wb') as f:
#     #     contents = f.write(csv_file)
#     # print(contents)
#     # fs.put(contents, filename="file99")
#     return jsonify("s")

@app.route('/moody', methods=['POST'])
def moody():  
    # rd = request.get_data()
    # print(rd)
    data = request.files['data']
    print(data)
    st = data.read()
    l = st.decode()
    evl = eval(l)
    s_id = evl['sid']
    mood = evl['mood']
    print(mood)
    md = { "mood": mood }
    survey_coll = mongo.db.get_collection(s_id)
    survey_coll.insert_one(md)
    
    if 'filed' not in request.files:
        print("not")
        pass
    else:
        f = request.files['filed']
        print(f)
        contents = f.read()
        fs = gridfs.GridFS(db, s_id)
        fname = f.name
        fs.put(contents, filename=fname)
    return 'file uploaded successfully'

@app.route('/final', methods=['GET', 'POST'])
def final():
    return render_template("final.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2017)
