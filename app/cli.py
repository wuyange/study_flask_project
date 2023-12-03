from .models.user import PermissionModel, RoleModel, PermissionEnum, UserModel
import click
from .exts import db

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

def register_cli(app):

    app.cli.command("create-role")(create_role)
    app.cli.command("create-permission")(create_permission)
    app.cli.command("create-administrator")(create_administrator)