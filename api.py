import flask
import sqlite3
from waitress import serve
from flask import jsonify
import datetime, time
import pandas as pd

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
        data2.append({"classId":classid, "className":classname, "grade":grade, "formTeacherId":formteacherid})
    
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
        data2.append({"subjectId":subjectid, "name":name, "subjectCode":subjectcode})
    
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
        data2.append({"lessonId":lessonid, "subjectId":subjectid, "classId":classid, "teacherId":teacherid, "grade":grade, "semester":semester})
    return flask.make_response(jsonify(data2),200)
#table here

@app.route('/timetables')
def timetables():
    #no data
    db = sqlite3.connect("classes.db")
    cursor = db.cursor()
    data = cursor.execute("SELECT * FROM TIMETABLES").fetchall()
    db.close()
    data2 = []
    for row in data:
        lessonId, classId, dayOfWeek, startHour, startMinute, endHour, endMinute = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
        data2.append({"lessonId":lessonId, "classId":classId, "dayOfWeek":dayOfWeek, "startHour":startHour, "startMinute":startMinute, "endHour":endHour, "endMinute":endMinute})
    return flask.make_response(jsonify(data2),200)
    
    

@app.route('/lostandfound')
def lostandfound():
    db = sqlite3.connect("lostAndFound.db")
    cursor = db.cursor()
    data = cursor.execute("SELECT itemId, name, description, lastSeen, datePosted, found, creatorID FROM items").fetchall()
    db.close()
    data2 = []
    for row in data:
        itemId, name, description, lastSeen, datePosted, found, creatorID = row[0],row[1],row[2],row[3],row[4],row[5],row[6]
        data2.append({"itemId":itemId,"name":name, "description":description,"lastSeen":lastSeen,"datePosted":datePosted,"found":found,"creatorId":creatorID})
    return flask.make_response(jsonify(data2),200)

@app.route('/lostandfound_image')
def lostandfound_image():
    pass
    
@app.route('/books')
def books():
    db = sqlite3.connect("classes.db")
    cursor = db.cursor()
    data = cursor.execute("SELECT * FROM LESSONS").fetchall()
    db.close()
    data2 = []
    for row in data:
        bookId, bookTitle, bookAuthor, category, isbn, borrowed, borrowerId, borrowedOn, dueOn = row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]
        data2.append({"bookId":bookId, "bookTitle":bookTitle,"bookAuthor":bookAuthor, "category":category, "isbn":isbn, "borrowed":borrowed, "borrowerId":borrowerId, "borrowedOn":borrowedOn, "dueOn":dueOn})
    
    return flask.make_response(jsonify(books),200)
    
@app.route('/venues')
def venues():
    db = sqlite3.connect("facilities.db")
    cursor = db.cursor()
    data = cursor.execute("SELECT * FROM venues").fetchall()
    db.close()
    data2 = []
    for row in data:
        venueId, name, capacity, underMaintenance = row[0], row[1], row[2], row[3]
        data2.append({"venueId":venueId, "name":name, "capacity":capacity, "underMaintenance":underMaintenance})
    return flask.make_response(jsonify(data2),200)
    
@app.route('/bookings')
def bookings():
    db = sqlite3.connect("facilities.db")
    cursor = db.cursor()
    data = cursor.execute("SELECT * FROM BOOKINGS").fetchall()
    db.close()
    data2 = []
    for row in data:
        bookingId, bookerId, venueId, dateBooked, startHour, startMinute, endHour, endMinute = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]
        data2.append({"bookingId":bookingId, "bookerId":bookerId, "venueId":venueId, "dateBooked":dateBooked, "startHour":startHour, "startMinute":startMinute, "endHour":endHour, "endMinute":endMinute})
    return flask.make_response(jsonify(data2),200)

@app.route('/bookstore')
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
        
@app.route("/library_books")
def lib_books():
    db = sqlite3.connect("library.db")
    cursor = db.cursor()
    data = cursor.execute("SELECT * FROM books").fetchall()
    db.close()
    data2 = []
    for row in data:
        data2.append({"bookId":row[0], "bookTitle":row[1], "bookAuthor":row[2], "category":row[3], "isbn":row[4], "borrowed":row[5], "borrowerId":row[6], "borrowedOn":row[7], "dueOn":row[8]})
    return flask.make_response(jsonify(data2), 200)
    
@app.route("/borrow", methods=["POST"])
def borrow():
    try:
        bookId = int(flask.request.headers['bookId'])
    except KeyError:
        return flask.make_response("bookId not passed in request header",400)
        
    try:
        borrowerId = int(flask.request.headers['borrowerId'])
    except KeyError:
        return flask.make_response("borrowerId not passed in request header",400)
    
    db = sqlite3.connect("people.db")
    c = db.cursor()
    c.execute('''SELECT * FROM students WHERE studentId = (?)''', (borrowerId,))
    student = c.fetchone()
    
    if student == None:
        return flask.make_response("Student does not exist", 400)
    
    db.close()
    
    db = sqlite3.connect('library.db')
    c = db.cursor()
    c.execute('''SELECT * FROM books WHERE bookId = (?)''', (bookId,))
    book = c.fetchone()

    if book != None:
        if book[5] == 1:
            db.close()
            return flask.make_response("Book is already borrowed", 400)
        else: 
            c.execute(f'''UPDATE books SET borrowed = 1, borrowerId = {borrowerId} , borrowedOn = "{pd.Timestamp(datetime.datetime.now().strftime('%d/%m/%Y')).to_pydatetime()}" , dueOn = "{pd.Timestamp((datetime.datetime.now()+datetime.timedelta(days=14)).strftime('%d/%m/%Y')).to_pydatetime()}" WHERE bookId = {bookId}''')
            db.commit()
            db.close()
            return flask.make_response("Success!", 200)
    else:
        return flask.make_response("Book does not exist", 400)

@app.route("/return", methods=['POST'])
def return_book():
    db = sqlite3.connect('library.db')
    c = db.cursor()
    try:
        bookId = int(flask.request.headers['bookId'])
        c.execute('''SELECT * FROM books WHERE bookId = (?)''', (bookId,))
        book = c.fetchone()
        if book != None:
            if book[5] == 0:
                db.close()
                return flask.make_response("Book is not borrowed", 400)
            else:
                c.execute('''UPDATE books SET borrowed = 0, borrowerId = 0, borrowedOn = NULL, dueOn = NULL WHERE bookId = (?)''', (bookId,))
                db.commit()
                db.close()
                return flask.make_response("Success!", 200)
        else:
            return flask.make_response("Book does not exist", 400)
        
    except KeyError:
        db.close()
        return flask.make_response("bookId not passed in request header",400)
        

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=55555)