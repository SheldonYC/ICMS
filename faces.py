import urllib
import numpy as np
import mysql.connector
import cv2
import pyttsx3
import pickle
from datetime import datetime
import sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import webbrowser

# library for sending email, all codes are commented out. Not gonna really send a email
# email tutorial used: https://www.learncodewithmike.com/2020/02/python-email.html
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import smtplib

# 1 Create database connection
myconn = mysql.connector.connect(host="localhost", user="root", passwd="KMD9584sspn@", database="facerecognition")
date = datetime.utcnow()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
cursor = myconn.cursor()

#2 Load recognize and read label from model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("train.yml")

labels = {"person_name": 1}
with open("labels.pickle", "rb") as f:
    labels = pickle.load(f)
    labels = {v: k for k, v in labels.items()}

# create text to speech
engine = pyttsx3.init()
rate = engine.getProperty("rate")
engine.setProperty("rate", 175)

# Define camera and detect face
face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

inLoop = True
# default value
student_name  = "JACK"
student_id = "1"
student_email = "u3569274@connect.hku.hk"

# 3 Open the camera and start face recognition
while (inLoop):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

    for (x, y, w, h) in faces:
        # print(x, w, y, h)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        # predict the id and confidence for faces
        id_, conf = recognizer.predict(roi_gray)

        # If the face is recognized
        if conf >= 60:
            # print(id_)
            # print(labels[id_])
            font = cv2.QT_FONT_NORMAL
            id = 0
            id += 1
            name = labels[id_]
            current_name = name
            color = (255, 0, 0)
            stroke = 2
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

            # Find the student's information in the database.
            select = "SELECT * FROM Student WHERE student_name='%s'" % (name)
            name = cursor.execute(select)
            result = cursor.fetchall()
            student_id, student_name, student_email = result[0][0], result[0][1], result[0][2]
            # print(result)
            data = "error"

            for x in result:
                data = x

            # If the student's information is not found in the database
            if data == "error":
                print("The student", current_name, "is NOT FOUND in the database.")

            # If the student's information is found in the database
            else:
                inLoop=False
                break
                # code in here makes no sense to me, why keep the cv2 GUI alive when we are told to impement
                # our original GUI
                
                # Implement useful functions here.
                # Check the course and classroom for the student.
                #     If the student has class room within one hour, the corresponding course materials
                #         will be presented in the GUI.
                #     if the student does not have class at the moment, the GUI presents a personal class 
                #         timetable for the student.

                
                # Update the data in database
                # ate =  "UPDATE Student SET login_date=%s WHERE student_name=%s"
                # val = (date, current_name)
                # cursor.execute(update, val)
                # update = "UPDATE Student SET login_time=%s WHERE student_name=%s"
                # val = (current_time, current_name)
                # cursor.execute(update, val)
                # myconn.commit()upd
                
                # hello = ("Hello ", current_name, "You did attendance today")
                # print(hello)
                # engine.say(hello)
                # # engine.runAndWait()


        # If the face is unrecognized
        else: 
            color = (255, 0, 0)
            stroke = 2
            font = cv2.QT_FONT_NORMAL
            cv2.putText(frame, "UNKNOWN", (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
            # hello = ("Your face is not recognized")
            # print(hello)
            # engine.say(hello)
            # engine.runAndWait()

    cv2.imshow('Attendance System', frame)
    k = cv2.waitKey(20) & 0xff
    if k == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()

# check all place that need insert db record, hyperlink, revert back to 1 hour(from 24)?

# GUI for database
# student_name  = "JACK"
# student_id = "1"
# student_email = "u3569274@connect.hku.hk"

# will not actually send a email, those functions are commented out
# It is becuase they will contain personal information if the code works
def sendEmail():
    # content = MIMEMultipart()
    # content["subject"] = "Next Class information"
    # content["from"] = student_email
    # content["to"] = student_email
    # content.attach(MIMEText(nextClassInfo))

    # with smtplib.SMTP(host="smtp.gmail.com", port="999") as smtp:
    #     try:
    #         smtp.ehlo()
    #         smtp.starttls()
    #         smtp.login(student_email, "password")
    #         smtp.send_message(content)
    #         print("Complete!")
    #     except Exception as e:
    #         print("Error message: ", e)
    messagebox.showinfo(title="Notification", message="Successfully sent email!")
    # insert record of send email
    sql = "INSERT INTO Action (action_id, student_id, action_name, datetime) VALUES (3, 1, 'Send Email', NOW())"
    cursor.execute(sql)
    myconn.commit()


def openNote(note_link):
    webbrowser.get('windows-default').open_new(note_link)

def viewCourse(nextClass):
    top = Toplevel()
    top.geometry("600x480")
    # print(nextClass)
    # class information
    for (class_id, course_id, course_name, class_type, classroom_address, zoom_link, note_link, start_datetime, supplementary, message, teacher_name) in nextClass:
        Label(top, text=course_id + " " +course_name, font=("Arial", 20)).grid(row=0, sticky=W)
        Label(top, text=str(class_id) + "th " + class_type, font=("Arial", 15)).grid(row=1, sticky=W, pady=(0, 10))
        Label(top, text="Teacher: " + teacher_name, font=("Arial", 15)).grid(row=2, sticky=W)
        Label(top, text="Teacher's message: " + message, font=("Arial", 15), wraplength=600, justify="left").grid(row=3, sticky=W, pady=(0, 10))
        Label(top, text="Venue: " + classroom_address, font=("Arial", 15)).grid(row=4, sticky=W)
        Label(top, text="Start at: " + start_datetime.strftime("%H:%M:%S"), font=("Arial", 15)).grid(row=5, sticky=W)
        zoom = Label(top, text="Zoom link: " + zoom_link, fg="blue", cursor="hand2", font=("Arial", 15, "underline"))
        zoom.bind('<Button-1>', lambda x: webbrowser.get('windows-default').open_new(zoom_link))
        zoom.grid(row=6, sticky=W)
        Button(top, text="Get today's note", command=lambda: openNote(note_link), font=("Arial", 15), bg= "orange").grid(row=7, pady=(15))
        Label(top, text="Supplementary materials: ", font=("Arial", 15)).grid(row=8, sticky=W)
        sup = Label(top, text=supplementary, fg="blue", cursor="hand2", font=("Arial", 15, "underline"))
        sup.bind('<Button-1>', lambda x: webbrowser.get('windows-default').open_new("www.google.com"))
        sup.grid(row=9, sticky=W)

    # button to send email
    Button(top, text="Send me email", command=sendEmail, bg="yellow", font=("Arial", 15)).grid(row=10, pady=(15, 0))

def viewTimetable(listOfClass):
    top1 = Toplevel()
    if (len(listOfClass) == 0):
        timetable = Label(top1, text="You do not have any class today!", fg="Red", font=("Arial", 15)).pack()
        timetable = Label(top1, text="Enjoy your day off!", font=("Arial", 15)).pack()
    # if student has some class for today, show all class and remaining time to next class
    else:
        Label(top1, text="Your timetable for today", font=("Arial", 20)).pack()

        timetable = ttk.Treeview(top1)
        timetable["columns"] = ("Start Time", "Duration", "Course", "Class Type", "Venue")
        timetable.column("#0", width=0, stretch=NO)
        timetable.column("Start Time", width=100, minwidth=55, anchor=W)
        timetable.column("Duration", width=100, minwidth=55, anchor=W)
        timetable.column("Course", width=100, minwidth=55, anchor=W)
        timetable.column("Class Type", width=100, minwidth=55, anchor=W)
        timetable.column("Venue", width=100, minwidth=55, anchor=W)
        timetable.heading("Start Time", text="Start Time")
        timetable.heading("Duration", text="Duration")
        timetable.heading("Course", text="Course")
        timetable.heading("Class Type", text="Class Type")
        timetable.heading("Venue", text="Venue")

        i = 0
        for (dt, dur, cid, type, add) in listOfClass:
            timetable.insert(parent='', index='end', iid=i, values=(dt.time(), str(dur*30)+" mins", cid, type, add))
            i = i + 1
    timetable.pack()

# judge which infomation to display, depending on time till next class
def viewClass():
    # view class
    sql = "INSERT INTO Action (action_id, student_id, action_name, datetime) VALUES (2, 1, 'View class', NOW())"
    cursor.execute(sql)
    myconn.commit()

    # select classes of today, if any
    sql = """
        SELECT start_datetime, duration, course_id, class_type, classroom_address FROM Class
        WHERE DATE(start_datetime) = CURDATE() AND
        Class.course_id IN (
            SELECT course_id FROM Enroll WHERE student_id = {})
        ORDER BY start_datetime ASC
    """.format(student_id)
    cursor.execute(sql)
    result = cursor.fetchall()
    # print(result)

    # if student has at least 1 class today
    if (len(result) != 0):
        # query the next class information, assume only 1 class in next hour
        sql = """
        SELECT class_id, Class.course_id, course_name, class_type, classroom_address, zoom_link, note_link, start_datetime,  supplementary_material, teacher_message, teacher_name FROM Class, Course
        WHERE Class.course_id =Course.course_id AND
        start_datetime > NOW() AND
        Class.course_id IN (
            SELECT course_id FROM Enroll WHERE student_id = {})
        ORDER BY start_datetime ASC LIMIT 1
        """.format(student_id)
        cursor.execute(sql)
        next_class = cursor.fetchall()

        # finished all today's classes and do not have any class in the future
        if(len(next_class) == 0):
            viewTimetable([])
            return

        # check if next class is within 1 hour
        if ((next_class[0][7] - datetime.now()).total_seconds()/3600 <= 1):
            viewCourse(next_class)
        else:
            viewTimetable(result)
    # student does not have any class today
    else:
        viewTimetable([])

def viewAction():
    top2 = Toplevel()
    Label(top2, text="Your action history", font=("Arial", 30)).pack()

    # INSERT VIEW action to db
    sql = "INSERT INTO Action (action_id, student_id, action_name, datetime) VALUES (4, 1, 'View action', NOW())"
    cursor.execute(sql)
    myconn.commit()

    login_time =[]
    #select lastest login time, 0 for login, 1 for logout
    sql = "SELECT A.datetime FROM Action A WHERE A.action_id = 0 AND A.student_id = {} ORDER BY A.datetime DESC LIMIT 1 OFFSET 1".format(student_id)
    cursor.execute(sql)
    result = cursor.fetchall()
    login_time.append(result[0][0])

    #select lastest logout time
    sql = "SELECT A.datetime FROM Action A WHERE A.action_id = 1 AND A.student_id = {} ORDER BY A.datetime DESC LIMIT 1".format(student_id)
    cursor.execute(sql)
    result = cursor.fetchall()
    login_time.append(result[0][0])
    
    # calc time stayed in system, in minutes
    difference = (login_time[1] - login_time[0]).total_seconds()/60
    Label(top2, text="Last time, you stayed in system for: " + str(round(difference)) + " minutes", font=("Arial", 15)).pack()
    # select all action record from student
    sql = "SELECT A.action_name, A.datetime FROM Action A WHERE A.student_id = {} ORDER BY A.datetime DESC".format(student_id)
    cursor.execute(sql)
    result = cursor.fetchall()

    #create table for action record
    a_table = ttk.Treeview(top2)
    a_table["columns"] = ("Date", "Time", "Action")
    a_table.column("#0", width=0, stretch=NO)
    a_table.column("Date", width=100, minwidth=55, anchor=W)
    a_table.column("Time", width=50, minwidth=55, anchor=W)
    a_table.column("Action", width=150, minwidth=80, anchor=W)
    a_table.heading("Date", text="Date", anchor=W)
    a_table.heading("Time", text="Time", anchor=W)
    a_table.heading("Action", text="Action", anchor=W)

    i = 0
    for (action, dt) in result:
        a_table.insert(parent='', index='end', iid=i, values=(dt.date(), dt.time(),action))
        i = i + 1
    a_table.pack()


root = Tk()
root.geometry("500x250")
root.title("ICMS")

# Home page of GUI
# Welcome message
welcome = Label(root, text="Welcome to ICMS!", font=("Arial", 30))
welcome2 = Label(root, text="Your best support to A grade", fg="grey", font=("Arial", 15))
# Show user information
info = Label(root, text="Hi " + student_name.capitalize() + ", you log in at " + (datetime.now().strftime("%H:%M:%S")), font=("Arial", 15))
# Insert login to db
sql = "INSERT INTO Action (action_id, student_id, action_name, datetime) VALUES (0, 1, 'Sign in', NOW())"
cursor.execute(sql)
myconn.commit()


# Button for viewing class
view_class = Button(root, text="View Your Class", command=viewClass)
# Button for viewing actions
view_action = Button(root, text="View Your Action", command=viewAction)

welcome.pack()
welcome2.pack(pady=(0, 20))
info.pack(pady=(0, 20))
view_class.pack(pady=(0, 20))
view_action.pack()

root.mainloop()
# insert  logout to db
sql = "INSERT INTO Action (action_id, student_id, action_name, datetime) VALUES (1, 1, 'Sign out', NOW())"
cursor.execute(sql)
myconn.commit()
