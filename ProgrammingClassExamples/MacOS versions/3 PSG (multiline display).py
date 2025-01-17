
#PySimple examples (v 3.8)
#Tony Crewe
#Oct 2018 MacOS

import PySimpleGUI as sg

#sg.ChangeLookAndFeel('GreenTan')

sg.SetOptions (background_color = 'Grey',
            element_background_color = 'Grey',
            text_element_background_color = 'Grey',
               font = ('Courier New', 12, 'bold'),
               text_color = 'White',
               input_text_color ='White',
               button_color = ('Grey', 'White'))


layout = [
    [sg.Text('Enter and Add Data to Display', font = ('Calibri', 16,'bold'))],
    [sg.Text('Race:', size = (5,1)), sg.InputText(size = (8,1)),
    sg.Text('Club:', size = (5,1)), sg.InputText(size = (8,1))],
    [sg.Text('Name:', size = (5,1)), sg.InputText(size = (8,1)),
    sg.Text('Time:', size = (5,1)), sg.InputText(size = (8,1)),sg.Text(' '),
     sg.ReadButton('Add Data', font = ('Calibri', 12, 'bold'))],
    [sg.Text('_'*40)],
    [sg.Text('  Race   Club       Name          Time')],
    [sg.Multiline(size =(44,6),key = '_multiline_')]
 ]

window = sg.Window('Enter & Display Data').Layout(layout)

string = ''
S=[]
while True:
  
    button, value = window.Read()
    if button is not None:
    #use string formatting - best way? plus Courier New font - non-proportional font
        S += ['{:^9s}{:<11s}{:<10s}{:>8s}'.format(value[0],value[1],value[2],value[3])]
        for s in S:
            string = string + s + '\n'
        window.FindElement('_multiline_').Update(string)
        string =''
    else:
        break   
