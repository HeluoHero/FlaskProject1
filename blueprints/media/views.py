from flask import Blueprint, send_from_directory, current_app

bp = Blueprint('media', __name__, url_prefix='/media')


# /media/avatar/abc.jpg
# 部署的时候，在nginx中配置静态文件目录，将/media的前缀的url
# 访问/medio的时候，我们指定让他从media文件夹下寻找文件

@bp.route('/avatar/<filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)
