import sys
import os
from os import listdir

import PySimpleGUI as sg
import os


sg.theme("default1")
layout = [
          [sg.Text("Удаление пользователя: ", key = "Text1",text_color='blue',size=(52,1))],
          [sg.Text("Имя пользователя: ", key = "Text2",size=(14,1))],
          [sg.InputText(key = "UserName",size=(14,1))],
          [sg.Text("Файл:"),sg.Input("", size=(30,1)) ,sg.FileBrowse("Выбрать файл", key="-IN1-"),sg.T("", size=(5,1)) ],
          [sg.Button("Удалить пользователя", key = "Open")],
          [sg.Text("", key = "-Message-", text_color='green', size=(32,2))]

        ]

window = sg.Window('Удаление пользователя', layout, size=(400,200))
save_path = 'client/'

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event == "Open":
        test=os.listdir("/Users/User/Desktop/Распознавание лица/client")

        for item in test:
            if item.endswith(".jpg"):
                os.remove(item) 
            
            window['-Message-'].Update(text_color = 'green')
            window['-Message-'].Update("Пользователь успешно удален!")
                    
        else:
            pass


