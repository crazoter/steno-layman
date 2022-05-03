# https://gist.github.com/chriskiehl/2906125

#Giant dictonary to hold key name and VK value
VK_CODE = {'backspace':0x08,
           'tab':0x09,
           'clear':0x0C,
           'enter':0x0D,
           'shift':0x10,
           'ctrl':0x11,
           'alt':0x12,
           'pause':0x13,
           'caps_lock':0x14,
           'esc':0x1B,
           'spacebar':0x20,
           'page_up':0x21,
           'page_down':0x22,
           'end':0x23,
           'home':0x24,
           'left_arrow':0x25,
           'up_arrow':0x26,
           'right_arrow':0x27,
           'down_arrow':0x28,
           'select':0x29,
           'print':0x2A,
           'execute':0x2B,
           'print_screen':0x2C,
           'ins':0x2D,
           'del':0x2E,
           'help':0x2F,
           '0':0x30,
           '1':0x31,
           '2':0x32,
           '3':0x33,
           '4':0x34,
           '5':0x35,
           '6':0x36,
           '7':0x37,
           '8':0x38,
           '9':0x39,
           'a':0x41,
           'b':0x42,
           'c':0x43,
           'd':0x44,
           'e':0x45,
           'f':0x46,
           'g':0x47,
           'h':0x48,
           'i':0x49,
           'j':0x4A,
           'k':0x4B,
           'l':0x4C,
           'm':0x4D,
           'n':0x4E,
           'o':0x4F,
           'p':0x50,
           'q':0x51,
           'r':0x52,
           's':0x53,
           't':0x54,
           'u':0x55,
           'v':0x56,
           'w':0x57,
           'x':0x58,
           'y':0x59,
           'z':0x5A,
           'numpad_0':0x60,
           'numpad_1':0x61,
           'numpad_2':0x62,
           'numpad_3':0x63,
           'numpad_4':0x64,
           'numpad_5':0x65,
           'numpad_6':0x66,
           'numpad_7':0x67,
           'numpad_8':0x68,
           'numpad_9':0x69,
           'multiply_key':0x6A,
           'add_key':0x6B,
           'separator_key':0x6C,
           'subtract_key':0x6D,
           'decimal_key':0x6E,
           'divide_key':0x6F,
           'F1':0x70,
           'F2':0x71,
           'F3':0x72,
           'F4':0x73,
           'F5':0x74,
           'F6':0x75,
           'F7':0x76,
           'F8':0x77,
           'F9':0x78,
           'F10':0x79,
           'F11':0x7A,
           'F12':0x7B,
           'F13':0x7C,
           'F14':0x7D,
           'F15':0x7E,
           'F16':0x7F,
           'F17':0x80,
           'F18':0x81,
           'F19':0x82,
           'F20':0x83,
           'F21':0x84,
           'F22':0x85,
           'F23':0x86,
           'F24':0x87,
           'num_lock':0x90,
           'scroll_lock':0x91,
           'left_shift':0xA0,
           'right_shift':0xA1,
           'left_control':0xA2,
           'right_control':0xA3,
           'left_menu':0xA4,
           'right_menu':0xA5,
           'browser_back':0xA6,
           'browser_forward':0xA7,
           'browser_refresh':0xA8,
           'browser_stop':0xA9,
           'browser_search':0xAA,
           'browser_favorites':0xAB,
           'browser_start_and_home':0xAC,
           'volume_mute':0xAD,
           'volume_Down':0xAE,
           'volume_up':0xAF,
           'next_track':0xB0,
           'previous_track':0xB1,
           'stop_media':0xB2,
           'play/pause_media':0xB3,
           'start_mail':0xB4,
           'select_media':0xB5,
           'start_application_1':0xB6,
           'start_application_2':0xB7,
           'attn_key':0xF6,
           'crsel_key':0xF7,
           'exsel_key':0xF8,
           'play_key':0xFA,
           'zoom_key':0xFB,
           'clear_key':0xFE,
           '+':0xBB,
           ',':0xBC,
           '-':0xBD,
           '.':0xBE,
           '/':0xBF,
           '`':0xC0,
           ';':0xBA,
           '[':0xDB,
           '\\':0xDC,
           ']':0xDD,
           "'":0xDE,
           # Temporary fix
           ')':0x30,
           '!':0x31,
           '@':0x32,
           '#':0x33,
           '$':0x34,
           '%':0x35,
           '^':0x36,
           '&':0x37,
           '*':0x38,
           '(':0x39,
           'A':0x41,
           'B':0x42,
           'C':0x43,
           'D':0x44,
           'E':0x45,
           'F':0x46,
           'G':0x47,
           'H':0x48,
           'I':0x49,
           'J':0x4A,
           'K':0x4B,
           'L':0x4C,
           'M':0x4D,
           'N':0x4E,
           'O':0x4F,
           'P':0x50,
           'Q':0x51,
           'R':0x52,
           'S':0x53,
           'T':0x54,
           'U':0x55,
           'V':0x56,
           'W':0x57,
           'X':0x58,
           'Y':0x59,
           'Z':0x5A,
           '=':0xBB,
           '<':0xBC,
           '_':0xBD,
           '>':0xBE,
           '?':0xBF,
           '~':0xC0,
           ':':0xBA,
           '{':0xDB,
           '|':0xDC,
           '}':0xDD,
           '"':0xDE,
}

