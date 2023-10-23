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
def addMember(memberDicts:list):
    for memberDict in memberDicts:
        memberDict:dict
        name=memberDict.get("name",None)
        grade=memberDict.get("grade",0)
        userid=getOneFreeId(grade)
        with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:  
            cs=db.cursor()
            cs.execute("insert into Member(userid,name) values(?,?)",(userid,name))
            cs.close()


def getNowGradeinYear():
    return(getAppInfo("NowGrade")[0])

def assignYearForGrade(benchmark:int=2,grades:dict={}):
    pass

def getSocietyDataBase():
    return(f"{getNowGradeinYear()}.db")

def getGrades():
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select grade from grades")
        grades=cs.fetchall()
        cs.close()
        return(grades)

def getYearByGrade(grade:int):
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select year from grades where grade = ?",(grade))
        year=cs.fetchone()
        cs.close()
        return(year[0])

def getGradeById(Userid:int):
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select grade from Member where userid=?",(Userid,))
        grade=cs.fetchone()
        cs.close()
        return(grade[0])

def getMembers():
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        dictList=[]
        cs.execute("select userid,name,class,grade,position,department,contactstyle from Member")
        #         ("userid","name","class","grade","position","department","contactstyle")
        keys=getKeyWords()
        for i in cs.fetchall():
            dictList.append(dict(zip(keys,i)))
        return(dictList)

def getIdByYear(year:int):    
    Maxid=f"20{year}999"
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select userid from Member where userid<?",(int(Maxid),))
        idList=list(i[0] for i in cs.fetchall())
        cs.close()
        return(idList)

def findFreeId(IdList:list,year:int,number:int):
    resault=[]
    startId=int(f"20{year}001")
    maxId=max(IdList)
    for i in range(startId,maxId):
        if((not (i in IdList)) and (len(resault)<number)):
            resault.append(i)
    if(not len(resault)==number):
        list(range(maxId+1,maxId+(number-len(resault))+1)).extend(resault)
    return(resault)

def findOneFreeId(IdList:list,year:int):
    startId=int(f"20{year}001")
    maxId=max(IdList)
    for i in range(startId,maxId):
        if((not (i in IdList))):
            return(i)

def getFreeId(year:int,number:int):
    if(not len(getIdByYear(year))):
        start=int(f"20{year}001")
        return(list(range(start,start+number)))    
    return(findFreeId(getIdByYear(year),year,number))

def getOneFreeId(year:int):
    if(not len(getIdByYear(year))):
        return(int(f"20{year}001"))
    return(findOneFreeId(getIdByYear(year),year))
#===============获取关键信息描述=====================
def getPermissionInfo()->dict:
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        permission=dict()
        cs.execute("select permissionId,description from oprations")
        for i in cs.fetchall():
            permission[i[0]]=i[1]
        cs.close()
        return(permission)
    
def getGradeInfo()->dict:
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        grade=dict()
        cs.execute("select grade,description from grades")
        for i in cs.fetchall():
            grade[i[0]]=i[1]
        cs.close()
        return(grade)

def getDepartmentInfo()->dict:
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        department=dict()
        cs.execute("select departmentId,description from departments")
        for i in cs.fetchall():
            department[i[0]]=i[1]
        cs.close()
        return(department)

def getPositionInfo()->dict:
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        position=dict()
        cs.execute("select position,description from positions")
        for i in cs.fetchall():
            position[i[0]]=i[1]
        cs.close()
        return(position)
#=================================================
def getPermissionById(userId:int):
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select permission where oprationID=?",(int(userId),))
        permission=cs.fetchone()
        cs.close()
        return(permission[0])

def getOprationInfoById(userid:int):
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select password from oprations where oprationID=?",(int(userid),))
        info=cs.fetchone()
        cs.close()
        if(info):
            return(True,info)
        return(False,None)

def assignId(grade:int,infoDict:dict):
    infoDict["userid"]=getOneFreeId(getYearByGrade(grade))
    return(infoDict)

def getKeyWords()->tuple:
    return("userid","name","class","grade","position","department","contactstyle")

def renderInfo(infoDicts:list):
    notRenderKeywords=("userid","name","class","contactstyle")
    willRenderKeyWords=("grade","position","department")
    rendedDicts=[]
    grades=getGradeInfo()
    positions=getPositionInfo()
    departments=getDepartmentInfo()
    for Infodict in infoDicts:
        newDict=dict()
        for nRKW in notRenderKeywords:
            newDict[nRKW]=Infodict[nRKW]
        grade      =      grades.get(Infodict[  "grade"   ],"未知")
        position   =   positions.get(Infodict[ "position" ],"未知")
        department = departments.get(Infodict["department"],"未知")

        newDict["grade"]=grade        
        newDict["position"]=position
        newDict["department"]=department
        rendedDicts.append(newDict)
    return(rendedDicts)

def getSheetHeader():
    return("ID","姓名","班级","年级","职位","部门","联系方式")
"""======================================================="""
def CreateSocietyDatabase(Grade=None):
    if(not Grade):
        Grade=int(getNowGradeinYear())
    with dbconnect(f"{SOCIETYDATABASEPATH}{Grade}.db") as db:
        cs=db.cursor()
        cs.execute("CREATE TABLE IF NOT EXISTS  Member("
                "userid integer PRIMARY KEY,"
                "name text NOT NULL,"
                "class int default 1,"
                "grade int default 0,"
                "position int default 0,"
                "department int default 0,"
                "contactStyle text default '无'"
            ")"
        )
        #oprations
        cs.execute("create table if not exists oprations("
                "oprationID int primary key,"
                "password text,"
                "permission int default 0"
            ")"
        )
        #positions
        cs.execute("create table if not exists positions("
                "position int primary key,"
                "description text"
            ")"
        )
        #grades
        cs.execute("create table if not exists grades("
                "grade int primary key,"
                "year int,"
                "description text"
            ")"
        )
        #departments
        cs.execute("create table if not exists departments("
                "departmentId int primary key,"
                "description text"
            ")"
        )
        #permissions
        cs.execute("create table if not exists permissions("
                "permissionId int primary key,"
                "description text"
            ")"
        )
        positions=((0,"成员"),(1,"部长"),(2,"副会长"),(3,"部长/副会长"),(4,"会长"),(5,"部长/会长"))
        permissions=((0,"仅查看"),(1,"本年级本部门"),(2,"所有年级本部门"),(3,"本年级所有部门"),(4,"所有年级所有部门"))
        departments=((0,"科创部"),(1,"编程部"),(2,"航模部"),(3,"宣传部"),(4,"实践部"))
        grades=((0,2022,"高一"),(1,2021,"高二"),(2,2020,"高三"))

        commands=(
            "insert into permissions (permissionId,description) values(?,?)",
            "insert into positions(position,description) values(?,?)",
            "insert into departments(departmentId,description) values(?,?)",
            "insert into grades(grade,year,description) values(?,?,?)"
        )

        values=(
            permissions,
            positions,
            departments,
            grades
        )
        for c,s in zip(commands,values):
            try:
                cs.executemany(c,s)
            except:
                pass
        cs.close()




#===========================================================

    

if(__name__=="__main__"):
    print(getAppInfo("SuperOprationId"))
    print(getAppInfo("SuperOprationPassword"))
    print(getAppInfo("NowGrade"))
    # print(getFreeId(21,20))
    CreateSocietyDatabase(21)
    with open("./name.txt") as file:
        addMember([{"name":i,"grade":21} for i in file.readlines()])
    
