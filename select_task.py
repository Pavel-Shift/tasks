from sqlalchemy import create_engine, Table, Integer, String, Column, DateTime, MetaData, func, select

#engine = create_engine('sqlite:///tasks.db')

engine = create_engine("postgresql://xcnhbtjxnnbfuu:4f1961f672e831cf18722fb141ed5e304928a404cd2785ac0dc05bec11142f4d@ec2-34-255-134-200.eu-west-1.compute.amazonaws.com/d297cli1t1889p",echo = True)

meta = MetaData()

tasks = Table('tasks', meta,
    Column('id', Integer, primary_key = True),
    Column('task', String),
    Column('status', String),
    Column('fio', String),
    Column('create', DateTime),
    Column('work', DateTime),
    Column('complete', DateTime),
)

users = Table('users', meta,
    Column('login', String, primary_key = True),
    Column('password', String),
)

conn = engine.connect()

s = tasks.select()
result = conn.execute(s)

for row in result:
   print (row)

print('')

s = select([func.count()]).select_from(tasks)
result = conn.execute(s)

print(result.fetchone()[0] )

print('')
s = users.select()

result = conn.execute(s)

for row in result:
   print (row)