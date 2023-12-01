from functools import wraps
from flask import Flask,jsonify,render_template,redirect
from flask import request, session,url_for,abort,send_file,flash,get_flashed_messages
from flask_wtf.csrf import CSRFProtect
from os.path import isdir
from time import time
from importModule.Forms import LoginForm,LogoutForm,editMemberForm
from importModule.manageDatabase import *
from importModule.Appvalidator import LoginValiidator
from importModule.handle import handle_initEditMemberForm
from importModule.Filters import Filters,dataFilter




#======================初始化方法==============================
addOpration(2021001,"2021001",3)
appvalidator=LoginValiidator()
appFilter=Filters()
datafilter=dataFilter()

#=========================验证登录======================
def SuperOprationLogin(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if(appvalidator.ValidateSuperOpration(session)):
            return(f(*args,**kwargs))
        return(redirect(url_for("returnIndexPage")))
    return(decorated_function)


def OprationLogin(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if(appvalidator.validateOpration(session)):
            return(f(*args,**kwargs))
        return(redirect(url_for("returnIndexPage")))
    return(decorated_function)

def NormalOprationLogin(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if(appvalidator.ValidateSuperOpration(session)):
            return(f(*args,**kwargs))
        return(redirect(url_for("returnIndexPage")))
    return(decorated_function)


#========================常量================================
PATH=".\\WebFiles\\"
HTMLPATH=f"{PATH}HTML\\"
JSPATH=f"{PATH}JS\\"
CSSPATH=f"{PATH}CSS\\"
ICONPATH=f"{PATH}ICON\\"
GET="GET"
POST="POST"

#=====================================================

class AppSever:

    def run(self):
        app=Flask(__name__,template_folder="./WebFiles/templates")
        app.config["SECRET_KEY"]="SOCITY"
        csrf=CSRFProtect(app)

        self.history(app,csrf)
        self.returnResources(app,csrf)
        self.SocietyManageUrl(app,csrf)
        self.afterLogin(app,csrf)
        self.MembersManageUrl(app,csrf)

        app.run(host="0.0.0.0",port=80)

    #============================================

    def history(self,app:Flask,csrf:CSRFProtect):
        app.route("/history/")
        def historyData():
            return(render_template("histories.html"))

    #============================================

    def returnResources(self,app:Flask,csrf:CSRFProtect):
        @app.route("/",methods=[GET,POST])
        def returnIndexPage():
            form=LoginForm()
            if(appvalidator.validateOpration(session)):
                return(redirect(url_for("manageSocietyPage")))
            if(form.validate_on_submit()):
                userid=form.data["USERid"]
                password=form.data["password"]
                session["USERid"]=userid
                session["password"]=password
                return(redirect(url_for("manageSocietyPage")))
            return(render_template("index.html",form=form))

        @app.route("/CSS/<filename>",methods=[GET])
        def getCSS(filename):
            with open(f"{CSSPATH}{filename}") as file:
                return(file.read())

        @app.route("/JS/<filename>",methods=[GET])
        def getJS(filename):
            with open(f"{JSPATH}{filename}") as file:
                return(file.read())
            
        @app.route("/ICON/<filename>",methods=[GET])
        def getICON(filename):
            with open(f"{ICONPATH}{filename}","br") as file:
                return(file.read())



    #======================================
    def afterLogin(self,app:Flask,csrf:CSRFProtect):

        @app.route("/manage",methods=[GET])
        @OprationLogin
        def manageSocietyPage():
            return(render_template("/home.html",thisname="成员管理"))

        @app.route("/account",methods=[GET])
        @OprationLogin
        def accountPage():
            oprationStyle="普通管理员"if(appvalidator.ValidateNormalOpration(session))else"超级管理员"
            form=LogoutForm()
            return(render_template("account.html",
                USERid=session.get("USERid"),
                OprationStyle=oprationStyle,
                form=form
                )
            )

        @app.route("/socialFees",methods=[GET])
        @OprationLogin
        def SocialFeesPage():
            return(render_template("/feesManage.html"))

        @app.route("/meetingManage",methods=[GET])
        @OprationLogin
        def manageMeetingPage():
            return(render_template("/meetingManage.html"))

        @app.route("/SocietyManage",methods=[GET])
        @OprationLogin
        def SocietyManagePage():
            return(render_template("/SocietyManage.html"))

        @app.route("/logout",methods=[POST])
        @OprationLogin
        def logoutUrl():
            session.pop("USERid")
            session.pop("password")
            return(redirect(url_for("returnIndexPage")))
        
    def SocietyManageUrl(self,app:Flask,csrf:CSRFProtect):
        pass
        
    #======================================================
    def MembersManageUrl(self,app:Flask,csrf:CSRFProtect):
        @app.route("/Members/",methods=[GET])
        @OprationLogin
        def MembersRootPage():
            return(render_template("MemberRootPage.html",validateOpration=True))

        @app.route("/Members/view/",methods=[GET])
        def viewMembersPage():
            initInfo=getMembers()
            renderedInfo=renderInfo(initInfo)  
            return(
                render_template(
                    "viewMembers.html",
                    members=renderedInfo,
                    keywords=getMemberKeyWords(),
                    sheetheader=getMemberSheetHeader(),
                    KS=zip(getMemberKeyWords(),getMemberSheetHeader())
                )
            )

        @app.route("/Members/edit/",methods=[GET])
        @OprationLogin
        def EditMembersPage():
            if(appvalidator.ValidateNormalOpration(session)):
                userid=int(session.get("USERid"))
                initInfo=getMemberWithPemission(
                    datafilter.filterById(userid)
                )[1]
            else:
                initInfo=getMembers()
            renderedInfo=renderInfo(initInfo)
            controlers=[{"text":"编辑","controlerType":"config"},{"text":"删除","controlerType":"del"}]
            return(
                render_template(
                    "EditMembers.html",
                    members=renderedInfo,
                    keywords=getMemberKeyWords(),
                    sheetheader=getMemberSheetHeader(),
                    controlers=controlers,
                    controlKey=["操作"],
                    KS=zip(getMemberKeyWords(),getMemberSheetHeader())
                )
            )

        @app.route("/Members/edit/<int:userid>",methods=[GET,POST])
        @OprationLogin
        def EditMemberPage(userid):
            userid=int(userid)
            oprationid=int(session.get("USERid"))
            userinfo=getMemberById(userid)
            if(not userinfo[0]):
                return(render_template("404Page.html",errs=[f"不存在id({userid})"]))
            if(not appvalidator.ValidateSuperOpration):
                if(not appFilter.filterById(oprationid,getMemberById(userid)[1])):
                    return(render_template("404Page.html",errs=[f"权限不足({userid})"]))
            form=editMemberForm()
            handle_initEditMemberForm(form,userinfo[1],request.method)
            if(form.validate_on_submit()):
                if(appvalidator.ValidateNormalOpration(session)):
                    oprationInfo=getMemberById(oprationid)[1]
                    oprationInfo:dict
                    oprationGrade=oprationInfo.get("grade")
                    oprationPosition=oprationInfo.get("position")
                    newGrade=form.data.get("grade")
                    newPosition=form.data.get("position")
                    oldGrade=userinfo[1].get("grade")
                    oldPosition=userinfo[1].get("position")
                    if (
                        (((newGrade >= oprationGrade) and (newGrade > oldGrade)) or (
                            (newPosition >= oprationPosition) and (newPosition > oldPosition)) and userid != oprationid)
                        or ((newGrade > oprationGrade) or (newPosition > oprationPosition))
                    ):
                        flash("权限不足",f"{userid}")
                        return(redirect(request.url))
                msg=editMember(userid,form.data,userinfo[1])
                if(msg[0]):
                    flash("提交成功",f"{userid}")
                    return(redirect(request.url))
                else:
                    flash(msg[1],f"{userid}")
                    return(redirect(request.url))
            else:
                return(render_template("editMember.html",form=form,userid=userid))
            
        @app.route("/Members/add/",methods=[GET])
        @OprationLogin
        def addMember():
            initInfo=getMembers()
            renderedInfo=renderInfo(initInfo)  
            return(
                render_template(
                    "addMember.html",
                    members=renderedInfo,
                    keywords=getMemberKeyWords(),
                    sheetheader=getMemberSheetHeader(),
                    KS=zip(getMemberKeyWords(),getMemberSheetHeader())
                )
            )
        
        @csrf.exempt
        @app.route("/deleteMember",methods=[POST])
        @OprationLogin
        def deleteMemberUrl():
            userid=request.form.get("userid")
            test=request.form.get("test")
            returnFalse=request.form.get("returnFalse")
            if(not test):
                stat=deleteMember(int(userid))
            else:
                stat=not returnFalse
            return(jsonify({"stat":stat}))
