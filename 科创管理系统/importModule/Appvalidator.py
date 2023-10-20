from flask.sessions import SessionMixin
from .manageDatabase import *
from werkzeug.security import check_password_hash

class LoginValiidator:
    def ValidateOpration(self,session:SessionMixin):
        if(self.ValidateIsLogin(session)):
            userid=session.get("USERid",None)
            password=session.get("password",None)
            info=getOprationInfoById(userid)
            if(info[0]):
                if(check_password_hash(password,info[0])):
                    return(True)
        return(False)

    def ValidateIsLogin(self,session:SessionMixin):
        userid=session.get("USERid",None)
        password=session.get("password",None)
        if( userid and password):
            return(True)
        return(False)
    
    def ValidateOnlyNormalOpration(self,session:SessionMixin):
        if(self.ValidateSuperOpration(session)):
            return(False)
        return(True)
    
    def ValidateSuperOpration(self,session:SessionMixin):
        if(self.ValidateIsLogin(session)):
            userid=session.get("USERid",None)
            password=session.get("password",None)
            superoprationId=getAppInfo("SuperOprationId")[0]
            info=getAppInfo("SuperOprationPassword")
            if(info):
                return(check_password_hash(password,info[0]) and userid==superoprationId)
        return(False)
    

