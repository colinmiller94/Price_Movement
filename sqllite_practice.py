import sqlite3

#connect to existing database, or creates new database
conn = sqlite3.connect('employee.db')

#create cursor
c = conn.cursor()

# c.execute("""CREATE TABLE employees (
#             first text,
#             last text,
#             pay integer
#             )""")
for i in range(4):
    c.execute(" INSERT INTO employees values('Callie', 'Miller', 41209)")
c.execute("SELECT * from employees;")

print(c.fetchall())
# c.fetchman(5)
# c.fetchall()
#
# c.execute("delete from employees where first = 'Callie';")
# c.execute("SELECT * from employees;")
# print(c.fetchall())






conn.commit()
conn.close()