import flask
import sqlite3
from waitress import serve
from flask import jsonify

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
    data = cursor.fetchall()
    db.close()
    data2 = []
    for row in data:
        data2.append({"studentId":row[0], "name":row[1], "classId":row[2]})
    return flask.make_response(jsonify(data2),200)

@app.route("/student_photo",methods=["GET"])
def student_photo():
    try:
        id = flask.request.headers['ID']
    except KeyError:
        return flask.make_response("ID not passed in request header",400)
    else:
        db = sqlite3.connect("people.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT image FROM students WHERE studentId={id}")
        photo = str((cursor.fetchall())[0])
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
    for row in data:
        data2.append({"teacherId":row[0], "name":row[1]})
    return flask.make_response(jsonify(data2),200)

@app.route("/teacher_photo",methods=["GET"])
def teacher_photo():
    pass

@app.route('/classes')
def classes():
    db = sqlite3.connect("classes.db")
    cursor = db.cursor()
    data = cursor.execute("SELECT * FROM CLASSES").fetchall()
    db.close()
    data2 = []
    for row in data:
        classid, classname, grade, formteacherid = row[0], row[1], row[2], row[3]
        data2.append({"classid":classid, "classname":classname, "grade":grade, "formteacherid":formteacherid})
    
    return flask.make_response(jsonify(data2),200)
    
@app.route('/subjects')
def subjects():
    db = sqlite3.connect("classes.db")
    cursor = db.cursor()
    data = cursor.execute("SELECT * FROM SUBJECTS").fetchall()
    db.close()
    data2 = []
    for row in data:
        subjectid, name, subjectcode = row[0], row[1], row[2]
        data2.append({"subjectid":subjectid, "name":name, "subjectcode":subjectcode})
    
    return flask.make_response(jsonify(data2), 200)

@app.route('/lessons')
def lessons():
    db = sqlite3.connect("classes.db")
    cursor = db.cursor()
    data = cursor.execute("SELECT * FROM LESSONS").fetchall()
    db.close()
    data2 = []
    for row in data:
        lessonid, subjectid, classid, teacherid, grade, semester = row[0], row[1], row[2], row[3], row[4], row[5]
        data2.append({"lessonid":lessonid, "classid":classid, "teacerid":teacherid, "grade":grade, "semester":semester})
    return flask.make_response(jsonify(data2),200)
#table here

@app.route('/timetables')
def timetables():
    #no data
    db = sqlite3.connect("classes.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM TIMETABLES").fetchall()
    db.close()
    timetable = []
    for row in cursor:
        lessonId, classId, dayOfWeek, startHour, startMinute, endHour, endMinute = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
        timetable.append({"lessonId":lessonId, "classId":classId, "dayOfWeek":dayOfWeek, "startHour":startHour, "startMinute":startMinute, "endHour":endHour, "endMinute":endMinute})
    return flask.make_response(jsonify(timetable),200)
    
    

@app.route('/lostandfound')
def lostandfound():
    db = sqlite3.connect("lostAndFound.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM lostitems").fetchall()
    db.close()
    items = []
    for row in cursor:
        itemId, name, description, image, lastSeen, datePosted, found, creatorID = row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]
        items.append({"itemId":itemId,"name":name, "description":description,"image":image,"lastSeen":lastSeen,"datePosted":datePosted,"found":found,"creatorID":creatorID})
    return flask.make_response(jsonify(items),200)
    
@app.route('/books')
def books():
    db = sqlite3.connect("classes.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM LESSONS").fetchall()
    db.close()
    books = []
    for row in cursor:
        bookId, bookTitle, bookAuthor, category, isbn, borrowed, borrowerId, borrowedOn, dueOn = row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]
        books.append({"bookId":bookId, "bookTitle":bookTitle,"bookAuthor":bookAuthor, "category":category, "isbn":isbn, "borrowed":borrowed, "borrowerId":borrowerId, "borrowedOn":borrowedOn, "dueOn":dueOn})
    
    return flask.make_response(jsonify(books),200)
    
@app.route('/venues')
def venues():
    db = sqlite3.connect("facilities.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM venues").fetchall()
    db.close()
    venues = []
    for row in cursor:
        venueId, name, capacity, underMaintenance = row[0], row[1], row[2], row[3]
        venues.append({"venueId":venueId, "name":name, "capacity":capacity, "underMaintenance":underMaintenance})
    return flask.make_response(jsonify(venues),200)
    
@app.route('/bookings')
def bookings():
    db = sqlite3.connect("facilities.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM BOOKINGS").fetchall()
    db.close()
    bookings = []
    for row in cursor:
        bookingId, bookerId, venueId, dateBooked, startHour, startMinute, endHour, endMinute = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]
        bookings.append({"bookingId":bookingId, "bookerId":bookerId, "venueId":venueId, "dateBooked":dateBooked, "startHour":startHour, "startMinute":startMinute, "endHour":endHour, "endMinute":endMinute})
    return flask.make_response(jsonify(bookings),200)

@app.route('/items')
def items():
    db = sqlite3.connect("bookstore.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ITEMS").fetchall()
    db.close()
    items = []
    for row in cursor:
        itemId, name, price, image, description, stock = row[0], row[1], row[2], row[3], row[4]
        items.append({"itemId":itemId, "name":name, "price":price, "image":image, "description":description,"stock":stock})
    return flask.make_response(jsonify(items),200)

@app.route('/users')
def users():
    db = sqlite3.connect("todos.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ITEMS").fetchall()
    db.close()
    users = []
    for row in cursor:
        userId, username, password, image = row[0], row[1], row[2], row[3]
        users.append({"userId":userId, "username":username,"password":password,"image":image})
    return flask.make_response(jsonify(users), 200)
    
@app.route('/todos')
def todos():
    db = sqlite3.connect("todos.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ITEMS").fetchall()
    db.close()
    todos = []
    for row in cursor:
        todoId, title, userId, category, dueDate, isDone = row[0], row[1], row[2], row[3], row[4]
        todos.append({"todoId":todoId, "title":title, "userId":userId, "category":category, "dueDate":dueDate, "isDone":isDone})
    return flask.make_response(jsonify(todos),200)
        

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=55555)