from flask_wtf.file import FileAllowed, FileSize
from wtforms import Form, ValidationError
from wtforms.fields import StringField
from wtforms.validators import Email, Length, equal_to
from models.auth import UserModel
from exts import cache
from flask import request


class BaseForm(Form):
    @property
    def messages(self):
        message_list = []
        if self.errors:
            for errors in self.errors.items():
                message_list.append(errors)
        return message_list


class RegisterForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱！')])
    email_captcha = StringField(validators=[Length(min=6, max=6, message='请输入正确的邮箱验证码！')])
    username = StringField(validators=[Length(min=3, max=20, message='请输入正确长度的用户名！')])
    password = StringField(validators=[Length(min=6, max=20, message='请输入正确长度的密码！')])
    repeat_password = StringField(validators=[Length(min=6, max=20, message='请输入正确长度的密码！'),
                                              equal_to('password', message='两次密码不一致！')])
    graph_captcha = StringField(validators=[Length(min=4, max=4, message='请输入正确长度的图形验证码！')])

    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise ValidationError(message='邮箱已被注册！')

    def validate_email_captcha(self, field):
        email_captcha = field.data
        email = self.email.data
        cache_captcha = cache.get(email)
        if not cache_captcha or cache_captcha != email_captcha:
            raise ValidationError(message='邮箱验证码错误！')

    def validate_graph_captcha(self, field):
        key = request.cookies.get('_graph_captcha_key')
        cache_captcha = cache.get(key)
        graph_captcha = field.data
        if not cache_captcha or cache_captcha.lower() != graph_captcha.lower():
            raise ValidationError(message='图形验证码错误！')


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱！')])
    password = StringField(validators=[Length(min=6, max=20, message='请输入正确长度的密码！')])
    remember = StringField()

    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if not user:
            raise ValidationError(message='邮箱账户错误！')


class UploadAvatarForm(BaseForm):
    image = StringField(validators=[FileAllowed(['jpg', 'png', 'jpeg'], message='图片格式不符合要求！'),
                                    FileSize(max_size=1024 * 1024 * 5, message='图片大小不能超过5M！')])


class EditProfileForm(BaseForm):
    signature = StringField(validators=[Length(min=1, max=100, message='个性签名长度在1-100之间！')])
