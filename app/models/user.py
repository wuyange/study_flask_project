from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from shortuuid import uuid
from datetime import datetime
from sqlalchemy.orm import validates
import re

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
    users = db.relationship("UserModel", back_populates='role')


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(30), default=uuid)
    username = db.Column(db.String(20), nullable=False, unique=True)
    _password = db.Column(db.String(200), nullable=False, name='password')
    email = db.Column(db.String(50), nullable=False, unique=True)
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    join_time = db.Column(db.DateTime, default=datetime.now)
    is_staff = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    # 外键
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("RoleModel", back_populates="users")

    @validates('username')
    def validate_username(self, key, username):
        assert len(username) >= 4 and len(username) <= 32, "用户名长度只能在4到32之间"
        assert re.match(r'^[A-Za-z0-9_]*$', username), "用户名只能由数字、字母和下划线组成"
        assert not UserModel.query.filter_by(username=username).all(), "用户名已经被注册"
        return username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password:str):
        self._password = generate_password_hash(password)

    def check_password(self, password:str):
        return check_password_hash(self._password, password)

    def has_permission(self, permission:PermissionEnum):
        return permission in [permission.name for permission in self.role.permissions]
