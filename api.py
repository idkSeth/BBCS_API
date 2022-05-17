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
    data = tuple(cursor.fetchall())
    db.close()
    response = flask.make_response(flask.jsonify({"data": data}),200)
    return response

@app.route("/student_photo",methods=["GET"])
def student_photo():
    pass
    

@app.route("/teachers", methods=["GET"])
def teachers():
    db = sqlite3.connect("people.db")
    cursor = db.cursor()
    cursor.execute("SELECT teacherId, name FROM teachers")
    data = tuple(cursor.fetchall())
    db.close()
    response = flask.make_response(flask.jsonify({"data": data}),200)
    return response

@app.route("/teacher_photo",methods=["GET"])
def teacher_photo():
    pass

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=55555)