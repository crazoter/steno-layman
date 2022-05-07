import tk
import sys
import os
from timeit import default_timer as timer
from threading import Thread,Event
from enum import Enum
from collections import deque
from symspellpy import SymSpell, Verbosity
import numpy as np

# https://stackoverflow.com/questions/62854319/how-to-make-pynput-prevent-certain-keystrokes-from-reaching-a-particular-applica
# https://gist.github.com/chriskiehl/2906125
import win32api
# pywin32
import win32.lib.win32con as win32con
from pynput.keyboard import Key, KeyCode, Listener, Controller

import Levenshtein
from thefuzz import process as FuzzProcess

from Vkcodes import VK_CODE, VK_CODE_TO_ALPHA, SUPPRESSED_VK_CODES, VK_CODE_WHITESPACE
from WordUnscrambler import *

class SEARCH_ALGORITHM(Enum):
  UNSCRAMBLER = 1
  THE_FUZZ = 2
  CLUSTERING = 3
  SYM_SPELL = 4

CURRENT_SEARCH_ALGORITHM = SEARCH_ALGORITHM.SYM_SPELL

class SPACING_MODE(Enum):
  ADD_SPACE = 1 # Default
  CAMEL_CASE = 2
  SNAKE_CASE = 3
  NO_SPACE = 4
  AUTO_CAPITAL = 5
  NLP = 6 # Spellcheck & recommendation using NLP 

MAX_SEARCH_DEPTH = 3
MAX_DUPE_CHARS = 8
SYMSPELL_MAX_EDIT = 6

def getCharsSortedByFrequency():
  CHARS = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
  # https://en.wikipedia.org/wiki/Letter_frequency
  FREQUENCY_IN_DICTIONARY = [7.8,2,4,3.8,11,1.4,3,2.3,8.6,0.21,0.97,5.3,2.7,7.2,6.1,2.8,0.19,7.3,8.7,6.7,3.3,1,0.91,0.27,1.6,0.44]
  tmp = list(zip(CHARS,FREQUENCY_IN_DICTIONARY))
  tmp.sort(key=lambda t: t[1], reverse=True)
  return list(zip(*tmp))[0]

CHARS_BY_FREQUENCY = getCharsSortedByFrequency()

def initMatchData(currentWord):
  return [currentWord, "", None, None]

# matchData = [currentWord, output, shortestDistance, bestCharDist]
def getBestFromBinSearch(matches, depth, data):
  if not matches:
    return
  # Get best word by Levenshtein distance
  for s in matches:
    # Add length to weight (to defray costs of swap; otherwise, ti -> tit over it)
    currCharDist = abs(len(s) - len(data[0]))
    distance = Levenshtein.distance(s, data[0]) + currCharDist + depth
    if distance == data[2] and data[3] > currCharDist:
      data[3] = currCharDist
      data[1] = s
    if data[2] == None or distance < data[2]:
      data[2] = distance
      data[3] = currCharDist
      data[1] = s

def bfsBinSearch(ind, currentWord, firstNum, firstDepth):
  # BFS to ensure when we visit a permutation, it's with the shortest path
  # matches = set(ind.get(firstNum, []))
  matchData = initMatchData(currentWord)
  result = ind.get(firstNum)
  if result:
    getBestFromBinSearch(result, 0, matchData)
  traversed = set([firstNum])
  q = deque([(firstNum, firstDepth)])
  while len(q) > 0:
    currNum, depth = q.pop()
    for i in range(NUMBER_OF_ALPHABETS):
      # Add word 
      if bitmaskNum(currNum, i, True) < MAX_DUPE_CHARS:
        newNum = ModifyInt(currNum, i, 1)
        if depth > 0 and newNum not in traversed:
          traversed.add(newNum)
          result = ind.get(newNum)
          if result:
            # matches.update(result)
            getBestFromBinSearch(result, firstDepth + 1 - depth, matchData)
          q.append((newNum, depth - 1))
      # Remove word
      if bitmaskNum(currNum, i, False) > 0:
        newNum = ModifyInt(currNum, i, -1)
        if depth > 0 and newNum not in traversed:
          traversed.add(newNum)
          result = ind.get(newNum)
          if result:
            # matches.update(result)
            getBestFromBinSearch(result, firstDepth + 1 - depth, matchData)
          q.append((newNum, depth - 1))
      # Swap word
  # return matches
  return matchData

