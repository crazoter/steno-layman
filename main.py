import tk

import sys
import os
from threading import Thread,Event
from enum import Enum

# https://stackoverflow.com/questions/62854319/how-to-make-pynput-prevent-certain-keystrokes-from-reaching-a-particular-applica
# https://gist.github.com/chriskiehl/2906125
import win32api
# pywin32
import win32.lib.win32con as win32con
from pynput.keyboard import Key, KeyCode, Listener, Controller

import Levenshtein

from Vkcodes import VK_CODE, VK_CODE_TO_ALPHA, SUPPRESSED_VK_CODES, VK_CODE_WHITESPACE
from WordUnscrambler import *

class SPACING_MODE(Enum):
  ADD_SPACE = 1 # Default
  CAMEL_CASE = 2
  # SNAKE_CASE = 3 # Press the symbol you want to delimit with
  # NO_SPACE = 4 # Press enter instead of space

def findMatches(s):
  global ind
  v = Vect2Int(Word2Vect(s))
  return ind.get(v, [])

def GetSnippets():
  try:
    dicopen = open("snippets.txt", "r")
    dicraw = dicopen.read()
    dicopen.close()
    diclist = dicraw.split("\n")
    diclist = RemoveFromList(diclist, '')
    snippets = {}
    for s in diclist:
      delimIdx = s.find(":")
      if (delimIdx > 0 and len(s[delimIdx+1:]) > 0):
        snippets[s[0:delimIdx]] = s[delimIdx+1:]
    return snippets
  except FileNotFoundError:
    print("No Snippets!")
    return {}

# Budget gui because i'm lazy 
def updateConsole(enabled, currentWord):
  global capitalizedArr
  # https://stackoverflow.com/questions/4810537/how-to-clear-the-screen-in-python
  os.system('cls') # on windows
  text = ""
  if enabled:
    text += "ACTIVE: "
    text += currentWord
  else:
    text = "DISABLED"
  print(text)
  print(capitalizedArr)

def addWordThread(evt):
  try:
    wta = str(input('What is the word you would like to add? '))
    wta = wta.strip().lower()
    dicopen = open("DL.txt", "a")
    dicopen.write('\n')
    dicopen.write(wta)
    dicopen.close()
  except BaseException as e:
    # KeyboardInterrupt alone didn't work
    pass

  # Tell main thread that it's done
  enabled = True
  currentWord = ""
  updateConsole(enabled, currentWord)
  print('Dictionary Updated.')
  evt.set()
  return

