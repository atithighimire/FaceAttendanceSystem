import tkinter as tk
from tkinter import *
import cv2
import csv
import os
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import json
from main_gui import BkgrFrame
#from report import view_attendance, view_details
# import tkinter.ttk as ttk
# import tkinter.font as font

from pymongo import MongoClient
mongo_client = MongoClient('127.0.0.1:27017')
db = mongo_client['face_recognition']

#####Window is our Main frame of system
window = tk.Tk()
window.title("Face Attendance System")
IMAGE_PATH = 'main.jpg'
WIDTH, HEIGHT = 1300, 690
window.geometry('{}x{}'.format(WIDTH, HEIGHT))
bkgframe = BkgrFrame(window, IMAGE_PATH, WIDTH, HEIGHT)
bkgframe.pack()
#window.geometry('1280x720')
#window.configure(background='RoyalBlue1')


##For clear textbox
def clear():
    txt.delete(first=0, last=22)


def clear1():
    txt2.delete(first=0, last=22)


def del_sc1():
    sc1.destroy()


def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry('300x100')
    sc1.iconbitmap('AMS.ico')
    sc1.title('Warning!!')
    sc1.configure(background='snow')
    Label(sc1, text='Enrollment & Name required!!!', fg='red', bg='snow', font=('times', 16, ' bold ')).pack()
    Button(sc1, text='OK', command=del_sc1, fg="white", bg="SpringGreen3", width=9, height=1, activebackground="SpringGreen4",
           font=('times', 15, ' bold ')).place(x=90, y=50)


def del_sc3():
    sc3.destroy()


def err_recognize():
    global sc3
    sc3 = tk.Tk()
    sc3.geometry('300x100')
    sc3.iconbitmap('AMS.ico')
    sc3.title('Not Recognized!!')
    sc3.configure(background='snow')
    Label(sc3, text='Error in filling attendance!!!', fg='red', bg='snow',
          font=('times', 16, 'bold')).pack()
    Button(sc3, text='OK', command=del_sc3, fg='white', bg='SpringGreen3',
           width=9, height=1, activebackground='SpringGreen4',
           font=('times', 15, 'bold')).place(x=90, y=50)


##Error screen2
def del_sc2():
    sc2.destroy()


def err_screen1():
    global sc2
    sc2 = tk.Tk()
    sc2.geometry('300x100')
    sc2.iconbitmap('AMS.ico')
    sc2.title('Warning!!')
    sc2.configure(background='snow')
    Label(sc2, text='Please enter your subject name!!!', fg='red', bg='snow', font=('times', 16, ' bold ')).pack()
    Button(sc2, text='OK', command=del_sc2, fg="white", bg="SpringGreen3", width=9, height=1, activebackground="SpringGreen4",
           font=('times', 15, ' bold ')).place(x=90, y=50)

def checkIfIdExists(ID):
    studentDetailsCSV = "E:\Attendace_management_system\StudentDetails\StudentDetails.csv"
    if os.path.isfile(studentDetailsCSV):
        df = pd.read_csv(studentDetailsCSV)
        ids = df.index[(df["Enrollment"] == ID)]
        if list(ids):
            return True
        else:
            return False
    else:
        return False

