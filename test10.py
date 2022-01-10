import pandas as pd
import os
import json
from pymongo import MongoClient
client = MongoClient('127.0.0.1:27017')
db = client['face_recognition']

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

print(checkIfIdExists(101))

# a = [{'Enrollment': 15, 'Name': ['rama'], 'Date': '2019-06-27', 'Time': '19:59:42'}, {'Enrollment': 15, 'Name': ['rama'], 'Date': '2019-06-27', 'Time': '19:59:55'}]
#
# df = pd.DataFrame(a)
# newdf = df.append({'Enrollment': 16, 'Name': ['me'], 'Date': '2019-06-27', 'Time': '19:59:42'}, ignore_index=True)
# print(newdf)

# res = json.loads(df.T.to_json()).values()
# print(list(res)[0])
# db.data.insert_one(list(res)[0])
# col_names = ['Enrollment', 'Name', 'Date', 'Time']
# studentDetailsFilePath = os.path.join(os.path.dirname(__file__), 'StudentDetails', 'StudentDetails.csv')
# if not os.path.isfile(studentDetailsFilePath):
#     pd_df = pd.DataFrame([{i:'' for i in col_names}])
#     print(pd_df)
#     pd_df.to_csv(studentDetailsFilePath, index=False)