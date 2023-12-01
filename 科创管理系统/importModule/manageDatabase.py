from sqlite3 import connect as dbconnect
from importModule.initialName import initialNames
from time import time

DATABASEPATH="./database/"
APPDATAPATH="./database/AppData/"
SOCIETYDATABASEPATH="./database/SocietyDatabase/"
HISTORYPATH="./database/SocietyDatabase/history/"

positions=((0,"成员"),(1,"部长"),(2,"副会长"),(3,"部长/副会长"),(4,"会长"),(5,"部长/会长"))
permissions=((0,"仅查看"),(1,"本年级本部门"),(2,"所有年级本部门"),(3,"本年级所有部门"),(4,"所有年级所有部门"))
departments=((0,"科创部"),(1,"编程部"),(2,"航模部"),(3,"宣传部"),(4,"实践部"))
grades=((0,2022,"高一"),(1,2021,"高二"),(2,2020,"高三"))

#===================程序数据库==================================
def getAppInfo(keytext)->tuple:
    with dbconnect(f"{APPDATAPATH}appdata.db") as db:
        cs=db.cursor()
        cs.execute("select valuetext,typetext from KeyValue where keytext = ?",(keytext,))
        info=cs.fetchone()
        cs.close()
        return(info)

def writeAppdata(keytext:str,valuetext:str,typetext:str="str")->bool:
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

def changeAppdata(keytext:str,valuetext:str,typetext:str="str")->bool:
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

def CreateAppdatabase()->None:
    with dbconnect(f"{APPDATAPATH}appdata.db") as db:
        cs=db.cursor()
        cs.execute("create TABLE IF NOT EXISTS KeyValue("
            "keytext text PRIMARY KEY,"
            "valuetext text,"
            "typetext text"
        ")")
        cs.close()
    writeAppdata("SuperOprationId","202101","int")
    writeAppdata("SuperOprationPassword","202101","int")
    writeAppdata("NowGrade","21","int")
#==========================获取年级=========================================
def getNowGradeinYear()->int:
    return(getAppInfo("NowGrade")[0])

def getSocietyDataBase()->str:
    return(f"{getNowGradeinYear()}.db")

#============================管理员操作==========================


#添加管理员
def addOpration(userid:int,password=202101,permission:int=1)->dict:
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("SELECT userid FROM Member WHERE userid=?",(userid,))
        if(not cs.fetchone()):
            cs.close()
            return(False)
        cs.execute("select * from oprations where oprationID=?",(userid,))
        if(cs.fetchone()):
            cs.close()
            return(False)
        cs.execute("insert into oprations(oprationID,password,permission) values(?,?,?)",(userid,password,permission))
        cs.close()
        return(True)

def getPermissionById(userId:int)->int:
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select permission from oprations where oprationID=?",(int(userId),))
        permission=cs.fetchone()
        cs.close()
        return(permission[0])

def getOprationPwdById(userid:int)->tuple:
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select password from oprations where oprationID=?",(int(userid),))
        info=cs.fetchone()
        cs.close()
        if(info):
            return(True,info[0])
        return(False,())

#===========================成员相关操作========================
#添加成员
def addMember(memberDicts:list)->bool:
    newlist=[]
    grades=getGradeInfo().keys()
    departments=getDepartmentInfo().keys()
    for memberDict in memberDicts:
        memberDict:dict
        name=memberDict.get("name")
        grade=memberDict.get("grade",0)
        userclass=memberDict.get("userclass",1)
        position=memberDict.get("position",0)
        department=memberDict.get("department",0)
        contactStyle=memberDict.get("contactStyle","无")
        if(not grade in grades):
            grade=0
        if(not department in departments):
            department=0
        userid=getOneFreeId(grade)
        newlist.append((userid,name,userclass,position,department,contactStyle))
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.executemany(
            "insert into Member"
            "(userid,name,userclass,position,department,contactStyle) "
            "values(?,?,?,?,?,?)",
            newlist
        )
        cs.close()

