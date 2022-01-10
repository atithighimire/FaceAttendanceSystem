import tkinter
import csv
import os
import subprocess
import sys


def view_details():
    root1 = tkinter.Tk()
    root1.geometry('880x500')
    root1.title("Student Details")
    root1.configure(background='azure')

    cs = 'E:\Attendace_management_system\StudentDetails\StudentDetails.csv'

    with open(cs, newline="") as file:
        reader = csv.reader(file)
        r = 0

        for col in reader:
            c = 0
            for row in col:
                # i've added some styling
                label = tkinter.Label(root1, width=8, height=1, fg="black", font=('times', 15, ' bold '),
                                      bg="SeaGreen2", text=row, relief=tkinter.RIDGE)
                label.grid(row=r, column=c)
                c += 1
            r += 1

    root1.mainloop()


import subprocess
subprocess.Popen('explorer "C:\temp"')
def view_attendance():
    root2 = tkinter.Tk()
    root2.geometry('880x500')
    root2.title("Student Details")
    root2.configure(background='azure')
    import subprocess
    import sys
    path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
    sys.path.append(path)
    subprocess.Popen(r'explorer /select,"E:\Attendace_management_system\Attendance"')
        # r'explorer /select,"E:\Attendace_management_system\Attendance\-------Check atttendance-------"')

    """cs = os.path.join('E:\Attendace_management_system', 'Attendance',
                     Subject + "_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv")
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
            r += 1"""

    root2.mainloop()

