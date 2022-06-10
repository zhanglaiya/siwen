from sqlalchemy import (
    MetaData, Table, Column, Integer, String, DateTime, Boolean, PrimaryKeyConstraint)

metadata = MetaData()

tb_user = Table(
    'tb_user', metadata,
    Column('id', Integer, comment='id'),
    Column('username', String, comment='用户名'),
    Column('password', String, comment='密码'),
    Column('create_time', DateTime, comment='注册时间'),
    Column('disabled', Boolean, comment='注册时间'),
    PrimaryKeyConstraint('id', name='user_id')
)

