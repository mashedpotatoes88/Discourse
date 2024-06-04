#!C:/Users/ADMIN/AppData/Local/Programs/Python/Python312/python
print("Content-Type:text/html")
print()

import discoursedbconn as dbconn

# INPUT STRING STORED IN VARIABLE

# SQL STATEMENTS TO EXECUTE INSERT
count = 85
for i in range(4):
    count += i
    sql_update = f"UPDATE questions SET communityId = '5', userId = '5' WHERE questionId = '{count}'"
    dbconn.mycursor.execute(sql_update)
    dbconn.conn.commit()

# CLOSING CURSOR AND CONNECTIONS OPENED BY discoursedbconn.py
dbconn.mycursor.close()
dbconn.conn.close()