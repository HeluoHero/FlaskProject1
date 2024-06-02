from models.post import BoardModel
from exts import db


def init_boards():
    board_names = ['Python', 'Flask', 'Django', '爬虫', '前端']
    for index, board_name in enumerate(board_names):
        board = BoardModel(name=board_name, priority=len(board_names) - index)
        db.session.add(board)
    db.session.commit()
    print("初始化成功！")
