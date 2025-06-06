#!C:/Users/ADMIN/AppData/Local/Programs/Python/Python312/python
print("Content-Type: application/json")
print()

import discoursedbconn as dbconn
import json

def fetch_user_profile(userId):
    sql_select = f"""SELECT users.userId,\
                        users.username,\
                        users.communityId,\
                        community.communityName,\
                        users.yearJoined\
                        FROM users\
                        JOIN community ON users.communityId = community.communityId\
                        WHERE users.userId = '{userId}' """
    
    # EXECUTE SQL STATEMENT
    dbconn.mycursor.execute(sql_select)
    result = dbconn.mycursor.fetchall()[0]

    # INSERT DATA INTO TEMPLATE
    response = dbconn.template_user_profile % (result[0], result[1], result[2], result[3], result[4])
    return response

data = dbconn.read_json_input()
userId = data.get("userId")

# userId = 1

# MAIN
content = fetch_user_profile(userId)

# RETURN JSON
response = {"html_content" : content}
json_response = json.dumps(response)
print(json_response)

dbconn.mycursor.close()
dbconn.conn.close()