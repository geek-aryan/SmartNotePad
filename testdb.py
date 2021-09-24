from cx_Oracle import *
import traceback

con=None
try:
    conn=connect("mojo/mojo@127.0.0.1/xe")
    print('connected successfully to the db')
    print('db version:',conn.version)
    print('username',conn.username)
except DatabaseError:
    print("sorry connection failed")
    print(traceback.format_exc())
finally:
    if conn is not None:
        conn.close()
        print("disconnected successfull with the db")