# config.py文件
import os
from datetime import timedelta

# 基础怕配置
DEBUG = True
SECRET_KEY = "!#@$^$##@aseasd"
BASE_DIR = os.path.dirname(__file__)

# Session.permanent = True的情况下的过期时间
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

# 头像配置
AVATARS_SAVE_PATH = os.path.join(BASE_DIR, "media", "avatars")
# 帖子图片存放路径
POST_IMAGE_SAVE_PATH = os.path.join(BASE_DIR, "media", "post")
# 轮播图图片存放路径
BANNER_IMAGE_SAVE_PATH = os.path.join(BASE_DIR, "media", "banner")

# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USERNAME = "2170287357@qq.com"
MAIL_PASSWORD = "soxiuefwyupudjcj"
MAIL_DEFAULT_SENDER = "2170287357@qq.com"
MAIL_USE_SSL = True
MAIL_USE_TLS = False

# mysql配置信息
MYSQL_CONFIG = {
    "hostname": "itemdata",
    "port": 3306,
    "username": "root",
    "password": "123456",
    "database": "flask_course",
    "charset": "utf8mb4"
}

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset={charset}".format(
    user=MYSQL_CONFIG['username'],
    password=MYSQL_CONFIG['password'],
    host=MYSQL_CONFIG['hostname'],
    port=MYSQL_CONFIG['port'],
    db=MYSQL_CONFIG['database'],
    charset=MYSQL_CONFIG['charset']
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 缓存系统配置
CACHE_TYPE = "RedisCache"
CACHE_REDIS_HOST = "itemdata"
CACHE_REDIS_PORT = 6379
CACHE_REDIS_DB = 0
CACHE_DEFAULT_TIMEOUT = 300

# Celery配置
CELERY_BROKER_URL = f"redis://{CACHE_REDIS_HOST}:6379/{CACHE_REDIS_DB}"
CELERY_RESULT_BACKEND = f"redis://{CACHE_REDIS_HOST}:6379/{CACHE_REDIS_DB}"

if __name__ == '__main__':
    print(SQLALCHEMY_DATABASE_URI)
