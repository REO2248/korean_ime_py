import pynput.keyboard as keyboard
from convtable import conversion_table
from keytable import keytable
from acor_dic import acor_dic
from worddic import worddic

keycontroller = keyboard.Controller()

internalkeystroke=1

def common_prefix(str1, str2):
    min_length = min(len(str1), len(str2))
    for i in range(min_length):
        if str1[i] != str2[i]:
            return str1[:i]
    return str1[:min_length]

def bsandinput(str1, str2):
    prefix = common_prefix(str1, str2)
    return len(str1) - len(prefix), str2[len(prefix):]

def keystroke(key):
    global internalkeystroke
    global keycontroller
    internalkeystroke+=1
    keycontroller.press(key)
    keycontroller.release(key)

def input_text(text):
    global keystroke
    global internalkeystroke
    for char in text:
        keystroke(char)

def conversion(text):
    r=text[:]
    for conv in conversion_table:
        r=r.replace(conv[0],conv[1])
    return r

beforetext=''
lastbefore=''

def commit():
    global beforetext
    global lastbefore
    if lastbefore in acor_dic.keys():
        for i in range(len(lastbefore)):
            keystroke(keyboard.Key.backspace)
        input_text(acor_dic[lastbefore])
    beforetext=''
    lastbefore=''

def stroke(char=''):
    global beforetext
    global lastbefore
    backspaced=0
    if char=='BACKSPACE':
        beforetext=beforetext[0:-1]
        backspaced=1
    else:
        beforetext+=char
    bslen, viewtext=bsandinput(lastbefore,conversion(beforetext))
    for i in range(bslen-backspaced):
        keystroke(keyboard.Key.backspace)
    input_text(viewtext)
    print(conversion(beforetext))
    lastbefore=conversion(beforetext)



with keyboard.Events() as events:
    for event in events:
        if event.key==keyboard.Key.esc:
            exit()
        if type(event)==keyboard.Events.Release:
            pass
        if type(event)==keyboard.Events.Press:
            if internalkeystroke>0:
                internalkeystroke-=1
                continue
            if type(event.key)==keyboard._win32.KeyCode and event.key.char is not None and event.key.char in keytable.keys():
                keystroke(keyboard.Key.backspace)
                stroke(keytable[event.key.char])
            elif event.key==keyboard.Key.backspace:
                if len(beforetext)>0:
                    stroke('BACKSPACE')
                else:
                    commit()
            else:
                if event.key in [keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r,
                                keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
                    continue
                if type(event.key)==keyboard._win32.KeyCode and event.key.char is not None or event.key==keyboard.Key.enter or event.key==keyboard.Key.space:
                    keystroke(keyboard.Key.backspace)
                commit()
                keystroke(event.key)