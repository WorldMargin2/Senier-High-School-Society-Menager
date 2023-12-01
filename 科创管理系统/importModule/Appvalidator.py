from flask.sessions import SessionMixin
from importModule.manageDatabase import *
from time import time

def checkRuntime(handle,*args):
    s=time()
    handle(*args)
    e=time()
    print(e-s)

class LoginValiidator:
    def ValidateNormalOpration(self,session:SessionMixin):
        if(self.ValidateIsLogin(session)):
            userid=int(session.get("USERid"))
            password=session.get("password")
            info=getOprationPwdById(userid)
            if(info[0]):
                if(password==info[1]):
                    return(True)
            return(False)

    def ValidateIsLogin(self,session:SessionMixin):
        userid=session.get("USERid")
        password=session.get("password")
        if( userid and password):
            return(True)
        return(False)

    def validateOpration(self,session:SessionMixin):
        if(self.ValidateSuperOpration(session) ):
            return(True)
        if(self.ValidateNormalOpration(session)):
            return(True)
        return(False)

    def ValidateSuperOpration(self,session:SessionMixin):
        if(self.ValidateIsLogin(session)):
            userid=session.get("USERid")
            password=session.get("password")
            superoprationId=getAppInfo("SuperOprationId")[0]
            info=getAppInfo("SuperOprationPassword")
            if(info):
                return(password==info[0] and userid==superoprationId)
        return(False)


