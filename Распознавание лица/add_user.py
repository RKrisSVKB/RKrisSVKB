import PySimpleGUI as sg
import os


sg.theme("default1")
layout = [
          [sg.Text("Добавление пользователя: ", key = "Text1",text_color='blue',size=(52,1))],
          [sg.Text("Имя пользователя: ", key = "Text2",size=(14,1))],
          [sg.InputText(key = "UserName",size=(14,1))],
          [sg.Text("Файл:"),sg.Input("", size=(30,1)) ,sg.FileBrowse("Выбрать файл", key="-IN1-"),sg.T("", size=(5,1)) ],
          [sg.Button("Добавить пользователя", key = "Open")],
          [sg.Text("", key = "-Message-", text_color='green', size=(32,2))]

        ]

window = sg.Window('Добавление пользователя', layout, size=(400,200))
save_path = 'client/'

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event == "Open":
        FilePath = values["-IN1-"]
        f = open(FilePath, "r")
        if FilePath[-3:].lower() == "jpg":
            file_name = values["UserName"] + ".jpg"
            completeName = os.path.join(save_path, file_name)
            file1 = open(completeName, "w")
            file1.close()
            window['-Message-'].Update(text_color = 'green')
            window['-Message-'].Update("Пользователь успешно добавлен!")

        else:
            window['-Message-'].Update(text_color = 'red')
            window['-Message-'].Update("Выбранный файл должен иметь расширение .jpg!")
    
        f.close()
    else:
        pass
           
