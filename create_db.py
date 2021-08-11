from sqlalchemy import create_engine, Table, Integer, String, Column, DateTime, MetaData

engine = create_engine('sqlite:///tasks.db')

meta = MetaData()

tasks = Table('tasks', meta,
    Column('id', Integer, primary_key = True),
    Column('status', String),
    Column('fio', String),
    Column('create', DateTime),
    Column('work', DateTime),
    Column('comlete', DateTime),
)

users = Table('users', meta,
    Column('login', String, primary_key = True),
    Column('password', String),
)

meta.create_all(engine)

conn = engine.connect()
conn.execute( users.insert(),[
    {'login':'Ivanov', 'password':'11082021'},
    {'login':'Petrov', 'password':'12082021'},
    {'login':'Sidorov', 'password':'13082021'},
])