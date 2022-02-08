import face_recognition
from os import listdir
from os.path import isfile, join
from glob import glob

def get_users():
    names=[]
    encods=[]
    for i in glob("client/*.jpg"):
        img = face_recognition.load_image_file(i)
        encoding = face_recognition.encodings(img)[0]
        encods.append(encoding)
        names.append(i[7:-4])
    return names, encods


