import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt
import time

import cv2
import base64

cred = credentials.Certificate("./esp32-cam-46d27-firebase-adminsdk-2pon8-5ac2bf0802.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://esp32-cam-46d27-default-rtdb.asia-southeast1.firebasedatabase.app'
})

ref = db.reference("/esp32-cam")

firebase_dict = ref.get()

PUSH_CHARS = "-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz"

def get_timestamp_from_id(id):
    timestr = id[0:8]
    timestamp = 0
    for idx, ch in enumerate(timestr):
        timestamp = timestamp * 64 + PUSH_CHARS.index(ch)
    return timestamp/1000

# def readb64(uri):
#    encoded_data = uri.split(',')[1]
#    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
#    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#    return img


def readb64(uri):
    encoded_data = uri.split(',')[1]
    imgdata = base64.b64decode(encoded_data)
    print(imgdata)
    message = imgdata.decode('ascii')
    filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
            f.write(message)

    img = cv2.imread(filename)
    cv2.imread(img)


# print(list)
timestamps = []

for key in firebase_dict:
    timestamp = get_timestamp_from_id(key)
    timestamps.append(timestamp)

    photo64 = firebase_dict[key]["photo"]

    img = readb64(firebase_dict[key]["photo"])
    
    cv2.imshow("plant-pot",img)
    cv2.waitKey(0)
    # print(list[key])


dates=[dt.datetime.fromtimestamp(ts) for ts in timestamps]
values=np.ones(len(dates))
plt.subplots_adjust(bottom=0.2)
plt.xticks( rotation=25 )
ax=plt.gca()
xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
plt.plot(dates,values)
plt.show()




