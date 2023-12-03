from enum import Enum
from . import Base
from app.exts import db

class PermissionEnum(Enum):
    BOARD = "板块"
    POST = "帖子"
    COMMENT = "评论"
    FRONT_USER = "前台用户"
    CMS_USER = "后台用户"

permission_role_table = db.Table(
    'permission_role_table',
    db.Column("permission_id", db.Integer, db.ForeignKey("permission.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"))
)


class PermissionModel(Base):
    __tablename__ = "permission"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Enum(PermissionEnum), nullable=False, unique=True)
    roles = db.relationship("RoleModel", secondary=permission_role_table, back_populates='permissions')


class RoleModel(Base):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    desc = db.Column(db.String(255))
    permissions = db.relationship("PermissionModel", secondary=permission_role_table, back_populates='roles')