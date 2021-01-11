from tkinter import *
from tkinter import messagebox
import random
from PIL import Image, ImageTk

#####FUNCTIONS

def clear():
    serviceVar.set('')
    userVar.set('')
    passVar.set('')
    scoreGenerate(passVar.get())
            
def retrieve():
    global services, passwords, usernames
    service = serviceVar.get()
    service=service.upper()
    if service in services:
        username=usernames[services[service]]
        password = passwords[services[service]]
        passEntry.delete(0,END)
        passEntry.insert(0,password)
        userEntry.delete(0, END)
        userEntry.insert(0,username)
        scoreGenerate(password)
    else:
        retrieveErrorMessage()

def savePass():
    global n, services, passwords, usernames
    newServ=serviceVar.get()
    newServ=newServ.upper()
    newPass=passVar.get()
    newUser=userVar.get()
    if newPass != '' and newServ != '' and newUser != '':
        if newServ not in services:
            
            passwords.append(newPass)
            usernames.append(newUser)
            services[newServ]=n+1
            serviceVar.set('')
            userVar.set('')
            passVar.set('')
            n+=1
            if len(services) > 1:
                serviceListVar.set(f'{serviceListVar.get()}, {newServ}')
            else:
                serviceListVar.set(newServ)
        elif newServ in services and (newPass not in passwords or newUser not in usernames):
            ans=messagebox.askquestion('Account already exists', 'You already have an account saved for this service, would you like to replace it?', icon='warning')
            if ans=='yes':
                passwords[services[newServ]]=newPass
                usernames[services[newServ]]=newUser
            else:
                pass
            
            serviceVar.set('')
            userVar.set('')
            passVar.set('')
        else:
            serviceVar.set('')
            userVar.set('')
            passVar.set('')
    else:
        messagebox.showinfo("Empty Entries", "You have not completed every required field.", icon="warning")
    scoreGenerate(passVar.get())
    
def showLists():
    listVar.set(f'{services}, {usernames}, {passwords}, {letters}')

def scoreGenerate(password):
    totalScore=0
    totalScore=checkLength(password) + checkSymbols(password) + checkNumbers(password) - checkConsecutiveLower(password)
    scoreVar.set(totalScore)
    scaleColour()
    
def score(event):
    c=event.char
    p=passVar.get()
    if c == '':
        pass
    elif c in letters or c in nums or c in symbs:
        password=f'{p}{c}'
        totalScore=0
        totalScore=checkLength(password) + checkSymbols(password) + checkNumbers(password) - checkConsecutiveLower(password)
        scoreVar.set(totalScore)
    elif ord(c) == 8:
        password=f'{p[0:-1]}'
        totalScore=0
        totalScore=checkLength(password) + checkSymbols(password) + checkNumbers(password) - checkConsecutiveLower(password)
        scoreVar.set(totalScore)
    scaleColour()

def checkLength(password):
    lengthScore=0
    lengthScore=len(password)*4
    return lengthScore

def checkSymbols(password):
    numSymbols=0
    for i in password:
        if i in symbs:
            numSymbols+=1
    return numSymbols*6

def checkNumbers(password):
    numCount=0
    for i in password:
        if i in nums:
            numCount+=1
    return numCount*2

def checkConsecutiveLower(password):
    x=0
    for i in range (len(password)):
        if i==len(password)-1:
            pass
        elif password[i].islower() == True:
            if password[i+1].islower() == True:
                x+=1
        elif password[i].isupper() == True:
            if password[i+1].isupper() == True:
                x+=1
    return x*2

def generatePass():
    passVar.set('')
    newPass=''
    for i in range(5):
        newPass+=random.choice(letters)
        newPass+=random.choice(symbs)
        newPass+=random.choice(nums)
    passVar.set(newPass)
    scoreGenerate(newPass)

def scaleColour():
    totalScore=scoreVar.get()
    colour=''
    if totalScore==100:
        colour="#009900"
    elif totalScore > 74:
        colour="#99FF33"
    elif totalScore > 49:
        colour="#FFCC00"
    elif totalScore > 24:
        colour="#FF6600"
    else:
        colour="#FF0000"
    scoreScale.config(troughcolor=colour)