###For take images for datasets
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def take_img():
    l1 = txt.get()
    l2 = txt2.get()

    if not l1 or not RepresentsInt(l1):
        err_screen()

    elif not l2 or not l2.isalpha():
        err_screen()

    elif checkIfIdExists(int(l1)):
        err_screen()
    else:
        try:
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            Enrollment = txt.get()
            Name = txt2.get()

            sampleNum = 0
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # faces = detector.detectMultiScale(gray, 1.3, 5)

                faces = detector.detectMultiScale(
                    gray,
                    scaleFactor=1.3,
                    minNeighbors=5,
                    minSize=(30, 30),
                    # flags=cv2.cv.CV_HAAR_SCALE_IMAGE
                    flags=cv2.CASCADE_SCALE_IMAGE
                )

                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    cv2.imwrite("TrainingImage/ " + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    cv2.imshow('Frame', img)
                # wait for 100 miliseconds
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # break if the sample number is more than 200
                elif sampleNum >= 200:
                    break
            cam.release()
            cv2.destroyAllWindows()
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

            studentDetailsFilePath = os.path.join(os.path.dirname(__file__), 'StudentDetails', 'StudentDetails.csv')
            student_df = pd.DataFrame([{'Enrollment': Enrollment, 'Name': Name, 'Date': Date, 'Time': Time}])
            if not os.path.isfile(studentDetailsFilePath):
                student_df.to_csv('StudentDetails\StudentDetails.csv', index=False)
            else:
                student_df.to_csv(studentDetailsFilePath, mode='a', header=False, index=False)

            # insert student details to db
            student_details_insertion_data = list(json.loads(student_df.T.to_json()).values())
            db.student_details.insert_many(student_details_insertion_data)

            res = "Images is saved for Enrollment no : " + Enrollment + "  and Name : " + Name
            Notification.configure(text=res, bg="SpringGreen3", fg="white", width=45, height=1, font=('times', 18, 'bold'))
            Notification.place(x=660, y=450)

        except FileExistsError as F:
            f = 'Student Data already exists'
            Notification.configure(text=f, bg="firebrick1", fg="white", width=30, height=1, font=('times', 18, 'bold'))
            Notification.place(x=660, y=5)


###for choose subject and fill attendance
def subjectchoose():
    def Fillattendances():
        sub = tx.get()
        now = time.time()  ###For calculate seconds of video
        future = now + 15
        face_counter = 0
        face_matches_threshold = 20
        confidence_threshold = 45
        if time.time() < future:
            if sub == '':
                err_screen1()
            else:
                recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
                try:
                    recognizer.read("TrainingImageLabel\Trainner.yml")
                except:
                    e = 'Model not found,Please train model'
                    Notifica.configure(text=e, bg="firebrick1", fg="white", width=30, height=1, font=('times', 18, 'bold'))
                    Notification.place(x=660, y=5)
                harcascadePath = "haarcascade_frontalface_default.xml"
                faceCascade = cv2.CascadeClassifier(harcascadePath)
                df = pd.read_csv("StudentDetails\StudentDetails.csv")
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ['Subject', 'Enrollment', 'Name', 'Date', 'Time']
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    ret, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(gray, 1.3, 7)
                    for (x, y, w, h) in faces:
                        global Id
                        roi_gray = gray[y:y + h, x:x + w]
                        Id, conf = recognizer.predict(roi_gray)
                        print(conf)
                        if (conf < confidence_threshold):
                            # print(conf)
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                            # print(Id)
                            # print(df.loc[df['Enrollment'] == Id]['Name'])
                            aa_ini = df[df['Enrollment'] == Id]
                            aa = aa_ini.iloc[0]['Name']
                            global tt
                            tt = str(Id) + "-" + aa
                            En = '15624031' + str(Id)
                            attendance.loc[len(attendance)] = [Subject, Id, aa, date, timeStamp]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)
                            face_counter += 1

                        else:
                            Id = 'Unknown'
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)

                    ## change the face_counter value if you need to check the matches for more faces and get accurate recognition
                    if time.time() > future or face_counter >= face_matches_threshold:
                        break

                    attendance = attendance.drop_duplicates(['Enrollment'], keep='first')

                    cv2.imshow('Filling attendance..', im)
                    key = cv2.waitKey(30) & 0xff
                    if key == 27:
                        break

                if face_counter >= face_matches_threshold:

                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    Hour, Minute, Second = timeStamp.split(":")

                    ####Creatting csv of attendance
                    attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
                    # fileName = "Attendance/" + Subject + "_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
                    fileName =  os.path.join("E:\Attendace_management_system\Attendance", "attendance.csv")
                    if not os.path.isfile(fileName):
                        attendance.to_csv(fileName, index=False)
                    else:
                        attendance.to_csv(fileName, mode='a', header=False, index=False)

                    #### code to insert to db ###
                    insertion_data = list(json.loads(attendance.T.to_json()).values())
                    # print("*"*50, insertion_data[0])
                    db.attendance.insert_many(insertion_data)
                    #### code to insert to db ###

                    M = 'Attendance filled Successfully'
                else:
                    M = 'Attendance failed'

                Notifica.configure(text=M, bg="SpringGreen3", fg="white", width=30, height=1, font=('times', 18, 'bold'))
                Notifica.place(x=660, y=5)

                cam.release()
                cv2.destroyAllWindows()

                import csv
                import tkinter
                root = tkinter.Tk()

                if face_counter >= face_matches_threshold:
                    root.title("Attendance of " + Subject)
                    root.configure(background='azure')
                    cs = os.path.join('E:\Attendace_management_system\Attendance', "attendance.csv")
                    with open(cs, newline="") as file:
                        reader = csv.reader(file)
                        r = 0

                        for col in reader:
                            c = 0
                            for row in col:
                                # i've added some styling
                                label = tkinter.Label(root, width=8, height=1, fg="black", font=('times', 15, ' bold '),
                                                      bg="Seagreen2", text=row, relief=tkinter.RIDGE)
                                label.grid(row=r, column=c)
                                c += 1
                            r += 1
                    root.mainloop()
                    print(attendance)
                else:
                    err_recognize()
                    print("Could not get attendance")

    ###windo is frame for subject chooser
    windo = tk.Tk()
    windo.iconbitmap('AMS.ico')
    windo.title("Enter subject name")
    windo.geometry('580x320')
    windo.configure(background='snow')

    Notifica = tk.Label(windo, text="Attendance filled Successfully", bg="SpringGreen3", fg="white", width=33,
                        height=2, font=('times', 15, 'bold'))


    sub = tk.Label(windo, text="Enter Subject", width=15, height=2, fg="light sea green", bg="snow",
                   font=('times', 20, ' bold '))
    sub.place(x=6, y=35)

    tx = tk.Entry(windo, width=20, bg="lavender", fg="black", font=('times', 23, ' bold '))
    tx.place(x=50, y=110)

    fill_a = tk.Button(windo, text="Fill Attendance", fg="white", command=Fillattendances, bg="light sea green", width=38,
                       height=2,
                       activebackground="DodgerBlue2", font=('times', 15, ' bold '))
    fill_a.place(x=50, y=185)
    windo.mainloop()


