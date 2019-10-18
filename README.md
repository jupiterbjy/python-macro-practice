# Introduction
Noob's attempt on language he never learned about.

In short, this script will read off from .txt file which contains macro actions. But currently only supports image-search based macros, no 'wait' or 'keypress' kinda things yet. Will eventually be implemented when I'm out of army. Got motif from android app 'Frep' by strai.

Create onefile with pyinstaller from MacroLoader.py & TemplateImageGenerator.py And you're good to go.

Will complete Readme section when I have time to put GUI on this script.

Example of usage: https://youtu.be/_ichOg5tf8Y


# File explanation

Details are provided in comments inside each scripts.

**OneFilePathDetector.py**: Set working directory to .exe even when onefile argument was used to create it.
Include this to your project and use function DetectFrozen() to set working directory automatically.

**ImgWrapper.py**: Wrapper around cv2, which provides various macro-ready functions like scanning occurance, search image in area, etc.
Include this for ease of life when creating macro like this yourself. Might need to cleanup a bit later.

**TemplateImageGenerator.py**: Created this after seeing Win10's win+shift+s function breaks. This does similar job, by creating image file where you've pointed while pressing 'f2' key. You can see how this works from youtube link above - Appears for first few seconds.

**MacroLoader.py**: Main macro module, useless outside of this macro for sure. Will generate global coordination variables and load up .txt file you've typed.

**KillProcess.py**: Just provides some text and countdown or key-press requirement before killing scrips. You'll need time to copy console output before complaining to me "This doesn't work!", so this exists.