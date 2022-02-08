import face_recognition
import cv2
import numpy as np 
from livenessmodel import get_liveness_model
from userss import get_users
font = cv2.FONT_HERSHEY_DUPLEX

# Получить живую сеть
model = get_liveness_model()
# Загрузить веса в новую модель
model.load_weights("model/model.h5")
# Чтение данных пользователей и создание кодировок лиц
names, encods = get_users()
video_capture = cv2.VideoCapture(0)
video_capture.set(3, 640)
video_capture.set(4, 480)
# Инициализирование некоторых переменных
locations = []
encodings = []
names = []
process = True
inputdb = []
while True:
    # Захватить один кадр видео
    if len(inputdb) < 24:
        ret, frame = video_capture.read()
        liveimg = cv2.resize(frame, (100,100))
        liveimg = cv2.cvtColor(liveimg, cv2.COLOR_BGR2GRAY)
        inputdb.append(liveimg)
    else:
        ret, frame = video_capture.read()
        liveimg = cv2.resize(frame, (100,100))
        liveimg = cv2.cvtColor(liveimg, cv2.COLOR_BGR2GRAY)
        inputdb.append(liveimg)
        inp = np.array([inputdb[-24:]])
        inp = inp/255
        inp = inp.reshape(1,24,100,100,1)
        pred = model.predict(inp)
        inputdb = inputdb[-25:]
        if pred[0][0]> .95:
            # Измените размер кадра видео до размера 1/4 для более быстрой обработки распознавания лиц
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Обрабатывать только каждый второй кадр видео, чтобы сэкономить время
            if process:
                # Найти все лица и кодировки лиц в текущем кадре видео
                locations = face_recognition.face_locations(small_frame)
                encodings = face_recognition.face_encodings(small_frame, locations)
                name = "Unknown"
                names = []
                for encoding in encodings:
                    for ii in range(len(encods)):
                        # Посмотреть, совпадает ли лицо с известным лицом (лицами)
                        match = recognition.compare_faces([encods[ii]], encoding)
                        if match[0]:
                            name = names[ii]
                    names.append(name)
            process = not process
            unlock = False
            for n in names:
                if n != 'Unknown':
                    unlock=True
            # Показать результат
            for (top, right, bottom, left), name in zip(locations, names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                # Рамка вокруг лица
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
                # Метка с именем под лицом
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 0), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                if unlock:
                    cv2.putText(frame, 'UNLOCK', (frame.shape[1]//2, frame.shape[0]//2), font, 1.0, (255, 255, 255), 1)
                else:
                    cv2.putText(frame, 'LOCKED!', (frame.shape[1]//2, frame.shape[0]//2), font, 1.0, (255, 255, 255), 1)
        # Отображение показателя живучести в верхнем левом углу    
        cv2.putText(frame, str(pred[0][0]), (20, 20), font, 1.0, (255, 255, 0), 1)
        # Полученное изображение
        cv2.imshow('Video', frame)
        # Нажмите «q» на клавиатуре, чтобы выйти!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
video_capture.release()
cv2.destroyAllWindows()
