from logging import setLogRecordFactory
import string
from flask import *
from flask_pymongo import PyMongo
from pymongo import MongoClient
import datetime
from flask import flash
from flask import url_for
import gridfs

app = Flask(__name__)
app.config['SECRET_KEY'] = "2019"
app.config["MONGO_URI"] = "mongodb://localhost:27017/survey"
mongo = PyMongo(app)

# Mongo DB
# first time -> 회원가입
client = MongoClient('localhost', 27017)
members = mongo.db.members
db = client['survey']

#홈화면
@app.route('/')
def home():
    return render_template('login.html')

# 회원가입
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        id = request.form.get("id", type=str)
        pwd = request.form.get("pwd", type=str)
        pwd2 = request.form.get("pwd2", type=str)
        
        current_utc_time = round(datetime.datetime.utcnow().timestamp() * 1000)
        post = {
            "id": id,
            "password": pwd,
            "register_date": current_utc_time,
            "attach_count": 0,
            "submit_count": 0,
        }

        #회원가입시 컬렉션 생성
        mongo.db.create_collection(id) 

        if not (id and pwd and pwd2):
            return "모두 입력해주세요"
        elif pwd != pwd2:
            return "비밀번호를 확인해주세요."
        else:
            members.insert_one(post)
            return render_template("one_time.html", data=id)

@app.route('/ajax', methods=['GET', 'POST'])
def ajax():
    data = request.get_json()
    #회원가입한 id와 같은 이름의 컬렉션 찾기
    #list()함수 이용해서 첫 번째 키 가져오기(id 값)
    x_survey = list(data.values())[0]
    survey_result = mongo.db.get_collection(x_survey)
    # #ID 요소 제거
    del data['ID']
    # #해당 컬렉션에 data upload
    survey_result.insert_one(data)
    data.pop('_id')
    return jsonify(result = "success", result2= data)
    
#로그인
@app.route('/user/login', methods = ['POST'])
def login():
    id = request.form['id']
    pwd = request.form['pwd']

    user = members.find_one({'id':id}, {'pwd':pwd})
    if user is None:
        return "<h1>다시 로그인해주세요</h1>"
    else:
        member_id = members.find_one({'id': id})
        count = member_id['submit_count']
        fcount = member_id['attach_count']

        if count == 0: 
            return render_template('daily.html', sid=id, cnt=count, fcnt=fcount)
        elif count % 7 == 0:
            return render_template('weekly.html', sid=id, cnt=count, fcnt=fcount)
        elif count % 7 != 0:
            return render_template('daily.html', sid=id, cnt=count, fcnt=fcount)

# @app.route('/weekly', methods=['GET', 'POST'])
# def ajax2():
#     data = request.get_json()
#     print(data)
#     x_survey = list(data.values())[0]
#     survey_result = mongo.db.get_collection(x_survey)
#     del data['ID']
#     survey_result.insert_one(data)
#     return jsonify(result = "success", result2= data)

@app.route('/moody', methods=['POST'])
def moody():  
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
        fname = f.filename
        members.update_one({'id': s_id}, {'$inc': {'attach_count': 1}})
        fs.put(contents, filename=fname)
        
    members.update_one({'id': s_id}, {'$inc': {'submit_count': 1}})
    return render_template('weekly.html')

@app.route('/final', methods=['GET', 'POST'])
def final():
    return render_template("final.html")

# @app.route('/daily', methods=['GET', 'POST'])
# def daily():
#     print(ssid)
#     return render_template("daily.html", cnt=ssid)

@app.route('/weekly', methods=['GET', 'POST'])
def weekly():
    data = request.get_json()
    print(data)
    x_survey = list(data.values())[0]
    survey_result = mongo.db.get_collection(x_survey)
    del data['ID']
    survey_result.insert_one(data)
    data.pop('_id')
    member_id = members.find_one({'id': x_survey})
    count = member_id['submit_count']
    fcount = member_id['attach_count']

    # return 'file uploaded successfully'
    # return render_template('daily.html', sid=x_survey)

    return jsonify(render_template("daily.html", sid=x_survey, cnt=count, fcnt=fcount))

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2019)