import tk

import sys
import os

# https://stackoverflow.com/questions/62854319/how-to-make-pynput-prevent-certain-keystrokes-from-reaching-a-particular-applica
# https://gist.github.com/chriskiehl/2906125
import win32api
# pywin32
import win32.lib.win32con as win32con
from pynput.keyboard import Key, KeyCode, Listener, Controller

import Levenshtein

from vkcodes import VK_CODE, VK_CODE_TO_ALPHA, SUPPRESSED_VK_CODES, VK_CODE_WHITESPACE

# https://github.com/tinmarr/Word-Unscrambler
def RemoveFromList(thelist, val):
    return [value for value in thelist if value != val]

def GetDic():
    try:
        dicopen = open("DL.txt", "r")
        dicraw = dicopen.read()
        dicopen.close()
        diclist = dicraw.split("\n")
        diclist = RemoveFromList(diclist, '')
        return diclist
    except FileNotFoundError:
        print("No Dictionary!")
        return 
    
def Word2Vect(word):
    l = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    v = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    w = word.lower()
    wl = list(w)
    for i in range(0, len(wl)):
        if wl[i] in l:
            ind = l.index(wl[i])
            v[ind] += 1
    return v

def Vect2Int(vect):
    pv = 0
    f = 0
    for i in range(0, len(vect)):
        wip = (vect[i]*(2**pv))
        f += wip
        pv += 4
    return f
    
def Ints2Dic(dic):
    d = {}
    for i in range(0, len(dic)):
        v = Word2Vect(dic[i])
        Int = Vect2Int(v)
        if Int in d:
            tat = d.get(Int)
            tat.append(dic[i])
            d[Int] = tat
        elif Int not in d:
            d[Int] = [dic[i]]
    return d

def findMatches(s):
  global ind
  v = Vect2Int(Word2Vect(s))
  return ind.get(v, [])

def main():
  global listener
  global currentWord
  global ind
  global heldKeys
  global enabled
  global isAddingWord

  # Initialize dictionary
  d = GetDic()
  ind = Ints2Dic(d)

  controller = Controller()

  heldKeys = set()

  enabled = True
  isAddingWord = False
  currentWord = ""

  def outputWord(word):
    for c in word:
      win32api.keybd_event(VK_CODE[c], 0, 0, EXTRA_INFO_FLAG)
      win32api.keybd_event(VK_CODE[c], 0, win32con.KEYEVENTF_KEYUP, EXTRA_INFO_FLAG)

  def updateConsole():
    global currentWord
    global enabled
    # https://stackoverflow.com/questions/4810537/how-to-clear-the-screen-in-python
    os.system('cls') # on windows
    text = ""
    if enabled:
      text += "ACTIVE: "
      text += currentWord
    else:
      text = "DISABLED"
    print(text)

  def on_press(key):
    global heldKeys
    global currentWord
    
    # print('on press', key)
    if key == Key.backspace and len(currentWord) > 0:
      if (Key.ctrl_l not in heldKeys and 
      Key.ctrl_r not in heldKeys):
        currentWord = currentWord[:-1]
      else:
        currentWord = ""
      updateConsole()
    elif (
      Key.ctrl_l not in heldKeys and 
      Key.ctrl_r not in heldKeys and 
      Key.alt_l not in heldKeys and 
      Key.alt_gr not in heldKeys):
      # Ignore special command strokes
      char = str(key)[1:-1]
      if len(char) == 1 and char.isalpha():
        currentWord += char
        updateConsole()
      elif len(currentWord) > 0 and (
        key == Key.space or 
        key == Key.tab or 
        key == Key.enter or 
        (len(char) == 1 and not char.isalpha())
      ):
        matches = findMatches(currentWord)
        # print(currentWord, "matches", matches)
        if (len(matches) == 0):
          outputWord(currentWord)
        else:
          # Order words by Levenshtein distance
          # https://towardsdatascience.com/calculating-string-similarity-in-python-276e18a7d33a
          matches.sort(key=lambda s: Levenshtein.distance(s, currentWord))
          # print(currentWord, "matches", matches)
          outputWord(matches[0])
        currentWord = ""
        if (key == Key.space):
          char = "spacebar"
        elif (key == Key.tab):
          char = "tab"
        elif (key == Key.enter):
          char = "enter"
        win32api.keybd_event(VK_CODE[char], 0, 0, EXTRA_INFO_FLAG)
        win32api.keybd_event(VK_CODE[char], 0, win32con.KEYEVENTF_KEYUP, EXTRA_INFO_FLAG)
        updateConsole()

    if key not in heldKeys:
      heldKeys.add(key)

  def on_release(key):
    global heldKeys
    # print('on release', key)
    if key in heldKeys:
      heldKeys.remove(key)
    if key == Key.esc:
      return False # This will quit the listener

  EXTRA_INFO_FLAG = 1
  # https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-kbdllhookstruct
  def win32_event_filter(msg, data):
    global heldKeys
    global enabled
    global isAddingWord
    global currentWord

    # print(msg, data.vkCode, data.dwExtraInfo)

    # Using the extra info flag to mark our own injected messages
    if data.dwExtraInfo or isAddingWord:
      listener._suppress = False
      return False

    # Suppress key if it's alphabet
    if (msg == 257 or msg == 256) and data.vkCode in VK_CODE_TO_ALPHA and (
      Key.ctrl_l not in heldKeys and 
      Key.ctrl_r not in heldKeys and 
      Key.alt_l not in heldKeys and 
      Key.alt_gr not in heldKeys):
      if enabled:
        listener._suppress = True
      else:
        listener._suppress = False
        return False
      # return False # if you return False, your on_press/on_release will not be called
    elif msg == 256 and data.vkCode == VK_CODE['spacebar'] and (Key.shift in heldKeys and Key.ctrl_l in heldKeys):
      # Add new word using shift ctrl space
      enabled = not enabled
      updateConsole()
      isAddingWord = True
      wta = str(input('What is the word you would like to add? '))
      dicopen = open("DL.txt", "a")
      dicopen.write('\n')
      dicopen.write(wta)
      dicopen.close()
      d = GetDic()
      ind = Ints2Dic(d)
      print('Dictionary Updated')
      isAddingWord = False
    elif msg == 256 and data.vkCode == VK_CODE['spacebar'] and (Key.shift in heldKeys or Key.shift_r in heldKeys):
      # Toggle functionality using shift space
      enabled = not enabled
      updateConsole()
      listener._suppress = True
    elif msg == 256 and (data.vkCode == VK_CODE['backspace'] or data.vkCode in SUPPRESSED_VK_CODES) and len(currentWord) > 0:
      # Suppress output if backspace or triggerring unscrambling process
      listener._suppress = True
    else:
      listener._suppress = False

    return True

  # Collect events until released
  listener = Listener(on_press=on_press, on_release=on_release, win32_event_filter=win32_event_filter, suppress=False)
  with listener as ml:
    ml.join()

if __name__ == "__main__":
  main()
