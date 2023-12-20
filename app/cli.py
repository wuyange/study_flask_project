from .models.user import PermissionModel, RoleModel, PermissionEnum, UserModel
from .models.post import *
from .exts import db

from faker import Faker
import random
import click

def create_permission():
    click.echo('-------')
    for permission in PermissionEnum:
        with db.auto_commit():
            db.session.add(PermissionModel(name=permission))
    click.echo("权限添加成功！")


def create_role():
    with db.auto_commit():
        # 稽查
        inspector = RoleModel(name="稽查",desc="负责审核帖子和评论是否合法合规！")
        inspector.permissions = PermissionModel.query.filter(PermissionModel.name.in_(
            [PermissionEnum.POST,PermissionEnum.COMMENT])).all()
        # 运营
        operator = RoleModel(name="运营",desc="负责网站持续正常运营！")
        operator.permissions = PermissionModel.query.filter(PermissionModel.name.notin_([
            PermissionEnum.CMS_USER
            ])).all()
        # 管理员
        administrator = RoleModel(name="管理员",desc="负责整个网站所有工作！")
        administrator.permissions = PermissionModel.query.all()
        db.session.add_all([inspector,operator,administrator])
    click.echo("角色添加成功！")

@click.option('--username', '-u')
@click.option('--password', '-p')
@click.option('--email', '-e')
def create_administrator(username, password, email):
    with db.auto_commit():
        user = UserModel(username=username, password=password, email=email)
        user.role = RoleModel.query.filter(RoleModel.name=='管理员').first()
        db.session.add(user)
        
def create_board():
    with db.auto_commit():
        board_names = ['Python语法', 'web开发', '测试开发', '运维开发']
        for board_name in board_names:
            board = BoardModel(name=board_name)
            db.session.add(board)
    click.echo("板块添加成功！")

@click.option('--num', '-n')
def create_test_post(num):
    fake = Faker(locale="zh_CN")
    author = UserModel.query.first()
    boards = BoardModel.query.all()
    click.echo("开始生成测试帖子...")
    with db.auto_commit():
        for _ in range(int(num)):
            title = fake.sentence()
            content = fake.paragraph(nb_sentences=10)
            random_index = random.randint(0,3)
            board = boards[random_index]
            post = PostModel(title=title, content=content, board=board, author=author)
            db.session.add(post)
    click.echo("测试帖子生成成功！")

def register_cli(app):

    app.cli.command("create-role")(create_role)
    app.cli.command("create-permission")(create_permission)
    app.cli.command("create-administrator")(create_administrator)
    app.cli.command("create-board")(create_board)
    app.cli.command("create-test-post")(create_test_post)
