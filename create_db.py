from sqlalchemy import create_engine, Table, Integer, String, Column, DateTime, MetaData

#engine = create_engine('sqlite:///tasks.db')
engine = create_engine("postgresql://xcnhbtjxnnbfuu:4f1961f672e831cf18722fb141ed5e304928a404cd2785ac0dc05bec11142f4d@ec2-34-255-134-200.eu-west-1.compute.amazonaws.com/d297cli1t1889p",echo = True)

meta = MetaData()

works = Table('works', meta,
    Column('id', Integer, primary_key = True),
    Column('worker', String),
    Column('fio', String),
    Column('date_start', String),
    Column('date_stop', String),
    Column('comment', String),
    Column('status', String),
    Column('done', String),
    Column('create', DateTime),
    Column('work', DateTime),
    Column('complete', DateTime),
              )


tasks = Table('tasks', meta,
    Column('id', Integer, primary_key = True),
    Column('task', String),
    Column('status', String),
    Column('fio', String),
    Column('create', DateTime),
    Column('work', DateTime),
    Column('complete', DateTime),
    Column('done', String),
)

users = Table('users', meta,
    Column('login', String, primary_key = True),
    Column('password', String),
)


meta.create_all(engine)





conn = engine.connect()
conn.execute( users.insert(),[
    {'login':'Глотов', 'password':'a12345678'},
    {'login':'Аслуева', 'password':'a12345678'},
    {'login':'Князев', 'password':'a12345678'},
    {'login':'Лучков', 'password':'a12345678'},
    {'login':'Ислямов', 'password':'a12345678'},
    {'login':'Котов', 'password':'a12345678'},
])