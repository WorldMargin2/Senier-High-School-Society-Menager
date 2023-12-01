from flask.sessions import SessionMixin
from .manageDatabase import getPermissionById,getGradeById,getMemberById

class Filters:
    def filterByGrade(self,oprationInfo:dict,targetDicts:list):
        resault = []
        grade=oprationInfo.get("grade")
        for i in targetDicts:
            i:dict
            if(i.get("grade")==grade):
                resault.append(i)
        return(resault)

    def filterByDepartment(self,oprationInfo:dict,targetDicts:list):
        resault = []
        department=oprationInfo.get("department")
        for i in targetDicts:
            i:dict
            if(i.get("department")==department):
                resault.append(i)
        return(resault)

    def filterByPosition(self,oprationInfo:dict,targetDicts:list):
        resault = []
        position=oprationInfo.get("position")
        for i in targetDicts:
            i:dict
            if(i.get("position")<=position):
                resault.append(i)
        return(resault)

    def filterById(self,userid:int,MemberDics:list,filterType:str="w"):
        if((filterType=="r")or(filterType=="R")):
            return(MemberDics)
        filterall=lambda oprationInfo,x:x
        handleStyle={
            0:(filterall,),
            1:(self.filterByDepartment,self.filterByGrade,self.filterByPosition),
            2:(self.filterByDepartment,self.filterByPosition),
            3:(self.filterByGrade,self.filterByPosition),
            4:(filterall,self.filterByPosition)
        }
        permission=getPermissionById(userid)
        oprationInfo=getMemberById(userid)[1]
        for i in handleStyle.get(permission,(filterall,)):
            MemberDics=i(oprationInfo,MemberDics)
        return(MemberDics)

class dataFilter:
    def filterById(self,userid:int,filterType:str="w"):
        permissions={}
        handleStyle={
            0:(),
            1:(self.filterByDepartment,self.filterByGrade,self.filterByPosition),
            2:(self.filterByDepartment,self.filterByPosition),
            3:(self.filterByGrade,self.filterByPosition),
            4:(self.filterByPosition)
        }
        permission=getPermissionById(userid)
        oprationInfo=getMemberById(userid)[1]
        for i in handleStyle.get(permission,()):
            i(oprationInfo,permissions)
        return(permissions)

    def filterByGrade(self,oprationInfo:dict,permissions:list):
        grade=oprationInfo.get("grade")
        data={
            "relation":"=",
            "value":grade
        }
        permissions["grade"]=data

    def filterByDepartment(self,oprationInfo:dict,permissions:dict):
        department=oprationInfo.get("department")
        data={
            "relation":"=",
            "value":department
        }
        permissions["department"]=data

    def filterByPosition(self,oprationInfo:dict,permissions:dict):
        position=oprationInfo.get("position")
        data={
            "relation":"<=",
            "value":position
        }
        permissions["position"]=data