VK_CODE_TO_ALPHA = {
           0x41:'a',
           0x42:'b',
           0x43:'c',
           0x44:'d',
           0x45:'e',
           0x46:'f',
           0x47:'g',
           0x48:'h',
           0x49:'i',
           0x4A:'j',
           0x4B:'k',
           0x4C:'l',
           0x4D:'m',
           0x4E:'n',
           0x4F:'o',
           0x50:'p',
           0x51:'q',
           0x52:'r',
           0x53:'s',
           0x54:'t',
           0x55:'u',
           0x56:'v',
           0x57:'w',
           0x58:'x',
           0x59:'y',
           0x5A:'z'}

VK_CODE_WHITESPACE = {
  0x20:'spacebar',
  'tab':0x09,
  'enter':0x0D,
}

SUPPRESSED_VK_CODES = {
  0x20:'spacebar',
  0x09:'tab',
  0x0D:'enter',
  0x30:'0',
  0x31:'1',
  0x32:'2',
  0x33:'3',
  0x34:'4',
  0x35:'5',
  0x36:'6',
  0x37:'7',
  0x38:'8',
  0x39:'9',
  0xBB:'+',
  0xBC:',',
  0xBD:'-',
  0xBE:'.',
  0xBF:'/',
  0xC0:'`',
  0xBA:';',
  0xDB:'[',
  0xDC:'\\',
  0xDD:']',
  0xDE:"'",
  0xC0:'`'
}

def press(*args):
    '''
    one press, one release.
    accepts as many arguments as you want. e.g. press('left_arrow', 'a','b').
    '''
    for i in args:
        win32api.keybd_event(VK_CODE[i], 0,0,0)
        time.sleep(.05)
        win32api.keybd_event(VK_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)

def pressAndHold(*args):
    '''
    press and hold. Do NOT release.
    accepts as many arguments as you want.
    e.g. pressAndHold('left_arrow', 'a','b').
    '''
    for i in args:
        win32api.keybd_event(VK_CODE[i], 0,0,0)
        time.sleep(.05)
           
def pressHoldRelease(*args):
    '''
    press and hold passed in strings. Once held, release
    accepts as many arguments as you want.
    e.g. pressAndHold('left_arrow', 'a','b').

    this is useful for issuing shortcut command or shift commands.
    e.g. pressHoldRelease('ctrl', 'alt', 'del'), pressHoldRelease('shift','a')
    '''
    for i in args:
        win32api.keybd_event(VK_CODE[i], 0,0,0)
        time.sleep(.05)
            
    for i in args:
            win32api.keybd_event(VK_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)
            time.sleep(.1)
            
        

def release(*args):
    '''
    release depressed keys
    accepts as many arguments as you want.
    e.g. release('left_arrow', 'a','b').
    '''
    for i in args:
           win32api.keybd_event(VK_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)


def typer(string=None,*args):
##    time.sleep(4)
    for i in string:
        if i == ' ':
            win32api.keybd_event(VK_CODE['spacebar'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['spacebar'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == '!':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['1'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['1'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == '@':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['2'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['2'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == '{':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['['], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['['],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == '?':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['/'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['/'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == ':':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE[';'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE[';'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == '"':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['\''], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['\''],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == '}':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE[']'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE[']'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == '#':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['3'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['3'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == '$':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['4'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['4'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == '%':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['5'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['5'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == '^':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['6'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['6'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == '&':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['7'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['7'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == '*':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['8'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['8'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == '(':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['9'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['9'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == ')':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['0'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['0'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == '_':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['-'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['-'],0 ,win32con.KEYEVENTF_KEYUP ,0)


        elif i == '=':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['+'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['+'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == '~':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['`'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['`'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == '<':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE[','], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE[','],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == '>':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['.'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['.'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'A':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['a'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['a'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'B':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['b'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['b'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'C':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['c'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['c'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'D':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['d'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['d'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'E':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['e'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['e'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'F':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['f'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['f'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'G':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['g'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['g'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'H':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['h'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['h'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'I':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['i'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['i'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'J':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['j'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['j'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'K':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['k'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['k'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'L':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['l'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['l'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'M':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['m'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['m'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'N':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['n'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['n'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'O':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['o'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['o'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'P':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['p'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['p'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'Q':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['q'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['q'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'R':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['r'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['r'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'S':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['s'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['s'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'T':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['t'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['t'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'U':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['u'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['u'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'V':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['v'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['v'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'W':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['w'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['w'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'X':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['x'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['x'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'Y':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['y'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['y'],0 ,win32con.KEYEVENTF_KEYUP ,0)

        elif i == 'Z':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE['z'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE['z'],0 ,win32con.KEYEVENTF_KEYUP ,0)

    
        else:    
            win32api.keybd_event(VK_CODE[i], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)
