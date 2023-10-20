from manageDatabase import *

class Filters:
    def filterByGrades(self,grades,targetDicts):
        resault = []
        for dict in targetDicts:
            if(dict["grade"] in grades):
                resault.append(dict)
        return(resault)

    def filterByDepartments(self,departments,targetDicts):
        resault = []
        for dict in targetDicts:
            if(dict["department"] in departments):
                resault.append(dict)
        return(resault)

    def filterByPositions(self,positions,targetDicts):
        resault = []
        for dict in targetDicts:
            if(dict["position"] in positions):
                resault.append(dict)
        return(resault)
    
    def filterGradesById(self,UserId):
        UserPermissionOnGrade=getPermissionById(UserId)
        selfGrade=getGradeById(UserId)
        
