from importModule.init import initDirectory,initDataBase
initDirectory()
initDataBase()
import sever

if(__name__=="__main__"):
    Sever=sever.AppSever()
    Sever.run()
    "🤟🤓"