def admin_panel():
    #win = tk.Tk()
    win = Toplevel(window)
    win.iconbitmap('AMS.ico')
    win.title("LogIn")
    img_path = 'register.jpg'
    width, height = 880, 500
    win.geometry('{}x{}'.format(width, height))
    admin_frame = BkgrFrame(win, img_path, width, height)
    admin_frame.pack()

    #win.geometry('880x420')
    #win.configure(background='snow')

    def log_in():
        username = un_entr.get()
        password = pw_entr.get()

        if username == 'admin':
            if password == 'admin':
                win.destroy()
                import csv
                import tkinter
                # root = tkinter.Tk()
                # root.geometry('880x500')
                # root.title("Student Details")
                # root.configure(background='azure')
                #
                # cs = os.path.join('E:\Attendace_management_system', 'StudentDetails', "StudentDetails.csv")
                # with open(cs, newline="") as file:
                #     reader = csv.reader(file)
                #     r = 0
                #
                #     for col in reader:
                #         c = 0
                #         for row in col:
                #             # i've added some styling
                #             label = tkinter.Label(root, width=8, height=1, fg="black", font=('times', 15, ' bold '),
                #                                   bg="Seagreen2", text=row, relief=tkinter.RIDGE)
                #             label.grid(row=r, column=c)
                #             c += 1
                #         r += 1
                # root.mainloop()

                root = tkinter.Tk()
                root.geometry('600x400')
                root.title("Attendance Details")
                root.configure(background='azure')

                cs2 = os.path.join('E:\Attendace_management_system', 'Attendance', 'attendance.csv')
                with open(cs2, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(root, width=8, height=1, fg="black", font=('times', 15, ' bold '),
                                                  bg="Seagreen2", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()


                # att_details_button = tkinter.Button(root, text="Attendance Details", command=view_attendance(), fg="black", width=7, height=2,
                #                                     bg="SeaGreen2", activebackground="DodgerBlue2",
                #                                     font=('times', 15, ' bold '))
                # att_details_button.place(x=310, y=360)
                #
                # std_details_button = tkinter.Button(root, text="Student Details", command=view_details(), fg="black",
                #                                     width=7, height=2,
                #                                     bg="SeaGreen2", activebackground="DodgerBlue2",
                #                                     font=('times', 15, ' bold '))
                # std_details_button.place(x=400, y=360)


                """cs = 'E:\Attendace_management_system\StudentDetails\StudentDetails.csv'

                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(root, width=8, height=1, fg="black", font=('times', 15, ' bold '),
                                                  bg="SeaGreen2", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1"""
                # root.mainloop()
            else:
                valid = 'Incorrect Username or Password!'
                Nt.configure(text=valid, bg="firebrick1", fg="snow", width=30, height=1,font=('times', 19, 'bold'))
                Nt.place(x=452, y=0)

        else:
            valid = 'Incorrect Username or Password!'
            Nt.configure(text=valid, bg="firebrick1", fg="snow", width=30, height=1, font=('times', 19, 'bold'))
            Nt.place(x=452, y=0)

    Nt = tk.Label(win, text="Attendance filled Successfully!", bg="SpringGreen3", fg="snow", width=27,
                  height=1, font=('times', 19, 'bold'))
    # Nt.place(x=120, y=350)

    un = tk.Label(win, text="Enter username", width=15, height=1, fg="DodgerBlue2", bg="white",
                  font=('times', 15, ' bold '))
    un.place(x=30, y=210)

    pw = tk.Label(win, text="Enter password", width=15, height=1, fg="DodgerBlue2", bg="white",
                  font=('times', 15, ' bold '))
    pw.place(x=30, y=320)

    def c00():
        un_entr.delete(first=0, last=22)

    un_entr = tk.Entry(win, width=15, bg="LightCyan3", fg="navy", font=('times', 23, ' bold '))
    un_entr.place(x=40, y=250)

    def c11():
        pw_entr.delete(first=0, last=22)

    pw_entr = tk.Entry(win, width=15, show="*", bg="LightCyan3", fg="navy", font=('times', 23, ' bold '))
    pw_entr.place(x=40, y=360)

    c0 = tk.Button(win, text="Clear", command=c00, fg="snow", bg="navy", width=7, height=1,
                   activebackground="RoyalBlue1", font=('times', 15, ' bold '))
    c0.place(x=310, y=250)

    c1 = tk.Button(win, text="Clear", command=c11, fg="snow", bg="navy", width=7, height=1,
                   activebackground="RoyalBlue1", font=('times', 15, ' bold '))
    c1.place(x=310, y=360)

    Login = tk.Button(win, text="LogIn", fg="snow", bg="SeaGreen2", width=10,
                      height=1,
                      activebackground="PaleGreen2", command=log_in, font=('times', 18, ' bold '))
    Login.place(x=132, y=443)
    win.mainloop()


###For train the model
def trainimg():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    global detector
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    try:
        global faces, Id
        faces, Id = getImagesAndLabels("TrainingImage")
    except Exception as e:
        l = 'please make "TrainingImage" folder & put Images'
        Notification.configure(text=l, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)

    recognizer.train(faces, np.array(Id))
    try:
        recognizer.save("TrainingImageLabel\Trainner.yml")
    except Exception as e:
        q = 'Please make "TrainingImageLabel" folder'
        Notification.configure(text=q, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)

    res = "Model Trained"  # +",".join(str(f) for f in Id)
    Notification.configure(text=res, bg="SpringGreen3", width=30, font=('times', 18, 'bold'))
    Notification.place(x=650, y=450)


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faceSamples = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces = detector.detectMultiScale(imageNp)
        # If a face is there then append that in the list as well as Id of it
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y + h, x:x + w])
            Ids.append(Id)
    return faceSamples, Ids


