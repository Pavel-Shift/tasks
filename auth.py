from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

engine = create_engine('sqlite:///tasks.db', echo=True)
meta = MetaData()

users = Table('users', meta,
                Column('login', String, primary_key=True),
                  Column('password', String),
                  )

conn = engine.connect()
s = users.select().where(users.c.login == 'Sidorov', users.c.password == '13082021')
result = conn.execute(s)

print(len(result.fetchall()))