def helpMe(event):
    messagebox.showinfo("Help", "You must enter an entry for each field to save a password to the database.\nAccounts are saved by service name, so entering the service name and clicking \"Retrieve\" will retrieve your account info from the database.\nThe Generate button will create a 100 point scored password.\nClear will empty all entries. Please use this button instead of clicking and dragging.")

def retrieveErrorMessage():
    messagebox.showinfo("Retrieval Error", "Oops! Looks like we don't have an account from that service saved for you! Make sure the service entry is filled in correctly.")

#######MAIN

root=Tk()
root.config(bg="#33CCCC")
mainframe=Frame(root)

global n, services, passwords, usernames
services={}
passwords=[]
usernames=[]
n=-1

letters=[]
for i in range(65,91,1):
    letters.append(chr(i))
for i in range(97,123,1):
    letters.append(chr(i))

symbs=[]
for i in range(32,48,1):
    symbs.append(chr(i))
for i in range(57,65,1):
    symbs.append(chr(i))

nums=[]
for i in range(48,58,1):
    nums.append(chr(i))

infoImg=Image.open("info.jpg").resize((20,20))
infoPhoto=ImageTk.PhotoImage(infoImg)
infoLabel=Label(mainframe, image=infoPhoto)
infoLabel.image = infoPhoto
infoLabel.bind("<Button-1>", helpMe)

titleLabel=Label(mainframe, text='Password Manager', font=("Courier, 20"))

serviceLabel=Label(mainframe, text='Service')
serviceVar=StringVar()
serviceEntry=Entry(mainframe, text='', width=50, textvariable=serviceVar)

userLabel=Label(mainframe, text='Username')
userVar=StringVar()
userEntry=Entry(mainframe, text='', width=50, textvariable=userVar)

passLabel=Label(mainframe, text='Password')
passVar=StringVar()
passEntry=Entry(mainframe, text='', width=50, textvariable=passVar)
passEntry.bind("<Key>", score)
storePassVar=StringVar()


scoreVar=IntVar()
scoreVar.set(0)
scoreScale=Scale(mainframe, variable=scoreVar, from_=0, to=100, orient=HORIZONTAL, length=200, troughcolor="red")

generateButton=Button(mainframe, text='Generate', command=generatePass)

saveButton=Button(mainframe, text='Save', command=savePass)

retrieveButton=Button(mainframe, text='Retrieve', command=retrieve)

clearButton=Button(mainframe, text='Clear', command=clear)

helpButton=Button(mainframe, text='Help', command=helpMe)

servicesFrame=Frame(root)
serviceTitleLabel=Label(servicesFrame, text='Services saved')
serviceListVar=StringVar()
serviceListLabel=Label(servicesFrame, text='', textvariable=serviceListVar, justify=CENTER, wraplength=421)

ruleframe=Frame(root)
ruleLabel=Label(ruleframe, text="Your password should include:\n -a mix of lowercase and uppercase letters\n -numbers and symbols", fg="#009900")

ruleLabel2=Label(ruleframe, text="Points will be deducted for consecutive lowercase or uppercase letters (-2 each)", fg="#FF0000")



#######GRID

root.minsize(width=250, height=400)
root.maxsize(width=1920, height=1080)
mainframe.grid(padx=50, pady=50, row=1, column=1, rowspan=2)


ruleframe.grid(padx=50, pady=50, row=1, column=2)
ruleLabel.grid()
ruleLabel2.grid()

servicesFrame.grid(row=2, column=2)
serviceTitleLabel.grid(row=1, column=2, columnspan=3, padx=170)
serviceListLabel.grid(row=2, column=2, columnspan=3)

titleLabel.grid(row=1, columnspan=6, column=1)
serviceLabel.grid(row=2, column=1)
serviceEntry.grid(row=2, columnspan=4, column=2)
userLabel.grid(row=3, column=1)
userEntry.grid(row=3, columnspan=4, column=2)
passLabel.grid(row=4, column=1)
passEntry.grid(row=4, columnspan=4, column=2)
scoreScale.grid(row=5, columnspan=4, column=2)
generateButton.grid(row=6, column=1, pady=20, padx=20)
saveButton.grid(row=6, column=2)
retrieveButton.grid(row=6, column=3)
clearButton.grid(row=6, column=4)
infoLabel.grid(row=6, column=5)
