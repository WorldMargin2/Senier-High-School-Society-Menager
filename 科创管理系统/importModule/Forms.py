from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms import HiddenField,SelectField,IntegerField
from wtforms import TextAreaField
from wtforms.validators import InputRequired,NumberRange
from wtforms.validators import Length

class LoginForm(FlaskForm):
    USERid=StringField(
        "UserId",
        render_kw={"placeholder":"管理员ID"},
        validators=[InputRequired()]
    )
    password = PasswordField(
        "Password",
        render_kw={"placeholder": "管理员密码"},
        validators=[InputRequired()]
    )
    submit=SubmitField("登录")


class LogoutForm(FlaskForm):
    submit=SubmitField("退出登录")

class editMemberForm(FlaskForm):
    userid=IntegerField(
        label="ID",     
        validators=[InputRequired()],
        render_kw={"readonly":True}
    )
    name=StringField(
        label="姓名", 
        validators=[InputRequired()]
    )
    grade=SelectField(
        label="年级", 
        coerce=int,
        validators=[InputRequired()]
    )
    userclass=IntegerField(
        label="班级", 
        validators=[NumberRange(1,30),InputRequired()]
    )
    position=SelectField(
        label="职位", 
        coerce=int,
        validators=[InputRequired()]
    )
    department=SelectField(
        label="部门", 
        coerce=int,
        validators=[InputRequired()]
    )
    contactStyle=TextAreaField(
        label="联系方式",
        validators=[Length(0,255)]
    )
    submit=SubmitField(
        "提交"
    )



