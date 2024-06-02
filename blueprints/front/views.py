from hashlib import md5
from io import BytesIO
from flask_avatars import Identicon
from flask import (
    Blueprint,
    render_template,
    request,
    current_app,
    make_response,
    session,
    redirect,
    g
)
from exts import cache, db
from utils import restful
from utils.captcha import Captcha
from .decorators import login_required
from .forms import RegisterForm, LoginForm, UploadAvatarForm, EditProfileForm
from models.auth import UserModel
import time
import random
import string
import os
from hashlib import md5

bp = Blueprint('front', __name__, url_prefix='/')


# 钩子函数：before_request，在调用视图函数之前执行
@bp.before_request
def before_request():
    if 'user_id' in session:
        user_id = session.get('user_id')
        user = UserModel.query.get(user_id)
        setattr(g, 'user', user)


# 请求 => before_request => 视图函数（如果返回模板） =>
# context_processor => 将context_processor返回的变量和添加到模板中

# 设置上下文
@bp.context_processor
def front_context_processor():
    if hasattr(g, 'user'):
        return {'user': g.get('user')}
    else:
        return {}


@bp.route('/')
def index():  # put application's code here
    return render_template('front/index.html')


@bp.get('/logout')
def logout():
    session.clear()
    return redirect('/')


@bp.route('/setting')
@login_required
def setting():
    email_hash = md5(g.user.email.encode('utf-8')).hexdigest()
    return render_template('front/setting.html', email_hash=email_hash)


@bp.get('/email/captcha')
def email_captcha():
    # /email/captcha?email=xxx@qq.com
    email = request.args.get('email')
    if not email:
        return restful.params_error(message="请先传入邮箱！")
    captcha = ''.join(random.sample(string.digits * 4, 6))
    body = "【HELUO】提醒！您的验证码是：" + captcha
    try:
        current_app.celery.send_task("send_email", (email, captcha, body))  # 使用current_app获取app对象
        cache.set(email, captcha, timeout=60)
    except Exception as e:
        return restful.server_error()
    return restful.ok(message='邮件发送成功')


@bp.get('/graph/captcha')
def graph_captcha():
    captcha, image = Captcha.gene_graph_captcha()
    # 将验证码存入缓存
    key = md5((captcha + str(time.time())).encode('utf-8')).hexdigest()
    cache.set(key, captcha)
    # with open('captcha.png', 'wb') as fp:
    #     image.save(fp, 'png')
    out = BytesIO()
    image.save(out, 'png')
    # 把out文件指针指向最开始的位置
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    resp.set_cookie('_graph_captcha_key', key, max_age=3600)
    return resp


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('front/login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = UserModel.query.filter_by(email=email).first()
            if not user or not user.check_password(password):
                return restful.params_error("邮箱或密码错误！")  # 如果是邮箱未注册的情况，可能会存在信息泄露，所以提示邮箱或者密码错误即可
            session['user_id'] = user.id
            if remember == 1:
                # 默认session过期时间，就是只要浏览器关闭，session就失效了
                session.permanent = True
            return restful.ok("登录成功！")
        else:
            return restful.params_error(message=form.messages[0])


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('front/register.html')
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            identicon = Identicon()
            filenames = identicon.generate(text=md5(email.encode("utf-8")).hexdigest())
            avatar = filenames[2]
            user = UserModel(email=email, username=username, password=password, avatar=avatar)
            db.session.add(user)
            db.session.commit()
            return restful.ok()
        else:
            # form.errors中存放了所有的错误信息
            # {'graph_captcha': ['请输入正确长度的图形验证码！', '图形验证码错误！']}
            message = form.messages[0]
            return restful.params_error(message=message)


@bp.post('/avatar/upload')
@login_required
def upload_avatar():
    form = UploadAvatarForm(request.files)
    if form.validate():
        image = form.image.data
        # 不要使用用户上传的文件名，否则容易被黑客攻击
        _, ext = os.path.splitext(image.filename)
        filename = md5((g.user.email + str(time.time())).encode('utf-8')).hexdigest() + ext
        image_path = os.path.join(current_app.config['AVATARS_SAVE_PATH'], filename)
        image.save(image_path)
        # 看个人需求，是否图片上传完成后立马修改用户的头像字段
        g.user.avatar = filename
        db.session.commit()
        return restful.ok(data={"avatar": filename})
    else:
        message = form.messages[0]
        return restful.params_error(message=message)


@bp.post('/profile/edit')
@login_required
def edit_profile():
    form = EditProfileForm(request.form)
    if form.validate():
        print(form.signature)
        g.user.signature = form.signature.data
        db.session.commit()
        return restful.ok()
    else:
        return restful.params_error(message=form.messages[0])
