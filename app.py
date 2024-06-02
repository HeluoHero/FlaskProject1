from flask import Flask
from flask_migrate import Migrate

import commands
import config
from exts import db, mail, cache, csrf, avatars
from models import auth
from blueprints.front import front_bp
from blueprints.media import media_bp
from bbs_celery import make_celery

app = Flask(__name__)

# 配置文件
app.config.from_object(config)
# 初始化db
db.init_app(app)
# 初始化mail
mail.init_app(app)
# 初始化cache
cache.init_app(app)
# 初始化avatars
avatars.init_app(app)
# 初始化migrate
migrate = Migrate(app, db)
# 初始化csrf
csrf = csrf.init_app(app)
# 构建celery
celery = make_celery(app)

# 注册蓝图
app.register_blueprint(front_bp)
app.register_blueprint(media_bp)

# 注册命令
app.cli.command("init_boards")(commands.init_boards)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8999)
