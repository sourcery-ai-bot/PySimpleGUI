import subprocess
import sys
import PySimpleGUI as sg
import re

"""
	Demo Program - Realtime output of a shell command in the window using ANSI color codes
		Shows how you can run a long-running subprocess and have the output
		be displayed in realtime in the window.  The output is assumed to have color codes embedded in it
"""


def cut_ansi_string_into_parts(string_with_ansi_codes):
    """
    Converts a string with ambedded ANSI Color Codes and parses it to create
    a list of tuples describing pieces of the input string.
    :param string_with_ansi_codes:
    :return: [(sty, str, str, str), ...] A list of tuples. Each tuple has format: (text, text color, background color, effects)
    """
    color_codes_english = ['Black', 'Red', 'Green', 'Yellow', 'Blue', 'Magenta', 'Cyan', 'White', 'Reset']
    color_codes = ["30m", "31m", "32m", "33m", "34m", "35m", "36m", "37m", "0m"]
    effect_codes_english = ['Italic', 'Underline', 'Slow Blink', 'Rapid Blink', 'Crossed Out']
    effect_codes = ["3m", "4m", "5m", "6m", "9m"]
    background_codes = ["40m", "41m", "42m", "43m", "44m", "45m", "46m", "47m"]
    background_codes_english = ["Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White"]

    ansi_codes = color_codes + effect_codes

    tuple_list = []

    string_list = string_with_ansi_codes.split("\u001b[")

    if (len(string_list)) == 1:
        string_list = string_with_ansi_codes.split("\033[")

    for teststring in string_list:
        if teststring == string_with_ansi_codes:
            tuple_list += [(teststring, None, None, None)]
            break
        if any(code in teststring for code in ansi_codes):
            static_string = None
            color_used = None
            effect_used = None
            background_used = None
            for color in range(len(color_codes)):
                if teststring.startswith(color_codes[color]):
                    working_thread = teststring.split(color_codes[color])
                    ansi_strip = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
                    static_string = ansi_strip.sub('', working_thread[1])
                    color_used = color_codes_english[color]
            for effect in range(len(effect_codes)):
                if teststring.startswith(effect_codes[effect]):
                    working_thread = teststring.split(effect_codes[effect])
                    ansi_strip = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
                    static_string = ansi_strip.sub('', working_thread[1])
                    effect_used = effect_codes_english[effect]
            for background in range(len(background_codes)):
                if teststring.startswith(background_codes[background]):
                    working_thread = teststring.split(background_codes[background])
                    ansi_strip = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
                    static_string = ansi_strip.sub('', working_thread[1])
                    background_used = background_codes_english[background]
            try:
                if not tuple_list[-1][0]:
                    if tuple_list[-1][1] is not None:
                        color_used = tuple_list[-1][1]
                    if tuple_list[-1][2] is not None:
                        background_used = tuple_list[-1][2]
                    if tuple_list[-1][3] is not None:
                        effect_used = tuple_list[-1][3]
                tuple_list += [(static_string, color_used, background_used, effect_used)]
            except Exception:
                tuple_list += [(static_string, color_used, background_used, effect_used)]

    return [
        (tuple_[0], tuple_[1], tuple_[2], tuple_[3])
        for tuple_ in tuple_list
        if tuple_[0]
    ]


def main():
    layout = [
        [sg.Multiline(size=(110, 30), font='courier 10', background_color='black', text_color='white', key='-MLINE-')],
        [sg.T('Promt> '), sg.Input(key='-IN-', focus=True, do_not_clear=False)],
        [sg.Button('Run', bind_return_key=True), sg.Button('Exit')]]

    window = sg.Window('Realtime Shell Command Output', layout)

    while True:  # Event Loop
        event, values = window.read()
        # print(event, values)
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Run':
            runCommand(cmd=values['-IN-'], window=window)
    window.close()


def runCommand(cmd, timeout=None, window=None):
    """ run shell command
    @param cmd: command to execute
    @param timeout: timeout for command execution
    @param window: the PySimpleGUI window that the output is going to (needed to do refresh on)
    @return: (return code from command, command output)
    """
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        ansi_list = cut_ansi_string_into_parts(line)
        for ansi_item in ansi_list:
            if ansi_item[1] == 'Reset':
                ansi_item[1] = None
            window['-MLINE-'].update(ansi_item[0] + '\n', text_color_for_value=ansi_item[1], background_color_for_value=ansi_item[2], append=True,
                                     autoscroll=True)
        window.refresh()

    return p.wait(timeout)


sg.theme('Dark Blue 3')
main()