#编辑成员
def editMember(userid:int,form:dict,old_info:dict)->(bool,str):
    kwl=["name","grade","position","userclass","department","contactStyle","userid"]
    if((form.get("userid"))!=userid):
        return(False,"请不要修改ID")
    isSame=False
    for i in kwl:
        isSame=True
        if(form.get(i)!=old_info.get(i)):
            isSame=False
            break
    if(isSame):
        return(False,"未更改任何内容")
    form["contactStyle"]=form["contactStyle"].strip("\n\t\r")
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute(
            "UPDATE Member SET name=?,grade=?,position=?,userclass=?,department=?,contactStyle=?"
            " WHERE userid=?",
            [form.get(i) for i in kwl]
        )
        cs.close()
    return(True,"")

#删除成员
def deleteMember(userID:int)->bool:
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select name from Member where userid=?",(userID,))
        if(cs.fetchone()):
            cs.execute("delete from Member where userid=?",(userID,))
            cs.close()
            return(True)
        cs.close()
        return(False)

#获取所有成员信息
def getMembers()->list:
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        dictList=[]
        cs.execute("select userid,name,userclass,grade,position,department,contactStyle from Member")
        #         ("userid","name","userclass","grade","position","department","contactStyle")
        keys=getMemberKeyWords()
        for i in cs.fetchall():
            dictList.append(dict(zip(keys,i)))
        return(dictList)

#根据权限获取成员
def getMemberWithPemission(Permission:dict):
    dictList=[]
    keys=getMemberKeyWords()
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select MAX(departmentId) from departments")
        maxDepartment=cs.fetchone()[0]
        cs.execute("select MAX(grade) from grades")
        maxGrade=cs.fetchone()[0]
        cs.execute("select MAX(position) from positions")
        maxPosion=cs.fetchone()[0]
        initialPermission={
            "grade":{
                "relation":"<=",
                "value":maxGrade
            },
            "position":{
                "relation":"<=",
                "value":maxPosion
            },
            "department":{
                "relation":"<=",
                "value":maxDepartment
            }
        }
        initialPermission.update(Permission)
        if(initialPermission["grade"]["value"]>maxGrade):
            initialPermission["grade"]["value"]=maxGrade
        if(initialPermission["department"]["value"]>maxDepartment):
            initialPermission["grade"]["value"]=maxDepartment
        if(initialPermission["position"]["value"]>maxPosion):
            initialPermission["grade"]["value"]=maxPosion
        command=(
            "SELECT"
            " userid,name,userclass,grade,position,department,contactStyle"
            " FROM Member WHERE "
        )
        addToCommandList=[
            f"{i}{initialPermission[i]['relation']}{initialPermission[i]['value']}"
            for i in initialPermission.keys()
        ]
        command+=" AND ".join(addToCommandList)
        cs.execute(command)
        info=cs.fetchall()
        cs.close()
        if(info):
            for i in info:
                dictList.append(dict(zip(keys,i)))
            return(True,dictList)
        else:
            return(False,())
    

#获取成员信息
def getMemberById(userid:int)->tuple:
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select userid,name,userclass,grade,position,department,contactStyle from Member where userid = ?",(userid,))
        result=cs.fetchone()
        cs.close()
    if(result):
        keys=getMemberKeyWords()
        result=[dict(zip(keys,result))]
        return(True,result[0])
    else:
        return(False,())

#获取并渲染成员信息
def SearchMemberInfo(userid:int)->tuple:
    result=getMemberById(userid)
    if(result[0]):
        keys=getMemberKeyWords()
        result=renderInfo([dict(zip(keys,result[1]))])
        return(True,result[0])
    else:
        return(False,())

#=========================获取成员信息==================================
def getGrades()->list:
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select grade from grades")
        grades=cs.fetchall()
        cs.close()
        return(grades)

