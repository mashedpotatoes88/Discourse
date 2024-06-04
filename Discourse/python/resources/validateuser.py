#!C:/Users/ADMIN/AppData/Local/Programs/Python/Python312/python
print("Content-Type: application/json")
print()

import os
import sys
import json
import discoursedbconn as dbconn

# READ JSON FROM STDIN
content_length = int(os.environ.get('CONTENT_LENGTH', 0))
json_data = sys.stdin.read(content_length)
data = json.loads(json_data)

# GETTING FORM INPUTS AND STORING IN VARIABLES
username_entry = data.get("username")
password_entry = data.get("password")


# CHECK IF USERNAME AND PASSWORD MATCH IN THE DB
sql_select = f"SELECT users.userId, users.username, users.communityId, users.radarCount, \
            users.notificationsCount, community.communityName FROM users JOIN community ON \
            users.communityId = community.communityId WHERE username = '{username_entry}' \
            AND password = '{password_entry}'"

dbconn.mycursor.execute(sql_select)
results = list(dbconn.mycursor.fetchall())

for result in results:
    result = list(result)
    for i in range(len(result)):
        if type(result[i]) == int:
            result[i] = str(result[i])
        else:
            continue

results = results[0]
# SEND THESE NUMBERS TO JAVASCRIPT
response = {'html_content': results}
json_response = json.dumps(response).strip()
print(json_response)

