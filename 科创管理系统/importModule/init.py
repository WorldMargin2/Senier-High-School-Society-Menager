import os
from random import randint
from importModule.initialName import initialNames
from importModule.manageDatabase import CreateSocietyDatabase, addMember ,CreateAppdatabase
from importModule.manageDatabase import DATABASEPATH,APPDATAPATH,HISTORYPATH,SOCIETYDATABASEPATH




def initDirectory():
    print("init path")
    if(not os.path.isdir(HISTORYPATH)):
        os.makedirs(HISTORYPATH)
    if(not os.path.isdir(APPDATAPATH)):
        os.makedirs(APPDATAPATH)

def initDataBase(grade=21):
    print("init database")
    if(not os.path.exists(f"{APPDATAPATH}appdata.db")):
        CreateAppdatabase()
    if(not os.path.exists(f"{SOCIETYDATABASEPATH}{grade}.db")):
        CreateSocietyDatabase(grade)
        names=initialNames.splitlines()
        if("" in names):
            names.remove("")
        addMember([{"name":i,"grade":21,"userclass":randint(1,30)} for i in names])



