import pynput.keyboard as keyboard
from convtable import conversion_table
from keytable import keytable

keycontroller = keyboard.Controller()

internalkeystroke=1

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
    #input_text(lastbefore)
    beforetext=''
    lastbefore=''

def stroke(char=''):
    global beforetext
    global lastbefore
    bslen=len(lastbefore)
    if char=='BACKSPACE':
        beforetext=beforetext[0:-1]
        bslen-=1
    else:
        beforetext+=char
    for i in range(bslen):
        keystroke(keyboard.Key.backspace)
    input_text(conversion(beforetext))
    print(conversion(beforetext))
    lastbefore=conversion(beforetext)

with keyboard.Events() as events:
    for event in events:
        if type(event)==keyboard.Events.Release:
            pass
        if event.key==keyboard.Key.esc:
            exit()
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
                keystroke(keyboard.Key.backspace)
                commit()
                keystroke(event.key)