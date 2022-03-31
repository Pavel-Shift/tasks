import psycopg2


con = psycopg2.connect(dbname='d297cli1t1889p', user='xcnhbtjxnnbfuu',
                       password='4f1961f672e831cf18722fb141ed5e304928a404cd2785ac0dc05bec11142f4d',
                       host='ec2-34-255-134-200.eu-west-1.compute.amazonaws.com')


cur = con.cursor()
cur.execute("ALTER TABLE USERS ADD COLUMN ID VARCHAR(9)")

con.commit()
con.close()
