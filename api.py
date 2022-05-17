import flask
import sqlite3
from waitress import serve

app = flask.Flask(__name__)

@app.route("/")
def index():
    with open("readme.md") as f:
        return f.read()

@app.route("/students",methods=['GET'])
def students():
    db = sqlite3.connect("people.db")
    cursor = db.cursor()
    cursor.execute("SELECT studentId, name, classId FROM students")
    data = list(cursor.fetchall())
    db.close()
    data2 = []
    for i in data:
        data2.append({"studentId":i[0], "name":i[1], "classId":i[2]})
    return flask.make_response({"students":tuple(data2)},200)

@app.route("/student_photo",methods=["GET"])
def student_photo():
    try:
        id = flask.request.headers['ID']
    except KeyError:
        return flask.make_response("ID not passed in request header",400)
    else:
        db = sqlite3.connect("people.db")
        cursor = db.cursor()
        cursor.execute("SELECT image FROM students WHERE studentId = (?)", tuple(id))
        photo = tuple(cursor.fetchall())
        db.close()
        return flask.make_response({"photo":photo},200)
    
        
    

@app.route("/teachers", methods=["GET"])
def teachers():
    db = sqlite3.connect("people.db")
    cursor = db.cursor()
    cursor.execute("SELECT teacherId, name FROM teachers")
    data = tuple(cursor.fetchall())
    db.close()
    data2 = []
    for i in data:
        data2.append({"teacherId":i[0], "name":i[1]})
    return flask.make_response({"teachers": data2},200)

@app.route("/teacher_photo",methods=["GET"])
def teacher_photo():
    pass

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=55555)