from importModule.manageDatabase import getDepartmentInfo,getGradeInfo
from importModule.manageDatabase import getPermissionInfo,getPositionInfo
from importModule.Forms import editMemberForm
from flask import render_template


def handle_initEditMemberForm(form:editMemberForm,info:dict,method):
    form.department.choices=list(getDepartmentInfo().items())
    form.position.choices=list(getPositionInfo().items())
    form.grade.choices=list(getGradeInfo().items())    
    if(method=="GET"):
        form.department.default=info["department"]
        form.grade.default=info["grade"]
        form.position.default=info["position"]
        form.userid.default=info["userid"]
        form.name.default=info["name"]
        form.userclass.default=info["userclass"]
        form.contactStyle.default=info["contactStyle"]
        form.process()