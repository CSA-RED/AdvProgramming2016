'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
#####
Rylan Denis
Mr. Davis
Hangman
11/17/2016
Adv. Comp. Prog.
'''

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random

allPasswords=["BORNINTHEUSA","USUCKATHACKING","NICETRYNERD","FBIISBETTERTHANCIA","THECIAARENERDS","DOUBLEHACKINGKEYBOARDS"]
allHints=["The secret ending of Hotline Miami","Insult your skills","Sarcastic congratulations","Insult to your company","Thrown shade at your job","Essential hacking equipment"]
errorCounter=0
usePass=""
lose=False #accounts for all game end scenarios
allTriesGUI=['''



     -------
     | ___ |
     | | | |
     | |_| |
     |_____|''','''


     |
     -------
     | ___ |
     | | | |
     | |_| |
     |_____|''','''
     /
     |
     |
     -------
     | ___ |
     | | | |
     | |_| |
     |_____|''','''
     /-----
     |
     |
     -------
     | ___ |
     | | | |
     | |_| |
     |_____|''','''
     /-----\\
     |     |
     |
     -------
     | ___ |
     | | | |
     | |_| |
     |_____|''','''
     /-----\\
     |     |
     |     |
     -------
     | ___ |
     | | | |
     | |_| |
     |_____|
    GAME OVER''']

def about():
    messagebox.showinfo(title="About",message="Version .1\nAuthor: Rylan Denis\n\nYou are brand new at the CIA, but a new lead on the whereabouts of the elusive hacker Joshua Carrillo may be just the break you're looking for. Try to find the code that will break his firewalls and show you where he is, but watch out! If you fail too many times, he'll get away.")  # Gives user the version number

def instructions():
    messagebox.showinfo(title="Instructions",message="Using the entry box, input a single letter to guess for the password and hit submit. If the letter is in the password, it will show up; however, if it isn't, Joshua will take notice and tighten his security.")

def passwordSet():
    global realLetList,usePass
    thisPass=random.choice(allPasswords)
    usePass=""
    for i in thisPass:
        usePass+="_ "
        realLetList.append(i)
    passVar.set(usePass)
    counter=0
    for i in allPasswords:
        if thisPass==i:
            break
        else:
            counter+=1
    hintVar.set(allHints[counter])

def setLettersChecked():
    let=""
    for i in guessedLetters:
        let+=i+" "
    allAttempts.config(state="normal")
    allAttempts.delete('1.0',END)
    allAttempts.insert('1.0',let)
    allAttempts.config(state="disabled")

def setGUI():
    hangmanIcon.config(state="normal")
    hangmanIcon.delete('1.0',END)
    hangmanIcon.insert('1.0',allTriesGUI[errorCounter])
    hangmanIcon.config(state="disabled")

def endGameFail():
    global lose
    result.set("GAME OVER: Joshua noticed your hacking attempts, and his new encryptions are too complex...")
    submitBtn.state(["disabled"])
    guessEntry.config(state="disabled")
    guessVar.set("")
    lose=True

def endGameWin():
    global lose
    result.set("YOU WIN: You've successully hacked into Joshua's database, allowing the CIA to track his location. The CIA applauds you.")
    submitBtn.state(["disabled"])
    guessEntry.config(state="disabled")
    guessVar.set("")
    lose=True

def failedGuess():
    global errorCounter
    result.set("Incorrect guess! Security is getting tighter...")
    setLettersChecked()
    errorCounter+=1
    setGUI()
    guessVar.set("")
    if errorCounter>=5:
        errorCounter=4
        endGameFail()

def updateProgress():
    realLets=''.join(realLetList)
    uniqueChars=''.join(set(realLets))
    total=int((float(len(correctLetters))/float(len(uniqueChars)))*100)
    bar.config(value=total)
    decryptProgVar.set("Decrypt at:\n"+str(total)+"%")

def updatePassword():
    wholePass=passVar.get().split()
    allLet=realLetList
    for i in correctLetters:
        passIndex=[]
        passCount=0
        for l in allLet:
            if l==i:
                passIndex.append(passCount)
            passCount+=1
        for c in passIndex:
            wholePass[c]=i
    newPass=""
    for i in wholePass:
        newPass+=i+" "
    passVar.set(newPass)
    updateProgress()

def correctGuess():
    result.set("Correct guess! You're getting closer to cracking the code...")
    setLettersChecked()
    updatePassword()
    guessVar.set("")
    if "_" not in passVar.get():
        endGameWin()

def guessCheck():
    if guessVar.get() in guessedLetters:
        result.set("ERROR: You've already guessed this letter!")
    else:
        if guessVar.get() in realLetList:
            guessedLetters.append(guessVar.get())
            correctLetters.append(guessVar.get())
            correctGuess()
        else:
            guessedLetters.append(guessVar.get())
            failedGuess()

def submit(*args):
    if lose==False:
        result.set("")
        if guessVar.get() == "":
            result.set("ERROR: Must enter a guess before submitting")
        elif len(guessVar.get())!=1:
            result.set("ERROR: Guess must be one letter.")
        else:
            try:
                int(guessVar.get())
            except ValueError:
                guessVar.set(guessVar.get().upper())
                guessCheck()
                pass
            else:
                result.set("ERROR: Guess must be a letter.")

root = Tk()
root.title("Hackerman")
root.option_add("*tearOff", FALSE) #removes tearoffs from menus

mainframe = ttk.Frame(root, padding="3 3 12 12")
attempted = ttk.Frame(mainframe, borderwidth=5, width=100, height=100, relief="sunken", padding="4 4 15 15")
attempted.grid(column=0,row=0,sticky=(N,S,E,W))
progress = ttk.Frame(mainframe, borderwidth=5, width=100, height=100, relief="sunken", padding="4 4 15 15")
progress.grid(column=1,row=0,sticky=(N,S,E,W))
hintBox = ttk.Frame(mainframe, borderwidth=5, width=100, height=100, relief="sunken", padding="4 4 15 15")
hintBox.grid(column=0,row=2,columnspan=3,sticky=(N,S,E,W))
passBox = ttk.Frame(mainframe, borderwidth=5, width=100, height=100, relief="sunken", padding="4 4 15 15")
passBox.grid(column=0,row=3,columnspan=3,sticky=(N,S,E,W))
submitBox = ttk.Frame(mainframe, borderwidth=5, width=100, height=100, relief="sunken", padding="4 4 15 15")
submitBox.grid(column=0,row=4,columnspan=3,sticky=(N,S,E,W))
resultBox = ttk.Frame(mainframe, borderwidth=5, width=100, height=100, relief="sunken", padding="4 4 15 15")
resultBox.grid(column=0,row=1,columnspan=3,sticky=(N,S,E,W))
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

menu=Menu(root)
root.config(menu=menu)

fileMenu=Menu(menu)
helpMenu=Menu(menu)
menu.add_cascade(label="File",menu=fileMenu)
menu.add_cascade(label="Help",menu=helpMenu)
fileMenu.add_command(label="Exit", command=root.quit)
helpMenu.add_command(label="About", command=about) #option to see about messagebox
helpMenu.add_command(label="Instructions", command=instructions) #option to see instruction messagebox

#variables
decryptProgVar=StringVar()
hintVar=StringVar()
passVar=StringVar()
guessVar=StringVar()
result=StringVar()
realLetList=[]
guessedLetters=[]
correctLetters=[]

#widgets
attemptedLabel=ttk.Label(attempted,text="Attempted Decrypts:")
allAttempts=Text(attempted,width=25,height=8,state="disabled")
bar=ttk.Progressbar(progress, orient=VERTICAL, length=151, mode='determinate')
progLabel=ttk.Label(progress,textvariable=decryptProgVar)
hangmanIcon=Text(mainframe,width=25,height=10,state="disabled")
hintLabel=ttk.Label(hintBox,text="Hint:")
hint=ttk.Entry(hintBox,width=100,state="disabled",textvariable=hintVar)
passLabel=ttk.Label(passBox,text="Password:")
passw=ttk.Label(passBox,textvariable=passVar)
guessLabel=ttk.Label(submitBox,text="Your Guess:")
guessEntry=ttk.Entry(submitBox,width=1,textvariable=guessVar)
submitBtn=ttk.Button(submitBox,text="Submit Decrypt",command=submit)
resultLabel=ttk.Label(resultBox,textvariable=result)

#grid
attemptedLabel.grid(column=0,row=0,sticky=(N,E,W))
allAttempts.grid(column=0,row=1,sticky=(N,E,W,S))
bar.grid(column=0,row=0,sticky=(N,W,S))
progLabel.grid(column=1,row=0,sticky=(N,W,E))
hangmanIcon.grid(column=2,row=0,sticky=(N,S,E,W))
hintLabel.grid(column=0,row=0,sticky=(N,S,E,W))
hint.grid(column=1,row=0,rowspan=2,sticky=(N,S,E,W))
passLabel.grid(column=0,row=0,sticky=(N,S,E,W))
passw.grid(column=1,row=0,columnspan=2,sticky=(N,S,E,W))
guessLabel.grid(column=0,row=0,sticky=(N,S,E,W))
guessEntry.grid(column=0,row=1,sticky=(N,S,E,W))
submitBtn.grid(column=1,row=1,columnspan=3,sticky=(N,S,E,W))
ttk.Label(submitBox,text="											                                    ").grid(column=0,row=2,columnspan=4,sticky=(N,S,E,W))
resultLabel.grid(column=0,row=0,columnspan=3,sticky=(N,S,E,W))
ttk.Sizegrip(root).grid(column=999, row=999, sticky=(S,E))

#weight fix
root.grid_columnconfigure(0,weight=1)
root.grid_rowconfigure(0,weight=1)
mainframe.columnconfigure(0, weight=3)
mainframe.columnconfigure(1, weight=3)
mainframe.columnconfigure(2, weight=3)
mainframe.columnconfigure(3, weight=3)
mainframe.rowconfigure(0, weight=3)
mainframe.rowconfigure(1, weight=3)
mainframe.rowconfigure(2, weight=3)
mainframe.rowconfigure(3, weight=3)
mainframe.rowconfigure(4, weight=3)

for child in mainframe.winfo_children(): child.grid_configure(padx=7, pady=7)
for child in attempted.winfo_children(): child.grid_configure(padx=3, pady=3)
for child in progress.winfo_children(): child.grid_configure(padx=3, pady=3)
for child in hintBox.winfo_children(): child.grid_configure(padx=3, pady=3)
for child in passBox.winfo_children(): child.grid_configure(padx=3, pady=3)
for child in submitBox.winfo_children(): child.grid_configure(padx=3, pady=3)

decryptProgVar.set("Decrypt at:\n0%")
passwordSet()
setGUI()

root.bind('<Return>',submit)
guessEntry.focus()
root.mainloop()