def searchByUnscramble(s):
  global ind
  # print(currentWord, "matches", matches)
  # Perform minor typo fix checks
  # Amortized O(n)
  # Possible Optimizations:
  # Don't vect2int the whole array
  # Perform the search on the matched array instead of concat then search whole array
  # Early terminate
  # Remove excess characters 
  currV = Word2Vect(currentWord)
  currNum = Vect2Int(currV)
  # output = ""
  # matches = bfsBinSearch(ind, currNum, 3)
  matches = []
  _, output, success, _ = bfsBinSearch(ind, currentWord, currNum, 3)

  # # Optimizations: perform the search without having to rebuild the vector
  # # Possible Heuristics:
  # # Only add existing characters
  # # Only remove characters
  # # First iteration: basic check (26+26)
  # for i in range(len(currV)):
  #   matches.update(ind.get(ModifyInt(currNum, i, 1), []))
  #   if (currV[i] > 0):
  #     matches.update(ind.get(ModifyInt(currNum, i, -1), []))

  # # Second iteration: 2 depth search (26^2 *4)
  # if (len(matches) == 0):
  #   for i in range(len(currV)):
  #     currV[i] += 1
  #     tmpNum = ModifyInt(currNum, i, 1)
  #     for j in range(len(currV)):
  #       if (currV[j] >= MAX_DUPE_CHARS):
  #         continue
  #       # Add 2
  #       matches.update(ind.get(ModifyInt(tmpNum, i, 1), []))
  #       if (i == j or currV[j] <= 0):
  #         continue
  #       # Add 1 subtract 1
  #       matches.update(ind.get(ModifyInt(tmpNum, i, -1), []))
  #     if i <= 0:
  #       continue
  #     currV[i] -= 1
  #     tmpNum = ModifyInt(currNum, i, -1)
  #     for j in range(len(currV)):
  #       if (currV[j] <= 0):
  #         continue
  #       # Subtract 2
  #       matches.update(ind.get(ModifyInt(tmpNum, i, -1), []))
  #       if (i == j or currV[j] >= MAX_DUPE_CHARS):
  #         continue
  #       # Subtract 1 add 1
  #       matches.update(ind.get(ModifyInt(tmpNum, i, 1), []))

  # # Use clustering for deeper search
  # if (len(matches) == 0):
  #   matches = transformWordIntoCluster(currentWord)

  # If still can't find anything just return the word as-is
  # if (len(matches) == 0):
  if not success:
    output = s
  elif len(matches) > 0:
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
  return (matches, output)

def searchByTheFuzz(s):
  global d
  matches = FuzzProcess.extract(s, d, limit = 3)
  return (matches, matches[0][0])
def searchByClusteringOnly(currentWord):
  matches = transformWordIntoCluster(currentWord)
  # Get best word by Levenshtein distance
  output = None
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
  return (matches, output)

# DP approach: O(xy)
# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/longest_common_subsequence.py
def lcs(x: str, y: str):
    m = len(x)
    n = len(y)

    L = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                match = 1
            else:
                match = 0

            L[i][j] = max(L[i - 1][j], L[i][j - 1], L[i - 1][j - 1] + match)

    seq = ""
    i, j = m, n
    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            match = 1
        else:
            match = 0

        if L[i][j] == L[i - 1][j - 1] + match:
            if match == 1:
                seq = x[i - 1] + seq
            i -= 1
            j -= 1
        elif L[i][j] == L[i - 1][j]:
            i -= 1
        else:
            j -= 1

    return L[m][n], seq

DISTANCE_HEURISTIC_WEIGHTS = np.array([
  2, # Binned alphabet distance
  1, # Word length
  -3, # LCS
  1, # Edit distance (levenshtein)
  2, # First char match
  2, # Last char match,
  -2  # Word frequency 
])

def searchBySymSpell(currentWord):
  global sym_spell
  suggestions = sym_spell.lookup(
    currentWord, Verbosity.CLOSEST, max_edit_distance=SYMSPELL_MAX_EDIT)
  # Give it some more breadth (for context implementation)
  # suggestions = suggestions + sym_spell.lookup(
  #   currentWord, Verbosity.ALL, max_edit_distance=2)
  # Current word by default
  output = currentWord
  shortestDistance = None
  # Tiebreak by least amount of characters added / removed
  bestCharDist = None
  matches = []
  freqSum = 0
  for suggestion in suggestions:
    freqSum += suggestion._count

  for suggestion in suggestions:
    lcsL, lcsSeq = lcs(currentWord, suggestion.term)
    # Heuristics (in order of priority):
    # Binned alphabet distance
    # Word length
    # LCS
    # Edit distance (levenshtein)
    # First char match
    # Last char match
    distances = np.array([
      binnedAlphabetDistance(currentWord, suggestion.term),
      abs(len(suggestion.term) - len(currentWord)),
      lcsL,
      suggestion.distance,
      0 if currentWord[0] == suggestion.term[0] else 1,
      0 if currentWord[-1] == suggestion.term[-1] else 1,
      suggestion._count / (freqSum * 1.0) * len(suggestions)
    ])
    matches.append((suggestion.term, distances))
    distance = np.sum(distances * DISTANCE_HEURISTIC_WEIGHTS)

    if shortestDistance == None or distance < shortestDistance:
      shortestDistance = distance
      output = suggestion.term

  return (matches, output)