window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.iconbitmap('AMS.ico')


def on_closing():
    from tkinter import messagebox
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()


window.protocol("WM_DELETE_WINDOW", on_closing)

Notification = tk.Label(window, text=" Enrollment and name  is blank", bg="SpringGreen2", fg="white", width=30,
                        height=1, font=('times', 18, 'bold'))

lbl = tk.Label(window, text="Enter Enrollment", width=15, height=1, fg="Black", font=('times', 15, ' bold '))
lbl.place(x=660, y=200)

txt = tk.Entry(window, validate="key", width=20, bg="white", fg="black", font=('times', 25, ' bold '))
txt.place(x=660, y=240)

lbl2 = tk.Label(window, text="Enter Name", width=15, fg="Black", height=1, font=('times', 15, ' bold '))
lbl2.place(x=660, y=300)


txt2 = tk.Entry(window, validate="key", width=20, bg="white", fg="black", font=('times', 25, ' bold '))
txt2.place(x=660, y=340)
txt2 = tk.Entry(window, width=20, bg="white", fg="black", font=('times', 25, ' bold '))
txt2.place(x=660, y=340)

clearButton = tk.Button(window, text="Clear", command=clear, fg="snow", bg="orange", width=10, height=1,
                        activebackground="goldenrod", font=('times new roman', 15, ' bold '))
clearButton.place(x=1030, y=240)

clearButton1 = tk.Button(window, text="Clear", command=clear1, fg="snow", bg="orange", width=10, height=1,
                         activebackground="goldenrod", font=('times', 15, ' bold '))
clearButton1.place(x=1030, y=340)

takeImg = tk.Button(window, text="Take Images", command=take_img, fg="DodgerBlue2", bg="snow", width=10, height=1,
                    activebackground="DodgerBlue4", font=('times', 15, ' bold '))
takeImg.place(x=660, y=500)

trainImg = tk.Button(window, text="Train Images", fg="DodgerBlue2", command=trainimg, bg="snow", width=10, height=1,
                     activebackground="DodgerBlue4", font=('times', 15, ' bold '))
trainImg.place(x=850, y=500)

FA = tk.Button(window, text="Automatic Attendance", fg="DodgerBlue2", command=subjectchoose, bg="snow", width=15, height=1,
               activebackground="DodgerBlue4", font=('times', 15, ' bold '))
FA.place(x=1050, y=500)

AP = tk.Button(window, text="Admin LogIn", command=admin_panel, fg="DodgerBlue2", bg="snow", width=48, height=2,
               activebackground="DodgerBlue4", font=('times', 15, ' bold '))
AP.place(x=660, y=600)

window.mainloop()