def getYearByGrade(grade:int)->int:
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select year from grades where grade = ?",(grade))
        year=cs.fetchone()
        cs.close()
        return(year[0])

def getGradeById(Userid:int)->int:
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select grade from Member where userid=?",(Userid,))
        grade=cs.fetchone()
        cs.close()
        return(grade[0])

#=========================分配ID===================================
def getIdByYear(year:int)->int:
    Maxid=f"20{year}999"
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        cs.execute("select userid from Member where userid<=?",(int(Maxid),))
        idList=list(i[0] for i in cs.fetchall())
        cs.close()
        return(idList)

def findFreeId(IdList:list,year:int,number:int)->list:
    resault=[]
    startId=int(f"20{year}001")
    maxId=max(IdList)
    for i in range(startId,maxId):
        if((not (i in IdList)) and (len(resault)<number)):
            resault.append(i)
    if(not len(resault)==number):
        list(range(maxId+1,maxId+(number-len(resault))+1)).extend(resault)
    return(resault)

def findOneFreeId(IdList:list,year:int)->int:
    startId=int(f"20{year}001")
    maxId=max(IdList)
    for i in range(startId,maxId):
        if((not (i in IdList))):
            return(i)

def getFreeId(year:int,number:int)->list:
    if(not len(getIdByYear(year))):
        start=int(f"20{year}001")
        return(list(range(start,start+number)))
    return(findFreeId(getIdByYear(year),year,number))

def getOneFreeId(year:int)->int:
    if(not len(getIdByYear(year))):
        return(int(f"20{year}001"))
    return(findOneFreeId(getIdByYear(year),year))

def assignId(grade:int,infoDict:dict)->dict:
    infoDict["userid"]=getOneFreeId(getYearByGrade(grade))
    return(infoDict)

#===============获取关键信息描述(权限，年级，职位，部门等)=====================
def getPermissionInfo()->dict:
    with dbconnect(f"{SOCIETYDATABASEPATH}{getSocietyDataBase()}") as db:
        cs=db.cursor()
        permission=dict()
        cs.execute("select permissionId,description from permissions")
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

def getMemberKeyWords()->tuple:
    return("userid","name","userclass","grade","position","department","contactStyle")

def getMemberSheetHeader()->tuple:
    return("ID","姓名","班级","年级","职位","部门","联系方式")

def renderInfo(infoDicts:list)->list:
    notRenderKeywords=("userid","name","userclass","contactStyle")
    willRenderKeyWords=("grade","position","department")
    rendedDicts=[]
    grades=getGradeInfo()
    positions=getPositionInfo()
    departments=getDepartmentInfo()
    for Infodict in infoDicts:
        newDict=dict()
        for nRKW in notRenderKeywords:
            newDict[nRKW]=Infodict[nRKW]
        newDict["grade"]=grades.get(Infodict[  "grade"   ],"未知")
        newDict["position"]=positions.get(Infodict[ "position" ],"未知")
        newDict["department"]=departments.get(Infodict["department"],"未知")
        rendedDicts.append(newDict)
    return(rendedDicts)

def getKeyWordDict()->dict:
    return(dict(zip(getMemberKeyWords(),getMemberSheetHeader())))

"""===================创建数据库===================================="""
def CreateSocietyDatabase(Grade=None):
    if(not Grade):
        Grade=int(getNowGradeinYear())
    with dbconnect(f"{SOCIETYDATABASEPATH}{Grade}.db") as db:
        cs=db.cursor()
        cs.execute("CREATE TABLE IF NOT EXISTS  Member("
                "userid integer PRIMARY KEY,"
                "name text NOT NULL,"
                "userclass int default 1,"
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

        cs.execute("create table if not exists LoginLog("
                "oprationID int,"
                "LoginTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
                "Operate text,"
                "Address text"
            ")"
        )
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
    CreateSocietyDatabase(21)