def main():
  global listener
  global currentWord
  global ind
  global heldKeys
  global enabled
  global isAddingWord
  global capsLockActive
  global capitalizedArr
  global addWordEvent
  global snippets

  # Initialize dictionary
  d = GetDic()
  ind = Ints2Dic(d)

  snippets = GetSnippets()

  addWordEvent = Event()

  controller = Controller()

  heldKeys = set()

  enabled = True
  isAddingWord = False
  currentWord = ""
  capsLockActive = False
  # Note that this is not exact for spellchecked words.
  capitalizedArr = []
  currentSpacingMode = SPACING_MODE.ADD_SPACE

  def keyIsWhitespace(key):
    return (key == Key.space or 
      key == Key.tab or 
      key == Key.enter)

  def noCmdKeyIsHeld(heldKeys):
    return (Key.ctrl_l not in heldKeys and 
      Key.ctrl_r not in heldKeys and 
      Key.alt_l not in heldKeys and 
      Key.alt_gr not in heldKeys and
      Key.cmd not in heldKeys)

  def outputWord(word):
    global capitalizedArr 
    global capsLockActive
    global heldKeys
    idx = 0
    word = word.lower()
    for c in word:
      if idx >= len (capitalizedArr):
        idx = 0

      # Use shift based on state of capslock
      shiftKeysPressed = Key.shift in heldKeys or Key.shift_r in heldKeys

      if capitalizedArr[idx] != capsLockActive:
        win32api.keybd_event(VK_CODE['left_shift'], 0, 0, EXTRA_INFO_FLAG)
      elif not capitalizedArr[idx] and shiftKeysPressed:
        win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, EXTRA_INFO_FLAG)
        win32api.keybd_event(VK_CODE['right_shift'], 0, win32con.KEYEVENTF_KEYUP, EXTRA_INFO_FLAG)

      win32api.keybd_event(VK_CODE[c], 0, 0, EXTRA_INFO_FLAG)
      win32api.keybd_event(VK_CODE[c], 0, win32con.KEYEVENTF_KEYUP, EXTRA_INFO_FLAG)

      if capitalizedArr[idx] != capsLockActive:
        win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, EXTRA_INFO_FLAG)
      # Re-inputting the shift keys causes issues, so I'll omit it for now
      # elif not capitalizedArr[idx] and shiftKeysPressed:
      #   win32api.keybd_event(VK_CODE['left_shift'], 0, 0, EXTRA_INFO_FLAG)
      #   win32api.keybd_event(VK_CODE['right_shift'], 0, 0, EXTRA_INFO_FLAG)

      idx += 1

  def on_press(key):
    global heldKeys
    global currentWord
    global capsLockActive
    global capitalizedArr
    global snippets

    matches = []
    
    # print('on press', key)
    if (key == Key.caps_lock):
      # May want to improve with
      # https://stackoverflow.com/questions/34028478/python-3-detect-caps-lock-status
      capsLockActive = not capsLockActive
    elif key == Key.backspace and len(currentWord) > 0:
      # Delete the previous char in the buffer
      if (Key.ctrl_l not in heldKeys and 
      Key.ctrl_r not in heldKeys):
        currentWord = currentWord[:-1]
        capitalizedArr = capitalizedArr[:-1]
      else:
        currentWord = ""
        capitalizedArr = []
      updateConsole(enabled, currentWord)
    elif noCmdKeyIsHeld(heldKeys):
      # Ignore special command strokes
      char = str(key)[1:-1]
      if len(char) == 1 and char.isalpha():
        # Add character
        currentWord += char
        # Add capitalization
        capitalizedArr.append(capsLockActive or Key.shift in heldKeys or Key.shift_r in heldKeys)

        updateConsole(enabled, currentWord)
      elif len(currentWord) > 0 and (
        keyIsWhitespace(key) or 
        (len(char) == 1 and not char.isalpha())
      ):
        output = None
        # Perform conversion if shift is not held on whitespace
        if (Key.shift not in heldKeys and Key.shift_r not in heldKeys):
          matches = findMatches(currentWord)
          # print(currentWord, "matches", matches)
          # Perform minor typo fix checks
          # Amortized O(n)
          for i in range(len(currentWord)):
            # Try duplicating the character 
            matches = matches + findMatches(currentWord[:i] + currentWord[i] + currentWord[i:])
            # Try removing the character 
            matches = matches + findMatches(currentWord[0:i] + currentWord[i+1:])
            
          # If still can't find anything just return the word as-is
          if (len(matches) == 0):
            output = currentWord
          else:
            # Get best word by Levenshtein distance
            # https://towardsdatascience.com/calculating-string-similarity-in-python-276e18a7d33a
            shortestDistance = None
            # Tiebreak by least amount of characters added / removed
            bestCharDist = None
            for s in matches:
              # Add length to weight (to defray costs of swap; otherwise, ti -> tit over it)
              currCharDist = abs(len(s) - len(currentWord))
              distance = Levenshtein.distance(s, currentWord) + currCharDist
              if distance == shortestDistance and bestCharDist > currCharDist:
                bestCharDist = currCharDist
                output = s
              if shortestDistance == None or distance < shortestDistance:
                shortestDistance = distance
                bestCharDist = currCharDist
                output = s
        else:
          # Output without conversion if shift + space
          output = currentWord

        leftShift = Key.shift in heldKeys
        rightShift = Key.shift_r in heldKeys

        if output and snippets and output in snippets:
          output = snippets[output]

        outputWord(output)
        prevInput = currentWord
        currentWord = ""
        capitalizedArr = []
        # We blocked the actual key sent, so need to send it out here 
        if (key == Key.space):
          char = "spacebar"
        elif (key == Key.tab):
          char = "tab"
        elif (key == Key.enter):
          # Just send as-is without anything behind if pressed enter
          char = None
        if char:
          if (leftShift):
            win32api.keybd_event(VK_CODE['left_shift'], 0, 0, EXTRA_INFO_FLAG)
          if (rightShift):
            win32api.keybd_event(VK_CODE['right_shift'], 0, 0, EXTRA_INFO_FLAG)

          win32api.keybd_event(VK_CODE[char], 0, 0, EXTRA_INFO_FLAG)
          win32api.keybd_event(VK_CODE[char], 0, win32con.KEYEVENTF_KEYUP, EXTRA_INFO_FLAG)

        updateConsole(enabled, currentWord)
        print("Previous input:", prevInput)
        print("Previous output:", output)
        if (matches):
          print("Found matches (unordered):", matches)
        else:
          print("No matches found in dictionary")

    if key not in heldKeys:
      heldKeys.add(key)

  def on_release(key):
    global heldKeys
    # print('on release', key)
    if key in heldKeys:
      heldKeys.remove(key)
    if key == Key.esc:
      # Exit
      return False

  EXTRA_INFO_FLAG = 1
  # https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-kbdllhookstruct
  def win32_event_filter(msg, data):
    global heldKeys
    global enabled
    global isAddingWord
    global currentWord
    global addWordEvent
    global d
    global ind

    # print(msg, data.vkCode, data.dwExtraInfo)

    # Wait for response from thread after adding a word and set flags.
    # put into another thread for responsiveness.
    if isAddingWord and addWordEvent.is_set():
      # Reset dict
      d = GetDic()
      ind = Ints2Dic(d)
      print('Reloading dictionary...')
      enabled = True
      isAddingWord = False

    # Using the extra info flag to mark our own injected messages
    if data.dwExtraInfo or isAddingWord:
      listener._suppress = False
      return False

    # Suppress key if app is enabled, it's alphabet & it's not part of a command
    if (msg == 257 or msg == 256) and data.vkCode in VK_CODE_TO_ALPHA and noCmdKeyIsHeld(heldKeys):
      listener._suppress = enabled
      return enabled
    elif msg == 256 and data.vkCode == VK_CODE['spacebar'] and (Key.shift in heldKeys and Key.ctrl_l in heldKeys):
      # Add new word using shift ctrl space
      enabled = False
      isAddingWord = True
      # Clear the old command flags (shift and ctrl)
      win32api.keybd_event(0xA0, 0, win32con.KEYEVENTF_KEYUP, 0)
      win32api.keybd_event(0xA1, 0, win32con.KEYEVENTF_KEYUP, 0)
      win32api.keybd_event(0xA2, 0, win32con.KEYEVENTF_KEYUP, 0)
      win32api.keybd_event(0xA3, 0, win32con.KEYEVENTF_KEYUP, 0)
      # p = subprocess.call(["py", "./addWord.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
      addWordEvent=Event()
      thread = Thread(target = addWordThread, args = (addWordEvent, ))
      thread.start()
    elif msg == 256 and data.vkCode == VK_CODE['spacebar'] and (
      Key.shift in heldKeys or Key.shift_r in heldKeys
    ):
      # Toggle functionality using shift space
      # If currentWord is not empty:
      # shift space: then spit it out without conversion
      # shift enter: spit it out without conversion or adding a new space
      # Otherwise, shift space disables the tool
      if len(currentWord) <= 0:
        enabled = not enabled
      updateConsole(enabled, currentWord)
      listener._suppress = True
    elif msg == 256 and (data.vkCode == VK_CODE['backspace'] or data.vkCode in SUPPRESSED_VK_CODES) and len(currentWord) > 0:
      # Suppress output if backspace or triggerring unscrambling process
      listener._suppress = True
    else:
      # else just don't touch the key
      listener._suppress = False
    return True

  # Collect events until released
  updateConsole(enabled, currentWord)
  listener = Listener(on_press=on_press, on_release=on_release, win32_event_filter=win32_event_filter, suppress=False)
  with listener as ml:
    ml.join()

if __name__ == "__main__":
  main()
