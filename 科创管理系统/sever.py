from flask import Flask,jsonify,render_template,redirect,request, session,url_for,abort,send_file
from flask_wtf.csrf import CSRFProtect
from os.path import isdir
from importModule.Forms import LoginForm,LogoutForm
from importModule.manageDatabase import *
from importModule.Appvalidator import LoginValiidator
from werkzeug.security import generate_password_hash


appvalidator=LoginValiidator()
def tryLogin(session):
    if(appvalidator.ValidateOpration(session) or
        appvalidator.ValidateSuperOpration(session)
    ):
        return(True)
    return(False)



PATH=".\\WebFiles\\"
HTMLPATH=f"{PATH}HTML\\"
JSPATH=f"{PATH}JS\\"
CSSPATH=f"{PATH}CSS\\"
GET="GET"
POST="POST"



class AppSever:

    def run(self):
        app=Flask(__name__,template_folder="./WebFiles/templates")
        app.config["SECRET_KEY"]="SOCITY"
        # app.debug=True
        csrf=CSRFProtect(app)
        

        self.returnResources(app)
        self.responseRequese(app)
        self.afterLogin(app)
        
        app.run(host="0.0.0.0",port=80)
    #============================================
    def returnResources(self,app:Flask):
        @app.route("/",methods=[GET,POST])
        def returnIndexPage():
            form=LoginForm()
            if(tryLogin(session)):
                return(redirect(url_for("manageSociety")))
            if form.validate_on_submit():
                userid=form.data["USERid"]
                password=form.data["password"]
                session["USERid"]=userid
                session["password"]=generate_password_hash(password)
                return(redirect(url_for("manageSociety")))
            return(render_template("index.html",form=form))
            
            
        
        @app.route("/CSS/<filename>",methods=[GET])
        def getCSS(filename):
            with open(f"{CSSPATH}{filename}") as file:
                return(file.read())
            
        @app.route("/JS/<filename>",methods=[GET])
        def getJS(filename):
            with open(f"{JSPATH}{filename}") as file:
                return(file.read())
        
        
    #=========================================
    def responseRequese(self,app:Flask):
        pass
    #======================================
    def afterLogin(self,app:Flask):
        @app.route("/manage",methods=[GET])
        def manageSociety():
            if(tryLogin(session)):
                return(render_template("/homeExample.html",thisname="成员管理"))
            return(redirect(url_for("returnIndexPage")))
        
        @app.route("/account",methods=[GET])
        def account():
            if(tryLogin(session)):
                oprationStyle="普通管理员"if(appvalidator.ValidateOnlyNormalOpration(session))else"超级管理员"
                form=LogoutForm()
                return(render_template("account.html",
                    USERid=session.get("USERid",None),
                    OprationStyle=oprationStyle,
                    form=form
                    )
                )
            return(redirect(url_for("returnIndexPage")))
        
        
        @app.route("/manageMember",methods=[GET])
        def manageMember():
            if(tryLogin(session)):
                return(render_template("/normalManage.html"))
            return(redirect(url_for("returnIndexPage")))
        
        @app.route("/socialFees",methods=[GET])
        def SocialFees():
            if(tryLogin(session)):
                return(render_template("/normalManage.html"))
            return(redirect(url_for("returnIndexPage")))

        
        @app.route("/meetingmanagement",methods=[GET])
        def manageMeeting():
            if(tryLogin(session)):
                return(render_template("/normalManage.html"))
            return(redirect(url_for("returnIndexPage")))
        
        @app.route("/SocietyManage",methods=[GET])
        def SocietyManage():
            if(tryLogin(session)):
                return(render_template("/normalManage.html"))
            return(redirect(url_for("returnIndexPage")))
        
        @app.route("/members",methods=[GET])
        def ReturnMembers():
            return(render_template("viewMembers.html",members=getMembers()))
        
        @app.route("/logout",methods=[POST])
        def logout():
            if(tryLogin(session)):
                session.pop("USERid",None)
                session.pop("password",None)
            return(redirect(url_for("returnIndexPage")))
        


