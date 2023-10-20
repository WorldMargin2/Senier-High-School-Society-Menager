from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    USERid=StringField("UserId",render_kw={"placeholder":"管理员ID"},validators=[InputRequired()])
    password=PasswordField("Password",render_kw={"placeholder":"管理员密码"},validators=[InputRequired()])
    submit=SubmitField("登录")


class LogoutForm(FlaskForm):
    submit=SubmitField("退出登录")



