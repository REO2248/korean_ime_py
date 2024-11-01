import pynput.keyboard as keyboard
from convtable import conversion_table
from keytable import keytable
from acor_dic import acor_dic
from worddic import worddic

keycontroller = keyboard.Controller()

internalkeystroke=0

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
convtext=''
convselecting=False
convnum=0

def commit():
    global beforetext
    global lastbefore
    global convtext
    global convselecting
    global convnum
    if lastbefore in acor_dic.keys():
        for i in range(len(lastbefore)):
            keystroke(keyboard.Key.backspace)
        input_text(acor_dic[lastbefore])
    beforetext=''
    lastbefore=''
    convselecting=False
    convnum=0

def stroke(char=''):
    global beforetext
    global lastbefore
    global convtext
    global convselecting
    global convnum
    global commit
    backspaced=0
    convselecting=False
    convnum=0
    if char=='BACKSPACE':
        beforetext=beforetext[0:-1]
        backspaced=1
    elif char in '《》〈〉':
        beforetext+=char
        commit()
        input_text(char)
        return
    else:
        if convselecting:
            commit()
        beforetext+=char
    bslen, viewtext=bsandinput(lastbefore,conversion(beforetext))
    for i in range(bslen-backspaced):
        keystroke(keyboard.Key.backspace)
    input_text(viewtext)
    print(conversion(beforetext).replace('','김일성').replace('','김정일').replace('','김정은'))
    lastbefore=conversion(beforetext)

def convkey(shift:int=1):
    global beforetext
    global lastbefore
    global convtext
    global convselecting
    global convnum
    if conversion(beforetext) not in worddic:
        return
    if not convselecting:
        convtext=conversion(beforetext)
    thiswordconvs=[convtext.replace('','김일성').replace('','김정일').replace('','김정은')] + worddic[convtext]
    for i in range(len(thiswordconvs[convnum])):
        keystroke(keyboard.Key.backspace)
    convselecting=True
    convnum+=shift
    convnum=convnum%len(thiswordconvs)
    input_text(thiswordconvs[convnum])
    print('  '.join(f'>>{i}:{item}<<' if i == convnum else f'{i}:{item}' for i, item in enumerate(thiswordconvs)))
    print(convnum,thiswordconvs[convnum])
    lastbefore=thiswordconvs[convnum]

shiftldown=False
ctrlldown=False
is_inputmethod_enable=True

with keyboard.Events() as events:
    for event in events:
        if shiftldown and event.key==keyboard.Key.esc:
            exit()
        if type(event)==keyboard.Events.Release:
            if event.key==keyboard.Key.shift:
                shiftldown=False
            elif event.key==keyboard.Key.ctrl_l:
                ctrlldown=False
        if type(event)==keyboard.Events.Press:
            if internalkeystroke>0:
                internalkeystroke-=1
                continue
            if event.key==keyboard.Key.shift:
                shiftldown=True
            elif event.key==keyboard.Key.ctrl_l:
                ctrlldown=True
            if shiftldown and event.key==keyboard.Key.shift_r:
                if is_inputmethod_enable:
                    if convselecting:
                        commit()
                    is_inputmethod_enable=False
                    print('disabled')
                else:
                    is_inputmethod_enable=True
                    print('enabled')
                continue
            if not is_inputmethod_enable:
                continue
            if ctrlldown:
                continue
            if type(event.key)==keyboard._win32.KeyCode and event.key.char is not None and event.key.char in keytable.keys():
                if convselecting:
                    commit()
                keystroke(keyboard.Key.backspace)
                stroke(keytable[event.key.char])
            elif event.key==keyboard.Key.backspace:
                if len(beforetext)>0:
                    stroke('BACKSPACE')
                else:
                    commit()
            elif event.key==keyboard.Key.shift_r:
                if convselecting and shiftldown:
                    convkey(-1)
                else:
                    convkey(1)
            else:
                if event.key in [keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r,
                                keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
                    continue
                if type(event.key)==keyboard._win32.KeyCode and event.key.char is not None or event.key==keyboard.Key.enter or event.key==keyboard.Key.space:
                    keystroke(keyboard.Key.backspace)
                commit()
                if internalkeystroke>0:
                    keystroke(event.key)