# Stenography for the Layman

## Introduction
This is an experimental python project that allows you to type faster and more comfortably by borrowing ideas from Stenography.

One of the reasons [stenography](https://www.youtube.com/watch?v=UA6UythLlEI) allows you to type faster by pressing multiple keys at once (this is called chording). However, Stenography is difficult to learn and even harder to master ([it can take approximately 3 - 6 months to reach ~40 WPM using stenography](https://didoesdigital.com/typey-type/support)) as you have to relearn the keyboard layout, steno theory & the shorthands (briefs). This means that Stenography has a very high barrier to entry for the layman.

The layman is familiar with QWERTY / whatever keyboard layout they use. Thus, for the layman's use-case, we should adapt some concepts from stenography without changing the layout of the keyboard to achieve faster typing speeds and better typing quality of life.

This project allow users to type multiple characters, even out of order. Once a user is satisfied, they can input a whitespace character. This then becomes a [word unscrambling problem](https://wordunscrambler.me/). One can then unscramble the words (e.g. with [this](https://github.com/tinmarr/Word-Unscrambler)). Due to the nature of the implementation, it works not only for QWERTY, but also to other keyboard layouts like DVORAK.
- To deal with typos and anagrams, we can use [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) and pick the option closest to the input from the user. While this means that users should not input words *entirely* out of order, it allows them to implicitly select the option they have in mind without a GUI, improving the workflow.

Limitations:
- The number of keys you can press simultaneously may be limited by your [keyboard hardware](https://en.wikipedia.org/wiki/Rollover_(keyboard)).
- Windows only (can be extended to other OSes)
- Documentation for setting up the project is limited as it's still a WIP. But app works fine
- the implementation is somewhat technical and there is no exe yet (it's all python files).

## Motivation (verbose)
- Have you ever watched a video on someone typing 200+ WPM with stenography and went "Holy shit, I want to do that too!"?
- Perhaps in your enthusiasm you hopped onto the open source stenography project [Plover](https://github.com/openstenoproject/plover) , installed it, played around with it, and then realized something: it was hard-as-balls to use.
	- There aren't even enough keys to fit all the alphabets of the English language onto a stenographer keyboard, so some alphabets have to be represented by multiple keys. 'L' is represented by 'HR'. 'G' is represented by 'TPKW'. And that's just the left hand, which is used for the front of the word. You have another set of things to learn for the vowels and the back of the word, and that's just the keyboard layout.
	- So basically, you got to relearn QWERTY, but with half the number of buttons.
- A little more Googling and you find out that it can take approximately *3 - 6 months* to reach ~40 WPM using stenography ([src](https://didoesdigital.com/typey-type/support)). In comparison, your typing speed with a QWERTY keyboard can be from around 40-70 WPM or even higher depending on your proficiency. Aspiring stenographers spend *2 years* of their life just to learn how to type this thing (albeit graduating at a wack speed of 225 WPM).
- What that means is that you have to spend at least 3 - 6 months learning this thing, which is not just a new keyboard layout, but also what is arguably a new language altogether, since stenography is full of shortcuts called "briefs". These shortcuts allow you to type words and phrases that aren't intuitively based on the characters you actually press.
- Stenographers need that speed for transcribing text, but the layman doesn't; it's good enough if they get a small improvement, better still if you can achieve that without relearning the keyboard. Maybe you already know how to touch type on the keyboard and you're just looking to make your typing speed faster without having to go through the hassle.
- This is a tool designed for people for you.

## Why stenography is faster
- Stenography is faster than typing on a keyboard for a variety of reasons:

1. The layout is a lot more compact, so the fingers don't have to travel much.
2. Words are typed by pressing multiple buttons at once (this is called chording), or chaining these chords together for more complicated words. This means less time waiting for characters to be typed.
3. There are *a lot* of shorthand, which allow common words to be quickly typed using a chord or two.

These factors result in a much higher typing speed, but also create a very high barrier to entry for stenography. 

## Borrowing ideas from stenography to make typing on QWERTY faster

The strategy to improving typing speed and quality of life for the average layman is to leverage on their prior experience of typing on keyboards and reduce the amount of re-learning required. 

This tool aims to provide keyboard users access to point (2). This means that we trade some speed & comfort benefits in exchange for a much lower barrier to entry.

The idea is simple: 
1. Allow the user to press multiple buttons on the keyboard at the same time (this will depend on whether your keyboard can support [that](https://en.wikipedia.org/wiki/Rollover_(keyboard))). The input will be scrambled. We assume that the characters of the word is all there, but scrambled. 
2. We assume that the user wants to move on to the next word only upon pressing a space / enter / non-alphabet. 
	1. This allows him to input more characters if necessary (e.g. multiples of the same character like "allow"), or even type the characters normally so that he can improve his pace at his own speed, or even find a few optimizations on his own.
3. What we're left with is a group of words which are unordered. This is essentially a [word unscrambling problem](https://wordunscrambler.me/). One can then unscramble the words (e.g. with [this](https://github.com/tinmarr/Word-Unscrambler)).
4. If the unordered words form an [anagram](https://en.wikipedia.org/wiki/Anagram) (i.e. more than 1 solution), then we display a list of solutions to the user to choose from. However, since the application does not have a GUI yet, the options are sorted by most similar to the original input (by Levenshtein distance), and the closest option is returned.
6. At this stage, the tool only converts exact matches. Inputs with typos are not handled. If there are no matches found, it will just return the input with typo as-is without any conversion. 

Supplementing the tool to provide the benefit offered by point (3) would require an auto-complete / recommender system, which is a little more involved. There are no plans to implement that as this was developed as an exploration tool.

## Operating the tool
- The objective of the tool is to retain the same feel that typing confers, but allow the user to press multiple keys are the same time.
- Usage flow:
	- When the tool is enabled, anything typed will be collected by the tool and not actually output to the text field.
	- Backspace / CTRL+Backspace will modify what was typed if there is content that is not yet output. Otherwise it will behave normally.
	- Pressing space, tab, enter or inputting any non alphabetical symbols will trigger the unscrambling process.
	- If the input is an anagram, the user will be shown a list of options which they can select by typing a character (representing the word on the left). Note that this list is ordered based on the similarity of the word to the input.
- Commands:
	- CTRL + SPACE: Enable / Disable the tool.
  - CTRL + SHIFT + SPACE: Add a new word to the dictionary.
  - ESC: Stop the program.
- Other notes & design considerations:
	- Pressing backspace removes previously input characters (ctrl + backspace removes the whole thing).
- KIV (unimplemented features):
	- SHIFT + SPACE: If there is currently no ongoing word, swap the space mode. Otherwise, swaps the space mode only for the next word. 
  - capitalization management: handle & monitor the state of the shift / capslock key accordingly.
  There are the following modes:
		- Add space (default): Pressing space will trigger the unscrambling process. Afterwhich, a space is added to the end of the word.
		- No spacing: Pressing space will trigger the unscrambling process. Afterwhich, no space is added to the end of the word.
    - If the word is an anagram, the shown options will be selectable by alphabets instead of numbers (to reduce hand movement). These options are sorted based their similarity to the original input.
	  - Words immediately after a symbol will not be capitalized. Conversely, words after a symbol and a space will be auto-capitalized.
	  - When inputting characters, characters that were capitalized during input will remain capitalized. 

## Implementation (Windows)
- pyWinHook & pynput for monitoring and sending keypresses
	- Installing pyWinHook requires [swig.exe](https://sourceforge.net/projects/swig/) to be in your PATH environment variable.
- tkinter for displaying text (KIV)
