from pydoc import cli
from unittest import result
from flask import *
from flask_pymongo import PyMongo
from pymongo import MongoClient
import datetime
from flask import flash
from flask import url_for
from bson import json_util
from sqlalchemy import JSON
import gridfs
# from mongoengine_jsonencoder import MongoEngineJSONEncoder

app = Flask(__name__)
app.config['SECRET_KEY'] = "2019"
app.config["MONGO_URI"] = "mongodb://localhost:27017/survey"
mongo = PyMongo(app)
# app.json_encoder = MongoEngineJSONEncoder

# Mongo DB
# first time -> 회원가입
client = MongoClient('localhost', 27017)
members = mongo.db.members
db = client['survey']
# survey_result = mongo.db.survey_result

#홈화면
@app.route('/')
def home():
    # return render_template('one_time.html')
    return render_template('register.html')

#홈화면
@app.route('/login')
def home2():
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
        # resp = jsonify({'login':True})
        # value='1'
        member_id = members.find_one({'id': id})
        count = member_id['count']
        fcount = member_id['logincount']
        print(count)
        print(count % 7)
        if count == 0: 
            return render_template('daily.html', sid=id, cnt=count, fcnt=fcount)
        elif count % 7 == 0:
            return render_template('weekly.html', sid=id, cnt=count, fcnt=fcount)
        elif count % 7 != 0:
            return render_template('daily.html', sid=id, cnt=count, fcnt=fcount)

        # if count != 0:
        #     return render_template('daily.html', sid=id, cnt=count, fcnt=fcount)
        # elif count % 7 == 0:
        #     return render_template('weekly.html', sid=id, cnt=count, fcnt=fcount)

        # elif count %  7 == 0:
        #     return render_template('weekly.html', count)
        # return render_template('weekly.html', data=id)
        # return render_template('daily.html', sid=id)

#weekly
@app.route('/ajax2', methods=['GET', 'POST'])
def ajax2():
    data = request.get_json()
    # print(data)
    x_survey = list(data.values())[0]
    # print(x_survey)
    survey_result = mongo.db.get_collection(x_survey)
    # m = list(data.values())[1][5:14]
    # print(m)
    # if (m['value'] == '0'):
    # for cnt in m:
        # print(cnt['value'])
        # print(list(cnt.values())[1])
    #     if next((cnt for cnt in m if cnt['value'] ==''), None):
    #         cnt['value']=0
    #         print(cnt)
    # print(next((item for item in m if item['value']==''), None))
    # if next((item for item in m if item['value']==''), None):      
    del data['ID']
    survey_result.insert_one(data)
    data.pop('_id')
    return jsonify(result = "success", result2= data)

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
        fname = f.filename
        members.update_one({'id': s_id}, {'$inc': {'logincount': 1}})
        fs.put(contents, filename=fname)
        
    members.update_one({'id': s_id}, {'$inc': {'count': 1}})
    return 'file uploaded successfully'


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
        print(id)

        #회원가입시 컬렉션 생성
        mongo.db.create_collection(id) 
        # survey_result = mongo.db.get_collection(id)
        # survey_result.insert_one({'ID': 'S333'})

        if not (id and pwd and pwd2):
            return "모두 입력해주세요"
        elif pwd != pwd2:
            return "비밀번호를 확인해주세요."
        else:
            members.insert_one(post)
            # return "회원가입 완료"
            # flash("회원가입 완료")
            return render_template("one_time.html", data=id)

#one_time
@app.route('/ajax', methods=['GET', 'POST'])
def ajax():
    data = request.get_json()
    # print(data)
    # print(list(data.values())[1][4])
    m = list(data.values())[1][9]
    # print(m)
    # print(m['value'])
    if (m['value'] == '2'):
        # print(data['1_formData1'])
        dict = { 'name' : 'q9', 'value' : '0'}
        print(data['1_formData1'].insert(10, dict))
    #회원가입한 id와 같은 이름의 컬렉션 찾기
    #list()함수 이용해서 첫 번째 키 가져오기(id 값)
    x_survey = list(data.values())[0]
    survey_result = mongo.db.get_collection(x_survey)
    # #ID 요소 제거
    del data['ID']
    # #해당 컬렉션에 data upload
    survey_result.insert_one(data)
    #5월30일 테스트용으로 회원가입하지 않고, S000 계정 사용
    print(data)
    c = list(data.values())[0]
    if (c[0]['name'] == 'q1-1' and c[1]['name'] == 'q1-2' and c[2]['name'] == 'q1-3' and c[3]['name'] == 'q2' and c[4]['name'] == 'q3' and c[5]['name'] == 'q4' and c[6]['name'] == 'q5' and c[7]['name'] == 'q6' and c[8]['name'] == 'q7' and c[9]['name'] == 'q8' and c[10]['name'] == 'q9' and c[11]['name'] == 'q10'):
        print("모두 다 채움")
    #     print("다 채움")
    # print(c[0]['name']=='q1-1' and c[1]['name']=='q1-2')
    
    # print(c[0]['name'])
    # print(c[1]['name'])
    # print(c[2]['name'])
    # print(c[3]['name'])    
    # mem = mongo.db.S000
    # mem.insert_one(data)
    data.pop('_id')
    return jsonify(result = "success", result2= data)
    #return render_template('final.html')

@app.route('/final', methods=['GET', 'POST'])
def final():
    return render_template("final.html")

@app.route('/weekly', methods=['GET', 'POST'])
def weekly():
    return render_template('weekly.html', data=id)

@app.route('/pop.html', methods=['GET'])
def window_pop():
    return render_template("pop.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2019)
