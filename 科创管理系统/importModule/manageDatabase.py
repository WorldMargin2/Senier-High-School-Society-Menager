from sqlite3 import connect as dbconnect





DATABASEPATH="./database/"
APPDATAPATH="./database/AppData/"
SOCIETYDATABASEPATH="./database/SocietyDatabase/"
HISTORYPATH="./database/SocietyDatabase/history/"
#=====================================================
def getAppInfo(keytext):
    with dbconnect(f"{APPDATAPATH}appdata.db") as db:
        cs=db.cursor()
        cs.execute("select valuetext,typetext from KeyValue where keytext = ?",(keytext,))
        info=cs.fetchone()
        cs.close()
        return(info)
    
def writeAppdata(keytext,valuetext,typetext="str"):
    with dbconnect(f"{APPDATAPATH}appdata.db") as db:
        cs=db.cursor()
        cs.execute("select * from KeyValue where keytext=?",(keytext,))
        if(cs.fetchone()):
            cs.close()
            return(False)
        cs.execute("insert into KeyValue(keytext,valuetext,typetext)"
            " values (?,?,?)",
            (keytext,valuetext,typetext)
        )
        cs.close()
        return(True)

def changeAppdata(keytext,valuetext,typetext="str"):
    with dbconnect(f"{APPDATAPATH}appdata.db") as db:
        cs=db.cursor()
        cs.execute("select * from KeyValue where keytext=?",(keytext,))
        if(cs.fetchone()):
            cs.execute("update KeyValue set valuetext=? typetext=? where keytext=?",(valuetext,typetext,keytext))
            cs.close()
            return(True)
        cs.close()
        writeAppdata(keytext,valuetext,typetext)
        return(False)

def CreateAppdatabase():
    with dbconnect(f"{APPDATAPATH}appdata.db") as db:
        cs=db.cursor()
        cs.execute("create TABLE IF NOT EXISTS KeyValue("
            "keytext text PRIMARY KEY,"
            "valuetext text,"
            "typetext text"
        ")")
        writeAppdata("SuperOprationId","202101","int")
        writeAppdata("SuperOprationPassword","202101","int")
        writeAppdata("NowGrade","21","int")
        cs.close()

#=====================社团数据库操作相关================================
def getNowGrade():    
    return(getAppInfo("NowGrade")[0])

def getSocietyDataBase():
    return(f"{getNowGrade()}.db")

def getGrades():
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select grade from grades")
        grades=cs.fetchall()
        cs.close()
        return(grades)

def getYearByGrade(grade):
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select year from grades where grade = ?",(grade))
        year=cs.fetchone()
        cs.close()
        return(year)

def getGradeById(Userid):
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select grade from Menber where userid=?",(Userid,))
        grade=cs.fetchone()
        cs.close()
        return(grade)

def getMembers():
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        dictList=[]
        cs.execute("select userid,name,class,grade,position,department,contactstyle from Member")
        keys=("userid","name","class","grade","position","department","contactstyle")
        for i in cs.fetchall():
            dictList.append(dict(zip(keys,i)))
        return(dictList)

def getIdByYear(year):    
    Maxid=f"20{year}999"
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select userid from Member where userid<?",(int(Maxid),))
        idList=cs.fetchall()
        cs.close()
        return(idList)

def findFreeId(IdList,year,number):
    resault=[]
    startId=int(f"20{year}001")
    maxId=max(IdList)
    for i in range(startId,maxId):
        if((not (i in IdList)) and (len(resault)<number)):
            resault.append(i)
    if(not len(resault)==number):
        list(range(maxId+1,maxId+(number-len(resault))+1)).extend(resault)
    return(resault)

def getFreeId(year,number):
    if(not len(getIdByYear(year))):
        start=int(f"20{year}001")
        return(list(range(start,start+number)))    
    return(findFreeId(getIdByYear(year),year,number))

def getPermission(userId):
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select permission from oprations where oprationID=?",(int(userId),))
        permission=cs.fetchone()
        cs.close()
        return(permission)

def getPermissionById(userId):
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select permission where oprationID=?",(int(userId),))
        permission=cs.fetchone()
        cs.close()
        return(permission)

def getOprationInfoById(userid):
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select password from oprations where oprationID=?",(int(userid),))
        info=cs.fetchone()
        cs.close()
        if(info):
            return(True,info)
        return(False,None)

def assignId(grade):
    pass


"""======================================================="""
def CreateSocietyDatabase(Grade=None):
    if(not Grade):
        Grade=int(getNowGrade())
    with dbconnect(f"{SOCIETYDATABASEPATH}{Grade}.db") as db:
        cs=db.cursor()
        cs.execute("CREATE TABLE IF NOT EXISTS  Member("
                "userid integer PRIMARY KEY,"
                "name text NOT NULL,"
                "class TEXT NOT NULL default 1,"
                "grade TEXT NOT NULL default 0,"
                "position INTEGER NOT NULL default 0,"
                "department TEXT NOT NULL,"
                "contactStyle text default NULL"
            ")"
        )

        cs.execute("create table if not exists oprations("
                "oprationID int primary key,"
                "password text,"
                "permission int default 0"
            ")"
        )

        cs.execute("create table if not exists positions("
                "posision int primary key,"
                "description text"
            ")"
        )
        
        cs.execute("create table if not exists grades("
                "grade int primary key,"
                "year int"
                "description text"
            ")"
        )

        cs.execute("create table if not exists departments("
                "departmentId int primary key,"
                "description text"
            ")"
        )

        cs.execute("create table if not exists permissions("
                "permissionId int primary key,"
                "description text"
            ")"
        )
        cs.close()




#===========================================================

    

if(__name__=="__main__"):
    print(getAppInfo("SuperOprationId"))
    print(getAppInfo("SuperOprationPassword"))
    print(getAppInfo("NowGrade"))
    print(getFreeId(21,20))
    CreateSocietyDatabase(21)
    
