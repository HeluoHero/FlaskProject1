from flask_mail import Message
from exts import mail
from celery import Celery


# 定义任务函数
def send_email(recipients, subject, body):
    message = Message(subject=subject, recipients=[recipients], body=body)
    mail.send(message)
    print('邮件发送成功')


# 创建celery对象
def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    app.celery = celery

    # 添加任务
    celery.task(name='send_email')(send_email)

    return celery