def findMatchesAndWord(s):
  global timeTaken
  # dirty but lazy
  start = timer()
  result = None
  if CURRENT_SEARCH_ALGORITHM == SEARCH_ALGORITHM.UNSCRAMBLER:
    result = searchByUnscramble(s)
  if CURRENT_SEARCH_ALGORITHM == SEARCH_ALGORITHM.THE_FUZZ:
    result = searchByTheFuzz(s)
  if CURRENT_SEARCH_ALGORITHM == SEARCH_ALGORITHM.CLUSTERING:
    result = searchByClusteringOnly(s)
  if CURRENT_SEARCH_ALGORITHM == SEARCH_ALGORITHM.SYM_SPELL:
    result = searchBySymSpell(s)
  end = timer()
  timeTaken = end - start
  return result

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
  global timeTaken
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
  print("Time (s):", timeTaken)

def addWordThread(evt):
  try:
    wta = str(input('What is the word you would like to add?auto (CTRL+C to cancel) '))
    wta = wta.strip().lower()
    dicopen = open("DL.txt", "a")
    dicopen.write('\n')
    dicopen.write(wta)
    dicopen.close()
  except BaseException as e:
    # KeyboardInterrupt alone didn't work
    print("Cancelling operation...")
    pass

  # Tell main thread that it's done
  enabled = True
  currentWord = ""
  updateConsole(enabled, currentWord)
  print('Dictionary Updated.')
  evt.set()
  return

def initDict():
  global d
  global ind
  global wordCluster
  global sym_spell

  print('Preparing the dictionary...')
  if CURRENT_SEARCH_ALGORITHM == SEARCH_ALGORITHM.UNSCRAMBLER:
    d = GetDic()
    ind = Ints2Dic(d)
  if CURRENT_SEARCH_ALGORITHM == SEARCH_ALGORITHM.CLUSTERING:
    dic2Cluster(d)
  if CURRENT_SEARCH_ALGORITHM == SEARCH_ALGORITHM.SYM_SPELL:
    sym_spell = SymSpell(max_dictionary_edit_distance=SYMSPELL_MAX_EDIT)
    # https://symspellpy.readthedocs.io/en/latest/api/symspellpy.html#symspellpy.symspellpy.SymSpell.load_dictionary
    # sym_spell.create_dictionary("frequency_dictionary_en_82_765.txt")
    sym_spell.load_dictionary("frequency_dictionary_en_82_765.txt", 0, 1)

def main():
  global listener
  global currentWord
  global heldKeys
  global enabled
  global isAddingWord
  global capsLockActive
  global capitalizedArr
  global addWordEvent
  global snippets
  global timeTaken

  timeTaken = 0

  # Initialize dictionary
  initDict()

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
      # if (Key.ctrl_l not in heldKeys and 
      # Key.ctrl_r not in heldKeys):
      #   currentWord = currentWord[:-1]
      #   capitalizedArr = capitalizedArr[:-1]
      # else:
      # Just delete the full word
      currentWord = ""
      capitalizedArr = []
      updateConsole(enabled, currentWord)
    elif noCmdKeyIsHeld(heldKeys):
      # Ignore special command strokes
      char = str(key)[1:-1]
      if len(char) == 1 and char.isalpha():
        # Add character
        currentWord += char.lower()
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
          matches, output = findMatchesAndWord(currentWord)
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
    global enabled
    # print('on release', key)
    if key in heldKeys:
      heldKeys.remove(key)
    if key == Key.esc:
      if (Key.shift in heldKeys or 
      Key.shift_r in heldKeys):
        # Exit
        return False
      else:
        enabled = not enabled
        updateConsole(enabled, currentWord)

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
      initDict()
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
      # if len(currentWord) <= 0:
      #   enabled = not enabled
      # updateConsole(enabled, currentWord)
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
